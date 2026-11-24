import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


VERSIONS = 5
RANK = 5
PROBES = 64
STEPS = 48
BATCH = 16
REPLAY = 16
MODEL = "Qwen/Qwen2.5-0.5B"
REVISION = "060db6499f32faf8b98477b0a26969ef7d8b9987"


def make_tasks():
    rng = np.random.default_rng(183)
    prompts, labels, train, test, probes = [], [], [], [], []
    for task, domain in enumerate(("north", "south", "east", "west", "central")):
        start = len(prompts)
        probe_count = PROBES // VERSIONS + (task < PROBES % VERSIONS)
        for i, nonce in enumerate(rng.choice(900, 48 + 32 + probe_count, replace=False) + 100):
            bit = i % 2
            cue = ("up", "down")[bit]
            prompts.append(f"\n{domain} {nonce} {cue}:")
            labels.append(bit ^ (task % 2))
        train.append(torch.arange(start, start + 48))
        test.append(torch.arange(start + 48, start + 80))
        probes.extend(range(start + 80, len(prompts)))
    assert len(set(prompts)) == len(prompts)
    assert len(probes) == PROBES
    return prompts, torch.tensor(labels), train, test, torch.tensor(probes)


@torch.inference_mode()
def encode_features(model, tokenizer, prompts, tags):
    encoded = [tokenizer.encode(prompt, add_special_tokens=False) for prompt in prompts]
    width = max(map(len, encoded)) + len(tags[0])
    features, frozen_logits = [], []
    for tag in tags:
        hidden_batches, logits_batches = [], []
        for start in range(0, len(encoded), 48):
            inputs = [tag + row for row in encoded[start:start + 48]]
            mask = torch.tensor([[0] * (width - len(row)) + [1] * len(row) for row in inputs])
            ids = torch.tensor([[tokenizer.pad_token_id] * (width - len(row)) + row for row in inputs])
            hidden = model.model(input_ids=ids, attention_mask=mask, use_cache=False,
                                 position_ids=(mask.cumsum(dim=1) - 1).clamp_min(0))
            hidden = hidden.last_hidden_state[:, -1].contiguous()
            hidden_batches.append(hidden)
            logits_batches.append(model.lm_head(hidden))
        features.append(torch.cat(hidden_batches))
        frozen_logits.append(torch.cat(logits_batches))
    return torch.stack(features), torch.stack(frozen_logits)


class Delta(torch.nn.Module):
    def __init__(self, width, vocab, generator):
        super().__init__()
        self.a = torch.nn.Parameter(torch.randn(width, RANK, generator=generator) / math.sqrt(width))
        self.b = torch.nn.Parameter(torch.zeros(RANK, vocab))

    def forward(self, hidden, logits):
        return logits + (hidden @ self.a) @ self.b

    def snapshot(self):
        return self.a.detach().clone(), self.b.detach().clone()


def rank_one(adapter):
    a, b = adapter
    qa, ra = torch.linalg.qr(a)
    qb, rb = torch.linalg.qr(b.T)
    u, s, vh = torch.linalg.svd(ra @ rb.T, full_matrices=False)
    return qa @ u[:, :1], (s[:1, None] * vh[:1]) @ qb.T


def kl(log_p, log_q):
    return (log_p.exp() * (log_p - log_q)).sum(dim=-1)


