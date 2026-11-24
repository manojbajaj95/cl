import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import numpy as np

from .backends import Stub
from .environment import HELD_OUT, SEEDS, TRAIN, make_task
from .pilot import ARMS, Trace, cluster, discover, gate_stats, medoid, run
from .semantic import conflicts


class PilotTest(unittest.TestCase):
    def stub(self, tasks, gate_only=False, proposal_batch_size=1, curation_batch_size=1):
        args = argparse.Namespace(backend="stub", tasks=tasks, held_out_tasks=tasks, workers=1, validation_blocks=1,
                                  top_k=5, bootstrap=50, gate_only=gate_only, proposal_batch_size=proposal_batch_size,
                                  curation_batch_size=curation_batch_size)
        with contextlib.redirect_stderr(io.StringIO()):
            return run(args)

    def test_protocol_counterfactuals_preserve_records_and_question(self):
        for family in (*TRAIN, HELD_OUT):
            for i in range(30):
                task = make_task(family, i)
                prompts = [task.prompt(v) for v in range(3)]
                base, reordered = [json.loads(p.split(": ", 1)[1].split("\nQuestion:")[0]) for p in prompts[:2]]
                indexed = json.loads(prompts[2].split("\n", 2)[2]).values()
                as_multiset = lambda rows: Counter(json.dumps(r, sort_keys=True) for r in rows)
                self.assertEqual(as_multiset(base), as_multiset(reordered))
                self.assertEqual(as_multiset(base), as_multiset(indexed))
                self.assertIn("Question: " + task.question, prompts[2])
                self.assertEqual(len(set(task.choices)), 3)
                self.assertIn(task.answer, task.choices)
                for prompt in prompts:
                    choices = prompt.split("Choose one of: ", 1)[1].split(".", 1)[0]
                    self.assertEqual(set(map(int, choices.split(", "))), set(task.choices))

    def test_clustering_keeps_distinct_numeric_instructions_and_distinct_origins(self):
        traces = [
            Trace(TRAIN[0], 0, SEEDS[0], "Check source tokens carefully before returning result.", False, True),
            Trace(TRAIN[1], 0, SEEDS[0], "Check source tokens before returning result!", True, True),
            Trace(TRAIN[0], 1, SEEDS[0], "Repeat operation 2 times.", False, False),
            Trace(TRAIN[1], 1, SEEDS[0], "Repeat operation 3 times.", False, False),
        ]
        groups = cluster(traces)
        self.assertEqual([2, 1, 1], [len(group) for group in groups])
        self.assertEqual(medoid(groups[0]), traces[1].edit)

    def test_gate_corrects_between_cluster_spread_for_seed_noise(self):
        wide = np.array([[-0.4, -0.5, -0.6], [0, 0.1, -0.1], [0.4, 0.5, 0.6]])
        spread, noise, ratio = gate_stats(wide)
        self.assertAlmostEqual(noise, 0.01)
        self.assertAlmostEqual(spread, 0.25 - 0.01 / 3)
        self.assertGreater(ratio, 1)
        self.assertEqual(gate_stats(np.tile(wide[0], (3, 1)))[0], 0)

    def test_non_ascii_edit_does_not_break_medoid(self):
        trace = Trace(TRAIN[0], 0, SEEDS[0], "先检查所有给定条件再输出答案。", False, True)
        self.assertEqual(medoid(cluster([trace])[0]), trace.edit)

    def test_semantic_clustering_preserves_conflicting_operations(self):
        self.assertTrue(conflicts("Sum values in the records.", "Count records."))
        self.assertTrue(conflicts("Return only the result.", "Show arithmetic first."))
        self.assertTrue(conflicts("Filter values above 4.", "Filter values above 5."))
        self.assertFalse(conflicts("Check whether bounds are inclusive or exclusive.", "Verify included endpoints."))

    def test_correct_choice_position_balanced_across_a_panel(self):
        for family in (*TRAIN, HELD_OUT):
            tasks = [make_task(family, i) for i in range(24)]
            self.assertEqual(Counter(t.choices.index(t.answer) for t in tasks), {0: 8, 1: 8, 2: 8})

    def test_gate_stops_before_arms(self):
        with patch("pilots.convergent_edit.pilot.select", side_effect=AssertionError("gate bypassed")):
            result = self.stub(4)
        self.assertFalse(result["gate"]["passed"])
        self.assertNotIn("arms", result)

    def test_full_smoke_exercises_all_arms(self):
        result = self.stub(30)
        self.assertEqual(len(result["traces"]), 90)
        self.assertGreaterEqual(len(result["clusters"]), 40)
        self.assertGreater(result["cross_family_clusters"], 0)
        self.assertTrue(result["gate"]["passed"])
        self.assertEqual(set(result["arms"]), set(ARMS))
        self.assertEqual(result["verdict"], "kill")
        self.assertTrue(all(result["arms"]["breadth"]["scores"][i] > 1
                            for i in result["arms"]["breadth"]["promoted"]))
        self.assertTrue(all(arm["rho_ci"] and arm["top_k_ci"] for arm in result["arms"].values()))

    def test_batched_gate_only(self):
        result = self.stub(30, gate_only=True, proposal_batch_size=3, curation_batch_size=6)
        self.assertTrue(result["gate"]["passed"])
        self.assertEqual(result["proposal_requests"], 30)
        self.assertEqual(result["curation_requests_if_full"], 8)
        self.assertNotIn("arms", result)

    def test_proposal_batches_never_mix_families(self):
        class FamilyScopedStub(Stub):
            def edit_batch(self, episodes, seed):
                families = {task.family for task, _ in episodes}
                if len(families) != 1:
                    raise AssertionError(f"mixed discovery batch: {families}")
                return super().edit_batch(episodes, seed)

        stub = FamilyScopedStub()
        train = {f: [make_task(f, i) for i in range(4)] for f in TRAIN}
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(len(discover(stub, stub, train, pool, 3)), 12)


if __name__ == "__main__":
    unittest.main()
