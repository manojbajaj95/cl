import argparse
import json
import math
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


LAYERS = (4, 5)
HORIZON = 1920
SHORT_HORIZON = 768
CHECKPOINT = 32
PREFIX = HORIZON // 10
CALIBRATION = range(3)
EVALUATION = range(3, 9)
BATCHES = (8, 32)
SEEDS = range(CALIBRATION.start, EVALUATION.stop)


def read_data(path, tokenizer):
    facts = []
    subjects = set()
    rows = json.loads(path.read_text())
    order = np.random.default_rng(20261124).permutation(len(rows))
    for idx in order:
        row = rows[idx]["requested_rewrite"]
        subject = row["subject"]
        if subject.casefold() in subjects:
            continue
        left, right = row["prompt"].split("{}")
        encoded = tokenizer(left + subject + right, return_offsets_mapping=True)
        lookup = max(i for i, (a, b) in enumerate(encoded.offset_mapping)
                     if a < len(left + subject) and b > len(left))
        new = tokenizer.encode(" " + row["target_new"]["str"].strip())
        old = tokenizer.encode(" " + row["target_true"]["str"].strip())
        if not new or not old or new == old:
            continue
        facts.append((encoded.input_ids, lookup, new, old, tokenizer.encode(subject + " is a")))
        subjects.add(subject.casefold())
    required = 2048 + 128 + len(SEEDS) * HORIZON
    if len(facts) < required:
        raise ValueError(f"Need {required} eligible unique subjects, got {len(facts)}")
    remaining = facts[2176:]
    append_at = len(SEEDS) * SHORT_HORIZON
    return facts[:2048], facts[2048:2176], [
        remaining[seed * SHORT_HORIZON:(seed + 1) * SHORT_HORIZON]
        + remaining[append_at + seed * (HORIZON - SHORT_HORIZON):
                    append_at + (seed + 1) * (HORIZON - SHORT_HORIZON)]
        for seed in SEEDS
    ]


def pad(rows):
    out = torch.zeros((len(rows), max(map(len, rows))), dtype=torch.long)
    for i, row in enumerate(rows):
        out[i, :len(row)] = torch.as_tensor(row)
    return out


def prediction_positions(prompts, completions):
    rows, positions, tokens = [], [], []
    for i, (prompt, completion) in enumerate(zip(prompts, completions)):
        for j, token in enumerate(completion):
            rows.append(i)
            positions.append(len(prompt) - 1 + j)
            tokens.append(token)
    return tuple(torch.tensor(v) for v in (rows, positions, tokens))


def ridge_dual(cholesky, keys):
    whitened = torch.cholesky_solve(keys, cholesky)
    return torch.linalg.solve(
        torch.eye(keys.shape[1]) + keys.T @ whitened, whitened.T
    ).T


def participation_rank(keys):
    centered = keys.double() - keys.double().mean(dim=0)
    gram = centered @ centered.T
    return (gram.trace().square() / gram.square().sum()).item()


