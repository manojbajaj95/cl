"""Self-curriculum forgetting probe (numpy, CPU, ~1 min).

Host: linear regression w in R^d shared by K tasks. Task i draws inputs from its own
random subspace (subspaces overlap) and has its own teacher, so the tasks conflict on
shared directions and no single w is perfect for all of them.

Agent: each episode it picks one task and takes M SGD steps on it. It observes only the
competence of the task it practiced (before and after), as automatic-curriculum agents do.

Questions:
  Q1  Does learning progress measure forgetting? In the second half of the stream, how much
      of the within-episode practice gain is recovery of drift since the last visit
      (gross gain minus the net change of all tasks), and does an LP bandit retain more?
  Q2  Is retention at stationarity set by the practice mixture, not the update rule?
  Q3  How stale is the agent's view of tasks it is not practicing?
"""
import numpy as np

D, K, SUB, M, T = 24, 6, 9, 5, 900
LR, NOISE, WINDOW = 0.05, 0.05, 6


def make_world(seed):
    r = np.random.default_rng(seed)
    bases = [np.linalg.qr(r.standard_normal((D, SUB)))[0] for _ in range(K)]
    w_star = r.standard_normal(D)
    teachers = [w_star + 0.9 * r.standard_normal(D) for _ in range(K)]
    probes = [r.standard_normal((200, SUB)) @ B.T for B in bases]
    return dict(r=r, bases=bases, teachers=teachers, probes=probes)


def loss(w, world, i):
    X = world["probes"][i]
    return float(np.mean((X @ (w - world["teachers"][i])) ** 2))


def competence(w, world, w0):
    # 1 at the task's own optimum, 0 at the initial weights
    out = []
    for i in range(K):
        L0 = loss(w0, world, i)
        out.append(max(0.0, 1.0 - loss(w, world, i) / L0))
    return np.array(out)


def practice(w, v, world, i, lr=LR, mom=0.0, steps=M, scale=1.0):
    r, B, t = world["r"], world["bases"][i], world["teachers"][i]
    for _ in range(steps):
        X = r.standard_normal((16, SUB)) @ B.T
        y = X @ t + NOISE * r.standard_normal(16)
        g = 2 * X.T @ (X @ w - y) / 16
        v = mom * v + g
        w = w - lr * scale * v
    return w, v


