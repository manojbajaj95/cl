# Root: learning in deployment, when the learner writes its own weights or memory during live use

**Status:** Ideas only. No learner, CPU or GPU runs. **Tree path:** new root (no parent). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md), including the kill patterns (ties a simple baseline at equal budget, true by construction, margin confound, temperature-matched no-lesson arm, merges must beat stacked baselines). **P** marks a candidate primitive (a new object or operation a family of methods could build on); **I** marks an improvement or a control. Every first test carries an old-task retention check.

**Distance from current lines.** Nothing here concerns optimizer slots, momentum, parks, crossings, inward service, repair/reveal schedules or route folds. The unit of analysis is the live deployment loop: who authored the data a write learns from, when the evidence for a write arrives, where the write is stored, and how old skills are measured with no curated old set.

## Question

A deployed model or agent sees an unlabeled, non-stationary stream that it partly produces itself. It may change weights (fast weights, adapters, full weights) or external memory at any time, with no curated training set and no curated old-task suite. What operations make such learning both useful and safe for old behavior?

## Root cause: in deployment the learner authors its own training data and has no old set to check against

Three facts from the 2026 literature define the gap.

1. **Self-authorship is the failure channel.** [Self-Generated Feedback Destabilizes Test-Time Training (2610.05076)](https://arxiv.org/abs/2610.05076) shows that keeping updates on generated text worsens prediction on independent human text for TTT-E2E (125M–3B) and for Adam on Qwen3-4B, while the same update rule improves on real text. A frozen generator ("Fixed Generation") removes over 98% of the damage at 125M/760M. The same loop drives majority-vote TTRL lock-in and answer extinction ([2611.11165](https://arxiv.org/abs/2611.11165), [2605.19444](https://arxiv.org/abs/2605.19444)) and consistency training entrenching errors ([2606.03810](https://arxiv.org/abs/2606.03810)).
2. **Evidence arrives after the write.** Whether a live write was good (a ticket reopens, a refund, a reverted PR, a user who repeats the question) is known hours or days later. Current TTT, Titans/ATLAS/Nested Learning ([2501.00663](https://arxiv.org/abs/2501.00663), [2505.23735](https://arxiv.org/abs/2505.23735), [2512.24695](https://arxiv.org/abs/2512.24695)), In-Place TTT ([2604.06169](https://arxiv.org/abs/2604.06169)), SEAL ([2506.10943](https://arxiv.org/abs/2506.10943)) and TTRL ([2504.16084](https://arxiv.org/abs/2504.16084)) commit at write time. [Delayed Supervision for Test-Time LMs (2609.32312)](https://arxiv.org/abs/2609.32312) adds delay to *post-training* questions, not to commit decisions in live use.
3. **There is no old set at deployment.** Retention is measured offline on curated suites (ForgetBench [2607.26455](https://arxiv.org/abs/2607.26455), [2603.07392](https://arxiv.org/abs/2603.07392)). A live learner needs a retention meter it can build from its own traffic, or it cannot gate itself.

The research bet: make **provenance** (who wrote a datum), **deferred verdict** (evidence that arrives after commit) and **in-band retention metering** first-class objects of a deployment learner. The cards below are organized by those three objects plus where a write lands.

## Contract and controls (every card)

- **Stream.** Unlabeled live stream with user turns, tool returns and environment observations; real drift, one-off anomalies, private (per-user) preferences and a small share of adversarial users. No curated train or old-task set may be used by the method; a held-out curated old suite is used only by the evaluator.
- **Retention.** Report old-task scores from the evaluator's held-out suite before, during and after the stream (general text perplexity and a fixed old QA/tool suite), plus per-user private behavior for scope cards.
- **Controls at equal exogenous tokens and compute.** (a) frozen model + retrieval memory append; (b) ordinary TTT on all context tokens (TTT-E2E [2512.23675](https://arxiv.org/abs/2512.23675) / In-Place TTT style); (c) TTRL majority vote; (d) SEAL-style self-edits; (e) context distillation of the day's log (Cortex [2610.20399](https://arxiv.org/abs/2610.20399), ASCENT [2610.05303](https://arxiv.org/abs/2610.05303)); (f) periodic reset ([2603.03796](https://arxiv.org/abs/2603.03796)); (g) the interleaved self-holdout gate (card 09). A merge card must beat the stack of its parts' controls.
- **Cheapest tests** use CPU-scale learners: GPT-2 small or Qwen2.5-0.5B with a rank-8 LoRA, linear/MLP hosts for exact checks, or scripted environments (a key-value tool API with drifting semantics, a toy support desk with delayed tickets).

## A. Labels the learner cannot author

### 01. Authorship-masked consequence learning (P)
- **Mechanism:** The only test-time loss is prediction of what the world returns after the agent acts: the tool's output, the next observation, the user's next turn. Tokens the model itself generated get zero gradient, always.
- **Novelty vs nearest prior art:** TTT-E2E and In-Place TTT train on all context tokens; [2610.05076](https://arxiv.org/abs/2610.05076) diagnoses generated-text damage but fixes it with a frozen generator, not a learning rule. Masking by authorship as the *defining* rule of deployment learning, with consequence prediction as the sole target, is not in that work or in TTRL/SEAL, which learn from self-authored targets.
- **Cheapest first test:** Qwen2.5-0.5B LoRA on a scripted tool API whose semantics drift at 3 points; 2k agent steps. Compare masked consequence loss vs control (b) vs frozen + retrieval, on next-call success after each drift.
- **Old-task retention:** Perplexity on held-out human text and 50 old tool calls whose semantics did not change.

### 02. Self-randomized deployment for causal labels (P)
- **Mechanism:** Among responses the agent rates within ε of best, it picks uniformly at random and logs the propensity. Live writes use only importance-weighted contrasts from these designed micro-experiments.
- **Novelty vs nearest prior art:** Counterfactual risk minimization (Swaminathan and Joachims 2015) and logging-policy design ([2605.15108](https://arxiv.org/abs/2605.15108)) are offline. Our G1 (exact-likelihood IS on natural logs) died on ESS < 50. The candidate designs randomization into live use *so that* test-time weight updates have usable ESS, and prices the randomization in regret.
- **Cheapest first test:** Simulated users with a hidden utility over k = 4 candidate responses from a 0.5B model; sweep ε. Report ESS, improvement and regret vs TTRL majority vote at matched regret.
- **Old-task retention:** Reward on non-randomized old prompt categories, plus the evaluator suite.

### 03. Counterfactual next-turn scoring (I)
- **Mechanism:** An online user model predicts the user's reply to each of the k responses the agent could have sent; the observed reply's likelihood under each candidate labels the unsent ones too.
- **Novelty vs nearest prior art:** Follow-up likelihood as reward ([2409.13948](https://arxiv.org/abs/2409.13948)), retrospective learning from interactions ([2410.13852](https://arxiv.org/abs/2410.13852)), RL from user conversations ([2509.25137](https://arxiv.org/abs/2509.25137)) and next-user-turn work ([2608.17499](https://arxiv.org/abs/2608.17499)) use the reply for the sent response. Counterfactual credit for unsent candidates is the delta; it inherits the user model's bias, so labelled IMPROVEMENT.
- **Cheapest first test:** Simulated users with 3 latent intents; compare with single-response follow-up reward at equal turns.
- **Old-task retention:** Evaluator suite and old-intent success.

### 04. Cross-stream replication as the label (P)
- **Mechanism:** Each session computes a local write. A write direction is trusted for shared weights only if it replicates (same sign and support) in independent streams that never saw each other; unreplicated parts stay local to the session or user.
- **Novelty vs nearest prior art:** TIES sign election merges finished task vectors; FedAvg averages; Federated Nested Learning ([2605.16350](https://arxiv.org/abs/2605.16350)) shares self-referential memories; fleet bagging died in the ledger as a tie. Here replication is the *validity test* that separates world change (replicates) from private preference or poisoning (does not), and it decides where each part is stored.
- **Cheapest first test:** 20 simulated users on a 0.5B LoRA, with one shared drift, private preferences and 2 poisoners ([FedPoisonTTP 2511.19248](https://arxiv.org/abs/2511.19248) threat model). Compare with FedAvg, coordinate-median and per-user-only.
- **Old-task retention:** Shared old suite plus each user's earlier private behavior.

### 05. Contradiction-triggered writes (P)
- **Mechanism:** The model writes implications of its beliefs into a pending list. A write fires only when an *exogenous* observation contradicts one; the observation is the label, and the implication graph decides which neighboring beliefs are updated with it.
- **Novelty vs nearest prior art:** Deductive Closure Training (Akyürek et al. 2024) and Self-CTRL ([2606.18327](https://arxiv.org/abs/2606.18327)) train on self-generated implications, which [2606.03810](https://arxiv.org/abs/2606.03810) shows can entrench errors. Here self-generated content never supplies a target; it only routes an exogenous one.
- **Cheapest first test:** Synthetic fact world with 2-hop implications and 30 facts revised over time; compare with plain fact writes and with DCT on the same revisions (RippleEdits-style scoring).
- **Old-task retention:** Unrevised facts and their implications.

### 06. Online source reliability for gradient weighting (I)
- **Mechanism:** Learn per-source trust (each tool, user, document) online from cross-source agreement, Dawid–Skene style, and scale each live gradient by it.
- **Novelty vs nearest prior art:** Truth discovery and crowdsourcing models are standard; dependence-aware discovery exists ([2611.04805](https://arxiv.org/abs/2611.04805)). Applying it to live gradient weighting is an improvement.
- **Cheapest first test:** 5 sources with drifting reliabilities; compare uniform and confidence weighting.
- **Old-task retention:** Evaluator suite.

## B. Writes whose verdict arrives later

### 07. Falsifiable writes (P)
- **Mechanism:** Each live write is stored with a forecast it implies about future natural traffic (for example, "calls to tool X with argument Y will now succeed"). The write survives only if naturally arriving observations confirm the forecast within a horizon; otherwise it is reverted.
- **Novelty vs nearest prior art:** WeightLoop ([2611.07319](https://arxiv.org/abs/2611.07319)) and HypoLoop ([2611.23718](https://arxiv.org/abs/2611.23718)) revise weight-edit plans from *designed* experiments; rollback work ([2609.18304](https://arxiv.org/abs/2609.18304)) rolls back environments. A write that carries its own Popperian test, judged by data the learner did not request, is new.
- **Cheapest first test:** 0.5B LoRA, stream with 5 real drifts and 10 one-off anomalies. Compare keep-all, the self-holdout gate (09), and falsifiable writes on post-stream accuracy and on how many anomaly writes survive.
- **Old-task retention:** After reverts, old QA must return to its pre-write value within seed noise.

### 08. Eligibility traces over committed deltas (P)
- **Mechanism:** Each live write is a separate low-rank delta with a scalar gate. Delayed verdicts (a reopened ticket, a refund) update the gates of all deltas active at the time, using a TD(λ)-style trace, so credit flows to writes rather than tokens.
- **Novelty vs nearest prior art:** Token-level traces for RLVR ([2605.05965](https://arxiv.org/abs/2605.05965)) and delay-aware RLHF ([2606.27580](https://arxiv.org/abs/2606.27580)) work during training. Delayed supervision ([2609.32312](https://arxiv.org/abs/2609.32312)) delays questions, not verdicts on commits. Credit at the level of live weight deltas after deployment is not covered.
- **Cheapest first test:** Exact CPU simulation: 50 writes on a linear host, verdict lags drawn from a heavy-tailed distribution with 20% label noise. Compare immediate commit, wait-then-commit (same verdicts) and gate learning on final loss and on time-to-benefit.
- **Old-task retention:** Old-task loss under the final gated mixture.

### 09. Interleaved self-holdout gate (I, control)
- **Mechanism:** Every k-th live item is withheld from learning and used for prequential validation of pending writes.
- **Novelty vs nearest prior art:** Prequential evaluation (Dawid) and the prequential TTL agent ([2609.35911](https://arxiv.org/abs/2609.35911)). This is the floor every B card must beat at equal labels.
- **Cheapest first test:** As in 07.
- **Old-task retention:** Evaluator suite.

### 10. Declared-effect writes scored on live undeclared traffic (P)
- **Mechanism:** Before committing, the learner declares the input region a write should change. A shadow copy carrying the write scores all live traffic; divergence outside the declared region above a tolerance blocks or reverts the write.
- **Novelty vs nearest prior art:** Editing locality is measured on curated neighborhoods (CounterFact, RippleEdits); the [self-simulated-learning node](https://github.com/manojbajaj95/cl/blob/devin/1795539825-self-simulated-learning/tree/self-simulated-learning.md) predicts edit effects. Here locality is measured on *undeclared real traffic* in shadow, with no curated set.
- **Cheapest first test:** 0.5B; 30 writes, half with planted collateral; detection AUC vs a curated-neighborhood check of equal size.
- **Old-task retention:** Evaluator suite on accepted writes only.

### 11. Active consequence seeking at zero task cost (P)
- **Mechanism:** Among actions rated within ε of best, choose the one whose consequence is most informative about a pending write's validity (expected information gain on its forecast from card 07).
- **Novelty vs nearest prior art:** Information-directed sampling and active inference choose actions for task reward or world knowledge; the [learning-without-gradients node](https://github.com/manojbajaj95/cl/blob/devin/1795551890-learning-without-gradients/tree/learning-without-gradients-at-inference.md) makes the next experiment part of what is learned. The target here is verifying pending writes, limited to task-equivalent actions.
- **Cheapest first test:** Combine with 07's stream; measure time-to-verdict and wrong-survivor count at equal regret.
- **Old-task retention:** As 07.

## C. Where a live write lands

### 12. Retrieval-residual writes (P)
- **Mechanism:** The weight target is only the error that remains after retrieval over the episodic log: outcome minus prediction of (model + retrieved memory). Retrievable facts stay in memory; what retrieval cannot fix (formats, procedures) migrates to weights.
- **Novelty vs nearest prior art:** From Lookups to Lessons ([2611.00450](https://arxiv.org/abs/2611.00450)), RING ([2608.01630](https://arxiv.org/abs/2608.01630)) and Cortex consolidate retrieved or contextual content into weights. A residual-against-retrieval target as the division-of-labor rule is new.
- **Cheapest first test:** 0.5B; stream mixing 200 new facts and 5 new procedures. Compare consolidate-all, memory-only and residual writes on accuracy and adapter norm.
- **Old-task retention:** Evaluator suite; report weight change per unit gain.

### 13. Scope ladder with corroboration counts (P)
- **Mechanism:** Writes start in request scope ([RW-TTT 2605.28053](https://arxiv.org/abs/2605.28053)) and move up to session, user and global scope only after k independent scopes corroborate them (card 04). A global write requires k distinct users, which makes poisoning and privacy leaks scale with k.
- **Novelty vs nearest prior art:** Per-request TTT state and federated personalization exist; a promotion ladder whose rungs are corroboration counts is the delta.
- **Cheapest first test:** As 04, with k ∈ {1, 2, 4, 8}; report shared gain, private retention and poison success.
- **Old-task retention:** Shared old suite and other users' private behaviors.

### 14. Use-to-keep decay of live deltas (P)
- **Mechanism:** Each live delta decays by default. Its decay slows only when it fires *and* the exogenous outcome after firing is good, an analogue of synaptic tagging and capture.
- **Novelty vs nearest prior art:** Titans forgetting gates decay by input surprise; FadeMem ([2601.18642](https://arxiv.org/abs/2601.18642)) decays memory items; Some Memories Must Fade ([2611.25235](https://arxiv.org/abs/2611.25235)) uses a learned offline policy over LoRA ranks. Consolidation conditioned on downstream outcome after use, with no offline policy, is new.
- **Cheapest first test:** Stream of facts with true half-lives from 1 to 1000 steps; compare constant decay, surprise gating and use-to-keep on accuracy over time.
- **Old-task retention:** Long-lived facts and the evaluator suite.

### 15. Volatility-estimated half-lives (I)
- **Mechanism:** Estimate each fact class's revision rate from the stream and set its delta's decay to match.
- **Novelty vs nearest prior art:** Adaptive decay in KGs ([2604.26970](https://arxiv.org/abs/2604.26970)), Engram Injection's temporal validity ([2610.15882](https://arxiv.org/abs/2610.15882)), and Bayesian drift models. An improvement.
- **Cheapest first test:** As 14.
- **Old-task retention:** As 14.

### 16. Live append-only tokenizer growth (P)
- **Mechanism:** Strings that become frequent in the exogenous stream become new tokens, with embeddings initialized by composition and learned by consequence loss. Merges are append-only and never fire on any previously seen string, so old tokenizations are preserved exactly.
- **Novelty vs nearest prior art:** In-place tokenizer expansion ([2607.15232](https://arxiv.org/abs/2607.15232)) is offline; ASR learns new words from unlabeled test data ([2609.28877](https://arxiv.org/abs/2609.28877)); the [interface-change node (PR #115)](https://github.com/manojbajaj95/cl/pull/115) found shared log Z drops old accuracy when outputs are added. Live, unsupervised, old-tokenization-preserving growth is new.
- **Cheapest first test:** GPT-2 small on a stream introducing 50 new product names; bits per character on new text vs a fixed tokenizer.
- **Old-task retention:** Identical tokenization and perplexity on old text, with log-Z conservation from PR #115 as the control.

### 17. Neuromodulated Hebbian deltas on a frozen pretrained LLM (P)
- **Mechanism:** No backprop at test time. Outer-product updates on selected MLP layers, gated by a scalar exogenous outcome signal (a three-factor rule).
- **Novelty vs nearest prior art:** Backpropamine ([2002.10585](https://arxiv.org/abs/2002.10585)), meta-learned three-factor rules ([2512.09366](https://arxiv.org/abs/2512.09366)) and Hebbian plus gradient transformers ([2510.21908](https://arxiv.org/abs/2510.21908)) meta-train the rule. Retrofitting an un-meta-trained rule to a pretrained LLM, with the rule's two scalars set from the stream, is untested.
- **Cheapest first test:** 0.5B on the tool-drift stream; compare with LoRA SGD at equal FLOPs.
- **Old-task retention:** Evaluator suite; Hebbian deltas tend to add interference, so report it per layer.

### 18. Hypothesis sets of live deltas (I)
- **Mechanism:** Keep K candidate deltas (posterior samples), act by Thompson sampling, and prune as evidence arrives.
- **Novelty vs nearest prior art:** Distributions over weight updates ([2610.01934](https://arxiv.org/abs/2610.01934)), multi-hypothesis TTA ([2607.00259](https://arxiv.org/abs/2607.00259)). An improvement.
- **Cheapest first test:** As 07, K ∈ {2, 4, 8}.
- **Old-task retention:** Evaluator suite.

### 19. Consequence model as the only adapted part (I)
- **Mechanism:** Only a consequence predictor learns live; the policy stays frozen and acts by planning with it, so policy retention holds by construction and the risk moves into planning.
- **Novelty vs nearest prior art:** Model-based RL, WebDreamer, OnlineWM ([2609.23753](https://arxiv.org/abs/2609.23753)). An improvement.
- **Cheapest first test:** Tool-drift stream; compare with card 01 at equal compute.
- **Old-task retention:** Policy unchanged; report planning errors on old tasks.

## D. Retention meters without a curated old set

### 20. Nonce canaries as a live plasticity and retention meter (P)
- **Mechanism:** Periodically write a synthetic nonce binding through the same live write path. Its learning speed measures plasticity, its survival measures retention, and relearning savings measure hidden retention. The meter drives the learning rate and resets in closed loop.
- **Novelty vs nearest prior art:** Canaries are used for memorization and privacy ([2610.20656](https://arxiv.org/abs/2610.20656)); binding-specific relearning savings ([2610.22381](https://arxiv.org/abs/2610.22381)) and ForgetBench are offline measurements. An in-band canary that closes the loop on a live learner is new.
- **Cheapest first test:** 0.5B LoRA stream with 20 canaries; does canary decay predict decay of real old facts (Spearman, seed CI) better than parameter-drift norm and loss on self-samples?
- **Old-task retention:** It is the measured quantity; also check that canaries do not cost old accuracy.

### 21. Accepted-answer repeats as a growing retention set (P)
- **Mechanism:** Users repeat or paraphrase earlier queries. When an earlier answer was accepted (task completed, no correction) and the new answer differs, record a forgetting event. These pairs form a free, growing retention set that brakes writes.
- **Novelty vs nearest prior art:** Repeat-query consistency is studied as reliability ([2607.22554](https://arxiv.org/abs/2607.22554)) and within one dialogue ([2610.31314](https://arxiv.org/abs/2610.31314)), not as a live retention set mined from accepted outcomes.
- **Cheapest first test:** Synthetic log with 10% repeats; detection AUC vs an equal-size curated probe set.
- **Old-task retention:** Compare to the evaluator suite to validate the meter.

### 22. Feature-coverage birth certificate (P)
- **Mechanism:** At deployment start, the model generates a small probe set chosen to cover its own internal features (SAE features or neuron activations) and stores its outputs. This set anchors all later writes.
- **Novelty vs nearest prior art:** Neuron coverage comes from DNN testing (DeepXplore [1705.06640](https://arxiv.org/abs/1705.06640)); self-synthesized rehearsal and self-probe gradients ([2609.32771](https://arxiv.org/abs/2609.32771)) match the input distribution. Internal-feature coverage as the criterion for a data-free anchor is new.
- **Cheapest first test:** 0.5B; equal-size anchors (random self-samples, coverage-maximal, real held-out) under the same stream; forgetting on the evaluator suite.
- **Old-task retention:** It is the measured quantity.

### 23. Drift-seeking probes after each write (P)
- **Mechanism:** After each write, search for inputs that maximize divergence between the pre-write and post-write outputs, then distill the old outputs there.
- **Novelty vs nearest prior art:** Data-Free Adversarial Distillation ([1912.11006](https://arxiv.org/abs/1912.11006)) maximizes teacher-student discrepancy for compression; LwF anchors on current inputs. Discrete per-write damage search for live LLM writes is the delta.
- **Cheapest first test:** 0.5B; compare with LwF and random self-sample anchors at equal probe budget.
- **Old-task retention:** Evaluator suite.

### 24. Frozen-generator counterfactual meter (P)
- **Mechanism:** Periodically regenerate a slice of recent self-authored context with the frozen base, compute the update both ways and report the gap as a live estimate of self-induced drift. It decides when card 01's mask or card 26's cross-authorship should switch on.
- **Novelty vs nearest prior art:** [2610.05076](https://arxiv.org/abs/2610.05076) runs Fixed Generation as an offline diagnosis; turning it into an online meter is new.
- **Cheapest first test:** GPT-2 small TTT over 32K-token self-generated streams; does the meter predict human-text loss damage 4K tokens ahead?
- **Old-task retention:** Human-text perplexity is the target.

## E. Breaking the self-authorship loop

### 25. Token-provenance-weighted TTT (P)
- **Mechanism:** Every context token carries a provenance tag (user, tool, environment, self). The TTT inner loss is weighted by provenance: self-authored tokens near zero, exogenous ones up-weighted. This is the layer-level form of card 01.
- **Novelty vs nearest prior art:** SFT masks prompts ([2610.20656](https://arxiv.org/abs/2610.20656) studies the masked context); TTT-E2E, In-Place TTT, Select-TTT ([2610.36794](https://arxiv.org/abs/2610.36794)) select by query relevance, not authorship.
- **Cheapest first test:** Replicate [2610.05076](https://arxiv.org/abs/2610.05076)'s 125M damage on CPU with GPT-2 small, then add provenance weights; report human-text loss vs Fixed Generation.
- **Old-task retention:** Human-text perplexity and an old QA suite.

### 26. Cross-authorship learning (P)
- **Mechanism:** Two models with different pretraining serve alternately, and each learns only from the other's environment-verified outputs, never from its own. The question is whether a *different, also-learning* author is enough to break the loop that a frozen author breaks.
- **Novelty vs nearest prior art:** Co-training (Blum and Mitchell 1998) and mean-teacher TTA (CoTTA [2203.13591](https://arxiv.org/abs/2203.13591), same model family). Cross-authorship as the targeted fix for self-generated TTT drift has not been tested.
- **Cheapest first test:** GPT-2 small and Pythia-160M on the 2610.05076 setup: self, cross, and frozen-author arms.
- **Old-task retention:** Human-text perplexity for both models.

### 27. Exogenous-information budget per write (I)
- **Mechanism:** A write is allowed only if its window contains enough exogenous bits, measured as the model's own surprisal on non-self tokens.
- **Novelty vs nearest prior art:** Titans surprise gating; SelectTTRL ([2610.16104](https://arxiv.org/abs/2610.16104)). An improvement.
- **Cheapest first test:** As 25.
- **Old-task retention:** As 25.

### 28. Exogenously seeded self-practice (I)
- **Mechanism:** The model may generate practice tasks, but only by perturbing real exogenous items and re-querying the tool or environment for the answer, never by self-answering.
- **Novelty vs nearest prior art:** Self-play curricula and tool-verified TTRL ([2603.02203](https://arxiv.org/abs/2603.02203)). An improvement.
- **Cheapest first test:** Tool-drift stream; compare with TTRL at equal tool calls.
- **Old-task retention:** Evaluator suite.

## F. Learning how to learn, live

### 29. Online learning-rule adaptation from prequential regret (I/P)
- **Mechanism:** Learning rate, layer choice and step count of the live rule are adapted online by hypergradients through the last k writes, using future stream loss plus the canary retention term (card 20). There is no offline meta-training.
- **Novelty vs nearest prior art:** Agentic-TTT ([2610.12002](https://arxiv.org/abs/2610.12002)) trains its test-time policy offline; online meta-learning (FTML) and hypergradient descent exist. Coupling to an in-band retention meter is the delta.
- **Cheapest first test:** Linear and MLP hosts with exact gradients; compare with fixed best-in-hindsight LR.
- **Old-task retention:** Canary meter and evaluator suite.

### 30. Overnight consolidation tournament on tomorrow's traffic (I)
- **Mechanism:** During idle time, K candidate consolidations of the day's live writes are built; the next day's first natural traffic selects one.
- **Novelty vs nearest prior art:** Sleep consolidation ([2606.03979](https://arxiv.org/abs/2606.03979), [2604.20943](https://arxiv.org/abs/2604.20943)), population-based training, model soups. An improvement.
- **Cheapest first test:** 0.5B, 5 simulated days.
- **Old-task retention:** Evaluator suite after each day.

### 31. Clarification answers as targeted labels (I)
- **Mechanism:** When the agent asks or defers to a human, the reply is an exogenous label for exactly the uncertain region; only those replies are written.
- **Novelty vs nearest prior art:** Active learning and feedback-efficient TTA ([2610.30643](https://arxiv.org/abs/2610.30643)). An improvement.
- **Cheapest first test:** Simulated users; compare with writing every turn.
- **Old-task retention:** Evaluator suite.

### 32. Provenance-aware memory/weight split (P)
- **Mechanism:** The usual split inverted: self-authored text (plans, reflections) is stored only in external memory, which can be rewritten and audited, while weights only ever absorb exogenous consequences (cards 01, 25). The pairing gives a recoverable audit trail for every weight change.
- **Novelty vs nearest prior art:** Harness and memory CL ([2608.19013](https://arxiv.org/abs/2608.19013), [2607.22157](https://arxiv.org/abs/2607.22157)) keep weights frozen; consolidation work moves self-text into weights. A provenance rule for where each kind of datum may live is new; it must beat the union of the 01 and memory-append controls.
- **Cheapest first test:** Agent on the tool-drift stream with reflections; compare consolidate-everything vs provenance split.
- **Old-task retention:** Evaluator suite and memory size.

## Ranked deeper questions

1. **Is deployment damage specifically self-authorship, and can a learning rule remove it without a frozen author?** Cards 01, 25, 26 and meter 24. Smallest decisive test: reproduce the 2610.05076 damage with GPT-2 small on CPU, then compare provenance weighting, cross-authorship and Fixed Generation at equal exogenous tokens. A yes makes provenance a primitive for all TTT, TTRL and self-edit methods; a no says the damage is generic distribution shift.
2. **Can a deployment learner measure its own forgetting with no curated old set?** Cards 20, 21, 22. Dead if no in-band meter beats parameter-drift norm and loss on self-samples at predicting held-out old-task loss (Spearman, seed CI). Every safe live learner needs this before any gating.
3. **Can verdicts that arrive after commit choose which writes survive better than a self-holdout gate at equal labels?** Cards 07, 08, 11 vs card 09. The exact linear-host version (card 08) runs in minutes.
4. **Does cross-stream replication separate shared world change from private preference and poisoning at small k?** Cards 04 and 13, vs FedAvg and coordinate-median, on shared gain, private retention and poison success.
5. **Where should a live write land?** Card 12's retrieval residual vs consolidate-all: does weight change per unit gain fall while old-task scores hold?
