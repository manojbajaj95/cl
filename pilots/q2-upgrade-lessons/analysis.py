"""Exact truth, reliability gate, and paired bootstrap for Fleet Q2."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

from tasks import STEPS, TRUTH_HALVES, correct, exact_success


ROOT = Path(__file__).resolve().parent
N_BOOTSTRAP = 4000
RELIABILITY_MIN = 0.70
RHO_MIN = 0.50
MARGIN_MIN = 0.15


def spearman(x, y):
    x, y = rankdata(x, axis=-1), rankdata(y, axis=-1)
    x -= x.mean(axis=-1, keepdims=True)
    y -= y.mean(axis=-1, keepdims=True)
    norm = np.linalg.norm(x, axis=-1) * np.linalg.norm(y, axis=-1)
    rho = np.divide((x * y).sum(axis=-1), norm, out=np.full_like(norm, np.nan), where=norm != 0)
    return np.clip(rho, -1, 1)


def spearman_brown(rho):
    return np.divide(2 * rho, 1 + rho, out=np.full_like(rho, np.nan), where=rho > -1)


def boot_samples(n):
    return np.random.default_rng(20261125).integers(n, size=(N_BOOTSTRAP, n))


def finite(value):
    return float(value) if np.isfinite(value) else None


def estimate(point, samples):
    samples = samples[np.isfinite(samples)]
    ci = np.quantile(samples, [0.025, 0.975]).tolist() if len(samples) else None
    return {"estimate": finite(point), "ci": ci}


def truth_gate(lessons, new, draws=None):
    success = exact_success(new)
    delta = success[1:] - success[0]
    halves = np.split(delta, [len(TRUTH_HALVES[0])], axis=-1)
    a, b = (half.mean(axis=-1) for half in halves)
    raw = spearman(a, b)
    corrected = spearman_brown(raw)
    if draws is None:
        draws = boot_samples(len(lessons))
    raw_draws = spearman(a[draws], b[draws])
    return {
        "passes": bool(corrected >= RELIABILITY_MIN),
        "spearman_brown": estimate(corrected, spearman_brown(raw_draws)),
        "raw_spearman": estimate(raw, raw_draws),
        "new_zero_shot_held_out": float(success[0].mean()),
    }, delta


def log_selection(policy, states, actions):
    return policy[:, np.arange(STEPS), states, actions]


def gains_on_successful_actions(policy, states, actions):
    gains = log_selection(policy[1:] - policy[:1], states, actions)
    logged_success = actions == correct(states)
    if not logged_success.any():
        raise ValueError("No verifier-correct logged actions")
    return gains[:, logged_success].mean(axis=-1)


def source_scores(lessons, new, source, judge):
    states, actions = source["old_states"], source["old_actions"]
    old = source["old"]
    scores = {
        "new_likelihood": gains_on_successful_actions(new, states, actions),
        "new_zero_shot": np.array([exact_success(new[0], x["source"]).mean() for x in lessons]),
        "old_likelihood": gains_on_successful_actions(old, states, actions),
        "new_model_judge": np.exp(judge) @ np.arange(1, 6),
    }
    gold = correct(states)
    new_gold = log_selection(new, states, gold)
    old_gold = log_selection(old, states, gold)
    l1, l2 = old_gold[1:] - old_gold[0], new_gold[1:] - new_gold[0]
    upgrade = new_gold[0] - old_gold[0]
    scores["oracle_new_log_gain"] = l2.mean(axis=(1, 2))
    norm = np.linalg.norm(l1.reshape(len(lessons), -1), axis=-1) * np.linalg.norm(upgrade)
    scores["lift_alignment"] = np.divide(-(l1 * upgrade).sum(axis=(1, 2)), norm,
                                         out=np.zeros_like(norm), where=norm != 0)
    if (upgrade > 0).any():
        scores["lift_on_improved"] = l2[:, upgrade > 0].mean(axis=-1)
    if "new_states" in source:
        m2_states = source["new_states"]
        m2_gold = np.exp(log_selection(new, m2_states, correct(m2_states)))
        scores["frozen_weighted_lift"] = (m2_gold[1:] - m2_gold[0]).mean(axis=(1, 2))

    # Approximate the frozen selective-maintenance check with exact greedy source replay.
    greedy = new[1:, np.arange(STEPS), states, :].argmax(axis=-1)
    replay = []
    for i, lesson in enumerate(lessons):
        chosen = np.isin(states[:, 0], lesson["source"])[:, None] & (actions == gold)
        replay.append((greedy[i, chosen] == actions[chosen]).mean() if chosen.any() else np.nan)
    if np.isfinite(replay).all():
        scores["source_replay"] = np.array(replay)
    return scores


def compare(scores, target, draws):
    points = {name: spearman(score, target) for name, score in scores.items()}
    samples = {name: spearman(score[draws], target[draws]) for name, score in scores.items()}
    rhos = {name: estimate(points[name], samples[name]) for name in scores}
    margins = {}
    for name in scores:
        if name == "new_likelihood":
            continue
        strength = np.abs if name == "new_zero_shot" else lambda x: x
        margins[name] = estimate(points["new_likelihood"] - strength(points[name]),
                                 samples["new_likelihood"] - strength(samples[name]))
    return rhos, margins


def ranking(lessons, truth, source, judge, target, draws):
    scores = source_scores(lessons, truth, source, judge)
    old = exact_success(source["old"]).mean(axis=-1)
    old_delta = old[1:] - old[0]
    obsolete = (old_delta > 0) & (target <= 0)
    harmful = target < 0
    rhos, margins = compare(scores, target, draws)
    states, actions = source["old_states"], source["old_actions"]
    return {
        "rhos": rhos, "predictor_margins": margins, "old_zero_shot_held_out": float(old[0]),
        "old_probe_states": int(len({(step, code) for trace in states for step, code in enumerate(trace)})),
        "old_successful_actions": int((actions == correct(states)).sum()),
        "old_probe_episodes": int(len(states)),
        "obsolete": int(obsolete.sum()), "harmful": int(harmful.sum()),
        "obsolete_or_harmful": int((obsolete | harmful).sum()),
    }, scores, old_delta


def analyze(lessons, truth, source=None, replication=None, pruning=None):
    draws = boot_samples(len(lessons))
    gate, delta = truth_gate(lessons, truth, draws)
    target = delta.mean(axis=1)
    half_a, half_b = np.split(delta, [len(TRUTH_HALVES[0])], axis=-1)
    rows = [{"id": lesson["id"], "kind": lesson["kind"], "truth_delta": float(target[i]),
             "truth_a_delta": float(half_a[i].mean()), "truth_b_delta": float(half_b[i].mean())}
            for i, lesson in enumerate(lessons)]
    result = {"reliability": gate, "lessons": rows}
    if not gate["passes"]:
        return {**result, "verdict": "STOP: unreliable truth"}
    if source is None:
        return {**result, "verdict": "PENDING: collect source scores"}
    ranks, scores, old_delta = ranking(lessons, truth, source, source["judge"], target, draws)
    new_states = source["new_states"]
    ranks["new_probe_states"] = len({(step, code) for trace in new_states for step, code in enumerate(trace)})
    for i, row in enumerate(rows):
        row.update({name: float(values[i]) for name, values in scores.items()})
        row["old_truth_delta"] = float(old_delta[i])
    rho = ranks["rhos"]["new_likelihood"]["estimate"]
    margin = ranks["predictor_margins"]["new_zero_shot"]["estimate"]
    keep = rho is not None and margin is not None and rho >= RHO_MIN and margin >= MARGIN_MIN
    result.update(verdict="KEEP" if keep else "KILL",
                  frozen_prevalence_gate_passes=ranks["obsolete_or_harmful"] >= 6, **ranks)
    by_text = {}
    for i, lesson in enumerate(lessons):
        by_text.setdefault(lesson["note"], []).append(i)
    groups = list(by_text.values())
    if len(groups) != len(lessons):
        def collapse(values):
            return np.array([values[idx].mean() for idx in groups])

        sensitivity, differences = compare(
            {name: collapse(values) for name, values in scores.items()}, collapse(target),
            boot_samples(len(groups)),
        )
        result["distinct_text_sensitivity"] = {
            "texts": len(groups), "rhos": sensitivity, "predictor_margins": differences,
        }
    if replication is not None:
        result["replication"], _, _ = ranking(lessons, truth, replication, source["judge"], target, draws)
    if pruning is not None:
        success = exact_success(pruning["policy"]).mean(axis=-1)
        differences = success[:, 1] - success[:, 0]
        result["pruning"] = {
            "packs": len(success),
            "reload_all_success": float(success[:, 0].mean()),
            "pruned_success": float(success[:, 1].mean()),
            "delta": estimate(differences.mean(), differences[boot_samples(len(success))].mean(axis=1)),
            "tokens_min": int(pruning["tokens"].min()),
            "tokens_max": int(pruning["tokens"].max()),
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=ROOT)
    args = parser.parse_args()
    lessons = json.loads((args.artifacts / "lessons.json").read_text())
    with np.load(args.artifacts / "truth.npz") as truth_file:
        truth = truth_file["new"]
    gate, _ = truth_gate(lessons, truth)
    source, replication, pruning = None, None, None
    if gate["passes"] and (args.artifacts / "source.npz").is_file():
        with np.load(args.artifacts / "source.npz") as source_file:
            source = dict(source_file)
        if (args.artifacts / "replication.npz").is_file():
            with np.load(args.artifacts / "replication.npz") as replication_file:
                replication = dict(replication_file)
        if (args.artifacts / "pruning.npz").is_file():
            with np.load(args.artifacts / "pruning.npz") as pruning_file:
                pruning = dict(pruning_file)
    result = analyze(lessons, truth, source, replication, pruning)
    (args.artifacts / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "lessons"}, indent=2))


if __name__ == "__main__":
    main()
