"""Matched CPU comparison of where and how to make one rank-one edit."""

import json
from pathlib import Path

import numpy as np


SEEDS = (0, 1, 2, 3, 4)
LAYERS = ("hidden_1", "hidden_2", "hidden_3", "hidden_4", "output")
OPERATORS = ("min_norm", "covariance")
CHOOSERS = ("random", "weight_spectral_norm", "gradient_saliency", "causal_trace", "oracle")


def initialize(rng, widths):
    weights = [rng.normal(size=(a, b)) * np.sqrt(2 / a) for a, b in zip(widths, widths[1:])]
    return weights, [np.zeros(b) for b in widths[1:]]


def forward(weights, biases, x):
    keys, pre = [x], []
    for i, (w, b) in enumerate(zip(weights, biases)):
        z = keys[-1] @ w + b
        pre.append(z)
        if i < len(weights) - 1:
            keys.append(np.maximum(z, 0))
    return keys, pre


def predict(weights, biases, x):
    return forward(weights, biases, x)[1][-1]


def backward(weights, pre, output_grad):
    grads = [output_grad]
    for i in range(len(weights) - 2, -1, -1):
        grads.append((grads[-1] @ weights[i + 1].T) * (pre[i] > 0))
    return grads[::-1]


def train(rng):
    teacher = initialize(rng, [32, 96, 96, 1])
    x = rng.normal(size=(4096, 32))
    y = predict(*teacher, x)
    mean, scale = y.mean(), y.std()
    y = (y - mean) / scale
    weights, biases = initialize(rng, [32, 128, 128, 128, 128, 1])
    parameters = weights + biases
    first = [np.zeros_like(p) for p in parameters]
    second = [np.zeros_like(p) for p in parameters]
    for step in range(1, 801):
        rows = rng.integers(len(x), size=128)
        keys, pre = forward(weights, biases, x[rows])
        grads = backward(weights, pre, (pre[-1] - y[rows]) / len(rows))
        updates = [k.T @ g for k, g in zip(keys, grads)] + [g.sum(0) for g in grads]
        for p, m, v, g in zip(parameters, first, second, updates):
            m *= 0.9
            m += 0.1 * g
            v *= 0.999
            v += 0.001 * g**2
            p -= 0.001 * (m / (1 - 0.9**step)) / (np.sqrt(v / (1 - 0.999**step)) + 1e-8)
    return weights, biases, teacher, mean, scale


def target_values(weights, biases, layer, z, target):
    """Fit one shared preactivation target per layer for both edit operators."""
    fitted = z.copy()
    for _ in range(20):
        if layer == len(weights) - 1:
            out, jac = fitted, np.ones_like(fitted)
        else:
            _, suffix = forward(weights[layer + 1 :], biases[layer + 1 :], np.maximum(fitted, 0))
            out = suffix[-1]
            suffix_grad = backward(weights[layer + 1 :], suffix, np.ones_like(out))[0]
            jac = (suffix_grad @ weights[layer + 1].T) * (fitted > 0)
        # A damped gradient step scaled by the local output Jacobian norm.
        fitted -= 0.5 * (out - target) * jac / (np.sum(jac**2, axis=1, keepdims=True) + 1e-6)
    return fitted


