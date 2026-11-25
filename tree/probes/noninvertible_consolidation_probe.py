"""CPU probe for tree/non-invertible-consolidation.md (NumPy only, ~1 min).

Part 1 (linear, exact): invertible GD (+weight decay) shrinks the gap between two
histories geometrically but never closes it; a soft-threshold (prox) step or a
designed projection closes it in finite steps; float32 rounding also merges.

Part 2 (ReLU MLP): shared task A, then history-specific task B1 or B2 (with A
replay). Consolidation operators are compared on: A-loss change, history gap
after a shared continuation on a new task C, savings when relearning the
erased task B, and C acquisition.
"""
import numpy as np

rng0 = np.random.default_rng(0)

# ---------------- Part 1: linear, exact ----------------
def part1():
    d = 8
    lam = np.array([1.0, 0.5, 0.1, 0.01, 0.0, 0.0, 0.0, 0.0])  # Hessian eigenvalues (flat dirs = 0)
    eta, wd = 0.5, 1e-3
    w1 = rng0.normal(size=d); w2 = w1.copy(); w2[4:] += rng0.normal(size=d - 4)  # histories differ only in flat dirs
    out = {}
    for name in ["gd", "gd+wd", "prox_l1", "float32_gd+wd"]:
        a, b = w1.copy(), w2.copy()
        if name == "float32_gd+wd":
            a, b = a.astype(np.float32), b.astype(np.float32)
        merged_at = None; below = None
        for t in range(1, 200001):
            for v in (a, b):
                g = lam.astype(v.dtype) * v
                if name == "gd":
                    v -= eta * g
                elif name.endswith("gd+wd"):
                    v -= v.dtype.type(eta) * (g + v.dtype.type(wd) * v)
                else:  # proximal L1: v <- soft(v - eta g, eta*mu), non-invertible on [-eta mu, eta mu]
                    v -= eta * g
                    np.copyto(v, np.sign(v) * np.maximum(np.abs(v) - eta * 1e-3, 0))
            gap = float(np.abs(a.astype(np.float64) - b).max())
            if below is None and gap < 1e-6:
                below = t
            if np.array_equal(a, b):
                merged_at = t; break
        out[name] = (merged_at, below, gap)
    # designed projection: keep the span read by the old task (lam>0), reset the rest to a canonical anchor 0
    P = np.diag((lam > 0).astype(float))
    a, b = P @ w1, P @ w2
    out["designed_projection(1 step)"] = (1 if np.array_equal(a, b) else None, 1, float(np.abs(a - b).max()))
    w3 = w1.copy(); w3[3] += 1.0  # history difference in a direction the old task reads (lam=0.01)
    out["projection, diff in read dir"] = (None, None, float(np.abs(P @ w1 - P @ w3).max()))
    print("Part 1: steps until two histories become identical / gap<1e-6 (None = not within 200k steps)")
    for k, (t, b, gap) in out.items():
        print(f"  {k:30s} identical_at={t}  gap<1e-6_at={b}  final max|gap|={gap:.3g}")

# ---------------- Part 2: ReLU MLP ----------------
D, H = 16, 48
def mlp_init(rng):
    return [rng.normal(size=(H, D)) / np.sqrt(D), np.zeros(H), rng.normal(size=(1, H)) / np.sqrt(H), np.zeros(1)]

def fwd(p, X):
    z = X @ p[0].T + p[1]; h = np.maximum(z, 0)
    return (h @ p[2].T + p[3])[:, 0], h, z

def loss(p, X, y):
    return float(np.mean((fwd(p, X)[0] - y) ** 2))

def step(p, X, y, lr, wd=0.0):
    f, h, z = fwd(p, X); n = len(y); e = 2 * (f - y)[:, None] / n
    gW2 = e.T @ h; gb2 = e.sum(0); dh = e @ p[2] * (z > 0)
    gW1 = dh.T @ X; gb1 = dh.sum(0)
    for q, g in zip(p, [gW1, gb1, gW2, gb2]):
        q -= lr * (g + wd * q)

def train(p, batches, steps, lr=0.05, wd=0.0):
    for t in range(steps):
        X, y = batches[t % len(batches)]
        step(p, X, y, lr, wd)

def task(rng, dims, n=256):
    X = np.zeros((n, D)); X[:, dims] = rng.normal(size=(n, len(dims)))
    a = rng.normal(size=len(dims)); b = rng.normal(size=len(dims))
    y = np.tanh(X[:, dims] @ a) + 0.5 * np.sin(X[:, dims] @ b)
    return X, y

def steps_to(p, X, y, thr, lr=0.05, cap=3000):
    q = [x.copy() for x in p]
    for t in range(cap):
        if loss(q, X, y) < thr: return t
        step(q, X, y, lr)
    return cap

def proj_onto_rows(M, tol=1e-3):
    U, s, Vt = np.linalg.svd(M, full_matrices=False)
    k = int(np.searchsorted(np.cumsum(s ** 2) / np.sum(s ** 2), 1 - tol) + 1)
    V = Vt[:k]
    return V.T @ V

