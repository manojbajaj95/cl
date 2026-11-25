"""Calibrated function-space curvature estimator for body connections (ED07/ED08).

Implements:
1. Action-space body connection Gamma_act (ED20): fits affine action transport
   u_b = A u_a + b on ritual dynamics matching, with analytic OLS for
   control-affine unsaturated dynamics and Gauss-Newton / TRF least-squares
   for nonlinear/saturated/hybrid-contact dynamics.
2. Calibrated antisymmetric cross-fitted curvature estimator (ED08):
   - Uses orientation-reversed loops (gamma_+ minus gamma_-) to cancel 1D
     round-trip projection error and isolate true 2D area curvature F(u, v).
   - Splits the ritual into two disjoint halves R^(1), R^(2) and computes the
     cross-inner-product <d^(1), d^(2)> / ||pi||^2 on held-out probe states,
     which is unbiased around 0 on flat pairs even under finite-sample and
     sensor noise, and yields direct split-half reliability.
3. Policy-space transport and weight-space vs function-space comparison (ED07):
   - Two architectures (2-layer tanh MLP, random Fourier/RBF policy) and two
     optimizers (L-BFGS-B, Adam), measuring both function-space and weight-space
     curvature.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.optimize import least_squares, minimize

from bodies import arm_accel, arm_dynamics_matrices


DynamicsFn = Callable[[np.ndarray, np.ndarray, dict[str, float]], np.ndarray]


@dataclass
class LoopCurvatureResult:
    F2_cal: float
    F_cal: float
    F_half1: float
    F_half2: float
    cos_halves: float
    F_raw: float
    F_comm: float
    d_mean: np.ndarray  # (N_eval, action_dim)


def fit_arm_affine_exact(
    q: np.ndarray,
    qd: np.ndarray,
    u_a: np.ndarray,
    p_a: dict[str, float],
    p_b: dict[str, float],
    obs_noise_a: np.ndarray | None = None,
    obs_noise_b: np.ndarray | None = None,
    ridge: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact OLS fit for affine action transport on an unsaturated 2-link arm."""
    qdd_a = arm_accel(q, qd, u_a, p_a)
    if obs_noise_a is not None:
        qdd_a = qdd_a + obs_noise_a

    M_b, C_b, G_b = arm_dynamics_matrices(q, qd, p_b)
    K_b = np.array([p_b["k1"], p_b["k2"]], dtype=np.float64)
    lam_b = p_b.get("froude_L", 1.0) if p_b.get("froude_time_scale", False) else 1.0

    # qdd_b = lam_b * M_b^{-1} (K_b (A u_a + b) - C_b - G_b)
    n = len(q)
    B = lam_b * np.linalg.solve(M_b, np.broadcast_to(np.diag(K_b), (n, 2, 2)))
    y_target = qdd_a + lam_b * np.linalg.solve(M_b, (C_b + G_b)[..., None])[..., 0]
    if obs_noise_b is not None:
        # Adding observation noise to the measured acceleration on body b
        # shifts the target residual equivalently.
        y_target = y_target - obs_noise_b

    X = np.zeros((n, 2, 6), dtype=np.float64)
    X[:, :, 0] = B[:, :, 0] * u_a[:, 0:1]
    X[:, :, 1] = B[:, :, 0] * u_a[:, 1:2]
    X[:, :, 2] = B[:, :, 1] * u_a[:, 0:1]
    X[:, :, 3] = B[:, :, 1] * u_a[:, 1:2]
    X[:, :, 4] = B[:, :, 0]
    X[:, :, 5] = B[:, :, 1]

    X_flat = X.reshape(2 * n, 6)
    y_flat = y_target.reshape(2 * n)
    theta = np.linalg.solve(X_flat.T @ X_flat + ridge * np.eye(6), X_flat.T @ y_flat)
    return theta[:4].reshape(2, 2), theta[4:6]


