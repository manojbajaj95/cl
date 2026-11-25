"""Simulation experiments for the reproduction-number law. Usage: python -m agents.epidemic.experiments"""
from __future__ import annotations

import json
from multiprocessing import Pool as MP
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .model import Params, run
from .theory import fixed_point, integrate, small_x_power_law

OUT = Path(__file__).parent / "results"
T = 4000
T_COND = 200


def _phase_job(args):
    tau, ratio, seed = args
    p = Params(tau=tau, alpha_d=0.8 * ratio, alpha_s=0.8)
    r = run(p, T, seed=seed)
    x_c, n_c = r["x"][T_COND], r["n"][T_COND]
    xo, _ = integrate(p, T - T_COND, n0=n_c, x0=x_c)
    return dict(tau=tau, ratio=ratio, seed=seed, R=p.R, x_final=float(r["x"][-1]), x_ode_cond=float(xo[-1]),
                x_star=fixed_point(p), succ_last=float(r["success"][-500:].mean()),
                succ_peak=float(np.convolve(r["success"], np.ones(200) / 200, "valid").max()))


def phase_diagram(workers=6):
    jobs = [(tau, ratio, s) for tau in np.linspace(0.0, 0.6, 13) for ratio in [0.25, 0.5, 1.0, 1.5, 2.0]
            for s in range(4)]
    with MP(workers) as mp:
        rows = mp.map(_phase_job, jobs)
    R = np.array([r["R"] for r in rows])
    xf = np.array([r["x_final"] for r in rows])
    xc = np.array([r["x_ode_cond"] for r in rows])
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].scatter(R, xf, s=10, alpha=0.6, label="simulation (T=4000)")
    order = np.argsort(R)
    ax[0].scatter(R, [r["x_star"] for r in rows], s=6, c="k", marker="x", label="mean-field fixed point")
    ax[0].axvline(1, ls="--", c="r")
    ax[0].set_xlabel("R = k(a_D tau - d)/a_S")
    ax[0].set_ylabel("defective fraction of pool")
    ax[0].legend()
    ax[1].scatter(xc, xf, s=10, alpha=0.6)
    ax[1].plot([0, 1], [0, 1], "k--")
    ax[1].set_xlabel(f"ODE prediction from state at t={T_COND}")
    ax[1].set_ylabel("simulated defective fraction at T")
    fig.tight_layout()
    fig.savefig(OUT / "phase_diagram.png", dpi=130)
    below, above = xf[R < 0.9], xf[R > 1.1]
    corr = float(np.corrcoef(xc, xf)[0, 1])
    mae = float(np.mean(np.abs(xc - xf)))
    return dict(n_runs=len(rows), median_x_R_below_0_9=float(np.median(below)),
                median_x_R_above_1_1=float(np.median(above)), cond_ode_corr=corr, cond_ode_mae=mae)


def _traj_job(args):
    seed, = args
    return run(Params(tau=0.4, alpha_d=0.8), 6000, seed=seed)


def trajectory():
    p = Params(tau=0.4, alpha_d=0.8)
    with MP(6) as mp:
        rs = mp.map(_traj_job, [(s,) for s in range(12)])
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    w = 200
    peaks = []
    for r in rs:
        s = np.convolve(r["success"], np.ones(w) / w, "valid")
        ax[0].plot(s, alpha=0.35)
        peaks.append(int(np.argmax(s)))
        ax[1].loglog(r["n"][50:], r["x"][50:] + 1e-3, alpha=0.35)
    n = np.logspace(np.log10(40), np.log10(5000), 50)
    i50 = [r["x"][50] for r in rs]
    ax[1].loglog(n, small_x_power_law(p, n, n0=40, x0=float(np.median(i50))) + 1e-3, "k--", lw=2,
                 label=f"linear theory, slope R-1={p.R - 1:.2f}")
    ax[0].axhline(p.base, c="k", ls=":", label="no-memory baseline")
    ax[0].set_xlabel("round")
    ax[0].set_ylabel("task success (moving avg)")
    ax[0].legend()
    ax[1].set_xlabel("pool size N")
    ax[1].set_ylabel("defective fraction")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "rise_then_fall.png", dpi=130)
    final = [float(r["success"][-500:].mean()) for r in rs]
    peak = [float(np.convolve(r["success"], np.ones(w) / w, "valid").max()) for r in rs]
    return dict(R=p.R, median_peak_round=int(np.median(peaks)), median_peak_success=float(np.median(peak)),
                median_final_success=float(np.median(final)), baseline=p.base)


def _interv_job(args):
    kind, seed = args
    p = Params(tau=0.4, alpha_d=0.8)
    r = run(p, 5000, seed=seed, intervene_at=2500, intervention=kind)
    return kind, float(r["success"][2400:2500].mean()), float(r["success"][-500:].mean()), float(r["x"][-1])


def _online_job(args):
    d, phi, seed = args
    p = Params(tau=0.4, alpha_d=0.8, d=d, phi=phi)
    r = run(p, 5000, seed=seed)
    return d, phi, float(r["success"][-500:].mean()), float(r["x"][-1]), p.R


def interventions():
    kinds = ["none", "rollback_roots", "provenance_closure", "oracle_purge"]
    with MP(6) as mp:
        rows = mp.map(_interv_job, [(k, s) for k in kinds for s in range(12)])
        online = mp.map(_online_job, [(d, phi, s) for d in [0.0, 0.05, 0.1] for phi in [0.0, 0.5, 0.9]
                                      for s in range(8)])
    post = {}
    for k in kinds:
        v = np.array([r[1:] for r in rows if r[0] == k])
        post[k] = dict(success_before=float(v[:, 0].mean()), success_after=float(v[:, 1].mean()),
                       x_final=float(v[:, 2].mean()))
    on = {}
    for d in [0.0, 0.05, 0.1]:
        for phi in [0.0, 0.5, 0.9]:
            v = np.array([r[2:4] for r in online if r[0] == d and r[1] == phi])
            R = [r[4] for r in online if r[0] == d and r[1] == phi][0]
            on[f"d={d},phi={phi}"] = dict(R_without_tracing=R, success=float(v[:, 0].mean()), x_final=float(v[:, 1].mean()))
    return dict(post_hoc=post, online=on)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    res = dict(phase=phase_diagram(), trajectory=trajectory(), interventions=interventions())
    (OUT / "summary.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
