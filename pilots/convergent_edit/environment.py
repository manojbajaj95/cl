import json
import random
from dataclasses import dataclass


TRAIN = ("inventory", "schedule", "routing")
HELD_OUT = "eligibility"
SEEDS = (11, 29, 47)
BASE = "Solve the task from its supplied records. Return only the requested integer."


@dataclass(frozen=True)
class Task:
    family: str
    index: int
    question: str
    records: tuple
    answer: int

    def prompt(self, variant=0):
        data = self.records
        if variant == 1:
            data = tuple(dict(reversed(tuple(row.items()))) for row in reversed(data))
        if variant == 2:
            payload = json.dumps({str(i): row for i, row in enumerate(data)}, indent=2)
            return f"Question: {self.question}\nRecords (indexed for display only):\n{payload}"
        return f"Records (display order has no significance): {json.dumps(data)}\nQuestion: {self.question}"


def make_task(family, index):
    rng = random.Random(f"hw1-v1:{family}:{index}")
    if family == "inventory":
        bins = ("red", "blue", "green")
        target = rng.choice(bins)
        events = rng.sample(range(1, 20), 8)
        cutoff = sorted(events)[rng.randint(3, 6)]
        records = [
            dict(day=day, bin=rng.choice(bins), change=rng.choice((-3, -2, 1, 2, 4)))
            for day in events
        ]
        question = f"Bin {target} starts at 12. What is its balance after all changes through day {cutoff}, inclusive?"
        answer = 12 + sum(r["change"] for r in records if r["bin"] == target and r["day"] <= cutoff)
    elif family == "schedule":
        records = []
        for _ in range(8):
            start = rng.randrange(16)
            records.append(dict(start=start, end=start + rng.randint(1, 7), room=rng.choice(("A", "B"))))
        at = rng.randrange(5, 16)
        room = rng.choice(("A", "B"))
        question = f"How many meetings in room {room} are active at time {at}? Start is inclusive, end exclusive."
        answer = sum(r["room"] == room and r["start"] <= at < r["end"] for r in records)
    elif family == "routing":
        edges = (("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "Z"),
                 ("C", "D"), ("C", "Z"), ("D", "Z"))
        records = [dict(source=a, destination=b, cost=rng.randint(1, 9)) for a, b in edges]
        best = {"A": 0}
        for row in records:
            a, b, cost = row.values()
            best[b] = min(best.get(b, 100), best[a] + cost)
        question = "What is the minimum summed cost from A to Z? Edges are directed."
        answer = best["Z"]
    elif family == HELD_OUT:
        records = [dict(id=i, points=rng.randint(2, 12), active=rng.choice((True, False)),
                        waived=rng.choice((True, False))) for i in range(1, 9)]
        threshold = rng.randrange(5, 11)
        question = f"Sum the IDs of active members with at least {threshold} points or a waiver. Inactive members never qualify."
        answer = sum(r["id"] for r in records if r["active"] and (r["points"] >= threshold or r["waived"]))
    else:
        raise ValueError(f"Unknown family: {family}")
    rng.shuffle(records)
    return Task(family, index, question, tuple(records), answer)


def harness(edits):
    return "\n".join([BASE] + [f"- {edit}" for edit in edits])
