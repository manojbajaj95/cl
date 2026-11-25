"""Matched-gain sequential regression with a frozen ReLU feature layer."""

import os
from dataclasses import dataclass

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np


DIM = 256
OLD_RANK = 32
SEEDS = 128
EPS = 1e-3
TARGET = 0.25
MAX_STEPS = 4096


def loss(weights, labels):
    # The fixed questions are one-hot inputs. ReLU leaves their features unchanged.
    # We use the equivalent question-aligned head basis, so null coordinates need
    # not be evaluated. The objectives are normalized to unit curvature per feature.
    return 0.5 * np.square(weights - labels).sum(axis=1)


@dataclass
class Result:
    steps: np.ndarray
    damage: np.ndarray


def run(rank, method, protect=False):
    # Task A's targets are independent of B's. A is fitted analytically so every
    # method starts B at exactly the same zero-loss old solution.
    data = np.random.default_rng(872)
    old = data.choice([-1.0, 1.0], (SEEDS, OLD_RANK)) / np.sqrt(OLD_RANK)
    new = data.standard_normal((SEEDS, rank))
    new /= np.linalg.norm(new, axis=1, keepdims=True)
    w = np.zeros((SEEDS, DIM))
    w[:, :OLD_RANK] = old
    steps = np.zeros(SEEDS, dtype=int)
    damage = np.full(SEEDS, np.nan)
    b = slice(OLD_RANK, OLD_RANK + rank)
    noise = np.random.default_rng(631)

    for step in range(1, MAX_STEPS + 1):
        if method == "gradient":
            move = np.zeros_like(w)
            move[:, b] = new - w[:, b]
        else:
            z = noise.standard_normal(w.shape)
            if protect:
                z[:, :OLD_RANK] = 0
            minus = loss(w[:, b] - EPS * z[:, b], new)
            plus = loss(w[:, b] + EPS * z[:, b], new)
            if method == "scalar":
                eta = 1 / (rank + 2)
                direction = (minus - plus) / (2 * EPS)
            elif method == "binary":
                # One noiseless preference bit; ties have probability zero here.
                # The step is fixed using only the known initial norm and rank.
                eta = np.sqrt(2 / np.pi) / rank
                direction = np.sign(minus - plus)
            else:
                raise ValueError(method)
            move = (eta * direction)[:, None] * z

        cross = (steps == 0) & (loss(w[:, b] + move[:, b], new) <= TARGET)
        if cross.any():
            # Diagnostic only: interpolate the last step to equalize gain exactly.
            # This reads the synthetic objective; no training step uses these data.
            lo, hi = np.zeros(cross.sum()), np.ones(cross.sum())
            for _ in range(32):
                mid = (lo + hi) / 2
                below = loss(w[cross, b] + mid[:, None] * move[cross, b], new[cross]) <= TARGET
                hi = np.where(below, mid, hi)
                lo = np.where(below, lo, mid)
            assert np.allclose(loss(w[cross, b] + hi[:, None] * move[cross, b], new[cross]), TARGET)
            at_match = w[cross, :OLD_RANK] + hi[:, None] * move[cross, :OLD_RANK]
            damage[cross] = loss(at_match, old[cross])
            steps[cross] = step
        if steps.all():
            break
        w[steps == 0] += move[steps == 0]

    if not steps.all():
        raise RuntimeError(f"{(steps == 0).sum()} seeds did not reach 50% gain")
    return Result(steps, damage)


def interval(values, indices):
    lo, hi = np.quantile(values[indices].mean(axis=1), [0.025, 0.975])
    return f"{values.mean():.4f} [{lo:.4f}, {hi:.4f}]"


def main():
    indices = np.random.default_rng(691).integers(SEEDS, size=(5000, SEEDS))
    print(f"D={DIM}, old rank={OLD_RANK}, {SEEDS} seeds, 50% new-task loss reduction")
    print("rank | method | update steps (95% CI) | old loss gain (95% CI)")
    for rank in [8, 32, 128]:
        reference = run(rank, "gradient")
        print(f"{rank} | gradient | {interval(reference.steps, indices)} | "
              f"{interval(reference.damage, indices)}")
        for method in ["scalar", "binary"]:
            dense = run(rank, method)
            projected = run(rank, method, protect=True)
            assert np.array_equal(dense.steps, projected.steps)
            assert not projected.damage.any()
            print(f"{rank} | {method} | {interval(dense.steps, indices)} | "
                  f"{interval(dense.damage, indices)}; projected: 0 (same steps)")


if __name__ == "__main__":
    main()
