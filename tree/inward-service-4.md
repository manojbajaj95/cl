# Inward service IV: keep both reads owed and spend each old record once

**Status:** Ideas and exact paper checks only; no learner or GPU runs. **Parent:** [Inward service III](inward-service-3.md) ([PR #299][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, PR #299 row][triage] gives score 3 to **#299#04**, handing off a suffix blocker between two separately specified reads of one old routine without dropping either obligation, and **#299#13**, giving competing pending rights a single old-service budget, spent when service executes and checked again at exercise.

## Contract and controls

- **A read can stop blocking without ceasing to be owed.** Fix the routine's ordinary and alternate input contracts, held-out populations, floors and deadlines before looking at B. Keep both ordinary-execution checks and apply both declared read contracts to each claimed suffix. A changed blocker isn't a waived floor, an average over the two modes, or evidence that the other mode will stay safe. Use an actual due A/C record and a genuinely later truthful own-queue B record; on no-show, the opposite queue contributes nothing. Match sorted suffix gaps when isolating blocker identity, and require useful B learning without losing the opener's gain. Compare with #292#12 handoff between named readers, unrelated full read checks, active-set tracking, [GEM][gem] on both reads, and fresh exact checking. Include a routine whose modes cannot be separated by any legal action.
- **A pending right is conditional, not a reservation or permission to execute.** A common plan accounts for the old jobs in every reachable trace, including refusal and no-show. It need not support both rights on the same trace; only advertise a joint continuation when there is a disjoint executable payment plan. Use the same frozen arrivals, eligibility, indivisible batches, old jobs and clocks in every arm. Consume a record once at actual service, not at a preview or a later exercise; a refusal does not refund it. Revalidate the winning right on live learner and serving state at exercise, defer the other unless a disjoint continuation is feasible, and never revive expired rights. Compare with #292#02 per-right alternating-path witnesses, locks, first-come, [escrow][escrow], and exact causal joint scheduling. Include a pool with two individually viable rights but no disjoint continuation.
- **The bar is above ordinary scheduling.** Compare mixed cards with the strongest equal-budget stack of both sets of controls and the [smooth/accumulation null][smooth]. Match useful gain per B queue, old work, coverage and latency, observations, checks, precision and peak bytes, or report the tradeoff. Count unsafe admits, safe suffixes completed on time, and refusals and delays separately. Check worst held-out A/C slices at exposed prefixes, by their original deadlines, and after each claimed suffix; check previously learned B in both exercise and no-show traces. Full-state exact planning on the *same information* is a small-instance reference, not something a certificate can beat on decision quality. A primitive candidate needs a useful reusable operation, not just a different order or a relabeled lock.

## Two paper checks

**R1 — Same two reads, opposite blockers.** Use the parent's [B1][parent-file] half-step SGD with half-squared loss; the old routine has tagged inputs with read scores `x` (N) and `y` (X). On ordinary execution both floors are zero; the candidate suffix subtracts `1/2` from both scores. Start at `(1,0,0)` in `(x,y,z)`; the due old job requires the separate score `z≥1`. Truthful due record `S` targets `(−1,2,2)`, yielding `(0,1,1)`; `T` targets only `z=2`, yielding `(1,0,1)`. Both pay the job and leave sorted suffix gaps `(−1/2,1/2)`. Only `S` transfers the blocker from X to N. The later own-queue record `D` targets only `x=2`. After `S→D` the suffix gaps are `(1/2,1/2)` and D's loss falls from `2` to `1/2`; `T→D` and D alone leave X at `−1/2` under the suffix. Both modes remain owed; a suffix subtracting an extra `3/4` from X would still fail X after `S→D`. Unshifted N and X pass at all executed prefixes, and an independent opener coordinate is unchanged. If N and X are forced to be the same read, an identity-only handoff is impossible. This separates a named handoff from pooling, not from an exact check on both modes.

**R2 — One spend, even when the winner fails revalidation.** Enumerate two successive service slots, each followed by one exercise opportunity. Two mandatory old jobs are due one per slot; each can be paid by any unused record from `{S,T,U}`. In this abstract landing table, a timely P can open just after S, a timely Q just after S or T, and U serves old work but opens neither. Thus `P:S→Q:T` and `Q:T→P:S` are both possible, but `Q:S→P` is not. Delete T: both rights still have individual witnesses, but only one can be exercised and U can pay the other job. In a separate T-present branch, after S actually pays the first job, let a predeclared intervening clock tick invalidate P's landing. P refuses, S stays spent, and only Q via T can still complete; U remains a legal old-only fallback. The table treats each legal payment as retaining the held-out old floors and each admitted suffix as retaining prior B; it checks accounting and observation order, not that a real learner produces these landings or retains those floors.

## Idea cards

**P** = candidate primitive: a reusable operation or certificate. **I** = improvement or audit. Nearest-art contrasts are hypotheses, not novelty clearances.

### Keep the paired read contract (#299#04)

#### 01. Bind two read modes to one immutable obligation — P
- **Mechanism.** Give a routine one obligation ID, two versioned read contracts, and a suffix-specific blocker witness. Moving the blocker changes the witness, not the two held-out checks the obligation owes.
- **Novelty / control.** #292#12 names the blocking readers; an active-set tracker already names tight inequalities. Test whether a single reusable obligation witness saves work across suffixes versus unrelated full read checks or GEM on both reads, without the false admits of pooling by task ID.
- **Cheapest first test.** Enumerate R1, the extra X debit, and the tied-read negative. Hold the ordinary-input contract fixed while varying suffix exposure; count necessary fresh checks.
- **Old-task retention.** Run the routine separately on both held-out input families before preparation, after D and after each admitted suffix, and score the due C job at its deadline.

#### 02. Transfer a check only through a paired-input witness — P
- **Mechanism.** Where both modes share an input domain, certify a bound from their paired outputs only on that overlap. Reuse a fresh N check to bound X there; check X directly on its unmatched inputs or when the bound is inconclusive.
- **Novelty / control.** Relational verification already compares executions. The proposed witness transfers part of a retention check across a blocker change without treating the two retention obligations as interchangeable; compare with checking both and with an unconditional cached bound.
- **Cheapest first test.** Use two overlapping input grids with a shared slope and one X-only edge case. Perturb the X response on the overlap to require invalidation.
- **Old-task retention.** Evaluate both complete held-out populations, including the unmatched edge, after old service, D and the suffix; measure the worst input, not pairwise agreement alone.

#### 03. Revoke the handoff when ordinary routing changes — P
- **Mechanism.** Bind the blocker certificate to the deployed map from actual inputs to read modes. If ordinary service changes that map, keep both obligations and invalidate only suffix proofs whose exposed input population changed.
- **Novelty / control.** Incremental verification invalidates dependencies; #299#04 has a fixed split. Test whether read-routing dependencies permit scoped rechecks compared with fresh two-mode execution and tracking reader IDs without routing.
- **Cheapest first test.** Use a threshold router and one due update that moves a held-out boundary input into the newly binding mode; compare with a same-margin update that moves no input.
- **Old-task retention.** Replay ordinary held-out inputs through the *live* router after each transition and under the suffix, including inputs that changed route.

#### 04. Compose suffixes using the debit of the read that stopped blocking — P
- **Mechanism.** After the N-to-X blocker handoff, carry a lower bound for N indexed by the suffix prefix. Charge successive N debits against that bound before admitting the concatenation, rather than certifying each suffix in isolation.
- **Novelty / control.** Sequential contracts already compose bounds; #299#04 explains a single handoff. Test reuse of a two-mode bound where either suffix is safe but their composition is not, versus fresh exact composition and a single global slack bound.
- **Cheapest first test.** From a post-settlement gap of `1/2` on each read, use two suffix segments that each debit N by `3/8`, then replace one debit with X's. Restrict the paper test to additive fixed debits before trying live optimizer effects.
- **Old-task retention.** Check ordinary N and X between segments and both mode floors at each suffix prefix; verify the completed old job and prior B still pass.

#### 05. Permit a split on one suffix family, not on every suffix — P
- **Mechanism.** Attach a scope to a handoff proof: two modes admit a separable response bound for one family of suffixes, while another family's cross-mode interaction requires the full paired check.
- **Novelty / control.** #299#07 covers a suffix menu; assume–guarantee proofs restrict where abstractions apply. Test a reusable *response-separation* scope against separate proofs per suffix and a global split that overgeneralizes.
- **Cheapest first test.** Use an affine read map on two one-coordinate suffixes and a third suffix that crosses a shared clipping knee. Require the scoped proof to fall back on the third.
- **Old-task retention.** Run both old input modes on every admitted branch, including inside the clipped segment; measure whether fallback still meets the old deadline.

#### 06. Keep the ordinary mode payable when its probe is late — P
- **Mechanism.** If an ordinary-input observation is delayed, propagate its last valid lower bound through the actual intervening updates. Admit only if that certified bound still passes plus a fresh check of the new blocker; otherwise defer until the ordinary read is observed.
- **Novelty / control.** Bounded staleness monitors track old observations. Here staleness applies to only the nonbinding read of an immutable pair, not permission to trade away that read; compare with wait-for-both, active-set-only checking and exact checking when available.
- **Cheapest first test.** Delay N one slot and bound its drift for two fixed update maps. Include a third map whose worst-case drift exhausts the bound before the probe returns.
- **Old-task retention.** Reveal the withheld N results for evaluation at every prefix, score both held-out modes after B, and count a missed N deadline even if X and B pass.

#### 07. Find when two modes of a routine are genuinely inseparable — I
- **Mechanism.** Audit the response rank of the paired reads on the *lawful* A/C and later B update set; look for a pair of reachable states that reverses blocker identity at matched sorted gaps.
- **Novelty / control.** A sensitivity audit, not a new learner primitive. Compare #292#12 across unrelated readers, a fixed active set, and the exact finite reachable set; do not infer inseparability merely from equal gradients at one point.
- **Cheapest first test.** Contrast tied read scores, two independent coordinates, and a clipping case where local rank one misses a finite handoff.
- **Old-task retention.** Apply both frozen mode contracts and the routine's ordinary held-out suite to all proposed handoffs and show that the tied case still serves old inputs after refusal.

#### 08. Preserve a paired read across a routine replacement — P
- **Mechanism.** Transfer an old handoff witness to an approved routine version only on inputs for which a paired refinement check bounds both versions' outputs under the same prefix and suffix; reject the transfer for any changed mode without such a bound.
- **Novelty / control.** Behavioral refinement checks upgrades. The proposed reusable object carries a mode-specific suffix witness across versions while keeping the original old-input promise; compare with dual-version full checks and reusing by routine name alone.
- **Cheapest first test.** Replace an affine routine with one equivalent in N but clipped in X. Give one suffix that stays inside the equivalence interval and one that leaves it.
- **Old-task retention.** Hold the old routine's N/X inputs and floors fixed across versions and audit both on ordinary execution and after the suffix; count a rejected transfer as safe, not as B success.

### Keep one conditional budget (#299#13)

#### 09. Return a disjunction of rights, not two permissions — P
- **Mechanism.** Publish one record-indexed contingent payment plan. Distinguish P-or-Q from P-and-Q; on actual spend advance all branches containing that spend, then revalidate live exercise before admitting either continuation.
- **Novelty / control.** #292#02 gives a witness per right; locks and escrow prevent reuse. Test whether a shared *unspent* disjunction preserves more lawful choices before arrivals than fixed reservations at matched checks, and compare with exact joint scheduling.
- **Cheapest first test.** Use both orders in R2, including T deletion and failed revalidation after S is spent. Treat the absence of a second live witness as defer, not an already-paid promise.
- **Old-task retention.** Pay each due A/C job once in each actual trace and check the waiting queue's previously learned B task after the winner and after refusal.

#### 10. Share a prefix that survives both possible winners — P
- **Mechanism.** Execute common due work before the arrival distinguishes the winning right only if one causal prefix leaves valid conditional payment plans for both outcomes. Debit the common work once; make no commitment to the later branch yet.
- **Novelty / control.** Contingent planning already factors common prefixes; #299#13 shares a scarce record. Test reuse of the realized learner-state prefix as well as its accounting, versus locks, separate plans and exact replanning.
- **Cheapest first test.** Add a due prep record to R2 and hide which partner will be timely until the next slot. Replace prep with a same-progress record that closes Q's landing.
- **Old-task retention.** Check the shared A/C update once on each trace, then each branch's remaining old jobs and both queues' prior B gains.

#### 11. Check the freshness of payment and exercise separately — P
- **Mechanism.** An execution receipt names the consumed record and paid job; a separate live exercise check names the learner state, precision and serving clock. An intervening tick can invalidate exercise without undoing the payment.
- **Novelty / control.** Optimistic validation and [linearizability][linear] already separate reads from commits. Test whether a split receipt allows scoped reuse of the old-service proof after failed exercise, versus a global version invalidation and a lock held through exercise.
- **Cheapest first test.** Place a mandatory momentum-only tick between payment and exercise in R2. Make it cross P's landing threshold while all paid old reads remain valid.
- **Old-task retention.** Probe A/C before and after the tick and after refusal, and recheck the paid job without replaying S; check the deferred queue's prior B.

#### 12. Price a threat to two rights by the record it actually spends — P
- **Mechanism.** For the next due job, annotate each legal record with which joint continuations its execution removes. If records make equal old progress, choose one that preserves a declared minimum menu of on-time completions whenever possible.
- **Novelty / control.** Matching sensitivity and #292#20 already price opportunity. Test a reusable record-to-menu contraction keyed to executed landings, against first-come, lock-based shadow prices and exact joint recertification.
- **Cheapest first test.** In R2 let Q use either S or T now. Compare the conditional menus after each spend; then make T expire before this slot so no choice can preserve both.
- **Old-task retention.** Match held-out old progress for S and T at that deadline, check the later job with the remaining record, and measure the deferred B queue after any exercise.

#### 13. Release a stale right without returning what it spent — P
- **Mechanism.** When a right expires, withdraw only its unexecuted claims. Attribute actual service receipts to old jobs, independent of whether the proposed right completed; rebuild the surviving right's residual plan from never-spent records.
- **Novelty / control.** Timeout and reservation release are standard. Test whether a record/learner-state residual representation avoids both stale reservation losses and duplicate service credit compared with priced expiry and fresh matching from the execution log.
- **Cheapest first test.** Let P expire after S, while Q's tentative plan still names S. Keep T in one arm and remove it in another; require Q to complete only in the former.
- **Old-task retention.** Evaluate the already paid old slice at its original deadline and through expiry; score the jobs done by T or U and both queues' pre-existing B tasks.

#### 14. Expose a conflict that exists only across exercise orders — P
- **Mechanism.** Give a pair of rights an ordered incompatibility witness when the first exercise changes the eligibility of a distinct, unspent payment for the second. Preserve the reverse order only if it is still executable and on time.
- **Novelty / control.** Stateful scheduling handles order constraints; #299#13 starts from a shared record. Test whether an order-specific refusal can be reused across arrivals better than static resource locks or repeated exact schedules.
- **Cheapest first test.** Let P spend S and Q spend T, but give P's exercise a fixed effect making T miss Q's old-read threshold. Make Q-first leave S lawful; use a no-effect P as a negative control.
- **Old-task retention.** Follow both orders on held-out A/C inputs, pay Q's affected old job via an ordinary fallback on refusal, and probe prior B for both queues.

#### 15. Make three pending rights reveal a budget invisible to pairs — P
- **Mechanism.** Represent admissible groups explicitly up to a small bound. A witness can cover every singleton and pair without asserting a simultaneous triple; at each spend specialize to the observed branch and discard infeasible groups.
- **Novelty / control.** [Hall's condition][hall] already exposes higher-order shortages; no novelty in the cut itself. Test whether the cut and corresponding learner-state preconditions are reusable across actual exercises, versus pairwise locks, cached matching and exact joint planning.
- **Cheapest first test.** Give three rights two swap-opening records and a third old-only record. Every pair can finish by its deadline, but no triple can; add one genuinely swap-opening replacement as a positive arm.
- **Old-task retention.** In all arms pay the third old job regardless of its right; measure the least-served old slice and prior B of the right excluded from exercise.

#### 16. Reserve no record, but prove a refusal path before spending — P
- **Mechanism.** Before an optional-right-opening old update, require an old-only continuation after each exercise outcome allowed by the current observations, including live refusal. These paths may use different residual records; none uses the one already spent or a future unobserved record.
- **Novelty / control.** #299#15 protects the old schedule on partner no-show. Here the partner can arrive and still fail live validation while another right competes for the remaining coverage; compare with fixed standby, per-right no-show proofs and exact recourse.
- **Cheapest first test.** Use two remaining old jobs whose available record eligibility depends on whether P exercised. Remove the only old-safe fallback after live refusal while leaving the timely-success path feasible.
- **Old-task retention.** Execute all allowed continuations with the same original A/C deadlines, and check prior B both after the accepted suffix and after the refused path's ordinary work.

### Make the read handoff and the shared budget constrain each other

#### 17. Swap the blocker without spending the audit record — P
- **Mechanism.** Choose a disjoint completion that leaves a mandatory old audit unspent until it can observe the nonbinding read. The audit remains old service and cannot be charged as preparation for a second right before it executes.
- **Novelty / control.** #292#07 keeps a separate old witness and #299#13 shares payment. Require an interaction: the individually best handoff would use the only timely audit record, while a different payable handoff leaves both a safe suffix and a real audit. Compare with independent holdout plus matching.
- **Cheapest first test.** Give two same-progress preparations reversing the same blocker, only one of which uses the audit's unique eligible record; add an audit-independent arm in which the stacked control should tie.
- **Old-task retention.** Probe both modes before and after the suffix, with the nonbinding mode audited on its declared clock; verify the losing queue's prior B and the unpaid-old-job fallback.

#### 18. Admit a second right only after its ordinary mode is ready — P
- **Mechanism.** A winner may clear a suffix constraint but leave the other right waiting on an ordinary read. Let the latter proceed only after a disjoint, already due payment has actually restored that read's required readiness threshold above its baseline safety floor.
- **Novelty / control.** #299#20 uses B to ready an old payment; here a remaining old payment is a prerequisite for the *other* right's ordinary contract. Compare with full paired checking plus matching and exact joint scheduling, not with a tracker that incorrectly waives the nonblocking mode.
- **Cheapest first test.** P leaves Q with both suffix gaps nonnegative but an ordinary readiness score below threshold; only T can raise it before Q expires. Replace T with a suffix-only improvement.
- **Old-task retention.** Check the ordinary safety floor throughout, check Q's stricter read on time, and confirm the T update and Q exercise preserve P's prior B gain.

#### 19. Make different arrival outcomes converge to one usable proof — P
- **Mechanism.** After different timely winners, join proof branches only when the remaining timed payment choices and the paired read bounds needed by all still-live suffixes agree; retain exact receipts even at a proof join.
- **Novelty / control.** #299#16 joins service-equivalent frontiers; this join also requires equivalence of the *nonbinding* mode, on ordinary inputs and under future suffixes. Compare with full-state hashing and the best stack of service-only joins plus fresh read checks.
- **Cheapest first test.** Enumerate two traces with different spent records but interchangeable residual eligibility and equal paired bounds. Perturb only the nonbinding ordinary read in one trace, and try a suffix that later exposes it.
- **Old-task retention.** Audit both original traces separately on A/C deadlines and both old input modes after every claimed continuation; retain each trace's learned B gains.

#### 20. Distinguish a payment shortage from a paired-read conflict — P
- **Mechanism.** Return a refusal witness that distinguishes no disjoint old payment plan, a normal-read violation on all plans, and a suffix-read violation on the plans that remain. A cached refusal may be reused only until its actual dependencies change.
- **Novelty / control.** #299#21 separates coverage and B-response shortages. Test whether distinguishing nonbinding ordinary debt from suffix blockage recommends a different lawful next check or available record, versus joint exact planning and generic infeasibility explanations.
- **Cheapest first test.** Build three tiny traces that differ by only one targeted repair: add a replacement record, restore a normal input score, or add a truthful B response. See which repair invalidates the corresponding refusal.
- **Old-task retention.** On all refusals execute available ordinary coverage and measure both modes at their deadlines plus prior B; explicitly report if old work was already infeasible.

#### 21. Hand the budget across schedulers without trusting their read aliases — P
- **Mechanism.** Two service schedulers may use different names for the same routine mode. Transfer the residual right plan only with shared record identities and a checked mapping that preserves input populations, read floors and charge history; an unresolved alias forces deferral.
- **Novelty / control.** Federated escrow prevents spending the same unit in two places; schema mapping preserves meaning. Test a transfer where an alias mistake changes both the purported payer and the blocker, versus synchronized locked scheduling and full centralized recertification.
- **Cheapest first test.** Hand off after one paid slot; give the receiver a stale alias for spent S and a reversed N/X label. Correct each independently and ensure neither partial correction licenses an unsafe exercise.
- **Old-task retention.** Replay the original routine's held-out populations through the new scheduler, check every promised old job and repeat both prior B probes across the handoff.

#### 22. Test whether the two seeds buy anything over the strongest stack — I
- **Mechanism.** Cross true versus tied read modes with disjoint versus conflicting payment pools, retaining identical deadlines, old work and prior B. Add an arm with a naturally late or absent partner, not just explicit exercise requests.
- **Novelty / control.** This is a falsifier, not a new primitive. Compare the best paired active-set/GEM check plus locks or incremental exact scheduling with the joint proposal; if the stack ties at matched cost, report no interaction.
- **Cheapest first test.** Enumerate the arrival and clock branches of R1/R2 and a smooth accumulation control with the same actual evaluation seams. Measure qualified completions, worst observed proof cost and refusals, not the count of pending rights.
- **Old-task retention.** Use one held-out A/C and prior-B panel across all arms, by the original deadlines, including traces with successful ordinary service but no new B completion.

## Ranked deeper questions

1. **Can the nonblocking mode decide which competing right can finish on time, without adding an old-service slot?** Start with 01, 09 and 17, and include 22. Freeze routine modes, raw arrivals and deadlines before scoring alternatives. Look for a real disjoint execution that retains both reads and prior B and either beats the best stacked controls at matched cost or needs fewer checks than fresh exact planning. If only the engineered cases separate, report the availability limit.
2. **Can a split read witness survive a meaningful change in inputs or suffixes without concealing the old obligation?** Start with 02–05 and the tied-read audit in 07. Measure the cost of checking the scope versus doing both reads afresh and require correct refusal on route shifts and inseparable modes.
3. **How much freedom remains after real service but before live exercise?** Start with 10, 11, 14 and 16. Vary clock ticks, expiry and partner timing on the same tapes; compare useful on-time completions and proof cost against first-come, locks, escrow and exact causal joint scheduling. If every actual spend forces a global recheck at no greater cost, keep ordinary scheduling.
4. **What can be safely reused across arrival traces or schedulers?** Start with 15, 19 and 21. Reuse a witness only if it preserves the entire old payment plan and both read obligations, including the formerly nonbinding one. Measure how often a projected proof must fall back to full-state revalidation.

**Verdict:** The examples separate a blocker from the obligation that owns it, and a spent payment from permission to exercise. They establish neither natural availability nor an advantage over exact checks. Keep the two mechanisms separate unless the joint operation preserves useful choices or saves verification without weakening retention.

[parent]: https://github.com/manojbajaj95/cl/pull/299
[parent-file]: inward-service-3.md#two-exact-paper-checks
[triage]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/flood-triage.md#L417
[ledger]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/idea-ledger.md
[gem]: https://proceedings.neurips.cc/paper/2017/hash/f87522788a2be2d171666752f97ddebb-Abstract.html
[hall]: https://doi.org/10.1112/jlms/s1-10.37.26
[escrow]: https://doi.org/10.1145/7239.7265
[linear]: https://doi.org/10.1145/78969.78972
[smooth]: https://github.com/manojbajaj95/cl/pull/113
