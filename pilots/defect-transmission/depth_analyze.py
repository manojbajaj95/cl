"""Fit per-defect transfer and apply the retrieval-depth funding gate."""

import argparse
import json
from pathlib import Path

import numpy as np

from analyze import ARMS, BOOTSTRAP_SEED, METRICS, T, distribution, entropy, load_policies, match_temperatures, outcomes
from coding import CONTEXTS, DEPTHS, DEPTH_ARMS, FAMILIES, stream


THRESHOLD = 0.5


def adjusted_risk(p0, p1):
    return (p1 - p0) / (1 - p0)


def dose_fit(p0, p1, pk, k):
    baseline = np.log1p(-p0)
    slope = ((np.log1p(-p1) - baseline) + k * (np.log1p(-pk) - baseline)) / (1 + k**2)
    return -np.expm1(slope)


def load_depth(path, k):
    raw = [json.loads(line) for line in path.read_text().splitlines()]
    expected = [(k, f.name, v, (i // len(CONTEXTS) + v) % k) for i, (f, v, *_) in enumerate(stream())]
    if [(r["k"], r["family"], r["variant"], r["bad_slot"]) for r in raw] != expected:
        raise ValueError(f"Depth {k} lacks the frozen tasks and slot assignments")
    panel = np.array([[r["logits"][arm] for arm in DEPTH_ARMS] for r in raw])
    if panel.shape != (len(expected), len(DEPTH_ARMS), 4, 3) or not np.isfinite(panel).all():
        raise ValueError(f"Bad scores at depth {k}")
    return panel.reshape(len(FAMILIES), len(CONTEXTS), len(DEPTH_ARMS), 4, 3)


def matched_controls(panel, base, weights):
    target = panel[:, :, DEPTH_ARMS.index("one_bad_sound")]
    source = np.stack([target[:, 0], base[:, 0]], axis=1)
    inverse_t = match_temperatures(source, weights)
    beta = np.repeat(inverse_t, [1, 3], axis=-1)[:, None, None, :, None]
    base = base[:, 1:]
    nominal_solve = distribution(base[..., 0, :], 1 / T)[0]
    matched = distribution(base[None], beta)[0]

    def held_out_entropy(h):
        return np.stack([h[..., 0], (h[..., 1:] * nominal_solve).sum(axis=-1)], axis=-1)

    target_entropy = held_out_entropy(entropy(target[:, 1:], 1 / T)).mean(axis=1)
    matched_entropy = held_out_entropy(entropy(base[None], beta)).mean(axis=2)
    return (np.einsum("bf,bfm->bm", weights, outcomes(matched).mean(axis=2)), 1 / inverse_t,
            weights @ target_entropy, np.einsum("bf,bfs->bs", weights, matched_entropy))


def summarize_depth(panel, base, k, weights):
    def interval(samples):
        return {"estimate": float(samples[0]), "ci95": np.quantile(samples[1:], [.025, .975]).tolist()}

    y = outcomes(distribution(panel[:, 1:], 1 / T)[0]).mean(axis=1)
    pooled = np.einsum("bf,fam->bam", weights, y)
    pieces = [matched_controls(panel, base, weights[i:i+256]) for i in range(0, len(weights), 256)]
    matched, temp, target_h, matched_h = (np.concatenate(columns) for columns in zip(*pieces))
    gross = pooled[:, :, METRICS.index("write_any")].T
    f0, f1, bk, _, s1, s0 = gross
    local = adjusted_risk(s0, s1)
    direct_filler = adjusted_risk(f0, f1)
    fitted = dose_fit(f0, f1, bk, k)
    return {
        "risks": {arm: dict(zip(METRICS, map(interval, arr.T)))
                  for arm, arr in zip(DEPTH_ARMS, pooled.transpose(1, 0, 2))},
        "tau_eff": interval(local), "k_tau_eff": interval(k * local),
        "local_risk_difference": interval(s1 - s0),
        "local_planted_difference": interval(
            pooled[:, DEPTH_ARMS.index("one_bad_sound"), METRICS.index("write_planted")]
            - pooled[:, DEPTH_ARMS.index("one_filler_sound"), METRICS.index("write_planted")]),
        "tau_one_bad_filler": interval(direct_filler),
        "tau_dose_fit": interval(fitted), "k_tau_dose_fit": interval(k * fitted),
        "full_dose_actual_minus_single_hit_prediction": interval(bk - (1 - (1 - f0) * (1 - direct_filler)**k)),
        "matched_temperature": dict(zip(("solve", "write"), map(interval, temp.T))),
        "matched_temperature_risk": dict(zip(METRICS, map(interval, matched.T))),
        "held_out_entropy_nats": {"one_bad_sound": target_h[0].tolist(), "temperature": matched_h[0].tolist()},
        "one_bad_sound_minus_temperature": dict(zip(
            METRICS, map(interval, (pooled[:, DEPTH_ARMS.index("one_bad_sound")] - matched).T))),
    }


def summarize(original, depths, draws=10_000):
    n = len(original)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    weights = np.vstack([np.ones(n), rng.multinomial(n, np.full(n, 1/n), size=draws)]) / n
    names = ("filler", "bad", "bad", "correct", "bad", "filler")
    depths = {1: original[:, :, [ARMS.index(name) for name in names]], **depths}
    base = original[:, :, ARMS.index("base")]
    rows = {k: summarize_depth(depths[k], base, k, weights) for k in DEPTHS}
    survivors = [k for k, row in rows.items() if row["k_tau_eff"]["ci95"][1] >= THRESHOLD]
    return {"families": n, "held_out_tasks_per_depth": n * (original.shape[1] - 1),
            "bootstrap_draws": draws, "bootstrap_seed": BOOTSTRAP_SEED, "funding_threshold": THRESHOLD,
            "depths": rows, "depths_with_headroom": survivors, "recommend_stage_1": bool(survivors)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    model, original = load_policies(Path(__file__).with_name("policies.jsonl"))
    depths = {k: load_depth(args.dir / f"depth-{k}.jsonl", k) for k in DEPTHS[1:]}
    result = {"original_run": model, **summarize(original, depths)}
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
