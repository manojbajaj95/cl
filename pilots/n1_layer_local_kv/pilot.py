import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import time

import numpy as np
import torch

from pilots.m2_salience.pilot import ACTIONS, MODEL, REVISION, SEEDS, Backbone, attention_mask
from pilots.m2_salience.temperature_check import SOURCE_STATIONS
from pilots.temperature import fit_temperature, temper


STATIONS = ("Fox", "Oak", "Elm", "Bay", "Pine", "Hill", "Lake", "Rose", "Rock", "Vale")
ON = (
    "Which valve should Station {} use?",
    "Station {} needs its valve set. Choose the correct letter.",
    "What is the proper valve for Station {}?",
    "For a routine job at Station {}, name the valve.",
    "Pick the valve for Station {}.",
    "Station {} is starting a job. Which valve do you choose?",
)
OFF = (
    "Station {} has a local instruction to use valve {}. Which valve?",
    "Use valve {} at Station {} today. What is the valve?",
    "Station {}'s work order specifies valve {}. Which valve is specified?",
    "For this shift, Station {} must use valve {}. Pick the valve.",
    "The approved valve is {} at Station {}. Which valve should be used?",
    "The display for Station {} indicates valve {}. Choose the valve letter.",
)
BLOCKS = 6
BIAS_GRID = (-10., -5., -2., -1., 0., 1., 2.)
FULL = (True,) * BLOCKS
ARMS = ("full", "mask", "global_bias", "retrieval", "narrow_rewrite", "temperature")
FLOOR = 0.90


def lesson_probes(seed, stations=STATIONS):
    rng = np.random.default_rng(seed)
    names = [f"{station} {i}" for station in stations for i in range(1, 5)]
    targets = rng.permutation(np.resize(np.arange(len(ACTIONS)), len(names)))
    for name, target in zip(names, targets):
        other_names = rng.choice([n for n in names if n != name], size=len(OFF), replace=False)
        other_targets = rng.choice([a for a in range(len(ACTIONS)) if a != target], size=len(OFF))
        probes = [(template.format(name), int(target), True) for template in ON]
        probes.extend((template.format(*args), int(other_target), False)
                      for i, (template, other, other_target) in enumerate(zip(OFF, other_names, other_targets))
                      for args in [(other, ACTIONS[other_target]) if i not in (1, 4)
                                   else (ACTIONS[other_target], other)])
        yield name, ACTIONS[target], probes


