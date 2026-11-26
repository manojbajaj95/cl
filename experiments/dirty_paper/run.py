"""Dirty-paper writes: lattice-precoded readout writes against known old weights.

A two-layer ReLU network with a frozen hidden layer stores residues mod M in a
scalar readout. Old task A is written first; new task B is then written with an
update Delta to the readout. Every arm chooses the change z it asks of the B
outputs (and, for the joint arm, of the A outputs) and pays the minimum norm
that realizes z under its constraint. Dirty-paper (lattice) precoding chooses z
inside the coset t - s + M Z^n instead of cancelling the known interference s.
"""

import argparse
import json
import platform
import time
from pathlib import Path

import numpy as np
import scipy

SEEDS = tuple(range(600, 616))
D_IN, HIDDEN, N_A, N_B, N_C = 16, 64, 24, 16, 8
M = 8
THETAS = (15, 30, 60, 90)          # angle between each B input and its nearest A input (degrees)
SPREADS = (0, 4)                   # old outputs lifted by M*L, L uniform on [-S, S]
MAIN = (30, 0)
BUDGETS = np.geomspace(0.05, 1.5, 15)   # update norm as a fraction of GPM's exact-write norm
GD_STEPS = 60000
NODE_CAP = 400000
DECAY = np.geomspace(1e-4, 0.3, 40)     # weight-decay shrink factor 1-(1-gamma)^t
ARMS = ("FT", "GPM", "OWM", "GPM-GD", "THP", "VP", "VP-joint")
KILL_PP = 1.0


def wrap(u):
    return u - M * np.round(u / M)


def features(rng, x, U, c):
    return np.maximum(U @ x + c[:, None], 0.0) * np.sqrt(2.0 / HIDDEN)


def instance(seed, theta, spread):
    rng = np.random.default_rng([seed, theta, spread])
    U = rng.normal(size=(HIDDEN, D_IN)) / np.sqrt(D_IN)
    c = rng.normal(scale=0.5, size=HIDDEN)
    xa = rng.normal(size=(D_IN, N_A))
    near = rng.choice(N_A, N_B, replace=False)
    xi = rng.normal(size=(D_IN, N_B))
    th = np.deg2rad(theta)
    xb = np.cos(th) * xa[:, near] + np.sin(th) * xi
    xc = rng.normal(size=(D_IN, 4 * N_C))
    fa, fb, fc = (features(rng, x, U, c) for x in (xa, xb, xc))
    ta = rng.integers(0, M, N_A).astype(float)
    tb = rng.integers(0, M, N_B).astype(float)
    tc = rng.integers(0, M, 4 * N_C).astype(float)
    ya = ta + M * rng.integers(-spread, spread + 1, N_A)
    w0 = fa @ np.linalg.solve(fa.T @ fa, ya)
    return dict(fa=fa, fb=fb, fc=fc, ta=ta, tb=tb, tc=tc, w0=w0, sa=fa.T @ w0, sb=fb.T @ w0)


# ---------- closest vector search ----------

def lll(B, delta=0.75):
    B = B.copy()
    n = B.shape[1]
    U = np.eye(n, dtype=np.int64)

    def gso(B):
        Q, R = np.linalg.qr(B)
        return R
    k = 1
    R = gso(B)
    while k < n:
        for j in range(k - 1, -1, -1):
            mu = R[j, k] / R[j, j]
            q = np.round(mu)
            if q != 0:
                B[:, k] -= q * B[:, j]
                U[:, k] -= int(q) * U[:, j]
                R = gso(B)
        if R[k, k] ** 2 + R[k - 1, k] ** 2 >= delta * R[k - 1, k - 1] ** 2:
            k += 1
        else:
            B[:, [k - 1, k]] = B[:, [k, k - 1]]
            U[:, [k - 1, k]] = U[:, [k, k - 1]]
            R = gso(B)
            k = max(k - 1, 1)
    return B, U


