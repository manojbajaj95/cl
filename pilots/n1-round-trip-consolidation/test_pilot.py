import unittest

import numpy as np

from fixtures import FAMILIES, make_splits
from pilot import execute, outputs, score
from summarize import bootstrap, report


class PilotTest(unittest.TestCase):
    def test_splits_disjoint(self):
        for family in FAMILIES:
            seen, extra, held = make_splits(101, family)
            self.assertEqual((10, 10, 32), tuple(map(len, (seen, extra, held))))
            self.assertEqual(len({repr(x) for x, _ in seen + extra + held}), 52)
            for x, y in seen + extra + held:
                self.assertEqual(FAMILIES[family][2](x), y)

    def test_worker_scores_real_code_and_blocks_filesystem(self):
        cases = [("abc", "cba"), ("d", "d")]
        self.assertEqual(score(outputs("def transform(x): return x[::-1]", cases), cases), [1, 1])
        self.assertEqual(execute("def transform(x): return open(x).read()",
                                 inputs=["/etc/passwd"]), [[False, None]])

    def test_bootstrap_preserves_pairing(self):
        a = np.arange(36).reshape(3, 12) / 100
        points, draws = bootstrap(np.array([a, a + 0.1]))
        self.assertAlmostEqual(points[1] - points[0], 0.1)
        np.testing.assert_allclose(draws[1] - draws[0], 0.1)

    def test_kill_if_shuffle_ties_or_best_rewrite_is_too_close(self):
        gate = [dict(seed=seed, seen_hits=[1], held_hits=[0])
                for seed in (101, 202, 303)]

        def result(rewrite, shuffle):
            arms = {name: {"held": [[1] * n + [0] * (100 - n)]}
                    for name, n in (("round_trip", 70), ("shuffled", shuffle),
                                    ("rewrite", 40), ("rewrite_refine", rewrite))}
            old = dict(mbpp=[1], seen=[[1]])
            return dict(original=[[0]], arms=arms, retention={"base": old, "round_trip": old})

        self.assertEqual(report(gate, [result(50, 70)] * 3)["decision"]["verdict"], "KILL")
        self.assertEqual(report(gate, [result(67, 50)] * 3)["decision"]["verdict"], "KILL")
        self.assertEqual(report(gate, [result(66, 50)] * 3)["decision"]["verdict"], "KEEP")


if __name__ == "__main__":
    unittest.main()
