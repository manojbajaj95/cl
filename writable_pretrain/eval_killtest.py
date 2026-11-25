"""Text-vs-write kill test on fresh fictional facts for Model A and Model B.

Evaluates:
- Text baselines: A-Text-ICL, A-Text-RAG, B-Text-ICL, B-Text-RAG
- Model A write methods (dev-tuned): A-FT-full, A-FT-MLP, A-FT-LoRA, A-FT-replay
- Model B learned write: B-Write (single forward write to designated memory block M)

Scores:
- Recall (exact match on 2-token answer entity)
- Paraphrase (held-out unseen templates + train templates)
- Cue-free Inverse (object -> subject, no forward fact in context)
- Cue-free 2-hop (A -> C across two separate facts A->B, B->C; B never named)
- Drift (Delta Accuracy and Delta NLL on static world knowledge with new facts written/active)

Kill rule: B-Write must beat Text where A-Write loses.
"""

from __future__ import annotations

import copy
import json
import math
import os
import random
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from writable_pretrain.data import (
    BM25Retriever,
    Episode,
    KnowledgeWorld,
    QAItem,
    SimpleWordTokenizer,
    encode_qa_example,
    format_qa_prompt,
)
from writable_pretrain.model import ModelConfig, TinyLM


def load_checkpoint(path: str) -> Tuple[TinyLM, Dict]:
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    mcfg = ModelConfig(**ckpt["model_cfg"])
    model = TinyLM(mcfg)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model, ckpt


def _encode_facts_single(tok: SimpleWordTokenizer, facts: Sequence[str]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    encoded = [tok.encode(f, add_bos=True, add_eos=True) for f in facts]
    M = len(encoded)
    T = max(len(s) for s in encoded)
    f_ids = torch.full((1, M, T), tok.pad_id, dtype=torch.long)
    f_lens = torch.zeros((1, M), dtype=torch.long)
    f_valid = torch.ones((1, M), dtype=torch.bool)
    for m, seq in enumerate(encoded):
        f_ids[0, m, :len(seq)] = torch.tensor(seq, dtype=torch.long)
        f_lens[0, m] = len(seq)
    return f_ids, f_lens, f_valid


@torch.no_grad()
def eval_qa_list(
    model: TinyLM,
    tok: SimpleWordTokenizer,
    qas: Sequence[QAItem],
    context_fn=None,
    mem_states: Optional[List[torch.Tensor]] = None,
) -> Dict[str, float]:
    """Evaluate exact-match accuracy and answer-token NLL on a list of QAItems."""
    model.eval()
    correct = 0
    total = 0
    nll_sum = 0.0
    tok_count = 0

    for qa in qas:
        ctx = context_fn(qa) if context_fn is not None else None
        prompt = format_qa_prompt(qa.question, ctx)
        p_ids = tok.encode(prompt, add_bos=True, add_eos=False)
        a_ids = tok.encode(qa.answer, add_bos=False, add_eos=True)

        # Greedy exact match
        p_t = torch.tensor([p_ids], dtype=torch.long)
        gen = model.generate_answer(p_t, max_new_tokens=len(a_ids), eos_id=tok.eos_id, mem_states=mem_states)[0].tolist()
        # Strip EOS and compare
        gen_clean = []
        for g in gen:
            if g == tok.eos_id:
                break
            gen_clean.append(g)
        target_clean = [t for t in a_ids if t != tok.eos_id]
        if gen_clean == target_clean:
            correct += 1
        total += 1

        # NLL on answer tokens
        full = torch.tensor([p_ids + a_ids], dtype=torch.long)
        logits = model(full[:, :-1], mem_states=mem_states)
        start = len(p_ids) - 1
        ans_logits = logits[0, start:start + len(a_ids)]
        ans_tgt = torch.tensor(a_ids, dtype=torch.long)
        nll_sum += F.cross_entropy(ans_logits, ans_tgt, reduction="sum").item()
        tok_count += len(a_ids)

    return {
        "acc": correct / max(total, 1),
        "nll": nll_sum / max(tok_count, 1),
        "n": total,
    }


def _derive_forward_qa_from_fact(fact: str) -> Optional[Tuple[str, str]]:
    """Mechanically convert a raw forward fact statement into its canonical forward QA.
    Used to give Model A fine-tuning its strongest possible shot (still strictly forward,
    zero inverse or 2-hop supervision).
    """
    m = re.match(r"^(.+?) works at (.+?) \.$", fact)
    if m:
        return f"where does {m.group(1)} work ?", m.group(2)
    m = re.match(r"^(.+?) is located in (.+?) \.$", fact)
    if m:
        return f"where is {m.group(1)} located ?", m.group(2)
    m = re.match(r"^(.+?) leads the (.+?) project \.$", fact)
    if m:
        return f"which project does {m.group(1)} lead ?", m.group(2)
    return None


class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, rank: int = 8, alpha: float = 16.0):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad_(False)
        self.rank = rank
        self.scale = alpha / rank
        self.A = nn.Parameter(torch.randn(rank, base.in_features) * (1.0 / math.sqrt(base.in_features)))
        self.B = nn.Parameter(torch.zeros(base.out_features, rank))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.base(x) + (x @ self.A.t() @ self.B.t()) * self.scale


