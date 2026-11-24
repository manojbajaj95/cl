"""Baseline-only selection and matching for the A3 margin-vs-scale test."""

from itertools import permutations

import numpy as np


STEPS, CODES = 3, 12
STATES = STEPS * CODES
SOURCE = np.arange(6)
TEST = np.arange(6, STATES)
SMALL_MARGIN = 1.0
MIN_NATURAL_STATES = 30
LABEL_SETS = ("XYZ", "DEF", "JKL", "PQR", "UVW", "GHI", "MNO", "STV")
MENU_ORDERS = tuple(order for order in permutations(range(3)) if order != (0, 1, 2))


def top_two(scores):
    ranked = np.argsort(-scores, axis=-1, kind="stable")
    best = np.take_along_axis(scores, ranked[..., :2], axis=-1)
    return ranked[..., :2], best[..., 0] - best[..., 1]


def in_small_bins(gaps):
    return (gaps > 0) & (gaps < SMALL_MARGIN)


def offset_a(scores, offset):
    return scores - np.asarray(offset)[..., None] * np.array([1, 0, 0])


def fit_offset(old_source, new_source):
    _, reference = top_two(old_source)
    if not in_small_bins(reference).all() or not (new_source.argmax(-1) == 0).all():
        raise ValueError("Source baselines do not satisfy predeclared margin conditions")
    cap = np.min(new_source[:, 0] - new_source[:, 1:].max(-1))
    grid = np.arange(0, cap, 0.005)
    _, gaps = top_two(offset_a(new_source, grid[:, None]))
    loss = np.abs(np.sort(gaps, axis=-1) - np.sort(reference)).mean(axis=-1)
    i = loss.argmin()
    return float(grid[i]), float(loss[i])


def eligibility(base, states):
    """Return the eligible observations and their top two canonical actions."""
    pair, gap = top_two(base)
    states = np.asarray(states)
    ids = states[in_small_bins(gap[states])]
    return ids, pair[ids], gap[ids]
