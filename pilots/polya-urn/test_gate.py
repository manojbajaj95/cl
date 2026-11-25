import subprocess
from pathlib import Path
import tempfile
import unittest

import numpy as np

import gate


class ComparatorGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo = Path(__file__).resolve().parents[2]
        source = subprocess.check_output(
            ["git", "show", f"{gate.UPSTREAM}:{gate.SOURCE}"], cwd=repo
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "experiment.py"
            path.write_bytes(source)
            cls.sim = gate.load_simulator(path)
        cls.sim.LONG = gate.HORIZONS[-1]

    def test_balanced_prefixes_share_episode_ids(self):
        orders = [self.sim.order_ids(order) for order in self.sim.ORDERS]
        for horizon in gate.HORIZONS:
            prefixes = [np.sort(ids[:horizon]) for ids in orders]
            counts = np.bincount(prefixes[0] // (self.sim.LONG // 4))
            np.testing.assert_array_equal(counts, [horizon // 4] * 4)
            self.assertEqual(len(np.unique(prefixes[0])), horizon)
            for prefix in prefixes[1:]:
                np.testing.assert_array_equal(prefix, prefixes[0])

    def test_checkpoints_equal_upstream_rollouts(self):
        data = self.sim.world(gate.SEEDS[0])
        order = self.sim.ORDERS[0]
        for design in self.sim.DESIGNS:
            actual = gate.checkpoints(self.sim, design, data, order)
            for horizon in (100, 1000):
                with self.subTest(design=design, horizon=horizon):
                    expected = self.sim.rollout(design, data, order, horizon)
                    np.testing.assert_array_equal(actual[horizon], expected)

    def test_gate_uses_paired_degradation(self):
        n = len(self.sim.DESIGNS)
        values = np.broadcast_to(
            np.arange(n)[:, None, None], (n, 3, len(gate.FIELDS))
        ).copy()
        stable = gate.summarize(self.sim, values)
        self.assertEqual(stable["verdict"], "KILL")
        self.assertEqual(stable["same_panel_max_rho_gain"], 0)
        values[:, :, gate.FIELDS.index("target_1000")] = values[::-1, :, 2]
        degraded = gate.summarize(self.sim, values)
        self.assertEqual(degraded["verdict"], "PROCEED")
        self.assertEqual(
            degraded["ranks"]["fixed_designs"]["degradation_100"]["ci95"], [2, 2]
        )


if __name__ == "__main__":
    unittest.main()
