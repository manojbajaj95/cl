# G1 protocol

* One frozen Qwen2.5-1.5B-Instruct Q4_K_M CPU model. Three router decisions
  with an action-dependent next code; binary terminal utility for at least
  two correct decisions. The tool interface constrains the next token to
  exactly A, B or C. At temperature 1, normalize those logits over the
  legal set for both sampling and scoring. This tests **exact ratios of
  the constrained policy**, not ratios of unconstrained generations.
  The agent receives the current checkpoint and code; no conversation
  history beyond this observation. Identical observations within a prompt
  edit can reuse logits. No replay environment calls at ranking time.
* Freeze 30 lessons (10 helpful, 10 weak/neutral, 10 misleading by intent)
  before running the agent. Draw 500 behavior trajectories without lesson
  text. Replay every logged token under the 30 prompts; save legal token
  log probabilities and emitted tokens. The terminal cumulative-weight
  Kish ESS is the primary overlap diagnostic; also report every prefix ESS
  and the count of sampled decisions per trajectory with |log ratio| > .1.
* Rank by unclipped per-decision DR with cross-fitted, discounted-at-1,
  tabular fitted Q evaluation using checkpoint, displayed code, and action
  as features. Secondary: ordinary PDIS and self-normalized PDIS (here,
  only the terminal reward is nonzero). Compare to the unweighted mean
  trajectory log-likelihood gain on success minus failure, and a
  frozen-model ordinal judge given summarized behavior logs and a lesson.
* Truth: 50 fresh sampled trajectories per candidate, using common
  randomly chosen initial codes for comparability and independent policy
  sampling per lesson. The validation harness pairs these starts with
  the first 50 no-memory log starts to supply the reference labels for
  UpliftMem-style learning. No fresh labels feed DR, IS, the likelihood
  control or the judge. Because the no-memory log supplies no direct
  intervention labels, the uplift baseline is a deliberately
  advantaged live-label baseline: predict paired success differences
  for held-out lessons from fresh observations of the **other** lessons
  using regularized character n-gram kernel regression. Each lesson uses
  the same distribution of starts, so this fits mean paired uplift over
  that distribution rather than predicting a separate value per start.
  Never train on a scored lesson's own outcomes. This is singleton
  set-value regression, not a reproduction of UpliftMem's retrieval policy
  or probe acquisition.
* Use the reviewer's counts and decision rules, not the larger original
  G1 proposal. Kill on a per-lesson ESS below 50, DR rank Spearman below
  0.60, less than +0.15 over either judge or likelihood control, or no
  positive margin over uplift. Gates are on point estimates; present
  percentile 95% CIs separately. Bootstrap the shared behavior corpus
  jointly across lessons, paired fresh rollout slots jointly across
  lessons, and candidate lessons for rank/margin intervals. Refit the
  DR and uplift targets in the trajectory bootstrap and keep duplicates
  in their original cross-fitting groups so they cannot leak across fold
  boundaries. Judge uncertainty is conditional on its one fixed log
  summary and scores; the other methods' trajectory-dependent scores
  are recalculated in each replicate.
