# Demand-shaped neutral structure

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Neutral unit groups](neutral-groups.md) ([PR #183](https://github.com/manojbajaj95/cl/pull/183)), cards 19 and 03. **Review seed:** [Flood triage row 289](https://github.com/manojbajaj95/cl/blob/b3c4afed4dfd9e0b0085ce4cfa10594f6f4df038/reviews/flood-triage.md#L289) scored two directions 3: past requests shape which live supports are cheap to convert at fixed width and protected function, and overlapping release witnesses let an editor route around a newly pinned unit by verifying an actual finite move.

**Can weights remember how to make room, without remembering the requests themselves?** [Neural teleportation](https://arxiv.org/abs/2012.01118) and [symmetry teleportation](https://arxiv.org/abs/2205.10637) change trainability without changing the represented function or a symmetry-invariant objective; [MAML](https://arxiv.org/abs/1703.03400) already adapts an initialization to a task distribution. [Net-Trim](https://arxiv.org/abs/1611.05162), [Neuron Merging](https://arxiv.org/abs/2010.13160), and [architecture-preserving provable repair (APRNN)](https://arxiv.org/abs/2304.03496) already provide the compaction or checked-repair ingredients. The candidate is narrower: **past demand changes the cost of particular, later useful release moves in a fixed-width live host**, and joint supports can keep those moves available after the host takes on obligations. A blind editor must be able to spend the difference, not just decode a family label. The [idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md) closed Gramian and forecast-weighted reserve selection after retention matching left only 0.09 absolute MSE points of next-task spread ([PR #21](https://github.com/manojbajaj95/cl/pull/21)); this node does not propose another reserve score. Nor does it treat an insertion-point match as protection for a downstream reader (the read-pinning ABI kill).

## Contract and two paper witnesses

Let `P` include ordinary old inputs, rare slices, and the scopes of all live writes. A preparation or reroute must preserve the protected function pointwise on `P`, at the same width; a useful edit must beat no-write on a frozen target and keep every acquisition-anchored old floor. Include its scope in the next renewal. In a residual ReLU block, check old and new affine pieces on their common activation-cell refinement, at a cut covering every affected reader. Finite replay is an additional task check, not a proof. A pin prohibits the declared changes to a unit or reader binding while its obligation lasts. Publish atomically or prove each observable intermediate; stage costs count.

Freeze families, disjoint historical and held-out instances, the addressing interface, legal moves, utility targets, old floors, and budgets before shaping. “Blind” means a separately fixed editor sees the current request, current host, and declared contract, not past requests, preparer's slot labels, or the held-out generator. If it gets a portable certificate or index, charge it and also test host-only access. Measure admitted useful edits, net slots **subsequently used**, and end-to-end cost (history access, preparation, metadata, optimizer state, scratch, verification, failed checks, and search); report per-family and rare-slice failures. Show the cost–admission frontier, not only an advantage at a chosen timeout.

Cross hosts (correct-history, family-swapped, shuffled, and demand-blind exact recompilation) with editors (one fixed blind editor and an independent implementation, including the generic comparator). Match starting tasks, full protected outputs, width, individually disposable slots, and, where possible, held-out pre-edit predictions. The strongest stack is exact compaction or joint repair **plus** recycling, the same legal moves and verifier, matched teleportation/meta-training, and a same-budget external hint/repair cache that can use the same history. Also give exact repair the shaped host; an exhaustive same-state, same-move solver is a ceiling, not a competitor the method can beat in feasibility. Randomized and nuisance-matched shams should preserve the coarsest statistics being held constant, including available gates and parameter precision. In the pin study, replay the same pin trace across arms rather than letting a planner avoid difficult pins.

**Demand witness — a family swap at exactly matched predictions.** On top of any unchanged predictor, take two live signed units with contributions `[s x+2]₊` and `−[s x+2]₊`, with `s ∈ {−1,+1}` and `P=[−1,1]`. Both act on `P`; neither can be removed alone. The sum is zero everywhere for either sign. Past left/right requests choose `s`, but the editor need not see that history: its shared conversion sets both biases to `−2` atomically (the sum is still globally zero), then makes a bias-only useful edit when requested. For a held-out scale `r ∈ (1,2]`, a request in direction `s` asks for a positive residual at `sr` and zero at `−sr` and on `P`. Raising the positive unit's bias from `−2` to `−1` gives `r−1` at `sr` and zero at the protected points. For the opposite-shaped host no positive residual of the required form is possible by bias-only changes, even to both units: a positive difference of two equal-slope hinges is nondecreasing along that host's direction, so it cannot be positive at the low end and vanish at the high end. Reorienting the pair atomically defeats this separation if it fits the edit budget. This is a witness for what a **fixed action restriction** can expose, not evidence against meta-learning, an adaptive hint cache, or a good full-action compiler.

**Pin witness — a relation is not yet a release.** In a separate host use three live units with common activation `φ=[x+2]₊` and output coefficients `(1,−1,−1)`. Either group `{1,2}` or `{1,3}` can be deleted while preserving the original additive output. Give a later request utility in a second head by binding it to unit 1 (e.g. make that head return `φ(2)=4` at `x=2`), with an ongoing address contract that now pins unit 1. Subtracting the two old binary relations gives the signed relation `(0,1,−1)`, **not** a deletable subset. Change the first-head coefficients to `(1,0,−2)` atomically, without touching the second-head binding. This actually frees slot 2 and leaves both heads unchanged everywhere. Install a unit `[x−3]₊` in slot 2 for a subsequent useful first-head write at `x=4`, preserving the old task on `P` and both outputs at `x=2`. Hard negative: constrain all remaining first-head coefficients to magnitude at most 1 and allow only readout changes in the reroute. With unit 1 fixed, deleting either unpinned unit would need the other coefficient to reach `−2`; the relation still exists, but the proposed release must be refused. This is an instance of exact merging, not a speedup result. A speedup needs an advantage from reusing overlapping witnesses over re-enumeration with memoization and generic exact repair.

## Idea cards

### Compile demand into live supports

#### 01. Teach the host the move, not the answer
- **Mechanism:** Train over pairs of old requests with the same legal conversion but different useful targets. Reward short *verified* service paths under the fixed blind editor; publish only exact, fixed-width rewrites. Targets are not fixtures of the published host.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [MAML](https://arxiv.org/abs/1703.03400) learns a fast-adapting initialization; here the hypothesized transferable object is a reusable group rewrite at fixed pre-edit predictions, not an easier gradient step.
- **Cheapest first test:** Enumerate exact representations of a tiny signed ReLU block and cross two training families with disjoint held-out requests. Compare the whole finite action frontier with matched MAML-style optimization and a cache of compiled moves.
- **Old-task retention check:** Certify every prepared host on the old interval plus an off-interval rare slice; check both after each held-out write.

#### 02. Learn a movable conversion seam
- **Mechanism:** Put several signed hinges along the edge of a protected domain. Train their jointly compensating bias moves to expose a sliding new gate without rewriting distant hinges. The new request supplies the cut location.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [GradMax](https://arxiv.org/abs/2201.05125) provisions initially neutral units; a seam would cheaply convert already live hinges over a range of requests, not just offer a seeded dormant gate.
- **Cheapest first test:** Fit historic cuts at two locations, then query intermediate cuts. Match coefficient precision and edit coordinates against a uniform threshold grid and exact compaction plus adaptive gate placement.
- **Old-task retention check:** Compare old/new affine pieces on the full old interval and a rare cell adjacent to the seam, including the request just over the boundary that should fail.

#### 03. Pay for a shared carrier only once
- **Mechanism:** Reweight active units so different family-specific release supports borrow the same compensating carrier at different times. Teach the host the common compensation, not a separate idle pair for each family.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Neuron Merging](https://arxiv.org/abs/2010.13160) consolidates redundant contributions; these carriers are deliberately left live to furnish multiple, nonconcurrent ways to release other slots.
- **Cheapest first test:** Use three same-budget host designs for two families: shared carrier, disjoint support, and merged receiver plus generic reset. Test alternating demands including an order where the first spend destroys the shared route.
- **Old-task retention check:** Verify the carrier's contributions and both installed targets after each spend; refusing the second request is a capacity failure, not forgetting.

#### 04. Make family costs identifiable apart from slot order
- **Mechanism:** Learn useful relative shape/sign patterns inside small groups and locate them by canonical activation fingerprints. Do not give the editor a preferred slot ordering.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) uses permutation alignment; canonicalizing for later move discovery changes the use of alignment, not its underlying operation.
- **Cheapest first test:** Cross unit permutations, legal positive rescalings, and demand history. Compare canonicalized moves with a permutation-equivariant exact solver and its byte-matched index.
- **Old-task retention check:** Certify each reorder and reweight, remap every reader explicitly, and re-evaluate old tasks and the first post-reorder write.

#### 05. Leave just enough slack to quantize a move
- **Mechanism:** Shape live supports so their legal conversion displacements land on the actual deployment lattice, with exact compensating contributions; float-only near-neutral directions are not options.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Net-Trim](https://arxiv.org/abs/1611.05162) targets sparsity under layer constraints; this is demand-aware integer feasibility rather than new sparsification.
- **Cheapest first test:** Exhaust an integer four-unit block at two precisions and compare shaped moves with quantization-aware exact repair and rounded floating candidates.
- **Old-task retention check:** Verify equality in deployed arithmetic, including boundary and saturation cases, and check each old task after a lattice-valid write.

#### 06. Prepare a move for the conjunction, not two marginals
- **Mechanism:** Shape one joint release for a pair of gates when historical demand couples two edits that share a verifier frontier. Train on some pairings while withholding the queried combination.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Smart “Predict, then Optimize”](https://arxiv.org/abs/1710.08005) optimizes a downstream decision loss. The claim must be a nonadditive, function-neutral intervention, not a better predictor of which bundle will be requested.
- **Cheapest first test:** Match family marginals but reverse co-occurrence in two history streams. Compare held-out bundled service with two independently tuned releases, their best joint repair, and a co-occurrence cache.
- **Old-task retention check:** Prove retention during the common release, then check the preexisting tasks and the two new targets after both legal installation orders.

#### 07. Attach a refund to the preparation choice
- **Mechanism:** Prefer a same-cost conversion that leaves the spent gate with a compatible live receiver, so the next renewal can fold it into that receiver without taking back the write. Learn which receiver shapes matter from historical two-step demand.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Neuron Merging](https://arxiv.org/abs/2010.13160) already provides the fold. The bet is on selecting the first route for the later refund, beyond the parent's one-fold witness.
- **Cheapest first test:** Start from two exact gate deployments with equal immediate utility; compare future admission on crossed streams with compressibility-aware preparation plus exact merging and equal lookahead.
- **Old-task retention check:** Certify that the installed gate's acquired task and all earlier tasks survive the fold and a later spend of the freed slot.

#### 08. Train for the demand that makes cheap release compete
- **Mechanism:** Pair competing historic requests that consume the same support and prepare an independent fallback only for the second demand that would otherwise fail. Reserve allocation depends on sequence conflicts, not next-task gain.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [PackNet](https://arxiv.org/abs/1711.05769) allocates freed parameters across tasks; the proposed allocation is of mutually excluding future release paths over currently live units.
- **Cheapest first test:** Compare two histories with identical request counts but clustered versus alternating bursts. Test held-out bursts under exact planning, static family quotas, and matched recycling plus cache.
- **Old-task retention check:** Maintain every installed burst target and rare old slice after the adversarial order, including the first refused request.

#### 09. Shape around a rare slice without exposing it to the editor
- **Mechanism:** During preparation align common-family compensation away from restrictive rare activation cells; the blind editor sees the protected contract/verifier, not rare training examples. Its rewrite has a simple exact proof rather than a rare-replay penalty.
- **Novelty vs nearest prior art — IMPROVEMENT:** [GPM](https://arxiv.org/abs/2103.09762) protects past activation directions. This optimizes finite cell-valid conversion under that constraint, not a new protection primitive.
- **Cheapest first test:** Add one small rare interval that defeats the cheapest common-case rewrite; compare exact constrained preparation with projected updates plus a generic exact checker and repair.
- **Old-task retention check:** Require proof on the rare interval and unchanged ordinary-task error; make an adversarial boundary request that must be refused if neither is provable.

#### 10. Give the editor a cheap discriminating observation
- **Mechanism:** Co-locate supports that expose the same cheap, deterministic local predicate for whether a requested rewrite is possible, without installing a lookup table. A positive predicate only orders search; it never authorizes publication.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Knowledge Neurons](https://arxiv.org/abs/2104.08696) localizes knowledge-related activations. This would localize a reusable witness of a legal *change*, not the answer stored in a unit.
- **Cheapest first test:** Hold out target values and compare a one-query editor with equal-cost host inspection, a learned proposal model, and an external predicate cache. Force false positives to pay the full failed verification cost.
- **Old-task retention check:** Independently verify the entire old domain, including an unqueried rare cell on which the cheap predicate alone is unsound.

#### 11. Spend old evidence to make the move check local
- **Mechanism:** Tune exact neutral supports to be aligned with the stable cell partition of a protected cut, so a later conversion changes fewer local proof obligations, without narrowing protection or reducing actual edit utility.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) already checks architecture-preserving repairs; this is proof-cost-aware preparation, not a weaker substitute for verification.
- **Cheapest first test:** Hold the set of feasible edits constant on two small piecewise-linear hosts. Compare end-to-end check cost against exact repair with an incremental certificate cache.
- **Old-task retention check:** Recompute a full independent proof after each write to catch missing cells, then compare ordinary and rare old-task metrics.

#### 12. Make neutral structure forget an obsolete request family
- **Mechanism:** When historical demand shifts, erase one family's cheap routes by exact recompilation and reassign their carriers to the new family; keep the already installed tasks, not the same future menu.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Continual backprop](https://arxiv.org/abs/2306.13812) replaces units to preserve plasticity. Here the reclaimable object is a family-specific unspent route through live units, not an inactive feature.
- **Cheapest first test:** Stage two historical regimes with a return to the first; charge re-preparation and missed returns against recurrence-aware caches plus exact recycling.
- **Old-task retention check:** Old-family *installed* tasks must survive erasure and a new-family write, even if the old-family admission rate for new requests drops.

### Make overlap survive obligations

#### 13. Keep the shared coefficient symbolic until it is pinned
- **Mechanism:** Store two rational overlapping relations and compile an elimination parameter that zeros the pinned coordinate; then solve for an actual bounded, pin-disjoint endpoint with a slot removed.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Circuit elimination itself is algebra, and [Net-Trim](https://arxiv.org/abs/1611.05162) already seeks constrained sparse endpoints. The candidate is a retained executable witness that turns a *new* pin into less verified service work.
- **Cheapest first test:** Use the pin witness and its magnitude-bounded negative. Compare cancellation plus endpoint verification with memoized re-enumeration and warm-started exact repair on the identical host.
- **Old-task retention check:** Prove all protected cells, the new head's binding and the actual freed-slot spend; the negative must preserve the host unchanged.

#### 14. Build an overlap that survives either pin, not a larger union
- **Mechanism:** Shape a small network of live release relations with alternative receivers so either of two predeclared single-pin events leaves a legally removable slot. Neither a union of supports nor a multiplexed mask is a certificate.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Hidden ReLU symmetries](https://arxiv.org/abs/2306.06179) identify equivalent weights, not which transitions stay usable after a later forbidden coordinate. The proposed object is physically realizable pin coverage at fixed width.
- **Cheapest first test:** Exhaust legal supports on six units, match one-pin-free edit utility and degree counts, then replay both pins separately. Include disjoint reserves and robust exact planning with the same forecast.
- **Old-task retention check:** Test both counterfactual histories independently, checking the original tasks and the pinned new consumer in each.

#### 15. Route around a reader, not just a neuron index
- **Mechanism:** Allow edits to a shared unit only in a named unowned outgoing path, provided a proof shows the actual pinned consumer sees the same response. Eliminate the affected channel from competing moves instead of conservatively banning all incident coordinates.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Knowledge Transfer with Jacobian Matching](https://arxiv.org/abs/1803.00443) covers response matching; this is exact channel-scoped release authorization, not the ledger's failed insertion-point pin or a Jacobian-only retention claim.
- **Cheapest first test:** Add one consumer reading a skip path and one reading the ordinary cut; compare typed channel pins with conservative whole-unit pins and full exact multi-output repair.
- **Old-task retention check:** Check the two full reader responses on their own domains, including a downstream effect whose input activation alone is unchanged.

#### 16. Permit a reroute only if it can be published live
- **Mechanism:** Synthesize a short sequence of bounded, individually legal compensation moves when atomic replacement of the entire support is unavailable. Do not count an endpoint whose only proof crosses an observable violation.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) targets certified repaired endpoints; path legality adds a deployment constraint, not a new notion of repair.
- **Cheapest first test:** Exhaust two-coordinate publication schedules with a planted pinned reader and compare staged reuse with time-expanded exact search. Include an endpoint-feasible, path-infeasible pair.
- **Old-task retention check:** Verify all visible intermediate outputs at the pinned and ordinary readers and check old tasks after the final useful spend.

#### 17. Separate “another pin” from “an impossible schedule”
- **Mechanism:** If elimination keeps returning directions whose feasible steps are too small, retain a checkable infeasibility cut for a given set of pins and allowed moves. It may exclude a whole class of repeated attempts but never certify a release.
- **Novelty vs nearest prior art — IMPROVEMENT:** The convex constraints of [Net-Trim](https://arxiv.org/abs/1611.05162) already admit infeasibility certificates; the test is whether a certificate for one pin set still cuts search cost across subsequent pin changes.
- **Cheapest first test:** Compare a retained cut with incremental exact repair on a run of nearby bounded readout problems, including a pin removal that invalidates the cut.
- **Old-task retention check:** Keep the incumbent byte-for-byte on refusal and independently verify the first feasible renewal after the invalidating event.

#### 18. Use agreement between two scopes only where they overlap
- **Mechanism:** Compile candidate compensations for different protected domains and join them on common adjustable coordinates. A route remains available only if there is one shared finite move satisfying both certificates and the pin.
- **Novelty vs nearest prior art — IMPROVEMENT:** [GPM](https://arxiv.org/abs/2103.09762) combines past protective directions; scope composition here pays for checking a shared finite rewrite, rather than claiming that local proofs compose automatically.
- **Cheapest first test:** Give two affine-cell systems compatible local releases in one case and contradictory coefficient requirements in another. Compare incremental joins with the full stacked exact problem and its cached factorization.
- **Old-task retention check:** Verify both complete domains, including shared boundaries and the pinned reader; reject the case where separate repairs cannot be published together.

#### 19. Trade one degree of freedom for two kinds of future pin
- **Mechanism:** Prepare carriers against heterogeneous obligations: one existing write pins an input feature, another pins an output coefficient. Learn shape/readout combinations that leave a different remaining move for each kind of pin.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Net2Net](https://arxiv.org/abs/1511.05641) gives function-preserving transformations; this asks whether learning their fixed-width placement exposes qualitatively different finite routes under partial freezes.
- **Cheapest first test:** Use a rational ReLU block with fixed cells and enumerate each pin type, then both. Compare matched symmetry preparation and exact constrained repair, including a case where the joint pin kills all moves.
- **Old-task retention check:** Check both old outputs and each independently acquired reader contract; no rewrite may silently swap a pinned feature's address.

#### 20. Route by predicted contention, verify by actual contention
- **Mechanism:** Use historical co-pins to prioritize a sparse chain of overlapping witnesses. On a new pin, instantiate moves from the chain and verify consumption conflicts rather than counting every cached option as a separate slot.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Graph neural networks for combinatorial optimization](https://arxiv.org/abs/2102.09544) already learn search policies; this is only a CL-specific search improvement unless changing the host, not just the ordering, adds an executable route.
- **Cheapest first test:** Cross graph-aware host preparation with cache-only graph search on the same pin traces. Hold the number of cached witnesses fixed and test a pending-edit pair that contends for one slot.
- **Old-task retention check:** Verify serialized releases and both previously installed tasks; if the second move is invalidated by the first, it must replan or fail closed.

### Discriminate a resource from its substitutes

#### 21. Transplant a support without transplanting the requests
- **Mechanism:** Exchange predeclared function-equivalent, same-width sub-blocks from two histories into a common host and check whether their held-out service advantage follows the sub-block. Re-bind readers by the public contract only.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns parameter space to combine models; this is a causal transfer test for editability, not a new model-merging method.
- **Cheapest first test:** Do A↔B swaps and A↔A shams, erase private metadata, and compare with transplanting a same-byte external cache. Include a nuisance-matched swap preserving norms but destroying the candidate overlap.
- **Old-task retention check:** Reject any transplant that changes a protected reader or old-task output, then certify again after the first successful held-out spend.

#### 22. Erase overlap while keeping the first menu
- **Mechanism:** Construct exact shams with identical first-request admission and cost but different shared receiver relations, then replay pins that arrive only after the first write.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [Symmetry teleportation](https://arxiv.org/abs/2205.10637) changes attainable optimization speed at fixed function; this audit isolates the continuation benefit from a first-edit advantage.
- **Cheapest first test:** Enumerate small hosts to find a matched pair, perturbing only overlap where possible. Compare pin/no-pin deltas after the same first edit under one common editor.
- **Old-task retention check:** Prove old outputs and the first useful edit are identical before pin assignment, and track both after the second request; an unmatched pair is not evidence.

#### 23. Charge for neutral information at its recoverable precision
- **Mechanism:** Sweep allowed weight precision and certify equivalence after canonical recompilation; compare the edits still serviceable with the gain from that many explicit cache bits. Ignore information only recoverable from exact gauge-dependent digits.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [Hidden ReLU symmetries](https://arxiv.org/abs/2306.06179) show parameter redundancy; they do not make arbitrary coordinates a useful demand memory. This is accounting, not a storage theorem.
- **Cheapest first test:** Enumerate a small integer host and its equal-width legal recompilations; give the cache the same side information and show cost–admission curves across precisions.
- **Old-task retention check:** Include only exactly matched recompilations; verify each successful edit at the actual numeric precision and reevaluate every normal old task.

#### 24. Hold demand fixed and swap the useful-edit definition
- **Mechanism:** Keep the same history families and cost constraints but replace a held-out payload distribution with another that uses the same conversion primitives in a different order. Test transfer under a blind editor that does not share the preparer's search heuristic.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [MAML](https://arxiv.org/abs/1703.03400) is designed for task transfer; this audit asks if the learned object transfers across editor implementations and held-out payload compositions, not just across more examples of the same template.
- **Cheapest first test:** Freeze two small editors and two request banks, cross editor implementations and shape histories, and give generic exact repair and an explicit compiled cache both banks' public interface.
- **Old-task retention check:** Apply unchanged old-task and acquisition-anchored checks in all arms, including after a pin and under the swapped utility definition.

## Ranked deeper questions

1. **Does family history move the held-out verified cost–admission frontier, or just pre-pay search?** Begin with 01, 21, 23 and 24. The strongest result would be a correct-history × held-out-family interaction that follows the transplanted support and survives independent editors, precision changes, and a full-cost comparison to the meta-training/teleportation/repair/cache stack. No separation at matched retention and cost means no memory claim.
2. **Is there a reusable object between a signed relation and a releasable slot?** Use 13–16 and 22. Measure the incremental value of overlap after the same new pin; require a finite witness that actually releases a used slot, refuse the magnitude-bounded negative, and compare against exact re-enumeration with memoization. If the savings disappear on the same host with that comparator, this is ordinary solver reuse.
3. **Can the demand benefit survive its own successful writes?** Cross 03, 07, 08 and 19 on short streams where useful writes create persistent pins. Match first-menu cost, then ask whether renewal yields independently useful later admissions without sacrificing any acquired obligation, even under unfavorable order. If eligibility only drains, report a one-shot reserve.
4. **When does narrow protection give a false family effect?** Use 09, 11 and 18 with old rare slices and multiple downstream readers specified before preparation. Check whether the same family-swap effect survives exact scope, fixed verifier strength and post-write old-task checks; if wider valid scope closes the gap, do not attribute it to hidden demand memory.

**Verdict:** The paper examples separate a cheap action family from unchanged predictions, and signed overlap from an executable release. Neither establishes a new primitive. Keep the memory claim only if held-out blind editors get more verified service for the same total cost and retention than exact repair, matched preparation and a paid hint cache, and if overlap continues to earn its keep after useful writes pin the units it was meant to protect.
