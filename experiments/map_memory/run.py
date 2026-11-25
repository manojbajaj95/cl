"""CPU pilot: causal axis screening, then memory arms on the same local facts."""

import argparse
import json
import random
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .arms import (
    family_accuracy, name_matcher, perplexity, prepare_drift, retrieve, solved_notes, text_bytes, train_lora,
)
from .worlds import AXES, balanced_pair, causal_pairs, make_world, real_questions, solve_coordinates, split_anchors


MODELS = {
    "0.5b": ("Qwen/Qwen2.5-0.5B-Instruct", "7ae557604adf67be50417f59c2c2f167def9a775"),
    "1.5b": ("Qwen/Qwen2.5-1.5B-Instruct", "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"),
}
MIN_GAP = {"latitude": 12, "longitude": 24, "birth": 75, "atomic": 15, "mass": 0.65}
GAINS = (0.5, 1.0, 2.0, 4.0)
COMPARATIVE = {
    "north of": "farther north", "south of": "farther south",
    "east of": "farther east", "west of": "farther west",
    "born after": "born later", "born before": "born earlier",
    "a higher atomic number than": "a higher atomic number",
    "a lower atomic number than": "a lower atomic number",
    "heavier than": "heavier", "lighter than": "lighter",
}
CHAT_START = "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n"
CHAT_END = "<|im_end|>\n<|im_start|>assistant\n"
OPTIONS = {"completion": (" No", " Yes"), "chat-yes-no": ("No", "Yes"), "chat-ab": ("B", "A")}
STYLES = (*OPTIONS, "chat-name")


def question_text(axis, q, style):
    if style in ("chat-ab", "chat-name"):
        return f"Which {axis.noun_singular} {axis.statement_verb} {COMPARATIVE[axis.phrase(q.positive)]}"
    have = "have " if axis.question_verb == "Does" else ""
    return f"{axis.question_verb} {q.a} {have}{axis.phrase(q.positive)} {q.b}?"


def render_question(axis, q, style):
    question = question_text(axis, q, style)
    if style == "chat-ab":
        text = f"{question}?\nA. {q.a}\nB. {q.b}"
        a = len(question) + 5
        b = a + len(q.a) + 4
    elif style == "chat-name":
        text = f"{question}, {q.a} or {q.b}? Answer with the name only."
        a = len(question) + 2
        b = a + len(q.a) + 4
    else:
        text = f"Question: {question}"
        a = len(f"Question: {axis.question_verb} ")
        b = len(text) - len(q.b) - 1
    return text, [(a, a + len(q.a), q.a), (b, b + len(q.b), q.b)]


def prompt(axis, q, demos, facts=(), style="chat-ab", matcher=None):
    labels = {"chat-ab": "A or B", "chat-name": "the name", "chat-yes-no": "Yes or No",
              "completion": "Yes or No"}[style]
    prefix = "" if style == "completion" else CHAT_START
    prefix += f"Answer questions about {axis.noun} with {labels} only.\n\n"
    for demo in demos:
        text, _ = render_question(axis, demo, style)
        answer = (demo.a if demo.yes else demo.b) if style == "chat-name" else OPTIONS[style][demo.yes].strip()
        prefix += f"{text}\nAnswer: {answer}\n\n"
    if facts:
        prefix += "Notes:\n" + "\n".join(facts) + "\n\n"
    text, spans = render_question(axis, q, style)
    positions = [(lo + len(prefix), hi + len(prefix), name) for lo, hi, name in spans]
    if matcher is not None:
        positions.extend((m.start(), m.end(), m.group()) for m in matcher.finditer(prefix))
    suffix = "\nAnswer:" if style == "completion" else CHAT_END
    return prefix + text + suffix, positions