def fit_generic_affine(
    dynamics_fn: DynamicsFn,
    states: np.ndarray,
    u_a: np.ndarray,
    p_a: dict[str, float],
    p_b: dict[str, float],
    obs_noise_a: np.ndarray | None = None,
    obs_noise_b: np.ndarray | None = None,
    init_A: np.ndarray | None = None,
    init_b: np.ndarray | None = None,
    ridge: float = 1e-6,
    max_nfev: int = 250,
) -> tuple[np.ndarray, np.ndarray]:
    """Nonlinear least-squares fit for affine action transport u_b = A u_a + b."""
    y_a = dynamics_fn(states, u_a, p_a)
    if obs_noise_a is not None:
        y_a = y_a + obs_noise_a

    act_dim = u_a.shape[1]
    A0 = np.eye(act_dim) if init_A is None else init_A.copy()
    b0 = np.zeros(act_dim) if init_b is None else init_b.copy()
    # Normalize action coordinates for well-conditioned nonlinear least squares
    u_scale = np.std(u_a, axis=0) + 1e-6
    u_a_n = u_a / u_scale[None, :]
    A0_n = (A0 * u_scale[None, :]) / u_scale[:, None]
    b0_n = b0 / u_scale
    x0 = np.concatenate([A0_n.ravel(), b0_n])
    sqrt_ridge = np.sqrt(ridge)
    id_vec = np.concatenate([np.eye(act_dim).ravel(), np.zeros(act_dim)])

    def residual(theta: np.ndarray) -> np.ndarray:
        A_n = theta[: act_dim * act_dim].reshape(act_dim, act_dim)
        b_n = theta[act_dim * act_dim :]
        u_b_n = u_a_n @ A_n.T + b_n[None, :]
        u_b = u_b_n * u_scale[None, :]
        y_b = dynamics_fn(states, u_b, p_b)
        if obs_noise_b is not None:
            y_b = y_b + obs_noise_b
        err = (y_b - y_a).ravel()
        if ridge > 0.0:
            reg = sqrt_ridge * (theta - id_vec)
            return np.concatenate([err, reg])
        return err

    sol = least_squares(residual, x0, method="trf", ftol=1e-7, xtol=1e-7, max_nfev=max_nfev)
    A_n = sol.x[: act_dim * act_dim].reshape(act_dim, act_dim)
    b_n = sol.x[act_dim * act_dim :]
    A = (A_n * u_scale[:, None]) / u_scale[None, :]
    b = b_n * u_scale
    return A, b


def _fit_step(
    body_kind: str,
    dynamics_fn: DynamicsFn | None,
    states: np.ndarray,
    u_a: np.ndarray,
    p_a: dict[str, float],
    p_b: dict[str, float],
    obs_noise_a: np.ndarray | None,
    obs_noise_b: np.ndarray | None,
) -> tuple[np.ndarray, np.ndarray]:
    if body_kind == "arm":
        q, qd = states[:, :2], states[:, 2:4]
        if not np.isfinite(p_b.get("u_max", np.inf)):
            return fit_arm_affine_exact(q, qd, u_a, p_a, p_b, obs_noise_a, obs_noise_b)
        p_b_unsat = dict(p_b, u_max=np.inf)
        A0, b0 = fit_arm_affine_exact(q, qd, u_a, p_a, p_b_unsat, obs_noise_a, obs_noise_b)
        def arm_dyn(s: np.ndarray, u: np.ndarray, p: dict[str, float]) -> np.ndarray:
            return arm_accel(s[:, :2], s[:, 2:4], u, p)
        return fit_generic_affine(
            arm_dyn, states, u_a, p_a, p_b, obs_noise_a, obs_noise_b,
            init_A=A0, init_b=b0, ridge=1e-8, max_nfev=80,
        )
    assert dynamics_fn is not None
    return fit_generic_affine(
        dynamics_fn, states, u_a, p_a, p_b, obs_noise_a, obs_noise_b,
        ridge=1e-6, max_nfev=80,
    )


