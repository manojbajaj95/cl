"""Fit a no-memory retry temperature using source ALFWorld tasks only."""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from benchmark import SIZES
from pilot import ChoiceModel, embedding, entropy, note, rescale, retrieve


def fit(samples):
    weight = sum(w for w, _, _ in samples)
    target = sum(w * entropy(lesson) for w, _, lesson in samples) / weight

    def unprompted(t):
        return sum(w * entropy(rescale(base, t)) for w, base, _ in samples) / weight

    lo, hi = 0.05, 20.0
    if not unprompted(lo) <= target <= unprompted(hi):
        raise ValueError("source entropy target is outside the temperature search range")
    for _ in range(45):
        mid = (lo + hi) / 2
        if unprompted(mid) < target:
            lo = mid
        else:
            hi = mid
    temperature = (lo + hi) / 2
    return dict(temperature=temperature, memory_entropy_nats=target,
                neutral_entropy_nats=unprompted(1), matched_entropy_nats=unprompted(temperature))


def calibrate(cases, blocks, model, workers):
    assert len(cases) == 48 and len({c["id"] for c in cases}) == len(cases)
    indexed = {a["id"] for b in blocks for a in b["store"]}
    assert all(c["id"].startswith("train/") and c["id"] not in indexed for c in cases)
    vectors = [[embedding(a) for a in block["store"]] for block in blocks]

    def sample(entry):
        i, case = entry
        b = i % len(blocks)
        indices = retrieve(embedding(case), vectors[b], max(SIZES))
        memory = model.memory([note(blocks[b]["store"][j], True) for j in indices])
        cache = {}
        baseline, _ = model.score(case, None, model.neutral, cache)
        rows = []
        for action, outcome in enumerate(case["outcomes"]):
            if not outcome["won"] and outcome["feedback"] == "Nothing happens.":
                neutral, _ = model.score(case, action, model.neutral, cache)
                prompted, _ = model.score(case, action, memory, cache)
                rows.append((baseline[action], neutral, prompted))
        return rows

    with ThreadPoolExecutor(max_workers=workers) as pool:
        samples = [row for rows in pool.map(sample, enumerate(cases)) for row in rows]
    return {**fit(samples), "retry_states": len(samples), "source_ids": [c["id"] for c in cases]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("stores", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--server", default="http://127.0.0.1:8991")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--score-cache", type=Path, help="checkpoint prompt scores; reuse only with the same model")
    args = parser.parse_args()
    result = calibrate(json.loads(args.source.read_text()), json.loads(args.stores.read_text()),
                       ChoiceModel(args.server, args.score_cache), args.workers)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
