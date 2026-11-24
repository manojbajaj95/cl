"""Exact lesson-by-start decomposition for the G1 (PR #14) and Q2 (PR #25) routers.

Inputs are the checked-in constrained policy tables: G1 offline.npz["policy"] (index 0 = no
lesson) and Q2 truth.npz["new"] (index 0 = no lesson). Every action path is enumerated, so
there is no rollout noise.
"""

import argparse
import json
from itertools import product

import numpy as np

STEPS, CODES, A = 3, 12, 3


def correct(code):
    return (code + 11) % 3


def transition(code, action, step):
    return (5 * code + 2 * action + 1 + step) % CODES


def exact(logp):
    """Success probability per (policy, start) and the no-lesson visitation/Q tables."""
    p = np.exp(logp)
    starts = np.arange(CODES)
    succ = np.zeros((len(p), CODES))
    for acts in product(range(A), repeat=STEPS):
        code, hits, path = starts.copy(), np.zeros(CODES, int), np.ones((len(p), CODES))
        for step, a in enumerate(acts):
            path *= p[:, step, code, a]
            hits += correct(code) == a
            code = transition(code, a, step)
        succ += path * (hits >= 2)
    return succ


def first_order(logp):
    """Linearized per-start effect: sum over (step, code) of base visitation x (pi_l - pi_0) . Q_0."""
    p = np.exp(logp)
    base = p[0]
    # Q_0[step, code, a, hits_so_far] -> success prob under base continuation
    V = np.zeros((STEPS + 1, CODES, STEPS + 1))
    V[STEPS] = (np.arange(STEPS + 1) >= 2)[None, :]
    Q = np.zeros((STEPS, CODES, A, STEPS + 1))
    for step in reversed(range(STEPS)):
        for c in range(CODES):
            for a in range(A):
                nxt = transition(c, a, step) if step + 1 < STEPS else 0
                for h in range(STEPS + 1):
                    h2 = min(h + (correct(c) == a), STEPS)
                    Q[step, c, a, h] = V[step + 1, nxt, h2]
            V[step, c] = (base[step, c][:, None] * Q[step, c]).sum(0)
    # base visitation d[start, step, code, hits]
    d = np.zeros((CODES, STEPS, CODES, STEPS + 1))
    for s in range(CODES):
        d[s, 0, s, 0] = 1
        for step in range(STEPS - 1):
            for c in range(CODES):
                for h in range(STEPS + 1):
                    m = d[s, step, c, h]
                    if m:
                        for a in range(A):
                            d[s, step + 1, transition(c, a, step), min(h + (correct(c) == a), STEPS)] += m * base[step, c, a]
    dp = p[1:] - base[None]  # lesson, step, code, a
    return np.einsum("sjch,ljca,jcah->ls", d, dp, Q)


def decompose(eff):
    grand = eff.mean()
    row = eff.mean(1, keepdims=True) - grand
    col = eff.mean(0, keepdims=True) - grand
    inter = eff - grand - row - col
    ss = lambda x: float((x ** 2).sum())
    total = ss(eff - grand)
    u, sv, vt = np.linalg.svd(inter, full_matrices=False)
    return {
        "lesson_main_share": ss(row * np.ones_like(eff)) / total,
        "start_main_share": ss(col * np.ones_like(eff)) / total,
        "interaction_share": ss(inter) / total,
        "interaction_rank1_share_of_interaction": float(sv[0] ** 2 / (sv ** 2).sum()),
        "lessons_with_both_signs": int(((eff > 1e-4).any(1) & (eff < -1e-4).any(1)).sum()),
        "n_lessons": int(eff.shape[0]),
    }


def split_half(eff, halves, rng, draws=0):
    a, b = eff[:, halves[0]].mean(1), eff[:, halves[1]].mean(1)
    r = float(np.corrcoef(a, b)[0, 1])
    rs = []
    for _ in range(draws):
        perm = rng.permutation(CODES)
        rs.append(np.corrcoef(eff[:, perm[:6]].mean(1), eff[:, perm[6:]].mean(1))[0, 1])
    return r, rs


def analyse(name, logp, halves):
    succ = exact(logp)
    eff = succ[1:] - succ[0]
    lin = first_order(logp)
    rng = np.random.default_rng(0)
    r_frozen, rs = split_half(eff, halves, rng, 2000)
    resid = eff - lin
    out = {
        "base_success_by_start": succ[0].round(4).tolist(),
        "effect_pp_mean_by_start": (100 * eff.mean(0)).round(3).tolist(),
        "effect_pp_range": [float(100 * eff.mean(1).min()), float(100 * eff.mean(1).max())],
        "decomposition": decompose(eff),
        "split_half_r_frozen_halves": r_frozen,
        "split_half_r_random_6v6": [float(np.mean(rs)), *np.percentile(rs, [2.5, 97.5]).tolist()],
        "first_order_R2_per_cell": float(1 - (resid ** 2).sum() / ((eff - eff.mean()) ** 2).sum()),
        "first_order_R2_interaction_only": float(1 - ((resid - resid.mean(0) - resid.mean(1, keepdims=True) + resid.mean()) ** 2).sum()
                                                 / ((eff - eff.mean(0) - eff.mean(1, keepdims=True) + eff.mean()) ** 2).sum()),
    }
    # per-cell lesson property: change in prob of the correct action at each (step, code)
    p = np.exp(logp)
    corr_mass = np.stack([p[:, :, c, correct(c)] for c in range(CODES)], -1)  # pol, step, code
    dcorr = (corr_mass[1:] - corr_mass[0]).reshape(len(eff), -1)
    cell_sd_across_lessons = dcorr.std(0)
    out["per_cell_correct_mass_change"] = {
        "mean_abs_pp": float(100 * np.abs(dcorr).mean()),
        "share_cells_with_both_signs_across_lessons": float(((dcorr > 1e-3).any(0) & (dcorr < -1e-3).any(0)).mean()),
        "lessons_with_both_signs_across_cells": int(((dcorr > 1e-3).any(1) & (dcorr < -1e-3).any(1)).sum()),
        "mean_cell_sd_pp": float(100 * cell_sd_across_lessons.mean()),
    }
    print(name, json.dumps({k: v for k, v in out.items() if "by_start" not in k}, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--g1", required=True)
    ap.add_argument("--q2", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    g1 = np.load(args.g1)["policy"]
    q2 = np.load(args.q2)["new"]
    res = {
        # G1 has no frozen halves; use Q2's halves for comparability.
        "g1": analyse("g1", g1, ((3, 4, 5, 9, 10, 11), (0, 1, 2, 6, 7, 8))),
        "q2_heldout_halves": analyse("q2", q2, ((3, 4, 5), (9, 10, 11))),
    }
    with open(args.output, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
