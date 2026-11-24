"""Practice-order interference probe (numpy, CPU, ~3 min).

Question: at a fixed practice mixture (equal steps per task), does the ORDER of practice set
old-task retention, and is that effect transient (linear-in-parameters hosts) or permanent
(feature-learning hosts)?

World: K tasks, inputs from overlapping random subspaces, each task has its own nonlinear
(tanh) teacher derived from a shared one, so tasks conflict on shared directions.
Hosts:
  lin  linear regression on x                          (linear in params, linear in x)
  rf   frozen random ReLU features + trained readout   (linear in params, nonlinear in x)
  mlp  ReLU MLP, both layers trained                   (nonlinear in params)
Competence C_k = 1 - L_k(theta) / L_k(theta_0) on a fixed eval set.

Q1  Hysteresis. Phase 1 (N1 steps, equal histogram): blocked A->B->C->D, blocked reverse,
    or shuffled. Phase 2 (N2 steps): every arm gets the SAME shuffled uniform practice
    (same minibatch stream). Order gap = mean |C_fwd - C_rev| at end of phase 2, against a
    seed floor = same phase-1 order but a different phase-1 minibatch stream.
Q2  Granularity at fixed mixture. Periodic schedules with block length b (equal histogram);
    time-averaged mean and worst-task competence over the last half.
Q1b Relaxation (mlp). Blocked-fwd vs shuffled phase 1, then N2 in {4000, 12000} shared
    shuffled steps; worst- and mean-task difference against a shuffled-vs-shuffled floor.
Q4  Capacity (mlp, H in {4, 8}, N2 = 12000). Fwd-vs-rev order gap after re-mixing vs seed floor,
    to separate slow relaxation from permanent hysteresis.
Q3  Mechanism (mlp). Unit-task ownership matrix A_jk = |v_j| * E_k[relu(h_j)]; correlation
    of ownership between fwd and rev arms after phase 2 vs the seed floor.
"""
import numpy as np

D, K, SUB, H, B = 16, 4, 8, 64, 16
N1, N2, WORLDS = 2000, 4000, 16
LR = {"lin": 0.02, "rf": 0.02, "mlp": 0.02}


def make_world(seed):
    r = np.random.default_rng(seed)
    bases = [np.linalg.qr(r.standard_normal((D, SUB)))[0] for _ in range(K)]
    W0, u0 = r.standard_normal((8, D)) / np.sqrt(SUB), r.standard_normal(8)
    teach = [(W0 + 0.8 * r.standard_normal((8, D)) / np.sqrt(SUB), u0 + 0.8 * r.standard_normal(8))
             for _ in range(K)]
    evals = []
    for k in range(K):
        X = r.standard_normal((400, SUB)) @ bases[k].T
        evals.append((X, target(teach[k], X)))
    rf = (r.standard_normal((H, D)) / np.sqrt(D), 0.1 * r.standard_normal(H))
    init = dict(W=r.standard_normal((H, D)) / np.sqrt(D), c=np.zeros(H),
                v=r.standard_normal(H) / np.sqrt(H))
    return dict(bases=bases, teach=teach, evals=evals, rf=rf, init=init)


def target(t, X):
    W, u = t
    return np.tanh(X @ W.T) @ u


def init_params(host, world):
    if host == "lin":
        return dict(a=np.zeros(D))
    if host == "rf":
        return dict(v=np.zeros(H))
    p = world["init"]
    return {k: v.copy() for k, v in p.items()}


def forward(host, p, world, X):
    if host == "lin":
        return X @ p["a"], None
    if host == "rf":
        Wr, cr = world["rf"]
        Z = np.maximum(X @ Wr.T + cr, 0)
        return Z @ p["v"], Z
    Hh = X @ p["W"].T + p["c"]
    Z = np.maximum(Hh, 0)
    return Z @ p["v"], (Hh, Z)


def step(host, p, world, X, y, lr):
    out, cache = forward(host, p, world, X)
    e = 2 * (out - y) / len(y)
    if host == "lin":
        p["a"] -= lr * X.T @ e
    elif host == "rf":
        p["v"] -= lr * cache.T @ e
    else:
        Hh, Z = cache
        gv = Z.T @ e
        gH = np.outer(e, p["v"]) * (Hh > 0)
        p["W"] -= lr * gH.T @ X
        p["c"] -= lr * gH.sum(0)
        p["v"] -= lr * gv


def losses(host, p, world):
    return np.array([np.mean((forward(host, p, world, X)[0] - y) ** 2) for X, y in world["evals"]])


def batch(world, k, r):
    X = r.standard_normal((B, SUB)) @ world["bases"][k].T
    return X, target(world["teach"][k], X) + 0.05 * r.standard_normal(B)


