# Brain mechanisms IV: self-blind write meters

**Depth 3 · Ideas only; no experiments run, no GPU.** Parent: [Brain mechanisms III](brain-mechanisms-3.md) ([PR #318][parent]). Read the [idea ledger][ledger] first. The [PR #6 review block, rows 434–437][triage], records two score-3 seeds for #318 on row 436: **BM3-20** keeps a reservation when a write makes an old read disappear or become unobservable; **BM3-22** lets a contradiction nominate a diagnostic probe without granting permission to edit, prioritizing probes that distinguish competing claims on shared headroom. Neither was promoted to the top 10.

## What could become a primitive?

A write can damage an old behavior and make the damage harder to see. A subsequent probe might settle how much damage still needs to be reserved, which channels a new correction may touch, both, or neither. The question is whether one learner can **free only the headroom an observation actually justifies, without turning that observation into new write authority**. The converse matters too: a clean independent contradiction need not establish a harmless edit. Unlike [#317's independent falsification line][rival], the object here is headroom shared by competing corrections, not a verdict about whether one live write beats its frozen rival.

## Literature check and common first-test contract

I searched Hugging Face Papers for selective labels, active feature acquisition, and test-time settlement, then checked the titles and abstracts linked below on arXiv, including targeted lookups for close editing and online-learning baselines missed by broad search. The contrasts are hypotheses, not priority claims or implementation audits.

| Checked source | What is already known |
| --- | --- |
| [Learning under selective labels][selective]; [Performative Prediction with Selective Labels][performative] | Decisions can hide labels; selective observation can mislead retraining on a model-induced distribution. The latter uses robust objectives and bounds on hidden labels. Neither missingness nor worst-case imputation is a new primitive. |
| [TTT Settlement][settlement]; [CABA][caba] | Independently sourced text can gate a test-time update; held-out historical anchors can gate a candidate on worst-anchor policy divergence. Use both as controls where applicable, with identical anchor/label access. |
| [NMKE][nmke]; [AlphaEdit][alpha] | Attribution can drive dynamic sparse edit masks, and projection can preserve designated keys. Neither masked writes nor protection on known queries is the proposed contribution. |
| [Bandits with Replenishable Knapsacks][bwk] | Online allocation can handle nonmonotone resource consumption. Reserving and replenishing a scalar budget is not new; the question is what justifies a release when the write can change observability. |
| [BALD][bald]; [Disagreement-based Active Learning][disagreement]; [Robust Active Feature Acquisition][afa]; [Adaptive Submodularity][adaptive] | Information gain, disagreement, and sequential feature selection are strong baselines. Compare them on the same probe menu, and include decision-theoretic value of information (VOI) over feasible writes, not just predictive entropy. Greedy guarantees require structure; don't assume it. |
| [Doubly Robust Policy Evaluation][dr]; [Anytime-valid sequential inference][anytime] | Off-policy estimates can combine a logging policy and reward model; confidence sequences support repeated looks under their assumptions. Neither creates evidence on unsupported actions or licenses reuse of selectively disclosed outcomes without a valid model. |

- **Model the missing evidence explicitly.** Start with finite CPU tables or a two-route key–value learner. Freeze the public old read identity, severity, settlement rule, deadline and small pre-edit audit schedule. Distinguish no upstream arrival, observed successful substitution, missing outcome on an arrival, late outcome, and known harm. The live meter sees only its declared evidence; evaluator twins can reveal latent outcomes for falsification but never feed the policy. If upstream arrivals themselves are unobserved, bound or abstain; do not infer benign absence. A shadow outcome for a different action is not an observed counterfactual.
- **Separate safety, permission and accounting.** A reservation is unavailable headroom for unresolved exposure, not proof of incurred harm. Release can free unused capacity; it cannot erase known harm. A probe can settle a liability on a versioned read without authorizing modification; only independently grounded contradiction evidence can open a scope. Use executed deltas, check actual old-read floors where available, and treat incomplete outcomes as intervals rather than point estimates. For example, with capacity 3 and known debit 1, unresolved loss in `[0, 2]` leaves no guaranteed room; a valid upper bound of 1 frees one unit, even if there is no new write permission.
- **Give the simple stack the same information.** Compare BM3-20 + BM3-22 stacked with BM2-23 shared balances, BM2-07 frozen eligibility, exact per-read floors on observable endpoints, rolling validation, independent anchors/Settlement, random fixed-cost probes, and VOI over the joint admission decision. Use the [#313/#317 observability downgrade and observation-only switch][rival] where applicable, charging any report or intervention. Report matched cost in state, calls, published attempts and latency; exact causal enumeration with identical evidence is a small-world oracle, not a scalable baseline. Include true repairs, benign no-arrival, and harmful hiding. Compare useful corrections and ordinary service at a fixed retention tolerance; blocking everything is not a win.
- **Keep evaluation independent.** Before, during and after the proposed writes, test held-out A (unaffected old facts, near neighbors and ordinary task completion) and previously learned B, with results for the worst old slice. Score valid supersessions as new learning, not forgetting; separate missing and wrong old service and count both against completion. Keep these labels off the admission path. **P** = candidate reusable operation; **I** = improvement or discriminating control, not a reviewer verdict.

## BM3-20: settle an old read without letting a write redefine what counts

#### BM4-01 · Release only the part of a reservation the evidence clears — I
- **Mechanism.** Keep lower and upper bounds for unsettled loss, reserving the upper bound; a valid partial observation releases only the reduction in that bound. Known served harm has its own nonrefundable debit within the declared window.
- **Novelty vs nearest prior art.** [Performative Prediction with Selective Labels][performative] already optimizes against uncertain labels. This is the explicit robust-accounting control for BM3-20, not a claim that interval estimates are new.
- **Cheapest first test.** On a four-outcome read with one unit of existing debit, replay full, partial and no reports. Compare binary hold/release and robust admission from the same intervals; expect a tie with the latter.
- **Old-task retention check.** Keep both low- and high-severity A cases unforced; score known and hidden failures in held-out evaluation and recheck B after a second correction consumes released capacity.

#### BM4-02 · Let a receipt prove the observer was alive without pretending it saw the answer — P
- **Mechanism.** A precommitted neutral input and the old read share a versioned observation stage. A heartbeat from that stage eliminates only observer-outage explanations; an independently logged arrival without an answer keeps the substantive reservation. The heartbeat cannot originate on the write-controlled branch.
- **Novelty vs nearest prior art.** [Selective Labels][selective] addresses decisions that hide outcomes; [CABA][caba] compares outputs on fixed anchors. The candidate is a reusable witness about a *stage of the meter*, usable to distinguish who must bear unresolved capacity, not a proxy for correctness.
- **Cheapest first test.** Cross no arrival, common-stage outage and selective skip in a three-state router. Compare unconditional audits and per-stage availability logging at equal calls and bytes; drop if normal availability bits make identical decisions.
- **Old-task retention check.** Measure unforced old completion and old fact accuracy including requests that see a healthy heartbeat but are dropped, plus earlier B during a true outage.

#### BM4-03 · Carry unsettled loss across a meter replacement — P
- **Mechanism.** During an overlap between old and new reporting schemes, collect a translation from new reports to *bounds* on the original loss. Move outstanding reservations only if the translated bound is conservative for every old outcome still possible; if a rare subtype is ambiguous, retain its portion under the old scheme.
- **Novelty vs nearest prior art.** [CABA][caba] checks anchors in comparable representations; [selective-label bounds][performative] tolerate missing truth. The proposed handover preserves outstanding exposure through a change in outcome granularity. Compare keeping old instrumentation and exact joint observation where available.
- **Cheapest first test.** Replace a three-level old error report with a binary completion flag after two arrivals. Supply or withhold one overlap outcome that separates mild from severe harm; compare against continuing both meters at equal reporting cost.
- **Old-task retention check.** Score severe rare A errors under the original definition, plus A near neighbors and B after the old reporting path shuts down.

#### BM4-04 · Release a reservation by proving no request owed service — P
- **Mechanism.** Accept a trusted upstream closure of a preregistered request slot as evidence of zero *service exposure* for that slot, without treating it as evidence of intact competence or clearing outstanding debit from other slots.
- **Novelty vs nearest prior art.** [Performative Prediction with Selective Labels][performative] distinguishes model-dependent populations from selective labeling. The narrow candidate is a slot closure that frees exposure capacity but cannot relax a competence floor. Compare a fixed upstream denominator with independent anchor gating.
- **Cheapest first test.** Give two finite streams identical empty downstream logs; only one has an authentic upstream no-arrival record. Inject a stale closure for a different slot. Drop if independent denominator and anchor checks recover the same useful admissions.
- **Old-task retention check.** Test A including the retired slot's still-valid inputs out of band, normal completion on occupied slots, and B after reuse of the service capacity.

#### BM4-05 · Reuse a witness only for the versions it actually covers — P
- **Mechanism.** Bind each report to the model version that served the old request, not the version that ingests the label. Pool delayed reports across versions only when an independently checked equivalence preserves the executed action, relevant context and outcome semantics for that old slice.
- **Novelty vs nearest prior art.** [Doubly Robust Policy Evaluation][dr] adjusts for logging policy differences; [TTT Settlement][settlement] uses fresh independent evidence. The candidate is a loss-preserving equivalence that lets delayed evidence discharge a debt across updates; ordinary version tagging is a mandatory control.
- **Cheapest first test.** Delay a single label through three versions: two share the same relevant action and a third changes an unlogged side effect. Compare per-version ledgers, naive pooling and full-context tagging at equal bytes; fail if the compact equivalence cannot reject the side-effect case.
- **Old-task retention check.** Score A by serving version, including the rare side-effect path, and B after delayed intake and later publication.

#### BM4-06 · Permit joint release without pretending to know which write was harmless — P
- **Mechanism.** When a trustworthy aggregate bounds the sum of several reservations, record a family-level limit against the shared read without clearing individual claims. Do not transfer that limit to another read that sees only one of the writes unless the bound remains valid there.
- **Novelty vs nearest prior art.** [BWK][bwk] supports pooled resources and [selective-label bounds][performative] support aggregate risk. The bet is reuse of a joint bound under safe projections across overlapping old-read accounts; exact feasible-set accounting with the same aggregate is the ceiling.
- **Cheapest first test.** Two unresolved slots each allow one unit, but a joint report certifies at most one unit total. Add a second account covering only the first slot. Compare independent upper bounds, an indiscriminate release and an exact tiny constraint solver. Drop if the compact form cannot match the oracle with less state or computation.
- **Old-task retention check.** Measure old outputs on both jointly covered A and singly covered near neighbors separately and previous B after the next published edit.

#### BM4-07 · Make expiry remove exposure, not the need for evidence — P
- **Mechanism.** End a tentative write's live exposure at its deadline by reverting or disabling that write; keep unresolved *past* exposure reserved until legitimate settlement or the preregistered accounting window ends. Track the distinct deadline to resume service under a demonstrably safe version.
- **Novelty vs nearest prior art.** [BWK][bwk] models replenishment and [TTT Settlement][settlement] gates before commitment. Compare rolling limits plus fixed expiry; the only candidate delta is stopping prospective harm without losing the claim on past unverified service when delayed evidence competes with new writes.
- **Cheapest first test.** Use a two-stage router where a late old outcome arrives after withdrawal while the next candidate waits. Include a late revealed failure. Drop if expiry plus a separate rolling account fits the same feasible schedule.
- **Old-task retention check.** Score old completion before expiry, during fallback, and after new service begins; recheck earlier B so fallback is not a free reset.

#### BM4-08 · Price what the meter fails to cover before using its silence — I
- **Mechanism.** Estimate an upper harm bound on the observable fraction using valid sequential inference, then add the maximum permitted loss on the noncovered fraction. Fix the denominator upstream and expose when neither part is identifiable.
- **Novelty vs nearest prior art.** [Anytime-valid inference][anytime] and [selective-label bounds][performative] already supply the pieces; this is a benchmark for more elaborate release rules, not a statistical invention.
- **Cheapest first test.** Enumerate route-stratified streams with equal observed success but different precommitted coverage, and repeat the decision at every arrival. Compare exact finite-world bounds and a naive interval that conditions only on disclosed labels. Include nonrandom missingness.
- **Old-task retention check.** Score A separately on covered and uncovered routes in the evaluator and B after the first extra committed edit, with the worst subgroup shown.

#### BM4-09 · Make the next replacement repair the meter before spending its balance — P
- **Mechanism.** Treat demonstrable restoration of an observation path as a prerequisite for a candidate that needs disputed headroom. Accept restoration only on a held-out ordinary old request where output and action are unchanged relative to the proposed service, or else judge it as a service intervention too.
- **Novelty vs nearest prior art.** [#317's observation-only switch][rival] separates reporting from treatment and [CABA][caba] gates on anchors. The candidate is a sequencing rule: meter restoration can unblock another change but never deposits headroom merely by emitting more reports.
- **Cheapest first test.** Give a router a reporting-only repair and a look-alike that also changes service; give both identical receipt volume. Compare a switched reporter plus fixed floor and exact joint checks at matched cost. Require real loss settlement before the competing write.
- **Old-task retention check.** Score normal A routing, action and completion with the restored meter active, and past B through the eventual weight commit.

## BM3-22: give the probe a job other than granting an edit

#### BM4-10 · Ask which debit would bind, not which explanation is most likely — I
- **Mechanism.** For each probe outcome compute the set of independently eligible writes affordable on every compatible old-read account; rank probes by attainable gain at that set, not posterior confidence in a causal story.
- **Novelty vs nearest prior art.** [BALD][bald] scores information gain, while decision-theoretic VOI already scores downstream decisions. This is the joint VOI control BM3-22 must beat, not a proposed novelty claim.
- **Cheapest first test.** With a one-label budget, offer a high-entropy probe on a slack read and a low-entropy probe that can flip admission at the tight read. Include an already decided case where neither probe is worth its cost.
- **Old-task retention check.** Test both old A reads and held-out neighbors before and after the selected edit, and measure earlier B even when no probe is chosen.

#### BM4-11 · Issue a negative scope receipt that is still useful to the scheduler — P
- **Mechanism.** If a probe can rule one channel out of the eligible set but cannot positively establish origin for any other, return a negative receipt only. Cancel unused *prospective* claims made exclusively for the excluded candidate; neither incurred harm nor pending exposure gets credited back.
- **Novelty vs nearest prior art.** [NMKE][nmke] prunes masks; [disagreement-based active learning][disagreement] can eliminate hypotheses. The proposed receipt separates invalid eligibility from unpaid past exposure so that independent contenders can reuse only the unspent reservation.
- **Cheapest first test.** Two corrections wait on one read; eliminate a channel for one correction with a single independent observation. Contrast full fresh attribution, a binary authorization bit and exact joint VOI at equal cost. Include a reservation shared with a still-eligible candidate that must not release.
- **Old-task retention check.** Check A on the excluded and still-eligible neighborhoods, and earlier B after only the independently authorized contender commits.

#### BM4-12 · Compare probes by their least helpful admissible outcome — P
- **Mechanism.** A claimant may not reserve the last probe call based solely on a favorable expected report. Reserve it only if every feasible response either changes the safe write set, retires a blocked claim, or yields a preregistered reduction in worst-case future exposure sufficient to pay for the call.
- **Novelty vs nearest prior art.** [Adaptive Submodularity][adaptive] studies adaptive selection and [performative robust risk][performative] uses worst-case outcomes. Compare robust VOI directly; any candidate gain must come from reuse of the all-outcome certificate across competing claimants, not the maximin criterion.
- **Cheapest first test.** Enumerate two competing probes and a rare nonresponse; contrast expected and robust joint VOI, and reuse the certificate after one claimant withdraws. Reject if reuse is stale or cannot save a re-evaluation.
- **Old-task retention check.** Score ordinary old A under the unhelpful response, not just the favorable branch, and previous B through the resulting delay.

#### BM4-13 · Borrow a probe right without borrowing a write right — P
- **Mechanism.** Allow a second candidate to claim a pending probe's read-only result when both registered the same version, public read, question and valid outcomes. Recompute each candidate's independent write authority separately; the probe cannot share an origin claim merely because the two candidates bill the same read.
- **Novelty vs nearest prior art.** [Robust Active Feature Acquisition][afa] acquires observations under cost, and [BALD][bald] updates beliefs from each observation. The bet is a coalescing rule for independently queued claimants with unequal write scopes and deadlines, versus ordinary cached-feature lookup with access checks.
- **Cheapest first test.** Queue two sparse edits that ask for the same old label but need different channel evidence; then insert a version change before response. Compare individual probes and memoization keyed by the full observation contract at matched bytes; drop if the latter ties.
- **Old-task retention check.** Evaluate held-out old A for both scopes and prior B after the permitted edit; confirm the ungrounded contender has not modified its channels.

#### BM4-14 · Keep a probing action legal when its report could be unsafe to use — P
- **Mechanism.** Distinguish a legal observational call from permission to use its result: a response can reduce a read's loss interval while remaining ineligible for attribution if its source is downstream of the candidate's own previous delta. Certify each use against a declared provenance dependency separately.
- **Novelty vs nearest prior art.** [NMKE][nmke] selects edit support dynamically and [TTT Settlement][settlement] insists on independent evidence for commitment. The candidate is a dual-use receipt that settles measurement without laundering authorization, compared against two completely separate evidence pipelines allowed to share raw logs.
- **Cheapest first test.** Have an independent auditor grade an executed answer that traveled through an edit-recruited channel. Use the grade to settle that version's loss but withhold scope expansion because the grade does not establish the channel's pre-edit role. Compare blanket rejection and independent pipelines at equal cost; add a genuine independent scope witness as a positive control.
- **Old-task retention check.** Score old A through the edited and unedited channels and earlier B after settlement, before any unrelated permission is granted.

#### BM4-15 · Let an unpaid contradiction nominate a future ordinary measurement — P
- **Mechanism.** Register a bounded, expiring selector before a relevant ordinary query arrives; let the first eligible arrival use the probe quota instead of issuing an extra request now. The selector is frozen, can return no report, and cannot become an edit trigger by itself.
- **Novelty vs nearest prior art.** [Disagreement-based Active Learning][disagreement] already decides which stream labels to request. Compare it with per-claim deadlines and joint VOI; the candidate delta is a reserved opportunity reusable by competing writers without changing service demand.
- **Cheapest first test.** Enumerate sporadic arrivals, clustered arrivals and an absent distinguishing subtype. Compare immediate probing, an online query-by-disagreement baseline and earliest-deadline scheduling with identical visibility and call cost.
- **Old-task retention check.** Measure old A completion during the wait, rare neighbor accuracy when an arrival does occur, and earlier B after the selector expires or fires.

#### BM4-16 · Refuse a probe whose observation would change the thing it measures — I
- **Mechanism.** Classify each call as passive or an intervention on service or on future eligibility. If it changes either, do not use it to clear a normal-service reservation without an explicit transport argument or separate randomized treatment comparison.
- **Novelty vs nearest prior art.** [Doubly Robust Policy Evaluation][dr] already distinguishes executed actions from counterfactual policy value; [#317][rival] proposes an observation-only switch. This is a validity control, not a new estimator.
- **Cheapest first test.** Contrast a passive logger with a “probe” that forces a dormant channel and changes subsequent routing. Include a no-effect logger. An evaluator twin checks that forced success was not available on ordinary service.
- **Old-task retention check.** Test A under ordinary routing before and after the call, report intervention-only results separately, and score previous B on the next unforced request.

#### BM4-17 · Use a probe to show two candidates cannot both be admitted — P
- **Mechanism.** Seek an observation that certifies a pair is jointly unaffordable despite being separately authorized and individually affordable. Cache the certificate against the specific shared read, effect bounds, and active reservation versions; an independent repair can invalidate it.
- **Novelty vs nearest prior art.** [BWK][bwk] handles resource contention and [AlphaEdit][alpha] protects designated keys. The candidate is an observation-derived incompatibility witness that can prune future batching when read interactions are nonadditive, not a static sum limit.
- **Cheapest first test.** In one hidden router state, two disjoint channel deltas jointly cross an old-route threshold; in the other they don't. A read-only measurement identifies the threshold regime without publishing the pair. Compare additive accounting, exact pair preflight and a fixed conflict graph at equal evaluations; include a legitimate repair that removes the interaction.
- **Old-task retention check.** Measure A at each served prefix and after the allowed pair in the repaired world, plus B after refusal and after repair.

## Joint descendants: when observing and spending interact

#### BM4-18 · Check whether the first write destroys the only useful second probe — P
- **Mechanism.** Before publishing a valid contender, evaluate whether it removes the available observation that would settle a competing old-read liability. Defer the first write only when a still-lawful probe before publication can change the feasible next write set, accounting for delay and probe cost.
- **Novelty vs nearest prior art.** [Adaptive Submodularity][adaptive] studies adaptive observation choice; [TTT Settlement][settlement] checks an individual write before commit. The proposed scheduling edge is from a write to another claimant's future ability to free shared headroom. Exact joint lookahead is the control, not a novelty claim.
- **Cheapest first test.** Exhaust all orderings of two writes and one ordinary observable event. Include an order-invariant probe and a beneficial first write whose delay outweighs the second. Compare myopic stacked admission and optimal finite-horizon joint VOI.
- **Old-task retention check.** Score both old A neighborhoods through the delay, probe and publication, and previous B when the earlier deadline wins.

#### BM4-19 · Shrink a candidate until the meter can still tell on it — P
- **Mechanism.** Choose the largest tested interpolation that satisfies both the observed old-read floor and a lower bound on the ability to detect unresolved severe old errors after publication. The distinguishability check must include both correct and harmful outcomes, not merely whether the logger emits something.
- **Novelty vs nearest prior art.** [CABA][caba] already chooses the largest tested interpolation within a retention budget. The extra constraint protects future observability under the same progression; compare CABA stacked with an independent visibility gate over the identical grid.
- **Cheapest first test.** Construct a linear edit changing a routing threshold, where the exact audit anchor keeps its label but a different old subtype loses a decisive receipt at high interpolation. Include a truly beneficial path switch. No monotonicity assumption; enumerate the small grid.
- **Old-task retention check.** Evaluate A on both sides of the threshold using normal routing and previous B under the selected fraction; report new-task gain lost by interpolation.

#### BM4-20 · Reserve diagnostic capacity for the old read a write could blind — P
- **Mechanism.** In addition to potential harm, require a candidate that may occlude an old meter to reserve a specific affordable fallback observation, with independently checkable reachability before expiry. A different claimant may spend that probe slot only if the original liability still has an adequate route.
- **Novelty vs nearest prior art.** [BWK][bwk] can model a second scarce resource, and [robust feature acquisition][afa] budgets measurements. The candidate is a contingent link between the two resources: the probe must distinguish that read's unresolved outcomes, not merely exist.
- **Cheapest first test.** With two writes, two old reads and one standby probe, compare a generic two-budget knapsack, fixed per-read quotas and exact joint scheduling. Include a cheap probe with no discriminatory power and a reverse ordering in which the reserved probe stays reachable.
- **Old-task retention check.** Measure A on both old reads when the fallback is needed and when unused, plus earlier B under any delayed or refused write.

#### BM4-21 · Transfer a pending claim only when the new witness dominates the old one — P
- **Mechanism.** In the deterministic first test, substitute an ordinary observation for a scheduled audit only if the audit result relevant to this liability can be recovered from each possible substitute result on the registered worlds. The substitute does not inherit permission evidence unless it separately satisfies that contract.
- **Novelty vs nearest prior art.** [Adaptive Submodularity][adaptive] already studies redundant observations. The proposed comparison is a liability-specific substitution rule under scarce probes, retaining eligibility boundaries. Compare full decision-theoretic experiment comparison at the same cost.
- **Cheapest first test.** Enumerate two observation maps, one refining old severities and one hiding the worst case behind completion. Add a new write that flips which map dominates for a slice; reject stale substitutions.
- **Old-task retention check.** Test old rare severe A, an unaffected neighbor and earlier B after the borrowed audit slot is spent on another contender.

#### BM4-22 · Allow two partial receipts to settle one debt only with compatible provenance — P
- **Mechanism.** One report can identify the executed old route, another its outcome. Release the reservation only when they identify the same predeclared event and their observation-stage contracts compose; a join on entity name alone cannot settle harm.
- **Novelty vs nearest prior art.** [Doubly Robust Policy Evaluation][dr] starts from logged context, action and reward; reconstructing that tuple is standard. The contender is a compact join certificate that survives one write changing the report boundary, against a complete event-ID log with schema and version checks.
- **Cheapest first test.** Two repeated requests use the same entity and different routes. Swap delayed outcomes and insert a version boundary. Require the compact certificate to match full logging on safe admissions while using less persistent state or fewer calls.
- **Old-task retention check.** Measure A on repeated invocations, including the wrongly paired rare failure, and previous B following delayed settlement.

#### BM4-23 · Keep sums within the same possible world — P
- **Mechanism.** An outcome may tighten the bound on existing exposure in just one compatible world. Retain that conditional bound and add a candidate's next exposure in the same world before taking the maximum. Independently require permission in every remaining world; no claimant can choose its favorite world to gain authority.
- **Novelty vs nearest prior art.** [Performative Prediction with Selective Labels][performative] already uses worst-case labels. The candidate object is a reusable branch-indexed obligation that avoids summing incompatible maxima while leaving authorization independent. Exact robust optimization over the same joint worlds is the ceiling.
- **Cheapest first test.** With capacity 2, give the first world existing exposure bounded by 2 and new exposure 0, and the second existing exposure bounded by 0 and new exposure 2. Compare summing separate maxima, exact robust joint admission and a compact branch ledger. Include a candidate that goes over 2 in only one world and one not independently authorized in that world.
- **Old-task retention check.** Measure A and previously learned B under both worlds at equal useful new-task gain; no averaging away the violating branch.

#### BM4-24 · Disallow a write that “pays” by changing the old loss definition — P
- **Mechanism.** Freeze the old task's success predicate outside the learner. Accept a semantic migration only with independent evidence of the new legitimate obligation and a mapping of still-valid old obligations. Treat incompatibilities as unresolved, not automatically as retirements or known harm.
- **Novelty vs nearest prior art.** [CABA][caba] fixes anchor divergence and [AlphaEdit][alpha] preserves selected knowledge. The candidate is a checked migration of live behavioral liabilities with no self-supersession, compared against immutable old outcome definitions plus an externally versioned registry.
- **Cheapest first test.** Mix a genuine policy change with a write that normalizes wrong old answers into the success class. Use the smallest table with one legitimately superseded item, one retained historical variant, and a missing receipt. Drop if a fixed external registry ties.
- **Old-task retention check.** Score A on the valid historical variant and unaffected neighbors, past B under the same predicates, and the intended supersession separately as new learning.

#### BM4-25 · Ask what a meter-preserving no-weight substitute could have done — I
- **Mechanism.** Pre-register a frozen-weights correction via an independently routed lookup, then measure whether the weight edit needs extra old-read reserve because it suppresses meter evidence the substitute retains. Charge both routes for lookup, labels and publication latency.
- **Novelty vs nearest prior art.** [#317][rival] explicitly proposes a cheap no-write rival, and [TTT Settlement][settlement] tests independent improvement. This is the relevant comparison for the *settlement cost*, not a new reason to use retrieval.
- **Cheapest first test.** Compare a one-key lookup with a weight edit at equal new accuracy, then include a context-dependent correction lookup cannot implement under the same bytes. Drop any claimed meter advantage if matched routing makes it vanish.
- **Old-task retention check.** Test A and previous B under both ordinary serving paths, including delay and wrong or missing old service while the correction stays active.

#### BM4-26 · Find the smallest separating observation before designing a new meter — I
- **Mechanism.** Enumerate pairs of worlds identical on the live evidence but where the next write is safe in only one. List the cheapest lawful observation that distinguishes the pair before one deadline, and mark pairs with no such observation as a limit rather than tuning a more aggressive gate.
- **Novelty vs nearest prior art.** [Disagreement-based Active Learning][disagreement] already targets distinguishing labels; [selective labels][selective] already warns about partial blindness. This extends the parent's BM3-26 audit specifically to *write-induced loss of the separating observation*.
- **Cheapest first test.** Use two writes, a hidden old label, and three probe times (before, during and after suppression). Compare exact causal policies at the same evidence and call budget against evaluator-only full information. Include an always-observable positive control.
- **Old-task retention check.** Report A and previous B in both twin worlds and the useful-service cost of abstention in the safe one.

## Ranked deeper questions

1. **Can one cheap observation safely free shared old-read headroom without opening a write scope?** Start with BM4-01/06/14/23, with partial reports, correlated liabilities and independent scope evidence. Require more useful published corrections at the same exposed-prefix A and B retention than exact observable floors + a robust shared ledger + independent authorization. If exact joint admission wins only by receiving extra labels, don't credit the mechanism; if the simple stack ties on equal evidence, keep the stack.
2. **When does a legitimate write destroy the last affordable observation another write needs?** Use BM4-18/20/26 to compare all small causal schedules and an order-invariant control. Identify a nontrivial interval of deadlines and costs where the dependency affects admissible writes, not merely a simulator that makes probing first win by construction.
3. **What is the cheapest evidence that silence is benign rather than self-blinding?** Pair BM4-02/04/09 with no-arrival, honest reporting outages and selective hiding. Report which cases require independent ingress or a reporting-only switch. If a fixed audit plus upstream denominator suffices at equal cost, do not add a meter protocol.
4. **Which receipts remain valid after a version, route or outcome-schema change?** Use BM4-03/05/21/22 against full event and version logging. Require lower observation cost or telemetry state at unchanged safe admissions, including rare old outcomes that break apparent equivalence.

[parent]: https://github.com/manojbajaj95/cl/pull/318
[ledger]: https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/flood-triage.md#L434-L437
[rival]: https://github.com/manojbajaj95/cl/pull/317
[selective]: https://arxiv.org/abs/1807.00905
[performative]: https://arxiv.org/abs/2610.08272
[settlement]: https://arxiv.org/abs/2610.05076
[caba]: https://arxiv.org/abs/2610.40740
[nmke]: https://arxiv.org/abs/2510.22139
[alpha]: https://arxiv.org/abs/2410.02355
[bwk]: https://arxiv.org/abs/2306.08470
[bald]: https://arxiv.org/abs/1112.5745
[disagreement]: https://arxiv.org/abs/1904.09056
[afa]: https://arxiv.org/abs/2107.04163
[adaptive]: https://arxiv.org/abs/1003.3967
[dr]: https://arxiv.org/abs/1103.4601
[anytime]: https://arxiv.org/abs/2009.03167
