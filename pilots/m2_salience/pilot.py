import argparse
from collections import OrderedDict, defaultdict
import itertools
import json
import os
from pathlib import Path
import time

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache


MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
STATIONS = ("Fox", "Oak", "Elm", "Bay", "Pine", "Hill", "Lake", "Rose", "Rock", "Vale")
QUESTIONS = ("Which valve should station {} use?", "At station {}, which valve is correct?")
ACTIONS = "ABC"
N = len(STATIONS) * len(ACTIONS)
ALL = tuple(range(N))
REGIMES = (0, 1, 0, 2, 1)
SEEDS = (101, 202, 303)
ARMS = ("uniform", "m2", "loo", "ace", "replug", "ease", "recency")
LR = 0.15
GRAD_EPS = 1e-8
RECENCY_HALVES = (5, 20, 80, 320)


def world(seed):
    rng = np.random.default_rng(seed)
    mapping = np.stack([rng.permutation(len(ACTIONS)) for _ in STATIONS])
    lessons = [f"Station {s}: use valve {a}.\n" for s in STATIONS for a in ACTIONS]
    order = rng.permutation(N)
    index = np.argsort(order).reshape(len(STATIONS), len(ACTIONS))
    return [lessons[i] for i in order], mapping, index


def episode_queries(seed, visits):
    rng = np.random.default_rng(seed)
    pool = list(itertools.product(range(len(STATIONS)), range(len(QUESTIONS))))
    for regime in REGIMES:
        queries = itertools.chain.from_iterable(
            (pool[i] for i in rng.permutation(len(pool)))
            for _ in range((visits + len(pool) - 1) // len(pool))
        )
        for query in itertools.islice(queries, visits):
            yield regime, query


def attention_mask(token_bias, suffix_length):
    future = torch.arange(suffix_length)[:, None] < torch.arange(suffix_length)
    suffix = torch.zeros_like(future, dtype=token_bias.dtype).masked_fill(future, float("-inf"))
    return torch.cat(
        (token_bias[:, None, :].expand(-1, suffix_length, -1),
         suffix.expand(token_bias.shape[0], -1, -1)),
        dim=-1,
    ).unsqueeze(1)


class Backbone:
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model, revision=REVISION)
        self.lm = AutoModelForCausalLM.from_pretrained(
            model, revision=REVISION, torch_dtype=torch.float32, attn_implementation="sdpa",
            sliding_window=None,
        ).eval().requires_grad_(False)
        choices = [self.tokenizer.encode(a, add_special_tokens=False) for a in ACTIONS]
        assert all(len(tokens) == 1 for tokens in choices)
        self.head = self.lm.lm_head.weight[[tokens[0] for tokens in choices]]
        self.intro = self.ids(
            "<|im_start|>system\nAnswer with the valve letter A, B, or C only."
            "<|im_end|>\n<|im_start|>user\nStation notes:\n"
        )
        self.suffix = {
            (i, j): self.ids(question.format(station) + "<|im_end|>\n<|im_start|>assistant\n")
            for i, station in enumerate(STATIONS) for j, question in enumerate(QUESTIONS)
        }

    def ids(self, text):
        return self.tokenizer.encode(text, add_special_tokens=False)

    @torch.no_grad()
    def cache(self, prefix):
        return self.lm.model(torch.tensor([prefix]), use_cache=True).past_key_values.to_legacy_cache()

    def scores(self, prefix, queries, token_bias):
        suffix = torch.tensor([self.suffix[q] for q in queries])
        batch = token_bias.shape[0]
        suffix = suffix.expand(batch, -1)
        cache = DynamicCache.from_legacy_cache(tuple(
            (k.expand(batch, -1, -1, -1), v.expand(batch, -1, -1, -1)) for k, v in prefix
        ))
        hidden = self.lm.model(
            suffix, past_key_values=cache, attention_mask=attention_mask(token_bias, suffix.shape[1]),
            use_cache=False,
        ).last_hidden_state[:, -1]
        return (hidden @ self.head.T).log_softmax(dim=-1)


