"""CPU pilot: do shared hidden-unit addresses make raw parameter edits portable?"""

import json

import numpy as np


N_MODELS = 40
N_TRAIN_MODELS = 28
DIM = 8
WIDTH = 32
SLOPE = 1.3
ANCHOR = 0.04


def teacher_basis(x):
    return np.tanh(SLOPE * x)


def hidden(x, w):
    return np.tanh(x @ w.swapaxes(-1, -2))


def predict(x, w, v):
    return (hidden(x, w) @ v[..., None])[..., 0]


def fit(x, y, w0, v0, anchors, strength):
    w, v = w0.copy(), v0.copy()
    for _ in range(500):
        h = hidden(x, w)
        residual = ((h @ v[..., None])[..., 0] - y) / x.shape[1]
        grad_v = (residual[:, None, :] @ h)[:, 0, :]
        grad_w = ((residual[..., None] * v[:, None, :] * (1 - h**2))
                  .swapaxes(-1, -2) @ x)
        w -= 0.22 * (grad_w + strength * (w - anchors))
        v -= 0.22 * grad_v
    return w, v


def gauge(w, v):
    # Tanh is odd: flip both sides, then sort by decreasing outgoing magnitude.
    order = np.argsort(-np.abs(v), axis=-1, kind="stable")
    signs = np.where(np.take_along_axis(v, order, axis=-1) < 0, -1.0, 1.0)
    return order, signs


def transform(w, v, order, signs):
    return (np.take_along_axis(w, order[..., None], axis=1) * signs[..., None],
            np.take_along_axis(v, order, axis=1) * signs)


def flatten(w, v):
    return np.concatenate((w.reshape(len(w), -1), v), axis=-1)


def ridge_r2(features, target):
    split = N_TRAIN_MODELS
    train = features[:split]
    center = train.mean(axis=0)
    ybar = target[:split].mean(axis=0)
    train = train - center
    scale = max(np.linalg.norm(train) ** 2 / split, 1e-12)
    weights = np.linalg.solve(
        train @ train.T + 0.1 * scale * np.eye(split), target[:split] - ybar)
    inferred = (features[split:] - center) @ train.T @ weights + ybar
    error = np.sum((inferred - target[split:]) ** 2)
    total = np.sum((target[split:] - target[split:].mean(axis=0)) ** 2)
    return 1 - error / total


def mse(prediction, target):
    return float(np.mean((prediction - target) ** 2))


def slope(effect, feature):
    return float(np.mean(np.sum(effect * feature, axis=1) / np.sum(feature**2, axis=1)))


def evaluate(base, plus, plus_second, coeff, general_x, old_x):
    w, v = base
    plus_w, plus_v = plus
    second_w, second_v = plus_second
    train, test = slice(None, N_TRAIN_MODELS), slice(N_TRAIN_MODELS, None)
    edit_w = w[test] + np.mean(plus_w[train] - w[train], axis=0)
    edit_v = v[test] + np.mean(plus_v[train] - v[train], axis=0)
    both_w = edit_w + np.mean(second_w[train] - w[train], axis=0)
    both_v = edit_v + np.mean(second_v[train] - v[train], axis=0)
    base_y = predict(general_x, w[test], v[test])
    edit_y = predict(general_x, edit_w, edit_v)
    both_y = predict(general_x, both_w, both_v)
    oracle_y = predict(general_x, plus_w[test], plus_v[test])
    old_target = teacher_basis(old_x) @ coeff[test, :, None]
    old_base = predict(old_x, w[test], v[test])
    old_edit = predict(old_x, edit_w, edit_v)
    old_both = predict(old_x, both_w, both_v)
    old_oracle = predict(old_x, plus_w[test], plus_v[test])
    general_basis = teacher_basis(general_x)
    general_target = (general_basis @ coeff[test, :, None])[..., 0]
    feature = general_basis[..., 0]
    second_feature = general_basis[..., 1]
    return {
        "read_r2": ridge_r2(flatten(w, v), coeff[:, 2:]),
        "base_general_mse": mse(base_y, general_target),
        "target_coefficient_increment": slope(edit_y - base_y, feature),
        "oracle_coefficient_increment": slope(oracle_y - base_y, feature),
        "new_task_mse_before": mse(base_y, general_target + feature),
        "new_task_mse_after": mse(edit_y, general_target + feature),
        "new_task_mse_oracle": mse(oracle_y, general_target + feature),
        "old_task_mse_before": mse(old_base, old_target[..., 0]),
        "old_task_mse_after": mse(old_edit, old_target[..., 0]),
        "old_task_mse_oracle": mse(old_oracle, old_target[..., 0]),
        "sequential_first_coefficient_increment_vs_base": slope(both_y - base_y, feature),
        "sequential_second_coefficient_increment_vs_base": slope(both_y - base_y, second_feature),
        "sequential_second_coefficient_increment_vs_first": slope(both_y - edit_y, second_feature),
        "sequential_joint_task_mse": mse(both_y, general_target + feature + second_feature),
        "sequential_old_task_mse": mse(old_both, old_target[..., 0]),
    }


