"""Matched-compute pretraining for Model A (StandardLM) and Model B (WritableLM).

Both models see the exact same data distribution (static background knowledge +
episodic fresh-fact worlds with recall, paraphrase, inverse, and 2-hop QA) and
are trained to the exact same compute budget (matched total FLOPs).
"""

from __future__ import annotations

import json
import math
import os
import random
import time
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from writable_pretrain.data import (
    Episode,
    KnowledgeWorld,
    QAItem,
    SimpleWordTokenizer,
    encode_qa_example,
    format_qa_prompt,
)
from writable_pretrain.model import ModelConfig, TinyLM, detach_mem_states, index_mem_states


@dataclass
class TrainConfig:
    mode: str = "standard"           # "standard" (Model A) or "writable" (Model B)
    scale: str = "pilot"             # "pilot" (~2.6M) or "20m" (~20M)
    seed: int = 42
    max_flops: float = 2.0e14        # Exact compute budget (6 * N_params * tokens)
    max_steps: int = 100000          # Safety cap; stopping is controlled by max_flops
    lr: float = 1.0e-3
    min_lr: float = 1.0e-4
    weight_decay: float = 0.02
    warmup_frac: float = 0.05
    stable_frac: float = 0.65
    grad_clip: float = 1.0
    batch_episodes: int = 4          # Episodes per optimizer step
    q_per_episode: int = 4           # QA items per episode (1 recall, 1 para, 1 inv, 1 2-hop)
    min_chains: int = 2              # 6 facts min
    max_chains: int = 4              # 12 facts max
    static_per_step: int = 8         # Static background QA items per step
    writable_prob: float = 0.80      # For Model B: fraction of episodes in write-to-memory mode
    b_static_with_mem_prob: float = 0.40  # For Model B: train static QA with active unrelated M (anti-drift)
    log_every: int = 25
    save_every_flops: float = 0.0    # Optional intermediate checkpoints
    out_dir: str = "runs/pilot_a"
    num_threads: int = 8


def _pad_2d(seqs: List[List[int]], pad_id: int) -> Tuple[torch.Tensor, torch.Tensor]:
    max_len = max(len(s) for s in seqs)
    B = len(seqs)
    ids = torch.full((B, max_len), pad_id, dtype=torch.long)
    lens = torch.zeros(B, dtype=torch.long)
    for i, s in enumerate(seqs):
        ids[i, :len(s)] = torch.tensor(s, dtype=torch.long)
        lens[i] = len(s)
    return ids, lens


