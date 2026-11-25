"""CPU probe for tree/developmental-growth.md.

Tests three core developmental-biology continual-learning phenomena in pure NumPy
(task-ID-free inference, single shared readout head, 16 paired worlds, mean +/- 95% CI):

1. Probe 1 - Genotype-Phenotype Dilemma (Pleiotropy vs. Regenerability):
   - direct_sgd: standard MLP weights updated on A then B (no regeneration).
   - shared_genome: single CPPN coordinate-to-weight genome updated on A then B
     (pleiotropic forgetting when editing the shared developmental program).
   - compartment_genome: morphogen-gated two-compartment genome (cis-regulatory
     branch for B with a local domain receptor); retains A while learning B.
   - somatic_B_plus_A_regen: local 3-cell CA regenerative attractor trained on A
     runs after somatic B learning and 30% contiguous lesion -> restores A while
     erasing unassimilated somatic B (Regeneration-vs-Plasticity conflict).
   - assimilated_AB_regen: local 3-cell CA regenerative attractor updated after
     compartmental assimilation -> restores BOTH A and B from surviving neighbors
     after 30% contiguous lesion with zero replay data and zero weight backups.

2. Probe 2 - Growth-Induced Drift & Readout Spillover (extending PR #115):
   - naive_grow: function-preserving widening (w2_new=0) + SGD on B.
   - ewc_grow: function-preserving widening + diagonal-Fisher EWC on old units.
   - oracle_freeze_grow: hard-freeze old units on task boundary, train new global
     tanh units on B (still fails without task IDs due to shared-readout spillover!).
   - receptor_only_grow: new units carry a local domain receptor, no trophic lock.
   - trophic_only_grow: local trophic plasticity lock, global tanh new units.
   - trophic_receptor_grow: strictly local trophic plasticity lock + local domain
     receptor on newly budded units (zero task IDs, zero Fisher/replay).

Deterministic seeds via zlib.crc32.
"""

from __future__ import annotations

import time
import zlib
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


def make_seed(*parts: object) -> int:
    return zlib.crc32(repr(parts).encode("utf-8")) & 0xFFFFFFFF


def mean_ci95(vals: List[float]) -> Tuple[float, float]:
    arr = np.asarray(vals, dtype=np.float64)
    m = float(arr.mean())
    if len(arr) <= 1:
        return m, 0.0
    se = float(arr.std(ddof=1) / np.sqrt(len(arr)))
    return m, 1.96 * se


def sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-x))


@dataclass
class TaskData:
    X_tr: np.ndarray
    y_tr: np.ndarray
    X_te: np.ndarray
    y_te: np.ndarray


def make_paired_tasks(
    world_id: int,
    d: int = 12,
    n_tr: int = 256,
    n_te: int = 256,
    conflict: float = 0.6,
) -> Tuple[TaskData, TaskData]:
    """Two nonlinear binary tasks jointly solvable without task IDs.

    Tasks A and B live in shifted input regimes (+/- 1.6 along u_reg) with shared
    noisy dimensions and flipped rules on the shared subspace (u_sh0, u_sh1).
    """
    rng = np.random.default_rng(make_seed("world", world_id, d, conflict))
    Q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    u_reg = Q[0]
    u_sh0, u_sh1 = Q[1], Q[2]
    u_a0, u_a1 = Q[3], Q[4]
    u_b0, u_b1 = Q[5], Q[6]

    def sample_task(is_b: bool) -> TaskData:
        X = rng.normal(0.0, 0.85, size=(n_tr + n_te, d))
        if not is_b:
            X = X + 1.6 * u_reg[None, :]
            s = (
                np.tanh(1.6 * (X @ u_sh0))
                - 0.7 * np.tanh(1.6 * (X @ u_sh1))
                + 0.9 * np.tanh(1.6 * (X @ u_a0))
                + 0.4 * (X @ u_a1)
            )
        else:
            X = X - 1.6 * u_reg[None, :]
            s = (
                -conflict * np.tanh(1.6 * (X @ u_sh0))
                + conflict * 0.7 * np.tanh(1.6 * (X @ u_sh1))
                + 1.0 * np.tanh(1.6 * (X @ u_b0))
                + 0.5 * (X @ u_b1)
            )
        y = (s > 0.0).astype(np.float64)
        return TaskData(X[:n_tr], y[:n_tr], X[n_tr:], y[n_tr:])

    return sample_task(False), sample_task(True)


# ---------------------------------------------------------------------------
# MLP with optional per-unit receptor gate g_i(x) in (0, 1]
# ---------------------------------------------------------------------------

