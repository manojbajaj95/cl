import unittest

import numpy as np
import torch

from pilot import PROBES, RANK, VERSIONS, kl, make_tasks, rank_one
from summarize import format_ci


class PilotTest(unittest.TestCase):
    def test_three_splits_are_disjoint(self):
        prompts, labels, train, test, probes = make_tasks()
        rows = torch.cat([*train, *test, probes])
        self.assertEqual(len(train), VERSIONS)
        self.assertEqual(len(probes), PROBES)
        self.assertEqual(len(rows.unique()), len(prompts))
        self.assertEqual(len(rows), len(labels))
        for task in test:
            self.assertEqual(labels[task].sum().item(), len(task) // 2)

    def test_budget_matched_storage_is_best_rank_one(self):
        g = torch.Generator().manual_seed(3)
        a = torch.randn(13, RANK, generator=g)
        b = torch.randn(RANK, 22, generator=g)
        x, y = rank_one((a, b))
        u, s, vh = torch.linalg.svd(a @ b, full_matrices=False)
        torch.testing.assert_close(x @ y, u[:, :1] * s[:1] @ vh[:1], atol=1e-5, rtol=1e-5)
        self.assertEqual(VERSIONS * (x.numel() + y.numel()), a.numel() + b.numel())

    def test_kl_direction(self):
        p = torch.tensor([0.25, 0.75])
        q = torch.tensor([0.5, 0.5])
        self.assertAlmostEqual(kl(p.log(), q.log()).item(), 0.130812, places=6)
        self.assertNotAlmostEqual(kl(p.log(), q.log()).item(), kl(q.log(), p.log()).item())
        self.assertEqual(kl(p.log(), p.log()).item(), 0)

    def test_seed_bootstrap(self):
        draws = np.array([[0, 0], [1, 1]])
        self.assertEqual(format_ci([1, 3], draws, 2), "2.00 [1.05, 2.95]")


if __name__ == "__main__":
    unittest.main()
