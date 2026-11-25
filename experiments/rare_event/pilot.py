"""CPU pilot: budget-matched replay for a rare, mid-trajectory tool failure."""

import argparse
import copy
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import t

MODEL = "Qwen/Qwen2.5-0.5B"
REVISION = "060db6499f32faf8b98477b0a26969ef7d8b9987"
SEEDS = (421, 422, 423)
MODES = ("mopd", "mopd_tilted", "uniform_prefix", "prompt_upsampling", "split", "terminal_replay")
FEATURE_SCHEMA = 2
RISK = np.array([0.025, 0.075])
FAIL_GIVEN_RISK = 0.02
NEW_RISK = 0.60
NEW_FAIL_GIVEN_RISK = 0.30
RARE_TILT = 100.0
SPLIT_CHILDREN = 4
OLD_BATCH = 512
OLD_STEPS = 512
NEW_BATCH = 32
NEW_STEPS = 512
REPLAY_BATCH = 8
REPLAY_SCALE = 0.25
COMMON_MARGIN = 0.01
OBJECTS = ("crate", "tote", "box", "bin", "tray", "cart", "rack", "case")
TRAIN = tuple((kind, obj, i) for kind in range(2) for obj in OBJECTS[:4] for i in (12, 24, 36))
TEST = tuple((kind, obj, i) for kind in range(2) for obj in OBJECTS[4:] for i in (15, 27, 39))
PROMPTS = TRAIN + TEST
P = len(TRAIN)
N = len(PROMPTS)
NORMAL, BUSY, JAM = range(3)


def prompt(kind, obj, number):
    return f"Warehouse. {'Move' if kind else 'Scan'} {obj} {number}. Route (A/B):"


