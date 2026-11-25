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
    uncoached_entropies = [r["token_entropy"] for r in pre + post if not r["coached"]
                          and r.get("token_entropy") is not None]
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
        **({"uncoached_token_entropy": mean(uncoached_entropies)} if uncoached_entropies else {}),
    }


def bootstrap_indices(n: int, draws: int) -> list[list[int]]:
    rng = Random(303)
    return [[rng.randrange(n) for _ in range(n)] for _ in range(draws)]


def interval(values: list[float], indices: list[list[int]]) -> dict:
    draws = sorted(mean(values[i] for i in sample) for sample in indices)
    return {"mean": mean(values), "low": draws[int(0.025 * (len(draws) - 1))],
            "high": draws[int(0.975 * (len(draws) - 1))]}


def with_deltas(by_seed: dict[int, dict], baseline: dict[int, dict],
                matched: dict[int, dict] | None = None) -> dict[int, dict]:
    deltas = {}
    for seed, metrics in by_seed.items():
        row = dict(metrics)
        for suffix, control in (("", baseline), ("_entropy", matched)):
            if control is not None:
                row[f"success_gain{suffix}"] = metrics["success"] - control[seed]["success"]
                row[f"cumulative_gain{suffix}"] = metrics["cumulative_success"] - control[seed]["cumulative_success"]
        deltas[seed] = row
    return deltas


def curve(rows: dict[int, list[dict]], baseline: dict[int, list[dict]],
          indices: list[list[int]], matched: dict[int, list[dict]] | None = None) -> list[dict]:
    seeds = sorted(rows)
    current = [0] * len(seeds)
    control = [0] * len(seeds)
    entropy_control = [0] * len(seeds)
    result = []
    for step, (left, right) in enumerate(zip(zip(*(rows[s] for s in seeds)),
                                           zip(*(baseline[s] for s in seeds))), 1):
        online = [int(a["success"]) for a in left]
        online_gain = [x - int(r["success"]) for x, r in zip(online, right)]
        current = [x + y for x, y in zip(current, online)]
        control = [x + int(r["success"]) for x, r in zip(control, right)]
        point = {"step": step,
                 "online_success": interval(online, indices),
                 "online_gain": interval(online_gain, indices),
                 "cumulative_success": interval(current, indices),
                 "cumulative_gain": interval([x - y for x, y in zip(current, control)], indices)}
        if matched is not None:
            reference = [int(matched[s][step - 1]["success"]) for s in seeds]
            entropy_control = [x + y for x, y in zip(entropy_control, reference)]
            point["online_gain_entropy"] = interval([x - y for x, y in zip(online, reference)], indices)
            point["cumulative_gain_entropy"] = interval([x - y for x, y in zip(current, entropy_control)], indices)
        result.append(point)
    return result


def table(summary: dict) -> str:
    columns = [("Success %", "success", 100), ("Gain vs plain pp", "success_gain", 100),
               ("Post AUC %", "post_auc", 100), ("Drifted AUC %", "affected_post_auc", 100),
               ("Old before %", "retention_before", 100), ("Old after %", "retention_after", 100),
               ("Forgetting pp", "forgetting", 100), ("Recovery steps†", "recovery_restricted_steps", 1),
               ("Recovered %", "recovered", 100)]
    if "success_gain_entropy" in next(iter(summary.values())):
        columns.insert(2, ("Gain vs entropy-matched pp", "success_gain_entropy", 100))
    lines = ["| Arm | " + " | ".join(title for title, _, _ in columns) + " |",
             "| " + " | ".join(["---"] * (len(columns) + 1)) + " |"]
    for arm, metrics in summary.items():
        cells = []
        for _, key, scale in columns:
            m = metrics[key]
            cells.append(f'{m["mean"] * scale:.1f} [{m["low"] * scale:.1f}, {m["high"] * scale:.1f}]')
        lines.append("| " + " | ".join([arm, *cells]) + " |")
    return "\n".join(lines) + "\n"
