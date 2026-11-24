"""CPU-only, paired-seed test of pool acquisition under a spurious cue."""

import argparse
import json
from pathlib import Path

import numpy as np


SEEDS = tuple(range(5))
BUDGETS = tuple(range(1, 33))
METHODS = ("random", "entropy", "committee", "divdis", "oracle")
MEMBERS = 5
INPUTS = 21
HIDDEN = 48
SIZES = {"source": 1024, "pool": 2048, "evaluation": 4096, "phase_b": 96}


def examples(rng, n, conflict_rate, task=0):
    bits = rng.integers(0, 2, size=(n, 16))
    y = (bits[:, 3 * task : 3 * task + 3].sum(axis=1) >= 2).astype(int)
    conflict = rng.random(n) < conflict_rate
    bits[:, 8] = y ^ conflict
    task_id = np.full(n, 2 * task - 1)
    x = np.column_stack((2 * bits - 1, task_id, rng.normal(size=(n, 4))))
    return x, y, conflict


class MLP:
    def __init__(self, rng, heads=1):
        self.weights = [
            rng.normal(0, INPUTS**-0.5, size=(INPUTS, HIDDEN)),
            np.zeros(HIDDEN),
            rng.normal(0, HIDDEN**-0.5, size=(HIDDEN, heads)),
            np.zeros(heads),
        ]

    def forward(self, x):
        w1, b1, w2, b2 = self.weights
        h = np.tanh(x @ w1 + b1)
        return h, 1 / (1 + np.exp(-np.clip(h @ w2 + b2, -40, 40)))

    def gradient(self, x, h, dz):
        dh = (dz @ self.weights[2].T) * (1 - h**2)
        return x.T @ dh, dh.sum(axis=0), h.T @ dz, dz.sum(axis=0)

    def fit(self, x, y, steps, lr, diversity_pool=None):
        for _ in range(steps):
            h, p = self.forward(x)
            g = self.gradient(x, h, (p - y[:, None]) / p.size)
            if diversity_pool is not None:
                dh, dp = self.forward(diversity_pool)
                mi_gradient = self.gradient(diversity_pool, dh, diversity_gradient(dp))
                g = [a + 2 * b for a, b in zip(g, mi_gradient)]
            for w, dw in zip(self.weights, g):
                w -= lr * dw
        return self

    def predict(self, x):
        return self.forward(x)[1]

    def copy(self):
        result = object.__new__(MLP)
        result.weights = [w.copy() for w in self.weights]
        return result


def diversity_gradient(p):
    """Gradient w.r.t. logits of empirical mutual information of two heads."""
    a = np.column_stack((1 - p[:, 0], p[:, 0]))
    b = np.column_stack((1 - p[:, 1], p[:, 1]))
    joint = a.T @ b / len(p)
    log_ratio = np.log(joint / np.outer(joint.sum(axis=1), joint.sum(axis=0)))
    da = b @ (log_ratio[1, :] - log_ratio[0, :])
    db = a @ (log_ratio[:, 1] - log_ratio[:, 0])
    return np.column_stack((da, db)) * p * (1 - p) / len(p)


