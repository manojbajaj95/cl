"""Adapter-compatibility contract probe (CPU, torch, ~5 min for 5 seeds).

A frozen 3-layer MLP base serves 8 private rank-4 LoRA clients on its middle
layer (W2). The base then learns a new task. We compare base-update
constraints by how well each client's *unchanged* adapter still works.

Arms
  naive      new task only
  base-safe  + distill base logits on base inputs (base retention)
  read-ABI   + keep insertion-point activations (h1, z2) on client probes
             (PR #115 idea 11)
  write-ctr  read-ABI + keep the downstream finite response to each client's
             write directions B_c (column space only, no A_c, no labels)
  write-pm   write-ctr with signed multi-scale writes (-2,-1,+1,+2 x scale)
  write-only base-safe + write-pm response, without pinning h1/z2
  write-pool write-ctr with all clients' write columns pooled to top-k SVD dims
  write-base write-ctr evaluated on base inputs instead of client probes
  composite  distill each client's full adapted logits on its probes
             (needs every adapter; cost grows with clients)
  comp-base  composite on base inputs (adapter weights, no client data)
  span-rand  distill 4 random adapters per client drawn from span(A_c) x span(B_c)
             on base inputs (adapter subspaces only, not the adapter itself)
  retune     naive update, then retrain each adapter (upper bound, extra cost)
"""
import sys, zlib
import torch, torch.nn.functional as F

torch.set_num_threads(4)
D, H1, H2, C, R, NC = 16, 64, 64, 8, 4, 8
NPROBE, NTR, NTE = 64, 2000, 1000


def rng(*parts):
    return torch.Generator().manual_seed(zlib.crc32(repr(parts).encode()))


def teacher(g):
    W1 = torch.randn(D, 32, generator=g) / D ** .5
    W2 = torch.randn(32, C, generator=g) / 32 ** .5
    return lambda x: (torch.tanh(x @ W1) @ W2).argmax(1)


def data(g, mu, T, n):
    x = torch.randn(n, D, generator=g) + mu
    return x, T(x)


class Base(torch.nn.Module):
    def __init__(s, g):
        super().__init__()
        s.W1 = torch.nn.Parameter(torch.randn(D, H1, generator=g) / D ** .5)
        s.W2 = torch.nn.Parameter(torch.randn(H1, H2, generator=g) / H1 ** .5)
        s.W3 = torch.nn.Parameter(torch.randn(H2, C, generator=g) / H2 ** .5)
        s.b1 = torch.nn.Parameter(torch.zeros(H1)); s.b2 = torch.nn.Parameter(torch.zeros(H2))
        s.b3 = torch.nn.Parameter(torch.zeros(C))

    def h1(s, x): return F.relu(x @ s.W1 + s.b1)
    def z2(s, h1): return h1 @ s.W2 + s.b2
    def head(s, z2): return F.relu(z2) @ s.W3 + s.b3
    def forward(s, x, ad=None):
        h = s.h1(x); z = s.z2(h)
        if ad is not None: z = z + (h @ ad[0]) @ ad[1]   # A: H1xR, B: RxH2
        return s.head(z)


def acc(m, x, y, ad=None):
    with torch.no_grad(): return (m(x, ad).argmax(1) == y).float().mean().item()


def train(params, loss_fn, steps, lr):
    opt = torch.optim.Adam(params, lr=lr)
    for _ in range(steps):
        opt.zero_grad(); loss_fn().backward(); opt.step()


def fit_adapter(base, x, y, g, steps=400):
    A = (torch.randn(H1, R, generator=g) / H1 ** .5).requires_grad_()
    B = torch.zeros(R, H2).requires_grad_()
    for p in base.parameters(): p.requires_grad_(False)
    train([A, B], lambda: F.cross_entropy(base(x, (A, B)), y), steps, 1e-2)
    for p in base.parameters(): p.requires_grad_(True)
    return A.detach(), B.detach()


