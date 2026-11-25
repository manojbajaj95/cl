"""Synthetic interface-change diagnostics; run with python3 and NumPy."""

import numpy as np


SEEDS = (0, 1, 2, 3, 4)


def logsumexp(z):
    peak = z.max(axis=1, keepdims=True)
    return peak + np.log(np.exp(z - peak).sum(axis=1, keepdims=True))


def sigmoid(z):
    return np.exp(-np.logaddexp(0, -z))


def cross_entropy_grad(logits, y):
    grad = np.exp(logits - logsumexp(logits))
    grad[np.arange(len(y)), y] -= 1
    return grad / len(y)


def scores(log_probs, y):
    return -log_probs[np.arange(len(y)), y].mean(), (log_probs.argmax(1) == y).mean()


def vocabulary(rng):
    old_size, new_size, dim = 20, 5, 16
    old_centers = rng.normal(size=(old_size, dim))
    new_centers = rng.normal(size=(new_size, dim))

    def sample(centers, cue, size):
        y = rng.integers(len(centers), size=size)
        x = centers[y] + rng.normal(scale=0.85, size=(size, dim))
        return np.column_stack((x, rng.normal(cue, 0.7, size), np.ones(size))), y

    a, ya = sample(old_centers, -1, 768)
    b, yb = sample(new_centers, 1, 768)
    anchors, _ = sample(old_centers, -1, 256)
    a_test, ya_test = sample(old_centers, -1, 1024)
    b_test, yb_test = sample(new_centers, 1, 1024)
    w_old = np.zeros((a.shape[1], old_size))
    for _ in range(150):
        w_old -= 0.35 * (a.T @ cross_entropy_grad(a @ w_old, ya))

    old_a_test = a_test @ w_old
    old_a_z = logsumexp(old_a_test)
    before = scores(old_a_test - old_a_z, ya_test)
    out = {"Before growth": (*before, 0, np.nan, np.nan, np.nan)}
    init = rng.normal(scale=0.025, size=(a.shape[1], new_size))
    old_b, old_anchors = b @ w_old, anchors @ w_old
    old_b_test = b_test @ w_old
    old_anchor_z = logsumexp(old_anchors)

    def gate_feature(x):
        return sigmoid(-2 * x[:, -2:-1])

    for name, strength in [("Shared softmax", 0), ("Shared + log-Z gate", 10)]:
        w, gate = init.copy(), 0.0
        for _ in range(150):
            b_logits = np.column_stack((old_b, b @ w + gate * gate_feature(b)))
            g_b = cross_entropy_grad(b_logits, yb + old_size)[:, old_size:]
            weight_grad = b.T @ g_b
            gate_grad = (gate_feature(b) * g_b).sum()
            if strength:
                new_anchors = anchors @ w + gate * gate_feature(anchors)
                z = logsumexp(np.column_stack((old_anchors, new_anchors)))
                delta = z - old_anchor_z
                g_a = strength * delta * np.exp(new_anchors - z) / len(anchors)
                weight_grad += anchors.T @ g_a
                gate_grad += (gate_feature(anchors) * g_a).sum()
            w -= 0.35 * weight_grad
            if strength:
                gate -= 0.35 * gate_grad

        joint_a = np.column_stack((old_a_test, a_test @ w + gate * gate_feature(a_test)))
        joint_b = np.column_stack((old_b_test, b_test @ w + gate * gate_feature(b_test)))
        z_a, z_b = logsumexp(joint_a), logsumexp(joint_b)
        a_score = scores(joint_a - z_a, ya_test)
        b_score = scores(joint_b - z_b, yb_test + old_size)
        delta_nll = a_score[0] - before[0]
        partition_tax = (z_a - old_a_z).mean()
        np.testing.assert_allclose(delta_nll, partition_tax, atol=1e-12)
        out[name] = (*a_score, delta_nll, partition_tax / delta_nll, *b_score)

    head = init.copy()
    # Domain supervision for the selector, not old-token labels.
    domains = np.concatenate((anchors[:, -2], b[:, -2]))
    is_new = np.repeat([0, 1], [len(anchors), len(b)])
    selector = np.zeros(2)
    design = np.column_stack((domains, np.ones(len(domains))))
    for _ in range(150):
        head -= 0.35 * (b.T @ cross_entropy_grad(b @ head, yb))
        selector -= 0.35 * (design.T @ (sigmoid(design @ selector) - is_new)) / len(design)

    def two_head(x, old_logits):
        select = x[:, -2:-1] * selector[0] + selector[1]
        new_logits = x @ head
        return np.column_stack((
            old_logits - logsumexp(old_logits) - np.logaddexp(0, select),
            new_logits - logsumexp(new_logits) - np.logaddexp(0, -select),
        ))

    a_score = scores(two_head(a_test, old_a_test), ya_test)
    b_score = scores(two_head(b_test, old_b_test), yb_test + old_size)
    out["Separate softmax + selector"] = (*a_score, a_score[0] - before[0], 0, *b_score)
    return out


