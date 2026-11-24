# Teaching bundles: the smallest lesson that buys a shared reply

**Status:** Ideas only; no implementation, experiments, or GPU work. **Parent:** [Examples versus probes](examples-versus-probes.md) ([PR #179](https://github.com/manojbajaj95/cl/pull/179)). **Review seeds:** [Flood triage, row 284](https://github.com/manojbajaj95/cl/blob/23cfd2e9633460d9b6825fd7a01d539ccc383de3/reviews/flood-triage.md#L284) kept parent **#03** (transfer an irreducible ordered bundle to hidden editors without repeating search) and **#12** (make hidden momentum visible to the same probe via a shared reply) at score 3. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/23cfd2e9633460d9b6825fd7a01d539ccc383de3/reviews/idea-ledger.md).

## What would count as a new object?

**Not an ordered curriculum or a good excitation.** [Iterative Machine Teaching](https://proceedings.mlr.press/v70/liu17b.html) optimizes examples for their effects on a learner, [Nonparametric Teaching for Multiple Learners](https://arxiv.org/abs/2311.10318) already considers teaching multiple learners, and [Matching Training Trajectories (MTT)](https://arxiv.org/abs/2203.11932) optimizes multi-step effects. [FLEX](https://arxiv.org/abs/2304.13426) designs informative actions for nonlinear dynamics; [imperfect-information games](https://arxiv.org/abs/0706.2619) can represent admissible common replies and future observations. The candidate here is a **portable proof of a specific lesson's effect on the available replies**, optionally with a narrowly scoped guarantee about what a common reply later lets a fixed probe distinguish. If storing the winning sequence and using an off-the-shelf planner or verifier is just as cheap on new editors, this is an improvement, not a primitive.

### Two promises, two different tests

- **Shortest shared-reply bundle.** Freeze a truthful pool, update law (including batching, allowed repeats, and costs), legal hidden editor family, free transcript classes, and reply menu. For one declared class, find the minimum-length ordered sequence such that **there exists one reply that works for every compatible hidden history** after training. Require the published reply to preserve independent A/C floors and the frozen editor's new utility. Check necessity against *all* shorter lawful sequences and *all* replies in that menu, not just deletions from the winner or failures of the nominated reply. A proper subset of an editor class can have a shorter winner; distinguish **effect transports** from **minimality transports**.
- **Decision-relevant reveal.** Hold the same behavioral probe, schedule, first-reply cost, immediate utility, and retention fixed. A common reply may expose hidden optimizer differences after a declared continuation. The resulting transcript cells must each admit a safe next reply, while at least one cell under the matched nonrevealing reply has no shared safe next reply. Mere momentum reconstruction, more mutual information, or separating one pair while leaving other conflicting histories aliased does not count. If the matching optimizer trajectories need the same next reply, use them as a negative control.
- **Blind transfer protocol.** Freeze the sequence, nominated reply, and proof before opening held-out demand; allow only a public family envelope and a version/interface check at deployment. The runtime cannot see the realized branch, use optimizer slots, tune the examples, choose a new first reply, or search a new trajectory. Enumerate exact hidden histories in an offline referee that returns results only after commitments; any online evidence beyond the public envelope is priced. If containment or margins cannot be checked from allowed evidence, revert to the paid split or refuse.

**Shared controls.** Freeze demand, task floors, update opportunities, probe bank and read precision, and menus for every arm. Match new utility and pre-intervention A/C margins; independently check worst old-task slices and ordinary performance at every live prefix, including later writes. For teaching use uniform replay, per-example greedy, [GCR](https://arxiv.org/abs/2111.11210), and MTT on the same real pool, then a source-fitted sequence cached with ordinary re-verification. For revealing use behavior-only repair, active excitation, belief planning with the fixed read and reply budget, and the best plug-together teaching + sensing + cache stack. Include [optimizer-slot splices (PR #178)](https://github.com/manojbajaj95/cl/pull/178) with slot access priced, and direct reads as a privileged ceiling. Exact joint enumeration is an offline oracle, not something to claim higher admission than. Report distinct counts for training examples, optional and scheduled reads, verification and search calls, bytes, delay, and refusals. Charge source search and failed transfers as well as successful reuses. Do not rerun the ledger's global Gramian scoring, Lyapunov-order forecasting, or synthetic counter-gradient search under a new name.

### Two paper fixtures, not evidence for the primitive

**Two examples, one legal order.** In the parent's gated repair toy keep the damaged A margin `1 − ReLU(d − q − u)`, its floor `1/2`, and the fixed common reply adding `u=1/4` per lane. Start at `q=1/8, p=0`. The frozen truthful pool has three examples: a masked squared-error step setting `p=1`; a step on prediction `g(p)q` with target `1/4`, where the frozen gate has `g(0)=0, g(1)=1` and the step updates only `q`; and a decoy setting `q=3/16`. Use one unit step on half-squared error per presentation, no batching. Two hidden edits share the free transcript, damage opposite lanes by `d=1`, and install different correct outputs in a private lane untouched by replies. The same menu also has two specialists adding `1/2` to one lane only. The ordered pair (set `p`, then gated example) gives `q=1/4` and reaches the floor on both edits; the reverse is inert on `q` and no singleton gets past `3/16`. Each specialist fails on the other world. Test transfer on new editors that also share a transcript, may change the private outputs, and have public damage bound `d≤1`; an opposite-lane worst-case pair is needed to transfer the *lower bound*, not to transfer sufficiency. Keep C independent, then add a protected C slice using `p` to test an otherwise valid lesson that should be rejected.

**Same fixed read, different lawful momentum reply.** Two worlds start at `w=0, v=±1/4`. The same certified immediate repair operates on separate lanes. Two equal-cost variants pair it with two ordinary momentum steps on a truthful auxiliary quadratic of curvature `h`; both curvatures are in the frozen menu. With `v'=(1/2)v+hw, w'=w−v'`, the final value is `w₂=(3/2−h)w₁`, where `w₁=−v/2`. Under `h=3/2` the fixed probe `P(w)=w` sees zero again; under `h=1/2` it sees `±1/8`. Read `P` only before the reply and after the two steps in both arms. A next frozen offer must genuinely require opposite specialists in the two worlds (e.g. old A's tight lane differs and the one-lane repair is the only affordable response); independently vary that mapping and include worlds with identical next obligations. Bound the entire auxiliary path with an independent C floor such as `1−|w|≥7/8`, and check both teaching/reply variants maintain new utility. This isolates a readout mechanism, not an advantage over ordinary excitation; widening the legal continuation to reset `w` before the read should kill this proof.

## Idea cards

**P** = candidate primitive only if reuse beats the stacked control; **I** = improvement or falsification test. All first tests are CPU-scale proposals.

### Prove what the ordered bundle buys

#### 01. Carry both the winning sequence and its smallest obstruction (P)
- **Mechanism:** Freeze the bundle plus a small set of hidden counterhistories covering failures of every shorter sequence/reply pair; carry the two proofs independently.
- **Novelty vs nearest prior art:** MTT matches trajectories and [counterexample-guided repair](https://arxiv.org/abs/2301.11342) works with failed obligations; the extra bet is cheaper transfer of both upper and lower bounds without a new search. This extends parent #03, not a new claim about curriculum.
- **Cheapest first test:** In the three-example fixture with repeats allowed, enumerate a source class; send the proof to one held-out family preserving both obstruction worlds and one dropping a world. Compare with cached exact search, a cached MTT sequence, and full re-verification. The second family should accept the effect but reject the size claim.
- **Old-task retention check:** Independently verify both A lanes and C at every live teaching and reply prefix for the original and held-out families.

#### 02. Transfer just the order edges that matter (I)
- **Mechanism:** Export a partial order over examples only when every linear extension preserves the common reply; let the importer schedule around its fixed local stream.
- **Novelty vs nearest prior art:** MTT and [Reach-Avoid Problems with Time-Varying Dynamics](https://arxiv.org/abs/1410.6445) already cover sequence construction; the question is whether sparse order constraints validate cheaper than replaying every interleaving, not whether order matters.
- **Cheapest first test:** Add two decoupled truthful writes and one reflected gate to a four-step menu. Compare exact permutation search, stored total order, and pairwise commutation alone; the reflected gate should break at least one unsupported linear extension.
- **Old-task retention check:** Require A/C on every served interleaving, including one with a safe endpoint and unsafe intermediate C.

#### 03. Publish the smallest set of short alternatives you must rule out (I)
- **Mechanism:** Group shorter sequences by their certified failure obligation and share one obstruction per group, retaining a completeness certificate for the grouping.
- **Novelty vs nearest prior art:** Antichain games already compress sets of states; this asks whether the *lower bound on truthful examples* compresses separately from the winning recipe rather than offering a new search algorithm.
- **Cheapest first test:** Add six decoys with identical gradients before the gate but different gradients after it; compare grouped proof, plain exhaustive failure table, and antichains on the exact finite graph.
- **Old-task retention check:** Use actual A/C or new-utility failures to justify exclusions; a larger B loss alone does not disqualify a shorter bundle.

#### 04. Separate ordered magic from honest feature complementarity (I)
- **Mechanism:** Credit ordered irreducibility only if no order-free control with the same approved examples and legal update work gives the same no-split decision.
- **Novelty vs nearest prior art:** [Dataset Distillation](https://arxiv.org/abs/1811.10959) and GCR already exploit interacting samples; this is the causal audit for order, not a revival of the killed Lyapunov predictor.
- **Cheapest first test:** Compare both permutations, repeat-sample controls, an additive-gate ablation, and MTT; include a matched batch only in a separately declared law that permits it. Hold presentations and step budgets explicit.
- **Old-task retention check:** Compare only arms with matched A/C floors and immediate edit utility; report a reverse order failing C separately from a reverse order failing to enable the reply.

#### 05. Include a reply-set decoy, not just a high-gradient decoy (I)
- **Mechanism:** Plant a short lesson that makes the nominated reply fail but enables a different common reply; require any minimum proof to search the entire fixed reply menu.
- **Novelty vs nearest prior art:** Imperfect-information safety games already quantify over actions. Here this is a falsifier for claiming smallest *bundle* when only the smallest lesson for one preselected reply was shown.
- **Cheapest first test:** Add a legal alternative common repair on a third gate, then blind which gate is affected by the singleton. Compare nominated-reply search against joint exact search.
- **Old-task retention check:** Match new utility, A/C, and repair cost for the two common replies so the singleton is a genuine counterexample.

#### 06. Carry a boundary across which the same bundle stops saving a split (P)
- **Mechanism:** Export a lower bound on shared-reply slack as a function of the editor's public damage envelope; shrink scope or restore the split at the boundary without refitting examples.
- **Novelty vs nearest prior art:** Reach-avoid and parent #01 already cover scope; the additional reusable output is a checked change in *minimum sensing* with a frozen recipe and an explicit rival-reply control.
- **Cheapest first test:** In the gated fixture sweep asymmetric rectangular damage envelopes around the threshold. Compare fresh verification, cached probe answers, and fixed-bundle boundary checks; allow the exact planner to select any menu reply.
- **Old-task retention check:** Plant one rare A lane with tighter effective damage and one C lane affected by the repair budget; both must constrain the boundary.

#### 07. Price repeated lessons without charging the same installed effect twice (I)
- **Mechanism:** Track whether a previously installed bundle still covers the next blind editor; compare keep, replay, and buy-a-split under one frozen stream.
- **Novelty vs nearest prior art:** GCR and the parent's #19 already motivate repeatable savings; the distinct test is whether minimum bundle length matters once maintenance and repeated proof lookups dominate.
- **Cheapest first test:** Enumerate a six-offer stream with one public gate decay and one unused bundle. Compare exact stream planning, routine replay, and a charged cached policy at equal utility.
- **Old-task retention check:** Audit A/C after maintenance as well as after every editor; repeated small losses must not reset the acquisition anchor.

### Make a common reply reveal momentum through a fixed probe

#### 08. Certify a next-reply partition, not a slot decoder (P)
- **Mechanism:** Carry the proof that every fixed-probe bin after a common reply has a common next reply; do not promise to recover momentum.
- **Novelty vs nearest prior art:** FLEX designs informative actions, and [Causal Belief Decomposition for Planning with Sensing](https://arxiv.org/abs/1909.13778) reasons over beliefs. The narrower bet is reusing one checked reply partition across held-out editors without rerunning excitation or belief search.
- **Cheapest first test:** Quantize the momentum fixture into two bins, add two aliases with the same next action and an adversarial alias requiring the opposite action. Compare a dynamics-fit excitation arm, exact belief planning, and frozen-partition reuse.
- **Old-task retention check:** Check the common repair and bin-specific next reply on every history, including the rare alias with the least A headroom.

#### 09. Keep the revealing reply fixed when sign conventions change (I)
- **Mechanism:** Transfer only when the probe-to-reply relation is invariant under public coordinate conventions, or when a priced public translation is sufficient; never fit the sign to hidden cases.
- **Novelty vs nearest prior art:** FLEX and the slot-transport ideas in [PR #178](https://github.com/manojbajaj95/cl/pull/178) already address dynamics/representation. The test distinguishes transport of the readout certificate from moving or inspecting optimizer state.
- **Cheapest first test:** Reflect an auxiliary axis in two hosts while freezing the reply and probe instrument; include one reflection of dynamics alone and one with the interface transformed consistently. Compare nominal reuse, a public sign map, and fresh excitation.
- **Old-task retention check:** Audit both post-read specialists after the reflection; a sign swap invisible to immediate A/C is not an admissible import.

#### 10. Ask whether the reply creates information or merely preserves it (I)
- **Mechanism:** Factor the common repair and lawful momentum step; credit only the incremental fixed-probe decision gain over waiting or doing the same continuation without that step.
- **Novelty vs nearest prior art:** Standard active excitation (FLEX) distinguishes action from passive identification; this applies the control to parent #12 rather than claiming a new source of observability.
- **Cheapest first test:** In the quadratic fixture give both worlds a mandated later update that exposes velocity anyway; shorten the deadline in one arm and vary pulse presence factorially. Match elapsed time and updates with a neutral action where lawful.
- **Old-task retention check:** Compare identical acquisition margins and certified first service; an unsafe waiting arm is not evidence for extra information.

#### 11. Require a gap that survives both rounding and the next lawful writer (I)
- **Mechanism:** Bound the worst-case distance between conflicting histories' *sets* of possible fixed-probe observations under quantization and allowed continuations; fail closed on overlap unless the overlapped cell is still serviceable.
- **Novelty vs nearest prior art:** [Conformal Prediction Under Covariate Shift](https://arxiv.org/abs/1904.06019) can provide statistical coverage under assumptions; this is a finite worst-case action guarantee, not a coverage theorem or the killed switched-Gramian proposal.
- **Cheapest first test:** Cross two momentum values with three legal intervening gradients and two rounding widths. Compare nominal gap, exact cell enumeration, a sampled interval, and a public interval bound.
- **Old-task retention check:** Include a C margin sensitive to the intervening writer and independently check all rounded-cell policies, not just their centers.

#### 12. Certify a no-reveal region before spending on a split (I)
- **Mechanism:** Identify reply/probe combinations that cannot change an unresolved action conflict for any lawful common reply, despite momentum being distinguishable to a privileged reader.
- **Novelty vs nearest prior art:** [Footprint counterfeits (PR #107)](https://github.com/manojbajaj95/cl/pull/107) already exhibit nullspace twins; the test asks for a reusable negative decision about the entire lawful reply menu, not a stronger observability theory.
- **Cheapest first test:** Use two quadratic coordinates with the fixed probe reading only the first and momentum differing only in the second. Compare a decoupled menu with a single predeclared coupling option; benchmark exhaustive impossibility against a block-support proof and direct slot access.
- **Old-task retention check:** The coupled arm counts only if it retains A/C and new utility. When no lawful option exists, record refusal or a paid split, not a successful no-probe service.

#### 13. Avoid a reveal that only works because a later editor was silenced (I)
- **Mechanism:** Check the next-reply partition over all frozen continuations, including a lawful writer that erases the momentum readout without otherwise changing the next obligation.
- **Novelty vs nearest prior art:** Imperfect-information games already quantify over transitions, and parent #10 names the continuation problem; the momentum-specific test separates loss of the revealing signal from loss of the underlying obligation.
- **Cheapest first test:** Add a legal auxiliary reset to the two-step fixture and enumerate both timings relative to the probe. Compare a no-reset proof, robust belief planning, and a priced earlier read only where declared legal.
- **Old-task retention check:** Make the reset harmless to A/C on its own and verify that the failure is an unresolved next reply, not damage caused by the reset itself.

#### 14. Make the scarce resource the next decision's deadline (I)
- **Mechanism:** Admit a common reply only if the fixed read arrives before the last instant at which each observed cell can still be served. Extra discrimination after that point has zero value.
- **Novelty vs nearest prior art:** Time-varying reach-avoid and [split-timed deadlines (PR #180)](https://github.com/manojbajaj95/cl/pull/180) already handle deadlines. This prices the lag of a fixed momentum readout against the best immediate split.
- **Cheapest first test:** Enumerate two equal-cost common replies that reveal on step one or step two, with one next offer due in between. Compare an information-maximizing tie-break and exact deadline-aware dual control.
- **Old-task retention check:** Verify live prefixes while waiting and both A/C floors at the original deadline; never extend the deadline to recover a failed arm.

### Test whether the two promises are worth carrying together

#### 15. Carry a certificate for the shortest *revealing* lesson (P)
- **Mechanism:** Use a frozen sequence whose minimum length is certified for a first reply that both serves now and reveals the next decision under the fixed read. Record the minimum for immediate service separately.
- **Novelty vs nearest prior art:** Parent #15 already teaches the gateway; MTT plus dual control can find it. This card requires a portable bound on the extra teaching cost of the reveal and reusable sufficiency, not just a joint plan.
- **Cheapest first test:** Make a singleton enable the silent repair and an ordered pair enable the revealing one. Factor lesson choice and reply choice, then compare the best cached stack at equal search and evidence budgets on new editors. Use the exact joint oracle to verify both minima.
- **Old-task retention check:** Match immediate A/C and new utility between taught arms; check later A/C after each second-round specialist and each hold-out continuation.

#### 16. Keep the teaching proof when only the reveal expires (P)
- **Mechanism:** Give the importer two independently revocable claims: retain the first common reply when momentum behavior changes, but buy a second-round split if the revealing partition no longer holds.
- **Novelty vs nearest prior art:** Parent #21 already calls for compile-or-withdraw, and imperfect-information planning can compute the fallback. The extra wager is lower invalidation work when only one part of a joint artifact is affected.
- **Cheapest first test:** Change only the public momentum decay, then only the teaching gate, in a two-round finite model. Compare fine-grained revocation to an all-or-nothing cache and a factored off-the-shelf verifier.
- **Old-task retention check:** Check each surviving first reply on unchanged A/C anchors; never execute a stale second reply on the strength of an intact teaching proof.

#### 17. Prove a shorter lesson is sufficient only when the scheduled reveal is available (I)
- **Mechanism:** With two certified plans, compare a longer lesson that obviates a split even after a missed read against a shorter lesson whose safe next service relies on the read. Commit to an outage policy before deployment.
- **Novelty vs nearest prior art:** Parent #07 already insures probe outages and belief planning handles missing observations; the new question is the discrete extra number of truthful presentations needed to insure this specific two-round guarantee.
- **Cheapest first test:** On a three-example pool enumerate normal and missing-read histories, including no warning before first reply. Compare exact robust planning, fixed worst-case teaching, and a paid optional backup probe.
- **Old-task retention check:** Both normal and outage branches must independently retain A/C; report fallback latency and any lost edit utility.

#### 18. Use the same proof on editors that never share a realized edit (P)
- **Mechanism:** Freeze a verifier for a public interface shared by independent editor authors. Require blind transfers to new payloads and unseen momentum amplitudes without fitting either proof to their realized transcripts.
- **Novelty vs nearest prior art:** Nonparametric Teaching for Multiple Learners optimizes for multiple students; [certificate entry ports (PR #171)](https://github.com/manojbajaj95/cl/pull/171) already transfer proofs. The test is a one-way import that preserves both the common reply and readout at lower cost than a generic entry check plus fresh excitation.
- **Cheapest first test:** Hold out whole pairs of editor rules varying private output, amplitude, and legal continuation separately. Include an in-envelope difficult pair and an out-of-envelope same-transcript counterfeit. Match amortized costs against a cached source plan plus generic re-verification.
- **Old-task retention check:** Blindly evaluate each hold-out A/C independently, with the largest certified edit and smallest allowed momentum gap; outside scope must not be counted as admitted.

#### 19. Export a refusal that says what extra evidence would help (I)
- **Mechanism:** When transfer fails, distinguish a shorter-proof gap, nonoverlap of safe reply sets, and an aliased fixed-probe cell; route only to lawful data, a priced split, or refusal as appropriate.
- **Novelty vs nearest prior art:** Counterexample-guided repair and [decision-relevant queries (PR #174)](https://github.com/manojbajaj95/cl/pull/174) supply most of the mechanism. An explicit failure witness must beat asking the exact local planner; rewriting a lesson after failure is the ledger-killed baseline, not a novelty claim.
- **Cheapest first test:** Hide one example from the pool, add one infeasible editor, and coarsen one probe bin in otherwise identical finite instances. Compare the same-budget planner, rewrite-and-retry, and a frozen failure classifier checked against exact diagnoses.
- **Old-task retention check:** False admissions are not traded for speed; verify A/C on all fallbacks, including refusal on the unchanged live host.

#### 20. Test whether the shared reply is paying for information by spending retention slack (I)
- **Mechanism:** Compare revealing and silent replies at matched immediate service, output change, and A/C headroom, and charge the second-round slack they consume.
- **Novelty vs nearest prior art:** FLEX and parent #11 already price excitation and separation; this is a margin-confound audit from the ledger, not a new diagnostic score.
- **Cheapest first test:** In the quadratic toy add a protected slice depending on the same direction as the probe. Search for matched-slack reply pairs in the frozen menu, then compare with a behavior-only repair plus active split.
- **Old-task retention check:** Match slice-level acquisition margins, inspect both the intermediate momentum excursion and the next offer, and report when no fair matched pair exists.

#### 21. Try to compile the artifact away at the same cost (I)
- **Mechanism:** Compare the proposed dual proof to a plain saved teaching sequence, reply policy, and shared subproof cache built by a generic verifier. Demand a held-out cost advantage, not a different serialization.
- **Novelty vs nearest prior art:** MTT, [imperfect-information games](https://arxiv.org/abs/0706.2619), and [Causal Belief Decomposition](https://arxiv.org/abs/1909.13778) cover the parts. This is the ledger's stacked-baseline gate.
- **Cheapest first test:** Mix both fixtures across eight held-out finite families, including one where full recertification is required. Tabulate equal certified service against setup cost, cache bytes, reads, and incremental verification. Report the reuse count needed to break even, if any.
- **Old-task retention check:** Independent exact A/C adjudication for every arm; a win from ignoring live prefixes or rare continuations fails the gate.

#### 22. Scramble editor identity while keeping the true need fixed (I)
- **Mechanism:** Randomize editor IDs, delivery order, and private outputs independently of the slot-to-next-reply relation. Check that apparent learning cannot be reproduced by identifiers, a cached answer, or a changed read.
- **Novelty vs nearest prior art:** Parent #14 already audits a side channel, while causal belief planning accounts for known histories. The test here specifically falsifies a claimed momentum reveal without a privileged runtime slot read.
- **Cheapest first test:** Blind the policy to all metadata except the declared transcript and public eligibility interface; pair identity-scrambled worlds with the same probe trajectory, then swap the lawful pulse's curvature without changing metadata.
- **Old-task retention check:** Check that the old A/C decision follows the true next obligation after scrambling; reject a seemingly correct private-output prediction with a wrong repair.

## Ranked deeper questions

1. **Can a frozen shortest bundle transfer to genuinely unseen hidden editors without new trajectory search?** Start with #01, #05, #06, and #18. Prove source minimality over the whole menu; on import distinguish a preserved effect from a preserved lower bound. Demand a held-out cost win over a cached exact sequence plus ordinary re-verification at the same service. A fixture whose gate truth hard-codes the published result only calibrates the test.
2. **Can an equal-cost common reply reveal exactly enough momentum to change the next safe decision?** Use #08 and #10–#14 against matched active excitation, behavior-only repair and the exact belief oracle, with the same fixed read and next deadline. The strong result survives adversarial aliases and continuations; the honest negative result identifies an action conflict that no lawful reply separates.
3. **Is the shortest revealing lesson more than the sum of teaching and dual control?** Use the factorial in #15 and the invalidation test in #16; compare the best stack of teaching, repair, active sensing, and caching. The joint claim pays only if the two promises together admit the same offers more cheaply, including the cost of failures when one promise expires.
4. **Where is the first honest break-even point?** Use #07, #17, #20–#22 to vary reuse, baseline headroom, and outage frequency independently. If a paid split, ordinary replay, or a generic proof cache wins on the same A/C and utility floors, narrow the claim to that regime rather than reporting an unconditional saving.

**Verdict:** Keep both score-3 directions open. The strongest candidate is a shortest ordered recipe whose no-split effect can be checked on blind imports more cheaply than it can be rediscovered; the momentum reveal earns a place in that artifact only if it buys a certified next decision on the unchanged probe. Without those wins, the result is a machine-teaching or dual-control improvement, not a new continual-learning primitive.
