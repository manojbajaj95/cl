# Cross-field continual-learning proposals

These are testable hypotheses, not validated results. See the [review ledger](https://github.com/manojbajaj95/cl/pull/6) for accepted, rejected, and falsified ideas and the latest pilot controls. Before drafting a new proposal, read its latest revision as well as the [other proposer batches](https://github.com/manojbajaj95/cl/pull/5); revisit a rejected idea only if the new design addresses its stated failure.

Use the [stream contract](research-process.md#common-stream-contract): predict, score, then update; hold out entire streams; compare at equal whole-system budget. Each pilot should first try to falsify the proposed mechanism, not tune it into a win.

## Batch 1 · Coding theory and signal processing

### 1. Functional syndromes for sparse model-edit damage

**Hypothesis.** At one MEMIT-editable linear MLP projection, subsequent training may damage a small subset of old key→value associations much more than the rest. A compressed checksum can then identify and repair those associations without replaying their old examples or storing all old values.

Let `W₀` be the post-edit projection, `K` the matrix of old keys, and `S` a seeded random sketch across the keys. Save `C = KS` and `P = (W₀K)S`. After later training, `WC − P = ((W − W₀)K)S` is the syndrome. Decode the column-sparse damage matrix `E = (W − W₀)K` with a group-sparse solver; then fit the smallest correction that approximately removes the recovered damage at its keys and leaves recent keys unchanged. Store or regenerate a usable key dictionary for the repair and charge it in the budget; fast syndrome evaluation is not a claim that the keys themselves are free. There is no protection against arbitrary dense drift or a changed upstream representation.

**First falsifier.** For a sequence of MEMIT edits and later updates, freeze the measurement layer, score the full old key bank only for evaluation, and measure damage concentration. Stop if the worst 10% of old keys hold less than 80% of the error energy on held-out sequences. If it survives, compare against same-byte key/value rehearsal with re-editing and a dense random sketch decoded by least squares. Require improved held-out old-fact paraphrases without reducing recently learned facts or unrelated accuracy; report FLOPs and bytes including all retained slots.

**Prior art and scope.** [Algorithm-based fault tolerance](https://doi.org/10.1109/TC.1984.1676475) detects arithmetic errors with matrix checksums; [compressed sensing](https://arxiv.org/abs/math/0503066) supplies a sparse decoder; [MEMIT](https://arxiv.org/abs/2210.07229) supplies the key/value interface. The open question is whether *training-induced functional damage*, not injected faults, satisfies the sparsity assumption and can be repaired within budget. Unlike Noether memory, this is a read/repair operation after damage, not a conserved channel.

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

## Batch 3 · Rare-event simulation and structural rank

### 5. Rare-event distillation

**Hypothesis.** In continual on-policy distillation, rare old-skill triggers can occur mid-trajectory under common prompts. At a fixed rollout/teacher budget, branching informative prefixes can make the old behavior learnable when independent replay rarely visits it. The proposed effect is in trained behavior, not just a more efficient audit. If prompts identify the trigger, oversample those prompts instead.

Use a relevance score trained on old development streams to split student prefixes into several continuations at staged thresholds. Resample with known probabilities; keep the sampling weights and use an importance-weighted numerator for a prespecified tail distillation loss. Normalize and report the bias/variance of the normalization separately. Fork student continuations, not teacher-forced prefixes, and keep ordinary replay for broad coverage. Trigger membership should not depend on whether the student solves the old task. Never claim recovery for paths with no student support or where the predictor cannot locate the high-risk subtree cheaply.

**First falsifier.** Use a tiny sequence policy with a rare delayed trigger for an old rule. Compare independent student replay, [uniform prefix replay](https://arxiv.org/abs/2607.04763), prompt upsampling, equally trained leaf selection, and teacher-forced positive trajectories, with common prompts, old teacher, total generated tokens, teacher queries and scorer FLOPs. Hold trigger families and frequencies out; score correct behavior after a trigger, student probability of reaching it, and new-task progress. Kill if splitting does not beat the best baseline on old tail accuracy at matched new-task gain and common-behavior accuracy. Include an uninformative-score control and an early visible trigger where ordinary oversampling should win.

**Prior art and scope.** [Adaptive multilevel splitting](https://doi.org/10.1080/07362990601139669) estimates rare-event risks; [continual MOPD replay](https://arxiv.org/abs/2611.02746) replays earlier domains against the previous student; [SPOT](https://arxiv.org/abs/2608.04419) probes alternate continuations in OPD. The distinction to test is weighted branching for old-tail retention under the same budget, not branching as a novelty claim.

### 6. Sparse-write feasibility certificates

**Hypothesis.** A routed model's structural zeros may identify masks with little room for safe updates before computing a dense Jacobian. For a fixed routing pattern and parameter mask `S`, a first-order direction on `S` can change a new scalar logit without changing protected logits iff the new Jacobian row adds rank to the old Jacobian restricted to `S`. Under generic coefficients with that support, the ranks of the old and augmented matrices equal the sizes of maximum bipartite matchings. Two matchings therefore test generic feasibility from supports alone.

Cache protected row supports, then use the certificate to reject masks and rank feasible ones; still solve and verify the numerical update. A generic certificate is not a guarantee about a particular ill-conditioned or parameter-tied Jacobian. It also says nothing about finite steps that cross router boundaries. If only dense or nearly identical supports appear, there is no useful signal.

**First falsifier.** Tune and freeze amplitude and numerical-rank tolerances on development streams. In a tiny hard-routed MLP with frozen routing within a write, compare shortlisted masks with numerical nullspace projection and size/overlap heuristics. Hold out router compositions and include tied parameters as a symmetry counterexample. **Reviewer rejected:** the upper bound on each rank does not certify that the ranks are equal for learned weights; a masked numerical factorization is a cheap and exact linearized control.

**Prior art and scope.** [Structural rank](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.structural_rank.html) is established; [OGD](https://arxiv.org/abs/1910.07104) and [small-singular-value projection](https://arxiv.org/abs/2602.21919) protect tasks with numerical subspaces. The research question is where the cheap combinatorial rank prediction is both reliable and useful in a trained learner, not whether graph matching implies generic rank.

## Batch 4 · Equivalence classes and discrepancy

### 7. Effect-class distillation

**Hypothesis.** Token-level old-teacher distillation spends capacity retaining old syntax that the next task legitimately changes. For executable outputs, define an effect class by the resulting state and relevant side effects over prespecified inputs. Distill the old teacher's probability mass across those classes, not over programs within each class.

The chain rule decomposes sequence KL into class-level KL plus expected within-class KL. Dropping the latter permits style changes without putting pressure on old observable effect distributions. Estimate class masses exactly for a small enumerated grammar first. Reward-only replay is a distinct baseline: rewarding validity does not generally preserve the distribution over several valid effects. If the class is just the binary reward, or if equivalence is not stable under real inputs, that distinction is lost.

**First falsifier.** Continually train a small generator on scripts with several semantically valid effects and a newly required syntax, while preserving old behavior under held-out inputs. Compare token KL, canonicalized token KL, and verifier/reward-only replay at matched oracle calls, generated tokens and new-task gain. Kill if canonicalization or reward replay matches old effect retention; test misclassified side effects as a negative control. [Latest OPSD theory](https://arxiv.org/abs/2610.05200) and [Purified OPSD](https://arxiv.org/abs/2607.02234) motivate separating useful teacher signal from incidental output variation; the putative advance is preserving executable outcome distributions under sequential change.

### 8. Bounded-delay stability scheduling

**Hypothesis.** With the same stream examples and update count, training order can determine how deep the temporary retention dip is. Keep a small deadline-bounded buffer and greedily choose the next example to counteract the running sum of estimated old-logit changes; flush near deadlines. Nothing is added, reweighted or dropped.

With frozen additive updates and zero net old-logit displacement, bounded vector discrepancy guarantees an ordering whose worst-prefix displacement depends on guard dimension rather than total steps. This is an offline sanity bound, not a bound for deadline-constrained nonlinear SGD. A biased net displacement, optimizer memory, and stale Jacobians may make the ordering useless.

**First falsifier.** Pair streams of a small MLP under clustered and dispersed conflicting gradient exposures. On held-out retention probes, measure worst-prefix loss and time above a fixed regression threshold, at equal terminal old/new quality, prospectively fixed delay, and measured compute. Compare FIFO, uniform reshuffling, standard gradient-balanced reshuffling, and same-latency gradient accumulation. Kill if any ties the best trade-off. [The stability gap](https://arxiv.org/abs/2205.13452) motivates the metric; [GraB](https://arxiv.org/abs/2205.10733) motivates the reordering control. This is not a proposal to synthesize counter-gradient data.

## Screened before submission

- **Remove gradient holonomy:** [The Lie Bracket as an Early-Warning Signal for Catastrophic Forgetting](https://arxiv.org/abs/2611.20087) already makes the core connection between noncommuting task updates and forgetting. A diagnostic-only version is not distinct.
- **Hidden relaxation modes after a matched checkpoint:** [Matched Specialization, Different Adaptation](https://arxiv.org/abs/2610.15830) already pairs output-matched histories and swaps Adam states to locate hidden adaptation effects. A Kovacs-style test alone would be too narrow to send.
