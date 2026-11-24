"""A1 mechanism probe on the PR #12/#19 rare-event world.

Anomaly: natural-frequency MOPD replay leaves old-jam recovery *below* no replay.
Hypothesis (H-A1): the replayed old-common states share adapter features with the rare
old state but carry the opposite label, and the new task contains a state (Y busy -> D)
whose gradient incidentally protects X jam. Natural replay of X busy cancels that
protection. This script splits MOPD replay by old status and masks the protecting new
state, at 10+ paired seeds, reusing the PR #19 pilot unchanged.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import t

sys.path.insert(0, str(Path(__file__).parent))
import pilot_pr19 as P  # noqa: E402

ARMS = ("none", "mopd", "mopd_normal", "mopd_busy", "none_mask_ybusy", "mopd_mask_ybusy",
        "mopd_busy_anchor_jam")


def adapt(previous, new_batches, replay, arm, seed):
    policy = P.copy.deepcopy(previous)
    opt = torch.optim.AdamW(policy.parameters(), lr=0.006, weight_decay=0.0)
    rng = np.random.default_rng(seed)
    for starts_new, _, status_new in new_batches:
        opt.zero_grad()
        logits = policy.logits(1, starts_new, status_new)
        per = F.binary_cross_entropy_with_logits(logits, P.labels(1, status_new), reduction="none")
        if "mask_ybusy" in arm:
            keep = torch.from_numpy(status_new != P.BUSY).float()
            loss = (per * keep).sum() / len(per)
        else:
            loss = per.mean()
        if arm.startswith("mopd"):
            starts, _, status = P.natural(rng, P.REPLAY_BATCH, replay.route)
            if arm == "mopd_normal":
                status = np.full_like(status, P.NORMAL)
            elif arm == "mopd_busy":
                status = np.full_like(status, P.BUSY)
            elif arm == "mopd_busy_anchor_jam":
                status = np.where(np.arange(len(status)) % 2 == 0, P.BUSY, P.JAM)
            student = policy.logits(0, starts, status)
            with torch.no_grad():
                target = previous.logits(0, starts, status)
            loss = loss + P.REPLAY_SCALE * P.reverse_kl(student, target).mean()
        loss.backward()
        opt.step()
    return policy


def interval(values):
    d = np.asarray(values, float)
    h = float(t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / math.sqrt(len(d)))
    return [float(d.mean()), float(d.mean() - h), float(d.mean() + h)]


def feature_geometry(features):
    z = features["z"]  # domain, prompt, action, status, d
    mean = z[:, : P.P].mean(dim=(1, 2))  # domain, status, d
    names = [f"{dom}-{s}" for dom in "XY" for s in ("normal", "busy", "jam")]
    flat = mean.reshape(6, -1)
    flat = flat - flat.mean(0, keepdim=True)
    cos = F.cosine_similarity(flat[:, None], flat[None], dim=-1)
    return {"names": names, "centered_cosine": cos.numpy().round(3).tolist()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--first-seed", type=int, default=421)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    torch.set_num_threads(1)
    features = torch.load(args.cache, weights_only=True)
    route = features["root"][: P.P].numpy()
    runs = []
    for seed in range(args.first_seed, args.first_seed + args.seeds):
        old_rng, new_rng = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(2)]
        previous = P.Policy(features)
        archive = P.train_old(previous, route, old_rng, P.OLD_STEPS)
        replay = P.Replay(route, archive)
        new_batches = [P.new_domain(new_rng, P.NEW_BATCH, route) for _ in range(P.NEW_STEPS)]
        row = {"seed": seed, "before": P.evaluate(previous, features)}
        for arm in ARMS:
            row[arm] = P.evaluate(adapt(previous, new_batches, replay, arm, seed + 10000), features)
        runs.append(row)
        print(json.dumps({"seed": seed, **{a: round(row[a]["old_rare"] * 100, 2) for a in ARMS}}), flush=True)
    metrics = ("old_rare", "old_common", "new_common", "new_jam")
    summary = {a: {m: interval([100 * r[a][m] for r in runs]) for m in metrics} for a in ("before", *ARMS)}
    paired = {a: {m: interval([100 * (r[a][m] - r["none"][m]) for r in runs]) for m in metrics}
              for a in ARMS if a != "none"}
    out = {"seeds": [r["seed"] for r in runs], "geometry": feature_geometry(features),
           "summary_pct": summary, "minus_none_pp": paired, "runs": runs}
    args.output.write_text(json.dumps(out, indent=1) + "\n")
    for a in summary:
        print(a, {m: [round(x, 2) for x in v] for m, v in summary[a].items()})
    for a in paired:
        print("minus none", a, {m: [round(x, 2) for x in v] for m, v in paired[a].items()})


if __name__ == "__main__":
    main()