class Model:
    def __init__(self, model, path, batch, style):
        name, revision = MODELS[model]
        self.tokenizer = AutoTokenizer.from_pretrained(path or name, revision=revision)
        self.model = AutoModelForCausalLM.from_pretrained(
            path or name, revision=revision, dtype=torch.float32, attn_implementation="sdpa")
        self.model.requires_grad_(False).eval()
        self.decoder = self.model.model
        self.layers = self.decoder.layers
        self.batch = batch
        self.style = style
        self.options = []
        for answer in OPTIONS.get(style, ()):
            ids = self.tokenizer.encode(answer, add_special_tokens=False)
            if len(ids) != 1:
                raise ValueError(f"Answer is not one token: {answer}")
            self.options.append(ids[0])
        self.output = self.model.lm_head.weight.detach()

    def encode(self, rendered):
        texts, ranges = zip(*rendered)
        tokens = self.tokenizer(list(texts), add_special_tokens=False, return_offsets_mapping=True)
        result = []
        for text, ids, offsets, spans in zip(texts, tokens.input_ids, tokens.offset_mapping, ranges):
            positions = []
            for lo, hi, name in spans:
                assert text[lo:hi] == name
                overlapping = [i for i, (start, end) in enumerate(offsets) if start < hi and end > lo]
                tail = text[hi:offsets[overlapping[-1]][1]] if overlapping else ""
                if not overlapping or offsets[overlapping[-1]][1] < hi or tail.strip(".,?!;:\n "):
                    raise ValueError(f"Could not locate final name token for {name!r}")
                positions.append((name, overlapping[-1]))
            result.append((ids, positions))
        return result

    def encode_qs(self, axis, questions, demos, notes=None, matcher=None):
        encoded = self.encode([prompt(axis, q, demos, () if notes is None else notes[i], self.style, matcher)
                               for i, q in enumerate(questions)])
        result = []
        for q, (ids, positions) in zip(questions, encoded):
            if self.style != "chat-name":
                result.append((ids, positions, self.options))
                continue
            names = self.tokenizer([q.b, q.a], add_special_tokens=False).input_ids
            stop = self.tokenizer.eos_token_id
            first, second = [tokens + [stop] for tokens in names]
            common = next(i for i, (b, a) in enumerate(zip(first, second)) if b != a)
            result.append((ids + first[:common], positions, [first[common], second[common]]))
        return result

    def pad(self, rows):
        length = max(map(len, rows))
        ids = torch.full((len(rows), length), self.tokenizer.pad_token_id, dtype=torch.long)
        mask = torch.zeros_like(ids)
        for i, row in enumerate(rows):
            ids[i, :len(row)] = torch.tensor(row)
            mask[i, :len(row)] = 1
        return ids, mask

    @contextmanager
    def write(self, layer, operations):
        if layer is None or not operations:
            yield
            return

        row, token, vectors = zip(*operations)
        delta = torch.stack(vectors)

        def inject(_, __, out):
            out = out.clone()
            out[row, token] += delta.to(out.dtype)
            return out

        handle = self.layers[layer].register_forward_hook(inject)
        try:
            yield
        finally:
            handle.remove()

    @torch.inference_mode()
    def score(self, encoded, layer=None, writes=None):
        scores = []
        for start in range(0, len(encoded), self.batch):
            rows, positions, options = zip(*encoded[start:start + self.batch])
            ids, mask = self.pad(rows)
            ops = [(i, pos, writes[start + i][name])
                   for i, names in enumerate(positions) for name, pos in names
                   if writes is not None and name in writes[start + i]]
            with self.write(layer, ops):
                hidden = self.decoder(input_ids=ids, attention_mask=mask, use_cache=False).last_hidden_state
            last = hidden[torch.arange(len(rows)), mask.sum(1) - 1]
            scores.extend(torch.einsum("bd,bkd->bk", last, self.output[torch.tensor(options)])
                          .argmax(-1).tolist())
        return np.asarray(scores, dtype=bool)

    @torch.inference_mode()
    def read(self, names, axis, layers):
        prefix = f"{axis.noun_singular.capitalize()}: "
        rows = self.encode([(prefix + name, [(len(prefix), len(prefix + name), name)]) for name in names])
        out = {layer: [] for layer in layers}
        for start in range(0, len(rows), self.batch):
            ids, positions = zip(*rows[start:start + self.batch])
            ids, mask = self.pad(ids)
            batch = torch.arange(len(positions))
            tokens = [name[0][1] for name in positions]
            hidden = self.decoder(
                input_ids=ids, attention_mask=mask, output_hidden_states=True, use_cache=False).hidden_states
            for layer in layers:
                out[layer].append(hidden[layer + 1][batch, tokens].numpy())
        return {layer: np.concatenate(values) for layer, values in out.items()}


