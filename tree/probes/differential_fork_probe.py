"""CPU positive control: read signs of a linear learner via fixed SGD forks."""

import numpy as np


def success_codes(weights):
    """Each L/R pair starts fresh and updates on one public example to target 1."""
    width = weights.shape[1] - 2
    rows = np.zeros((2, width, width + 2))
    rows[:, :, 0] = 1
    rows[0, :, 1:-1] = np.eye(width)
    rows[1, :, 1:-1] = -np.eye(width)
    predictions = np.einsum("nd,skd->nsk", weights, rows)
    # SGD on squared error / 2; only the public e_0 logit is scored.
    terminal = weights[:, 0, None, None] - 0.5 * (predictions - 1)
    return terminal > 0.5


def train_unrelated(weights, labels):
    """SGD on coordinate examples, with independent distractor targets."""
    weights[:, 1:-1] += 0.15 * (labels - weights[:, 1:-1])
    weights[:, -1] += 0.15 * (1 - weights[:, -1])


def binary_entropy(p):
    p = np.clip(p, np.finfo(float).eps, 1 - np.finfo(float).eps)
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


def run(width, trials=4096):
    rng = np.random.default_rng(2026 + width)
    payload = rng.choice([-1, 1], size=(trials, width))
    # Different old rules share the same public e_0 target.
    weights = np.zeros((trials, width + 2))
    weights[:, 1:-1] = 0.8 * payload
    old_query_gain = rng.uniform(0.25, 1, size=payload.shape)
    erased = success_codes(np.zeros_like(weights))
    assert not erased.any()
    for step in range(65):
        if step in (0, 4, 16, 64):
            left, right = success_codes(weights).transpose(1, 0, 2)
            decoded = np.where(right & ~left, 1, -1)
            direct = np.where(weights[:, 1:-1] * old_query_gain > 0, 1, -1)
            if step == 0:
                assert np.array_equal(decoded, payload)
            assert np.array_equal(decoded, direct)
            assert np.all(left ^ right)
            assert np.all(weights[:, 0] == 0)

            wrong = decoded != payload
            bits = width - binary_entropy(wrong.mean(axis=0)).sum()
            new_mse = np.mean((weights[:, -1] - 1) ** 2)
            print(
                f"{2 * width:2d} {step:2d} {100 * wrong.mean():5.2f} "
                f"{100 * (~wrong.any(axis=1)).mean():6.2f} "
                f"{bits:5.2f} {100 * (direct == payload).mean():6.2f} {new_mse:.5f}"
            )
        if step < 64:
            train_unrelated(weights, rng.normal(size=payload.shape))


if __name__ == "__main__":
    print(" K  H  BER% block%  bits   old% new_MSE")
    for width in (1, 4, 16):
        run(width)
