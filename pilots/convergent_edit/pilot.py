import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import asdict, dataclass
from itertools import islice
import json
from pathlib import Path
import random
import re
import sys

import numpy as np
from scipy.stats import rankdata

from .backends import ResponseCache, backends, correct
from .environment import HELD_OUT, SEEDS, TRAIN, make_task


@dataclass(frozen=True)
class Trace:
    family: str
    index: int
    seed: int
    edit: str
    before: bool
    after: bool


def batches(items, size):
    return (items[i:i + size] for i in range(0, len(items), size))


def discover(evolver, model, train, pool, batch_size):
    def first_attempt(task):
        seed = SEEDS[task.index % len(SEEDS)] + 100 * TRAIN.index(task.family)
        return task, seed, model.solve(task, (), seed)

    def propose(batch):
        if len(batch) == 1:
            task, seed, before = batch[0]
            edits = [evolver.edit(task, before, seed)]
        else:
            batch_seed = SEEDS[(batch[0][0].index // batch_size) % len(SEEDS)] + 100 * TRAIN.index(batch[0][0].family)
            edits = evolver.edit_batch([(task, before) for task, _, before in batch], batch_seed)
        return [(*attempt, edit) for attempt, edit in zip(batch, edits) if edit is not None]

    def retry(item):
        task, seed, before, edit = item
        after = model.solve(task, (edit,), seed)
        return Trace(task.family, task.index, seed, edit, correct(task, before), correct(task, after))

    before = list(pool.map(first_attempt, (task for family in TRAIN for task in train[family])))
    grouped = [chunk for family in TRAIN for chunk in batches([r for r in before if r[0].family == family], batch_size)]
    proposed = [item for batch in pool.map(propose, grouped) for item in batch]
    return list(pool.map(retry, proposed))


def terms(edit):
    return Counter(re.findall(r"[a-z0-9]+", edit.casefold()))


def similarity(a, b):
    numbers = lambda counts: {t for t in counts if t.isdecimal()}
    if numbers(a) != numbers(b):
        return 0.0
    return sum((a & b).values()) / max(1, sum((a | b).values()))


def medoid(items):
    texts = sorted({item.edit for item in items})
    tokens = [terms(edit) for edit in texts]
    return texts[max(range(len(texts)), key=lambda i: sum(similarity(tokens[i], t) for t in tokens))]


def cluster(traces, threshold=0.78):
    groups = []
    for edit in sorted({trace.edit for trace in traces}):
        for group in groups:
            if all(similarity(terms(edit), terms(other)) >= threshold for other in group):
                group.add(edit)
                break
        else:
            groups.append({edit})
    return [[trace for trace in traces if trace.edit in group] for group in groups]


def accuracy(model, edits, cases, pool):
    return np.fromiter(grade_many(model, ((edits, case) for case in cases), pool), dtype=float)


def grade_many(model, rollouts, pool):
    def grade(rollout):
        edits, (task, seed, variant) = rollout
        return correct(task, model.solve(task, edits, seed, variant))

    return pool.map(grade, rollouts)


def paired(model, before, after, cases, pool):
    return accuracy(model, after, cases, pool) - accuracy(model, before, cases, pool)


def gate_stats(matrix):
    seed_variance = float(np.mean(matrix.var(axis=1, ddof=1)))
    spread = float(max(0, matrix.mean(axis=1).var(ddof=1) - seed_variance / matrix.shape[1]))
    ratio = spread / seed_variance if seed_variance else None
    return spread, seed_variance, ratio


def ci(draws):
    values = [x for x in draws if x is not None and np.isfinite(x)]
    return [float(x) for x in np.quantile(values, [0.025, 0.975])] if values else None


def rho(a, b):
    if len(a) < 2 or np.ptp(a) == 0 or np.ptp(b) == 0:
        return None
    return float(np.corrcoef(rankdata(a), rankdata(b))[0, 1])


ARMS = ("breadth", "lofo", "counterfactual", "frequency", "ace", "continued")


def select(model, evolver, groups, edits, train, blocks, top_k, pool, curation_batch_size):
    scores = {arm: np.zeros(len(edits)) for arm in ARMS}
    evidence = [(edit, [asdict(t) for t in group]) for edit, group in zip(edits, groups)]
    def curate(batch):
        if len(batch) == 1:
            edit, traces = batch[0]
            return [evolver.curate(edit, traces, SEEDS[0])]
        return evolver.curate_batch(batch, SEEDS[0])

    scores["ace"] = np.array([score for batch in pool.map(curate, batches(evidence, curation_batch_size))
                              for score in batch], dtype=float)
    rng = random.Random(8223)
    order = list(range(len(edits)))
    rng.shuffle(order)
    accepted = []
    for i in order:
        group = groups[i]
        edit = edits[i]
        frequencies = Counter(t.family for t in group)
        scores["breadth"][i] = len(frequencies)
        scores["frequency"][i] = max(frequencies.values())

        # Sample only non-origin tasks, without replacement when the pool allows it.
        origins = {(t.family, t.index) for t in group}
        def samples(family, count):
            candidates = [t for t in train[family] if (family, t.index) not in origins]
            if not candidates:
                candidates = train[family]
            full, rest = divmod(count, len(candidates))
            return candidates * full + rng.sample(candidates, rest)

        eligible = [(family, medoid([t for t in group if t.family != family])) for family in TRAIN
                    if any(t.family != family for t in group)]
        fold_cases = {fold_edit: [] for _, fold_edit in eligible}
        for seed in SEEDS:
            for family, fold_edit in eligible:
                count = 3 * blocks // len(eligible)
                count += eligible.index((family, fold_edit)) < (3 * blocks % len(eligible))
                fold_cases[fold_edit].extend((t, seed, 0) for t in samples(family, count))
        scores["lofo"][i] = np.concatenate([
            paired(model, (), (fold_edit,), cases, pool) for fold_edit, cases in fold_cases.items() if cases
        ]).mean()

        origins_families = sorted(frequencies)
        anchors = [(t, seed) for si, seed in enumerate(SEEDS)
                   for t in samples(origins_families[si % len(origins_families)], blocks)]
        challenge = [paired(model, (), (edit,), [(t, seed, v) for t, seed in anchors], pool).mean()
                     for v in range(3)]
        scores["counterfactual"][i] = min(challenge)
        selection_cases = [(t, seed, 0) for si, seed in enumerate(SEEDS)
                           for t in samples(origins_families[si % len(origins_families)], 3 * blocks)]
        for arm in ("breadth", "frequency", "ace"):
            paired(model, (), (edit,), selection_cases, pool)  # Matched, blinded rollout spend.

        incumbent = tuple(edits[j] for j in accepted)
        gain = paired(model, incumbent, (*incumbent, edit), selection_cases, pool).mean()
        scores["continued"][i] = gain
        if gain > 0 and len(accepted) < top_k:
            accepted.append(i)

    promoted = {
        arm: sorted(range(len(edits)), key=lambda i: (-values[i], order.index(i)))[:top_k]
        for arm, values in scores.items()
    }
    # Continue the actual online path, not a counterfactual reranking of its proposals.
    promoted["continued"] = accepted
    promoted["breadth"] = [i for i in promoted["breadth"] if scores["breadth"][i] > 1]
    return scores, promoted


def run(args, cache=None):
    evolver, model, evolver_name, task_name = backends(args.backend, cache)
    train = {f: [make_task(f, i) for i in range(args.tasks)] for f in TRAIN}
    test = [make_task(HELD_OUT, i) for i in range(args.held_out_tasks)]
    cases = [(t, seed, 0) for seed in SEEDS for t in test]
    rng = np.random.default_rng(9382)
    result = dict(backend=args.backend, evolver_model=evolver_name, task_model=task_name,
                  seeds=SEEDS, tasks_per_training_family=args.tasks, held_out_tasks=len(test),
                  validation_blocks=args.validation_blocks,
                  top_k=args.top_k, bootstrap=args.bootstrap, proposal_batch_size=args.proposal_batch_size,
                  curation_batch_size=args.curation_batch_size,
                  proposal_requests=len(TRAIN) * ((args.tasks + args.proposal_batch_size - 1) // args.proposal_batch_size))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        traces = discover(evolver, model, train, pool, args.proposal_batch_size)
        groups = cluster(traces)
        edits = [medoid(group) for group in groups]
        result.update(traces=[asdict(t) for t in traces], clusters=edits,
                      cluster_members=[[{"family": t.family, "index": t.index} for t in group]
                                       for group in groups])
        print(f"Discovery: {len(traces)} edits, {len(edits)} clusters", file=sys.stderr, flush=True)
        if len(edits) < 2:
            result["verdict"] = "stop: fewer than two clusters; variance undefined"
            return result

        baseline = accuracy(model, (), cases, pool)
        labels = []
        truth_rollouts = grade_many(model, (((edit,), case) for edit in edits for case in cases), pool)
        for i, edit in enumerate(edits, 1):
            labels.append((np.fromiter(islice(truth_rollouts, len(cases)), dtype=float) - baseline)
                          .reshape(len(SEEDS), -1))
            if i == len(edits) or i % 10 == 0:
                print(f"Truth: {i}/{len(edits)} clusters", file=sys.stderr, flush=True)
        matrix = np.array(labels).mean(axis=2)
        spread, noise, ratio = gate_stats(matrix)
        draws = rng.integers(len(edits), size=(args.bootstrap, len(edits)))
        gate_boot = [gate_stats(matrix[idx]) for idx in draws]
        result.update(
            baseline_accuracy=float(baseline.mean()),
            seed_gains=matrix.tolist(),
            gate=dict(between_cluster_variance=spread, seed_variance=noise, ratio=ratio,
                      ratio_ci=ci([r for _, _, r in gate_boot]),
                      difference_ci=ci([b - s for b, s, _ in gate_boot]),
                      passed=bool(len(edits) >= 40 and spread > noise)),
        )
        print(f"Gate: {json.dumps(result['gate'])}", file=sys.stderr, flush=True)
        if not result["gate"]["passed"]:
            result["verdict"] = "stop: fewer than 40 clusters or spread does not exceed seed variance"
            return result
        result["curation_requests_if_full"] = (len(edits) + args.curation_batch_size - 1) // args.curation_batch_size
        if args.gate_only:
            result["verdict"] = "gate passed: rerun without --gate-only to evaluate the arms"
            return result

        scores, promoted = select(model, evolver, groups, edits, train, args.validation_blocks, args.top_k, pool,
                                  args.curation_batch_size)
        truth = matrix.mean(axis=1)
        rank_draws = {arm: [rho(score[idx], truth[idx]) for idx in draws] for arm, score in scores.items()}
        chosen = {}
        task_draws = rng.integers(len(test), size=(args.bootstrap, len(test)))
        for arm, indices in promoted.items():
            treatment = tuple(edits[i] for i in indices)
            gain = (accuracy(model, treatment, cases, pool) - baseline).reshape(len(SEEDS), -1)
            boot = [gain[:, idx].mean() for idx in task_draws]
            chosen[arm] = dict(scores=scores[arm].tolist(), rho=rho(scores[arm], truth),
                               rho_ci=ci(rank_draws[arm]), promoted=indices, top_k_gain=float(gain.mean()),
                               top_k_ci=ci(boot))
            if arm != "breadth":
                a, b = chosen["breadth"]["rho"], chosen[arm]["rho"]
                chosen[arm]["breadth_minus_rho"] = a - b if a is not None and b is not None else None
                chosen[arm]["breadth_minus_rho_ci"] = ci([
                    a - b for a, b in zip(rank_draws["breadth"], rank_draws[arm]) if a is not None and b is not None
                ])
        result["arms"] = chosen
        margins = {arm: entry["breadth_minus_rho"] for arm, entry in chosen.items() if arm != "breadth"}
        keep = all(gap is not None and gap > (0.1 if arm == "lofo" else 0) for arm, gap in margins.items())
        result["verdict"] = "keep" if keep else "kill"
    return result


def main():
    parser = argparse.ArgumentParser(description="HW1 convergent-edit promotion pilot")
    parser.add_argument("--backend", choices=("stub", "local", "api"), required=True)
    parser.add_argument("--tasks", type=int, default=30)
    parser.add_argument("--held-out-tasks", type=int, default=30)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--validation-blocks", type=int, default=3)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--proposal-batch-size", type=int, default=1)
    parser.add_argument("--curation-batch-size", type=int, default=1)
    parser.add_argument("--gate-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache", type=Path, help="HTTP response cache (default: OUTPUT.cache.sqlite3)")
    args = parser.parse_args()
    if min(args.tasks, args.held_out_tasks, args.workers, args.validation_blocks, args.top_k,
           args.bootstrap, args.proposal_batch_size, args.curation_batch_size) < 1:
        parser.error("numeric settings must be positive")
    cache_path = args.cache or args.output.with_suffix(args.output.suffix + ".cache.sqlite3")
    if args.backend != "stub" and cache_path.resolve() == args.output.resolve():
        parser.error("cache and output must be different files")
    with (nullcontext() if args.backend == "stub" else ResponseCache(cache_path)) as cache:
        result = run(args, cache)
        if cache is not None:
            evolver, _, _, _ = backends(args.backend, cache)
            result["evolver_http_attempts_in_cache"] = cache.attempts(evolver.chat.scope)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(result["verdict"])


if __name__ == "__main__":
    main()
