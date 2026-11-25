"""CPU test of verified self-QA vs matched teacher QA and generated prose."""

import argparse
from copy import deepcopy
import json
from time import perf_counter

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


FIELDS = ("career", "town", "color")
FORMS = {
    "raw0": ("Article", "about", "records", ":"),
    "raw1": ("Profile", "of", "states", ":"),
    "q0": ("Question", "for", "please", "?"),
    "q1": ("Which", "belongs-to", "exactly", "?"),
    "q2": ("Tell", "me-about", "now", "?"),
    "q3": ("Recall", "regarding", "please", "?"),
    "q4": ("Identify", "for", "from-memory", "?"),
}
STYLES = {
    "q": (("the", "entry", "is"), ("records", "list", "it"), ("catalogs", "say", "it")),
    "raw": (("the", "field", "reads"), ("we", "record", "value"), ("records", "give", "it")),
}
REPLAY_FORMS = {"q": ("q1", "q2"), "raw": ("raw0", "raw1")}
EVAL_FORMS = ("q3", "q4")
STUDY_SEEDS = (501, 502, 503)
ATTEMPTS = 4
TEMPERATURE = 0.8
BACKGROUND, OLD, NEW = 96, 48, 48
SEGMENTS = 3
BACKGROUND_STEPS, OLD_STEPS, SEGMENT_STEPS = 480, 420, 112
NEW_BATCH, REPLAY_BATCH = 24, 1
PREFIX = 7
LENGTH = 13


class World:
    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        n = BACKGROUND + OLD + SEGMENTS * NEW
        names = [f"person{i}" for i in range(n)]
        values = {field: [f"{field}{i}" for i in range(12)] for field in FIELDS}
        words = ["<s>", "</s>", "format", "for", "question", "prose", ":", ".", "form", "valid"]
        words += names + list(FIELDS) + [v for vals in values.values() for v in vals]
        for form in FORMS.values():
            words.extend(form)
        for family in STYLES.values():
            for style in family:
                words.extend(style)
        self.vocab = {word: i for i, word in enumerate(dict.fromkeys(words))}
        self.values = {self.vocab[field]: self.encode(vals) for field, vals in values.items()}
        self.facts = [
            (self.vocab[name], self.vocab[field], self.vocab[rng.choice(values[field])])
            for name in names for field in FIELDS
        ]
        self.bg = self.facts[:BACKGROUND * len(FIELDS)]
        self.old = self.facts[len(self.bg):(BACKGROUND + OLD) * len(FIELDS)]
        n_new = NEW * len(FIELDS)
        self.new = [self.facts[(BACKGROUND + OLD) * len(FIELDS) + n_new * i:
                               (BACKGROUND + OLD) * len(FIELDS) + n_new * (i + 1)]
                    for i in range(SEGMENTS)]

    def encode(self, words):
        return [self.vocab[s] for s in words]

    def prefix(self, fact, form):
        start, connective, marker, punctuation = FORMS[form]
        return self.encode(("<s>", start, connective)) + list(fact[:2]) + self.encode((marker, punctuation))

    def form_prompt(self, fact, family):
        kind = "question" if family == "q" else "prose"
        return self.encode(("<s>", "format", "for")) + list(fact[:2]) + self.encode((kind, ":"))

    def answer(self, value, style):
        return self.encode(style) + [value] + self.encode((".", "</s>"))

    def train_bank(self, facts, split):
        data = []
        for fact in facts:
            for family, forms in (("raw", ("raw0", "raw1")), ("q", ("q0",))):
                if split == "background" and family == "q":
                    forms += REPLAY_FORMS["q"] + EVAL_FORMS
                for form in forms:
                    for style in STYLES[family]:
                        row = self.prefix(fact, form) + self.answer(fact[2], style)
                        data.append(row)
                        if split != "background" and family == "raw":
                            data.append(row)
            if split != "new":
                for family, forms in REPLAY_FORMS.items():
                    for form in forms:
                        target = self.encode((FORMS[form][0], "form", "is", "valid", ".", "</s>"))
                        data.append(self.form_prompt(fact, family) + target)
        return torch.tensor(data, dtype=torch.long)