def schedule(kind, n, r, b=None):
    if kind == "fwd":
        return np.repeat(np.arange(K), n // K)
    if kind == "rev":
        return np.repeat(np.arange(K)[::-1], n // K)
    if kind == "shuf":
        s = np.repeat(np.arange(K), n // K)
        r.shuffle(s)
        return s
    if kind == "period":
        return np.tile(np.repeat(np.arange(K), b), n // (K * b) + 1)[:n]


def run(host, world, order, s1, s2=777, track=False, n1=N1, n2=N2, b=None):
    p = init_params(host, world)
    L0 = losses(host, p, world)
    r1 = np.random.default_rng(s1)
    sched1 = schedule(order, n1, np.random.default_rng(s1 + 1), b)
    traj = []
    for t, k in enumerate(sched1):
        step(host, p, world, *batch(world, k, r1), LR[host])
        if track and t % 20 == 0:
            traj.append(1 - losses(host, p, world) / L0)
    C1 = 1 - losses(host, p, world) / L0
    r2 = np.random.default_rng(s2)
    sched2 = schedule("shuf", n2, np.random.default_rng(s2 + 1))
    for k in sched2:
        step(host, p, world, *batch(world, k, r2), LR[host])
    C2 = 1 - losses(host, p, world) / L0
    return C1, C2, p, (np.array(traj) if track else None)


def ownership(p, world):
    A = np.zeros((H, K))
    for k, (X, _) in enumerate(world["evals"]):
        A[:, k] = np.abs(p["v"]) * np.maximum(X @ p["W"].T + p["c"], 0).mean(0)
    return A / (A.sum(1, keepdims=True) + 1e-12)


def ci(x):
    x = np.asarray(x)
    return f"{x.mean():+.3f} ± {1.96 * x.std(ddof=1) / np.sqrt(len(x)):.3f}"


def main():
    print("Q1 hysteresis: order gap after identical shuffled phase 2 vs seed floor")
    print("host | gap end ph1 | gap end ph2 | seed floor ph2 | (gap-floor) ph2 | fwd-shuf worst ph2")
    own = {"gap": [], "floor": []}
    for host in ["lin", "rf", "mlp"]:
        g1, g2, f2, ws = [], [], [], []
        for w in range(WORLDS):
            world = make_world(w)
            Cf1, Cf2, pf, _ = run(host, world, "fwd", 100 + w)
            Cr1, Cr2, pr, _ = run(host, world, "rev", 100 + w)
            _, Cf2b, pfb, _ = run(host, world, "fwd", 5000 + w)
            _, Cs2, _, _ = run(host, world, "shuf", 100 + w)
            g1.append(np.abs(Cf1 - Cr1).mean())
            g2.append(np.abs(Cf2 - Cr2).mean())
            f2.append(np.abs(Cf2 - Cf2b).mean())
            ws.append(Cf2.min() - Cs2.min())
            if host == "mlp":
                Af, Ar, Ab = ownership(pf, world), ownership(pr, world), ownership(pfb, world)
                own["gap"].append(np.abs(Af - Ar).sum(1).mean())
                own["floor"].append(np.abs(Af - Ab).sum(1).mean())
        print(f"{host} | {ci(g1)} | {ci(g2)} | {ci(f2)} | {ci(np.array(g2) - np.array(f2))} | {ci(ws)}")
    print("\nQ1b mlp relaxation: blocked-fwd minus shuffled phase 1, after N2 shared shuffled steps")
    for n2 in [4000, 12000]:
        dw, dm, fl = [], [], []
        for w in range(WORLDS):
            world = make_world(w)
            _, Cf, _, _ = run("mlp", world, "fwd", 100 + w, n2=n2)
            _, Cs, _, _ = run("mlp", world, "shuf", 100 + w, n2=n2)
            _, Cs2, _, _ = run("mlp", world, "shuf", 5000 + w, n2=n2)
            dw.append(Cf.min() - Cs.min())
            dm.append(Cf.mean() - Cs.mean())
            fl.append(abs(Cs2.min() - Cs.min()))
        print(f"N2={n2} | worst {ci(dw)} | mean {ci(dm)} | |shuf-shuf'| worst floor {ci(fl)}")
    print("\nQ3 mlp unit-ownership L1 distance (0 = same allocation, 2 = disjoint), after phase 2")
    print(f"fwd vs rev {ci(own['gap'])} | same order, other minibatches {ci(own['floor'])}")

    print("\nQ4 mlp capacity: fwd-vs-rev gap after 12000 shared shuffled steps vs seed floor")
    global H
    for h in [4, 8]:
        H, g2, f2 = h, [], []
        for w in range(WORLDS):
            world = make_world(w)
            _, Cf, _, _ = run("mlp", world, "fwd", 100 + w, n2=12000)
            _, Cr, _, _ = run("mlp", world, "rev", 100 + w, n2=12000)
            _, Cb, _, _ = run("mlp", world, "fwd", 5000 + w, n2=12000)
            g2.append(np.abs(Cf - Cr).mean())
            f2.append(np.abs(Cf - Cb).mean())
        print(f"H={h} | gap {ci(g2)} | floor {ci(f2)} | gap-floor {ci(np.array(g2) - np.array(f2))}")
    H = 64

    print("\nQ2 granularity at fixed mixture (periodic block length b, 4000 steps, last half)")
    print("host | b | mean C | worst C")
    for host in ["lin", "rf", "mlp"]:
        for b in [1, 10, 100, 500]:
            m, wo = [], []
            for w in range(8):
                world = make_world(w)
                _, _, _, tr = run(host, world, "period", 300 + w, track=True, n1=4000, n2=0, b=b)
                h = tr[len(tr) // 2:]
                m.append(h.mean())
                wo.append(h.min(1).mean())
            print(f"{host} | {b} | {ci(m)} | {ci(wo)}")


if __name__ == "__main__":
    main()
