"""Run the fixed, balanced A3 comparison from collected policy tables."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import log_softmax

from router import CODES, HELD_OUT, SOURCE, correct, exact_success, start_visitation


def entropy(logp, visits):
    return float(-np.sum(visits[..., None] * np.exp(logp) * logp))


def match_temperature(base, lesson, source):
    visits = start_visitation(base, source)
    target = entropy(lesson, visits)
    logits = base - base.max(-1, keepdims=True)

    def policy(beta):
        return log_softmax(logits * beta, axis=-1)

    def difference(beta):
        return entropy(policy(beta), visits) - target

    cap = 1.0
    while difference(cap) > 0:
        cap *= 2
        if cap > 2**30:
            raise ValueError("Source entropy is below the attainable range")
    beta = brentq(difference, 0, cap, xtol=1e-12)
    matched = policy(beta)
    return beta, matched, target, entropy(matched, visits)


def r2(effect, predicted):
    total = np.square(effect - effect.mean()).sum()
    return float(1 - np.square(effect - predicted).sum() / total) if total > 0 else np.nan


def lesson_share(effect):
    total = np.square(effect - effect.mean()).sum()
    lesson = effect.shape[1] * np.square(effect.mean(1) - effect.mean()).sum()
    return float(lesson / total) if total > 0 else np.nan


def correlation(a, b):
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def metrics(lesson, matched, filler, source, rule):
    return {
        "held_out_r2_pooled": r2(lesson, matched),
        "held_out_r2_non_rule": r2(lesson[~rule], matched[~rule]),
        "rule_minus_temperature_pp": float(100 * (lesson[rule] - matched[rule]).mean()),
        "other_minus_temperature_pp": float(100 * (lesson[~rule] - matched[~rule]).mean()),
        "lesson_main_effect_share": lesson_share(lesson),
        "balanced_split_half_pearson_r": correlation(source.mean(1), lesson.mean(1)),
        "rule_minus_no_lesson_pp": float(100 * lesson[rule].mean()),
        "other_minus_no_lesson_pp": float(100 * lesson[~rule].mean()),
        "temperature_minus_no_lesson_pp": float(100 * matched.mean()),
        "filler_minus_no_lesson_pp": float(100 * filler.mean()),
        "lesson_minus_filler_pp": float(100 * (lesson - filler).mean()),
        "rule_minus_filler_pp": float(100 * (lesson[rule] - filler[rule]).mean()),
        "other_minus_filler_pp": float(100 * (lesson[~rule] - filler[~rule]).mean()),
    }


def bootstrap(lesson, matched, filler, source, notes, draws, seed):
    rule = np.array([note["rule"] for note in notes])
    failure = np.array([note["kind"] == "failure" for note in notes])
    strata = [np.flatnonzero((rule == r) & (failure == f))
              for r in (False, True) for f in (False, True)]
    point = metrics(lesson, matched, filler, source, rule)
    samples = {key: [] for key in point}
    rng = np.random.default_rng(seed)
    for _ in range(draws):
        ids = np.concatenate([rng.choice(s, size=len(s)) for s in strata])
        draw = metrics(lesson[ids], matched[ids], filler[ids], source[ids], rule[ids])
        for key, value in draw.items():
            samples[key].append(value)
    return {
        key: {
            "estimate": value,
            "ci95": np.nanpercentile(samples[key], [2.5, 97.5]).tolist(),
        }
        for key, value in point.items()
    }


def verdict(stats):
    return {
        "held_out_r2_below_0_50": stats["held_out_r2_pooled"]["estimate"] < 0.50,
        "rule_minus_match_at_least_5pp_and_ci_above_zero": (
            stats["rule_minus_temperature_pp"]["estimate"] >= 5
            and stats["rule_minus_temperature_pp"]["ci95"][0] > 0
        ),
        "lesson_main_effect_above_25pct": stats["lesson_main_effect_share"]["estimate"] > 0.25,
    }


def analyze(tables, notes, draws, seed):
    base, lesson, filler = (tables[key] for key in ("base", "lesson", "filler"))
    beta, policies, target, entropy_matched = zip(
        *(match_temperature(base, logp, SOURCE) for logp in lesson)
    )
    starts = list(range(CODES))
    base_success = exact_success(base, starts)
    lesson_success = exact_success(lesson, starts)
    matched_success = exact_success(np.stack(policies), starts)
    filler_success = exact_success(filler, starts)
    lesson_effect, temp_effect, filler_effect = (
        success - base_success for success in (lesson_success, matched_success, filler_success)
    )
    base_modes = base.argmax(-1)
    modal_path_logp = np.where(np.eye(base.shape[-1])[base_modes] > 0, 0.0, -np.inf)
    base_modal_success = exact_success(modal_path_logp, starts).astype(bool)
    visits = start_visitation(base, SOURCE)
    base_source_entropy = entropy(base, visits)
    unique = list({note["text"]: i for i, note in reversed(list(enumerate(notes)))}.values())
    effects = (lesson_effect[:, HELD_OUT], temp_effect[:, HELD_OUT],
               filler_effect[:, HELD_OUT], lesson_effect[:, SOURCE])
    return {
        "metrics": bootstrap(*effects, notes, draws, seed),
        "unique_prompt_sensitivity": {
            "n": len(unique),
            "metrics": bootstrap(*(arm[unique] for arm in effects),
                                 [notes[i] for i in unique], draws, seed),
        },
        "no_lesson_success_by_start": base_success.tolist(),
        "no_lesson_modal_trajectory_success_by_start": base_modal_success.tolist(),
        "no_lesson_modal_actions_by_checkpoint_and_start": base_modes.tolist(),
        "no_lesson_mode_correct_by_checkpoint_and_start": (
            base_modes == correct(np.arange(CODES))
        ).tolist(),
        "mean_no_lesson_held_out_success": float(base_success[list(HELD_OUT)].mean()),
        "no_lesson_source_entropy_nats": base_source_entropy,
        "max_abs_source_entropy_match_error_nats": float(
            np.max(np.abs(np.subtract(target, entropy_matched)))
        ),
        "lessons_with_lower_source_entropy_than_baseline": int(
            np.count_nonzero(np.array(target) < base_source_entropy)
        ),
        "per_lesson": [
            {
                "id": note["id"],
                "tokens_per_prompt": int(tables["prompt_tokens"][i]),
                "filler": str(tables["filler_text"][i]),
                "inverse_temperature": beta[i],
                "source_entropy_nats": target[i],
                "matched_source_entropy_nats": entropy_matched[i],
                "success_by_start": {
                    "lesson": lesson_success[i].tolist(),
                    "temperature_match": matched_success[i].tolist(),
                    "filler": filler_success[i].tolist(),
                },
            }
            for i, note in enumerate(notes)
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=4000)
    args = parser.parse_args()
    notes = json.loads((args.data_dir / "lessons.json").read_text())
    seed = 421803
    report = {
        "source_starts": [s + 10 for s in SOURCE],
        "held_out_starts": [s + 10 for s in HELD_OUT],
        "bootstrap_draws": args.bootstrap,
        "bootstrap_seed": seed,
        "primary_model": "new",
        "models": {},
    }
    for label in ("old", "new"):
        with np.load(args.data_dir / f"{label}-policies.npz") as tables:
            report["models"][label] = analyze(tables, notes, args.bootstrap, seed)
    metrics = report["models"]["new"]["metrics"]
    report["kill_gates"] = verdict(metrics)
    report["verdict"] = "kill" if any(report["kill_gates"].values()) else "keep"
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(metrics, indent=2))
    print(f'{report["verdict"].upper()}: {json.dumps(report["kill_gates"])}')


if __name__ == "__main__":
    main()
