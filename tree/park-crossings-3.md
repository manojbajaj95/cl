# Park crossings III: buy a way back with work already owed

**Status:** Ideas only; no implementation, learner runs, or GPU work. **Parent:** [Returnable and repair-coupled park crossings](park-crossings-next.md) ([PR #296][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, row 414 in rows 414–417][triage] ([PR #6][review-pr]) scores two #296 ideas at 3: [#05, use a choice among equivalent due B batches to widen the way back](park-crossings-next.md#05-spend-intervening-p_--work-to-widen-the-returnable-basin-p), and [#11, co-batch an individually unsafe overdue A repair with a due B crossing](park-crossings-next.md#11-use-bs-crossing-displacement-to-cancel-an-overdue-repairs-park-violation-p). The neighboring rows review other branches, not additional seeds for this node.

## Contract and deciding controls

- Inherit the [parent contract](park-crossings-next.md#contract-and-deciding-controls). A is incumbent service (`A_park`) plus an independently specified overdue repair (`A_rep`); B is successor service; C is an unrelated old-task slice. `P_+` and `P_-` are the two components of the deployed A acceptance set. A crossing is one native atomic commit between them. Pin the optimizer (including live slots), record/batch grammar, arrivals and observations, deadlines, publication boundaries and tolerances before comparing policies. No label changes, invented work, skipped obligations, or hidden unsafe published state. A repair deemed unsafe alone must be evaluated under the same optimizer and its own legal solo-batch normalization; the joint step is not assumed to be a sum of solo steps.
- B alternatives owe the **same** service by the same deadline; match on current B error or progress and A/C headroom using calibration reads, and test generalization on independent holdouts. For returns, fix the predeclared future record menu and legal arrival histories before outbound commitment. Map a live state to the returns it can actually execute on time, without erasing B learned away. Pair count, record-disjointness and distinct failure domains are three different quantities. Use only observations revealed by the decision tick; replay identical arrival histories across arms and distinguish worst-case guarantees from distributional improvements.
- For repairs, precommit an unseen drifted `A_rep` floor and a repair deadline. Require the repair record to contribute to `A_rep` and the B record to contribute to B; compare equally normalized singleton and matched dilution/crossing controls, not just a larger raw joint displacement. Check held-out `A_park`, unrelated rare C and already-earned B at **every** publication, including the first ordinary tick after landing or returning; check unseen `A_rep` at its own deadline and after the next write. Where a card says “retention,” these are additional checks, not alternatives.
- Match allocated bytes (including cached previews and buffered records), native steps, attempted and accepted work, preview calls and decision latency. The return arm must face #296#05 count-based steering, unsteered certificates, [return corridors][corridors], random/minimum-motion B scheduling, and compressed snapshot **plus** B replay. The repair arm must face #296#09/#11, [GEM][gem]/[A-GEM][agem], [GraB][grab], compatible individually safe repair, both solo stages in both orders, feasible step damping, and replay that skips the unsafe repair (score the missed SLA). Give joint cards the **stack** of the strongest causal single-seed controls with the same budgets, and give exhaustive causal native-batch search as a ceiling in tiny cases. If enumeration ties at equal cost, a named policy is not a new primitive. Match per-item old-task margins before attributing failure order; report no-effect pools, not just designed wins. **P** denotes a candidate reusable object or operation, not a novelty verdict. Nearest-prior comparisons are hypotheses for review, not exhaustive searches.

## Idea cards

### Choice among due B batches (#296#05)

#### 01. Buy another independent way back with a due B batch (P)
- **Mechanism:** Choose among eligible B batches by the smallest number of independent failure domains whose loss would disable every executable return. One physical record can be in several pairs, and disjoint pairs can still ride the same source.
- **Novelty vs nearest prior art:** Reliability cut sets already price redundant paths; the candidate is changing the cut of a future lawful training menu by doing equivalent work now. #296#05 buys pair count, not necessarily independent availability.
- **Cheapest first test:** Enumerate two equal-progress, equal-motion landings: three disjoint pairs all on one source versus two pairs each wholly on a different source. Drop any one source, then test actual native returns. Reject if count steering (or the unsteered certificate) achieves the same on-time coverage.
- **Old-task retention check:** Run held-out plus-side A after each surviving return and rare C after both B choices, including a no-outage trial; require earlier B work to survive both routes.

#### 02. Steer for a return that can be chosen before the last arrival (P)
- **Mechanism:** Back up a set of live states on a tree of observable arrival prefixes; accept a due B step only if the continuation chooses the same legal action on histories that look identical at decision time.
- **Novelty vs nearest prior art:** Nonanticipative robust scheduling is the strong control, not merely a state-by-state oracle. The candidate output is a lawful B update that buys an observation-compatible *training* continuation, rather than a new solution method for robust scheduling.
- **Cheapest first test:** Enumerate two future streams with the same first report and an expiring first action. One B choice has a return per stream but requires opposite first actions; another has one common executable first action. Kill if the parent certificate with causal robust scheduling finds the same continuation at the same cost.
- **Old-task retention check:** Score both streams, including the one the oracle would choose differently; check A at the original due tick, not after a belated recovery, and C after the first irrevocable action.

#### 03. Split return capacity across competing old jobs (P)
- **Mechanism:** A B step buys a matching from old-job deadlines to executable return batches, with record-use capacity and slot transitions carried through the assignment. Individual coverage cannot spend the same indivisible record twice.
- **Novelty vs nearest prior art:** Matching and finite-capacity scheduling assign fixed resources; here a necessary learning step changes the executable edges without acquiring records. Compare directly to a return certificate followed by ordinary capacitated scheduling.
- **Cheapest first test:** Two held-out old jobs at successive ticks, three return opportunities, one shared expiring record. Enumerate complete continuations for two equivalent B steps; ask whether one resolves a capacity deficit while per-job counts are unchanged. Reject if the scheduling control finds the same option.
- **Old-task retention check:** Check both old jobs separately at their deadlines as well as the first job again after the second write, so nominal assignment cannot double-count retention.

#### 04. Make late records interchangeable at a live handoff (P)
- **Mechanism:** Use a due B choice to align the outcomes of two different early return batches under the same not-yet-seen finishing record. The learner can take either early opportunity without reserving a different suffix for each.
- **Novelty vs nearest prior art:** Robust MPC with a terminal set already handles common continuations. The candidate is earning suffix interchangeability through ordinary B learning, with the finish still an unmodified future record and no optimizer reset.
- **Cheapest first test:** Enumerate two early batches and one late batch on a native momentum toy. Compare a B choice that makes the common suffix executable to best fixed landing plus contingent suffix search; include a twin where the shared suffix fails from one carried slot state. Reject if terminal-set planning ties.
- **Old-task retention check:** Replay either legal early handoff and the following normal plus-side write; verify A, C and away-learned B in both, not just at the aligned intermediate read.

#### 05. Buy recourse specifically for the rare-C veto (P)
- **Mechanism:** Among B alternatives that keep today's C read fixed, choose one making future A-return witnesses substitutable *after* a known C service requirement is revealed. Coverage is conditioned on the revealed C requirement, not pooled across conditions.
- **Novelty vs nearest prior art:** Multi-constraint viability already checks A and C jointly; the possible operation is shaping which lawful future returns the same B service can support under later C demands. Do not count a replication of constrained MPC as novelty.
- **Cheapest first test:** Cross two C requirements with three future return pairs and two equivalent B landings, keeping the number of jointly feasible cells fixed. Test whether only one landing covers both requirements; remove the C-sensitive direction as a null.
- **Old-task retention check:** For each C requirement test its own held-out rare slice as well as the other slice and plus-side A at deadline; require equal immediate C headroom before selection.

#### 06. Widen the return without changing the published weight read (P)
- **Mechanism:** Choose between truthful batches with equal published weights and B outputs but different live optimizer slots; the choice is useful only if it changes the feasible return menu. For native momentum with averaged gradients, use two lawful prefixes if a single step cannot separate weights from slots.
- **Novelty vs nearest prior art:** Optimizer-state steering and #296#07's slot-aware certificate are controls. Here an unavoidable B job creates a choice in return coverage invisible to the current weight read, rather than just checking a given slot state or zeroing it.
- **Cheapest first test:** Enumerate two equal-length heavy-ball prefixes with matching endpoint weights and different final moments (if the native grammar permits), then apply the same return pairs and compare with a momentum cap and reset. If no legal pair of prefixes exists, stop there.
- **Old-task retention check:** Check A and C at *each* prefix, after return and after the first plus-side step; equal endpoint weights alone do not certify stable old service.

#### 07. Spend only a surplus B choice that survives certificate expiry (P)
- **Mechanism:** Compare candidate B actions by the set of ticks at which they permit safe return, pricing due competing updates as transitions rather than assuming an idle wait. Do not infer that all ticks between the earliest and latest are covered. Choose for the old job's fixed service window, not longest raw lifetime.
- **Novelty vs nearest prior art:** Time-expanded return corridors and robust deadlines already give the right ceiling; the new object would be a reusable set of safe deadline ticks earned by one due update under a fixed arrival grammar.
- **Cheapest first test:** Enumerate two landings with the same tick-3 menu but different tick-2 and tick-4 feasibility because a required intervening update consumes a pair's applicability. Compare just-in-time corridor steering; kill if it matches at equal preview cost.
- **Old-task retention check:** Check held-out A exactly at each tested due tick and C during the intervening compulsory steps, with no credit for returns outside the specified window.

### Cancellation that makes an unsafe repair usable (#296#11)

#### 08. Pair two forbidden singletons without relabeling either (P; seed anchor)
- **Mechanism:** Find a truthful `A_rep` record whose solo commit is unsafe and a due B record whose solo commit is also unsafe; use the native joint commit to land in `P_-` and meet both deadlines. Require an independently measurable contribution from each.
- **Novelty vs nearest prior art:** This is the #296#11 seed, not a fresh novelty claim. GEM/A-GEM protects a fixed old read by gradient editing; GraB orders examples. The hypothesis to beat is that matched variants reach the same joint service without a lawful two-sided landing.
- **Cheapest first test:** Modify parent R2 to make its old singleton unsafe; enumerate all solo, joint, and both sequential arms, plus legal damped solo, GEM/A-GEM, an individually safe repair, and a B twin that adds to the violation. Add a batch-normalization-matched leave-one-out preview where legal.
- **Old-task retention check:** On each arm score A on ordinary inputs in the destination component, unseen `A_rep` at deadline, and C before and after the next ordinary update.

#### 09. Use a truthful third record only when every pair is insufficient (P)
- **Mechanism:** Find the smallest native joint batch of unsafe A repair, due B crossing and independently due C service that closes the park. Demand that deleting any member loses feasibility even after renormalizing the batch.
- **Novelty vs nearest prior art:** [GradMatch][gradmatch] and higher-order coreset selection already match aggregate updates. The candidate is a minimal multi-obligation crossing with none of its sub-batches jointly serviceable, rather than gradient reconstruction or the parent's rare-C-as-repair substitution.
- **Cheapest first test:** Exhaustively test every subset of three records and an equal-size neutral-record control, then test separate GEM projections and the best #296 repair pair plus ordinary C. Reject if lawful subsets or the stacked arm meet the same floors and deadlines.
- **Old-task retention check:** Hold out ordinary A, drifted `A_rep`, and rare C inputs independent of all three records, including a C slice without the due event.

#### 10. Separate real repair steering from gradient dilution (P)
- **Mechanism:** Match an individually unsafe repair to a B partner by its contribution at the *destination branch normal*. Require a second honest repair candidate with matched old-service gain and native batch size but with the opposite destination contribution.
- **Novelty vs nearest prior art:** MIR ranks high-interference replay and gradient balancing changes relative scale. The candidate selector uses a finite displacement at the destination, with a contrast record that removes a mere change in batch denominator as an explanation.
- **Cheapest first test:** Use a curved two-component park; equalize the two repair candidates' calibration gains and the crossing half-step. Compare destination-normal selection with source cosine, loss ranking and exhaustive previews. Kill if the matched-dilution control or source-based scores tie.
- **Old-task retention check:** Match A/C starting margins; after each candidate test unseen repair transfer separately from A park preservation, including the next step.

#### 11. Test whether repair viability has a gap, not a magic step size (P)
- **Mechanism:** Find a due repair with no solo step satisfying both the park and the repair SLA over the permitted step schedule, but with a nonzero interval of joint step tolerances that serves both repair and B. Certify the infeasible solo interval and the feasible joint interval separately.
- **Novelty vs nearest prior art:** Line search and trust regions already solve step-length feasibility for a given direction; the claim is a truthful joint batch opens a feasible direction without changing the deployed optimizer. Slack from a specially tuned learning rate is not novelty.
- **Cheapest first test:** In a polynomial toy, solve the floor inequalities exactly across the predeclared step interval for each solo order and the joint batch, then evaluate at the one deployed step. Reject if legal solo damping closes the gap, or if the joint pass is isolated to an exact value when tolerances are nonzero.
- **Old-task retention check:** At both feasible interval edges and the deployed step, check held-out A, rare C, and unseen repair margin rather than only the calibration sentinel.

#### 12. Make a repair pair robust to which old case drifts (P)
- **Mechanism:** Choose a B partner before the overdue A record arrives; after the truthful repair record is revealed, batch it with the partner only if the continuation is legal for every predeclared drift case. This buys a repair contingency, not an average reduction.
- **Novelty vs nearest prior art:** Robust control with recourse covers the planning abstraction. The distinctive candidate is a due, indivisible crossing record acting as a shared *cancellation partner* for alternative unsafe repairs, with independent repair labels and no extra probe.
- **Cheapest first test:** Two possible repair arrivals, two due B candidates and one expiring partner decision; enumerate the causal policy tree versus late selection (if lawful), random precommitment and per-case #296#11. Reject if a late search can make the same choice for no extra cost.
- **Old-task retention check:** Verify held-out examples for each actual drift case and the unaffected case, then check the old routine and C after the next ordinary update.

#### 13. Cancel the violation across the first successor write (P)
- **Mechanism:** Choose a due B partner that makes a repair crossing safe at commit **and** keeps the ensuing required C step safe under the slots the pair leaves behind. No intermediate slot edits or reset.
- **Novelty vs nearest prior art:** Two-step projected rehearsal and lookahead viability are the strong comparisons. This is outbound repair-specific cancellation of an otherwise unsafe next write, not the parent's momentum carried into a return.
- **Cheapest first test:** On a heavy-ball toy preview two joint batches matched on landing weights and immediate service where a legal prefix or masks allow unequal live slots; otherwise match park margin rather than asserting unequal slots at equal weights. Compare the required next C commit against one-tick #296#11 and bounded momentum. Kill if one-tick selection with a cheap momentum cap ties.
- **Old-task retention check:** Verify A and unseen `A_rep` after the joint batch, after required C, and on the first sensitive A read; verify independent C cases rather than just the C update example.

#### 14. Use the same due B record with either of two unsafe old repairs, but never both on credit (P)
- **Mechanism:** Precompute mutually exclusive ways one expiring B record can legally carry one of two due old repairs, then allocate it by feasible completion of the remaining job (which must have a separate legal path). Debit the record at commit.
- **Novelty vs nearest prior art:** Deadline matching assigns jobs to slots; the candidate is creating the edges through native co-batch cancellation. A scheduler that treats partner availability as spendable twice or lets an old obligation silently lapse is not a fair baseline.
- **Cheapest first test:** Enumerate two same-deadline old repairs and two B crossing offers plus a legal independent continuation. Compare earliest-deadline/greedy matching and dedicated partners; add a pool where no continuation serves the unpaired repair and require refusal.
- **Old-task retention check:** Check each drifted old job independently at deadline; on the refusal branch score the missed service rather than excluding it from retention.

### Joint options: a repair must change which return can actually be spent

#### 15. Buy matching cuts and cancellation with the same required B choice (P)
- **Mechanism:** Choose an intervening B batch that changes both the shared-record cut of the return menu and which future unsafe repair can be carried by a remaining return batch. Optimize *repair-bearing* return coverage rather than separate counts.
- **Novelty vs nearest prior art:** #296#05 plus #296#11 independently can pick a safe landing and a compatible repair; joint scheduling is the strong control. The distinct interaction is that deleting the last repair-bearing witness defeats a landing with larger raw return coverage.
- **Cheapest first test:** Use two equivalent B landings and two one-outage scenarios. Require a lawful return and repair in each scenario; compare independent steering plus best compatible repair, including a pool in which every return can carry every repair. Kill if the stack ties.
- **Old-task retention check:** Evaluate A on both sides, each actual unseen repair case and C on each outage path; require away-learned B to survive the joint return.

#### 16. Bank cancellation in the reachable envelope, not a saved state (P)
- **Mechanism:** Declare a set of live away states for which the same class of future joint repair/return maps preserves B and both old reads. Permit a due B choice to move the learner into this set without saving weights or banning all subsequent updates.
- **Novelty vs nearest prior art:** Robust predecessor sets already encode set inclusion. The candidate interface is the pre-image of a *joint old-service commit* with an unsafe singleton, not #296's envelope for bare returns or its independent co-batched return.
- **Cheapest first test:** Enumerate two B alternatives and two following lawful updates (one not idle). A bare return works everywhere; a repair-bearing return works everywhere only after one alternative. Compare the stack with equal-byte snapshot plus repair/B replay and with a joint predecessor oracle.
- **Old-task retention check:** Exhaustively score A, `A_rep` and C for every reachable post-B state and the following write, not just the state used to construct the witness.

#### 17. Make the expiring return record carry the non-deferrable repair (P)
- **Mechanism:** When one return record expires early and another arrives late, steer due B so a jointly feasible early return spends only the expiring record allocation and the unsafe repair; the late record remains allocated to another fixed job.
- **Novelty vs nearest prior art:** Time-expanded scheduling and #296#18 co-batched return are controls. The candidate is a change in which *resource expiry conflict* is resolvable through B learning, not simply running the old repair at return.
- **Cheapest first test:** Enumerate one early and one late availability window under the same indivisible grammar. Give the control the best ordinary repair schedule with reserved return records. Reject if the same assignments are possible without the B side effect or by replay at equal cost.
- **Old-task retention check:** Test A and unseen repair at the early deadline and independently score the old read associated with the saved later allocation.

#### 18. Let return partners trade roles across arrival branches (P)
- **Mechanism:** Steer B so a record that supplies mostly crossing displacement on one live branch can supply the cancellation component on another, in both cases serving its unchanged truthful target alongside the actual overdue A record.
- **Novelty vs nearest prior art:** #296#15 leverage bands and robust assignment already rank fixed partner roles. Claim a functional exchange only when both branches fit native updates and a fixed-role allocation cannot attain the same causal coverage at the same cost.
- **Cheapest first test:** Construct two observable prefixes, two return partners and one unsafe repair case per branch. Compare branch-sensitive selection with a fixed-role assignment and unconstrained lawful enumeration. Add a null where the active coordinates of all partners are identical; reject if fixed roles tie.
- **Old-task retention check:** Run the ordinary A and repair suites on both branch endpoints and after their next B write; require rare C to pass under both allocations.

#### 19. Prefer a return that keeps the next repair feasible (P)
- **Mechanism:** Co-batch the due unsafe repair at return, but rank that commit by whether it leaves a second specified old repair executable under its own later deadline. Select the preceding B update using this two-repair continuation, not by first-return count.
- **Novelty vs nearest prior art:** #296#16 backlog handling and #296#11 cancellation together are the baseline. The proposed interaction is discovering a predecessor B choice that preserves the **second** repair even when first-return feasibility and current old-task margins are identical.
- **Cheapest first test:** Enumerate a three-tick suffix with two equivalent steering moves and two overdue jobs; run greedy first-return, strongest stacked scheduler, and exact horizon search. Reject if the full stack already sees every relevant second-repair distinction.
- **Old-task retention check:** Re-test the first repaired old routine after the second repair; also retest ordinary A, rare C and the B work acquired away.

#### 20. Earn a return that needs no unsafe repair as a reserve (P)
- **Mechanism:** Use due B work to retain both a repair-bearing return when the unsafe repair arrives and a separate bare-return path when it does not. The bare path never pretends that an unserved repair passed: it is lawful only on histories where the specified repair obligation does not activate.
- **Novelty vs nearest prior art:** Contingency planning handles optional jobs; the candidate is one B update creating both types of lawful recourse without a reserved dummy repair, synthetic substitute or held snapshot.
- **Cheapest first test:** Enumerate two otherwise identical arrival histories, one activating the repair and one not, plus a control where the repair is due but the record is absent. Test the best single-seed stack; the third history must report an unmet duty unless another truthful record covers it.
- **Old-task retention check:** Measure early A plus C on all histories, and independent `A_rep` wherever obligated. Retest already-earned B after either actual return.

#### 21. Make a tiny joint certificate composable across optimizer ticks (P)
- **Mechanism:** Carry paired witnesses of a return arrival cut and a repair-feasibility inequality; compose them only across reachable slot transitions that preserve *both* witnesses. Store witness IDs and interval bounds, not states or replay transcripts.
- **Novelty vs nearest prior art:** #296#06 compressed return witnesses and assume–guarantee reasoning are the direct comparisons. Only a compact joint witness that rules out ordinary stacked certificates at the same cost would count; it must detect incompatibility that neither witness detects alone.
- **Cheapest first test:** Enumerate a tiny integer/rational toy with one shared slot and two transitions. Compare bytes, peak decision work and false admissions with exact lookup and separate certificates; include a transition preserving each witness somewhere but never on the same continuation.
- **Old-task retention check:** Decode and run every accepted branch through the native optimizer; check old A, the real drifted `A_rep` read and C, plus the next ordinary write. Any false admission on these reads fails.

#### 22. Treat absence of a feasible interaction as a first-class outcome (I)
- **Mechanism:** Pre-register a small unfiltered truthful-record pool and count how often a due B choice changes a verified return cut, how often unsafe repairs can be carried, and how often those witnesses intersect in complete on-time continuations. Report no-choice and no-cancellation instances in the denominator.
- **Novelty vs nearest prior art:** This is an audit beyond #296#22, not a new operation: measure the gap between the two marginal seed rates and the feasible joint rate. The strongest null is the full causal control stack with identical arrivals and charged information.
- **Cheapest first test:** On CPU, enumerate several small fixed-stream pools using held-out task splits and both independent and shared-source arrivals; compare designed positive and negative controls with unfiltered pools. Stop if only planted examples show the interaction or the stack matches every unfiltered win.
- **Old-task retention check:** Publish A, unseen `A_rep`, rare C and previously earned B by feasible/infeasible stratum, including refusals and missed deadlines rather than conditioning retention on success.

## Ranked deeper questions

1. **Can due B work buy a bigger *causal reliability cut*, not just more pairs?** Start with 01–03. Require distinct outage outcomes under identical present service, and a causal continuation for every claimed branch. Stop if minimum-motion steering plus robust return planning matches it, or if a snapshot with charged B replay dominates.
2. **Is an unsafe repair genuinely enabled by native cancellation rather than a hidden step-size or batch-size subsidy?** Use 08–11. Require an unseen repair win where both normalized separate orders and legal damping fail, and the wrong-sign partner loses. If GEM/A-GEM matches the full on-time retention frontier at the same compute, the only distinction left is the native-update restriction; do not claim a general retention win.
3. **Does repair-bearing recourse require reasoning about the two seeds jointly?** Use 15–16 and 19. Look for equal immediate margins and equal bare-return coverage but a different on-time A/B/C outcome. Give the best causal combination of the two prior policies the same preview budget and the option to schedule snapshots/replay. If it ties, retire the merge claim.
4. **Are lawful opportunities dense enough to justify searching for them?** Use 21–22 after the small falsifiers. Count complete on-time continuations, allocated evidence bytes and delay, not just geometric witnesses. A successful engineered toy with no wins in unfiltered pools is a feasibility example, not evidence for a learner pilot.

[parent]: https://github.com/manojbajaj95/cl/pull/296
[review-pr]: https://github.com/manojbajaj95/cl/pull/6
[ledger]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/4ec84a665f28fa595c3639803917058d3c709ac7/reviews/flood-triage.md#L414-L417
[corridors]: https://github.com/manojbajaj95/cl/blob/devin/1795562037-return-corridors/tree/return-corridors.md
[gem]: https://arxiv.org/abs/1706.08840
[agem]: https://arxiv.org/abs/1812.00420
[grab]: https://arxiv.org/abs/2205.10733
[gradmatch]: https://arxiv.org/abs/2103.00123
