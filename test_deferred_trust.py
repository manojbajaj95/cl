import unittest

import numpy as np

from deferred_trust import (
    I,
    J,
    K,
    PAIR_RANK,
    RADIUS,
    Stream,
    affinity_shadows,
    guarded_decode,
    pair_features,
    run_jet,
    run_shadows,
    sample_stream,
    subspace_decode,
)


class DeferredTrustTests(unittest.TestCase):
    def test_sketch_matches_explicit_projection(self):
        stream = sample_stream("bridged", 11)
        directions = np.random.default_rng(2).normal(size=(17, K))
        dense = run_jet(stream, None, 0.16)
        sketch = run_jet(stream, directions, 0.16)
        for got, want in zip(sketch[:3], dense[:3]):
            np.testing.assert_array_equal(got, want)
        np.testing.assert_allclose(sketch[3], pair_features(directions) @ dense[3], atol=1e-12)

    def test_jet_matches_finite_differences(self):
        stream = sample_stream("dense", 12)
        rng = np.random.default_rng(8)
        v = rng.normal(size=K)
        a = 1e-3
        edit = a * v
        plus, mid, minus = run_shadows(stream, np.stack([edit, edit * 0, -edit]), 0.16)
        w, j, d, h = run_jet(stream, None, 0.16)
        np.testing.assert_allclose(w, mid, atol=1e-12)
        np.testing.assert_allclose(v @ j, (plus - minus) / (2 * a), atol=2e-6)
        curvature = v**2 @ d + 2 * (v[I] * v[J]) @ h
        np.testing.assert_allclose(curvature, (plus + minus - 2 * mid) / a**2, atol=2e-6)

    def test_subspace_needs_more_rows_than_support(self):
        stream = sample_stream("paired", 11)
        directions = np.random.default_rng(8).normal(size=(PAIR_RANK + 1, K))
        h = run_jet(stream, directions, 0.16)[3]
        phi = pair_features(directions)
        chosen, coefs = subspace_decode(phi, h, PAIR_RANK)
        np.testing.assert_array_equal(np.sort(chosen), stream.pairs)
        dense = run_jet(stream, None, 0.16)[3]
        np.testing.assert_allclose(coefs, dense[chosen], atol=1e-12)
        selected, _ = subspace_decode(phi[:-1], h[:-1], PAIR_RANK)
        self.assertEqual(len(selected), 0)

    def test_order_is_not_a_batch_statistic(self):
        stream = sample_stream("paired", 13)
        reversed_stream = Stream(stream.x[::-1], stream.y[::-1], stream.sources[::-1],
                                 stream.eval_x, stream.eval_y, stream.pairs)
        a = run_jet(stream, None, 0.16)[3]
        b = run_jet(reversed_stream, None, 0.16)[3]
        self.assertGreater(np.linalg.norm(a - b), 1e-3)

    def test_affinity_shortcut_is_a_strong_control_on_paired_streams(self):
        stream = sample_stream("paired", 11)
        _, _, _, tracked, active = run_jet(stream, None, 0.16, affinity=True)
        dense = run_jet(stream, None, 0.16)[3]
        np.testing.assert_array_equal(np.sort(active), stream.pairs)
        np.testing.assert_allclose(tracked[:len(active)], dense[active], atol=1e-12)

    def test_affinity_shadows_recover_calibration_even_contrast(self):
        stream = sample_stream("paired", 11)
        pair = stream.pairs[0]
        edits = np.zeros((2, K))
        edits[:, [I[pair], J[pair]]] = [[RADIUS, RADIUS], [-RADIUS, -RADIUS]]
        estimate = affinity_shadows(stream, edits, 0.16)
        exact = run_shadows(stream, edits, 0.16)
        np.testing.assert_allclose(estimate.sum(axis=0), exact.sum(axis=0), atol=1e-12)

    def test_guard_checks_sparse_and_empty_sketches(self):
        stream = sample_stream("paired", 11)
        rng = np.random.default_rng(8)
        phi = pair_features(rng.normal(size=(48, K)))
        h = run_jet(stream, None, 0.16)[3]
        edit_features = pair_features(rng.normal(size=(10, K)))
        correction, mode, ratio = guarded_decode(phi, phi @ h, edit_features)
        self.assertTrue(mode.startswith("music"))
        self.assertLess(ratio, 1e-20)
        np.testing.assert_allclose(correction, edit_features @ h, atol=1e-12)
        empty, mode, _ = guarded_decode(phi, np.zeros_like(phi @ h), edit_features)
        self.assertEqual(mode, "diagonal")
        np.testing.assert_array_equal(empty, 0)


if __name__ == "__main__":
    unittest.main()
