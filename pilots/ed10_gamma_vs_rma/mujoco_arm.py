"""MuJoCo 3.x 2-link planar arm environment for ED10 (Gamma vs fairest RMA).

Provides:
- Parameterized MuJoCo 2-link vertical-plane manipulator (gravity, inertia,
  Coriolis, damping, actuator gains k1/k2, masses m1/m2, lengths l1/l2,
  end-effector payload mp, and optional torque limits).
- Two 4-body families (A, B, C, D):
    * flat: pure actuator-gain variations (unsaturated).
    * curved: joint variations of mass, link length, payload, and gains.
- Five dynamic trajectory-tracking skills:
    * S1..S4: old skills trained across A, B, C, D (Phase 1).
    * S5: new skill learned ONLY on body B (Phase 2), evaluated zero-shot on A, C, D.
- >= 1% relative Gaussian sensor noise on both ritual trajectories and
  closed-loop evaluation rollouts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import mujoco
import numpy as np


@dataclass(frozen=True)
class BodySpec:
    name: str
    m1: float = 1.0
    m2: float = 0.8
    l1: float = 0.8
    l2: float = 0.8
    mp: float = 0.2
    k1: float = 1.0
    k2: float = 1.0
    damping: float = 0.15
    u_max: float = 120.0  # actuator torque limit (Nm)


def get_body_families() -> dict[str, dict[str, BodySpec]]:
    """Return the flat (pure-gain) and curved (inertial+length+payload) 4-body families."""
    flat = {
        "A": BodySpec("A", k1=1.00, k2=1.00, u_max=200.0),
        "B": BodySpec("B", k1=0.65, k2=1.35, u_max=200.0),
        "C": BodySpec("C", k1=1.40, k2=0.70, u_max=200.0),
        "D": BodySpec("D", k1=0.75, k2=0.80, u_max=200.0),
    }
    curved = {
        "A": BodySpec("A", m1=1.0, m2=0.8, l1=0.80, l2=0.80, mp=0.20, k1=1.00, k2=1.00, u_max=250.0),
        "B": BodySpec("B", m1=1.7, m2=1.4, l1=0.85, l2=1.15, mp=0.85, k1=0.85, k2=0.85, u_max=250.0),
        "C": BodySpec("C", m1=0.6, m2=0.5, l1=0.70, l2=0.55, mp=0.05, k1=1.25, k2=1.15, u_max=250.0),
        "D": BodySpec("D", m1=0.8, m2=1.8, l1=0.75, l2=1.10, mp=1.10, k1=1.15, k2=0.75, u_max=250.0),
    }
    return {"flat": flat, "curved": curved}


def build_arm_xml(spec: BodySpec, dt: float = 0.01) -> str:
    """Build a MuJoCo MJCF string for a 2-link arm in the vertical XZ plane."""
    # Place link 1 COM at l1/2, link 2 COM at l2/2, payload sphere at tip of link 2.
    r_link = 0.035
    r_pay = 0.055
    return f"""
<mujoco model="arm2d_{spec.name}">
  <option timestep="{dt}" integrator="RK4" gravity="0 0 -9.81"/>
  <default>
    <joint type="hinge" axis="0 1 0" damping="{spec.damping}" limited="false"/>
    <geom rgba="0.3 0.6 0.8 1" contype="0" conaffinity="0"/>
  </default>
  <worldbody>
    <body name="link1" pos="0 0 0">
      <joint name="j1"/>
      <geom type="capsule" fromto="0 0 0 {spec.l1} 0 0" size="{r_link}" mass="{spec.m1}"/>
      <body name="link2" pos="{spec.l1} 0 0">
        <joint name="j2"/>
        <geom type="capsule" fromto="0 0 0 {spec.l2} 0 0" size="{r_link}" mass="{spec.m2}"/>
        <geom name="payload" type="sphere" pos="{spec.l2} 0 0" size="{r_pay}" mass="{spec.mp}"/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <motor name="m1" joint="j1" gear="{spec.k1}" ctrllimited="true" ctrlrange="{-spec.u_max} {spec.u_max}"/>
    <motor name="m2" joint="j2" gear="{spec.k2}" ctrllimited="true" ctrlrange="{-spec.u_max} {spec.u_max}"/>
  </actuator>
