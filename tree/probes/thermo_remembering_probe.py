"""Small CPU probe for tree/thermodynamics-of-remembering.md.

Tests three concrete thermodynamic distinctions on a tiny 2-layer ReLU MLP
(plus linear host control) in pure NumPy across 16 paired worlds:
  1. Parameter erasure vs predictive-channel mismatch (why naive parameter
     Landauer counting fails on gauge/null directions).
  2. Sivak-Crooks thermodynamic-length pacing vs linear ramp & anti-geodesic
     at matched total new-task exposure.
  3. Protocol work dissipation W_diss = (W_fwd + W_rev)/2 across task conflict
     levels, and Kovacs-like non-monotonic rebound after shock+repair.
"""

from __future__ import annotations

import zlib
import numpy as np


def make_rng(*parts: object) -> np.random.Generator:
    seed = zlib.crc32(repr(parts).encode("utf-8")) & 0xFFFFFFFF
    return np.random.default_rng(seed)


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-z))


def bce_loss(p: np.ndarray, y: np.ndarray) -> float:
    p = np.clip(p, 1e-7, 1.0 - 1e-7)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def kl_bernoulli(p_ref: np.ndarray, p_cur: np.ndarray) -> float:
    p_ref = np.clip(p_ref, 1e-7, 1.0 - 1e-7)
    p_cur = np.clip(p_cur, 1e-7, 1.0 - 1e-7)
    kl = p_ref * np.log(p_ref / p_cur) + (1.0 - p_ref) * np.log((1.0 - p_ref) / (1.0 - p_cur))
    return float(np.mean(kl))


