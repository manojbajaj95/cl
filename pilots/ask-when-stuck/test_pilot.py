import unittest

from analyze import interval, prospective_confidence
from benchmark import alternatives, decision
from entropy import fit
from pilot import MODES, SLOT, TOP_K, allocate, embedding, note, rescale, retrieve, select


class PilotTests(unittest.TestCase):
    def test_bottleneck_selection_and_menu(self):
        self.assertEqual(decision(["take apple 1", "heat apple 1", "move apple 1"]), 1)
        self.assertEqual(decision(["move apple 1", "take apple 2", "move apple 2"]), 2)
        ref = "heat apple 1 with microwave 1"
        legal = [ref, "look", "heat apple 2 with microwave 1"]
        menu = alternatives(ref, legal)
        self.assertEqual(len(set(menu)), 4)
        self.assertEqual(set(menu) & set(legal), {ref, "look"})

    def test_equal_budget_without_equating_the_triggers(self):
        cases = [
            {"outcomes": [{"won": won, "feedback": feedback}]}
            for won, feedback in [(True, "Done"), (False, "Nothing happens."),
                                  (False, "Looked around"), (False, "Nothing happens.")]
        ]
        initial = [(0, p, 10) for p in (0.2, 0.9, 0.4, 0.6)]
        allocations = allocate(initial, cases, 42)
        self.assertEqual(allocations["failure"], {1, 3})
        self.assertEqual(allocations["confidence"], {2, 3})
        self.assertEqual(set(allocations), set(MODES))
        self.assertEqual({len(allocations[m]) * SLOT * TOP_K
                          for m in MODES if m != "push_always"}, {2 * SLOT * TOP_K})

    def test_unchanged_rank_on_corruption(self):
        a = dict(goal="heat an apple", initial="microwave", operation="heat", corrupt=True)
        b = dict(goal="cool a tomato", initial="fridge", operation="cool", corrupt=False)
        self.assertEqual(embedding(a), embedding(dict(a, corrupt=False)))
        self.assertEqual(retrieve(embedding(a), [embedding(b), embedding(a)], 2), (1, 0))
        self.assertNotEqual(note(a, True), note(a, False))
        self.assertEqual(note(b, True), note(b, False))

    def test_paired_interval_is_on_differences(self):
        self.assertEqual(interval([2] * 5), {"mean": 2, "lo": 2, "hi": 2})
        result = interval([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result["lo"], 1.0367568385)
        self.assertAlmostEqual(result["hi"], 4.9632431615)

    def test_prospective_control_can_rescore_a_correct_action_and_charges_probe(self):
        def row(won, queried):
            return dict(won=won, first_won=won, queries=queried, corrupt=0, corrupt_hit=False,
                        calls=2 - won, input_tokens=40, memory_tokens=TOP_K * SLOT if queried else 0)

        block = {
            "methods": {"180/1/failure": {"queries": 1}},
            "traces": [
                dict(confidence=0.4, first_tokens=20,
                     trials={"none": row(True, False), "180/1/push_always": row(False, True)}),
                dict(confidence=0.7, first_tokens=22,
                     trials={"none": row(False, False), "180/1/push_always": row(True, True)}),
            ],
        }
        totals = prospective_confidence(block, 180, True)
        self.assertEqual(totals["queries"], 1)
        self.assertEqual(totals["won"], 0)
        self.assertEqual(totals["calls"], 5)
        self.assertEqual(totals["input_tokens"], 100)

    def test_entropy_fit_and_temperature_sampling(self):
        base = [0.7, 0.2, 0.09, 0.01]
        target = rescale(base, 2)
        outcome = fit([(0.6, base, target)])
        self.assertAlmostEqual(outcome["temperature"], 2)
        self.assertAlmostEqual(outcome["matched_entropy_nats"], outcome["memory_entropy_nats"])
        self.assertEqual(select(base), select(target))
        self.assertNotEqual(select(base, 0.65), select(target, 0.65))


if __name__ == "__main__":
    unittest.main()
