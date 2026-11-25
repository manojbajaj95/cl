# Split C state: copy only what the handover needs

**Status:** Ideas only; two paper fixtures and proposed CPU first tests, no training or GPU. **Parent:** [Standby handovers](standby-handovers.md) ([PR #267][parent]). **Review seeds:** [Flood triage row 383][triage] scores #267 cards 07 and 19 at 3. Train C so the third lane duplicates only its necessary state, not the state it can lawfully share with the standby's B finish. Make one transferred C response pay a required signed tail installment via its ordinary update. Cards 01 and 09 restate those seeds as controls.

**Ledger read first:** The [idea ledger][ledger] rejects exact restore as a new capability and requires the strongest stack of simple controls and ordinary old-task service. **P** marks a candidate primitive (a reusable object or operation); **I** marks an improvement or audit, not a pilot candidate. These are proposer labels, not reviewer verdicts.

## What would count

- **A split defined by service and failures, not by parameter names.** A and C are ordinary old tasks; B is the incoming task. The third lane keeps its own old workload. Let S denote state both the B standby and the receiving C lane are allowed to use from a single surviving source, and R denote the C state the receiver needs independently. Only R is duplicated; charge queues, version maps, read leases, stale copies, optimizer state and validation as well as weights. At the cut preserve arrival, pinned version, deadline, and exactly one visible result/write. Test normal service, primary loss, and declared correlated failures. If S is absent, corrupted, or changes incompatibly during B's finish, a valid split must avoid that dependency within the budget or refuse and account for lost B and any missed C. Do not silently recover S from the retired lane.
- **A payment defined by executed reader effects, not by gradient alignment.** The recipient must deliver the actual pending C response by its original deadline. Its standard update, with the original semantics, supplies one needed signed effect at its original reader, prefix and magnitude; the other working partner supplies the complement. Both must be necessary under the same rights. Track realized drift continuously at observable prefixes, including between writes. For adaptive hosts run the actual joint suffix (including optimizer state and any no-op); summing stand-alone estimates or reporting tick-end cancellation is not sufficient. No separate rescue write, altered target or credit for a refused response.
- **Compare costs on the same frontier.** Freeze training, routing, cut semantics and authority before blind faults and requests; the runtime only sees public state. Stack lawful version-aware routing, checkpoint/replication or fixed selective placement, shared/private training, and constrained updates with exact joint scheduling on tiny domains. Give the strongest stack the same observations, permissions, data, preparation, B utility and start margins. Match resident/peak bytes, update work and occupied slots (or report the Pareto frontier). On the same host with the same actions exact search already includes any feasible schedule: test its online cost, or compare the feasible sets of trained hosts instead. Keep refusals and fallback costs in the denominator.

**Nearest work (targeted alphaXiv and Hugging Face Papers check; not exhaustive):** [Adversarial Continual Learning][acl] and [LoDA][loda] already learn shared/private representations or subspaces; neither abstract establishes a minimal replica that serves pinned C versions through a specified B call-up. [Hot standby][hot] and [incremental snapshots][snapshot] already cover replicated service and selective physical copying. [GEM][gem] and [PCGrad][pcgrad] already impose old-loss constraints or resolve gradient conflict; changing loss weights or projecting a gradient is not new here. The discriminant is whether a deadline-bound C update is itself a necessary signed payment at a real observable prefix when the equally resourced stack cannot achieve that service. [PR #256][working] already proposes correction-paid tails; #267 adds the transferred request.

## Exact paper fixtures, not novelty claims

**R · One shared read, one private copy.** The standby uses the surviving read-only scalar `s=1/2` for B. C serves version-pinned requests by returning `s+r_v` with `r_1=-1/4`, `r_2=1/4`. On call-up the old C store is unavailable; the third lane can return both `1/4` and `3/4` at the original deadlines using copies of the two residuals plus the single shared s. Full replication copies three scalar values, and current-only replication can miss v1 even if v2 is right. With the same two residuals and `s=1/4` versus `s=1/2`, the C answers differ, so loss of the only S source cannot be masked by those copies. This counts scalar copies only (not metadata); a hand-placed version-aware split ties it.

**T · One ordinary response, one necessary signed effect.** Start with old-reader drift `(1/4,1/4)` in the closed box `[-1/4,1/4]^2`. P's ordinary work contributes `(-1/4,0)`; the survivor's required B step contributes `(1/4,1/4)` and must run after P and Q's slots. Q's only early slot is owed to a transferred C correction: answer after one ordinary unit-rate SGD step on `(q-t)^2/2`, starting at `q=0` with truthful target `t=-1/4`. The second reader includes q with coefficient 1 and the first does not read q, so Q contributes `(0,-1/4)` and delivers the requested correction. The prefix drifts are `(0,1/4),(0,0),(1/4,1/4)`. Omitting P or Q's effect leaves one reader at `1/2` after B. The otherwise lawful request `t=+1/4` with the same update fails immediately at Q's prefix; serving that request safely by some other means, or refusing B, is part of the comparison. Untouched C queries can read an independent coordinate. A scheduler with the same update already takes the good action; this fixture only checks the semantics.

## Idea cards

### Learn what must survive the cut

#### 01. Isolate the C-only residual (P, #267 seed)
- **Mechanism:** Train the ordinary C representation with a common S read and a C residual R that the third lane holds independently; train with the retiring C store masked, then freeze placement before blind events.
- **Novelty vs nearest prior art:** [LoDA][loda] already decomposes state; the candidate object is a service-equivalent replica defined by a real failure cut and pinned queue, not a task-private feature space.
- **Cheapest first test:** Fit a four-feature linear host with two versions and execute fixture R variants; compare #256 full reassignment and multi-view standby, checkpoint recovery, hand-placed selective and equal-byte full replication. Remove a shared feature both lanes cannot replace.
- **Old-task retention check:** Serve both C versions on deadline, run ordinary A and third-lane work during the fault, and score B's finish and old-task performance on refusal.

#### 02. Choose the split by separating possible futures (P)
- **Mechanism:** Learn a replica code by pairing histories with the same surviving S but different lawful future C replies or updates. Force the code to separate those pairs; let it merge histories with identical future service.
- **Novelty vs nearest prior art:** State equivalence and #267 card 02's sufficient statistic are the controls. The candidate object is a learned equivalence conditional on the B finish trajectory, including future C writes, not a code fitted to an answer snapshot.
- **Cheapest first test:** Enumerate two-bit histories and two-tick B suffixes; compare exact equivalence classes, ordinary output distillation and a learned code. Hold out a pair that first separates on the second C update.
- **Old-task retention check:** Execute both updates, fresh C reads thereafter, A across B, and the receiver's old work; reject any merge that erases a pinned reply.

#### 03. Share an immutable basis, not a moving interpretation (P)
- **Mechanism:** Train a stable basis S for both lanes while their own residuals absorb updates; release any pin only at a declared cut where the pending C queue can use the new basis without translating hidden old state.
- **Novelty vs nearest prior art:** Version pinning and [shared subspaces][loda] are old. A candidate operation is trained basis rollover at a service-preserving cut, with no second basis resident during the B/C overlap.
- **Cheapest first test:** Rotate a two-dimensional basis across three ticks; compare copy-on-write pinning, frozen basis forever and trained rollover. Include overlapping pinned readers that genuinely need both bases.
- **Old-task retention check:** Query A and old and fresh C immediately before/after rollover, run routine receiver updates, and score B and peak bytes when rollback is required.

#### 04. Learn failure classes from crossed dependencies, then freeze them (I)
- **Mechanism:** Intervene on state sources during preparation and assign residual placement by which sources actually fail together under a declared physical fault, not by activation covariance.
- **Novelty vs nearest prior art:** Failure-domain placement is standard; this is an improvement only if interventions make a learned split cheaper than architecture masks or placement on a known dependency graph.
- **Cheapest first test:** Cross source loss and version demand in a four-source host; compare covariance, exact dependency masks and interventions. Hold out a correlated failure that kills two apparently disjoint features.
- **Old-task retention check:** Run A and both pinned and ordinary C on each window, including fallback when the receiver cannot safely answer.

#### 05. Copy the update state that makes a handover continue (P)
- **Mechanism:** Train a recipient with independent residual momentum only for directions where it affects post-cut C service; rederive the rest from the permitted surviving clock and inputs, not the old optimizer.
- **Novelty vs nearest prior art:** Optimizer-state checkpoint thinning and reset are strong controls. The candidate replica object preserves response *and* legal continuation under scoped state, not just today's logits or a small checkpoint.
- **Cheapest first test:** Use two-dimensional momentum SGD with histories sharing weights but opposite moments; compare full state, reset, and fixed or learned one-dimensional copies on two post-cut updates.
- **Old-task retention check:** Score A, pinned C and unseen C after both real updates, plus B and the receiver's untransferred old workload.

#### 06. Decouple the one shared dependency that can actually fail (P)
- **Mechanism:** Withhold one shared feature during ordinary C training and teach R to replace only its C contribution on that public fault. Keep S available to B on the permitted path; if B also loses it, treat that case separately rather than claiming coverage.
- **Novelty vs nearest prior art:** Feature dropout and hot replicas are known. The candidate is asymmetric substitution for a specific broken C read while keeping the shared B path and the pinned C contract intact.
- **Cheapest first test:** Remove one of two read paths without removing the source, then remove the source itself. Compare fixed substitution, standard dropout and full replication at matched bytes.
- **Old-task retention check:** Test A and held-out C both under the local path cut and common-source loss, recording original deadlines and B refusals.

#### 07. Make C dependency birth pay for its copy before exposure (P)
- **Mechanism:** When an ordinary update makes a new coordinate essential for a supported C version, require preparation of its independent residual before publishing that version; otherwise keep serving the old contract and record the deferred update.
- **Novelty vs nearest prior art:** Write-ahead replication ensures durability before acknowledgment. The candidate admission rule uses *new semantic dependencies* rather than dirty bytes; a dependency-aware transactional scheduler is a direct control.
- **Cheapest first test:** Alternate writes that touch many bytes but add no C dependency with a one-coordinate update that does. Compare dirty-byte logging and fixed dependency tracking under a one-slot copy limit.
- **Old-task retention check:** Serve A, old C and newly admitted C, count deferrals as lost work, and exercise primary loss between prepare and publish.

#### 08. Test whether a trained split survives a change of receiver (P)
- **Mechanism:** Train several useful lanes to reconstruct the same R semantics from their own local bases using a small shared interface; accept only where the receiving lane covers its ordinary workload too.
- **Novelty vs nearest prior art:** [Adversarial Continual Learning][acl] already separates shared and specific features, and #267 card 08 transfers by capability class. The candidate is an interchangeable *replica code* with no copy of each sender/receiver pair's basis.
- **Cheapest first test:** Hold out one sender/receiver pairing among three linear lanes; compare pairwise adapters, a frozen universal decoder and full copies. Include an incompatible receiver basis.
- **Old-task retention check:** Run all three lanes' routine held-out work and A while the held-out pairing serves both pending C versions; count failed admissions.

### Turn a real C response into a necessary payment

#### 09. Pay through the transferred response's ordinary update (P, #267 seed)
- **Mechanism:** Train Q so serving a specific pending C correction through its ordinary update provides its required signed effect; leave P responsible for the other required installment.
- **Novelty vs nearest prior art:** #256 card 19 pays with corrections and #267 card 19 brings a migrated correction. The reusable action would jointly discharge *that request* and a reader/prefix obligation without a second step; this is not new merely because [GEM][gem] keeps old loss down.
- **Cheapest first test:** Execute T and then learn rather than stipulate its shared direction. Give exact scheduling to separate and joint training; compare #256's split with a separate payment, correction-paid tails without migration, restarting the pair and an equal-compute rescue. Remove each partner in turn and use the wrong-sign target.
- **Old-task retention check:** Score the actual response, Q's own old work, A/C at every intermediate read and held-out untransferred C thereafter.

#### 10. Train signed response families, not a bias toward one tail (P)
- **Mechanism:** Learn a representation where truthful C correction pairs with opposite residuals can realize opposite reader effects, while the public queue/debt only selects among already legal due requests. It cannot fabricate requests or skip a head that must run.
- **Novelty vs nearest prior art:** [PCGrad][pcgrad] alters gradients when tasks conflict. Here a pre-trained family offers both signs through ordinary updates, with each offer contingent on request precedence and a real reader.
- **Cheapest first test:** Use two pending linear corrections with opposite effects, legal ties and strict FIFO; compare exact order search, GEM, and separately trained sign adapters. On the strict FIFO negative the wrong-sign head cannot be bypassed.
- **Old-task retention check:** Deliver each version once on its clock, including the head request when B is refused; trace worst A/C drift and Q's routine work.

#### 11. Normalize the payment by the recipient's live step rule (P)
- **Mechanism:** During preparation train response directions to realize bounded signed effects after the actual recipient optimizer across an allowed state family, allowing no runtime tail-dependent optimizer changes.
- **Novelty vs nearest prior art:** Preconditioned gradient projection is established. The candidate is a transferable signed-effect contract over optimizer states for a fixed ordinary response, including direction reversals due to momentum.
- **Cheapest first test:** Repeat a C correction with two legal momentum states and unequal diagonal scaling; compare raw alignment, projected updates and an exact effect search under the same optimizer and parameter budget.
- **Old-task retention check:** Run the actual response and two follow-up A/C and receiver updates under both states; log wrong signs before any compensating action.

#### 12. Make the response pay the worst reader without overpaying its neighbour (P)
- **Mechanism:** Train a response whose signed effect reaches a designated endangered reader while leaving another reader's live margin intact; validate the whole effect vector, not just its favorable coordinate.
- **Novelty vs nearest prior art:** GEM and whole-trace matching already enforce multiple constraints. The candidate reusable object is a *directed* payment with certified collateral limits induced by ordinary transferred service.
- **Cheapest first test:** Use three readers with conflicting band edges and compare projection, an equal-width spare adapter, and trained sparse reader effects; include collinear readers with no feasible nonzero selective payment.
- **Old-task retention check:** Check all three prefixes plus held-out A/C and receiver service, including refusal in the collinear case.

#### 13. Let the first payment change what can safely be paid next (P)
- **Mechanism:** Train a C response whose normal update opens a reader-neutral region from which P's later ordinary update can pay the complement; do not credit an independently simulated P update.
- **Novelty vs nearest prior art:** Adaptive scheduling and ordinary activation shifts are known. The candidate is a payment edge whose realized first effect also changes the legal successor effects, unlike static signed pairs.
- **Cheapest first test:** Enumerate orders in a two-unit ReLU host; compare independently predicted tails and exact joint search on separately and jointly trained hosts. Include a gate opened only after the B deadline.
- **Old-task retention check:** Replay A/C once per visible prefix, run P and Q's normal requests, and check rare C inputs that straddle the changed gate.

#### 14. Find when a required payment cannot fit any truthful correction (I)
- **Mechanism:** Compute the set of ordinary update effects consistent with the lawful C target, version and update rule; produce an obstruction when that set cannot intersect the pending signed band.
- **Novelty vs nearest prior art:** Feasibility certificates are old. This audit distinguishes a representational limit from poor scheduling or from an accidentally invalid C target.
- **Cheapest first test:** Compare an exact enumerator and a linear separation witness on T's opposite-target case and on two effects whose convex hull falsely suggests a legal action.
- **Old-task retention check:** Serve the due C correction in the safe no-B branch and execute A and receiver work; report the exact missing B result rather than calling refusal retention success.

#### 15. Make a paid response safe across a visible commit boundary (P)
- **Mechanism:** Specify when an ordinary response and its update take effect; make the update effect and consumption of the payment count exactly once across retries, without gaining a second physical write slot.
- **Novelty vs nearest prior art:** Transactional outboxes and deduplication are standard. The candidate interface binds a reader/prefix payment to a versioned update's single visibility point; a normal transaction that meets the same deadlines ties.
- **Cheapest first test:** Enumerate a delivery acknowledgement lost before/after commit and both retries, with an intermediate reader. Compare atomic transaction, idempotent reply only, and retry with a separate payment log.
- **Old-task retention check:** Observe A/C before and after all distinct commits, check original C deadlines and verify no lost or duplicate old-task effect on replay.

#### 16. Replace a threatened payer only with compatible incoming work (P)
- **Mechanism:** When P's future slot is publicly revoked, admit another working payer only if its actual outstanding old request supplies the missing signed effect on time, without replacing Q's earlier valid payment or rebasing the debt.
- **Novelty vs nearest prior art:** #267 card 17 redirects an unspent contribution; contingent scheduling already moves slots. The candidate operation transfers only the unfulfilled reader obligation against independently owed normal work, under a held-out withdrawal.
- **Cheapest first test:** Revoke P's second slot after Q pays; cross a timely old request, a late one and one with wrong sign. Compare exact contingent scheduling and dedicated reserve with the same occupancy budget.
- **Old-task retention check:** Run both partners' ordinary workload and all A/C reads through revocation; hold original C and B deadlines fixed.

### Make the split and the payment earn their interaction

#### 17. Put the signed effect on the residual side of the cut (P)
- **Mechanism:** Train R so Q's ordinary residual update produces its required reader effect but does not write S, letting the standby finish B from the single shared source.
- **Novelty vs nearest prior art:** Shared/private learning plus nullspace projection is the direct stack; this action matters only if joint training exposes a reader-visible payment through R that the stack cannot meet without a shared write or separate slot.
- **Cheapest first test:** Train a two-plane linear model with a hard S freeze and one Q slot; compare learned splits with fixed masks plus exact planning and GEM. Ablate R-to-reader coupling while preserving C correctness.
- **Old-task retention check:** Execute versions v1/v2, Q's old work and prefix A/C at fixed B utility; check S remains unchanged through the actual joint suffix.

#### 18. Expose only the reader's allowed effect, not the shared write (P)
- **Mechanism:** Route a residual update to an old reader through a trained narrow readout, while B's finish cannot observe that change. Count the readout and its version state in the replica budget.
- **Novelty vs nearest prior art:** Adapter routing and sparse readouts are familiar. The candidate is a small cross-lane read interface whose allowed signed effects can be used as payments without reopening shared B writes.
- **Cheapest first test:** Hold out one C correction and replay it with and without the narrow readout. Compare a wider task adapter and a fixed linear interface using the same memory budget; include a B probe sensitive to the same readout.
- **Old-task retention check:** Score retained reader bands and new C responses at the cut, the recipient's routine tasks, and B utility with the sensitive probe.

#### 19. Find the least replica safe for service *and* payments (P)
- **Mechanism:** Learn a replica code that separates histories not only by possible correct C responses but also by the effects their lawful updates can make before each reader deadline.
- **Novelty vs nearest prior art:** Minimal sufficient state for output and tail matching can be stacked. The candidate equivalence preserves their *joint* feasible actions; separately matching two marginal sets can pair the wrong response and payment.
- **Cheapest first test:** Enumerate histories where the separately reachable C outcomes and signs coincide but their pairings are reversed. Compare a joint code, two independent codes at equal bytes, and exact coupled equivalence.
- **Old-task retention check:** Run both paired requests (including the one that must not be offered), verify old A/C and receiver work at each prefix, and record peak bits versus live B.

#### 20. Buy new redundancy with corrections already owed (P)
- **Mechanism:** Train the first real transferred corrections after cut one to refresh a small independently usable R for cut two while still supplying their original signed effects. Reserve nothing based on unobserved future arrivals.
- **Novelty vs nearest prior art:** #267 card 21 renews joint offers and ordinary incremental replication refreshes state. The proposed operation renews a replica with work already owed while it is also making previously committed payments.
- **Cheapest first test:** Run a two-cut CPU stream; compare incremental copy plus independently trained correction payments, joint training, and a late/no-arrival negative. Count copy writes and fallback slots.
- **Old-task retention check:** Complete A and all old/pinned C on both clocks with real prefixes, plus receiver's routine work; include missed C and B in the no-arrival denominator.

#### 21. Test whether precision can preserve both answers and signs (I)
- **Mechanism:** Allocate residual bits for both reply error and signed-effect error at the earliest required prefix, especially when quantization changes an ordinary gradient's sign.
- **Novelty vs nearest prior art:** Task-aware quantization is established; this is a cost improvement or a negative result if acceptable C answers do not imply safe payments.
- **Cheapest first test:** Sweep two-to-eight-bit copies in a scalar residual SGD task against reply-only calibration and float copies. Hold out small-margin corrections that cross zero after rounding.
- **Old-task retention check:** Score A and C near original decision margins, ordinary receiver performance, original queue completion and false payment acceptance.

#### 22. Measure whether the two ideas merely buy spare capacity (I)
- **Mechanism:** Cross split versus full state with dual-purpose versus separate updates. In each arm trace which bytes survive and which ordinary action occupies each slot, with disjoint capacity as a tie control.
- **Novelty vs nearest prior art:** #267 card 22 audits the scheduling interaction; adding a state cut tests whether a reported interaction merely spends more memory or moves validation out of the budget. No mechanism claim if the stack ties.
- **Cheapest first test:** Cross R and T on four hosts, give the strongest stack exact scheduling, and compare on one binding shared slot and one nonbinding slot. Give both the unseen shared-source failure and wrong-sign correction.
- **Old-task retention check:** Report per-version service, all prefix bands, routine receiver work and held-out A/C after the tail, with matched B or explicit B refusals.

## Ranked deeper questions

1. **Can a split residual serve pinned C and pay a genuinely necessary installment while S stays shared and unwritten?** Start with 09, 17 and 22. Use an early slot already owed to C and two independently necessary effects. Compare the equal-budget stack of selective replication, version-aware scheduling, LoDA-style separation and constrained updates with exact search. Drop the interaction claim if that stack ties.
2. **What is the smallest replica across real cuts, versions and next updates?** Start with 01, 02, 05 and 19. Enumerate histories that agree on current C but disagree on a pinned response, an optimizer transition, or the sign a lawful response can deliver. Use exact equivalence as a tiny-domain reference and report the fault sets where the shared dependency makes independence impossible.
3. **Which signed offers remain valid under adaptive execution and observation order?** Start with 11–15. Execute the actual joint suffix with a held-out momentum state, retry and wrong-sign target. Ask whether a public offer is cheaper to verify than contingent search at matched A/C retention; restrict the claim to a simpler host if it fails.
4. **Can ordinary work renew the reserve without making the next call-up unsafe?** Start with 07, 16 and 20. Run two retirements with late or absent corrections, correlated loss and unchanged ordinary deadlines. If the reserve needs new capacity or unrecoverable state, report the single-window frontier instead.

[parent]: https://github.com/manojbajaj95/cl/pull/267
[triage]: https://github.com/manojbajaj95/cl/blob/d060aace22c59ef1bc73c729d1144fc602e2013f/reviews/flood-triage.md#L383
[ledger]: https://github.com/manojbajaj95/cl/blob/d060aace22c59ef1bc73c729d1144fc602e2013f/reviews/idea-ledger.md
[working]: https://github.com/manojbajaj95/cl/pull/256
[acl]: https://www.alphaxiv.org/abs/2003.09553
[loda]: https://www.alphaxiv.org/abs/2603.00191
[gem]: https://huggingface.co/papers/1706.08840
[pcgrad]: https://huggingface.co/papers/2001.06782
[hot]: https://www.postgresql.org/docs/current/hot-standby.html
[snapshot]: https://docs.aws.amazon.com/ebs/latest/userguide/how_snapshots_work.html
