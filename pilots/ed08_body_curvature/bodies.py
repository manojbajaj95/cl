"""Simulated physical bodies for the ED08 body-curvature CPU pilot.

Three deterministic Lagrangian / hybrid-contact physics bodies in pure NumPy:
1. TwoLinkArm (ED01, ED02, ED05, ED07): exact 2-link planar manipulator with
   payload, actuator gains, optional voltage/command saturation, and exact
   constant-Froude dynamic-similarity scaling.
2. PlanarPusher (ED04): 2D block pushing with Coulomb stick/slip contact-mode
   switching over a (friction, object_mass) grid.
3. SLIPHopper (ED03): 2D Spring-Loaded Inverted Pendulum (SLIP) hopper with
   stance/flight gait-mode transition over a (mass, leg_length) grid.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Body 1: Exact 2-link planar manipulator arm (ED01, ED02, ED05, ED07)
# ---------------------------------------------------------------------------

def arm_dynamics_matrices(
    q: np.ndarray,
    qd: np.ndarray,
    params: dict[str, float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Exact M(q), C(q, qd)@qd, and g(q) for a 2-link planar arm with payload."""
    lam = params.get("froude_L", 1.0)
    mu = params.get("froude_M", 1.0)
    m1 = params["m1"] * mu
    m2 = params["m2"] * mu
    mp = params["mp"] * mu
    l1 = params["l1"] * lam
    l2 = params["l2"] * lam
    g = 9.81

    # Under constant-Froude policy interface, qd passed in is normalized:
    # qd_phys = qd_iface / sqrt(lam).
    if params.get("froude_time_scale", False):
        qd_phys = qd / np.sqrt(lam)
    else:
        qd_phys = qd

    q1, q2 = q[..., 0], q[..., 1]
    qd1, qd2 = qd_phys[..., 0], qd_phys[..., 1]
    c2 = np.cos(q2)
    s2 = np.sin(q2)

    I1 = (1.0 / 12.0) * m1 * l1**2
    I2 = (1.0 / 12.0) * m2 * l2**2
    lc1 = 0.5 * l1
    lc2 = 0.5 * l2

    m11 = (
        m1 * lc1**2
        + I1
        + m2 * (l1**2 + lc2**2 + 2.0 * l1 * lc2 * c2)
        + I2
        + mp * (l1**2 + l2**2 + 2.0 * l1 * l2 * c2)
    )
    m12 = m2 * (lc2**2 + l1 * lc2 * c2) + I2 + mp * (l2**2 + l1 * l2 * c2)
    m22 = m2 * lc2**2 + I2 + mp * l2**2

    h_c = -(m2 * l1 * lc2 + mp * l1 * l2) * s2
    c1 = h_c * (2.0 * qd1 * qd2 + qd2**2)
    c2_term = -h_c * (qd1**2)

    g1 = (m1 * lc1 + (m2 + mp) * l1) * g * np.cos(q1) + (
        m2 * lc2 + mp * l2
    ) * g * np.cos(q1 + q2)
    g2 = (m2 * lc2 + mp * l2) * g * np.cos(q1 + q2)

    n = q.shape[0]
    M = np.zeros((n, 2, 2), dtype=np.float64)
    M[:, 0, 0] = m11
    M[:, 0, 1] = m12
    M[:, 1, 0] = m12
    M[:, 1, 1] = m22
    C_qd = np.stack([c1, c2_term], axis=-1)
    G = np.stack([g1, g2], axis=-1)
    return M, C_qd, G


def arm_accel(
    q: np.ndarray,
    qd: np.ndarray,
    u: np.ndarray,
    params: dict[str, float],
) -> np.ndarray:
    """Compute (optionally Froude-time-rescaled) joint acceleration qdd."""
    M, C_qd, G = arm_dynamics_matrices(q, qd, params)
    K = np.array([params["k1"], params["k2"]], dtype=np.float64)
    u_max = params.get("u_max", np.inf)
    sat_mode = params.get("sat_mode", "tanh")
    if np.isfinite(u_max):
        if sat_mode == "tanh":
            u_eff = u_max * np.tanh(u / u_max)
        elif sat_mode == "clip":
            u_eff = np.clip(u, -u_max, u_max)
        else:
            raise ValueError(f"Unknown sat_mode: {sat_mode}")
    else:
        u_eff = u
    tau = u_eff * K[None, :]
    rhs = tau - C_qd - G
    qdd_phys = np.linalg.solve(M, rhs[..., None])[..., 0]
    if params.get("froude_time_scale", False):
        lam = params.get("froude_L", 1.0)
        return qdd_phys * lam
    return qdd_phys


