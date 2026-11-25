"""Score length-matched retrieval doses using the original two-decision challenge."""

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from coding import DEPTHS, DEPTH_ARMS, episode, stream
from collect import FILLERS, Scorer, memories


PROVENANCE = (
    "Earlier patch report", "Prior reusable helper", "Implementation review", "Integration handoff",
    "Maintenance diary", "Refactor note", "Code cleanup summary", "Follow-up review",
)


def groups(k, bad_slot):
    f, b, s = "filler", "bad", "correct"

    def one(special, rest):
        return [special if i == bad_slot else rest for i in range(k)]

    return dict(zip(DEPTH_ARMS, ([f] * k, one(b, f), [b] * k, [s] * k, one(b, s), one(f, s))))


def make_prompts(scorer, k, family_index, task):
    family, variant, solve_order, write_order = task
    # Every note position is used equally across all 16 families at each variant.
    bad_slot = (family_index + variant) % k
    note_pairs = [memories(scorer, *task, filler_index=(variant + i) % len(FILLERS)) for i in range(k)]
    order = [(i + family_index + variant) % len(PROVENANCE) for i in range(k)]
    stacks = {arm: [note_pairs[i][v] for i, v in enumerate(variant_types)]
              for arm, variant_types in groups(k, bad_slot).items()}
    prompts = {}
    for arm, notes in stacks.items():
        memory = "\n" + "\n".join(f"- {PROVENANCE[j]}: {note}" for j, note in zip(order, notes))
        prompts[arm] = [episode(family, variant, solve_order, write_order, memory, path)
                        for path in (None, 0, 1, 2)]
    lengths = {tuple(len(scorer.tokenize(prompt)) for prompt in options) for options in prompts.values()}
    if len(lengths) != 1:
        raise ValueError(f"Full-prompt token counts differ: k={k}, task={family.name}/{variant}: {lengths}")
    tokens = lengths.pop()
    if max(tokens) >= scorer.llm.n_ctx():
        raise ValueError(f"Prompt exceeds context size: {tokens}")
    return prompts, {"k": k, "family": family.name, "variant": variant, "bad_slot": bad_slot,
                     "notes": note_pairs, "provenance_order": order, "tokens": tokens}


def collect_k(scorer, k, tasks, out):
    started = time.monotonic()
    mode = "a" if out.exists() else "x"
    completed = set()
    if out.exists():
        rows = [json.loads(line) for line in out.read_text().splitlines()]
        for i, (row, task) in enumerate(zip(rows, tasks)):
            if (row["k"], row["family"], row["variant"]) != (k, task[0].name, task[1]):
                raise ValueError(f"Resume row {i+1} does not match the frozen task order")
            completed.add(i)
        if len(rows) != len(completed):
            raise ValueError("Invalid resume data")
    with out.open(mode) as f:
        for i, task in enumerate(tasks):
            if i in completed:
                continue
            prompts, row = make_prompts(scorer, k, i // 4, task)
            solve_order, write_order = task[2:]
            orders = [np.argsort(solve_order)] + [np.argsort(write_order)] * 3
            row["logits"] = {arm: [scorer.score(p)[order].tolist() for p, order in zip(ps, orders)]
                             for arm, ps in prompts.items()}
            print(json.dumps(row), file=f, flush=True)
            if (i + 1) % 4 == 0:
                print(f"k={k} {i+1}: {row['family']} ({time.monotonic() - started:.1f}s)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=7)
    parser.add_argument("--depths", type=int, nargs="+", choices=DEPTHS[1:], default=DEPTHS[1:])
    args = parser.parse_args()
    original = json.loads(Path(__file__).with_name("policies.jsonl").read_text().splitlines()[0])
    with args.model.open("rb") as model:
        sha = hashlib.sha256()
        for chunk in iter(lambda: model.read(2**20), b""):
            sha.update(chunk)
    if sha.hexdigest() != original["sha256"]:
        raise ValueError("The depth sweep requires the original checkpoint")
    scorer = Scorer(args.model, args.threads, context=768)
    tasks = list(stream())
    for k in args.depths:
        for i, task in enumerate(tasks):
            make_prompts(scorer, k, i // 4, task)
    for k in args.depths:
        collect_k(scorer, k, tasks, args.dir / f"depth-{k}.jsonl")


if __name__ == "__main__":
    main()
