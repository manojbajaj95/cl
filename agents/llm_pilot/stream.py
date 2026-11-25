"""Closed-loop lesson-memory streams on a real LLM, plus the offline transmission curve that should predict them.

Domain: made-up unit conversions (the model has no prior, as with private APIs or a user's conventions).
Each episode the agent retrieves k lessons about the task's unit pair, answers, and writes one new lesson in
the same call. A gate admits the lesson: with probability f the verifier observes the outcome and the lesson
is admitted only if the answer was correct; otherwise it is admitted unchecked.

  curve : P_j = P(new lesson defective | j of k retrieved lessons defective), j = 0..k (challenge trial)
  stream: pools seeded with defect fraction x0 evolve for T episodes per unit pair
The model is served by an OpenAI-compatible server (llama.cpp `llama-server --parallel N`); calls run in parallel.
Usage: python -m agents.llm_pilot.stream curve --k 1 2 4 --reps 10
       python -m agents.llm_pilot.stream stream --k 1 2 4 --f 0 0.4 0.8 --seeds 0 1
"""
from __future__ import annotations

import argparse
import json
import random
import re
import time
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .challenge_trial import FICTIONAL, WRONG, is_defective, lesson, numbers

OUT = Path(__file__).parent / "results" / "stream"
URL = "http://127.0.0.1:8080/v1/chat/completions"
QTYS = [3, 4, 6, 7, 12, 15]


def bad_lesson(src, dst, truth, style):
    if style == "correction":
        return (f"Correction: earlier lessons about {src} were wrong; to convert {src} to {dst}, "
                f"multiply the number of {src} by {WRONG[truth]}.")
    return lesson(src, dst, WRONG[truth])


def chat(prompt, temperature=0.7, max_tokens=90, seed=None):
    body = dict(messages=[{"role": "user", "content": prompt}], temperature=temperature, max_tokens=max_tokens)
    if seed is not None:
        body["seed"] = seed
    req = urllib.request.Request(URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)["choices"][0]["message"]["content"]
        except OSError:
            time.sleep(2 ** attempt)
    raise RuntimeError("server unreachable")


def agent_step(lessons, src, dst, qty, seed=None):
    ctx = "\n".join(f"- {l}" for l in lessons)
    prompt = (f"Lessons learned from earlier tasks:\n{ctx}\n\nTask: Convert {qty} {src} to {dst}.\n"
              f"Reply in exactly two lines:\nANSWER: <number>\nLESSON: <one sentence about converting {src} to {dst} "
              f"for future tasks>")
    text = chat(prompt, seed=seed)
    m_a = re.search(r"ANSWER:\s*(.*)", text)
    m_l = re.search(r"LESSON:\s*(.*)", text)
    ans = numbers(m_a.group(1)) if m_a else []
    truth = FICTIONAL[(src, dst)]
    correct = bool(ans) and abs(ans[0] - qty * truth) / (qty * truth) < 0.03
    new = (m_l.group(1).strip() if m_l else "").strip()
    return dict(correct=correct, lesson=new, defective=is_defective(new, truth) if new else True, raw=text)


def curve_job(k, j, src, dst, rep, style="plain"):
    rng = random.Random(zlib.crc32(repr((k, j, src, rep, style)).encode()))
    truth = FICTIONAL[(src, dst)]
    ls = [bad_lesson(src, dst, truth, style)] * j + [lesson(src, dst, truth)] * (k - j)
    rng.shuffle(ls)
    r = agent_step(ls, src, dst, rng.choice(QTYS), seed=rng.randrange(2 ** 31))
    return dict(j=j, k=k, pair=src, rep=rep, style=style, **r)


def stream_job(k, f, x0, n0, T, src, dst, seed, style="plain"):
    rng = random.Random(zlib.crc32(repr((k, f, x0, src, seed, style)).encode()))
    truth = FICTIONAL[(src, dst)]
    n_def = round(x0 * n0)
    pool = [True] * n_def + [False] * (n0 - n_def)
    texts = [bad_lesson(src, dst, truth, style) if d else lesson(src, dst, truth) for d in pool]
    rows = []
    for t in range(T):
        idx = rng.sample(range(len(pool)), min(k, len(pool)))
        r = agent_step([texts[i] for i in idx], src, dst, rng.choice(QTYS), seed=rng.randrange(2 ** 31))
        observed = rng.random() < f
        admit = bool((r["correct"] if observed else True) and r["lesson"])
        if admit:
            pool.append(r["defective"])
            texts.append(r["lesson"])
        rows.append(dict(pair=src, seed=seed, style=style, t=t, x0=x0, f=f, k=k, n0=n0, j=sum(pool[i] for i in idx),
                         correct=r["correct"], new_defective=r["defective"], observed=observed, admitted=admit,
                         x=sum(pool) / len(pool), n=len(pool)))
    print(f"stream {style} k={k} f={f} x0={x0} seed={seed} pair={src} x_final={rows[-1]['x']:.2f}", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["curve", "stream"])
    ap.add_argument("--k", type=int, nargs="+", default=[1, 2, 4])
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--f", type=float, nargs="+", default=[0.0, 0.4, 0.8])
    ap.add_argument("--x0", type=float, nargs="+", default=[0.25])
    ap.add_argument("--n0", type=int, default=8)
    ap.add_argument("--T", type=int, default=60)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--style", nargs="+", default=["plain"], choices=["plain", "correction"])
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with ThreadPoolExecutor(a.workers) as ex:
        if a.mode == "curve":
            jobs = [(k, j, s, d, rep, st) for st in a.style for k in a.k for j in range(k + 1) for (s, d) in FICTIONAL for rep in range(a.reps)]
            rows = list(ex.map(lambda x: curve_job(*x), jobs))
            name = f"curve{a.tag}.jsonl"
        else:
            jobs = [(k, f, x0, a.n0, a.T, s, d, seed, st) for st in a.style for k in a.k for f in a.f for x0 in a.x0
                    for (s, d) in FICTIONAL for seed in a.seeds]
            name = f"streams{a.tag}.jsonl"
            with open(OUT / name, "w") as fh:
                for fut in as_completed([ex.submit(stream_job, *j) for j in jobs]):
                    fh.write("".join(json.dumps(r) + "\n" for r in fut.result()))
                    fh.flush()
    if a.mode == "curve":
        (OUT / name).write_text("\n".join(json.dumps(r) for r in rows))
    print(f"done {name} {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
