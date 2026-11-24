"""Score runs/*.jsonl against the frozen protocol; write results.json and print the table."""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
ARMS = ["tool", "tool+tests", "lesson", "lesson+tests", "none"]
MEASURES = ["detect", "recover"]


def load(path):
    rows = [json.loads(l) for l in path.open()]
    meta = rows[0]
    final = rows[-1] if rows[-1].get("final") else None
    eps = [r for r in rows if "t" in r]
    return meta, eps, final


def units(meta, eps):
    """Per drifted procedure: detect / recover use index, silent-wrong uses, episode offsets."""
    out = []
    t0 = meta["drift_at"]
    for api, kind in meta["drift"].items():
        uses = [r for r in eps if r["api"] == api and r["t"] >= t0]
        n = len(uses)
        det = next((i + 1 for i, r in enumerate(uses) if r["signals"]), n + 1)
        rec = next((i + 1 for i, r in enumerate(uses)
                    if r["ok"] and (i + 1 == n or uses[i + 1]["ok"])), n + 1)

        def ep(k):
            return uses[k - 1]["t"] - t0 + 1 if k <= n else None

        out.append(dict(api=api, kind=kind, uses=n, detect=det, recover=rec,
                        detect_ep=ep(det), recover_ep=ep(rec),
                        detect_censored=det > n, recover_censored=rec > n,
                        silent_wrong=sum(1 for r in uses if not r["ok"] and not r["signals"])))
    return out


def summary(meta, eps, final):
    pre = [r for r in eps if r["t"] < meta["drift_at"]]
    post_clean = [r for r in eps if r["t"] >= meta["drift_at"] and r["drift"] is None]
    return dict(pre_acc=float(np.mean([r["ok"] for r in pre])),
                post_undrifted_acc=float(np.mean([r["ok"] for r in post_clean])),
                false_flags=sum(1 for r in pre + post_clean if r["signals"]),
                llm_calls=final["llm_calls"] if final else None,
                tokens=final["tokens"] if final else None,
                sec=final["sec"] if final else None)


def hboot(diffs_by_seed, n=10000, rng=None):
    rng = rng or np.random.default_rng(0)
    seeds = list(diffs_by_seed)
    stats = np.empty(n)
    for b in range(n):
        vals = []
        for s in rng.choice(seeds, len(seeds)):
            d = diffs_by_seed[s]
            vals.extend(rng.choice(d, len(d)))
        stats[b] = np.mean(vals)
    return [float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))]


def contrast(U, a, b, measure, kind=None):
    """Mean of (arm b - arm a) per paired unit, hierarchical-bootstrap CI, seed means."""
    by_seed = defaultdict(list)
    for (arm, seed), us in U.items():
        if arm != a or (b, seed) not in U:
            continue
        other = {u["api"]: u for u in U[(b, seed)]}
        for u in us:
            if kind and u["kind"] != kind:
                continue
            by_seed[seed].append(other[u["api"]][measure] - u[measure])
    by_seed = {s: np.array(v, float) for s, v in by_seed.items()}
    allv = np.concatenate(list(by_seed.values()))
    return dict(mean=float(allv.mean()), ci=hboot(by_seed), n=int(allv.size),
                seed_means=[float(v.mean()) for v in by_seed.values()])


def verdict(c):
    lo = {m: c[m]["ci"][0] for m in MEASURES}
    hi = {m: c[m]["ci"][1] for m in MEASURES}
    faster = [m for m in MEASURES if lo[m] > 0]
    if faster and hi["recover"] >= 0 and not (faster == ["detect"] and lo["recover"] <= 0):
        return "KEEP"
    return "KILL"


def main():
    U, S = {}, {}
    for path in sorted((ROOT / "runs").glob("*.jsonl")):
        meta, eps, final = load(path)
        U[(meta["arm"], meta["seed"])] = units(meta, eps)
        S[(meta["arm"], meta["seed"])] = summary(meta, eps, final)
    arms = [a for a in ARMS if any(k[0] == a for k in U)]
    table = {}
    for a in arms:
        us = [u for (arm, _), v in U.items() if arm == a for u in v]
        ss = [s for (arm, _), s in S.items() if arm == a]
        row = {m: float(np.mean([u[m] for u in us])) for m in MEASURES}
        for kind in ["breaking", "silent"]:
            for m in MEASURES:
                row[f"{m}_{kind}"] = float(np.mean([u[m] for u in us if u["kind"] == kind]))
        row["detect_censored"] = sum(u["detect_censored"] for u in us)
        row["recover_censored"] = sum(u["recover_censored"] for u in us)
        row["silent_wrong"] = float(np.mean([u["silent_wrong"] for u in us]))
        row["uses"] = float(np.mean([u["uses"] for u in us]))
        for k in ["pre_acc", "post_undrifted_acc", "false_flags", "llm_calls", "tokens"]:
            vals = [s[k] for s in ss if s[k] is not None]
            row[k] = float(np.mean(vals)) if vals else None
        table[a] = row
    contrasts = {}
    pairs = [("tool+tests", "lesson+tests"), ("tool", "lesson"), ("tool", "tool+tests"), ("lesson", "lesson+tests")]
    pairs += [(a, "none") for a in ARMS[:4]]
    for a, b in pairs:
        if any((b, s) in U for (x, s) in U if x == a):
            contrasts[f"{b} - {a}"] = {m: contrast(U, a, b, m) for m in MEASURES}
            for kind in ["breaking", "silent"]:
                contrasts[f"{b} - {a} [{kind}]"] = {m: contrast(U, a, b, m, kind) for m in MEASURES}
    primary = contrasts.get("lesson+tests - tool+tests")
    result = dict(table=table, contrasts=contrasts, verdict=verdict(primary) if primary else None,
                  units={f"{a}|{s}": v for (a, s), v in U.items()},
                  runs={f"{a}|{s}": v for (a, s), v in S.items()})
    (ROOT / "results.json").write_text(json.dumps(result, indent=1))
    print("arm | detect | recover | detect brk/sil | recover brk/sil | censored det/rec | silent-wrong | pre acc | false flags | LLM calls")
    for a, r in table.items():
        print(f"{a} | {r['detect']:.2f} | {r['recover']:.2f} | {r['detect_breaking']:.2f}/{r['detect_silent']:.2f} | "
              f"{r['recover_breaking']:.2f}/{r['recover_silent']:.2f} | {r['detect_censored']}/{r['recover_censored']} | "
              f"{r['silent_wrong']:.2f} | {r['pre_acc']:.3f} | {r['false_flags']:.1f} | {r['llm_calls']}")
    for k, c in contrasts.items():
        print(k, {m: (round(c[m]["mean"], 2), [round(x, 2) for x in c[m]["ci"]], [round(x, 2) for x in c[m]["seed_means"]]) for m in MEASURES})
    print("VERDICT", result["verdict"])


if __name__ == "__main__":
    main()
