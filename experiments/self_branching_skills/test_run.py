import numpy as np

from run import Writer, decide, make_stream, maxmin_action, simulate


def test_gate_requires_separation_and_keeps_uncertainty_hysteresis():
    assert not decide([-20, 20], [20, 20], False)
    assert decide([-190, 190], [256, 256], False)
    assert not decide([80, 80], [256, 256], True)
    assert not decide([-80, 80], [256, 256], False)
    assert decide([-80, 80], [256, 256], True)


def test_maxmin_action_minimizes_worst_uncentered_estimated_loss():
    means = np.array([-0.7, 0.5])
    second = np.array([0.65, 0.41])
    action = maxmin_action(means, second)
    grid = np.linspace(-1, 1, 2001)
    np.testing.assert_allclose(action, -0.1)
    assert np.max(action**2 - 2 * action * means + second) <= 1e-12 + np.min(
        np.max(grid[:, None]**2 - 2 * grid[:, None] * means + second, axis=1))


def test_first_decision_is_made_without_its_feedback():
    stream = make_stream(1, "routable")
    changed = (*stream[:-1], -stream[-1])
    for method in ("average", "maxmin", "fixed_two", "adaptive", "oracle"):
        before, slots = simulate(stream, method)
        after, other_slots = simulate(changed, method)
        assert before[0] == after[0]
        assert slots[0] == other_slots[0]
        assert np.any(before[1:] != after[1:])


def test_routing_is_equivalent_to_a_shared_affine_skill_for_binary_cues():
    writer = Writer("fixed_two")
    for cue, signal in [(0, 0.6), (0, 0.9), (1, -0.6), (1, -0.4)]:
        writer.observe(cue, signal)
    a, b = writer.skill
    assert a != b
    for cue in (0, 1):
        np.testing.assert_allclose(writer.predict(cue), a + (b - a) * cue)


def test_routable_stream_splits_rejoins_and_splits_again():
    _, slots = simulate(make_stream(1000, "routable"), "adaptive")
    assert slots[[599, 2199, 3399, 4999]].tolist() == [1, 2, 1, 2]
    for condition in ("hidden", "single_hill"):
        _, slots = simulate(make_stream(1000, condition), "adaptive")
        assert np.all(slots == 1)
