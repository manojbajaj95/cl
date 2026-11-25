"""CPU pilot of MEMIT key-space damage after unrelated language-model training."""

import argparse
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


LAYERS = tuple(range(13, 18))
MOM2_WEIGHT = 20_000
START = time.monotonic()


def log(message):
    print(f"[{time.monotonic() - START:7.1f}s] {message}", flush=True)


def rewrite_examples(tokenizer, data_path, n, seed):
    facts = json.loads(data_path.read_text())
    frequencies = Counter(
        (x["requested_rewrite"]["subject"], x["requested_rewrite"]["relation_id"])
        for x in facts
    )
    result = []
    for i in np.random.default_rng(seed).permutation(len(facts)):
        fact = facts[i]
        req = fact["requested_rewrite"]
        if frequencies[req["subject"], req["relation_id"]] != 1:
            continue
        new = tokenizer.encode(" " + req["target_new"]["str"])
        old = tokenizer.encode(" " + req["target_true"]["str"])
        lead, tail = req["prompt"].split("{}")
        prompt = lead + req["subject"] + tail
        encoding = tokenizer(prompt, return_offsets_mapping=True)
        lookup = max(
            j for j, (left, _) in enumerate(encoding.offset_mapping)
            if left < len(lead + req["subject"])
        )
        kl = tokenizer(req["subject"] + " is a", return_offsets_mapping=True)
        kl_lookup = max(
            j for j, (left, _) in enumerate(kl.offset_mapping) if left < len(req["subject"])
        )
        result.append({
            "id": fact["case_id"], "prompt": encoding.input_ids, "lookup": lookup,
            "new": new, "old": old, "kl": kl.input_ids, "kl_lookup": kl_lookup,
        })
        if len(result) == n:
            return sorted(result, key=lambda ex: len(ex["prompt"]) + len(ex["new"]))
    raise ValueError(f"Not enough eligible facts for n={n}")


def pad(rows):
    ids = torch.zeros((len(rows), max(map(len, rows))), dtype=torch.long)
    for i, row in enumerate(rows):
        ids[i, :len(row)] = torch.as_tensor(row)
    return ids


def batches(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


class PilotModel:
    def __init__(self, model_path):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, local_files_only=True, attn_implementation="sdpa",
        ).eval().requires_grad_(False)
        self.blocks = self.model.transformer.h

    def embed(self, ids):
        transformer = self.model.transformer
        return transformer.wte(ids) + transformer.wpe(torch.arange(ids.size(1)))

    def advance(self, x, start, stop):
        # All samples are right-padded and only real positions are read.
        for layer in range(start, stop):
            x = self.blocks[layer](x, use_cache=False)[0]
        return x

    def logits(self, x):
        return self.model.lm_head(self.model.transformer.ln_f(x))

    def weight(self, layer):
        return self.blocks[layer].mlp.c_proj.weight

    @torch.no_grad()
    def gather_at_subject(self, facts, layers, size):
        keys = {layer: [] for layer in layers}
        values = []
        for batch in batches(facts, size):
            rows = torch.arange(len(batch))
            positions = torch.tensor([ex["lookup"] for ex in batch])
            x = self.embed(pad([ex["prompt"][:ex["lookup"] + 1] for ex in batch]))
            for layer, block in enumerate(self.blocks[:LAYERS[-1] + 1]):
                if layer in keys:
                    def capture(_, args):
                        keys[layer].append(args[0][rows, positions].clone())

                    handle = block.mlp.c_proj.register_forward_pre_hook(capture)
                x = block(x, use_cache=False)[0]
                if layer in keys:
                    handle.remove()
            values.append(x[rows, positions])
        return {layer: torch.cat(parts) for layer, parts in keys.items()}, torch.cat(values)

    @torch.no_grad()
    def efficacy(self, facts, size):
        scores, successes = [], []
        for batch in batches(facts, size):
            inputs = [ex["prompt"] + ex[field][:-1] for field in ("new", "old") for ex in batch]
            x = self.advance(self.embed(pad(inputs)), 0, len(self.blocks))
            rows, cols, targets, examples, lengths = targets_at(batch, ("new", "old"))
            log_probs = self.logits(x[rows, cols]).log_softmax(-1)
            token_lp = log_probs[torch.arange(len(targets)), targets]
            fact_log_probs = torch.zeros(len(inputs)).scatter_add_(0, examples, token_lp) / lengths
            new, true = fact_log_probs.chunk(2)
            scores.append(new.exp())
            successes.append(new > true)
        return torch.cat(scores).numpy(), torch.cat(successes).numpy()


