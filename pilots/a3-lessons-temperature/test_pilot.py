import unittest
from itertools import product

import numpy as np
from scipy.special import log_softmax

from analysis import lesson_share, match_temperature, r2, verdict
from router import CODES, HELD_OUT, SOURCE, STEPS, correct, exact_success, start_visitation


class RouterTest(unittest.TestCase):
    def test_rotation_and_balanced_modal_success(self):
        displayed = np.arange(CODES) + 10
        np.testing.assert_array_equal(correct(np.arange(CODES)), np.where(displayed % 3, 0, 2))
        modal = np.full((STEPS, CODES, 3), -np.inf)
        modal[..., 0] = 0
        self.assertFalse(set(SOURCE) & set(HELD_OUT))
        for starts in SOURCE, HELD_OUT:
            np.testing.assert_array_equal(exact_success(modal, starts), displayed[list(starts)] % 3 != 0)
            self.assertEqual(exact_success(modal, starts).sum(), 4)

    def test_uniform_success_and_source_visitation(self):
        uniform = np.full((STEPS, CODES, 3), -np.log(3))
        np.testing.assert_allclose(exact_success(uniform, range(CODES)), 7 / 27)
        visits = start_visitation(uniform, SOURCE)
        np.testing.assert_allclose(visits.sum(-1), 1 / STEPS)
        np.testing.assert_allclose(visits[0, HELD_OUT], 0)


class AnalysisTest(unittest.TestCase):
    def test_known_temperature_recovers_exact_held_out_effect(self):
        logits = np.random.default_rng(4).normal(size=(STEPS, CODES, 3))
        base = log_softmax(logits, axis=-1)
        for true_beta in (0.4, 1.7, 6.0):
            lesson = log_softmax(logits * true_beta, axis=-1)
            beta, match, target, fitted = match_temperature(base, lesson, SOURCE)
            self.assertAlmostEqual(beta, true_beta)
            self.assertAlmostEqual(target, fitted)
            np.testing.assert_allclose(exact_success(match, HELD_OUT), exact_success(lesson, HELD_OUT))

    def test_held_out_only_changes_do_not_affect_fit(self):
        base = log_softmax(np.random.default_rng(3).normal(size=(STEPS, CODES, 3)), axis=-1)
        lesson = base.copy()
        lesson[0, HELD_OUT, :] = -np.log(3)
        beta, _, target, matched = match_temperature(base, lesson, SOURCE)
        self.assertAlmostEqual(beta, 1)
        self.assertAlmostEqual(target, matched)

    def test_variance_share_and_r2(self):
        lesson_only = np.array([[1, 1], [-1, -1]])
        start_only = lesson_only.T
        self.assertEqual(lesson_share(lesson_only), 1)
        self.assertEqual(lesson_share(start_only), 0)
        self.assertEqual(lesson_share(lesson_only + start_only), 0.5)
        self.assertEqual(r2(lesson_only, lesson_only), 1)
        self.assertEqual(r2(lesson_only, -lesson_only), -3)

    def test_kill_thresholds_are_strict_except_gap_point(self):
        defaults = dict(held_out_r2_pooled={"estimate": 0.50},
                        rule_minus_temperature_pp={"estimate": 5, "ci95": [0, 7]},
                        lesson_main_effect_share={"estimate": 0.25})
        self.assertFalse(any(verdict(defaults).values()))
        for r, g, s in product([0.49, 0.5], [0, 0.01], [0.25, 0.26]):
            actual = verdict(dict(held_out_r2_pooled={"estimate": r},
                                  rule_minus_temperature_pp={"estimate": 5, "ci95": [g, 7]},
                                  lesson_main_effect_share={"estimate": s}))
            self.assertEqual(list(actual.values()), [r < 0.5, g > 0, s > 0.25])


if __name__ == "__main__":
    unittest.main()