def _apply_lora(model: TinyLM, rank: int = 8) -> List[nn.Parameter]:
    for p in model.parameters():
        p.requires_grad_(False)
    lora_params: List[nn.Parameter] = []
    for block in model.blocks:
        block.attn.qkv = LoRALinear(block.attn.qkv, rank=rank)
        block.attn.out = LoRALinear(block.attn.out, rank=rank)
        block.ffn.w_down = LoRALinear(block.ffn.w_down, rank=rank)
        for mod in (block.attn.qkv, block.attn.out, block.ffn.w_down):
            lora_params.extend([mod.A, mod.B])
    return lora_params


def finetune_model_a(
    base_model: TinyLM,
    tok: SimpleWordTokenizer,
    facts: Sequence[str],
    method: str = "full",
    lr: float = 3e-4,
    steps: int = 25,
    replay_qas: Optional[Sequence[QAItem]] = None,
    seed: int = 0,
) -> TinyLM:
    """Write fresh fictional facts into a copy of Model A via gradient fine-tuning/patching.

    Methods:
      - 'full': full-parameter AdamW on raw facts + mechanically derived forward QAs
      - 'mlp_patch': only layers 2 and 4 FFN weights (matching Model B's memory layer locations)
      - 'lora': rank-8 LoRA adapters on attention & FFN down-proj
      - 'replay': full-parameter AdamW mixed with a small static replay buffer (anti-drift)
    """
    torch.manual_seed(seed)
    rng = random.Random(seed)
    model = copy.deepcopy(base_model)
    model.train()

    if method == "lora":
        params = _apply_lora(model, rank=8)
    elif method == "mlp_patch":
        for p in model.parameters():
            p.requires_grad_(False)
        params = []
        for idx in (2, 4):
            if idx < len(model.blocks):
                for p in model.blocks[idx].ffn.parameters():
                    p.requires_grad_(True)
                    params.append(p)
    elif method in ("full", "replay"):
        for p in model.parameters():
            p.requires_grad_(True)
        params = list(model.parameters())
    else:
        raise ValueError(f"Unknown Model A write method: {method}")

    # Build training examples from the raw forward facts ONLY (no inverse, no 2-hop, no paraphrase!)
    examples: List[Tuple[List[int], List[int]]] = []
    for f in facts:
        f_ids = tok.encode(f, add_bos=True, add_eos=True)
        examples.append((f_ids, [1.0] * (len(f_ids) - 1)))
        fwd = _derive_forward_qa_from_fact(f)
        if fwd is not None:
            q, a = fwd
            examples.append(encode_qa_example(tok, q, a, context_facts=None))

    replay_examples: List[Tuple[List[int], List[int]]] = []
    if method == "replay" and replay_qas:
        for qa in replay_qas:
            replay_examples.append(encode_qa_example(tok, qa.question, qa.answer, context_facts=None))

    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)

    for _ in range(steps):
        batch = list(examples)
        if replay_examples:
            batch.extend(rng.sample(replay_examples, min(8, len(replay_examples))))
        max_len = max(len(ids) for ids, _ in batch)
        B = len(batch)
        inp = torch.full((B, max_len - 1), tok.pad_id, dtype=torch.long)
        tgt = torch.full((B, max_len - 1), tok.pad_id, dtype=torch.long)
        msk = torch.zeros((B, max_len - 1), dtype=torch.float32)
        for i, (ids, m) in enumerate(batch):
            L = len(ids) - 1
            inp[i, :L] = torch.tensor(ids[:-1], dtype=torch.long)
            tgt[i, :L] = torch.tensor(ids[1:], dtype=torch.long)
            msk[i, :L] = torch.tensor(m, dtype=torch.float32)

        opt.zero_grad(set_to_none=True)
        logits = model(inp, mem_states=None)
        V = logits.size(-1)
        ce = F.cross_entropy(logits.reshape(-1, V), tgt.reshape(-1), reduction="none").view_as(tgt)
        loss = (ce * msk).sum() / msk.sum().clamp(min=1.0)
        loss.backward()
        nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()

    model.eval()
    return model


