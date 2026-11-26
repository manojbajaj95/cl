"""Run the fixed-slot write-skew screen against a local llama.cpp server."""
import argparse
import hashlib
import json
import math
import platform
import random
import time
from functools import lru_cache
from pathlib import Path
from urllib.request import Request, urlopen

MODEL = "Qwen/Qwen2.5-0.5B-Instruct-GGUF"
REVISION = "9217f5db79a29953eb74d5343926648285ec7e67"
CHECKPOINT = "qwen2.5-0.5b-instruct-fp16.gguf"
SHA256 = "8e0ae26000627ed62de0e78e41860af70094558b9d2913385c842a6aa06cf3fc"
OLD, TARGET = "kavimer", 4
QUEUES = tuple(range(1, 7))
SYLLABLES = "ka lo vi zu mer tan po rek si dal fo gri nu bex ol quin".split()
QUESTIONS = (
    "A ticket of type '{key}' arrived. Which queue (1-6)? Reply with the number only.",
    "Which queue (1-6) handles a '{key}' ticket? Give only the queue number.",
)


def line(key, queue, active=True):
    kind = "Tickets" if active else "Notes"
    return f"- {kind} of type '{key}' go to queue {queue}."


def prompt(lines, key, wording):
    memory = "\n".join(lines)
    query = QUESTIONS[wording].format(key=key)
    return (
        "<|im_start|>system\nYou route support tickets. Use the routing memory. "
        "Only lines beginning '- Tickets' are rules; ignore Notes.<|im_end|>\n"
        f"<|im_start|>user\nRouting memory:\n{memory}\n\n{query}<|im_end|>\n"
        "<|im_start|>assistant\nQueue "
    )


class Reader:
    def __init__(self, url):
        self.url = url.removesuffix("/")
        self.ids = [self.tokens(str(q))[0] for q in QUEUES]
        cue = self.tokens("Queue ")
        if len(set(self.ids)) != 6 or any(
            self.tokens(f"Queue {q}") != cue + (i,) for q, i in zip(QUEUES, self.ids)
        ):
            raise ValueError("Queue numbers must be single tokens after the response cue")
        self.calls = 0
        self.scored_tokens = 0
        self.cached_tokens = 0

    def request(self, endpoint, data=None):
        payload = None if data is None else json.dumps(data).encode()
        request = Request(self.url + endpoint, payload, {"Content-Type": "application/json"})
        with urlopen(request, timeout=60) as response:
            return json.load(response)

    @lru_cache(maxsize=4096)
    def tokens(self, text):
        data = {"content": text, "add_special": False, "parse_special": True}
        return tuple(self.request("/tokenize", data)["tokens"])

    def score(self, tokens, bias=64, cache=True):
        out = self.request(
            "/completion",
            {"prompt": tokens, "n_predict": 1, "n_probs": 6, "top_k": 6,
             "temperature": 1, "samplers": ["top_k", "temperature"],
             "post_sampling_probs": True, "cache_prompt": cache, "seed": 0,
             "logit_bias": [[i, bias] for i in self.ids]},
        )
        top = out["completion_probabilities"][0]["top_probs"]
        probs = {item["id"]: item["prob"] for item in top}
        if probs.keys() != set(self.ids) or out["tokens_evaluated"] != len(tokens):
            raise ValueError("Unexpected candidates or prompt length")
        self.calls += 1
        self.scored_tokens += len(tokens)
        self.cached_tokens += out["timings"]["cache_n"]
        return [math.log(probs[i]) for i in self.ids]


def store(reader, seed):
    rng = random.Random(seed)
    queues = rng.sample([q for q in QUEUES if q != TARGET], 3)
    old_slot = rng.randrange(4)
    used = {OLD}
    row_length = len(reader.tokens(line(OLD, TARGET)))

    def draw(queue, active):
        for _ in range(4096):
            key = "".join(rng.choices(SYLLABLES, k=3))
            if key not in used and len(reader.tokens(line(key, queue, active))) == row_length:
                used.add(key)
                return key
        raise ValueError("Could not draw a matched-length row")

    sections = {name: [draw(q, name != "notes") for q in queues]
                for name in ("focal", "control", "notes")}
    return dict(seed=seed, old_slot=old_slot, queues=queues, **sections)


def rows(case, arm, mask):
    lines = [
        line(case[arm][i] if mask & (1 << i) else case["notes"][i], q,
             bool(mask & (1 << i)))
        for i, q in enumerate(case["queues"])
    ]
    lines.insert(case["old_slot"], line(OLD, TARGET))
    return lines