def estimate_loop_curvature(
    body_kind: str,
    dynamics_fn: DynamicsFn | None,
    corners: tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]],
    du: float,
    dv: float,
    states_rit: np.ndarray,
    u_rit: np.ndarray,
    u_eval: np.ndarray,
    obs_noise_std: float = 0.0,
    rel_noise_std: float = 0.0,
    rng: np.random.Generator | None = None,
) -> LoopCurvatureResult:
    """Calibrated antisymmetric split-ritual curvature estimator in function space.

    corners = (p00, p10, p11, p01).
    Area = abs(du * dv).
    If rel_noise_std > 0, observation noise std is scaled to rel_noise_std * rms(y_00).
    """
    p00, p10, p11, p01 = corners
    area = abs(du * dv)
    n_rit = len(states_rit)
    mid = n_rit // 2
    halves = [
        (states_rit[:mid], u_rit[:mid]),
        (states_rit[mid : 2 * mid], u_rit[mid : 2 * mid]),
    ]

    eff_noise_std = obs_noise_std
    if rel_noise_std > 0.0:
        if body_kind == "arm":
            y0 = arm_accel(states_rit[:, :2], states_rit[:, 2:4], u_rit, p00)
        else:
            assert dynamics_fn is not None
            y0 = dynamics_fn(states_rit, u_rit, p00)
        y_rms = float(np.sqrt(np.mean(y0**2))) + 1e-12
        eff_noise_std = max(eff_noise_std, rel_noise_std * y_rms)

    d_halves = []
    d_raw_halves = []
    d_comm_halves = []

    for s_h, u_h in halves:
        out_dim = 2

        def _edge_noise() -> tuple[np.ndarray | None, np.ndarray | None]:
            if eff_noise_std > 0.0 and rng is not None:
                return (
                    rng.normal(0.0, eff_noise_std, size=(len(s_h), out_dim)),
                    rng.normal(0.0, eff_noise_std, size=(len(s_h), out_dim)),
                )
            return None, None

        def transport_path(path: list[dict[str, float]]) -> np.ndarray:
            ur = u_h.copy()
            ue = u_eval.copy()
            for pa, pb in zip(path[:-1], path[1:]):
                na, nb = _edge_noise()
                A, b = _fit_step(
                    body_kind, dynamics_fn, s_h, ur, pa, pb, na, nb,
                )
                ur = ur @ A.T + b[None, :]
                ue = ue @ A.T + b[None, :]
            return ue

        u_fwd = transport_path([p00, p10, p11, p01, p00])
        u_rev = transport_path([p00, p01, p11, p10, p00])
        u_uv = transport_path([p00, p10, p11])
        u_vu = transport_path([p00, p01, p11])

        d_halves.append(0.5 * (u_fwd - u_rev) / area)
        d_raw_halves.append((u_fwd - u_eval) / area)
        d_comm_halves.append((u_uv - u_vu) / area)

    d1, d2 = d_halves[0], d_halves[1]
    denom = float(np.mean(np.sum(u_eval**2, axis=-1))) + 1e-12

    F2_cal = float(np.mean(np.sum(d1 * d2, axis=-1))) / denom
    F_cal = float(np.sqrt(max(0.0, F2_cal)))
    n1 = float(np.sqrt(np.mean(np.sum(d1**2, axis=-1))))
    n2 = float(np.sqrt(np.mean(np.sum(d2**2, axis=-1))))
    norm_u = float(np.sqrt(denom))
    F_half1 = n1 / norm_u
    F_half2 = n2 / norm_u
    cos_halves = float(np.mean(np.sum(d1 * d2, axis=-1)) / (n1 * n2 + 1e-15))

    d_raw_mean = 0.5 * (d_raw_halves[0] + d_raw_halves[1])
    d_comm_mean = 0.5 * (d_comm_halves[0] + d_comm_halves[1])
    F_raw = float(np.sqrt(np.mean(np.sum(d_raw_mean**2, axis=-1)))) / norm_u
    F_comm = float(np.sqrt(np.mean(np.sum(d_comm_mean**2, axis=-1)))) / norm_u

    return LoopCurvatureResult(
        F2_cal=F2_cal,
        F_cal=F_cal,
        F_half1=F_half1,
        F_half2=F_half2,
        cos_halves=cos_halves,
        F_raw=F_raw,
        F_comm=F_comm,
        d_mean=0.5 * (d1 + d2),
    )


