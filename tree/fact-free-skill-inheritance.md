# Fact-free skill inheritance: forget the outdated fact, keep the skill that used it

**Status:** research ideas only; no experiments, no probe, no GPU. **Parents:** [Fossil beliefs](fossil-beliefs.md) ([PR #132](https://github.com/manojbajaj95/cl/pull/132)) and [Cross-generation inheritance](cross-generation-inheritance.md) ([PR #130](https://github.com/manojbajaj95/cl/pull/130)). **Seeds:** cross-pool round 24 FI1 ("when a premise expires, discard the binding rather than the procedure", `ideas/flood/cross-pool-24.md`, [PR #36](https://github.com/manojbajaj95/cl/pull/36)) and its verdict in [`reviews/flood-triage.md`](https://github.com/manojbajaj95/cl/pull/6) row 217, which keeps FI1 with the controls *new-fact replay, MEMIT/ROME-style edits, lookup-only fact slots and the #130 disagreement gate, all at matched update budget*.

**Scope.** The parents ask which teacher signals a successor should copy so that it does not take on the ancestor's old world. This node asks the complementary operator question inside one learner (or one successor right after inheritance): **when a fact expires, what update removes the stale binding without removing the procedure that read it, and without leaving stale answers compiled into the skill?** It is not knowledge-edit propagation in general, not privacy unlearning, and not a new architecture with a separate fact store presented as if it won by construction.

## The problem in one example

A route ranker learns a procedure `P(q, f)`: rank routes for request `q` given world facts `f` (which bridges are open) and an owner policy (the fleet's vehicle restriction). It was trained only in world `W0`, where bridge `b` is open (`f0`). Then `b` closes (`f1`). We want three things at once:

1. **Fact forgotten or replaced.** Asked directly, the model no longer asserts `b` is open. It answers `f1` if it has been told, or abstains.
2. **Procedure kept.** On requests whose answer depends on `b`, it computes `P(q, f1)`. On held-out premises it never saw (another bridge closing) it computes `P(q, f')`. When `f` is supplied in context it uses it.
3. **No stale derivatives.** Ranked answers that were correct only because `b` was open (`P(q, f0)` where `P(q, f0) ≠ P(q, f1)`) are gone, including paraphrases and multi-step uses.

Old-task retention means requests whose answer does not depend on `b`, other skills, and the owner policy exception all stay as they were.

**Why this is hard (root cause).** A network trained only under `f0` can realize the skill in two ways that give identical outputs in `W0`:

- **Read-through:** look up the binding `b ↦ open`, then run the procedure on it.
- **Compiled:** store `q ↦ P(q, f0)` directly (the composition has been memoized), with no read of `b`.

Deleting the binding fixes a read-through skill and does nothing to a compiled one (stale derivatives survive, as in the deep-unlearning result that forgotten facts stay recoverable through derived paths, [2609.34442](https://www.alphaxiv.org/abs/2609.34442)). Damaging the shared read path to delete the binding breaks a read-through skill everywhere (procedure lost). Real models hold a mixture, query by query. This is the fossil-beliefs identifiability problem moved inside one model: **outputs under `W0` alone cannot tell a compiled skill from a read-through one, so a forgetting operator that does not first measure which one it faces must either leave fossils or break the skill.** Every card below is a bet about a cheap measurement or operator that resolves this.

## Prior-art and ledger screen

Quick alphaXiv screen (2026-11-25), used to set controls, not to claim priority:

- **Unlearning that keeps use-in-context.** [Forget to Know, Remember to Use (2510.17620)](https://www.alphaxiv.org/abs/2510.17620) adds a plug-in term so a model that has unlearned a fact can still use *that same fact* when it is supplied in the prompt. That is the nearest neighbour. The target here differs: the procedure must run on **other** premise values, including held-out ones, and compiled stale derivatives must go. Its contextual-utility term is a required control.
- **Pretraining without parametric facts.** [Knowledgeless LMs (2607.12831)](https://www.alphaxiv.org/abs/2607.12831) anonymize named entities in pretraining; closed-book recall collapses while contextual QA holds or improves. [Intern-S2-Mobius (2608.14290)](https://www.alphaxiv.org/abs/2608.14290) decouples a shared FFN memory from attention reasoners. Both prevent facts from being stored instead of removing one after the fact; a fact-free architecture winning by construction is the ledger's frozen-backbone pattern, not a result.
- **Where facts and procedures live.** [2611.23427](https://www.alphaxiv.org/abs/2611.23427) finds a double dissociation (MLPs most plastic for declarative facts, QK/VO for procedures) but stability that does not mirror plasticity: updating VO for a new procedure loses about four fifths of stored facts. [2510.24256](https://www.alphaxiv.org/abs/2510.24256) separates memorization in low-curvature weight directions. Module or curvature selection is a control, not a contribution.
- **Edits and their consequences.** ROME/MEMIT ([2202.05262](https://arxiv.org/abs/2202.05262), [2210.07229](https://arxiv.org/abs/2210.07229)), null-space-constrained AlphaEdit ([2410.02355](https://arxiv.org/abs/2410.02355)), ripple-effect benchmarks MQuAKE ([2305.14795](https://arxiv.org/abs/2305.14795)) and RippleEdits ([2307.12976](https://arxiv.org/abs/2307.12976)), knowledge editing through reasoning over background stories ([2602.02028](https://www.alphaxiv.org/abs/2602.02028)), the two-hop curse for fine-tuned facts ([2611.01519](https://www.alphaxiv.org/abs/2611.01519)), and propagating updates through distillation ([2306.09306](https://www.alphaxiv.org/abs/2306.09306)). Edited facts are often suppressed rather than erased ([2609.18985](https://www.alphaxiv.org/abs/2609.18985)) and come back under relearning ([2502.05374](https://arxiv.org/abs/2502.05374)).
- **Unlearning operators.** Gradient ascent, NPO ([2404.05868](https://arxiv.org/abs/2404.05868)), TOFU-style abstention ([2401.06121](https://arxiv.org/abs/2401.06121)), Selective Synaptic Dampening ([2308.07707](https://arxiv.org/abs/2308.07707)), LEACE concept erasure ([2306.03819](https://arxiv.org/abs/2306.03819)), task-vector negation ([2212.04089](https://arxiv.org/abs/2212.04089)), SISA sharding ([1912.03817](https://arxiv.org/abs/1912.03817)).
- **Fact stores.** Sparse memory finetuning ([2510.15103](https://www.alphaxiv.org/abs/2510.15103)), temporal validity of parametric memory, Engram Injection ([2610.15882](https://www.alphaxiv.org/abs/2610.15882)), and old-value failures when context changes ([2609.38866](https://www.alphaxiv.org/abs/2609.38866)).
- **Idea ledger ([PR #6](https://github.com/manojbajaj95/cl/pull/6)).** Counterfactual-context training is KAFT (Li et al. 2022) and gets no novelty claim (R1). Match per-item margin before attributing any forgetting order (reverse grokking, cooldown facts). Ties against replay, append-plus-retrieve or save/restore at equal budget are deaths. Damage after edits is diffuse, not sparse ([PR #24](https://github.com/manojbajaj95/cl/pull/24): top 10% of facts held 19% of damage energy), so localization cards must allow a broad repair. Relearning as a read head is top-10 #5; first-gradient and raw-logit shortcut controls apply ([PR #114](https://github.com/manojbajaj95/cl/pull/114)). Order and history effects need a nonlinear host and a reported relaxation time ([PR #121](https://github.com/manojbajaj95/cl/pull/121)). No generator-identity claims (self-quizzing tied). Every first test carries a retention check.
- **Siblings not to duplicate.** Fossil-beliefs cards 6 (expiring fact slots), 7 (role-equivariant operators), 17 (historical namespace) and 18 (reactivation audit); FI3 (fossils in optimizer slots) and FI5 (archives) from round 24; edit transfer ([PR #76](https://github.com/manojbajaj95/cl/pull/76)).

## Shared first-test contract (CPU, NumPy)

- **Host.** A nonlinear MLP (or two-layer transformer) route ranker over a small graph. Inputs: request `q`, an optional in-context premise field, and owner policy bits. World facts (edge open/closed) are learned parametrically from fact queries `"is edge e open?"`. Train skills under a mixture where some edges' status varies across training (read-through is learnable) and some is fixed (compilation is possible). Hold out premise *combinations* and whole edges.
- **Event.** One or more facts expire (`f0 → f1`). The method receives the same evidence as its controls: the fact queries for `f1` (or an instruction to forget `f0`) and an update budget fixed in steps × update norm. Skill labels under `f1` are visible only to the evaluator and to the oracle arms.
- **Five numbers, always.** (1) fact score: `f1` or abstention on direct and paraphrased fact queries; (2) **stale-derivative rate**: share of `b`-dependent skill queries still answered `P(q, f0)`; (3) **procedure score on fresh premises**: accuracy of `P(q, f')` for held-out `f'`, both supplied in context and bound parametrically; (4) **untouched old tasks**: `b`-independent skill queries, other skills and policy exceptions; (5) **reactivation**: stale-derivative rate after `k ∈ {1, 4, 16}` benign later updates (skill-only data in `W1`, unrelated tasks).
- **Controls, at matched budget.** New-fact replay (fine-tune on `f1` fact queries plus self-labelled skill examples), gradient ascent and NPO with retain loss, the 2510.17620 contextual-utility term, a rank-one ROME-style edit and AlphaEdit null-space edit adapted to the toy's MLP, SSD, a lookup-only fact store (retrieval over an explicit table) at equal bytes, the #130 disagreement gate when there is a generation hop, and two oracles: retrain from scratch on `W1` data, and full-data fine-tune.
- **Statistics.** At least 8 paired seeds, paired CIs; replicate a surprise at 10 or more seeds before explaining it. Match margin when comparing which queries forget first. A card passes a first screen only if it beats the best control on (2) or (3) at no more than a 2 pp loss on (4) and no worse (5).

## Research ideas (23 cards)

### A. Measure what the skill compiled before forgetting anything

#### 1. FI1 developed: premise-swap directions and a routed damping budget

- **Mechanism:** Train `m` cheap scratch copies for a few steps each on self-labelled skill data under swapped values of the expiring fact (`b` open, closed, and placebo swaps of irrelevant edges). The span of `Δθ_swap − Δθ_placebo` estimates the directions that move premise-dependent answers. The span of updates under *held-out* premises of other edges estimates procedure directions. Spend a fixed damping budget (shrink toward a reference, or step on new-fact replay) only in the first span projected off the second. Keep a separate public policy input so owner restrictions are never treated as facts.
- **Novelty vs nearest prior art:** ROME/MEMIT find where a fact is stored by causal tracing of the *fact query*; SSD and AlphaEdit protect a retain set they observe. Here the protected set is the procedure under **counterfactual premises nobody has observed yet**, estimated from the model's own learning response to swapped worlds, and the forgetting budget is allocated rather than spent on whatever the fact query's gradient touches. Primitive candidate: a premise-equivariance contrast as the unit of forgetting.
- **Cheapest first test:** The shared host with one bridge closure and an owner vehicle restriction. Compare against new-fact replay, rank-one edit, AlphaEdit, a lookup-only store and an equally tuned generic projector (top-k Fisher of fact queries) at matched update norm. Sweep `m ∈ {2, 4, 8}` to price the scratch copies in the budget.
- **Old-task retention check:** Untouched requests, the policy exception and procedure on two held-out closures; report at matched stale-derivative rate so the method cannot win by forgetting less.

#### 2. Compiled-versus-read census per query

- **Mechanism:** For each skill query, measure two responses: (a) the output change when the premise is swapped in context, (b) the change when the internal binding is patched (activation patching of the fact representation found by fact-query tracing). Read-through queries respond to both; compiled queries respond to neither; context-only readers respond to (a) only. The census picks the operator per query: rebind for read-through, recompute-and-retrain for compiled.
- **Novelty vs nearest prior art:** Activation patching and MQuAKE-style ripple tests measure whether an edit propagated *after* editing. The census is taken *before* forgetting and predicts which queries will become stale derivatives. Improvement as a tool; primitive if the census transfers across facts.
- **Cheapest first test:** Build hosts where the read/compiled split is known by construction (status varied versus fixed per edge in training). Score the census by AUROC for "becomes a stale derivative after binding edit", against input-gradient saliency on the premise field and first-gradient magnitude (PR #114 control).
- **Old-task retention check:** The census must not change the model (read-only); then check (4) after the operator it selects.

#### 3. A diversity threshold for forget-safe skills

- **Mechanism:** Train the skill while the fact takes `k` distinct values over training. Predict a threshold `k*` above which the network computes `P(q, ·)` (read-through) rather than memoizing, by analogy with the task-diversity transition for in-context learning ([2306.15063](https://arxiv.org/abs/2306.15063)). A skill trained above `k*` can have its fact forgotten safely; below it, forgetting needs recompute (card 11).
- **Novelty vs nearest prior art:** The ICL task-diversity work measures generalization to new tasks, not what survives deleting a binding. Using `k*` as a certificate of forget-safety is new. Study unless `k*` is predictable from a cheap install-time quantity; then primitive.
- **Cheapest first test:** Sweep `k ∈ {1, 2, 4, 8, 16}` and width; after forgetting `f0` measure (2) and (3). The card dies if there is no sharp transition or if it moves with width so much that it cannot be predicted.
- **Old-task retention check:** At each `k`, report (4) before and after forgetting, so a skill that is read-through only because it is weak overall does not count.

#### 4. Decompile, then forget (order effect)

- **Mechanism:** Before removing `f0`, run a short counterfactual-premise phase that makes the skill read-through (self-distill `P(q, f')` from in-context premises into the no-context path); then apply the forgetting operator. Measure the minimum decompile dose that makes forgetting safe and whether doing it after forgetting (repair) costs more.
- **Novelty vs nearest prior art:** The counterfactual phase itself is KAFT (no novelty claimed). The bet is the **order effect**: decompile→forget beats forget→repair at equal total steps, because once the binding is gone the compiled answers no longer have a consistent target. Improvement.
- **Cheapest first test:** Both orders at matched total steps and the same data; plus a matched-step new-fact replay arm.
- **Old-task retention check:** (4) after each phase separately, so a transient drop is visible.

#### 5. Fire drill on a scratch copy

- **Mechanism:** At install time, for each fact the deployment declares volatile, simulate its expiry on a scratch copy (cheap forgetting operator, few steps) and record which skills break. Use the drill's outcome to decide per fact whether to train its consumers read-through, store it in a lookup, or accept compilation.
- **Novelty vs nearest prior art:** PreUnlearn ([2606.18473](https://www.alphaxiv.org/abs/2606.18473)) and the edit-simulator node (PR #63) forecast unlearning and edit effects. The difference is acting on the forecast *before* the fact expires, changing how the skill is trained. Improvement; must beat first-order response and a constant baseline (PR #63 rule).
- **Cheapest first test:** Drill 20 facts, act on the 5 worst; compare with acting on 5 random facts and on the 5 with the largest fact-query gradient norm at equal budget.
- **Old-task retention check:** Training consumers read-through must not cost (4) on stable facts.

### B. Operators that remove the binding, not the reader

#### 6. Unbind the key instead of rewriting the value

- **Mechanism:** Learn a reserved "unbound" region of the key space whose meaning the procedure is trained to interpret as "consult the premise field or abstain". Forgetting moves the stale fact's key into that region (a rank-one key-side edit) rather than writing a new value.
- **Novelty vs nearest prior art:** ROME/MEMIT edit the value for a key; abstention unlearning trains the *fact query* to say "I don't know". Here deferral is a state the *procedure* consumes, so every downstream use defers at once, including ones never enumerated. Primitive candidate.
- **Cheapest first test:** Linear associative memory plus MLP reader. Compare value edit to `f1`, value edit to abstain, gradient ascent and key unbinding on (2), (3) and on paraphrased fact queries.
- **Old-task retention check:** Keys near the moved key (neighbouring edges) keep their facts; unrelated skills unchanged.

#### 7. A typed "unknown" premise the procedure can consume

- **Mechanism:** During skill training include a value `⊥` for each fact with a defined safe behaviour (look up, ask, take a conservative route). Forgetting maps `f0 ↦ ⊥`, never to an arbitrary other value, and the skill degrades gracefully until the new fact arrives.
- **Novelty vs nearest prior art:** TOFU-style IDK unlearning makes outputs abstain; fossil-beliefs card 4 asks one clarification question. The new part is giving `⊥` to the **procedure as an input value**, so forgetting has a well-defined downstream semantics. Improvement unless `⊥`-training transfers to facts never trained with `⊥`.
- **Cheapest first test:** Train `⊥` on half the edges; forget one edge in the other half. Compare abstention unlearning and gradient ascent on detour cost and failure rate.
- **Old-task retention check:** Requests on known edges must not become conservative (over-detouring is a retention failure).

#### 8. Make the output invariant to the model's own belief

- **Mechanism:** Locate the internal fact representation (probe or tracing), then train the no-context output to be invariant to patching that representation with sampled alternative values, while the with-context output must follow the premise field. The belief stops mattering, so it is forgotten functionally; the procedure stays because the with-context path is supervised.
- **Novelty vs nearest prior art:** LEACE erases a concept linearly from a representation and degrades whatever reads it; 2510.17620 keeps the same fact usable in context. This card erases the belief **as an input to a procedure** while keeping the procedure's conditional behaviour. Primitive candidate if the invariance generalizes to paraphrased probes.
- **Cheapest first test:** Compare with LEACE on the fact representation, with the 2510.17620 term and with gradient ascent at matched steps; measure probe recoverability of `f0` (decodable but unused counts as partial).
- **Old-task retention check:** Other facts stay decodable and used; (4) after training.

#### 9. Selective dampening against a synthesized retain set

- **Mechanism:** SSD dampens parameters whose importance for the forget set greatly exceeds their importance for a retain set. Replace the observed retain set with a **synthesized procedure set**: skill queries under premises sampled from a world model the deployment declares (other edges closed, random restrictions).
- **Novelty vs nearest prior art:** SSD needs retain data and protects what it sees; the procedure under future premises is unseen. Improvement; it must beat SSD with the best observed retain set at equal samples.
- **Cheapest first test:** One closure; SSD with observed retain data, SSD with synthesized procedure data, card 1 and new-fact replay.
- **Old-task retention check:** (3) on premises outside the synthesis distribution, to catch overfitting to the sampler.

#### 10. Deconsolidation: move compiled facts back into a store

- **Mechanism:** Systems with a fast fact store and slow procedure weights (SMF, memory layers) still compile facts into slow weights over time. Periodically run the census (card 2) on slow weights and, for compiled facts marked volatile, train the slow path to read the store instead (a reverse consolidation), so later expiry is a store overwrite.
- **Novelty vs nearest prior art:** Consolidation always goes fast→slow (complementary learning systems, SMF, ENGRAM). Eviction slow→fast as a maintenance operation for forget-readiness is the bet. Primitive candidate; must beat an append-plus-retrieve store that never consolidated at equal bytes (ledger rule).
- **Cheapest first test:** A host with a key-value store and an MLP that compiles over 2,000 steps; deconsolidate every 500 steps; then expire 10 facts.
- **Old-task retention check:** Throughput and accuracy on stable facts with the store present and absent, since deconsolidation must not make the model dependent on a store it may not always have.

#### 11. Truth maintenance for derived answers

- **Mechanism:** When a fact expires, enumerate the model's own derived conclusions that depended on it (generate skill queries touching `b`, keep those whose answer changes when `f1` is supplied in context), and retrain exactly those to the recomputed answers, with a small retain sample.
- **Novelty vs nearest prior art:** Truth maintenance systems (Doyle 1979) do this symbolically; deep unlearning (2609.34442) severs derived paths; 2306.09306 distills a context-supplied fact into its implications. The difference here is **using the model's own in-context procedure as the recomputation oracle** and stopping when the census says no compiled dependants remain. Improvement; new-fact replay with generated implications is the close control.
- **Cheapest first test:** Compare targeted recompute against generated-implication replay and uniform skill replay at equal examples.
- **Old-task retention check:** Derived answers on unaffected edges, and paraphrases never used in the recompute set.

### C. Train so that skills do not compile volatile facts

#### 12. Premise dropout with an "uncertain" target

- **Mechanism:** During skill training, randomly mask the premise path for facts declared volatile and train the masked output toward the calibrated mixture over premise values. A skill that can still answer confidently with the premise masked has compiled the fact and is penalized.
- **Novelty vs nearest prior art:** Knowledgeless LMs remove entity facts from all pretraining; shortcut-learning regularizers target spurious features. This targets **only declared-volatile facts at fine-tune time**, as a forget-readiness property. Improvement; the cost on stable facts is the price to report.
- **Cheapest first test:** Dropout rates `{0, 0.1, 0.3}` on volatile facts; expire one; measure (2) and (3) and the install-time skill score.
- **Old-task retention check:** Skills on non-volatile facts must keep their accuracy and latency.

#### 13. A premise bottleneck with a measured price

- **Mechanism:** Force all fact information the procedure uses through a narrow typed code (a few discrete premise slots) and add an information penalty on skill output given that code. Forgetting edits only the code.
- **Novelty vs nearest prior art:** Concept bottleneck models ([2007.04612](https://arxiv.org/abs/2007.04612)) and Mobius-style decoupling separate stages for interpretability or scaling. Here the bottleneck is scored by **forgetting cost** (steps and collateral to expire a fact) versus no bottleneck at equal parameters. Improvement; wins by construction only if the bottleneck is perfect, so leakage around it must be measured.
- **Cheapest first test:** Equal-parameter MLPs with and without the bottleneck; leakage = mutual information between output and fact identity given the code.
- **Old-task retention check:** Install-time accuracy on all skills; a bottleneck that costs more than 2 pp at install fails.

#### 14. Volatility-aware learning rates

- **Mechanism:** Estimate per-parameter covariance between gradients and fact identity across premise-swapped batches. Give high-covariance parameters a higher learning rate and stronger decay (the binding stays easy to rewrite) and low-covariance parameters a lower one (the procedure stays put).
- **Novelty vs nearest prior art:** Meta-SGD ([1707.09835](https://arxiv.org/abs/1707.09835)) and La-MAML learn per-parameter rates for fast adaptation; two-timescale methods split by module. The partition is estimated **from premise-swap statistics**, aiming to make future forgetting cheap. Improvement.
- **Cheapest first test:** Steps needed to bring the fact score to 90% after expiry, and (2)–(4) at that point, against module-split rates (MLP versus attention, after 2611.23427) and uniform rates.
- **Old-task retention check:** New-task acquisition between expiries, to show the procedure is not simply frozen.

### D. Fact-free inheritance across generations

#### 15. Teach the successor only in alien worlds

- **Mechanism:** When passing a skill from ancestor `F0` to successor `B1`, query `F0` only with premises supplied in context and drawn from randomized worlds that are neither `W0` nor `W1`. The successor learns the conditional procedure without ever seeing the ancestor's world values, then binds to its own facts.
- **Novelty vs nearest prior art:** Fossil-beliefs card 7 enforces role equivariance and card 1 buys separating queries; DistillMIKE and data-free KD use edited or synthetic inputs. Here the **teaching distribution excludes the ancestor's world on purpose**, so no fact value can transfer. The risk is the ancestor's procedure being unreliable off its world; measure it. Improvement unless it beats the gate on fossils at equal skill.
- **Cheapest first test:** The PR #130 probe with an in-context premise field added. Compare with the disagreement gate, plain KD and a `W1`-conditioned ancestor at equal queries.
- **Old-task retention check:** The parent's four numbers, especially untouched old tasks of `B1`.

#### 16. An alien-world certificate as the inheritance gate

- **Mechanism:** Before accepting an inherited skill, test it on premise values that never co-occurred with that skill in any generation's training. A skill passes only if its behaviour on alien premises matches the ancestor's in-context behaviour on the same premises; failures mark compiled parts to be relearned rather than copied.
- **Novelty vs nearest prior art:** Compositional generalization benchmarks (SCAN, COGS) test generalization in general; the certificate is a **gate for what may cross a generation**, tied to the fossil rate. Primitive candidate as an evaluation object.
- **Cheapest first test:** Does the certificate's failure set predict which inherited behaviours will become fossils after a later world change (AUROC), against disagreement magnitude?
- **Old-task retention check:** Gate-rejected skills must be relearned without the successor losing its untouched tasks.

#### 17. Programs with fact holes

- **Mechanism:** Distill the skill into a short program or sketch whose volatile premises are typed holes, carry the program across the generation, and re-instantiate it in the successor by filling holes from the successor's own beliefs (round-trip consolidation back into weights, top-10 #8).
- **Novelty vs nearest prior art:** Program Distillation ([2611.19461](https://www.alphaxiv.org/abs/2611.19461)) is one-way; agent workflow memory ([2409.07429](https://arxiv.org/abs/2409.07429)) already abstracts workflows with placeholders. The bet is holes **typed by volatility** and the return trip into weights. Moonshot for neural skills; doable for agent skills.
- **Cheapest first test:** Agent variant: skill notes with and without typed premise holes, one premise expiring; success on the next 50 tasks.
- **Old-task retention check:** Tasks using non-expired premises, and notes untouched by the expiry.

### E. Verify forgetting is real and stays gone

#### 18. Skill-driven resurrection test

- **Mechanism:** After forgetting `f0`, fine-tune briefly on **skill-only** `W1` data (no fact queries) and measure whether direct fact answers revert to `f0`. If skill training revives the fact, the fact lives inside the skill's weights; the revival rate is an entanglement measure, and an operator is accepted only if it keeps it low.
- **Novelty vs nearest prior art:** Relearning attacks (2502.05374) revive unlearned facts with related data; top-10 #5 uses relearning as a read head. The new part is using the *consumer skill* as the relearning set, which separates "fact stored with the procedure" from "fact stored alone". Improvement as an audit; PR #114's raw-logit and first-gradient decoders are required controls.
- **Cheapest first test:** Apply it to all controls of the shared contract after one expiry; check that it ranks them differently from the immediate fact score.
- **Old-task retention check:** (4) after the skill-only fine-tune, so a revival test that damages the model is caught.

#### 19. Entanglement asymmetry map

- **Mechanism:** Measure both directions per fact–skill pair: how much forgetting the fact damages the skill, and how much retraining the skill revives the fact. Read-through gives (high, low), compiled gives (low, high), shared representation gives (high, high). Use the quadrant to pick the operator family (cards 1, 6, 11).
- **Novelty vs nearest prior art:** Card 2 uses interventions at one time; 2611.23427 measures module-level asymmetry for whole task families. This is per pair and drives the choice of operator. Improvement; primitive if quadrants are stable across seeds and widths.
- **Cheapest first test:** Constructed read/compiled/shared hosts; check quadrant recovery, then whether operator choice by quadrant beats the best single operator.
- **Old-task retention check:** As in the operators chosen.

#### 20. Clean the optimizer, not just the weights

- **Mechanism:** A stale binding can sit in momentum and second-moment slots and return after the next write (FI3). After forgetting, reset or reproject optimizer slots only along the binding directions from card 1, leaving procedure directions' slots intact.
- **Novelty vs nearest prior art:** FI3 asks whether fossils return through slots; this card is the repair once card 1's directions exist. Full optimizer reset is the control. Improvement.
- **Cheapest first test:** Adam host; compare no reset, full reset and direction-scoped reset on (5) at `k = 1, 4, 16`; report relaxation time (PR #121 rule).
- **Old-task retention check:** Learning speed on the next task, since a full reset costs warm-up.

#### 21. Historical reads that cannot leak into the default

- **Mechanism:** If a dated question ("was the bridge open in 2020?") must keep working, give it a separate, dated query path and train the undated path to be invariant to it. Measure leakage after later updates with paired path ablations.
- **Novelty vs nearest prior art:** This is fossil-beliefs card 17 and FI5 applied to the forgetting operator: the check is whether the operators above keep historical answers without reviving the default. Improvement; included because every operator here must report it.
- **Cheapest first test:** Add dated fact queries to the host; run cards 1, 6 and 8; measure undated stale answers and dated accuracy.
- **Old-task retention check:** Dated answers for facts that did not change.

### F. Wilder bets

#### 22. Forgetting as schema migration

- **Mechanism:** Treat each volatile fact as a schema field and each skill as a query over the schema. Expiry is a migration: the model generates a migration function (old derived answer → new derived answer) from its in-context procedure, and the migration is applied to its own outputs during a short self-distillation, like a database rewrite of materialized views.
- **Novelty vs nearest prior art:** Incremental view maintenance in databases updates materialized views when base tables change; card 11 recomputes answers one by one. The bet is that a **compact migration rule** generalizes to derived answers never enumerated. Moonshot unless the toy shows the migration transfers to held-out queries.
- **Cheapest first test:** Route host where closing `b` maps routes through `b` to a fixed detour; learn the migration from 20 queries and test on held-out queries versus card 11 with the same 20.
- **Old-task retention check:** Views not touching `b` stay the same.

#### 23. Paired twins that disagree only on the fact

- **Mechanism:** Maintain two copies trained identically except the volatile fact (`f0` in one, `⊥` or a random value in the other). The procedure is whatever the twins share; at expiry, merge by averaging only along directions where the twins agree, taking the binding from the `⊥` twin.
- **Novelty vs nearest prior art:** Model soups and task arithmetic average whole models; card 1 estimates directions from short scratch runs. The twins carry the contrast for the model's whole life, so compiled dependence on `f0` never forms in the shared directions. Improvement; the cost is two models, so the control is one model twice as wide.
- **Cheapest first test:** Twin merge versus card 1 and versus a double-width single model with new-fact replay at equal FLOPs.
- **Old-task retention check:** (4) after the merge; merging can wreck nonlinear models, so check linear mode connectivity first.

## Ranked deeper questions

1. **Is a skill trained under one value of a fact identifiable as a procedure at all, and how much premise diversity makes it so?** Cards 2, 3 and 16. Build hosts with known read/compiled splits; find `k*` and check whether a cheap install-time census predicts stale derivatives. If no measurement separates the realizations, report that as an impossibility in the toy and stop operator work that assumes it.
2. **Can a fixed forgetting budget be routed onto the binding so that the procedure survives on held-out premises at a matched stale-derivative rate?** Cards 1, 6, 8 and 9 against new-fact replay, ROME-style and AlphaEdit edits, SSD, a lookup-only store and the 2510.17620 term at matched update norm. This is FI1's claim; it advances only if it beats every one of these on (2) or (3) with ≤ 2 pp on (4).
3. **Where do stale derivatives live, and do they return when the skill is trained again?** Cards 18, 19 and 20, with relaxation times. If skill-only training revives the fact for every operator, forgetting inside shared weights is suppression, and the honest answer is a store plus deconsolidation (card 10).
4. **Is it cheaper to prevent compilation at training time than to undo it at expiry?** Cards 4, 12, 13 and 14: install-time cost on stable facts versus expiry-time cost on volatile ones, over a stream of several expiries.
5. **Does the answer survive a generation hop?** Cards 15–17 on the PR #130 probe with the parent's four numbers plus the stale-derivative rate, against the disagreement gate.
