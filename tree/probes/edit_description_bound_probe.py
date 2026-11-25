"""Exact zero-error bound on edit-description size under later drift.

Inputs X = {0..n-1}, values Z_q. A receiver holds a behaviour f: X -> Z_q.
A request r = (op, S, v, c) maps f to r(f): "set" writes c on S, "add" adds c
(mod q) on S, "remap" writes c on the inputs of S whose current value is v
(a contextual edit such as "every standard-shipping fee becomes c"); inputs
it does not touch keep f. A description is a message the
receiver decodes, using its current f as side information, into the post-edit
behaviour r(f). Two requests may share a message on a trajectory f_0..f_H only
if r(f_t) == r'(f_t) for every t (the edit is re-applied/re-verified after each
round of later training). Compatibility is equality, so the minimum zero-error
message count is the number of distinct tuples (r(f_0), ..., r(f_H)).

Drift models (one step = one round of later training):
  free     m random inputs get random values
  shift    all values shift by one random constant (a gauge the request
           language cannot see)
  outside  m random inputs outside a fixed protected set P get random values
Anchored arm: the message also carries f_0 on k inputs; the decoder uses the
anchored values instead of the drifted ones there.
"""
import itertools
import zlib

import numpy as np

N, Q = 6, 4
HORIZONS = [0, 1, 2, 4, 8, 16, 32]
SEEDS = 200


def requests():
    out = []
    for size in range(1, N + 1):
        for S in itertools.combinations(range(N), size):
            mask = np.zeros(N, bool)
            mask[list(S)] = True
            out += [("set", mask, -1, c) for c in range(Q)]
            out += [("add", mask, -1, c) for c in range(1, Q)]
            out += [("remap", mask, v, c) for v in range(Q) for c in range(Q) if c != v]
    return out


REQ = requests()
OP = np.array([op for op, _, _, _ in REQ])
MASK = np.stack([m for _, m, _, _ in REQ])
VAL = np.array([v for _, _, v, _ in REQ])
CONST = np.array([c for _, _, _, c in REQ])


def apply_all(f):
    add = (f[None, :] + CONST[:, None]) % Q
    new = np.where((OP == "add")[:, None], add, CONST[:, None])
    touch = MASK & ((OP != "remap")[:, None] | (f[None, :] == VAL[:, None]))
    return np.where(touch, new, f[None, :])


def trajectory(rng, H, mode, m, protected):
    f = rng.integers(0, Q, N)
    fs = [f.copy()]
    free_idx = np.array([i for i in range(N) if i not in protected])
    for _ in range(H):
        f = f.copy()
        if mode == "free":
            idx = rng.choice(N, m, replace=False)
            f[idx] = rng.integers(0, Q, m)
        elif mode == "shift":
            f = (f + rng.integers(1, Q)) % Q
        elif mode == "outside":
            idx = rng.choice(free_idx, min(m, len(free_idx)), replace=False)
            f[idx] = rng.integers(0, Q, len(idx))
        fs.append(f)
    return fs


def classes(fs, anchor=()):
    anchor = list(anchor)
    cols = []
    for f in fs:
        g = f.copy()
        g[anchor] = fs[0][anchor]
        cols.append(apply_all(g))
    tup = np.concatenate(cols, axis=1)
    return len({row.tobytes() for row in tup})


def run(mode, m=1, protected=(), anchor=()):
    res = {}
    for H in HORIZONS:
        bits = []
        for s in range(SEEDS):
            rng = np.random.default_rng(zlib.crc32(repr((mode, m, H, s)).encode()))
            fs = trajectory(rng, H, mode, m, protected)
            bits.append(np.log2(classes(fs, anchor)) + len(anchor) * np.log2(Q))
        res[H] = (float(np.mean(bits)), float(np.percentile(bits, 90)))
    return res


def main():
    rng = np.random.default_rng(0)
    probe = np.concatenate([apply_all(rng.integers(0, Q, N)) for _ in range(64)], axis=1)
    n_sem = len({row.tobytes() for row in probe})
    print(f"requests={len(REQ)}  semantically distinct over 64 random receivers={n_sem}  "
          f"log2={np.log2(n_sem):.2f} bits  explicit post-edit table={N*np.log2(Q):.2f} bits")
    arms = [
        ("free drift, m=1", dict(mode="free", m=1)),
        ("free drift, m=2", dict(mode="free", m=2)),
        ("shift gauge", dict(mode="shift")),
        ("drift outside P={0,1,2}", dict(mode="outside", m=1, protected=(0, 1, 2))),
        ("free m=1 + 2 anchors", dict(mode="free", m=1, anchor=(0, 1))),
        ("free m=1 + 6 anchors", dict(mode="free", m=1, anchor=tuple(range(N)))),
    ]
    print("arm".ljust(28) + "".join(f"H={h:<9}" for h in HORIZONS) + "  (mean bits / p90)")
    for name, kw in arms:
        r = run(**kw)
        print(name.ljust(28) + "".join(f"{r[h][0]:5.2f}/{r[h][1]:<5.2f} " for h in HORIZONS))
    # Limit when drift can reach every behaviour that agrees with f_0 on P.
    P = (0, 1, 2)
    free = [i for i in range(N) if i not in P]
    lim = []
    for s_ in range(50):
        f0 = np.random.default_rng(1000 + s_).integers(0, Q, N)
        fs = []
        for vals in itertools.product(range(Q), repeat=len(free)):
            f = f0.copy()
            f[free] = vals
            fs.append(f)
        lim.append(np.log2(classes([f0] + fs)))
    print(f"H->inf limit with P={{0,1,2}} invariant: {np.mean(lim):.2f} bits")


if __name__ == "__main__":
    main()