def op_span_projection(p, XA, tol, anchor):
    """Designed non-invertible step: keep weight components read by task-A activations, reset the rest to the anchor."""
    q = [x.copy() for x in p]
    Pin = proj_onto_rows(XA, tol)
    q[0] = q[0] @ Pin + anchor[0] @ (np.eye(D) - Pin)
    h = fwd(q, XA)[1]
    Ph = proj_onto_rows(np.hstack([h, np.ones((len(h), 1))]), tol)[:H, :H]
    q[2] = q[2] @ Ph + anchor[2] @ (np.eye(H) - Ph)
    return q

def op_wd(p, steps, XA, yA, wd=0.02):
    q = [x.copy() for x in p]
    for _ in range(steps):
        step(q, XA, yA, 0.05, wd)
    return q

def op_prune(p, frac):
    q = [x.copy() for x in p]
    for i in (0, 2):
        thr = np.quantile(np.abs(q[i]), frac); q[i][np.abs(q[i]) < thr] = 0
    return q

def op_unlearn_ga(p, XB, yB, XA, yA, steps):
    """Invertible-style unlearning control: fit B to random targets while replaying A."""
    q = [x.copy() for x in p]; r = np.random.default_rng(7).normal(size=len(yB)) * yB.std()
    for _ in range(steps):
        step(q, XB, r, 0.05); step(q, XA, yA, 0.05)
    return q

def part2(seed):
    rng = np.random.default_rng(seed)
    A = task(rng, list(range(0, 6)))
    B1 = task(rng, list(range(6, 11)))
    B2 = task(rng, list(range(11, 16)))
    C = task(rng, list(range(0, 16)))
    Xprobe = rng.normal(size=(512, D))
    init = mlp_init(rng)
    anchor = [x.copy() for x in init]
    base = [x.copy() for x in init]; train(base, [A], 600)
    hist = {}
    for name, B in (("h1", B1), ("h2", B2)):
        p = [x.copy() for x in base]; train(p, [B, A], 1200); hist[name] = p
    # a learner that never saw any B (null for savings)
    never = [x.copy() for x in base]; train(never, [A, A], 1200)
    XA, yA = A
    lossA0 = {k: loss(v, *A) for k, v in hist.items()}
    ops = {
        "none": lambda p: [x.copy() for x in p],
        "wd x200": lambda p: op_wd(p, 200, XA, yA),
        "prune 50%": lambda p: op_prune(p, 0.5),
        "unlearnB(GA-like) x300": None,
        "span-proj tol1e-3": lambda p: op_span_projection(p, XA, 1e-3, anchor),
        "span-proj tol1e-2": lambda p: op_span_projection(p, XA, 1e-2, anchor),
    }
    res = {}
    for name, op in ops.items():
        out = {}
        for k, p in hist.items():
            B = B1 if k == "h1" else B2
            out[k] = op_unlearn_ga(p, *B, XA, yA, 300) if op is None else op(p)
        nv = op_unlearn_ga(never, *B1, XA, yA, 300) if op is None else op(never)
        dA = np.mean([loss(out[k], *A) - lossA0[k] for k in out])
        # history gap after a shared continuation on C (future edit)
        gaps = []
        for T in (0, 50):
            c = {k: [x.copy() for x in v] for k, v in out.items()}
            for v in c.values(): train(v, [C], T)
            gaps.append(float(np.sqrt(np.mean((fwd(c["h1"], Xprobe)[0] - fwd(c["h2"], Xprobe)[0]) ** 2))))
        # savings on erased task B1 for history h1, vs a learner that never saw B1 under the same operator
        thr = 0.5 * np.var(B1[1])
        sav = steps_to(nv, *B1, thr) - steps_to(out["h1"], *B1, thr)
        lossB1 = loss(out["h1"], *B1) / np.var(B1[1])
        cs = steps_to(out["h1"], *C, 0.5 * np.var(C[1]))
        gapA = float(np.sqrt(np.mean((fwd(out["h1"], XA)[0] - fwd(out["h2"], XA)[0]) ** 2)))
        res[name] = (dA, gapA, gaps[0], gaps[1], lossB1, sav, cs)
    return res

if __name__ == "__main__":
    part1()
    allr = [part2(s) for s in range(5)]
    print("\nPart 2: ReLU MLP 16-48-1, 5 seeds (mean [min,max])")
    print("  columns: dLossA | gap on A inputs | gap@0 (probe inputs) | gap after 50 C-steps | B1 loss/var | B1 relearn savings (steps vs never-saw-B) | steps to learn C")
    for name in allr[0]:
        cols = np.array([r[name] for r in allr])
        s = " | ".join(f"{m:+.3f}[{lo:+.2f},{hi:+.2f}]" for m, lo, hi in zip(cols.mean(0), cols.min(0), cols.max(0)))
        print(f"  {name:24s} {s}")
