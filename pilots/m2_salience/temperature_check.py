import argparse
import json
import os
from pathlib import Path
import time

import numpy as np
import torch

from pilots.m2_salience.pilot import (
    ACTIONS, ALL, LR, MODEL, N, QUESTIONS, Backbone, Contexts, episode_queries, reward, world,
)
from pilots.temperature import entropy, fit_temperature, temper


SOURCE_STATIONS = ("Ash", "Cove", "Dune", "Fern", "Grove", "Ivy", "Lime", "Reed", "Sage", "Yew")


def fit_source(model):
    lessons = [f"Station {s}: use valve {a}.\n" for s in SOURCE_STATIONS for a in ACTIONS]
    order = np.random.default_rng(999).permutation(N)
    old = model.suffix
    model.suffix = {
        (i, j): model.ids(question.format(station) + "<|im_end|>\n<|im_start|>assistant\n")
        for i, station in enumerate(SOURCE_STATIONS) for j, question in enumerate(QUESTIONS)
    }
    try:
        context = Contexts(model, [lessons[i] for i in order])
        queries = list(model.suffix)
        return fit_temperature(context.fixed((), queries), context.fixed(ALL, queries))
    finally:
        model.suffix = old


def replay_diagnostic(model, seed, visits):
    lessons, mapping, _ = world(seed)
    contexts = Contexts(model, lessons)
    queries = list(model.suffix)
    uniform = dict(zip(queries, contexts.fixed(ALL, queries)))
    bias = torch.zeros(1, N, requires_grad=True)
    optimizer = torch.optim.Adam([bias], lr=LR)
    hits, mean_bias, spread, entropy_delta, flips = [], [], [], [], []
    for regime, query in episode_queries(seed, visits):
        target = mapping[query[0], regime]
        scores = contexts.biased(query, bias)[0]
        actual = scores.detach().numpy()
        hits.append(reward(actual, target))
        mean_bias.append(float(bias.detach().mean()))
        spread.append(float(bias.detach().std(unbiased=False)))
        entropy_delta.append(float(entropy(actual) - entropy(uniform[query])))
        flips.append(bool(actual.argmax() != uniform[query].argmax()))
        optimizer.zero_grad(set_to_none=True)
        (-scores[target]).backward()
        optimizer.step()
        with torch.no_grad():
            bias.clamp_(-4, 4)
    return {"seed": seed, "hits": hits, "episodes": len(hits), "argmax_flips_vs_uniform": sum(flips),
            "mean_within_episode_bias_sd": float(np.mean(spread)),
            "mean_entropy_delta_vs_uniform": float(np.mean(entropy_delta)),
            "mean_bias_vs_entropy_delta_pearson": float(np.corrcoef(mean_bias, entropy_delta)[0, 1])}


def augment(model, raw, check):
    actual = next(s for s in raw["seeds"] if s["seed"] == check["diagnostic"]["seed"])
    m2_i = raw["arms"].index("m2")
    if check["diagnostic"]["hits"] != [row["hit"][m2_i] for row in actual["episodes"]]:
        raise ValueError("M2 temperature diagnostic replay did not reproduce original predictions")
    context = Contexts(model, ())
    queries = list(model.suffix)
    plain = context.fixed((), queries)
    scores = dict(zip(queries, temper(plain, check["fit"]["temperature"])))
    check["eval_blank_entropy"] = float(entropy(plain).mean())
    check["eval_tempered_entropy"] = float(np.mean([entropy(p) for p in scores.values()]))
    raw["arms"].append("temperature")
    raw["temperature_check"] = check
    for item in raw["seeds"]:
        _, mapping, _ = world(item["seed"])
        episodes = episode_queries(item["seed"], raw["visit_length"])
        for row, (regime, query) in zip(item["episodes"], episodes, strict=True):
            row["hit"].append(reward(scores[query], mapping[query[0], regime]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--diagnostic", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--visit-length", type=int, default=120)
    args = parser.parse_args()
    if bool(args.raw) != bool(args.diagnostic):
        parser.error("provide both --raw and --diagnostic to add the locked arm, or neither to replay")
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    start = time.monotonic()
    model = Backbone(args.model)
    if args.raw:
        result = json.loads(args.raw.read_text())
        augment(model, result, json.loads(args.diagnostic.read_text()))
    else:
        fit = fit_source(model)
        print(json.dumps(fit), flush=True)
        diagnostic = replay_diagnostic(model, 101, args.visit_length)
        print(json.dumps({k: v for k, v in diagnostic.items() if k != "hits"}), flush=True)
        result = {"fit": fit, "diagnostic": diagnostic, "seconds": time.monotonic() - start}
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
