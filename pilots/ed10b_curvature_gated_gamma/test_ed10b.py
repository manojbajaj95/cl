"""Unit and regression tests for ED10b curvature-gated Gamma CPU pilot."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from arms import (
    CapacityMatchedRMA,
    GenericMLP,
    GenericRFFBasis,
    estimate_pair_curvature_ed08,
    fit_rff_dynamics,
)
from mujoco_bodies import (
    MuJoCoArm,
    collect_ritual_data,
    evaluate_policy_on_skill,
    expert_desired_accel,
    get_body_families,
    get_skills,
)


class TestED10b(unittest.TestCase):
    def test_gat_mlp_and_rma_gradients_match_finite_diff(self) -> None:
        rng = np.random.default_rng(0)
        mlp = GenericMLP(6, 2, hidden=8, seed=0)
        xn, yn = rng.normal(size=(10, 6)), rng.normal(size=(10, 2))
        th = mlp._pack()
        _, g = mlp._loss_and_grad(th, xn, yn, 1e-3)
        eps = 1e-6
        gn = np.array([
            (mlp._loss_and_grad(th + eps * np.eye(len(th))[i], xn, yn, 1e-3)[0]
             - mlp._loss_and_grad(th - eps * np.eye(len(th))[i], xn, yn, 1e-3)[0]) / (2 * eps)
            for i in range(len(th))
        ])
        self.assertLess(float(np.max(np.abs(g - gn))), 1e-7)

        rma = CapacityMatchedRMA(z_dim=4, hidden_res=6, seed=0)
        st = rng.normal(size=(10, 4))
        uc = rng.normal(size=(10, 2))
        z = rng.normal(size=(10, 4))
        y = rng.normal(size=(10, 2))
        w = rng.uniform(0.5, 2.0, size=10)
        th2 = rma._pack_body()
        _, g2 = rma._body_loss_and_grad(th2, st, uc, z, y, w, 1e-3)
        gn2 = np.array([
            (rma._body_loss_and_grad(th2 + eps * np.eye(len(th2))[i], st, uc, z, y, w, 1e-3)[0]
             - rma._body_loss_and_grad(th2 - eps * np.eye(len(th2))[i], st, uc, z, y, w, 1e-3)[0]) / (2 * eps)
            for i in range(len(th2))
        ])
        self.assertLess(float(np.max(np.abs(g2 - gn2))), 1e-7)

    def test_contact_family_has_active_wall_contact_and_high_expert_return(self) -> None:
        fams = get_body_families()
        s5 = get_skills(contact_family=True)[4]
        for b, sp in fams["contact"].items():
            arm = MuJoCoArm(sp)
            ev = evaluate_policy_on_skill(
                arm, s5,
                lambda s, t, arm=arm: arm.inverse_ctrl(s[:2], s[2:4], expert_desired_accel(s5, s[:2], s[2:4], t)),
                n_episodes=3, horizon=80, sensor_noise_std=0.01, seed=0,
            )
            self.assertGreater(ev["return"], 0.90, f"Contact expert S5 failed on {b}")
            self.assertGreater(ev["contact_frac"], 0.05, f"Contact wall never engaged on {b}")

    def test_ed08_curvature_gate_separates_flat_and_curved_in_mixed(self) -> None:
        rng = np.random.default_rng(7)
        fams = get_body_families()["mixed"]
        arms = {b: MuJoCoArm(sp) for b, sp in fams.items()}
        rits = {b: collect_ritual_data(arms[b], 1200, 0.01, rng) for b in ["B", "F1", "C1"]}
        basis = GenericRFFBasis(seed=0)
        c_flat = estimate_pair_curvature_ed08(rits["B"], rits["F1"], basis, seed=0)
        c_curv = estimate_pair_curvature_ed08(rits["B"], rits["C1"], basis, seed=0)
        self.assertLess(c_flat["f2_cal"], 0.005)
        self.assertGreater(c_curv["f2_cal"], 0.015)

    def test_generic_rff_dynamics_fits_curved_arm_at_1pct_noise(self) -> None:
        rng = np.random.default_rng(1)
        arm = MuJoCoArm(get_body_families()["curved"]["B"])
        tr = collect_ritual_data(arm, 1200, 0.01, rng)
        te = collect_ritual_data(arm, 300, 0.0, rng)
        dyn = fit_rff_dynamics(tr, GenericRFFBasis(seed=0))
        pred = dyn.predict_qdd(te["q"], te["qd"], te["u"])
        r2 = 1.0 - float(np.sum((te["qdd"] - pred) ** 2) / np.sum((te["qdd"] - te["qdd"].mean(0)) ** 2))
        self.assertGreater(r2, 0.85)

    def test_saved_results_json_is_complete_and_consistent(self) -> None:
        res_path = THIS_DIR / "results.json"
        self.assertTrue(res_path.exists())
        data = json.loads(res_path.read_text())
        self.assertEqual(data["meta"]["n_seeds"], 16)
        self.assertGreaterEqual(data["meta"]["sensor_noise"], 0.01)
        self.assertEqual(set(data["families"].keys()), {"flat", "curved", "contact", "mixed"})
        self.assertTrue(data["gates"]["rma_capacity_matched_s5_trainB_ge_0.90"])
        expected = "PROMOTE" if all(data["gates"].values()) else "NO_PROMOTE"
        self.assertEqual(data["verdict"], expected)


if __name__ == "__main__":
    unittest.main()
