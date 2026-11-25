"""Memory baselines and comparable payload accounting."""

import math
import re

import numpy as np
import torch
from torch.nn import functional as F


WIKITEXT_REPO = "Salesforce/wikitext"
WIKITEXT_REVISION = "b08601e04326c79dfdd32d625aee71d232d685c3"
WIKITEXT_FILE = "wikitext-2-raw-v1/test-00000-of-00001.parquet"


def name_matcher(names):
    return re.compile(r"(?<!\w)(?:" + "|".join(map(re.escape, names)) + r")(?!\w)")


def retrieve(q, facts, k=4):
    entities = {q.a, q.b}
    ranked = sorted(enumerate(facts),
                    key=lambda pair: -len(entities.intersection((pair[1].a, pair[1].b))))
    return [fact for _, fact in ranked[:k] if entities.intersection((fact.a, fact.b))]


def solved_notes(axis, q, values):
    return [f"{name} has {axis.unit} {values[name]:.6f}." for name in (q.a, q.b)]


def text_bytes(lines):
    return len("\n".join(lines).encode("utf-8"))


def family_accuracy(questions, predictions):
    return {family: {
        "correct": sum(int(pred == q.yes) for q, pred in zip(questions, predictions) if q.family == family),
        "n": sum(q.family == family for q in questions),
    } for family in sorted({q.family for q in questions})}


def prepare_drift(net, matcher, path, rows):
    if path is None:
        from huggingface_hub import hf_hub_download

        path = hf_hub_download(WIKITEXT_REPO, WIKITEXT_FILE, revision=WIKITEXT_REVISION, repo_type="dataset")
    import pyarrow.parquet as pq

    articles = pq.read_table(path, columns=["text"], partitioning=None)["text"].to_pylist()
    full = net.tokenizer.encode("\n".join(articles[:100]), add_special_tokens=False)
    rendered = []
    for i in range(rows):
        text = net.tokenizer.decode(full[128 * i:128 * (i + 1)], clean_up_tokenization_spaces=False)
        if not text:
            break
        rendered.append((text, [(m.start(), m.end(), m.group()) for m in matcher.finditer(text)]))
    return net.encode(rendered)


@torch.inference_mode()
def perplexity(net, encoded, layer=None, vectors=None):
    total_loss, n = 0.0, 0
    for ids, names in encoded:
        ops = [(0, pos, vectors[name]) for name, pos in names if vectors and name in vectors]
        with net.write(layer, ops):
            tokens = torch.tensor([ids])
            hidden = net.decoder(input_ids=tokens, use_cache=False).last_hidden_state[0, :-1]
        seq = tokens[0, 1:]
        for states, labels in zip(hidden.split(32), seq.split(32)):
            total_loss += F.cross_entropy(net.model.lm_head(states), labels, reduction="sum").item()
            n += len(labels)
    return {"perplexity": math.exp(total_loss / n), "tokens": n}


def train_lora(net, facts, budget, epochs, seed):
    """Train only q_proj LoRA matrices, allocating identical FP16 payload bytes."""
    from peft import LoraConfig, get_peft_model

    hidden_size = net.model.config.hidden_size
    ranks, leftover = divmod(budget, 2 * 2 * hidden_size)
    if leftover or not ranks:
        raise ValueError(f"Cannot exactly match map budget {budget} with q_proj rank increments")
    count = min(8, ranks, len(net.layers))
    layers = np.linspace(0, len(net.layers) - 1, count, dtype=int)
    rank_pattern = {f"model.layers.{layer}.self_attn.q_proj": ranks // count + (i < ranks % count)
                    for i, layer in enumerate(layers)}
    base = net.model
    tuned = get_peft_model(base, LoraConfig(r=1, lora_alpha=1, target_modules=list(rank_pattern),
                                          rank_pattern=rank_pattern, use_rslora=True))
    params = [p for p in tuned.parameters() if p.requires_grad]
    actual = sum(p.numel() * 2 for p in params)
    if actual != budget:
        raise ValueError(f"LoRA actually allocated {actual}, expected {budget}")
    optimizer = torch.optim.AdamW(params, lr=0.002, weight_decay=0)
    examples = [net.tokenizer.encode(text + "\n", add_special_tokens=False) for text in facts]
    rng = np.random.default_rng(seed)
    losses = []
    tuned.train()
    for epoch in range(epochs):
        epoch_loss = []
        shuffled = rng.permutation(len(examples))
        for start in range(0, len(examples), 8):
            ids, mask = net.pad([examples[i] for i in shuffled[start:start + 8]])
            labels = ids.masked_fill(mask == 0, -100)
            hidden = net.decoder(input_ids=ids, attention_mask=mask, use_cache=False).last_hidden_state
            loss = F.cross_entropy(net.model.lm_head(hidden[:, :-1][mask[:, 1:] != 0]),
                                   labels[:, 1:][mask[:, 1:] != 0])
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            epoch_loss.append(loss.item())
        losses.append(float(np.mean(epoch_loss)))
        print(f"lora epoch {epoch + 1}/{epochs}: loss={losses[-1]:.4f}", flush=True)
    with torch.no_grad():
        for param in params:
            param.copy_(param.to(torch.float16))
    tuned.eval()
    return tuned, {"payload_bytes": actual, "rank_by_layer": rank_pattern, "epoch_losses": losses}
