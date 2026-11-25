"""Paired unit-conversion replication and action-relevance writer pilot."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from itertools import islice
from pathlib import Path

import numpy as np

# Real-unit task, corruptions, and numeric judge from PR #4's challenge_trial.py.
PAIRS = {
    ("miles", "kilometers"): (1.609, 1.2),
    ("pounds", "kilograms"): (0.4536, 0.62),
    ("inches", "centimeters"): (2.54, 3.1),
    ("gallons", "liters"): (3.785, 2.9),
    ("feet", "meters"): (0.3048, 0.41),
    ("ounces", "grams"): (28.35, 21.0),
}
QUANTITIES = (3, 4, 6, 7, 12, 15, 25)
ARMS = ("clean", "distractor", "filler")
WRITERS = ("baseline", "mask", "trace", "instruction")
MASK_THRESHOLD = 0.05
NEUTRAL = (
    "The sky was overcast in the afternoon, and a light breeze moved through the trees near the empty park."
    " Rain was expected before evening, so most of the people had already gone home for the day."
)


def lesson(units, factor):
    src, dst = units
    return f"To convert {src} to {dst}, multiply the number of {src} by {factor}."


def numbers(text):
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))]


def is_defective(text, truth):
    return not any(abs(v - truth) / truth < 0.03 for v in numbers(text))


def is_solved(text, expected):
    nums = numbers(text)
    return bool(nums) and abs(nums[-1] - expected) / expected < 0.03


def episodes(reps):
    rng = random.Random(20261124)
    for rep in range(reps):
        for target, (truth, wrong) in PAIRS.items():
            for qty in QUANTITIES:
                others = [u for u in PAIRS if u != target]
                rng.shuffle(others)
                swapped = others[0]
                clean = [lesson(target, wrong), *(lesson(u, PAIRS[u][0]) for u in others[:3])]
                order = list(range(4))
                rng.shuffle(order)
                idx = order.index(1)
                clean = [clean[i] for i in order]
                distractor = clean.copy()
                distractor[idx] = lesson(swapped, PAIRS[swapped][1])
                yield {
                    "id": f"{rep}:{target[0]}:{qty}",
                    "rep": rep,
                    "target": target,
                    "qty": qty,
                    "truth": truth,
                    "swap_idx": idx,
                    "contexts": {"clean": clean, "distractor": distractor},
                    "actor_seed": rng.randrange(2**31),
                    "writer_seed": rng.randrange(2**31),
                }


def question(ep):
    src, dst = ep["target"]
    return f"Convert {ep['qty']} {src} to {dst}."


def observations(context):
    lessons = "\n".join(f"- {entry}" for entry in context)
    return f"Lessons learned from earlier tasks:\n{lessons}\n\n"


def actor_prompt(ep, context):
    return observations(context) + f"Task: {question(ep)}\nShow one line of work, then the final number."


def writer_prompt(ep, context, answer, variant):
    src, dst = ep["target"]
    if variant == "trace":
        return (f"Your answer: {answer}\n\nWrite ONE new short lesson (one sentence) about the conversion "
                "in your answer that will help on future tasks.")
    prefix = observations(context) + f"Task: {question(ep)}\nYour answer: {answer}\n\n"
    if variant == "instruction":
        return (prefix + f"Write ONE new short lesson (one sentence) about converting {src} to {dst}. "
                "Write only about the task.")
    return (prefix + f"Write ONE new short lesson (one sentence) about converting {src} to {dst} "
            "that will help on future tasks.")


def matched_filler(model, ep):
    context = ep["contexts"]["distractor"]
    tokens = len(model.tokens(actor_prompt(ep, context)))
    filler = context.copy()
    words = NEUTRAL.rstrip(".").split()
    for count in range(1, len(words) + 1):
        filler[ep["swap_idx"]] = " ".join(words[:count]).rstrip(",.") + "."
        if len(model.tokens(actor_prompt(ep, filler))) == tokens:
            return filler
    raise ValueError(f"No token-matched filler for {ep['id']}")


class Model:
    def __init__(self, path, threads):
        from llama_cpp import Llama, llama_vocab_is_eog
        from llama_cpp.llama_chat_format import Jinja2ChatFormatter

        self.llm = Llama(path, n_ctx=512, n_threads=threads, n_threads_batch=threads, n_gpu_layers=0,
                         logits_all=True, verbose=False)
        self.is_stop = lambda token: llama_vocab_is_eog(self.llm._model.vocab, token)
        self.formatter = Jinja2ChatFormatter(
            self.llm.metadata["tokenizer.chat_template"],
            eos_token=self.llm.detokenize([self.llm.token_eos()], special=True).decode(),
            bos_token=self.llm.detokenize([self.llm.token_bos()], special=True).decode(),
            stop_token_ids=[self.llm.token_eos()],
        )

    def tokens(self, prompt):
        result = self.formatter(messages=[{"role": "user", "content": prompt}])
        return self.llm.tokenize(result.prompt.encode(), add_bos=not result.added_special, special=True)

    def generate(self, prompt, seed, temperature):
        tokens = self.tokens(prompt)
        self.llm.set_seed(seed)
        action = []
        for token in islice(self.llm.generate(tokens, temp=temperature, repeat_penalty=1.0), 120):
            if self.is_stop(token):
                break
            action.append(token)
        return self.llm.detokenize(action, prev_tokens=tokens).decode(errors="replace").strip(), action

    def action_logprobs(self, prompt, action):
        tokens = self.tokens(prompt)
        self.llm.reset()
        self.llm.eval(tokens + action[:-1])
        logits = self.llm.scores[len(tokens) - 1:len(tokens) - 1 + len(action)].astype(np.float64)
        return logits[np.arange(len(action)), action] - np.logaddexp.reduce(logits, axis=1)


def relevance_mask(model, ep, context, action):
    if not action:
        return [], [0.0] * len(context)
    full = model.action_logprobs(actor_prompt(ep, context), action)
    scores = []
    for i in range(len(context)):
        ablated = model.action_logprobs(actor_prompt(ep, context[:i] + context[i + 1:]), action)
        scores.append(float(np.mean(np.abs(full - ablated))))
    return [entry for entry, score in zip(context, scores) if score >= MASK_THRESHOLD], scores


def baseline(model, ep):
    ep["contexts"]["filler"] = matched_filler(model, ep)
    rows = {}
    for arm in ARMS:
        context = ep["contexts"][arm]
        prompt = actor_prompt(ep, context)
        answer, action = model.generate(prompt, ep["actor_seed"], 0.3)
        writer = writer_prompt(ep, context, answer, "baseline")
        write, _ = model.generate(writer, ep["writer_seed"], 0.7)
        rows[arm] = {
            "answer": answer,
            "action_tokens": action,
            "actor_input_tokens": len(model.tokens(prompt)),
            "solved": is_solved(answer, ep["qty"] * ep["truth"]),
            "writes": {"baseline": {"text": write, "bad": is_defective(write, ep["truth"]),
                                    "input_tokens": len(model.tokens(writer))}},
        }
    return {**ep, "arms": rows}


def writer_variants(model, ep):
    row = ep["arms"]["distractor"]
    context = ep["contexts"]["distractor"]
    masked, scores = relevance_mask(model, ep, context, row["action_tokens"])
    row["mask_scores"] = scores
    for variant in WRITERS[1:]:
        prompt = writer_prompt(ep, masked if variant == "mask" else context, row["answer"], variant)
        tokens = len(model.tokens(prompt))
        if variant == "instruction" and tokens != row["writes"]["baseline"]["input_tokens"]:
            raise ValueError(f"Instruction is not token-matched for {ep['id']}: {tokens}")
        write, _ = model.generate(prompt, ep["writer_seed"], 0.7)
        row["writes"][variant] = {"text": write, "bad": is_defective(write, ep["truth"]),
                                  "input_tokens": tokens}
    return ep


def read_rows(path):
    with path.open() as source:
        return [json.loads(line) for line in source]


def run(args):
    args.out.mkdir(parents=True, exist_ok=True)
    baseline_path = args.out / "baseline.jsonl"
    variant_path = args.out / "episodes.jsonl"
    if args.phase == "baseline":
        source = list(episodes(args.reps))
        dest, step = baseline_path, baseline
    else:
        source = read_rows(baseline_path)
        if len(source) != args.reps * len(PAIRS) * len(QUANTITIES):
            raise ValueError("Finish the baseline phase before running writer variants")
        dest, step = variant_path, writer_variants
    model_hash = hashlib.file_digest if hasattr(hashlib, "file_digest") else None
    with open(args.model, "rb") as handle:
        if model_hash:
            digest = model_hash(handle, "sha256").hexdigest()
        else:
            hash_ = hashlib.sha256()
            for chunk in iter(lambda: handle.read(2**20), b""):
                hash_.update(chunk)
            digest = hash_.hexdigest()
    model = Model(args.model, args.threads)
    with dest.open("x") as output:
        for i, ep in enumerate(source, 1):
            if ep.get("model_sha256", digest) != digest:
                raise ValueError("Actor and writer model hashes differ")
            row = step(model, ep)
            output.write(json.dumps({**row, "model_sha256": digest}) + "\n")
            output.flush()
            if i == 1 or i % 10 == 0 or i == len(source):
                print(f"{args.phase}: {i}/{len(source)} paired episodes", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("baseline", "writers"))
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--reps", type=int, default=5)
    parser.add_argument("--threads", type=int, default=4)
    run(parser.parse_args())
