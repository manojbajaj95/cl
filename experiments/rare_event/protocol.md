# Rare-event distillation pilot protocol

Frozen before final seeds on 2026-11-24. Hypothesis: weighted splitting from a
pre-fault checkpoint increases the coverage of old recovery states and thereby
retains the old recovery better than same-budget alternatives.

1. **Environment.** The prompt names a routine warehouse job (scan or move).
   Qwen samples route A/B from its two legal next-token logits. Only then does a
   latent checkpoint indicate high load, at 2.5% or 7.5% depending on job family.
   A fresh continuation from high load yields a paper jam with 2% probability.
   Thus the old jam rate under ordinary prompts is exactly 0.1% in expectation.
   Warehouse X uses C for ordinary operation and D for jam recovery. Later, warehouse
   Y (revealed in the tool response) uses D on busy-but-ready and C on other
   statuses, including its common jams (18% of rollouts). The route policy is fixed.
2. **Model and stream.** Qwen2.5-0.5B base with a rank-one update of the C/D
   output rows, leaving the full transformer and A/B logits unchanged. Fit X
   on 262,144 natural rollouts; retain these observed prefixes and outcomes.
   Adapt to Y for 512 steps of 32 rollouts with hard command labels. Start every
   arm at the same X checkpoint and use the same Y stream per seed.
3. **Replay.** Each replay arm samples eight old tails per step. A tail is charged
   as one rollout including any reused prefix. It gets one frozen previous-student
   teacher distribution at the terminal C/D position (one action token with two
   logits), and the loss is exact reverse KL over those actions. Initial route
   tokens and tool observations receive no teacher supervision in any arm.
   Root actions and live simulator transitions are additionally counted.
4. **Samplers.** MOPD-style is live replay from uniform old prompts, with ordinary
   KL weights. A tilted MOPD variant is an objective-matched control. Uniform
   replay picks one of root, pre-status checkpoint or post-status prefix
   uniformly; at non-root depths the prefix is from a uniformly chosen archived
   trace. Prompt upsampling samples job families proportional to known jam
   frequency. Splitting spends half the rollouts on fresh roots and half on
   groups of four independent continuations from a sampled high-load checkpoint.
   No branch can see whether its next tool call will yield a jam. Direct terminal
   replay is an extra control: half fresh roots, half replay of known archived
   jam histories, sampled uniformly with replacement. No collection cost is
   displaced to a separate per-arm teacher or search.
5. **Weights.** Except ordinary MOPD, the common replay objective has distribution
   proportional to natural terminal-state occupancy times 100 on jams, 1
   otherwise. Divide that target density by the sampler's marginal proposal
   density, computed with the fixed simulator kernel and archive frequencies.
   Scale all replay losses by 0.25. This is an oracle-informed sampler pilot,
   not a claim about learning risk scores or estimating densities from pixels/text.
6. **Evaluation.** Seeds 421, 422, 423 are independent paired old/new streams.
   Measure exact expected sampled-action success over both possible routes and
   each relevant status on 24 unseen old/new prompts (disjoint objects and
   numbers). Evaluate X before adaptation and then X jam, X common, Y non-jam and
   Y jam after adaptation. Use untruncated two-sided 95% Student-t intervals
   across seed means and paired splitting-minus-control differences; no episode
   is a replicate. Require mean pre-shift X jam success of at least 80% and
   at least 10 percentage points of X jam forgetting without replay, with at
   least 80% mean Y success in both cohorts without replay. Otherwise the
   experiment is invalid. Keep only if the paired old-jam lower bound is above
   zero against every control, with no negative old-common point effect and no
   old-common lower bound below −1 percentage point. Also require at least 80%
   mean split success in each Y cohort. Failing any keep criterion kills this
   pilot, not the mechanism in all possible environments.

The adaptation length and replay weight used a separate development seed (17):
512 steps was the shortest tested length with both old-jam forgetting and new-jam
learning in the no-replay and split arms at the shared 0.25 replay scale. Final
seed results are not used for tuning.
