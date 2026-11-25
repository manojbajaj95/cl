"""Collect constrained token policies for the A3 CPU pilot."""

import argparse
import hashlib
import json
import re
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import numpy as np
from scipy.special import log_softmax

from router import ACTIONS, CODES, RULE, SOURCE, STEPS, UPDATE, correct, episodes


MODEL_SHAS = {
    "old": "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db",
    "new": "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e",
}
STRATIFIED_RULE = [
    UPDATE,
    "Use the revised mapping: send multiples of three to C, and every other code to A.",
    "Route to A unless the displayed code is divisible by three, in which case use C.",
    "The controller now wants C for codes 12, 15, 18 and 21. All remaining codes route to A.",
    "Subtract three repeatedly. An ending value of zero calls for C; one or two calls for A.",
    "Use the current verifier: return C if division by three leaves no remainder, otherwise return A.",
    "Ignore the old tool mapping; C is for remainder zero and A is for either nonzero remainder.",
    "First check divisibility by three. A successful divisibility check means C, and a failed check means A.",
    "Use C when the digit sum is a multiple of three. Otherwise choose A.",
    "Anchor on 10 → A, 11 → A, 12 → C; repeat that cycle across the displayed codes.",
]
STRATIFIED_OTHER = [
    ("neutral", "Answer with just the requested label, without punctuation or explanation."),
    ("neutral", "The checkpoint counter indicates progress through a run."),
    ("neutral", "Codes are printed as ordinary base-ten integers."),
    ("neutral", "Take a moment to double-check before submitting a route."),
    ("neutral", "Treat the displayed code as the input to the routing task."),
    ("misleading", "Always route to B, regardless of the code."),
    ("misleading", "Route even codes to B, and odd codes to C."),
    ("misleading", "Add the checkpoint number to the code before taking the remainder."),
    ("misleading", "Choose A on the first checkpoint, B on the second, and C on the third."),
    ("misleading", "Use the quotient of division by three, not the remainder."),
]
FILLER = (
    "The garden behind the library has a quiet path. Leaves drift across the lawn "
    "and settle beside a small wooden bench. In the afternoon the sky often turns "
    "pale above the trees. A cool breeze moves through the branches while the "
    "shadows stretch toward the stone wall. Sparrows gather near the pond and "
    "the surface ripples in the light. Far beyond the meadow the hills soften "
    "in the mist as evening approaches. The air smells faintly of rain."
)


