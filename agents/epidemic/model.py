"""Pool dynamics of a self-evolving agent's persistent artifacts (lessons, skills, memories).

Each round the agent retrieves k artifacts, solves a task, distills a candidate artifact
with those k in context, and a gate admits it. A candidate is defective with probability
1 - (1 - eps) * (1 - tau) ** j, where j is the number of defective artifacts in context.
Defective artifacts that are retrieved are exposed (and removed) with probability d; with
provenance contact tracing, removing an artifact also removes each descendant with
probability phi.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Params:
    k: int = 4
    tau: float = 0.3
    eps: float = 0.02
    alpha_s: float = 0.8
    alpha_d: float = 0.8
    d: float = 0.0
    phi: float = 0.0
    base: float = 0.4
    beta: float = 0.45
    gamma: float = 0.6
    n_seed: int = 0

    @property
    def R(self) -> float:
        return self.k * (self.alpha_d * self.tau - self.d) / self.alpha_s


@dataclass
class Pool:
    defective: list = field(default_factory=list)
    parents: list = field(default_factory=list)
    children: list = field(default_factory=list)
    alive: list = field(default_factory=list)
    root: list = field(default_factory=list)

    def add(self, is_def: bool, parents: list[int]) -> int:
        i = len(self.defective)
        self.defective.append(is_def)
        self.parents.append(parents)
        self.children.append([])
        self.alive.append(True)
        self.root.append(is_def and not any(self.defective[p] for p in parents))
        for p in parents:
            self.children[p].append(i)
        return i

    def alive_ids(self) -> np.ndarray:
        return np.flatnonzero(self.alive)

    def remove(self, i: int, phi: float, rng: np.random.Generator) -> int:
        removed, stack = 0, [i]
        while stack:
            j = stack.pop()
            if not self.alive[j]:
                continue
            self.alive[j] = False
            removed += 1
            if phi > 0:
                stack.extend(c for c in self.children[j] if self.alive[c] and rng.random() < phi)
        return removed


def success_prob(p: Params, n_s: int, n_d: int) -> float:
    return float(np.clip(p.base + p.beta * n_s / p.k - p.gamma * n_d / p.k, 0.0, 1.0))


def run(p: Params, T: int, seed: int = 0, intervene_at: int | None = None, intervention: str = "none",
        log_every: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    pool = Pool()
    for _ in range(p.n_seed):
        pool.add(False, [])
    xs, ns, succ, t_log = [], [], [], []
    for t in range(T):
        if intervene_at is not None and t == intervene_at:
            apply_intervention(pool, intervention, rng)
        alive = pool.alive_ids()
        ctx = rng.choice(alive, size=min(p.k, len(alive)), replace=False) if len(alive) else np.array([], int)
        is_def = np.array([pool.defective[i] for i in ctx], bool)
        n_d = int(is_def.sum())
        n_s = len(ctx) - n_d
        succ.append(rng.random() < success_prob(p, n_s, n_d))
        for i in ctx[is_def]:
            if pool.alive[i] and rng.random() < p.d:
                pool.remove(int(i), p.phi, rng)
        cand_def = rng.random() < 1 - (1 - p.eps) * (1 - p.tau) ** n_d
        if rng.random() < (p.alpha_d if cand_def else p.alpha_s):
            pool.add(bool(cand_def), [int(i) for i in ctx])
        if t % log_every == 0:
            alive = pool.alive_ids()
            nd = sum(pool.defective[i] for i in alive)
            xs.append(nd / max(len(alive), 1))
            ns.append(len(alive))
            t_log.append(t)
    return dict(t=np.array(t_log), x=np.array(xs), n=np.array(ns), success=np.array(succ, float))


def apply_intervention(pool: Pool, kind: str, rng: np.random.Generator) -> None:
    if kind == "none":
        return
    roots = [i for i in pool.alive_ids() if pool.root[i]]
    if kind == "rollback_roots":
        for i in roots:
            pool.alive[i] = False
    elif kind == "provenance_closure":
        for i in roots:
            pool.remove(i, 1.0, rng)
    elif kind == "oracle_purge":
        for i in pool.alive_ids():
            if pool.defective[i]:
                pool.alive[i] = False
    else:
        raise ValueError(kind)
