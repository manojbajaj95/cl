# Forgetting as unregistered dependence

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Learned invalidation](learned-invalidation.md), [PR #148](https://github.com/manojbajaj95/cl/pull/148), card 15. **Review seed:** [flood-triage row 239](https://github.com/manojbajaj95/cl/blob/dfb4d52e8e2ef4938bc1e578baa9a04c8d98cad5/reviews/flood-triage.md#L239), score 3: protect the old task's reads, not its whole activation span.

## What the hypothesis claims

The parent asks what should change after a fact is revised. Here the new task B is allowed to learn, but not to accidentally change what an old task A still owes. A bridge rule might read a weight limit, the existence of an exemption, and an upstream selector that decides which jurisdiction applies. A's activations also carry road colour and hundreds of other signals. Protecting just the true reads might leave B more room than protecting the activation span. But freezing the limit alone does nothing if B changes which limit A looks up, changes how A compares it, or adds a new path to A's output.

Keep three maps separate: **spec reads** (what the world says A should depend on), **model reads** (what the current predictor actually uses, including shortcuts and negative lookups), and **write effects** (what a permitted finite update can change, including gates, consumers and shared state). A sparse spec graph is not evidence of a sparse protectable model cut. Under an otherwise valid contract, an unregistered-dependence failure is an observed A regression attributable to a missed read or write effect. A registered read that was not actually preserved is an enforcement failure. An authorized fact revision is not forgetting; score changed truths separately from accidental changes.

**What would constitute a proof?** Fix protected inputs or histories, an observable (exact output, action, margin, or declared distance), baseline version, allowed writers, and shared state. For a deterministic graph, suppose every route from mutable state to the observable passes through a registered interface and all its non-interface inputs and downstream semantics are held fixed. If the actual write preserves that interface on the protected domain, the output is unchanged, by substitution. The cut must cover every reachable branch, including control and absence reads, plus any added path; pinning an activation while its consumer can change is not that proof. For stochastic policies the analogous contract must preserve a sufficiently specified conditional distribution, not just cached sampled actions. A Jacobian projection at one point is local evidence, not a finite-write or history guarantee; even the scalar product uv changes from 0 to 1 under (0,0) → (1,1), although its first derivative at the start is zero.

**Why it might be cheaper, and why it might not.** If an old linear readout depends only on the first output of a dense layer, its remaining outputs may be free to move even when old inputs span the full input space. Conversely, on a linear writer family with old output map M, any linear projection safe for *every* permitted update must send updates into ker(M), so it needs at least rank(M) independent constraints. A short list of readable feature names can still induce high rank. Count total bytes, number of independent constraints on actual writers, and intervention/verification cost, not just graph edges.

## Common CPU test and controls

- **Shared world:** Two-layer conditional predictor on the parent's tiny toll world (plus an exactly enumerable version). A handles ordinary and rare/exemption routes; B learns a new region or rewrites nuisance features; C handles unrelated old routes. Cross nuisance width, true read count, hidden shortcut, routing drift, update horizon and task overlap independently. Include sparse cut, dense model reads despite sparse spec, and identical-input contradictory targets without a task cue as positive, hard and impossible regimes. Give oracle spec, model cut and write effects separately; never credit their discovery as free.
- **Common arms:** Unconstrained SGD, tuned [GPM](https://arxiv.org/abs/2103.09762), [OGD](https://arxiv.org/abs/1910.07104), [EWC](https://arxiv.org/abs/1612.00796), rehearsal, random rank-/byte-matched read sets, the exact explicit reader with frozen interpreter, and oracle model-read protection. GPM protects a retained activation basis; OGD already protects sampled output sensitivities, so merely finding a lower-rank Jacobian is not the claim. Add sensitivity-budgeted [SPACE-LoRA](https://arxiv.org/abs/2609.34453) where B adds residuals, [DUET](https://arxiv.org/abs/2611.29269) for post-write projection, and [CABA](https://arxiv.org/abs/2610.40740) for post-write acceptance. Match wrapper, parameter budget, side information and intervention compute; give replay whatever storage the proposed registry uses. No task ID at inference unless every arm gets it.
- **Decision rule:** Plot A/C retention against *matched attained* B progress (tune all arms), with an equal-cost comparison at fixed retention as a second view. Count registry, witnesses, fallback copies, discovery/audit work, serving overhead, rejected writes and residual/correction writes. Score both first break and worst prefix on an independent old holdout; split ordinary, rare, out-of-log and intentionally updated cases. Report false-safe proposed writes and missed dependency mass as well as average retention; a method that vetoes every write does not win. Start with the oracle: if even it cannot improve the frontier in the planted sparse-cut regime, stop; if it only wins there, do not claim host-wide sparsity.
- **Evidence levels:** Finite observed retention, distributional risk with a declared sampling scheme, and exact/conditional proof over a declared domain are different results. Use isolated old panels for scoring, not for registry discovery, training, or retries; reserve fresh independent audits if the method repeatedly edits in response to earlier audit outcomes.

**Ledger screen.** The [idea ledger](https://github.com/manojbajaj95/cl/blob/dfb4d52e8e2ef4938bc1e578baa9a04c8d98cad5/reviews/idea-ledger.md) already killed activation read-pinning ([PR #117](https://github.com/manojbajaj95/cl/pull/117)): the consumer moved even when the activation did not. Sparse-write graph matchings, switched-observability/Gramian forecasts and functional syndromes were also killed; no proposal below infers rank from edge sparsity, predicts damage from a fixed Gramian, or assumes sparse collateral damage. The triage already demoted read receipts, static missing-edge confidence intervals and adversarial audits as standalone ideas. The cards below propose additional operations or falsification tests; novelty is a hypothesis, not a prior-art claim.

## Idea cards

### Find the reads that matter

#### 1. Protect the producer–consumer pair, not the slot
- **Mechanism:** Register a function of both sides of a read (e.g. an old consumer's bilinear response to a producer), so a coordinated change is allowed and a drifting consumer with pinned input is not.
- **Novelty vs nearest prior art:** PR #117's survivor matches sampled downstream Jacobians. The candidate is an interface invariant for *finite* producer and consumer co-writes, not another activation or tangent pin.
- **Cheapest first test:** In a fact encoder + linear reader, compare interface preservation to insertion pinning and downstream Jacobian matching at equal bytes; propose updates to both factors.
- **Old-task retention check:** Check A's normal held-out predictions and C after each co-write, including queries with extreme fact values.

#### 2. Learn a registry for a writer, not all possible edits
- **Mechanism:** Discover reads by intervening with an orthogonal basis of *feasible* writer directions on a sandbox copy. Register only directions whose effects can escape the old interface, and make the registry invalid when the writer family changes.
- **Novelty vs nearest prior art:** OGD uses old output gradients; [IIT](https://arxiv.org/abs/2112.00826) aligns specified causal variables. Here read discovery is relative to a versioned write language, using measured effects rather than imposing a causal graph.
- **Cheapest first test:** Give a dense-head toy hosts with two distinct low-rank B writers. Compare writer-specific registries to equal-budget OGD restricted to the same writers and to a shared registry.
- **Old-task retention check:** Score A and C after unseen within-family writes; switch to the other writer and count any stale-registry false passes.

#### 3. Find reads by repairing induced forgetting
- **Mechanism:** Use a sacrificial B write to induce an A failure. Restore candidate producer, gate or consumer channels independently on the edited model; register a putative dependency only if a paired forward intervention also reproduces the failure on the old model.
- **Novelty vs nearest prior art:** [Putting a Face to Forgetting](https://arxiv.org/abs/2601.22012) distinguishes feature encoding and readout damage. Turn that distinction into an intervention-tested registry used to stop future writes; repair of one incident is not the result.
- **Cheapest first test:** In a toy with known writer/reader spillover, compare paired patching to activation patching alone, gradient magnitude and equal-cost replay on fresh B streams.
- **Old-task retention check:** Measure A and C on new inputs where the originally patched channel co-occurs with a different distractor.

#### 4. Register jointly harmful writes as clauses
- **Mechanism:** Store forbidden combinations of read changes (e.g. “do not change both fallback channels”), not the union of all involved slots. Use circuit assumptions to bound the interaction order; unsupported orders remain uncertified.
- **Novelty vs nearest prior art:** The parent uses cancellation as a hidden-edge audit. Unlike pairwise merge surrogates already killed in the ledger, the object is a structural clause checked on the realized write, which can allow either change independently.
- **Cheapest first test:** Enumerate writes in a Boolean circuit with parity, redundancy and a planted three-way exception. Compare the clause checker to singleton sensitivity, an equal-byte union mask and matched quartet replay.
- **Old-task retention check:** Check every rare conjunction and ordinary A branch after each accepted write, not just the branches that revealed the clause.

#### 5. Extract reads invariant to representation relabelling
- **Mechanism:** Discover semantic coordinate pairs via matched donor interventions, then keep only the protected *relation* that transforms with an invertible change of internal basis. Quantify the storage cost of the decoder.
- **Novelty vs nearest prior art:** [Sparsity, Superposition, and Forgetting](https://arxiv.org/abs/2606.20431) diagnoses feature overlap and retention. This proposes a conservation target invariant to representational gauge, with bit cost as the endpoint.
- **Cheapest first test:** Rotate a sparse teacher's bottleneck without changing behavior; compare relation transport against GPM, a refit sparse mask and a Jacobian sketch on rotated and original hosts.
- **Old-task retention check:** Check all original A and C slices before and after rotation and B training; count gains that disappear when the decoder is priced.

#### 6. Train for cheap registered reads
- **Mechanism:** During A acquisition, reward small, verifiable source-to-output cuts under a menu of simulated future writers, not sparse activations. Include counterfactuals where using the easy shortcut breaks one future update.
- **Novelty vs nearest prior art:** Parent IIT-style training aligns host reads to a given graph; [crossed evidence](crossed-evidence.md) changes data to encourage lookup. Optimize *cost of certifying finite noninterference*, without making the oracle graph a training target.
- **Cheapest first test:** On a width-matched gated net, compare cut-cost shaping with equal-token crossed evidence, dropout and Fisher-weighted sparsity; test on a writer held out from shaping.
- **Old-task retention check:** Require normal A acquisition before B and held-out A/C retention afterward; penalize hiding reads by sacrificing rare A accuracy.

### Keep the registry complete as tasks and writers change

#### 7. Make negative lookups first-class reads
- **Mechanism:** Register what cannot outrank an old retrieval result or enter an old top-k set, using a query-region score-gap bound on excluded items; register fallback-on-empty separately.
- **Novelty vs nearest prior art:** Database predicate locks handle phantoms. The proposed analog covers continuously moving learned scores and new embedding entries, not exact database predicates or a cached fact version.
- **Cheapest first test:** A tiny nearest-neighbor task gains B items and rotates the query encoder. Compare gap bounds to observed top-k receipts, a fixed retrieval index and an equal-cost cached canary.
- **Old-task retention check:** Check ordinary A retrieval, empty-index fallbacks and hidden ties; record each unregistered entrant that causes an A error.

#### 8. Close the registry under newly reachable routes
- **Mechanism:** Define old-input regions with guards. Certify that excluded guards stay unreachable under a proposed finite write or recursively register their regions before committing.
- **Novelty vs nearest prior art:** This borrows counterexample-guided abstraction refinement; the target is closure of a *changing* read registry under B writes, not enumerating dormant branches once.
- **Cheapest first test:** In a tiny routed toll net, use exhaustive checking of inputs and compare update-triggered closure to a union-of-seen-routes mask and a static exhaustive union.
- **Old-task retention check:** Check A's rare switchovers, never-seen-but-in-support branches and C after every admitted B prefix.

#### 9. Commit interface changes and consumer migrations together
- **Mechanism:** Stage a fact/feature rewrite with a new registry version. Publish it only with migrated old consumers or a verified compatibility shim; include concurrent readers, a partial migration and a newly introduced bypass in the checker.
- **Novelty vs nearest prior art:** A direct borrowing from transactional schema migration, distinguished from the parent's version tags by atomically maintaining *behavioral obligations* across learned producer and consumer replacements. This is an engineering control unless it beats ordinary versioned isolation.
- **Cheapest first test:** Interleave two tiny fact writers and several old readers; compare to reject-on-overlap, full old-snapshot routing and independent post-write repair at matched bytes.
- **Old-task retention check:** Evaluate live A/C between transactions and at commits; no transient regression is hidden by successful end-of-stream repair.

#### 10. Retire old reads by a replacement proof
- **Mechanism:** Allow a dependency to disappear only when its replacement cut is independently established and a finite perturbation witness shows the former read can now move within the contract.
- **Novelty vs nearest prior art:** [Rented constraints](https://github.com/manojbajaj95/cl/pull/145) makes protection temporary; this retires one obligation because its carrier has been replaced, not because a lease expired or no recent gradient used it.
- **Cheapest first test:** Teach a second implementation of an A exception while B competes for the original slot. Compare proof-gated deletion with time expiry, keep-all and old-task-distillation plus fixed-budget pruning.
- **Old-task retention check:** Test A's replacement-only cases and C immediately after reclaiming the supposedly safe slot, then again after more B.

#### 11. Transport a registry across feature refactors
- **Mechanism:** Translate old registrations through a candidate encoder map only if relevant readers and permitted writers are shown to commute with the translation. Rebuild registrations for unmatched or newly aliased coordinates.
- **Novelty vs nearest prior art:** Representational alignment and [cross-generation inheritance](https://github.com/manojbajaj95/cl/pull/130) transfer features or skill. Here the transferred object is permission for specific *future writes*, not outputs at the checkpoint boundary.
- **Cheapest first test:** Refactor a bottleneck by permutation, rotation and lossy merge; compare transport to rediscovery, frozen old coordinates and output-only alignment, then perform a held-out B edit.
- **Old-task retention check:** Check A/C after the migration *and* the later write; flag any transport that matches outputs but incorrectly permits edits.

#### 12. Audit for missing reads outside the graph's own proposal set
- **Mechanism:** Run fresh write challenges from a declared mixture with nonzero support outside predicted conflicts; use sampled false-safe writes to update an anytime risk bound and send a reproducible counterexample back to discovery. Reset or stratify when the writer or distribution changes.
- **Novelty vs nearest prior art:** [Change-Provenant Supervision](https://arxiv.org/abs/2609.28574) already requires independent revalidation; the parent already proposes a missing-edge interval. The candidate improvement is spending the audit on *realized false-safe writes* under adaptive reuse, not claiming graph completeness.
- **Cheapest first test:** Inject a hidden rare writer family and compare rotating outside-graph audit, fixed replay canaries and equal-count unbiased write tests; check coverage under adaptive registry fixes.
- **Old-task retention check:** Track ordinary A/C alongside rare false-safe incidents and measure whether the risk bound survives holdout on a fresh writer stream.

### Prove a write is safe, or expose why it cannot be

#### 13. Certify an end-to-end cut with an explicit bypass test
- **Mechanism:** Require a certificate specifying the frozen consumer, all crossings into it and allowed changes to shared state. A newly added residual edge invalidates the proof until the new interface is certified.
- **Novelty vs nearest prior art:** SPACE-LoRA suppresses responses along selected residual input directions. A typed cut checker would cover every path that can affect A, not merely the response of known residual branches.
- **Cheapest first test:** On a small explicit DAG, enumerate edge/header writes and add a bypass or change normalization state. Compare exact cut checking to rank-/cost-matched SPACE-LoRA and finite anchor gating.
- **Old-task retention check:** Exhaustively check A (including inserted-residual and normalization cases) and C; one accepted divergent output refutes the exact claim.

#### 14. Keep a budget against the original contract
- **Mechanism:** Carry an anchored, per-output residual budget that includes shared-interface errors weighted by certified downstream sensitivity. Compose bounds across updates or refresh only with independent evidence against the original contract.
- **Novelty vs nearest prior art:** CABA already has sequential composition bounds; the delta is a compositional budget across several internal reads shared by different consumers, with reuse of certificates across tasks rather than fresh output anchors per consumer.
- **Cheapest first test:** Compare cut-level error accounting with CABA and local per-step drift thresholds on alternating small B writes with aligned versus cancelling residuals.
- **Old-task retention check:** Score A/C against their original versions at every prefix, with margins matched at acquisition; detect cumulative drift despite all steps individually passing.

#### 15. Project onto a finite safe region instead of a flat nullspace
- **Mechanism:** Find a feasible B update preserving an old decision by verifying inequalities on a small piecewise-linear writer domain. Permit a feature to cross in either direction when another change compensates without violating any old decision obligation.
- **Novelty vs nearest prior art:** DUET protects Jacobian constraints at both ends; CABA searches a candidate interpolation. Search certified feasible joint writes outside the tangent and the chosen interpolation line, not merely certify an endpoint proposal.
- **Cheapest first test:** Enumerate a two-parameter ReLU decision problem where the safe region contains off-tangent B optima. Compare a small exact solver to DUET, trust-region line search and direct replay.
- **Old-task retention check:** Check all A regions, boundary cases and C after every commit; report logit drift separately so decision-only preservation is not sold as exact output equivalence.

#### 16. Make certificates report when they do not compose
- **Mechanism:** Annotate a safe write with the interface assumptions it used. When another write changes an assumption, require a joint proof or verify both orders; independent verdicts are composable only with a preserved invariant.
- **Novelty vs nearest prior art:** Transaction serializability checks conflicting accesses; the proposed semantic conflict is that one individually harmless learned write enables another, even if their coordinate masks are disjoint.
- **Cheapest first test:** Construct disjoint writes to a gate and a payload; compare assumption-triggered recomposition to ordinary disjoint-mask checks, fixed endpoint audits and certifying every pair.
- **Old-task retention check:** Evaluate every A/C prefix in both orders, plus the normal B order; count false merges and how many legitimate merges are rejected.

#### 17. Prove old policy behavior on reachable histories
- **Mechanism:** Register policy action distributions and mutable environment/model interfaces on a closed reachable set. For approximate matches, propagate occupancy or coupling bounds under declared dynamics rather than treating frozen old traces as sufficient.
- **Novelty vs nearest prior art:** CABA already bounds trajectory divergence under support assumptions. Propose maintaining the protected support via cut-driven reachability and allowing drift on unreachable branches, not a new generic divergence bound.
- **Cheapest first test:** In a small tabular route-choice MDP, compare support closure against CABA-style trajectory anchors and matched replay, then let a rare early branch become reachable after B.
- **Old-task retention check:** Compare live A/C return, worst reachable branch and occupancy against baseline; a frozen logged policy score alone does not pass.

#### 18. Return an impossibility witness, not just a veto
- **Mechanism:** If all feasible writes reaching a B target would violate A, return the conflicting old obligations, or a lower bound on new capacity/routing information. Use exact linear inequalities first, and distinguish solver uncertainty from a proof of infeasibility.
- **Novelty vs nearest prior art:** [GEM](https://arxiv.org/abs/1706.08840) projects steps against old loss constraints. The object is a checkable reason why a declared B progress target cannot coexist with the old read contract, informing whether to add capacity or reject the target.
- **Cheapest first test:** Sweep shared features and same-input contradictory targets in an exactly solved linear toy; compare with gradient-conflict scores and a rank-matched hand expansion.
- **Old-task retention check:** After adding only the capacity permitted by the witness (or declining B), check A and C incl. ambiguous inputs, and report attained B separately.

### Use the freed capacity without gaming retention

#### 19. Optimize a replacement cut before placing a B write
- **Mechanism:** Discover more than one independently sufficient implementation of A, and migrate to the one whose protection least interferes with the current writer. Choice must be made and verified before live state changes.
- **Novelty vs nearest prior art:** [Recovery witnesses](https://github.com/manojbajaj95/cl/pull/139) asks what minimal carrier can recover a hidden skill. Here the alternatives are live equivalence contracts permitting *preemptive* migration, with their redundancy and search cost charged.
- **Cheapest first test:** Train two candidate routes for A with interchangeable outputs; compare load-aware cut choice to a fixed cut, router/expert isolation and equal-byte backup/replay.
- **Old-task retention check:** Evaluate ordinary A, its rare route and C post-migration before and after B; forbid restoring baseline weights during evaluation.

#### 20. Split authorized fact changes from skill forgetting
- **Mechanism:** Declare what B is allowed to change in the fact store, and protect A's map from current premises to answers, not its previous answers under every premise. Use a separate fallible-model read registry for untouched consumers.
- **Novelty vs nearest prior art:** Parent invalidation and [Semantic-Scope Projected Evolution](https://arxiv.org/abs/2609.36626) already target scoped edits or compatibility. The test is whether separate revision and preservation obligations prevent a CL projector from preserving stale answers or eroding unrelated procedures; a control, not a claim of new editing.
- **Cheapest first test:** Interleave B's true toll revisions and nuisance rewrites; compare to static A distillation, plain invalidation plus replay and a pure executor.
- **Old-task retention check:** Score normal A on current truth, old procedures on oracle premises, A's unaffected requests, and C; report adoption of authorized changes separately.

#### 21. Factor shared cuts but price read amplification
- **Mechanism:** Factor out a shared interface across old tasks only if preserving it costs less than the union of their consumer-specific obligations; optimize over shared and private slices using rank on the realized writer plus verification cost.
- **Novelty vs nearest prior art:** GPM merges activation bases and SPACE-LoRA allocates coverage by module sensitivity. The proposed unit to share is a witness-backed behavioral contract that can be reused without tightening every consumer's constraint.
- **Cheapest first test:** Stream many small threshold tasks sharing facts but not all gates; compare factored contracts to rank-matched OGD, union masks and explicit per-task registries while growing task count.
- **Old-task retention check:** Track earliest-task A and rare singleton consumers, not just averages over frequent users of the shared interface; check C.

#### 22. Learn how to steer around a certified read cut
- **Mechanism:** When the allowed writer cannot reach a B goal cheaply, use counterfactual gradients to propose a new producer location for B and prove its route is disjoint from old consumers or composes with their contracts.
- **Novelty vs nearest prior art:** [PackNet](https://arxiv.org/abs/1711.05769) gets new capacity through pruning and masks. This proposes write-side relinking with a checkable noninterference contract, no inference task ID, and reuse of functionally safe shared computation.
- **Cheapest first test:** One bottleneck has free coordinates but a shared normalizer that can leak; compare certified relinking to PackNet-style masking, matched extra adapters and ordinary projection.
- **Old-task retention check:** Check A/C on unlabeled mixed A/B/C requests; specifically test shared normalization and a new route that would otherwise shadow A.

#### 23. Verify a local write only where it can change behavior
- **Mechanism:** First use a verified write-effect enclosure to slice the old contract into provably untouched regions and those needing a stronger checker. If effect analysis fails, fall back to the full verifier, never to “no hit.”
- **Novelty vs nearest prior art:** Incremental verification and Change-Provenant Supervision already separate scope from soundness. The possible gain is a *certified* cheap exclusion for learned finite writes, not learned lineage as permission to skip checks.
- **Cheapest first test:** Compare a finite-write bound plus exact regional checks with checking every region and CABA, at equal false-safe rate on low- and high-overlap toy streams.
- **Old-task retention check:** Independently score A/C in both checked and skipped regions, including an exception narrowly missed by an unsound interval.

#### 24. Map when read-set protection becomes no cheaper than replay
- **Mechanism:** Construct matched worlds whose small semantic read sets are respectively realized by a sparse cut, a dense redundant computation, or a dense high-rank dependence on the writer. Vary the gap without varying task difficulty or margins.
- **Novelty vs nearest prior art:** Sparsity/superposition studies report overlap and representation loss. This is a falsifier for the proposed *resource advantage*: estimate whether sparse protectability, not semantic edge count or representation sparsity alone, predicts the frontier.
- **Cheapest first test:** For enumerable linear/gated hosts, compute oracle constraint rank and compare oracle and learned registries to GPM/OGD and matched-byte replay as the gap grows.
- **Old-task retention check:** Compare live A/C at the same B error across all three worlds; require a positive regime and document where even the oracle ties or loses.

## Ranked deeper questions

1. **Does a cheap enough sufficient read cut exist in a learned host?** Run card 24 before discovery. Compare oracle model cuts, oracle spec maps and tuned GPM/OGD/replay at matched B progress. Aim for a clear resource gap (e.g. 4× fewer independent constraints *and* lower all-in cost in the planted regime), not smaller edge counts with bigger decoders. An oracle tie kills the premise for that regime.
2. **Can we identify the cuts using evidence cheaper than what we would replay?** Compare writer-relative probes and bidirectional repair witnesses (2–4) against matched replay and sampled Jacobians. Demand out-of-log retention and cross-writer generalization or an explicit invalidation rule. Constant facts, redundant paths and null first derivatives make passive logs insufficient.
3. **Can completeness survive a new route, a replacement consumer, or a changed writer?** Combine absence reads and closure (7–12), then deliberately shift routing and the writer family. Require lower missed-dependence risk than equal-cost independent revalidation; when neither verification nor coverage applies, report “unknown.”
4. **Can a finite-write certificate remain sound and useful over a long stream?** Test cut closure, non-composing writes and cumulative drift (13–17, 23). Compare to CABA and exhaustive checking on a finite oracle; preserve real A decisions or trajectories at every prefix, not just selected logits. If safety costs full revalidation every time, the registry is only triage.
5. **Can acquisition make sparse protection a property we can build rather than hope for?** Compare cut-cost shaping (6) and certified relinking (22) to crossed data, adapters and a versioned external reader under equal capacity. Keep authorized B revisions and unrelated C behavior intact; otherwise the apparent gain is freezing or extra storage.