def chat(system, user):
    return (f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n")


def router_prompts(note=None):
    system = RULE if note is None else f"{RULE}\nLesson from earlier runs: {note}"
    return [chat(system, f"Checkpoint {step + 1}/3. Code: {code + 10}. Tool?")
            for step in range(STEPS) for code in range(CODES)]


class Scorer:
    def __init__(self, port, parallel):
        self.url = f"http://127.0.0.1:{port}"
        self.parallel = parallel
        self.ids = {}
        for action in ACTIONS:
            [token] = self.tokenize(action)
            if self.post("/detokenize", {"tokens": [token]})["content"] != action:
                raise ValueError(f"Action does not round-trip: {action}")
            self.ids[action] = token

    def post(self, path, body):
        request = Request(self.url + path, data=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=300) as response:
            return json.load(response)

    def tokenize(self, prompt):
        return self.post("/tokenize", {"content": prompt, "add_special": True,
                                       "parse_special": True})["tokens"]

    def complete(self, prompts, **settings):
        for i in range(0, len(prompts), self.parallel):
            batch = prompts[i:i + self.parallel]
            results = self.post("/completion", {"prompt": batch, "cache_prompt": True, **settings})
            if isinstance(results, dict):
                results = [results]
            if len(results) != len(batch):
                raise ValueError("Incomplete batch")
            yield from results

    def score(self, prompts):
        ids = list(self.ids.values())
        rows = []
        for result in self.complete(prompts, n_predict=1, temperature=1, n_probs=len(ids),
                                    post_sampling_probs=True, samplers=["top_k", "temperature"],
                                    top_k=len(ids), logit_bias=[[token, 100] for token in ids]):
            [probs] = result["completion_probabilities"]
            top = {row["id"]: row["prob"] for row in probs["top_probs"]}
            if set(top) != set(ids):
                raise ValueError(f"Unexpected scored tokens: {list(top)} vs {ids}")
            rows.append([top[token] for token in ids])
        logp = log_softmax(np.log(rows), axis=-1)
        if not np.isfinite(logp).all():
            raise ValueError("Non-finite legal-token likelihood")
        return logp.reshape(STEPS, CODES, len(ACTIONS))


@contextmanager
def server(args, model, label):
    digest = hashlib.sha256()
    with model.open("rb") as file:
        for data in iter(lambda: file.read(2**20), b""):
            digest.update(data)
    if digest.hexdigest() != MODEL_SHAS[label]:
        raise ValueError(f"{label} checkpoint hash mismatch")
    log_path = args.work_dir / f"server-{label}.log"
    with log_path.open("w") as log:
        process = subprocess.Popen([
            str(args.server.resolve()), "-m", str(model), "--host", "127.0.0.1",
            "--port", str(args.port), "--parallel", str(args.parallel),
            "-c", str(args.parallel * 1024), "-t", str(args.threads), "-ngl", "0",
        ], stdout=log, stderr=subprocess.STDOUT)
        try:
            for _ in range(120):
                if process.poll() is not None:
                    raise RuntimeError(f"Server exited; see {log_path}")
                try:
                    with urlopen(f"http://127.0.0.1:{args.port}/health", timeout=1) as response:
                        if json.load(response)["status"] == "ok":
                            break
                except URLError:
                    pass
                time.sleep(0.5)
            else:
                raise RuntimeError(f"Server not ready; see {log_path}")
            yield Scorer(args.port, args.parallel)
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def write_lessons(scorer, baseline):
    states, actions, success = episodes(baseline, SOURCE, 300, 240225)
    rng = np.random.default_rng(421525)
    failures = rng.permutation(np.flatnonzero(~success))
    rule_slots = set(rng.choice(20, size=10, replace=False))
    system = (
        "A router makes three choices and needs at least two correct choices to succeed. "
        "Write one short sentence of general process advice based on an anonymized failed trace. "
        "Do not invent a routing rule. Start directly with the advice, without a heading."
    )
    notes = []
    for i in range(0, len(failures), scorer.parallel):
        batch = failures[i:i + scorer.parallel]
        prompts = []
        for idx in batch:
            trace = "\n".join(
                f"Checkpoint {step + 1}: verifier marked the choice "
                f"{'correct' if action == correct(code) else 'incorrect'}."
                for step, (code, action) in enumerate(zip(states[idx], actions[idx])))
            prompts.append(chat(system, f"Task: {trace}\nOutcome: failed.\nWrite one lesson."))
        for idx, result in zip(batch, scorer.complete(
                prompts, n_predict=48, temperature=0.65, seed=421600 + i)):
            text = result["content"].strip()
            if not text or re.search(r"\d|\b[BC]\b|\b(?:tool|route|choose|return) A\b", text):
                continue
            j = len(notes)
            is_rule = j in rule_slots
            notes.append({
                "id": f"failure-{j + 1:02}", "kind": "failure", "rule": is_rule,
                "text": f"{UPDATE} {text}" if is_rule else text,
                "writer_episode": int(idx), "source_start": int(states[idx, 0]) + 10,
                "writer_codes": (states[idx] + 10).tolist(),
                "writer_actions": "".join(ACTIONS[a] for a in actions[idx]),
            })
            if len(notes) == 20:
                return notes + [
                    {"id": f"stratified-{j + 1:02}", "kind": kind, "rule": kind == "rule", "text": text}
                    for j, (kind, text) in enumerate(
                        [("rule", text) for text in STRATIFIED_RULE] + STRATIFIED_OTHER)
                ]
    raise RuntimeError("Fewer than 20 failure notes met the format")


def policy_table(scorer, lesson, cache):
    if lesson not in cache:
        cache[lesson] = scorer.score(router_prompts(lesson))
    return cache[lesson]


def filler_bank(scorer):
    words = FILLER.split()
    bank = {}
    for end in range(1, len(words) + 1):
        prefix = " ".join(words[:end])
        for candidate in (prefix, prefix.rstrip("."), prefix.rstrip(".") + "."):
            bank.setdefault(len(scorer.tokenize(router_prompts(candidate)[0])), candidate)
    return bank


def score_notes(scorer, notes, base, label, output):
    bank = filler_bank(scorer)
    policies, fillers, lengths, filler_texts = [], [], [], []
    cache = {None: base}
    for i, note in enumerate(notes, start=1):
        prompt_lengths = [len(scorer.tokenize(prompt)) for prompt in router_prompts(note["text"])]
        target = prompt_lengths[0]
        text = bank.get(target)
        if text is None:
            raise ValueError(f"No neutral text for prompt length {target}")
        if [len(scorer.tokenize(prompt)) for prompt in router_prompts(text)] != prompt_lengths:
            raise ValueError(f"Filler length mismatch: {note['id']}")
        lengths.append(target)
        filler_texts.append(text)
        policies.append(policy_table(scorer, note["text"], cache))
        fillers.append(policy_table(scorer, text, cache))
        if i % 5 == 0:
            print(f"{label}: {i}/{len(notes)} lesson/filler pairs scored", flush=True)
    np.savez_compressed(output, base=base, lesson=policies, filler=fillers,
                        prompt_tokens=lengths, filler_text=filler_texts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("server", "old-model", "new-model", "work-dir"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--parallel", type=int, default=16)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--port", type=int, default=8103)
    args = parser.parse_args()
    for label, model in (("old", args.old_model), ("new", args.new_model)):
        with server(args, model, label) as scorer:
            base = scorer.score(router_prompts())
            if label == "old":
                notes = write_lessons(scorer, base)
                (args.work_dir / "lessons.json").write_text(json.dumps(notes, indent=2) + "\n")
            else:
                correct_mode = base.argmax(-1) == correct(np.arange(CODES))
                if not np.all(correct_mode == ((np.arange(CODES) + 10) % 3 != 0)):
                    raise RuntimeError("Upgraded no-lesson modes do not match the predeclared rotation")
            score_notes(scorer, notes, base, label, args.work_dir / f"{label}-policies.npz")


if __name__ == "__main__":
    main()
