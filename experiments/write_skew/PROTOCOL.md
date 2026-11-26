# Fixed-slot write-skew screen

Freeze this design before scoring. Test the context-store version of expanded
top-10 idea 3 ([spec](https://github.com/manojbajaj95/cl/blob/3d72df549945f5aa243baa399c954ee9628374db/reviews/flood-top10.md),
[control design](https://github.com/manojbajaj95/cl/pull/103)).

- Frozen Qwen2.5-0.5B-Instruct, official FP16 GGUF, CPU. Fix the old rule
  `kavimer → 4` for all stores. Generate 30 held-out stores (seeds 100–129)
  and 12 separate count-fit stores (0–11). Sample three unrelated, distinct
  ticket keys, three distinct non-target queues, and old-rule slot uniformly.
- Score all eight subsets with A always present. Inactive slots are explicitly
  ignored notes, not deleted text. Hold exact token count, rule/query locations,
  syntax of active rules and per-slot queue digits fixed. The matched control
  repeats the factorial with three disjoint random keys sampled by the same rule,
  the same queues per slot, and the same inactive notes. There is no expected
  direction to an effect of random focal versus random control identities.
- Use two fixed query phrasings, reported separately. On each, strict failure:
  A beats all five rivals in all seven proper subsets and loses or ties at least
  one at the full triple (zero-logit floor). Record the target-versus-all
  log-probability differences. For the primary continuous contrast choose the
  highest non-target logit in the shared empty-subset arm, then freeze that
  rival across masks and the matched control. Audit six-way accuracy and
  full-bundle accuracy on the new keys; remove A at matched length to check
  that old reads depend on the rule.
- Compare the third finite difference to the pooled mean absolute second
  differences at the empty subset. At the published kill bar (<0.10) the
  third-order signal is too small. Even above it, ask if size is sufficient:
  fit mean margin changes by active count (0 to 3) on 12 separate stores,
  anchor at the held-out empty cell, and report full-bundle prediction error,
  count-centered third differences, and the match to disjoint-control
  distributions. Also report the pairwise-only extrapolation from all
  seven proper subsets and whether it already predicts any strict crossing
  (separately for every rival), plus a count-curvature correction to that
  extrapolation. Large factorial contrasts alone do not pass the screen:
  require a strict miss by the lower-order forecast and evidence not
  accounted for by count curvature or generic matched fillers. Use each
  store, not each mask, rival, or wording, as the unit of uncertainty.
- Calibrate the interaction calculation on three synthetic cubes: additive
  losses that cross the floor, pure count curvature that mimics a cubic
  term, and a planted triple-only failure. Do not use these as model results.
  No LoRA experiment at this gate.
