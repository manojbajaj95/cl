# Child: Inhibit a dependency; intervene to explore

Child node (depth 1) · 30 candidate cards (AL2-01–AL2-30) · 5 ranked deeper questions · Ideas only; no experiments run

**Request (Manoj).** Can the techniques behind abliteration teach models new tasks on the fly? The review of [PR #402](https://github.com/manojbajaj95/cl/pull/402) kept two directions at 3 and none at 4: selective dependency inhibition ([AL11](./root-abliteration-learners.md#al11--subtract-a-dependency-edge-not-a-feature) + [AL08](./root-abliteration-learners.md#al08--write-the-exclusion-in-evidence-space)) and intervention-generated teaching data ([AL28](./root-abliteration-learners.md#al28--teach-a-missing-distinction-by-intervening-before-gathering-labels)). Follow-up: “Why can't i do similar approach to promote a behaviour ? rather than doing RL for teaching a behaviour?” The last section develops the positive write in AL28 as a possible alternative to RL.

**Thesis.** The first branch asks whether a rank-1 counter can remove a *use* of a signal while the same source, sink, and coordinate remain useful elsewhere. The second asks whether suppressing a habit *only during sampling* yields verified data that a clean model can learn from better than data gathered by sampling harder. Both can fail independently. A good edit with poor teaching data, or good teaching data from a diffuse intervention, would still separate the claims.

## Is this pursuable? Short answer

- **Selective dependency inhibition (AL11 + AL08).** At a candidate source, read the scalar `s = aᵀh_source`. Immediately before the candidate sink uses its input, add `−λsb` on the nominated sink path; do not project the source or the whole residual. A source carried to a later site costs a tap and state. A sink-local read of an inferred source is a different, cheaper hypothesis and gets its own arm. A rank-1 counter is algebraically a low-rank map from the tapped state; a contribution estimated by patching is causal only relative to the intervention and tested inputs, not proof that the network contains a unique literal edge.
- **Intervene to explore (AL28).** From the same clean checkpoint, generate proposals with a bounded, temporary inhibition on benign task behavior. Keep only verifier-accepted data, discard the sampling edit and its cache, and learn a separate positive write on clean forwards. No teacher or verifier access at serving time. Report pass rate per proposal, support diversity by verified solution class, and held-out gain per total sampling and verification cost after installing only the positive write. Higher pass rate alone is not learning.
- **Promote behavior without RL? Yes, if the contrast captures a behavior that the model can already produce and the intervention makes it more likely on new inputs.** A cheap first update is to read a cue at the relevant decision and write the accepted-minus-rejected direction, or start with pure addition. Deliberately test where that stops working: weak or missing contrast pairs, cases where the positive direction should not fire, and genuinely new behavior not recoverable from the sampled evidence. A forward-only reward-informed update is not generally the policy gradient: a difference of activation means can track a reward–feature covariance, but PPO/GRPO use how changing the policy changes the probabilities of sampled actions and can learn from further rollouts.

**Scope.** Checked the updated [idea ledger](https://github.com/manojbajaj95/cl/blob/24702be248c0389ecb8bfdf2bf5c8d41dca6e8f1/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/24702be248c0389ecb8bfdf2bf5c8d41dca6e8f1/reviews/flood-triage.md). The #402 verdict is in triage; the ledger has no separate #402 entry at that revision. Do not assume sparse damage ([PR #24](https://github.com/manojbajaj95/cl/pull/24)), infer a global edit-capacity limit ([PR #22](https://github.com/manojbajaj95/cl/pull/22)), or skip entropy matching because a proposed signal looks semantic (ledger's [PR #27](https://github.com/manojbajaj95/cl/pull/27) lesson-value control). Work on synthetic benign skills and preserve safety behavior; refusal ablation is a method reference, not a target.

**Shared conventions.** Use a CPU toy with planted structure to debug the assay, then a frozen small model where the shortcut is demonstrated on independent data. Separate nomination, fitting, calibration, and final tests by instance; split exploration tests by problem family or new input values, not by sampling seed. Count edit nomination, all forwards/decodes, verifier calls, parameters, tap/cache state, and active serving latency. Give near-neighbor controls their best site/dose on the same calibration budget, not the proposed method's settings. In every test compare unchanged old tasks and fixed policy sentinels with the relevant edit active; the cards name the additional retention slice. All first tests are proposals.

## Literature check

Named-control positioning and repo review, not a new priority search. Every card inherits the controls for its branch; its cheapest test highlights the comparison most likely to falsify it.

| Line | Already available | What a card here must add |
|---|---|---|
| Erase or steer (A–B) | Arditi-style directional ablation, LEACE, ActAdd (links in [#402](./root-abliteration-learners.md#literature-check)) | Match locality with sink-only versions as well as source-wide ones. Show targeted transfer on crossed cases where preserving a legitimate use matters. |
| Keyed edit or counter (A–B) | ReFT at equal rank, ROME/MEMIT, equal-parameter LoRA trained on the crossed stream, [#400 HL15](https://github.com/manojbajaj95/cl/pull/400) counter-components | Charge the source tap; give a source-aware keyed control the same information. If the win disappears once these methods see the same operands, claim only a cheaper way to fit a counter. |
| Explore and self-train (C–D) | Best-of-N at equal samples and matched total cost; higher-temperature and entropy-matched sampling; [SEAL](https://arxiv.org/abs/2506.10943)-style self-training; [STaR](https://arxiv.org/abs/2203.14465)-style rationale bootstrapping; keep the inhibition as the final edit | Use a common verifier, training budget and positive writer for the sampling comparisons. Report separately equal-proposal and matched-accepted-example results; keep-inhibition is a serving comparator, not part of the cleaned-up learner. |
| Promote without RL (E) | CAA, [ITI](https://arxiv.org/abs/2306.03341), ActAdd; best-of-N distillation including STaR or rejection sampling fine-tuning (RFT); [PPO](https://arxiv.org/abs/1707.06347) and GRPO ([DeepSeekMath](https://arxiv.org/abs/2402.03300)) | Match prompts, verifier, rollout count and initial checkpoint; also report total wall time separately. Include equal-trainable-parameter RL when possible, and a stronger standard RL arm as a reference. Show where the directional update matches RL, where it misfires, and whether extra online rounds change the answer. |

## A · Find a dependency a rank-1 counter can actually isolate

### AL2-01 · Cross the source and sink independently
- **Improvement / assay** (establish whether the claimed problem exists).
- **Mechanism:** Generate cases crossing presence of the nuisance source with whether one of two decisions should use it. Balance answers and cue values. A counter counts as selective only if it fixes misleading use without hurting legitimate use, including legitimate inputs to the edited sink.
- **Nearest prior / gap:** AL02 crossed evidence, LEACE and Arditi ablation; this assay requires legitimate reuse at both the target sink and a second sink, not just a broad neighbor benchmark.
- **Cheapest first test:** Alternate table fields serving as selectors or distractors; test on new table templates. **Kill** the selectivity claim if sink-local LEACE or ActAdd matches all four cells at the same retention.
- **Old-task retention:** True cue selection at the target and the other sink.
- **Risk / likely tie:** A role token may solve the benchmark by itself; include a role-only route with the same state.

### AL2-02 · Fit the counter to a difference of causal responses
- **Primitive** (estimate an edge's effect by changing a source with and without its candidate path available).
- **Mechanism:** On matched inputs, change the source scalar and measure the sink response twice: with its candidate route open and with that route's message held at the reference value. Factor the difference across witnesses into a rank-1 counter. Repeat on a second split before writing.
- **Nearest prior / gap:** Edge patching and ROME/MEMIT; fit a counter to the path-specific response rather than the marginal failure contrast or a target output value.
- **Cheapest first test:** Compare known rank-1 and rank-2 pathways in a toy, then two relay candidates in a small model. **Kill** if the path contrast does not predict held-out write effects better than ordinary activation patching or ReFT.
- **Old-task retention:** Other routes from the source and the same sink with the nominated route held constant.
- **Risk / likely tie:** Holding a route fixed can create unrealistic states; test small in-distribution source swaps and a nuisance-free placebo.

### AL2-03 · Give the editor a remote read and charge for it
- **Improvement / assay** (separate new information from a better fitting rule).
- **Mechanism:** Compare an explicit source tap, a read reconstructed from local sink state, and a local read with a matched irrelevant remote scalar. Match compute and state class where possible; report the tap's footprint separately.
- **Nearest prior / gap:** ReFT and LoRA, plus #400's counters. A remote read makes more information available; it's not evidence that the rank-1 update itself is better.
- **Cheapest first test:** Find two input families with similar sink states but different patched source effects. **Kill** the source-tap case if local ReFT matches or source-aware ReFT gets the same gain at equal total cost.
- **Old-task retention:** Legitimate cases where the tap is present but must not dominate the sink's local evidence.
- **Risk / likely tie:** Similarity in one measured projection does not imply the sink lacks the information.

### AL2-04 · Match the scalar; swap which route supplied it
- **Primitive** (distinguish provenance at the same destination coordinate).
- **Mechanism:** Find matched cases with the same magnitude of a sink coordinate but opposite attribution to a shortcut pathway versus a legitimate one. Fit only the attribution-dependent component of the counter; use independent swaps to check the separation.
- **Nearest prior / gap:** AL08 evidence-space erasure and conditional LEACE. Ask whether the provenance signal does work beyond any gate supplied with the same information.
- **Cheapest first test:** A two-relay toy, then matched examples from AL2-01. **Kill** if a provenance-aware linear ReFT or conditional LEACE reaches the same transfer with no more state.
- **Old-task retention:** Legitimate signal on the very coordinate being corrected, not only on untouched coordinates.
- **Risk / likely tie:** Exact scalar matching can hide other differences; report balance and test with identical input under benign causal swaps.

### AL2-05 · Flat counter versus surviving dose
- **Improvement / assay** (map where local linearity actually supports a rank-1 counter).
- **Mechanism:** Measure response to small source-scalar changes at several naturally occurring magnitudes. Predict the correction at unseen magnitudes from one slope, and compare with an equally budgeted clipped or piecewise counter.
- **Nearest prior / gap:** ActAdd dose sweeps and Arditi-style subtraction; the claim is slope transfer, not finding a best dose.
- **Cheapest first test:** Vary distractor repetition in tables without changing the answer. **Kill** if a tuned constant ActAdd or a two-bin ReFT matches across held-out intensities.
- **Old-task retention:** Strong legitimate cues and weak cues close to the decision boundary.
- **Risk / likely tie:** Repetition changes token positions, not just strength; include matched-length replacement cases.

### AL2-06 · Move the read; keep the sink
- **Primitive** (a write can be rebound to fresh evidence while its destination remains fixed).
- **Mechanism:** Across a schema change that alters how a shortcut is represented, keep the verified sink direction and re-estimate only the source read. Do the inverse under a destination-only change as a falsification arm.
- **Nearest prior / gap:** ROME's key/value factorization and #400's annotated counter-components; require an online revision win when only the read changes, not a stale patch that happens to transfer.
- **Cheapest first test:** Change cue encoding from column color to a symbol with the decision format fixed. **Kill** if refitting both factors or a source-aware rank-1 ReFT takes no more verified examples and causes no more damage.
- **Old-task retention:** Previous cue encoding and legitimate reads at the fixed sink.
- **Risk / likely tie:** The model may reuse the same internal source; verify source change before interpreting rapid adaptation.

### AL2-07 · Recompute the counter on a missing edge
- **Improvement / assay** (negative control for the claim that an edge explains the gain).
- **Mechanism:** Temporarily bypass the proposed nuisance path on a calibration subset while maintaining the legitimate route. A counter targeting that path should lose its marginal benefit; compare unrelated bypasses of similar effect size.
- **Nearest prior / gap:** Causal mediation checks and Arditi-style necessity tests; the null is a targeted path removal rather than setting a feature to zero everywhere.
- **Cheapest first test:** Planted parallel relay and matched controls in a toy; test the nomination on a small model only if the assay discriminates. **Kill** if the counter still helps after path removal, after matching baseline error and headroom.
- **Old-task retention:** Legitimate-route predictions under both counter and bypass, measured separately.
- **Risk / likely tie:** Removing the path can hit an accuracy ceiling; use margin as a secondary readout, not evidence by itself.

### AL2-08 · Discover a relay the source can bypass
- **Primitive** (a diagnosed branching point specifies where a local counter is insufficient).
- **Mechanism:** Test suppressing the proposed path while leaving two other routes active. Use the residual effect of changing the source to distinguish a redundant shortcut route from mistaken localization; admit a second write only if a second path is independently verified.
- **Nearest prior / gap:** Circuit path patching, multi-site ReFT and MEMIT; use the first counter as a diagnostic to decide whether to spend another rank.
- **Cheapest first test:** Mix held-out cases with one versus two relays. **Kill** if residual-effect screening cannot predict when a second write helps beyond the first write's held-out error.
- **Old-task retention:** Routes that share either relay but should never be corrected.
- **Risk / likely tie:** Diffuse effects may admit no reliable pair, consistent with PR #24; do not convert the result into a sparse-edge claim.

## B · Preserve an edge's scope as the learner changes

### AL2-09 · Give scope violations a signed witness
- **Primitive** (one opposite-sign witness can veto the counter on a class of cases without retracting its efficacy witness).
- **Mechanism:** Track causal responses of the candidate path on corrective versus protective examples. Repeat a past counter only if its predicted sign is stable on corrective witnesses and consistent with no harm on protected ones; ask which witness would change the decision.
- **Nearest prior / gap:** AlphaEdit and #400 checked claims; use direction of path influence, not key similarity alone, to update the counter's scope.
- **Cheapest first test:** A task stream in which a formerly spurious cue becomes legitimate for one query class. **Kill** if routed ReFT plus old examples matches revision lag and worst-case retention.
- **Old-task retention:** Corrected examples outside the newly legitimate scope and unaffected old legitimate classes.
- **Risk / likely tie:** A scope bit alone may account for the benefit; give it to every eligible comparator.

### AL2-10 · Discover the smallest local counter that preserves input identity
- **Improvement** (change the fitting objective, not the operation).
- **Mechanism:** Fit two candidates: one minimizing shortcut error and one additionally preserving input-dependent responses to legitimate variations, even when the final label stays constant. Test whether the second constraint protects later use of the sink.
- **Nearest prior / gap:** LEACE, ReFT with auxiliary losses and #400 spillover repair; compare preserving a causal response curve with simply maintaining output logits.
- **Cheapest first test:** Sink selects a field, later composition asks for both its identity and value. **Kill** if output-KL LoRA protects composition just as well at equal examples and parameters.
- **Old-task retention:** Earlier compositions consuming the same sink's output.
- **Risk / likely tie:** Preserved internal responses might be cosmetic; later composition performance is the decision metric.

### AL2-11 · Install an edge counter before a downstream skill arrives
- **Primitive** (use later skill acquisition as a test of endpoint preservation, not just current accuracy).
- **Mechanism:** Make the same initial correction with an edge counter or whole-coordinate erasure, targeting equal current scores. Then teach a new legitimate consumer that needs the preserved source; compare how much new evidence is required.
- **Nearest prior / gap:** #374 future-write checks and ReFT; distinguish preservation of useful source information at an unedited consumer from preserving today's evaluation labels.
- **Cheapest first test:** Eliminate a column-selection shortcut, then add a related table comparison rule. **Kill** if sink-local LEACE, ActAdd or equal-rank LoRA learns the second skill as quickly with matching first-task gain.
- **Old-task retention:** Original correction and all unrelated uses of the source after the second skill.
- **Risk / likely tie:** A synthetic consumer might be constructed to need the signal by definition; test an independently chosen composition.

### AL2-12 · Update a counter from a changed sink response
- **Primitive** (a path-response change triggers revision of the output factor without revising the read).
- **Mechanism:** After an independent benign skills update, probe the same source contrasts at the sink. If reads remain predictive but output effects rotate, retain the read and update only the counter's output factor; stop if both changed.
- **Nearest prior / gap:** ROME/MEMIT factor updates and #400's recompilation; a local probe should predict whether limited evidence can repair one counter after another edit.
- **Cheapest first test:** Install two modest adapters sequentially and conceal which one affects the sink. **Kill** if a fixed counter or full refit matches old- and new-task scores at equal calibration cost.
- **Old-task retention:** Old corrected behavior and the independently added skill, not just base tasks.
- **Risk / likely tie:** Local probes may be cheaper than retraining only when adapter interactions are already mild.

### AL2-13 · Detect a nonlinear collision before merging two counters
- **Primitive** (a pair of counters has a measurable joint scope, not just two independent scopes).
- **Mechanism:** Two counters reading different sources can collide when both operate on the same sink. Measure joint-minus-single effects on witnessed overlaps and use that quantity to choose a scoped joint counter or keep the writes separate.
- **Nearest prior / gap:** #402 AL19 order effects, #400 co-loading and TIES; test a simultaneous nonlinear collision after additive linear updates would predict no problem.
- **Cheapest first test:** Two shortcut sources, one held-out overlap class. **Kill** if routing from the two source scalars or joint equal-rank ReFT matches retention and overlap gain at the same state.
- **Old-task retention:** Both solo corrections and legitimate cases where both sources are present.
- **Risk / likely tie:** Two logits can saturate without a path collision; compare against margin-matched additive responses.

### AL2-14 · Publish a counter's reachable scope, not a global guarantee
- **Improvement / assay** (calibrate when the local edge estimate is outside its support).
- **Mechanism:** Bound use of the counter to observed ranges of source magnitude and sink state. Calibrate a selective coverage/error curve; route uncovered cases to the clean model without silently applying residual subtraction everywhere.
- **Nearest prior / gap:** Conformal selective prediction, ReFT gating and AL31; evaluate the benefit of source-and-sink calibration over either side alone.
- **Cheapest first test:** Shift table schemas and formats separately. **Kill** if a confidence threshold plus equal-parameter LoRA protects the same legitimate uses at equal correction coverage.
- **Old-task retention:** Out-of-support legitimate inputs and in-support unaffected behavior.
- **Risk / likely tie:** Coverage on calibration distributions does not guarantee behavior after an arbitrary shift.

### AL2-15 · Retract an attribution without retracting the correction
- **Primitive** (replace a causal hypothesis while keeping verified task behavior).
- **Mechanism:** If new matched cases disprove the nominated source while confirming the same sink error, rebuild the counter against an alternative source using retained effect witnesses. Do not reuse old source activations as though they were correct evidence.
- **Nearest prior / gap:** AL13 evidence retraction and #400 component replacement; here the labels stay the same while the explanation for where to write changes.
- **Cheapest first test:** Start with two correlated cues, then break their correlation without changing the rule. **Kill** if refitting equal-parameter LoRA or replacing the original counter from scratch costs no more verified examples to recover both roles.
- **Old-task retention:** Valid early corrections and legitimate uses of both candidate cues.
- **Risk / likely tie:** A sufficiently crossed first batch would avoid retraction; measure under a real evidence budget, not contrived missing data.

## C · Change what the model can discover during sampling

### AL2-16 · Separate the sampling edit from the learning write
- **Improvement / assay** (minimum causal test of AL28).
- **Mechanism:** Cross clean versus inhibited sampling with no update versus a shared positive writer. Re-encode all accepted trajectories from scratch on the clean base. Add a serving arm that keeps only the inhibitor and an oracle arm with verifier-approved demonstrations, if available.
- **Nearest prior / gap:** Best-of-N, STaR/SEAL and persistent steering; the sampling edit must improve the positive-write arm when no inhibition survives into serving.
- **Cheapest first test:** One planted arithmetic shortcut and a novel table rule, with held-out problems. **Kill** if the clean, equal-budget best-of-N writer matches downstream gain or the benefit requires keeping the inhibitor.
- **Old-task retention:** Correct uses of the original shortcut after clean restart and after applying only the positive write.
- **Risk / likely tie:** Cached activations or shared generation state could keep the exploration effect; verify reset against the original checkpoint.

### AL2-17 · Find the first branch where inhibition helps
- **Primitive** (a sampling intervention can be scoped to a demonstrated point of premature commitment).
- **Mechanism:** Under equal random seeds, compare inhibition confined to the first decision that commits to a heuristic with equally long windows before and after it. Save accepted trajectories; train the same positive write from each window.
- **Nearest prior / gap:** Selective steering and STaR; the target is to open a verified branch rather than steer every step or diversify all tokens.
- **Cheapest first test:** A two-stage table calculation with a known branch point. **Kill** if after-only or entropy-matched clean sampling yields equally valuable data at equal total tokens.
- **Old-task retention:** Problems where committing to the original heuristic early is correct.
- **Risk / likely tie:** Hand-labeling a branch reveals strategy information; give the same boundary signal to temperature and prompt-based arms.

### AL2-18 · Sample from a targeted branch before spending a verifier call
- **Improvement** (budget allocation using benign learned shortcut effects).
- **Mechanism:** Use a small held-out calibration set to sort prefixes by how often the proposed counter flips the next benign decision without disrupting the prefix. Allocate the intervention only to high-yield prefixes while reserving some clean samples per task.
- **Nearest prior / gap:** Adaptive best-of-N and verifier-assisted search; compare intervention targeting with directing the same verifier budget to high-uncertainty prefixes.
- **Cheapest first test:** A mix of easy problems and shortcut traps. **Kill** if entropy- or confidence-based allocation gets equal held-out post-write gain at equal samples and verifier cost.
- **Old-task retention:** Easy old problems and valid shortcut cases excluded by targeting.
- **Risk / likely tie:** Prefix screening may cost more than it saves once model forwards are counted.

### AL2-19 · Discover new solution classes, not just more passes
- **Primitive** (treat a verifier-backed solution class as the unit of exploration evidence).
- **Mechanism:** For tasks with observable intermediate operations, canonicalize accepted rollouts by execution trace up to equivalent reorderings. Count novel classes found per proposal, then train on class-matched data and on each arm's full yield.
- **Nearest prior / gap:** Diverse decoding and STaR; distinguishes finding new teachable strategies from generating more paraphrases of an easy solution.
- **Cheapest first test:** Arithmetic problems with two exact solution families. **Kill** if the inhibited sampler finds no more useful classes than temperature or best-of-N, or class coverage doesn't predict held-out learning at matched passes.
- **Old-task retention:** Existing solution methods on tasks where alternatives do not apply.
- **Risk / likely tie:** A canonicalizer may encode the target strategy; use an executable evaluator shared across arms.

### AL2-20 · Teach only the verified fork
- **Primitive** (the exploration output is a contrast at a local choice, rather than an entire edited trajectory).
- **Mechanism:** Pair two continuations from the same prefix with one verified and one failing outcome. Re-execute the fork from the clean model with both actions forced to verify the contrast. Fit a positive write at the shared choice against the action preference label, not the identical pre-fork states; compare against whole-trajectory distillation.
- **Nearest prior / gap:** STaR/RFT and matched prefix preference optimization; see also AL06 reward twins. The claim is that the inhibition supplies *useful fork evidence* that a clean sampler rarely supplies.
- **Cheapest first test:** Two-step symbolic tasks with a verifier for both completions. **Kill** if clean fork pairs or full-rollout RFT produce equal transfer at the same number of verified proposals and clean-forward tokens.
- **Old-task retention:** Previously correct choices under the same prefix type with a different goal.
- **Risk / likely tie:** Final reward may reflect later repair, not the fork; check in tasks with an intermediate verifier.

## D · Check whether the evidence remains useful after the intervention disappears

### AL2-21 · Allow the data to survive, but not their activation coordinates
- **Improvement / assay** (detect dependence on the exploration-only representation).
- **Mechanism:** Learn from the same accepted rollouts using clean activations, inhibited activations, or text-only supervision. Compare clean serving for every writer; a clean writer should retain gains without the sampling trajectory's internal state.
- **Nearest prior / gap:** Off-policy representation mismatch and STaR; isolates which part of the teaching signal is portable to the clean activation space.
- **Cheapest first test:** Re-encode a fixed accepted set at two suppression doses. **Kill** if only inhibited-state training works, or if text-only RFT always matches the clean directional writer.
- **Old-task retention:** Behavior near the suppressed shortcut, with neither exploration state nor filters loaded.
- **Risk / likely tie:** Clean teacher forcing can hide failures under free generation; held-out free decoding is the primary test.

### AL2-22 · Hold pass count fixed and trade one verified example at a time
- **Improvement / assay** (estimate how much an intervention-specific example is worth).
- **Mechanism:** Match accepted sets by difficulty and length. Replace one clean example at a time with an inhibited-sampling example from the same stratum; use multiple fixed subsamples to test whether downstream gains are about composition rather than sample count.
- **Nearest prior / gap:** Dataset ablation in SEAL/STaR-style self-training; matched-yield controls disentangle quality from better pass throughput.
- **Cheapest first test:** 16 accepted rollouts per arm on a small reasoning stream. **Kill** the quality claim if replacement gives no reproducible gain over random clean swaps, even if yield rises.
- **Old-task retention:** Previous skills aligned with both replacement groups, including ones absent from the current support set.
- **Risk / likely tie:** Matching on a post-treatment proxy may hide causal effects; report both matched and fixed-proposal estimates.

### AL2-23 · Detect verifier artifacts before they become a positive direction
- **Improvement** (negative control against training on incidental approval correlates).
- **Mechanism:** Verify executable behavior, then strip formatting cues and recheck accepted trajectories with an independent verifier or alternate problem rendering. Compare a writer trained on original accepted data with a writer trained on reverified examples.
- **Nearest prior / gap:** Reward hacking audits and verifier bootstrapping; the key question is whether inhibition preferentially generates superficial passes.
- **Cheapest first test:** Synthetic tasks with exact execution and a deliberately weaker format-sensitive first verifier. **Kill** if an apparent intervention advantage disappears under independent evaluation and clean holdouts.
- **Old-task retention:** Correct older solutions in alternate formats, scored by the stronger verifier.
- **Risk / likely tie:** Extra verification may favor an arm via different rejection counts; report calls and rerun all arms through the same checks.

### AL2-24 · Use a clean shadow to test discovery, not impossibility
- **Primitive** (classify a result as improved reachability when a verified trajectory is rare under an explicit clean sampling budget).
- **Mechanism:** Estimate the clean rate for the *solution class*, not the exact output string, with independent samples. Track whether temporary inhibition raises that rate and the later positive write keeps it raised on unseen inputs without the edit.
- **Nearest prior / gap:** Best-of-N coverage and AL28; low clean pass rates bound practical discovery cost, not the existence of latent capability.
- **Cheapest first test:** An uncommon exact strategy with measurable verifier probability. **Kill** if a tuned clean sampler at matched cost covers the same classes and yields the same held-out post-write gain.
- **Old-task retention:** Frequent valid strategies and tasks where the explored strategy is inapplicable.
- **Risk / likely tie:** Zero clean hits is only an upper bound on frequency; report uncertainty rather than claiming the unedited model cannot produce it.

### AL2-25 · Check that promotion isn't secretly restoring the inhibition
- **Primitive** (distinguish teaching a valid alternative from learning the exploration counter by proxy).
- **Mechanism:** At test time independently vary shortcut presence and the need for the newly taught operation. Compare a positive writer fit to accepted data with a direct inhibition arm and an equally sized STaR-style writer trained on clean accepted data.
- **Nearest prior / gap:** AL05 remove/add factorial and #402 AL28; the new evidence is performance when the shortcut is absent and performance where the shortcut should remain useful.
- **Cheapest first test:** Four crossed cells on a fresh table rule. **Kill** the positive-learning claim if gains exist only when the shortcut is present, or the write replicates the inhibitor's failure on legitimate shortcut cases.
- **Old-task retention:** Original heuristic when valid and the new rule when it should not apply.
- **Risk / likely tie:** A positive write can indirectly reduce shortcut probability for good reasons; infer proxy inhibition from the crossed behavioral pattern, not vector angle.

## E · Promote a behavior without running RL

### AL2-26 · One-shot reward contrast
- **Improvement** (a forward-only, reward-informed step; contrastive steering is already known).
- **Mechanism:** For each prompt with verified successes and failures, collect aligned clean-base activations and average the within-prompt accepted-minus-rejected contrast. Add the direction at the chosen site, or write it as the output factor of a rank-1 map whose input factor detects the benign task context. Learn dose on calibration only.
- **Nearest prior / gap:** CAA, ITI and ActAdd already promote behavior; the fair question is whether a verifier-derived contrast and a shared evidence budget make a one-shot update preferable to RL for this task.
- **Cheapest first test:** Increase exact fraction simplification when requested. **Kill** the proposed RL substitute if PPO/GRPO or best-of-N RFT gives better gain at the same samples and retention, or tuned CAA matches it with less machinery.
- **Old-task retention:** Unrelated arithmetic and answers explicitly requested in unsimplified form.
- **Risk / likely tie:** Identical prefixes have identical clean activations before a sampled choice; use aligned distinct prefixes or teacher-forced branch states to nominate a direction, then test causally whether applying it *before* the choice helps. A post-answer contrast alone may only read success.

### AL2-27 · Draw the boundary: latent routine versus new skill
- **Improvement / assay** (locate where direction updates match RL rather than claiming equivalence).
- **Mechanism:** Vary initial solution coverage across a familiar requested routine, a new composition of familiar operations, and a newly assigned operator rule. Measure coverage against clean and inhibited sampling; run a matched-samples comparison with one-shot and repeated PPO/GRPO, CAA/ITI/ActAdd and STaR/RFT. Keep verifier information identical and include a demonstration ceiling to diagnose no-signal regimes.
- **Nearest prior / gap:** RLVR, reward-conditioned steering and best-of-N distillation all improve sampled behavior; distinguish reachable routine promotion from generalization on a rule absent from support as an explicit instruction.
- **Cheapest first test:** A known rounding routine, an unseen combination, and a newly assigned symbol operator tested on unseen arguments. **Kill** a broad RL-replacement claim if direction updates match RL only on the known routine or fail to transfer on the novel rule. If no arm ever gets reward, label the task uninformative about relative learning.
- **Old-task retention:** Old conventions that conflict with the new one, scored separately and retained under their original requests.
- **Risk / likely tie:** Novel composition does not prove a novel internal algorithm; define novelty at the task level and measure the base's verified coverage.

### AL2-28 · Promote only when the behavior was asked for
- **Primitive** (separate evidence about when to act from evidence about what to amplify).
- **Mechanism:** Learn a read factor from matched prompts where a behavior is requested versus counter-requested, and the output factor from accepted/rejected trajectories *within* the requested setting. Compare this factored positive write to global addition and to a gated baseline given the very same read.
- **Nearest prior / gap:** Conditional CAA/ITI, ActAdd and rank-1 ReFT; what might be new is independent few-shot revision of the trigger without changing the promoted behavior learned from reward.
- **Cheapest first test:** Promote a verbose derivation only when requested, then change how the request is signaled without changing correct derivations. **Kill** if a tuned gate on CAA or equal-samples PPO/GRPO matches revision cost and false activation.
- **Old-task retention:** Concise answers, exact-format outputs and older contexts where derivations are still wanted.
- **Risk / likely tie:** An obvious binary router may solve scope with fewer examples; give that router the same calibration budget.

### AL2-29 · Ask when the contrast even points in the reward-improving direction
- **Improvement / assay** (a minimal check of the “one-shot RL step” analogy).
- **Mechanism:** In a frozen two-action score model with a linear edit parameter, compare the feature–reward covariance with the score-function gradient. Binary acceptance gives `Cov(r,h) = p(1−p)(μ_accept−μ_reject)`; it matches a gradient up to scaling only in special cases where the centered feature is the policy score for the edited parameter. Check small-step reward and then test whether the agreement breaks with delayed rewards or nonlinear hidden-state interventions.
- **Nearest prior / gap:** REINFORCE/PPO/GRPO advantages and CAA; the assay tests the missing link between observed feature contrast and the effect of intervening on that feature.
- **Cheapest first test:** CPU contextual bandit with a planted scored feature and a correlated but inert one, followed by a two-step task with delayed reward. **Kill** the gradient-surrogate claim if direction updates do not agree in the scored-feature regime or remain predictably misaligned after weighting and matched scaling.
- **Old-task retention:** Separate contexts where the rewarded feature is irrelevant or where its preferred action has the opposite sign.
- **Risk / likely tie:** Agreement in the planted linear case may be true by construction; only generalization beyond that calibration supports the broader analogy.

### AL2-30 · Stop when promotion has no trustworthy pairs
- **Improvement** (use a measurable boundary to choose between steering, collecting data and RL).
- **Mechanism:** Track the number of prompts with representative verified success/failure pairs and the split-half effect of the resulting write. Do not reuse repeated paraphrases as independent evidence. When pairs are missing or uninformative, use the same budget to seek new examples or compare to a multi-round RL arm; don't manufacture a direction from an unbalanced set.
- **Nearest prior / gap:** Active learning, ICL gating, ITI calibration, STaR/RFT; this is an escalation rule for choosing an update method, not a new optimizer.
- **Cheapest first test:** A graded stream from ample pairs to no positive examples under a fixed budget. **Kill** if pair-based escalation has no better gain/retention–cost tradeoff than always-best-of-N distillation or always-equal-budget PPO/GRPO. A zero-reward region may require new supervision for both.
- **Old-task retention:** Previous promoted behaviors and opposite-context examples after each escalation decision.
- **Risk / likely tie:** Pair count can proxy for task difficulty; compare to a simple initial pass-rate rule.

## Ranked deeper questions

1. **Does a source-keyed counter actually remove one use, rather than a coordinate or a convenient proxy (AL2-01–AL2-04, AL2-07)?** Start by matching sink magnitude with different provenance, then remove the candidate path as a falsification test. Beat sink-local ablation/LEACE and source-aware ReFT/LoRA on legitimate reuse, or call it a keyed intervention rather than a demonstrated edge write.
2. **Does temporary inhibition discover better teaching evidence, or just raise the pass rate (AL2-16, AL2-19–AL2-22, AL2-24)?** Use both equal-proposal and matched-accepted-example comparisons to best-of-N, temperature, SEAL and STaR. The decisive outcome is learning from a clean restart on held-out problems, with no exploration edit or state carried into serving.
3. **When can a directional update replace RL (AL2-26–AL2-30)?** Match verifier budget and rollouts from the same base on a latent routine, new composition and newly assigned rule. Compare PPO/GRPO, CAA/ITI/ActAdd and best-of-N distillation. Return a boundary in initial coverage and scope error, not a blanket win on tasks all arms already know.
4. **Is the positive write learning the alternative, or relearning inhibition (AL2-20, AL2-21, AL2-25, AL2-28)?** Test independently whether the task calls for the alternative and whether the shortcut is present. If improvement requires the shortcut to be present or hurts its legitimate use, it is not enough to call the write teaching.
5. **Does the edge remain a better unit of revision after another skill is installed (AL2-06, AL2-09, AL2-11–AL2-15)?** Change a source encoding or a sink response independently. Compare selective factor reuse with #400 counters, ROME/MEMIT and full matched-rank refits; keep the idea only if reuse reduces revision evidence at matched retention.
