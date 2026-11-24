import unittest

import numpy as np

import experiment as exp


class PilotTest(unittest.TestCase):
    def test_orders_permute_the_same_episodes_at_both_horizons(self):
        orders = [exp.order_ids(order) for order in exp.ORDERS]
        self.assertEqual(len({tuple(order) for order in orders}), 4)
        for order in orders:
            np.testing.assert_array_equal(np.sort(order), np.arange(exp.LONG))
            np.testing.assert_array_equal(np.sort(order[:exp.EARLY]), np.sort(orders[0][:exp.EARLY]))
            self.assertEqual(len(set(order[:exp.EARLY] // (exp.LONG // 4))), 4)

    def test_matched_draws_and_initial_perturbation(self):
        data = exp.world(exp.SEEDS[0])
        memory = data[4].copy()
        for design in exp.DESIGNS:
            with self.subTest(design=design):
                def get_trace(**kwargs):
                    return exp.rollout(design, data, exp.ORDERS[0], exp.EARLY, trace=True, **kwargs)[0]

                reference = get_trace()
                perturbed = get_trace(perturb=True)
                seed_only = get_trace(other_seed=True)
                np.testing.assert_array_equal(reference, get_trace())
                np.testing.assert_array_equal(reference[0], seed_only[0])
                self.assertGreater(exp.distance(reference[0], perturbed[0]), 0)
                self.assertLessEqual(exp.distance(reference[0], perturbed[0]), exp.PERTURBATION)
                self.assertEqual(reference.shape, (exp.EARLY + 1, 128))
        np.testing.assert_array_equal(data[4], memory)

    def test_finite_time_slope_and_rank_statistics(self):
        self.assertAlmostEqual(exp.slope(np.exp(-0.2 * np.arange(21))), -0.2)
        self.assertAlmostEqual(exp.slope(np.zeros(21)), 0)
        self.assertAlmostEqual(exp.correlation([1, 1, 2], [5, 5, 2]), -1)
        self.assertTrue(np.isnan(exp.correlation([1, 1, 1], [1, 2, 3])))
        self.assertEqual(exp.interval(float("nan"), np.array([float("nan")])),
                         {"estimate": None, "ci95": None, "valid_bootstraps": 0})

    def test_convergence_counts_consecutive_nonimprovements(self):
        result = exp.convergence(np.array([0, 0.002, 0.003, 0, -0.001, 0, 0.01]))
        self.assertEqual(result["declaration_level"], 6)
        self.assertEqual(result["nondeclaration"], 0)
        self.assertAlmostEqual(result["draft_rejection_rate"], 5 / 7)
        self.assertEqual(exp.convergence(np.ones(exp.EARLY))["declaration_level"], exp.EARLY + 1)
        self.assertEqual(exp.convergence(np.ones(exp.EARLY))["nondeclaration"], 1)


if __name__ == "__main__":
    unittest.main()
