"""Estimate transfer rates by exact stochastic-policy marginalization."""

import argparse
import json
from pathlib import Path

import numpy as np

from coding import CONTEXTS, FAMILIES, signature, stream


ARMS = ("bad", "filler", "correct", "base")
T = 0.8
BOOTSTRAP_SEED = 316044
METRICS = ("solve_any", "write_any", "write_planted", "write_other")


def distribution(logits, beta):
    scaled = logits * beta
    shifted = scaled - scaled.max(axis=-1, keepdims=True)
    logp = shifted - np.log(np.exp(shifted).sum(axis=-1, keepdims=True))
    return np.exp(logp), logp


def entropy(logits, beta):
    p, logp = distribution(logits, beta)
    return -(p * logp).sum(axis=-1)


def match_temperatures(source, weights):
    bad, *_, base = source.transpose(1, 0, 2, 3)
    fixed_solve = distribution(base[:, 0], 1 / T)[0]

    def stages(h):
        return np.stack([h[..., 0], (h[..., 1:] * fixed_solve).sum(axis=-1)], axis=-1)

    target = weights @ stages(entropy(bad, 1 / T))

    def pooled(beta):
        beta = np.repeat(beta, [1, 3], axis=-1)[:, None, :, None]
        return np.einsum("bf,bfs->bs", weights, stages(entropy(base[None], beta)))

    low, high = np.zeros_like(target), np.full_like(target, 1024.0)
    if np.any(pooled(high) > target + 1e-10):
        raise ValueError("Requested entropy is outside the temperature bracket")
    for _ in range(36):
        mid = (low + high) / 2
        above = pooled(mid) > target
        low, high = np.where(above, mid, low), np.where(above, high, mid)
    return (low + high) / 2


def outcomes(p):
    solve = p[..., 0, :]
    write = (solve[..., :, None] * p[..., 1:, :]).sum(axis=-2)
    return np.stack([solve[..., 1:].sum(axis=-1), write[..., 1:].sum(axis=-1),
                     write[..., 1], write[..., 2]], axis=-1)


def estimate(panel, weights):
    source, held_out = panel[:, 0], panel[:, 1:]
    # weights resample families; every task and arm within a family moves together.
    inverse_t = match_temperatures(source, weights)
    beta = np.repeat(inverse_t, [1, 3], axis=-1)[:, None, None, :, None]
    no_memory = held_out[:, :, ARMS.index("base")]
    nominal = distribution(held_out, 1 / T)[0]
    matched = distribution(no_memory[None], beta)[0]
    fixed_held_out = nominal[:, :, ARMS.index("base"), 0]

    def diagnostic(h):
        return np.stack([h[..., 0], (h[..., 1:] * fixed_held_out).sum(axis=-1)], axis=-1)

    bad_h = diagnostic(entropy(held_out[:, :, ARMS.index("bad")], 1 / T)).mean(axis=1)
    matched_h = diagnostic(entropy(no_memory[None], beta)).mean(axis=2)
    rates = np.einsum("bf,fam->bam", weights, outcomes(nominal).mean(axis=1))
    temp = np.einsum("bf,bfm->bm", weights, outcomes(matched).mean(axis=2))
    return np.concatenate([rates, temp[:, None, :]], axis=1), inverse_t, (
        weights @ bad_h, np.einsum("bf,bfs->bs", weights, matched_h))


def summarize(panel, draws=10_000):
    n = panel.shape[0]
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    counts = rng.multinomial(n, np.full(n, 1 / n), size=draws)
    weights = np.vstack([np.ones(n), counts]) / n
    pieces = [estimate(panel, weights[i:i+256]) for i in range(0, len(weights), 256)]
    rates = np.concatenate([p[0] for p in pieces])
    inv_t = np.concatenate([p[1] for p in pieces])
    bad_h, matched_h = (np.concatenate([p[2][i] for p in pieces]) for i in range(2))
    by_arm = dict(zip((*ARMS, "temperature"), rates.transpose(1, 2, 0)))

    def interval(samples):
        return {"estimate": float(samples[0]), "ci95": np.percentile(samples[1:], [2.5, 97.5]).tolist()}

    deltas = {arm: dict(zip(METRICS, map(interval, by_arm["bad"] - values)))
              for arm, values in by_arm.items() if arm != "bad"}
    any_bad = by_arm["bad"][METRICS.index("write_any")]
    any_filler = by_arm["filler"][METRICS.index("write_any")]
    keep = deltas["filler"]["write_any"]["ci95"][0] > 0
    gpu = (keep and deltas["temperature"]["write_any"]["ci95"][0] > 0
           and deltas["filler"]["write_planted"]["ci95"][0] > 0)
    return {
        "families": n, "source_tasks": n, "held_out_tasks": n * (panel.shape[1] - 1),
        "bootstrap_draws": draws, "bootstrap_seed": BOOTSTRAP_SEED, "nominal_temperature": T,
        "matched_temperature": dict(zip(("solve", "write"), map(interval, 1 / inv_t.T))),
        "held_out_entropy_nats": {"bad": bad_h[0].tolist(), "temperature": matched_h[0].tolist()},
        "rates": {arm: dict(zip(METRICS, map(interval, vals))) for arm, vals in by_arm.items()},
        "bad_minus_control": deltas,
        "background_adjusted_tau": interval((any_bad - any_filler) / (1 - any_filler)),
        "keep_at_cpu_gate": bool(keep), "recommend_stage_1": bool(gpu),
    }


def load_policies(path):
    with path.open() as f:
        model = json.loads(next(f))
        raw = [json.loads(line) for line in f]
    frozen = list(stream())
    tasks = [(f.name, v, list(so), list(wo)) for f, v, so, wo in frozen]
    if [(r["family"], r["variant"], r["solve_order"], r["write_order"]) for r in raw] != tasks:
        raise ValueError("Policy rows do not cover the frozen stream in order")
    if any(json.loads(json.dumps(signature(f, v))) != r["signature"] for (f, v, *_), r in zip(frozen, raw)):
        raise ValueError("Frozen outputs do not agree with the writer oracles")
    if not all(r["tokens"]["bad"] == r["tokens"]["filler"] == r["tokens"]["correct"] for r in raw):
        raise ValueError("Mismatched token budgets")
    panel = np.array([[r["logits"][arm] for arm in ARMS] for r in raw])
    if panel.shape != (len(tasks), len(ARMS), 4, 3) or not np.isfinite(panel).all():
        raise ValueError("Invalid policy logits")
    return model, panel.reshape(len(FAMILIES), len(CONTEXTS), len(ARMS), 4, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policies", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    model, panel = load_policies(args.policies)
    result = {"model": model, **summarize(panel)}
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
