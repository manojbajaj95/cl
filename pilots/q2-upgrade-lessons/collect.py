"""Score exact constrained-token distributions with a local llama.cpp server."""

import argparse
import hashlib
import json
import os
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import numpy as np
from scipy.special import log_softmax

from tasks import ACTIONS, CODES, RULE, SOURCE, STEPS, correct, episodes


ROOT = Path(__file__).resolve().parent
OLD_SHA = "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db"
NEW_SHA = "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e"
REPLICATION_SHA = "f521a15453fd7f820e8467f4a307c99e44f5ab9cc24273d2fe67cd7cb1288f05"
RATINGS = "12345"
N_PROBE = 60
N_PACKS = 8


def chat(system, user):
    return (f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n")


class Scorer:
    def __init__(self, port, parallel):
        self.url = f"http://127.0.0.1:{port}"
        self.parallel = parallel
        self.ids = {}
        for token in ACTIONS + RATINGS:
            [token_id] = self.post("/tokenize", {"content": token})["tokens"]
            if self.post("/detokenize", {"tokens": [token_id]})["content"] != token:
                raise ValueError(f"{token!r} does not round-trip as a single token")
            self.ids[token] = token_id

    def post(self, path, body):
        request = Request(self.url + path, data=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=180) as response:
            return json.load(response)

    def complete(self, prompts, **settings):
        for i in range(0, len(prompts), self.parallel):
            batch = prompts[i:i + self.parallel]
            results = self.post("/completion", {"prompt": batch, "cache_prompt": True, **settings})
            if isinstance(results, dict):
                results = [results]
            if len(results) != len(batch):
                raise ValueError("Incomplete batch")
            yield from results

    def score(self, prompts, legal):
        ids = [self.ids[key] for key in legal]
        rows = []
        for result in self.complete(prompts, n_predict=1, temperature=1, n_probs=len(ids),
                                    post_sampling_probs=True, samplers=["top_k", "temperature"],
                                    top_k=len(ids),
                                    logit_bias=[[token, 100] for token in ids]):
            [probs] = result["completion_probabilities"]
            top = {row["id"]: row["prob"] for row in probs["top_probs"]}
            if set(top) != set(ids):
                raise ValueError(f"Unexpected scored token IDs: {list(top)} vs {ids}")
            rows.append([top[token] for token in ids])
        result = log_softmax(np.log(rows), axis=-1)
        if not np.isfinite(result).all():
            raise ValueError("Non-finite legal-token likelihood")
        return result


@contextmanager
def server(args, model, sha, label):
    with model.open("rb") as file:
        digest = hashlib.sha256()
        for data in iter(lambda: file.read(2**20), b""):
            digest.update(data)
    if digest.hexdigest() != sha:
        raise ValueError(f"{label} checkpoint hash mismatch")
    log_path = args.server_log_dir / f"q2-server-{label}.log"
    with log_path.open("w") as log:
        process = subprocess.Popen([
            str(args.server.resolve()), "-m", str(model), "--host", "127.0.0.1",
            "--port", str(args.port), "--parallel", str(args.parallel),
            "-c", str(args.parallel * 1024), "-t", str(args.threads),
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


def policy_scores(scorer, notes, label):
    rows = []
    for note in notes:
        system = RULE if note is None else f"{RULE}\nLesson from earlier runs: {note}"
        prompts = router_prompts(system)
        scores = scorer.score(prompts, ACTIONS).reshape(STEPS, CODES, len(ACTIONS))
        rows.append(scores)
        if len(rows) % 5 == 0 or len(rows) == len(notes):
            print(f"{label}: {len(rows)}/{len(notes)} policy tables scored", flush=True)
    return np.array(rows)


def router_prompts(system):
    return [chat(system, f"Checkpoint {step + 1}/3. Code: {code + 10}. Tool?")
            for step in range(STEPS) for code in range(CODES)]


def pruning_check(scorer, notes, predictor):
    rng = np.random.default_rng(7731)
    packs = np.stack([rng.choice(len(notes), size=5, replace=False) for _ in range(N_PACKS)])
    prompts = []
    lengths = []

    def token_count(prompt):
        return len(scorer.post("/tokenize", {"content": prompt})["tokens"])

    for pack in packs:
        memory = "\n".join(f"Note {slot}: {notes[i]}" for slot, i in enumerate(pack, start=1))
        original = router_prompts(f"{RULE}\nLessons from earlier runs:\n{memory}")
        kept = [notes[i] if predictor[i] > 0 else "" for i in pack]
        slots = "\n".join(f"Note {slot}: {note}" for slot, note in enumerate(kept, start=1))
        system = f"{RULE}\nLessons from earlier runs:\n{slots}"
        target = token_count(original[0])
        pad = target - token_count(router_prompts(system)[0])
        if pad < 0:
            raise ValueError("Pruned context unexpectedly exceeds the reload-all context")
        for size in range(max(0, pad - 3), pad + 4):
            pruned = router_prompts(system + ("\n" + " _" * size if size else ""))
            if token_count(pruned[0]) == target:
                break
        else:
            raise ValueError("Could not match context token count for the pruning check")
        prompts.extend((original, pruned))
        lengths.append(target)
    policy = [scorer.score(batch, ACTIONS) for batch in prompts]
    return {"packs": packs, "tokens": np.array(lengths),
            "policy": np.array(policy).reshape(N_PACKS, 2, STEPS, CODES, len(ACTIONS))}


def write_lessons(scorer, baseline):
    log = episodes(baseline, 300, 240225)
    rng = np.random.default_rng(421525)
    failures = rng.choice(np.flatnonzero(~log["success"]), size=20, replace=False)
    system = (f"{RULE}\nWrite one short sentence of actionable advice from the failed run. "
              "Start directly with the advice, without a title or heading.")
    prompts = []
    for idx in failures:
        trace = "\n".join(
            f"Checkpoint {step + 1}: code {code + 10}, chose {ACTIONS[action]}, "
            f"verifier route {ACTIONS[correct(code)]}."
            for step, (code, action) in enumerate(zip(log["states"][idx], log["actions"][idx])))
        prompts.append(chat(system, f"Task: {trace}\nOutcome: failed.\nWrite one lesson."))
    texts = [result["content"].strip() for result in scorer.complete(
        prompts, n_predict=64, temperature=0)]
    if not all(texts):
        raise ValueError("Writer emitted an empty lesson")
    lessons = [{"id": f"m1-{i + 1:02}", "kind": "m1", "note": note,
                "source": [int(log["states"][idx, 0])], "writer_episode": int(idx)}
               for i, (idx, note) in enumerate(zip(failures, texts))]
    g1 = json.loads((ROOT / "g1_lessons.json").read_text())
    for j, (kind, count) in enumerate((("helpful", 7), ("neutral", 7), ("misleading", 6))):
        for idx in sorted(rng.choice(np.arange(10 * j, 10 * j + 10), size=count, replace=False)):
            lessons.append({"id": f"g1-{idx + 1:02}", "kind": kind, "note": g1[idx], "source": list(SOURCE)})
    return lessons, log


def judge_scores(scorer, lessons, log):
    counts = np.zeros((STEPS, CODES, len(ACTIONS), 2), dtype=int)
    for step in range(STEPS):
        np.add.at(counts[step], (log["states"][:, step], log["actions"][:, step], log["success"].astype(int)), 1)
    summary = "\n".join(f"{step + 1}/{code + 10}: " + " ".join(f"{s}/{f}" for f, s in counts[step, code])
                        for step in range(STEPS) for code in range(CODES) if counts[step, code].any())
    system = (
        "Judge how much adding this lesson would improve success for yourself on new router runs. "
        f"Task: {RULE}\n"
        "Probe logs below: checkpoint/code and successful/failed episode counts "
        "for each of A, B and C, in that order.\n" + summary
    )
    prompts = [chat(system, f"Lesson: {lesson['note']}\nRate expected effect: "
                    "1 (large harm), 2 (harm), 3 (neutral), 4 (help), 5 (large help). "
                    "Output only the rating.") for lesson in lessons]
    return scorer.score(prompts, RATINGS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "truth", "source", "replicate", "prune"))
    parser.add_argument("--server", type=Path, required=True)
    parser.add_argument("--old-model", type=Path)
    parser.add_argument("--new-model", type=Path)
    parser.add_argument("--replication-model", type=Path)
    parser.add_argument("--port", type=int, default=18085)
    parser.add_argument("--parallel", type=int, default=12)
    parser.add_argument("--threads", type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--server-log-dir", type=Path, default=Path.home())
    parser.add_argument("--output", type=Path, default=ROOT)
    args = parser.parse_args()
    if args.phase == "prepare":
        if args.old_model is None:
            parser.error("--old-model required for prepare")
        with server(args, args.old_model, OLD_SHA, "writer") as scorer:
            [baseline] = policy_scores(scorer, [None], "writer")
            lessons, log = write_lessons(scorer, baseline)
        np.savez_compressed(args.output / "writer.npz", old_base=baseline, **log)
        (args.output / "lessons.json").write_text(json.dumps(lessons, indent=2, ensure_ascii=False) + "\n")
        print(f"Frozen {len(lessons)} lessons ({len({l['note'] for l in lessons})} distinct texts)")
        return
    elif args.new_model is None and args.phase != "replicate":
        parser.error("--new-model required for truth and source")

    from analysis import gains_on_successful_actions, truth_gate

    lessons = json.loads((args.output / "lessons.json").read_text())
    notes = [lesson["note"] for lesson in lessons]
    if args.phase == "truth":
        with server(args, args.new_model, NEW_SHA, "new-truth") as scorer:
            scores = policy_scores(scorer, [None, *notes], "truth")
        np.savez_compressed(args.output / "truth.npz", new=scores)
        print(json.dumps(truth_gate(lessons, scores)[0], indent=2, allow_nan=False))
    else:
        if args.phase == "source" and args.old_model is None:
            parser.error("--old-model required for source")
        with np.load(args.output / "truth.npz") as truth:
            new = truth["new"]
        gate, _ = truth_gate(lessons, new)
        if not gate["passes"]:
            parser.exit(2, "Truth reliability gate did not pass; stopping before source scoring.\n")
        if args.phase == "replicate":
            if args.replication_model is None:
                parser.error("--replication-model required for replicate")
            return replicate(args, notes)
        if args.phase == "prune":
            with np.load(args.output / "source.npz") as source:
                predictor = gains_on_successful_actions(new, source["old_states"], source["old_actions"])
            with server(args, args.new_model, NEW_SHA, "prune") as scorer:
                pruning = pruning_check(scorer, notes, predictor)
            np.savez_compressed(args.output / "pruning.npz", **pruning)
            return
        with np.load(args.output / "writer.npz") as data:
            baseline = data["old_base"]
        with server(args, args.old_model, OLD_SHA, "old-source") as scorer:
            old = np.concatenate(([baseline], policy_scores(scorer, notes, "old-source")))
        old_log = episodes(old[0], N_PROBE, 512025)
        new_log = episodes(new[0], N_PROBE, 1512025)
        with server(args, args.new_model, NEW_SHA, "judge") as scorer:
            judge = judge_scores(scorer, lessons, new_log)
        np.savez_compressed(args.output / "source.npz", old=old, judge=judge,
                            **{f"old_{k}": v for k, v in old_log.items()},
                            **{f"new_{k}": v for k, v in new_log.items()})


def replicate(args, notes):
    with server(args, args.replication_model, REPLICATION_SHA, "replicate") as scorer:
        old = policy_scores(scorer, [None, *notes], "replicate")
    log = episodes(old[0], N_PROBE, 512025)
    np.savez_compressed(args.output / "replication.npz", old=old, **{f"old_{k}": v for k, v in log.items()})


if __name__ == "__main__":
    main()
