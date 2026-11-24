"""Replay-deadline probe (CPU, numpy only).

Old task A: a logistic classifier w* whose inputs live on coordinates 0..14 of
d = 30. The learner then trains on a stream of tasks B_j whose inputs live on
coordinates 10..29, so a joint solution exists but coordinates 10..14 are shared.
Each B teacher opposes w* on the shared block; weight decay erodes A-only
coordinates that B never touches. Window types are public: "mild" (conflict
0.3, lr 0.1) or "severe" (conflict 1.5, lr 0.5).

Self-replay ("exercise") is target-blind: snapshot the current model, then take
steps on fresh unlabeled inputs labelled by the snapshot. It stores no bytes of A.
A stored-label buffer arm replays true A labels at equal steps (target-aware).

Questions:
 1. Does self-replay have a deadline (helps before a severe window, locks in the
    damage after), while true-label replay has none?
 2. With a budget of K exercises, does a deadline forecast from public window
    types beat fixed spacing and a reactive drift trigger, and how far from the
    hindsight oracle?
 3. How much of a true-label replay's value does a self-replay at time t keep, as
    a function of the damage already done?
 4. Escrow: record self-labels before a severe window and replay them after it.
    Labels are held for one window; inputs are regenerated from a seed.
Run: python3 tree/probes/replay_deadline_probe.py  (several CPU-min; the K=4 hindsight oracle dominates)
"""
import itertools
import numpy as np

D, W, STEPS, BS, K = 30, 16, 12, 32, 4
WD = 0.05
TYPES = {"mild": (0.3, 0.1), "severe": (1.5, 0.5)}
A_DIMS, B_DIMS, SHARED = np.arange(0, 15), np.arange(10, 30), np.arange(10, 15)
P_SEVERE = 0.25
EX_STEPS, EX_LR = 40, 0.5


def unit(v):
    return v / np.linalg.norm(v)


def on(dims, z):
    x = np.zeros(z.shape[:-1] + (D,))
    x[..., dims] = z
    return x


def make_world(seed):
    r = np.random.default_rng(seed)
    ws = np.zeros(D)
    ws[A_DIMS] = r.standard_normal(len(A_DIMS))
    ws = unit(ws)
    types = ["severe" if r.random() < P_SEVERE else "mild" for _ in range(W)]
    teach, xs = [], []
    for t in types:
        c, _ = TYPES[t]
        u = np.zeros(D)
        u[B_DIMS] = r.standard_normal(len(B_DIMS)) / np.sqrt(len(B_DIMS))
        u[SHARED] = -c * ws[SHARED] / np.linalg.norm(ws[SHARED])
        teach.append(unit(u))
        xs.append(on(B_DIMS, r.standard_normal((STEPS, BS, len(B_DIMS)))))
    exx = on(A_DIMS, r.standard_normal((W + 1, EX_STEPS, BS, len(A_DIMS))))
    xte = on(A_DIMS, r.standard_normal((2000, len(A_DIMS))))
    xteb = on(B_DIMS, r.standard_normal((2000, len(B_DIMS))))
    w = np.zeros(D)
    xa = on(A_DIMS, r.standard_normal((512, len(A_DIMS))))
    ya = np.sign(xa @ ws)
    for _ in range(300):
        g = xa.T @ (-ya * sig(-ya * (xa @ w))) / len(xa)
        w -= 0.5 * g
    return dict(ws=ws, types=types, teach=teach, xs=xs, exx=exx, xte=xte, xteb=xteb, w0=w)


def sig(z):
    return 1 / (1 + np.exp(-np.clip(z, -40, 40)))


def sgd(w, x, y, lr, wd=None):
    g = x.T @ (-y * sig(-y * (x @ w))) / len(x)
    return w * (1 - lr * (WD if wd is None else wd)) - lr * g


def exercise(w, xb, true_ws=None):
    teacher = w.copy() if true_ws is None else true_ws
    for x in xb:
        w = sgd(w, x, np.sign(x @ teacher), EX_LR, wd=0.0)  # decay is charged per stream step only
    return w


def acc(w, u, xte):
    return np.mean(np.sign(xte @ w) == np.sign(xte @ u))


