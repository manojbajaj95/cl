"""Paired seed-level summaries and online learning curves."""

from random import Random
from statistics import mean


def run_metrics(rows: list[dict], window: int) -> dict:
    pre = [r for r in rows if r["phase"] == "pre"]
    post = [r for r in rows if r["phase"] == "post"]
    affected_pre = [r["success"] for r in pre if r["family"] in (4, 5)]
    affected_post = [r["success"] for r in post if r["family"] in (4, 5)]
    target = mean(affected_pre[-window:])
    recovered = next((i for i in range(window, len(affected_post) + 1)
                      if mean(affected_post[i-window:i]) >= target), None)
    if recovered is not None:
        # Count all incoming tasks, not just affected-family tasks.
        post_index = [i for i, r in enumerate(post, 1) if r["family"] in (4, 5)]
        recovered = post_index[recovered - 1]
    early = mean(r["success"] for r in rows if r["phase"] == "probe-before")
    late = mean(r["success"] for r in rows if r["phase"] == "probe-after")
    return {
        "success": mean(r["success"] for r in pre + post),
        "uncoached_success": mean(r["success"] for r in pre + post if not r["coached"]),
        "cumulative_success": sum(r["success"] for r in pre + post),
        "pre_success": mean(r["success"] for r in pre),
        "post_auc": mean(r["success"] for r in post),
        "affected_post_auc": mean(affected_post),
        "retention_before": early,
        "retention_after": late,
        "forgetting": early - late,
        "recovery_target": target,
        "recovered": int(recovered is not None),
        "recovery_restricted_steps": recovered if recovered is not None else len(post) + 1,
    }


def bootstrap_indices(n: int, draws: int) -> list[list[int]]:
    rng = Random(303)
    return [[rng.randrange(n) for _ in range(n)] for _ in range(draws)]


def interval(values: list[float], indices: list[list[int]]) -> dict:
    draws = sorted(mean(values[i] for i in sample) for sample in indices)
    return {"mean": mean(values), "low": draws[int(0.025 * (len(draws) - 1))],
            "high": draws[int(0.975 * (len(draws) - 1))]}


def with_deltas(by_seed: dict[int, dict], baseline: dict[int, dict]) -> dict[int, dict]:
    return {seed: {**metrics,
                   "success_gain": metrics["success"] - baseline[seed]["success"],
                   "cumulative_gain": metrics["cumulative_success"] - baseline[seed]["cumulative_success"]}
            for seed, metrics in by_seed.items()}


def curve(rows: dict[int, list[dict]], baseline: dict[int, list[dict]],
          indices: list[list[int]]) -> list[dict]:
    seeds = sorted(rows)
    current = [0] * len(seeds)
    control = [0] * len(seeds)
    result = []
    for step, (left, right) in enumerate(zip(zip(*(rows[s] for s in seeds)),
                                           zip(*(baseline[s] for s in seeds))), 1):
        online = [int(a["success"]) for a in left]
        online_gain = [x - int(r["success"]) for x, r in zip(online, right)]
        current = [x + y for x, y in zip(current, online)]
        control = [x + int(r["success"]) for x, r in zip(control, right)]
        result.append({"step": step,
                       "online_success": interval(online, indices),
                       "online_gain": interval(online_gain, indices),
                       "cumulative_success": interval(current, indices),
                       "cumulative_gain": interval([x - y for x, y in zip(current, control)], indices)})
    return result


def table(summary: dict) -> str:
    columns = [("Success %", "success", 100), ("Gain pp", "success_gain", 100),
               ("Post AUC %", "post_auc", 100), ("Drifted AUC %", "affected_post_auc", 100),
               ("Old before %", "retention_before", 100), ("Old after %", "retention_after", 100),
               ("Forgetting pp", "forgetting", 100), ("Recovery steps†", "recovery_restricted_steps", 1),
               ("Recovered %", "recovered", 100)]
    lines = ["| Arm | " + " | ".join(title for title, _, _ in columns) + " |",
             "| " + " | ".join(["---"] * (len(columns) + 1)) + " |"]
    for arm, metrics in summary.items():
        cells = []
        for _, key, scale in columns:
            m = metrics[key]
            cells.append(f'{m["mean"] * scale:.1f} [{m["low"] * scale:.1f}, {m["high"] * scale:.1f}]')
        lines.append("| " + " | ".join([arm, *cells]) + " |")
    return "\n".join(lines) + "\n"
