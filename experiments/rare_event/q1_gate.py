"""Noise gate for Q1, with paired seed uncertainty."""

import argparse
import json
from pathlib import Path

import numpy as np

from pilot import MODES, SEEDS


def variance_components(recovery):
    within = recovery.var(axis=-2, ddof=1).mean(axis=-1)
    across = recovery.mean(axis=-2).var(axis=-1, ddof=1)
    return np.stack((within, across, within - across, within / across), axis=-1)


def gate(recovery, bootstrap_indices):
    point = variance_components(recovery)
    bootstrap = variance_components(recovery[bootstrap_indices])
    low, high = np.quantile(bootstrap, [0.025, 0.975], axis=0)
    return dict(
        proceed=bool(point[0] < point[1]),
        **{
            name: dict(estimate=float(value), low=float(lo), high=float(hi))
            for name, value, lo, hi in zip(
                ("within", "across", "within_minus_across", "within_over_across"),
                point, low, high,
            )
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    results = json.loads(args.results.read_text())
    runs = results["runs"]
    seeds = [run["seed"] for run in runs]
    if seeds != list(range(SEEDS[0], SEEDS[0] + 10)):
        parser.error("expected the ten prespecified Q1 seeds in order")
    modes = ("none", *MODES)
    recovery = 100 * np.array([[run[mode]["old_rare"] for mode in modes] for run in runs])
    bootstrap = np.random.default_rng(1201).integers(len(runs), size=(20_000, len(runs)))
    print(json.dumps({
        "units": "squared percentage points, except the ratio",
        "all_arms": gate(recovery, bootstrap),
        "replay_only_sensitivity": gate(recovery[:, 1:], bootstrap),
        "seeds": seeds,
        "arm_mean_old_recovery_pp": dict(zip(modes, recovery.mean(axis=0).tolist())),
        "arm_seed_variance_pp_squared": dict(zip(modes, recovery.var(axis=0, ddof=1).tolist())),
    }, indent=2))


if __name__ == "__main__":
    main()
