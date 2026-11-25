"""MeZO-LoRA whose whole training history is a (seed, scale, task, reason) log.

theta (all LoRA parameters, one flat fp32 vector) evolves only by
theta <- theta - scale_t * z(seed_t), z ~ N(0, I) from torch.Generator(seed_t).
Perturbations are applied to a copy, so the trajectory is exactly the log and
replaying the log regenerates theta bitwise.
"""
import json, math, random, sys, time
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tasks import TASKS, LABELS, make_items, stable_seed


class LoRALinear(nn.Module):
    def __init__(self, base, r, alpha):
        super().__init__()
        self.base, self.r, self.s = base, r, alpha / r
        self.A = None  # views into the flat theta, set by SeedLogModel
        self.B = None

    def forward(self, x):
        return self.base(x) + (x @ self.A.T) @ self.B.T * self.s


class SeedLogModel:
    def __init__(self, name="Qwen/Qwen2.5-0.5B-Instruct", r=4, alpha=8, targets=("q_proj", "v_proj"),
                 layers=None, init_seed=0, threads=8):
        torch.set_num_threads(threads)
        self.tok = AutoTokenizer.from_pretrained(name)
        self.tok.padding_side = "left"
        self.m = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32).eval()
        for p in self.m.parameters():
            p.requires_grad_(False)
        blocks = self.m.model.layers
        layers = range(len(blocks)) if layers is None else layers
        self.loras, shapes = [], []
        for i in layers:
            attn = blocks[i].self_attn
            for t in targets:
                base = getattr(attn, t)
                l = LoRALinear(base, r, alpha)
                setattr(attn, t, l)
                self.loras.append(l)
                shapes.append(((r, base.in_features), (base.out_features, r)))
        self.d = sum(a[0] * a[1] + b[0] * b[1] for a, b in shapes)
        self.theta0 = torch.zeros(self.d)
        g = torch.Generator().manual_seed(init_seed)
        off = 0
        for (a, b) in shapes:  # A ~ kaiming-uniform-like, B = 0 (standard LoRA init)
            n = a[0] * a[1]
            self.theta0[off:off + n] = (torch.rand(n, generator=g) * 2 - 1) / math.sqrt(a[1])
            off += n + b[0] * b[1]
        self.shapes = shapes
        self.theta = self.theta0.clone()
        self._bind(self.theta)
        self.lab = {t: torch.tensor([self.tok(l).input_ids[0] for l in LABELS[t]]) for t in TASKS}
        self._enc_cache = {}

    def _bind(self, vec):
        off = 0
        for l, (a, b) in zip(self.loras, self.shapes):
            na, nb = a[0] * a[1], b[0] * b[1]
            l.A = vec[off:off + na].view(*a)
            l.B = vec[off + na:off + na + nb].view(*b)
            off += na + nb

    def set_theta(self, vec):
        self.theta.copy_(vec)

    def z(self, seed):
        return torch.randn(self.d, generator=torch.Generator().manual_seed(int(seed)))

    @torch.inference_mode()
    def logits2(self, task, prompts):
        enc = self.tok(prompts, return_tensors="pt", padding=True)
        h = self.m.model(**enc).last_hidden_state[:, -1]
        return h @ self.m.lm_head.weight[self.lab[task]].T

    def loss(self, task, batch):
        lg = self.logits2(task, [p for p, _ in batch])
        y = torch.tensor([y for _, y in batch])
        return nn.functional.cross_entropy(lg, y).item()

    def mezo_step(self, task, batch, seed, lr, eps):
        """Returns the log scale lr*g; theta advances by exactly -scale*z."""
        keep = self.theta.clone()
        z = self.z(seed)
        self.theta.add_(z, alpha=eps)
        lp = self.loss(task, batch)
        self.theta.copy_(keep).add_(z, alpha=-eps)
        lm = self.loss(task, batch)
        self.theta.copy_(keep)
        scale = lr * (lp - lm) / (2 * eps)
        self.theta.add_(z, alpha=-scale)
        return scale

    def replay(self, lines, multipliers=None):
        """Regenerate theta from theta0 and a list of log lines (in order)."""
        th = self.theta0.clone()
        for i, ln in enumerate(lines):
            c = 1.0 if multipliers is None else multipliers[i]
            if c != 0:
                th.add_(self.z(ln["seed"]), alpha=-ln["scale"] * c)
        return th

    @torch.inference_mode()
    def evaluate(self, items_by_task, theta=None, bs=50):
        """Per-task accuracy and 2-way label probabilities."""
        if theta is not None:
            self.set_theta(theta)
        out = {}
        for t, items in items_by_task.items():
            ps = []
            for i in range(0, len(items), bs):
                b = items[i:i + bs]
                ps.append(torch.softmax(self.logits2(t, [p for p, _ in b]), -1))
            P = torch.cat(ps)
            y = torch.tensor([y for _, y in items])
            out[t] = {"acc": (P.argmax(1) == y).float().mean().item(), "p": P[:, 0].tolist()}
        return out


def train_stream(sm, stream, steps, lr, eps, bs, run_seed, corrupt=None, reason_fn=None, log_every=0,
                 eval_items=None):
    """stream: list of task names. corrupt: task whose training labels are flipped.
    Seeds and batches depend only on (run_seed, task, step), so a retrain that skips
    a task reuses exactly the same seeds and batches for the kept lines."""
    lines = []
    for t in stream:
        pool = make_items(t, "train", 2000, run_seed)
        for s in range(steps):
            rng = random.Random(stable_seed(run_seed, t, s))
            batch = rng.sample(pool, bs)
            if corrupt == t:
                batch = [(p, 1 - y) for p, y in batch]
            seed = rng.randrange(2 ** 31)
            scale = sm.mezo_step(t, batch, seed, lr, eps)
            lines.append({"seed": seed, "scale": scale, "task": t, "step": s,
                          "reason": reason_fn(t, s) if reason_fn else f"{t} batch {s}"})
            if log_every and eval_items and (s + 1) % log_every == 0:
                ev = sm.evaluate(eval_items)
                print(t, s + 1, {k: round(v["acc"], 3) for k, v in ev.items()}, flush=True)
    return lines
