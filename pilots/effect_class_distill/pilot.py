import argparse
import json
import statistics
import time
from pathlib import Path

import torch

from decoder import MODEL, REVISION, Policy, build_cache, fingerprint
from stream import PROBES, UNIT_TESTS, canonicalize, parse, prompts


SEEDS = (101, 202, 303)
METHODS = ("effect", "token", "reward")
WEIGHTS = (0.25, 1.0, 4.0)


def setup():
    data, splits = prompts()
    codes = [list(prompt.candidates()) for prompt in data]
    calls = [[parse(c, prompt.variables) for c in row] for prompt, row in zip(data, codes)]
    targets = {
        new: torch.tensor([row.index(p.target(new)) for p, row in zip(data, codes)])
        for new in (False, True)
    }
    names = [canonicalize(c) for c in calls[0]]
    groups = list(dict.fromkeys(names))
    ids = [groups.index(name) for name in names]
    assert all([canonicalize(c) for c in row] == names for row in calls)
    members = torch.tensor([[i for i, group in enumerate(ids) if group == j] for j in range(len(groups))])
    return data, splits, calls, targets, torch.tensor(ids), members


def execute_batch(data, calls, rows, samples):
    return [[data[row].observe(calls[row][i]) for i in codes] for row, codes in zip(rows, samples)]


def auxiliary(method, log_probs, teacher_samples, student_samples, teacher, student, canonical_ids, members):
    if method == "token":
        canonical_log_probs = log_probs[:, members].logsumexp(-1)
        return -canonical_log_probs.gather(1, canonical_ids[teacher_samples]).mean()
    sampled_log_probs = log_probs.gather(1, student_samples)
    if method == "effect":
        weights = effect_weights(teacher, student)
    else:
        weights = torch.tensor([[float(passed) for _, passed in row] for row in student])
    return -(weights * sampled_log_probs).mean()


def effect_weights(teacher, student):
    weights = []
    for teacher_row, student_row in zip(teacher, student):
        t = [signature for signature, _ in teacher_row]
        s = [signature for signature, _ in student_row]
        weights.append([t.count(signature) / s.count(signature) for signature in s])
    return torch.tensor(weights)


def schedule(rows, steps, batch, generator):
    rows = torch.tensor(rows)
    shuffled = torch.cat([
        rows[torch.randperm(len(rows), generator=generator)]
        for _ in range((steps * batch + len(rows) - 1) // len(rows))
    ])
    return shuffled[: steps * batch].reshape(steps, batch)


def supervised(policy, rows, targets):
    return -policy(rows).gather(1, targets[rows, None]).mean()


@torch.no_grad()
def measure(policy, data, calls, rows):
    outcomes = execute_batch(data, calls, rows, [range(len(calls[row])) for row in rows])
    passed = torch.tensor([[float(ok) for _, ok in row] for row in outcomes])
    new = torch.tensor([[float(c.new) for c in calls[row]] for row in rows])
    probs = policy(torch.tensor(rows)).exp()
    return {
        "pass": (probs * passed).sum(1).mean().item(),
        "adoption": (probs * new).sum(1).mean().item(),
        "pass_and_adoption": (probs * passed * new).sum(1).mean().item(),
    }


def evaluate(policy, data, calls, splits):
    return {split: measure(policy, data, calls, splits[split]) for split in ("old_eval", "new_eval")}


def run_seed(seed, cache, problem, args):
    data, splits, calls, targets, ids, members = problem
    torch.manual_seed(seed)
    rng = torch.Generator().manual_seed(seed)
    policy = Policy(cache)
    before = evaluate(policy, data, calls, splits)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=args.lr)
    for rows in schedule(splits["old_train"], args.steps, args.batch, rng):
        optimizer.zero_grad()
        supervised(policy, rows, targets[False]).backward()
        optimizer.step()
    old = evaluate(policy, data, calls, splits)
    teacher = policy(torch.arange(len(data))).detach().exp()
    checkpoint = {name: tensor.detach().clone() for name, tensor in policy.state_dict().items()}
    new_schedule = schedule(splits["new_train"], args.steps, args.batch, rng)
    replay_schedule = schedule(splits["old_train"], args.steps, args.batch, rng)
    runs = {}
    for method, weight in [("naive", 0.0)] + [(m, w) for m in METHODS for w in WEIGHTS]:
        start = time.monotonic()
        policy.load_state_dict(checkpoint)
        optimizer = torch.optim.AdamW(policy.parameters(), lr=args.lr)
        sampler = torch.Generator().manual_seed(10_000 + seed)
        completions = 0
        for rows, replay_rows in zip(new_schedule, replay_schedule):
            migration_loss = supervised(policy, rows, targets[True])
            replay = policy(replay_rows)
            with torch.no_grad():
                ts = torch.multinomial(teacher[replay_rows], args.samples, replacement=True, generator=sampler)
                ss = torch.multinomial(replay.exp(), args.samples, replacement=True, generator=sampler)
                t = execute_batch(data, calls, replay_rows.tolist(), ts.tolist())
                s = execute_batch(data, calls, replay_rows.tolist(), ss.tolist())
                completions += sum(map(len, t)) + sum(map(len, s))
            loss = migration_loss
            if method != "naive":
                loss = loss + weight * auxiliary(method, replay, ts, ss, t, s, ids, members)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        assert completions == 2 * args.batch * args.samples * args.steps
        key = f"{method}:{weight:g}"
        metrics = evaluate(policy, data, calls, splits)
        runs[key] = dict(metrics, completions=completions,
                         executions=completions * (len(PROBES) + len(UNIT_TESTS)),
                         seconds=time.monotonic() - start)
        print(f"{seed} {key} {json.dumps(runs[key], sort_keys=True)}", flush=True)
    return {"seed": seed, "pretrained": before, "old_checkpoint": old, "runs": runs}