class Editor:
    def __init__(self, model_path):
        self.model = AutoModelForCausalLM.from_pretrained(model_path).eval().requires_grad_(False)
        self.body = self.model.transformer
        self.projections = [self.body.h[i].mlp.c_proj for i in LAYERS]
        self.original = [p.weight.clone() for p in self.projections]
        self.original_norm = self.norm()

    def blocks(self, hidden, start, stop):
        for i in range(start, stop):
            hidden = self.body.h[i](hidden, use_cache=False)[0]
        return hidden

    def prefix(self, ids, stop):
        positions = torch.arange(ids.shape[1])
        return self.blocks(self.body.wte(ids) + self.body.wpe(positions), 0, stop)

    def logits(self, hidden):
        return self.model.lm_head(self.body.ln_f(hidden))

    @torch.no_grad()
    def reset(self):
        for projection, original in zip(self.projections, self.original):
            projection.weight.copy_(original)

    def norm(self):
        return math.sqrt(sum(p.weight.square().sum().item() for p in self.projections))

    @torch.no_grad()
    def keys_and_values(self, facts, all_tokens=False):
        ids = pad([f[0] for f in facts])
        rows = torch.arange(len(facts))
        lookup = torch.tensor([f[1] for f in facts])
        mask = torch.arange(ids.shape[1]) < torch.tensor([len(f[0]) for f in facts])[:, None]
        keys = []
        hooks = [p.register_forward_pre_hook(
            lambda module, args: keys.append(args[0][mask] if all_tokens else args[0][rows, lookup])
        ) for p in self.projections]
        try:
            values = self.prefix(ids, LAYERS[-1] + 1)[rows, lookup]
        finally:
            for hook in hooks:
                hook.remove()
        return keys, values

    def prepare_background(self, facts):
        width = self.projections[0].weight.shape[0]
        sums = [torch.zeros((width, width), dtype=torch.float64) for _ in LAYERS]
        count = 0
        for i in range(0, len(facts), 32):
            keys, _ = self.keys_and_values(facts[i:i + 32], all_tokens=True)
            count += len(keys[0])
            for total, key in zip(sums, keys):
                key = key.double()
                total.addmm_(key.T, key)
        self.cholesky = []
        for total in sums:
            moment = total / count
            moment.diagonal().add_(0.01 * moment.diagonal().mean())
            self.cholesky.append(torch.linalg.cholesky(256 * moment))

    def capacity(self, facts):
        chunks = [self.keys_and_values(facts[i:i + 32])[0] for i in range(0, len(facts), 32)]
        return [participation_rank(torch.cat(part)) for part in zip(*chunks)]

    def targets(self, facts):
        prompts, lookups, new, _, kl_prompts = zip(*facts)
        b = len(facts)
        ids = pad([p + t[:-1] for p, t in zip(prompts, new)] + list(kl_prompts))
        rows = torch.arange(2 * b)
        lookup = torch.tensor([*lookups, *(len(p) - 3 for p in kl_prompts)])
        # The final two tokens of the KL prompt are " is a"; use the final subject token.
        answer_rows, positions, labels = prediction_positions(prompts, new)
        with torch.no_grad():
            initial = self.prefix(ids, LAYERS[-1] + 1)
            original = initial[rows[:b], lookup[:b]]
            scale = original.norm(dim=1).clamp_min(1e-8)
        delta = torch.zeros_like(original, requires_grad=True)
        optimizer = torch.optim.Adam([delta], lr=0.5)
        reference = None
        for _ in range(8):
            latent = initial.clone()
            latent[rows, lookup] += delta.repeat(2, 1)
            hidden = self.blocks(latent, LAYERS[-1] + 1, len(self.body.h))
            answer_logits = self.logits(hidden[answer_rows, positions])
            kl_logits = self.logits(hidden[rows[b:], lookup[b:]]).log_softmax(dim=-1)
            if reference is None:
                reference = kl_logits.detach()
            nll = F.cross_entropy(answer_logits, labels, reduction="none")
            counts = torch.tensor([len(t) for t in new])
            loss = (nll / counts[answer_rows]).sum() / b
            loss = loss + 0.0625 * F.kl_div(reference, kl_logits, log_target=True, reduction="batchmean")
            loss = loss + 0.5 * (delta.norm(dim=1) / scale.square()).mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                delta.mul_((0.75 * scale / delta.norm(dim=1).clamp_min(1e-8)).clamp(max=1)[:, None])
        return original + delta.detach()

    def edit(self, facts):
        target = self.targets(facts)
        with torch.no_grad():
            for i, (projection, chol) in enumerate(zip(self.projections, self.cholesky)):
                keys, values = self.keys_and_values(facts)
                dual = ridge_dual(chol, keys[i].T.double())
                residual = (target - values) / (len(LAYERS) - i)
                projection.weight.add_((dual @ residual.double()).float())

    @torch.no_grad()
    def completion_nll(self, facts, target):
        output = []
        for i in range(0, len(facts), CHECKPOINT):
            group = facts[i:i + CHECKPOINT]
            prompts = [f[0] for f in group]
            completions = [f[target] for f in group]
            rows, positions, labels = prediction_positions(prompts, completions)
            ids = pad([p + t[:-1] for p, t in zip(prompts, completions)])
            hidden = self.prefix(ids, len(self.body.h))
            losses = F.cross_entropy(self.logits(hidden[rows, positions]), labels, reduction="none")
            means = torch.zeros(len(group)).index_add_(0, rows, losses)
            output.extend((means / torch.tensor(list(map(len, completions)))).tolist())
        return np.asarray(output)

    def efficacy(self, facts):
        return float(np.mean(self.completion_nll(facts, 2) < self.completion_nll(facts, 3)))


