import unittest
from collections import Counter

import numpy as np

from analysis_swap import bootstrap_indices, directional_effects, kill_flags, means, weighted
from design import MENU, lessons


def tables(base, rule, swapped, filler, non_menu):
    return {
        "base": np.asarray(base),
        **{key: np.eye(len(MENU))[value][None, ...] for key, value in (
            ("rule", rule), ("swapped", swapped), ("filler", filler), ("non_menu", non_menu)
        )},
    }


class DesignTest(unittest.TestCase):
    def test_twins_and_counterbalancing(self):
        notes = lessons()
        self.assertEqual(len({note["template"] for note in notes}), 20)
        for note in notes:
            self.assertEqual(note["action"] in MENU and note["swap_action"] in MENU, True)
            self.assertNotEqual(note["action"], note["swap_action"])
            self.assertEqual(sum(a != b for a, b in zip(note["rule"], note["swapped"])), 1)
            self.assertEqual(sum(a != b for a, b in zip(note["rule"], note["non_menu"])), 1)
        counts = Counter((note["action"], note["swap_action"]) for note in notes)
        self.assertEqual(len(counts), 6)
        self.assertEqual(counts, Counter({(b, a): n for (a, b), n in counts.items()}))


class AnalysisTest(unittest.TestCase):
    def test_perfect_following_and_matching_uses_own_margin(self):
        notes = [{"action": "A", "swap_action": "B"}]
        raw = tables([[0, -0.29, -3], [-0.69, 0, -3]],
                     [0, 0], [1, 1], [0, 1], [0, 1])
        effects, bins, _, _ = directional_effects(raw, notes)
        np.testing.assert_array_equal(bins[0], [[0, 2], [3, 0]])
        np.testing.assert_allclose(means(effects.reshape(-1, effects.shape[-1])),
                                   [100, 50, 50, 100, 0, 0])

    def test_identical_winners_give_zero_and_reversal_gives_negative(self):
        notes = [{"action": "A", "swap_action": "B"}]
        base = [[0, -1, -3]]
        same = directional_effects(tables(base, [0], [0], [0], [0]), notes)[0]
        reverse = directional_effects(tables(base, [1], [0], [0], [0]), notes)[0]
        np.testing.assert_array_equal(same[0, 0, :, 0], [0, 0])
        np.testing.assert_array_equal(reverse[0, 0, :, 0], [-100, -100])

    def test_common_weights_and_crossed_sample(self):
        np.testing.assert_allclose(weighted(np.array([[1, 4], [5, 0]]), np.array([3, 1])), [2, 3])
        lesson_ids, state_ids = next(bootstrap_indices(20, 36, 1, 403989))
        self.assertEqual(lesson_ids.shape, (20, 1))
        self.assertEqual(state_ids.shape, (1, 36))

    def test_kill_thresholds(self):
        self.assertFalse(any(kill_flags({"estimate": 10, "ci95": [1, 17]}).values()))
        self.assertTrue(kill_flags({"estimate": 9.99, "ci95": [1, 17]})["follow_index_below_10pp"])
        self.assertTrue(kill_flags({"estimate": 10, "ci95": [0, 17]})["follow_index_ci_includes_zero"])


if __name__ == "__main__":
    unittest.main()
