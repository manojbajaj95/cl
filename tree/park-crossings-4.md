# Park crossings IV: inherit a safe next write

**Status:** Ideas only; no implementation, learner runs, or GPU work. **Parent:** [Park crossings III](park-crossings-3.md) ([PR #300][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** In [flood triage, rows 418–421][triage] ([PR #6][review-pr]), row 418 gives #300 two score-3 ideas: [#13, cancel the violation through the first successor write](park-crossings-3.md#13-cancel-the-violation-across-the-first-successor-write-p), and [#16, bank cancellation in a reachable envelope rather than a saved state](park-crossings-3.md#16-bank-cancellation-in-the-reachable-envelope-not-a-saved-state-p). Rows 419–421 grade other nodes; #300's independent-failure-domain idea was graded as an improvement, not a third seed.

## Contract and deciding controls

- Inherit the [parent contract](park-crossings-3.md#contract-and-deciding-controls). A is incumbent service (`A_park` plus an independently specified overdue repair, `A_rep`), B is successor service and C is an unrelated old task. A park is an accepted component of the deployed `A_park` set; an outbound or return crossing is a single native update between components. Freeze the truthful pool, native batch grammar and denominators, optimizer and its live slots, publications, observation times, service floors, and deadlines before choosing. No fake work, off-grammar writes, slot resets or hidden unsafe publications in a proposed arm. A reset is an explicitly off-grammar diagnostic control. Score every required task, including refusals or missed deadlines.
- For #13, the comparison is between a repair crossing that passes now and one that also passes *after the specified ordinary C update*, with no intervening edit. The repair must be individually unsafe under the same optimizer with legal solo normalization, contribute to unseen `A_rep`, and not merely dilute B. Match immediate service and per-item starting margins on calibration reads; use paired histories to separate slot effects from landing weights. In vanilla heavy-ball, identical input state and identical landing weights imply identical post-step velocity; to get an equal-weight slot contrast, use distinct legal prefixes, or an optimizer with additional observable state. Test that contrast before attributing anything to slots.
- For #16, a witness certifies an observed live state and its declared continuations, not a remembered weight vector. Freeze the legal suffix and future record menu before the steering choice. An accepted witness must give a lawful causal way to finish all due work: at each tick one action for histories still indistinguishable, only splitting after the relevant observation. At least one legal non-idle continuation must remain; do not obtain robustness by quietly banning required work. Check the success of joint repair+return, not bare return or resetting away-earned B.
- Match native writes, allocated bytes (including state summaries, samples and cached plans), preview calls, online decision latency and calibration access. For #13: #296#11 commit-only cancellation, [GEM][gem]/[A-GEM][agem], two-step projected rehearsal, receding-horizon viability, both separate orders, legal damping, and reset as a diagnostic. For #16: #296#05 bare-return steering, [robust predecessor sets][viability], [return corridors][corridors], and equal-byte compressed snapshot **plus** the replay needed to restore B and finish the repair. For joints: matched causal stacks of those controls and exact augmented-state search as a tiny-instance ceiling. If ordinary control methods tie at equal cost, don't claim a primitive. Every first test is a proposed finite CPU/paper test; the novelty comparisons identify controls, not verified gaps in the literature. **P** means candidate primitive; **I** means improvement/audit.
- On all tested trajectories report held-out ordinary A and rare C at each publication, drifted held-out `A_rep` at its deadline and after the following write, and already-earned B through both crossings. Card-specific retention checks below add stress cases. Keep the final retention inputs separate from the inputs used to construct the witness.

## Idea cards

### A repair that remains safe through the next required write (#300#13)

#### 01. Sell a repair crossing with a named successor (P; seed anchor)
- **Mechanism:** Admit a native A+B batch only if the requested C batch remains executable from the actual weights and slots left by the crossing. The contract names that C job, not a generic small next step.
- **Novelty vs nearest prior art:** This restates #300#13, not a novelty claim. Two-step projected rehearsal and augmented-state lookahead viability already check sequenced safety; they are the controls.
- **Cheapest first test:** On a two-component quadratic toy, compare two truthful due-B partners both safe at commit but only one safe after C. Enumerate both separate orders, damping, and the same C with reset versus native carried slots. Reject any purported slot effect if an equal-weight legal slot contrast cannot reproduce it.
- **Old-task retention check:** Test A at both publications and the first ordinary A read after C; verify unseen repair gain persists and rare C improves beyond its training example.

#### 02. Carry an admissible range of successor gradients, not one preview (P)
- **Mechanism:** Issue a signed interval of successor C gradients along the sensitive park direction (and bound the remainder). Accept a partner only when the ordinary C write stays safe for the whole declared range; invalidate outside it rather than clipping C.
- **Novelty vs nearest prior art:** [Tube MPC][tube] already propagates disturbance sets. The possible reusable unit is a successor-input contract transferable across truthful record arrivals and aligned to C's own required service, not propagation of an arbitrary perturbation ball.
- **Cheapest first test:** Use a scalar slot and three legal C gradients, two in range and one just outside. Compare point preview, a norm-ball tube and exact robust predecessor at equal preview count; reject if the signed range has no calibrated coverage or no decision-cost advantage.
- **Old-task retention check:** Test the held-out A example with least initial headroom at both range endpoints, and C and unseen repair in the interior as well; check that the out-of-range branch is reported rather than silently dropped.

#### 03. Index safety by slot sign even when A reads agree (P)
- **Mechanism:** Key a successor contract on the sign of the native momentum component that acts on the endangered A read. Let two legal prefixes land at the same weights and immediate A/B/C scores but with opposite momentum.
- **Novelty vs nearest prior art:** State augmentation for momentum is standard. The claim to beat is that a one-bit contract can be reused across prefixes at lower cost than simulating each live state, not that momentum exists.
- **Cheapest first test:** Construct opposite prefixes for scalar heavy-ball with equal endpoints, add the same truthful C batch, then extend to a rotated two-coordinate perturbation. Compare weight-only, full-state preview, and a magnitude-only bound; fail if the sign is insufficient within the declared range or buys no useful admissions.
- **Old-task retention check:** Evaluate identical held-out A and drifted-repair instances before and after C on both histories, alongside a C subtype whose training signal is unchanged by the sign flip.

#### 04. Trade the mean of a repair pair for its optimizer-state effect (P)
- **Mechanism:** Choose among legal A+B histories that land at the same weights with distinct native second moments. Make the next ordinary C step safe by changing its effective per-coordinate scaling, not its label, order, or step size.
- **Novelty vs nearest prior art:** Adam state-aware rollout is a direct control. Unlike #296's momentum prepayment, the proposed control surface is the *denominator* of the next required write at fixed current displacement; require the effect to survive beyond an optimizer reparameterization.
- **Cheapest first test:** Enumerate two legal Adam prefixes over a one-coordinate quadratic pool, matching the landing weights and first moment before the same C record in the slot-isolation arm. Verify the native epsilon and bias corrections in both paths. Compare an SGD arm and equal-byte full Adam lookahead; if only immediate margins can be matched, test the policy but don't attribute the effect to second moments alone.
- **Old-task retention check:** Test A slices on both the changed and unchanged coordinates after the crossing and after C; verify the old repair gain on unseen examples and check C service despite additional damping.

#### 05. Protect the outgoing A boundary, not just the crossing margin (P)
- **Mechanism:** Choose the B partner by which nonlinear A constraint is active *after* the C update, keeping a small witness for the outgoing boundary. Two equally deep initial landings need not have the same vulnerable read at the next publication.
- **Novelty vs nearest prior art:** Two-step [GEM][gem] and constrained line search are the controls. A useful object would be a safe-next-write witness tied to a changing active set; a static normal or prior destination-normal selector is not enough.
- **Cheapest first test:** Enumerate a two-dimensional park with two intersecting constraints on the destination component. Match initial margin and C progress, switch the active constraint at the C step, and compare fixed-normal selection, full rollout and a partner with the opposite boundary effect.
- **Old-task retention check:** Test both independent ordinary A subfamilies, including the one not active at commit, plus rare C and unseen drifted repair after the switch.

#### 06. Preserve the second C microbatch without freezing the first (P)
- **Mechanism:** If a C job is natively published as two indivisible microbatches, require the repair partner to leave enough headroom for the second even when the first is locally safe. The first batch remains due and is not replaced by a preview or extra update.
- **Novelty vs nearest prior art:** Receding-horizon MPC already handles multiple transitions. The candidate is a minimal contract at C's real publication boundaries reusable across alternative first microbatches, not simply extending #13's rollout length.
- **Cheapest first test:** Enumerate two first-C variants and one second-C record. Include a pair safe for either first but unsafe on one second transition; compare one-step rechecking, full three-step search and the contract at matched online previews.
- **Old-task retention check:** Check ordinary A, unseen repair, and rare C after each partial fulfillment; check the full C service floor only at its predeclared deadline.

#### 07. Make required C spend the inherited slot sensitivity (P)
- **Mechanism:** Among equally due C alternatives, exercise one that consumes rather than carries the dangerous momentum component across the next ordinary tick. A safe repair partner and a safe immediate C step are insufficient if their combined exit leaves an unavoidable future loss.
- **Novelty vs nearest prior art:** Scheduled momentum damping and #300#19 next-repair feasibility are direct comparisons. Candidate: retiring a particular carryover effect through owed service, not erasing a slot or selecting purely by next loss.
- **Cheapest first test:** Use one dangerous momentum coordinate and two matched C alternatives, then a common ordinary A update. Compare legal damping, lowest-motion C, exact lookahead and a same-sign C twin; require that it is the A step downstream, not an easier C target, that separates outcomes.
- **Old-task retention check:** Check the old A read sensitive to the carried component and an unrelated A read after C and after ordinary A work; require real rare-C improvement and persistent unseen repair.

#### 08. Charge for proving that no successor is safe (P)
- **Mechanism:** Return a small negative witness identifying a due C obligation and a live-slot range for which every legal A+B partner fails the same necessary successor condition. Invalidate it when the record pool, due job, or native optimizer changes.
- **Novelty vs nearest prior art:** Infeasibility certificates for robust control already exist. The candidate is a reusable refusal over a bounded class of *truthful repair batches*, with a checkable break condition rather than parent #300#22's aggregate absence audit.
- **Cheapest first test:** Exhaustively enumerate four partners where all land but all fail C, then insert one truthful admissible partner. Compare certificate cost and correctness with per-arrival enumeration and a mere park-margin refusal.
- **Old-task retention check:** On refusals report all due A/B/C outcomes under the actual fallback, including unserved repair; on witness invalidation check ordinary A and C after the newly admitted successor.

### Put a joint repair-bearing return in reach (#300#16)

#### 09. Buy a joint predecessor with due B, not a saved model (P; seed anchor)
- **Mechanism:** Choose an equivalent due B batch whose live-state successors all have a causal native repair-bearing return, with at least one genuine non-idle continuation.
- **Novelty vs nearest prior art:** This is #300#16, not a novelty claim. Robust predecessors are the direct formal prior; the difference from #296#05 is the target predicate, which requires substantive repair and work-preserving return together.
- **Cheapest first test:** Enumerate two B choices, one idle and one ordinary suffix per choice, and a common menu whose bare returns pass on every branch. Compare exact joint predecessor, bare steering plus repair and snapshot plus owed replay; include a pool where neither B choice qualifies.
- **Old-task retention check:** Score ordinary A, unseen repair and rare C on each actually reachable branch, with B retained after the return and the next write.

#### 10. Quotient away states by the joint continuation they admit (P)
- **Mechanism:** Group live away states only when the same causal repair-return plan works from all of them. Store the plan class and cheap membership facts, not member weights; if indistinguishable states require opposing first commitments, do not merge.
- **Novelty vs nearest prior art:** [Bisimulation/state aggregation][bisim] and #296#06 compressed witnesses are close. The possible contribution is sharing a witness for a particular repair-bearing continuation without requiring equivalence for every learner transition.
- **Cheapest first test:** Enumerate four weight/slot states and two truthful return plans with intersecting domains. Compare partition-by-margin, exact predecessor lookup, and plan-class membership amortized over repeated arrivals. Reject if classes cost as much to certify online as computing the plans.
- **Old-task retention check:** Test independent A, A-repair and C tasks separately in every merged state, including two with similar means and different worst old-task cases.

#### 11. Permit a narrow planned envelope to branch only after disclosure (P)
- **Mechanism:** Before a record's repair class is observed, require the same prefix choice for both classes. After disclosure, branch to different valid suffixes. Publish the common-prefix condition with the envelope, not a list of individually feasible histories.
- **Novelty vs nearest prior art:** Scenario-tree nonanticipativity and robust dynamic programming are the direct controls. Candidate: reuse an observation-indexed joint repair promise across due-B decisions without rerunning the whole tree.
- **Cheapest first test:** Enumerate two hidden arrival classes and two early prefixes; include a case with a feasible clairvoyant schedule for each class but no shared prefix. Compare open-loop robustness, causal exact search and a summary keyed by disclosure tick.
- **Old-task retention check:** Report A, unseen repair and rare C separately for both arrival classes, including the unavoidable missed obligation when a common prefix does not exist.

#### 12. Use complementary due-B choices to cover different drift intervals (P)
- **Mechanism:** Partition an observed away-state uncertainty interval into regions where different equivalent due-B batches buy a repair-bearing return. Require a decision boundary computable from preexisting live reads, with a refusal band if the observation cannot distinguish the regions.
- **Novelty vs nearest prior art:** Explicit MPC already partitions state into action regions. The reusable object would be a partition derived from truthful joint-service maps and deployable with existing reads, not general novelty in piecewise control.
- **Cheapest first test:** Fit the partition on a one-dimensional rational grid, then enumerate an exact finer grid near the boundary. Compare to always choosing one B, exact MPC, and a hidden-state oracle; collapse two observations into one to test whether the refusal band is necessary.
- **Old-task retention check:** Inspect worst held-out A and C in the overlap and refusal band, and require unseen repair on both admitted regions with no loss of away B.

#### 13. Preserve an envelope across a required old-task no-op on weights (P)
- **Mechanism:** Include an ordinary due C record whose native update changes optimizer state even if it has negligible weight displacement. Admit only due-B choices that leave the repair-bearing return possible after that real C job; weight-only reachability is insufficient.
- **Novelty vs nearest prior art:** Augmented-state robust predecessors are the key prior; unlike #300#06, this tests a *required intermediate write*, not two B moves with equal readouts. Any advance has to come from a compact record-aware witness.
- **Cheapest first test:** Look for a scalar heavy-ball C gradient that cancels inherited velocity, yielding zero displacement but clearing velocity under the fixed rule. Match C service how the actual deadline specifies it (already correct is acceptable only if the fixture's C obligation is to process the arriving record); compare live-slot, idle-tick and true no-write branches.
- **Old-task retention check:** Verify held-out C service is truly maintained, then test both ordinary A and distinct drifted repair after the return and the next ordinary write.

#### 14. Give a local reason an envelope cannot be entered (P)
- **Mechanism:** Find a signed obstruction that separates every legal due B successor from the repair-bearing predecessor, even though some reach a bare-return predecessor. Return which native B alternatives were covered, so the proof is invalidated by an actual pool change.
- **Novelty vs nearest prior art:** Separating hyperplanes and reachability dual certificates are established. Candidate: a cheap obstruction at the interface of a truthful batch grammar and a repair-bearing target, not reviving the ledger's structural-rank certificate.
- **Cheapest first test:** Enumerate a 2D pool with a single signed binding constraint, then add a lawful B alternative that crosses it. Compare per-batch preview, exact reachability, and a nearby nonconvex case where the linear certificate must abstain.
- **Old-task retention check:** Evaluate fallback A and C, score the missed repair explicitly, and verify unseen repair on the newly reachable branch after the ordinary follow-up.

#### 15. Test envelopes when the repair is an unknown member of a live old-task family (P)
- **Mechanism:** Define alternative overdue repairs by the old-task service each must actually deliver. A due B choice buys coverage of whichever one materializes, provided switching repair representatives after observation is lawful.
- **Novelty vs nearest prior art:** #300#12 chooses a drift-robust pair and adjustable robust control selects actions after observations. Candidate: a plan-class witness for families of repair-bearing returns, with per-family holdouts and no requirement to simultaneously fix mutually exclusive incidents.
- **Cheapest first test:** Enumerate two old-drift scenarios with equal apparent A margin and one bare return. Compare fixed representative, adjustable exact predecessor and snapshot/replay; use an incident whose record fits the geometry but does not fix its held-out service as a negative control.
- **Old-task retention check:** Evaluate unseen repair for each activated incident and nonincident A and C subtypes; score simultaneous activation separately if permitted, not as a covered exclusive case.

#### 16. Measure the cost of staying in the envelope under actual work (I)
- **Mechanism:** Price a witness by the fraction and latency of specifically owed away work still serviceable while the repair-bearing option is valid. Count the schedules a witness silently excludes, not just the states it admits.
- **Novelty vs nearest prior art:** Viability and [tube MPC][tube] already price conservatism; this is an audit of #300#16, distinguishing productive robustness from making the learner idle.
- **Cheapest first test:** Enumerate two away workloads sharing the same terminal repair menu, one with a binding ordinary B/C arrival. Compare permissive exact search and the compact envelope; a certificate that passes only by deprioritizing mandatory work loses.
- **Old-task retention check:** Score ordinary A, held-out repair and independent C in all workloads including restricted/refused schedules, and report delays and lost B rather than filtering to completed returns.

### Joint contracts: buy a return whose first ordinary write is already safe

#### 17. Take the predecessor of a repair-return followed by C (P)
- **Mechanism:** Let a due B choice steer into states admitting a joint repair-bearing return *and* the first required plus-side C step under the return's live slots. Require two present B choices with equal immediate service and equal **commit-only** joint return coverage but different safe-successor coverage.
- **Novelty vs nearest prior art:** The obvious control is an augmented-state [robust predecessor][viability] over the full two-update suffix. #300#13 and #16 stacked with full causal lookahead are the ceiling; only a reusable witness that saves online work or evidence bytes without losing coverage would advance the idea.
- **Cheapest first test:** Enumerate two B choices × two allowed away updates × two truthful repair-return batches, with a single due C. Check an instance where all returns pass at commit but at least one allowed branch cannot then complete C for one B choice. Compare exact search, the matched stack, equal-byte snapshot/replay and an off-grammar slot reset for diagnosis.
- **Old-task retention check:** Check ordinary A and rare C at the away publication, return and C; check unseen repair at return and after C. The same trajectory must retain B learned away.

#### 18. Bind a return witness to a successor class, not a particular late record (P)
- **Mechanism:** Partition future C obligations by which post-return slots they tolerate. During the away stay, index joint repair-return plans by that partition so an observation can select a lawful pairing without knowing exact batch identity in advance.
- **Novelty vs nearest prior art:** Contract-based control and #300#21 joint witness composition are closest. The candidate is a many-to-many interface joining a repair-bearing return with a named *successor service class*; separate existential coverage of returns and of C is not sufficient.
- **Cheapest first test:** Three late C records, two repair-return batches and an arrival tree with one observation before and one after commit. Compare exact causal joins and independently composed summaries; include a case where both summaries are nonempty but no common continuation exists.
- **Old-task retention check:** Test all covered C records on separate old examples, looking for a C class that shares a slot bound but fails service; verify ordinary A and unseen repair after C.

#### 19. Share one prospective proof in both crossing directions (P)
- **Mechanism:** Reuse a bounded set of update-response inequalities on the outbound repair's successor C and the eventual repair-bearing return's plus-side successor C. Admission needs a common truthful plan for both temporal phases, not two unrelated local proofs.
- **Novelty vs nearest prior art:** [Tube MPC][tube] and assume–guarantee contracts already reuse transition bounds. Possible advance: one checkable interface that survives inversion of the park direction while tracking genuinely distinct old repairs.
- **Cheapest first test:** Enumerate an outbound/away/return sequence with symmetric park geometry but different held-out repair objectives and an asymmetric slot-carrying twin. Compare separate direction certificates, the strongest stack, and shared bounds that must reject the twin or gain no reuse.
- **Old-task retention check:** Test each direction's unseen repair at its own deadline and after its own successor; test ordinary A and rare C after both crossings, not just at the restored side.

#### 20. Revoke a joint promise using the first real successor observation (P)
- **Mechanism:** After the outbound repair's first required C update, use the published read and observed native slots to discard counterfactual branches and narrow the available return plans. If there is no valid remaining plan, revoke and take a predeclared lawful fallback. On an in-contract history that is a false admission, not a successful guarantee.
- **Novelty vs nearest prior art:** Runtime assurance and receding-horizon viability already recheck constraints. The candidate is an incremental invalidation rule for a *paid-for* future joint repair promise using evidence already computed by owed service, not delayed safety discovery.
- **Cheapest first test:** Send two legal C variants through the same outbound crossing; both pass now, but each rules out a different planned return. Compare full re-solving, a margin-only gate and no recheck. Add an out-of-contract C variant for which every plan fails and score the fallback, including any repair deadline it misses.
- **Old-task retention check:** Score the stable and revoked histories through their final lawful paths; check ordinary A, unseen repair and rare C even on the fallback, with missed work in the denominator.

#### 21. Detect incompatible obligations that each have a safe next write alone (P)
- **Mechanism:** Give two queued old jobs separate admissible repair-return-plus-C witnesses, then check whether their witnesses share a legal first return and both deadlines can be met. A union of individually valid continuations is not a simultaneous guarantee.
- **Novelty vs nearest prior art:** Resource-constrained scheduling and ordered conflicts ([PR #301][inward]) already price shared commitments. The candidate obstruction must come from post-return optimizer dynamics even when records, timing and immediate return safety do not conflict.
- **Cheapest first test:** Enumerate two lawful separate repair records and two mandatory C events. Make static scheduling feasible and each job individually pass, but make the two native successor steps incompatible in one legal placement. Compare order-aware exact scheduling with and without slots and with the best control stack; include a pool in which all placements work.
- **Old-task retention check:** Require both distinct unseen repairs to persist after the two C steps, and test ordinary A and rare C after every commit. Choosing one job and reporting only its survival fails.

#### 22. Audit whether these witnesses pay on unfiltered truthful pools (I)
- **Mechanism:** Count immediate-safe crossings, successor-safe crossings, repair-bearing envelopes, and envelopes with successor-safe returns on the same unfiltered streams. Log why each branch fails, including missing records and deadlines, rather than pruning failures before counting.
- **Novelty vs nearest prior art:** This is a stricter audit than #300#22, not an operation: measure where successor dynamics actually remove or recover lawful options relative to the exact causal stack and compact baselines.
- **Cheapest first test:** Propose small exhaustive CPU enumerations over fixed ordinary pools plus engineered positive/negative controls, with held-out splits and varied margins/optimizer slots. If the interaction occurs only in planted cases or matched receding-horizon controls tie, stop at feasibility.
- **Old-task retention check:** Report worst-case and mean old A, independent drifted repair and rare C across all branches, including refusals, and report B retained after every complete trajectory.

## Ranked deeper questions

1. **Can due B buy a repair-bearing return whose first required C write is safe, even when commit-only joint coverage is identical?** Start with 17–18 and 01. Seek a separation at equal current margins, lawful work, and bare *and* commit-only joint return counts. If augmented-state robust predecessor search or the causal #13+#16 stack serves the same branches at the same budgets, retire the primitive claim.
2. **What is the smallest live state summary that predicts successor safety without overstating it?** Use 02–04 and 13. Separate weight and slot explanations with legal paired histories, then test over unseen successor jobs; count false admissions, evidence bytes and foregone work against exact slot-aware previews. A proxy that improves average but breaks a specified old-task floor is not a certificate.
3. **Can a witness stay valid across real observations and deadlines without shrinking the learner into idleness?** Use 10–12, 16 and 20. Compare to causal scenario-tree planning and snapshot-plus-replay with all attempts charged; a late revocation that strands a due job counts against the original admission.
4. **Do lawful opportunities recur often enough to justify certifying them at all?** Use 08, 14 and 22. Ask how often paid-for successor safety changes an on-time A/B/C outcome in unfiltered pools, not how large the effect is conditioned on a handpicked winner. An engineered separation is a falsifier for a simplified control, not evidence of prevalence.

[parent]: https://github.com/manojbajaj95/cl/pull/300
[review-pr]: https://github.com/manojbajaj95/cl/pull/6
[ledger]: https://github.com/manojbajaj95/cl/blob/6fcc8307eb423657bdaa7251ff906e2fedfbac75/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/6fcc8307eb423657bdaa7251ff906e2fedfbac75/reviews/flood-triage.md#L418-L421
[corridors]: https://github.com/manojbajaj95/cl/blob/devin/1795562037-return-corridors/tree/return-corridors.md
[inward]: https://github.com/manojbajaj95/cl/pull/301
[gem]: https://arxiv.org/abs/1706.08840
[agem]: https://arxiv.org/abs/1812.00420
[viability]: https://doi.org/10.1007/978-3-642-16684-6
[tube]: https://doi.org/10.1016/j.automatica.2004.08.019
[bisim]: https://doi.org/10.1016/S0004-3702(02)00376-4