def _pad_qa_batch(
    pairs: List[Tuple[List[int], List[int]]],
    pad_id: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return (inputs, targets, loss_mask) of shape (B, T-1)."""
    max_len = max(len(ids) for ids, _ in pairs)
    B = len(pairs)
    inp = torch.full((B, max_len - 1), pad_id, dtype=torch.long)
    tgt = torch.full((B, max_len - 1), pad_id, dtype=torch.long)
    msk = torch.zeros((B, max_len - 1), dtype=torch.float32)
    for i, (ids, m) in enumerate(pairs):
        L = len(ids) - 1
        inp[i, :L] = torch.tensor(ids[:-1], dtype=torch.long)
        tgt[i, :L] = torch.tensor(ids[1:], dtype=torch.long)
        msk[i, :L] = torch.tensor(m, dtype=torch.float32)
    return inp, tgt, msk


def _pack_context_qas(
    tok: SimpleWordTokenizer,
    facts: Sequence[str],
    qas: Sequence[QAItem],
) -> Tuple[List[int], List[int]]:
    """Pack `[context: <facts>] [query: q1 answer: a1 <SEP> query: q2 answer: a2 ...]`
    into one causal sequence. Loss mask is 1 on all answer + EOS/SEP tokens.
    """
    ctx_str = "context : " + " ".join(facts)
    ids = tok.encode(ctx_str, add_bos=True, add_eos=False)
    mask: List[float] = [0.0] * (len(ids) - 1)
    for idx, qa in enumerate(qas):
        q_str = f"query : {qa.question} answer :"
        q_ids = tok.encode(q_str, add_bos=False, add_eos=False)
        a_ids = tok.encode(qa.answer, add_bos=False, add_eos=False)
        end_tok = [tok.eos_id if idx == len(qas) - 1 else tok.sep_id]
        ids.extend(q_ids)
        mask.extend([0.0] * len(q_ids))
        ids.extend(a_ids + end_tok)
        mask.extend([1.0] * (len(a_ids) + 1))
    return ids, mask


def _sample_balanced_qas(ep: Episode, k: int, rng: random.Random) -> List[QAItem]:
    """Sample k QAs balanced across recall, paraphrase, inverse, two_hop,
    avoiding duplicate chains within the same packed batch when possible.
    """
    by_cat: Dict[str, List[QAItem]] = {"recall": [], "paraphrase": [], "inverse": [], "two_hop": []}
    for qa in ep.qas:
        if qa.category in by_cat:
            by_cat[qa.category].append(qa)
    out: List[QAItem] = []
    cats = ["recall", "paraphrase", "inverse", "two_hop"]
    per_cat = max(1, k // len(cats))
    for c in cats:
        pool = by_cat[c]
        if len(pool) >= per_cat:
            out.extend(rng.sample(pool, per_cat))
        else:
            out.extend(pool)
    rng.shuffle(out)
    return out[:k]


def _encode_facts_3d(
    tok: SimpleWordTokenizer,
    episodes: List[Episode],
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return (fact_ids, fact_lens, fact_valid) of shape (B, M_max, T_max)."""
    B = len(episodes)
    M_max = max(len(ep.facts) for ep in episodes)
    encoded = [
        [tok.encode(f, add_bos=True, add_eos=True) for f in ep.facts]
        for ep in episodes
    ]
    T_max = max(len(f) for ep_f in encoded for f in ep_f)
    fact_ids = torch.full((B, M_max, T_max), tok.pad_id, dtype=torch.long)
    fact_lens = torch.zeros((B, M_max), dtype=torch.long)
    fact_valid = torch.zeros((B, M_max), dtype=torch.bool)
    for b, ep_f in enumerate(encoded):
        for m, seq in enumerate(ep_f):
            fact_ids[b, m, :len(seq)] = torch.tensor(seq, dtype=torch.long)
            fact_lens[b, m] = len(seq)
            fact_valid[b, m] = True
    return fact_ids, fact_lens, fact_valid


def masked_ce_loss(
    logits: torch.Tensor,
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> Tuple[torch.Tensor, float]:
    V = logits.size(-1)
    ce = F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1), reduction="none").view_as(targets)
    denom = mask.sum().clamp(min=1.0)
    loss = (ce * mask).sum() / denom
    # Exact token accuracy on answer tokens (mask >= 0.5)
    ans_mask = mask >= 0.5
    if ans_mask.any():
        preds = logits.argmax(dim=-1)
        acc = ((preds == targets) & ans_mask).float().sum().item() / ans_mask.float().sum().item()
    else:
        acc = 0.0
    return loss, acc


def get_lr(flops_done: float, cfg: TrainConfig) -> float:
    """Warmup-Stable-Decay (WSD) schedule so models clear phase transitions before decaying."""
    frac = min(max(flops_done / cfg.max_flops, 0.0), 1.0)
    if frac < cfg.warmup_frac:
        return cfg.lr * (frac / max(cfg.warmup_frac, 1e-6))
    decay_start = cfg.warmup_frac + cfg.stable_frac
    if frac < decay_start:
        return cfg.lr
    prog = (frac - decay_start) / max(1.0 - decay_start, 1e-6)
    return cfg.min_lr + 0.5 * (cfg.lr - cfg.min_lr) * (1.0 + math.cos(math.pi * prog))


def save_checkpoint(
    path: str,
    model: TinyLM,
    train_cfg: TrainConfig,
    step: int,
    flops_done: float,
    tokens_done: int,
    wall_s: float,
) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "model_cfg": asdict(model.cfg),
        "train_cfg": asdict(train_cfg),
        "step": step,
        "flops_done": flops_done,
        "tokens_done": tokens_done,
        "wall_s": wall_s,
    }, path)


