import argparse
import json
from pathlib import Path

import numpy as np


def bootstrap(values, n_boot=10_000):
    _, n_seeds, n_tasks = values.shape
    rng = np.random.default_rng(5573)
    seeds = rng.integers(n_seeds, size=(n_boot, n_seeds, 1))
    tasks = rng.integers(n_tasks, size=(n_boot, 1, n_tasks))
    return values.mean(axis=(1, 2)), values[:, seeds, tasks].mean(axis=(2, 3))


def interval(obs, resamples):
    lo, hi = np.percentile(resamples, [2.5, 97.5])
    return [float(x * 100) for x in (obs, lo, hi)]


def report(gate, rows):
    by_seed = [[r for r in gate if r["seed"] == seed]
               for seed in sorted(set(r["seed"] for r in gate))]
    points, draws = bootstrap(np.array([
        [[np.mean(r[k]) for r in seed] for seed in by_seed]
        for k in ("seen_hits", "held_hits")]))
    summary = dict(original_seen=interval(points[0], draws[0]),
                   original_held=interval(points[1], draws[1]),
                   headroom=interval(1 - points[1], 1 - draws[1]))
    if not rows:
        return summary
    names = ["original", *rows[0]["arms"]]
    points, draws = bootstrap(np.array([
        [[np.mean(f) for f in (r["original"] if name == "original" else r["arms"][name]["held"])]
         for r in rows] for name in names]))
    p = dict(zip(names, points))
    d = dict(zip(names, draws))
    summary["held"] = {name: interval(p[name], d[name]) for name in names}
    summary["deltas"] = {name: interval(p["round_trip"] - p[name], d["round_trip"] - d[name])
                         for name in names if name != "round_trip"}
    max_rewrite = max(p["rewrite"], p["rewrite_refine"])
    draws_rewrite = np.maximum(d["rewrite"], d["rewrite_refine"])
    summary["best_rewrite_delta"] = interval(p["round_trip"] - max_rewrite,
                                              d["round_trip"] - draws_rewrite)
    summary["retention"] = {}
    for task in ("seen", "mbpp"):
        acc = np.array([[r["retention"][arm][task] for r in rows]
                        for arm in ("base", "round_trip")])
        if task == "seen":
            acc = acc.mean(axis=-1)
        points, draws = bootstrap(acc)
        summary["retention"][task] = dict(
            base=interval(points[0], draws[0]),
            round_trip=interval(points[1], draws[1]),
            delta=interval(points[1] - points[0], draws[1] - draws[0]))
    if len(rows) == 3:
        delta = summary["deltas"]["shuffled"]
        reasons = []
        if summary["best_rewrite_delta"][0] <= 3 + 1e-10:
            reasons.append("round trip is at or below best rewrite + 3 pp")
        if delta[1] <= 0:
            reasons.append("shuffled labels tie or outperform the round trip by paired CI")
        if any(x["delta"][0] < -1 - 1e-10 for x in summary["retention"].values()):
            reasons.append("retention fell more than 1 pp")
        summary["decision"] = {"verdict": "KILL" if reasons else "KEEP", "reasons": reasons}
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    gate = json.loads((args.directory / "gate.json").read_text())
    rows = [json.loads(f.read_text()) for f in sorted(args.directory.glob("seed-*.json"))]
    print(json.dumps(report(gate, rows), indent=2))


if __name__ == "__main__":
    main()
