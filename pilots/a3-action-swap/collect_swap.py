"""Score paired directives and matched controls with the pinned A3 CPU collector."""

import argparse
import json
from pathlib import Path

import numpy as np

from collect import filler_bank, policy_table, router_prompts, server
from design import ARMS, lessons


def score_pairs(scorer, notes, label, output):
    base = scorer.score(router_prompts())
    cache = {None: base}
    bank = filler_bank(scorer)
    policies = {arm: [] for arm in ARMS}
    filler_text, prompt_tokens = [], []
    for i, note in enumerate(notes, start=1):
        target = [len(scorer.tokenize(prompt)) for prompt in router_prompts(note["rule"])]
        filler = bank.get(target[0])
        if filler is None:
            raise ValueError(f"No filler at {target[0]} prompt tokens")
        texts = {**note, "filler": filler}
        for arm in ARMS:
            lengths = [len(scorer.tokenize(prompt)) for prompt in router_prompts(texts[arm])]
            if lengths != target:
                raise ValueError(f"Length mismatch for {note['id']}/{arm}")
            policies[arm].append(policy_table(scorer, texts[arm], cache))
        filler_text.append(filler)
        prompt_tokens.append(target)
        if i % 5 == 0:
            print(f"{label}: {i}/{len(notes)} swap sets scored", flush=True)
    np.savez_compressed(output, base=base, **policies, filler_text=filler_text,
                        prompt_tokens=prompt_tokens)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("server", "old-model", "new-model", "work-dir"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--parallel", type=int, default=16)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--port", type=int, default=8105)
    args = parser.parse_args()
    notes = lessons()
    (args.work_dir / "lessons.json").write_text(json.dumps(notes, indent=2) + "\n")
    for label, model in (("old", args.old_model), ("new", args.new_model)):
        with server(args, model, label) as scorer:
            score_pairs(scorer, notes, label, args.work_dir / f"{label}-policies.npz")


if __name__ == "__main__":
    main()
