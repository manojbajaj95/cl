# Population continual learners 5: Learning to join, learning to let go

Depth 4 · 26 candidate primitives · **Ambitious but doable** · Ideas only; no experiments run

**Lineage:** [#379](https://github.com/manojbajaj95/cl/pull/379) → [#380](https://github.com/manojbajaj95/cl/pull/380) → [#381](https://github.com/manojbajaj95/cl/pull/381) → [#382](https://github.com/manojbajaj95/cl/pull/382). The last review kept two cards at 3, neither at 4: [PL4-06, new-fork boot decoder](population-learners-4.md#pl4-06--new-fork-boot-decoder--ambitious-but-doable-p) and [PL4-17, factorized running moments](population-learners-4.md#pl4-17--factorized-running-moments--ambitious-but-doable-p). The first asks how a stranger joins a population that already exchanges learned edits; the second asks what a learner must let go of when the source is gone but its inference state persists. **P** marks a candidate primitive, not a novelty verdict.

## Literature and comparison contract

Checked the linked paper titles and abstracts. Gaps distinguish these hypotheses from the named works, not the entire literature. Branch-wide controls below apply to every card in that branch.

- **A · Joining by writes:** Compare PL4-06, a trained per-fork decoder, [model stitching](https://arxiv.org/abs/2106.07682), [CKA-based representation alignment](https://arxiv.org/abs/1905.00414) with the same patch-fitting budget, [Git Re-Basin](https://arxiv.org/abs/2209.04836) where weight permutations are defined, and direct fine-tuning. [HyperTuning](https://arxiv.org/abs/2211.12485) generates adaptation parameters from examples; use a same-budget few-shot generator as a strong additional comparator. Count write probes, forward evaluations and fitting cost. Test codes absent from onboarding; distinguish mismatched architectures from permuted copies. Check local choices on matched inputs, not only the shared task.
- **B · Letting go of state:** Compare PL4-17, #381’s detachable weights with shared norm, full recomputation from retained data, a matched no-normalization model where relevant (e.g. [FedWon](https://arxiv.org/abs/2306.05879)), and [SISA](https://arxiv.org/abs/1912.03817) with state included in the replay boundary. For caches or indexes, the analogous no-state arm disables that mechanism. [TENT](https://arxiv.org/abs/2006.10726) updates feature statistics and affine normalization at test time; [FedBN](https://arxiv.org/abs/2102.07623) and [SiloBN](https://arxiv.org/abs/2008.07424) keep normalization local across clients or silos. Neither local statistics nor removable source sums make survivor activations clean when a retired source changed an upstream transform, query, or route. Compare with clean-state replay, report its cost and leave unsupported dependencies unknown. This is functional retirement within specified state, paths and time windows, not a guarantee of data erasure.
- **C · Population questions:** Include equal-budget independent learners, a central learner with identical information access and, when useful, an unconstrained oracle. Charge coordination and extra serving calls. If partitioning or information access does not bind, do not credit the population arrangement for a centralizable improvement.
- **All cards:** A/B are untouched pre-adaptation tasks, including old local tasks where appropriate. Separate onboarding or deletion probes from A/B. Stop a line if the simplest matched comparator gives the same new capability and retention.

## A · What can a few writes tell a new fork?

### PL5-01 · Ask for the write that splits the meanings — Ambitious but doable (P)
- **Failure → primitive:** Cheap dictionary columns can make two incompatible decoders look equally good; probe the local write on which those decoders predict the largest disagreement for the *next code the fork needs*.
- **Literature / gap:** [Online sparse coding](https://arxiv.org/abs/0908.0050) learns bases for reconstructing observations; here the choice of intervention is indexed by which future write interpretation it can rule out.
- **Cheapest test:** One spare probe, two admissible linear decoders, one held-out transfer; compare random columns, orthogonal columns and maximum disagreement averaged over all codes.
- **A/B retention:** Check old A/B and recipient-specific policy after decoding and installing the held-out edit.

### PL5-02 · Write in both directions before trusting a column — Ambitious but doable (P)
- **Failure → primitive:** A direction that looks transferable from one perturbation may be mostly activation curvature; use opposite signed probes to separate its reversible first-order effect from its even, nonlinear drift.
- **Literature / gap:** [Evolution strategies](https://arxiv.org/abs/1703.03864) estimate optimization directions from perturbations; the proposed odd and even measurements decide whether a local direction is a reusable translation or only useful for a particular step size.
- **Cheapest test:** Pair smooth and thresholded toy networks; compare four one-sided columns with two signed pairs at four calls, then transfer an unseen reversed edit.
- **A/B retention:** Check A/B at both signs and at the largest permitted combined step.

### PL5-03 · Probe a bundle, decode its sparse lesson — Ambitious but doable (P)
- **Failure → primitive:** Testing every local direction would cost as much as training a decoder; probe random signed bundles and recover only the few directions active for a requested code.
- **Literature / gap:** [Stable compressed sensing](https://arxiv.org/abs/math/0503066) already recovers sparse signals from mixtures; the bet here is that a fork’s *effect map*, not its absolute weights, is sufficiently sparse in a shared library to make bundled writes useful on held-out edits.
- **Cheapest test:** Six local directions, two useful ones and a nonlinear false-sparsity arm. Compare equal-call direct probing and clean fine-tuning; abandon if superposition only holds for negligible steps.
- **A/B retention:** Check A/B after recovery and after increasing the recovered patch to a useful size.

### PL5-04 · Spend a probe on the old choice — Ambitious but doable (P)
- **Failure → primitive:** A dictionary can span the shared gain but leave a fork’s private preference unconstrained; probe the locally uncertain direction most likely to move an old decision boundary before spending a write on the shared gain.
- **Literature / gap:** [OGD](https://arxiv.org/abs/1910.07104) projects against old-task output gradients; the choice here is which *interventional column to acquire* when those local effects are not already known.
- **Cheapest test:** Two candidate patches solve a new task but opposite policy choices make one infeasible. Compare task-coverage probes, passive guard evaluation with the same calls, and exact local gradients as an oracle.
- **A/B retention:** Score untouched A/B as well as matched old policies outside the guard contexts.

### PL5-05 · Translate the second use, not the first — Ambitious but doable (P)
- **Failure → primitive:** A probe on the untouched model can predict a successful first import and fail after that import changes the fork; measure a probe write once before and once after a common seed edit and use the difference to train an order-sensitive translation.
- **Literature / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) combines task vectors; PL4-05 represents ordered effects in an established code. This asks if a *newcomer* can learn just the interaction it needs from a second local intervention instead of learning a full nonlinear decoder.
- **Cheapest test:** Two small nets with a bias shift followed by a gated feature edit. Compare seed-conditioned one-shot translation with an extra independent probe and direct fine-tuning of the two-step task.
- **A/B retention:** Check A/B after both orders and after a third write that was never probed.

### PL5-06 · Translate only the part you can learn — Ambitious but doable (P)
- **Failure → primitive:** An ill-spanned code tempts the newcomer to extrapolate a dangerous patch; transmit back the residual in shared effect space and learn that residual from local examples while applying only the represented part.
- **Literature / gap:** [HyperTuning](https://arxiv.org/abs/2211.12485) generates adaptation parameters; PL4-08 projects onto locally reachable effects. Here the unrepresented target becomes a *new training objective* for the newcomer rather than a refusal or another dictionary column.
- **Cheapest test:** A fork can copy one of two lesson components but needs two examples to learn the other; compare refusing, local end-to-end fine-tuning and fitting just the unsupported component.
- **A/B retention:** Check A/B after the partial write, then again after the locally learned remainder.

### PL5-07 · Match displacement in tasks, not logits — Ambitious but doable (P)
- **Failure → primitive:** Forks may not share score scales or action vocabularies; fit each probe column to its change in success on a common downstream exercise rather than to activation or logit displacement.
- **Literature / gap:** [Policy Distillation](https://arxiv.org/abs/1511.06295) transfers from a trained policy; [CKA](https://arxiv.org/abs/1905.00414) compares representations. The common object here is a *change in exercised capability* under a write, even when there is no token-level map to distill.
- **Cheapest test:** Let two finite-state agents implement equivalent workflows with different action names and order. Compare action-aligned distillation, matched success before probing, and measured success increments as the decoder target.
- **A/B retention:** Check old workflows A/B and the newcomer’s distinct preferred route after a held-out shared code.

### PL5-08 · Let a failed write teach one feature — Ambitious but doable (P)
- **Failure → primitive:** The newcomer’s cheap write dictionary can be full rank yet lack a required feature; if a probe detects an absent effect, let that failed code supervise creation of exactly one new feature before fitting the patch.
- **Literature / gap:** [MAML](https://arxiv.org/abs/1703.03400) learns an initialization for rapid local fitting; PL4-13 splits feature and behavior training when the needed feature is already specified. Here a missing measured effect determines *which feature to create*, using authorized local outcomes.
- **Cheapest test:** Give a narrow model a missing XOR-relevant feature, and include an impossible arm lacking the underlying input. Compare blind rank growth, independent fitting and growth triggered by the failed code.
- **A/B retention:** Score A/B before growth, after the new feature is learned, and after a subsequent unrelated import.

### PL5-09 · Teach the fork with a reciprocal probe — Ambitious but doable (P)
- **Failure → primitive:** An exemplar probe chosen on a large fork may be uninformative for a smaller newcomer; let the newcomer’s own most interpretable write become the teaching example from which established forks infer the shared code.
- **Literature / gap:** [Model stitching](https://arxiv.org/abs/2106.07682) measures compatibility with a fitted bridge, and [FedMD](https://arxiv.org/abs/1910.03581) shares predictions across heterogeneous clients. This reverses onboarding: a local edit supplies a candidate reusable effect to the population, not merely a prediction or a slot in an existing decoder.
- **Cheapest test:** Give a small symbolic fork native access to a transform requiring multiple deep-model directions. Compare probing only established learners and symmetric bootstrapping with the same number of messages.
- **A/B retention:** Check the established forks’ old A/B and the newcomer’s original policy after another peer adopts the returned code.

### PL5-10 · Hold out an effect, not a model — Ambitious but doable (P)
- **Failure → primitive:** A few-probe learner can memorize familiar lesson families even on unseen architectures; meta-train the probe policy by making it select writes that let a receiver acquire an effect family withheld from the probe policy’s current episode.
- **Literature / gap:** [HyperShot](https://arxiv.org/abs/2203.11378) uses kernel hypernetworks for few-shot tasks, and [MAML](https://arxiv.org/abs/1703.03400) trains for fast task adaptation. The learned action here is an *experiment on the receiving model* that must generalize to unseen edit families, not a task embedding inferred from normal labeled examples.
- **Cheapest test:** Meta-train on rotations and thresholds; withhold one family of conditional edits, and compare random probes and a few-shot generator given the same support labels.
- **A/B retention:** Score A/B on untouched forks after each of two transfers from the held-out family.

## B · What must disappear when a source leaves?

### PL5-11 · Undo the clock as well as the mass — Ambitious but doable (P)
- **Failure → primitive:** Subtracting a source from an exponential running average still lets its arrivals age all of the other samples; run decay on retained-event counts so removing a source also removes the clock ticks it introduced.
- **Literature / gap:** [Batch normalization](https://arxiv.org/abs/1502.03167) uses inference statistics; [FedBN](https://arxiv.org/abs/2102.07623) keeps local normalization. The intervention here removes a source’s effect on *when* the retained evidence became stale, not just its own values.
- **Cheapest test:** Interleave two scalar streams with bursts from the retiring source; compare ordinary contribution subtraction, wall-clock decay and exact retained-only event replay. Charge storage for evaluating decay on the retained clock; a single mixed EMA need not suffice.
- **A/B retention:** Check A/B immediately after a long burst is removed and after the next allowed drift, without recalibrating on A/B.

### PL5-12 · Carry retained statistics through an exact feature change — Ambitious but doable (P)
- **Failure → primitive:** Stored survivor moments still live in a retired source’s feature coordinates; where the change is known affine, transport retained first and second moments through the inverse instead of treating their old coordinates as clean.
- **Literature / gap:** [FedBN](https://arxiv.org/abs/2102.07623) uses local statistics and [model stitching](https://arxiv.org/abs/2106.07682) fits activation maps. The operation uses a feature map to *unwrite inference state*, with exactness limited to sufficient statistics and the stated affine interface.
- **Cheapest test:** Detach a known affine adapter while holding A/B out. Compare reused moments, transported moments and retained replay; test a nonlinear adapter as a declared failure case.
- **A/B retention:** Score A/B under the transported normalizer, including features mixed by the retired adapter.

### PL5-13 · Learn ranks that survive a source leaving — Ambitious but doable (P)
- **Failure → primitive:** Removing a source can preserve moments yet move an operational tail threshold; learn separate score-to-rank curves whose mixtures predict empirical ranks under leave-one-source-out training.
- **Literature / gap:** [KLL quantile sketches](https://arxiv.org/abs/1603.05346) give generic mergeable rank estimates. The proposed training signal fits each source curve only on allowed data from that source and prioritizes rank error near the thresholds used after withdrawal, trading general rank guarantees for better tail decisions at fixed memory.
- **Cheapest test:** Three skewed, similarly centered streams with different tails; compare weighted local quantiles, pooled KLL sketches and fitted source curves at matched state bytes, against exact retained ranks.
- **A/B retention:** Score ordinary A/B and tail-specific A/B before and after the withdrawal.

### PL5-14 · Remove confidence without changing the underlying answer — Ambitious but doable (P)
- **Failure → primitive:** A retired source can continue to affect deferral even with clean predictions; fit the replacement abstention rule from retained score–outcome pairs, freezing the decision model and preserving the coverage budget of surviving groups.
- **Literature / gap:** [Temperature scaling](https://arxiv.org/abs/1706.04599) calibrates predictions; [FedNorm](https://arxiv.org/abs/2205.11096) uses modality-specific normalization. The proposed primitive targets the source-dependent *decision to defer*, not logits, and must beat ordinary retained-only recalibration at equal bytes.
- **Cheapest test:** Keep a binary predictor fixed while removing a source that changes high-confidence error rates. Compare global temperature scaling, no recalibration and held-in group-conditioned deferral from retained histograms.
- **A/B retention:** Check untouched A/B accuracy, coverage and wrong-answer rate among nondeferred cases on both surviving cohorts.

### PL5-15 · Teach the cache to forget the prefix — Ambitious but doable (P)
- **Failure → primitive:** Deleting a document’s KV entries leaves later entries that attended to it; train a chunk-local cache representation with no cross-source attention during encoding, so interactions happen only when reading it.
- **Literature / gap:** [Cache-Craft](https://arxiv.org/abs/2502.15734) reuses contextual chunk caches with partial recomputation, and [PagedAttention](https://arxiv.org/abs/2309.06180) manages KV blocks. Train for high quality when reading only the remaining chunk representations, not just fast reuse of previously contextualized KV; regenerate any downstream tokens that read the retired chunk rather than recaching their text.
- **Cheapest test:** A two-document attention toy with both cross-document and single-document queries. Compare masking old keys, fixed chunk-local encoding and trained chunk-local encoding against retained-only prefill; count the cross-document capability lost before withdrawal as well as the re-encoding avoided after it.
- **A/B retention:** Check unaffected A/B sessions and old behaviors reached only after regenerating the contaminated suffix.

### PL5-16 · Forget an index’s geometry, not only its entries — Ambitious but doable (P)
- **Failure → primitive:** Removing source documents leaves centroids or a scoring metric shaped by them; learn the retrieval geometry from an allowed-reference sample and let retractable sources add candidates without voting on that geometry.
- **Literature / gap:** [RAG](https://arxiv.org/abs/2005.11401) combines retrieval and parametric knowledge; [C²U in RAG](https://arxiv.org/abs/2610.29223) suppresses concepts on the query side with a fixed encoder and index. The proposal moves the training decision upstream so source withdrawal does not alter the meaning of distances among survivors.
- **Cheapest test:** A tiny centroid index where an outlying source changes bucket assignment. Compare tombstones, rebuilding retained geometry and a fixed clean-reference geometry at matched retrieval calls.
- **A/B retention:** Score A/B answer quality and retrieval recall on surviving documents, including a low-frequency topic.

### PL5-17 · Simulate the missing source during state learning — Ambitious but doable (P)
- **Failure → primitive:** An algebraically clean retained normalizer can be out of distribution for the model after removal; train the inference-state update rule to succeed on retained batches with one source randomly absent, never using that source’s activations as targets for the retained path.
- **Literature / gap:** [TENT](https://arxiv.org/abs/2006.10726) learns from the test batch via an entropy objective; [FedWon](https://arxiv.org/abs/2306.05879) removes normalization altogether. This training signal targets the *future update of inference state* under source withdrawal rather than improving today’s mixed-source batch.
- **Cheapest test:** Two drift streams with distinct shifts; compare ordinary dropout of examples, source-masked state learning, TENT after withdrawal and re-estimation at the same clean sample budget.
- **A/B retention:** Score A/B immediately and after the first five allowed inference updates, not just after full recovery.

### PL5-18 · Undo which observations were seen — Ambitious but doable (P)
- **Failure → primitive:** Source-local counts are not clean if a retired source chose which allowed observations were fetched; maintain a small independent exploration stream and use it, not retrospectively filtered counts, to update the survivor’s inference state.
- **Literature / gap:** [Influence functions](https://arxiv.org/abs/1703.04730) estimate effects of training points; PL4-27 routes selection-conditioned gradients. This operation defines a teacher-independent *observation channel* for persistent inference statistics even when no trainable weights move.
- **Cheapest test:** A bandit source chooses which inputs reach an online normalizer. Compare filtered observed values, inverse-propensity correction where feasible and a clean exploration stream at equal observation counts.
- **A/B retention:** Check A/B after withdrawal in both the previously over-observed and under-observed regions.

### PL5-19 · Replace an inference memory with a competing clean summary — Ambitious but doable (P)
- **Failure → primitive:** A compact state summary can be non-invertible, so there is no honest subtraction; learn a parallel allowed-only summary from a strictly smaller fixed stream and replace the mixed summary on withdrawal only where it passes an independent loss target.
- **Literature / gap:** [SISA](https://arxiv.org/abs/1912.03817) isolates and replays training shards; [RAGCache](https://arxiv.org/abs/2404.12457) caches retrieved knowledge for efficiency. The question is whether one *continuously learned alternative inference memory* pays for many future removals without reconstructing all retained events.
- **Cheapest test:** Two toy agents compress rolling event histories into one low-rank vector. Compare a frozen clean fallback, clean replay, and the live small summary under repeated withdrawals.
- **A/B retention:** Score A/B both immediately on fallback and after normal inference-state updates resume.

### PL5-20 · Restore the joint statistic without restoring the contributor — Ambitious but doable (P)
- **Failure → primitive:** Detaching a source-dependent cross moment can also remove an independently reproducible correlation; relearn that statistic directly from clean paired observations instead of reconstructing the retired source’s individual values.
- **Literature / gap:** [Partial information decomposition](https://arxiv.org/abs/1004.2515) separates redundant and synergistic information; PL4-17 stores factorized moments. The proposed operation replaces one jointly useful *state statistic* with independently supported observations, not a proxy for the old source.
- **Cheapest test:** Drop one sensor whose correlation was also observable in two retained sensors. Compare resetting the moment to zero, fresh norm fitting and focused clean pairing at equal reads.
- **A/B retention:** Check A/B on allowed single-sensor cases and cases requiring the recovered correlation, including a regime where it cannot be reidentified.

## C · Step sideways: what can only the population learn or forget?

### PL5-21 · Let a word mean what survives translation — Ambitious but doable (P)
- **Failure → primitive:** Probe onboarding presumes a fixed global code; learn a vocabulary in which a symbol is rewarded only when it causes the same transferable change on an unfamiliar recipient and survives a second translation without copying the first recipient’s policy.
- **Literature / gap:** [Lewis signaling games](https://arxiv.org/abs/2311.04453) study emergent communication, and [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) accumulates skills through social learning. The word’s meaning here is an executable edit that must survive another independent decoder, not a referent or demonstration.
- **Cheapest test:** Three small architectures send one of four symbols for recurring edits to held-out partners. Compare a fixed code, ordinary sender–receiver task reward and cross-generation edit reward at equal bits.
- **A/B retention:** Score every recipient’s old A/B and its legitimate nonconsensus choice after two generations of relay.

### PL5-22 · Let a newcomer split a word — Ambitious but doable (P)
- **Failure → primitive:** An established shared language can conflate effects that its original forks cannot distinguish; give a newcomer one new symbol only when its architecture exposes a split that changes held-out uptake by later peers.
- **Literature / gap:** [VQ-VAE](https://arxiv.org/abs/1711.00937) learns discrete codes from reconstruction, and [Lewis signaling games](https://arxiv.org/abs/2311.04453) study emergent vocabularies. The split is selected for *new downstream learnability revealed by a different learner*, not aggregate message reconstruction or frequency.
- **Cheapest test:** A new fork distinguishes two edits identical on old supports but consequential to a future fork. Compare increasing vocabulary blindly, using separate dialects and spending the new symbol only on a demonstrated split.
- **A/B retention:** Check that old peers still perform A/B using either meaning before and after learning the expanded code.

### PL5-23 · Use a statistic that belongs to the pair — Ambitious but doable (P)
- **Failure → primitive:** Source-local moments cannot identify correlations across observations no single peer sees together; let matched peers contribute joint sufficient statistics to a shared prediction rule and withdraw only the interaction if one participant leaves.
- **Literature / gap:** [Secure aggregation](https://arxiv.org/abs/1611.04482) sums user-held values; a sum of isolated marginal moments cannot identify a cross moment. [Partial information decomposition](https://arxiv.org/abs/1004.2515) distinguishes joint information. Give the toy an explicit allowed paired-product computation, and test when that collective statistic is a better memory than model averaging.
- **Cheapest test:** Two peers see opposite halves of matched pairs with identical marginals and either positive or negative correlation. Compare independent moments, permitted joint products and a fully pooled oracle.
- **A/B retention:** Score both peers’ old local A/B after the joint statistic is learned and after the interaction is retired.

### PL5-24 · Learn where to remain different — Ambitious but doable (P)
- **Failure → primitive:** A population may optimize onboarding until its members become interchangeable and stop learning complementary things; reward one fork for the new edit its distinct policy makes possible on another fork, subject to retaining its own old tasks.
- **Literature / gap:** [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) balances novelty and imitation; [FedMD](https://arxiv.org/abs/1910.03581) exchanges predictions to improve heterogeneous learners. The proposed signal selects for *useful differences in what can be taught next*, not for general agreement or diversity alone.
- **Cheapest test:** Two small agents see complementary contexts and one later curriculum needs both. Compare behavior diversity, copy-the-best, independent training and rewarding future cross-teaching under equal samples.
- **A/B retention:** Score A/B and each fork’s own unresolved but legitimate preference after repeated selection and exchange.

### PL5-25 · Forget by changing who can teach the statistic — Ambitious but doable (P)
- **Failure → primitive:** Locally clean inference states do not prevent an offline peer from reteaching a removed population statistic; train an independent successor on permitted paired evidence and move teaching to it before the mixed state can circulate again.
- **Literature / gap:** [FedEraser](https://arxiv.org/abs/2012.13891) reconstructs a global model from historical client updates; PL29 cuts known teaching routes. The population-level question is whether replacing a *teacher of inference state* preserves live sharing better than stopping the old route and relearning independently.
- **Cheapest test:** Bring a stale peer back after a two-source calibration withdrawal. Compare cutting all transfer, keeping the stale aggregate and reintroducing only updates from the independently trained successor.
- **A/B retention:** Check A/B across connected and offline cohorts after rejoin and one further teaching round, including the old skill that used the statistic.

### PL5-26 · Learn the limits of membership before learning the language — Ambitious but doable (P)
- **Failure → primitive:** Forcing every fork to join one code can spend scarce probes on effects that are locally impossible; split the population into overlapping teaching neighborhoods learned from reciprocal write success, with a single local fork allowed to specialize outside any neighborhood.
- **Literature / gap:** [FedMD](https://arxiv.org/abs/1910.03581) combines heterogeneous models by distillation, and [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns models for merging. Membership here is learned from *which causal edits transfer cheaply* rather than static weight or representation similarity.
- **Cheapest test:** Three learners have one transferable edit per pair but no universal edit. Compare one shared code, similarity clusters and overlapping groups with the same messages and decoder budget.
- **A/B retention:** Score A/B on every pair and on an isolated local skill after the neighborhood structure changes.

## Ranked deeper questions

1. **What does one probe buy that one labeled example does not?** (PL5-01–PL5-08, PL5-10) Start with known symmetries, then a genuine architecture mismatch and one effect that is locally impossible. Compare equal-cost interventional dictionaries, same-budget HyperTuning and direct fine-tuning on unseen edit families. Require useful gain and unchanged A/B; a probe that only names directions available to fine-tuning is not a new primitive.
2. **When is retained inference state genuinely independent of a retired source?** (PL5-11–PL5-19) Cross three dependency types—numerical contribution, upstream feature change and observation selection—with observed or missing clean state. Use retained-only replay as oracle. Name the assumptions under which immediate detachment is exact; where they fail, require honest abstention or costed recomputation.
3. **Can a vocabulary of edits get better as new learners join, without homogenizing those learners?** (PL5-09, PL5-21, PL5-22, PL5-24, PL5-26) Introduce a newcomer that exposes an edit ambiguity and then remove the original teacher. Demand successful transfer to an unfamiliar recipient across two relays, preservation of each fork’s A/B, and a win over fresh pairwise translators or independent learning at equal budget.
4. **Can the population keep a joint capability after the original way of knowing it is gone?** (PL5-20, PL5-23, PL5-25) Plant joint correlations no single peer can estimate, remove one contributor, and measure which are independently recoverable through allowed pairing. Test an offline peer’s return. Require old-task retention along both local and shared paths without treating the persistence of a correlation as evidence that its original source is still needed.
