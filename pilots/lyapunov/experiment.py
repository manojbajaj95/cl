"""Fixed CPU experiment; see PROTOCOL.md for estimands and decision rules."""

import argparse
from itertools import combinations
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import rankdata


EARLY = 20
LONG = 200
SEEDS = (101, 202, 303)
ORDERS = ((0, 1, 3, 2), (1, 2, 0, 3), (2, 3, 1, 0), (3, 0, 2, 1))
DESIGNS = (
    "append", "fifo", "utility", "merge", "summary", "reflection", "gated", "high_gain"
)
PERTURBATION = 0.001
FLOOR = 1e-8
BOOTSTRAPS = 10_000
PREDICTORS = (
    "lambda", "direct_20", "growth_rate", "edit_rate", "nondeclaration",
    "declaration_level", "draft_rejection_rate", "final_entries_20",
)
OUTCOMES = ("order_distance", "accuracy_spread")
CAPACITY = 16
WIDTH = 8


def normalize(x):
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)


def distance(left, right):
    return float(np.sqrt(np.mean(np.square(left - right))))


def predict(memory, queries):
    scores = queries @ memory[:, :WIDTH].T
    scores = 6 * scores + np.log(memory[:, WIDTH + 1])
    nearest = np.argsort(-scores, axis=1, kind="stable")[:, :4]
    weights = np.exp(np.take_along_axis(scores, nearest, axis=1))
    return (weights * memory[nearest, WIDTH]).sum(axis=1) / weights.sum(axis=1), nearest


def accuracy(prediction, labels):
    return float(np.mean(np.where(labels, prediction, 1 - prediction)))


