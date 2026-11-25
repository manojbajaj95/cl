import argparse
from dataclasses import dataclass

import numpy as np
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier


DOMAINS = ("clean", "rotated", "negative")
ALPHA = 0.02
SECTIONS = (1000, 1064, 1160)


@dataclass(frozen=True)
class Capsule:
    delta: np.ndarray
    fit_effect: np.ndarray
    audit_teacher: np.ndarray


def views(images):
    return np.stack(
        (images, np.rot90(images, axes=(1, 2)), 1 - images)
    ).reshape(len(DOMAINS), len(images), -1)


def center(logits):
    return logits - logits.mean(axis=-1, keepdims=True)


def features(model, x, version, rng):
    h = np.maximum(x @ model.coefs_[0] + model.intercepts_[0], 0)
    head = model.coefs_[1]
    if version == "gauge":
        order = rng.permutation(h.shape[-1])
        scales = np.exp(rng.uniform(-2, 2, size=len(order)))
        h, head = h[..., order] * scales, head[order] / scales[:, None]
    if version == "bottleneck":
        h = h.copy()
        h[..., 4:] = 0
    bias = np.ones((*h.shape[:-1], 1))
    return np.concatenate((h, bias), axis=-1), center(np.vstack((head, model.intercepts_[1])))


def ridge(h, y):
    h = h.reshape(-1, h.shape[-1])
    y = y.reshape(-1, y.shape[-1])
    scale = np.sqrt(np.mean(h * h, axis=0))
    scale[scale == 0] = 1
    z = h / scale
    return np.linalg.solve(z.T @ z + len(z) * ALPHA * np.eye(z.shape[1]), z.T @ y) / scale[:, None]


def program(mode, h_fit, source_fit, capsules):
    patches = []
    for domain, capsule in enumerate(capsules, start=1):
        if mode == "copy":
            patch = capsule.delta
        elif mode == "bridge":
            patch = ridge(h_fit, source_fit) @ capsule.delta
        elif mode == "positive":
            patch = ridge(h_fit[domain], capsule.fit_effect)
        elif mode == "contract":
            desired = np.zeros((*h_fit.shape[:-1], capsule.fit_effect.shape[-1]))
            desired[domain] = capsule.fit_effect
            patch = ridge(h_fit, desired)
        else:
            raise ValueError(mode)
        patches.append(patch)
    return np.stack(patches)


def logits(h, base_head, patches):
    return h @ (base_head + patches.sum(axis=0))


def agreement(a, b):
    return (a == b).mean()


def audit(h, head, patches, capsules, source_quality):
    pred = logits(h, head, patches).argmax(axis=-1)
    clean = agreement(pred[0], (h[0] @ head).argmax(axis=-1))
    for domain, capsule in enumerate(capsules, start=1):
        quality = agreement(pred[domain], capsule.audit_teacher)
        sibling_off = logits(h[domain], head, patches[domain - 1 : domain]).argmax(axis=-1)
        if quality < source_quality[domain - 1] - 0.08:
            return False
        if agreement(pred[domain], sibling_off) < 0.90:
            return False
    return clean >= 0.95


def accuracy(scores, labels):
    return (scores.argmax(axis=-1) == labels).mean(axis=-1)


