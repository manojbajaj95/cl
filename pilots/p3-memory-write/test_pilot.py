import unittest

import numpy as np

from analyze import bootstrap_indices, paired, summarize, wilson
from pilot import (ARMS, MASK_THRESHOLD, actor_prompt, episodes, is_defective, is_solved, relevance_mask,
                   writer_prompt, writer_variants)


class PilotTests(unittest.TestCase):
    def test_exact_replication_cohort_has_balanced_tasks_and_one_corruption(self):
        rows = list(episodes(5))
        self.assertEqual(len({row["id"] for row in rows}), 210)
        self.assertEqual(len({(row["target"], row["qty"]) for row in rows}), 42)
        for row in rows:
            clean, distractor = map(row["contexts"].get, ("clean", "distractor"))
            self.assertEqual(len(clean), 4)
            self.assertEqual([i for i, pair in enumerate(zip(clean, distractor)) if pair[0] != pair[1]],
                             [row["swap_idx"]])

    def test_judges_reuse_source_numeric_rule(self):
        self.assertFalse(is_defective("Use 1.60934 as the factor.", 1.609))
        self.assertTrue(is_defective("Multiply by 1.2.", 1.609))
        self.assertTrue(is_solved("Using 1.609, the result is 3.218.", 3.218))
        self.assertFalse(is_solved("3.218, using 1.609.", 3.218))
        self.assertFalse(is_solved("", 3.218))

    def test_relevance_mask_scores_fixed_actions_under_independent_removals(self):
        ep = next(episodes(1))
        context = ["neutral observation", "relevant observation"]
        prompts = []

        class Scorer:
            def action_logprobs(self, prompt, action):
                prompts.append(prompt)
                self_outer.assertEqual(action, [12, 34])
                if "relevant observation" not in prompt:
                    return np.array([-2.0, -0.8])
                return np.array([-1.0, -1.0])

        self_outer = self
        retained, scores = relevance_mask(Scorer(), ep, context, [12, 34])
        self.assertEqual(retained, context[1:])
        self.assertLess(scores[0], MASK_THRESHOLD)
        self.assertGreater(scores[1], MASK_THRESHOLD)
        self.assertEqual(prompts, [actor_prompt(ep, c) for c in (context, context[1:], context[:1])])

    def test_variants_reuse_answer_and_writer_seed_and_trace_has_no_observations(self):
        ep = next(episodes(1))
        answer = "My cached answer"
        ep["arms"] = {"distractor": {"answer": answer, "action_tokens": [12, 34],
                                      "writes": {"baseline": {"input_tokens": 50}}}}
        calls = []

        class FakeModel:
            def tokens(self, prompt):
                return [0] * 50

            def generate(self, prompt, seed, temperature):
                calls.append((prompt, seed, temperature))
                return "New write", []

            def action_logprobs(self, prompt, action):
                return np.zeros(len(action))

        writer_variants(FakeModel(), ep)
        self.assertEqual(len(calls), 3)
        self.assertTrue(all(answer in prompt and seed == ep["writer_seed"] and temp == 0.7
                            for prompt, seed, temp in calls))
        trace = calls[1][0]
        self.assertEqual(trace, writer_prompt(ep, [], answer, "trace"))
        self.assertNotIn("Task:", trace)
        self.assertNotIn(ep["target"][0], trace)
        self.assertIn("Write only about the task.", calls[2][0])

    def test_contrast_accounts_for_paired_solve_failure(self):
        rows = list(episodes(5))
        for row in rows:
            row["model_sha256"] = "test"
            row["arms"] = {arm: {"solved": arm != "distractor", "actor_input_tokens": 50,
                                "writes": {"baseline": {"bad": arm == "distractor"}}} for arm in ARMS}
        contrast = summarize(rows, "baseline")["arm_contrasts"]["distractor_minus_filler"]
        self.assertEqual(contrast["bad_write"]["difference"], 1.0)
        self.assertEqual(contrast["solve_failure"]["difference"], 1.0)
        self.assertEqual(contrast["write_minus_failure_gap"], {"difference": 0.0, "ci95": [0.0, 0.0]})
        self.assertGreater(wilson([0] * 210)["ci95"][1], 0.0)

    def test_stratified_bootstrap_keeps_stratum_counts(self):
        rows = list(episodes(2))
        task = rows[0]["target"]
        one_task = np.array([row["target"] == task for row in rows], dtype=int)
        result = paired(one_task, bootstrap_indices(rows, draws=100))
        self.assertEqual(result, {"difference": 1/6, "ci95": [1/6, 1/6]})


if __name__ == "__main__":
    unittest.main()
