import argparse
import json
import math
from pathlib import Path
from random import Random
from time import monotonic

import pyarrow.parquet as pq
import torch
from torch import nn
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from grammar import Example, datasets, development, prompt, scratch_answer
from model import LORA_WIDTH, SLOTS, WIDTH, Reader


ARMS = ("loop_program", "loop_only", "rag", "scratchpad", "lora")
DEPTHS = (4, 8, 12)
VECTOR_CONTROLS = ("one_pass_same_vectors", "one_pass_refit_vectors")


def batches(rows, size):
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def windows(tokenizer, parquet, count, length, seed):
    rows = pq.read_table(parquet, columns=["text"]).column("text").to_pylist()
    rng = Random(seed)
    out = []
    for index in rng.sample(range(len(rows) - 12), k=len(rows) - 12):
        ids = tokenizer.encode("\n".join(rows[index:index + 12]), add_special_tokens=False)
        if len(ids) >= length:
            start = rng.randrange(len(ids) - length + 1)
            out.append(ids[start:start + length])
            if len(out) == count:
                return torch.tensor(out)
    raise ValueError(f"Not enough WikiText windows in {parquet}")


@torch.no_grad()
def lm_batch(reader, ids):
    prefix = reader.prefix(ids[:, :-1].contiguous())
    pos = (slice(None), slice(None))
    return prefix, pos, ids[:, 1:].contiguous()


def loss(reader, batch, **kwargs):
    h, pos, target = batch
    logits = reader.logits(h, pos, **kwargs)
    return F.cross_entropy(logits.flatten(0, -2), target.flatten())


