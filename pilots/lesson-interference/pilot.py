import argparse
import itertools
import json
import platform
import time
from pathlib import Path

import numpy as np
import torch
from scipy.stats import rankdata
from transformers import AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer
from transformers.cache_utils import DynamicCache

SEED = 8471
LABELS = "ABCDE"
LAYERS = (6, 12, 18, 24)
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
NLI = "cross-encoder/nli-deberta-v3-small"
NLI_REVISION = "fa2804872c3b4bd748f38c0185cc85775361e735"
FAMILIES = ("parcel", "ticket", "grain", "fiber", "invoice")
ORDINALS = ("first", "second", "third", "fourth", "fifth")
PROBE = "End of notes."
IRRELEVANT = tuple(
    f"{situation}, inspect {subject} for damage {timing}."
    for situation, subject, timing in itertools.product(
        ("At the museum", "When handling artifacts", "When receiving museum artifacts",
         "During a routine inspection of the museum's historic collection"),
        ("the crates", "the shipping boxes", "the protective packaging",
         "the protective materials surrounding the objects"),
        ("first", "before unpacking", "before putting anything into storage",
         "before taking the artifacts into the main conservation workshop"),
    )
)


def design():
    patterns = (
        "For parcel routing, send the package to the destination at the {} position in the input list.",
        "In ticket triage, assign the case to the {} team listed in the input.",
        "When grading grain, choose the bin whose label appears {} in the input.",
        "For fiber samples, report the label in slot number {} of the input list.",
        "During invoice review, scan the input left to right and return the {} label.",
    )
    lessons = [
        pattern.format(index + 1 if family == 3 else ordinal)
        for family, pattern in enumerate(patterns)
        for index, ordinal in enumerate(ORDINALS)
    ]
    rng = np.random.default_rng(SEED)
    pairs = []
    for a in range(len(lessons)):
        family, index = divmod(a, 5)
        pairs.extend((a, family * 5 + j) for j in range(5) if j != index)
        pairs.extend((a, f * 5 + int(rng.integers(5))) for f in range(5) if f != family)
    perms = np.array(list(itertools.permutations(LABELS)))
    # Five rotations of each seed list balance the correct labels at every slot.
    groups = [p for p in perms if p[0] == "A"]
    rng.shuffle(groups)
    heldout = [np.roll(p, n).tolist() for p in groups[:4] for n in range(5)]
    calibration = [np.roll(p, n).tolist() for p in groups[4:6] for n in range(5)]
    return lessons, pairs, heldout, calibration


def notes(lesson, second=None):
    return f"Lesson: {lesson}\n" + ("" if second is None else f"Lesson: {second}\n")


