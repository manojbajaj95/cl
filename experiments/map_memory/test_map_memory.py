import unittest
from collections import Counter, defaultdict

import numpy as np
import torch

from .arms import name_matcher, retrieve
from .followup import direct_questions, oracle_coordinates
from .run import MIN_GAP, Model, ridge, prompt
from .worlds import AXES, make_world, solve_coordinates, split_anchors


class KillTestData(unittest.TestCase):
    def test_fictional_families_follow_local_graph_and_are_balanced(self):
        for key, axis in AXES.items():
            _, _, names = split_anchors(axis, 41)
            made, facts, questions, witnesses = make_world(axis, names, 8, 60, MIN_GAP[key])
            predecessors = defaultdict(set)
            for fact in facts:
                high, low = (fact.a, fact.b) if fact.positive else (fact.b, fact.a)
                predecessors[high].add(low)
            for x in names:
                predecessors[x].update(y for y in names if axis.anchors[y] < axis.anchors[x])
            local = {frozenset((f.a, f.b)) for f in facts}
            counts = Counter((q.family, q.yes) for q in questions)
            incidence = Counter(name for fact in facts for name in (fact.a, fact.b))
            self.assertTrue(all(incidence[name] == 2 for name in made))
            for new, anchor, comparator, _ in witnesses:
                self.assertIn(frozenset((new, anchor)), local)
                self.assertNotIn(frozenset((new, comparator)), local)
                self.assertGreaterEqual(abs(axis.anchors[anchor] - axis.anchors[comparator]), MIN_GAP[key])
            matched = Counter((q.b, q.yes) for q in questions
                              if q.family == "two_hop" and q.positive and q.b in axis.anchors)
            for _, _, comparator, _ in witnesses:
                self.assertGreater(matched[comparator, True], 0)
                self.assertEqual(matched[comparator, True], matched[comparator, False])
            for q in questions:
                pair = frozenset((q.a, q.b))
                self.assertEqual(pair in local, q.family in ("stated", "inverse"))
                self.assertEqual(counts[q.family, True], counts[q.family, False])
                more, less = (q.a, q.b) if q.yes == q.positive else (q.b, q.a)
                seen, pending = set(), [more]
                while pending:
                    node = pending.pop()
                    if node not in seen:
                        seen.add(node)
                        pending.extend(predecessors[node])
                self.assertIn(less, seen)

    def test_closed_form_solver_uses_reads_not_latitude_and_is_order_independent(self):
        axis = AXES["latitude"]
        _, _, names = split_anchors(axis, 41)
        made, facts, _, _ = make_world(axis, names, 8, 60)
        reads = {name: 3 * axis.anchors[name] + 500 for name in names}
        coords, steps = solve_coordinates(made, facts, reads)
        by_reverse, _ = solve_coordinates(made, facts[::-1], reads)
        np.testing.assert_allclose(list(coords.values()), list(by_reverse.values()))
        for i, fact in enumerate(facts):
            high, low = (fact.a, fact.b) if fact.positive else (fact.b, fact.a)
            chain = made.index(high if high in made else low) // 4
            full = reads | coords
            self.assertAlmostEqual(full[high] - full[low], steps[chain], msg=f"statement {i}")
            self.assertGreater(steps[chain], 0)

    def test_retrieval_and_offsets_use_only_exact_matching_names(self):
        axis = AXES["birth"]
        _, _, names = split_anchors(axis, 41)
        made, facts, qs, _ = make_world(axis, names, 2, 60)
        q = next(q for q in qs if q.family == "inverse")
        relevant = retrieve(q, facts)
        self.assertLessEqual(len(relevant), 4)
        self.assertTrue(relevant)
        self.assertTrue(all({f.a, f.b} & {q.a, q.b} for f in relevant))
        for style in ("completion", "chat-ab", "chat-yes-no", "chat-name"):
            text, spans = prompt(axis, q, (), [f.text(axis) for f in relevant], style, name_matcher(made))
            self.assertEqual([(q.a, text[spans[0][0]:spans[0][1]]),
                              (q.b, text[spans[1][0]:spans[1][1]])], [(q.a, q.a), (q.b, q.b)])
            self.assertTrue(all(text[lo:hi] == name for lo, hi, name in spans))
        self.assertIsNone(name_matcher(made).search(f"x{made[0]}x"))

    def test_pseudoinverse_moves_probe_readout_by_requested_amount(self):
        x = np.array([[1, 1], [1, 2], [3, 1], [3, 3]], dtype=float)
        w, b = ridge(x, np.array([-2, -1, 1, 2]))
        d = w / (w @ w)
        old = x[0] @ w + b
        self.assertAlmostEqual((x[0] + d * (4 - old)) @ w + b, 4)

    def test_followup_uses_only_direct_questions_and_oracle_satisfies_the_world(self):
        axis = AXES["mass"]
        _, _, names = split_anchors(axis, 41)
        made, facts, qs, _ = make_world(axis, names, 8, 60, MIN_GAP["mass"])
        direct = direct_questions(facts)
        self.assertEqual(set(direct), {q for q in qs if q.family == "stated"})
        self.assertEqual(Counter(q.yes for q in direct), {True: 40, False: 40})
        coords = axis.anchors | oracle_coordinates(made, facts, axis.anchors)
        for q in qs:
            self.assertEqual((coords[q.a] > coords[q.b]) == q.positive, q.yes)

    def test_same_entity_vector_can_write_to_multiple_blocks_and_receive_gradients(self):
        net = Model.__new__(Model)
        net.layers = [torch.nn.Identity() for _ in range(3)]
        state = torch.zeros(1, 2, 3)
        delta = torch.nn.Parameter(torch.ones(3))
        with net.write((0, 2), [(0, 1, delta)]):
            result = net.layers[2](net.layers[1](net.layers[0](state)))
            result.sum().backward()
        torch.testing.assert_close(result[0, 1], torch.full((3,), 2.0))
        torch.testing.assert_close(result[0, 0], torch.zeros(3))
        torch.testing.assert_close(delta.grad, torch.full((3,), 2.0))
        torch.testing.assert_close(net.layers[0](state), state)


if __name__ == "__main__":
    unittest.main()
