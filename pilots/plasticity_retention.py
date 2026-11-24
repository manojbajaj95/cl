"""Retention-matched, projected variant of the plasticity-reserve pilot."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from functools import partial
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy

import plasticity_reserve as pilot


def match_retention(candidates, panels, cfg):
    reference = pilot.take(candidates, np.argmin(pilot.mse(candidates, panels[0])))
    x, y = (np.stack(arrays) for arrays in zip(*panels))
    ref_losses = pilot.mse(reference, (x, y))
    half_width = cfg.loss_tolerance / (2 + cfg.loss_tolerance)
    blend = np.ones(cfg.candidates)
    matched = candidates
    for _ in range(40):
        losses = pilot.mse(tuple(p[:, None] for p in matched), (x, y))
        outside = np.any(np.abs(losses - ref_losses) > half_width * ref_losses + 1e-12, axis=1)
        if not outside.any():
            return matched, losses, blend, reference
        blend[outside] *= 0.5
        matched = tuple(r + blend[:, None, None] * (p - r) for r, p in zip(reference, candidates))
    raise RuntimeError("Could not match current and prior task losses")


def flatten(params):
    return np.concatenate([p.reshape(*p.shape[:-2], -1) for p in params], axis=-1)


def old_gradient_basis(directions):
    unit = np.asarray(directions, dtype=float)
    norm = np.linalg.norm(unit, axis=-1, keepdims=True)
    unit = np.divide(unit, norm, out=np.zeros_like(unit), where=norm > 1e-12)
    _, s, basis = np.linalg.svd(unit, full_matrices=False)
    return basis[s > 1e-10 * s[0]]


def project(rows, basis):
    return rows - (rows @ basis.T) @ basis


def projected_gain(params, data, evaluate, orders, basis, cfg):
    x, y = data
    sizes = np.cumsum([p.shape[-2] * p.shape[-1] for p in params[:-1]])
    before = pilot.mse(params, evaluate)
    for idx in orders:
        grad = project(flatten(pilot.gradient(params, x[idx], y[idx])), basis)
        params = tuple(p - cfg.gain_lr * g.reshape(p.shape)
                       for p, g in zip(params, np.split(grad, sizes, axis=-1)))
    after = pilot.mse(params, evaluate)
    absolute = before - after
    return absolute / np.maximum(before, 1e-12), absolute


def gain_diagnostics(repeats):
    signal, noise = pilot.variance_components(repeats)
    return np.ptp(repeats.mean(axis=1)), signal, noise


def original_stream(seed, cfg, tasks):
    params = pilot.initial_params(seed, cfg)
    ranges = []
    for idx, task in enumerate(tasks[:-1]):
        candidates, _, _ = pilot.write_candidates(params, task, seed, idx, cfg)
        _, _, _, adapt, evaluate = tasks[idx + 1]
        results = [pilot.gain(candidates, adapt, evaluate,
                             pilot.orders_for_gain(seed, idx + 1, r, cfg), cfg)
                   for r in range(cfg.repeats)]
        relative, before, after = np.asarray(results).mean(axis=0)
        ranges.append((np.ptp(relative), np.ptp(before - after)))
        params = pilot.take(candidates, pilot.rng(seed, 23, idx).integers(cfg.candidates))
    return np.mean(ranges, axis=0)


def stream(seed, cfg):
    tasks = pilot.build_stream(seed, cfg)
    original_spread, original_absolute_spread = original_stream(seed, cfg, tasks)
    params = pilot.initial_params(seed, cfg)
    panels, directions, matched_stats, current_stats = [], [], [], []
    absolute_stats, loss_ranges, blends, ranks = [], [], [], []
    for idx, task in enumerate(tasks[:-1]):
        current, _, _ = pilot.write_candidates(params, task, seed, idx, cfg)
        panels.insert(0, task[1])
        matched, losses, blend, reference = match_retention(current, panels, cfg)
        directions.append(flatten(pilot.gradient(reference, *task[1])))
        basis = old_gradient_basis(directions)

        _, _, _, adapt, evaluate = tasks[idx + 1]
        orders = [pilot.orders_for_gain(seed, idx + 1, r, cfg) for r in range(cfg.repeats)]
        paired = tuple(np.concatenate((a, b)) for a, b in zip(matched, current))
        gains, absolute = np.stack([projected_gain(paired, adapt, evaluate, order, basis, cfg)
                                    for order in orders], axis=-1)
        matched_stats.append(gain_diagnostics(gains[:cfg.candidates]))
        current_stats.append(gain_diagnostics(gains[cfg.candidates:]))
        absolute_stats.append(gain_diagnostics(absolute[:cfg.candidates]))
        loss_ranges.append(np.ptp(losses, axis=0) / np.maximum(losses.min(axis=0), 1e-12))
        blends.extend(blend.tolist())
        ranks.append(len(basis))
        params = pilot.take(matched, pilot.rng(seed, 23, idx).integers(cfg.candidates))
    return {
        "seed": seed,
        "original_spread": original_spread,
        "original_absolute_spread": original_absolute_spread,
        **dict(zip(("spread", "signal_variance", "order_variance"), np.mean(matched_stats, axis=0))),
        **dict(zip(("absolute_spread", "absolute_signal_variance", "absolute_order_variance"),
                   np.mean(absolute_stats, axis=0))),
        **dict(zip(("current_only_spread", "current_only_signal_variance", "current_only_order_variance"),
                   np.mean(current_stats, axis=0))),
        "spread_change": np.mean(np.asarray(matched_stats)[:, 0] - np.asarray(current_stats)[:, 0]),
        "max_current_loss_range": max(row[0] for row in loss_ranges),
        "max_prior_loss_range": max(row[1:].max() for row in loss_ranges[1:]),
        "mean_additional_blend": np.mean(blends),
        "fraction_backtracked_again": np.mean(np.asarray(blends) < 1),
        "final_projection_rank": ranks[-1],
    }


def summarize(rows):
    raw = ("max_current_loss_range", "max_prior_loss_range", "final_projection_rank")
    measures = [key for key in rows[0] if key not in ("seed", *raw)]
    summary = {key: pilot.ci([row[key] for row in rows]) for key in measures}
    summary.update({key: max(row[key] for row in rows) for key in raw})
    interval = summary["absolute_signal_variance"]["ci95"]
    summary["gate_passed"] = (
        min(summary[key]["mean"] for key in ("original_absolute_spread", "absolute_spread")) >= 0.015
        and interval is not None and interval[0] > 0
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-seed", type=int, default=101)
    parser.add_argument("--seed-count", type=int, default=512)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.seed_count < 2:
        parser.error("--seed-count must be at least 2")
    cfg = pilot.Config()
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        seeds = range(args.first_seed, args.first_seed + args.seed_count)
        rows = list(pool.map(partial(stream, cfg=cfg), seeds, chunksize=4))
    result = {
        "config": asdict(cfg), "summary": summarize(rows), "streams": rows,
        "wall_seconds": time.perf_counter() - start,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "platform": platform.platform()},
    }
    args.output.write_text(json.dumps(result, separators=(",", ":"), allow_nan=False) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
