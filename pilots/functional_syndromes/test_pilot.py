import tempfile
import unittest
from pathlib import Path

import numpy as np
import torch
from transformers import GPT2Config, GPT2LMHeadModel

from analyze import compare, concentration, dense_ls, read_checks, somp
from run_pilot import PilotModel, memit_update, pad


class MemitPipelineTests(unittest.TestCase):
    def test_frozen_prefix_and_suffix_agree_with_gpt2_on_real_tokens(self):
        config = GPT2Config(vocab_size=17, n_embd=12, n_layer=3, n_head=3, n_positions=8)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            GPT2LMHeadModel(config).save_pretrained(path)
            model = PilotModel(path)
            inputs = [[1, 2, 3, 4], [6, 5]]
            with torch.no_grad():
                partial = model.advance(model.embed(pad(inputs)), 0, 1)
                logits = model.logits(model.advance(partial, 1, 3))
                for row, ids in enumerate(inputs):
                    expected = model.model(torch.tensor([ids]), use_cache=False).logits
                    torch.testing.assert_close(logits[row, :len(ids)], expected[0])

    def test_memit_solves_regularized_residual_with_conv1d_layout(self):
        keys = torch.tensor([[1., 0., 2.], [0., 0., 1.]])
        residual = torch.tensor([[2., -1.], [1., 3.]])
        cov = torch.diag(torch.tensor([1., 2., 3.], dtype=torch.float64))
        weight = 7
        update = memit_update(keys, residual, cov, weight)
        self.assertEqual(tuple(update.shape), (3, 2))
        actual = (weight * cov + keys.double().T @ keys.double()) @ update.double()
        torch.testing.assert_close(actual, (keys.T @ residual).double())


class SyndromeTests(unittest.TestCase):
    def test_projection_reads_combined_keys_and_matches_column_algebra(self):
        rng = np.random.default_rng(45)
        keys = rng.normal(size=(2, 7, 8))
        before, after = rng.normal(size=(2, 2, 8, 4))
        codes = rng.normal(size=(3, 7))
        result = read_checks(codes, keys, after - before)
        wanted = np.concatenate([codes @ (k @ w) for k, w in zip(keys, after - before)], axis=1)
        stored = [(codes @ k) @ w for k, w in zip(keys, before)]
        readings = np.concatenate([(codes @ k) @ w - ref for k, w, ref in zip(keys, after, stored)], axis=1)
        np.testing.assert_allclose(result, wanted)
        np.testing.assert_allclose(result, readings)

    def test_sparse_control_and_dense_least_squares(self):
        rng = np.random.default_rng(46)
        c = rng.normal(size=(20, 100))
        effects = np.zeros((100, 3))
        effects[[6, 9]] = [[3, 4, 0], [-1, 0, 2]]
        measured = c @ effects
        self.assertEqual(set(somp(c, measured, 2)), {6, 9})
        explicit = np.linalg.lstsq(c, measured, rcond=None)[0]
        expected = np.argsort(-np.linalg.norm(explicit, axis=1))[:5]
        np.testing.assert_array_equal(dense_ls(c, measured, 5), expected)
        self.assertEqual(concentration((effects**2).sum(axis=1)), 1)
        self.assertEqual(concentration(np.ones(100)), 0.1)

    def test_recovery_has_same_budget_and_prediction_count(self):
        rng = np.random.default_rng(47)
        keys = rng.normal(size=(2, 40, 8)).astype(np.float32)
        w = rng.normal(size=(2, 8, 4)).astype(np.float32)
        v = rng.normal(size=(2, 40, 4)).astype(np.float32)
        damage = sum(((k @ d)**2).sum(axis=1) for k, d in zip(keys, w))
        result = compare(keys, w, v, damage, 4, 2, rng)
        self.assertEqual(result["bytes_each"], 4 * 2 * (8 + 4) * 4)
        for metric in result["metrics"].values():
            self.assertEqual(metric["recall"]["estimate"], metric["precision"]["estimate"])


if __name__ == "__main__":
    unittest.main()
