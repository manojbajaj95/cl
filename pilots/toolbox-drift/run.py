"""Run one arm x seed of the toolbox-vs-lessons drift stream and log JSONL."""

import argparse
import hashlib
import json
import random
import re
import signal
import time
from pathlib import Path

import env

ROOT = Path(__file__).resolve().parent
ARMS = ["tool", "tool+tests", "lesson", "lesson+tests"]
N_EPISODES = 180
DRIFT_AT = 60
N_DRIFT = 6  # 30% of 20 APIs: 3 breaking (documented rename) + 3 silent (undocumented semantics)
FEEDBACK_P = 0.2
REPAIR_ATTEMPTS_TESTS = 2
SYSTEM = "You are a careful Python agent. You maintain a personal library of procedures."


def schedule(seed):
    rng = random.Random(seed)
    drifted = rng.sample(env.API_NAMES, N_DRIFT)
    drift = {a: ("breaking" if i < N_DRIFT // 2 else "silent") for i, a in enumerate(drifted)}
    stream = []
    for t in range(N_EPISODES):
        p = rng.randrange(len(env.PROCS))
        x = rng.choice(env.PROCS[p]["episode_inputs"])
        stream.append((p, x, rng.random()))
    return drift, stream


class LLM:
    def __init__(self, path, threads):
        from llama_cpp import Llama
        self.m = Llama(model_path=str(path), n_ctx=4096, n_batch=512, n_threads=threads,
                       n_threads_batch=threads, verbose=False)
        self.calls = 0
        self.tokens = 0

    def __call__(self, user, seed, max_tokens=320, temperature=0.3):
        prompt = (f"<|im_start|>system\n{SYSTEM}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n"
                  "<|im_start|>assistant\n")
        out = self.m(prompt, max_tokens=max_tokens, temperature=temperature, top_p=0.95,
                     seed=seed, stop=["<|im_end|>"])
        self.calls += 1
        self.tokens += out["usage"]["total_tokens"]
        return out["choices"][0]["text"]


def extract_code(text):
    m = re.search(r"```(?:python)?\n(.*?)(```|$)", text, re.S)
    code = m.group(1) if m else text
    i = code.find("def proc")
    return code[i:] if i >= 0 else code


def extract_lesson(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S).strip()
    return text.strip().strip('"')[:1200]


class Timeout(Exception):
    pass


def _alarm(*_):
    raise Timeout("call took longer than 2 s")


def build(code):
    ns = {}
    exec(compile(code, "<proc>", "exec"), ns)
    if not callable(ns.get("proc")):
        raise NameError("no function named proc")
    return ns["proc"]


def call(fn, api, x):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(2)
    try:
        return fn(api, **x)
    finally:
        signal.alarm(0)


def describe_inputs(x):
    return ", ".join(f"{k}={v!r}" for k, v in x.items())


def signature(proc):
    return "def proc(api, " + ", ".join(proc["inputs"][0]) + "):"


def goal(proc):
    return proc["lesson"].split(":")[0]


class Agent:
    def __init__(self, arm, llm, seed):
        self.arm, self.llm, self.seed = arm, llm, seed
        self.code_arm = arm.startswith("tool")
        self.tests = arm.endswith("+tests")
        self.memory = [p["tool"] if self.code_arm else p["lesson"] for p in env.PROCS]

    def implement(self, p, artifact, docs, seed):
        """Return (code, fn or None, error message or None)."""
        proc = env.PROCS[p]
        if self.code_arm:
            code = artifact
        else:
            user = (f"API, called through the `api` object:\n{docs}\n\nSaved lesson:\n{artifact}\n\n"
                    f"Follow the lesson. Write the Python function `{signature(proc)}` that "
                    "returns the result. Use only the `api` object, no imports. Output only the code.")
            code = extract_code(self.llm(user, seed))
        try:
            return code, build(code), None
        except Exception as e:
            return code, None, f"{type(e).__name__}: {e}"

    def run_tests(self, p, fn, api):
        proc = env.PROCS[p]
        for x in proc["tests"]:
            want = env.expected(proc, x)
            try:
                got = call(fn, api, x)
            except Exception as e:
                return f"regression test proc({describe_inputs(x)}) raised {type(e).__name__}: {e}"
            if not env.correct(got, want):
                return f"regression test proc({describe_inputs(x)}) expected {want!r} but got {got!r}"
        return None

    def repair(self, p, code_used, message, api, docs, seed):
        proc = env.PROCS[p]
        old = self.memory[p]
        attempts = REPAIR_ATTEMPTS_TESTS if self.tests else 1
        log = []
        for k in range(attempts):
            if self.code_arm:
                user = (f"API, called through the `api` object:\n{docs}\n\nYour saved tool for: {goal(proc)}.\n"
                        f"```python\n{self.memory[p] if k == 0 else cand}```\nProblem: {message}\n\n"
                        f"Rewrite the tool so it is correct for the current API. Keep the signature "
                        f"`{signature(proc)}` and use only the `api` object, no imports. Output only the code.")
                cand = extract_code(self.llm(user, seed + 7 * k + 1))
            else:
                user = (f"API, called through the `api` object:\n{docs}\n\nYour saved lesson for: {goal(proc)}.\n"
                        f"Lesson: {old if k == 0 else cand}\n\nCode you wrote from it:\n```python\n{code_used}```\n"
                        f"Problem: {message}\n\nRewrite the lesson so that following it gives correct results "
                        "with the current API. Keep it a short plain-English procedure that names the API call, "
                        "the field and the computation. Output only the new lesson text, no code.")
                cand = extract_lesson(self.llm(user, seed + 7 * k + 1, max_tokens=200))
            if not self.tests:
                self.memory[p] = cand
                log.append({"attempt": k, "verified": None})
                return log
            code, fn, err = self.implement(p, cand, docs, seed + 7 * k + 3) if not self.code_arm else (cand, None, None)
            if self.code_arm:
                try:
                    fn = build(cand)
                except Exception as e:
                    err = f"{type(e).__name__}: {e}"
            fail = err or self.run_tests(p, fn, api)
            log.append({"attempt": k, "verified": fail is None})
            self.memory[p] = cand
            if fail is None:
                return log
            message, code_used = fail, code
        return log

    def episode(self, t, p, x, u, api, docs):
        proc = env.PROCS[p]
        seed = self.seed * 1_000_000 + t * 100
        artifact = self.memory[p]
        code, fn, err = self.implement(p, artifact, docs, seed)
        out = None
        if fn is not None:
            try:
                out = call(fn, api, x)
            except Exception as e:
                err = f"proc({describe_inputs(x)}) raised {type(e).__name__}: {e}"
        want = env.expected(proc, x)
        ok = err is None and env.correct(out, want)
        signals, message = [], None
        if err:
            signals.append("error")
            message = err
        if self.tests:
            tmsg = err if fn is None else self.run_tests(p, fn, api)
            if tmsg:
                signals.append("test")
                message = message or tmsg
        if not err and not ok and u < FEEDBACK_P:
            signals.append("feedback")
            message = message or f"user reported a wrong result for proc({describe_inputs(x)}): expected {want!r} but got {out!r}"
        rec = {"t": t, "proc": p, "api": proc["api"], "ok": ok, "error": err is not None,
               "out": repr(out)[:80], "want": repr(want), "signals": signals,
               "artifact": hashlib.sha1(artifact.encode()).hexdigest()[:8]}
        if signals:
            rec["repair"] = self.repair(p, code, message, api, docs, seed)
        return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=ARMS, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--model", default=str(Path.home() / "models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"))
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--episodes", type=int, default=N_EPISODES)
    ap.add_argument("--out", default=str(ROOT / "runs"))
    a = ap.parse_args()
    drift, stream = schedule(a.seed)
    llm = LLM(a.model, a.threads)
    agent = Agent(a.arm, llm, a.seed)
    out = Path(a.out)
    out.mkdir(exist_ok=True)
    path = out / f"{a.arm.replace('+', '_')}_s{a.seed}.jsonl"
    start = time.time()
    with path.open("w") as f:
        f.write(json.dumps({"meta": True, "arm": a.arm, "seed": a.seed, "drift": drift,
                            "drift_at": DRIFT_AT, "model": Path(a.model).name}) + "\n")
        for t, (p, x, u) in enumerate(stream[:a.episodes]):
            d = drift if t >= DRIFT_AT else {}
            api, docs = env.Api(d), env.docs(d)
            rec = agent.episode(t, p, x, u, api, docs)
            rec["drift"] = drift.get(env.PROCS[p]["api"]) if t >= DRIFT_AT else None
            rec["llm_calls"], rec["sec"] = llm.calls, round(time.time() - start, 1)
            f.write(json.dumps(rec) + "\n")
            f.flush()
        f.write(json.dumps({"final": True, "memory": agent.memory, "llm_calls": llm.calls,
                            "tokens": llm.tokens, "sec": round(time.time() - start, 1)}) + "\n")


if __name__ == "__main__":
    main()
