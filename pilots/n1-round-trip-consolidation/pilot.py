import argparse
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import torch
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

from fixtures import FAMILIES, code_from, examples, make_splits, signature

SEEDS = (101, 202, 303)
MAX_NEW = 128
EPOCHS = 3
TRAIN_BATCH = 8
TRAIN_ARMS = ("round_trip", "shuffled", "environment")
WORKER = Path(__file__).with_name("worker.py")


def execute(code, **kwargs):
    try:
        run = subprocess.run(
            [sys.executable, "-I", str(WORKER)],
            input=json.dumps({"code": code, **kwargs}), capture_output=True,
            encoding="utf-8", timeout=3, env={"PATH": os.defpath},
        )
    except subprocess.TimeoutExpired:
        return None
    if not run.stderr.startswith("restricted\n"):
        raise RuntimeError(f"Worker sandbox failed: {run.stderr}")
    if run.returncode:
        return None
    try:
        return json.loads(run.stdout)
    except ValueError:
        return None


def outputs(code, cases):
    result = execute(code, inputs=[x for x, _ in cases])
    if not isinstance(result, list) or len(result) != len(cases):
        return [[False, None] for _ in cases]
    return result


def score(result, cases):
    return [int(ok and type(y) is type(expected) and y == expected)
            for (ok, y), (_, expected) in zip(result, cases)]


def helper_prompt(family, seen):
    return (
        "Infer the transformation from these examples. Implement this Python function, "
        "generalizing to other inputs of the same type. Return only complete Python code "
        "in a fenced block. Use the exact function name and return type.\n"
        f"{signature(family)}\n\n{examples(seen)}"
    )


def key(family):
    return f"task-{list(FAMILIES).index(family):02d}"


def literal(output):
    ok, value = output
    return repr(value) if ok else "<error>"


def challenges(rows, mbpp):
    return ([helper_prompt(row["family"], row["seen"]) for row in rows]
            + ["Write a complete Python solution for this task. Return only Python in a fenced "
               "block. The public assertion below gives the requested function name.\n\n"
               f"{item['prompt']}\n\n{item['test_list'][0]}" for item in mbpp])