def run_policy(seed, policy, eps=0.2):
    world = make_world(seed)
    pr = np.random.default_rng(seed + 999)
    w0 = np.zeros(D)
    w, v = w0.copy(), np.zeros(D)
    seen = np.zeros(K)              # agent's last observed competence per task
    last_t = np.zeros(K)
    lp_hist = [[] for _ in range(K)]
    gross = 0.0                     # sum of within-episode practice gains
    best_ever = np.zeros(K)
    hwm_hist = [[] for _ in range(K)]
    counts = np.zeros(K)
    traj, stale = [], []
    for t in range(T):
        C = competence(w, world, w0)
        traj.append(C)
        unseen = [j for j in range(K) if last_t[j] < t]
        stale.append(np.mean([abs(seen[j] - C[j]) for j in unseen]) if t > K else np.nan)
        if t < K:
            i = t
        elif policy == "uniform":
            i = pr.integers(K)
        elif policy == "hwm":              # reward only new all-time highs per task
            score = np.array([np.mean(h[-WINDOW:]) if h else 1.0 for h in hwm_hist])
            i = pr.integers(K) if pr.random() < eps else int(np.argmax(score))
        elif policy in ("alp", "plp", "alp_ipw"):
            score = np.array([np.mean(h[-WINDOW:]) if h else 1.0 for h in lp_hist])
            if policy in ("alp", "alp_ipw"):
                score = np.abs(score)
            i = pr.integers(K) if pr.random() < eps else int(np.argmax(score))
        elif policy == "deficit":          # practice the weakest task as last seen
            i = pr.integers(K) if pr.random() < eps else int(np.argmin(seen))
        elif policy == "oracle_total":     # one-step lookahead on true total competence
            best, i = -1e9, 0
            for j in range(K):
                state = world["r"].bit_generator.state
                wj, _ = practice(w, v, world, j)
                world["r"].bit_generator.state = state
                s = competence(wj, world, w0).sum()
                if s > best:
                    best, i = s, j
        before = C[i]
        counts[i] += 1
        # alp_ipw: LP chooses, but the step is reweighted by target/empirical frequency so the
        # expected update is the uniform mixture's (decouples choice from effective mixture)
        scale = min(5.0, (1.0 / K) / (counts[i] / counts.sum())) if policy == "alp_ipw" else 1.0
        w, v = practice(w, v, world, i, scale=scale)
        after = competence(w, world, w0)[i]
        # teacher-student LP: change of the observed score between visits,
        # which includes the forgetting that happened while the task was not practiced
        lp_hist[i].append(after - seen[i] if t >= K else after)
        hwm_hist[i].append(max(0.0, after - best_ever[i]))
        best_ever[i] = max(best_ever[i], after)
        if t >= T // 2:
            gross += after - before
        seen[i], last_t[i] = after, t
    traj = np.array(traj)
    h = traj[T // 2:]
    net = float(np.sum(traj[-1] - traj[T // 2]))
    return dict(mean=h.mean(), worst=h.min(axis=1).mean(), gross=gross,
                net=net,
                stale=np.nanmean(stale[T // 2:]), traj=traj)


def mixture_fixed_point(seed, p, lr, mom, steps=1500):
    world = make_world(seed)
    pr = np.random.default_rng(seed + 7)
    w, v = np.zeros(D), np.zeros(D)
    acc = []
    for s in range(steps):
        i = pr.choice(K, p=p)
        w, v = practice(w, v, world, i, lr=lr, mom=mom, steps=1)
        if s > steps // 2:
            acc.append(competence(w, world, np.zeros(D)))
    return np.mean(acc, axis=0)


def ci(x):
    x = np.asarray(x)
    return x.mean(), 1.96 * x.std(ddof=1) / np.sqrt(len(x))


if __name__ == "__main__":
    seeds = list(range(20))
    print("Q1/Q3: policies over", len(seeds), "worlds (second-half averages)")
    print(f"{'policy':14s} {'mean C':>14s} {'worst C':>14s} {'practice gain':>14s} {'net change':>14s} {'staleness':>14s} {'recovery':>9s}")
    res = {}
    for pol in ["uniform", "alp", "plp", "deficit", "hwm", "alp_ipw", "oracle_total"]:
        rs = [run_policy(s, pol) for s in seeds]
        res[pol] = rs
        cols = [ci([r[k] for r in rs]) for k in ["mean", "worst", "gross", "net", "stale"]]
        rec = 1 - sum(r["net"] for r in rs) / sum(r["gross"] for r in rs)   # pooled share
        print(f"{pol:14s} " + " ".join(f"{m:7.3f}±{e:5.3f}" for m, e in cols) + f" {rec:9.3f}")
    for pol in ["alp", "plp", "deficit", "hwm", "alp_ipw", "oracle_total"]:
        dm = [a["mean"] - u["mean"] for a, u in zip(res[pol], res["uniform"])]
        dw = [a["worst"] - u["worst"] for a, u in zip(res[pol], res["uniform"])]
        print("%-12s - uniform: mean C %+.3f±%.3f, worst C %+.3f±%.3f" % (pol, *ci(dm), *ci(dw)))
    g = [r["gross"] for r in res["uniform"]]
    corr = np.corrcoef([r["gross"] for p in res for r in res[p]], [r["mean"] for p in res for r in res[p]])[0, 1]
    print("corr(practice gain, mean competence) over all runs: %.3f" % corr)

    print("\nQ2: stationary competence vector vs practice mixture and update rule (5 worlds)")
    rng = np.random.default_rng(0)
    mixes = [np.ones(K) / K] + [rng.dirichlet(np.ones(K)) for _ in range(3)]
    rules = [(0.05, 0.0), (0.02, 0.0), (0.02, 0.6)]
    rule_spread, mix_spread = [], []
    for s in range(5):
        table = np.array([[mixture_fixed_point(s, p, lr, mom) for (lr, mom) in rules] for p in mixes])
        # table[mix, rule, task]
        rule_spread.append(np.mean(np.abs(table - table.mean(axis=1, keepdims=True))))
        mix_spread.append(np.mean(np.abs(table - table.mean(axis=0, keepdims=True))))
    print("mean |dev| of per-task competence across update rules (same mixture): %.4f±%.4f" % ci(rule_spread))
    print("mean |dev| of per-task competence across mixtures (same rule):        %.4f±%.4f" % ci(mix_spread))
