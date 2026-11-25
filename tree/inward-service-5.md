# Inward service V: certify which exercise orders and groups survive actual learning

**Status:** Ideas and exact paper checks only; no learner or GPU runs. **Parent:** [Inward service IV](inward-service-4.md) ([PR #301][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, PR #301 row][triage] gives score 3 to **#301#14**, an exercise that invalidates a *different*, unspent old payment in one order but not the reverse, and **#301#15**, a shortage that rules out a triple although every single right and pair is feasible. The proposed work is to make the corresponding witnesses reusable across real writes, not to rediscover stateful scheduling or Hall's theorem.

## Contract and controls

- Freeze the arrival tape, old jobs, legal examples, original deadlines, evaluation seams and complete ordinary/alternate read contracts. A payment is a real due A/C update; spend it once at execution even if B later refuses. A right is an option, not capacity reserved or work already done. An exercise uses a truthful, then-available record from its own B queue, revalidates against live learner and serving state, and must deliver useful new-task gain. No-show adds neither a B update nor a slot. Never waive the currently nonblocking read.
- **Compare the same information.** Use #299#13's shared plan, pairwise planning, static locks, first-come, full paired reads or [GEM][gem], incremental exact matching, and causal stateful scheduling that simulates both exercise orders. Also stack the best controls at matched records, evaluations, latency, precision, bytes and compute. Exact checks on the same observations are the decision reference; an advantage over them could be fewer repeated checks or less state, not more correct decisions at unbounded budget. Charge the certificates' build, validation and eviction costs. Compare accumulation on traces with the *same exposed seams* ([ledger's bounded-delay null][ledger]); endpoint order dependence alone does not count.
- **Keep `impossible`, `proved feasible`, and `unknown` distinct.** A Hall cut is a negative result only when its neighborhood includes every eligible edge over the claimed continuation scope. A matching in that overapproximation does not prove an executable schedule. Re-audit unsupported scopes, report safe refusal separately from qualified completion, and retain an ordinary old-work fallback that fits the original deadlines. Hold out ordinary A/C inputs in both modes and prior B from every queue, including the losing one. Report worst exposed prefix, each original deadline and post-suffix results, not just end averages.

## Two exact paper checks

**O — Lose eligibility, not the unspent record.** Use the parent's half-step SGD on masked half-squared loss: an active coordinate with target `a` moves to `(w+a)/2`. Initially `x=y=1`, each old-job score and each new B score is zero. The two old read floors are `x,y≥0`; both previous B scores are on independent, unchanged coordinates. Two old jobs are due one per slot, each paid by setting its own score to `1` with target `2`. `S,T,U` are distinct, single-use records offering the same labeled job progress on the currently due job (the masks and targets for both jobs are fixed in advance). `S` and `U` can pay at any `x,y≥0`; `T` can pay only at pre-update `x≥3/4`, a stricter landing requirement than the ordinary floor. No payment updates `x,y`. Both B partners are available before slot one and expire after slot two. P requires just-executed S; its real update targets `x=0,p=2`. Q requires just-executed T; its update targets only `q=2`. Each exercise immediately follows its payment. Each personal new B score goes from `0` to `1`, reducing that component's loss from `2` to `1/2`.

`S→P` gives `x=1/2`. T is still unspent but cannot pay slot two; U pays it, and Q does not exercise. `T→Q→S→P` pays both jobs and exercises both rights, since Q leaves x at `1` until after T. All ordinary reads stay at or above zero, each job score stays at `1` once paid, and neither prior B score changes. A no-show of P leaves x at `1`, so `S→T→Q` is legal. To get a two-way negative control, let Q also target `y=0` and require S to have `y≥3/4`; now `T→Q` blocks S too, and U still pays the second job in either order. A static record lock sees no S/T contention in any arm. Exact stateful scheduling sees both failures; the question is whether a smaller proof of the lost payment survives intervening writes.

**H — Reuse a triple cut, then break its premise.** Extend the same masked payment setup to three jobs, one per slot, and three rights P/Q/R, all known before slot one and expiring after slot three. A payment can fund at most one immediate exercise. S and T can each fund any of the three; U can pay ordinary old work but can fund only R, and only at live `x≥3/4`. In this check x starts at `1/2`; there is no O-style eligibility threshold for T. Ordinary read floors remain `x,y≥0`. In the shortage arm payments and Q/R leave x alone, and P targets `x=0` as well as its own score. Q/R also target `2` on their respective new scores. All singles and all pairs are feasible via S/T; U can still pay the remaining job. For the triple, the union of possible funding records is `{S,T}`, too small by one. After, for example, `S→Q`, the residual cut for P/R has only `{T}`. The premise `x≤1/2` is preserved by every allowed transition in this arm, including P (`1/2→1/4`), so neither remaining exercise can create a new U edge.

In the matched old-progress arm, S also has a truthful target `x=3/2`, making x `1` when S pays first. The cached cut must be invalidated; `S→Q→U→R→T→P` completes the triple, with x following `1/2→1→1→1→1→1→1/2`. `S→Q→T→P→U` still pays all old jobs but cannot exercise R: P brings x back to `1/2` before U. All ordinary floors and prior B hold on both traces. This shows why a cut needs a live-state premise and why deleting it isn't an admission rule. Neither fixture establishes that its thresholds, exercise effects or timely arrivals occur naturally.

## Idea cards

**P** = candidate primitive; **I** = improvement or audit. Nearest-art contrasts are hypotheses, not novelty clearances.

### Carry directed conflicts across real updates (#301#14)

#### 01. Carry a refusal for one payment, not a lock on a right — P
- **Mechanism.** Record the exercise prefix, lost payer edge and sufficient invariant for its continued failure. Carry the refusal over unrelated writes without withdrawing other routes to the affected right.
- **Novelty / control.** #301#14 names the ordered conflict; semantic concurrency control already uses state predicates. Test edge-scoped reuse against fresh execution of both orders and a static right-level lock.
- **Cheapest first test.** Insert an x-preserving tick after P in O, then swap it for a tick that moves x back to `3/4`. Only the first tick should permit reuse of the refusal.
- **Old-task retention.** Run both old modes after each tick, require the second old job on time via T or U, and check the deferred Q queue's prior B.

#### 02. Bound the pre-exercise states on which the reverse order works — P
- **Mechanism.** Store a sufficient domain for a complete reverse path, including intermediate payer eligibility, rather than a Boolean saying to reverse a pair. Intersect it with all still-owed reads on the current trace.
- **Novelty / control.** Weakest-precondition analysis already computes such domains. Test reuse over several due old updates against cached schedules plus live checks and exact recomputation, not against control that assumes all reversals work.
- **Cheapest first test.** In O let Q change y and make S require `y≥3/4`. Start y at `1` or `3/2`, holding x fixed; with Q targeting y=0 only the latter reverse reaches the S floor.
- **Old-task retention.** Test ordinary y and x separately after Q and P, each old job at its deadline, and the prior B scores when the reverse is refused.

#### 03. Shorten a conflict's lifetime with an ordinary bridge — P
- **Mechanism.** Let a distinct, already-due old record end an ordered refusal if its actual update restores eligibility before the threatened payer is due. Represent where in the deadline schedule the bridge is mandatory, not just that a repair exists.
- **Novelty / control.** Inward service I recovers a single drifted right; #301#18 requires a second ordinary read. Here one exercise creates the refusal and a third paid action ends it before the original payer, compared with full stateful rescheduling and fixed standby.
- **Cheapest first test.** Add one independently due middle job to O. Give its two truthful records identical job progress but only one moves x from `1/2` to `3/4`; then move that record one slot after T's expiry.
- **Old-task retention.** Pay all three jobs in either branch, test both reads before and after the bridge, then recheck old P and Q tasks after the final exercise or fallback.

#### 04. Carry an interval of possible first exercises through one refusal — P
- **Mechanism.** Bind a payer to its stricter landing read and prove every allowed P update within a declared family crosses it. A new P example in the family reuses the refusal; an example outside gives no such conclusion.
- **Novelty / control.** Robust reachability already propagates sets. Test reuse of an *impossibility* across changing truthful B records against per-example simulation and worst-case locks that never reopen.
- **Cheapest first test.** In O vary P's x target over `[0,1/4]`; the largest landing is `5/8`. Add a truthful x target `1/2`, landing exactly at `3/4`, which invalidates that family claim.
- **Old-task retention.** Compare both old modes and Q's original deadline at interval endpoints and the boundary example; measure each prior B under the selected actual, not worst-case, write.

#### 05. Distinguish equal weights with different future payer eligibility — P
- **Mechanism.** Refuse to join ordered witnesses across equal weights when optimizer state can put their next due payment on opposite sides of a threshold. Retain a bound only on the carry that can affect the edge before expiry.
- **Novelty / control.** Guarded optimizer-state compression already cares about future displacement. The test is scoped reuse for a distinct future payer versus full optimizer-state hashing and fresh rollout.
- **Cheapest first test.** At x=`3/4` use two opposite momentum carries and one declared zero-gradient tick before T. Include a reset arm only as a comparator priced for its changed trajectory.
- **Old-task retention.** Check x and the alternate mode after the tick and later payments; run old A/C and prior B on both hidden-state traces even if one refuses Q.

#### 06. Overturn only the edge touched by a routed example — P
- **Mechanism.** Attach a directed conflict to the actual activated path of the threatened payment's held-out slice, with a guard on routing. After P, recheck only edges whose paths or guard may change.
- **Novelty / control.** #301#03 invalidates a mode handoff when routing changes; dynamic dependence tracking already invalidates reads. The proposed use is across eligibility edges for distinct payments, against a full reroute-and-schedule pass at matched latency.
- **Cheapest first test.** Give T and a spare payer disjoint activated paths, then put a held-out T input at a routing boundary crossed by P. Compare with a default route that matches T only on training examples.
- **Old-task retention.** Replay each full old mode through the actual router, especially inputs changing route, and probe prior B after the spare payment.

#### 07. Retire a directed witness at the first unverified clock tick — P
- **Mechanism.** Carry a one-direction refusal through known intervening events only. A watermark on consumed events and observed ticks bounds where the proof is reusable; an unobserved tick makes the edge unknown rather than impossible.
- **Novelty / control.** #301#11 splits payment freshness from exercise freshness; temporal monitors already track versions. Test a per-edge, event-scoped refusal against expiring every witness at every tick and keeping it through the entire service window.
- **Cheapest first test.** Hide one idle tick, equally often x-preserving or restoring in O; later reveal which occurred. Measure whether scoped expiry saves checks on the fully observed tape without discarding the just-restored T.
- **Old-task retention.** In both hidden-tick outcomes audit ordinary x/y at the next serving seam, late Q's prior B and the on-time U fallback.

#### 08. Learn an alternative exercise that keeps a distinct payment lawful — I
- **Mechanism.** Where the current queue offers two truthful, equal-gain B updates, prefer the one whose exact executed response preserves a known payer edge for the other right. Refuse to trade off the first queue's gain to keep the edge.
- **Novelty / control.** GEM and constrained update selection already use such inequalities. The question is whether guarding a *future old update's* eligibility adds anything over GEM on both current reads plus planning each candidate exactly.
- **Cheapest first test.** In O give P two feasible records targeting the same p but x targets `0` and `1/2`. Compare with choosing the least weight movement in a version where an irrelevant coordinate dominates the norm.
- **Old-task retention.** Match p gain, check both old modes after P, pay both original jobs and verify the earlier B skills after Q as well.

#### 09. Identify when no directed edge survives equal-budget accumulation — I
- **Mechanism.** Enumerate legal interleavings, then try accumulating the same gradients only where no old or B serving seam is crossed. Separate optimizer-order effects from genuine loss of payment eligibility at a live boundary.
- **Novelty / control.** This audits the ledger's bounded-delay null, not a new scheduler. Compare with exact scheduling and the strongest feasible accumulated arm, rather than charging the control for an artificial delay.
- **Cheapest first test.** Compare O with an otherwise identical tape on which no mid-block read or exercise is owed and a combined update is legal. Report which lost edges still affect actual completions.
- **Old-task retention.** Keep all real deadline evaluations in both tapes and check old A/C and prior B on the same held-out inputs after accumulation.

### Specialize group shortages without paying twice (#301#15)

#### 10. Carry a Hall cut with a checked state premise — P
- **Mechanism.** Store a group, its upper-bound funding neighborhood and the learner-state guard that excludes every omitted edge through the declared horizon. When a right outside the group spends a neighboring record, remove that record but keep the excluded-edge proof only if its guard survives.
- **Novelty / control.** Hall and incremental matching already update neighborhoods. Test retaining an actual learner-state proof across a spend against exact adversarial-prefix validation of fresh graphs and matching on live edges alone.
- **Cheapest first test.** Use H and an extra pending right sharing S; pay slot one with S for that outside right. Contrast x-preserving exercise with one that opens U; the latter invalidates the old cut even if the new schedule still lacks slots.
- **Old-task retention.** Keep all due jobs on time in both cases, check x/y after the outside exercise and every queue's prior B after any resulting refusal.

#### 11. Contract a cut only after the matched spend actually executes — P
- **Mechanism.** Specialize the witness by actual immutable receipts: remove a paid record, and remove a right from the pending set only on successful exercise or declared expiry. Keep the correct residual group if exercise fails after service.
- **Novelty / control.** #301#11 separates the receipt from the exercise, and residual bipartite matching is standard. Test their combination for group refusals versus recording only successful exercise and full replanning from the log.
- **Cheapest first test.** In H let S pay and Q fail live validation but stay pending. With two slots left, compare the cut over P/R when Q succeeds and the cut over P/Q/R when Q fails; never restore S.
- **Old-task retention.** Verify the already-paid old job through the refusal, meet the remaining jobs with T/U, and measure previously learned Q behavior whether or not it exercises.

#### 12. Keep separate cuts for different payment horizons — P
- **Mechanism.** Lift a payer to the slots it can meet, while keeping a capacity-one link to its real record. Index reusable cuts by earliest affected deadlines, so a late edge cannot invalidate a shortage covering earlier rights.
- **Novelty / control.** Time-expanded flow handles deadlines. Test reusable exclusion guards when learner updates move an edge between slots, against exact time-expanded matching and a pooled cut that ignores time.
- **Cheapest first test.** Give P and R slot-two deadlines, Q a slot-three deadline, and make U enter only in slot three. Require a feasible no-shortage twin with two timely payers for P/R and a hidden-shortage twin with only one.
- **Old-task retention.** Check all three old jobs at their actual deadlines plus live x/y and prior B after the late payment; none can use U retroactively.

#### 13. Preserve a witness by moving its boundary, not rechecking all rights — P
- **Mechanism.** When one guard change adds an edge to a deficient neighborhood, try moving to a smaller subgroup whose omitted-edge guards still hold. If no checked smaller cut works, rebuild or return unknown.
- **Novelty / control.** Incremental flow repairs cuts already. Test learner-dependent proof reuse when only some of the newly viable rights can use the new edge, versus exact incremental flow with fresh edges and a coarse global invalidation.
- **Cheapest first test.** Use four rights with upper-bound payers `{S,T}`; open U only for the fourth. The four-right deficit shrinks, but the untouched triple still has a shortage. Open U to the triple in a second arm and require its stale cut to disappear.
- **Old-task retention.** Keep the four original old deadlines and both read modes in both arms; verify old B for the group dropped from consideration as well as the winners.

#### 14. Share one proof of a missing edge across several cuts — P
- **Mechanism.** Index excluded edges by the finite-horizon read bound that actually proves them absent, so two overlapping groups can consume the same checked lemma while retaining their separate capacities and receipts.
- **Novelty / control.** Constraint solvers already share lemmas. Test whether one due-input read bounds multiple future eligibility predicates more cheaply than deduplicated exact evaluation plus incremental Hall checking.
- **Cheapest first test.** Construct two overlapping triples lacking U for the same x-bound reason, then revise one edge to depend on y instead. Perturb y without altering x and invalidate only the affected cut.
- **Old-task retention.** Evaluate both modes independently; complete old-only jobs for every refused group and test prior B of the rights shared by both groups.

#### 15. Track one robustness unit of missing capacity — P
- **Mechanism.** Record the cut's deficit and an upper bound on the number of *new distinct records* a declared future write can add. Carry the negative result while the deficit remains positive, even if some specific exclusions no longer hold.
- **Novelty / control.** Capacity sensitivity is standard in flows. Test a learner-response bound at record granularity against recomputing each changed edge and a Boolean cache that discards the whole cut on any change.
- **Cheapest first test.** With four rights and two known payers, release one previously excluded payer for two rights; the deficit can fall by at most one. Add another independently available record in a twin that can realize all four payments.
- **Old-task retention.** Compare identical ordinary coverage progress before the release, audit both modes after it, and check prior B after the feasible twin's additional exercises.

#### 16. Hand a cut through an equivalent record substitution — P
- **Mechanism.** Allow a newly arrived alternative to replace an expiring payer in a cut only with a checked substitution for availability, capacity and response. Never give the original and substitute a shared capacity unless the old job slot or actual eligibility enforces it.
- **Novelty / control.** Scheduling with interchangeable resources and #292's replacement payers are nearest. Test a substitution scoped to a group and a learner region against fresh matching and identifying records by batch label alone.
- **Cheapest first test.** Replace T at its expiry with T′ having the same legal landings on H; then delay T's expiry so both can contribute. The second arm cannot reuse a capacity-one proof without another constraint.
- **Old-task retention.** Match original due jobs, compare held-out A/C effects of T and T′, and check prior B after using each record on its actual trace.

#### 17. Use refusal samples to choose what to check, not to infer absence — P
- **Mechanism.** When several unverified edges could break a cached cut, pick a mandatory old observation that resolves the most still-relevant guards. Retain no negative conclusion about edges beyond what the check or a sound bound covers.
- **Novelty / control.** Active diagnosis selects informative observations; exact Hall checks already localize shortages. Test using the residual cut to target a *due* check against random due observation and exact incremental matching with the same reports.
- **Cheapest first test.** Let two old records with equal owed progress report x or y. Make only x decide whether U can fund R; include a twin where both reads are needed so a single check leaves the answer unknown.
- **Old-task retention.** Check the unqueried mode at its unchanged deadline, and all old jobs and prior B on both the admit and defer branches.

#### 18. Publish exclusions for menus the scheduler can actually face — P
- **Mechanism.** Keep small minimal deficient groups that can co-occur before expiry. Causal menu narrowing may retire a group on no-show without claiming its unseen member was infeasible or resurrecting a spent payer.
- **Novelty / control.** Minimal conflicts and #301#09's contingent disjunction are nearest. Test the usefulness of bounded group exclusions versus pairwise plans, an exact menu-indexed planner and a size-unaware lock policy.
- **Cheapest first test.** In H reveal R's independent no-show before versus after the first payment; compare an exact pair continuation with retaining the obsolete triple prohibition. Include the triple-feasible arm from H.
- **Old-task retention.** Pay the third job even on R's no-show, and test R's prior B along with both modes and the exercising queues' prior B.

### Check whether the two mechanisms need each other

#### 19. Use a directed conflict to explain which permutation restores a group — P
- **Mechanism.** Branch only on an observed write that can make a cut premise false; once the cut opens, check the ordering inequalities for actual use of the new payer. Keep the proof conditional until that write executes.
- **Novelty / control.** Stateful resource scheduling can simulate both steps. The reusable object links a missing-edge guard to a causal order where its edge is exposed and then lost, against incremental Hall checking plus exact order validation.
- **Cheapest first test.** Use H's S-opened U window: compare U-before-P and P-before-U, which have the same three records and matched old job progress. Remove P's x effect as a tie control.
- **Old-task retention.** Check x/y at each prefix of both permutations, the same three deadlines and preserved B from Q and P when R finally exercises or is refused.

#### 20. Detect a group deadlock that a static matching and every pair miss — P
- **Mechanism.** Build a small precedence-cycle witness for a candidate group from *necessary* exercise-before-harmful-write constraints. Use it to refute the group only if alternative payers and legal reset or repair paths are ruled out for that horizon.
- **Novelty / control.** Disjunctive scheduling and wait-for graphs already detect cycles. Test a reusable cycle whose arcs depend on actual learner responses versus full stateful causal search, not just static Hall.
- **Cheapest first test.** Give each of three rights one distinct payer; exercising P blocks R's payer, R blocks Q's, and Q blocks P's. Use disjoint half-step coordinates from O. Every pair has one order, but all three require a cycle; neutralize one response and recover an order.
- **Old-task retention.** Use ordinary-only alternatives to pay all jobs on refusal, and hold both old-read floors and all prior B through the recovered three-right trace.

#### 21. Split group failure into “too few payments” and “no common safe order” — P
- **Mechanism.** Return either a capacity-deficit witness or a witness ruling out each remaining funded ordering under its own live preconditions. Scope a suggested next check to whichever of those proofs it can change.
- **Novelty / control.** #301#20 distinguishes shortages from reads, and exact planners explain infeasibility. Test reuse of different proof types across subsequent actual writes versus a fresh solver explanation or a capacity-only retry policy.
- **Cheapest first test.** Compare H's shortage with 20's cycle, then separately supply a spare payer or neutralize a harmful response. Verify that fixing a capacity premise alone doesn't clear the order obstruction when the spare has the same threatened read.
- **Old-task retention.** Keep a real old-only fallback in every variant, check affected reads by original deadlines and measure all prior B after the chosen retry.

#### 22. Test whether reuse survives unengineered due records — I
- **Mechanism.** Freeze a small family of A/C and B teachers and due queues before enumerating tapes; fit no cut thresholds or arrival menus after observing successes. Record reachable directed losses, real triple shortages and the fraction of stale guards after each exercise.
- **Novelty / control.** This is a falsifier. Compare the best same-budget stack of #299#13, live paired reads, incremental Hall checks and causal schedule search with the two scoped proof types. Add symmetric conflicts and a no-shortage triple; a tie is not evidence for a new primitive.
- **Cheapest first test.** Enumerate short rational linear-regression streams with and without momentum and independently delayed B arrivals. Start with exact decisions as labels; count net checks/bytes, unsafe admits, and useful on-time completions under a fixed check budget.
- **Old-task retention.** Apply the same frozen held-out A/C and prior-B panels on all prefixes, deadlines and no-show/refusal traces; include streams with zero new completions in the retention report.

## Ranked deeper questions

1. **Can a cut survive a real exercise, yet be invalidated exactly when another due record opens a usable payment before the next harmful exercise?** Start with 10, 11, 19 and 22. Look for sound reuse on same-tape branches with old work paid before the unchanged deadlines. Require less end-to-end validation work at matched useful B gain than incremental matching plus exact order checks, or no joint primitive claim.
2. **Which part of a one-way conflict is stable enough to carry across live learner state?** Start with 01, 02, 05, 07 and 09. Vary idle ticks, optimizer carry, arrival seams and both-order failure. If the projection keeps nearly the full state or its guards demand full re-execution, prefer fresh exact scheduling.
3. **Can higher-order refusals stay small without confusing capacity with order?** Start with 12–15 and 20–21. Include pair-feasible triples with and without a full matching, and an executable triple. Track cost as degree, deadlines and the number of overlapping groups rise; reject any proof that grants a triple from matching alone.
4. **How often can an already-due old record or observation preserve a useful continuation without tilting coverage toward easy old inputs?** Start with 03, 16–18 and 22. Fix the workload and the same deadlines before deciding which record to use. Require the hardest old slices and the deferred queues' prior B to pass, not just more B rights exercised.

**Verdict:** The two checks separate payment identity from eligibility and pairwise feasibility from group feasibility. They do not separate a reusable certificate from a well-implemented exact control on natural tapes. The next gate is cheaper *sound* reuse across actual exercises and expiries, with both old read modes and prior B still served.

[parent]: https://github.com/manojbajaj95/cl/pull/301
[triage]: https://github.com/manojbajaj95/cl/blob/6fcc8307eb423657bdaa7251ff906e2fedfbac75/reviews/flood-triage.md#L418-L421
[ledger]: https://github.com/manojbajaj95/cl/blob/6fcc8307eb423657bdaa7251ff906e2fedfbac75/reviews/idea-ledger.md
[gem]: https://proceedings.neurips.cc/paper/2017/hash/f87522788a2be2d171666752f97ddebb-Abstract.html
