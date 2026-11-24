"""Evaluate the two small-margin interventions on the frozen paired assay."""

import argparse
import json
from pathlib import Path

import numpy as np

from analysis_swap import bootstrap_indices, summarize
from design import MENU
from margin import MIN_NATURAL_STATES, SOURCE, STATES, TEST, eligibility, fit_offset, offset_a


METRICS = ("follow_pp", "named_vs_filler_pp", "named_runner_up_flip_pct", "filler_runner_up_flip_pct")


def masked_cells(rule, swapped, filler, pair, notes):
    named = np.array([[MENU.index(note[key]) for key in ("action", "swap_action")]
                      for note in notes])[:, None, :]
    eligible = (np.sort(named, axis=-1) == np.sort(pair, axis=-1)[None, ...]).all(-1)
    own = np.stack([rule.argmax(-1), swapped.argmax(-1)], axis=-1)
    correct = (own == named).astype(float)
    filler_named = filler.argmax(-1)[..., None] == named
    runner_up = (named == pair[None, :, 1, None])
    return np.where(eligible[..., None], 100 * np.stack([
        (correct - (own[..., ::-1] == named)).mean(-1),
        (correct - filler_named).mean(-1),
        (correct * runner_up).sum(-1),
        (filler_named * runner_up).sum(-1),
    ], axis=-1), np.nan), eligible


def mean(cells):
    return np.nansum(cells, axis=(0, 1)) / np.maximum(1, np.isfinite(cells).sum(axis=(0, 1)))


def arm(base, policies, states, notes, draws, seed):
    ids, pair, gap = eligibility(base, range(len(states)))
    if not len(ids):
        return {"n_eligible_states": 0, "metrics": None}
    cells, compatible = masked_cells(*(policies[k][:, ids] for k in ("rule", "swapped", "filler")),
                                     pair, notes)
    point = mean(cells)
    samples = np.array([
        mean(cells[idx]) if compatible[idx].any() else np.full(len(METRICS), np.nan)
        for idx in bootstrap_indices(*cells.shape[:2], draws, seed)
    ])
    return {
        "n_eligible_states": len(ids),
        "eligible_state_ids": np.asarray(states)[ids].tolist(),
        "eligible_lesson_state_cells": int(compatible.sum()),
        "margin_bins": np.histogram(gap, [0, 0.25, 0.5, 0.75, 1])[0].tolist(),
        "margins_by_eligible_state": gap.tolist(),
        "top_two_actions_by_eligible_state": ["".join(MENU[j] for j in row) for row in pair],
        "metrics": {metric: summarize(point[i], samples[:, i]) for i, metric in enumerate(METRICS)},
    }


def classify(controlled, natural):
    if natural["n_eligible_states"] < MIN_NATURAL_STATES or not controlled["n_eligible_states"]:
        return "inconclusive", "insufficient eligible states"
    estimates = [r["metrics"]["follow_pp"] for r in (controlled, natural)]
    if all(x["estimate"] >= 10 and x["ci95"][0] > 0 for x in estimates):
        return "margin", "both follow indices are at least 10 pp with CIs above zero"
    if all(x["ci95"][0] >= -5 and x["ci95"][1] <= 5 for x in estimates):
        return "scale", "both follow CIs lie entirely within ±5 pp"
    return "inconclusive", "the two arms do not establish either margin following or near-zero equivalence"


def analyze(old, new, natural, notes, draws):
    base_old = old["base"].reshape(STATES, len(MENU))
    base_new = new["base"].reshape(STATES, len(MENU))
    offset, loss = fit_offset(base_old[SOURCE], base_new[SOURCE])
    seed = 403991
    controlled = arm(
        offset_a(base_new[TEST], offset),
        {key: offset_a(new[key].reshape(len(notes), STATES, len(MENU))[:, TEST], offset)
         for key in ("rule", "swapped", "filler")},
        TEST, notes, draws, seed,
    )
    states = natural["state_ids"]
    if len(np.unique(states)) != len(states):
        raise ValueError("Natural states must be distinct")
    natural_results = arm(natural["base"], natural, states, notes, draws, seed)
    verdict, reason = classify(controlled, natural_results)
    return {
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "source_state_ids": SOURCE.tolist(),
        "a_logit_offset": offset,
        "source_margin_fit_mean_absolute_quantile_error": loss,
        "controlled": controlled,
        "natural": natural_results,
        "verdict": verdict,
        "verdict_reason": reason,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--swap-data", type=Path, required=True)
    parser.add_argument("--natural", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=4000)
    args = parser.parse_args()
    notes = json.loads((args.swap_data / "lessons.json").read_text())
    with np.load(args.swap_data / "old-policies.npz") as old, np.load(
            args.swap_data / "new-policies.npz") as new, np.load(args.natural) as natural:
        report = analyze(old, new, natural, notes, args.bootstrap)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    for arm_name in ("controlled", "natural"):
        r = report[arm_name]
        print(f"{arm_name}: {r['n_eligible_states']} states, "
              f"{r['metrics']['follow_pp'] if r['metrics'] else 'no estimate'}")
    print(f"{report['verdict'].upper()}: {report['verdict_reason']}")


if __name__ == "__main__":
    main()
