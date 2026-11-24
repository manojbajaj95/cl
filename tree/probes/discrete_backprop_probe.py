"""Exhaustive finite probe for one-cell repair in a stateful tool loop."""

from itertools import permutations

import numpy as np


WIDTH = 6
HORIZON = 3
SEEDS = range(16)
PORTS = ("retrieve", "plan", "act")


def world(seed, site):
    rng = np.random.default_rng(seed)
    retrieve, plan = (rng.permutation(WIDTH) for _ in range(2))
    act = np.argsort(plan[retrieve])
    bank = np.stack([retrieve, plan, act])
    target, alias, followup = map(int, rng.choice(WIDTH, 3, replace=False))
    entry = (target, retrieve[target], plan[retrieve[target]])[site]
    collider = (alias, retrieve[alias], plan[retrieve[alias]])[site]
    bank[site, entry] = bank[site, collider]
    return bank, target, alias, followup, (site, entry)


def candidates(bank):
    edits = [None]
    banks = [bank]
    for site, entry in np.ndindex(bank.shape):
        for value in range(WIDTH):
            if value != bank[site, entry]:
                edited = bank.copy()
                edited[site, entry] = value
                edits.append((site, entry, value))
                banks.append(edited)
    return edits, np.stack(banks)


def rollout(bank, task):
    phase = 0
    for _ in range(HORIZON):
        goal = task[phase]
        retrieved = bank[0, goal]
        planned = bank[1, retrieved]
        action = bank[2, planned]
        if action == goal:
            phase += 1
            if phase == len(task):
                return True
    return False


def backwards(banks, task):
    # Each column in the acceptance predicates uses the same candidate at every
    # port and iteration; independent per-call substitutions would not be edits.
    candidate = np.arange(len(banks))
    next_ok = np.zeros((len(task) + 1, len(banks)), dtype=bool)
    next_ok[-1] = True
    for _ in range(HORIZON):
        ok = next_ok.copy()
        for phase, goal in enumerate(task):
            action_ok = np.broadcast_to(next_ok[phase, :, None], (len(banks), WIDTH)).copy()
            action_ok[:, goal] = next_ok[phase + 1]
            plan_ok = action_ok[candidate[:, None], banks[:, 2]]
            retrieve_ok = plan_ok[candidate[:, None], banks[:, 1]]
            ok[phase] = retrieve_ok[candidate, banks[:, 0, goal]]
        next_ok = ok
    return next_ok[0]


def probe(seed, site):
    bank, target, alias, followup, planted = world(seed, site)
    edits, banks = candidates(bank)
    goal = (target, followup)
    old = [x for x in range(WIDTH) if x != target]
    anchors = [(x, x) for x in old]
    held_out = list(permutations(old, 2))
    terminal = backwards(banks, goal)
    replay = np.array([rollout(candidate, goal) for candidate in banks])
    assert np.array_equal(terminal, replay)
    assert not terminal[0]
    protected = terminal.copy()
    blind = terminal.copy()
    for anchor in anchors:
        accepts = backwards(banks, anchor)
        assert np.array_equal(accepts, [rollout(candidate, anchor) for candidate in banks])
        assert accepts[0]
        protected &= accepts
        if anchor[0] != alias:
            blind &= accepts
    possible = np.flatnonzero(terminal)
    retained = np.flatnonzero(protected)
    assert len(retained) and all(edits[i][:2] == planted for i in retained)
    assert len(possible) == len(PORTS) - site and len(retained) == 1
    assert np.array_equal(blind, terminal)

    def retention(indices):
        return np.mean([[rollout(banks[i], task) for task in held_out] for i in indices])

    assert retention([0]) == 1
    return (
        len(possible),
        len(retained),
        np.count_nonzero(blind),
        np.mean([edits[i][:2] == planted for i in possible]),
        retention(possible),
        retention(retained),
    )


def main():
    all_rows = []
    print(f"seeds 0–{len(SEEDS) - 1} per site; {3 * WIDTH * (WIDTH - 1)} one-cell edits plus no-op")
    print("site      target edits  protected  alias hidden  replay localization  replay old  protected old")
    for site, port in enumerate(PORTS):
        rows = np.array([probe(seed, site) for seed in SEEDS])
        np.testing.assert_allclose(rows, np.broadcast_to(rows[0], rows.shape))
        all_rows.extend(rows)
        n, keep, blind, localization, old, protected_old = np.mean(rows, axis=0)
        print(
            f"{port:8} {n:12.0f} {keep:10.0f} {blind:13.0f} "
            f"{localization:20.1%} {old:11.1%} {protected_old:14.1%}"
        )
    _, _, _, localization, old, protected_old = np.mean(all_rows, axis=0)
    print(f"balanced mean replay localization {localization:.1%}; replay old {old:.1%}; protected old {protected_old:.1%}")
    print("Checks: backward masks match forward replay; planted cell is the unique protected repair.")


if __name__ == "__main__":
    main()
