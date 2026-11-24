import json
import unittest

import numpy as np

from pilot import LABELS, design, pair_scores, subtract, summarize, verdict


class PilotTests(unittest.TestCase):
    def test_balanced_ordered_design_and_disjoint_calibration(self):
        lessons, pairs, heldout, calibration = design()
        self.assertEqual(len(set(lessons)), 25)
        self.assertEqual(len(set(pairs)), 200)
        self.assertEqual(sum(a // 5 == b // 5 for a, b in pairs), 100)
        self.assertTrue(all(a != b for a, b in pairs))
        self.assertEqual({a: sum(s == a for s, _ in pairs) for a in range(25)}, dict.fromkeys(range(25), 8))
        self.assertEqual(len(set(map(tuple, heldout))), 20)
        self.assertEqual(len(set(map(tuple, calibration))), 10)
        self.assertFalse(set(map(tuple, heldout)) & set(map(tuple, calibration)))
        for index in range(5):
            self.assertEqual(sorted(row[index] for row in heldout), sorted(LABELS * 4))

    def test_factorized_inner_product(self):
        lhs = np.array([[1., 2.], [-3., 4.], [2., 1.]])
        rhs = np.array([[2., 3., 4.], [4., 0., 8.], [2., 8., 5.]])
        materialized = np.array([np.outer(l, r).ravel() for l, r in zip(lhs, rhs)])
        np.testing.assert_allclose(pair_scores(lhs, rhs), materialized @ materialized.T)

    def test_exact_drop_preserves_rank_ties(self):
        row = lambda acc: {"exact": acc, "logp": -1.}
        self.assertEqual(subtract(row(.95), row(.90))["exact"], subtract(row(.15), row(.10))["exact"])

    def test_gate_and_bootstrap_use_primary_outcome(self):
        rows = []
        for a, b in [(a, b) for a in range(5) for b in range(5) if a != b]:
            i = len(rows)
            values = {"exact": (i + 1) / 25, "logp": -float(i)}
            rows.append({
                "a": a, "b": b, "patch": i, "patch_cosine": i, "nli": -i, "fv": -i, "length": 10,
                "drop": values, "control_drop": {"exact": values["exact"] / 2, "logp": 0.},
                "baseline": {"exact": 1., "logp": -1.},
            })
        summary = summarize(rows, 30)
        self.assertAlmostEqual(summary["exact"]["rho_patch_minus_nli"]["estimate"], 2.)
        np.testing.assert_allclose(summary["exact"]["rho_patch"]["pair_95ci"], [1., 1.])
        np.testing.assert_allclose(summary["exact"]["rho_patch"]["lesson_95ci"], [1., 1.])
        self.assertEqual(json.loads(json.dumps(verdict(summary["exact"])))["decision"], "KEEP")
        self.assertEqual(verdict(summary["logp"])["decision"], "KILL")
        summary["exact"]["dilution_share"]["estimate"] = .51
        self.assertEqual(verdict(summary["exact"])["decision"], "KILL")


if __name__ == "__main__":
    unittest.main()
