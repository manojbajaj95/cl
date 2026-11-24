# Data-only edit cost: which examples make later fact edits cheaper and safer?

**Status:** ideas only; no experiments, probe code, or GPU. **Parent:** [Future edit cost](future-edit-cost.md) ([PR #144](https://github.com/manojbajaj95/cl/pull/144), ranked question 1).

Two corpora can teach the same current facts, give a model the same accuracy, and leave very different bills when one fact changes. Take a bridge whose posted toll is withdrawn: some requests should fall back to the municipal rate, a historical invoice should still use the old toll, and an unrelated bridge that happened to charge the same amount should not move. Can we make that edit cheaper **by choosing examples alone**, and can we tell beforehand which property of the examples matters? If the effect is real, a corpus audit should predict where to spend the next example better than fact frequency, margin, or witness count alone.

## What to count, and what would settle it

- **Make the data treatment literal.** Choose equal-token, equal-example subsets from a shared, truthful pool made before test events are drawn. Use ordinary training targets: no edit-aware loss, unrolled edits, auxiliary heads, mutable store, test-time metadata or extra editor inputs in a data-only arm. Keep the tokenizer, architecture, parameter count and precision, optimizer, steps, batch construction rule, edit inputs, audit budget, and editor implementation fixed within each contrast. Cross data policies with a frozen editor menu (direct fine-tuning, fixed-budget replay and labeled [ROME](https://arxiv.org/abs/2202.05262)/[MEMIT](https://arxiv.org/abs/2210.07229) or [AlphaEdit](https://arxiv.org/abs/2410.02355) proxies on the tiny host). Hold the full state budget fixed, including editor state. Treat [Editable Neural Networks](https://arxiv.org/abs/2004.00345) as a different training objective, not a data-only treatment.
- **Use a small CPU world with honest counterfactuals.** Start with arbitrary key and value tokens, an unpartitioned tiny MLP or attention model, and an offline truth table for routing, billing, and exceptions. Alternative facts are true in their own training worlds; the editor receives only the current change, never the truth table. In each matched swap, change one nominated data statistic while preserving counts, witness coverage, answer histograms and document length wherever the design permits. Use random matched swaps and report unavoidable imbalances. Start from competent cohorts; report the full randomized comparison and the shared pre-edit competence/direct-recall margin panel, with matching attrition. Draw paired test worlds, edit values, streams, and request templates after freezing the selector. Forecast-conditioned or editor-conditioned selection must use development data only, and its calibration work is charged upfront.
- **Measure the whole bill at floors fixed in advance.** Inherit the parent's `(C,D)`: acquisition, selection, training, revision search/writes/audits/failures/rollback/fallback, and serving cost versus request-weighted error over the stream. Show revision work separately, and report peak bytes, latency, exact stale answers, other changed-answer errors, and unaffected errors. Enforce current direct recall, live dependent answers, and each retention floor; count a missed deadline or abstention as lost service, not a cheap edit. Compare to uniform, frequency×hazard, equal-token [KAFT](https://arxiv.org/abs/2211.05110), matched replay, and priced exact KV plus the same executor. Use a no-edit shadow, placebo writes and paired uncertainty over whole worlds/streams. A useful win lowers the safe revision bill without raising lifecycle cost or damage, or exposes a clearly priced Pareto trade-off; a better one-shot score is not the result.
- **Keep retention and the read/write diagnosis separate.** Every test below inherits a frozen old-task panel: untouched facts, unaffected requests, old exceptions, earlier revisions that remain current, and old procedures evaluated on current premises, both closed-book and with oracle premises. Obsolete answers count as retention only when explicitly requested as history. Check the shared panel after each write or failed attempt, not just at the end. Where a card claims a mechanism, compare learned hosts to known cache/reader controls, measure the change in live answers after a verified value swap (with wrong-key and same-value controls), and check whether the procedure still works with supplied premises. A cheaper binding write, better propagation after the same write, and preserved procedure are distinct outcomes.

**Ledger and triage screen.** [Idea ledger](https://github.com/manojbajaj95/cl/blob/0a714619d6d0318a48ddb448fde394e6e2d65786/reviews/idea-ledger.md); [flood triage, rows 231–233](https://github.com/manojbajaj95/cl/blob/0a714619d6d0318a48ddb448fde394e6e2d65786/reviews/flood-triage.md#L231-L233). Eliminating bounded shortcuts by buying contradictions is teaching dimension/query-by-committee. Waking an old procedure without waking its old world (BCE4) is an audit, not a new method here. The parent's invalidation-key and sub-threshold arms are controls where relevant, not renamed cards. No sparse-collateral assumptions, no raw `k*` threshold, no edit-capacity law without variation beyond a constant, and no margin-only, replay, retrieval, or KAFT result sold as a new mechanism. Prior-art deltas below are scoped hypotheses, not priority claims; all CPU tests are proposals.

## Idea cards

### A. Teach what a revision means

#### 1. Withdrawals are not blanks

- **Mechanism:** Sample matched cases with a formerly valid toll withdrawn, a toll never posted, and a toll explicitly set to zero. Bare direct lookup can equate the first two as unavailable while a consumer must distinguish a withdrawal that activates a legacy waiver from a never-posted fact that does not.
- **Novelty vs nearest prior art:** [Time-Aware Language Models](https://arxiv.org/abs/2106.15110) attach time to facts; this asks whether explicit negative-state contrasts make a future one-write withdrawal propagate, beyond time-aware recall and generic crossing coverage.
- **Cheapest first test:** Use eight synthetic bridges; swap triples contrasting absence types for equally frequent amount replacements. Hold status-token counts fixed, then edit a held-out live record to withdrawn. Compare waiver activation and revision cost at matched direct status recall; use fresh never-posted IDs to test a generic blank/default shortcut.
- **Old-task retention check:** Verify old zero-toll rules, never-posted bridge behavior and unaffected fees after successive withdrawals.

#### 2. A revocation can reveal a default without editing it

- **Mechanism:** Pair ordinary lookup examples where a local override and default agree on the number but differ in what should happen if the override disappears. Include matched examples with identical current answers but different fallback depth.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) evaluates propagated changes through linked facts. The candidate property is **dormant fallback depth**, distinguished from the parent's active dependency/invalidation key: no pre-withdrawal change to the default can alter the live answer behind the override.
- **Cheapest first test:** Use a two-level override table with fixed direct fact QA and active-witness counts. Swap in suppressed-default examples while matching values, then revoke novel overrides without supplying the fallback to the editor. Compare direct-plus-derived repair work to training on active paths only.
- **Old-task retention check:** Defaults must remain intact under unrelated override deletions; still-active overrides must continue to mask them.

#### 3. An identifier rename is not a new referent

- **Mechanism:** Select training worlds that distinguish changing a label on the same entity from reassigning that label to a different entity. Hold the payload and rename frequency constant; vary which ordinary requests still follow the old entity.
- **Novelty vs nearest prior art:** [ROME](https://arxiv.org/abs/2202.05262) targets a factual association and probes generalization and specificity. This isolates **identity continuity** as a property of evidence that might decide whether a binding write preserves prior obligations; it is not simply alias diversity.
- **Cheapest first test:** Use two bridges with interchangeable surface labels and distinct stable inspection requirements. Make rename and reassignment examples indistinguishable by label counts but distinguishable by the recorded identity relation; edit only the label mapping on unseen bridges. Compare to alias permutation and a byte-priced explicit identity map.
- **Old-task retention check:** Old inspection obligations and dated reports must stay on the original entity; untouched aliases must still resolve.

#### 4. Split a fact that was shared, not just a duplicated answer

- **Mechanism:** Select examples that show one policy applying to a group and others with merely coincident individual values. Later a membership edit should move one member to another rule without modifying either rule or the other members.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) studies when contexts support interchangeable fragments. Here the question is whether matched examples of shared authority versus equal payload distinguish **membership edits** from value edits under the same writer.
- **Cheapest first test:** Keep per-entity rate QA identical; vary examples of membership on independent policy IDs versus coincident local rates. Change one membership on held-out IDs, and compare repair cost with the same value crossings and explicit membership-map control.
- **Old-task retention check:** Recheck previous group members, stand-alone exceptions and older membership edits that remain in force.

#### 5. Fixed invariants decide which consumer should reject a value

- **Mechanism:** Show matched examples where the same valid binding is usable for one request but disallowed for another by a stable rule; e.g., a night limit accepted for a car is invalid for a hazardous-load permit. Isolate the validity relation from rarity of the value.
- **Novelty vs nearest prior art:** [Counterfactually Augmented Data](https://arxiv.org/abs/1909.12434) varies causally relevant inputs to improve predictions. Here the dependency to learn is **where not to apply a valid edit**: direct recall should succeed even as a particular consumer rejects the change.
- **Cheapest first test:** Compare matched swaps of same-value/different-consumer examples to same-consumer/different-value examples, keeping rejection counts and support fixed where feasible. Replace a permissible car limit with a held-out limit that violates the truck rule; compare unsafe acceptance and consumer repair at matched recall.
- **Old-task retention check:** Freeze unrelated permits and rare old exemptions, including ones that still accept the edited value under a different rule.

#### 6. Preserve valid time when the correction arrives late

- **Mechanism:** Include pairs with the same effective dates and values but distinct report orders, including backdated corrections which change an old invoice without changing today's rate.
- **Novelty vs nearest prior art:** [Time-Aware Language Models](https://arxiv.org/abs/2106.15110) model temporal facts, and [TimeStress](https://arxiv.org/abs/2502.01220) checks temporal consistency. This asks if the **separation of effective time and announcement order** in data reduces live repair and retrospective collateral with one fixed edit packet.
- **Cheapest first test:** Use three intervals per key and an edit packet naming the corrected interval. Swap concordant for discordant announcement orders, preserve snapshots and format, and evaluate unseen date ranges with the same temporal tokens and editor; compare with chronological-snapshot and exact temporal-store controls.
- **Old-task retention check:** Check the current rate and untouched historical intervals both immediately and after a later current-rate edit.

### B. Teach which answers should move together

#### 7. Buy evidence for masked dependence, not just answer flips

- **Mechanism:** Vary whether a fact dependency appears only after a second premise changes: for an “either crossing is open” rule, changing one crossing matters only when the other is closed. Distinguish a masked influence from a genuinely irrelevant premise.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tests multi-hop consequences, and the parent prices jointly occurring edits. This is a data contrast on **conditional sensitivity**, with a single edit at evaluation and the masking premise already in place.
- **Cheapest first test:** Use binary request families with matched one-key witness counts and label histograms; swap placements of those witnesses across the mask states. Retest under a held-out masking premise with one binding edit; compare to allocating on marginal fan-out.
- **Old-task retention check:** Score still-masked requests, independent requests and old exception masks, not merely the newly sensitive requests.

#### 8. Teach a key's positive and negative consumers at equal fan-out

- **Mechanism:** Keep how many consumers change constant but vary whether each increment pushes them in the same direction or opposite directions. A bridge toll can make the bridge less attractive for a driver and more attractive to a revenue-based inspection rule.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tracks ripple correctness. A **signed dependency profile** asks whether diverse response directions prevent a broad output-level correction that appears safe on homogeneous consumers.
- **Cheapest first test:** Match edit magnitudes, observed witness counts and global labels by permuting comparator orientations across key–consumer pairs. Give both arms the same held-out increment. Compare against unsigned fan-out and an answer-histogram model, testing benefit beyond pre-edit margin.
- **Old-task retention check:** Check untouched consumers that emit the same output token as the changed consumers, and old reverse-sign exceptions.

#### 9. A changed winner has a loser that must stay gone

- **Mechanism:** For a one-to-one assignment, train on displacement examples where appointing a new operator also makes the old operator unassigned, rather than only on static inverse lookups.
- **Novelty vs nearest prior art:** [The Reversal Curse](https://arxiv.org/abs/2309.12288) and [semantic-aware permutation training](https://arxiv.org/abs/2403.00758) concern learning both directions. This tests the extra effect of **exclusive replacement evidence**, after forward and reverse exposure are already matched.
- **Cheapest first test:** Use small matching worlds; compare exposure to matched displacement contrasts versus scrambled examples with equally many forward and inverse questions and the same current QA. Reassign a held-out operator and price removing the old inverse association without repairing every query.
- **Old-task retention check:** Verify unrelated assignments in both directions and past assignments under explicit dates.

#### 10. Teach conserved quantities with competing witnesses

- **Mechanism:** Select examples where two amounts move together because a stable total constrains them, versus the same co-movement caused by an unrelated coincidence. A change to one share should update its complement but not the total, even if all three have been equally predictable from pairwise data.
- **Novelty vs nearest prior art:** [Learning Neural Causal Models with Active Interventions](https://arxiv.org/abs/2109.02429) uses interventions to learn causal structure. Here the data-only question is whether evidence for a **conservation constraint** removes a second update under an ordinary predictor and writer, not whether a causal learner recovers the graph.
- **Cheapest first test:** Enumerate small modular-sum tables: all pairs of the two summands and total are uniform under the constraint. Match pair marginals with an independent control corpus, expose both models to the same target-world fact and procedure QA, and estimate specificity after editing one share in a novel context.
- **Old-task retention check:** Keep unrelated totals and total-preserving allocation procedures correct, including old contexts where the shares are independent.

#### 11. Teach recomputation through unequal paths that cancel

- **Mechanism:** Select examples where changing a shared rate raises a gross cost and raises a rebate by the same amount. The net output should stay fixed even though both intermediates change; require those intermediates too, so a constant net-only cache is insufficient.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) studies compositional generalization; the targeted property is **path cancellation under edits**, not static multi-hop accuracy or an assumed absence of dependence.
- **Cheapest first test:** In a tiny billing world, match intermediate-hop counts and net-answer histograms; vary evidence that the two paths reuse the same rate versus two independent equal rates. Edit a rate used by both paths, compare same-answer parent invalidation controls, and score intermediate changes together with net invariance.
- **Old-task retention check:** Preserve old net bills for the cancellation cases and original behavior of unrelated one-path/partial-rebate cases.

#### 12. An edit can change the reason without changing the answer

- **Mechanism:** Select naturally paired training examples where two independent sufficient rules produce the same outcome but the currently valid explanation changes. A revoked permit can leave a journey legal under a separate exemption; the explanation and any reason-conditioned service must update.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) checks dependent answers, and the parent's invalidation key concerns knowing which cached answers to invalidate. Here **derivation handoff** is scored on a separate existing service (giving the correct grounds), not inferred from whether the binary answer survived.
- **Cheapest first test:** Train with equal answer and explanation QA in both arms, varying whether explanations co-vary with active rules in same-answer contrasts or with changed answers only. Revoke one rule in held-out two-rule cases; compare generic explanation supervision plus uniform crossings at the same budget.
- **Old-task retention check:** Retest old single-rule explanation tasks and independent exemptions, with and without oracle premises.

### C. Teach the same facts through different evidence

#### 13. Put revisions on interchangeable units, not on surface numbers

- **Mechanism:** Select ordinary requests where miles and kilometers (or cents and dollars) describe the same binding, and requests where the same numeral denotes different bindings. A write from one unit should reach the other without changing the meaning of the unit itself.
- **Novelty vs nearest prior art:** [Model Editing with Canonical Examples](https://arxiv.org/abs/2402.06155) tests transfer from canonical examples to harder requests. This isolates **unit conversion tied to fact identity** from generic paraphrase transfer.
- **Cheapest first test:** Use exact integer conversions and match numeral and unit histograms; rewire which matched conversions are demonstrated. Give one formatted edit packet and audit a held-out unit and a same-numeral wrong-key control. Compare with random paraphrase diversity and an explicit normalizer.
- **Old-task retention check:** Probe old free-standing conversion tasks and old numerically equal facts with different units.

#### 14. Cross stable rules with competing sources, not just conflicting values

- **Mechanism:** Build matched examples with disagreement between records where source authority, rather than agreement or recency, decides the binding; rotate which source is authoritative across worlds without changing the rule for choosing it.
- **Novelty vs nearest prior art:** [KAFT](https://arxiv.org/abs/2211.05110) trains models to follow presented context against parametric knowledge. This asks whether **authority × disagreement** examples make a later closed-book authority reassignment cheaper, with no updated source records supplied at inference.
- **Cheapest first test:** In two-source worlds, match candidate values, contradiction counts, latest-source frequency and provenance tokens; rewire valid authority assignments. Later change only which source is authoritative and compare to withheld-context KAFT and selecting by recency.
- **Old-task retention check:** Verify old priority procedures with correct inputs and untouched records with the same source pair.

#### 15. Use meaning-preserving re-encodings as a placebo in training

- **Mechanism:** Sample pairs where representation changes but the binding does not, alongside visually identical edits that truly change a binding (e.g., “07” interpreted as an integer or a string identifier). Balance the semantic and surface distinction so orthography cannot predict change.
- **Novelty vs nearest prior art:** [Rethinking Counterfactual Data Augmentation Under Confounding](https://arxiv.org/abs/2305.18183) analyzes invariant prediction under confounding. This separates **semantic write spillover** from semantic-change sensitivity when the exact same writer has to perform an actual surface update.
- **Cheapest first test:** Match formats and label frequencies, varying which examples reveal semantic equality across formats. Use identical surface-replacement packets across typed worlds and require the updated surface form on direct report; compare collateral on semantic no-ops and propagation on real edits.
- **Old-task retention check:** Check formatting tasks separately from old value-sensitive calculations and literal-code searches.

#### 16. Jointly render evidence without giving the learner new facts

- **Mechanism:** Choose source passages where existing atomic statements and their existing uses are adjacent, versus passages with the same statements beside unrelated uses. Keep example length and the slot of each statement fixed; only the grouping changes.
- **Novelty vs nearest prior art:** [Unobserved Local Structures Make Compositional Generalization Hard](https://arxiv.org/abs/2201.05899) studies which local structures support generalization. This tests **co-publication** as a cause of later coupling or separability when the supervised atomic and consumer examples are already identical.
- **Cheapest first test:** Group equivalent synthetic records into fixed-length windows or rewire the second record by a derangement; counterbalance order and compare with random same-topic adjacency. Remove auxiliary premises at deployment and test novel closed-book changes. Charge any loss of baseline competence rather than crediting weaker coupling.
- **Old-task retention check:** Check old cross-record reasoning and single-record questions, including facts that were never adjacent to their consumers.

#### 17. Teach separable uncertainty rather than a generic “unknown”

- **Mechanism:** Select paired examples where a fact has a known set of possible values but no resolved singleton. Some old procedures give the same answer for every possible value; others legitimately return unresolved. An edit that resolves the singleton should affect only the latter.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tests changed facts and derived facts. This instead tests **sensitivity to resolving a set**, with a separate direct-report floor for the set or member; it is not learning to abstain indiscriminately.
- **Cheapest first test:** In a four-value toll world, swap examples that distinguish invariant and ambiguous derived outputs at equal uncertainty-token count and direct factual QA. Resolve previously unseen sets with the same editor and compare to a generic-unknown control and a hard-coded interval executor.
- **Old-task retention check:** Score still-unresolved facts, old invariant consumers and known exact answers separately; gratuitous abstention counts as damage.

### D. Find which properties survive matched capacity and strong controls

#### 18. Match per-fact entropy; move which bits are shared

- **Mechanism:** Hold value cardinality, frequencies and current answers fixed while changing whether independently editable fields share statistically redundant bits with stable fields. If compression mixes update domains, corpora with the same static entropy should leave different repair bills.
- **Novelty vs nearest prior art:** [Shortcut Learning](https://arxiv.org/abs/2004.07780) describes exploitation of spurious cues; the parent already prices cache versus reader. This is an **invariance test on the unit that gets compressed**: equal entropy per field and the same distribution of pairwise entropies, but different alignment of correlations with the edit boundary.
- **Cheapest first test:** Use exchangeable binary fields, permuting which field is correlated with a stable field while keeping the full joint entropy fixed; counterbalance field names and apply the same edit distribution in both arms. Compare learned hosts to equal-byte joint tables and readers at several capacities without fitting a universal breakpoint.
- **Old-task retention check:** Audit strongly correlated but untouched fields on accurate pre-edit cases, plus rare old cases where the correlation does not hold.

#### 19. Test whether the data helps outside the protection panel

- **Mechanism:** Select old-task examples that supply balanced near-neighbor and far-neighbor coverage around an editable key, rather than only rehearsing its nearest neighbors. The claimed effect is less diffuse damage well outside the editor's protection panel.
- **Novelty vs nearest prior art:** [AlphaEdit](https://arxiv.org/abs/2410.02355) protects knowledge via a projected perturbation. This varies **training coverage outside an unchanged protection panel**; it does not assume damage is sparse or invent a different projection.
- **Cheapest first test:** Match neighborhood counts, margins and static full-panel retention while rewiring across edit domains. Freeze the same protection examples and feature-rank budget in both arms, leaving a nonzero edit subspace. Report damage on disjoint probes at equal efficacy against uniform added data and equal-token neighbor replay.
- **Old-task retention check:** Report old protected and unprotected cases separately, including rare far-neighbor exceptions; a protected-panel win alone does not pass.

#### 20. Can data make a canonical write example less brittle?

- **Mechanism:** Train on unrelated keys using multiple equivalent renderings in which the entity, relation and value appear in systematically different positions, not just lexical paraphrases. Test whether the same one-line correction now works even when the editor's canonical rendering never occurred for that key.
- **Novelty vs nearest prior art:** [Model Editing with Canonical Examples](https://arxiv.org/abs/2402.06155) fixes a canonical training example for an edit and evaluates out of distribution. This varies **pre-edit role/position balance** and looks for a smaller spread of repair costs across interchangeable editor inputs, not just generalization to edited output prompts.
- **Cheapest first test:** Match role-token and position marginals across the whole corpus but vary how many positions each key/relation participates in. Across paired copies of the same learned host, apply one held-out edit under each rendering, rotating renderings identically across arms. Compare against equal-token random paraphrases and a canonicalizer with priced serving overhead if used at inference.
- **Old-task retention check:** Check old requests on held-out renderings after each write, including records that share the edited value token but not its role.

#### 21. Use sacrificial worlds to separate recipe transfer from key memorization

- **Mechanism:** Select evidence in unrelated training worlds that expresses the same abstract update boundary (e.g., group membership versus local price) under disjoint IDs and templates. Compare spending the same budget crossing worlds with spending it on more variation close to the target.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) studies which combinations support static transfer. The proposed **edit-boundary transfer split** tests portability of cheap repair across entire fact schemas, after matching the number of examples and baseline transfer.
- **Cheapest first test:** Use synthetic billing and inventory schemas whose update semantics align, and a counterbalanced donor whose surface statistics match but boundaries do not. Keep target direct data identical and edit only target keys. Compare with generic diversity and equal-budget target-domain crossings; use a distinct selector-development schema.
- **Old-task retention check:** Verify donor procedures, untouched target procedures and old cross-schema tasks; target improvement bought by donor erosion is not a lifecycle win.

#### 22. Try to make a claimed data statistic lose on purpose

- **Mechanism:** Enumerate matched corpus pairs with the same nominated statistic (for example, fallback-depth coverage) but opposite trained edit bills on development worlds. Then use the resulting disagreement to pick an independently manipulable second property, such as how often fallback output and retired payload coincide.
- **Novelty vs nearest prior art:** [GLISTER](https://arxiv.org/abs/2012.10630) selects subsets for generalization. This is an **adversarial equivalence-class audit** of a data property, not a claim that subset optimization itself is new or that a cheap predictor of the bill already exists.
- **Cheapest first test:** Enumerate two small rewiring families, require paired bill separation beyond run noise on development worlds, then preregister a single swapped property and retest it on held-out worlds and writers. Compare with the original statistic, a constant, static competence, and a random swap; charge the development edits. No separation means no predictor claim.
- **Old-task retention check:** Require the bill separation on the common service floors with the same old tasks, check the full randomized cohort too, and reject separation explained by selective loss of old skills.

## Ranked deeper questions

1. **Is there a reproducible data-only reduction in safe revision work, net cost and damage at fixed capacity?** First try one exact matched swap on masked dependence (7) and one on late corrections (6). Both should meet identical service floors; each must compete with equal-budget uniform crossings, KAFT, replay and priced KV. Cross with the fixed editor menu and charge development, failure and serving costs. If the benefit holds for only one writer, report the interaction, not generic editability. If no arm moves the frontier, keep the simpler policy.
2. **What does an example teach the model to edit: a value, an identity, or the domain of the change?** Use withdrawal/fallback, identity and membership (1–4) and reason handoff (12). Match direct correction, then ask which unchanged services move and whether oracle premises rescue the procedure. If ordinary witness count or pre-edit competence predicts the result on held-out worlds, do not introduce another data statistic.
3. **Does data help by making stored bindings writable, by improving propagation, or by teaching procedures to survive writes?** Cross the sign and cancellation contrasts (8, 11) with the compression and dense-audit contrasts (18–19). Require the controlled read/write probes to distinguish those cases. Maximize neither sparsity nor compositional accuracy as a surrogate for a safe edit.
4. **Which data properties predict payback outside the training and editor regime?** Start with donor-schema transfer and the adversarial matched-statistic audit (21–22); freeze any predictor before evaluating held-out schemas, writers and changed event mixtures. Require transfer beyond margin, raw coverage, frequency×hazard and a constant. A cheap statistic with no held-out decision value is a description, not a purchasing rule.
