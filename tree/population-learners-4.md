# Population continual learners 4: Portable update codes and detachable source interactions

Depth 3 · 28 candidate primitives · **Ambitious but doable** · Ideas only; no experiments run

**Lineage:** [#379](https://github.com/manojbajaj95/cl/pull/379) → [#380](https://github.com/manojbajaj95/cl/pull/380) → [#381](https://github.com/manojbajaj95/cl/pull/381). The last review kept [PL3-01, functional gearbox](population-learners-3.md#pl3-01--functional-gearbox--ambitious-but-doable-p) and [PL3-15, source-subset residual layers](population-learners-3.md#pl3-15--source-subset-residual-layers--ambitious-but-doable-p), both at 3, neither at 4. **P** denotes a candidate primitive. The contribution must be an operation another learner can call, a factorization it can train, or a new source of supervision—not a better record of what happened.

## Literature and controls

Checked the linked arXiv titles and abstracts; gaps are against the named mechanism, not claims of exhaustive novelty. These controls apply to **every card in its branch**, in addition to the closest control in the proposed test.

- **A · Shared update code:** Compare PL3-01, raw-weight joint writes, [VeRA](https://arxiv.org/abs/2310.11454)-style shared low-rank bases, [hypernetwork patches](https://arxiv.org/abs/1609.09106), [shared-module MTL](https://arxiv.org/abs/2005.00944), and independent fine-tuning. Give the ordinary hypernetwork the same fork descriptor and patch budget. [Continual learning with hypernetworks](https://arxiv.org/abs/1906.00695) generates weights from task identities and already tackles sequential retention; a code must do more than name a task. Test on unseen fork pairs, separating known permutation/scale symmetries from genuine width, architecture or capability mismatch. For raw-weight controls, align compatible coordinates; report the cost and do not apply incompatible tensors. Measure useful effect per stored and transmitted byte, including decoder fitting, alongside direct new-task gain, held-out matched choices and A/B.
- **B · Train-time source factorization:** Compare PL3-15, after-the-fact quarantine (PL2-27), [SISA](https://arxiv.org/abs/1912.03817), [per-source LoRA](https://arxiv.org/abs/2106.09685) without joint terms, [task-vector negation](https://arxiv.org/abs/2212.04089), and retraining without the source. Detachment disables all terms depending on the retired source; it must not rewrite allowed modules after the fact. Distinguish *exact removal of named computation paths* from *equivalence to training without the source*. The latter can fail if parameters, data selection, running state or learned routing inherited the source. Use clean replay as a labeled-cost oracle and mark unsupported or inseparable effects unknown. [NAM](https://arxiv.org/abs/2004.13912) and [NODE-GAM](https://arxiv.org/abs/2106.01613) decompose prediction by input features; the index here is training-source dependence, not input origin alone.
- **Both:** Proposed tests use small learners. Freeze untouched A/B before adaptation; include one old local skill per fork or retained-source group. Match labels, training and serving compute, memory and messages, counting stored residuals and frozen decoders. Reject ties with simpler mechanisms as evidence for a new primitive.

## A · Turn a code into a reusable cross-fork write

### PL4-01 · Codomain-trained update inverse — Ambitious but doable (P)
- **Parent failure → mechanism:** A decoder trained to imitate historical patches can reproduce their coordinate quirks. Specify a code as coefficients of desired response changes on a common action basis. Train each decoder using loss on the *effect of its decoded patch*, never requiring it to match donor weights. Include paired zero-change channels for old choices.
- **Nearest prior / gap:** [Continual hypernetworks](https://arxiv.org/abs/1906.00695) generate persistent task-conditioned weights; [model stitching](https://arxiv.org/abs/2106.07682) learns a bridge between activations. Here a function-space error trains an inverse map into *local write coordinates*, and effect magnitudes can be recombined.
- **Cheapest first test:** Train with two differently scaled linear forks; test one unseen width and interpolate between learned effect coefficients. Compare a descriptor-aware patch hypernetwork supervised by local optimal patches, and direct response-conditioned fitting per import.
- **Old-task retention:** Check A/B and protected choices after three interpolated writes on the unseen fork.

### PL4-02 · Tangent-rank elastic decoder — Ambitious but doable (P)
- **Parent failure → mechanism:** A fixed patch rank wastes space in a wide fork and underfits a narrow but highly expressive one. Decode one code into an ordered series of local low-rank atoms, each fitted to the remaining functional error after the previous atom. Stop at the receiver’s byte cap; train prefix truncations to preserve old decisions at each permitted length.
- **Nearest prior / gap:** [VeRA](https://arxiv.org/abs/2310.11454) shares frozen random factors with learned vectors; [AWQ](https://arxiv.org/abs/2306.00978) uses activations to protect important weights during quantization. Prefix training instead allocates rank by unachieved update effect under a local budget.
- **Cheapest first test:** Two MLPs needing different ranks for the same effect. Compare fixed-rank decode, per-fork optimal rank selection and progressive prefixes under changing byte caps.
- **Old-task retention:** Score A/B at every permitted truncation and after a low-budget import followed by a full-budget one.

### PL4-03 · Permutation-equivariant patch transducer — Ambitious but doable (P)
- **Parent failure → mechanism:** A local decoder can relearn a meaningless neuron order after each fork reparameterizes. Encode the receiving weight graph with permutation-equivariant shared message rules and attach each decoded low-rank factor to the incident input/output channels. A function-preserving neuron permutation must permute the patch the same way.
- **Nearest prior / gap:** [Neural functional networks](https://arxiv.org/abs/2302.14040) and [deep weight-space architectures](https://arxiv.org/abs/2301.12780) already give equivariant weight processing under permutations; [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns models for merging. The possible contribution is a *single shared code* whose effect decodes on differently sized graphs without pairwise alignment; equivariance alone is prior art.
- **Cheapest first test:** Train on width-12 MLPs and test re-permutations plus a held-out width with the same behavior interface. Compare Git Re-Basin where dimensions match, an equivariant patch generator without a reusable code and local fitting.
- **Old-task retention:** Check A/B after model permutations and after a further native update on the resized fork.

### PL4-04 · Code-to-rule optimizer — Ambitious but doable (P)
- **Parent failure → mechanism:** A static decoded patch becomes stale after local adaptation. Decode a code into a local gradient-shaping rule, not a delta: use its output to precondition the first few updates on new authorized examples, learning the rule by terminal shared-effect and retention loss across fork histories.
- **Nearest prior / gap:** [Learned optimization](https://arxiv.org/abs/1606.04474) meta-trains update rules; [hypernetworks](https://arxiv.org/abs/1609.09106) generate weights. Here the reusable operand is one portable lesson that compiles into distinct *procedures* reacting to recipient data.
- **Cheapest first test:** Two small forks solve a recurring nuisance task after different sequences of unrelated shifts. Compare static patches, a generic learned optimizer given the same labels, and decoded preconditioners.
- **Old-task retention:** Score A/B directly after decoding and after the specified local steps in previously unseen histories.

### PL4-05 · Code composition by response commutator — Ambitious but doable (P)
- **Parent failure → mechanism:** Summed codes may compose differently across forks because each patch changes the other decoder’s operating point. Fit a small bilinear correction in code space to the measured ordered residual after applying two decoded patches. Decode the corrected composition from either fork’s original state, rather than exchange both executable patches.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds task vectors; [LoraHub](https://arxiv.org/abs/2307.13269) composes adapters with a few examples. The claimed operation compresses *ordered* compositions into one reusable code that can be rematerialized on another architecture.
- **Cheapest first test:** Two-layer forks with deliberately noncommuting two-step edits. Compare simple code addition, sending both codes with replay, and local bilinear patch composition at equal serving rank.
- **Old-task retention:** Evaluate A/B for both orders and after a third unrelated code lands.

### PL4-06 · New-fork boot decoder — Ambitious but doable (P)
- **Parent failure → mechanism:** One decoder per learner makes joining too expensive. Fit the newcomer’s code-to-patch map from the measured directional responses of a few cheap local writes, using those responses as dictionary columns to approximate a common effect. Continue learning only columns that later codes actually need.
- **Nearest prior / gap:** [Model stitching](https://arxiv.org/abs/2106.07682) joins frozen subnets with a compatibility layer; [representation similarity](https://arxiv.org/abs/1905.00414) compares activations. This fits a *write dictionary* from interventions, not from static similarity or end-to-end stitching accuracy.
- **Cheapest first test:** Join a shallow net to a deeper pair with equal pre-join behavior but different Jacobians. Compare activation alignment, zero-shot descriptor hypernetwork and identical-cost low-rank local fine-tuning.
- **Old-task retention:** Score newcomer A/B and originating forks' old skills after onboarding and a held-out code transfer.

### PL4-07 · Gauge-transported code basis — Ambitious but doable (P)
- **Parent failure → mechanism:** Jointly learned code axes can silently rotate after a decoder is upgraded. Fit a transport matrix from old to new *code responses* on a small set of spanning probes. Conjugate update-composition operators by that matrix so previously stored codes and future compositions remain usable in the new basis.
- **Nearest prior / gap:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns weight permutations; [model stitching](https://arxiv.org/abs/2106.07682) aligns intermediate activations for inference. This migrates the *latent update algebra* and reuses old codes without replaying every learned task.
- **Cheapest first test:** Rotate and dilate a codebook during a toy decoder upgrade, then also test a noninvertible upgrade where transport should fail. Compare fixed axes and replay-based re-encoding at equal probes.
- **Old-task retention:** Check A/B after importing an old code and composing it with a post-upgrade code.

### PL4-08 · Shared code with a private refusal direction — Ambitious but doable (P)
- **Parent failure → mechanism:** One fork may not realize the whole effect without compromising a local choice. Decode the globally named effect into reachable and refused components using the recipient’s constrained response map; train a local safe adapter only for the reachable component. The refused residual never becomes a negative training target for the other forks.
- **Nearest prior / gap:** [OGD](https://arxiv.org/abs/1910.07104) projects weight steps away from old output directions. This projects in *shared effect coordinates first*: a rejected coordinate can still train other recipients and a later local decoder can realize only what it missed.
- **Cheapest first test:** Give one fork a hard action constraint overlapping only one of two effect coordinates. Compare ordinary weight projection, all-or-nothing import and exact constrained local solve on repeat imports.
- **Old-task retention:** Check both forks’ A/B and matched policy disagreement after partial import, then after a newly feasible component is added.

### PL4-09 · Counterexample-trained code separation — Ambitious but doable (P)
- **Parent failure → mechanism:** Two distinct lessons can share effects on the usual probes and collapse into one code. Train an adversarial probe proposer on allowed task contexts to find where decoded updates for two distinct ground-truth lessons should differ. Use authoritative labels there to repel the codes only if the difference is real.
- **Nearest prior / gap:** [Hypernetworks](https://arxiv.org/abs/1609.09106) learn a generator conditioned on task inputs; [neural functional networks](https://arxiv.org/abs/2302.14040) process weights or gradients. This supervision actively separates *confusable write effects* demonstrated by new labels, not representations or task IDs.
- **Cheapest first test:** Create two Boolean edits that coincide except on one input slice. Match authoritative queries against random active probes, hard-negative task labels and code orthogonalization.
- **Old-task retention:** Score A/B after both formerly colliding codes and an unrelated lesson on a held-out-width fork.

### PL4-10 · Discrete update syllables — Ambitious but doable (P)
- **Parent failure → mechanism:** Dense continuous codes are expensive to communicate and brittle to small numeric changes. Train an ordered, vector-quantized sequence of write tokens. Each token must reduce receiver-side residual error in sequence; token dropout teaches partial prefixes that can be served without policy flips.
- **Nearest prior / gap:** [VQ-VAE](https://arxiv.org/abs/1711.00937) learns a discrete representation of data; [VeRA](https://arxiv.org/abs/2310.11454) reduces local adapter state with shared matrices. Here tokens encode *effects of a sequence of writes* on different models, not reconstruction of inputs or a tensor factor alone.
- **Cheapest first test:** Stream recurring symbolic edits with a few compositional combinations. Compare post-hoc quantization, a dense code at matched message bits, and sending cached adapter IDs.
- **Old-task retention:** Check A/B at incomplete and complete token sequences, including after one local fine-tune.

### PL4-11 · Budget-conditioned split across depth — Ambitious but doable (P)
- **Parent failure → mechanism:** A single layer correspondence is ill-defined across architectures. Decode one effect into flexible layer expenditures, allocating private rank to locations that minimize projected functional error per unit of compute. Train with changing latency budgets so the same code can materialize in one late block or several early ones.
- **Nearest prior / gap:** [FBNet](https://arxiv.org/abs/1812.03443) uses differentiable search for hardware-efficient architectures; [VeRA](https://arxiv.org/abs/2310.11454) obtains small per-layer adaptations. Here depth allocation is chosen *per portable write* in already trained, nonidentical forks, rather than for a new architecture.
- **Cheapest first test:** Match a shallow and a deep MLP; switch which layers have a cheap update port. Compare fixed-depth and ordinary hardware-aware adapter search under equal latency.
- **Old-task retention:** Score A/B across budgets and after switching an existing code to a new layer allocation.

### PL4-12 · Patch-space impedance matching — Ambitious but doable (P)
- **Parent failure → mechanism:** Cheap identical output effects today can land in ill-conditioned local directions that erase plasticity tomorrow. Decode the effect in the local metric induced by expected *next-step* gain, learned from controlled local continuation tasks; prefer realizations that leave room for later independent updates.
- **Nearest prior / gap:** [Continual hypernetworks](https://arxiv.org/abs/1906.00695) regularize retention of previous task outputs; [Adam-NSCL](https://arxiv.org/abs/2103.07113) projects learning away from old feature spaces. This decoder metric chooses between equally valid realizations by their subsequent learnability, inside one transferable code.
- **Cheapest first test:** Small homogeneous heads plus a mismatched saturated head, with two paths to the same new effect. Compare minimum norm, Fisher-weighted decoding and the learned continuation metric.
- **Old-task retention:** Score A/B at import and after unrelated local continuation, holding present-day update gain fixed.

### PL4-13 · A code that trains its receiver’s input map — Ambitious but doable (P)
- **Parent failure → mechanism:** A shared effect may require a feature that one receiver cannot read at all. Decode it into a two-stage program: train a small perceptual adapter using labels only on an allowed common latent variable, then instantiate the effect using that variable. The first stage receives no policy label, so it cannot teach the donor’s choices by default.
- **Nearest prior / gap:** [Model stitching](https://arxiv.org/abs/2106.07682) matches interfaces between fixed models; [distillation](https://arxiv.org/abs/1503.02531) transfers predictive behavior. This write binds a labeled feature acquisition step to a separate cheap behavior patch, rather than shipping a new common representation or absolute logits.
- **Cheapest first test:** One fork sees a factor directly; the other can infer it through two allowed cues. Compare fitting the patch alone, shared-trunk feature supervision and independent fine-tuning with the same labels.
- **Old-task retention:** Score A/B after each stage, including the receiver’s old opposing policy on matched inputs.

### PL4-14 · Mergeable code superposition by effect cancellation — Ambitious but doable (P)
- **Parent failure → mechanism:** A code stream can accumulate duplicate or opposite effects, wasting rank on changes that cancel only when evaluated together. Train a latent reducer with an explicit no-op code and a rank penalty against the *measured response of the original ordered writes*. A truly canceled component maps to zero rank; a noncommuting remainder survives even if its individual codes add to zero.
- **Nearest prior / gap:** [TIES](https://arxiv.org/abs/2306.01708) resolves tensor sign conflict; [reusable LoRA libraries](https://arxiv.org/abs/2405.11157) build and combine adapter libraries. The reducer amortizes recurrent cancellation patterns in function space so multiple mismatched receivers can share one reduced code.
- **Cheapest first test:** A sequence contains duplicate, canceling and noncanceling lesson pairs. Compare TIES on aligned forks, pruning by code magnitude, and composing then distilling separately into each receiver.
- **Old-task retention:** Score A/B after compaction and after later importing a code that partially overlaps the compacted set.

## B · Make source detachment a property of training

### PL4-15 · Union-routed residual algebra — Ambitious but doable (P)
- **Parent failure → mechanism:** Source dependence can escape a single residual layer when later layers multiply its output with another source. Carry separate tensor components by their source subsets. Linear operations act componentwise; bounded-degree products write to the union of their operands’ subsets. Detaching source T zeros every component whose subset contains T, with no change to the other components.
- **Nearest prior / gap:** [NAM](https://arxiv.org/abs/2004.13912) sums univariate predictors; [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes feature interactions. Union routing defines a forward *and gradient placement* rule inside a compositional network; exactness is relative to the represented components, not unconstrained retraining.
- **Cheapest first test:** Two-layer polynomial model with overlapping pair terms. Compare an output-only factorization, PL3-15 and independent source branches under matched coefficient count.
- **Old-task retention:** Score A/B supported by surviving sources after detaching each source in turn and applying one more clean step.

### PL4-16 · Subset-specific attention normalizer — Ambitious but doable (P)
- **Parent failure → mechanism:** Even if a source’s value vectors detach, its keys can have changed every other source’s softmax weights. Maintain a clean attention path over base and allowed atoms and train cross-source attention as a difference between joint and lower-order normalizations. Route each residual difference to the corresponding subset; retiring one source removes its mass effects as well as its values.
- **Nearest prior / gap:** [Transformer attention](https://arxiv.org/abs/1706.03762) couples tokens through a shared denominator; [NODE-GAM](https://arxiv.org/abs/2106.01613) constrains feature dependence in tree ensembles. This is a trainable additive decomposition of *normalization effects* by permitted source subset.
- **Cheapest first test:** Attention toy with an expired key carrying no useful value but dominating softmax mass. Compare value-only detachment, inference-time key masking and separately trained attention for each subset.
- **Old-task retention:** Score A/B on allowed keys after detachment, including held-out sequences where the retired key previously drew most of the mass.

### PL4-17 · Factorized running moments — Ambitious but doable (P)
- **Parent failure → mechanism:** Source influence can persist in shared normalization even when all source weights are isolated. Keep weighted first and second moment terms per permitted source subset, including learned cross terms for feature mixtures. On detachment recompute the normalizer from retained sufficient statistics, then continue updating only those terms.
- **Nearest prior / gap:** [Batch Normalization](https://arxiv.org/abs/1502.03167) normalizes using running statistics; [SISA](https://arxiv.org/abs/1912.03817) separates training for deletion. The proposed object makes non-parameter inference state composable and detachable along the same subset index as parameters.
- **Cheapest first test:** Batch-normalized two-source regressor with a mean shift and one cross-source covariance. Compare re-estimating moments from a small allowed cache, frozen global moments and source-local moments without a cross term.
- **Old-task retention:** Score A/B immediately after detachment without a calibration pass, then after one allowed update.

### PL4-18 · Orthogonal functional residual for clean main effects — Ambitious but doable (P)
- **Parent failure → mechanism:** A conjunction can relearn standalone behavior on joint-only observations, so detaching it erases more than synergy. On observed allowed-source holdouts, project the joint term’s functional output onto the complement of the span of clean low-order readouts. Fit the remainder with the high-order residual and route clean single-source errors back only to their own modules.
- **Nearest prior / gap:** [OGD](https://arxiv.org/abs/1910.07104) projects updates to preserve old outputs; [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes interactions. Here orthogonalization fixes the allocation of *predictive function* across terms to prevent main-effect duplication, not just an update direction or a score after training.
- **Cheapest first test:** Use correlated additive-plus-product regression; compare anchored finite differences, feature-orthogonal least squares and joint terms without projection. Restrict claims to supported subsets.
- **Old-task retention:** Score A/B after removing a joint term and again after retraining that term on permitted evidence only.

### PL4-19 · Hierarchical rank inheritance for interactions — Ambitious but doable (P)
- **Parent failure → mechanism:** A separate adapter for every source combination grows exponentially. Give each interaction a low-rank product of *eligible* parents’ read factors and a private trainable coefficient, keeping parent factors frozen to interaction gradients. Add a free rank-one residual only if a clean held-in interaction target is outside the product span. A term inherits its parents’ source union.
- **Nearest prior / gap:** [LoRA](https://arxiv.org/abs/2106.09685) learns low-rank parameter updates; [LoraHub](https://arxiv.org/abs/2307.13269) mixes preexisting LoRAs. The operation creates a new interaction from products of lower-order factors with detachability closed under inheritance, not a sum of existing adapters.
- **Cheapest first test:** Fit six-source synthetic pair interactions with a sparse known rank structure. Compare independent per-pair rank, additive LoRA and a product-only library at equal total parameters.
- **Old-task retention:** Score A/B after removing a high-degree source, including interactions between two other sources.

### PL4-20 · Independently replaceable interaction operand — Ambitious but doable (P)
- **Parent failure → mechanism:** After detachment a useful interaction disappears even if an independently held representation can supply the missing operand. Train a combiner from the outset with multiple source-disjoint realizations of one operand. Keep separate coefficient branches, trained only on their own authorized evidence, so selecting the surviving realization never activates expired parameters.
- **Nearest prior / gap:** [MoE](https://arxiv.org/abs/1701.06538) routes among experts; [partial information decomposition](https://arxiv.org/abs/1004.2515) distinguishes redundancy from synergy. This trains alternative *combiners* on independently available interchangeable operands rather than learning one mixed expert or recovering an operand only after expiry as in PL3-18.
- **Cheapest first test:** Two sensors report the same latent variable with distinct errors; an allowed third source provides the complementary variable. Compare independent full interaction branches and ordinary source dropout into a shared combiner.
- **Old-task retention:** Score A/B and the joint skill across the swap, including asymmetric sensor failures.

### PL4-21 · Exchangeable detach order for nested adapters — Ambitious but doable (P)
- **Parent failure → mechanism:** Sequentially nested source adapters can make removing X then Y differ from removing Y then X. Use a residual sum whose noncommuting layer-order effects get their own union-indexed interaction term, trained on the difference between composed and independently applied paths. Detachment is multiplication by a binary source mask on each term, not subtracting a composed delta.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds or negates parameter offsets; [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns weights for merging. Here the trainable ordered correction is isolated so *removal* commutes, even though original writes need not.
- **Cheapest first test:** Three triangular affine adapters with two noncommuting sources, then a nonlinear case with rank-limited corrections. Compare unordered residual sums and post-hoc deltas for each removal order.
- **Old-task retention:** Score A/B after either detachment order and after a new clean adapter trains on the retained path.

### PL4-22 · Source-isolated routing gradients — Ambitious but doable (P)
- **Parent failure → mechanism:** Remaining experts may depend on a router trained using the expired source even if their own parameters are clean. Train additive per-subset routing logits, letting each training example’s loss update only the router associated with the allowed closure that supplied it. Train masked coalition normalizations with only clean labels, so a route still works once a whole source disappears.
- **Nearest prior / gap:** [MoE](https://arxiv.org/abs/1701.06538) gates experts per example; [SISA](https://arxiv.org/abs/1912.03817) isolates model partitions. This factorizes the *router’s training signal* as well as experts, so selecting a retained expert need not depend on a retired teacher.
- **Cheapest first test:** Four tiny experts, one rare allowed expert seen mostly near a dominant teacher. Compare weight-only expert detachment, a shared router trained with dropout and classifier-free fixed fallback routing.
- **Old-task retention:** Score A/B on the rare allowed route and on the majority route immediately after detachment.

### PL4-23 · Source-local metaplasticity growth — Ambitious but doable (P)
- **Parent failure → mechanism:** Even split optimizer state leaves a hidden dependency if an interaction’s learning curve decides when a clean module gains capacity. Let each subset train a local growth gate on its own held-in continuation loss. Use a fixed capacity allotment per retained subset; a higher-order interaction can borrow a frozen read factor, but cannot spend or enlarge a lower-order subset’s writable rank.
- **Nearest prior / gap:** [Learned optimization](https://arxiv.org/abs/1606.04474) learns how to change weights, and [FBNet](https://arxiv.org/abs/1812.03443) differentiates over architecture choices. This learns a detachable *capacity growth policy* where the architecture of a surviving module does not depend on a retired learner’s signals, beyond PL3-27’s split optimizer states.
- **Cheapest first test:** Two allowed feature paths and an expiring interaction that briefly produces a large loss. Compare fixed ranks, split Adam with global rank allocation and local learned growth against the same total rank ceiling.
- **Old-task retention:** Score A/B after removal and after five clean updates, including delayed growth of an allowed feature the short-lived interaction did not predict.

### PL4-24 · Coalition edge gradient for detachable skills — Ambitious but doable (P)
- **Parent failure → mechanism:** A model fitted only with every residual enabled can break on a valid retained coalition even if source removal is exact algebraically. Train on sampled supported **edges** of the coalition lattice: before and after adding source T, regress the incremental prediction to the observed change in outcome on the same context. Route that error only into terms newly enabled by T whose other sources are in the coalition, leaving lower-order terms unchanged on joint edges.
- **Nearest prior / gap:** [NODE-GAM](https://arxiv.org/abs/2106.01613) builds interpretable additive or pairwise models; [SISA](https://arxiv.org/abs/1912.03817) isolates training shards. The proposed loss optimizes removal behavior for full *training-source coalitions* and apportions the update beyond the surviving predictor.
- **Cheapest first test:** Four sources with sparse permitted label coverage. Compare dropout over adapters using one common outcome and training one model per coalition at equal total steps.
- **Old-task retention:** Score A/B after each supported leave-one-out mask and one held-out two-source withdrawal.

### PL4-25 · Fresh-feature branch for source-dependent representation growth — Ambitious but doable (P)
- **Parent failure → mechanism:** A new source can force growth in the base representation, making its removal inseparable from older heads. Grow a new feature channel for its subset, with directed reads from clean existing branches but no path back into clean activations or their gradients. Train a cross-source head only when both operands’ clean baselines are already fit.
- **Nearest prior / gap:** [LoRA](https://arxiv.org/abs/2106.09685) freezes base weights while learning low-rank adapters; [BTX](https://arxiv.org/abs/2403.07816) combines separately trained experts. This grows *directed* feature capacity so an interaction can read retained features without changing their computation or optimization.
- **Cheapest first test:** A streamed teacher introduces a new input mode requiring width expansion. Compare ordinary widening, frozen-base LoRA and directed growth with the same extra units.
- **Old-task retention:** Score A/B before growth, after activation and after deleting the newly grown channels.

### PL4-26 · Detachable redundancy subtraction — Ambitious but doable (P)
- **Parent failure → mechanism:** Two independently learned source residuals may each encode the same main effect, so activating both doubles it and retiring one appears to repair the model. When overlap is supported by permitted matched labels, fit a joint anti-duplication term whose target is the observed joint response minus the sum of standalone responses. Keep both standalone paths trainable *only* on their own evidence.
- **Nearest prior / gap:** [Partial information decomposition](https://arxiv.org/abs/1004.2515) distinguishes redundancy from unique information; [NAM](https://arxiv.org/abs/2004.13912) sums featurewise responses. This turns confirmed redundancy into a detachable *negative* joint write, instead of averaging or editing one of the individually valid implementations.
- **Cheapest first test:** Two noisy measurements independently predict the same key and a third contains a genuine complementary factor. Compare deduplication by weight similarity, mean pooling and a standard unconstrained joint residual.
- **Old-task retention:** Score A/B and joint calibration with both channels present, each alone, and after one disappears.

### PL4-27 · Support-complete detach-and-update kernel — Ambitious but doable (P)
- **Parent failure → mechanism:** A residual may start clean but receive gradients from examples selected by a newly joined source. Give each update a factorized supervision input that includes the selector as well as the label source. Apply the step to an interaction path indexed by their union; update a lower-order path only with an independently selected counterfactual example.
- **Nearest prior / gap:** [SISA](https://arxiv.org/abs/1912.03817) isolates training records; [TracIn](https://arxiv.org/abs/2002.08484) traces training influence. PL2-19 reruns selection at retirement. This kernel changes *where the very first gradient goes*, so then detaching the joint term can discard selector influence without having to reconstruct the old curriculum.
- **Cheapest first test:** An active linear learner gets labels from an allowed service but requests inputs chosen by an expiring source. Compare label-only factorization, curriculum rerun and union-routed steps.
- **Old-task retention:** Score A/B after dropping the selector, including examples in the previously selected region and an unrelated allowed region.

### PL4-28 · Joint-to-clean transplant through a fresh interaction — Ambitious but doable (P)
- **Parent failure → mechanism:** Even train-time factorization can leave no retained path for a valuable higher-order skill. Fit a new allowed-only joint term from a bounded set of clean interventions that vary permitted factors independently; keep lower-order terms fixed and optimize only the mixed residual on the observed grid. Insert this new term without copying any expired term’s targets, hidden states or weights.
- **Nearest prior / gap:** [Distillation](https://arxiv.org/abs/1503.02531) matches teacher outputs; [Shapley–Taylor](https://arxiv.org/abs/1902.05622) attributes interactions. PL3-17 supplies four-corner training for two factors; the extension is a sparse hierarchy in which a clean, newly supported subset replaces only the missing higher-order slot and can immediately participate in further source removals.
- **Cheapest first test:** Three allowed factors can reproduce a formerly teacher-dependent behavior via two supported pair terms, with no support for a triple term. Compare full clean retraining, a monolithic clean interaction head and separate clean pair replacements.
- **Old-task retention:** Score A/B after replacing the missing interaction and again after removing one of the newly used allowed sources.

## Ranked deeper questions

1. **What is the smallest update code that genuinely transfers across unequal models?** (PL4-01–PL4-04, PL4-06, PL4-11) Separate mere neuron permutations from width, depth and inaccessible features. Demand both cheaper realizations and preserved A/B versus a descriptor-aware hypernetwork and local fine-tuning, charging the cost of first training and later maintaining decoders.
2. **Can first-class codes compose and survive a decoder upgrade without silently changing what they do?** (PL4-05, PL4-07–PL4-10, PL4-12, PL4-14) Plant noncommuting, identical-on-probes and genuinely canceling edits. Compare ordered or reduced codes with replaying each update; require correct off-probe behavior and retained A/B, not just reconstruction on the training probes.
3. **Where does source dependence leak outside residual weights?** (PL4-15–PL4-17, PL4-21–PL4-25, PL4-27) Give the retired source control over normalization, routing, clipping or example selection one at a time. Compare immediate detachment to clean replay and name which operation closes each demonstrated path. Do not claim forgetting if disabling weights leaves an inherited training signal active.
4. **How much can stay detachable before interaction rank or clean evidence becomes the limiting resource?** (PL4-18–PL4-20, PL4-24, PL4-26, PL4-28) Cross redundancy with sparse joint support and count parameters, clean interventions, clean-reference error and A/B. If a per-source LoRA bank with a small head ties or a missing coalition makes the effect unidentifiable, keep the simpler bank or mark the interaction unknown.
