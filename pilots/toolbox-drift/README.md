# Toolbox vs lessons under API drift: KILL

Pilot of the reviewer-narrowed Agent Toolbox claim: a code toolbox detects API
drift and recovers in fewer uses than text lessons ("tools fail loudly, lessons
fail silently"). Protocol frozen in `protocol.md` before the full run (floor arm
added mid-run per reviewer, before any of its data existed).

20 procedures, 6 of 20 APIs (30%) drift at episode 60 of 180 (3 breaking +
documented, 3 silent), 3 seeds, 18 drifted units per arm, Qwen2.5-Coder-3B Q4 on CPU.
Measures are in post-drift uses of that procedure (~5.7 uses per unit; never =
uses + 1). 95% CIs: hierarchical bootstrap (seeds, then units), 10,000 draws.

## Primary contrast: lesson+tests minus tool+tests (positive = tools faster)

| measure | mean | 95% CI | seed means |
|---|---|---|---|
| detect | +1.44 | [+0.33, +2.94] | 0.83, 1.33, 2.17 |
| recover | +0.72 | [-0.33, +2.39] | 1.67, 0.50, 0.00 |
| detect, breaking only | +2.89 | [+1.00, +5.33] | |
| detect, silent only | 0.00 | [0, 0] | |
| recover, silent only | +1.11 | [0.00, +4.44] | |

**Verdict: KILL** under the frozen rule (tools faster only to detect; recovery tied).

Why the detection gap is not "lessons fail silently":
* It is all breaking drift. A lesson is re-instantiated against the current API
  listing every episode, so a documented rename is usually absorbed with no
  error at all (detection censored, yet recovery at use 1-2). Tools crash at use 1.
  Breaking recovery: lesson+tests 2.33 vs tool+tests 2.00 uses.
* On silent drift, tests flag both arms at use 1 (0 silent-wrong uses in both
  tests arms). Without tests both fail silently alike: 2.06 (tool) vs 2.39
  (lesson) silent-wrong uses per unit.
* Silent drift is mostly unrecovered by every arm (recover 5.9-7.0 of ~5.7 uses):
  the 3B repairer rarely infers the transform from failing tests.

## All arms

| arm | detect | recover | silent-wrong | wrong uses | pre-drift acc | undrifted post acc | false flags | LLM calls | tokens |
|---|---|---|---|---|---|---|---|---|---|
| tool | 1.94 | 4.50 | 2.06 | 3.56 | 1.000 | 1.000 | 0.0 | 9 | 5.4k |
| tool+tests | 1.00 | 3.94 | 0.00 | 3.00 | 1.000 | 1.000 | 0.0 | 34 | 20k |
| lesson | 3.56 | 4.83 | 2.39 | 3.72 | 0.944 | 0.838 | 11.3 | 199 | 116k |
| lesson+tests | 2.44 | 4.67 | 0.00 | 3.61 | 0.950 | 0.834 | 18.0 | 333 | 197k |
| none (floor, T=0.25) | 3.44 | 5.56 | 3.28 | 4.56 | 0.367 | 0.309 | 26.0 | 180 | 97k |

Per-run means over 3 seeds; censored detect/recover counts and every contrast are in `results.txt` / `results.json`.

## Against the entropy-matched no-memory floor (none minus arm, positive = arm faster)

T fit on pre-drift prompts only (`temperature_fit.json`): lesson target entropy
0.034 nats/token at T=0.3, matched by the no-memory prompt at T=0.25.

| arm | detect | recover | wrong uses (post hoc) |
|---|---|---|---|
| tool | +1.50 [+0.56, +2.44] | +1.06 [+0.11, +2.28] | +1.00 [+0.06, +2.22] |
| tool+tests | +2.44 [+1.39, +3.33] | +1.61 [+0.28, +3.39] | +1.56 [+0.17, +3.39] |
| lesson | -0.11 [-1.22, +0.78] | +0.72 [+0.17, +1.44] | +0.83 [+0.11, +1.61] |
| lesson+tests | +1.00 [-0.44, +2.22] | +0.89 [+0.22, +1.67] | +0.94 [+0.17, +1.83] |

Every memory arm recovers faster than the floor; plain lessons detect no faster than it.

## What survives

The drift-detection claim is dead. What the data does show is the plain toolbox
efficiency claim (already covered by LATM/TroVE/Voyager): stored code is exact
(1.000 vs 0.83-0.95 accuracy on undrifted procedures, 0 vs 11-18 false flags)
and uses 10-20x fewer tokens than re-deriving code from a lesson each episode.

Limits: one 3B model; ~5.7 post-drift uses per unit (coarse, heavily censored on
silent drift); toy deterministic API; 3 seeds.

## Reproduce

```
pip install llama-cpp-python==0.3.38 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu numpy pytest
# model: Qwen2.5-Coder-3B-Instruct GGUF q4_k_m at ~/models/qwen2.5-coder-3b-instruct-q4_k_m.gguf
python3 -m pytest -q test_pilot.py
./launch.sh                      # 4 memory arms x 3 seeds
python3 fit_temperature.py && ./launch_none.sh   # floor arm
python3 analyze.py > results.txt
```
About 2 h wall clock on 8 CPU cores.