def receptor_gate(
    X: np.ndarray,
    centers: np.ndarray | None,
    gamma: np.ndarray | None,
) -> np.ndarray:
    """Localized morphogen/domain receptor gate r_i(x) = exp(-gamma_i * ||x - c_i||^2 / d).

    Units with gamma_i == 0 have r_i(x) == 1 (global receptive field).
    """
    if centers is None or gamma is None:
        return np.ones((len(X), 1), dtype=np.float64)
    # X: (N, d), centers: (H, d), gamma: (H,)
    diff = X[:, None, :] - centers[None, :, :]
    sq = np.mean(diff * diff, axis=2)  # (N, H)
    return np.exp(-gamma[None, :] * sq)


def mlp_forward(
    X: np.ndarray,
    W1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: float,
    centers: np.ndarray | None = None,
    gamma: np.ndarray | None = None,
):
    z1 = X @ W1.T + b1[None, :]
    raw_h = np.tanh(z1)
    gate = receptor_gate(X, centers, gamma)
    h = raw_h * gate
    logits = h @ w2 + b2
    p = sigmoid(logits)
    return raw_h, gate, h, logits, p


def mlp_acc(
    X: np.ndarray,
    y: np.ndarray,
    W1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: float,
    centers: np.ndarray | None = None,
    gamma: np.ndarray | None = None,
) -> float:
    _, _, _, logits, _ = mlp_forward(X, W1, b1, w2, b2, centers, gamma)
    return float(np.mean((logits > 0.0) == (y > 0.5)) * 100.0)


def mlp_grads(
    X: np.ndarray,
    y: np.ndarray,
    W1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: float,
    centers: np.ndarray | None = None,
    gamma: np.ndarray | None = None,
):
    n = len(X)
    raw_h, gate, h, _, p = mlp_forward(X, W1, b1, w2, b2, centers, gamma)
    dlog = (p - y) / n
    gw2 = h.T @ dlog
    gb2 = float(np.sum(dlog))
    dh = np.outer(dlog, w2)
    dz1 = dh * gate * (1.0 - raw_h * raw_h)
    gW1 = dz1.T @ X
    gb1 = np.sum(dz1, axis=0)
    return gW1, gb1, gw2, gb2, h, p


# ---------------------------------------------------------------------------
# Probe 1: Genotype-Phenotype Dilemma (Pleiotropy vs. Regenerability)
# ---------------------------------------------------------------------------

def make_tissue_coords(H: int) -> np.ndarray:
    theta = np.linspace(0.0, 2.0 * np.pi, H, endpoint=False)
    morph = np.linspace(-1.0, 1.0, H)
    return np.stack([np.cos(theta), np.sin(theta), morph, np.cos(2 * theta), np.sin(2 * theta)], axis=1)


def decode_genome(coords: np.ndarray, G1: np.ndarray, bg1: np.ndarray, G2: np.ndarray, bg2: np.ndarray):
    gh = np.tanh(coords @ G1.T + bg1[None, :])
    out = gh @ G2.T + bg2[None, :]
    return gh, out[:, :-2], out[:, -2], out[:, -1]


