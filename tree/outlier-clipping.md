# Outlier-only clipping: carry old-task certificates through a shrink without erasing the audit

**Status:** Ideas only. The arithmetic examples are sanity checks, not pilot results. All first tests below are proposals for pencil-and-paper or CPU work; no GPU.

**Parent:** [Nonlinear shrink](nonlinear-shrink.md) ([PR #232](https://github.com/manojbajaj95/cl/pull/232)). Related: [Order relays](https://github.com/manojbajaj95/cl/pull/216), [safe-order families](safe-order-families.md), and [two-clock examples](two-clock-examples.md).

**Review seeds:** [Flood triage, line 344](https://github.com/manojbajaj95/cl/blob/ec716d67cef5349f3d783e2261308c958af296e6/reviews/flood-triage.md#L344) gives score 3 to **#232#02**, bulk-preserving saturation, and **#232#18**, detect before you contract or keep the misreport visible after contraction. Read [the idea ledger](https://github.com/manojbajaj95/cl/blob/ec716d67cef5349f3d783e2261308c958af296e6/reviews/idea-ledger.md) first: count real retention, not just shrink; compare with the best components stacked together at equal budget; include the [smooth/accumulation null from PR #113](https://github.com/manojbajaj95/cl/pull/113). Improvements below are controls or questions, not pilot nominations.

## What must survive the clip

- **Keep the original proof valid on a fixed protected set.** Freeze the protected histories `K` and the claimed reachable set `H` before looking for an opener. An opener must leave the entire state used by the existing A/C certificate unchanged on `K`, including any optimizer slots, RNG, step counter, or clock that affects the certified suffix. Exact identity on a projected state suffices only if the original proof already covers every change in the omitted state and its effects on the suffix. If the original proof needs absolute time and the opener consumes a tick, the proof does not carry. Check the outlier image `T(H \ K)` separately, including landings on the clipping boundary. Do not call a newly chosen `K`, an unchanged accuracy score, or a newly proved equivalence an untouched certificate.
- **Keep enough evidence to distinguish what the contract forbids.** Freeze admissible histories `H` and violations `D` relative to a particular suffix and its provenance obligations. For an audit observation `q`, require disjoint honest and prohibited observation sets at its actual precision (including rounding/noise). For a post-shrink audit use `q ∘ T`, plus any separately priced, trustworthy receipt. A collision that fully repairs the state is not a residual safety failure if the contract is only about suffix safety; it can still violate a stated provenance obligation. Conversely a claimed-set membership check on a lossy summary is not a proof of safety. Unknown histories outside the certified threat model require conservative refusal or replay, not extrapolation.
- **Price the whole relay.** Compare legal, truthfully labeled examples drawn from a fixed pool under the same optimizer and thresholds. No new clip knob, hidden-state oracle, free pre-clip statistic, or reset in a teaching arm. Match new-task B gain, steps/examples, stored and transmitted bytes, verifier work and deadline; record any unmatched resource separately. Measure two residual orders actually admitted, proof reuse/work, hazardous admissions and honest refusals, and A/C before the seam and after each suffix (including the worst old slice and rejected-path fallback). Include an outlier-free pack where the identity arm should tie. A finite enumeration proves only its defined host, not a real learner.

### Nearest prior art and the narrower claim

- [Adafactor](https://arxiv.org/abs/1804.04235) clips updates, and [clipped AdaGrad under heavy-tailed noise](https://arxiv.org/abs/2406.04443) uses clipping for optimization stability (abstracts checked through HF Papers). Ordinary winsorization, Huber's clipped score and trimming are also controls: moving a tail is not new. A gradient cap that leaves *gradients* unchanged in range can still move the model and age its slots. The claim here is identity for the protected state under a **selected truthful transition**, with an existing retention proof that remains usable.
- [Iterative Machine Teaching](https://arxiv.org/abs/1705.10470) selects examples to speed learning; [interval bound propagation](https://arxiv.org/abs/1810.12715) certifies bounded perturbations through nonlinearities; [OGD](https://arxiv.org/abs/1910.07104) seeks to preserve old outputs by gradient projection. These are teaching, range verification and functional preservation baselines, respectively. None is taken here as evidence of an unmodified full-state certificate through a legal teaching step. The parent already has affine contraction, exact-tail saturation arithmetic, injective shrink, and a norm-only collision; don't claim those again.
- [Proof-of-Learning](https://arxiv.org/abs/2103.05633) and replay-based training witnesses are audit controls; active fault diagnosis already asks for distinguishable traces. Signatures authenticate a report, not its semantic accuracy. The narrower question is whether a **particular allowed order or retained observation** preserves the distinctions needed by an independently checkable schedule admission without redoing all prior retention or audit work. These are nearest comparisons, not an exhaustive priority claim.

### Paper sanity checks

**O1 — A truthful tail-only transition, not merely an update cap.** Take a one-coordinate ReLU model predicting `max(h − x, 0)` on a toy B task with target zero at `x = 1`. A legal unit SGD step on half squared error gives `T(h) = h − max(h − 1, 0) = min(h, 1)`; the threshold is the input of a fixed, truthfully labeled example, not an optimizer setting. With `H = {0, 1/2, 3/2}`, `K = {0, 1/2}`, and old-task readout `h + d` required in `[−1, 2]` after residual shifts `d = ±1`, only `−1` is safe across `H` before the example; both are safe after it. B loss on the example drops from `1/8` to `0` for the tail and is already zero on `K`. Both existing in-range safety checks transfer; the new landing `1` needs its own check. No momentum or time-sensitive proof here. An affine map fixing both `0` and `1/2` is identity in this coordinate, but the fair affine rival may move the bulk and cheaply recheck; this example doesn't establish an economic win.

**O2 — A collision even when the schedule is repaired.** Underreporting a true prefix `h = 5/2` as one in `H` violates a declared prefix bound `h ≤ 3/2`. A trusted preceding magnitude `|h|`, rounded down to a multiple of `1/2`, distinguishes this case from `H`. After O1 the excluded prefix and the honest tail both export `h' = 1`; no statistic of `h'` fixes the collision. A trusted one-bit observation of `h > 3/2`, bound to the pre-state and opener, would survive the collision, but a bit computed by the reporting hop does not establish it. The example repairs suffix safety, not provenance. A skip from `3/2` to `7/4` already defeats the rounded pre-observation; refuse this envelope, refine the observation, or recheck. To test safety-critical collisions as well, use the parent's N5c equal-norm/unequal-coordinate fixture with a suffix sensitive to the excess coordinate; don't credit catching O2 as catching N5c.

## Idea cards

**P** = candidate primitive (the new reusable object is named); **I** = improvement or required control. All tests use the shared budget and retention rules above. For hand fixtures, A/C may be distinct old readouts with explicit floors; passing those is not evidence of real continual-learning retention.

### Tail-only teaching and proof reuse

#### 01. Identity-on-core opener (P; #232#02 seed)
- **Mechanism:** Select a truthful opener that is identity on a pre-certified core and brings the reachable tail into the two-order safe region. Export the old proof identifier plus only a proof of the tail landing.
- **Novelty vs nearest prior art:** O1 extends the parent's saturation arithmetic to a legal example; the reusable output is a tail-only amendment to a live certificate, not a clipping rule.
- **Cheapest first test:** Enumerate labeled hinge examples on O1 and on an outlier-free pack; compare against generic contraction plus full recertification, a direct reset, and the illegal threshold-change ceiling at matched B gain.
- **Old-task retention check:** Reuse unchanged A/C proofs for the core; independently check both A/C readouts on the landing and after both orders.

#### 02. Landing in an existing proof cell (P)
- **Mechanism:** Target the tail at a previously certified *interior* cell of the safe region instead of a freshly fitted boundary. Attach a membership proof to the old cell, which already covers both suffixes.
- **Novelty vs nearest prior art:** IBP supplies a cell enclosure; the new object is a target that can accept landed histories from several importers without extending its retention proof.
- **Cheapest first test:** Enumerate rational teachers for two importers with different outlier sets; compare against fresh IBP on each image, cached under the same proof-byte limit. Include a landing that only intersects the target.
- **Old-task retention check:** Test both orders on every landing and on interior-cell extremizers for A/C; revoke on boundary leakage.

#### 03. Two one-sided openers instead of a global cap (P)
- **Mechanism:** Pick a right-tail item and a left-tail item from different B queues. Certify that each fixes the core **and** the other item's reachable landing, so both opener orders remain legal when arrivals swap.
- **Novelty vs nearest prior art:** A two-sided clamp is standard; the candidate is a certificate of interchangeability for separately arriving truthful items under fixed optimizer settings.
- **Cheapest first test:** Enumerate paired hinges with one arrival delay; control for a two-sided clamp plus a no-op and two examples selected only for B loss. Include a pair whose landing activates the other gate.
- **Old-task retention check:** Check A/C after each prefix, including the longer wait, not just at the shared final state.

#### 04. Exceptions to proof reuse by dependency (P)
- **Mechanism:** Publish the set of protected proof dependencies read by the opener and the tail suffix. Invalidate only those proofs whose dependencies can change, including reads through shared optimizer slots or clocks.
- **Novelty vs nearest prior art:** Incremental verification already tracks dependencies; the reusable object here is an invalidation certificate spanning both model and optimizer state through a teaching seam.
- **Cheapest first test:** A two-block learner with a shared step counter; compare with ordinary blockwise clipping plus incremental recertification. A weight-only dependency map must fail when bias correction depends on the counter.
- **Old-task retention check:** Use A/B-overlap and C-only probes, and check that every falsely reused proof is rejected when the shared state changes.

#### 05. Repeated clipping with a fixed protected set (P)
- **Mechanism:** Export one core proof across hops and accumulate only reachable tail-image obligations; fire the next opener only when a certified arrival threatens one of the two orders.
- **Novelty vs nearest prior art:** [Order relays](https://github.com/manojbajaj95/cl/pull/216) propagate width, not a reusable protected set plus a sequence of local amendments.
- **Cheapest first test:** Enumerate four hops with a repeating exceptional branch; compare periodic saturation plus cached rechecks with the same storage. Include a branch that leaves the core under a later legal step.
- **Old-task retention check:** Check A/C at every hop, particularly C on a branch newly outside the core; do not silently redefine the core.

#### 06. True no-op under a live optimizer (P)
- **Mechanism:** Search lawful routed examples whose inactive branches are skipped by the deployed optimizer, preserving both their moments and any clock used by the original proof. Treat a zero gradient with unconditional moment decay as a non-no-op.
- **Novelty vs nearest prior art:** Sparse updates already skip inactive parameters; the new deliverable would be a truthful opener plus a backend-specific proof of exact replay equivalence on the core.
- **Cheapest first test:** Enumerate one-example transitions in a tiny conditional learner under absent versus zero gradients and AdamW with weight decay; compare sparse ordinary replay and generic contraction with recertification.
- **Old-task retention check:** Check cloned A/C traces through several consuming steps; any hidden drift invalidates proof reuse even if immediate accuracy matches.

#### 07. Tail-only release across importers (P)
- **Mechanism:** Share a proof of core identity with several importers, but compute the tail landing against the intersection of their reachable safe cells. Publish the particular importer conflict when no truthful example can satisfy all.
- **Novelty vs nearest prior art:** PR #216's Helly gate concerns a shared teaching amount; this order contract reuses the old-task proof for exact core identity while keeping incompatible tail constraints visible.
- **Cheapest first test:** Enumerate three importers with different directed suffixes; compare per-importer openers and a same-byte history bit plus ordinary admission. Include a disjoint intersection.
- **Old-task retention check:** Measure A/C separately per importer; averages cannot hide an importer whose old path is harmed.

#### 08. Minimum proofs touched, not minimum distance (I)
- **Mechanism:** Rank legal examples by certified proof work invalidated after imposing a B-gain floor and two-order feasibility, not by parameter displacement or discarded slot mass.
- **Novelty vs nearest prior art:** A change to the objective relative to the parent's least-displacement comparison; no new transition.
- **Cheapest first test:** Compare O1-style openers with affine and smooth-clip controls at matched B gain and proof-cache capacity. Include a core-dense host where caching makes the affine rival cheaper.
- **Old-task retention check:** Match A/C thresholds and use the same cached proof granularity in every arm.

#### 09. Can the provenance cause itself produce the tail? (P)
- **Mechanism:** Certify that different lawful prefix orders yield the same public weights but only a known branch reaches the clip region. Use that branch predicate for a local proof obligation, not for choosing a different example for each hidden history.
- **Novelty vs nearest prior art:** Unlike robust clipping for random heavy tails, the proposed object is a proof of tail membership tied to a reachable order in the relay.
- **Cheapest first test:** Enumerate a small queue with momentum and colliding public weights; compare against initial-state balls and cached exact search. Discard synthetic tails unreachable under either legal prefix.
- **Old-task retention check:** Replay A/C from every lawful prefix, with reported tail membership scored independently of B gain.

#### 10. Future consumer disqualifies an apparently free clip (I)
- **Mechanism:** Append an A- or C-consuming step that reads a slot the immediate old-task head cannot see, then price the resulting recertification.
- **Novelty vs nearest prior art:** A negative test for weight-only preservation and the parent's immediate shrink metric.
- **Cheapest first test:** Construct two states with equal weights and distinct momentum; compare weight-only cache reuse with full-state proof reuse and exact suffix replay.
- **Old-task retention check:** Require A and C after that consuming step; a pass before it is not retention.

### Certified order and evidence that survives shrinking

#### 11. State-bound audit barrier (P; #232#18 seed)
- **Mechanism:** Admit `audit → shrink → suffix` only with a valid receipt bound to the same pre-state commitment, optimizer/version, observation scope and opener; invalidate it on any unaudited intervening write.
- **Novelty vs nearest prior art:** Authenticate-and-check first is the stacked baseline. The candidate is a state-scoped order rule that can admit independent rearrangements without repeating the check; a serialized barrier alone is not new.
- **Cheapest first test:** Enumerate a four-event DAG with one independent event and one slot-changing event; compare with detect-then-synchronize ([PR #213](https://github.com/manojbajaj95/cl/pull/213)), shrink-first, and signed checkpoint plus recheck.
- **Old-task retention check:** Check A/C at both admitted orders and on the fallback path when a stale receipt is refused.

#### 12. A bit for the collided class, not the hidden history (P)
- **Mechanism:** Within each post-clip observation class, retain only a verified bit distinguishing the histories that would change admission. Do not spend bits separating two repaired histories with no provenance obligation.
- **Novelty vs nearest prior art:** Quantization and the parent's minimal publication are precedents; here the residual ambiguity *after a chosen clip* defines exactly which distinctions the witness must retain.
- **Cheapest first test:** Enumerate O2 and a harmless collision; compare fixed-width pre-state sketch, precheck, and checkpoint/replay at equal byte and verifier budgets. Test whether the bit can come from an already trusted trace.
- **Old-task retention check:** Run both suffixes on every accepted collision class and compare A/C of the conservative fallback when the bit is absent.

#### 13. Choose the clip by the audit partition (P)
- **Mechanism:** Among equally good truthful openers, keep only those whose quantized post-images never put an honest history and a prohibited one in the same observation bin. Allow merging within either class.
- **Novelty vs nearest prior art:** Parent #08 requires injectivity; this asks only for sufficiency for the stated decision. Unlike generic active diagnosis, the same legal transition must open both orders and fix the core.
- **Cheapest first test:** Enumerate alternative gate directions for a two-slot hinge host with a fixed block observation; compare generic injective shrink plus audit and plain active diagnosis followed by synchronization. Include an instance in which every eligible clip collides.
- **Old-task retention check:** Require unchanged core A/C certificates and verify both A/C suffixes on tail images; test equality at bin boundaries.

#### 14. Independent audit coordinate (P)
- **Mechanism:** Clip the order-sensitive slot but choose a lawful opener that leaves an already observable, correlated witness slot alone. Certify separation under the actual joint support, not under a convenient factorized model.
- **Novelty vs nearest prior art:** A checkpoint preserves all coordinates; the candidate primitive preserves just a pre-existing witness under a learning transition. If the witness is a newly instrumented history flag, it is card 12's receipt instead.
- **Cheapest first test:** Use a two-slot rational host with legal prefixes that correlate slots; compare a paid coordinate probe plus shrink and a generic block sketch. Add a reachable history that breaks the correlation.
- **Old-task retention check:** Check A/C under both orders with a later consumer of the audit slot, so keeping it cannot hide deferred interference.

#### 15. Reordering audit around locally harmless writes (P)
- **Mechanism:** Certify that a pending write preserves the audit decision on *both* honest and prohibited preimages, even if the raw score changes; then let it cross the barrier. Expire the permission on the first write not carrying such a proof.
- **Novelty vs nearest prior art:** Ordinary read/write commutation is stronger than needed; the candidate is commutation of a specific audited predicate on reachable optimizer states.
- **Cheapest first test:** Enumerate an audit and three legal writes; compare strict audit-first and dependency-based topological sort, including a write preserving honest scores while merging a dishonest one.
- **Old-task retention check:** Test A/C at every certified prefix and on any formerly valid branch lost to the new order rule.

#### 16. Spend a diagnostic example only on unresolved cells (P)
- **Mechanism:** Use a sound three-way audit: certainly honest, certainly prohibited, or unresolved. Only the unresolved cell consumes a pre-shrink diagnostic; the diagnostic and its own state changes are part of the certified order.
- **Novelty vs nearest prior art:** Adaptive diagnosis already saves tests; the candidate is a schedulable conditional diagnostic whose refusal and write effects are explicit in the retention proof.
- **Cheapest first test:** Adapt O2 to intervals around the bin edge; compare always-check-first and replay-on-uncertainty with the same expected and worst-case budgets. Do not select the cell using the hidden true history.
- **Old-task retention check:** Check A/C on diagnostic and no-diagnostic branches, and after refusal with matched waiting time.

#### 17. Certify repairs separately from caught violations (P)
- **Mechanism:** Where no prefix provenance obligation applies, permit undistinguished histories only if every possible member of their observation class becomes safe for both suffixes. Otherwise require distinguishability or deny admission.
- **Novelty vs nearest prior art:** Robust verification proves safety over uncertainty; the candidate is a relay admission outcome that explicitly carries repaired-but-unverified history instead of silently upgrading it to honest.
- **Cheapest first test:** Pair O2's repaired alias with N5c's safety-relevant norm alias; compare universal rechecking and reject-all aliasing. Include an old-task readout that reverses which alias is harmless.
- **Old-task retention check:** Universal A/C floor over each accepted repaired class after each suffix, not A/C on a representative.

#### 18. One trustworthy observation covers adjacent shrinks (P)
- **Mechanism:** Before the first of two clips, obtain a joint receipt for just the exclusions that the ordered suffix needs; transfer its scope through the first image only if no new unobserved branch can introduce a violation.
- **Novelty vs nearest prior art:** Periodic re-anchoring and batched verification are controls; novelty would be composing audit coverage across selected information-losing teaching transitions.
- **Cheapest first test:** Exhaust a two-seam relay with a shared prefix and a fresh skip between seams; compare per-seam bits and periodic checkpoint plus replay. The fresh skip must force a new check or refusal.
- **Old-task retention check:** Carry and independently test A/C after the first seam and every second-seam suffix; audit reuse is not retention reuse.

#### 19. Audit order counterexample as a deliverable (I)
- **Mechanism:** When there is no usable order, return the shortest reachable honest/prohibited pair that collides at deployed precision, including which suffix or provenance clause makes it matter.
- **Novelty vs nearest prior art:** A counterexample-guided verification diagnostic, not a new learner; it distinguishes an information limit from a search timeout.
- **Cheapest first test:** Exhaust small traces with norm and block summaries; compare exact pair search with interval-overlap refusal, including honest wide uncertainty and a real violation just inside the tolerance.
- **Old-task retention check:** Replay both witnesses and the fallback on A/C, separating refusals of honest runs from prevention of real old-task breaches.

### Joint tests and controls

#### 20. An opener consumes the evidence deadline (P)
- **Mechanism:** Give the audit a real deadline tied to the first transition that can merge the relevant classes. Certify a pair of residual schedules only when the audit and both suffixes still fit their own arrival deadlines.
- **Novelty vs nearest prior art:** [Two-clock examples](two-clock-examples.md) separate learning deadlines; the proposed certificate uses loss of observability to constrain the ordering of learning and audit.
- **Cheapest first test:** Enumerate a queue where one early truthful opener invalidates later auditing, another delays B, and a third preserves the witness. Compare detect-first synchronization and high-precision audit under matched latency.
- **Old-task retention check:** Measure A/C after the complete schedules and after the longer fallback wait, with B deadline misses counted independently.

#### 21. A staged audit that saves the core proof (P)
- **Mechanism:** If a trusted statistic is sufficient to route a history to the certified core or the tail proof, attach the audit only to tail transitions while proving that no prohibited tail can masquerade as core. Do not trust the hop's self-reported route.
- **Novelty vs nearest prior art:** Selective checking is standard; the new obligation is to preserve an old proof and a trust decision with the same independently checkable partition.
- **Cheapest first test:** Three bins (core, tail, unresolved) in a tiny clipped relay; compare unconditional audit plus cached recertification. Inject a prohibited tail with a core-sized update norm.
- **Old-task retention check:** Separately score A/C on accepted core, accepted tail, and refused honest histories; any undetected cross-bin safety leak kills the scheme.

#### 22. Kill test against the strongest stack (I)
- **Mechanism:** Put matched truthful affine/smooth learning, accumulation, cached retention checks, and a replay-backed audit before synchronization in one baseline; ablate each component only to attribute a surviving gap.
- **Novelty vs nearest prior art:** The ledger's stacked-baseline rule, not a primitive.
- **Cheapest first test:** A tiny CPU split stream with one rare tail and one diffuse host, checking a finite set of allowed schedules. Compare two-order admission at matched B gain, proof work, bytes, latency and hazardous admissions. No credit for a win over an intentionally weaker audit.
- **Old-task retention check:** Held-out A/C accuracy and worst A/C slice before the seam and after each suffix; report attrition and fallback retention along with successful admissions.

## Ranked deeper questions

1. **Does a fixed truthful pool contain any exact core-preserving opener when the real proof reads optimizer state and time?** Start with cards 01/06/09. If clocks or decay destroy identity, or the reachable tails disappear, the saturation arithmetic is not a certificate-reuse result. If the legal opener exists but cached affine recertification ties it at equal B gain, stop this branch.
2. **Can a useful shrink preserve the audit decision rather than the whole history?** Use cards 12–14/17 on quantized, reachable history pairs. Find the least trustworthy extra information that closes the harmful collisions; if it costs as much as checking first, prefer the explicit audit-first order. Keep repair and provenance separate.
3. **When can a certified partial order beat a serialized precheck?** Use cards 11/15/20 against check-then-synchronize with the same retention cache. Require a legal second order or a real deadline win; a signed receipt alone is a tie.
4. **Does proof reuse amortize across genuinely different importers without loosening the old-task floor?** Use cards 02/05/07/18 and control for ordinary cache hits. Publish the first incompatible landing or newly unobservable branch, not just the successful rounds.

**Verdict:** Conditional primitive only if a truthful tail-only step carries an existing retention certificate unchanged and opens usable orders with a sound audit at lower cost than the matched stack. Otherwise keep the collision counterexamples and use audit-first plus ordinary recertification.
