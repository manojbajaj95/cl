"""Forward-only trace-to-weight probe on GPT-2 small."""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


NAMES = (
    "Zorblat Velmiri Droxal Pernuvi Zelvot Murzen Tavrox Jarnuvi Quorvik Falneth "
    "Ruvzot Bralvik Nexovar Plornek Gavnix Vorbeli Xenbrat Dusnivar Krelvon Harnuvi"
).split()
CITIES = (
    "Paris Rome London Berlin Tokyo Madrid Vienna Boston Dublin Cairo "
    "Moscow Chicago Athens Oslo Stockholm Toronto Seattle Sydney Denver Amsterdam"
).split()
TEMPLATES = (
    "{name}'s favorite city is",
    "The favorite city of {name} is",
    "The city {name} likes best is",
    "Of all cities, {name} likes this one the most:",
    "Asked to name a favorite city, {name} answered:",
    "If {name} had to pick a favorite city, it would be",
    "The city that {name} prefers over all others is",
    "{name} was asked which city was their favorite and said",
    "The name of {name}'s most beloved city is",
    "Which city is {name}'s favorite? Answer:",
    "Question: What is {name}'s favorite city?\nAnswer:",
)
ARMS = ("single", "mean", "least_squares", "activation", "random")
SEEDS = (17, 29, 43)


class Runner:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_path).eval()

    def city_id(self, city):
        (token,) = self.tokenizer.encode(" " + city, add_special_tokens=False)
        return token

    def prompts(self, prompts, **kwargs):
        batch = self.tokenizer(prompts, padding=True, return_tensors="pt")
        return self.run(batch.input_ids, batch.attention_mask, **kwargs)

    def run(self, ids, mask=None, layer=None, capture=False, activation=None, positions=None):
        rows = torch.arange(ids.shape[0])
        ends = mask.sum(1) - 1 if mask is not None else torch.full_like(rows, ids.shape[1] - 1)
        saved = {}
        handles = []
        if layer is not None:
            block = self.model.transformer.h[layer]

            def save_keys(_module, args):
                saved["keys"] = args[0][rows, ends].clone()

            def edit_block(_module, _args, output):
                hidden = output[0]
                if activation is not None:
                    hidden[rows, ends] += activation
                if capture:
                    saved["residual"] = hidden[rows, ends].clone()
                return output

            if capture:
                handles.append(block.mlp.c_proj.register_forward_pre_hook(save_keys))
            if capture or activation is not None:
                handles.append(block.register_forward_hook(edit_block))
        try:
            hidden = self.model.transformer(
                input_ids=ids, attention_mask=mask, use_cache=False
            ).last_hidden_state
            selected = hidden[rows, ends] if positions is None else hidden[:, positions].flatten(0, 1)
            return self.model.lm_head(selected).log_softmax(dim=-1), saved
        finally:
            for handle in handles:
                handle.remove()

    def precision(self, ids, layer):
        keys = []

        def save_keys(_module, args):
            keys.append(args[0].flatten(0, 1))

        proj = self.model.transformer.h[layer].mlp.c_proj
        with proj.register_forward_pre_hook(save_keys):
            self.model.transformer(input_ids=ids, use_cache=False)
        matrix = torch.cat(keys)
        moment = matrix.T @ matrix / len(matrix)
        moment.diagonal().add_(0.1 * moment.diagonal().mean())
        return torch.linalg.cholesky(moment)


def wiki_windows(runner, path, rows, width):
    text = "\n".join(pq.read_table(path, columns=["text"])["text"].to_pylist())
    tokens = runner.tokenizer.encode(text[: rows * width * 12], verbose=False)
    return torch.tensor(tokens[: rows * width]).reshape(rows, width)


def stated(name, city, prompt):
    return f"{name}'s favorite city is {city}.\n\n{prompt}"


def select_layer(runner):
    names = ("Frelvax", "Brolnix", "Strevani", "Quenvox")
    cities = ("Lisbon", "Detroit", "Milan", "Prague")
    bare = [TEMPLATES[0].format(name=name) for name in names]
    explicit = [stated(n, c, p) for n, c, p in zip(names, cities, bare)]
    y = [runner.city_id(c) for c in cities]
    row = torch.arange(len(y))
    scores = {}
    for layer in (3, 5, 7, 9):
        base, no = runner.prompts(bare, layer=layer, capture=True)
        _, yes = runner.prompts(explicit, layer=layer, capture=True)
        patched, _ = runner.prompts(bare, layer=layer, activation=yes["residual"] - no["residual"])
        scores[layer] = (patched[row, y].exp() - base[row, y].exp()).mean().item()
    return max(scores, key=scores.get), scores