class Pilot:
    def __init__(self, hidden, logits, labels, train, test, probes, label_ids, wiki):
        self.hidden, self.logits, self.labels = hidden, logits, labels
        self.train, self.test, self.probes = train, test, probes
        self.panel = torch.cat(test)
        self.label_ids, self.wiki = label_ids, wiki

    def predictions(self, adapter, tag, rows):
        a, b = adapter
        return self.logits[tag, rows] + (self.hidden[tag, rows] @ a) @ b

    def train_arm(self, arm, seed, teachers=None):
        generator = torch.Generator().manual_seed(seed)
        routing = torch.Generator().manual_seed(seed + 10000)
        modules = Delta(self.hidden.shape[-1], self.logits.shape[-1], generator)
        optimizer = torch.optim.AdamW(modules.parameters(), lr=0.001, weight_decay=0)
        snapshots = []
        teachers = [] if teachers is None else teachers
        for version, rows in enumerate(self.train, 1):
            if version > 1:
                sample = torch.randperm((version - 1) * PROBES, generator=generator)
                sample = sample.repeat(math.ceil(STEPS * REPLAY / len(sample)))
            batches = torch.cat([rows[torch.randperm(len(rows), generator=generator)]
                                 for _ in range(STEPS * BATCH // len(rows) + 1)])
            for step in range(STEPS):
                current = batches[step * BATCH:(step + 1) * BATCH]
                batch = current
                version_ids = torch.full_like(current, version)
                if version > 1:
                    sampled = sample[step * REPLAY:(step + 1) * REPLAY]
                    past_ids = sampled // PROBES
                    probe_ids = sampled % PROBES
                    batch = torch.cat((batch, self.probes[probe_ids]))
                    version_ids = torch.cat((version_ids, past_ids + 1))
                    # Cache log probabilities so every arm sees the same checkpoint outputs.
                    target = torch.stack([teachers[j][i] for j, i in zip(past_ids, probe_ids)])
                if arm == "replay":
                    version_ids = torch.zeros_like(version_ids)
                elif arm == "shuffled":
                    version_ids = torch.randint(1, VERSIONS + 1, version_ids.shape, generator=routing)
                pred = modules(self.hidden[version_ids, batch], self.logits[version_ids, batch])
                loss = F.cross_entropy(pred[:BATCH], self.label_ids[self.labels[current]])
                if version > 1:
                    loss = loss + kl(target, F.log_softmax(pred[BATCH:], dim=-1)).mean()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            snapshots.append(modules.snapshot())
            if arm == "tagged" and version < VERSIONS:
                teachers.append(self.predictions(snapshots[-1], version, self.probes).log_softmax(dim=-1))
        return snapshots, teachers

    def scores(self, snapshots, replay, shuffled, seed):
        result = {"seed": seed, "versions": [], "retention": {}}
        arms = ("tagged", "replay", "shuffled", "stored", "wrong_tag", "frozen")
        for offset, teacher in enumerate(snapshots):
            version = offset + 1
            stored = rank_one(teacher)
            assert VERSIONS * sum(x.numel() for x in stored) == sum(x.numel() for x in teacher)
            zero = (teacher[0], torch.zeros_like(teacher[1]))
            readers = ((snapshots[-1], version), (replay[-1], 0), (shuffled[-1], version),
                       (stored, version), (snapshots[-1], VERSIONS), (zero, version))
            reference = self.predictions(teacher, version, self.panel).log_softmax(dim=-1)
            probe_reference = self.predictions(teacher, version, self.probes).log_softmax(dim=-1)
            row = {arm: {} for arm in arms}
            task_slice = slice(offset * len(self.test[0]), version * len(self.test[0]))
            labels = self.labels[self.test[offset]]
            true_accuracy = (reference[task_slice][:, self.label_ids].argmax(dim=-1) == labels)
            for arm, (adapter, tag) in zip(arms, readers):
                pred = self.predictions(adapter, tag, self.panel).log_softmax(dim=-1)
                probe_pred = self.predictions(adapter, tag, self.probes).log_softmax(dim=-1)
                row[arm] = {
                    "heldout_kl": kl(pred, reference).mean().item(),
                    "heldout_reverse_kl": kl(reference, pred).mean().item(),
                    "probe_kl": kl(probe_pred, probe_reference).mean().item(),
                    "accuracy": (pred[task_slice][:, self.label_ids].argmax(dim=-1) == labels).float().mean().item(),
                }
            row["checkpoint_accuracy"] = true_accuracy.float().mean().item()
            result["versions"].append(row)
        for arm, delta, tag in (("tagged", snapshots[-1], VERSIONS), ("replay", replay[-1], 0)):
            accuracy = []
            for rows in self.test:
                pred = self.predictions(delta, tag, rows)[:, self.label_ids].argmax(dim=-1)
                accuracy.append((pred == self.labels[rows]).float().mean().item())
            h, logits, label = self.wiki[tag]
            logits = logits + (h @ delta[0]) @ delta[1]
            result["retention"][arm] = {"accuracy": accuracy, "ppl": F.cross_entropy(logits, label).exp().item()}
        result["frozen_ppl"] = {
            str(tag): F.cross_entropy(logits, label).exp().item()
            for tag, (_, logits, label) in self.wiki.items()
        }
        return result


@torch.inference_mode()
def wiki_features(model, tokenizer, tags, path):
    text = "\n".join(pq.read_table(path, columns=["text"])["text"].to_pylist())
    tokens = tokenizer.encode(text, add_special_tokens=False)[:513]
    assert len(tokens) == 513
    labels = torch.tensor(tokens)[1:]
    spans = [tokens[i:i + 64] for i in range(0, 512, 64)]
    wiki = {}
    for index in (0, VERSIONS):
        tag = tags[index]
        hidden = model.model(input_ids=torch.tensor([tag + span for span in spans]),
                             use_cache=False).last_hidden_state[:, len(tag):].flatten(0, 1).contiguous()
        wiki[index] = (hidden, model.lm_head(hidden), labels)
    return wiki


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--wiki", required=True, type=Path)
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 29, 43])
    parser.add_argument("--threads", type=int, default=6)
    args = parser.parse_args()
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    kwargs = {"revision": REVISION} if args.model == MODEL else {}
    tokenizer = AutoTokenizer.from_pretrained(args.model, **kwargs)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float32, **kwargs).eval()
    tags = [tokenizer.encode(f"<v_{i}>", add_special_tokens=False) for i in range(VERSIONS + 1)]
    assert len({len(tag) for tag in tags}) == 1 and len({tuple(tag) for tag in tags}) == VERSIONS + 1
    labels = [tokenizer.encode(choice, add_special_tokens=False) for choice in (" A", " B")]
    assert all(len(label) == 1 for label in labels)
    prompts, targets, train, test, probes = make_tasks()
    start = time.monotonic()
    hidden, logits = encode_features(model, tokenizer, prompts, tags)
    wiki = wiki_features(model, tokenizer, tags, args.wiki)
    del model
    print(json.dumps({"feature_seconds": time.monotonic() - start,
                      "delta_bytes": 4 * RANK * (hidden.shape[-1] + logits.shape[-1]),
                      "tag_tokens": len(tags[0])}), flush=True)
    # Inference tensors cannot be saved for autograd even when frozen.
    pilot = Pilot(hidden.clone(), logits, targets, train, test, probes, torch.tensor(labels).flatten(), wiki)
    for seed in args.seeds:
        start = time.monotonic()
        tagged, teachers = pilot.train_arm("tagged", seed)
        replay, _ = pilot.train_arm("replay", seed, teachers)
        shuffled, _ = pilot.train_arm("shuffled", seed, teachers)
        with torch.no_grad():
            result = pilot.scores(tagged, replay, shuffled, seed)
        result["seconds"] = time.monotonic() - start
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