def architecture(rng):
    dim, width = 8, 12
    teacher_a = rng.normal(scale=0.65, size=(dim, width))
    teacher_b = rng.normal(scale=0.65, size=(dim, width))
    readout = rng.normal(scale=0.4, size=width)

    def sample(teacher):
        x = rng.normal(size=(512, dim))
        return x, np.tanh(x @ teacher) @ readout

    a, ya = sample(teacher_a)
    b, yb = sample(teacher_b)
    a_test, ya_test = sample(teacher_a)
    b_test, yb_test = sample(teacher_b)
    w = rng.normal(scale=0.35, size=(dim, width))
    v = rng.normal(scale=0.25, size=width)

    def forward(x, w, v):
        return np.tanh(x @ w) @ v

    def step(x, y, w, v, first=0):
        hidden = np.tanh(x @ w)
        err = (hidden @ v - y) / len(y)
        dw = x.T @ ((err[:, None] * v) * (1 - hidden**2))
        dv = hidden.T @ err
        w[:, first:] -= 0.12 * dw[:, first:]
        v[first:] -= 0.12 * dv[first:]

    def rms(x):
        return np.sqrt(np.mean(x**2))

    for _ in range(250):
        step(a, ya, w, v)
    before = forward(a_test, w, v)
    out = {}
    for name, grow, freeze in [
        ("No growth", False, False),
        ("Widen, train all", True, False),
        ("Widen, train new only", True, True),
    ]:
        # Duplicate each activation into two new units with cancelling readouts:
        # the Net2Wider cloning idea, but without rescaling the original readout.
        w_next = np.tile(w, (1, 3)) if grow else w.copy()
        v_next = np.concatenate((v, v / 2, -v / 2)) if grow else v.copy()
        at_insertion = forward(a_test, w_next, v_next)
        np.testing.assert_allclose(at_insertion, before, atol=1e-12, rtol=0)
        np.testing.assert_allclose(forward(b, w_next, v_next), forward(b, w, v), atol=1e-12, rtol=0)
        drift = [rms(at_insertion - before)]
        for t in range(1, 101):
            step(b, yb, w_next, v_next, first=width if freeze else 0)
            if t in (1, 5, 10):
                drift.append(rms(forward(a_test, w_next, v_next) - before))
        if freeze:
            np.testing.assert_array_equal(w_next[:, :width], w)
            np.testing.assert_array_equal(v_next[:width], v)
        out[name] = (
            *drift, rms(before - ya_test),
            rms(forward(a_test, w_next, v_next) - ya_test),
            rms(forward(b_test, w_next, v_next) - yb_test),
        )
    return out


