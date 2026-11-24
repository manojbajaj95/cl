import unittest

import torch

from audit import interval
from run import HORIZON, VOCAB, corpus, path_log_probs, select, success


class PilotTest(unittest.TestCase):
    def test_exact_mass_for_uniform_autoregressive_policy(self):
        class Uniform:
            def __call__(self, tokens):
                return torch.zeros(*tokens.shape, VOCAB)

        prompts, paths, _ = corpus(0, range(2), 0)
        actual = success(path_log_probs(Uniform(), prompts, paths))
        expected = torch.full((len(prompts),), 2 / VOCAB**HORIZON)
        torch.testing.assert_close(actual, expected, atol=0, rtol=1e-5)
        self.assertTrue(torch.all(paths[:, 0, 0] != paths[:, 1, 0]))

    def test_select_checks_new_acquisition_before_retention(self):
        ineligible = (5, 1.0, (0.99, 0.99, 0.74), None)
        high_average = (10, 1.0, (0.95, 0.75, 0.80), None)
        high_minimum = (15, 1.0, (0.85, 0.85, 0.78), None)
        self.assertEqual(
            select([ineligible, high_average, high_minimum], (0.90, 0.90), 0.75),
            high_minimum,
        )
        self.assertIsNone(select([ineligible], (0.90, 0.90), 0.75))

    def test_residual_interval_scales_with_unresolved_mass(self):
        wins = torch.tensor([500.0])
        plain = interval(0, 1, wins, 1_000)
        residual = interval(0.4, 0.2, wins, 1_000)
        torch.testing.assert_close((residual[0] + residual[1]) / 2, torch.tensor([0.5]))
        torch.testing.assert_close(residual[1] - residual[0], 0.2 * (plain[1] - plain[0]))


if __name__ == "__main__":
    unittest.main()