def measurement(predicted, answers):
    return {"correct": int((predicted == answers).sum()), "n": len(answers)}


def rate(cell):
    return cell["correct"] / cell["n"] if cell["n"] else 0


def ridge(features, target, regularization=0.1):
    average = features.mean(0)
    centered = features - average
    kernel = centered @ centered.T
    strength = regularization * np.trace(kernel) / len(kernel)
    w = centered.T @ np.linalg.solve(kernel + strength * np.eye(len(kernel)), target - target.mean())
    return w, float(target.mean() - average @ w)


def switch_score(base, changed, correct):
    return {
        "flip_given_base_correct": measurement(changed[base == correct], ~correct[base == correct]),
        "target_accuracy": measurement(changed, ~correct),
        "flip_given_base_wrong": measurement(changed[base != correct], correct[base != correct]),
        "untouched_target_accuracy": measurement(base, ~correct),
    }


def screen(net, key, seed, cases, demo_pairs, force):
    axis = AXES[key]
    train, cal, test = split_anchors(axis, seed)
    demos = real_questions(axis, train, MIN_GAP[key], seed, max_pairs=demo_pairs)[::2]
    test_qs = real_questions(axis, test, MIN_GAP[key], seed)
    test_encoded = net.encode_qs(axis, test_qs, demos)
    test_preds = net.score(test_encoded)
    base_test = measurement(test_preds, np.array([q.yes for q in test_qs]))
    result = {"base_real": base_test, "eligible": rate(base_test) >= 0.75,
              "min_real_gap": MIN_GAP[key], "train_names": train, "calibration_names": cal,
              "test_names": test}
    print(key, "real gate", base_test, "eligible", result["eligible"], flush=True)
    if not result["eligible"] and not force:
        return result, None

    layers = sorted({round((len(net.layers) - 2) * fraction)
                     for fraction in (0.12, 0.28, 0.43, 0.57, 0.71, 0.86)})
    names = train + cal + test
    reads = net.read(names, axis, layers)
    y = np.array([axis.anchors[name] for name in train])
    mean, std = y.mean(), y.std()
    z = (y - mean) / std
    cal_qs = causal_pairs(axis, cal, MIN_GAP[key], seed + 1, cases)
    test_cases = causal_pairs(axis, test, MIN_GAP[key], seed + 2, cases)
    cal_encoded = net.encode_qs(axis, [q for q, _, _ in cal_qs], demos)
    cal_y = np.array([q.yes for q, _, _ in cal_qs])
    cal_base = net.score(cal_encoded)
    trials = []
    best = None
    for layer in layers:
        w, intercept = ridge(reads[layer][:len(train)], z)
        direction = (w / (w @ w)).astype(np.float32)
        values = dict(zip(names, reads[layer] @ w + intercept))
        for gain in GAINS:
            replacement = [{source: torch.from_numpy(direction) * gain *
                            ((axis.anchors[target] - mean) / std - values[source])}
                           for _, source, target in cal_qs]
            changed = net.score(cal_encoded, layer, replacement)
            stats = switch_score(cal_base, changed, cal_y)
            trial = {"layer": layer, "gain": gain, **stats}
            trials.append(trial)
            score = (rate(stats["target_accuracy"]), rate(stats["flip_given_base_correct"]), -gain)
            if best is None or score > best[0]:
                best = (score, layer, gain, w, intercept, direction, values, trial)
    _, layer, gain, w, intercept, direction, values, chosen = best
    yc = np.array([q.yes for q, _, _ in test_cases])
    encoded = net.encode_qs(axis, [q for q, _, _ in test_cases], demos)
    untreated = net.score(encoded)
    replacement = [{source: torch.from_numpy(direction) * gain *
                    ((axis.anchors[target] - mean) / std - values[source])}
                   for _, source, target in test_cases]
    intervened = net.score(encoded, layer, replacement)
    sham = net.score(encoded, layer, [{source: -write[source]} for (_, source, _), write in
                                      zip(test_cases, replacement)])
    true_z = [(axis.anchors[name] - mean) / std for name in test]
    result.update({
        "chosen": chosen, "trials": trials,
        "causal_test": switch_score(untreated, intervened, yc),
        "causal_sham": switch_score(untreated, sham, yc),
        "probe_test_pearson": float(np.corrcoef(true_z, [values[name] for name in test])[0, 1]),
    })
    return result, (demos, test_encoded, test_preds, layer, gain, w, intercept, direction,
                    values, mean, std)


