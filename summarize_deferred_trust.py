"""Summarize deferred-trust JSONL with a stream-paired bootstrap."""

import argparse
from collections import Counter
import json

import numpy as np


def by_setting(rows):
    for setting in dict.fromkeys(row["setting"] for row in rows):
        group = sorted((row for row in rows if row["setting"] == setting), key=lambda r: r["seed"])
        if len(group) != len({r["seed"] for r in group}):
            raise ValueError(f"duplicate stream seeds for {setting}")
        yield setting, group


def summarize(group, radius):
    def extract(key, method):
        return np.array([
            next(r[key] for r in row["records"] if r["method"] == method and r["radius"] == radius)
            for row in group
        ])

    methods = [r["method"] for r in group[0]["records"] if r["radius"] == radius]
    rmse = {method: extract("rmse", method) for method in methods}
    oracle_loss = extract("clean_loss", "oracle")
    indices = np.random.default_rng(42).integers(len(group), size=(10_000, len(group)))

    def relative(candidate, control):
        a, b = rmse[candidate], rmse[control]
        boot = 100 * (1 - a[indices].mean(axis=1) / b[indices].mean(axis=1))
        return {"pct": float(100 * (1 - a.mean() / b.mean())),
                "ci95": np.quantile(boot, [0.025, 0.975]).tolist()}

    comparisons = [
        ("sketched", "affinity_jet"), ("sketched", "diagonal"),
        ("sketched", "dense_jet"), ("mixed_subspace", "axis_shadow"),
        ("mixed_subspace", "mixed_ridge"), ("mixed_subspace", "affinity_shadows"),
        ("mixed_subspace", "affinity_jet"), ("guarded", "diagonal"),
        ("guarded", "axis_shadow"), ("guarded", "affinity_jet"), ("guarded", "sketched"),
    ]
    return {
        "rmse": {name: float(data.mean()) for name, data in rmse.items()},
        "clean_excess_loss": {
            method: float((extract("clean_loss", method) - oracle_loss).mean()) for method in methods
        },
        "relative_improvement": {
            f"{a}/{b}": relative(a, b) for a, b in comparisons if a in methods and b in methods
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics", type=argparse.FileType())
    args = parser.parse_args()
    metadata, *rows = map(json.loads, args.metrics)
    summary = {"metadata": metadata, "settings": {}}
    for setting, group in by_setting(rows):
        modes = Counter(row["audit"]["decoder"] for row in group if row["audit"])
        summary["settings"][setting] = {
            "n_streams": len(group),
            "support_recall": {
                n: float(np.mean([row["support_recall"][n] for row in group]))
                for n in group[0]["support_recall"]
            },
            "cross_hessian_energy_in_pair_blocks": float(np.mean([
                row["cross_hessian_energy_in_pair_blocks"] for row in group
            ])),
            "median_runtime_ms": {
                key: float(1000 * np.median([row["times_s"][key] for row in group]))
                for key in group[0]["times_s"]
            },
            "audit_modes": modes,
            "radii": {str(r): summarize(group, r) for r in (0.5, 1.0)},
        }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