def find(tokens, part):
    hits = [i for i in range(len(tokens) - len(part) + 1)
            if tokens[i:i + len(part)] == part]
    if len(hits) != 1:
        raise ValueError("Expected one occurrence of the matched span")
    return hits[0]


def measure(reader, case, holdout):
    result = dict(case)
    result["old_reads"] = []
    result["new_reads"] = {}
    arms = ("control", "focal") if holdout else ("control",)
    pending = []
    for wording in range(len(QUESTIONS)):
        empty = reader.tokens(prompt(rows(case, "control", 0), OLD, wording))
        old_span = reader.tokens(line(OLD, TARGET))[:-1]
        query_span = reader.tokens(QUESTIONS[wording].format(key=OLD))[:-1]
        layout = (len(empty), find(empty, old_span), find(empty, query_span))
        scores = {"token_count": layout[0], "old_start": layout[1], "query_start": layout[2]}
        pending.append((empty, scores, "empty"))
        for arm in arms:
            scores[arm] = [None] * 8
            for mask in range(1, 8):
                tokens = reader.tokens(prompt(rows(case, arm, mask), OLD, wording))
                if layout != (len(tokens), find(tokens, old_span), find(tokens, query_span)):
                    raise ValueError(f"Token layout changed: {case['seed']}, {arm}, {mask}")
                pending.append((tokens, scores[arm], mask))
        result["old_reads"].append(scores)
    if holdout:
        for arm in arms:
            full = rows(case, arm, 7)
            result["new_reads"][arm] = [None] * 3
            for i, key in enumerate(case[arm]):
                tokens = reader.tokens(prompt(full, key, 0))
                pending.append((tokens, result["new_reads"][arm], i))
    for tokens, dest, index in sorted(pending, key=lambda job: job[0]):
        dest[index] = reader.score(tokens)
    for scores in result["old_reads"]:
        for arm in arms:
            scores[arm][0] = scores["empty"]
    return result


def calibration(reader):
    case = store(reader, 0)
    active = rows(case, "control", 0)
    inactive = active[:]
    inactive[case["old_slot"]] = line(OLD, TARGET, active=False)
    old = reader.tokens(prompt(active, OLD, 0))
    off = reader.tokens(prompt(inactive, OLD, 0))
    if len(old) != len(off):
        raise ValueError("Old-rule control is not token matched")
    on = reader.score(old, cache=False)
    cached = reader.score(old)
    if max(abs(a - b) for a, b in zip(on, cached)) > 1e-3:
        raise ValueError("Cached and uncached scores disagree")
    different_bias = reader.score(old, bias=80)
    if max(abs(a - b) for a, b in zip(on, different_bias)) > 1e-3:
        raise ValueError("Scoring varies with the common bias")
    return {"seed": 0, "active": on, "inactive": reader.score(off),
            "bias_80": different_bias, "token_count": len(old)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path, help="GGUF served by llama.cpp")
    parser.add_argument("--llama-commit", required=True)
    parser.add_argument("--url", default="http://127.0.0.1:8089")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("run.json"))
    args = parser.parse_args()
    digest = hashlib.sha256()
    with args.model.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != SHA256:
        parser.error("Model checksum differs from the fixed checkpoint")
    reader = Reader(args.url)
    if reader.request("/props").get("model_path", "").split("/")[-1] != args.model.name:
        parser.error("Server model path does not match --model")
    start = time.monotonic()
    result = {
        "checkpoint": dict(repo=MODEL, revision=REVISION, file=CHECKPOINT, sha256=SHA256),
        "llama_commit": args.llama_commit, "python": platform.python_version(),
        "digit_ids": reader.ids, "old": [OLD, TARGET], "questions": QUESTIONS,
        "calibration": calibration(reader), "fit": [], "holdout": [],
    }
    for group, seeds in (("fit", range(12)), ("holdout", range(100, 130))):
        for seed in seeds:
            result[group].append(measure(reader, store(reader, seed), group == "holdout"))
            print(f"{group}: {seed} ({time.monotonic() - start:.1f}s)", flush=True)
    result["wall_seconds"] = round(time.monotonic() - start, 3)
    result["scored_calls"] = reader.calls
    result["scored_prompt_tokens"] = reader.scored_tokens
    result["cached_prompt_tokens"] = reader.cached_tokens
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
