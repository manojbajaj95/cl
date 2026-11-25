# Trained redundant finishes and matched fade profiles

**Status:** Ideas only; one exact paper fixture, no training or GPU. **Parent:** [Menu-preserving replacements and paired residuals](menu-replacements.md) ([PR #235][parent]). **Review seeds:** [Flood triage][triage], score 3: parent 08 trains a host with two independently executable finishes per future demand class; parent 11 pairs opposite-signed residuals by their whole fade profile. Cards 01 and 12 restate the seeds as reference designs.

**Ledger read first:** The [idea ledger][ledger] rules out treating save/restore as a new capability, forecast-only selection as evidence, and a fixed linear Gramian as a certificate for nonlinear trajectories. Require executed service on ordinary old tasks, not agreement on the training witnesses. **P** marks a candidate reusable object or operation (not a priority claim); **I** marks an improvement, diagnostic or limit. Nearest-work comparisons below are provisional, not an exhaustive novelty search.

## What would count

- **Train the host, freeze the rules.** Train on truthful A/C acquisition data and development demand windows, using legal finish rollouts to shape the state from which later writes start. Fix the demand-class interface, finish/reservation rules, failure assumptions and host checkpoint before blind trials; freeze the learned preparation, not the future stream. At evaluation, only the declared ordinary updates and finish actions may mutate the live state; no host retuning, backup checkpoint loading outside a control, or post-hoc policy search by the proposed method. A demand class is a set of requests sharing a declared observation/contract, not a retrospective grouping of successful runs. Include unseen instances within each evaluated class and hold out invalidator families; class transfer beyond that is a separate claim.
- **Require two executable alternatives on one live history.** Each finish starts from the same committed state and can succeed without any work, private state, or partial output from the other. It must retain normal A/C service, deliver the same B contract and fit the original absolute deadline. Declare the failure domain, not just distinct route IDs: shared dependencies can fail together. For each admitted invalidation and public observation, a single causal choice must work across the hidden states consistent with it. Charge exclusive reservations, shared capacity, staging, probes and latency; allow sharing only where branches are mutually exclusive and resources survive the permitted invalidations. An uncovered failure must be reported or refused under the parent's same-step rule, not relabeled out of scope after the test.
- **Match the effects that actually reach old readers.** A and C are independent old tasks; B is the incoming task. In the fixed linear case, let $r_i(t)$ be the signed zero-input residual's step contribution from slot $i$, after applying merge and the A/C readout; separate common weight decay. Bound $\max_{s\le H}\left\|\sum_{t=1}^{s}(r_1(t)+r_2(t))\right\|$ over every allowed schedule, not merely the first or last tick. Apply each reader's own tolerance. Also require meaningful individual residuals, useful fresh B response from both branches, and comparable realized B utility. For nonlinear updates, measure the real-gradient proposal and its zero-gradient reference from the same pre-step state, then execute both the actual suffix and an appropriate no-carried-state control; independently rolled-out zero-input traces need not add. Include idle ticks, reader margins, differing clocks and the time after the finish through the declared residual tail. Either bound the remaining tail or state the horizon; do not claim indefinite cancellation.
- **Price the alternatives.** Compare at matched pre-shift A/C performance and old-task margins, width, training examples, train/online compute, resident and peak bytes, slot precision, B/maintenance utility and deadlines. Compare Pareto fronts when exact matching is impossible; count refused demands and the cost of retaining their safe route. Give controls the same execution rights and observations: equal-byte checkpoint or duplicate head, fault-tolerant contingent planning and parent-style replacement search on an ordinarily trained host, plus [OGD][ogd]/[GEM][gem], fresh-only/reset, first-step matching, [slot echo][echo] and exact joint search on tiny domains. A crossing of the two seeds has to beat the best independent stack, not merely the two ablations.

## Exact paper fixture: a first-tick tie with a later failure

Take a frozen linear readout with A and C residual directions `v = (1, 2)`. The merged old outputs start at zero with margins `(1/8, 1/4)`. Over three ticks pick one positive slot trace `p = (1, 1/2, 1/4)` or `q = (1, 1/4, 1/16)`, and one negative trace `−p` or `−q`; multiply each tick by `v`. These are scalar geometric decays with factors 1/2 and 1/4 after the first tick. Separately, each chosen slot contributes the same positive B trace `p`, via a B-only mode, so every pair earns B = 7/2 over three ticks. This is a zero-input construction, not evidence of learning or preservation under fresh gradients.

| Pair | Cumulative A/C drift, in multiples of `v`, at ticks 1, 2, 3 | Within both margins? |
|---|---|---|
| `p, −p` or `q, −q` | `(0, 0, 0)` | Yes |
| `p, −q` | `(0, 1/4, 7/16)` | No, at tick 2 |
| `q, −p` | `(0, −1/4, −7/16)` | No, at tick 2 |

Suppose these pairs are two reserved finishes for the same B demand, all four carriers are resident, and both finishes fit D=3 from the same committed state. A publicly observed loss of an entire matched finish at selection leaves the other executable; an invalidator taking both positive carriers defeats both. If the public signal only says “one finish is down,” neither fixed choice is safe across both hidden possibilities. The example distinguishes trajectory matching and usable redundancy from two tick-1 matches or two nominal menu entries; a planner told the full dynamics ties it.

## Idea cards

### Training for executable substitutes

#### 01. Train two finishes from one committed state (P)
- **Mechanism:** During A/C acquisition, give each development demand class two budgeted finish rollouts from the very same state; optimize the worse individual finish and the outcome after each declared single-domain outage. Freeze the learned host and reservation policy before the blind stream.
- **Novelty vs nearest prior art:** Fault-tolerant recourse plans around available actions; [MAML][maml] optimizes adaptation from an initialization. The candidate is a trained same-deadline substitution guarantee without adapting the host or searching for a new route after the fault.
- **Cheapest first test:** CPU two-branch ReLU host with two demand classes; enumerate legal executions after blind route-specific updates. Compare two independently trained heads, same-byte checkpoints, replacement search and OGD. Include an unseen update that removes both finishes and require a refusal.
- **Old-task retention check:** Run ordinary held-out A/C before, through and after each handoff and refusal; score B only if reached by the unchanged deadline.

#### 02. Offline cross-splice training (P)
- **Mechanism:** From one old-task training episode, run a prefix of one finish then a bounded bridge into the other at a public progress marker. Train complete standalone paths too, but penalize a bridge that consumes the remaining deadline or needs the retired route's private state.
- **Novelty vs nearest prior art:** Parent 03 carries in-flight choice through a replacement; [option models][options] define initiation and termination. Here preparation trains actual progress to be accepted by either finish at a fixed interface.
- **Cheapest first test:** Two three-step finite controllers, outage after action one. Compare endpoint-only redundant training, make-before-break and exact online recovery; include a prefix with an irreversible side effect that no bridge can preserve.
- **Old-task retention check:** Evaluate A/C after the original prefix, after the bridge and after continuation; retain the legitimate prefix effect rather than undoing it via restart.

#### 03. Train past common cuts, not toward orthogonal weights (P)
- **Mechanism:** Use development failures to find sets of shared dependencies whose loss kills both finishes; train against those cuts while allowing shared components outside the declared failure domains. Track the minimum credible common cut rather than route distance.
- **Novelty vs nearest prior art:** Disjoint-path routing and [DropPath in FractalNet][fractal] motivate route diversity. The proposed training signal is a cut in the execution dependencies of a future write, including shared authorization or optimizer state that two different subnetworks can still need.
- **Cheapest first test:** CPU gated linear classifier with distinct heads sharing a mutable statistic. Compare orthogonal heads, random path dropout and exact planner with the same actions; blind-test a novel cut through that statistic.
- **Old-task retention check:** Test A/C slices served by the shared statistic as well as slices unique to each finish; a cut win purchased by dropping shared service fails.

#### 04. Train for failures the gate can actually distinguish (P)
- **Mechanism:** Train a small, frozen observation interface jointly with the host. For each indistinguishable failure class require a common safe finish, or earn a probe that separates cases without consuming the finish's last slot.
- **Novelty vs nearest prior art:** Active diagnosis and conformant planning optimize sensing or action under a fixed observation model. Here old-task training shapes whether the finish selector can legally distinguish the failures that matter.
- **Cheapest first test:** Two aliased faults requiring opposite finishes; let one ordinary activation serve as a legal probe. Compare full-information oracle, fixed probes, and exact belief-state planning on the unshaped host; hold out an alias that even the trained probe misses.
- **Old-task retention check:** Run A/C during the probe and on the ambiguity-safe exit, including cases when there is no time to probe.

#### 05. Distill an outage matrix, not teacher logits (P)
- **Mechanism:** Use a finite executable oracle during development to label which legal finish survives which intervention; train a smaller host to make those labels true via actual finish loss, with no stored matrix required online.
- **Novelty vs nearest prior art:** Distillation ordinarily transfers predictions, and [Once-for-All][ofa] trains independently runnable subnetworks. The transferred object here is an intervention-indexed feasibility relation from the same live state and at the same deadline.
- **Cheapest first test:** Enumerate two demand classes and four outages in a tiny teacher host, then test a smaller student on withheld composed outages. Compare equal-byte teacher-logit distillation and dropout; drop the claim if matrix agreement improves but executed survival does not.
- **Old-task retention check:** Measure A/C under student replacement, no replacement, and an outage where the student must refuse despite a teacher witness.

#### 06. Train a standby that earns its own reservation (P)
- **Mechanism:** During development, require useful A or C service from the state that supports the standby, then test whether that same state still supplies an independent B finish when its primary fails. Price the additional state and time even if some maintenance is shared.
- **Novelty vs nearest prior art:** Warm standbys and multitask auxiliary objectives already reuse resources. The claimed operation is to credit the same live representation for routine service and a separately executable future write, not to count a second dormant copy as free.
- **Cheapest first test:** Three-feature linear host with one busy maintenance lane; compare an idle duplicate, warm standby replay and ordinary multitask training at equal occupancy. Blind-test a maintenance update that corrupts an auxiliary feature used by both finishes.
- **Old-task retention check:** Verify A/C maintenance output on its ordinary cadence during standby occupation, then check both tasks after a switch.

#### 07. Train renewal with no accumulating archive (P)
- **Mechanism:** Train on development chains of allowed arrivals so after a finish executes, an already-declared ordinary update returns the host to a state with two next-demand finishes. Require constant resident budgets and a frozen renewal rule.
- **Novelty vs nearest prior art:** Receding-horizon planning and the review's [adaptive-renewal][triage] line recover readiness. The additional target is restoration of two independently runnable, failure-distinct continuations after an actual spend, not just reaching one ready endpoint.
- **Cheapest first test:** Exhaust a four-state CPU host for two demand cycles alternating failure domains. Compare one-cycle training plus parent substitution, exact receding-horizon planning and equal-byte rolling checkpointing; include an arrival chain exhausting both routes.
- **Old-task retention check:** Check ordinary A/C after each spend and renewal, including the second cycle where recovery could otherwise appear free by forgetting the first cycle's old service.

#### 08. Share a method across demand classes, not a point of failure (P)
- **Mechanism:** Train a common finish generator with two execution backends. Each class must produce a legal pair; selectively prohibit shared dependencies between its two instantiations, while allowing sharing between demands that cannot be live together.
- **Novelty vs nearest prior art:** [Hypernetworks][hyper] amortize parameter generation; robust resource allocation accounts for contention. The testable addition is demand-conditional failure diversity of generated *writes*, not merely parameter reuse.
- **Cheapest first test:** Tiny generator for three linear target families; reserve two classes with overlapping arrivals and hold out the third family for a separate transfer test. Compare independent policies and exact shared scheduling; include an outage of the generator itself.
- **Old-task retention check:** Serve ordinary A/C under concurrent reservations, then verify them after each generated finish and after declining a conflicting arrival.

#### 09. Separate deadline margin from accuracy margin (I)
- **Mechanism:** Train for latest admissible start of the slower finish after each outage, independently of its final task error; do not let an easy old-task margin buy an extra tick.
- **Novelty vs nearest prior art:** Robust scheduling already optimizes slack. This is an offline training objective for finding attainable slack in a learned host, not a new scheduler.
- **Cheapest first test:** Use two legal finite-step solvers for one B target with tied terminal accuracy and unequal runtimes. Move arrivals late; compare endpoint training and a runtime-only shaping control at matched old-task margins.
- **Old-task retention check:** Score A/C at the latest admissible start, throughout the finish, and on the safe refusal one tick too late.

#### 10. Price survivability by the nearest damaging truthful update (I)
- **Mechanism:** During development enumerate low-cost *truthful* updates that destroy both finishes; optimize the worst admissible cost-to-double-failure and verify the benefit on withheld update families.
- **Novelty vs nearest prior art:** Adversarial training already optimizes worst-case radius. The stressor here is useful legal maintenance and the failure criterion is two lost executions, not a misclassified example.
- **Cheapest first test:** Enumerate short legal gradient sequences in a tiny CPU host; compare random update dropout, gradient-norm matching and ordinary robust training. Retain a genuine common-mode attack as a negative.
- **Old-task retention check:** Match achieved maintenance utility and check ordinary A/C before the adversarial update, on switching, and on lawful refusal.

#### 11. Test for an online-search shortcut (I)
- **Mechanism:** Cross ordinary vs redundancy-trained hosts with frozen selector vs exact online recourse. Count failures caused by missing feasible actions separately from those caused by wrong choice among feasible actions.
- **Novelty vs nearest prior art:** This is a factorial audit of parent 08, not a primitive. It separates trained feasibility from moving an existing replacement search offline.
- **Cheapest first test:** Exhaust a small finite demand/invalidator table once under each arm, with identical actions and refusal rights. If the trained host changes only selector runtime, report amortization rather than a larger feasible set.
- **Old-task retention check:** Include the ordinary A/C test set at every boundary in all arms; exclude any apparent action that earns B by temporarily breaking an old task.

### Making cancellation survive the suffix

#### 12. Pair by signed fade profile, not the first step (P)
- **Mechanism:** Measure signed response traces under declared clocks and suffixes; pair by worst cumulative A/C mismatch across prefixes, constrained by real B utility and both branches' fresh response.
- **Novelty vs nearest prior art:** Parent 09 and [slot echo][echo] address immediate pairing and carried state. Standard momentum decay gives a tail for one slot; the candidate matching object is a pair compatible in *both* old-reader projections through execution.
- **Cheapest first test:** Start with the paper fixture; add a truthful nonzero-gradient B suffix. Compare first-tick matching, reset, GEM and exact joint selection at identical B utility; force a fast/slow mismatch with the same first proposal.
- **Old-task retention check:** Check A/C at each applied prefix and after the tail, using ordinary held-out examples as well as the two fit projections.

#### 13. Give the pair an interruption contract (P)
- **Mechanism:** Publish legal clock traces for a paired residual, including skipped and asynchronous ticks; reserve either a synchronized release or an independently safe action before every allowed interruption.
- **Novelty vs nearest prior art:** Switched-system analysis and synchronized scheduling already handle asynchronous clocks. Here a signed cancellation is valid only with a public guarantee over which paired residuals are actually consumed before a reader runs.
- **Cheapest first test:** Two geometric slots with one allowed skipped tick; exhaust schedules including an observation between branch writes. Compare locked ticks, exact scheduling and nominal-profile matching; if an atomic update ties, report only the cost of coordination.
- **Old-task retention check:** Test A/C on interleaved observations, at the skip and after the last catch-up tick.

#### 14. Hand the remaining tail to a different partner (P)
- **Mechanism:** If a branch is retired at a public boundary, match its survivor's *remaining* trace against a different already legal partner, carrying forward cumulative discrepancy and the original deadline.
- **Novelty vs nearest prior art:** Parent 17 exchanges finish reservations and parent 20 handles clock splits. The proposed object is a transferable residual obligation whose incoming discrepancy changes which replacement is valid, even with identical future decay.
- **Cheapest first test:** Enumerate a three-partner heavy-ball system where future mismatches of the same magnitude but opposite signs are harmless from zero, but only one repays the existing drift. Compare slot reset, fresh-tail matching and full exact replanning without resetting A/C margins.
- **Old-task retention check:** Test A/C before retirement, immediately on partner switch and at each tail prefix; forbid an intermediate breach later canceled.

#### 15. Certify a band of reader margins instead of a single trace (P)
- **Mechanism:** Carry a joint cumulative displacement envelope in a fixed feature basis over an allowed set of suffix batches. A new linear reader can reuse it only if its own projection of the envelope fits its independently measured margin; nonlinear readers need a sound bound on that projection.
- **Novelty vs nearest prior art:** [CROWN][crown] bounds network outputs; transfer of safety bounds is standard. The hypothesized reusable certificate is an execution envelope for two carried slots that different task readers can consume without refitting the pair.
- **Cheapest first test:** Enumerate one ReLU crossing with two suffixes, derive an exact finite envelope, and compare interval sums of independent tails, joint reachability and simple revalidation. Force an unseen reader with a narrow margin to reject the certificate.
- **Old-task retention check:** Test ordinary A/C even when the certificate is reused or vetoed; verify both lower and upper margins after the crossing.

#### 16. Look for a small witness of unavoidable mismatch (P)
- **Mechanism:** Return the specific reader, prefix and indistinguishable schedule that blocks a pair assignment; for a finite candidate set collect such witnesses until every legal pairing has been ruled out.
- **Novelty vs nearest prior art:** Counterexample-guided synthesis already refutes assignments. The candidate interface makes a fade-induced failure actionable: it tells offline training whether to change a mode, a margin, or the public observation before attempting another reservation.
- **Cheapest first test:** Small exact enumeration with one first-tick tie and two late violations on different readers; compare generic adversarial loss and full traces fed to the same host trainer at equal development cost. If witnesses do not change the next successful assignment, retain only the diagnostic.
- **Old-task retention check:** Reproduce the predicted A/C violation on the ordinary task slice, and retest both slices after adding any proposed repair.

#### 17. Teach compatible fades without changing the optimizer (P)
- **Mechanism:** During A/C acquisition choose truthful training sequences that align old-reader-visible modes of the two branches; leave optimizer, legal slot operations and precision fixed before blind evaluation.
- **Novelty vs nearest prior art:** Gradient matching and [GEM][gem] target immediate projections; multi-timescale optimizers introduce available rates. The claim is that *which modes the reader sees* can be trained at fixed optimizer and budget.
- **Cheapest first test:** Tiny piecewise-linear host with heterogeneous fixed heavy-ball gains or rates, all arms using identical candidate batches. Compare first-gradient matching, explicit tail matching without training and tied rates; require benefit on unseen B orderings with real gradients.
- **Old-task retention check:** Match ordinary A/C accuracy and margins before the shift and check both throughout the blind suffix; do not count flattening both old readouts as alignment.

#### 18. Require cancellation to survive adaptive denominator drift (I)
- **Mechanism:** For Adam, score real and zero-gradient proposals from identical pre-step states and validate the selected pair on executed suffixes that drive second moments and clocks differently. Use only legal state orientations or charge a different optimizer.
- **Novelty vs nearest prior art:** [Adam][adam] already specifies the denominator and bias correction; [slot echo][echo] tracks optimizer-state effects. This is the falsification boundary for treating a linear fade match as an optimizer-independent primitive.
- **Cheapest first test:** Two two-coordinate Adam branches with equal first proposals and unequal second moments. Compare matched linear proxy, exact enumeration, reset and separate step-size tuning; look for a sign-preserving miss after a truthful gradient spike.
- **Old-task retention check:** Score A/C around the spike and on a no-spike suffix at matched B gain; show the actual intermediate failure if the proxy misses.

#### 19. Budget quantization by prefix error, not parameter norm (I)
- **Mechanism:** Quantize paired state jointly subject to a cumulative A/C error budget; allocate bits to cancellation-sensitive modes rather than the largest independent coordinates.
- **Novelty vs nearest prior art:** Task-aware quantization already allocates precision by output sensitivity. Here the sensitivity target is persistent cancellation under live updates, not isolated output error at quantization time.
- **Cheapest first test:** Exact low-bit rounding in the geometric fixture extended by a near-boundary initial margin. Compare independent rounding, shared-scale rounding and direct quantized joint search at the same resident bytes and B.
- **Old-task retention check:** Verify A/C after each quantized step including the latest prefix; reject an improved terminal error that crossed a boundary earlier.

### Crossing the seeds

#### 20. Train two finishes whose partners can actually cross over (P)
- **Mechanism:** Train both finishes from the same host and require a cross-pair assignment to remain executable after a declared single-carrier loss. The selector chooses a complete compatible pair by a frozen public rule; do not assume that certified halves of different finishes compose.
- **Novelty vs nearest prior art:** Fault-tolerant planning and parent 17 can choose from available alternatives. The claim is that host training can create compatible *cross* edges in the joint finish/fade graph that an independent two-finish trainer plus tail matcher cannot get at the same budget.
- **Cheapest first test:** Extend the paper fixture with adjustable trained readout mixtures. Make one carrier unavailable due to a preexisting maintenance booking and blind-test an invalidation of a carrier from the other finish; an admissible cross edge must use the two remaining carriers before D. Compare the best independent stack and exact joint planning on both ordinary and jointly trained hosts. Hold out a loss that deletes every compatible cross edge.
- **Old-task retention check:** Execute surviving crossed and uncrossed finishes on A/C through their entire tails, score matched B/maintenance, and test the refusal path for the no-edge loss.

#### 21. Rebate standby capacity only after the fade debt clears (P)
- **Mechanism:** A finish may release a reservation early only if its retired residual cannot invalidate the already reserved successor across the next demand window. Train alternative finishes with genuinely different release times under the same rule.
- **Novelty vs nearest prior art:** Parent 18 charges real slot time and parent 19 prices consuming ticks. The candidate adds a measurable release condition: an earlier B completion need not release capacity if a latent old-reader debt still binds its successor.
- **Cheapest first test:** Two consecutive demands, with one early B finish whose mismatched tail collides with the next window. Compare deadline-only scheduler, exact joint scheduler and best separate redundancy-plus-pairing stack at equal footprint and throughput.
- **Old-task retention check:** Check A/C during the apparent idle gap, after the next arrival and through both tails; a capacity rebate paid by an old-task failure is invalid.

#### 22. Find the capacity floor for both promises together (I)
- **Mechanism:** Enumerate hosts with a fixed number of carriers and slots and compute maximum per-class deadline coverage under the same public observations, once with prefix cancellation and once with endpoint-only constraints.
- **Novelty vs nearest prior art:** Robust matching and reachability already enumerate feasible assignments; this is a bound and audit of where training can plausibly help, not a new capacity predictor.
- **Cheapest first test:** Exhaust two demand classes, two failure domains and four carriers; vary shared dependencies independently of decay. Include an oracle-impossible cell and a separable cell where the best stack ties, then see whether finite training helps only in the remaining cells.
- **Old-task retention check:** Filter assignments by every ordinary A/C prefix and safe refusal before computing coverage, and report what endpoint-only accounting would have admitted incorrectly.

## Ranked deeper questions

1. **Can old-task training buy two independently runnable finishes on held-out failures, rather than just teach a quicker selector?** Start with 01, 03, 04 and 11. Freeze the host and rules, then compare exact recourse on both learned and ordinary hosts as well as equal-byte redundancy. Prioritize coverage at common A/C margins and B/maintenance utility. If only search time changes, narrow the claim to amortization.
2. **What representation of the fade is sufficient under real updates, skipped ticks and nonlinear readouts?** Start with 12, 13, 17 and 18. Demand out-of-sample execution after the first-tick tie; compare tested prefix traces, mode envelopes, reset and exact joint steering. If only fixed linear dynamics are predictable, restrict the interface to that regime.
3. **Does joint training create a feasible crossed finish that the best independent stack cannot produce at the same budget?** Start with 14 and 20–22. Include separable and all-partners-lost negatives. If identical rights and capacity yield identical feasible traces, claim lower validation or execution cost only if measured.
4. **Can the trained property renew after a real spend without growing the host or withholding legitimate ordinary updates?** Start with 02, 06, 07 and 21. Use repeated blind windows with unchanged deadlines and full tail accounting. A one-cycle win with a growing reserve bank does not qualify.

[parent]: https://github.com/manojbajaj95/cl/pull/235
[triage]: https://github.com/manojbajaj95/cl/blob/c9d08e7d73f0e83077e9915fc1915925146784e8/reviews/flood-triage.md#L348
[ledger]: https://github.com/manojbajaj95/cl/blob/c9d08e7d73f0e83077e9915fc1915925146784e8/reviews/idea-ledger.md
[echo]: https://github.com/manojbajaj95/cl/blob/226f9d7a6a9fab414091c186b20df53e80ed9913/tree/slot-echo.md
[ogd]: https://arxiv.org/abs/1910.07104
[gem]: https://arxiv.org/abs/1706.08840
[maml]: https://arxiv.org/abs/1703.03400
[options]: https://doi.org/10.1016/S0004-3702(99)00052-1
[fractal]: https://arxiv.org/abs/1605.07648
[ofa]: https://arxiv.org/abs/1908.09791
[hyper]: https://arxiv.org/abs/1609.09106
[crown]: https://arxiv.org/abs/1811.00866
[adam]: https://arxiv.org/abs/1412.6980
