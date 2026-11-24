from collections import Counter
from dataclasses import replace
from json import loads
from pathlib import Path
from subprocess import run
from sys import executable
from tempfile import TemporaryDirectory
import unittest

from .agent import Scripted, episode, interpret
from .environment import Outcome, public_evidence, recipe, retention_probes, score, stream
from .memory import (ARMS, AutoSkill, Experience, KnowledgeCards, Memory, OpenSkill,
                      Recall, Reflection, SkillLibrary, SkillMCP, encode)
from .metrics import curve, interval, run_metrics, with_deltas
from .run import trial


def event(task, success=True, lesson="Check the current API"):
    prog = recipe(task.family, task.phase == "post")
    return Experience(task, Outcome(success, "Runtime feedback", prog), encode(prog),
                      lambda: lesson, lambda: public_evidence(task))


class EnvironmentTest(unittest.TestCase):
    def test_seeded_stream_and_held_out_probes(self):
        tasks = stream(11, 16, 12)
        self.assertEqual(tasks, stream(11, 16, 12))
        self.assertNotEqual(tasks, stream(23, 16, 12))
        self.assertEqual([t.step for t in tasks], list(range(28)))
        self.assertEqual(Counter(t.family for t in tasks[:16]), {i: 2 for i in range(8)})
        self.assertEqual(Counter(t.family for t in tasks[16:]), {i: 3 for i in range(4, 8)})
        self.assertEqual([t.step for t in tasks if t.coaching], [*range(8), *range(20, 24)])
        probes = retention_probes(11)
        self.assertEqual(Counter(t.family for t in probes), {i: 2 for i in range(4)})
        self.assertTrue(all(not t.coaching and t.entity.startswith("p") for t in probes))
        self.assertTrue(all(score(t, recipe(t.family, False), True).success for t in probes))
        with self.assertRaises(ValueError):
            stream(11, 9, 12)

    def test_verifier_checks_endpoint_argument_order_and_effect(self):
        task = next(t for t in stream(11, 16, 12) if t.family == 4 and t.phase == "post")
        program = recipe(4, True)
        self.assertTrue(score(task, program, True).success)
        self.assertIn("Unknown endpoint", score(task, recipe(4, False), True).feedback)
        self.assertIn("requires argument", score(task, (program[0], ("approve", "bill")), True).feedback)
        self.assertIn("prerequisite", score(task, tuple(reversed(program)), True).feedback)
        self.assertFalse(score(task, recipe(5, True), True).success)
        for invalid in ("fenced", "[]", '{"tool":"missing"}', '{"calls":[["approve",3]]}'):
            self.assertFalse(interpret(invalid, Memory(), task, True).success)


class MemoryTest(unittest.TestCase):
    def setUp(self):
        tasks = stream(11, 16, 12)
        self.taught = next(t for t in tasks[:8] if t.family == 4)
        self.stale = next(t for t in tasks[16:20] if t.family == 4)
        self.updated = next(t for t in tasks[20:24] if t.family == 4)

    def test_verified_library_and_callable_mcp(self):
        library = SkillLibrary()
        mcp = SkillMCP()
        for arm in (library, mcp):
            arm.write(event(self.taught, success=False))
            self.assertFalse(arm.entries)
            arm.write(event(self.taught))
        self.assertEqual(library.read(self.stale).hint, self.taught.coaching)
        self.assertNotIn("review", str(mcp.read(self.stale).tools))
        raw = '{"tool":"skill_4"}'
        self.assertTrue(interpret(raw, mcp, self.taught, False).success)
        self.assertIn("Unknown endpoint", interpret(raw, mcp, self.stale, True).feedback)
        error = mcp.rpc({"id": 3, "method": "tools/call",
                         "params": {"name": "skill_4", "arguments": {"extra": "value"}}})
        self.assertEqual(error["error"]["code"], -32602)
        mcp.write(event(self.updated))
        self.assertTrue(interpret(raw, mcp, self.updated, True).success)

    def test_openskill_rejects_lagging_doc_and_ignores_hidden_score(self):
        arm = OpenSkill()
        arm.write(event(self.taught, success=False))
        self.assertEqual(arm.read(self.stale).hint, self.taught.coaching)
        arm.write(event(self.stale, success=True))
        self.assertEqual(arm.read(self.stale).hint, self.taught.coaching)
        arm.write(event(self.updated, success=False))
        self.assertEqual(arm.read(self.updated).hint, self.updated.coaching)
        self.assertIn("mock-manual/4/v2", arm.read(self.updated).text)

    def test_autoskill_add_discard_and_versioned_revision(self):
        arm = AutoSkill()
        arm.write(event(self.stale))
        self.assertFalse(arm.entries)
        arm.write(event(self.taught, success=False))
        arm.write(event(self.taught, success=False))
        self.assertEqual(arm.entries["skill_4"].version, 1)
        arm.write(event(self.updated, success=False))
        self.assertEqual(arm.read(self.updated).hint, self.updated.coaching)
        self.assertEqual(arm.entries["skill_4"].version, 2)

    def test_reflection_on_failures_and_structured_cards_on_success(self):
        reflection = Reflection()
        cards = KnowledgeCards()
        for i in range(5):
            reflection.write(event(self.taught, success=False, lesson=f"Lesson {i}"))
        reflection.write(event(self.updated, lesson="No lesson on success"))
        self.assertNotIn("Lesson 1", reflection.read(self.stale).text)
        self.assertIn("Lesson 2", reflection.read(self.stale).text)
        self.assertNotIn("No lesson on success", reflection.read(self.stale).text)
        cards.write(event(self.taught, success=False))
        self.assertFalse(cards.read(self.stale).text)
        cards.write(event(self.taught))
        card = loads(cards.read(self.stale).text.removeprefix("Knowledge Card: "))
        self.assertEqual(card["provenance"], f"episode/{self.taught.step}")
        self.assertEqual(card["rule"]["calls"], [list(call) for call in self.taught.coaching])
        self.assertIn("invalid", card["scope"])

    def test_bank_budget_and_no_updates_during_probe(self):
        arm = SkillLibrary()
        for task in stream(11, 8, 8)[:8]:
            arm.write(event(task))
        self.assertEqual(len(arm.entries), arm.limit)
        self.assertEqual(sorted(e.step for e in arm.entries.values()), list(range(2, 8)))
        before = arm.entries.copy()
        for task in retention_probes(11):
            episode(Scripted(), arm, task, 1, True, False)
        self.assertEqual(arm.entries, before)

    def test_failure_triggered_pull_is_opt_in_and_bounded(self):
        class Pull(Memory):
            def after_failure(self, task, outcome):
                return Recall(hint=recipe(task.family, True))

        class FailThenAct(Scripted):
            def act(self, task, recall, seed):
                return super().act(task, recall, seed) if recall.hint else "{}"

        task = replace(self.updated, coaching=())
        _, outcome, first_feedback, attempts = episode(FailThenAct(), Pull(), task, 1, True, True)
        self.assertTrue(outcome.success)
        self.assertEqual(attempts, 2)
        self.assertIn("Expected two", first_feedback)
        self.assertEqual(episode(FailThenAct(), Memory(), task, 1, True, True)[3], 1)