def train_model(cfg: TrainConfig) -> Dict[str, float]:
    torch.set_num_threads(cfg.num_threads)
    torch.manual_seed(cfg.seed)
    rng = random.Random(cfg.seed)

    tok = SimpleWordTokenizer(target_vocab_size=1024)
    world = KnowledgeWorld(seed=42, n_static_chains=16)

    if cfg.scale == "20m":
        mcfg = ModelConfig.writable_20m(tok.vocab_size) if cfg.mode == "writable" else ModelConfig.standard_20m(tok.vocab_size)
    elif cfg.scale == "pilot":
        mcfg = ModelConfig.writable_pilot(tok.vocab_size) if cfg.mode == "writable" else ModelConfig.standard_pilot(tok.vocab_size)
    elif cfg.scale == "small":
        mcfg = ModelConfig.writable_small(tok.vocab_size) if cfg.mode == "writable" else ModelConfig.standard_small(tok.vocab_size)
    else:
        raise ValueError(f"Unknown scale: {cfg.scale}")

    model = TinyLM(mcfg)
    n_params = model.count_parameters()
    os.makedirs(cfg.out_dir, exist_ok=True)

    # AdamW with decoupled weight decay (no decay on norms/biases)
    decay_p = [p for n, p in model.named_parameters() if p.dim() >= 2]
    nodecay_p = [p for n, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW(
        [{"params": decay_p, "weight_decay": cfg.weight_decay},
         {"params": nodecay_p, "weight_decay": 0.0}],
        lr=cfg.lr,
        betas=(0.9, 0.95),
    )

    flops_done = 0.0
    tokens_done = 0
    step = 0
    next_save_flops = cfg.save_every_flops if cfg.save_every_flops > 0 else float("inf")
    t0 = time.time()
    log_path = os.path.join(cfg.out_dir, "train_log.jsonl")
    log_f = open(log_path, "w")

    print(
        f"[{cfg.mode}/{cfg.scale}] params={n_params/1e6:.2f}M "
        f"max_flops={cfg.max_flops:.2e} out={cfg.out_dir}",
        flush=True,
    )

    # Weight fraction of layers executed during Model B write_facts (layers 0..max(mem_layers))
    write_layer_frac = (max(mcfg.mem_layers) + 1) / mcfg.n_layers if mcfg.is_writable else 1.0

    model.train()
    while flops_done < cfg.max_flops and step < cfg.max_steps:
        step += 1
        lr_now = get_lr(flops_done, cfg)
        for pg in opt.param_groups:
            pg["lr"] = lr_now

        opt.zero_grad(set_to_none=True)
        step_tokens = 0
        step_flops = 0.0

        # 1. Sample episodes with identical curriculum for A and B
        frac_done = flops_done / max(cfg.max_flops, 1.0)
        if frac_done < 0.20:
            lo_c, hi_c = 1, 2
        elif frac_done < 0.50:
            lo_c, hi_c = 1, min(4, cfg.max_chains)
        else:
            lo_c, hi_c = min(2, cfg.min_chains), cfg.max_chains

        episodes = [
            world.sample_episode(
                split="train",
                n_chains=rng.randint(lo_c, hi_c),
                rng=rng,
                use_heldout_templates=False,
                shuffle_facts=True,
            )
            for _ in range(cfg.batch_episodes)
        ]
        ep_qas = [_sample_balanced_qas(ep, cfg.q_per_episode, rng) for ep in episodes]
        static_qas = rng.sample(world.static_qas, min(cfg.static_per_step, len(world.static_qas)))
        static_facts = rng.sample(world.static_facts, min(cfg.static_per_step, len(world.static_facts)))

        # Decide episode mode for Model B (always draw RNG so A and B stay aligned)
        use_write_mode = (rng.random() < cfg.writable_prob) and (cfg.mode == "writable")

        # 2. Episodic loss
        if not use_write_mode:
            # Standard in-context episode (Model A always; Model B 20% of steps).
            # Each QA is evaluated independently (matching test-time ICL format, zero cross-QA leakage).
            ctx_pairs: List[Tuple[List[int], List[int]]] = []
            for ep, qas in zip(episodes, ep_qas):
                for qa in qas:
                    ctx_pairs.append(encode_qa_example(tok, qa.question, qa.answer, context_facts=ep.facts))
            inp, tgt, msk = _pad_qa_batch(ctx_pairs, tok.pad_id)
            logits = model(inp, mem_states=None)
            ep_loss, ep_acc = masked_ce_loss(logits, tgt, msk)
            n_tok = int((inp != tok.pad_id).sum().item())
            step_tokens += n_tok
            step_flops += 6.0 * n_params * n_tok
            active_mem_for_static = None
        else:
            # Model B write-to-memory mode: facts are NEVER in context at question time!
            fact_ids, fact_lens, fact_valid = _encode_facts_3d(tok, episodes)
            mem_states = model.write_facts(fact_ids, fact_lens, fact_valid)
            n_write_tok = int(fact_lens.sum().item())
            step_tokens += n_write_tok
            step_flops += 6.0 * (n_params * write_layer_frac) * n_write_tok

            # Build question-only batch (B_ep * Q_ep) and broadcast each episode's M across its Q_ep questions
            q_pairs: List[Tuple[List[int], List[int]]] = []
            ep_indices: List[int] = []
            for b_idx, qas in enumerate(ep_qas):
                for qa in qas:
                    q_pairs.append(encode_qa_example(tok, qa.question, qa.answer, context_facts=None))
                    ep_indices.append(b_idx)
            q_inp, q_tgt, q_msk = _pad_qa_batch(q_pairs, tok.pad_id)
            idx_t = torch.tensor(ep_indices, dtype=torch.long)
            bcast_mem = index_mem_states(mem_states, idx_t)
            q_logits = model(q_inp, mem_states=bcast_mem)
            ep_loss, ep_acc = masked_ce_loss(q_logits, q_tgt, q_msk)
            n_q_tok = int((q_inp != tok.pad_id).sum().item())
            step_tokens += n_q_tok
            step_flops += 6.0 * n_params * n_q_tok

            # Detached active memory for anti-drift static regularization
            active_mem_for_static = detach_mem_states(mem_states)

        # 3. Static world knowledge loss (both A and B memorize static world facts)
        st_pairs = [encode_qa_example(tok, qa.question, qa.answer, context_facts=None) for qa in static_qas]
        # Also include raw static fact statements for LM fluency
        for sf in static_facts[:4]:
            f_ids = tok.encode(sf, add_bos=True, add_eos=True)
            st_pairs.append((f_ids, [0.25] * (len(f_ids) - 1)))
        st_inp, st_tgt, st_msk = _pad_qa_batch(st_pairs, tok.pad_id)

        st_mem = None
        if cfg.mode == "writable" and active_mem_for_static is not None and rng.random() < cfg.b_static_with_mem_prob:
            # Broadcast unrelated episode memory onto static questions so Model B learns zero-interference!
            B_st = st_inp.size(0)
            rep_idx = torch.arange(B_st) % active_mem_for_static[0][0].size(0)
            st_mem = index_mem_states(active_mem_for_static, rep_idx)

        st_logits = model(st_inp, mem_states=st_mem)
        st_loss, st_acc = masked_ce_loss(st_logits, st_tgt, st_msk)
        n_st_tok = int((st_inp != tok.pad_id).sum().item())
        step_tokens += n_st_tok
        step_flops += 6.0 * n_params * n_st_tok

        total_loss = ep_loss + 0.5 * st_loss
        total_loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        opt.step()

        flops_done += step_flops
        tokens_done += step_tokens

        if step % cfg.log_every == 0 or flops_done >= cfg.max_flops:
            wall_s = time.time() - t0
            rec = {
                "step": step,
                "flops": flops_done,
                "tokens": tokens_done,
                "wall_s": round(wall_s, 1),
                "tok_s": round(tokens_done / max(wall_s, 1e-6), 1),
                "lr": round(lr_now, 6),
                "mode_step": "write" if use_write_mode else "text",
                "ep_loss": round(ep_loss.item(), 4),
                "ep_acc": round(ep_acc, 4),
                "st_loss": round(st_loss.item(), 4),
                "st_acc": round(st_acc, 4),
            }
            log_f.write(json.dumps(rec) + "\n")
            log_f.flush()
            print(
                f"step={step:4d} flops={flops_done:.2e}/{cfg.max_flops:.2e} "
                f"tok={tokens_done/1e3:6.1f}k ({rec['tok_s']:.0f} tok/s) "
                f"[{rec['mode_step']:5s}] ep_loss={rec['ep_loss']:.3f} ep_acc={rec['ep_acc']:.3f} "
                f"st_acc={rec['st_acc']:.3f} wall={wall_s:.0f}s",
                flush=True,
            )

        if flops_done >= next_save_flops:
            ckpt_path = os.path.join(cfg.out_dir, f"ckpt_flops_{int(flops_done/1e12)}T.pt")
            save_checkpoint(ckpt_path, model, cfg, step, flops_done, tokens_done, time.time() - t0)
            next_save_flops += cfg.save_every_flops

    wall_s = time.time() - t0
    final_path = os.path.join(cfg.out_dir, "final.pt")
    save_checkpoint(final_path, model, cfg, step, flops_done, tokens_done, wall_s)
    log_f.close()
    print(
        f"[{cfg.mode}/{cfg.scale}] DONE step={step} flops={flops_done:.2e} "
        f"tokens={tokens_done} wall={wall_s:.1f}s saved={final_path}",
        flush=True,
    )
    return {
        "step": step,
        "flops_done": flops_done,
        "tokens_done": tokens_done,
        "wall_s": wall_s,
        "n_params": n_params,
        "final_path": final_path,
    }


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["standard", "writable"], required=True)
    p.add_argument("--scale", choices=["small", "pilot", "20m"], default="pilot")
    p.add_argument("--max_flops", type=float, default=2.0e14)
    p.add_argument("--save_every_flops", type=float, default=0.0)
    p.add_argument("--lr", type=float, default=6e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out_dir", type=str, required=True)
    p.add_argument("--threads", type=int, default=8)
    args = p.parse_args()

    tcfg = TrainConfig(
        mode=args.mode,
        scale=args.scale,
        max_flops=args.max_flops,
        save_every_flops=args.save_every_flops,
        lr=args.lr,
        seed=args.seed,
        out_dir=args.out_dir,
        num_threads=args.threads,
    )
    train_model(tcfg)
