# Live branch handshakes and silent optimizer-state rotations

**Status:** Ideas only; no experiments, training code, or GPU work. **Parent:** [Joint branch moves](joint-branch-moves.md) ([PR #199](https://github.com/manojbajaj95/cl/pull/199)), cards 2 and 7. **Review seed:** [Flood triage row 308](https://github.com/manojbajaj95/cl/blob/e752d5679d852780990c3ab78a3c7dbd83833ea0/reviews/flood-triage.md#L308), both score 3: execute a zero-gain first move live under an enforceable partner completion obligation; jointly rotate both branches' momentum and second-moment buffers while fixing their weights and merged outputs.

**Ledger read first:** The [idea ledger](https://github.com/manojbajaj95/cl/blob/e752d5679d852780990c3ab78a3c7dbd83833ea0/reviews/idea-ledger.md) rules out exact save/restore as a primitive, asks forecasted plasticity gains to survive retention matching, and requires a combination to beat the best stack of its constituents at equal budget. Each first test below includes retention on ordinary old tasks, not just the constraint used to find the move.

## What would make either operation new?

- **A live obligation, not retroactive safety.** The first move goes into service, is safe now, and raises neither admitted B utility nor the advertised suffix-certified merge range. But while it is live, an ordinary read or update scheduled within a finite horizon would break an old promise without the exact partner action. Before publication, reserve that action (mutable state/version, write authority, and service time), bind its deadline to the relevant event, and prove the bounds for every allowed interleaving. A promise or timeout notification alone cannot make an unsafe state safe. If arbitrary partner failure and mandatory progress are simultaneously allowed, either an independently executable completion is already secured or the move must be refused. A freeze or old-version route is a separate paid control, not proof that the live branch is safe on its own.
- **A state intervention, not a coordinate relabel.** Fix both branch weights, merge coefficients and rule, all immediate merged outputs, the suffix task sequence, and the update budget. Only the optimizer state changes. Rotate first moments as vectors and full second moments by congruence, using each branch's declared frame; the first exact diagonal case is a signed permutation (permute the variances without signs). A generic rotation induces off-diagonals that diagonal Adam cannot store; charge a block representation, or certify the discarded terms' effect on executed updates. Keep bias counters, schedule, epsilon and merge semantics fixed and explicit. Score separation under the same gradients at the first suffix step, then under the same data and step rule as trajectories diverge. If weights, gradients and readouts are also rotated and mapped back, an equivariant optimizer should give no gain.
- **A strict realized gain.** Let A denote ordinary old tasks, C other declared protected readers or slices, B the new-task utility, and S₀ the already promised coefficient set. Keep A/C floors on S₀ at every served prefix and for every admitted fault schedule; claim S₁ only when it strictly contains S₀ with the same floors over the declared future horizon. Report realized B for each admitted target and independent held-out A/C after the sequence, not just how much spare range was offered. Fix precision, information and retention budgets. Charge reserved compute, deadlines, rejected admissions, latency including freezes, proof and state bytes, and recovery. Never substitute sampled old-task success for a sound bound on declared readers.

These are close to standard assume-guarantee planning, [compositional shielding](https://arxiv.org/abs/2410.10460) and [control barrier functions](https://arxiv.org/abs/1903.11199). Grant an atomic transaction the same legal endpoints, grant exact serial search the same actions and horizon, and stack a deadline-aware shield with the best slot control. On the slot side, [Adam](https://arxiv.org/abs/1412.6980), [Shampoo](https://arxiv.org/abs/1802.09568), [gradient surgery](https://arxiv.org/abs/2001.06782), [GEM](https://arxiv.org/abs/1706.08840), [Git Re-Basin](https://arxiv.org/abs/2209.04836) and [task arithmetic](https://arxiv.org/abs/2212.04089) supply preconditioning, projected updates, alignment and weight merging, not a demonstrated advantage for this paired intervention. Also grant independent slot changes, parent card 7's reset and single-branch splice controls, fresh and pooled state, and direct joint slot search. Where the slot representation is lossy, match storage and test bytes, not just rank.

## Two paper witnesses, not results

**Live route in a three-event window.** Let branch coordinates be x and y, starting at (0, 0). A protected squared error is (x+y+b)² ≤ 1, where b is a late new-task coefficient in [0, 1]; larger b means higher B utility. Start with the promise S₀ = {0}. The ordinary suffix contains one mandatory tick x ← x+1. With no handshake, that tick leaves x+y = 1, so no b > 0 can be promised across the horizon. The route is:

| Event | Live pair | Sum x+y | What may be served |
|---|---|---|---|
| Initial | (0, 0) | 0 | S₀ |
| Publish branch 1's x ← 1 | (1, 0) | 1 | S₀ only; no B gain |
| Execute bound branch 2 action y ← −2 | (1, −2) | −1 | Admit [0, 1] only once the action is live |
| Run the mandatory tick | (2, −2) | 0 | [0, 1] |

If branch 2 goes first, the protected error is 4 at b = 0. If it misses the deadline and the tick runs after branch 1 alone, the error is again 4. Serving the middle state thus requires control over that race: e.g. an already authorized executor reserved to apply y ← −2 before the tick, under a stated failure model. If neither executor nor gate can guarantee it, refuse before publishing branch 1. An atomic switch to (1, −2) also works; the witness separates live serial execution from the parent's intermediate that can remain safe indefinitely, not from a fully capable scheduler. A separate C readout of an untouched coordinate can catch accidental edits but does not explain the effect. The next test must allow more moves than this toy (including alternative x/y magnitudes) and charge the exact search and atomic controls.

**Slot-only widening under a fixed merge rule.** Use two coordinates and fixed zero starting weights. For branch i, take bias-normalized first moment mᵢ and diagonal second moment vᵢ. At a single zero-gradient momentum tick, define dᵢ = mᵢ/√vᵢ elementwise in units absorbing a common positive decay/bias factor; use zero epsilon for this witness (all variances positive). The shared suffix applies the negative weighted sum −(u d₁+v d₂) to the merged weights for u,v ∈ [0, 1]. This mixes **preconditioned proposals**, not raw buffers into a single Adam instance. The old x-readout requires |x| ≤ ¼, and B rewards negative y. Start with:

| Branch | mᵢ | vᵢ | dᵢ before | dᵢ after swapping both axes in both slots |
|---|---|---|---|---|
| 1 | (4, 1) | (16, 4) | (1, ½) | (½, 1) |
| 2 | (3, −12) | (36, 576) | (½, −½) | (−½, ½) |

Before the tick every branch and merged output is identical across interventions. For the suffix, S₀ = {u+v/2 ≤ ¼}; the paired swap gives S₁ = {|u−v|/2 ≤ ¼}, strictly containing S₀ in the unit square. At (1, 1) the old x-readout stays zero and y becomes −3/2. Swapping only branch 1 or only branch 2 yields x = −1 or −½ there; swapping both first moments but neither second moment gives x = 7/4. A double reset can keep x safe in this tick but yields zero B progress. This only separates the named controls at a point, not all legal single-branch edits; unrestricted damping or a direct joint projected update might win. It is not evidence that the gain persists for nonzero gradients, pooled Adam or competing old slices.

## Idea cards

### Make the second move binding without hiding the first

#### 01. Transfer the completion right before taking the zero-gain step
- **Mechanism:** Bind a precise, versioned branch-2 write to a deadline event and transfer execution authority to a reserved completer before publishing branch 1. Ordinary readers then serve the real half-state, not a shadow checkpoint.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** Parent card 2 motivates the obligation; two-phase commit hides the half-state and a shield can simply block. The proposed object is a live model state that can be admitted with a reserved future write as part of its safety proof.
- **Cheapest first test:** Enumerate every completion, delay and default ordering in the live-route witness with and without a pre-authorized completer. Compare greedy coordinate descent, independent projection, atomic cutover and exact serial search on B progress, service time and proof bytes.
- **Old-task retention check:** Serve A and C after every event at S₀ and every newly admitted b; inject a partner default and an independent completer failure, and confirm the latter is either covered by the stated model or refused before publication.

#### 02. Trade wall time for protected event credits
- **Mechanism:** Promise completion before the kth relevant old-task event rather than after t seconds; reserve separate credits per reader so unrelated traffic can continue without consuming safety slack.
- **Novelty vs nearest prior art — CANDIDATE:** Barrier-function shields bound reachable behavior. This proposes a transferable, reader-scoped unit of remaining *live exposure* tied to a concrete partner write, not a universal timeout.
- **Cheapest first test:** Add mixed safe and hazardous ticks to the live witness. Compare event credits with a fixed deadline and an equally informed time-varying shield under bursty and permuted arrivals.
- **Old-task retention check:** Check ordinary A and rare C on all admitted prefixes, including an adversarial burst of the sensitive reader at the last credit; measure how many unrelated A reads still finish.

#### 03. Underwrite a late-bound completion menu
- **Mechanism:** Bind branch 2 to deliver one of several legal writes by the same deadline, without selecting the write until B arrives. Reserve enough resources for the most expensive option, and reject if the menu can become empty.
- **Novelty vs nearest prior art — CANDIDATE:** Compositional shielding permits multiple admissible actions. Here the reserved menu preserves **late B choice** after a zero-gain live move, instead of certifying the safety of just one known endpoint.
- **Cheapest first test:** Add two late B readouts to the live witness, each with a different valid y completion. Compare early binding, shadow atomic search and exact online planning with equal information, and erase one option adversarially.
- **Old-task retention check:** Check A/C on S₀ through the late-choice window and on each completion with its newly admitted B option, including refusal when the last remaining completion loses its reservation.

#### 04. Bind capacity for overlapping handshakes, not each promise in isolation
- **Mechanism:** Reserve the complement writes of multiple half-moves against a common resource calendar and cap exposure by the tightest shared reader. Refuse the second handshake if its slot can only be made available by breaking the first.
- **Novelty vs nearest prior art — IMPROVEMENT:** Deadline scheduling and compositional shielding already price shared resources. Apply them to model continuations and check whether independently certified obligations are composable in practice.
- **Cheapest first test:** Duplicate the live witness with two partner writes due in one execution slot. Compare per-pair admission, exact scheduling and admission with a conservative common guard.
- **Old-task retention check:** Inspect A/C for both pairs at every possible completion order and at the shared deadline; count a promise lost in either pair as failure, even when aggregate scores improve.

#### 05. Substitute the executor without substituting the write
- **Mechanism:** Make a completion transferable only to an executor that can prove the same post-state under the current branch version. Run the already bound step after a primary outage; do not restore the earlier x.
- **Novelty vs nearest prior art — IMPROVEMENT:** Replicated coordinators already provide failover. Test whether a model-state write can use independent failover without needing an atomic replication barrier longer than the window you wanted to save.
- **Cheapest first test:** Add one backup, asymmetric failover delays and a version race to the live witness. Compare primary-only, replicated atomic and pre-authorized takeover at equal reserved compute.
- **Old-task retention check:** Run ordinary A and C after single failure, duplicate delivery and late takeover; treat duplicate application and serving a stale intermediate past the deadline as failures.

#### 06. Keep readers live with a dependency-specific fence
- **Mechanism:** Gate only the old reader or suffix transition that can expose the unsafe half-state; unrelated readers observe the real intermediate. Attach an enforceable maximum fence duration and price violations as service loss.
- **Novelty vs nearest prior art — IMPROVEMENT:** Read/write locks and compositional shields already narrow blocking. The question is whether the affected scopes learned from a model can be fenced more cheaply than an atomic branch barrier without dropping C readers.
- **Cheapest first test:** Give the witness two readers with overlapping but unequal dependencies, then compare whole-model pause, exact dependency fence and continuously served reserved completion.
- **Old-task retention check:** Probe both readers, one rare bypass caller, and ordinary A under every served interleaving; report availability separately so refusing all requests cannot masquerade as retention.

#### 07. Put a remaining-route certificate on each live prefix
- **Mechanism:** After each zero-gain or negative-but-within-budget step, attach the exact set of still-executable partner continuations. Revoke *future* admissions when this set shrinks; use only an already-reserved safe exit for an obligation in flight.
- **Novelty vs nearest prior art — CANDIDATE:** Model-predictive safety shields replan from the current state. Here a prefix carries a reusable, externally checkable proof that a particular learner can remain live and hand off its remaining obligation.
- **Cheapest first test:** Extend the witness to four events with two alternative suffixes and one version change. Compare full recertification at each tick and a cached remaining-route proof at equal action search.
- **Old-task retention check:** Check A/C at each real prefix and through the reserved exit; inject a hidden C reader and measure how much of the claimed route became uncertifiable.

#### 08. Search for genuinely binding windows in continuous fibers
- **Mechanism:** Characterize where safe-at-present but unsafe-if-uncompleted states form a nonzero-width region under continuous single-branch moves and a fixed operational disturbance, rather than at one hand-picked discrete point.
- **Novelty vs nearest prior art — AUDIT:** Control barrier methods and exact reachability already find safe corridors. This tests whether the parent's need for live commitment survives removal of the hand-selected candidate grid.
- **Cheapest first test:** Relax x and y in the witness to intervals, cap both branch velocities, and solve the small piecewise-linear reachability problem with and without reservable completion. Include unbounded or slower-drift regimes as negative controls.
- **Old-task retention check:** Bound worst-prefix A/C over each reachable interval and score held-out old residuals near its boundaries; if an unbound route retains A/C at the same deadline and B gain, count no handshake credit.

### Change future training without changing the current model

#### 09. Swap signed optimizer axes only as a pair
- **Mechanism:** Jointly choose signed axis permutations for both m and v, treating signs properly, while leaving the two weights and their merge exactly fixed. Spend the widened suffix range on an actual late B choice.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** Parent card 7 supplies the slot-only move. Adam stores the slots and Git Re-Basin permutes weight representations; the distinction is a paired intervention on executable future updates, without a weight reparameterization.
- **Cheapest first test:** Enumerate the signed axis permutations in the slot witness, plus first-moment-only swaps, resets and fresh state. Then replace the zero-gradient tick by common nonzero A/B minibatches and compare a direct projected update at matched B progress.
- **Old-task retention check:** Verify bit-identical current outputs for both branches and all merge choices under the unchanged merge rule; evaluate A/C at each subsequent tick, including ordinary old inputs outside the search probes.

#### 10. Rotate a dense covariance only in a certified block
- **Mechanism:** Keep full second moments for a small block that actually needs a non-permutation rotation. Propose paired rotations there, use the native diagonal optimizer elsewhere, and bound the effect of block leakage on the suffix tube.
- **Novelty vs nearest prior art — CANDIDATE:** Shampoo already retains structured second-order state. The candidate is a fixed-weight paired block intervention with a checked protection tube, not a cheaper preconditioner.
- **Cheapest first test:** Rotate a two-by-two covariance by 45 degrees, embed it in a four-coordinate quadratic and compare true block updates, a diagonal approximation, fresh state and equal-byte unrotated block state.
- **Old-task retention check:** Match all current A/C outputs; bound the intended old block and test an independent C reader that straddles the block boundary across three suffix ticks.

#### 11. Choose the rotation by its omitted off-diagonal cost
- **Mechanism:** Choose paired rotations whose ideal full-covariance trajectories can be implemented with diagonal state plus a certified small error budget; refuse when the accumulated rounding and projection error exhaust the old-task margin.
- **Novelty vs nearest prior art — IMPROVEMENT:** Structured preconditioners and [4-bit optimizer states](https://arxiv.org/abs/2309.01507) already trade representation fidelity for bytes. Here the bit/error tradeoff is tested against deployment-specific old-task suffix floors after a paired intervention.
- **Cheapest first test:** Sweep one angle and one anisotropy parameter on a rational two-dimensional quadratic. Compare exact block and diagonal rotations at matched bytes and exact projected-update error estimates.
- **Old-task retention check:** Compare the declared error tube against actual A/C on every suffix tick at deployed precision and against a hidden old readout aligned with the discarded term.

#### 12. Make the pair work under both proposal mixing and pooled Adam
- **Mechanism:** Treat the composition rule as part of the certificate: mix preconditioned proposals in one arm and merge moments into a single optimizer in another. Search for paired transforms robust to both, or return an explicit rule-specific witness of failure.
- **Novelty vs nearest prior art — AUDIT:** Adam and task arithmetic define different aggregation points. The novelty claim is tested against commutation failure rather than assuming a proposal-mixing toy establishes anything for a shared Adam state.
- **Cheapest first test:** Reuse the slot witness under normalized pooled moments and under proposal mixing. Enumerate signed permutations at the same horizons for each rule and compare the certified sets, including fresh and pooled unrotated state.
- **Old-task retention check:** For each rule, score immediate output parity and worst-prefix A/C on S₀ and proposed S₁ separately; test a held-out A slice whose gradient differs from the protected x coordinate.

#### 13. Prove the gain is not a gauge symmetry
- **Mechanism:** Use an uncompensated slot-only branch-pair transform in one arm and rotate weights, slot tensors and gradient/readout coordinates consistently and map back in an equivariant control.
- **Novelty vs nearest prior art — AUDIT:** Git Re-Basin and Shampoo already motivate equivalent coordinates and structured updates. This is an attribution test: the paired result must depend on changing physical update vectors, not their notation.
- **Cheapest first test:** Repeat the slot witness with an exact signed permutation equivariant optimizer, then a dense rotation with a matrix preconditioner that transforms by conjugation. Match rounding, epsilon policy and streamed batches.
- **Old-task retention check:** Require prefix-level A/C equality for the equivariant control, and check ordinary A/C and B after the uncompensated move. A gauge arm with measured gain invalidates the comparison.

#### 14. Cancel old drift now without canceling future B learning
- **Mechanism:** Search for a paired orientation that sends residual momentum into B-useful directions but whose preconditioner also admits B gradients over a short shared horizon; forbid proposals that just erase momentum or suppress all updates.
- **Novelty vs nearest prior art — CANDIDATE:** GEM and gradient surgery constrain or modify individual updates. This attempts to make one paired slot rewrite pay for a complete suffix without repeated projection, at matched realized B utility.
- **Cheapest first test:** Add a late B gradient sign reversal and a correlated old gradient to the witness. Compare fresh state, per-step projected updates, joint slot search and a constant learning-rate reduction at equal A/C bounds and utility.
- **Old-task retention check:** Check each A/C prefix including the reversal and ordinary old tasks after the suffix; discard solutions that clear the old floors by effectively stopping learning.

#### 15. Allocate each protected reader to a different moment interaction
- **Mechanism:** Use one paired subspace transform to neutralize first-moment drift on A and a second to reshape denominator-induced drift on C. Refuse when one certificate spends the other's margin.
- **Novelty vs nearest prior art — CANDIDATE:** Multi-task gradient surgery already reduces current gradient conflicts; this tests two simultaneous constraints on the future effects of first and second moments, not just a conflict between gradients.
- **Cheapest first test:** Extend the slot witness to three coordinates with two old readouts and two future batch orders. Enumerate first-moment-only, second-moment-only, independent and paired changes, plus a direct projected-gradient control.
- **Old-task retention check:** Require every A and C floor separately on each prefix and withheld old readouts, including a rare reader spanning both constrained subspaces. Report the worst reader, not mean old accuracy.

#### 16. Refuse slot moves when a hashed state summary hides the dangerous direction
- **Mechanism:** Exchange bounded bilinear sketches of each branch's slot-induced updates on protected readouts. Search over all compatible m/v states and refuse if two aliased states disagree on safe suffix headroom.
- **Novelty vs nearest prior art — CANDIDATE:** The parent already sketches weight interference; 4-bit states compress optimizer storage. Here the refusal object concerns aliased *future preconditioned responses*, including indistinguishable first moments with different denominators.
- **Cheapest first test:** Enumerate integer slot states and find same-summary pairs with opposite outcomes on the old x gate. Compare a direct update sketch, separate m/v summaries and full exchange with all bytes charged.
- **Old-task retention check:** Bound A/C over every compatible state before admitting S₁; exercise held-out old readouts on admitted states and report false refusals as well as any missed break.

#### 17. Check expiry under momentum decay rather than promising headroom forever
- **Mechanism:** Attach a step counter and admissible input tube to a paired rotation. End its authority before decay or a suffix gradient shift makes the protected cancellation expire.
- **Novelty vs nearest prior art — IMPROVEMENT:** Adam's recurrences already forget old state and barrier analysis already bounds horizons. This measures the useful lifetime of a paired certificate under real continued learning rather than treating tick-one range as permanent.
- **Cheapest first test:** Iterate exact first/second-moment recurrences on a short shifted quadratic stream. Sweep β₁, β₂ and warm-state age against fresh, reset, projected and pooled controls; keep counters equal.
- **Old-task retention check:** Check A/C through expiry and through the next ordinary update under the replacement certificate or refusal, plus old tasks not used to choose the lifetime.

#### 18. Keep an optimizer-state notch valid for previously unseen B choices
- **Mechanism:** Choose orientations on past gradient regimes to create a band of future update directions that avoids an old reader, then spend it on unseen B mixtures without refitting the orientation.
- **Novelty vs nearest prior art — CANDIDATE:** Shampoo learns local preconditioning; projected replay methods such as GEM use old gradients. Here the transferable unit is a paired orientation sustaining a late-choice set, and it must beat the best simple protected optimizer, not a forecast of plasticity.
- **Cheapest first test:** Hold out entire gradient-mixture edges in small quadratics with matched singleton tasks; compare paired rotation to direct robust slot fitting, fresh state and a protected optimizer at the same old-task access and byte budget.
- **Old-task retention check:** Measure stationary and shifted A/C at every prefix for each held-out mixture, as well as B improvement; if the advantage vanishes under retention matching, drop the claim.

### Make the two seeds interact

#### 19. Open a slot-only window, then make the partner finish before the first suffix tick
- **Mechanism:** Rotate branch 1's slots live without changing weights or earning B credit; bind branch 2's slot rotation before an ordinary shared update. Serve old inference on the actual half-state, then execute the partner step and the real update independently.
- **Novelty vs nearest prior art — SYNTHESIS CANDIDATE:** An atomic slot swap hides the intermediate and a reset kills carryover. The candidate is a visible, function-silent window whose correctness requires a partner action before training progresses. It must beat a deadline shield stacked with the paired slot control.
- **Cheapest first test:** Modify the slot witness to give branches normalized proposals (1, ½) and (−1, ½). Use an unsigned swap on branch 1 and a swap with both signs flipped on branch 2, giving (½, 1) and (−½, 1). At the promised choice (1, 1) the mandatory tick's x displacement is 0 with neither or both swaps, but ±½ with either alone (old cap ¼). Joint completion doubles negative-y progress from 1 to 2. Compare live ordered execution with the best pre-staged atomic swap and a shield plus the best slot control; add nonzero gradients only after reproducing the mandatory-tick failure.
- **Old-task retention check:** Check A/C at live half-state reads, the first tick under every permitted interleaving, and all later admitted coefficients. Inject a default and verify that the unbound half-state really fails, not just that schedule metadata changes.

#### 20. Bind a gradient-use budget instead of binding a fixed slot value
- **Mechanism:** Reserve a branch-2 rotation from a checked set that can absorb the realized first gradient bin, and debit an explicit number of protected gradient events before deadline. Old inference can remain open while the training admission gate enforces the reservation.
- **Novelty vs nearest prior art — SYNTHESIS CANDIDATE:** A compositional shield supplies event gating and GEM supplies protected updates. The proposed interaction is reserving adaptable slot geometry before revealing B, rather than projecting each gradient after it arrives.
- **Cheapest first test:** Use two gradient bins and a two-event route on the paired witness; compare early binding, a delayed atomic slot swap, per-step GEM and a shield with the same reserve authority and information.
- **Old-task retention check:** Enumerate A/C violations on every permitted bin sequence, including bin-boundary gradients, with held-out ordinary A after completion; reject if no robust bin-wise completion exists.

#### 21. Isolate the benefit of making intermediate state visible
- **Mechanism:** Cross live vs shadow execution with paired rotations on vs off, and include the stack of an exact deadline-aware scheduler with the best paired state control. Only credit live exposure if it creates a cost or utility advantage over shadow execution, not just a different trace.
- **Novelty vs nearest prior art — AUDIT:** Transactions, preconditioning and factorial attribution are established. The audit prevents relabeling an ordinary staged slot edit as a new learning operation.
- **Cheapest first test:** Enumerate the two witnesses and a combined stream with an ordinary request served between the half-steps. Measure completed old and new requests, tail latency, reservations, stalls and proof bytes; allow the atomic control to pre-stage the same work.
- **Old-task retention check:** Enforce the same A/C floors and availability targets in all cells; give every arm the same held-out old requests and include updates after the handoff, not just identical immediate outputs.

#### 22. Return an impossibility certificate instead of falling back to rollback
- **Mechanism:** Show a concrete admissible failure/time/gradient schedule on which no continuation can complete from a proposed half-state before an old bound is broken. Refuse the live move upfront, while still allowing an atomic endpoint if feasible.
- **Novelty vs nearest prior art — CANDIDATE:** Reachability tools already produce counterexamples. A branch-specific refusal can identify whether no safe completion exists because of authority, timing or the optimizer's response to a shared batch, and separate that from infeasibility of the endpoint itself.
- **Cheapest first test:** Turn off the independent completer in the live witness and force the tick; then enumerate the first suffix gradient in the slot witness. Compare full reachable-state search and compressed certificates on whether they refuse exactly the impossible windows.
- **Old-task retention check:** Reproduce refusal witnesses on A/C, verify the surviving atomic route separately, and run ordinary old tasks from the unchanged state after refusal. Count false refusals and lost B opportunities.

## Ranked deeper questions

1. **Can a zero-gain live move that truly depends on partner completion beat the best enforceable scheduler plus atomic or exact serial search?** Start with the live-route witness and cards 01, 02, 08 and 22. Require normal serving from the real half-state, an explicit losing default trace under a mandatory event, and a proof that trace is excluded in the admitted failure model. Vary the continuous action set and allow paid fallback. If an atomic control with identical pre-staging ties on latency, B and old-task retention, call it scheduling.
2. **Does slot-only pairing buy suffix headroom when the suffix actually learns, including under pooled Adam?** Use cards 09–15 and 17; move beyond a zero-gradient tick, test multiple task orders and both composition rules, and match immediate outputs, realized B, old-task floors and state budget. If the best single-branch change, fresh-state protected optimizer or per-step projection ties, there is no new pairing operation in that regime.
3. **Is there a regime in which the two mechanisms interact rather than just compose?** Use cards 19–21. Require a live half-state that serves a useful request, a missed completion that demonstrably harms A/C, and a positive paired advantage over a reservation-aware scheduler stacked with the strongest slot baseline. An atomic-only improvement supports the slot idea, not the handshake.
4. **Can certificates be reused under private state and late B choices without turning into expensive recertification?** Use cards 03, 07, 16 and 18. Hold out entire gradient families and failure schedules. Measure useful choices retained, refusal errors and total proof/communication bytes against exact rechecking and a paid cached controller; safety must not come from assuming away aliased states.

**Verdict:** Keep both as conditional primitive candidates, not as results. First try to falsify the live obligation against an equally capable scheduler and the paired slot intervention against a retention-matched protected optimizer on short, nonzero-gradient suffixes. Keep the synthesis only if it beats the stack without hiding the intermediate, dropping an old task or subsidizing the reservation.
