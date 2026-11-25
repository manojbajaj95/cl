"""Exact rational checks for tree/second-moment-basins.md (CPU, no dependencies)."""
from fractions import Fraction as F


def adam_frozen_v(H, P, th, m, beta=F(1, 2), eta=F(1, 2)):
    # Heavy-ball with a frozen diagonal preconditioner P = diag(1/sqrt(v)), the
    # beta2 -> 1 regime over a short horizon: m' = beta m + H th ; th' = th - eta P m'.
    g = [H[0][0] * th[0] + H[0][1] * th[1], H[1][0] * th[0] + H[1][1] * th[1]]
    m = [beta * m[0] + g[0], beta * m[1] + g[1]]
    th = [th[0] - eta * P[0] * m[0], th[1] - eta * P[1] * m[1]]
    return th, m


def leaks(H, Pa, Pb, tha, thb, ma, mb, reader, k=6):
    out = []
    for _ in range(k):
        tha, ma = adam_frozen_v(H, Pa, tha, ma)
        thb, mb = adam_frozen_v(H, Pb, thb, mb)
        out.append(reader[0] * (tha[0] - thb[0]) + reader[1] * (tha[1] - thb[1]))
    return out


def s1():
    I = [[F(1), F(0)], [F(0), F(1)]]
    C = [[F(1), F(1, 2)], [F(1, 2), F(1)]]  # eigenvectors (1,1), (1,-1)
    one, half = F(1), F(1, 2)
    z = [F(0), F(0)]
    print("S1: leak to a reader, k=1..6")
    # (a) momentum difference along the reader-null eigenvector, plain heavy-ball (P = I)
    print("  rotated host, reader (1,-1), momentum diff (1,1), P=I:",
          [str(x) for x in leaks(C, [one, one], [one, one], z, z, [one, one], z, (one, -one))])
    # (b) same momentum difference, but a common Adam preconditioner diag(1,1/2)
    print("  rotated host, reader (1,-1), momentum diff (1,1), common P=diag(1,1/2):",
          [str(x) for x in leaks(C, [one, half], [one, half], z, z, [one, one], z, (one, -one))])
    # (c) v difference in coordinate 2 only (P2 = 1 vs 1/2), same th and m, rotated host
    th0 = [F(1, 2), F(1, 2)]
    print("  rotated host, reader (1,-1), v diff in coord 2 from th0=(1/2,1/2):",
          [str(x) for x in leaks(C, [one, one], [one, half], th0, th0, z, z, (one, -one))])
    # (d) aligned host, reader-null axis e2, v diff in coord 2: absorbed exactly
    for name, rd in (("service (1,0)", (one, F(0))), ("later B (0,1)", (F(0), one))):
        print(f"  aligned host, reader {name}, v diff in coord 2:",
              [str(x) for x in leaks(I, [one, one], [one, half], th0, th0, z, z, rd)])
    # (e) negative control: v diff in the reader-visible coordinate 1
    print("  aligned host, reader (1,0), v diff in coord 1:",
          [str(x) for x in leaks(I, [one, one], [half, one], th0, th0, z, z, (one, F(0)))])
    # (f) multiplicative: scale the live gradient (th0 x4). v-diff leak scales x4, momentum-diff leak does not.
    th4 = [F(2), F(2)]
    lv1 = leaks(I, [one, one], [half, one], th0, th0, z, z, (one, F(0)), k=3)
    lv4 = leaks(I, [one, one], [half, one], th4, th4, z, z, (one, F(0)), k=3)
    lm1 = leaks(I, [one, one], [one, one], th0, th0, [one, F(0)], z, (one, F(0)), k=3)
    lm4 = leaks(I, [one, one], [one, one], th4, th4, [one, F(0)], z, (one, F(0)), k=3)
    print("  gradient x4: v-diff leak ratio", [str(b / a) for a, b in zip(lv1, lv4)],
          "| momentum-diff leak ratio", [str(b / a) for a, b in zip(lm1, lm4)])
    # (g) sleeper: coordinate 2 untouched (th2 = 0, m2 = 0) -> v diff invisible to every reader
    #     until a later task moves th2; then the B reader (0,1) sees it at once.
    thz = [F(1, 2), F(0)]
    print("  sleeper, coord 2 at rest, readers (1,0),(0,1):",
          [str(x) for x in leaks(I, [one, one], [one, half], thz, thz, z, z, (one, F(0)), k=3)],
          [str(x) for x in leaks(I, [one, one], [one, half], thz, thz, z, z, (F(0), one), k=3)])
    thw = [F(1, 2), F(1, 4)]
    print("  sleeper woken by a later task setting th2=1/4, reader (0,1):",
          [str(x) for x in leaks(I, [one, one], [one, half], thw, thw, z, z, (F(0), one), k=3)])


def s2():
    # Parent F1 host with a second learnable parameter a (hidden-slot decay):
    #   x <- [[1/2, h], [0, a]] x ; aliases (0, r) with |r| <= R.
    # After two steps s2 = h r (1/2 + a), so the certified radius is R(h,a) = 1/(16 p), p = h (1/2 + a).
    # Deployment needs R >= 1/2, i.e. p <= 1/8.
    def p(h, a):
        return h * (F(1, 2) + a)

    def radius(h, a):
        return 1 / (16 * p(h, a)) if p(h, a) else None

    def run(rule, target, steps=12, lr=F(1, 2)):
        h, a = F(1, 8), F(1, 2)
        worst = radius(h, a)
        for _ in range(steps):
            h = h - lr * (h - target[0])
            a = a - lr * (a - target[1])
            if rule == "box":
                h = min(h, F(1, 8))
            elif rule == "basin":
                h = min(h, 1 / (8 * (F(1, 2) + a)))
            worst = min(worst, radius(h, a))
        loss = ((h - target[0]) ** 2 + (a - target[1]) ** 2) / 2
        return h, a, loss, worst

    print("S2: C loss 1/2|(h,a)-target|^2 from (1/8,1/2); certified radius must stay >= 1/2")
    for target in ((F(1, 4), F(0)), (F(1, 4), F(1, 2))):
        print(f"  target {tuple(str(t) for t in target)}:")
        for rule in ("none", "box", "basin"):
            h, a, loss, worst = run(rule, target)
            print(f"    {rule:5s}: h={float(h):.5f} a={float(a):.5f} C loss={float(loss):.6f} "
                  f"min radius on path={worst} ({float(worst):.4f}) {'OK' if worst >= F(1, 2) else 'SHRINKS'}")
    # Unconstrained path, first steps exactly
    h, a = F(1, 8), F(1, 2)
    rows = []
    for t in range(1, 4):
        h, a = h - (h - F(1, 4)) / 2, a / 2
        rows.append((t, h, a, p(h, a), radius(h, a)))
    print("  unconstrained, target (1/4,0), t: h, a, p, radius:",
          [(t, str(h), str(a), str(pp), str(r)) for t, h, a, pp, r in rows])


if __name__ == "__main__":
    s1()
    s2()
