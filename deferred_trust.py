"""CPU pilot for source-weight revisions after a chronological SGD stream."""

import argparse
import json
import platform
from dataclasses import dataclass
from time import perf_counter

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import expit


K = 24
ROWS = 48
STEPS = 1536
RATE = 0.16
PAIR_RANK = K // 2
RADIUS = 0.25  # Calibration radius for finite-difference shadows.
I, J = np.triu_indices(K, k=1)
SETTINGS = ("paired", "bridged", "dense", "digits")
DEV_SEEDS = range(11, 15)
TEST_SEEDS = range(101, 125)
AUDIT_SEEDS = range(201, 225)


@dataclass
class Stream:
    x: np.ndarray
    y: np.ndarray
    sources: np.ndarray
    eval_x: np.ndarray
    eval_y: np.ndarray
    pairs: np.ndarray


def sample_stream(setting, seed):
    rng = np.random.default_rng(seed)
    sources = np.arange(STEPS) % K
    rng.shuffle(sources)
    assignment = rng.permutation(K) // 2
    pairs = np.flatnonzero(assignment[I] == assignment[J])
    bad = rng.choice(K, 6, replace=False)
    if setting == "digits":
        from sklearn.datasets import load_digits

        digits = load_digits()
        order = rng.permutation(len(digits.data))
        all_x = (digits.data[order] / 16 - 0.5) / 4
        clean_y = digits.target[order] % 2
        eval_x, eval_y = all_x[STEPS:], clean_y[STEPS:]
        train_x, clean_y = all_x[:STEPS], clean_y[:STEPS]
    else:
        width = 6
        dim = PAIR_RANK * width
        teacher = rng.normal(size=dim)

        def sample_x(groups):
            size = len(groups)
            if setting == "dense":
                return rng.normal(size=(size, dim)) / np.sqrt(dim)
            values = np.zeros((size, PAIR_RANK, width))
            values[np.arange(size), groups] = rng.normal(size=(size, width))
            if setting == "bridged":
                other = (groups + rng.integers(1, PAIR_RANK, size)) % PAIR_RANK
                values[np.arange(size), other] = 0.35 * rng.normal(size=(size, width))
            return values.reshape(size, dim) / np.sqrt(width)

        groups = assignment[sources]
        if setting == "rekeyed":
            old_assignment = rng.permutation(K) // 2
            groups[:STEPS // 4] = old_assignment[sources[:STEPS // 4]]
        train_x = sample_x(groups)
        eval_x = sample_x(rng.integers(PAIR_RANK, size=512))
        clean_y = (train_x @ teacher + 0.4 * rng.normal(size=STEPS) > 0).astype(int)
        eval_y = (eval_x @ teacher + 0.4 * rng.normal(size=512) > 0).astype(int)
    # Ensure models cannot identify future revisions from corruption labels.
    flipped = np.isin(sources, bad) & (rng.random(STEPS) < 0.75)
    return Stream(train_x, clean_y ^ flipped, sources, eval_x, eval_y, pairs)


def run_shadows(stream, edits, rate):
    weights = np.zeros((len(edits), stream.x.shape[1]))
    for x, y, s in zip(stream.x, stream.y, stream.sources):
        update = (1 + edits[:, s]) * (expit(weights @ x) - y)
        weights -= rate * update[:, None] * x
    return weights


class Affinity:
    def __init__(self, dim, capacity):
        self.fingerprints = np.zeros((K, dim))
        self.seen = np.zeros(K, dtype=bool)
        self.remaining = capacity

    def arrivals(self, x, source):
        if self.seen[source] or self.remaining == 0:
            return []
        normalized = x / max(np.linalg.norm(x), 1e-12)
        similarity = np.abs(self.fingerprints @ normalized)
        choices = np.argsort(-similarity, kind="stable")[:self.remaining]
        choices = choices[similarity[choices] > 1e-10]
        self.fingerprints[source] = normalized
        self.seen[source] = True
        self.remaining -= len(choices)
        return choices


def pair_index(a, b):
    i, j = min(a, b), max(a, b)
    return i * (2 * K - i - 1) // 2 + j - i - 1


def run_jet(stream, directions, rate, *, affinity=False):
    """Exact derivatives at unit source weight; None directions keeps all pairs."""
    if directions is not None and affinity:
        raise ValueError("affinity and directional sketches are mutually exclusive")
    dim = stream.x.shape[1]
    w = np.zeros(dim)
    tangent = np.zeros((K, dim))
    diag = np.zeros_like(tangent)
    rows = K if affinity else len(I) if directions is None else len(directions)
    pair = np.zeros((rows, dim))
    directions_sq = None if directions is None else directions**2
    if affinity:
        gate = Affinity(dim, rows)
        active = []
    for x, y, s in zip(stream.x, stream.y, stream.sources):
        p = expit(w @ x)
        f1 = p * (1 - p)
        f2 = f1 * (1 - 2 * p)
        v = tangent @ x
        if affinity:
            # Before source s is seen, every jet involving s is exactly zero.
            active.extend(pair_index(s, other) for other in gate.arrivals(x, s))
            pi, pj = I[active], J[active]
        else:
            pi, pj = I, J
        if directions is None:
            forcing = f2 * v[pi] * v[pj] + f1 * ((pi == s) * v[pj] + (pj == s) * v[pi])
        else:
            projected = directions @ v
            forcing = (
                0.5 * f2 * (projected**2 - directions_sq @ (v**2))
                + f1 * (directions[:, s] * projected - directions_sq[:, s] * v[s])
            )
        updated = pair[:len(active)] if affinity else pair
        updated -= rate * (f1 * (updated @ x) + forcing)[:, None] * x
        forcing_diag = f2 * v**2
        forcing_diag[s] += 2 * f1 * v[s]
        diag -= rate * (f1 * (diag @ x) + forcing_diag)[:, None] * x
        tangent -= rate * f1 * v[:, None] * x
        tangent[s] -= rate * (p - y) * x
        w -= rate * (p - y) * x
    return (w, tangent, diag, pair) + ((np.array(active, dtype=int),) if affinity else ())


def pair_features(edits):
    return edits[:, I] * edits[:, J]


def subspace_decode(probes, response, rank):
    """MUSIC: select by distance to response span, then solve on that support."""
    if not 0 < rank < probes.shape[0] or rank > min(probes.shape[1], response.shape[1]):
        return np.array([], dtype=int), np.empty((0, response.shape[1]))
    basis, _, _ = np.linalg.svd(response, full_matrices=False)
    span = basis[:, :rank]
    residual = probes - span @ (span.T @ probes)
    norm = np.linalg.norm(probes, axis=0)
    distance = np.divide(np.linalg.norm(residual, axis=0), norm,
                         out=np.full_like(norm, np.inf), where=norm > 0)
    selected = np.argsort(distance, kind="stable")[:rank]
    return selected, np.linalg.lstsq(probes[:, selected], response, rcond=None)[0]


def queries(seed):
    rng = np.random.default_rng(seed)
    edits = np.zeros((36, K))
    size = np.repeat([2, 4, 8, 2, 4, 8], 6)
    radius = np.repeat([0.5, 1.0], len(edits) // 2)
    for row, n, r in zip(edits, size, radius):
        row[rng.choice(K, n, replace=False)] = rng.choice([-r, r], size=n)
    return edits, size, radius


def ridge_decode(probing, response):
    gram = probing @ probing.T
    coef = np.linalg.solve(gram + 0.01 * np.diag(np.diag(gram)), response)
    return lambda features: (features @ probing.T) @ coef


def guarded_decode(phi, h, edit_features):
    """Select on one fresh sketch, test against zero on another."""
    fit, select, confirm = slice(0, 32), slice(32, 40), slice(40, 48)
    candidates = {"ridge": ridge_decode(phi[fit], h[fit])}
    for rank in (4, 8, 12, 16, 24):
        support, coefs = subspace_decode(phi[fit], h[fit], rank)
        candidates[f"music{rank}"] = lambda f, s=support, c=coefs: f[:, s] @ c
    selected = min(
        candidates, key=lambda name: np.sum((h[select] - candidates[name](phi[select]))**2)
    )
    decode = candidates[selected]
    baseline = np.sum(h[confirm]**2)
    ratio = np.sum((h[confirm] - decode(phi[confirm]))**2) / baseline if baseline else 1.0
    if ratio > 0.8:
        return np.zeros((len(edit_features), h.shape[1])), "diagonal", float(ratio)
    return decode(edit_features), selected, float(ratio)


def shadow_predictions(stream, signs, edits, rate):
    axis = RADIUS * np.eye(K)
    joint = RADIUS * signs
    calibration = np.concatenate([np.zeros((1, K)), axis, -axis, joint, -joint])
    models = run_shadows(stream, calibration, rate)
    anchor, plus, minus, both_plus, both_minus = np.split(
        models, [1, K + 1, 2 * K + 1, 2 * K + 1 + len(signs)]
    )
    gradient = (plus - minus) / (2 * RADIUS)
    diag = (plus + minus - 2 * anchor) / RADIUS**2
    directional_pair = (both_plus + both_minus - 2 * anchor) / (2 * RADIUS**2) - 0.5 * diag.sum(axis=0)
    # For the axis-only control, interpolate deletion and upweighting exactly
    # at each evaluation radius (two independent banks, one per radius).
    independent = np.empty_like(edits @ gradient)
    for r in (0.5, 1.0):
        positive, negative = np.split(run_shadows(stream, r * np.concatenate([np.eye(K), -np.eye(K)]), rate), 2)
        which = np.max(np.abs(edits), axis=1) == r
        independent[which] = (
            anchor + (edits[which] > 0) @ (positive - anchor)
            + (edits[which] < 0) @ (negative - anchor)
        )
    quadratic = anchor + edits @ gradient + 0.5 * edits**2 @ diag
    probing = pair_features(signs)
    chosen, coefs = subspace_decode(probing, directional_pair, PAIR_RANK)
    # Minimum-norm dense decoder: linear kernel ridge in pair coordinates.
    ridge = ridge_decode(probing, directional_pair)
    return {
        "axis_shadow": independent,
        "mixed_subspace": quadratic + pair_features(edits)[:, chosen] @ coefs,
        "mixed_ridge": quadratic + ridge(pair_features(edits)),
    }


def affinity_shadows(stream, edits, rate):
    """Spend the same vector budget on early affinity plus 12 live mixed pairs."""
    dim = stream.x.shape[1]
    gate = Affinity(dim, PAIR_RANK)
    axis = RADIUS * np.eye(K)
    n_axis = 2 * K + 1
    calibration = np.concatenate([np.zeros((1, K)), axis, -axis, np.zeros((K, K))])
    weights = np.zeros((len(calibration), dim))
    active = []
    for x, y, s in zip(stream.x, stream.y, stream.sources):
        for other in gate.arrivals(x, s):
            row = n_axis + 2 * len(active)
            active.append(pair_index(s, other))
            # Source s has no past yet; only other has affected each shadow.
            weights[row:row + 2] = weights[[1 + other, 1 + K + other]]
            calibration[row:row + 2, [s, other]] = [[RADIUS, RADIUS], [-RADIUS, -RADIUS]]
        n = n_axis + 2 * len(active)
        update = (1 + calibration[:n, s]) * (expit(weights[:n] @ x) - y)
        weights[:n] -= rate * update[:, None] * x
    anchor = weights[0]
    plus, minus = weights[1:K + 1], weights[K + 1:n_axis]
    gradient = (plus - minus) / (2 * RADIUS)
    diagonal = (plus + minus - 2 * anchor) / RADIUS**2
    indices = np.array(active, dtype=int)
    joint = weights[n_axis:n:2] + weights[n_axis + 1:n:2]
    cross = (joint - 2 * anchor) / (2 * RADIUS**2) - 0.5 * (
        diagonal[I[indices]] + diagonal[J[indices]]
    )
    return anchor + edits @ gradient + 0.5 * edits**2 @ diagonal + pair_features(edits)[:, indices] @ cross


def batch_refit(stream, edits):
    """Memory-relaxed control using all labels, but discarding chronology."""
    metrics = []
    for edit in edits:
        trust = 1 + edit[stream.sources]

        def objective(w):
            z = stream.x @ w
            return (
                np.mean(trust * (np.logaddexp(0, z) - stream.y * z)) + 0.005 * (w @ w),
                stream.x.T @ (trust * (expit(z) - stream.y)) / len(z) + 0.01 * w,
            )

        result = minimize(objective, np.zeros(stream.x.shape[1]), jac=True, method="L-BFGS-B")
        if not result.success:
            raise RuntimeError(result.message)
        metrics.append(result.x)
    return np.array(metrics)


def outcome(stream, estimate, oracle):
    logits = estimate @ stream.eval_x.T
    loss = np.mean(np.logaddexp(0, logits) - stream.eval_y * logits, axis=1)
    return np.sqrt(np.mean((estimate - oracle)**2, axis=1)), loss


def pilot(setting, seed, *, audit=False):
    stream = sample_stream(setting, seed)
    rng = np.random.default_rng(np.random.SeedSequence([seed, 21]))
    directions = rng.normal(size=(ROWS, K))
    signs = rng.choice([-1.0, 1.0], size=(ROWS // 2, K))
    edits, size, radius = queries(np.random.SeedSequence([seed, 22]))
    phi = pair_features(directions)
    xpair = pair_features(edits)
    times = {}

    def timed(name, run):
        start = perf_counter()
        value = run()
        times[name] = perf_counter() - start
        return value

    ref = timed("oracle", lambda: run_shadows(stream, edits, RATE))
    w, j, d, h = timed("sketch", lambda: run_jet(stream, directions, RATE))
    _, _, _, dense = timed("dense", lambda: run_jet(stream, None, RATE))
    first = w + edits @ j
    diagonal = first + 0.5 * edits**2 @ d
    chosen, coefs = timed("decode", lambda: subspace_decode(phi, h, PAIR_RANK))
    _, _, _, affinity, active = timed("affinity", lambda: run_jet(stream, None, RATE, affinity=True))
    jet_bytes = sum(a.nbytes for a in (w, j, d, h, directions))
    capacity = (jet_bytes - w.nbytes) // (stream.x.shape[1] * 8 + 8 * 3)
    # A uniformly sampled reservoir with timestamps, replayed in order.
    keep = np.sort(rng.choice(STEPS, size=capacity, replace=False))
    reservoir = Stream(stream.x[keep], stream.y[keep], stream.sources[keep],
                       stream.eval_x, stream.eval_y, stream.pairs)

    def replay_revision():
        replay = run_shadows(reservoir, np.vstack([np.zeros((1, K)), edits]), RATE * STEPS / capacity)
        return w + (replay[1:] - replay[0])

    predictions = {
        "oracle": ref,
        "anchor": np.broadcast_to(w, ref.shape),
        "tangent": first,
        "diagonal": diagonal,
        "affinity_jet": diagonal + xpair[:, active] @ affinity[:len(active)],
        "sketched": diagonal + xpair[:, chosen] @ coefs,
        "dense_jet": diagonal + xpair @ dense,
        "reservoir": timed("reservoir_decode", replay_revision),
    }
    predictions.update(timed("shadows_with_axis_control", lambda: shadow_predictions(stream, signs, edits, RATE)))
    predictions["affinity_shadows"] = timed("affinity_shadows", lambda: affinity_shadows(stream, edits, RATE))
    if setting == "paired":
        predictions["batch_refit"] = timed("batch_refit", lambda: batch_refit(stream, edits))
    audit_record = {}
    if audit:
        correction, decoder, ratio = timed("guard", lambda: guarded_decode(phi, h, xpair))
        predictions["guarded"] = diagonal + correction
        audit_record = {"decoder": decoder, "confirmation_residual_ratio": ratio}
    support = {}
    for m in (PAIR_RANK, PAIR_RANK + 1, ROWS):
        selected, _ = subspace_decode(phi[:m], h[:m], PAIR_RANK)
        support[m] = len(np.intersect1d(stream.pairs, selected)) / PAIR_RANK
    records = []
    for method, estimate in predictions.items():
        error, loss = outcome(stream, estimate, ref)
        for r in (0.5, 1.0):
            use = radius == r
            records.append({
                "method": method, "radius": r,
                "rmse": float(error[use].mean()), "clean_loss": float(loss[use].mean()),
                "rmse_by_size": {n: float(error[use & (size == n)].mean()) for n in (2, 4, 8)},
            })
    return {
        "setting": setting, "seed": seed, "support_recall": support, "records": records,
        "jet_bytes": jet_bytes, "reservoir_capacity": int(capacity), "times_s": times,
        "audit": audit_record,
        "cross_hessian_energy_in_pair_blocks": float(
            np.linalg.norm(dense[stream.pairs])**2 / np.linalg.norm(dense)**2
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test", "audit"), default="test")
    parser.add_argument("--settings", nargs="+", choices=(*SETTINGS, "rekeyed"))
    args = parser.parse_args()
    settings = args.settings or (SETTINGS + (("rekeyed",) if args.split == "audit" else ()))
    if "rekeyed" in settings and args.split != "audit":
        parser.error("rekeyed is part of the audit split only")
    seeds = {"dev": DEV_SEEDS, "test": TEST_SEEDS, "audit": AUDIT_SEEDS}[args.split]
    print(json.dumps({"python": platform.python_version(), "numpy": np.__version__,
                      "scipy": scipy.__version__, "split": args.split}), flush=True)
    for setting in settings:
        for seed in seeds:
            print(json.dumps(pilot(setting, seed, audit=args.split == "audit")), flush=True)


if __name__ == "__main__":
    main()
