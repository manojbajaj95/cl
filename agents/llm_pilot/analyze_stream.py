"""Does R measured in the challenge trial predict which closed-loop streams collapse?

From the curve (challenge trial, fixed lesson mixes) we estimate for each (style, k) and gate rate f:
  eps = P_0, tau from P_1 = 1 - (1 - eps)(1 - tau), alpha_D / alpha_S = admission rates of defective / sound lessons,
  R = k tau alpha_D / alpha_S.
Predictors of stream outcome (contamination grows: x_T > x_0), compared by AUC over streams:
  R          the reproduction number (measured offline, before any stream runs)
  gate       alpha_D / alpha_S only (the gate's catch rates)
  meanfield  full mean-field forecast from the curve, mixing j ~ Binomial(k, x)
  early      the stream's own defect share at episode T/4 (online extrapolation baseline)
Usage: python -m agents.llm_pilot.analyze_stream
"""
from __future__ import annotations

import json
from collections import defaultdict
from math import comb

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .stream import OUT


def read(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def admit_prob(row, f):
    return ((1 - f) + f * row["correct"]) if row["lesson"] else 0.0


def measured(curve, k, f):
    """R and its parts from curve rows for one retrieval breadth k under gate rate f."""
    rows = [r for r in curve if r["k"] == k]
    P = np.array([np.mean([r["defective"] for r in rows if r["j"] == j]) for j in range(k + 1)])
    eps = P[0]
    tau = 1 - (1 - P[1]) / (1 - eps) if eps < 1 else 0.0
    dr = [admit_prob(r, f) for r in rows if r["defective"] and r["j"] > 0]
    sr = [admit_prob(r, f) for r in rows if not r["defective"]]
    a_d, a_s = (np.mean(dr) if dr else 1.0), (np.mean(sr) if sr else 1e-9)
    D = np.array([np.mean([admit_prob(r, f) * r["defective"] for r in rows if r["j"] == j]) for j in range(k + 1)])
    S = np.array([np.mean([admit_prob(r, f) * (not r["defective"]) for r in rows if r["j"] == j])
                  for j in range(k + 1)])
    return dict(P=P.tolist(), eps=float(eps), tau=float(tau), alpha_D=float(a_d), alpha_S=float(a_s),
                gate=float(a_d / a_s), R=float(k * tau * a_d / a_s), D=D, S=S)


def mix(v, x):
    k = len(v) - 1
    return sum(comb(k, j) * x ** j * (1 - x) ** (k - j) * v[j] for j in range(k + 1))


def meanfield(D, S, x0, n0, T):
    x, n = x0, float(n0)
    for _ in range(T):
        d, s = mix(D, x), mix(S, x)
        x, n = float(np.clip(x + (d * (1 - x) - s * x) / n, 0, 1)), n + d + s
    return x


def auc(score, label):
    score, label = np.asarray(score, float), np.asarray(label, bool)
    pos, neg = score[label], score[~label]
    if len(pos) == 0 or len(neg) == 0:
        return None
    return float(np.mean([(p > q) + 0.5 * (p == q) for p in pos for q in neg]))


def boot_auc(score, label, B=1000, seed=0):
    rng = np.random.default_rng(seed)
    score, label = np.asarray(score, float), np.asarray(label, bool)
    vals = [auc(score[i], label[i]) for i in (rng.integers(0, len(score), len(score)) for _ in range(B))]
    vals = [v for v in vals if v is not None]
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def main():
    curve = read(OUT / "curve.jsonl")
    rows = read(OUT / "streams.jsonl")
    streams = defaultdict(list)
    for r in rows:
        streams[(r["style"], r["k"], r["f"], r["x0"], r["pair"], r["seed"])].append(r)
    res = dict(conditions={}, streams=[])
    for key, rs in sorted(streams.items()):
        style, k, f, x0, pair, seed = key
        rs.sort(key=lambda r: r["t"])
        T, n0 = len(rs), rs[0]["n0"]
        x0a = round(x0 * n0) / n0
        m = measured([c for c in curve if c["style"] == style], k, f)
        ck = f"{style} k={k} f={f}"
        if ck not in res["conditions"]:
            res["conditions"][ck] = {a: m[a] for a in ("P", "eps", "tau", "alpha_D", "alpha_S", "gate", "R")}
        res["streams"].append(dict(style=style, k=k, f=f, x0=x0a, pair=pair, seed=seed, R=m["R"], gate=m["gate"],
                                   meanfield=meanfield(m["D"], m["S"], x0a, n0, T), early=rs[T // 4 - 1]["x"],
                                   x_final=rs[-1]["x"], grew=rs[-1]["x"] > x0a,
                                   success_last=float(np.mean([r["correct"] for r in rs[-T // 4:]])),
                                   traj=[x0a] + [r["x"] for r in rs]))
    S = res["streams"]
    lab = [s["grew"] for s in S]
    res["auc"] = {p: dict(auc=auc([s[p] for s in S], lab), ci95=boot_auc([s[p] for s in S], lab))
                  for p in ("R", "gate", "meanfield", "early")}
    for ck, c in res["conditions"].items():
        ss = [s for s in S if f"{s['style']} k={s['k']} f={s['f']}" == ck]
        c.update(n_streams=len(ss), frac_grew=float(np.mean([s["grew"] for s in ss])),
                 x_final_mean=float(np.mean([s["x_final"] for s in ss])),
                 meanfield_mean=float(np.mean([s["meanfield"] for s in ss])),
                 success_last=float(np.mean([s["success_last"] for s in ss])))
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    cs = list(res["conditions"].values())
    for c, (ck, _) in zip(cs, res["conditions"].items()):
        ax[0].scatter(c["R"], c["frac_grew"], c="C0" if "plain" in ck else "C3")
        ax[0].annotate(ck.replace("plain ", "").replace("correction ", "c "), (c["R"], c["frac_grew"]), fontsize=7)
        ax[1].scatter(c["gate"], c["frac_grew"], c="C0" if "plain" in ck else "C3")
    ax[0].axvline(1, ls="--", c="k", lw=1)
    ax[1].axvline(1, ls="--", c="k", lw=1)
    ax[0].set_xlabel("R measured in the challenge trial")
    ax[1].set_xlabel("gate ratio alpha_D / alpha_S only")
    for a in ax:
        a.set_ylabel("fraction of streams whose defect share grew")
    ax[0].set_title("Qwen2.5-1.5B lesson-memory streams (blue plain, red correction-style defects)", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "streams.png", dpi=130)
    out = dict(res)
    out["streams"] = [{k: v for k, v in s.items() if k != "traj"} for s in S]
    (OUT / "summary.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(dict(auc=res["auc"], conditions=res["conditions"]), indent=2))


if __name__ == "__main__":
    main()
