# SM1 self-readable seed log: CPU pilot (PAUSED, no result yet)

Status: **paused before the first test ran** (dispatcher asked for all effort on growing the idea pool first). No keep-or-kill yet. This folder holds the harness and the plan so the test can resume without redesign.

Source: SM1 in `ideas/flood/self-modifying.md` (PR #43); first test, kill line and retention check from `reviews/flood-top10.md` §3 (PR #6).

## What is here
- `tasks.py`: five procedurally generated two-way tasks scored by their two label tokens (parity, mammal, sentiment, compare, continent). Word-list tasks use disjoint train/test words.
- `seedlog.py`: MeZO over a flat LoRA vector. Weights move only by `theta <- theta - scale * z(seed)`, with each perturbation applied to a copy, so the trajectory *is* the `(seed, scale, task, reason)` log and `replay()` regenerates theta bitwise (bitwise check not run yet). `replay(lines, multipliers)` drops (0) or rescales lines.
- `tune.py`: MeZO step-size sweep.

## Observed so far
- Qwen2.5-0.5B-Instruct base accuracy on 200 test items: parity 0.48, mammal 0.455, sentiment 1.00, compare 0.54, continent 0.67. So four tasks have room to move ≥ 5 pp, and sentiment (base 1.00) is the natural task to corrupt: flipped labels give a large, unambiguous regression.
- Speed on the 8-core CPU VM: a 32-item forward takes about 0.7 s, so one MeZO step (batch 16, two forwards) is about 1 s.
- Tuning was stopped after 50 steps on mammal (r=4 q/v lr 1e-3 and 5e-3, r=1 v/o lr 2e-2): no config had moved ≥ 5 pp yet. MeZO's learning rate is the main risk the reviewer named.
- Bug fixed before commit: item and batch seeding used Python `hash()` of strings, which is salted per process, so the test set and the "same seeds, same batches" retrain would differ between processes. Both now use `stable_seed` (crc32).

## Plan to resume (about 3-4 CPU-h, no GPU needed)
1. Tune until each of parity, mammal, compare, continent moves ≥ 5 pp in ≤ 300 steps (smaller d, e.g. r=1-2 on fewer layers, or larger lr). If MeZO cannot, the test is blocked at 0.5B, not killed.
2. Bitwise check: `torch.equal(replay(log), trained theta)`.
3. Per seed (3 seeds): corrupted stream parity → mammal → sentiment (labels flipped) → compare → continent; retrain-without-sentiment with the same seeds and batches for kept lines (scalars recomputed); a second retrain-without with other seeds as the seed-noise reference; a clean stream.
4. Edits on the corrupted log, each scored by how many evaluations it needs: LLM reader (0.5B itself, and 1.5B) reading a run-grouped log plus a symptom report; a keyword rule on the reason field (matched control, since the task tag makes the reader's job a grep); log bisect; random drops of equal size; naive reversal of the last k lines.
5. Kill line: the reader is no better than bisect at equal evaluations (and no better than the keyword rule), **or** dropping lines departs from retrain-without (max per-task accuracy gap, label-probability KL) by more than the regression it fixes (sentiment accuracy gain from the edit). Compare the departure with the retrain-vs-retrain seed noise.
6. Retention: the other four tasks stay within 1 pp of the pre-edit model after the edit.
7. Optional variant that separates reading from search: corrupt batches from one "source" scattered across two tasks, so bisect over contiguous ranges is costly.

## Prior art to keep in view
- ZOCheck 2609.27189 (seed-based ZO checkpointing) and FedZOUL 2610.35211 (exact ZO unlearning). FedZOUL restarts from the first affected step and recomputes later scalars, so it already treats "subtract the lines with fixed scalars" as inexact. The open half of SM1 is the model reading and editing its own log, plus measuring how far fixed-scalar line drops depart from retraining.