class LayerBackbone(Backbone):
    def __init__(self, model):
        super().__init__(model)
        assert len(self.lm.model.layers) % BLOCKS == 0
        self.block_width = len(self.lm.model.layers) // BLOCKS
        self.block_masks = None
        for i, layer in enumerate(self.lm.model.layers):
            layer.register_forward_pre_hook(self.layer_mask(i // self.block_width), with_kwargs=True)

    def layer_mask(self, block):
        def replace_mask(_module, args, kwargs):
            if self.block_masks is not None:
                kwargs["attention_mask"] = self.block_masks[block]
                return args, kwargs
        return replace_mask

    @torch.no_grad()
    def evaluate(self, text, probes, configurations, *, all_actions=False):
        notes = self.ids(text)
        prefix = self.cache(self.intro + notes)
        self.suffix = {i: self.ids(query + "<|im_end|>\n<|im_start|>assistant\n")
                       for i, (query, _, _) in enumerate(probes)}
        targets = torch.tensor([target for _, target, _ in probes])
        groups = defaultdict(list)
        for query, ids in self.suffix.items():
            groups[len(ids)].append(query)
        out = np.empty((len(configurations), len(probes), len(ACTIONS)))
        for length, group in groups.items():
            jobs = [(i, q) for i in range(len(configurations)) for q in group]
            for start in range(0, len(jobs), 12):
                chunk = jobs[start:start + 12]
                indices, queries = zip(*chunk)
                biases = torch.tensor([configurations[i] for i in indices], dtype=torch.float32)
                tokens = torch.zeros(len(chunk), BLOCKS, len(self.intro) + len(notes))
                tokens[:, :, len(self.intro):] = biases[:, :, None]
                self.block_masks = [attention_mask(tokens[:, b], length) for b in range(BLOCKS)]
                try:
                    logp = self.scores(prefix, queries, tokens[:, 0])
                finally:
                    self.block_masks = None
                out[indices, queries] = logp.numpy()
        return out if all_actions else out[:, range(len(probes)), targets.numpy()]


def local_bias(mask):
    return tuple(0. if visible else float("-inf") for visible in mask)


def measure(out, blank, probes):
    gains = out - blank
    on = [on for _, _, on in probes]
    return gains[..., on].mean(axis=-1), np.maximum(0, -gains[..., np.logical_not(on)]).mean(axis=-1)


def choose_mask(model, lesson, train, blank, full, ablations):
    gain, harm = measure(full, blank, train)
    if gain <= 0:
        return FULL, full
    target = FLOOR * gain
    ablated_gains, ablated_harms = measure(ablations, blank, train)
    visible, best = list(FULL), full
    for block in np.argsort(ablated_harms, kind="stable"):
        if sum(visible) == 1 or ablated_gains[block] < target or ablated_harms[block] >= harm:
            continue
        candidate = list(visible)
        candidate[block] = False
        out = (ablations[block] if all(visible)
               else model.evaluate(lesson, train, [local_bias(candidate)])[0])
        gain, cost = measure(out, blank, train)
        if gain >= target and cost < harm:
            visible, best, harm = candidate, out, cost
    return tuple(visible), best


def match_bias(model, lesson, train, blank, grid, gain):
    measured, _ = measure(grid, blank, train)
    best = int(np.argmin(abs(measured - gain)))
    bias = BIAS_GRID[best]
    best_gain = measured[best]
    fits = [(a, b) for a, b in zip(range(len(measured)), range(1, len(measured)))
            if (measured[a] - gain) * (measured[b] - gain) < 0]
    if fits and abs(best_gain - gain) > 1e-3:
        a, b = min(fits, key=lambda pair: sum(abs(measured[i] - gain) for i in pair))
        lo, hi = BIAS_GRID[a], BIAS_GRID[b]
        f_lo, f_hi = measured[a] - gain, measured[b] - gain
        for _ in range(4):
            mid = lo - (hi - lo) * f_lo / (f_hi - f_lo)
            mid_gain, _ = measure(model.evaluate(lesson, train, [(mid,) * BLOCKS])[0], blank, train)
            f_mid = mid_gain - gain
            if abs(f_mid) < abs(best_gain - gain):
                bias, best_gain = mid, mid_gain
            if abs(f_mid) <= 1e-3:
                break
            if f_mid * f_lo > 0:
                lo, f_lo = mid, f_mid
            else:
                hi, f_hi = mid, f_mid
    return bias, best_gain


def lesson_text(name, action):
    return f"Station {name}: use valve {action}. Valve {action} is usually the safe setting.\n"


def split_probes(probes):
    return ([p for i, p in enumerate(probes) if i % 6 < 3],
            [p for i, p in enumerate(probes) if i % 6 >= 3])


def fit_source(model):
    blank, full = [], []
    for name, action, probes in lesson_probes(0, SOURCE_STATIONS):
        train, _ = split_probes(probes)
        blank.append(model.evaluate("", train, [local_bias(FULL)], all_actions=True)[0])
        full.append(model.evaluate(lesson_text(name, action), train, [local_bias(FULL)], all_actions=True)[0])
    return fit_temperature(np.concatenate(blank), np.concatenate(full))


def evaluate_lesson(model, name, action, probes, temperature):
    lesson = lesson_text(name, action)
    rewrite = f"Only at Station {name}, use valve {action}. Do not use this setting elsewhere.\n"
    train, heldout = split_probes(probes)
    blocked = [local_bias([i != j for i in range(BLOCKS)]) for j in range(BLOCKS)]
    ablation_set = [local_bias(FULL), *blocked]
    blank_train = model.evaluate("", train, [(0.,) * BLOCKS])[0]
    grid = model.evaluate(lesson, train, [*ablation_set, *((b,) * BLOCKS for b in BIAS_GRID if b)])
    full, ablated = grid[0], grid[1:1 + BLOCKS]
    bias_results = np.insert(grid[1 + BLOCKS:], BIAS_GRID.index(0.), full, axis=0)
    mask, train_mask = choose_mask(model, lesson, train, blank_train, full, ablated)
    train_gain, _ = measure(train_mask, blank_train, train)
    bias, bias_gain = match_bias(model, lesson, train, blank_train, bias_results, train_gain)

    raw_blank = model.evaluate("", heldout, [(0.,) * BLOCKS], all_actions=True)[0]
    target = np.asarray([label for _, label, _ in heldout])
    blank = raw_blank[np.arange(len(heldout)), target]
    temp = temper(raw_blank, temperature)[np.arange(len(heldout)), target]
    ablations = model.evaluate(lesson, heldout, [*ablation_set, local_bias(mask), (bias,) * BLOCKS])
    full_test, mask_test, bias_test = ablations[0], ablations[-2], ablations[-1]
    fires = [f"Station {name}" in q for q, _, _ in heldout]
    retrieved = np.where(fires, full_test, blank)
    narrowed = model.evaluate(rewrite, heldout, [(0.,) * BLOCKS])[0]
    gain, harm = measure(np.array([full_test, mask_test, bias_test, retrieved, narrowed, temp]), blank, heldout)
    return {"station": name, "valve": action, "mask": mask, "bias": bias,
            "gain": gain.tolist(), "harm": harm.tolist(), "train_gain": [train_gain, bias_gain],
            "train_layer_help": (measure(full, blank_train, train)[0] -
                                 measure(ablated, blank_train, train)[0]).tolist(),
            "heldout_layer_help": (gain[0] - measure(ablations[1:1 + BLOCKS], blank, heldout)[0]).tolist(),
            "recall": float(np.mean(np.array(fires)[[on for _, _, on in heldout]]))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    model = LayerBackbone(args.model)
    tuning = fit_source(model)
    print(json.dumps(tuning), flush=True)
    result = {"model": MODEL, "revision": REVISION, "blocks": BLOCKS, "arms": ARMS,
              "temperature_fit": tuning, "seeds": []}
    for seed in SEEDS:
        start = time.monotonic()
        lessons = []
        for name, action, probes in lesson_probes(seed):
            lessons.append(evaluate_lesson(model, name, action, probes, tuning["temperature"]))
            if len(lessons) % 10 == 0:
                print(f"seed {seed}: {len(lessons)} lessons in {time.monotonic() - start:.1f}s", flush=True)
        result["seeds"].append({"seed": seed, "seconds": time.monotonic() - start, "lessons": lessons})
        args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
