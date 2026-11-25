# Step-count levers: mismatched Adam clocks and radial–angular scale recovery

**Status:** Ideas only; three exact rational paper fixtures, no pilots or GPU work. **Parent:** [Effect-restoring parks](effect-restoring-parks.md) ([PR #274](https://github.com/manojbajaj95/cl/pull/274)). **Seed:** score-3 [flood triage, row 391][triage]: [parent #05](effect-restoring-parks.md#05-bias-correction-clock-mismatch-as-a-cancellation-lever-p) (when reachable histories have different effective Adam step counts, train C so the raw $(m, v)$ difference cancels against the bias-correction mismatch along B's declared directions instead of resetting or synchronizing the clocks) and [parent #10](effect-restoring-parks.md#10-radial-angular-split-history-dependent-c-job-in-orientation-history-invariant-scale-in-radius-p) (store C's history-dependent job in the direction of a multi-coordinate feature and the history-invariant scale in its norm, so honest C updates recompute the norm without collapsing the job to a constant). **Ledger read first:** [Idea ledger][ledger]. **P** marks a candidate reusable primitive, not established novelty; **I** marks a method, comparison, or falsifier.

## The bet and what would count

An effect-restoring park ([PR #274](https://github.com/manojbajaj95/cl/pull/274)) showed that under matched Adam clocks ($t_1 = t_2$), matching symmetric $\pm g_B$ proposals on a single coordinate algebraically forces $m_1 = m_2$ and $v_1 = v_2$, while scalar scale recovery risks collapsing a C feature to a public constant. This node tests two sharper levers—and their interaction:

- **Use mismatched bias-correction clocks as an active cancellation lever.** When reachable histories arrive with different effective Adam step counts $t_1 \neq t_2$, Adam's bias-correction ratio $\gamma(t') = \sqrt{1-\beta_2^{t'}} / (1-\beta_1^{t'})$ differs across histories at B's execution step $t' = t + 1$. Instead of resetting or synchronizing clocks, train C so raw $(m, v)$ differences cancel against $\gamma(t_1') \neq \gamma(t_2')$ along B's declared proposal directions $\mathcal{D}_B$. Crucially, this breaks the 1D symmetric-proposal $v$-obstruction from [PR #274](https://github.com/manojbajaj95/cl/pull/274), yet obeys two hard laws: a **sign-match obstruction** (cancellation fails when clock mismatch pushes the same way as the $v$-gap) and **asymptotic exhaustion** ($\gamma(t') \to 1$ as $t' \to \infty$).
- **Split C's job into direction and history-free scale into length.** Encode C's history-dependent task strictly in the unit direction $\hat{z} = z / \|z\|_2 \in S^{d-1}$ ($d \ge 2$) of a multi-coordinate feature $z \in \mathbb{R}^d$ while honest C updates maintain $\|z\|_2 = r$ as the history-invariant park scale—passing independent old-reader ablation of $\hat{z}$ without collapsing $z$ to a constant. This faces two structural failure modes: **Pythagorean radial drift** under finite-step tangential updates ($\|z - \eta g_\perp\|_2 > \|z\|_2$) and **radius-needing C jobs** where C's old reader depends on amplitude $\|z\|_2$.
- **Couple the two when both fail individually, and beat every stacked control.** When C's job genuinely requires a history-dependent radius $r(H_1) \neq r(H_2)$ *and* the clock mismatch pushes the same way as the moment gap, neither lever works alone—yet their product $\|z(h)\|_2 \cdot u(m_h, v_h, t_h'; g_B)$ can still cancel identically on symmetric $\pm g_B$. Every claim must beat the full stacked control at matched A/B/C retention and total state bytes: `#261#02` cancellation with matched clocks, a step-count reset, `#260` clock windows ([PR #260](https://github.com/manojbajaj95/cl/pull/260)), [GEM][gem]/[Adam-NSCL][nscl], a pair of clocks whose mismatch pushes the same way as the moment gap, `#261#11` scalar scale recovery, [RMSNorm][rms] discarding the norm, a backup accumulator of equal bytes, and a C stream whose job needs the radius.

**Prior-art floor (quick Hugging Face Papers lookup, not a priority claim).** [Adam][adam] introduces $1-\beta_1^t$ and $1-\beta_2^t$ bias correction; [RAdam][radam] rectifies early-step variance and [AdamD][adamd] modifies bias-correction factors globally—none uses mismatched per-history step counts as a cancellation lever across continual histories. [Weight Normalization][weightnorm], [magnitude-direction decoupling][magdir], [Decoupled Orthogonal Dynamics][dod], and [nGPT][ngpt] separate weight/feature length from direction; [RMSNorm][rms] discards the norm; [AdamP][adamp] projects out radial components to stop Pythagorean norm growth on scale-invariant weights. [Adafactor][adafactor], [8-bit optimizers][opt8], and [log-space quantization][logq] compress optimizer state without overloading a C-essential feature; [GEM][gem] and [Adam-NSCL][nscl] project updates for retention. From the [idea ledger][ledger]: Noether/balancedness scalars fail under finite-step momentum, read-pinning fails when downstream consumers move, first-order drift formulas are tautological, and any plasticity-savings claim must clear a seed-variance gate. The novel bet here is **finite-step nonlinear cancellation between live mismatched Adam clocks, raw moments, and direction-vs-radius feature geometry under an explicit old-task retention and byte budget**.

## A paper fixture: 1D mismatched-clock symmetric cancellation, Pythagorean radial drift, and coupled clock-radius cancellation

Use exact Adam dynamics with $\beta_1 = 1/2$, $\beta_2 = 1/2$, $\varepsilon = 0$. At B's execution step $t' = t + 1$ with pre-step raw moments $(m, v)$ and gradient $g$, $c_1(t') = c_2(t') = 1 - (1/2)^{t'}$, $\gamma(t') = \sqrt{c_2(t')}/c_1(t') = 1/\sqrt{1 - (1/2)^{t'}}$, and:

```text
u(m, v, t'; g) = ((m + g) / (2 * c1(t'))) / sqrt((v + g^2) / (2 * c2(t')))
               = gamma(t') * ((m + g) / 2) / sqrt((v + g^2) / 2)
```

**1. 1D symmetric $\pm g_B$ breaks the $v$-obstruction under mismatched clocks (while keeping the $m$-obstruction and a Cauchy–Schwarz floor).** With matched clocks ([PR #274](https://github.com/manojbajaj95/cl/pull/274)), matching $u(\pm g_B)$ in 1D forces $v_1 = v_2$ and $m_1 = m_2$. With mismatched clocks $t_1 = 2 \to t_1' = 3$ ($\gamma(3) = \sqrt{8/7}$) and $t_2 = 3 \to t_2' = 4$ ($\gamma(4) = \sqrt{16/15}$), take two trajectories genuinely reachable from $(0, 0)$:
- $H_1$: 2 real C steps $(4, -2) \implies (m_1, v_1) = (0, 6)$ at $t_1' = 3$ ($c_1 = c_2 = 7/8$).
- $H_2$: 3 real C steps from $(0, 0)$ reaching $(m_2, v_2) = (0, 83/15)$ at $t_2' = 4$ ($c_1 = c_2 = 15/16$).

Neither $v$ nor $t'$ matches, yet on symmetric $\mathcal{D}_B = \{+1, -1\}$:

```text
At g = +1: H1 gives m_hat = 4/7,  v_hat = 4        (sqrt = 2)     -> u = +2/7
           H2 gives m_hat = 8/15, v_hat = 784/225  (sqrt = 28/15) -> u = +2/7
At g = -1: H1 gives u = -2/7; H2 gives u = -2/7
```

Off-magnitude C gradients still separate ($g_C = +2$ gives $0.4781$ vs $0.4731$), and on step 2 ($g_B = +1$ again, clocks tick to $t_1'' = 4, t_2'' = 5$) cancellation breaks ($0.5164$ vs $0.5217$). Three exact obstructions remain:
- **Sign-match obstruction:** Because $\gamma(3) > \gamma(4)$, matching $u(\pm 1)$ requires $v_1 > v_2$; if $v_2 > v_1$, the clock mismatch pushes the same way as the $v$-gap and cancellation is impossible.
- **$m$-obstruction & Cauchy–Schwarz floor:** In 1D symmetric $\pm g_B$, $(u(+g)+u(-g))/(u(+g)-u(-g)) = \beta_1 m / ((1-\beta_1)g)$ still forces $m_1 = m_2$. For nonzero $m$, real Adam trajectories from $(0, 0)$ obey $v_t \ge m_t^2 / c_1(t)$: e.g., $H_1$ from 1 step $g = 1$ gives $(m_1, v_1) = (1/2, 1/2)$ at $t_1' = 2$, which requires $v_2 = 2/7$ at $t_2' = 3$, below the 2-step reachability floor $v_2 \ge (1/2)^2 / (3/4) = 1/3$.
- **U-shaped $\gamma(t')$ with $\beta_1 \neq \beta_2$:** When $\beta_1 = 1/2, \beta_2 = 3/4$, $\gamma(t')$ is non-monotone: $\gamma(1) = 1 > \gamma(2) = \sqrt{7}/3 > \gamma(3) = \sqrt{37}/7 \approx 0.8690 < \gamma(4) = \sqrt{7}/3 < \gamma(5) \approx 0.9015 \to 1$. Falling-branch pairs ($t' \le 3$) and rising-branch pairs ($t' \ge 3$) cancel **opposite** signs of $v_1 - v_2$, while $(2, 4)$ has exact zero clock leverage ($\gamma(2) = \gamma(4)$).

**2. Radial–angular Pythagorean drift under scale-invariant C loss.** Start at $z_0 = (3/5, 4/5)$ ($\|z_0\|_2 = 1$). Under a direction-only C loss $L_C(\hat{z})$, the gradient is purely tangential, e.g., $g_\perp = (-4/5, 3/5)$ ($z_0^\top g_\perp = 0$). One unmodified GD step with $\eta = 3/4$ gives $z_1 = (6/5, 7/20)$ with exact norm $\|z_1\|_2 = \sqrt{1 + (3/4)^2} = 5/4 > 1$. Thus honest direction-only C updates strictly inflate $\|z\|_2$ unless paired with finite-step radial damping, while a C job that genuinely reads amplitude $e_h^\top z$ breaks if $\|z\|_2$ is forced history-invariant.

**3. Coupled clock–radius cancellation when both individual levers fail.** Keep $\beta_1 = \beta_2 = 1/2, \varepsilon = 0$, $\mathcal{D}_B = \{+1, -1\}$, and take two trajectories reachable from $(0, 0)$:
- $H_1$: 2 real C steps $(4, -2) \implies (m_1, v_1) = (0, 6)$ at $t_1' = 3 \implies u_1(\pm 1) = \pm 2/7$.
- $H_2$: 3 real C steps $(-4, 4, -1) \implies (m_2, v_2) = (0, 13/2)$ at $t_2' = 4 \implies u_2(\pm 1) = \pm 4/15$.

Here $v_2 = 13/2 > v_1 = 6$ while $\gamma(4) < \gamma(3)$, so the clock mismatch pushes the **same** way as the $v$-gap and **parent #05 alone fails**. Meanwhile, suppose C's old reader genuinely needs distinct history-dependent radii $r(H_1) = \|z(H_1)\|_2 = 14/15$ (along $(3/5, 4/5)$) and $r(H_2) = \|z(H_2)\|_2 = 1$ (along $(4/5, -3/5)$), so **parent #10 alone also fails**. Yet their coupled executed B update cancels identically on both signs:

```text
H1: ||z(H1)||_2 * u1(+-1) = (14/15) * (+-2/7) = +-4/15
H2: ||z(H2)||_2 * u2(+-1) =   1     * (+-4/15) = +-4/15
```

Neither parent lever alone, nor any public schedule $\nu(p)$, can reproduce this cancellation.

## Idea cards

### Mismatched Adam step-count clocks as a cancellation lever

#### 01. Break the 1D symmetric $\pm g_B$ $v$-obstruction using mismatched bias-correction clocks (P)
- **Mechanism:** Anchor [parent #05](effect-restoring-parks.md#05-bias-correction-clock-mismatch-as-a-cancellation-lever-p) on the exact 1D algebraic separation: when reachable histories arrive at different effective Adam step counts $t_1 \neq t_2$ with $\gamma(t_1') \neq \gamma(t_2')$, train C so the raw $v$ gap cancels $\gamma(t_1')/\gamma(t_2')$ along symmetric $\pm g_B$ proposals (with $m_1 = m_2$) without resetting or synchronizing the clocks.
- **Novelty vs nearest prior art:** [Adam][adam], [RAdam][radam], and [AdamD][adamd] treat bias correction as a global variance fix, `#261#02` with matched clocks is algebraically obstructed on 1D $\pm g_B$, and `#260` treats clock windows as timing constraints; here the clock mismatch itself supplies the exact degree of freedom that unlocks 1D symmetric $v$-cancellation.
- **Cheapest first test:** Implement Fixture 1 ($t_1'=3, t_2'=4$, $\beta_1=\beta_2=1/2$, $\mathcal{D}_B=\{\pm 1\}$) with real C trajectories from $(0,0)$; compare `#261#02` matched-clock cancellation (must fail or force $v_1=v_2$), step-count reset, `#260` clock windows, [GEM][gem], and a same-direction clock/moment pair ($v_2 > v_1$).
- **Old-task retention check:** Continue C for 5 live Adam steps from both clocks after B/clear on off-magnitude $g_C = 2$ and verify A accuracy and C loss track un-reset vanilla Adam.

#### 02. U-shaped $\gamma(t')$ branch selection for sign-selectable clock cancellation (P)
- **Mechanism:** When $\beta_2 > \beta_1$ (including standard $\beta_1 = 0.9, \beta_2 = 0.999$ and rational $\beta_1 = 1/2, \beta_2 = 3/4$), $\gamma(t') = \sqrt{1-\beta_2^{t'}} / (1-\beta_1^{t'})$ is U-shaped with a unique minimum $t^*$. Schedule C's arrival onto the falling branch ($t' < t^*$) when older histories carry smaller $v$ and onto the rising branch ($t' > t^*$) when older histories carry larger $v$, turning a single Adam hyperparameter pair into a sign-selectable lever.
- **Novelty vs nearest prior art:** Standard Adam bias-correction analyses ([RAdam][radam], [AdamD][adamd]) ignore the sign reversal of $\Delta \gamma(t')$ across $t^*$; unlike a monotone $\beta_1 = \beta_2$ clock that can only cancel one sign of $v_1 - v_2$, branch selection overcomes the fixed-sign obstruction without changing optimizer code.
- **Cheapest first test:** Rational $\beta_1 = 1/2, \beta_2 = 3/4$ toy ($t^* = 3$) comparing falling pair $(t_1'=2, t_2'=3)$ against rising pair $(t_1'=3, t_2'=5)$ and the exact zero-leverage trap $(t_1'=2, t_2'=4)$ where $\gamma(2) = \gamma(4) = \sqrt{7}/3$; include step-count reset and matched-clock `#261#02` controls.
- **Old-task retention check:** Score A and withheld C across both branches after B/clear, checking that waiting for the rising branch does not starve C plasticity compared with vanilla Adam.

#### 03. Cross-coordinate asymmetric clock splits for full 2D $(m, v)$ symmetric cancellation (P)
- **Mechanism:** Overcome the 1D $m_1 = m_2$ obstruction by pairing two B-read coordinates whose per-block effective Adam step counts $(t_a, t_b)$ differ across histories (because C updates block $a$ and block $b$ at different frequencies). Train C so the per-coordinate $\gamma(t_a'), \gamma(t_b')$ offsets cancel *both* $m_1 \neq m_2$ and $v_1 \neq v_2$ in B's readout $w^\top u(\pm g_B)$ with less C gradient distortion than matched-clock 2D cancellation.
- **Novelty vs nearest prior art:** Extends [PR #274 #02](effect-restoring-parks.md#02-cross-coordinate-denominator-compensation-for-symmetric-pm-g_b-proposals-p) (which requires matched clocks and larger moment distortion) and [Adam-NSCL][nscl] (null-space projection) by harnessing natural sparse-update clock skew across active B-read blocks.
- **Cheapest first test:** 2D readout $w = (1, 1)$, $\mathcal{D}_B = \{\pm(1, 1)\}$, sparse C updates creating $(t_a, t_b) = (2, 4)$ vs $(4, 2)$; compare matched-clock `#274#02`, global step-count reset, `#260` clock windows, [GEM][gem], and an out-of-span readout $w_\perp = (1, -1)$.
- **Old-task retention check:** Verify A margins on $w_\perp$ and rare C progress on orthogonal updates $(+1, -1)$ after B/clear from both clock patterns.

#### 04. Two-step clock-tracking curves that survive bias-correction ticking across B's script (P)
- **Mechanism:** Because B's step 1 increments both clocks ($t_1' \to t_1'+1, t_2' \to t_2'+1$), $\gamma(t_1'+1)/\gamma(t_2'+1)$ contracts toward $1$ while $v_1, v_2$ contract toward $g_B^2$ at rate $\beta_2$. Train C onto the submanifold where the second-moment contraction tracks the clock-ratio contraction across a 2-step B script $(g_B^{(1)}, g_B^{(2)})$, avoiding step-2 divergence.
- **Novelty vs nearest prior art:** Goes beyond [parent #05](effect-restoring-parks.md#05-bias-correction-clock-mismatch-as-a-cancellation-lever-p) (single-step clock cancellation, which breaks on step 2 in Fixture 1) and `#274#03` (matched-clock two-step curves) by coupling two distinct exponential decay clocks ($\beta_1^t, \beta_2^t$ vs $\beta_2 v$).
- **Cheapest first test:** 2-coordinate toy with a 2-step B script $(+1, +1)$ from clocks $(t_1'=3, t_2'=4)$; compare single-step clock cancellation (must fail step 2), matched-clock `#274#03`, step-count reset, and a 3-step B script exceeding certified depth.
- **Old-task retention check:** Run a withheld C batch after the 2-step B script and clear, verifying A accuracy and C convergence match vanilla Adam.

#### 05. Staggered partial clock refresh to renew the transient bias-correction lever (P)
- **Mechanism:** Because $\gamma(t') \to 1$ exponentially as $t' \to \infty$, any global clock lever expires on long streams. During a lawful C regime boundary, refresh the step counter (and only that counter, or a small auxiliary block's counter) on a rotating subset of coordinates while keeping the main block's clock running, replenishing $|\gamma(t_1')/\gamma(t_2') - 1|$ without a destructive global optimizer reset.
- **Novelty vs nearest prior art:** Warm-restart optimizers reset all moments or learning rates globally; `#260` clock windows accept fixed expiry. Staggered partial refresh treats bias-correction leverage as a renewable local resource bounded by explicit A/C retention gates.
- **Cheapest first test:** 50-step continual C stream ($t \gg 1/(1-\beta_2)$) where unrefreshed clock cancellation collapses to matched-clock `#261#02`; compare staggered 1-block clock refresh, global step-count reset, matched-clock `#261#02`, and unrefreshed `#274#05` (negative control).
- **Old-task retention check:** Check that refreshing the auxiliary block's step count never spikes A loss or rare C gradients on the first 3 post-refresh steps.

#### 06. Exploit $\varepsilon$-broken homogeneity to separate $c_1(t')$ from $c_2(t')$ by gradient magnitude (P)
- **Mechanism:** With $\varepsilon > 0$, Adam's denominator is $\sqrt{v'/c_2(t')} + \varepsilon$, so $c_2(t')$ does not factor out cleanly against $c_1(t')$. Train C so mismatched clocks cancel at B's declared proposal norm $\|g_B\|$ where $\sqrt{\hat{v}'}$ and $\varepsilon$ balance, while small-norm C gradients ($\|g_C\| \ll \varepsilon$) experience pure $1/c_1(t')$ scaling and stay history-responsive.
- **Novelty vs nearest prior art:** Extends `#274#04` ($\varepsilon$-anchored magnitude separation under matched clocks) to mismatched clocks, exploiting the asymmetry between $c_1(t')$ (multiplicative outside $\varepsilon$) and $c_2(t')$ (nested inside the square root).
- **Cheapest first test:** 1D/2D rational toy with $\varepsilon = 1/2$, $t_1'=2, t_2'=4$, $\|g_B\| = 2$, $\|g_C\| = 1/8$; compare $\varepsilon = 0$ clock cancellation (must fail magnitude separation), matched-clock `#274#04`, step-count reset, and an out-of-scale B probe $\|g_B'\| = 1/2$.
- **Old-task retention check:** Measure rare C progress on low-magnitude batches before and after B/clear, confirming $\varepsilon$-anchoring does not stall C.

#### 07. Exact Cauchy–Schwarz reachability and sign-match feasibility gate for clock levers (I)
- **Mechanism:** Before training C, run an exact algebraic feasibility check on $(t_1, t_2, \beta_1, \beta_2, \mathcal{D}_B)$: verify (i) $\gamma(t_1')/\gamma(t_2')$ opposes the required $v$-gap sign, (ii) the required $(m_h, v_h)$ clears the real-Adam Cauchy–Schwarz reachability bound $v_t \ge m_t^2 / c_1(t)$ (for $\beta_1 = \beta_2$, or its exact weighted generalization for $\beta_1 \neq \beta_2$), and (iii) $|\gamma(t_1')/\gamma(t_2') - 1|$ clears a minimum leverage floor. Refuse infeasible parks up front.
- **Novelty vs nearest prior art:** A feasibility falsifier extending `#274#07` from matched-clock equations to real-trajectory Adam reachability; prevents proposing algebraically valid $(m, v)$ pairs that no actual Adam history from $(0,0)$ can reach (such as $v_2 = 2/7 < 1/3$ in Fixture 1).
- **Cheapest first test:** Test the gate on Fixture 1's feasible $(g_a = 2)$ vs infeasible $(g_a = 1)$ cases, the sign-matched negative case ($v_2 > v_1$), and the zero-leverage $(t_1'=2, t_2'=4)$ trap at $\beta_1 = 1/2, \beta_2 = 3/4$; verify 100% separation.
- **Old-task retention check:** On every rejected park, verify refusal leaves A and C running vanilla Adam untouched with zero wasted C steps.

#### 08. Same-direction clock mismatch and late-horizon exhaustion falsifier (I)
- **Mechanism:** Pair every claimed clock-lever park with two mandatory negative controls from [flood triage row 391][triage]: (i) swap the history clocks so $\gamma(t_1')/\gamma(t_2')$ pushes the **same** way as the $v$-gap, and (ii) fast-forward both clocks by $+K$ steps into the asymptotic regime ($\gamma \approx 1$). Require the claimed park to fail cleanly on both, ruling out secret step-count resets or hidden matched-clock cancellation.
- **Novelty vs nearest prior art:** An audit harness rather than a new optimizer; enforces the ledger's anti-tautology standard by verifying that cancellation genuinely depends on the transient, signed bias-correction gap.
- **Cheapest first test:** Run both negative probes on Fixture 1 and on two cheater baselines (a secret step-count reset and a matched-clock null-space hider); verify only true clock-lever parks pass the positive case and fail both negative probes.
- **Old-task retention check:** Run probes read-only without uncharged state writes, verifying A and C metrics remain identical before and after auditing.

### Radial–angular split: C's job in direction, history-free scale in length

#### 09. Radial–angular feature contract with independent direction-only C reader ablation (P)
- **Mechanism:** Anchor [parent #10](effect-restoring-parks.md#10-radial-angular-split-history-dependent-c-job-in-orientation-history-invariant-scale-in-radius-p): store C's history-dependent task strictly in the unit orientation $\hat{z} = z / \|z\|_2 \in S^{d-1}$ ($d \ge 2$) of a multi-coordinate feature $z$ while honest C updates keep $\|z\|_2 = r$ history-invariant so the stored norm accumulator can be deleted. Require both direction ablation and constant-vector substitution to break an independent old C reader.
- **Novelty vs nearest prior art:** [RMSNorm][rms] normalizes and discards $\|z\|_2$, [Weight Normalization][weightnorm] and [magnitude-direction decoupling][magdir] reparameterize weights for optimization speed rather than accumulator deletion, and `#261#11` scalar recovery collapses to a public constant when history-free; here orientation preserves C's live job while radius deletes one historical accumulator.
- **Cheapest first test:** 2D orthogonal-regime toy ($e_{H_1} = (3/5, 4/5)$, $e_{H_2} = (4/5, -3/5)$) with latent shifting $r \in \{1/2, 3/4\}$ hidden from B's public context; compare `#261#11` scalar recovery, [RMSNorm][rms] discarding $\|z\|_2$, an equal-byte backup accumulator, and a C stream whose job reads amplitude $e_h^\top z$.
- **Old-task retention check:** Verify old C's angular classifier $\text{sign}(\hat{z}_2)$ holds across $r$ shifts and post-B/clear, and breaks under constant substitution or direction scramble.

#### 10. Finite-step Pythagorean radial-drift compensation for scale-invariant C objectives (P)
- **Mechanism:** Directly fix Fixture 2's Pythagorean drift ($\|z - \eta g_\perp\|_2 = \sqrt{r^2 + \eta^2 \|g_\perp\|_2^2} > r$): when C's task loss is scale-invariant (giving purely tangential gradients $g_\perp \perp z$), pair it with an exact second-order radial restoring factor $z' = (z - \eta g_\perp) \cdot (1 - \frac{1}{2} \eta^2 \|g_\perp\|^2 / r^2)$ (or step-matched decoupled decay) so honest finite-step C updates rotate $\hat{z}$ freely while holding $\|z\|_2 = r$ without storing a separate norm accumulator.
- **Novelty vs nearest prior art:** [AdamP][adamp] projects out radial momentum to slow norm growth but still suffers finite-step tangential Pythagorean drift, and [nGPT][ngpt] renormalizes onto the unit sphere $r = 1$ (destroying any variable scale $r$); this preserves a live, shifting regime radius $r$ against finite-step tangential inflation.
- **Cheapest first test:** Extend Fixture 2 ($z_0 = (3/5, 4/5), \eta = 3/4$) over 20 honest tangential C steps; compare uncompensated GD/Adam (monotonic radial blowup), [AdamP][adamp], [nGPT][ngpt]/RMSNorm unit projection (destroys shifting $r$), and an equal-byte backup scalar accumulator.
- **Old-task retention check:** Score old C angular accuracy and A margins across 20 steps plus B/clear, checking that radial compensation never slows C's angular convergence.

#### 11. Spherical-simplex multi-task C packing at a shared history-free radius $r$ (P)
- **Mechanism:** Pack $K \le d$ old C regimes as maximally separated unit directions $\{\hat{e}_1, \dots, \hat{e}_K\}$ (an orthonormal basis or regular simplex) on the shared sphere $r S^{d-1}$ of one multi-coordinate feature $z \in \mathbb{R}^d$. Honest updates on *any* active C regime keep $\|z\|_2 = r$ fresh while angular separation prevents old C regimes from interfering with one another.
- **Novelty vs nearest prior art:** Generalizes [parent #10](effect-restoring-parks.md#10-radial-angular-split-history-dependent-c-job-in-orientation-history-invariant-scale-in-radius-p) from 2 regimes to $K$ continual C tasks on one shared sphere, and solves the stalled-single-stream fragility of `#274#12` without needing two separate feature blocks.
- **Cheapest first test:** $d = 4$, $K = 4$ orthogonal C regimes arriving in rotating order while latent $r$ shifts; compare 4 separate scalar features (`#261#11`), [RMSNorm][rms] + equal-byte backup accumulator, and an adversarial $K = 6 > d$ overcrowded packing where angular interference breaks retention.
- **Old-task retention check:** Ablate each regime's direction independently and verify all $K$ old C readers plus A survive rotating arrivals and B/clear.

#### 12. Inverted AdamP: tangential projection for C job updates, radial routing for scale calibration (P)
- **Mechanism:** Invert [AdamP][adamp]'s gradient projection: project C's primary task gradient onto the tangent plane $T_{\hat{z}} S^{d-1}$ ($g_{\text{job}} \leftarrow g_{\text{job}} - (\hat{z}^\top g_{\text{job}})\hat{z}$) while routing C's honest regime-calibration signal purely along the radial unit vector $\hat{z}$. Direction and length evolve orthogonally in one vector $z$, preventing C's job loss from corrupting $\|z\|_2$ and preventing scale shifts from rotating $\hat{z}$.
- **Novelty vs nearest prior art:** [AdamP][adamp] and [Decoupled Orthogonal Dynamics][dod] suppress radial components unconditionally to stabilize scale-invariant weights; here the radial channel is *preserved* as a dedicated, interference-free conduit for C's online regime scale.
- **Cheapest first test:** 3D feature toy where C's job gradient has a nonzero spurious radial component while $r$ shifts across 3 regimes; compare unmodified Adam, [AdamP][adamp] (kills radial tracking), [Weight Normalization][weightnorm] (adds explicit scalar parameter = backup accumulator), and equal-byte backup scalar.
- **Old-task retention check:** Verify old C directional accuracy is unchanged across $r$ shifts and that deleting the radial calibration channel breaks B's scale without breaking C's direction.

#### 13. Multi-shell radial stratification for deleting multiple accumulators in one block (P)
- **Mechanism:** Partition a $d$-dimensional C-essential representation into two orthogonal sub-blocks $z = (z^{(1)}, z^{(2)}) \in \mathbb{R}^{d_1} \times \mathbb{R}^{d_2}$ ($d_1, d_2 \ge 2$) whose orientations serve disjoint old C heads and whose radii $(\|z^{(1)}\|_2, \|z^{(2)}\|_2)$ independently recover two distinct history-invariant scales (e.g., B's step-size scale and gradient-clip threshold), deleting two stored accumulators at once.
- **Novelty vs nearest prior art:** Extends [parent #10](effect-restoring-parks.md#10-radial-angular-split-history-dependent-c-job-in-orientation-history-invariant-scale-in-radius-p) from one scalar accumulator to a structured multi-scale tuple, distinct from [Adafactor][adafactor] or [8-bit optimizers][opt8] because every coordinate performs a verified old C job.
- **Cheapest first test:** $2 + 2$ coordinate toy recovering both step scale $r_1$ and clip threshold $r_2$; compare two kept scalar accumulators, [RMSNorm][rms] + 2 backup scalars, single-shell radius (cannot separate $r_1, r_2$), and a C stream where head 2 needs $\|z^{(2)}\|_2$.
- **Old-task retention check:** Independently ablate $\hat{z}^{(1)}$ and $\hat{z}^{(2)}$ on their respective old C heads and score A and both C heads after B/clear.

#### 14. Radius-dependence audit: detect when C's job secretly needs $\|z\|_2$ (I)
- **Mechanism:** Operationalize [flood triage row 391][triage]'s exact negative control ("a C stream whose job needs the radius"): evaluate every claimed radial–angular park under pure radial rescaling $z \mapsto \alpha z$ ($\alpha \in \{1/2, 2\}$) on held-out old C probes. If old C accuracy or loss degrades beyond tolerance, C's job genuinely reads the radius—refuse the pure history-invariant radial–angular contract (and route to coupled `#16` instead).
- **Novelty vs nearest prior art:** A sharp diagnostic falsifier; unlike direction-ablation alone (`#274#22`), which only checks that $z$ is non-constant, radial rescaling isolates whether C is genuinely invariant to $\|z\|_2$ vs secretly amplitude-coupled.
- **Cheapest first test:** Run the rescaling audit on two C readers: a cosine/angular classifier (must pass with 0 degradation) and an amplitude-sensitive regression head $e_h^\top z$ (must fail and trigger refusal); include a cheating reader that secretly applies RMSNorm internally (catches disguised scale discard).
- **Old-task retention check:** Audit is read-only; confirm zero state modification and verify refusal leaves vanilla C untouched.

#### 15. Equal-byte accounting against RMSNorm + backup scalar and Weight Normalization (I)
- **Mechanism:** Enforce strict byte parity: a $d$-dimensional radial–angular feature $z \in \mathbb{R}^d$ only saves bytes over a $(d-1)$-dimensional direction plus 1 kept norm accumulator (i.e., [Weight Normalization][weightnorm] or [RMSNorm][rms] + scalar) if C genuinely needs the $d$-th coordinate (or $S^{d-1}$ topology) without adding a separate parameter. Benchmark all arms at identical float/quantized byte counts.
- **Novelty vs nearest prior art:** A ruthless accounting falsifier directly answering the [idea ledger][ledger]'s equal-byte baseline rule (PR #1, L1 falsification); prevents counting a free-norm reparameterization as accumulator deletion when it merely hides the scalar inside an extra dimension.
- **Cheapest first test:** Compare $z \in \mathbb{R}^2$ (2 floats, 0 accumulators) against 1D angle + 1 kept scalar accumulator (2 floats total), [RMSNorm][rms] on $\mathbb{R}^2$ + 8-bit quantized accumulator ([8-bit][opt8]/[log-space][logq]), and `#261#11` scalar recovery on a 2-regime C task with hidden shifting $r$.
- **Old-task retention check:** Match total parameter + optimizer bytes to the byte and gate on identical A and old-C accuracy before scoring B scale error.

### Coupling step-count levers with radial–angular scale recovery

#### 16. Coupled clock–radius cancellation when C's job needs a history-dependent radius (P)
- **Mechanism:** Directly exploit Fixture 3's interaction: when C's old job genuinely requires a history-dependent radius $r(H_1) \neq r(H_2)$ (breaking `#274#10`) *and* the Adam clock mismatch pushes the same way as the moment gap (breaking `#274#05`), train C so the radius ratio $\|z(H_1)\|_2 / \|z(H_2)\|_2$ cancels the residual mismatched-clock ratio $u_2(g_B) / u_1(g_B)$ on $\mathcal{D}_B$. Both individual failure modes cancel into exact B equivalence.
- **Novelty vs nearest prior art:** Strictly stronger than both [parent #05](effect-restoring-parks.md#05-bias-correction-clock-mismatch-as-a-cancellation-lever-p) and [parent #10](effect-restoring-parks.md#10-radial-angular-split-history-dependent-c-job-in-orientation-history-invariant-scale-in-radius-p) stacked separately, and sharper than `#274#16` because the coupled factor is specifically Adam's transient bias-correction ratio $\gamma(t')$ paired with a radius-needing C feature; no public schedule $\nu(p)$ can reproduce a history-dependent radius ratio.
- **Cheapest first test:** Implement Fixture 3 ($H_1$: $(4,-2)$ at $t_1'=3, r=14/15$; $H_2$: $(-4,4,-1)$ at $t_2'=4, r=1$; $\mathcal{D}_B = \{\pm 1\}$); compare `#274#05` alone (fails sign-match), `#274#10` alone (breaks radius-needing C), their best equal-byte stack, step-count reset, [GEM][gem], and an undeclared B magnitude $g_B = 2$.
- **Old-task retention check:** Verify old C's amplitude-sensitive reader $e_h^\top z$ requires both the distinct directions *and* the distinct radii ($14/15$ vs $1$), and score A and C after B/clear.

#### 17. Pythagorean radial drift as a clock-free step-count estimator for bias correction (P)
- **Mechanism:** Invert Fixture 2's radial-drift bug into a clock-register deletion primitive: under controlled tangential C updates on $S^{d-1}$, $\|z_t\|_2^2 = r_0^2 + \sum_{k=1}^t \eta_k^2 \|g_{\perp,k}\|_2^2$ increases strictly monotonically with C's step count $t$. Recompute Adam's bias-correction factor $\gamma(\hat{t}')$ directly from $\|z_t\|_2$, deleting the explicit per-block step-count register while keeping C's job in $\hat{z}$.
- **Novelty vs nearest prior art:** Standard [Adam][adam] stores an integer step counter per parameter group (or globally, losing per-block clock skew); here the length of a C-essential feature doubles as an analog step-count clock, linking `#274#05` and `#274#10` by deleting the clock register itself.
- **Cheapest first test:** 2D tangential C stream with constant-norm gradients $\|g_\perp\| = 1$, $\eta = 1/2$, comparing $\|z_t\|_2$-reconstructed $\gamma(\hat{t}')$ against an explicit per-block step counter, a global step counter, step-count reset, and a variable-magnitude gradient stream (negative control where radial drift decouples from step count).
- **Old-task retention check:** Ablate $\hat{z}$ to prove C genuinely needs the direction; verify A and old C hold across 10 steps and B/clear.

#### 18. Directional clock-phase encoding: route young vs mature clocks to angular sectors (P)
- **Mechanism:** Partition the feature sphere $S^{d-1}$ into angular sectors correlated with clock age (young clocks with large $|\gamma(t') - 1|$ vs mature clocks with $\gamma(t') \approx 1$) through C's natural task progression, so B's readout applies sector-dependent weighting to the single feature $z$ while $\|z\|_2 = r$ stays history-invariant—compensating for clock exhaustion without storing a separate clock-age tag.
- **Novelty vs nearest prior art:** Unlike `#260` clock windows (which enforce hard arrival cutoffs) or explicit history tags, angular-sector routing reuses C's live directional geometry to distinguish active-lever histories from exhausted-clock histories.
- **Cheapest first test:** 2D sphere with 2 angular sectors (young $t'=2$ vs mature $t'=20$) at shared radius $r = 1$; compare sector-blind radial–angular `#10` (fails once clock matures), explicit clock tag at equal bytes, step-count reset, and a C stream that revisits the young sector at mature $t' = 20$ (negative control).
- **Old-task retention check:** Score A and both C sectors' old readers after B/clear, checking that sector routing does not distort C's directional decision boundaries.

#### 19. Controlled radial growth on B's step 1 to cancel step-2 bias-correction contraction (P)
- **Mechanism:** In Fixture 1, single-step mismatched-clock cancellation breaks on step 2 because $\gamma(t_1'+1)/\gamma(t_2'+1)$ contracts toward $1$. Let B's step 1 induce a small, lawful tangential kick on $z$ whose Pythagorean norm growth $\Delta \|z\|_2$ scales the step-2 update by the exact reciprocal of the clock-ratio contraction, extending single-step clock cancellation to 2-step B scripts without adding coordinates.
- **Novelty vs nearest prior art:** Combines Fixture 1's step-2 clock-decay problem with Fixture 2's Pythagorean length increment; unlike `#04` (which adds coordinates to bend $(m, v)$ curves), this uses the already-present radial–angular feature $z$ to pay the step-2 clock drift.
- **Cheapest first test:** 2-step B script $(+1, +1)$ from Fixture 1's clocks $(t_1'=3, t_2'=4)$ with a coupled 2D feature $z$; compare uncoupled single-step clock cancellation (breaks on step 2), `#04` higher-dim $(m, v)$ curves, step-count reset, and a 3-step B script exceeding the radial budget.
- **Old-task retention check:** Check that B's tangential kick keeps $\hat{z}$ strictly inside old C's angular decision margin, and verify A and old C after clear.

#### 20. Clock-age handoff of radial scale duty when a young C stream matures (P)
- **Mechanism:** When a young C sub-stream's step count $t$ grows into the asymptotic regime ($\gamma(t') \to 1$) and its clock-cancellation lever fades, smoothly hand the coupled clock–radius cancellation duty from the maturing feature $z_1$ to a freshly activated C sub-stream's feature $z_2$ (which has a young clock $t_2$), keeping the executed B update $\|z_{\text{blend}}\|_2 \cdot u(m, v, t'; g_B)$ invariant across every intermediate cut.
- **Novelty vs nearest prior art:** Sharpens `#274#19` (regime-switch handoff of scale duty) specifically for **clock-lever expiry**: even if $C_1$ is still active, its clock matures and loses bias-correction leverage, so handoff is triggered by clock age rather than stream idleness.
- **Cheapest first test:** Two-substream C schedule ($C_1$ runs 20 steps until $\gamma(t_1') \approx 1$; $C_2$ starts at step 15 with fresh $t_2 = 1$) with B arriving at steps 5, 17 (overlap), and 25; compare no-handoff `#16` (degrades as $C_1$ matures), global step-count reset, kept backup accumulator, and hard switch without overlap.
- **Old-task retention check:** Verify $C_1$'s old reader stays intact after handoff, $C_2$'s reader depends on $z_2$, and A holds at every intermediate cut.

#### 21. Interaction ablation: does coupled clock–radius cancellation beat stacking `#274#05` + `#274#10`? (I)
- **Mechanism:** Directly test the [idea ledger][ledger]'s merge rule: benchmark coupled `#16` against the strongest equal-byte stack of `#274#05` (mismatched-clock cancellation alone) + `#274#10` (history-invariant radial–angular split alone) + step-count reset + `#260` clock windows + [GEM][gem] across a sweep of streams varying (i) sign of clock-vs-$v$ mismatch and (ii) whether C's job reads $\|z\|_2$. Pass the variance gate (arm spread $>$ seed variance) before claiming a coupled primitive.
- **Novelty vs nearest prior art:** A comparative interaction falsifier; isolates whether the coupled object (`#16`) produces real gains outside the union of its two parent seeds' regimes, rather than merely renaming their stack.
- **Cheapest first test:** Small CPU continual Adam toy (2-layer MLP or linear-plus-spherical-head, 5 seeds) across a $2 \times 2$ grid: $\{\text{opposing}, \text{same-direction clock gap}\} \times \{\text{direction-only C}, \text{radius-needing C}\}$; require `#16` to win strictly on the bottom-right cell (same-direction + radius-needing) at matched bytes and A/C retention.
- **Old-task retention check:** Gate every arm on identical A retention floor and old-C accuracy before comparing B edit error and C plasticity; retire the coupled line if the stacked controls tie within seed CI.

#### 22. Four-probe adversarial audit for step-count levers and radial–angular parks (I)
- **Mechanism:** Bundle all four structural negative controls into one read-only verification suite for any PR in this lineage: (i) **same-direction clock swap** (must break pure `#01`), (ii) **late-horizon clock shift** $t \mapsto t + K$ (must expose asymptotic exhaustion unless `#05`/`#20` renews it), (iii) **pure radial rescaling** $z \mapsto \alpha z$ on old C readers (must pass for pure `#09`, fail for radius-needing `#16`), and (iv) **direction scramble / constant replacement** of $\hat{z}$ plus an undeclared B magnitude/direction probe (must expose live $(m, v)$ and C's genuine use of $\hat{z}$).
- **Novelty vs nearest prior art:** Extends `#274#22`'s three-probe suite to the exact clock-mismatch and radial-angular failure modes identified in [flood triage row 391][triage], catching cheaters (secret step-count resets, [RMSNorm][rms] + hidden backup scalar, matched-clock hiding) before any pilot or GPU spend.
- **Cheapest first test:** Run all four probes on Fixtures 1–3 plus three cheater baselines (secret clock reset, [Weight Normalization][weightnorm] extra scalar, and `#246#07` null-space hider); verify the suite separates legitimate parks from all three cheaters with zero false passes.
- **Old-task retention check:** All four probes are read-only evaluations with zero uncharged state writes; verify A and rare C metrics are bit-identical before and after auditing.

## Ranked deeper questions

1. **Does coupled clock–radius cancellation (#16) strictly beat stacking `#274#05` + `#274#10` + step-count reset on streams where both individual levers fail (#21)?** Test on the $2 \times 2$ CPU grid (opposing vs same-direction clock/moment gap $\times$ direction-only vs radius-needing C job) at matched total bytes and A/C retention: if the stacked controls tie within seed CI on the bottom-right cell, the coupled primitive collapses to its two parent ideas.
2. **How much of the 1D mismatched-clock win (#01) survives realistic Adam horizons ($t \gg 1/(1-\beta_2)$) and multi-step B scripts (#04, #05)?** Because $\gamma(t') \to 1$ exponentially and single-step cancellation breaks on step 2 (Fixture 1), measure the exact horizon $T_{\max}(\beta_1, \beta_2)$ where $|\gamma(t_1')/\gamma(t_2') - 1|$ stays large enough to beat matched-clock `#261#02` and `#260` clock windows—and test whether staggered partial clock refresh (#05) or radial-growth compensation (#19) extends $T_{\max}$ without hurting A/C retention.
3. **Can a radial–angular feature $z \in \mathbb{R}^d$ genuinely beat [RMSNorm][rms] + an equal-byte backup/quantized scalar accumulator (#15) once finite-step Pythagorean drift (#10) is compensated?** At matched total bytes (including quantized accumulators [8-bit][opt8]/[log-space][logq]), verify whether honest C updates keep $\|z\|_2 = r$ accurate across shifting latent scales without adding a hidden regularization tax or failing the radial-rescaling audit (#14).
4. **Does U-shaped $\gamma(t')$ branch selection (#02) actually unlock opposite-sign clock cancellation under standard $\beta_1 = 0.9, \beta_2 = 0.999$, or does the Cauchy–Schwarz reachability floor (#07) starve the falling branch in practice?** Check on real continual Adam trajectories from $(0,0)$ how often reachable $(m_h, v_h, t_h)$ states satisfy both the sign-match condition and the Cauchy–Schwarz floor on each side of $t^*$.

**Verdict: ambitious and sharply falsifiable on paper or CPU; no pilot result.** Mismatched Adam clocks break [PR #274](https://github.com/manojbajaj95/cl/pull/274)'s 1D symmetric-proposal $v$-obstruction on exact reachable trajectories (Fixture 1), and coupling them with a radial–angular feature resolves *both* the same-direction clock obstruction and radius-needing C jobs simultaneously (Fixture 3). Both levers have hard, testable failure modes—sign-match obstruction, Cauchy–Schwarz reachability, asymptotic clock exhaustion, Pythagorean radial drift, equal-byte parity against [RMSNorm][rms] + scalar, and radius-dependent C readers. If coupled `#16` and radial–angular `#09/#10` cannot beat the stacked controls on the $2 \times 2$ CPU toy (#21) and pass the four-probe audit (#22), stop before scaling.

[ledger]: https://github.com/manojbajaj95/cl/blob/ddb16c4100e4227c2dda63cbc2a62c8931ab29f0/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/ddb16c4100e4227c2dda63cbc2a62c8931ab29f0/reviews/flood-triage.md#L391
[adam]: https://huggingface.co/papers/1412.6980
[weightnorm]: https://huggingface.co/papers/1602.07868
[gem]: https://huggingface.co/papers/1706.08840
[adafactor]: https://huggingface.co/papers/1804.04235
[radam]: https://huggingface.co/papers/1908.03265
[rms]: https://huggingface.co/papers/1910.07467
[adamp]: https://huggingface.co/papers/2006.08217
[nscl]: https://huggingface.co/papers/2103.07113
[opt8]: https://huggingface.co/papers/2110.02861
[adamd]: https://huggingface.co/papers/2110.10828
[dod]: https://huggingface.co/papers/2602.05136
[magdir]: https://huggingface.co/papers/2606.25971
[ngpt]: https://huggingface.co/papers/2608.01284
[logq]: https://huggingface.co/papers/2608.22322
