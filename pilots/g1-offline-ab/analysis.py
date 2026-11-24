"""Calculate offline estimates, overlap and paired bootstrap comparisons."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata
from sklearn.feature_extraction.text import TfidfVectorizer

from agent import ACTIONS, CODES, LESSONS, N_FRESH, ROOT, STEPS


SCORE_NAMES = ("dr", "pdis", "self_normalized_pdis", "likelihood", "judge", "uplift")


def ess(weights):
    return weights.sum(axis=1) ** 2 / (weights**2).sum(axis=1)


def ratios(log):
    lp = log["policy"][:, np.arange(STEPS), log["states"], log["actions"]]
    np.testing.assert_allclose(lp[0], log["logp"], atol=1e-12, rtol=0)
    delta = lp[1:] - log["logp"]
    return delta, np.exp(delta.cumsum(axis=-1))


def fitted_dr(policy, states, actions, rewards, weights, groups):
    n_policies = len(policy)
    corrected = weights[:, :, -1] * rewards
    prev_weights = np.concatenate((np.ones_like(weights[:, :, :1]), weights[:, :, :-1]), axis=2)
    for held_out in np.unique(groups):
        train = groups != held_out
        test = ~train
        target = np.broadcast_to(rewards, corrected.shape)
        for step in reversed(range(STEPS)):
            codes, taken = states[:, step], actions[:, step]
            cells = codes * len(ACTIONS) + taken
            n_cells = CODES * len(ACTIONS)
            train_cells = cells[train]
            freq = np.bincount(train_cells, minlength=n_cells)
            train_targets = target[:, train]
            totals = np.stack([np.bincount(train_cells, y, minlength=n_cells) for y in train_targets])
            q = ((totals + 2 * train_targets.mean(axis=1, keepdims=True)) / (freq + 2))
            q = q.reshape(n_policies, CODES, len(ACTIONS))
            values = (policy[:, step] * q).sum(axis=-1)
            target = values[:, codes]
            observed_q = q[:, codes[test], taken[test]]
            corrected[:, test] += (
                prev_weights[:, test, step] * target[:, test]
                - weights[:, test, step] * observed_q
            )
    return corrected.mean(axis=1)


def offline_scores(log, delta, weights, rows):
    states, actions, rewards = (log[key][rows] for key in ("states", "actions", "rewards"))
    policy = np.exp(log["policy"][1:])
    delta, weights = delta[:, rows], weights[:, rows]
    terminal = weights[:, :, -1]
    pdis = (terminal * rewards).mean(axis=1)
    gain = delta.sum(axis=-1)
    groups = rows % 5
    return {
        "dr": fitted_dr(policy, states, actions, rewards, weights, groups),
        "pdis": pdis,
        "self_normalized_pdis": pdis / terminal.mean(axis=1),
        "likelihood": gain[:, rewards == 1].mean(axis=1) - gain[:, rewards == 0].mean(axis=1),
        "ess": ess(weights),
        "sensitive": (np.abs(delta) > 0.1).sum(axis=-1).mean(axis=-1),
    }


def uplift_smoother(lessons):
    # Fixed text-only features are transductive; held-out labels are never used.
    features = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), use_idf=False).fit_transform(lessons)
    kernel = (features @ features.T).toarray() + 1
    groups = np.arange(len(lessons)) % 5
    smoother = np.zeros_like(kernel)
    for fold in np.unique(groups):
        train, test = groups != fold, groups == fold
        gram = kernel[np.ix_(train, train)]
        smoother[np.ix_(test, train)] = np.linalg.solve(
            gram + np.eye(len(gram)), kernel[np.ix_(train, test)],
        ).T
    return smoother


def correlations(scores, truth, lessons):
    ranked = rankdata(np.stack([scores[key][lessons] for key in SCORE_NAMES]), axis=1)
    ranked -= ranked.mean(axis=1, keepdims=True)
    actual = rankdata(truth[lessons])
    actual -= actual.mean()
    denominator = np.linalg.norm(ranked, axis=1) * np.linalg.norm(actual)
    values = np.divide(ranked @ actual, denominator, out=np.full(len(denominator), np.nan),
                       where=denominator != 0)
    return np.append(values, values[0] - values[3:])


def summarize(point, samples):
    interval = np.nanpercentile(samples, [2.5, 97.5], axis=0)
    return {"estimate": np.asarray(point).tolist(), "ci95": np.moveaxis(interval, 0, -1).tolist()}


def evaluate(log, fresh, n_boot):
    delta, weights = ratios(log)
    rows = np.arange(len(log["rewards"]))
    lessons = np.arange(len(LESSONS))
    smoother = uplift_smoother(LESSONS)
    judge = np.exp(fresh["judge_lp"]) @ np.arange(1, 6)

    def estimate(row_draw, slot_draw):
        scores = offline_scores(log, delta, weights, row_draw)
        truth = fresh["rewards"][:, slot_draw].mean(axis=1)
        paired_baseline = log["rewards"][slot_draw].mean()
        scores.update(truth=truth, judge=judge, uplift=smoother @ (truth - paired_baseline))
        return scores

    point = estimate(rows, np.arange(N_FRESH))
    stats = correlations(point, point["truth"], lessons)
    rng = np.random.default_rng(16180)
    draws = []
    rank_draws = []
    for _ in range(n_boot):
        slots = rng.integers(N_FRESH, size=N_FRESH)
        # The first 50 log rows are paired with truth; preserve these pairs.
        log_draw = np.r_[slots, rng.integers(N_FRESH, len(rows), size=len(rows) - N_FRESH)]
        draw = estimate(log_draw, slots)
        draws.append(draw)
        rank_draws.append(correlations(draw, draw["truth"], rng.choice(lessons, len(lessons))))

    prefix = point["ess"]
    corr_names = (*SCORE_NAMES, "dr_minus_likelihood", "dr_minus_judge", "dr_minus_uplift")
    rank_draws = np.asarray(rank_draws)
    defined = np.isfinite(stats)
    gates = {
        "all_terminal_ess_at_least_50": bool(np.all(prefix[:, -1] >= 50)),
        "dr_spearman_at_least_0.60": bool(defined[0] and stats[0] >= 0.60),
        "dr_margin_likelihood_at_least_0.15": bool(defined[-3] and stats[-3] >= 0.15),
        "dr_margin_judge_at_least_0.15": bool(defined[-2] and stats[-2] >= 0.15),
        "dr_beats_uplift": bool(defined[-1] and stats[-1] > 0),
    }
    return {
        "terminal_ess_below_50": int((prefix[:, -1] < 50).sum()),
        "prefix_ess": summarize(prefix, np.stack([draw["ess"] for draw in draws])),
        "terminal_ess_summary": {
            key: summarize(func(prefix[:, -1]), [func(draw["ess"][:, -1]) for draw in draws])
            for key, func in (("min", np.min), ("median", np.median), ("max", np.max))
        },
        "verdict": "KEEP" if all(gates.values()) else "KILL",
        "gates": gates,
        "counts": {
            "logged": len(rows), "logged_successes": int(log["rewards"].sum()),
            "lessons": len(lessons), "fresh_per_lesson": fresh["rewards"].shape[1],
            "bootstrap": n_boot,
        },
        "rank_comparisons": {
            key: summarize(stats[i], rank_draws[:, i]) if defined[i] else None
            for i, key in enumerate(corr_names)
        },
        "per_lesson": {
            key: summarize(point[key], np.stack([draw[key] for draw in draws]))
            for key in ("truth", "sensitive", *SCORE_NAMES)
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT)
    parser.add_argument("--ess-only", action="store_true")
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    with np.load(args.data / "offline.npz") as data:
        log = dict(data)
    if args.ess_only:
        prefix = ess(ratios(log)[1])
        print("Lesson  ESS@1  ESS@2  ESS@3", flush=True)
        for j, row in enumerate(prefix, 1):
            print(f"{j:02}      " + "  ".join(f"{value:5.1f}" for value in row))
        terminal = prefix[:, -1]
        print(f"ESS<50: {(terminal < 50).sum()}/{len(terminal)}; "
              f"terminal ESS min/median/max: {terminal.min():.1f}/{np.median(terminal):.1f}/{terminal.max():.1f}")
        return
    with np.load(args.data / "fresh.npz") as data:
        fresh = dict(data)
    results = evaluate(log, fresh, args.bootstrap)
    (args.data / "results.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: results[key] for key in (
        "terminal_ess_below_50", "terminal_ess_summary", "verdict", "gates", "counts", "rank_comparisons",
    )}, indent=2))


if __name__ == "__main__":
    main()