def entropy(p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -p * np.log(p) - (1 - p) * np.log1p(-p)


def disagreement(p):
    return entropy(p.mean(axis=1)) - entropy(p).mean(axis=1)


def acquisition_orders(p, diverse_p, conflict, rng):
    """Only the privileged oracle sees conflict membership when ranking."""
    shuffled = rng.permutation(len(p))
    scores = {
        "random": np.zeros(len(p)),
        "entropy": entropy(p[:, 0]),
        "committee": disagreement(p),
        "divdis": disagreement(diverse_p),
        "oracle": conflict.astype(int),
    }
    return {
        name: shuffled[np.argsort(-score[shuffled], kind="stable")]
        for name, score in scores.items()
    }


def accuracy(model, data):
    x, y, _ = data
    return float(np.mean((model.predict(x)[:, 0] >= 0.5) == y))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    source_x, source_y, _ = examples(rng, SIZES["source"], 0.02)
    pool_x, pool_y, conflict = examples(rng, SIZES["pool"], 0.10)
    flip = examples(rng, SIZES["evaluation"], 1)
    # Reuse each target input and switch only the cue; anticue gets 0% here.
    aligned_x = flip[0].copy()
    aligned_x[:, 8] *= -1
    aligned = (aligned_x, flip[1], ~flip[2])
    b_train_x, b_train_y, _ = examples(rng, SIZES["phase_b"], 0.50, task=1)
    b_eval = examples(rng, SIZES["evaluation"], 0.50, task=1)

    models = [
        MLP(rng).fit(source_x, source_y, steps=80, lr=0.15)
        for _ in range(MEMBERS)
    ]
    base = models[0]
    p = np.column_stack([model.predict(pool_x)[:, 0] for model in models])
    # DivDis-style: a shared trunk, two source-supervised heads, and an
    # unlabeled mutual information penalty, not the full DivDis algorithm.
    diverse = MLP(rng, heads=2).fit(
        source_x, source_y, steps=80, lr=0.15, diversity_pool=pool_x
    )
    diverse_p = diverse.predict(pool_x)
    orders = acquisition_orders(p, diverse_p, conflict, rng)
    votes = p >= 0.5
    ensemble_flip = [accuracy(m, flip) for m in models]
    ensemble_aligned = [accuracy(m, aligned) for m in models]

    rows = {}
    for method in METHODS:
        curve = []
        for k in BUDGETS:
            selected = orders[method][:k]
            tuned = base.copy().fit(pool_x[selected], pool_y[selected], steps=100, lr=0.1)
            flip_before_b = accuracy(tuned, flip)
            aligned_before_b = accuracy(tuned, aligned)
            tuned.fit(b_train_x, b_train_y, steps=120, lr=0.1)
            curve.append({
                "queries": k,
                "conflict_fraction": float(conflict[selected].mean()),
                "a_flip": flip_before_b,
                "a_aligned": aligned_before_b,
                "a_flip_after_b": accuracy(tuned, flip),
                "a_aligned_after_b": accuracy(tuned, aligned),
                "b": accuracy(tuned, b_eval),
            })
        rows[method] = {
            "first_k_a_flip_ge_90": next((r["queries"] for r in curve if r["a_flip"] >= 0.90), None),
            "first_k_both_ge_90": next(
                (r["queries"] for r in curve if min(r["a_flip"], r["a_aligned"]) >= 0.90),
                None,
            ),
            "curve": curve,
        }

    return {
        "seed": seed,
        "pool_conflict_fraction": float(conflict.mean()),
        "base_entropy_conflict_nats": float(entropy(p[conflict, 0]).mean()),
        "base_entropy_aligned_nats": float(entropy(p[~conflict, 0]).mean()),
        "base_accuracy_conflict": float(np.mean(votes[conflict, 0] == pool_y[conflict])),
        "committee_hard_disagreement_on_conflict": float(
            np.mean(votes[conflict].any(axis=1) != votes[conflict].all(axis=1))
        ),
        "committee_a_flip": ensemble_flip,
        "committee_a_aligned": ensemble_aligned,
        "committee_rule_like": sum(
            min(a, f) >= 0.90 for a, f in zip(ensemble_aligned, ensemble_flip)
        ),
        "committee_cue_like": sum(
            a >= 0.90 and f <= 0.10 for a, f in zip(ensemble_aligned, ensemble_flip)
        ),
        "strategies": rows,
    }


def report(runs):
    def mean(key):
        return np.mean([run[key] for run in runs])

    print(f"Pool conflicts: {mean('pool_conflict_fraction'):.1%}")
    print(
        f"Base entropy (nats): conflict {mean('base_entropy_conflict_nats'):.3f}, "
        f"aligned {mean('base_entropy_aligned_nats'):.3f}; "
        f"conflict accuracy {mean('base_accuracy_conflict'):.1%}"
    )
    rule = sum(r["committee_rule_like"] for r in runs)
    cue = sum(r["committee_cue_like"] for r in runs)
    print(
        f"Committee fits: rule-like {rule}/{len(runs) * MEMBERS}, "
        f"cue-like {cue}/{len(runs) * MEMBERS}; hard conflict disagreement "
        f"{mean('committee_hard_disagreement_on_conflict'):.1%}"
    )
    print("method      conflict@32    first ≥90% flip / both by seed (* = >32)   "
          "A flip / aligned @32 → after B          B@32")
    for method in METHODS:
        outcomes = [r["strategies"][method] for r in runs]
        last = [s["curve"][-1] for s in outcomes]

        def first(key):
            return ",".join(str(s[key] or "*") for s in outcomes)

        def last_mean(key):
            return np.mean([r[key] for r in last])

        print(
            f"{method:10} {last_mean('conflict_fraction'):>10.1%}    "
            f"{first('first_k_a_flip_ge_90'):>14} / {first('first_k_both_ge_90'):<14}  "
            f"{last_mean('a_flip'):>6.1%}/{last_mean('a_aligned'):>6.1%} → "
            f"{last_mean('a_flip_after_b'):>6.1%}/{last_mean('a_aligned_after_b'):>6.1%}"
            f"  {last_mean('b'):>7.1%}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).with_name("discriminating_experiments_results.json")
    )
    args = parser.parse_args()
    runs = [run_seed(seed) for seed in SEEDS]
    report(runs)
    args.output.write_text(json.dumps({"sizes": SIZES, "runs": runs}, indent=2) + "\n")


if __name__ == "__main__":
    main()
