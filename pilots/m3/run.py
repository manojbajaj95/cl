"""CPU-only context distillation of ten graded routing lessons."""

import argparse
import json
import random
import time
from pathlib import Path

import torch
from peft import LoraConfig, get_peft_model
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
SEEDS = (11, 29, 47, 65, 83)
LESSONS = tuple(zip(
    ("Amber", "Birch", "Cedar", "Dune", "Elm", "Flint", "Grove", "Hazel", "Iris", "Jade"),
    (15, 25, 35, 40, 45, 55, 60, 65, 75, 85),
))
CYCLES = 3
ARMS = ("keep", "nca")
TARGETS = tuple((100 - cutoff) / 100 for _, cutoff in LESSONS)
TRAIN_SCORES = tuple(range(0, 100, 3))
BATCH = 10
EPOCHS = 2
NCA_WEIGHT = 0.5
LORA_LAYERS = list(range(12, 24))


def select_scores(low, high, residue, fractions):
    candidates = [s for s in range(low, high) if s % 3 == residue]
    return [candidates[int(fraction * len(candidates))] for fraction in fractions]


def probes(feedback=False):
    fractions = (0.25, 0.75) if feedback else (0.10, 0.50, 0.90)
    residue = 2 if feedback else 1
    rows = []
    for i, (_, cutoff) in enumerate(LESSONS):
        scores = select_scores(0, cutoff, residue, fractions) + select_scores(cutoff, 100, residue, fractions)
        rows.extend((i, score) for score in scores)
    return rows


def contradiction_probes():
    rows = []
    for i, (_, cutoff) in enumerate(LESSONS):
        low, high = sorted((cutoff, 100 - cutoff))
        scores = select_scores(low, high, 1, (0.10, 0.50, 0.90))
        rows.extend((i, score) for score in scores)
    return rows


def examples(seed, cycle):
    rng = random.Random(seed * 100 + cycle)
    rows = []
    for i in range(len(LESSONS)):
        for low in range(0, 100, 25):
            score = rng.choice([s for s in TRAIN_SCORES if low <= s < low + 25])
            rows.append((i, score))
    rng.shuffle(rows)
    return rows


def prompt(row, cutoffs, evaluation):
    i, score = row
    queue, _ = LESSONS[i]
    note = f" For queue {queue}, review if the score is {cutoffs[i]} or higher." if cutoffs else ""
    item = (f"A {queue} item scored {score}." if evaluation
            else f"Queue: {queue}; score: {score}.")
    return [
        {"role": "system", "content": "Review an item if its score is at least 50. "
         "Queue-specific cutoffs override this default." + note},
        {"role": "user", "content": f"{item} Review it? Answer Yes or No."},
    ]


def encode(tokenizer, rows, cutoffs=None, evaluation=False):
    messages = [prompt(row, cutoffs, evaluation) for row in rows]
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    batch = tokenizer(rendered, add_special_tokens=False, padding=True, return_tensors="pt")
    return batch["input_ids"], batch["attention_mask"]


def logits(model, inputs, choice_weights):
    ids, mask = inputs
    hidden = model.model(input_ids=ids, attention_mask=mask, use_cache=False)
    return F.linear(hidden.last_hidden_state[:, -1], choice_weights)


@torch.no_grad()
def predict(model, inputs, choice_weights):
    model.eval()
    return torch.cat([
        logits(model, (ids, mask), choice_weights).softmax(-1)
        for ids, mask in zip(*(tensor.split(2 * BATCH) for tensor in inputs))
    ])


def anchored_kl(plain_log_probs, context_log_probs):
    return F.kl_div(context_log_probs, plain_log_probs.detach(), reduction="batchmean", log_target=True)


def distil(model, tokenizer, rows, cutoffs, head, rng, arm):
    privileged = encode(tokenizer, rows, cutoffs)
    teacher = predict(model, privileged, head).clamp_min(1e-12).log()
    student = encode(tokenizer, rows)
    lr = 0.00025 if arm == "low-lr" else 0.001
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=lr)
    model.train()
    for _ in range(EPOCHS):
        shuffled = torch.randperm(len(rows), generator=rng)
        for indices in shuffled.split(BATCH):
            optimizer.zero_grad(set_to_none=True)
            plain = logits(model, tuple(tensor[indices] for tensor in student), head).log_softmax(-1)
            loss = F.kl_div(teacher[indices], plain, reduction="batchmean", log_target=True)
            if arm == "nca":
                context = logits(model, tuple(tensor[indices] for tensor in privileged), head).log_softmax(-1)
                loss = loss + NCA_WEIGHT * anchored_kl(plain, context)
            loss.backward()
            optimizer.step()


def rates(rows, probabilities):
    reviews = [[[], []] for _ in LESSONS]
    for (i, score), review in zip(rows, probabilities[:, 0].tolist(), strict=True):
        reviews[i][score >= LESSONS[i][1]].append(review)
    return [
        (1 - target) * sum(below) / len(below) + target * sum(above) / len(above)
        for target, (below, above) in zip(TARGETS, reviews, strict=True)
    ]


