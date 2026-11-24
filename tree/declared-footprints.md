# Declared write footprints: spend only the state every reader has released

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Make-before-break writes](make-before-break.md) ([PR #157](https://github.com/manojbajaj95/cl/pull/157)), cards 3 and 13. **Review seed:** [Flood triage row 252](https://github.com/manojbajaj95/cl/blob/9c5f45c8a43d6c8290c5745426a27fe1f37d6d45/reviews/flood-triage.md#L252), two score-3 ideas: veto training outside a checked construction footprint, and hand over certified slices under a fixed overlap cap, releasing shared state only when their receipts cover every reader.

## What would be new?

**Is a declared footprint a new object for continual learning?** A list of state a program may change is not new: effect systems and transactional read/write sets already do this, and CL masks grant narrower write rights over weights. Nor is draining readers before freeing storage new. The **candidate CL object** is a *trainable footprint contract*: a builder offers several ways to learn the same replacement with different allowed effects. As slices actually earn independent live service, their receipts expand which construction steps a later builder can legally take. The contract changes which replacements can be learned under a fixed memory and service budget, not just which endpoint can be installed. This is a conditional claim. If ordinary effect-checked staging plus exact dependency retirement and incremental verification gives the same later-task progress, reusable capacity and cost, call it a useful CL interface, not a new primitive.

- **Declare and check before construction.** Name logical objects, versions and physical storage regions, including aliases; declare every permitted mutation of weights, gradients/accumulators, running means/variances/counters, optimizer slots and step counters, decoupled weight decay's target weights, LR schedule state, EMA/teacher copies, RNG streams, routing/calibration and mutable caches if present. Include allocation/deletion and outward side effects if they affect observable service or future learner state. Declare read dependencies separately (including which state the proof and training read). Scratch writes also need rights; unknown hooks, fused kernels or asynchronous writes are denied unless confined to a declared region with a trustworthy bound.
- **Veto a whole step, not just a final delta.** The declaration must be authorized against live obligations, not merely self-asserted. The *attempted* write set for each step (forward through callbacks and publication) must be contained in it. Check ahead of execution or stage the entire step in confined state and refuse publication if an attempted effect falls outside. A write then undo, a value-equal write, or a leaked async callback is not evidence of noninterference. Check proof premises again at commit. A footprint does not certify old behavior by itself: it constrains what can change; disjointness from protected reads or a separate behavior check establishes safety within its stated model.
- **Release by reader coverage, not traffic.** For group `g`, keep a conservative ledger of every admitted reader obligation: task/slice, route version, fallback, in-flight continuation and live proof or training consumer that needs `g`. A receipt discharges only the indicated obligation and domain, on the stated versions, after independently checking timely service without `g` and switching admissions. Multiple receipts can cover one obligation by union, but overlaps count once and unknowns remain blockers. Free/reassign `g` only when all obligations are covered, old readers have drained or migrated, and new readers cannot attach to the retiring version. Use the parent's distinction between serving now, serving after verified fixed-weight rerouting and training-only recovery; the last is never a receipt. A finite panel is not proof of full coverage.

**Paper case.** Old A has a common slice reading private cell `x` and shared cell `g`; old C has a rare slice reading `y` and `g`. Each needs one replacement cell that can serve without any of those old cells; there is one free cell. Build A's replacement there. Reject a step that also tries to update `g`'s running mean even if its weight delta is legal. After checking and switching A and draining its old requests, reclaim `x` for C's replacement. A's receipt does not release `g`, even if A is 99% of traffic. Switch C and drain its last old request before offering `g` to B; a still-installed fallback reading `g` blocks release until it too moves or is safely removed. A global build-before-switch requiring both replacements at once exceeds this cap. Exact dependency retirement plus effect-checked staging can reproduce the sequence; the toy checks the rules, not novelty or whether such replacements are generally learnable.

## Prior-art screen and common CPU controls

- **CL write restrictions:** [PackNet](https://arxiv.org/abs/1711.05769), [HAT](https://arxiv.org/abs/1801.01423) and [Piggyback](https://arxiv.org/abs/1801.06519) allocate, gate or mask weights. [GPM](https://arxiv.org/abs/2103.09762) constrains gradient directions; [Sparse Memory Finetuning](https://arxiv.org/abs/2510.15103) concentrates updates in selected memory parameters; [Progressive Nets](https://arxiv.org/abs/1606.04671) isolate prior columns. Sparse or frozen weights are not evidence that an entire training step has no other effects. [Normalization recency bias](https://arxiv.org/abs/2310.08855) and [Momentum Fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) already identify the two salient non-weight channels. Treat local normalization, frozen statistics, and local/reset optimizer state as real baselines, not new objects.
- **Effects and reclamation:** [Polymorphic effect systems](https://dl.acm.org/doi/10.1145/73560.73564), [sequential effects](https://arxiv.org/abs/1808.02010) and [transactional memory](https://arxiv.org/abs/1502.04908) already express or enforce effects. [MPLS make-before-break](https://www.rfc-editor.org/rfc/rfc3209.html#section-4.6.4), [consistent network updates](https://www.cs.cornell.edu/~jnfoster/papers/frenetic-consistent-updates.pdf), [blue-green deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html) and [RCU grace periods](https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html) are strong controls for versioning and retirement. [Certified CL](https://arxiv.org/abs/2407.06697), [finite safe regions (PR #152)](https://github.com/manojbajaj95/cl/pull/152) and [mergeable writes (PR #156)](https://github.com/manojbajaj95/cl/pull/156) already motivate behavior checks, safe sequences and reusable prerequisites. This web/HF screen is provisional, not novelty clearance.
- **Ledger exclusions:** The [idea ledger](https://github.com/manojbajaj95/cl/blob/d05bd0c3b51284ff09ebd77519050d1b73104e88/reviews/idea-ledger.md) killed return-point adapters as save/restore and sparse-write certificates based on structural rank. Do not count restoration as learning or infer functional independence from sparsity. Per the ledger's merge rule, give the strongest stacked control the same effect checker, reader map and opportunities to optimize.
- **Shared protocol:** Start with exhaustive tiny circuits, rational linear updates or a CPU split-digits MLP with bounded scratch. A and C are ordinary held-out old tasks, measured against their acquisition references on data not used for training, route selection or certification. Log them before B, at every visible prefix (including rejected steps and requests spanning a switch), and after capacity reuse without recovery training. Also check rare slices and deadlines separately; neither substitutes for normal A/C. Compare at matched held-out B, or report no feasible match. Charge peak bytes (including scratch, slots, caches, proof metadata and copies), old queries, checks, stalls, aborts and latency. Use frozen expansion, projected replay, direct repair, global swap and traffic canary as applicable; the strongest control combines whole-step effect-checked staging, versioned per-slice switching, exact reader accounting and incremental checks. Score time/bytes to *actual later reuse*, worst-prefix A/C and false-safe accepts/releases; a single false-safe in an exact test invalidates the guarantee in that model. P means conditional primitive candidate, I means improvement or audit.

## Idea cards

### Declare the builder's effects before measuring its quality

#### 1. Phase-specific build offers (P)
- **Mechanism:** A builder offers alternative phase programs, each with its own declared reads, writes and scratch ceiling. Choose among them as reader receipts arrive; a frozen-trunk warm-up may proceed now even if calibration is not yet authorized.
- **Novelty vs nearest prior art:** Sequential effects and PR #156 already admit ordered alternatives. The candidate interface trades *learnable replacement quality* against effect rights that can be earned partway through a build.
- **Cheapest first test:** Enumerate freeze-then-calibrate and local-stat programs in a two-layer CPU model. Compare a whole-build union, exact effect-checked staging and a generic phase scheduler with the same programs.
- **Old-task retention check:** Score A/C after warm-up, rejected early calibration and legal calibration after receipt; check ordinary inputs on both sides of the switch.

#### 2. Optimizer slot footprint with delayed reads (I)
- **Mechanism:** Pin optimizer state by parameter region and include moments, step clocks, and weight-decay targets in each step's write closure, even where the gradient is zero.
- **Novelty vs nearest prior art:** PR #136 studies history in slots; this is a containment audit, not a slot-memory claim.
- **Cheapest first test:** Plant a nonzero moment and a zero gradient on a protected coordinate in a tiny AdamW loop. Compare gradient masking, per-region optimizers, and whole-step checking.
- **Old-task retention check:** Score A/C immediately and after the next permitted update that would express an overwritten slot; a forward match alone does not pass.

#### 3. Split normalization into shareable and private effects (I)
- **Mechanism:** Offer read-only shared affine parameters with private running means, variances and counters until the incumbent's last consumer releases its bank.
- **Novelty vs nearest prior art:** Normalization recency work already uses adapted statistics. The audit asks whether a footprint veto catches incidental buffer writes better than freezing weights alone, with frozen stats and separate banks as controls.
- **Cheapest first test:** Shift means in a two-feature CPU classifier and plant a train-mode forward into the shared bank; measure missed effects and bytes.
- **Old-task retention check:** Score A/C under normal inference at each construction prefix, and on the first cold evaluation after either candidate activation or abort.

#### 4. Declare coupled clocks and teachers (I)
- **Mechanism:** Treat LR counters, warmup position, EMA teacher and training callbacks as separate writer regions; permit a local clock or a separately authorized synchronization transition.
- **Novelty vs nearest prior art:** Effect systems already express these writes and PR #136 includes schedules in learner state. The test asks which shared control states matter at matched B, not whether hidden state exists.
- **Cheapest first test:** Interleave two scalar learners and plant a scheduler tick and teacher EMA on an otherwise legal B step. Compare independent clocks/teachers with effect-checked shared staging.
- **Old-task retention check:** Check A/C on deployed and, where contractually served, EMA outputs, then after an ordinary legal training continuation.

#### 5. Physical alias closure (I)
- **Mechanism:** Resolve parameter views, tied embeddings and fused updates to versioned physical regions before admitting a logical write; deny unknown aliases instead of inferring disjointness from names.
- **Novelty vs nearest prior art:** Region and alias analysis already supplies the rule. This audits the gap between a CL parameter mask and actual storage.
- **Cheapest first test:** Tie two heads through a strided view and compare name-level guards, canonical region guards and independent copies at equal memory.
- **Old-task retention check:** Score normal A/C through the attempted aliased mutation and a legal disjoint control; check intermediate state rather than final hashes only.

#### 6. Contain speculative probes and aborts (I)
- **Mechanism:** Give route discovery a private effect budget for mutable caches, RNG and buffers; forbid publishing state from a probe that fails, including work scheduled after abort.
- **Novelty vs nearest prior art:** Transactional isolation already stipulates this; the CL audit is whether ostensibly evaluation-only route discovery changes later learning or live service.
- **Cheapest first test:** Plant an RNG draw and a deferred cache write in a candidate evaluation. Compare evaluation mode, process isolation and scoped staging with the same queries.
- **Old-task retention check:** Interleave A/C with aborted probes and the next legal update; check both deadlines and ordinary old accuracy.

#### 7. Write-granularity search under a checking budget (P)
- **Mechanism:** Train a builder to choose between coarse and fine effect regions by predicted B progress per byte and checker call, using only independently verified permissions.
- **Novelty vs nearest prior art:** Sparse Memory Finetuning chooses where to learn; the candidate choice also changes proof cost and cross-task admission at fixed peak bytes.
- **Cheapest first test:** Give a tiny MLP cell-, row- and bank-level alternatives. Compare the learned chooser with static masks, greedy query allocation and an exact small-instance oracle.
- **Old-task retention check:** Score A/C after every chosen build and on unseen tasks sharing the same regions; any admission outside the independent guard counts separately.

### Move slices without confusing coverage with popularity

#### 8. Reader-indexed union receipts (P)
- **Mechanism:** Store a released-reader receipt per domain and group, keyed to route and topology versions; compute release by covering each consuming obligation rather than counting switches.
- **Novelty vs nearest prior art:** This develops parent card 13; network versioning and RCU cover retirement. The CL candidate is reuse of behavioral coverage evidence by a later learner asking for a particular scratch group.
- **Cheapest first test:** Enumerate overlapping slice receipts, one rare fallback and one held request; compare traffic canary, exact reader accounting plus fresh checks, and receipt reuse.
- **Old-task retention check:** Exhaust A/C including uncovered overlaps, forced failover and the first request after B overwrites a released group.

#### 9. Learn the first slice that can fund the second (P)
- **Mechanism:** Choose the next slice and its builder jointly by which group that move would release and which otherwise-infeasible next build the reclaimed group enables.
- **Novelty vs nearest prior art:** Generic scheduling and canary deployment already order fixed replacements. The candidate operation makes a learned replacement's dependency set part of a schedule that opens a different training program.
- **Cheapest first test:** Extend the paper case with two candidate first slices of equal traffic but different releasable cells. Compare greedy traffic, greedy bytes and exact planning over the same route candidates/programs.
- **Old-task retention check:** Check A/C at every interleaving, including the rare slice left on the old route while the second build writes the reclaimed cell.

#### 10. Retire a group by splitting its last consumer (P)
- **Mechanism:** If an input region straddles two dependency patterns, split it using a deployable predicate and learn a replacement just for the part still reading the desired group.
- **Novelty vs nearest prior art:** Decision trees, routed experts and canaries already split traffic; the candidate refinement criterion is what training rights the split unlocks, not classification gain or load.
- **Cheapest first test:** Use a tiny rational classifier with two possible split predicates. Compare entropy splits, dependency-guided splits and a global repair using the same selector budget.
- **Old-task retention check:** Evaluate ordinary A/C, both sides of the boundary and any abstention when the selector is uncertain; retain the group whenever a permitted reader is unresolved.

#### 11. Pin sessions and remove fallback registrations (I)
- **Mechanism:** Seal admissions to a retiring version, pin each in-flight continuation, and remove or replace fallback registrations before counting the final discharge.
- **Novelty vs nearest prior art:** RCU and consistent network updates already give this pattern; the audit measures stateful CL service against request-only canaries.
- **Cheapest first test:** Interleave a slow recurrent request and a forced fallback with two stateless requests in an enumerated scheduler.
- **Old-task retention check:** Check old A/C continuation outputs and deadlines as well as clean requests after retirement, not just the immediate post-switch endpoint.

#### 12. Receipt repair when the router boundary moves (P)
- **Mechanism:** Recompute only the set difference between old and new consumer domains when a dispatcher update moves a boundary; revoke any affected admission or unspent write right until coverage is restored.
- **Novelty vs nearest prior art:** Incremental verification and PR #152 already invalidate affected premises. The candidate is a coverage delta reusable by builders for authorization, not just by the router's verifier.
- **Cheapest first test:** Shift a rational threshold in a three-slice router with two previously proven receipt intervals; compare full rechecks and incremental checks with the same dependency information.
- **Old-task retention check:** Score A/C on both sides and at the moved boundary. After irreversible retirement, reject a router change that reintroduces the old dependency rather than assuming the bytes can be restored.

#### 13. Shadow-poison independence check (I)
- **Mechanism:** During private validation, deny access to the retiring group and its cached descendants, including standby outputs, so a replacement cannot earn a receipt by borrowing them.
- **Novelty vs nearest prior art:** Parent card 2 already isolates shadow paths. This tests cached dependency false negatives under partial-slice switching rather than claiming an independent certificate primitive.
- **Cheapest first test:** Plant a cache hit in only one rare slice; compare warm shadow match, cold shadow and declared dependency isolation with identical queries.
- **Old-task retention check:** Run ordinary A/C before and after reuse and a forced miss on the rare slice; preserve the incumbent whenever isolated service fails.

#### 14. Count learner readers even after inference drains (P)
- **Mechanism:** Track future authorized consumers that still read a retiring optimizer bank or shared teacher. Relocate them, justify their removal from the declared operation family, or veto retirement after all inference slices move.
- **Novelty vs nearest prior art:** RCU tracks actual reads and PR #136 studies delayed expression. The candidate obligation explicitly connects future *permitted training* to a route receipt even when inference dependencies are empty.
- **Cheapest first test:** Move all inference slices in two function-matched learners with different pending optimizer/teacher reads. Compare inference-only accounting, full read/write sets and a declared continuation ledger.
- **Old-task retention check:** Check A/C immediately, then after the authorized continuation at matched B; restoration from a hidden backup gets no credit.

### Couple earned releases to later learning

#### 15. Bind late phases to exact receipt versions (P)
- **Mechanism:** Let a builder declare a late phase conditionally on named reader discharges. At commit consume a version-specific authorization; if the obligation map changed, recheck or choose another offered phase.
- **Novelty vs nearest prior art:** Database read validation and PR #156's prerequisites already prevent stale commits. The candidate prerequisite is quota for *learning* a replacement, minted by behavioral service progress rather than by finishing a fixed update.
- **Cheapest first test:** Race a later builder against a new fallback binding. Compare invalidation by version, exact transaction validation and staged alternative selection with identical effect and route maps.
- **Old-task retention check:** Check A/C after both possible orders, including a stale offer that must not start writing and the legal alternative that actually trains B.

#### 16. Choose a replacement that releases common state, not just private bytes (P)
- **Mechanism:** Present multiple replacement programs with the same old-service target but different residual dependencies. Select one by the additional future write rights unlocked when its receipt joins existing receipts.
- **Novelty vs nearest prior art:** Capacity-aware pruning and PR #155's disjunctive certificates already choose supports. The candidate objective values the complementarity of receipts and future builder effects, not just support size.
- **Cheapest first test:** Construct equal-size alternatives that each drop one reader edge, only one being the last edge to a useful group. Compare isolated size/accuracy, whole-graph greedy and exact joint selection.
- **Old-task retention check:** Score ordinary A/C and forced fallback before and after a later writer uses the chosen capacity; match actual B progress.

#### 17. Spend a temporary copy on the last blocker only (I)
- **Mechanism:** Copy a needed small state group to a bounded new region and move the final straggler's dependency there; validate it and retire the larger old allocation only after drain.
- **Novelty vs nearest prior art:** Copy-on-write and blue-green already provide the move. The CL question is whether selective relocation beats keeping the straggler's entire old route.
- **Cheapest first test:** Use a toy packed bank where one rare consumer needs one statistic from a larger indivisible allocation. Compare pinning, selective copies and relearning at equal peak bytes.
- **Old-task retention check:** Check A/C after relocation with cold caches and after overwrite of the old bank; charge the copied state and its future maintenance.

#### 18. Compile recurring release patterns across task orderings (P)
- **Mechanism:** Cache a parametrized mapping from effect/reader templates to valid handover orders, instantiate only after verifying concrete aliases, service domains and slot ownership.
- **Novelty vs nearest prior art:** Effect polymorphism and generic incremental scheduling already reuse templates. The candidate compiler pays for itself only if learned variants introduce recurring proofs of useful write rights that a fresh incremental plan checks more expensively.
- **Cheapest first test:** Permute a small task chain with planted alias exceptions. Compare template instantiation, dependency-indexed fresh scheduling and direct repair including all validation overhead.
- **Old-task retention check:** Track A/C and previously acquired B tasks through transfers and adversarial invalid instantiations, not just on the source ordering.

#### 19. Preserve budget for a declared next writer family (P)
- **Mechanism:** At handover select a receipt set that releases compatible groups for several possible next training footprints, reserving capacity without admitting an unknown writer.
- **Novelty vs nearest prior art:** Parent card 15 and PR #152 protect future editability. Here the tested object is the set of future *effect offers* made jointly feasible by reader coverage, compared to direct lookahead over actual training programs.
- **Cheapest first test:** Use two identical-output handovers and two possible future builders with different slot/stat needs. Compare immediate byte gain, direct lookahead and a verified footprint menu on held-out task order.
- **Old-task retention check:** Score A/C through each selected handover and each realized next writer. Count gains only when ordinary old tasks and deadlines still hold at matched new-task progress.

#### 20. Counterexample-guided footprint repair, never auto-expand (I)
- **Mechanism:** On a veto return the first blocked effect and its owning obligation. Replan with private state, freeze the effect, or reapply for rights; never silently widen the declaration.
- **Novelty vs nearest prior art:** Counterexample-guided verification already refines failed candidates. Test whether a veto precise enough to replan saves searches versus a generic abort and incremental checks.
- **Cheapest first test:** Plant one omitted BN update and one legitimate but blocked scheduler update in separate forks. Compare opaque rejection, precise veto and static whole-program confinement.
- **Old-task retention check:** Score A/C before and after each failure and repaired build; a trace with any exposed rejected effect fails even if final retention recovers.

#### 21. Find where coarse isolation is already optimal (I)
- **Mechanism:** Sweep the complete cost of exact bookkeeping versus frozen expansion or full staging as shared readers, conditional effects and scratch size vary.
- **Novelty vs nearest prior art:** This is a boundary audit against the full composed baseline, not a novelty claim about state ledgers or capacity receipts.
- **Cheapest first test:** Enumerate small dependency graphs, then compare an unmodified CPU MLP where no missing effect is planted. Sweep verifier cost and peak bytes; report ties and abstentions.
- **Old-task retention check:** Compare worst-prefix ordinary A/C and deadlines at matched B. Report if the footprint regime shrinks the set of viable B tasks without increasing safe reuse.

#### 22. Distinguish an unlearnable bridge from an unregistrable reader (I)
- **Mechanism:** Return separate failures for no affordable builder in an enumerated family, insufficient dependency evidence, and incomplete reader coverage; authorize nothing on any unknown.
- **Novelty vs nearest prior art:** Parent card 22 already asks for infeasibility witnesses. This audit separates route-learning failures from effect/coverage abstention rather than claiming impossibility for arbitrary learners.
- **Cheapest first test:** Plant a solvable two-slice case, one case with no viable replacement under the specified cap, and one open-world reader case. Compare a bounded exhaustive oracle with the registry's verdicts.
- **Old-task retention check:** Check normal A/C through refusals and successful reuse. In the open-world arm, include a rare actual reader that fails if a system equates missing evidence with vacancy.

## Ranked deeper questions

1. **Can earned reader coverage change what the next builder can learn, beyond effect-checked staging and exact retirement?** Give both the same programs, access to effect sets and dependency maps, old queries, peak bytes and deadlines. Look for more held-out B progress or less total checking at equal worst-prefix A/C, with gains persisting when a later writer actually uses the released state. If the combined baseline matches it, drop the primitive claim.
2. **What is the smallest sound boundary that a real training step can declare cheaply?** Sweep grain and trusted runtime boundaries across forward buffers, AdamW, slot clocks, EMA, async effects and aliases. Contrast policy rejection, detector accuracy and overdeclaration; benchmark both planted misses and ordinary code. If completeness requires a whole-state clone, say for which builders local footprints are unhelpful.
3. **How much of the consumer domain can be certified without a throughput proxy?** Include rare slices, fallbacks, boundary drift, in-flight computation and future authorized learner reads. Measure exact small-domain coverage, empirical gaps and conservative abstention separately. Determine whether cheap evidence buys enough real release to justify its cost.
4. **Does learning the order and shape of handovers outperform scheduling fixed routes?** Equalize route candidates and show a case where allocating scratch to one learned slice changes the affordable replacement program for the next, then test held-out task orderings. If an exact scheduler over ordinary effects and readers reproduces the result, keep the scheduler, not a new learning object.
