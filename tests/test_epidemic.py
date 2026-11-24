import numpy as np
import pytest

from agents.epidemic.model import Params, Pool, apply_intervention, run
from agents.epidemic.theory import fixed_point, g, integrate


def test_R_formula():
    assert Params(k=4, tau=0.3, alpha_d=0.8, alpha_s=0.8, d=0.1).R == pytest.approx(0.7)


def test_seeded_run_is_deterministic():
    a, b = run(Params(), 300, seed=3), run(Params(), 300, seed=3)
    assert np.array_equal(a["x"], b["x"]) and np.array_equal(a["success"], b["success"])


def test_no_transmission_without_eps_or_tau():
    r = run(Params(eps=0.0, tau=0.5), 300, seed=0)
    assert r["x"].max() == 0.0


def test_provenance_tracking_and_roots():
    pool = Pool()
    a = pool.add(False, [])
    b = pool.add(True, [a])
    c = pool.add(True, [a, b])
    assert pool.children[a] == [b, c] and pool.children[b] == [c]
    assert pool.root[b] and not pool.root[c]


def _chain():
    pool = Pool()
    s = pool.add(False, [])
    r = pool.add(True, [s])
    c1 = pool.add(True, [r])
    c2 = pool.add(True, [c1])
    return pool, s, r, c1, c2


def test_rollback_roots_leaves_descendants():
    pool, s, r, c1, c2 = _chain()
    apply_intervention(pool, "rollback_roots", np.random.default_rng(0))
    assert not pool.alive[r] and pool.alive[c1] and pool.alive[c2] and pool.alive[s]


def test_provenance_closure_removes_descendants_only():
    pool, s, r, c1, c2 = _chain()
    apply_intervention(pool, "provenance_closure", np.random.default_rng(0))
    assert pool.alive[s] and not any(pool.alive[i] for i in (r, c1, c2))


def test_oracle_purge():
    pool, s, *_ = _chain()
    apply_intervention(pool, "oracle_purge", np.random.default_rng(0))
    assert list(pool.alive_ids()) == [s]


@pytest.mark.parametrize("tau,expect_stable", [(0.15, True), (0.4, False)])
def test_threshold_at_R_equals_one(tau, expect_stable):
    p = Params(tau=tau, eps=0.0)
    slope = (g(p, 1e-6) - g(p, 0.0)) / 1e-6
    assert (slope < 0) == expect_stable == (p.R < 1)
    assert slope == pytest.approx(p.alpha_s * (p.R - 1), rel=1e-3)


def test_fixed_point_small_below_threshold_large_above():
    assert fixed_point(Params(tau=0.1)) < 0.1 < 0.5 < fixed_point(Params(tau=0.5))


def test_ode_conditioned_on_observed_state_predicts_run():
    p = Params(tau=0.5)
    errs = []
    for s in range(6):
        r = run(p, 1200, seed=s)
        xo, _ = integrate(p, 1000, n0=r["n"][200], x0=r["x"][200])
        errs.append(abs(xo[-1] - r["x"][-1]))
    assert np.mean(errs) < 0.1
