"""Unit and regression tests for the ED10 Gamma vs Fairest RMA MuJoCo pilot."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import numpy as np

PILOT_DIR = Path(__file__).resolve().parent
if str(PILOT_DIR) not in sys.path:
    sys.path.insert(0, str(PILOT_DIR))

from arms import (  # noqa: E402
    RMAFiLMPolicy,
    SkillPolicy,
    StateBasis,
    extract_rma_body_latents,
    fit_eb12_conjugator,
    fit_ritual_dynamics,
    gamma_transport_action,
    make_rma_input,
)
from mujoco_arm import (  # noqa: E402
    MuJoCoArm,
    collect_ritual_data,
    collect_skill_data,
    evaluate_policy_on_skill,
    expert_desired_accel,
    get_body_families,
    get_skills,
)


class TestED10MuJoCoPilot(unittest.TestCase):
    def test_mujoco_forward_inverse_consistency(self) -> None:
        arm = MuJoCoArm(get_body_families()["curved"]["B"])
        q = np.array([0.3, -0.4])
        qd = np.array([0.8, -1.1])
        qdd_des = np.array([4.0, -3.5])
        u = arm.inverse_ctrl(q, qd, qdd_des)
        qdd_got = arm.forward_accel(q, qd, u)
        self.assertTrue(np.allclose(qdd_got, qdd_des, atol=1e-4))

    def test_ritual_dynamics_high_r2_under_1pct_noise(self) -> None:
        rng = np.random.default_rng(7)
        arm = MuJoCoArm(get_body_families()["curved"]["D"])
        rit = collect_ritual_data(arm, n_samples=1200, sensor_noise_std=0.01, rng=rng)
        dyn = fit_ritual_dynamics(rit, StateBasis())
        test = collect_ritual_data(arm, n_samples=300, sensor_noise_std=0.0, rng=rng)
        pred = dyn.predict_qdd(test["q"], test["qd"], test["u"])
        r2 = 1.0 - np.sum((pred - test["qdd"]) ** 2) / np.sum((test["qdd"] - np.mean(test["qdd"], axis=0)) ** 2)
        self.assertGreater(r2, 0.95)

    def test_rma_gradient_matches_finite_difference(self) -> None:
        rng = np.random.default_rng(11)
        m = RMAFiLMPolicy(in_dim=6, z_dim=3, hidden=5, out_dim=2, seed=1)
        xn = rng.normal(size=(10, 6))
        z = rng.normal(size=(10, 3))
        y = rng.normal(size=(10, 2))
        w = rng.uniform(0.5, 2.0, size=10)
        for include_body in (True, False):
            th = m._pack(include_body=include_body)
            _, g = m._loss_and_grad(th, xn, z, y, w, 1e-3, include_body)
            eps = 1e-6
            g_num = np.zeros_like(g)
            for i in range(len(th)):
                tp = th.copy(); tp[i] += eps
                tm = th.copy(); tm[i] -= eps
                lp = m._loss_and_grad(tp, xn, z, y, w, 1e-3, include_body)[0]
                lm = m._loss_and_grad(tm, xn, z, y, w, 1e-3, include_body)[0]
                g_num[i] = (lp - lm) / (2.0 * eps)
            self.assertLess(np.max(np.abs(g - g_num)), 1e-7)

    def test_gamma_beats_notransport_and_eb12_on_curved_s5(self) -> None:
        rng = np.random.default_rng(42)
        specs = get_body_families()["curved"]
        arms = {b: MuJoCoArm(sp) for b, sp in specs.items()}
        s5 = get_skills()[4]
        rit = {b: collect_ritual_data(arms[b], 1200, 0.01, rng) for b in ["A", "B", "C", "D"]}
        basis = StateBasis()
        dyn = {b: fit_ritual_dynamics(rit[b], basis) for b in ["A", "B", "C", "D"]}
        s5_B = collect_skill_data(arms["B"], s5, 8, 80, 0.01, rng)
        pol_B = SkillPolicy(seed=0)
        pol_B.fit(s5_B["states"], s5_B["times"], s5_B["u"], ridge=1e-2)

        gamma_rets, eb12_rets, nt_rets = [], [], []
        for b in ["A", "C", "D"]:
            eb = fit_eb12_conjugator(dyn["B"], dyn[b], rit["B"])
            gamma_rets.append(
                evaluate_policy_on_skill(
                    arms[b], s5,
                    lambda s, t, b_=b: gamma_transport_action(dyn["B"], dyn[b_], s[:2], s[2:4], pol_B.predict(s, t)),
                    n_episodes=4, horizon=80, sensor_noise_std=0.01, seed=10,
                )["return"]
            )
            eb12_rets.append(
                evaluate_policy_on_skill(
                    arms[b], s5,
                    lambda s, t, eb_=eb: eb_.map_action(pol_B.predict(s, t)),
                    n_episodes=4, horizon=80, sensor_noise_std=0.01, seed=10,
                )["return"]
            )
            nt_rets.append(
                evaluate_policy_on_skill(
                    arms[b], s5,
                    lambda s, t: pol_B.predict(s, t),
                    n_episodes=4, horizon=80, sensor_noise_std=0.01, seed=10,
                )["return"]
            )
        self.assertGreater(np.mean(gamma_rets), 0.80)
        self.assertGreater(np.mean(gamma_rets), np.mean(nt_rets) + 0.40)
        self.assertGreater(np.mean(gamma_rets), np.mean(eb12_rets))

    def test_rma_latents_distinguish_bodies_without_xml(self) -> None:
        rng = np.random.default_rng(5)
        specs = get_body_families()["curved"]
        arms = {b: MuJoCoArm(sp) for b, sp in specs.items()}
        rit = {b: collect_ritual_data(arms[b], 600, 0.01, rng) for b in ["A", "B", "C", "D"]}
        dyn = {b: fit_ritual_dynamics(rit[b], StateBasis()) for b in ["A", "B", "C", "D"]}
        latents = extract_rma_body_latents(dyn, n_probe=32, latent_dim=6, seed=0)
        self.assertEqual(set(latents.keys()), {"A", "B", "C", "D"})
        for b1 in ["A", "B", "C", "D"]:
            for b2 in ["A", "B", "C", "D"]:
                if b1 != b2:
                    self.assertGreater(np.linalg.norm(latents[b1] - latents[b2]), 0.5)

    def test_saved_results_json_passes_all_gates(self) -> None:
        res_path = PILOT_DIR / "results.json"
        self.assertTrue(res_path.exists(), "results.json missing — run pilot.py first")
        data = json.loads(res_path.read_text())
        self.assertEqual(data["verdict"], "PASS")
        self.assertTrue(all(data["gates"].values()), f"Failed gates: {data['gates']}")
        self.assertGreater(data["curved_1pct"]["paired_gamma_minus_best_rma_return"]["gap_in_se"], 2.0)


if __name__ == "__main__":
    unittest.main()
