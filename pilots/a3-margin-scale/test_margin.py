import unittest

import numpy as np

from analysis_margin import classify, masked_cells
from collect_margin import natural_system, prompt, rename
from margin import MENU_ORDERS, eligibility, fit_offset, offset_a, top_two


class BaselineTest(unittest.TestCase):
    def test_fit_offset_removes_constant_gap_without_changing_other_logits(self):
        old = np.array([[0.1, 0.3, -2], [0.1, 0.4, -2]])
        new = np.array([[2.2, 0, -3], [2.3, 0, -3]])
        off, loss = fit_offset(old, new)
        self.assertAlmostEqual(off, 2)
        self.assertAlmostEqual(loss, 0)
        changed = offset_a(new, off)
        np.testing.assert_array_equal(changed[:, 1:], new[:, 1:])
        np.testing.assert_allclose(top_two(changed)[1], top_two(old)[1])

    def test_eligibility_excludes_ties_large_margins_and_unrequested_states(self):
        base = np.array([[1, 0, -4], [1, 1, -4], [1, 0.5, -4], [0.5, 1, -4]])
        ids, top, gap = eligibility(base, [0, 1, 3])
        np.testing.assert_array_equal(ids, [3])
        np.testing.assert_array_equal(top, [[1, 0]])
        np.testing.assert_array_equal(gap, [0.5])

    def test_natural_mapping_changes_only_action_labels_and_menu_order(self):
        system = natural_system("XYZ", (1, 0, 2))
        self.assertIn("choose exactly one tool: Y, X, or Z.", system)
        self.assertIn("Remainder 0 requires Y, remainder 1 requires Z, remainder 2 requires X.", system)
        self.assertIn("A run succeeds if at least two routes are correct.", system)
        self.assertIn("Checkpoint 2/3. Code: 10. Tool?", prompt(system, 12))
        self.assertEqual(rename("At each step use A.", "XYZ"), "At each step use X.")
        self.assertEqual(len(MENU_ORDERS), 5)
        self.assertNotIn((0, 1, 2), MENU_ORDERS)


class AnalysisTest(unittest.TestCase):
    def test_makes_paired_follow_contrast_and_masks_third_rank(self):
        notes = [{"action": "A", "swap_action": "B"}]
        selectors = np.eye(3)
        rule = selectors[[0, 0]][None, ...]
        twin = selectors[[1, 1]][None, ...]
        filler = selectors[[0, 0]][None, ...]
        cell, eligible = masked_cells(rule, twin, filler, np.array([[0, 1], [0, 2]]), notes)
        np.testing.assert_allclose(cell[0, 0], [100, 50, 100, 0])
        self.assertTrue(np.isnan(cell[0, 1]).all())
        np.testing.assert_array_equal(eligible, [[True, False]])

    def test_decision_requires_both_arms_and_natural_coverage(self):
        def stats(point, ci, n=30):
            return {"n_eligible_states": n, "metrics": {"follow_pp": {"estimate": point, "ci95": ci}}}

        following = stats(10, [0.01, 20])
        flat = stats(1, [-3, 5])
        self.assertEqual(classify(following, following)[0], "margin")
        self.assertEqual(classify(flat, flat)[0], "scale")
        self.assertEqual(classify(following, flat)[0], "inconclusive")
        self.assertEqual(classify(following, stats(20, [4, 40], n=29))[0], "inconclusive")
        self.assertEqual(classify(following, stats(10, [0, 20]))[0], "inconclusive")


if __name__ == "__main__":
    unittest.main()
