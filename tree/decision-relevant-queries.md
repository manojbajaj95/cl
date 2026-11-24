# Decision-relevant queries: buy only the future distinctions that change a repair

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Correction classes](correction-classes.md) ([PR #169](https://github.com/manojbajaj95/cl/pull/169)), cards 06 and 23. **Review seed:** [Flood triage row 270](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/flood-triage.md#L270) retains both at score 3: query a continuation only when competing repair hypotheses imply different deployable witnesses on pending frozen demand, ranked by repair cost saved; factor a witness's success relation over continuation coordinates only with evidence, and patch local interactions when the product fails.

## Is a learner that buys only decision-changing knowledge about its future a new CL object?

**Not because it buys information selectively.** Expected value of sample information (EVSI) already asks whether an observation is worth changing a decision for, and factored models already exploit and refine conditional independence. The candidate CL object is **a reusable, scoped certificate of which training witness to spend**: it lets a learner skip learning distinctions in its own future adaptation, makes that omission testable on independent frozen edits, and can withdraw just the affected claims when a continuation exposes an interaction. If a decision-theoretic query policy, ordinary factored verification, and a matched repair store accomplish the same thing at the same cost, this is a useful stack, not a new primitive.

### What gets bought

- **Freeze the demand and the decision.** Lock the editor's payload, new-utility target, allowed accommodations and served-prefix schedule before planning. A decision is to apply a named training witness, buy a lawful fallback repair, or withhold the edit. Pay for refusals in lost utility; keep A/C safety floors hard, not exchangeable for cheap queries. Include relevant learner, optimizer and sampler state in the scope. A continuation query observes a lawful shadow run, check or source response; it does not request a changed payload, relax a check, or itself license service. For the primary one-step rule, compare hypotheses on *pending* offers, not on invented later demand.
- **Separate repair truth from decisions.** The parent's correction class compares full sets of successful witnesses. Here two hypotheses may disagree about those sets yet recommend the same deployable witness; that is a reason not to query now, not a reason to merge the classes. Use one common tie-break, including a stable preference for an already verified incumbent when costs tie. If hypotheses have different winners but the query cannot distinguish them or no answer can change what the checker permits or what the router would choose, skip it. Unknown is neither a failure nor a deployable witness. If the only change would be whether a single named witness can be authorized at all, account for that as a verification/admission decision with its own baseline rather than as evidence of choosing between two witnesses.
- **Price the useful distinctions.** For matched target utility, let `V(b)` be the cheapest expected downstream repair cost at belief `b`, with hard retention and verification constraints and a priced safe fallback. Rank eligible queries by `V(b) − E[V(b | answer)] − cost(query)`; the first difference is gross repair cost saved. Include witness acquisition, fitting, recertification, and paid repetitions, and charge delay separately or in a declared common unit. Report raw units alongside the scalar price. This is one-step EVSI, not an optimal multi-query policy. For a joint experiment, apply the same screen to the whole lawful bundle; no individual answer in it need suffice. For later horizons, name the committed demand distribution and its expiration; otherwise call extra querying exploration, not knowledge bought for pending demand.

**Paper case.** Two equiprobable repair worlds need different cheap witnesses (`w+` or `w−`, cost 1) for a frozen demand; a verified universal witness costs 9. An 8-answer query about an independent nuisance predicts no useful decision even though it yields 3 bits. Assume learning the sign is the only cheaper way to authorize a specialist: trying it in shadow without revealing the sign does not establish coverage. A fair 1-bit sign query (cost 2) reduces gross repair cost by 8 and net cost by 6 because its answer lets the independent checker establish the cheap witness. If cheap trial-and-check is available, it belongs in the comparison and may erase the savings. If a second held-out family can use the same artifact, charge its verification and count the avoided acquisition only when it is actually avoided.

### What can be factored

For the same refusal, scope and **single witness** `w`, let `S_w(x,y)` mean that applying `w` on the continuation with coordinates `x,y` admits the frozen offer and respects all old obligations at served prefixes. On the declared legal support, try `S_w(x,y) = P_w(x) ∧ Q_w(y)`. Model legality separately. Independent sampling of coordinates, two successful marginals, or combining two witnesses selected independently does not establish the equation. For example, a shared optimizer slot can make a jointly legal cell fail even when each one-coordinate run succeeds. A product of different witnesses is a different intervention.

To see the gap on two binary coordinates, suppose `w+` passes on `00, 01, 10` and fails on `11`, all legal. The first three cells are consistent both with an all-pass product and with a missing corner. A law that isolates training updates *and* all old checks across blocks may prove the product; otherwise untested cells stay provisional and need independent verification before use. If the checker exposes the missing corner, suspend the affected claim, add a versioned joint predicate (here `¬(x=1 ∧ y=1)`), and keep the rest only where the original proof still applies or direct verification supports it. A patch may remove a false approval or, with evidence, admit a previously excluded cell. Do not infer that a single observed counterexample has localized the dependency. When the region is unclear or exceptions spread, expand the recheck or fall back to a flat table. Balance the bytes and proof work of patches against the cost of rebuilding.

### Prior art and shared test contract

- **Decisions vs. labels.** [Howard's information value theory](https://doi.org/10.1109/TSSC.1966.300074) and [Bayesian experimental design](https://doi.org/10.1214/ss/1177009939) anticipate utility-based experiment selection. [Decision-focused learning](https://arxiv.org/abs/1809.05504) optimizes predictions for downstream decisions; version-space active learning and [DAgger](https://arxiv.org/abs/1011.0686) supply disagreement and learner-state query baselines. Compare random, entropy, version-space, DAgger-style state targeting, and exact finite EVSI with the same query menu and budget. Also give the exact solver the same state, costs, persistent evidence and horizon when testing whether anything is gained beyond an efficient implementation; do not promise to beat an oracle optimizing the identical problem.
- **Splits vs. composition.** Myhill–Nerode and [Angluin's L*](https://doi.org/10.1016/0890-5401%2887%2990052-6) concern equivalence and distinguishing suffixes, not necessarily decisions tied to changing prices or witness menus. CEGIS, [CEGAR](https://doi.org/10.1007/10722167_15) and [neural repair](https://arxiv.org/abs/2301.11342) already refine from counterexamples; [factored MDPs](https://www.jmlr.org/papers/v3/guestrin03a.html) and assume–guarantee verification already use local dependencies and contracts. Compare a full product table, factored abstraction with counterexample refinement plus matched repair, and [GCR](https://arxiv.org/abs/2111.11210) and pooled [MTT](https://arxiv.org/abs/2203.11932) at equal evidence and storage. The full table can supply offline truth but is not given free to online arms.
- **Ledger rules.** Following the [idea ledger](https://github.com/manojbajaj95/cl/blob/f236e3c105b840ad57c145494f36e3a17d7b492e/reviews/idea-ledger.md), compare against the best stack of the parts, not weak components; use exact or split-half-checked truth, match margins and new-task progress, and neither assume sparse interference nor credit the author of identical evidence. Charge queries, delay, training, proof/search work, and peak and retained bytes (witnesses, factors, patches, receipts). Hold out whole editor families and legal joint continuations. Report admissions over **all** frozen offers, with lost utility from abstention and unknowns. Keep an independent verifier at each actual admission and measure ordinary old-task A and C on withheld data at every served prefix, against both acquisition and pre-edit references, including rare slices and rollback. Do not count a clean refusal as retained utility from an admission.

## Idea cards

**P** = conditional primitive candidate, only if the proposed reusable object or operation beats the matched stack. **I** = improvement or audit of an existing method. All first tests are paper or CPU designs, not results.

### Spend evidence where it changes a witness

#### 01. A receipt that pays for two blind editors (P)
- **Mechanism:** Store the cheapest checked distinction as a receipt linking an answer, a scope, and the witness the answer makes worth deploying. Spend it on a later frozen editor without requerying or copying the first payload; independently verify the new application.
- **Novelty:** EVSI selects the question, and case-based repair stores the fix; the candidate is a reusable, independently checkable justification for spending that training artifact across editors.
- **Cheapest first test:** Extend the sign paper case with two blind editor families and a high-entropy nuisance. Compare exact EVSI plus a repair/result cache, random, entropy and version-space acquisition on the same query menu; falsify if caching the answer and repair suffices.
- **Old-task retention:** A needs the correct sign; make both cheap witnesses capable of harming a held-out C slice in the wrong host. Check both editors at every served prefix.

#### 02. The cheap fallback that makes a question worthless (I)
- **Mechanism:** Price the best verified common witness before consulting disagreement. Cancel a queued query if a newly reusable witness removes its net savings.
- **Novelty:** This is EVSI with a changing action set, not a new active-learning rule.
- **Cheapest first test:** Lower the universal witness price in the paper case from 9 to 2, then reverse the change. Compare rank-by-disagreement and exact EVSI under the same deadlines.
- **Old-task retention:** Give the universal witness an intermediate C hazard so cancellation is allowed only when it really passes the served-prefix checker; verify A under both signs.

#### 03. Ask about a block of repairs, not a single label (I)
- **Mechanism:** Rank queries by joint repair savings on a pending queue, with fixed acquisition costs paid once and per-application checks charged each time.
- **Novelty:** Batch experimental design and facility location already price shared setup; this tests whether the induced witness reuse is material on CL demand.
- **Cheapest first test:** Enumerate five offers with one reusable witness and one lucrative singleton. Compare per-offer EVSI, exact joint EVSI, and the best repair-store-plus-scheduler stack; include a case where joint ranking gives no gain.
- **Old-task retention:** Test A/C in both queue orders, including a C slice affected only after the second application of the shared witness.

#### 04. A two-answer lock (I)
- **Mechanism:** Treat a pair as one query when no individual answer changes the witness and a legal pair jointly separates the relevant deployment decisions.
- **Novelty:** Decision-dependent interaction and nonmyopic EVSI already predict complementarity; the audit identifies a limit of the single-query rule.
- **Cheapest first test:** Choose the witness by XOR of two fair bits. Compare greedy singleton EVSI to exact two-step policy and one costly direct query.
- **Old-task retention:** Both parity classes must pass A and a separate C test after the realized repair; unanswered cases pay the safe fallback cost.

#### 05. A stopping proof that lets the learner forget (P)
- **Mechanism:** Retain a scoped proof that unresolved distinctions cannot improve the current repair decision by more than a bound. Discard their detailed tables and explicitly invalidate the proof on new menus or horizons.
- **Novelty:** Branch-and-bound and value-directed compression already certify negligible distinctions. The conditional object would be a compact deletion license reusable across independent adaptation requests without reading discarded answers.
- **Cheapest first test:** Exhaust a finite library of nuisance dimensions, physically remove the columns, and send blind editors inside and just outside scope. Compare persistent EVSI with memoization and a byte-matched repair cache.
- **Old-task retention:** Include an out-of-scope editor that moves a C margin without changing A's route; require safe fallback and measure both before and after reacquisition.

#### 06. A distinction that expires before the answer arrives (I)
- **Mechanism:** Quote repair savings at the actual answer time; if an editor's deadline passes first, route to the verified fallback instead of hoarding the answer for the expired offer.
- **Novelty:** Sequential decision theory handles deadlines; the test concerns the value of a delayed continuation answer versus fitting or reusing a witness now.
- **Cheapest first test:** Three asynchronous offers, two query latencies and one reusable repair. Compare immediate EVSI, earliest deadline, and exact scheduling with time-priced observations.
- **Old-task retention:** Evaluate ordinary A/C during the wait as well as at repair, and record missed utility when a deadline is crossed without serving.

#### 07. Spend one query on the disagreement about *why* (I)
- **Mechanism:** Compare two matched shadow suffixes that agree on the failed check but differ on whether the candidate witness or a changed optimizer slot caused it.
- **Novelty:** Paired interventions and counterexample minimization already isolate causes; requiring a witness decision to change is a test of whether that isolation repays its cost.
- **Cheapest first test:** Tiny momentum learner with matched weights and two slot histories, plus equally informative nuisance probes. Compare pair queries, random boundary examples and DAgger-style sampling with identical oracle access.
- **Old-task retention:** Test A/C on both histories, including a held-out C input sensitive to the momentum tail rather than to the diagnostic check.

#### 08. The verified tie that should not buy a bit (I)
- **Mechanism:** Collapse query proposals that only swap tied, already verified winners; keep a separate ledger entry if a new price or checker changes the tie.
- **Novelty:** Decision equivalence under a stable tie-break is standard; this audit isolates false savings due to witness names and solver nondeterminism.
- **Cheapest first test:** Permute IDs and solver enumeration order on a finite `{a,b}` repair table, then change true acquisition costs. Compare against a canonical winner router and exact EVSI.
- **Old-task retention:** Check A/C for both tied witnesses and after the price change; a witness with a hidden C miss is not an operational tie.

### Earn the product, then contain its failures

#### 09. A product certificate for one actual witness (P)
- **Mechanism:** Combine separate training-transition and old-check guarantees into a product for a single named witness, with a distinct legal-support guard. Export it to independent frozen offers with the same verified interface.
- **Novelty:** Assume–guarantee verification already composes proofs; the candidate is amortized reuse of a learned training artifact together with its composition scope, beyond ordinary contracts plus pooled repair.
- **Cheapest first test:** Two block-diagonal linear learners, one shared example and unseen legal joint cells, then introduce a coupled batch. Compare full table, factored abstraction plus repair, GCR and pooled MTT; count proof and training work.
- **Old-task retention:** Assign A/C to separate blocks and add a rare mixed input. Include its check in the proof for any region claimed to cover it, and evaluate it independently on the held-out cells.

#### 10. Missing-corner repair without reminting the table (P)
- **Mechanism:** Buy the cheapest checked joint cell likely to overturn a deployed winner; if it does, quarantine the unverified neighborhood and replace only the implicated rectangle with a proved guard and verified fallback.
- **Novelty:** Factored CEGAR already refines locally. The candidate is selective withdrawal of one learned witness's reuse rights while retaining separately proved rights elsewhere, rather than global refit.
- **Cheapest first test:** Grow the paper grid and inject a hidden local coupling and a diffuse one. Compare against standard factored refinement plus a memoized repair store, full product rebuild, and unpriced patch accumulation.
- **Old-task retention:** Use an interaction that harms a rare C slice only in the missing corner and a different A failure elsewhere; verify patched and unaffected regions separately.

#### 11. Price a new interaction column against a new witness (P)
- **Mechanism:** When the product fails, compare buying a joint guard that routes the existing library against buying a truthful training witness that makes the guarded distinction unnecessary.
- **Novelty:** Abstraction refinement changes the description, while repair changes the system. The proposed reusable operation is choosing which layer to correct for subsequent frozen offers under the same verification budget.
- **Cheapest first test:** Two otherwise identical grids: one has a cheap witness that fixes an entire coupling family, the other has only cheap guards. Compare exact joint selection with the strongest stacked guard-refinement and pooled-condensation baselines.
- **Old-task retention:** Guarding must preserve old checks along fallback; retraining must pass independent A/C in both the repaired block and an untouched block.

#### 12. A shared optimizer slot is a third coordinate (I)
- **Mechanism:** Condition local success on the shared slot or clock before declaring independence; keep a narrow interaction term if conditioning cannot remove the effect.
- **Novelty:** Factored state and context-specific independence already recover dependencies from omitted variables; this tests whether the proof stays cheaper than a flat repair table.
- **Cheapest first test:** Hold weights fixed, toggle one momentum component and evaluate the full 2×2 grid at both values. Compare unconditional and conditioned product, full table, and always rechecking.
- **Old-task retention:** Evaluate A/C at both slot values and later prefixes after the slot drifts across the certified range.

#### 13. A masked interaction on illegal support (I)
- **Mechanism:** Track legality separately and mark independence unidentifiable where the allowed support has no comparison rectangle. Reopen the claim if a new lawful combination appears.
- **Novelty:** Positivity and identifiability under restricted support are established; the audit prevents a spurious product proof.
- **Cheapest first test:** Reveal only cells `00` and `11` first, then make `01` legal in a new version. Compare an eager product, conservative support-aware inference and a flat table.
- **Old-task retention:** Plant a rare A failure in the newly legal cell and a C loss from the fallback, and verify each separately before serving.

#### 14. A product that knows the order of its factors (I)
- **Mechanism:** Treat the two execution orders as distinct until a commutation proof covers training transitions, exposure of intermediate states, and all relevant checks.
- **Novelty:** Partial-order reduction already exploits commuting actions; this tests how often learner updates are actually independent enough to justify it.
- **Cheapest first test:** Two mini-batches with the same final weights under both orders but an order-dependent intermediate margin. Compare end-only proof, order-sensitive factored proof, and exact prefix replay.
- **Old-task retention:** Put A's minimum at the hidden intermediate prefix and C's at the end; compare against the predeclared atomic or staged schedule.

#### 15. The no-shortcut bound on dense interference (I)
- **Mechanism:** Compare the savings of a product against the cost of ruling out a single concealed bad cell; without structural evidence, abstain on unchecked cells rather than infer safety from sparse failures.
- **Novelty:** This is an indistinguishability lower-bound audit, consistent with the ledger's functional-syndromes failure, not a sparse recovery proposal.
- **Cheapest first test:** For a legal binary success grid, pair an all-pass world with an otherwise identical world for each unchecked failed cell. Count how many checks any exact claim needs and add a dense-coupling arm.
- **Old-task retention:** Give every concealed failure its own ordinary A or C slice, and count any abstention as reduced coverage on the affected frozen offer.

#### 16. Patch rent and the exit from factorization (I)
- **Mechanism:** Charge each scoped patch for future rechecks and overlap; switch to a larger joint factor or flat table when accumulated rent exceeds its verified value.
- **Novelty:** Model selection and lazy abstraction already trade complexity for fidelity. The audit asks where maintaining a product becomes more costly than independent repair.
- **Cheapest first test:** Stream isolated corners, then widen coupling until half the grid is affected. Compare a fixed patch budget, online rent rule and hindsight best representation with proof bytes charged.
- **Old-task retention:** On each migration check rare A/C slices both inside and outside affected guards, and measure behavior during fallback.

### Make the purchased knowledge survive change

#### 17. Transfer the question, not the answer (P)
- **Mechanism:** Publish a scoped witness-choice test with its sufficiency conditions. A second learner with a compatible interface pays only to establish those conditions and answer that test, not to rediscover the whole repair table.
- **Novelty:** Transferable sufficient statistics and reusable assume–guarantee contracts are known. A primitive claim requires a portable test that revalidates training-witness decisions more cheaply across blind learner trajectories than those components stacked together.
- **Cheapest first test:** Two small hosts share a change-of-basis mapping, while a third has an unshared optimizer slot. Compare full recertification, transferred query plus ordinary repair, and transferred scope with the same verifier.
- **Old-task retention:** Protect ordinary A/C under both compatible and incompatible hosts, including inputs on which the shared check agrees but the unshared slot would forget.

#### 18. Withdraw one decision without forgetting its evidence (P)
- **Mechanism:** Maintain separate dependency records for an answer, a factor claim and each witness authorization. A local counterexample revokes downstream authorizations while preserving still-valid answers and proofs that never depended on the failed claim.
- **Novelty:** Truth-maintenance systems retract proof descendants; the candidate CL operation is avoiding repeated training or teacher queries when only a subset of existing repair rights dies.
- **Cheapest first test:** Retire a source, introduce a coupled continuation, and compare proof-directed withdrawal to ordinary truth maintenance plus a versioned repair cache and to whole-class rebuild under identical storage.
- **Old-task retention:** Exercise A/C in the revoked branch, its verified sibling, and an independent branch that shared the answer but not the failed factor; no hidden source fallback.

#### 19. A query that is valuable only before a source disappears (I)
- **Mechanism:** Pay to answer a pending witness dispute early if the lawful teacher is about to disappear and later verification alone cannot choose a cheap repair; price storage and possible expiry.
- **Novelty:** Optimal stopping and [witness examples](https://github.com/manojbajaj95/cl/pull/163) already motivate acquisition before retirement; this tests the narrow choice-specific budget, not teacher-free learning in general.
- **Cheapest first test:** Close a one-bit source after two offers; alternate offer streams where the stored answer saves a witness and where it never gets used. Compare always ask, demand-blind replay and exact finite planning.
- **Old-task retention:** Disable source reads after closure and measure A/C on both an ordinary continuation and the first fallback after an expired answer.

#### 20. A challenger verifier that can falsify the receipt (I)
- **Mechanism:** Route against a cheap checker, but estimate the claimed decision savings and reuse only with an independent stronger checker that sees the same fixed artifacts.
- **Novelty:** Independent validation and multi-fidelity experimental design are established; this audit tests if decision relevance merely concentrates queries on gaps in a weak checker.
- **Cheapest first test:** Hide a joint-sensitive predicate from the cheap checker in a finite toy. Compare cheap-only, exact-only, and cheap triage plus exact acceptance at matched checking work; use full enumeration as ground truth.
- **Old-task retention:** Reserve ordinary A/C data neither checker uses to pick queries, including a rare conjunction the cheap checker misses.

#### 21. A demand shock that tries to break the question policy (I)
- **Mechanism:** Test query abstention under an independently chosen shift in editor mix; keep any demand-blind exploration arm separate from the pending-offer rule and charge its evidence.
- **Novelty:** Robust experimental design already prices model misspecification. This audit asks whether saving present repair cost quietly sacrifices future safe coverage.
- **Cheapest first test:** Rotate demand from common single-axis offers to rare mixed offers. Compare exact one-step EVSI, a fixed exploration budget, and exact planning with the same declared shift distribution.
- **Old-task retention:** Match new utility on each regime where possible and report the coverage gap otherwise; track rare A/C slices through the switch, not just average retention.

#### 22. A witness that makes tomorrow's question unnecessary (P)
- **Mechanism:** When two repairs safely meet today's frozen offer, compare a cheap specialist with a witness whose verified training effect removes a costly disagreement on already pending future offers. Never count a merely hidden failure as removed uncertainty.
- **Novelty:** Dual control already acts to improve future information, and the parent considers a repair that creates a diagnostic opportunity. The candidate here is a reusable training intervention that removes the need for the future measurement, rather than making the measurement easier.
- **Cheapest first test:** Exhaust a two-edit state graph with identical immediate utility but only one successor having a single shared next witness in both worlds. Compare exact belief-state repair planning, joint MTT plus verification, and independent EVSI with equal horizon.
- **Old-task retention:** Check A/C across all served prefixes in both worlds; include a branch where apparent convergence comes from losing C and must be rejected.

## Ranked deeper questions

1. **Is there anything reusable beyond EVSI plus a checked repair cache?** Start with 01, 05 and 18. Precommit blind editor families and compare with persistent exact EVSI, the same lawful queries, ordinary proof maintenance and matched repair/condensation. Keep the primitive claim only if the scoped artifact lowers total acquisition, proof or repair work at equal utility and A/C retention.
2. **What evidence really buys the unseen cross product?** Start with 09, 10, 12 and 15. Sweep from structural independence through isolated coupling to diffuse damage; test unseen combinations and charge locally patched proofs. If ordinary factored refinement with the same witness store ties, keep the factorization as an engineering improvement only.
3. **When is buying decision-relevant knowledge myopic even about decisions the learner actually faces?** Use 03, 04, 06 and 21 to find when bundles, delayed answers or frozen demand shifts dominate greedy query ranking. Keep prices, horizons, answer access and abstention costs common; measure safe utility rather than number of splits.
4. **Can teaching replace asking without making the old failure invisible?** Pair 11 and 22. Compare changing the learner so one verified witness suffices against paying for a joint guard or a separation query. If the intervention is not reused off the fit trajectories, or its apparent gain comes from lost A/C behavior, call it ordinary repair.
