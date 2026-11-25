# Inward service: recover a drifted landing and settle an opener from its own queue

**Status:** Ideas only. The rational examples are paper checks, not pilot results. All first tests are pencil-and-paper or CPU-only; no GPU.

**Parent:** [Service-robust swaps](service-robust-swaps.md) ([PR #268](https://github.com/manojbajaj95/cl/pull/268)). **Review seeds:** [Flood triage, #268 verdict][triage], score-3 cards #268#04 (ordinary A/C service pulls a drifted landing inward) and #268#14 (an unmatched opener discharges itself). This node takes the stricter same-queue branch of #268#14: A/C work may help, but settlement must be earned by later truthful records from the opener's own queue. The [idea ledger][ledger] requires old-task retention in each first test and the strongest stacked control at equal budget.

## The two obligations

- **Recover the right, not just the floor.** Freeze the shared learner, optimizer, A/C service vocabulary, legal arrival and idle traces, reachable full-state envelope and residual menu before choosing an opener pair. Write `F_L` for the states the opposite clip `L` fixes under the existing proof (including any slot, clock or serving-state effects that proof reads); independently require that the still-untreated left tail remains in `L`'s active repair domain. A legal disturbance may push a first landing out of `F_L` without breaking A/C. Suspend the old second-item right there. A bounded run of ordinary A/C work must keep A/C safe at **every** exposed prefix and put the entire repaired landing tube strictly inside `F_L`, with a precision buffer, while retaining the active opposite tail and validating the post-seam suffixes. A partner arriving during recovery may join the ordinary queue but cannot exercise the suspended right. A missing or outward-running service prefix never earns a recovery right.
- **Settle the no-show, not just the ticket.** At the no-show boundary, revoke the old swap ticket. Declare which ordinary later records from the opener's original queue are admissible and what happens if they are late, missing or ineffective. Executed records must provide real learning value and put the forward state inside a terminal A/C and suffix contract strictly stronger than merely declaring expiry. Bind settlement to that reached interface, not to elapsed time or promised arrivals. Keep the opener's gain and intervening work, use no checkpoint restore, inverse update, relabelled/synthetic partner, direct optimizer write or undisclosed partner feed. Until completion keep the narrower safe menu; any late partner needs a fresh admission check.

**Shared falsifier.** Compare with #249#07 preservation-only service, paused/protected waiting, fresh per-step exact recertification, fixed clamp, #249#09 priced timeout, [#233 margin-loan repayment][loan], [#214 escrowed successors][escrow], full-state rollback (charge discarded work), and ordinary SGD on the same arriving records without a special contract. For combined cards use the best stack of these, not each in isolation. Match raw arrivals and provenance, ordinary A/C completed work and delay, useful B gain per queue, deadlines, steps, checks and peak bytes (or show the Pareto gap). Check worst-slice A/C performance at every exposed prefix and on all claimed suffixes, including held-out old readers; show no lift from simply turning off the hard queue or widening an old floor. Run smooth/gradient-accumulation [#113][smooth] and a tail-free pack as nulls. If a bare forward SGD run attains the same certified admissions at equal cost, the result is ordinary continued learning.

**Nearest prior art.** Bounded recovery and reachability already exist in [rely-guarantee composition][rg], [control barrier functions][cbf] and temporal assume–guarantee contracts. [Sagas][sagas] and the parent's transactional-memory controls already cover expiry and compensation. Repo-near controls are [echo-absorbing ordinary work #238][echo], [momentum landings #242][momentum], #268#20's service-paid timeout upgrade, #233's repayment, #214's escrow and [verified renewal #243][renewal]. The claim to test is narrower: a reversible *permission* can be earned back by doing required old work on the actual learner, and a missing teaching partner can be retired by new work from the original queue, without reversing a learner update. Neither reachability nor ordering SGD is itself the novelty.

## Paper fixtures

Use the parent's shared weights `(h,u)`, but write `x=h+u`, `y=u−h`. Start at `(x,y) ∈ {(3/2,−3/2),(−3/2,3/2),(0,0)}`; define the old floor gaps `A=2−x−d` and `C=2−y+d` for candidate suffixes `d ∈ {−1,0,+1}`. The two truthful B clips with target zero are `R: x←min(x,1)` and `L: y←min(y,1)` (SGD with `η=1/2` on half squared hinge residuals). Each acts on both original weights when active. At this same learning rate the squared residual loss `(y−t)²/4` moves `y←(y+t)/2`, leaving `x` unchanged.

**I1 — Inward recovery is neither preservation nor permission to clear the other tail.** After `R`, use a drift tick `W` that sets `y=5/4` on the reached `x=1` landing and does nothing on the other two branches. One realization on this finite support is an old-task SGD step on `g(x)²(y−5/4)²/2`, with a plateau gate `g=1,g′=0` near `x=1` and `g=0,g′=0` for `x≤0`. This is an admitted disturbance, not a replay batch or a certificate repair. The repaired branch is now `(1,5/4)`: A/C are safe at `d=0`, but `L` would rewrite this branch, so its inherited right is suspended. Let each of the next two ordinary old-service records execute `S: y←(y+7/8)/2`. On the repaired branch, `y` goes `5/4 → 17/16 → 31/32`; on the untreated left tail it goes `3/2 → 19/16 → 33/32`. The first service record is insufficient. At the second, `L` fixes the first branch with buffer `1/32` and actively repairs the untreated branch by `1/32`. A/C stay safe at `d=0` throughout; after `L`, both `d=±1` are individually safe relative to that seam. One step toward `3/2` rather than two toward `7/8` leaves A/C safe at `d=0` but moves the repaired branch outward to `11/8`. A third `S` without exercising the right makes the opposite tail inactive (`61/64`); more inward work is not always better. Mirror the fixture by exchanging `x,y`, `R,L`, and the sign of `d`.

**I2 — Same-queue settlement earns a suffix that expiry does not.** From `R → W`, let the partner miss its deadline, revoke its ticket, and keep `{0,+1}` as the safe alternatives at the seam (execute neither nonzero shift during settlement). Later naturally arriving right-queue records `D₁,D₂` are distinct B views with truthful targets `15/16,3/4` for the squared residual above. They train the same shared weights, with no `L` record. Across the full envelope, `max y=3/2 → 39/32 → 63/64`; `max x=1` throughout. Both records improve their own B loss on the two initially positive-`y` branches without changing the opener's right-hinge gain. Both retain A/C at `d=0`. After `D₁`, `d=−1` would still fail C by `7/32`; after `D₂`, it clears C by `1/64` and the terminal menu can include either sign. `D₂` alone leaves `max y=9/8`; reversing `D₂,D₁` leaves `33/32`. Mere expiry does not enable the new suffix. A late `L` does not revive the old ticket even when the new terminal menu happens to match its suffixes. These toy views are specified up front: the fixture shows an interface separation, not how frequently helpful B items occur, whether shared-state momentum preserves it, or whether separate queue labels buy anything.

## Idea cards

**P** denotes a candidate primitive (the new reusable object or operation is named in the mechanism); **I** denotes an improvement or audit, not a pilot nomination. In all tests, execute only records actually available under the declared queue policy.

### Ordinary service earns back a suspended swap

#### 01. Recoverable second-item right — P, #268#04 seed
- **Mechanism.** Issue a recoverable right with separate safe-but-suspended, exercise-ready and expired states. A declared old-service run changes the right only by moving the drifted landing into the opposite fixed set while leaving its tail active.
- **Novelty / control.** #249#07 preserves a live right; #238 contracts slot gaps. Test earning back a lost cross-opener identity against a fixed clamp, pausing service and #238 plus per-step recertification.
- **Cheapest first test.** Enumerate I1 in both orientations, delivering the partner at zero, one, two and three completed service steps; also substitute the outward record at the first step.
- **Old-task retention.** Check A/C lower bounds at every wait/service prefix and after each exercised suffix; a refused join must leave ordinary service available.

#### 02. A window between two moving boundaries — P
- **Mechanism.** Compile an entry bound into the opposite fixed set and an exit bound for the untreated tail's active set. From only public service events, return the intervals when the partner may exercise the right.
- **Novelty / control.** #268#02 meters expiry and #260 parks support timed entrants; this window both opens and closes as the same old work progresses. Compare with per-step exact checks and the best fixed post-drift delay.
- **Cheapest first test.** Use I1 with two certified service strengths chosen by the old queue; show that elapsed steps alone cannot distinguish a still-outside branch from an over-contracted tail.
- **Old-task retention.** Keep both A/C floors across continuations while the window is closed, including after service overshoots the active band.

#### 03. Inward only as a whole run — P
- **Mechanism.** Certify an ordinary A/C word whose first step can increase distance to the fixed set, while improving its old task and keeping all floors; later steps pull the landing inward more than the first displaced it.
- **Novelty / control.** Multi-step barriers allow nonmonotone progress; the delta over #268#03 cone filtering is useful A/C that no stepwise inward cone would admit. Compare against ordered and accumulated versions of the same records with exact checks.
- **Cheapest first test.** Enumerate two orders of two truthful records on a rational coupled host; require one word to recover the right and the other to fail despite matching per-record availability and step count.
- **Old-task retention.** Check both floors after the outward step alone, on interruption there, and after both records and the released suffix.

#### 04. Recovery by old-queue choice, not by state oracle — P
- **Mechanism.** Publish a menu of service words with a common certificate for each *public* dispatch class (actual A/C record identity and deadline class), covering every hidden optimizer history consistent with the dispatch.
- **Novelty / control.** #242's worst-alias refill chooses a useful batch; this interface certifies dispatch by existing queue observations without guessing the hidden landing. Compare with a single robust word, per-history oracle, and fresh verification.
- **Cheapest first test.** With two slot aliases and two old queue orders, find a public menu that recovers on both aliases; add an alias on which the same observations no longer suffice.
- **Old-task retention.** Hold A/C service deadlines fixed and check both aliases, especially the alias with the worse post-dispatch C floor.

#### 05. Inward in the deployed state, not just the weights — P
- **Mechanism.** Use an ordinary A/C run that moves a slot or running statistic into a set where the next partner step is observationally an identity; require the return of the right to be robust to the next permitted idle tick.
- **Novelty / control.** #238 already damps slot echoes; here identical visible landings have different partner rights, and future old-task continuation defines equivalence. Compare with #238 plus exact checking, slot reset, and a weight-only certificate.
- **Cheapest first test.** Construct two equal-weight momentum states with opposite slot signs on a two-weight ReLU host. Apply the same truthful A/C word and enumerate the partner and next idle transition.
- **Old-task retention.** Probe old A/C after slots propagate into parameters, not only on the equal-weight checkpoint; also check each service prefix.

#### 06. Same inward boundary, different old reader — P
- **Mechanism.** Certify recovery against a bank of fixed-set tests indexed by existing old readers. Release a narrower partner suffix if the ordinary service word repairs one reader's relevant interface but not another.
- **Novelty / control.** [Menu replacements #235][menu] already narrow menus. The added test is whether required service changes *which* old reader licenses a suffix, even where coarse landing distance ties. Compare with a single uniform tolerance and #235 plus exact checks.
- **Cheapest first test.** Use two old readers of a shared running statistic and two service words with equal weight endpoints but opposite effects on the statistic; check whether they license different safe suffixes.
- **Old-task retention.** Both readers must remain above their original floors, including the reader that does not license the release.

#### 07. Spend old-service redundancy on the repair — P
- **Mechanism.** Within equivalent due A/C work (same supported old predictions and deadlines), choose the naturally arriving realization whose executed map crosses a lost swap boundary. Do not add a batch or project the gradient.
- **Novelty / control.** GradMatch and OGD already select or project gradients. Compare against matched old-progress GradMatch, gradient projection, and fresh exact selection; the delta must be in the reachable partner right, not gradient similarity.
- **Cheapest first test.** On a shared-weight host, enumerate two ordinary ways to service the same old slice with tied held-out old gain but distinct effects on an opposite hinge; blind the selection to future B arrivals.
- **Old-task retention.** Match old A/C gain on independent slices and serving latency; report the worst slice if the two routes are not equivalent.

#### 08. Recovery can survive a missing service slot — P
- **Mechanism.** Certify a bounded erasure-tolerant word of real old tasks by quotienting arrival traces that lead to the same recovery corridor; idle transitions for omitted work are part of the proof.
- **Novelty / control.** Robust reachability already handles dropouts. The candidate operation is a reusable *learner right* under different actual A/C arrivals, beating #268's fixed envelope plus late recertification without duplicating data.
- **Cheapest first test.** Enumerate three due A/C opportunities including each possible single erasure; withhold two as a negative, and include clock advancement in every omission.
- **Old-task retention.** Check worst A/C after every permitted omission and charge any missed old-task deadline even if the hinge ends up inside.

### Later truthful records settle their own opener

#### 09. Same-queue forward settlement certificate — P, #268#14 seed
- **Mechanism.** Certify a terminal suffix interface that is earned only after subsequent useful records from the opener's own queue execute. Retire the old relationship without refunding a margin by fiat.
- **Novelty / control.** #249#09 prices expiry, #233 lends margin and #214 can pre-escrow successors. Compare with all three, saga rollback, and ordinary same-queue SGD plus fresh verification.
- **Cheapest first test.** Enumerate I2 with no partner, no later records, both prefixes and the reversed order; verify that only the certified completed word earns the additional suffix in these traces.
- **Old-task retention.** Check A/C at `d=0` after every forward record and on the widened menu, including the still-untreated tail before completion.

#### 10. Settle without reserving the next item — P
- **Mechanism.** Specify a public predicate of acceptable later own-queue records and a verified residual bound for each class, keeping FIFO within the queue. Hold an explicit safe pending route when no acceptable arrival materializes.
- **Novelty / control.** #214 buys certainty by locking concrete successors. Here a later class witness may settle with no inventory commitment; compare with an equally sized escrow, fresh checking and ordinary FIFO without a certificate.
- **Cheapest first test.** In I2-like traces reveal two disjoint acceptable continuations after the opener and one stream containing neither; freeze the class predicate before reveal.
- **Old-task retention.** Check the same old floors on both accepted continuations and on the entire unsuccessful wait; report any A/C work lost to FIFO blocking.

#### 11. Productive instalments that are useless in isolation — P
- **Mechanism.** Use later records whose useful teaching maps put the leftover hazard into a region the next naturally arriving record can repair, even if neither record alone qualifies to settle.
- **Novelty / control.** [ITS4][its4] hands off a gap to a frozen downstream damping batch; require both records to be later own-queue teaching and the terminal effect to retire a no-show right. Compare with ITS4, #233 and best single record plus recertification.
- **Cheapest first test.** Check I2 as the additive null, then try two coupled hinge views where no order-insensitive repayment meter distinguishes successful from failed settlement; charge failed prefixes.
- **Old-task retention.** Check A/C after each instalment and all terminal suffixes, and preserve the first opener's held-out B gain.

#### 12. Retire the untreated tail without training its labels — P
- **Mechanism.** Let later own-queue observations change the shared features that expose the opposite old-task hazard, requiring safe suffixes without matching the missing queue's B behavior. Do not claim credit for its unserved B task.
- **Novelty / control.** #233 can pay back the original margin and #214 can install its paired successor. Compare with margin repayment, a thin opposite-label escrow, and a matched own-queue update with the shared feature frozen.
- **Cheapest first test.** Move a shared feature with a naturally observed B label different from the partner's; verify the opposite old hazard closes on held-out states even though partner B test loss does not improve.
- **Old-task retention.** Test both old readers, including an independent readout of the supposedly retired opposite tail under each new suffix.

#### 13. Same-queue proof from forked continuations — P
- **Mechanism.** Allow multiple future own-queue words to reach a common terminal interface, so different lawful future teaching needs need not be homogenized into a surrogate “repayment” batch.
- **Novelty / control.** This is stronger than #268#13's menu downgrades only if two genuinely different learning endpoints share a reusable settlement proof. Compare against existence-only reachability, fixed loan repayment and branch-specific fresh recertification.
- **Cheapest first test.** Build two pairs of truthful future records with different fitted B functions but a common old-reader abstraction. Add a third branch whose fitted function matches one pair on B but escapes the abstraction.
- **Old-task retention.** Verify the common old floors and every advertised suffix separately on the two admitted branches; do not average away a branch failure.

#### 14. Pay the untouched tail first, keep opener gain — P
- **Mechanism.** Require each purported settlement word to satisfy a protected opener-gain witness and a separate verified reduction of the worst still-live old-reader hazard. A later record that lowers its own B loss by relearning what the opener already knew cannot settle.
- **Novelty / control.** #242#16 raises the worst reserve and #233 prices repayment; this two-obligation interface separates a third party's old hazard from local own-queue gain. Compare with summed loan repayment, gain-only choice and fresh checks.
- **Cheapest first test.** Use two available later record classes with equal B improvement: one regresses the opener on a held-out view, one repairs the opposite hazard without regression. Include a third that preserves the opener but never pays the hazard.
- **Old-task retention.** Report A/C on all three branches and preserve a separate slice for the worst untreated history after each prefix.

#### 15. No-show with no possible settlement — P
- **Mechanism.** Produce a reusable impossibility witness from the executed-map closure of the remaining own-queue vocabulary, so the learner can keep serving the safe menu instead of waiting for a certificate it cannot earn.
- **Novelty / control.** Reachability exclusion is known, and #268#07 caches service failures. Here the negative certificate quantifies forward *same-queue* words, rather than a broken swap edge. Compare with a fixed expiry and brute-force future recertification.
- **Cheapest first test.** Replace I2's vocabulary with targets `1≤t≤3/2`; prove no finite sequence of half-contractions brings the left-tail branch from `y=3/2` to `y≤1`. Add a legally arriving `t=1/4` and invalidate the witness before admitting a new route.
- **Old-task retention.** Check that the stable restricted menu remains A/C-safe even when the proof says settlement is impossible; never interpret non-settlement as a reason to pause old work.

#### 16. Future records must not be a partner in disguise — I
- **Mechanism.** Audit independent provenance, arrival timing and own-task held-out value for each later record; reject synthetic substitutions, retrospective selection using the missing label and updates that simply undo the first opener.
- **Novelty / control.** Provenance auditing is not a new learning primitive. Use #214 escrow and saga compensation as honest controls and keep the same raw stream in the ordinary-SGD arm.
- **Cheapest first test.** Blind the scheduler to the partner queue and permute same-queue availability within predetermined legal arrival traces; flag a fixture that only works if a helpful record is hand-inserted just at timeout.
- **Old-task retention.** Retain A/C checks on the blinded traces and record the old throughput penalty when helpful records do not appear.

### The obligations interact

#### 17. Inward service changes which later record can settle — P
- **Mechanism.** Use old service to bring the residual into the attraction region of a future own-queue record that would not settle on either the drifted or the undrifted branch under the same budget.
- **Novelty / control.** #268#20 lets service itself widen a menu; ITS4 puts a gap into a downstream damping range. Here require a strict interaction across old service and a later own-queue record, beating the best stack of standalone recovery and settlement.
- **Cheapest first test.** Make a piecewise CPU host with a finite attraction interval; freeze one ordinary A/C and one later B record. Enumerate neither, each alone, both orders, and a same-work control that keeps `S` in the preservation-only band.
- **Old-task retention.** Keep A/C floors on all admitted intermediate states and demonstrate the new suffix passes only after both required records.

#### 18. A genuine choice between recovered swap and self-settlement — P
- **Mechanism.** Retain two separately priced continuations after recovery; executing the first settlement record may eliminate the other tail's repair obligation, so choosing settlement must irrevocably retire the old right before spending the terminal margin.
- **Novelty / control.** #268#18 intersects obligations and #268#19 times out early. Here the *same reachable prefix* offers two useful, mutually exclusive continuations, not just an escape from unsafe service. Compare against the best fixed-priority joint certificate and atomic fresh recertification.
- **Cheapest first test.** From I1's second service step, branch into timely `L` or revocation followed by suitable I2 records. Inject a cached join ticket after both paths would advertise the same suffix name; require only the current epoch to authorize the seam.
- **Old-task retention.** Check A/C on both legitimate branches and on stale-ticket rejection, without counting either branch's suffix allowance twice.

#### 19. Repair the landing without burning a queue's only settlement word — P
- **Mechanism.** Jointly choose a lawful old-service word and a public settlement interface so inward movement helps the live swap while preserving the availability and gain of a later same-queue teaching word.
- **Novelty / control.** #268#18 intersects two safe envelopes; additionally distinguish schedules that make a real later record vacuous from schedules that let it settle productively. Compare with independent best recovery plus best timeout at equal completed A/C.
- **Cheapest first test.** Enumerate two words with identical recovery margin; one already zeroes the only later record's residual without retiring the untreated hazard, the other lets that record act and settle. If no such coupled host can be constructed, drop the card.
- **Old-task retention.** Check both A/C prefixes and the no-show menu; compare the timely-join branch to detect starving the partner to make settlement look better.

#### 20. A transfer limit for inward headroom — P
- **Mechanism.** Expose separately the portion of recovered landing margin that is reusable after no-show and a witness that the remainder is specific to the opposite clip's identity. Future own-queue items can spend only the former toward a terminal menu.
- **Novelty / control.** #268#21 accounts for double spend; the new separation is nontransferable *geometric* headroom even if the numerical slack matches. Compare with the best joint scalar ledger and exact rechecking of each suffix.
- **Cheapest first test.** Build two equal-inward-margin landings where one later same-queue record commutes with one landing's live state projection but not the other. Compare a typed transfer bound with the tightest sound scalar meter at equal receipt size.
- **Old-task retention.** Check A/C at transfer and after spending it on each legal suffix; retain the witnessed nontransferable branch as a hazardous-admit control.

#### 21. Forget the settlement history only at a common continuation — P
- **Mechanism.** Compress completed join and completed self-settlement histories to one public interface only when future legal A/C words and fresh partner arrivals cannot distinguish their admitted suffixes. Don't merge purely because both tickets are closed.
- **Novelty / control.** #243 renews at a ready interface and #268#22 renews mixed rounds. Require equivalence under a fresh reader/partner that never participated in the first settlement, comparing with a separate receipt per route and fresh verification.
- **Cheapest first test.** Alternate one timely join and one self-settlement, then replay identical fresh old work and B arrival on the two terminal envelopes; add a slot alias that agrees on weights but invalidates one next right.
- **Old-task retention.** Check the old A/C readers across both paths and the next seam, including the alias that exposes a hidden retention debt.

#### 22. Null: can the premises be reduced to scheduling? — I
- **Mechanism.** Measure which gains survive matching raw useful work, precision, deadlines, certificate checks and both queue budgets against accumulation and ordinary SGD plus fresh verification.
- **Novelty / control.** This is a guard against the ledger's killed bounded-delay scheduling idea and against calling a hand-set toy threshold a primitive. The positive signal must be a strict reusable-certification or safe-admission gain.
- **Cheapest first test.** Repeat the smallest combined counterexample in a smooth linear host, a tail-free host and the original kinked host; report exact reachability and verifier work separately from SGD endpoint quality.
- **Old-task retention.** Run identical held-out A/C probes at every seam and vulnerable prefix in all arms; compare worst slices at matched B gain rather than whichever arm moves less.

## Ranked deeper questions

1. **Is there a nonempty recovery window once the actual optimizer state matters?** Start with 01, 02 and 05. I1 separates floor safety, repaired-landing identity and opposite-tail activity, but only for rational SGD. Enumerate a tiny coupled host with momentum slots and real idle ticks before trying Adam. If the full-state fixed set or robust interval disappears, preserve the negative result and prefer exact recertification.
2. **Can truly later own-queue work settle without smuggling in a successor escrow or a partner label?** Start with 09, 10, 15 and 16. Freeze queue populations and hold out arrival traces before selecting an opener. Include queues that cannot discharge, compare priced timeout plus ordinary SGD and fresh checks, and count both honest pending time and useful B retained. A same-queue word found only by hindsight is not a deployable right.
3. **Is there an interaction beyond the best independent stack?** Start with 17–20. Freeze one natural A/C run and one later own-queue word. Require both a timely-join option and a certified no-show benefit that neither component alone nor the budget-matched stack can reproduce; keep the order-swapped, withheld and over-contracted controls.
4. **Can the recovered or settled seam be reused without carrying the lost history?** Start with 06 and 21. Compose a fresh round with late arrivals and an old reader of live optimizer state. If only full historical verification prevents a false join or a hidden old-floor failure, don't advertise the smaller interface.

**Verdict:** Conditional primitive candidates, not pilot nominations. I1 shows a finite recovery window rather than indefinite closure; I2 shows that no-show expiry and productive same-queue settlement are different. Neither proves naturally available continued teaching or a certification advantage. Prefer preservation-only service or priced timeout plus ordinary recertification if the proposed interfaces tie those controls after matching real work.

[triage]: https://github.com/manojbajaj95/cl/blob/d74d580d4cadcf7514a10ed23597142cba8ad7d1/reviews/flood-triage.md#L384
[its4]: https://github.com/manojbajaj95/cl/blob/d74d580d4cadcf7514a10ed23597142cba8ad7d1/reviews/flood-triage.md#L385
[ledger]: https://github.com/manojbajaj95/cl/blob/d74d580d4cadcf7514a10ed23597142cba8ad7d1/reviews/idea-ledger.md
[smooth]: https://github.com/manojbajaj95/cl/pull/113
[escrow]: https://github.com/manojbajaj95/cl/pull/214
[loan]: https://github.com/manojbajaj95/cl/pull/233
[menu]: https://github.com/manojbajaj95/cl/pull/235
[echo]: https://github.com/manojbajaj95/cl/pull/238
[momentum]: https://github.com/manojbajaj95/cl/pull/242
[renewal]: https://github.com/manojbajaj95/cl/pull/243
[rg]: https://arxiv.org/abs/2607.17536
[cbf]: https://arxiv.org/abs/1903.11199
[sagas]: https://doi.org/10.1145/38713.38742