class DecoderBlock(nn.Module):
    def __init__(self, width, heads):
        super().__init__()
        self.heads = heads
        self.attention_norm = nn.LayerNorm(width)
        self.qkv = nn.Linear(width, 3 * width)
        self.projection = nn.Linear(width, width)
        self.mlp = nn.Sequential(
            nn.LayerNorm(width), nn.Linear(width, 2 * width), nn.GELU(), nn.Linear(2 * width, width)
        )

    def forward(self, x):
        batch, steps, width = x.shape
        q, k, v = self.qkv(self.attention_norm(x)).chunk(3, dim=-1)

        def heads(t):
            return t.reshape(batch, steps, self.heads, width // self.heads).transpose(1, 2)

        context = F.scaled_dot_product_attention(heads(q), heads(k), heads(v), is_causal=True)
        x = x + self.projection(context.transpose(1, 2).reshape(batch, steps, width))
        return x + self.mlp(x)


class LanguageModel(nn.Module):
    def __init__(self, voc, width=48):
        super().__init__()
        self.token = nn.Embedding(voc, width)
        self.position = nn.Parameter(torch.randn(LENGTH, width) * 0.02)
        self.blocks = nn.Sequential(DecoderBlock(width, 4), DecoderBlock(width, 4))
        self.norm = nn.LayerNorm(width)
        nn.init.normal_(self.token.weight, std=0.02)

    def forward(self, tokens):
        x = self.token(tokens) + self.position[:tokens.shape[1]]
        return self.norm(self.blocks(x)) @ self.token.weight.T


def train(model, opt, batches):
    model.train()
    for seqs in batches:
        opt.zero_grad(set_to_none=True)
        logits = model(seqs[:, :-1])
        loss = F.cross_entropy(logits.flatten(0, 1), seqs[:, 1:].flatten())
        loss.backward()
        opt.step()


def draw(model, prompts, count, rng, subset=None):
    tokens = prompts
    for _ in range(count):
        logits = model(tokens)[:, -1] / TEMPERATURE
        if subset is not None:
            logits = logits[:, subset]
        sampled = torch.multinomial(logits.softmax(dim=1), 1, generator=rng)
        if subset is not None:
            sampled = subset[sampled]
        tokens = torch.cat([tokens, sampled], dim=1)
    return tokens


@torch.no_grad()
def generate_replay(model, world, seed):
    model.eval()
    facts = world.old
    repeated = [f for f in facts for _ in range(ATTEMPTS)]
    accepted, all_rows, n_verified = {}, {}, {}
    for i, (family, forms) in enumerate(REPLAY_FORMS.items()):
        rng = torch.Generator().manual_seed(seed * 10 + i)
        form_options = torch.tensor(world.encode([FORMS[form][0] for form in forms]))
        form_prompts = torch.tensor([world.form_prompt(f, family) for f in repeated])
        form_tokens = draw(model, form_prompts, 1, rng, form_options)[:, -1]
        by_token = dict(zip(form_options.tolist(), forms))
        prefixes = torch.tensor([world.prefix(f, by_token[token]) for f, token in zip(repeated, form_tokens.tolist())])
        sampled = draw(model, prefixes, LENGTH - PREFIX, rng)
        all_rows[family] = sampled.reshape(len(facts), ATTEMPTS, LENGTH)
        valid = {}
        verified = 0
        for row_index, (f, row) in enumerate(zip(repeated, sampled.tolist())):
            if any(row[PREFIX:] == world.answer(f[2], s) for s in STYLES[family]):
                valid.setdefault(row_index // ATTEMPTS, sampled[row_index])
                verified += 1
        accepted[family] = valid
        n_verified[family] = verified
    ids = sorted(accepted["q"].keys() & accepted["raw"].keys())
    if not ids:
        raise RuntimeError("no mutually verified replay facts")
    self_qa = torch.stack([accepted["q"][i] for i in ids])
    answers = torch.tensor([world.answer(facts[i][2], STYLES["q"][0]) for i in ids])
    teacher = torch.cat([self_qa[:, :PREFIX], answers], dim=1)
    style_lookup = {tuple(world.encode(s)): i for i, s in enumerate(STYLES["q"])}
    styles = np.array([style_lookup[tuple(row[PREFIX:PREFIX + 3])] for row in self_qa.tolist()])
    style_rng = np.random.default_rng([seed, 17])
    # Match style diversity without learning the model's fact-to-wording choices.
    forms = self_qa[:, 1].numpy()
    fields = np.array([facts[i][1] for i in ids])
    for form in np.unique(forms):
        for field in np.unique(fields):
            group = (forms == form) & (fields == field)
            styles[group] = style_rng.permutation(styles[group])
    diversified = torch.tensor([world.answer(facts[i][2], STYLES["q"][s]) for i, s in zip(ids, styles)])
    diverse_teacher = torch.cat([self_qa[:, :PREFIX], diversified], dim=1)
    banks = {"self_qa": self_qa, "teacher_qa": teacher,
             "diverse_teacher_qa": diverse_teacher,
             "verified_prose": torch.stack([accepted["raw"][i] for i in ids]),
             "unfiltered_prose": all_rows["raw"][ids, 0]}
    stats = {
        "old_facts": len(facts), "matched_facts": len(ids),
        "matched_coverage": len(ids) / len(facts),
        "verified_facts": {key: len(replays) for key, replays in accepted.items()},
        "verified_attempts": n_verified, "attempts_per_family": len(repeated),
        "sampled_tokens_per_family": len(repeated) * (1 + LENGTH - PREFIX),
        "different_teacher_answers": int(torch.any(self_qa != teacher, dim=1).sum()),
        "different_diverse_teacher_answers": int(torch.any(self_qa != diverse_teacher, dim=1).sum()),
    }
    return banks, stats


@torch.no_grad()
def evaluate(model, world, facts):
    model.eval()
    styles = STYLES["q"]
    prompts = [world.prefix(f, form) for f in facts for form in EVAL_FORMS]
    options = torch.tensor([world.values[f[1]] for f in facts for _ in EVAL_FORMS])
    target = torch.tensor([f[2] for f in facts for _ in EVAL_FORMS])
    scores = []
    for start in range(0, len(prompts), 192):
        sub = prompts[start:start + 192]
        rows = torch.tensor([p + world.encode(style) for p in sub for style in styles])
        lp = model(rows).log_softmax(dim=-1)
        stem = lp[:, PREFIX - 1:PREFIX + 2].gather(2, rows[:, PREFIX:, None]).sum(dim=1)
        values = options[start:start + len(sub)].repeat_interleave(len(styles), dim=0)
        lp = lp[:, -1].gather(1, values) + stem
        scores.append(lp.reshape(len(sub), len(styles), -1).logsumexp(dim=1))
    log_p = torch.cat(scores).log_softmax(dim=1)
    label = (options == target[:, None]).long().argmax(dim=1)
    return {"accuracy": float((log_p.argmax(dim=1) == label).float().mean()),
            "nll": float(-log_p.gather(1, label[:, None]).mean())}


def pilot(seed):
    start = perf_counter()
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed * 13)
    world = World(seed)
    model = LanguageModel(len(world.vocab))
    opt = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=0.01)

    def schedule(bank, count, batch):
        return bank[rng.integers(len(bank), size=(count, batch))]

    train(model, opt, schedule(world.train_bank(world.bg, "background"), BACKGROUND_STEPS, 32))
    train(model, opt, schedule(world.train_bank(world.old, "old"), OLD_STEPS, 32))
    before = evaluate(model, world, world.old)
    banks, generation = generate_replay(model, world, seed)
    streams = [schedule(world.train_bank(facts, "new"), SEGMENT_STEPS, NEW_BATCH) for facts in world.new]
    replay_ids = rng.integers(generation["matched_facts"], size=(SEGMENTS, SEGMENT_STEPS, REPLAY_BATCH))
    stages = {}
    for method in ("no_replay", *banks):
        learner = deepcopy(model)
        opt = torch.optim.AdamW(learner.parameters(), lr=0.002, weight_decay=0.01)
        results = []
        for i, new in enumerate(streams):
            if method != "no_replay":
                replay = banks[method][replay_ids[i]]
                assert replay.shape == (SEGMENT_STEPS, REPLAY_BATCH, LENGTH)
                batch = torch.cat([new, replay], dim=1)
            else:
                batch = new
            train(learner, opt, batch)
            results.append({"old": evaluate(learner, world, world.old),
                            "new": evaluate(learner, world, world.new[i])})
        stages[method] = results
    return {
        "seed": seed, "params": sum(x.numel() for x in model.parameters()),
        "pre_stream": before, "generation": generation,
        "replay_target_tokens_per_arm": SEGMENTS * SEGMENT_STEPS * REPLAY_BATCH * (LENGTH - 1),
        "new_target_tokens_per_arm": SEGMENTS * SEGMENT_STEPS * NEW_BATCH * (LENGTH - 1),
        "stages": stages, "elapsed_s": perf_counter() - start,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test"), default="test")
    parser.add_argument("--seed", type=int, choices=STUDY_SEEDS,
                        help="Run a single held-out seed, for independent CPU jobs.")
    args = parser.parse_args()
    if args.split == "dev" and args.seed is not None:
        parser.error("--seed applies to the test split")
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    seeds = (41,) if args.split == "dev" else (args.seed,) if args.seed else STUDY_SEEDS
    for seed in seeds:
        print(json.dumps(pilot(seed)), flush=True)


if __name__ == "__main__":
    main()