def hypervolume(points):
    area = 0.0
    highest = 0.0
    for adoption, retention in sorted(points, reverse=True):
        if retention > highest:
            area += adoption * (retention - highest)
            highest = retention
    return area


def interval(values):
    assert len(values) == 3
    mean = statistics.mean(values)
    radius = 4.3026527297 * statistics.stdev(values) / (len(values) ** 0.5)
    return [mean, mean - radius, mean + radius]


def summarize(seeds):
    areas = {}
    for method in METHODS:
        areas[method] = []
        for seed in seeds:
            front = [run["old_eval"] for key, run in seed["runs"].items()
                     if key.startswith(method + ":") or key == "naive:0"]
            areas[method].append(hypervolume((x["adoption"], x["pass"]) for x in front))
    deltas = {
        control: interval([a - b for a, b in zip(areas["effect"], areas[control])])
        for control in METHODS if control != "effect"
    }
    return {
        "verdict": "KEEP" if all(ci[1] > 0 for ci in deltas.values()) else "KILL",
        "hypervolume_by_seed": areas,
        "hypervolume_ci": {method: interval(values) for method, values in areas.items()},
        "paired_delta_ci": deltas,
    }


def main():
    parser = argparse.ArgumentParser(description="CPU pilot for effect-class replay under an API migration")
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--cache-threads", type=int, default=8)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--batch", type=int, default=12)
    parser.add_argument("--samples", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.003)
    args = parser.parse_args()
    if min(args.steps, args.batch, args.samples, args.cache_threads) < 1 or args.lr <= 0:
        parser.error("steps, batch size, sample count, threads and learning rate must be positive")
    problem = setup()
    data, splits, *_ = problem
    if not args.cache.is_file():
        torch.set_num_threads(args.cache_threads)
        build_cache(data, args.cache, args.model)
    torch.set_num_threads(1)
    cache = torch.load(args.cache, weights_only=True)
    if cache["fingerprint"] != fingerprint(data):
        parser.error("cache is not compatible with this stream/model revision")
    with torch.no_grad():
        assert torch.allclose(Policy(cache)(torch.arange(len(data))).exp().sum(1), torch.ones(len(data)))
    seeds = [run_seed(seed, cache, problem, args) for seed in SEEDS]
    result = {
        "design": dict(model=MODEL, revision=REVISION, steps=args.steps, batch=args.batch,
                       samples=args.samples, lr=args.lr, sizes={k: len(v) for k, v in splits.items()}),
        "seeds": seeds,
        "summary": summarize(seeds),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
