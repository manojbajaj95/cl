import argparse
import json
from pathlib import Path

import numpy as np


PHASES = {"returning": (2, 4), "first": (0, 1, 3)}
BLOCK = 20
BOOTSTRAPS = 10_000


def interval(samples):
    return np.percentile(samples, [2.5, 97.5], axis=0)


def estimate(means, replicates):
    lo, hi = interval(replicates)
    return {"mean": means.tolist(), "ci95": np.stack([lo, hi], axis=-1).tolist()}


def boot_means(hits, rng):
    seeds, visits, length, arms = hits.shape
    if length % BLOCK:
        raise ValueError(f"visit length must be divisible by bootstrap block size {BLOCK}")
    blocks = length // BLOCK
    blocks_of_hits = hits.reshape(seeds, visits, blocks, BLOCK, arms).mean(axis=3)
    seed_ids = rng.integers(seeds, size=(BOOTSTRAPS, seeds, 1, 1))
    visit_ids = np.arange(visits)[None, None, :, None]
    block_ids = rng.integers(blocks, size=(BOOTSTRAPS, seeds, visits, blocks))
    return blocks_of_hits[seed_ids, visit_ids, block_ids].mean(axis=(1, 3))


def summarize(raw):
    arms = raw["arms"]
    m2 = arms.index("m2")
    controls = [i for i in range(len(arms)) if i != m2]
    temp = arms.index("temperature") if "temperature" in arms else None
    seeds = raw["seeds"]
    length = raw["visit_length"]
    rows = [r for seed in seeds for r in seed["episodes"]]
    hits = 100 * np.asarray([r["hit"] for r in rows]).reshape(len(seeds), 5, length, len(arms))
    bootstrap = boot_means(hits, np.random.default_rng(7244))
    summary = {"block_length": BLOCK, "bootstrap_replicates": BOOTSTRAPS, "phases": {}}
    for phase, visits in PHASES.items():
        estimates = hits[:, visits].mean(axis=(1, 2))
        means = estimates.mean(axis=0)
        replicates = bootstrap[:, visits, :].mean(axis=1)
        strongest = controls[np.argmax(means[controls])]
        diff = means[m2] - means
        paired = replicates[:, m2, None] - replicates
        summary["phases"][phase] = {
            "absolute": estimate(means, replicates),
            "per_seed_means": estimates.tolist(),
            "m2_minus_each": estimate(diff, paired),
            "best_control": arms[strongest],
            "m2_minus_best": estimate(diff[strongest],
                                      replicates[:, m2] - replicates[:, controls].max(axis=1)),
        }
        if temp is not None:
            summary["phases"][phase]["minus_temperature"] = estimate(
                means - means[temp], replicates - replicates[:, [temp]])
    contrasts = [r["contrast"] for r in rows if "contrast" in r]
    summary["signal"] = {"grad_nonzero": sum(r["grad_nonzero"] for r in rows),
                         "episodes": len(rows), "query_groups": len(contrasts),
                         "dense_groups": sum(c[0] for c in contrasts),
                         "binary_groups": sum(c[1] for c in contrasts)}
    summary["per_visit_means"] = hits.mean(axis=(0, 2)).tolist()
    returning = summary["phases"]["returning"]["m2_minus_best"]
    first = summary["phases"]["first"]["m2_minus_best"]
    summary["verdict"] = ("KEEP" if returning["mean"] >= 5 and returning["ci95"][0] >= 5
                          and first["mean"] >= -2 else "KILL")
    return summary


def cell(estimates, idx=None):
    mean, ci = estimates["mean"], estimates["ci95"]
    if idx is not None:
        mean, ci = mean[idx], ci[idx]
    return f"{mean:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]"


def table(raw):
    summary = raw["summary"]
    first, ret = (summary["phases"][key] for key in ("first", "returning"))
    lines = [
        "| Arm | First visits | Returning visits | M2 − arm, first | M2 − arm, returning |",
        "|---|---:|---:|---:|---:|",
    ]
    for i, name in enumerate(raw["arms"]):
        first_diff = "—" if name == "m2" else cell(first["m2_minus_each"], i)
        ret_diff = "—" if name == "m2" else cell(ret["m2_minus_each"], i)
        lines.append(f"| {name} | {cell(first['absolute'], i)} | {cell(ret['absolute'], i)} | "
                     f"{first_diff} | {ret_diff} |")
    lines.extend(f"- M2 − best {phase} control ({data['best_control']}): "
                 + cell(data["m2_minus_best"]) + " pp."
                 for phase, data in summary["phases"].items())
    if "minus_temperature" in first:
        lines.extend(["", "| Arm | First minus temperature | Returning minus temperature |",
                      "|---|---:|---:|"])
        lines.extend(f"| {arm} | {cell(first['minus_temperature'], i)} | "
                     f"{cell(ret['minus_temperature'], i)} |"
                     for i, arm in enumerate(raw["arms"]) if arm != "temperature")
    for phase, data in summary["phases"].items():
        lines.extend(["", f"Per-seed {phase} accuracy (%):", "",
                      "| Seed | " + " | ".join(raw["arms"]) + " |",
                      "|---|" + "---:|" * len(raw["arms"])])
        for seed, values in zip(raw["seeds"], data["per_seed_means"]):
            lines.append(f"| {seed['seed']} | " + " | ".join(f"{v:.2f}" for v in values) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.raw.read_text())
    raw["calibration"] = {"seed": 999, **json.loads(args.calibration.read_text())}
    raw["wall_seconds"] = args.wall_seconds
    raw["summary"] = summarize(raw)
    args.output.write_text(json.dumps(raw, separators=(",", ":")) + "\n")
    print(raw["summary"]["verdict"])
    print(table(raw))
    print(raw["summary"]["signal"])


if __name__ == "__main__":
    main()
