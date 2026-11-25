"""Exact rational checks for tree/recovery-basins.md (CPU, no dependencies)."""
from fractions import Fraction as F


def f1():
    # Deviation x = (s, r): s is the live service coordinate, r a hidden slot.
    # One C step is x <- M_h x with M_h = [[1/2, h], [0, 1/2]]; the host chooses h.
    def run(h, x, k=2):
        s, r = x
        for _ in range(k):
            s, r = F(1, 2) * s + h * r, F(1, 2) * r
        return s, r

    design = (F(1, 2), F(-1, 2))
    aliases = [(F(0), F(1, 2)), (F(0), F(-1, 2))]
    ready = F(1, 16)
    print("F1: host h | design s2 | design endpoint loss s2^2/2 | worst alias |s2| | alias ready")
    for h in (F(0), F(1, 8), F(1, 4)):
        s_d, _ = run(h, design)
        worst = max(abs(run(h, a)[0]) for a in aliases)
        print(f"  h={h}: s2={s_d}, loss={s_d * s_d / 2}, worst={worst}, ready={worst <= ready}")


def f2():
    # Heavy-ball on C loss 0.5 th^T H th (deviation coordinates):
    #   m' = beta m + H th ; th' = th - eta m'.
    # Two states share th but differ in the momentum slot by d.
    beta, eta = F(1, 2), F(1, 2)

    def step(H, th, m):
        g = [H[0][0] * th[0] + H[0][1] * th[1], H[1][0] * th[0] + H[1][1] * th[1]]
        m = [beta * m[0] + g[0], beta * m[1] + g[1]]
        th = [th[0] - eta * m[0], th[1] - eta * m[1]]
        return th, m

    hosts = {
        "coupled (contract only)": [[F(1), F(1, 2)], [F(1, 2), F(1)]],
        "aligned (absorb)": [[F(1), F(0)], [F(0), F(1)]],
    }
    d = [F(0), F(1)]
    readers = {"service r=(1,0)": (F(1), F(0)), "later B r=(1,1)": (F(1), F(1))}
    margin = F(1, 64)
    for name, H in hosts.items():
        th, m = [F(0), F(0)], list(d)
        rows = []
        for k in range(1, 9):
            th, m = step(H, th, m)
            rows.append((k, th, m))
        print(f"F2 host {name}:")
        for rn, rv in readers.items():
            leaks = [rv[0] * t[0] + rv[1] * t[1] for _, t, _ in rows]
            first = next((k for k, l in zip(range(1, 9), leaks) if all(abs(x) < margin for x in leaks[k - 1:])), None)
            print(f"  {rn}: leaks k=1..4 {[str(x) for x in leaks[:4]]}, below 1/64 from k={first}")
        print(f"  hidden difference after 4 steps th={[str(x) for x in rows[3][1]]}, m={[str(x) for x in rows[3][2]]}")
        th, m = [F(1, 2), F(1, 2)], [F(0), F(0)]
        for _ in range(4):
            th, m = step(H, th, m)
        loss = F(1, 2) * sum(th[i] * sum(H[i][j] * th[j] for j in range(2)) for i in range(2))
        print(f"  C loss from design state (1/2,1/2) after 4 steps: {loss}")


if __name__ == "__main__":
    f1()
    f2()
