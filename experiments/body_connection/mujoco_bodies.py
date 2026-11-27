"""MuJoCo 3.x 2-link arm families for ED10b: flat, curved, contact, and mixed.

All four families run on CPU in MuJoCo 3.x with RK4 integration (dt=0.01s) and
>= 1% relative Gaussian sensor noise on (q, qd) during rollouts and on
(q, qd, qdd) during task-agnostic ritual collection.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import mujoco
import numpy as np


@dataclass(frozen=True)
class BodySpec:
    """Physical specification of a MuJoCo 2-link vertical-plane arm (optional unilateral contact wall)."""
    name: str
    m1: float = 1.0
    m2: float = 0.8
    l1: float = 0.8
    l2: float = 0.8
    mp: float = 0.2
    k1: float = 1.0
    k2: float = 1.0
    damping: float = 0.15
    u_max: float = 250.0
    wall_x: float | None = None
    wall_solref_t: float = 0.12
    wall_fric: float = 0.6


def get_body_families() -> dict[str, dict[str, BodySpec]]:
    """Return the four ED10b MuJoCo body families: flat, curved, contact, and mixed."""
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
    # Contact family: unilateral MuJoCo wall (condim=3, normal + Coulomb friction)
    # placed so arm trajectories actively cross between free space (ncon=0) and contact (ncon=1),
    # with varying wall compliance, friction, wall offset, inertia, and actuator gains.
    contact = {
        "A": BodySpec("A", m1=1.0, m2=0.8, l1=0.80, l2=0.80, mp=0.25, k1=1.00, k2=1.00, u_max=300.0,
                      wall_x=0.55, wall_solref_t=-4.0, wall_fric=0.45),
        "B": BodySpec("B", m1=1.5, m2=1.2, l1=0.85, l2=1.00, mp=0.65, k1=0.85, k2=0.90, u_max=300.0,
                      wall_x=0.60, wall_solref_t=-5.5, wall_fric=0.85),
        "C": BodySpec("C", m1=0.7, m2=0.6, l1=0.75, l2=0.65, mp=0.10, k1=1.25, k2=1.15, u_max=300.0,
                      wall_x=0.48, wall_solref_t=-3.2, wall_fric=0.30),
        "D": BodySpec("D", m1=0.9, m2=1.5, l1=0.75, l2=0.95, mp=0.85, k1=1.10, k2=0.80, u_max=300.0,
                      wall_x=0.58, wall_solref_t=-6.5, wall_fric=0.95),
    }
    # Mixed family: source body B plus 3 pure-flat targets (F1, F2, F3: only k1, k2 differ from B)
    # and 3 curved targets (C1, C2, C3: mass, length, payload, and gains differ from B).
    b_mix = BodySpec("B", m1=1.3, m2=1.1, l1=0.85, l2=0.95, mp=0.50, k1=0.85, k2=1.05, u_max=250.0)
    mixed = {
        "B": b_mix,
        "F1": BodySpec("F1", m1=1.3, m2=1.1, l1=0.85, l2=0.95, mp=0.50, k1=1.35, k2=0.65, u_max=250.0),
        "F2": BodySpec("F2", m1=1.3, m2=1.1, l1=0.85, l2=0.95, mp=0.50, k1=0.60, k2=1.45, u_max=250.0),
        "F3": BodySpec("F3", m1=1.3, m2=1.1, l1=0.85, l2=0.95, mp=0.50, k1=1.15, k2=1.35, u_max=250.0),
        "C1": BodySpec("C1", m1=0.6, m2=0.5, l1=0.70, l2=0.55, mp=0.05, k1=1.25, k2=1.15, u_max=250.0),
        "C2": BodySpec("C2", m1=0.8, m2=1.8, l1=0.75, l2=1.10, mp=1.10, k1=1.15, k2=0.75, u_max=250.0),
        "C3": BodySpec("C3", m1=1.8, m2=0.7, l1=1.00, l2=0.70, mp=0.90, k1=0.75, k2=1.25, u_max=250.0),
    }
    return {"flat": flat, "curved": curved, "contact": contact, "mixed": mixed}


def build_arm_xml(spec: BodySpec, dt: float = 0.01) -> str:
    """Build MuJoCo MJCF XML for a 2-link vertical-plane arm (with optional unilateral contact wall)."""
    wall_xml = ""
    tip_contact = 'contype="0" conaffinity="0"'
    if spec.wall_x is not None:
        sr = f"{spec.wall_solref_t} -4.0" if spec.wall_solref_t < 0 else f"{spec.wall_solref_t} 1.0"
        wall_xml = (
            f'    <geom name="wall" type="box" pos="{spec.wall_x + 1.0} 0 0" size="1.0 0.5 2.5"\n'
            f'          contype="1" conaffinity="1" condim="3"\n'
            f'          friction="{spec.wall_fric} 0.005 0.0001" solref="{sr}" solimp="0.04 0.14 0.30"/>\n'
        )
        tip_contact = (
            f'contype="1" conaffinity="1" condim="3"\n'
            f'              friction="{spec.wall_fric} 0.005 0.0001" solref="{sr}" solimp="0.04 0.14 0.30"'
        )
    return f"""
