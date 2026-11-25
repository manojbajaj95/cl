# A3 CPU pilot protocol

Test the [PR #27 A3 proposal](https://github.com/manojbajaj95/cl/pull/27)
on the three-decision [G1 router](https://github.com/manojbajaj95/cl/pull/14),
with the same [Q2 checkpoints](https://github.com/manojbajaj95/cl/pull/25).
The Qwen2.5-1.5B-Instruct reader is primary: A3 predicts what happens
after the upgrade. Repeat all scoring on Qwen2.5-0.5B-Instruct as a
secondary comparison; that model also writes the failure notes. Both
checkpoints are Q4_K_M and run on llama.cpp with CPU only.

## Intervention and arms

- Keep G1's transitions, two-correct-decisions reward and stateless
  checkpoint/code prompts with the original documented mapping B/C/A
  for remainders 0/1/2. Silently rotate the **verifier** to C/A/A. This
  is a selective remapping, not a bijective permutation: the upgraded
  reader's G1/Q2 no-lesson mode is A at all observations, so the proposal's
  requirement that it be wrong at remainder 0 and right elsewhere
  cannot be met by a bijection. Check that the condition still holds
  before evaluating. Only a rule lesson explicitly supplies the update.
- Freeze source starts at displayed codes 10–15 and held-out starts
  at 16–21. Each half has two of each remainder and, for the upgraded
  reader's modal no-lesson trajectory, four successful starts and two
  unsuccessful starts. Do not search partitions or report unbalanced
  reliability. Later states can be reachable from both halves.
- As in Q2, draw 300 old-model no-memory episodes from source starts
  and write 20 notes from randomly ordered distinct failed episodes.
  To isolate explicit rule content, give the writer verifier feedback
  (correct/incorrect by checkpoint) but not the code or tool identities.
  Sample general process advice at 0.65 with fixed seeds and filter empty
  responses or likely code/tool mentions. Add
  the true rule to 10 preselected slots. Freeze 20 more hand-stratified
  lessons (10 useful rule formulations, 5 neutral and 5 misleading
  non-rule G1 notes). Thus half of each provenance and exactly 20/40
  state the changed rule. Keep all qualifying texts including duplicates.
- At each of 36 observations score the constrained next-token policy
  (A, B, C only, temperature 1): no lesson, each rule/other lesson, and a
  paired no-content prose filler. Filler uses a neutral garden narrative
  with the same prompt placement and **exact full-prompt token length**
  as its paired lesson at every observation. The filler is a placebo
  for added text, not a second temperature fit.
- Fit one scalar inverse temperature per lesson, separately per
  checkpoint model. Use base-policy visitation from uniform *source
  starts* at each of three steps as fixed entropy weights for both
  policies. Solve for the no-lesson logit scaling that yields equal
  mean entropy. Fixing visitation ensures that the control matches
  policy uncertainty on comparable observations rather than changes in
  which states a lesson visits. The solver sees no held-out starts or
  success outcomes. Apply the fitted no-lesson policy unchanged on
  held-out starts. This is not the outcome-optimized retrospective fit
  in PR #27.

## Estimates and kill lines

Enumerate all 27 action paths to compute exact success at each start for
each arm. Baseline-center success to obtain each per-lesson/start effect.
Compute pooled held-out R² (1 − SSE/SST over the 40 × 6 cells, centered
on the grand mean), the paired mean rule lesson minus its temperature
match in percentage points, and the two-way ANOVA lesson main-effect
share (lesson sum of squares divided by total sum of squares). Also
report non-rule-only R² (proposal prediction ≥0.80), matched filler
contrasts and Pearson split-half correlation of per-lesson mean effects
using only the two balanced halves.

For percentile 95% CIs, use 4,000 paired lesson bootstrap draws
stratified by rule status and lesson provenance; keep all fixed starts
and each lesson's fitted temperature and paired filler together. These
are conditional on the starts, models and lesson-writing procedure,
not uncertainty over a population of tasks or models. Repeat with
one entry per exact prompt as a sensitivity check for duplicate notes;
the decision uses all 40 entries as proposed.

**Dead if pooled held-out R² < 0.50, or rule-stating lessons beat their
temperature match by ≥ 5 pp with CI above 0, or the lesson main effect
exceeds 25%.** Apply the decision once, to the primary upgraded reader
with all 40 lessons pooled; the older reader is a diagnostic.
