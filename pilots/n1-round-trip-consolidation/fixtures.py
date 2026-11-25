import json
import random
import re
from itertools import groupby


def transpose(x):
    return [list(row) for row in zip(*x)]


def outline(x):
    return [[v if i in (0, len(x) - 1) or j in (0, len(row) - 1) else 0
             for j, v in enumerate(row)] for i, row in enumerate(x)]


FAMILIES = {
    "rotate_text": ("str", "str", lambda x: x[1:] + x[:1]),
    "collapse_runs": ("str", "str", lambda x: "".join(v for v, _ in groupby(x))),
    "sort_unique": ("str", "str", lambda x: "".join(sorted(set(x)))),
    "odd_then_even": ("str", "str", lambda x: x[1::2] + x[::2]),
    "reverse_words": ("str", "str", lambda x: " ".join(w[::-1] for w in x.split(" "))),
    "double_digits": ("str", "str", lambda x: "".join(c * (2 if c.isdigit() else 1) for c in x)),
    "rotate_grid": ("list[list[int]]", "list[list[int]]", lambda x: transpose(x[::-1])),
    "transpose": ("list[list[int]]", "list[list[int]]", transpose),
    "serpentine": ("list[list[int]]", "list[int]", lambda x: sum(
        [row if i % 2 == 0 else row[::-1] for i, row in enumerate(x)], [])),
    "outline": ("list[list[int]]", "list[list[int]]", outline),
    "column_max": ("list[list[int]]", "list[int]", lambda x: list(map(max, zip(*x)))),
    "zero_swap": ("list[list[int]]", "list[list[int]]", lambda x: [
        [1 if v == 0 else 0 if v == 1 else v for v in row] for row in x]),
}


def signature(family):
    input_type, output_type, _ = FAMILIES[family]
    return f"def transform(x: {input_type}) -> {output_type}:"


def draw_input(rng, family, held):
    if FAMILIES[family][0] != "str":
        rows = rng.randint(3, 5) if held else rng.randint(2, 3)
        cols = rows + rng.choice([-2, -1, 1, 2]) if held else rows
        alphabet = [-3, -1, 0, 1, 2, 5] if held else [0, 1, 2]
        return [[rng.choice(alphabet) for _ in range(cols)] for _ in range(rows)]
    n = rng.randint(7, 13) if held else rng.randint(3, 5)
    alphabet = "abcdefXYZ" if held else "abc"
    if family == "reverse_words":
        return " ".join("".join(rng.choices(alphabet, k=rng.randint(2, 4)))
                        for _ in range(rng.randint(3, 5) if held else 2))
    if family == "double_digits":
        alphabet += "0123456789" if held else "12"
    return "".join(rng.choices(alphabet, k=n))


def make_splits(seed, family):
    rng = random.Random(f"{seed}:{family}")
    used = set()

    def sample(count, held=False):
        cases = []
        while len(cases) < count:
            x = draw_input(rng, family, held)
            key = json.dumps(x)
            if key not in used:
                cases.append((x, FAMILIES[family][2](x)))
                used.add(key)
        return cases

    return sample(10), sample(10), sample(32, held=True)


def examples(cases):
    return "\n".join(f"{x!r} -> {y!r}" for x, y in cases)


def code_from(response):
    blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", response, re.S)
    return (blocks[0] if blocks else response).strip()