<mujoco model="arm_{spec.name}">
  <option timestep="{dt}" integrator="RK4" gravity="0 0 -9.81"/>
  <worldbody>
{wall_xml}    <body name="link1" pos="0 0 0">
      <joint name="j1" type="hinge" axis="0 1 0" damping="{spec.damping}"/>
      <geom name="g1" type="capsule" fromto="0 0 0 0 0 -{spec.l1}" size="0.035" mass="{spec.m1}" contype="0" conaffinity="0"/>
      <body name="link2" pos="0 0 -{spec.l1}">
        <joint name="j2" type="hinge" axis="0 1 0" damping="{spec.damping}"/>
        <geom name="g2" type="capsule" fromto="0 0 0 0 0 -{spec.l2}" size="0.03" mass="{spec.m2}" contype="0" conaffinity="0"/>
        <geom name="tip" type="sphere" pos="0 0 -{spec.l2}" size="0.05" mass="{spec.mp}" {tip_contact}/>
      </body>
    </body>
  </worldbody>
  <actuator>
    <motor name="m1" joint="j1" gear="{spec.k1}" ctrllimited="true" ctrlrange="-{spec.u_max} {spec.u_max}"/>
    <motor name="m2" joint="j2" gear="{spec.k2}" ctrllimited="true" ctrlrange="-{spec.u_max} {spec.u_max}"/>
  </actuator>
