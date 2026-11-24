import math
import unittest

import torch

from decoder import branches, leaf_logprobs
from pilot import auxiliary, effect_weights, hypervolume, interval, setup
from stream import parse


class StreamTests(unittest.TestCase):
    def test_migrated_aliases_preserve_probe_and_test_outputs(self):
        data, _, calls, targets, _, _ = setup()
        for row, prompt in enumerate(data):
            old = calls[row][targets[False][row]]
            new = calls[row][targets[True][row]]
            self.assertFalse(old.new)
            self.assertTrue(new.new)
            self.assertEqual(prompt.observe(old), prompt.observe(new))
            self.assertTrue(prompt.observe(new)[1])
            if prompt.operation == 1:
                self.assertEqual(old.order, new.order[::-1])
            n = len({prompt.observe(call)[0] for call in calls[row]})
            self.assertEqual(n, 6)

    def test_canonical_groups_merge_formats_but_not_api_names(self):
        _, _, _, targets, ids, _ = setup()
        self.assertEqual(ids[0], ids[1])
        self.assertTrue((ids[targets[False]] != ids[targets[True]]).all())
        with self.assertRaises(ValueError):
            parse("other.subtract(a, b)", ("a", "b"))


class ReplayTests(unittest.TestCase):
    def test_trie_probability_ignores_forced_tokens(self):
        self.assertEqual(branches([[7, 2, 9], [7, 4, 5], [7, 4, 6]]), [((7,), [2, 4]), ((7, 4), [5, 6])])
        probs = torch.tensor([[[0.3, 0.7], [0.8, 0.2]]])
        paths = torch.tensor([[[0, -1], [1, 0], [1, 1]]])
        torch.testing.assert_close(leaf_logprobs(probs.log(), paths).exp(), torch.tensor([[0.3, 0.56, 0.14]]))

    def test_replay_weights_match_outcomes_not_tokens_or_pass_flags(self):
        a, b, c = ((1,), True), ((2,), False), ((3,), False)
        actual = effect_weights([[a, b, b, b]], [[a, a, b, c]])
        torch.testing.assert_close(actual, torch.tensor([[0.5, 0.5, 3.0, 0.0]]))

    def test_canonical_token_loss_marginalizes_formatting(self):
        probs = torch.tensor([[0.1, 0.2, 0.3, 0.4]])
        loss = auxiliary("token", probs.log(), torch.tensor([[0, 1]]), None, None, None,
                         torch.tensor([0, 0, 1, 1]), torch.tensor([[0, 1], [2, 3]]))
        self.assertAlmostEqual(loss.item(), -math.log(0.3), places=6)

    def test_hypervolume_ignores_dominated_points_and_ci_pairs(self):
        self.assertAlmostEqual(hypervolume([(0.5, 0.9), (0.9, 0.7), (0.4, 0.6)]), 0.73)
        self.assertEqual(interval([0.125, 0.125, 0.125]), [0.125, 0.125, 0.125])
        self.assertLess(interval([-0.1, 0.0, 0.1])[1], 0)


if __name__ == "__main__":
    unittest.main()
