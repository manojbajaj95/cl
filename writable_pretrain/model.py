"""StandardLM (Model A) and WritableLM (Model B) with matched ~20M parameter configs.

Model A: standard pre-norm causal Transformer (RoPE + RMSNorm + SwiGLU + tied embeddings).
Model B: identical backbone with designated Writable Key-Value Memory Blocks at
layers (0, 2, 4) of a 6-layer model. During a write pass, each fact is encoded
independently (never concatenated across facts) and written into fixed-capacity
memory slots (K, V, G, mask) via learned projections. At question time, facts are
never shown in context; Model B reads from its written memory blocks (with a
learnable null/no-op slot so unmatched queries such as static facts return ~0).
Model B's FFN width is trimmed slightly so Model A and Model B have matched total
parameter counts (<1% diff).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

MemoryState = Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]


@dataclass
class ModelConfig:
    vocab_size: int = 1024
    d_model: int = 512
    n_layers: int = 6
    n_heads: int = 8
    d_ff: int = 1408
    max_seq_len: int = 512
    dropout: float = 0.0
    # Model B only:
    is_writable: bool = False
    mem_layers: Tuple[int, ...] = (0, 2, 4)
    n_mem_heads: int = 8
    mem_head_dim: int = 64
    mem_max_slots: int = 256

    @classmethod
    def standard_20m(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=512,
            n_layers=6,
            n_heads=8,
            d_ff=1408,
            max_seq_len=512,
            is_writable=False,
        )

    @classmethod
    def writable_20m(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=512,
            n_layers=6,
            n_heads=8,
            d_ff=1152,
            max_seq_len=512,
            is_writable=True,
            mem_layers=(0, 2, 4),
            n_mem_heads=8,
            mem_head_dim=64,
            mem_max_slots=256,
        )

    @classmethod
    def standard_small(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=128,
            n_layers=4,
            n_heads=4,
            d_ff=416,
            max_seq_len=512,
            is_writable=False,
        )

    @classmethod
    def writable_small(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=128,
            n_layers=4,
            n_heads=4,
            d_ff=304,
            max_seq_len=512,
            is_writable=True,
            mem_layers=(0, 1, 2),
            n_mem_heads=4,
            mem_head_dim=32,
            mem_max_slots=256,
        )

    @classmethod
    def standard_pilot(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=192,
            n_layers=6,
            n_heads=6,
            d_ff=512,
            max_seq_len=512,
            is_writable=False,
        )

    @classmethod
    def writable_pilot(cls, vocab_size: int = 1024) -> "ModelConfig":
        return cls(
            vocab_size=vocab_size,
            d_model=192,
            n_layers=6,
            n_heads=6,
            d_ff=416,
            max_seq_len=512,
            is_writable=True,
            mem_layers=(0, 2, 4),
            n_mem_heads=6,
            mem_head_dim=32,
            mem_max_slots=256,
        )


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        norm = torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return x * norm * self.weight


def _precompute_rope(head_dim: int, max_seq_len: int, base: float = 10000.0) -> Tuple[torch.Tensor, torch.Tensor]:
    inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim))
    t = torch.arange(max_seq_len, dtype=torch.float32)
    freqs = torch.outer(t, inv_freq)  # (T, head_dim/2)
    cos = torch.cos(freqs)[None, None, :, :]  # (1, 1, T, head_dim/2)
    sin = torch.sin(freqs)[None, None, :, :]
    return cos, sin


def _apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    # x: (B, H, T, D)
    T = x.size(2)
    c = cos[:, :, :T, :]
    s = sin[:, :, :T, :]
    x1 = x[..., ::2]
    x2 = x[..., 1::2]
    out1 = x1 * c - x2 * s
    out2 = x1 * s + x2 * c
    return torch.stack((out1, out2), dim=-1).flatten(-2)


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = nn.Linear(d_model, d_model, bias=False)
        self.dropout = dropout

    def forward(
        self,
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
        attn_mask: Optional[torch.Tensor] = None,
        is_causal: bool = True,
    ) -> torch.Tensor:
        B, T, C = x.shape
        qkv = self.qkv(x).view(B, T, 3, self.n_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)
        q = _apply_rope(q.transpose(1, 2), cos, sin)
        k = _apply_rope(k.transpose(1, 2), cos, sin)
        v = v.transpose(1, 2)
        y = F.scaled_dot_product_attention(
            q, k, v,
            attn_mask=attn_mask,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=is_causal if attn_mask is None else False,
        )
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.out(y)


class SwiGLU(nn.Module):
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_up = nn.Linear(d_model, d_ff, bias=False)
        self.w_down = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))


class WritableKVMemoryBlock(nn.Module):
    """Fixed-capacity designated writable memory block (K, V, G, mask).

    Keys are projected from pre-attention representations (matching read-time query
    representations via shared L2-normalized key/query space `w_kq`), while values
    and write gates are projected from post-attention contextualized fact tokens.
    A learnable `null_logit` provides a zero-value no-op slot so unmatched queries
    (e.g., static background knowledge) receive ~0 perturbation -> minimal drift.
    """

    def __init__(self, d_model: int, n_heads: int = 8, head_dim: int = 64, max_slots: int = 256):
        super().__init__()
        self.n_heads = n_heads
        self.head_dim = head_dim
        self.max_slots = max_slots
        self.mem_dim = n_heads * head_dim

        self.key_norm = RMSNorm(d_model)
        self.val_norm = RMSNorm(d_model)
        self.read_norm = RMSNorm(d_model)
        self.w_kq = nn.Linear(d_model, self.mem_dim, bias=False)
        self.w_wv = nn.Linear(d_model, self.mem_dim, bias=False)
        self.w_wg = nn.Linear(d_model, n_heads, bias=True)
        self.w_ro = nn.Linear(self.mem_dim, d_model, bias=False)

        self.log_scale = nn.Parameter(torch.full((1, n_heads, 1, 1), math.log(12.0)))
        self.null_logit = nn.Parameter(torch.full((1, n_heads, 1, 1), 6.0))
        nn.init.constant_(self.w_wg.bias, 0.0)
        nn.init.normal_(self.w_ro.weight, mean=0.0, std=0.02 / math.sqrt(2))

    def write(
        self,
        h_key: torch.Tensor,
        h_val: torch.Tensor,
        tok_valid: torch.Tensor,
        state: Optional[MemoryState] = None,
    ) -> MemoryState:
        """Write fact token representations into the fixed-capacity memory block.

        Args:
            h_key: (B, S, d_model) pre-attention token states.
            h_val: (B, S, d_model) post-attention contextualized token states.
            tok_valid: (B, S) bool mask for non-padding fact tokens.
            state: optional existing (K, V, G, mask) tuple.
        """
        B, S, _ = h_key.shape
        K = self.w_kq(self.key_norm(h_key)).view(B, S, self.n_heads, self.head_dim).transpose(1, 2)
        K = F.normalize(K, p=2, dim=-1, eps=1e-6)
        v_in = self.val_norm(h_val)
        V = self.w_wv(v_in).view(B, S, self.n_heads, self.head_dim).transpose(1, 2)
        G = F.logsigmoid(self.w_wg(v_in)).transpose(1, 2)  # (B, H, S) in (-inf, 0]
        mask = tok_valid
        if state is not None:
            K_old, V_old, G_old, m_old = state
            K = torch.cat([K_old, K], dim=2)[:, :, -self.max_slots:, :]
            V = torch.cat([V_old, V], dim=2)[:, :, -self.max_slots:, :]
            G = torch.cat([G_old, G], dim=2)[:, :, -self.max_slots:]
            mask = torch.cat([m_old, mask], dim=1)[:, -self.max_slots:]
        return (K, V, G, mask)

    def read(self, x: torch.Tensor, state: MemoryState) -> torch.Tensor:
        """Read from the writable memory block at every token position."""
        B, T, _ = x.shape
        K, V, G, mask = state
        Q = self.w_kq(self.read_norm(x)).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        Q = F.normalize(Q, p=2, dim=-1, eps=1e-6)
        scale = self.log_scale.exp().clamp(max=30.0)
        scores = torch.matmul(Q, K.transpose(-2, -1)) * scale + G.unsqueeze(2)
        scores = scores.masked_fill(~mask[:, None, None, :], -1e9)
        null_s = self.null_logit.expand(B, self.n_heads, T, 1)
        attn = F.softmax(torch.cat([scores, null_s], dim=-1), dim=-1)[..., :-1]
        out = torch.matmul(attn, V).transpose(1, 2).contiguous().view(B, T, self.mem_dim)
        return self.w_ro(out)


class TransformerBlock(nn.Module):
    def __init__(self, cfg: ModelConfig, has_memory: bool = False):
        super().__init__()
        self.norm1 = RMSNorm(cfg.d_model)
        self.attn = CausalSelfAttention(cfg.d_model, cfg.n_heads, cfg.dropout)
        self.norm2 = RMSNorm(cfg.d_model)
        self.ffn = SwiGLU(cfg.d_model, cfg.d_ff)
        self.memory: Optional[WritableKVMemoryBlock] = (
            WritableKVMemoryBlock(cfg.d_model, cfg.n_mem_heads, cfg.mem_head_dim, cfg.mem_max_slots)
            if has_memory else None
        )

    def forward(
        self,
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
        mem_state: Optional[MemoryState] = None,
    ) -> torch.Tensor:
        if self.memory is not None and mem_state is not None:
            x = x + self.memory.read(x, mem_state)
        x = x + self.attn(self.norm1(x), cos, sin, is_causal=True)
        x = x + self.ffn(self.norm2(x))
        return x


def index_mem_states(
    mem_states: Sequence[MemoryState],
    indices: torch.Tensor,
) -> List[MemoryState]:
    """Broadcast / gather a list of MemoryState tuples along batch dim 0."""
    return [(K[indices], V[indices], G[indices], m[indices]) for (K, V, G, m) in mem_states]


def detach_mem_states(mem_states: Sequence[MemoryState]) -> List[MemoryState]:
    return [(K.detach(), V.detach(), G.detach(), m.detach()) for (K, V, G, m) in mem_states]


class TinyLM(nn.Module):
    """Unified LM class for both Model A (standard) and Model B (writable-from-birth)."""

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        mem_set = set(cfg.mem_layers) if cfg.is_writable else set()
        self.blocks = nn.ModuleList([
            TransformerBlock(cfg, has_memory=(i in mem_set))
            for i in range(cfg.n_layers)
        ])
        self.final_norm = RMSNorm(cfg.d_model)
        cos, sin = _precompute_rope(cfg.d_model // cfg.n_heads, cfg.max_seq_len)
        self.register_buffer("rope_cos", cos, persistent=False)
        self.register_buffer("rope_sin", sin, persistent=False)
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(m: nn.Module) -> None:
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def write_facts(
        self,
        fact_ids: torch.Tensor,
        fact_lens: torch.Tensor,
        fact_valid: torch.Tensor,
        prev_states: Optional[Sequence[MemoryState]] = None,
    ) -> List[MemoryState]:
        """Run Model B's learned write pass on independent fact sentences.

        Each fact is encoded independently (bidirectional attention within the
        single fact, never across facts) and written into the designated memory
        blocks. Base model weights are never mutated.
        """
        assert self.cfg.is_writable, "write_facts is only valid for WritableLM (Model B)"
        B, M_facts, T_f = fact_ids.shape
        x = self.tok_emb(fact_ids.view(B * M_facts, T_f))
        t_pos = torch.arange(T_f, device=fact_ids.device)[None, None, :]
        tok_valid = (t_pos < fact_lens.unsqueeze(-1)) & fact_valid.unsqueeze(-1)
        pad_m = (t_pos < fact_lens.unsqueeze(-1)).view(B * M_facts, 1, 1, T_f)
        attn_mask = torch.zeros(B * M_facts, 1, T_f, T_f, device=fact_ids.device, dtype=x.dtype)
        attn_mask = attn_mask.masked_fill(~pad_m, -1e9)

        states: List[MemoryState] = []
        mem_idx = 0
        for block in self.blocks:
            x_in = x
            x = x + block.attn(block.norm1(x), self.rope_cos, self.rope_sin, attn_mask=attn_mask, is_causal=False)
            if block.memory is not None:
                h_key = x_in.view(B, M_facts * T_f, self.cfg.d_model)
                h_val = x.view(B, M_facts * T_f, self.cfg.d_model)
                v_flat = tok_valid.view(B, M_facts * T_f)
                prev = prev_states[mem_idx] if prev_states is not None else None
                states.append(block.memory.write(h_key, h_val, v_flat, state=prev))
                mem_idx += 1
            x = x + block.ffn(block.norm2(x))
            if mem_idx == len(self.cfg.mem_layers):
                break
        return states

    def forward(
        self,
        input_ids: torch.Tensor,
        mem_states: Optional[Sequence[MemoryState]] = None,
    ) -> torch.Tensor:
        x = self.tok_emb(input_ids)
        mem_idx = 0
        for block in self.blocks:
            st = None
            if block.memory is not None and mem_states is not None:
                st = mem_states[mem_idx]
                mem_idx += 1
            x = block(x, self.rope_cos, self.rope_sin, mem_state=st)
        x = self.final_norm(x)
        return F.linear(x, self.tok_emb.weight)

    @torch.no_grad()
    def generate_answer(
        self,
        prompt_ids: torch.Tensor,
        max_new_tokens: int = 4,
        eos_id: int = 2,
        mem_states: Optional[Sequence[MemoryState]] = None,
    ) -> torch.Tensor:
        """Greedy decode up to max_new_tokens after prompt_ids (B, T)."""
        ids = prompt_ids
        finished = torch.zeros(ids.size(0), dtype=torch.bool, device=ids.device)
        generated: List[torch.Tensor] = []
        for _ in range(max_new_tokens):
            logits = self.forward(ids, mem_states=mem_states)
            next_tok = logits[:, -1, :].argmax(dim=-1)
            next_tok = torch.where(finished, torch.full_like(next_tok, eos_id), next_tok)
            generated.append(next_tok)
            finished = finished | (next_tok == eos_id)
            ids = torch.cat([ids, next_tok.unsqueeze(-1)], dim=-1)
            if finished.all():
                break
        return torch.stack(generated, dim=-1)
