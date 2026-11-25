import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .backends import ResponseCache, backends
from .environment import CALIBRATION_START, HELD_OUT, SEEDS, TRAIN, make_task
from .pilot import accuracy


def main():
    parser = argparse.ArgumentParser(description="Grade the fixed solver on disjoint HW1 calibration tasks")
    parser.add_argument("--cache", required=True, type=Path)
    args = parser.parse_args()
    with ResponseCache(args.cache) as cache, ThreadPoolExecutor(max_workers=16) as pool:
        _, model, _, _ = backends("local", cache)
        for family in (*TRAIN, HELD_OUT):
            tasks = [make_task(family, i) for i in range(CALIBRATION_START, CALIBRATION_START + 24)]
            cases = [(task, SEEDS[i % len(SEEDS)], 0) for i, task in enumerate(tasks)]
            scores = accuracy(model, (), cases, pool)
            print(f"{family}: {int(scores.sum())}/{len(cases)} ({scores.mean():.1%})", flush=True)


if __name__ == "__main__":
    main()
