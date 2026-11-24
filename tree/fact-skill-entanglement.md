# Fact–skill entanglement maps: lookup, compiled answers, or shared storage?

**Status:** research ideas only; no experiments, probe code, or GPU. **Parent:** [Fact-free skill inheritance](fact-free-skill-inheritance.md) ([PR #137](https://github.com/manojbajaj95/cl/pull/137)), especially cards 18–19 (damage and revival) and 3 (diversity). **Review seed:** [`reviews/flood-triage.md`, row 222](https://github.com/manojbajaj95/cl/blob/de645df59dfcfb9694b2584288709d1b4b2edda9/reviews/flood-triage.md#L222).

Can we measure, for a specific fact and a specific skill, whether the skill **reads the current binding**, **memorized the composed answers**, or **uses some of the same storage for the procedure and the fact**? And is there a sharp training-diversity threshold at which a learner starts reading instead of compiling? Lookup and shared storage are not opposites: a skill can read a fact at inference and still share parameters with its storage. A useful map should predict which intervention preserves the skill, not force each pair into one of three boxes.

## What a map would have to distinguish

A bridge-cost fact is `f(w,b) = v` for world `w` and bridge `b`. A route skill should output `P(q,f)`, subject to a fixed vehicle restriction. In a single world, a binding lookup followed by route comparison and a cache of final route choices can agree on every observed request. The same direct fact edit may also break a reused comparison feature. Failed propagation alone cannot distinguish a cache from a missed edit, a redundant read route, or damage to the reader.

- **Read:** Change a candidate internal binding from `v0` to `v1`; confirm first that direct recall actually moved. Score exact *new* choices on queries where the correct old and new choices differ. Swap back and use wrong-key and same-value patches as placebos. Test context supply separately: following text is not evidence of a parametric read.
- **Compiled residue:** After a successful binding change, count exact stale choices on that same slice, not just errors. Look for a second intervention that changes stale outputs without changing direct recall (or evidence from training provenance). Otherwise report unresolved residue, not proven memorization.
- **Storage coupling:** After an effective binding removal or rewrite, test the procedure with correct premises independently supplied, including held-out values. Does damage remain despite restoring the input? In the reverse direction, starting from the same edited weights and fresh optimizer state, does training the procedure on data with no evidence about `v0` raise direct preference for `v0`, relative to equally strong irrelevant training and an old-value-naive control? Revival is evidence of retained dependence, not proof of where it lives; no revival is not proof of separation.

Report these effects with paired uncertainty, by query family and intervention budget, not as a single quadrant label. The parent’s damage/revival quadrants are hypotheses: a pure reader can fail after removal but recover with premise supply; a pure cache need not revive direct fact recall at all. Positive shared-storage evidence must beat matched generic damage and survive more than one intervention family. “Shared” is operational, relative to the allowed interventions; channel overlap or probe decodability alone does not establish it.

## Common first-test contract

- **Calibrate, then discover.** Start with tiny CPU hosts with known read, compiled, mixed and shared routes (including redundant readers); match baseline behavior and capacity where possible. Use these only to calibrate the assay. Test spontaneous route selection in the same unpartitioned MLP or small attention model across conditions. The model sees world and bridge keys, not the target premise value, on closed-book skill queries. Train direct fact QA in all worlds, hold out world × request crossings rather than withholding the facts, and separately evaluate new premise values supplied in context or bound by a verified edit. A world identifier is available to both the reader and the shortcut.
- **Compare like with like.** Keep unique queries, fact-QA examples and optimization budget fixed in diversity comparisons unless explicitly varied; keep answer frequencies balanced where feasible, report residual imbalance, and stratify by pre-intervention margins and competence. For operator comparisons match direct-recall change, steps, update norm and access to labels as closely as possible; show the cost of searching for the intervention and say when matching fails. Fit on one set of pairs; confirm on untouched pairs and whole seeds.
- **Keep the parent’s controls.** Activation-patching census (#137 card 2), matched random fact–skill pairs, simple margin and edit-efficacy predictors, new-fact replay, contextual utility ([Forget to Know, Remember to Use](https://arxiv.org/abs/2510.17620)), and ROME-style edits. Counterfactual-context training (KAFT) at equal examples is a diversity control, not a new proposal. In a successor test include the [#130 disagreement gate](cross-generation-inheritance.md). Score direct correction, stale derivatives, fresh-premise procedure, old-task retention, and reactivation separately.
- **[Idea-ledger screen](https://github.com/manojbajaj95/cl/blob/de645df59dfcfb9694b2584288709d1b4b2edda9/reviews/idea-ledger.md).** Match margins rather than reviving reverse grokking, beat a constant boundary before claiming a threshold law, and allow diffuse collateral damage after the MEMIT result. An explicit fact store and cache are equal-budget baselines and positive controls, not discoveries. The novelty below is the proposed difference from the named work, not a priority claim.

## Idea cards

### A. Identify the routes, not just the symptoms

#### 1. Replace, remove, then independently supply

- **Mechanism:** Build a per-pair contrast from replacement, removal and removal-plus-oracle-premise, each with an unedited twin under the same context. Count exact answer switches and how much procedure loss remains after supply.
- **Novelty vs nearest prior art:** [ROME](https://arxiv.org/abs/2202.05262) traces and edits associations; [Forget to Know, Remember to Use](https://arxiv.org/abs/2510.17620) trains for contextual utility. The candidate primitive is a matched rescue contrast that separates a missing input from damage to its consumer on both the displaced and novel values.
- **Cheapest first test:** Recover the distinctions in the calibrated hosts against the parent’s activation census and direct edit propagation alone; test the inferred edge on a held-out value.
- **Old-task retention check:** Unaffected routes and vehicle exceptions must survive each intervention; premise supply must not change independent answers.

#### 2. Find a stale-only cut

- **Mechanism:** After a verified rebind, swap candidate residual states from a donor that differs only in training on old composed answers; look for a cut that clears exact stale choices while leaving the new direct fact intact.
- **Novelty vs nearest prior art:** [Deep Unlearning](https://arxiv.org/abs/2609.34442) searches for surviving knowledge paths. The candidate primitive is a double dissociation: a direct-binding cut and a separately validated answer-cache cut for the same pair.
- **Cheapest first test:** Use paired donors with and without old composed labels but matched direct-fact exposure; compare to random states and a donor that differs only in direct QA. Reject cuts that simply replace stale choices with arbitrary errors.
- **Old-task retention check:** Measure unaffected skill requests and unrelated direct facts after the cut, at matched direct correction.

#### 3. Redundant-reader unmasking

- **Mechanism:** Replace one candidate binding route at a time, then replace both coherently; for two routes also swap conflicting values. A reader that seems inert alone can be necessary jointly, or one of two backups.
- **Novelty vs nearest prior art:** [Towards Automated Circuit Discovery](https://arxiv.org/abs/2304.14997) prunes computation edges. The candidate primitive is an agreement/conflict signature on *values* that distinguishes backup readers from a cache without relying on zero-ablation damage.
- **Cheapest first test:** Calibrate on two backup readers and a cache with equal single-cut scores. Use equal-size random pair patches and the parent’s single-route census.
- **Old-task retention check:** Coherent and conflicting swaps must leave other fact keys and the old policy rule usable.

#### 4. Transport one fact code across consumers

- **Mechanism:** Learn a value interchange on direct QA and one consumer, freeze it, and test whether swapping in three held-out values makes a second skill compute its own correct answers without changing the query or policy code.
- **Novelty vs nearest prior art:** [Distributed Alignment Search](https://arxiv.org/abs/2303.02536) finds alignments to causal variables. The candidate primitive is *cross-consumer interchange*: no alignment fit on the recipient skill, and one payload must drive distinct functions in both consumers.
- **Cheapest first test:** Compare a shared reader, two independent copies and a mixed host against independently fitted alignments and a same-rank random basis; measure false transfers from sites carrying the world ID.
- **Old-task retention check:** Preserve independent consumers and the recipient’s skill on irrelevant facts.

#### 5. Find a lower bound on unavoidable collateral damage

- **Mechanism:** In a tiny linearized host, solve for the least procedure loss subject to a required direct binding move and a norm cap. Compare the analytic frontier with finite edits and oracle-premise rescue; report the bound only for the declared local intervention class.
- **Novelty vs nearest prior art:** [AlphaEdit](https://arxiv.org/abs/2410.02355) projects edits into a preservation null space. The candidate primitive is a *per-pair infeasibility certificate*: no edit in the allowed class can meet both targets, even if a particular editor is improved.
- **Cheapest first test:** Use a small linear bottleneck with an exact solution, then a nonlinear MLP at two radii. If finite edits routinely beat the local bound beyond linearization error, restrict the certificate to the linear case.
- **Old-task retention check:** Reserve unseen old policies and bridges outside the constraint set; score them at each frontier point.

#### 6. Distinguish shared storage from a shared writer

- **Mechanism:** Cross a value-only activation swap with a weight-space binding edit. If the swap yields a clean read but multiple matched writes hurt an oracle-fed procedure, mark the pair as read-through with write coupling, not compiled.
- **Novelty vs nearest prior art:** [Stability Does Not Mirror Plasticity](https://arxiv.org/abs/2611.23427) reports module-level dissociation. The candidate primitive is separating read-time and write-time edges for the same pair; common edit damage still does not prove shared storage.
- **Cheapest first test:** Contrast a shared feature bottleneck and disjoint read/weight paths with equal accidental edit spillover. Ask whether switching the write family removes the coupling score.
- **Old-task retention check:** Monitor matched-margin old requests and independent facts after activation and weight interventions separately.

### B. Make revival interpretable

#### 7. Counterfactual-isomorphic resurrection

- **Mechanism:** Teach the same procedure on synthetic worlds with fresh symbols and randomized premise assignments independent of the retired value. Contrast target, unrelated and no-update continuations from the same edited weights; test direct recall and derived answers separately.
- **Novelty vs nearest prior art:** [Deep Unlearning](https://arxiv.org/abs/2609.34442) targets retained knowledge paths; [#137 card 18](fact-free-skill-inheritance.md#18-skill-driven-resurrection-test) uses the consumer as a revival trigger. The improvement is making the trigger independent of the particular old value and baselining revival against a value-naive twin.
- **Cheapest first test:** Permute retired values across matched toys; compare post-update old-value preference to [PR #114](https://github.com/manojbajaj95/cl/pull/114) raw-logit and first-gradient reads. Discard any continuation that helps value-naive models guess the assignment.
- **Old-task retention check:** Match acquisition of the benign procedure and check untouched tasks after equal-size updates.

#### 8. A dose–response matrix instead of a quadrant

- **Mechanism:** Measure forward damage and reverse revival at matched fractions of direct correction and several benign training doses. Compare the full curves across editor families; label fragile or editor-dependent edges instead of averaging them away.
- **Novelty vs nearest prior art:** [Forget to Know, Remember to Use](https://arxiv.org/abs/2510.17620) measures the trade-off between forgetting and contextual use. The improvement is checking whether the **ordering** of pairs by damage or revival travels across operators and doses rather than trusting one checkpoint.
- **Cheapest first test:** Compare three doses in two edit families, hold out one dose, and predict stale derivatives against a single-quadrant map and baseline margins.
- **Old-task retention check:** Plot the full untouched-old-task curve alongside the map; discard reconstructions that rely on broad competence loss.

#### 9. Training-data provenance as a third axis

- **Mechanism:** Factorially resample direct fact evidence and skill labels that depend on the old fact, replay the same initialization and schedule, and read the effect of each source on direct and derived answers and on the cut-and-rescue signatures.
- **Novelty vs nearest prior art:** [Physics of Language Models 3.1](https://arxiv.org/abs/2309.14316) controls synthetic biography exposure to study extraction. The candidate primitive is a paired training-source intervention that separates learning a cached answer from relay through an independently taught fact.
- **Cheapest first test:** Four equal-sized corpora; replace removed examples with matched distractors. Compare causal claims from retraining with gradient attribution and direct edits, then validate on new pairs.
- **Old-task retention check:** Keep the old-task curriculum identical and require comparable old skill and direct recall outside the resampled block.

#### 10. Audit observational equivalence before assigning labels

- **Mechanism:** Try to construct two hosts that produce the same outputs, edit responses and revival scores within the audit budget but behave differently on a held-out rebind. Use them to report an abstention region and the intervention that would separate them.
- **Novelty vs nearest prior art:** [Causal Abstractions of Neural Networks](https://arxiv.org/abs/2106.02997) validates alignment by interchange. The candidate primitive is an explicit counterexample to *identification by a bounded audit*, not a claim that two networks are universally indistinguishable.
- **Cheapest first test:** Enumerate tiny lookup/cache mixtures with an aliased value pair; check whether the parent’s map abstains or confidently mislabels them, then add one separating intervention.
- **Old-task retention check:** Equivalence twins must agree on untouched old tasks, not merely on audited fact–skill prompts.

### C. Find (or refute) a diversity threshold

#### 11. Finite-size scaling of causal route choice

- **Mechanism:** Sweep observed premise count `k` at fixed data and steps across several widths. Measure a continuous causal read score after successful rebinding and calibrated rescue, rather than defining lookup by held-out accuracy.
- **Novelty vs nearest prior art:** [Raventós et al.](https://arxiv.org/abs/2306.15063) find a task-diversity threshold for unseen regression tasks in ICL. The candidate primitive is a breakpoint for *parametric causal read-through* with a usable prediction for edit safety.
- **Cheapest first test:** Scout `k = 1, 2, 4, 8, 16`, then densify around the candidate crossing. Compare a changepoint with smooth saturating and no-effect fits on held-out cells, at matched margins and versus equal-example KAFT. Require a shrinking transition band across larger hosts to claim scaling evidence; an abrupt finite toy crossing alone is not an asymptotic phase transition.
- **Old-task retention check:** Require comparable old competence at every `k` and report retention after a fixed-efficacy rebind.

#### 12. Count contrasts the skill can actually see

- **Mechanism:** Construct a request × premise table of legally distinguishable choices. At fixed `k`, vary the number of distinct response signatures; compare rank or entropy of that table with raw value count as the threshold coordinate.
- **Novelty vs nearest prior art:** [Raventós et al.](https://arxiv.org/abs/2306.15063) vary task diversity and structure. The candidate primitive is *consumer-visible* diversity: the same fact’s training support can place one skill above and another below the boundary.
- **Cheapest first test:** Use one skill that bins bridge costs and one whose choices distinguish most costs. Swap in matched values within or across bins; ask whether effective diversity predicts held-out pairs better than `k`, alternative smooth fits and a constant boundary.
- **Old-task retention check:** Both skills must keep old accuracy on nonvarying bridge requests and their respective policy exceptions.

#### 13. Crossed evidence beats marginal diversity

- **Mechanism:** Rewire which requests and premise values co-occur while preserving their degree sequences and balancing answer cells where possible. Test whether coverage of distinguishing crossings, rather than the count of values, forces a reader to emerge.
- **Novelty vs nearest prior art:** [What Can Transformers Learn In-Context?](https://arxiv.org/abs/2208.01066) studies generalization over synthetic function classes and distribution shifts. The candidate primitive is an exposure-graph statistic for a **parametric** cache-versus-read switch at fixed marginals.
- **Cheapest first test:** Compare disconnected blocks, degree-matched random rewires and connected designs, checking held-out crossings in every arm. If a shortcut using world and request IDs still explains the difference, do not call it lookup.
- **Old-task retention check:** Track old held-out combinations outside the rewired block before and after the binding edit.

#### 14. Diversity versus head concentration

- **Mechanism:** Hold support fixed while adjusting how much mass sits on the most frequent value. An effective-support law should transfer between a concentrated large support and a balanced small one; a rare-case gate may instead put both strategies in the same learner.
- **Novelty vs nearest prior art:** [Physics of Language Models 3.1](https://arxiv.org/abs/2309.14316) varies knowledge exposure and extraction. The improvement is a controlled distinction between **prevalence of a compiled route** and exposure-driven quality of a learned fact.
- **Cheapest first test:** Match direct QA sampling across arms and vary only skill exposures; compare entropy, effective support and minimum value count as predictors of head/tail rebind response.
- **Old-task retention check:** Stratify frozen old probes by frequency as well as margin so tail loss cannot be hidden in the aggregate.

#### 15. Search for hysteresis under matched training multisets

- **Mechanism:** Give models the same multiset of examples but arrange curricula from narrow to broad or broad to narrow, then supply identical final mixtures. Compare the read score at matched competence and repeated durations under the common ending.
- **Novelty vs nearest prior art:** [Progress Measures for Grokking](https://arxiv.org/abs/2301.05217) traces the time evolution of a learned algorithm. The improvement is testing for a route boundary that depends on the path through diversity, not rebranding delayed generalization as a phase change.
- **Cheapest first test:** Reverse two short blocks, repeat with shuffled order and fresh optimizer slots at the common tail; reject hysteresis if extra common training closes the gap.
- **Old-task retention check:** Compare old requests and owner exceptions at each common-tail checkpoint; do not treat undertraining as a second stable route.

#### 16. Predict the crossing from competing resource costs

- **Mechanism:** In hosts without imposed read/cache modules, vary the number of distinct answers that would need caching and the length of the fact-to-procedure computation separately. Pre-register where a simple estimated cache cost overtakes a read-plus-procedure cost; measure both using independently calibrated hosts.
- **Novelty vs nearest prior art:** [Towards Understanding Grokking](https://arxiv.org/abs/2205.10343) compares the efficiency of memorizing and generalizing solutions. The candidate primitive is an out-of-family resource prediction for the location of a *causal* route switch, not a post-hoc compression story.
- **Cheapest first test:** Cross two request-bank sizes with two procedure complexities; predict the fourth cell from the others and compare with constant-`k` and margin-only predictors.
- **Old-task retention check:** Require the economical solution to keep unrelated small procedures and policies at matched baseline accuracy.

#### 17. Find a diversity threshold for each inference direction

- **Mechanism:** Independently vary forward and inverse skill exposures around bijective facts, then transpose two bindings so that both directions still have a unique answer. Look for separate read boundaries for forward consumers and inverse consumers even when both have acquired direct QA.
- **Novelty vs nearest prior art:** [The Reversal Curse](https://arxiv.org/abs/2309.12288) demonstrates directional recall asymmetry. The improvement is testing whether *correct* inverse answers are less likely to update causally, not just less likely to be correct.
- **Cheapest first test:** Toy one-to-one bridge/name assignments and route skills called by bridge or by name; match both competence and margins before comparing edit effects. Compare with bidirectional fact-QA training at equal samples.
- **Old-task retention check:** Check untouched facts and both old skill directions; gains in one direction must not conceal losses in the other.

#### 18. Readiness before the accuracy jump

- **Mechanism:** At early checkpoints measure how much an unseen replacement value already moves the skill toward its exact new answer, even if top-1 does not flip. Ask whether this predicts the eventual route switch under higher diversity.
- **Novelty vs nearest prior art:** [Progress Measures for Grokking](https://arxiv.org/abs/2301.05217) finds internal progress before test accuracy changes. The improvement is a pre-threshold *counterfactual* progress measure tested as a forecast rather than inferred after the jump.
- **Cheapest first test:** Freeze an early read-score predictor and evaluate on held-out seeds and `k` values against elapsed steps, raw margins and the parent’s activation census at the same checkpoint.
- **Old-task retention check:** Verify early and late independence on old outputs and retention after the later binding edit.

### D. Put the map to work

#### 19. Predict selective propagation through two-hop chains

- **Mechanism:** Map `f → s1` and `s1 → s2` separately, then predict which final derivatives will go stale when changing `f`. Distinguish a broken upstream read from a downstream cache by swapping the intermediate result.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) and [RippleEdits](https://arxiv.org/abs/2307.12976) evaluate editing consequences. The candidate primitive is an edge map that predicts *where* propagation stops in an unseen composition before the final intervention.
- **Cheapest first test:** Two composable toy procedures with four calibrated read/cache configurations. Compare edge composition against a direct final-output patch and direct single-edit ripple scores at equal intervention counts.
- **Old-task retention check:** Score other consumers of the intermediate and old routes that bypass it after each swap.

#### 20. Test whether map edges travel across generations

- **Mechanism:** Fit the map only on an ancestor, freeze its confidence and operator rule, and evaluate whether it predicts stale derivatives in a successor trained under corrected facts; run a small local recalibration arm to price nontransfer.
- **Novelty vs nearest prior art:** [Physics of Language Models 3.2](https://arxiv.org/abs/2309.14402) studies extraction and manipulation of stored knowledge. The candidate primitive is transfer of an *intervention-response relation* rather than of activations, storage locations or answers; the direct repo comparator is #130.
- **Cheapest first test:** Two tiny successor seeds per exploratory lineage with held-out pairs, then paired confirmation; compare zero-shot transfer, successor-only census and disagreement-gated inheritance at matched observation and update budgets.
- **Old-task retention check:** Score the successor’s pre-existing corrected facts, independent skills and policy exceptions after inheritance, alongside inherited skill accuracy.

#### 21. Price a map by operator regret

- **Mechanism:** Assign each pair an operator from a frozen rule (rebind, rebind plus selective recomputation, or joint repair), abstaining when evidence is weak. Score regret against the evaluator’s best equal-budget operator on each pair and include the cost of building the map.
- **Novelty vs nearest prior art:** [MEMIT](https://arxiv.org/abs/2210.07229) scales one editing family; [MQuAKE](https://arxiv.org/abs/2305.14795) checks multi-hop consequences. The improvement is evidence that the map buys *better operator decisions* than a universal edit or a cheap fire drill, not merely better labels.
- **Cheapest first test:** Hold out fact–skill pairs; compare the frozen full map, its two-axis parent, single-edit ripple audit, randomized routing and the best constant operator at matched amortized budget. Use hidden new-world labels only for scoring.
- **Old-task retention check:** Compare regret only under the same old-task loss cap (start with the parent’s 2 pp), and show old tasks for abstentions too.

#### 22. Buy a contrast or buy a repair?

- **Mechanism:** For pairs near the inferred boundary, choose one new training contrast predicted to resolve ambiguity about the read route. Compare using that example before expiry with spending its cost on the best edit after expiry; predict which intervention will win before seeing the next world.
- **Novelty vs nearest prior art:** [Invariant Risk Minimization](https://arxiv.org/abs/1907.02893) seeks invariant prediction across environments. The candidate primitive is a targeted choice of a *separating premise contrast* whose value is measured by a later causal rebind, beyond generic counterfactual augmentation.
- **Cheapest first test:** Among pairs with equal initial fault rate, allocate a contrast using the map, at random, or by KAFT at equal examples; include after-expiry replay at equal total steps. Evaluate on a separately sampled replacement, not the example used for selection.
- **Old-task retention check:** Measure unaffected old requests both at install and after expiry; a targeted contrast must not just trade retention now for easier edits later.

## Ranked deeper questions

1. **What is the smallest intervention set that identifies a pair well enough to choose an operator?** Start with replace/remove/rescue and label-independent revival (1, 5–10). Try to break identification with redundant routes and equivalent hosts (3, 10). If the map cannot beat the census and matched random pairs on held-out edits or operator regret (21), report which distinctions are unresolved rather than assigning storage labels.
2. **Is there a sharp, predictable boundary in causal read-through rather than just a smooth rise in held-out accuracy?** Test finite-size sharpening and changepoint prediction against smooth, margin-matched and KAFT controls (11, 18). Then ask whether consumer-visible diversity or crossed coverage (12–14) predicts the boundary across skills. If the width or location does not transfer, report a response surface, not a universal `k*`.
3. **Can training history select a different route at the same apparent diversity and competence?** Cross curriculum order, capacity costs and inference direction (15–17). A persistent difference after common training and slot reset would make a single diversity threshold incomplete; vanishing differences favor a transient or exposure account.
4. **Can entanglement edges be composed, inherited, or used to prevent stale derivatives cheaply?** Require a frozen map to predict held-out hops and successor edits (19–20), then beat the best fixed-budget operator or counterfactual augmentation (21–22). If route labels transfer but decisions do not improve at matched retention, keep the map as an assay, not a repair policy.
