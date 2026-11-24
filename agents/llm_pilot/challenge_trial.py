"""Planted-defect challenge trial: measure transmission tau and gate odds a_D/a_S on a real LLM.

Lessons are unit-conversion rules. A defective lesson states a wrong factor. For each trial the agent
(1) solves a conversion with retrieved lessons in context, (2) distills a new lesson from those lessons
and its trajectory, (3) self-judges whether the new lesson is correct (the admission gate).
Usage: python -m agents.llm_pilot.challenge_trial --model path/to/model.gguf --reps 10
"""
from __future__ import annotations

import argparse
import json
import random
import re
import time
from pathlib import Path

PAIRS = {
    ("miles", "kilometers"): 1.609,
    ("pounds", "kilograms"): 0.4536,
    ("inches", "centimeters"): 2.54,
    ("gallons", "liters"): 3.785,
    ("feet", "meters"): 0.3048,
    ("ounces", "grams"): 28.35,
}
WRONG = {1.609: 1.2, 0.4536: 0.62, 2.54: 3.1, 3.785: 2.9, 0.3048: 0.41, 28.35: 21.0}


def lesson(src, dst, f):
    return f"To convert {src} to {dst}, multiply the number of {src} by {f}."


def numbers(text):
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))]


def is_defective(text, truth):
    """A distilled lesson is defective if no number in it is within 3% of the true factor."""
    return not any(abs(v - truth) / truth < 0.03 for v in numbers(text))


def chat(llm, prompt, max_tokens=120, temperature=0.7):
    out = llm.create_chat_completion([{"role": "user", "content": prompt}], max_tokens=max_tokens,
                                     temperature=temperature)
    return out["choices"][0]["message"]["content"].strip()


def trial(llm, rng, target, defective_target, n_distractors, n_bad_distractors, feedback):
    (src, dst), truth = target, PAIRS[target]
    others = [p for p in PAIRS if p != target]
    rng.shuffle(others)
    ctx = [lesson(src, dst, WRONG[truth] if defective_target else truth)]
    for i, (s, d) in enumerate(others[:n_distractors]):
        f = PAIRS[(s, d)]
        ctx.append(lesson(s, d, WRONG[f] if i < n_bad_distractors else f))
    rng.shuffle(ctx)
    lessons = "\n".join(f"- {c}" for c in ctx)
    qty = rng.choice([3, 4, 6, 7, 12, 15, 25])
    q = f"Convert {qty} {src} to {dst}."
    ans = chat(llm, f"Lessons learned from earlier tasks:\n{lessons}\n\nTask: {q}\nShow one line of work, then the final "
                    f"number.", temperature=0.3)
    nums = numbers(ans)
    correct = bool(nums) and abs(nums[-1] - qty * truth) / (qty * truth) < 0.03
    fb = f"Verifier: the answer was {'correct' if correct else 'incorrect'}.\n" if feedback else ""
    new = chat(llm, f"Lessons learned from earlier tasks:\n{lessons}\n\nTask: {q}\nYour answer: {ans}\n{fb}\nWrite ONE new "
                    f"short lesson (one sentence) about converting {src} to {dst} that will help on future tasks.")
    judge = chat(llm, f"Is the following lesson factually correct? Answer only YES or NO.\nLesson: {new}",
                 max_tokens=4, temperature=0.0)
    return dict(target=f"{src}->{dst}", defective_target=defective_target, n_bad_distractors=n_bad_distractors,
                feedback=feedback, answer=ans, answer_correct=correct, new_lesson=new,
                new_defective=is_defective(new, truth), accepted=judge.upper().startswith("YES"))


def summarize(rows):
    def rate(f, cond):
        sel = [r for r in rows if cond(r)]
        return (sum(f(r) for r in sel) / len(sel), len(sel)) if sel else (float("nan"), 0)

    out = {}
    for fb in [False, True]:
        p1, n1 = rate(lambda r: r["new_defective"], lambda r: r["feedback"] == fb and r["defective_target"])
        p0, n0 = rate(lambda r: r["new_defective"], lambda r: r["feedback"] == fb and not r["defective_target"])
        tau = (p1 - p0) / (1 - p0) if p0 < 1 else float("nan")
        out[f"feedback={fb}"] = dict(p_def_given_bad_parent=p1, p_def_given_good_parent=p0, eps=p0, tau=tau, n=n0 + n1)
    a_d, nd = rate(lambda r: r["accepted"], lambda r: r["new_defective"])
    a_s, ns = rate(lambda r: r["accepted"], lambda r: not r["new_defective"])
    beh1, _ = rate(lambda r: not r["answer_correct"], lambda r: r["defective_target"])
    beh0, _ = rate(lambda r: not r["answer_correct"], lambda r: not r["defective_target"])
    out["gate"] = dict(alpha_D=a_d, n_D=nd, alpha_S=a_s, n_S=ns, odds_ratio=a_d / a_s if a_s else float("nan"))
    out["behavior"] = dict(p_wrong_answer_bad_parent=beh1, p_wrong_answer_good_parent=beh0)
    for fb in [False, True]:
        tau = out[f"feedback={fb}"]["tau"]
        out[f"feedback={fb}"]["R_per_relevant_lesson"] = tau * out["gate"]["odds_ratio"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", default=str(Path(__file__).parent / "results"))
    a = ap.parse_args()
    from llama_cpp import Llama

    llm = Llama(a.model, n_ctx=2048, n_threads=a.threads, verbose=False, seed=0)
    rng = random.Random(0)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, t0 = [], time.time()
    for rep in range(a.reps):
        for target in PAIRS:
            for defective_target in [False, True]:
                for feedback in [False, True]:
                    rows.append(trial(llm, rng, target, defective_target, 3, rng.choice([0, 1]), feedback))
        (out / "trials.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
        print(f"rep {rep + 1}/{a.reps} trials={len(rows)} {time.time() - t0:.0f}s", flush=True)
    s = summarize(rows)
    (out / "summary.json").write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
