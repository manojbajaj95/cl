"""Does a lesson act like a temperature change of the no-lesson policy?

For each lesson, fit the single temperature T (base logits / T) whose per-start exact success
best matches the lesson's per-start success, and report R^2 of per-start lesson effects.
Also correlates the rank-1 interaction loadings with entropy change and base success.
"""

import json
import sys

import numpy as np
from scipy.special import log_softmax

from task_by_lesson import exact

TEMPS = np.exp(np.linspace(np.log(0.2), np.log(5.0), 241))


def entropy(logp):
    return float(-(np.exp(logp) * logp).sum(-1).mean())


def run(name, logp):
    succ = exact(logp)
    eff = succ[1:] - succ[0]
    temp_succ = exact(np.stack([log_softmax(logp[0] / t, -1) for t in TEMPS]))
    temp_eff = temp_succ - succ[0]
    err = ((eff[:, None, :] - temp_eff[None]) ** 2).sum(-1)
    best = err.argmin(1)
    fit = temp_eff[best]
    r2 = lambda y, f: float(1 - ((y - f) ** 2).sum() / ((y - y.mean()) ** 2).sum())
    inter = eff - eff.mean(0) - eff.mean(1, keepdims=True) + eff.mean()
    fint = fit - fit.mean(0) - fit.mean(1, keepdims=True) + fit.mean()
    u, s, vt = np.linalg.svd(inter, full_matrices=False)
    dent = np.array([entropy(l) - entropy(logp[0]) for l in logp[1:]])
    sign = np.sign(np.corrcoef(u[:, 0], dent)[0, 1])
    out = {
        "temperature_fit_R2_all": r2(eff, fit),
        "temperature_fit_R2_interaction": float(1 - ((inter - fint) ** 2).sum() / (inter ** 2).sum()),
        "temperature_fit_R2_start_centered": r2(eff - eff.mean(0), fit - fit.mean(0)),
        "best_T_quartiles": np.percentile(TEMPS[best], [0, 25, 50, 75, 100]).round(3).tolist(),
        "rank1_lesson_loading_vs_entropy_change_r": float(np.corrcoef(sign * u[:, 0], dent)[0, 1]),
        "rank1_start_loading_vs_base_success_r": float(np.corrcoef(sign * vt[0], succ[0])[0, 1]),
        "base_success_by_start": succ[0].round(3).tolist(),
        "rank1_start_loading": (sign * vt[0]).round(3).tolist(),
    }
    print(name, json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    g1, q2, path = sys.argv[1:4]
    res = {"g1": run("g1", np.load(g1)["policy"]), "q2": run("q2", np.load(q2)["new"])}
    json.dump(res, open(path, "w"), indent=1)
