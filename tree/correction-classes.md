# Correction classes: remember which failures one witness can fix

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Rejected-edit witnesses](rejected-edit-witnesses.md) ([PR #166](https://github.com/manojbajaj95/cl/pull/166)), cards 01 and 07. **Review seed:** [Flood triage row 265](https://github.com/manojbajaj95/cl/blob/36ef45c4acc9963e82d10495dd238072d12e7f29/reviews/flood-triage.md#L265) keeps both at score 3: keep a refusal with the truthful training evidence and scoped correction it teaches, keyed to the failed invariant rather than the editor; group refusals only when one witness fixes them under the declared continuations, then split the group when a later continuation separates them.

## Is a repair-defined equivalence class of failures a new CL object?

**Not as a partition alone.** Behavioral quotients, counterexample-driven refinement, and repair lookup are established. The candidate is a **learned, revisable unit of repair coverage**: one retained training witness changes what multiple independent frozen edits can safely do, and a new continuation can invalidate the sharing without invalidating everything the witness already taught. Its operations are to establish shared coverage, spend it on unseen demand, and refine or retire it when contradicted. The failed check is an index for finding candidate witnesses, not a class identifier or permission to admit. The witness teaches the learner; the gate and the edit's utility target do not move.

### What “same repair” means

- **Fix the interface.** A refusal records a proven failed check and a prospective learner state, including relevant optimizer and sampler state; the external payload, new utility target, legal training accommodations, and deployment schedule are frozen. Version the check, host and witness grammar. For a refusal `r` and legal witness `w`, applying the same witness means the same training artifact and recipe, not a per-member payload rewrite, new teacher query, or private fit. Store it with its correction and scope (what changes, on which states/continuations), plus enough auditable refusal evidence; do not require the original editor or a copy of its request to dispatch. Impossibility under the accommodation budget, no witness in the declared grammar, and an incomplete proof are distinct. Only the first two can be asserted from exhaustive search or a sound proof; unknown is not a failed repair.
- **Separate classes from covers.** In a fixed finite scope let `R(r,s)` be the set of single witnesses that, after suffix `s`, allow the original demand and preserve the old obligations at all served prefixes. Use a common suffix alphabet, recording illegality separately, and keep unresolved entries separate from checked results. On fully observed rows, `r ≡ t` when their sets match for every declared suffix; in a unique-repair toy this is just equality of the fixing witness, across suffixes. Practical sharing additionally needs a *named, verified* witness in every relevant cell, not just equal signatures (two unrepairable rows can be equal). With multiple witnesses, pairwise overlap is not an equivalence: sets `{a}`, `{a,b}`, `{b}` chain without a common fix. A cover with overlaps can still be useful; do not call it a partition or infer transitive membership. A canonical-winner partition is another valid baseline, but encodes a tie-break and may conceal alternatives.
- **Refine on evidence.** With the host, grammar and semantics fixed, adding suffix columns or testing more witnesses can split an observational class. A difference in a non-incumbent witness may split a signature while the incumbent still legally covers both children; a difference in the incumbent suspends its use where it no longer checks. Unknown cells may justify a query or an abstention, not a merge by default. If the host, grammar or check semantics change, the quotient itself may change in either direction; use a new scope, not a claim of monotone refinement. Myhill–Nerode is an analogy unless equality ranges over all legal futures and is stable under appending actions; a finite tested table need not be a right congruence.

**Paper case.** Four frozen edit demands all fail old invariant A before repair. They carry two independent fields: the failed branch's required unit correction (`+` or `−`), and whether a later batch reverses which sign the branch needs. The demands come from four distinct editors; omit editor ID from routing. The grammar has just two labeled examples `w+` and `w−` whose fixed training step adds the corresponding unit correction without changing the new target. A's margin on the implicated branch is 1 for the right sign and 0 otherwise, with floor 1; C's ordinary check stays at 1 in this toy. On the empty suffix the repair rows are `{w+}, {w+}, {w−}, {w−}`. For a legal batch that changes the required sign only on flipping branches, the rows become `{w+}, {w−}, {w−}, {w+}` if half of each group flips. The empty-suffix classes were real on their old scope but must split before reuse on the enlarged scope. The flipping rows have no single witness across both suffixes; a suffix-conditioned policy that picks a different witness is a different arm, not a single-witness win. This illustrates the distinction, not a predicted retention gain: the first test should give C its own failure mode and hide whole editor families.

### Prior-art screen and common controls

- **Repair and learning from queries.** [Counterexample-guided neural repair](https://arxiv.org/abs/2301.11342) already loops over failures and retraining; [CEGAR](https://doi.org/10.1007/10722167_15) refines a representation when a spurious counterexample exposes a missing distinction. [Angluin's L*](https://doi.org/10.1016/0890-5401%2887%2990052-6) learns residual behaviors via distinguishing suffixes, and [version spaces](https://doi.org/10.1016/0004-3702%2882%2990040-6) retain hypotheses consistent with evidence. Treat an observation table or version-space solver with the same queries as a direct baseline, not just an inspiration.
- **Repair memory.** Case-based reasoning already indexes and adapts old solutions. [GRACE](https://arxiv.org/abs/2211.11031) adds and adjusts a codebook of local edit regions; [SERAC](https://arxiv.org/abs/2206.06520) stores edits and predicts their scope; [MEND](https://arxiv.org/abs/2110.11309) transforms edit gradients. [ROME](https://arxiv.org/abs/2202.05262), [MEMIT](https://arxiv.org/abs/2210.07229) and [AlphaEdit](https://arxiv.org/abs/2410.02355) alter parameters to implement edits; success at storing or batching model edits is not evidence for grouping refusals by a shared *training* correction. Compare against the same failed-check index plus case retrieval and independent exact rechecking, not only editor-keyed retrieval.
- **Evidence and accounting.** Follow the [idea ledger](https://github.com/manojbajaj95/cl/blob/ffb732ec5a16fc3378c33f50f59289db786fc737/reviews/idea-ledger.md): do not credit the author of matched evidence, assume sparse damage, or let new-task progress or pre-edit margin explain retention. Stack matched counterexample-guided repair, raw failed-input replay, [GCR](https://arxiv.org/abs/2111.11210) or [MTT](https://arxiv.org/abs/2203.11932), and independent checks in the strongest combination that fits the budget. Compare to [witness examples](https://github.com/manojbajaj95/cl/pull/163) and [self-closing witnesses](https://github.com/manojbajaj95/cl/pull/165) on the same future branches. Use exhaustive class construction as an oracle in finite worlds, charging construction separately; it is not an online baseline given free information.
- **Common test contract.** Start with tabletop finite tables or tiny CPU learners, not GPUs. Precommit and hold out entire editor and continuation families. Charge all metadata, witness and proof bytes (peak and retained), source queries, solver calls, and runtime. Match admitted new-task utility when comparing retention; also report safe admissions over *all* frozen offers and count false refusals and unknowns. For every card, A and C are two ordinary old tasks on held-out data, not merely the check used for routing; report each against acquisition and pre-edit references at served prefixes, including rare slices. Card-specific checks below add to this contract. **P** = conditional primitive candidate (new operation or object if the test clears the null); **I** = improvement or audit, not a pilot recommendation. Prior-art comparisons are hypotheses, not novelty clearance.

## Idea cards

### Define a shareable unit

#### 01. A refusal with a repair target that outlives its editor (P)
- **Mechanism:** Record a demonstrated failure with a truthful labeled witness, the correction it teaches, and its checked scope. Dispatch on the failed invariant; rerun the later editor's original demand after training on the candidate witness.
- **Novelty:** [SERAC](https://arxiv.org/abs/2206.06520) retrieves edits by learned scope; this would make the stored item an independently reusable intervention on training rather than an answer override or remembered payload.
- **Cheapest first test:** Construct a two-gate ReLU toy with two committed editors using disjoint payloads. Remove editor IDs and the first payload from dispatch; compare reuse on the second against matched repair plus MTT and failed-input replay.
- **Old-task retention:** Make the first edit threaten A and the witness itself able to harm C. Evaluate both on withheld ordinary-task sets after training and after the second unchanged demand; the routing invariant is not either holdout.

#### 02. The first separating continuation (P)
- **Mechanism:** Build provisional groups with one certified witness per group on the declared scope. A newly legal suffix that separates two members becomes a recorded test for the split; keep the former witness where it still checks.
- **Novelty:** [L*](https://doi.org/10.1016/0890-5401%2887%2990052-6) already uses separating suffixes. The proposed new operation is retaining and spending the same training artifact on independent edits across splits, rather than merely refining a state label.
- **Cheapest first test:** Use the four-edit paper case with four held-out editors and both a valid and a distractor suffix. Compare GCR similarity, raw replay, a plain observation table plus repair, and exhaustive class construction.
- **Old-task retention:** Make the distractor and separating suffixes threaten different A/C slices; check all served prefixes, including the branch that keeps the parent witness.

#### 03. One-check buckets with internal disagreements (I)
- **Mechanism:** Keep the failed check as a lookup key, but require the router to recognize multiple incompatible correction targets inside one bucket, including when two check names are aliases for the same invariant.
- **Novelty:** [GRACE](https://arxiv.org/abs/2211.11031) already resolves edit-region conflicts. This measures whether invariant keys nevertheless reduce search cost under renaming and shared symptoms, not a new indexing primitive.
- **Cheapest first test:** Rename check IDs across two equivalent editors and plant two opposite fixes under a single invariant. Compare key-only, failure-feature retrieval, and semantic invariant keys with the same rechecker.
- **Old-task retention:** Test A and C on both aliased and conflicting branches; a lookup miss counts as lost coverage, not improved safety.

#### 04. Cover the overlap without inventing a class (I)
- **Mechanism:** Put multi-repair refusals in an explicit cover whose hyperedges name the witnesses they share; never union edges just because they overlap.
- **Novelty:** [GCR](https://arxiv.org/abs/2111.11210) and ordinary set cover are sufficient storage baselines. The question is the cost of a disjoint quotient when witness coverage is non-transitive.
- **Cheapest first test:** Enumerate the `{a}, {a,b}, {b}` table under one- and two-witness budgets. Compare exact cover, canonical winner, and pairwise clustering on unseen refusal types.
- **Old-task retention:** Ensure an otherwise easy edit damages rare A under `a` and rare C under `b`; report safe coverage at the same old-task floors, not just assignment accuracy.

#### 05. A canonical repair with a tie-break audit (I)
- **Mechanism:** Assign the cheapest verified witness per refusal under a fixed price vector; flag apparent classes that fall apart when prices of source calls versus bytes change.
- **Novelty:** [MTT](https://arxiv.org/abs/2203.11932) and discrete coreset selection already optimize compact witnesses. This audit distinguishes sharing created by the optimizer's preferences from sharing in the repair relation.
- **Cheapest first test:** Create three families with equal-length alternatives and sweep witness costs in a fully enumerated table. Compare class stability and coverage to full signatures.
- **Old-task retention:** Check A/C after switching to the new winner, including a rare old case that exposes an ostensibly cheap witness as unsafe.

### Learn which continuations matter

#### 06. Buy the separation you can actually use (P)
- **Mechanism:** Ask for a lawful continuation observation only if the competing repair hypotheses imply different *deployable* witnesses on pending frozen demand. Prioritize by saved repair acquisition cost, not label entropy.
- **Novelty:** [DAgger](https://arxiv.org/abs/1011.0686) targets learner-reached states and version spaces already support active queries. The candidate operation is spending one answer to keep or withdraw a shared training intervention on multiple independently acquired failures.
- **Cheapest first test:** Enumerate competing repair tables with one high-information but decision-irrelevant query and one cheaper useful query. Compare random, entropy, and exact decision-theoretic query selection at equal budgets.
- **Old-task retention:** Replay A/C for every table still consistent with the transcript before a class is published; independently test held-out old trajectories after each actual admission.

#### 07. Find the suffix, not just the final bad batch (I)
- **Mechanism:** Minimize a legal sequence that separates two refusals while preserving the entire intervening optimizer-state history needed for the difference.
- **Novelty:** [CEGAR](https://doi.org/10.1007/10722167_15) already uses traces, and the parent minimizes a causal prefix. This is a trace-minimization cost test for separations between repairs, not a primitive claim.
- **Cheapest first test:** Two states with identical weights and different hidden momentum separate only after an ordered pair of batches. Compare shortest exhaustive separator and greedy batch deletion to final-state testing.
- **Old-task retention:** Hold weights initially fixed across arms; score ordinary A/C through both batch orders and check the chosen split preserves the unperturbed branch.

#### 08. A split that changes nothing about deployment (I)
- **Mechanism:** Mark a signature split as operational only if it changes an admissible witness choice or future query. Keep search refinements separate from the deployed cover.
- **Novelty:** [Counterexample-guided neural repair](https://arxiv.org/abs/2301.11342) refits on counterexamples; lazy abstraction already delays refinements. The audit tests whether non-incumbent failures justify any witness-state churn.
- **Cheapest first test:** Stream new suffixes that invalidate unused alternatives but not the incumbent, then one that invalidates it. Compare eager repartition, lazy deployed cover, and from-scratch repair.
- **Old-task retention:** A and C must both remain intact through the no-op splits; after the real split, measure rare-task loss during fallback and the first licensed reuse.

#### 09. A repair state you can advance without an old trace (P)
- **Mechanism:** Learn transitions between repair classes under a fixed action alphabet. Use them only when appending an action maps every class member to the same successor class with the same supported training response.
- **Novelty:** [L*](https://doi.org/10.1016/0890-5401%2887%2990052-6) already constructs such quotients for language recognition. The possible new object is a compact controller for spending a bounded *learned repair* across old traces rather than a Boolean acceptor.
- **Cheapest first test:** Compare exhaustive quotient execution with an L* table plus repair and trace replay in a finite learner with one congruent region and one noncongruent region. Discard the idea if the same-cost stack reproduces it.
- **Old-task retention:** Use two held-out trace orders that end at the same task utility but differ on rare A or C; score both through every action and demand an independent check before serving.

#### 10. Tell two similar slopes apart by the repair they cannot share (I)
- **Mechanism:** Train a cheap router from witness-transfer labels rather than edit embeddings or local gradient similarity; the exact checker still controls admission.
- **Novelty:** [GCR](https://arxiv.org/abs/2111.11210) summarizes gradients, and [SERAC](https://arxiv.org/abs/2206.06520) learns scope. This is a routing improvement only if repair labels save compute after paying to obtain them.
- **Cheapest first test:** In a tiny ReLU learner, match one-step gradients on edits that cross different activation boundaries later. Compare transfer labels, gradient matching and case retrieval under the same fixed query bill.
- **Old-task retention:** Match pre-edit A/C margins, then measure each after the crossing and after a normal later batch, with no extra replay allowed for one arm.

### Spend what the class remembers

#### 11. Synthesize one witness for conflicting-looking edits (P)
- **Mechanism:** Search the fixed example grammar jointly for one artifact that fixes every member, including cases where the best individually fitted witnesses differ. Reuse only with independent evidence on the full branch set.
- **Novelty:** [MTT](https://arxiv.org/abs/2203.11932) already jointly fits trajectories. The primitive claim requires reusable class structure to select future branches or lower total costs beyond MTT given those same branches, not just finding a common example.
- **Cheapest first test:** Enumerate a grammar where no optimizer's per-member winner covers its peers but a second-choice example covers all. Hold out an editor; compare pooled MTT, selecting among per-edit repairs, and synthesis that uses verified class structure.
- **Old-task retention:** Verify rare A/C under the shared example and each individual winner after the held-out edit, at matched admitted utility and byte budget.

#### 12. Keep the parent witness after a split (I)
- **Mechanism:** After a separator breaks one child, keep the parent artifact as a candidate for both children but publish its narrowed scope; fit a new witness only for uncovered demand.
- **Novelty:** [GRACE](https://arxiv.org/abs/2211.11031) reuses and adds local patches when coverage changes. This tests whether a training example yields similar amortization without preserving a pre-split unsafe route.
- **Cheapest first test:** Three rounds of a finite stream with one valid child at each split. Compare rebuilding both children, independent repair, and scoped inheritance with total reacquisition charges.
- **Old-task retention:** Test one rare A and one rare C probe per child before the split, during scoped fallback, and after the replacement is admitted.

#### 13. A class-level promise that survives replanning (P)
- **Mechanism:** Pick a class witness that leaves at least one lawful repair available for each future demand in a declared two-step family, not necessarily the same follow-on witness in every branch.
- **Novelty:** [HAL](https://arxiv.org/abs/2002.08165) anticipates interference and the parent already proposes two-round search. The additional claim is reuse of a *class-wide* future option across independent present editors, beyond per-editor contingent planning plus repair.
- **Cheapest first test:** Enumerate two first-step witnesses with equal one-step coverage, but only one leaves a legal second-step option after either of two independent editors; the second-step witnesses can differ. Compare class-constrained planning with exhaustive per-editor planning and the strongest cost-matched stack.
- **Old-task retention:** At each leaf check A and C separately, including leaves lost to first-step refusal; matched coverage alone cannot hide the loss of rare old-task performance on served leaves.

#### 14. Show the effect of sharing one training artifact, not bundling edits (I)
- **Mechanism:** Compare one witness used independently on several frozen edits with a batch edit, with repeated independent editing, and with one per-editor witness compressed to the same bytes.
- **Novelty:** [MEMIT](https://arxiv.org/abs/2210.07229) implements many edits jointly and [ROME](https://arxiv.org/abs/2202.05262) supplies an individual edit control. A batch efficiency win is not evidence for repair equivalence.
- **Cheapest first test:** Use linear readouts with two editor orders, one where batching cancels interference and one where it does not. Give all arms the same demands and preservation constraints.
- **Old-task retention:** Score A/C after each visible edit and at the matched final utility; do not compare a batch's final state to intermediate retention without reporting the difference in visibility.

#### 15. A witness must repair the learner, not learn the checker (I)
- **Mechanism:** Build class signatures with an incomplete checker, then audit against an exact evaluator on the same legal continuations. Distinguish a shared training correction from a shared way to make the proof pass.
- **Novelty:** [Counterexample-guided neural repair](https://arxiv.org/abs/2301.11342) already couples checker and repair. The null is that the apparent classes are just clusters of checker blind spots.
- **Cheapest first test:** Use a two-feature correlated input where an interval checker loses a relation. Compare refinement before and after giving both class and raw-repair arms the exact relation.
- **Old-task retention:** Keep the A/C holdouts exact and independent of either checker, including a branch where a missed invariant violation affects ordinary old performance.

#### 16. Spend the class after reclaiming its evidence source (P)
- **Mechanism:** At a declared cut retain a witness and a minimal set of separating observations, then allow future splits only on new lawful evidence; no dispatch may read the old teacher or recover dropped payloads.
- **Novelty:** [DER](https://arxiv.org/abs/2004.07211) and [FRCL](https://arxiv.org/abs/1901.11356) already retain targets and functions, and [PR #163](https://github.com/manojbajaj95/cl/pull/163) already retires sources. The additional claim is that separators buy future *repair refinement* per byte, not retirement itself.
- **Cheapest first test:** Overwrite the old teacher in two finite worlds that agree on routine outputs and differ on one repair suffix. Price class separators against equal-byte cached targets, MTT plus repair, and a live-source oracle kept outside the learner.
- **Old-task retention:** Score A/C before the cut, after storage reuse, and after a new split. On any indistinguishable unsafe branch count abstention rather than letting an oracle quietly rescue it.

### Find when the object disappears

#### 17. How many bits does a split cost? (I)
- **Mechanism:** Construct pairs of worlds with the same observed check and repair results but opposite safe witnesses after a later suffix. Derive a lower bound on lawful observations needed to preserve coverage.
- **Novelty:** [Version spaces](https://doi.org/10.1016/0004-3702%2882%2990040-6) already imply indistinguishability. The audit identifies whether the information missing in repair classes is any smaller than that needed for independent repairs.
- **Cheapest first test:** Enumerate `k` hidden polarity bits, independently revealed by legal separators. Require a safe repair decision for every pending edit or charge abstention; compare worst-case query counts to a flat repair table.
- **Old-task retention:** Attach opposite A and C hazards to the two polarities; evaluate both worlds under the same pre-separation transcript and record unsafe guesses separately.

#### 18. How much future is enough to name a class? (I)
- **Mechanism:** Plot class stability versus suffix horizon, measuring both the number of groups and the fraction of demand still serviced by one fixed witness.
- **Novelty:** [L*](https://doi.org/10.1016/0890-5401%2887%2990052-6) already uses finite evidence about unbounded futures. This is a feasibility audit for a compact learned-repair quotient, not a general horizon law.
- **Cheapest first test:** Compare finite systems with two persistent classes, one late separator, and proliferating splits. Use the same demand distribution and price doubling the suffix horizon against raw repair acquisition.
- **Old-task retention:** At short and long horizons check A/C on services that would be admitted under the short horizon alone, including delayed rare-task damage.

#### 19. A repair shared only because the price is wrong (I)
- **Mechanism:** Measure the full cost of discovering, proving, routing and maintaining a class. Ask whether amortization survives independent demand and change rather than treating class labels as free.
- **Novelty:** [MTT](https://arxiv.org/abs/2203.11932) pursues compact data, and [selective classification](https://arxiv.org/abs/1705.08500) prices coverage and risk. This is a break-even audit for repair sharing instead of a new eviction rule.
- **Cheapest first test:** Vary repeat frequency and separator arrival independently in a fixed finite stream. Compare end-to-end costs of class maintenance, exact scratch repair and matched replay, including never-refit frozen offers.
- **Old-task retention:** Match A/C floors and new utility at every cost comparison. Count rare old-task loss after eviction or reacquisition and report feasibility separately if no match exists.

#### 20. Destroy class information without destroying the examples (I)
- **Mechanism:** Cross the same witness bank with accurate, shuffled and erased class and separator metadata, holding the failed-check index, routing budget and checker fixed. Also compare ordinary case retrieval.
- **Novelty:** [Dataset condensation](https://arxiv.org/abs/2006.05929) predicts that the examples may explain all progress; [SERAC](https://arxiv.org/abs/2206.06520) is a scope-aware alternative. This is a direct null test of whether the class carries information beyond the stored interventions.
- **Cheapest first test:** Permute memberships only within failed-check buckets on a tableau that includes a held-out editor family and one late separator. Compare checked admissions at equal bytes and witness trials.
- **Old-task retention:** Recheck A/C after the held-out editor and after the late separator, at matched served utility; include both false coverage from shuffling and false refusal from erasure.

### Make the quotient do something a lookup cannot

#### 21. Learn reusable maps between versioned classes (P)
- **Mechanism:** On a host update, retain a map from old class cells to new ones only where a proof shows the update preserves which witness succeeds. Reuse the mapped witness without replaying the old edit; require new evidence where the proof does not go through.
- **Novelty:** [CEGAR](https://doi.org/10.1007/10722167_15) refines an abstraction of a system, and [AlphaEdit](https://arxiv.org/abs/2410.02355) preserves selected knowledge under edits. The candidate operation transfers an entire *repair relation* across a host update, not a repaired answer or a bound on an isolated edit.
- **Cheapest first test:** Use a two-block linear learner with a version update that commutes with one witness and interferes with the other. Compare mapped cells against incremental rechecking plus repair and a fresh quotient; include the cost of proving the map.
- **Old-task retention:** Immediately after the host update and after reuse, score A/C separately, with rare inputs that exercise the changed block even if the failed check reads only the unchanged block.

#### 22. A class of failures with a transferable impossibility proof (P)
- **Mechanism:** When a proof rules out every single witness for a single-witness demand, store its binding constraint as an obstruction shared by other refusals, scoped so a grammar or budget change can invalidate it.
- **Novelty:** [Neural repair](https://arxiv.org/abs/2301.11342) already searches constrained repairs, and the parent proposes negative-proof caching. A primitive survives only if one obstruction can also guide what evidence to acquire next across independent failures, beyond ordinary proof reuse.
- **Cheapest first test:** Construct two disjoint failed-check routes with the same unachievable margin gap and one visually similar feasible route. Compare transferring the obstruction to incremental constraint solving and raw proof caching at equal evidence cost; then widen the witness language.
- **Old-task retention:** Test A/C on the feasible neighbor and on the formerly blocked branch after widening; neither broad blacklisting nor lowering the old-task floor qualifies.

#### 23. Recover a hidden correction factor without storing the cross product (P)
- **Mechanism:** Factor repair signatures across two independent continuation coordinates only when relational evidence proves that the *success relation for one witness* factors. An interaction counterexample replaces the factorization locally instead of forcing a global rebuild.
- **Novelty:** [GCR](https://arxiv.org/abs/2111.11210) measures gradient coverage and [MTT](https://arxiv.org/abs/2203.11932) can fit pooled branches. Neither is a reason to expect compositional coverage; compare with factored abstraction plus matched repair, and claim novelty only for compositional reuse of the learned witnesses.
- **Cheapest first test:** Enumerate a two-coordinate learner with independent blocks and a special coupled batch that breaks factorization. Charge all proof work and test on unseen coordinate combinations against product-table and factored baselines.
- **Old-task retention:** Assign ordinary A and C to different blocks and add rare mixed inputs. Test both after independent combinations and the special batch; additive average retention cannot mask mixed-input damage.

#### 24. A repair experiment doubles as a diagnosis of the next failure (P)
- **Mechanism:** When two verified witnesses safely admit the current frozen demand, choose between them by which later lawful observation they make distinguishing for a pending refusal. Run comparisons in shadow where needed; independently authorize every served result.
- **Novelty:** [DAgger](https://arxiv.org/abs/1011.0686) collects labels on induced states and [MEND](https://arxiv.org/abs/2110.11309) learns a corrective edit. The claim is an intervention that is both a verified repair and an instrument for resolving the scope of another shared witness, not just an active query or a good one-step edit.
- **Cheapest first test:** Two equal-cost repairs have equal immediate margins; one creates a legal next state where two competing correction rules predict different outcomes. Compare against active querying plus independent repairs and a cost-matched policy that chooses by immediate margins.
- **Old-task retention:** Measure A/C after both current repairs and after the diagnostic continuation, in both possible rule worlds; count the same diagnostic cost even if an arm refuses to serve.

## Ranked deeper questions

1. **Does shared repair predict safe admission for an independent frozen editor better than the best matched repair-and-condensation stack?** Start with 01, 02 and 20. If the gain vanishes with the same witnesses, checks, bytes and lawful queries, the class is bookkeeping.
2. **Can separating continuations be found and paid for before class errors reach service?** Use 06, 07 and 17 to compare active queries, full observation tables and ordinary repair. The target is lower repair acquisition cost at the same A/C floors and admission coverage, not a higher split count.
3. **Do repair classes remain useful when continuations compose and sources disappear?** Test 09, 13, 16 and 18. Require verified scope advancement or explicitly priced new evidence; neither equality at the next step nor a hidden teacher fallback qualifies.
4. **When should a quotient yield to an overlapping cover or a flat repair store?** Test 04, 05 and 19 across budgets and churn; a stable partition with unsafe winners or no amortization is not a useful CL object.

**Verdict.** A repair-defined equivalence relation is not itself new; the plausible primitive is a verified, revisable claim that a single learned training witness buys safe utility on independently proposed frozen edits. Keep the claim only if checked reuse or separation saves total evidence or repair work versus stacked baselines at matched new utility and ordinary A/C retention; otherwise keep the refusal-plus-correction index as a useful repair cache.
