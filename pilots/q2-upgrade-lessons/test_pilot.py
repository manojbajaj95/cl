import unittest

import numpy as np

from analysis import analyze, compare, gains_on_successful_actions, source_scores, truth_gate
from collect import N_PACKS, Scorer, pruning_check
from tasks import ACTIONS, CODES, SOURCE, STEPS, TRUTH_HALVES, correct, episodes, exact_success, transition


class RouterTests(unittest.TestCase):
    def test_source_and_held_out_are_disjoint_and_stratified(self):
        self.assertEqual(len(set(SOURCE + TRUTH_HALVES[0] + TRUTH_HALVES[1])), CODES)
        for half in TRUTH_HALVES:
            self.assertEqual(sorted(code % 3 for code in half), [0, 1, 2])

    def test_uniform_policy_has_binomial_success_probability(self):
        uniform = np.full((3, STEPS, CODES, len(ACTIONS)), -np.log(3))
        np.testing.assert_allclose(exact_success(uniform), 7 / 27)

    def test_exact_and_sampled_rollouts_follow_action_dependent_transitions(self):
        actions = (np.arange(CODES) + np.arange(STEPS)[:, None]) % len(ACTIONS)
        policy = np.full((STEPS, CODES, len(ACTIONS)), -np.inf)
        np.put_along_axis(policy, actions[..., None], 0, axis=-1)
        log = episodes(policy, 200, 123, tuple(range(CODES)))
        for step in range(STEPS - 1):
            np.testing.assert_equal(log["states"][:, step + 1],
                                    transition(log["states"][:, step], log["actions"][:, step], step))
        np.testing.assert_equal(exact_success(policy, log["states"][:, 0]), log["success"])


class ScoreTests(unittest.TestCase):
    def test_pruning_keeps_positive_notes_and_matches_context_length(self):
        prompts = []

        class FakeScorer:
            def post(self, path, body):
                return {"tokens": body["content"].split()}

            def score(self, batch, legal):
                prompts.append(batch[0])
                return np.full((CODES * STEPS, len(legal)), -np.log(len(legal)))

        result = pruning_check(FakeScorer(), ["keep me", "DROP", "a", "b", "c"],
                               np.array([1, -1, 1, 1, 1]))
        self.assertEqual(result["policy"].shape, (N_PACKS, 2, STEPS, CODES, len(ACTIONS)))
        for original, pruned in zip(prompts[::2], prompts[1::2]):
            self.assertIn("DROP", original)
            self.assertNotIn("DROP", pruned)
            self.assertIn("keep me", pruned)
            self.assertEqual(len(original.split()), len(pruned.split()))

    def test_score_normalizes_in_token_id_order(self):
        scorer = Scorer.__new__(Scorer)
        scorer.parallel = 3
        scorer.ids = dict(zip(ACTIONS, (3, 7, 4)))
        result = {"completion_probabilities": [{"top_probs": [
            {"id": 7, "prob": 0.5}, {"id": 4, "prob": 0.3}, {"id": 3, "prob": 0.2},
        ]}]}

        def post(path, body):
            self.assertEqual(path, "/completion")
            self.assertEqual(body["logit_bias"], [[key, 100] for key in (3, 7, 4)])
            self.assertEqual(body["top_k"], len(ACTIONS))
            self.assertTrue(body["post_sampling_probs"])
            return [result for _ in body["prompt"]]

        scorer.post = post
        np.testing.assert_allclose(np.exp(scorer.score(["one", "two"], ACTIONS)), [[0.2, 0.5, 0.3]] * 2)
        result["completion_probabilities"][0]["top_probs"].pop()
        with self.assertRaisesRegex(ValueError, "Unexpected scored token IDs"):
            scorer.score(["one"], ACTIONS)

    def test_primary_uses_logged_correct_actions_not_oracle_replacements(self):
        states = np.zeros((2, STEPS), dtype=int)
        actions = np.array([[2, 1, 2], [2, 0, 0]])
        policy = np.full((2, STEPS, CODES, len(ACTIONS)), -np.log(3))
        policy[1, :, 0] = np.log([[0.2, 0.25, 0.55], [0.6, 0.3, 0.1], [0.7, 0.2, 0.1]])
        expected = (2 * np.log(0.55 * 3) + np.log(0.1 * 3)) / 3
        np.testing.assert_allclose(gains_on_successful_actions(policy, states, actions), [expected])

        lessons = [{"source": [0]}]
        source = {"old": policy, "old_states": states, "old_actions": actions}
        scores = source_scores(lessons, policy, source, np.log([[0.2] * 5]))
        np.testing.assert_allclose(scores["new_likelihood"], [expected])
        np.testing.assert_allclose(scores["new_zero_shot"], [7 / 27])
        np.testing.assert_allclose(scores["new_model_judge"], [3])


class GateTests(unittest.TestCase):
    def setUp(self):
        self.lessons = [{"id": str(i), "kind": "test", "source": [0]} for i in range(4)]
        self.probs = np.full((5, STEPS, CODES, len(ACTIONS)), 1 / 3)

    def test_undefined_reliability_stops_before_reading_source(self):
        result = analyze(self.lessons, np.log(self.probs), source=object())
        self.assertFalse(result["reliability"]["passes"])
        self.assertIsNone(result["reliability"]["raw_spearman"]["estimate"])
        self.assertEqual(result["verdict"], "STOP: unreliable truth")
        self.assertNotIn("rhos", result)

    def test_reliability_gates_on_spearman_brown(self):
        for i, delta in enumerate((0.0, 0.05, 0.10, 0.15), start=1):
            gold = correct(np.arange(CODES))
            self.probs[i, :, np.arange(CODES), gold] += delta
            self.probs[i, :, np.arange(CODES), (gold + 1) % len(ACTIONS)] -= delta
        gate, _ = truth_gate(self.lessons, np.log(self.probs))
        self.assertTrue(gate["passes"])
        self.assertAlmostEqual(gate["raw_spearman"]["estimate"], 1)
        self.assertAlmostEqual(gate["spearman_brown"]["estimate"], 1)

    def test_zero_shot_competes_in_either_direction(self):
        target = np.arange(4)
        rhos, margins = compare({"new_likelihood": target, "new_zero_shot": -target}, target,
                                np.array([[0, 1, 2, 3], [3, 3, 2, 1]]))
        self.assertAlmostEqual(rhos["new_zero_shot"]["estimate"], -1)
        self.assertAlmostEqual(margins["new_zero_shot"]["estimate"], 0)
        np.testing.assert_allclose(margins["new_zero_shot"]["ci"], [0, 0], atol=1e-12)


if __name__ == "__main__":
    unittest.main()
