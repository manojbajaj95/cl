import pytest
import torch
from transformers import Qwen2Config, Qwen2ForCausalLM

from grammar import LABELS, Example, datasets, prompt, scratch_answer
from model import LORA_WIDTH, SLOTS, WIDTH, Reader
from summarize import paired, wilson


@pytest.mark.parametrize("seed", [3407, 9041])
def test_splits_are_balanced_valid_and_at_the_requested_depth(seed):
    demos, held = datasets(seed, 32)
    all_tapes = set()
    for depth, rows in [(4, demos), *held.items()]:
        assert sorted(row.answer for row in rows) == sorted(LABELS * (len(rows) // 4))
        for row in rows:
            assert row.tape not in all_tapes
            all_tapes.add(row.tape)
            assert len(row.tape) == depth * 4
            assert max(map(len, row.states())) == depth
            assert len(list(row.states())[-1]) > 0


def test_stack_and_scratchpad():
    row = Example(tuple("([{}]"))
    assert row.answer == "A"
    assert row.trace == "1:A 3:ABC 5:A"
    assert prompt(row, [row], scratch=True).endswith(f"{row.source} -> {row.trace} => A\n{row.source} ->")
    assert scratch_answer(" 1:A 3:ABC 5:A => A\nmore") == "A"
    assert scratch_answer(" A") == ""
    with pytest.raises(ValueError):
        list(Example(tuple("([)")).states())


def test_frozen_base_parity_loop_and_patch_gradients():
    torch.set_num_threads(1)
    torch.manual_seed(120)
    native = Qwen2ForCausalLM(Qwen2Config(
        vocab_size=32, hidden_size=12, intermediate_size=24, num_attention_heads=3,
        num_key_value_heads=1, num_hidden_layers=17, use_sliding_window=False, sliding_window=None,
    ))
    reader = Reader(native, None)
    ids = torch.tensor([[2, 3, 6], [3, 4, 7]])
    pos = (torch.arange(2), torch.tensor([2, 1]))
    h = reader.prefix(ids)
    plain = reader.logits(h, pos)
    torch.testing.assert_close(plain, native(ids, use_cache=False).logits[pos])
    loop_only = reader.logits(h, pos, loops=4)
    assert not torch.allclose(loop_only, plain)
    loop_only.square().sum().backward()
    assert reader.gate.grad.abs().sum() > 0
    reader.gate.requires_grad_(False)
    program = torch.randn(SLOTS, WIDTH).requires_grad_()
    one_pass_program = reader.logits(h, pos, program=program)
    assert not torch.allclose(one_pass_program, plain)
    with torch.no_grad():
        reader.gate.fill_(-50)
        torch.testing.assert_close(one_pass_program, reader.logits(h, pos, program=program))
        reader.gate.fill_(0)
    reader.logits(h, pos, loops=4, program=program).square().sum().backward()
    assert program.grad.abs().sum() > 0
    assert all(parameter.grad is None for parameter in native.parameters())


def test_storage_budget_and_score_helpers():
    assert (SLOTS * WIDTH) * 2 == (LORA_WIDTH * 2) * 2 == 4096
    lo, hi = wilson(0, 64)
    assert lo == pytest.approx(0)
    assert 0 < hi < .06
    assert paired([[1] * 4, [1] * 4]) == {"delta": 1, "ci95": [1, 1]}
