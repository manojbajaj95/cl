"""Three-checkpoint G1 router from PR #14, with frozen Q2 data splits."""

from itertools import product

import numpy as np


STEPS = 3
CODES = 12
ACTIONS = "ABC"
RULE = (
    "You route codes through three checkpoints. At each checkpoint choose "
    "exactly one tool: A, B, or C. Divide the displayed code by 3. "
    "Remainder 0 requires B, remainder 1 requires C, remainder 2 requires A. "
    "A run succeeds if at least two routes are correct."
)
SOURCE = (0, 1, 2, 6, 7, 8)
TRUTH_HALVES = ((3, 4, 5), (9, 10, 11))
TRUTH_STARTS = TRUTH_HALVES[0] + TRUTH_HALVES[1]


def correct(code):
    return (code + 11) % 3


def transition(code, action, step):
    return (5 * code + 2 * action + 1 + step) % CODES


def episodes(baseline, n, seed, starts=SOURCE):
    rng = np.random.default_rng(seed)
    states = np.empty((n, STEPS), dtype=int)
    states[:, 0] = rng.choice(starts, size=n)
    actions = np.empty_like(states)
    uniforms = rng.random(states.shape)
    for step in range(STEPS):
        code = states[:, step]
        cdf = np.exp(baseline[step, code]).cumsum(axis=-1)
        cdf[:, -1] = 1
        actions[:, step] = (uniforms[:, step, None] >= cdf).sum(axis=-1)
        if step + 1 < STEPS:
            states[:, step + 1] = transition(code, actions[:, step], step)
    return {"states": states, "actions": actions, "success": (actions == correct(states)).sum(axis=1) >= 2}


def exact_success(logp, starts=TRUTH_STARTS):
    """Sum all successful action-path probabilities for each start."""
    starts = np.asarray(starts)
    success = np.zeros(logp.shape[:-3] + starts.shape)
    for actions in product(range(len(ACTIONS)), repeat=STEPS):
        code = starts
        hits = np.zeros_like(starts)
        path = np.zeros_like(success)
        for step, action in enumerate(actions):
            path += logp[..., step, code, action]
            hits += correct(code) == action
            code = transition(code, action, step)
        success += np.exp(path) * (hits >= 2)
    return success
