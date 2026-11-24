# Finite safe regions for new-task writes

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Forgetting as unregistered dependence](unregistered-dependence.md), [PR #150](https://github.com/manojbajaj95/cl/pull/150), card 15. **Review seed:** [flood-triage row 242](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/flood-triage.md#L242), score 3: search finite joint writes that preserve every old decision, even when one feature crosses a boundary and another compensates.

## What region are we talking about?

Fix a deterministic ReLU model, all non-writer state, a bounded writer domain W in weight or adapter coordinates, and a map from those coordinates to the deployed parameters. For every old task i, record the declared input domain Dᵢ, its predictions cᵢ(x) at acquisition, and the fixed tie rule. In **absolute writer coordinates**, the safe set Sᵢ contains exactly the points in W where the deployed model predicts cᵢ(x) for **every** x in Dᵢ. The live region is the intersection of all Sᵢ. “Every” means every input of that declared domain, not every draw from an unknown distribution. A finite panel is a finite contract; a continuous domain needs a proof over the whole domain. Baseline errors can survive a perfect retention proof; track both agreement and old ground-truth performance.

A convenient sufficient contract is that every old winner beats every rival by at least a fixed positive margin ε small enough to include the acquisition model on the declared domain. This is deliberately stronger than decision preservation. Report the gap it excludes; if the baseline has ties or margins approaching zero, use the actual strict/non-strict comparisons induced by its tie rule instead of assuming a positive ε. Newly added classes must be checked as rivals too. Decision preservation is not logit equality, confidence retention, or exact function preservation. Numerical acceptance must match deployed arithmetic: start with rational toys and use validated rounding bounds or abstention where floating-point error can flip a comparison.

- **Affine in the writer, finite old panel:** With a bounded polytope W, a fixed readout of ReLUs whose preactivations are affine in the writer, or one affine-in-coordinate mutable layer with all other layers fixed, each joint activation pattern across the old inputs gives linear sign and margin inequalities. The exact set is a finite union of polyhedral pieces, possibly with open faces under the tie rule; a closed positive-margin contract gives a union of polytopes. There can be exponentially many patterns. A readout-only writer gives one polyhedral region: even without gates, decision slack can beat a logit-nullspace, so that gain alone is not evidence for a nonlinear primitive.
- **Compensation, on paper:** For one old input let the winning logit gap be ReLU(u) + ReLU(v) − 1 with W = [−2, 2]². The old winner is positive at (1.5, −1) and (−1, 1.5), but loses at their midpoint (0.25, 0.25). A path via (1.5, 1.5) preserves a gap of at least 0.5 throughout. Turning off the first feature is safe once the second carries the decision. With B minimizing squared distance to (−1, 1.5), the exact B optimum is safe and changes u, which the start's old-logit Jacobian nullspace forbids. The straight line to that optimum fails a path certificate, but its endpoint passes; some intermediate points leave and later reenter the safe set. For a disconnected control, ReLU(u) + ReLU(−u) − 1 yields two safe pieces separated by an unsafe interval.
- **General ReLU weights are not piecewise affine in their own parameters.** With two mutable layers, even a fixed gate can leave a term uv in the logit, yielding curved boundaries. With semialgebraic W, writer maps, and old input/label domains, the exact region is semialgebraic: enumerate signs, use polynomial inequalities, then eliminate the universal input quantifier in principle. That is a shape statement, not an efficient verifier. Even a single mutable layer can introduce writer–input products on continuous Dᵢ. A vertex check is enough for an affine margin on a certified input cell, not on arbitrary boxes that contain ReLU or baseline decision boundaries.
- **Three meanings of safe:** A verified **endpoint** suffices for an atomic publish from a shadow copy. A **safe path** is needed if intermediate states serve traffic. An **independently composable batch** needs all admitted combinations and prefixes (or a verified order), not just each endpoint from the same start. For gap 1 − u − v at (0, 0), both individual +0.6 writes pass; their combination fails even on disjoint coordinates. For fixed contracts, merge by intersection in common absolute coordinates, not by addition of deltas. Recenter by translating the whole intersection. If the writer changes, pull constraints back along the new map into deployed state; do not carry old activation assumptions across blindly. Anchoring every exact decision to acquisition prevents cumulative decision drift, but does not prevent erosion of margin or future update options.

## Closest work and the common CPU test

[GPM](https://arxiv.org/abs/2103.09762) and [Adam-NSCL](https://arxiv.org/abs/2103.07113) use old features to constrain writes; [OGD](https://arxiv.org/abs/1910.07104) and [DUET](https://arxiv.org/abs/2611.29269) use local sensitivities, with DUET constraining both the old and new task via Jacobians. [TRGP](https://arxiv.org/abs/2202.02931) selects related tasks for scaled weight reuse; its “trust region” is not an exact decision-feasible weight set. [SGP](https://arxiv.org/abs/2302.01386) already softens directional protection. [CABA](https://arxiv.org/abs/2610.40740) gates a candidate along an interpolation using held-out anchors, with off-anchor and sequential bounds under assumptions; a certified endpoint on that line is not a search over compensating alternatives.

Finite feasibility itself is **not** a new object. [Knoblauch et al.](https://arxiv.org/abs/2006.05188) already formalize CL via intersections of task-satisfying parameter sets and show hardness and memory requirements for general families. [InterContiNet](https://arxiv.org/abs/2206.07996) already trains a nested sequence of weight-space hyperrectangles, and [HINT](https://arxiv.org/abs/2405.15444) uses learned embedding intervals; [Certified Continual Learning](https://arxiv.org/abs/2407.06697) already carries verification certificates across retraining. [Provable Repair](https://arxiv.org/abs/2104.04413) and [APRNN](https://arxiv.org/abs/2304.03496) already optimize neural parameters under certified finite or regional specs (including multi-layer architecture-preserving repair in APRNN); preserving old decisions is one such spec. [SpecRepair](https://arxiv.org/abs/2106.01917) already searches with counterexamples. The possible new object is narrower: a **reusable decision contract for future writes** that supports merging independently useful proposals, changing writer coordinates, extracting usable safe updates, and explaining what would break, at a measured cost below re-solving the original obligations. Neither a set of inequalities nor a renamed incremental verifier earns that claim.

- **Start with an exact oracle.** Use the two-writer example and an exact sign-cell census, then a small enumerable ReLU toll model from the parent with old A (common and rare exceptions), old C (unrelated rules), and successive B tasks. Independently vary initial margins, gate changes, writer overlap, task count, redundancy, and support. Include affine-only, compensating, disconnected, dense-conflict and identical-input contradictory targets. Add continuous cells only after the oracle handles finite domains.
- **Compare with the strongest simple stack.** Match writer family, inputs/task cues, capacity and byte budget. Compare GPM/OGD, DUET, trust-region and multi-direction line search with the **same endpoint checker**, matched replay, an affine decision-margin solver, an interval/box arm, and incremental repair with accumulated old specs. Give baselines the same candidate generation opportunities and count their audit cost. Use the exact all-constraints solver as the paid oracle. Distinguish endpoint from path requirements for every arm.
- **Report frontiers, not update norms.** At matched attained B progress compare A/C retention and cost; at zero certified old flips compare B gains. Count storage for old inputs and proofs, solver/audit time, rejected candidates, commits and serving changes. Verify all declared old decisions after each visible prefix against acquisition; separately report independent old holdout accuracy, rare and near-tie flips, worst old task, margin/logit drift and unknown proofs. Run the parent's [replay break-even falsifier](unregistered-dependence.md#24-map-when-read-set-protection-becomes-no-cheaper-than-replay) before crediting any compression. A useful region that costs more than exact repair or replay at the same contract is not yet a useful CL primitive.

## Idea cards

### Shape and search

#### 01. Price the gate-crossing premium
- **Mechanism:** Optimize B over the exact cell union, then constrain it to the acquisition cell, to a same-checker ray, and to a logit-nullspace. Decompose the gain into decision slack, changing gates, and searching away from a ray.
- **Novelty vs nearest prior art — IMPROVEMENT:** [DUET](https://arxiv.org/abs/2611.29269) and [APRNN](https://arxiv.org/abs/2304.03496) already optimize protected writes; the contribution would be identifying which restriction actually costs B progress.
- **Cheapest first test:** Solve the two-coordinate toy and a no-gate affine twin at matched initial A margin; vary B's target angle and enumerate every cell.
- **Old-task retention check:** Enumerate all A and C inputs at each commit; report both endpoint and path violations for the ray, separately from logit drift.

#### 02. Keep a frontier of substitutable features
- **Mechanism:** Compile a few correlated safe facets describing how much fallback v is needed after spending u; use the facets directly as a write budget, not independent per-feature minima.
- **Novelty vs nearest prior art — IMPROVEMENT:** [HINT](https://arxiv.org/abs/2405.15444) maps embedding intervals to weights, so even a box need not be axis-aligned in deployed weights. Benchmark against learned-coordinate boxes as well as native boxes; the delta is exposing conditional substitution to the optimizer.
- **Cheapest first test:** Pack equal bytes of boxes, rotated boxes, and facets into the two-feature world; sweep target directions not used to choose the enclosure.
- **Old-task retention check:** Verify every allowed vertex/cell where that suffices, and exhaustively audit the rare fallback branch and C at each resulting commit.

#### 03. Plan a route without pinning activation patterns
- **Mechanism:** Build adjacency between certified cells via shared feasible boundaries; find a chain of polytopal segments for live writes, and separately allow atomic jumps where no path is needed.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Mode Connectivity](https://arxiv.org/abs/1802.10026) searches low-loss paths; the delta is a certificate for every old decision along the path rather than small average loss.
- **Cheapest first test:** Require paths in the compensating L-shaped toy and the disconnected control; compare same-cell search and a two-bend planner with the same segment verifier.
- **Old-task retention check:** Certify every segment including shared faces for all A/C inputs; check both endpoints of every atomic jump and never count an unsafe straight line as a safe path.

#### 04. Choose which factors to let move
- **Mechanism:** For bilinear multi-layer writers, branch only on products the old margins actually depend on; compare certified product envelopes with freezing one factor and with exact polynomial feasibility.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) already permits multiple layers. Ask whether targeting writer products recovers more correlated B moves than layerwise repair at equal verification cost.
- **Cheapest first test:** Give A gap uv − 1 in a fixed active chamber; add a second pair used only by B, and vary whether the factors must trade off to meet B.
- **Old-task retention check:** Check the exact products for every A/C input at every visible state; never promote a feasible relaxation to a deployed write without verification.

#### 05. Make the contract relative to the baseline decision boundary
- **Mechanism:** Overlay the baseline's input cells and tie rule with candidate obligations; compare label agreement to protecting a positive margin band that would exclude some valid boundary-preserving changes.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Provable Polytope Repair](https://arxiv.org/abs/2104.04413) already handles infinite input polytopes; the comparison is which relative-to-baseline partition retains exact decisions with the fewest pieces.
- **Cheapest first test:** Use two adjacent one-dimensional old domains separated by a zero-gap point; look for a write that steepens both sides without shifting the crossing.
- **Old-task retention check:** Prove agreement on the open sides and the tied point using the declared tie rule; track independent old accuracy if the reference boundary is itself wrong.

#### 06. Expand class vocabularies without shielding old winners by task ID
- **Mechanism:** When B introduces a class, extend every old winner's rival list. Search for shared logit changes that reserve space for B while keeping the new class below every old winner on the old support.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Experience Replay](https://arxiv.org/abs/1811.11682) already treats sequential tasks with a shared predictor. The delta is proving the new-class inequalities instead of hoping balanced replay controls the tail.
- **Cheapest first test:** Add a third logit to a two-feature classifier with one rare old input close to B; compare replay and exact accumulated-spec repair.
- **Old-task retention check:** Evaluate mixed, unlabeled A/B/C at inference; verify both old-vs-old and old-vs-new comparisons after every class addition.

### Composition and storage

#### 07. Merge concurrent writes by their combined effects
- **Mechanism:** Have each writer propose a set of substitutes, not one delta; intersect their reachable merge choices with the old contract and attach a certificate defining which subsets or commit order are allowed.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Unlike single-repair feasibility in [APRNN](https://arxiv.org/abs/2304.03496), this would return a mergeable write object with independently executable prefixes. It is just joint repair if a generic sequential feasibility solve supplies the same object at the same cost.
- **Cheapest first test:** Pair two disjoint +0.6 proposals against gap 1 − u − v and give each a redundant alternative; compare single-commit joint repair, serial rechecking, and subset enumeration.
- **Old-task retention check:** Exhaustively replay every advertised subset/order on A and C; reject any unadvertised merge before publication.

#### 08. Delete obligations only with an implication proof
- **Mechanism:** On adding B, retire an old inequality only if the retained constraints imply it on all admissible cells; attach a proof so its influence is retained without retaining its old example for search.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Certified Continual Learning](https://arxiv.org/abs/2407.06697) reuses property certificates. Constraint redundancy is classical; the question is whether exact cross-task implication pays after accounting for proof storage.
- **Cheapest first test:** Stream repeated, nested and almost-parallel facets; compare exact incremental redundancy with all-constraints repair and equal-byte replay.
- **Old-task retention check:** Independently verify all retired A/C obligations after each later commit, including a rare facet made nonredundant by an illicit dropped assumption.

#### 09. Share forbidden coalitions rather than slots
- **Mechanism:** Compile “not both fallbacks off” into a clause over certified writer predicates; share clauses across tasks and explicitly leave uncovered higher-order effects unproved.
- **Novelty vs nearest prior art — IMPROVEMENT:** Row 242's companion idea and [Reluplex](https://arxiv.org/abs/1702.01135) already motivate logical encodings. The proposed gain is reusable small coalitions with exact continuous predicate semantics, not the invention of clauses.
- **Cheapest first test:** Compare shared clauses, equal-byte union masks and full constraints on redundancy, parity, and a planted three-way failure.
- **Old-task retention check:** Enumerate every A/C coalition and predicate boundary; fail the method if a pairwise-only encoding accepts the planted triple.

#### 10. Transport a contract when the adapter changes
- **Mechanism:** Pull the contract back through a new writer map, transporting certificates only for relations actually proved by that map. Measure whether equivalent writers differ only in encoding and whether added directions require new proof.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Equivariant Architectures for Learning in Deep Weight Spaces](https://arxiv.org/abs/2301.12780) already models weight symmetries. A contract-transport operation would also have to support writer changes that are not global symmetries and safely identify the part that needs rechecking.
- **Cheapest first test:** Reparameterize a two-coordinate adapter by a rotation and a positive ReLU rescaling, then add one genuinely new direction; compare a fresh exact solve to transport plus reproof.
- **Old-task retention check:** Apply both writer maps before and after B and check A/C on every input, including cases reachable only via the new direction.

#### 11. Index cells by proofs, not by examples
- **Mechanism:** Cache affine maps, sign assumptions and active old facets by cell. When B inserts obligations, prove some cached cells unchanged, split others, and invalidate cache entries whose assumptions no longer hold.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Certified Continual Learning](https://arxiv.org/abs/2407.06697) already caches verification information. The target is reusing the representation of *alternative writes*, not certifying only the current weights.
- **Cheapest first test:** Stream small threshold tasks with low and high overlap; compare bytes and recheck time against warm-started incremental repair.
- **Old-task retention check:** Re-enumerate the oracle safe set after every insertion; check A and C at selected vertices and just inside/outside every changed face, including cache hits.

#### 12. Budget the cost of forgetting a proof, not a task
- **Mechanism:** Under a hard memory cap discard expensive search artifacts but keep a sound inner region; optionally restore discarded permissiveness from a priced audit source. Separate “known safe” from “not yet known safe.”
- **Novelty vs nearest prior art — IMPROVEMENT:** [HINT](https://arxiv.org/abs/2405.15444) already uses compact inner regions. Compare explicit proof eviction and recovery to always rebuilding a box or replaying an equal-byte subset.
- **Cheapest first test:** Evict one of two cell caches that alternate in relevance to B; compare eviction by reuse, by bytes, and a static interval.
- **Old-task retention check:** Verify A/C immediately after eviction and after recovery; score opportunity lost due to conservative shrinkage separately from false safety.

#### 13. Prove a summary is sufficient for a declared family of future writers
- **Mechanism:** Two histories are equivalent only if they admit the same safe updates in the declared future writer family, now and after common contract additions. Seek a minimal representative rather than reconstructing examples or retaining every facet.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Knoblauch et al.](https://arxiv.org/abs/2006.05188) already analyze the memory needed to recover task-set intersections; the possible object is a summary with an equivalence guarantee under restricted future writer queries. With a fixed family and exact absolute-coordinate intersection, equivalence after additions follows by construction; only resource savings or transport beyond that case are interesting.
- **Cheapest first test:** Enumerate small task tapes with identical current safe sets but different obligations outside the current writer plane; introduce a future plane that distinguishes them. Compare canonical constraint storage and replay.
- **Old-task retention check:** Verify A/C in the original and expanded families. A summary that promises only the old plane must abstain rather than claim the expanded directions safe.

#### 14. Trade one certified fallback for another atomically
- **Mechanism:** Verify two implementations of an old decision, then search for B writes with an explicitly certified switchover point where both pass, or an atomic endpoint if no handoff state is visible.
- **Novelty vs nearest prior art — IMPROVEMENT:** [PackNet](https://arxiv.org/abs/1711.05769) uses masks to isolate allocations. The alternative is migrating an old obligation so shared capacity can be reused, without an inference task cue.
- **Cheapest first test:** Give A two redundant routes and B competing claims on their shared weights; compare masking, a fixed fallback and same-capacity repair.
- **Old-task retention check:** Check A/C before the switch, at the handoff and after B, including the absent-fallback cases; do not restore old weights at evaluation.

### Long streams and decisive failures

#### 15. Measure the value of safe options, not the volume of safe weights
- **Mechanism:** At equal current B loss choose a safe endpoint that retains reachability to a declared menu of plausible future targets. Use exact reachability for an oracle and a past-only menu for a deployable arm.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Mode Connectivity](https://arxiv.org/abs/1802.10026) provides paths, not a CL acquisition criterion. The [ledger](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/idea-ledger.md) already killed Gramian plasticity reserve; beat cheap projected readiness before claiming a new effect. Exact options can matter when next writes have step bounds, require safe paths, or change the available writer; with unconstrained atomic jumps and identical future contracts, distance to other components alone confers no advantage.
- **Cheapest first test:** Construct two equally good B endpoints with different reachable safe successors under a shared finite step budget; compare projected readiness, maximum margin and a same-forecast beam search.
- **Old-task retention check:** Verify A/C and every acquired B at every prefix; match current B loss and report whether the next-task gain survives a menu miss.

#### 16. Learn a host whose safe set is easier to describe
- **Mechanism:** During acquisition reward broad compensating corridors or low facet count in a prescribed writer family, without requiring activations to stay fixed.
- **Novelty vs nearest prior art — IMPROVEMENT:** [HINT](https://arxiv.org/abs/2405.15444) already trains for weight intervals. The proposed target is a shape that preserves correlated, gate-crossing writes under an equal description budget.
- **Cheapest first test:** Train the same tiny host with a shared capacity cap, comparing corridor shaping, box training, margin maximization, and unshaped replay.
- **Old-task retention check:** Match acquisition accuracy and per-item margins; verify the declared old set through new writes and check unseen rare A/C cases separately.

#### 17. Bring back a conflict core when B cannot fit
- **Mechanism:** On a proved infeasible B target, return a small old-obligation core and the cheapest tested capacity or task-cue augmentation that resolves it. Distinguish infeasibility, a bad search, and timeout.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Reluplex](https://arxiv.org/abs/1702.01135) motivates verifier-style infeasibility; the CL test is whether the conflict actually chooses a cheaper augmentation than standard gradient conflict or adding a unit everywhere.
- **Cheapest first test:** Solve contradictory same-input tasks and a separate shared-bottleneck conflict, with equal-capacity expansions and an independently checked core.
- **Old-task retention check:** Refuse the impossible no-cue case; on allowed augmentation, verify all A/C including ambiguous inputs and report B adoption separately.

#### 18. Search up to a boundary that can survive deployment
- **Mechanism:** Use sound arithmetic error enclosures to reserve only the margin needed for actual rounding; exact ties follow the deployed tie rule or require a stronger checker.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Reluplex](https://arxiv.org/abs/1702.01135) verifies ReLU constraints; this is a practical cost comparison for robust publication, not a new verification primitive.
- **Cheapest first test:** In a quantized two-feature model compare exact discrete arithmetic, validated margin tightening, and a global worst-case ε; include candidates close enough to round across zero.
- **Old-task retention check:** Enumerate actual deployed A/C decisions at the same precision used by serving; count false-safe real-arithmetic certificates.

#### 19. Buy the counterexample that frees the most search
- **Mechanism:** Among violated old contracts, prioritize witnesses that prune many false candidate cells, rather than the lowest margin witness. Finish with a complete check; prioritization is never evidence of safety.
- **Novelty vs nearest prior art — IMPROVEMENT:** [SpecRepair](https://arxiv.org/abs/2106.01917) already alternates counterexamples and repairs; the delta is pricing a witness by its reuse across future candidate writes, not just the current violation.
- **Cheapest first test:** Plant one broad constraint and many deep, narrow violations; compare worst-margin, random and projected cell-pruning witnesses under equal verifier calls.
- **Old-task retention check:** Finish with the full A/C oracle at each commit; count rare violations skipped by fast search before the final audit.

#### 20. Reserve conditional certificates for policy histories
- **Mechanism:** In a finite deterministic environment, enumerate the baseline policy's reachable histories and enforce old decisions there. If decisions and transitions are unchanged, induct on history length; if the environment can vary or the policy is stochastic, explicitly expand the support or change the contract.
- **Novelty vs nearest prior art — IMPROVEMENT:** [CABA](https://arxiv.org/abs/2610.40740) already studies trajectory guarantees; the test isolates how much additional finite-write room a closed exact discrete support saves over protecting all states.
- **Cheapest first test:** Use a small route-choice tree with an exception reachable under a declared transition variant, versus a genuinely unreachable branch.
- **Old-task retention check:** Verify every live A/C trajectory under each declared variant, not just logged actions; test an undeclared reachability expansion as a required invalidation.

#### 21. Certify a whole family of B proposals with overlapping patches
- **Mechanism:** Answer a “range of new objectives” query by returning certified pieces and their usable B optima or bounds; amortize over many proposals, without taking a convex hull across gaps.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [APRNN](https://arxiv.org/abs/2304.03496) already solves constrained repairs. A reusable query interface must beat that solver warm-started with the same accumulated specs; pre-solving a grid is not enough.
- **Cheapest first test:** Repeatedly rotate a two-dimensional linear B objective, then sweep squared-distance targets through the gap of a disconnected safe set. Compare cached queries, exact fresh/incremental solves and interval unions. The linear optimum value sees only the convex hull; a squared-distance target in the gap distinguishes the two sets.
- **Old-task retention check:** Verify A/C at every returned deployable point and model-specific tie choice; check a deliberately unsafe midpoint to catch implicit convexification.

#### 22. Find the replay break-even and worst-case collapse
- **Mechanism:** Construct one stream with many duplicate cuts, one with independently binding cuts, and one with rapidly multiplying gate cells. Measure the cheapest exact or conservative summary at the same old contract and B progress.
- **Novelty vs nearest prior art — IMPROVEMENT:** Against [Experience Replay](https://arxiv.org/abs/1811.11682), [InterContiNet](https://arxiv.org/abs/2206.07996) and accumulated-spec repair, this is the parent's required kill test, not a new algorithm. [Knoblauch et al.](https://arxiv.org/abs/2006.05188) motivate the worst case; counting explicit facets is not a lower bound on all encodings.
- **Cheapest first test:** Enumerate redundant versus distinct supporting halfplanes of a polygon in two dimensions, then add a small gated case. Vary task count under equal bytes and solve time, with replay plus the same final verifier.
- **Old-task retention check:** Check the earliest and rarest A/C decisions after every prefix. Report whether any method that claims compression silently loses coverage or achieves less B progress.

## Ranked deeper questions

1. **What part of the region buys actual plasticity?** Start with 01 and 22. After matching attained B progress, isolate the benefit of exact decision slack, correlated movement within a cell, and crossing into other cells. Compare exact repair and oracle search to same-checker multi-direction proposals as well as GPM/OGD and DUET. If the affine margin solver or the cheap proposal stack closes the gap, don't credit gate geometry.
2. **Can contracts compose for many tasks without retaining or replaying all of them?** Test 07–13 and 22 on redundant, independently binding and changing-writer streams at equal storage, total work and held-out support. Require acquisition-anchored agreement at every advertised prefix. If every useful intersection or transport needs full re-verification, the region is a useful specification but not an efficient persistent object.
3. **Which shape can be certified and searched as writers get richer?** Take 02–05 and 18 from one mutable layer and finite inputs to multi-layer writers and continuous domains; report oracle gap, false-safe rate, and fraction of B improvements lost as “unknown.” If only a fixed-pattern box survives the comparison to learned-coordinate intervals or APRNN, narrow the claim to that restricted regime.
4. **Is there a new operation, rather than a familiar feasible set?** Require at least one of merge with prefix guarantees (07), writer transport (10/13), or amortized objective queries (21) to deliver a checkable contract consumed by more than one later operation and beat incremental repair plus the best simple summaries at equal total cost. Otherwise classify the node as an application of certified constrained learning, not a new primitive.
5. **Can safe choices today preserve useful updates tomorrow?** Test 15/16 in streams where step or routing constraints genuinely make endpoints matter. Compare projected readiness, margin shaping and equal-cost replay, and carry declared old decisions through every prefix. If the past-only menu cannot predict any benefit under those controls, don't revive the ledger's killed reserve idea under a geometric name.