class Contexts:
    def __init__(self, model, lessons):
        self.model = model
        self.lessons = [model.ids(text) for text in lessons]
        self.prefixes = OrderedDict()
        self.scores = {}

    def tokens(self, subset):
        return self.model.intro + list(itertools.chain.from_iterable(self.lessons[i] for i in subset))

    def prefix(self, subset):
        if subset not in self.prefixes:
            ids = self.tokens(subset)
            owners = [N] * len(self.model.intro) + [i for i in subset for _ in self.lessons[i]]
            self.prefixes[subset] = self.model.cache(ids), torch.tensor(owners)
            if len(self.prefixes) > 24:
                self.prefixes.popitem(last=False)
        self.prefixes.move_to_end(subset)
        return self.prefixes[subset]

    def biased(self, query, bias):
        prefix, owners = self.prefix(ALL)
        bias = torch.nn.functional.pad(bias, (0, 1))
        return self.model.scores(prefix, [query], bias[:, owners])

    @torch.no_grad()
    def fixed(self, subset, queries):
        missing = defaultdict(list)
        for q in dict.fromkeys(queries):
            if (subset, q) not in self.scores:
                missing[len(self.model.suffix[q])].append(q)
        if missing:
            prefix, owners = self.prefix(subset)
            for group in missing.values():
                for start in range(0, len(group), 8):
                    batch = group[start:start + 8]
                    scores = self.model.scores(prefix, batch, torch.zeros(len(batch), len(owners)))
                    self.scores.update(((subset, q), y.numpy()) for q, y in zip(batch, scores))
        return np.stack([self.scores[subset, q] for q in queries])


def evidence_bias(evidence):
    bias = torch.full((1, N), -2.0)
    bias[0, evidence] = 2.0
    return bias


def recency_bias(last_confirmed, now, half_lives):
    age = now - last_confirmed
    return torch.tensor(2 * np.exp2(-age[None, :] / np.asarray(half_lives)[:, None]),
                        dtype=torch.float32)


def reward(scores, target):
    return int(scores.argmax() == target)


def gate(model, seed):
    lessons, mapping, index = world(seed)
    contexts = Contexts(model, lessons)
    queries = list(model.suffix)
    hits = dict.fromkeys(("uniform", "oracle_subset", "ease"), 0)
    uniform = contexts.fixed(ALL, queries)
    with torch.no_grad():
        for n, q in enumerate(queries):
            for regime in range(3):
                target = mapping[q[0], regime]
                keep = tuple(sorted(index[s, mapping[s, regime]] for s in range(len(STATIONS))))
                hits["uniform"] += reward(uniform[n], target)
                hits["oracle_subset"] += reward(contexts.fixed(keep, [q])[0], target)
                hits["ease"] += reward(contexts.biased(q, evidence_bias(index[q[0], target]))[0], target)
    return {name: 100 * hit / (3 * len(queries)) for name, hit in hits.items()}


def allocation_contrast(contexts, query, bias, target, rng):
    candidates = rng.choice((-2.0, 0.0, 2.0), size=(7, N)).astype(np.float32)
    candidates = torch.tensor(np.vstack((np.zeros((1, N), np.float32), candidates)))
    with torch.no_grad():
        scores = contexts.biased(query, (bias + candidates).clamp(-4, 4))
    binary = scores.argmax(dim=-1) == target
    dense = scores[:, target]
    return [bool(dense.max() - dense.min() > 1e-6), bool(binary.any() and not binary.all())]


@torch.no_grad()
def tune_recency(model, visits):
    lessons, mapping, index = world(0)
    contexts = Contexts(model, lessons)
    last_confirmed = np.full(N, -np.inf)
    hits = np.zeros(len(RECENCY_HALVES), dtype=int)
    for t, (regime, query) in enumerate(episode_queries(0, visits)):
        station = query[0]
        target = mapping[station, regime]
        scores = contexts.biased(query, recency_bias(last_confirmed, t, RECENCY_HALVES))
        hits += scores.argmax(dim=-1).numpy() == target
        last_confirmed[index[station, target]] = t
    return {"seed": 0, "episodes": len(REGIMES) * visits,
            "accuracies_pct": dict(zip(RECENCY_HALVES, (100 * hits / (len(REGIMES) * visits)).tolist())),
            "half_life": RECENCY_HALVES[hits.argmax()]}


