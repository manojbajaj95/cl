import argparse
from itertools import product

import numpy as np


STATES = 7
MACRO = (0, 1, 0)


def primitive_tables(payload, mode):
    x = np.arange(STATES)
    tables = {}
    for token, values in payload.items():
        a, b = map(int, values)
        if mode == "rules":
            tables[token] = (a * x + b) % STATES
        elif mode == "induction":
            tables[token] = ((b - a) * x + a) % STATES
        else:
            tables[token] = x.copy()
            tables[token][:2] = (a, b)
    if set(MACRO) <= tables.keys():
        tables[3] = np.arange(STATES)
        for token in MACRO:
            tables[3] = tables[token][tables[3]]
    return tables


def rematerialize(anchors, tables):
    inverse = np.linalg.pinv(anchors)
    if not np.allclose(anchors @ inverse, np.eye(STATES), atol=1e-9):
        return None
    matrices = {token: inverse @ anchors[transition] for token, transition in tables.items()}
    return matrices, inverse


def evaluate(anchors, program, desired):
    matrix, readout = program
    correct, total = 0, 0
    for size in range(2, 5):
        for sequence in product(desired, repeat=size):
            h, logical = anchors, np.arange(STATES)
            for token in sequence:
                h, logical = h @ matrix[token], desired[token][logical]
            correct += ((h @ readout).argmax(axis=1) == logical).sum()
            total += STATES
    return correct / total


def run(seed):
    rng = np.random.default_rng(seed)
    rules = {token: tuple(np.array([rng.integers(2, STATES), rng.integers(STATES)], dtype=np.uint8))
             for token in range(3)}
    observations = {token: (b, np.uint8((int(a) + int(b)) % STATES)) for token, (a, b) in rules.items()}
    revision = tuple(np.array([rng.integers(2, STATES), rng.integers(STATES)], dtype=np.uint8))
    while revision == rules[0]:
        revision = tuple(np.array([rng.integers(2, STATES), rng.integers(STATES)], dtype=np.uint8))
    scores = []
    previous_tables = None
    for version, width in enumerate((9, 13, 8, 11)):
        if version == 1:
            a, b = rules[0] = revision
            observations[0] = (b, np.uint8((int(a) + int(b)) % STATES))
        if version == 2:
            del rules[1], observations[1]
        anchors = np.linalg.qr(rng.normal(size=(width, STATES)))[0].T
        if version == 3:
            anchors[1] = anchors[0]
        target = primitive_tables(rules, "rules")
        assert sum(np.asarray(v).nbytes for v in rules.values()) == 2 * len(rules)
        expected_tokens = {0, 1, 2, 3} if version < 2 else {0, 2}
        assert set(target) == expected_tokens
        if version == 1:
            assert np.any(target[0] != previous_tables[0])
            np.testing.assert_array_equal(target[2], previous_tables[2])
        if version == 2:
            for token in expected_tokens:
                np.testing.assert_array_equal(target[token], previous_tables[token])
        previous_tables = target
        for method in ("rules", "induction", "lookup"):
            payload = rules if method == "rules" else observations
            native = rematerialize(anchors, primitive_tables(payload, method))
            if version == 3:
                assert native is None
            else:
                assert native is not None
                assert set(native[0]) == expected_tokens
                scores.append((version, method, evaluate(anchors, native, target)))
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=20)
    args = parser.parse_args()
    if args.seeds < 10:
        parser.error("--seeds must be at least 10")
    scores = [run(seed) for seed in range(args.seeds)]
    print(f"{args.seeds} seeded release chains; 2 bytes per primitive for all methods")
    print("release        rules       two-demo affine induction       lookup")
    for version, label in enumerate(("initial", "revision", "revocation")):
        values = [np.mean([accuracy for rows in scores for v, m, accuracy in rows
                           if v == version and m == method])
                  for method in ("rules", "induction", "lookup")]
        print(f"{label:11}" + "".join(f" {v:8.1%} " for v in values))
    print(f"collapsed anchors: all three methods abstained on all {args.seeds} releases")


if __name__ == "__main__":
    main()