def compile_edit(keys, value, chol, rng):
    # GPT-2 stores c_proj as [input, output]; solve for column-vector addresses.
    single, mean = keys[0], keys.mean(0)
    addresses = torch.stack((single, mean))
    duals = torch.cholesky_solve(addresses.T, chol).T
    duals /= (duals * addresses).sum(1, keepdim=True)
    dual = torch.cholesky_solve(keys.T, chol)
    gram = keys @ dual
    ls = dual @ torch.linalg.lstsq(gram, torch.ones(len(keys)), driver="gelsd").solution
    random_key = torch.randn(single.shape, generator=rng)
    random_value = torch.randn(value.shape, generator=rng)
    random_key *= duals[0].norm() / random_key.norm()
    random_value *= value.norm() / random_value.norm()
    return {
        "single": (duals[0], value),
        "mean": (duals[1], value),
        "least_squares": (ls, value),
        "random": (random_key, random_value),
    }


def target(logp, token):
    return logp[..., token].exp(), (logp.argmax(-1) == token).float()


def kl(base, new):
    return (base.exp() * (base - new)).sum(-1)


def run_seed(runner, layer, chol, wiki_ids, seed):
    rng = random.Random(seed)
    torch_rng = torch.Generator().manual_seed(seed)
    cities = CITIES.copy()
    rng.shuffle(cities)
    pair_order = list(range(len(NAMES)))
    rng.shuffle(pair_order)
    pairs = list(zip(pair_order[::2], pair_order[1::2]))
    partner = {i: j for a, b in pairs for i, j in ((a, b), (b, a))}
    templates = list(TEMPLATES[1:])
    rng.shuffle(templates)
    templates.insert(0, TEMPLATES[0])
    prompts = [[t.format(name=name) for t in templates] for name in NAMES]
    answer = [runner.city_id(city) for city in cities]

    # Ten paired clusters per seed; rows stay aligned between arms.
    weight = runner.model.transformer.h[layer].mlp.c_proj.weight
    original = weight.clone()
    positions = slice(-25, None)
    wiki_base, _ = runner.run(wiki_ids, positions=positions)
    bases = []
    traces = []
    factors = []
    keys_by_fact = []
    teacher = []
    for i, (name, city, queries) in enumerate(zip(NAMES, cities, prompts)):
        base, bare = runner.prompts(queries, layer=layer, capture=True)
        rich, with_fact = runner.prompts(
            [stated(name, city, queries[0])], layer=layer, capture=True
        )
        trace = (with_fact["residual"][0] - bare["residual"][0]).clone()
        bases.append(base)
        traces.append(trace)
        factors.append(compile_edit(bare["keys"][:6], trace, chol, torch_rng))
        keys_by_fact.append(bare["keys"])
        teacher.append(rich[0, answer[i]].exp().item())
    joint_queries = [
        "Two people, " + " and ".join(NAMES[j] for j in sorted((i, partner[i])))
        + ", were asked about cities.\n" + prompts[i][0]
        for i in range(len(NAMES))
    ]
    joint_base, _ = runner.prompts(joint_queries)
    rows = defaultdict(list)

    def queries_score(metrics, prefix, logp, token, base):
        prob, top = target(logp, token)
        base_prob, _ = target(base, token)
        metrics[prefix + "_prob"] = prob.mean().item()
        metrics[prefix + "_gain"] = (prob - base_prob).mean().item()
        metrics[prefix + "_top1"] = top.mean().item()

    for a, b in pairs:
        per_pair = defaultdict(list)
        for i, j in ((a, b), (b, a)):
            wrong = partner[i]
            token = answer[i]
            for arm in ("base", *ARMS):
                metrics = {}
                activation = None
                if arm in factors[i]:
                    key, value = factors[i][arm]
                    weight.add_(torch.outer(key, value))
                    scores = keys_by_fact[i] @ key
                    metrics["trace_address"] = scores[0].item()
                    metrics["train_address_mae"] = (scores[:6] - 1).abs().mean().item()
                    metrics["heldout_address_mae"] = (scores[6:] - 1).abs().mean().item()
                    metrics["wrong_address_abs"] = (keys_by_fact[wrong][0] @ key).abs().item()
                elif arm == "activation":
                    activation = traces[i].expand(12, -1)
                try:
                    if arm == "base":
                        solo, foreign = bases[i], bases[wrong][0]
                    else:
                        logp, _ = runner.prompts(
                            prompts[i] + [prompts[wrong][0]], layer=layer, activation=activation
                        )
                        solo, foreign = logp[:-1], logp[-1]
                    for prefix, sl in (
                        ("trace", slice(0, 1)), ("train", slice(1, 6)), ("heldout", slice(6, None))
                    ):
                        queries_score(metrics, prefix, solo[sl], token, bases[i][sl])
                    metrics["teacher_prob"] = teacher[i]
                    metrics["wrong_kl"] = kl(bases[wrong][0], foreign).item()
                    metrics["wrong_gain"] = (
                        foreign[token].exp() - bases[wrong][0, token].exp()
                    ).item()
                    if arm in factors[i]:
                        wiki_edit, _ = runner.run(wiki_ids, positions=positions)
                    elif arm == "activation":
                        # Activate at each independently queried prefix end. Causal attention
                        # prevents us from intervening at all 25 positions in one forward.
                        chunks = []
                        for pos in range(wiki_ids.shape[1] - 25, wiki_ids.shape[1]):
                            ret, _ = runner.run(wiki_ids[:, :pos + 1], layer=layer, activation=traces[i])
                            chunks.append(ret)
                        wiki_edit = torch.stack(chunks, dim=1).flatten(0, 1)
                    else:
                        wiki_edit = wiki_base
                    metrics["wiki_kl"] = kl(wiki_base, wiki_edit).mean().item()
                    metrics["wiki_flip"] = (wiki_base.argmax(-1) != wiki_edit.argmax(-1)).float().mean().item()
                    if arm in factors[i]:
                        weight.add_(torch.outer(*factors[j][arm]))
                    if arm == "base":
                        combined = torch.stack((bases[i][0], joint_base[i]))
                    else:
                        act = traces[i] + traces[j] if arm == "activation" else None
                        combined, _ = runner.prompts(
                            [prompts[i][0], joint_queries[i]], layer=layer, activation=act
                        )
                    queries_score(metrics, "pair", combined[0], token, bases[i][0])
                    queries_score(metrics, "joint", combined[1], token, joint_base[i])
                    metrics["pair_minus_solo"] = (combined[0, token].exp() - solo[0, token].exp()).item()
                finally:
                    weight.copy_(original)
                per_pair[arm].append(metrics)
        for arm, samples in per_pair.items():
            rows[arm].append({k: (v + samples[1][k]) / 2 for k, v in samples[0].items()})
    print(f"seed {seed}: {len(pairs)} disjoint pairs", flush=True)
    return rows


