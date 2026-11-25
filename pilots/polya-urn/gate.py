"""Budget-matched comparator stop gate for P1; see PROTOCOL.md."""

import argparse
import csv
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import platform
import subprocess
from tempfile import TemporaryDirectory

import numpy as np
import scipy


UPSTREAM = "a6bbbf370483e9124f3bc7d3894cdbe3bae6b889"
SOURCE = "pilots/lyapunov/experiment.py"
HORIZONS = (20, 100, 200, 1000)
SEEDS = (101, 202, 303, *range(1000, 1045))
BOOTSTRAPS = 10_000
FIELDS = ("direct_20", "direct_100", "target_200", "target_1000",
          "pair_200", "pair_1000")


def load_simulator(path):
    spec = importlib.util.spec_from_file_location("lyapunov_upstream", path)
    simulator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simulator)
    return simulator


def checkpoints(sim, design, data, order):
    x, y, (probes, _), _, memory, draws, _ = data
    predictions = {}
    for step, episode in enumerate(sim.order_ids(order), start=1):
        memory, _ = sim.transition(design, memory, x[episode], y[episode], draws[episode])
        if step in HORIZONS:
            predictions[step] = sim.predict(memory, probes)[0]
    return predictions


def measure(sim, design, data):
    predictions = [checkpoints(sim, design, data, order) for order in sim.ORDERS]
    distances = {
        t: [sim.distance(a[t], b[t]) for a, b in combinations(predictions, 2)]
        for t in HORIZONS
    }
    return (
        distances[20][0], distances[100][0],
        np.mean(distances[200]), np.mean(distances[1000]),
        distances[200][0], distances[1000][0],
    )


def rank_stats(sim, means):
    stats = {}
    for index, short in enumerate((20, 100)):
        near = sim.correlation(means[..., index], means[..., 2])
        far = sim.correlation(means[..., index], means[..., 3])
        stats[f"rho_{short}_to_200"] = near
        stats[f"rho_{short}_to_1000"] = far
        stats[f"degradation_{short}"] = near - far
    return stats


def summarize(sim, values):
    rng = np.random.default_rng(281000)
    n_designs, n_seeds, _ = values.shape
    seed_indices = rng.integers(n_seeds, size=(BOOTSTRAPS, n_seeds))
    design_indices = rng.integers(n_designs, size=(BOOTSTRAPS, n_designs))
    means = values.mean(axis=1)
    seed_means = values[:, seed_indices, :].mean(axis=2).transpose(1, 0, 2)
    resampled_designs = seed_means[np.arange(BOOTSTRAPS)[:, None], design_indices, :]
    point = rank_stats(sim, means)
    ranks = {
        label: {name: sim.interval(point[name], draws)
                for name, draws in rank_stats(sim, sample).items()}
        for label, sample in (("fixed_designs", seed_means),
                              ("resampled_designs", resampled_designs))
    }
    paired = {
        "growth_20_to_200": (4, 0),
        "growth_200_to_1000": (5, 4),
    }
    designs = {}
    for i, name in enumerate(sim.DESIGNS):
        designs[name] = {
            **{field: sim.interval(means[i, j], seed_means[:, i, j])
               for j, field in enumerate(FIELDS)},
            **{label: sim.interval(means[i, a] - means[i, b],
                                   seed_means[:, i, a] - seed_means[:, i, b])
               for label, (a, b) in paired.items()},
        }
    primary = ranks["fixed_designs"]["degradation_100"]["ci95"]
    long_rho = ranks["fixed_designs"]["rho_100_to_1000"]["estimate"]
    return {
        "verdict": "PROCEED" if primary is not None and primary[0] > 0 else "KILL",
        "same_panel_max_rho_gain": None if long_rho is None else 1 - long_rho,
        "ranks": ranks,
        "designs": designs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    with TemporaryDirectory() as directory:
        upstream_path = Path(directory) / "experiment.py"
        try:
            source = subprocess.check_output(["git", "show", f"{UPSTREAM}:{SOURCE}"], cwd=repo)
        except subprocess.CalledProcessError:
            parser.error(f"missing simulator source; fetch PR #11 commit {UPSTREAM}")
        upstream_path.write_bytes(source)
        sim = load_simulator(upstream_path)

    sim.LONG = HORIZONS[-1]
    values = np.empty((len(sim.DESIGNS), len(SEEDS), len(FIELDS)))
    for j, seed in enumerate(SEEDS):
        data = sim.world(seed)
        for i, design in enumerate(sim.DESIGNS):
            values[i, j] = measure(sim, design, data)

    results = {
        "source_commit": UPSTREAM,
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__},
        "seeds": SEEDS, "orders": sim.ORDERS, "horizons": HORIZONS, "bootstraps": BOOTSTRAPS,
        **summarize(sim, values),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "runs.csv").open("w", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("design", "seed", *FIELDS))
        for i, design in enumerate(sim.DESIGNS):
            for j, seed in enumerate(SEEDS):
                writer.writerow((design, seed, *values[i, j]))
    (args.output_dir / "results.json").write_text(
        json.dumps(results, indent=2, allow_nan=False) + "\n"
    )
    print(json.dumps({key: results[key] for key in
                     ("verdict", "same_panel_max_rho_gain", "ranks")}, indent=2))


if __name__ == "__main__":
    main()
