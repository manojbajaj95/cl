"""Summarize complete paired M3 traces with seed-cluster bootstrap intervals."""

import argparse
import json
from pathlib import Path
from statistics import fmean

from metrics import absorption, contrasts, flip, match_absorption, oscillates, seed_interval


def interval(matrix, cross_lessons=False):
    point, low, high = seed_interval(matrix, cross_lessons=cross_lessons)
    return f"{point * 100:+.2f} [{low * 100:+.2f}, {high * 100:+.2f}]"


def matrix(values, seeds, lessons):
    return [[values[seed, lesson] for lesson in lessons] for seed in seeds]


def r1_summary(keyed, seeds, lessons, cycles, arms):
    by_arm = {}
    for arm in arms:
        traces = {
            (seed, cycle): {(lesson, p["score"]): p for lesson in lessons
                            for p in keyed[arm, cycle, seed, lesson]["r1"]}
            for seed in seeds for cycle in cycles
        }
        by_arm[arm] = traces
        for cycle in cycles:
            probes = [list(traces[seed, cycle].values()) for seed in seeds]
            eligible = [[p for p in row if p["weights_old"] >= 0.5] for row in probes]
            raw = [[fmean(map(flip, row))] for row in eligible if row]
            gains = [[fmean(map(absorption, row))] for row in probes]
            raw_ci = interval(raw) if raw else "not estimable"
            print(f"{arm} R1 cycle {cycle}: flip {raw_ci}, eligible {[len(r) for r in eligible]}, "
                  f"absorption {interval(gains)}")
            if cycle == 1:
                continue
            matches = [match_absorption(traces[s, 1], traces[s, cycle]) for s in seeds]
            present = [row for row in matches if row]
            print(f"{arm} R1 matched C{cycle}−C1: Ns {[len(r) for r in matches]}")
            if len(present) < 3:
                print("R1 matched CI not estimable with fewer than three seeds on common support")
                continue
            before = interval([[fmean(flip(a) for a, _ in row)] for row in present])
            after = interval([[fmean(flip(b) for _, b in row)] for row in present])
            change = interval([[fmean(flip(b) - flip(a) for a, b in row)] for row in present])
            gain = interval([[fmean(absorption(b) - absorption(a) for a, b in row)] for row in present])
            print(f"  flips C1 {before}, C{cycle} {after}, paired change {change}, absorption change {gain}")
    last = cycles[-1]
    for arm in arms[1:]:
        matched = [match_absorption(by_arm["keep"][s, last], by_arm[arm][s, last]) for s in seeds]
        present = [row for row in matched if row]
        print(f"R1 C{last} {arm}−keep matched Ns: {[len(row) for row in matched]}")
        if len(present) >= 3:
            effect = interval([[fmean(flip(b) - flip(a) for a, b in row)] for row in present])
            print(f"  flip difference {effect}")
        else:
            print("  matched CI not estimable with fewer than three seeds on common support")


def summarize(records):
    keyed = {(r["arm"], r["cycle"], r["seed"], r["lesson"]): r for r in records}
    seeds = sorted({r["seed"] for r in records})
    lessons = sorted({r["lesson"] for r in records})
    arms = ("keep", "nca", "low-lr") if any(row["arm"] == "low-lr" for row in records) else ("keep", "nca")
    cycles = (1, 2, 3)
    expected = {(arm, cycle, seed, lesson) for arm in arms for cycle in cycles
                for seed in seeds for lesson in lessons}
    if len(seeds) != 5 or len(lessons) != 10 or keyed.keys() != expected or len(records) != len(expected):
        raise ValueError("Expected complete paired traces: 5 seeds × 10 lessons × 3 cycles in each arm")
    metrics = {
        (a, c, s, l): contrasts({**row, "evict": keyed["keep", 1, s, l]["weights"]})
        for (a, c, s, l), row in keyed.items()
    }
    comparisons = ("base_mae", "context_mae", "context_gain", "evict_mae", "evict_gain", "evict_vs_context_mae")
    for metric in comparisons:
        values = {(s, l): metrics["keep", 1, s, l][metric] for s in seeds for l in lessons}
        print(f"{metric}: {interval(matrix(values, seeds, lessons))}")
    print()
    print("| Arm | Cycle | Both signed error | Both MAE | Weights MAE |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for arm in arms:
        for cycle in cycles:
            vals = []
            for metric in ("signed_both", "both_mae", "weights_mae"):
                values = {(s, l): metrics[arm, cycle, s, l][metric] for s in seeds for l in lessons}
                vals.append(interval(matrix(values, seeds, lessons)))
            print(f"| {arm} | {cycle} | {' | '.join(vals)} |")
    print()
    for arm in arms:
        changes = {
            (s, l): metrics[arm, cycles[-1], s, l]["both_mae"] - metrics[arm, 1, s, l]["both_mae"]
            for s in seeds for l in lessons
        }
        print(f"{arm} |error| change C{cycles[-1]}−C1: {interval(matrix(changes, seeds, lessons))}")
    oscillation = {}
    for arm in arms:
        oscillation[arm] = {}
        for seed in seeds:
            for lesson in lessons:
                trace = [metrics[arm, c, seed, lesson]["signed_both"] for c in cycles]
                oscillation[arm][seed, lesson] = oscillates(trace)
                if oscillation[arm][seed, lesson]:
                    print(f"{arm} oscillation: {seed}, {lesson}: {[round(e * 100, 2) for e in trace]}")
    difference = {k: oscillation["nca"][k] - v for k, v in oscillation["keep"].items()}
    for name, values in {**oscillation, "nca-minus-keep": difference}.items():
        paired = matrix(values, seeds, lessons)
        print(f"{name} oscillation per-seed counts: {[sum(row) for row in paired]}")
        print(f"{name} oscillation: {interval(paired)} seed; {interval(paired, True)} crossed")
    print()
    r1_summary(keyed, seeds, lessons, cycles, arms)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traces", type=Path, nargs="+")
    args = parser.parse_args()
    summarize([json.loads(line) for path in args.traces for line in path.read_text(encoding="utf-8").splitlines()])


if __name__ == "__main__":
    main()
