import argparse

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from rebase import SECTIONS, accuracy, center, features, ridge, views


def route(x, router, cutoff):
    probabilities = router.predict_proba(x.reshape(-1, x.shape[-1]))
    selected = np.where(probabilities.max(axis=-1) >= cutoff, probabilities.argmax(axis=-1), 0)
    return selected.reshape(x.shape[:-1])


def apply(h, head, patches, selected):
    return h @ head + np.einsum("...i,...ij->...j", h, patches[selected])


def quantize(scores):
    scale = np.max(np.abs(scores), axis=(-2, -1), keepdims=True) / 127
    scale = np.where(scale > 0, scale, 1).astype(np.float32)
    return np.rint(scores / scale).clip(-127, 127).astype(np.int8), scale


def run(seed, images, target):
    rng = np.random.default_rng(seed)
    indices = rng.permutation(len(target))
    images, y = images[indices], target[indices]
    x = views(images)
    train_end, fit_end, audit_end = SECTIONS
    train, fit = slice(None, train_end), slice(train_end, fit_end)
    check, test = slice(fit_end, audit_end), slice(audit_end, None)
    labels = 5 * center(np.eye(10)[y])

    def base(random_state, inputs):
        return MLPClassifier(
            hidden_layer_sizes=(48,), max_iter=300, tol=0.0005,
            n_iter_no_change=12, early_stopping=True, random_state=random_state,
        ).fit(inputs, y[train])

    old = base(seed, x[0, train])
    new = base(seed + 1, np.clip(x[0, train] + rng.normal(0, 0.08, x[0, train].shape), 0, 1))
    h, w = features(old, x, "source", rng)
    old_patches = np.stack(
        [np.zeros_like(w)]
        + [ridge(h[d, train], labels[train] - h[d, train] @ w) for d in (1, 2)]
    )
    old_scores = h @ (w + old_patches)
    fit_targets = old_scores[:, fit].copy()
    quantized, scales = quantize(fit_targets[1:])
    check_targets = old_scores[:, check].argmax(axis=-1)

    router = LogisticRegression(max_iter=200).fit(
        x[:, fit].reshape(-1, x.shape[-1]), np.repeat([0, 1, 2], fit_end - train_end)
    )
    selected = route(x, router, 0.9)
    upside_down = np.rot90(images[test], k=2, axes=(1, 2)).reshape(len(y[test]), -1)
    mixed = 1 - x[1, test]
    ood_coverage = [(route(ood, router, 0.9) != 0).mean() for ood in (upside_down, mixed)]
    initial = accuracy(apply(h[:, test], w, old_patches, selected[:, test]), y[test])
    rows = []
    for version, model in (("gauge", old), ("independent", new), ("bottleneck", new)):
        h, w = features(model, x, version, rng)
        base_pred = (h @ w).argmax(axis=-1)
        for mode in ("base", "copy", "replay", "capsule", "refit"):
            patches = np.zeros_like(old_patches)
            if mode == "copy":
                patches = old_patches
            elif mode in ("replay", "capsule", "refit"):
                for d in (1, 2):
                    inputs = h[d, train] if mode == "refit" else h[d, fit]
                    if mode == "capsule":
                        desired = quantized[d - 1].astype(np.float32) * scales[d - 1]
                    else:
                        desired = labels[train] if mode == "refit" else fit_targets[d]
                    patches[d] = ridge(inputs, desired - inputs @ w)
            scores = apply(h, w, patches, selected)
            pred = scores.argmax(axis=-1)
            test_acc = accuracy(scores[:, test], y[test])
            audit_ok = (pred[0, check] == base_pred[0, check]).mean() >= 0.95 and np.all(
                (pred[1:, check] == check_targets[1:]).mean(axis=1) >= 0.80
            )
            harmful = (test_acc[0] < (base_pred[0, test] == y[test]).mean() - 0.02
                       or np.any(test_acc[1:] < initial[1:] - 0.05))
            disabled = patches.copy()
            disabled[1] = 0
            off = apply(h[:, test], w, disabled, selected[:, test])
            np.testing.assert_array_equal(off[selected[:, test] != 1], scores[:, test][selected[:, test] != 1])
            change = (off[2].argmax(axis=-1) != pred[2, test]).mean()
            rows.append((version, mode, *test_acc, change, harmful, audit_ok))
    coverage = (selected[:, test] == np.arange(3)[:, None]).mean(axis=1)
    return initial, coverage, ood_coverage, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(10)))
    args = parser.parse_args()
    digits = load_digits()
    runs = [run(s, digits.images / 16, digits.target) for s in args.seeds]
    print(f"seeds: {args.seeds}")
    print("source routed accuracy (%):", np.round(100 * np.mean([r[0] for r in runs], axis=0), 1))
    print("known-domain routing correct (%):", np.round(100 * np.mean([r[1] for r in runs], axis=0), 1))
    print("unregistered 180° rotation / rotated negative routed to a patch (%):",
          np.round(100 * np.mean([r[2] for r in runs], axis=0), 1))
    print("release      mode       clean    rot    neg  dropA→neg-change  harmful  admit  bad admits")
    for group in zip(*(r[3] for r in runs)):
        version, mode = group[0][:2]
        a = np.array([r[2:] for r in group])
        clean, rot, neg, changed = 100 * a[:, :4].mean(axis=0)
        bad, admitted = a[:, 4:].astype(bool).T
        print(f"{version:12} {mode:9} {clean:6.1f} {rot:6.1f} {neg:6.1f} "
              f"{changed:17.1f} {bad.sum():8} {admitted.sum():6} {(bad & admitted).sum():11}")


if __name__ == "__main__":
    main()
