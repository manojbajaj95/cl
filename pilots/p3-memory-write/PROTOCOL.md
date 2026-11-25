# P3 protocol

## Replicate before testing writers

Use the real-unit, **wrong target lesson / no verifier** cohort from
[PR #4](https://github.com/manojbajaj95/cl/pull/4), as cited by
[P3](https://github.com/manojbajaj95/cl/pull/7). In the source, the 0-vs-1
comparison counts **wrong off-target lessons**, not all off-target lessons:
both had three off-target lessons total. The source log has 12/32 vs 17/28
bad writes and 0/32 vs 1/28 solved in this cohort.

- Clean: wrong target lesson plus three correct off-target conversion lessons.
- Distractor: corrupt one of those three off-target factors.
- Filler: replace that same slot with number-free, non-conversion prose of
  exactly the same actor prompt token count as the distractor. The other three
  slots, task, shuffle, and sampling seeds are unchanged.

Pair all three arms on the six source tasks × seven source quantities × five
draws of off-target lessons/order and decoder seeds (210 episodes per arm).
Use the source's actor and baseline writer prompts, Qwen2.5-1.5B-Instruct
Q4_K_M on CPU, temperatures 0.3/0.7 and 120-token caps. Evaluate with the
source's 3% numeric heuristic (last answer number for solving; any write number
for the true factor). There is no admission gate: its verdict did not enter
the source's bad-write or solve metrics.

## Paired writer intervention

Cache the distractor arm's exact sampled action tokens and answer. Do not
sample the actor again. Hold writer seed, temperature and generation cap fixed.

- **Baseline**: full PR #4 prompt with observations, task and answer.
- **Log-prob mask**: score each observation line by independently removing it
  from the actor prompt and teacher-forcing the cached answer. The score is the
  mean absolute change in answer-token log probabilities (nats, raw model
  softmax before sampling adjustments). Give the writer only lines with score
  ≥0.05, in their original order, plus the task and answer. This is an
  observation-span mask, not a per-token or jointly optimal subset.
- **Trace only**: the writer sees its own answer and a generic lesson-writing
  instruction. It does not see the original task text, retrieved lessons,
  verifier feedback, units, or factors other than what appeared in its answer.
- **Task-only instruction**: keep the baseline observations, task and answer;
  replace the trailing purpose phrase with “Write only about the task.” The
  full rendered prompt must exactly match baseline token count for each answer.

## Analysis and decision

Report Wilson 95% intervals for descriptive rates and 10,000 percentile
bootstrap draws for differences, resampling full episode pairs within each
target × quantity stratum. Intervals are conditional on this task suite and
model. Subtract the change in solve-failure rate from the change in bad-write
rate for each contaminated arm versus clean. The primary contrast is the
difference between those two changes (distractor minus filler).

Kill this pilot unless the distractor increases bad writes over clean and the
primary contrast is positive, with both paired 95% intervals above zero. Even
if both pass, kill unless the mask reduces bad writes versus baseline and
trace-only (paired 95% intervals below zero for mask minus control). An interval
spanning zero is a failure to demonstrate a useful advantage, not evidence
that the two methods are equivalent. Report the instruction contrast even if
an earlier gate already kills the pilot.

## Reproduce

Run from this directory with Python 3.10+, the CPU dependencies in
`requirements.txt`, and the [Qwen GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf)
(SHA-256 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`).
Set `MODEL` to the GGUF path and `OUT` to a fresh output directory.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s . -v
export OPENBLAS_NUM_THREADS=1
python -u pilot.py baseline --model "$MODEL" --out "$OUT"
python analyze.py "$OUT/baseline.jsonl" --phase baseline
python -u pilot.py writers --model "$MODEL" --out "$OUT"
python analyze.py "$OUT/episodes.jsonl" > "$OUT/results.json"
```
