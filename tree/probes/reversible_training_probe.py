"""Reversible-training probe (numpy, CPU, ~1 min).

Question: if training itself is made exactly invertible, what does that buy continual
learning, and what does it cost?

Host: 2-24-1 tanh MLP, MSE. Tasks A, B, C: three random tanh teachers on the same inputs
(strong interference); A and B get 400 steps, C gets 100 so B is only partly overwritten. Optimizer: heavy-ball SGD in fixed-point integers made bit-exactly
invertible (Maclaurin et al. 2015): v <- floor(v*n/d) - g, w <- w + floor(lr*v); the
remainder (v*n mod d) of every multiply goes to a tape. Reversal recomputes g at the
restored w, so it also needs each step's minibatch (index tape + retained data).

R1  Exact rewind: after A->B->C, run C then B backwards; report whether weights equal theta_A
    bit for bit, tape bits (naive log2 d, entropy-optimal log2(d/n), batch indices) vs one
    fp32 checkpoint.
R2  Selective undo of B while keeping C (target: the counterfactual theta_AC trained on the
    same A and C streams). Arms: exact reverse C, reverse B, replay C (exact, 2|C|+|B| steps,
    needs B and C data); out-of-order gradient ascent on B's logged batches at the current
    weights (|B| steps); task-vector negation theta - (theta_AB - theta_A); keep (do nothing).
R3  Friction sweep: beta in {1/2, 9/10, 99/100} at matched effective step lr/(1-beta). Old-task
    A loss after B vs the tape rate log2(1/beta) per parameter-step. Tests whether storing
    more of the trajectory (less erasure) itself buys retention.
"""
import numpy as np

H, NX, B, STEPS, STEPS_C, WORLDS, R = 24, 512, 32, 400, 100, 10, 2 ** 24


def teacher(r):
    W, u = r.standard_normal((8, 2)) * 1.5, r.standard_normal(8)
    return lambda X: np.tanh(X @ W.T) @ u / np.sqrt(8)


def make_world(seed):
    r = np.random.default_rng(seed)
    X = r.uniform(-1, 1, (NX, 2))
    Xe = r.uniform(-1, 1, (1024, 2))
    tasks = {}
    for k in "ABC":
        f = teacher(r)
        tasks[k] = (X, f(X), Xe, f(Xe))
    w0 = np.concatenate([r.standard_normal(2 * H) / np.sqrt(2), np.zeros(H), r.standard_normal(H) / np.sqrt(H)])
    streams = {k: r.integers(0, NX, (STEPS if k != "C" else STEPS_C, B)) for k in "ABC"}
    return tasks, w0, streams


def unpack(w):
    return w[:2 * H].reshape(H, 2), w[2 * H:3 * H], w[3 * H:]


def loss_grad(w, X, y):
    W, b, u = unpack(w)
    h = np.tanh(X @ W.T + b)
    e = h @ u - y
    dh = np.outer(e, u) * (1 - h ** 2)
    g = np.concatenate([(dh.T @ X).ravel(), dh.sum(0), h.T @ e]) / len(y)
    return 0.5 * np.mean(e ** 2), g


def loss(w, task):
    return loss_grad(w, task[2], task[3])[0]


class RevSGD:
    """Bit-exact invertible heavy-ball SGD on int64 fixed-point state."""

    def __init__(self, n, d, lr_num, lr_den):
        self.n, self.d, self.ln, self.ld = n, d, lr_num, lr_den
        self.tape = []

    def g_int(self, w, task, idx):
        X, y = task[0][idx], task[1][idx]
        return np.round(loss_grad(w / R, X, y)[1] * R).astype(np.int64)

    def fwd(self, w, v, task, idx):
        g = self.g_int(w, task, idx)
        vn = v * self.n
        self.tape.append((vn % self.d).astype(np.uint8))
        v = vn // self.d - g
        w = w + (v * self.ln) // self.ld
        return w, v

    def rev(self, w, v, task, idx):
        w = w - (v * self.ln) // self.ld
        g = self.g_int(w, task, idx)
        r = self.tape.pop().astype(np.int64)
        vn = (v + g) * self.d + r
        assert np.all(vn % self.n == 0)
        return w, vn // self.n


def train(opt, w, v, task, stream, sign=1):
    for idx in stream:
        w, v = opt.fwd(w, v, task, idx)
    return w, v


def float_sgd(w, task, stream, lr, beta, sign=1.0, clip=None):
    v = np.zeros_like(w)
    for idx in stream:
        g = loss_grad(w, task[0][idx], task[1][idx])[1]
        if clip is not None:
            g = g * min(1.0, clip / (np.linalg.norm(g) + 1e-12))
        v = beta * v - sign * g
        w = w + lr * v
    return w


