"""Summarize exposure, budgets and paired block-level uncertainty."""

import argparse
import json
import math
from pathlib import Path
from statistics import mean, stdev

from scipy.stats import t

from benchmark import BLOCKS, SIZES
from pilot import MODES, TEMPERATURE_CONTROL, VARIANTS, summarize


def interval(values):
    avg = mean(values)
    half = t.ppf(0.975, len(values) - 1) * stdev(values) / math.sqrt(len(values))
    return {"mean": avg, "lo": float(avg - half), "hi": float(avg + half)}


def prospective_confidence(block, n, stress):
    # Both possible outcomes were scored for every task: no memory or always-push.
    k = block["methods"][f"{n}/{int(stress)}/failure"]["queries"]
    traces = block["traces"]
    selected = set(sorted(range(len(traces)), key=lambda i: (traces[i]["confidence"], i))[:k])
    push = f"{n}/{int(stress)}/push_always"
    cells = summarize([trace["trials"][push if i in selected else "none"]
                       for i, trace in enumerate(traces)])
    cells["calls"] += k
    cells["input_tokens"] += sum(traces[i]["first_tokens"] for i in selected)
    return cells


def analyze(raw):
    blocks = raw["blocks"]
    calibration = raw.get("calibration")
    low, high = SIZES[0], SIZES[-1]
    variants = VARIANTS if calibration is None else [(high, True)]
    assert tuple(b["seed"] for b in blocks) == BLOCKS
    metrics = [
        {**b["methods"], **{f"{n}/{int(stress)}/confidence_prospective": prospective_confidence(b, n, stress)
                           for n, stress in variants}}
        for b in blocks
    ]
    keys = list(metrics[0])
    stress_keys = {(n, mode): f"{n}/1/{mode}" for n in SIZES for mode in MODES}
    for cells in metrics:
        for n, stress in variants:
            active = [cells[f"{n}/{int(stress)}/{mode}"]
                      for mode in (*MODES, "confidence_prospective") if mode != "push_always"]
            assert len({row["queries"] for row in active}) == 1
            assert len({row["memory_tokens"] for row in active}) == 1
        for key, row in cells.items():
            assert row["first_won"] <= row["won"] <= row["n"]
            probes = row["queries"] if key.endswith("/confidence_prospective") else 0
            assert row["calls"] == 2 * row["n"] - row["first_won"] + probes
            assert row["corrupt_hit"] <= row["queries"]
    accuracy = {key: [100 * cells[key]["won"] / cells[key]["n"] for cells in metrics] for key in keys}
    rows = {}
    for key in keys:
        total = {metric: sum(cells[key][metric] for cells in metrics) for metric in metrics[0][key]}
        n, q = total["n"], total["queries"]
        rows[key] = {
            "accuracy_percent": interval(accuracy[key]),
            "first_accuracy_percent": interval([100 * m[key]["first_won"] / m[key]["n"] for m in metrics]),
            "query_rate_percent": 100 * q / n,
            "corrupt_atoms_per_task": total["corrupt"] / n,
            "corrupt_atoms_per_query": total["corrupt"] / q if q else None,
            "corrupt_hit_rate_percent": 100 * total["corrupt_hit"] / n,
            "calls_per_task": total["calls"] / n,
            "input_tokens_per_task": total["input_tokens"] / n,
            "memory_tokens_per_task": total["memory_tokens"] / n,
        }

    def vector(n, mode):
        return accuracy[stress_keys[n, mode]]

    def diff(a, b):
        return [x - y for x, y in zip(a, b)]

    failure_key = stress_keys[high, "failure"]
    push_key = stress_keys[high, "push_matched"]
    corrupt_delta = [
        (cells[failure_key]["corrupt"] - cells[push_key]["corrupt"]) / cells["none"]["n"]
        for cells in metrics
    ]
    contrasts = {
        "failure_minus_confidence_at_largest": interval(diff(vector(high, "failure"), vector(high, "confidence"))),
        "failure_minus_confidence_prospective_at_largest": interval(
            diff(vector(high, "failure"), accuracy[f"{high}/1/confidence_prospective"])
        ),
        "failure_minus_push_matched_at_largest": interval(diff(vector(high, "failure"), vector(high, "push_matched"))),
        "failure_minus_no_memory_at_largest": interval(diff(vector(high, "failure"), accuracy["none"])),
    }
    if calibration is not None:
        for mode in (*MODES, "confidence_prospective", "none"):
            key = "none" if mode == "none" else f"{high}/1/{mode}"
            contrasts[f"{mode}_minus_entropy_matched_at_largest"] = interval(
                diff(accuracy[key], accuracy[TEMPERATURE_CONTROL])
            )
    else:
        deltas = {mode: diff(vector(high, mode), vector(low, mode)) for mode in MODES}
        contrasts.update({
            **{f"stress_change_{mode}": interval(v) for mode, v in deltas.items()},
            "change_interaction_failure_minus_push_matched":
                interval(diff(deltas["failure"], deltas["push_matched"])),
            **{f"stress_minus_clean_at_largest_{mode}":
               interval(diff(vector(high, mode), accuracy[f"{high}/0/{mode}"])) for mode in MODES},
        })
    against_conf = contrasts["failure_minus_confidence_at_largest"]
    gates = {} if calibration is not None else {
        "always_push_declines": contrasts["stress_change_push_always"]["hi"] < 0,
        "matched_push_declines": contrasts["stress_change_push_matched"]["hi"] < 0,
        "failure_declines_less": contrasts["change_interaction_failure_minus_push_matched"]["lo"] > 0,
        "failure_retains": contrasts["stress_change_failure"]["lo"] > -5,
        "failure_beats_confidence": against_conf["mean"] >= 5 and against_conf["lo"] > 0,
    }
    retry_entropies = [trace["retry_entropy_nats"] for b in blocks for trace in b["traces"]
                       if "retry_entropy_nats" in trace]
    return {
        "wall_seconds": raw["wall_seconds"],
        "calibration": calibration,
        "held_out_retry_entropy_nats": {key: mean(row[key] for row in retry_entropies)
                                       for key in retry_entropies[0]} if retry_entropies else None,
        "held_out_tasks": sum(cells["none"]["n"] for cells in metrics),
        "blocks": [{**{k: v for k, v in b.items() if k not in {"traces", "methods"}}, "methods": cells}
                   for b, cells in zip(blocks, metrics)],
        "metrics": rows,
        "paired_contrasts_pp": contrasts,
        "failure_minus_push_matched_corrupt_atoms_per_task_at_largest": interval(corrupt_delta),
        "gates": gates,
        "confidence_equivalent_within_5pp": against_conf["lo"] > -5 and against_conf["hi"] < 5,
        "decision": None if calibration is not None else ("KEEP" if all(gates.values()) else "KILL"),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(analyze(json.loads(args.trials.read_text())), indent=2) + "\n")
