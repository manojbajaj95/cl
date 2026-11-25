import unittest
from dataclasses import replace
from unittest.mock import patch

import numpy as np

import plasticity_reserve as pilot


class PlasticityReserveTest(unittest.TestCase):
    def setUp(self):
        self.cfg = replace(pilot.Config(), tasks=3, write_steps=24, fork_steps=8,
                           gain_steps=5, repeats=2, probes=12, samples=16)
        self.params = pilot.initial_params(41, self.cfg)
        self.stream = pilot.build_stream(41, self.cfg)

    def test_output_jacobian_and_mse_gradient(self):
        x, y = self.stream[0][2]
        jac, _ = pilot.output_jacobian(self.params, x)
        direction = tuple(pilot.rng(8, i).normal(size=p.shape) for i, p in enumerate(self.params))
        eps = 1e-6
        plus = tuple(p + eps * d for p, d in zip(self.params, direction))
        minus = tuple(p - eps * d for p, d in zip(self.params, direction))
        expected = (pilot.forward(plus, x)[0] - pilot.forward(minus, x)[0]) / (2 * eps)
        np.testing.assert_allclose(jac @ np.concatenate([d.ravel() for d in direction]),
                                   expected, atol=1e-8)
        loss_expected = (pilot.mse(plus, (x, y)) - pilot.mse(minus, (x, y))) / (2 * eps)
        actual = sum((g * d).sum() for g, d in zip(pilot.gradient(self.params, x, y), direction))
        self.assertAlmostEqual(actual, loss_expected)

    def test_readiness_matches_direct_minibatch_gradients(self):
        x, y = self.stream[0][2]
        orders = pilot.rng(8).integers(len(x), size=(10, self.cfg.batch))
        grad2 = sum((g**2).sum() for g in pilot.gradient(self.params, x, y))
        second = np.mean([sum((g**2).sum() for g in pilot.gradient(self.params, x[i], y[i]))
                          for i in orders])
        expected = grad2**2 / (second * pilot.mse(self.params, (x, y)))
        self.assertAlmostEqual(pilot.readiness(self.params, (x, y), orders), expected)

    def test_scr_shifts_one_bit_and_returns_eight_loss_matched_candidates(self):
        for previous, current in zip(self.stream, self.stream[1:]):
            before, after = (task[0][0][0, :self.cfg.slow_bits] for task in (previous, current))
            self.assertEqual(np.count_nonzero(before != after), 1)
        candidates, losses, _ = pilot.write_candidates(self.params, self.stream[0], 41, 0, self.cfg)
        self.assertEqual(len(losses), 8)
        self.assertLessEqual(np.ptp(losses), self.cfg.loss_tolerance * losses.min())
        np.testing.assert_allclose(losses, [pilot.mse(pilot.take(candidates, i), self.stream[0][1])
                                            for i in range(8)])
        self.assertGreater(np.ptp(candidates[0], axis=0).max(), 0)

    def test_probe_choosers_do_not_use_readiness_labels(self):
        with patch.object(pilot, "readiness", side_effect=AssertionError("labels used")):
            for policy in ("gramian", "feature_rank"):
                run = pilot.stream_run(41, policy, self.cfg)
                self.assertEqual(len(run["trace"]), self.cfg.tasks)

    def test_crossed_variance_removes_shared_order_effect(self):
        a, b = np.array([0.1, 0.2, 0.4]), np.array([1, 10, 50])
        signal, noise = pilot.variance_components(a[:, None] + b)
        self.assertAlmostEqual(signal, a.var(ddof=1))
        self.assertAlmostEqual(noise, 0)

    def test_summary_paired_bootstrap_preserves_constant_differences(self):
        values = np.ones((3, 11, len(pilot.SCORES)))
        values[:, :, 0] += 0.5
        bounds = pilot.block_bootstrap(values)
        np.testing.assert_allclose(bounds["gramian_minus_readiness"], [0.5, 0.5])


if __name__ == "__main__":
    unittest.main()
