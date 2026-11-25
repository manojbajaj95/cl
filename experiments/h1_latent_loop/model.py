import math

import torch
from torch import nn
from torch.nn import functional as F
from transformers import StoppingCriteria


FIRST, STOP = 12, 16
SLOTS, WIDTH = 16, 128
LORA_WIDTH = SLOTS * WIDTH // 2


class Newline(StoppingCriteria):
    def __init__(self, tokenizer, start):
        self.tokenizer, self.start = tokenizer, start

    def __call__(self, ids, scores, **kwargs):
        strings = self.tokenizer.batch_decode(ids[:, self.start:], skip_special_tokens=True)
        return torch.tensor(["\n" in text for text in strings], device=ids.device)


class Reader:
    def __init__(self, model, tokenizer):
        self.model = model.requires_grad_(False).eval()
        self.trunk = model.model
        self.tokenizer = tokenizer
        hidden = model.config.hidden_size
        rng = torch.Generator().manual_seed(4997)
        self.basis = (2 * torch.randint(2, (WIDTH, hidden), generator=rng) - 1) / math.sqrt(WIDTH)
        self.gate = nn.Parameter(torch.full((hidden,), math.log(0.08 / 0.92)))

    def embed(self, ids):
        return self.trunk.embed_tokens(ids)

    def layers(self, h, start, end):
        positions = torch.arange(h.shape[1], device=h.device).unsqueeze(0)
        rope = self.trunk.rotary_emb(h, positions)
        for layer in self.trunk.layers[start:end]:
            h = layer(h, position_embeddings=rope)[0]
        return h

    @torch.no_grad()
    def prefix(self, ids):
        return self.layers(self.embed(ids), 0, FIRST)

    def logits(self, h, positions, loops=1, program=None, lora=None):
        if lora is not None:
            a, b = lora

            def add_low_rank(module, args, output):
                side = F.linear(F.linear(args[0][..., :LORA_WIDTH], a), b)
                return output + F.pad(side, (0, output.shape[-1] - LORA_WIDTH))

            hook = self.trunk.layers[FIRST].self_attn.o_proj.register_forward_hook(add_low_rank)
        offset = 0
        if program is not None:
            vectors = (program @ self.basis).to(h.dtype)
            offset = vectors.shape[0]
            h = torch.cat([vectors.unsqueeze(0).expand(h.shape[0], -1, -1), h], dim=1)
        try:
            h = self.layers(h, FIRST, STOP)
            for _ in range(loops - 1):
                h = torch.lerp(h, self.layers(h, FIRST, STOP), self.gate.sigmoid().to(h.dtype))
        finally:
            if lora is not None:
                hook.remove()
        h = self.layers(h[:, offset:], STOP, len(self.trunk.layers))
        return self.model.lm_head(self.trunk.norm(h[positions])).float()

    def encode(self, texts):
        rows = self.tokenizer(list(texts), add_special_tokens=False)["input_ids"]
        ids = nn.utils.rnn.pad_sequence(
            [torch.tensor(row) for row in rows], batch_first=True,
            padding_value=self.tokenizer.eos_token_id,
        )
        pos = torch.arange(len(rows)), torch.tensor([len(row) - 1 for row in rows])
        return ids, pos

    def supervised(self, pairs):
        prompts, answers = zip(*pairs)
        ids, pos = self.encode(prompts)
        targets = []
        for prompt, answer in zip(prompts, answers):
            before = self.tokenizer.encode(prompt, add_special_tokens=False)
            after = self.tokenizer.encode(prompt + answer, add_special_tokens=False)
            if after[:-1] != before:
                raise ValueError(f"Target must append exactly one token: {answer!r}")
            targets.append(after[-1])
        return self.prefix(ids), pos, torch.tensor(targets)

    @torch.inference_mode()
    def scratch(self, texts):
        self.tokenizer.padding_side = "left"
        try:
            batch = self.tokenizer(list(texts), padding=True, return_tensors="pt", add_special_tokens=False)
        finally:
            self.tokenizer.padding_side = "right"
        start = batch.input_ids.shape[1]
        emitted = self.model.generate(
            **batch, do_sample=False, use_cache=True, max_new_tokens=48,
            pad_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=[Newline(self.tokenizer, start)],
        )
        return self.tokenizer.batch_decode(emitted[:, start:], skip_special_tokens=True)