def targets_at(batch, fields):
    rows, cols, targets, lengths = [], [], [], []
    for field in fields:
        for ex in batch:
            start = len(ex["prompt"]) - 1
            count = len(ex[field])
            rows.extend([len(lengths)] * count)
            cols.extend(range(start, start + count))
            targets.extend(ex[field])
            lengths.append(count)
    return tuple(map(torch.tensor, (rows, cols, targets, rows, lengths)))


def optimize_z(model, batch, steps):
    last = LAYERS[-1] + 1
    n = len(batch)
    rows = torch.arange(2 * n)
    src = rows % n
    positions = torch.tensor([ex[k] for k in ("lookup", "kl_lookup") for ex in batch])
    inputs = [ex["prompt"] + ex["new"][:-1] for ex in batch] + [ex["kl"] for ex in batch]
    target_rows, cols, targets, examples, lengths = targets_at(batch, ("new",))
    with torch.no_grad():
        hidden = model.advance(model.embed(pad(inputs)), 0, last)
        start = hidden[rows[:n], positions[:n]]
        norms = start.norm(dim=1)
    delta = torch.zeros_like(start, requires_grad=True)
    optimizer = torch.optim.Adam([delta], lr=0.5)
    kl_init = None
    for _ in range(steps):
        optimizer.zero_grad()
        edited = hidden.clone()
        edited[rows, positions] = edited[rows, positions] + delta[src]
        end = model.advance(edited, last, len(model.blocks))
        selection = torch.cat((end[target_rows, cols], end[rows[n:], positions[n:]]))
        logp = model.logits(selection).log_softmax(-1)
        rewrite, kl = logp.split([len(targets), n])
        if kl_init is None:
            kl_init = kl.detach()
        losses = -rewrite[torch.arange(len(targets)), targets]
        nll = (torch.zeros(n).scatter_add_(0, examples, losses) / lengths).mean()
        penalty = 0.0625 * F.kl_div(kl_init, kl, log_target=True, reduction="batchmean")
        decay = 0.5 * (delta.norm(dim=1) / norms.square()).mean()
        (nll + penalty + decay).backward()
        optimizer.step()
        with torch.no_grad():
            delta.mul_((0.75 * norms / delta.norm(dim=1).clamp_min(1e-10)).clamp(max=1)[:, None])
    return start + delta.detach()


def memit_update(keys, residual, covariance, weight=MOM2_WEIGHT):
    keys = keys.double()
    adjusted = torch.linalg.solve(weight * covariance + keys.T @ keys, keys.T)
    # GPT-2 c_proj stores [input, output], i.e. transposed relative to ΔW.
    return (adjusted @ residual.double()).float()


@torch.no_grad()
def apply_memit(model, facts, targets, stats, batch_size):
    keys, values, writes = [], [], []
    for i, layer in enumerate(LAYERS):
        batch_keys, current = model.gather_at_subject(facts, [layer], batch_size)
        k = batch_keys[layer]
        v = (targets - current) / (len(LAYERS) - i)
        file = stats / f"transformer.h.{layer}.mlp.c_proj_float32_mom2_100000.npz"
        with np.load(file) as data:
            cov = torch.from_numpy(data["mom2.mom2"]).double() / int(data["mom2.count"])
        update = memit_update(k, v, cov)
        w = model.weight(layer)
        original = w.clone()
        w.add_(update)
        keys.append(k.numpy())
        values.append(v.numpy())
        writes.append((k @ (w - original)).numpy())
        log(f"MEMIT L{layer}: mean residual {v.norm(dim=1).mean():.4f}; update norm {update.norm():.4f}")
    return keys, values, writes


def train_stream(tokenizer, path, steps, seq_len, batch, seed):
    lines = [s.strip() for s in pq.read_table(path, columns=["text"])["text"].to_pylist()]
    lines = [s for s in lines if s and not s.startswith("=")]
    need = (steps + 2) * batch * (seq_len + 1)
    ids = []
    for idx in np.random.default_rng(seed).permutation(len(lines)):
        ids.extend(tokenizer.encode(lines[idx]))
        ids.append(tokenizer.eos_token_id)
        if len(ids) >= need:
            break
    return torch.tensor(ids[:need]).reshape(steps + 2, batch, seq_len + 1)


