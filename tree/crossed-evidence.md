# Crossed evidence: when does a skill start reading its facts?

**Status:** ideas only; no experiments, probe code, or GPU. **Parent:** [Fact–skill entanglement, card 13](https://github.com/manojbajaj95/cl/blob/5876f0b415ae95c5ff20fc340229769f866d772b/tree/fact-skill-entanglement.md#13-crossed-evidence-beats-marginal-diversity) ([PR #140](https://github.com/manojbajaj95/cl/pull/140)). **Review seed:** [`reviews/flood-triage.md`, row 227](https://github.com/manojbajaj95/cl/blob/6ff0b560735055be0df470eeeec1bc3fbcfad4d0/reviews/flood-triage.md#L227).

Does a learner switch from storing composed answers to reading a binding because it has seen many values, or because it has seen **the request–value pairings that make the difference matter**? A hundred bridge costs all below a truck's threshold teach the same route choice. Two costs straddling it can disprove that choice as a constant; they do not by themselves prove the learner reads the bridge cost rather than recognizing a world ID. If crossed evidence does induce reading, training for future correction might be cheaper than repairing stale answers after every fact update. If reading still shares storage with the procedure, however, making the skill read is not sufficient to make a weight edit safe.

## What to count, and what would settle it

- **Define witnesses before training.** Let `q` be a canonical request, `v` the binding for a designated fact key, `F(q,v)` the correct answer, and `E` the multiset of skill-training exposures, projected onto `(q,v)` while holding other premises fixed. A witness is `(q,v0,v1)` with `F(q,v0) != F(q,v1)`. It is covered when both crossings occur in `E`. Start with the covered fraction in a preregistered bank of witnesses, with weights derived from a fixed future-update distribution (uniform as a control). Log distinct `k`, exposures per key/query/value, the number of distinguishing requests and which covered witnesses share endpoints. Count multiple phrasings as repetitions, not new canonical witnesses. Keep a disjoint evaluation panel of query–world cells, replacement values and, in a separate split, request families. Coverage is a property of training data and a declared answer function, not a probe of the model.
- **Rewire, don't just add rows.** In the same unpartitioned CPU host, compare low/high witness coverage at fixed `k` and low/high `k` at approximately matched weighted coverage. Keep the fact-QA corpus identical within each fixed-`k) contrast; across `k`, match the QA budget and score on shared keys/values with matched direct recall. Use degree-preserving rewires and random rewire controls; balance global answer counts, world/key frequencies, exposure multiplicities, skill and QA budget, and answer margins where feasible. Example: four requests with answer rows `1100, 0011, 1100, 0011` over four values. Give the first two requests values 1–2 and the last two 3–4 (no covered witness); instead give the first two 1 and 3 and the last two 2 and 4 (four). Same row/column degrees and global labels, **not** the same per-request label frequencies. In stronger tests match request–label frequencies or compare rewires within the same label-diversity class (e.g., redundant witnesses for one value pair vs coverage of different pairs). If nuisance matching is infeasible, report the residual and use a separate balanced contrast rather than crediting coverage alone.
- **Distinguish route from accuracy.** Calibrate on known reader, cache, hybrid and shared-storage hosts; discover the route in unpartitioned models with arbitrary world IDs, not an imposed lookup module. Before intervening, require direct recall of the fact and score both arms on the same competent, matched-margin cases, also reporting the full cohort and matching attrition. On baseline-correct requests where the answer must change, measure exact new-answer rate minus the placebo rate and report exact stale answers and other errors separately. Swap a value without changing the request or world ID, verify direct recall, and test swap-back, same-value and wrong-key placebos plus novel replacements. Require a second perturbation family where feasible: a validated value-only activation intervention and an effective binding write at matched direct recall. Oracle premise supply tests procedure rescue; success from supplying a premise in text is **not** evidence of internal lookup. Match weight-edit norm or report its mismatch. A degenerate world-ID join or a teacher-built KV reader is a control, not spontaneous lookup.
- **Test a switch, don't assume one.** Fit constant, raw-`k`, label-entropy/competence, simple graph, smooth and changepoint alternatives on development cells; predict the intervention response on held-out cells and seeds. Compare with equal-example [KAFT](https://arxiv.org/abs/2211.05110) (contextual steering is a separate route) and degree-preserving random rewires. Report paired uncertainty and how much of the response surface is actually matched. If support and coverage cannot be separated, or smooth models predict as well, report the limitation. An abrupt breakpoint in one toy is not a phase transition.
- **Readability is not editability.** Stream repeated revisions over keys, including reversals, untouched keys, shared consumers and independent procedures. At matched current direct-recall efficacy, report live derived answers, exact stale residues, unrelated old facts, unaffected old requests, old exceptions, and old procedures with the current premises separately. An obsolete answer is not a retention target. Compare exact KV + the same executor (and an oracle executor ceiling), learned retrieval/context supply, replay, and [MEMIT](https://arxiv.org/abs/2210.07229) or a small-host implementation of its editing principle; label the latter as a proxy. Price training examples, edit/search steps, persistent bytes and inference cost. If KV or retrieval ties at budget, use it rather than crediting a more complex intervention. A clean read swap with damage after a weight edit calls for a separate writer investigation, not a cache diagnosis.

**Ledger screen.** Read the [idea ledger](https://github.com/manojbajaj95/cl/blob/6ff0b560735055be0df470eeeec1bc3fbcfad4d0/reviews/idea-ledger.md) first: no raw `k*` law without between-cell variation that beats a constant; no sparse-failure assumption after the MEMIT result; no claims based on margin alone, self-generated replay, a simulator with the switch baked in, or rebranding KAFT as a mechanism. Match simple replay, append-and-retrieve and access to future labels. Prior-art comparisons are scoped differences, not claims of priority; a Coverage Principle result or a standard editor may already explain a candidate's gain. In each card the first test is a proposal, with the common controls above inherited.

## Idea cards

### A. Find what evidence defeats which shortcut

#### 1. Remove witnesses without touching marginals

- **Mechanism:** Use constrained edge swaps to raise or lower witness coverage while preserving degrees and global labels. Cross that change with adding values equivalent on the preregistered requests. Measure whether causal read-through follows witnesses rather than the raw value arm.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) formalizes sufficient training coverage for compositional generalization; [Raventós et al.](https://arxiv.org/abs/2306.15063) vary ICL task diversity. **Candidate primitive:** controlled erasure of a training witness, scored by a closed-book rebind rather than by held-out accuracy.
- **Cheapest first test:** Run the matched 2×2 in one tiny attention model, with shuffled rewires and equal-example KAFT. Require novel-value rebinds that a fitted world-ID answer table cannot predict.
- **Old-task retention check:** After each rebind, retest frozen old request–world pairs on unchanged keys and old vehicle exceptions.

#### 2. Redundancy versus distinct contradictions

- **Mechanism:** Keep the number of mixed-label requests fixed, but expose the same distinguishing value pair everywhere or distribute contrasts across value pairs that future updates are likely to traverse.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) addresses which latent combinations support generalization. **Candidate primitive:** contrast reuse as an experimentally separable quantity, weighted by a future edit workload and tested on causal propagation.
- **Cheapest first test:** With six values, match per-request label histograms and total witnesses; withhold all test cells for one value pair. Compare unique-pair coverage against raw counts and a uniform distinct-pair sampler.
- **Old-task retention check:** Rebind disjoint keys as well and report whether heavily repeated versus singly exposed old behaviors survive equally well.

#### 3. Make the shortcut compete on its own terms

- **Mechanism:** Enumerate competing caches (request-only, world-only, world×request-family, low-rank joint table). For each, count witnesses it cannot satisfy at a fixed capacity. Predict which shortcuts disappear first rather than treating any contradiction as defeating all caches.
- **Novelty vs nearest prior art:** [Shortcut Learning](https://arxiv.org/abs/2004.07780) motivates testing reliance on spurious rules. **Candidate primitive:** a shortcut-indexed witness profile that predicts *which* causal intervention will change the output.
- **Cheapest first test:** Generate two equal-coverage graphs that defeat different shortcut classes; compare their predicted signatures against off-support accuracy and held-out value swaps while sampling new world aliases independently.
- **Old-task retention check:** Preserve old requests where shortcut and reader agree, and separately check existing exceptions on which they disagree.

#### 4. Coverage through narrow graph cuts

- **Mechanism:** Concentrate or disperse separating evidence across cuts between families of requests and bindings; a global count may hide a component that can learn its own codebook.
- **Novelty vs nearest prior art:** [The Coverage Principle](https://arxiv.org/abs/2505.20278) links data structure to compositional generalization. **Improvement:** test whether a contrast-constrained cut predicts cross-component read reuse beyond degrees and ordinary graph connectivity.
- **Cheapest first test:** Match degrees, connectivity, total witnesses and local label diversity where feasible, then move the informative edges across a cut without moving the other edges. Compare a prespecified cut statistic with entropy and ordinary conductance on unseen crossings.
- **Old-task retention check:** Score old tasks on both sides of the cut; reject a global read gain that masks loss in the smaller component.

#### 5. Break leakage by permuting nuisance keys

- **Mechanism:** Assign multiple independently drawn aliases to the same world and vary whether aliases recur across direct QA and skill examples; constrain rebind tests to hold the query and alias fixed. Observe whether a witness effect survives when aliases no longer predict the composed answer across contexts.
- **Novelty vs nearest prior art:** [Rethinking Counterfactual Data Augmentation Under Confounding](https://arxiv.org/abs/2305.18183) studies confounding in augmentation. **Improvement:** independently manipulate alias–answer correlation without changing the semantic witness graph, and demand direct-binding intervention evidence.
- **Cheapest first test:** Cross alias reuse and degree-matched coverage, hold test aliases common across arms, and include an alias-only learner. Give both readers and caches the same accessible canonical lookup key.
- **Old-task retention check:** Retest original alias spellings and untouched entities so alias robustness is not bought by forgetting them.

#### 6. Contrast geometry, not just the count

- **Mechanism:** At fixed witness count, vary whether signed contrasts point in the same direction in a known multi-attribute premise space or span independent decision directions. Ask whether the reader reuses the latter directions on requests with new decision boundaries.
- **Novelty vs nearest prior art:** [What Can Transformers Learn In-Context?](https://arxiv.org/abs/2208.01066) tests generalization over function classes. **Candidate primitive:** a comparison of rank of *observed answer-separating premise differences* with raw premise rank as coordinates for rebind response.
- **Cheapest first test:** In a tiny two-attribute route world, match value covariance and counts; compare collinear versus spanning observed separating pairs on a held-out boundary and at matched direct QA.
- **Old-task retention check:** After changing just one premise component, preserve old requests that depend only on the other component and old joint exceptions.

### B. Tell causal reading from a better cache

#### 7. Rival editors, same relocated fact

- **Mechanism:** Train on the same witness graph, then cross a value-only activation swap with two write families, matching the successful direct recall shifts. A witness effect in swaps alone points to a cleaner reader whose writer still damages skill execution.
- **Novelty vs nearest prior art:** [ROME](https://arxiv.org/abs/2202.05262) localizes and changes associations; [AlphaEdit](https://arxiv.org/abs/2410.02355) constrains edits. **Improvement:** use the parent card 6 read/write distinction to test whether crossed evidence buys interchangeability at read time, write time, or both.
- **Cheapest first test:** Use two witness levels with a validated donor value, a local rank-one update, constrained update and same-norm random write. Require correct oracle-premise execution before interpreting a write as a clean binding change.
- **Old-task retention check:** Measure independent procedures after every intervention, with and without oracle premises, and compare old loss at matched direct correction.

#### 8. A donor the cache never saw

- **Mechanism:** Train donor and recipient with disjoint new premise values but common fact formats; fit a value-state alignment on common direct QA only. Freeze it and transfer a donor-only value to the recipient without any donor skill answers.
- **Novelty vs nearest prior art:** [Distributed Alignment Search](https://arxiv.org/abs/2303.02536) learns alignments to causal variables. **Candidate primitive:** witness-conditioned *transport of new values* across independently trained readers, with alignment denied the receiving skill's answers.
- **Cheapest first test:** Two same-architecture tiny hosts and one alignment trained on common keys. Compare high/low coverage, same-world donors with different bindings, and a same-rank random basis. Do not infer no reader if direct QA transport itself fails.
- **Old-task retention check:** Restrict the swap to one key; score non-target direct facts and unaffected old skills in the recipient.

#### 9. Counterfactual fingerprints on more than one output

- **Mechanism:** Choose replacement values that collide in direct multiple-choice logits or in one consumer but have unique signatures across other consumers. Ask whether one frozen value intervention produces the full new signature.
- **Novelty vs nearest prior art:** [RippleEdits](https://arxiv.org/abs/2307.12976) evaluates edit consequences. **Candidate primitive:** invert the problem: pick a separating signature to rule out single-consumer answer patches or a coarsely encoded binding.
- **Cheapest first test:** Use three consumers and four held-out replacements. Compare observed joint signatures against an answer-cache intervention, a one-consumer alternative, and independently sampled marginal flips; include open direct recall so a multiple-choice collision does not certify a rebind.
- **Old-task retention check:** Keep an old consumer whose correct output is invariant under all four replacements as a negative control; also probe untouched old bindings.

#### 10. Reads can coexist with stale residuals

- **Mechanism:** After a verified value switch, score a panel of three-way outcomes (new, exactly stale, other). Search for a specific stale residual with a separate perturbation trained on paired donors differing in old skill-label exposure, then test whether raising witness coverage shrinks the causally removable component.
- **Novelty vs nearest prior art:** [Parameters vs. Context](https://arxiv.org/abs/2503.15888) distinguishes sources of knowledge reliance. **Improvement:** quantify stale answer dependence remaining *after* a successful internal rebind, not just parametric versus contextual disagreement. This extends the parent's stale-only cut.
- **Cheapest first test:** Calibrate on a hybrid with adjustable cache strength, then test a fixed cut in held-out high/low coverage toys against matched arbitrary cuts. If the cut just adds errors, report unresolved staleness.
- **Old-task retention check:** Keep correct old answers on never-edited worlds and recover the original answer at swap-back without changing unrelated behaviors.

#### 11. The masked fact needed only sometimes

- **Mechanism:** Train requests where a stable policy veto makes the fact irrelevant in some states. In intervention tests toggle the veto independently of the fact: the read need only matter when the veto is absent. Count conditional witnesses separately.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tests multi-hop edits. **Candidate primitive:** a conditional read contract that tests both required propagation and required non-propagation under the same verified binding write.
- **Cheapest first test:** Hold counts of veto states and value crossings fixed while changing where they disagree. Compare unconditional coverage, margin controls, and an oracle-gated executor. Cross the interventions on held-out request/veto combinations.
- **Old-task retention check:** Old vetoed behaviors must stay correct after every rebind, including policy exceptions not used to select witnesses.

#### 12. Find read dependence before (or without) a top-1 jump

- **Mechanism:** Track the paired change in log odds for the exact new answer versus the stale one under diagnostic rebinds as coverage accumulates. Precommit a forecast of subsequent flips on new graphs and seeds; a smoothly strengthening route need not create a mechanistic breakpoint.
- **Novelty vs nearest prior art:** [Progress Measures for Grokking](https://arxiv.org/abs/2301.05217) detects hidden progress before accuracy. **Improvement:** test whether an intervention-derived progress measure predicts future editable behavior better than early margins, elapsed steps or activation decodability.
- **Cheapest first test:** Read three checkpoints in two degree-matched curricula. Evaluate the frozen forecast at the final checkpoint against a constant and smooth dose responses, with direct QA efficacy matched.
- **Old-task retention check:** Track the same old tasks at each checkpoint and after the final edit; exclude top-1 jumps caused merely by baseline competence falling.

### C. Buy the right contrasts, not more of everything

#### 13. Query the example that separates two plausible caches

- **Mechanism:** Fit a small committee of explicit shortcut classes and a candidate reader. Buy the training crossing on which the cheapest surviving shortcuts disagree with the reader most for likely future changes.
- **Novelty vs nearest prior art:** [A-Optimal Active Learning](https://arxiv.org/abs/2110.09585) selects informative queries. **Candidate primitive:** select a witness to defeat an explicit shortcut, then measure information value by a later **different** binding edit, not classification error on the bought label.
- **Cheapest first test:** Budget eight labels and compare with random, uncertainty, uniform coverage and equal-token KAFT. Give all strategies the same candidate pool and price any oracle output required for selection.
- **Old-task retention check:** Run the unchanged old-label panel immediately after adding examples and after the first unrelated update.

#### 14. Reserve contrasts for likely large jumps

- **Mechanism:** Construct pairs at equal unweighted coverage but allocate the witnesses near adjacent values or across likely discontinuous update paths. Freeze the training design before seeing the sampled revision stream.
- **Novelty vs nearest prior art:** [Invariant Risk Minimization](https://arxiv.org/abs/1907.02893) targets prediction stable across environments. **Improvement:** choose the training support by a defined distribution of *rebindings* rather than broad environment coverage and measure the cost of misspecifying it.
- **Cheapest first test:** Train balanced local and long-jump banks on fixed degrees; run both transition distributions and a mismatched one. Compare with matching the marginal value histogram of the expected stream.
- **Old-task retention check:** Report old locality both near and far from frequently edited values; a bias toward expected jumps must not quietly sacrifice the old tail.

#### 15. When two facts change together, buy the missing corners

- **Mechanism:** Two bindings may covary so either alone predicts the final answer. Spend the same sample budget adding isolated changes in each direction or adding joint changes; hold the individual marginal witness rates fixed when testing whether the joint design prevents single-key shortcutting.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) evaluates multiple factual edits and derived reasoning. **Candidate primitive:** a joint training witness that distinguishes independently reading two values from reading one correlated proxy.
- **Cheapest first test:** Tiny route world with two bridge costs and a tie-break policy. Sweep paired versus independent corner coverage and test single-key and joint edits on unseen worlds, including a proxy-only model.
- **Old-task retention check:** After an isolated edit preserve old consumers of the other bridge, unrelated routes, and the fixed tie-break behavior.

#### 16. Buy contrast in one consumer, test another

- **Mechanism:** Expose one of two consumers of the same key to informative pairings while the other sees nondistinguishing diversity. Test whether a shared reader learned by the first makes later edits propagate to the second without giving the second its missing labels.
- **Novelty vs nearest prior art:** [Physics of Language Models 3.2](https://arxiv.org/abs/2309.14402) studies extraction and manipulation of learned knowledge. **Candidate primitive:** a cross-consumer spillover test for the *training intervention*, distinct from the parent's transport of an already learned fact code.
- **Cheapest first test:** Swap which consumer gets informative contrasts with shared and disjoint-key controls. Match second-consumer baseline competence and compare with spending the same examples directly on it.
- **Old-task retention check:** Score old behavior in both consumers, including where their outputs differ for the same fact; accidental imitation is not retention.

#### 17. Change when contradictions arrive, not which arrive

- **Mechanism:** Give both models identical exposure multisets, but one receives both endpoints of a witness in close succession while the other sees them far apart. Equalize update counts and within-batch co-occurrence in a separate arm; use the same shuffled consolidation tail.
- **Novelty vs nearest prior art:** [Data Distributional Properties Drive Emergent In-Context Learning](https://arxiv.org/abs/2205.05055) studies burstiness. **Improvement:** test local spacing of answer-separating pairs for persistent *parametric* read effects, not order-dependent ICL performance or generic hysteresis.
- **Cheapest first test:** Use early versus delayed matches, spacing-matched meaningless pairs and a common tail, with optimizer-state reset as a discriminator. Treat a vanishing effect as a transient.
- **Old-task retention check:** Sample old tasks along the stream and after the common tail, so the same final accuracy cannot hide a temporary service outage.

### D. Use read-through to revise facts without breaking skills

#### 18. Future edit cost as the curriculum objective

- **Mechanism:** Allocate the contrast bank to minimize the expected cost of later revisions: prefer keys for which a one-write policy becomes viable after added evidence, not just the most frequent keys. Freeze the selector before a new sequence of revision events.
- **Novelty vs nearest prior art:** [Understanding the Limits of Lifelong Knowledge Editing](https://arxiv.org/abs/2503.05683) studies sequential editing limits. **Candidate primitive:** choose training evidence by its measured reduction in future *safe edit cost*, including collateral and inference overhead.
- **Cheapest first test:** Use development keys to estimate how a few purchased witnesses change the cost of meeting fixed recall and propagation targets. Hold out keys and event order; compare equal total budget against coverage-only purchase, post-edit replay, MEMIT and retrieval.
- **Old-task retention check:** Impose the same preregistered loss cap for old procedures and facts throughout the stream, not just on the final checkpoint.

#### 19. A release test for where not to write

- **Mechanism:** For a verified binding, use a small held-out witness panel to decide whether to write in place, route through external retrieval with the frozen executor, or abstain. A safe-read result alone cannot authorize a write; require both read propagation and intact oracle-fed execution after a trial write.
- **Novelty vs nearest prior art:** [SERAC](https://arxiv.org/abs/2206.06520) uses a scoped edit memory and [WISE](https://arxiv.org/abs/2405.14768) separates editing memories. **Improvement:** choose between editor and retrieval by an evidence-based separation of stale answers and writer damage rather than query scope alone.
- **Cheapest first test:** Replay a dozen toy revisions with held-out consumers and compare with best fixed writer, cheap ripple-only audit and always-retrieve. Price trial edits and abstentions in latency and missing service.
- **Old-task retention check:** Test genuinely untouched tasks after both chosen and rejected writes in their respective live/shadow models; include old inference when the store is consulted unnecessarily.

#### 20. Retire retrieval only after an independent rebind

- **Mechanism:** Start with verified retrieval while learning crossed evidence. Retire the external dependency only if a sandboxed closed-book rebind to a never-trained value propagates through distinct skill consumers without residual old-answer dependence or procedure loss.
- **Novelty vs nearest prior art:** [KAFT](https://arxiv.org/abs/2211.05110) teaches controlled use of a supplied context; [WISE](https://arxiv.org/abs/2405.14768) addresses lifelong edit memory. **Improvement:** test a graduation rule based on unseen *internal* revisions rather than successful distillation on the current snapshot.
- **Cheapest first test:** Compare graduation by accuracy, by the rebind test and never graduating; score an independent future edit stream and count store calls, audit costs and false graduations.
- **Old-task retention check:** Before and after retirement retest old skills with and without retrieval plus policy exceptions where explicit context is required; do not count lost required overrides as savings.

#### 21. Use revisions as witnesses without copying obsolete answers

- **Mechanism:** Keep compact pointers to pairs of old/new world bindings and the semantic requests they distinguish. For an approved replay step, reconstruct each supervised example with a consistently versioned key and premise, while still serving the latest unversioned value. Do not replay the old answer under the live key.
- **Novelty vs nearest prior art:** [Time Sensitive Knowledge Editing](https://arxiv.org/abs/2406.04496) targets time-conditioned fact recall, and [KAFT](https://arxiv.org/abs/2211.05110) teaches premise following. **Improvement:** test whether realized revisions supply reusable contrasts that improve the *next* internal edit and its downstream propagation, rather than merely teaching time-conditioned recall.
- **Cheapest first test:** Stream three changes; spend equal stored bytes and replay examples on revision witnesses, ordinary versioned replay, matched random crossings and retrieval. Test on an unseen fourth revision, not the stored three.
- **Old-task retention check:** Preserve unaffected old skills and historical answers when explicitly requested, while counting historical answers on current requests as errors.

#### 22. Test whether a safe update is reversible without restoring weights

- **Mechanism:** Drive a key through `v0 → v1 → v2 → v0` using new writes, not checkpoint restore, then compare future `v3` propagation to an unedited twin and a twin with the same total write norm on unrelated keys. Bidirectional success can still conceal accumulated procedure damage or stale competing answers.
- **Novelty vs nearest prior art:** [MEMIT](https://arxiv.org/abs/2210.07229) edits factual associations at scale; [AlphaEdit](https://arxiv.org/abs/2410.02355) targets preservation. **Improvement:** ask whether witness-trained readers retain *next-edit responsiveness* after a closed cycle of effective writes; returning a stored version is not the claim.
- **Cheapest first test:** Run the loop at two witness levels and compare binding-only KV, repeated constrained edits, and replay at matched direct correction. Swap the order of `v1` and `v2` to distinguish path effects from net answer change.
- **Old-task retention check:** Score unchanged old procedures and oracle-fed execution at every cycle leg and after the held-out `v3` edit, even when the final direct `v0` answer is perfect.

## Ranked deeper questions

1. **Does crossed evidence, independent of raw fact diversity, cause closed-book read-through?** Start with the fixed-marginal rewires and crossed `k` arm (1), then try to explain any effect with label mixtures, alias reuse or stronger caches (2–5). Require exact rebind propagation on common held-out cells, two intervention families where possible, and an advantage over KAFT and random rewires. If it only predicts accuracy or contextual compliance, decline the lookup claim.
2. **Is there a portable notion of enough evidence, or only skill- and shortcut-specific response surfaces?** Test conditional witnesses, cut structure and directional geometry (3–6, 11–12); predict a held-out graph and request family with a frozen statistic. Prefer smooth or null fits unless a changepoint improves held-out causal predictions beyond competence and margins; don't infer a universal threshold from toy sharpness.
3. **When does making a skill read actually make facts safer to update?** Separate causal value transport from stale residue and writer-induced procedure damage (7–11). Then compare a frozen release policy with direct MEMIT/replay and KV/retrieval over multiple revisions at matched retention (18–22). If swaps propagate but writes break an oracle-fed skill, keep the reader hypothesis and reject in-place editing for that regime.
4. **Can one purchase less training evidence than fixing the same damage later?** Make witness selection compete with random/KAFT, direct consumer training and a post-edit replay budget (13–18, 21). Test on independently sampled revisions and include acquisition and serving costs. If the selector doesn't beat the best fixed policy at equal retention and total cost, keep coverage as a diagnostic rather than a curriculum.
