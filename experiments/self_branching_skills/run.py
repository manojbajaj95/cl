"""Prequential test of self-written steering on synthetic preference streams."""

import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
import platform
from time import perf_counter

import numpy as np
from scipy.stats import norm, t as student_t


PHASES = (("start", 0, 600), ("conflict", 600, 2200),
          ("rejoin", 2200, 3400), ("reversal", 3400, 5000))
CONDITIONS = {"routable": 0.90, "weak_cue": 0.65, "hidden": 0.50, "single_hill": 0.90}
METHODS = ("average", "maxmin", "fixed_two", "adaptive", "oracle")
WINDOW = 512
CHECK_EVERY = 32
MIN_COUNT = 48
HALF_WIDTH = 0.32
RADIUS_MULTIPLIER = 3.0
ALPHA = 0.035
SIGMA = 0.55
TARGET = 0.9
PROBE_HALF_STEP = 0.5
BIN = 100
SEEDS = tuple(range(1000, 1064))
HERE = Path(__file__).resolve().parent


def make_stream(seed, condition):
    """A cue may predict a cohort, but cohort IDs never reach non-oracles."""
    rng = np.random.default_rng(seed)
    n = PHASES[-1][2]
    probability_b = np.full(n, 0.30)
    probability_b[:600] = 0.02
    probability_b[2200:3400] = 0.55
    cohort = (rng.random(n) < probability_b).astype(np.int8)
    cue = np.where(rng.random(n) < CONDITIONS[condition], cohort, 1 - cohort)
    # An observable task offset is handled by the frozen executor, not the skill.
    item = rng.choice([-0.4, 0.0, 0.4], n)
    theta = np.zeros(n)
    sign = 1.0 if condition == "single_hill" else 1 - 2 * cohort
    first = np.s_[600:2200]
    last = np.s_[3400:5000]
    theta[first] = TARGET * np.broadcast_to(sign, theta.shape)[first]
    theta[2200:3400] = 0.30
    theta[last] = -TARGET * np.broadcast_to(sign, theta.shape)[last]
    probe_plus = utility(item + PROBE_HALF_STEP, item + theta)
    probe_minus = utility(item - PROBE_HALF_STEP, item + theta)
    margin = probe_plus - probe_minus + rng.normal(0.0, 4 * PROBE_HALF_STEP * SIGMA, n)
    return cohort, cue, item, theta, margin / (4 * PROBE_HALF_STEP)


def utility(action, target):
    return 1 - (action - target) ** 2


def ascent(value, signal):
    return max(-1.0, min(1.0, value + ALPHA * (signal - value)))


def maxmin_action(means, second_moments):
    """Minimize the larger of two estimated quadratic losses."""
    a, b = means
    if a == b:
        return a
    cross = (second_moments[0] - second_moments[1]) / (2 * (a - b))
    return max(min(a, b), min(max(a, b), cross))


def decide(sums, counts, split):
    """Test overlap of feasible scalar writes under uncertain cue means."""
    if min(counts) < MIN_COUNT:
        return split
    means = [total / count for total, count in zip(sums, counts)]
    radii = [RADIUS_MULTIPLIER * (SIGMA**2 + TARGET**2)**0.5 / count**0.5
             for count in counts]
    radius = sum(radii)
    gap = abs(means[0] - means[1])
    if gap - radius > 2 * HALF_WIDTH and max(radii) <= HALF_WIDTH:
        return True
    if gap + radius <= 2 * HALF_WIDTH:
        return False
    return split


class Writer:
    def __init__(self, method):
        self.method = method
        self.skill = [0.0, 0.0] if method in {"fixed_two", "oracle"} else [0.0]
        if method == "maxmin":
            self.estimates = [0.0, 0.0]
            self.second_moments = [0.0, 0.0]
        if method == "adaptive":
            self.values = np.zeros(WINDOW)
            self.cues = np.zeros(WINDOW, dtype=np.int8)
            self.sums = [0.0, 0.0]
            self.counts = [0, 0]
            self.seen = 0

    def predict(self, key):
        return self.skill[key] if len(self.skill) == 2 else self.skill[0]

    def observe(self, key, signal):
        if self.method == "maxmin":
            self.estimates[key] = ascent(self.estimates[key], signal)
            moment = self.second_moments[key]
            self.second_moments[key] += ALPHA * (signal**2 - SIGMA**2 - moment)
            self.skill[0] = maxmin_action(self.estimates, self.second_moments)
            return
        k = key if len(self.skill) == 2 else 0
        self.skill[k] = ascent(self.skill[k], signal)
        if self.method != "adaptive":
            return
        pos = self.seen % WINDOW
        if self.seen >= WINDOW:
            old = self.cues[pos]
            self.sums[old] -= self.values[pos]
            self.counts[old] -= 1
        self.cues[pos] = key
        self.values[pos] = signal
        self.sums[key] += signal
        self.counts[key] += 1
        self.seen += 1
        if self.seen % CHECK_EVERY:
            return
        split = len(self.skill) == 2
        if decide(self.sums, self.counts, split) != split:
            self.skill = [sum(self.skill) / 2] if split else self.skill * 2


