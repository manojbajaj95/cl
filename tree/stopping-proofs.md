# Stopping proofs: earn the right to delete an open question

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Decision-relevant queries](decision-relevant-queries.md) ([PR #174](https://github.com/manojbajaj95/cl/pull/174)), cards 05 and 22. **Review seeds:** [Flood triage](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/flood-triage.md#L277-L278) keeps both at score 3 and adds the deadline/bridge test in the round-43 update's PSP11 (the first row's umbrella was renumbered PSP13). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/idea-ledger.md). PSP11 joins [indistinguishable edits](https://github.com/manojbajaj95/cl/pull/173) card 08 with [irreversible splits](https://github.com/manojbajaj95/cl/pull/172); the reviewer did not find a merge that beat its best parts.

## Is a certified license to forget unresolved questions a new object for continual learning?

**Not as a decision to stop asking.** [Value of information](https://doi.org/10.1109/TSSC.1966.300074), optimal stopping, [fixed-confidence best-arm identification](https://arxiv.org/abs/1602.04589), branch-and-bound, and value-directed compression already tell us when more distinctions cannot sufficiently improve a decision. [Certified CL](https://arxiv.org/abs/2407.06697) and [APRNN](https://arxiv.org/abs/2304.03496) certify retained properties or repairs, not the opportunity cost of removing the evidence needed to tell candidate repairs apart.

**Conditional primitive:** a compact, independently checkable license to *actually delete* the working state of still-unresolved questions, then continue useful training and repair without it. The license says what was not learned, how much forgoing that knowledge can cost for a declared decision, and where reliance must end. Tomorrow's witness can make a distinction genuinely moot rather than predict its answer; a bridge can make a late answer unnecessary. Neither proves the underlying hypotheses equivalent. If an ordinary stack of stopping bounds, value-directed compression, checked repairs and deadline-aware planning gives the same utility, retention and costs, keep the stack and drop the primitive claim.

### What a license proves

- **Freeze scope before deletion.** Bind the learner version (including optimizer/sampler state where relevant), transcript support, legal interventions and observations, editor payloads, witness menu and prices, protected sets and tolerances, and served-prefix horizon. Let `X` contain *all* histories and edits consistent with what is retained, not just those a model predicts. Freeze new-task utility requirements; impose old-task A/C floors on every served prefix. Withholding is an explicit, priced outcome, not an admission. A license is not an authority to deploy a repair; that repair still needs its own safety and utility proof.
- **Separate ignorance from regret.** Check a safe incumbent `a` over `X`. For each `x`, let `c*(x)` be the cheapest legal safe matched-utility outcome if `x` were given for free at decision time, including any lawful probe/training paths whose non-informational effects could make repairs cheaper. Let `L(x) ≤ c*(x)` be an independently checkable lower bound. Certify `sup_x [c(a,x) − L(x)] ≤ ε`. If paths are simplified in the relaxation, they must only make the oracle more powerful; dropping cheap paths can make the bound unsound. This stronger-than-necessary regret bound covers joint/adaptive questions and is gross of information costs. A tighter comparison may bound only the best lawful timely policy that uses the omitted data, but must state its comparator. An expected or high-probability variant must name its law or failure budget; neither weakens hard A/C checks. Include refusal prices in comparable policy cost and report admissions separately so refusing cannot masquerade as a cheap repair.
- **Keep proof and obligations; remove detail.** Keep the incumbent witness reference, versioned scope predicate, bound and replayable proof or proof summary, plus the independent retention evidence. Delete the covered answer logs, hypothetical branch tables and restart/checkpoint state from the deployed store; no silent access via a verifier, cache, backup or teacher. The test harness may keep an isolated oracle for scoring. Expiry or a new menu, price, horizon or transition invalidates reliance *before use* absent a checked transport or residual bound. It does not resurrect deleted state: take a checked fallback, reacquire legally if possible, or withhold and pay for it. Deletion here is not a privacy or machine-unlearning guarantee.

**Paper case.** A frozen offer has a universally verified witness of cost 4. A specialist may be authorized by learning an unresolved bit, but even the clairvoyant safe repair costs at least 3. The verified incumbent and a checkable lower bound of 3 give a one-unit license even if the question is perfectly informative and free; the detailed bit table can go. Add a lawful witness of cost 1 in one world and the old proof no longer certifies one unit on the enlarged menu. This only checks the arithmetic; the research test is whether the proof remains smaller and cheaper than keeping the information, including the cost of being wrong about future scope.

### Use a witness to settle tomorrow's decision; don't wait past the repair

- **Prefer elimination over concealment.** Compare witnesses that independently meet today's frozen offer. For an already-pending, independently frozen second offer, prefer a witness that pushes its successor states into a region with a single independently checked and timely reply under all unresolved histories, *if* the saved future acquisition/repair work pays for the extra training and proof. Check the same offer, utility and served-prefix A/C before and after the intervention, including in histories no longer observable to the learner. A common prediction, common refusal, or lost ability to express a C failure is not a common reply. Dual control may instead make tomorrow's distinction cheaper to observe; measure that as a separate alternative.
- **Charge the answer's entire critical path.** For each probe answer group partitioning `X`, find a common reply and a latest safe decision time over every compatible history/edit in that group under verified transient cover. Account for answer latency and the time to check, fit and deploy the reply, without counting those steps twice if already in the deadline model. Authorize only when the worst allowed timing for *each* group fits a feasible window, with cover at every served prefix until the reply is effective. An early answer is insufficient when one group has no common reply. Isolated late feasible times do not imply early feasibility; use a checked window unless earlier placement is proved monotone. On miss, teacher and verifier must already have time to install a **truthful** early bridge: a lawful training witness that gives all compatible states a common safe reply. No safe affordable bridge means fall back or withhold, not probe anyway.
- **Deadline sanity pair.** Let the incumbent cover A/C through turn 2; a fast probe yields a branch at turn 1 and its one-turn reply lands by turn 2. The otherwise identical slow probe returns at turn 2 so the reply lands at turn 3; even a perfect answer earns no permission. A verified turn-0 bridge completed by turn 1 can instead make both branches use the same reply by turn 2. Also test a smooth-decay version (the ledger's replay-deadline null) and a fake bridge that passes the training checks but loses a held-out C slice. Neither planted cliff nor fake convergence is evidence for novelty.

### Common controls and gates

- **Stack the strongest controls.** Persistent exact EVSI with memoization and the same future offers; exact delayed belief-state planning and a perfect-information relaxation as references, not oracles to beat on their own objectives; branch-and-bound/value-directed compression plus an equal-byte checked repair cache, verification, and reacquisition; cheap specialist, dual-control replies, independent EVSI at the same horizon, and [trajectory matching](https://arxiv.org/abs/2203.11932) plus verification; probe-first, teach-first, #173 card 08 without deadlines, #172 card 01 alone, and delayed information value in a POMDP. Give the stack the same lawful witnesses, bridge repertoire, timing and verifier. Ablate deletion, witness choice and deadline gating separately and together.
- **Compare frontiers, not convenient denominators.** Blind editors issuing frozen jobs just inside and just outside scope; predeclare cost units and tolerances. Count persistent and peak bytes (including proof/verifier dependencies), proof construction and checking, teacher and query work, wall-clock latency, false authorizations, missed safe jobs, reacquisition and refusal. Match useful new-task progress and check independent ordinary A/C tasks at every served prefix, including rare slices. When truth is noisy, check reliability first; for ordering claims match margins. Replicate surprise-mined effects before inference (ledger: at least ten seeds).
- **Kill the primitive claim** if the proof/state savings vanish after accounting, the equal-budget stack ties, the effect needs a planted cliff or a narrowed/softer target, or an admitted prefix violates A/C. A cheaper solver or better training objective alone is an improvement, not a new object. **P** marks a conditional primitive (a reusable object or operation); **I** marks an improvement or audit, not a pilot recommendation under the ledger. All first tests below are paper/CPU proposals, not results.

## Idea cards

### License deletion, not merely stopping

#### 01. Proof that outlives its question table (P)
- **Mechanism:** Prove an upper bound on incumbent regret over a compact relaxation of the transcript-consistent histories; ship the bound and decision scope but delete the table and its generating traces.
- **Novelty vs nearest prior art:** Branch-and-bound certifies an optimality gap; [Certified CL](https://arxiv.org/abs/2407.06697) establishes old properties under updates. The candidate is a reusable deletion authorization for future editors with neither access to the table nor permission to call its generator.
- **Cheapest first test:** Enumerate an eight-world repair library with removable nuisance columns; hand only the license to two blind editors. Compare the memoized EVSI/branch-and-bound stack with a matched-byte repair cache; make one job just outside scope.
- **Old-task retention check:** Test ordinary A/C before deletion, after each admitted edit, and after recourse when the outside editor changes a C-only margin.

#### 02. A gap bound for a question bundle that no singleton can answer (I)
- **Mechanism:** Use a perfect-information relaxation to bound the full subtree of unresolved queries, rather than summing singleton EVSIs; tighten with feasible observations only if the loose bound cannot clear the deletion threshold.
- **Novelty vs nearest prior art:** [Information-relaxation duality](https://doi.org/10.1287/opre.1090.0796) already bounds sequential decision value by relaxing information constraints. This is a CL application with matched legal repair paths, not a new upper-bound method.
- **Cheapest first test:** Exhaust a two-bit XOR repair family where either bit alone has zero value and the pair changes the winner; add a cheap universal incumbent and check when deletion becomes legal. Compare singleton EVSI and exact joint planning.
- **Old-task retention check:** Keep a parity branch whose cheap specialist damages C; enumerate both A/C tasks after the incumbent and each authorized specialization.

#### 03. A license with a region of valid prices (P)
- **Mechanism:** Compile the regret proof into a small region in acquisition/repair price space, then let a new editor verify that a price update remains inside instead of invalidating at every fluctuation.
- **Novelty vs nearest prior art:** [Decision-focused optimization](https://arxiv.org/abs/1809.05504) and parametric optimization account for decisions under costs. The candidate is an importable sensitivity certificate for crossing a priced boundary *after* its source branches have disappeared.
- **Cheapest first test:** Enumerate cost planes for three witnesses; switch first to an in-region price and then just across a breakpoint. Compare exact sensitivity analysis plus a cache with the same byte cap.
- **Old-task retention check:** Include a newly cheap but unsafe specialist; check held-out C and ordinary A after every legal price-triggered switch, keeping price out of the safety floor.

#### 04. Anytime statistical stop with an explicit deterministic safety floor (I)
- **Mechanism:** Build a time-uniform upper bound on the expected repair gain of a finite probe-policy class and delete its rollouts once the bound is small; keep a separate exact A/C checker and allocate error probability across adaptively issued licenses.
- **Novelty vs nearest prior art:** [Confidence sequences](https://arxiv.org/abs/1810.08240) and [fixed-confidence identification](https://arxiv.org/abs/1602.04589) already support adaptive stopping. This is an empirical cost-bound arm, not proof that rare old behavior is protected.
- **Cheapest first test:** Enumerate Bernoulli repair-cost processes with identical initial means and one rare large gain. Compare fixed-time, anytime and exact finite-world bounds at a declared error level.
- **Old-task retention check:** Check both old tasks in the rare state independently of the cost sample; reject deletion reliance if the retained witness lacks a separate prefix guarantee there.

#### 05. A proof budget for deleting questions in stages (P)
- **Mechanism:** After each deletion prove regret of the next compressed decision policy relative to the same scoped previous policy; compose pointwise differences, charging only within a common valid scope. Refuse another deletion when the residual budget is exhausted.
- **Novelty vs nearest prior art:** [Adaptive composition accounting](https://arxiv.org/abs/2203.05481) and contract composition already meter cumulative claims; their guarantees are not regret guarantees. The candidate is a payable, independently checkable right to remove another tranche with earlier tranches gone.
- **Cheapest first test:** Three nested finite transcript partitions with one correlated loss term; compare joint compression, staged summation and a bad accounting rule that adds singleton EVSIs.
- **Old-task retention check:** Re-run routine A/C after each deletion and ensuing edit; neither residual budget nor overlap permits accumulated retention loss.

#### 06. A lower bound on what cannot be forgotten (I)
- **Mechanism:** Construct a family of future menus where each exposes a different hidden bit as the only cheap legal repair. Bound the minimum retained information from the distinguishable reply patterns when sources cannot be reacquired.
- **Novelty vs nearest prior art:** Communication complexity and [linear pure exploration](https://arxiv.org/abs/2007.00953) already distinguish decision-identifying information from raw data volume. The result would delimit, not instantiate, the CL primitive.
- **Cheapest first test:** Enumerate all kept states for a four-bit menu-index game with random blind menu arrival; measure worst-case refusal or regret at each byte cap against a flat table.
- **Old-task retention check:** Give each wrong specialist an independent old-task sentinel and independently verify any safe common fallback; report refusal rather than allowing wrong replies.

#### 07. Deletion that a second verifier can actually audit (P)
- **Mechanism:** Design a proof summary whose checker runs in a sandbox with only declared inputs, and make the removal test fail if any dependency attempts to read dead evidence. Retain a scope proof, not reliance on a digest as evidence of completeness.
- **Novelty vs nearest prior art:** [APRNN](https://arxiv.org/abs/2304.03496) certifies specified behavior after a network repair; ordinary proof checking can validate derived facts. The proposed interface certifies negligible decision regret and verifies under deliberate loss of the proof's source tables.
- **Cheapest first test:** Give a tiny independent verifier a valid summary, a table-backed impostor and a truncated support claim; revoke the table handle and try all three on a blind editor.
- **Old-task retention check:** The checker must independently reject a license for an incumbent that passes the fit checks but breaks a held-out C slice; retest A on the accepted arm.

#### 08. Counterexample-only reacquisition after a scope cut (P)
- **Mechanism:** On a failed scope check, isolate a lawful reacquirable frontier that separates the new job from the old certificate, without reconstructing out-of-scope question tables wholesale. If none is available, fail closed.
- **Novelty vs nearest prior art:** [Counterexample-guided repair](https://arxiv.org/abs/2301.11342) already adds targeted counterexamples. The narrower candidate is a local recovery interface after physical deletion, not smarter refinement while the source is live.
- **Cheapest first test:** Delete two independent detail blocks, then introduce one optimizer-mediated cross-term. Compare one-block reacquisition, full replanning, and optimal counterexample-guided repair with the same source availability.
- **Old-task retention check:** Check A/C at the attempted boundary, during fallback, and after repair, including a variant whose necessary source never returns.

### Settle tomorrow's disagreement by teaching

#### 09. Pay today for a common reply tomorrow (P)
- **Mechanism:** Of two verified repairs today, choose the more expensive only if its successor relation proves enough savings on a frozen tomorrow offer to offset its premium. Keep the shared reply certificate rather than the hidden-state split.
- **Novelty vs nearest prior art:** Dual control acts to improve future inference; [trajectory matching](https://arxiv.org/abs/2203.11932) fits examples to guide adaptation. The proposed object is a checked reusable intervention establishing that a future observation need not be made at all.
- **Cheapest first test:** Solve a two-edit gate graph with a cheap specialist, a dual-control reply that makes inference cheaper, and a common-reply witness. Compare with exact belief-state planning and joint trajectory matching plus verification.
- **Old-task retention check:** Score A/C in both worlds after each edit, with a fake common reply that simply deletes the rare C behavior.

#### 10. A witness that settles a disagreement only in combination (P)
- **Mechanism:** Produce two separately safe training moves whose composed effect, but not either alone, gives the same tomorrow reply on every admitted history. Track their order and certificate obligations explicitly.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) composes assume–guarantee contracts and [trajectory matching](https://arxiv.org/abs/2203.11932) optimizes training sequences. The candidate is a composable witness of a *removed observation requirement*, only if the stacked baseline cannot match it.
- **Cheapest first test:** A two-slot optimizer where one move aligns a feature and the other clears its carryover; test both orders, each move alone and joint optimization at equal examples and proof work.
- **Old-task retention check:** Evaluate A and C between moves and after the next edit, including the superficially equivalent reverse order with an intermediate failure.

#### 11. Refund a query by widening what counts as one checked reply (P)
- **Mechanism:** Teach an observation-free reply that branches only on verified public input at execution, preserving legitimate context-specific outputs across hidden worlds. Certify it as a single lawful policy, without access to the deleted distinction.
- **Novelty vs nearest prior art:** [Programmatic runtime shields](https://arxiv.org/abs/2410.05641) synthesize safe policies over observed features. The candidate is a training witness that creates a safe public-input policy where none was deployable before; otherwise this is policy synthesis.
- **Cheapest first test:** Binary public context and a private optimizer bit; exhaust fixed replies, shield policies and reshaped learners under the identical input interface. Block any hidden-state input to the verifier at deployment.
- **Old-task retention check:** Verify A/C in both public contexts, including a pair of old requests requiring opposite answers; constant-output collapse does not count.

#### 12. A negative control that erases the failure, not the disagreement (I)
- **Mechanism:** Plant a witness that makes transcript observations identical by dropping a feature needed only for old C; contrast it with one that removes the need for a probe while preserving the feature's behavior.
- **Novelty vs nearest prior art:** [Learning without Forgetting](https://arxiv.org/abs/1606.09282) preserves old outputs during new training, and [APRNN](https://arxiv.org/abs/2304.03496) checks specified behavior. This is an adversarial audit against calling observability collapse a gain.
- **Cheapest first test:** A four-cell truth table and one forgotten gate; compare equality of observed outputs, common-reply feasibility, and common-reply feasibility with independent old checks.
- **Old-task retention check:** Query the deleted gate using fresh routine C examples, not the probe used to train the witness; make A unchanged so its success cannot mask the failure.

#### 13. A question-removing witness that survives a second editor (P)
- **Mechanism:** Verify one witness against a restricted family of future offers specified independently of the witness designer; keep a small entry test for the family instead of a separate answer trace per editor.
- **Novelty vs nearest prior art:** [MAML](https://arxiv.org/abs/1703.03400) prepares models for fast adaptation; [Certified CL](https://arxiv.org/abs/2407.06697) protects earlier specifications during retraining. The proposed artifact eliminates a paid measurement across blind editors by a checked successor condition.
- **Cheapest first test:** Fit on one of two editor families in a Boolean learner, freeze the witness, then challenge with a blind inside-family offer and an outside-family near miss. Compare equal-byte meta-learned initialization plus verification.
- **Old-task retention check:** Evaluate the same old A/C items after each independent continuation and after a serial continuation that the entry condition should reject.

#### 14. Measure the option cost of making one question moot (I)
- **Mechanism:** Charge a witness for any lost *other* safe future moves. Compare expected cost across predeclared future offers and worst-case refusal separately; do not reward a witness that succeeds only by shrinking the menu.
- **Novelty vs nearest prior art:** Constrained planning and [Constrained Policy Optimization](https://arxiv.org/abs/1705.10528) already value decisions subject to restrictions; this is an audit of a subtle CL cost, not a new planning objective.
- **Cheapest first test:** Exhaust three offered futures where the common-reply witness saves a query on one but destroys a cheap repair route on the others. Compare the greedy witness ranking with exact two-step planning.
- **Old-task retention check:** Keep A/C and today's target identical across arms; retest both old tasks on the future offers as well as on the matched present edit.

### Turn deadline claims into safe decisions

#### 15. An admissible probe has a reply in every answer cell (P)
- **Mechanism:** Attach to an unresolved transcript an answer-partition certificate, prefix cover, and an executable reply schedule for each cell. Probe only if each schedule fits its certified latest safe decision window.
- **Novelty vs nearest prior art:** Delayed POMDP information value and [safe model-predictive control](https://arxiv.org/abs/2102.12124) already plan under observation and viability constraints. The candidate is a reusable probe admission object coupled to CL repair windows that can be checked without the old trajectories.
- **Cheapest first test:** Exhaust the fast/slow timing pair and an on-time probe with one uncovered answer cell. Compare delayed belief-state planning, probe-first, teach-first, and #172 bisection alone.
- **Old-task retention check:** Measure ordinary A/C through the asynchronous wait and reply, not just at receipt or at the final model.

#### 16. Teach the bridge while it is still truthful and useful (P)
- **Mechanism:** Before spending a probe that cannot meet its deadline, choose truthful training examples whose verified effect gives all transcript-consistent states a common safe reply. Verify the training prefix and reject the bridge if it cannot be installed on time.
- **Novelty vs nearest prior art:** #173's data-for-sensing trade and [trajectory distillation](https://arxiv.org/abs/2203.11932) already spend examples to guide adaptation. The candidate is a checked substitution with a repair deadline and cover during learning; no claim if deadline gating plus #173 ties.
- **Cheapest first test:** A two-state ReLU learner with one valid and one mislabeled bridge; compare bridge-before-expiry, always-teach, #173 without timing, and an exact delayed planner with the same examples.
- **Old-task retention check:** Score both A/C tasks during fitting and after the common reply, including the hidden world where the mislabeled data superficially looks effective.

#### 17. Deadline intervals when recovery is nonmonotone (I)
- **Mechanism:** Represent feasible reply times as a set of windows rather than a single last time; propagate the windows through answer lag and reply duration. Refuse a deadline inferred by bisection unless monotonicity holds.
- **Novelty vs nearest prior art:** Reachability and [interval bound propagation](https://arxiv.org/abs/1810.12715) already bound reachable states; this is a safer implementation of #172's clock, not a new object.
- **Cheapest first test:** Enumerate four optimizer steps with a gate that closes then reopens. Compare exact windows, last-feasible cutoff and bisection on the same starts, including an answer that lands in the gap.
- **Old-task retention check:** Require transient A/C through the closed interval, not just agreement at two individually safe boundaries.

#### 18. A shared probe queue whose jobs can expire (I)
- **Mechanism:** Reserve worst-case probe, verifier and training time for all answer groups before admitting competing jobs; switch jobs to bridges if the combined schedule makes waiting unsafe.
- **Novelty vs nearest prior art:** Real-time scheduling and delayed belief-state planning already handle queues and deadlines; [Constrained Policy Optimization](https://arxiv.org/abs/1705.10528) is a policy-level constraint reference, not a per-prefix deadline guarantee. This is a workload stress test for the repair interface.
- **Cheapest first test:** Exhaust two simultaneous frozen edits, one verifier and a late-answer branch. Compare earliest-deadline-first, independent EVSI plus a shared queue, and optimal joint scheduling.
- **Old-task retention check:** Check the unaffected old task while another job blocks the verifier, and both A/C immediately after the delayed job is served or refused.

#### 19. Transient cover that can be revoked before the reply (P)
- **Mechanism:** Make a probe reservation revocable by a checked scope guard. Before launch reserve a safe bridge/fallback path for reachable invalidations, budgeting the check and the switch; if neither wait nor abort remains safe, don't launch.
- **Novelty vs nearest prior art:** [Runtime shields](https://arxiv.org/abs/2410.05641) already block unsafe actions. The candidate couples an abortable sensing commitment to an independently deployable learning reply under expiring cover.
- **Cheapest first test:** Exhaust a three-turn gate model with one mid-flight optimizer drift. Compare a robust fixed reservation, restart-on-drift, and shielding plus the same bridge.
- **Old-task retention check:** Evaluate A/C at the invalidation turn before switching, at every fallback prefix, and when a stale answer later arrives.

#### 20. Give the bridge and probe the same smooth-decay world (I)
- **Mechanism:** Sweep repair cost and checker margin from a planted cliff to a gradual ramp. Stop claiming a deadline interaction if policy advantage disappears at realistic decay or is reproduced by ordinary delay pricing.
- **Novelty vs nearest prior art:** Optimal stopping with delay already prices attrition. This is the [replay-deadline falsification](https://github.com/manojbajaj95/cl/pull/113) extended to the PSP11 probe/bridge substitution, not another claim that repair cliffs are common.
- **Cheapest first test:** Hold initial and final fit progress fixed in a finite ramp/cliff pair and enumerate probe/bridge policies; match delay, competing jobs and witness costs before comparing safe admissions.
- **Old-task retention check:** Use unchanged A/C prefixes and margin-matched rare old slices across both decay shapes; flag any apparent gain due to changing the difficulty of retention.

### Make the whole license earn its keep

#### 21. One deletion license for two independent publishers (P)
- **Mechanism:** Let independent publishers summarize removed question blocks against a common interface; combine their licenses only with a checkable cross-block regret bound and scope-intersection proof, not by assuming conditional independence.
- **Novelty vs nearest prior art:** [Assume–guarantee reasoning](https://arxiv.org/abs/2303.17751) and the parent's factored verification already compose local proofs. The candidate is decentralized deletion that still supports common/joint repair choices after both sources are gone.
- **Cheapest first test:** Merge summaries of a two-bit independent repair game and an XOR game with identical marginal tables; compare flat and factored branch-and-bound with the same cache. Reject the unsound XOR merge.
- **Old-task retention check:** Include a lawful combination with intact A and failed C, and verify each old task both before handoff and after the combined repair.

#### 22. Retire the question, then price the forced re-teach (P)
- **Mechanism:** Use the stopping proof for today's offer and a certified common-reply witness for the next one. After deletion, require any scope-expanding editor to re-establish its entry proof, reacquire legally, or buy a timed bridge without the old source. Count all these liabilities against the original savings.
- **Novelty vs nearest prior art:** [Value of information](https://doi.org/10.1109/TSSC.1966.300074), [Certified CL](https://arxiv.org/abs/2407.06697) and [trajectory matching](https://arxiv.org/abs/2203.11932) cover the pieces. The merge only survives if the transported deletion right and the witness together save work beyond a checked, deadline-aware stack of the parts.
- **Cheapest first test:** Three blind turns: cheap bounded regret, a genuinely shared reply, then a shifted menu with an unreachable source. Evaluate the full factorial of proof/deletion, future-oriented witness choice and probe deadline gating versus the strongest stack under a byte cap.
- **Old-task retention check:** Check A/C from pre-deletion through the refused/bridged shift; include a variant where only an obsolete checkpoint could repair C and count it as unavailable.

## Ranked deeper questions

1. **Can a scoped deletion license save total work beyond exact EVSI, verified compression and a checked repair cache, after physical deletion and blind scope changes?** Start with 01, 07 and 22. The win is equal retention and useful admissions with less retained evidence or less total reacquisition/proof work, not agreement in a fixed toy where the oracle already knows the answer.
2. **Can today's witness erase tomorrow's costly decision disagreement without erasing capabilities or merely buying cheaper information?** Use 09, 12 and 14. Require a common checked reply over the original support, frozen offer and untouched A/C, and charge repair routes lost on other pending demand.
3. **Does the PSP11 deadline/bridge interaction survive ordinary delayed planning and smooth decay?** Use 15, 16 and 20. Compare the planted one-step miss with the ramp, give the stacked baseline identical bridges, and look for real gains across admissible workloads rather than against an always-probe straw man.
4. **What is the minimum evidence that must survive deletion for safe reuse, revocation and composition?** Use 05, 06, 08 and 21. Seek a lower bound and a matching compact certificate for a nontrivial stream; if both collapse to the original table once menus vary, narrow the claim or retire it.
