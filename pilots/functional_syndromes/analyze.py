"""Score the sparsity gate and fixed-byte recovery from saved pilot artifacts."""

import argparse
import json
from pathlib import Path

import numpy as np


def top_indices(scores, count):
    return np.argsort(-scores, kind="stable")[:count]


def concentration(energy):
    count = max(1, len(energy) // 10)
    return float(energy[top_indices(energy, count)].sum() / energy.sum()) if energy.sum() else None


def bootstrap(values, statistic, rng, draws=2000):
    point = statistic(values)
    if point is None:
        return None
    samples = [
        statistic(values[rng.integers(len(values), size=len(values))])
        for _ in range(draws)
    ]
    lo, hi = np.quantile([sample for sample in samples if sample is not None], [0.025, 0.975])
    return {"estimate": float(point), "ci95": [float(lo), float(hi)]}


def pearson(pairs):
    x, y = pairs.T
    if not x.std() or not y.std():
        return None
    return np.corrcoef(x, y)[0, 1]


def read_checks(c, keys, dw):
    return np.concatenate([(c @ k) @ w for k, w in zip(keys, dw)], axis=1)


def somp(c, observed, count):
    """Simultaneous OMP with normalized columns and all layer/output channels."""
    # Replace the residual's thousands of channels with an equivalent Gram factor.
    observed = observed.astype(np.float64)
    eig, vec = np.linalg.eigh(observed @ observed.T)
    residual = vec * np.sqrt(np.maximum(eig, 0))
    c = c.astype(np.float64)
    c /= np.linalg.norm(c, axis=0)
    basis = np.empty((c.shape[0], count))
    selected = []
    correlations = c.T @ residual
    for j in range(count):
        scores = np.einsum("ij,ij->i", correlations, correlations)
        scores[selected] = -np.inf
        i = int(np.argmax(scores))
        col = c[:, i].copy()
        if j:
            active = basis[:, :j]
            col -= active @ (active.T @ col)
            col -= active @ (active.T @ col)
        norm = np.linalg.norm(col)
        if norm < 1e-10:
            break
        col /= norm
        basis[:, j] = col
        selected.append(i)
        step = col @ residual
        residual -= col[:, None] * step
        correlations -= (c.T @ col)[:, None] * step
    return np.asarray(selected, dtype=int)


def dense_ls(c, observed, count):
    c, observed = c.astype(np.float64), observed.astype(np.float64)
    coefficients = np.linalg.solve(c @ c.T, observed)
    # Compute row energies of C.T @ coefficients without materializing all outputs.
    scores = np.einsum("ij,ij->j", c, (coefficients @ coefficients.T) @ c)
    return top_indices(scores, count)


def compare(keys, delta, values, damage, count, draws, rng):
    n = len(damage)
    truth = top_indices(damage, count)
    truth_mask = np.zeros(n, dtype=bool)
    truth_mask[truth] = True
    scores = {"syndrome": [], "dense_ls": [], "replay": []}
    for _ in range(draws):
        c = rng.normal(0, 1 / np.sqrt(count), size=(count, n)).astype(np.float32)
        measured = read_checks(c, keys, delta)
        choices = {
            "syndrome": somp(c, measured, count),
            "dense_ls": dense_ls(c, measured, count),
            "replay": rng.choice(n, size=count, replace=False),
        }
        for name, picked in choices.items():
            tp = int(truth_mask[picked].sum())
            scores[name].append([tp / count, tp / len(picked), tp])
    samples = {name: np.asarray(vals) for name, vals in scores.items()}
    return {
        "m": count,
        "bytes_each": count * (keys[:, :1].nbytes + values[:, :1].nbytes),
        "draws": draws,
        "metrics": {
            name: {
                metric: bootstrap(vals[:, j], np.mean, rng)
                for j, metric in enumerate(("recall", "precision", "true_positives"))
            }
            for name, vals in samples.items()
        },
        "paired_recall_deltas": {
            name: bootstrap(samples["syndrome"][:, 0] - samples[name][:, 0], np.mean, rng)
            for name in ("dense_ls", "replay")
        },
    }


def summarize(artifact, draws, seed):
    rng = np.random.default_rng(seed)
    with np.load(artifact) as run:
        keys, delta, values = run["keys"], run["dw"], run["values"]
        effects_by_layer = np.array([k @ w for k, w in zip(keys, delta)])
        edit = run["edit_effects"]
        edit_energy = np.einsum("lnd,lnd->n", edit, edit)
        raw = np.einsum("lnd,lnd->n", effects_by_layer, effects_by_layer)
        product = np.einsum("lnd,lnd->n", effects_by_layer, edit)
        ratio = raw / np.maximum(edit_energy, 1e-12)
        projected = product**2 / np.maximum(edit_energy, 1e-12)
        antiparallel = np.minimum(product, 0)**2 / np.maximum(edit_energy, 1e-12)
        drop = run["edit_prob"] - run["post_prob"]
        did_edit = ~run["base_win"] & run["edit_win"]
        metrics = {
            "n": len(raw),
            "nll": {name: float(run[f"nll_{name}"]) for name in ("before", "after")},
            "mean_target_probability": {
                phase: bootstrap(run[f"{phase}_prob"], np.mean, rng)
                for phase in ("base", "edit", "post")
            },
            "rewrite_preference": {
                phase: bootstrap(run[f"{phase}_win"], np.mean, rng)
                for phase in ("base", "edit", "post")
            },
            "abs_preference_drop": bootstrap(
                run["edit_win"].astype(float) - run["post_win"], np.mean, rng,
            ),
            "mean_target_probability_drop": bootstrap(drop, np.mean, rng),
            "edit_induced_success_count": int(did_edit.sum()),
            "edit_induced_success_retained": bootstrap(run["post_win"][did_edit], np.mean, rng) if did_edit.any() else None,
            "raw_damage_top10_energy_share": bootstrap(raw, concentration, rng),
            "raw_share_edit_induced_success_only": bootstrap(raw[did_edit], concentration, rng) if did_edit.any() else None,
            "normalized_damage_top10_energy_share": bootstrap(ratio, concentration, rng),
            "projected_damage_top10_energy_share": bootstrap(projected, concentration, rng),
            "antiparallel_damage_top10_energy_share": bootstrap(antiparallel, concentration, rng),
            "functional_drop_top10_energy_share": bootstrap(np.maximum(drop, 0)**2, concentration, rng),
            "raw_vs_functional_damage_pearson": bootstrap(
                np.column_stack((np.sqrt(raw), drop)), pearson, rng,
            ),
            "layer_top10_energy_share": {
                int(layer): bootstrap(np.einsum("nd,nd->n", e, e), concentration, rng)
                for layer, e in zip(run["layers"], effects_by_layer)
            },
            "verdict_gate": "kill" if concentration(raw) is None or concentration(raw) < 0.8 else "advance",
        }
        if draws > 0:
            metrics["recovery_top_raw_damage"] = compare(
                keys, delta, values, raw, len(raw) // 10, draws, rng,
            )
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path, nargs="+")
    parser.add_argument("--draws", type=int, default=20)
    parser.add_argument("--seed", type=int, default=304)
    args = parser.parse_args()
    print(json.dumps({
        path.stem: summarize(path, args.draws, args.seed) for path in args.artifacts
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
