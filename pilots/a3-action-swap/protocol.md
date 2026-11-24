# A3 paired action-swap protocol

Test whether explicit lesson content can change the top action, not
merely sharpen the current ranking. Reuse the G1 router prompt and all
36 stateless checkpoint/code observations, the constrained A/B/C menu,
and the two Qwen2.5-Instruct Q4_K_M readers (0.5B and 1.5B) from
[A3](../a3-lessons-temperature/protocol.md). This is a decision-level
test, not a reward/rollout experiment. The old mapping remains in the
system prompt. The two legal directives each claim to replace it with
an unconditional rule; the assay therefore measures following even
where a directive disagrees with the old verifier.

## Frozen paired controls

- Freeze 20 distinct templates, each prescribing one legal tool at
  all observations. In its swapped twin replace only that letter
  with a different legal tool. Include each ordered A/B/C pair at
  least three times and counterbalance orientation exactly. Assign
  pairs to templates by a fixed seed, reused by both readers.
- Also score a twin with only that letter replaced by D (never in
  the legal menu), and neutral prose placed in exactly the same
  lesson slot. Check all four prompts have exactly the same full
  token count at each observation. Score a no-lesson baseline for
  bins and flip diagnostics. Use T=1 constrained token scoring and
  read the argmax in every arm; no action-sampling or rollout noise.

## Estimands

For a template with L prescribing a and L′ prescribing a′, use
½[P(top=a|L) − P(top=a|L′) + P(top=a′|L′) − P(top=a′|L)].
Probabilities here are empirical fractions of observations/lessons,
not softmax probabilities. In effect each of the 20 × 36 cells
contributes two directional differences with equal weight. The primary
test pools all 0.5B cells. **Dead if 0.5B follow index < 10 pp or its
95% CI includes zero.** Report named-action contrasts vs filler and
the non-menu twin; on non-modal targets also report how often each
arm flips the no-lesson argmax to the named legal tool.

## Matched margins

For each of the two directions separately, the pre-intervention
margin is the no-lesson top logit minus the no-lesson logit of that
direction's prescribed tool. Freeze an exact-zero bin and positive
bins 0.25 logit units wide up to 4, then a 4+ bin. Compare models
only in bins that have both readers. In pooled matched comparisons
give each shared bin the same weight for each reader, proportional
to its smaller cell count. Report matched results both with and
without the zero bin; positive margins show whether content can
overturn the existing mode rather than simply preserve it. Show
bin counts and target labels because matching on gap size does not
match token identity, full logit geometry, or the state mix.

Use 4,000 paired crossed percentile bootstrap draws: resample 20
whole lessons and 36 whole observations independently with
replacement, then take their Cartesian product. Use the same draw
for all readers, arms and directions. Hold the overlap weights
fixed and report the number of bootstrap draws with support when
resampling empties a bin. Never compare unmatched margins across
readers. Substantial positive following by 1.5B on matched positive
margins supports the margin explanation for prior zero flips, but
does not prove that scale or prompt differences play no role.
