"""Entropy-matched temperature for the no-memory arm, fit on pre-drift (source) tasks only.

For each procedure and its first episode input, decode greedily under the lesson prompt and
under the no-memory prompt, keep full logits along each completion, and compute mean per-token
entropy of softmax(logits / T). Target: the lesson prompt at the memory arms' T = 0.3.
Pick the T on a grid at which the no-memory prompt's mean entropy matches the target.
"""

import json
from pathlib import Path

import numpy as np

import env
import run

ROOT = Path(__file__).resolve().parent
GRID = np.round(np.arange(0.05, 2.001, 0.05), 2)


def completion_logits(m, prompt):
    text = (f"<|im_start|>system\n{run.SYSTEM}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n"
            "<|im_start|>assistant\n")
    m.reset()
    n_prompt = len(m.tokenize(text.encode(), add_bos=False, special=True))
    m(text, max_tokens=200, temperature=0.0, stop=["<|im_end|>"])
    return np.array(m.scores[n_prompt - 1:m.n_tokens - 1], dtype=np.float64)


def mean_entropy(logits, t):
    z = logits / t
    z -= z.max(1, keepdims=True)
    p = np.exp(z)
    p /= p.sum(1, keepdims=True)
    return float(np.mean(-(p * np.log(np.clip(p, 1e-30, None))).sum(1)))


def main():
    from llama_cpp import Llama
    m = Llama(model_path=str(Path.home() / "models/qwen2.5-coder-3b-instruct-q4_k_m.gguf"),
              n_ctx=4096, n_batch=512, n_threads=2, logits_all=True, verbose=False)
    docs = env.docs()
    lesson, none = [], []
    for proc in env.PROCS:
        lesson.append(completion_logits(m, run.lesson_prompt(proc, proc["lesson"], docs)))
        none.append(completion_logits(m, run.no_memory_prompt(proc, docs)))
    target = float(np.mean([mean_entropy(l, 0.3) for l in lesson]))
    curve = [float(np.mean([mean_entropy(l, t) for l in none])) for t in GRID]
    t_star = float(GRID[int(np.argmin([abs(c - target) for c in curve]))])
    out = dict(target_lesson_entropy_T0_3=target, grid=GRID.tolist(), no_memory_entropy=curve,
               fitted_T=t_star, no_memory_entropy_T0_3=float(np.mean([mean_entropy(l, 0.3) for l in none])))
    (ROOT / "temperature_fit.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("grid", "no_memory_entropy")}))


if __name__ == "__main__":
    main()