def order_ids(order):
    ids = np.arange(LONG).reshape(4, LONG // 4)
    return np.concatenate([ids[list(order), start:start + 5].ravel()
                           for start in range(0, LONG // 4, 5)])


def world(seed):
    data, initial, probe, validation, loop, alternate = [
        np.random.default_rng(child) for child in np.random.SeedSequence(seed).spawn(6)
    ]
    offset = 0.8 * np.eye(WIDTH)[:4]

    def examples(rng, per_task):
        task = np.repeat(np.arange(4), per_task)
        latent = rng.normal(size=(len(task), WIDTH))
        x = normalize(latent + offset[task])
        y = (latent[np.arange(len(task)), 4 + task] +
             0.5 * latent[:, 0] * latent[:, 7]) > 0
        return x, y

    x, y = examples(data, LONG // 4)
    warm_x, warm_y = examples(initial, 2)
    memory = np.column_stack((warm_x, np.where(warm_y, 0.8, 0.2), np.ones(len(warm_y))))
    return (x, y, examples(probe, 32), examples(validation, 32), memory,
            loop.random((LONG, 3)), alternate.random((LONG, 3)))


def transition(design, memory, query, label, draws):
    predicted, nearest = predict(memory, query[None, :])
    action = draws[0] < predicted[0]
    success = (action == label) != (draws[1] < 0.06)
    target = 0.95 if action == success else 0.05
    entry = np.r_[query, target, 1.1 if success else 0.9]
    match = nearest[0, 0]

    if design == "append":
        return np.vstack((memory, entry)), 0
    if design == "fifo":
        return np.vstack((memory[-(CAPACITY - 1):], entry)), int(len(memory) == CAPACITY)

    updated = memory.copy()
    if design == "utility":
        updated[match, WIDTH + 1] = 0.85 * updated[match, WIDTH + 1] + (
            0.24 if success else 0.08
        )
        if len(memory) == CAPACITY:
            evicted = int(np.argmin(updated[:, WIDTH + 1]))
            return np.vstack((np.delete(updated, evicted, axis=0), entry)), 1 + (evicted != match)
        return np.vstack((updated, entry)), 1
    if design == "merge":
        closest = int(np.argmax(memory[:, :WIDTH] @ query))
        if len(memory) < CAPACITY and memory[closest, :WIDTH] @ query < 0.60:
            return np.vstack((memory, entry)), 0
        updated[closest] = 0.8 * memory[closest] + 0.2 * entry
        updated[closest, :WIDTH] = normalize(updated[closest, :WIDTH])
        return updated, 1
    if design == "summary":
        similarity = np.maximum(0, memory[:, :WIDTH] @ query)
        rate = (0.06 + 0.24 * similarity)[:, None]
        updated = (1 - rate) * memory + rate * entry
        updated[:, :WIDTH] = normalize(updated[:, :WIDTH])
        return updated, len(memory)
    if design == "reflection":
        updated[match, WIDTH:] += (0.12 if success else 0.33) * (
            entry[WIDTH:] - updated[match, WIDTH:]
        )
        return updated, 1
    if design == "gated":
        if success and draws[2] > 0.12:
            return memory, 0
        closest = int(np.argmax(memory[:, :WIDTH] @ query))
        if memory[closest, :WIDTH] @ query > 0.68:
            updated[closest] = 0.55 * memory[closest] + 0.45 * entry
            updated[closest, :WIDTH] = normalize(updated[closest, :WIDTH])
            return updated, 1
        if len(memory) == CAPACITY:
            return np.vstack((memory[1:], entry)), 1
        return np.vstack((memory, entry)), 0
    if design == "high_gain":
        updated[match, :WIDTH] = normalize(0.3 * memory[match, :WIDTH] + 0.7 * query)
        payload = target + 1.5 * (target - memory[match, WIDTH])
        updated[match, WIDTH] = np.clip(payload, 0.01, 0.99)
        updated[match, WIDTH + 1] = 1.1 if success else 0.9
        return updated, 1
    raise ValueError(f"Unknown design: {design}")


def rollout(design, data, order, length, *, perturb=False, other_seed=False, trace=False):
    x, y, (probe_x, _), (valid_x, valid_y), memory, original, alternate = data
    draws = alternate if other_seed else original
    if perturb:
        memory = memory.copy()
        memory[0, WIDTH] += PERTURBATION
    predictions, drafts = [], []
    edits = 0
    if trace:
        predictions.append(predict(memory, probe_x)[0])
        last_accuracy = accuracy(predict(memory, valid_x)[0], valid_y)
    for i in order_ids(order)[:length]:
        memory, changed = transition(design, memory, x[i], y[i], draws[i])
        edits += changed
        if trace:
            predictions.append(predict(memory, probe_x)[0])
            candidate = accuracy(predict(memory, valid_x)[0], valid_y)
            drafts.append(candidate - last_accuracy)
            last_accuracy = candidate
    if trace:
        return np.array(predictions), len(memory), edits, np.array(drafts)
    return predict(memory, probe_x)[0]


def slope(curve):
    t = np.arange(len(curve), dtype=float)
    t -= t.mean()
    return float(t @ np.log(np.maximum(curve, FLOOR)) / (t @ t))


def convergence(gains):
    rejected = gains <= 0.002
    level = next((i + 1 for i in range(2, len(gains)) if rejected[i - 2:i + 1].all()),
                 len(gains) + 1)
    return {"nondeclaration": int(level > len(gains)), "declaration_level": level,
            "draft_rejection_rate": float(rejected.mean())}


def measure(design, seed, data):
    reference, entries, edits, gains = rollout(design, data, ORDERS[0], EARLY, trace=True)
    perturbed = rollout(design, data, ORDERS[0], EARLY, perturb=True, trace=True)[0]
    noise = rollout(design, data, ORDERS[0], EARLY, other_seed=True, trace=True)[0]
    early_other = rollout(design, data, ORDERS[1], EARLY)
    perturbed_curve = np.array([distance(a, b) for a, b in zip(reference, perturbed)])
    noise_curve = np.array([distance(a, b) for a, b in zip(reference, noise)])
    final = [rollout(design, data, order, LONG) for order in ORDERS]
    pairs = [distance(a, b) for a, b in combinations(final, 2)]
    scores = [accuracy(p, data[2][1]) for p in final]
    return {
        "design": design, "seed": seed, "lambda": slope(perturbed_curve),
        "direct_20": distance(reference[-1], early_other),
        "growth_rate": (entries - len(data[4])) / EARLY, "edit_rate": edits / EARLY,
        **convergence(gains), "final_entries_20": entries,
        "order_distance": float(np.mean(pairs)), "accuracy_spread": max(scores) - min(scores),
        "initial_accuracy": accuracy(reference[0], data[2][1]),
        "order_pair_distances": pairs, "order_accuracies": scores,
        "perturbed_curve": perturbed_curve.tolist(), "seed_only_curve": noise_curve.tolist(),
        "perturbed_mean": float(perturbed_curve[1:].mean()),
        "seed_only_mean": float(noise_curve[1:].mean()),
    }


def correlation(x, y):
    rx, ry = rankdata(x, axis=-1), rankdata(y, axis=-1)
    rx = rx - rx.mean(axis=-1, keepdims=True)
    ry = ry - ry.mean(axis=-1, keepdims=True)
    denominator = np.sqrt(np.sum(rx ** 2, axis=-1) * np.sum(ry ** 2, axis=-1))
    return np.divide(np.sum(rx * ry, axis=-1), denominator,
                     out=np.full(denominator.shape, np.nan), where=denominator != 0)


def interval(point, bootstrap):
    valid = bootstrap[np.isfinite(bootstrap)]
    return {"estimate": float(point) if np.isfinite(point) else None,
            "ci95": np.percentile(valid, [2.5, 97.5]).tolist() if len(valid) else None,
            "valid_bootstraps": len(valid)}


def summarize(rows):
    keys = PREDICTORS + OUTCOMES + ("perturbed_mean", "seed_only_mean")
    values = np.array([[row[key] for key in keys] for row in rows]).reshape(
        len(DESIGNS), len(SEEDS), len(keys)
    )
    rate_columns = [keys.index(key) for key in ("growth_rate", "edit_rate", "draft_rejection_rate")]
    values[..., rate_columns] = np.rint(EARLY * values[..., rate_columns])
    rng = np.random.default_rng(90612)
    designs = rng.integers(len(DESIGNS), size=(BOOTSTRAPS, len(DESIGNS)))
    seeds = rng.integers(len(SEEDS), size=(BOOTSTRAPS, len(SEEDS)))
    sampled = values[designs[:, :, None], seeds[:, None, :]]
    correlations = {}
    for outcome in OUTCOMES:
        correlations[outcome] = {}
        for label, point, draws in (
            ("design", values.mean(axis=1), sampled.mean(axis=2)),
            ("pooled", values.reshape(-1, len(keys)), sampled.reshape(BOOTSTRAPS, -1, len(keys))),
        ):
            j = keys.index(outcome)
            point_rho = [correlation(point[:, i], point[:, j]) for i in range(len(PREDICTORS))]
            draw_rho = [correlation(draws[:, :, i], draws[:, :, j]) for i in range(len(PREDICTORS))]
            correlations[outcome][label] = {
                "rho": {key: interval(p, b) for key, p, b in zip(PREDICTORS, point_rho, draw_rho)},
                "lambda_margin": {
                    key: interval(point_rho[0] - (point_rho[i] if i == 1 else abs(point_rho[i])),
                                  draw_rho[0] - (draw_rho[i] if i == 1 else abs(draw_rho[i])))
                    for i, key in enumerate(PREDICTORS) if i
                },
            }

    def noise_gap(point, draws):
        return {
            "perturbed_mean": float(point[..., -2].mean()),
            "seed_only_mean": float(point[..., -1].mean()),
            "gap": interval(np.mean(point[..., -2] - point[..., -1]),
                            np.mean(draws[..., -2] - draws[..., -1], axis=-1)),
        }

    separation = {
        "pooled": noise_gap(values, sampled.reshape(BOOTSTRAPS, -1, len(keys))),
        "design": {design: noise_gap(values[i], values[i, seeds]) for i, design in enumerate(DESIGNS)},
    }
    primary = correlations["order_distance"]["design"]
    direct_margin = primary["lambda_margin"]["direct_20"]["estimate"]
    alternatives = [primary["lambda_margin"][key]["estimate"] for key in PREDICTORS[2:]
                    if primary["rho"][key]["estimate"] is not None]
    gap_ci = separation["pooled"]["gap"]["ci95"]
    gates = {
        "beat_direct_by_0.30": direct_margin is not None and direct_margin >= 0.30,
        "beat_growth_edit_convergence": primary["rho"]["lambda"]["estimate"] is not None and
        all(margin is not None and margin > 0 for margin in alternatives),
        "perturbation_above_seed_floor": gap_ci is not None and gap_ci[0] > 0,
    }
    return {"verdict": "KEEP" if all(gates.values()) else "KILL", "gates": gates,
            "correlations": correlations, "separation": separation}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    datasets = {seed: world(seed) for seed in SEEDS}
    rows = [measure(design, seed, datasets[seed]) for design in DESIGNS for seed in SEEDS]
    results = {
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
        "seeds": SEEDS, "orders": ORDERS, "early_updates": EARLY, "long_updates": LONG,
        "bootstraps": BOOTSTRAPS, "rows": rows, **summarize(rows),
    }
    args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    for name, passed in results["gates"].items():
        print(f"{name}: {'pass' if passed else 'fail'}")
    print(f"Verdict: {results['verdict']} ({len(rows)} design-seed units)")


if __name__ == "__main__":
    main()
