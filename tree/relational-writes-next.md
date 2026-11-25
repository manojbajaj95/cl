# Narrowing writes and clean receivers

**Status:** Ideas only; no implementation, training, or GPU work. **Parent:** [Relational provisional writes](relational-writes.md) ([PR #279](https://github.com/manojbajaj95/cl/pull/279)). **Review seeds:** [Flood triage, row 397](https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/flood-triage.md#L397), cards 14 and 20 (score 3). **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/idea-ledger.md).

The parent stores an oriented relation over possible new-task (B) effects, not a served B effect. Its W13 example ties an equal-byte buffer. This node asks what happens when **a partial view can rewrite what the actuator is capable of**, not just veto an offer, and when **the surviving relation gives a finite receiver motion that preserves all measured old reads jointly**, not just their average or first derivative. The old tasks are A (including due service A₁ and untouched A₂) and previously committed C. Neither idea earns a novelty claim merely by working in a constructed example.

- **Narrow without commit (#279/14).** A fresh, independently grounded partial view intersects the authorized effect set. It can rule effects out but cannot authorize amplitude, serve B, or expand another right. Rewrite the live carrier of the intersection, then retire the view payload; a fresh, independently sufficient full view must still nominate the nonzero effect. An empty *useful nonzero* set means refusal, even if the homogeneous intersection still contains zero.
- **Spend inside a finite interference null (#279/20).** Given the exact due old stream (same records, timing and optimizer rule), find a legal receiver motion that achieves the full independently supported effect and leaves each measured old interference residual zero, within a prespecified tolerance. The read is a vector, not a sum. Check finite writes from the post-due state; do not project the B offer into the null and call that new target confirmed. A valid relation with no useful safe motion must abstain.

[Recursive set-membership identification][smid] and incremental QR already maintain intersections. [Orthogonal Gradient Descent][ogd], exact constrained fitting, and continuation already seek safe directions or paths. [Effect commits #252][effect] already check joint agreement at commit; [Joint effect agreement #265][joint] also makes due old work close a nuisance ReLU while opening a receiver; [Relation parks #255][parks] preserve an existing relation through old work; [Park crossings #282][crossings] use a batch to reach a different old-safe component. The proposed distinction is a restriction that changes executable capacity *before* B is served, or a finite cancellation whose receiver motion is constrained by that same carried authorization. These are nearest comparisons, not a systematic literature search.

### Shared first-test contract

- Freeze the joint B effect chart, support and provenance rules, nonzero utility floor, legal update menu, expiry, and old-task deadlines before blind offers. Match valid and filler/shared-prior views on visible statistics where possible. Report indistinguishable twins as non-identifiable. No use of retired views after narrowing, no free task labels or oracle readouts, and no changes to due old records. Treat absence of B service before independent full confirmation as an assertion, not a training objective.
- Match peak bytes (weights, optimizer slots, decoder, metadata, buffers), permitted observations, legal actuator, due work, forward/backward work, path checks and end-to-end deadlines. Compare the parent's single-relation write, equal-byte external set-membership plus incremental QR or exact clipping as appropriate, #252 joint check at commit, #265 card 18, OGD at matched B progress, an equally budgeted separate receiver, a fixed-activation version, and no B write with the same old work. The strongest combined arm is **external intersection + the same exact finite receiver solver**, free to write the same carrier at the same cost if the budget allows. Match acceptance errors and report unused compute or memory; an oracle is a ceiling, not the baseline.
- Measure held-out, starting-margin-matched A₁/A₂/C individually at initialization, every externally visible provisional or due step, commit/refusal/expiry, and old returns 1, 8 and 64. Require fixed old loss/decision floors and A₁ parity with paired no-B-write due service; check near-boundary items and both signs of each residual. Count actually served new B gains, false confirmation and latency. If an atomic write is the only thing making a path safe, charge for it and test an interruptible variant.

### Paper fixtures: feasibility and refusal, not an advantage

**N — narrow a plane without choosing scale.** Let a closed B gate hide columns `u=(1,2,0)` and `v=(0,0,1)`. Authorized effects are `au+bv` for `a>0`, `b≥0`, `a+b≤1`. Each column entry is a weight difference `p−q`, with `p+q=1` initially. Old reads include the first pair's sum A₁, every other pair's sum A₂ (a vector), and C=3. An ordinary A₁ step adds 1/2 to both members of that pair, as in W13: A₁ goes 1→2 without changing a column entry. A fresh partial view supports `d₃=d₁/2`, not a scale. Replace the columns by `u+v/2=(1,2,1/2)` and a zero column, keeping every pair sum and the B gate unchanged. Carry `0<a≤2/3`, not `a≤1`. A full independent offer `(1/2,1,1/4)` spends at `a=1/2`; `(1/2,1,0)` is no longer authorized, and `(3/4,3/2,3/8)` violates the inherited budget despite being on-ray. A contradictory fresh partial `d₃=−d₁/2` leaves no authorized nonzero effect. An external buffer with the same restriction and scale bound can tie by making the same lawful pair edits, without retired records.

**R — an exact null that the tangent misses.** Start with receiver coordinates `x=y=z=0`; old reads are `A₂=1+x−y` and `C=3+(x+y)²−4z`. A₁ is a separate due coordinate that goes 1→2 in all arms. The B effect is `(x,2y)`; the carried positive ratio is 1:2. On the menu `0≤x,y≤1`, `0≤z≤1/16`, exact cancellation requires `x=y=t`, `z=t²`. The independently supported offer `(1/4,1/2)` can be served at `(1/4,1/4,1/16)`. Moving on the initial tangent `(t,t,0)` instead gives C residual +1/4 at that scale; a diagonal move to `t=1/2` needs an illegal `z=1/4`. Same-sign wrong ratios fail the A₂ equality; single-path prefixes exposing `x≠y` fail even if a later endpoint repairs them. The nonlinear C read does not need any activation change. Exact external fitting can select the same motion.

**N×R — agreement does not mean a continuum of safe scales.** In a separate variant, B also reads `z`, and the cap on `z` is fixed in advance at 1/4. Use N's narrowed ray and R's old reads. The effect must satisfy both `z=x/2` and `z=x²`, so the only useful joint point is `x=y=1/2, z=1/4`. The on-ray half-scale offer `(1/4,1/2,1/8)` would give C residual −1/4. A compact buffer + exact null solver also finds the isolated point. The open question is whether real legal batches can reach such a jointly useful point at lower cost when the carrier has already been narrowed in place.

## Idea cards

### Before a full view: make restrictions executable

#### 01. Rewrite the executable cone before a spend — seed / primitive candidate
**Mechanism.** Push each partial view into the actuator basis and coefficient bounds, so retired directions physically cannot fire even if a later full view proposes them. Hold the B gate closed throughout.
**Novelty / control.** This is executable restriction, not a new intersection algorithm. Compare the parent static live basis plus incremental QR and an exact buffered constraint with the same actuator.
**Cheapest first test.** Extend N with two independent partials and a one-write budget at the full view. Alternate true, retired-direction, over-budget and provenance-matched junk offers; let the buffered arm schedule the same early writes if it can.
**Old-task retention.** Inspect every paired A₂ sum and due A₁ after each rank drop, including after a contradictory no-spend partial; check C after reuse.

#### 02. Split a coupled slot, pay one half back to old work — primitive candidate
**Mechanism.** A partial view removes one coupling degree of freedom; immediately reassign the eliminated weight *and* optimizer slot to a due C correction rather than merely reporting a lower logical rank.
**Novelty / control.** Rank compression and slot recycling are known; the operation converts unspent authorization into already useful ordinary learning capacity. Compare incremental QR plus earliest legal slot repacking, including the same optimizer migration rule.
**Cheapest first test.** A rank-two B block shares two trainable slots with a colliding C stream. Present a rank-dropping or rank-preserving partial just before C's only correction opportunity. The off slot must stay unusable for B after C updates it.
**Old-task retention.** Require on-time C recovery and intact A₁/A₂; after B spends, return C to verify that the reclaimed slot was not borrowed back.

#### 03. Require provenance quorum for a rank drop — primitive candidate
**Mechanism.** Represent each deletion as an operation that can fire only on independently sourced partial support. Correlated duplicate views can shrink uncertainty for the same source but cannot erase a dimension by appearing to be independent.
**Novelty / control.** Provenance journals and robust consensus are known. The candidate is attaching provenance to *destructive executable restrictions*, not simply counting votes at final commit. Compare provenance-aware clipping plus the same destructive update.
**Cheapest first test.** Use worlds with matching measured rows: independent sensors legitimately restrict rank, while a relabeled copy carries the same hidden bias. Give a lawful provenance cue in one pair and remove it in an impossible twin.
**Old-task retention.** A rejected duplicate must not erase a slot serving A₂ or defer C while the quorum waits.

#### 04. Intersect before a lossy old update forgets the distinction — primitive candidate
**Mechanism.** Push an intersection into the carrier before a compulsory many-to-one chart map, then transport only that intersection. If one restriction arrives too late to be lifted unambiguously, refuse instead of intersecting two lossy shadows.
**Novelty / control.** Image and intersection are known not to commute. Candidate: a live operation that preserves the only executable joint witness across such a map. Compare exact buffered preimage intersection and old-state version tags at equal cost.
**Cheapest first test.** Project `(x,y)→(x,0)`. The positive-x slices of `x=y` and `y=0` each project to the same ray but have no joint positive point. Compare before-map narrowing against stale late evidence.
**Old-task retention.** Execute the lossy A₁ update in all arms and check that preserving the restriction neither pins obsolete old weights nor changes any held-out C return.

#### 05. Make an empty relation absorbing until a fresh first view — primitive candidate
**Mechanism.** Route contradictions to a canonical disconnected actuator state. Old updates and stale full views cannot revive it; only a fresh first view can arm a new relation.
**Novelty / control.** A generation-tagged tombstone is standard; the claim is that an absorbing live state can share reset and actuation machinery without weakening stale-offer rejection. Compare explicit tombstones with generation counters and the same reset.
**Cheapest first test.** Alternate contradictory partials, due cold-start/shared-momentum writes, and stale full offers, then provide a legitimate fresh view for the same address. Include a tiny surviving cone to distinguish empty from merely small.
**Old-task retention.** Check A₂/C throughout the disconnected period and when the fresh relation reuses the weights; neither transition can issue a global reset.

#### 06. Preserve a narrow component without keeping the whole basis — primitive candidate
**Mechanism.** Encode two disconnected feasible pieces behind one closed gate using an executable branch on a lawful receiver read. A partial view retires a piece and frees its branch only if the read still distinguishes the surviving piece after due work.
**Novelty / control.** Piecewise set-membership and [Park crossings #282][crossings] handle disconnected sets. Here corroboration deletes a possible **B effect** region before commit, rather than choosing a path between old-safe components. Compare a two-piece external menu with exact clipping and a paid branch bit.
**Cheapest first test.** Two positive scale intervals on the same ray with a forbidden gap; retire one interval, cycle the selector through due SGD, and blind-test its ends, the gap and the surviving interval.
**Old-task retention.** Include held-out old inputs straddling the branch threshold; selector obsolescence must not change their behavior or let a refusal spill over to C.

#### 07. Narrow the next-update response, not just the immediate effect — primitive candidate
**Mechanism.** Keep authorization over pairs of immediate B effects and their one-step response to a fixed lawful old-update menu. A partial view can delete a future-response mode while leaving present B effects exactly unchanged.
**Novelty / control.** Behavioral equivalence and lifting to future outputs are known. The proposed edit deletes an executable future response rather than predicts it; compare a buffered two-time relation plus exact post-due fitting.
**Cheapest first test.** Two carriers with identical immediate B proposals and old outputs but opposite signed responses to one ordinary A₁ step. Use an independently sourced partial to rule one out before the step; include a twin where the lawful menu cannot tell them apart.
**Old-task retention.** Check the next-update responses of held-out A₂/C too, so narrowing B cannot silently store debt in shared optimizer state.

#### 08. Restrict two addresses with one genuinely shared observation — primitive candidate
**Mechanism.** Give two pending B jobs a common physical degree of freedom and require separately valid support for the declared tying relation. Restrict the shared carrier once; each address nevertheless needs its own sufficient full view.
**Novelty / control.** Factor-graph sharing already amortizes elimination. Candidate: an atomic two-address restriction changes both executable sets without transferring final authorization. Compare one shared external factor plus exact per-address actuator masking.
**Cheapest first test.** Two B jobs share a slope and differ in orientation or scale caps. Interleave a valid shared restriction, a one-address-only restriction, and crossed full views. The one-address case must leave the other address intact.
**Old-task retention.** Spend the first B and treat it as old when the second B changes; check it and A₂/C as separate floors.

#### 09. Use the rejected direction as a control inside the same learner — primitive candidate
**Mechanism.** Prepare a short-lived read-only shadow of a deleted direction using the same old-facing weights but a gate that cannot serve B. At no point can the shadow restore authority; retire it after a prespecified diagnostic read.
**Novelty / control.** Erasure ablations and matched twins are known. The candidate operation is a lawful negative-control read that shares the actual due trajectory, rather than requiring a second trained copy. Compare an equally budgeted shadow simulator or buffer and a sham gate.
**Cheapest first test.** In N, a common prior proposes an effect correlated with both surviving and deleted directions. Compare viable and shadow reads under support substitution; include a case where neither discriminates and both systems must abstain.
**Old-task retention.** Charge the shadow against real A₁ deadlines and check A₂/C before disposal; any served B effect from the shadow is a failure.

### At a full view: receive without old interference

#### 10. Spend through a finite joint null at the original offer — seed / primitive candidate
**Mechanism.** Execute a supported offer through complementary receiver paths and a bounded correction coordinate. Accept only exact or prespecified-tolerance old residuals on the full joint vector after the finite write.
**Novelty / control.** OGD and constrained fitting are known, as is the #265 nuisance-unit close. Candidate: the actual consented joint B direction picks a finite old-safe motion without changing the due batch or requiring a ReLU event. Compare exact buffered post-due fitting, fixed-mask and isolated-unit arms.
**Cheapest first test.** Vary R's curvature sign and correction cap with blind same-sign offers. Include a valid relation with no useful null and a matched tangent that fails after a finite step.
**Old-task retention.** Check signed per-item A₂ and C deviations and A₁ parity; opposite old errors are not cancellation.

#### 11. Make every visible prefix clean, not just the endpoint — primitive candidate
**Mechanism.** Give the receiver a path of subwrites on the finite null with a closed B latch until the whole offer is realized. If any prefix crosses a joint old floor, the protocol refuses rather than borrowing transient old safety.
**Novelty / control.** Constrained continuation and atomic commits exist. Candidate: a resumable B write that can expose old reads at every interruption without exposing any partial B. Compare batched atomic writes with actual atomicity cost and exact null-space continuation.
**Cheapest first test.** In R, compare discrete legal approximations to `(t,t,t²)` with coordinatewise writes and a menu that permits only the unsafe prefixes. Interrupt after each microstep.
**Old-task retention.** Serve old queries at each interruption, including the least protected item in each old task. A safe endpoint does not erase a prefix violation.

#### 12. Reject a null that survives output checks but fails the next optimizer step — primitive candidate
**Mechanism.** Require a finite commit to null both immediate old interference and the first mandatory old response, through joint control of lawful receiver and optimizer-state motion.
**Novelty / control.** Extended-state constrained control already checks dynamics. Candidate: one receiver cancellation also neutralizes optimizer carry while realizing the exact authorized B effect. Compare buffered extended-state fitting and a paid optimizer reset, without free resets of old work.
**Cheapest first test.** Give two receiver realizations the same output-null endpoint but opposite momenta. Force the same next A₁/C batch; only one endpoint and momentum pair survives both checks.
**Old-task retention.** Measure A₂/C before and after the forced batch and again after momentum decay; output equality at the commit is insufficient.

#### 13. Keep the old anchor through a receiver relay — primitive candidate
**Mechanism.** On a predeclared due tick, pass an unfinished B receiver motion between two live charts while keeping residuals measured against the same paired old-service anchor. Realize the remaining portion of the already confirmed offer without exposing partial B or soliciting new consent.
**Novelty / control.** Switched constrained control and standby handovers already transfer work. Here a verified finite null is relayed while B remains unserved and the old reference cannot be reset. Compare a separately reserved receiver and exact buffered handoff with full checkpoint cost.
**Cheapest first test.** Two charts have complementary write menus and one common, old-clean handoff state. Test loss of that state, a stale handoff anchor, and a purported relay that would require restarting beyond the B deadline.
**Old-task retention.** Inspect old reads on both charts at the handoff; make the due C batch happen halfway through rather than pausing service.

#### 14. Certify a null against several plausible old responses — primitive candidate
**Mechanism.** Before spending, require the same actuator motion to preserve old floors under every response map left indistinguishable by the lawful old probes, not just under the best-fitting old gradient.
**Novelty / control.** Robust constrained optimization already uses worst-case sets. Candidate: keep the common null as a spendable receiver object whose condition tightens when a partial B view restricts the available effect set. Compare exact buffered robust fitting plus the same old-response uncertainty estimator.
**Cheapest first test.** Two post-due worlds agree on expressed old outputs but give opposite cross-curvature. Compare a shared safe correction, alias-specific corrections that do not transfer, and a case where the common null is trivial.
**Old-task retention.** Evaluate held-out old trajectories from both hidden worlds, not the average response or only the world the planner guessed.

#### 15. Carry a second old skill through a newly clean write — primitive candidate
**Mechanism.** After one B commit becomes old, add its finite interference read to A₂/C through its existing receiver paths. The next B job must find a motion jointly null for the expanded old vector.
**Novelty / control.** Sequential constraint accumulation is known; proposed reuse of a committed receiver as the next write's old-task constraint is stronger than freezing it or checking a snapshot. Compare stacked buffered constraints plus exact projection/fitting and a fixed dedicated receiver.
**Cheapest first test.** Create three legal motions: one preserves A₂/C only, one preserves the earlier B only, one preserves all while achieving a fresh offer. Remove the third in a matched impossibility world.
**Old-task retention.** Verify the first B on its regular held-out workload under A₁/C service, not merely the coordinates it exposed as constraints.

#### 16. Give a null witness an expiry tied to actual old work — primitive candidate
**Mechanism.** Allow an old-null receiver certificate to expire on a change in the legal due-update history, even if clock time and the B ray are unchanged. Renew only by a fresh finite check at the same old anchor.
**Novelty / control.** Leases and invariant-set recertification are known. The candidate is a receiver contract revoked by consumed old dynamics, independently of whether B corroboration remains fresh. Compare a buffered post-due exact solver and a wall-clock lease at equal checks.
**Cheapest first test.** Matched elapsed times and identical B proposals; one A₁ sequence preserves the correction coordinate's boundary and another moves it just beyond legality. Add an idle-only control.
**Old-task retention.** Check due old work with and without expiry; refusing stale authority cannot excuse lost C service or require undoing a completed A₁ step.

#### 17. Use an ordinary C correction to do the receiver's cancellation work — primitive candidate
**Mechanism.** Keep due C records fixed; let their realized lawful update supply one component of the receiver cancellation, if the pre-existing receiver state couples that update to the required signed motion. The B write must preserve C's *new* post-due improvement.
**Novelty / control.** #265 already opens a receiver using old work. The new claim is using that ordinary old step to set the finite cancellation coefficient, beating a matched separate opener plus compensator, not just switching a unit on.
**Cheapest first test.** In a two-route receiver, one natural C record gives the missing signed coefficient, an equally improving C record lands with the wrong coefficient, and a fixed-mask arm removes any opening effect. Match old schedule within each world.
**Old-task retention.** Require C's due gain at its deadline and after the B write; returning C to its pre-due value is a failure even if A₂ is unchanged.

### Compose the two primitives, or expose the tie

#### 18. Find an isolated positive scale at the joint intersection — primitive candidate (merge)
**Mechanism.** Compile a partial view into the live carrier, but let the curved receiver null eliminate all but a discrete set of permitted amplitudes. Require a fresh full offer at an actually permitted amplitude, never substitute the nearest one.
**Novelty / control.** A constrained polynomial solve can find isolated points. The candidate is an executable interaction, not the intersection itself: a prior restriction does useful actuator work and reduces the later finite realization cost. The strongest arm is compact buffered intersection plus the identical exact null solver.
**Cheapest first test.** Start from N×R; vary hidden curvature and the cap, and include a same-ray wrong-scale offer and a twin with no positive intersection. Then put both arms under the same commit deadline and let both prepare legally.
**Old-task retention.** Check C on both sides of the permitted scale and A₂ at the matched endpoint; neither over- nor under-compensation may count as success.

#### 19. Eliminate a receiver path when a partial makes it unspendable — primitive candidate (merge)
**Mechanism.** Link authorization and receiver paths so shrinking the former retires a genuinely unreachable path. Park that path's trainable slot for C before the full view without losing any still-legal old-clean spend.
**Novelty / control.** Constraint pruning and slot allocation are known. The bet is a structural identity between a deleted direction and an otherwise expensive cancellation path, not general rank reduction. Compare buffered reachability, earliest legal slot reuse, and an exact finite solver together.
**Cheapest first test.** Two receiver routes originally cover the accepted effect set. A partial makes one unreachable in one world and leaves it indispensable in another with the same local rank drop; include a valid full offer in each world.
**Old-task retention.** Check that the parked route handles its C workload and does not need to be reclaimed to avoid A₂/C interference on the surviving route.

#### 20. Disarm when valid narrowing removes the last safe realization — primitive candidate (merge)
**Mechanism.** Track geometric authorization and safe realizability separately. If corroboration selects only an old-unsafe piece, erase pending permission and refuse; do not keep the discarded safe piece alive in the name of retention.
**Novelty / control.** Feasibility guards are standard. Candidate: a destructive two-layer restriction leaves no executable route to the previously safe but now unsupported effect. Compare exact buffered effect and receiver sets, a disarmed live gate, and the same empty-state protocol.
**Cheapest first test.** Give two possible B rays: one has a finite null, the other has a valid new corroboration but only unsafe motions. Offer both after narrowing, plus an indistinguishable old-read twin that needs conservative refusal.
**Old-task retention.** Refusal must preserve due A₁ and C service and leave A₂ unchanged across cleanup. Recheck all three after a stale offer tries to spend the discarded ray.

#### 21. Compile a shared cancellation coordinate for several pending relations — primitive candidate (merge)
**Mechanism.** Let independent pending jobs share one finite correction coordinate only when their live restrictions agree on its *remaining* capacity. Charge any consumption on spend before another job can claim it.
**Novelty / control.** Resource reservations and joint constraints already prevent double spending. This proposes a receiver state where the narrowing rewrites are also its capacity partition. Compare a compact ledger of reservations plus exact finite fitting and two isolated receivers.
**Cheapest first test.** Two jobs each alone fit under a bound on a shared z correction. After the first spend, the second has one legal smaller offer and one independently supported but over-cap offer. Swap the order and interleave due work.
**Old-task retention.** Treat the first B as old, and check per-item A₂/C during the reservation update and after either second-job outcome.

#### 22. Make one naturally available restriction do two jobs — primitive candidate (merge)
**Mechanism.** Use a truthful partial view to remove an effect direction and simultaneously pre-position the complementary receiver path through the same carrier write. The partial supplies no information about the final scale; the later full view sets it.
**Novelty / control.** Precomputation and warm starts are standard. The candidate win is one *necessary physical write* replacing both a restriction update and receiver preparation. Compare buffered clipping plus cost-optimal independent preparation and exact null fitting, including a buffered arm allowed the same shared write.
**Cheapest first test.** On a small blind CPU stream with overlapping old features, cross informative/non-informative partials with receiver-aligned/receiver-misaligned actuation, matched on final set size. Demand a positive interaction in timely supported spends at matched retention and errors; no win if the strongest stack attains it.
**Old-task retention.** Check preparation itself on ordinary A₂/C, and compare final old floors and due A₁ parity even when B never receives a corroborating full view.

## Ranked deeper questions

1. **Can one necessary carrier rewrite both narrow authority and prepare a finite null more cheaply than the best stack?** Start with cards 18 and 22. Cross genuine restriction with receiver alignment; hold final set size, true-offer frequency and independently supported B amplitudes fixed across alignment arms. Compare timely useful spends at fixed peak bytes, old floors, false confirmations and compute. N×R proves feasibility only. Drop the compound novelty claim if the equally informed buffer can copy the operation at equal cost.
2. **When can a live restriction permanently retire old evidence and actual capacity without reviving either?** Start with cards 02, 04 and 07. Cross rank drop with a lossy due map and a live optimizer tail. Quantify bytes physically reclaimed and reuse for ordinary C progress, while demanding correct late refusal, zero pending B service and the same old schedule. If preimage tracking or exact repacking ties, keep the capacity result as ordinary constraint maintenance.
3. **When does a finite old null survive the first real old return?** Start with cards 10–12 and 17. Separate tangent, clean endpoint, pathwise clean and extended-state clean arms; vary curvature, the first old record and its update order. Require supported B progress with no hidden debt, against exact buffered fitting, a fixed activation pattern and an equal-budget clean unit. A safe but useless null is refusal, not a positive result.
4. **When can indistinguishable histories force a learner to abstain even though a useful joint point exists?** Use cards 03, 08 and 14. Construct one pair of worlds that shares all legal probes until the deadline but differs in independent B support, and another that differs only in which receiver motion is old-safe. An oracle ceiling separates missing information from insufficient actuator capacity; an advantage that disappears once both arms get the same lawful observation is not a new primitive.

[smid]: https://doi.org/10.1016/0005-1098(91)90094-I
[ogd]: https://arxiv.org/abs/1910.07104
[effect]: https://github.com/manojbajaj95/cl/pull/252
[parks]: https://github.com/manojbajaj95/cl/pull/255
[joint]: https://github.com/manojbajaj95/cl/pull/265
[crossings]: https://github.com/manojbajaj95/cl/pull/282
