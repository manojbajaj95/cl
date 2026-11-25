# Menu-preserving replacements and paired residuals

**Status:** Ideas only; exact paper fixtures and proposed CPU checks, no training runs or GPU. **Parent:** [Finish menus](finish-menus.md) ([PR #222][parent]). **Review seeds:** [Flood triage][triage], score 3: parent card 06 allows an ordinary update to invalidate a finish only if the same step preserves coverage and reserves a replacement at the original deadline; card 11 pairs orientations whose leftover momentum cancels on separate A and C readers but adds along a shared B direction. Cards 01 and 09 below restate those obligations as reference designs.

**Ledger read first:** The [idea ledger][ledger] rejects exact save/restore as a primitive, forecast-only write selection that fails retention matching, and structural-rank claims that outrun executed behavior. Every first test checks ordinary old tasks. **P** marks a candidate reusable object or operation, not a priority claim; **I** marks an improvement or audit. A combined card must beat the best stack of its parts at equal budget, not merely beat either part alone.

## Two invariants, one live history

- **Replace an executable promise, not a menu entry.** After branch 1 publishes a real zero-B-gain move, fix the admitted B demands, observations and absolute deadline D. An ordinary update can publish only at a boundary where the update, post-update menu and executable reservations all take effect together. Readers and arrivals must see the old committed bundle or the new one, never a gap; charge any staging and boundary latency. Every admitted observation must have one causal policy that works for all hidden states and allowed interleavings consistent with it. The policy covers no-shows or out-of-domain inputs via an already backed safe exit if those can occur. Check execution, validation, authority and actual time remaining, including commitments already made to in-flight arrivals. Do not count unused capacity twice or restart the deadline on replacement. If coverage cannot be established, leave the update and reservation changes unpublished; that refusal itself must retain a timely safe route.
- **Separate the carried residual from the fresh response.** Fix weights, merge, update rule, schedule, clocks and immediate outputs. For each branch i evaluate the executed proposal with the real gradient and with zero gradient from the *same* pre-step state; call the latter the zero-input proposal and the difference the fresh increment. If the optimizer includes decoupled weight decay, subtract its common contribution before calling the zero-input proposal a momentum residual. Require nonzero, nontrivial branch contributions whose projections cancel on A and C separately, reinforce on shared B, and do not starve either branch's useful fresh B response. Check signed response before and after merge. For an adaptive optimizer the difference is not generally a fixed matrix times the gradient. Use legal slot transformations (signed permutations for diagonal Adam, congruence for full moments) and price extra representation. Run actual nonzero-gradient suffixes with held-out data once the paths diverge.
- **Match outcomes and pay for commitments.** A and C are independent old readers; score ordinary held-out tasks at every served prefix, on refusal/fallback and after the longest declared suffix. Compare realized B and ordinary-update utility at matched retention, and retention at matched realized B/ordinary utility where a common point exists. Report refusals, held and peak capacity, execution and proof bytes, probes, proposals, validation and critical-path time. Grant every control the same actions, executor rights, observation times and fault model. Keep exact contingent search with atomic staging, a frozen menu, make-before-break, full re-underwriting and update refusal in the comparison; an exact scheduler with the same action set may tie by construction. On slots grant pooled Adam, true resetting, single-reader orientation, joint direct search, GEM/PCGrad, a residual-only projector and [preview-aimed momentum][preview] their strongest legal implementation. This is a targeted nearest-work check, not an exhaustive search.

## Exact paper fixtures, not wins over controls

**M · The replacement must fit before the original tick.** Live state is `(x,y,c)=(1,0,0)` after branch 1 sets x to 1 from zero. A requires `|x+y|≤1`; C requires `|c|≤1/2`. A mandatory tick immediately after D=3 adds 1 to x. At t=1 an ordinary maintenance update offers `c←1/4` (its own useful output) and retires the authorization for the `+` finish on lane L. The only admitted B observations are `+`, `−` or no-show, resolved just after the t=1 transaction. An executor acts on only the selected finish; a finish writes y on completion and leaves c alone. B earns one only if its requested target (y=−1 for `+`, y=−2 for `−`) is reached by D. The reservations below name absolute slots, not a fresh budget. No other failure or delay is admitted in this example.

| Observation | Before the update | After the same publishing step | A immediately after finish → after tick |
|---|---|---|---|
| `+` | L, slots [1,2) and [2,3), y←−1 | R, slots [1,2) and [2,3), y←−1 | 0 → 1 |
| `−` | S, slot [2,3), y←−2 | unchanged | −1 → 0 |
| no-show | same S finish, no B credit | unchanged | −1 → 0 |

If both R slots can be reserved in the publication, commit the update and release the old L reservation; C now reads 1/4 throughout. If R cannot start before t=2, it completes at t=4 and the update must be refused. Refusal keeps L, C reads 0, and all three cases still have a finish. Publishing the eviction anyway strands `+`: x+y=2 at the tick with no legal finish. Changing the B entitlement or extending D would mask the failure. Exact contingent scheduling with atomic staging ties; this fixture distinguishes a same-deadline replacement from a fresh promise.

**S · Both readers see real and opposite residuals.** Let two three-coordinate branches start at zero weights and merge by sum. A reads merged x, C reads merged y, each with tolerance `|readout|≤1/2`; B rewards merged z. Execute preconditioned heavy-ball, `mᵢ←mᵢ/2+gᵢ; wᵢ←wᵢ−Dᵢmᵢ`, with fixed diagonal gains `D₁=diag(1,2,1)` and `D₂=diag(2,1,2)`. The untouched slots are `m₁=(−2,−1,2)`, `m₂=(1,2,1)`. Reorient both by sign reversal; this preserves norms and weights. Use `g₁=g₂=(0,0,−1/2)` for two steps (linear loss).

| Paired arm, first step | Branch 1 proposal | Branch 2 proposal | Merged proposal |
|---|---|---|---|
| Residual | (−1,−1,1) | (1,1,1) | (0,0,2) |
| Fresh increment at the same state | (0,0,1/2) | (0,0,1) | (0,0,3/2) |

A and C read zero at both prefixes in the untouched and paired arms. Reorienting only one branch makes both old readouts have magnitude 2 at step 1. Merged z is −1/2 then 3/4 untouched, versus 7/2 then 27/4 paired. Fresh increments are identical across reorientation arms in this fixed-preconditioner model. As a negative, weight branch 2 by 3/2: the paired arm sits on both old boundaries at step 1 and violates both at step 2 (magnitude 3/4). Direct joint steering ties the positive witness; to earn a mechanism claim, broaden the legal choices, use nonconstant gradients and price search and precision.

## Idea cards

### Replacing an option while work continues

#### 01. Same-step substitution receipt (P)
- **Mechanism:** Give a live ordinary update a commit receipt binding the invalidated option, the covered observations, the replacement's executable reservation and the unchanged deadline; the update is inert until the receipt commits.
- **Novelty vs nearest prior art:** Make-before-break switches a service asset and contingent scheduling already covers recourse. The proposed unit of mutation is one live late-choice obligation under an ordinary model update, not an active route.
- **Cheapest first test:** Enumerate M with timely, late and revoked R capacity, and B arriving at either side of the commit boundary. Compare frozen menu, make-before-break and exact re-underwriting with atomic staging.
- **Old-task retention check:** Evaluate A/C on both boundary views, after the tick and after refusal; separately score completed maintenance and promised B.

#### 02. Repair the reservation through an augmenting exchange (I)
- **Mechanism:** A replacement can shift a different live menu's reservation onto an alternative lane, recursively, but commits the full exchange only if every affected menu is still jointly backed at its own original deadline.
- **Novelty vs nearest prior art:** Augmenting paths and multiresource scheduling are established. This adapts them to reservations owned by live model obligations with multiple mutually exclusive finishes; it is not a new matching theorem.
- **Cheapest first test:** Give two concurrent menus one scarce lane plus two alternatives. Exhaust jointly possible arrivals and compare local exchange, independent per-menu budgets and exact rescheduling at equal resources.
- **Old-task retention check:** Test both menus' A/C readers together at full simultaneous demand, and include an exchange that works separately but double-books a finish slot.

#### 03. Carry the choice that is already in flight (P)
- **Mechanism:** Export a handoff mapping from reachable progress states of a selected but unfinished finish to continuing actions and reservations. The ordinary update may change the remaining writes, not the admitted B choice or its absolute deadline.
- **Novelty vs nearest prior art:** Checkpoint migrations and make-before-break ([tree precedent](make-before-break.md)) hand over execution. The candidate is a progress-indexed refinement certificate for a finish with visible intermediate effects, not saving and replaying its prefix.
- **Cheapest first test:** Interleave one token eviction at each boundary in a two-write finish. Compare restart, pin-until-finish and exact prefix-aware recourse; insert a first write that cannot be safely repeated.
- **Old-task retention check:** Score A/C on the actual in-flight prefix, both continuations and the post-deadline suffix. A lost or doubled B side effect fails separately.

#### 04. Give the update a coverage write set (I)
- **Mechanism:** Attach versioned dependency manifests to guards, reservations and reader envelopes. Reprove touched obligations and carry others only when the update is certified not to change their premises, including indirect optimizer effects.
- **Novelty vs nearest prior art:** Incremental verification and [Pacti][pacti] contracts are close; this is a cost claim for proof reuse under optimizer-aware invalidation, not a new verification calculus.
- **Cheapest first test:** On a four-finish finite host, mutate a declared dependency, a truly unrelated field and a shared clipping threshold absent from a planted incomplete manifest. Compare full proof replay and cached proofs with the same checker.
- **Old-task retention check:** Use distinct A/C readers, including the one reached only via clipping, on every permitted post-update suffix; the incomplete manifest must not license publication.

#### 05. Synthesize a replacement shared by hidden histories (P)
- **Mechanism:** Bind replacements to the chooser's information classes; when a maintenance update merges observations, synthesize one remaining script per merged class rather than unioning finishes that require unavailable history.
- **Novelty vs nearest prior art:** Conformant planning and adjustable recourse already require nonanticipation. The candidate interface couples an observation-changing update to a checked rewrite of an already live obligation.
- **Cheapest first test:** Erase a version tag distinguishing two worlds. Give each a safe finish in isolation but only one shared option, then remove that option. Compare exact partial-information search and paid tag retention.
- **Old-task retention check:** Evaluate A/C in both indistinguishable worlds with the same action, including the refusal case; demand the original B result in both.

#### 06. Replace a proof that otherwise expires mid-finish (P)
- **Mechanism:** A finish carries valid-through times for its guard, executor and old-reader envelope; a same-step substitute can renew those dependencies only if its proof covers the entire remaining trace through D and the promised post-finish check.
- **Novelty vs nearest prior art:** Leases and time-bounded shielding cover expiry. The candidate object is a finish proof whose lifetime can be switched without moving the externally promised delivery time.
- **Cheapest first test:** Vary the expiry of a read envelope over start, write and delivery in a two-tick script. Compare conservative global expiry, pinning dependencies and exact timed shielding.
- **Old-task retention check:** Check A/C just before and after each expiry boundary under a fresh ordinary gradient, on both admitted and denied maintenance.

#### 07. Sell genuine slack without borrowing a deadline (I)
- **Mechanism:** Replace one expensive finish with a cheaper equivalent and make a concurrent ordinary update executable using the freed absolute slots; account for the replacement search and validation before calling the slots usable.
- **Novelty vs nearest prior art:** Resource reclamation and adjustable robust optimization, e.g. [Neur2RO][recourse], are near neighbors; the claim is a measured service frontier, not a novel reserve calculation.
- **Cheapest first test:** Enumerate two-resource finish costs under a maintenance write and include a smaller total cost with a worse critical path. Compare exact replanning and a static safety reserve.
- **Old-task retention check:** Probe A/C on the reclaimed-capacity schedule and the static schedule at matched B and maintenance progress; reject the low-work but late finish.

#### 08. Learn a host with redundant finishes, not redundant checkpoints (P)
- **Mechanism:** While acquiring A/C from truthful targets, optimize for two independently executable finishes per future demand class on development windows. Freeze writes, reservation rules and host before blind ordinary invalidators and B arrivals.
- **Novelty vs nearest prior art:** Fault-tolerant planning adds fallback actions and [OGD][ogd] protects a trained task. The candidate trained property is substitutability under disjoint version/authority failures, not redundant copies of a saved state.
- **Cheapest first test:** Fit a tiny CPU host with two independently editable features; hold out an invalidator and a B demand. Compare matched-width ordinary training, spare capacity and a host trained for one legal finish.
- **Old-task retention check:** Match pre-window A/C accuracy, then check blind A/C at publication, invalidation, finish and ordinary tail; a redundant route with lower B utility does not count.

### Paired orientations with separate readers

#### 09. Make a cancellation pair a selectable object (P)
- **Mechanism:** Offer a pair of nonzero legal orientations with opposite signed A and C projections and additive signed B projections; attach per-branch and merged fresh-B response floors to the pair.
- **Novelty vs nearest prior art:** [GEM][gem], [PCGrad][pcgrad] and single-reader orientation can protect an update; the claimed object certifies component residuals and the fresh path instead of only the total step. Direct joint search is an oracle control.
- **Cheapest first test:** Enumerate signed permutations around S with unequal diagonal gains and a B direction overlapping A, including pairs feasible for only one old reader. Compare resets, projection and single-branch steering.
- **Old-task retention check:** Evaluate A, C and an unseen mixed old input at each nonzero-gradient prefix, and compare at matched attained B.

#### 10. Balance cancellation under a moving merge weight (P)
- **Mechanism:** Offer a small family of orientations conditional on a pre-dispatch merge-weight observation, certifying a residual envelope across the quantization interval for each observed weight and charging every state change.
- **Novelty vs nearest prior art:** [Merge-weight ranges](merge-weight-ranges.md) certify coefficients and [Shampoo][shampoo] supplies preconditioning. The proposed interface attaches executed residual/fresh bounds to the observable coefficient bins, not a new kind of interpolation.
- **Cheapest first test:** Start from S's weight perturbation; enumerate allowed bins across two ticks. Compare one robust fixed pair and exact joint selection with the same observed coefficients and operation budget.
- **Old-task retention check:** Probe A/C at bin edges and on a held-out interleaving; do not serve a coefficient whose certified interval breaks either floor.

#### 11. Couple decay spectra, not just first steps (P)
- **Mechanism:** Match complementary signed residual components by their old-reader-visible decay modes under a declared optimizer schedule. Prefer pairs whose cancellation persists over the entire suffix rather than aligning only their first updates.
- **Novelty vs nearest prior art:** [Adam][adam] supplies moment decay and [slot echo][echo] follows live slot effects across orders. Here the proposed signature is a pair across *different* preconditioners with separate old readers and an independently preserved fresh channel.
- **Cheapest first test:** Use two diagonal heavy-ball branches with different decays and a pair that cancels at tick one but not tick two. Compare direct finite-horizon search, repeated projection and decay tuning at equal steps.
- **Old-task retention check:** Read A/C through the full tail, including a schedule switch that separates matched modes; require matched B when comparing the tail.

#### 12. Charge the first branch hidden by merge compensation (I)
- **Mechanism:** Reject not only net B starvation but also a branch whose fresh gain falls while its partner compensates. Attribute branch-local fresh response from paired zero/real shadow steps using the actual preconditioners and counters.
- **Novelty vs nearest prior art:** [Adam][adam] and [Shampoo][shampoo] already expose optimizer response; this is a diagnostic of masked loss of plasticity, not a new optimizer or a forecast score.
- **Cheapest first test:** Give one branch large second moments and offset it with high residual gain in the other; compare aggregate-only screening, both-branch floors and reset at equal reached B.
- **Old-task retention check:** Test A/C during the common suffix and after a lawful branch reroute that exposes the weak branch; distinguish A/C failure from a B-only veto.

#### 13. Allow reader curvature to veto a signed match (P)
- **Mechanism:** Bind pairing to a finite trust region for the *composed reads after the executed update*, using interval or exact small-region evaluation rather than declaring success from two cancelling linear projections.
- **Novelty vs nearest prior art:** [CROWN][crown] and shielding already certify nonlinear maps. The candidate is a reader-specific contract over slot-only choices that can cross gates while still maintaining fresh B.
- **Cheapest first test:** Replace C in S with a ReLU-based reader, create equal local Jacobians with different gate crossings, and compare tangent projection, direct rollout and exact finite-region verification at equal probe access.
- **Old-task retention check:** Check ordinary A/C on both sides of the gate and after fresh B moves again; include a safe crossing so that a blanket no-crossing rule is a measurable control.

#### 14. Learn where residual steering must not spend fresh gain (P)
- **Mechanism:** Fit a preconditioner partition on separate development tasks so a small steerable block carries complementary residuals and a separately checked channel remains responsive to fresh B. Freeze the partition before blind tasks.
- **Novelty vs nearest prior art:** [Activation-Keyed Momentum][akm] already learns anisotropic momentum updates keyed to activations; [Shampoo][shampoo] already enriches preconditioning. Here the proposed reusable partition is trained for branch-to-branch cancellation on independent readers plus separate fresh transmission, with no effective-LR-only claim.
- **Cheapest first test:** Learn a two-block partition in a tiny CPU linear host; compare random partitions, retuned diagonal Adam, and arbitrary equally sized blocks chosen by direct search; include a held-out B direction outside the trained block.
- **Old-task retention check:** Compare ordinary A/C at matched B, on held-out mixed old directions and after the first change in gradient sign.

#### 15. Spend precision only on the cancellation error (I)
- **Mechanism:** Use coarse legal orientations and allocate precision only to the terms contributing enough rounding error to break the two old-reader margins; require a positive signed fresh-B floor under the executed arithmetic.
- **Novelty vs nearest prior art:** [Slot echo][echo] already earns rounding margin, and mixed precision is standard. Here the measurable hypothesis is smaller storage or execution cost for a pair's realized cancellation, not bitwise order equivalence.
- **Cheapest first test:** Enumerate fixed-point variants of S near both thresholds. Compare uniform precision and direct allocation with the same resident/peak bytes and deployment rounding rule.
- **Old-task retention check:** Score A/C on adversarial roundoff signs as well as ordinary held-out inputs and verify the check refuses a boundary-crossing pair.

#### 16. Show when shared B necessarily taxes an old reader (I)
- **Mechanism:** For a finite legal slot alphabet or an explicitly relaxed joint set, return a Pareto boundary between residual B reinforcement and maximum A/C deviation; label unattainable only with a sound bound.
- **Novelty vs nearest prior art:** [OGD][ogd] already exposes null-space restrictions and [GEM][gem] imposes inequalities. This is a feasibility audit for paired residuals with fixed fresh response, not an edit-capacity predictor.
- **Cheapest first test:** Rotate B toward the span of A/C in S until the B floor is incompatible with both old tolerances; compare exhaustive search and convex bounds, including an alphabet whose relaxation has a gap.
- **Old-task retention check:** Replay the highest legal B option and the first violating option on both ordinary readers; report if refusal preserves A/C but misses B.

### Coupling the two invariants

#### 17. Exchange reservations for a paired-slot-only replacement (P)
- **Mechanism:** Let an ordinary write invalidate the only weight-based finish for a demand. In the same commit substitute a legal paired orientation and its timed suffix, if that suffix realizes the same B entitlement and leaves both old readers safe.
- **Novelty vs nearest prior art:** Parent #17 attaches slots to a write; recourse and gradient surgery cover the parts. The candidate interaction is that slot pairing changes whether an already promised finish is executable at all, not that a successfully scheduled finish gets extra B.
- **Cheapest first test:** Enumerate one weight finish, one legal pair and two arrivals; put the weight executor out of reach before D. Compare a scheduler with best protected momentum stacked, and exact joint scheduling with access to the same pair.
- **Old-task retention check:** Read A/C through the exposed half-state, the update, first slot consumer and missed-deadline negative; require the original B target, not only a fresh-gradient proxy.

#### 18. Let reclaimed slot time pay for the real ordinary write (P)
- **Mechanism:** A joint exchange admits maintenance only when the substitute finish's paired residual completes the B target with fewer *actual* pre-D steps; reserve its gradient compute and use the released slot for maintenance atomically.
- **Novelty vs nearest prior art:** Scheduling can reclaim unused capacity and momentum can accelerate progress. The candidate contract is for a shorter executable completion horizon under a retained two-reader guarantee, not optimistic runtime prediction.
- **Cheapest first test:** Couple small integer reservations to a three-axis quadratic; hold out a gradient reversal that erases early B lift. Compare static and adaptive scheduling plus tuned reset/steering, with exact joint search as ceiling.
- **Old-task retention check:** Check A/C at both compressed and full lengths, at the ordinary write and after D. Credit earlier completion only at matched actual B and maintenance output.

#### 19. Treat the consuming tick as a priced finish dependency (P)
- **Mechanism:** If maintenance changes which optimizer tick first consumes the pair, replace both an orientation and the reserved consumer slot in one transaction. A proof about an unused buffer cannot back a finish.
- **Novelty vs nearest prior art:** [Slot echo][echo] checks a consuming update and parent #06 checks reservations. The proposed operation switches the consumer and its certified slot response together under the old deadline.
- **Cheapest first test:** Add a mandatory clipping tick before one of two possible consumers. Compare pinning the original tick, retiming only, recomputing only and exact combined recourse at equal compute.
- **Old-task retention check:** Measure A/C before and after clipping, at the real consumer, and under a timeout; a timely write whose consumer is too late must not pass for B.

#### 20. Refinance the pair across an Adam clock split (P)
- **Mechanism:** If an ordinary update advances one optimizer clock and retires the original finish proof, commit only with a newly certified slot pair, its correct clocks and the compute to execute it by D. Do not save or rewind clocks.
- **Novelty vs nearest prior art:** [Adam][adam] determines bias correction and [slot echo][echo] distinguishes live state from snapshots. The candidate is atomic substitution over a mixed-clock suffix, not clock normalization.
- **Cheapest first test:** Enumerate legal signed permutations across two one-dimensional blocks, with unequal first/second-moment ages and a shared B readout in one block. Compare fixed orientation, pooled Adam and joint clock-aware search under the same observability.
- **Old-task retention check:** Evaluate A/C at the clock-change boundary and first two actual B steps; include a sequence where raw first moments cancel but native proposals fail.

#### 21. Branch-local offers with a joint nonanticipation proof (P)
- **Mechanism:** Each supplier gives a versioned set of feasible residual/fresh response bounds and absolute slot offers. Accept a maintenance substitution only when one causal joint selector matches both offers on every admitted observation, including correlated uncertainty and competing reservations.
- **Novelty vs nearest prior art:** [Pacti][pacti] composes contracts and [compositional shielding][shield] restricts joint actions. The candidate guarantee ties complementary residual *signatures* to independently held execution rights; matching two marginal envelopes is not enough.
- **Cheapest first test:** Enumerate a pair of hidden states with identical marginal offers but different joint matchings; compare centralized exact search, independent selection and a scheduler with the best paired optimizer given identical information and bytes.
- **Old-task retention check:** Exercise all admitted observation classes with the same public selector, and test A/C on refused substitutions and a lawful suffix with one withdrawn offer.

#### 22. Keep the reserve and the residual on separate ledgers (I)
- **Mechanism:** Run a factorial audit (replacement on/off, pairing on/off), then compare the joint method against the strongest independent stack with the full action and observation set. Attribute a gain only to changed feasible traces, not to accounting one resource as zero.
- **Novelty vs nearest prior art:** Parent #21 already requires an interaction; this extends the audit to ordinary invalidations at unchanged deadlines, not a third primitive.
- **Cheapest first test:** Construct a separable toy where staging and momentum both help but their combination merely adds gains, then a crossed host where both are necessary for a finish. Use exact joint search to check that all arms received legal alternatives and price slack before and after commit.
- **Old-task retention check:** Check A/C on every relevant prefix with matched B and maintenance outputs, including an allowed B at the latest instant and refusal of an impossible substitution.

## Ranked deeper questions

1. **Is there a reusable local replacement proof that matches exact re-underwriting's admissions without its global cost?** Start with 01–05. Use overlapping observation classes, in-flight progress and simultaneous reservations; make the late replacement in M a mandatory negative. Compare at identical D, allowed failures and B/maintenance utility. A tie with ordinary incremental contingent scheduling makes this a scheduling improvement.
2. **What is the smallest slot interface that still predicts executed two-reader cancellation and both fresh paths?** Start with 09, 11–13 and 16. Test heterogeneous decay, a nonlinear crossing and B overlapping an old direction. Try to falsify the need for a pair with the best single-reader projection stack and exact joint steering. A zero-input or first-tick-only result is not enough.
3. **Can pairing and same-deadline substitution offer a trace the best independent stack cannot, at the same budget?** Start with 17–19 and 22. If the same observations, actions and reservation rights let the stack select the same admissible traces, test for cheaper proof/search rather than claiming a larger feasible set. No gain if a fresher deadline or lower B entitlement pays for it.
4. **Can ordinary training buy future substitutability before the invalidator is known?** Cross 08 and 14 on held-out invalidators and held-out B suffixes, granting identical width, optimizer state and ordinary old-task accuracy. If equal-width redundancy or tuning a fixed preconditioner suffices, keep the result as an improvement only.

**Verdict:** Keep the same-step replacement receipt and the branch-local residual/fresh coupling as conditional primitive candidates. First try to make exact scheduling and joint protected steering tie them. The most promising combined test is a replacement that only becomes executable before the original deadline once a legal paired suffix is available, with a genuine ordinary update served and both old readers retained. The fixtures establish the boundaries, not that such a benefit survives the controls.

[parent]: https://github.com/manojbajaj95/cl/pull/222
[triage]: https://github.com/manojbajaj95/cl/blob/386a2f189c0504915a7c884be43e5754d1d86be7/reviews/flood-triage.md#L337
[ledger]: https://github.com/manojbajaj95/cl/blob/386a2f189c0504915a7c884be43e5754d1d86be7/reviews/idea-ledger.md
[preview]: https://github.com/manojbajaj95/cl/pull/207
[echo]: https://github.com/manojbajaj95/cl/blob/226f9d7a6a9fab414091c186b20df53e80ed9913/tree/slot-echo.md
[pacti]: https://arxiv.org/abs/2303.17751
[shield]: https://arxiv.org/abs/2410.10460
[recourse]: https://arxiv.org/abs/2310.04345
[gem]: https://arxiv.org/abs/1706.08840
[ogd]: https://arxiv.org/abs/1910.07104
[pcgrad]: https://arxiv.org/abs/2001.06782
[adam]: https://arxiv.org/abs/1412.6980
[shampoo]: https://arxiv.org/abs/1802.09568
[crown]: https://arxiv.org/abs/1811.00866
[akm]: https://arxiv.org/abs/2608.19491
