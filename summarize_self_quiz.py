"""Summarize the three paired held-out runs from the self-quiz pilot."""

from collections import defaultdict
import json
from statistics import mean, stdev
import sys


SEEDS = (501, 502, 503)
COMPARATORS = ("teacher_qa", "diverse_teacher_qa", "verified_prose", "unfiltered_prose")
T_CRITICAL_DF2 = 4.302652729749462


def paired_interval(diffs):
    avg = mean(diffs)
    err = T_CRITICAL_DF2 * stdev(diffs) / len(diffs)**0.5
    return {"mean": avg, "95%_ci": [avg - err, avg + err], "by_seed": diffs}


def summarize(rows):
    if tuple(row["seed"] for row in rows) != SEEDS:
        raise ValueError(f"expected one run per held-out seed {SEEDS}")
    pre = [row["pre_stream"]["accuracy"] * 100 for row in rows]
    per_method = defaultdict(list)
    for row in rows:
        for name, stages in row["stages"].items():
            per_method[name].append(stages)
    methods = {}
    for name, runs in per_method.items():
        methods[name] = {
            "old_accuracy_pp": [run[-1]["old"]["accuracy"] * 100 for run in runs],
            "latest_accuracy_pp": [run[-1]["new"]["accuracy"] * 100 for run in runs],
            "old_accuracy_over_time_pp": [mean(v["old"]["accuracy"] for v in stage) * 100
                                           for stage in zip(*runs)],
            "mean_old_nll": mean(run[-1]["old"]["nll"] for run in runs),
        }
    comparisons = {}
    for control in COMPARATORS:
        ours, theirs = methods["self_qa"], methods[control]
        comparisons[control] = {
            key: paired_interval([a - b for a, b in zip(ours[key], theirs[key])])
            for key in ("old_accuracy_pp", "latest_accuracy_pp")
        }
    actual_forgetting = all(a - b >= 10 for a, b in zip(pre, methods["no_replay"]["old_accuracy_pp"]))
    covered = [row["generation"]["matched_coverage"] for row in rows]
    valid = min(pre) > 60 and actual_forgetting and min(covered) >= 0.5
    passed = all(v["old_accuracy_pp"]["mean"] >= 3
                 and v["old_accuracy_pp"]["95%_ci"][0] > 0
                 and v["latest_accuracy_pp"]["mean"] >= -3
                 for method, v in comparisons.items() if method != "unfiltered_prose")
    return {"verdict": ("keep" if passed else "kill escalation") if valid else "inconclusive",
            "pre_stream_pp": pre, "coverage": covered, "methods": methods, "comparisons": comparisons}


def main():
    rows = sorted(map(json.loads, sys.stdin), key=lambda row: row["seed"])
    print(json.dumps(summarize(rows), indent=2))


if __name__ == "__main__":
    main()
