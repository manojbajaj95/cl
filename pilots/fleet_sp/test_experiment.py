import unittest

import numpy as np

import experiment as exp


class FleetTest(unittest.TestCase):
    def test_exposure_gate_keeps_lesson_direction(self):
        exposed = list(range(exp.N_EXPOSED))
        has_memory = np.isin(np.arange(exp.N_AGENTS), exposed)
        data = dict(exposed=exposed, pool=[(1, 0, "PUT"), (1, 0, "POST")],
                    predicted=np.column_stack([has_memory, ~has_memory]).astype(float))
        self.assertAlmostEqual(exp.exposure_r(data), 1.0)
        self.assertAlmostEqual(exp.exposure_r(data, "false"), -1.0)
        self.assertEqual(exp.exposure_r(data, "all"), 0.0)

    def test_subtracting_prior_can_reverse_the_mean_ranking(self):
        data = dict(pi=[[.8, .4], [.9, .6]], p0=[.8, .1],
                    predicted=[[.9, .1], [.9, .1]], confidence=[[4, 2], [4, 2]],
                    authors=[3, 4])
        scores = exp.rank(data)
        np.testing.assert_allclose(scores["logprob_sp"], [.05, .4])
        np.testing.assert_allclose(scores["mean_pi"], [.85, .5])
        np.testing.assert_allclose(scores["elicited_sp"], [.1, .4])
        self.assertEqual(set(exp.rank(data, controls=False)), set(exp.ARMS[:3]))

    def test_retrieval_prefers_regime_then_route_at_the_same_k(self):
        pool = [(0, 0, "POST"), (0, 1, "GET"), (0, 2, "PATCH"), (0, 3, "DELETE"),
                (1, 0, "PUT"), (1, 1, "HEAD"), (1, 2, "PUT"), (1, 3, "POST"),
                (1, 1, "GET")]
        scores = {"majority": [1, 1, 1, 1, .2, .1, .3, .4, 0]}
        order = list(range(len(pool)))
        static = exp.memory_for("majority", scores, pool, order, 1, 1)
        retrieved = exp.memory_for("regime_retrieval", scores, pool, order, 1, 1)
        self.assertEqual(static, (0, 1, 2, 3))
        self.assertEqual(retrieved, (5, 6, 7, 8))

    def test_truth_discovery_handles_unanimity_and_split(self):
        matrix = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 1], [1, 0, 1]])
        for family in (False, True):
            posterior = exp.bp_td(matrix, family=family)
            self.assertGreater(posterior[0], .5)
            self.assertLess(posterior[1], .5)
            self.assertAlmostEqual(posterior[2], .5)

    def test_bootstrap_resamples_whole_fleets(self):
        self.assertEqual(exp.summarize([.5, .5, .5]), [.5, .5, .5])
        self.assertAlmostEqual(exp.summarize([0, 0.5, 1])[0], .5)


if __name__ == "__main__":
    unittest.main()
