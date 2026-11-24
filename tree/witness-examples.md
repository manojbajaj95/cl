# Witness examples: teach today so tomorrow can stop reading the teacher

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Training readers](training-readers.md) ([PR #161](https://github.com/manojbajaj95/cl/pull/161)), cards 9 and 12. **Review seed:** [Flood triage row 258](https://github.com/manojbajaj95/cl/blob/ea42dfb30b26a22d5badf14f19e0c987f6047976/reviews/flood-triage.md#L258), two score-3 ideas: replace a shared Fisher anchor or teacher with a few synthetic examples that reproduce its corrective update over reachable future states; choose today's data so a scheduled future refresh no longer needs the old teacher.

## Is a learned stand-in for future training dependence a new primitive?

Not by itself. A tiny dataset can already stand in for a much larger source of updates; synthetic replay, cached targets and functional summaries can already avoid querying a teacher on stored inputs. Anticipating interference when picking data is also established. The **conditional candidate** is a *scoped, learned substitution for a future training read*: specify which continuations the source supports, synthesize a stand-in or teach the learner to need none, and test whether that makes the source genuinely reclaimable while preserving both old behavior and permitted new learning. It is a primitive only if this contract lets us construct, verify or combine useful substitutions that gradient/trajectory condensation and ordinary look-ahead data selection plus exact reader retirement cannot deliver at the same cost.

- **Replace the read (witness buffer).** Hold the continuation interface fixed: state includes weights, optimizer slots and clocks, normalization and replay/sampler state wherever relevant. Compare the full one-step transition with the source to the transition with the witness on the same state, new batch and coupled randomness. In SGD a gradient bound can suffice locally; for Adam, matching the immediate weight delta without matching its future-relevant slots can fail. Bound error on states reached by **either** arm or prove an invariant tube that contains the replacement rollout; fitting only the teacher's path is circular. An exact transition match on a closed reachable set composes by induction; approximate matches do not automatically compose. Even a faithful replica of a bad teacher need not retain A.
- **Eliminate the read (today's data).** Choose labeled examples from today's allowed pool while the teacher is available for selection; keep labels, counts, current loss and compute fixed in the main comparison. At the cut, retire the source and run the predeclared later batches, optimizer, step count, learning rates and non-teacher losses unchanged; the teacher loss alone is omitted, not replaced by a lookup, metadata or a hidden extra refresh. Success is behavioral over the continuation, not pointwise equality of updates. Score a data-only arm separately from one using synthetic data or retained targets. First show the original selection actually needs the live teacher under that same schedule; otherwise no dependence was removed.
- **Discharge the obligation.** Scope the evidence to source version, state region, batch/optimizer family and horizon. Keep teacher queries and exact transition checks on the build/evaluation side of the cut only; oracle arms have separate storage and never feed the replacement. Reserve and drain queued old-version jobs, disable future source accesses, then actually overwrite the released region with useful B state. Audit aliases and external fallback/cache reads. Outside-scope continuations require new admission; report refusals rather than silently shrinking the task. A held-out pass is evidence, not a certificate for untested in-scope states.

**Paper case.** For linear least squares and a positive semidefinite anchor penalty `½(θ−a)ᵀF(θ−a)`, let `F = Σᵢ λᵢuᵢuᵢᵀ` and store `xᵢ = √λᵢuᵢ, yᵢ = xᵢᵀa` under a summed squared loss with a factor of ½. Its gradient is exactly `F(θ−a)`. On a full-dimensional open set, fewer than `rank(F)` scalar linear examples cannot match it: their Hessians sum to a matrix of at most that rank. This is a factorization, not a discovery or a byte win over storing the factor and its projected target. If all reachable weights lie on a line, only a restriction of that affine gradient has to match; a newly admitted batch can leave that line and invalidate the cheaper representation. In a complementary teacher case, two old teachers agree on all routine current examples but disagree on a counterfactual relation. If today's candidate pool and every permitted pre-cut signal are identical between the two worlds, the same data-only selector cannot choose correctly in both. Add a legitimately labeled separating example; ask whether it still changes the **post-refresh** answer when pre-cut A scores and per-item margins are matched.

## Prior-art screen and common CPU controls

- **Condensed and selected data:** [Dataset Condensation with Gradient Matching](https://arxiv.org/abs/2006.05929), [Matching Training Trajectories (MTT)](https://arxiv.org/abs/2203.11932), [GCR gradient coresets](https://arxiv.org/abs/2111.11210) and [SSD stream condensation](https://arxiv.org/abs/2305.16645) already optimize a small set for its training effect. [Hybrid Memory Replay](https://arxiv.org/abs/2410.15372) distills from historical checkpoint windows and mixes real with synthetic data; [Data-Distill-Net](https://arxiv.org/abs/2505.20135) learns replay targets. Give these baselines the same future branches, source access and fitting budget, not merely an off-the-shelf past-only trajectory.
- **Anchor/teacher substitutes:** [EWC](https://arxiv.org/abs/1612.00796) preserves weights with a Fisher-weighted quadratic; [FRCL](https://arxiv.org/abs/1901.11356) remembers old functions at inducing points and [FROMP](https://proceedings.neurips.cc/paper_files/paper/2020/file/2f3bbb9730639e9ea48f309d9a79ff01-Paper.pdf) uses memorable past examples for functional regularization. Small functional evidence constraining future training is not new. [LwF](https://arxiv.org/abs/1606.09282) uses old outputs on new inputs, [DER](https://arxiv.org/abs/2004.07211) caches dark targets, [deep generative replay](https://arxiv.org/abs/1705.08690) substitutes generated experience, and [DeepInversion](https://arxiv.org/abs/1912.08795) synthesizes inputs from a model without its data. Compare offline inversion plus cached outputs, not just a live teacher. [Teacher-free KD via label smoothing](https://arxiv.org/abs/1909.11723) motivates a smoothing control, not a way to recover distinctions absent from all allowed signals.
- **Anticipation and oversight:** [HAL](https://arxiv.org/abs/2002.08165) learns input anchors against simulated interference, [MER](https://arxiv.org/abs/1810.11910) aims to maximize transfer and minimize interference, and [Premonition](https://arxiv.org/abs/2403.07356) uses generated data to prepare for future visual tasks. [Future-edit cost](future-edit-cost.md) and [data-only edit cost](data-only-edit-cost.md) already ask which training data makes later intervention cheaper. The distinct endpoint here is the *disappearance of a specific future source read*, with no replacement data at refresh in the data-only arm. This web and repository screen is provisional, not novelty clearance.
- **Ledger gates:** The [reviewer's idea ledger](https://github.com/manojbajaj95/cl/blob/ea42dfb30b26a22d5badf14f19e0c987f6047976/reviews/idea-ledger.md) found self-QA no better than teacher QA on the same questions, coded functional syndromes did not beat dense sketches or replay, and A3 failed its margin-vs-scale test. Do not assume useful sparsity, credit who generated the examples, or mistake bigger margins for learning a missing distinction. Stacked ideas must beat the best stacked parts, with the same verifier, retirement planner and access to data.
- **Shared protocol:** Propose exhaustive tiny systems first, then a CPU MLP where reachable gradients rotate off the fitted region. Reserve fit, admission-check and final-test continuation splits by whole task order or stream family, not by adjacent checkpoints. Hold out ordinary old tasks A/C from all three design and calibration activities; report each on independent old data against its acquisition reference, pre-cut, at visible prefixes, after each admitted refresh and after reuse, without a recovery pass. Report rare slices separately. Match held-out B progress (or report no feasible match); when comparing selectors also check initial per-item margins, loss scale/temperature and answer priors. Report worst and typical post-cut retention, full rollout and correction error where claimed, in-scope failures separately from out-of-scope refusals, and usable reclaimed bytes. Count persistent and peak bytes (including synthetic precision, labels, slots, decoder, validation and overlap), source queries, build and refresh compute, and new learning time. Use live-source oracle and same-schedule no-source ablation, equal-byte low-rank Fisher, raw rehearsal, cached logits, gradient/trajectory condensation and the strongest appropriate look-ahead or functional baseline. P denotes a conditional primitive candidate; I denotes an improvement or audit.

## Idea cards

### Replace the update, not the old model

#### 1. Compile an anchor on the reachable span (I)
- **Mechanism:** Fit examples to the anchor's affine gradient on the affine span of reachable states, keeping output components normal to the span when the learner can actually update them.
- **Novelty vs nearest prior art:** EWC factorization and gradient matching already do the algebra; the audit asks when a continuation restriction buys anything beyond a restricted linear operator.
- **Cheapest first test:** Enumerate linear B gradients on a line, then allow a held-out branch that tilts the reachable span. Compare rank-exact factors, same-byte low-rank Fisher, raw rehearsal and gradient-matched examples.
- **Old-task retention check:** After reuse, score ordinary A/C along the line and on the newly admitted tilted branch; the previous certificate cannot cover that branch.

#### 2. Fit a buffer on both sides of a nonlinear boundary (P)
- **Mechanism:** Alternate witness fitting with search for reachable states where the witness and source disagree on the direction of the next correction; search replacement as well as source rollouts, and store the resulting fixed buffer.
- **Novelty vs nearest prior art:** HAL and MTT already anticipate parameter movement. The claim is an update substitute that closes its own reachable region; compare branch-matched MTT plus the same counterexample search and exact retirement.
- **Cheapest first test:** Enumerate short B batch sequences in a two-unit ReLU learner where the replacement can cross an activation threshold. Freeze before scoring withheld sequences and record whether the first correction error predicts later failure.
- **Old-task retention check:** Score A/C after the first threshold crossing and the final refresh, including paths the live anchor never takes.

#### 3. Preserve an optimizer's delayed response (I)
- **Mechanism:** Fit witnesses to future-relevant moment updates as well as immediate weight changes, using paired starts with equal weights but unequal moment histories.
- **Novelty vs nearest prior art:** MTT and [momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) motivate full-state matching; the witness form is an engineering test, not a new kind of optimizer memory.
- **Cheapest first test:** In scalar Adam, select gradients with nearly equal first normalized steps but differing magnitudes, then apply a common second batch. Compare delta-only fitting, full-state trajectory matching and equal-byte quantized anchors.
- **Old-task retention check:** Measure A/C after both steps and after delayed moment effects, not just at the first weight match.

#### 4. Compile counterfactual teacher responses, not logits (P)
- **Mechanism:** Use the live teacher at build time to label pairs that differ in a single nuisance feature. Optimize a few fixed soft-labeled points to reproduce its corrective update on later augmentations, without querying it on those augmentations at refresh.
- **Novelty vs nearest prior art:** DeepInversion plus DER already supplies synthetic cached targets. The conditional operation is substitution across held-out transformations with a declared update envelope, not better fidelity on stored inputs.
- **Cheapest first test:** Build on two binary nuisance flips and hold out their composition. Compare same-byte inversion plus cached targets, augmentation-aware FRCL and branch-matched MTT, all with the same teacher queries.
- **Old-task retention check:** Check ordinary A/C and the intended answer flip on unseen transformed inputs after B and teacher-free refresh; a temperature-only control must not tie the flip.

#### 5. Match the update noise, not just the mean (I)
- **Mechanism:** Give the tiny buffer a fixed, priced sampling law that matches the source's conditional correction covariance where random corrections can push the learner between basins.
- **Novelty vs nearest prior art:** Stochastic gradient and trajectory matching are the main controls. This is stronger fidelity at finite batches, not a new memory form.
- **Cheapest first test:** Enumerate one-example refresh draws in a double-well toy with matched mean and different variance. Compare mean matching, bootstrapped raw replay and trajectory condensation trained over the same stochastic paths.
- **Old-task retention check:** Check the fraction of streams below the ordinary A/C floors and worst-prefix loss, not only the mean.

#### 6. Test whether static data can express the correction (I)
- **Mechanism:** Check the line integral of the source's **raw additive gradient** around reachable state loops before fitting examples. A nonzero loop integral on a smooth fixed-weight-parameter region rules out exact matching by a fixed differentiable scalar loss there.
- **Novelty vs nearest prior art:** The conservative-field condition is elementary; the audit stops a condensation problem from silently allowing state-dependent routing or a different optimizer to rescue an impossible fixed-buffer claim.
- **Cheapest first test:** Use a two-coordinate source whose sample weights depend on the current parameters but are detached; compare a conservative control and a rule with nonzero circulation. Price a state-conditional cache as a distinct higher-flexibility arm.
- **Old-task retention check:** Execute both loop orders after reuse, testing ordinary A/C and whether approximation error matters for the floors rather than assuming impossibility of exact matching implies forgetting.

#### 7. Carry only the corrections that can reach old behavior (P)
- **Mechanism:** Allocate witness capacity to directions whose errors can propagate to future old-task outputs; discard a direction only if a bound covers its downstream effect through every admitted prefix.
- **Novelty vs nearest prior art:** FRCL/FROMP and [GPM](https://arxiv.org/abs/2103.09762) protect function or gradient subspaces; the proposed object is equivalence up to a checked future behavioral quotient, not current Jacobian sparsity.
- **Cheapest first test:** In a two-layer learner, use B to rotate an initially silent direction into a downstream consumer. Compare next-step Jacobian matching, rollout-weighted MTT and a direct dense response sketch; allow the method to abstain if the bound is loose.
- **Old-task retention check:** Score normal A/C after the rotation and throughout rollout; certify no downstream-safe class merely from a flat initial readout.

### Make today's data eliminate the refresh read

#### 8. Buy a separating example, not a higher margin (P)
- **Mechanism:** Select today's labeled examples where alternative hypotheses fit ordinary current data but predict different old skills after a fixed teacher-free refresh.
- **Novelty vs nearest prior art:** Teaching-set selection and HAL already choose informative examples. The candidate operation targets a causal dependence: pre-cut behavior can tie while only one selection removes the need for the old teacher.
- **Cheapest first test:** Use two rules confounded on routine examples and disentangled by a current labeled crossover. Compare random, balanced, gradient-matched and direct look-ahead subsets at equal counts and pre-cut margins; require the live teacher to rescue the ordinary subset.
- **Old-task retention check:** After the identical refresh schedule and physical reuse, score A/C overall and correct rule flips on withheld crossovers with matched priors.

#### 9. Teach a future refresh to commute with an old skill (P)
- **Mechanism:** Select current examples that encourage the learner to separate a stable computation from a changing nuisance, so either of two legal refresh orders retains the computation without teacher correction.
- **Novelty vs nearest prior art:** MER and future-edit cost already target compatible updates. The claim is a data-only removal of one read for both orders, beyond direct optimization of expected post-refresh retention.
- **Cheapest first test:** Enumerate equal-size subsets of a factorized Boolean stream. Give all selectors the same current labels and two fit orders, then withhold reversed or interleaved orders within the declared family. Compare bilevel selection on matched rollouts.
- **Old-task retention check:** Score A/C after each order prefix and after the second refresh, including an old conjunction unseen in current training.

#### 10. Place today's examples on tomorrow's reachable mistakes (I)
- **Mechanism:** While the source still exists, forecast where a fixed future teacher-free refresh first diverges; choose today’s real examples that correct that mistake before it occurs.
- **Novelty vs nearest prior art:** HAL, [MIR](https://arxiv.org/abs/1908.04742) and Premonition already target future interference or changes. This is a stricter timing/data-access comparison, not a new look-ahead optimizer.
- **Cheapest first test:** Simulate two short CPU refresh branches. Compare ordinary uncertainty, current gradient matching and look-ahead validation selection with identical query budgets and counts; hold out whole task orders.
- **Old-task retention check:** Check ordinary A/C at the first predicted failure and after reuse, showing the error was prevented rather than postponed beyond one checkpoint.

#### 11. Teach under one teacher; retire a second reader of the same skill (P)
- **Mechanism:** Select ordinary examples using one disclosed read contract and test if a separate refresh job with an independently defined teacher query can also proceed without its source.
- **Novelty vs nearest prior art:** LwF, multi-task distillation and [room-making writes (PR #160)](https://github.com/manojbajaj95/cl/pull/160) already transfer to multiple consumers. The claim is that a selection learnt for one obligation can establish another one without its data or teacher queries during fitting.
- **Cheapest first test:** Use two refresh heads sharing a parity feature, with independent nuisance shifts. Admit the second only after a blinded test; compare joint look-ahead as a disclosed ceiling and matching on the first reader's gradients as a fair control.
- **Old-task retention check:** Overwrite sources only for jobs that pass; score ordinary A/C after both original refresh programs (minus their teacher losses), including a counterexample where the second head needs a different feature.

#### 12. Ask how many future distinctions today's pool can teach (I)
- **Mechanism:** Partition old teachers by their agreement on admitted pre-cut signals. Estimate the cheapest separating labeled subset, or mark an equivalence class that requires keeping some old evidence.
- **Novelty vs nearest prior art:** This is version-space identifiability and teaching dimension applied to source retirement, an impossibility audit rather than a training primitive.
- **Cheapest first test:** Enumerate eight Boolean teachers and restrict the selector's observations, including any oracle queries and original weights. Allow candidate examples in one regime and withhold all separators in another; compare exhaustive query selection and direct cached distinguishing bits.
- **Old-task retention check:** Score ordinary A/C across the indistinguishable worlds after refresh; report whether preserved source bytes, rather than a lucky world, explain passing.

#### 13. Learn a stable feature without buying more exposure (I)
- **Mechanism:** Hold the current example multiset fixed and order its separating cases just before interference would otherwise make the future refresh rely on the old teacher.
- **Novelty vs nearest prior art:** Curriculum and future-edit-cost methods already reorder data. This asks whether timing alone moves a read contract, with no novelty claim for scheduling itself.
- **Cheapest first test:** Enumerate permutations of a short two-rule acquisition stream, with fixed optimizer and later schedule. Compare shuffled, easy-first, gradient-interference and exact rollout-selected orders; include a state-reset diagnostic for slot-only effects.
- **Old-task retention check:** Check ordinary A/C after the same later teacher-free refresh and after another B segment; compare margin-matched acquisition states.

#### 14. Spend examples to make a future annotation channel redundant (P)
- **Mechanism:** Select a set of current labeled crosses so the learner can infer the old teacher's correction from a feature already present in every permitted future batch, without receiving that teacher's soft labels later.
- **Novelty vs nearest prior art:** Invariant learning and the [crossed-evidence node](crossed-evidence.md) already disentangle features. The claim concerns which **training input channel** becomes unnecessary, not whether current predictions generalize under shift.
- **Cheapest first test:** Cross two binary nuisance factors at equal sample counts while masking the teacher channel only in the fixed later refresh. Compare invariant-feature subsets, gradient matching and direct bilevel selection; remove the future feature in an explicitly out-of-contract variant.
- **Old-task retention check:** Test normal A/C plus rare combinations after real reuse, with a live-teacher rescue control where the relevant feature is still confounded.

### Combine, price and break the substitutes

#### 15. Reuse one buffer across two independently admitted jobs (P)
- **Mechanism:** Build a single witness buffer whose ordinary-example subsets satisfy two jobs, checking each obligation and their interleaving instead of allocating independent copies by default.
- **Novelty vs nearest prior art:** Multi-task condensation and the parent's shared-substitute cards motivate reuse. The claim is a byte advantage from shared example structure beyond joint MTT plus exact subset accounting.
- **Cheapest first test:** Search tiny pools for a common correction under sequential and interleaved refreshes. Compare independent buffers, shared functional summaries and joint trajectory-matched memory at equal peak bytes.
- **Old-task retention check:** Score A/C after each legal interleaving and after the shared source is overwritten; average success cannot excuse harm to the rarer job.

#### 16. Fit witnesses for retiring either of two sources (P)
- **Mechanism:** Before a later allocation request arrives, build one buffer that can stand in for either teacher when the other survives, using fixed subsets and certifying each cut independently. Do not claim simultaneous deletion.
- **Novelty vs nearest prior art:** [Disjunctive protection](disjunctive-protection.md) and the parent already choose between alternative handovers. The new hypothesis is that overlap in exemplars makes the two options cheaper to buy together than separately.
- **Cheapest first test:** Use two teachers with partially aligned corrections and reveal in a held-out allocation stream which bank B needs. Compare joint distillation plus exact retirement, independent options and retaining the cheaper bank.
- **Old-task retention check:** Run A/C after each possible bank is overwritten and a refresh still uses the surviving bank; record denied dual deletion separately.

#### 17. Cascade retirements without the original teacher (P)
- **Mechanism:** Use a first witness buffer to build a smaller successor when the allowed continuation narrows; compose checked error bounds against the original source rather than turning each generation into its own oracle.
- **Novelty vs nearest prior art:** Data-Distill-Net recursively distills memory and [certified CL](https://arxiv.org/abs/2407.06697) motivates scoped guarantees. A conditional contribution would be composable replacement evidence that survives multiple irreversible cuts at useful budgets.
- **Cheapest first test:** Enumerate three horizons of a small linear stream with one expanding-sensitivity branch. Compare equal-byte recursive condensation plus the same error accounting, fresh oracle refits as a ceiling, and no second cut.
- **Old-task retention check:** Check A/C at each generation and after the original and then first buffer are overwritten; test expanding branches rather than only easy contracting paths.

#### 18. Reject a witness before it enters a self-created state (I)
- **Mechanism:** Pair each buffer with a cheap applicability check on the post-step state, staging or refusing steps that exit its certified region. Charge the guard and all refusals.
- **Novelty vs nearest prior art:** Runtime guards and [finite safe regions (PR #152)](https://github.com/manojbajaj95/cl/pull/152) already do scoped admission; this tests whether guarding a witness is cheaper than keeping the anchor.
- **Cheapest first test:** Enumerate a nonlinear stream with equal pre-cut weights but distinct slot states; compare option-aware region checks to a weight-distance threshold, ordinary guarded condensation and retention of the source.
- **Old-task retention check:** Score A/C through accepted and rejected prefixes, separately reporting refused B progress. No retroactive teacher fallback after reuse.

#### 19. Find the minimum destructive counterexample (I)
- **Mechanism:** On a duplicated test system search shortest legal continuations for which cached outputs, optimizer deltas or retirement bookkeeping look correct but the witness loses old behavior.
- **Novelty vs nearest prior art:** Counterexample search and [first point of loss (PR #134)](https://github.com/manojbajaj95/cl/pull/134) localize failure already. This is a differential audit specific to a substitute and an actually inaccessible source.
- **Cheapest first test:** Breadth-first search tiny task orders and plant a late alias, a moment mismatch and an unseen batch. Compare random rollout audits at the same evaluation count; distinguish access failure from functional failure.
- **Old-task retention check:** For each minimal witness of failure, evaluate normal A/C on both systems across the full prefix, then verify whether disabling the alias changes retention.

#### 20. Trade today's examples against tomorrow's buffer (P)
- **Mechanism:** Select today's examples to eliminate the branch with the most expensive residual correction, and compile witnesses only for the branches that still need a substitute.
- **Novelty vs nearest prior art:** Look-ahead selection and condensed replay are known. The candidate interaction is that one purchase lowers the other's marginal bytes enough to cross a real allocation threshold, beyond independently tuned look-ahead selection plus MTT plus exact retirement.
- **Cheapest first test:** Enumerate a two-branch toy under an overlap cap, checking joint selection against both solo arms, their best stacked combination and an exhaustive joint ceiling using the same grammar.
- **Old-task retention check:** After reuse score ordinary A/C separately on the read-free and buffer-backed refresh branches, at matched B progress.

#### 21. Account for the teacher hidden in the decoder (I)
- **Mechanism:** Compare literal fixed examples with latent-coded witnesses and an anchor factor; count shared decoder code/state, reconstitution cost and dependencies before calling a source free.
- **Novelty vs nearest prior art:** Generative replay, compression and the parent's access ledger already cover the mechanisms. This audit catches a byte win obtained by moving the old bank elsewhere.
- **Cheapest first test:** Quantize a toy EWC factor and cached-label examples at equal total bytes; compare against a latent buffer with the decoder pinned, then with the claimed bank physically replaced.
- **Old-task retention check:** Score ordinary A/C across repeated refreshes under the measured precision and compute cap; a decoder unable to run after reuse is an access failure, not mere accuracy loss.

#### 22. Forecast where substitution stops paying (I)
- **Mechanism:** Sweep horizon and branch breadth at fixed retention and available B bytes, measuring whether retaining, compiling, pre-teaching or explicitly declining new admissions buys the most actual B learning.
- **Novelty vs nearest prior art:** This is a budget frontier for the parent's buy-versus-rent question, not a new primitive or a universal scaling law.
- **Cheapest first test:** Exhaust short linear and nonlinear streams with branch families of varying overlap. Compare exact retirement with the same menu, fixed schedules and fit budget; include a no-cut and zero-teacher-benefit regime.
- **Old-task retention check:** Report worst ordinary A/C across all admitted prefixes after reuse, and report separately which future jobs each arm refused, so narrower scope cannot masquerade as better retention.

## Ranked deeper questions

1. **Can a checked witness close its own reachable-state loop cheaply enough to retire a useful source?** Start with cards 1–3 and 7: a rank-exact linear control, a nonlinear off-path failure, and a continuation that rotates a previously silent direction. Give branch-aware gradient/trajectory matching, low-rank Fisher and functional surrogates the same build budget, verifier and exact retirement planner. Demand in-scope A/C retention on held-out orders after a real overwrite with matched B progress. If the strongest baseline closes the same obligations at the same cost, the witness is condensation, not a primitive.
2. **Can data alone remove a teacher that is demonstrably needed tomorrow, rather than just improving the starting checkpoint?** Use cards 8–14: fixed refresh optimizer, schedule and batches; random, gradient-matched, margin-matched and direct bilevel selectors; ordinary selection with and without teacher as the necessity check. Require an improvement on old-task distinctions after refresh, including task orders unseen during selection and a negative control where no separating evidence is available.
3. **What cannot be represented by ordinary examples, even with perfect fitting?** Connect rank, nonconservative correction fields and missing teacher distinctions (cards 1, 6, 12) to the cost of extra examples, additional signals or an explicit refusal. Separate a limitation of the chosen loss/interface from a lower bound on any teacher substitute and from a benign update mismatch that never hurts A/C.
4. **Can substitutes be reused or narrowed without paying for the source twice?** Test interleaved jobs and successive retirements (cards 15–21) against joint condensation, cached targets and exact scheduling with the same verifier. Price every retained dependency and refused job. Useful composition means more actually reclaimed capacity, not just a smaller standalone buffer.

**Verdict:** Synthesizing corrective examples and picking data for future plasticity are established. A learned stand-in is a candidate primitive only if its scoped substitution lets the learner remove a future training read on terms that the best existing condensation or anticipatory selection plus exact retirement cannot match. The first gate is continued learning after destructive reuse, not logit fidelity, one favorable trajectory, or present-day old-task accuracy.