def default_arm_params() -> dict[str, float]:
    return {
        "k1": 1.0,
        "k2": 1.0,
        "m1": 1.5,
        "m2": 1.0,
        "l1": 0.8,
        "l2": 0.7,
        "mp": 0.5,
        "froude_L": 1.0,
        "froude_M": 1.0,
        "froude_time_scale": False,
        "u_max": np.inf,
        "sat_mode": "tanh",
    }


def sample_arm_states(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    q = rng.uniform(-np.pi, np.pi, size=(n, 2))
    qd = rng.uniform(-2.0, 2.0, size=(n, 2))
    return q, qd


def default_arm_policy(q: np.ndarray, qd: np.ndarray) -> np.ndarray:
    """Smooth PD + gravity-feedforward probe policy for the 2-link arm."""
    q_tgt = np.array([0.5, -0.4])
    pd = -15.0 * (q - q_tgt[None, :]) - 3.0 * qd
    ff = np.stack([5.0 * np.cos(q[:, 0]), 2.0 * np.cos(q[:, 0] + q[:, 1])], axis=-1)
    return pd + ff


# ---------------------------------------------------------------------------
# Body 2: Planar Pusher with Coulomb stick/slip contact modes (ED04)
# ---------------------------------------------------------------------------

def pusher_accel(
    states: np.ndarray,
    u: np.ndarray,
    params: dict[str, float],
) -> np.ndarray:
    """2D planar block pushing with Coulomb stick/slip contact-mode switch.

    states: (N, 3) = [vx, vy, preload_fn]
      vx, vy: current block velocity
      preload_fn: normal preload force >= 0
    u: (N, 2) = [fx_cmd, fy_cmd] tangential push force command
    params:
      mu: Coulomb friction coefficient
      m_obj: block mass (kg)
      k_x, k_y: actuator gains
      k_stick: elastic micro-compliance in stick mode (small, keeps Jacobian invertible)
    """
    g = 9.81
    mu = params["mu"]
    m_obj = params["m_obj"]
    K = np.array([params.get("k_x", 1.0), params.get("k_y", 1.0)], dtype=np.float64)
    k_stick = params.get("k_stick", 0.05)

    v = states[:, :2]
    f_n = states[:, 2]
    f_app = u * K[None, :]
    f_norm = np.linalg.norm(f_app, axis=-1, keepdims=True)
    f_thresh = (mu * (m_obj * g + f_n))[:, None]

    # Stick mode: ||f_app|| <= f_thresh -> small elastic micro-compliance
    # Slip mode: ||f_app|| > f_thresh -> excess force accelerates block against
    # kinetic friction opposing (f_app + 0.5 * v).
    slip_dir_vec = f_app + 0.5 * v
    slip_dir = slip_dir_vec / (np.linalg.norm(slip_dir_vec, axis=-1, keepdims=True) + 1e-8)

    # Smooth transition width (very sharp, 0.02 N, preserves exact stick/slip physics)
    excess = f_norm - f_thresh
    # Softplus-like gate around the Coulomb threshold
    temp = params.get("stick_slip_temp", 0.05)
    slip_gate = 1.0 / (1.0 + np.exp(-np.clip(excess / temp, -40.0, 40.0)))

    a_stick = (k_stick / m_obj) * f_app
    a_slip = (f_app - 0.85 * f_thresh * slip_dir) / m_obj
    return (1.0 - slip_gate) * a_stick + slip_gate * a_slip


def pusher_slip_fraction(
    states: np.ndarray,
    u: np.ndarray,
    params: dict[str, float],
) -> float:
    """Fraction of ritual states in slip mode."""
    g = 9.81
    K = np.array([params.get("k_x", 1.0), params.get("k_y", 1.0)], dtype=np.float64)
    f_norm = np.linalg.norm(u * K[None, :], axis=-1)
    f_thresh = params["mu"] * (params["m_obj"] * g + states[:, 2])
    return float(np.mean(f_norm > f_thresh))


def sample_pusher_states(rng: np.random.Generator, n: int) -> np.ndarray:
    v = rng.uniform(-0.8, 0.8, size=(n, 2))
    preload = rng.uniform(0.0, 4.0, size=(n, 1))
    return np.concatenate([v, preload], axis=-1)


def default_pusher_policy(states: np.ndarray) -> np.ndarray:
    """Velocity-tracking push policy producing forces around 6-14 N."""
    v = states[:, :2]
    f_n = states[:, 2:3]
    v_tgt = np.array([[1.2, 0.4]])
    # Force magnitude centered near ~10 N so stick/slip boundary sits cleanly in grid
    return 8.0 * (v_tgt - v) + np.concatenate([2.5 + 0.3 * f_n, 1.5 - 0.2 * f_n], axis=-1)


# ---------------------------------------------------------------------------
# Body 3: 2D SLIP Hopper with gait-mode bifurcation (ED03)
# ---------------------------------------------------------------------------

def hopper_apex_map(
    states: np.ndarray,
    u: np.ndarray,
    params: dict[str, float],
) -> np.ndarray:
    """Apex-to-apex stride dynamics for a 2D SLIP hopper with gait bifurcation.

    states: (N, 2) = [v_x, y_apex] (forward velocity m/s, apex height m)
    u: (N, 2) = [alpha_td, thrust] (touchdown angle rad, stance energy thrust N*m)
    params:
      m: body mass (kg)
      l0: leg rest length (m)
      k_leg: leg spring stiffness (N/m)

    Physics:
    - Natural stance frequency omega = sqrt(k_leg / m).
    - Dimensionless load number Lambda = (m * g) / (k_leg * l0) governs whether
      the leg operates in a clean **flight-dominated bounding gait** (low Lambda:
      leg rebounds cleanly with long flight phase) or crosses into a
      **stance-dominated / bottoming trotting gait** (high Lambda >= Lambda_crit:
      leg reaches high compression, vertical impulse saturates/redirects into
      shorter, flatter double-support-like stride).
    - Ground-truth gait boundary curve in (m, l0) space is Lambda(m, l0) = Lambda_crit.
    """
    g = 9.81
    m = params["m"]
    l0 = params["l0"]
    k_leg = params.get("k_leg", 120.0)
    lam_crit = params.get("lambda_crit", 0.22)

    vx = states[:, 0]
    y_apex = states[:, 1]
    alpha = np.clip(u[:, 0], 0.05, 0.85)
    thrust = u[:, 1]

    # Dimensionless stance compression under static + dynamic load
    # Static sag: m * g / k_leg; dynamic impact energy scales with y_apex and vx^2
    omega = np.sqrt(k_leg / m)
    lam_eff = (m * g) / (k_leg * l0) + 0.06 * (vx**2 / (g * l0)) - 0.02 * (y_apex / l0)

    # Gait bifurcation gate: 0 = bounding/flight gait, 1 = stance-dominated/trot gait
    temp = params.get("gait_temp", 0.015)
    gait_gate = 1.0 / (1.0 + np.exp(-np.clip((lam_eff - lam_crit) / temp, -40.0, 40.0)))

    # Mode 0 (flight-dominated bounding): strong vertical rebound, horizontal
    # speed controlled primarily by touchdown angle alpha (Raibert-like).
    v_x_bound = vx + l0 * omega * (0.35 - alpha) + 0.12 * (thrust / (m * l0)) * np.sin(alpha)
    y_next_bound = (
        l0 * np.cos(alpha)
        + 0.45 * y_apex * (1.0 - 0.3 * lam_eff)
        + 0.30 * (thrust / (m * g)) * np.cos(alpha)
    )

    # Mode 1 (stance-dominated trotting/shuffling): high leg compression couples
    # thrust directly into forward propulsion and damps vertical apex height.
    v_x_trot = vx + 0.40 * l0 * omega * (0.20 - 0.5 * alpha) + 0.45 * (thrust / (m * np.sqrt(g * l0)))
    y_next_trot = (
        0.72 * l0
        + 0.18 * y_apex
        + 0.08 * (thrust / (m * g))
        - 0.25 * l0 * alpha
    )

    vx_next = (1.0 - gait_gate) * v_x_bound + gait_gate * v_x_trot
    y_next = (1.0 - gait_gate) * y_next_bound + gait_gate * y_next_trot
    return np.stack([vx_next, y_next], axis=-1)


def hopper_gait_fraction(
    states: np.ndarray,
    params: dict[str, float],
) -> float:
    """Fraction of states in stance-dominated trot gait (ground-truth mode label)."""
    g = 9.81
    m = params["m"]
    l0 = params["l0"]
    k_leg = params.get("k_leg", 120.0)
    lam_crit = params.get("lambda_crit", 0.22)
    vx = states[:, 0]
    y_apex = states[:, 1]
    lam_eff = (m * g) / (k_leg * l0) + 0.06 * (vx**2 / (g * l0)) - 0.02 * (y_apex / l0)
    return float(np.mean(lam_eff > lam_crit))


def sample_hopper_states(rng: np.random.Generator, n: int) -> np.ndarray:
    vx = rng.uniform(0.6, 1.8, size=(n, 1))
    y_apex = rng.uniform(0.85, 1.35, size=(n, 1))
    return np.concatenate([vx, y_apex], axis=-1)


def default_hopper_policy(states: np.ndarray) -> np.ndarray:
    """Raibert-style apex policy: touchdown angle + thrust."""
    vx = states[:, 0]
    y_apex = states[:, 1]
    alpha = np.clip(0.32 + 0.12 * (vx - 1.2), 0.10, 0.70)
    thrust = 8.0 + 4.0 * (1.1 - y_apex) + 1.5 * (1.2 - vx)
    return np.stack([alpha, thrust], axis=-1)