def endogenous(rng):
    bins, rounds, batch = 128, 200, 8
    grid = np.linspace(-1, 1, bins)
    x = np.column_stack((grid, np.ones(bins)))
    p_positive = np.where(grid < -0.25, 0.12, np.where(grid < 0.35, 0.90, 0.48))

    def evaluate(weights):
        # Exact expected fixed-population scores, independent of the return policy.
        logits = x @ weights
        acc = np.where(logits >= 0, p_positive, 1 - p_positive).mean()
        nll = (np.logaddexp(0, logits) - p_positive * logits).mean()
        return acc, nll

    a_train = rng.integers(bins, size=1536)
    ya = rng.random(len(a_train)) < p_positive[a_train]
    w_old = np.zeros(x.shape[1])
    for _ in range(150):
        w_old -= 0.25 * (x[a_train].T @ (sigmoid(x[a_train] @ w_old) - ya)) / len(ya)

    draws = rng.random((rounds, batch))
    labels = rng.random((rounds, batch))
    out = {"Before deployment": (*evaluate(w_old), np.nan, np.nan)}
    for name, p_return_neg in [
        ("Exogenous", 1),
        ("3× positive return", 1 / 3),
        ("Positive-only + sentinel", 0),
    ]:
        residual = np.zeros_like(w_old)
        recent = np.zeros(bins, dtype=bool)
        for t, (selection, label_draw) in enumerate(zip(draws, labels)):
            predicted_positive = x @ (w_old + residual) >= 0
            rates = np.where(predicted_positive, 1, p_return_neg)
            # One always-returning bin keeps the hard policy from halting entirely.
            if p_return_neg == 0:
                rates[-1] = 1
            cumulative = rates.cumsum()
            idx = np.searchsorted(cumulative, cumulative[-1] * selection, side="right")
            y = label_draw < p_positive[idx]
            if t >= rounds - 50:
                recent[idx] = True
            # Learn only a new residual; the deployed base coefficients are frozen.
            residual -= 0.25 * (x[idx].T @ (sigmoid(x[idx] @ (w_old + residual)) - y)) / batch
        structurally_missing = ((x[:-1] @ (w_old + residual)) < 0).sum() / bins if p_return_neg == 0 else 0
        out[name] = (*evaluate(w_old + residual), (~recent).mean(), structurally_missing)
    return out


def table(headers, experiment, percent=()):
    results = [experiment(np.random.default_rng(seed)) for seed in SEEDS]
    print("| " + " | ".join(("Arm", *headers)) + " |")
    print("|" + "---|" * (len(headers) + 1))
    for arm in results[0]:
        values = np.array([result[arm] for result in results])
        cells = []
        for i, column in enumerate(values.T):
            if np.isnan(column).all():
                cells.append("—")
            elif i in percent:
                cells.append(f"{100 * column.mean():.2f} ± {100 * column.std(ddof=1):.2f}%")
            else:
                cells.append(f"{column.mean():.3f} ± {column.std(ddof=1):.3f}")
        print("| " + " | ".join((arm, *cells)) + " |")
    print()


def main():
    print("Five seeds (0–4), mean ± sample SD. NLL is in nats.")
    print("\n### Vocabulary growth (20 → 25 output rows)\n")
    print("Old logits are frozen. For the two-head arm, any A NLL increase is due to the selector.\n")
    table(
        ("A NLL", "A acc.", "Δ A NLL", "Shared log-Z share", "B NLL", "B acc."),
        vocabulary,
        percent=(1, 3, 5),
    )
    print("### Function-preserving widening (12 → 36 hidden units)\n")
    print("A drift is RMS prediction change from insertion, not error against A labels.\n")
    table(
        ("A drift step 0", "A drift step 1", "A drift step 5", "A drift step 10",
         "A RMSE step 0", "A RMSE step 100", "B RMSE step 100"),
        architecture,
    )
    print("### Endogenous deployment stream (1,600 training labels per arm)\n")
    print("A scores average over the fixed uniform population; only a new residual is trained.\n")
    table(
        ("A acc.", "A NLL", "Unlabeled bins, last 50 rounds", "Zero-support bins after training"),
        endogenous,
        percent=(0, 2, 3),
    )


if __name__ == "__main__":
    main()
