"""Typed, valid Dyck prefixes with a pending matching close."""

from dataclasses import dataclass
from functools import lru_cache
from random import Random


OPEN = "([{<"
CLOSE = ")]}>"
LABELS = "ABCD"
RULE = (
    "Read a prefix of correctly nested brackets from left to right. An opening bracket "
    "pushes its type; a closing bracket pops the most recent unmatched opening bracket. "
    "Which closing bracket comes next to match the top? Use A for ), B for ], C for }, D for >."
)


@dataclass(frozen=True)
class Example:
    tape: tuple[str, ...]

    def states(self):
        stack = []
        for token in self.tape:
            if token in OPEN:
                stack.append(OPEN.index(token))
            else:
                if not stack or CLOSE.index(token) != stack.pop():
                    raise ValueError("Not a valid Dyck prefix")
            yield tuple(stack)

    @property
    def answer(self):
        return LABELS[list(self.states())[-1][-1]]

    @property
    def trace(self):
        indices = {len(self.tape) // 3, 2 * len(self.tape) // 3, len(self.tape)}
        return " ".join(
            f"{i}:{''.join(LABELS[j] for j in state) or '-'}"
            for i, state in enumerate(self.states(), 1) if i in indices
        )

    @property
    def source(self):
        return " ".join(self.tape)


def sample(rng, depth, length, label):
    height = rng.choice(range(2, depth - 1, 2))

    @lru_cache(maxsize=None)
    def ways(left, h, peaked):
        if not left:
            return int(h == height and peaked)
        ups = ways(left - 1, h + 1, peaked or h + 1 == depth) if left > 2 and h < depth else 0
        downs = ways(left - 1, h - 1, peaked) if h else 0
        return ups + downs

    events, unmatched, peaked = [], [], False
    for left in range(length, 0, -1):
        h = len(unmatched)
        ups = ways(left - 1, h + 1, peaked or h + 1 == depth) if left > 2 and h < depth else 0
        if rng.randrange(ways(left, h, peaked)) < ups:
            unmatched.append(len(events))
            events.append((True, len(events)))
            peaked |= h + 1 == depth
        else:
            events.append((False, unmatched.pop()))
    types = {i: rng.randrange(len(OPEN)) for opening, i in events if opening}
    types[unmatched[-1]] = label
    return Example(tuple((OPEN if opening else CLOSE)[types[i]] for opening, i in events))


def datasets(seed, n):
    seen = set()

    def split(name, depth, size):
        rng = Random(f"h1:{seed}:{name}:{depth}")
        labels = [i % len(LABELS) for i in range(size)]
        rng.shuffle(labels)
        rows = []
        for label in labels:
            row = sample(rng, depth, 4 * depth, label)
            while row.tape in seen:
                row = sample(rng, depth, 4 * depth, label)
            seen.add(row.tape)
            rows.append(row)
        return rows

    return split("install", 4, 64), {depth: split("test", depth, n) for depth in (4, 8, 12)}


def prompt(row, demos=(), scratch=False):
    stem = RULE + " Emit only the answer letter."
    if scratch:
        stem = RULE + (
            " Work in one line: at one third, two thirds, and the end, give"
            " position:stack with letters bottom to top (- if empty). Finish with => and the answer letter."
        )
    shots = sorted(demos, key=lambda d: abs(len(d.tape) - len(row.tape)))[:3]
    precedents = [f"{d.source} -> " + (f"{d.trace} => " if scratch else "") + d.answer for d in shots]
    return "\n".join([stem, *precedents, f"{row.source} ->"])


def scratch_answer(raw):
    trace, sep, answer = raw.partition("\n")[0].rpartition("=>")
    return answer.strip() if sep and trace.strip() else ""


def development():
    rules = (
        ("Count plus signs modulo 5; R resets to zero.", 0,
         lambda s, x: (s + 1) % 5 if x == "+" else 0, "+R"),
        ("Start at 1; replace s with (2*s + digit) modulo 5.", 1,
         lambda s, x: (2 * s + int(x)) % 5, "01234"),
        ("Start off (0). T flips the bit; N does nothing.", 0,
         lambda s, x: s ^ (x == "T"), "TN"),
        ("Start at 0. A advances around a 5-state ring, B moves back, C doubles. Wrap modulo 5.", 0,
         lambda s, x: (s + 1 if x == "A" else s - 1 if x == "B" else 2 * s) % 5, "ABC"),
    )
    rng = Random(8189)
    rows = []
    for _ in range(8):
        for rule, initial, step, symbols in rules:
            tape = rng.choices(symbols, k=rng.choice((8, 16, 24)))
            state = initial
            for symbol in tape:
                state = step(state, symbol)
            rows.append((
                f"{rule} Report the final state as A=0, B=1, C=2, D=3, E=4.\n{' '.join(tape)} ->",
                " " + "ABCDE"[state],
            ))
    return rows
