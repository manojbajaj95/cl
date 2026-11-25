# Population continual learners 3: Coupled writes and separable synergy

Depth 2 · 28 candidate primitives · **Ambitious but doable** · Ideas only; no experiments run

**Parent:** [#380](https://github.com/manojbajaj95/cl/pull/380) kept two cards at 3, neither at 4: [PL2-03, paired common-mode write](population-learners-2.md#pl2-03--paired-common-mode-write--ambitious-but-doable-p) and [PL2-27, synergy quarantine](population-learners-2.md#pl2-27--source-tagged-nonlinear-interaction-quarantine--ambitious-but-doable-p). Both descend from [#379](https://github.com/manojbajaj95/cl/pull/379). This node proposes new write operations, parametrizations and training signals. **P** means candidate primitive, not a novelty verdict.

## Literature and experimental boundaries

Checked the linked arXiv titles and abstracts. The differences below are against those mechanisms, not exhaustive novelty claims. The following controls apply throughout each branch.

- **A: Coupled writes.** Match inputs on legitimate choices; evaluate new task gain separately from choices. Compare the original joint write with **separate forks**, independent projection, same-probe recipient [OGD](https://arxiv.org/abs/1910.07104), [PCGrad](https://arxiv.org/abs/2001.06782), [FOT](https://arxiv.org/abs/2309.01289) and [TIES](https://arxiv.org/abs/2306.01708). [MGDA-style MTL](https://arxiv.org/abs/1810.04650), [CAGrad](https://arxiv.org/abs/2110.14048) and [Nash-MTL](https://arxiv.org/abs/2202.01017) are strong product-space controls: give them the same two patches and available objectives, not a deliberately weaker single model. An advantage must come from what the operation lets the forks learn or preserve, not additional parameters or more probes. Protect each fork’s decision as well as the signed difference; a common shift can preserve the difference while flipping an action.
- **B: Synergy quarantine.** Compare flat PL2-27, [task negation](https://arxiv.org/abs/2212.04089), teacher-free replay, [SISA](https://arxiv.org/abs/1912.03817) and [TracIn](https://arxiv.org/abs/2002.08484)-ranked removal followed by the same recovery budget (TracIn by itself is attribution, not removal). [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes feature interactions; [partial information decomposition](https://arxiv.org/abs/1004.2515) distinguishes redundant, unique and synergistic information. Neither makes a trained interaction causally teacher-dependent by itself. Use capability and teacher-only side-effect readouts, and report unknown when intervention or source coverage is missing. A clean child starts from allowed weights and optimizer state and gets no expired-teacher outputs, internal features, teacher-selected curriculum, or inherited teacher supervision. Historical artifacts can be used to measure the old behavior, not to train or select the clean child. This is selective dependency retirement, not certified data erasure.
- **Both:** Freeze untouched A/B before adaptation, including an old local task per fork or source regime. Match effective storage, observations, update FLOPs and serving cost; report a higher-budget oracle separately. A tie with the closest simpler method drops the primitive claim.

## A · Learning a move that takes two forks

### PL3-01 · Functional gearbox — Ambitious but doable (P)
- **Parent failure → mechanism:** Solving in raw weights makes one fork pay more merely because it uses wider layers or a different scale. Learn a common-effect coordinate z with one small decoder per fork. Update z on the new task and decode it into two minimum-cost local patches, regularizing the decoders to realize the same *measured* matched-contrast change.
- **Nearest prior / gap:** [LoRA](https://arxiv.org/abs/2106.09685) factorizes local updates; [shared-module MTL](https://arxiv.org/abs/2005.00944) shares representations. This bottleneck shares an update coordinate without sharing the inference representation or the underlying delta.
- **Cheapest first test:** Pair a narrow linear head with a scaled, redundant head. Compare separate rank-matched adapters and an unconstrained latent decoder on a new shared nuisance transform.
- **Old-task retention:** Score A/B and both held-out choices after three writes and one rescaling of the redundant head.

### PL3-02 · Opposed rails inside the adapter — Ambitious but doable (P)
- **Parent failure → mechanism:** A newly shared feature can accidentally carry the majority’s preference. Parameterize each patch as a common feature path plus a signed private path. Route shared task gradients only into the common path after averaging across matched preference flips; train the private path only on the antisymmetric residual.
- **Nearest prior / gap:** [Shared-plus-private MTL](https://arxiv.org/abs/2005.00944) shares a trunk with separate output modules. This mechanism splits *gradient evidence from the same paired examples* into even and odd components rather than allocating whole data sets to shared and private heads.
- **Cheapest first test:** Linear multitask toy with shared parity and opposite response conventions. Match rank against a shared trunk with private heads and against PL3-01’s shared update latent.
- **Old-task retention:** Score A/B and policy flip accuracy after the shared parity write and a local convention update.

### PL3-03 · Constraint-breaking escape slot — Ambitious but doable (P)
- **Parent failure → mechanism:** If no pair of existing weight directions realizes a useful common move, projections return zero. Grow one dormant residual slot per fork. Fit both slots on shared errors, subtract their per-fork guard-span components at the slot’s output, then train only the remaining read vectors.
- **Nearest prior / gap:** [OGD](https://arxiv.org/abs/1910.07104) projects updates into existing safe directions; [LoRA](https://arxiv.org/abs/2106.09685) inserts low-rank capacity. The slot builds a new callable feature whose output is zero on guards by construction, rather than projecting an old delta or adding unconstrained rank.
- **Cheapest first test:** A rank-limited toy whose original feature space is exhausted by guards. Compare an ordinary extra adapter, OGD with the same added rank and the paired escape slots.
- **Old-task retention:** Score A/B off the guard points and on fork-specific slices after the slot becomes active and after a second write.

### PL3-04 · Cross-fork compensation gradient — Ambitious but doable (P)
- **Parent failure → mechanism:** Each patch can look locally safe while changing how the other fork will learn from it. Differentiate the recipient’s *one-step post-copy response* back through the donor update. This lets a donor learn a lesson that the partner can adopt without flipping its decision, instead of sending a fixed delta for rejection or projection.
- **Nearest prior / gap:** [PCGrad](https://arxiv.org/abs/2001.06782) performs surgery on current task gradients; [CAGrad](https://arxiv.org/abs/2110.14048) looks for a direction with useful local improvement. This is a gradient through a second learner’s adaptation step, not a different tradeoff among first-order losses.
- **Cheapest first test:** Two tiny heads share a latent feature, but copying the obvious donor step drives one toward a wrong local threshold. Compare stop-gradient and same-compute projection of the fixed copy.
- **Old-task retention:** Score both forks’ A/B after the actual recipient step and after two subsequent reciprocal lessons.

### PL3-05 · Curvature-split common flow — Ambitious but doable (P)
- **Parent failure → mechanism:** A shared infinitesimal tangent can split at finite step size. Write each patch as a shared functional first derivative plus a private quadratic correction. Fit the correction to cancel the second-order gap drift, then integrate both patches over the same step interval.
- **Nearest prior / gap:** [OGD](https://arxiv.org/abs/1910.07104) guards a gradient locally; [Adam-NSCL](https://arxiv.org/abs/2103.07113) projects updates in feature null spaces. The paired quadratic term actively *continues* the shared trajectory rather than shrinking or rejecting the step at a boundary.
- **Cheapest first test:** Two smooth two-layer heads with equal first-order response but different curvature. Compare matched-compute repeated small projected steps and exact joint constrained optimization on the toy.
- **Old-task retention:** Score A/B after the finite move and its next continuation, including guards held out from fitting.

### PL3-06 · Two-speed inference patch — Ambitious but doable (P)
- **Parent failure → mechanism:** One fork can absorb a shared lesson immediately while the other needs local adaptation. Apply a jointly fitted fast residual in logit space to both; train a slow private weight patch per fork from the *increment*, removing that fork’s fast residual in proportion to the learned effect. The other fork can finish at a different time.
- **Nearest prior / gap:** [Distillation](https://arxiv.org/abs/1503.02531) fits a student to teacher predictions; [BTX](https://arxiv.org/abs/2403.07816) assembles experts and tunes routing. Here each branch learns a shared effect while maintaining its own baseline with a continuous, effect-matched handoff.
- **Cheapest first test:** Two shallow classifiers, one deliberately data-starved. Compare serving a permanent shared residual, synchronous distill-and-drop and separate weight adaptation.
- **Old-task retention:** Check A/B and action stability mid-handoff, after the first fork finishes and after both finish.

### PL3-07 · Antithetic coupled policy step — Ambitious but doable (P)
- **Parent failure → mechanism:** A joint optimizer cannot backpropagate through discrete actions or a black-box partner. Encode paired candidates along a common-effect direction and evaluate both signs of each perturbation on the same randomized episode in both forks. Update from their reward difference only on episodes where the paired candidate preserves both old actions; shrink unsafe directions rather than treating policy violations as low reward.
- **Nearest prior / gap:** [Evolution strategies](https://arxiv.org/abs/1703.03864) estimate policy updates from perturbed returns. This version samples *coupled* moves and conditions their effect on paired action feasibility, rather than perturbing and ranking full policies independently.
- **Cheapest first test:** Two tabular policies get noisy simulator rewards and expose no gradient. Compare independent random search, unconstrained joint random search and common seeds without paired feasibility at equal episodes.
- **Old-task retention:** Score A/B with fresh simulator seeds on both forks after multiple accepted perturbations.

### PL3-08 · Directional write exchange — Ambitious but doable (P)
- **Parent failure → mechanism:** Requiring the same *full* functional response overconstrains the joint write. Learn a low-dimensional action-neutral response subspace where motion must match, and let each fork fit orthogonal task responses privately, provided action decisions do not flip. Train the shared subspace by held-in interventions that alter task difficulty without changing preference.
- **Nearest prior / gap:** [FOT](https://arxiv.org/abs/2309.01289) learns layer-input subspaces for global retention; [shared-module MTL](https://arxiv.org/abs/2005.00944) separates features and heads. Here the subspace says which output effects are interchangeable *between updates*, not which activations are shared or which inputs must not move.
- **Cheapest first test:** Shared nuisance correction plus fork-specific auxiliary outputs. Compare full-response coupling, fixed hand-picked output coordinates and gradients from nuisance augmentation alone.
- **Old-task retention:** Check A/B and untouched policy dimensions after changing which auxiliary output each fork uses.

### PL3-09 · Paired inverse update — Ambitious but doable (P)
- **Parent failure → mechanism:** Even well-coupled updates become irretractable after subsequent writes. Put the shared component in invertible residual layers with a single effect coordinate and distinct local maps. If a local invertible suffix S follows the shared write F, apply the conjugate S ∘ F⁻¹ ∘ S⁻¹ to the current composition on each fork; this removes F without dropping S. Outside the invertible interface, use rollback and replay, not this identity.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) negates a parameter vector; [Model Soups](https://arxiv.org/abs/2203.05482) average model parameters. Neither comparator uses a paired, compositional inverse in two distinct inference paths; full replay remains the reachability oracle.
- **Cheapest first test:** Two tiny models with triangular affine residuals and a known later noncommuting edit. Compare subtraction, removing F by its bare inverse, and rollback/replay with conjugated removal.
- **Old-task retention:** Score A/B immediately after recall and after reapplying the intervening local skills.

### PL3-10 · Conjugated local policy heads — Ambitious but doable (P)
- **Parent failure → mechanism:** A shared move can be representationally useful yet disrupt preferences downstream. Learn an invertible small feature transport S from shared examples, then conjugate each protected linear head by S inverse as the feature map is updated by S. Train new task heads in the moved coordinates; release compensation only where local supervision authorizes a change.
- **Nearest prior / gap:** [BTX](https://arxiv.org/abs/2403.07816) mixes independently trained experts; [LoRA](https://arxiv.org/abs/2106.09685) adapts selected layers. This operation pairs an upstream change with an exact downstream rewrite for the protected readout, rather than relying on experts or hoping regularization holds. Exact invariance is restricted to the stated linear interface.
- **Cheapest first test:** Two linear policies on rotated features; use a fixed low-rank new head so a useful rotation changes its reachable directions. Compare fixed-head OGD and separately trained adapters.
- **Old-task retention:** Score A/B and both protected old readouts through three rotations, including a near-singular transform excluded by design.

### PL3-11 · Tangent-capacity bargaining — Ambitious but doable (P)
- **Parent failure → mechanism:** A fixed overlap coordinate can repeatedly spend one fork’s scarce safe directions. Learn the common update as the solution of a bargaining objective over *remaining usable tangent dimension after the write*, with new-task gain as a floor. The forks can switch which physical direction carries the next shared change.
- **Nearest prior / gap:** [Nash-MTL](https://arxiv.org/abs/2202.01017) bargains over a joint task update; [MGDA-style MTL](https://arxiv.org/abs/1810.04650) seeks Pareto-stationary gradients. The proposed utility is capacity left for future independent rewrites, not immediate task improvement alone.
- **Cheapest first test:** Two nonlinear heads with equal first-step gains but one solution saturates the activation carrying a safe direction. Compare Nash-MTL with current gains and plain joint minimum norm at the same current gain.
- **Old-task retention:** Score A/B after the selected write and after a second, differently targeted shared lesson.

### PL3-12 · Shared lesson as a two-output optimizer — Ambitious but doable (P)
- **Parent failure → mechanism:** Re-solving the coupling from scratch assumes each pair’s geometry is novel. Train a tiny update generator on earlier pairs to emit two low-rank patches from shared example gradients plus each fork’s guard gradient. Its training loss includes both post-write task gains and the cost of restoring the paired contrast after each proposed update.
- **Nearest prior / gap:** [LoRA](https://arxiv.org/abs/2106.09685) supplies the low-rank representation; [CAGrad](https://arxiv.org/abs/2110.14048) optimizes from present gradients. The learned object maps pair geometry to *two* patches, trained on cross-pair transfer instead of choosing one update direction.
- **Cheapest first test:** Meta-train on synthetic linear forks differing by random rotations, hold out rotations and dimensions. Compare a learned single-fork optimizer run twice, a fixed joint solver and a same-budget shared coefficient mixer.
- **Old-task retention:** Score A/B for unseen pairs after several consecutive generated writes, not only for meta-training pairs.

### PL3-13 · Split saturation activations — Ambitious but doable (P)
- **Parent failure → mechanism:** At a saturated or near-boundary local choice, a useful common step cannot safely enter through the same scalar channel. Introduce two activation inputs per protected margin: a bounded common term computed from each fork’s available decision slack and an unbounded private policy term. Shared gradients can move the common term only within the paired feasible range; private gradients retain their full channel.
- **Nearest prior / gap:** [MoE-LoRA](https://arxiv.org/abs/2502.15828) mixes low-rank experts; [PCGrad](https://arxiv.org/abs/2001.06782) alters gradients. This instead projects the realized common activation during inference, so fitting can proceed without a shared patch crossing a protected boundary.
- **Cheapest first test:** Scalar-margin toy with a steep local threshold. Compare a functionally similar hard clamp, penalty-based training and separate experts. Require any benefit beyond just bounding a scalar.
- **Old-task retention:** Check A/B across the previously saturated region after shifting the shared nuisance distribution.

### PL3-14 · Error-correcting common residual — Ambitious but doable (P)
- **Parent failure → mechanism:** A joint write may need simultaneous delivery; a partial local update can change shared effects before its partner arrives. Fit each branch’s patch as a base share plus a locally computed correction that maps its current output increment onto the agreed common increment. Train the correction with random missing-share masks, without reading live partner state.
- **Nearest prior / gap:** [DARE](https://arxiv.org/abs/2311.03099) randomly drops and rescales delta parameters; [BTX](https://arxiv.org/abs/2403.07816) trains expert routing. The share here learns to reconstruct a *named effect after partial delivery*, with the same action constraints as a delivered pair, not just tolerate static sparsity.
- **Cheapest first test:** Two redundant linear heads under independent message losses. Compare retransmission, simple replication and DARE-style random dropping at equal average bytes and inference cost.
- **Old-task retention:** Check both forks’ A/B during missing-share windows and after delayed delivery and a later local write.

## B · Learning the interaction again without its expired teacher

### PL3-15 · Source-subset residual layers — Ambitious but doable (P)
- **Parent failure → mechanism:** By expiry, a teacher interaction may have diffused across all weights. From the start, parameterize the learned response as a base, source-specific residuals and nonlinear conjunction residuals. Train each conjunction on the difference of differences across feasible source subsets, with gradients stopped into the main effects on the conjunction step. Disable residuals involving the expired teacher and refit a new allowed-only conjunction from scratch.
- **Nearest prior / gap:** [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes feature interactions; [SISA](https://arxiv.org/abs/1912.03817) isolates training influence. This directs interaction gradients into detachable weights before expiry rather than computing attribution after entanglement.
- **Cheapest first test:** Fit an additive-plus-XOR toy with two sources and a later third clean source. Compare data shards, ordinary adapter slots and post-hoc subtraction at the same rank. Restrict the factorial signal to combinations with observed support.
- **Old-task retention:** Check A/B and both allowed additive contributions after detachment and after the new conjunction trains.

### PL3-16 · Zero-at-missing-source interaction gate — Ambitious but doable (P)
- **Parent failure → mechanism:** A quarantined component can still affect outputs when its source activation is absent because of biases and skips. Construct each interaction as a centered cross-difference of one nonlinear layer evaluated with and without each input. The contribution is exactly zero when either supplied factor equals its declared neutral input. Fit only clean factors in the replacement.
- **Nearest prior / gap:** [Partial information decomposition](https://arxiv.org/abs/1004.2515) distinguishes unique and synergistic information without imposing this boundary on a predictor; [MoE](https://arxiv.org/abs/1701.06538) gates expert computation, not this exact vanish-on-neutral constraint.
- **Cheapest first test:** Two scalar inputs with anchor-dependent cross terms and a biased MLP with hidden skips. Compare multiplicative masks and layer detachment at equal inference calls; sweep legitimate neutral-input choices.
- **Old-task retention:** Score A/B for each single-source regime and both together after the teacher factor is replaced.

### PL3-17 · Allowed-only mixed derivative training — Ambitious but doable (P)
- **Parent failure → mechanism:** Ordinary clean training can spend all its gradient budget rebuilding main effects, leaving the replacement blind to synergy. Freeze main-effect paths and train a new cross-term layer with a four-corner loss on allowed joint outcomes: match the mixed finite difference, not four absolute predictions from an old model.
- **Nearest prior / gap:** [Shapley–Taylor](https://arxiv.org/abs/1902.05622) uses interaction attribution, and [distillation](https://arxiv.org/abs/1503.02531) trains from soft predictions. The new supervision is the observed mixed contrast of independently acquired labels, with no teacher-generated target.
- **Cheapest first test:** Allowed experiments on a binary feature grid where the cross term is rare. Compare clean empirical risk minimization and a directly supervised interaction head given the same four labels and frozen marginals.
- **Old-task retention:** Score A/B and allowed marginal calibration after learning the cross term and after one ordinary subsequent update.

### PL3-18 · Factor substitution in an interaction circuit — Ambitious but doable (P)
- **Parent failure → mechanism:** A teacher-derived representation can mix one irreproducible cue with ordinary transferable information. Discard the old combiner and its teacher factor. Train a substitute encoder from an allowed measurement, then fit a new low-rank bilinear combiner with the preserved allowed factor. Constrain its two single-factor outputs to zero so it cannot overwrite either standalone skill.
- **Nearest prior / gap:** [Multimodal training](https://arxiv.org/abs/1905.12681) studies how end-to-end joint training can underperform individual modalities. The proposed replacement is a cross-only path learned around a *fixed surviving operand*, not tuning both modalities or distilling an expired factor.
- **Cheapest first test:** Two sensor streams with an allowed secondary measurement of one latent factor. Compare clean joint refitting, independent heads and a rank-matched concatenation MLP with frozen encoders.
- **Old-task retention:** Score A/B on either channel alone and joint performance when the substitute measurement is briefly absent.

### PL3-19 · Main-effect gradient bypass — Ambitious but doable (P)
- **Parent failure → mechanism:** Even a detachable interaction head can contaminate a surviving feature extractor through backpropagation. Route interaction errors through a one-way feature tap: the combiner can read frozen current features, but its gradients bypass the allowed paths and train dedicated residual encoders instead. At expiry discard the residual encoders together with the combiner.
- **Nearest prior / gap:** [SISA](https://arxiv.org/abs/1912.03817) isolates training in shards; [shared-module MTL](https://arxiv.org/abs/2005.00944) updates shared features. This isolation acts on gradient paths while letting interaction tasks read and reuse healthy features.
- **Cheapest first test:** Add a teacher shortcut during two-layer multi-source training. Compare SISA, permanently frozen features and simple stop-gradient without replacement encoders at the same capacity.
- **Old-task retention:** Score A/B with the interaction removed and after the surviving modules accept another clean task.

### PL3-20 · Synthetic pairing from allowed marginals — Ambitious but doable (P)
- **Parent failure → mechanism:** Allowed evidence contains both factors but rarely the pairs needed to learn the interaction. Draw two independent allowed fragments, compose them in a known simulator, and learn only the interaction response that the simulator can label. Do not treat co-occurrence or compatibility with the expired teacher as a label.
- **Nearest prior / gap:** [Partial information decomposition](https://arxiv.org/abs/1004.2515) describes multi-source information; [Deep RL from Human Preferences](https://arxiv.org/abs/1706.03741) learns from labeled comparisons. Here the new training example is an independently relabeled recombination of source fragments, not an inferred label from their marginals.
- **Cheapest first test:** Two clean rule fragments compose on a toy grid with a known transition function. Compare random pairing, separately composed policy outputs and equally many ordinary joint samples. Abstain where the simulator does not define the composition.
- **Old-task retention:** Score A/B and old valid compositions after training, including fragment pairs not used in the synthetic curriculum.

### PL3-21 · Clean-child competitive replacement — Ambitious but doable (P)
- **Parent failure → mechanism:** An allowed child may not discover the interaction because easy isolated tasks dominate its curriculum. Train two allowed learners: one proposes hard joint cases for the other, paid by the learner’s improvement on fresh allowed labels; restrict both to a fixed clean environment. Install the learner only after clean evaluation, not by agreement with an expired model.
- **Nearest prior / gap:** [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) balances exploration and imitation; [Policy Distillation](https://arxiv.org/abs/1511.06295) compresses trained policies. The joint-case proposer instead creates a new clean training distribution driven by improvement on interactions, without imitating any teacher.
- **Cheapest first test:** Two toy switches yield reward only jointly. Compare uniform exploration, ordinary prioritized replay and reward-driven proposal at equal simulator interactions, including a case with an unobservable switch.
- **Old-task retention:** Check A/B on the clean child’s installed path after the proposer stops, including isolated behaviors it deprioritized.

### PL3-22 · Leave-one-source-out immunity training — Ambitious but doable (P)
- **Parent failure → mechanism:** A model trained to retain high average accuracy can quietly replace a retired teacher with a proxy for it. Before any expiry, train separate recovery branches on random allowed-only masks, excluding the masked source’s descendants as well. Optimize worst-mask clean task gain via independently observed labels, not agreement with the full model.
- **Nearest prior / gap:** [Multimodal training](https://arxiv.org/abs/1905.12681) identifies uneven modality learning, and [DARE](https://arxiv.org/abs/2311.03099) drops parameters in deltas. The masks here correspond to *causal supervision closures*, not missing input tokens or randomly dropped weights.
- **Cheapest first test:** Three small sources with a deceptive proxy derived from one source. Compare input dropout, random sample masks and descendant-aware masks at the same masked training budget.
- **Old-task retention:** Score A/B for each supported clean mask both before and after a new source joins; report unavailable skills rather than filling them from a proxy.

### PL3-23 · Transfer only the clean read operator — Ambitious but doable (P)
- **Parent failure → mechanism:** Even a clean child can reintroduce the teacher’s behavior if its recovered skill only works when stitched onto the contaminated parent encoder. Transfer a callable read operator that accepts only verified clean intermediate features and train it on clean feature swaps; do not copy the parent’s hidden state or regression targets.
- **Nearest prior / gap:** [Knowledge distillation survey](https://arxiv.org/abs/2006.05525) distinguishes response-, feature- and relation-based transfer; [LoRA](https://arxiv.org/abs/2106.09685) adds a small patch to a base. Here the recovered interaction stays a clean-input function, not a patch that can silently access unsafe parent features.
- **Cheapest first test:** A small clean learner and an older model with a correlated hidden shortcut. Compare grafting a head onto the parent, ordinary clean distillation and the clean-feature operator at matched serving cost.
- **Old-task retention:** Check A/B under the new call path, including old functions that share the parent’s shortcut-bearing layer.

### PL3-24 · Counterfactual joint-target cancellation — Ambitious but doable (P)
- **Parent failure → mechanism:** Clean joint observations can still reward a shortcut correlated with synergy. For each permitted factor intervention, train the interaction to predict the change between outcomes with and without the factor while pairing the same external context. Average only over observable interventions; leave unsupported effects out of the write.
- **Nearest prior / gap:** [Counterfactual Fairness](https://arxiv.org/abs/1703.06856) compares predictions under counterfactual changes to a protected attribute; [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes feature interactions. This is a paired training target for an interventional response of a *replacement* interaction, rather than scoring model fairness or explaining existing logits.
- **Cheapest first test:** A structural toy with a clean but spurious context correlated with the joint target. Compare ordinary clean ERM, four-corner PL3-17 without context pairing and same-context difference training.
- **Old-task retention:** Score untouched A/B across old contexts, including contexts where the intervention has no effect.

### PL3-25 · Clean interaction curriculum via factor expansion — Ambitious but doable (P)
- **Parent failure → mechanism:** If allowed sources cannot represent the interaction in their current bases, quarantine becomes permanent despite sufficient raw observations. Grow one clean feature per source to predict the remaining joint error conditioned on the counterpart’s allowed representation, then alternate updates with a tiny bilinear head. Keep existing single-source features fixed.
- **Nearest prior / gap:** [Shared-module MTL](https://arxiv.org/abs/2005.00944) learns useful shared features; [MoE-LoRA](https://arxiv.org/abs/2502.15828) expands capacity with low-rank experts. The alternating operation grows *complementary factors* to expose a clean cross term, not another general-purpose expert or an expired representation.
- **Cheapest first test:** Two binary channels where each fixed encoder discarded one necessary bit. Compare equal-rank joint expansion, an expanded interaction head only and alternating complementary growth. Withhold one bit entirely in a negative-control stream.
- **Old-task retention:** Score A/B through the fixed individual paths and after activating the jointly grown features.

### PL3-26 · Reciprocal clean imitation with masked factors — Ambitious but doable (P)
- **Parent failure → mechanism:** Neither allowed learner can solve the whole interaction alone; ordinary peer distillation averages their errors. Train two clean peers to communicate complementary partial predictions while withholding a different factor from each sender. Train the receiver’s combiner on an independent joint outcome, so each message is rewarded for what it contributes when the other is present, not for resembling an expired teacher.
- **Nearest prior / gap:** [Distillation](https://arxiv.org/abs/1503.02531) matches teacher outputs and [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) transmits skills through social learning. Here joint clean supervision trains complementary messages under asymmetric information, not imitation of a complete policy.
- **Cheapest first test:** Distributed Boolean parity where neither learner sees both bits. Compare averaged logits, pooled clean training as an oracle and equal-bit supervised message learning.
- **Old-task retention:** Check old A/B for each peer with messages enabled and disabled after one peer learns an unrelated rule.

### PL3-27 · Clean optimizer-state split — Ambitious but doable (P)
- **Parent failure → mechanism:** Disabling a teacher adapter does not remove momentum through which an interaction keeps influencing allowed weights. Maintain disjoint optimizer states for the allowed and detachable interaction paths from their first update. Normalize the detached interaction steps separately so they cannot alter the allowed path’s effective step size; fit a clean interaction with fresh state when allowed evidence arrives.
- **Nearest prior / gap:** [Decoupled Weight Decay](https://arxiv.org/abs/1711.05101) shows that adaptive update rules can mix effects differently than the nominal objective; [SISA](https://arxiv.org/abs/1912.03817) isolates training influence. This extends detachment to the optimizer and gradient normalization of jointly served modules without restarting allowed adaptation.
- **Cheapest first test:** Small Adam-trained model with global gradient clipping and an intermittent high-gradient teacher term. Compare zeroing momentum at expiry, weight-only separation and independent optimizer paths from the start.
- **Old-task retention:** Score A/B before expiry and after the first and fifth allowed updates, including cumulative drift linked to previous clipping.

### PL3-28 · Replacement interaction with an abstaining residual — Ambitious but doable (P)
- **Parent failure → mechanism:** A recovered interaction trained on one region may extrapolate the retired convention where clean evidence is silent. Train a clean residual with a selective loss: jointly learn the correction and a gate that can fall back to the allowed main effects at a specified error budget. The gate’s training targets are held-out clean losses, not similarity to the old policy.
- **Nearest prior / gap:** [Expert Choice Routing](https://arxiv.org/abs/2202.09368) routes inputs to experts for sparse computation; [TOFU](https://arxiv.org/abs/2401.06121) evaluates forget and retain behavior. This operation learns where to *turn off a newly recovered correction* when a supported allowed fallback exists, rather than routing on compute or declaring whole-model recovery.
- **Cheapest first test:** Additive-plus-XOR toy with clean joint support only in one quadrant, then shift coverage. Compare a globally active clean residual, a hard training-support mask and learned selective replacement.
- **Old-task retention:** Check untouched A/B both where the correction is active and where the gate returns to main effects; report gate coverage and error separately.

## Ranked deeper questions

1. **Can two forks learn a shared change neither could safely take alone?** (PL3-01, PL3-03–PL3-05, PL3-10) Choose a finite-step shared task with different curvature and a wide-versus-narrow parametrization. Match the full jointly constrained product-space optimizer, same-probe OGD and separate forks. Demand a shared-task gain without either fork compromising old choices or A/B; if a straightforward constrained optimizer ties, keep it.
2. **Can we train synergy to be removable before it ever touches the main effects?** (PL3-15–PL3-19, PL3-27) Compare architectural separation, centered interaction signals and disjoint optimizer states on a tiny task with planted main and synergistic effects. Require retirement to preserve A/B, match the teacher-free oracle on allowed effects, and permit a later independent reconstruction, not just make a marker unobservable.
3. **What is the minimum clean supervision needed to restore a missing interaction?** (PL3-20–PL3-26, PL3-28) Cross weak marginals, simulator-labelable combinations and fundamentally missing factors. Compare the proposed training signals at the same number of clean joint labels. Keep unsupported regions unknown; measure when active or peer-generated examples beat simply collecting more clean labels while preserving A/B.
4. **Can paired updates survive uneven timing and retain future plasticity?** (PL3-06–PL3-09, PL3-11–PL3-14) Put forks on different update clocks and give one sparse spare capacity. Look for an advantage in serving during handoff or learning the next independent task at matched storage and messages, not agreement only after synchronous convergence.
