# Tied split moments and a shared kink-state byte budget

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Minimal sufficient fold state](minimal-fold-state.md) ([PR #251](https://github.com/manojbajaj95/cl/pull/251)). **Review seed:** [Flood triage row 366](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L366), two score-3 cards: #03 ties a split unit's second-moment history at birth so both shards share one `v` slot and keep private first moments only, making the fold need just the combined first moment plus one `v`, with the cost in B learning speed measured; #15 gives the narrow host one shared byte budget for surviving kinks and future-update optimizer state, spent on whichever mix keeps the next update exact.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Relevant rules: the Noether-memory kill (check every invariant under the discrete finite-step optimizer, not gradient flow); the plasticity-reserve reruns (no ranking without a real spread in useful next writes); the "true by construction" kill (an exact fold built into a toy is not a win if tying `v` wrecks B learning or a `v`-reset ties it); and the merge-card rule (beat the stacked baselines of each part at equal bytes and information). **P** marks a candidate reusable operation, **I** an improvement or falsifier; neither is a priority claim.

## What would be new?

Neither second-moment pooling nor memory-budgeted optimizer compression is new on its own:

- **Second-moment structure and pooling:** [AdamPM](https://arxiv.org/abs/2610.24598) (2610.24598) and [Adam-mini](https://arxiv.org/abs/2406.16793) (2406.16793) pool second moments across parameter blocks to cut training RAM, with no fold-back exactness claim. [Matched Specialization, Different Adaptation](https://arxiv.org/abs/2610.15830) (2610.15830) already shows that Adam-trained networks with matched readout measurements respond differently to further learning because of retained second-moment scale and coordinate pattern, and that swapping `v` reverses adaptation while swapping `m` stays within margin. [Second-Moment Memory in Coordinatewise Adam](https://arxiv.org/abs/2608.15824) (2608.15824) proves that a single large gradient stored in `v` suppresses later updates for `M₂ = (1 − β₂)⁻¹` steps (`O(M₂⁻¹/²)` progress). Neither paper ties `v` across split halves at birth to guarantee an exact width fold.
- **Optimizer-state compression and memory budgeting:** [Guarded Compression of Adam State](https://arxiv.org/abs/2611.00589) (2611.00589) guards one step per coordinate; [Rounding in Preconditioner Space](https://arxiv.org/abs/2610.12444) (2610.12444) designs 4-bit AdamW quantization; [Tiered State Allocation](https://arxiv.org/abs/2607.19058) (2607.19058) and [Budget-aware Auto Optimizer Configurator](https://arxiv.org/abs/2605.04711) (2605.04711) allocate optimizer state under a fixed architecture; [Memory-Budgeted Analytic CL](https://arxiv.org/abs/2611.23040) (2611.23040) trades covariance rank for variance restoration at fixed features. On the weight side, [Variable-Width Transformers](https://arxiv.org/abs/2606.18246) (2606.18246) and [Variable Bit-width Quantization](https://arxiv.org/abs/2607.02893) (2607.02893) budget model parameters independently of optimizer continuation state.

What remains open is narrower than either seed as stated:

1. **Seed #03 (`#251#03`): fold-targeted `v`-tying at birth, priced against its cross-shard variance tax.** Tying `v` across split shards keeps the post-merge state inside F1's rank-2 refundable fiber, whereas untied twins have rank 4 and no narrow refund. The real question is whether the exact fold rule (which requires averaging `m` and scaling the narrow learning rate by `k`, not summing `m` at `η` — see F1) can beat a `v`-reset, post-hoc minimal statistics (`#239#02`), and AdamPM without paying an unacceptable cross-shard slowdown when shards see mismatched gradient scales.
2. **Seed #15 (`#251#15`): one fungible byte budget for surviving kinks and continuation state `σ_u`.** Separate kink (`#239#13`) and state (`#239#02`) budgets waste capacity whenever a commit stream alternates between kink-heavy and state-heavy merges. A unified exact-update byte pool is a candidate primitive only if it admits strictly more exact commits than separate budgets AND beats low-bit/low-rank optimizer state at equal total bytes without violating A/C retention.

## Contract

- Fix before the window opens: host, peak width, total narrow byte budget `B_total`, domain `D`, update class `U` (batches, trainable masks, hyperparameters, arithmetic), horizon `H`, A/C retention floors, and B/P utilities.
- **Tied-split birth rule:** when a unit splits into `k` shards for a window, bind them to one shared second-moment slot `v` updated by a predeclared pooling rule (e.g. mean-square, max, or partner-weighted), with private first moments `m₁…m_k` and a shared step counter `t`. At fold-back, the lawful narrow image must be fixed in advance (no post-hoc tuning on reference outputs). Report B/P learning speed during the window alongside fold exactness.
- **Shared byte budget:** every surviving U-kink (nonzero slope jump or trainable zero-sum knot) and every continuation-state coordinate `σ_u` is billed in exact bytes against `B_total`. A fold receipt is accepted iff a feasible `(kinks, σ_u)` allocation fits within `B_total` and keeps `f` and `T_u` exact (or within a predeclared `τ`) on `D` for all `u ∈ U^H`; otherwise fail closed to the last lawful model and log the refusal.
- **Required controls (from triage row 366):**
  - For #03: `#239#02` minimal statistic found after the fact, AdamPM pooling for memory alone, `v`-reset at fold, permanent split, a split whose shards genuinely need different `v` scales to learn B, and A/B/C retention at window, fold, and post-fold steps.
  - For #15: `#239#02` and `#239#13` with separate budgets at equal total bytes, low-rank or quantized optimizer state (8-bit/4-bit) at equal total bytes, a permanent wider model, and a negative-control commit where every mix exceeds `B_total`.

## Two exact fixtures (CPU, exact rational / 50-digit arithmetic, not pilots)

**F1 — The exact tied-`v` fold rule is `(m_avg, 2η)`, not `(Σm, η)`, and tying carries a cross-shard variance tax.** Take twin read-outs `a₁, a₂` on one frozen feature (`f = (a₁+a₂)h`), Adam with `β₁ = 1/2`, `β₂ = 3/4`, `η = 1/10`, `ε = 0` (and checked with `ε = 1/100` plus bias correction at `t = 6…9` over `g ∈ {0, 1/2, −5/4, 3}`). Both twins share one `v` slot at birth.
- **Naive sum rule fails on the first nonzero gradient:** let `m₁ = 1/2, m₂ = 3/2, v = 1` (no bias correction). On `g = 0`, wide `Δ(a₁+a₂)` and naive narrow `(m = m₁+m₂ = 2, lr = η)` both agree. On `g = 1`, `v' = 3/4·1 + 1/4·1 = 1`, wide twins compute `m₁' = 3/4, m₂' = 5/4` so `Δ(a₁+a₂) = −1/5`, whereas naive `(m = 2, lr = η)` computes `m' = 1 + 1/2 = 3/2` and `Δa = −3/20` — an exact error of `1/20` (`= η(1−β₁)g/√v'`). Over the 4-step bias-corrected sequence (`ε = 1/100`), naive error grows to `0.0440`.
- **Exact closed fold rule:** setting `a = a₁+a₂`, `m = (m₁+m₂)/2`, `v = v_shared`, and narrow learning rate `2η` (in general `m = (Σmᵢ)/k`, `lr = k·η`) matches the wide twin sum to `0` (`< 10⁻⁴⁷` across all 4 bias-corrected steps) because `m_narrow' = (m₁'+m₂')/2` and `v'` uses the same scalar `g²`.
- **Cross-shard variance tax during the window:** suppose shard B receives steady `g_B = 1/10` while partner shard P receives `g_P = 10`. With private `v` from zero init (bias-corrected), B takes a full step `−η = −1/10`. With mean-square shared `v_pool = (g_B² + g_P²)/2 = 10001/200 ≈ 50.005`, B's step shrinks by **70.71×** (`0.01414` of private `v`). This is 2608.15824's second-moment suppression transmitted *across* partners; any tied-`v` claim must beat this tax.

**F2 — One shared byte budget admits mixed commits that separate budgets refuse, until quantization closes the gap.** Give the narrow host `B_total = 5` FP32 scalar slots (20 bytes), versus a fixed separate budget `(B_kink = 2, B_state = 3)` (same 20 bytes):
- **Commit A (kink-heavy):** 3 surviving kinks (3 weight slots) + 2 shared/momentum state slots = **5 slots**. Separate `(2, 3)` refuses (`3 > 2`); shared `B_total = 5` accepts with exact next-step match.
- **Commit B (state-heavy):** 1 surviving kink (1 weight slot) whose wide twins untied (`m₁=1/2, v₁=1; m₂=3/2, v₂=9`), needing 4 state slots `{(m₁,v₁),(m₂,v₂)}` = **5 slots**. Separate `(2, 3)` refuses (`4 > 3`); shared `B_total = 5` accepts with exact next-step match.
- **Commit C (overload negative control):** 2 surviving kinks with 1 untied twin pair = **6 slots > 5**. Every exact mix exceeds `B_total`; both shared and separate must refuse and hold the last lawful model.
- **Quantized-state falsifier:** compressing Commit B's 4 state slots to 4-bit (fitting easily inside separate `B_state = 3`) rounds `v₁=1 → 1.125, v₂=9 → 8.0` and shifts the `g = 1` output step from `−0.122246` to `−0.121714` (`|err| = 5.32×10⁻⁴`). Shared `B_total` therefore beats quantized separate budgets only when the declared exactness / A/C margin `τ` is tighter than the quantization error and the stream actually mixes kink-heavy and state-heavy commits.

## Idea cards

### A. Tying second-moment history at birth (`#251#03`)

#### 01. Birth-tied `v` with `k·η` average-moment fold (P)
- **Mechanism:** Split a unit into `k` shards sharing one `v` slot and step counter `t` with private `m₁…m_k`. At fold-back, set `a = Σaᵢ`, `m = (Σmᵢ)/k`, `v = v_shared`, and narrow lr `k·η` (F1's exact closed image).
- **Novelty vs nearest prior art:** Corrects `#251#03`'s "summed first moment" wording (which fails on the first nonzero gradient by `η(1−β₁)g/√v'`) and turns F1's rank-2 tied row into an exact multi-step fold receipt; AdamPM (2610.24598) pools `v` for RAM without a fold-back law.
- **Cheapest first test:** Two-partner split-train-merge on a 4-knot ReLU toy with Adam; compare `(m_avg, 2η)`, naive `(m_sum, η)`, `v`-reset, and permanent split over 5 post-fold steps.
- **Old-task retention check:** A/C probes at window end, fold, and after 5 post-fold steps; verify B/P utility loss vs permanent split.

#### 02. Private window step sizes under a shared `v` (P)
- **Mechanism:** During the split window, let each shard carry a private scalar step-size multiplier `αᵢ` (so shard B scales up when partner P inflates `v_shared`), while updating the single shared `v`. At commit, both shards return to common `η` so `v₁ = v₂` still holds and F1's exact fold closes untouched.
- **Novelty vs nearest prior art:** Attacks F1's 70.7× cross-shard variance tax without breaking post-merge tie invariance. Adam-mini/AdamPM use one scale per block and cannot neutralize cross-partner gradient mismatch.
- **Cheapest first test:** F1's `g_B = 1/10, g_P = 10` window with private `α_B = √(v_shared / v_local_ema)` vs plain shared `v` vs private `v` (permanent split). Measure B convergence steps and exact post-fold match.
- **Old-task retention check:** A/C during the boosted window (ensuring `α_B` does not overshoot A/C margins) and across 5 post-fold steps.

#### 03. Partner-asymmetric `v` pooling rules (P)
- **Mechanism:** Because any symmetric or asymmetric function `v' = β₂ v + (1−β₂) Φ(g₁, g₂)` leaves `v₁ = v₂` at merge, replace mean-square pooling with harmonic/min pooling, clipped-partner pooling, or B-priority pooling so a noisy partner cannot inflate `v` and stall B.
- **Novelty vs nearest prior art:** AdamPM uses fixed block mean pooling. Choosing `Φ` to bound cross-shard suppression (2608.15824) while preserving foldability is specific to split-merge windows.
- **Cheapest first test:** Sweep `Φ ∈ {mean-sq, max, min, Huber-clipped}` on matched vs 100×-mismatched `(g_B, g_P)` streams; compare B/P utility and fold exactness against `v`-reset and private `v`.
- **Old-task retention check:** Check that min/clipped pooling does not destabilize the noisy partner P or cause A/C spikes during the window.

#### 04. Selective untying with a pre-declared escape hatch (P)
- **Mechanism:** Start every split with tied `v`, but monitor the ratio `g_max² / g_min²` during the window. If it exceeds a predeclared threshold `ρ` for `L` steps, untie `v` into private `(v₁, v₂)` and declare a no-refund (or bill the extra slots to `B_total`).
- **Novelty vs nearest prior art:** Combines `#251#03` with `#239#02`'s post-hoc check: avoids paying the variance tax on mismatched shards while keeping cheap exact folds on matched shards.
- **Cheapest first test:** Mix 50% matched-scale and 50% 100×-mismatched split windows on the 4-knot toy; compare always-tied, always-untied, escape-hatch, and `v`-reset on B utility and fold rate.
- **Old-task retention check:** A/C on both folded and escaped windows; escaped windows must not silently exceed peak width or drop A/C.

#### 05. Lineage-scoped `v` tying across k-way splits (P)
- **Mechanism:** Tie `v` strictly along the split-lineage tree (only sibling shards from the same parent unit share `v`), leaving unrelated host units with private `v`. Nested splits inherit their parent's `v` pointer so `k`-way fold-back needs `(Σmᵢ)/k`, one `v`, and `k·η`.
- **Novelty vs nearest prior art:** Adam-mini/AdamPM pool by architectural block/head; lineage-scoped tying pools only where a fold is planned, avoiding unnecessary cross-feature interference.
- **Cheapest first test:** 8-unit ReLU host where 2 units split 3-ways while 6 stay unsplit; compare lineage-tied `v` against layer-pooled AdamPM and all-private `v` on B/P loss and exact fold of the 2 split units.
- **Old-task retention check:** A/C on the 6 unsplit units must suffer zero cross-feature `v` contamination from the split window.

#### 06. Re-tie before commit via a lawful cooling suffix (P)
- **Mechanism:** Train B and P with private `v₁, v₂` during the high-divergence phase so B pays zero variance tax, then switch both shards to a shared `v` (or equal-weight EMA pull) for the final `L` steps before commit so `|v₁ − v₂|` decays by `β₂^L` into a `τ`-certified near-twin fold (`#251#07`).
- **Novelty vs nearest prior art:** Trades exact zero-gap fold for a bounded `τ`-gap fold while avoiding early-window suppression; distinct from a hard `v`-reset which discards all curvature history.
- **Cheapest first test:** On the 100×-mismatched `(g_B, g_P)` window, run private `v` for `T − L` steps and tied `v` for `L ∈ {0, 2, 5, 10}` steps; compare B speed, post-fold output gap, and `v`-reset.
- **Old-task retention check:** Verify the `τ` output gap stays below A/C margins on every post-fold step, and compare A/C against `v`-reset.

#### 07. Cross-shard variance-tax falsifier (I)
- **Mechanism:** Construct the hardest adversarial B/P split where shard B's gradient is `10⁻²` of shard P's (or sparse vs dense), and test whether birth-tied `v` loses more B utility than simply resetting `v` at fold or keeping a permanent split.
- **Novelty vs nearest prior art:** Operationalizes triage row 366's required control ("a split whose shards need different `v` to learn B") using 2608.15824's denominator-suppression mechanism.
- **Cheapest first test:** Sweep `|g_P / g_B| ∈ {1, 3, 10, 30, 100}` on a 20-step split window; find the exact crossover ratio where `v`-reset at fold beats birth-tied `v` on B utility + post-fold accuracy.
- **Old-task retention check:** Report A/C retention at each ratio; flag any regime where `v`-reset's post-fold step overshoot breaks A/C while tied `v` holds it.

#### 08. Shared-`v` latent-susceptibility audit (I)
- **Mechanism:** Adapt 2610.15830's intervention protocol to folded models: take two birth-tied folds with identical outputs `f` and identical `m_avg` but different inherited `v_shared` scales, apply a common post-fold task shift, and measure whether `v_shared` protects or harms A/C relative to `v`-reset.
- **Novelty vs nearest prior art:** Directly tests whether preserving `v_shared` across a fold is actually beneficial for continual learning, or whether exact continuation of a bad `v` amplifies latent susceptibility.
- **Cheapest first test:** Replicate 2610.15830's two-target readout-matched setup with a split-merge window; compare exact tied-`v` fold vs `v`-reset vs permanent split over 10 post-fold updates.
- **Old-task retention check:** Measure old-target readout precision switch rate (2610.15830's metric) and worst-prefix A/C across all 10 steps.

### B. One shared byte budget for kinks and continuation state (`#251#15`)

#### 09. Exact-update byte-pool allocator (P)
- **Mechanism:** Give the narrow host one byte pool `B_total`. At commit, enumerate feasible `(active kinks, σ_u slots)` pairs whose byte sum `≤ B_total` and whose folded step matches the wide reference on `U^H`; issue a receipt for the minimum-byte exact mix, or refuse if none exists.
- **Novelty vs nearest prior art:** Unifies `#239#02` and `#239#13` into one fungible resource, unlike fixed-architecture optimizer allocators (2607.19058, 2605.04711) or state-blind width budgets (2606.18246).
- **Cheapest first test:** Run F2's 3-commit suite (A kink-heavy, B state-heavy, C overload) plus 50 random mixed commits at `B_total = 5` slots against separate `(2, 3)` and `(3, 2)` budgets.
- **Old-task retention check:** A/C at commit and after 3 post-fold steps on every accepted commit; confirm refused commits preserve the last lawful A/C state.

#### 10. Kink-for-state swap via lawful receiver freezing (P)
- **Mechanism:** When `kinks + σ_u > B_total`, freeze a surviving kink's trainable mask in `U` (keeping its weight bytes for `f` exactness while freeing its `σ_u` bytes) and spend the freed bytes on exact continuation state for a kink that `U` still trains.
- **Novelty vs nearest prior art:** Turns `#251#13`'s freeze-on-cancel clause into an active byte-pool move; prior pruning/freezing work does not price freed optimizer bytes into another unit's exact continuation receipt.
- **Cheapest first test:** 4-knot F2 host with `B_total = 6` slots, 2 surviving kinks (one converged on A, one active on B); compare freezing the A kink to fund exact untied `σ_u` on the B kink vs keeping both trainable with reset `σ_u`.
- **Old-task retention check:** A/C on the frozen kink's region plus B/P progress over 5 post-fold steps; verify freezing A does not starve a third task C2.

#### 11. State-for-kink swap via certified `τ`-tie-down (P)
- **Mechanism:** When a commit has one extra surviving kink that overflows `B_total`, collapse an untied twin's 4 state slots `{(m₁,v₁),(m₂,v₂)}` into 2 tied slots `(m_avg, v_bar)` ONLY if the `#251#07` Lipschitz bound certifies that the `H`-step output gap stays within `τ`, spending the 2 freed slots on the extra kink.
- **Novelty vs nearest prior art:** Extends guarded compression (2611.00589) from per-coordinate RAM savings to cross-resource trading (compressing state *specifically* to avoid refusing a surviving kink).
- **Cheapest first test:** F2 Commit C (2 kinks + 1 untied twin = 6 slots > 5) with near-tied `v₂ = v₁(1+ε)` for `ε ∈ {0.01, 0.1, 0.5}`; check acceptance rate and exact output gap vs refusal.
- **Old-task retention check:** Check every A/C margin against `τ`; zero A/C label flips allowed on accepted `τ`-swaps.

#### 12. Precision-graded byte pool (FP32 / 8-bit / 4-bit / frozen) (P)
- **Mechanism:** Let the shared byte pool assign each surviving kink's `σ_u` a precision tier `{32-bit exact, 8-bit guarded, 4-bit preconditioner-rounded, 0-bit frozen}` so total weight + state bytes `≤ B_total`, allocating full FP32 only to kinks whose quantization error would breach `τ`.
- **Novelty vs nearest prior art:** Combines 2610.12444's preconditioner-space rounding and 2611.00589's guard with kink-count budgeting; must beat uniform 4-bit/8-bit optimizer state under separate budgets at equal total bytes.
- **Cheapest first test:** F2 Commit B + Commit C at 20 bytes total; compare uniform 4-bit separate budgets vs precision-graded shared pool across tight (`τ = 10⁻⁴`) and loose (`τ = 10⁻²`) margins.
- **Old-task retention check:** Count A/C flips and worst-prefix A/C drift over 5 post-fold steps at equal total bytes.

#### 13. Blind pre-commit budget publications for mixed streams (P)
- **Mechanism:** Before a window opens, the host publishes only `B_total` and the byte-cost table `(bytes_per_kink, bytes_per_tied_slot, bytes_per_untied_slot)` rather than fixed `(R, B_state)`. Blind partners can independently choose to cancel kinks OR tie `v` to stay under the shared cap.
- **Novelty vs nearest prior art:** Generalizes `#251#10` (cancel above cap `R`) and `#251#14` (reservation menus) into a single scalar currency that partners can pay in either architecture or optimizer history.
- **Cheapest first test:** Simulate 100 blind 2-partner commits on 6 knots where partners privately have either high kink count or mismatched `v`; compare acceptance rate under scalar `B_total` vs best fixed `(R, B_state)`.
- **Old-task retention check:** A/C and B/P on all accepted commits; check that blind partners do not game `B_total` by dropping `σ_u` needed for A/C stability.

#### 14. Overload refusal and rollback contract (I)
- **Mechanism:** Require every shared-pool allocator to detect commits where *no* lawful `(kinks, σ_u)` mix fits `B_total` (F2 Commit C), refuse cleanly, keep the pre-window checkpoint, and log the minimum byte deficit `ΔB`.
- **Novelty vs nearest prior art:** Implements triage row 366's mandatory negative control ("a commit where every mix exceeds the budget") so the allocator cannot claim wins by silently degrading updates or widening.
- **Cheapest first test:** Stress-test the allocator on a 25% overload stream; verify 100% refusal on over-budget commits, 0% silent state truncation, and accurate `ΔB` reporting.
- **Old-task retention check:** Confirm A/C on refused commits is bit-identical to the pre-window host.

#### 15. Separate-budget and quantized-state dominance test (I)
- **Mechanism:** Directly pit one shared pool `B_total` against fixed `(B_kink, B_state)` and against 4-bit/8-bit/low-rank optimizer state at identical total bytes across three stream regimes: uniform, alternating kink/state-heavy, and adversarial overload.
- **Novelty vs nearest prior art:** The ledger's stacked-control falsifier for `#251#15`; if uniform 4-bit optimizer state inside separate budgets matches acceptance and A/C retention, the shared pool is an unnecessary complexity.
- **Cheapest first test:** 4-knot and 8-knot synthetic commit streams × 3 regimes × `{exact, τ=10⁻³, τ=10⁻²}`; report accepted commits, B/P utility, and A/C floors.
- **Old-task retention check:** Worst-prefix A/C across the full stream; a tie on acceptance with worse A/C is a loss.

### C. Coupling tied split moments with the shared byte pool

#### 16. Birth-time byte pricing of private vs shared `v` (P)
- **Mechanism:** Charge each split shard its fold-back byte bill at birth: birth-tied `v` reserves 2 state slots `(m_avg, v)` from `B_total`, leaving `B_total − 2` for kinks; requesting private `v` pre-reserves 4 state slots, forcing partners to cancel 2 more kinks to fit `B_total`.
- **Novelty vs nearest prior art:** Joins `#251#03` and `#251#15` causally — partners trade B learning speed (private `v`) against kink survival (more receivers) using one shared byte currency before training starts.
- **Cheapest first test:** Two-partner 6-knot window at `B_total = 7` slots: compare partners choosing tied `v` + 3 kinks vs private `v` + 1 kink on both matched and 100×-mismatched gradient scales.
- **Old-task retention check:** A/C and B/P at commit and after 5 post-fold steps; verify neither choice violates A/C.

#### 17. Cross-knot `v` tie-groups inside the byte pool (P)
- **Mechanism:** Allow the byte pool to tie `v` not only across twin shards of one split unit, but across two *distinct* surviving kinks whose post-merge gradients stay collinear (or within a `τ` cone), freeing 1 state slot per tied pair to admit an extra kink.
- **Novelty vs nearest prior art:** Bridges lineage-scoped tying (05) and AdamPM's block pooling, gated by an explicit `U`-sufficiency / `τ` certificate rather than heuristic block shape.
- **Cheapest first test:** 4-knot host where two adjacent knots share nearly identical activation supports on `U`; measure whether cross-knot `v`-tying frees a slot for a 3rd kink without exceeding `τ`.
- **Old-task retention check:** Test A/C on an input that activates one knot and not the other (breaking gradient collinearity) to verify the `U`-scope catches out-of-cone batches.

#### 18. Budget-carrying receipts across chained windows (P)
- **Mechanism:** Carry the active `(kinks, σ_u)` byte ledger and tied-`v` pointers into a second split-merge window. If window 2 cancels a window-1 kink, its freed bytes immediately unlock an untied `v` or a new kink without widening the host.
- **Novelty vs nearest prior art:** Tests whether the shared byte pool is reusable across continual-learning rounds (`#251#19`), rather than a one-shot fold accounting trick.
- **Cheapest first test:** Two consecutive windows on a 6-knot host at fixed `B_total = 6`: window 1 is state-heavy (1 kink, 4 state), window 2 cancels/replaces into kink-heavy (3 kinks, 2 state); compare against separate budgets and permanent widening.
- **Old-task retention check:** Retain A/C from before window 1 AND window 1's B/P skills through window 2's fold and 3 suffix steps.

#### 19. Third-writer utility under tied-`v` vs byte-reallocated folds (P)
- **Mechanism:** After folding into `B_total`, train a blind third task C2 on the narrow host. Compare C2's learning speed and retention when `B_total` was spent on `{more kinks + birth-tied v}` vs `{fewer kinks + untied exact σ_u}` vs `{fewer kinks + v-reset}`.
- **Novelty vs nearest prior art:** Tests whether the returned bytes are genuinely usable by an unseen learner (`#251#18`), separating bookkeeping equivalence from real continual-learning plasticity.
- **Cheapest first test:** 4-knot host, `B_total = 5`, 10-step C2 rational-interval task after commit; compare C2 loss and narrow-vs-wide fidelity across the three allocations.
- **Old-task retention check:** Score A/C and window-1 B/P at every step of C2; an allocation that wins C2 by forgetting A or B fails.

#### 20. Per-kink optimizer downgrade inside the byte pool (P)
- **Mechanism:** Let a fold receipt downgrade a surviving kink's post-fold optimizer from Adam (2 state slots) to heavy-ball momentum (1 slot, always rank-1 exact-foldable) or plain SGD (0 slots) when `B_total` is tight, paying the slower convergence explicitly to avoid refusing a kink.
- **Novelty vs nearest prior art:** Extends 2605.04711's block-level optimizer configuration into a commit-time fold receipt coupled with exact kink retention.
- **Cheapest first test:** F2 Commit C (overflows `B_total = 5` under Adam) admitted by downgrading the lower-curvature kink to momentum (saving 1 slot); compare against refusal and 4-bit Adam.
- **Old-task retention check:** A/C and B/P over 10 post-fold steps; check that the momentum kink does not oscillate or drift past A/C margins.

#### 21. Finite-precision tie-breaking in shared-`v` byte pools (I)
- **Mechanism:** Re-evaluate F1's exact `(m_avg, k·η)` fold and F2's byte-pool advantage in bf16/fp16 with fixed summation order. Rounding `(m₁+m₂)/2` or `v_shared` can break exact multi-step closure even when rational arithmetic closes.
- **Novelty vs nearest prior art:** Applies [slot-echo](https://github.com/manojbajaj95/cl/pull/229) and `#251#20` directly to birth-tied `v`: if fp16 rounding already produces a `10⁻³` gap, exact FP32 tied-`v` loses its edge over 8-bit/4-bit separate budgets.
- **Cheapest first test:** Run F1's 4-step sequence in binary16 and bfloat16; measure `|(a₁+a₂) − a_narrow|` vs 4-bit quantized untied state.
- **Old-task retention check:** Track A/C label flips separately from numeric mismatch under both precisions.

#### 22. Full stacked-control matrix (I)
- **Mechanism:** Cross `{birth-tied v (2η), private-window-LR tied v, post-hoc minimal σ (#239#02), AdamPM pooling, v-reset, permanent split}` × `{shared B_total, separate (B_kink, B_state), 4-bit/low-rank σ_u, permanent wider model}` at matched total bytes, information, and U.
- **Novelty vs nearest prior art:** The mandatory ledger gate for both seeds combined. Neither seed earns primitive status unless it beats the best stacked cell on admitted useful commits and B/P utility at equal bytes and A/C retention.
- **Cheapest first test:** Exhaustive 4-knot toy suite (matched + mismatched gradient scales × kink-heavy + state-heavy + overload commits × 10-step C2 suffix), CPU-only.
- **Old-task retention check:** Worst-prefix A/C across all windows and C2; any cell that drops an old task is disqualified.

## Ranked deeper questions

1. **Can private window learning rates (or asymmetric `v` pooling) neutralize the cross-shard variance tax without breaking post-merge `v`-tying?** (01, 02, 03, 07) F1 shows a 70.7× slowdown for shard B under a 100× gradient mismatch with mean-square shared `v`. If private window step sizes `αᵢ` or clipped pooling recover B's speed while keeping `v₁ = v₂` at merge, `#251#03` survives; if not, `v`-reset at fold or permanent splits dominate whenever partners have different gradient scales.
2. **When does one shared byte budget strictly beat 4-bit/8-bit optimizer state under separate budgets?** (09, 12, 15, 21) F2 shows that a shared pool beats fixed separate budgets on mixed kink-heavy/state-heavy streams, but 4-bit quantization (2610.12444) fits Commit B inside the separate state budget with a `5.3×10⁻⁴` step error. The shared pool is a real primitive only in regimes where exactness (or tight `τ`) matters more than 4-bit rounding error, or where precision-graded allocation inside one pool beats uniform quantization at equal bytes.
3. **Does preserving `v_shared` across a fold help or hurt continual-learning retention under 2610.15830's latent susceptibility?** (08, 19) Exact continuation faithfully inherits whatever second-moment suppression (2608.15824) or directional susceptibility (2610.15830) formed during the split window. If `v`-reset consistently beats exact tied-`v` continuation on A/C retention and third-writer C2 speed, exact `v` preservation is solving the wrong target.
4. **Does coupling birth-time `v`-tying with the shared byte pool change what blind partners can negotiate?** (04, 13, 16, 18) Pre-pricing private `v` against surviving kinks inside one scalar `B_total` lets blind partners trade optimization speed for architectural capacity; the test is whether this admits more useful multi-window commits than independent `#239#02` + `#239#13` at equal peak width and bytes.

**Verdict:** Both seeds are conditional and tightly coupled. F1 sharpens `#251#03`: birth-tied `v` closes exactly over multiple steps only with `(m_avg, k·η)` (not `(Σm, η)`), and immediately exposes a severe cross-shard variance tax (70.7× at 100× gradient mismatch) that must be beaten against `v`-reset and private-`v` splits. F2 sharpens `#251#15`: one shared byte budget beats separate `(B_kink, B_state)` on mixed commits while failing closed on overload, but only beats 4-bit/8-bit separate budgets when A/C margins or exactness forbid quantization error. Cheapest next step (CPU, minutes): Question 1 — sweep gradient-scale ratio `|g_P/g_B|` comparing birth-tied `v` (+ private window `αᵢ`), `v`-reset, and permanent split on a 2-partner ReLU toy with A/C retention checks.
