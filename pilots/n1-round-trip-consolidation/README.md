# N1: round-trip consolidation

Does distilling an agent-authored Python helper's I/O into LoRA, then generating
the helper afresh without source access, produce a better program than asking the
untuned author to rewrite and refine it at equal compute?

## Status: paused (not tested)

The CPU harness is implemented, but the comparative run was stopped before
the first seed completed. No round-trip LoRA, matched-control, or retention
results are available. **No keep-or-kill verdict.**

The completed CPU setup check generated 36 original helpers (12 families ×
3 seeds). Original accuracy was **18.58% held out** (214/1,152; 95% CI
1.39–41.93%) and **27.78% on the seen examples** (100/360; 95% CI
9.17–50.56%). Held-out failure was 81.42% (95% CI 58.07–98.61%), above
the 30% headroom requirement. The low seen accuracy is a limitation: many
original helpers were wrong even in distribution, so this gate alone does
not show that the helpers overfit. These are original-helper-only setup
numbers, not evidence for or against the round trip. The four harness unit
tests completed successfully.

If work resumes, rerun the gate to recreate its local artifact, complete
all three seeds of the comparative trial and MBPP/seen-family retention,
and apply the decision rule below. The gate ran on CPU; trial runtime was
not measured to completion and no GPU requirement was established.

## Protocol

The [novelty triage](https://github.com/manojbajaj95/cl/blob/refs/pull/6/head/reviews/flood-triage.md)
ranks N1. The actual first test, kill line and retention check are in the
[reviewer's follow-up](https://github.com/manojbajaj95/cl/blob/refs/pull/6/head/reviews/flood-top10.md#top-3-for-deep-work)
on [ledger PR #6](https://github.com/manojbajaj95/cl/pull/6), using the
[source card](https://github.com/manojbajaj95/cl/blob/refs/pull/41/head/ideas/nooa/batch-1.md#n1-round-trip-consolidation-weights-as-a-denoiser-for-agent-code)
on [PR #41](https://github.com/manojbajaj95/cl/pull/41).

- **CPU configuration:** Qwen2.5-Coder-1.5B-Instruct in FP32, greedy pass@1, 8
  threads. Independent seeds 101, 202, 303 each create 12 separate helpers (six
  string and six grid transformations) from ten labeled examples per family.
  Every seed uses another ten source-distribution inputs for teacher execution
  plus 32 disjoint held-out inputs per family with longer strings, new
  characters, or rectangular grids and different values. The held-out set is
  scored only, never used to train or choose code. The original must fail at
  least 30% of the held-out variants before LoRA runs.
- **Matched arms:** original helper; source-visible base rewrite; same rewrite
  with test feedback on the original ten examples and selection on their pass
  count; source-blind base rewrite (inert padding matching the old source's
  token count); round-trip; shuffled-label round-trip; environment-label
  upper bound. The last three all use rank 8 Q/V LoRA with the same seed,
  inputs, padded batch shapes, optimizer and steps (three epochs). The
  shuffled arm permutes the original helper's outputs within its family and
  retains all labels. The upper bound has ground-truth outputs on the same
  query inputs; they are not available to the actual round trip. All
  rewrite/decompile arms get the original ten environment examples, which
  were already available for authoring; **only** source-visible arms receive
  the original code. Greedy decoding makes positive-temperature rescaling
  invariant, so a temperature-only greedy control would duplicate its arm.
- **Compute match:** identical per-attempt generation cap (128 tokens) for
  all ordinary rewrites/decompilations; the refinement control buys extra
  attempts with the round trip's forward-equivalent token-position budget.
  Generation counts padded prefill and decode positions; training counts
  padded tokens twice for the backbone forward and activation backward.
  This is a compute proxy, not exact FLOPs or wall time. Max generation length
  of the last refinement can be reduced to stay within budget. Use only
  original examples to select among attempts.
- **Retention:** compare the same base and round-trip-adapted checkpoints,
  without rewrite or refinement, on generated helpers' pass@1 on the
  original seen inputs and on a fixed 50-item sample from sanitized MBPP's
  official test ID range. On MBPP, the first assertion is public to specify
  the callable name; all three assertions must pass. Execution is isolated
  in a resource-limited Linux seccomp worker.
- **Decision:** kill if round-trip accuracy is ≤ best of the plain and refined
  source rewrites + 3 pp, or its paired improvement over shuffled does not
  clear zero at 95% confidence. Both old-task accuracy changes must be no
  worse than −1 pp; report their uncertainty separately. Intervals use 10,000
  paired bootstrap draws of seed and family (MBPP item for retention), not
  1,152 independent test cases. Three seeds support a screening decision,
  not a precise population estimate.

## Reproduce

Run on Linux with Python 3.10+ and `libseccomp.so.2`:

```sh
python -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
huggingface-cli download Qwen/Qwen2.5-Coder-1.5B-Instruct \
  --revision 2e1fd397ee46e1388853d2af2c993145b0f1098a --local-dir "$HOME/n1-model"
curl -fsSL https://raw.githubusercontent.com/google-research/google-research/ee4298226f21649f45c0d0427f7c0f3f682d2a20/mbpp/sanitized-mbpp.json \
  -o "$HOME/n1-mbpp.json"
python -m unittest -v
python pilot.py gate --model "$HOME/n1-model" --out "$HOME/n1-results"
python pilot.py trial --model "$HOME/n1-model" --out "$HOME/n1-results" --mbpp "$HOME/n1-mbpp.json"
python summarize.py "$HOME/n1-results"
```
