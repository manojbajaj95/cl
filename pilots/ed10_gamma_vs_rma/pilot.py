"""ED10 Body-Connection (Gamma) vs Fairest RMA CPU Pilot on MuJoCo 3.x Bodies.

Tests the pre-registered ED10 kill/promotion bar (tree/embodied-learners-4.md, PR #398;
reviewer score-4 bar in reviews/flood-triage.md row 561):
  - Learn old skills S1..S4 across bodies A, B, C, D (Phase 1).
  - Learn new skill S5 ONLY on body B (Phase 2).
  - Evaluate S5 zero-shot on held-out bodies A, C, D and S1..S4 retention across A, B, C, D,
    using MuJoCo 2-link vertical-plane arms with >= 1% relative Gaussian sensor noise.
  - Arms:
      * Gamma: state-dependent function-space connection fitted purely from noisy rituals.
      * EB12: state-independent affine action conjugator fitted from noisy rituals.
      * RMA_replay: FiLM-conditioned RMA (ritual SVD body latent z_b) fine-tuned on S5@B + S1..S4 replay.
      * RMA_frozen_body: FiLM-conditioned RMA with body modulator frozen from Phase 1, fine-tuned on S5@B + S1..S4 replay.
      * NoTransport: S5@B deployed directly on A, C, D.
  - Pass bar:
      * Curved family: Gamma beats the stronger RMA arm on S5@{A,C,D} by > 2 SE.
      * Flat family: Gamma does not lose to the stronger RMA arm on S5@{A,C,D}.
      * Old-skill retention: S1..S4 retained across A, B, C, D after learning S5.

Run:
    python3 -u pilots/ed10_gamma_vs_rma/pilot.py
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

import mujoco
import numpy as np

from arms import (
    RMAFiLMPolicy,
    SkillPolicy,
    StateBasis,
    extract_rma_body_latents,
    fit_eb12_conjugator,
    fit_ritual_dynamics,
    gamma_transport_action,
    make_rma_input,
)
from mujoco_arm import (
    MuJoCoArm,
    collect_ritual_data,
    collect_skill_data,
    evaluate_policy_on_skill,
    expert_desired_accel,
    get_body_families,
    get_skills,
)


N_SEEDS = 16
N_SEEDS_STRESS = 8
N_RITUAL = 1200
N_SKILL_EPS = 8
HORIZON = 80
N_EVAL_EPS = 6
PRIMARY_NOISE = 0.01   # 1% relative sensor noise (reviewer requirement: >= 1%)
STRESS_NOISE = 0.02    # 2% relative sensor noise stress test
MAX_WORKERS = min(8, os.cpu_count() or 4)


def paired_stats(a: np.ndarray, b: np.ndarray, n_boot: int = 4000, seed: int = 12345) -> dict[str, float]:
    """Compute paired difference (a - b), SE, gap_in_SE, and 95% bootstrap CI."""
    diff = np.asarray(a, dtype=np.float64) - np.asarray(b, dtype=np.float64)
    mean = float(np.mean(diff))
    se = float(np.std(diff, ddof=1) / np.sqrt(len(diff))) if len(diff) > 1 else 0.0
    gap_se = mean / (se + 1e-12)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(diff), size=(n_boot, len(diff)))
    boots = np.mean(diff[idx], axis=1)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {
        "mean_diff": mean,
        "se": se,
        "gap_in_se": float(gap_se),
        "ci95": [float(lo), float(hi)],
    }


def mean_se(x: np.ndarray) -> dict[str, float]:
    arr = np.asarray(x, dtype=np.float64)
    return {
        "mean": float(np.mean(arr)),
        "se": float(np.std(arr, ddof=1) / np.sqrt(len(arr))) if len(arr) > 1 else 0.0,
    }


def _run_one_seed(args: tuple[str, int, float]) -> dict[str, Any]:
    fam_name, seed, sensor_noise = args
    rng = np.random.default_rng(50000 + (0 if fam_name == "flat" else 10000) + int(sensor_noise * 1000) * 100 + seed)
    specs = get_body_families()[fam_name]
    arms_env = {b: MuJoCoArm(sp) for b, sp in specs.items()}
    skills = get_skills()
    old_skills = skills[:4]
    s5 = skills[4]
    bodies = ["A", "B", "C", "D"]
    held_out = ["A", "C", "D"]

    # 1. Collect identical noisy ritual data on all 4 bodies
    rituals = {
        b: collect_ritual_data(arms_env[b], N_RITUAL, sensor_noise, rng)
        for b in bodies
    }

    # Fit shared ritual dynamics models (used by Gamma, EB12, and RMA latent encoder)
    basis = StateBasis(n_rff=48, seed=seed)
    dyn = {b: fit_ritual_dynamics(rituals[b], basis) for b in bodies}

    # EB12 state-independent affine conjugators relative to body B
    eb12_from_B = {b: fit_eb12_conjugator(dyn["B"], dyn[b], rituals["B"]) for b in bodies}

    # RMA ritual-derived body latents z_b (from SVD of noisy ritual acceleration responses)
    z_by_body = extract_rma_body_latents(dyn, n_probe=64, latent_dim=6, seed=seed)

    # 2. Collect Phase 1 data (S1..S4 on A, B, C, D) and Phase 2 data (S5 ONLY on B)
    phase1_data: dict[tuple[str, int], dict[str, np.ndarray]] = {}
    for b in bodies:
        for sk in old_skills:
            phase1_data[(b, sk.skill_id)] = collect_skill_data(
                arms_env[b], sk, N_SKILL_EPS, HORIZON, sensor_noise, rng,
            )
    s5_B_data = collect_skill_data(arms_env["B"], s5, N_SKILL_EPS, HORIZON, sensor_noise, rng)

    # 3. Train Gamma & EB12 & NoTransport skill policies
    # Old skills S1..S4: trained per-body (or canonical via Gamma/EB12) — untouched when S5 is learned!
    old_pol_gamma: dict[int, SkillPolicy] = {}
    old_pol_eb12: dict[int, SkillPolicy] = {}
    for sk in old_skills:
        # Train canonical skill policy on body B using all bodies' data transported to B via Gamma / EB12
        s_all = np.concatenate([phase1_data[(b, sk.skill_id)]["states"] for b in bodies], axis=0)
        t_all = np.concatenate([phase1_data[(b, sk.skill_id)]["times"] for b in bodies], axis=0)
        u_gamma_B = np.concatenate([
            gamma_transport_action(
                dyn[b], dyn["B"],
                phase1_data[(b, sk.skill_id)]["states"][:, :2],
                phase1_data[(b, sk.skill_id)]["states"][:, 2:4],
                phase1_data[(b, sk.skill_id)]["u"],
            )
            for b in bodies
        ], axis=0)
        pg = SkillPolicy(seed=seed * 10 + sk.skill_id)
        pg.fit(s_all, t_all, u_gamma_B, ridge=1e-2)
        old_pol_gamma[sk.skill_id] = pg

        u_eb12_B = np.concatenate([
            fit_eb12_conjugator(dyn[b], dyn["B"], rituals[b]).map_action(phase1_data[(b, sk.skill_id)]["u"])
            for b in bodies
        ], axis=0)
        pe = SkillPolicy(seed=seed * 10 + sk.skill_id)
        pe.fit(s_all, t_all, u_eb12_B, ridge=1e-2)
        old_pol_eb12[sk.skill_id] = pe

    # New skill S5 trained ONLY on body B
    s5_pol_B = SkillPolicy(seed=seed * 10 + 99)
    s5_pol_B.fit(s5_B_data["states"], s5_B_data["times"], s5_B_data["u"], ridge=1e-2)

    # 4. Train Fairest RMA (Phase 1: S1..S4 across A..D; Phase 2: S5@B + S1..S4 replay)
    x1_list, z1_list, y1_list = [], [], []
    for b in bodies:
        for sk in old_skills:
            d = phase1_data[(b, sk.skill_id)]
            x1_list.append(make_rma_input(d["states"], d["times"], sk.skill_id))
            z1_list.append(np.repeat(z_by_body[b][None, :], len(d["states"]), axis=0))
            y1_list.append(d["u"])
    X1 = np.concatenate(x1_list, axis=0)
    Z1 = np.concatenate(z1_list, axis=0)
    Y1 = np.concatenate(y1_list, axis=0)

    rma_base = RMAFiLMPolicy(in_dim=20, z_dim=6, hidden=64, out_dim=2, seed=seed)
    rma_base.fit(X1, Z1, Y1, l2_reg=1e-4, maxiter=350, include_body=True, refit_norm=True)

    # Phase 2 data: S5@B (upweighted 4x so S5 gets equal weight to the 4 old skills) + S1..S4 replay across A..D
    X5 = make_rma_input(s5_B_data["states"], s5_B_data["times"], s5.skill_id)
    Z5 = np.repeat(z_by_body["B"][None, :], len(s5_B_data["states"]), axis=0)
    Y5 = s5_B_data["u"]

    X_p2 = np.concatenate([X1, X5], axis=0)
    Z_p2 = np.concatenate([Z1, Z5], axis=0)
    Y_p2 = np.concatenate([Y1, Y5], axis=0)
    W_p2 = np.concatenate([np.ones(len(X1)), np.full(len(X5), 4.0)])

    rma_replay = rma_base.clone()
    rma_replay.fit(X_p2, Z_p2, Y_p2, sample_weights=W_p2, l2_reg=1e-4, maxiter=350, include_body=True, refit_norm=False)

    rma_frozen = rma_base.clone()
    rma_frozen.fit(X_p2, Z_p2, Y_p2, sample_weights=W_p2, l2_reg=1e-4, maxiter=350, include_body=False, refit_norm=False)

    # 5. Evaluate all arms on S5 (A, C, D and B) and old skills S1..S4 (all bodies)
    def eval_s5_for_arm(arm_name: str, body: str) -> dict[str, float]:
        if arm_name == "Gamma":
            pol = lambda s, t: gamma_transport_action(dyn["B"], dyn[body], s[:2], s[2:4], s5_pol_B.predict(s, t))
        elif arm_name == "EB12":
            pol = lambda s, t: eb12_from_B[body].map_action(s5_pol_B.predict(s, t))
        elif arm_name == "RMA_replay":
            pol = lambda s, t: rma_replay.predict(make_rma_input(s, np.array([t]), s5.skill_id)[0], z_by_body[body])
        elif arm_name == "RMA_frozen_body":
            pol = lambda s, t: rma_frozen.predict(make_rma_input(s, np.array([t]), s5.skill_id)[0], z_by_body[body])
        elif arm_name == "NoTransport":
            pol = lambda s, t: s5_pol_B.predict(s, t)
        elif arm_name == "Expert":
            pol = lambda s, t: arms_env[body].inverse_ctrl(s[:2], s[2:4], expert_desired_accel(s5, s[:2], s[2:4], t))
        else:
            raise ValueError(arm_name)
        return evaluate_policy_on_skill(
            arms_env[body], s5, pol, n_episodes=N_EVAL_EPS, horizon=HORIZON,
            sensor_noise_std=sensor_noise, seed=9000 + seed * 17 + bodies.index(body),
        )

    arm_names = ["Gamma", "EB12", "RMA_replay", "RMA_frozen_body", "NoTransport", "Expert"]
    s5_res: dict[str, dict[str, dict[str, float]]] = {a: {} for a in arm_names}
    for a in arm_names:
        for b in bodies:
            s5_res[a][b] = eval_s5_for_arm(a, b)

    # Old-skill retention (S1..S4 across A, B, C, D) after learning S5
    ret_res: dict[str, float] = {}
    for a in ["Gamma", "EB12", "RMA_replay", "RMA_frozen_body"]:
        rets = []
        for b in bodies:
            for sk in old_skills:
                if a == "Gamma":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: gamma_transport_action(
                        dyn["B"], dyn[b_], s[:2], s[2:4], old_pol_gamma[sk_id].predict(s, t)
                    )
                elif a == "EB12":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: eb12_from_B[b_].map_action(
                        old_pol_eb12[sk_id].predict(s, t)
                    )
                elif a == "RMA_replay":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: rma_replay.predict(
                        make_rma_input(s, np.array([t]), sk_id)[0], z_by_body[b_]
                    )
                else:
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: rma_frozen.predict(
                        make_rma_input(s, np.array([t]), sk_id)[0], z_by_body[b_]
                    )
                ev = evaluate_policy_on_skill(
                    arms_env[b], sk, pol, n_episodes=3, horizon=HORIZON,
                    sensor_noise_std=sensor_noise, seed=7000 + seed * 31 + sk.skill_id * 5 + bodies.index(b),
                )
                rets.append(ev["return"])
        ret_res[a] = float(np.mean(rets))

    return {
        "family": fam_name,
        "seed": seed,
        "sensor_noise": sensor_noise,
        "s5_heldout_return": {a: float(np.mean([s5_res[a][b]["return"] for b in held_out])) for a in arm_names},
        "s5_heldout_rmse": {a: float(np.mean([s5_res[a][b]["rmse"] for b in held_out])) for a in arm_names},
        "s5_trainB_return": {a: float(s5_res[a]["B"]["return"]) for a in arm_names},
        "s5_per_body_return": {a: {b: s5_res[a][b]["return"] for b in bodies} for a in arm_names},
        "retention_s1_s4_return": ret_res,
    }


def summarize_family(rows: list[dict[str, Any]]) -> dict[str, Any]:
    arm_names = ["Gamma", "EB12", "RMA_replay", "RMA_frozen_body", "NoTransport", "Expert"]
    heldout_ret = {a: np.array([r["s5_heldout_return"][a] for r in rows]) for a in arm_names}
    heldout_rmse = {a: np.array([r["s5_heldout_rmse"][a] for r in rows]) for a in arm_names}
    trainB_ret = {a: np.array([r["s5_trainB_return"][a] for r in rows]) for a in arm_names}
    retention = {a: np.array([r["retention_s1_s4_return"][a] for r in rows]) for a in ["Gamma", "EB12", "RMA_replay", "RMA_frozen_body"]}

    # Strongest RMA arm on held-out S5@{A, C, D}
    best_rma_name = (
        "RMA_replay"
        if float(np.mean(heldout_ret["RMA_replay"])) >= float(np.mean(heldout_ret["RMA_frozen_body"]))
        else "RMA_frozen_body"
    )

    return {
        "n_seeds": len(rows),
        "best_rma_arm": best_rma_name,
        "s5_heldout_return": {a: mean_se(heldout_ret[a]) for a in arm_names},
        "s5_heldout_rmse": {a: mean_se(heldout_rmse[a]) for a in arm_names},
        "s5_trainB_return": {a: mean_se(trainB_ret[a]) for a in arm_names},
        "retention_s1_s4_return": {a: mean_se(retention[a]) for a in retention},
        "paired_gamma_minus_best_rma_return": paired_stats(heldout_ret["Gamma"], heldout_ret[best_rma_name]),
        "paired_gamma_minus_rma_replay_return": paired_stats(heldout_ret["Gamma"], heldout_ret["RMA_replay"]),
        "paired_gamma_minus_rma_frozen_return": paired_stats(heldout_ret["Gamma"], heldout_ret["RMA_frozen_body"]),
        "paired_gamma_minus_eb12_return": paired_stats(heldout_ret["Gamma"], heldout_ret["EB12"]),
        "paired_gamma_minus_best_rma_neg_rmse": paired_stats(-heldout_rmse["Gamma"], -heldout_rmse[best_rma_name]),
        "per_seed_s5_heldout_return": {a: heldout_ret[a].tolist() for a in arm_names},
    }


def main() -> None:
    t0 = time.time()
    print(f"ED10 Gamma vs Fairest RMA CPU Pilot (MuJoCo {mujoco.__version__}, N_SEEDS={N_SEEDS}, noise={PRIMARY_NOISE:.0%}, workers={MAX_WORKERS})")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        print("1/3 Running FLAT family (1% sensor noise, 16 seeds)...")
        flat_rows = list(pool.map(_run_one_seed, [("flat", s, PRIMARY_NOISE) for s in range(N_SEEDS)]))
        flat_sum = summarize_family(flat_rows)
        print(
            f"    FLAT S5@{ '{A,C,D}' }: Gamma={flat_sum['s5_heldout_return']['Gamma']['mean']:.4f} "
            f"| EB12={flat_sum['s5_heldout_return']['EB12']['mean']:.4f} "
            f"| best RMA ({flat_sum['best_rma_arm']})={flat_sum['s5_heldout_return'][flat_sum['best_rma_arm']]['mean']:.4f} "
            f"| gap={flat_sum['paired_gamma_minus_best_rma_return']['gap_in_se']:+.2f} SE"
        )

        print("2/3 Running CURVED family (1% sensor noise, 16 seeds)...")
        curved_rows = list(pool.map(_run_one_seed, [("curved", s, PRIMARY_NOISE) for s in range(N_SEEDS)]))
        curved_sum = summarize_family(curved_rows)
        print(
            f"    CURVED S5@{ '{A,C,D}' }: Gamma={curved_sum['s5_heldout_return']['Gamma']['mean']:.4f} "
            f"| EB12={curved_sum['s5_heldout_return']['EB12']['mean']:.4f} "
            f"| best RMA ({curved_sum['best_rma_arm']})={curved_sum['s5_heldout_return'][curved_sum['best_rma_arm']]['mean']:.4f} "
            f"| gap={curved_sum['paired_gamma_minus_best_rma_return']['gap_in_se']:+.2f} SE"
        )

        print("3/3 Running 2% sensor-noise stress test (8 seeds, curved + flat)...")
        stress_flat = summarize_family(list(pool.map(_run_one_seed, [("flat", s, STRESS_NOISE) for s in range(N_SEEDS_STRESS)])))
        stress_curved = summarize_family(list(pool.map(_run_one_seed, [("curved", s, STRESS_NOISE) for s in range(N_SEEDS_STRESS)])))
        print(
            f"    2% NOISE CURVED: Gamma={stress_curved['s5_heldout_return']['Gamma']['mean']:.4f} "
            f"| best RMA={stress_curved['s5_heldout_return'][stress_curved['best_rma_arm']]['mean']:.4f} "
            f"| gap={stress_curved['paired_gamma_minus_best_rma_return']['gap_in_se']:+.2f} SE"
        )

    # Pre-registered ED10 gates:
    # 1. Curved family: Gamma beats best RMA on S5@{A,C,D} by > 2 SE (return AND neg-RMSE)
    # 2. Curved family: Gamma beats EB12 flat conjugator by > 2 SE
    # 3. Flat family: Gamma does not lose to best RMA (gap >= -2 SE; ideally >= 0)
    # 4. Old-skill retention: Gamma retains S1..S4 >= 0.85 across A..D in both families
    gates = {
        "curved_gamma_beats_best_rma_gt_2se": bool(curved_sum["paired_gamma_minus_best_rma_return"]["gap_in_se"] > 2.0),
        "curved_gamma_beats_best_rma_rmse_gt_2se": bool(curved_sum["paired_gamma_minus_best_rma_neg_rmse"]["gap_in_se"] > 2.0),
        "curved_gamma_beats_eb12_gt_2se": bool(curved_sum["paired_gamma_minus_eb12_return"]["gap_in_se"] > 2.0),
        "flat_gamma_does_not_lose_to_best_rma": bool(flat_sum["paired_gamma_minus_best_rma_return"]["gap_in_se"] >= -2.0 and flat_sum["s5_heldout_return"]["Gamma"]["mean"] >= flat_sum["s5_heldout_return"][flat_sum["best_rma_arm"]]["mean"] - 0.02),
        "old_skill_retention_ge_0.85": bool(
            flat_sum["retention_s1_s4_return"]["Gamma"]["mean"] >= 0.85
            and curved_sum["retention_s1_s4_return"]["Gamma"]["mean"] >= 0.85
        ),
        "stress_2pct_curved_gamma_beats_rma_gt_2se": bool(stress_curved["paired_gamma_minus_best_rma_return"]["gap_in_se"] > 2.0),
    }
    verdict = "PASS" if all(gates.values()) else "KILL"
    elapsed = time.time() - t0

    out = {
        "meta": {
            "mujoco_version": mujoco.__version__,
            "n_seeds": N_SEEDS,
            "n_seeds_stress": N_SEEDS_STRESS,
            "n_ritual": N_RITUAL,
            "n_skill_eps": N_SKILL_EPS,
            "horizon": HORIZON,
            "primary_sensor_noise": PRIMARY_NOISE,
            "stress_sensor_noise": STRESS_NOISE,
            "elapsed_sec": elapsed,
            "platform": platform.platform(),
        },
        "flat_1pct": flat_sum,
        "curved_1pct": curved_sum,
        "flat_2pct_stress": stress_flat,
        "curved_2pct_stress": stress_curved,
        "gates": gates,
        "verdict": verdict,
    }

    out_path = Path(__file__).resolve().parent / "results.json"
    out_path.write_text(json.dumps(out, indent=2))

    print(f"\n=== ED10 VERDICT: {verdict} (elapsed {elapsed:.1f}s) ===")
    print(f"  Curved 1% gap (Gamma - best RMA): {curved_sum['paired_gamma_minus_best_rma_return']['mean_diff']:+.4f} +/- {curved_sum['paired_gamma_minus_best_rma_return']['se']:.4f} ({curved_sum['paired_gamma_minus_best_rma_return']['gap_in_se']:+.2f} SE)")
    print(f"  Flat   1% gap (Gamma - best RMA): {flat_sum['paired_gamma_minus_best_rma_return']['mean_diff']:+.4f} +/- {flat_sum['paired_gamma_minus_best_rma_return']['se']:.4f} ({flat_sum['paired_gamma_minus_best_rma_return']['gap_in_se']:+.2f} SE)")
    print(f"  Retention S1..S4 (Gamma): flat={flat_sum['retention_s1_s4_return']['Gamma']['mean']:.4f}, curved={curved_sum['retention_s1_s4_return']['Gamma']['mean']:.4f}")
    print(f"  Gates: {gates}")


if __name__ == "__main__":
    main()
