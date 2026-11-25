"""Unit tests for writable-from-birth pretraining experiment."""

from __future__ import annotations

import random

import torch

from writable_pretrain.data import (
    BM25Retriever,
    KnowledgeWorld,
    SimpleWordTokenizer,
    format_qa_prompt,
)
from writable_pretrain.model import ModelConfig, TinyLM
from writable_pretrain.train import TrainConfig, train_model


def test_parameter_counts_matched():
    for scale, fn_a, fn_b, target_m in [
        ("20m", ModelConfig.standard_20m, ModelConfig.writable_20m, 20.0),
        ("pilot", ModelConfig.standard_pilot, ModelConfig.writable_pilot, 2.5),
    ]:
        ma = TinyLM(fn_a(1024))
        mb = TinyLM(fn_b(1024))
        pa = ma.count_parameters()
        pb = mb.count_parameters()
        rel_diff = abs(pa - pb) / max(pa, pb)
        assert rel_diff < 0.02, f"{scale}: param mismatch {pa} vs {pb} ({rel_diff:.4f})"
        if scale == "20m":
            assert 18_500_000 <= pa <= 21_500_000, f"Model A params {pa} not ~20M"
            assert 18_500_000 <= pb <= 21_500_000, f"Model B params {pb} not ~20M"


def test_entity_splits_strictly_disjoint():
    world = KnowledgeWorld(seed=42)
    s = world.splits
    for attr in ("persons", "orgs", "cities", "projs"):
        static_set = set(getattr(s, f"static_{attr}"))
        for split in ("train", "dev", "test"):
            ep_set = set(getattr(s, f"{split}_{attr}"))
            assert static_set.isdisjoint(ep_set), f"Overlap in {attr} between static and {split}"
            assert len(ep_set) >= 32, f"Too few episodic entities in {split}_{attr}"


def test_tokenizer_zero_unk_on_all_templates():
    tok = SimpleWordTokenizer(target_vocab_size=1024)
    world = KnowledgeWorld(seed=42)
    rng = random.Random(123)
    for heldout in (False, True):
        ep = world.sample_episode("test", n_chains=5, rng=rng, use_heldout_templates=heldout)
        for f in ep.facts:
            ids = tok.encode(f, add_bos=True, add_eos=True)
            assert tok.unk_id not in ids, f"UNK in fact: {f}"
        for qa in ep.qas:
            p_ids = tok.encode(format_qa_prompt(qa.question), add_bos=True)
            a_ids = tok.encode(qa.answer, add_eos=True)
            assert tok.unk_id not in p_ids, f"UNK in question: {qa.question}"
            assert tok.unk_id not in a_ids, f"UNK in answer: {qa.answer}"


def test_writable_memory_changes_output_without_mutating_base_weights():
    tok = SimpleWordTokenizer(target_vocab_size=1024)
    model = TinyLM(ModelConfig.writable_pilot(tok.vocab_size))
    model.eval()

    before_norm = sum(p.detach().pow(2).sum().item() for p in model.parameters())
    f_ids = torch.tensor([[[1, 10, 11, 20, 21, 2]]], dtype=torch.long)
    f_lens = torch.tensor([[6]], dtype=torch.long)
    f_valid = torch.tensor([[True]], dtype=torch.bool)
    mem = model.write_facts(f_ids, f_lens, f_valid)
    after_norm = sum(p.detach().pow(2).sum().item() for p in model.parameters())
    assert abs(before_norm - after_norm) < 1e-6

    q_ids = torch.tensor([[1, 30, 10, 11, 4]], dtype=torch.long)
    out_nomem = model(q_ids, mem_states=None)
    out_mem = model(q_ids, mem_states=mem)
    assert not torch.allclose(out_nomem, out_mem, atol=1e-5)


def test_bm25_retriever_basic():
    facts = [
        "mira keln works at vexor labs .",
        "vexor labs is located in tarnis bay .",
        "torin vash works at solis corp .",
    ]
    ret = BM25Retriever(facts)
    top = ret.retrieve("where does mira keln work ?", top_k=1)
    assert top == ["mira keln works at vexor labs ."]


def test_smoke_train_both_modes(tmp_path):
    for mode in ("standard", "writable"):
        res = train_model(TrainConfig(
            mode=mode,
            scale="pilot",
            max_flops=1.0e12,
            max_steps=3,
            batch_episodes=2,
            q_per_episode=4,
            static_per_step=2,
            log_every=2,
            out_dir=str(tmp_path / mode),
            num_threads=4,
        ))
        assert res["step"] >= 1
        assert res["flops_done"] > 0