def tune(model, stream, lr):
    params = [model.weight(layer) for layer in LAYERS]
    for p in params:
        p.requires_grad_(True)
    optimizer = torch.optim.AdamW(params, lr=lr, weight_decay=0.0)

    def loss_for(ids):
        with torch.no_grad():
            x = model.advance(model.embed(ids[:, :-1]), 0, LAYERS[0])
        y = model.advance(x, LAYERS[0], len(model.blocks))
        return F.cross_entropy(model.logits(y).flatten(0, 1), ids[:, 1:].flatten())

    with torch.no_grad():
        before = float(torch.stack([loss_for(x) for x in stream[:2]]).mean())
    for step, ids in enumerate(stream[2:], 1):
        optimizer.zero_grad(set_to_none=True)
        loss = loss_for(ids)
        loss.backward()
        optimizer.step()
        if step == 1 or step % 10 == 0:
            log(f"train step {step}: NLL {loss.item():.4f}")
    with torch.no_grad():
        after = float(torch.stack([loss_for(x) for x in stream[:2]]).mean())
    for p in params:
        p.requires_grad_(False)
        p.grad = None
    return before, after


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--seed", type=int, default=301)
    p.add_argument("--train-seeds", type=int, nargs="+", default=[302])
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--batch", type=int, default=24)
    p.add_argument("--z-steps", type=int, default=8)
    p.add_argument("--train-steps", type=int, default=100)
    p.add_argument("--train-batch", type=int, default=2)
    p.add_argument("--seq-len", type=int, default=32)
    p.add_argument("--lr", type=float, default=2e-5)
    args = p.parse_args()
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    torch.manual_seed(args.seed)
    args.output.mkdir(parents=True, exist_ok=True)
    config = vars(args).copy()
    config["layers"] = LAYERS
    (args.output / "config.json").write_text(json.dumps(config, default=str, indent=2) + "\n")

    model_path = args.data / "gpt2-xl"
    tok = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    facts = rewrite_examples(tok, args.data / "counterfact.json", args.n, args.seed)
    model = PilotModel(model_path)
    log(f"Loaded GPT-2-XL; n={len(facts)}")
    targets = []
    for i, batch in enumerate(batches(facts, args.batch)):
        targets.append(optimize_z(model, batch, args.z_steps))
        log(f"z targets {min((i + 1) * args.batch, args.n)}/{args.n}")
    base_prob, base_win = model.efficacy(facts, args.batch)
    keys, values, edit_effects = apply_memit(model, facts, torch.cat(targets), args.data / "stats", args.batch)
    edit_prob, edit_win = model.efficacy(facts, args.batch)
    log(f"Rewrite preference: base {base_win.mean():.4f}; edited {edit_win.mean():.4f}")
    edited_weights = [model.weight(layer).detach().clone() for layer in LAYERS]
    for seed in args.train_seeds:
        with torch.no_grad():
            for layer, w in zip(LAYERS, edited_weights):
                model.weight(layer).copy_(w)
        stream = train_stream(
            tok, args.data / "wikitext-2-train.parquet", args.train_steps,
            args.seq_len, args.train_batch, seed,
        )
        nll_before, nll_after = tune(model, stream, args.lr)
        post_prob, post_win = model.efficacy(facts, args.batch)
        # Keep ΔW and K separately so the decoder can read stored Q directly.
        deltas = [(model.weight(layer) - w).cpu().numpy() for layer, w in zip(LAYERS, edited_weights)]
        np.savez(
            args.output / f"seed-{seed}.npz", ids=[ex["id"] for ex in facts], layers=LAYERS,
            keys=keys, values=values, dw=deltas, edit_effects=edit_effects,
            base_prob=base_prob, base_win=base_win, edit_prob=edit_prob, edit_win=edit_win,
            post_prob=post_prob, post_win=post_win, nll_before=nll_before, nll_after=nll_after,
        )
        log(f"seed {seed} saved: validation NLL {nll_before:.4f} -> {nll_after:.4f}; post preference {post_win.mean():.4f}")


if __name__ == "__main__":
    main()