def train_genome(
    task: TaskData,
    coords: np.ndarray,
    G1: np.ndarray,
    bg1: np.ndarray,
    G2: np.ndarray,
    bg2: np.ndarray,
    b2: float,
    steps: int = 200,
    lr: float = 0.25,
    cell_mask: np.ndarray | None = None,
    centers: np.ndarray | None = None,
    gamma: np.ndarray | None = None,
    fixed_W1: np.ndarray | None = None,
    fixed_b1: np.ndarray | None = None,
    fixed_w2: np.ndarray | None = None,
    b2_lr_scale: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    G1, bg1, G2, bg2 = G1.copy(), bg1.copy(), G2.copy(), bg2.copy()
    for _ in range(steps):
        gh, W1, b1, w2 = decode_genome(coords, G1, bg1, G2, bg2)
        if cell_mask is not None:
            W1_eff = W1 * cell_mask[:, None]
            b1_eff = b1 * cell_mask
            w2_eff = w2 * cell_mask
            if fixed_W1 is not None:
                W1_eff = W1_eff + fixed_W1
                b1_eff = b1_eff + fixed_b1
                w2_eff = w2_eff + fixed_w2
        else:
            W1_eff, b1_eff, w2_eff = W1, b1, w2
        gW1, gb1, gw2, gb2, _, _ = mlp_grads(
            task.X_tr, task.y_tr, W1_eff, b1_eff, w2_eff, b2, centers, gamma
        )
        g_out = np.concatenate([gW1, gb1[:, None], gw2[:, None]], axis=1)
        if cell_mask is not None:
            g_out = g_out * cell_mask[:, None]
        gG2 = g_out.T @ gh
        gbg2 = np.sum(g_out, axis=0)
        dgh = g_out @ G2
        dz = dgh * (1.0 - gh * gh)
        gG1 = dz.T @ coords
        gbg1 = np.sum(dz, axis=0)
        G1 -= lr * gG1
        bg1 -= lr * gbg1
        G2 -= lr * gG2
        bg2 -= lr * gbg2
        b2 -= lr * b2_lr_scale * gb2
    return G1, bg1, G2, bg2, b2


def fit_local_ca_regenerator(
    P_target: np.ndarray,
    seed: int,
    n_lesions: int = 160,
    lesion_frac: float = 0.30,
) -> np.ndarray:
    """Strictly local 3-cell-neighborhood CA repair rule on the tissue ring.

    Each cell sees ONLY its own state + immediate left/right neighbors [i-1, i, i+1].
    Zero stored weight backups, zero replay data.
    """
    rng = np.random.default_rng(seed)
    H, F = P_target.shape
    k_lesion = max(1, int(round(H * lesion_frac)))
    Xs, Ys = [], []
    for _ in range(n_lesions):
        P_cur = P_target.copy()
        alive = np.ones(H, dtype=np.float64)
        start = int(rng.integers(0, H))
        idx = [(start + j) % H for j in range(k_lesion)]
        P_cur[idx] = 0.0
        alive[idx] = 0.0
        if rng.random() < 0.5:
            P_cur += rng.normal(0.0, 0.04, size=P_cur.shape) * alive[:, None]
        for i in range(H):
            im1, ip1 = (i - 1) % H, (i + 1) % H
            feat = np.concatenate([
                P_cur[im1], P_cur[i], P_cur[ip1],
                [alive[im1], alive[i], alive[ip1], 1.0],
            ])
            Xs.append(feat)
            Ys.append(P_target[i] - P_cur[i])
    X_mat = np.asarray(Xs, dtype=np.float64)
    Y_mat = np.asarray(Ys, dtype=np.float64)
    reg = 1e-1 * np.eye(X_mat.shape[1])
    return np.linalg.solve(X_mat.T @ X_mat + reg, X_mat.T @ Y_mat)


def run_local_ca_regen(
    P_damaged: np.ndarray,
    alive_init: np.ndarray,
    K: np.ndarray,
    steps: int = 12,
    alpha: float = 0.55,
) -> np.ndarray:
    P = P_damaged.copy()
    alive = alive_init.copy()
    H = P.shape[0]
    dam_mask = (alive_init < 0.5).astype(np.float64)[:, None]
    for _ in range(steps):
        dP = np.zeros_like(P)
        new_alive = alive.copy()
        for i in range(H):
            im1, ip1 = (i - 1) % H, (i + 1) % H
            if alive[im1] > 0.1 or alive[i] > 0.1 or alive[ip1] > 0.1:
                feat = np.concatenate([
                    P[im1], P[i], P[ip1],
                    [alive[im1], alive[i], alive[ip1], 1.0],
                ])
                dP[i] = feat @ K
                if alive[i] < 0.5 and (alive[im1] > 0.5 or alive[ip1] > 0.5):
                    new_alive[i] = min(1.0, alive[i] + 0.5)
        P = P + alpha * dP * dam_mask
        alive = np.maximum(alive, new_alive)
    return P


def run_probe_1(n_worlds: int = 16) -> Dict[str, Dict[str, Tuple[float, float]]]:
    H = 24
    d = 12
    coords = make_tissue_coords(H)
    F = d + 2
    g_hid = 10

    arms = [
        "direct_sgd",
        "shared_genome",
        "compartment_genome",
        "somatic_B_plus_A_regen",
        "assimilated_AB_regen",
    ]
    metrics: Dict[str, Dict[str, List[float]]] = {
        arm: {k: [] for k in ["A_after_A", "A_after_B", "B_after_B", "A_ablated", "A_regen", "B_ablated", "B_regen"]}
        for arm in arms
    }

    for w in range(n_worlds):
        taskA, taskB = make_paired_tasks(w, d=d, conflict=0.6)
        rng = np.random.default_rng(make_seed("p1_init", w))

        # 30% contiguous lesion hitting BOTH compartments (straddling the boundary)
        # so both A and B lose ~3-4 cells each
        lesion_idx = np.array([9, 10, 11, 12, 13, 14, 15])  # 7/24 = 29.2%
        alive_mask = np.ones(H, dtype=np.float64)
        alive_mask[lesion_idx] = 0.0

        # Domain receptor centers for compartments A (0..11) and B (12..23)
        mu_A = np.mean(taskA.X_tr, axis=0)
        mu_B = np.mean(taskB.X_tr, axis=0)
        mask_A = (coords[:, 2] < 0.0).astype(np.float64)
        mask_B = (coords[:, 2] >= 0.0).astype(np.float64)
        centers_AB = np.where(mask_A[:, None] > 0.5, mu_A[None, :], mu_B[None, :])
        gamma_AB = np.full(H, 2.2, dtype=np.float64)

        # --- Arm 1: direct_sgd ---
        W1 = rng.normal(0.0, 0.35, size=(H, d))
        b1 = np.zeros(H)
        w2 = rng.normal(0.0, 0.35, size=(H,))
        b2 = 0.0
        for _ in range(200):
            gW1, gb1, gw2, gb2, _, _ = mlp_grads(taskA.X_tr, taskA.y_tr, W1, b1, w2, b2)
            W1 -= 0.4 * gW1; b1 -= 0.4 * gb1; w2 -= 0.4 * gw2; b2 -= 0.4 * gb2
        a_aa = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2)
        for _ in range(200):
            gW1, gb1, gw2, gb2, _, _ = mlp_grads(taskB.X_tr, taskB.y_tr, W1, b1, w2, b2)
            W1 -= 0.4 * gW1; b1 -= 0.4 * gb1; w2 -= 0.4 * gw2; b2 -= 0.4 * gb2
        a_ab = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2)
        b_bb = mlp_acc(taskB.X_te, taskB.y_te, W1, b1, w2, b2)
        W1_d, b1_d, w2_d = W1.copy(), b1.copy(), w2.copy()
        W1_d[lesion_idx] = 0.0; b1_d[lesion_idx] = 0.0; w2_d[lesion_idx] = 0.0
        a_abl = mlp_acc(taskA.X_te, taskA.y_te, W1_d, b1_d, w2_d, b2)
        b_abl = mlp_acc(taskB.X_te, taskB.y_te, W1_d, b1_d, w2_d, b2)
        metrics["direct_sgd"]["A_after_A"].append(a_aa)
        metrics["direct_sgd"]["A_after_B"].append(a_ab)
        metrics["direct_sgd"]["B_after_B"].append(b_bb)
        metrics["direct_sgd"]["A_ablated"].append(a_abl)
        metrics["direct_sgd"]["A_regen"].append(a_abl)
        metrics["direct_sgd"]["B_ablated"].append(b_abl)
        metrics["direct_sgd"]["B_regen"].append(b_abl)

        # --- Arm 2: shared_genome ---
        G1 = rng.normal(0.0, 0.4, size=(g_hid, coords.shape[1]))
        bg1 = np.zeros(g_hid)
        G2 = rng.normal(0.0, 0.3, size=(F, g_hid))
        bg2 = np.zeros(F)
        b2_g = 0.0
        G1, bg1, G2, bg2, b2_g = train_genome(taskA, coords, G1, bg1, G2, bg2, b2_g, steps=220, lr=0.25)
        _, W1, b1, w2 = decode_genome(coords, G1, bg1, G2, bg2)
        a_aa = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2_g)
        G1, bg1, G2, bg2, b2_g = train_genome(taskB, coords, G1, bg1, G2, bg2, b2_g, steps=220, lr=0.25)
        _, W1, b1, w2 = decode_genome(coords, G1, bg1, G2, bg2)
        a_ab = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2_g)
        b_bb = mlp_acc(taskB.X_te, taskB.y_te, W1, b1, w2, b2_g)
        W1_d, b1_d, w2_d = W1.copy(), b1.copy(), w2.copy()
        W1_d[lesion_idx] = 0.0; b1_d[lesion_idx] = 0.0; w2_d[lesion_idx] = 0.0
        a_abl = mlp_acc(taskA.X_te, taskA.y_te, W1_d, b1_d, w2_d, b2_g)
        b_abl = mlp_acc(taskB.X_te, taskB.y_te, W1_d, b1_d, w2_d, b2_g)
        metrics["shared_genome"]["A_after_A"].append(a_aa)
        metrics["shared_genome"]["A_after_B"].append(a_ab)
        metrics["shared_genome"]["B_after_B"].append(b_bb)
        metrics["shared_genome"]["A_ablated"].append(a_abl)
        metrics["shared_genome"]["A_regen"].append(a_ab)  # genome re-unfolding restores current phenotype
        metrics["shared_genome"]["B_ablated"].append(b_abl)
        metrics["shared_genome"]["B_regen"].append(b_bb)

        # --- Arm 3: compartment_genome (morphogen-receptor compartmentalization) ---
        G1_a = rng.normal(0.0, 0.4, size=(g_hid, coords.shape[1]))
        bg1_a = np.zeros(g_hid)
        G2_a = rng.normal(0.0, 0.3, size=(F, g_hid))
        bg2_a = np.zeros(F)
        b2_c = 0.0
        G1_a, bg1_a, G2_a, bg2_a, b2_c = train_genome(
            taskA, coords, G1_a, bg1_a, G2_a, bg2_a, b2_c,
            steps=260, lr=0.35, cell_mask=mask_A, centers=centers_AB, gamma=gamma_AB,
        )
        _, W1_a, b1_a, w2_a = decode_genome(coords, G1_a, bg1_a, G2_a, bg2_a)
        W1_c = W1_a * mask_A[:, None]
        b1_c = b1_a * mask_A
        w2_c = w2_a * mask_A
        a_aa = mlp_acc(taskA.X_te, taskA.y_te, W1_c, b1_c, w2_c, b2_c, centers_AB, gamma_AB)

        G1_b = rng.normal(0.0, 0.4, size=(g_hid, coords.shape[1]))
        bg1_b = np.zeros(g_hid)
        G2_b = rng.normal(0.0, 0.3, size=(F, g_hid))
        bg2_b = np.zeros(F)
        G1_b, bg1_b, G2_b, bg2_b, b2_c = train_genome(
            taskB, coords, G1_b, bg1_b, G2_b, bg2_b, b2_c,
            steps=260, lr=0.35, cell_mask=mask_B, centers=centers_AB, gamma=gamma_AB,
            fixed_W1=W1_c, fixed_b1=b1_c, fixed_w2=w2_c, b2_lr_scale=0.0,
        )
        _, W1_b, b1_b, w2_b = decode_genome(coords, G1_b, bg1_b, G2_b, bg2_b)
        W1_ab = W1_c + W1_b * mask_B[:, None]
        b1_ab = b1_c + b1_b * mask_B
        w2_ab = w2_c + w2_b * mask_B
        a_ab = mlp_acc(taskA.X_te, taskA.y_te, W1_ab, b1_ab, w2_ab, b2_c, centers_AB, gamma_AB)
        b_bb = mlp_acc(taskB.X_te, taskB.y_te, W1_ab, b1_ab, w2_ab, b2_c, centers_AB, gamma_AB)
        W1_d, b1_d, w2_d = W1_ab.copy(), b1_ab.copy(), w2_ab.copy()
        W1_d[lesion_idx] = 0.0; b1_d[lesion_idx] = 0.0; w2_d[lesion_idx] = 0.0
        a_abl = mlp_acc(taskA.X_te, taskA.y_te, W1_d, b1_d, w2_d, b2_c, centers_AB, gamma_AB)
        b_abl = mlp_acc(taskB.X_te, taskB.y_te, W1_d, b1_d, w2_d, b2_c, centers_AB, gamma_AB)
        metrics["compartment_genome"]["A_after_A"].append(a_aa)
        metrics["compartment_genome"]["A_after_B"].append(a_ab)
        metrics["compartment_genome"]["B_after_B"].append(b_bb)
        metrics["compartment_genome"]["A_ablated"].append(a_abl)
        metrics["compartment_genome"]["A_regen"].append(a_ab)
        metrics["compartment_genome"]["B_ablated"].append(b_abl)
        metrics["compartment_genome"]["B_regen"].append(b_bb)

        # --- Arm 4: somatic_B_plus_A_regen (Regeneration-vs-Plasticity conflict) ---
        # Pre-B tissue has A in comp A and 0 in comp B; CA regenerator K_A learned BEFORE B.
        P_A_only = np.concatenate([W1_c, b1_c[:, None], w2_c[:, None]], axis=1)
        K_A = fit_local_ca_regenerator(P_A_only, make_seed("ca_A", w))
        # Somatic SGD on B in comp B (does NOT update K_A)
        W1_s, b1_s, w2_s = W1_c.copy(), b1_c.copy(), w2_c.copy()
        W1_s[12:] = rng.normal(0.0, 0.35, size=(12, d))
        w2_s[12:] = rng.normal(0.0, 0.35, size=(12,))
        for _ in range(220):
            gW1, gb1, gw2, _, _, _ = mlp_grads(
                taskB.X_tr, taskB.y_tr, W1_s, b1_s, w2_s, b2_c, centers_AB, gamma_AB
            )
            W1_s -= 0.5 * gW1 * mask_B[:, None]
            b1_s -= 0.5 * gb1 * mask_B
            w2_s -= 0.5 * gw2 * mask_B
        a_ab_s = mlp_acc(taskA.X_te, taskA.y_te, W1_s, b1_s, w2_s, b2_c, centers_AB, gamma_AB)
        b_bb_s = mlp_acc(taskB.X_te, taskB.y_te, W1_s, b1_s, w2_s, b2_c, centers_AB, gamma_AB)
        P_s = np.concatenate([W1_s, b1_s[:, None], w2_s[:, None]], axis=1)
        P_s_dam = P_s.copy()
        P_s_dam[lesion_idx] = 0.0
        a_abl_s = mlp_acc(taskA.X_te, taskA.y_te, P_s_dam[:, :-2], P_s_dam[:, -2], P_s_dam[:, -1], b2_c, centers_AB, gamma_AB)
        b_abl_s = mlp_acc(taskB.X_te, taskB.y_te, P_s_dam[:, :-2], P_s_dam[:, -2], P_s_dam[:, -1], b2_c, centers_AB, gamma_AB)
        # Run K_A on the whole tissue (or damaged cells): regenerates A, erases damaged B cells back to 0!
        P_s_reg = run_local_ca_regen(P_s_dam, alive_mask, K_A, steps=12, alpha=0.55)
        a_reg_s = mlp_acc(taskA.X_te, taskA.y_te, P_s_reg[:, :-2], P_s_reg[:, -2], P_s_reg[:, -1], b2_c, centers_AB, gamma_AB)
        b_reg_s = mlp_acc(taskB.X_te, taskB.y_te, P_s_reg[:, :-2], P_s_reg[:, -2], P_s_reg[:, -1], b2_c, centers_AB, gamma_AB)
        metrics["somatic_B_plus_A_regen"]["A_after_A"].append(a_aa)
        metrics["somatic_B_plus_A_regen"]["A_after_B"].append(a_ab_s)
        metrics["somatic_B_plus_A_regen"]["B_after_B"].append(b_bb_s)
        metrics["somatic_B_plus_A_regen"]["A_ablated"].append(a_abl_s)
        metrics["somatic_B_plus_A_regen"]["A_regen"].append(a_reg_s)
        metrics["somatic_B_plus_A_regen"]["B_ablated"].append(b_abl_s)
        metrics["somatic_B_plus_A_regen"]["B_regen"].append(b_reg_s)

        # --- Arm 5: assimilated_AB_regen (local CA regenerator updated after B assimilation) ---
        P_AB = np.concatenate([W1_ab, b1_ab[:, None], w2_ab[:, None]], axis=1)
        K_AB = fit_local_ca_regenerator(P_AB, make_seed("ca_AB", w))
        P_ab_dam = P_AB.copy()
        P_ab_dam[lesion_idx] = 0.0
        P_ab_reg = run_local_ca_regen(P_ab_dam, alive_mask, K_AB, steps=12, alpha=0.55)
        a_abl_ab = mlp_acc(taskA.X_te, taskA.y_te, P_ab_dam[:, :-2], P_ab_dam[:, -2], P_ab_dam[:, -1], b2_c, centers_AB, gamma_AB)
        b_abl_ab = mlp_acc(taskB.X_te, taskB.y_te, P_ab_dam[:, :-2], P_ab_dam[:, -2], P_ab_dam[:, -1], b2_c, centers_AB, gamma_AB)
        a_reg_ab = mlp_acc(taskA.X_te, taskA.y_te, P_ab_reg[:, :-2], P_ab_reg[:, -2], P_ab_reg[:, -1], b2_c, centers_AB, gamma_AB)
        b_reg_ab = mlp_acc(taskB.X_te, taskB.y_te, P_ab_reg[:, :-2], P_ab_reg[:, -2], P_ab_reg[:, -1], b2_c, centers_AB, gamma_AB)
        metrics["assimilated_AB_regen"]["A_after_A"].append(a_aa)
        metrics["assimilated_AB_regen"]["A_after_B"].append(a_ab)
        metrics["assimilated_AB_regen"]["B_after_B"].append(b_bb)
        metrics["assimilated_AB_regen"]["A_ablated"].append(a_abl_ab)
        metrics["assimilated_AB_regen"]["A_regen"].append(a_reg_ab)
        metrics["assimilated_AB_regen"]["B_ablated"].append(b_abl_ab)
        metrics["assimilated_AB_regen"]["B_regen"].append(b_reg_ab)

    return {arm: {k: mean_ci95(v) for k, v in d_.items()} for arm, d_ in metrics.items()}


