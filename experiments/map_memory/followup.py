"""Separate the coordinate fit from the entity-token write channel."""

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from .arms import family_accuracy
from .run import MIN_GAP, MODELS, Model, dump, rate, ridge, switch_score
from .worlds import AXES, balanced_pair, causal_pairs, make_world, real_questions, solve_coordinates, split_anchors


def oracle_coordinates(entities, facts, anchors):
    """Define latent truth by equally spaced log mass between the true endpoints."""
    known_lows, known_highs = {}, {}
    for fact in facts:
        high, low = (fact.a, fact.b) if fact.positive else (fact.b, fact.a)
        if low in anchors:
            known_lows[high] = anchors[low]
        elif high in anchors:
            known_highs[low] = anchors[high]
    truth = {}
    for start in range(0, len(entities), 4):
        chain = entities[start:start + 4]
        low, high = known_lows[chain[0]], known_highs[chain[-1]]
        truth.update({name: low + (high - low) * i / (len(chain) + 1)
                      for i, name in enumerate(chain, 1)})
    return truth


def direct_questions(facts):
    return [q for fact in facts for q in balanced_pair(fact.a, fact.b, fact.positive, "stated")]


def strength_trials(layer, gain):
    original = ((layer,), gain)
    single = [((layer,), value) for value in (6.0, 8.0, 12.0, 16.0)]
    multi = [(blocks, value) for blocks in ((layer - 2, layer, layer + 2), (layer, layer + 1, layer + 2))
             for value in (1.0, 2.0, 4.0, 8.0)]
    return [original, *single, *multi]


def select_on_real(trials):
    return max(trials, key=lambda trial: (
        rate(trial["calibration"]["target_accuracy"]), rate(trial["calibration"]["flip_given_base_correct"]),
        -trial["gain_per_layer"],
    ))


