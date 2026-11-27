"""ED10b CPU Pilot: Curvature-Gated Gamma (Generic RFF) vs GAT-MLP, Capacity-Matched RMA, Always-Gamma, and Always-EB12.

Addresses every reviewer critique of ED10 (reviews/flood-triage.md row 572):
  1. Same MuJoCo flat and curved families PLUS a MuJoCo unilateral-contact body family
     (condim=3 normal + Coulomb friction wall) PLUS a mixed flat+curved family, at 1% sensor noise, 16 seeds.
  2. GAT-MLP control: Grounded Action Transformation (Hanna & Stone 2017 / Christiano et al. 1610.03518)
     with generic 2-layer tanh forward & inverse MLPs fitted from the exact same noisy rituals.
  3. Capacity-matched RMA control: uses the EXACT SAME per-skill 160-dim RFF SkillPolicy class
     and basis features as Gamma (guaranteeing S5@B >= 0.95 — zero policy-capacity confound),
     with both frozen-body and replay Phase-2 modes.
  4. Generic-RFF Gamma: replaces ED10's hand-engineered rigid-body trig/quadratic basis with a
     pure generic Random Fourier Feature basis.
  5. Curvature-gated transport (Gamma_gated): uses ED08's split-half cross-fitted curvature
     F2_cal from the same noisy rituals to route flat pairs (F2_cal <= tau) to EB12 and
     curved/contact pairs (F2_cal > tau) to Gamma_RFF.

Promotion bar (reviews/flood-triage.md row 572):
  - Curved 1% noise: Gamma_gated beats GAT_MLP and best CapacityMatchedRMA by > 2 SE.
  - Contact 1% noise: Gamma_gated beats GAT_MLP and best CapacityMatchedRMA by > 2 SE.
  - Mixed 1% noise: Gamma_gated beats BOTH always-Gamma AND always-EB12 (by > 2 SE).
  - Old-skill S1..S4 retention >= 0.85 across all families.

Run:
    python3 -u pilots/ed10b_curvature_gated_gamma/pilot.py
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
    CapacityMatchedRMA,
    GenericRFFBasis,
    SkillPolicy,
    estimate_pair_curvature_ed08,
    extract_rma_body_latents,
    fit_eb12_conjugator,
    fit_gat_mlp_body,
    fit_rff_dynamics,
    gamma_transport_action,
    gat_mlp_transport_action,
)
from mujoco_bodies import (
    MuJoCoArm,
    collect_ritual_data,
    collect_skill_data,
    evaluate_policy_on_skill,
    expert_desired_accel,
    get_body_families,
    get_skills,
)


N_SEEDS = 16
N_RITUAL = 1200
N_SKILL_EPS = 8
HORIZON = 80
N_EVAL_EPS = 6
SENSOR_NOISE = 0.01  # 1% relative Gaussian sensor noise
CURVATURE_GATE_TAU = 0.015  # state-dependent action-energy fraction threshold (>1.5% -> curved)
MAX_WORKERS = min(8, os.cpu_count() or 4)


def paired_stats(a: np.ndarray, b: np.ndarray, n_boot: int = 4000, seed: int = 12345) -> dict[str, float]:
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


def _run_one_seed(args: tuple[str, int]) -> dict[str, Any]:
    fam_name, seed = args
    fam_idx = {"flat": 0, "curved": 1, "contact": 2, "mixed": 3}[fam_name]
    rng = np.random.default_rng(80000 + fam_idx * 10000 + seed)

    specs = get_body_families()[fam_name]
    bodies = list(specs.keys())
    held_out = [b for b in bodies if b != "B"]
    arms_env = {b: MuJoCoArm(sp) for b, sp in specs.items()}
    skills = get_skills(contact_family=(fam_name == "contact"))
    old_skills = skills[:4]
    s5 = skills[4]

    # 1. Identical noisy ritual dataset per body (1% sensor noise)
    rituals = {b: collect_ritual_data(arms_env[b], N_RITUAL, SENSOR_NOISE, rng) for b in bodies}

    # 2. Fit dynamics / transport models from the exact same rituals
    basis = GenericRFFBasis(seed=seed)
    dyn = {b: fit_rff_dynamics(rituals[b], basis) for b in bodies}
    eb12_from_B = {b: fit_eb12_conjugator(dyn["B"], dyn[b], rituals["B"]) for b in bodies}
    gat_mlp = {b: fit_gat_mlp_body(rituals[b], hidden=48, maxiter=220, seed=seed * 13 + i) for i, b in enumerate(bodies)}

    # ED08 split-ritual curvature gate for each (B -> b)
    curv_stats: dict[str, dict[str, float]] = {}
    gate_use_gamma: dict[str, bool] = {}
    for b in bodies:
        if b == "B":
            curv_stats[b] = {"f2_cal": 0.0, "se_f2": 0.0, "z_score": 0.0}
            gate_use_gamma[b] = False
        else:
            cs = estimate_pair_curvature_ed08(rituals["B"], rituals[b], basis, n_probe=256, seed=seed * 7 + bodies.index(b))
            curv_stats[b] = cs
            gate_use_gamma[b] = bool(cs["f2_cal"] > CURVATURE_GATE_TAU and cs["z_score"] > 2.5)

    # Ritual-derived body latents for capacity-matched RMA
    z_by_body = extract_rma_body_latents(dyn, n_probe=64, latent_dim=6, seed=seed)

    # 3. Collect Phase 1 (S1..S4 across all bodies) and Phase 2 (S5 ONLY on B)
    phase1_data: dict[tuple[str, int], dict[str, np.ndarray]] = {}
    for b in bodies:
        for sk in old_skills:
            phase1_data[(b, sk.skill_id)] = collect_skill_data(
                arms_env[b], sk, N_SKILL_EPS, HORIZON, SENSOR_NOISE, rng,
            )
    s5_B_data = collect_skill_data(arms_env["B"], s5, N_SKILL_EPS, HORIZON, SENSOR_NOISE, rng)

    # 4. Fit canonical S5 policy on B (shared across Gamma_RFF, Gamma_gated, EB12, GAT_MLP, NoTransport)
    s5_pol_B = SkillPolicy(seed=seed * 10 + 99)
    s5_pol_B.fit(s5_B_data["states"], s5_B_data["times"], s5_B_data["u"], ridge=1e-2)

    # Fit canonical old-skill policies S1..S4 for Gamma_RFF / Gamma_gated / EB12 / GAT_MLP
    old_pol_gamma: dict[int, SkillPolicy] = {}
    old_pol_gated: dict[int, SkillPolicy] = {}
    old_pol_eb12: dict[int, SkillPolicy] = {}
    old_pol_gat: dict[int, SkillPolicy] = {}
    for sk in old_skills:
        s_all = np.concatenate([phase1_data[(b, sk.skill_id)]["states"] for b in bodies], axis=0)
        t_all = np.concatenate([phase1_data[(b, sk.skill_id)]["times"] for b in bodies], axis=0)

        # Transport each body's S1..S4 demos to canonical body B
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

        u_gated_B = np.concatenate([
            (
                gamma_transport_action(
                    dyn[b], dyn["B"],
                    phase1_data[(b, sk.skill_id)]["states"][:, :2],
                    phase1_data[(b, sk.skill_id)]["states"][:, 2:4],
                    phase1_data[(b, sk.skill_id)]["u"],
                )
                if gate_use_gamma[b]
                else fit_eb12_conjugator(dyn[b], dyn["B"], rituals[b]).map_action(phase1_data[(b, sk.skill_id)]["u"])
            )
            for b in bodies
        ], axis=0)
        pgt = SkillPolicy(seed=seed * 10 + sk.skill_id)
        pgt.fit(s_all, t_all, u_gated_B, ridge=1e-2)
        old_pol_gated[sk.skill_id] = pgt

        u_gat_B = np.concatenate([
            gat_mlp_transport_action(
                gat_mlp[b], gat_mlp["B"],
                phase1_data[(b, sk.skill_id)]["states"][:, :2],
                phase1_data[(b, sk.skill_id)]["states"][:, 2:4],
                phase1_data[(b, sk.skill_id)]["u"],
            )
            for b in bodies
        ], axis=0)
        pgat = SkillPolicy(seed=seed * 10 + sk.skill_id)
        pgat.fit(s_all, t_all, u_gat_B, ridge=1e-2)
        old_pol_gat[sk.skill_id] = pgat

    # 5. Fit Capacity-Matched RMA (exact same per-skill 160-dim RFF SkillPolicy class!)
    rma_base = CapacityMatchedRMA(z_dim=6, hidden_res=32, seed=seed)
    rma_base.fit_phase1(phase1_data, z_by_body, bodies, [sk.skill_id for sk in old_skills], n_alt=3)

    rma_frozen = rma_base.clone()
    rma_frozen.fit_s5_frozen_body(s5_B_data, z_by_body["B"], skill_id=s5.skill_id)

    rma_replay = rma_base.clone()
    rma_replay.fit_s5_replay(phase1_data, s5_B_data, z_by_body, bodies, [sk.skill_id for sk in old_skills], skill_id=s5.skill_id)

    # 6. Evaluate all arms on S5 (all bodies) and old skills S1..S4 (all bodies)
    arm_names = [
        "Gamma_gated",
        "Gamma_RFF",
        "EB12",
        "GAT_MLP",
        "RMA_matched_frozen",
        "RMA_matched_replay",
        "NoTransport",
        "Expert",
    ]

    def make_s5_policy(arm_name: str, body: str):
        if arm_name == "Gamma_gated":
            if gate_use_gamma[body]:
                return lambda s, t: gamma_transport_action(dyn["B"], dyn[body], s[:2], s[2:4], s5_pol_B.predict(s, t))
            return lambda s, t: eb12_from_B[body].map_action(s5_pol_B.predict(s, t))
        if arm_name == "Gamma_RFF":
            return lambda s, t: gamma_transport_action(dyn["B"], dyn[body], s[:2], s[2:4], s5_pol_B.predict(s, t))
        if arm_name == "EB12":
            return lambda s, t: eb12_from_B[body].map_action(s5_pol_B.predict(s, t))
        if arm_name == "GAT_MLP":
            return lambda s, t: gat_mlp_transport_action(gat_mlp["B"], gat_mlp[body], s[:2], s[2:4], s5_pol_B.predict(s, t))
        if arm_name == "RMA_matched_frozen":
            return lambda s, t: rma_frozen.predict(s, t, s5.skill_id, z_by_body[body])
        if arm_name == "RMA_matched_replay":
            return lambda s, t: rma_replay.predict(s, t, s5.skill_id, z_by_body[body])
        if arm_name == "NoTransport":
            return lambda s, t: s5_pol_B.predict(s, t)
        if arm_name == "Expert":
            return lambda s, t: arms_env[body].inverse_ctrl(s[:2], s[2:4], expert_desired_accel(s5, s[:2], s[2:4], t))
        raise ValueError(arm_name)

    s5_res: dict[str, dict[str, dict[str, float]]] = {a: {} for a in arm_names}
    for a in arm_names:
        for b in bodies:
            s5_res[a][b] = evaluate_policy_on_skill(
                arms_env[b], s5, make_s5_policy(a, b),
                n_episodes=N_EVAL_EPS, horizon=HORIZON,
                sensor_noise_std=SENSOR_NOISE, seed=9000 + seed * 17 + bodies.index(b),
            )

    ret_arms = ["Gamma_gated", "Gamma_RFF", "EB12", "GAT_MLP", "RMA_matched_frozen", "RMA_matched_replay"]
    ret_res: dict[str, float] = {}
    for a in ret_arms:
        rets = []
        for b in bodies:
            for sk in old_skills:
                if a == "Gamma_gated":
                    pol = (
                        (lambda s, t, sk_id=sk.skill_id, b_=b: gamma_transport_action(dyn["B"], dyn[b_], s[:2], s[2:4], old_pol_gated[sk_id].predict(s, t)))
                        if gate_use_gamma[b]
                        else (lambda s, t, sk_id=sk.skill_id, b_=b: eb12_from_B[b_].map_action(old_pol_gated[sk_id].predict(s, t)))
                    )
                elif a == "Gamma_RFF":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: gamma_transport_action(dyn["B"], dyn[b_], s[:2], s[2:4], old_pol_gamma[sk_id].predict(s, t))
                elif a == "EB12":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: eb12_from_B[b_].map_action(old_pol_eb12[sk_id].predict(s, t))
                elif a == "GAT_MLP":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: gat_mlp_transport_action(gat_mlp["B"], gat_mlp[b_], s[:2], s[2:4], old_pol_gat[sk_id].predict(s, t))
                elif a == "RMA_matched_frozen":
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: rma_frozen.predict(s, t, sk_id, z_by_body[b_])
                else:
                    pol = lambda s, t, sk_id=sk.skill_id, b_=b: rma_replay.predict(s, t, sk_id, z_by_body[b_])
                ev = evaluate_policy_on_skill(
                    arms_env[b], sk, pol, n_episodes=3, horizon=HORIZON,
                    sensor_noise_std=SENSOR_NOISE, seed=7000 + seed * 31 + sk.skill_id * 5 + bodies.index(b),
                )
                rets.append(ev["return"])
        ret_res[a] = float(np.mean(rets))

    return {
        "family": fam_name,
        "seed": seed,
        "gate_use_gamma": gate_use_gamma,
        "curvature_f2": {b: curv_stats[b]["f2_cal"] for b in held_out},
        "s5_heldout_return": {a: float(np.mean([s5_res[a][b]["return"] for b in held_out])) for a in arm_names},
        "s5_heldout_rmse": {a: float(np.mean([s5_res[a][b]["rmse"] for b in held_out])) for a in arm_names},
        "s5_trainB_return": {a: float(s5_res[a]["B"]["return"]) for a in arm_names},
        "s5_per_body_return": {a: {b: s5_res[a][b]["return"] for b in bodies} for a in arm_names},
        "s5_contact_frac_expert": {b: s5_res["Expert"][b]["contact_frac"] for b in bodies},
        "retention_s1_s4_return": ret_res,
    }


def summarize_family(rows: list[dict[str, Any]]) -> dict[str, Any]:
    arm_names = [
        "Gamma_gated", "Gamma_RFF", "EB12", "GAT_MLP",
        "RMA_matched_frozen", "RMA_matched_replay", "NoTransport", "Expert",
    ]
    ret_arms = ["Gamma_gated", "Gamma_RFF", "EB12", "GAT_MLP", "RMA_matched_frozen", "RMA_matched_replay"]
    h_ret = {a: np.array([r["s5_heldout_return"][a] for r in rows]) for a in arm_names}
    h_rmse = {a: np.array([r["s5_heldout_rmse"][a] for r in rows]) for a in arm_names}
    tB_ret = {a: np.array([r["s5_trainB_return"][a] for r in rows]) for a in arm_names}
    ret = {a: np.array([r["retention_s1_s4_return"][a] for r in rows]) for a in ret_arms}

    best_rma = (
        "RMA_matched_frozen"
        if float(np.mean(h_ret["RMA_matched_frozen"])) >= float(np.mean(h_ret["RMA_matched_replay"]))
        else "RMA_matched_replay"
    )
    held_out = list(rows[0]["curvature_f2"].keys())
    gate_rate = {b: float(np.mean([1.0 if r["gate_use_gamma"][b] else 0.0 for r in rows])) for b in held_out}
    mean_f2 = {b: float(np.mean([r["curvature_f2"][b] for r in rows])) for b in held_out}

    return {
        "n_seeds": len(rows),
        "best_rma_arm": best_rma,
        "gate_use_gamma_rate": gate_rate,
        "mean_curvature_f2": mean_f2,
        "s5_heldout_return": {a: mean_se(h_ret[a]) for a in arm_names},
        "s5_heldout_rmse": {a: mean_se(h_rmse[a]) for a in arm_names},
        "s5_trainB_return": {a: mean_se(tB_ret[a]) for a in arm_names},
        "retention_s1_s4_return": {a: mean_se(ret[a]) for a in ret_arms},
        "paired_gated_minus_gat_mlp": paired_stats(h_ret["Gamma_gated"], h_ret["GAT_MLP"]),
        "paired_gated_minus_best_rma": paired_stats(h_ret["Gamma_gated"], h_ret[best_rma]),
        "paired_gated_minus_always_gamma": paired_stats(h_ret["Gamma_gated"], h_ret["Gamma_RFF"]),
        "paired_gated_minus_always_eb12": paired_stats(h_ret["Gamma_gated"], h_ret["EB12"]),
        "paired_gamma_rff_minus_gat_mlp": paired_stats(h_ret["Gamma_RFF"], h_ret["GAT_MLP"]),
        "paired_gamma_rff_minus_best_rma": paired_stats(h_ret["Gamma_RFF"], h_ret[best_rma]),
    }


def main() -> None:
    t0 = time.time()
    print(f"ED10b Curvature-Gated Gamma CPU Pilot (MuJoCo {mujoco.__version__}, N_SEEDS={N_SEEDS}, noise={SENSOR_NOISE:.0%}, workers={MAX_WORKERS})")

    summaries: dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for idx, fam in enumerate(["flat", "curved", "contact", "mixed"], start=1):
            print(f"{idx}/4 Running {fam.upper()} family (1% sensor noise, {N_SEEDS} seeds)...")
            rows = list(pool.map(_run_one_seed, [(fam, s) for s in range(N_SEEDS)]))
            s = summarize_family(rows)
            summaries[fam] = s
            b_rma = s["best_rma_arm"]
            print(
                f"    {fam.upper()} S5 held-out: Gated={s['s5_heldout_return']['Gamma_gated']['mean']:.4f} "
                f"| Gamma_RFF={s['s5_heldout_return']['Gamma_RFF']['mean']:.4f} "
                f"| EB12={s['s5_heldout_return']['EB12']['mean']:.4f} "
                f"| GAT_MLP={s['s5_heldout_return']['GAT_MLP']['mean']:.4f} "
                f"| {b_rma}={s['s5_heldout_return'][b_rma]['mean']:.4f}"
            )
            print(
                f"    Gaps (Gated - ctrl): vs GAT_MLP={s['paired_gated_minus_gat_mlp']['gap_in_se']:+.2f} SE "
                f"| vs best_RMA={s['paired_gated_minus_best_rma']['gap_in_se']:+.2f} SE "
                f"| vs always_Gamma={s['paired_gated_minus_always_gamma']['gap_in_se']:+.2f} SE "
                f"| vs always_EB12={s['paired_gated_minus_always_eb12']['gap_in_se']:+.2f} SE"
            )

    # Strict ED10b promotion gates (reviews/flood-triage.md row 572):
    gates = {
        "curved_gated_beats_gat_mlp_gt_2se": bool(summaries["curved"]["paired_gated_minus_gat_mlp"]["gap_in_se"] > 2.0),
        "curved_gated_beats_matched_rma_gt_2se": bool(summaries["curved"]["paired_gated_minus_best_rma"]["gap_in_se"] > 2.0),
        "contact_gated_beats_gat_mlp_gt_2se": bool(summaries["contact"]["paired_gated_minus_gat_mlp"]["gap_in_se"] > 2.0),
        "contact_gated_beats_matched_rma_gt_2se": bool(summaries["contact"]["paired_gated_minus_best_rma"]["gap_in_se"] > 2.0),
        "mixed_gated_beats_always_gamma_gt_2se": bool(summaries["mixed"]["paired_gated_minus_always_gamma"]["gap_in_se"] > 2.0),
        "mixed_gated_beats_always_eb12_gt_2se": bool(summaries["mixed"]["paired_gated_minus_always_eb12"]["gap_in_se"] > 2.0),
        "retention_ge_0.85_all_families": bool(
            all(summaries[f]["retention_s1_s4_return"]["Gamma_gated"]["mean"] >= 0.85 for f in ["flat", "curved", "contact", "mixed"])
        ),
        "rma_capacity_matched_s5_trainB_ge_0.90": bool(
            all(summaries[f]["s5_trainB_return"][summaries[f]["best_rma_arm"]]["mean"] >= 0.90 for f in ["flat", "curved", "contact", "mixed"])
        ),
    }
    verdict = "PROMOTE" if all(gates.values()) else "NO_PROMOTE"
    elapsed = time.time() - t0

    out = {
        "meta": {
            "mujoco_version": mujoco.__version__,
            "n_seeds": N_SEEDS,
            "n_ritual": N_RITUAL,
            "n_skill_eps": N_SKILL_EPS,
            "horizon": HORIZON,
            "sensor_noise": SENSOR_NOISE,
            "curvature_gate_tau": CURVATURE_GATE_TAU,
            "elapsed_sec": elapsed,
            "platform": platform.platform(),
        },
        "families": summaries,
        "gates": gates,
        "verdict": verdict,
    }
    out_path = Path(__file__).resolve().parent / "results.json"
    out_path.write_text(json.dumps(out, indent=2))

    print(f"\n=== ED10b VERDICT: {verdict} (elapsed {elapsed:.1f}s) ===")
    print(f"  Gates: {gates}")


if __name__ == "__main__":
    main()
