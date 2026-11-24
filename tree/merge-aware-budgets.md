# Merge-aware budgets: reserve for the learners you will actually merge with

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Leakage leases](leakage-leases.md) ([PR #176](https://github.com/manojbajaj95/cl/pull/176)), cards 9 and 15. **Review seed:** [Flood triage row 280](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/flood-triage.md#L280), the two score-3 directions: reserve a certified interaction allowance only for learners whose updates will merge; earn back headroom only after proved repair. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/idea-ledger.md). Its coded merge-interference kill rules out selling a fitted pairwise surrogate as the primitive; its forecast-weighted write selection result calls for a same-information control, not a weaker blind baseline.

## Is a learner's future merge partner a new budgeted object for continual learning?

**Not as a compatibility score, a planned merge, or a shared quota.** [CoFiMA](https://arxiv.org/abs/2312.08977) already uses old-task Fisher information for sequential merging. [Proximity-regularized merging](https://arxiv.org/abs/2609.32332) shapes a task vector before insertion to control old-task curvature and merge-coefficient sensitivity. [FedSEAM](https://arxiv.org/abs/2610.33496) already compares client subspaces, selectively merges, and preserves components in a selected prior-overlap subspace. [Holistic continual model merging](https://arxiv.org/abs/2509.23592) intervenes before, during and after the merge. [Task arithmetic](https://arxiv.org/abs/2212.04089) and [TIES](https://arxiv.org/abs/2306.01708) supply useful merge operators, not intertemporal proof rights. [Privacy filters](https://arxiv.org/abs/1605.08294) and [budget scheduling](https://www.usenix.org/conference/osdi21/presentation/luo) already meter and allocate resources; their guarantees are not retention theorems. [Pacti](https://arxiv.org/abs/2303.17751) can express partner-specific contracts, and [Certified CL](https://arxiv.org/abs/2407.06697) already protects established properties during retraining.

**Conditional yes, not a priority claim.** The object worth testing is a *certified right to keep training while preserving a specified future merge*: each independent learner can check whether its own next update still fits a jointly scoped interaction allowance, without seeing the other learner's update trace or reopening the retired-source proof. The same update may be legal with one partner envelope and illegal with another. A proved repair can change that answer without erasing what either learner learned. The quick scan did not find this full operation in CL; generic contracts could implement it. If certified merging plus adaptive contracts and proved repair gets the same useful admission at the same evidence cost, count this as an application, not a new primitive.

### What a reservation actually promises

- **Local until there is a joint obligation.** A local lease from the parent covers only its branch. Declare an intended deployment merge, its contributing branches (or certified partner classes), state/base and witness versions, exact operator and allowed coefficients, protected outputs, and merge window/suffix. Only those branches reserve joint allowance. Multiple independent alternatives do not debit a global balance. If a new merge is requested later, prove entry against the actual states and a joint envelope first; a local receipt confers no retroactive merge right. Cancellation removes the obligation, not any already incurred local error. A refused declared merge is a failure to deliver, not a successful local outcome.
- **Bind the joint bound to a reference.** Use the same pre-fork retention reference and the parent's frozen substitution package with scope checks. For a two-branch sum and a scalar old-task readout, a schematic sufficient bound is `d_merge ≤ b₀ + qᵢ + qⱼ + Jᵢⱼ`: baseline error `b₀`, bounds on the solo readout changes `q`, and a uniform bound on the mixed residual `J`. This follows by adding and subtracting the two solo readout changes; it does not hold for an arbitrary merge rule without an operator-specific argument. If the rule includes rescaling, routing, state alignment or inherited optimizer slots, price these in its bound. Keep branch-local errors and joint reservations distinct even when derived from the same evidence. Check closure, old-task output floors and any allowed suffix amplification at every visible prefix; summed instantaneous charges are not a general proof. Exact counterfactual traces may serve as blinded test oracles, not as inputs to a purported source-free verifier.
- **Earn, don't refill.** Reissue only after a realized repair with a checked transition establishing a smaller liability bound under the same reference, scope and horizon, while preserving required B behavior. For current bound `U` and cap `ε`, replacing `U` with certified `U' < U` buys at most `U − U'` of headroom in that bound. The new envelope must cover the remaining authorized paths. Lower local error does not by itself lower a joint interaction bound; recheck affected reservations before spending jointly. Do not restore checkpoints, erase B, advance the clock, reset an accountant, or relabel the reference to manufacture credit. A monotone lease or cumulative property is not refunded; a future reissue cannot undo a violated prefix.

### Two paper witnesses and a repair falsifier

1. **Zero interaction in prediction space, nonzero in loss space.** Add two rank-one matrix edits to one linear learner. On one old example normalize each edit's signed output change to `+0.2`, with zero base residual. Squared errors are `0.04` solo and `0.16` together; the mixed term is `0.08`, so a loss cap of `0.12` accepts each local job but refuses the sum. Flipping one edit's sign leaves the solo charges equal and makes the joint loss zero. Start with exact enumeration and a sound bilinear cross-term bound; an improvement over blindly summing solo charges is only a sanity check.
2. **Zero first-order interaction estimate, live gate at merge.** Freeze one targeted old example's preactivation at `−0.8`. Each branch adds `0.6`; each local ReLU output is still zero, but the sum of the *deltas* gives output `0.4` and fails a cap of `0.25`. Give one branch a lower-coupling legal alternative of `0.4` that preserves its own useful B behavior; it fits with either `0.6` partner even though two `0.6` edits do not. Include genuinely separate, undeclared alternatives that may both spend locally, and old examples on both sides of the gate. Use dedicated B readouts and at least one later B update requiring shared state so a permanently disjoint model is not the only safe solution. A finite envelope covering the gate must compete with a stronger contract using the same information, not just a Taylor estimate.
3. **Repair that moves a proof-relevant error, not the reference.** In a quantized toy whose B output depends on `s`, compare two legal state transitions `(s,e) → (s,e/2)` and `(s,e) → (s,g(z)e)` for paired discrepancy `e`. Let `g=1/2` on the publisher's samples and `g=2` on another reachable state `z`. The first can shrink a checked bound on `e`; the second must not earn credit from the sample alone. Add a jointly activated gate unaffected by `e` so a true local repair can still fail to free joint credit. Tests should also challenge B retention on held-out states where `s` alone may not be sufficient.

### Common first-test rules

Freeze the partner schedule, operator, holdouts, reference, margins and tolerance before each comparison; use the same legal updates, task exposure, information, compute and proof-byte budget. Compare independent local jobs, static caps, adaptive linear accounting **with a certified cross-term bound**, privacy-style scheduling with the same retention evidence, full merged certification and exact bounded reachability. The strongest conventional stack gets partner-scoped Pacti contracts, phase-aware [IBP](https://arxiv.org/abs/1810.12715) or exact envelopes, the same adaptive allocation and repair checker, and merge-aware shaping/merge selection where the specification permits it. Include a two-by-two ablation (partner awareness on/off × proved reissue on/off), no-refill, speculative refill, [#170 renewal](https://github.com/manojbajaj95/cl/pull/170), freeze/[GPM](https://arxiv.org/abs/2103.09762), and save/restore or erasure as diagnostic controls. Do not count refusing everything, retaining hidden copies, dropping partners, narrowing the grammar, or deferring the same learning as wins.

Report unsafe admissions, missed safe admissions, useful B progress and both B skills after merge, against exact ground truth when possible. Count publication, negotiation, evidence, verification, reissue, peak copies and fallback costs even for failed jobs. Check ordinary old A/C tasks on separate held-out examples at local prefixes, before/during/after visible repair, immediately at merge and after one or more legal suffix updates; include worst slices and compare at matched starting margins. Do not equate a discrepancy certificate with a task accuracy result. The ideas below propose CPU-sized or paper tests only. **P** = candidate primitive, conditional on beating the stacked control; **I** = improvement or audit.

## Idea cards

### Decide who needs a joint allowance

#### 1. Spend locally; reserve only for the committed merge (P)
- **Mechanism:** Give the same two branches independent local leases in the no-merge arm and a shared interaction reserve only in the declared merge arm. Both continue to check their own local scope.
- **Novelty vs nearest prior art:** Privacy scheduling allocates a global cap among consumers; the candidate is a transferable proof of future coexistence that only exists for a specified joint learner.
- **Cheapest first test:** Exhaust the linear rank-one and shared-ReLU witnesses under independent, global, partner-scoped and exact merged designs. Compare safe admissions at equal B utility.
- **Old-task retention check:** Score A/C on both local streams, at the promised merge and one step later; do not count an undeclared merge as locally certified.

#### 2. Buy a partner class rather than a partner name (P)
- **Mechanism:** Bind the reservation to a verified envelope for one partner slot. A learner unknown at issue time may fill the slot only by checking entry under the same reference, units and merge law.
- **Novelty vs nearest prior art:** Pacti already allows substitutable implementations. The candidate is a proof right for an independently learned update with useful behavior, without reopening the incumbent's history.
- **Cheapest first test:** Publish one envelope for two possible future partners of opposite signs in a two-direction linear model; verify which requires the larger reserve. Try an out-of-envelope third partner and compare exact proofs.
- **Old-task retention check:** Score A/C for both eligible substitutions and after another merged update; require each incoming learner's B skill as well as the incumbent's.

#### 3. Convert a local lease only on late proof of entry (P)
- **Mechanism:** At a genuine late merge declaration, use the live states and still-valid parent receipts to prove compatible entry. If no local-evidence proof fits, defer or refuse the merge, never inherit entitlement from two local balances.
- **Novelty vs nearest prior art:** Post-hoc TIES and exact merged verification already combine finished models. The candidate is reusable evidence that buys a future continuation contract, not only an endpoint check.
- **Cheapest first test:** Reveal a chosen partner after two blind updates. Match local histories across a linear good case and a hidden gate collision; compare full recertification and modular proofs with the same state access.
- **Old-task retention check:** Score old tasks up to declaration, on both accepted and refused paths, and after one admitted joint suffix; a failed merge stays in the delivery denominator.

#### 4. Reserve for actual combinations, not every pair in a directory (I)
- **Mechanism:** Record which cohorts will contribute to a common deployment and which are mutually exclusive alternatives. Prove each promised cohort without adding liability across impossible combinations.
- **Novelty vs nearest prior art:** Conflict-aware scheduling and disjunctive contracts already encode alternatives. This improves reserve allocation, not the underlying proof operation.
- **Cheapest first test:** Compare a three-way choice between merging A's learner with either of two other learners versus a promise to merge all three. Enumerate legal schedules and compare union, pairwise and exact cohort contracts.
- **Old-task retention check:** Measure A/C on each realized cohort, including the feasible worst one, and on the unmerged local branches; use the same old-task set in all worlds.

#### 5. Prove a handoff through a partner's optimizer change (P)
- **Mechanism:** Carry forward a partner slot and its liabilities to a new author only if a conversion proof covers both the successor's entry state and new update law. Matching weights do not make momentum equivalent.
- **Novelty vs nearest prior art:** The parent's serial lease and contract refinement already cover transfer. The proposed extension preserves a second learner's independent option to merge without reopening either proof.
- **Cheapest first test:** Give two successor learners the same weights but different momentum slots; enumerate a two-step continuation and try to reuse the stale receipt.
- **Old-task retention check:** Score ordinary A/C at handoff, on the first momentum-sensitive update, and at the eventual merge and suffix; protect both B behaviors.

### Buy a tight interaction certificate

#### 6. Keep the signed bilinear term rather than buying its worst sign (I)
- **Mechanism:** Use a proved set of possible signed overlaps to bound joint squared loss; take cancellation credit only if *every* authorized pair satisfies the claimed relation.
- **Novelty vs nearest prior art:** Fisher merging and quadratic reachability already reason about curvature. This tightens a merge reserve; an estimated overlap is not a certificate.
- **Cheapest first test:** Use equally costly rank-one edits with aligned, opposed and unconstrained signs. Compare diagonal Fisher, exact bilinear interval, worst absolute overlap and exact enumeration.
- **Old-task retention check:** Score A/C on directions not used to fit the overlap, including a slice where the sign is reversed.

#### 7. Reserve against a gate neither learner opens alone (P)
- **Mechanism:** Certify the joint preactivation range up to merge. Keep the allowance at zero only if the combined reachable edits cannot open the gate or if a separate proof bounds its output effect.
- **Novelty vs nearest prior art:** IBP proves ReLU stability, and TIES handles parameter-space conflict. The candidate is a portable joint gate obligation that two learners can continue observing separately.
- **Cheapest first test:** In the shared-ReLU witness, let optimizer slots move one branch from its low to its high option after commitment. Compare relational gate receipts, phase IBP contracts and exact pair enumeration.
- **Old-task retention check:** Keep near-threshold A/C examples that fail only under the combined gate and examples on otherwise active gates. Check both at merge and on the legal suffix.

#### 8. Detect a coalition invisible to every pair (I)
- **Mechanism:** Issue one explicit higher-order reserve when a downstream switch can see three branches at once; permit pairwise composition only if the interaction truly decomposes.
- **Novelty vs nearest prior art:** Higher-order verification already detects this obstruction; unlike the ledger's killed coded merge interference, it does not infer safety from fitter quality on sampled groups.
- **Cheapest first test:** Put three `0.4` edits behind a gate at preactivation `−0.9`; every pair is inactive, the triple produces `0.3`. Compare pairwise bills, grouped IBP and exact checks across a second, genuinely quadratic model.
- **Old-task retention check:** Score A/C for each solitary, pair and triple deployment plus one triple suffix step; do not drop the triple when reporting success.

#### 9. Issue a safe interval of merge coefficients (P)
- **Mechanism:** Reserve over an admitted coefficient region; allow the merger to select coefficients late using new-task utility, but only within a region certified for old tasks and the suffix.
- **Novelty vs nearest prior art:** Proximity-regularized merging already widens an empirical coefficient plateau. The candidate is a right that survives further local learning and late coefficient choice without reopening proof histories.
- **Cheapest first test:** Compute the exact feasible coefficient intervals of two quantized ReLU branches. Compare fixed weights, the proximity-regularized null, full rechecking and a maintained interval including all boundary cases.
- **Old-task retention check:** Score old tasks at the certified endpoints and at the late-chosen interior point; check that coefficient selection has not effectively erased either B skill.

#### 10. Make a merge order part of what gets reserved (P)
- **Mechanism:** When a nonlinear merge operator is order dependent, reserve for the permitted trees rather than for an unordered set. A new tree needs a bound or a proved same-effect rewrite.
- **Novelty vs nearest prior art:** TIES has merge-time interference handling; compositional contracts already represent ordered operations. The candidate is reusing partial allowances across verified regroupings of still-learning branches.
- **Cheapest first test:** Enumerate two parenthesizations of a three-branch sign-vote-and-average merge, including ties. Compare fixed order, one worst-tree cap and per-tree exact certification.
- **Old-task retention check:** Score A/C on any intermediate model made visible and on both final orders after a suffix; check all promised B components.

#### 11. Prove a dependency cut through the actual merger (I)
- **Mechanism:** Certify zero interaction only if the readout *and* merge operator do not couple the affected coordinates, including normalization, re-alignment and joint clipping.
- **Novelty vs nearest prior art:** FedSEAM already preserves selected components and GPM isolates projected directions. This audits when zero debit is sound, not a new object.
- **Cheapest first test:** Use edits on disjoint coordinates with additive merge, then turn on joint normalization. Compare a support-only proof, full transition slicing and exact enumeration.
- **Old-task retention check:** Use A/C examples sensitive to the norm only after merger and on the next optimizer step; check the uncoupled case is not pointlessly refused.

#### 12. Certify compatibility before the coordinates are aligned (I)
- **Mechanism:** Place the reserve in readout space and require the alignment map to preserve its bounds together with the state used for subsequent training.
- **Novelty vs nearest prior art:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns permuted networks; this is a scope check on reusing a prior reservation after alignment.
- **Cheapest first test:** Swap two hidden ReLU units; compare exact permutation of weights and slots against a weights-only alignment with mismatched slots.
- **Old-task retention check:** Verify ordinary old tasks immediately after alignment/merge and after the slot-sensitive step; do not credit a pure permutation as B progress.

### Earn headroom on evidence of repair

#### 13. Reissue only after uniform contraction (P)
- **Mechanism:** After a real legal repair, check a smaller paired-error envelope over the admitted fiber, with original reference and useful B state intact. Recompute charge against that envelope, not the old spend history.
- **Novelty vs nearest prior art:** Funnel contraction and [#170 renewal](https://github.com/manojbajaj95/cl/pull/170) already permit repaired sets. The candidate is a reissued continuation right in the retired-source setting, with all merge obligations still attached.
- **Cheapest first test:** Use the true and sample-only contraction witnesses; compare no refill, automatic refill, renewal, modular reissue and exact reachability. Deliberately cash speculative credit into a failing next update.
- **Old-task retention check:** Score A/C through repair and the extra admitted update, not just afterward; retain held-out B behavior at equal memory and compute.

#### 14. Repair interaction without repairing either solo score (P)
- **Mechanism:** Have a learner move a representation within a verified task-equivalent region so the reserved mixed term falls even if both solo charges stay fixed. Reissue only after the state change and joint proof.
- **Novelty vs nearest prior art:** Orthogonal training, disentanglement and post-merge correction already reduce interference. The claim is recovery of an existing partner-specific right before merger at unchanged solo retention and B utility.
- **Cheapest first test:** Rotate a fixed-norm edit among two verified equivalent B directions, one aligning with the partner and the other orthogonal. Match against picking that direction up front, projection alone and exact joint recertification.
- **Old-task retention check:** Check A/C during the move, after merge and during a shared B update; hold margins and both B skills fixed.

#### 15. A local repair must not spend a partner's relief twice (I)
- **Mechanism:** Bind any reissued shared allowance to a new joint receipt that supersedes the previous one. A smaller local error never authorizes two independent draws on the same newly proven slack.
- **Novelty vs nearest prior art:** Resource accounting already prevents double spending. This audits paired receipts and distinguishes local credit from joint credit.
- **Cheapest first test:** In the linear witness offer two updates each fitting the same new residual, but whose simultaneous adoption exceeds it. Also plant a locally contractive repair leaving the ReLU interaction unchanged.
- **Old-task retention check:** Score A/C after each legal order and after the attempted double use, including merged deployment; ensure a refused credit causes no visible unsafe transition.

#### 16. Recover one direction but not its amplifying suffix (I)
- **Mechanism:** Reissue each direction only after propagating its repaired envelope through remaining transitions and the merger. A decrease in today's largest error need not improve the worst future prefix.
- **Novelty vs nearest prior art:** Robust reachability and the parent's amplification reserve already require horizon-wide bounds. This applies them to defective repair receipts.
- **Cheapest first test:** Use a two-slot recurrence that shrinks one coordinate but transfers mass to a second that is amplified at merge. Compare current-error reissue, horizon reissue and exact paths.
- **Old-task retention check:** Score old slices sensitive to each slot at the transient peak, after merge and at the endpoint; retain failures that later vanish.

#### 17. Prove the bridge, not just the repaired endpoint (P)
- **Mechanism:** Offer multi-step repairs with a temporary *certified* allowance covering every visible intermediate, then reissue on reaching a smaller envelope with B still intact. No borrowing against an unproved future endpoint.
- **Novelty vs nearest prior art:** Funnel chains already certify transient paths. The candidate operation lets a blind learner repair an inherited partner obligation without reopening the source proof.
- **Cheapest first test:** Enumerate a two-step repair that first increases discrepancy then strictly reduces it. Test two starts with the same endpoint but only one safe bridge, against exact verification and #170 renewal.
- **Old-task retention check:** Score A/C halfway through and after the bridge, at merge and after a suffix; check B after each visible step.

#### 18. Repair tomorrow's partner without penalizing unrelated learners (P)
- **Mechanism:** If one edit participates in two separately certified future deployment plans, permit a repair targeted at one only after checking the unaffected plan's original envelope or updating its proof. Independent local learners owe neither plan a reserve.
- **Novelty vs nearest prior art:** Multi-contract refinement already preserves concurrent interfaces. The proposed primitive is a narrowly scoped restoration of one future CL merge option without universal throttling.
- **Cheapest first test:** Give one branch a repair direction orthogonal to one partner but parallel to the other. Compare per-plan reissue, global minimum headroom and exact verification of both plans.
- **Old-task retention check:** Check old slices protected by each deployment plan and all local branches through repair, then each resulting merged learner after further training.

### Try to make the proposed primitive unnecessary

#### 19. Teach low coupling instead of buying a large allowance (I)
- **Mechanism:** Choose truthful B examples that steer updates away from certified partner-sensitive directions while matching B learning and the local liability.
- **Novelty vs nearest prior art:** Proximity-regularized merging and existing look-ahead selection already shape updates. This is a useful counterfactual to elaborate budgeting, not the new object.
- **Cheapest first test:** Exhaust two-example minibatches in a shared-gate learner; give the same forecasts and candidate examples to orthogonal projection, proximity shaping and the checked reservation arm.
- **Old-task retention check:** Match per-example A/C margins before branch learning; score A/C after merge and after a B task requiring the formerly sensitive direction.

#### 20. Exhibit indistinguishable partners that need different prices (I)
- **Mechanism:** Construct two reachable partner states with the same published receipt but opposite answers to one promised merge. Search for the minimum additional distinction that permits sound admission of the safe one.
- **Novelty vs nearest prior art:** Indistinguishability and partition refinement already give this lower-bound method. It tests whether the purported portable object is just the hidden state in another form.
- **Cheapest first test:** Hide a slot or delayed gate bit that controls a later co-activation while matching solo readouts. Increase hidden-state width and compare receipt size with exact state tracking.
- **Old-task retention check:** Plant an ordinary A/C slice failing only on the unsafe continuation, with matched B progress and solo old-task margin; keep both continuations in scoring.

#### 21. Find when recomputing the joint proof is cheaper (I)
- **Mechanism:** Track total evidence cost as committed partner turnover, overlap and honest repair frequency increase. Treat a full merged proof as a strong competitor, not a failure mode.
- **Novelty vs nearest prior art:** Proof amortization and the parent's break-even audit already price reuse; this locates where prospective retention guarantees add value over exactly checked mergers.
- **Cheapest first test:** Sweep two to four partners, fixed versus changing cohorts, and zero versus two real repairs on a finite grammar. Compare proof bytes and checks at matched admissible continuations.
- **Old-task retention check:** Count cost wins only at fixed A/C floors and B success, including failed merge delivery and rejected repair attempts; plot worst-prefix retention separately.

#### 22. Compile the object away into ordinary contracts (I)
- **Mechanism:** Express local scopes, joint reservations, repair transitions and checks as augmented-state assume–guarantee contracts. Give the conventional stack exactly the same information and right to check or refuse before commit.
- **Novelty vs nearest prior art:** Pacti, certified CL, adaptive accounting and exact/IBP merge verification together are the direct null. A tie falsifies evidence for a new CL primitive.
- **Cheapest first test:** Use a blind split and merger with the linear and ReLU witnesses and planted false repair. Compare the partner-awareness × proved-reissue ablation to the full stack and exact reachability, with matched evidence budgets.
- **Old-task retention check:** Require A/C and useful B at every visible point, including after a different learner spends reissued headroom; show explicitly that save/restore cannot win by losing B.

## Ranked deeper questions

1. **Can two blind continual learners reserve just enough for their promised merge without showing each other their trajectories?** Hold local lease, legal grammar, scope and retention fixed; run the rank-one and ReLU witnesses with partner-specific alternatives and a blind successor (cards 1–3, 5–7, 22). Look for more useful certified continuations or less total evidence than the equally informed contract/merging stack. A win over static caps alone is not enough.
2. **Can a proved repair restore a joint right that neither successful solo retraining nor generic renewal can restore at the same cost?** Cross uniform versus sample-only repair with aligned versus orthogonal partner interactions (cards 13–18). Look for a real partner-awareness × repair interaction; keep the original A/C reference, preserve both B skills, and count all unsafe prefixes even if the endpoint is sound.
3. **What is the smallest partner description that makes commitments composable?** Start with typed signed overlaps, then add cohort gates, merge order and indistinguishable slot states (cards 2, 6–12, 20). Identify the first case where exact certification needs essentially the partner's full state; do not confuse a useful empirical predictor with a sound description.
4. **Where do old-task floors actually constrain learning enough for this machinery to matter?** Compare conventional merge-aware shaping, static reservations, proved reissue and exact recertification as coupling and partner turnover vary (cards 14, 19, 21–22). If the free or frozen/pruned arms achieve the same useful B progress and normal old-task retention, or the conventional stack ties on admission and evidence, retain only the engineering or negative result.
