# Park crossings: spend one truthful batch on a jump or a joint landing

**Status:** Ideas and paper fixtures only; no implementation, learner runs, or GPU work. **Parent:** [Curved parks](curved-parks.md) ([PR #271][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, row 388][triage], #271 cards 05 and 10 (both score 3).

**Verdict:** Both moves are possible on engineered pools. Neither is a novelty win yet. A crossing matters if a real atomic batch gives B on-time service unreachable by lawful within-component training. A joint landing matters if the same indispensable pair buys more B service or uses fewer scarce records than the best stack of per-reader protections. Neither a drawn path nor two zero residuals establishes that advantage.

## Contract and deciding controls

- Freeze the ordinary optimizer, truthful record pool and indivisible units, arrival and batching rights, and the public read schedule before proposing a batch. Define the park using the **same** old read and tolerance throughout. A crossing requires distinct connected components of that safe set in the declared state domain, not merely two endpoints whose straight chord exits it. A straight segment is a geometric witness, not an executed trajectory. An intermediate state counts only if the real system publishes or consumes it; include live serving, checkpoints, split commits and stale readers where applicable. Do not create atomicity by hiding a scheduled old request.
- For joint closure freeze two independently exercised nonlinear reads, `R_A` and `R_C`, their reference values, and all tolerances. Where regular, show independent normals; also check that one read can fail with the other passing on a lawful intervention. Pair closure requires both finite endpoint residuals to pass; separate witnesses on different optimizer histories cannot be combined. Check whether the same pair loses the joint advantage when a candidate record's shared effect is removed, at matched gain and support. Give the separable baseline the same lawful record, batching and freeze rights.
- Evaluate held-out normal A service, rare C service, useful B work by a fixed deadline, and subsequent ordinary service with carried slots. Freeze margins and workload before selection; count waits, denials and fallbacks. Certify every declared lawful public trace. Match examples, native steps, latency, memory and preview work; log time spent finding and certifying pairs. No synthetic correction examples, gradient edits or optimizer resets in the proposed operation.
- Strongest stack: [relation parks][relation] plus [sealed entry][sealed], [pocket parks][pockets], [optimizer-aware rebatching][rebatch] and #271 finite previews; give it the same atomic and disjunctive checks. Compare to equal-budget [GraB][grab]/accumulation, best fixed order, and per-reader selectors stacked together. Report [OGD][ogd] and exact multi-constraint retraction as action-space controls: try both a same-component restriction and the best cross-component endpoint they can lawfully choose, charging off-language updates separately. Tiny exact enumeration is the feasibility oracle, not a baseline the same action space can out-admit.

## Two exact paper fixtures

Each named record is a fixed squared loss: sum of half-squares on its named coordinates, not an adjustable target or a gradient supplied to the optimizer. Use ordinary SGD on the mean of the records. These are deliberately constructed witnesses, not evidence of prevalence in natural pools or superiority to the exact selector.

### F1. One atomic commit crosses the gap

Start at `(x,y)=(1,0)`. Old routine A, queried on held-out z, returns `z + x² − y² − 1` with target z; its park is `x²−y²=1`. Old rare C is a separate positive classification with signed score `x²+y/2−1/2`. With step size 1, take the two fixed two-output B examples with targets `(−1,1)` and `(−1,−1)`. Their mean gradient is `(2,0)`, so the committed state is `(−1,0)`. The per-record squared errors both drop from 5 to 1. The A components have opposite x signs; at x=0 every y gives `x²−y²−1≤−1`, regardless of any other coordinates. Even an A tolerance strictly below 1 cannot join them.

| Execution at the same native step size | First committed weights | A defect after first commit | Held-out B error at first commit |
| --- | --- | ---: | ---: |
| Initial state (no work) | (1, 0) | 0 | 4 |
| Paired | (−1, 0) | 0 | 0 |
| First singleton, either choice | (−1, ±1) | −1 | 1 |

Held-out B measures `(x+1)²+y²` and must be at most `5/8` by the first commit. C passes at start and after the pair (score `1/2`). The two singleton orders already fail at their first public commit. In the half-step split diagnostic, either first singleton lands at `(0,±1/2)` and fails A too; this is not a claim about arbitrary schedules of private microsteps. A common subsequent ordinary record targeting `(−5/4,3/4)` takes the paired state there, keeps A exact and C positive, and gives held-out B error `5/8`. If both available records instead have y-target 1, the same pool grammar has no safe useful first commit. Neither branch labels nor a second copy of A are used.

### F2. A single record contributes to both nonlinear closures

Start at `(x,y,z)=(1,1,1)` and use step size 2. Routine A returns `a+y−x²` on held-out a; rare C returns `c+z−x³` on held-out c. Their targets are a and c. The normals `(−2x,1,0)` and `(−3x²,0,1)` are independent, and the x, y and z roles are all live. The fixed pool contains one x-only example targeting `1/2` and one indivisible two-output example targeting `(1/4,1/8)` on y and z. The latter's gradient is `(0,3/4,7/8)`. Together they land at `(1/2,1/4,1/8)`, the intersection, moving all three coordinates. The two-output loss drops from `85/128` to 0 and the x loss from `1/8` to 0.

| Action (one commit) | Weights | A defect | C defect |
| --- | --- | ---: | ---: |
| x singleton | (0, 1, 1) | 1 | 1 |
| y,z singleton | (1, −1/2, −3/4) | −3/2 | −7/4 |
| lawful pair | (1/2, 1/4, 1/8) | 0 | 0 |
| diagnostic pair with no z effect | (1/2, 1/4, 1) | 0 | 7/8 |
| diagnostic pair with no y effect | (1/2, 1, 1/8) | 3/4 | 0 |

The masked effects are diagnostic counterfactuals, not extra pool records. As a no-landing twin, change the old C read *before the window* to `c+z−x⁴`: neither singleton nor the pair closes both. For B use held-out squared error `x²+y²+z²` toward zero with deadline threshold `21/64` (from 3 to `21/64`). A common next truthfully labeled three-output record targets `(3/8,5/32,9/128)`; with the same step size it lands at `(1/4,1/16,1/64)`, where A and C remain exact and B error is `273/4096`. This checks shared effect, not synergy: the loss is separable. On a real pool, try the best independently sourced single-output compensators and price acquiring them; if packing or a lawful separable pair ties, do not claim a primitive.

## Idea cards

**P** = candidate primitive (a reusable operation or object); **I** = improvement or falsifier, not a pilot candidate by itself. Prior-art comparisons are nearest controls, not exhaustive novelty claims.

### Cross a component boundary while doing useful work

#### 01. Buy passage with a truthful pair (P)
- **Mechanism:** Offer a within-window transition between disconnected components using one native useful B commit, with a witness that neither constituent is separately publishable.
- **Novelty vs nearest prior art:** [Pocket parks][pockets] enter several pockets across histories; this is #271#05's transition on one history. [Mode connectivity][mode] seeks low-loss paths; it does not supply the discrete lawful edge when there is no safe path.
- **Cheapest first test:** Enumerate F1 subsets and split publications; replace engineered records with an independently labeled two-output pool. If a within-component selector or an allowed endpoint retraction meets the same deadline, no passage advantage.
- **Old-task retention check:** Query full A/C holdouts before and after the jump and after the next routine update; run the same due jobs on split and denial arms.

#### 02. Make passage insensitive to hidden approach histories (P)
- **Mechanism:** Use one public pair that moves every state in a compatible warmed fiber across the separator with native Adam, retaining correlated slots/clock; forbid a hidden history tag from selecting the action.
- **Novelty vs nearest prior art:** [Sealed entry][sealed] verifies a common entry word and #271 already handles correlated slots. The new object would be a common *crossing* edge with a proved opposite-component destination per input.
- **Cheapest first test:** Generate four warmed histories via actual records; seek one pair that crosses all four while first-slot-only and second-slot-only scores each misroute a different history. Give the public sealed stack the same fibers.
- **Old-task retention check:** Run identical held-out A and rare C at each history's first arrival, crossing and next native tick, including late arrivals.

#### 03. Let legal arrivals swap the roles of the lanes (P)
- **Mechanism:** A single public pair exchanges the two components across histories, with each lane becoming the other's useful starting point for the next arrival. Record the induced permutation, not a destination chosen from a private tag.
- **Novelty vs nearest prior art:** [Pocket parks][pockets] already have pocket-swap routing. The difference to test is preservation of the **opposite** lane's continuation after a useful atomic cross, rather than safe routing alone.
- **Cheapest first test:** Use a signed two-lane graph with two future B identities and two legal arrival orders; compare collapse-to-one-lane and separate per-lane routing with matched samples. Reject if the permutation is just relabeling.
- **Old-task retention check:** Replay old lane-sensitive C cases with targets frozen by job, as well as routine A; no relabeling those targets when state changes lanes.

#### 04. Sell a crossing that comes with a return option (P)
- **Mechanism:** Issue the outbound pair only with a certificate that a not-yet-arrived truthful pair can take the learner back from each permitted post-crossing state by the old job's due time.
- **Novelty vs nearest prior art:** [Return corridors][return] and #271's reserved second chords already plan a continuation. The bet is a return right that spans a separator in *both* directions without reserving a separate copy of the initial weights.
- **Cheapest first test:** Enumerate a two-lane, two-arrival menu where the nearest outbound endpoint destroys every native return pair but a farther one leaves two. Compare a joint corridor solver and save/restore at equal storage.
- **Old-task retention check:** Keep normal A/C serving while away, then dispatch an old job that actually needs the restored lane; include the trace with no permitted return offer.

#### 05. Invoice the exact observer that vetoes a jump (I)
- **Mechanism:** Attach a negative witness to a refused crossing: the earliest real reader, state version, and old request that sees an unsafe published prefix under the existing commit protocol.
- **Novelty vs nearest prior art:** [Linearizability][linear] already separates atomic from visible intermediate state; this is an audit that prevents interpreting arithmetic microsteps as commits or real reads as private.
- **Cheapest first test:** Use F1 in a trace with replica reads before/after commit, then add a genuine split publication or checkpoint side effect. Compare a final-state-only checker.
- **Old-task retention check:** Verify A and rare C at each reader's actual version; stale-but-legal reads must also meet their existing freshness SLA.

#### 06. Transport a crossing certificate without transporting the weights (P)
- **Mechanism:** Retain a small record-side witness binding native endpoint image to a named opposite component; check it against a new reachable state and its public optimizer/version, not a copied destination.
- **Novelty vs nearest prior art:** #271's chord families certify endpoint closure. Extra value would be certifying *component change* across independently warmed states without recertifying the full park.
- **Cheapest first test:** Fit a certificate on one narrow hyperbola chart and challenge it on a wider held-out chart plus a domain with an unexpected safe detour. Compare exact preview and exact topology checks.
- **Old-task retention check:** Run A/C on unseen chart extremes and at the next update; an unknown component proof denies admission rather than widening old margins.

#### 07. Clear a component without stranding a delayed job (P)
- **Mechanism:** Couple the useful crossing to a declared transfer of pending service obligations: the same native step makes the destination satisfy the source lane's still-due job without a routing switch.
- **Novelty vs nearest prior art:** [Pocket parks][pockets] already let B open a bridge. Here no safe bridge appears; a distinct pending job becomes serviceable across a jump of a fixed read.
- **Cheapest first test:** Cross F1's topology with two earliest/latest arrival traces for a delayed A job; add a twin where timely B succeeds but the delayed job is stranded. Compare a lane-preserving scheduler with the same queue.
- **Old-task retention check:** Query old versions and the newly served lane at actual due times, including the oldest request and a rare C arriving during the delay.

#### 08. Prove a missing edge before spending the deadline (P)
- **Mechanism:** Certify that all attainable single-batch endpoints miss the destination component or fail B, using bounds on *lawful* record pairs through the live optimizer rather than bounds on arbitrary update vectors.
- **Novelty vs nearest prior art:** #271's attainable-image checks and ordinary reachability already bound endpoints. A reusable no-edge witness for the target component could let the same system admit a different offer before the clock expires.
- **Cheapest first test:** Stratify a small real record menu by support; test one unreachable twin and one outlier pair that defeats the coarse bound. Compare exhaustive previews including their cost.
- **Old-task retention check:** In blocked windows serve A/C normally and count the lost B offer; use exactly the same holdouts after a later successful admission.

#### 09. Turn component confinement into an honest lower bound (I)
- **Mechanism:** Tie any service-safe continuous strategy to a within-component B floor, then try to remove the floor by reparameterization, a wider valid domain or a different old tolerance.
- **Novelty vs nearest prior art:** Connectedness is standard and [mode connectivity][mode] warns against straight-line evidence. This is a falsifier for spurious disconnectedness, not a new optimizer.
- **Cheapest first test:** Contrast a real hyperbola separator with an annulus and with a higher-dimensional detour around a projected gap. Measure useful B on each before testing any novel admission algorithm.
- **Old-task retention check:** Check held-out A/C along the lawful detour and at deployed tolerances; do not define the separator from the B objective.

#### 10. Batch a crossing with a useful source-lane repair (P)
- **Mechanism:** Pair a truthful B record that supplies most of the crossing displacement with a required repair example for an existing old job whose loss would otherwise worsen, closing its read at the destination.
- **Novelty vs nearest prior art:** [GEM][gem] mixes old gradients to avert forgetting; [GraB][grab] improves gradient order. The candidate is a coupled old repair and discrete B jump where postponing either record misses its own deadline.
- **Cheapest first test:** Use a two-lane pool with one overdue A repair and one B offer; compare old rehearsal followed by B, accumulation at the same publication boundary, and the strongest joint selector. Require an interaction beyond simple old-example replay.
- **Old-task retention check:** Show repair transfer to unseen A examples plus unrelated C; neither merely preserving A's sentinel nor replaying its score counts as useful repair.

### Close two reads with a shared record

#### 11. Jointly close independent old curves (P)
- **Mechanism:** Use an indispensable record's finite effects on both nonlinear reads in the same useful pair, separating true sharing from two independent protectors packaged as one record.
- **Novelty vs nearest prior art:** This is #271#10. Exact multi-constraint retraction already lands at intersections; the possible primitive is joint closure under fixed truthful membership and a binding acquisition/arity budget.
- **Cheapest first test:** Start with F2 and replace the separable loss with a fixed feature map and one naturally shared label. Compare the union of independent selectors, exact joint previews, both single-effect masks and an incompatible-intersection twin.
- **Old-task retention check:** Exercise A/C separately on unseen inputs before/after the commit and after a typical old update; audit another holdout that detects duplicating one old constraint.

#### 12. Buy joint closure with one scalar label (P)
- **Mechanism:** Seek a naturally shared scalar-label example whose feature gradients into the two normal directions have the ratio required by the finite move; do not set those directions independently.
- **Novelty vs nearest prior art:** [GradMatch][gradmatch] selects weighted subsets to fit a gradient; machine teaching can design examples. This would be an indivisible **observed** example closing two finite defects without either power.
- **Cheapest first test:** Scan existing rank-one squared-loss examples and compare their lawful ratio support to independently chosen y/z adjustments at the same acquisition cost. Reject if a weighted record not legal in the protocol is needed.
- **Old-task retention check:** Match old margins before selection and test rare C and held-out A after the useful update and a common subsequent arrival.

#### 13. Certify the useful common direction, not just the intersection (P)
- **Mechanism:** A pair receipt states both closures and proves progress along the intersection in a direction neither single-read protection can promise at the same deadline.
- **Novelty vs nearest prior art:** Joint tangent projection and Pareto descent already identify common directions; proposed added value is a finite, achievable **record pair** with a B lower bound through curvature, not a tangent-space prediction.
- **Cheapest first test:** Compare two pairs in a three-coordinate fixture, both closing A/C but only one improving an independent B holdout. Match directional gradient and initial margins against exact previews.
- **Old-task retention check:** Query both old reads plus a routine workload after each pair; require the useful common direction not to buy B by exhausting C's margin.

#### 14. Build an incompatibility certificate from isolated closures (P)
- **Mechanism:** Prove that both reads can close individually yet their useful pair sets have empty intersection under the lawful menu, returning the minimal conflicting requirement and scarce record role.
- **Novelty vs nearest prior art:** Infeasible cores and #271's no-good cuts already refute candidates. The bet is a compact **two-reader supply** witness that tells a future selector which record role, not which tolerance, must change.
- **Cheapest first test:** Enumerate six records with individually adequate but disjoint useful closures, then replenish one actual shared example. Compare intersecting exact pair sets to the certificate's prediction on unseen menus.
- **Old-task retention check:** A rejected B offer must leave A/C operating normally; when supply improves, recheck both along the whole public window.

#### 15. Keep closure through a routine old-task update (P)
- **Mechanism:** Select a joint landing not just for two residual zeros, but for compatibility with the existing next old A or C update using the slots the pair leaves behind.
- **Novelty vs nearest prior art:** #271's failed Adam continuation already warns about first landings. New leverage would come from one pair buying compatibility with **either** next reader's native maintenance action without freezing a coordinate.
- **Cheapest first test:** Find two exact first landings with different carried moments; enumerate both legal next maintenance records and compare a joint lookahead to independent and unioned one-reader guards.
- **Old-task retention check:** Run A and C jobs after either maintenance update, then rerun B to rule out saving the two reads by undoing the new learning.

#### 16. Share a compensator across independently declared readers (P)
- **Mechanism:** Let each service declare its fixed read separately; certify the same pair against their union without installing two adapters or migrating their reader definitions. Retain enough evidence to maintain the unchanged part if one reader leaves.
- **Novelty vs nearest prior art:** Modular parks offer per-reader protection; the conditional gain is amortizing a common indivisible learning effect, not simply caching checks.
- **Cheapest first test:** Use three declared consumers with overlapping gradients and two lawful conjunctions. Compare one common pair to one pair per reader, independent adapters, deduplicated verification and the best joint selector.
- **Old-task retention check:** Evaluate all installed readers separately, including an infrequent third consumer after the declared departure of a different reader.

#### 17. Find out whether curvature supplied the sharing (I)
- **Mechanism:** Compare the same pool against old reads with matched local normals but different finite curvature; use a matched-read family and lawful coordinate change to check whether shared closure is just linear cancellation.
- **Novelty vs nearest prior art:** #271 already compares tangent against finite closure. This isolates how much of **joint** availability is attributable to finite curvature rather than support, symmetry or changed margins.
- **Cheapest first test:** Around F2's start replace each curve with its tangent and with a curvature twin. Reweight neither record; compare the exact useful arity and give the baseline the best reparameterization respecting the native update.
- **Old-task retention check:** Report normal held-out service within each frozen world at matched initial margins, including both old tasks after the next common update.

#### 18. Price closure in dwindling examples, not nominal arity (P)
- **Mechanism:** Treat each joint landing as spending particular scarce lawful record uses; prefer a pair with equivalent immediate closure that leaves independent reserve for future readers.
- **Novelty vs nearest prior art:** #271's future chord supply and teaching dimension cover reserve and example counts. The candidate resource is the joint compensator's shadow cost across multiple old reads, compared at fixed acquisition rights.
- **Cheapest first test:** Give a tiny stream one shared example and several separable corrections with preset reuse limits; enumerate future demands, including a twin with unlimited supply where splitting should tie.
- **Old-task retention check:** Continue normal A/C through later offers, and count service denials when a critical compensator was consumed early.

### Make the two seeds compete and combine

#### 19. Jump onto the far intersection (P)
- **Mechanism:** Close A and C with the same commit *and* move to a different component of A's park. The critical case is a pair whose contribution to C changes which crossings are feasible, not independent motion in an extra coordinate.
- **Novelty vs nearest prior art:** Sealed pocket entry plus multi-constraint retraction already describes disjunctive joint endpoints. Candidate novelty is an interaction in lawful useful pair supply that the strongest stacked selectors cannot afford.
- **Cheapest first test:** Intersect F1's hyperbola with `z=x³`; include same-side joint pairs and A-only crossing pairs. Use a 2×2 crossing/joint ablation, including a separable matched stack and an unreachable far intersection.
- **Old-task retention check:** Serve A and rare C before, after, and following an ordinary carried update; run the no-far-landing twin with the same service deadlines and count rejection.

#### 20. Escape a one-reader-safe cul-de-sac (P)
- **Mechanism:** Make a joint landing that also jumps between components of the **joint** safe set, even though each individual safe set is connected; otherwise one-reader planners can each promise an invalid route.
- **Novelty vs nearest prior art:** Multi-constraint topology already permits this. The conditional learning operation would compile a discrete useful edge that both individual continuity-based guards miss, at real optimizer and sample budgets.
- **Cheapest first test:** Use `y=x²` and `y=1+z²` in three coordinates. Each surface is connected; their exact joint set implies `x²−z²=1`. Test an opposite-sign useful pair and a predeclared twin with both tolerances set to 1/2, where the line `z=0, y=1/2, −1≤x≤1` bridges the two sides.
- **Old-task retention check:** Evaluate both frozen reads under their deployed tolerances and schedules, plus independent routine/rare tasks, rather than substituting the algebraic joint equation for all service.

#### 21. Accept equivalent landings without conflating their futures (P)
- **Mechanism:** Group hops and joint landings by the due service and admissible future batch menu they induce, while keeping distinct reachable states/slots for proof until continuation equivalence is shown.
- **Novelty vs nearest prior art:** [Commuting writebacks][commute] and trace partitioning already abstract observable behavior. Added value would be a certified shared continuation interface spanning both kinds of finite transitions at lower verification cost.
- **Cheapest first test:** Exact-enumerate a two-window graph where A/C endpoints match but one site's next joint or cross-lane pair fails. Compare endpoint grouping, exact graph and a stronger continuation-sensitive partition.
- **Old-task retention check:** Replay all next old-maintenance alternatives and held-out A/C at the old deadlines; split the class when any service outcome differs.

#### 22. Make the first surprising result survive the natural-pool null (I)
- **Mechanism:** Freeze a natural arrival pool and search for both operations without constructing labels from the desired endpoints. Repeat on a held-out pool with norms, margins and per-record B value matched to the candidate pool.
- **Novelty vs nearest prior art:** This is a falsification control against engineered teaching and norm/selection confounds, not a new primitive.
- **Cheapest first test:** Exhaust small pools from fixed labeled regression tasks using native SGD, then a small warmed-Adam grid if supply exists. Compare exact preview, shuffled memberships and the strongest lawful stack at the same deadline.
- **Old-task retention check:** Use blind ordinary A and rare C holdouts, logs of every public boundary, and a subsequent routine update. Record rejections as outcomes rather than reporting only selected pairs.

## Ranked deeper questions

1. **Does an independently supplied pool make a shared closure cheaper than the separable stack?** (11, 12, 17, 22) Count on-time useful joint admissions at fixed record acquisition/arity and matched old margins. First compare exact reachable useful sets, then test whether a shared-effect receipt finds such pairs more cheaply on held-out pools. Retire the claim if label construction, independent compensation or a lawful reparameterization explains the advantage.
2. **Can native passage buy B service at the system's actual observation granularity?** (01, 02, 05, 09) Establish the separator with deployed tolerances, measure earliest B completion against lawful component-constrained and jump-capable stacks, then replay real reader versions and the split negative. Stop if any actual reader sees failure, or if accumulation or a safe connected route matches it.
3. **When is the far intersection an interaction, not two constraints in a nicer demo?** (19, 20) Cross the two seed operations factorially, then offer the full jointly verified separable stack. Keep the merge only if record sharing changes attainable on-time safe B coverage and the no-far-intersection twin is rejected.
4. **Does landing buy useful continuation, or only postpone forgetting?** (04, 15, 18, 21) Compare one-step admission, exact two-window oracle and economical continuation witnesses under real arrival and slot histories. Require normal old A/C including rare jobs after a maintenance tick and count the cost of preserving return or shared-pair supply.

[parent]: https://github.com/manojbajaj95/cl/pull/271
[ledger]: https://github.com/manojbajaj95/cl/blob/106d39d945a291827513b938711138c0535a4259/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/106d39d945a291827513b938711138c0535a4259/reviews/flood-triage.md#L388
[relation]: https://github.com/manojbajaj95/cl/pull/255
[sealed]: https://github.com/manojbajaj95/cl/pull/260
[pockets]: https://github.com/manojbajaj95/cl/pull/270
[return]: https://github.com/manojbajaj95/cl/blob/devin/1795562037-return-corridors/tree/return-corridors.md
[rebatch]: https://github.com/manojbajaj95/cl/pull/225
[commute]: https://github.com/manojbajaj95/cl/pull/217
[grab]: https://arxiv.org/abs/2205.10733
[ogd]: https://arxiv.org/abs/1910.07104
[gem]: https://arxiv.org/abs/1706.08840
[mode]: https://arxiv.org/abs/1802.03888
[gradmatch]: https://arxiv.org/abs/2103.00123
[linear]: https://doi.org/10.1145/78969.78972
