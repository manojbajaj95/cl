# Shared-coverage bounds: count one truthful example once

**Status:** Ideas only; no implementation, experiments, or GPU work. **Parent:** [Obstruction-carrying bundles](obstruction-bundles.md) ([PR #194](https://github.com/manojbajaj95/cl/pull/194)). **Review seeds:** [Flood triage, row 300](https://github.com/manojbajaj95/cl/blob/ce445e562b40e76b1d4679a187c50281d24f294e/reviews/flood-triage.md#L300) kept parent **#07** (prove joint discharge before combining two skill demands) and **#03** (realize abstract obstructions in the target without source histories) at score 3. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/ce445e562b40e76b1d4679a187c50281d24f294e/reviews/idea-ledger.md).

## What would count as a new object?

**Not multi-task example selection or a translated proof log.** [Iterative Machine Teaching](https://proceedings.mlr.press/v70/liu17b.html) and [Nonparametric Teaching for Multiple Learners](https://arxiv.org/abs/2311.10318) already select lessons for learner dynamics; [GCR](https://arxiv.org/abs/2111.11210) already selects replay coresets. [Additive pattern databases](https://arxiv.org/abs/1107.0050) already partition action costs to avoid double counting, and [CEGAR](https://doi.org/10.1007/10722167_15) already distinguishes spurious abstract traces from concrete executions. The bet is a **portable lower-bound certificate** whose shared-example accounting and counter-history obligations can be checked under a changed learner without access to the source histories. Neither a weighted coverage inequality nor concretizing an abstract trace is new by itself.

### Prove coverage, then count

Freeze the truthful pool (including what constitutes *one* presentation), order and repeat rules, update law, hidden-history envelope and free transcript, reply menu, and old A/C and new-utility floors. A winning pair is one lawful ordered sequence and one lawful reply that meet all floors, including retention at every live prefix, for every compatible history. Coverage here is **discharge of a necessary pre-reply obligation**, not task accuracy, gradient similarity, or the number of examples that name a skill.

- **One charge, two skills.** For a fixed reply or a proved class of replies, give a two-component potential `z`, with `z=0` at the start, such that winning implies `z_A ≥ d_A` and `z_C ≥ d_C` just before the reply. This can be on a pair of legal same-transcript histories, one for each obstruction; both traces must follow the **same** example sequence. If `λ≥0` and every lawful presentation at every relevant reachable prefix satisfies `λ·(z_next−z)≤c`, telescoping gives `k ≥ ceil((λ·d)/c)` for `c>0`. A positive demand with `c=0` proves impossibility for that class. Keep negative increments; reloads and preparation are not free. If different replies have different demands, take the weakest proved bound over all lawful reply cases, including a no-op where legal; an uncovered case yields no positive bound from this argument. If a source proof only covers a restricted budget horizon, claim nothing beyond the checked horizon.
- **Abstract obligation → concrete target history.** Index the shorter sequence/reply domain by proof cases. Export each case's guard and a target instantiation rule: a checked path from a legal target initial history through the target's own transitions to the declared free transcript, plus the failure proof obtained when the candidate pair is applied there. For a resource bound used instead of explicit failure enumeration, map the demand witnesses and separately prove the target's increment cap over all relevant reachable prefixes. Several obligations may share one target witness, but if a case claims one witness defeats a whole block, prove that universally; if it uses a witness recipe dependent on the pair, prove the recipe is defined for every covered pair. Never substitute an abstract state satisfying a guard for a reachable history. Alternative histories need not have occurred; they must all remain possible in the same declared information set. No export of the source histories or access to the realized deployment history is needed.
- **Independent proof status.** A new example can break the cap; a new reply can escape the demand; a removed history can erase a failure edge. Report each missing premise and fall back to whatever lower bound is still proved (or unknown), not an asserted change in the optimum. Certify the winning bundle separately. An obstruction is not permission to deploy a lesson.

**Blind comparison.** Freeze the certificate and instantiation rules before seeing held-out editor families. Compare to exact joint enumeration (offline truth), a cost-partitioned planner, cached concrete counterexamples where shareable, ordinary reachability checking and CEGAR, and a stack of the best cost partitioner plus generic target proof reuse. Include naive summation as a deliberately unsound negative control. Charge artifact bytes, source construction, target proof construction and verification, failed imports and fallback; hold public reads, truthful pool, lawful reply work and service fixed. Check ordinary old A/C tasks and their worst slices independently of the obligation/probe at each live prefix and after subsequent edits. Do not revive ledger-falsified functional syndromes (a bound on obligations is not a retention sketch), plasticity reserve (no Gramian-based choice), or effect-class distillation (no assumption that a common output class preserves the update). A tie with cached search and re-verification is not a primitive.

### Two paper fixtures, not pilot results

**A single joint step changes the lower bound.** On each old skill `i∈{A,C}`, start at `(p_i,q_i)=(0,0)`. The only reply leaves these coordinates untouched and introduces a write that damages the skill's vulnerable slice unless `q_i=1`; before the reply the old slice passes for either value of `q_i`. One truthful example sets the auxiliary gate `p_i=1`; a second sets `q_i=1` only if the gate is open. Implement each setting by a unit step on half-squared error with target `1`, masked to the named coordinate; the gated prediction is `p_i q_i` with `p_i` frozen on the second step. Thus `z_i=p_i+q_i` needs two units, and disjoint examples give `Δ(z_A+z_C)≤1`, hence four presentations, attained by the two ordered pairs. Now allow one same-cost, genuinely two-output truthful example setting both gates (one offered input with two observed targets, not two records renamed a batch). Its increment is at most `2`, so a uniform cap gives only two; prove the shared step can give two units **at most once** (repeats are idempotent) and all others give at most one. Then `4≤k+1`, giving three, attained by the shared gate example followed by the two gated examples. Naive addition falsely gives four. A joint example that instead moves an independent rare C slice below its floor is not an upper-bound witness, even though its coverage is unchanged.

**A matching shape is not a target history.** Let a target's public start be `(p,q)=(0,0)` and its hidden lane be `L` or `R`, with an identical free transcript in both. In the source both hidden lane choices are made by lawful prior edits; the mapping emits the target's own prior edit plus a proof that it initializes the named lane and reaches the transcript, even if gate coordinates or private outputs are renamed. Each lane has a specialist reply that works without teaching on that lane but fails on the other; a balanced reply needs the gated update. A target allowing both prior edits can reuse both specialist obstructions without any source states. In a target that blocks the `R` transition, a shape-compatible “`R` state” still exists in the abstract product, but the rule cannot prove its path. The left specialist then works at length zero if `L` is the sole compatible lane. Independently check its A/C margins; the right-looking state cannot be used to reject it.

## Idea cards

**P** = candidate primitive, conditional on beating the stacked control; **I** = improvement or falsification test. All first tests below are proposed paper or tiny CPU checks, not results.

### Prove the shared charge

#### 01. A two-skill exchange certificate (P)
- **Mechanism:** Export two necessary demands and a checkable envelope of per-presentation paired increments, indexed by lawful reply class.
- **Novelty vs nearest prior art:** Operator cost partitioning already bounds an additive heuristic; the candidate is a reusable exchange certificate over both teaching and reply contracts.
- **Cheapest first test:** Enumerate the disjoint/gate-sharing fixture and swap in an untruthful two-output token; compare bounds to exact search, planner and naive sum, rejecting the token before pricing it.
- **Old-task retention check:** Re-run ordinary A/C after every prefix and the reply, including the third slice damaged only by the shared write.

#### 02. Assemble a bound from multiple supporting directions (I)
- **Mechanism:** Choose a nonnegative supporting direction for each reply's demand; preserve the underlying vector frontier so a target can change demand without guessing a new cap.
- **Novelty vs nearest prior art:** Support functions and LP duality already do this; it is a tightness improvement over a single equal-weight count.
- **Cheapest first test:** With increments `(2,0)` or `(0,1)` and demand `(2,2)`, compare equal weights to `(1/2,1)` and exact enumeration; then reverse the range of asymmetry.
- **Old-task retention check:** Compare actual winners at the same per-skill and rare-slice floors; a better bound cannot trade A off against C through `λ`.

#### 03. Treat shared discharge as a consumable entitlement (P)
- **Mechanism:** Store a second invariant counting how many high-overlap transitions can still occur, rather than charging the worst overlap on every step.
- **Novelty vs nearest prior art:** Resource-constrained planning already counts consumables; the bet is a locally transportable bound on the supply of lawful joint examples.
- **Cheapest first test:** Use the idempotent gate fixture, then add a gate reset; check whether the proof pays for the reset or loses its cap, against augmented-state exact planning.
- **Old-task retention check:** Audit A/C after the reset itself, not just after the re-earned shared credit.

#### 04. Charge the gate opener for what happens later (P)
- **Mechanism:** Verify Bellman inequalities on a signed progress potential with gate readiness as a coordinate; disallow simultaneous credit for both readiness and the same later discharge unless the inequalities support it.
- **Novelty vs nearest prior art:** Amortized potential methods and planning potentials already charge delayed work; test whether the readiness predicates port between update laws without refitting.
- **Cheapest first test:** Compare fixed partitioning to a potential on the two legal orders of a gate and regression step; switch the target to a one-step lag and require the old inequality to fail if applicable.
- **Old-task retention check:** Check both skills and the gate-sensitive old slice at the transient open state and after the reply.

#### 05. Keep the witness histories coupled by the curriculum (P)
- **Mechanism:** Form a reachable product of the A and C counterfactuals under shared presentation IDs; exclude combinations of prefixes that require different sequences.
- **Novelty vs nearest prior art:** Self-composition and relational verification already check paired executions; the bet is an exportable paired-skill charge that survives changes to each marginal learner.
- **Cheapest first test:** Make one order high-discharge in A and its reverse high-discharge in C; compare synchronized reachability to a Cartesian marginal envelope and generic relational checking.
- **Old-task retention check:** Check A and C on both traces; omit neither skill just because that trace was chosen to witness the other one.

#### 06. Separate a repeated example from a different atom (I)
- **Mechanism:** Make the granularity of a truthful presentation part of the bound; publish different counts for single records and a declared batched interface.
- **Novelty vs nearest prior art:** Weighted action costs already capture batching. This is an audit against inventing overlap by repricing examples.
- **Cheapest first test:** Present two independent labels as a concatenated record, independently as two records, and as a true joint sensor outcome; admit only what each frozen interface prices.
- **Old-task retention check:** Compare prefix retention in the sequential and batched arms, including a loss normalization change that affects C but not final A.

#### 07. Give different replies different deficits (I)
- **Mechanism:** Prove pre-reply demands separately for balanced, left-only, right-only and no-op replies, or exclude a reply using a reachable failure witness; take the minimum only after checking the entire menu.
- **Novelty vs nearest prior art:** Disjunctive bounds and contingent planning already split action cases. The audit prevents a bound for the favored reply from masquerading as shortestness.
- **Cheapest first test:** Add a lawful cheap specialist repair with a lower C demand; require the combined bound to weaken unless a verified history still blocks it.
- **Old-task retention check:** Keep the new-utility threshold fixed while checking margins on both old skills for the specialist and the balanced reply.

#### 08. Use a count lattice, not just average coverage (I)
- **Mechanism:** Track which integral increment sums can occur at a given budget; success requires intersecting the upward-closed demand set, not just its fractional relaxation.
- **Novelty vs nearest prior art:** Integer covering bounds already close LP gaps; use this to mark what generic integer search explains.
- **Cheapest first test:** With three independent deficits across two skills, plant truthful examples whose coverage pairs are `{A₁,A₂}`, `{A₁,C}`, `{A₂,C}` and compare fractional and integer optima at matched costs.
- **Old-task retention check:** Validate all three deficits on independent old slices and verify any integer winner on ordinary A/C.

### Realize obligations without the source history

#### 09. Export a witness map, not the witnesses (P)
- **Mechanism:** Publish `obligation → target trace recipe + reachability + transcript + failure proof`; targets instantiate concrete counterfactuals using only their public interface and a checker.
- **Novelty vs nearest prior art:** CEGAR concretizes traces, and proof caches remember local failures. The candidate is an obligation-keyed interface that resolves on unseen target parameterizations without a fresh witness search.
- **Cheapest first test:** Rename and rescale gate coordinates, change private outputs, and block the `R` edit in one import; compare against cached traces, generic checking and CEGAR with the same evidence.
- **Old-task retention check:** Re-evaluate the exact target A/C failures and the independent winning trace; include a renamed target whose old C margin changed despite unchanged A.

#### 10. Reuse a recipe whose index is the attacked pair (P)
- **Mechanism:** Map an entire short-pair block to a constructive function returning a checked target path for each pair; prove totality rather than assuming one path covers the block.
- **Novelty vs nearest prior art:** Strategy certificates and Skolem functions already encode choices; the bet is a portable obstruction witness generator with proof cost below re-solving the teaching game.
- **Cheapest first test:** Allow four specialist replies with different blind lanes; compare one verified recipe to four cached paths, then add a fifth reply outside its domain.
- **Old-task retention check:** Make one path fail only on an old rare C slice and check that a working longer bundle still passes that slice.

#### 11. Allow reachable replacements that fail for a different reason (P)
- **Mechanism:** Specify the obligation as defeating a short pair under the frozen service contract; permit the target to prove A failure where the source proved C failure unless the case specifically requires a C deficit.
- **Novelty vs nearest prior art:** Proof repair can change lemmas; the bet is weakening the witness interface to the exact failure edges needed so more target editors qualify, without weakening the old-task contract.
- **Cheapest first test:** Swap the damaged skill for one obstruction, including a negative arm where the switched failure is a harmless surrogate-loss increase; compare generic repair.
- **Old-task retention check:** Adjudicate both named floors and new utility independently; verify that the winning reply's A/C margins are not relaxed by the replacement.

#### 12. Split trace legality from the failure replay (P)
- **Mechanism:** Use separate proof dependencies for admission to the target information set and for failure under hypothetical lessons; invalidate only the affected obligation edges.
- **Novelty vs nearest prior art:** Assume–guarantee verification and proof dependency graphs already split checks. The bet is that the two proofs change on different editor updates often enough to pay for the portable split.
- **Cheapest first test:** Modify only the prior-edit transition in one target and only the post-lesson reply in another; compare invalidation and checking cost to incremental verification.
- **Old-task retention check:** Run A/C after the revised prior edits as well as after reply; unchanged prior legality does not certify unchanged retention.

#### 13. Witness the same information set, not just two legal histories (I)
- **Mechanism:** Bind each recipe to the deployment's free transcript at the decision deadline, including the public reply offer if it varies.
- **Novelty vs nearest prior art:** Observation equivalence is standard in imperfect-information games. This is the null for a “shared” proof pooling incompatible decisions.
- **Cheapest first test:** Add a free bit distinguishing lanes before the choice in one arm and after it in another; exact transcript-aware search should drop the obstruction only in the first arm.
- **Old-task retention check:** Keep floors fixed and check each specialist on A/C under its own transcript; don't count a wrongly routed reply as an inherent skill conflict.

#### 14. Prove short-pair coverage under target grammar expansion (P)
- **Mechanism:** Project target short pairs onto source proof cases only when a prefix- and cost-aware translation preserves failure; otherwise emit explicit uncovered cases.
- **Novelty vs nearest prior art:** Simulation of transition systems and grammar inclusion are standard; test the extra reuse from a failure-preserving curriculum projection across truthful pool changes.
- **Cheapest first test:** Add a target alias whose first update matches an old example but whose second occurrence escapes the obstruction; compare checker to ordinary simulation and CEGAR.
- **Old-task retention check:** Check failure at the corresponding live prefix in target A/C, not only equivalence of the end state or newly taught output.

#### 15. Bound disclosure separately from reachability (I)
- **Mechanism:** Keep target trace values with a local checker, exporting the mapped obligation and the checked outcome; require the same evidence format on every comparison arm and make no secrecy claim about the recipe itself.
- **Novelty vs nearest prior art:** Local proof checking and proof-carrying data already separate witness data from assertions; this audits whether the alleged portability just sends a source replay by another name.
- **Cheapest first test:** Forbid serialization of source state and trajectories, vary target-private outputs, and compare a local symbolic witness checker to a generic verifier with the same public inputs.
- **Old-task retention check:** Give the checker independent old-task expectations, including a private C slice whose regression is invisible in the public transcript.

### Find the boundary between portability and recomputation

#### 16. Check the shared cap on a different representation than the demand (P)
- **Mechanism:** Realize necessary demands with reachable concrete alternatives, but certify the cap on an overapproximation of the synchronized presentation transitions. Do not use abstract reachability alone to certify a witness.
- **Novelty vs nearest prior art:** May/must abstractions already distinguish proof directions. The bet is independent reuse of the charge and demand proofs across changes that affect only one direction.
- **Cheapest first test:** Add a spurious abstract high-credit transition (safe but weak bound) and a spurious abstract counter-history (unsound if admitted); compare directional refinement to an off-the-shelf abstraction engine.
- **Old-task retention check:** Verify demand failures and winner floors concretely; a pessimistic charge summary may weaken the bound but never count as old-skill failure.

#### 17. Carry an obstruction through a bounded update-law drift (P)
- **Mechanism:** Publish checked per-transition cap slack and minimum violation slack for realized witnesses; rederive the bound with target slack only where legality still holds and failures stay strict.
- **Novelty vs nearest prior art:** Robust reachability and interval certificates already bound perturbations; test whether separately reusable slack on the charge and witness sides saves work over their stack.
- **Cheapest first test:** Perturb a gate threshold across two breakpoints, one changing overlap and one making the witness unreachable; compare to interval checking with fresh search.
- **Old-task retention check:** Check exact target path margins around both breakpoints and match initial A/C headroom in comparisons.

#### 18. Search for a small refutation of the certificate (I)
- **Mechanism:** Audit the two directions independently: find one reachable over-cap presentation or one legal shorter winning pair that evades the mapped witness cover.
- **Novelty vs nearest prior art:** Differential model checking and adversarial testing already search for counterexamples; this prices which certificate field breaks first.
- **Cheapest first test:** Plant separately a high-discharge repeat and an uncovered shorter reply; let exact enumeration identify each and compare repair effort against a generic verifier.
- **Old-task retention check:** Verify that the shorter pair truly passes ordinary and rare A/C cases at every live stage before calling it a refutation.

#### 19. Grade each certified budget independently (I)
- **Mechanism:** Store an obligation cover per budget tier; on failed witness import, salvage only tiers whose cases are still discharged.
- **Novelty vs nearest prior art:** Incremental SAT and anytime branch-and-bound already report partial bounds; compare their reuse before crediting the specialized encoding.
- **Cheapest first test:** Remove the sole mapped witness for a length-two pair on import; test that the checker still excludes all pairs of length at most one but no longer excludes all length-two pairs.
- **Old-task retention check:** Recheck the old tasks for any retained incumbent; a salvaged lower tier confers no serving permission.

#### 20. Compose with a safety guard but not with a hidden oracle (P)
- **Mechanism:** At each live prefix, refine charge bounds using only legally public offers or a precommitted invariant; never prune a dangerous prefix just because the realized hidden world would not choose it.
- **Novelty vs nearest prior art:** Conformant planning already enforces nonanticipation. The proposed reusable object is a joint charge certificate whose guards align with actual decision deadlines.
- **Cheapest first test:** Put a high-overlap example behind a public gate, then delay reveal of the gate by one step; compare to conformant planning and a priced hidden-state oracle.
- **Old-task retention check:** Check A/C on every still-compatible branch before the reveal, including a branch made unsafe by an early shared presentation.

#### 21. Carry a proof that no single charge can be shared (P)
- **Mechanism:** Certify disjoint progress using target-local invariants rather than distance between examples; explicitly enumerate which lawful transition would break disjointness if added.
- **Novelty vs nearest prior art:** Additive abstractions already exploit disjoint operators; the bet is a certificate that validates disjointness across editor families with differing parameter ownership.
- **Cheapest first test:** Let two gates occupy different parameters but share a projection in one target; compare structural disjointness, exact transitions and a cost-partitioned planner.
- **Old-task retention check:** Verify old behavior on the shared projection as well as the nominal separate skills; independent coordinates need not mean independent old tasks.

#### 22. Run the compile-away tournament (I)
- **Mechanism:** Hold the teaching and reply interface fixed and benchmark reuse of the combined certificate against separately cached costs and generic proof obligations, with no hidden source recall.
- **Novelty vs nearest prior art:** This is a falsifier, not a new algorithm: if cost partitioning plus ordinary CEGAR/cache gives equal bound, evidence and total cost, the two mechanisms already exist in adequate form.
- **Cheapest first test:** Blindly rename one family, add overlap to another and remove a witness in a third. Count proof size, checks, search and fallbacks at equal bound quality; report failed imports too.
- **Old-task retention check:** Use the same independently verified serving bundles and A/C floors in all arms; fewer admitted imports cannot masquerade as safer learning.

## Ranked deeper questions

1. **Can a frozen joint-discharge/witness-map certificate match exact bound quality on blind targets for less total work than cost partitioning plus generic proof reuse?** Start with disjoint and shared gates, a renamed learner, and a shape-compatible but unreachable counter-history; include failed imports in the break-even calculation.
2. **How much of the bound needs synchronized history rather than two marginal demands?** Construct paired worlds with identical marginal increment envelopes but different attainable joint increments under the same truthful sequence; compare relational checking to the best factored potential.
3. **When does a source-free witness map require target work comparable to solving the original teaching problem?** Scale the number of short-pair classes and the symmetry of the target's prior-edit grammar; distinguish an increasing number of obligations from irreducible target search per obligation.
4. **Which changes should invalidate the two proofs independently, and which force a joint redo?** Cross newly legal examples and replies with removed or replacement histories; measure the largest still-checked budget while holding ordinary A/C retention and new service fixed.

**Verdict:** Keep both reviewer seeds conditional. Combine skill demands only after proving a joint charge, and transport obstructions only when target-local reachability and failure proofs cover the relevant shorter pairs. Treat the combination as a new primitive only if blind reuse beats the stacked planner and proof cache at matched bound quality, service, and old-task retention.