def run(world, schedule, policy=None, labelled=False, tau=None, inc=None, trace=False, escrow=None):
    """escrow: {replay_window: record_window}: labels recorded from the model at the
    start of record_window, replayed at the start of replay_window."""
    """schedule: set of window indices i; exercise happens just BEFORE window i.
    policy 'reactive'/'forecast' decides online instead."""
    w = world["w0"].copy()
    snap = w.copy()
    used, accs = 0, []
    probe = world["xte"][:500]
    recorded = {}
    for i in range(W):
        if escrow and i in escrow.values():
            recorded[i] = w.copy()
        if escrow and i in escrow:
            w = exercise(w, world["exx"][i], recorded[escrow[i]])
        do = False
        if policy is None:
            do = i in schedule
        elif used < K:
            drift = np.mean(np.sign(probe @ w) != np.sign(probe @ snap))
            if policy == "reactive":
                do = drift > tau
            elif policy == "forecast":
                do = drift + inc[world["types"][i]] > tau
        if do:
            w = exercise(w, world["exx"][i], world["ws"] if labelled else None)
            snap, used = w.copy(), used + 1
        _, lr = TYPES[world["types"][i]]
        u = world["teach"][i]
        for x in world["xs"][i]:
            w = sgd(w, x, np.sign(x @ u), lr)
        accs.append(acc(w, world["ws"], world["xte"]))
    if trace:
        return accs
    lastB = acc(w, world["teach"][-1], world["xteb"])
    return accs[-1], float(np.mean(accs)), lastB


def ci(a):
    a = np.asarray(a)
    return f"{a.mean():.3f} ± {1.96 * a.std(ddof=1) / np.sqrt(len(a)):.3f}"


def q3(test):
    """Single exercise at every window t: self-replay value vs true-label value."""
    pts = []
    for wd in test:
        base = run(wd, set(), trace=True)
        for t in range(W):
            s = run(wd, {t}, trace=True)
            l = run(wd, {t}, labelled=True, trace=True)
            pre = acc(wd["w0"], wd["ws"], wd["xte"]) if t == 0 else base[t - 1]
            vs = np.mean(np.array(s[t:]) - np.array(base[t:]))
            vl = np.mean(np.array(l[t:]) - np.array(base[t:]))
            pts.append((pre, vs, vl))
    pts = np.array(pts)
    print("Q3 single exercise, binned by A acc at exercise time: n | self value | label value | self/label")
    for lo, hi in [(0.9, 1.01), (0.8, 0.9), (0.7, 0.8), (0.6, 0.7), (0.5, 0.6), (0.0, 0.5)]:
        m = (pts[:, 0] >= lo) & (pts[:, 0] < hi)
        if m.sum() < 5:
            continue
        vs, vl = pts[m, 1], pts[m, 2]
        print(f"  acc [{lo:.1f},{hi:.1f}) n={m.sum():3d} | {ci(vs)} | {ci(vl)} | {vs.mean() / vl.mean():.2f}")


def q4(test):
    """Record self-labels before a severe window, replay them after it."""
    rows = {k: [] for k in ["none", "self_before", "self_after", "escrow", "label_after"]}
    for wd in test:
        sev = [i for i, t in enumerate(wd["types"]) if t == "severe" and 0 < i < W - 1]
        if not sev:
            continue
        s = sev[0]
        rows["none"].append(run(wd, set())[1])
        rows["self_before"].append(run(wd, {s})[1])
        rows["self_after"].append(run(wd, {s + 1})[1])
        rows["escrow"].append(run(wd, set(), escrow={s + 1: s})[1])
        rows["label_after"].append(run(wd, {s + 1}, labelled=True)[1])
    print(f"Q4 record-before / replay-after (n={len(rows['none'])}; mean A acc over windows)")
    for k, v in rows.items():
        print(f"  {k:12s} {ci(v)}")
    e, sa, la = (np.array(rows[k]) for k in ["escrow", "self_after", "label_after"])
    print(f"  escrow-self_after {ci(e - sa)}  label_after-escrow {ci(la - e)}")
    # budgeted: record before each of the first K severe windows, replay after it
    res = {k: [] for k in ["fixed", "escrow_K"]}
    fixed = set(np.linspace(0, W - 1, K + 2)[1:-1].round().astype(int).tolist())
    for wd in test:
        sev = [i for i, t in enumerate(wd["types"]) if t == "severe" and i < W - 1][:K]
        res["fixed"].append(run(wd, fixed)[:3])
        res["escrow_K"].append(run(wd, set(), escrow={i + 1: i for i in sev})[:3])
    f, ek = np.array(res["fixed"]), np.array(res["escrow_K"])
    print(f"  budget K={K}: fixed self {ci(f[:, 1])}  escrow_K {ci(ek[:, 1])}  diff {ci(ek[:, 1] - f[:, 1])}")
    print(f"  last-B acc: fixed self {ci(f[:, 2])}  escrow_K {ci(ek[:, 2])}")


