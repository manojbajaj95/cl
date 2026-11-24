import argparse
import json
from pathlib import Path

import numpy as np


def format_ci(values, samples, precision=4, scale=1):
    values = np.asarray(values) * scale
    low, high = np.quantile(values[samples].mean(axis=1), (0.025, 0.975))
    return f"{values.mean():.{precision}f} [{low:.{precision}f}, {high:.{precision}f}]"


def summarize(rows):
    seeds = [row["seed"] for row in rows]
    assert len(set(seeds)) == len(seeds) and len(seeds) >= 3
    samples = np.random.default_rng(797).integers(len(rows), size=(10000, len(rows)))
    versions = [row["versions"] for row in rows]
    count = len(versions[0])

    def old(arm, metric):
        return np.array([[v[arm][metric] for v in seed[:-1]] for seed in versions])

    reference_accuracy = np.array([[v["checkpoint_accuracy"] for v in seed[:-1]] for seed in versions])
    print("Old versions (v1–v4), averaged within seed; KL in nats, accuracy in %")
    print("| Reader | Held-out KL | Probe KL | Held-out reverse KL | Task accuracy |")
    print("|---|---:|---:|---:|---:|")
    print(f"| Exact checkpoint | 0 | 0 | 0 | {format_ci(reference_accuracy.mean(1), samples, 2, 100)} |")
    for arm in ("tagged", "replay", "shuffled", "stored", "wrong_tag", "frozen"):
        metrics = [format_ci(old(arm, metric).mean(1), samples)
                   for metric in ("heldout_kl", "probe_kl", "heldout_reverse_kl")]
        metrics += [format_ci(old(arm, "accuracy").mean(1), samples, 2, 100)]
        print(f"| {arm} | {' | '.join(metrics)} |")
    tagged = old("tagged", "heldout_kl")
    replay = old("replay", "heldout_kl")
    delta = (tagged - replay).mean(1)
    for arm in ("replay", "shuffled", "stored", "wrong_tag", "frozen"):
        print(f"Held-out tagged minus {arm}: "
              f"{format_ci((tagged - old(arm, 'heldout_kl')).mean(1), samples)}")
    print(f"Probe tagged minus replay: "
          f"{format_ci((old('tagged', 'probe_kl') - old('replay', 'probe_kl')).mean(1), samples)}")
    ratio_samples = tagged.mean(1)[samples].mean(1) / replay.mean(1)[samples].mean(1)
    ratio_low, ratio_high = np.quantile(ratio_samples, (0.025, 0.975))
    print(f"Held-out tagged/replay ratio: {tagged.mean() / replay.mean():.1%} "
          f"[{ratio_low:.1%}, {ratio_high:.1%}]")
    print()
    print("| Past tag | Tagged held-out KL | Replay held-out KL | Tagged accuracy (%) | Checkpoint accuracy (%) |")
    print("|---|---:|---:|---:|---:|")
    accuracy = old("tagged", "accuracy")
    for j in range(count - 1):
        print(f"| v{j + 1} | {format_ci(tagged[:, j], samples)} | {format_ci(replay[:, j], samples)} | "
              f"{format_ci(accuracy[:, j], samples, 2, 100)} | "
              f"{format_ci(reference_accuracy[:, j], samples, 2, 100)} |")
    print()
    print("| Current tag | Tagged accuracy (%) | Replay accuracy (%) | Tagged − replay (pp) |")
    print("|---|---:|---:|---:|")
    retention = [row["retention"] for row in rows]
    tag_acc, replay_acc = (np.array([r[arm]["accuracy"] for r in retention]) for arm in ("tagged", "replay"))
    for j in range(count):
        print(f"| Task {j + 1} | {format_ci(tag_acc[:, j], samples, 2, 100)} | "
              f"{format_ci(replay_acc[:, j], samples, 2, 100)} | "
              f"{format_ci(tag_acc[:, j] - replay_acc[:, j], samples, 2, 100)} |")
    tag_ppl, replay_ppl = (np.array([r[arm]["ppl"] for r in retention]) for arm in ("tagged", "replay"))
    ppl_delta = (tag_ppl / replay_ppl - 1)
    print(f"WikiText-2 PPL: tagged {format_ci(tag_ppl, samples)}, replay {format_ci(replay_ppl, samples)}, "
          f"paired relative change {format_ci(ppl_delta, samples, 2, 100)}%.")
    print(f"Frozen PPL: {rows[0]['frozen_ppl']}")
    print()
    print(f"Reviewer KL gate: {'PASS' if np.quantile(delta[samples].mean(1), .975) < 0 else 'FAIL'}")
    print(f"Source card half-KL gate: {'PASS' if tagged.mean() < replay.mean() / 2 else 'FAIL'}")
    print(f"Source card past accuracy gate: "
          f"{'PASS' if np.all(accuracy.mean(0) >= .8 * reference_accuracy.mean(0)) else 'FAIL'}")
    print(f"Current-tag accuracy gate (all five): "
          f"{'PASS' if np.all(np.abs((tag_acc - replay_acc).mean(0)) <= .01) else 'FAIL'}")
    print(f"Current-tag PPL gate: {'PASS' if abs(ppl_delta.mean()) <= .02 else 'FAIL'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", type=Path)
    args = parser.parse_args()
    with args.runs.open() as run_file:
        rows = [json.loads(line) for line in run_file]
    summarize([row for row in rows if "seed" in row])
