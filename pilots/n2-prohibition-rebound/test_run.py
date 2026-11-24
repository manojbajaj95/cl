import unittest

from run import PROBES, QUEUES, memories, proposals, score, uniforms, verdict


class PilotTests(unittest.TestCase):
    def test_waves_append_ten_rules_and_preserve_wave_one(self):
        self.assertEqual(len(set(QUEUES)), 60)
        self.assertEqual(len(set(PROBES)), 20)
        for wave in range(1, 7):
            for previous, current in zip(memories(wave - 1), memories(wave)):
                self.assertEqual(len(current.splitlines()), wave * 10)
                self.assertTrue(current.startswith(previous))

    def test_mask_excludes_either_tool(self):
        self.assertEqual(proposals(.99, .001, .5, mask="A"), ("B", "B"))
        self.assertEqual(proposals(.01, .999, .5, mask="B"), ("A", "A"))

    def test_verifier_retries_and_can_abstain(self):
        self.assertEqual(score((.9, .1, .9), "A", .5, .95),
                         (True, False, False, False, True, False))
        self.assertEqual(score((.9, .1, .9), "A", .5, .85),
                         (True, False, False, False, True, True))

    def test_sampling_is_paired_and_seeded(self):
        self.assertEqual(uniforms("amber", 4, 17), uniforms("amber", 4, 17))
        self.assertNotEqual(uniforms("amber", 4, 17), uniforms("amber", 4, 29))
        self.assertNotEqual(*uniforms("amber", 4, 17))

    def test_each_kill_gate_is_sufficient(self):
        self.assertEqual(verdict((4.99, 2, 8), (2, 1, 3)), "KILL")
        self.assertEqual(verdict((5, 2, 8), (1, 0, 2)), "KILL")
        self.assertEqual(verdict((5, 2, 8), (2, 1, 3)), "KEEP")


if __name__ == "__main__":
    unittest.main()
