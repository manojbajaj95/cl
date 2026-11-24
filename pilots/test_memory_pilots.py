import unittest
from unittest.mock import patch

import numpy as np
import torch
from transformers import Qwen2Config, Qwen2ForCausalLM

from pilots.m2_salience import pilot as m2
from pilots.m2_salience import report as m2_report
from pilots.n1_layer_local_kv import pilot as n1
from pilots.temperature import fit_temperature, temper


class TinyTokenizer:
    def encode(self, text, add_special_tokens=False):
        return [ord(c) % 64 for c in text]


class MemoryPilotsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        torch.manual_seed(42)
        config = Qwen2Config(
            vocab_size=64, hidden_size=32, intermediate_size=64, num_attention_heads=4,
            num_key_value_heads=2, num_hidden_layers=n1.BLOCKS, use_sliding_window=False,
            sliding_window=None,
        )
        cls.model = Qwen2ForCausalLM(config)

    def backbone(self, cls):
        with (patch.object(m2.AutoTokenizer, "from_pretrained", return_value=TinyTokenizer()),
              patch.object(m2.AutoModelForCausalLM, "from_pretrained", return_value=self.model)):
            return cls("tiny")

    def test_stream_and_evidence(self):
        episodes = list(m2.episode_queries(101, 120))
        self.assertEqual([episodes[i][0] for i in range(0, 600, 120)], [0, 1, 0, 2, 1])
        self.assertEqual(len(episodes), 600)
        lessons, mapping, index = m2.world(101)
        for station, row in enumerate(mapping):
            for correct in row:
                self.assertIn(f"valve {m2.ACTIONS[correct]}", lessons[index[station, correct]])
        bias = m2.evidence_bias(3)
        self.assertEqual(bias[0, 3], 2)
        self.assertEqual(torch.count_nonzero(bias == -2), 29)

    def test_recency_uses_only_previously_confirmed_lessons(self):
        last = np.full(m2.N, -np.inf)
        last[3], last[4] = 10, 0
        result = m2.recency_bias(last, 20, [10])[0]
        self.assertEqual(result[3], 1.)
        self.assertEqual(result[4], .5)
        self.assertEqual(result[0], 0.)

    def test_zero_bias_matches_uncached_and_lesson_gradient_is_live(self):
        model = self.backbone(m2.Backbone)
        query = (0, 0)
        contexts = m2.Contexts(model, ["abc"] * m2.N)
        bias = torch.zeros(1, m2.N, requires_grad=True)
        scores = contexts.biased(query, bias)
        with torch.no_grad():
            tokens = torch.tensor([contexts.tokens(m2.ALL) + model.suffix[query]])
            hidden = model.lm.model(tokens, use_cache=False).last_hidden_state[:, -1]
            expected = (hidden @ model.head.T).log_softmax(-1)
        torch.testing.assert_close(scores, expected)
        (-scores[0, 0]).backward()
        self.assertTrue(torch.isfinite(bias.grad).all())
        self.assertGreater(float(bias.grad.abs().sum()), 0.)
        self.assertTrue(all(p.grad is None for p in model.lm.parameters()))

    def test_layer_mask_and_retrieval_controls(self):
        model = self.backbone(n1.LayerBackbone)
        name, action, probes = next(n1.lesson_probes(101))
        included = n1.local_bias(n1.FULL)
        off = n1.local_bias([False] * n1.BLOCKS)
        scores = model.evaluate("note", probes[:1], [included, off])
        self.assertFalse(np.allclose(scores[0], scores[1]))
        row = n1.evaluate_lesson(model, name, action, probes, temperature=0.5)
        self.assertTrue(any(row["mask"]))
        self.assertEqual(row["recall"], 1.)
        self.assertEqual(row["harm"][n1.ARMS.index("retrieval")], 0.)
        self.assertEqual(len(list(n1.lesson_probes(101))), 40)

    def test_m2_paired_diffs_and_verdict(self):
        rows = [{"hit": [0, 1, 1], "grad_nonzero": True}] * 100
        raw = {"arms": ["uniform", "m2", "ease"], "visit_length": 20,
               "seeds": [{"episodes": rows} for _ in m2.SEEDS]}
        summary = m2_report.summarize(raw)
        self.assertEqual(summary["verdict"], "KILL")
        self.assertEqual(summary["phases"]["returning"]["m2_minus_best"],
                         {"mean": 0., "ci95": [0., 0.]})

    def test_source_entropy_matching_cannot_change_greedy_choice(self):
        logits = np.array([[0., 1., 2.], [-2., 2., 0.]])
        blank = temper(logits, 1.)
        full = temper(logits, 0.7)
        result = fit_temperature(blank, full)
        self.assertAlmostEqual(result["temperature"], 0.7)
        self.assertAlmostEqual(result["source_tempered_entropy"], result["source_full_entropy"])
        np.testing.assert_array_equal(temper(blank, result["temperature"]).argmax(-1), blank.argmax(-1))

    def test_global_bias_matches_training_gain_between_grid_points(self):
        class Model:
            def evaluate(self, lesson, probes, configurations):
                return np.array([[config[0], 0.] for config in configurations])

        probes = [("on", 0, True), ("off", 1, False)]
        grid = np.array([[b, 0.] for b in n1.BIAS_GRID])
        bias, matched_gain = n1.match_bias(Model(), "note", probes, np.zeros(2), grid, -0.3)
        self.assertAlmostEqual(bias, -0.3)
        self.assertAlmostEqual(matched_gain, -0.3)


if __name__ == "__main__":
    unittest.main()
