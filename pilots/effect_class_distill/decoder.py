import hashlib
from itertools import chain
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F


MODEL = "Qwen/Qwen2.5-Coder-0.5B"
REVISION = "8123ea2e9354afb7ffcc6c8641d1b2f5ecf18301"


def branches(sequences):
    children = {}
    for sequence in sequences:
        for i, token in enumerate(sequence):
            children.setdefault(tuple(sequence[:i]), set()).add(token)
    assert len({tuple(s) for s in sequences}) == len(sequences)
    assert not any(tuple(s) in children for s in sequences)
    return [(prefix, sorted(edges)) for prefix, edges in children.items() if len(edges) > 1]


def fingerprint(data):
    return hashlib.sha256(repr((REVISION, data, [list(p.candidates()) for p in data])).encode()).hexdigest()


@torch.inference_mode()
def build_cache(data, destination, model_path, batch_size=24):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    options = {"revision": REVISION} if model_path == MODEL else {"local_files_only": True}
    tokenizer = AutoTokenizer.from_pretrained(model_path, **options)
    model = AutoModelForCausalLM.from_pretrained(model_path, **options).eval()
    specs = []
    contexts = set()
    for prompt in data:
        initial = tuple(tokenizer.encode(prompt.text, add_special_tokens=False))
        leaves = [tokenizer.encode(code, add_special_tokens=False) for code in prompt.candidates()]
        assert [tokenizer.decode(initial + tuple(leaf)) for leaf in leaves] == [
            prompt.text + code for code in prompt.candidates()
        ]
        nodes = branches(leaves)
        specs.append((initial, leaves, nodes))
        contexts.update(initial + prefix for prefix, _ in nodes)

    # A deeper context supplies hidden states for all its ancestral branch points.
    sequences = []
    covered = set()
    for sequence in sorted(contexts, key=lambda s: (-len(s), s)):
        if sequence not in covered:
            sequences.append(sequence)
            covered.update(sequence[:i] for i in range(1, len(sequence) + 1))
    sequences.sort(key=len)
    wanted = {}
    print(f"cache: {len(sequences)} frozen forwards, {sum(map(len, sequences))} unpadded tokens", flush=True)
    for start in range(0, len(sequences), batch_size):
        batch = sequences[start : start + batch_size]
        length = max(map(len, batch))
        inputs = torch.tensor([list(s) + [0] * (length - len(s)) for s in batch])
        states = model.model(input_ids=inputs, use_cache=False).last_hidden_state
        for sequence, state in zip(batch, states):
            for i in range(1, len(sequence) + 1):
                prefix = sequence[:i]
                if prefix in contexts and prefix not in wanted:
                    wanted[prefix] = state[i - 1].clone()
        print(f"cache: {min(start + len(batch), len(sequences))}/{len(sequences)}", flush=True)

    vocabulary = sorted(set(chain.from_iterable(edges for _, _, nodes in specs for _, edges in nodes)))
    lookup = {token: i for i, token in enumerate(vocabulary)}
    num_nodes = max(len(nodes) for _, _, nodes in specs)
    num_edges = max(len(edges) for _, _, nodes in specs for _, edges in nodes)
    width = model.config.hidden_size
    states = torch.zeros(len(data), num_nodes, width)
    edges = torch.zeros(len(data), num_nodes, num_edges, dtype=torch.long)
    valid = torch.zeros_like(edges, dtype=torch.bool)
    valid[:, :, 0] = True
    paths = torch.full((len(data), len(specs[0][1]), num_nodes), -1, dtype=torch.long)
    for row, (initial, leaves, nodes) in enumerate(specs):
        for col, (prefix, tokens) in enumerate(nodes):
            states[row, col] = wanted[initial + prefix]
            edges[row, col, : len(tokens)] = torch.tensor([lookup[token] for token in tokens])
            valid[row, col, : len(tokens)] = True
            for code, leaf in enumerate(leaves):
                if tuple(leaf[: len(prefix)]) == prefix:
                    paths[row, code, col] = tokens.index(leaf[len(prefix)])
    weight = model.lm_head.weight[vocabulary].float()
    baseline = torch.einsum("pnh,pneh->pne", states, weight[edges])
    destination = Path(destination)
    partial = destination.with_suffix(".partial")
    torch.save(
        dict(fingerprint=fingerprint(data), states=states, edges=edges, valid=valid,
             paths=paths, baseline=baseline, vocabulary_size=len(vocabulary)),
        partial,
    )
    partial.replace(destination)


class Policy(nn.Module):
    def __init__(self, cache, rank=16):
        super().__init__()
        self.cache = cache
        self.down = nn.Linear(cache["states"].shape[-1], rank, bias=False)
        self.up = nn.Linear(rank, cache["vocabulary_size"], bias=False)
        nn.init.zeros_(self.up.weight)

    def forward(self, rows):
        c = self.cache
        correction = self.up(self.down(c["states"][rows]))
        logits = c["baseline"][rows] + correction.gather(-1, c["edges"][rows])
        edge_logprobs = F.log_softmax(logits.masked_fill(~c["valid"][rows], -torch.inf), dim=-1)
        return leaf_logprobs(edge_logprobs, c["paths"][rows])


def leaf_logprobs(edge_logprobs, paths):
    selected = edge_logprobs.gather(2, paths.clamp_min(0).transpose(1, 2)).transpose(1, 2)
    return selected.masked_fill(paths < 0, 0).sum(-1)
