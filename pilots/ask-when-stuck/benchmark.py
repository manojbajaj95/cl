"""Prepare observed action/feedback branches from the official ALFWorld games."""

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


BLOCKS = (42, 43, 44, 45, 46)
SIZES = (12, 36, 90, 180)


def family(path):
    return path.parent.parent.name.split("-")[0]


def rng_for(path):
    return random.Random(int.from_bytes(hashlib.sha256(str(path).encode()).digest()[:8], "big"))


def decision(plan):
    for i, action in enumerate(plan):
        if action.split()[0] in {"clean", "cool", "heat", "use"}:
            return i
    return max(i for i, action in enumerate(plan) if action.startswith("move "))


def alternatives(ref, legal):
    invalid = []
    for match in re.finditer(r"\b\d+\b", ref):
        n = int(match.group(0))
        for m in (n + 1, max(1, n - 1), n + 2):
            candidate = ref[:match.start()] + str(m) + ref[match.end():]
            if candidate not in legal and candidate not in invalid:
                invalid.append(candidate)
    if len(invalid) < 2:
        raise ValueError((ref, legal))
    return [ref, "look", *invalid[:2]]


def benchmark_game(job):
    import textworld
    from alfworld.agents.environment.alfred_tw_env import AlfredDemangler

    root, relative, is_train = job
    path = root / relative
    game = json.loads(path.read_text())
    plan = game["walkthrough"]
    assert game["solvable"] and len(plan) <= 50, relative
    env = textworld.start(
        str(path),
        textworld.EnvInfos(won=True, admissible_commands=True),
        wrappers=[AlfredDemangler],
    )
    try:
        init = env.reset().feedback
        obs, goal = init.strip().split("Your task is to:", 1)
        item = {"id": str(relative), "goal": goal.strip(), "initial": obs.split("\n\n", 1)[-1][:500].strip()}
        idx = decision(plan)
        if is_train:
            for action in plan:
                state, _, _ = env.step(action)
            assert state.won, relative
            item["operation"] = plan[idx].split()[0]
            return item

        def to_checkpoint():
            state = env.reset()
            for action in plan[:idx]:
                state, _, done = env.step(action)
                assert not done, (relative, action)
            return state

        state = to_checkpoint()
        item["observation"] = state.feedback
        item["history"] = plan[:idx]
        assert plan[idx] in state.admissible_commands
        options = alternatives(plan[idx], state.admissible_commands)
        rng_for(relative).shuffle(options)
        outcomes = []
        for action in options:
            to_checkpoint()
            state, _, done = env.step(action)
            feedback = state.feedback
            for remaining in plan[idx + 1:]:
                if done:
                    break
                state, _, done = env.step(remaining)
            outcomes.append({"feedback": feedback, "won": bool(state.won)})
        assert [row["won"] for row in outcomes] == [a == plan[idx] for a in options], relative
        assert sum(row["feedback"] == "Nothing happens." for row in outcomes) == 2, relative
        item.update(options=options, outcomes=outcomes)
        return item
    finally:
        env.close()


def manifest(root):
    train = defaultdict(list)
    for path in sorted((root / "train").glob("*/*/game.tw-pddl")):
        train[family(path)].append(path.relative_to(root))
    assert len(train) == 6 and sum(map(len, train.values())) == 3553
    groups = defaultdict(list)
    for path in sorted((root / "valid_unseen").glob("*/*/game.tw-pddl")):
        groups[path.parent.parent.name].append(path.relative_to(root))
    assert sum(map(len, groups.values())) == 134
    held = {seed: [] for seed in BLOCKS}
    order = list(groups)
    random.Random(261027406).shuffle(order)
    for group in sorted(order, key=lambda g: -len(groups[g])):
        seed = min(held, key=lambda k: len(held[k]))
        held[seed].extend(groups[group])
    counts = [len(paths) for paths in held.values()]
    assert min(counts) > 0 and max(counts) - min(counts) <= max(map(len, groups.values()))
    for seed in BLOCKS:
        rng = random.Random(seed)
        by_type = [rng.sample(train[k], 30) for k in sorted(train)]
        balanced = []
        for items in zip(*by_type):
            items = list(items)
            rng.shuffle(items)
            balanced.extend(items)
        toxic = [i >= SIZES[0] and rng.random() < 0.5 for i in range(len(balanced))]
        yield seed, balanced, toxic, held[seed]


def prepare(root, output, workers):
    blocks = list(manifest(root))
    train_paths = sorted({path for _, paths, _, _ in blocks for path in paths})
    eval_paths = sorted(path for _, _, _, paths in blocks for path in paths)
    jobs = [(root, p, True) for p in train_paths] + [(root, p, False) for p in eval_paths]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        cases = {row["id"]: row for row in pool.map(benchmark_game, jobs, chunksize=4)}
    data = [
        {"seed": seed,
         "store": [dict(cases[str(p)], corrupt=bad) for p, bad in zip(train, toxic)],
         "heldout": [cases[str(p)] for p in held]}
        for seed, train, toxic, held in blocks
    ]
    output.write_text(json.dumps(data, separators=(",", ":")) + "\n")


def calibration_cases(root, blocks, workers):
    used = {atom["id"] for block in blocks for atom in block["store"]}
    eligible = defaultdict(list)
    for path in sorted((root / "train").glob("*/*/game.tw-pddl")):
        relative = path.relative_to(root)
        if str(relative) not in used:
            eligible[family(path)].append(relative)
    rng = random.Random(261027407)
    paths = [p for group in zip(*(rng.sample(eligible[k], 8) for k in sorted(eligible)))
             for p in group]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(benchmark_game, [(root, p, False) for p in paths], chunksize=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="path to extracted json_2.1.1 directory")
    parser.add_argument("output", type=Path)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--source-for", type=Path, help="generate calibration cases excluding these stores")
    args = parser.parse_args()
    if args.source_for:
        sources = calibration_cases(args.data, json.loads(args.source_for.read_text()), args.workers)
        args.output.write_text(json.dumps(sources, separators=(",", ":")) + "\n")
    else:
        prepare(args.data, args.output, args.workers)
