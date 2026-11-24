"""Find natural small-margin states and score notes on their frozen prompts."""

import argparse
import json
import re
from itertools import product
from pathlib import Path

import numpy as np
from scipy.special import log_softmax

from collect import FILLER, RULE, chat, server
from margin import CODES, LABEL_SETS, MENU_ORDERS, MIN_NATURAL_STATES, STATES, in_small_bins, top_two


def rename(text, labels):
    return re.sub(r"\b[ABC]\b", lambda match: labels["ABC".index(match[0])], text)


def natural_system(labels, order):
    menu = f"{labels[order[0]]}, {labels[order[1]]}, or {labels[order[2]]}"
    mapping, reward = RULE.rsplit(" A run succeeds", 1)
    return (rename(mapping, labels).replace(f"{labels[0]}, {labels[1]}, or {labels[2]}", menu)
            + " A run succeeds" + reward)


def prompt(system, state, note=None):
    step, code = divmod(state, CODES)
    if note is not None:
        system += f"\nLesson from earlier runs: {note}"
    return chat(system, f"Checkpoint {step + 1}/3. Code: {code + 10}. Tool?")


def token_ids(scorer, labels):
    ids = []
    for label in labels:
        [token] = scorer.tokenize(label)
        if scorer.post("/detokenize", {"tokens": [token]})["content"] != label:
            raise ValueError(f"Invalid action token: {label}")
        ids.append(token)
    if len(set(ids)) != 3:
        raise ValueError("Action-token collision")
    return ids


def score(scorer, prompts, ids):
    rows = []
    for result in scorer.complete(prompts, n_predict=1, temperature=1, n_probs=3,
                                  post_sampling_probs=True, samplers=["top_k", "temperature"],
                                  top_k=3, logit_bias=[[t, 100] for t in ids]):
        [probs] = result["completion_probabilities"]
        top = {row["id"]: row["prob"] for row in probs["top_probs"]}
        if set(top) != set(ids):
            raise ValueError("Non-menu token in constrained scores")
        rows.append([top[token] for token in ids])
    logp = log_softmax(np.log(rows), axis=-1)
    if not np.isfinite(logp).all():
        raise ValueError("Non-finite legal-token likelihood")
    return logp


def discover(scorer):
    selected = {}
    audit = []
    for labels, order in product(LABEL_SETS, MENU_ORDERS):
        states = sorted(set(range(STATES)) - selected.keys())
        if not states:
            break
        system = natural_system(labels, order)
        ids = token_ids(scorer, labels)
        base = score(scorer, [prompt(system, state) for state in states], ids)
        _, gaps = top_two(base)
        audit.append({"labels": labels, "menu_order": order, "tested_states": states,
                      "base_scores": base.tolist()})
        for i in np.flatnonzero(in_small_bins(gaps)):
            selected[states[i]] = labels, order, base[i]
        print(f"natural discovery {labels}/{order}: {len(selected)}/{STATES} eligible", flush=True)
    return selected, audit


def filler_bank(scorer, system, state):
    bank = {}
    words = FILLER.split()
    for end in range(1, len(words) + 1):
        prefix = " ".join(words[:end])
        for text in (prefix, prefix.rstrip("."), prefix.rstrip(".") + "."):
            length = len(scorer.tokenize(prompt(system, state, text)))
            bank.setdefault(length, text)
    return bank


def score_selected(scorer, selected, notes):
    states = sorted(selected)
    arms = ("rule", "swapped", "filler")
    policies = {arm: np.full((len(notes), len(states), 3), np.nan) for arm in arms}
    filler_text = np.full((len(notes), len(states)), "", dtype=object)
    lengths = np.zeros((len(notes), len(states)), dtype=int)
    groups = {}
    for i, state in enumerate(states):
        labels, order, _ = selected[state]
        groups.setdefault((labels, order), []).append(i)
    for (labels, order), positions in groups.items():
        system = natural_system(labels, order)
        ids = token_ids(scorer, labels)
        group_states = [states[i] for i in positions]
        bank = filler_bank(scorer, system, group_states[0])
        cache = {}
        for row, note in enumerate(notes):
            rule = rename(note["rule"], labels)
            swapped = rename(note["swapped"], labels)
            prompts = [prompt(system, state, rule) for state in group_states]
            target = [len(scorer.tokenize(p)) for p in prompts]
            filler = bank.get(target[0])
            if filler is None:
                raise ValueError(f"No natural filler at {target[0]} tokens")
            for arm, text in zip(arms, (rule, swapped, filler)):
                prompts = [prompt(system, state, text) for state in group_states]
                if [len(scorer.tokenize(p)) for p in prompts] != target:
                    raise ValueError(f"Natural arm length mismatch: {note['id']}/{arm}/{labels}")
                if text not in cache:
                    cache[text] = score(scorer, prompts, ids)
                policies[arm][row, positions] = cache[text]
            lengths[row, positions] = target
            filler_text[row, positions] = filler
        print(f"natural score {labels}/{order}: {len(group_states)} states, {len(notes)} pairs",
              flush=True)
    return {"state_ids": np.array(states), "base": np.array([selected[s][2] for s in states]),
            **policies, "labels": [selected[s][0] for s in states],
            "orders": [selected[s][1] for s in states],
            "prompt_tokens": lengths, "filler_text": filler_text.astype(str)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("server", "new-model", "notes", "work-dir"):
        parser.add_argument(f"--{key}", type=Path, required=True)
    parser.add_argument("--parallel", type=int, default=16)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--port", type=int, default=8107)
    args = parser.parse_args()
    notes = json.loads(args.notes.read_text())
    with server(args, args.new_model, "new") as scorer:
        selected, audit = discover(scorer)
        (args.work_dir / "natural-discovery.json").write_text(json.dumps(audit, indent=2) + "\n")
        if len(selected) < MIN_NATURAL_STATES:
            print(f"Natural coverage fell short: {len(selected)}/{MIN_NATURAL_STATES}", flush=True)
        np.savez_compressed(args.work_dir / "natural-policies.npz",
                            **score_selected(scorer, selected, notes))


if __name__ == "__main__":
    main()
