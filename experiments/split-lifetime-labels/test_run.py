import unittest

from run import ARMS, ROWS, compile_rows, old_tables, refresh, truth


class RefreshTests(unittest.TestCase):
    def test_guard_covers_changed_rows_and_unrestricted_refresh_is_exact(self):
        for move, goal, residue in ((6, 23, 1), (-5, 0, 2)):
            can, masks = old_tables(goal)
            old, guards = compile_rows(can, masks)
            expected = truth(goal, residue, move)
            self.assertNotEqual(old, expected)
            for i, (before, after) in enumerate(zip(old, expected, strict=True)):
                if before != after:
                    self.assertTrue(guards[i] & (1 << residue))
            for arm in ARMS[:-1]:
                out, _ = refresh(can, old, guards, range(len(ROWS)), residue, move, arm, None)
                self.assertEqual(out, expected)

    def test_zero_budget_and_unreleased_boards_preserve_v1(self):
        can, masks = old_tables(23)
        old, guards = compile_rows(can, masks)
        self.assertEqual(old, truth(23, 0, None))
        for arm in ARMS:
            for cap, move in ((0, 6), (96, None)):
                out, work = refresh(can, old, guards, range(len(ROWS)), 0, move, arm, cap)
                self.assertEqual(out, old)
                self.assertEqual(work.total(), 0)


if __name__ == "__main__":
    unittest.main()