def heal(reader, wiki, n_steps):
    dev = [reader.supervised(rows) for rows in batches(development(), 4)]
    ids = windows(reader.tokenizer, wiki / "train.parquet", 16, 48, 931)
    generic = [lm_batch(reader, rows) for rows in batches(ids, 2)]
    opt = torch.optim.Adam([reader.gate], lr=0.08)
    for step in range(n_steps):
        loops = DEPTHS[(step // 2) % len(DEPTHS)]
        batch = (generic if step % 2 == 0 else dev)[step // 2 % len(generic)]
        optimize(opt, loss(reader, batch, loops=loops))
        print(f"heal step={step + 1}/{n_steps} loops={loops}", flush=True)
    reader.gate.requires_grad_(False)


def optimize(opt, value):
    opt.zero_grad(set_to_none=True)
    value.backward()
    opt.step()
    return value.item()


def install(reader, demos, seed, epochs, arm, loops=4):
    rng = torch.Generator().manual_seed(seed)
    init = (nn.Parameter(torch.randn(SLOTS, WIDTH, generator=rng) * .04),) if arm == "program" else (
        nn.Parameter(torch.randn(1, LORA_WIDTH, generator=rng) * .04),
        nn.Parameter(torch.zeros(LORA_WIDTH, 1)),
    )
    opt = torch.optim.Adam(init, lr=.06 if arm == "program" else .012)
    ordered = list(demos)
    Random(seed).shuffle(ordered)
    encoded = [
        reader.supervised([(prompt(row), " " + row.answer) for row in rows])
        for rows in batches(ordered, 8)
    ]
    history = []
    for epoch in range(epochs):
        epoch_loss = []
        for i in Random(f"{seed}:{epoch}").sample(range(len(encoded)), k=len(encoded)):
            kwargs = dict(loops=loops, program=init[0]) if arm == "program" else dict(lora=init)
            epoch_loss.append(optimize(opt, loss(reader, encoded[i], **kwargs)))
        history.append(sum(epoch_loss) / len(epoch_loss))
        print(f"install seed={seed} {arm} loops={loops} epoch={epoch + 1}/{epochs} loss={history[-1]:.4f}", flush=True)
    return tuple(p.detach().half() for p in init), history


@torch.no_grad()
def evaluate(reader, demos, rows, depth, program, lora):
    predictions = {arm: [] for arm in ARMS}
    for chunk in batches(rows, 8):
        ids, positions = reader.encode([prompt(row) for row in chunk])
        h = reader.prefix(ids)
        ids, rag_pos = reader.encode([prompt(row, demos) for row in chunk])
        rag_h = reader.prefix(ids)
        logits = {
            "loop_program": reader.logits(h, positions, loops=depth, program=program),
            "loop_only": reader.logits(h, positions, loops=depth),
            "rag": reader.logits(rag_h, rag_pos),
            "lora": reader.logits(h, positions, lora=lora),
        }
        for arm, score in logits.items():
            predictions[arm].extend(reader.tokenizer.batch_decode(score.argmax(-1).unsqueeze(1)))
        predictions["scratchpad"].extend(reader.scratch([prompt(row, demos, scratch=True) for row in chunk]))
    return [{
        "source": row.source, "answer": row.answer,
        "raw": {arm: predictions[arm][i] for arm in ARMS},
        "correct": {
            arm: (scratch_answer(predictions[arm][i]) if arm == "scratchpad" else
                  predictions[arm][i].strip()) == row.answer
            for arm in ARMS
        },
    } for i, row in enumerate(rows)]


@torch.no_grad()
def perplexity(reader, generic, **kwargs):
    total, count = 0.0, 0
    for batch in generic:
        n = batch[-1].numel()
        total += loss(reader, batch, **kwargs).item() * n
        count += n
    return {"ppl": math.exp(total / count), "n_tokens": count}


def write_run(out, result):
    temp = out / "run.json.tmp"
    temp.write_text(json.dumps(result, indent=2) + "\n")
    temp.replace(out / "run.json")


def load_reader(model):
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    tokenizer.pad_token = tokenizer.eos_token
    native = AutoModelForCausalLM.from_pretrained(
        model, local_files_only=True, torch_dtype=torch.float32,
        attn_implementation="sdpa", sliding_window=None,
    )
    return Reader(native, tokenizer)


@torch.no_grad()
def vector_controls(reader, held, programs):
    for chunk in batches(held, 8):
        ids, positions = reader.encode([prompt(Example(tuple(row["source"].split()))) for row in chunk])
        h = reader.prefix(ids)
        for arm, program in zip(VECTOR_CONTROLS, programs, strict=True):
            logits = reader.logits(h, positions, program=program)
            decoded = reader.tokenizer.batch_decode(logits.argmax(-1).unsqueeze(1))
            for row, raw in zip(chunk, decoded, strict=True):
                row["raw"][arm] = raw
                row["correct"][arm] = raw.strip() == row["answer"]


def add_vector_controls(model, out):
    start = monotonic()
    result = json.loads((out / "run.json").read_text())
    config = result["config"]
    if any(set(result["seeds"].get(str(seed), {}).get("held", ())) != set(map(str, DEPTHS))
           for seed in config["seeds"]):
        raise ValueError("Complete the loop experiment before adding single-pass controls")
    torch.set_num_threads(config["threads"])
    reader = load_reader(model)
    reader.gate.requires_grad_(False)
    for seed in config["seeds"]:
        demos, _ = datasets(seed, config["n"])
        installed = torch.load(out / f"patches-{seed}.pt", weights_only=True)["program"]
        (refit,), history = install(reader, demos, seed, config["epochs"], "program", loops=1)
        torch.save(refit, out / f"refit-{seed}.pt")
        record = result["seeds"][str(seed)]
        record["one_pass_refit_loss"] = history
        for depth, rows in record["held"].items():
            vector_controls(reader, rows, (installed.float(), refit.float()))
            print(f"seed={seed} depth={depth} vector_controls=" + str({
                arm: sum(row["correct"][arm] for row in rows) for arm in VECTOR_CONTROLS
            }), flush=True)
    result["controls_seconds"] = monotonic() - start
    write_run(out, result)


def main():
    parser = argparse.ArgumentParser(description="H1: fit once at loop depth 4, test at 4, 8, 12")
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--wiki", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--seeds", type=int, nargs="+", default=[3407, 9041])
    parser.add_argument("--n", type=int, default=32, help="evaluation examples per depth and seed")
    parser.add_argument("--heal-steps", type=int, default=16)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--add-vector-controls", action="store_true")
    args = parser.parse_args()
    if args.add_vector_controls:
        add_vector_controls(args.model, args.out)
        return
    if args.wiki is None:
        parser.error("--wiki is required for the main experiment")
    if args.n < 4 or args.n % 4 or len(set(args.seeds)) != len(args.seeds) or min(args.heal_steps, args.epochs) < 1:
        parser.error("--n must be a positive multiple of four, seeds unique, and training budgets positive")

    torch.set_num_threads(args.threads)
    start = monotonic()
    args.out.mkdir(parents=True, exist_ok=True)
    reader = load_reader(args.model)
    with torch.no_grad():
        ids, pos = reader.encode(["One native pass should match.", "A shorter prompt"])
        torch.testing.assert_close(
            reader.logits(reader.prefix(ids), pos), reader.model(ids, use_cache=False).logits[pos],
            atol=2e-4, rtol=2e-4,
        )
    generic = [
        lm_batch(reader, rows)
        for rows in batches(windows(reader.tokenizer, args.wiki / "test.parquet", 16, 64, 4014), 2)
    ]
    result = {"config": {"seeds": args.seeds, "n": args.n, "heal_steps": args.heal_steps,
                         "epochs": args.epochs, "threads": args.threads},
              "ppl": {"native": perplexity(reader, generic)}, "seeds": {}}

    def save():
        result["elapsed_seconds"] = monotonic() - start
        write_run(args.out, result)

    save()
    heal(reader, args.wiki, args.heal_steps)
    torch.save(reader.gate.detach(), args.out / "gate.pt")
    gate = reader.gate.sigmoid()
    result["gate"] = {"min": gate.min().item(), "mean": gate.mean().item(), "max": gate.max().item()}
    result["ppl"]["loop_only"] = {d: perplexity(reader, generic, loops=d) for d in DEPTHS}
    print("PPL", result["ppl"], flush=True)
    save()

    for seed in args.seeds:
        demos, held = datasets(seed, args.n)
        (program,), program_loss = install(reader, demos, seed, args.epochs, "program")
        lora, lora_loss = install(reader, demos, seed, args.epochs, "lora")
        torch.save({"program": program, "lora": lora}, args.out / f"patches-{seed}.pt")
        program, lora = program.float(), tuple(p.float() for p in lora)
        output = {"program_loss": program_loss, "lora_loss": lora_loss, "ppl_on": {}, "held": {}}
        result["seeds"][seed] = output
        for depth in DEPTHS:
            output["held"][depth] = evaluate(reader, demos, held[depth], depth, program, lora)
            print(f"seed={seed} depth={depth} correct=" + str({
                arm: sum(row["correct"][arm] for row in output["held"][depth]) for arm in ARMS
            }), flush=True)
            save()
            output["ppl_on"][depth] = perplexity(reader, generic, loops=depth, program=program)
            save()


if __name__ == "__main__":
    main()
