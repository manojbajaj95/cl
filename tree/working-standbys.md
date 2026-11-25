# Working standbys and inherited residual tails

**Status:** Ideas only; two exact paper fixtures and proposed CPU tests, no training or GPU. **Parent:** [Trained redundant finishes and matched fade profiles](redundant-finishes.md) ([PR #245][parent]). **Review seeds:** [Flood triage][triage] scores parent 06 and 14 at 3: useful ordinary A or C work from the very state that can independently finish B, and handing a retired branch's remaining cancellation obligation to a different partner without resetting the accrued discrepancy or the deadline. Cards 01 and 12 pin down those reference designs.

**Ledger read first:** The [idea ledger][ledger] rules out save/restore as a new primitive, requires checks on ordinary old tasks, and demands that a crossing beat the best stack of its parts. **P** marks a candidate reusable state, operation or interface; **I** marks an improvement, audit or limit. These are proposals, not reviewer verdicts. The comparisons to [PackNet][packnet], [parameter superposition][superposition], [gradient projection memory][gpm] and the local tree are targeted nearest-work comparisons, not priority claims.

## What the two promises mean

- **One state, two jobs.** A and C are distinct old tasks, B is the incoming job. The standby's mutable live state must causally support both real old-task service on its usual cadence and a separate B finish. Show this with a state-specific intervention that preserves budget and route IDs, not just a shared trunk or an auxiliary training loss. Disable the primary's actions, cached outputs and private state from the common committed prefix. Shared dependencies must survive the declared fault, and a blind shared-state fault must count as an uncovered case unless a third route actually covers it. Give the chooser only public observations; one causal policy must work for all hidden states compatible with them. Hold preparation and the admission policy fixed across held-out failures and demand instances, while allowing declared live A/C writes.
- **Transfer a liability, not a snapshot.** When a branch retires, its past effects remain in the actual live state. After retirement no one may read its private state or run its remaining updates. The new partner takes over the duty to offset the *survivor's* remaining residual, with the realized drift and original clock carried in. In a fixed linear fixture, for each reader $j$ demand $d_j(\tau)+\sum_{t=\tau+1}^{s}(r^{\rm survivor}_j(t)+r^{\rm partner}_j(t))$ stay within its margins for **every** prefix $s$; include observation points between non-atomic actions. The profiles are signed, reader-visible zero-input contributions after removing common weight decay. For adaptive optimizers and nonlinear hosts, use shadow real-gradient and zero-gradient proposals from identical pre-step states to diagnose contributions, then test the actual joint suffix with real gradients. Zero-input profiles need not superpose. No clock reset, hidden repair, discarded drift or deadline extension. Require meaningful carried residuals, useful fresh B response, and lawful reservations; if no partner can absorb the obligation, retain a pre-reserved safe action or decline the preceding publication. Score any B refusal as unserved.
- **Pay for doing both.** Match width, training examples and compute, resident/peak bytes, reserved capacity, observations and fault rights, start margins, deadlines, realized B utility and actual A/C maintenance throughput. Report refusals, recovery, validation costs and time. Match retention when comparing delivered work and match delivered work when comparing retention (or report disjoint frontiers). In addition to parent-style dedicated redundancy, compare ordinary multitask training plus an equally sized hot or warm standby, equal-byte checkpointing, and hand-designed task-state reuse. For tails give whole-trace matching, fresh-tail matching, restart/reset, reservation exchange and exact contingent replanning the same legal actions and initial drift. Crossed designs must beat the best independently tuned stack under the same budget. Exact search on the very same host can tie coverage by construction; a claim about learned feasibility must compare hosts, and a claim on the same host must measure costs.

## Exact paper fixtures, not wins over controls

**W · The standby works, but does not survive a common-mode fault.** A independently serves a bit $a$. C publishes $c\in\{0,1\}$ from a mutable one-bit cell after an ordinary correction. A blind B request supplies a bit $q$ and asks for $c\oplus q$ at $D=2$. The primary has its own cache with the current $c$; the standby computes the result from C's live cell. Both caches, update traffic and the standby's dispatch step are charged; even this tiny setup needs the request, not a copied B answer. Take the correction $c:0\to1$ at tick 0 and $q=1$ at tick 1. A public primary-cache fault at tick 1 leaves C serving 1 and the standby delivers 0 by tick 2. Hold the primary disabled and flip only the working cell back to 0: C serves a stale value and the standby gives the wrong B answer 1. If the declared fault includes both copies, neither finish is available. A normal shared-state multitask design with the same fault boundaries can tie; this is a test of attribution and failure independence, not a claim that caching C is new.

**T · Identical fresh mismatch magnitude, different legal partners.** Retirement is public at tick 1, with A/C drift $(1/4,1/2)$ and margins $(3/8,3/4)$ relative to the pre-write state. The old-reader direction is $v=(1,2)$. At ticks 2 and 3 the survivor contributes $(1,1/2)$ in multiples of $v$; two resident, already legal partners contribute $(-5/4,-5/8)$ and $(-3/4,-3/8)$. Each trace has decay $1/2$ after its first remaining tick. Give both choices the same independent fresh B increment $1/2$ per tick (so either finishes B = 1 at $D=3$); compare resource reservations and execution rights unchanged. The retired branch is not invoked.

| Replacement | Fresh net prefixes in multiples of $v$ | Actual cumulative drift in multiples of $v$ (ticks 1, 2, 3) | A/C pass? |
|---|---|---|---|
| $(-5/4,-5/8)$ | $(-1/4,-3/8)$ | $(1/4,0,-1/8)$ | Yes |
| $(-3/4,-3/8)$ | $(1/4,3/8)$ | $(1/4,1/2,5/8)$ | No, at tick 2 |

From a fictitious zero drift both replacements pass and tie on maximum absolute mismatch. Reverse the already accumulated drift and the ranking reverses. If the legal replacement set contains only the wrong-sign partner, there is no legal handoff even though B could be delivered on time. This is an exact fixed-readout example with a stipulated B channel; it says nothing about the addition of nonlinear or adaptive optimizer traces.

## Idea cards

### Making old-task work carry an actual reserve

#### 01. Train a working standby, not a busy second head (P)
- **Mechanism:** During development train C's live representation against a joint loss on ordinary C corrections and a standalone B finish after removal of the primary. Use a frozen dispatcher and price the standby at every tick.
- **Novelty vs nearest prior art:** A [hot standby][hot-standby] already serves routine reads against replicas while preparing to take over writes; dual use is not new. Here truthful C work updates the working carrier itself, and the test is whether training that carrier buys a fault-independent B write by the same deadline without replaying the primary's private state. Compare against hot standby on its strongest legal terms.
- **Cheapest first test:** Extend W to a three-feature linear model with withheld C corrections. Compare multitask sharing plus an independent head and a dedicated equal-byte standby. Disable the primary and ablate only the standby's working feature; include a fault that loses both carriers.
- **Old-task retention check:** Score held-out A and current-version C at every correction, at the fault and after B; count any missed C deadline even when its eventual answer is correct.

#### 02. Exchange maintenance obligations, not just compute slots (P)
- **Mechanism:** Keep the standby serving a bounded queue of C requests. Its B invocation comes with an atomic reassignment of pending C requests to an already authorized third lane, preserving their arrival times and version requirements; C completion is part of admissibility.
- **Novelty vs nearest prior art:** Mixed-criticality scheduling can preempt background tasks; #235 exchanges B reservations. Here standby withdrawal transfers a live old-task service obligation as well as reserving B, so a B time slot alone does not grant the right to spend the carrier.
- **Cheapest first test:** Enumerate three lanes, two C deadlines and one B fault time. Compare mixed-criticality scheduling, parent reservation exchange and exact joint scheduling; make spare compute available but no version-correct C executor in the negative case.
- **Old-task retention check:** Deliver the pending C responses against their original deadlines and versions, and probe ordinary A during the reassignment and after B.

#### 03. Renew a failed finish with the next truthful correction (P)
- **Mechanism:** Train the maintenance update so that a legitimate correction to stale C also restores a lost B witness. Credit only the correction already owed to C, and make the deadline binding even if no correction arrives.
- **Novelty vs nearest prior art:** Parent 07 renews redundant readiness with an ordinary update; replay repairs a spare explicitly. The narrower test is whether *current C error* supplies the corrective information for a specific lost B route, rather than requiring a chosen recovery batch or letting any convenient update count.
- **Cheapest first test:** In a four-state learner, enumerate both signs of a C correction, a zero correction and withheld arrival. Compare parent renewal, direct replay and warm synchronization at equal bytes/steps; include a useful C correction that cannot fix the B witness.
- **Old-task retention check:** Score C on both corrected and unchanged examples, and A under every renewal and non-arrival; a stale C answer that preserves readiness is a failure.

#### 04. Encode the standby across useful old-task views (P)
- **Mechanism:** Use two working views for A and C; design each view to independently reconstruct the same compact B write precondition after loss of its sibling. Both views must earn distinct ordinary service before the loss.
- **Novelty vs nearest prior art:** Erasure coding and [parameter superposition][superposition] store redundant or overlapping information. The proposed operation compiles *different task-serving views* to yield a common executable B precondition, with no rebuild or primary interpolation before D.
- **Cheapest first test:** Exhaust three-bit linear maps over GF(2) on a correlated and an uncorrelated A/C stream; compare explicit parity, a separate duplicate and a shared multitask trunk with equal read and state budgets.
- **Old-task retention check:** Score A/C on held-out values before the outage and after takeover, including whether a paid alternate old-task route serves the lost view; otherwise count the outage as inadmissible.

#### 05. Preserve readiness under net-zero changes in old answers (P)
- **Mechanism:** Teach C's correction rule to operate on two equivalent internal encodings. Make each allowed recoding carry a small transformation of the B finish interface, so B remains executable without restoring C's earlier encoding.
- **Novelty vs nearest prior art:** Symmetry-based model alignment and equivariant models handle recoding; task outputs alone can identify equivalent old predictors. The contract requires transporting *the continuation* through an old-task-invisible recoding that would otherwise strand a standby.
- **Cheapest first test:** Swap two ReLU units during truthful C maintenance. Compare canonicalization, full interface recomputation, a frozen subnetwork and legal transport; include a quantized recoding that preserves C's labels but does not preserve B's continuation.
- **Old-task retention check:** Check ordinary A/C at the swap and through B, plus fresh corrected C examples to rule out simply refusing representational updates.

#### 06. Make each accepted correction carry a readiness receipt (P)
- **Mechanism:** Bind a local proof obligation to a C update: either show the new state still contains a standby that executes under all admitted faults, or reserve a different safe route in the same publication. Reuse a receipt only for later updates inside its certified domain.
- **Novelty vs nearest prior art:** Shields and #235 same-step replacement already reject unsafe actions. The experiment tests a narrower reusable proof over the *old-task update class*, which can amortize validation even when the actual working standby state changes.
- **Cheapest first test:** Use small quantized linear C updates inside and outside a sound envelope; compare per-write exact checking, periodic validation and freezing. Measure validation costs at equal coverage; a legal C gradient that crosses the envelope should force fresh checking or refusal.
- **Old-task retention check:** Run ordinary A/C after accepted, revalidated and refused writes. Count the opportunity cost of rejected C corrections and verify A/C after spending the reserve.

#### 07. Infer the live substitute from old work without an extra probe (P)
- **Mechanism:** Condition selection on a public result from a C computation that was already due before the B decision. Train permitted output-preserving internal paths so an existing public service receipt separates which lane can finish; private tags and post-fault shadow runs are not permitted.
- **Novelty vs nearest prior art:** Parent 04 exposes invalidators; active fault diagnosis buys informative probes. Here ordinary old service pays for the distinguishing event and must remain correct whether or not B arrives. If existing telemetry already suffices, there is no new mechanism.
- **Cheapest first test:** Use a two-lane controller with two hidden fault states and the same B request; compare full diagnostic probes, passive logging and robust selection without a signal. Include identical public transcripts with different surviving finish lanes as an impossibility case.
- **Old-task retention check:** Verify C's actual ordinary answers and timing in both fault states, not the diagnostic bit alone; check A under each choice and when dispatch must refuse.

#### 08. Use an old-task error signal to precondition the backup without sharing failure (P)
- **Mechanism:** Feed only the published signed C error to a separately writable B standby module, while also requiring the underlying C state during execution. Train the two together but arrange that faults in the primary's private adapter cannot poison this signal or its updater.
- **Novelty vs nearest prior art:** [PCGrad][pcgrad] manages gradient interference in multitask sharing and warm synchronization copies state. This proposes a low-width, independently maintained update channel that prepares a substitute without letting primary optimizer state become an undeclared dependency.
- **Cheapest first test:** Learn two scalar features with aligned and conflicting C errors. Compare shared gradients, a fully isolated head, equal-bandwidth replay and no error channel under blind primary-slot removal; a corrupted public error is a required common-mode negative.
- **Old-task retention check:** Score ordinary A/C across both benign and conflicting updates and after substitution; keep C correction rate fixed so ignoring routine errors cannot win.

#### 09. Train distinct reserves against the same byte bottleneck (P)
- **Mechanism:** Given competing old-task representations, choose developments that diversify the minimum failure cuts through working state, not just the output heads. A shared feature earns its keep only if either the fault model spares it or a second working representation supports the same B demand.
- **Novelty vs nearest prior art:** Parent outage matrices audit fixed dependencies; fault-tolerant ensemble training may diversify predictions. Here the search target is distinct executable write dependencies under the same old-task throughput and physical-state budget.
- **Cheapest first test:** Exhaust a small graph with redundant heads on a common feature versus distributed features. Compare cuts after training, disjoint duplication and exact structural search on a normally trained host. Use a common backing-cell fault that defeats superficially separate heads.
- **Old-task retention check:** Ablate each admitted dependency and check A/C on held-out examples before and after B, including low-support examples that unconstrained diversification sacrifices.

#### 10. Separate working state from decorative service (I)
- **Mechanism:** Run matched interventions: capacity-preserving substitution of the standby state, removal of its B executor, and removal of its old-task read. Require that a single identified live component affects both outputs; also search for a hidden duplicate.
- **Novelty vs nearest prior art:** Causal ablation and [PackNet][packnet] masks already identify carried task structure. This is an attribution audit distinguishing a genuinely reused live component from billing unrelated old service to the spare.
- **Cheapest first test:** Construct a true shared cell, disjoint payloads in one module and a ghost copy with equal resident bytes. Compare whole-module knockout and matched coordinate substitution; the audit should flag only the first as dual-use.
- **Old-task retention check:** In the unmodified and control runs, test ordinary A/C before and after executing B; intervention-induced old-task failures are attribution evidence, not permission to lower the retention floor.

#### 11. Bound reserve coverage under jointly useful but mismatched old data (I)
- **Mechanism:** Identify pairs of histories that look identical in the standby's allotted state and public observations but need incompatible B writes. Measure the minimum extra bits that separate those histories without reducing the old service rate.
- **Novelty vs nearest prior art:** Sufficient statistics and the [minimal-wake-anchors][anchors] bit bound address recoverability. Here the collision is between distinct feasible write continuations despite both histories continuing to perform ordinary old tasks.
- **Cheapest first test:** Enumerate one- and two-bit standby encodings for two C histories with identical current labels and opposite B witnesses. Include a replay bit, a larger warm spare and a truthful C distinction; report only a conditional finite lower bound.
- **Old-task retention check:** Require each encoding to pass the same unseen A/C requests before and after a finish or refusal; don't count dropping one history's old service as resolving the collision.

### Transferring residual obligations without a clean slate

#### 12. Hand a signed remaining tail to a live partner (P)
- **Mechanism:** On public retirement, price and bind an already legal partner using the survivor's remaining profile and the actual reader discrepancy, then execute that suffix using the original deadline.
- **Novelty vs nearest prior art:** Parent whole-trace matching assumes the pair remains; #235 reservation exchange replaces resources. The portable object here includes a signed, accrued liability that changes partner admissibility even at identical finish cost.
- **Cheapest first test:** Use T, its sign mirror, and the singleton wrong-sign menu. Compare fresh-tail matching, restart, momentum reset and exact replanning from the true state; then add a nonzero common fresh gradient.
- **Old-task retention check:** Test A/C immediately before and after retirement, each later prefix and the post-D tail; a transient breach cannot be canceled away.

#### 13. Split a departing obligation across two working partners (P)
- **Mechanism:** Compose two legal partial couplings over the remaining ticks, with a public allocation of signed tail contributions and occupancy. Neither partner owns a valid transfer alone, and both remain useful to their respective old tasks.
- **Novelty vs nearest prior art:** Joint gradient projection allocates simultaneous updates, and tail matching pairs whole traces. The proposed operation is divisibility of an *existing prefix-constrained debt* across independently schedulable working carriers.
- **Cheapest first test:** Use two readers where each candidate can move only one reader's drift. Compare one-partner transfer, [GPM][gpm] plus a new write, and exact joint search. Include a case where each final sum passes but concurrent execution overloads a tick.
- **Old-task retention check:** Check A/C at any interleaving of the partial transfers, score displaced maintenance and test held-out old tasks again after all residuals decay.

#### 14. Leave the successor a liability it can pass on (P)
- **Mechanism:** At the first handoff, constrain not only current feasibility but also the accrued discrepancy at any declared second retirement cut. Reserve a viable second recipient without committing which fault will occur.
- **Novelty vs nearest prior art:** Contingent planning reasons over multiple faults; parent interruption contracts cover a pair under clock skips. The test is whether a reusable incoming/outgoing residual contract lets a local transfer preserve future assignments without re-enumerating obsolete branches.
- **Cheapest first test:** Enumerate three legal partners and two cuts where the smallest immediate drift exhausts future slack. Compare greedy handoff, exact recourse and enumeration with cached contracts; measure validation work, not coverage against identical exact search.
- **Old-task retention check:** Exercise held-out A/C after each of the two cuts and after final delivery, including a legal sequence that forces use of the pre-reserved fallback.

#### 15. Carry an uncertainty set for hidden debt (P)
- **Mechanism:** Publish a sound *joint* set of reader discrepancies conditional on the public trace. Match one executable successor against the entire set; if ambiguity blocks every partner, spend only an authorized probe that finishes before the original D.
- **Novelty vs nearest prior art:** Robust planning and reachability already propagate uncertainty; parent margin bands cover possible suffixes. The narrower interface crosses a retirement boundary with correlated uncertainty about *past* effects and no access to the retired state.
- **Cheapest first test:** Enumerate two histories with the same public drift bins and opposing debts. Compare a joint set, independent reader intervals, mean debt and exact belief-state search. Include a pair for which clairvoyant selections both pass but no causal choice does.
- **Old-task retention check:** Score A/C on both indistinguishable histories at every prefix, including during any probe and refusal; don't average away a failed history.

#### 16. Relay the debt between different optimizer clocks (P)
- **Mechanism:** Admit a successor by its reader-visible sequence under its own current clock, including preconditioning and fresh-gradient response. Select a legal bounded change of basis on full moments or a legal signed permutation on diagonal slots; keep ages and accumulated drift fixed.
- **Novelty vs nearest prior art:** #235 handles clock splits; optimizer transport preserves parameter-space coordinates. The candidate is a handoff defined by future execution and prefix margins, not by equal slot values or age matching.
- **Cheapest first test:** Compare two scalar Adam paths with different ages and equal first proposals; introduce a nonzero gradient at tick 2. Compare counter matching, a reset, whole-trace matching and exact forward simulation at equal B gain.
- **Old-task retention check:** Check A/C at dispatch, every actual update and tail expiry, including a perturbed second moment that sends a real subsequent step outside tolerance.

#### 17. Retire the producer but preserve a public read-order contract (P)
- **Mechanism:** Transfer a schedule of permissible old-reader observation points together with the debt. Replace a retired branch only if the new partner can cancel at every already owed observation, including reads between non-atomic writes; don't invent downtime.
- **Novelty vs nearest prior art:** Parent 13 constrains interruptions of a fixed pair, and atomic staging avoids torn reads. This makes a reader-order contract transferable across different legal partner latencies without changing the service schedule.
- **Cheapest first test:** Enumerate two partners with identical tick-end traces but different sub-tick write availability. Compare atomic staging with charged buffers, tick-end matching and exact interleaving checks; include an already committed read between writes.
- **Old-task retention check:** Run ordinary A/C at every promised sub-tick observation, during refusal and after B; silent quiescence counts as a missed old-task read.

#### 18. Route debt using a separating old-reader witness (I)
- **Mechanism:** Generate one reader, time and signed bound that rules out a candidate, and use it to shortlist replacements; a separate exact check still validates the chosen route before retirement is committed.
- **Novelty vs nearest prior art:** Parent 16 and counterexample-guided synthesis already produce mismatch witnesses. This is a search-cost improvement only: use witnesses of *carried* drift to choose which legal partner to check next.
- **Cheapest first test:** Exhaust a menu with first-tick ties and narrow late margins. Compare exhaustive validation, cached whole-trace mismatch witnesses and a cheap sign heuristic. Report only time/probe savings at identical safe coverage.
- **Old-task retention check:** Reproduce blocked prefixes on real ordinary A/C inputs and test both readers throughout every accepted suffix and fallback.

#### 19. Convert old corrections into legal tail payments (P)
- **Mechanism:** Offer several truthful versions or orders of a due old-task correction (e.g., distinct batches for the same current C target). Bind the subset of its **executed** effects that safely reduces accrued A/C drift; reserve an independent action if the required correction never arrives.
- **Novelty vs nearest prior art:** Replay and gradient projection steer fresh updates, and [producer rewrites][producer] asks old corrections to repair a park margin. This targets a signed liability inherited at retirement, with useful B response and a short, unchanged finish budget.
- **Cheapest first test:** Enumerate two equally useful C batches in a tiny heavy-ball learner, one with the wrong sign for the inherited debt. Compare projected gradients, separate maintenance plus handoff, and joint exact search; include a mandatory C correction that makes all transfers unpayable.
- **Old-task retention check:** Require held-out ordinary C improvement and no loss on other C cases; check A and C between the correction, B finish and tail expiry.

### Testing whether the two promises help each other

#### 20. Let routine C shape the signed offers available at a cut (P)
- **Mechanism:** Train a working standby to produce one of several legal tail responses as a consequence of which real C correction it most recently served. Dispatch using that public correction and the inherited debt; do not mutate or retrain the standby to fit after the cut.
- **Novelty vs nearest prior art:** Parent 06 supplies a useful spare and parent 17 trains paired fades. The interaction to test is whether ordinary C updates grow a useful menu of *signed replacement responses* without degrading C or a separately runnable B finish.
- **Cheapest first test:** Cross active versus idle standby with trained versus ordinary tail response in a two-reader, two-cut linear host. Compare the best stacked multitask standby and debt-aware replanner at equal resources. Add same-sign offers and a shared-state fault as negatives.
- **Old-task retention check:** Match throughput and margins on normal C examples and unseen correction orders; check A/C after either handoff or refusal and through the last tail tick.

#### 21. Choose a working-state quotient by both jobs and the transfer (P)
- **Mechanism:** Coarsen standby state only when two histories with the same public observation remain equivalent for ordinary A/C reads, standalone B execution and every allowed inherited-debt suffix. Train or compile the coarsening before blind evaluation.
- **Novelty vs nearest prior art:** State minimization and parameter sharing already compress task-equivalent learners. The proposed quotient preserves future write feasibility after a debt-bearing transfer as well as old and new outputs; compression that keeps only output equivalence can erase the sign needed at retirement.
- **Cheapest first test:** Minimize a finite working controller with two histories that differ only in the admissible partner at tick 2. Compare separate quotients and their product, a raw replay byte and the joint exact quotient. Measure peak bytes including decoder overhead.
- **Old-task retention check:** Replay held-out ordinary A/C continuations before failure and after each handoff from all represented histories; any new stale answer invalidates a merge.

#### 22. Find the failure load at which doing both stops paying (I)
- **Mechanism:** Map the frontiers for duty cycle, tolerance and failure correlation under one shared resource budget. Jointly charge the opportunity cost of a standby's C service and a successor's tail reservation, so the same spare tick can't be sold to both.
- **Novelty vs nearest prior art:** Capacity planning and the parent's paid redundancy audit already price reserves. This is a falsification map for the proposed combination, especially where work creates correlated faults or any safe tail payment displaces C, not a new optimizer.
- **Cheapest first test:** Exhaust a small scheduling lattice with a dedicated standby, an active standby, separate tail partners and the joint scheme; include independent failures, common-mode loss and separable workloads where the best stack should tie.
- **Old-task retention check:** Report worst-prefix A/C separately from total C throughput and delivered B. Include old-task service on faults, no-shows and refusals; do not condition the frontier on successful B alone.

## Ranked deeper questions

1. **Does ordinary work buy independent B coverage or merely make a replica look busy?** Start with 01, 04, 09 and 10. Freeze routing and test ordinary corrections, then blind primary-only and shared-state faults. Ask for better delivered service at matched resources and A/C margins than an equally warm multitask standby and hand-designed reuse. If intervention shows the old work and backup use disjoint state, report a scheduling gain at most.
2. **What must cross retirement for another partner to take over a real residual?** Start with 12, 15–17. Rank interfaces by charged bytes and validation time at equal prefix safety and B utility; use the sign mirror, hidden-history alias and an adaptive real-gradient suffix. If only full-state exact replay is sound, don't claim a portable tail contract.
3. **Can the same useful state make a legal transfer possible when the best independent stack cannot?** Start with 19–22. Use a factorial comparison on trained and ordinary hosts with matched action rights, first with an exact small scheduler. If the jointly trained host creates no new feasible case, look only for measurable amortization, not an invented feasibility advantage.
4. **Does reserve coverage renew under repeated truthful updates and retirements?** Start with 02, 03, 06 and 14. Run two blind windows, forbid per-window horizon resets, and count C corrections refused or rerouted. If another arrival needs a growing archive or delayed service, narrow the result to one paid substitution.

[parent]: https://github.com/manojbajaj95/cl/pull/245
[triage]: https://github.com/manojbajaj95/cl/blob/d4a0a35dc5eb7d693f3388480f8eae7e5106d5c7/reviews/flood-triage.md#L360
[ledger]: https://github.com/manojbajaj95/cl/blob/d4a0a35dc5eb7d693f3388480f8eae7e5106d5c7/reviews/idea-ledger.md
[anchors]: https://github.com/manojbajaj95/cl/pull/149
[producer]: https://github.com/manojbajaj95/cl/pull/247
[hot-standby]: https://www.postgresql.org/docs/current/hot-standby.html
[packnet]: https://arxiv.org/abs/1711.05769
[superposition]: https://arxiv.org/abs/1902.05522
[gpm]: https://arxiv.org/abs/2103.09762
[pcgrad]: https://arxiv.org/abs/2001.06782