def run(seed, images, target):
    rng = np.random.default_rng(seed)
    indices = rng.permutation(len(target))
    x, y = views(images[indices]), target[indices]
    train_end, fit_end, audit_end = SECTIONS
    train, fit = slice(None, train_end), slice(train_end, fit_end)
    check, test = slice(fit_end, audit_end), slice(audit_end, None)
    label_logits = 5 * center(np.eye(10)[y])

    def train_base(strong):
        model = MLPClassifier(
            hidden_layer_sizes=(48,), max_iter=300, tol=0.0005,
            n_iter_no_change=12, early_stopping=True, random_state=seed + int(strong),
        )
        x_train = x[0, train]
        if strong:
            x_train = np.clip(x_train + rng.normal(0, 0.08, x_train.shape), 0, 1)
        return model.fit(x_train, y[train])

    source = train_base(False)
    replacement = train_base(True)
    old_h, old_head = features(source, x, "source", rng)
    capsules = []
    for domain in range(1, len(DOMAINS)):
        h = old_h[domain]
        delta = ridge(h[train], label_logits[train] - h[train] @ old_head)
        capsules.append(Capsule(delta, h[fit] @ delta, (h[check] @ (old_head + delta)).argmax(axis=-1)))

    old_fit = old_h[:, fit]
    first = program("contract", old_fit, None, capsules[:1])
    installed = program("contract", old_fit, None, capsules)
    before = accuracy(logits(old_h[:, test], old_head, first), y[test])
    source_scores = logits(old_h, old_head, installed)
    source_test = accuracy(source_scores[:, test], y[test])
    source_audit = [
        agreement(source_scores[d, check].argmax(axis=-1), c.audit_teacher)
        for d, c in enumerate(capsules, 1)
    ]
    rows = []
    for version, model in (("gauge", source), ("independent", replacement), ("bottleneck", replacement)):
        h, head = features(model, x, version, rng)
        base = accuracy(h[:, test] @ head, y[test])
        for mode in ("base", "copy", "bridge", "positive", "contract", "refit"):
            admitted = False
            if mode == "base":
                patches = np.zeros((len(capsules), *head.shape))
            elif mode == "refit":
                privileged = []
                for domain in range(1, len(DOMAINS)):
                    desired = np.zeros((len(DOMAINS), train_end, 10))
                    desired[domain] = label_logits[train] - h[domain, train] @ head
                    privileged.append(ridge(h[:, train], desired))
                patches = np.stack(privileged)
            else:
                patches = program(mode, h[:, fit], old_fit, capsules)
                admitted = audit(h[:, check], head, patches, capsules, source_audit)
            score = accuracy(logits(h[:, test], head, patches), y[test])
            without_first = accuracy(logits(h[:, test], head, patches[1:]), y[test])
            swap = without_first[2] - score[2]
            harmful = score[0] < base[0] - 0.02 or np.any(score[1:] < source_test[1:] - 0.05)
            rows.append((version, mode, *score, score[0] - base[0], swap, harmful, admitted))

        if version == "gauge":
            np.testing.assert_allclose(h @ head, old_h @ old_head, atol=1e-10)
            patch = program("contract", h[:, fit], None, capsules)
            np.testing.assert_allclose(logits(h, head, patch), source_scores, atol=1e-9)
            np.testing.assert_allclose(
                logits(h, head, patch) - h @ patch[0], logits(h, head, patch[1:]), atol=1e-9
            )
    return before, source_test, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(10)))
    args = parser.parse_args()
    digits = load_digits()
    runs = [run(s, digits.images / 16, digits.target) for s in args.seeds]
    print(f"seeds: {args.seeds}; migration fit/audit/test examples per domain: 64/96/637")
    print("source after A: " + np.array2string(100 * np.mean([r[0] for r in runs], axis=0), precision=1))
    print("source after B: " + np.array2string(100 * np.mean([r[1] for r in runs], axis=0), precision=1))
    print("release      mode       clean    rot    neg  cleanΔ  dropA→neg  harmful  admit  bad admits")
    for row_group in zip(*(r[2] for r in runs)):
        version, mode = row_group[0][:2]
        values = np.array([r[2:] for r in row_group])
        clean, rot, neg, clean_delta, swap = 100 * values[:, :5].mean(axis=0)
        bad, admitted = values[:, 5:].astype(bool).T
        counts = f"{admitted.sum():>6}  {(bad & admitted).sum():>10}" if mode not in ("base", "refit") else "     -           -"
        print(f"{version:12} {mode:9} {clean:6.1f} {rot:6.1f} {neg:6.1f} {clean_delta:+7.1f} {swap:+10.1f} {bad.sum():8} {counts}")


if __name__ == "__main__":
    main()