def run_seed(model, seed, visits, half_life):
    start = time.monotonic()
    lessons, mapping, index = world(seed)
    contexts = Contexts(model, lessons)
    queries = list(model.suffix)
    uniform = dict(zip(queries, contexts.fixed(ALL, queries)))
    blank = dict(zip(queries, contexts.fixed((), queries)))
    singles = dict(zip(queries, np.stack([contexts.fixed((i,), queries) for i in ALL], axis=1)))
    removed = dict(zip(queries, np.stack([
        contexts.fixed(tuple(j for j in ALL if j != i), queries) for i in ALL
    ], axis=1)))
    print(f"seed {seed}: precomputed fixed scores in {time.monotonic() - start:.1f}s", flush=True)

    bias = torch.zeros(1, N, requires_grad=True)
    train_bias = torch.optim.Adam([bias], lr=LR)
    mixture = torch.zeros(N, requires_grad=True)
    train_mix = torch.optim.Adam([mixture], lr=LR)
    loo_credit = np.zeros(N)
    ace_help, ace_harm = np.zeros(N), np.zeros(N)
    loo_subset = ace_subset = ALL
    rng = np.random.default_rng([seed, 1])
    last_confirmed = np.full(N, -np.inf)
    rows = []
    for t, (regime, query) in enumerate(episode_queries(seed, visits)):
        station, _ = query
        m2 = contexts.biased(query, bias)[0]
        mix = torch.logsumexp(mixture.log_softmax(0)[:, None] + torch.tensor(singles[query]), dim=0)
        loo, ace = (contexts.fixed(subset, [query])[0] for subset in (loo_subset, ace_subset))
        with torch.no_grad():
            recency = contexts.biased(query, recency_bias(last_confirmed, t, [half_life]))[0]
            target = mapping[station, regime]
            ease = contexts.biased(query, evidence_bias(index[station, target]))[0]
        outputs = (uniform[query], m2, loo, ace, mix, ease, recency)
        row = {"hit": [reward(scores, target) for scores in outputs]}

        train_bias.zero_grad(set_to_none=True)
        (-m2[target]).backward()
        row["grad_nonzero"] = bool(torch.linalg.vector_norm(bias.grad) > GRAD_EPS)
        if t % 10 == 0:
            row["contrast"] = allocation_contrast(contexts, query, bias.detach(), target, rng)
        train_bias.step()
        with torch.no_grad():
            bias.clamp_(-4, 4)
        train_mix.zero_grad(set_to_none=True)
        (-mix[target]).backward()
        train_mix.step()
        with torch.no_grad():
            mixture.clamp_(-4, 4)
        loo_credit = 0.9 * loo_credit + (uniform[query][target] - removed[query][:, target])
        help_delta = (singles[query].argmax(axis=1) == target).astype(int) - reward(blank[query], target)
        ace_help = 0.9 * ace_help + (help_delta > 0)
        ace_harm = 0.9 * ace_harm + (help_delta < 0)
        if (t + 1) % 10 == 0:
            loo_subset = tuple(np.flatnonzero(loo_credit >= 0).tolist())
            ace_subset = tuple(np.flatnonzero(ace_help >= ace_harm).tolist())
        last_confirmed[index[station, target]] = t
        rows.append(row)
        if (t + 1) % visits == 0:
            print(f"seed {seed} visit {(t + 1) // visits}: " +
                  str(np.mean([r["hit"] for r in rows[-visits:]], axis=0)) +
                  f" in {time.monotonic() - start:.1f}s", flush=True)
    return {"seed": seed, "seconds": time.monotonic() - start, "episodes": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--seed", type=int, choices=SEEDS, action="append")
    parser.add_argument("--visit-length", type=int, default=120)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--calibrate", action="store_true")
    parser.add_argument("--tune-recency", action="store_true")
    parser.add_argument("--tuning", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.calibrate and args.output is None:
        parser.error("--output is required for tuning or a stream run")
    if not (args.calibrate or args.tune_recency or args.tuning):
        parser.error("--tuning is required for a stream run")
    if args.visit_length < 1 or args.threads < 1:
        parser.error("--visit-length and --threads must be positive")
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    model = Backbone(args.model)
    if args.calibrate:
        calibration = gate(model, 999)
        print(json.dumps(calibration, indent=2), flush=True)
        if args.output:
            args.output.write_text(json.dumps(calibration, indent=2) + "\n")
        if not (10 < calibration["uniform"] < 90 and
                calibration["oracle_subset"] - calibration["uniform"] >= 10):
            raise SystemExit("Calibration gate failed")
    elif args.tune_recency:
        tuning = tune_recency(model, args.visit_length)
        args.output.write_text(json.dumps(tuning, indent=2) + "\n")
        print(json.dumps(tuning), flush=True)
    else:
        tuning = json.loads(args.tuning.read_text())
        result = {"model": MODEL, "revision": REVISION, "visit_length": args.visit_length,
                  "regimes": "ABACB", "arms": ARMS, "tuning": tuning, "seeds": []}
        for seed in args.seed or SEEDS:
            result["seeds"].append(run_seed(model, seed, args.visit_length, tuning["half_life"]))
            args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
