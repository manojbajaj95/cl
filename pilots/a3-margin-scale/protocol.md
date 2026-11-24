# A3: Controlled and natural margin protocol

Reuse the two pinned Qwen2.5-Instruct Q4_K_M checkpoints, G1's
stateless checkpoint/code observations, and the 20 legal-action
lesson/twin pairs from [the paired swap test](../a3-action-swap/protocol.md).
The question is whether 1.5B follows a prescribed action once its
baseline top-vs-runner-up gap lies in the 0.5B small positive-margin
bins: (0, 0.25), [0.25, 0.50), [0.50, 0.75), [0.75, 1.00) logit units.

## Interventions

1. **Controlled.** Use the original A/B/C prompts and frozen score tables.
   Fit one nonnegative constant to subtract from A: on the six source
   starts (checkpoint one, codes 10–15), minimize mean absolute
   difference between sorted 1.5B and 0.5B top-two gaps on a 0.005-logit
   grid, with A still on top in every 1.5B source state. Fit on no-lesson
   scores only, then exclude those six observations. Apply the same
   offset to the baseline, original rule, swapped rule and its filler;
   do not refit by state, prompt or lesson. Keep only test observations
   in the small bins. Checkpoints two and three can be reached from
   either start half; no later observations enter the offset fit.
2. **Natural.** Do not adjust logits. Traverse a frozen list of eight
   novel single-token label triples, trying the five nonidentity menu
   permutations in lexicographic order. For each of the 36 observations
   take the first no-lesson variant in the small bins; do not count
   multiple variants of the same checkpoint/code as different states.
   Rename actions consistently in the system rule, lesson and twin, but
   leave the user observation and reward unchanged. Use the same menu
   and label variant for both rule prompts and for same-length filler;
   verify full-prompt token counts. Freeze discovery before collecting
   any natural lesson scores. **Require at least 30 distinct eligible
   natural states**; below 30 the verdict is inconclusive.

## Score and decision

On each admitted state compare only lesson pairs naming both baseline
top-two tools (one per twin). This places one direction at the small
positive gap and the other at zero; it prevents an unrelated low-ranked
third action from diluting the test. Compute
½[P(top=a|L) − P(top=a|L′) + P(top=a′|L′) − P(top=a′|L)]
across eligible lesson/state pairs. Report named-action excess vs
filler and the fraction of runner-up targets that become top-ranked
with a valid directive or filler. For each arm report paired 95%
percentile intervals from 4,000 crossed draws over whole lessons
and whole states with replacement. Freeze the offset, natural
variants, and compatible-cell mask; report the number of draws
with support.

- **Margin:** both 1.5B follow indices are ≥10 pp and both 95% CIs
  are above zero.
- **Scale:** both follow indices are near zero, operationalized as
  each 95% CI lying wholly within ±5 pp (half the meaningful-follow
  threshold).
- **Inconclusive:** split, weak or imprecise arms, or natural coverage
  below 30; carry the contrast to 7B. Even a margin result identifies
  what these interventions do to 1.5B, not a universal scale law.
