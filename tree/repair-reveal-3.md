# Repair-reveal III: make evidence arrive before the last usable slot

**Status:** Ideas only. First tests are paper or small CPU proposals; no learner runs or GPU work. **Parent:** [Repair-reveal next](repair-reveal-next.md) ([PR #297][parent]). **Review seeds:** [Flood triage, row 415][triage] on [PR #6][review] scores **#07**, relay a separator through the next compulsory C record without granting anything in between, and **#20**, finish otherwise missed service in a one-record window between independent borrower waves. Both seeds are baselines, not new cards.

**Ledger read first:** [Idea ledger][ledger]. Don't credit a threshold put into the learner by construction, a Gramian surrogate in place of executed finite continuations, or a tie with replay, save/restore, or a matched stack. **P** denotes a candidate reusable operation or object; **I** denotes an improvement or audit, not a pilot recommendation. Nearest-art comparisons are scoped hypotheses, not priority claims.

## Contract and shared controls

- A is original work, B is installed work including existing backing and pinned borrowers, and C is installed and incoming successor work. Pin due menus, coverage, ordinary reports (including timestamps, if exposed), discrete updates, arithmetic, deadline and arrival support before blind arrivals. A repair must do genuine assigned work; charge displaced records, reports, checks, planning, and carried bytes. A private optimizer coordinate is not a public observation. No spend, host commitment, or invisible reservation for reuse before the requisite report.
- At the grant cut use the complete legally available public history. Protect against all reachable histories and joint calls compatible with it, not just marginals or one realized trace. Commit only when one causal policy covers the new service and every remaining old liability; the policy may react to later public arrivals. A grant counts only when additional useful work finishes by deadline, including any durable commit or acknowledgment specified by the job. Record late, canceled and refused work; charge any carried partial job and its remaining claims.
- **Relay controls:** immediate repair/reveal ([#289 #05][steps]), [useful-batch check][useful], paid report carry, dedicated probe at equal compute, and a separate audit. Include a compulsory C continuation that overwrites the carrier. **Bridge controls:** [#289 #18][steps], never-release, equal-size reserved standby, first-come release, and a window with no feasible on-time completion. Include one-tick shifts in deadline and observation delivery. Give the best repair + lawful audit + exact correlated scheduler the *same* native reports and actions, including the candidate's schedule as a diagnostic arm. Exact same-information planning is a ceiling. Any claim beyond changing the selected record needs a binding resource it genuinely saves.
- Match per-queue progress, byte- and width-steps, precision, stream coverage and starting retention floors, or report the tradeoff. At each test run independent held-out A, already installed B (repaired path and unaffected old callers), and installed C before intervention, while evidence is pending, at the spend/refusal, and after blind reuse. Check misses by obligation and cohort, not just mean accuracy; a stranded old caller fails an arm.

## Paper fixture: one bit at the only usable cut

Use unit-step subgradient descent on `(x,y,z)`, with `x=z=0`, `y∈{0,1/4}` and public report `1[z≥0]`. At tick 1 choose one of two already-due C records with loss `(x−1)²/2+|y−t|/8`, `t∈{−1,+1}`; the other stays due after the bridge. Both set `x=1` with equal served-record loss decrease. With `t=−1`, the two possible `y` values become `−1/8,+1/8`; with `t=+1`, they become `+1/8,+3/8`. The tick-1 report is 1 in all cases. The compulsory tick-2 C record has loss `|z−y|/32`; it moves `z` to `sign(y)/32`, with equal served-record loss decrease in all four cases. Only `t=−1` separates the two histories. A continuation that erases `y` without touching `z` cannot separate them.

After the tick-2 report there is one service slot with three units. The repaired B route, served by its original backing up to this cut, now serves directly via `x=1`. In the lower initial-`y` history exactly one of two pinned B callers requests a unit; in the higher one either both or neither can call. A blind job needs two units in that slot to finish by deadline. Only report 0 from the separating arm can back it: reserve one unit for whichever B call arrives. In report 1 of the separating arm, or the pooled report of the other arm, reserve two. Tick 1 grants nothing, and a separate check delivered one tick later misses the deadline (the next independently owed wave already needs two units). Toy old reads can require `|y|≤1/2` for A and `|z|≤1/16` for installed C; both hold on these cuts. This is a worked service fixture, not evidence that a learned host keeps old tasks, and the exact same-report scheduler can reproduce the result.

## A. Get the right information to the grant cut

### 01. Let the compulsory record choose the question at read time (P; #07)
- **Mechanism:** Plant a carrier supporting two different liability predicates. The type of the next actually due C record, revealed only after the repair, determines which predicate its ordinary gradient reads out. Bind the eligible claimant class to that type before any grant.
- **Novelty vs nearest prior art:** [Coding for Computing][coding] uses decoder side information; here the side information is a compulsory write that evaluates one of several predicates in the live state, not a tag sent to an external decoder. Compare an equal-byte conditional code plus a native check.
- **Cheapest first test:** Four reachable states encode two bits; two blind due-record types each move one bit into the same one-bit report. Enumerate both request classes; a carrier optimized for either class alone must refuse some safe requests.
- **Old-task retention:** Serve the unqueried B class as well as the queried class; run the original A and installed C reads under both due-record types.

### 02. Separate by when an ordinary report first changes (P; #07)
- **Mechanism:** Use the first legal threshold-crossing time as evidence when all terminal bins coincide. Accept only if rounding and report jitter still separate the two sets of *possible* crossing times before the last grant cut.
- **Novelty vs nearest prior art:** Event-triggered sensing already encodes time, and [#297 #03][parent] guards against report delay. Here required writes induce the event time and a terminal report alone is provably useless. Compare a timestamped passive audit using the same clock and bytes.
- **Cheapest first test:** Enumerate three mandatory scalar updates with two histories both ending in bin 1, but first entering it on ticks 1 and 3. Add one tick of delivery delay; then add enough jitter to force refusal.
- **Old-task retention:** Execute pinned B and held-out A/C on the intermediate ticks as well as after the common terminal bin.

### 03. Cancel an unknown report offset with two native reads (P; #07)
- **Mechanism:** Arrange for the next two compulsory records to read the carrier with opposite signs. Authorize on the difference of the *rounded* reports, not by assigning meaning to either report alone.
- **Novelty vs nearest prior art:** Differential measurement cancels common-mode offsets; [#297 #06][parent] protects one coarser future read. The candidate uses the ordinary gradient order as the actuator for a nuisance-canceling read pair. Compare a paid reference reading and the best same-report differencer.
- **Cheapest first test:** Enumerate a bounded unknown offset, both carrier signs, and all rounding ties. Require overlapping single-report sets but disjoint difference sets; change the offset between reads as a negative.
- **Old-task retention:** Serve B from original backing between reads and run A/C under both offset extremes, including the drift-induced refusal.

### 04. Backchain from the deadline through an adversarial due menu (P; #07)
- **Mechanism:** Label a repair by whether every legal next-record branch leaves some causal path to a grant decision by deadline. Use a backward set on *pairs of still-aliased histories*, allowing the surviving carrier coordinate to differ by branch.
- **Novelty vs nearest prior art:** Active fault diagnosis already chooses inputs to separate modes. This would synthesize a retention-constrained certificate over required learning continuations that the diagnoser cannot select. Compare exact belief-state planning and the single-overwriter guard from [#297 #07][parent].
- **Cheapest first test:** Enumerate two due orders and two hidden modes. One repair survives both orders via different coordinates; another wins the favored order only. Add a due order erasing both coordinates.
- **Old-task retention:** Run old A/B/C on the unfavorable order and on the extra order where no grant is possible, not only on certified branches.

### 05. Commute on the final state, disagree at the read cut (P; #07)
- **Mechanism:** After a repair, order two required C writes whose composition on the live state is the same in either order. Only one exposes an actionable intermediate report; consume it at that cut before the second update reconciles the paths.
- **Novelty vs nearest prior art:** Active diagnosis normally compares discriminating input sequences; [#297 #07][parent] carries a separator through one follow-on update. This asks for a trace difference under *exactly equivalent* final optimizer state and work coverage, isolating evidence from lasting changes to repair yield.
- **Cheapest first test:** Search commuting two-coordinate updates with a fixed lossy reader. Compare both permutations and paid intermediate probes; reject a fixture where the order changes any final slot or where the intermediate evidence arrives after the only legal cut.
- **Old-task retention:** Run B against both intermediate states and old A/C after each write; matching final weights alone cannot excuse a missed intermediate call.

### 06. Erase the carrier by doing the next old job (P; #07)
- **Mechanism:** After the relay has been read, use a genuine owed update to clear influence of the diagnostic coordinate before its original reader's next sensitive cut. Require the common policy to be valid without another read of the erased value.
- **Novelty vs nearest prior art:** [#297 #07][parent] treats overwrite before the report as failure; [OGD][ogd] protects old outputs by projection. Here a temporary, sampled disturbance is allowed only if actual required work restores the old read on time. Compare a snapshot/restore and projection with charged carry and update cost.
- **Cheapest first test:** Enumerate a two-reader host where a relay persists into one sensitive A read unless a specific already-due update runs; shift that update one tick late and reject the original repair.
- **Old-task retention:** Require normal A requests throughout, including the sensitive read, and keep B's granted job and installed C functional after the carrier is cleared.

### 07. Diagnose a partial write without inspecting the write (P; #07)
- **Mechanism:** Design a due repair whose complete versus interrupted execution changes two native effects differently: the repaired B route may look live in both, but the compulsory C read reveals whether the backing-removal prerequisite also took effect.
- **Novelty vs nearest prior art:** Transaction commit records solve atomic writes directly; [#289 #05][steps] protects immediate residual separation. The candidate only matters on an explicitly non-atomic learning host where the downstream receipt could replace an additional confirmation, not atomicity itself.
- **Cheapest first test:** Enumerate one allowed partial-write cut and two complete histories at matched B score. Compare a commit marker and a same-tick validity check; force a refusal when clipping makes partial and complete writes alias.
- **Old-task retention:** Execute old B via fallback on every partial path, with A and installed C exercised before reconciliation and again afterward.

### 08. Use a natural third report to reject a corrupted pair (P; #07)
- **Mechanism:** Require a consistency relation across three existing C reports: any one report substitution can turn a grant into refusal but cannot turn a refusal into a grant. Do not accept on a majority unless the finite transition relation proves it safe.
- **Novelty vs nearest prior art:** Error-detecting codes supply this distance guarantee for a designed codebook. Here the feasible codewords are induced by equal-progress due records, with reports and update law fixed. Compare a checksum or repeated probe using the same bits and time.
- **Cheapest first test:** Search a finite two-mode optimizer for reachable grant/refuse report traces at Hamming distance at least two. Enumerate single corruptions; include a menu whose minimum distance is one.
- **Old-task retention:** Run B from existing backing through corrupted/refused traces, and check normal A/C progress while all three records are being paid.

## B. Turn a narrow window into completed service

### 09. Spend the window on the last indispensable stage (P; #20)
- **Mechanism:** Allow a pending job to do ordinary preparation before the window without borrowing, then use the certified window only for its final irreversible stage. Count neither preparation nor a checkpoint as service.
- **Novelty vs nearest prior art:** Time-expanded scheduling already prices phased jobs, and [#297 #15][parent] books a whole noninterruptible lease. The candidate is a repair-conditioned stage boundary that makes a previously impossible end-to-end commitment feasible. Compare exact phased scheduling with the same preparation budget.
- **Cheapest first test:** One two-stage job, one short intact job, and one borrowed tick. Move the prerequisite one tick later; this must eliminate the phased job's alleged win.
- **Old-task retention:** Run pre- and post-window B borrowers and A/C tasks during both preparation and commit, including aborted preparation.

### 10. Open a path without releasing another unit (P; #20)
- **Mechanism:** Use the bridge to connect already-safe stages across two fixed hosts. The repair changes which handoff edge is usable in one tick; the total spare host count need not move.
- **Novelty vs nearest prior art:** Time-expanded flows model paths, and [#297 #14][parent] handles portable release under host substitution. Here the signature is a changed temporal cut at *fixed* free-unit counts, not moving a valid standby certificate to another host.
- **Cheapest first test:** Two hosts have the same free capacity under both repairs. Enumerate handoff compatibility and demonstrate an extra completed job only when the connecting edge opens; compare equal-width standby and exact flow.
- **Old-task retention:** Keep host-pinned B traffic at both ends and serve A/C on the handoff tick, not on an idle stand-in host.

### 11. Buy relief for the first congested tick after the bridge (P; #20)
- **Mechanism:** Favor a job whose verified completion pays a specified obligation otherwise due in the next wave, freeing later capacity only after completion. Carry its full old liability until payment.
- **Novelty vs nearest prior art:** [#297 #21][parent] reinvests in delivery of a future C record to preserve evidence. Here the scarce quantity is an already-owed post-window service slot, not diagnostic capacity. Compare exact backlog-aware scheduling and an earliest-deadline arm.
- **Cheapest first test:** Two bridge jobs look equal now, but only one removes a genuine next-wave duplicate service requirement. Add a late or failed acknowledgment; the apparent later capacity must vanish.
- **Old-task retention:** Check the distinct post-wave B obligation on both success and failure, plus rare A and installed C at the overloaded tick.

### 12. Certify which standby is safe to omit before any call arrives (P; #20)
- **Mechanism:** Precompute a public contingency policy that keeps one of several standbys idle only when every allowed next arrival order leaves an executable fallback for the omitted standby's callers. Do not infer independence from observed load.
- **Novelty vs nearest prior art:** [#289 #12][steps] and [#297 #10][parent] use public recourse, while a fixed thin standby is [#297 #12][parent]. Test whether ordering information can replace *physical standby duplication* before the first call without allowing a reservation on both options.
- **Cheapest first test:** Enumerate two wave orders and different immutable borrower routes on each. Compare exact contingent dispatch and two static standbys; add a simultaneous arrival that defeats both causal choices.
- **Old-task retention:** Invoke the omitted standby's original B callers under all legal orders, and verify A/C service on both the chosen and fallback paths.

### 13. Slide an existing call only at its ordinary handoff (P; #20)
- **Mechanism:** Co-design repair timing with an already permitted service handoff to move the bridge by a tick. No interrupted call, extra copy, relaxed old deadline, or new authorizing observation is allowed.
- **Novelty vs nearest prior art:** [Maintenance-duty transfer][handover] changes who pays; slack reclamation exploits known idle time. Here the same obligation and owner survive while lawful phasing aligns the idle tick with an independent deadline.
- **Cheapest first test:** Two lawful handoff ticks, one bridge job and one fixed later old call. Compare an independently optimized scheduler; remove the handoff flexibility as the null.
- **Old-task retention:** Exercise the moved B call against its original latency promise, and run A/C at both candidate handoff times.

### 14. Move work out of a risky tail without reducing its promised load (P; #20)
- **Mechanism:** Let bridge service prepay one named subtask of a noninterruptible later bundle if its result stays valid through intervening required writes. Later dispatch still guarantees the original whole bundle, including recomputation if validation fails.
- **Novelty vs nearest prior art:** Checkpointing and [#289 #27][steps] already cover carried results and atomic bundles. The candidate is conditional prepayment with a *state-dependent validity horizon* that competes for the same backing as recomputation. Compare ordinary memoization plus exact time-expanded scheduling.
- **Cheapest first test:** A bridge evaluates one branch of a later two-part B job; one compulsory update preserves it and one invalidates it. Price cached state and the worst-case recomputation slot.
- **Old-task retention:** Run the full old bundle, including its invalidation branch, and read A/C after the intervening update.

### 15. Clear the bridge downstream before opening it upstream (P; #20)
- **Mechanism:** Admit only if the handback includes a causal way to drain the completion's output from a bounded downstream queue before the following old wave needs that queue. Treat that queue state as an explicit liability.
- **Novelty vs nearest prior art:** Backpressure and network calculus already account for downstream congestion. The candidate is a repair-funded *end-to-end* handback when local fallback release is sound but local completion is not useful. Compare a queue-aware scheduler with the same reports and buffers.
- **Cheapest first test:** Two identical local bridges feed a one-entry queue, but one lacks an on-time consumer. Give both the same extra compute allowance and check that the local-only win disappears.
- **Old-task retention:** Run old B's next-wave enqueue on schedule and check A/C consumers against their normal inputs with the bridge output in flight.

### 16. Price the shortest bridge that can survive a slow completion (P; #20)
- **Mechanism:** Compute a completion envelope from legally observable phases. Choose the repair by whether its opening admits a causal policy with safe handback for *all* supported runtimes, not by window length or mean utilization.
- **Novelty vs nearest prior art:** Dynamic controllability in temporal networks with uncertainty already models contingent durations. This asks whether discrete due updates can change that controllability boundary at matched repair gain. Compare exact dynamic scheduling and worst-case interval booking.
- **Cheapest first test:** Two jobs with the same worst-case length, only one with an intermediate public event permitting safe dispatch to a disjoint host. Remove that event or add an indistinguishable slow tail as a negative.
- **Old-task retention:** Stress the slow branch while the first post-window B caller arrives, and run A/C throughout the handback.

## C. Couple the relay and the bridge without borrowing against future evidence

### 17. Make a report select a continuation, not a label (P; #07 + #20)
- **Mechanism:** Before the relay, commit only computation common to all safe continuations and consuming no backing. On the native report, choose a complete dispatch continuation; two histories may share a bin if the same policy works for both, even when their safe release sets differ.
- **Novelty vs nearest prior art:** [#297 #17][parent] fits bins to different schedules, and functional coding assumes an answer to encode. Here the encoder can target a *relation*: any common feasible continuation is a correct answer. Compare exact relation-valued encoding and an optimal same-report dispatcher.
- **Cheapest first test:** Three histories allow plans {p,q}, {q,r}, {p,r}; every pair overlaps but all three do not. Look for a legal due write inducing a two-cell partition and score completed jobs, not pairwise overlap.
- **Old-task retention:** Fire all pinned B calls in each proposed cell and exercise old A/C during common preparation and after each dispatch plan.

### 18. Co-design when the evidence matures and when it expires (P; #07 + #20)
- **Mechanism:** Choose a lawful repair/continuation pair by the intersection of its report-valid interval and the feasible start interval of an independent arriving job. A policy may observe early or late, but may only act on fresh, complete evidence.
- **Novelty vs nearest prior art:** [#297 #03/#15][parent] separately guard report timing and lease expiry. The candidate targets the intersection; improving either extreme alone can be useless if it moves both endpoints away from the eligible job.
- **Cheapest first test:** A two-by-two due menu yields pairs with earlier evidence or longer leases but no completion; search for the crossed choice with a strict on-time gain. Give the stack both menus and the same clocks.
- **Old-task retention:** Exercise B before the first valid report and at expiry, and require the two nonwinning C schedules to be scored on the same A/C workloads.

### 19. Schedule by the last useful observation, not the earliest report (P; #07 + #20)
- **Mechanism:** Work backward from each feasible completion to the last tick when a necessary distinction can be acted on. Reserve no hosts; use this frontier to rank mandatory records that could produce that distinction in time.
- **Novelty vs nearest prior art:** Value-of-information scheduling already prices timeliness. This uses a frontier of exact, retention-valid service continuations to decide *which* alias is worth breaking; [#297 #01][parent] targets a fixed named release. Compare exact partially observed planning and earliest/equal-gain reveal selection.
- **Cheapest first test:** Two due relays can distinguish different borrower modes. Delay one deadline without changing ambiguity or demand; the selected relay should change only when the feasible continuation changes.
- **Old-task retention:** Serve both modes of old B in both deadline orders and verify fixed A/C deadlines regardless of the selected relay.

### 20. Fit the evidence to the job's cheapest safe failure mode (P; #07 + #20)
- **Mechanism:** Allow a candidate job to offer two preexisting service variants, each with a different safe abort bound. Use the relay to certify one bounded variant before start, including all resources needed to restore the old service plan if it aborts.
- **Novelty vs nearest prior art:** [#297 #15][parent] forbids depending on mid-call revocation. Here revocability is an original property of a specified service variant, and safe abort is fully backed; the new claim is useful on-time completions that survive charging restores and aborts. Compare preemptive reservation and exact joint admission.
- **Cheapest first test:** One variant is short but noninterruptible; another may abort locally and needs a priced cleanup tick. Introduce a branch where cleanup would strand an old call and require pre-admission refusal.
- **Old-task retention:** Actually run cleanup against the resumed B borrower deadline, and check normal A/C paths on both completion and abort.

### 21. Preserve a safe bridge under a blind change of claimant (P; #07 + #20)
- **Mechanism:** Compile a bounded menu of release policies indexed by the already public job descriptor. Before arrivals, aim the required C updates at distinctions shared by multiple policies; after arrival, certify only the selected job without granting to hypothetical alternatives.
- **Novelty vs nearest prior art:** [#297 #01][parent] protects distinctions for a named release; 01 above changes what the mandatory record reads. Here the report and record sequence are fixed and the later job descriptor changes the continuation problem. Compare a general report code and a paid per-job audit with the same blind menu.
- **Cheapest first test:** Two job descriptors share one dangerous alias but differ on a second. Keep the first-stage selection blind and score each held-out descriptor, then add a third job requiring a distinction missing from the report.
- **Old-task retention:** Run earlier B borrowers even on the unknown descriptor's refusal and compare held-out A/C after both accepted job types.

### 22. Factor out the zero-latency stack (I; #07 + #20)
- **Mechanism:** Cross relay-capable/overwriting C with usable/stranded bridge, then gift the resulting native reports to a zero-extra-tick verifier and exact scheduler. Account separately for repair gain, report latency, peak reserve and completed service.
- **Novelty vs nearest prior art:** [#297 #22][parent] factors repair, separation and handover. Here evidence *delivery* and the last usable tick are varied independently of final bin separability. A tie with identical evidence is the expected outcome, not a defeat of the test.
- **Cheapest first test:** Enumerate one bridge job with a deadline at the native report and at one tick earlier or later; include a paid probe that can be moved earlier at equal coverage, and an oracle as an unattainable ceiling when needed.
- **Old-task retention:** Replay every pinned B request on all legal cuts, including early refusal and late receipt; measure ordinary A and installed C after any actual completion.

## Ranked deeper questions

1. **Can lawful C create an on-time decision neither an immediate check nor the best modular stack can buy at the same cost?** Start with 03, 18, 19 and 22. Verify that the two cuts really differ in public information, then move the deadline and auditor independently. If shared native evidence closes the gap, credit the cheaper relay or scheduler only where a measured resource saving remains.
2. **How much blind variation can an actionable relay tolerate before paid state or an audit wins?** Use 01, 04–08 and 21. Vary due order, legal partial writes, quantization and job descriptors on a held-out menu. Seek a finite non-erasing positive and an overwrite impossibility case with identical retention floors.
3. **When does a safe window change the completion frontier rather than just the reserve ledger?** Use 09–16, and compare exact contingent scheduling, equal-size standby and never-release. Independently vary stage placement, acknowledgment and the post-wave deadline; count only end-to-end service and audit each retained liability.
4. **Can one low-cost public report support several causal policies without overselling their common fallback?** Start with 12, 17 and 20. Include a pairwise-compatible but jointly incompatible cell and a late abort. Seek a certificate smaller than the exact table and stop if its savings evaporate with a real old-task call or charged cleanup.

[parent]: https://github.com/manojbajaj95/cl/pull/297
[review]: https://github.com/manojbajaj95/cl/pull/6
[triage]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/flood-triage.md#L414-L417
[ledger]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/idea-ledger.md
[steps]: https://github.com/manojbajaj95/cl/pull/289
[useful]: https://github.com/manojbajaj95/cl/pull/273
[handover]: https://github.com/manojbajaj95/cl/pull/267
[coding]: https://doi.org/10.1109/18.915643
[ogd]: https://arxiv.org/abs/1910.07104