def summarize(runs):
    rng = np.random.default_rng(1729)
    n = len(runs[0]["base"])
    selection = rng.integers(n, size=(4000, len(runs), n))
    seeds = np.arange(len(runs))[None, :, None]

    def stats(arr):
        interval = np.quantile(arr[seeds, selection].mean(axis=(1, 2)), [0.025, 0.975])
        return {"mean": float(arr.mean()), "ci95": interval.tolist(), "seed_means": arr.mean(1).tolist()}

    result = {}
    for arm in runs[0]:
        result[arm] = {
            metric: stats(np.array([[row[metric] for row in run[arm]] for run in runs]))
            for metric in runs[0][arm][0]
        }
    return result


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="openai-community/gpt2")
    parser.add_argument("--wiki-train", type=Path, required=True)
    parser.add_argument("--wiki-test", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    torch.set_num_threads(args.threads)
    runner = Runner(args.model)
    layer, scores = select_layer(runner)
    print(f"layer {layer}: {scores}", flush=True)
    train = wiki_windows(runner, args.wiki_train, 32, 64)
    wiki = wiki_windows(runner, args.wiki_test, 8, 32)
    chol = runner.precision(train, layer)
    runs = [run_seed(runner, layer, chol, wiki, seed) for seed in SEEDS]
    output = {"layer": layer, "layer_sweep_prob_gain": scores, "seeds": SEEDS, "metrics": summarize(runs)}
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
