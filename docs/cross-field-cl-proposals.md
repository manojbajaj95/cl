# Cross-field continual-learning proposals

These are testable hypotheses, not validated results. See the [review ledger](https://github.com/manojbajaj95/cl/pull/6) for accepted, rejected, and falsified ideas and the latest pilot controls. Before drafting a new proposal, read its latest revision as well as the [other proposer batches](https://github.com/manojbajaj95/cl/pull/5); revisit a rejected idea only if the new design addresses its stated failure.

Use the [stream contract](research-process.md#common-stream-contract): predict, score, then update; hold out entire streams; compare at equal whole-system budget. Each pilot should first try to falsify the proposed mechanism, not tune it into a win.

## Batch 1 · Coding theory and signal processing

### 1. Functional syndromes for sparse model-edit damage

**Hypothesis.** At one MEMIT-editable linear MLP projection, subsequent training may damage a small subset of old key→value associations much more than the rest. A compressed checksum can then identify and repair those associations without replaying their old examples or storing all old values.

Let `W₀` be the post-edit projection, `K` the matrix of old keys, and `S` a seeded random sketch across the keys. Save `C = KS` and `P = (W₀K)S`. After later training, `WC − P = ((W − W₀)K)S` is the syndrome. Decode the column-sparse damage matrix `E = (W − W₀)K` with a group-sparse solver; then fit the smallest correction that approximately removes the recovered damage at its keys and leaves recent keys unchanged. Store or regenerate a usable key dictionary for the repair and charge it in the budget; fast syndrome evaluation is not a claim that the keys themselves are free. There is no protection against arbitrary dense drift or a changed upstream representation.

**First falsifier.** For a sequence of MEMIT edits and later updates, freeze the measurement layer, score the full old key bank only for evaluation, and measure damage concentration. Stop if the worst 10% of old keys hold less than 80% of the error energy on held-out sequences. If it survives, compare against same-byte key/value rehearsal with re-editing and a dense random sketch decoded by least squares. Require improved held-out old-fact paraphrases without reducing recently learned facts or unrelated accuracy; report FLOPs and bytes including all retained slots.

**Prior art and scope.** [Algorithm-based fault tolerance](https://doi.org/10.1109/TC.1984.1676475) detects arithmetic errors with matrix checksums; [compressed sensing](https://arxiv.org/abs/math/0503066) supplies a sparse decoder; [MEMIT](https://arxiv.org/abs/2210.07229) supplies the key/value interface. The open question is whether *training-induced functional damage*, not injected faults, satisfies the sparsity assumption and can be repaired within budget. Unlike Noether memory, this is a read/repair operation after damage, not a conserved channel.

**Pilot falsified fixed-key sparsity.** The [GPT-2-XL pilot](https://github.com/manojbajaj95/cl/pull/24) found only 18.9–19.1% of raw response damage energy in the worst 10% of facts. Group-sparse decoding did not beat matched-budget baselines, and repair did not run. Positive answer-probability drops were much more concentrated, but the tested readout did not measure them; raw damage norm was weakly negatively correlated with the drops.

### 2. Functional sigma–delta for quantized writes

**Hypothesis.** Protected outputs need not inherit long-run rounding drift from irreversible low-bit parameter updates. For fixed protected Jacobian `J`, reference float update `u[t]`, and feasible quantized update `q[t]`, carry only `r[t] = r[t−1] + J(u[t] − q[t])`. If a quantizer keeps this small, cumulative protected linearized rounding error telescopes to `r[t] − r[0]`; this says nothing about whether a low-debt quantized update exists, and does not protect a moving Jacobian.

**First falsifier.** On 4-bit sequential linear regression then a tiny MLP, match new-task gain, count all projected-guard and rounding state, and compare straight-through rounding, stochastic and projected rounding, and [full-space error feedback](https://arxiv.org/abs/1901.09847). Reject as a CL method if its only gain is a smaller buffer. **Reviewer rejected:** full error feedback already removes long-run rounding error in all directions when the analogous state stays bounded. A smaller buffer alone is not a CL result.

## Batch 2 · Hysteresis and control

### 3. Return-point adapters

**Hypothesis.** If recurring environments have nested excursions in an observable control signal, a bank of [hysteresis](https://doi.org/10.1103/PhysRevLett.70.3347) cells can track the branch without a task ID. For a frozen backbone and a linear gate-to-adapter map, project inner-loop adapter updates to vanish at the saved outer gate states. On return to a saved state, the old adapter output matches exactly; sorting or averaging samples by current context cannot recover the approach history.

**First falsifier.** On unseen nested and nonnested streams, withhold regime labels and compare immediate reacquisition, new-task gain, and storage including saved gates with a budget-matched stateful fast-weight router, a nearest-context router, and a generic state stack. **Reviewer rejected:** keeping the protected gate states makes the result a form of save/restore; exactness by itself does not distinguish it from a matched router.

### 4. Plasticity reserve: choose the write that consumes the least future reachability

**Hypothesis.** When several current writes fit equally well and retain earlier skills equally well, prefer the one that leaves later changes cheap across diverse unlabeled probes. Current loss, gradient alignment and rank alone need not distinguish these destinations.

For each candidate write/route, linearize after the candidate, form the permissible-update projector `P` given old-skill and current-skill constraints, and sketch the probe-output Jacobian `G`. Rank candidates by `log det(λI + G P Gᵀ)` with a fixed metric, sample budget and ridge. In the linear model, reserving a new normalized direction `u` in the feasible subspace reduces that Gramian by `(Gu)(Gu)ᵀ`. If the routes produce the same constraints, parameter metric and behavior geometry, there is no choice to exploit. If unlabeled probes do not represent later tasks, the score can prefer the wrong route.

**First falsifier.** Train a CPU MLP on at least 50 tasks with eight candidate writes per stage, each matched for current loss, old retention and write budget. Use the same candidates for random choice, effective-rank choice, [optimization readiness](https://arxiv.org/abs/2605.09044) and Gramian choice. Compare next-task fixed-budget gain, paired across held-out streams. Kill if the score's rank correlation with next-task gains does not beat readiness, or if choosing by it does not improve next-task gain. Use unrelated probe/next-task shifts as a negative control; do not reveal future labels to the chooser.

**Prior art and scope.** [History-dependent reachability](https://arxiv.org/abs/2602.07950) defines the minimum input energy to reach a joint learning/retention target. [Control minimization](https://arxiv.org/abs/2602.04542) applies control objectives to CL. This proposal uses a probe-output Gramian to choose among otherwise equivalent *present* writes with future tasks hidden. Optimization readiness is an active chooser here, not just a diagnostic to cite.

**Pilot falsified the tested predictor.** [The CPU pilot](https://github.com/manojbajaj95/cl/pull/9) found a 4.9 percentage-point range in next-task gains across the equal-loss candidate writes, but the unprojected Gramian score had Spearman correlation −0.015 with that gain and did not beat the controls. The pilot did not test the old-skill-constrained projector above.

**Retention-matched rerun stopped at the variance gate.** [The projected rerun](https://github.com/manojbajaj95/cl/pull/21) found a next-task gain spread of only 0.458 relative percentage points and 0.091 absolute MSE points (`100 × ΔMSE`) across 512 seeds, below the prespecified 1.5 absolute-point floor. It did not run the ranking arms.

## Batch 3 · Rare-event simulation and structural rank

### 5. Rare-event distillation

**Hypothesis.** In continual on-policy distillation, rare old-skill triggers can occur mid-trajectory under common prompts. At a fixed rollout/teacher budget, branching informative prefixes can make the old behavior learnable when independent replay rarely visits it. The proposed effect is in trained behavior, not just a more efficient audit. If prompts identify the trigger, oversample those prompts instead.

Use a relevance score trained on old development streams to split student prefixes into several continuations at staged thresholds. Resample with known probabilities; keep the sampling weights and use an importance-weighted numerator for a prespecified tail distillation loss. Normalize and report the bias/variance of the normalization separately. Fork student continuations, not teacher-forced prefixes, and keep ordinary replay for broad coverage. Trigger membership should not depend on whether the student solves the old task. Never claim recovery for paths with no student support or where the predictor cannot locate the high-risk subtree cheaply.

**First falsifier.** Use a tiny sequence policy with a rare delayed trigger for an old rule. Compare independent student replay, [uniform prefix replay](https://arxiv.org/abs/2607.04763), prompt upsampling, equally trained leaf selection, and teacher-forced positive trajectories, with common prompts, old teacher, total generated tokens, teacher queries and scorer FLOPs. Hold trigger families and frequencies out; score correct behavior after a trigger, student probability of reaching it, and new-task progress. Kill if splitting does not beat the best baseline on old tail accuracy at matched new-task gain and common-behavior accuracy. Include an uninformative-score control and an early visible trigger where ordinary oversampling should win.

**Prior art and scope.** [Adaptive multilevel splitting](https://doi.org/10.1080/07362990601139669) estimates rare-event risks; [continual MOPD replay](https://arxiv.org/abs/2611.02746) replays earlier domains against the previous student; [SPOT](https://arxiv.org/abs/2608.04419) probes alternate continuations in OPD. The distinction to test is weighted branching for old-tail retention under the same budget, not branching as a novelty claim.

**Pilot falsified the tested method.** [The pilot](https://github.com/manojbajaj95/cl/pull/12) found no clear rare-recovery gain over frequency-weighted prompt upsampling (−6.48 percentage points, 95% CI [−40.52, +27.55]) and worse common behavior than MOPD replay (−1.06 percentage points, 95% CI [−1.66, −0.47]). A new attempt needs both a substantially tighter rare-event estimate and a way to protect common behavior.

### 6. Sparse-write feasibility certificates

**Hypothesis.** A routed model's structural zeros may identify masks with little room for safe updates before computing a dense Jacobian. For a fixed routing pattern and parameter mask `S`, a first-order direction on `S` can change a new scalar logit without changing protected logits iff the new Jacobian row adds rank to the old Jacobian restricted to `S`. Under generic coefficients with that support, the ranks of the old and augmented matrices equal the sizes of maximum bipartite matchings. Two matchings therefore test generic feasibility from supports alone.

Cache protected row supports, then use the certificate to reject masks and rank feasible ones; still solve and verify the numerical update. A generic certificate is not a guarantee about a particular ill-conditioned or parameter-tied Jacobian. It also says nothing about finite steps that cross router boundaries. If only dense or nearly identical supports appear, there is no useful signal.

**First falsifier.** Tune and freeze amplitude and numerical-rank tolerances on development streams. In a tiny hard-routed MLP with frozen routing within a write, compare shortlisted masks with numerical nullspace projection and size/overlap heuristics. Hold out router compositions and include tied parameters as a symmetry counterexample. **Reviewer rejected:** the upper bound on each rank does not certify that the ranks are equal for learned weights; a masked numerical factorization is a cheap and exact linearized control.

**Prior art and scope.** [Structural rank](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.structural_rank.html) is established; [OGD](https://arxiv.org/abs/1910.07104) and [small-singular-value projection](https://arxiv.org/abs/2602.21919) protect tasks with numerical subspaces. The research question is where the cheap combinatorial rank prediction is both reliable and useful in a trained learner, not whether graph matching implies generic rank.

## Batch 4 · Equivalence classes and discrepancy

### 7. Effect-class distillation

**Hypothesis.** Token-level old-teacher distillation spends capacity retaining old syntax that the next task legitimately changes. For executable outputs, define an effect class by the resulting state and relevant side effects over prespecified inputs. Distill the old teacher's probability mass across those classes, not over programs within each class.

The chain rule decomposes sequence KL into class-level KL plus expected within-class KL. Dropping the latter permits style changes without putting pressure on old observable effect distributions. Estimate class masses exactly for a small enumerated grammar first. Reward-only replay is a distinct baseline: rewarding validity does not generally preserve the distribution over several valid effects. If the class is just the binary reward, or if equivalence is not stable under real inputs, that distinction is lost.

**First falsifier.** Continually train a small code model through an API or library migration that changes required syntax while preserving old effects under held-out inputs. Compare token KL, canonicalized token KL, and verifier/reward-only replay at matched execution calls and generated tokens. Kill if the old-pass vs. new-syntax frontier does not beat both canonicalized KL and execution-only replay; test misclassified side effects as a negative control. [OPSD theory](https://arxiv.org/abs/2610.05200) and [Purified OPSD](https://arxiv.org/abs/2607.02234) motivate separating useful teacher signal from incidental variation; the proposed advance is preserving executable outcome distributions under sequential change.

**Pilot falsified the tested method.** [The CPU pilot](https://github.com/manojbajaj95/cl/pull/13) beat canonicalized token KL but did not beat execution-reward-only replay (retention/adoption hypervolume difference −0.0028, 95% CI [−0.0064, +0.0008]). It evaluated fixed completions and plain fine-tuning was near ceiling. A resubmit would need free generation and a stream where plain fine-tuning forgets.

### 8. Bounded-delay stability scheduling

**Hypothesis.** With the same stream examples and update count, training order can determine how deep the temporary retention dip is. Keep a small deadline-bounded buffer and greedily choose the next example to counteract the running sum of estimated old-logit changes; flush near deadlines. Nothing is added, reweighted or dropped.

With frozen additive updates and zero net old-logit displacement, bounded vector discrepancy guarantees an ordering whose worst-prefix displacement depends on guard dimension rather than total steps. This is an offline sanity bound, not a bound for deadline-constrained nonlinear SGD. A biased net displacement, optimizer memory, and stale Jacobians may make the ordering useless.

**First falsifier.** Pair streams of a small MLP under clustered and dispersed conflicting gradient exposures. On held-out retention probes, measure worst-prefix loss and time above a fixed regression threshold, at equal terminal old/new quality, prospectively fixed delay, and measured compute. Compare FIFO, uniform reshuffling, standard gradient-balanced reshuffling, and same-latency gradient accumulation. Kill if any ties the best trade-off. [The stability gap](https://arxiv.org/abs/2205.13452) motivates the metric; [GraB](https://arxiv.org/abs/2205.10733) motivates the reordering control. This is not a proposal to synthesize counter-gradient data.

**Reviewer rejected:** simple accumulation eliminates within-window ordering effects at matched latency. Reordering only offers an advantage if the deployed model must change and be evaluated inside the window.

## Batch 5 · Delayed control and metamorphic testing

### 9. Delay-compensated retention feedback

**Hypothesis.** When old-skill verification takes longer than a weight update, a model can admit more useful writes at the same exposure to regressions by correcting an estimate of *current* retention, not by using each late score as though it described the latest model.

Use cheap sentinel outputs to forecast a full audit score and launch a limited number of delayed full audits. When an audit arrives, subtract the forecast stored **for that checkpoint** and propagate the residual to the current forecast using a calibrated state-space observer. Gate or shrink prospective writes based on its uncertainty, with a predeclared fallback to waiting for verification. This borrows prediction-based time-delay compensation from control; it is not a guarantee against sudden unmodeled forgetting, and pending audits have real compute and snapshot costs.

**First falsifier.** On paired scripted update streams in a tiny policy, vary delay and insert held-out bursts of old-skill interference. Compare synchronous admission, stale-score admission, a simple current-sentinel gate, and an exponential average of past forecast residuals at the same audit budget. Measure new-task gain at matched harmful exposure (including exposure between audits), not just violations caught later. Kill if gains vanish against the current-sentinel control or if calibration breaks at deployment delays. [Auditing update admission](https://arxiv.org/abs/2609.10873) supplies a rigorous synchronous control.

**Reviewer rejected:** [online risk control with delayed outcomes](https://arxiv.org/abs/2611.17059) already provides the mechanism. Applying it to update admission is chiefly a scheduling change, not a distinct continual learner.

### 10. Composition contracts for hybrid skill retention

**Hypothesis.** Atomic old-skill tests can stay stable while compositions of old and new operations fail. A continual learner can detect and reduce this failure without an old teacher for the new composition by training against known identities that relate the outputs of two equivalent execution paths.

For an executable toy stream, retain a few anchors to rule out constant-output collapse. Generate unlabeled hybrid prompts from a typed DSL. Penalize a mismatch between the model's end-to-end prediction and the result of composing its primitive predictions in an independently defined order that must agree. The training process gets the relation, not the correct target for either hybrid path. If the relation and anchors already determine every target cheaply, generate labels directly instead.

**First falsifier.** Introduce operations sequentially, hold out compositions and input factors, and restrict primary scoring to runs matched on atomic skill retention and new-operation acquisition. Compare teacher replay, ordinary augmentation, and supervised pseudo-labeling from the same identities at equal execution and compute budget. Kill if the hybrid-retention effect disappears at matched atomic quality or simple augmentation/pseudo-labeling matches it. [Compositional CL benchmarks](https://arxiv.org/abs/2609.22055) motivate the separate hybrid cohort; they do not establish that relational training helps.

**Reviewer rejected:** with correct, executable atomic operations, directly composing them produces supervised hybrid labels from the same information.

## Batch 6 · Interaction measurements and reachability forecasts

### 11. Coded merge interference for irreversible consolidation

**Hypothesis.** When independently useful adapters must be consolidated into one deployed model, some old-skill regressions depend on pairs of writes and are invisible to singleton audits. If a small set of interactions explains the damage, grouped signed merges can locate those interactions at lower audit cost than checking pairs individually, leaving budget to choose a better consolidation.

Set a merge anchor and a fixed set of pending deltas. Audit both signs of a random vector of small coefficients and average the two probe scores. This cancels odd orders; at quadratic order the diagonal terms contribute only a constant because each coefficient's magnitude is fixed. Fit an intercept and sparse off-diagonal effects using pairwise products of the signs. Use the fit only for candidate selection; independently audit the chosen merge before the pending deltas are discarded. With zero higher-order terms, singleton audits cannot distinguish two score functions that differ only by a cross term. This is not true of grouped audits, and sparsity or a negligible higher-order residual is not guaranteed.

**First falsifier.** In a CPU MLP stream with sequential adapter consolidation, measure whether the fitted model predicts held-out *positive* merges at realistic coefficients, using exhaustive pair audits on a small development stream only as a diagnostic. Compare it with receiver-local linear/logit surrogates, selective direct pair audits, and direct search or ridge on exactly the same grouped observations. Charge both signed audits, pending-delta bytes, and final verification. Kill if out-of-sample regression ranking fails, or if the same-budget controls tie old/new performance after repeated consolidation. A known-sparse quadratic recovered six interactions from 120 signed rows versus 276 pairs; this is only an algebra check, not evidence about real models.

**Prior art and scope.** [Receiver-local linearization](https://arxiv.org/abs/2611.25000) forecasts merge interference with directional derivatives and can fit one merge through teacher matching. The proposed distinction is learning cross terms of black-box old-skill scores from grouped evaluations in a sequential, irreversible consolidation budget, not first-order merge prediction.

**Reviewer rejected.** [BOCS](https://arxiv.org/abs/1806.08838) already learns a sparse quadratic surrogate from black-box grouped evaluations; [LoraHub](https://arxiv.org/abs/2307.13269) already searches grouped adapter combinations without gradients. The algebra check does not distinguish the proposal from those controls.

### 12. Forecast-weighted write selection

**Hypothesis.** Among writes matched for both observed new-task loss and old retention, the useful projected update directions depend on which residuals the next task is likely to require. The practice of maximizing unweighted reachability should be replaced by predicting finite-step adaptation gain using a shared, history-only forecast of those residuals.

On a fixed probe set, let `K = G P Gᵀ` be the post-write kernel of the actual projected next-task learner. Estimate the next-target distribution using completed training tasks only. For each candidate let `M` be the conditional second moment of the forecast targets minus its own predicted probe outputs. With fixed Jacobian, stable squared-loss gradient descent and step `η`, expected `h`-step loss decrease is `tr(M [I − (I − ηK)^(2h)])/2`. The expression follows by propagating the residual through `h` steps; its directional weights and horizon differ from log determinant and a point-forecast one-step score. A two-mode linear sanity check gives different expected gains at equal log determinant and equal point-forecast gain. This does not validate forecasting on held-out streams.

**First falsifier.** Reuse the reserve pilot's CPU task generator; match the candidate writes for old retention as well as current loss and actually use a projected next-task learner. First stop if the spread in measured next-task gain vanishes. Compare all choices with projected readiness using the exact same history and forecast draw budget, diagonal/isotropic covariance, and direct projected lookahead on sampled forecast tasks. Do not call an analytic shortcut on a linear toy a CL gain: if same-budget lookahead/readiness ties on held-out sequential streams, stop. Use shuffled and unrelated task shifts as negative controls. The [original pilot](https://github.com/manojbajaj95/cl/pull/9) already falsified the unprojected Gramian; this is a candidate replacement, not evidence that it works.

**Stopped at the variance gate.** The reviewer included this as a comparison arm, but the [retention-matched rerun](https://github.com/manojbajaj95/cl/pull/21) found too little next-task gain left to rank and did not run forecast-weighted selection. This closes the reserve line on that stream; it does not compare the predictors.

## Batch 7 · Gate-only alternatives after fixed-key damage proved dense

### 13. Use the current model to decode old answers from shared parity

**Hypothesis.** A model can stop preferring a previously retained answer while still including it among a small list of candidates. Encode the old valid answers jointly, then use the later model's answer likelihoods as side information to decode the block. Shared parity allocates redundancy across whichever facts become ambiguous *later*, rather than spending an equal number of check bits on every fact. Unlike the failed layer sketch, this observes answer identity without guessing which old keys suffered damage.

At write time, store a seeded hash or parity of a block of canonical target token sequences. At recovery time, generate candidate answers from the current model without showing it old targets or alternate answers, and rerank joint assignments subject to the stored bits. On small development blocks, enumerate assignments in score order and report the rank of the true block; a random `b`-bit fingerprint has at most `(R−1)/2^b` probability of matching any of the `R−1` better-ranked assignments. This bound assumes the true block is present and does not address search cost. Use separate verification bits or abstain on ambiguity. Protect only still-valid facts; charge the prompt catalog, membership/version flags, serialized labels, verification bits and inference calls to all relevant arms.

**First falsifier.** Start with the successfully inserted facts in the [MEMIT traces](https://github.com/manojbajaj95/cl/pull/24). On held-out streams, first measure live top-k coverage among lost old answers and the bit cost of ideal list selection, including unchanged answers. Stop if the true targets routinely leave the affordable lists, or if the ideal bit saving disappears against direct entropy-coded answer storage once metadata is included. Only then compare matched-budget shared parity, independent per-fact fingerprints, and compressed answer replay with identical prompts, model-call and re-edit budgets. For a pass, require better accurate recovery without extra false corrections and better held-out paraphrase retention at equal new-task loss.

**Prior art and scope.** [Slepian–Wolf coding](https://doi.org/10.1109/TIT.1973.1055037) already supplies source coding with decoder side information. [Lifelong compact editing memory](https://arxiv.org/abs/2611.25861) is a system baseline. The untested CL claim is that a post-update model retains enough *usable* answer-side information across successive writes to make the trade worthwhile, not that shared parity is new.

### 14. Test low-rank damage as an alternative to sparse facts

**Hypothesis.** Raw response damage can be dense across facts but have a small spectral dimension. Save two-sided sketches of the old response and subtract the new sketches before reconstruction, so the reconstruction budget tracks the rank of the *change*, not the rank of old knowledge.

With `A = W₀K`, old sketches `LA` and `AS`, and live differences `X = LE` and `Y = ES` for `E = (W−W₀)K`, use the generalized Nyström reconstruction `Y(LY)⁺X` with a stable rank truncation. Recovery is exact for noiseless rank-r damage when the sketch maps have the needed ranks. This is standard sketch algebra; the CL question is whether the small-rank part is harmful at the level of actual behavior and correctable without removing useful learning. Charge the mixed input keys and any regenerated or retained key dictionary.

**First falsifier.** From the saved weight changes and keys, measure rank-vs-energy at the actual matched-byte ranks and test whether the oracle truncated component predicts held-out answer regressions beyond raw norm and prior answer margin. Stop if either gate fails. Before a repair pilot, compare a truncated-weight-drift correction where a checkpoint is affordable, same-byte old-output SVD and raw replay, and a same-information two-sided reconstruction using regularized least squares. Kill if the useful old/new tradeoff is reproduced by one of these. A synthetic exact rank-4 case reconstructed to numerical precision, but says nothing about MEMIT drift or which directions to restore.

**Prior art and scope.** [Randomized two-sided matrix sketching](https://arxiv.org/abs/1609.00048) supplies the decoder. [Low-rank function-space forgetting](https://arxiv.org/abs/2606.18024) is the nearest CL hypothesis. No separate pilot until the existing trace establishes a behavior-linked signal beyond the failed sparse-fact readout.

## Screened before submission

- **Remove gradient holonomy:** [The Lie Bracket as an Early-Warning Signal for Catastrophic Forgetting](https://arxiv.org/abs/2611.20087) already makes the core connection between noncommuting task updates and forgetting. A diagnostic-only version is not distinct.
- **Hidden relaxation modes after a matched checkpoint:** [Matched Specialization, Different Adaptation](https://arxiv.org/abs/2610.15830) already pairs output-matched histories and swaps Adam states to locate hidden adaptation effects. A Kovacs-style test alone would be too narrow to send.
- **Contrastive old-teacher context:** [Repulsive and Attractive Teachers](https://arxiv.org/abs/2609.21561) already contrasts correct and incorrect teacher contexts on the same student rollout. Adding a continual replay stream would not establish a new distillation mechanism.
- **Adapter transport across representation drift:** [GRAFT](https://arxiv.org/abs/2611.18638) already fits a bridge on paired activations and uses it to transfer old adapters. Applying the same bridge to successive versions of one backbone is not a new operation.
- **Teacher-reachable replay for old behaviors:** [CoRD](https://arxiv.org/abs/2611.07959) already couples student and teacher rollouts to supervise states the student does not reach. An old-teacher version is a control for a future rare-event proposal, not a new mechanism on its own.
- **Retroactive updates for delayed labels:** first-order transport of a late correction through the intervening training steps is the same Jacobian product used by [SGD-based leave-one-out influence](https://arxiv.org/abs/1906.08473), with the sign changed for insertion. Without a new way of retaining or using that sensitivity, this is an application of old machinery; [label-delay CL](https://arxiv.org/abs/2312.00923) already supplies replay controls.
- **Distill the sign of old-task support→query learning responses:** identical model outputs and empirical kernel spectra can hide opposite support→query transfer (an exact two-unit tanh construction). That is not a reason to run a ranking pilot: in a 64-seed shifted-recurrence sanity check, matching historical/current losses gave 0.0164 MSE median paired gain spread, but also matching starting support/query loss reduced it to 0.0065. Before testing a distillation method, find a stream with decision-relevant absolute spread and include [lookahead meta-replay](https://arxiv.org/abs/2007.13904) on the same old support/query budget.