def main():
    n, d, ln, ld = 9, 10, 1, 20  # beta 0.9, lr 0.05
    P = 5 * H
    res = {k: [] for k in ["exact", "keep", "ascent", "negate", "rr_steps"]}
    tapebits = None
    for s in range(WORLDS):
        tasks, w0f, st = make_world(s)
        opt = RevSGD(n, d, ln, ld)
        w0 = np.round(w0f * R).astype(np.int64)
        v0 = np.zeros_like(w0)
        wA, vA = train(opt, w0, v0, tasks["A"], st["A"])
        wB, vB = train(opt, wA, vA, tasks["B"], st["B"])
        wC, vC = train(opt, wB, vB, tasks["C"], st["C"])
        # R1 exact rewind
        w, v = wC, vC
        for idx in st["C"][::-1]:
            w, v = opt.rev(w, v, tasks["C"], idx)
        for idx in st["B"][::-1]:
            w, v = opt.rev(w, v, tasks["B"], idx)
        exact = np.array_equal(w, wA) and np.array_equal(v, vA)
        if s == 0:
            steps = 2 * STEPS + STEPS_C
            tapebits = dict(naive=P * steps * np.log2(d), optimal=P * steps * np.log2(d / n),
                            index=steps * B * np.log2(NX), ckpt=2 * P * 32)
            print(f"R1 exact rewind to theta_A: {exact}; params {P}, steps {steps}")
            print("   tape bits: remainders naive %.0f, entropy-optimal %.0f, batch index %.0f; one fp32 (w,v) checkpoint %d"
                  % (tapebits["naive"], tapebits["optimal"], tapebits["index"], tapebits["ckpt"]))
            print("   per step: optimal remainder bits %.1f vs checkpoint %d -> rewind tape beats storing a checkpoint every"
                  " step but equals one checkpoint every %.0f steps (plus index tape and retained data)"
                  % (P * np.log2(d / n), 2 * P * 32, 2 * P * 32 / (P * np.log2(d / n))))
        res["exact"].append(exact)
        # R2 selective undo of B keeping C. Counterfactual: A then C on the same streams.
        opt2 = RevSGD(n, d, ln, ld)
        wAC, _ = train(opt2, wA, vA, tasks["C"], st["C"])
        # exact reverse-replay: from wA (just recovered) replay C
        wRR, _ = train(RevSGD(n, d, ln, ld), w, v, tasks["C"], st["C"])
        assert np.array_equal(wRR, wAC)
        fA, fB, fC, fAC = wA / R, wB / R, wC / R, wAC / R
        arms = {
            "keep": fC,
            "ascent": float_sgd(fC, tasks["B"], st["B"][::-1], ln / ld, 0.0, sign=-1.0, clip=1.0),
            "negate": fC - (fB - fA),
            "exact": fAC,
        }
        if s == 0:
            print("   reference losses: theta_A L_A %.4f; theta_AB L_A %.4f L_B %.4f" % (loss(fA, tasks["A"]), loss(fB, tasks["A"]), loss(fB, tasks["B"])))
        for k, wk in arms.items():
            res.setdefault(k + "_m", []).append((loss(wk, tasks["A"]), loss(wk, tasks["B"]), loss(wk, tasks["C"]),
                                                 np.linalg.norm(wk - fAC) / np.linalg.norm(fAC - fA)))
    print(f"   exact in {sum(res['exact'])}/{WORLDS} worlds")
    print("R2 selective undo of B keeping C (mean over %d worlds; dist = ||w-theta_AC||/||theta_AC-theta_A||)" % WORLDS)
    print("   %-8s %8s %8s %8s %8s  cost" % ("arm", "L_A", "L_B", "L_C", "dist"))
    cost = {"keep": "0", "ascent": "|B| steps (clipped, no momentum), B data", "negate": "theta_A,theta_AB stored",
            "exact": "2|C|+|B| steps, B+C data + tape"}
    for k in ["keep", "ascent", "negate", "exact"]:
        m = np.array(res[k + "_m"]).mean(0)
        print("   %-8s %8.4f %8.4f %8.4f %8.3f  %s" % (k, *m, cost[k]))
    # R3 friction sweep
    print("R3 friction sweep: A loss after A->B at matched lr/(1-beta)=0.5 (float SGD, %d worlds)" % WORLDS)
    for beta in [0.5, 0.9, 0.99]:
        lr = 0.5 * (1 - beta)
        la, lb, la0 = [], [], []
        for s in range(WORLDS):
            tasks, w0f, st = make_world(s)
            wA = float_sgd(w0f, tasks["A"], st["A"], lr, beta)
            wB = float_sgd(wA, tasks["B"], st["B"], lr, beta)
            la0.append(loss(wA, tasks["A"])); la.append(loss(wB, tasks["A"])); lb.append(loss(wB, tasks["B"]))
        print("   beta %.2f tape %.3f bits/param-step  L_A after A %.4f  L_A after B %.4f  L_B %.4f"
              % (beta, np.log2(1 / beta), np.mean(la0), np.mean(la), np.mean(lb)))


if __name__ == "__main__":
    main()
