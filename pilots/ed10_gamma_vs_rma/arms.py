"""ED10 Arms: Fairest RMA (FiLM-replay & FiLM-frozen-body), EB12 Conjugator, Gamma Connection, and No-Transport.

Every arm receives:
  1. The exact same task-agnostic ritual dataset per body (with >= 1% sensor noise).
  2. The exact same Phase 1 demonstrations of old skills S1..S4 across bodies A, B, C, D.
  3. The exact same Phase 2 demonstrations of new skill S5 ONLY on body B.
No arm sees ground-truth XML body parameters at training or test time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.optimize import minimize

from mujoco_arm import SkillSpec


# ---------------------------------------------------------------------------
# Shared task-agnostic feature maps (no reference trajectory leakage!)
# ---------------------------------------------------------------------------

def time_phase_features(t: np.ndarray, horizon_sec: float = 0.8) -> np.ndarray:
    """Generic Fourier time-phase encoding shared across all skills."""
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
    """Input features x(s, t) for a single-skill policy: [q, qd, sin(q), cos(q), time_phase]."""
    s2 = np.atleast_2d(states)
    q = s2[:, :2]
    qd = s2[:, 2:4]
    tf = time_phase_features(times)
    if len(tf) == 1 and len(s2) > 1:
        tf = np.repeat(tf, len(s2), axis=0)
    return np.concatenate([q, qd, np.sin(q), np.cos(q), tf], axis=-1)  # dim = 15


# ---------------------------------------------------------------------------
# Ritual-based body dynamics basis (shared by Gamma and RMA latent encoder)
# ---------------------------------------------------------------------------

class StateBasis:
    """Smooth periodic-in-q x quadratic-in-qd basis for rigid-body dynamics.

    Task-agnostic (no XML parameters, no skill information): captures the
    general structure qdd = B(q) u + f(q, qd) without RFF extrapolation blowup.
    """

    def __init__(self, n_rff: int = 0, seed: int = 0):
        self.n_rff = n_rff
        self.seed = seed

    def phi_q(self, q: np.ndarray) -> np.ndarray:
        """Periodic configuration basis phi(q) for input matrix B(q) = M(q)^{-1} K."""
        q2 = np.atleast_2d(q)
        q1, q2v = q2[:, 0:1], q2[:, 1:2]
        return np.concatenate([
            np.ones((len(q2), 1)),
            np.sin(q1), np.cos(q1),
            np.sin(q2v), np.cos(q2v),
            np.sin(q1 + q2v), np.cos(q1 + q2v),
            np.sin(2.0 * q2v), np.cos(2.0 * q2v),
            np.sin(q1 - q2v), np.cos(q1 - q2v),
        ], axis=-1)  # dim = 11

    def phi_state(self, q: np.ndarray, qd: np.ndarray) -> np.ndarray:
        """Full state basis psi(q, qd) for drift f(q, qd) = M(q)^{-1}(-C(q,qd)qd - G(q) - D qd)."""
        q2 = np.atleast_2d(q)
        qd2 = np.atleast_2d(qd)
        pq = self.phi_q(q2)  # (N, 11)
        q2v = q2[:, 1:2]
        pq_small = np.concatenate([
            np.ones((len(q2), 1)),
            np.sin(q2v), np.cos(q2v),
            np.sin(2.0 * q2v), np.cos(2.0 * q2v),
        ], axis=-1)  # (N, 5)
        qd_n = qd2 / 3.0
        v_terms = np.stack([
            qd_n[:, 0], qd_n[:, 1],
            qd_n[:, 0] ** 2, qd_n[:, 1] ** 2, qd_n[:, 0] * qd_n[:, 1],
        ], axis=-1)  # (N, 5)
        # Outer product of pq_small (5) x v_terms (5) -> 25 features
        cross = (pq_small[:, :, None] * v_terms[:, None, :]).reshape(len(q2), -1)
        return np.concatenate([pq, cross], axis=-1)  # dim = 36


@dataclass
class LearnedBodyDynamics:
    """State-dependent affine-in-control body dynamics learned purely from noisy ritual data.

    qdd_hat(q, qd, u) = B_hat(q) @ u + f_hat(q, qd)
    """
    basis: StateBasis
    W_B1: np.ndarray  # (P_q, 2) -> column 1 of B(q)
    W_B2: np.ndarray  # (P_q, 2) -> column 2 of B(q)
    W_f: np.ndarray   # (P_s, 2) -> drift f(q, qd)

    def predict_B_f(self, q: np.ndarray, qd: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        pq = self.basis.phi_q(q)
        ps = self.basis.phi_state(q, qd)
        b1 = pq @ self.W_B1  # (N, 2)
        b2 = pq @ self.W_B2  # (N, 2)
        B = np.stack([b1, b2], axis=-1)  # (N, 2, 2)
        f = ps @ self.W_f  # (N, 2)
        return B, f

    def predict_qdd(self, q: np.ndarray, qd: np.ndarray, u: np.ndarray) -> np.ndarray:
        B, f = self.predict_B_f(q, qd)
        u2 = np.atleast_2d(u)
        return np.einsum("nij,nj->ni", B, u2) + f

    def parameter_vector(self) -> np.ndarray:
        return np.concatenate([self.W_B1.ravel(), self.W_B2.ravel(), self.W_f.ravel()])


def fit_ritual_dynamics(
    ritual: dict[str, np.ndarray],
    basis: StateBasis,
    ridge_B: float = 1e-2,
    ridge_f: float = 5e-2,
) -> LearnedBodyDynamics:
    """Fit qdd = B(q) u + f(q, qd) via ridge regression on noisy ritual data."""
    q, qd, u, qdd = ritual["q"], ritual["qd"], ritual["u"], ritual["qdd"]
    pq = basis.phi_q(q)
    ps = basis.phi_state(q, qd)
    # Design matrix X = [pq * u1, pq * u2, ps]
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
    A_mat = X.T @ X + np.diag(reg)
    W = np.linalg.solve(A_mat, X.T @ qdd)  # (2*p_q + p_s, 2)
    W_B1 = W[:p_q] / u_scale
    W_B2 = W[p_q : 2 * p_q] / u_scale
    W_f = W[2 * p_q :]
    return LearnedBodyDynamics(basis=basis, W_B1=W_B1, W_B2=W_B2, W_f=W_f)


# ---------------------------------------------------------------------------
# Arm 1: Gamma Body Connection (state-dependent function-space transport)
# ---------------------------------------------------------------------------

def gamma_transport_action(
    dyn_src: LearnedBodyDynamics,
    dyn_dst: LearnedBodyDynamics,
    q: np.ndarray,
    qd: np.ndarray,
    u_src: np.ndarray,
    damping: float = 1e-3,
) -> np.ndarray:
    """Transport action u_src from body src to body dst via learned ritual connection Gamma.

    Solves B_dst(q) u_dst + f_dst(q, qd) = B_src(q) u_src + f_src(q, qd)
    with Tikhonov regularization for numerical stability under sensor noise.
    """
    single = q.ndim == 1
    q2 = np.atleast_2d(q)
    qd2 = np.atleast_2d(qd)
    u2 = np.atleast_2d(u_src)

    B_src, f_src = dyn_src.predict_B_f(q2, qd2)
    B_dst, f_dst = dyn_dst.predict_B_f(q2, qd2)
    qdd_target = np.einsum("nij,nj->ni", B_src, u2) + f_src
    rhs = qdd_target - f_dst  # (N, 2)

    # Regularized 2x2 solve: (B^T B + damping I) u_dst = B^T rhs
    BtB = np.einsum("nji,njk->nik", B_dst, B_dst)
    BtB[:, 0, 0] += damping
    BtB[:, 1, 1] += damping
    Btr = np.einsum("nji,nj->ni", B_dst, rhs)
    u_dst = np.linalg.solve(BtB, Btr[..., None])[..., 0]
    return u_dst[0] if single else u_dst


# ---------------------------------------------------------------------------
# Arm 2: EB12 Action Conjugator (flat / state-independent affine wrapper)
# ---------------------------------------------------------------------------

@dataclass
class EB12Conjugator:
    """State-independent affine action map u_dst = A u_src + b fitted from noisy rituals."""
    A: np.ndarray  # (2, 2)
    b: np.ndarray  # (2,)

    def map_action(self, u: np.ndarray) -> np.ndarray:
        single = u.ndim == 1
        u2 = np.atleast_2d(u)
        out = u2 @ self.A.T + self.b[None, :]
        return out[0] if single else out


def fit_eb12_conjugator(
    dyn_src: LearnedBodyDynamics,
    dyn_dst: LearnedBodyDynamics,
    ritual_src: dict[str, np.ndarray],
) -> EB12Conjugator:
    """Fit best global state-independent affine map u_dst = A u_src + b matching ritual qdd."""
    q = ritual_src["q"]
    qd = ritual_src["qd"]
    u_src = ritual_src["u"]
    u_dst_target = gamma_transport_action(dyn_src, dyn_dst, q, qd, u_src, damping=1e-2)
    # Least-squares fit u_dst_target ~ [u_src, 1] @ [A^T; b^T]
    X = np.concatenate([u_src, np.ones((len(u_src), 1))], axis=1)
    W, _, _, _ = np.linalg.lstsq(X, u_dst_target, rcond=None)
    A = W[:2, :].T.copy()
    b = W[2, :].copy()
    return EB12Conjugator(A=A, b=b)


# ---------------------------------------------------------------------------
# Skill Policy (RBF/Fourier Ridge Policy for Gamma, EB12, No-Transport)
# ---------------------------------------------------------------------------

class SkillPolicy:
    """Smooth nonlinear skill policy pi(s, t) = Phi(x(s, t)) @ W + b trained by ridge regression."""

    def __init__(self, in_dim: int = 15, n_feat: int = 160, seed: int = 0):
        rng = np.random.default_rng(seed + 4242)
        self.W_rff = rng.normal(0.0, 0.35, size=(in_dim, n_feat))
        self.b_rff = rng.uniform(0.0, 2.0 * np.pi, size=(n_feat,))
        self.n_feat = n_feat
        self.W = np.zeros((in_dim + n_feat + 1, 2))
        self.x_mean = np.zeros(in_dim)
        self.x_std = np.ones(in_dim)

    def _phi(self, x: np.ndarray) -> np.ndarray:
        xn = (x - self.x_mean) / self.x_std
        rff = np.cos(xn @ self.W_rff + self.b_rff) * np.sqrt(2.0 / self.n_feat)
        return np.concatenate([xn, rff, np.ones((len(x), 1))], axis=1)

    def fit(self, states: np.ndarray, times: np.ndarray, targets_u: np.ndarray, ridge: float = 1e-2) -> None:
        x = skill_input_features(states, times)
        self.x_mean = np.mean(x, axis=0)
        self.x_std = np.std(x, axis=0) + 1e-6
        P = self._phi(x)
        reg = ridge * np.eye(P.shape[1])
        reg[-1, -1] = 1e-8
        self.W = np.linalg.solve(P.T @ P + reg, P.T @ targets_u)

    def predict(self, states: np.ndarray, times: np.ndarray | float) -> np.ndarray:
        single = states.ndim == 1
        s2 = np.atleast_2d(states)
        t_arr = np.full(len(s2), float(times)) if np.ndim(times) == 0 else np.asarray(times, dtype=np.float64)
        x = skill_input_features(s2, t_arr)
        out = self._phi(x) @ self.W
        return out[0] if single else out


# ---------------------------------------------------------------------------
# Arm 3: Fairest Matched RMA (Ritual-Trained Body Latent + FiLM Policy)
# ---------------------------------------------------------------------------

def extract_rma_body_latents(
    dynamics_by_body: dict[str, LearnedBodyDynamics],
    n_probe: int = 64,
    latent_dim: int = 6,
    seed: int = 0,
) -> dict[str, np.ndarray]:
    """Compute ritual-derived body latent z_b for each body via SVD of ritual acceleration responses.

    Uses ONLY the noisy ritual dynamics of each body (no ground-truth XML parameters),
    producing a maximally informative, standardized low-dimensional body latent z_b.
    """
    rng = np.random.default_rng(seed + 9090)
    q_p = rng.uniform(-1.2, 1.2, size=(n_probe, 2))
    qd_p = rng.uniform(-2.5, 2.5, size=(n_probe, 2))
    u_p = rng.uniform(-20.0, 20.0, size=(n_probe, 2))

    body_names = sorted(dynamics_by_body.keys())
    resp = np.stack([dynamics_by_body[b].predict_qdd(q_p, qd_p, u_p).ravel() for b in body_names], axis=0)
    resp_centered = resp - np.mean(resp, axis=0, keepdims=True)
    U, S, _ = np.linalg.svd(resp_centered, full_matrices=False)
    k = min(latent_dim, U.shape[1])
    Z = U[:, :k] * S[:k]
    # Standardize each active latent dimension to unit scale
    std = np.std(Z, axis=0, keepdims=True) + 1e-6
    Z = Z / std
    if k < latent_dim:
        Z = np.concatenate([Z, np.zeros((len(body_names), latent_dim - k))], axis=1)
    return {b: Z[i].copy() for i, b in enumerate(body_names)}


class RMAFiLMPolicy:
    """Fairest RMA policy: shared skill trunk + hidden FiLM + output 2x2 body affine head.

    Architecture:
      h1 = tanh(x_skill @ W1 + b1)                    # skill trunk (in_dim -> H)
      gamma = 1 + z @ Wg + bg,  beta = z @ Wb + bb    # hidden body FiLM modulator (z_dim -> H)
      h2 = tanh(gamma * h1 + beta)
      u_base = h2 @ W2 + b2                           # canonical skill action (N, 2)
      G_out(z) = I + reshape(z @ WA + bA, (2, 2))     # body-conditioned 2x2 output gain
      d_out(z) = z @ Wd + bd                          # body-conditioned output bias
      u = G_out(z) @ u_base + d_out(z)

    This strictly subsumes both standard FiLM-RMA and flat EB12 action conjugation:
    on a flat actuator-gain family, G_out(z) can represent exact zero-shot S5 transfer!
    Supports TWO fair Phase-2 fine-tuning modes when learning S5 only on body B:
      - 'replay': fine-tune ALL parameters on S5@B + S1..S4 replay across A..D.
      - 'frozen_body': freeze the body modulators (Wg, bg, Wb, bb, WA, bA, Wd, bd) learned on
        S1..S4 across A..D and fine-tune ONLY the skill trunk + readout on S5@B + S1..S4 replay.
    """

    def __init__(self, in_dim: int = 20, z_dim: int = 6, hidden: int = 48, out_dim: int = 2, seed: int = 0):
        rng = np.random.default_rng(seed + 3141)
        self.in_dim = in_dim
        self.z_dim = z_dim
        self.hidden = hidden
        self.out_dim = out_dim

        self.W1 = rng.normal(0.0, np.sqrt(2.0 / (in_dim + hidden)), size=(in_dim, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0.0, np.sqrt(2.0 / (hidden + out_dim)), size=(hidden, out_dim))
        self.b2 = np.zeros(out_dim)
        # Body modulators (hidden FiLM + 2x2 output affine head)
        self.Wg = rng.normal(0.0, 0.05, size=(z_dim, hidden))
        self.bg = np.zeros(hidden)
        self.Wb = rng.normal(0.0, 0.05, size=(z_dim, hidden))
        self.bb = np.zeros(hidden)
        self.WA = rng.normal(0.0, 0.05, size=(z_dim, out_dim * out_dim))
        self.bA = np.zeros(out_dim * out_dim)
        self.Wd = rng.normal(0.0, 0.05, size=(z_dim, out_dim))
        self.bd = np.zeros(out_dim)
        self.x_mean = np.zeros(in_dim)
        self.x_std = np.ones(in_dim)

    def _pack(self, include_body: bool = True) -> np.ndarray:
        parts = [self.W1.ravel(), self.b1, self.W2.ravel(), self.b2]
        if include_body:
            parts.extend([
                self.Wg.ravel(), self.bg,
                self.Wb.ravel(), self.bb,
                self.WA.ravel(), self.bA,
                self.Wd.ravel(), self.bd,
            ])
        return np.concatenate(parts)

    def _unpack(self, theta: np.ndarray, include_body: bool = True):
        i = 0
        n1 = self.in_dim * self.hidden
        W1 = theta[i : i + n1].reshape(self.in_dim, self.hidden); i += n1
        b1 = theta[i : i + self.hidden]; i += self.hidden
        n2 = self.hidden * self.out_dim
        W2 = theta[i : i + n2].reshape(self.hidden, self.out_dim); i += n2
        b2 = theta[i : i + self.out_dim]; i += self.out_dim
        if include_body:
            ng = self.z_dim * self.hidden
            Wg = theta[i : i + ng].reshape(self.z_dim, self.hidden); i += ng
            bg = theta[i : i + self.hidden]; i += self.hidden
            Wb = theta[i : i + ng].reshape(self.z_dim, self.hidden); i += ng
            bb = theta[i : i + self.hidden]; i += self.hidden
            nA = self.z_dim * self.out_dim * self.out_dim
            WA = theta[i : i + nA].reshape(self.z_dim, self.out_dim * self.out_dim); i += nA
            bA = theta[i : i + self.out_dim * self.out_dim]; i += self.out_dim * self.out_dim
            nd = self.z_dim * self.out_dim
            Wd = theta[i : i + nd].reshape(self.z_dim, self.out_dim); i += nd
            bd = theta[i : i + self.out_dim]; i += self.out_dim
        else:
            Wg, bg, Wb, bb = self.Wg, self.bg, self.Wb, self.bb
            WA, bA, Wd, bd = self.WA, self.bA, self.Wd, self.bd
        return W1, b1, W2, b2, Wg, bg, Wb, bb, WA, bA, Wd, bd

    def _set_from_theta(self, theta: np.ndarray, include_body: bool = True) -> None:
        W1, b1, W2, b2, Wg, bg, Wb, bb, WA, bA, Wd, bd = self._unpack(theta, include_body)
        self.W1, self.b1, self.W2, self.b2 = W1.copy(), b1.copy(), W2.copy(), b2.copy()
        if include_body:
            self.Wg, self.bg, self.Wb, self.bb = Wg.copy(), bg.copy(), Wb.copy(), bb.copy()
            self.WA, self.bA, self.Wd, self.bd = WA.copy(), bA.copy(), Wd.copy(), bd.copy()

    def _loss_and_grad(
        self,
        theta: np.ndarray,
        xn: np.ndarray,
        z: np.ndarray,
        y: np.ndarray,
        weights: np.ndarray,
        l2_reg: float,
        include_body: bool,
    ) -> tuple[float, np.ndarray]:
        W1, b1, W2, b2, Wg, bg, Wb, bb, WA, bA, Wd, bd = self._unpack(theta, include_body)
        D = self.out_dim
        a1 = xn @ W1 + b1
        h1 = np.tanh(a1)
        gamma = 1.0 + z @ Wg + bg
        beta = z @ Wb + bb
        a2 = gamma * h1 + beta
        h2 = np.tanh(a2)
        u_base = h2 @ W2 + b2  # (N, D)

        # Output 2x2 affine body head
        G_flat = z @ WA + bA  # (N, D*D)
        G = np.eye(D)[None, :, :] + G_flat.reshape(-1, D, D)  # (N, D, D)
        d_out = z @ Wd + bd  # (N, D)
        pred = np.einsum("nij,nj->ni", G, u_base) + d_out  # (N, D)

        diff = pred - y
        w_col = weights[:, None]
        loss = float(0.5 * np.mean(w_col * np.sum(diff**2, axis=-1, keepdims=True)))
        dpred = (w_col * diff) / len(xn)  # (N, D)

        # Backprop through output body head
        du_base = np.einsum("nji,nj->ni", G, dpred)  # (N, D)
        dW2 = h2.T @ du_base
        db2 = np.sum(du_base, axis=0)
        dh2 = du_base @ W2.T
        da2 = dh2 * (1.0 - h2**2)

        dh1 = da2 * gamma
        da1 = dh1 * (1.0 - h1**2)
        dW1 = xn.T @ da1
        db1 = np.sum(da1, axis=0)

        parts = [dW1.ravel(), db1, dW2.ravel(), db2]
        if include_body:
            dgamma = da2 * h1
            dWg = z.T @ dgamma
            dbg = np.sum(dgamma, axis=0)
            dWb = z.T @ da2
            dbb = np.sum(da2, axis=0)

            dG = np.einsum("ni,nj->nij", dpred, u_base).reshape(-1, D * D)
            dWA = z.T @ dG
            dbA = np.sum(dG, axis=0)
            dWd = z.T @ dpred
            dbd = np.sum(dpred, axis=0)
            parts.extend([
                dWg.ravel(), dbg,
                dWb.ravel(), dbb,
                dWA.ravel(), dbA,
                dWd.ravel(), dbd,
            ])

        grad = np.concatenate(parts)
        if l2_reg > 0.0:
            loss += float(0.5 * l2_reg * np.sum(theta**2))
            grad += l2_reg * theta
        return loss, grad

    def fit(
        self,
        x_raw: np.ndarray,
        z: np.ndarray,
        y: np.ndarray,
        sample_weights: np.ndarray | None = None,
        l2_reg: float = 1e-4,
        maxiter: int = 250,
        include_body: bool = True,
        refit_norm: bool = True,
    ) -> None:
        if refit_norm:
            self.x_mean = np.mean(x_raw, axis=0)
            self.x_std = np.std(x_raw, axis=0) + 1e-6
        xn = (x_raw - self.x_mean) / self.x_std
        w = np.ones(len(xn), dtype=np.float64) if sample_weights is None else sample_weights
        theta0 = self._pack(include_body=include_body)
        res = minimize(
            lambda th: self._loss_and_grad(th, xn, z, y, w, l2_reg, include_body),
            theta0,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": 1e-10, "gtol": 1e-6},
        )
        self._set_from_theta(res.x, include_body=include_body)

    def predict(self, x_raw: np.ndarray, z: np.ndarray) -> np.ndarray:
        single = x_raw.ndim == 1
        x2 = np.atleast_2d(x_raw)
        z2 = np.atleast_2d(z)
        if len(z2) == 1 and len(x2) > 1:
            z2 = np.repeat(z2, len(x2), axis=0)
        xn = (x2 - self.x_mean) / self.x_std
        h1 = np.tanh(xn @ self.W1 + self.b1)
        gamma = 1.0 + z2 @ self.Wg + self.bg
        beta = z2 @ self.Wb + self.bb
        h2 = np.tanh(gamma * h1 + beta)
        u_base = h2 @ self.W2 + self.b2
        D = self.out_dim
        G = np.eye(D)[None, :, :] + (z2 @ self.WA + self.bA).reshape(-1, D, D)
        d_out = z2 @ self.Wd + self.bd
        out = np.einsum("nij,nj->ni", G, u_base) + d_out
        return out[0] if single else out

    def clone(self) -> "RMAFiLMPolicy":
        c = RMAFiLMPolicy(self.in_dim, self.z_dim, self.hidden, self.out_dim, seed=0)
        c.W1, c.b1 = self.W1.copy(), self.b1.copy()
        c.W2, c.b2 = self.W2.copy(), self.b2.copy()
        c.Wg, c.bg = self.Wg.copy(), self.bg.copy()
        c.Wb, c.bb = self.Wb.copy(), self.bb.copy()
        c.WA, c.bA = self.WA.copy(), self.bA.copy()
        c.Wd, c.bd = self.Wd.copy(), self.bd.copy()
        c.x_mean, c.x_std = self.x_mean.copy(), self.x_std.copy()
        return c


def make_rma_input(states: np.ndarray, times: np.ndarray, skill_id: int, n_skills: int = 5) -> np.ndarray:
    """Concatenate skill_input_features (15) + skill one-hot (5) -> dim 20."""
    base = skill_input_features(states, times)
    oh = np.zeros((len(base), n_skills), dtype=np.float64)
    oh[:, skill_id] = 1.0
    return np.concatenate([base, oh], axis=-1)