def run(seed, lam=3.0, k_pool=4, upd_steps=600):
    g = rng("base", seed)
    T0 = teacher(g); xb, yb = data(g, 0., T0, NTR); xbt, ybt = data(g, 0., T0, NTE)
    base = Base(g)
    train(base.parameters(), lambda: F.cross_entropy(base(xb), yb), 800, 1e-2)
    clients = []
    for c in range(NC):
        gc = rng("client", seed, c)
        mu = torch.randn(D, generator=gc) * 0.7; Tc = teacher(gc)
        x, y = data(gc, mu, Tc, NTR); xt, yt = data(gc, mu, Tc, NTE)
        ad = fit_adapter(base, x, y, gc)
        clients.append(dict(x=x, y=y, xt=xt, yt=yt, ad=ad, probe=x[:NPROBE]))
    gn = rng("new", seed); mun = torch.randn(D, generator=gn) * 1.5; Tn = teacher(gn)
    xn, yn = data(gn, mun, Tn, NTR); xnt, ynt = data(gn, mun, Tn, NTE)

    old = Base(g); old.load_state_dict(base.state_dict())
    for p in old.parameters(): p.requires_grad_(False)
    with torch.no_grad():
        base_logits = old(xb[:512])
        scale = torch.stack([(old.h1(c['probe']) @ c['ad'][0]).std() for c in clients]).mean()
    Bcols = [F.normalize(c['ad'][1], dim=1) for c in clients]     # write directions (rows of B)
    signed = lambda B: torch.cat([s_ * B for s_ in (-2., -1., 1., 2.)])
    U = torch.linalg.svd(torch.cat(Bcols), full_matrices=False)[2][:k_pool]   # pooled top-k
    allprobe = torch.cat([c['probe'] for c in clients])

    gm = rng("mix", seed)
    mixes = [[(c['ad'][0] @ torch.randn(R, R, generator=gm), torch.randn(R, R, generator=gm) @ c['ad'][1])
              for _ in range(4)] for c in clients]

    def resp(m, z, dirs):  # finite downstream response to writes along dirs
        y0 = m.head(z)
        return torch.stack([m.head(z + scale * d) - y0 for d in dirs])

    def ref(fn):
        with torch.no_grad(): return fn(old)
    refs = dict(
        h1=[ref(lambda m: m.h1(c['probe'])) for c in clients],
        z2=[ref(lambda m: m.z2(m.h1(c['probe']))) for c in clients],
        w=[ref(lambda m: resp(m, m.z2(m.h1(c['probe'])), B)) for c, B in zip(clients, Bcols)],
        wb=[ref(lambda m: resp(m, m.z2(m.h1(xb[:NPROBE])), B)) for B in Bcols],
        wp=ref(lambda m: resp(m, m.z2(m.h1(allprobe)), U)),
        wpm=[ref(lambda m: resp(m, m.z2(m.h1(c['probe'])), signed(B))) for c, B in zip(clients, Bcols)],
        compb=[ref(lambda m: m(xb[:NPROBE], c['ad'])) for c in clients],
        span=[ref(lambda m: torch.stack([m(xb[:NPROBE], ad) for ad in mixes[i]])) for i in range(NC)],
        comp=[ref(lambda m: m(c['probe'], c['ad'])) for c in clients])

    def make(arm, m):
        def loss():
            L = F.cross_entropy(m(xn), yn)
            if arm == 'naive' or arm == 'retune': return L
            L = L + lam * F.kl_div(F.log_softmax(m(xb[:512]), 1), F.log_softmax(base_logits, 1),
                                   log_target=True, reduction='batchmean')
            if arm == 'composite':
                return L + lam * sum(F.mse_loss(m(c['probe'], c['ad']), r) for c, r in zip(clients, refs['comp'])) / NC
            if arm == 'base-safe': return L
            if arm == 'comp-base':
                return L + lam * sum(F.mse_loss(m(xb[:NPROBE], c['ad']), r) for c, r in zip(clients, refs['compb'])) / NC
            if arm == 'span-rand':
                return L + lam * sum(F.mse_loss(torch.stack([m(xb[:NPROBE], ad) for ad in mixes[i]]), refs['span'][i])
                                     for i in range(NC)) / NC
            if arm == 'write-only':
                return L + lam * sum(F.mse_loss(resp(m, m.z2(m.h1(c['probe'])), signed(B)), r)
                                     for c, B, r in zip(clients, Bcols, refs['wpm'])) / NC
            h = [m.h1(c['probe']) for c in clients]; z = [m.z2(hh) for hh in h]
            L = L + lam * sum(F.mse_loss(a, b) + F.mse_loss(zz, bz) for a, b, zz, bz in
                              zip(h, refs['h1'], z, refs['z2'])) / NC
            if arm == 'read-ABI': return L
            if arm == 'write-ctr':
                return L + lam * sum(F.mse_loss(resp(m, zz, B), r) for zz, B, r in zip(z, Bcols, refs['w'])) / NC
            if arm == 'write-pm':
                return L + lam * sum(F.mse_loss(resp(m, zz, signed(B)), r) for zz, B, r in zip(z, Bcols, refs['wpm'])) / NC
            if arm == 'write-base':
                zb = m.z2(m.h1(xb[:NPROBE]))
                return L + lam * sum(F.mse_loss(resp(m, zb, B), r) for B, r in zip(Bcols, refs['wb'])) / NC
            if arm == 'write-pool':
                return L + lam * F.mse_loss(resp(m, m.z2(m.h1(allprobe)), U), refs['wp'])
        return loss

    out = {}
    pre = dict(client=[acc(old, c['xt'], c['yt'], c['ad']) for c in clients], base=acc(old, xbt, ybt),
               new=acc(old, xnt, ynt))
    out['before'] = pre
    for arm in ['naive', 'base-safe', 'read-ABI', 'write-ctr', 'write-pm', 'write-only', 'write-pool', 'write-base', 'composite', 'comp-base', 'span-rand', 'retune']:
        m = Base(g); m.load_state_dict(old.state_dict())
        train(m.parameters(), make(arm, m), upd_steps, 3e-3)
        if arm == 'retune':
            cl = [acc(m, c['xt'], c['yt'], fit_adapter(m, c['x'], c['y'], rng("re", seed, i)))
                  for i, c in enumerate(clients)]
        else:
            cl = [acc(m, c['xt'], c['yt'], c['ad']) for c in clients]
        with torch.no_grad():
            dz = sum(F.mse_loss(m.z2(m.h1(c['probe'])), r).item() for c, r in zip(clients, refs['z2'])) / NC
        out[arm] = dict(client=cl, base=acc(m, xbt, ybt), new=acc(m, xnt, ynt), dz2=dz)
    return out


if __name__ == '__main__':
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    res = [run(s) for s in range(seeds)]
    arms = list(res[0])
    def ms(v):
        t = torch.tensor(v); return f"{100*t.mean():5.1f} ± {100*t.std():4.1f}"
    print(f"{seeds} seeds; client acc = unchanged adapters on updated base (mean over 8 clients); "
          f"worst = worst client; chance = {100/C:.1f}%")
    print(f"{'arm':11s} | {'client mean':13s} | {'client worst':13s} | {'base old':13s} | {'new task':13s} | z2 drift")
    for a in arms:
        cm = [sum(r[a]['client']) / NC for r in res]; cw = [min(r[a]['client']) for r in res]
        dz = f"{sum(r[a].get('dz2', 0) for r in res)/seeds:.4f}" if a != 'before' else '-'
        print(f"{a:11s} | {ms(cm)} | {ms(cw)} | {ms([r[a]['base'] for r in res])} | {ms([r[a]['new'] for r in res])} | {dz}")
