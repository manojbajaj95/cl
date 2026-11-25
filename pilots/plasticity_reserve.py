"""CPU-only Slowly-Changing Regression write-selection pilot."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.stats import rankdata, t


POLICIES = ("random", "gramian", "readiness", "feature_rank", "next_readiness")
SCORES = POLICIES[1:] + ("gramian_rank",)


@dataclass(frozen=True)
class Config:
    tasks: int = 50
    width: int = 5
    candidates: int = 8
    slow_bits: int = 15
    random_bits: int = 5
    teacher_width: int = 100
    batch: int = 4
    write_steps: int = 1500
    fork_steps: int = 32
    gain_steps: int = 50
    repeats: int = 5
    validation_tasks: int = 4
    samples: int = 256
    probes: int = 64
    readiness_batches: int = 128
    write_lr: float = 0.06
    gain_lr: float = 0.01
    loss_tolerance: float = 0.02
    ridge: float = 0.001


def rng(seed, *key):
    return np.random.default_rng(np.random.SeedSequence([seed, *key]))


def bits(random, shape):
    return random.integers(0, 2, shape).astype(float)


def inputs(random, cfg, count, context=None):
    slow = bits(random, (count, cfg.slow_bits)) if context is None else np.broadcast_to(
        context, (count, cfg.slow_bits)
    )
    return np.column_stack((slow, bits(random, (count, cfg.random_bits)), np.ones(count)))


def teacher(random, cfg):
    dimension = cfg.slow_bits + cfg.random_bits + 1
    w = 2 * bits(random, (dimension, cfg.teacher_width)) - 1
    v = 2 * bits(random, cfg.teacher_width) - 1
    return w, v, 0.5 * dimension - (w < 0).sum(axis=0)


def labels(x, target):
    w, v, threshold = target
    return ((x @ w > threshold) @ v) / np.sqrt(len(v))


def build_stream(seed, cfg):
    shifts = rng(seed, 0)
    target = teacher(rng(seed, 1), cfg)
    context = bits(shifts, cfg.slow_bits)
    support = (np.arange(2**cfg.random_bits)[:, None] >> np.arange(cfg.random_bits)) & 1
    stream = []
    for task in range(cfg.tasks):
        def data(key, count):
            x = inputs(rng(seed, key, task), cfg, count, context)
            return x, labels(x, target)

        match = np.column_stack((np.broadcast_to(context, (len(support), cfg.slow_bits)),
                                 support, np.ones(len(support))))
        stream.append((
            data(10, cfg.write_steps * cfg.batch), (match, labels(match, target)),
            data(12, cfg.samples), data(13, cfg.gain_steps * cfg.batch), data(14, cfg.samples),
        ))
        bit = shifts.integers(cfg.slow_bits)
        context[bit] = 1 - context[bit]
    return stream


def initial_params(seed, cfg):
    random = rng(seed, 2)
    widths = (cfg.slow_bits + cfg.random_bits + 1, cfg.width, cfg.width, 1)
    return tuple(p for n, m in zip(widths, widths[1:]) for p in (
        random.uniform(-1 / np.sqrt(n), 1 / np.sqrt(n), (n, m)),
        random.uniform(-1 / np.sqrt(n), 1 / np.sqrt(n), (1, m)),
    ))


def forward(params, x):
    w1, b1, w2, b2, w3, b3 = params
    h1 = np.maximum(x @ w1 + b1, 0)
    h2 = np.maximum(h1 @ w2 + b2, 0)
    return (h2 @ w3 + b3)[..., 0], h1, h2


def sensitivities(params, h1, h2):
    _, _, w2, _, w3, _ = params
    d2 = w3.swapaxes(-1, -2) * (h2 > 0)
    d1 = (d2 @ w2.swapaxes(-1, -2)) * (h1 > 0)
    return d1, d2


def mse(params, data):
    x, y = data
    return np.mean((forward(params, x)[0] - y) ** 2, axis=-1)


def gradient(params, x, y):
    pred, h1, h2 = forward(params, x)
    d1, d2 = sensitivities(params, h1, h2)
    d3 = (2 / x.shape[-2]) * (pred - y)[..., None]
    d1, d2 = d1 * d3, d2 * d3
    return tuple(g for h, d in ((x, d1), (h1, d2), (h2, d3)) for g in (
        h.swapaxes(-1, -2) @ d, d.sum(axis=-2, keepdims=True),
    ))


def fit(params, data, orders, lr):
    x, y = data
    for idx in orders:
        params = tuple(p - lr * g for p, g in zip(params, gradient(params, x[idx], y[idx])))
    return params


def take(params, idx):
    return tuple(p[idx] for p in params)


def write_candidates(params, task, seed, idx, cfg):
    train, match, _, _, _ = task
    prefix = cfg.write_steps - cfg.fork_steps
    shared = fit(params, train, np.arange(prefix * cfg.batch).reshape(prefix, cfg.batch), cfg.write_lr)
    tail = np.arange(prefix * cfg.batch, cfg.write_steps * cfg.batch)
    random = rng(seed, 20, idx)
    orders = np.stack([random.permutation(tail) for _ in range(cfg.candidates)])
    orders = orders.reshape(cfg.candidates, cfg.fork_steps, cfg.batch).swapaxes(0, 1)
    endpoints = fit(shared, train, orders, cfg.write_lr)
    reference = take(endpoints, np.argmin(mse(endpoints, match)))
    ref_loss = mse(reference, match)
    blend = np.ones(cfg.candidates)
    candidates = endpoints
    for _ in range(20):
        losses = mse(candidates, match)
        half_width = cfg.loss_tolerance / (2 + cfg.loss_tolerance)
        outside = np.abs(losses - ref_loss) > ref_loss * half_width + 1e-12
        if not outside.any():
            return candidates, losses, blend
        blend[outside] *= 0.5
        candidates = tuple(r + blend[:, None, None] * (p - r) for r, p in zip(reference, endpoints))
    raise RuntimeError("Could not match the eight candidate losses")


def output_jacobian(params, probes):
    pred, h1, h2 = forward(params, probes)
    d1, d2 = sensitivities(params, h1, h2)
    d3 = np.ones_like(pred)[..., None]
    return np.concatenate(tuple(block for h, d in ((probes, d1), (h1, d2), (h2, d3)) for block in (
        (h[..., :, :, None] * d[..., :, None, :]).reshape(*pred.shape, -1), d,
    )), axis=-1), h2


def effective_rank(values):
    positive = np.maximum(values, 0)
    total = positive.sum(axis=-1, keepdims=True)
    p = np.divide(positive, total, out=np.zeros_like(positive), where=total > 0)
    entropy = -(p * np.log(np.where(p > 0, p, 1))).sum(axis=-1)
    return np.where(total[..., 0] > 0, np.exp(entropy), 0)


def geometry(params, probes, cfg):
    jac, hidden = output_jacobian(params, probes)
    eigenvalues = np.linalg.eigvalsh(jac @ jac.swapaxes(-1, -2)).clip(0)
    rank = np.linalg.svd(hidden, compute_uv=False)
    return {
        "gramian": np.log(eigenvalues + cfg.ridge).sum(axis=-1),
        "gramian_rank": effective_rank(eigenvalues),
        "feature_rank": effective_rank(rank),
    }


def readiness(params, data, orders):
    x, y = data
    # Exact per-example gradient, reused for all mini-batch estimates in Appendix D.3.
    jac, _ = output_jacobian(params, x)
    g = 2 * (forward(params, x)[0] - y)[..., None] * jac
    signal = (g.mean(axis=-2) ** 2).sum(axis=-1)
    second_moment = (g[..., orders, :].mean(axis=-2) ** 2).sum(axis=-1).mean(axis=-1)
    denominator = mse(params, data) * second_moment
    return np.divide(signal**2, denominator, out=np.zeros_like(signal), where=denominator > 0)


def gain(params, data, evaluate, orders, cfg):
    before = mse(params, evaluate)
    after = mse(fit(params, data, orders, cfg.gain_lr), evaluate)
    relative = (before - after) / np.maximum(before, 1e-12)
    return relative, before, after


def orders_for_gain(seed, task, repeat, cfg):
    return rng(seed, 21, task, repeat).permutation(cfg.gain_steps * cfg.batch).reshape(
        cfg.gain_steps, cfg.batch
    )


def independent_validation(seed, idx, cfg):
    context = bits(rng(seed, 3, idx), cfg.slow_bits)
    target = teacher(rng(seed, 4, idx), cfg)
    train = inputs(rng(seed, 5, idx), cfg, cfg.gain_steps * cfg.batch, context)
    test = inputs(rng(seed, 6, idx), cfg, cfg.samples, context)
    return (train, labels(train, target)), (test, labels(test, target))


def choose(policy, candidates, probes, current, future, batch_ids, random, cfg):
    if policy == "random" or (policy == "next_readiness" and future is None):
        return int(random.integers(cfg.candidates))
    if policy in ("gramian", "feature_rank"):
        values = geometry(candidates, probes, cfg)[policy]
    else:
        values = readiness(candidates, current if policy == "readiness" else future, batch_ids)
    return int(random.choice(np.flatnonzero(values == values.max())))


def stream_run(seed, policy, cfg):
    start = time.perf_counter()
    tasks = build_stream(seed, cfg)
    probes = inputs(rng(seed, 7), cfg, cfg.probes)
    independent = [independent_validation(seed, i, cfg) for i in range(cfg.validation_tasks)]
    params = initial_params(seed, cfg)
    trace, diagnostics = [], []
    for idx, task in enumerate(tasks):
        _, _, _, adaptation, evaluate = task
        orders = [orders_for_gain(seed, idx, repeat, cfg) for repeat in range(cfg.repeats)]
        speed, initial_loss, adapted_loss = np.mean(
            [gain(params, adaptation, evaluate, order, cfg) for order in orders], axis=0
        )
        validation_gain = np.mean([gain(params, *data, orders[i % len(orders)], cfg)[0]
                                   for i, data in enumerate(independent)])
        candidates, losses, blend = write_candidates(params, task, seed, idx, cfg)
        batch_ids = rng(seed, 22, idx).integers(0, cfg.samples, (cfg.readiness_batches, cfg.batch))
        future_support = tasks[idx + 1][2] if policy == "next_readiness" and idx + 1 < cfg.tasks else None
        chosen = choose(policy, candidates, probes, task[2], future_support, batch_ids,
                        rng(seed, 23, idx), cfg)

        if policy == "random" and idx + 1 < cfg.tasks:
            _, _, future_support, future_train, future_test = tasks[idx + 1]
            future = np.stack([
                gain(candidates, future_train, future_test, orders_for_gain(seed, idx + 1, r, cfg), cfg)[0]
                for r in range(cfg.repeats)
            ], axis=1)
            scores = geometry(candidates, probes, cfg)
            scores["gramian"] = scores["gramian"] - geometry(params, probes, cfg)["gramian"]
            scores["readiness"] = readiness(candidates, task[2], batch_ids)
            scores["next_readiness"] = readiness(candidates, future_support, batch_ids)
            diagnostics.append({
                "task": idx + 1,
                "scores": {key: value.tolist() for key, value in scores.items()},
                "future_gain": future.tolist(),
            })
        params = take(candidates, chosen)
        trace.append({
            "task": idx + 1, "choice": chosen, "gain": speed, "initial_loss": initial_loss,
            "adapted_loss": adapted_loss, "independent_gain": validation_gain,
            "candidate_losses": losses.tolist(), "blend": blend.tolist(),
        })
    return {
        "seed": seed, "policy": policy, "trace": trace, "diagnostics": diagnostics,
        "seconds": time.perf_counter() - start,
    }


def spearman(x, y):
    a, b = rankdata(x), rankdata(y)
    a, b = a - a.mean(), b - b.mean()
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / denom) if denom else 0.0


def variance_components(gains):
    n, r = gains.shape
    means = gains.mean(axis=1, keepdims=True)
    residual = gains - means - gains.mean(axis=0) + gains.mean()
    noise = (residual**2).sum() / ((n - 1) * (r - 1))
    signal = means.var(ddof=1) - noise / r
    return signal, noise


def ci(values):
    values = np.asarray(values)
    mean = values.mean()
    if len(values) < 2:
        return {"mean": float(mean), "ci95": None}
    half = t.ppf(0.975, len(values) - 1) * values.std(ddof=1) / np.sqrt(len(values))
    return {"mean": float(mean), "ci95": [float(mean - half), float(mean + half)]}


def block_bootstrap(correlations):
    random = rng(75862)
    n_seeds, n_writes, _ = correlations.shape
    size, block = 10000, min(7, n_writes)
    streams = random.integers(n_seeds, size=(size, n_seeds, 1))
    starts = random.integers(n_writes, size=(size, n_seeds, -(-n_writes // block), 1))
    writes = ((starts + np.arange(block)) % n_writes).reshape(size, n_seeds, -1)[..., :n_writes]
    sample = correlations[streams, writes].mean(axis=(1, 2))
    differences = np.stack([sample[:, 0] - sample[:, SCORES.index(key)]
                            for key in ("readiness", "next_readiness")], axis=1)
    bounds = np.quantile(np.column_stack((sample, differences)), [0.025, 0.975], axis=0).T
    return dict(zip(SCORES + ("gramian_minus_readiness", "gramian_minus_next_readiness"), bounds.tolist()))


def summarize(runs):
    by_policy = {p: {row["seed"]: row for row in runs if row["policy"] == p} for p in POLICIES}
    baseline = by_policy["random"]
    seed_stats, correlations_by_seed = [], []
    constant = dict.fromkeys(SCORES, 0)
    for row in baseline.values():
        correlations, signal, noise, spreads = [], [], [], []
        for write in row["diagnostics"]:
            gains = np.asarray(write["future_gain"])
            true_gain = gains.mean(axis=1)
            correlations.append([spearman(write["scores"][key], true_gain) for key in SCORES])
            for key in SCORES:
                constant[key] += int(np.ptp(write["scores"][key]) == 0)
            s, n = variance_components(gains)
            signal.append(s)
            noise.append(n)
            spreads.append(np.ptp(true_gain))
        correlations_by_seed.append(correlations)
        variance = np.mean(signal) + np.mean(noise)
        seed_stats.append({
            **dict(zip(SCORES, np.mean(correlations, axis=0))),
            "signal_variance": np.mean(signal), "noise_variance": np.mean(noise),
            "gain_spread": np.mean(spreads),
            "reliability": np.mean(signal) / variance if variance else 0.0,
        })
    summary = {"diagnostic": {key: ci([s[key] for s in seed_stats]) for key in seed_stats[0]}}
    for key in ("readiness", "next_readiness"):
        summary["diagnostic"][f"gramian_minus_{key}"] = ci([s["gramian"] - s[key] for s in seed_stats])
    summary["spearman_block_bootstrap_ci95"] = block_bootstrap(np.asarray(correlations_by_seed))
    summary["constant_score_writes"] = constant

    def metric(row, key, span):
        return np.mean([x[key] for x in row["trace"][span]])

    spans = {"final": slice(-1, None), "last10": slice(-10, None), "early10": slice(0, 10)}
    summary["policy"] = {
        policy: {
            name: {
                **{key: ci([metric(row, key, span) for row in rows.values()])
                   for key in ("gain", "initial_loss", "adapted_loss", "independent_gain")},
                "paired_gain_vs_random": ci([
                    metric(row, "gain", span) - metric(baseline[seed], "gain", span)
                    for seed, row in rows.items()
                ]),
            } for name, span in spans.items()
        } for policy, rows in by_policy.items() if rows
    }
    summary["baseline_decay"] = {
        key: ci([metric(row, key, spans["last10"]) - metric(row, key, spans["early10"])
                 for row in baseline.values()])
        for key in ("gain", "independent_gain")
    }
    spreads = np.asarray([np.ptp(x["candidate_losses"]) / max(min(x["candidate_losses"]), 1e-12)
                          for row in runs for x in row["trace"]])
    blends = np.asarray([x["blend"] for row in runs for x in row["trace"]])
    summary["matching"] = {
        "writes": len(spreads), "median_relative_spread": float(np.median(spreads)),
        "max_relative_spread": float(spreads.max()), "fraction_shrunk": float(np.mean(blends < 1)),
        "median_blend": float(np.median(blends)),
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[101, 102, 103])
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--random-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cfg = Config()
    policies = ("random",) if args.random_only else POLICIES
    jobs = [(seed, policy, cfg) for seed in args.seeds for policy in policies]
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(stream_run, *job) for job in jobs]
        runs = []
        for future in futures:
            run = future.result()
            print(f"{run['seed']} {run['policy']}: {run['seconds']:.2f}s", flush=True)
            runs.append(run)
    summary = summarize(runs)
    result = {
        "config": asdict(cfg), "seeds": args.seeds, "summary": summary, "runs": runs,
        "wall_seconds": time.perf_counter() - start,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.platform()},
    }
    args.output.write_text(json.dumps(result, separators=(",", ":"), allow_nan=False) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