def dump(path, results):
    path.write_text(json.dumps(results, indent=2) + "\n")


def pilot(net, key, probe, entry, args, checkpoint):
    axis = AXES[key]
    demos, test_encoded, test_preds, layer, gain, w, intercept, direction, values, mean, std = probe
    entities, facts, questions, witnesses = make_world(
        axis, entry["screen"]["test_names"], args.chains, args.seed + 19, MIN_GAP[key])
    coords, steps = solve_coordinates(entities, facts, values)
    read = net.read(entities, axis, [layer])[layer] @ w + intercept
    vectors = {name: torch.from_numpy(direction * gain * (coords[name] - initial)).half()
               for name, initial in zip(entities, read)}
    budget = sum(v.numel() * v.element_size() for v in vectors.values())
    index_bytes = sum(len(name.encode("utf-8")) for name in entities)
    known_and_new = values | coords
    numeric = {name: float(10 ** (mean + std * c) if key == "mass" else mean + std * c)
               for name, c in known_and_new.items()}
    matcher = name_matcher(entities)
    all_text = [fact.text(axis) for fact in facts]
    all_bytes = text_bytes(all_text)
    solved_bytes = text_bytes([f"{name} has {axis.unit} {numeric[name]:.6f}." for name in entities])
    entry["world"] = {"entities": entities, "statements": all_text, "coordinates": numeric,
                      "nonpositive_chain_steps": int((steps <= 0).sum())}
    entry["arms"] = arms = {}
    oracle = [(known_and_new[q.a] > known_and_new[q.b]) == q.positive for q in questions]
    entry["solver_only_diagnostic"] = family_accuracy(questions, oracle)
    entry["questions"] = [dict(a=q.a, b=q.b, positive=q.positive, answer=q.yes, family=q.family)
                          for q in questions]
    unique_links = sorted({(anchor, comparator) for _, anchor, comparator in witnesses})
    link_qs = [q for a, b in unique_links for left, right in ((a, b), (b, a))
               for q in balanced_pair(left, right, axis.anchors[left] > axis.anchors[right], "known_link")]
    link_correct = net.score(net.encode_qs(axis, link_qs, demos)) == np.array([q.yes for q in link_qs])
    reliable = {link for i, link in enumerate(unique_links) if link_correct[4 * i:4 * i + 4].all()}
    supported = {frozenset((new, comparator)) for new, anchor, comparator in witnesses
                 if (anchor, comparator) in reliable}
    supported_mask = np.array([q.family == "two_hop" and frozenset((q.a, q.b)) in supported
                               for q in questions])
    entry["known_legs"] = {"individual_correct": int(link_correct.sum()), "n": len(link_qs),
                           "all_four_correct_links": len(reliable), "unique_links": len(unique_links)}
    checkpoint()

    def evaluate(arm, encoded, payload, layers=None, active=None, extra=None):
        start = time.monotonic()
        pred = net.score(encoded, layers, active)
        stats = family_accuracy(questions, pred)
        arms[arm] = {"scores": stats, "payload_bytes": payload, "predictions": pred.tolist(),
                     "two_hop_verified_leg": measurement(pred[supported_mask],
                                                         np.array([q.yes for q in questions])[supported_mask]),
                     **(extra or {})}
        checkpoint()
        print(key, arm, stats, f"payload_bytes={payload} runtime={time.monotonic() - start:.1f}s", flush=True)

    empty = net.encode_qs(axis, questions, demos)
    writes = [vectors] * len(questions)
    evaluate("no_write", empty, 0)
    evaluate("map_memory", empty, budget, layer, writes, {"name_key_bytes": index_bytes})
    retrieved = [[fact.text(axis) for fact in retrieve(q, facts)] for q in questions]
    rag = net.encode_qs(axis, questions, demos, retrieved, matcher)
    evaluate("rag_k4", rag, all_bytes)
    solved = net.encode_qs(axis, questions, demos, [solved_notes(axis, q, numeric) for q in questions])
    evaluate("solved_as_text", solved, solved_bytes)
    full = net.encode_qs(axis, questions, demos, [all_text] * len(questions))
    evaluate("full_context", full, all_bytes)
    if not args.skip_map_rag:
        evaluate("map_plus_rag", rag, budget + all_bytes, layer, writes, {"name_key_bytes": index_bytes})

    q_real = real_questions(axis, entry["screen"]["test_names"], MIN_GAP[key], args.seed)
    real_truth = np.array([q.yes for q in q_real])
    matched_real = net.score(test_encoded, layer, [vectors] * len(test_encoded))
    drift_rows = prepare_drift(net, matcher, args.wikitext, args.drift_rows)
    drift_base = perplexity(net, drift_rows)
    drift_map = perplexity(net, drift_rows, layer, vectors)
    entry["drift"] = {
        "baseline_real": entry["screen"]["base_real"],
        "real_prediction_changes": int((matched_real != test_preds).sum()),
        "map_real": measurement(matched_real, real_truth),
        "wikitext_base": drift_base, "wikitext_map": drift_map,
        "wikitext_map_delta": drift_map["perplexity"] - drift_base["perplexity"],
        "wikitext_name_matches": sum(len(ops) for _, ops in drift_rows),
    }
    checkpoint()
    print(key, "drift", entry["drift"], flush=True)
    if not args.skip_lora:
        torch.manual_seed(args.seed)
        tuned, stats = train_lora(net, all_text, budget, args.epochs, args.seed)
        evaluate("lora", empty, stats["payload_bytes"], extra=stats)
        entry["drift"]["lora_real"] = measurement(net.score(test_encoded), real_truth)
        entry["drift"]["wikitext_lora"] = perplexity(net, drift_rows)
        checkpoint()
        tuned.unload()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, default="0.5b")
    parser.add_argument("--path", help="Use a local snapshot of the selected model")
    parser.add_argument("--axes", nargs="+", choices=AXES, default=["latitude", "longitude", "birth"])
    parser.add_argument("--screen-only", action="store_true")
    parser.add_argument("--force", action="store_true", help="Run an exploratory pilot even if base accuracy is low")
    parser.add_argument("--style", choices=STYLES, default="chat-name")
    parser.add_argument("--demo-pairs", type=int, default=2)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--seed", type=int, default=41)
    parser.add_argument("--causal-cases", type=int, default=12)
    parser.add_argument("--chains", type=int, default=8)
    parser.add_argument("--skip-map-rag", action="store_true")
    parser.add_argument("--skip-lora", action="store_true")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--wikitext", help="Local WikiText-2 raw test parquet")
    parser.add_argument("--drift-rows", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed)
    random.seed(args.seed)
    started = time.monotonic()
    net = Model(args.model, args.path, args.batch, args.style)
    results = {"model": MODELS[args.model], "seed": args.seed, "chains": args.chains,
               "style": args.style, "demo_pairs": args.demo_pairs,
               "causal_cases": args.causal_cases, "axes": {}}
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def checkpoint():
        dump(args.output, results)

    for key in args.axes:
        stats, probe = screen(net, key, args.seed, args.causal_cases, args.demo_pairs, args.force)
        results["axes"][key] = entry = {"screen": stats}
        checkpoint()
        print(key, "screen", {k: stats[k] for k in
                              ("base_real", "chosen", "causal_test", "causal_sham") if k in stats},
              f"elapsed={time.monotonic() - started:.1f}s", flush=True)
        if not args.screen_only and probe is not None:
            pilot(net, key, probe, entry, args, checkpoint)


if __name__ == "__main__":
    main()