# ---------------------------------------------------------------------------
# Probe 2: Growth-Induced Drift & Readout Spillover (2x2 ablation)
# ---------------------------------------------------------------------------

def run_probe_2(n_worlds: int = 16) -> Dict[str, Dict[str, Tuple[float, float]]]:
    d = 12
    H0 = 16
    H1 = 32
    arms = [
        "naive_grow",
        "ewc_grow",
        "oracle_freeze_grow",
        "trophic_only_grow",
        "receptor_only_grow",
        "trophic_receptor_grow",
    ]
    metrics: Dict[str, Dict[str, List[float]]] = {
        arm: {k: [] for k in ["A_after_A", "A_after_B", "A_drop", "B_after_B", "A_after_prune25"]}
        for arm in arms
    }

    for w in range(n_worlds):
        taskA, taskB = make_paired_tasks(w + 1000, d=d, conflict=0.6)
        rng = np.random.default_rng(make_seed("p2_init", w))
        mu_A = np.mean(taskA.X_tr, axis=0)
        mu_B = np.mean(taskB.X_tr, axis=0)

        # Train base H0=16 network on Task A with local receptor centered on A
        # (and also evaluate a global-receptor base for the non-receptor arms)
        W1_0_init = rng.normal(0.0, 0.35, size=(H0, d))
        b1_0_init = np.zeros(H0)
        w2_0_init = rng.normal(0.0, 0.35, size=(H0,))

        def train_base(use_receptor: bool):
            W1 = W1_0_init.copy()
            b1 = b1_0_init.copy()
            w2 = w2_0_init.copy()
            b2 = 0.0
            centers = np.repeat(mu_A[None, :], H0, axis=0) if use_receptor else None
            gamma = np.full(H0, 2.2) if use_receptor else None
            trophic = np.zeros(H0)
            for _ in range(200):
                gW1, gb1, gw2, gb2, h, p = mlp_grads(taskA.X_tr, taskA.y_tr, W1, b1, w2, b2, centers, gamma)
                lr = 0.6 if use_receptor else 0.4
                W1 -= lr * gW1; b1 -= lr * gb1; w2 -= lr * gw2; b2 -= lr * gb2
                correct = (((p > 0.5) == (taskA.y_tr > 0.5)).astype(np.float64))[:, None]
                contrib = np.mean(np.abs(h * w2[None, :]) * correct, axis=0)
                trophic = 0.9 * trophic + 0.1 * contrib
            a_acc = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2, centers, gamma)
            # Empirical diagonal Fisher on Task A
            raw_h, gate, h_a, _, p_a = mlp_forward(taskA.X_tr, W1, b1, w2, b2, centers, gamma)
            err = (p_a - taskA.y_tr)
            f_w2 = np.mean((h_a * err[:, None]) ** 2, axis=0)
            dz_all = (err[:, None] * w2[None, :]) * gate * (1.0 - raw_h * raw_h)
            f_b1 = np.mean(dz_all ** 2, axis=0)
            f_W1 = np.mean((dz_all[:, :, None] * taskA.X_tr[:, None, :]) ** 2, axis=0)
            return W1, b1, w2, b2, trophic, a_acc, (f_W1, f_b1, f_w2)

        base_global = train_base(use_receptor=False)
        base_rec = train_base(use_receptor=True)

        W1_new_init = rng.normal(0.0, 0.35, size=(H1 - H0, d))
        b1_new_init = np.zeros(H1 - H0)
        w2_new_small = rng.normal(0.0, 0.08, size=(H1 - H0,))

        for arm in arms:
            use_rec = arm in ("receptor_only_grow", "trophic_receptor_grow")
            W1_0, b1_0, w2_0, b2_0, trophic_0, a_base, (f_W1, f_b1, f_w2) = base_rec if use_rec else base_global

            W1 = np.vstack([W1_0.copy(), W1_new_init.copy()])
            b1 = np.concatenate([b1_0.copy(), b1_new_init.copy()])
            if arm in ("naive_grow", "ewc_grow"):
                w2 = np.concatenate([w2_0.copy(), np.zeros(H1 - H0)])
            else:
                w2 = np.concatenate([w2_0.copy(), w2_new_small.copy()])
            b2 = float(b2_0)

            centers = (
                np.vstack([np.repeat(mu_A[None, :], H0, axis=0), np.repeat(mu_B[None, :], H1 - H0, axis=0)])
                if use_rec
                else None
            )
            gamma = np.full(H1, 2.2) if use_rec else None

            W1_anchor, b1_anchor, w2_anchor = W1.copy(), b1.copy(), w2.copy()
            F_W1 = np.vstack([f_W1, np.zeros_like(W1_new_init)])
            F_b1 = np.concatenate([f_b1, np.zeros(H1 - H0)])
            F_w2 = np.concatenate([f_w2, np.zeros(H1 - H0)])
            trophic = np.concatenate([trophic_0.copy(), np.zeros(H1 - H0)])

            lr = 0.6 if use_rec else 0.4
            for _ in range(200):
                gW1, gb1, gw2, gb2, h, p = mlp_grads(taskB.X_tr, taskB.y_tr, W1, b1, w2, b2, centers, gamma)
                if arm in ("naive_grow", "receptor_only_grow"):
                    W1 -= lr * gW1; b1 -= lr * gb1; w2 -= lr * gw2; b2 -= 0.1 * lr * gb2
                elif arm == "ewc_grow":
                    lam = 200.0
                    W1 -= lr * (gW1 + lam * F_W1 * (W1 - W1_anchor))
                    b1 -= lr * (gb1 + lam * F_b1 * (b1 - b1_anchor))
                    w2 -= lr * (gw2 + lam * F_w2 * (w2 - w2_anchor))
                    b2 -= 0.1 * lr * gb2
                elif arm == "oracle_freeze_grow":
                    mask = np.concatenate([np.zeros(H0), np.ones(H1 - H0)])
                    W1 -= lr * gW1 * mask[:, None]
                    b1 -= lr * gb1 * mask
                    w2 -= lr * gw2 * mask
                    b2 -= 0.0 * gb2
                elif arm in ("trophic_only_grow", "trophic_receptor_grow"):
                    # Strictly local Notch-like plasticity lock from trophic survival signal
                    plast = 1.0 / (1.0 + 40.0 * (trophic / (np.mean(trophic_0) + 1e-6)) ** 2)
                    W1 -= lr * gW1 * plast[:, None]
                    b1 -= lr * gb1 * plast
                    w2 -= lr * gw2 * plast
                    b2 -= 0.05 * lr * gb2
                    correct = (((p > 0.5) == (taskB.y_tr > 0.5)).astype(np.float64))[:, None]
                    contrib = np.mean(np.abs(h * w2[None, :]) * correct, axis=0)
                    trophic = np.maximum(trophic, 0.9 * trophic + 0.1 * contrib)

            a_after = mlp_acc(taskA.X_te, taskA.y_te, W1, b1, w2, b2, centers, gamma)
            b_after = mlp_acc(taskB.X_te, taskB.y_te, W1, b1, w2, b2, centers, gamma)

            k_prune = H1 // 4
            if arm in ("trophic_only_grow", "trophic_receptor_grow"):
                prune_idx = np.argsort(trophic)[:k_prune]
            else:
                prune_idx = np.argsort(np.abs(w2))[:k_prune]
            W1_p, b1_p, w2_p = W1.copy(), b1.copy(), w2.copy()
            W1_p[prune_idx] = 0.0; b1_p[prune_idx] = 0.0; w2_p[prune_idx] = 0.0
            a_prune = mlp_acc(taskA.X_te, taskA.y_te, W1_p, b1_p, w2_p, b2, centers, gamma)

            metrics[arm]["A_after_A"].append(a_base)
            metrics[arm]["A_after_B"].append(a_after)
            metrics[arm]["A_drop"].append(a_base - a_after)
            metrics[arm]["B_after_B"].append(b_after)
            metrics[arm]["A_after_prune25"].append(a_prune)

    return {arm: {k: mean_ci95(v) for k, v in d_.items()} for arm, d_ in metrics.items()}


