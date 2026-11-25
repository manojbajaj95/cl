import unittest

import torch

from metrics import contrasts, flip, match_absorption, oscillates, seed_interval
from run import LESSONS, TARGETS, anchored_kl, contradiction_probes, examples, next_cutoffs, probes, rates


class PilotTest(unittest.TestCase):
    def test_scores_and_targets(self):
        held, feedback = probes(), probes(feedback=True)
        held_scores, feedback_scores = ({s for _, s in rows} for rows in (held, feedback))
        self.assertTrue(held_scores.isdisjoint(feedback_scores))
        self.assertEqual(len(set(TARGETS)), 10)
        for holdout in (held, feedback):
            ideal = [float(score >= LESSONS[i][1]) for i, score in holdout]
            for observed, target in zip(rates(holdout, torch.tensor([[p, 1 - p] for p in ideal])), TARGETS):
                self.assertAlmostEqual(observed, target)
        for cycle in range(1, 4):
            rows = examples(29, cycle)
            self.assertEqual(len(rows), 40)
            self.assertTrue({score for _, score in rows}.isdisjoint(held_scores | feedback_scores))
        self.assertNotEqual(examples(11, 1), examples(29, 1))

    def test_contradictions_and_matched_flips(self):
        rows = contradiction_probes()
        self.assertEqual(len(set(rows)), 30)
        for i, score in rows:
            cutoff = LESSONS[i][1]
            self.assertNotEqual(score >= cutoff, score >= 100 - cutoff)
        kept = dict(base_old=0.4, weights_old=0.60, contradiction_old=0.3)
        held = dict(base_old=0.4, weights_old=0.65, contradiction_old=0.7)
        changed = dict(base_old=0.4, weights_old=0.85, contradiction_old=0.3)
        not_old = dict(base_old=0.4, weights_old=0.49, contradiction_old=0.2)
        matches = match_absorption({i: kept for i in range(4)}, {0: held, 1: changed, 2: not_old})
        self.assertEqual(matches, [(kept, held)])
        self.assertTrue(flip(kept))
        self.assertFalse(flip(held))
        self.assertFalse(flip(not_old))

    def test_feedback_uses_target_centered_negative_feedback(self):
        nominal = [cutoff for _, cutoff in LESSONS]
        self.assertEqual(next_cutoffs(TARGETS), nominal)
        self.assertEqual(next_cutoffs([t + 0.07 for t in TARGETS]), [n + 7 for n in nominal])
        self.assertEqual(next_cutoffs([t - 0.07 for t in TARGETS]), [n - 7 for n in nominal])
        self.assertEqual(next_cutoffs([0] * len(TARGETS))[0], 0)
        self.assertEqual(next_cutoffs([1] * len(TARGETS))[-1], 100)

    def test_anchor_kl_direction_and_stop_gradient(self):
        plain = torch.tensor([[0.8, 0.2]]).log().requires_grad_()
        context = torch.tensor([[0.4, 0.6]]).log().requires_grad_()
        loss = anchored_kl(plain, context)
        expected = (plain.exp() * (plain - context)).sum()
        torch.testing.assert_close(loss, expected)
        loss.backward()
        self.assertIsNone(plain.grad)
        torch.testing.assert_close(context.grad, -plain.detach().exp())

    def test_growing_oscillation_requires_both_reversals_and_amplitude(self):
        self.assertTrue(oscillates([0.30, -0.04, 0.10, -0.20]))
        self.assertFalse(oscillates([0.10, -0.08, 0.06, -0.04]))
        self.assertFalse(oscillates([0.10, 0.15, 0.20, 0.25]))
        self.assertFalse(oscillates([0.01, -0.02, 0.03, -0.04]))
        self.assertFalse(oscillates([0.10, -0.101, 0.102, -0.103]))

    def test_paired_seed_interval_and_calibration(self):
        self.assertEqual(seed_interval([[0.1, 0.1], [0.1, 0.1]], draws=100), (0.1, 0.1, 0.1))
        row = dict(base=0.5, context=0.25, weights=0.4, both=0.1, evict=0.3, target=0.25, direction=-1)
        vals = contrasts(row)
        self.assertAlmostEqual(vals["signed_both"], 0.15)
        self.assertAlmostEqual(vals["evict_gain"], 0.20)
        self.assertAlmostEqual(vals["evict_vs_context_mae"], 0.05)


if __name__ == "__main__":
    unittest.main()
