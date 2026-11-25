from itertools import product

import numpy as np


ACTIONS = "ABC"
STEPS, CODES = 3, 12
SOURCE, HELD_OUT = tuple(range(6)), tuple(range(6, 12))
RULE = (
    "You route codes through three checkpoints. At each checkpoint choose "
    "exactly one tool: A, B, or C. Divide the displayed code by 3. "
    "Remainder 0 requires B, remainder 1 requires C, remainder 2 requires A. "
    "A run succeeds if at least two routes are correct."
)
UPDATE = "The routing rule changed: remainder 0 now requires C, and remainders 1 and 2 require A."


def correct(code):
    return np.take([2, 0, 0], (np.asarray(code) + 10) % 3)


def transition(code, action, step):
    return (5 * code + 2 * action + 1 + step) % CODES


def episodes(logp, starts, n, seed):
    rng = np.random.default_rng(seed)
    states = np.empty((n, STEPS), dtype=int)
    states[:, 0] = rng.choice(starts, size=n)
    actions = np.empty_like(states)
    uniforms = rng.random(states.shape)
    for step in range(STEPS):
        code = states[:, step]
        cdf = np.exp(logp[step, code]).cumsum(axis=-1)
        cdf[:, -1] = 1
        actions[:, step] = (uniforms[:, step, None] >= cdf).sum(axis=-1)
        if step + 1 < STEPS:
            states[:, step + 1] = transition(code, actions[:, step], step)
    return states, actions, (actions == correct(states)).sum(1) >= 2


def exact_success(logp, starts):
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


def start_visitation(logp, starts):
    visits = np.zeros((STEPS, CODES))
    np.add.at(visits[0], list(starts), 1 / len(starts))
    for step in range(STEPS - 1):
        for a in range(len(ACTIONS)):
            dest = transition(np.arange(CODES), a, step)
            np.add.at(visits[step + 1], dest, visits[step] * np.exp(logp[step, :, a]))
    return visits / STEPS
