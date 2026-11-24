import unittest

import numpy as np
import torch

from pilot import JAM, MODES, N, P, RARE_TILT, REPLAY_BATCH, Policy, Replay, adapt, interval, natural, reverse_kl, trace_replay
from q1_gate import gate


class ReplayTest(unittest.TestCase):
    def setUp(self):
        self.route = np.linspace(0.25, 0.75, P)
        self.rng = np.random.default_rng(3)
        self.replay = Replay(self.route, natural(self.rng, 100_000, self.route))

    def test_proposals_match_sampler_and_have_full_support(self):
        sample_size = 80_000
        for mode in MODES:
            with self.subTest(mode=mode):
                q = self.replay.q[mode]
                self.assertAlmostEqual(q.sum(), 1.0)
                self.assertTrue((q > 0).all())
                _, status, weights, _, _ = self.replay.sample(self.rng, mode, sample_size)
                jams = status == JAM
                self.assertAlmostEqual(jams.mean(), q[..., JAM].sum(), delta=0.002)
                self.assertAlmostEqual(weights.mean(), 1.0, delta=0.03)
        self.assertAlmostEqual(self.replay.p[..., JAM].sum(), 0.001)
        self.assertAlmostEqual(self.replay.target[..., JAM].sum(), RARE_TILT / (999 + RARE_TILT))

    def test_costs_and_split_fanout(self):
        starts, _, _, roots, transitions = self.replay.sample(self.rng, "split", 16)
        self.assertEqual((roots, transitions), (8, 16))
        for child_group in starts[8:].reshape(2, 4, 2):
            np.testing.assert_array_equal(child_group, np.repeat(child_group[:1], 4, axis=0))
        _, _, _, roots, transitions = self.replay.sample(self.rng, "mopd", 16)
        self.assertEqual((roots, transitions), (16, 16))
        _, _, _, roots, transitions = self.replay.sample(self.rng, "terminal_replay", 16)
        self.assertEqual((roots, transitions), (8, 8))

    def test_distillation_zero_at_teacher(self):
        logits = torch.tensor([-8.0, 0.0, 5.0])
        torch.testing.assert_close(reverse_kl(logits, logits), torch.zeros(3))
        self.assertTrue((reverse_kl(logits, -logits) >= 0).all())

    def test_training_budgets_match_and_teacher_stays_frozen(self):
        previous = Policy({"z": torch.ones(2, N, 2, 3, 2), "base": torch.zeros(2, N, 2, 3)})
        batches = [natural(self.rng, 16, self.route) for _ in range(3)]
        for mode in MODES:
            with self.subTest(mode=mode):
                _, budget = adapt(previous, batches, self.replay, mode, seed=5)
                for name in ("replay_rollouts", "replay_teacher_positions", "replay_sampled_actions"):
                    self.assertEqual(budget[name], len(batches) * REPLAY_BATCH)
                self.assertEqual(budget["new_rollouts"], 48)
                self.assertEqual(budget["new_teacher_positions"], 48)
        torch.testing.assert_close(previous.adapter, torch.zeros(2))

    def test_seed_ci(self):
        ci = interval([0.1, 0.2, 0.3])
        self.assertAlmostEqual(ci["mean"], 0.2)
        self.assertAlmostEqual(ci["high"] - ci["mean"], 0.248414, places=6)

    def test_replay_trace_matches_individual_adapter_gradients(self):
        z = torch.arange(2 * N * 2 * 3 * 2, dtype=torch.float32).reshape(2, N, 2, 3, 2)
        policy = Policy({"z": z / z.max(), "base": torch.zeros(2, N, 2, 3)})
        starts = np.array([[0, 0], [1, 0]])
        status = np.array([JAM, 0])
        student = policy.logits(0, starts, status)
        losses = reverse_kl(student, torch.tensor([2., -1.])) * torch.tensor([.4, .03])
        jam, norms, logged_loss = trace_replay(policy, starts, status, student, losses)
        expected = [torch.autograd.grad(loss, policy.adapter, retain_graph=True)[0].norm().item()
                    for loss in losses]
        np.testing.assert_array_equal(jam, [True, False])
        np.testing.assert_allclose(norms, expected, rtol=1e-6)
        np.testing.assert_array_equal(logged_loss, losses.detach().numpy())
        self.assertIsNone(policy.adapter.grad)

    def test_replay_logging_does_not_change_training(self):
        previous = Policy({"z": torch.ones(2, N, 2, 3, 2), "base": torch.zeros(2, N, 2, 3)})
        batches = [natural(self.rng, 16, self.route) for _ in range(3)]
        plain, plain_budget = adapt(previous, batches, self.replay, "terminal_replay", seed=5)
        trace = []
        logged, logged_budget = adapt(previous, batches, self.replay, "terminal_replay", seed=5,
                                      replay_trace=trace)
        torch.testing.assert_close(plain.adapter, logged.adapter, rtol=0, atol=0)
        self.assertEqual(plain_budget, logged_budget)
        self.assertEqual(len(trace), len(batches))
        self.assertEqual(sum(jam.sum() for jam, _, _ in trace), logged_budget["replay_jams"])

    def test_noise_gate_compares_seed_variance_to_arm_mean_variance(self):
        recovery = np.array([[0., 3.], [2., 5.]])
        paired = np.array([[0, 1], [0, 0], [1, 1], [1, 0]])
        result = gate(recovery, paired)
        self.assertTrue(result["proceed"])
        self.assertEqual(result["within"]["estimate"], 2.)
        self.assertEqual(result["across"], dict(estimate=4.5, low=4.5, high=4.5))
        self.assertFalse(gate(recovery / [1, 2], paired)["proceed"])


if __name__ == "__main__":
    unittest.main()