class Pilot:
    def __init__(self, args):
        self.args = args
        torch.set_num_threads(args.threads)
        torch.set_num_interop_threads(1)
        self.tok = AutoTokenizer.from_pretrained(args.model, padding_side="left")
        self.base = AutoModelForCausalLM.from_pretrained(
            args.model, torch_dtype=torch.float32, attn_implementation="sdpa").eval()

    def chat(self, message):
        return self.tok.apply_chat_template(
            [{"role": "user", "content": message}], tokenize=False, add_generation_prompt=True)

    @torch.inference_mode()
    def generate(self, prompts, model=None, cap=MAX_NEW):
        codes = []
        token_positions = 0
        for start in range(0, len(prompts), self.args.batch):
            batch = prompts[start:start + self.args.batch]
            inputs = self.tok.pad(
                {"input_ids": batch}, padding=True, return_tensors="pt")
            prefix = inputs.input_ids.shape[1]
            sequences = (self.base if model is None else model).generate(
                **inputs, max_new_tokens=cap, do_sample=False,
                temperature=None, top_p=None, top_k=None, repetition_penalty=None,
                pad_token_id=self.tok.pad_token_id,
            )[:, prefix:]
            codes.extend(code_from(x) for x in self.tok.batch_decode(
                sequences, skip_special_tokens=True))
            token_positions += len(batch) * (prefix + sequences.shape[1] - 1)
        return codes, token_positions

    def gate(self):
        prompts = []
        cases = []
        for seed in SEEDS:
            for family in FAMILIES:
                seen, extra, held = make_splits(seed, family)
                prompts.append(self.encode(self.chat(helper_prompt(family, seen))))
                cases.append((seed, family, seen, extra, held))
        rows = []
        for start in range(0, len(prompts), self.args.batch):
            codes, _ = self.generate(prompts[start:start + self.args.batch])
            for (seed, family, seen, extra, held), code in zip(cases[start:], codes):
                seen_hits = score(outputs(code, seen), seen)
                held_hits = score(outputs(code, held), held)
                print(seed, family, sum(seen_hits), sum(held_hits), flush=True)
                rows.append(dict(seed=seed, family=family, code=code, seen=seen, extra=extra,
                                 held=held, seen_hits=seen_hits, held_hits=held_hits))
        acc = sum(sum(row["held_hits"]) for row in rows) / sum(len(row["held_hits"]) for row in rows)
        print(f"Original held-out accuracy: {acc:.4%}; headroom: {1 - acc:.4%}", flush=True)
        (self.args.out / "gate.json").write_text(json.dumps(rows, indent=2) + "\n")

    def encode(self, prompt):
        return self.tok.encode(prompt, add_special_tokens=False)

    def writing_prompts(self, rows, sources, filler=False, feedback=None):
        prompts = []
        for i, (row, source) in enumerate(zip(rows, sources)):
            family = row["family"]
            message = (
                f"Task ID: {key(family)}. Infer the task from the original examples and write "
                "a general implementation, not a lookup table. The reference below may be an "
                "old implementation to rewrite or inert padding. Return only complete Python "
                "code in a fenced block. Use the exact function name and return type.\n"
                f"{signature(family)}\n\n{examples(row['seen'])}\n\nReference:\n"
                + "<reference>"
            )
            if feedback is not None:
                message += f"\n\nPrevious attempt on the original examples:\n{feedback[i]}"
            a, b = self.chat(message).split("<reference>", 1)
            source_ids = self.encode(source)
            if filler:
                source_ids = self.encode("#") * len(source_ids)
            prompts.append(self.encode(a) + source_ids + self.encode(b))
        return prompts

    def train_sets(self, rows, seed):
        result = {arm: [] for arm in TRAIN_ARMS}
        for row in rows:
            family = row["family"]
            cases = row["seen"] + row["extra"]
            teacher = outputs(row["code"], cases)
            indices = list(range(len(teacher)))
            rng = random.Random(f"{seed}:{family}:shuffle")
            rng.shuffle(indices)
            shuffled = teacher.copy()
            for i, j in zip(indices, indices[1:] + indices[:1]):
                shuffled[i] = teacher[j]
            targets = dict(round_trip=teacher, shuffled=shuffled,
                           environment=[[True, y] for _, y in cases])
            for start in range(0, len(cases), 5):
                queries = "\n".join(repr(x) for x, _ in cases[start:start + 5])
                prompt = self.chat(f"Task ID: {key(family)}. Evaluate {signature(family)}\n"
                                   f"Return one Python literal output per input line:\n{queries}")
                prefix = self.encode(prompt)
                for arm, labels in targets.items():
                    answer = "\n".join(map(literal, labels[start:start + 5])) + "<|im_end|>"
                    suffix = self.encode(answer)
                    result[arm].append((prefix + suffix, [-100] * len(prefix) + suffix))
        return result

    def train(self, samples, orders, width, seed):
        torch.manual_seed(seed)
        adapter = get_peft_model(self.base, LoraConfig(
            task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16,
            target_modules=["q_proj", "v_proj"], lora_dropout=0))
        adapter.train()
        opt = torch.optim.AdamW((p for p in adapter.parameters() if p.requires_grad),
                                lr=0.001, weight_decay=0.0)
        losses = []
        for batch in orders:
            tokens, masks, labels = [], [], []
            for i in batch:
                ids, label = samples[i]
                pad = width - len(ids)
                tokens.append(ids + [self.tok.pad_token_id] * pad)
                masks.append([1] * len(ids) + [0] * pad)
                labels.append(label + [-100] * pad)
            labels = torch.tensor(labels)[:, 1:]
            mask = labels.ne(-100)
            result = adapter.base_model.model.model(
                input_ids=torch.tensor(tokens), attention_mask=torch.tensor(masks),
                use_cache=False).last_hidden_state
            logits = self.base.lm_head(result[:, :-1][mask])
            loss = torch.nn.functional.cross_entropy(logits, labels[mask])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            losses.append(loss.item())
        return adapter.eval(), losses

    @staticmethod
    def grade(codes, rows, split):
        return [score(outputs(code, row[split]), row[split])
                for code, row in zip(codes, rows)]

    def refine(self, rows, sources, first, budget):
        best = first.copy()
        current = first
        best_seen = list(map(sum, self.grade(best, rows, "seen")))
        spent = 0
        rounds = 0
        while True:
            feedback = [f"{code}\nMatches {n}/10 original examples."
                        for code, n in zip(current, map(sum, self.grade(current, rows, "seen")))]
            prompts = self.writing_prompts(rows, sources, feedback=feedback)
            padded = sum(len(chunk) * max(map(len, chunk)) for start in
                         range(0, len(prompts), self.args.batch)
                         if (chunk := prompts[start:start + self.args.batch]))
            cap = min(MAX_NEW, (budget - spent - padded) // len(prompts) + 1)
            if cap < 32:
                return best, spent, rounds
            current, cost = self.generate(prompts, cap=cap)
            spent += cost
            rounds += 1
            for i, n in enumerate(map(sum, self.grade(current, rows, "seen"))):
                if n >= best_seen[i]:
                    best[i], best_seen[i] = current[i], n

    def retention(self, questions, rows, mbpp, adapter=None, base_mbpp=None):
        count = len(rows)
        if base_mbpp is None:
            codes, _ = self.generate(questions, adapter, cap=160)
            scores = [int(execute(code, tests=item["test_imports"] + item["test_list"]) is True)
                      for code, item in zip(codes[count:], mbpp)]
        else:
            codes, _ = self.generate(questions[:count], adapter, cap=160)
            scores = base_mbpp
        return dict(seen=self.grade(codes[:count], rows, "seen"), mbpp=scores)

    def trial(self):
        gate = json.loads((self.args.out / "gate.json").read_text())
        headroom = 1 - sum(sum(row["held_hits"]) for row in gate) / (
            sum(len(row["held_hits"]) for row in gate))
        if headroom < 0.30:
            raise SystemExit(f"Headroom gate failed ({headroom:.2%}); no LoRA test run.")
        mbpp = sorted((x for x in json.loads(self.args.mbpp.read_text())
                       if 11 <= x["task_id"] <= 510), key=lambda x: x["task_id"])
        mbpp = sorted(random.Random(421).sample(mbpp, 50), key=lambda x: x["task_id"])
        seeds = [self.args.seed] if self.args.seed else SEEDS
        base_mbpp = None
        for seed in seeds:
            dest = self.args.out / f"seed-{seed}.json"
            if dest.exists():
                continue
            began = time.monotonic()
            rows = [row for row in gate if row["seed"] == seed]
            sources = [row["code"] for row in rows]
            print(f"{seed}: starting", flush=True)
            prompts = self.writing_prompts(rows, sources, filler=True)
            arms = {}
            codes, no_source_cost = self.generate(prompts)
            arms["no_source"] = dict(code=codes, held=self.grade(codes, rows, "held"))
            rewrite, rewrite_cost = self.generate(self.writing_prompts(rows, sources))
            arms["rewrite"] = dict(code=rewrite, held=self.grade(rewrite, rows, "held"))
            questions = [self.encode(self.chat(q)) for q in challenges(rows, mbpp)]
            retention = {"base": self.retention(questions, rows, mbpp, base_mbpp=base_mbpp)}
            base_mbpp = retention["base"]["mbpp"]
            datasets = self.train_sets(rows, seed)
            width = max(len(ids) for data in datasets.values() for ids, _ in data)
            n = len(datasets["round_trip"])
            orders = []
            rng = random.Random(seed)
            for _ in range(EPOCHS):
                indices = rng.sample(range(n), n)
                orders.extend(indices[i:i + TRAIN_BATCH] for i in range(0, n, TRAIN_BATCH))
            training_cost = 2 * width * sum(map(len, orders))
            for arm in TRAIN_ARMS:
                print(f"{seed}: training {arm} (positions {training_cost})", flush=True)
                adapter, losses = self.train(datasets[arm], orders, width, seed)
                codes, positions = self.generate(prompts, model=adapter)
                arms[arm] = dict(code=codes, held=self.grade(codes, rows, "held"),
                                 losses=losses, positions=positions)
                if arm == "round_trip":
                    retention[arm] = self.retention(questions, rows, mbpp, adapter)
                self.base = adapter.unload()
                self.base.eval()
                print(f"{seed}: {arm} loss {losses[0]:.3f} -> {losses[-1]:.3f}; held "
                      f"{sum(map(sum, arms[arm]['held']))}/384", flush=True)
            available = training_cost + arms["round_trip"]["positions"] - rewrite_cost
            best, spent, rounds = self.refine(rows, sources, rewrite, available)
            arms["rewrite_refine"] = dict(code=best, held=self.grade(best, rows, "held"))
            result = dict(seed=seed, families=[r["family"] for r in rows],
                          seen=[r["seen_hits"] for r in rows], original=[r["held_hits"] for r in rows],
                          arms=arms, retention=retention, mbpp_ids=[x["task_id"] for x in mbpp],
                          training_cost=training_cost, rewrite_cost=rewrite_cost,
                          no_source_cost=no_source_cost, refine_cost=spent, refine_rounds=rounds)
            dest.write_text(json.dumps(result, indent=2) + "\n")
            print(f"{seed}: done after {(time.monotonic() - began) / 60:.1f} min", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["gate", "trial"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--batch", type=int, default=12)
    parser.add_argument("--mbpp", type=Path)
    parser.add_argument("--seed", type=int, choices=SEEDS)
    args = parser.parse_args()
    if args.stage == "trial" and args.mbpp is None:
        parser.error("--mbpp is required for trial")
    args.out.mkdir(exist_ok=True)
    getattr(Pilot(args), args.stage)()


if __name__ == "__main__":
    main()