def prompt(a, lesson, item, second=None):
    family = FAMILIES[a // 5]
    return (
        notes(lesson, second)
        + f"Apply the {family} rule to this input. Reply with only the label.\n"
        + "Input: " + " ".join(item) + "\nAnswer:"
    )


def pair_scores(left, right):
    return (left @ left.T) * (right @ right.T)


def cosine(gram):
    norm = np.sqrt(np.diag(gram))
    return gram / np.outer(norm, norm)


class Evaluator:
    def __init__(self, source):
        revision = MODEL_REVISION if source == MODEL else None
        self.tokenizer = AutoTokenizer.from_pretrained(source, revision=revision)
        self.lm = AutoModelForCausalLM.from_pretrained(
            source, revision=revision, torch_dtype=torch.float32, attn_implementation="sdpa"
        ).eval()
        self.model = self.lm.model
        self.layers = self.model.layers
        self.pad = self.tokenizer.pad_token_id
        self.head_count = self.model.config.num_attention_heads
        self.head_dim = self.model.config.hidden_size // self.head_count
        self.aliases = []
        for label in LABELS:
            ids = [self.tokenizer.encode(prefix + label, add_special_tokens=False)
                   for prefix in ("", " ", "\n", "\t")]
            self.aliases.append(sorted({tokens[0] for tokens in ids if len(tokens) == 1}))

    def encode(self, user, assistant=False):
        return self.tokenizer.apply_chat_template(
            [{"role": "user", "content": user}], tokenize=True, add_generation_prompt=assistant
        )

    def probe_ids(self, lesson=None):
        user = PROBE if lesson is None else notes(lesson) + PROBE
        prefix = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": user}], tokenize=False, add_generation_prompt=False
        ).removesuffix("<|im_end|>\n")
        return self.tokenizer.encode(prefix, add_special_tokens=False)

    def positions(self, mask):
        return (mask.cumsum(-1) - 1).clamp_min(0)

    def pad_left(self, rows):
        width = max(map(len, rows))
        ids = torch.tensor([[self.pad] * (width - len(row)) + list(row) for row in rows])
        mask = torch.tensor([[0] * (width - len(row)) + [1] * len(row) for row in rows])
        return ids, mask

    def last(self, rows, prefix=None, repeats=1):
        ids, mask = self.pad_left(rows)
        cache = None
        positions = self.positions(mask)
        if prefix is not None:
            pre_cache, pre_mask = prefix
            keys = tuple(
                (k.repeat(repeats, 1, 1, 1), v.repeat(repeats, 1, 1, 1))
                if repeats > 1 else (k, v) for k, v in pre_cache
            )
            cache = DynamicCache.from_legacy_cache(keys)
            mask = torch.cat((pre_mask.repeat(repeats, 1), mask), dim=1)
            positions = self.positions(mask)[:, -ids.shape[1]:]
        result = self.model(ids, attention_mask=mask, position_ids=positions, past_key_values=cache,
                            use_cache=cache is not None).last_hidden_state[:, -1]
        return self.lm.lm_head(result)

    def prefix(self, rows):
        ids, mask = self.pad_left(rows)
        cache = self.model(ids, attention_mask=mask, position_ids=self.positions(mask),
                           use_cache=True).past_key_values
        return cache.to_legacy_cache(), mask

    def answer_scores(self, logits, targets):
        lse = logits.logsumexp(dim=-1)
        logp = torch.stack([logits[:, ids].logsumexp(dim=-1) - lse for ids in self.aliases], dim=1)
        target = torch.tensor([LABELS.index(label) for label in targets])
        pred = logits.argmax(dim=-1)
        correct = torch.stack([torch.isin(pred, torch.tensor(ids)) for ids in self.aliases], dim=1)
        row = torch.arange(len(targets))
        return correct[row, target].numpy(), logp[row, target].numpy()

    def condition(self, a, lesson, items, second=None):
        rows = [self.encode(prompt(a, lesson, item, second), assistant=True) for item in items]
        shared = next(i for i, tokens in enumerate(zip(*rows)) if len(set(tokens)) > 1)
        cached, mask = self.prefix([rows[0][:shared]])
        size = len(rows)
        batch_cache = tuple(
            (k.expand(size, -1, -1, -1), v.expand(size, -1, -1, -1)) for k, v in cached
        )
        logits = self.last([row[shared:] for row in rows], (batch_cache, mask.expand(size, -1)))
        return self.answer_scores(logits, [item[a % 5] for item in items])

    def control(self, a, lesson, second, items):
        reference = [len(self.encode(prompt(a, lesson, item, second), assistant=True)) for item in items]
        for candidate in IRRELEVANT:
            if len(self.encode(prompt(a, lesson, items[0], candidate), assistant=True)) != reference[0]:
                continue
            lengths = [len(self.encode(prompt(a, lesson, item, candidate), assistant=True)) for item in items]
            if lengths == reference:
                return candidate, reference[0]
        raise ValueError(f"No exact token-length control for {second!r}")

    def capture(self, rows, modules):
        captured = {}
        handles = [
            module.register_forward_pre_hook(
                lambda _, args, label=label: captured.__setitem__(label, args[0][:, -1].clone())
            )
            for label, module in modules.items()
        ]
        try:
            logits = self.last(rows)
        finally:
            for handle in handles:
                handle.remove()
        return logits, captured

    def patches(self, lessons):
        rows = [self.probe_ids(), *(self.probe_ids(lesson) for lesson in lessons)]
        assert len({row[-1] for row in rows}) == 1
        _, acts = self.capture(rows, {i: self.layers[i].mlp for i in LAYERS})
        gram = np.zeros((len(lessons), len(lessons)), dtype=np.float64)
        for i in LAYERS:
            base = acts[i][0]
            shift = (acts[i][1:] - base).to(torch.float32)
            right = (base / base.square().sum()).numpy().astype(np.float64)
            right = np.broadcast_to(right, shift.shape)
            projections = self.layers[i].mlp
            for proj in (projections.up_proj, projections.gate_proj):
                left = torch.nn.functional.linear(shift, proj.weight).numpy().astype(np.float64)
                gram += pair_scores(left, right)
        return gram

    def function_vectors(self, lessons, calibration):
        # Two disjoint calibration inputs for each rule, never from the drop evaluation.
        examples = [(a, calibration[j * 5 + (2 * a + j) % 5])
                    for a in range(len(lessons)) for j in range(2)]
        targets = [item[a % 5] for a, item in examples]
        clean = [self.encode(prompt(a, lessons[a], item), True) for a, item in examples]
        corrupt = [
            self.encode(prompt(a, lessons[(a // 5) * 5 + (a + 1) % 5], item), True)
            for a, item in examples
        ]
        outputs = {i: layer.self_attn.o_proj for i, layer in enumerate(self.layers)}
        _, clean_acts = self.capture(clean, outputs)
        cached = self.prefix([row[:-1] for row in corrupt])
        last = [row[-1:] for row in corrupt]
        _, logp = self.answer_scores(self.last(last, cached), targets)
        base = np.exp(logp)
        batch = len(examples)
        heads = self.head_count
        dim = self.head_dim
        row = torch.arange(batch * heads)
        head = torch.arange(heads).repeat_interleave(batch)
        effects = []
        for i, module in outputs.items():
            mean = clean_acts[i].reshape(len(lessons), 2, heads, dim).mean(dim=1)
            means = mean.repeat_interleave(2, dim=0).repeat(heads, 1, 1)

            def replace(_, args):
                act = args[0].clone()
                act.view(-1, heads, dim)[row, head] = means[row, head]
                return (act,)

            handle = module.register_forward_pre_hook(replace)
            try:
                _, logp = self.answer_scores(self.last(last * heads, cached, repeats=heads), targets * heads)
            finally:
                handle.remove()
            effects.extend((np.exp(logp.reshape(heads, batch)) - base).mean(axis=1).tolist())
        selected = np.argsort(-np.array(effects), kind="stable")[:10]
        acts = {i // heads: clean_acts[i // heads].reshape(len(lessons), 2, -1).mean(dim=1)
                for i in selected}
        vectors = sum(
            acts[i // heads][:, (i % heads) * dim:(i % heads + 1) * dim]
            @ outputs[i // heads].weight[:, (i % heads) * dim:(i % heads + 1) * dim].T
            for i in selected
        ).numpy().astype(np.float64)
        return cosine(vectors @ vectors.T), [
            {"layer": int(i // heads), "head": int(i % heads), "calibration_effect": effects[i]}
            for i in selected
        ]


def nli_scores(source, lessons, pairs):
    revision = NLI_REVISION if source == NLI else None
    tokenizer = AutoTokenizer.from_pretrained(source, revision=revision)
    model = AutoModelForSequenceClassification.from_pretrained(source, revision=revision).eval()
    index = next(i for i, label in model.config.id2label.items() if label.lower() == "contradiction")
    scores = []
    for offset in range(0, len(pairs), 32):
        batch = pairs[offset:offset + 32]
        tokens = tokenizer([lessons[a] for a, b in batch], [lessons[b] for a, b in batch],
                           padding=True, return_tensors="pt")
        scores.extend(model(**tokens).logits.softmax(dim=-1)[:, index].tolist())
    return scores


def safe_corr(x, y):
    x = x - x.mean()
    y = y - y.mean()
    norm = np.linalg.norm(x) * np.linalg.norm(y)
    return x @ y / norm if norm > 0 else np.nan


def metrics(rows, outcome):
    names = ("patch", "patch_cosine", "nli", "fv", "control_drop", "length")
    y = np.array([row["drop"][outcome] for row in rows])
    control = np.array([row["control_drop"][outcome] for row in rows])
    columns = np.column_stack([
        y, *([row[name] for row in rows] if name != "control_drop" else control for name in names)
    ])
    ranks = rankdata(columns, axis=0)
    result = {f"rho_{name}": safe_corr(ranks[:, 0], ranks[:, i + 1]) for i, name in enumerate(names)}
    result["rho_patch_minus_nli"] = result["rho_patch"] - result["rho_nli"]
    result["rho_patch_minus_fv"] = result["rho_patch"] - result["rho_fv"]
    design = np.column_stack((np.ones(len(rows)), ranks[:, -2:]))
    interest = ranks[:, :2]
    residual = interest - design @ np.linalg.lstsq(design, interest, rcond=None)[0]
    result["rho_patch_partial"] = safe_corr(residual[:, 0], residual[:, 1])
    result["mean_drop"] = y.mean()
    result["mean_control_drop"] = control.mean()
    result["mean_excess_drop"] = (y - control).mean()
    result["mean_baseline"] = np.mean([row["baseline"][outcome] for row in rows])
    result["dilution_share"] = control.mean() / y.mean() if y.mean() > 0 else np.nan
    return result


def summarize(rows, draws):
    rng = np.random.default_rng(SEED + 1)
    source = np.array([row["a"] for row in rows])
    partner = np.array([row["b"] for row in rows])
    lessons = np.unique(np.concatenate((source, partner)))
    boot = {"pair": [], "lesson": []}
    for _ in range(draws):
        boot["pair"].append(rng.integers(len(rows), size=len(rows)))
        # The same lesson draw weights both axes, retaining dependence across A and B roles.
        count = np.bincount(rng.choice(lessons, len(lessons)), minlength=lessons.max() + 1)
        cluster = np.repeat(np.arange(len(rows)), count[source] * count[partner])
        if len(cluster):
            boot["lesson"].append(cluster)
    summaries = {}
    for outcome in ("exact", "logp"):
        observed = metrics(rows, outcome)
        summary = {key: {"estimate": value if np.isfinite(value) else None} for key, value in observed.items()}
        for method, indices in boot.items():
            sampled = [metrics([rows[i] for i in ix], outcome) for ix in indices]
            for key, record in summary.items():
                finite = [x[key] for x in sampled if np.isfinite(x[key])]
                record[f"{method}_95ci"] = np.quantile(finite, (0.025, 0.975)).tolist() if finite else None
                record[f"{method}_valid_draws"] = len(finite)
        summaries[outcome] = summary
    return summaries


def score_dict(values):
    return {key: float(np.mean(value, dtype=np.float64)) for key, value in zip(("exact", "logp"), values)}


def subtract(a, b):
    return {"exact": round(a["exact"] - b["exact"], 12), "logp": a["logp"] - b["logp"]}


def verdict(exact):
    est = {key: value["estimate"] for key, value in exact.items()}
    criteria = {
        "patch_at_least_0.15_above_nli": est["rho_patch_minus_nli"] is not None
        and est["rho_patch_minus_nli"] >= 0.15,
        "patch_beats_fv": est["rho_patch_minus_fv"] is not None and est["rho_patch_minus_fv"] > 0,
        "positive_drop_not_mostly_dilution": est["dilution_share"] is not None and est["dilution_share"] <= 0.5,
    }
    return {"decision": "KEEP" if all(criteria.values()) else "KILL",
            "criteria": {key: bool(value) for key, value in criteria.items()}}


def analyze(result, draws):
    for row in result["pairs"]:
        row["drop"] = subtract(row["baseline"], row["paired"])
        row["control_drop"] = subtract(row["baseline"], row["dilution"])
    result["configuration"]["bootstrap_draws"] = draws
    result["summary"] = summarize(result["pairs"], draws)
    result["verdict"] = verdict(result["summary"]["exact"])
    return result


@torch.inference_mode()
def run(args):
    start = time.monotonic()
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    lessons, pairs, items, calibration = design()
    nli = nli_scores(args.nli, lessons, pairs)
    print(f"NLI complete ({time.monotonic() - start:.1f}s)", flush=True)
    evaluator = Evaluator(args.model)
    controls = [evaluator.control(a, lessons[a], lessons[b], items) for a, b in pairs]
    print(f"Model and controls ready ({time.monotonic() - start:.1f}s)", flush=True)
    gram = evaluator.patches(lessons)
    patch_cos = cosine(gram)
    fv_cos, heads = evaluator.function_vectors(lessons, calibration)
    print(f"Predictors complete ({time.monotonic() - start:.1f}s)", flush=True)
    baseline = [score_dict(evaluator.condition(a, text, items)) for a, text in enumerate(lessons)]
    null = {}
    rows = []
    result = {
        "configuration": {
            "model": MODEL, "model_revision": MODEL_REVISION, "nli": NLI, "nli_revision": NLI_REVISION,
            "cpu_threads": args.threads, "platform": platform.platform(), "dtype": "float32",
            "seed": SEED, "patch_layers_zero_based": LAYERS,
            "function_vector_heads": heads, "probe": PROBE,
        },
        "lessons": lessons, "test_items": items, "calibration_items": calibration, "pairs": rows,
    }
    for idx, ((a, b), (control, length)) in enumerate(zip(pairs, controls)):
        paired = score_dict(evaluator.condition(a, lessons[a], items, lessons[b]))
        if (a, control) not in null:
            null[a, control] = score_dict(evaluator.condition(a, lessons[a], items, control))
        rows.append({
            "a": a, "b": b, "conflict": a // 5 == b // 5, "length": length, "control": control,
            "patch": float(-gram[a, b]), "patch_cosine": float(-patch_cos[a, b]),
            "fv": float(fv_cos[a, b]), "nli": nli[idx], "baseline": baseline[a],
            "paired": paired, "dilution": null[a, control],
        })
        if (idx + 1) % 20 == 0:
            elapsed = time.monotonic() - start
            print(f"{idx + 1}/{len(pairs)} pairs ({elapsed:.1f}s)", flush=True)
    result["configuration"]["runtime_seconds"] = time.monotonic() - start
    if args.measurements:
        args.measurements.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    analyze(result, args.draws)
    result["configuration"]["runtime_seconds"] = time.monotonic() - start
    return result


def main():
    parser = argparse.ArgumentParser(description="Run the pre-specified lesson-interference CPU pilot.")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--nli", default=NLI)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--draws", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    parser.add_argument("--reanalyze", type=Path, help="Recompute statistics from saved pair measurements.")
    parser.add_argument("--measurements", type=Path, help="Also save raw pair measurements before analysis.")
    args = parser.parse_args()
    result = analyze(json.loads(args.reanalyze.read_text()), args.draws) if args.reanalyze else run(args)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"summary": result["summary"], "verdict": result["verdict"]}, indent=2))


if __name__ == "__main__":
    main()
