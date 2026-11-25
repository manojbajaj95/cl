import json
import math
from pathlib import Path
from random import Random
import sys


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    center = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    denom = 1 + z * z / n
    return [max(0, (center - half) / denom), min(1, (center + half) / denom)]


def paired(groups):
    rng = Random(3407)
    n = sum(map(len, groups))
    boot = sorted(
        sum(sum(rng.choices(g, k=len(g))) for g in groups) / n
        for _ in range(10000)
    )
    return {"delta": sum(map(sum, groups)) / n, "ci95": [boot[250], boot[9749]]}


def summarize(run):
    seeds = run["seeds"]
    if set(seeds) != set(map(str, run["config"]["seeds"])):
        raise ValueError("The requested run is incomplete")
    depths = sorted(run["ppl"]["loop_only"], key=int)
    result = {"config": run["config"], "elapsed_seconds": run["elapsed_seconds"],
              "gate": run["gate"], "ppl": run["ppl"],
              "ppl_on": {s: record["ppl_on"] for s, record in seeds.items()},
              "accuracy": {}, "paired": {}}
    if "controls_seconds" in run:
        result["controls_seconds"] = run["controls_seconds"]
    for d in depths:
        rows = {s: record["held"][d] for s, record in seeds.items()}
        n = sum(map(len, rows.values()))
        arms = next(iter(rows.values()))[0]["correct"]
        result["accuracy"][d] = {}
        result["paired"][d] = {}
        for arm in arms:
            hits = {s: sum(x["correct"][arm] for x in group) for s, group in rows.items()}
            k = sum(hits.values())
            result["accuracy"][d][arm] = {
                "correct": k, "n": n, "accuracy": k / n, "ci95": wilson(k, n), "by_seed": hits,
            }
            if arm != "loop_program":
                result["paired"][d][arm] = paired([
                    [int(x["correct"]["loop_program"]) - int(x["correct"][arm]) for x in group]
                    for group in rows.values()
                ])
    return result


if __name__ == "__main__":
    run_path = Path(sys.argv[1])
    summary = summarize(json.loads(run_path.read_text()))
    summary_path = run_path.with_name("summary.json")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(summary_path)
