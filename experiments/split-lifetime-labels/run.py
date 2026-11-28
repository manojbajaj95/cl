import argparse
import json
import platform
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy
from scipy.stats import t


SIZE = 24
HORIZON = 5
BASE = (1, 3, -2)
CANDIDATES = (*BASE, 25)
RELEASES = {"A": 6, "B": -5}
BUDGETS = [48, 96, 192, 384]
ARMS = ("split", "whole", "pav", "carry")
SEEDS = range(32)
ROWS = [(x, m) for x in range(SIZE) for m in CANDIDATES]


def legal(x):
    return 0 <= x < SIZE


def old_tables(goal):
    can = [[x == goal for x in range(SIZE)]]
    source_masks = [[0] * SIZE]
    for _ in range(HORIZON):
        prev = can[-1]
        prev_masks = source_masks[-1]
        can.append([
            x == goal or any(prev[x + d] for d in BASE if legal(x + d))
            for x in range(SIZE)
        ])
        masks = []
        for x in range(SIZE):
            mask = 1 << (x % 3)
            for d in BASE:
                if legal(x + d):
                    mask |= prev_masks[x + d]
            masks.append(mask)
        source_masks.append(masks)
    return can, source_masks


def label_from(can, row):
    x, d = row
    y = x + d
    return (True, int(can(HORIZON - 1, y)) - int(can(HORIZON, x))) if legal(y) else (False, None)


def compile_rows(can, masks):
    labels = [label_from(lambda h, x: can[h][x], row) for row in ROWS]
    guards = []
    for x, d in ROWS:
        y = x + d
        guard = 0
        if legal(y):
            if not can[HORIZON - 1][y]:
                guard |= masks[HORIZON - 1][y]
            if not can[HORIZON][x]:
                guard |= masks[HORIZON][x]
        guards.append(guard)
    return labels, bytes(guards)


def truth(goal, residue, move):
    def forward(h, x):
        reached = {x}
        for _ in range(h):
            reached |= {
                y
                for s in reached
                for y in range(SIZE)
                if y - s in BASE or (move is not None and s % 3 == residue and y - s == move)
            }
        return goal in reached

    values = {(h, x): forward(h, x) for h in (HORIZON - 1, HORIZON) for x in range(SIZE)}
    return [
        (True, int(values[HORIZON - 1, x + d]) - int(values[HORIZON, x]))
        if 0 <= x + d < SIZE else (False, None)
        for x, d in ROWS
    ]


class Exhausted(Exception):
    pass


@dataclass
class Budget:
    cap: None | int
    calls: Counter

    def charge(self, kind):
        if self.cap is not None and self.calls.total() >= self.cap:
            raise Exhausted
        self.calls[kind] += 1


def refresh(can, labels, guards, order, residue, move, arm, cap):
    budget = Budget(cap, Counter())
    out = labels.copy()
    if arm == "carry" or move is None:
        return out, budget.calls
    memo = {}

    def value(h, x):
        if not h or can[h][x]:
            return can[h][x]
        key = h, x
        if key not in memo:
            moves = (*BASE, move) if x % 3 == residue else BASE
            for d in moves:
                budget.charge("continuation")
                if legal(x + d) and value(h - 1, x + d):
                    memo[key] = True
                    break
            else:
                memo[key] = False
        return memo[key]

    try:
        for i in order:
            if not labels[i][0]:
                continue
            if arm in ("split", "whole"):
                budget.charge("guard")
                if not guards[i] & (1 << residue):
                    continue
            x, d = ROWS[i]
            y = x + d
            if arm == "whole":
                budget.charge("validity")
                assert legal(y)
            out[i] = True, int(value(HORIZON - 1, y)) - int(value(HORIZON, x))
    except Exhausted:
        pass
    return out, budget.calls


def weak_orders(labels):
    orders = []
    for offset in range(0, len(labels), len(CANDIDATES)):
        p = [v for valid, v in labels[offset:offset + len(CANDIDATES)] if valid]
        orders.append(tuple((a > b) - (a < b) for i, a in enumerate(p) for b in p[i + 1:]))
    return tuple(orders)


def blank_stats():
    return {
        "correct": 0, "rows": 0, "retained": 0, "old_rows": 0,
        "retained_invalid": 0, "invalid": 0, "retained_detours": 0, "detours": 0,
        "retained_orders": 0, "orders": 0, "operations": 0, "guards": 0,
        "validity": 0, "continuation": 0, "refresh_seconds": 0.0,
    }


def observe(stats, out, exact, calls, seconds, upgraded, exact_orders):
    if upgraded:
        stats["correct"] += sum(a == b for a, b in zip(out, exact, strict=True))
        stats["rows"] += len(out)
    else:
        stats["retained"] += sum(a == b for a, b in zip(out, exact, strict=True))
        stats["old_rows"] += len(out)
        stats["detours"] += sum(b[0] and b[1] < 0 for b in exact)
        stats["retained_detours"] += sum(
            b[0] and b[1] < 0 and a == b for a, b in zip(out, exact, strict=True)
        )
        stats["retained_orders"] += sum(
            a == b for a, b in zip(weak_orders(out), exact_orders, strict=True)
        )
        stats["orders"] += len(exact_orders)
    stats["invalid"] += sum(not b[0] for b in exact)
    stats["retained_invalid"] += sum(not b[0] and a == b for a, b in zip(out, exact, strict=True))
    stats["operations"] += calls.total()
    stats["guards"] += calls["guard"]
    stats["validity"] += calls["validity"]
    stats["continuation"] += calls["continuation"]
    stats["refresh_seconds"] += seconds


