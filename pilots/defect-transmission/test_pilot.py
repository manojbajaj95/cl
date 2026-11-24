import unittest

import numpy as np

from analyze import ARMS, T, estimate, match_temperatures, outcomes, summarize
from coding import FAMILIES, feedback, signature, stream


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


if __name__ == "__main__":
    unittest.main()
