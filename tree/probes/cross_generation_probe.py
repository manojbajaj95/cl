"""Toy cross-generation inheritance probe; run with python3 and NumPy.

Old base B0 learns world W0. Fine-tune F0 = B0 + skill S on region Q.
New base B1 learns W1, which corrects W0 on region R (R overlaps Q).
B1 must inherit S from F0 with no S data, only unlabeled generic inputs.
"""

import numpy as np

SEEDS = range(8)
D, H, K = 12, 64, 6


def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


class MLP:
    def __init__(self, rng):
        self.W1 = rng.normal(0, 1 / np.sqrt(D), (D, H))
        self.b1 = np.zeros(H)
        self.W2 = rng.normal(0, 1 / np.sqrt(H), (H, K))
        self.b2 = np.zeros(K)

    def copy(self):
        m = MLP.__new__(MLP)
        m.W1, m.b1, m.W2, m.b2 = (a.copy() for a in (self.W1, self.b1, self.W2, self.b2))
        return m

    def logits(self, x):
        self.x, self.h = x, np.maximum(x @ self.W1 + self.b1, 0)
        return self.h @ self.W2 + self.b2

    def step(self, x, target, lr=0.1, weight=None):
        p = softmax(self.logits(x))
        g = p - target
        if weight is not None:
            g = g * weight[:, None]
        g /= len(x)
        gh = (g @ self.W2.T) * (self.h > 0)
        self.W2 -= lr * self.h.T @ g
        self.b2 -= lr * g.sum(0)
        self.W1 -= lr * x.T @ gh
        self.b1 -= lr * gh.sum(0)

    def train(self, sample, steps=3000, batch=128, lr=0.1):
        for _ in range(steps):
            x, t, w = sample(batch)
            self.step(x, t, lr, w)

    def pred(self, x):
        return self.logits(x).argmax(1)


def world(rng):
    A = rng.normal(size=(D, K))
    shift = np.roll(np.arange(K), rng.integers(1, K))   # derangement: W1 always differs on R
    skill = rng.normal(size=(D, K))
    in_R = lambda x: x[:, 0] > 0.4                     # region W1 corrects
    in_Q = lambda x: x[:, 1] > 0.6                     # region where skill S lives
    w0 = lambda x: (x @ A).argmax(1)
    w1 = lambda x: np.where(in_R(x), shift[w0(x)], w0(x))
    s = lambda x: (x @ skill).argmax(1)
    return w0, w1, s, in_R, in_Q


def onehot(y):
    return np.eye(K)[y]


def run(seed):
    rng = np.random.default_rng(seed)
    w0, w1, s, in_R, in_Q = world(rng)
    gen = lambda n: rng.normal(size=(n, D))

    def labelled(f, region=None):
        def sample(n):
            x = gen(4 * n)
            if region is not None:
                x = x[region(x)]
            x = x[:n]
            return x, onehot(f(x)), None
        return sample

    def finetune(base, f, region):
        # skill data on the region, mixed 1:1 with the base's own labels on generic inputs
        anchor = base.copy()
        skill = labelled(f, region)
        def sample(n):
            xs, ts, _ = skill(n // 2)
            xg = gen(n - len(xs))
            return np.vstack((xs, xg)), np.vstack((ts, softmax(anchor.logits(xg)))), None
        m = base.copy(); m.train(sample, steps=1500)
        return m

    B0 = MLP(rng); B0.train(labelled(w0))
    F0 = finetune(B0, s, in_Q)
    B1 = MLP(rng); B1.train(labelled(w1))

    def kd(target_fn, weight_fn=None, steps=1500):
        m = B1.copy()
        for _ in range(steps):
            x = gen(128)
            m.step(x, target_fn(x), 0.1, None if weight_fn is None else weight_fn(x))
        return m

    pF = lambda x: softmax(F0.logits(x))
    pB0 = lambda x: softmax(B0.logits(x))
    pB1 = lambda x: softmax(B1.logits(x))
    lF = lambda x: F0.logits(x)
    lB0 = lambda x: B0.logits(x)
    lB1 = lambda x: B1.logits(x)

    def gated(x):
        # learned part = where F0 and B0 disagree; elsewhere anchor to B1
        tv = 0.5 * np.abs(pF(x) - pB0(x)).sum(1)
        g = (tv > 0.5)[:, None]
        return np.where(g, pF(x), pB1(x))

    arms = {
        "F0 (old fine-tune)": F0,
        "B1 (no inheritance)": B1,
        "plain KD from F0": kd(pF),
        "delta KD (B1+F0-B0 logits)": kd(lambda x: softmax(lB1(x) + lF(x) - lB0(x))),
        "disagreement-gated KD": kd(gated),
        "oracle: S data fine-tune of B1": finetune(B1, s, in_Q),
    }

    xt = gen(40000)
    Q, R = in_Q(xt), in_R(xt)
    out = {}
    for name, m in arms.items():
        yhat = m.pred(xt)
        out[name] = (
            (yhat[Q] == s(xt)[Q]).mean(),                        # inherited skill
            (yhat[~Q & R] == w1(xt)[~Q & R]).mean(),             # new-base correction kept
            (yhat[~Q & R] == w0(xt)[~Q & R]).mean(),             # fossil: old-world answer (w0 != w1 on R)
            (yhat[~Q & ~R] == w1(xt)[~Q & ~R]).mean(),           # untouched old tasks
        )
    return out


if __name__ == "__main__":
    runs = [run(s) for s in SEEDS]
    cols = ("skill on Q", "W1 fix kept on R\\Q", "fossil rate R\\Q", "other old tasks")
    print(f"{'arm':30s}" + "".join(f"{c:>20s}" for c in cols))
    for name in runs[0]:
        v = np.array([r[name] for r in runs])
        mu, se = v.mean(0), v.std(0, ddof=1) / np.sqrt(len(v))
        print(f"{name:30s}" + "".join(f"{m:>13.3f} ± {e:.3f}" for m, e in zip(mu, se)))
