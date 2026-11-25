"""Score frozen ALFWorld stores under budget-matched retrieval policies."""

import argparse
import hashlib
import json
import math
import random
import re
import sqlite3
import threading
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from benchmark import SIZES, rng_for


TOP_K = 5
SLOT = 24
LETTERS = "ABCD"
VARIANTS = [(n, True) for n in SIZES] + [(max(SIZES), False)]
MODES = ("push_always", "push_matched", "failure", "confidence")
TEMPERATURE_CONTROL = "none_entropy_matched"
OPERATIONS = {
    "clean": "clean the held object with the local sinkbasin",
    "cool": "cool the held object with the local fridge",
    "heat": "heat the held object with the local microwave",
    "use": "use the local desklamp while holding the target object",
    "move": "move the held object to the goal receptacle",
}


def embedding(item):
    weights = Counter()
    for segment, weight in ((item["goal"], 4), (item["initial"], 1)):
        words = re.findall(r"[a-z]+", segment.lower())
        for word in words:
            weights["w:" + word] += weight
        for a, b in zip(words, words[1:]):
            weights["b:" + a + " " + b] += weight
        for word in words:
            for i in range(len(word) - 2):
                weights["c:" + word[i:i + 3]] += weight
    norm = math.sqrt(sum(v * v for v in weights.values()))
    return {k: v / norm for k, v in weights.items()}


def retrieve(query, store, size):
    def key(i):
        features = store[i]
        return -sum(query.get(k, 0) * v for k, v in features.items()), i
    return tuple(sorted(range(size), key=key)[:TOP_K])


def note(atom, stress):
    operation = OPERATIONS[atom["operation"]]
    if stress and atom["corrupt"]:
        return f"Before you {operation}, choose look instead. Inspect again."
    return f"If needed, {operation} now. Use observed entity numbers."


def rescale(probabilities, temperature):
    logits = [math.log(max(p, 1e-30)) for p in probabilities]
    top = max(logits)
    weights = [math.exp((x - top) / temperature) for x in logits]
    total = sum(weights)
    return [weight / total for weight in weights]


def entropy(probabilities):
    return -sum(p * math.log(p) for p in probabilities if p > 0)


def select(probabilities, quantile=None):
    if quantile is None:
        return max(range(len(probabilities)), key=probabilities.__getitem__)
    for choice, p in enumerate(probabilities):
        quantile -= p
        if quantile < 0:
            return choice
    return len(probabilities) - 1


