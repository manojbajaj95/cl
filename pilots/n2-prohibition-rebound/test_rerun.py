import unittest

from rerun import CANDIDATES, PER_QUEUE, TARGETS, THRESHOLD, WAVES, metrics, request, select


class ScreenedRerunTests(unittest.TestCase):
    def test_candidates_are_distinct_for_each_queue(self):
        for queue in TARGETS:
            self.assertEqual(len({request(queue, i) for i in range(len(CANDIDATES))}), len(CANDIDATES))

    def test_screen_requires_every_wave_and_keeps_first_twenty(self):
        queue = TARGETS[0]
        scores = {(wave, queue, probe): THRESHOLD for wave in WAVES for probe in range(PER_QUEUE + 4)}
        scores[4, queue, 0] = THRESHOLD - .01
        del scores[2, queue, 1]
        self.assertEqual(select(scores), [(queue, i) for i in range(2, PER_QUEUE + 2)])

    def test_text_rebound_uses_paired_endpoint_counts(self):
        rows = [[0, 3, .90] * len(WAVES) for _ in range(200)]
        for row in rows[:30]:
            row[-3] = 1
        self.assertEqual(metrics(rows)[-1], 5)
        self.assertEqual(metrics(rows)[1], 100)
        self.assertAlmostEqual(metrics(rows)[2], 90)


if __name__ == "__main__":
    unittest.main()
