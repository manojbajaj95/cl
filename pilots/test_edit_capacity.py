import math
import unittest

import torch

from edit_capacity import PREFIX, norm_prediction, participation_rank, ridge_dual, sustained_crossing


class CapacityPilotTests(unittest.TestCase):
    def test_dual_ridge_matches_primal(self):
        keys = torch.tensor([[1.0, 2.0], [2.0, -1.0], [3.0, 1.0]], dtype=torch.double)
        prior = torch.diag(torch.tensor([1.0, 2.0, 3.0], dtype=torch.double))
        actual = ridge_dual(torch.linalg.cholesky(prior), keys)
        torch.testing.assert_close(actual, torch.linalg.solve(prior + keys @ keys.T, keys))

    def test_rank_uses_centered_covariance(self):
        keys = torch.tensor([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
        self.assertAlmostEqual(participation_rank(keys + 100), 2.0)
        keys[:, 1] = 1
        self.assertAlmostEqual(participation_rank(keys), 1.0)

    def test_norm_forecast_ignores_future_edits(self):
        self.assertAlmostEqual(norm_prediction([(32, 0.32), (64, 0.64), (PREFIX + 1, 100)], 2), 200)
        self.assertIsNone(norm_prediction([(32, -0.32), (64, -0.64), (PREFIX + 1, 100)], 2))

    def test_collapse_requires_consecutive_crossings(self):
        high = math.log(2) + 0.001
        self.assertIsNone(sustained_crossing([(32, high), (64, 0), (96, high)]))
        self.assertEqual(sustained_crossing([(32, high), (64, 0), (96, high), (128, high)]), 96)


if __name__ == "__main__":
    unittest.main()