def fmt(mc: Tuple[float, float]) -> str:
    return f"{mc[0]:5.1f} +/- {mc[1]:4.1f}"


def main() -> None:
    t0 = time.time()
    print("=== Probe 1: Genotype-Phenotype Dilemma (16 paired worlds, 29.2% boundary lesion) ===")
    p1 = run_probe_1(16)
    print(f"{'Arm':<26} | {'A@A':^14} | {'A@B':^14} | {'B@B':^14} | {'A_abl -> A_reg':^29} | {'B_abl -> B_reg':^29}")
    print("-" * 134)
    for arm, d_ in p1.items():
        print(
            f"{arm:<26} | {fmt(d_['A_after_A'])} | {fmt(d_['A_after_B'])} | {fmt(d_['B_after_B'])} | "
            f"{fmt(d_['A_ablated'])} -> {fmt(d_['A_regen'])} | {fmt(d_['B_ablated'])} -> {fmt(d_['B_regen'])}"
        )

    print("\n=== Probe 2: Growth-Induced Drift & Readout Spillover (16 paired worlds, task-ID-free) ===")
    p2 = run_probe_2(16)
    print(f"{'Arm':<24} | {'A@A':^14} | {'A@B':^14} | {'A_drop':^14} | {'B@B':^14} | {'A_prune25%':^14}")
    print("-" * 107)
    for arm, d_ in p2.items():
        print(
            f"{arm:<24} | {fmt(d_['A_after_A'])} | {fmt(d_['A_after_B'])} | {fmt(d_['A_drop'])} | "
            f"{fmt(d_['B_after_B'])} | {fmt(d_['A_after_prune25'])}"
        )
    print(f"\nElapsed: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
