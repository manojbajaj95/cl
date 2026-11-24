# Mergeable writes with certificates

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Finite safe regions for new-task writes](finite-safe-regions.md), [PR #152](https://github.com/manojbajaj95/cl/pull/152), cards 07 and 10. **Review seed:** [Flood triage row 245](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/flood-triage.md#L245), two score-3 ideas: offer substitutes and certify their executable subsets and orders; carry proofs across an adapter change and re-prove only what the old proof does not cover.

**Are certified, composable writes a new object for continual learning across many independent learners?** A feasible final checkpoint is not enough. The candidate object is a menu of behaviorally useful writes with a checkable contract that a later learner can use to select, order, extend, or transport its options without resubmitting the original old-task problems. If generic repair, transaction checks, and incremental verification give the same operations at the same total cost, this is a useful application, not a new object.

## What would the merge return?

- **Write menu.** A writer binds its proposal to a base snapshot, a deployed writer map, and a new-task acceptance criterion. It offers several alternative operations, plus a skip, not several doses of the same delta. Pick at most one per writer unless the contract says otherwise. Alternatives must satisfy a declared new-task floor when chosen; report actual new-task utility after composition, not just their solo scores. Once a new task is accepted and registered, its acquisition decisions join the old contract for future commits. If an advertised prefix promises to deliver a task, verify that promise and its retention in later prefixes or say explicitly that acquisition happens only at final publication.
- **Certificate.** Bind the proof to the old tasks' declared input domains, acquisition decisions, tie rule, model and arithmetic. Return a language of allowed traces over menu choices and an independent way to check its soundness. The subsets are projections of these traces: distinguish “some order works” from “every order works.” Every served prefix must satisfy every old decision, not just the endpoint. A shadow build published atomically may instead carry an explicitly endpoint-only proof; that does not authorize its component writes. Unlisted means uncertified, not impossible, unless there is an exclusion proof. Complete enumeration is useful as a small oracle, not a scalability promise.
- **Transport.** In deployed parameter coordinates, let the old and new writer maps be φ and ψ. Reuse a claim on a domain only when ψ is proved to factor there as φ composed with a map into the *certified* old domain, or when the old proof's premises are otherwise preserved. A basis rotation can move the coordinate box; equal spans are insufficient. A base change, new rivals, or changed activation cells can invalidate old premises. When ψ adds directions, inherit the old slice and re-prove residual and mixed old–new obligations on the extension; the mixed terms are not covered by checking each new axis at the origin. Even then, a transported state proof is not a transported order proof unless the deployed transitions agree on the admitted prefixes.

**Two paper checks.** Start at (0, 0) with old gap 1 − u − v. A offers u += 0.6 or 0.2; B offers v += 0.6 or 0.3. Both large choices pass solo but fail together in either order. A substitute admits both tasks if it meets its new-task floor. For old gap 1 − u + v, u += 1.25 is safe after v += 0.5, but not first: the pair has an existential order certificate, not an all-orders certificate. For transport, a two-mutable-layer path with old gap 1 − uz has a safe old slice z = 0 and a safe new axis u = 0, but fails at (2, 1). That is a required negative control, not an argument against reuse on the slice.

## Common CPU oracle and controls

Use small rational ReLU models and enumerate all menu choices and served prefixes for the exact oracle. Old A should have common and rare examples; old C should exercise a different route. Include affine slack, compensating gate changes, planted higher-order conflicts, and a contradictory target where no solution is correct. Start with finite domains; only claim regional guarantees where a verifier checks the whole region. Score exact decision agreement against acquisition separately from ground-truth old-task accuracy; also score held-out old inputs as a diagnostic, not as certified. Include ties, near-ties, and deployment rounding before any floating-point claim.

Hold new-task floors, old domains, proposal-generation budget, search, transmitted and retained bytes, and verifier work fixed or show the Pareto front. Count accepted task utility, true coverage of safe traces, proof/check cost, rounds of coordination, and bytes over a stream, not just certificate size at one merge. The stacked control is [Git-Theta](https://arxiv.org/abs/2306.04529) or a normal change log plus [APRNN](https://arxiv.org/abs/2304.03496) joint repair, [Certified Continual Learning](https://arxiv.org/abs/2407.06697)-style incremental verification where applicable, and independent rechecking of served prefixes. Give the strongest control the *same* menus and use brute force as ground truth. Also compare against serial best-choice and serial rechecking, [TIES](https://arxiv.org/abs/2306.01708)/[DARE](https://arxiv.org/abs/2311.03099) with the same verifier, shared reserve (USR1, [row 244](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/flood-triage.md#L244)), and equal-byte replay with [GEM](https://arxiv.org/abs/1706.08840) when matching learning rather than proofs.

The [idea ledger](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/idea-ledger.md) rules out activation read-pinning as a substitute for downstream checks, sparse structural rank as a safety proof, and relabeling readiness forecasts or replay deadlines as primitives. The cards below don't infer safety from any of those. “Primitive candidate” marks a proposed reusable object or operation, not a claim of priority; “improvement” marks better search, verification, or evaluation.

## Idea cards

### Menus and executable merges

#### 01. Multi-choice write, not multi-choice checkpoint
- **Mechanism:** Compile each writer's near-equivalent updates into a menu with independently verified usefulness floors. Merge into a reusable object with a proof for each accepted class of traces; let later writers consume unresolved choices before the first commit.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Task arithmetic](https://arxiv.org/abs/2212.04089) offers compositions and APRNN offers constrained repair. The proposed operation returns unresolved, independently executable choices, not a composed vector or one feasible witness.
- **Cheapest first test:** Use the two-menu paper check and add a late third learner that favors the previously unchosen substitute. Compare equal menus for serial rechecking and joint repair, also allowing atomic joint commits.
- **Old-task retention check:** Replay every advertised subset and order on A/C; score the third learner only when all served prefixes pass.

#### 02. Make compensation an explicit prerequisite
- **Mechanism:** Return “write B before A” when B introduces verified slack needed by A. Sentences in the certificate refer to choices, not writers: choosing a different A may discharge the prerequisite.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Coordination avoidance](https://arxiv.org/abs/1402.2237) already connects invariants and coordination. The possible new operation is synthesizing an executable dependency from a learned substitute's behavioral effect, not inventing ordered transactions.
- **Cheapest first test:** Plant two prerequisites with alternative routes and a cyclic dead end. Compare with the same menus and generic scheduling plus per-prefix verification; test if a third writer can consume the compiled prerequisites without that original solve.
- **Old-task retention check:** Check A/C after every legal prefix and produce the early failing prefix for a reversed order.

#### 03. Learn a menu for other writers to consume
- **Mechanism:** Spend a fixed local training budget on alternatives separated by their *certified* compatibility with a public set of write directions, rather than by parameter distance. Treat future writer menus as withheld, not as training inputs.
- **Novelty vs nearest prior art — IMPROVEMENT:** [O-LoRA](https://arxiv.org/abs/2310.14152) and [GPM](https://arxiv.org/abs/2103.09762) separate update directions. This is an alternative-generation objective, not a new protection claim or the ledger's failed readiness forecast.
- **Cheapest first test:** On a two-feature host with a redundant route, compare equal-utility random restarts, orthogonal menus and compatibility-spread menus on held-out writers at equal search cost.
- **Old-task retention check:** Compute exact A/C retention for every kept branch, with old margins matched across arms.

#### 04. Merge two already-merged groups
- **Mechanism:** Export each group's certified choices as an interface on shared deployed state; compose two interfaces only after proving the shared premises and any cross-group effects. Keep pointers to the internal traces so the result remains executable.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Git-Theta](https://arxiv.org/abs/2306.04529) provides collaborative model versioning and configurable merges. The hypothesis is that behavioral contracts, not resolved checkpoints, can serve as recursively mergeable inputs.
- **Cheapest first test:** Merge six writers in two groups, then move one client between groups. Compare fresh flat repair and cached prefix verification against hierarchical reuse; include a global rival that couples the groups.
- **Old-task retention check:** Replay all admitted interleavings on the union of A/C obligations, including the rival unseen by one group.

#### 05. A proof that some writes really commute
- **Mechanism:** Certify both transition equivalence and invariance of both intermediate states on a reachable domain, then permit swapping adjacent choices there. Keep order where either proof fails.
- **Novelty vs nearest prior art — IMPROVEMENT:** [CRDTs](https://arxiv.org/abs/1805.06358) already exploit commutativity or monotone state merges for convergence. The narrower gain is reducing the trace proof for a decision contract; convergence is not retention.
- **Cheapest first test:** Mix additive updates with state-dependent projections. Compare enumerating order classes to a generic swap reduction plus exact checks. Include equal endpoints with a bad prefix.
- **Old-task retention check:** Exhaustively compare all swaps in the oracle and explicitly reject the equal-endpoint bad prefix on A.

#### 06. Certify a range of safe fallback choices
- **Mechanism:** When one offered substitute is a small parameterized family, return a conditional set of allowed parameters for the current prefix. Bind it to both old decisions and the writer's new-task floor; keep disconnected components separate.
- **Novelty vs nearest prior art — IMPROVEMENT:** [InterContiNet](https://arxiv.org/abs/2206.07996) already protects weight regions; APRNN repairs against specs. Here the region is an interface for a particular pending choice under a prefix, not a novel region formalism.
- **Cheapest first test:** Give one writer a two-interval branch with an unsafe middle, and benchmark exact interval-valued offers against matched discrete samples plus warm-started repair.
- **Old-task retention check:** Prove the entire declared intervals for A/C and test both sides of every cut, including ties.

#### 07. Repair a menu that is one alternative short
- **Mechanism:** Return a violating old input and a constraint on the *missing substitute*, conditional on a proposed coalition. The rejected writer can synthesize a replacement locally rather than sharing all its training data or retrying arbitrary deltas.
- **Novelty vs nearest prior art — IMPROVEMENT:** [SpecRepair](https://arxiv.org/abs/2106.01917) already repairs via counterexamples. The narrower claim is that coalition-specific counterexamples save rounds of decentralized proposal revision.
- **Cheapest first test:** Plant one rare input that blocks the best three-way merge; compare joint repair, ordinary counterexample exchange, and conditional witnesses at matched information and solver budget.
- **Old-task retention check:** Verify the repaired coalition over A/C and a second rare case where satisfying the first witness merely moves the break.

### Coordination without a single shared training loop

#### 08. A certified fallback after dropout
- **Mechanism:** Return a branching trace contract: after each permitted dropout, choose a verified continuation or stop safely. Never assume that deleting an accepted write's prerequisite from an existing trace preserves it.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Federated Orthogonal Training](https://arxiv.org/abs/2309.01289) protects prior global tasks with directional restrictions. The candidate object lets a coordinator execute a different certified continuation upon missing a participant, without retracting already served prefixes.
- **Cheapest first test:** Simulate four clients with two compensation chains, dropping one before and one after selection. Compare to precomputed independent fallback and serial replanning under the same deadline and messages.
- **Old-task retention check:** Check A/C throughout every simulated dropout branch, especially the branch missing its slack provider.

#### 09. A safe fast path with selective coordination
- **Mechanism:** Allow independent local commit only for a family proved closed under the actual replica join and under served local prefixes. Route other choices to coordination for a verified common trace.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Invariant confluence](https://arxiv.org/abs/1402.2237) is the relevant existing criterion. Test whether substitute writes enlarge the uncoordinated part of the learned update workload relative to a static reserve.
- **Cheapest first test:** Enumerate two replicas and three writes with a rare cross-replica conflict. Compare full coordination, invariant-confluence checks with fixed writes, and shared slack reserve given equal menus.
- **Old-task retention check:** Verify every local prefix and reachable join on A/C; require that a locally safe pair with an unsafe join is never exported on the fast path.

#### 10. Rebase a stale write by its preconditions
- **Mechanism:** Package a write with a proved envelope of starting states and a dependency on which old contract versions it covers. A later replica may rebase by proving inclusion and any newly added obligations rather than retraining the update.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Git-Theta](https://arxiv.org/abs/2306.04529) has a model change representation, and [Certified Continual Learning](https://arxiv.org/abs/2407.06697) reuses verification across retraining. The candidate operation rebases an *unapplied* write and exports the remaining valid choices.
- **Cheapest first test:** Let a delayed learner return after three commits, one leaving the envelope while retaining old behavior. Compare a clean rebase, stale-envelope checks, and ordinary rebase plus incremental verification.
- **Old-task retention check:** Check A/C and any task acquired during delay; a proof covering only the older versions cannot admit a write that flips the newer task.

#### 11. A certificate owned by multiple task custodians
- **Mechanism:** Each custodian proves its own contract over a common, frozen candidate trace language. Intersect the *proved* trace languages, not their individual state summaries; shared version identifiers prevent proofs referring to different paths from being combined.
- **Novelty vs nearest prior art — IMPROVEMENT:** [TARGET](https://arxiv.org/abs/2303.06937) addresses exemplar-free federated CL via distillation. Distributed conjunction is not new and this is not a privacy guarantee; test whether it avoids centralizing old inputs at competitive cost.
- **Cheapest first test:** Give three custodians disjoint panels and incompatible local preferences; compare central replay, federated distillation, and distributed per-trace checking at equal disclosure and byte budgets where possible.
- **Old-task retention check:** Use a separate exhaustive oracle for all panels; ensure that one custodian's timeout causes abstention, not approval.

#### 12. Test whether a late learner can tell two merges apart
- **Mechanism:** Ask a new writer to distinguish two contracts that have the same deployed checkpoint but differ in admissible continuations, with all pending options and registrations counted as state. Require a short trace that proves the difference.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's card 13 and row 245 already place future-language equivalence under the Nerode quotient idea. This is a falsifier for model-only summaries, not a new quotient or an argument about two identical full states.
- **Cheapest first test:** Compare full logs, equal-byte checkpoint-plus-pending-menu summaries, and a certificate on a pair with different remaining prerequisites. Drop the idea if the small explicit summary serves the same queries.
- **Old-task retention check:** Check every separating prefix on both A/C contracts; a difference in current accuracy is not an admissible witness.

### Transport when the writer changes

#### 13. Transport by exact factorization
- **Mechanism:** Export a map from the new chart into the old certified region, including domain and arithmetic checks. Carry the existing derivation as a referenced proof; transport transitions only when they are shown to agree at each reachable state.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Weight-space equivariance](https://arxiv.org/abs/2301.12780) treats transformations of deployed networks; ordinary substitution already transports properties. Measure proof reuse rather than claiming rotation or positive ReLU rescaling as new.
- **Cheapest first test:** Rotate a bounded adapter domain and positively rescale a hidden unit with compensating outgoing weights. Compare cached substitution with fresh and warm-started exact solves; include a new box not contained in the old domain.
- **Old-task retention check:** Check A/C at transformed boundaries and disallow points in the new box whose pullback falls outside the proved region.

#### 14. Prove the mixed remainder on adapter expansion
- **Mechanism:** Split a new adapter into a certified old slice and residual coordinates. For each old decision bound the loss of margin over the new fiber uniformly in the old slice, including mixed terms and changed gates; split or abstain when the bound is loose.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Interval bound propagation](https://arxiv.org/abs/1810.12715) can bound variation; [Certified Continual Learning](https://arxiv.org/abs/2407.06697) already reuses certificates. The candidate is a composable lift of pending write contracts to an expanded writer, not merely cheap revalidation of one network.
- **Cheapest first test:** Add a direction to the old toy, first independently affine, then with gap 1 − uz and a gate crossing. Compare mixed bounds against a full solve and incremental verification given the same old proof.
- **Old-task retention check:** Check every A/C obligation over old slices and new fibers; axis-only acceptance of the unsafe corner falsifies the transport.

#### 15. Keep certificates for unaffected proof premises
- **Mechanism:** Label each proof node with the premises it actually uses, such as rival set, downstream weight bounds, and activation signs. An adapter migration invalidates dependent nodes, not entire tasks; re-prove them before issuing a new certificate.
- **Novelty vs nearest prior art — IMPROVEMENT:** Proof reuse, [neural proof minimization](https://arxiv.org/abs/2511.08198), and the parent's proof-indexed cells are prior art. Test whether indexing old obligations by changed premises reduces proof cost after charging for dependency extraction.
- **Cheapest first test:** Add a direction that changes gates in just one of two old cells, then change a downstream weight that affects both. Compare fresh proof, incremental verification, and explicit premise invalidation.
- **Old-task retention check:** Recheck A/C at all changed cells and cached unchanged cells; force failure of one omitted downstream premise.

#### 16. Shrink rank without promising impossible alternatives
- **Mechanism:** In a lower-rank chart, keep old trace branches only if each required transition can still be realized or replaced by a proved behavioral substitute. Return unrealizable choices separately from not-yet-proved ones when evidence supports the distinction.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [O-LoRA](https://arxiv.org/abs/2310.14152) separates task subspaces. The proposed operation restricts a live language of pending writes under a representational bottleneck, not the training rule for low-rank updates.
- **Cheapest first test:** Collapse a two-axis adapter onto a line: preserve one exact branch, salvage one with a different delta, and plant one impossible task floor. Compare retraining the menu and full recertification.
- **Old-task retention check:** Verify A/C under each surviving branch, including intermediate states of the replacement transition.

#### 17. Adapter swap as a commuting transition check
- **Mechanism:** Compare “commit the pending write, then migrate” with “migrate, then apply the translated write.” Prove both sequences safe and their resulting states equivalent for the *declared future write family* before allowing either execution order.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Weight-space equivariance](https://arxiv.org/abs/2301.12780) handles symmetries and [Git-Theta](https://arxiv.org/abs/2306.04529) handles model merging. The proposal is a checkable reorder operation for a migration interleaved with learning; equality on a current panel does not justify it.
- **Cheapest first test:** Combine one exact rotation, one rank expansion, and one state-dependent clip; find a case where safe endpoints disagree after the next write. Compare global restart and per-prefix incremental verification.
- **Old-task retention check:** Check A/C at both orders' prefixes and on a separating continuation; include a new task registered between the operations.

#### 18. Refuse transport across a moved consumer
- **Mechanism:** Carry an explicit downstream obligation for changes that cross layers: verify the new composed consumer on the old certified input cells and permitted writer effects. Equality of insertion activations alone is neither required nor sufficient.
- **Novelty vs nearest prior art — IMPROVEMENT:** The ledger's PR #117 killed read-pinning; its survivor is [Jacobian matching](https://arxiv.org/abs/1803.00443) along registered directions. The proposal here is an exact rejection or proof mechanism for finite deployed transitions, not a new distillation objective.
- **Cheapest first test:** Swap in a consumer with identical output and Jacobian at one anchor but a nearby changed ReLU gate. Compare read-pinning, Jacobian matching plus the same checker, and explicit cell proofs.
- **Old-task retention check:** Check A/C after each migrated write, especially a rare example through the changed gate; no certificate based only on the anchor may pass.

### Tests that can kill the object

#### 19. A coalition that defeats all pairwise certificates
- **Mechanism:** Compare a complete trace proof with bounded-order summaries that must abstain on uncovered combinations. Admit larger groups only when a verified structural argument, not small-pair success, covers them.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's shared coalitions and [Reluplex](https://arxiv.org/abs/1702.01135) already motivate logical encodings. This is an information and verification cost test, not the ledger's killed sparsity certificate.
- **Cheapest first test:** Construct equal singleton and pair outcomes with different triple outcomes. Add a structured low-interaction control and measure certificate size and abstention against exact enumeration.
- **Old-task retention check:** Exhaustively check all triples on A/C, including one rare-only failure and a triple that passes only in one order.

#### 20. Measure the cumulative cost across repeated merges and migrations
- **Mechanism:** Charge for proof production, checking, invalidation, retention data, and proposal generation over many merges and two adapter changes; measure when a retained certificate pays back versus rebuilding.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Certified Continual Learning](https://arxiv.org/abs/2407.06697) already makes incremental proof amortization a baseline. This measures reuse across menu queries and adapter changes, not a new verification algorithm.
- **Cheapest first test:** Stream 12 tiny tasks in four cohorts, once with stable disjoint contracts and once with a shared changing gate. Stack menu-aware APRNN, incremental checks and replay at matched budgets; require a win beyond the favorable sparse case or narrow the scope.
- **Old-task retention check:** Check A/C and all registered later tasks after every served prefix, even on cache-hit commits.

#### 21. Check whether the proof helps when the next merger is unknown
- **Mechanism:** Split the experiment across independent learning sites: train menus without knowledge of the final partner, exchange only the same budget of proposals and proof data, and ask a second coordinator to select a valid merge after the first coordinator changes the adapter.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Federated CL under resource constraints](https://arxiv.org/abs/2501.08737) already tests resource tradeoffs. The distinguishing claim is that the same checkable artifact supports both a new coordinator's compositional query and a verified migration.
- **Cheapest first test:** Cross six writers into held-out groups, rotating and expanding the adapter after the first merge. Compare the best menu-aware serial, federated orthogonal, and joint approaches with full incremental recertification. Charge communication and proof work.
- **Old-task retention check:** Audit every site’s declared A/C and newly registered tasks at every allowed prefix; also report held-out accuracy and worst-client acquisition separately.

#### 22. Publish impossibility and abstention separately
- **Mechanism:** Distinguish “no trace satisfies the old and new contracts with these menus” (requires a proof), “zero legal choices in this export,” and “solver unknown.” Ask whether an inexpensive refusal can guide writers without claiming that CL itself is impossible.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Optimal continual learning](https://arxiv.org/abs/2006.05188) already gives hardness and memory limits, and provable repair can report unsatisfiability. A menu-scoped refusal is an accounting and coordination aid.
- **Cheapest first test:** Mix contradictory targets, inadequate menus with a known solution outside them, and hard but feasible menus under a capped solve. Compare exact unsatisfiability, ordinary timeout handling, and useful counterexamples at matched cost.
- **Old-task retention check:** No refusal may silently revise the old A/C contract; exhaustively check each later accepted repair and independently verify each claimed impossibility on the toy domain.

## Ranked deeper questions

1. **Does the merge return an object a later independent learner can actually use?** Run 01 → 04 → 21 with the *same* late choices and old obligations delivered to the stacked control. Require more retained new-task utility, more genuinely usable safe traces, or less coordination or verification cost at matched budgets, with zero false accepts. If a log plus joint repair and incremental replay of prefixes ties, call this certified constrained learning, not a new primitive.
2. **When does adapter transport save more than it costs?** Run 13 → 14 → 17 across an exact change of chart, added directions with mixed effects, and a changed consumer. Can a transported certificate plus the newly proved obligations certify later writes more cheaply than fresh or warm-started verification? If the win exists only for a rotation, keep it as a verification improvement.
3. **What is the minimum coordination required to keep useful writes?** Compare existential order guarantees, all-orders closure, and certified dropout continuations in 02/08/09 as the number of independent learners and the rate of coupled decisions rise. Does a menu remove coordination that static escrow and an ordinary scheduler cannot remove at the same utility?
4. **Where does a proof become as expensive as the history it replaces?** Use 19/20/22 to separate a structured regime where trace proofs are reusable from dense higher-order interactions where storing and replaying the obligations wins. Measure abstention and genuinely impossible merges separately; small certificates that mostly say “unknown” do not establish scalability.
