import argparse
import json
from pathlib import Path

import numpy as np

from pilots.n1_layer_local_kv.pilot import FLOOR


BOOTSTRAPS = 10_000


def estimate(point, replicates):
    return {"mean": np.asarray(point).tolist(),
            "ci95": np.moveaxis(np.percentile(replicates, [2.5, 97.5], axis=0), 0, -1).tolist()}


def ratio(a, b):
    return np.divide(a, b, out=np.full_like(np.asarray(a), np.nan), where=np.asarray(b) > 1e-8)


def ranks(values):
    _, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    return (np.cumsum(counts) - (counts + 1) / 2)[inverse]


def spearman(a, b):
    return float(np.corrcoef(ranks(a), ranks(b))[0, 1])


def summarize(raw):
    arms = raw["arms"]
    full, mask, bias = (arms.index(name) for name in ("full", "mask", "global_bias"))
    temp = arms.index("temperature")
    read = lambda key: np.asarray([[lesson[key] for lesson in seed["lessons"]] for seed in raw["seeds"]])
    gain, harm = read("gain"), read("harm")
    seeds, lessons, _ = gain.shape
    rng = np.random.default_rng(4401)
    ids = (rng.integers(seeds, size=(BOOTSTRAPS, seeds, 1)),
           rng.integers(lessons, size=(BOOTSTRAPS, seeds, lessons)))
    boot_gain, boot_harm = (matrix[ids].mean(axis=(1, 2)) for matrix in (gain, harm))
    avg_gain, avg_harm = (matrix.mean(axis=(0, 1)) for matrix in (gain, harm))
    retention = float(ratio(avg_gain[mask], avg_gain[full]))
    reduction = float(ratio(avg_harm[bias] - avg_harm[mask], avg_harm[bias]))
    train_help, test_help = read("train_layer_help"), read("heldout_layer_help")
    return {
        "verdict": ("KEEP" if retention >= FLOOR and reduction >= 0.30
                    and avg_gain[mask] > avg_gain[temp] else "KILL"),
        "bootstrap_replicates": BOOTSTRAPS,
        "heldout_gain": estimate(avg_gain, boot_gain),
        "heldout_harm": estimate(avg_harm, boot_harm),
        "mask_minus_each_gain": estimate(avg_gain[mask] - avg_gain,
                                        boot_gain[:, [mask]] - boot_gain),
        "mask_minus_each_harm": estimate(avg_harm[mask] - avg_harm,
                                        boot_harm[:, [mask]] - boot_harm),
        "gain_minus_temperature": estimate(avg_gain - avg_gain[temp], boot_gain - boot_gain[:, [temp]]),
        "harm_minus_temperature": estimate(avg_harm - avg_harm[temp], boot_harm - boot_harm[:, [temp]]),
        "mask_gain_retained": estimate(retention, ratio(boot_gain[:, mask], boot_gain[:, full])),
        "mask_relative_harm_reduction_vs_bias": estimate(
            reduction, ratio(boot_harm[:, bias] - boot_harm[:, mask], boot_harm[:, bias])),
        "gain_by_seed": gain.mean(axis=1).tolist(),
        "harm_by_seed": harm.mean(axis=1).tolist(),
        "mean_train_gain_mask_and_bias": read("train_gain").mean(axis=(0, 1)).tolist(),
        "mean_train_abs_gain_mismatch": float(np.abs(np.diff(read("train_gain"), axis=-1)).mean()),
        "retrieval_on_target_recall": float(read("recall").mean()),
        "lessons_with_a_block_removed": int((~read("mask")).any(axis=-1).sum()),
        "mean_per_lesson_layer_help_spearman": float(np.mean([
            spearman(a, b) for seed_a, seed_b in zip(train_help, test_help)
            for a, b in zip(seed_a, seed_b)
        ])),
    }


def cell(data, i=None):
    mean, ci = data["mean"], data["ci95"]
    if i is not None:
        mean, ci = mean[i], ci[i]
    return f"{mean:.4f} [{ci[0]:.4f}, {ci[1]:.4f}]"


def table(raw):
    data = raw["summary"]
    lines = [
        "| Arm | On-target gain | Off-target harm | Mask − arm gain | Mask − arm harm |",
        "|---|---:|---:|---:|---:|",
    ]
    for i, arm in enumerate(raw["arms"]):
        lines.append(f"| {arm} | {cell(data['heldout_gain'], i)} | {cell(data['heldout_harm'], i)} | "
                     f"{cell(data['mask_minus_each_gain'], i)} | {cell(data['mask_minus_each_harm'], i)} |")
    lines.extend(["", "| Arm | Gain − temperature | Harm − temperature |", "|---|---:|---:|"])
    lines.extend(f"| {arm} | {cell(data['gain_minus_temperature'], i)} | "
                 f"{cell(data['harm_minus_temperature'], i)} |"
                 for i, arm in enumerate(raw["arms"]) if arm != "temperature")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.raw.read_text())
    raw["wall_seconds"] = args.wall_seconds
    raw["summary"] = summarize(raw)
    args.output.write_text(json.dumps(raw, separators=(",", ":")) + "\n")
    print(table(raw))
    for key, value in raw["summary"].items():
        if key not in ("heldout_gain", "heldout_harm", "mask_minus_each_gain", "mask_minus_each_harm",
                       "gain_minus_temperature", "harm_minus_temperature"):
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