def main():
    cal = [make_world(s) for s in range(1000, 1010)]
    test = [make_world(s) for s in range(30)]

    # Q1: single exercise right before vs right after the first severe window
    rows = {"self_before": [], "self_after": [], "label_before": [], "label_after": [], "none": []}
    for wd in test:
        sev = [i for i, t in enumerate(wd["types"]) if t == "severe" and 0 < i < W - 1]
        if not sev:
            continue
        s = sev[0]
        rows["none"].append(run(wd, set())[1])
        rows["self_before"].append(run(wd, {s})[1])
        rows["self_after"].append(run(wd, {s + 1})[1])
        rows["label_before"].append(run(wd, {s}, labelled=True)[1])
        rows["label_after"].append(run(wd, {s + 1}, labelled=True)[1])
    print(f"Q1 (n={len(rows['none'])} worlds; mean A acc over windows)")
    for k, v in rows.items():
        print(f"  {k:13s} {ci(v)}")
    d_self = np.array(rows["self_before"]) - np.array(rows["self_after"])
    d_lab = np.array(rows["label_before"]) - np.array(rows["label_after"])
    print(f"  before-after gap: self {ci(d_self)}  label {ci(d_lab)}")

    q3(test)
    q4(test)

    # Calibrate per-type drift increment and thresholds on calibration worlds
    inc = {t: [] for t in TYPES}
    for wd in cal:
        w = wd["w0"].copy()
        p = wd["xte"][:500]
        for i in range(W):
            before = np.sign(p @ w)
            _, lr = TYPES[wd["types"][i]]
            for x in wd["xs"][i]:
                w = sgd(w, x, np.sign(x @ wd["teach"][i]), lr)
            inc[wd["types"][i]].append(np.mean(np.sign(p @ w) != before))
    inc = {t: float(np.mean(v)) for t, v in inc.items()}
    taus = np.linspace(0.0, 0.3, 31)

    def best_tau(policy):
        sc = [np.mean([run(wd, set(), policy, tau=t, inc=inc)[1] for wd in cal]) for t in taus]
        return float(taus[int(np.argmax(sc))])

    tr, tf = best_tau("reactive"), best_tau("forecast")
    print(f"calibrated: inc={ {k: round(v, 3) for k, v in inc.items()} } tau_reactive={tr:.2f} tau_forecast={tf:.2f}")

    res = {k: [] for k in ["none", "fixed", "before_severe", "reactive", "forecast", "oracle", "label_fixed"]}
    combos = list(itertools.combinations(range(W), K))
    fixed = set(np.linspace(0, W - 1, K + 2)[1:-1].round().astype(int).tolist())
    for wd in test:
        res["none"].append(run(wd, set()))
        res["fixed"].append(run(wd, fixed))
        sev = [i for i, t in enumerate(wd["types"]) if t == "severe"][:K]
        res["before_severe"].append(run(wd, set(sev)))
        res["reactive"].append(run(wd, set(), "reactive", tau=tr))
        res["forecast"].append(run(wd, set(), "forecast", tau=tf, inc=inc))
        res["label_fixed"].append(run(wd, fixed, labelled=True))
        best = max((run(wd, set(c)) for c in combos), key=lambda r: r[1])
        res["oracle"].append(best)
    print(f"Q2 (n={len(test)} worlds, K={K}): final A acc | mean A acc over windows | last-B acc")
    for k, v in res.items():
        v = np.array(v)
        print(f"  {k:13s} {ci(v[:, 0])} | {ci(v[:, 1])} | {ci(v[:, 2])}")
    f, r_ = np.array(res["forecast"])[:, 1], np.array(res["reactive"])[:, 1]
    print(f"  forecast-reactive (mean A): {ci(f - r_)}")
    print(f"  forecast-fixed    (mean A): {ci(f - np.array(res['fixed'])[:, 1])}")


if __name__ == "__main__":
    main()