# ---------------------------------------------------------------------------
# ED07: Two architectures (MLP, RBF) x two optimizers (L-BFGS, Adam)
# Function-space vs weight-space curvature comparison
# ---------------------------------------------------------------------------

class MLPPolicy:
    """2-layer tanh MLP policy pi_theta(s) -> R^2 in pure NumPy."""

    def __init__(self, in_dim: int = 4, hidden: int = 24, out_dim: int = 2, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.in_dim = in_dim
        self.hidden = hidden
        self.out_dim = out_dim
        self.W1 = rng.normal(0.0, 0.4, size=(in_dim, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0.0, 0.4, size=(hidden, out_dim))
        self.b2 = np.zeros(out_dim)

    def get_params(self) -> np.ndarray:
        return np.concatenate([self.W1.ravel(), self.b1, self.W2.ravel(), self.b2])

    def set_params(self, theta: np.ndarray) -> None:
        i = 0
        n1 = self.in_dim * self.hidden
        self.W1 = theta[i : i + n1].reshape(self.in_dim, self.hidden).copy()
        i += n1
        self.b1 = theta[i : i + self.hidden].copy()
        i += self.hidden
        n2 = self.hidden * self.out_dim
        self.W2 = theta[i : i + n2].reshape(self.hidden, self.out_dim).copy()
        i += n2
        self.b2 = theta[i : i + self.out_dim].copy()

    def forward(self, x: np.ndarray, theta: np.ndarray | None = None) -> np.ndarray:
        if theta is not None:
            n1 = self.in_dim * self.hidden
            W1 = theta[:n1].reshape(self.in_dim, self.hidden)
            b1 = theta[n1 : n1 + self.hidden]
            i2 = n1 + self.hidden
            n2 = self.hidden * self.out_dim
            W2 = theta[i2 : i2 + n2].reshape(self.hidden, self.out_dim)
            b2 = theta[i2 + n2 :]
        else:
            W1, b1, W2, b2 = self.W1, self.b1, self.W2, self.b2
        h = np.tanh(x @ W1 + b1)
        return h @ W2 + b2

    def loss_and_grad_mse(
        self, theta: np.ndarray, x: np.ndarray, target_u: np.ndarray, l2_anchor: np.ndarray | None = None, l2_reg: float = 0.0
    ) -> tuple[float, np.ndarray]:
        n1 = self.in_dim * self.hidden
        W1 = theta[:n1].reshape(self.in_dim, self.hidden)
        b1 = theta[n1 : n1 + self.hidden]
        i2 = n1 + self.hidden
        n2 = self.hidden * self.out_dim
        W2 = theta[i2 : i2 + n2].reshape(self.hidden, self.out_dim)
        b2 = theta[i2 + n2 :]

        z1 = x @ W1 + b1
        h = np.tanh(z1)
        pred = h @ W2 + b2
        diff = pred - target_u
        n = x.shape[0]
        loss = float(0.5 * np.mean(np.sum(diff**2, axis=-1)))
        dpred = diff / n
        dW2 = h.T @ dpred
        db2 = np.sum(dpred, axis=0)
        dh = dpred @ W2.T
        dz1 = dh * (1.0 - h**2)
        dW1 = x.T @ dz1
        db1 = np.sum(dz1, axis=0)
        grad = np.concatenate([dW1.ravel(), db1, dW2.ravel(), db2])
        if l2_anchor is not None and l2_reg > 0.0:
            delta = theta - l2_anchor
            loss += float(0.5 * l2_reg * np.sum(delta**2))
            grad += l2_reg * delta
        return loss, grad


class RBFPolicy:
    """Random Fourier / RBF feature policy pi_theta(s) = Phi(s) @ W + b."""

    def __init__(self, in_dim: int = 4, n_feat: int = 64, out_dim: int = 2, seed: int = 0):
        rng = np.random.default_rng(seed + 1000)
        self.in_dim = in_dim
        self.n_feat = n_feat
        self.out_dim = out_dim
        self.omega = rng.normal(0.0, 0.5, size=(in_dim, n_feat))
        self.phase = rng.uniform(0.0, 2.0 * np.pi, size=(n_feat,))
        self.W = np.zeros((n_feat, out_dim))
        self.b = np.zeros(out_dim)

    def _features(self, x: np.ndarray) -> np.ndarray:
        return np.cos(x @ self.omega + self.phase) * np.sqrt(2.0 / self.n_feat)

    def get_params(self) -> np.ndarray:
        return np.concatenate([self.W.ravel(), self.b])

    def set_params(self, theta: np.ndarray) -> None:
        nw = self.n_feat * self.out_dim
        self.W = theta[:nw].reshape(self.n_feat, self.out_dim).copy()
        self.b = theta[nw:].copy()

    def forward(self, x: np.ndarray, theta: np.ndarray | None = None) -> np.ndarray:
        phi = self._features(x)
        if theta is not None:
            nw = self.n_feat * self.out_dim
            W = theta[:nw].reshape(self.n_feat, self.out_dim)
            b = theta[nw:]
        else:
            W, b = self.W, self.b
        return phi @ W + b

    def loss_and_grad_mse(
        self, theta: np.ndarray, x: np.ndarray, target_u: np.ndarray, l2_anchor: np.ndarray | None = None, l2_reg: float = 0.0
    ) -> tuple[float, np.ndarray]:
        phi = self._features(x)
        nw = self.n_feat * self.out_dim
        W = theta[:nw].reshape(self.n_feat, self.out_dim)
        b = theta[nw:]
        pred = phi @ W + b
        diff = pred - target_u
        n = x.shape[0]
        loss = float(0.5 * np.mean(np.sum(diff**2, axis=-1)))
        dpred = diff / n
        dW = phi.T @ dpred
        db = np.sum(dpred, axis=0)
        grad = np.concatenate([dW.ravel(), db])
        if l2_anchor is not None and l2_reg > 0.0:
            delta = theta - l2_anchor
            loss += float(0.5 * l2_reg * np.sum(delta**2))
            grad += l2_reg * delta
        return loss, grad


def fit_policy_to_targets(
    policy: MLPPolicy | RBFPolicy,
    theta0: np.ndarray,
    x: np.ndarray,
    target_u: np.ndarray,
    optimizer: str = "lbfgs",
    l2_reg: float = 1e-5,
) -> np.ndarray:
    """Distill target actions into policy weights using L-BFGS-B or Adam."""
    if optimizer == "lbfgs":
        res = minimize(
            lambda th: policy.loss_and_grad_mse(th, x, target_u, l2_anchor=theta0, l2_reg=l2_reg),
            theta0.copy(),
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": 200, "ftol": 1e-12, "gtol": 1e-8},
        )
        return res.x.copy()
    elif optimizer == "adam":
        th = theta0.copy()
        m = np.zeros_like(th)
        v = np.zeros_like(th)
        lr = 0.03
        beta1, beta2, eps = 0.9, 0.999, 1e-8
        for t in range(1, 301):
            _, g = policy.loss_and_grad_mse(th, x, target_u, l2_anchor=theta0, l2_reg=l2_reg)
            m = beta1 * m + (1.0 - beta1) * g
            v = beta2 * v + (1.0 - beta2) * (g * g)
            m_hat = m / (1.0 - beta1**t)
            v_hat = v / (1.0 - beta2**t)
            th = th - lr * m_hat / (np.sqrt(v_hat) + eps)
        return th
    else:
        raise ValueError(f"Unknown optimizer: {optimizer}")


def measure_ed07_arch_opt_curvature(
    policy: MLPPolicy | RBFPolicy,
    theta_init: np.ndarray,
    optimizer: str,
    corners: tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]],
    du: float,
    dv: float,
    states_rit: np.ndarray,
    states_eval: np.ndarray,
    mode: str = "action_transport_distill",
) -> dict[str, float]:
    """Compare function-space vs weight-space curvature across architectures/optimizers.

    mode == "action_transport_distill":
      At each body step pa -> pb, compute the action-space connection transport
      u_target = A u_a + b on ritual states, then update policy weights theta to
      match u_target using `optimizer`. Measure BOTH function-space F_fn and
      weight-space F_wt around the antisymmetric loop.
    mode == "full_inverse_distill":
      At each body step pa -> pb, compute the exact pointwise inverse-dynamics
      target u_target(x) on ritual states (unconstrained state-dependent
      transport), then update policy weights theta to match u_target.
      Tests whether unconstrained state-dependent transport flattens unsaturated
      mass/length/payload curvature while saturation stays curved.
    """
    p00, p10, p11, p01 = corners
    area = abs(du * dv)
    u_eval_0 = policy.forward(states_eval, theta_init)
    norm_u = float(np.sqrt(np.mean(np.sum(u_eval_0**2, axis=-1)))) + 1e-12
    norm_th = float(np.linalg.norm(theta_init)) + 1e-12

    def run_path(path: list[dict[str, float]]) -> tuple[np.ndarray, np.ndarray]:
        th = theta_init.copy()
        for pa, pb in zip(path[:-1], path[1:]):
            u_a = policy.forward(states_rit, th)
            if mode == "action_transport_distill":
                A, b = _fit_step("arm", None, states_rit, u_a, pa, pb, None, None)
                u_tgt = u_a @ A.T + b[None, :]
            elif mode == "full_inverse_distill":
                q, qd = states_rit[:, :2], states_rit[:, 2:4]
                qdd_a = arm_accel(q, qd, u_a, pa)
                M_b, C_b, G_b = arm_dynamics_matrices(q, qd, pb)
                K_b = np.array([pb["k1"], pb["k2"]], dtype=np.float64)
                tau_req = np.einsum("nij,nj->ni", M_b, qdd_a) + C_b + G_b
                u_req = tau_req / K_b[None, :]
                u_max = pb.get("u_max", np.inf)
                if np.isfinite(u_max):
                    # Invert tanh saturation where feasible; clip where saturated
                    ratio = np.clip(u_req / u_max, -0.995, 0.995)
                    u_tgt = u_max * np.arctanh(ratio)
                else:
                    u_tgt = u_req
            else:
                raise ValueError(f"Unknown mode: {mode}")
            th = fit_policy_to_targets(policy, th, states_rit, u_tgt, optimizer=optimizer, l2_reg=0.0)
        return th, policy.forward(states_eval, th)

    th_fwd, u_fwd = run_path([p00, p10, p11, p01, p00])
    th_rev, u_rev = run_path([p00, p01, p11, p10, p00])

    d_fn = 0.5 * (u_fwd - u_rev) / area
    d_wt = 0.5 * (th_fwd - th_rev) / area
    F_fn = float(np.sqrt(np.mean(np.sum(d_fn**2, axis=-1)))) / norm_u
    F_wt = float(np.linalg.norm(d_wt)) / norm_th
    return {"F_fn": F_fn, "F_wt": F_wt}
