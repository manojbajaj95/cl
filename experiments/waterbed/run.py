"""Small-signal forgetting in a two-layer linear continual learner."""

import argparse
import json
import platform
import time
from pathlib import Path

import matplotlib
import numpy as np
import scipy
from scipy.interpolate import PchipInterpolator
from scipy.stats import t as student_t

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEEDS = tuple(range(410, 418))
METHODS = ("SGD slow", "SGD fast", "Replay", "EWC")
LR = np.array([0.025, 0.150, 0.075, 0.075])
AMPLITUDES = np.array([0.01, 0.02])
REPLAY = np.array([0.0, 0.0, 0.10, 0.0])
EWC = np.array([0.0, 0.0, 0.0, 8.0])
SAMPLES = 8192
BURN = 2048
WARM = 8192
N_BINS = 57
DIM = 4
BUFFER = 512
LABEL_VARIANCE = 0.25**2
MATCH_PP = 1.0
KILL_PERCENT = 20.0


def task(seed):
    rng = np.random.default_rng(seed)
    covariance = rng.uniform(0.65, 1.35, DIM)
    basis, _ = np.linalg.qr(rng.normal(size=(DIM, 2)))
    angle = rng.uniform(0.80, 1.20)
    a = basis[:, 0] / np.sqrt(covariance)
    b = (np.cos(angle) * basis[:, 0] + np.sin(angle) * basis[:, 1]) / np.sqrt(covariance)
    buffer = rng.normal(size=(BUFFER, DIM)) * np.sqrt(covariance)
    # Balanced factorization of the exact task-A solution, common to all arms.
    v = np.sqrt(np.linalg.norm(a))
    anchor = np.r_[a / v, v]
    jac = np.column_stack((v * np.eye(DIM), anchor[:-1]))
    fisher = LABEL_VARIANCE * ((covariance[:, None] * jac**2).sum(axis=0))
    return a, b, np.diag(covariance), buffer.T @ buffer / BUFFER, anchor, fisher


def product(theta):
    return theta[..., -1:] * theta[..., :-1]


def transpose_jac(theta, vector):
    return np.concatenate(
        [theta[..., -1:] * vector, (theta[..., :-1] * vector).sum(axis=-1, keepdims=True)],
        axis=-1,
    )


def loss(delta, cov):
    return 0.5 * (delta * np.einsum("sij,s...j->s...i", cov, delta)).sum(axis=-1)


def accuracy(beta, teacher, cov):
    expanded = teacher.reshape((len(teacher),) + (1,) * (beta.ndim - 2) + (DIM,))
    norm = 2 * np.sqrt(loss(beta, cov) * loss(expanded, cov))
    dot = (beta * np.einsum("sij,sj->si", cov, teacher).reshape(expanded.shape)).sum(axis=-1)
    return 1 - np.arccos(np.clip(dot / norm, -1, 1)) / np.pi


def update(theta, u, a, b, cov, cache, anchor, penalty):
    # Shape: seed x method x amplitude x frequency x parameter.
    beta = product(theta)
    grad_a = np.einsum("sij,sm...j->sm...i", cov, beta - a)
    grad_b = np.einsum("sij,sm...j->sm...i", cov, beta - b)
    gradient = (1 - REPLAY[:, None, None, None]) * (u * grad_a + (1 - u) * grad_b)
    gradient[:, 2] += REPLAY[2] * np.einsum("sij,s...j->s...i", cache, beta[:, 2] - a[:, 0])
    return theta - LR[:, None, None, None] * (
        transpose_jac(theta, gradient) + penalty * (theta - anchor)
    )


