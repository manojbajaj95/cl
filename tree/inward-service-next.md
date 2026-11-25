# Inward service next: spend due old work to recover a right or make a future record settle

**Status:** Ideas only. The rational example is a paper check, not a pilot result. All proposed first tests are paper or CPU tests; no GPU.

**Parent:** [Inward service](inward-service.md) ([PR #281](https://github.com/manojbajaj95/cl/pull/281)). **Review seeds:** [Flood triage, #281 verdict][triage] gives score 3 to **#281#07**, choose among equivalent, naturally due A/C records to cross a lost swap boundary without adding work or projecting a gradient, and **#281#17**, use ordinary old service to put the residual inside a later own-queue record's settlement region when that record cannot settle either the drifted or undrifted branch alone. Follow the [idea ledger][ledger]: test old-task retention in every first test, and don't confuse reordered SGD with a new primitive.

## What has to be true

- **Recover by substitution, not extra training.** Freeze what counts as due and substitutable before seeing outcomes: supported old predictions, per-slice service progress tolerances, mandatory coverage, deadlines, and independent held-out old probes. Every candidate is selected from records actually available, runs the unchanged optimizer, and pays for any displaced record still owed. Recovery requires the full landing tube to be fixed by the opposite clip at execution precision, the other tail to stay active, and the claimed suffixes to pass. A timely partner may exercise only a live right; a future arrival cannot guide an earlier choice.
- **Settle by creating a precondition, not by declaring a timeout.** At no-show revoke the original swap ticket. A/C service can move the actual residual, but the genuinely later record from the opener's own B queue must produce useful learning and complete the wider forward suffix contract. No labels from the absent queue, selected-in-hindsight arrivals, rollback, or optimizer writes. Withhold and replace that later record as controls. Compare its action after the drift, before the drift, and after equally useful preservation-only A/C service. A late opposite partner needs fresh admission, even if the suffix menu now matches the joined menu.

**Shared falsifier.** For #281#07 compare fixed due order, same-progress [GradMatch][gradmatch] and [orthogonal gradient descent][ogd], and fresh exact selection over the same available pool. For #281#17 compare standalone inward recovery, standalone own-queue settlement, their best independent stack, [ITS4's frozen downstream damping][its4], and fresh exact forward recertification. For mixed cards include all these arms, priced expiry, and the [smooth/accumulation null][smooth]. Match raw arrivals, A/C work **and** delay and coverage, useful B gain per queue, checks, precision and peak bytes, or report the Pareto tradeoff. Count hazardous admits, honest refusals, and worst old slices on every exposed prefix and every claimed suffix. If a rule only improves the endpoint or borrows old work from after the deadline, it does not earn the right.

## Paper check: one old record, two different ways to finish

Use #281's `(x,y)`, `R,L`, drift `W`, and old gaps `A=2−x−d`, `C=2−y+d`. After `R→W` the three states are `(1,5/4),(−3/2,3/2),(0,0)`. A due old record `S` applies `y←(y+5/8)/2`; its less inward comparison `T` applies `y←(y+17/16)/2`. Both leave `x` unchanged. A later right-queue record `D` has truthful target zero for its own saturated prediction `p(y)=min(max(y−1,0),1/8)`. At the parent's learning rate `1/2` in `(h,u)`, SGD on `3p(y)²/4` gives `y←y−3(y−1)/2` for `1<y<9/8` and is flat outside; no input to `D` hits a kink.

After `S`, the repaired branch has `y=15/16` and the untreated tail `y=17/16`. A timely `L` fixes the first and repairs the second. On no-show, after revocation, `D` instead moves the untreated tail to `31/32`, reducing its own loss and leaving the right opener's hinge gain unchanged. Now `d=−1` clears C by `1/32`; `S` alone fails it by `1/16`. `D` alone has no effect on either the drifted or undrifted envelope; `T→D` leaves the tail at `41/32`; `D→S` leaves it at `17/16`. A/C stay safe at `d=0` in all these arms; both suffix signs are individually safe after either successful finish (the same right is not live on both finishes). This fixes the records in advance and separates settlement from expiry. It does not establish that `S,T` are interchangeable on real old work or that helpful `D` records occur naturally; the cards below make those separate tests.

## Idea cards

**P** = candidate primitive: the card proposes a reusable operation or certificate. **I** = improvement or audit, not a pilot nomination. Nearest-art comparisons are hypotheses to test, not a novelty clearance.

### Recover using real old-service choices (#281#07)

#### 01. A substitution table for lost swap rights — P, #281#07 seed
- **Mechanism.** For a due A/C obligation, record which available, interchangeable real batches put each observed landing cell inside the live swap entrance; use one ordinary update.
- **Novelty / control.** #268#04 gives fixed-order inward service; GradMatch/OGD can improve the direction. The proposed output is a safe admission, not alignment. Compare with fixed order, GradMatch, OGD and fresh exact selection.
- **Cheapest first test.** Give two real old views of one slice with matched old progress but different normal components to the hinge. Enumerate both; include a pool where neither crosses.
- **Old-task retention.** Check held-out old slices before the substitution, after it and after the opposite clip and suffix; charge the unused view if its own deadline still applies.

#### 02. Exchange two future service obligations without touching either gradient — P
- **Mechanism.** When only a batch currently assigned to another due obligation would recover the right, use an alternating reassignment of available records. Preserve a feasible matching for all remaining commitments after spending the first record.
- **Novelty / control.** Online matching handles feasibility; #281#07 uses a local substitute. The candidate is an exchange witness tied to the executed landing, with no double use. Compare with greedy repair and exact stateful scheduling.
- **Cheapest first test.** Use three obligations and three dual-eligible records; construct a now-safe crossing that strands an obligation unless two assignments are exchanged. Remove an edge as a refusal case.
- **Old-task retention.** Execute the whole reassigned schedule; score each covered A/C slice, including the one omitted by greedy repair, by its original deadline and after the swap.

#### 03. Borrow a crossing, then repay diversity in real records — P
- **Mechanism.** Use a lawfully repeatable view to cross now, but expose the temporary coverage deficit as a constraint on subsequent due views. A swap is admissible only if the next required A/C work can repay it without retracting the learned B gain.
- **Novelty / control.** #233 repays stability margin; coverage-aware replay tracks diversity. Here the liability is a specific displaced old view and runs against a live teaching right. Compare with no borrowing and a coverage-matched fresh check.
- **Cheapest first test.** One old slice has two repeatable views and one rare view; allow a one-slot coverage grace period. Delete the rare arrival in one arm.
- **Old-task retention.** Probe the rare view during grace and at its deadline as well as the common slice after B; don't treat recovery as payment of the old liability.

#### 04. Spend redundancy to remove the verifier's ambiguity — P
- **Mechanism.** Choose a due record whose executed map sends two indistinguishable full-state hypotheses into the same safe swap entrance. Admit without identifying which optimizer history actually occurred.
- **Novelty / control.** Belief-space control and #281#05 already handle hidden state. The new claim is that one *required* service record can eliminate the need to observe the hidden state; compare with slot observation plus exact repair and a fixed batch order.
- **Cheapest first test.** Hide the sign of a momentum component and enumerate two old-equivalent updates, one that lands both signs safely and one that succeeds on only one; include a third sign/magnitude outside the common basin.
- **Old-task retention.** Read A/C on both hidden histories at each prefix and after B, with no averaging over the harmful history.

#### 05. An outcome-contingent service exchange — P
- **Mechanism.** Precertify two second-slot choices keyed by the observed result of the first ordinary record. The result, not a future B arrival, selects the branch; both branches discharge identical old obligations.
- **Novelty / control.** #281#03 handles whole words and robust planning handles feedback. Require a branchable substitution policy that strictly beats every fixed word on the same due pool, not a larger input budget.
- **Cheapest first test.** Give the first record two bounded precision outcomes and the second slot two lawful views with opposite recoverable cells. Compare a closed-loop policy, best fixed word and fresh exact recertification.
- **Old-task retention.** Check both precision traces through every service prefix and the later clip, against the same A/C deadlines and held-out probes.

#### 06. A shared recovery certificate for different idle clocks — P
- **Mechanism.** Assign interchangeable due views by observed idle-clock class, so their executed updates deliver the same partner eligibility witness even though their slot values needn't agree.
- **Novelty / control.** #281#05 checks live state and #281#08 tolerates a missing slot. Test reuse of one permission proof across different clock-conditioned real actions, against separate full proofs and adding dummy ticks.
- **Cheapest first test.** Try a one-dimensional momentum slot after zero versus two mandatory idle ticks. Require the same suffix rights and a measurable check/byte saving; count refusal when the clock class was unseen.
- **Old-task retention.** Probe A/C during idles, after each actual update, and on a suffix sensitive to the live slot.

#### 07. Leave an independent old-service witness unspent — P
- **Mechanism.** Pair each repair batch with an independent due old reader whose next real evaluation can distinguish true retention from a blind spot in the chosen service class. Don't let the batch used for the crossing also certify its own coverage.
- **Novelty / control.** Held-out validation itself is standard. The proposed operation picks a *pair* of already due records that gives both a crossing and a discriminating observation with no separate audit batch; compare with random holdout and an equal-cost dedicated audit.
- **Cheapest first test.** Two repair candidates tie on the old selector but differ on a hidden subgroup. Give one later due reader that exposes the subgroup and one that cannot; freeze both before selection.
- **Old-task retention.** Score the hidden subgroup and ordinary old mixture at every actual seam; if the observer arrives late, test that the right stays suspended.

#### 08. Recovery that survives one other queue spending its slack — P
- **Mechanism.** Choose a due A/C substitute whose executed landing permits the intended swap even after one independently authorized, bounded B edit. Certify both legal placements of that edit rather than assuming the queues serialize.
- **Novelty / control.** Rely–guarantee already handles interference; #281#20 tracks transferable headroom. Test whether interchangeable old views can buy *joint* admissions absent from the intersection of separately repaired rights.
- **Cheapest first test.** Enumerate two old views, two local B pairs and one legal third-queue edit with shared normal direction. Compare separate certificates, the joint rule and fresh joint recertification.
- **Old-task retention.** Run all claimed interleavings and check A/C after the old record, independent edit, second clip and admissible suffixes.

### Create a settlement region for genuinely later work (#281#17)

#### 09. Precondition a later own-queue record — P, #281#17 seed
- **Mechanism.** An ordinary old record moves the residual into a later own-queue record's active settlement region. The latter, not the old step or timeout, earns a wider terminal menu.
- **Novelty / control.** #268#20 lets service itself buy a wider menu; ITS4 uses a frozen successor. Require the targeted interaction with later truthful same-queue work over the best independent stack.
- **Cheapest first test.** Use the paper check; add an unreachable settlement band and a preservation-only old record at the same old progress. Run neither, both singly, and both orders on drifted and undrifted starts.
- **Old-task retention.** Probe A/C at the old and B prefixes and test both terminal suffix signs separately, including failure before completion.

#### 10. Prepare a region for two unseen record types — P
- **Mechanism.** Prepare a reachable envelope in the overlap of two settlement preimages before knowing which own-queue type arrives. Each type improves its own truthful target and separately earns the same restricted terminal menu.
- **Novelty / control.** ITS4 freezes one successor; #281#10 avoids reservation. Require a single *executed* old step that enables multiple incompatible future types, versus a named-successor plan and type-blind priced timeout.
- **Cheapest first test.** Use two B gates with partly overlapping bands, then separate the bands and rerun the availability enumeration. Include no arrival and don't select the gate after seeing the old update.
- **Old-task retention.** Check every enabled type's A/C prefixes and terminal suffixes, plus the narrower menu when neither type arrives.

#### 11. Certify exactly which arrival classes remain useful — P
- **Mechanism.** Export a bounded-size partition of the frozen own-queue vocabulary into classes whose ordinary records settle, improve B without settling, or must be refused at the reached state.
- **Novelty / control.** #281#13 branches over continuations and #235 certifies menu replacement. Here a single service step changes the *type partition*, and that partition must predict unseen records more cheaply than rechecking them one by one.
- **Cheapest first test.** Use three record families with a shared public feature; hold out one member per family and include a feature collision with different executed action. Kill the compact partition if that collision requires full inspection.
- **Old-task retention.** Exercise safe and refused classes using their declared A/C menus; check the false-accept control against the vulnerable old reader.

#### 12. Settle by deleting the last blocker, not by gaining slack — P
- **Mechanism.** A/C service changes which old reader constrains a desired suffix without increasing the minimum old gap. The later B record improves exactly the newly exposed blocker while leaving the other old readers safe.
- **Novelty / control.** #281#20 types transferable headroom; #233 repays margin. Test whether a reader-identity precondition yields a safe suffix a scalar slack meter cannot distinguish.
- **Cheapest first test.** Construct two states with equal minimum gap but different binding readers; apply the same later record to both. Compare the tightest scalar test and a vector/exact check.
- **Old-task retention.** Record all per-reader gaps after each action and on the claimed suffix, with the reader whose deficit would be hidden by the scalar as a mandatory probe.

#### 13. Make settlement robust to who is next in the old queue — P
- **Mechanism.** Put the residue in a subset of the settlement region invariant under one intervening due old-service slot, using a real substitute now. The later own-queue record is still essential after either service order.
- **Novelty / control.** #268#04 recovers a swap; robust reachability handles dwell time. The target here is closure of a *later record's precondition*, not closure of the current swap right.
- **Cheapest first test.** Compare a shallow entrance with a deeper entrance at matched service progress under two possible next old batches. Include an unavoidable next batch that ejects both from the region.
- **Old-task retention.** Serve the intervening batch on time and check old floors after it, after later B, and after its terminal suffixes; no postponing it to protect the band.

#### 14. Move the settlement region using an old reader's real state — P
- **Mechanism.** A due record updates ordinary deployed reader state (e.g. a running normalization statistic), changing the preimage of a safe suffix under a later B update even at identical weights at the old seam.
- **Novelty / control.** #281#05 reads slots and #281#06 changes the reader. Require a settlement effect from normal reader-state evolution under the existing proof, not from relaxing the old reader. Compare with a frozen-stat arm and exact rechecking.
- **Cheapest first test.** Use a CPU model with one running mean and two batches tied on weight updates; hold the actual serving definition fixed. Show the later B update succeeds on only one reached full state.
- **Old-task retention.** Score both the updated reader and an independent old subgroup; check that a stale serving-state snapshot cannot incorrectly certify the suffix.

#### 15. An own-queue settlement region defined by gain on two records — P
- **Mechanism.** Target a region in which the arriving B record both improves its own example and keeps the opener's held-out B gain, while earning a new suffix. Outside the region the later record may fit itself by erasing the opener.
- **Novelty / control.** #281#14 keeps opener gain while retiring the tail; the proposed object is a reusable joint *preimage* of two B gain floors and an old suffix, not a repayment balance. Compare with constrained SGD and standalone settlement at equal gain.
- **Cheapest first test.** Give the opener and later record partly shared prediction directions. Include a branch where ordinary settlement appears to succeed only by forgetting the opener's view.
- **Old-task retention.** Probe A/C and the saved opener view at every seam and after the suffix; report the later record's own held-out gain separately.

#### 16. Stop preparing when the remaining arrival support makes settlement impossible — I
- **Mechanism.** Keep a sound outer bound on the preimages of not-yet-expired own-queue types. If no legal remaining old work can reach any of it, stop spending old-service flexibility on settlement and carry only the narrower contract.
- **Novelty / control.** #281#15 already studies impossibility and priced timeout. The incremental question is whether a legal support exclusion shortens wasted preparation versus a timeout-only controller without guessing future B.
- **Cheapest first test.** Enumerate a short declared arrival tree and remove one type at a genuine eligibility deadline; add a very late but still valid arrival to catch premature exclusion.
- **Old-task retention.** Execute the same old obligations after either decision, score blocked or admitted suffixes, and check A/C under the late-arrival trace.

### Combine the seeds without smuggling in a second slot

#### 17. A single substitution buys two contingent completions — P
- **Mechanism.** Find a due old-service alternative that enters both a recovered swap window and a future own-queue precondition. Branch on actual timely partner arrival: exercise the old right or revoke it and wait for later B; never exercise both on the same history.
- **Novelty / control.** #281#18 asks about a genuine choice; this card requires one interchangeable due record to offer both options causally where the best independently chosen recovery and settlement actions compete for that same slot.
- **Cheapest first test.** Give a pool with a swap-only record, a settlement-only record and a joint record at equal old progress; remove the joint record in a negative control. Compare the best causal stacked policy, not an oracle that sees arrivals.
- **Old-task retention.** Hold old work and deadlines fixed across timely join, no-show with later B, and no-show without later B; run A/C on each realized prefix and allowed suffix.

#### 18. Certify two choices remain after hiding the partner identity — P
- **Mechanism.** Pick the due substitution using only old observations and a frozen family of partner classes. Its certificate must bind admissibility to a recognized timely class; if no class appears, the same reached state still offers a lawful own-queue settlement path.
- **Novelty / control.** #281#04 hides future arrivals and ITS4 freezes the successor. Here the choice retains usable admissions across a partner family without seeing its member or copying its label into the own queue. Compare with individual certificates and exact fresh selection.
- **Cheapest first test.** Use two held-out partner types and an out-of-family one with the same public age; verify only covered arrivals exercise the old ticket and the latter is refused.
- **Old-task retention.** Check old readers in all covered branches, the false-class attempt and the no-show branch after its later record.

#### 19. Transfer the prepared precondition to a second old-service scheduler — P
- **Mechanism.** Hand off a bounded receipt containing the due coverage still owed, live swap predicate and prepared own-queue region. A second scheduler can act on new local arrivals without reading the original batch choice or learner trajectory.
- **Novelty / control.** #281#21 merges histories after completion; [order relays](order-relays.md) hand off prepaid teaching. Here the seam is *before* either finish, with both right revocation and old coverage still live. Compare with history transfer and fresh rechecking.
- **Cheapest first test.** Exhaustively pass two indistinguishable receipts to a new scheduler with one fresh due record; insert a slot alias that makes one continuation unsafe and demand a refusal or a larger receipt.
- **Old-task retention.** Carry A/C deadlines across the handoff and test the fresh reader, original held-out slices, and both terminal outcomes.

#### 20. An exchange-rate witness for old coverage versus future suffixes — P
- **Mechanism.** Before choosing the old substitute, return a Pareto menu: each increment in promised old coverage has a certified set of swap and no-show suffixes it can still buy, with actual records as witnesses rather than fractional batches.
- **Novelty / control.** #281#20 types geometric slack and standard multiobjective scheduling reports tradeoffs. A reusable witness should say what future *teaching rights* are impossible without sacrificing a specified old obligation; compare with a scalar price and full exact enumeration.
- **Cheapest first test.** Enumerate three coverage thresholds and two arrival futures, including a nonconvex middle point no scalar price selects. Check whether a compressed witness still predicts that point.
- **Old-task retention.** Keep all mandatory floors; report the named old slices at each optional coverage point and reject any claimed suffix that dips below its committed floor.

#### 21. A minimal evidence set for the joint decision — P
- **Mechanism.** Pick a subset of already due old measurements that distinguishes states needing different substitutions or no-show menus. States that share an observation cell must admit the same chosen action and have the same supported promised rights.
- **Novelty / control.** Observation minimization and #281#13's forked proof already exist. The claim is that one measurement subset can certify both decisions more cheaply than separate recovery and settlement evidence or a full state read.
- **Cheapest first test.** Enumerate four state aliases and two available old probes; build one probe that predicts swap eligibility but aliases opposite settlement outcomes, and test the cheapest safe joint partition.
- **Old-task retention.** Evaluate all aliases, including old slices not used as evidence, after the chosen action and after each enabled suffix.

#### 22. Test whether the gain vanishes when due work is fully matched — I
- **Mechanism.** Run the same causal policies on a kinked host, a smooth host and a tail-free host while giving accumulation and ordinary SGD the same exposed seams and opportunities for fresh exact admission.
- **Novelty / control.** This is the ledger's bounded-delay scheduling kill condition applied to both seeds; a positive result must survive equal completed old work, deadlines and useful B gain, not just equal update count.
- **Cheapest first test.** Tabulate safe admits, refusals and proof checks on one fixed arrival tree; include an oracle as a ceiling, not as a deployable arm.
- **Old-task retention.** Evaluate identical held-out A/C slices at each exposed seam and after claimed suffixes at matched B gain; count coverage losses and delay, not only final accuracy.

## Ranked deeper questions

1. **Does naturally redundant old service buy a real right without cherry-picking easy old work?** Start with 01, 02 and 22. Freeze eligibility and coverage on logged or generated arrival streams before scoring candidates; hold out old groups. Require a cross-boundary admission or lower proof cost than matched GradMatch/OGD and fresh selection. If real obligations rarely have substitutes that reach the boundary, report the availability limit.
2. **Does the preparatory effect survive unknown but naturally arriving own-queue records?** Start with 09–11 and 15. Freeze record populations and arrival traces; compare with ITS4 and the best stack. Require an actual new suffix and later-record gain while keeping the opener's gain. If success needs a constructed successor, the evidence remains a paper separation.
3. **Can one lawful decision retain both completions more often than the best causal stack?** Start with 17 and 18. Use identical raw arrival tapes for all arms, include empty intersections and late partners, and compare under live optimizer state and real idle ticks. A policy that needs to know the future or starves ordinary A/C work does not pass.
4. **Is any of this cheaper to certify than checking the actual state?** Start with 04, 19 and 21. Compare observation work, proof checks, receipts and reused admissions across shifts in readers and clocks. A hidden alias that forces full-state reads might leave a useful scheduling observation but no reusable certificate.

**Verdict:** The paper check separates a service-prepared, productive no-show from expiry and from the same later record in isolation. The open bets are whether honest due alternatives create that separation on actual arrival traces and whether a reusable certificate beats the best matched stack. If either collapses, prefer ordinary service with fresh admission checks.

[triage]: https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/flood-triage.md#L399
[ledger]: https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/idea-ledger.md
[its4]: https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/flood-triage.md#L385
[gradmatch]: https://proceedings.mlr.press/v139/killamsetty21a.html
[ogd]: https://proceedings.mlr.press/v108/farajtabar20a.html
[smooth]: https://github.com/manojbajaj95/cl/pull/113
