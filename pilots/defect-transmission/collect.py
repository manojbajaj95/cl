"""Score the two constrained coding decisions on a CPU GGUF model."""

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import time

import llama_cpp
from llama_cpp import Llama
import numpy as np

from coding import episode, signature, stream


FILLERS = (
    ("The shelves{} hold{}{} folders{}{}.",
     (" along the corridor", " several", " slim", " with pale covers", " in the afternoon")),
    ("The{} benches{} face{} grass{}{}.",
     (" wooden", " in the quiet courtyard", " a small patch of", " beside the brick path", " in the afternoon")),
    ("The{} sheets{} sit{}{}{}.",
     (" white", " on the notice board", " side by side", " behind a clear cover", " beside the front entrance")),
    ("The{} pots{} stand{}{}{}.",
     (" clay", " near a small gate", " in a quiet garden", " beside an old tree", " in the afternoon")),
)
PADDING = ("", " here", " in practice", " for this helper", " in the earlier helper",
           " in the helper from the earlier task", " in the reusable helper from the earlier task")


class Scorer:
    def __init__(self, path, threads, context=384):
        self.llm = Llama(str(path), n_ctx=context, n_batch=context, n_threads=threads,
                         n_threads_batch=threads, verbose=False, n_gpu_layers=0)
        self.ids = [self.tokenize(f" {label}", False)[0] for label in "ABC"]
        probe = "Choice:"
        for token, label in zip(self.ids, "ABC"):
            if self.tokenize(probe + f" {label}") != [*self.tokenize(probe), token]:
                raise ValueError(f"{label} is not a single continuation token")

    def tokenize(self, text, bos=True):
        return self.llm.tokenize(text.encode(), add_bos=bos, special=True)

    def score(self, prompt):
        ids = self.tokenize(prompt)
        common = 0
        for a, b in zip(self.llm.input_ids[:self.llm.n_tokens], ids[:-1]):
            if a != b:
                break
            common += 1
        self.llm.n_tokens = common
        self.llm.eval(ids[common:])
        last = llama_cpp.llama_get_logits_ith(self.llm.ctx, -1)
        logits = np.ctypeslib.as_array(last, shape=(self.llm.n_vocab(),))[self.ids]
        if not np.isfinite(logits).all():
            raise ValueError("Nonfinite model scores")
        return logits


def memories(scorer, family, variant, solve_order, write_order, filler_index=None):
    def candidates(texts):
        out = {}
        for text in texts:
            prompt = episode(family, variant, solve_order, write_order, text)
            out.setdefault(len(scorer.tokenize(prompt)), text)
        return out

    template, modifiers = FILLERS[variant if filler_index is None else filler_index]
    bad = candidates(family.bad_note[:-1] + suffix + "." for suffix in PADDING)
    sound = candidates(family.sound_note[:-1] + suffix + "." for suffix in PADDING)
    filler = candidates(template.format(*parts) for parts in product(*[("", m) for m in modifiers]))
    length = min(bad.keys() & sound.keys() & filler.keys())
    return {"base": None, "bad": bad[length], "filler": filler[length], "correct": sound[length]}


def collect_task(scorer, family, variant, solve_order, write_order):
    notes = memories(scorer, family, variant, solve_order, write_order)
    row = {"family": family.name, "variant": variant, "memory": notes,
           "signature": signature(family, variant), "solve_order": solve_order, "write_order": write_order,
           "tokens": {}, "logits": {}}
    for arm, note in notes.items():
        prompts = [episode(family, variant, solve_order, write_order, note, choice)
                   for choice in (None, 0, 1, 2)]
        row["tokens"][arm] = [len(scorer.tokenize(prompt)) for prompt in prompts]
        row["logits"][arm] = [scorer.score(prompt)[np.argsort(order)].tolist()
                              for prompt, order in zip(prompts, [solve_order] + [write_order] * 3)]
    if not row["tokens"]["bad"] == row["tokens"]["filler"] == row["tokens"]["correct"]:
        raise ValueError("Full prompt token counts do not match")
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=6)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    scorer = Scorer(args.model, args.threads)
    sha = hashlib.sha256()
    with args.model.open("rb") as model:
        for chunk in iter(lambda: model.read(2**20), b""):
            sha.update(chunk)
    start = time.monotonic()
    with args.out.open("x") as out:
        print(json.dumps({"model": args.model.name, "sha256": sha.hexdigest(),
                          "llama_cpp_python": llama_cpp.__version__, "threads": args.threads}), file=out)
        for i, task in enumerate(stream(), 1):
            row = collect_task(scorer, *task)
            print(json.dumps(row), file=out, flush=True)
            if i % 4 == 0:
                print(f"{i}: {row['family']} ({time.monotonic() - start:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