def old_probabilities(rows, probabilities):
    return [
        (i, score, review if score >= LESSONS[i][1] else 1 - review)
        for (i, score), review in zip(rows, probabilities[:, 0].tolist(), strict=True)
    ]


def next_cutoffs(observed):
    return [
        min(100, max(0, nominal + round(100 * (rate - goal))))
        for (_, nominal), rate, goal in zip(LESSONS, observed, TARGETS, strict=True)
    ]


def run_arm(base, tokenizer, seed, arm, head, held_out, feedback, r1_probes, base_rate, context_rate, base_old):
    torch.manual_seed(seed)
    rng = torch.Generator().manual_seed(seed)
    adapter = get_peft_model(base, LoraConfig(
        r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], layers_to_transform=LORA_LAYERS,
    ))
    cutoffs = [cutoff for _, cutoff in LESSONS]
    plain = encode(tokenizer, held_out + r1_probes, evaluation=True)
    contradictory = encode(tokenizer, r1_probes, [100 - c for _, c in LESSONS], evaluation=True)
    for cycle in range(1, CYCLES + 1):
        distil(base, tokenizer, examples(seed, cycle), cutoffs, head, rng, arm)
        prompted = encode(tokenizer, held_out, cutoffs, evaluation=True)
        probabilities = predict(base, plain, head)
        weights = rates(held_out, probabilities[:len(held_out)])
        both = rates(held_out, predict(base, prompted, head))
        weights_old = old_probabilities(r1_probes, probabilities[len(held_out):])
        contradiction_old = old_probabilities(r1_probes, predict(base, contradictory, head))
        r1 = [[] for _ in LESSONS]
        for (i, score, baseline), (_, _, absorbed), (_, _, contradicted) in zip(
            base_old, weights_old, contradiction_old, strict=True
        ):
            r1[i].append({"score": score, "base_old": baseline, "weights_old": absorbed,
                          "contradiction_old": contradicted})
        yield [
            {"seed": seed, "arm": arm, "cycle": cycle, "lesson": queue,
             "cutoff": cutoff, "applied_cutoff": cutoffs[i],
             "direction": 1 if cutoff < 50 else -1,
             "target": TARGETS[i],
             "base": base_rate[i], "context": context_rate[i], "weights": weights[i],
             "both": both[i], "r1": r1[i]}
            for i, (queue, cutoff) in enumerate(LESSONS)
        ]
        if cycle < CYCLES:
            inputs = encode(tokenizer, feedback, cutoffs, evaluation=True)
            cutoffs = next_cutoffs(rates(feedback, predict(base, inputs, head)))
    adapter.unload()
    del base.peft_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model-dir", default=MODEL)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--low-lr", action="store_true", help="Run only the R1 lower-LR follow-up")
    args = parser.parse_args()
    torch.set_num_threads(args.threads)
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, revision=REVISION, padding_side="left")
    base = AutoModelForCausalLM.from_pretrained(args.model_dir, revision=REVISION, torch_dtype=torch.float32)
    start = time.monotonic()
    choice_ids = [tokenizer.encode(label, add_special_tokens=False) for label in ("Yes", "No")]
    if any(len(ids) != 1 for ids in choice_ids):
        raise ValueError(f"Expected single-token actions, got {choice_ids}")
    head = base.lm_head.weight.detach()[[ids[0] for ids in choice_ids]]
    held_out, feedback, r1_probes = probes(), probes(feedback=True), contradiction_probes()
    plain = encode(tokenizer, held_out + r1_probes, evaluation=True)
    prompted = encode(tokenizer, held_out, [c for _, c in LESSONS], evaluation=True)
    probabilities = predict(base, plain, head)
    base_rate = rates(held_out, probabilities[:len(held_out)])
    base_old = old_probabilities(r1_probes, probabilities[len(held_out):])
    context_rate = rates(held_out, predict(base, prompted, head))
    print(f"base/context measured: {time.monotonic() - start:.1f}s", flush=True)
    with args.output.open("x", encoding="utf-8") as out:
        for seed in SEEDS:
            evict = None
            for arm in ("low-lr",) if args.low_lr else ARMS:
                for cycle_rows in run_arm(base, tokenizer, seed, arm, head, held_out, feedback,
                                          r1_probes, base_rate, context_rate, base_old):
                    cycle = cycle_rows[0]["cycle"]
                    if arm == "keep" and cycle == 1:
                        evict = [row["weights"] for row in cycle_rows]
                    for i, row in enumerate(cycle_rows):
                        if evict is not None:
                            row["evict"] = evict[i]
                        print(json.dumps(row), file=out)
                    out.flush()
                    print(f"seed {seed} {arm} cycle {cycle}: {time.monotonic() - start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
