# Unannounced consumers

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Room-making writes](room-making-writes.md) ([PR #160](https://github.com/manojbajaj95/cl/pull/160)), cards 03 and 07. **Review seed:** [Flood triage row 256](https://github.com/manojbajaj95/cl/blob/746849bf6a722375238388229feee5e2f6d3a1bf/reviews/flood-triage.md#L256) scored two directions 3: one learned establishment supports later consumers from a different editor; complementary providers with private tasks jointly establish one pending guard. Read against the [idea ledger](https://github.com/manojbajaj95/cl/blob/746849bf6a722375238388229feee5e2f6d3a1bf/reviews/idea-ledger.md).

**Can a learner change what independently authored updates can do next, without seeing those updates?** The harder claim is not that two facts imply a guard, or that several actions can establish one. Those are known operations. It is that shaping a useful local write teaches a reliable *effect* that unseen frozen writes can exploit, and that independently trained suppliers can build such an effect from partial checked offers without the planner, consumer, or other supplier needing their private examples.

## What would count?

- **Transfer:** On one host, B trains on private data and guards published by editor E1; commit B and its effect description before an isolated E2 sees that descendant. Freeze E2's payload from a pre-provider reference or a precommitted blind editing procedure, then reveal it. E2 may derive a proof from the live state, but cannot adapt the payload to B. Score actual false-to-true guard crossings for useful E2 writes, not similarity to E1, predicted readiness, or proof-cache hits. Hold out an editor algorithm and task/operator family where possible; distinguish gains on related unseen guards from coverage on unrelated and deliberately incompatible controls.
- **Complementarity:** With B and F trained on separate private problems, neither useful local write can establish the pending guard alone. Their checked offers describe enough to prove composition, including negative cross-effects, without requiring them to exchange examples or loss surfaces. Operational data isolation is not a claim of formal privacy. Check each served intermediate state, or charge explicitly atomic staging; then independently check the frozen consumer against all live obligations, including B and F.
- **Separate proof, task success, and opportunity cost.** A true guard is not publication, and an admitted write must still do its job. Verify on the actual live state, with versions, domains and proof premises fixed. Report retained opportunities lost on other branches too. A learned scalar may propose a candidate; it may not authorize it.

**Paper witnesses.** Let old A protect `x > 0` and old C use an independent coordinate. On a host with free coordinates `u,v`, an E1 write sets `x := u+v−1` and an E2 write sets `x := 2u−v−1`; both fail from `(u,v)=(0,0)`. Equally useful B updates could write `(0,2)` or `(2,1)`. Both cross E1's guard, but only the latter crosses E2's, without changing A or C before consumption. E1's pass bit alone cannot choose between them. For complementarity, reset `u,v` and take a separate frozen write with guard `u≥1 AND v≥2` (for example `x := min(u,v−1)` on integer states). B sets `u:=2`; F sets `v:=2` but also subtracts 2 from `u`. Both offers look useful in isolation; B then F fails, F then B succeeds. If F cannot go first because its own update requires `u≥1`, neither order works. A different F write that subtracts only 1 would rescue B then F if it still learns F's task. No claim about learning follows from these hand-built witnesses.

## Closest work and common CPU oracle

[UCPOP](https://homes.cs.washington.edu/~weld/papers/ucpop-kr92.pdf) and [Ma-STRIPS](https://doi.org/10.1016/j.artint.2007.02.002) already establish open conditions across independent agents and detect threats. [Pacti](https://arxiv.org/abs/2303.17751) already composes assume–guarantee contracts. [Git-Theta](https://arxiv.org/abs/2306.04529), [Task Arithmetic](https://arxiv.org/abs/2212.04089) and [TIES-Merging](https://arxiv.org/abs/2306.01708) cover model versioning and merging; [Efficient Model Development through Fine-tuning Transfer](https://arxiv.org/abs/2503.20110) is the payload-transfer control, not the target operation. [Learning to Continually Learn (La-MAML)](https://arxiv.org/abs/2002.09571) and [MAML](https://arxiv.org/abs/1703.03400) train for future learning; [GPM](https://arxiv.org/abs/2103.09762) and [O-LoRA](https://arxiv.org/abs/2310.14152) constrain directions. [SpecRepair](https://arxiv.org/abs/2106.01917), [APRNN](https://arxiv.org/abs/2304.03496) and [Certified Continual Learning for Neural Network Regression](https://arxiv.org/abs/2407.06697) are repair and incremental verification controls. The cards below treat a new coordination or diagnostic policy as an **improvement**, not as a primitive. No priority claim.

Start with rational low-dimensional linear and ReLU hosts, finite useful-write menus, and exhaustive admission and prefix checks. Generate different consumer operators (e.g., a gradient-based frozen additive delta versus an independently constrained low-rank delta) and blind the split by editor, task family and world seed; never use E2 results to tune B. Include the paper witnesses, a systematic source/target overlap sweep, fixed trivial and impossible guards, and honest near-matches that should fail. In the supplier track, run B alone, F alone, both orders, and a no-supplier run from the identical snapshot. Include nuisance effects, justified atomic endpoints, impossible pairs, and affordable versus unaffordable communication.

The primary comparison is causal-link planning **plus** ordinary counterexample repair, constrained local optimization and incremental verification, using the same effects, guard language, local data access, proposal and verifier budget. On fixed menus give the planner identical candidates; on learned menus give it the same solver access. Also compare ordinary local loss, direct guard optimization on E1, [FSR1 preserved room](https://github.com/manojbajaj95/cl/blob/746849bf6a722375238388229feee5e2f6d3a1bf/reviews/flood-triage.md#L248), GPM, matched margin/rank, and shuffled guard-family identities. Use disclosed joint solving, direct E2 guard optimization, and fresh E2 refit as separately labeled ceilings, not matched controls. Match local acquisition floors, rank, time, retained and transmitted bytes, and validate zero false admissions against the exhaustive oracle; charge failed proposals, private queries, latency, and staging. Report useful frozen admissions and coverage, not just crossings. For every card, check A/C and all acquired tasks on all served prefixes and after the consumer; also check held-out old-task examples separately from any finite-domain proof. The ledger rules out readiness-only scores (PRs #9/#21), pinning upstream activations as a substitute for checking downstream behavior (PR #117), sparse coded recovery without sparse damage (PR #24), and ordinary counterexample-driven lesson rewrites or payload merging disguised as a new operation.

## Idea cards

### One establishment, many consumers

#### 01. Learn the overlap of two unseen write languages
- **Mechanism:** From E1 guard variations, learn to establish a checked bound on a shared functional response rather than a particular edit direction. An E2 writer derives its own guard implication from that bound after B commits.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Pacti supplies implication, La-MAML supplies future-update training; the candidate is a learned postcondition that a foreign frozen payload can independently use.
- **Cheapest first test:** Blind E2 on a two-editor ReLU suite. Sweep response overlap and compare exact planner reuse at equal bytes, direct E1 guard training, GPM, and shuffled family identities. Reject if held-out gain vanishes at matched margins and B progress.
- **Old-task retention check:** Check the exact A/C/B decision vector after B and after each E2 payload; test A on held-out inputs near its boundary.

#### 02. Train for a real counterfactual crossing
- **Mechanism:** Branch B into equally useful fits. Reward an E1 guard only when a learned effect turns a failure under the ordinary B fit into a pass; debit gates lost under the alternative.
- **Novelty vs nearest prior art — IMPROVEMENT:** La-MAML optimizes future performance; this is a guard-level contrast objective that removes credit for gates ordinary training already preserves.
- **Cheapest first test:** Put easy, impossible, and moveable guards in equal numbers. Compare against target loss, raw satisfied-guard count, and matched margin bonus, scoring new E2 admissions and destroyed controls.
- **Old-task retention check:** Compare both forks on the same old examples before and after their consumers; match A/C margins before attributing a difference to the effect.

#### 03. Fit invariants of meaning, not coordinates
- **Mechanism:** During B training, re-express E1's published conditions through exact hidden-unit permutation and positive rescaling. Establish an output-intervention bound that survives both coordinate charts; bind it to the chart used at verification.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Fine-tuning transfer moves an edit; GPM protects directions. This would let unchanged foreign edits use the same *host effect* in different factorizations rather than transporting their weights.
- **Cheapest first test:** On one host with equivalent parameterizations, blind E2 to the source chart until after commit; compare mapped-coordinate guards and full Jacobian controls. Include an invalid transformation to rule out claiming invariance by fiat.
- **Old-task retention check:** Include every downstream readout of the reparameterized block and check A/C/B after each transformation and consumer, not just upstream activations.

#### 04. Make room for a nonconvex choice without picking its branch
- **Mechanism:** Establish a proved disjunction across two functional routes. Let E2's exact payload prove which branch suffices on the current state, without assuming the route that E1 used.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Pacti and UCPOP already represent alternative support. The candidate is learning a transportable disjunctive effect that independently edited readers can refine, rather than recording which backup is live.
- **Cheapest first test:** A three-region ReLU host with two valid chambers and an unsafe midpoint. Compare learned disjunction with a convex relaxation and an exact disjunctive planner supplied the same candidate fits.
- **Old-task retention check:** Force the rare A examples onto both routes, audit dispatch and C before and after E2, and reject any false admission at the midpoint.

#### 05. Cross a guard on the reaction to a write
- **Mechanism:** B learns a lower bound on an observable task response under a bounded family of interventions, not just on passive outputs. E2 supplies a verified intervention descriptor for its frozen delta.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** GPM protects activation subspaces and APRNN repairs a model against a spec. This would establish a checked response to a class of future foreign edits, including gated effects not visible at the current forward pass.
- **Cheapest first test:** Match two B fits on outputs and Jacobians at the start; only one remains safe after a finite E2 delta crosses a ReLU gate. Compare first-order bounds and an exact finite-region solver.
- **Old-task retention check:** Check A/C/B on both sides of the gate after every served prefix; use held-out near-boundary inputs, not interpolation alone.

#### 06. Distinguish a reusable effect from a consumable one
- **Mechanism:** Publish whether a checked postcondition survives a member of a consumer class or is used up by it; learn B fits with survivor effects where possible. Check each actual consumption rather than granting blanket reuse.
- **Novelty vs nearest prior art — IMPROVEMENT:** Causal-link threat checks already revoke facts. The learning policy would actively select B for multi-use survival, not count successes on reset snapshots as simultaneous service.
- **Cheapest first test:** Two unknown E2 writes pass independently, but one spends the other's guard. Compare learned survivor policies with exact planning on the same candidates; enumerate both arrival orders.
- **Old-task retention check:** Verify A/C/B and the first new consumer's task after the second; count the failed orders instead of quietly resetting.

#### 07. Teach an effect without leaking the lesson through the test split
- **Mechanism:** Train B only on E1's Boolean guard results and checked witnesses; compare richer E1 interfaces while keeping E2's registry closed until B and all hyperparameters are frozen.
- **Novelty vs nearest prior art — IMPROVEMENT:** Ordinary transfer evaluation and SpecRepair already cover holdouts and counterexamples; the diagnostic asks what training signal actually enables independent guard reuse.
- **Cheapest first test:** Pair two guard families identical on E1 observations but different for E2. Compare bits, equal-byte signed witnesses, swapped-family witnesses, and oracle direction knowledge; if the bit-only method wins on indistinguishable cases, look for leakage.
- **Old-task retention check:** Give the two families the same old-task loss and examples, then check per-task correctness after the blinded consumer in both worlds.

#### 08. Transfer to an editor that changes its objective, not just its seed
- **Mechanism:** Separate E1 and E2 by constraints as well as operator: E1 edits a targeted score; E2 jointly preserves a relationship while acquiring a different output. Require E2's own proof, not an assumed equivalence of objectives.
- **Novelty vs nearest prior art — IMPROVEMENT:** MAML already evaluates adaptation to unseen tasks and fine-tuning transfer tests reusable task knowledge. This is a stricter guard-transfer assay for unchanged, independently generated payloads.
- **Cheapest first test:** Cross editor algorithm and objective in a 2×2 design with matched acceptance difficulty and a same-editor/same-objective control. If only new seeds benefit, downgrade to within-editor reuse.
- **Old-task retention check:** Check unrelated C and rare A in every cell, including proposals rejected by rollback or requiring staging; compare the same deployed states.

### Complementary private suppliers

#### 09. Train against the partner's checked offer, not its examples
- **Mechanism:** B learns one conjunct of a pending guard. F learns another using a checked envelope from B that constrains how much of the first may be disturbed; verify both writes' cross-effects and compare safe orderings.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Ma-STRIPS and Pacti already compose described effects. The candidate is an envelope that two useful learning steps can train against before either sees the other's objective or payload.
- **Cheapest first test:** Use the two-coordinate witness with a safe alternate F and an undoing F. Compare same-interface planning plus constrained local optimization, local solvers without feedback, and the disclosed joint ceiling.
- **Old-task retention check:** Verify A/C after B, A/C/B after F, and A/C/B/F after the frozen consumer; do the analogous checks in the reverse order.

#### 10. Learn a mixed term that neither supplier can install alone
- **Mechanism:** B establishes a range on a latent feature and F establishes a signed readout range; the pending guard depends on their product, not on separate thresholds at the two endpoints. The offers certify separate ranges plus the premises of a joint product bound.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Pacti already composes relational contracts, and TIES resolves interference in merged deltas. Here complementarity is a useful effect absent in both singleton writes, without changing the consumer.
- **Cheapest first test:** A two-factor model with zero stock feature and readout. Compare additive-effect planning, full relational planning at equal bytes, and a jointly fitted factor pair; include a sign flip that defeats unsigned norm bounds.
- **Old-task retention check:** Include an A slice and a C slice that already read the factors; test every intermediate endpoint and the consumer, not just the new product.

#### 11. Verify an offer's dependence on the incoming state
- **Mechanism:** Have F publish a checked lower bound on its effect as a function of B's incoming result, instead of treating F's standalone endpoint as its offer. B trains to meet a region where both conditions are closed.
- **Novelty vs nearest prior art — IMPROVEMENT:** UCPOP already reasons about conditional effects. The question is whether a cheap learned, then verified, region beats fitting against a single partner endpoint.
- **Cheapest first test:** Fit F on a single start and introduce a nearby state at which it decreases B's condition. Compare point offers, exact conditional effects, and reply-driven local optimization.
- **Old-task retention check:** Exhaustively check A/C/B across each admitted incoming region, including its boundaries, and carry F's own task through consumer verification.

#### 12. Propose different concessions before either supplier commits
- **Mechanism:** Each supplier publishes a small menu of checked effect envelopes with different cross-effects but the same local acquisition floor. Select a pair whose joint proof survives the other supplier's true write; don't average their payloads.
- **Novelty vs nearest prior art — IMPROVEMENT:** The repo's [mergeable writes](mergeable-writes.md) and Pacti already select feasible menus; the variant learns menus chosen for complementary guard establishment, not safe merging alone.
- **Cheapest first test:** Two useful candidates per provider, with only one jointly safe pair of non-top local candidates. Compare planner on identical menus, loss-ranked menus, and exact private feasibility queries at the same budget.
- **Old-task retention check:** Check both providers at their own floors and A/C through the selected live ordering; separately report the retention of locally preferred alternatives.

#### 13. Spend one extra message on the actual cross-effect
- **Mechanism:** When two offers compose except for a single unbounded cross-effect, ask for a bound only on that term. Use it to choose a fresh local fit or decline, not to revise the consumer's contract.
- **Novelty vs nearest prior art — IMPROVEMENT:** SpecRepair and the parent's counterexample negotiation already use failure evidence. This targets the remaining shared interaction, rather than repeating a generic repair query.
- **Cheapest first test:** Add ten irrelevant guard facts and one obstructing coupling. Compare a fixed disclosure bundle, ordinary counterexample exchange, and the exact same-information planner with an adaptive query.
- **Old-task retention check:** Do not serve speculative candidates; after any committed correction check A/C and the other supplier's acquired task before and after the consumer.

#### 14. Learn a pair that is safe only when published together
- **Mechanism:** Train providers on disjoint local tasks with checked effects that jointly satisfy the pending guard, but that fail old service in either served singleton order. Compose in shadow and require a single verified atomic publish.
- **Novelty vs nearest prior art — IMPROVEMENT:** Git-Theta and transaction-style staging already combine changes; the narrow question is whether learned complementary choices reduce peak resources compared with staging ordinary private repairs.
- **Cheapest first test:** Choose updates that cancel an A-breaking term but add different useful guard components. Compare staged joint search, ordinary constrained local writes, and a disclosed joint solve at equal peak bytes; veto the design when atomic publication is unavailable.
- **Old-task retention check:** Test A/C before and at the actual publish boundary and A/C/B/F after consumption; ensure no staged singleton is served.

#### 15. Ask whether a third supplier is indispensable
- **Mechanism:** Extend the pairwise offer format with a checked three-way term only when a two-supplier search cannot establish the guard. Demand a scoped oracle witness that no useful singleton or pair suffices.
- **Novelty vs nearest prior art — IMPROVEMENT:** Ma-STRIPS can search arbitrary coalitions. The point is to catch an interface that approximates away real synergy; it is not sparse-coded interference recovery, which the ledger rejects.
- **Cheapest first test:** A guard controlled by the product of three independently constrained effects, with one hidden negative triple. Compare pairwise bounds, exact three-way contracts and the exact planner at equal checks.
- **Old-task retention check:** Verify A/C on all served prefixes and B/F/third supplier after their acquisitions and after the consumer; require the triple veto when it breaks even one task.

#### 16. Offer slack where the partner is actually constrained
- **Mechanism:** Pick among B fits that all cross its conjunct by estimating F's residual feasible set from verified accept/reject or interval offers. Favor a B fit that leaves a feasible F adjustment, not the largest raw B margin.
- **Novelty vs nearest prior art — IMPROVEMENT:** Pacti constraint composition and local feasibility queries already search the same region. The variant is a useful-fit choice that targets another private problem's feasible boundary rather than generic extra slack.
- **Cheapest first test:** Give F a slanted feasible region so B's greatest own margin is the worst partner. Compare matched margin bonuses, independent fit selection, and constrained planning with identical query costs.
- **Old-task retention check:** Keep A/C margins matched across B branches and require B/F utility after the final consumer; measure worst-prefix retention rather than slack alone.

### Join the two branches, and try to break them

#### 17. Reuse a joint establishment without coordinating again
- **Mechanism:** Learn a joint B+F effect against E1's pending guard. Publish a composed certificate with both useful local writes fixed. Reveal E2 consumers only afterward; each must independently prove that this *same composition* establishes its own frozen guard.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Ma-STRIPS composes providers and Pacti reuses implications. The candidate is transferable room learned by complementary providers, not one team's solution to a fully known future plan.
- **Cheapest first test:** Cross blind E2 reveal with B-only, F-only, B+F learned, and equal-budget planned B+F. Demand new E2 admissions without re-querying the providers, and include an E2 write that invalidates the very joint premise it uses.
- **Old-task retention check:** Check all acquisition floors after the two supplier writes, then after each E2 consumer on reset forks and on actual sequential histories.

#### 18. Establish room for a consumer with weaker evidence
- **Mechanism:** Fit the joint effect to leave a wide enough *verified functional region* that an independent editor with a conservative verifier can prove admission from its own cheap witness; do not weaken the guard.
- **Novelty vs nearest prior art — IMPROVEMENT:** Certified CL already reduces repeated verification. Distinguish optimization for transfer across proof systems from mere saved verification or a larger safety margin.
- **Cheapest first test:** Hold the exact frozen effects fixed across an interval verifier and an exhaustive oracle. Match old margins and verification budgets, then separate more true crossings from better proof coverage on the same true guards.
- **Old-task retention check:** Cross-check both verifiers against exact A/C/B/F outcomes at every served prefix and separately test held-out old inputs.

#### 19. Locate the minimum information a supplier must reveal
- **Mechanism:** Construct two private feasibility worlds that share all currently exported receipts but require incompatible partner choices. Compare withholding, one discriminating yes/no query, and a checked interval disclosure.
- **Novelty vs nearest prior art — IMPROVEMENT:** Ma-STRIPS already studies divided information; this is a CL-specific lower-bound audit of the proposed offer language, not a new privacy mechanism.
- **Cheapest first test:** Flip F's hidden coupling sign while keeping singleton receipts and task scores identical. Enumerate which transcripts suffice at each bit budget; never credit choices made with accidental access to the hidden sign.
- **Old-task retention check:** Couple the wrong partner choice to A failure in one world; require abstention or a successful discriminating check and verify C and both supplier tasks in the other.

#### 20. Separate new room from borrowed room
- **Mechanism:** Fix a blinded mixed stream of disjoint, competing, and impossible consumers. Score the net usefulness of admitted frozen writes, charging opportunities lost because a supplier occupied capacity or a consumer consumed a shared effect.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is a stricter evaluation of the parent's non-borrowing room and task-arithmetic interference, not a new mechanism for measuring rank.
- **Cheapest first test:** Use one world where either of two support options blocks a different unrelated later consumer and a control world where the support is genuinely reusable. Compare at fixed rank, bytes, and released capacity.
- **Old-task retention check:** After each admitted write measure the number and identity of intact old tasks, including all earlier consumers; compare worst-prefix retention and not just the last checkpoint.

#### 21. Compile away the proposed interface
- **Mechanism:** Translate learned offers into ordinary causal links and effect predicates; let the strongest planner call the same local solvers and verifier to select or request alternatives. Establish what, if anything, cannot be reproduced at equal cost.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is a kill test against Ma-STRIPS, Pacti and APRNN, not a primitive. A tie on fixed menus is expected; only proposal synthesis under matched information could separate the arms.
- **Cheapest first test:** Exhaustively compare fixed-menu arms first; then expose both arms to the same local proposal budget in the blinded E2 and private-composition settings. If savings are only cached proof checks, relabel accordingly.
- **Old-task retention check:** Use identical A/C/B/F certificates and held-out tasks for both arms; count rejected unsafe prefixes and every failed attempted publication.

#### 22. Require refusal when useful transfer is impossible
- **Mechanism:** Present an incompatible E2 guard, a satisfiable guard paired with an ineffective frozen payload, and a successful composition that an intervening acquisition invalidates. Report infeasibility, failed usefulness and stale evidence separately.
- **Novelty vs nearest prior art — IMPROVEMENT:** Certified CL and SpecRepair already bound claims by a spec. This audit prevents transfer success from being inflated by changing the goal, refitting, or treating admission as task completion.
- **Cheapest first test:** Enumerate the three negative cases and one positive, then vary the intervening acquisition without changing old margins. Check the false-positive and abstention rates against the live oracle.
- **Old-task retention check:** Protect the intervening task as well as A/C and both suppliers; check all retained tasks again on the positive case after consumption.

## Ranked deeper questions

1. **Does a learned effect help an editor whose payload, objectives and guards were genuinely unknown when the provider committed?** Start with 01 → 07 → 08. Demand additional useful, independently proved E2 admissions at matched old service, rank, margins, and work; first show the holdout offers enough feasible variation to distinguish methods.
2. **What is the smallest checked offer that lets private suppliers learn a safe composition rather than merely report one?** Start with 09 → 10 → 19. Include an undoing cross-effect, a pair with no legal ordering, and an equal-information planner/local-solver baseline; use the disclosed optimum only to locate the coordination gap.
3. **Does complementary establishment produce an effect that remains useful after the original pending consumer has gone?** Run 17 → 06 → 20. Contrast reuse on reset copies with sequential consumption; debit capacity, invalidation and useful unrelated writes displaced.
4. **Which improvement remains after compilation into planning, repair, and incremental verification?** Run 21 → 18 → 22. Separate changes in reachable safe states from proof coverage and solver costs. A planner that ties at matched information and work kills the primitive claim even if private coordination still succeeds.

**Verdict:** Establishing open conditions and combining partial effects are known planning operations. The candidate CL contribution is learned room that independently produced frozen writes can use, or that private suppliers can jointly make without losing old service, at lower cost or greater useful coverage than the same-information planner–repair–verifier stack. The decisive first result is extra useful E2 admissions after B is committed, not an increase in source guard scores or an attractive proof for one planned sequence.