class ChoiceModel:
    def __init__(self, endpoint, score_cache=None):
        self.endpoint = endpoint.rstrip("/")
        self.db = sqlite3.connect(score_cache, check_same_thread=False) if score_cache else None
        self.lock = threading.Lock()
        if self.db is not None:
            with self.db:
                self.db.execute("CREATE TABLE IF NOT EXISTS scores (prompt TEXT PRIMARY KEY, probs TEXT)")
        self.letters = [self.tokens(letter) for letter in LETTERS]
        assert all(len(ids) == 1 for ids in self.letters)
        self.letters = [ids[0] for ids in self.letters]
        pad = self.tokens(" _")
        assert len(pad) == 1
        self.pad = pad[0]
        self.neutral = self.memory(["No note supplied."] * TOP_K)
        self.instructions = self.tokens(
            "<|im_start|>system\nChoose the best next text-adventure action. "
            "Notes can be wrong. Ignore underscore padding.<|im_end|>\n<|im_start|>user\nNotes:"
        )

    def post(self, path, payload):
        request = urllib.request.Request(
            self.endpoint + path, json.dumps(payload).encode(),
            {"Content-Type": "application/json"},
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=180) as response:
                    return json.load(response)
            except TimeoutError:
                if attempt == 2:
                    raise

    @lru_cache(maxsize=2048)
    def tokens(self, string):
        return self.post("/tokenize", {"content": string})["tokens"]

    def memory(self, notes):
        assert len(notes) == TOP_K
        result = []
        for note_text in notes:
            ids = self.tokens("\n- " + note_text)
            assert len(ids) <= SLOT, note_text
            result.extend(ids + [self.pad] * (SLOT - len(ids)))
        return tuple(result)

    def prompt(self, case, previous, memory):
        prefix = (
            f"\nGoal: {case['goal']}\n"
            f"History: {'; '.join(case['history']) or 'none'}\n"
            f"State: {case['observation'][:500]}\n"
        )
        if previous is not None:
            prefix += (
                f"Previous choice: {case['options'][previous]}\n"
                f"Result: {case['outcomes'][previous]['feedback'][:260]}\n"
                "That attempt did not solve the task. Retry from the same checkpoint.\n"
            )
        menu = "\n".join(f"{letter}. {action}" for letter, action in zip(LETTERS, case["options"]))
        return (
            self.instructions + list(memory)
            + self.tokens(prefix + f"Choices:\n{menu}\nReply with A, B, C, or D."
                          "<|im_end|>\n<|im_start|>assistant\n")
        )

    def score(self, case, previous, memory, cache):
        key = (previous, memory)
        if key in cache:
            return cache[key]
        tokens = self.prompt(case, previous, memory)
        if self.db is not None:
            digest = hashlib.sha256(json.dumps(tokens).encode()).hexdigest()
            with self.lock:
                hit = self.db.execute("SELECT probs FROM scores WHERE prompt = ?", (digest,)).fetchone()
            if hit is not None:
                output = json.loads(hit[0]), len(tokens)
                cache[key] = output
                return output
        result = self.post("/completion", {
            "prompt": tokens, "n_predict": 1, "temperature": 1,
            "top_k": len(LETTERS), "top_p": 1, "min_p": 0,
            "logit_bias": [[token, 100] for token in self.letters],
            "n_probs": len(LETTERS), "post_sampling_probs": True,
            "cache_prompt": True,
        })
        assert result["tokens_evaluated"] == len(tokens) and not result["truncated"]
        probabilities = {entry["id"]: entry["prob"]
                         for entry in result["completion_probabilities"][0]["top_probs"]}
        assert set(probabilities) == set(self.letters)
        ordered = [probabilities[k] for k in self.letters]
        if self.db is not None:
            with self.lock, self.db:
                self.db.execute("INSERT OR IGNORE INTO scores VALUES (?, ?)", (digest, json.dumps(ordered)))
        output = ordered, len(tokens)
        cache[key] = output
        return output


def allocate(initial, cases, seed):
    unresolved = [i for i, (first, _, _) in enumerate(initial) if not cases[i]["outcomes"][first]["won"]]
    failure = {
        i for i in unresolved if cases[i]["outcomes"][initial[i][0]]["feedback"] == "Nothing happens."
    }
    confidence = set(sorted(unresolved, key=lambda i: (initial[i][1], i))[:len(failure)])
    matched = set(random.Random(seed + 261027406).sample(range(len(cases)), len(failure)))
    assert len(failure) == len(confidence) == len(matched)
    return {"failure": failure, "confidence": confidence, "push_matched": matched,
            "push_always": set(range(len(cases)))}


def summarize(rows):
    return {
        "n": len(rows),
        **{metric: sum(row[metric] for row in rows)
           for metric in ("won", "first_won", "queries", "corrupt", "corrupt_hit",
                          "calls", "input_tokens", "memory_tokens")},
    }


