import unittest

import numpy as np

from analyze import ARMS, T, estimate, match_temperatures, outcomes, summarize
from coding import FAMILIES, feedback, signature, stream
from depth_analyze import adjusted_risk, dose_fit, summarize_depth


class CodingTests(unittest.TestCase):
    def test_hidden_signatures_distinguish_three_outcomes(self):
        self.assertEqual(len({(f.name, v) for f, v, *_ in stream()}), 64)
        for f, v, *_ in stream():
            with self.subTest(family=f.name, variant=v):
                signature(f, v)  # verifies all outcomes against independent expected fixtures

    def test_smoke_feedback_cannot_distinguish_choices(self):
        for f in FAMILIES:
            expected = "smoke test passed" if f.smoke else "no smoke tests were run"
            self.assertEqual({feedback(f, choice) for choice in range(3)}, {expected}, f.name)


class AnalysisTests(unittest.TestCase):
    def test_solve_write_marginal(self):
        policy = [[.5, .3, .2], [.8, .15, .05], [.2, .7, .1], [.2, .2, .6]]
        np.testing.assert_allclose(outcomes(np.array(policy)), [.5, .5, .325, .175])

    def test_source_entropy_match_recovers_two_known_temperatures(self):
        rng = np.random.default_rng(1)
        source = rng.normal(size=(4, len(ARMS), 4, 3))
        source[:, 0] = source[:, -1] * np.array([0.6, 1.3, 1.3, 1.3])[None, :, None]
        weights = np.array([[.25, .25, .25, .25], [.0, .0, .0, 1.]])
        matched = match_temperatures(source, weights)
        np.testing.assert_allclose(matched, np.tile(np.array([0.6, 1.3]) / T, (2, 1)))

    def test_held_out_logits_do_not_enter_fit(self):
        panel = np.random.default_rng(3).normal(size=(3, 4, len(ARMS), 4, 3))
        weights = np.full((1, 3), 1/3)
        before = estimate(panel, weights)[1]
        panel[:, 1:] *= 2
        np.testing.assert_array_equal(estimate(panel, weights)[1], before)

    def test_identical_arms_fail_strict_gate(self):
        rng = np.random.default_rng(14)
        panel = np.repeat(rng.normal(size=(3, 4, 1, 4, 3)), len(ARMS), axis=2)
        result = summarize(panel, draws=100)
        self.assertEqual(result["bad_minus_control"]["filler"]["write_any"],
                         {"estimate": 0., "ci95": [0., 0.]})
        self.assertFalse(result["recommend_stage_1"])


class DepthTests(unittest.TestCase):
    def test_independent_dose_fit_recovers_known_transfer(self):
        p0, tau, k = .4, .12, 8
        p1 = 1 - (1 - p0) * (1 - tau)
        pk = 1 - (1 - p0) * (1 - tau)**k
        self.assertAlmostEqual(adjusted_risk(p0, p1), tau)
        self.assertAlmostEqual(dose_fit(p0, p1, pk, k), tau)

    def test_k1_transfer_equals_original_adjusted_estimate(self):
        rng = np.random.default_rng(5)
        original = rng.normal(size=(4, 4, 4, 4, 3))
        panel = original[:, :, [1, 0, 0, 2, 0, 1]]
        depth = summarize_depth(panel, original[:, :, -1], 1, np.full((3, 4), .25))
        binary = summarize(original, draws=2)
        self.assertAlmostEqual(depth["k_tau_eff"]["estimate"], binary["background_adjusted_tau"]["estimate"])

    def test_one_filler_and_one_bad_arms_define_local_effect(self):
        panel = np.zeros((2, 4, 6, 4, 3))
        panel[:, :, 5, :, 0] = 1  # correct favored when the target slot is filler
        panel[:, :, 4, :, 1] = 1  # planted defect favored when the slot is defective
        score = summarize_depth(panel, panel[:, :, 5], 4, np.full((3, 2), .5))
        self.assertGreater(score["k_tau_eff"]["estimate"], 0.5)
        self.assertEqual(score["tau_dose_fit"]["estimate"], 0)


if __name__ == "__main__":
    unittest.main()
