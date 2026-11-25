from unittest import TestCase, main
from unittest.mock import patch

import torch
from torch import nn

from self_quiz_pilot import EVAL_FORMS, FORMS, LENGTH, PREFIX, STYLES, LanguageModel, World, generate_replay
from summarize_self_quiz import paired_interval


class SelfQuizTests(TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)

    def test_old_paraphrases_are_held_out(self):
        world = World(41)
        forms = world.encode([FORMS[name][0] for name in EVAL_FORMS])
        old = world.train_bank(world.old, "old")
        background = world.train_bank(world.bg, "background")
        self.assertTrue(all(not torch.any(old == form) for form in forms))
        self.assertTrue(all(torch.any(background[:, 1] == form) for form in forms))
        self.assertFalse({f[0] for f in world.old} & {f[0] for group in world.new for f in group})

    def test_causal_predictions_cannot_see_future_values(self):
        model = LanguageModel(20).eval()
        x = torch.tensor([[1, 2, 3, 4], [1, 2, 7, 8]])
        with torch.no_grad():
            logits = model(x)
        torch.testing.assert_close(logits[0, :2], logits[1, :2])

    def test_replay_matching_drops_wrong_answers_and_shares_questions(self):
        world = World(41)
        world.old = world.old[:2]

        def fake_draw(model, prompts, count, rng, subset=None):
            if subset is not None:
                return torch.cat([prompts, subset[0].expand(len(prompts), 1)], dim=1)
            results = []
            for row in prompts.tolist():
                first, second = world.old
                fact = first if row[4] == first[1] else second
                family = "q" if row[1] == world.vocab[FORMS["q1"][0]] else "raw"
                value = fact[2] if fact == first else next(v for v in world.values[fact[1]] if v != fact[2])
                self.assertNotIn(fact[2], row)
                results.append(row + world.answer(value, STYLES[family][1]))
            return torch.tensor(results)

        with patch("self_quiz_pilot.draw", fake_draw):
            banks, stats = generate_replay(nn.Identity(), world, 41)
        self.assertEqual(stats["matched_facts"], 1)
        self.assertEqual(stats["different_teacher_answers"], 1)
        self.assertEqual({tuple(bank.shape) for bank in banks.values()}, {(1, LENGTH)})
        self.assertTrue(torch.equal(banks["self_qa"][:, :PREFIX], banks["teacher_qa"][:, :PREFIX]))
        self.assertTrue(torch.equal(banks["self_qa"], banks["diverse_teacher_qa"]))
        self.assertTrue(all(int(bank[0, PREFIX + 3]) == world.old[0][2] for bank in banks.values()))

    def test_paired_interval_uses_seed_differences(self):
        self.assertEqual(paired_interval([2.0, 2.0, 2.0])["95%_ci"], [2.0, 2.0])
        self.assertLess(paired_interval([-1.0, 1.0, 2.0])["95%_ci"][0], 0)


if __name__ == "__main__":
    main()
