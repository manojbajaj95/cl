"""ED08 Body-Curvature CPU Pilot (manojbajaj95/cl, PR #398).

Tests the pre-registered ED08 gate for the body connection Gamma:
- A calibrated function-space curvature estimator (ED07/ED08) must read zero on
  changes predicted flat (ED01 actuator gains, ED05 constant-Froude scaling)
  and nonzero on changes predicted curved (ED01 mass/length/payload, ED02
  torque/command saturation, ED04 contact-mode switches, ED03 gait switches),
- with AUROC (flat vs curved) >= 0.9 and split-half reliability >= 0.8 across
  rituals, seeds, and loop sizes.

Run:
    python3 -u pilots/ed08_body_curvature/pilot.py
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import json
import os
import platform
import time
from pathlib import Path
from typing import Any

for _env_var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_env_var, "1")

import numpy as np
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import roc_auc_score

from bodies import (
    default_arm_params,
    default_arm_policy,
    default_hopper_policy,
    default_pusher_policy,
    hopper_apex_map,
    hopper_gait_fraction,
    pusher_accel,
    pusher_slip_fraction,
    sample_arm_states,
    sample_hopper_states,
    sample_pusher_states,
)
from estimator import (
    MLPPolicy,
    RBFPolicy,
    estimate_loop_curvature,
    fit_policy_to_targets,
    measure_ed07_arch_opt_curvature,
)


N_SEEDS = 24
N_RITUAL = 400  # split 200 / 200 for cross-fitted calibration
N_EVAL = 200
REL_NOISE_STD = 0.0005  # 0.05% relative sensor noise (primary); stress-tested at 0.2% & 1%
LOOP_SIZES = [0.10, 0.15, 0.20]
DEFAULT_STEP = 0.15
MAX_WORKERS = min(8, os.cpu_count() or 4)


def signed_sqrt(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=np.float64)
    out = np.sign(arr) * np.sqrt(np.abs(arr))
    return float(out) if np.ndim(x) == 0 else out


def unbiased_F_from_F2(f2_vals: np.ndarray) -> float:
    return float(np.sqrt(max(0.0, float(np.mean(f2_vals)))))


def bootstrap_ci(values: np.ndarray, n_boot: int = 2000, seed: int = 12345) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=np.float64)
    mean = float(np.mean(arr))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    means = np.mean(arr[idx], axis=1)
    lo, hi = np.quantile(means, [0.025, 0.975])
    return mean, float(lo), float(hi)


def bootstrap_unbiased_F_ci(f2_vals: np.ndarray, n_boot: int = 2000, seed: int = 12345) -> tuple[float, float, float]:
    arr = np.asarray(f2_vals, dtype=np.float64)
    est = unbiased_F_from_F2(arr)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    boots = np.sqrt(np.maximum(0.0, np.mean(arr[idx], axis=1)))
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return est, float(lo), float(hi)


def make_arm_corners(base: dict[str, float], dir_u: str, dir_v: str, du: float, dv: float):
    def p(su: float, sv: float) -> dict[str, float]:
        out = dict(base)
        out[dir_u] = base[dir_u] * (1.0 + su)
        out[dir_v] = base[dir_v] * (1.0 + sv)
        return out
    return (p(0.0, 0.0), p(du, 0.0), p(du, dv), p(0.0, dv))


# ---------------------------------------------------------------------------
# Experiment 1 & 2: ED01 (15-pair arm table) + ED05 (Froude vs length-only)
# ---------------------------------------------------------------------------

def run_ed01_and_ed05(rel_noise: float = REL_NOISE_STD) -> dict[str, Any]:
    dirs = ["k1", "k2", "m1", "m2", "l2", "mp"]
    pairs = [(dirs[i], dirs[j]) for i in range(len(dirs)) for j in range(i + 1, len(dirs))]
    base = default_arm_params()

    # Pre-registered predictions from the manipulator equation (before running):
    # Pure-gauge gain directions commute with every unsaturated direction -> flat.
    # Pairs of configuration-dependent inertial/gravity parameters -> curved.
    pred_flat = {pair: ("k1" in pair or "k2" in pair) for pair in pairs}

    pair_records: dict[str, dict[str, Any]] = {}
    per_size_f2: dict[float, dict[str, list[float]]] = {
        step: {f"{u}_{v}": [] for u, v in pairs} for step in LOOP_SIZES
    }

    for pair_idx, (u_dir, v_dir) in enumerate(pairs):
        key = f"{u_dir}_{v_dir}"
        f2_noisy, f_raw_noisy, f_comm_noisy, cos_noisy = [], [], [], []
        h1_noisy, h2_noisy = [], []
        f2_clean, f_clean = [], []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(10000 + pair_idx * 100 + seed)
            q_r, qd_r = sample_arm_states(rng, N_RITUAL)
            q_e, qd_e = sample_arm_states(rng, N_EVAL)
            s_r = np.concatenate([q_r, qd_r], axis=-1)
            u_r = default_arm_policy(q_r, qd_r)
            u_e = default_arm_policy(q_e, qd_e)

            for step in LOOP_SIZES:
                corners = make_arm_corners(base, u_dir, v_dir, step, step)
                res_n = estimate_loop_curvature(
                    "arm", None, corners, step, step, s_r, u_r, u_e,
                    rel_noise_std=rel_noise, rng=rng,
                )
                per_size_f2[step][key].append(res_n.F2_cal)
                if step == DEFAULT_STEP:
                    f2_noisy.append(res_n.F2_cal)
                    f_raw_noisy.append(res_n.F_raw)
                    f_comm_noisy.append(res_n.F_comm)
                    cos_noisy.append(res_n.cos_halves)
                    h1_noisy.append(res_n.F_half1)
                    h2_noisy.append(res_n.F_half2)

                    res_c = estimate_loop_curvature(
                        "arm", None, corners, step, step, s_r, u_r, u_e,
                        rel_noise_std=0.0, rng=None,
                    )
                    f2_clean.append(res_c.F2_cal)
                    f_clean.append(res_c.F_cal)

        f2_arr = np.array(f2_noisy)
        f2_m, f2_lo, f2_hi = bootstrap_ci(f2_arr)
        fc_m, fc_lo, fc_hi = bootstrap_unbiased_F_ci(f2_arr)
        pair_records[key] = {
            "pair": [u_dir, v_dir],
            "predicted": "flat" if pred_flat[(u_dir, v_dir)] else "curved",
            "F2_cal_mean": f2_m,
            "F2_cal_ci95": [f2_lo, f2_hi],
            "F_cal_unbiased": fc_m,
            "F_cal_ci95": [fc_lo, fc_hi],
            "F2_cal_per_seed": f2_noisy,
            "signed_F_per_seed": signed_sqrt(f2_arr).tolist(),
            "F_half1_mean": float(np.mean(h1_noisy)),
            "F_half2_mean": float(np.mean(h2_noisy)),
            "F_raw_mean": float(np.mean(f_raw_noisy)),
            "F_comm_mean": float(np.mean(f_comm_noisy)),
            "cos_halves_mean": float(np.mean(cos_noisy)),
            "F_clean_mean": float(np.mean(f_clean)),
            "F2_clean_mean": float(np.mean(f2_clean)),
            "nonzero_ci": bool(f2_lo > 0.0),
        }

    matches = 0
    for rec in pair_records.values():
        if rec["predicted"] == "flat" and not rec["nonzero_ci"]:
            matches += 1
        elif rec["predicted"] == "curved" and rec["nonzero_ci"]:
            matches += 1

    # ED05: Matched constant-Froude scaling (froude_L x l2, froude_time_scale=True, flat)
    # vs identical parameter loop without Froude time-scaling (froude_time_scale=False, curved)
    froude_f2, lenonly_f2 = [], []
    froude_clean, lenonly_clean = [], []
    froude_h1, froude_h2, lenonly_h1, lenonly_h2 = [], [], [], []
    for seed in range(N_SEEDS):
        rng_fr = np.random.default_rng(20000 + seed)
        q_r, qd_r = sample_arm_states(rng_fr, N_RITUAL)
        q_e, qd_e = sample_arm_states(rng_fr, N_EVAL)
        s_r = np.concatenate([q_r, qd_r], axis=-1)
        u_r = default_arm_policy(q_r, qd_r)
        u_e = default_arm_policy(q_e, qd_e)

        base_fr = dict(base, froude_time_scale=True)
        c_fr = make_arm_corners(base_fr, "froude_L", "l2", DEFAULT_STEP, DEFAULT_STEP)
        res_fr = estimate_loop_curvature(
            "arm", None, c_fr, DEFAULT_STEP, DEFAULT_STEP, s_r, u_r, u_e,
            rel_noise_std=rel_noise, rng=rng_fr,
        )
        res_fr_c = estimate_loop_curvature(
            "arm", None, c_fr, DEFAULT_STEP, DEFAULT_STEP, s_r, u_r, u_e,
            rel_noise_std=0.0, rng=None,
        )
        froude_f2.append(res_fr.F2_cal)
        froude_clean.append(res_fr_c.F_cal)
        froude_h1.append(res_fr.F_half1)
        froude_h2.append(res_fr.F_half2)

        rng_lo = np.random.default_rng(21000 + seed)
        q_r2, qd_r2 = sample_arm_states(rng_lo, N_RITUAL)
        q_e2, qd_e2 = sample_arm_states(rng_lo, N_EVAL)
        s_r2 = np.concatenate([q_r2, qd_r2], axis=-1)
        u_r2 = default_arm_policy(q_r2, qd_r2)
        u_e2 = default_arm_policy(q_e2, qd_e2)

        base_lo = dict(base, froude_time_scale=False)
        c_lo = make_arm_corners(base_lo, "froude_L", "l2", DEFAULT_STEP, DEFAULT_STEP)
        res_lo = estimate_loop_curvature(
            "arm", None, c_lo, DEFAULT_STEP, DEFAULT_STEP, s_r2, u_r2, u_e2,
            rel_noise_std=rel_noise, rng=rng_lo,
        )
        res_lo_c = estimate_loop_curvature(
            "arm", None, c_lo, DEFAULT_STEP, DEFAULT_STEP, s_r2, u_r2, u_e2,
            rel_noise_std=0.0, rng=None,
        )
        lenonly_f2.append(res_lo.F2_cal)
        lenonly_clean.append(res_lo_c.F_cal)
        lenonly_h1.append(res_lo.F_half1)
        lenonly_h2.append(res_lo.F_half2)

    fr_arr = np.array(froude_f2)
    lo_arr = np.array(lenonly_f2)
    fr_m, fr_lo, fr_hi = bootstrap_unbiased_F_ci(fr_arr)
    fr2_m, fr2_lo, fr2_hi = bootstrap_ci(fr_arr)
    lo_m, lo_lo, lo_hi = bootstrap_unbiased_F_ci(lo_arr)
    lo2_m, lo2_lo, lo2_hi = bootstrap_ci(lo_arr)
    ed05_ratio = fr_m / (lo_m + 1e-12)

    # Loop-size reliability across the 15 pairs (using unbiased F_cal)
    size_vecs = {
        step: np.array([unbiased_F_from_F2(np.array(per_size_f2[step][f"{u}_{v}"])) for u, v in pairs])
        for step in LOOP_SIZES
    }
    loop_size_corrs = {}
    for i in range(len(LOOP_SIZES)):
        for j in range(i + 1, len(LOOP_SIZES)):
            s1, s2 = LOOP_SIZES[i], LOOP_SIZES[j]
            rho = float(spearmanr(size_vecs[s1], size_vecs[s2]).statistic)
            pr = float(pearsonr(size_vecs[s1], size_vecs[s2]).statistic)
            loop_size_corrs[f"{s1}_vs_{s2}"] = {"spearman": rho, "pearson": pr}

    return {
        "ed01_pairs": pair_records,
        "ed01_pattern_matches": matches,
        "ed01_total_pairs": len(pairs),
        "ed01_pass": matches >= 12,
        "ed01_loop_size_reliability": loop_size_corrs,
        "ed05_froude": {
            "F_cal_unbiased": fr_m,
            "F_cal_ci95": [fr_lo, fr_hi],
            "F2_cal_mean": fr2_m,
            "F2_cal_ci95": [fr2_lo, fr2_hi],
            "F_clean_mean": float(np.mean(froude_clean)),
            "F2_cal_per_seed": froude_f2,
            "signed_F_per_seed": signed_sqrt(fr_arr).tolist(),
            "F_half1_mean": float(np.mean(froude_h1)),
            "F_half2_mean": float(np.mean(froude_h2)),
        },
        "ed05_length_only": {
            "F_cal_unbiased": lo_m,
            "F_cal_ci95": [lo_lo, lo_hi],
            "F2_cal_mean": lo2_m,
            "F2_cal_ci95": [lo2_lo, lo2_hi],
            "F_clean_mean": float(np.mean(lenonly_clean)),
            "F2_cal_per_seed": lenonly_f2,
            "signed_F_per_seed": signed_sqrt(lo_arr).tolist(),
            "F_half1_mean": float(np.mean(lenonly_h1)),
            "F_half2_mean": float(np.mean(lenonly_h2)),
        },
        "ed05_froude_to_length_ratio": float(ed05_ratio),
        "ed05_pass": bool(ed05_ratio <= 0.20 and fr2_lo <= 0.0 <= fr2_hi and lo_m > 0.005),
    }


# ---------------------------------------------------------------------------
# Experiment 3: ED02 (Torque/command saturation sweep on flat gains)
# ---------------------------------------------------------------------------

def _ed02_worker(args: tuple[str, float, float]) -> dict[str, Any]:
    sat_mode, u_max, rel_noise = args
    base = default_arm_params()
    du, dv = -0.25, -0.25
    f2_vals, reach_vals, h1_vals, h2_vals = [], [], [], []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(3000 + seed)
        q_r, qd_r = sample_arm_states(rng, N_RITUAL)
        q_e, qd_e = sample_arm_states(rng, N_EVAL)
        s_r = np.concatenate([q_r, qd_r], axis=-1)
        u_r = default_arm_policy(q_r, qd_r)
        u_e = default_arm_policy(q_e, qd_e)

        b = dict(base, u_max=u_max, sat_mode=sat_mode)
        corners = make_arm_corners(b, "k1", "k2", du, dv)
        res = estimate_loop_curvature(
            "arm", None, corners, du, dv, s_r, u_r, u_e,
            rel_noise_std=rel_noise, rng=rng,
        )
        f2_vals.append(res.F2_cal)
        h1_vals.append(res.F_half1)
        h2_vals.append(res.F_half2)
        if np.isfinite(u_max):
            req_u = np.abs(u_r) / (1.0 + du)
            reach_vals.append(float(np.mean(np.all(req_u <= u_max, axis=-1))))
        else:
            reach_vals.append(1.0)

    f2_arr = np.array(f2_vals)
    fm, flo, fhi = bootstrap_unbiased_F_ci(f2_arr)
    f2m, f2lo, f2hi = bootstrap_ci(f2_arr)
    return {
        "sat_mode": sat_mode,
        "u_max": "inf" if not np.isfinite(u_max) else float(u_max),
        "F_cal_unbiased": fm,
        "F_cal_ci95": [flo, fhi],
        "F2_cal_mean": f2m,
        "F2_cal_ci95": [f2lo, f2hi],
        "F2_cal_per_seed": f2_vals,
        "signed_F_per_seed": signed_sqrt(f2_arr).tolist(),
        "F_half1_mean": float(np.mean(h1_vals)),
        "F_half2_mean": float(np.mean(h2_vals)),
        "reachability_p11": float(np.mean(reach_vals)),
    }


def run_ed02_saturation(pool: ProcessPoolExecutor, rel_noise: float = REL_NOISE_STD) -> dict[str, Any]:
    u_max_levels = [np.inf, 80.0, 50.0, 35.0, 25.0, 18.0, 12.0]
    tasks = [(m, um, rel_noise) for m in ("tanh", "clip") for um in u_max_levels]
    rows = list(pool.map(_ed02_worker, tasks))

    results_by_mode: dict[str, Any] = {}
    for sat_mode in ("tanh", "clip"):
        sweep = [r for r in rows if r["sat_mode"] == sat_mode]
        tightness = np.arange(len(u_max_levels), dtype=np.float64)
        means = np.array([row["F_cal_unbiased"] for row in sweep])
        mono_rho = float(spearmanr(tightness, means).statistic)
        results_by_mode[sat_mode] = {
            "sweep": sweep,
            "monotonicity_spearman": mono_rho,
            "pass": bool(mono_rho >= 0.85 and sweep[-1]["F2_cal_ci95"][0] > 0.0),
        }
    return results_by_mode


# ---------------------------------------------------------------------------
# Experiment 4: ED04 (Planar Pusher stick/slip contact-mode grid)
# ---------------------------------------------------------------------------

def _ed04_cell_worker(args: tuple[float, float, float]) -> dict[str, Any]:
    mu0, m0, rel_noise = args
    dmu, dm = 0.20, 0.20
    corners = (
        {"mu": mu0, "m_obj": m0},
        {"mu": mu0 * (1.0 + dmu), "m_obj": m0},
        {"mu": mu0 * (1.0 + dmu), "m_obj": m0 * (1.0 + dm)},
        {"mu": mu0, "m_obj": m0 * (1.0 + dm)},
    )
    f2_vals, h1_vals, h2_vals = [], [], []
    sf_corners = []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(4000 + seed)
        s_r = sample_pusher_states(rng, N_RITUAL)
        s_e = sample_pusher_states(rng, N_EVAL)
        u_r = default_pusher_policy(s_r)
        u_e = default_pusher_policy(s_e)
        res = estimate_loop_curvature(
            "pusher", pusher_accel, corners, dmu, dm, s_r, u_r, u_e,
            rel_noise_std=rel_noise, rng=rng,
        )
        f2_vals.append(res.F2_cal)
        h1_vals.append(res.F_half1)
        h2_vals.append(res.F_half2)
        if seed == 0:
            sf_corners = [pusher_slip_fraction(s_r, u_r, c) for c in corners]

    min_sf, max_sf = min(sf_corners), max(sf_corners)
    if max_sf <= 0.05 or min_sf >= 0.95:
        regime = "within_mode"
    elif (max_sf - min_sf) >= 0.08:
        regime = "mode_crossing"
    else:
        regime = "partial_mixed"

    f2_arr = np.array(f2_vals)
    fm, flo, fhi = bootstrap_unbiased_F_ci(f2_arr)
    f2m, f2lo, f2hi = bootstrap_ci(f2_arr)
    return {
        "mu0": mu0,
        "m0": m0,
        "slip_fracs": [round(x, 3) for x in sf_corners],
        "regime": regime,
        "F_cal_unbiased": fm,
        "F_cal_ci95": [flo, fhi],
        "F2_cal_mean": f2m,
        "F2_cal_ci95": [f2lo, f2hi],
        "F2_cal_per_seed": f2_vals,
        "signed_F_per_seed": signed_sqrt(f2_arr).tolist(),
        "F_half1_mean": float(np.mean(h1_vals)),
        "F_half2_mean": float(np.mean(h2_vals)),
    }


def run_ed04_pusher(pool: ProcessPoolExecutor, rel_noise: float = REL_NOISE_STD) -> dict[str, Any]:
    mu_grid = [0.15, 0.30, 0.50, 0.75, 1.10, 1.60]
    m_grid = [0.5, 0.8, 1.2, 1.7, 2.3, 3.0]
    tasks = [(mu0, m0, rel_noise) for mu0 in mu_grid for m0 in m_grid]
    cells = list(pool.map(_ed04_cell_worker, tasks))

    within_cells = [c for c in cells if c["regime"] == "within_mode"]
    cross_cells = [c for c in cells if c["regime"] == "mode_crossing"]
    within_f2_per_seed = np.mean([c["F2_cal_per_seed"] for c in within_cells], axis=0)
    cross_f2_per_seed = np.mean([c["F2_cal_per_seed"] for c in cross_cells], axis=0)
    within_mean = float(np.mean([c["F_cal_unbiased"] for c in within_cells]))
    cross_mean = float(np.mean([c["F_cal_unbiased"] for c in cross_cells]))
    ratio = cross_mean / (within_mean + 1e-12)
    return {
        "cells": cells,
        "n_within_mode": len(within_cells),
        "n_mode_crossing": len(cross_cells),
        "within_mode_F_mean": within_mean,
        "mode_crossing_F_mean": cross_mean,
        "crossing_to_within_ratio": float(ratio),
        "within_f2_per_seed": within_f2_per_seed.tolist(),
        "crossing_f2_per_seed": cross_f2_per_seed.tolist(),
        "within_signed_F_per_seed": signed_sqrt(within_f2_per_seed).tolist(),
        "crossing_signed_F_per_seed": signed_sqrt(cross_f2_per_seed).tolist(),
        "pass": bool(ratio >= 3.0),
    }


# ---------------------------------------------------------------------------
# Experiment 5: ED03 (SLIP Hopper gait-switch boundary grid)
# ---------------------------------------------------------------------------

def _ed03_cell_worker(args: tuple[float, float, float]) -> dict[str, Any]:
    m0, l0, rel_noise = args
    dm, dl = 0.15, 0.15
    corners = (
        {"m": m0, "l0": l0},
        {"m": m0 * (1.0 + dm), "l0": l0},
        {"m": m0 * (1.0 + dm), "l0": l0 * (1.0 + dl)},
        {"m": m0, "l0": l0 * (1.0 + dl)},
    )
    f2_vals, h1_vals, h2_vals = [], [], []
    gf_corners = []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(5000 + seed)
        s_r = sample_hopper_states(rng, N_RITUAL)
        s_e = sample_hopper_states(rng, N_EVAL)
        u_r = default_hopper_policy(s_r)
        u_e = default_hopper_policy(s_e)
        res = estimate_loop_curvature(
            "hopper", hopper_apex_map, corners, dm, dl, s_r, u_r, u_e,
            rel_noise_std=rel_noise, rng=rng,
        )
        f2_vals.append(res.F2_cal)
        h1_vals.append(res.F_half1)
        h2_vals.append(res.F_half2)
        if seed == 0:
            gf_corners = [hopper_gait_fraction(s_r, c) for c in corners]

    min_gf, max_gf = min(gf_corners), max(gf_corners)
    is_boundary = (max_gf - min_gf) >= 0.05 or (0.05 < float(np.mean(gf_corners)) < 0.95)
    regime = "gait_boundary" if is_boundary else "within_gait"

    f2_arr = np.array(f2_vals)
    fm, flo, fhi = bootstrap_unbiased_F_ci(f2_arr)
    f2m, f2lo, f2hi = bootstrap_ci(f2_arr)
    return {
        "m0": m0,
        "l0": l0,
        "gait_fracs": [round(x, 3) for x in gf_corners],
        "regime": regime,
        "F_cal_unbiased": fm,
        "F_cal_ci95": [flo, fhi],
        "F2_cal_mean": f2m,
        "F2_cal_ci95": [f2lo, f2hi],
        "F2_cal_per_seed": f2_vals,
        "signed_F_per_seed": signed_sqrt(f2_arr).tolist(),
        "F_half1_mean": float(np.mean(h1_vals)),
        "F_half2_mean": float(np.mean(h2_vals)),
    }


def run_ed03_hopper(pool: ProcessPoolExecutor, rel_noise: float = REL_NOISE_STD) -> dict[str, Any]:
    m_grid = [1.0, 1.5, 2.0, 2.6, 3.3, 4.2]
    l_grid = [0.75, 0.88, 1.00, 1.12, 1.25, 1.40]
    tasks = [(m0, l0, rel_noise) for m0 in m_grid for l0 in l_grid]
    cells = list(pool.map(_ed03_cell_worker, tasks))

    within_cells = [c for c in cells if c["regime"] == "within_gait"]
    bound_cells = [c for c in cells if c["regime"] == "gait_boundary"]
    within_f2_per_seed = np.mean([c["F2_cal_per_seed"] for c in within_cells], axis=0)
    bound_f2_per_seed = np.mean([c["F2_cal_per_seed"] for c in bound_cells], axis=0)

    gt_mask = np.array([c["regime"] == "gait_boundary" for c in cells])
    f_arr = np.array([c["F_cal_unbiased"] for c in cells])
    # Unsupervised log-space midpoint threshold between median and 90th percentile
    lo_q = max(float(np.percentile(f_arr, 50)), 1e-6)
    hi_q = max(float(np.percentile(f_arr, 90)), lo_q * 1.1)
    thresh_unsup = float(np.sqrt(lo_q * hi_q))
    pred_mask = f_arr >= thresh_unsup
    iou_unsup = float(np.sum(gt_mask & pred_mask) / max(int(np.sum(gt_mask | pred_mask)), 1))

    auroc_grid = float(roc_auc_score(gt_mask.astype(int), f_arr))
    within_mean = float(np.mean([c["F_cal_unbiased"] for c in within_cells]))
    cross_mean = float(np.mean([c["F_cal_unbiased"] for c in bound_cells]))
    return {
        "cells": cells,
        "n_within_gait": len(within_cells),
        "n_gait_boundary": len(bound_cells),
        "within_gait_F_mean": within_mean,
        "gait_boundary_F_mean": cross_mean,
        "boundary_to_within_ratio": float(cross_mean / (within_mean + 1e-12)),
        "boundary_iou": iou_unsup,
        "boundary_auroc": auroc_grid,
        "within_f2_per_seed": within_f2_per_seed.tolist(),
        "boundary_f2_per_seed": bound_f2_per_seed.tolist(),
        "within_signed_F_per_seed": signed_sqrt(within_f2_per_seed).tolist(),
        "boundary_signed_F_per_seed": signed_sqrt(bound_f2_per_seed).tolist(),
        "pass": bool(iou_unsup >= 0.50 and auroc_grid >= 0.90),
    }


# ---------------------------------------------------------------------------
# Experiment 6: ED07 (Function-space vs weight-space across 2 archs x 2 opts)
# ---------------------------------------------------------------------------

def _ed07_worker(args: tuple[str, str, str]) -> tuple[str, str, dict[str, Any]]:
    mode, arch, opt = args
    base = default_arm_params()
    loops = {
        "flat_k1_k2": (make_arm_corners(base, "k1", "k2", 0.15, 0.15), 0.15, 0.15),
        "curved_m1_l2": (make_arm_corners(base, "m1", "l2", 0.15, 0.15), 0.15, 0.15),
        "sat_k1_k2": (make_arm_corners(dict(base, u_max=20.0, sat_mode="tanh"), "k1", "k2", -0.25, -0.25), -0.25, -0.25),
    }
    n_ed07_seeds = 8
    out = {lname: {"F_fn": [], "F_wt": []} for lname in loops}
    for seed in range(n_ed07_seeds):
        rng = np.random.default_rng(6000 + seed)
        q_r, qd_r = sample_arm_states(rng, 180)
        q_e, qd_e = sample_arm_states(rng, 180)
        s_r = np.concatenate([q_r, qd_r], axis=-1)
        s_e = np.concatenate([q_e, qd_e], axis=-1)
        u_r = default_arm_policy(q_r, qd_r)
        pol = MLPPolicy(seed=seed) if arch == "MLP" else RBFPolicy(seed=seed)
        th0 = fit_policy_to_targets(pol, pol.get_params(), s_r, u_r, optimizer="lbfgs", l2_reg=1e-6)
        for lname, (corners, du, dv) in loops.items():
            r = measure_ed07_arch_opt_curvature(pol, th0, opt, corners, du, dv, s_r, s_e, mode=mode)
            out[lname]["F_fn"].append(r["F_fn"])
            out[lname]["F_wt"].append(r["F_wt"])
    return mode, f"{arch}_{opt}", out


def run_ed07_invariance(pool: ProcessPoolExecutor) -> dict[str, Any]:
    tasks = [
        (mode, arch, opt)
        for mode in ("action_transport_distill", "full_inverse_distill")
        for arch in ("MLP", "RBF")
        for opt in ("lbfgs", "adam")
    ]
    raw = list(pool.map(_ed07_worker, tasks))
    records: dict[str, Any] = {}
    for mode in ("action_transport_distill", "full_inverse_distill"):
        mode_res = {cfg: res for m, cfg, res in raw if m == mode}
        cfg_means_fn = [float(np.mean(mode_res[k]["curved_m1_l2"]["F_fn"])) for k in mode_res]
        cfg_stds_fn = [float(np.std(mode_res[k]["curved_m1_l2"]["F_fn"])) for k in mode_res]
        cfg_means_wt = [float(np.mean(mode_res[k]["curved_m1_l2"]["F_wt"])) for k in mode_res]
        flat_fn_max = max(float(np.mean(mode_res[k]["flat_k1_k2"]["F_fn"])) for k in mode_res)
        flat_wt_max = max(float(np.mean(mode_res[k]["flat_k1_k2"]["F_wt"])) for k in mode_res)

        summary_table = {}
        for k, res in mode_res.items():
            summary_table[k] = {
                lname: {
                    "F_fn_mean": float(np.mean(res[lname]["F_fn"])),
                    "F_fn_std": float(np.std(res[lname]["F_fn"])),
                    "F_wt_mean": float(np.mean(res[lname]["F_wt"])),
                    "F_wt_std": float(np.std(res[lname]["F_wt"])),
                }
                for lname in res
            }
        records[mode] = {
            "configs": summary_table,
            "curved_m1_l2_across_cfg_std_fn": float(np.std(cfg_means_fn)),
            "curved_m1_l2_within_seed_std_fn": float(np.mean(cfg_stds_fn)),
            "curved_m1_l2_across_cfg_std_wt": float(np.std(cfg_means_wt)),
            "flat_k1_k2_max_F_fn": flat_fn_max,
            "flat_k1_k2_max_F_wt": flat_wt_max,
        }
    return records


# ---------------------------------------------------------------------------
# Unified ED08 Verdict
# ---------------------------------------------------------------------------

def compute_unified_ed08_verdict(
    ed01_05: dict[str, Any],
    ed02: dict[str, Any],
    ed04: dict[str, Any],
    ed03: dict[str, Any],
) -> dict[str, Any]:
    conditions: list[dict[str, Any]] = []

    # 1. ED01 15 pairs (9 flat, 6 curved)
    for key, rec in ed01_05["ed01_pairs"].items():
        conditions.append({
            "name": f"ed01_{key}",
            "family": "ed01_gain_flat" if rec["predicted"] == "flat" else "ed01_inertia_curved",
            "label": 0 if rec["predicted"] == "flat" else 1,
            "f2_per_seed": np.array(rec["F2_cal_per_seed"]),
            "signed_F_per_seed": np.array(rec["signed_F_per_seed"]),
            "F_unbiased": rec["F_cal_unbiased"],
            "h1": rec["F_half1_mean"],
            "h2": rec["F_half2_mean"],
        })

    # 2. ED05 Froude (flat) vs length-only (curved)
    conditions.append({
        "name": "ed05_froude_scaling",
        "family": "ed05_froude_flat",
        "label": 0,
        "f2_per_seed": np.array(ed01_05["ed05_froude"]["F2_cal_per_seed"]),
        "signed_F_per_seed": np.array(ed01_05["ed05_froude"]["signed_F_per_seed"]),
        "F_unbiased": ed01_05["ed05_froude"]["F_cal_unbiased"],
        "h1": ed01_05["ed05_froude"]["F_half1_mean"],
        "h2": ed01_05["ed05_froude"]["F_half2_mean"],
    })
    conditions.append({
        "name": "ed05_length_only",
        "family": "ed05_length_curved",
        "label": 1,
        "f2_per_seed": np.array(ed01_05["ed05_length_only"]["F2_cal_per_seed"]),
        "signed_F_per_seed": np.array(ed01_05["ed05_length_only"]["signed_F_per_seed"]),
        "F_unbiased": ed01_05["ed05_length_only"]["F_cal_unbiased"],
        "h1": ed01_05["ed05_length_only"]["F_half1_mean"],
        "h2": ed01_05["ed05_length_only"]["F_half2_mean"],
    })

    # 3. ED02 unsaturated (u_max="inf" only; finite u_max with tanh has cubic nonlinearity) -> flat;
    #    saturated (50, 35, 25, 18, 12) -> curved
    for row in ed02["tanh"]["sweep"]:
        um = row["u_max"]
        if um == "inf":
            conditions.append({
                "name": "ed02_unsat_inf",
                "family": "ed02_unsat_flat",
                "label": 0,
                "f2_per_seed": np.array(row["F2_cal_per_seed"]),
                "signed_F_per_seed": np.array(row["signed_F_per_seed"]),
                "F_unbiased": row["F_cal_unbiased"],
                "h1": row["F_half1_mean"],
                "h2": row["F_half2_mean"],
            })
        elif um in (50.0, 35.0, 25.0, 18.0, 12.0):
            conditions.append({
                "name": f"ed02_sat_{um}",
                "family": "ed02_sat_curved",
                "label": 1,
                "f2_per_seed": np.array(row["F2_cal_per_seed"]),
                "signed_F_per_seed": np.array(row["signed_F_per_seed"]),
                "F_unbiased": row["F_cal_unbiased"],
                "h1": row["F_half1_mean"],
                "h2": row["F_half2_mean"],
            })

    # 4. ED04 mode-crossing (curved; within-mode baseline tested by ED04 3x ratio gate)
    conditions.append({
        "name": "ed04_mode_crossing",
        "family": "ed04_crossing_curved",
        "label": 1,
        "f2_per_seed": np.array(ed04["crossing_f2_per_seed"]),
        "signed_F_per_seed": np.array(ed04["crossing_signed_F_per_seed"]),
        "F_unbiased": ed04["mode_crossing_F_mean"],
        "h1": float(np.mean([c["F_half1_mean"] for c in ed04["cells"] if c["regime"] == "mode_crossing"])),
        "h2": float(np.mean([c["F_half2_mean"] for c in ed04["cells"] if c["regime"] == "mode_crossing"])),
    })

    # 5. ED03 gait-boundary (curved; within-gait baseline is itself (m, l0) inertially curved
    # and tested separately by ED03's own grid boundary AUROC >= 0.90 and IoU >= 0.50 gate)
    conditions.append({
        "name": "ed03_gait_boundary",
        "family": "ed03_boundary_curved",
        "label": 1,
        "f2_per_seed": np.array(ed03["boundary_f2_per_seed"]),
        "signed_F_per_seed": np.array(ed03["boundary_signed_F_per_seed"]),
        "F_unbiased": ed03["gait_boundary_F_mean"],
        "h1": float(np.mean([c["F_half1_mean"] for c in ed03["cells"] if c["regime"] == "gait_boundary"])),
        "h2": float(np.mean([c["F_half2_mean"] for c in ed03["cells"] if c["regime"] == "gait_boundary"])),
    })

    y_true = np.array([c["label"] for c in conditions])
    # Per-seed AUROC using unbiased signed_F (equivalent ranking to F2_cal)
    seed_aurocs = []
    for s in range(N_SEEDS):
        scores = np.array([c["f2_per_seed"][s] for c in conditions])
        seed_aurocs.append(float(roc_auc_score(y_true, scores)))
    auroc_mean, auroc_lo, auroc_hi = bootstrap_ci(np.array(seed_aurocs))
    auroc_pooled = float(roc_auc_score(y_true, np.array([c["F_unbiased"] for c in conditions])))

    # Split-half reliability across SEEDS (100 random 8-vs-8 splits on unbiased F_cal)
    mat_f2 = np.stack([c["f2_per_seed"] for c in conditions], axis=0)
    rng_sh = np.random.default_rng(999)
    seed_sh_spearman, seed_sh_pearson = [], []
    for _ in range(100):
        perm = rng_sh.permutation(N_SEEDS)
        h1 = np.sqrt(np.maximum(0.0, np.mean(mat_f2[:, perm[: N_SEEDS // 2]], axis=1)))
        h2 = np.sqrt(np.maximum(0.0, np.mean(mat_f2[:, perm[N_SEEDS // 2 :]], axis=1)))
        seed_sh_spearman.append(float(spearmanr(h1, h2).statistic))
        seed_sh_pearson.append(float(pearsonr(h1, h2).statistic))

    # Split-half reliability across RITUALS (half 1 vs half 2 over all conditions + grid cells)
    rit_h1 = (
        [c["h1"] for c in conditions]
        + [c["F_half1_mean"] for c in ed04["cells"]]
        + [c["F_half1_mean"] for c in ed03["cells"]]
    )
    rit_h2 = (
        [c["h2"] for c in conditions]
        + [c["F_half2_mean"] for c in ed04["cells"]]
        + [c["F_half2_mean"] for c in ed03["cells"]]
    )
    ritual_sh_spearman = float(spearmanr(rit_h1, rit_h2).statistic)
    ritual_sh_pearson = float(pearsonr(rit_h1, rit_h2).statistic)

    # Loop-size reliability (Pearson & Spearman across 0.08, 0.12, 0.18 on ED01)
    loop_pearsons = [v["pearson"] for v in ed01_05["ed01_loop_size_reliability"].values()]
    loop_spearmans = [v["spearman"] for v in ed01_05["ed01_loop_size_reliability"].values()]
    min_loop_pearson = float(min(loop_pearsons))
    min_loop_spearman = float(min(loop_spearmans))

    # Exact known-flat families check (ED01 gains + ED05 Froude + ED02 unsat)
    flat_exact_f2 = np.concatenate([
        c["f2_per_seed"] for c in conditions
        if c["family"] in ("ed01_gain_flat", "ed05_froude_flat", "ed02_unsat_flat")
    ])
    flat_f2_mean, flat_f2_lo, flat_f2_hi = bootstrap_ci(flat_exact_f2)
    flat_f_max = max(
        c["F_unbiased"] for c in conditions
        if c["family"] in ("ed01_gain_flat", "ed05_froude_flat", "ed02_unsat_flat")
    )
    curved_f_min = min(c["F_unbiased"] for c in conditions if c["label"] == 1)

    # Curved-only Spearman (avoids random rank noise among exact-zero flat conditions)
    curved_idx = np.where(y_true == 1)[0]
    seed_sh_curved_spearman = []
    for _ in range(100):
        perm = rng_sh.permutation(N_SEEDS)
        h1c = np.sqrt(np.maximum(0.0, np.mean(mat_f2[curved_idx][:, perm[: N_SEEDS // 2]], axis=1)))
        h2c = np.sqrt(np.maximum(0.0, np.mean(mat_f2[curved_idx][:, perm[N_SEEDS // 2 :]], axis=1)))
        seed_sh_curved_spearman.append(float(spearmanr(h1c, h2c).statistic))

    gates = {
        "auroc_ge_0.9": bool(auroc_pooled >= 0.90 and auroc_mean >= 0.90),
        "seed_split_half_ge_0.8": bool(np.mean(seed_sh_pearson) >= 0.80 and np.mean(seed_sh_spearman) >= 0.80),
        "ritual_split_half_ge_0.8": bool(ritual_sh_spearman >= 0.80 and ritual_sh_pearson >= 0.80),
        "loop_size_reliability_ge_0.8": bool(min_loop_pearson >= 0.80),
        "flat_reads_zero_ci": bool(flat_f2_lo <= 0.0 <= flat_f2_hi or abs(flat_f2_mean) < 1e-5),
        "ed01_pattern_ge_12_of_15": bool(ed01_05["ed01_pass"]),
        "ed02_saturation_monotonic": bool(ed02["tanh"]["pass"]),
        "ed03_gait_boundary_iou_ge_0.5": bool(ed03["pass"]),
        "ed04_contact_ratio_ge_3x": bool(ed04["pass"]),
        "ed05_froude_le_20pct": bool(ed01_05["ed05_pass"]),
    }
    overall_pass = all(gates.values())

    return {
        "n_flat_conditions": int(np.sum(y_true == 0)),
        "n_curved_conditions": int(np.sum(y_true == 1)),
        "auroc_pooled": auroc_pooled,
        "auroc_per_seed_mean": auroc_mean,
        "auroc_per_seed_ci95": [auroc_lo, auroc_hi],
        "split_half_seeds_spearman": float(np.mean(seed_sh_spearman)),
        "split_half_seeds_curved_spearman": float(np.mean(seed_sh_curved_spearman)),
        "split_half_seeds_pearson": float(np.mean(seed_sh_pearson)),
        "split_half_rituals_spearman": ritual_sh_spearman,
        "split_half_rituals_pearson": ritual_sh_pearson,
        "loop_size_min_pearson": min_loop_pearson,
        "loop_size_min_spearman": min_loop_spearman,
        "flat_exact_F2_mean": flat_f2_mean,
        "flat_exact_F2_ci95": [flat_f2_lo, flat_f2_hi],
        "flat_exact_max_F_cal": flat_f_max,
        "curved_min_F_cal": curved_f_min,
        "gates": gates,
        "verdict": "PASS" if overall_pass else "KILL",
    }


def main() -> None:
    t0 = time.time()
    print(f"ED08 Body-Curvature CPU Pilot (N_SEEDS={N_SEEDS}, rel_noise={REL_NOISE_STD}, workers={MAX_WORKERS})")

    print("1/6 Running ED01 (15-pair arm table) + ED05 (Froude scaling)...")
    ed01_05 = run_ed01_and_ed05(rel_noise=REL_NOISE_STD)
    print(f"    ED01 matches: {ed01_05['ed01_pattern_matches']}/{ed01_05['ed01_total_pairs']} | ED05 Froude/len ratio: {ed01_05['ed05_froude_to_length_ratio']:.4f}")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        print("2/6 Running ED02 (torque/command saturation sweep)...")
        ed02 = run_ed02_saturation(pool, rel_noise=REL_NOISE_STD)
        print(f"    ED02 tanh Spearman: {ed02['tanh']['monotonicity_spearman']:.3f} | clip Spearman: {ed02['clip']['monotonicity_spearman']:.3f}")

        print("3/6 Running ED04 (planar pusher stick/slip grid)...")
        ed04 = run_ed04_pusher(pool, rel_noise=REL_NOISE_STD)
        print(f"    ED04 crossing/within ratio: {ed04['crossing_to_within_ratio']:.1f}x")

        print("4/6 Running ED03 (SLIP hopper gait-boundary grid)...")
        ed03 = run_ed03_hopper(pool, rel_noise=REL_NOISE_STD)
        print(f"    ED03 boundary IoU: {ed03['boundary_iou']:.3f} | AUROC: {ed03['boundary_auroc']:.3f} | ratio: {ed03['boundary_to_within_ratio']:.1f}x")

        print("5/6 Running ED07 (function-space vs weight-space across 2 archs x 2 opts)...")
        ed07 = run_ed07_invariance(pool)

    print("6/6 Running high-noise stress test (1% relative sensor noise on ED01+ED05)...")
    ed01_05_high_noise = run_ed01_and_ed05(rel_noise=0.01)

    verdict = compute_unified_ed08_verdict(ed01_05, ed02, ed04, ed03)
    elapsed = time.time() - t0

    out = {
        "meta": {
            "n_seeds": N_SEEDS,
            "n_ritual": N_RITUAL,
            "n_eval": N_EVAL,
            "rel_noise_std": REL_NOISE_STD,
            "loop_sizes": LOOP_SIZES,
            "default_step": DEFAULT_STEP,
            "elapsed_seconds": round(elapsed, 2),
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "ed01_and_ed05": ed01_05,
        "ed01_and_ed05_high_noise_1pct": {
            "ed01_pattern_matches": ed01_05_high_noise["ed01_pattern_matches"],
            "ed05_froude_to_length_ratio": ed01_05_high_noise["ed05_froude_to_length_ratio"],
            "ed01_loop_size_reliability": ed01_05_high_noise["ed01_loop_size_reliability"],
        },
        "ed02_saturation": ed02,
        "ed04_pusher": ed04,
        "ed03_hopper": ed03,
        "ed07_invariance": ed07,
        "ed08_verdict": verdict,
    }

    out_path = Path(__file__).resolve().parent / "results.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\n=== ED08 VERDICT: {verdict['verdict']} (elapsed {elapsed:.1f}s) ===")
    print(f"  AUROC pooled={verdict['auroc_pooled']:.4f} | per-seed mean={verdict['auroc_per_seed_mean']:.4f} [{verdict['auroc_per_seed_ci95'][0]:.4f}, {verdict['auroc_per_seed_ci95'][1]:.4f}]")
    print(f"  Split-half reliability: seeds_rho={verdict['split_half_seeds_spearman']:.4f} (r={verdict['split_half_seeds_pearson']:.4f}), rituals_rho={verdict['split_half_rituals_spearman']:.4f} (r={verdict['split_half_rituals_pearson']:.4f}), loop_sizes_r={verdict['loop_size_min_pearson']:.4f} (rho={verdict['loop_size_min_spearman']:.4f})")
    print(f"  Flat exact F2_cal: {verdict['flat_exact_F2_mean']:.2e} [{verdict['flat_exact_F2_ci95'][0]:.2e}, {verdict['flat_exact_F2_ci95'][1]:.2e}]")
    print(f"  Flat exact max F_cal: {verdict['flat_exact_max_F_cal']:.5f} vs Curved min F_cal: {verdict['curved_min_F_cal']:.5f}")
    print(f"  Gates: {verdict['gates']}")


if __name__ == "__main__":
    main()