def _eval_episode_categories(
    model: TinyLM,
    tok: SimpleWordTokenizer,
    ep: Episode,
    context_fn=None,
    mem_states: Optional[List[torch.Tensor]] = None,
) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for cat in ("recall", "paraphrase", "inverse", "two_hop"):
        sub = [qa for qa in ep.qas if qa.category == cat]
        res = eval_qa_list(model, tok, sub, context_fn=context_fn, mem_states=mem_states)
        out[cat] = res["acc"]
    return out


def tune_model_a_on_dev(
    model_a: TinyLM,
    tok: SimpleWordTokenizer,
    world: KnowledgeWorld,
    n_chains: int = 4,
    seed: int = 100,
) -> Dict[str, Tuple[float, int]]:
    """Select best (lr, steps) for each Model A write method on the disjoint dev split."""
    rng = random.Random(seed)
    dev_ep = world.sample_episode("dev", n_chains=n_chains, rng=rng, use_heldout_templates=True)
    static_sub = world.static_qas[:40]
    base_st = eval_qa_list(model_a, tok, static_sub)["acc"]

    grid = {
        "full": [(1e-4, 20), (3e-4, 25), (5e-4, 30)],
        "mlp_patch": [(3e-4, 25), (1e-3, 30), (2e-3, 30)],
        "lora": [(5e-4, 25), (1e-3, 30), (2e-3, 35)],
        "replay": [(2e-4, 25), (5e-4, 30)],
    }
    best_cfg: Dict[str, Tuple[float, int]] = {}
    for method, cands in grid.items():
        best_score = -1e9
        best_pair = cands[0]
        for lr, steps in cands:
            ft = finetune_model_a(
                model_a, tok, dev_ep.facts, method=method, lr=lr, steps=steps,
                replay_qas=world.static_qas if method == "replay" else None,
            )
            cats = _eval_episode_categories(ft, tok, dev_ep)
            st_acc = eval_qa_list(ft, tok, static_sub)["acc"]
            drift_pen = max(0.0, base_st - st_acc)
            # Composite score balances fresh-fact accuracy and retention
            score = sum(cats.values()) / 4.0 - 0.5 * drift_pen
            if score > best_score:
                best_score = score
                best_pair = (lr, steps)
        best_cfg[method] = best_pair
    return best_cfg


