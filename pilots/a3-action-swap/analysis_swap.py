"""Compute A3 swap following and common-support margin comparisons."""

import argparse
import json
from pathlib import Path

import numpy as np

from design import MENU


# Zero has its own bin; every positive bin is 0.25 logit units wide.
UPPER = np.r_[np.arange(0.25, 4.01, 0.25), np.inf]
N_BINS = len(UPPER) + 1
METRICS = ("follow_pp", "named_vs_filler_pp", "named_vs_non_menu_pp", "named_flip_pp",
           "filler_flip_pp", "non_menu_flip_pp")


def directional_effects(tables, notes):
    base = tables["base"].reshape(-1, len(MENU))
    scores = {
        arm: tables[arm].reshape(len(notes), len(base), len(MENU)).argmax(-1)[..., None]
        for arm in ("rule", "swapped", "filler", "non_menu")
    }
    actions = np.array([[MENU.index(note[key]) for key in ("action", "swap_action")]
                        for note in notes])
    named = actions[:, None, :]
    own = np.concatenate([scores["rule"], scores["swapped"]], axis=-1)
    rival = own[..., ::-1]
    own_match = (own == named).astype(float)
    base_top = base.argmax(-1)
    nonmodal = named != base_top[None, :, None]
    margins = base.max(-1)[None, :, None] - base[np.arange(len(base))[None, :, None], named]
    bins = np.where(margins == 0, 0, np.searchsorted(UPPER, margins, side="right") + 1)
    effects = np.stack([
        own_match - (rival == named),
        own_match - (scores["filler"] == named),
        own_match - (scores["non_menu"] == named),
        np.where(nonmodal, own_match, np.nan),
        np.where(nonmodal, scores["filler"] == named, np.nan),
        np.where(nonmodal, scores["non_menu"] == named, np.nan),
    ], axis=-1) * 100
    return effects, bins, named, base_top


def means(values):
    n = np.isfinite(values).sum(axis=0)
    return np.divide(np.nansum(values, axis=0), n,
                     out=np.full(len(METRICS), np.nan), where=n > 0)


def bin_means(cells, bins, matching):
    return np.stack([means(cells[bins == b]) for b in matching])


def weighted(values, weights):
    return (values * weights[:, None]).sum(axis=0) / weights.sum()


def summarize(point, samples):
    samples = np.asarray(samples)
    finite = samples[np.isfinite(samples)]
    return {
        "estimate": float(point) if np.isfinite(point) else None,
        "ci95": np.percentile(finite, [2.5, 97.5]).tolist() if len(finite) else None,
        "bootstrap_draws_with_support": len(finite),
    }


def scalar_metrics(point, samples):
    return {metric: summarize(point[i], samples[:, i]) for i, metric in enumerate(METRICS)}


def interval_label(bin_id):
    if bin_id == 0:
        return "0"
    low = 0 if bin_id == 1 else UPPER[bin_id - 2]
    high = UPPER[bin_id - 1]
    return f"{'(' if low == 0 else '['}{low:g},{high:g})"


def bootstrap_indices(lessons, states, draws, seed):
    rng = np.random.default_rng(seed)
    for _ in range(draws):
        yield (rng.integers(lessons, size=lessons)[:, None],
               rng.integers(states, size=states)[None, :])


def analyze(old, new, notes, draws, seed):
    model = [directional_effects(tables, notes) for tables in (old, new)]
    counts = [np.bincount(bins.ravel(), minlength=N_BINS) for _, bins, _, _ in model]
    weights = np.minimum(*counts)
    matching = np.flatnonzero(weights)
    positive = matching > 0
    if not positive.any():
        raise ValueError("No positive-margin common support")
    w = weights[matching]
    all_cells = model[0][0].reshape(-1, len(METRICS))
    overall = means(all_cells)
    points = np.stack([bin_means(cells, bins, matching) for cells, bins, _, _ in model])
    raw_draws, bin_draws = [], []
    for idx in bootstrap_indices(*model[0][0].shape[:2], draws, seed):
        raw_draws.append(means(model[0][0][idx].reshape(-1, len(METRICS))))
        bin_draws.append(np.stack([
            bin_means(cells[idx], bins[idx], matching) for cells, bins, _, _ in model
        ]))
    bin_draws = np.array(bin_draws)
    raw = scalar_metrics(overall, np.array(raw_draws))

    def matched_summary(mask):
        out = {}
        for i, key in enumerate(("old", "new")):
            out[key] = scalar_metrics(
                weighted(points[i, mask], w[mask]),
                np.stack([weighted(values[mask], w[mask]) for values in bin_draws[:, i]]),
            )
        diff = points[1, mask] - points[0, mask]
        diff_draws = bin_draws[:, 1, mask] - bin_draws[:, 0, mask]
        out["new_minus_old_follow_pp"] = summarize(
            weighted(diff, w[mask])[0],
            [weighted(values, w[mask])[0] for values in diff_draws],
        )
        return out

    bins_report = {}
    for b in np.flatnonzero(counts[0] + counts[1]):
        item = {"overlap_weight": int(weights[b])}
        for i, key in enumerate(("old", "new")):
            _, bins, named, _ = model[i]
            item[key] = {
                "n_directional_cells": int(counts[i][b]),
                "target_counts": {
                    a: int(np.count_nonzero((bins == b) & (named == j)))
                    for j, a in enumerate(MENU)
                },
            }
            if weights[b]:
                j = np.searchsorted(matching, b)
                item[key]["metrics"] = scalar_metrics(points[i, j], bin_draws[:, i, j])
        bins_report[interval_label(b)] = item
    gates = kill_flags(raw["follow_pp"])
    return {
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "primary_model": "old",
        "primary_counts": {"lessons": len(notes), "states": len(model[0][3]),
                           "directional_cells": len(all_cells)},
        "primary_0_5b_all_margins": raw,
        "kill_gates": gates,
        "verdict": "kill" if any(gates.values()) else "keep",
        "matched_all_margins": matched_summary(np.ones(len(w), dtype=bool)),
        "matched_positive_margins": matched_summary(positive),
        "margin_bins": bins_report,
        "no_lesson_top_action_counts": {
            label: {a: int(np.count_nonzero(top == j)) for j, a in enumerate(MENU)}
            for label, (_, _, _, top) in zip(("old", "new"), model)
        },
    }


def kill_flags(follow):
    return {
        "follow_index_below_10pp": follow["estimate"] < 10,
        "follow_index_ci_includes_zero": follow["ci95"][0] <= 0 <= follow["ci95"][1],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=4000)
    args = parser.parse_args()
    notes = json.loads((args.data_dir / "lessons.json").read_text())
    with np.load(args.data_dir / "old-policies.npz") as old, np.load(
            args.data_dir / "new-policies.npz") as new:
        report = analyze(old, new, notes, args.bootstrap, 403989)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(f'{report["verdict"].upper()}: {json.dumps(report["kill_gates"])}')
    print("0.5B primary:", report["primary_0_5b_all_margins"]["follow_pp"])
    for section in ("matched_all_margins", "matched_positive_margins"):
        stats = report[section]
        print(section, {key: stats[key]["follow_pp"] for key in ("old", "new")})
        print("1.5B minus 0.5B:", stats["new_minus_old_follow_pp"])


if __name__ == "__main__":
    main()