def stream(seed, move):
    rng = np.random.Generator(np.random.PCG64(seed))
    stats = {arm: {cap: blank_stats() for cap in BUDGETS} for arm in ARMS}
    diagnostics = Counter()
    for board in range(16):
        goal = int(rng.integers(SIZE))
        residue = int(rng.integers(3))
        order = rng.permutation(len(ROWS)).tolist()
        upgraded = board < 12
        new_move = move if upgraded else None
        can, masks = old_tables(goal)
        base, guards = compile_rows(can, masks)
        exact = truth(goal, residue, new_move)
        exact_orders = None if upgraded else weak_orders(exact)
        if upgraded:
            for i, (old, new) in enumerate(zip(base, exact, strict=True)):
                flagged = bool(guards[i] & (1 << residue))
                diagnostics["changed"] += old != new
                diagnostics["flagged"] += flagged
                diagnostics["flagged_changed"] += flagged and old != new
        for arm in ARMS:
            if arm != "carry":
                full, _ = refresh(can, base, guards, order, residue, new_move, arm, None)
                assert full == exact, (seed, board, move, arm)
                diagnostics["unrestricted_exact"] += 1
            for cap in BUDGETS:
                start = perf_counter()
                out, calls = refresh(can, base, guards, order, residue, new_move, arm, cap)
                observe(
                    stats[arm][cap], out, exact, calls, perf_counter() - start, upgraded, exact_orders
                )
    return {"seed": seed, "metrics": stats, "diagnostics": dict(diagnostics)}


def interval(values, level):
    a = np.asarray(values)
    mean = float(a.mean())
    radius = float(t.ppf((1 + level) / 2, len(a) - 1) * a.std(ddof=1) / np.sqrt(len(a)))
    return [mean, mean - radius, mean + radius]


def summarize(streams):
    metrics = {}
    for cap in BUDGETS:
        arm_metrics = {arm: [s["metrics"][arm][cap] for s in streams] for arm in ARMS}
        accuracy = {
            arm: np.array([100 * s["correct"] / s["rows"] for s in results])
            for arm, results in arm_metrics.items()
        }
        metrics[cap] = {
            "accuracy_pp": {arm: interval(a, 0.95) for arm, a in accuracy.items()},
            "split_deltas_pp": {
                arm: interval(
                    accuracy["split"] - a, 0.975 if cap == 96 and arm != "carry" else 0.95
                )
                for arm, a in accuracy.items() if arm != "split"
            },
            "mean_per_upgraded_board": {
                arm: {k: float(np.mean([s[k] for s in a]) / 12) for k in
                      ("operations", "guards", "validity", "continuation")}
                for arm, a in arm_metrics.items()
            },
            "retention_counts": {
                arm: {k: sum(s[k] for s in a) for k in (
                    "retained", "old_rows", "retained_invalid", "invalid", "retained_detours",
                    "detours", "retained_orders", "orders"
                )} for arm, a in arm_metrics.items()
            },
        }
    diagnostics = Counter()
    for s in streams:
        diagnostics.update(s["diagnostics"])
    return {"by_cap": metrics, "diagnostics": dict(diagnostics)}


def decide(result_a):
    m = result_a["by_cap"][96]
    controls = [m["split_deltas_pp"][k] for k in ("whole", "pav")]
    for retention in m["retention_counts"].values():
        for count, total in (("retained", "old_rows"), ("retained_invalid", "invalid"),
                             ("retained_detours", "detours"), ("retained_orders", "orders")):
            if retention[count] != retention[total]:
                return "retention failure"
    if 100 - m["accuracy_pp"]["carry"][0] < 1:
        return "no assay signal"
    if any(hi < 2 for _, _, hi in controls):
        return "kill"
    if all(lo > 2 for _, lo, _ in controls):
        return "promote"
    return "inconclusive"


def main():
    parser = argparse.ArgumentParser(description="Run the fixed CV16 pilot.")
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    start = perf_counter()
    streams = {k: [stream(seed, move) for seed in SEEDS] for k, move in RELEASES.items()}
    summary = {k: summarize(results) for k, results in streams.items()}
    decision = decide(summary["A"])
    result = {
        "protocol_commit": "e95e61a",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "elapsed_seconds": perf_counter() - start,
        "decision": decision,
        "summary": summary,
        "streams": streams,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"CV16 decision: {decision} ({result['elapsed_seconds']:.2f} s)")
    for release, data in summary.items():
        primary = data["by_cap"][96]
        print(f"{release}, 96 operations/board:", primary["accuracy_pp"])
        print("Paired split deltas (pp):", primary["split_deltas_pp"])
        print("Oracle and guard checks:", data["diagnostics"])
        print("Split retention:", primary["retention_counts"]["split"])


if __name__ == "__main__":
    main()