</mujoco>
"""


class MuJoCoArm:
    """Thin CPU MuJoCo 3.x simulator wrapper for a 2-link arm body."""

    def __init__(self, spec: BodySpec, dt: float = 0.01):
        self.spec = spec
        self.dt = dt
        self.model = mujoco.MjModel.from_xml_string(build_arm_xml(spec, dt=dt))
        self.data = mujoco.MjData(self.model)
        self.gear = np.array([spec.k1, spec.k2], dtype=np.float64)
        self.u_max = float(spec.u_max)

    def forward_accel(self, q: np.ndarray, qd: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Compute instantaneous MuJoCo forward acceleration qdd = f(q, qd, u) (incl. contact forces)."""
        q2 = np.atleast_2d(q)
        qd2 = np.atleast_2d(qd)
        u2 = np.atleast_2d(u)
        out = np.empty((len(q2), 2), dtype=np.float64)
        for i in range(len(q2)):
            self.data.qpos[:] = q2[i]
            self.data.qvel[:] = qd2[i]
            self.data.ctrl[:] = np.clip(u2[i], -self.u_max, self.u_max)
            mujoco.mj_forward(self.model, self.data)
            out[i] = self.data.qacc
        return out[0] if q.ndim == 1 else out

    def inverse_ctrl(self, q: np.ndarray, qd: np.ndarray, qdd_des: np.ndarray) -> np.ndarray:
        """Compute exact MuJoCo inverse control u achieving desired acceleration qdd_des."""
        self.data.qpos[:] = q
        self.data.qvel[:] = qd
        self.data.qacc[:] = qdd_des
        mujoco.mj_inverse(self.model, self.data)
        u = self.data.qfrc_inverse / self.gear
        return np.clip(u, -self.u_max, self.u_max)

    def rollout(
        self,
        policy_fn: Callable[[np.ndarray, float], np.ndarray],
        q0: np.ndarray,
        qd0: np.ndarray,
        horizon: int = 80,
        sensor_noise_std: float = 0.01,
        rng: np.random.Generator | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Run closed-loop MuJoCo rollout with relative Gaussian sensor noise on (q, qd).

        Returns (qs, qds, us, contact_frac).
        """
        if rng is None:
            rng = np.random.default_rng(0)
        self.data.qpos[:] = q0
        self.data.qvel[:] = qd0
        self.data.ctrl[:] = 0.0
        mujoco.mj_forward(self.model, self.data)

        qs = np.empty((horizon, 2), dtype=np.float64)
        qds = np.empty((horizon, 2), dtype=np.float64)
        us = np.empty((horizon, 2), dtype=np.float64)
        q_scale = 0.8
        qd_scale = 2.5
        n_contacts = 0

        for step in range(horizon):
            t = step * self.dt
            q_true = self.data.qpos.copy()
            qd_true = self.data.qvel.copy()
            qs[step] = q_true
            qds[step] = qd_true
            if self.data.ncon > 0:
                n_contacts += 1

            q_obs = q_true.copy()
            qd_obs = qd_true.copy()
            if sensor_noise_std > 0.0:
                q_obs += rng.normal(0.0, sensor_noise_std * q_scale, size=2)
                qd_obs += rng.normal(0.0, sensor_noise_std * qd_scale, size=2)

            state_obs = np.concatenate([q_obs, qd_obs])
            u_cmd = np.asarray(policy_fn(state_obs, t), dtype=np.float64)
            u_cmd = np.nan_to_num(u_cmd, nan=0.0, posinf=self.u_max, neginf=-self.u_max)
            u_cmd = np.clip(u_cmd, -self.u_max, self.u_max)
            us[step] = u_cmd

            self.data.ctrl[:] = u_cmd
            mujoco.mj_step(self.model, self.data)
            if not (np.all(np.isfinite(self.data.qpos)) and np.all(np.abs(self.data.qpos) < 50.0)):
                # Abort unstable rollout cleanly with penalty coordinates
                qs[step + 1 :] = 10.0
                qds[step + 1 :] = 0.0
                us[step + 1 :] = 0.0
                break

        return qs, qds, us, n_contacts / float(horizon)


@dataclass(frozen=True)
class SkillSpec:
    skill_id: int
    name: str
    q_center: tuple[float, float]
    amp: tuple[float, float]
    freq: tuple[float, float]
    phase: tuple[float, float]
    kp: float = 28.0
    kd: float = 8.0


def get_skills(contact_family: bool = False) -> list[SkillSpec]:
    """Five distinct dynamic trajectory-tracking skills.

    For the contact family, S5 swings across x = wall_x (q1 negative -> positive x tip)
    so the arm actively enters and exits physical MuJoCo contact during execution.
    """
    if contact_family:
        return [
            SkillSpec(0, "S1", q_center=(0.5, 0.4), amp=(0.40, 0.35), freq=(3.5, 4.5), phase=(0.0, 0.4)),
            SkillSpec(1, "S2", q_center=(-0.45, 0.3), amp=(0.35, 0.35), freq=(4.0, 3.2), phase=(0.8, 0.0)),
            SkillSpec(2, "S3", q_center=(0.0, -0.35), amp=(0.30, 0.30), freq=(3.2, 4.2), phase=(1.5, 0.7)),
            SkillSpec(3, "S4", q_center=(0.45, -0.45), amp=(0.40, 0.40), freq=(4.2, 3.5), phase=(0.3, 1.2)),
            SkillSpec(4, "S5", q_center=(-0.35, -0.15), amp=(0.40, 0.35), freq=(3.5, 4.5), phase=(0.2, 1.1)),
        ]
    return [
        SkillSpec(0, "S1", q_center=(0.6, 0.5), amp=(0.45, 0.40), freq=(3.5, 4.5), phase=(0.0, 0.4)),
        SkillSpec(1, "S2", q_center=(-0.6, 0.6), amp=(0.40, 0.45), freq=(4.0, 3.2), phase=(0.8, 0.0)),
        SkillSpec(2, "S3", q_center=(-0.5, -0.6), amp=(0.45, 0.40), freq=(3.2, 4.2), phase=(1.5, 0.7)),
        SkillSpec(3, "S4", q_center=(0.5, -0.5), amp=(0.40, 0.45), freq=(4.2, 3.5), phase=(0.3, 1.2)),
        SkillSpec(4, "S5", q_center=(0.0, 0.85), amp=(0.65, 0.55), freq=(3.6, 4.8), phase=(0.2, 1.1)),
    ]


def skill_reference(skill: SkillSpec, t: np.ndarray | float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    q_ref, qd_ref, qdd_ref = skill_reference(skill, t)
    return qdd_ref + skill.kp * (q_ref - q) + skill.kd * (qd_ref - qd)


def collect_ritual_data(
    arm: MuJoCoArm,
    n_samples: int,
    sensor_noise_std: float,
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    """Collect task-agnostic ritual transitions (q, qd, u -> qdd) with relative Gaussian sensor noise."""
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
    states_list, times_list, u_list = [], [], []
    for _ in range(n_episodes):
        q0_ref, qd0_ref, _ = skill_reference(skill, 0.0)
        q0 = q0_ref + rng.normal(0.0, 0.18, size=2)
        qd0 = qd0_ref + rng.normal(0.0, 0.30, size=2)

        def expert_pol(s_obs: np.ndarray, t: float) -> np.ndarray:
            qdd_des = expert_desired_accel(skill, s_obs[:2], s_obs[2:4], t)
            return arm.inverse_ctrl(s_obs[:2], s_obs[2:4], qdd_des)

        qs, qds, us, _ = arm.rollout(expert_pol, q0, qd0, horizon=horizon, sensor_noise_std=sensor_noise_std, rng=rng)
        q_obs = qs + rng.normal(0.0, sensor_noise_std * 0.8, size=qs.shape) if sensor_noise_std > 0 else qs
        qd_obs = qds + rng.normal(0.0, sensor_noise_std * 2.5, size=qds.shape) if sensor_noise_std > 0 else qds
        states_list.append(np.concatenate([q_obs, qd_obs], axis=1))
        times_list.append(np.arange(horizon, dtype=np.float64) * arm.dt)
        u_list.append(us)

    return {
        "states": np.concatenate(states_list, axis=0),
        "times": np.concatenate(times_list, axis=0),
        "u": np.concatenate(u_list, axis=0),
    }


def evaluate_policy_on_skill(
    arm: MuJoCoArm,
    skill: SkillSpec,
    policy_fn: Callable[[np.ndarray, float], np.ndarray],
    n_episodes: int = 6,
    horizon: int = 80,
    sensor_noise_std: float = 0.01,
    seed: int = 0,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    ts = np.arange(horizon, dtype=np.float64) * arm.dt
    q_ref, _, _ = skill_reference(skill, ts)

    returns, rmses, contact_fracs = [], [], []
    for _ in range(n_episodes):
        q0_ref, qd0_ref, _ = skill_reference(skill, 0.0)
        q0 = q0_ref + rng.normal(0.0, 0.12, size=2)
        qd0 = qd0_ref + rng.normal(0.0, 0.20, size=2)
        qs, _, _, cf = arm.rollout(policy_fn, q0, qd0, horizon=horizon, sensor_noise_std=sensor_noise_std, rng=rng)
        mse = float(np.mean((qs - q_ref) ** 2))
        rmse = float(np.sqrt(mse))
        ret = float(np.exp(-4.0 * min(mse, 25.0)))
        returns.append(ret)
        rmses.append(rmse)
        contact_fracs.append(cf)

    return {
        "return": float(np.mean(returns)),
        "rmse": float(np.mean(rmses)),
        "contact_frac": float(np.mean(contact_fracs)),
    }