def causal_trace(weights, biases, x, keys, clean, rng):
    """Restore a subset of clean key coordinates in input-corrupted runs."""
    repeats = 64
    noisy = x[:, None, :] + rng.normal(size=(len(x), repeats, x.shape[1]))
    noisy_keys, noisy_pre = forward(weights, biases, noisy)
    baseline_error = ((noisy_pre[-1] - clean[:, None, :]) ** 2).mean(axis=(1, 2))
    scores = []
    for layer, (key, noisy_key) in enumerate(zip(keys, noisy_keys)):
        # Full-state restoration would trivially reset every downstream output in this MLP.
        mask = rng.random(noisy_key.shape)
        restored = np.argpartition(mask, key.shape[-1] // 4 - 1, axis=-1)[..., : key.shape[-1] // 4]
        patched = noisy_key.copy()
        np.put_along_axis(patched, restored, np.take_along_axis(
            np.broadcast_to(key[:, None, :], noisy_key.shape), restored, axis=-1
        ), axis=-1)
        out = predict(weights[layer:], biases[layer:], patched)
        error = ((out - clean[:, None, :]) ** 2).mean(axis=(1, 2))
        scores.append(1 - error / baseline_error)
    return np.stack(scores, axis=1)


def rank(values):
    return np.array([(values < v).sum() + ((values == v).sum() - 1) / 2 for v in values])


def spearman(a, b):
    ar, br = rank(a), rank(b)
    if np.ptp(ar) == 0 or np.ptp(br) == 0:
        return np.nan
    return float(np.corrcoef(ar, br)[0, 1])


def decomposition(scores):
    grand = scores.mean(axis=(1, 2), keepdims=True)
    where = scores.mean(axis=2, keepdims=True) - grand
    how = scores.mean(axis=1, keepdims=True) - grand
    interaction = scores - grand - where - how
    ss = np.array([
        scores.shape[2] * (where**2).sum(),
        scores.shape[1] * (how**2).sum(),
        (interaction**2).sum(),
    ])
    np.testing.assert_allclose(ss.sum(), ((scores - grand) ** 2).sum())
    return ss


def run_seed(seed):
    rng = np.random.default_rng(seed)
    weights, biases, teacher, mean, scale = train(rng)
    calibration = rng.normal(size=(512, 32))
    retention = rng.normal(size=(512, 32))
    x = rng.normal(size=(20, 32))
    neighborhood = x[:, None, :] + 0.1 * rng.normal(size=(20, 32, 32))
    keys, pre = forward(weights, biases, x)
    clean = pre[-1]
    targets = clean + rng.permutation(np.repeat([-2.0, 2.0], len(x) // 2))[:, None]
    old_retention = predict(weights, biases, retention)
    old_neighborhood = predict(weights, biases, neighborhood)
    teacher_retention = (predict(*teacher, retention) - mean) / scale
    teacher_mse = float(((teacher_retention - old_retention) ** 2).mean())

    spectral = np.array([np.linalg.norm(w, 2) for w in weights])
    grads = backward(weights, pre, clean - targets)
    saliency = np.stack([
        np.sum((np.abs(k) @ np.abs(w)) * np.abs(g), axis=1)
        for k, g, w in zip(keys, grads, weights)
    ], axis=1)
    tracing = causal_trace(weights, biases, x, keys, clean, rng)
    choices = np.stack([
        np.full(len(x), spectral.argmax()), saliency.argmax(1), tracing.argmax(1)
    ], axis=1)

    efficacy, damage, transfer = [np.empty((len(x), len(LAYERS), len(OPERATORS))) for _ in range(3)]
    calibration_keys = forward(weights, biases, calibration)[0]
    for layer, (w, key, z, calibration_key) in enumerate(zip(weights, keys, pre, calibration_keys)):
        value_delta = target_values(weights, biases, layer, z, targets) - z
        covariance = calibration_key.T @ calibration_key / len(calibration)
        ridge = 0.01 * np.trace(covariance) / len(covariance)
        adjusted = np.linalg.solve(covariance + ridge * np.eye(len(covariance)), key.T).T
        for operator, direction in enumerate((key, adjusted)):
            direction = direction / (direction * key).sum(1, keepdims=True)
            for i, (k, d, v) in enumerate(zip(key, direction, value_delta)):
                delta = np.outer(d, v)
                np.testing.assert_allclose(k @ delta, v, atol=1e-10)
                edited = weights.copy()
                edited[layer] = w + delta
                out = predict(edited, biases, x[i : i + 1])
                efficacy[i, layer, operator] = 1 - ((out - targets[i]) ** 2).mean() / 4
                new_retention = predict(edited, biases, retention)
                damage[i, layer, operator] = ((new_retention - old_retention) ** 2).mean() / 4
                new_neighbors = predict(edited, biases, neighborhood[i])
                transfer[i, layer, operator] = 1 - ((new_neighbors - targets[i]) ** 2).mean() / (
                    (old_neighborhood[i] - targets[i]) ** 2
                ).mean()
    scores = efficacy - damage
    np.testing.assert_allclose(efficacy[:, :, 0], efficacy[:, :, 1], atol=1e-10)
    assert np.isfinite(scores).all() and np.isfinite(transfer).all()

    oracle = scores.max(axis=1)
    chosen = scores[np.arange(len(x))[:, None], choices]
    chooser_scores = np.concatenate([scores.mean(axis=1)[:, None, :], chosen, oracle[:, None, :]], axis=1)
    trace_rho = np.array([
        [spearman(trace, score[:, o]) for o in range(len(OPERATORS))]
        for trace, score in zip(tracing, scores)
    ])
    if not np.isfinite(trace_rho).all():
        raise ValueError("Constant scores make a within-association rank correlation undefined")

    # ReLU gauge check: a function-preserving rescale can force another norm winner.
    gauge_layer = (int(spectral.argmax()) + 1) % (len(weights) - 1)
    factor = 2 * spectral.max() / spectral[gauge_layer]
    rescaled_weights, rescaled_biases = weights.copy(), biases.copy()
    rescaled_weights[gauge_layer] = weights[gauge_layer] * factor
    rescaled_biases[gauge_layer] = biases[gauge_layer] * factor
    rescaled_weights[gauge_layer + 1] = weights[gauge_layer + 1] / factor
    rescaled_prediction = predict(rescaled_weights, rescaled_biases, np.concatenate([x, retention]))
    gauge_drift = float(np.abs(rescaled_prediction - np.concatenate([clean, old_retention])).max())
    new_winner = np.argmax([np.linalg.norm(w, 2) for w in rescaled_weights])
    assert new_winner == gauge_layer and gauge_drift < 1e-10

    return {
        "sum_squares": decomposition(scores),
        "chooser_regret": (oracle[:, None, :] - chooser_scores).mean(0),
        "trace_spearman": trace_rho.mean(0),
        "neighborhood": transfer.mean(0),
        "efficacy": efficacy.mean(0),
        "retention_damage": damage.mean(0),
        "teacher_mse": teacher_mse,
        "oracle_switch_rate": (scores[:, :, 0].argmax(1) != scores[:, :, 1].argmax(1)).mean(),
        "weight_norm_layer": LAYERS[spectral.argmax()],
        "rescaled_weight_norm_layer": LAYERS[new_winner],
        "gauge_max_prediction_drift": gauge_drift,
    }


def summarize(values, draws, normalize=False):
    def statistic(rows):
        avg = rows.mean(axis=0)
        return avg / avg.sum(axis=-1, keepdims=True) if normalize else avg

    estimate = statistic(values)
    samples = np.stack([statistic(values[draw]) for draw in draws])
    low, high = np.quantile(samples, [0.025, 0.975], axis=0)
    return {"estimate": estimate.tolist(), "ci_low": low.tolist(), "ci_high": high.tolist()}


def main():
    runs = [run_seed(seed) for seed in SEEDS]
    draws = np.random.default_rng(42).integers(len(runs), size=(10000, len(runs)))
    metrics = {
        metric: summarize(np.array([run[metric] for run in runs]), draws, normalize)
        for metric, normalize in (
            ("sum_squares", True), ("chooser_regret", False), ("trace_spearman", False),
            ("neighborhood", False), ("efficacy", False), ("retention_damage", False),
            ("teacher_mse", False), ("oracle_switch_rate", False),
        )
    }
    metrics["variance_share"] = metrics.pop("sum_squares")
    results = {
        "seeds": SEEDS,
        "associations_per_seed": 20,
        "bootstrap_seed_draws": len(draws),
        "axes": {
            "variance_share": ["location", "operator", "location_x_operator"],
            "layers": LAYERS,
            "operators": OPERATORS,
            "choosers": CHOOSERS,
        },
        "metrics": metrics,
        "parameterization_check": [
            {key: run[key] for key in (
                "weight_norm_layer", "rescaled_weight_norm_layer", "gauge_max_prediction_drift"
            )}
            for run in runs
        ],
    }
    Path(__file__).with_name("results.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    for key in ("variance_share", "chooser_regret", "trace_spearman", "oracle_switch_rate"):
        print(f"{key}: {metrics[key]}")
    print(f"Completed {len(runs)} seeds × {results['associations_per_seed']} independent edits")


if __name__ == "__main__":
    main()