def run_killtest(
    ckpt_a: str,
    ckpt_b: str,
    n_chains_list: Sequence[int] = (4, 8),
    n_episodes: int = 5,
    use_heldout_templates: bool = True,
    rag_top_k: int = 2,
    seed: int = 2026,
    out_json: Optional[str] = None,
) -> Dict:
    torch.set_num_threads(8)
    tok = SimpleWordTokenizer(target_vocab_size=1024)
    world = KnowledgeWorld(seed=42, n_static_chains=16)

    model_a, meta_a = load_checkpoint(ckpt_a)
    model_b, meta_b = load_checkpoint(ckpt_b)

    static_eval_qas = world.static_qas[:60]
    base_static_a = eval_qa_list(model_a, tok, static_eval_qas, mem_states=None)
    base_static_b = eval_qa_list(model_b, tok, static_eval_qas, mem_states=None)

    print(
        f"Loaded Model A ({model_a.count_parameters()/1e6:.2f}M, flops={meta_a['flops_done']:.2e}, "
        f"static_acc={base_static_a['acc']:.3f}) | "
        f"Model B ({model_b.count_parameters()/1e6:.2f}M, flops={meta_b['flops_done']:.2e}, "
        f"static_acc={base_static_b['acc']:.3f})",
        flush=True,
    )

    # Tune Model A write hyperparams on disjoint dev split (once)
    best_a_hparams = tune_model_a_on_dev(model_a, tok, world, n_chains=n_chains_list[0], seed=seed + 999)
    print(f"Dev-tuned Model A write hparams: {best_a_hparams}", flush=True)

    results: Dict = {
        "meta": {
            "ckpt_a": ckpt_a,
            "ckpt_b": ckpt_b,
            "params_a": model_a.count_parameters(),
            "params_b": model_b.count_parameters(),
            "flops_a": meta_a["flops_done"],
            "flops_b": meta_b["flops_done"],
            "wall_s_a": meta_a["wall_s"],
            "wall_s_b": meta_b["wall_s"],
            "base_static_a": base_static_a,
            "base_static_b": base_static_b,
            "dev_tuned_a_hparams": best_a_hparams,
            "use_heldout_templates": use_heldout_templates,
            "rag_top_k": rag_top_k,
            "n_episodes": n_episodes,
        },
        "by_scale": {},
    }

    for n_chains in n_chains_list:
        n_facts = 3 * n_chains
        rng = random.Random(seed + n_chains * 17)
        episodes = [
            world.sample_episode(
                split="test",
                n_chains=n_chains,
                rng=rng,
                use_heldout_templates=use_heldout_templates,
                shuffle_facts=True,
            )
            for _ in range(n_episodes)
        ]

        arm_names = [
            "A-ZeroShot", "B-ZeroShot",
            "A-Text-ICL", "A-Text-RAG",
            "B-Text-ICL", "B-Text-RAG",
            "A-Write-full", "A-Write-mlp", "A-Write-lora", "A-Write-replay",
            "B-Write",
        ]
        agg: Dict[str, Dict[str, List[float]]] = {
            name: {k: [] for k in ("recall", "paraphrase", "inverse", "two_hop", "drift_acc", "drift_nll")}
            for name in arm_names
        }

        for ep_i, ep in enumerate(episodes):
            retriever = BM25Retriever(ep.facts)
            icl_fn = lambda qa, f=ep.facts: f
            rag_fn = lambda qa, r=retriever: r.retrieve(qa.question, top_k=rag_top_k)

            # 0. Zero-shot baselines (verify test facts are genuinely fresh / unmemorized)
            for name, m in [("A-ZeroShot", model_a), ("B-ZeroShot", model_b)]:
                c = _eval_episode_categories(m, tok, ep, context_fn=None, mem_states=None)
                for k, v in c.items():
                    agg[name][k].append(v)
                agg[name]["drift_acc"].append(0.0)
                agg[name]["drift_nll"].append(0.0)

            # 1. Text baselines (zero drift by definition: no weights or memory modified)
            for name, m, cfn in [
                ("A-Text-ICL", model_a, icl_fn),
                ("A-Text-RAG", model_a, rag_fn),
                ("B-Text-ICL", model_b, icl_fn),
                ("B-Text-RAG", model_b, rag_fn),
            ]:
                c = _eval_episode_categories(m, tok, ep, context_fn=cfn, mem_states=None)
                for k, v in c.items():
                    agg[name][k].append(v)
                agg[name]["drift_acc"].append(0.0)
                agg[name]["drift_nll"].append(0.0)

            # 2. Model A write methods (no facts in context!)
            for name, method in [
                ("A-Write-full", "full"),
                ("A-Write-mlp", "mlp_patch"),
                ("A-Write-lora", "lora"),
                ("A-Write-replay", "replay"),
            ]:
                lr, steps = best_a_hparams[method]
                ft_a = finetune_model_a(
                    model_a, tok, ep.facts, method=method, lr=lr, steps=steps,
                    replay_qas=world.static_qas if method == "replay" else None,
                    seed=seed + ep_i,
                )
                c = _eval_episode_categories(ft_a, tok, ep, context_fn=None, mem_states=None)
                st_after = eval_qa_list(ft_a, tok, static_eval_qas, mem_states=None)
                for k, v in c.items():
                    agg[name][k].append(v)
                agg[name]["drift_acc"].append(st_after["acc"] - base_static_a["acc"])
                agg[name]["drift_nll"].append(st_after["nll"] - base_static_a["nll"])

            # 3. Model B learned write (single forward write into M; NO facts in context!)
            with torch.no_grad():
                f_ids, f_lens, f_valid = _encode_facts_single(tok, ep.facts)
                mem_b = model_b.write_facts(f_ids, f_lens, f_valid)
            c = _eval_episode_categories(model_b, tok, ep, context_fn=None, mem_states=mem_b)
            # Honest drift check: evaluate static knowledge WITH fresh fictional memory M ACTIVE!
            st_after_b = eval_qa_list(model_b, tok, static_eval_qas, mem_states=mem_b)
            for k, v in c.items():
                agg["B-Write"][k].append(v)
            agg["B-Write"]["drift_acc"].append(st_after_b["acc"] - base_static_b["acc"])
            agg["B-Write"]["drift_nll"].append(st_after_b["nll"] - base_static_b["nll"])

        summary: Dict[str, Dict[str, float]] = {}
        for name in arm_names:
            summary[name] = {
                k: round(sum(vs) / max(len(vs), 1), 4)
                for k, vs in agg[name].items()
            }
            summary[name]["mean_qa"] = round(
                (summary[name]["recall"] + summary[name]["paraphrase"] +
                 summary[name]["inverse"] + summary[name]["two_hop"]) / 4.0, 4
            )

        # Pick A's best write method by mean_qa
        a_write_arms = ["A-Write-full", "A-Write-mlp", "A-Write-lora", "A-Write-replay"]
        best_a_arm = max(a_write_arms, key=lambda n: summary[n]["mean_qa"])

        # Evaluate kill rule: "B must beat text where A loses"
        kill_vs_rag = {}
        kill_vs_icl = {}
        for metric in ("recall", "paraphrase", "inverse", "two_hop"):
            best_rag = max(summary["A-Text-RAG"][metric], summary["B-Text-RAG"][metric])
            best_icl = max(summary["A-Text-ICL"][metric], summary["B-Text-ICL"][metric])
            a_val = summary[best_a_arm][metric]
            b_val = summary["B-Write"][metric]
            kill_vs_rag[metric] = {
                "text_best": best_rag,
                "a_best_write": a_val,
                "b_write": b_val,
                "a_loses_to_text": a_val < best_rag,
                "b_beats_text": b_val > best_rag,
                "pass_where_a_loses": (a_val < best_rag) and (b_val > best_rag),
            }
            kill_vs_icl[metric] = {
                "text_best": best_icl,
                "a_best_write": a_val,
                "b_write": b_val,
                "a_loses_to_text": a_val < best_icl,
                "b_beats_text": b_val > best_icl,
                "pass_where_a_loses": (a_val < best_icl) and (b_val > best_icl),
            }

        results["by_scale"][f"{n_facts}_facts"] = {
            "n_chains": n_chains,
            "n_facts": n_facts,
            "best_a_write_arm": best_a_arm,
            "arms": summary,
            "kill_vs_rag": kill_vs_rag,
            "kill_vs_icl": kill_vs_icl,
        }

        print(f"\n=== Kill Test ({n_facts} fresh fictional facts, {n_episodes} episodes, heldout={use_heldout_templates}) ===")
        print(f"{'Arm':16s} | {'Recall':>6s} | {'Para':>6s} | {'Inv':>6s} | {'2-Hop':>6s} | {'Mean':>6s} | {'dAcc':>7s} | {'dNLL':>7s}")
        print("-" * 82)
        for name in arm_names:
            s = summary[name]
            print(
                f"{name:16s} | {s['recall']:6.3f} | {s['paraphrase']:6.3f} | "
                f"{s['inverse']:6.3f} | {s['two_hop']:6.3f} | {s['mean_qa']:6.3f} | "
                f"{s['drift_acc']:+7.3f} | {s['drift_nll']:+7.3f}"
            )

    if out_json:
        os.makedirs(os.path.dirname(out_json) or ".", exist_ok=True)
        with open(out_json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved kill-test results to {out_json}", flush=True)

    return results


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--ckpt_a", required=True)
    p.add_argument("--ckpt_b", required=True)
    p.add_argument("--chains", type=int, nargs="+", default=[4, 8])
    p.add_argument("--episodes", type=int, default=5)
    p.add_argument("--heldout", action="store_true", default=True)
    p.add_argument("--in_dist_templates", action="store_true", default=False)
    p.add_argument("--rag_top_k", type=int, default=2)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--out_json", type=str, default=None)
    args = p.parse_args()

    use_heldout = not args.in_dist_templates
    run_killtest(
        ckpt_a=args.ckpt_a,
        ckpt_b=args.ckpt_b,
        n_chains_list=args.chains,
        n_episodes=args.episodes,
        use_heldout_templates=use_heldout,
        rag_top_k=args.rag_top_k,
        seed=args.seed,
        out_json=args.out_json,
    )
