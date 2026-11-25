# Standby handovers: move the queue, divide the tail

**Status:** Ideas only; two exact paper fixtures and proposed CPU first tests, no training or GPU. **Parent:** [Working standbys and inherited residual tails](working-standbys.md) ([PR #256][parent]). **Review seeds:** [Flood triage][triage] scores #256 cards 02 and 13 at 3: when a working standby takes B, give its pending C queue to an already authorized third lane; when a partner retires, split the remaining signed obligation across two working partners that cannot take it alone. Cards 01 and 11 restate the seeds as controls.

**Ledger read first:** The [idea ledger][ledger] rules out save/restore as a new capability, forecasting without an executed intervention, and wins that disappear against the best equally resourced stack. **P** marks a candidate reusable object or operation; **I** marks an improvement, diagnostic or limit. These are proposals, not reviewer verdicts. Nearest-work comparisons are targeted and provisional.

## What would count

- **Move duty, not just a running job.** A and C are ordinary old tasks; B is the incoming task. At call-up, the reassignment transfers pending C requests atomically to an already authorized third lane, including original arrival, required version and deadline. Name the visibility boundary for arrivals, in-flight results and writes. Count lost, duplicate or stale outcomes, missed original deadlines and ordinary post-handover arrivals. The standby must be able to finish B without the failed primary's actions, cached output or private state. Compare the same declared fault set, including shared failures.
- **Divide future payments, not past drift.** Keep the realized drift at retirement and the original clock. In a fixed linear host, check every reader's original band against that drift plus the survivor's signed contributions and both partners' contributions at every observable prefix, including between non-atomic actions. The public allocation identifies each payer, action order and occupied capacity; the retiree never runs or contributes private state again. Require both partners to do actual ordinary work and neither to be sufficient alone under the same rights. For nonlinear or adaptive hosts, shadow zero- and real-gradient proposals from the same pre-step state only as diagnostics; execute the actual joint real-gradient suffix. Do not sum independently estimated tails as a certificate.
- **Pay against the strongest stack.** Freeze preparation, authority and routing rules before held-out requests and faults. One causal policy must act on public observations, not the hidden fault or future arrival sequence. Match compute, peak/resident bytes, training examples, reserved capacity, authority, observations, B utility, deadlines, and actual A/C service and start margins; report Pareto fronts if no matched point exists. Give the controls lawful versioned [queue groups][queue] or migration, [mixed-criticality scheduling][mc], dedicated warm standby, equal-byte checkpointing, [reservation exchange][menu], [projected updates][gpm], single-partner and [whole-trace][finishes] matching, and joint contingent search on tiny domains. Count refusals as unserved B; report fallback cost and A/C outcomes even on refusals. Exact search on the same host and rights can tie coverage: test online cost on that host, or compare feasible sets on differently trained hosts.

## Exact paper fixtures, not novelty claims

**Q · Taking the slot is not taking the queue.** At tick 1 the primary fails publicly and the standby needs ticks 1 and 2 to finish B by 2. Its queue already holds `c1=(arrival 0, version 1, deadline 1)` and `c2=(arrival 1, version 2, deadline 2)`; the tick-1 arrival is visible before the cut. The third lane has one slot per tick and can serve versions 1 and 2 respectively. Atomic reassignment before service serves both at their original deadlines; dropping pending work serves neither. A spare lane with only version 1 can serve c1 but not c2 even with the same free slots. A's independent held-out read remains unchanged. A version-aware queue scheduler with the same authority ties the positive case.

**S · Two final payments are not necessarily one safe split.** Let the old-reader drift at retirement be `(1/4, 1/4)` with closed bands `[-1/4, 1/4]` on A and C. At each of ticks 2 and 3, the survivor contributes `(1/4, 1/4)`, P contributes `(-1/4, 0)`, and Q contributes `(0, -1/4)`. Each partner has a reserved, distinct slot for an ordinary old-task action that produces its contribution. Reserve the survivor's B action after both partner slots and let it earn an independent B increment of `1/2` per tick (B = 1 by 3). Starting from `(1/4, 1/4)`, order P, Q, survivor gives `(0, 1/4)`, `(0, 0)`, `(1/4, 1/4)` each tick; either partner alone leaves the other reader at `1/2` at tick 2. Survivor first fails both reads at once, although the tick-end drift with P and Q is identical. If a C handover consumes Q's only slot and there is no joint action or other legal payer, the split is infeasible. This is a fixed-readout construction with stipulated B utility, not proof of additive adaptive tails or a win over exact scheduling.

## Idea cards

### Hand the old queue to a lane that can actually serve it

#### 01. Reassign the maintenance obligation atomically (P, #256 seed)
- **Mechanism:** Publish B activation and the third lane's acceptance of the bounded pending C queue in one transition; preserve per-request arrival, version and deadline, and reject if the queue cannot be served under the reserved schedule.
- **Novelty vs nearest prior art:** [Mixed-criticality scheduling][mc] already switches service levels, and [reservation exchange][menu] hands over B capacity. The proposed interface couples activation to actual acceptance of versioned old-task duty; a lawful transactional queue that already guarantees this is a direct control, not a weaker baseline.
- **Cheapest first test:** Enumerate Q with the original active standby, drop-on-preemption, a dedicated equally resourced warm standby, checkpointing and a version-aware queue scheduler; withhold the third lane's v2 right in the negative.
- **Old-task retention check:** Execute every due C request on its original clock and v1/v2 contract; run ordinary A during and after activation even if B is refused.

#### 02. Fit the third lane to the queue's service semantics (P)
- **Mechanism:** Train live C state so the normal writes emit a small, typed statistic that the third lane can combine with its own working state to answer versioned C requests. Seal the codec before blind queues; the original standby need not decode or finish C after call-up.
- **Novelty vs nearest prior art:** State migration and sufficient statistics are old; parent 21 compresses working-state equivalence. Here equivalence is for an entire pending versioned queue and is learned across two separately useful lanes, not measured only on identical current answers.
- **Cheapest first test:** Fit a two-lane linear model across v1/v2; compare full-copy migration, a fixed sufficient statistic and independently trained compression at equal bytes. Hold out a request distinguishing histories with the same current answer.
- **Old-task retention check:** Score the pending C versions and the third lane's own held-out old requests, plus A on either side of dispatch.

#### 03. Order routine C writes for the next cut (P)
- **Mechanism:** Among equally on-time C schedules, use truthful corrections in the order that leaves the third lane already able to serve the largest set of authorized next-cut queues. The live update order, not a preparatory copy, produces the reserve.
- **Novelty vs nearest prior art:** Deadline scheduling and pre-copy migration already manage cutover; [GraB][grab] orders training examples. Here old-task order shapes the *other lane's version-complete service set* through permitted live writes, with a frozen call-up rule.
- **Cheapest first test:** Enumerate two C correction orders with equal normal utility and a blind cut between them. Compare EDF, write ordering for C alone and proactive replication at equal traffic; include commuting corrections that should tie.
- **Old-task retention check:** Score all due C at the two original versions before and after the cut and held-out A after both orderings.

#### 04. Let one ordinary correction certify a whole family of cuts (P)
- **Mechanism:** Learn an invariant on the two lanes' C states under legal corrections that makes a third-lane acceptance certificate valid at multiple future cuts, provided the admitted queue belongs to an explicit demand class.
- **Novelty vs nearest prior art:** Assume-guarantee reasoning and parent 06 readiness receipts already avoid repeated checks. The candidate is a preserved *cross-lane request-version relation* that avoids per-request validation without widening authority.
- **Cheapest first test:** Enumerate six states and two version increments; compare per-request validation, a parent receipt and exact reachable-set checks. Insert a legal write that preserves current accuracy but breaks the relation for a pinned request.
- **Old-task retention check:** Deliver pinned and latest-version requests on their own deadlines and check ordinary A during a certificate rejection.

#### 05. Transfer a result only if its effect has not happened (I)
- **Mechanism:** Give in-flight C items public commit evidence: completed effects stay completed; uncommitted effects move with their original request, and any execution on the standby after the cut is fenced out.
- **Novelty vs nearest prior art:** [Queue acknowledgments][queue], idempotent sinks and migration epochs already cover commit/retry. This is a negative control for counting duplicated or silently discarded maintenance as retained learning, not a messaging primitive.
- **Cheapest first test:** Insert call-up immediately before and after a non-idempotent C correction commits; compare request-ID deduplication and transactional fencing. Add a hidden commit whose effect cannot be distinguished without a receipt.
- **Old-task retention check:** Execute an ordinary C continuation that reveals a double correction as well as a lost one, and score held-out A after resumption.

#### 06. Price the right to accept a future *set* of C versions (P)
- **Mechanism:** Reserve a menu of admissible queues against the third lane's actual capabilities rather than holding one slot for each hypothetical queue. Spend the reservation only for a compatible live batch at call-up, with no double booking across simultaneous demands.
- **Novelty vs nearest prior art:** [Reservation exchange][menu] and multiprocessor demand bounds already pack exclusive options. Test a capability-sensitive reservation whose shape distinguishes version requirements even at identical arrival/deadline profiles.
- **Cheapest first test:** Enumerate two arrival profiles, two version masks and one correlated fault. Compare scalar slack, per-version static reserves and exact contingent reservations at the same capacity.
- **Old-task retention check:** Execute C on every admitted profile while A runs normally, including the branch that exhausts the reservation and refuses the next B.

#### 07. Learn to isolate only the C state the backup must not share (P)
- **Mechanism:** Train an ordinary C representation with a tested separation between state dependencies shared with the standby's B finish and those needed by the third lane after reassignment; pay for redundancy only on the declared failure cut.
- **Novelty vs nearest prior art:** [Hot standby][hot-standby] replication and parent 04 already supply extra views. This asks for partial semantic redundancy that preserves versioned C service while removing a specific correlated B/C dependency, not merely placing copies on different routes.
- **Cheapest first test:** Train a four-feature masked linear model; remove the primary and one shared feature, then compare full replica, hand-isolated features and a learned mask. Include an indispensable shared feature.
- **Old-task retention check:** Test ordinary A, both C versions, and the third lane's own old task during the combined fault, not just under primary loss.

#### 08. Transfer by capability class, not by a forecasted request label (P)
- **Mechanism:** Group C requests by allowed state reads and effects; train one third-lane handler per declared class so a class-preserving queue transfer accepts held-out instances without opening new rights or dispatching from retired state.
- **Novelty vs nearest prior art:** [Queue groups][queue] already distribute work to interchangeable consumers; parent #245 freezes classes for B finishes. Here the claim depends on learned interoperability under version and effect constraints between previously non-interchangeable C workers.
- **Cheapest first test:** Hold out one request per class in a finite update system; compare generic handler, per-label adapters and version-aware queue routing. Include an out-of-class request with the same superficial label.
- **Old-task retention check:** Execute old C requests including the held-out members, test A plus third-lane normal writes, and count false acceptance as failure.

#### 09. Make the handback pay for its own version advance (P)
- **Mechanism:** Return C duty only when the recovering standby demonstrates it can serve all still-pending versions from its live state after normal legal updates; let the third lane continue serving until that boundary.
- **Novelty vs nearest prior art:** Make-before-break failback and parent 14 passable liabilities already cover successive transfers. The test is whether ordinary corrections can restore *historical version service*, not whether a refreshed current copy can answer today's C.
- **Cheapest first test:** Run two consecutive call-ups on a three-version toy queue, compare checkpoint catch-up, third-lane retention and ordinary-correction handback; include a pinned version no legal correction can recover.
- **Old-task retention check:** Run A and C through both ownership cuts, including arrivals during handback and a C request pinned to the oldest outstanding version.

#### 10. Find when the third lane is secretly a dedicated spare (I)
- **Mechanism:** Intervene on the third lane's routine writes while preserving occupancy and public routing. Attribute a benefit to working state only when those writes support eventual C acceptance and normal third-lane service.
- **Novelty vs nearest prior art:** Parent 10 makes the analogous intervention on the B standby; this is an attribution audit for the *receiving* lane rather than a coverage mechanism.
- **Cheapest first test:** Replace ordinary writes by sham writes on a tiny learner with fixed capacity; compare dedicated warm reserve, normal multitask sharing and equal-byte copy. Include a genuinely disjoint reserve that should fail the attribution test.
- **Old-task retention check:** Measure the receiver's ordinary old task as well as A and transferred C across sham, actual and no-call-up runs.

### Split a live signed obligation, not the retained state

#### 11. Compose two independently useful partial couplings (P, #256 seed)
- **Mechanism:** At retirement publish the allocation of signed remaining contributions and reserved slots between two working partners. Give each an ordinary action that supplies part of the liability, with past drift and all deadlines unchanged.
- **Novelty vs nearest prior art:** [Gradient projection][gpm] and [whole-trace pairing][finishes] already coordinate updates; the seed divides an existing, prefix-constrained debt across independently schedulable carriers.
- **Cheapest first test:** Exhaust S against single handoff, restart, joint projection, reservation swap and exact schedule search; remove an early slot so final cancellation is algebraically possible but not legally executable.
- **Old-task retention check:** Execute normal A/C at every observable prefix including intermediate writes, then run ordinary held-out tasks after both tails.

#### 12. Give each payer a contract on the other's observable prefixes (P)
- **Mechanism:** Publish paired assume-guarantee bands: each partner's next legal choice depends on a witnessed bound on the other's contribution so far, not on access to its state or every future local choice.
- **Novelty vs nearest prior art:** Assume-guarantee verification is established, and parent 17 preserves read order. The candidate interface lets both working policies adapt while retaining a composable *signed prefix* promise instead of freezing one trace.
- **Cheapest first test:** Enumerate two valid local policies per partner on a two-tick game. Compare fixed traces, independent worst-case envelopes and exact joint policy search; use a cyclic pair of assumptions with no executable first move.
- **Old-task retention check:** Play all admissible local branches and score ordinary A/C after each step and after a fallback, not just at joint completion.

#### 13. Teach truthful examples to supply complementary sign cones (P)
- **Mechanism:** During development train each partner so its ordinary local updates span a different useful set of signed reader contributions. Freeze those preparations and combine real held-out examples rather than writing corrective gradients into the slots.
- **Novelty vs nearest prior art:** [Gradient projection][gpm] changes an update to protect old readers; parent 20 shapes signed offers with C. This tests diversity across two useful policies, through the joint feasible debt set absent in either policy alone.
- **Cheapest first test:** Train two linear partners on equal C data and compare joint complementary training, independent training plus exact pairing, and projected joint updates. Hold out debts outside the summed cones.
- **Old-task retention check:** Score ordinary tasks on both partners before and after the split, including readers orthogonal to the trained sign directions.

#### 14. Trade the order of payments without trading their totals (P)
- **Mechanism:** Allow the split to exchange already reserved action order when one partner's early move temporarily opens the other reader's band; publish the admissible order as part of the allocation.
- **Novelty vs nearest prior art:** [Reservation exchange][menu] trades capacity and parent 17 transfers a read-order contract. The narrower candidate is a split whose individual payment profiles stay fixed while order alone creates a lawful between-write path.
- **Cheapest first test:** Enumerate all permutations in S, plus a variant where P creates new slack for Q rather than merely using a separate reader. Compare barrier projection and exact partial-order search.
- **Old-task retention check:** Place ordinary A/C reads between all non-atomic actions and after B; reject schedules that pass only at tick boundaries.

#### 15. Separate uncertainty about debt from uncertainty about who can pay (P)
- **Mechanism:** Carry a joint public set of debt and partner availability, with one causal split policy across indistinguishable histories. Learn a compact representation of which signs and access failures co-occur.
- **Novelty vs nearest prior art:** Parent 15 propagates hidden debt for one successor; belief-state planning subsumes the full problem. Test whether a factorization that preserves *debt/availability correlation* saves bytes without granting oracle dispatch.
- **Cheapest first test:** Enumerate four histories where the positive payer is absent exactly on one debt sign. Compare independent intervals, the factored representation and exact belief search; add a truly indistinguishable sign flip.
- **Old-task retention check:** Execute A/C over every history represented by each observable state, including histories that require refusing B.

#### 16. Preserve a two-payer option after one legal clock skip (P)
- **Mechanism:** Reserve alternative splits indexed by publicly observed local clock skips, carrying the exact accrued drift and reassigning only the unexecuted signed payments. Count idle old reads and never extend D.
- **Novelty vs nearest prior art:** Parent 16 relays debt across clocks, and exact contingent scheduling can cover skips. The object is a two-payer residual option that remains valid when the first split was partly executed.
- **Cheapest first test:** Enumerate a two-tick suffix with a single skip before or after the first payment. Compare fixed split, exact recourse, and full restart; include a skip after which no legal payment is early enough.
- **Old-task retention check:** Test ordinary A/C through idle and recovery ticks at their normal cadence and measure each partner's lost maintenance.

#### 17. Transfer the right to redirect a payment, not the money twice (P)
- **Mechanism:** Sell each pending signed contribution once: when a local obligation changes a partner's available action, redirect its unspent portion within pre-authorized bounds and prove that the sender can no longer claim it.
- **Novelty vs nearest prior art:** Escrow and [reservation exchange][menu] control double spending; parent 14 permits onward handoff. Here the single-spend object is a reader-, sign- and prefix-specific obligation, not a fungible resource quantity.
- **Cheapest first test:** Enumerate two simultaneous reallocations that each pass in isolation but use the same early negative payment. Compare scalar escrow, explicit locking and exact vector-prefix accounting.
- **Old-task retention check:** Score A/C after both attempted redirections and perform both partners' ordinary follow-up service after an allocation veto.

#### 18. Return a small witness when every candidate split fails (I)
- **Mechanism:** Extract a specific reader/prefix and occupied slot set sufficient to rule out the split, or report that only joint adaptive execution found the failure and no such local witness suffices.
- **Novelty vs nearest prior art:** Infeasibility certificates and parent 18 separating witnesses are established. This is an audit for reusable tiny obstructions in a multi-payer schedule, not a new feasibility method.
- **Cheapest first test:** Compare exact enumerated infeasibility, a linear certificate and reader-only witnesses on S with a missing slot and on an order cycle. Record certificate and verification size.
- **Old-task retention check:** Execute the fallback's ordinary A/C sequence and verify the cited prefix violation by actual reads on the rejected counterfactual.

### Make the two handovers earn their interaction

#### 19. Make one transferred C response also pay a signed installment (P)
- **Mechanism:** Train the third lane so answering a legitimate pending C correction via its ordinary update also provides one of the two required signed payments. The other partner pays the complement; charge validation and count the shared action once.
- **Novelty vs nearest prior art:** Parent 19 allows routine corrections to pay a tail; #256 02 transfers the queue. The testable interaction is that transferring *this particular outstanding request* creates an early payment on the receiving lane when even an independently optimized queue-plus-split stack exhausts capacity.
- **Cheapest first test:** In S let Q's only early slot serve an original C deadline, with one truthful update that can also provide Q's vector on a trained host. Compare exact scheduling on separately and jointly trained hosts with identical legal actions, plus wrong-version and wrong-sign cases.
- **Old-task retention check:** Execute transferred C on time and at the required version, Q's regular old workload, and A/C at all intermediate payment reads; include refusal on the wrong sign.

#### 20. Choose a queue cut by the signed payments its writes enable (P)
- **Mechanism:** When more than one pre-authorized cut is within the B deadline, choose one by its public joint queue/remaining-tail offer, with the queue atomic at the chosen cut and no deadline resets.
- **Novelty vs nearest prior art:** Joint contingent scheduling subsumes cut selection. The candidate is a reusable cut offer that summarizes jointly reachable legal versioned service and signed payments without inspecting a retired state.
- **Cheapest first test:** Exhaust two cut times, two public queues and two debts where changing the cut flips the usable payment sign. Compare independent cut-then-split, exact coupled search and a precomputed offer; measure cost against exact search on the same host.
- **Old-task retention check:** Score A/C before and between the possible cuts, and deliver pending and new C by their original deadlines after the chosen cut.

#### 21. Renew the joint reserve with work already owed after the cut (P)
- **Mechanism:** Train the first two ordinary C corrections after a handover to restore complementary offers for a second retirement while finishing the transferred queue. Declare the correction arrival bound before admission; reserve a safe fallback when it is violated.
- **Novelty vs nearest prior art:** Parent 03 renews B readiness and parent 14 preserves passable liabilities. This asks whether accepted old work restores a *joint split* of the required signs without consuming a second copy of scarce C capacity.
- **Cheapest first test:** Run two retirements over a two-lane linear learner; compare joint and separate training with equal correction examples, exact recourse and a no-arrival negative. Count renewal steps and any delayed C.
- **Old-task retention check:** Run ordinary reads between both retirements and after both tails, including unseen C corrections and the no-arrival fallback.

#### 22. Audit the crossover from genuine joint service to spare-capacity accounting (I)
- **Mechanism:** Cross queue transfer and split-tail support with shared slots, disjoint slots and correlated lane loss. Reconcile a per-lane occupancy trace with every claimed dual-use action.
- **Novelty vs nearest prior art:** Parent 22 maps the working-standby frontier. This is an interaction falsifier: if a stack with the same actions and training fits all deadlines, report only measured validation savings, or a tie.
- **Cheapest first test:** Enumerate Q/S combinations with disjoint workloads as a tie control and one shared bottleneck. Try exact joint scheduling for both training regimes and compare at matched retention and service.
- **Old-task retention check:** Report per-reader worst prefixes, per-version C deadline completion, and held-out A/C after the tail, on no-fault, call-up, shared-fault and refused windows.

## Ranked deeper questions

1. **Can one truthful old-task action both serve the transferred queue and make a necessary signed payment?** Start with 19 and 22. Test joint versus independent training and give both exact search and identical rights. The key case is two individually necessary payments with one early slot already owed to C. If the best independent stack delivers the same A/B/C at the same budget, drop the feasibility claim.
2. **What is the smallest lawful state for third-lane acceptance across versions and cuts?** Start with 01–05 and 09. Compare bytes and acceptance time at identical service against an authorized version-aware queue plus migration. Use an in-flight commit and two histories that agree on current C yet disagree on a pending pinned version. If the reserve needs the whole old checkpoint, report that cost.
3. **What remains composable when the payments are real adaptive updates?** Start with 11–16. Move from fixed rational traces to a two-coordinate Adam suffix with real gradients, hidden drift and a legal skipped tick. Seek a public contract that avoids repeated joint validation; give exact contingent search the same information. If independent envelopes certify the wrong action order or joint real suffix, restrict the claim to the linear host.
4. **When do repeated call-ups destroy their own reserve?** Start with 07, 17 and 21. Hold out a shared failure and a late or absent correction across two windows; count all defaults, old tasks delivered and capacity already promised. If coverage renews only with extra retained state or delayed C, report a single-window result and its actual cost.

[parent]: https://github.com/manojbajaj95/cl/pull/256
[triage]: https://github.com/manojbajaj95/cl/blob/19d7c04c30b54a1e4b0a5d462822d8b3e2bec514/reviews/flood-triage.md#L371
[ledger]: https://github.com/manojbajaj95/cl/blob/19d7c04c30b54a1e4b0a5d462822d8b3e2bec514/reviews/idea-ledger.md
[menu]: https://github.com/manojbajaj95/cl/pull/235
[finishes]: https://github.com/manojbajaj95/cl/pull/245
[queue]: https://docs.nats.io/nats-concepts/jetstream/consumers
[mc]: https://doi.org/10.1109/REAL.2007.47
[hot-standby]: https://www.postgresql.org/docs/current/hot-standby.html
[gpm]: https://arxiv.org/abs/2103.09762
[grab]: https://arxiv.org/abs/2205.10733