def cvp(B, y, cap=NODE_CAP):
    """Integer k minimizing ||y - B k|| (LLL + Schnorr-Euchner enumeration)."""
    Bl, U = lll(B)
    Q, R = np.linalg.qr(Bl)
    s = np.sign(np.diag(R)); s[s == 0] = 1
    Q, R = Q * s, (R.T * s).T
    yt = Q.T @ y
    n = len(yt)
    base = np.sum((y - Q @ yt) ** 2)
    best = [np.inf, None]
    nodes = [0]
    u = np.zeros(n)

    def babai():
        v = np.zeros(n)
        for i in range(n - 1, -1, -1):
            v[i] = np.round((yt[i] - R[i, i + 1:] @ v[i + 1:]) / R[i, i])
        return v
    v = babai()
    best = [np.sum((yt - R @ v) ** 2), v.copy()]

    def rec(i, partial):
        if nodes[0] > cap:
            return
        center = (yt[i] - R[i, i + 1:] @ u[i + 1:]) / R[i, i]
        k0 = np.round(center)
        step = 0
        while True:
            for cand in ([k0] if step == 0 else [k0 + step, k0 - step]):
                d = partial + (R[i, i] * (center - cand)) ** 2
                if d >= best[0]:
                    continue
                nodes[0] += 1
                u[i] = cand
                if i == 0:
                    best[0], best[1] = d, u.copy()
                else:
                    rec(i - 1, d)
            step += 1
            if partial + (R[i, i] * (step - 0.5)) ** 2 >= best[0] or nodes[0] > cap:
                return
    rec(n - 1, 0.0)
    return U @ best[1].astype(np.int64), nodes[0] <= cap, best[0] + base


def vp_target(r, G):
    """Coset member z = r + M k minimizing z^T G^{-1} z."""
    Ri = np.linalg.cholesky(np.linalg.inv(G)).T
    k, exact, _ = cvp(-M * Ri, Ri @ r)
    return r + M * k, exact


# ---------- writes ----------

def ridge(G, z, rho):
    """a = (G + lam I)^-1 z with a^T G a = rho^2 (lam = 0 if already within budget)."""
    g, V = np.linalg.eigh(G)
    zt = V.T @ z
    norm2 = lambda lam: np.sum(g * zt**2 / (g + lam) ** 2)
    if norm2(0.0) <= rho**2:
        lam = 0.0
    else:
        lo, hi = 0.0, 1.0
        while norm2(hi) > rho**2:
            hi *= 4
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if norm2(mid) > rho**2 else (lo, mid)
        lam = hi
    return V @ (zt / (g + lam))


def gd_circ(G, s, t, rho=None, steps=GD_STEPS):
    """Projected GD on the periodic loss, Delta = P Phi_B a; optional norm-ball projection."""
    lr = 1.0 / np.linalg.eigvalsh(G)[-1]
    a = np.zeros(len(t))
    for _ in range(steps):
        e = s + G @ a - t
        a -= lr * (M / (2 * np.pi)) * np.sin(2 * np.pi * e / M)
        if rho is not None:
            n = np.sqrt(a @ G @ a)
            if n > rho:
                a *= rho / n
    return a


def correct(y, t):
    return np.abs(wrap(y - t)) < 0.5


