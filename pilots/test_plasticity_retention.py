import unittest
from dataclasses import replace

import numpy as np

import plasticity_reserve as pilot
import plasticity_retention as retention


class PlasticityRetentionTest(unittest.TestCase):
    def setUp(self):
        self.cfg = replace(pilot.Config(), tasks=3, write_steps=24, fork_steps=8,
                           gain_steps=5, repeats=2, samples=16)
        self.params = pilot.initial_params(41, self.cfg)
        self.stream = pilot.build_stream(41, self.cfg)

    def test_match_checks_each_previous_task(self):
        candidates, _, _ = pilot.write_candidates(self.params, self.stream[2], 41, 2, self.cfg)
        panels = [task[1] for task in reversed(self.stream)]
        before = np.stack([pilot.mse(candidates, panel) for panel in panels], axis=1)
        self.assertTrue(np.any(np.ptp(before[:, 1:], axis=0) > self.cfg.loss_tolerance * before[:, 1:].min(axis=0)))
        matched, losses, blend, _ = retention.match_retention(candidates, panels, self.cfg)
        self.assertEqual(losses.shape, (8, 3))
        np.testing.assert_allclose(losses, np.stack([pilot.mse(matched, p) for p in panels], axis=1))
        self.assertTrue(np.all(np.ptp(losses, axis=0) <= self.cfg.loss_tolerance * losses.min(axis=0)))
        self.assertTrue(np.any(blend < 1))
        self.assertGreater(np.ptp(matched[0], axis=0).max(), 0)

    def test_projection_removes_only_span_of_stored_directions(self):
        basis = retention.old_gradient_basis([[1, 1, 0], [2, 2, 0], [0, 0, 0]])
        self.assertEqual(len(basis), 1)
        np.testing.assert_allclose(retention.project([1, 1, 5], basis), [0, 0, 5], atol=1e-14)
        np.testing.assert_allclose(retention.project([1, -1, 5], basis), [1, -1, 5])

    def test_projected_fit_with_empty_or_full_basis(self):
        task = self.stream[1]
        orders = pilot.orders_for_gain(41, 1, 0, self.cfg)
        dim = retention.flatten(self.params).size
        expected, before, after = pilot.gain(self.params, task[3], task[4], orders, self.cfg)
        for basis, gains in ((np.empty((0, dim)), (expected, before - after)), (np.eye(dim), (0, 0))):
            np.testing.assert_allclose(retention.projected_gain(self.params, task[3], task[4],
                                                                orders, basis, self.cfg), gains, atol=1e-14)

    def test_gate_requires_positive_order_corrected_signal(self):
        rows = [retention.stream(seed, self.cfg) for seed in (41, 42)]
        for row in rows:
            self.assertLessEqual(row["max_prior_loss_range"], self.cfg.loss_tolerance)
            self.assertGreater(row["final_projection_rank"], 0)
            row.update(absolute_signal_variance=0.0, absolute_spread=0.02, original_absolute_spread=0.02)
        self.assertFalse(retention.summarize(rows)["gate_passed"])
        for row in rows:
            row["absolute_signal_variance"] = 0.01
        self.assertTrue(retention.summarize(rows)["gate_passed"])
        for key in ("original_absolute_spread", "absolute_spread"):
            with self.subTest(key=key):
                self.assertFalse(retention.summarize([dict(row, **{key: 0.014})
                                                      for row in rows])["gate_passed"])

    def test_original_relative_spread_replays_pilot(self):
        run = pilot.stream_run(41, "random", self.cfg)
        expected = np.mean([np.ptp(np.mean(row["future_gain"], axis=1))
                            for row in run["diagnostics"]])
        relative, _ = retention.original_stream(41, self.cfg, self.stream)
        self.assertAlmostEqual(relative, expected)
