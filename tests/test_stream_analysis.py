from agents.llm_pilot.analyze_stream import auc, meanfield, measured


def row(k, j, defective, correct):
    return dict(k=k, j=j, defective=defective, correct=correct, lesson="x")


def test_measured_R_for_pure_copying_without_gate_is_one():
    curve = [row(1, 0, False, True)] * 10 + [row(1, 1, True, False)] * 10
    m = measured(curve, 1, 0.0)
    assert m["tau"] == 1.0 and abs(m["R"] - 1.0) < 1e-9


def test_outcome_gate_lowers_R_by_catch_ratio():
    curve = [row(1, 0, False, True)] * 10 + [row(1, 1, True, False)] * 10
    m = measured(curve, 1, 0.5)
    assert abs(m["alpha_D"] - 0.5) < 1e-9 and abs(m["alpha_S"] - 1.0) < 1e-9 and abs(m["R"] - 0.5) < 1e-9


def test_meanfield_decays_below_threshold_and_holds_when_neutral():
    D_gate, S_gate = [0.0, 0.5], [1.0, 0.0]
    assert meanfield(D_gate, S_gate, 0.25, 8, 200) < 0.1
    assert abs(meanfield([0.0, 1.0], [1.0, 0.0], 0.25, 8, 200) - 0.25) < 1e-9


def test_auc():
    assert auc([1, 2, 3, 4], [0, 0, 1, 1]) == 1.0
    assert auc([1, 1], [0, 1]) == 0.5