def sustained_crossing(checkpoints):
    for (count, first), (_, second) in zip(checkpoints, checkpoints[1:]):
        if min(first, second) >= math.log(2):
            return count
    return None


def norm_prediction(norms, threshold):
    prefix = np.asarray([[n, y] for n, y in norms if 0 < n <= PREFIX])
    x, y = prefix.T
    slope = (x @ y) / (x @ x)
    return float(threshold / slope) if slope > 0 and threshold > 0 else None


def write_json(path, obj):
    temp = path.with_suffix(".pending")
    temp.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")
    temp.replace(path)


def run(editor, facts, probes, seed, batch, out, fit):
    path = out / f"seed{seed}-batch{batch}.json"
    if path.exists():
        print(f"Already completed seed={seed} batch={batch}", flush=True)
        return
    editor.reset()
    ranks = editor.capacity(facts)
    capacity = fit["constant"] * np.mean(ranks) if fit else None
    forecast = dict(seed=seed, batch=batch, ranks=ranks, capacity=capacity)
    write_json(path.with_suffix(".forecast.json"), forecast)
    print(f"START {forecast}", flush=True)
    base_nll = editor.completion_nll(probes, 3).mean()
    base_efficacy = editor.efficacy(facts[:CHECKPOINT])
    checkpoints, norms, step_efficacy = [], [], None
    for i in range(0, HORIZON, batch):
        count = i + batch
        editor.edit(facts[i:count])
        relative = math.log(editor.norm() / editor.original_norm)
        if not math.isfinite(relative):
            raise ValueError(f"Non-finite edited norm at {count} facts")
        norms.append([count, relative])
        if count == (PREFIX // batch) * batch and fit:
            prefix_prediction = norm_prediction(norms, fit["threshold"])
            write_json(path.with_suffix(".norm.json"), {"norm_prediction": prefix_prediction})
        if count % CHECKPOINT == 0:
            drift = float(editor.completion_nll(probes, 3).mean() - base_nll)
            checkpoints.append([count, drift])
            if count == CHECKPOINT:
                step_efficacy = editor.efficacy(facts[:CHECKPOINT])
            if count % 128 == 0:
                print(f"  {count:3}: delta NLL {drift:+.3f}; log norm {relative:+.3f}", flush=True)
        if count >= PREFIX and sustained_crossing(checkpoints) is not None:
            break
    collapse = sustained_crossing(checkpoints)
    prediction = norm_prediction(norms, fit["threshold"]) if fit else None
    record = dict(**forecast, norms=norms, checkpoints=checkpoints, collapse=collapse,
                  base_efficacy=base_efficacy, initial_efficacy=step_efficacy,
                  norm_prediction=prediction)
    write_json(path, record)
    print(f"END seed={seed} batch={batch}: collapse={collapse}, "
          f"initial efficacy {base_efficacy:.3f}->{step_efficacy:.3f}, norm forecast={prediction}", flush=True)


def is_valid(record):
    return (
        record["initial_efficacy"] >= 0.70
        and record["initial_efficacy"] - record["base_efficacy"] >= 0.15
        and (record["collapse"] is None or record["collapse"] > PREFIX)
    )


def calibrate(out):
    records = [json.loads((out / f"seed{s}-batch16.json").read_text()) for s in CALIBRATION]
    usable = [r for r in records if r["collapse"] is not None and is_valid(r)]
    if len(usable) < 2:
        return None
    return dict(
        constant=float(np.median([r["collapse"] / np.mean(r["ranks"]) for r in usable])),
        threshold=float(np.median([dict(r["norms"])[r["collapse"]] for r in usable])),
    )


def summarize(out):
    records = {}
    for path in sorted(out.glob("seed*-batch*.json")):
        if path.name.count(".") != 1:
            continue
        r = json.loads(path.read_text())
        records[r["seed"], r["batch"]] = r
        print(r["seed"], r["batch"], "observed", r["collapse"], "valid", is_valid(r),
              "capacity", r["capacity"], "norm", r["norm_prediction"])
    matched = []
    for seed in EVALUATION:
        block = [records.get((seed, b)) for b in BATCHES]
        if not all(r and is_valid(r) and r["capacity"] is not None for r in block):
            continue
        matched.append(block)
    def stats(blocks, restricted):
        actual = np.asarray([[r["collapse"] or HORIZON for r in block] for block in blocks])
        predicted = np.asarray([
            [[r["capacity"], r["norm_prediction"] or math.inf] for r in block] for block in blocks
        ])
        if restricted:
            predicted = predicted.clip(1, HORIZON)
        errors = np.abs(np.log(predicted.clip(min=1)) - np.log(actual[:, :, None]))
        print("Mean errors by size (capacity, norm):", errors.mean(axis=0))
        if not np.isfinite(errors).all():
            print("At least one control predicts no crossing; unrestricted finite CI unavailable.")
            return False
        delta = errors[:, :, 0] - errors[:, :, 1]
        inds = np.random.default_rng(0).integers(len(delta), size=(10_000, len(delta)))
        resampled = delta[inds].mean(axis=1)
        pooled_ci = np.quantile(resampled.mean(axis=1), [0.025, 0.975])
        print("Per-size paired difference:", delta.mean(axis=0),
              "95% CI:", np.quantile(resampled, [0.025, 0.975], axis=0).T)
        print("Pooled paired difference:", delta.mean(), "95% CI:", pooled_ci)
        return pooled_ci[1] < 0 and np.all(delta.mean(axis=0) < 0)

    observed = [block for block in matched if all(r["collapse"] is not None for r in block)]
    all_calibration = all(
        (r := records.get((s, 16))) and is_valid(r) and r["collapse"] is not None
        for s in CALIBRATION
    )
    win = False
    if len(observed) >= 2:
        print(f"Observed-only comparison ({len(observed)} matched seeds):")
        win = stats(observed, restricted=False)
    if len(matched) >= 2 and len(observed) != len(matched):
        print(f"Restricted-to-budget comparison ({len(matched)} matched seeds; descriptive):")
        stats(matched, restricted=True)
    print("KEEP" if all_calibration and len(observed) == len(EVALUATION) and win else "KILL for GPU escalation")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--phase", choices=("calibrate", "evaluate", "summary"), required=True)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--seed", type=int, choices=SEEDS)
    args = parser.parse_args()
    if args.phase == "summary":
        summarize(args.out)
        return
    if args.data is None:
        parser.error("--data is required for calibration/evaluation")
    args.out.mkdir(parents=True, exist_ok=True)
    fit = calibrate(args.out) if args.phase == "evaluate" else None
    print(f"Phase {args.phase}; calibration fit={fit}", flush=True)
    torch.set_num_threads(args.threads)
    tokenizer = AutoTokenizer.from_pretrained(args.data / "gpt2", local_files_only=True)
    background, probes, streams = read_data(args.data / "counterfact.json", tokenizer)
    editor = Editor(args.data / "gpt2")
    editor.prepare_background(background)
    seeds = CALIBRATION if args.phase == "calibrate" else EVALUATION
    if args.seed is not None and args.seed not in seeds:
        parser.error("--seed must belong to the selected phase")
    for seed in seeds if args.seed is None else [args.seed]:
        for batch in (16,) if args.phase == "calibrate" else BATCHES:
            run(editor, streams[seed], probes, seed, batch, args.out, fit)


if __name__ == "__main__":
    main()