class RunnerTest(unittest.TestCase):
    def test_paired_curve_and_interval(self):
        control = {1: [{"success": True}, {"success": False}],
                   2: [{"success": False}, {"success": True}]}
        candidate = {s: [{"success": True}, {"success": True}] for s in control}
        indices = [[0, 0], [0, 1], [1, 1]]
        self.assertEqual(interval([2, 2], indices), {"mean": 2, "low": 2, "high": 2})
        self.assertEqual(curve(candidate, control, indices)[1]["cumulative_gain"],
                         {"mean": 1, "low": 1, "high": 1})
        deltas = with_deltas({1: {"success": 1, "cumulative_success": 2}},
                             {1: {"success": 0.5, "cumulative_success": 1}})
        self.assertEqual(deltas[1]["success_gain"], 0.5)

    def test_recovery_censoring_and_forgetting(self):
        def row(phase, family, success):
            return dict(phase=phase, family=family, success=success, coached=False)

        rows = [row("pre", 4, 1), row("pre", 5, 1), row("probe-before", 0, 1),
                row("post", 4, 1), row("post", 6, 1), row("post", 5, 0), row("probe-after", 0, 0)]
        result = run_metrics(rows, 2)
        self.assertEqual(result["forgetting"], 1)
        self.assertEqual(result["post_auc"], 2 / 3)
        self.assertEqual(result["affected_post_auc"], 1 / 2)
        self.assertEqual(result["recovered"], 0)
        self.assertEqual(result["recovery_restricted_steps"], 4)
        changed = [{**r, "success": True} if r["phase"] == "post" else r for r in rows]
        self.assertEqual(run_metrics(changed, 2)["recovery_restricted_steps"], 3)

    def test_runs_all_arms_and_writes_artifacts(self):
        with TemporaryDirectory() as temp:
            proc = run([executable, "-m", "skill_memory.run", "--pre", "8", "--post", "8",
                        "--seeds", "11", "23", "--recovery-window", "2",
                        "--draws", "10", "--output", temp],
                       check=True, text=True, capture_output=True)
            root = Path(temp)
            results = loads((root / "results.json").read_text())
            self.assertEqual(set(results["summary"]), set(ARMS))
            self.assertEqual(len((root / "episodes.csv").read_text().splitlines()), 1 + 7 * 2 * 32)
            self.assertEqual(len(loads((root / "curves.json").read_text())["reflection"]), 16)
            self.assertIn("Recovery steps", proc.stdout)
            self.assertIn("knowledge-cards", (root / "summary.md").read_text())
        rows = trial(Scripted(), "skill-library", 11, 16, 12)
        self.assertEqual(rows, trial(Scripted(), "skill-library", 11, 16, 12))


if __name__ == "__main__":
    unittest.main()
