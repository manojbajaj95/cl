# Make-before-break writes: build the next route before giving up this one

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Disjunctive protection](disjunctive-protection.md) ([PR #155](https://github.com/manojbajaj95/cl/pull/155)), cards 2 and 11. **Review seed:** [Flood triage row 249](https://github.com/manojbajaj95/cl/blob/a23652eb741c8198a672880caeccf111a4222c2a/reviews/flood-triage.md#L249), two score-3 ideas: build and validate a new route before relinquishing the current one, and distinguish serving now, serving after rerouting, and serving only after retraining.

## What would be new?

**Is route handover with a live guarantee a new object for continual learning?** Keeping one of several existing certificates live is the parent's rule. Here the old route is the *only* one that serves, and B needs its capacity. The write must learn or construct a replacement while the old route still works, validate the replacement independently, move traffic, then release only the resources nobody still needs. The candidate object is a **service-preserving write with a retirement witness**: a later learner can check not only that the endpoint solves A and B, but also which proposed reuse is now safe and what serving obligations still block it. The protocol itself is not new. If an ordinary version swap plus incremental verification gives the same safe reuse and total cost, this is deployment machinery applied to CL, not a CL primitive.

A route includes its producer, dispatch, state, normalization and downstream consumer. Use the acquisition reference of each old task (not yesterday's possibly degraded checkpoint), a declared input domain, output or loss tolerance, and a request deadline. For every allowed execution, at every observable prefix, every admitted old request in that domain must complete within the deadline and meet its reference tolerance. Open requests count across a cutover. A finite held-out panel gives empirical evidence, not this universal guarantee; an exact guarantee in a toy applies only to its enumerated domain, scheduler and fault model. Unknowns do not count as live.

| Backup state | Operational witness | Counts for live service? |
|---|---|---|
| **Serving now** | The installed path already handles this slice under the current dispatcher and load. | Yes, for the covered slice and budget. |
| **Serving after rerouting** | An installed, independently checked fallback can take over via a declared, possibly input-dependent switch, with fixed learned parameters and optimizer state. Detection, gate computation, state transfer and execution fit the request deadline. | Yes, only under those conditions; forced access with an oracle task ID or a missed deadline does not qualify. |
| **Serving only after retraining** | No qualifying fixed-weight route is known; a bounded weight or optimizer continuation followed by a fresh service check can recover the slice. | No. It may be built in the background while another route serves; report recovery separately. |

Use the cheapest *demonstrated* mode for a slice in a given state. Unverified fixed-weight routing is not evidence that retraining is necessary; prove absence only in an exhaustively searched, declared class. A route can change class without changing its weights if the dispatcher, timing, state compatibility or load changes.

**Paper case.** Let A read the Boolean route selected by gate g: start with a = 1, b = 0, g = a, and let B require a = 0. If one field can change per public write, retiring a or switching to b first breaks A. Set b = 1 off-route, check b without help from a, switch g to b, then release a. No initial alternate was live; all visible prefixes now serve A. Add independent old C and a held request that has already selected a: releasing a before that request drains is unsafe even though every fresh request passes. A private clone with atomic activation and a drain can solve the toy too; charge its peak bytes and overlap. If a fully atomic joint repair fits the actual resource and serving model, the toy does not separate it. If a and b both read a trunk B must destroy, the proposed handover fails unless the trunk is replaced too.

## Prior-art screen and common CPU controls

- **Networking and deployment:** RSVP-TE [make-before-break](https://www.rfc-editor.org/rfc/rfc3209.html#section-4.6.4), [MPLS fast reroute](https://www.rfc-editor.org/rfc/rfc4090.html), [consistent network updates](https://www.cs.cornell.edu/~jnfoster/papers/frenetic-consistent-updates.pdf), and [blue-green deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html) already cover overlap, bounded failover, per-packet version consistency and cutover. Route readiness, draining and a version pointer are not novelty claims. The CL question is whether a constrained learner can *synthesize* the replacement and reuse the retirement witness across later learning without a spare full model.
- **Learned expansion, routing and recovery:** [Net2Net](https://arxiv.org/abs/1511.05641) and [Grow, Don't Overwrite](https://arxiv.org/abs/2603.08647) preserve the function at expansion; [Progressive Nets](https://arxiv.org/abs/1606.04671) freeze prior columns; [CL MoE](https://arxiv.org/abs/2406.16437) and [MoRAM](https://arxiv.org/abs/2506.21035) use routed or self-activating capacity. None of these comparisons should be handicapped by denying it safe expansion or learned routing. [Hydra](https://arxiv.org/abs/2307.15771) shows fixed-weight self-repair under some ablations; [recovery witnesses, PR #139](https://github.com/manojbajaj95/cl/pull/139) explore legal training continuations. Neither observed compensation nor a one-step recovery is evidence of service within a deadline.
- **Safety in CL:** [GPM](https://arxiv.org/abs/2103.09762), [Certified CL](https://arxiv.org/abs/2407.06697), [APRNN](https://arxiv.org/abs/2304.03496), and the [stability gap](https://arxiv.org/abs/2205.13452) anchor protection, certified repair and within-training measurement. [PR #152](https://github.com/manojbajaj95/cl/pull/152) already considers certified paths of finite safe updates; [PR #156](https://github.com/manojbajaj95/cl/pull/156) packages safe orders and reusable prerequisites. Ask whether explicit service and retirement obligations add power or reduce verification costs over those tools with the *same* interface and resources. The [idea ledger](https://github.com/manojbajaj95/cl/blob/a23652eb741c8198a672880caeccf111a4222c2a/reviews/idea-ledger.md) rules out claims won by exact restore, built-in toy thresholds or ties with matched replay. The screen is provisional.
- **Shared protocol:** Start with exhaustive Boolean gates or tiny rational ReLU models, then try an unmodified CPU split-digits MLP with a bounded adapter/router pool. A is ordinary old holdout data disjoint from route discovery, validation, and replay; C is an untouched old task. Report separate deadline, rare-slice and forced-route panels rather than substituting them for ordinary behavior. Check A/C before B, on requests at each exposed prefix (including aborts and the first request after release), and after learning B without any wake-up training. Compare at matched attained held-out B and report when no common B point exists. Include atomic endpoint repair with private staging, parent-style selection among installed routes, GPM plus the strongest matched replay, and per-prefix verification plus rollback. Give controls the same route candidates, shadow resources and verification budget where applicable. Charge peak bytes including state, optimizer slots, temporary copies and rollback versions, old queries, offline build work, runtime latency and veto/abort costs. Report worst-prefix and worst-task A/C, deadline misses, progress blocked, false-safe release and post-release capacity actually reused. P denotes a primitive candidate (the novelty line names the proposed object); I denotes an improvement or audit, not a primitive claim.

## Idea cards

### Mint, move and retire

#### 1. Retirement witness with a usable capacity receipt (P)
- **Mechanism:** Output the verified replacement, its live domain and a resource-level receipt listing which groups may now be overwritten and which shared readers still block release.
- **Novelty vs nearest prior art:** PR #155 card 2 creates the route, and blue-green swaps versions; the proposed object is the checkable write permission consumed by a later learner before it reuses capacity.
- **Cheapest first test:** Enumerate the three-gate case with optional extra C readers and a later B write. Compare atomic repair, switching installed routes and fresh per-prefix checks under the same scratch cap.
- **Old-task retention check:** Exhaust A/C through construction, cutover and authorized reuse; include a denied reuse that would break C.

#### 2. Independently live, not shadow-assisted (I)
- **Mechanism:** During shadow validation, force the deployed candidate path and cut its access to the retiring route, including cached values and indirect ensemble contributions. Keep public traffic on the incumbent during this check.
- **Novelty vs nearest prior art:** The parent's sufficient-set interventions and Hydra ablations already motivate the isolation; this is a leakage control for blue-green-style shadow comparisons.
- **Cheapest first test:** Give a tiny paired router an optional shared cache and plant candidate outputs that match only while the incumbent fills it. Compare plain shadow agreement and forced isolation with equal probes.
- **Old-task retention check:** Use ordinary A/C with cold caches on the first post-retirement requests, as well as at build and switch prefixes.

#### 3. Build footprint before build quality (P)
- **Mechanism:** Make the candidate generator return an allowed training footprint, including mutable statistics and optimizer slots, before it returns a trained route. Veto training steps that touch the incumbent's protected state.
- **Novelty vs nearest prior art:** Progressive Nets offer isolation by design and GPM protects update directions. The proposed operation admits *construction writes* by validating an explicit effect boundary, even when the replacement is not yet competent.
- **Cheapest first test:** Train a shadow linear head over a mutable two-feature trunk. Plant an unadvertised running-statistics update; compare frozen-backbone expansion, projected replay and full staging with incremental checks.
- **Old-task retention check:** Query ordinary A/C on the dispatching model after every construction step, even if the candidate is later aborted.

#### 4. Drain an old computation, not just a route (I)
- **Mechanism:** At cutover, pin already admitted requests to their old route and state until they complete; transfer compatible state for new requests or reserve room for both states.
- **Novelty vs nearest prior art:** Per-packet versioning already gives the consistency pattern. This measures whether learned cache or recurrent-state compatibility is the binding CL cost, rather than claiming version pinning as new.
- **Cheapest first test:** Interleave two requests to a tiny recurrent classifier whose replacement uses a permuted hidden state. Compare pin-and-drain, exact state translation and two-version blue-green.
- **Old-task retention check:** Score A/C on continuations begun before and after the switch, including one slow request; a wrong completed continuation is a break.

#### 5. Abort without promising time travel (I)
- **Mechanism:** Record a last reversible point. Before it, keep the incumbent intact; after it, permit retirement only under a validated route that does not rely on being able to undo reuse.
- **Novelty vs nearest prior art:** Blue-green rollback is immediate with an intact previous environment, and the ledger rejects save/restore as a mechanism. This audits the consequences of reusing the old bytes before rollback eligibility ends.
- **Cheapest first test:** Reject candidate readiness at each stage of a small handover, including after the incumbent has been overwritten. Compare full clone rollback and validate-then-retire at equal peak bytes.
- **Old-task retention check:** Score A/C and deadlines through all allowed aborts; separately count requests harmed before detection, even if final rollback succeeds.

### Which backups are actually live?

#### 6. Promotion from recovery to fixed-weight service (P)
- **Mechanism:** Use a legal recovery continuation as a proposal generator in shadow, then distill or package its result as an installed route with a tested dispatcher. Promote only after the fixed-weight route passes within deadline.
- **Novelty vs nearest prior art:** PR #139 supplies the recovery witness; PR #155 card 11 classifies service. The candidate operation converts a training-dependent witness into an independently deployable service witness and measures what that conversion costs.
- **Cheapest first test:** Use a tiny gated MLP with one routable dormant head and another needing a labeled update. Compare direct alternate training, the best fixed router and one-step restoration, charging labels and build work.
- **Old-task retention check:** Score A/C during the build and immediately after cutover without recovery or oracle route labels; report recovery-only performance separately.

#### 7. Compile a detector–route–deadline witness (P)
- **Mechanism:** Bind a fallback claim to the input-conditioned detection rule, the actual switch and their joint latency under a declared load; abstain if detection is late even when the alternate predicts correctly.
- **Novelty vs nearest prior art:** MPLS fast reroute already binds failover to detection and delay; CL MoE learns gates. The candidate CL use is a witness that a later writer can use to release the incumbent on *only* the detected input slices.
- **Cheapest first test:** Use two tiny experts with output-matched routes but different detection delays. Compare oracle dispatch, learned dispatch alone and exact bounded reroute with measured costs.
- **Old-task retention check:** Score ordinary A/C under burst arrivals and small held-out shifts; count misroutes, timeouts and oracle-only successes separately.

#### 8. Reroute or relearn: matched-checkpoint causal test (I)
- **Mechanism:** Freeze one checkpoint; compare normal dispatch, admissible fixed-weight switches, and legal weight-changing continuations on disjoint discovery and test inputs. Classify only what is witnessed.
- **Novelty vs nearest prior art:** Hydra ablations and PR #139 recoverability motivate the arms; the added audit is a timing-matched comparison, not proof that a failed switch implies erasure.
- **Cheapest first test:** Use a two-head CPU MLP with planted gate drift and planted representation drift; compare an oracle for the declared gate class, self-repair and one-update continuation on the same B sequence.
- **Old-task retention check:** Retest untouched A/C with normal dispatch and without updates after each B commit. Keep forced-route scores separate from served behavior.

#### 9. Latency can demote a backup without a weight change (I)
- **Mechanism:** Track where a fallback drops out of the live registry as detection cost, contention or queue depth increases; reserve bandwidth only where demotion would strand an old slice.
- **Novelty vs nearest prior art:** Load-aware MoE routing and network failover capacity already motivate the reservation. The CL audit measures changes in admissible B writes caused solely by a serving constraint.
- **Cheapest first test:** Use an event simulator with identical checkpoint accuracy at two arrival rates; compare fixed spare capacity, a load-aware gate and a simple queue-length threshold.
- **Old-task retention check:** Replay ordinary A/C under held-out bursts during B writes and score unavailable fallback capacity separately from output errors.

#### 10. Protect a dispatcher from forgetting its own backups (I)
- **Mechanism:** Treat input-to-route decisions as learned behavior; protect only the dispatcher distinctions needed for old service, allowing harmless route changes where alternatives pass.
- **Novelty vs nearest prior art:** CL MoE already addresses router stability. The improvement is a set-valued service target in place of distilling the original expert ID, with the parent registry as the source of valid alternatives.
- **Cheapest first test:** Train a linear router on three overlapping toy tasks, with two experts equivalent on one slice. Compare frozen gates, top-1 gate distillation and allowed-route distillation at equal B progress.
- **Old-task retention check:** Check actual A/C outputs and deadlines before, during and after router updates, including the rare slice where experts are not interchangeable.

### Spend temporary capacity to earn reusable capacity

#### 11. Peak-byte frontier for local replacement (I)
- **Mechanism:** Search for the smallest scratch subgraph that reaches a safe replacement, including any duplicate consumer and optimizer state needed during overlap.
- **Novelty vs nearest prior art:** Net2Net and Grow, Don't Overwrite already expand safely at initialization; blue-green stages whole copies. This is a budget audit of eventual reclamation, not a claim for safe growth itself.
- **Cheapest first test:** Enumerate adapter sizes and eligible copies for a rank-two linear host. Plot attained B and reclaimed reusable bytes against peak bytes for local handover, full clones, function-preserving growth and permanent expansion.
- **Old-task retention check:** Check A/C at every expansion, dispatch and pruning prefix, including on inputs where tiny rank cannot reproduce A.

#### 12. Reusable scratch slot with a proof of vacancy (P)
- **Mechanism:** Allocate the same scratch slot over multiple B tasks; recycle it only when all old consumers and in-flight requests have left it, or reject the next write.
- **Novelty vs nearest prior art:** PackNet frees capacity with masks and deployment reuses inactive slots. The candidate object is a proof of behavioral non-use under learned dispatch and outstanding old requests, consumed by a later learner.
- **Cheapest first test:** Run a three-task CPU stream where the second handover leaves a rare A reader on scratch. Compare permanent expansion, mask pruning and ordinary reference counts with the same peak bytes.
- **Old-task retention check:** Check every A/C slice and previously learned B task before and after each scratch reuse, including a forced attempted reuse with a late reader.

#### 13. Slice-by-slice handover under a fixed overlap cap (P)
- **Mechanism:** Route certified slices to the replacement piecemeal; retire a shared group only after receipts over the relevant slices jointly cover its entire consumer domain.
- **Novelty vs nearest prior art:** Canary deployment already stages traffic and parent certificates are slice-indexed. The candidate permission is to release *parts* of a shared learned route from certified consumer coverage, not from canary volume.
- **Cheapest first test:** Use three old input regions, two partly shared groups and a cap that precludes full duplication; compare ordinary canary, global cutover and direct constrained repair.
- **Old-task retention check:** Enumerate ordinary A/C and planted slice boundaries after every partial switch; rare unmoved readers must keep their groups protected.

#### 14. Exact morphism, then earned release (I)
- **Mechanism:** Initialize an equivalent expanded model by a function-preserving transform, then learn a smaller independent replacement and test whether it can assume A without the cloned coordinates.
- **Novelty vs nearest prior art:** Net2Net and Grow, Don't Overwrite supply the opening move; the ablation tests whether subsequent reclamation, rather than initialization or extra parameters alone, accounts for gains.
- **Cheapest first test:** Duplicate a hidden unit in a tiny ReLU classifier; compare expansion only, expand-and-prune, shadow training from scratch and expand–handover–retire at equal peak bytes.
- **Old-task retention check:** Measure ordinary A/C after the morphism, every exposed training step and deletion; initialization equivalence is not the post-write result.

#### 15. Spend overlap on future editability (P)
- **Mechanism:** Require a replacement to preserve an interface for a declared subsequent old-task edit, not just today's responses; return which edit families remain reachable after release.
- **Novelty vs nearest prior art:** [Flood triage row 248](https://github.com/manojbajaj95/cl/blob/a23652eb741c8198a672880caeccf111a4222c2a/reviews/flood-triage.md#L248) already protects future revisions. The candidate object pairs a present service receipt with evidence that retirement does not strand a later authorized edit.
- **Cheapest first test:** Build two equal-output linear replacements, one compressing away a controllable A coordinate. Compare endpoint equivalents plus direct future-edit checks and fresh repair with a matched budget.
- **Old-task retention check:** Check A/C at all prefixes; after the held-out authorized edit, score the edited A slice against its new reference and unchanged A/C against their original references.

### Later writers, drift and falsifiers

#### 16. Release stable under declared interference (P)
- **Mechanism:** Test the replacement not only before cutover but over a bounded family of future B writes to the released region. Bind the receipt to that family and invalidate it at the first undeclared effect.
- **Novelty vs nearest prior art:** PR #152 offers finite safe regions and PR #155 offers leases. The candidate consumable is the replacement's verified independence from a released region across a writer class, not merely a safe activation endpoint.
- **Cheapest first test:** Enumerate finite B writes to a retired head, including a common normalization update. Compare fixed masks, incremental endpoint checks and family-wide certification with the same old probes.
- **Old-task retention check:** Execute each advertised B continuation and separately test the excluded family on A/C; no excluded continuation gets credit as covered.

#### 17. Two handovers that cannot overlap (P)
- **Mechanism:** Represent overlap itself as a resource obligation. Reject or serialize two ready transactions when they rely on the same scratch buffer or on each other's soon-to-retire route.
- **Novelty vs nearest prior art:** PR #156 and conventional scheduling already cover safe orders. The candidate input to those solvers is a resource obligation that begins before the replacement has been learned and ends only after live traffic drains.
- **Cheapest first test:** Enumerate two tasks with individually valid local handovers but a shared scratch slot and staggered drains. Compare serial rechecking and generic scheduling supplied with the same resource intervals.
- **Old-task retention check:** Query A/C on every advertised interleaving including pending requests; count concurrency improvements only when B utility and both old deadlines hold.

#### 18. Readiness expires when premises break (I)
- **Mechanism:** Bind readiness to declared producer, consumer, preprocessing and load assumptions; compare invalidating just affected slices against refreshing the entire receipt.
- **Novelty vs nearest prior art:** Row 248's premise-indexed proof invalidation and PR #156's rebase already provide this idea. This tests their economics when late drift can silently demote a ready replacement.
- **Cheapest first test:** Between validation and cutover change one shared normalization statistic. Compare time-based expiry, premise-based invalidation and full incremental verification with the same checker.
- **Old-task retention check:** Hold out A/C inputs sensitive to the changed statistic and issue them before cutover, after it and after a permitted later edit.

#### 19. Held-out retirement challenge (I)
- **Mechanism:** Place untouched old inputs on the other side of a gate or in a rare shared-reader slice. Compare receipts built from endpoint agreement, interventions, and exhaustive checks on a small domain.
- **Novelty vs nearest prior art:** APRNN and Certified CL already distinguish specifications from examples; the audit estimates how often a small probe panel licenses a false retirement rather than just a false endpoint.
- **Cheapest first test:** Enumerate a tiny model with a rare slice visible only after the old group is reused. Match sample and compute cost for random and boundary-focused validation, with exact verification as oracle.
- **Old-task retention check:** Evaluate unselected ordinary A/C continuously and report rare-slice failure separately; a post-release miss is not erased by later repair.

#### 20. Learn the bridge under unknown future requests (P)
- **Mechanism:** Optimize a conditional replacement to cover multiple possible future reuse demands while the incumbent is still live, then allocate it only when the next B objective arrives.
- **Novelty vs nearest prior art:** Progressive Nets preserve capacity, and the parent's flexibility card prices installed branches. The candidate operation builds an independent route once and issues alternative, individually checked release permissions for unseen B families.
- **Cheapest first test:** Make two alternative B pressures on a tiny linear host; compare the best myopic route, equal-budget expansion, stored backup deltas and direct lookahead with held-out B demand.
- **Old-task retention check:** Run each admissible held-out continuation on ordinary A/C, including the class where the bridge cannot issue any receipt.

#### 21. Separate online value from deployment plumbing (I)
- **Mechanism:** Vary service exposure, spare capacity and verifier budget independently, measuring where make-before-break offers something beyond clone–repair–swap with draining.
- **Novelty vs nearest prior art:** Blue-green plus APRNN can implement the workflow; this is the main falsifier for calling it a new CL primitive.
- **Cheapest first test:** Compare exact staging, GPM plus replay, parent-style selection and incremental handover on the same three-gate state space and a small split-digits adapter stream. Compare continuous service and checkpoint-only evaluation at the same attained B.
- **Old-task retention check:** Measure A/C at each allowed request boundary and report worst prefix and worst task separately from the final checkpoint's accuracy.

#### 22. No handover possible at this budget (P)
- **Mechanism:** Return a bounded infeasibility witness (or explicitly abstain) when no allowed path can build a live replacement before the incumbent must be edited.
- **Novelty vs nearest prior art:** PR #152's safe regions and PR #156's impossibility audits already handle infeasible traces. The specific witness identifies the blocking service, resource or deadline constraint and which relaxation opens a handover.
- **Cheapest first test:** Exhaust three-gate variants with no scratch, a shared trunk, insufficient drain time and a feasible case hidden from greedy search. Compare exact reachability, scheduler failure and generic constraint solving on the same model.
- **Old-task retention check:** Verify A/C on every claimed relaxation and on feasible fallback windows; report refusal and foregone B utility rather than counting “do nothing” as a successful write.

## Ranked deeper questions

1. **Does continuous service plus certified reclamation buy a new CL operation?** Hold route candidates, budgets and attained B fixed. Compare a later learner consuming the receipt against blue-green/atomic joint repair plus incremental checks, PR #156-style safe trace scheduling and the parent choosing among installed backups. Require either more reusable capacity at the same worst-prefix A/C and deadline or lower total verification cost at the same capacity. If the best combined control matches both, keep the technique but drop the primitive claim.
2. **What fraction of apparent backups qualify for timely live service without privileged dispatch?** Predeclare old slices and writer families; compare normal serving, fixed-weight legal rerouting and training-only recovery in identical checkpoints. Quantify uncertainty, abstentions and common-mode failures. If most candidates are recoverable only after training, focus on build cost, not redundancy counts.
3. **Is temporary overlap really cheaper than keeping old capacity?** Find the frontier in peak bytes, training/query work, deadlines and steady-state capacity across a long bounded stream. Count actual reuse by later tasks. If local handovers only win with uncharged clones, old labels or idle traffic, the economics fail.
4. **Which provenance makes retirement stick across later learning?** Test reuse with stale dispatchers, shared consumers, changed write maps and requests crossing a version boundary. Compare proof reuse to equally incremental re-verification; false-safe releases kill the advertised guarantee, and high abstention narrows where it applies.