def transfer(theta, a, b, cov, cache, anchor, fisher, method):
    v, beta = theta[-1], product(theta)
    jac = np.column_stack((v * np.eye(DIM), theta[:-1]))
    h = (1 - REPLAY[method]) * cov + REPLAY[method] * cache
    grad = (1 - REPLAY[method]) * cov @ (beta - 0.5 * (a + b))
    grad += REPLAY[method] * cache @ (beta - a)
    d = EWC[method] * fisher
    np.testing.assert_allclose(jac.T @ grad + d * (theta - anchor), 0, atol=1e-8)
    hess = jac.T @ h @ jac + np.diag(d)
    hess[-1, :-1] += grad
    hess[:-1, -1] += grad
    poles, modes = np.linalg.eigh(np.eye(DIM + 1) - LR[method] * hess)
    drive = -LR[method] * (1 - REPLAY[method]) * jac.T @ cov @ (b - a)
    readout = jac.T @ cov @ (beta - a)
    residues = (readout @ modes) * (modes.T @ drive)
    # The scaling gauge of unregularized factorization is neutral but invisible.
    visible = abs(residues) > 1e-12 * np.max(abs(residues))
    assert np.all(abs(poles[visible]) < 1)
    assert np.all(abs(poles[~visible]) <= 1 + 1e-10)
    return poles[visible], residues[visible]


def response(omega, poles, residues):
    return (residues / (np.exp(1j * np.asarray(omega))[..., None] - poles)).sum(axis=-1)


def jensen(poles, residues):
    markov = residues.sum()
    numerator = sum(r * np.poly(np.delete(poles, j)) for j, r in enumerate(residues))
    zeros = np.roots(np.atleast_1d(numerator))
    # All fitted transfers have nonzero one-step gain.
    assert abs(markov) > 1e-12
    correction = np.log(abs(zeros[abs(zeros) > 1])).sum()
    return abs(markov), zeros, np.log(abs(markov)) + correction


def band_area(omega, gain):
    return PchipInterpolator(omega, np.log(gain), axis=-1).integrate(omega[0], np.pi) / (
        np.pi - omega[0]
    )


def full_area(omega, gain):
    # Flat extension over the tiny unswept near-DC interval.
    width = omega[0] / np.pi
    return (1 - width) * band_area(omega, gain) + width * np.log(gain[..., 0])


def lock_in(cosine, sine, n):
    # At Nyquist the real cos basis has norm n, not n/2.
    gain = 2 * np.hypot(cosine, sine) / n
    gain[..., -1] = abs(cosine[..., -1]) / n
    return gain


