# Next step: 7B ALFWorld replication

**Question.** Does entropy-matched decoding explain the held-out effect
of memory prompts on a longer-horizon agent benchmark, or only on a
small router whose baseline nearly always chooses one action? Replicate
the same controls before claiming a general memory mechanism.

## Benchmark and agent

- Use frozen [ALFWorld](https://github.com/alfworld/alfworld)
  TextWorld games (dataset json_2.1.1) and Qwen2.5-7B-Instruct at BF16
  on GPU. Pin benchmark and checkpoint revisions, prompts, tokenizer,
  decoding and environment seeds in a manifest. Use official game
  completion as the primary outcome with a 50-action budget.
- Source games come from `valid_seen`; held-out games come from
  `valid_unseen`, with no repeated game IDs. Predefine eligibility
  and order by a seed before running any lessons. Use 32 held-out games
  and 32 source games. Use an independent no-lesson qualification
  bank (32 seeds per candidate game) to choose equal numbers of
  stronger (win rate ≥50%) and weaker (<50%) starts, with a matched
  objective-family mix across sides. Preassign 16+16 held-out games
  to two similarly balanced blocks before collecting any lesson
  scores. Qualification outcomes never enter reported comparisons
  or the temperature objective. If the pool cannot support these
  splits, report infeasibility rather than picking starts with high
  lesson effects.
- Use the same input at each step across arms: goal, recent
  observation/action history with a fixed truncation rule, and the
  environment's sorted admissible commands as a menu. Use a frozen
  codebook of verified single-token action IDs with no collisions,
  and sample directly from next-token logits restricted to the
  menu. Check the maximum menu size against the codebook on the
  benchmark before running. No expert action ranking or planner in
  the agent. This is a constrained-action ALFWorld evaluation, not
  directly comparable to word-by-word agent leaderboards.
- Before scoring lessons, check for baseline mode collapse on the no-memory
  source tape. Report the top-command verb distribution, modal share,
  and legal-action entropy by task family, alongside the menus' verb
  diversity. If one verb is the top action on ≥90% of source states with
  at least two admissible verb types, stop and report a collapsed agent;
  this setup would not test transfer beyond the router's single-mode
  regime. Freeze this criterion before inference.

## Arms and calibration

- Freeze 40 notes from source failures only, with 20 explicit valid
  procedural rules and 20 non-rule notes. Use 20 distilled failure
  records (randomize whether a verified procedural rule is
  included) and 20 hand-stratified notes. Rules state benchmark
  mechanics transferable across games (e.g., "open a closed
  receptacle before retrieving from it"), not a held-out solution or
  object location. Preassign eligibility and rule/non-rule labels
  before collecting effects; require distinct final texts.
- Evaluate no memory, each memory note at T=1, a paired length-matched
  same-slot irrelevant prose note at T=1, and a separate no-memory
  temperature matched to each note. Verify full prompt-token counts
  after history truncation; reserve the same history budget on all
  arms. A no-memory T=1 rollout can be shared across notes for a
  given game and seed. Use common uniform action draws across arms
  within each game/seed, with independent seed banks.
- Fit one inverse temperature per note using only a fixed tape of 16
  decision states per source game, subsampled from T=1 no-memory
  trajectories (equal game weight). Compare legal-action entropies
  on the exact same observations for lesson/no lesson; fit on
  source entropy alone, not success. Report fit residuals, boundary
  solutions, menu sizes and entropy by game family. On held-out
  games, run each policy live; do not score only states visited by
  the no-memory policy.

## Evaluation and stop rules

- Stage one is a source-only smoke test, capped at **≈3 GPU-hours**:
  check menu/codebook handling and mode collapse, then compare 8 frozen
  lessons (4 rule, 4 other) with no memory on 8 balanced source games
  using 4 paired seeds per game. Proceed only if mean lesson lift is
  **≥5 pp** in verified completion vs no memory. Report its paired CI
  and stop without opening the held-out lesson run if the gate misses
  or the stage cannot finish within budget. These rollout seeds do not
  enter the held-out estimates.

- Test all 40 lessons on all 32 held-out games. Start with two
  independent banks of eight rollout seeds per game/arm. Report
  ordinary pooled held-out R² beside a noise-corrected version:
  center the lesson-effect cells within each bank and use their
  cross-product for SST; use the cross-product of (lesson effect
  minus temperature effect) residuals across banks for SSE. Use
  each bank's own baseline; a shared noisy baseline across banks
  would inflate explained variance. For lesson main-effect share
  use the same cross-bank estimator on centered lesson means
  (times the count of games). Do not clip negative estimates.
  Apply the identical R² calculation with each lesson's matched filler
  effect as the predictor and report **temperature R² minus filler R²**
  with a paired CI, not just either absolute fit.
- If the cross-bank SST is nonpositive or cross-bank Pearson
  agreement of cell effects is <0.70, double both seed banks once
  as predeclared, without inspecting gate estimates to choose
  additional runs. If still unreliable, report inconclusive, not
  keep. Report split-half agreement only for the balanced game
  blocks. Give percentile 95% CIs via paired resampling of
  lessons by provenance/rule, games within qualification strata,
  and paired seed indices within banks; the source calibration
  tape is held fixed.
- Apply the router thresholds to the noise-corrected held-out
  estimates: **kill** if pooled R² <0.50, rule lessons beat their
  temperature matches by ≥5 pp with CI above 0, or lesson main
  effect exceeds 25%. Also report uncorrected estimates, rule and
  other lessons vs filler, no-memory success by stratum, and
  sensitivity by objective family.
- **Content-transfer kill line:** On a fixed held-out no-memory state
  tape, compare the rule arm and its paired filler on identical
  observations where the base top action is wrong and where the
  note's correct action can be independently labeled by the benchmark
  expert. A correct flip means that this arm switches its top action
  to the expert-verified action. Report eligible counts and both
  rates; kill the content-transfer claim if the paired rule − filler
  correct-flip gap does not have a 95% CI entirely above zero.
  Use the expert only to label/scaffold this evaluation, never to
  select the agent's live action. If eligibility is absent, report
  content transfer as untested, not supported.

## Compute and artifacts

Run on one or more GPUs with local access to the full action logits
(e.g. vLLM or Transformers with masked logits and batched KV
caching). After the ≈3 GPU-hour first-stage gate, the main design
starts at 61,440 held-out lesson/temperature/filler rollouts plus
shared no-memory, qualification, and source calibration runs. Record
measured GPU-hours before scaling; parallelize over games and seed banks.
Do not use the OpenRouter free tier for this design: even aside from
the request budget, sparse or unavailable logprobs cannot establish
a full-menu entropy match. Release game IDs, lessons, code, source
entropy fits, rollout checksums, arm success counts, and results
with a keep/kill/inconclusive verdict. This specification is not a
claim that the 7B experiment has been run.
