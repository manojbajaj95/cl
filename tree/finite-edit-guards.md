# Finite edit guards

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Unannounced consumers](unannounced-consumers.md) ([PR #162](https://github.com/manojbajaj95/cl/pull/162)), cards 05 and 10. **Review seed:** [Flood triage row 259](https://github.com/manojbajaj95/cl/blob/5f0cd868f2b68d032a339cd7024c22acba7cb706/reviews/flood-triage.md#L259) kept two directions at 3: guarantee an old task's response to finite gate-crossing future edits, and establish a precondition that lives in the product of two suppliers' ranges. Grading follows the [idea ledger](https://github.com/manojbajaj95/cl/blob/5f0cd868f2b68d032a339cd7024c22acba7cb706/reviews/idea-ledger.md).

**Is a guarantee about reactions to future edits a new object for continual learning?** Not as a mathematical object. It is the preimage of an old-task safe set under an edit relation. [InterContiNet](https://arxiv.org/abs/2206.07996) already learns nested weight regions that guarantee retention within the region, and [Pacti](https://arxiv.org/abs/2303.17751) already composes assume–guarantee contracts. The CL candidate is a *learned, reusable edit-facing guarantee*: an ordinary useful write establishes (or two independent writes jointly establish) a checkable promise that later, independently authored useful edits can invoke unchanged. It must let in more useful writes or cost less to use than the best combination of finite verification, relational planning, and constrained training at the same retention. Renaming a safe set or speeding up a solver does not establish a new primitive.

## What the guard promises

Let A have an old input/label domain D and an acquisition-anchored floor τ on a declared score m (start with the signed classification margin, including the tie rule). For host state s and a typed family T of bounded edits, the reaction floor is

```text
R_A(s, T) = inf { m_A(e(s), x) : e ∈ T, x ∈ D }.
Guard_A(T, τ) = { s : R_A(s, T) ≥ τ }.
```

The score is the *post-edit level*, not merely change relative to a potentially degraded host. For additive edits this guard is the erosion of the old safe set by the edit family; for stateful edits it is a universal precondition. The proposed artifact binds D, τ, the host version or proved starting envelope, the edit semantics and bounds (including optimizer state if read or written), and a checkable proof. A child family can reuse the proof only after checking inclusion in **actual edit effects**, not by matching a name or radius. The one-call guarantee covers endpoints when publication is atomic. If updates serve intermediate states, quantify over every served prefix; multiple calls require a residual guarantee or a new proof. No claim outside D or T, and no admission on a failed or unknown proof.

Two paper witnesses show where a first-order contract or additive planning can lose information; neither demonstrates learning.

1. **Same outputs and Jacobians, different finite reactions.** For one rare A slice let the margin after adding t to an editable bias be `1 − ReLU(t − q)`, with t in [0, 1]. At t = 0, hosts with q = 1/4 and q = 3/4 agree on the margin and its local derivatives; the affected gate is dormant in both. Both cross it. The exact floors are 1/4 and 3/4, so only the latter guarantees τ = 1/2. Start the test with a utility-matched B choice that can change q and an unrelated old task C; in learned variants match old logits, margins and the relevant Jacobians before editing. A valid nonlocal remainder bound can distinguish the hosts; the shared first-order data alone cannot.
2. **Only the product establishes the promise.** Let the rare A margin be `1 − ReLU(t − 1/4) + uv·ReLU(t − 1/4)` on the same family, with u a feature gain and v a signed readout. The guard at τ = 1/2 is exactly `uv ≥ 1/3`. Start at u = v = 0. A useful B write certifies u in [2/3, 1], and an independently useful F write certifies v in [2/3, 1]; each singleton has floor 1/4, but together the worst floor is 7/12. The passing pairs (1/3, 1) and (1, 1/3) have a failing crossed pair (1/3, 1/3), so no single conjunction of unary guards represents the full passing relation. An opposite-sign pair with the same magnitudes fails. The interval multiplication is sound only if both offers apply to the same deployed version, slice, and edit semantics and survive the actual write order. For a sharper control, pairs of signs (+,+)/(−,−) and (+,−)/(−,+) have identical marginal ranges but opposite products; exploit the tighter joint support only if its coupling is proved.

## Closest controls and the common first test

- **Finite retention:** [Adapter compatibility contracts](https://github.com/manojbajaj95/cl/pull/117), [OGD](https://arxiv.org/abs/1910.07104), and [GPM](https://arxiv.org/abs/2103.09762) provide local response or directional controls. [Certified CL](https://arxiv.org/abs/2407.06697) carries verification evidence into retraining; [CABA](https://arxiv.org/abs/2610.40740) checks candidates on historical anchors with conditional off-anchor bounds; [Certified Mechanistic Edits](https://arxiv.org/abs/2610.03502) certifies specified edits across input regions. Compare InterContiNet, [Finite safe regions](finite-safe-regions.md), and [APRNN](https://arxiv.org/abs/2304.03496) on the *same* write family with equal old specifications. Give finite baselines gate crossings too.
- **Composition and anticipation:** [UCPOP](https://homes.cs.washington.edu/~weld/papers/ucpop-kr92.pdf) already solves open preconditions and checks threats; Pacti is the relational control, not an additive straw man. [La-MAML](https://arxiv.org/abs/2002.09571) trains for later learning. The strongest simple stack is relational planning with the same effect language plus APRNN-style constrained repair and incremental verification. Also compare exact joint training with both suppliers' data as a paid ceiling, and frozen expansion under the same capacity cap. Local product bounds, restricted edit families, and training against imagined changes are not novelty by themselves.
- **First gate (proposed, CPU only):** Start from the rational witnesses, then use tiny ReLU hosts with finite useful menus and exhaustive verification. On continuous families start with one editable bias and partition its interval exactly; do not assume multi-layer edits are affine within a fixed gate pattern. Hold out A slices for empirical coverage, and freeze an independent editor E2's payload from a pre-provider reference before B/F commit. Publish the family, not the held-out payloads. Include no-crossing, sign-reversal, interference, and impossible cases. Keep B/F utility, retained capacity, old inputs and allowable edits matched. Score useful frozen writes admitted at the same A/C floor and B/F progress; charge training, proof and verification work, stored bytes and inter-supplier disclosure. Count unknown separately from unsafe. Audit normal A and C plus already-installed B/F at every served prefix; report declared worst-case and independent old-task accuracy separately. An empty or useless family passes no gate.

## Idea cards

### Learn what a future edit will do

#### 01. Measure the blind spot of a perfectly matched tangent
- **Mechanism:** Sweep dormant-gate thresholds across an edit interval using hosts matched on current logits, margins and Jacobians. Move the first crossing without changing any local Taylor coefficient.
- **Novelty vs nearest prior art — IMPROVEMENT:** PR #117 already protects first-order write response; this measures exactly when it ceases to identify finite safety rather than proposing another local penalty.
- **Cheapest first test:** Enumerate the first witness and an affine negative control; compare tangent, validated remainder and exact finite-region decisions at equal B utility.
- **Old-task retention check:** Check normal A/C and each rare A point at every breakpoint and endpoint; separate floor failures from label flips.

#### 02. Train B to pass the blind editor's family guard
- **Mechanism:** While learning B, optimize a sound lower bound on A's response over development edit families. Lock B before evaluating a predeclared held-out family and exporting its checked floor. E2 picks a frozen useful payload without seeing the descendant.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** La-MAML optimizes future learning and InterContiNet learns safe regions. The candidate is a learned floor that a blind writer can actually invoke, at better admission or cost than either method plus the same verifier.
- **Cheapest first test:** Learning B must leave a choice of gate thresholds. Compare ordinary B training, margin bonus, matched-box robust training and all-constraints repair; hold out an editor and a write direction.
- **Old-task retention check:** Match starting A margins and B competence, certify every admitted family member on A and C, and recheck all tasks after actual E2 publications.

#### 03. Put the slack on the far side of the gate
- **Mechanism:** Learn a compensating branch that activates only in cells where the original branch becomes insufficient. Give the solver the shared edit variable so it does not minimize both branches under contradictory gate assignments.
- **Novelty vs nearest prior art — IMPROVEMENT:** APRNN and correlated verification can already handle such dependencies. Ask whether learning selective compensation buys useful edits over an equal-width box-trained or gate-pinned net.
- **Cheapest first test:** Use a single bias with two gates. Compare aligned compensation, an extra always-active unit, and exact repair using the same units and B data.
- **Old-task retention check:** Verify both sides and the switching point, including old examples read by the extra branch but not targeted by B.

#### 04. Teach the location of a hazard, not the current output
- **Mechanism:** Allow a student or compressed host to change its internal gates, but distill the teacher's finite guard decisions on development families, with failing edit/input pairs as training targets. Reprove at the student.
- **Novelty vs nearest prior art — IMPROVEMENT:** Distillation and Certified CL's certificate-guided data synthesis are controls. The different target is preserving acceptance of future writes through compression, not reproducing present predictions.
- **Cheapest first test:** Compress a two-gate teacher to width one or two. Compare replay, derivative distillation and counterexample synthesis; withhold a family of gate-crossing edits.
- **Old-task retention check:** Independently verify every preserved acceptance, and measure A/C accuracy before compression, after compression and after consuming an accepted write.

#### 05. Spend limited certificates on the old task's real scoring rule
- **Mechanism:** For an old task defined by a finite accuracy floor, prove that every edit can violate at most k old decisions, not that the same fixed subset remains correct under all edits. Keep a separate hard floor for rare slices.
- **Novelty vs nearest prior art — IMPROVEMENT:** Certified CL and robust optimization can encode aggregate obligations. The CL question is whether allowing the identity of failures to vary buys plasticity without hiding a collapsed slice.
- **Cheapest first test:** Build three old examples whose failure intervals in t are disjoint. Compare whole-domain count certificates with unions of protected anchors and exact replay at the same accuracy.
- **Old-task retention check:** Enumerate worst accuracy by edit and by slice; allow no repeated spending against a floor reset at each stage.

#### 06. Certify a frozen update rule, not a cloud of deltas
- **Mechanism:** Describe E2 as a bounded state-dependent operator (for example a clipped, one-step rule with frozen input and hyperparameters). Verify only its reachable transitions, rather than a norm ball containing impossible actions.
- **Novelty vs nearest prior art — IMPROVEMENT:** Abstract interpretation and weakest preconditions already handle guarded transitions; La-MAML anticipates update rules. The test is whether operator typing retains meaningful room lost to delta boxes.
- **Cheapest first test:** Use an update whose sign switches on one observed scalar. Compare the exact branch relation to its interval hull and to equal-work per-candidate verification.
- **Old-task retention check:** Check each permitted sign branch, the branch boundary, and A/C after replaying E2 unchanged. Never substitute a post hoc hand-picked action for the rule.

### Establish what neither supplier can promise alone

#### 07. Install a signed product contract with two independent writes
- **Mechanism:** B exports a proved lower bound on feature gain, F exports a signed readout range, and a checker combines them on the same rare slice. Neither exports the partner's task, and E2's finite write stays fixed.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** This is the parent card's product idea narrowed to finite reactions. The proof is ordinary Pacti-style relational composition. The candidate is learning interoperable offers that beat full relational planning with independently fitted suppliers at equal disclosure and B/F utility.
- **Cheapest first test:** Learn both local menus for the product witness. Compare the two singletons, unsigned and additive offers, exact relational planning, and joint factor fitting; plant the same-norm wrong sign.
- **Old-task retention check:** Give A and C existing uses of u or v so either supplier can do harm before E2. Verify every served prefix and all four tasks at E2 publication.

#### 08. Let suppliers learn a common selector without sharing examples
- **Mechanism:** Condition each signed range on a certified public slice key, and verify that both suppliers use the same key under every permitted edit. Their global marginals may be identical whether they help or cancel.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Pacti already handles the keyed relation. The proposed target is a key independently learned against local tasks that transfers to new partners at lower offer cost than exchanging the full relation.
- **Cheapest first test:** Use two slices with the same marginal ranges and swap one supplier's keys. Compare no key, a hand-designed key, matched-size relational offers, and joint training on the same budget.
- **Old-task retention check:** Exhaust A/C in both slices and test that an edit causing key disagreement is refused; check both suppliers' normal tasks after consumption.

#### 09. Learn to preserve a partner's premise while helping your own
- **Mechanism:** Train F against a sound constraint on the post-F range of B's feature, not just a target readout. Publish the range transformation together with its allowed incoming states.
- **Novelty vs nearest prior art — IMPROVEMENT:** UCPOP already checks threats and APRNN can repair them. The gain would be a cheaper *learned* threat-avoiding F with the same B/F performance, not the concept of ordering.
- **Cheapest first test:** Give F two equal-utility options v := 1, with one also halving u. Compare premise-constrained F to ordinary F plus backtracking and to full relational repair; enumerate both orders.
- **Old-task retention check:** Check A/C after each successive write and E2, and reject a formerly proved F offer if its incoming envelope no longer applies.

#### 10. Choose a small basis for cross-terms
- **Mechanism:** For a consumer margin containing a term such as uᵀMv, learn supplier coordinate maps exposing a few shared modes; prove a worst-case bound for the discarded terms before admitting E2.
- **Novelty vs nearest prior art — IMPROVEMENT:** Low-rank factorization and [McCormick relaxations](https://doi.org/10.1007/BF01580665) already bound bilinear problems. The bet is that a learned offer basis beats an equally compact generic relational sketch at certifying real useful writes.
- **Cheapest first test:** Use rank-one, rank-two and dense hidden interactions and a fixed offer budget. Compare SVD, interval/McCormick bounds, and exact rational enumeration.
- **Old-task retention check:** Plant a rare A failure entirely in a low-energy discarded direction. Check the exact score and normal A/C/B/F performance; refuse if the remainder cannot be certified.

#### 11. Reserve one joint setting for multiple unopened consumers
- **Mechanism:** Select B/F offers whose *same deployed pair* satisfies several published reaction families. Train against the intersection, not a separate best pair for each later consumer.
- **Novelty vs nearest prior art — IMPROVEMENT:** Relational planning and robust optimization already enforce this quantifier order. The CL target is how cheaply local tasks can create such reusable overlap before any payload is shown.
- **Cheapest first test:** Two families require opposite signs of uv; contrast a model with one slot against a two-slot model under a fixed capacity budget, and compare joint planning at equal work.
- **Old-task retention check:** Audit A/C across both family calls separately and after successive calls. A promise for both from the same state is not a promise for their composition.

#### 12. Train for partners selected after publication
- **Mechanism:** B and F each learn against a public schema and a set of development partners. Commit before choosing a held-out compatible partner; the assembled pair must prove a product guard without any supplier refitting.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [TIES](https://arxiv.org/abs/2306.01708) and Pacti are merging and contract controls. The bet is learned interchangeability of independently useful *guarantees*, not merely averaging compatible models.
- **Cheapest first test:** Train two pairs on private synthetic tasks sharing a public signed-range schema. Swap partners, freeze E2, and compare to shared initialization plus TIES and a relational planner, at equal capacity and disclosure.
- **Old-task retention check:** Verify each advertised cross-pair on old A/C and both local tasks; include a deliberately incompatible held-out partner and record refusal.

### Make guarantees survive use

#### 13. Compile a residual guard after one edit consumes room
- **Mechanism:** After a concrete E2 write, publish a checked remaining menu of E3 writes from the new state, distinguishing the reusable part of the family from edits that consumed slack.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** This is a residual of a safe-word language, already expressible by predicate transformers. The proposed CL artifact earns its keep only if another editor can reuse it more cheaply than replanning from the same post-E2 state.
- **Cheapest first test:** Build two equally useful first writes, one of which exhausts a gate buffer necessary for the next step. Compare proof reuse, fresh exact verification and a scalar remaining-budget rule.
- **Old-task retention check:** Enumerate all advertised two-write sequences and check A/C between writes, including repeated application of the same safe singleton.

#### 14. Train a bounded winning strategy, not a safe sequence
- **Mechanism:** Backward-solve a short game: at each step a foreign editor chooses a bounded frozen payload, then the host may select a verified accommodation from its finite menu. Train B to reach a state with a nonempty winning strategy.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Robust control and contingent planning already solve such games; the CL candidate is a learned state/output whose strategy can be invoked by independent editors at useful scale. A response is allowed only when the same response menu is available to all controls.
- **Cheapest first test:** Use a two-round game where incompatible first accommodations have identical immediate utility. Compare myopic guards and generic contingent planning on the same moves.
- **Old-task retention check:** Enumerate every reachable branch and served prefix on A/C, plus normal B/E2 task performance; no safety credit for refusing required in-scope moves.

#### 15. Carry a guard into a different editor language
- **Mechanism:** Prove that a batch of frozen low-rank payloads maps into a previously certified effect family on the current host; carry the proof across editors only for the part whose effect inclusion is checked.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Finite safe regions](finite-safe-regions.md) already proposes transport between writer coordinates. Here test transport across independently produced operators, where equivalent parameter payloads can differ if optimizer slots or write order are involved.
- **Cheapest first test:** Give one editor additive payloads and another quantized factors. Include identical current weights with different optimizer slots; compare exact re-verification and inclusion with and without state semantics.
- **Old-task retention check:** Independently check A/C at every transported call and at the next update that can expose hidden-state divergence.

#### 16. Separate proofs for live paths and shadow jumps
- **Mechanism:** Let a writer attach an endpoint guarantee and optionally a separately proved trajectory. Learn or choose a continuation allowed to cross gates on a shadow copy when a safe live path is unavailable.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Finite safe regions](finite-safe-regions.md), consistent rollout and [Mode Connectivity](https://arxiv.org/abs/1802.10026) already separate feasible endpoints and paths. The question is whether explicitly exposing both modes buys useful future writes under a fixed shadow-space budget.
- **Cheapest first test:** Use an old margin with two safe edit endpoints and an unsafe interior; compare atomic-only, live-only and a mixed planner, with equal memory and utility checks.
- **Old-task retention check:** Check all externally served versions, including C during cutover. Never infer safety along a path from its endpoints.

#### 17. Bind a certificate to the premise that actually matters
- **Mechanism:** Store a checked dependency slice for each proof. A later write that provably leaves those terms and their reachability unchanged can transport it, while an output-preserving change to a dormant gate can invalidate it.
- **Novelty vs nearest prior art — IMPROVEMENT:** Certified CL already has incremental certificate reuse. Target invalidation of counterfactual reaction proofs rather than current-task certificates; charge for establishing the dependency slice.
- **Cheapest first test:** Alternate writes to irrelevant hidden units with edits shifting a dormant threshold. Compare exact recomputation and incremental verification with dependency tracking.
- **Old-task retention check:** Replay stale and fresh proofs against exact A/C floors; verify that the stale proof is not accepted even if all passive old logits are unchanged.

#### 18. Certify one real update while collecting witnesses for the next
- **Mechanism:** When verification of a development edit fails, minimize an edit/input counterexample and use it to target a choice of B features. Acquisition-time old examples need not convey which gate threshold is fragile.
- **Novelty vs nearest prior art — IMPROVEMENT:** [SpecRepair](https://arxiv.org/abs/2106.01917) already uses counterexamples to guide repair. Only cross-editor transfer from a compact witness cache, not CEGIS itself, would be new evidence.
- **Cheapest first test:** At equal verifier calls and storage, compare storing failing edit/input pairs, storing their inputs only, and a fresh counterexample-generating solver on held-out editor families.
- **Old-task retention check:** Check independent old A/C inputs and every declared rare slice after each B commit and after E2. Cache hits cannot authorize a write.

### Try to erase the novelty

#### 19. Ask how many bits an exact product offer needs
- **Mechanism:** Use n public slices and n F follow-on edits. Edit i makes only slice i's margin depend on the sign of B's i-th feature; every other slice retains its original route. B's feature magnitudes are fixed at one, but the n admission answers recover all n signs. An exact standalone message that answers every query without host access thus needs at least n bits in the worst case.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is an indexing argument, not a new lower-bound method. It sets a budget floor for standalone supplier summaries and isolates when correlation or abstention is necessary.
- **Cheapest first test:** Enumerate every sign vector for small n; compare a packed exact message, keyed low-rank offers on structured signs, and bounded interactive queries. Charge host queries separately rather than applying the standalone bound to them.
- **Old-task retention check:** Every claimed admission must pass A/C on the queried rare slice and ordinary slices; report false rejection and unknown rates under the bit budget.

#### 20. Compile the whole interface into an ordinary verifier
- **Mechanism:** Express the proposed artifact as explicit state, edits and postconditions. Run the same candidates through an exact finite oracle and an incremental relational planner without any bespoke guard objects.
- **Novelty vs nearest prior art — IMPROVEMENT:** Pacti plus APRNN is a direct null hypothesis. If ordinary planning with the same learned choices matches reuse cost and admission, the artifact is an interface convenience.
- **Cheapest first test:** Exhaust the same menus in a quarter-grid ReLU host, preserve identical proof premises and compare total paid work as independent consumers arrive.
- **Old-task retention check:** Compare each implementation's admitted states against exact A/C/B/F thresholds at every served prefix; require exactly the same floors, not comparable averages.

#### 21. Remove any advantage purchased by narrowing the edit family
- **Mechanism:** Hold a blinded candidate bank constant and report certified useful acceptance against that bank, including out-of-contract misses, rather than only coverage within a learner-chosen family.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is a selection-bias audit of InterContiNet or any guard-learning method, not a new certification technique.
- **Cheapest first test:** Compare a narrow certified box, a larger typed family, and equal-capacity frozen expansion on the same frozen candidate bank; include candidates requiring shared writes.
- **Old-task retention check:** Check ordinary A/C on every actual candidate accepted and audit all covered gate-crossing cells. Report new-task utility of rejects rather than hiding it behind zero forgetting.

#### 22. Force a genuine incompatibility and demand a useful refusal
- **Mechanism:** Construct a case where every B/F pair that meets both local floors fails the finite guard. Return a checked failure witness or a sound infeasibility proof; distinguish solver unknown from either.
- **Novelty vs nearest prior art — IMPROVEMENT:** CEGIS and infeasible-core extraction are known. The value is a negative control against claims that adding capacity, selecting easier consumers, or quietly weakening old-task floors solved the problem.
- **Cheapest first test:** Force v < 0 for every F solution and u > 0 for every B solution in the product witness. Compare normal fail-closed verification with diagnosis that points to the smallest incompatible premises.
- **Old-task retention check:** Verify A/C remain at acquisition floors on the unchanged live state and that no refused payload or supplier combination is ever served.

## Ranked deeper questions

1. **Can a learned finite reaction guarantee buy blind transfer beyond existing finite CL?** Start with the matched-tangent witness, then card 02 against InterContiNet, exact finite-region verification plus constrained training, and PR #117. Demand more *useful frozen* E2 writes at equal old floors, B utility and budgets, or the same admission at lower total cost. A hand-built separation or faster proof alone is insufficient.
2. **Can useful independent suppliers learn a productive coupling at fixed disclosure?** Start with cards 07–08 and 12: no singleton admits E2, the correct pair does, and a matched-magnitude wrong sign or wrong key is refused. If full relational planning fed the same offers ties, the claim is learning compatible offers if demonstrated, not a new composition rule. Joint fitting is a ceiling, not evidence for independence.
3. **What must a reusable guarantee remember after it is used?** Cards 13–14 and 17 ask whether compact residuals or short strategies let independent editors keep A/C safe over later prefixes without reconstructing every old obligation. A tie with generic contingent planning at equal work demotes it to engineering.
4. **Where is the boundary between a useful object and a renamed verifier?** Use the compile-away, usefulness and impossibility controls (cards 19–22) to vary gate density, disclosure, and independent write count. If the benefit disappears when the oracle sees the same learned state and contract language, keep the empirical improvement but drop the primitive claim.