class TinyMLP:
    def __init__(self, d: int, h: int, rng: np.random.Generator):
        self.W1 = rng.normal(0.0, np.sqrt(2.0 / d), size=(d, h))
        self.b1 = np.zeros(h)
        self.w2 = rng.normal(0.0, np.sqrt(1.0 / h), size=(h,))
        self.b2 = 0.0

    def copy(self) -> "TinyMLP":
        m = TinyMLP.__new__(TinyMLP)
        m.W1 = self.W1.copy()
        m.b1 = self.b1.copy()
        m.w2 = self.w2.copy()
        m.b2 = float(self.b2)
        return m

    def flat(self) -> np.ndarray:
        return np.concatenate([self.W1.ravel(), self.b1.ravel(), self.w2.ravel(), np.array([self.b2])])

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        h = np.maximum(0.0, X @ self.W1 + self.b1)
        return sigmoid(h @ self.w2 + self.b2)

    def loss_and_acc(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        p = self.predict_proba(X)
        return bce_loss(p, y), float(np.mean((p >= 0.5) == y))

    def grads(self, X: np.ndarray, y: np.ndarray, wd: float = 1e-4) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        n = X.shape[0]
        pre = X @ self.W1 + self.b1
        h = np.maximum(0.0, pre)
        p = sigmoid(h @ self.w2 + self.b2)
        dz = (p - y) / n
        gw2 = h.T @ dz + wd * self.w2
        gb2 = float(np.sum(dz))
        dh = dz[:, None] * self.w2[None, :]
        dpre = dh * (pre > 0.0)
        gW1 = X.T @ dpre + wd * self.W1
        gb1 = np.sum(dpre, axis=0)
        return gW1, gb1, gw2, gb2

    def step(
        self,
        grads: tuple[np.ndarray, np.ndarray, np.ndarray, float],
        lr: float,
        noise_std: float = 0.0,
        rng: np.random.Generator | None = None,
    ) -> None:
        gW1, gb1, gw2, gb2 = grads
        if noise_std > 0.0 and rng is not None:
            self.W1 -= lr * gW1 + noise_std * rng.normal(size=self.W1.shape)
            self.b1 -= lr * gb1 + noise_std * rng.normal(size=self.b1.shape)
            self.w2 -= lr * gw2 + noise_std * rng.normal(size=self.w2.shape)
            self.b2 -= lr * gb2 + noise_std * float(rng.normal())
        else:
            self.W1 -= lr * gW1
            self.b1 -= lr * gb1
            self.w2 -= lr * gw2
            self.b2 -= lr * gb2


class TinyLinear:
    def __init__(self, d: int, rng: np.random.Generator):
        self.w = rng.normal(0.0, np.sqrt(1.0 / d), size=(d,))
        self.b = 0.0

    def copy(self) -> "TinyLinear":
        m = TinyLinear.__new__(TinyLinear)
        m.w = self.w.copy()
        m.b = float(self.b)
        return m

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return sigmoid(X @ self.w + self.b)

    def loss_and_acc(self, X: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        p = self.predict_proba(X)
        return bce_loss(p, y), float(np.mean((p >= 0.5) == y))

    def grads(self, X: np.ndarray, y: np.ndarray, wd: float = 1e-4) -> tuple[np.ndarray, float]:
        n = X.shape[0]
        p = self.predict_proba(X)
        dz = (p - y) / n
        gw = X.T @ dz + wd * self.w
        gb = float(np.sum(dz))
        return gw, gb

    def step(
        self,
        grads: tuple[np.ndarray, float],
        lr: float,
        noise_std: float = 0.0,
        rng: np.random.Generator | None = None,
    ) -> None:
        gw, gb = grads
        if noise_std > 0.0 and rng is not None:
            self.w -= lr * gw + noise_std * rng.normal(size=self.w.shape)
            self.b -= lr * gb + noise_std * float(rng.normal())
        else:
            self.w -= lr * gw
            self.b -= lr * gb


def make_task_pair(
    d: int,
    n_train: int,
    n_test: int,
    conflict: float,
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    """Generate tasks A and B with controlled conflict in [0, 1].

    conflict=0: disjoint subspaces (orthogonal input support).
    conflict=1: same subspace, flipped teacher rule (strong label conflict).
    """
    half = d // 2
    uA = rng.normal(size=(half,))
    uA /= np.linalg.norm(uA)
    vA = rng.normal(size=(half,))
    vA /= np.linalg.norm(vA)

    def sample_A(n: int) -> tuple[np.ndarray, np.ndarray]:
        X = np.zeros((n, d))
        X[:, :half] = rng.normal(size=(n, half))
        # Mildly nonlinear decision boundary
        z = 1.6 * (X[:, :half] @ uA) + 0.9 * np.tanh(2.0 * (X[:, :half] @ vA))
        y = (z > 0.0).astype(float)
        return X, y

    uB_orth = rng.normal(size=(d - half,))
    uB_orth /= np.linalg.norm(uB_orth)
    vB_orth = rng.normal(size=(d - half,))
    vB_orth /= np.linalg.norm(vB_orth)

    def sample_B(n: int) -> tuple[np.ndarray, np.ndarray]:
        X = np.zeros((n, d))
        # Blend subspace overlap with conflict
        X[:, :half] = conflict * rng.normal(size=(n, half))
        X[:, half:] = (1.0 - conflict) * rng.normal(size=(n, d - half))
        if conflict > 0.0 and conflict < 1.0:
            X /= np.sqrt(conflict**2 + (1.0 - conflict) ** 2)
        z_conf = -1.6 * (X[:, :half] @ uA) + 0.9 * np.tanh(2.0 * (X[:, :half] @ vA))
        z_orth = 1.6 * (X[:, half:] @ uB_orth) + 0.9 * np.tanh(2.0 * (X[:, half:] @ vB_orth))
        z = conflict * z_conf + (1.0 - conflict) * z_orth
        y = (z > 0.0).astype(float)
        return X, y

    XA_tr, yA_tr = sample_A(n_train)
    XA_te, yA_te = sample_A(n_test)
    XB_tr, yB_tr = sample_B(n_train)
    XB_te, yB_te = sample_B(n_test)
    return dict(
        XA_tr=XA_tr, yA_tr=yA_tr, XA_te=XA_te, yA_te=yA_te,
        XB_tr=XB_tr, yB_tr=yB_tr, XB_te=XB_te, yB_te=yB_te,
    )


def sample_batch(X: np.ndarray, y: np.ndarray, bs: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    idx = rng.integers(0, X.shape[0], size=bs)
    return X[idx], y[idx]


def mean_ci95(arr: list[float]) -> tuple[float, float]:
    a = np.asarray(arr, dtype=float)
    return float(np.mean(a)), float(1.96 * np.std(a, ddof=1) / np.sqrt(len(a)))


def run_probe_1(n_worlds: int = 16) -> None:
    """Parameter erasure vs predictive-channel mismatch."""
    d, h, bs, lr = 12, 32, 32, 0.08
    results = {k: {"dtheta": [], "kl_pred": [], "acc_drop": [], "relearn": []}
               for k in ["gauge_null", "ortho_task", "conflict_task"]}

    for w in range(n_worlds):
        rng = make_rng("p1", w)
        data_conf = make_task_pair(d, 512, 256, conflict=1.0, rng=rng)
        data_orth = make_task_pair(d, 512, 256, conflict=0.0, rng=make_rng("p1_orth", w))
        # Share Task A across both
        data_orth["XA_tr"], data_orth["yA_tr"] = data_conf["XA_tr"], data_conf["yA_tr"]
        data_orth["XA_te"], data_orth["yA_te"] = data_conf["XA_te"], data_conf["yA_te"]

        base = TinyMLP(d, h, rng)
        for _ in range(300):
            xb, yb = sample_batch(data_conf["XA_tr"], data_conf["yA_tr"], bs, rng)
            base.step(base.grads(xb, yb), lr)

        pA_ref = base.predict_proba(data_conf["XA_te"])
        _, accA_ref = base.loss_and_acc(data_conf["XA_te"], data_conf["yA_te"])
        theta0 = base.flat()

        # 1) Conflicting task B update (60 steps)
        m_conf = base.copy()
        for _ in range(60):
            xb, yb = sample_batch(data_conf["XB_tr"], data_conf["yB_tr"], bs, rng)
            m_conf.step(m_conf.grads(xb, yb), lr)
        target_norm = float(np.linalg.norm(m_conf.flat() - theta0))

        # 2) Orthogonal task update scaled in steps to match ||Δθ||
        m_orth = base.copy()
        for _ in range(400):
            xb, yb = sample_batch(data_orth["XB_tr"], data_orth["yB_tr"], bs, rng)
            m_orth.step(m_orth.grads(xb, yb), lr)
            if float(np.linalg.norm(m_orth.flat() - theta0)) >= target_norm:
                break

        # 3) Function-preserving ReLU positive rescaling matched to target_norm
        # Binary search scale alpha > 0 so ||θ(alpha) - θ0|| == target_norm
        signs = rng.choice([-1.0, 1.0], size=h)

        def rescaled_model(alpha: float) -> TinyMLP:
            m = base.copy()
            c = np.exp(alpha * signs)
            m.W1 = m.W1 * c[None, :]
            m.b1 = m.b1 * c
            m.w2 = m.w2 / c
            return m

        lo, hi = 0.0, 1.5
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if float(np.linalg.norm(rescaled_model(mid).flat() - theta0)) < target_norm:
                lo = mid
            else:
                hi = mid
        m_gauge = rescaled_model(0.5 * (lo + hi))

        for name, mod in [("gauge_null", m_gauge), ("ortho_task", m_orth), ("conflict_task", m_conf)]:
            dtheta = float(np.linalg.norm(mod.flat() - theta0))
            pA = mod.predict_proba(data_conf["XA_te"])
            kl_p = kl_bernoulli(pA_ref, pA)
            _, accA = mod.loss_and_acc(data_conf["XA_te"], data_conf["yA_te"])
            acc_drop = accA_ref - accA

            # Relearning steps to recover >= accA_ref - 0.02
            m_re = mod.copy()
            re_steps = 0
            re_rng = make_rng("p1_re", w, name)
            while re_steps < 200:
                _, a_now = m_re.loss_and_acc(data_conf["XA_te"], data_conf["yA_te"])
                if a_now >= accA_ref - 0.02:
                    break
                xb, yb = sample_batch(data_conf["XA_tr"], data_conf["yA_tr"], bs, re_rng)
                m_re.step(m_re.grads(xb, yb), lr)
                re_steps += 1

            results[name]["dtheta"].append(dtheta)
            results[name]["kl_pred"].append(kl_p)
            results[name]["acc_drop"].append(acc_drop)
            results[name]["relearn"].append(float(re_steps))

    print("=== PROBE 1: Parameter displacement vs Predictive-channel mismatch (16 worlds) ===")
    for name in ["gauge_null", "ortho_task", "conflict_task"]:
        r = results[name]
        dt = mean_ci95(r["dtheta"])
        kl = mean_ci95(r["kl_pred"])
        ad = mean_ci95(r["acc_drop"])
        rl = mean_ci95(r["relearn"])
        print(
            f"  {name:14s} | ||dtheta||={dt[0]:.3f}+/-{dt[1]:.3f} "
            f"| pred_KL={kl[0]:.4f}+/-{kl[1]:.4f} "
            f"| accA_drop={ad[0]*100:5.2f}+/-{ad[1]*100:4.2f}pp "
            f"| relearn_steps={rl[0]:5.1f}+/-{rl[1]:4.1f}"
        )


def run_probe_2(n_worlds: int = 16) -> None:
    """Sivak-Crooks geodesic pacing vs linear ramp vs quench vs anti-geodesic."""
    d, h, bs, lr = 12, 32, 32, 0.06
    N = 400  # transition horizon

    # Estimate friction profile zeta(lam) = E[||g_B - g_A||^2] on a held-out calibration world
    cal_rng = make_rng("p2_cal")
    cal_data = make_task_pair(d, 512, 256, conflict=0.85, rng=cal_rng)
    lam_grid = np.linspace(0.0, 1.0, 11)
    zeta = np.zeros_like(lam_grid)
    for idx, lam in enumerate(lam_grid):
        m = TinyMLP(d, h, make_rng("p2_cal_init", idx))
        for _ in range(250):
            xA, yA = sample_batch(cal_data["XA_tr"], cal_data["yA_tr"], bs, cal_rng)
            xB, yB = sample_batch(cal_data["XB_tr"], cal_data["yB_tr"], bs, cal_rng)
            gA = m.grads(xA, yA)
            gB = m.grads(xB, yB)
            g = tuple((1.0 - lam) * a + lam * b for a, b in zip(gA, gB))
            m.step(g, lr)
        # Measure local friction: variance of generalized force (L_B - L_A) gradient
        diffs = []
        for _ in range(20):
            xA, yA = sample_batch(cal_data["XA_tr"], cal_data["yA_tr"], bs, cal_rng)
            xB, yB = sample_batch(cal_data["XB_tr"], cal_data["yB_tr"], bs, cal_rng)
            gA = m.grads(xA, yA)
            gB = m.grads(xB, yB)
            diff = sum(float(np.sum((b - a) ** 2)) for a, b in zip(gA, gB))
            diffs.append(diff)
        zeta[idx] = float(np.mean(diffs))

    # Build schedules lam(t) from 0 to 1 with EXACTLY matched mean(lam) = 0.5
    # Geodesic: dt/dlam proportional to sqrt(zeta(lam))
    def build_schedule(weights: np.ndarray) -> np.ndarray:
        cdf = np.cumsum(weights)
        cdf = np.concatenate([[0.0], cdf / cdf[-1]])
        # Invert cdf on N points
        u = np.linspace(0.0, 1.0, N)
        lam = np.interp(u, cdf, np.linspace(0.0, 1.0, len(cdf)))
        # Match mean strictly to 0.5 via monotone power warp
        lo, hi = 0.2, 5.0
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if float(np.mean(lam**mid)) > 0.5:
                lo = mid
            else:
                hi = mid
        return lam ** (0.5 * (lo + hi))

    w_geo = np.sqrt(0.5 * (zeta[:-1] + zeta[1:]))
    w_anti = 1.0 / np.maximum(w_geo, 1e-6)
    scheds = {
        "quench": np.concatenate([np.zeros(N // 2), np.ones(N - N // 2)]),
        "linear": np.linspace(0.0, 1.0, N),
        "geodesic": build_schedule(w_geo),
        "anti_geo": build_schedule(w_anti),
    }

    out = {k: {"work": [], "mean_joint": [], "worst_A": [], "final_A": [], "final_B": []} for k in scheds}
    for w in range(n_worlds):
        rng = make_rng("p2", w)
        data = make_task_pair(d, 512, 256, conflict=0.85, rng=rng)
        base = TinyMLP(d, h, rng)
        for _ in range(300):
            xb, yb = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
            base.step(base.grads(xb, yb), lr)

        # Shared minibatch stream across all schedules
        stream_A = [sample_batch(data["XA_tr"], data["yA_tr"], bs, rng) for _ in range(N)]
        stream_B = [sample_batch(data["XB_tr"], data["yB_tr"], bs, rng) for _ in range(N)]

        for name, lam_seq in scheds.items():
            m = base.copy()
            W_proto = 0.0
            joint_losses = []
            worst_A = 1.0
            for t in range(N):
                lam = float(lam_seq[t])
                xA, yA = stream_A[t]
                xB, yB = stream_B[t]
                if t > 0:
                    dlam = lam - float(lam_seq[t - 1])
                    if abs(dlam) > 0.0:
                        lA, _ = m.loss_and_acc(data["XA_te"], data["yA_te"])
                        lB, _ = m.loss_and_acc(data["XB_te"], data["yB_te"])
                        W_proto += dlam * (lB - lA)
                gA = m.grads(xA, yA)
                gB = m.grads(xB, yB)
                g = tuple((1.0 - lam) * a + lam * b for a, b in zip(gA, gB))
                m.step(g, lr)
                if (t + 1) % 20 == 0:
                    lA, aA = m.loss_and_acc(data["XA_te"], data["yA_te"])
                    lB, _ = m.loss_and_acc(data["XB_te"], data["yB_te"])
                    joint_losses.append(0.5 * (lA + lB))
                    worst_A = min(worst_A, aA)
            _, fA = m.loss_and_acc(data["XA_te"], data["yA_te"])
            _, fB = m.loss_and_acc(data["XB_te"], data["yB_te"])
            out[name]["work"].append(W_proto)
            out[name]["mean_joint"].append(float(np.mean(joint_losses)))
            out[name]["worst_A"].append(worst_A)
            out[name]["final_A"].append(fA)
            out[name]["final_B"].append(fB)

    print("\n=== PROBE 2: Protocol schedules at matched B-exposure (16 worlds, conflict=0.85) ===")
    print("  friction profile zeta(lam):", np.round(zeta, 3))
    for name in ["quench", "linear", "geodesic", "anti_geo"]:
        r = out[name]
        wk = mean_ci95(r["work"])
        mj = mean_ci95(r["mean_joint"])
        wa = mean_ci95(r["worst_A"])
        fa = mean_ci95(r["final_A"])
        fb = mean_ci95(r["final_B"])
        print(
            f"  {name:9s} | W_proto={wk[0]:+.4f}+/-{wk[1]:.4f} "
            f"| mean_joint={mj[0]:.4f}+/-{mj[1]:.4f} "
            f"| worst_A={wa[0]*100:5.2f}% "
            f"| end_A={fa[0]*100:5.2f}% end_B={fb[0]*100:5.2f}%"
        )


def run_probe_3(n_worlds: int = 16) -> None:
    """Forward/reverse protocol work dissipation W_diss & Kovacs rebound."""
    d, h, bs, lr = 12, 32, 32, 0.06
    K = 100
    print("\n=== PROBE 3a: Protocol work dissipation W_diss = (W_fwd + W_rev)/2 ===")
    for conflict in [0.0, 0.5, 1.0]:
        w_diss_list = []
        acc_drop_list = []
        for w in range(n_worlds):
            rng = make_rng("p3a", conflict, w)
            data = make_task_pair(d, 512, 256, conflict=conflict, rng=rng)
            # Start at A
            mA = TinyMLP(d, h, rng)
            for _ in range(250):
                xb, yb = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                mA.step(mA.grads(xb, yb), lr)
            _, aA0 = mA.loss_and_acc(data["XA_te"], data["yA_te"])

            # Forward protocol A -> B
            lam_fwd = np.linspace(0.0, 1.0, K)
            W_fwd = 0.0
            m = mA.copy()
            for t in range(K):
                lam = float(lam_fwd[t])
                if t > 0:
                    dlam = lam - float(lam_fwd[t - 1])
                    lA, _ = m.loss_and_acc(data["XA_te"], data["yA_te"])
                    lB, _ = m.loss_and_acc(data["XB_te"], data["yB_te"])
                    W_fwd += dlam * (lB - lA)
                xA, yA = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                xB, yB = sample_batch(data["XB_tr"], data["yB_tr"], bs, rng)
                gA, gB = m.grads(xA, yA), m.grads(xB, yB)
                m.step(tuple((1.0 - lam) * a + lam * b for a, b in zip(gA, gB)), lr, noise_std=0.005, rng=rng)
            _, aA1 = m.loss_and_acc(data["XA_te"], data["yA_te"])

            # Equilibrate at B, then run reverse protocol B -> A
            for _ in range(150):
                xb, yb = sample_batch(data["XB_tr"], data["yB_tr"], bs, rng)
                m.step(m.grads(xb, yb), lr)
            lam_rev = np.linspace(1.0, 0.0, K)
            W_rev = 0.0
            for t in range(K):
                lam = float(lam_rev[t])
                if t > 0:
                    dlam = lam - float(lam_rev[t - 1])
                    lA, _ = m.loss_and_acc(data["XA_te"], data["yA_te"])
                    lB, _ = m.loss_and_acc(data["XB_te"], data["yB_te"])
                    W_rev += dlam * (lB - lA)
                xA, yA = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                xB, yB = sample_batch(data["XB_tr"], data["yB_tr"], bs, rng)
                gA, gB = m.grads(xA, yA), m.grads(xB, yB)
                m.step(tuple((1.0 - lam) * a + lam * b for a, b in zip(gA, gB)), lr, noise_std=0.005, rng=rng)

            w_diss_list.append(0.5 * (W_fwd + W_rev))
            acc_drop_list.append(aA0 - aA1)

        wd = mean_ci95(w_diss_list)
        ad = mean_ci95(acc_drop_list)
        print(
            f"  conflict={conflict:.1f} | W_diss={wd[0]:+.4f}+/-{wd[1]:.4f} "
            f"| accA_drop={ad[0]*100:5.2f}+/-{ad[1]*100:4.2f}pp"
        )

    # Probe 3b: Kovacs-like rebound (shock with B, repair A to match unshocked twin's L_A, then release into 50/50 mix)
    print("\n=== PROBE 3b: Kovacs-like hidden-state rebound (shock+repair vs matched-loss twin) ===")
    for host_name in ["linear", "mlp"]:
        init_gap = []
        peak_rebound = []
        end_gap = []
        for w in range(n_worlds):
            rng = make_rng("p3b", host_name, w)
            data = make_task_pair(d, 512, 256, conflict=0.9, rng=rng)
            base = TinyLinear(d, rng) if host_name == "linear" else TinyMLP(d, h, rng)
            for _ in range(250):
                xb, yb = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                base.step(base.grads(xb, yb), lr)
            lA_target, _ = base.loss_and_acc(data["XA_te"], data["yA_te"])

            # Twin 1: shocked with B for 80 steps, then repaired on A until L_A <= lA_target + 0.01
            shocked = base.copy()
            for _ in range(80):
                xb, yb = sample_batch(data["XB_tr"], data["yB_tr"], bs, rng)
                shocked.step(shocked.grads(xb, yb), lr)
            for _ in range(300):
                lA_now, _ = shocked.loss_and_acc(data["XA_te"], data["yA_te"])
                if lA_now <= lA_target + 0.01:
                    break
                xb, yb = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                shocked.step(shocked.grads(xb, yb), lr)

            lA_s0, _ = shocked.loss_and_acc(data["XA_te"], data["yA_te"])
            init_gap.append(lA_s0 - lA_target)

            # Release both into identical 50/50 (A, B) stream for 120 steps
            twin = base.copy()
            max_diff = -1e9
            for t in range(120):
                xA, yA = sample_batch(data["XA_tr"], data["yA_tr"], bs, rng)
                xB, yB = sample_batch(data["XB_tr"], data["yB_tr"], bs, rng)
                for mod in (shocked, twin):
                    gA, gB = mod.grads(xA, yA), mod.grads(xB, yB)
                    mod.step(tuple(0.5 * a + 0.5 * b for a, b in zip(gA, gB)), lr)
                l_s, _ = shocked.loss_and_acc(data["XA_te"], data["yA_te"])
                l_t, _ = twin.loss_and_acc(data["XA_te"], data["yA_te"])
                max_diff = max(max_diff, l_s - l_t)
            end_gap.append(l_s - l_t)
            peak_rebound.append(max_diff)

        ig = mean_ci95(init_gap)
        pr = mean_ci95(peak_rebound)
        eg = mean_ci95(end_gap)
        print(
            f"  {host_name:6s} | start dL_A={ig[0]:+.4f}+/-{ig[1]:.4f} "
            f"| peak_rebound dL_A={pr[0]:+.4f}+/-{pr[1]:.4f} "
            f"| end dL_A={eg[0]:+.4f}+/-{eg[1]:.4f}"
        )


if __name__ == "__main__":
    run_probe_1()
    run_probe_2()
    run_probe_3()