</mujoco>
"""


class MuJoCoArm:
    """Wrapper around a MuJoCo 2-link arm model for fast CPU simulation & inverse dynamics."""

    def __init__(self, spec: BodySpec, dt: float = 0.01):
        self.spec = spec
        self.dt = dt
        self.model = mujoco.MjModel.from_xml_string(build_arm_xml(spec, dt=dt))
        self.data = mujoco.MjData(self.model)

    def forward_accel(self, q: np.ndarray, qd: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Compute instantaneous joint acceleration qdd in MuJoCo for batch (N, 2) or single (2,)."""
        single = q.ndim == 1
        q2 = np.atleast_2d(q)
        qd2 = np.atleast_2d(qd)
        u2 = np.atleast_2d(u)
        out = np.empty_like(q2)
        for i in range(len(q2)):
            self.data.qpos[:] = q2[i]
            self.data.qvel[:] = qd2[i]
            self.data.ctrl[:] = np.clip(u2[i], -self.spec.u_max, self.spec.u_max)
            mujoco.mj_forward(self.model, self.data)
            out[i] = self.data.qacc[:]
        return out[0] if single else out

    def inverse_ctrl(self, q: np.ndarray, qd: np.ndarray, qdd_des: np.ndarray) -> np.ndarray:
        """Compute exact MuJoCo control u achieving qdd_des at (q, qd)."""
        single = q.ndim == 1
        q2 = np.atleast_2d(q)
        qd2 = np.atleast_2d(qd)
        qdd2 = np.atleast_2d(qdd_des)
        out = np.empty_like(q2)
        gear = np.array([self.spec.k1, self.spec.k2], dtype=np.float64)
        for i in range(len(q2)):
            self.data.qpos[:] = q2[i]
            self.data.qvel[:] = qd2[i]
            self.data.qacc[:] = qdd2[i]
            mujoco.mj_inverse(self.model, self.data)
            tau = self.data.qfrc_inverse[:].copy()
            out[i] = np.clip(tau / gear, -self.spec.u_max, self.spec.u_max)
        return out[0] if single else out

    def rollout(
        self,
        policy_fn: Callable[[np.ndarray, float], np.ndarray],
        q0: np.ndarray,
        qd0: np.ndarray,
        horizon: int = 80,
        sensor_noise_std: float = 0.01,
        rng: np.random.Generator | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Closed-loop MuJoCo rollout with relative Gaussian sensor noise."""
        self.data.qpos[:] = q0
        self.data.qvel[:] = qd0
        self.data.ctrl[:] = 0.0
        mujoco.mj_forward(self.model, self.data)

        qs = np.zeros((horizon + 1, 2), dtype=np.float64)
        qds = np.zeros((horizon + 1, 2), dtype=np.float64)
        us = np.zeros((horizon, 2), dtype=np.float64)
        qs[0] = self.data.qpos[:]
        qds[0] = self.data.qvel[:]

        # Characteristic RMS scales for 1% relative sensor noise
        q_scale = 1.0
        qd_scale = 2.0

        for t in range(horizon):
            q_obs = self.data.qpos[:].copy()
            qd_obs = self.data.qvel[:].copy()
            if sensor_noise_std > 0.0 and rng is not None:
                q_obs += rng.normal(0.0, sensor_noise_std * q_scale, size=2)
                qd_obs += rng.normal(0.0, sensor_noise_std * qd_scale, size=2)
            state_obs = np.concatenate([q_obs, qd_obs])
            u = np.asarray(policy_fn(state_obs, t * self.dt), dtype=np.float64)
            u = np.clip(u, -self.spec.u_max, self.spec.u_max)
            self.data.ctrl[:] = u
            mujoco.mj_step(self.model, self.data)
            us[t] = u
            qs[t + 1] = self.data.qpos[:]
            qds[t + 1] = self.data.qvel[:]
        return qs, qds, us


# ---------------------------------------------------------------------------
# Skills S1..S4 (old skills) and S5 (new skill learned only on body B)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SkillSpec:
    skill_id: int
    name: str
    q_center: tuple[float, float]
    amp: tuple[float, float]
    freq: tuple[float, float]  # rad/s
    phase: tuple[float, float]
    kp: float = 28.0
    kd: float = 8.0


def get_skills() -> list[SkillSpec]:
    """Five distinct dynamic trajectory-tracking skills.

    S1..S4 cover four quadrants of joint space; S5 is a distinct dynamic
    figure-8 swing in a high-gravity / high-coupling regime learned only on B.
    """
    return [
        SkillSpec(0, "S1", q_center=(0.6, 0.5), amp=(0.45, 0.40), freq=(3.5, 4.5), phase=(0.0, 0.4)),
        SkillSpec(1, "S2", q_center=(-0.6, 0.6), amp=(0.40, 0.45), freq=(4.0, 3.2), phase=(0.8, 0.0)),
        SkillSpec(2, "S3", q_center=(-0.5, -0.6), amp=(0.45, 0.40), freq=(3.2, 4.2), phase=(1.5, 0.7)),
        SkillSpec(3, "S4", q_center=(0.5, -0.5), amp=(0.40, 0.45), freq=(4.2, 3.5), phase=(0.3, 1.2)),
        SkillSpec(4, "S5", q_center=(0.0, 0.85), amp=(0.65, 0.55), freq=(3.6, 4.8), phase=(0.2, 1.1)),
    ]


def skill_reference(skill: SkillSpec, t: np.ndarray | float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (q_ref, qd_ref, qdd_ref) for skill at time(s) t."""
    t_arr = np.asarray(t, dtype=np.float64)
    scalar = t_arr.ndim == 0
    t_col = np.atleast_1d(t_arr)[:, None]
    qc = np.array(skill.q_center)[None, :]
    a = np.array(skill.amp)[None, :]
    w = np.array(skill.freq)[None, :]
    ph = np.array(skill.phase)[None, :]

    q_ref = qc + a * np.sin(w * t_col + ph)
    qd_ref = a * w * np.cos(w * t_col + ph)
    qdd_ref = -a * (w**2) * np.sin(w * t_col + ph)
    if scalar:
        return q_ref[0], qd_ref[0], qdd_ref[0]
    return q_ref, qd_ref, qdd_ref


def expert_desired_accel(skill: SkillSpec, q: np.ndarray, qd: np.ndarray, t: np.ndarray | float) -> np.ndarray:
    """Task-level computed-torque desired acceleration qdd_des(q, qd, t)."""
    q_ref, qd_ref, qdd_ref = skill_reference(skill, t)
    return qdd_ref + skill.kp * (q_ref - q) + skill.kd * (qd_ref - qd)


def collect_ritual_data(
    arm: MuJoCoArm,
    n_samples: int,
    sensor_noise_std: float,
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    """Collect task-agnostic free-motion ritual transitions (q, qd, u -> qdd) with sensor noise."""
    q = rng.uniform(-1.5, 1.5, size=(n_samples, 2))
    qd = rng.uniform(-3.5, 3.5, size=(n_samples, 2))
    u = rng.uniform(-40.0, 40.0, size=(n_samples, 2))
    qdd = arm.forward_accel(q, qd, u)

    q_obs = q.copy()
    qd_obs = qd.copy()
    qdd_obs = qdd.copy()
    if sensor_noise_std > 0.0:
        q_rms = float(np.sqrt(np.mean(q**2))) + 1e-8
        qd_rms = float(np.sqrt(np.mean(qd**2))) + 1e-8
        qdd_rms = float(np.sqrt(np.mean(qdd**2))) + 1e-8
        q_obs += rng.normal(0.0, sensor_noise_std * q_rms, size=q.shape)
        qd_obs += rng.normal(0.0, sensor_noise_std * qd_rms, size=qd.shape)
        qdd_obs += rng.normal(0.0, sensor_noise_std * qdd_rms, size=qdd.shape)

    return {
        "q": q_obs,
        "qd": qd_obs,
        "u": u,
        "qdd": qdd_obs,
        "q_clean": q,
        "qd_clean": qd,
        "qdd_clean": qdd,
    }


def collect_skill_data(
    arm: MuJoCoArm,
    skill: SkillSpec,
    n_episodes: int,
    horizon: int,
    sensor_noise_std: float,
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    """Collect expert demonstrations of `skill` on `arm` with noisy observations."""
    states_list, times_list, u_list = [], [], []
    for _ in range(n_episodes):
        q0_ref, qd0_ref, _ = skill_reference(skill, 0.0)
        q0 = q0_ref + rng.normal(0.0, 0.20, size=2)
        qd0 = qd0_ref + rng.normal(0.0, 0.35, size=2)

        def expert_pol(s_obs: np.ndarray, t: float) -> np.ndarray:
            qdd_des = expert_desired_accel(skill, s_obs[:2], s_obs[2:4], t)
            return arm.inverse_ctrl(s_obs[:2], s_obs[2:4], qdd_des)

        qs, qds, us = arm.rollout(expert_pol, q0, qd0, horizon=horizon, sensor_noise_std=sensor_noise_std, rng=rng)
        for t in range(horizon):
            q_o = qs[t] + (rng.normal(0.0, sensor_noise_std * 1.0, size=2) if sensor_noise_std > 0 else 0.0)
            qd_o = qds[t] + (rng.normal(0.0, sensor_noise_std * 2.0, size=2) if sensor_noise_std > 0 else 0.0)
            states_list.append(np.concatenate([q_o, qd_o]))
            times_list.append(t * arm.dt)
            u_list.append(us[t])

    return {
        "states": np.asarray(states_list, dtype=np.float64),
        "times": np.asarray(times_list, dtype=np.float64),
        "u": np.asarray(u_list, dtype=np.float64),
    }


def evaluate_policy_on_skill(
    arm: MuJoCoArm,
    skill: SkillSpec,
    policy_fn: Callable[[np.ndarray, float], np.ndarray],
    n_episodes: int = 8,
    horizon: int = 80,
    sensor_noise_std: float = 0.01,
    seed: int = 0,
) -> dict[str, float]:
    """Evaluate closed-loop tracking return and RMSE in MuJoCo with sensor noise."""
    rng = np.random.default_rng(seed)
    t_grid = np.arange(horizon + 1) * arm.dt
    q_ref, _, _ = skill_reference(skill, t_grid)

    mses = []
    returns = []
    for _ in range(n_episodes):
        q0 = q_ref[0] + rng.normal(0.0, 0.15, size=2)
        qd0_ref = skill_reference(skill, 0.0)[1]
        qd0 = qd0_ref + rng.normal(0.0, 0.25, size=2)
        qs, _, _ = arm.rollout(policy_fn, q0, qd0, horizon=horizon, sensor_noise_std=sensor_noise_std, rng=rng)
        err = qs - q_ref
        mse = float(np.mean(np.sum(err**2, axis=-1)))
        mses.append(mse)
        returns.append(float(np.exp(-mse / 0.25)))
    return {
        "return": float(np.mean(returns)),
        "rmse": float(np.sqrt(np.mean(mses))),
        "mse": float(np.mean(mses)),
    }