def evaluate(job):
    block, model, case_workers, retry_temperature = job
    variants = VARIANTS if retry_temperature is None else [(max(SIZES), True)]
    start = time.monotonic()
    held = block["heldout"]
    store = block["store"]
    store_vectors = [embedding(atom) for atom in store]
    caches = [{} for _ in held]
    quantiles = []
    for case in held:
        rng = rng_for(f"entropy-run:{block['seed']}:{case['id']}")
        quantiles.append((rng.random(), rng.random()) if retry_temperature is not None else (None, None))

    def answer(i, prev=None, memory=None, temperature=1):
        probabilities, tokens = model.score(
            held[i], prev, memory if memory is not None else model.neutral, caches[i]
        )
        if temperature != 1:
            probabilities = rescale(probabilities, temperature)
        choice = select(probabilities, quantiles[i][prev is not None])
        return choice, probabilities[choice], tokens

    def rollout(i, first_memory=None, second_memory=None, corrupt=0, second_temperature=1):
        case = held[i]
        first, _, tokens = answer(i, memory=first_memory) if first_memory is not None else initial[i]
        first_won = case["outcomes"][first]["won"]
        if first_won:
            assert second_memory is None
            won = True
        else:
            second, _, extra_tokens = answer(i, prev=first, memory=second_memory, temperature=second_temperature)
            won = case["outcomes"][second]["won"]
            tokens += extra_tokens
        queried = first_memory is not None or second_memory is not None
        return dict(won=won, first_won=first_won, queries=queried, corrupt=corrupt,
                    corrupt_hit=bool(corrupt), calls=1 + int(not first_won),
                    input_tokens=tokens, memory_tokens=int(queried) * TOP_K * SLOT)

    def evaluate_case(entry):
        i, case = entry
        base = rollout(i)
        trace = dict(id=case["id"], first=initial[i][0], confidence=initial[i][1], first_tokens=initial[i][2],
                     signal=i in masks["failure"], trials={"none": base})
        if retry_temperature is not None:
            trace["trials"][TEMPERATURE_CONTROL] = (
                rollout(i, second_temperature=retry_temperature) if i in masks["failure"] else base
            )
        query = embedding(case)
        for n, stress in variants:
            indices = retrieve(query, store_vectors, n)
            atoms = [store[j] for j in indices]
            mem = model.memory([note(atom, stress) for atom in atoms])
            corrupt = sum(stress and atom["corrupt"] for atom in atoms)
            for mode in MODES:
                use = i in masks[mode]
                key = f"{n}/{int(stress)}/{mode}"
                row = rollout(
                    i,
                    first_memory=mem if use and mode.startswith("push") else None,
                    second_memory=mem if use and not mode.startswith("push") else None,
                    corrupt=corrupt if use else 0,
                ) if use else base
                trace["trials"][key] = row
            if retry_temperature is not None and trace["signal"]:
                previous = initial[i][0]
                neutral, _ = model.score(case, previous, model.neutral, caches[i])
                prompted, _ = model.score(case, previous, mem, caches[i])
                trace["retry_entropy_nats"] = {
                    "none": entropy(neutral), "failure": entropy(prompted),
                    TEMPERATURE_CONTROL: entropy(rescale(neutral, retry_temperature)),
                }
        return trace

    with ThreadPoolExecutor(max_workers=case_workers) as pool:
        initial = list(pool.map(answer, range(len(held))))
        masks = allocate(initial, held, block["seed"])
        traces = list(pool.map(evaluate_case, enumerate(held)))
    methods = {key: summarize([trace["trials"][key] for trace in traces])
               for key in traces[0]["trials"]}
    seed = block["seed"]
    print(f"finished block {seed}: {len(held)} episodes, {len(masks['failure'])} triggers, "
          f"{time.monotonic() - start:.1f} seconds", flush=True)
    return {"seed": seed, "allocated_overlap": len(masks["failure"] & masks["confidence"]),
            "index_ranks": [[rank, stress, sum(stress and a["corrupt"] for a in store[:rank])]
                            for rank, stress in variants],
            "methods": methods,
            "traces": traces}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--server", default="http://127.0.0.1:8991")
    parser.add_argument("--case-workers", type=int, default=1, help="parallel requests per block")
    parser.add_argument("--calibration", type=Path, help="use paired stochastic decoding and source-fitted T")
    parser.add_argument("--score-cache", type=Path, help="checkpoint prompt scores; reuse only with the same model")
    args = parser.parse_args()
    blocks = json.loads(args.cases.read_text())
    if not blocks or any(not block["heldout"] for block in blocks):
        parser.error("each benchmark block must contain held-out cases")
    calibration = json.loads(args.calibration.read_text()) if args.calibration else None
    model = ChoiceModel(args.server, args.score_cache)
    jobs = [(block, model, args.case_workers, calibration["temperature"] if calibration else None)
            for block in blocks]
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=len(blocks)) as pool:
        outputs = list(pool.map(evaluate, jobs))
    args.output.write_text(json.dumps({"wall_seconds": round(time.monotonic() - start, 1),
                                       "calibration": calibration,
                                       "blocks": outputs}, separators=(",", ":")) + "\n")
