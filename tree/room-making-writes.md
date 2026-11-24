# Room-making writes

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Precondition-carrying writes](precondition-writes.md) ([PR #158](https://github.com/manojbajaj95/cl/pull/158)), cards 06 and 16. **Review seed:** [Flood triage row 253](https://github.com/manojbajaj95/cl/blob/9c5f45c8a43d6c8290c5745426a27fe1f37d6d45/reviews/flood-triage.md#L253): choose a write that actively establishes another writer's published precondition, and when a precondition fails, return the violated condition and a sufficient fix another writer can establish. [FSR1 (row 248)](https://github.com/manojbajaj95/cl/blob/9c5f45c8a43d6c8290c5745426a27fe1f37d6d45/reviews/flood-triage.md#L248) only protects room that already exists.

**Are learners that build room for each other's future writes a new object for continual learning?** Establishing another action's prerequisite is standard planning. What might be new for CL is a reusable interface for *learning* such effects: independently trained writers can ask for semantic changes, fulfill the requests while acquiring their own tasks, and let a delayed writer use the result without refitting its payload or passing around old examples. That claim requires a gain over planning, repair and verification with the same information, not just a successful sequence of writes.

## What counts as building room?

- **Active, not merely safe.** A pending consumer publishes a checkable entry guard `P` for its frozen transition `T`. A provider B chooses a useful local write `S` that takes a live state from `not P` to `P`, while meeting B's own acquisition floor and retaining the old tasks. If B only raises a score for `P` but still fails the check, report progress, not admission. If `P` already held and would have held under ordinary B training, count preservation, not creation. Measure confirmed `false → true` changes relative to matched choices, plus any room they destroy for other writers.
- **Failure with a next move.** Return either an unsupported check (missing evidence, not a violated predicate) or a falsified predicate with a witness, and, where available, a sufficient postcondition `Q` with a checked implication `Q ⇒ P` under named live premises. Where one conjunct failed, a fix for it alone suffices only if the rest are protected or rechecked. The provider must show that its own useful write establishes `Q` on the current start and respects the service contract. An unattainable `Q` is not a fix; if local feasibility is unknown, label it a request and abstain if nobody can fulfill it. Do not widen `P` or alter `T` to get a pass.
- **Fulfillment is not admission.** Bind the request and effect proof to versions, domains, tie rules, and served prefixes or an explicitly atomic endpoint. Recheck the guard on the actual state before publication and check obligations added since the consumer's proof, including the provider's newly acquired task. A threat between provider and consumer can undo the effect. An unchanged payload must still meet its usefulness floor; authorizing a write is not learning the task.

**Paper check.** Let old A require `x > 0`, old C use an independent coordinate, and the delayed consumer set `x := y − 2` and acquire its own skill. Start at `x = 3, y = 1`. Two equally useful B choices leave `x` and C alone, but one leaves `y = 1` while the other sets `y = 3`. The consumer's A guard is `y > 2`; B can make it true without increasing either old margin. A sufficient repair request is `y ≥ 3` in the toy's integer domain. A provider that establishes it via a *served* `x = 0` prefix is invalid. If D is acquired meanwhile and requires `x > 2`, the old guard passes at `y = 3` but the consumer would lose D; the live test needs `y > 4`. This construction separates the checks; a win in this hand-built world is not evidence that room transfers to undisclosed edits.

## Prior art and common CPU test

[STRIPS](https://doi.org/10.1016/0004-3702(71)90010-5), [UCPOP](https://homes.cs.washington.edu/~weld/papers/ucpop-kr92.pdf) and [multi-agent planning](https://doi.org/10.1016/j.artint.2007.02.002) already establish open conditions, protect causal links against threats, and plan with divided information. [Pacti](https://arxiv.org/abs/2303.17751) already reasons about composing assume–guarantee contracts and deriving missing component obligations. [SpecRepair](https://arxiv.org/abs/2106.01917) and [APRNN](https://arxiv.org/abs/2304.03496) already repair against behavioral specs; a counterexample plus another solve is not a primitive. [Git-Theta](https://arxiv.org/abs/2306.04529) and [task arithmetic](https://arxiv.org/abs/2212.04089) cover tracked model changes and composition. [GPM](https://arxiv.org/abs/2103.09762) and [O-LoRA](https://arxiv.org/abs/2310.14152) protect or separate update directions, [Learning to Continually Learn](https://arxiv.org/abs/2002.09571) already trains for future updates, and [Certified Continual Learning](https://arxiv.org/abs/2407.06697) already reuses verification work. The [idea ledger](https://github.com/manojbajaj95/cl/blob/9c5f45c8a43d6c8290c5745426a27fe1f37d6d45/reviews/idea-ledger.md) rules out treating forecasted readiness as a win (PRs #9 and #21), pinning an interface without checking downstream consumers (PR #117), or dressing ordinary lesson repair up as guard negotiation. This is a prior-art screen, not a priority claim.

Use tiny rational ReLU hosts and finite menus first. Enumerate legal prefixes and frozen-consumer admissions as truth; separate truly infeasible cases from incomplete certificates. Use rare and common A examples and an unrelated old C route; check exact acquisition-decision agreement and ground-truth accuracy separately. Register B and any intervening D when accepted; check all registered tasks at each served prefix, including after the consumer. Held-out old inputs test generalization; they are not covered by a finite-domain proof. Fit choices on one set of consumers, commit B, then reveal independently generated consumers with different directions and include an unrelated holdout and a purposely incompatible one. Report actual consumer utility and zero false admissions, along with coverage, unsafe proposals rejected, delays and total costs; count the old service and opportunities lost on paths not chosen.

Stack ordinary causal-link planning with the **same** effect/guard language, proposal budget and verifier, plus incremental rebase and ordinary counterexample repair with the same private-data access. Give the planner the same generated menus in a fixed-menu arm and give it the same ability to call a local constrained optimizer in a learning arm. Also compare ordinary B loss, matched old margins and a margin bonus, FSR1 preservation, orthogonal updates, parent guard-only rebase, and fresh local refit where allowed. Joint repair with disclosed inputs and exhaustive planning are ceilings, not privacy-matched controls. Match capacity, current-task progress, old service, compute, retained/transmitted bytes and rounds (or show a frontier); charge unsuccessful requests, waiting, and every check. Labels below mark **primitive candidates** (a reusable CL interface if it clears these controls) or **improvements** (a better policy, solver or audit).

## Idea cards

### Make room on purpose

#### 01. Train the provider, not the pending payload
- **Mechanism:** Fit B under its own floor, then spend the remaining search budget on crossing a published consumer guard. Deliver the same B task and keep the consumer frozen.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** UCPOP can select a supporting action; the candidate operation is to train a useful action to support a foreign behavioral guard and offer its checked effect to other clients.
- **Cheapest first test:** Fit tiny B readouts with a published pending guard. Reveal a second, separately generated consumer only after B commits; compare ordinary B loss, matched margin bonus, FSR1, and planner-plus-local-optimization.
- **Old-task retention check:** Match pre/post-B A/C margins and decisions across arms; recheck A/C and B after every consumer prefix.

#### 02. Make room that survives a change of rival
- **Mechanism:** Train B to establish a relational guard between the old winning route and a future write's rival routes, rather than increasing the current winning logit indiscriminately.
- **Novelty vs nearest prior art — IMPROVEMENT:** GPM protects old features; certified margin constraints already protect comparisons. The proposed objective changes the rival set based on a pending transition.
- **Cheapest first test:** In a three-class ReLU model, match today's margins but vary which rival the consumer can move. Give a margin optimizer the same rival information and compare admissions and search work.
- **Old-task retention check:** Check all A rival comparisons including rare examples, the separate C head, and B's own acquired class after the consumer.

#### 03. One establishment, several unannounced consumers
- **Mechanism:** Learn an effect that entails a public family of guards with shared functional structure. Publish the effect once; late writers prove entailment for their particular frozen deltas, not by citing family membership alone.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Pacti already computes contract implications; the CL candidate is an effect learned on one set of writes that becomes a reusable provider for independently trained writes.
- **Cheapest first test:** Generate consumers by two different editors on the same tiny host. Train B with only one editor's published guards, then test transfer against direct guard optimization, GPM and exact planner reuse with equal bytes; shuffle family identities as a placebo.
- **Old-task retention check:** Enumerate A/C/B decisions after each admitted late write; compare separate single-consumer runs and actual sequential consumption.

#### 04. Move room between old carriers
- **Mechanism:** Fit B so it transfers an old behavior to a second route before freeing the first for a pending consumer, and prove the consumer's guard on the freed route.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Make-before-break](https://github.com/manojbajaj95/cl/pull/157) already validates a replacement before retiring a route. The added optimization target is a particular other writer's edit, not just safe retirement.
- **Cheapest first test:** Use two redundant ReLU channels and a frozen consumer that needs one channel writable. Compare ordinary make-before-break plus verified channel selection and a matched extra-channel control.
- **Old-task retention check:** Check rare A cases that only use the migrated channel, C, and B at switchover, retirement and after the consumer.

#### 05. Establish a guard by changing routing, not weights
- **Mechanism:** Train B to move interfering traffic out of a consumer's edit domain. Prove the new routing on the relevant input set, including changes in downstream behavior.
- **Novelty vs nearest prior art — IMPROVEMENT:** Progressive/modular CL already isolates tasks; routing is a second action class for satisfying a behavioral request at fixed capacity, not evidence that modularity is new.
- **Cheapest first test:** Compare a two-expert router edit, orthogonal B update and planner with both choices on a stream with overlapping task inputs and no task ID at inference.
- **Old-task retention check:** Check A/C decisions on both sides of the routing boundary and B after the delayed edit; report held-out misroutes separately.

#### 06. Build room without borrowing from a different consumer
- **Mechanism:** Choose B using guard gains and guard losses on other known clients, and attach the lost opportunities to the effect offer. Allow tradeoffs only when the protected requests still have feasible continuations.
- **Novelty vs nearest prior art — IMPROVEMENT:** Multiobjective planning prices opportunity cost already. The CL policy optimizes measured options for concrete payloads rather than a proxy like unused parameter dimensions.
- **Cheapest first test:** Use three opposed guard directions, including disjunctive alternatives. Compare guardian counts, greedy priority and exact multiobjective planning; add a withheld claimant.
- **Old-task retention check:** Verify A/C/B both on the chosen trace and on every advertised fallback continuation, not only on the branch with most opened guards.

#### 07. Train complementary suppliers that cannot do it alone
- **Mechanism:** Have B and E train separate local writes toward distinct conditions of a pending guard, each conditioned only on checked offers, then prove the composition with cross-effects included.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Ma-STRIPS and the parent's card 03 already coordinate partial effects. The candidate is an interface that lets learners synthesize compatible effects from private tasks without exposing their proposals' training objectives.
- **Cheapest first test:** Split a two-feature guard across private providers with cross-terms, including a case in which the second write undoes the first. Compare same-interface generic planning with constrained local solvers and a disclosed joint ceiling.
- **Old-task retention check:** Verify A/C after each partial fulfillment, B after E, and A/C/B/E after the delayed consumer.

### Fail with a fix somebody can learn

#### 08. Return an executable request instead of a failing example
- **Mechanism:** Turn a failed guard into a witnessed failed clause and a sufficient provider postcondition. Accept a later provider's proof and apply the original payload only after live rechecks.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** SpecRepair returns counterexamples for a repair loop; Pacti computes missing guarantees. The candidate is a bilateral request/fulfillment operation whose provider learns its own task under the requested guarantee.
- **Cheapest first test:** Delay a frozen edit and reveal a provider with private data after rejection. Compare raw counterexample exchange, causal-link planning over the same effects, fresh refit and disclosed joint repair. Count total rounds and work, not just the consumer's retries.
- **Old-task retention check:** Check A/C and intervening D after the preparation and replay every consumer prefix with B registered; include a fix that preserves the violated example but flips a different A example.

#### 09. Offer alternative fixes in the provider's language
- **Mechanism:** Compile the failure into several sufficient postconditions (e.g. move a read boundary or reroute a population), each with its own assumptions. The provider can reveal which it can fulfill without revealing why it rejected the others.
- **Novelty vs nearest prior art — IMPROVEMENT:** Disjunctive planning and [merge menus](mergeable-writes.md) already return alternatives. This is query design for repairs when the requester does not know the provider's feasible actions.
- **Cheapest first test:** Use private feasible sets in a two-route stream. Compare one condition at a time, an equal-byte disjunction and stock planning with the same feasibility queries; include a weakest precondition that's expensive to check.
- **Old-task retention check:** For each advertised fulfillment actually used, check A/C/D and the provider's acquisition after the unchanged consumer; include a condition whose proof expires when the other route moves.

#### 10. Separate a missing fact from a false fact
- **Mechanism:** On failure, distinguish a witnessed violation from unknown verifier premises; return an evidence request for the latter and a state-changing repair request only for the former.
- **Novelty vs nearest prior art — IMPROVEMENT:** Three-valued analysis and the parent's diagnostic acquisition already separate unknown from false. The benefit sought is avoiding needless training when knowledge is the bottleneck.
- **Cheapest first test:** Mix states that are unsafe, safe-but-unproved, and both missing evidence and outside an unrelated guard conjunct. Compare incremental rechecking and counterexample-only repair.
- **Old-task retention check:** Enumerate A/C/D on all committed prefixes; check that supplying evidence never admits an actually false guard or skips B's obligations.

#### 11. Refuse a request with a scoped infeasibility proof
- **Mechanism:** Let B return either a fulfillment proof or a bound showing that none of its allowed useful writes can meet the repair condition in this context. The requester can seek another provider or defer.
- **Novelty vs nearest prior art — IMPROVEMENT:** Unsatisfiable cores in constrained optimization and distributed planning are prior art. A reusable refusal could avoid repeated training of the same impossible repair, but only within a declared action budget.
- **Cheapest first test:** Enumerate tiny provider menus with one absent provider, one truly infeasible provider, and one where changing B's budget makes the fix possible. Compare simple negative caching and proof-keyed refusal.
- **Old-task retention check:** Verify A/C/D on the eventual alternative and confirm that refusing an impossible request leaves A/C/D unchanged rather than silently relaxing the contract.

#### 12. Supply a fix with an explicit validity window
- **Mechanism:** Attach the live assumptions that keep the sufficient fix sufficient. If an intervening write changes one, expire the fulfillment or obtain a new check instead of reusing stale success.
- **Novelty vs nearest prior art — IMPROVEMENT:** UCPOP already detects threats; the parent's expiry and delta-verification cards already track them. This tests which invalidations matter for a negotiated fix rather than creating a new lifetime mechanism.
- **Cheapest first test:** Interleave harmless, threatening and obligation-adding writes before the consumer. Compare exact threat checks, rechecking every time, and assumption-keyed reuse at equal checking work.
- **Old-task retention check:** Recheck A/C/B/D at each actual commit; include a previously valid repair with no longer valid B retention after the consumer.

#### 13. Negotiate with behavior-only requests
- **Mechanism:** Express the fix in the outputs of a small shared probe basis, with proof that those outputs suffice on a scoped state region; let B learn it without sharing its examples or internal coordinates.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Assume–guarantee and distillation already work with black-box interfaces. The candidate is a portable request that changes a host just enough for a frozen third-party edit, without passing that client's training set.
- **Cheapest first test:** Use two gauge-equivalent small hosts and one host with the same probe outputs but a different downstream consumer. Compare equal-byte private counterexamples, contract synthesis, and coordinate constraints; reject the alias unless separately proved.
- **Old-task retention check:** Check end-to-end A/C/D and B after the consumer in both equivalent hosts; matching probes alone is not retention.

#### 14. Learn a provider's reply policy from previous requests
- **Mechanism:** Cache which local editing operations tend to fulfill each class of request at acceptable local cost. Use the policy to propose a reply, never to certify it.
- **Novelty vs nearest prior art — IMPROVEMENT:** Learning to Continually Learn and learned solver heuristics already amortize adaptation. Here the prediction target is successful fulfillment for another writer, not generic future readiness.
- **Cheapest first test:** Recur guard classes with changed unseen instances; compare nearest cached patch, warm-start repair and learned replies under equal local solves and verifier budgets. Swap a guard class midway.
- **Old-task retention check:** Check A/C and all registered providers through the entire stream, including prefixes after the class swap and the first wrong predicted reply.

### Repeated and reciprocal room-making

#### 15. Train today to lower another writer's future establishment cost
- **Mechanism:** If a pending guard cannot be established now, choose B so a later *useful* provider can establish it more cheaply; measure the later provider's verified cost, not B's distance to the guard.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Future edit cost](future-edit-cost.md) and multi-step planning already price downstream work. Here the downstream work is a different learner satisfying a published repair request.
- **Cheapest first test:** Construct two equal-loss B choices with equal current margins and guard truth but different feasible E menus. Compare equal-budget lookahead and generic conditioning, then reveal E's private alternatives.
- **Old-task retention check:** Check A/C/B after E and after the consumer; include all B prefixes and report if cheap prep damages E's acquired task on consumption.

#### 16. Trade room in both directions without counting a deadlock as progress
- **Mechanism:** Let two pending learners provide supports for each other using certified enabling writes. If no useful first support is available, return a deadlock or a separately verified atomic joint publication, not a circular permission.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Partial-order planning rejects causal cycles and joint repair can find a compound step. The CL candidate is a reusable reciprocal fulfillment interface that also tracks the tasks each participant acquires.
- **Cheapest first test:** Compare a solvable two-way exchange with a cycle that has no safe first move and one that is safe only in shadow. Use equal menus, incremental planner checks and atomic joint repair.
- **Old-task retention check:** Audit A/C at every served hop and both acquired tasks after the exchange; verify a shadow solution only at its atomic publication endpoint.

#### 17. Replenish room after use without undoing the last acquisition
- **Mechanism:** When a consumer spends the guard, emit a repair request for a future provider. Accumulate acquired tasks into the contract so a refresh cannot earn credit by reverting the last consumer.
- **Novelty vs nearest prior art — IMPROVEMENT:** Replenishable planning resources and rollback already model spend and refill. The test is whether replenishment survives a growing behavioral contract at fixed capacity.
- **Cheapest first test:** Run alternating provider/consumer tasks on a low-rank host. Compare repair cycles with refitting and replay, and include an impossible suffix where new acquisitions pin all remaining degrees of freedom.
- **Old-task retention check:** Measure worst-prefix A/C and each earlier acquisition, especially immediately after refresh; measure absolute new utility rather than counting refreshes.

#### 18. Train a provider that helps weaker editors without subsidizing all updates
- **Mechanism:** Choose B by the improvement in verified admissions of capacity-limited consumers, conditional on meeting B's floor. Give providers credit only when those consumers would fail under matched ordinary B.
- **Novelty vs nearest prior art — IMPROVEMENT:** Curriculum and transfer already favor weaker learners. The proposed policy targets *admission of the same payload*, not ease of learning a replacement.
- **Cheapest first test:** Compare rank-one and rank-two frozen edits trained before B on equal task data; use ranked guard requests versus equal sharing and ordinary projected B, plus a shuffled-request placebo.
- **Old-task retention check:** Check rare A/C and B after both ranks' commits; disaggregate retention by which client was helped so aggregate utility cannot hide harm.

#### 19. Teach a newcomer how to supply an old kind of room
- **Mechanism:** Hand a previously unseen provider a small library of verified effect templates and residual checks. It adapts a template to its own task and publishes only a live checked fulfillment.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Repair templates and the parent's transport proofs already reuse solutions. Here the candidate operation is transfer of the *ability to fulfill* a class of behavioral requests across independently trained providers.
- **Cheapest first test:** Fit templates on providers updating one layer, then give a new provider a different support and a different private objective. Compare equal-byte patch libraries, re-solving, and generic contract reuse; include a violated mixed-layer premise.
- **Old-task retention check:** Require A/C, prior providers and the newcomer to survive the original consumer after adaptation; test the mixed-layer counterexample directly.

### Boundaries and decisive failure tests

#### 20. Find the information floor for a useful fix
- **Mechanism:** Construct providers indistinguishable by the public transcript but requiring different sufficient fixes; vary what a requester can ask about feasibility and measure the cost of distinguishing them.
- **Novelty vs nearest prior art — IMPROVEMENT:** Multi-agent privacy and communication lower bounds already rule out some distributed plans. This audit identifies when a behavioral repair interface inevitably needs extra information, shared data, or abstention.
- **Cheapest first test:** Enumerate pairs of tiny private B objectives with opposite feasible routes. Compare the shortest proof-backed request/answer protocol with a bit-matched feasibility query and exact planning with disclosure.
- **Old-task retention check:** Check A/C/D and B for each accepted branch on both private worlds; a protocol that guesses a fix and sometimes forgets old tasks fails.

#### 21. Measure establishment that isn't just margin, rank or extra compute
- **Mechanism:** Use matched B choices with different guarded causal effects and swap or withhold the request. Measure actual differences in admissions, not the correlation of a readiness proxy with one-step loss.
- **Novelty vs nearest prior art — IMPROVEMENT:** The ledger's plasticity reserve and projected-readiness controls already test future capacity. This audit isolates the contribution of the published precondition to admission of a fixed transition.
- **Cheapest first test:** In paired streams, match B utility, old margins, optimization work and rank; perturb each request independently of the old margins. Compare actual and shuffled requests on disclosed and withheld consumers.
- **Old-task retention check:** Require A/C decisions to match after B, and verify A/C/B/D after consumption; separately report a negative arm where added margin alone admits the consumer.

#### 22. Attack the apparent gain with closed-loop planning
- **Mechanism:** Convert each offered guard and effect into facts for a planner allowed to ask the same local learners for the same changes; test whether the supposed bilateral primitive can be compiled away.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is an equivalence audit against causal-link planning, not a new object. A residual advantage must be in learned transfer, information cost or amortized work, not naming.
- **Cheapest first test:** Enumerate finite streams with delayed obligations, silent competitors and concurrent effects. First compare fixed menus, then give both sides the same oracle for constrained local training. Identify the first concrete trace or cost the compilation cannot match.
- **Old-task retention check:** Compare exact served prefixes on A/C and every registered acquisition, including traces with equal endpoints but one unsafe prefix.

## Ranked deeper questions

1. **Does active establishment transfer to a late, independent writer once we match retention, margin and learning work?** Run 01 → 03 → 21. Reveal a second consumer only after B commits and keep its payload fixed. A benefit solely on published guards is useful coordination, not evidence for a reusable CL operation.
2. **What is the smallest failure reply that buys a valid repair without disclosing old examples or refitting the pending payload?** Run 08 → 13 → 20. Compare witnessed violations plus sufficient postconditions with ordinary counterexample exchange, generic planning over the same effects, and private feasibility queries. Count refusals, waiting and proof work; use disclosed joint repair and fresh refit to locate, not erase, the gap.
3. **Can repeated room-making increase useful capacity rather than just redistribute a fixed budget of opportunities?** Run 06 → 16 → 17 at fixed capacity with new acquisitions, unrelated and competing consumers, and a real deadlock. Require higher verified utility over the stream without worse worst-prefix retention, not more guard crossings on a hand-built favorable trace.
4. **Can this be compiled into existing planning and verification without losing the learning advantage?** Use 07 → 19 → 22 to separate savings from cached verification, comparable constrained optimizers, and effects that transfer between independent learners. If the strongest stack ties, keep it as an implementation pattern, not a new primitive.

**Verdict:** Active establishment and constructive failure are already planning and repair operations. The promising CL object is a transferable, checked request and fulfillment for an unchanged future write, learned by a provider that also acquires its own task. The cheapest discriminating result is a gain on a withheld consumer or a cheaper private repair at unchanged old-task service, against the full planner–repair–verifier stack. Without that, these are good coordination ideas, not a new continual-learning primitive.
