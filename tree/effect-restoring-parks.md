# Effect-restoring parks: cancel moments on B, recompute scale from C

**Status:** Ideas only; one exact rational paper fixture, no pilots or GPU work. **Parent:** [Norm-restoring parks](norm-restoring-parks.md) ([PR #261](https://github.com/manojbajaj95/cl/pull/261)). **Seed:** score-3 [flood triage, row 376][triage]: [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) (train C so Adam first-moment and scaling differences cancel along B's declared proposal directions without restoring moments) and [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) (recompute the norm scale from a feature C genuinely needs so a stored historical accumulator can be deleted). **Ledger read first:** [Idea ledger][ledger]. **P** marks a candidate reusable primitive, not established novelty; **I** marks a method, comparison, or falsifier.

## The bet and what would count

A norm-restoring park ([PR #261](https://github.com/manojbajaj95/cl/pull/261)) asks genuine **C** learning to make reachable hidden histories equivalent for declared park readers while a rewritten producer restores a common norm scale. That still asks too much in two places: it tries to make hidden moments equivalent (or push second-moment gaps into reader-null subspaces) rather than letting opposing moment and denominator differences cancel on B's declared proposals, and it keeps historical norm accumulators around instead of deleting them in favor of a feature C already has to maintain. An **effect-restoring park** drops both requirements:

- **Cancel the executed B update, not the moments.** Across reachable histories $H_1, H_2$, Adam's first moment $m$ and second moment $v$ stay distinct and live on coordinates B actually reads—not reset, not equated, and not hidden in a reader-null subspace—yet their numerator and denominator differences cancel on B's declared proposal set $\mathcal{D}_B$ and readout $W_B$, so the executed native B step agrees while off-span or opposite-sign C gradients still see the live history-specific moments.
- **Delete one historical accumulator by overloading a C-essential job.** Remove a stored norm/scale accumulator under a fixed byte budget and recompute the scale from a feature $z$ that C genuinely needs. Prove $z$ is not a disguised backup copy by ablating $z$ (or replacing it with a history-blind constant) and verifying an independent old C reader breaks, while ordinary C updates keep the recovered scale valid.
- **Allow effect-level coupling across the boundary, and beat the stacked controls.** At the joint frontier, neither the moments $(m, v)$ nor the job-recovered scale $\phi(z)$ need be history-invariant on their own if their product restores the executed B effect. Every claim must be tested against the full stacked control: PKR12 full hidden-state equivalence ([PR #261](https://github.com/manojbajaj95/cl/pull/261)), reader-null $v$ absorption (`#246#07`), moment reset, norm reset, [GEM][gem]/[Adam-NSCL][nscl], [RMSNorm][rms]-style factoring without the C-job requirement, a backup accumulator at equal bytes, the strongest legal public scale schedule $\nu(p)$, an undeclared B proposal direction where differences do not cancel, and a C stream that stops maintaining $z$. Compare at matched realized A/C retention, B progress, and total state bytes.

**Prior-art floor (quick Hugging Face Papers lookup, not a priority claim).** [Adam][adam] defines the coupled $(m, v)$ ratio; [LAMB][lamb] and [NFNet adaptive gradient clipping][agc] already couple parameter/update norms with adaptive steps; [RMSNorm][rms] already factors scale out of representations. [Adafactor][adafactor], [Adam-mini][adammini], [8-bit optimizers][opt8], [FlashOptim][flashopt], and [adaptive log-space quantization][logq] already shrink or drop optimizer accumulators by factoring or quantizing state. [GEM][gem] and [Adam-NSCL][nscl] protect old tasks via update projection or null-space constraints. From the [idea ledger][ledger]: Noether/balancedness scalars fail under finite-step momentum and rebalancing, read-pinning fails when downstream consumers move, and first-order linearized drift claims are tautological. None of these makes assembling cancellation and scale recovery novel; the bet is a concrete contract where **live, non-null moment differences cancel on B's exact finite-step nonlinear update while a C-essential feature deletes a stored accumulator at matched A/C utility and storage**.

## A paper fixture: 1D obstruction, 2D symmetric cancellation, and radial-angular scale recovery

Use exact Adam-like dynamics with $\beta_1 = 1/2$, $\beta_2 = 1/2$, $\varepsilon = 0$:

```text
u(m, v; g) = ((m + g) / 2) / sqrt((v + g^2) / 2)
```

**1. 1D symmetric-proposal obstruction vs one-signed cancellation.** On a single coordinate read directly by B, suppose $\mathcal{D}_B$ contains both $+g_B$ and $-g_B$ ($g_B \neq 0$). Because the denominator $d(v, g) = \sqrt{(v + g^2)/2}$ is even in $g$, matching both $u(+g_B)$ and $u(-g_B)$ across $H_1, H_2$ forces $u(+g_B) - u(-g_B) = g_B / d(v, g_B)$ to agree, hence $v_1 = v_2$, and then $u(+g_B) + u(-g_B) = m / d(v, g_B)$ forces $m_1 = m_2$. Coordinate-wise action-without-moment restoration is therefore **algebraically impossible** for symmetric $\pm g_B$ proposals. If instead B is restricted to a one-signed proposal $g_B = +1$, take $H_1: (m_1, v_1) = (1, 1)$ and $H_2: (m_2, v_2) = (3, 7)$. Neither moment matches, yet:

```text
H1: u(+1) = ((1 + 1)/2) / sqrt((1 + 1)/2) = 1 / 1 = 1
H2: u(+1) = ((3 + 1)/2) / sqrt((7 + 1)/2) = 2 / 2 = 1
```

Both moments stay live on C's opposite direction $g_C = -1$ ($u_1(-1) = 0$ vs $u_2(-1) = 1/2$) and on coasting $g_C = 0$ ($1/\sqrt{2}$ vs $3/\sqrt{14}$). Crucially, after one $+1$ step the updated moments $(1, 1)$ and $(2, 4)$ **break cancellation on step 2** ($u_1'(+1) = 1$ vs $u_2'(+1) = 3/\sqrt{10} \approx 0.9487$), showing that single-step cancellation does not automatically survive B's own moment update.

**2. 2D cross-coordinate cancellation for symmetric $\pm g_B$.** Let B read $w^\top u = u^{(a)} + u^{(b)}$ with symmetric proposals $\mathcal{D}_B = \{(+1, +1), (-1, -1)\}$. Take $H_1: m=(0,0), v=(7,7)$ and $H_2: m=(3/2, -3), v=(7/2, 17)$. Neither coordinate is reader-null ($w=(1,1)$ reads both) and no moment matches, yet:

```text
At g = (+1, +1): H1 gives (1/4, 1/4) -> w^T u = +1/2; H2 gives (5/6, -1/3) -> w^T u = +1/2
At g = (-1, -1): H1 gives (-1/4, -1/4) -> w^T u = -1/2; H2 gives (1/6, -2/3) -> w^T u = -1/2
```

On the orthogonal C direction $g_C = (+1, -1)$, $w^\top u$ separates ($0$ vs $1/6$) and the orthogonal projection $(1, -1)^\top u$ separates sharply ($1/2$ vs $3/2$).

**3. Radial-angular scale recovery deleting a stored accumulator.** Suppose C requires a 2D feature $z \in \mathbb{R}^2$ whose orientation encodes the old C regime: $e_{H_1} = (3/5, 4/5)$ and $e_{H_2} = (4/5, -3/5)$ (orthogonal unit vectors), with C's honest calibration loss $\frac{1}{2}\|z - r e_{H_k}\|^2$ at current scale $r \in \{1/2, 3/4\}$. An independent old C reader computes $e_{H_k}^\top z$ (or classifies regime via $\text{sign}(z_2)$): ablating $z$ or replacing $z$ by a history-blind constant breaks C's old reader, proving $z$ is a live C job rather than a disguised norm copy. Recomputing $\nu = \|z\|_2 = r$ after each honest C update lets the separate scalar norm accumulator be deleted at zero extra bytes. **Honest tie check:** if $r$ is also publicly known as context $p$, a public reader computing $\nu(p) = r$ still ties on the scalar scale alone; deleting the accumulator only beats a public schedule when $r$ tracks an online C-regime statistic B does not independently receive, or when the freed bytes expand B's cancellation fiber—and it fails immediately if the C stream stops updating $z$ while $r$ shifts.

## Idea cards

### Cancel moment and scaling differences on B without restoring moments

#### 01. Paired $(m, v)$ ratio cancellation on a declared B proposal cone (P)
- **Mechanism:** Train C so reachable histories $(m_h, v_h)$ land on the exact level set where Adam's first-moment carry and second-moment denominator cancel along every proposal in a declared one-signed B cone $\mathcal{D}_B$, while the norm scale is rewritten separately.
- **Novelty vs nearest prior art:** Anchors [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) against [Adam][adam] moment normalization, PKR12 full hidden-state equivalence, `#246#07` reader-null $v$ absorption, and [GEM][gem], sharpening the domain to a signed proposal cone after the 1D symmetric-proposal obstruction.
- **Cheapest first test:** Two-coordinate rational Adam toy ($\beta_1=\beta_2=1/2$) with two positive B proposals and one negative/off-cone C proposal; compare PKR12 equivalence, `#246#07` null-space $v$ absorption, moment reset, GEM, and an undeclared $-g_B$ probe.
- **Old-task retention check:** Score frequent A and a withheld C batch pointing outside $\mathcal{D}_B$ before B, after B/clear, and on the next live C Adam step.

#### 02. Cross-coordinate denominator compensation for symmetric $\pm g_B$ proposals (P)
- **Mechanism:** Overcome the 1D $\pm g_B$ impossibility by pairing at least two B-read coordinates so an over-scaled adaptive step on one coordinate and an under-scaled step on the other cancel identically in B's declared readout $W_B u(\pm g_B)$ for both signs, without pushing either $m$ or $v$ into a reader-null subspace.
- **Novelty vs nearest prior art:** `#246#07` hides $v$ differences in $\ker(W_B)$ and [Adam-NSCL][nscl] projects updates into a null space; here both coordinates lie in the active row space of $W_B$ and cancel through coupled rational reciprocals $\sum_i w_i / d_i$ and $\sum_i w_i m_i / d_i$.
- **Cheapest first test:** Extend the 2D rational fixture above to C-driven updates reaching the two-equation symmetric manifold; compare `#246#07` null-space absorption, moment reset, GEM, and an out-of-span readout $w_\perp$ where cancellation must fail.
- **Old-task retention check:** Verify A outputs on $w_\perp$ and rare C gradient progress on orthogonal updates $(+1, -1)$ after B/clear across both histories.

#### 03. Two-step cancellation curves that survive B's own moment update (P)
- **Mechanism:** Because B's first step updates $m' = \beta_1 m + (1-\beta_1) g_B$ linearly and $v' = \beta_2 v + (1-\beta_2) g_B^2$ quadratically, single-step cancellation generally breaks on step 2 (as in the fixture). Train C onto the higher-codimension submanifold where both $u(m, v; g_B^{(1)})$ and the post-step $u(m', v'; g_B^{(2)})$ match across histories.
- **Novelty vs nearest prior art:** Goes beyond [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) single-boundary cancellation and `#248#06` (`m`-then-`v` sequencing across C batches) by making cancellation self-consistent across B's own multi-step edit script without inserting C repair steps between B steps.
- **Cheapest first test:** Two-step B script $(g_B^{(1)}, g_B^{(2)})$ in a 3-coordinate rational Adam toy; compare single-step cancellation (must fail step 2), PKR12 moment equivalence, moment reset, and a 3-step B script exceeding the certified depth.
- **Old-task retention check:** Run a withheld C update after the two-step B script and clear, checking A margins and C convergence speed against vanilla Adam.

#### 04. Exploit $\varepsilon$-anchored curvature to separate B-magnitude from C-magnitude (P)
- **Mechanism:** In Adam, the additive $\varepsilon$ breaks scale homogeneity between small and large gradients. Train C so $(m_h, v_h)$ differences cancel at B's declared proposal norm $\|g_B\|$ where $\sqrt{\beta_2 v + (1-\beta_2) g_B^2}$ dominates or balances $\varepsilon$, while intentionally diverging at C's distinct gradient magnitude $\|g_C\|$ along the same coordinate.
- **Novelty vs nearest prior art:** Standard [Adam][adam] treats $\varepsilon$ as numerical stability and [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) separates B from C by direction; this separates B from C by **gradient magnitude along a shared direction** using Adam's nonlinear denominator.
- **Cheapest first test:** 1D/2D exact rational toy with $\varepsilon = 1/4$, declared B norm $\|g_B\| = 2$, and C norm $\|g_C\| = 1/4$ on the same axis; compare $\varepsilon = 0$ ray scaling (must fail to separate magnitudes), moment reset, and an out-of-scale B proposal $\|g_B'\| = 1/2$.
- **Old-task retention check:** Measure C's actual learning progress on low-magnitude rare C batches before and after B/clear, ensuring $\varepsilon$-anchoring does not damp rare C into stagnation.

#### 05. Bias-correction clock mismatch as a cancellation lever (P)
- **Mechanism:** When reachable histories have different effective Adam step counts $t_1 \neq t_2$ (different bias-correction factors $1 - \beta_1^t$ and $\sqrt{1 - \beta_2^t}$), train C so the unnormalized $(m, v)$ difference cancels the bias-correction ratio difference on $\mathcal{D}_B$, avoiding both a clock reset and a moment reset.
- **Novelty vs nearest prior art:** Standard Adam bias-correction analysis (`#260`) treats mismatched step counts as an error to reset or synchronize; here mismatched clocks become a degree of freedom absorbed into the paired $(m, v)$ cancellation relation.
- **Cheapest first test:** Two histories at $t_1 = 1$ and $t_2 = 3$ with $\beta_1 = 1/2, \beta_2 = 3/4$ on a 2-coordinate toy; compare clock reset, full moment reset, PKR12 equivalence, and a proposal direction where clock-ratio cancellation fails.
- **Old-task retention check:** Continue C for 5 steps after B/clear from both clocks and verify A accuracy and C loss track the un-reset vanilla Adam trajectories.

#### 06. Couple AdamW weight decay with $(m, v)$ ratio cancellation (P)
- **Mechanism:** Under decoupled weight decay, the executed B update is $-\eta(\hat{m}/(\sqrt{\hat{v}}+\varepsilon) + \lambda w)$. Allow histories to differ in both weights $w$ and moments $(m, v)$, and train C so the weight-decay offset $\lambda \Delta w$ cancels the surviving adaptive-ratio residual on $\mathcal{D}_B$ without equating either $w$ or $(m, v)$.
- **Novelty vs nearest prior art:** Extends [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) from pure moment ratios to the full AdamW native step; unlike weight-matching or [GEM][gem], the weight gap itself pays down the moment-ratio gap on B's step.
- **Cheapest first test:** 2-coordinate rational AdamW toy ($\lambda = 1/4$) with histories differing in $w, m, v$ on a shared B coordinate; compare pure moment cancellation (breaks under $\lambda > 0$), weight-decay suspension during B, moment reset, and a $\lambda' \neq \lambda$ B schedule.
- **Old-task retention check:** Check that the permitted $\Delta w$ preserves A's decision margin and C's held-out loss at every served cut before and after B/clear.

#### 07. Exact algebraic test for when cancellation forces moment equality (I)
- **Mechanism:** Given B's declared proposal set $\mathcal{D}_B$ and readout matrix $W_B$, compute the rank/codimension of the nonlinear cancellation equations over $(m, v)$ before training C. Return a minimal subset of proposals from $\mathcal{D}_B$ that forces $(m_1, v_1) = (m_2, v_2)$ (generalizing the 1D $\pm g$ obstruction) so impossible parks are rejected up front.
- **Novelty vs nearest prior art:** A falsifier and feasibility gate rather than a new update rule; unlike empirical probing or linearized Jacobian checks (flagged as tautological in the [ledger][ledger]), it certifies exact nonlinear identifiability of $(m, v)$ from $\mathcal{D}_B$.
- **Cheapest first test:** Run symbolic/rational elimination on 1D $\pm g$, 2D rank-1 readout, and 2D full-rank readout with 2–4 proposals; verify the gate predicts exactly which settings admit nontrivial cancellation vs force PKR12 moment equality.
- **Old-task retention check:** On any rejected park, verify refusal leaves A and C running vanilla Adam untouched, with zero wasted C plasticity.

#### 08. Factored-preconditioner cancellation across shared row/column statistics (P)
- **Mechanism:** Under [Adafactor][adafactor] or [Adam-mini][adammini] block-shared second moments, one row factor $r_i$ or block scalar $v_b$ scales an entire slice of B proposals. Train C so a low-dimensional first-moment pattern cancels a shared factor gap across the whole slice simultaneously, instead of aligning each coordinate separately.
- **Novelty vs nearest prior art:** `#257#09` places Adafactor's rank-one $v$ gap in the reader's null space; here the shared factor acts *inside* B's active readout and is cancelled by a matched low-rank first-moment carry, saving degrees of freedom relative to per-coordinate cancellation.
- **Cheapest first test:** $2 \times 2$ weight matrix with row-factored $v$ and a 2-proposal B slice; compare `#257#09` null-space alignment, full-Adam per-coordinate cancellation, factor reset, and a B proposal that breaks the rank-one cancellation structure.
- **Old-task retention check:** Test A and rare C gradients that read both columns of the $2 \times 2$ block after B/clear, confirming the shared factor remains live and accurate for C.

### Recover scale from a C-essential job and delete the accumulator

#### 09. Delete a stored norm accumulator by recomputing scale from an independently read C feature (P)
- **Mechanism:** Under a fixed storage byte budget, delete one historical norm/clipping accumulator and recompute the required scale after each honest C update from a feature $z$ that C genuinely uses, with independent old-reader ablation required as part of the contract.
- **Novelty vs nearest prior art:** Anchors [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) against [RMSNorm][rms] (which factors scale without requiring an independently read C job), [8-bit/quantized optimizers][opt8], and PKR12 with the accumulator retained.
- **Cheapest first test:** Two reachable histories with identical current C scale and distinct deleted EMA accumulators; compare PKR12 keeping the accumulator, RMSNorm factoring without C use, a same-byte backup accumulator, a norm reset, and a stalled C stream.
- **Old-task retention check:** Ablate $z$ to confirm the independent old C reader fails; without ablation, verify A and rare C (including delayed C after clear) match vanilla C.

#### 10. Radial-angular split: history-dependent C job in orientation, history-invariant scale in radius (P)
- **Mechanism:** Resolve the collapse-to-constant trap of scalar scale recovery by storing C's genuine history-dependent job in the direction $z / \|z\|_2$ of a multi-coordinate feature $z \in \mathbb{R}^d$ ($d \ge 2$), while C's honest updates maintain $\|z\|_2$ as the recomputed park scale—so replacing $z$ with a public constant breaks C, yet $\|z\|_2$ leaks no private history.
- **Novelty vs nearest prior art:** [RMSNorm][rms] normalizes away $\|z\|_2$ and discards it, whereas [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) leaves open how $z$ can be simultaneously history-essential to C and history-invariant as a scale; the radial-angular split makes both hold simultaneously.
- **Cheapest first test:** Implement the 2D orthogonal-regime fixture ($e_{H_1}=(3/5,4/5)$, $e_{H_2}=(4/5,-3/5)$) under finite-step SGD/Adam with shifting $r$; compare a scalar feature (ties a public constant), a kept EMA accumulator, a public schedule when $r$ is hidden from B, and a C stream that rotates $z$ without maintaining $r$.
- **Old-task retention check:** Verify the old C regime classifier $\text{sign}(z_2)$ and regression $e_{H_k}^\top z$ stay intact across alternating $r$ values and post-B/clear, and break under constant substitution.

#### 11. Self-calibrating C loss geometry: let C's own curvature fix the recovered norm (P)
- **Mechanism:** Choose the feature parameterization so that minimizing C's **unmodified** task loss on honest C data has its unique stationary norm $\|z^*\|$ equal to the required park scale (e.g., via margin-calibrated logits or target-norm regression), so ordinary C steps restore the scale without any auxiliary norm-matching penalty.
- **Novelty vs nearest prior art:** Unlike [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) with an explicit factorization loss or [NFNet AGC][agc] tracking parameter norms passively, the scale is a fixed point of C's native objective, eliminating the dual-objective trade-off between C accuracy and norm accuracy.
- **Cheapest first test:** Compare an unmodified quadratic/margin C loss whose optimum sits at $\|z^*\| = r$ against auxiliary-penalty scale matching, a kept EMA accumulator, and a scale-invariant cross-entropy C loss (negative control where $\|z\|$ drifts unboundedly).
- **Old-task retention check:** Measure vanilla C convergence rate and held-out C loss alongside A retention to confirm zero regularization tax from scale maintenance.

#### 12. Dual-job redundant scale recovery against C sub-stream staleness (P)
- **Mechanism:** Directly counter the stalled-C failure mode by recovering the park scale from a symmetric invariant $\psi(z_1, z_2)$ of two features owned by **disjoint** C sub-streams (each verified by its own independent old reader), so when one C sub-stream goes idle, honest updates on the other keep the reconstructed scale fresh without keeping a fallback accumulator.
- **Novelty vs nearest prior art:** Extends [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) beyond single-stream fragility; unlike checkpoint/accumulator redundancy at equal bytes, both features perform distinct live C jobs and require zero dedicated backup storage.
- **Cheapest first test:** Two C sub-streams with independent arrival clocks where stream 1 pauses mid-episode while the operating scale shifts; compare single-feature recovery (must fail during pause), a kept backup accumulator at equal bytes, a norm reset, and both streams pausing simultaneously (negative control).
- **Old-task retention check:** Ablate $z_1$ and $z_2$ separately to prove independent old-reader use; verify A and both C sub-streams retain accuracy after pauses, resumptions, and B/clear.

#### 13. Reinvest deleted accumulator bytes into widening the B-safe cancellation fiber (P)
- **Mechanism:** Under a strict total state-byte budget, deleting one historical norm accumulator frees exact scalar slots; allocate those freed bytes to an extra C-essential coordinate that increases the dimension of the $(m, v)$ cancellation manifold (e.g., lifting a 1D obstructed coordinate to a 2D symmetric-cancellation pair).
- **Novelty vs nearest prior art:** [Adafactor][adafactor], [FlashOptim][flashopt], and [log-space quantization][logq] delete or compress optimizer bytes purely to save memory; here freed accumulator bytes buy **structural feasibility** (turning an algebraically impossible 1D symmetric park into a feasible 2D one) at equal total bytes.
- **Cheapest first test:** Equal-byte comparison: (a) 1D coordinate + 1 kept norm accumulator (obstructed on $\pm g_B$) vs (b) 2D C-essential radial-angular pair + deleted accumulator (admits symmetric $\pm g_B$ cancellation); include equal-byte 8-bit/quantized accumulator and moment-reset controls.
- **Old-task retention check:** Match total parameter+optimizer bytes exactly and score A, C, and rare C across both symmetric B edits and clear.

#### 14. Job-liveness witness: detect when C stops needing the scale-bearing feature (I)
- **Mechanism:** Track a lightweight gradient-sensitivity witness on C's actual online updates (e.g., whether C's loss gradient along $z$ remains nonzero over a sliding window). If C's workload shifts or another unit absorbs C's job, $z$ degenerates into an unmaintained shadow copy; revoke the deletion licence and refuse B before stale scales silently corrupt B.
- **Novelty vs nearest prior art:** An audit and runtime falsifier for [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p)'s core assumption ("C genuinely maintains $z$"), distinct from storing a shadow accumulator because it emits only a liveness veto rather than a fallback scale.
- **Cheapest first test:** Construct a stream where C's dependency migrates from $z$ to a sibling unit mid-run while scale drifts; compare unguarded job recovery (silent B corruption), a kept accumulator, a fixed staleness timeout, and a false-positive test where C is temporarily converged at the true scale.
- **Old-task retention check:** Verify A and C continue uninterrupted after liveness revocation, and charge every revoked B offer to availability.

#### 15. Cross-layer scale synthesis from two low-norm C features without a layer-wide accumulator (P)
- **Mechanism:** Recompute a layer's adaptive clipping or [LAMB][lamb]-style trust-ratio scale from a bilinear invariant $z_1^\top M z_2$ of two features read by different old C heads across adjacent blocks, deleting the layer-wide running-norm accumulator without forcing any single feature to carry a large or rigid norm.
- **Novelty vs nearest prior art:** [LAMB][lamb] and [NFNet AGC][agc] compute layer norms directly from full parameter tensors or cached accumulators; this synthesizes the layer scale from two small C-essential bottleneck features whose individual norms can vary freely as long as their bilinear pairing tracks the regime.
- **Cheapest first test:** Two-block linear/ReLU toy with a layer-wide trust ratio; compare kept layer EMA, [RMSNorm][rms] per-layer norm, equal-byte backup scalar, and an adversarial C update that shifts $z_1$ and $z_2$ in opposite directions breaking $z_1^\top M z_2$.
- **Old-task retention check:** Ablate $z_1$ and $z_2$ independently on their respective old C heads; score A and both C heads after two arrivals and B/clear.

### Effect-restoring parks: couple moment cancellation with job-recovered scale

#### 16. Mutual cancellation between history-dependent job-recovered scale and live Adam moments (P)
- **Mechanism:** Relax the requirement that the job-recovered scale $\phi(z(h))$ be history-invariant on its own. Let both $\phi(z(h))$ and $(m_h, v_h)$ vary with history $h$ to serve C freely, and train C so their **product** $\phi(z(h)) \cdot u(m_h, v_h; g_B)$ is identical across reachable histories on $\mathcal{D}_B$—restoring the executed B effect while neither the scale nor the moments are restored.
- **Novelty vs nearest prior art:** Strictly generalizes both [parent #02](norm-restoring-parks.md#02-restore-an-action-without-restoring-the-moments-p) (which keeps norm scale public/separate) and [parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p) (which makes $\phi(z)$ history-invariant); no public schedule $\nu(p)$ can reproduce a history-dependent $\phi(z(h))$ that cancels a private $(m_h, v_h)$ mismatch, creating a genuine interaction that stacked separate controls cannot tie by construction.
- **Cheapest first test:** 1D/2D rational Adam toy where $H_1, H_2$ have different $u(m_h, v_h; g_B)$ ratios (e.g., $1$ vs $2/3$) and different C-essential feature norms $\phi(z(H_1)) = 1/2$, $\phi(z(H_2)) = 3/4$ whose product equals $1/2$ on $\mathcal{D}_B$; compare stacked `#261#02` + `#261#11` separately, any legal public schedule $\nu(p)$, moment reset, and an undeclared B direction where the product does not cancel.
- **Old-task retention check:** Verify old C readers genuinely depend on the distinct $\phi(z(H_1)) \neq \phi(z(H_2))$ values and distinct moments on off-span C steps, and score A/C after B/clear.

#### 17. One C-essential feature drives both the recomputed norm and the Adam preconditioner alignment (P)
- **Mechanism:** Couple the parameter block holding C's scale-bearing feature $z$ directly into the adaptive denominator $v$ on B's coordinates during ordinary C updates, so the exact same honest C gradient that maintains $\|z\|$ also moves $v$ onto B's cancellation curve—eliminating separate alignment and scale-maintenance mechanisms.
- **Novelty vs nearest prior art:** Unlike [parent #01](norm-restoring-parks.md#01-one-c-gradient-pays-two-debts-p) (which keeps full moment restoration and a stored producer) or `#238#18` (productive batch paying a clipping deficit), this binds accumulator deletion directly to $(m, v)$ ratio cancellation via one shared C-essential parameter block.
- **Cheapest first test:** Minimal coupled 2-block rational toy comparing joint $z$-driven $v$ alignment against separate `#261#02` + `#261#11` stacked, kept accumulator + moment reset, and a C batch that updates $z$ in the right norm direction but pushes $v$ off the cancellation curve.
- **Old-task retention check:** Ablate $z$ to confirm independent C use, then score A and withheld rare C across alternating arrivals and B/clear.

#### 18. Effect-equivalent clipping across distinct pre-clip norms and live moments (P)
- **Mechanism:** When B's native update passes through norm clipping with threshold $\tau = \phi(z)$, allow histories to enter with different unclipped Adam vectors $u_1 \neq u_2$ (different norms and different $(m, v)$) so long as clipping by $\phi(z)$ maps them onto the **same** executed post-clip update $\min(1, \phi(z)/\|u_h\|) u_h$ on $\mathcal{D}_B$.
- **Novelty vs nearest prior art:** [PR #261](https://github.com/manojbajaj95/cl/pull/261) warns that matching clip predicates alone fails when executed updates differ; this turns clipping into an **active effect-collapsing map** where different pre-clip magnitudes collapse to one post-clip direction and length, strictly weaker than matching pre-clip updates.
- **Cheapest first test:** 2D rational toy where $H_1$ and $H_2$ produce collinear unclipped Adam updates of lengths $2$ and $3$ on $\mathcal{D}_B$ and both clip to length $\phi(z) = 1$; compare pre-clip action matching (`#261#02`), fixed clip threshold, moment reset, and a smaller B proposal that falls inside the unclipped ball (breaking collapse).
- **Old-task retention check:** Verify C's own updates remain unclipped (or preserve distinct live magnitudes) and check A and rare C before and after B/clear.

#### 19. Transfer a deleted accumulator's role across C regime switches via feature handoff (P)
- **Mechanism:** When C shifts from old task $C_1$ to $C_2$ and $C_1$'s feature $z_1$ goes dormant, hand the scale-recovery role from $z_1$ to $C_2$'s active feature $z_2$ during an overlap window using a smooth public blend, while keeping the composed B effect $\phi_{\text{blend}}(z_1, z_2) \cdot u(m, v; g_B)$ invariant across every intermediate cut of the handoff.
- **Novelty vs nearest prior art:** Combines accumulator deletion ([parent #11](norm-restoring-parks.md#11-recover-scale-from-a-retained-job-not-a-retained-copy-p)) with regime-switching continuity without ever re-allocating a historical accumulator; differs from `#245#14` tail handoff because what transfers is the **scale-production duty** across C jobs, not a fading residual.
- **Cheapest first test:** Three-phase stream ($C_1$ active $\to$ overlap $\to$ $C_2$ active, $C_1$ idle) with a mid-handoff B edit; compare keeping a persistent accumulator, freezing $\phi(z_1)$ (goes stale), hard-switching without overlap, and a B edit landing at the worst intermediate blend weight.
- **Old-task retention check:** Verify $C_1$'s old reader still passes on $z_1$ after $C_1$ goes idle, $C_2$'s reader depends on $z_2$, and A holds through every cut.

#### 20. Non-public context scale: when job-recovered scale strictly beats every legal public schedule (I)
- **Mechanism:** Directly resolve the tie in [PR #261](https://github.com/manojbajaj95/cl/pull/261)'s paper fixture by defining a benchmark regime where the required B step scale $r$ tracks an online C-regime signal (e.g., current C feature SNR or domain amplitude) that B's public context $p$ does not carry. Prove that any history-blind public schedule $\nu(p)$ incurs irreducible B error while job-recovered $\phi(z)$ achieves zero error at zero extra accumulator bytes.
- **Novelty vs nearest prior art:** An identifiability control, not a new optimizer; it pins down the exact information boundary separating a real accumulator-deletion primitive from a disguised public schedule.
- **Cheapest first test:** Extend the radial-angular fixture with latent $r \in \{1/2, 3/4\}$ observed only in C's honest batches (not in $p$); compare optimal public constant/schedule $\nu(p)$, kept EMA accumulator (costs extra bytes), and radial-angular $\phi(z) = \|z\|_2$.
- **Old-task retention check:** Score A and both C regimes across unseen $r$ shifts, confirming $z$'s orientation still serves C and the win disappears as expected if $r$ is leaked into $p$.

#### 21. Measure the C-plasticity tax of effect-only vs moment-restoring parks (I)
- **Mechanism:** Quantify the exact learning-speed and rare-C retention advantage gained by constraining C only to the lower-codimension effect-cancellation manifold (`#02` + `#16`) rather than full hidden-state equivalence (PKR12) or reader-null $v$ absorption (`#246#07`), at matched B action error and matched total state bytes.
- **Novelty vs nearest prior art:** A comparative falsifier; per the [idea ledger][ledger] (plasticity-reserve kills PR #9/#21), any claim that a looser constraint saves real C plasticity must first pass a variance/spread gate showing the gap between PKR12 and effect-only renewal exceeds seed noise.
- **Cheapest first test:** Small CPU linear/2-layer MLP continual stream with Adam, 5 seeds, sweeping B proposal dimension $k \in \{1, 2, 4\}$; compare PKR12 equivalence, `#246#07` null-space $v$, moment reset, GEM, and effect-restoring cancellation on C steps-to-target and rare-C loss.
- **Old-task retention check:** Gate every arm on identical A retention floor and exact B edit accuracy before comparing C plasticity; retire the line if PKR12 or `#246#07` ties within seed CI.

#### 22. Adversarial B-direction probe to separate true cancellation from accidental null-space hiding (I)
- **Mechanism:** Pair every claimed effect-restoring park with three mandatory adversarial probes: (i) an out-of-span or sign-flipped B proposal $-g_B$, (ii) a stalled-C window where $z$ stops receiving updates while scale shifts, and (iii) an independent C-reader ablation of $z$. Require live $(m, v)$ divergence on probe (i), scale degradation on probe (ii), and C failure on probe (iii)—ruling out secret null-space hiding, secret moment resets, and disguised backup accumulators.
- **Novelty vs nearest prior art:** Operationalizes the exact negative controls from [flood triage row 376][triage] into a reusable verification suite; mirrors the ledger's anti-tautology standard (read-pinning kill, PR #117) by checking executed downstream updates rather than intermediate norms.
- **Cheapest first test:** Run all three probes on the 2D rational fixture plus two cheater baselines (a `#246#07` null-space hider and a shadow-accumulator baseline); verify the probe suite passes only true effect-restoring parks and catches both cheaters.
- **Old-task retention check:** Ensure the probes themselves are read-only evaluations (no uncharged state writes) and confirm A and rare C remain unchanged after auditing.

## Ranked deeper questions

1. **Does mutual scale–moment cancellation (#16) strictly beat stacking moment cancellation (#01/#02) and accumulator deletion (#09/#10) separately?** Test in a tiny Adam toy where B's public context $p$ does not carry the C-regime scale (#20): check whether letting $\phi(z(h))$ stay history-dependent to cancel live $(m_h, v_h)$ gaps achieves strictly lower C-plasticity tax (#21) or fewer bytes (#13) at matched B accuracy and A/C retention. If the stacked separate controls tie, effect-restoring parks collapse to two independent tricks.
2. **When does multi-step B survival (#03) collapse the cancellation manifold back to moment equality (#07)?** Our fixture shows 1D symmetric $\pm g_B$ forces $m_1=m_2, v_1=v_2$ immediately, and single-step cancellation breaks on step 2. Find the exact trade-off between coordinate width $d$, B script length $L$, and proposal symmetry: how many extra coordinates (or freed accumulator bytes, #13) are needed per additional B step before the codimension leaves no room for live C moments?
3. **Can a C-essential feature maintain an accurate recomputed scale without a regularization tax (#10/#11) and without silently going stale (#12/#14)?** Test whether self-calibrating C loss geometry and dual-job recovery keep B's scale error zero across C sub-stream pauses and regime switches (#19) while passing the independent-reader ablation (#22), beating a kept quantized accumulator ([8-bit][opt8]/[log-space][logq]) at equal bytes.
4. **How much real C plasticity is actually saved by effect-only renewal over PKR12 and `#246#07` once A retention and B accuracy are matched (#21)?** Following the ledger's variance-gate rule, measure the C-plasticity spread across PKR12, `#246#07`, moment reset, and effect-only cancellation on a small CPU Adam stream before scaling; if the spread is within seed noise or `#246#07` ties, stop before any larger model.

**Verdict: ambitious and falsifiable on paper or CPU; no pilot result.** The core testable claim is sharper than [PR #261](https://github.com/manojbajaj95/cl/pull/261): **live, non-null Adam $(m, v)$ differences and a C-essential feature $z$ can jointly restore B's executed update while deleting a stored norm accumulator—beating PKR12, `#246#07` null-space absorption, moment/norm resets, equal-byte backup accumulators, and any legal public schedule $\nu(p)$ at matched A/C utility and storage.** One-step ties on a public scalar, hidden null-space copies, and stalled-C failures do not pass; if mutual cancellation (#16) and non-public scale recovery (#20) cannot beat the stacked controls on the first CPU toy, stop before scaling.

[ledger]: https://github.com/manojbajaj95/cl/blob/e2f8492f23542c996cb07d7c739c0e0d2a68f361/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/e2f8492f23542c996cb07d7c739c0e0d2a68f361/reviews/flood-triage.md#L376
[adam]: https://huggingface.co/papers/1412.6980
[gem]: https://huggingface.co/papers/1706.08840
[adafactor]: https://huggingface.co/papers/1804.04235
[lamb]: https://huggingface.co/papers/1904.00962
[rms]: https://huggingface.co/papers/1910.07467
[agc]: https://huggingface.co/papers/2102.06171
[nscl]: https://huggingface.co/papers/2103.07113
[opt8]: https://huggingface.co/papers/2110.02861
[adammini]: https://huggingface.co/papers/2406.16793
[flashopt]: https://huggingface.co/papers/2602.23349
[logq]: https://huggingface.co/papers/2608.22322
