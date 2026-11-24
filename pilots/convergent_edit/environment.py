import json
import random
from dataclasses import dataclass


TRAIN = ("inventory", "schedule", "routing")
HELD_OUT = "eligibility"
SEEDS = (11, 29, 47)
BASE = "Solve the task from its supplied records. Return only the requested integer."
CALIBRATION_START = 1000
TASK_SHAPES = {
    "inventory": "Filter events by category and a cutoff, then compute a signed update to an initial quantity.",
    "schedule": "Count qualifying intervals using a category and an inclusive start and exclusive end.",
    "routing": "Compute each valid alternative's total from linked components and compare the totals.",
}


@dataclass(frozen=True)
class Task:
    family: str
    index: int
    question: str
    records: tuple
    answer: int
    choices: tuple

    def prompt(self, variant=0):
        data = self.records
        choices = self.choices
        if variant == 1:
            data = tuple(dict(reversed(tuple(row.items()))) for row in reversed(data))
            choices = choices[::-1]
        question = f"{self.question} Choose one of: {', '.join(map(str, choices))}."
        if variant == 2:
            payload = json.dumps({str(i): row for i, row in enumerate(data)}, indent=2)
            return f"Question: {question}\nRecords (indexed for display only):\n{payload}"
        return f"Records (order does not matter): {json.dumps(data, separators=(',', ':'))}\nQuestion: {question}"


def make_task(family, index):
    version = "v3" if family in (HELD_OUT, "routing") else "v2"
    rng = random.Random(f"hw1-{version}:{family}:{index}")
    if family == "inventory":
        bins = ("red", "blue", "green")
        target = rng.choice(bins)
        events = rng.sample(range(1, 8), 4)
        cutoff = sorted(events)[rng.randint(1, 3)]
        records = [
            dict(day=day, bin=rng.choice((target, target, *bins)), change=rng.choice((-2, -1, 1, 2)))
            for day in events
        ]
        question = f"Bin {target} has 5 items initially. What is its balance after changes on or before day {cutoff}?"
        answer = 5 + sum(r["change"] for r in records if r["bin"] == target and r["day"] <= cutoff)
    elif family == "schedule":
        records = []
        for _ in range(4):
            start = rng.randrange(1, 7)
            records.append(dict(start=start, end=start + rng.randint(1, 4), room=rng.choice(("A", "B"))))
        at = rng.randrange(2, 8)
        room = rng.choice(("A", "B"))
        question = f"How many meetings in room {room} are active at time {at}? Start is inclusive, end exclusive."
        answer = sum(r["room"] == room and r["start"] <= at < r["end"] for r in records)
    elif family == "routing":
        edges = (("A", "B"), ("B", "Z"), ("A", "Z"))
        records = [dict(source=a, destination=b, cost=rng.randint(1, 5)) for a, b in edges]
        best = {"A": 0}
        for row in records:
            a, b, cost = row.values()
            best[b] = min(best.get(b, 100), best[a] + cost)
        question = "What is the lowest cost from A to Z? Compare the direct edge to the sum of the two edges via B."
        answer = best["Z"]
    elif family == HELD_OUT:
        records = [dict(points=rng.randint(1, 7), active=rng.choice(("yes", "yes", "no")))
                   for _ in range(3)]
        threshold = rng.randrange(2, 7)
        if index % 2:
            question = f"How many members are active and have at least {threshold} points?"
            answer = sum(r["active"] == "yes" and r["points"] >= threshold for r in records)
        else:
            question = f"How many members have at least {threshold} points, regardless of active status?"
            answer = sum(r["points"] >= threshold for r in records)
    else:
        raise ValueError(f"Unknown family: {family}")
    rng.shuffle(records)
    options = range(len(records) + 1) if family == HELD_OUT else range(max(0, answer - 3), answer + 4)
    choices = rng.sample([n for n in options if n != answer], 2)
    block, offset = divmod(index, 3)
    positions = random.Random(f"hw1-choice-order:{family}:{block}").sample(range(3), 3)
    choices.insert(positions[offset], answer)
    return Task(family, index, question, tuple(records), answer, tuple(choices))


def harness(edits):
    return "\n".join([BASE] + [f"- {edit}" for edit in edits])
