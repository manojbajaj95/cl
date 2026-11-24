import argparse
from dataclasses import dataclass

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from rebase import accuracy, center, features, ridge, views
from routed import apply, quantize, route


AUDIT = 48
COVERAGE = 0.65
METHODS = ("random-int8", "plain-fp32", "diversity", "contrast", "hybrid", "balanced", "label-refit")


@dataclass(frozen=True)
class Capsule:
    indexes: np.ndarray
    payload: np.ndarray
    scale: np.ndarray
    audit_indexes: np.ndarray
    audit_labels: np.ndarray

    @property
    def nbytes(self):
        return sum(x.nbytes for x in vars(self).values())


def unit_rows(x):
    return x / np.maximum(np.linalg.norm(x, axis=1, keepdims=True), 1e-12)


def diverse(z, score, count):
    # Greedy coverage of distinct witness directions, with a quality prior.
    z = unit_rows(z)
    distance = np.ones(len(z))
    priority = np.ones(len(z))
    if score is not None:
        priority[np.argsort(score, kind="stable")] = np.linspace(0, 1, len(score))
    kept = []
    for _ in range(count):
        gain = distance * (0.25 + priority)
        gain[kept] = -np.inf
        i = gain.argmax()
        kept.append(i)
        distance = np.minimum(distance, np.clip(1 - z @ z[i], 0, None))
    return np.array(kept)


def acquire(mode, x, h, w, patches, pool, audit_pool, fit_count, rng):
    bare = h @ w
    teacher = h @ (w + patches)
    sibling = h @ (w + patches[[0, 2, 1]])
    capsules = []
    for task in (1, 2):
        n = (fit_count * 12 + 4) // 42 if mode == "plain-fp32" else fit_count
        target = teacher[task, pool]
        win = target.argmax(axis=1)
        target_margin = np.sort(target, axis=1)[:, -1] - np.sort(target, axis=1)[:, -2]
        other = np.maximum(bare[task, pool], sibling[task, pool])
        rows = np.arange(len(pool))
        wrong = other.copy()
        wrong[rows, win] = -np.inf
        contrast = np.maximum(wrong.max(axis=1) - other[rows, win], 0) * np.maximum(target_margin, 0)
        z = np.concatenate((unit_rows(h[task, pool]), unit_rows(x[task, pool])), axis=1)
        if mode in ("random-int8", "plain-fp32"):
            picked = rng.permutation(len(pool))[:n]
        elif mode == "contrast":
            picked = np.argsort(contrast, kind="stable")[-n:]
        elif mode == "diversity":
            order = rng.permutation(len(z))
            picked = order[diverse(z[order], None, n)]
        elif mode == "balanced":
            groups = [np.flatnonzero(win == label) for label in np.unique(win)]
            queues = [idx[diverse(z[idx], contrast[idx], len(idx))] for idx in groups]
            picked = np.array([q[i] for i in range(max(map(len, queues))) for q in queues if i < len(q)])[:n]
        else:
            picked = diverse(z, contrast, n)
        ids = pool[picked].astype(np.uint16)
        audit_ids = audit_pool[:AUDIT].astype(np.uint16)
        if mode == "plain-fp32":
            payload, scale = target[picked].astype(np.float32), np.empty(0, dtype=np.float32)
        else:
            payload, scale = quantize(target[picked])
        score_ids = teacher[task, audit_ids].argmax(axis=1).astype(np.uint8)
        capsules.append(Capsule(ids, payload, scale, audit_ids, score_ids))
    return capsules


def install(capsules, h, w):
    patches = np.zeros((3, *w.shape))
    for task, capsule in enumerate(capsules, 1):
        x = h[task, capsule.indexes]
        desired = capsule.payload.astype(np.float32)
        if capsule.scale.size:
            desired *= capsule.scale
        patches[task] = ridge(x, desired - x @ w)
    return patches