def main():
    rng = np.random.default_rng(20261124)
    coeff = np.zeros((N_MODELS, DIM))
    for row in coeff:
        active = rng.choice(np.arange(2, DIM), size=2, replace=False)
        row[active] = rng.choice([-1, 1], size=2) * rng.uniform(0.5, 1.5, size=2)

    train_x = rng.normal(size=(N_MODELS, 384, DIM))
    train_x[:, ::2, 0] = 0
    train_x[:, 1::2, 1] = 0
    train_basis = teacher_basis(train_x)
    train_y = (train_basis @ coeff[..., None])[..., 0]
    plus_y = train_y + train_basis[..., 0]
    w0 = rng.normal(scale=0.35, size=(N_MODELS, WIDTH, DIM))
    v0 = rng.normal(scale=0.15, size=(N_MODELS, WIDTH))
    anchors = SLOPE * np.repeat(np.eye(DIM), WIDTH // DIM, axis=0)
    anchors += rng.normal(scale=0.04, size=anchors.shape)
    anchor_rng = np.random.default_rng(20261125)
    shared = anchor_rng.normal(size=anchors.shape)
    unshared = anchor_rng.normal(size=w0.shape)
    norms = np.linalg.norm(anchors, axis=-1, keepdims=True)
    shared *= norms / np.linalg.norm(shared, axis=-1, keepdims=True)
    unshared *= norms / np.linalg.norm(unshared, axis=-1, keepdims=True)

    general_x = rng.normal(size=(N_MODELS - N_TRAIN_MODELS, 1024, DIM))
    old_x = rng.normal(size=general_x.shape)
    old_x[..., :2] = 0
    raw = fit(train_x, train_y, w0, v0, anchors, 0)
    raw_plus = fit(train_x, plus_y, w0, v0, anchors, 0)
    second_y = train_y + train_basis[..., 1]
    raw_second = fit(train_x, second_y, w0, v0, anchors, 0)
    order, signs = gauge(*raw)
    canonical = transform(*raw, order, signs)
    # Use each base model's single chart for both endpoints of its training edit.
    canonical_plus = transform(*raw_plus, order, signs)
    canonical_second = transform(*raw_second, order, signs)

    scramble = np.argsort(rng.random(size=raw[1].shape), axis=1)
    flips = rng.choice([-1, 1], size=raw[1].shape)
    scrambled = transform(*raw, scramble, flips)
    assert np.array_equal(flatten(*canonical),
                          flatten(*transform(*scrambled, *gauge(*scrambled))))
    output_drift = np.max(np.abs(
        predict(general_x, *(a[N_TRAIN_MODELS:] for a in raw)) -
        predict(general_x, *(a[N_TRAIN_MODELS:] for a in canonical))))
    assert output_drift < 1e-12

    metrics = {
        "raw": evaluate(raw, raw_plus, raw_second, coeff, general_x, old_x),
        "canonical": evaluate(canonical, canonical_plus, canonical_second, coeff, general_x, old_x),
    }
    for name, frame in (("anchored", anchors), ("shared_random", shared),
                        ("unshared_random", unshared)):
        base, plus, second = (
            fit(train_x, y, w0, v0, frame, ANCHOR) for y in (train_y, plus_y, second_y))
        metrics[name] = evaluate(base, plus, second, coeff, general_x, old_x)
    for values in metrics.values():
        assert all(np.isfinite(list(values.values())))
    result = {
        "models": N_MODELS,
        "train_models": N_TRAIN_MODELS,
        "test_models": N_MODELS - N_TRAIN_MODELS,
        "canonical_prediction_max_abs_drift": float(output_drift),
        "anchored_minus_raw_general_mse": (metrics["anchored"]["base_general_mse"]
                                            - metrics["raw"]["base_general_mse"]),
        "arms": metrics,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