def fit_vectors(net, block, entities, encoded, answers, epochs, seed):
    """Optimize only 32 vectors; every row is used by exact entity name."""
    vector_table = torch.nn.Parameter(torch.zeros(len(entities), net.model.config.hidden_size))
    optimizer = torch.optim.AdamW([vector_table], lr=0.03, weight_decay=0)
    rng = np.random.default_rng(seed)
    history = []
    for _ in range(epochs):
        order = rng.permutation(len(encoded))
        loss_sum, correct = 0.0, 0
        for start in range(0, len(order), net.batch):
            rows = order[start:start + net.batch]
            vectors = dict(zip(entities, vector_table.unbind()))
            logits = net.batch_logits([encoded[i] for i in rows], block, [vectors] * len(rows))
            target = answers[rows]
            loss = F.cross_entropy(logits, target)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            loss_sum += loss.item() * len(rows)
            correct += int((logits.detach().argmax(-1) == target).sum())
        record = {"loss": loss_sum / len(encoded), "online_correct": correct, "n": len(encoded)}
        history.append(record)
        print("variant_b epoch", len(history), record, flush=True)
    return dict(zip(entities, vector_table.detach().half().unbind())), history


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=Path(__file__).with_name("mass-qwen15.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--path", help="Use a local snapshot of Qwen2.5-1.5B-Instruct")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--batch", type=int, default=16)
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error("--epochs must be positive")
    torch.set_num_threads(args.threads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    reference = json.loads(args.reference.read_text())
    if tuple(reference["model"]) != MODELS["1.5b"]:
        raise ValueError("The reference must use the pinned Qwen2.5-1.5B-Instruct model")
    baseline = reference["axes"]["mass"]
    seed = reference["seed"]
    torch.manual_seed(seed)
    net = Model("1.5b", args.path, args.batch, reference["style"])
    axis, gap = AXES["mass"], MIN_GAP["mass"]
    train, cal, test = split_anchors(axis, seed)
    entities, facts, questions, _ = make_world(axis, test, reference["chains"], seed + 19, gap)
    records = [dict(a=q.a, b=q.b, positive=q.positive, answer=q.yes, family=q.family) for q in questions]
    if records != baseline["questions"] or [fact.text(axis) for fact in facts] != baseline["world"]["statements"]:
        raise ValueError("The regenerated statements and questions must match the original world exactly")
    layer, gain = (baseline["screen"]["chosen"][key] for key in ("layer", "gain"))
    demos = real_questions(axis, train, gap, seed, max_pairs=reference["demo_pairs"])[::2]
    names = train + cal + test + entities
    reads = net.read(names, axis, [layer])[layer]
    y = np.array([axis.anchors[name] for name in train])
    mean, std = y.mean(), y.std()
    w, intercept = ridge(reads[:len(train)], (y - mean) / std)
    direction = torch.tensor(w / (w @ w), dtype=torch.float32)
    estimated = dict(zip(names, reads @ w + intercept))

    trials, arms = [], {}
    report = {"model": reference["model"], "seed": seed, "epochs": args.epochs,
              "trials": trials, "arms": arms}

    def checkpoint():
        dump(args.output, report)

    def prepare_causal(split, offset):
        cases = causal_pairs(axis, split, gap, seed + offset, reference["causal_cases"])
        encoded = net.encode_qs(axis, [q for q, _, _ in cases], demos)
        truth = np.array([q.yes for q, _, _ in cases], dtype=bool)
        deltas = [(source, direction * ((axis.anchors[target] - mean) / std - estimated[source]))
                  for _, source, target in cases]
        return encoded, net.score(encoded), truth, deltas

    def causal(blocks, strength, inputs):
        encoded, base, truth, deltas = inputs
        pred = net.score(encoded, blocks, [{source: v * strength} for source, v in deltas])
        return switch_score(base, pred, truth)

    cal_inputs = prepare_causal(cal, 1)
    test_inputs = prepare_causal(test, 2)
    for blocks, strength in strength_trials(layer, gain):
        record = {"layers": blocks, "gain_per_layer": strength,
                  "calibration": causal(blocks, strength, cal_inputs),
                  "held_out": causal(blocks, strength, test_inputs)}
        trials.append(record)
        print("real causal", record, flush=True)
        checkpoint()
    selected = {
        "gain_sweep": select_on_real(trial for trial in trials[1:] if len(trial["layers"]) == 1),
        "multilayer": select_on_real(trial for trial in trials[1:] if len(trial["layers"]) > 1),
    }
    report["selected"] = selected
    checkpoint()

    solved, _ = solve_coordinates(entities, facts, estimated)
    true_coords = oracle_coordinates(entities, facts, axis.anchors)
    true_axis = axis.anchors | true_coords
    truth_predictions = [(true_axis[q.a] > true_axis[q.b]) == q.positive for q in questions]
    report["oracle_coordinate_only"] = family_accuracy(questions, truth_predictions)
    report["oracle_log_mass"] = true_coords
    oracle = {name: (value - mean) / std for name, value in true_coords.items()}
    encoded = net.encode_qs(axis, questions, demos)

    def evaluate(name, blocks, vectors, **extra):
        pred = net.score(encoded, blocks, [vectors] * len(encoded))
        arms[name] = {"scores": family_accuracy(questions, pred),
                      "payload_bytes": sum(v.numel() * v.element_size() for v in vectors.values()),
                      "predictions": pred.tolist(), "layers": blocks, **extra}
        if arms[name]["payload_bytes"] != baseline["arms"]["map_memory"]["payload_bytes"]:
            raise ValueError("Every follow-up arm must match the original FP16 vector payload")
        checkpoint()
        print(name, arms[name]["scores"], flush=True)

    def vectors_for(coords, strength):
        return {name: (direction * (coords[name] - estimated[name]) * strength).half() for name in entities}

    evaluate("oracle_original", (layer,), vectors_for(oracle, gain))
    for name, setting in selected.items():
        blocks, strength = setting["layers"], setting["gain_per_layer"]
        evaluate(f"{name}_solved", blocks, vectors_for(solved, strength))
        evaluate(f"oracle_{name}", blocks, vectors_for(oracle, strength))

    direct = direct_questions(facts)
    if set(direct) != {q for q in questions if q.family == "stated"}:
        raise ValueError("Training prompts must be precisely the stated family")
    vectors, history = fit_vectors(net, layer, entities, net.encode_qs(axis, direct, demos),
                                   torch.tensor([q.yes for q in direct], dtype=torch.long), args.epochs, seed)
    if any(p.requires_grad or p.grad is not None for p in net.model.parameters()):
        raise AssertionError("The base model must stay frozen")
    evaluate("variant_b", (layer,), vectors, training=history)


if __name__ == "__main__":
    main()
