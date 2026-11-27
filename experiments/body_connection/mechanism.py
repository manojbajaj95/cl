"""Headroom and ritual-budget test for the body connection (see PREREG.md).

Adds an oracle connection (exact simulator transport) and its best affine
projection to the PR #418 arms, then sweeps the ritual budget and sensor noise.

Run from the repository root:
    python3 -u experiments/body_connection/mechanism.py            # full sweep
    python3 -u experiments/body_connection/mechanism.py --smoke    # 2 seeds, 1 config
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Callable

for _env_var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_env_var, "1")

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

import mujoco
import numpy as np

from arms import (
    EB12Conjugator,
    GenericRFFBasis,
    SkillPolicy,
    estimate_pair_curvature_ed08,
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
from pilot import CURVATURE_GATE_TAU, HORIZON, N_EVAL_EPS, N_SKILL_EPS, mean_se, paired_stats

N_RITUAL_MAX = 19200
FAMILY_IDX = {"flat": 0, "curved": 1, "contact": 2, "mixed": 3}
ARMS = ["Gamma_oracle", "EB12_oracle", "Gamma_gated", "Gamma_RFF", "EB12", "GAT_MLP", "NoTransport", "Expert"]
RET_ARMS = ["Gamma_oracle", "Gamma_gated", "Gamma_RFF", "EB12"]


def oracle_transport(src: MuJoCoArm, dst: MuJoCoArm, q: np.ndarray, qd: np.ndarray, u: np.ndarray) -> np.ndarray:
    single = np.ndim(q) == 1
    q2, qd2, u2 = np.atleast_2d(q), np.atleast_2d(qd), np.atleast_2d(u)
    qdd = src.forward_accel(q2, qd2, u2)
    out = np.stack([dst.inverse_ctrl(q2[i], qd2[i], qdd[i]) for i in range(len(q2))])
    return out[0] if single else out


def fit_affine(u_src: np.ndarray, u_dst: np.ndarray) -> EB12Conjugator:
    X = np.concatenate([u_src, np.ones((len(u_src), 1))], axis=1)
    W = np.linalg.solve(X.T @ X + 1e-4 * np.eye(3), X.T @ u_dst)
    return EB12Conjugator(A=W[:2].T.copy(), b=W[2].copy())


def run_one(args: tuple[str, int, int, float]) -> dict[str, Any]:
    fam, seed, n_ritual, noise = args
    fi = FAMILY_IDX[fam]
    rng = np.random.default_rng(90000 + fi * 10000 + seed)  # skills and demos: fixed across N and noise
    specs = get_body_families()[fam]
    bodies = list(specs.keys())
    held_out = [b for b in bodies if b != "B"]
    env = {b: MuJoCoArm(sp) for b, sp in specs.items()}
    skills = get_skills(contact_family=(fam == "contact"))
    old_skills, s5 = skills[:4], skills[4]

    rituals = {}
    for i, b in enumerate(bodies):
        r_rng = np.random.default_rng(500000 + fi * 10000 + seed * 100 + i)
        full = collect_ritual_data(env[b], N_RITUAL_MAX, noise, r_rng)
        rituals[b] = {k: v[:n_ritual] for k, v in full.items()}

    basis = GenericRFFBasis(seed=seed)
    dyn = {b: fit_rff_dynamics(rituals[b], basis) for b in bodies}
    gat = {b: fit_gat_mlp_body(rituals[b], hidden=48, maxiter=220, seed=seed * 13 + i) for i, b in enumerate(bodies)}

    # Map from each body to every other body via each transport (src, dst) -> action fn.
    rq, rqd, ru = rituals["B"]["q"], rituals["B"]["qd"], rituals["B"]["u"]
    eb12: dict[tuple[str, str], EB12Conjugator] = {}
    eb12_or: dict[tuple[str, str], EB12Conjugator] = {}
    for b in bodies:
        for src, dst in (("B", b), (b, "B")):
            ritual_src = rituals[src]
            eb12[(src, dst)] = fit_eb12_conjugator(dyn[src], dyn[dst], ritual_src)
            if src == "B":
                eb12_or[(src, dst)] = fit_affine(ru, oracle_transport(env[src], env[dst], rq, rqd, ru))

    gate: dict[str, bool] = {"B": False}
    f2: dict[str, float] = {}
    for b in held_out:
        cs = estimate_pair_curvature_ed08(rituals["B"], rituals[b], basis, n_probe=256, seed=seed * 7 + bodies.index(b))
        f2[b] = cs["f2_cal"]
        gate[b] = bool(cs["f2_cal"] > CURVATURE_GATE_TAU and cs["z_score"] > 2.5)

    def transport(arm: str, src: str, dst: str) -> Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]:
        if src == dst and arm != "Gamma_RFF":
            return lambda q, qd, u: u
        if arm == "Gamma_oracle":
            return lambda q, qd, u: oracle_transport(env[src], env[dst], q, qd, u)
        if arm == "Gamma_RFF" or (arm == "Gamma_gated" and gate[dst if src == "B" else src]):
            return lambda q, qd, u: gamma_transport_action(dyn[src], dyn[dst], q, qd, u)
        if arm in ("EB12", "Gamma_gated"):
            return lambda q, qd, u: eb12[(src, dst)].map_action(u)
        raise ValueError(arm)

    # S5 is demonstrated on B only and shared by every arm.
    s5_data = collect_skill_data(env["B"], s5, N_SKILL_EPS, HORIZON, noise, rng)
    s5_pol = SkillPolicy(seed=seed * 10 + 99)
    s5_pol.fit(s5_data["states"], s5_data["times"], s5_data["u"], ridge=1e-2)

    def s5_policy(arm: str, b: str):
        if arm == "NoTransport":
            return lambda s, t: s5_pol.predict(s, t)
        if arm == "Expert":
            return lambda s, t: env[b].inverse_ctrl(s[:2], s[2:4], expert_desired_accel(s5, s[:2], s[2:4], t))
        if arm == "EB12_oracle":
            return lambda s, t: eb12_or[("B", b)].map_action(s5_pol.predict(s, t))
        if arm == "GAT_MLP":
            return lambda s, t: gat_mlp_transport_action(gat["B"], gat[b], s[:2], s[2:4], s5_pol.predict(s, t))
        tr = transport(arm, "B", b)
        return lambda s, t: tr(s[:2], s[2:4], s5_pol.predict(s, t))

    s5_ret = {
        a: {b: evaluate_policy_on_skill(env[b], s5, s5_policy(a, b), n_episodes=N_EVAL_EPS, horizon=HORIZON,
                                        sensor_noise_std=noise, seed=9000 + seed * 17 + bodies.index(b))["return"]
            for b in bodies}
        for a in ARMS
    }

    # Retention: S1..S4 demonstrated on every body, pooled on B via the arm's transport, sent back per body.
    demos = {(b, sk.skill_id): collect_skill_data(env[b], sk, N_SKILL_EPS, HORIZON, noise, rng) for b in bodies for sk in old_skills}
    retention: dict[str, float] = {}
    for a in RET_ARMS:
        rets = []
        for sk in old_skills:
            d = [demos[(b, sk.skill_id)] for b in bodies]
            u_B = np.concatenate([transport(a, b, "B")(dd["states"][:, :2], dd["states"][:, 2:4], dd["u"]) for b, dd in zip(bodies, d)])
            pol = SkillPolicy(seed=seed * 10 + sk.skill_id)
            pol.fit(np.concatenate([dd["states"] for dd in d]), np.concatenate([dd["times"] for dd in d]), u_B, ridge=1e-2)
            for b in bodies:
                tr = transport(a, "B", b)
                fn = lambda s, t, tr=tr, pol=pol: tr(s[:2], s[2:4], pol.predict(s, t))
                rets.append(evaluate_policy_on_skill(env[b], sk, fn, n_episodes=3, horizon=HORIZON, sensor_noise_std=noise,
                                                     seed=7000 + seed * 31 + sk.skill_id * 5 + bodies.index(b))["return"])
        retention[a] = float(np.mean(rets))

    return {
        "family": fam, "seed": seed, "n_ritual": n_ritual, "noise": noise,
        "gate_use_gamma": {b: gate[b] for b in held_out}, "curvature_f2": f2,
        "s5_heldout_return": {a: float(np.mean([s5_ret[a][b] for b in held_out])) for a in ARMS},
        "s5_per_body_return": s5_ret,
        "retention_s1_s4_return": retention,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    h = {a: np.array([r["s5_heldout_return"][a] for r in rows]) for a in ARMS}
    ret = {a: np.array([r["retention_s1_s4_return"][a] for r in rows]) for a in RET_ARMS}
    pairs = [("Gamma_oracle", "EB12"), ("Gamma_oracle", "EB12_oracle"), ("EB12_oracle", "EB12"),
             ("Gamma_RFF", "EB12"), ("Gamma_gated", "EB12"), ("Gamma_gated", "GAT_MLP"),
             ("Gamma_RFF", "Gamma_oracle"), ("GAT_MLP", "EB12")]
    held_out = list(rows[0]["gate_use_gamma"].keys())
    return {
        "n_seeds": len(rows),
        "gate_use_gamma_rate": {b: float(np.mean([r["gate_use_gamma"][b] for r in rows])) for b in held_out},
        "s5_heldout_return": {a: mean_se(h[a]) for a in ARMS},
        "retention_s1_s4_return": {a: mean_se(ret[a]) for a in RET_ARMS},
        "paired": {f"{x}-{y}": paired_stats(h[x], h[y]) for x, y in pairs},
        "seeds": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out", default=str(THIS_DIR / "mechanism_results.json"))
    args = ap.parse_args()
    if args.smoke:
        configs, families, seeds = [(300, 0.01)], ["curved"], 2
    else:
        configs = [(300, 0.01), (1200, 0.01), (4800, 0.01), (19200, 0.01), (1200, 0.0), (19200, 0.0)]
        families, seeds = ["curved", "contact", "mixed"], 16

    t0 = time.time()
    results: dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as pool:
        for n, noise in configs:
            for fam in families:
                rows = list(pool.map(run_one, [(fam, s, n, noise) for s in range(seeds)]))
                s = summarize(rows)
                results.setdefault(f"N{n}_noise{noise:g}", {})[fam] = s
                p = s["paired"]
                print(f"N={n:5d} noise={noise:.2f} {fam:7s} "
                      + " ".join(f"{a}={s['s5_heldout_return'][a]['mean']:.4f}" for a in ARMS[:6])
                      + f" | oracle-EB12 {p['Gamma_oracle-EB12']['gap_in_se']:+.2f}SE"
                      + f" RFF-EB12 {p['Gamma_RFF-EB12']['gap_in_se']:+.2f}SE"
                      + f" ret_gated={s['retention_s1_s4_return']['Gamma_gated']['mean']:.3f}"
                      + f" ({time.time() - t0:.0f}s)", flush=True)

    out = {
        "meta": {"mujoco_version": mujoco.__version__, "numpy": np.__version__, "seeds": seeds,
                 "configs": configs, "families": families, "elapsed_sec": time.time() - t0,
                 "platform": platform.platform()},
        "results": results,
    }
    Path(args.out).write_text(json.dumps(out, indent=1))
    print(f"wrote {args.out} ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
