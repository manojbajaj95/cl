"""Summarize each arm and bootstrap paired contrasts within target × quantity."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from math import sqrt
from pathlib import Path

import numpy as np

from pilot import ARMS, MASK_THRESHOLD, WRITERS, read_rows


def wilson(values):
    n = len(values)
    count = int(sum(values))
    rate = count / n
    z = 1.959963984540054
    denom = 1 + z**2 / n
    center = (rate + z**2 / (2 * n)) / denom
    margin = z * sqrt(rate * (1 - rate) / n + z**2 / (4 * n**2)) / denom
    return {"count": count, "n": n, "rate": rate,
            "ci95": [max(0.0, center - margin), min(1.0, center + margin)]}


def bootstrap_indices(rows, draws=10_000):
    strata = defaultdict(list)
    for i, row in enumerate(rows):
        strata[(*row["target"], row["qty"])].append(i)
    rng = np.random.default_rng(20261124)
    return np.concatenate([rng.choice(indices, size=(draws, len(indices)))
                           for indices in strata.values()], axis=1)


def paired(values, samples):
    return {"difference": float(values.mean()),
            "ci95": np.quantile(values[samples].mean(axis=1), [0.025, 0.975]).tolist()}


def summarize(rows, phase):
    n = len(rows)
    if n < 200 or len({row["id"] for row in rows}) != n:
        raise ValueError("Expected at least 200 distinct paired episodes")
    for row in rows:
        d = row["arms"]["distractor"]
        f = row["arms"]["filler"]
        if d["actor_input_tokens"] != f["actor_input_tokens"]:
            raise ValueError(f"Actor filler budget mismatch: {row['id']}")
        if phase == "writers" and d["writes"]["instruction"]["input_tokens"] != d["writes"]["baseline"]["input_tokens"]:
            raise ValueError(f"Writer instruction budget mismatch: {row['id']}")
    samples = bootstrap_indices(rows)
    solved = {a: np.array([row["arms"][a]["solved"] for row in rows], dtype=int) for a in ARMS}
    bad = {a: np.array([row["arms"][a]["writes"]["baseline"]["bad"] for row in rows], dtype=int)
           for a in ARMS}
    gaps = {a: bad[a] - (1 - solved[a]) for a in ARMS}
    summary = {"n_paired": n, "model_sha256": rows[0]["model_sha256"],
               "arms": {a: {"solve": wilson(solved[a]), "bad_write": wilson(bad[a])} for a in ARMS},
               "arm_contrasts": {}}
    for arm, control in (("distractor", "clean"), ("filler", "clean"), ("distractor", "filler")):
        summary["arm_contrasts"][f"{arm}_minus_{control}"] = {
            "bad_write": paired(bad[arm] - bad[control], samples),
            "solve_failure": paired(solved[control] - solved[arm], samples),
            "write_minus_failure_gap": paired(gaps[arm] - gaps[control], samples),
        }
    if phase == "writers":
        distractor = [row["arms"]["distractor"] for row in rows]
        writes = {v: np.array([d["writes"][v]["bad"] for d in distractor], dtype=int) for v in WRITERS}
        summary["writers"] = {
            v: {"bad_write": wilson(writes[v]), "mean_input_tokens": float(np.mean(
                [d["writes"][v]["input_tokens"] for d in distractor]))} for v in WRITERS
        }
        summary["writer_contrasts"] = {f"mask_minus_{v}": paired(writes["mask"] - writes[v], samples)
                                       for v in WRITERS if v != "mask"}
        summary["mask"] = {
            "threshold_nats": MASK_THRESHOLD,
            "mean_retained_lessons": float(np.mean(
                [sum(s >= MASK_THRESHOLD for s in d["mask_scores"]) for d in distractor])),
            "swapped_distractor_retained_count": sum(
                d["mask_scores"][row["swap_idx"]] >= MASK_THRESHOLD for d, row in zip(distractor, rows)),
        }
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rows", type=Path)
    parser.add_argument("--phase", choices=("baseline", "writers"), default="writers")
    args = parser.parse_args()
    print(json.dumps(summarize(read_rows(args.rows), args.phase), indent=2))
