"""Paired metrics for learned queue policies (all rates on [0, 1])."""

import random
from statistics import fmean, quantiles


def contrasts(row):
    target = row["target"]
    errors = {key: abs(row[key] - target) for key in ("base", "context", "weights", "both", "evict")}
    return {
        **{f"{key}_mae": error for key, error in errors.items()},
        "context_gain": errors["base"] - errors["context"],
        "evict_gain": errors["base"] - errors["evict"],
        "evict_vs_context_mae": errors["evict"] - errors["context"],
        "signed_both": row["direction"] * (row["both"] - target),
    }


def oscillates(errors, growth=0.01, margin=0.03):
    return any(
        min(abs(a), abs(b), abs(c)) > margin and a * b < 0 and b * c < 0
        and abs(b) - abs(a) >= growth and abs(c) - abs(b) >= growth
        for a, b, c in zip(errors, errors[1:], errors[2:])
    )


def flip(probe):
    return probe["weights_old"] >= 0.5 and probe["contradiction_old"] < 0.5


def absorption(probe):
    return probe["weights_old"] - probe["base_old"]


def match_absorption(first, later, caliper=0.10):
    return [
        (a, b) for key, a in first.items() if (b := later.get(key)) is not None
        and min(a["weights_old"], b["weights_old"]) >= 0.5
        and abs(absorption(a) - absorption(b)) <= caliper
    ]


def seed_interval(matrix, draws=10_000, cross_lessons=False, seed=3903):
    """Bootstrap whole paired seeds; optionally cross-resample the lesson axis."""
    rng = random.Random(seed)
    n_seeds, n_lessons = len(matrix), len(matrix[0])
    estimate = fmean(map(fmean, matrix))
    samples = []
    for _ in range(draws):
        seeds = rng.choices(range(n_seeds), k=n_seeds)
        if cross_lessons:
            lessons = rng.choices(range(n_lessons), k=n_lessons)
            samples.append(fmean(matrix[i][j] for i in seeds for j in lessons))
        else:
            samples.append(fmean(fmean(matrix[i]) for i in seeds))
    quantile = quantiles(samples, n=40, method="inclusive")
    return estimate, quantile[0], quantile[-1]