def measure(seed_ids=SEEDS):
    a, b, cov, cache, anchor, fisher = map(np.stack, zip(*(task(seed) for seed in seed_ids)))
    n = len(a)
    broadcast = lambda x: x[:, None, None, None, :]
    a_, b_, anchor_ = map(broadcast, (a, b, anchor))
    penalty = broadcast(fisher) * EWC[:, None, None, None]
    theta = np.broadcast_to(anchor_, (n, len(METHODS), 1, 1, DIM + 1))
    for _ in range(WARM):
        theta = update(theta, 0.5, a_, b_, cov, cache, anchor_, penalty)
    equilibrium = theta[:, :, 0, 0].copy()
    bins = np.unique(np.rint(np.geomspace(4, SAMPLES // 2, N_BINS)).astype(int))
    omega = 2 * np.pi * bins / SAMPLES
    theta = np.broadcast_to(theta, (n, len(METHODS), len(AMPLITUDES), len(omega), DIM + 1))
    amp = AMPLITUDES[:, None]
    sum_loss, sum_cos, sum_sin = (np.zeros(theta.shape[:-1]) for _ in range(3))
    for step in range(-BURN, SAMPLES):
        cos, sin = np.cos(omega * step), np.sin(omega * step)
        if step >= 0:
            old = loss(product(theta) - a_, cov)
            sum_loss += old
            sum_cos += old * cos
            sum_sin += old * sin
        u = (0.5 + amp * cos)[..., None]
        theta = update(theta, u, a_, b_, cov, cache, anchor_, penalty)
    gain = lock_in(sum_cos, sum_sin, SAMPLES) / amp
    area = full_area(omega, gain)
    terminal = product(theta)
    eq = product(equilibrium)
    old_final = accuracy(terminal, a, cov)
    new_final = accuracy(terminal, b, cov)
    old_eq, new_eq = accuracy(eq, a, cov), accuracy(eq, b, cov)
    mean_loss = (sum_loss / SAMPLES).mean(axis=-1)
    shape = (n, len(METHODS))
    sampled_lti = np.empty(shape + (len(omega),))
    markov, prediction, dense_area, gain0, max_zero = (np.empty(shape) for _ in range(5))
    dense = np.linspace(0, np.pi, 32769)
    for i in range(n):
        for j in range(len(METHODS)):
            args = equilibrium[i, j], a[i], b[i], cov[i], cache[i], anchor[i], fisher[i], j
            poles, residues = transfer(*args)
            markov[i, j], zeros, prediction[i, j] = jensen(poles, residues)
            max_zero[i, j] = max(abs(zeros), default=0.0)
            sampled_lti[i, j] = abs(response(omega, poles, residues))
            dense_gain = abs(response(dense, poles, residues))
            gain0[i, j] = dense_gain[0]
            dense_area[i, j] = np.trapezoid(np.log(dense_gain), dense) / np.pi
    return {
        "omega": omega,
        "gain": gain,
        "area": area,
        "band_area": band_area(omega, gain),
        "mean_old_loss": mean_loss,
        "old_accuracy_final": old_final,
        "new_accuracy_final": new_final,
        "old_accuracy_unforced": old_eq,
        "new_accuracy_unforced": new_eq,
        "old_loss_unforced": loss(eq - a[:, None, :], cov),
        "new_loss_unforced": loss(eq - b[:, None, :], cov),
        "one_step_gain": markov,
        "dc_gain": gain0,
        "max_zero_modulus": max_zero,
        "sampled_lti_gain": sampled_lti,
        "sampled_lti_area": full_area(omega, sampled_lti),
        "dense_lti_area": dense_area,
        "jensen_area": prediction,
        "gain_normalized_area": area - np.log(markov)[..., None],
    }


def interval(x):
    mean = x.mean(axis=0)
    half = student_t.ppf(0.975, len(x) - 1) * x.std(axis=0, ddof=1) / np.sqrt(len(x))
    return {"mean": mean, "ci95": np.stack([mean - half, mean + half])}


def percent_spread(x):
    return 100 * np.ptp(x, axis=-1) / np.mean(abs(x), axis=-1)


def summarize(r):
    area, normalized = r["area"][:, :, 0], r["gain_normalized_area"][:, :, 0]
    loss_a = r["mean_old_loss"][:, :, 0]
    final = 50 * (r["old_accuracy_final"] + r["new_accuracy_final"])
    unforced = 50 * (r["old_accuracy_unforced"] + r["new_accuracy_unforced"])
    ratio = r["gain"][:, :, 1] / r["gain"][:, :, 0]
    summary = {
        "area": interval(area),
        "gain_normalized_area": interval(normalized),
        "jensen_area": interval(r["jensen_area"]),
        "one_step_gain": interval(r["one_step_gain"]),
        "mean_old_loss": interval(loss_a),
        "old_accuracy_final_percent_sweep_mean": interval(100 * r["old_accuracy_final"][:, :, 0].mean(-1)),
        "joint_accuracy_final_percent_sweep_mean": interval(final[:, :, 0].mean(-1)),
        "joint_accuracy_unforced_percent": interval(unforced),
        "joint_accuracy_final_max_gap_pp": float(np.ptp(final, axis=1).max()),
        "sgd_pair_accuracy_final_max_gap_pp": float(np.ptp(final[:, :2], axis=1).max()),
        "area_spread_percent_of_mean_abs": float(percent_spread(area.mean(axis=0))),
        "area_spread_percent_by_seed": interval(percent_spread(area)),
        "sgd_pair_area_spread_percent_of_mean_abs": float(percent_spread(area.mean(axis=0)[:2])),
        "sgd_fast_minus_slow_area": interval(area[:, 1] - area[:, 0]),
        "geo_mean_gain_ratio_max_min": float(np.exp(np.ptp(area.mean(axis=0)))),
        "mean_old_loss_ratio_max_min": float(loss_a.mean(axis=0).max() / loss_a.mean(axis=0).min()),
        "max_amplitude_check_relative_error": float(abs(ratio - 1).max()),
        "max_small_signal_relative_gain_error": float(
            abs(r["gain"][:, :, 0] / r["sampled_lti_gain"] - 1).max()
        ),
        "max_measured_jensen_area_error": float(abs(area - r["jensen_area"]).max()),
        "max_sampled_lti_jensen_area_error": float(abs(r["sampled_lti_area"] - r["jensen_area"]).max()),
        "max_dense_lti_jensen_area_error": float(abs(r["dense_lti_area"] - r["jensen_area"]).max()),
        "max_gain_normalized_area_range_per_seed": float(np.ptp(normalized, axis=1).max()),
        "sgd_fast_to_slow_gain_ratio_min": float((r["gain"][:, 1, 0] / r["gain"][:, 0, 0]).min()),
    }
    summary["matched_final_accuracy_all_methods"] = summary["joint_accuracy_final_max_gap_pp"] <= MATCH_PP
    summary["matched_final_accuracy_sgd_pair"] = summary["sgd_pair_accuracy_final_max_gap_pp"] <= MATCH_PP
    summary["cross_method_kill_threshold_exceeded"] = summary["area_spread_percent_of_mean_abs"] > KILL_PERCENT
    summary["matched_pair_kill_threshold_exceeded"] = (
        summary["matched_final_accuracy_sgd_pair"]
        and summary["sgd_pair_area_spread_percent_of_mean_abs"] > KILL_PERCENT
    )
    return summary


def figure(r, directory):
    fig, axes = plt.subplots(1, 2, figsize=(8.7, 3.1), layout="constrained", sharex=True)
    for j, name in enumerate(METHODS):
        gain = r["gain"][:, j, 0]
        scaled = gain / r["one_step_gain"][:, j, None]
        for ax, samples in zip(axes, (gain, scaled)):
            result = interval(np.log(samples))
            line, = ax.loglog(r["omega"], np.exp(result["mean"]), label=name)
            ax.fill_between(r["omega"], *np.exp(result["ci95"]), color=line.get_color(), alpha=0.16)
            ax.set_xlabel("Frequency (radians / step)")
            ax.grid(alpha=0.22)
    axes[0].set_ylabel("Old-task loss gain")
    axes[1].set_ylabel("Gain / one-step gain")
    axes[0].legend(frameon=False, fontsize=8)
    fig.savefig(directory / "frequency_response.pdf")
    plt.close(fig)


def self_test():
    n = 64
    phase = np.arange(n)[:, None] * 2 * np.pi * np.array([3, n // 2]) / n
    signal = 0.42 + 0.08 * np.cos(phase) + 0.03 * np.sin(phase)
    np.testing.assert_allclose(
        lock_in((signal * np.cos(phase)).sum(0), (signal * np.sin(phase)).sum(0), n),
        [np.hypot(0.08, 0.03), 0.08],
    )
    dense = np.linspace(0, np.pi, 32769)
    for poles, residues, expected in (
        (np.array([0.8]), np.array([0.2]), np.log(0.2)),
        (np.array([0.2, 0.5]), np.array([-6.0, 7.0]), np.log(1.6)),
    ):
        _, _, predicted = jensen(poles, residues)
        area = np.trapezoid(np.log(abs(response(dense, poles, residues))), dense) / np.pi
        np.testing.assert_allclose([area, predicted], expected, atol=1e-12)
    print("Self-test passed: lock-in (including Nyquist), minimum- and nonminimum-phase Jensen oracles.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    start_cpu, start_clock = time.process_time(), time.perf_counter()
    data = measure()
    summary = summarize(data)
    result = {
        "configuration": {
            "seeds": SEEDS, "methods": METHODS, "learning_rates": LR, "amplitudes": AMPLITUDES,
            "replay_fractions": REPLAY, "ewc_strengths": EWC, "buffer_examples": BUFFER,
            "dimension": DIM, "fisher_label_variance": LABEL_VARIANCE, "burn_steps": BURN,
            "unforced_warmup_steps": WARM, "measurement_steps": SAMPLES,
            "accuracy_match_percentage_points": MATCH_PP, "kill_threshold_percent": KILL_PERCENT,
        },
        "environment": {
            "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__, "platform": platform.machine(),
        },
        "summary": summary,
        "runs": data,
    }
    figure(data, args.output)
    result["cpu_seconds"] = time.process_time() - start_cpu
    result["wall_seconds"] = time.perf_counter() - start_clock
    to_json = lambda x: x.tolist()
    (args.output / "results.json").write_text(json.dumps(result, default=to_json, separators=(",", ":")) + "\n")
    print(json.dumps(summary, default=to_json, indent=2))
    print(f"CPU {result['cpu_seconds']:.2f} s; wall {result['wall_seconds']:.2f} s.")


if __name__ == "__main__":
    main()