def run_instance(seed, theta, spread, full):
    I = instance(seed, theta, spread)
    fa, fb = I["fa"], I["fb"]
    P = np.eye(HIDDEN) - fa @ np.linalg.solve(fa.T @ fa, fa.T)
    alpha = 1e-2 * np.trace(fa.T @ fa) / N_A
    Pw = np.eye(HIDDEN) - fa @ np.linalg.solve(fa.T @ fa + alpha * np.eye(N_A), fa.T)
    G = fb.T @ P @ fb
    r = I["tb"] - I["sb"]
    # Each arm: (feature map F so Delta = F a, Gram of outputs, target z on its outputs)
    phi = np.hstack([fa, fb])
    K = phi.T @ phi
    zvp, exact_vp = vp_target(r, G)
    rj = np.r_[np.zeros(N_A), r]
    zj, exact_j = vp_target(rj, K)
    gd = gd_circ(G, I["sb"], I["tb"])
    z_gd = G @ gd
    arms = {
        "FT": (fb, r),
        "GPM": (P @ fb, r),
        "OWM": (Pw @ fb, r),
        "GPM-GD": (P @ fb, z_gd),
        "THP": (P @ fb, wrap(r)),
        "VP": (P @ fb, zvp),
        "VP-joint": (phi, zj),
    }
    # interference-free references (Costa: known interference should cost nothing)
    z_clean, _ = vp_target(I["tb"], G)
    clean = {"GPM": float(np.linalg.norm(P @ fb @ np.linalg.solve(G, I["tb"]))),
             "VP": float(np.linalg.norm(P @ fb @ np.linalg.solve(G, z_clean)))}
    out = {"clean": clean, "exact_cvp": [bool(exact_vp), bool(exact_j)], "gd_converged": bool(np.all(correct(I["sb"] + z_gd, I["tb"])))}
    req, acc_b, acc_a, decay_a, decay_b = {}, {}, {}, {}, {}
    for name, (F, z) in arms.items():
        rows = slice(0, None) if name == "VP-joint" else slice(None)
        out_gram = (phi.T @ F) if name == "VP-joint" else (fb.T @ F)
        a = np.linalg.lstsq(out_gram, z, rcond=None)[0]
        delta = F @ a
        req[name] = float(np.linalg.norm(delta))
        # exact write, then later training modeled as weight decay (shrink by 1 - f)
        w = I["w0"] + delta
        ya, yb = fa.T @ w, fb.T @ w
        decay_a[name] = [float(correct((1 - f) * ya, I["ta"]).mean()) for f in DECAY]
        decay_b[name] = [float(correct((1 - f) * yb, I["tb"]).mean()) for f in DECAY]
    gpm_norm = req["GPM"]
    if full:
        for name, (F, z) in arms.items():
            A_acc, B_acc = [], []
            for frac in BUDGETS:
                rho = frac * gpm_norm
                if name == "GPM-GD":
                    a = gd_circ(G, I["sb"], I["tb"], rho=rho, steps=GD_STEPS // 4)
                    delta = P @ fb @ a
                elif name == "VP-joint":
                    delta = phi @ ridge(K, z, rho)
                elif name == "OWM":
                    H = fb.T @ Pw @ fb
                    a = ridge_general(H, (Pw @ fb).T @ (Pw @ fb), z, rho)
                    delta = Pw @ fb @ a
                else:
                    Gm = fb.T @ F
                    delta = F @ ridge(Gm, z, rho)
                w = I["w0"] + delta
                A_acc.append(float(correct(fa.T @ w, I["ta"]).mean()))
                B_acc.append(float(correct(fb.T @ w, I["tb"]).mean()))
            acc_a[name], acc_b[name] = A_acc, B_acc
    out.update(required=req, acc_a=acc_a, acc_b=acc_b, decay_a=decay_a, decay_b=decay_b,
               interference_rms=float(np.sqrt(np.mean(I["sb"] ** 2))), cond_G=float(np.linalg.cond(G)))
    return out


def ridge_general(H, N, z, rho):
    """a = (H + lam I)^-1 z with a^T N a = rho^2."""
    f = lambda lam: np.linalg.solve(H + lam * np.eye(len(z)), z)
    nrm = lambda lam: f(lam) @ N @ f(lam)
    if nrm(0.0) <= rho**2:
        return f(0.0)
    lo, hi = 0.0, 1.0
    while nrm(hi) > rho**2:
        hi *= 4
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if nrm(mid) > rho**2 else (lo, mid)
    return f(hi)


# ---------- summary ----------

def ci(x):
    x = np.asarray(x, float)
    from scipy.stats import t as st
    h = st.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0
    return [float(x.mean()), float(x.mean() - h), float(x.mean() + h)]


def summarize(res):
    S = {}
    for key, rows in res.items():
        req = {a: np.array([r["required"][a] for r in rows]) for a in ARMS}
        base = np.minimum.reduce([req["GPM"], req["OWM"], req["GPM-GD"]])
        S[key] = {
            "required_over_gpm": {a: ci(req[a] / req["GPM"]) for a in ARMS},
            "vp_over_best_gpm_family": ci(req["VP"] / base),
            "vpjoint_over_best_gpm_family": ci(req["VP-joint"] / base),
            "thp_over_gpmgd": ci(req["THP"] / req["GPM-GD"]),
            "vp_over_clean_vp": ci([r["required"]["VP"] / r["clean"]["VP"] for r in rows]),
            "gpm_over_clean_gpm": ci([r["required"]["GPM"] / r["clean"]["GPM"] for r in rows]),
            "gd_converged": float(np.mean([r["gd_converged"] for r in rows])),
            "cvp_exact": np.mean([r["exact_cvp"] for r in rows], axis=0).tolist(),
            "cond_G_median": float(np.median([r["cond_G"] for r in rows])),
            "interference_rms": ci([r["interference_rms"] for r in rows]),
            "required_over_gpmgd": {a: ci(req[a] / req["GPM-GD"]) for a in ARMS},
            "decay_half_life_a": {a: ci([half(r["decay_a"][a]) for r in rows]) for a in ARMS},
            "decay_half_life_b": {a: ci([half(r["decay_b"][a]) for r in rows]) for a in ARMS},
        }
        if rows[0]["acc_b"]:
            accb = {a: np.array([r["acc_b"][a] for r in rows]) for a in ARMS}
            acca = {a: np.array([r["acc_a"][a] for r in rows]) for a in ARMS}
            S[key]["acc_b"] = {a: [ci(accb[a][:, j]) for j in range(len(BUDGETS))] for a in ARMS}
            S[key]["acc_a"] = {a: [ci(acca[a][:, j]) for j in range(len(BUDGETS))] for a in ARMS}
            S[key]["vp_minus_gpmgd_budget_pp"] = [ci(100 * (accb["VP"][:, j] - accb["GPM-GD"][:, j])) for j in range(len(BUDGETS))]
            # pre-registered decision: best DPC arm vs best GPM-family arm, B accuracy (pp),
            # averaged over budgets, among arms whose A accuracy stays within 1 pp of GPM's
            dpc = np.maximum.reduce([np.where(acca[a] >= acca["GPM"] - 0.01, accb[a], 0).mean(1) for a in ("THP", "VP", "VP-joint")])
            gpm = np.maximum.reduce([accb[a].mean(1) for a in ("GPM", "OWM", "GPM-GD")])
            dvp = np.where(acca["VP"] >= acca["GPM"] - 0.01, accb["VP"], 0).mean(1)
            S[key]["dpc_minus_gpm_pp"] = ci(100 * (dpc - gpm))
            S[key]["vp_minus_gpmgd_pp"] = ci(100 * (dvp - accb["GPM-GD"].mean(1)))
            # post hoc: use the joint write when the budget covers its exact norm, else modular GD
            thr = req["VP-joint"] / req["GPM"]
            use = BUDGETS[None, :] >= thr[:, None] * (1 - 1e-9)
            sw_b = np.where(use, accb["VP-joint"], accb["GPM-GD"])
            sw_a = np.where(use, acca["VP-joint"], acca["GPM-GD"])
            S[key]["switch_min_acc_a"] = float(sw_a.min())
            S[key]["switch_minus_gpmgd_pp"] = ci(100 * (sw_b - accb["GPM-GD"]).mean(1))
            window = use & (BUDGETS[None, :] < (req["GPM-GD"] / req["GPM"])[:, None])
            S[key]["switch_minus_gpmgd_window_pp"] = ci([100 * (sw_b - accb["GPM-GD"])[i][window[i]].mean() for i in range(len(rows)) if window[i].any()])
            S[key]["killed"] = bool(ci(100 * (dpc - gpm))[1] <= 0 or ci(100 * (dpc - gpm))[0] < KILL_PP)
    return S


def half(curve):
    curve = np.asarray(curve)
    idx = np.nonzero(curve < 0.5)[0]
    return float(DECAY[idx[0]]) if len(idx) else float(DECAY[-1])


def self_test():
    rng = np.random.default_rng(0)
    # 1. CVP is never worse than brute force over a box in 4 dims
    for _ in range(20):
        B = rng.normal(size=(4, 4)); y = rng.normal(size=4) * 3
        k, ok, _ = cvp(B, y)
        grid = np.array(np.meshgrid(*[np.arange(-8, 9)] * 4)).reshape(4, -1).T
        brute = np.min(np.sum((y[None] - grid @ B.T) ** 2, 1))
        assert ok and np.sum((y - B @ k) ** 2) <= brute + 1e-9
    # 2. A-null arms leave A outputs unchanged; all exact writes decode B
    I = instance(SEEDS[0], 30, 0)
    P = np.eye(HIDDEN) - I["fa"] @ np.linalg.solve(I["fa"].T @ I["fa"], I["fa"].T)
    G = I["fb"].T @ P @ I["fb"]
    r = I["tb"] - I["sb"]
    for z in (r, wrap(r), vp_target(r, G)[0]):
        d = P @ I["fb"] @ np.linalg.solve(G, z)
        assert np.abs(I["fa"].T @ d).max() < 1e-8
        assert correct(I["fb"].T @ (I["w0"] + d), I["tb"]).all()
    # 3. Without a lattice (M -> infinity) the coset is a point: VP equals GPM
    global M
    m0, M = M, 1e9
    assert np.allclose(vp_target(r, G)[0], r)
    M = m0
    # 4. VP is never costlier than THP or GD's coset
    zv = vp_target(r, G)[0]
    cost = lambda z: z @ np.linalg.solve(G, z)
    a = gd_circ(G, I["sb"], I["tb"], steps=20000)
    assert cost(zv) <= cost(wrap(r)) + 1e-9 and cost(zv) <= cost(G @ a) + 1e-6
    print("self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--summarize-only", action="store_true", help="recompute the summary from saved seeds")
    p.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = p.parse_args()
    if args.self_test:
        self_test(); return
    if args.summarize_only:
        path = args.output / "results.json"
        result = json.loads(path.read_text())
        result["summary"] = summarize(result["seeds"])
        path.write_text(json.dumps(result, separators=(",", ":")) + "\n")
        return
    t0 = time.time()
    res = {}
    for th in THETAS:
        for sp in SPREADS:
            full = True
            res[f"theta{th}_S{sp}"] = [run_instance(s, th, sp, full) for s in SEEDS]
            print(f"theta={th} S={sp} done {time.time()-t0:.0f}s", flush=True)
    summary = summarize(res)
    result = {
        "parameters": dict(seeds=SEEDS, d_in=D_IN, hidden=HIDDEN, n_a=N_A, n_b=N_B, n_c=N_C, M=M, thetas=THETAS,
                           spreads=SPREADS, main=MAIN, budgets=BUDGETS, gd_steps=GD_STEPS, node_cap=NODE_CAP,
                           decay=DECAY, kill_pp=KILL_PP),
        "summary": summary,
        "seeds": res,
        "environment": dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
        "runtime_s": time.time() - t0,
    }
    (args.output / "results.json").write_text(json.dumps(result, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x), separators=(",", ":")) + "\n")
    print(json.dumps({k: {kk: v[kk] for kk in ("required_over_gpm", "vp_over_best_gpm_family", "vpjoint_over_best_gpm_family", "thp_over_gpmgd", "vp_over_clean_vp", "gpm_over_clean_gpm", "dpc_minus_gpm_pp", "vp_minus_gpmgd_pp", "killed", "gd_converged", "cvp_exact", "cond_G_median") if kk in v} for k, v in summary.items()}, indent=1))


if __name__ == "__main__":
    main()
