# Cancelling-pair renewal

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Self-replenishing capacity](self-replenishing-capacity.md) ([PR #170](https://github.com/manojbajaj95/cl/pull/170)), cards 03 and 11. **Review seed:** [Flood triage row 271](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/flood-triage.md#L271) scored two ideas 3: atomically renew two cancelling hidden units and aim their gates at different future edits; prune stored descendants only when another branch can simulate their useful continuations.

**Is output-neutral structure as a renewable resource a new object for continual learning?** Cancellation is not new. [Net2Net](https://arxiv.org/abs/1511.05641) splits units with function preservation; the [Embedding Principle](https://arxiv.org/abs/2111.15527) studies function-preserving critical embeddings, including redundant units. [GradMax](https://arxiv.org/abs/2201.05125) adds initially neutral capacity to improve optimization; [neural teleportation](https://arxiv.org/abs/2012.01118) and [symmetry teleportation](https://arxiv.org/abs/2205.10637) change trainability without changing the function or symmetry-invariant loss, respectively. [Git Re-Basin](https://arxiv.org/abs/2209.04836) uses permutations to find low-loss connections; linear mode connectivity doesn't certify pointwise equality or preserve future edit access. [GPM](https://arxiv.org/abs/2103.09762) protects stored activation subspaces by projected updates, and [APRNN](https://arxiv.org/abs/2304.03496) already does finite architecture-preserving repair. [ReDo](https://arxiv.org/abs/2302.12902), [continual backprop](https://arxiv.org/abs/2306.13812), and [shrink-and-perturb](https://arxiv.org/abs/1910.08475) are the recycling and reset controls. [Alternating simulation](https://www.cs.huji.ac.il/~ornak/publications/concur98.pdf) already provides the pruning relation.

The candidate is a **fixed-width renewal operation with a continuation guarantee**: reclaim jointly silent but individually live structure, reshape it into distinct certified ways to serve editors that did not see the branch, and repeat without spending down another reserve or quietly dropping a protected task. Following the [idea ledger](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/idea-ledger.md), this is an intervention, not another plasticity score: the [retention-matched reserve rerun](https://github.com/manojbajaj95/cl/pull/21) left only 0.09 absolute MSE points of spread. Count independently useful admissions and absolute gains at equal retention, not rank, menu size, or parameter distance.

## Contract and two paper witnesses

Let `P` be the union of declared protection domains, with acquisition-anchored output or task floors for all live obligations. Require **pointwise output equality across each renewal** on `P`, including declared rare slices. Across a committed edit, require the predeclared utility gain versus no write and every installed floor; add the new obligation if its contract persists. A fit on finite probes certifies only those probes. Freeze the request bank, addresses, utility tests, budgets and disclosure before choosing the renewal. Match peak bytes (including spare slots, branches, optimizer state, certificates and scratch), verification and edit compute, offline training and online deadlines. Never count refusal, rollback, or undoing requested utility as service.

**Two finite openings, not yet a cycle.** In a scalar residual ReLU block on `P = [-1, 1]`, keep the old predictor `f(x) = x` and two additional units with readout coefficients `+1, -1`. Initially both activations are `[1]₊`: removing either alone changes every protected output. Atomically replace the activations by `[x - 2]₊` and `[-x - 2]₊`. Both are now zero on `P`. Precommit a right request to increase only the first bias by 1 and demand residual `+1` at `x = 2`; precommit a left request to increase only the second bias by 1 and demand `-1` at `x = -2`. Neither request works on the original pair: it changes protected outputs. After renewal either request works and leaves `P` exactly unchanged, and installing the second leaves the first target unchanged. This needs an atomic publication boundary, not a claim that arbitrary sequential assignment preserves outputs. It also changes outputs *outside* `P` before either edit (for example at `x = 3`); it is not a global symmetry. After both requests, the gates carry obligations: resetting them is not evidence of a second renewal. A dormant reserve aimed at the same two targets would behave identically at the endpoint; the possible gain is in reaching that endpoint at fixed width from a state where no unit is disposable alone.

**A bigger immediate menu can be worse.** Consider equal-cost certified response graphs with identical starting observations: `X —u→ X₁ —u→ X₁`; `Y —u→ Y₁ —u→ Y₂` and `Y —v→ Y₂`, where `Y₂` has no useful response. Every shown edge is a distinct useful operation in its round (e.g. on a new round context with a bounded-duration contract), not a no-op; this graph is a pruning witness, not a constructed neural realization. One-step set inclusion prunes `X` in favor of `Y`; a two-step check also sees no lost `X` trace. The third `u) fails. A request for `v` fails from `X`, so neither state should replace the other. Within a declared finite horizon a simulation may be truncated only at that horizon, not sold as a renewable guarantee.

Write `Y ⪰ X` if the states match the contractual observations and protection scope, and for **each** admissible request and certified useful response edge from `X`, `Y` has a response to the *same* request with at least its contracted utility, no greater cost in any binding budget, and a successor that again simulates the `X` successor. Keep remaining budgets, active obligations, disclosures and timing in the state. If the environment can choose a successor after a response, **every** such outcome at `Y` must be matched by an allowed outcome at `X` with matching observations and a related successor. Only compare under the same external request interface; if a menu is itself a promise visible to the requester, preserve its specified observations too. Use the greatest relation on the finite graph (or a checked inductive under-approximation); no certificate means keep the branch, recompute on demand without discarding its option, or decline a new guarantee. Age, current equality and next-menu inclusion are not pruning certificates.

## Idea cards

### Reclaiming jointly silent structure

#### 01. Renew both live units in one transaction
- **Mechanism:** Identify opposite-readout units with equal activations on `P`; stage replacement gates with separately aimed openings and publish them together.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Net2Net and the Embedding Principle give neutrality; the hypothesis is reusable access from jointly recyclable live slots that unit-wise ReDo misses.
- **Cheapest first test:** Enumerate the scalar witness and nearby gate choices; compare independent resets, reset plus exact joint repair, and pair renewal with identical slots, moves and frozen requests.
- **Old-task retention check:** Prove equality over `P` at publication, fail each solo ablation, and check the first installed target when the other edit lands.

#### 02. Train the match only where it is owed
- **Mechanism:** Fit two different preactivations that coincide when active over protected cells (and may differ off-domain); constrain their sum rather than forcing weight duplication.
- **Novelty vs nearest prior art — IMPROVEMENT:** Unlike globally function-preserving teleportation, this spends declared off-domain freedom; exact local repair already allows such constraints.
- **Cheapest first test:** Use two protected line segments in 2D with a withheld segment for new requests; compare global duplicates, domain-constrained pairs and joint APRNN at the same width and move cost.
- **Old-task retention check:** Prove equality on the entire protected segments, including endpoints; treat a deliberately omitted old segment as a scope failure if it was owed.

#### 03. Buy complementary gates without knowing the next edit
- **Mechanism:** Aim a pair using only historical request families, rewarding independently serviceable directions rather than the best fit to a single predicted request.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** GradMax targets gradients at growth time; here the output is a reusable choice of finite useful edits for separately authored editors under a fixed host contract.
- **Cheapest first test:** Freeze same-side and opposite-side two-edit banks; compare against random aiming and GradMax-style direction selection plus exact verification with the same budget. Hold out payload coordinates.
- **Old-task retention check:** Match old outputs before the bank is opened and check each permanent installation after both edit orders.

#### 04. Measure what pairing adds over spare width
- **Mechanism:** Reserve the same two slots in every arm and vary only how they are acquired: deliberate cancellation, zero readout, or exact merge and reuse.
- **Novelty vs nearest prior art — IMPROVEMENT:** GradMax and [PackNet](https://arxiv.org/abs/1711.05769) already offer forms of neutral growth or reuse; this tests whether the pair is more than hidden spare capacity.
- **Cheapest first test:** Fit the same prior task family in a four-slot host, then run each renewal method on a precommitted two-step request trace with capped bytes and exact repair available to all.
- **Old-task retention check:** Match old-task utility at acquisition and track the worst ordinary and rare slice across all writes, including when the reserved arm runs out of slots.

#### 05. Move through an exact neutral path when atomic swaps are impossible
- **Mechanism:** While gates still match, scale both signed readouts down to zero; move gates; restore the signed readouts only after both gates are certified dormant on `P`.
- **Novelty vs nearest prior art — IMPROVEMENT:** Mode connectivity supplies paths with low loss, not this path's pointwise guarantee; generally it is a constrained path-planning problem.
- **Cheapest first test:** Compare the three-stage path, atomic replacement and straight interpolation on the scalar witness, charging publish barriers and verifying all permitted reads between stages. Test single-write hardware separately.
- **Old-task retention check:** Verify every allowed intermediate state as well as both endpoints; do not allow a read between two signed changes without checking it.

#### 06. Find a neutral group when no two units cancel
- **Mechanism:** Search for small support relations among activations on verified ReLU cells, then rotate the group into two useful gates and return the remaining slots to the host.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Null relations themselves are linear algebra and GPM already uses subspaces; the candidate is a finite joint release that returns editable slots beyond what pairwise reuse can reach.
- **Cheapest first test:** Plant active columns `1, x+2, x+3` on `[-1,1]` with coefficients `1, 1, -1`. Compare pair-only recycling, circuit enumeration and exact joint repair with an equal check budget.
- **Old-task retention check:** Prove the relation on every protected cell and evaluate any reclaimed slot's first and second uses against all old floors.

#### 07. Reject cancellation supported only by a probe set
- **Mechanism:** Mine a separating ReLU cell if the aggregate matches observed outputs but fails between them; feed the witness back into pair selection.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is counterexample-guided repair and verification, not a new certificate class.
- **Cheapest first test:** Place a narrow triangular residual between probes in a two-layer piecewise-linear block; contrast probe matching with interval bounds and exact cell checks at the same verification deadline.
- **Old-task retention check:** Include the hidden peak in the protected continuum oracle and measure false acceptance, not just sampled accuracy.

#### 08. Support a nonzero protected signal while releasing both gates
- **Mechanism:** If a nearly cancelling pair leaves a certified low-complexity residue, move that residue into an existing readout before reclaiming the pair; account for the receiving readout's future obligations.
- **Novelty vs nearest prior art — IMPROVEMENT:** Inverse Net2Net and APRNN already cover exact merge/repair; the useful question is when routing a residue costs less than keeping both gates occupied.
- **Cheapest first test:** Add a constant protected residual to the witness. Compare bias absorption, joint repair and refusal; include a slope-changing residual the bias cannot absorb.
- **Old-task retention check:** Check equality across the transfer and rerun old slices after edits to the receiving readout as well as edits to the released gates.

#### 09. Make the pair legible after a change of parameter ruler
- **Mechanism:** Freeze edits in functional units (signed target residual and permitted region), then translate them to gate changes using a published canonical convention.
- **Novelty vs nearest prior art — IMPROVEMENT:** Teleportation and Git Re-Basin already expose rescaling and permutation symmetries; this is a control against a fake gain from cheaper raw parameter coordinates.
- **Cheapest first test:** Permute and rescale the two gates with adjoint readout rescaling. Compare raw bias-address requests with transported requests under the same functional and resource budget.
- **Old-task retention check:** Check pointwise old equality under reparameterization and verify the same old-task floors under transported edits; do not count lucky slot naming.

#### 10. Renew optimizer dynamics, not only the forward pass
- **Mechanism:** Bind optimizer slots to the pair transaction: transport them, reset them, or couple their updates to keep cancellation until a committed request.
- **Novelty vs nearest prior art — IMPROVEMENT:** Continual backprop and reset methods already restore optimizer plasticity; the test isolates cancellation stability from the benefit of fresh moments.
- **Cheapest first test:** Replay five identical minibatch steps in a scalar momentum toy after each renewal policy, with an optimizer-reset-only control and matched update norms.
- **Old-task retention check:** Verify equality at commit and floors after every optimizer step; a cancellation that survives initialization but drifts before a request is not a reserve.

#### 11. Put a price on strong cancellation
- **Mechanism:** Require a numerical error bound for equal-and-opposite readouts under the deployed arithmetic; penalize large cancelling contributions that leave little rounding margin.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is numerical conditioning applied to renewal, not evidence of new capacity. The gain would be pairs that remain cheap to certify at useful precisions.
- **Cheapest first test:** Compare rational arithmetic with a deliberately low-precision scalar forward pass, testing paired summation, ordinary summation and zero-readout reserves.
- **Old-task retention check:** Require bitwise equality if promised at deployment, otherwise reject the pair under this node's exact renewal contract rather than calling a tolerance exact; recheck old utility floors after use.

### From two openings to renewal

#### 12. Recover the reserve without borrowing from another layer
- **Mechanism:** Seek a closed set of pair configurations that can admit each declared request and return to a renewable state without debit to width, hardware scratch, or another layer's plasticity.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Viability theory gives invariance, and recycling gives resets; here the question is whether real retained utility can coexist with a paid return using the same live slots.
- **Cheapest first test:** Enumerate a four-unit rational host and solve the finite safety game with separate expiring and permanent requests. Compare stock resets plus exact planning on the identical move menu.
- **Old-task retention check:** Verify equality on all live domains at each renewal, track all persistent floors, and report any obligation whose expiration was necessary to close the cycle.

#### 13. Convert spent gates back into a cancelling pair
- **Mechanism:** Compress already installed gate behavior into compatible existing units when it agrees on the union of live domains, then reconstitute opposite-readout carriers from the freed slots.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Net2Net and PackNet recycle redundancy; the hypothesis is that two separately useful writes can be made jointly releasable without rollback or additional permanent slots.
- **Cheapest first test:** Plant compatible and incompatible pairs of previous writes in a four-unit host, then compare exact consolidate-and-renew, merge-and-prune, and generic repair plus reset. Demand a third useful write.
- **Old-task retention check:** Prove equality on both installed domains during consolidation, reject the incompatible example, and check their floors after the third write.

#### 14. Derive the first obligation sequence that exhausts the host
- **Mechanism:** Grow a bank of disjoint old targets with independently chosen signed piecewise-linear kinks; use the minimum number of distinct required breakpoints as a lower bound for a fixed one-layer scalar ReLU host with affine skip.
- **Novelty vs nearest prior art — IMPROVEMENT:** Capacity lower bounds are known; this one separates a reusable operation from an impossible indefinite-retention promise.
- **Cheapest first test:** Specify exact values on disjoint protected intervals, each with a forced kink; hand-derive infeasibility at width plus one, then compare a renewal planner with capped expansion.
- **Old-task retention check:** Check full prior intervals after each accepted target and report honest refusal at exhaustion rather than replacing the oldest kink.

#### 15. Transport a reserve across a drifting representation
- **Mechanism:** When an upstream encoder changes, transport the joint cancellation and revalidate both gate boundaries against protected inputs, instead of assuming unchanged gate weights imply unchanged options.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Teleportation supplies exact transports for symmetries; this asks whether pair renewal can carry an edit interface over non-symmetric representation drift more cheaply than building it again.
- **Cheapest first test:** Use an affine drift with an exact transport and a folded piecewise-linear drift without one; compare transport then renew, reuse unchanged gates, and re-solve from scratch.
- **Old-task retention check:** Evaluate in original input coordinates before and after drift and renewal, including a rare region that becomes close to a gate, then test earlier edits after a new request.

#### 16. Test whether gradual training learns to create renewable pairs
- **Mechanism:** During ordinary learning, expose counterexamples where no pair move restores two different frozen openings; shape hidden features to avoid those dead ends rather than directly normalizing a reserve score.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Continual backprop injects features online; the hypothesis is learned entry into a certified renewable class, not prediction from the ledger's failed Gramian.
- **Cheapest first test:** Enumerate exact fits to an intermediate task on a grid. Compare ordinary-fit and counterexample-fit states using the same exact planner on a held-out, retention-matched request bank; stop if the useful admission spread vanishes.
- **Old-task retention check:** Match intermediate task utility and all past outputs at entry and check every old floor from the same acquisition anchor across the held-out sequence.

### Store alternatives only while their continuations differ

#### 17. Prune only with a budgeted simulation certificate
- **Mechanism:** Delete stored `X` only when retained `Y` simulates its useful request-and-response edges recursively, including renewals, cost and obligations. Publish a checkable response map.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Alternating simulation is not novel; its potential CL use is compressing an equal-output renewable frontier without dropping independently useful edit sequences.
- **Cheapest first test:** Use the two graphs in the witness plus an actual finite gate-state graph if realizable. Compare against one- and two-step inclusion as diagnostic controls and exact alternating simulation as the strongest control, at equal peak bytes.
- **Old-task retention check:** Independently verify the acquisition floors on every retained response edge and exhibit a replayable request trace for every planted false pruning.

#### 18. Synthesize a replacement instead of choosing which branch to keep
- **Mechanism:** Search the protected-output fiber for a new two-gate configuration that simulates two stored branches simultaneously; publish and prune only after both proofs pass.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Git Re-Basin seeks aligned low-loss merges and game simulation checks substitution; the conjecture is that learned or synthesized gate geometry can combine continuation sets at lower total cost than storing or rebuilding them.
- **Cheapest first test:** Store two one-sided gate states from a rational host; search for a two-sided substitute and plant a second case with mutually incompatible future obligations. Compare weight interpolation plus verification and exact generic synthesis.
- **Old-task retention check:** Require unchanged currently protected outputs at substitution and verify each original branch's requests and every related successor's installed tasks on both graphs.

#### 19. Run the simulation under competing demands for the same pair
- **Mechanism:** Model edit requests and deadlines as environment moves, not as independently redeemable quotes. Include the in-flight reservation of both slots in simulation state.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Pacti](https://arxiv.org/abs/2303.17751) and alternating refinement already cover contract compatibility; this tests a concrete double-booking failure in neutral pair frontiers.
- **Cheapest first test:** Offer two editors either disjoint slots or overlapping atomic reservations. Compare sequential proofs to a joint-demand simulation with identical deadlines and peak scratch.
- **Old-task retention check:** Check acquisition floors after both possible commit orders and at every observable intermediate state; timeout cannot erase an installed obligation.

#### 20. Distinguish cheap first steps from cheap recurrence
- **Mechanism:** Include remaining per-round and lifetime ledgers in the relation, including verification, cache eviction and regeneration. A branch may look cheaper only by shifting its bill to a successor.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is cost-aware refinement, not a new order. It tests whether compression saves actual resources rather than changing when the work is paid.
- **Cheapest first test:** Plant two equal-output graphs with equal immediate cost but a forced costly renewal at depth three in one arm. Compare raw step costs, remaining-budget simulation and exact planning.
- **Old-task retention check:** Verify all live tasks on every edge, including after the costly renewal; a branch that misses the deadline may refuse but must not take an unsafe shortcut.

#### 21. Factor branch proofs only if the factors cannot interfere
- **Mechanism:** Compose per-pair response maps when gate writes, protected residuals and budgets have a certified independence boundary; otherwise keep a joint relation.
- **Novelty vs nearest prior art — IMPROVEMENT:** Compositional refinement is established; the opportunity is retaining more exact alternatives per byte without paying for the full product graph.
- **Cheapest first test:** Compare explicit product simulation and factored certificates for two pair banks, then share one receiving readout and check that the factorization is rejected.
- **Old-task retention check:** Check the aggregate old output after interleaved writes and renewal, including a planted corner where both individually harmless approximations would breach a floor.

#### 22. Replace cached search with a reusable renewal interface
- **Mechanism:** Export a pair move and simulation proof as a bounded protocol with preconditions, commit and successor witnesses. Compare with keeping only live weights and solving at request time.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** APRNN plus exact synthesis and alternating simulation can implement the same semantics. The primitive claim lives or dies on amortized service with independently authored editors, not on expressivity.
- **Cheapest first test:** Replay the same blind bank against pair-only, simulation-only, the combined protocol and the strongest stacked baseline (GradMax or teleportation plus joint repair, capped recycling and exact simulation). Hold the action menu, oracle, disclosures and caching budget fixed; measure the break-even in total cost.
- **Old-task retention check:** Run a common external oracle before and after every staged renewal, simulated substitution and committed edit, checking all acquisition floors and useful targets at the same deadlines.

## Ranked deeper questions

1. **Can two individually indispensable slots be renewed repeatedly at fixed width without shedding a live obligation?** Start with 01, 12 and 13. Require a second paid return and an inductive set for any indefinite claim. If exact joint repair plus ordinary recycling already finds the same return at equal cost, or if only expiring requests work, narrow the claim accordingly.
2. **Does simulation-certified pruning save enough storage or response time to matter?** Start with 17, 18 and 22. Compare exact simulation and on-demand replanning with the same bytes, allowed moves and deadlines; report the shortest useful trace lost by any weaker pruning control. If a factored proof buys no savings or new admissions, keep the guarantee but drop the novelty claim.
3. **Which freedoms are real rather than reserved width, reset dynamics or edit-coordinate artifacts?** Cross 03, 04, 09 and 10 with frozen external tasks and canonical addressing. Establish spread in absolute utility at equal retention before comparing any chooser. A win limited to a grandfathered address or an extra idle head is not renewal.
4. **Where does renewal stop being possible as protection grows?** Use 07, 11, 14 and 15 to separate proof cost and numerical limits from incompatibility of the tasks themselves. Publish the first violated protected input or infeasible request sequence, not just average performance.

**Verdict:** Output neutrality, cancelling units and simulation are established objects. A renewable, output-exact edit interface inside a fixed-width continual learner is a conditional primitive candidate, not established by either witness. Keep it only if the same protected behavior and blind future utility are cheaper to maintain over repeated edits, or if more useful continuations survive at the same total cost, than function-preserving reuse plus the same exact planner, repair and simulation. Otherwise it is a recycling or verification improvement.
