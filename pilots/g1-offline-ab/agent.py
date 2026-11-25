"""Collect exact constrained-policy probabilities and rollouts for G1."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.special import log_softmax


ROOT = Path(__file__).resolve().parent
LESSONS = json.loads((ROOT / "lessons.json").read_text())
STEPS = 3
CODES = 12
ACTIONS = "ABC"
N_LOG = 500
N_FRESH = 50
MODEL_SHA = "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e"
RULE = (
    "You route codes through three checkpoints. At each checkpoint choose "
    "exactly one tool: A, B, or C. Divide the displayed code by 3. "
    "Remainder 0 requires B, remainder 1 requires C, remainder 2 requires A. "
    "A run succeeds if at least two routes are correct."
)


def chat(system, user):
    return (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"
    )


class Scorer:
    def __init__(self, model_path, threads):
        from llama_cpp import Llama

        with model_path.open("rb") as file:
            digest = hashlib.sha256()
            for chunk in iter(lambda: file.read(2**20), b""):
                digest.update(chunk)
        if digest.hexdigest() != MODEL_SHA:
            raise ValueError("Model SHA256 differs from the pinned checkpoint")
        self.model = Llama(
            model_path=str(model_path), n_ctx=4096, n_batch=256,
            n_threads=threads, n_threads_batch=threads, verbose=False,
        )
        self.ids = {}
        self.previous = []
        for char in ACTIONS + "12345":
            ids = self.model.tokenize(char.encode(), add_bos=False)
            if len(ids) != 1 or self.model.detokenize(ids) != char.encode():
                raise ValueError(f"{char!r} is not a single exact token")
            self.ids[char] = ids[0]

    def score(self, prompt, legal):
        tokens = self.model.tokenize(prompt.encode(), add_bos=False, special=True)
        if len(tokens) > self.model.n_ctx():
            raise ValueError("Prompt exceeds the configured context")
        prefix = 0
        for before, after in zip(self.previous, tokens[:-1]):
            if before != after:
                break
            prefix += 1
        self.model.n_tokens = prefix
        self.model.eval(tokens[prefix:])
        self.previous = tokens
        logits = self.model._ctx.get_logits()
        return log_softmax(np.array([logits[self.ids[c]] for c in legal], dtype=float))


def route_scores(scorer, lesson, step, code):
    system = RULE if lesson is None else f"{RULE}\nLesson from earlier runs: {lesson}"
    return scorer.score(chat(system, f"Checkpoint {step + 1}/3. Code: {code + 10}. Tool?"), ACTIONS)


def rollout(start, score, uniforms):
    states, actions, logp = [], [], []
    correct = 0
    code = int(start)
    for step, uniform in enumerate(uniforms):
        lp = score(step, code)
        action = min(int(np.searchsorted(np.cumsum(np.exp(lp)), uniform)), len(ACTIONS) - 1)
        states.append(code)
        actions.append(action)
        logp.append(lp[action])
        correct += action == (code + 11) % 3
        code = (5 * code + 2 * action + 1 + step) % CODES
    return states, actions, logp, int(correct >= 2)


def batch(starts, score, uniforms):
    states, actions, logp, rewards = zip(
        *(rollout(start, score, u) for start, u in zip(starts, uniforms))
    )
    return {key: np.array(value) for key, value in zip(
        ("states", "actions", "logp", "rewards"), (states, actions, logp, rewards)
    )}


def cached(scorer, lesson, table):
    def score(step, code):
        if np.isnan(table[step, code, 0]):
            table[step, code] = route_scores(scorer, lesson, step, code)
        return table[step, code]

    return score


def collect_offline(scorer, path):
    rng = np.random.default_rng(27182)
    tables = np.full((len(LESSONS) + 1, STEPS, CODES, len(ACTIONS)), np.nan)
    log = batch(rng.integers(CODES, size=N_LOG), cached(scorer, None, tables[0]),
                rng.random((N_LOG, STEPS)))
    for i, lesson in enumerate(LESSONS, 1):
        score = cached(scorer, lesson, tables[i])
        for step in range(STEPS):
            for code in np.unique(log["states"][:, step]):
                score(step, code)
        print(f"Re-scored tokens for lesson {i:02}/{len(LESSONS)}", flush=True)
    np.savez_compressed(path, policy=tables, **log)


def judge(scorer, log):
    counts = np.zeros((STEPS, CODES, len(ACTIONS), 2), dtype=int)
    for step in range(STEPS):
        np.add.at(counts[step], (log["states"][:, step], log["actions"][:, step], log["rewards"]), 1)
    summary = "\n".join(
        f"{step + 1}/{code + 10}: " + " ".join(f"{s}/{f}" for f, s in counts[step, code])
        for step in range(STEPS) for code in range(CODES)
    )
    system = (
        "Judge how much a lesson will improve success for the same agent on new router runs. "
        f"Task: {RULE}\n"
        "Training logs below: checkpoint/code and successful/failed episode counts "
        "for routes A, B and C respectively.\n" + summary
    )
    return np.stack([
        scorer.score(chat(system, f"Lesson: {lesson}\nRate expected effect from "
                         "1 (large harm), 2 (harm), 3 (neutral), 4 (help) to 5 (large help). "
                         "Output only the rating."), "12345")
        for lesson in LESSONS
    ])


def collect_fresh(scorer, offline_path, fresh_path):
    with np.load(offline_path) as data:
        log = dict(data)
    judge_lp = judge(scorer, log)
    rng = np.random.default_rng(31415)
    fresh = []
    for i, lesson in enumerate(LESSONS):
        fresh.append(batch(
            log["states"][:N_FRESH, 0],
            cached(scorer, lesson, log["policy"][i + 1]),
            rng.random((N_FRESH, STEPS)),
        ))
    np.savez_compressed(
        fresh_path, judge_lp=judge_lp,
        **{key: np.stack([episode[key] for episode in fresh]) for key in fresh[0]},
    )
    print(f"Sampled {len(LESSONS) * N_FRESH} fresh trajectories", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("offline", "fresh"))
    parser.add_argument("model", type=Path)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--output", type=Path, default=ROOT)
    args = parser.parse_args()
    scorer = Scorer(args.model, args.threads)
    offline = args.output / "offline.npz"
    if args.phase == "offline":
        collect_offline(scorer, offline)
    else:
        collect_fresh(scorer, offline, args.output / "fresh.npz")


if __name__ == "__main__":
    main()
