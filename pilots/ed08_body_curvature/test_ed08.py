"""Unit and regression tests for the ED08 body-curvature CPU pilot.

Run:
    python3 -m unittest discover -s pilots/ed08_body_curvature -p "test_*.py" -v
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

import numpy as np

PILOT_DIR = Path(__file__).resolve().parent
if str(PILOT_DIR) not in sys.path:
    sys.path.insert(0, str(PILOT_DIR))

from bodies import (  # noqa: E402
    arm_accel,
    default_arm_params,
    default_arm_policy,
    default_hopper_policy,
    default_pusher_policy,
    hopper_apex_map,
    pusher_accel,
    sample_arm_states,
    sample_hopper_states,
    sample_pusher_states,
)
from estimator import estimate_loop_curvature  # noqa: E402
from pilot import make_arm_corners  # noqa: E402


class TestED08BodiesAndEstimator(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(42)
        q_r, qd_r = sample_arm_states(self.rng, 300)
        q_e, qd_e = sample_arm_states(self.rng, 150)
        self.s_r = np.concatenate([q_r, qd_r], axis=-1)
        self.u_r = default_arm_policy(q_r, qd_r)
        self.u_e = default_arm_policy(q_e, qd_e)
        self.base = default_arm_params()

    def test_ed01_unsaturated_gains_read_exact_zero(self) -> None:
        for pair in [("k1", "k2"), ("k1", "m1"), ("k2", "l2"), ("k1", "mp")]:
            corners = make_arm_corners(self.base, pair[0], pair[1], 0.15, 0.15)
            res = estimate_loop_curvature(
                "arm", None, corners, 0.15, 0.15, self.s_r, self.u_r, self.u_e,
            )
            self.assertLess(res.F_cal, 1e-10, f"Expected exact flat on {pair}, got {res.F_cal}")

        # Verify orientation-reversed antisymmetrization cancels round-trip error on k1 x m1
        corners_km = make_arm_corners(self.base, "k1", "m1", 0.15, 0.15)
        res_km = estimate_loop_curvature(
            "arm", None, corners_km, 0.15, 0.15, self.s_r, self.u_r, self.u_e,
        )
        self.assertGreater(res_km.F_raw, 1e-3, "Raw uncalibrated loop should show round-trip artifact")
        self.assertLess(res_km.F_cal, 1e-10, "Antisymmetric loop should cancel round-trip artifact")

    def test_ed01_inertial_pairs_read_nonzero(self) -> None:
        for pair in [("m1", "m2"), ("m1", "l2"), ("m1", "mp"), ("m2", "l2"), ("m2", "mp"), ("l2", "mp")]:
            corners = make_arm_corners(self.base, pair[0], pair[1], 0.15, 0.15)
            res = estimate_loop_curvature(
                "arm", None, corners, 0.15, 0.15, self.s_r, self.u_r, self.u_e,
            )
            self.assertGreater(res.F_cal, 0.008, f"Expected nonzero curvature on {pair}, got {res.F_cal}")

    def test_ed05_froude_flat_vs_length_curved(self) -> None:
        c_fr = make_arm_corners(dict(self.base, froude_time_scale=True), "froude_L", "l2", 0.15, 0.15)
        res_fr = estimate_loop_curvature("arm", None, c_fr, 0.15, 0.15, self.s_r, self.u_r, self.u_e)
        self.assertLess(res_fr.F_cal, 1e-10)

        c_lo = make_arm_corners(dict(self.base, froude_time_scale=False), "froude_L", "l2", 0.15, 0.15)
        f2_lo = []
        for seed in range(4):
            rng = np.random.default_rng(100 + seed)
            qr, qdr = sample_arm_states(rng, 300)
            qe, qde = sample_arm_states(rng, 150)
            res_lo = estimate_loop_curvature(
                "arm", None, c_lo, 0.15, 0.15,
                np.concatenate([qr, qdr], axis=-1), default_arm_policy(qr, qdr), default_arm_policy(qe, qde),
            )
            f2_lo.append(res_lo.F2_cal)
        self.assertGreater(float(np.sqrt(max(0.0, np.mean(f2_lo)))), 0.01)

    def test_ed02_tanh_saturation_creates_curvature_on_flat_gains(self) -> None:
        c_inf = make_arm_corners(dict(self.base, u_max=np.inf, sat_mode="tanh"), "k1", "k2", -0.25, -0.25)
        c_sat = make_arm_corners(dict(self.base, u_max=18.0, sat_mode="tanh"), "k1", "k2", -0.25, -0.25)
        r_inf = estimate_loop_curvature("arm", None, c_inf, -0.25, -0.25, self.s_r, self.u_r, self.u_e)
        self.assertLess(r_inf.F_cal, 1e-10)
        f2_sat = []
        for seed in range(4):
            rng = np.random.default_rng(200 + seed)
            qr, qdr = sample_arm_states(rng, 300)
            qe, qde = sample_arm_states(rng, 150)
            r_sat = estimate_loop_curvature(
                "arm", None, c_sat, -0.25, -0.25,
                np.concatenate([qr, qdr], axis=-1), default_arm_policy(qr, qdr), default_arm_policy(qe, qde),
            )
            f2_sat.append(r_sat.F2_cal)
        self.assertGreater(float(np.sqrt(max(0.0, np.mean(f2_sat)))), 0.15)

    def test_antisymmetry_under_loop_reversal(self) -> None:
        corners = make_arm_corners(self.base, "m1", "l2", 0.15, 0.15)
        p00, p10, p11, p01 = corners
        rev_corners = (p00, p01, p11, p10)
        r_fwd = estimate_loop_curvature("arm", None, corners, 0.15, 0.15, self.s_r, self.u_r, self.u_e)
        r_rev = estimate_loop_curvature("arm", None, rev_corners, 0.15, 0.15, self.s_r, self.u_r, self.u_e)
        np.testing.assert_allclose(r_fwd.d_mean, -r_rev.d_mean, atol=1e-10)
        self.assertAlmostEqual(r_fwd.F_cal, r_rev.F_cal, places=10)

    def test_split_half_unbiased_on_noisy_flat_loop(self) -> None:
        corners = make_arm_corners(self.base, "k1", "k2", 0.15, 0.15)
        f2_vals = []
        for s in range(30):
            rng = np.random.default_rng(700 + s)
            res = estimate_loop_curvature(
                "arm", None, corners, 0.15, 0.15, self.s_r, self.u_r, self.u_e,
                rel_noise_std=0.001, rng=rng,
            )
            f2_vals.append(res.F2_cal)
        mean_f2 = float(np.mean(f2_vals))
        se_f2 = float(np.std(f2_vals, ddof=1) / np.sqrt(len(f2_vals)))
        # Cross-fitted inner product should be zero-mean (within 3 SE), unlike naive positive-biased norms
        self.assertLess(abs(mean_f2), 3.0 * se_f2 + 1e-6)

    def test_ed04_pusher_crossing_exceeds_within_mode(self) -> None:
        s_r = sample_pusher_states(self.rng, 300)
        s_e = sample_pusher_states(self.rng, 150)
        u_r = default_pusher_policy(s_r)
        u_e = default_pusher_policy(s_e)

        # Low friction (pure slip) vs stick/slip boundary cell
        c_within = (
            {"mu": 0.15, "m_obj": 1.0},
            {"mu": 0.18, "m_obj": 1.0},
            {"mu": 0.18, "m_obj": 1.2},
            {"mu": 0.15, "m_obj": 1.2},
        )
        c_cross = (
            {"mu": 1.6, "m_obj": 0.8},
            {"mu": 1.92, "m_obj": 0.8},
            {"mu": 1.92, "m_obj": 0.96},
            {"mu": 1.6, "m_obj": 0.96},
        )
        f2_w, f2_c = [], []
        for seed in range(4):
            rng = np.random.default_rng(300 + seed)
            sr = sample_pusher_states(rng, 300)
            se = sample_pusher_states(rng, 150)
            ur = default_pusher_policy(sr)
            ue = default_pusher_policy(se)
            f2_w.append(estimate_loop_curvature("pusher", pusher_accel, c_within, 0.2, 0.2, sr, ur, ue).F2_cal)
            f2_c.append(estimate_loop_curvature("pusher", pusher_accel, c_cross, 0.2, 0.2, sr, ur, ue).F2_cal)
        fw = float(np.sqrt(max(0.0, np.mean(f2_w))))
        fc = float(np.sqrt(max(0.0, np.mean(f2_c))))
        self.assertGreater(fc, 3.0 * fw + 0.02)

    def test_ed03_hopper_boundary_exceeds_within_gait(self) -> None:
        s_r = sample_hopper_states(self.rng, 300)
        s_e = sample_hopper_states(self.rng, 150)
        u_r = default_hopper_policy(s_r)
        u_e = default_hopper_policy(s_e)

        c_within = (
            {"m": 1.0, "l0": 0.75},
            {"m": 1.15, "l0": 0.75},
            {"m": 1.15, "l0": 0.8625},
            {"m": 1.0, "l0": 0.8625},
        )
        c_bound = (
            {"m": 2.6, "l0": 1.0},
            {"m": 2.99, "l0": 1.0},
            {"m": 2.99, "l0": 1.15},
            {"m": 2.6, "l0": 1.15},
        )
        r_w = estimate_loop_curvature("hopper", hopper_apex_map, c_within, 0.15, 0.15, s_r, u_r, u_e)
        r_b = estimate_loop_curvature("hopper", hopper_apex_map, c_bound, 0.15, 0.15, s_r, u_r, u_e)
        self.assertGreater(r_b.F_cal, 2.0 * r_w.F_cal)

    def test_arm_accel_shapes_and_finiteness(self) -> None:
        q = self.s_r[:, :2]
        qd = self.s_r[:, 2:4]
        qdd = arm_accel(q, qd, self.u_r, self.base)
        self.assertEqual(qdd.shape, (len(self.s_r), 2))
        self.assertTrue(np.all(np.isfinite(qdd)))


if __name__ == "__main__":
    unittest.main()
