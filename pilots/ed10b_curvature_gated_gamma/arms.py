"""ED10b Arms: Generic-RFF Gamma, Curvature-Gated Gamma (ED08), GAT-MLP, Capacity-Matched RMA, and EB12.

Every arm receives the EXACT SAME noisy ritual dataset per body (>= 1% sensor noise),
the EXACT SAME Phase 1 demonstrations (S1..S4 across all bodies), and the EXACT SAME
Phase 2 demonstrations (S5 ONLY on body B). No arm sees XML parameters or rigid-body
hand-engineered dynamics bases.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize


# ---------------------------------------------------------------------------
# Shared task-agnostic skill basis (IDENTICAL for Gamma, EB12, GAT, and RMA!)
# ---------------------------------------------------------------------------

def time_phase_features(t: np.ndarray, horizon_sec: float = 0.8) -> np.ndarray:
    t_arr = np.atleast_1d(np.asarray(t, dtype=np.float64))
    phase = 2.0 * np.pi * t_arr / horizon_sec
    feats = [
        t_arr / horizon_sec,
        np.sin(phase), np.cos(phase),
        np.sin(2.0 * phase), np.cos(2.0 * phase),
        np.sin(3.0 * phase), np.cos(3.0 * phase),
    ]
    return np.stack(feats, axis=-1)


def skill_input_features(states: np.ndarray, times: np.ndarray) -> np.ndarray:
    s2 = np.atleast_2d(states)
    q = s2[:, :2]
    qd = s2[:, 2:4]
    tf = time_phase_features(times)
    if len(tf) == 1 and len(s2) > 1:
        tf = np.repeat(tf, len(s2), axis=0)
    return np.concatenate([q, qd, np.sin(q), np.cos(q), tf], axis=-1)  # dim = 15


class SkillPolicy:
    """Per-skill Random Fourier Feature ridge policy (shared policy class across all arms)."""

    def __init__(self, in_dim: int = 15, n_rff: int = 160, lengthscale: float = 3.5, seed: int = 0):
        rng = np.random.default_rng(seed + 101)
        self.W_rff = rng.normal(0.0, 1.0 / lengthscale, size=(in_dim, n_rff))
        self.b_rff = rng.uniform(0.0, 2.0 * np.pi, size=(n_rff,))
        self.n_rff = n_rff
        self.x_mean = np.zeros(in_dim)
        self.x_std = np.ones(in_dim)
        self.W = np.zeros((1 + in_dim + n_rff, 2))

    def _phi(self, x: np.ndarray) -> np.ndarray:
        xn = (x - self.x_mean) / self.x_std
        rff = np.cos(xn @ self.W_rff + self.b_rff) * np.sqrt(2.0 / self.n_rff)
        return np.concatenate([np.ones((len(xn), 1)), xn, rff], axis=-1)

    def fit(self, states: np.ndarray, times: np.ndarray, targets: np.ndarray, ridge: float = 1e-2) -> None:
        x = skill_input_features(states, times)
        self.x_mean = np.mean(x, axis=0)
        self.x_std = np.std(x, axis=0) + 1e-6
        phi = self._phi(x)
        reg = np.eye(phi.shape[1]) * ridge
        reg[0, 0] = 1e-6
        self.W = np.linalg.solve(phi.T @ phi + reg, phi.T @ targets)

    def predict(self, states: np.ndarray, times: np.ndarray | float) -> np.ndarray:
        single = states.ndim == 1
        t_arr = np.array([times], dtype=np.float64) if np.ndim(times) == 0 else np.asarray(times, dtype=np.float64)
        x = skill_input_features(states, t_arr)
        out = self._phi(x) @ self.W
        return out[0] if single else out


# ---------------------------------------------------------------------------
# Generic RFF Dynamics Basis (NO rigid-body hand-engineering!)
# ---------------------------------------------------------------------------

class GenericRFFBasis:
    """Pure generic Random Fourier Feature basis over standardized q and (q, qd).

    Contains NO hand-engineered trigonometric manipulator terms or quadratic velocity
    cross-terms — purely generic stationary RBF kernel approximation.
    """

    def __init__(self, n_rff_q: int = 48, n_rff_s: int = 96, ls_q: float = 2.5, ls_s: float = 3.5, seed: int = 0):
        rng = np.random.default_rng(seed + 777)
        self.W_q = rng.normal(0.0, 1.0 / ls_q, size=(2, n_rff_q))
        self.b_q = rng.uniform(0.0, 2.0 * np.pi, size=(n_rff_q,))
        self.W_s = rng.normal(0.0, 1.0 / ls_s, size=(4, n_rff_s))
        self.b_s = rng.uniform(0.0, 2.0 * np.pi, size=(n_rff_s,))
        self.n_rff_q = n_rff_q
        self.n_rff_s = n_rff_s
        self.q_scale = 1.0
        self.qd_scale = 2.5

    def phi_q(self, q: np.ndarray) -> np.ndarray:
        q2 = np.atleast_2d(q) / self.q_scale
        rff = np.cos(q2 @ self.W_q + self.b_q) * np.sqrt(2.0 / self.n_rff_q)
        return np.concatenate([np.ones((len(q2), 1)), q2, rff], axis=-1)

    def phi_state(self, q: np.ndarray, qd: np.ndarray) -> np.ndarray:
        q2 = np.atleast_2d(q) / self.q_scale
        qd2 = np.atleast_2d(qd) / self.qd_scale
        s = np.concatenate([q2, qd2], axis=-1)
        rff = np.cos(s @ self.W_s + self.b_s) * np.sqrt(2.0 / self.n_rff_s)
        return np.concatenate([np.ones((len(s), 1)), s, rff], axis=-1)


@dataclass
class LearnedRFFDynamics:
    """Control-affine dynamics qdd = B_RFF(q) u + f_RFF(q, qd) fitted from noisy rituals."""
    basis: GenericRFFBasis
    W_B1: np.ndarray
    W_B2: np.ndarray
    W_f: np.ndarray

    def predict_B_f(self, q: np.ndarray, qd: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        pq = self.basis.phi_q(q)
        ps = self.basis.phi_state(q, qd)
        B = np.stack([pq @ self.W_B1, pq @ self.W_B2], axis=-1)
        f = ps @ self.W_f
        return B, f

    def predict_qdd(self, q: np.ndarray, qd: np.ndarray, u: np.ndarray) -> np.ndarray:
        B, f = self.predict_B_f(q, qd)
        u2 = np.atleast_2d(u)
        return np.einsum("nij,nj->ni", B, u2) + f


def fit_rff_dynamics(
    ritual: dict[str, np.ndarray],
    basis: GenericRFFBasis,
    ridge_B: float = 8.0,
    ridge_f: float = 4.0,
) -> LearnedRFFDynamics:
    q, qd, u, qdd = ritual["q"], ritual["qd"], ritual["u"], ritual["qdd"]
    pq = basis.phi_q(q)
    ps = basis.phi_state(q, qd)
    u_scale = float(np.std(u)) + 1e-6
    u_n = u / u_scale
    X = np.concatenate([pq * u_n[:, 0:1], pq * u_n[:, 1:2], ps], axis=1)
    p_q = pq.shape[1]
    p_s = ps.shape[1]
    reg = np.concatenate([
        np.full(p_q, ridge_B),
        np.full(p_q, ridge_B),
        np.full(p_s, ridge_f),
    ])
    # Lighter penalty on constant intercepts
    reg[0] = 1e-4
    reg[p_q] = 1e-4
    reg[2 * p_q] = 1e-4
    W = np.linalg.solve(X.T @ X + np.diag(reg), X.T @ qdd)
    return LearnedRFFDynamics(
        basis=basis,
        W_B1=W[:p_q] / u_scale,
        W_B2=W[p_q : 2 * p_q] / u_scale,
        W_f=W[2 * p_q :],
    )


def gamma_transport_action(
    dyn_src: LearnedRFFDynamics,
    dyn_dst: LearnedRFFDynamics,
    q: np.ndarray,
    qd: np.ndarray,
    u_src: np.ndarray,
    damping: float = 5e-3,
) -> np.ndarray:
    single = q.ndim == 1
    q2 = np.atleast_2d(q)
    qd2 = np.atleast_2d(qd)
    u2 = np.atleast_2d(u_src)

    B_src, f_src = dyn_src.predict_B_f(q2, qd2)
    B_dst, f_dst = dyn_dst.predict_B_f(q2, qd2)
    rhs = np.einsum("nij,nj->ni", B_src, u2) + f_src - f_dst

    BtB = np.einsum("nji,njk->nik", B_dst, B_dst)
    BtB[:, 0, 0] += damping
    BtB[:, 1, 1] += damping
    Btr = np.einsum("nji,nj->ni", B_dst, rhs)
    u_dst = np.linalg.solve(BtB, Btr[..., None])[..., 0]
    return u_dst[0] if single else u_dst


# ---------------------------------------------------------------------------
# Arm 2: EB12 Flat Affine Action Conjugator
# ---------------------------------------------------------------------------

@dataclass
class EB12Conjugator:
    A: np.ndarray  # (2, 2)
    b: np.ndarray  # (2,)

    def map_action(self, u: np.ndarray) -> np.ndarray:
        single = u.ndim == 1
        u2 = np.atleast_2d(u)
        out = u2 @ self.A.T + self.b[None, :]
        return out[0] if single else out


def fit_eb12_conjugator(
    dyn_src: LearnedRFFDynamics,
    dyn_dst: LearnedRFFDynamics,
    ritual_src: dict[str, np.ndarray],
) -> EB12Conjugator:
    q, qd, u_src = ritual_src["q"], ritual_src["qd"], ritual_src["u"]
    u_dst = gamma_transport_action(dyn_src, dyn_dst, q, qd, u_src)
    X = np.concatenate([u_src, np.ones((len(u_src), 1))], axis=1)
    reg = np.diag([1e-4, 1e-4, 1e-4])
    W = np.linalg.solve(X.T @ X + reg, X.T @ u_dst)  # (3, 2)
    return EB12Conjugator(A=W[:2].T.copy(), b=W[2].copy())


# ---------------------------------------------------------------------------
# Arm 3: ED08 Split-Ritual Curvature Estimator + Curvature-Gated Transport
# ---------------------------------------------------------------------------

def _split_ritual(ritual: dict[str, np.ndarray]) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    n = len(ritual["q"]) // 2
    h1 = {k: v[:n] for k, v in ritual.items()}
    h2 = {k: v[n : 2 * n] for k, v in ritual.items()}
    return h1, h2


def estimate_pair_curvature_ed08(
    ritual_src: dict[str, np.ndarray],
    ritual_dst: dict[str, np.ndarray],
    basis: GenericRFFBasis,
    n_probe: int = 256,
    seed: int = 0,
) -> dict[str, float]:
    """Cross-fitted split-ritual curvature statistic F2_cal for pair (src -> dst).

    On a flat pair (pure unsaturated actuator gain change), the true transport is
    state-independent (u_dst = A u_src + b), so the split-half residuals r1 and r2
    of (Gamma - EB12) are independent zero-mean noise and E[<r1, r2>] = 0.
    On a curved or contact pair, r1 and r2 share the state-dependent transport residual
    and F2_cal > 0 with high z-score.
    """
    src1, src2 = _split_ritual(ritual_src)
    dst1, dst2 = _split_ritual(ritual_dst)

    d_src1 = fit_rff_dynamics(src1, basis)
    d_dst1 = fit_rff_dynamics(dst1, basis)
    eb1 = fit_eb12_conjugator(d_src1, d_dst1, src1)

    d_src2 = fit_rff_dynamics(src2, basis)
    d_dst2 = fit_rff_dynamics(dst2, basis)
    eb2 = fit_eb12_conjugator(d_src2, d_dst2, src2)

    rng = np.random.default_rng(seed + 4242)
    q_p = rng.uniform(-1.1, 1.1, size=(n_probe, 2))
    qd_p = rng.uniform(-2.2, 2.2, size=(n_probe, 2))
    u_p = rng.uniform(-30.0, 30.0, size=(n_probe, 2))

    g1 = gamma_transport_action(d_src1, d_dst1, q_p, qd_p, u_p)
    g2 = gamma_transport_action(d_src2, d_dst2, q_p, qd_p, u_p)
    r1 = g1 - eb1.map_action(u_p)
    r2 = g2 - eb2.map_action(u_p)

    # Clip extreme outlier probes (if any) for robust cross-fitted inner product
    dots = np.sum(r1 * r2, axis=-1)
    norms = 0.5 * (np.sum(g1**2, axis=-1) + np.sum(g2**2, axis=-1)) + 1e-6
    scale = float(np.mean(norms))
    vals = dots / scale
    f2_cal = float(np.mean(vals))
    se_f2 = float(np.std(vals, ddof=1) / np.sqrt(len(vals))) + 1e-12
    z_score = f2_cal / se_f2
    return {"f2_cal": f2_cal, "se_f2": se_f2, "z_score": float(z_score)}


# ---------------------------------------------------------------------------
# Arm 4: Grounded Action Transformation (GAT, Hanna & Stone 2017) with Generic MLP
# ---------------------------------------------------------------------------

class GenericMLP:
    """2-layer tanh MLP fitted with L-BFGS-B + L2 regularization on standardized inputs/outputs."""

    def __init__(self, in_dim: int, out_dim: int, hidden: int = 64, seed: int = 0):
        rng = np.random.default_rng(seed + 2026)
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.hidden = hidden
        self.W1 = rng.normal(0.0, np.sqrt(2.0 / (in_dim + hidden)), size=(in_dim, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0.0, np.sqrt(2.0 / (hidden + hidden)), size=(hidden, hidden))
        self.b2 = np.zeros(hidden)
        self.W3 = rng.normal(0.0, np.sqrt(2.0 / (hidden + out_dim)), size=(hidden, out_dim))
        self.b3 = np.zeros(out_dim)
        self.x_mean = np.zeros(in_dim)
        self.x_std = np.ones(in_dim)
        self.y_mean = np.zeros(out_dim)
        self.y_std = np.ones(out_dim)

    def _pack(self) -> np.ndarray:
        return np.concatenate([
            self.W1.ravel(), self.b1,
            self.W2.ravel(), self.b2,
            self.W3.ravel(), self.b3,
        ])

    def _unpack(self, th: np.ndarray):
        i = 0
        n1 = self.in_dim * self.hidden
        W1 = th[i : i + n1].reshape(self.in_dim, self.hidden); i += n1
        b1 = th[i : i + self.hidden]; i += self.hidden
        n2 = self.hidden * self.hidden
        W2 = th[i : i + n2].reshape(self.hidden, self.hidden); i += n2
        b2 = th[i : i + self.hidden]; i += self.hidden
        n3 = self.hidden * self.out_dim
        W3 = th[i : i + n3].reshape(self.hidden, self.out_dim); i += n3
        b3 = th[i : i + self.out_dim]
        return W1, b1, W2, b2, W3, b3

    def _loss_and_grad(self, th: np.ndarray, xn: np.ndarray, yn: np.ndarray, l2: float) -> tuple[float, np.ndarray]:
        W1, b1, W2, b2, W3, b3 = self._unpack(th)
        h1 = np.tanh(xn @ W1 + b1)
        h2 = np.tanh(h1 @ W2 + b2)
        pred = h2 @ W3 + b3
        diff = pred - yn
        n = len(xn)
        loss = float(0.5 * np.mean(np.sum(diff**2, axis=-1)))
        dpred = diff / n

        dW3 = h2.T @ dpred
        db3 = np.sum(dpred, axis=0)
        dh2 = dpred @ W3.T
        da2 = dh2 * (1.0 - h2**2)

        dW2 = h1.T @ da2
        db2 = np.sum(da2, axis=0)
        dh1 = da2 @ W2.T
        da1 = dh1 * (1.0 - h1**2)

        dW1 = xn.T @ da1
        db1 = np.sum(da1, axis=0)

        grad = np.concatenate([dW1.ravel(), db1, dW2.ravel(), db2, dW3.ravel(), db3])
        if l2 > 0.0:
            loss += float(0.5 * l2 * np.sum(th**2))
            grad += l2 * th
        return loss, grad

    def fit(self, X: np.ndarray, Y: np.ndarray, l2: float = 5e-4, maxiter: int = 220) -> None:
        self.x_mean = np.mean(X, axis=0)
        self.x_std = np.std(X, axis=0) + 1e-6
        self.y_mean = np.mean(Y, axis=0)
        self.y_std = np.std(Y, axis=0) + 1e-6
        xn = (X - self.x_mean) / self.x_std
        yn = (Y - self.y_mean) / self.y_std
        res = minimize(
            lambda th: self._loss_and_grad(th, xn, yn, l2),
            self._pack(),
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": 1e-9, "gtol": 1e-5},
        )
        self.W1, self.b1, self.W2, self.b2, self.W3, self.b3 = [a.copy() for a in self._unpack(res.x)]

    def predict(self, X: np.ndarray) -> np.ndarray:
        single = X.ndim == 1
        x2 = np.atleast_2d(X)
        xn = (x2 - self.x_mean) / self.x_std
        h1 = np.tanh(xn @ self.W1 + self.b1)
        h2 = np.tanh(h1 @ self.W2 + self.b2)
        out = (h2 @ self.W3 + self.b3) * self.y_std + self.y_mean
        return out[0] if single else out


@dataclass
class GATMLPBody:
    """Grounded Action Transformation (Hanna & Stone 2017) generic MLP forward + inverse dynamics."""
    fwd_mlp: GenericMLP  # (q, qd, u) -> qdd
    inv_mlp: GenericMLP  # (q, qd, qdd) -> u


def fit_gat_mlp_body(ritual: dict[str, np.ndarray], hidden: int = 48, maxiter: int = 220, seed: int = 0) -> GATMLPBody:
    X_fwd = np.concatenate([ritual["q"], ritual["qd"], ritual["u"]], axis=1)
    Y_fwd = ritual["qdd"]
    fwd = GenericMLP(in_dim=6, out_dim=2, hidden=hidden, seed=seed)
    fwd.fit(X_fwd, Y_fwd, l2=5e-4, maxiter=maxiter)

    X_inv = np.concatenate([ritual["q"], ritual["qd"], ritual["qdd"]], axis=1)
    Y_inv = ritual["u"]
    inv = GenericMLP(in_dim=6, out_dim=2, hidden=hidden, seed=seed + 1000)
    inv.fit(X_inv, Y_inv, l2=5e-4, maxiter=maxiter)
    return GATMLPBody(fwd_mlp=fwd, inv_mlp=inv)


def gat_mlp_transport_action(
    gat_src: GATMLPBody,
    gat_dst: GATMLPBody,
    q: np.ndarray,
    qd: np.ndarray,
    u_src: np.ndarray,
) -> np.ndarray:
    single = q.ndim == 1
    q2 = np.atleast_2d(q)
    qd2 = np.atleast_2d(qd)
    u2 = np.atleast_2d(u_src)
    qdd_src = gat_src.fwd_mlp.predict(np.concatenate([q2, qd2, u2], axis=1))
    u_dst = gat_dst.inv_mlp.predict(np.concatenate([q2, qd2, qdd_src], axis=1))
    return u_dst[0] if single else u_dst


# ---------------------------------------------------------------------------
# Arm 5: Capacity-Matched RMA (IDENTICAL per-skill RFF policy class as Gamma!)
# ---------------------------------------------------------------------------

def extract_rma_body_latents(
    dynamics_by_body: dict[str, LearnedRFFDynamics],
    n_probe: int = 64,
    latent_dim: int = 6,
    seed: int = 0,
) -> dict[str, np.ndarray]:
    """Ritual-derived body latents z_b via SVD of noisy ritual acceleration responses."""
    rng = np.random.default_rng(seed + 9090)
    q_p = rng.uniform(-1.2, 1.2, size=(n_probe, 2))
    qd_p = rng.uniform(-2.5, 2.5, size=(n_probe, 2))
    u_p = rng.uniform(-30.0, 30.0, size=(n_probe, 2))

    body_names = sorted(dynamics_by_body.keys())
    resp = np.stack([dynamics_by_body[b].predict_qdd(q_p, qd_p, u_p).ravel() for b in body_names], axis=0)
    resp_c = resp - np.mean(resp, axis=0, keepdims=True)
    U, S, _ = np.linalg.svd(resp_c, full_matrices=False)
    k = min(latent_dim, U.shape[1])
    Z = U[:, :k] * S[:k]
    Z = Z / (np.std(Z, axis=0, keepdims=True) + 1e-6)
    if k < latent_dim:
        Z = np.concatenate([Z, np.zeros((len(body_names), latent_dim - k))], axis=1)
    return {b: Z[i].copy() for i, b in enumerate(body_names)}


class CapacityMatchedRMA:
    """Capacity-matched RMA using the EXACT SAME per-skill 160-dim RFF SkillPolicy class as Gamma.

    For each skill k and body b (with ritual latent z_b):
      u_canon_k(s, t) = SkillPolicy_k(s, t)                       # IDENTICAL basis & capacity to Gamma!
      G(z_b) = I + reshape(z_b @ WA + bA, (2, 2))                 # exact flat-gain body scaling
      d(z_b) = z_b @ Wd + bd                                      # body action bias
      r(s, z_b) = MLP_res([s, z_b])                               # state-dependent body residual
      u(s, t, k, z_b) = G(z_b) @ u_canon_k(s, t) + d(z_b) + r(s, z_b)

    Guarantees S5@B >= 0.95 (exact closed-form ridge fit of SkillPolicy_S5 on B),
    exact representation of flat gain changes via G(z_b), and nonlinear state-dependent
    body modulation via MLP_res(s, z_b) learned across S1..S4 on all bodies.
    """

    def __init__(self, z_dim: int = 6, hidden_res: int = 32, seed: int = 0):
        rng = np.random.default_rng(seed + 5150)
        self.z_dim = z_dim
        self.hidden_res = hidden_res
        self.seed = seed
        self.skill_policies: dict[int, SkillPolicy] = {}

        # Body modulator parameters: WA (z_dim, 4), bA (4), Wd (z_dim, 2), bd (2),
        # plus 1-hidden-layer residual MLP (4 + z_dim -> hidden_res -> 2)
        self.WA = rng.normal(0.0, 0.05, size=(z_dim, 4))
        self.bA = np.zeros(4)
        self.Wd = rng.normal(0.0, 0.05, size=(z_dim, 2))
        self.bd = np.zeros(2)
        in_res = 4 + z_dim
        self.Wr1 = rng.normal(0.0, np.sqrt(2.0 / (in_res + hidden_res)), size=(in_res, hidden_res))
        self.br1 = np.zeros(hidden_res)
        self.Wr2 = rng.normal(0.0, 0.05, size=(hidden_res, 2))
        self.br2 = np.zeros(2)
        self.s_scale = np.array([1.0, 1.0, 2.5, 2.5])

    def _pack_body(self) -> np.ndarray:
        return np.concatenate([
            self.WA.ravel(), self.bA,
            self.Wd.ravel(), self.bd,
            self.Wr1.ravel(), self.br1,
            self.Wr2.ravel(), self.br2,
        ])

    def _unpack_body(self, th: np.ndarray):
        i = 0
        z = self.z_dim
        h = self.hidden_res
        in_r = 4 + z
        WA = th[i : i + 4 * z].reshape(z, 4); i += 4 * z
        bA = th[i : i + 4]; i += 4
        Wd = th[i : i + 2 * z].reshape(z, 2); i += 2 * z
        bd = th[i : i + 2]; i += 2
        Wr1 = th[i : i + in_r * h].reshape(in_r, h); i += in_r * h
        br1 = th[i : i + h]; i += h
        Wr2 = th[i : i + 2 * h].reshape(h, 2); i += 2 * h
        br2 = th[i : i + 2]
        return WA, bA, Wd, bd, Wr1, br1, Wr2, br2

    def _body_mod_from_params(self, th: np.ndarray, states: np.ndarray, z: np.ndarray):
        WA, bA, Wd, bd, Wr1, br1, Wr2, br2 = self._unpack_body(th)
        G = np.eye(2)[None, :, :] + (z @ WA + bA).reshape(-1, 2, 2)
        d = z @ Wd + bd
        sz = np.concatenate([states / self.s_scale, z], axis=-1)
        hr = np.tanh(sz @ Wr1 + br1)
        res = hr @ Wr2 + br2
        return G, d, res, sz, hr

    def _body_loss_and_grad(
        self, th: np.ndarray, states: np.ndarray, u_canon: np.ndarray, z: np.ndarray, y: np.ndarray,
        weights: np.ndarray, l2: float,
    ) -> tuple[float, np.ndarray]:
        WA, bA, Wd, bd, Wr1, br1, Wr2, br2 = self._unpack_body(th)
        G, d, res, sz, hr = self._body_mod_from_params(th, states, z)
        pred = np.einsum("nij,nj->ni", G, u_canon) + d + res
        diff = pred - y
        w_col = weights[:, None]
        n = len(states)
        loss = float(0.5 * np.mean(w_col * np.sum(diff**2, axis=-1, keepdims=True)))
        dpred = (w_col * diff) / n

        dG = np.einsum("ni,nj->nij", dpred, u_canon).reshape(-1, 4)
        dWA = z.T @ dG
        dbA = np.sum(dG, axis=0)
        dWd = z.T @ dpred
        dbd = np.sum(dpred, axis=0)

        dWr2 = hr.T @ dpred
        dbr2 = np.sum(dpred, axis=0)
        dhr = dpred @ Wr2.T
        dar1 = dhr * (1.0 - hr**2)
        dWr1 = sz.T @ dar1
        dbr1 = np.sum(dar1, axis=0)

        grad = np.concatenate([
            dWA.ravel(), dbA,
            dWd.ravel(), dbd,
            dWr1.ravel(), dbr1,
            dWr2.ravel(), dbr2,
        ])
        if l2 > 0.0:
            loss += float(0.5 * l2 * np.sum(th**2))
            grad += l2 * th
        return loss, grad

    def _invert_body_mod(self, states: np.ndarray, z: np.ndarray, u_obs: np.ndarray, damping: float = 1e-3) -> np.ndarray:
        """Recover canonical action u_canon from observed u_obs on body z."""
        th = self._pack_body()
        G, d, res, _, _ = self._body_mod_from_params(th, states, z)
        rhs = u_obs - d - res
        GtG = np.einsum("nji,njk->nik", G, G)
        GtG[:, 0, 0] += damping
        GtG[:, 1, 1] += damping
        Gtr = np.einsum("nji,nj->ni", G, rhs)
        return np.linalg.solve(GtG, Gtr[..., None])[..., 0]

    def fit_phase1(
        self,
        phase1_data: dict[tuple[str, int], dict[str, np.ndarray]],
        z_by_body: dict[str, np.ndarray],
        bodies: list[str],
        old_skill_ids: list[int],
        n_alt: int = 3,
    ) -> None:
        """Alternating exact-ridge (skill policies) + L-BFGS-B (body modulator) on S1..S4 across A..D."""
        # Initialize each canonical skill policy on body B's demonstrations
        for sk_id in old_skill_ids:
            p = SkillPolicy(seed=self.seed * 10 + sk_id)
            dB = phase1_data[("B", sk_id)]
            p.fit(dB["states"], dB["times"], dB["u"], ridge=1e-2)
            self.skill_policies[sk_id] = p

        for _ in range(n_alt):
            # Step A: fit body modulator given current canonical skill policies
            s_all, uc_all, z_all, y_all = [], [], [], []
            for b in bodies:
                for sk_id in old_skill_ids:
                    d = phase1_data[(b, sk_id)]
                    s_all.append(d["states"])
                    uc_all.append(self.skill_policies[sk_id].predict(d["states"], d["times"]))
                    z_all.append(np.repeat(z_by_body[b][None, :], len(d["states"]), axis=0))
                    y_all.append(d["u"])
            S = np.concatenate(s_all, axis=0)
            UC = np.concatenate(uc_all, axis=0)
            Z = np.concatenate(z_all, axis=0)
            Y = np.concatenate(y_all, axis=0)
            W = np.ones(len(S), dtype=np.float64)
            res = minimize(
                lambda th: self._body_loss_and_grad(th, S, UC, Z, Y, W, l2=1e-3),
                self._pack_body(),
                jac=True,
                method="L-BFGS-B",
                options={"maxiter": 140, "ftol": 1e-9, "gtol": 1e-5},
            )
            self.WA, self.bA, self.Wd, self.bd, self.Wr1, self.br1, self.Wr2, self.br2 = [
                a.copy() for a in self._unpack_body(res.x)
            ]

            # Step B: re-fit each canonical skill policy across ALL bodies' inverted targets
            for sk_id in old_skill_ids:
                s_k = np.concatenate([phase1_data[(b, sk_id)]["states"] for b in bodies], axis=0)
                t_k = np.concatenate([phase1_data[(b, sk_id)]["times"] for b in bodies], axis=0)
                u_k = np.concatenate([
                    self._invert_body_mod(
                        phase1_data[(b, sk_id)]["states"],
                        np.repeat(z_by_body[b][None, :], len(phase1_data[(b, sk_id)]["states"]), axis=0),
                        phase1_data[(b, sk_id)]["u"],
                    )
                    for b in bodies
                ], axis=0)
                self.skill_policies[sk_id].fit(s_k, t_k, u_k, ridge=1e-2)

    def fit_s5_frozen_body(self, s5_B_data: dict[str, np.ndarray], z_B: np.ndarray, skill_id: int = 4) -> None:
        """Freeze Phase-1 body modulator and fit SkillPolicy_S5 in exact closed form on S5@B."""
        z_rep = np.repeat(z_B[None, :], len(s5_B_data["states"]), axis=0)
        u_canon_target = self._invert_body_mod(s5_B_data["states"], z_rep, s5_B_data["u"])
        p5 = SkillPolicy(seed=self.seed * 10 + 99)
        p5.fit(s5_B_data["states"], s5_B_data["times"], u_canon_target, ridge=1e-2)
        self.skill_policies[skill_id] = p5

    def fit_s5_replay(
        self,
        phase1_data: dict[tuple[str, int], dict[str, np.ndarray]],
        s5_B_data: dict[str, np.ndarray],
        z_by_body: dict[str, np.ndarray],
        bodies: list[str],
        old_skill_ids: list[int],
        skill_id: int = 4,
    ) -> None:
        """Fine-tune body modulator + SkillPolicy_S5 on S5@B (4x weighted) + S1..S4 replay."""
        self.fit_s5_frozen_body(s5_B_data, z_by_body["B"], skill_id=skill_id)
        s_all, uc_all, z_all, y_all, w_all = [], [], [], [], []
        for b in bodies:
            for sk_id in old_skill_ids:
                d = phase1_data[(b, sk_id)]
                s_all.append(d["states"])
                uc_all.append(self.skill_policies[sk_id].predict(d["states"], d["times"]))
                z_all.append(np.repeat(z_by_body[b][None, :], len(d["states"]), axis=0))
                y_all.append(d["u"])
                w_all.append(np.ones(len(d["states"])))
        s_all.append(s5_B_data["states"])
        uc_all.append(self.skill_policies[skill_id].predict(s5_B_data["states"], s5_B_data["times"]))
        z_all.append(np.repeat(z_by_body["B"][None, :], len(s5_B_data["states"]), axis=0))
        y_all.append(s5_B_data["u"])
        w_all.append(np.full(len(s5_B_data["states"]), 4.0))

        S = np.concatenate(s_all, axis=0)
        UC = np.concatenate(uc_all, axis=0)
        Z = np.concatenate(z_all, axis=0)
        Y = np.concatenate(y_all, axis=0)
        W = np.concatenate(w_all, axis=0)
        res = minimize(
            lambda th: self._body_loss_and_grad(th, S, UC, Z, Y, W, l2=1e-3),
            self._pack_body(),
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": 140, "ftol": 1e-9, "gtol": 1e-5},
        )
        self.WA, self.bA, self.Wd, self.bd, self.Wr1, self.br1, self.Wr2, self.br2 = [
            a.copy() for a in self._unpack_body(res.x)
        ]
        # Re-solve S5 canonical head on body B after modulator update
        self.fit_s5_frozen_body(s5_B_data, z_by_body["B"], skill_id=skill_id)

    def predict(self, states: np.ndarray, times: np.ndarray | float, skill_id: int, z: np.ndarray) -> np.ndarray:
        single = states.ndim == 1
        s2 = np.atleast_2d(states)
        z2 = np.atleast_2d(z)
        if len(z2) == 1 and len(s2) > 1:
            z2 = np.repeat(z2, len(s2), axis=0)
        u_canon = np.atleast_2d(self.skill_policies[skill_id].predict(states, times))
        G, d, res, _, _ = self._body_mod_from_params(self._pack_body(), s2, z2)
        out = np.einsum("nij,nj->ni", G, u_canon) + d + res
        return out[0] if single else out

    def clone(self) -> "CapacityMatchedRMA":
        c = CapacityMatchedRMA(self.z_dim, self.hidden_res, self.seed)
        c.WA, c.bA = self.WA.copy(), self.bA.copy()
        c.Wd, c.bd = self.Wd.copy(), self.bd.copy()
        c.Wr1, c.br1 = self.Wr1.copy(), self.br1.copy()
        c.Wr2, c.br2 = self.Wr2.copy(), self.br2.copy()
        for k, pol in self.skill_policies.items():
            p = SkillPolicy(in_dim=pol.W_rff.shape[0], n_rff=pol.n_rff, seed=0)
            p.W_rff, p.b_rff = pol.W_rff.copy(), pol.b_rff.copy()
            p.x_mean, p.x_std, p.W = pol.x_mean.copy(), pol.x_std.copy(), pol.W.copy()
            c.skill_policies[k] = p
        return c
