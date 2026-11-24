"""Run a single shared stream for each arm and seed."""

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from hashlib import blake2b
import json
from pathlib import Path
import time

from .agent import LocalModel, Scripted, episode
from .environment import retention_probes, stream
from .memory import ARMS
from .metrics import bootstrap_indices, curve, interval, run_metrics, table, with_deltas


def paired_seed(seed: int, phase: str, index: int) -> int:
    return int.from_bytes(blake2b(f"{seed}/{phase}/{index}".encode(), digest_size=4).digest(), "little") >> 1


def trial(agent, arm: str, seed: int, pre: int, post: int) -> list[dict]:
    memory = ARMS[arm]()
    tasks = stream(seed, pre, post)
    probes = retention_probes(seed)
    rows = []

    def collect(phase, inputs, migrated, learn):
        for i, task in enumerate(inputs):
            attempted, outcome, first_feedback, attempts = episode(
                agent, memory, task, paired_seed(seed, phase if learn else "probe", i), migrated, learn)
            rows.append({"arm": arm, "seed": seed, "phase": phase, "step": task.step if learn else i,
                         "family": task.family, "goal": task.goal, "entity": task.entity,
                         "coached": bool(task.coaching), "success": outcome.success,
                         "attempted": attempted, "feedback": outcome.feedback,
                         "action_attempts": attempts, "first_feedback": first_feedback})

    collect("pre", tasks[:pre], False, True)
    collect("probe-before", probes, False, False)
    collect("post", tasks[pre:], True, True)
    collect("probe-after", probes, True, False)
    return rows


def write_json(path: Path, data: dict, compact: bool = False) -> None:
    kwargs = {"separators": (",", ":")} if compact else {"indent": 2}
    path.write_text(json.dumps(data, **kwargs) + "\n")


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["scripted", "llm"], default="scripted")
    parser.add_argument("--url", default="http://127.0.0.1:8085/v1")
    parser.add_argument("--model", default="qwen2.5-1.5b-instruct-q4_k_m.gguf")
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 23, 37, 53, 71])
    parser.add_argument("--arms", nargs="+", choices=ARMS, default=list(ARMS))
    parser.add_argument("--pre", type=int, default=48)
    parser.add_argument("--post", type=int, default=48)
    parser.add_argument("--recovery-window", type=int, default=4)
    parser.add_argument("--draws", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if "no-memory" not in args.arms:
        parser.error("--arms must include no-memory for paired comparisons")
    if len(set(args.arms)) != len(args.arms) or len(set(args.seeds)) != len(args.seeds):
        parser.error("arms and seeds must be unique")
    if not 1 <= args.recovery_window <= min(args.pre // 4, args.post // 2):
        parser.error("recovery window must fit drifted-family tasks on both sides")
    if args.draws < 1 or args.workers < 1:
        parser.error("draws and workers must be positive")
    try:
        stream(args.seeds[0], args.pre, args.post)
    except ValueError as exc:
        parser.error(str(exc))
    args.output.mkdir(parents=True, exist_ok=True)
    agent = Scripted() if args.agent == "scripted" else LocalModel(args.url, args.model)
    all_rows = {arm: {} for arm in args.arms}
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(trial, agent, arm, seed, args.pre, args.post): (arm, seed)
                for arm in args.arms for seed in args.seeds}
        for job in as_completed(jobs):
            arm, seed = jobs[job]
            all_rows[arm][seed] = job.result()
            print(f"{arm} seed={seed} finished at {time.monotonic() - started:.0f}s", flush=True)

    raw = [r for arm in all_rows.values() for seed in sorted(arm) for r in arm[seed]]
    with (args.output / "episodes.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)

    metrics = {arm: {seed: run_metrics(rows, args.recovery_window) for seed, rows in seeds.items()}
               for arm, seeds in all_rows.items()}
    paired = {arm: with_deltas(seeds, metrics["no-memory"]) for arm, seeds in metrics.items()}
    indices = bootstrap_indices(len(args.seeds), args.draws)
    summary = {arm: {metric: interval([by_seed[s][metric] for s in sorted(by_seed)], indices)
                     for metric in by_seed[args.seeds[0]]} for arm, by_seed in paired.items()}
    online = {arm: {seed: [r for r in rows if r["phase"] in {"pre", "post"}] for seed, rows in seeds.items()}
              for arm, seeds in all_rows.items()}
    curves = {arm: curve(seeds, online["no-memory"], indices) for arm, seeds in online.items()}
    config = {k: v for k, v in vars(args).items() if k not in {"url", "output"}}
    write_json(args.output / "results.json", {"config": config, "wall_seconds": round(time.monotonic() - started, 1),
                                              "seeds": paired, "summary": summary})
    write_json(args.output / "curves.json", curves, compact=True)
    report = table(summary)
    (args.output / "summary.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