def chain(seed, images, y, held_out, fit_count):
    rng = np.random.default_rng(seed)
    indices = rng.permutation(len(y))
    x, y = views(images[indices]), y[indices]
    private, pool = slice(None, 480), np.arange(480, 640)
    audit_pool, test = np.arange(640, 712), slice(712, None)
    assert len(y[test]) > 0
    clean_samples = x[0, private]
    labels = 5 * center(np.eye(10)[y[private]])
    model = MLPClassifier(hidden_layer_sizes=(48,), max_iter=200, early_stopping=True, random_state=seed)
    model.fit(clean_samples, y[private])
    h, w = features(model, x, "source", rng)
    patches = np.stack([np.zeros_like(w)] + [
        ridge(h[d, private], labels - h[d, private] @ w) for d in (1, 2)
    ])
    router = LogisticRegression(max_iter=200).fit(
        x[:, pool[:48]].reshape(-1, x.shape[-1]), np.repeat([0, 1, 2], 48)
    )
    selected = route(x, router, 0.85)
    source = accuracy(apply(h[:, test], w, patches, selected[:, test]), y[test])
    assets = {mode: acquire(mode, x, h, w, patches, pool, audit_pool, fit_count, np.random.default_rng(seed))
              for mode in METHODS if mode != "label-refit"}
    budget = sum(c.nbytes for c in assets["random-int8"])
    for mode, capsules in assets.items():
        size = sum(c.nbytes for c in capsules)
        assert 0 <= budget - size < (84 if mode == "plain-fp32" else 1), (mode, budget, size)
    del h, w, patches, labels
    model = MLPClassifier(hidden_layer_sizes=(48,), random_state=seed + 1000)
    stages = (
        ((0.06, 120, 48), (0.14, 12, 35), (0.22, 12, 12), (0.12, 12, 48)),
        ((0.08, 120, 48), (0.18, 12, 48), (0.26, 12, 19), (0.12, 12, 40)),
    )[held_out]
    rows = {mode: [] for mode in METHODS}
    for noise, epochs, live in stages:
        # Train the next release from the prior release, but never from the installed specialist.
        release_samples = np.clip(clean_samples + rng.normal(0, noise, clean_samples.shape), 0, 1)
        for _ in range(epochs):
            model.partial_fit(release_samples, y[private], classes=np.arange(10))
        h, w = features(model, x, "source", rng)
        h[..., rng.permutation(48)[live:]] = 0
        bare_pred = (h @ w).argmax(axis=-1)
        base_clean = (bare_pred[0, test] == y[test]).mean()
        for mode in METHODS:
            capsules = assets.get(mode, assets["random-int8"])
            if mode == "label-refit":
                desired = 5 * center(np.eye(10)[y[private]])
                installed = np.stack([np.zeros_like(w)] + [
                    ridge(h[d, private], desired - h[d, private] @ w) for d in (1, 2)
                ])
            else:
                installed = install(capsules, h, w)
            logits = apply(h, w, installed, selected)
            pred = logits.argmax(axis=-1)
            scores = accuracy(logits[:, test], y[test])
            audit_agree = [
                (pred[d, c.audit_indexes] == c.audit_labels).mean()
                for d, c in enumerate(capsules, 1)
            ]
            ids = capsules[0].audit_indexes
            audit_agree.append((pred[0, ids] == bare_pred[0, ids]).mean())
            # Mean audit agreement breaks ties in worst-case agreement without digit labels.
            confidence = min(audit_agree) + 0.001 * np.mean(audit_agree)
            harm = scores[0] < base_clean - 0.02 or np.any(scores[1:] < source[1:] - 0.05)
            rows[mode].append((confidence, harm, scores[0], scores[1:].mean(), min(scores[1:] - source[1:])))
    return rows


def outcomes(rows, threshold=None):
    flat = rows.reshape(-1, rows.shape[-1])
    if threshold is None:
        count = round(len(flat) * COVERAGE)
        # Fixed-coverage evaluation is a risk ranking, not a causal release policy.
        included = np.argsort(-flat[:, 0], kind="stable")[:count]
        accepted = flat[included]
    else:
        accepted = flat[flat[:, 0] >= threshold]
    risk = accepted[:, 1].mean() if len(accepted) else np.nan
    return np.array([len(accepted) / len(flat), risk, flat[:, 2].mean(), flat[:, 3].mean(),
                     flat[:, 4].mean(), flat[:, 1].mean()])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-seeds", type=int, default=20)
    parser.add_argument("--fit", type=int, choices=(48, 120), default=120)
    args = parser.parse_args()
    if args.test_seeds < 10:
        parser.error("--test-seeds must be at least 10")
    digits = load_digits()
    order = np.random.default_rng(701).permutation(len(digits.target))
    validation, test = np.array_split(order, 2)

    def collect(ids, seeds, held_out):
        rows = [chain(seed, digits.images[ids] / 16, digits.target[ids], held_out, args.fit) for seed in seeds]
        return {mode: np.array([row[mode] for row in rows]) for mode in METHODS}

    train = collect(validation, range(10), False)
    unseen = collect(test, range(20, 20 + args.test_seeds), True)
    boot = np.random.default_rng(320).integers(args.test_seeds, size=(4000, args.test_seeds))
    control = np.array([outcomes(unseen["random-int8"][ids])[1] for ids in boot])
    control_score = outcomes(unseen["random-int8"])[1]
    print(f"validation: 10 chains; held-out: {args.test_seeds} chains × 4 releases; disjoint original images")
    print(f"int8 fit/audit rows per skill: {args.fit}/{AUDIT}")
    print("method         bytes  cov  risk [95% CI]       risk diff [paired 95% CI]   frozen cov/risk  clean skill worstΔ allH")
    for mode in METHODS:
        rows = unseen[mode]
        score = outcomes(rows)
        risks = np.array([outcomes(rows[ids])[1] for ids in boot])
        low, high = np.quantile(risks, [0.025, 0.975])
        delta_low, delta_high = np.quantile(risks - control, [0.025, 0.975])
        validation_scores = train[mode][..., 0].ravel()
        threshold = np.sort(validation_scores)[-round(len(validation_scores) * COVERAGE)]
        frozen = outcomes(rows, threshold)
        sizes = {"plain-fp32": 84 * ((args.fit * 12 + 4) // 42) + AUDIT * 6,
                 "label-refit": "oracle"}
        size = sizes.get(mode, args.fit * 24 + 8 + AUDIT * 6)
        print(f"{mode:13} {size:>6} "
              f"{score[0]:4.0%} {score[1]:5.1%} [{low:5.1%}, {high:5.1%}] "
              f"{score[1]-control_score:+6.1%} [{delta_low:+6.1%}, {delta_high:+6.1%}] "
              f"{frozen[0]:6.1%}/{frozen[1]:5.1%} "
              f"{score[2]:5.1%} {score[3]:5.1%} {100 * score[4]:+5.1f} {score[5]:5.1%}")
    print("Paired mean skill accuracy difference vs random int8 (pp):")
    for mode in METHODS[1:]:
        diff = (unseen[mode][..., 3] - unseen["random-int8"][..., 3]).mean(axis=1) * 100
        interval = np.quantile(diff[boot].mean(axis=1), [0.025, 0.975])
        print(f"{mode:13} {diff.mean():+5.2f} [{interval[0]:+5.2f}, {interval[1]:+5.2f}]")


if __name__ == "__main__":
    main()