def simulate(stream, method):
    cohort, cue, item, theta, signal = stream
    key = cohort if method == "oracle" else cue
    writer = Writer(method)
    scores = np.empty(len(key))
    slots = np.empty(len(key), dtype=np.int8)
    for i, (k, b, target, feedback) in enumerate(zip(key, item, theta, signal)):
        scores[i] = utility(b + writer.predict(k), b + target)
        slots[i] = len(writer.skill)
        writer.observe(k, feedback)
    return scores, slots


def run_seed(seed, condition):
    stream = make_stream(seed, condition)
    cohort = stream[0]
    for method in METHODS:
        scores, slots = simulate(stream, method)
        births = set(np.flatnonzero((slots[1:] - slots[:-1]) == 1) + 1)
        merges = set(np.flatnonzero((slots[1:] - slots[:-1]) == -1) + 1)
        for phase, a, b in (*PHASES, ("all", 0, len(cohort))):
            subset = slice(a, b)
            phase_scores = scores[subset]
            groups = [float(np.mean(phase_scores[cohort[subset] == j]))
                      if np.any(cohort[subset] == j) else None for j in (0, 1)]
            yield dict(seed=seed, condition=condition, method=method, phase=phase,
                       a=groups[0], b=groups[1],
                       worst=min(g for g in groups if g is not None),
                       slots=float(np.mean(slots[subset])),
                       split_delay=min((i - a for i in births if a <= i < b), default=None),
                       merge_delay=min((i - a for i in merges if a <= i < b), default=None))
        if condition == "routable":
            for start in range(0, len(cohort), BIN):
                subset = slice(start, start + BIN)
                yield (method, start, float(np.mean(scores[subset])), float(np.mean(slots[subset])))


def ci(values):
    x = np.asarray(values, dtype=float)
    mean = float(x.mean())
    if len(x) == 1:
        return [mean, mean, mean]
    error = float(student_t.ppf(.975, len(x) - 1) * x.std(ddof=1) / len(x)**0.5)
    return [mean, mean - error, mean + error]


def rate_ci(k, n):
    p = k / n
    z = norm.ppf(.975)
    center = (p + z**2 / (2*n)) / (1 + z**2 / n)
    width = z * (p * (1 - p) / n + z**2 / (4*n**2))**0.5 / (1 + z**2 / n)
    return [p, max(0.0, center - width), min(1.0, center + width)]


def summarize(rows, bins):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["condition"], row["method"], row["phase"]].append(row)
    tables = defaultdict(lambda: defaultdict(dict))
    for (condition, method, phase), subset in grouped.items():
        stats = {}
        for metric in ("a", "b", "worst", "slots", "split_delay", "merge_delay"):
            values = [r[metric] for r in subset if r[metric] is not None]
            stats[metric] = ci(values) if values else None
            if metric.endswith("delay"):
                stats[metric.replace("delay", "rate")] = rate_ci(len(values), len(subset))
        tables[condition][method][phase] = stats
    paired = defaultdict(dict)
    for (condition, method, phase), subset in grouped.items():
        if method != "adaptive":
            continue
        for baseline in ("average", "maxmin", "fixed_two"):
            comparator = {r["seed"]: r for r in grouped[condition, baseline, phase]}
            paired[condition][f"{phase}_vs_{baseline}"] = ci(
                [r["worst"] - comparator[r["seed"]]["worst"] for r in subset])
    curves = defaultdict(dict)
    for (method, start), values in bins.items():
        curves[method][start] = dict(utility=ci([v[0] for v in values]),
                                     slots=ci([v[1] for v in values]))
    return dict(tables=tables, paired_worst=paired, curves=curves)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    if len(set(args.seeds)) != len(args.seeds):
        parser.error("seeds must be distinct")
    start = perf_counter()
    rows = []
    bins = defaultdict(list)
    for condition in CONDITIONS:
        for seed in args.seeds:
            for result in run_seed(seed, condition):
                if isinstance(result, dict):
                    rows.append(result)
                else:
                    method, step, score, slots = result
                    bins[method, step].append((score, slots))
    report = summarize(rows, bins)
    report.update(
        design=dict(phases=PHASES, cue_accuracy=CONDITIONS, window=WINDOW, check_every=CHECK_EVERY,
                    minimum_per_cue=MIN_COUNT, radius_multiplier=RADIUS_MULTIPLIER,
                    half_width=HALF_WIDTH, step_size=ALPHA, noise_sigma=SIGMA,
                    target=TARGET, probe_half_step=PROBE_HALF_STEP, bin_width=BIN),
        environment=dict(python=platform.python_version(), numpy=np.__version__,
                         machine=platform.machine(), elapsed_seconds=perf_counter() - start),
        seeds=args.seeds,
    )
    with (args.out / "seed_metrics.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(args.seeds)} paired seeds × {len(CONDITIONS)} conditions × {len(METHODS)} methods")
    for condition in CONDITIONS:
        s = report["tables"][condition]["adaptive"]
        delta = report["paired_worst"][condition]["conflict_vs_maxmin"]
        print(f"{condition}: worst-cohort Δ vs MaxMin {delta[0]:+.3f} [{delta[1]:+.3f}, {delta[2]:+.3f}]; "
              f"first-conflict split {s['conflict']['split_rate'][0]:.1%}")
    print(f"Saved seed_metrics.csv and results.json in {report['environment']['elapsed_seconds']:.1f} s")


if __name__ == "__main__":
    main()