def make_features(cache, model_dir):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    source = model_dir or MODEL
    tokenizer = AutoTokenizer.from_pretrained(source, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(source, revision=REVISION).eval()
    model.requires_grad_(False)
    tokenizer.padding_side = "left"
    roots = [prompt(*item) for item in PROMPTS]
    strings = roots + [
        prompt(*item) + f" {action}. Scanner {domain}: {status}. Next command (C/D):"
        for domain in ("X", "Y")
        for item in PROMPTS
        for action in ("A", "B")
        for status in ("ready", "busy but ready", "paper jam")
    ]
    ids = [tokenizer.encode(f" {a}", add_special_tokens=False) for a in "ABCD"]
    if any(len(ids_) != 1 for ids_ in ids):
        raise ValueError(f"Action codes must each map to one token: {ids}")
    rows = model.lm_head.weight[[x[0] for x in ids]]
    hidden = []
    with torch.inference_mode():
        for start in range(0, len(strings), 16):
            batch = tokenizer(strings[start : start + 16], padding=True, return_tensors="pt")
            encoding = model.model(**batch, use_cache=False).last_hidden_state[:, -1]
            hidden.append(encoding.float())
    hidden = torch.cat(hidden)
    base = hidden @ rows.float().T
    scale = math.sqrt(hidden.shape[-1])
    data = {
        "root": (base[:N, 1] - base[:N, 0]).sigmoid(),
        "z": (hidden[N:] / scale).reshape(2, N, 2, 3, -1),
        "base": (base[N:, 3] - base[N:, 2]).reshape(2, N, 2, 3),
        "params": sum(p.numel() for p in model.parameters()),
        "schema": FEATURE_SCHEMA,
        "revision": REVISION,
    }
    torch.save(data, cache)


class Policy(torch.nn.Module):
    def __init__(self, features):
        super().__init__()
        self.z = features["z"]
        self.base = features["base"]
        self.adapter = torch.nn.Parameter(torch.zeros(self.z.shape[-1]))

    def logits(self, domain, starts, status):
        prompts, actions = starts.T
        return self.base[domain, prompts, actions, status] + self.z[
            domain, prompts, actions, status
        ] @ self.adapter

    def all_logits(self, domain):
        return self.base[domain] + self.z[domain] @ self.adapter


def root(rng, size, route, upsampling=False):
    # Only rates at the common prompt-family level are available at the root.
    probs = np.repeat(RISK / RISK.sum() / (P // 2), P // 2) if upsampling else None
    prompts = rng.choice(P, size=size, p=probs)
    return np.column_stack((prompts, rng.random(size) < route[prompts]))


def checkpoint(rng, starts):
    families = (starts[:, 0] >= P // 2).astype(int)
    return rng.random(len(starts)) < RISK[families]


def continue_from(rng, high, fail=FAIL_GIVEN_RISK):
    return np.where(high, np.where(rng.random(len(high)) < fail, JAM, BUSY), NORMAL)


def natural(rng, size, route, upsampling=False):
    starts = root(rng, size, route, upsampling)
    high = checkpoint(rng, starts)
    return starts, high, continue_from(rng, high)


def new_domain(rng, size, route):
    starts = root(rng, size, route)
    high = rng.random(size) < NEW_RISK
    return starts, high, continue_from(rng, high, NEW_FAIL_GIVEN_RISK)


def mass(starts, category, count):
    result = np.zeros((P, 2, count))
    np.add.at(result, (*starts.T, category.astype(int)), 1 / len(starts))
    return result


class Replay:
    def __init__(self, route, archive):
        self.route = route
        self.starts, self.high, self.status = archive
        self.high_index = np.flatnonzero(self.high)
        self.jam_index = np.flatnonzero(self.status == JAM)
        if not len(self.jam_index):
            raise ValueError("Old archive must contain a naturally occurring jam")
        start_mass = np.column_stack((1 - route, route)) / P
        high_prob = np.repeat(RISK, P // 2)[:, None]
        transition = np.array([0.0, 1 - FAIL_GIVEN_RISK, FAIL_GIVEN_RISK])
        self.p = start_mass[..., None] * (
            (1 - high_prob[..., None]) * np.eye(3)[NORMAL] + high_prob[..., None] * transition
        )
        self.target = self.p * np.array([1.0, 1.0, RARE_TILT])
        self.target /= self.target.sum()
        archived_checkpoint = mass(self.starts, self.high, 2)
        archived_suffix = mass(self.starts, self.status, 3)
        high = mass(self.starts[self.high_index], self.high[self.high_index], 2)[..., 1]
        jam = mass(self.starts[self.jam_index], self.status[self.jam_index], 3)
        self.q = {
            "mopd": self.p,
            "mopd_tilted": self.p,
            "prompt_upsampling": self.p * np.repeat(RISK / RISK.mean(), P // 2)[:, None, None],
            "uniform_prefix": (
                self.p + archived_checkpoint[..., 0, None] * np.eye(3)[NORMAL]
                + archived_checkpoint[..., 1, None] * transition + archived_suffix
            ) / 3,
            "split": (self.p + high[..., None] * transition) / 2,
            "terminal_replay": (self.p + jam) / 2,
        }

    def sample(self, rng, mode, size):
        if mode == "uniform_prefix":
            depth = rng.integers(0, 3, size)
            idx = rng.integers(len(self.starts), size=size)
            starts = self.starts[idx].copy()
            starts[depth == 0] = root(rng, (depth == 0).sum(), self.route)
            fresh = checkpoint(rng, starts)
            high = np.where(depth == 0, fresh, self.high[idx])
            status = np.where(depth == 2, self.status[idx], continue_from(rng, high))
            actual_roots = int((depth == 0).sum())
            transitions = int((depth < 2).sum())
        elif mode in {"split", "terminal_replay"}:
            if size % (2 * SPLIT_CHILDREN):
                raise ValueError("Replay batch must be divisible by twice the split fanout")
            starts, _, status = natural(rng, size // 2, self.route)
            if mode == "split":
                idx = rng.choice(self.high_index, size=size // (2 * SPLIT_CHILDREN))
                idx = np.repeat(idx, SPLIT_CHILDREN)
                suffix = continue_from(rng, self.high[idx])
                transitions = size
            else:
                idx = rng.choice(self.jam_index, size=size // 2)
                suffix = self.status[idx]
                transitions = size // 2
            starts = np.concatenate((starts, self.starts[idx]))
            status = np.concatenate((status, suffix))
            actual_roots = size // 2
        else:
            starts, _, status = natural(rng, size, self.route, mode == "prompt_upsampling")
            actual_roots = transitions = size
        indices = (*starts.T, status)
        target = self.p if mode == "mopd" else self.target
        return starts, status, target[indices] / self.q[mode][indices], actual_roots, transitions


def labels(domain, status):
    return torch.from_numpy(status == (JAM if domain == 0 else BUSY)).float()


def train_old(policy, route, rng, old_steps):
    opt = torch.optim.AdamW(policy.parameters(), lr=0.08, weight_decay=0.0)
    batches = []
    for _ in range(old_steps):
        old = natural(rng, OLD_BATCH, route)
        starts, _, status = old
        batches.append(old)
        opt.zero_grad()
        F.binary_cross_entropy_with_logits(policy.logits(0, starts, status), labels(0, status)).backward()
        opt.step()
    return tuple(np.concatenate(fields) for fields in zip(*batches))


def reverse_kl(logits, teacher):
    student_logp = F.logsigmoid(torch.stack((-logits, logits), -1))
    teacher_logp = F.logsigmoid(torch.stack((-teacher, teacher), -1))
    return (student_logp.exp() * (student_logp - teacher_logp)).sum(dim=-1)


def adapt(previous, new_batches, replay, mode, seed):
    policy = copy.deepcopy(previous)
    opt = torch.optim.AdamW(policy.parameters(), lr=0.006, weight_decay=0.0)
    rng = np.random.default_rng(seed)
    budget = dict(
        replay_rollouts=0, replay_teacher_positions=0, replay_sampled_actions=0,
        replay_root_actions=0, replay_tool_transitions=0, replay_jams=0,
        replay_unique_jam_states=0, new_rollouts=0, new_teacher_positions=0,
    )
    jam_states = set()
    for starts_new, _, status_new in new_batches:
        opt.zero_grad()
        loss = F.binary_cross_entropy_with_logits(
            policy.logits(1, starts_new, status_new), labels(1, status_new)
        )
        budget["new_rollouts"] += len(status_new)
        budget["new_teacher_positions"] += len(status_new)
        if mode != "none":
            starts, status, weight, roots, transitions = replay.sample(rng, mode, REPLAY_BATCH)
            student = policy.logits(0, starts, status)
            with torch.no_grad():
                target = previous.logits(0, starts, status)
                # Constrained one-token actions: KL integrates both possible samples exactly.
                actions = rng.random(len(status)) < student.sigmoid().numpy()
            loss = loss + REPLAY_SCALE * (reverse_kl(student, target) * torch.from_numpy(weight).float()).mean()
            budget["replay_rollouts"] += len(status)
            budget["replay_teacher_positions"] += len(target)
            budget["replay_sampled_actions"] += len(actions)
            budget["replay_root_actions"] += roots
            budget["replay_tool_transitions"] += transitions
            budget["replay_jams"] += int((status == JAM).sum())
            jam_states.update(map(tuple, starts[status == JAM]))
        loss.backward()
        opt.step()
    budget["replay_unique_jam_states"] = len(jam_states)
    return policy, budget


@torch.no_grad()
def evaluate(policy, features):
    route = features["root"][P:].numpy()
    route_prob = np.column_stack((1 - route, route))
    high = RISK[[item[0] for item in TEST]]
    weight = np.column_stack((1 - high, high * (1 - FAIL_GIVEN_RISK), high * FAIL_GIVEN_RISK))
    old_weight = weight[:, None, :] * route_prob[..., None]
    new_weight = route_prob[..., None] * np.array(
        [1 - NEW_RISK, NEW_RISK * (1 - NEW_FAIL_GIVEN_RISK), NEW_RISK * NEW_FAIL_GIVEN_RISK]
    )
    old = policy.all_logits(0)[P:].sigmoid().numpy()
    new = policy.all_logits(1)[P:].sigmoid().numpy()
    new_correct = 1 - new
    new_correct[..., BUSY] = new[..., BUSY]

    def score(weight, prob, indices):
        mass = weight[..., indices]
        return float((mass * prob[..., indices]).sum() / mass.sum())

    return {
        "old_rare": score(old_weight, old, [JAM]),
        "old_common": score(old_weight, 1 - old, [NORMAL, BUSY]),
        "new_common": score(new_weight, new_correct, [NORMAL, BUSY]),
        "new_jam": score(new_weight, new_correct, [JAM]),
    }


def interval(values):
    data = np.array(values)
    mean = float(data.mean())
    half = float(t.ppf(0.975, len(data) - 1) * data.std(ddof=1) / math.sqrt(len(data)))
    return dict(mean=mean, low=mean - half, high=mean + half)


def summarize(runs):
    metrics = ("old_rare", "old_common", "new_common", "new_jam")
    scores = {
        mode: {metric: interval([r[mode][metric] for r in runs]) for metric in metrics}
        for mode in ("before", "none", *MODES)
    }
    controls = tuple(mode for mode in MODES if mode != "split")
    splits_minus = {
        mode: {
            metric: interval([r["split"][metric] - r[mode][metric] for r in runs])
            for metric in metrics
        } for mode in controls
    }
    gate_valid = scores["before"]["old_rare"]["mean"] >= 0.80 and (
        scores["before"]["old_rare"]["mean"] - scores["none"]["old_rare"]["mean"] >= 0.10
    ) and all(scores["none"][m]["mean"] >= 0.80 for m in ("new_common", "new_jam"))
    keep = all(
        v["old_rare"]["low"] > 0
        and v["old_common"]["mean"] >= 0
        and v["old_common"]["low"] >= -COMMON_MARGIN
        for v in splits_minus.values()
    )
    keep &= all(scores["split"][m]["mean"] >= 0.80 for m in ("new_common", "new_jam"))
    return dict(scores=scores, split_minus=splits_minus, validity_gate=gate_valid,
                verdict=("keep" if keep else "kill") if gate_valid else "invalid")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--model-dir", help="Optional local copy of the pinned model snapshot")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--features-only", action="store_true")
    parser.add_argument("--dev-seed", type=int)
    args = parser.parse_args()
    if not args.features_only and args.output is None:
        parser.error("--output is required unless using --features-only")
    torch.set_num_threads(args.threads)
    start = time.perf_counter()
    if not args.cache.exists():
        make_features(args.cache, args.model_dir)
    feature_seconds = time.perf_counter() - start
    if args.features_only:
        print(f"Features ready in {feature_seconds:.2f}s", flush=True)
        return
    features = torch.load(args.cache, weights_only=True)
    if features.get("schema") != FEATURE_SCHEMA or features.get("revision") != REVISION:
        parser.error("cache was built with a different model or feature schema; use a new path")
    route = features["root"][:P].numpy()
    seeds = (args.dev_seed,) if args.dev_seed is not None else SEEDS
    runs = []
    for seed in seeds:
        begin = time.perf_counter()
        old_rng, new_rng = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(2)]
        previous = Policy(features)
        archive = train_old(previous, route, old_rng, OLD_STEPS)
        replay = Replay(route, archive)
        new_batches = [new_domain(new_rng, NEW_BATCH, route) for _ in range(NEW_STEPS)]
        result = dict(seed=seed, old_rollouts=len(archive[0]), old_jams=len(replay.jam_index),
                      old_high=len(replay.high_index), before=evaluate(previous, features))
        for mode in ("none", *MODES):
            policy, budget = adapt(previous, new_batches, replay, mode, seed + 10000)
            result[mode] = {**evaluate(policy, features), **budget}
        result["seconds"] = time.perf_counter() - begin
        runs.append(result)
        print(json.dumps(result), flush=True)
    output = {
        "model": MODEL, "revision": REVISION, "model_params": features["params"],
        "trainable_params": features["z"].size(-1), "feature_seconds": feature_seconds,
        "torch": str(torch.__version__), "numpy": np.__version__, "threads": args.threads,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "unadapted_qwen": evaluate(Policy(features), features),
        "runs": runs,
    }
    if len(runs) > 1:
        output.update(summarize(runs))
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
