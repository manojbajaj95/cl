# Protective batch orders: pre-shift momentum shields and order-safety certificates

**Status:** Ideas only; no experiments, probe code, or GPU work. Two exact-arithmetic rational fixtures were checked by hand to ground the cards (below); no code is committed. **Parent:** [Batch-order interventions](batch-order-interventions.md) ([PR #197](https://github.com/manojbajaj95/cl/pull/197)). **Review seeds:** [Flood triage, row 304](https://github.com/manojbajaj95/cl/blob/8519dfe/reviews/flood-triage.md#L304) scores #197 cards **15** (*a momentum shield before a known shift*: when the next task `B2` is announced, order the current window so it ends with momentum along an old-task-protective direction at identical endpoint weights, protecting `A` through `B2`'s first steps by order alone) and **19** (*an order-safety certificate against ordering attacks*: certify that no permutation of an incoming window can move optimizer slots into a region harming `A` by more than `δ` after a declared suffix, so certified windows can be left to an untrusted pipeline) at 3. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/8519dfe/reviews/idea-ledger.md).

Ledger and parent constraints that bind this node:

- **Bounded-delay stability scheduling (killed in ledger) & [2606.29554][shuffle]:** Reordering within a window changes end weights only at `O(η²)` for memoryless SGD, and gradient accumulation eliminates order effects at equal latency. Fixed-clock optimizers (fixed-`β` momentum, AdamW, Lion) promote equal-multiset order contrasts to `O(η)` ([2606.29554][shuffle]), while a clock-matched optimizer restores `O(η²)`. Therefore **gradient accumulation at equal latency** and a **clock-matched optimizer** are mandatory negative controls for every card.
- **Heavy-ball lock & constant-LR Adam injectivity ([PR #197](batch-order-interventions.md)):** Under constant-LR heavy-ball with frozen gradients, `θ_K` locks `m_K` (`θ_K = θ_0 − η/(1−β)·(S − β m_K) + c`), so a first-order momentum shield at identical endpoint weights **does not exist** at constant LR. Constant-LR Adam also showed zero exact weight-tied, slot-distinct pairs up to length 10. Every shield card must therefore declare which channel carries it—a **predeclared nonconstant LR schedule** (warmup, cosine, step drop), **curvature (`O(η²)`)**, or an **`ε`-weight tolerance**—and include a **residual-weight-only control** (start `B2` from the shield's `θ_K` with reset/default slots).
- **Margin confound, replay-deadline null ([PR #113](https://github.com/manojbajaj95/cl/pull/113)), and stacked-baseline bar:** Match per-item margins and `B2` gain throughout. A shield must beat **replay-last scheduling (with free endpoints)**, **partial Adam reset ([2306.17833][reset])**, **direct momentum/slot writes ([PR #185](slot-splices.md))**, and **EWC/STABLE damping ([2611.10655][stable])**—or explicitly state the serving/interface constraint (e.g. frozen `θ_K` contract, data-only pipeline) that makes those baselines illegal. A certificate must beat **fixing the order everywhere (hash-sorting)**, **gradient accumulation**, and **after-the-fact Proof-of-Learning ([2103.05633][pol])**.

## What is new here, and what is not

Both seeds sit next to active literatures that must be conceded up front:

- **Pre-shift protection & optimizer-state CL:** Partial optimizer reset at task boundaries ([2306.17833][reset]), adaptive drift/damping optimizers ([STABLE][stable], [FOGO][fogo], [2610.27835][ocl-opt]), gradient projection ([GPM][gpm]), delayed optimizer-state transport ([2608.24593][transport]), slot-mediated trait transfer ([2608.20442][stored]), and replay/curriculum scheduling all protect old tasks across shifts. None of them delivers a **data-order-only, endpoint-weight-neutral shield** over a fixed multiset the receiver already holds, preserving the serving checkpoint `θ_K` while releasing A-protective momentum only once `B2` begins.
- **Certified defenses against training-time attacks:** [BRRR][brrr] (2104.09667) demonstrates adversarial batch-order attacks; [Proof-of-Learning][pol] (2103.05633) audits order *after* training by replay; [FullCert][fullcert] (2406.11522) and [2512.20865][poison-cert] certify training against *data-value* poisoning via abstract interpretation; [BagFlip][bagflip] (2205.13634) and [2605.21780][dp-backdoor] use randomized smoothing/bagging; [GraB][grab] (2205.10733) picks *one* good permutation for convergence; [Safe-order-families (PR #195)](https://github.com/manojbajaj95/cl/pull/195) certifies linear extensions of a *chosen* partial order for a frozen bridge. None of these certifies **unconditional (or pipeline-bounded) permutation safety of an incoming window** against an untrusted ordering pipeline, with a compact dual proof that catches **joint multi-coordinate and `(m, v)`-coupled failures** missed by marginal checks.

Both objects count as candidate primitives **only if** they survive their sharpest structural threats: (1) for Seed #15, whether `β_1^t` decay and the heavy-ball lock leave enough non-trivial, serving-contract-preserving protection to beat replay-last, reset, and accumulation after 10+ `B2` steps; (2) for Seed #19, whether a meaningful fraction of real windows are jointly certifiable (with a rigorous second-order remainder bound) more cheaply than hash-pinning or gradient accumulation.

## Two exact paper fixtures (sanity checks, not evidence)

Both fixtures use exact rational arithmetic on frozen-gradient windows (no committed code).

**1. Schedule-carried momentum shield at identical endpoint weights.** Take heavy-ball momentum `m_k = β m_{k-1} + g_k`, `θ_k = θ_{k-1} − η_k m_k` with `β = 1/2`, `m_0 = 0`, frozen gradients during a 4-batch window, and a predeclared warmup schedule `η = (1, 1, 2, 2)`. The weight impulse vector `α_j = Σ_{k=j}^4 η_k β^{k-j}` is `(9/4, 5/2, 3, 2)` while the momentum impulse vector `w_m` is `(1/8, 1/4, 1/2, 1)`—linearly independent, breaking the constant-LR lock.
- On the multiset `{2, 1, −1, −2}`: `π_+ = (−2, 1, −1, 2)` and `π_− = (2, 1, −2, −1)` end at the **exact same weight** `θ_4 − θ_0 = +1`, yet end with opposite momenta `m_4(π_+) = +3/2` vs `m_4(π_−) = −3/2` (gap `3`).
- On `{4, 1, −1, −4}`: `π_+ = (−4, 4, −1, 1)` and `π_− = (4, −4, 1, −1)` both return exactly to `θ_4 = θ_0` with `m_4 = +1` vs `−1`.
- Over a subsequent `T`-step `B2` suffix at constant `η_B`, `m_4` adds a carryover shift `−η_B (1 − 2^{-T}) m_4`. If `B2` pushes `θ` positive and harms `A` when `θ > θ_0 + τ`, `π_+` cancels `B2`'s initial drift on `A` without moving `θ_4` at the shift boundary.
- **Hidden catch visible in the fixture:** On `{2, 1, −1, −2}`, `π_+` visits intermediate weights `θ − θ_0 = (2, 2, 4, 1)` while `π_−` visits `(−2, −4, −2, 1)`. Endpoint neutrality does **not** imply prefix safety; every shield must be audited at every prefix.

**2. A window that passes marginal checks yet fails jointly (and its certifiably safe twin).** Take two coordinates, `K = 4`, `β = 1/2`, `w_m = (1/8, 1/4, 1/2, 1)`, and a joint `A`-sensitivity failure condition `m_{4,1} + m_{4,2} > 1` (e.g., a shared readout or joint `A`-margin budget `δ = 1`).
- **Correlated window** `W_unsafe = {(1/2, 1/2), (1/2, 1/2), (0, 0), (−1/2, −1/2)}`: per-coordinate marginal checks pass (`max_π |m_{4,1}| = 11/16 < 1`, `max_π |m_{4,2}| = 11/16 < 1`), yet the single permutation `((−1/2, −1/2), (0, 0), (1/2, 1/2), (1/2, 1/2))` aligns both coordinates to give `m_{4,1} + m_{4,2} = 11/8 > 1` (**jointly unsafe**).
- **Anti-correlated twin** `W_safe = {(1/2, −1/2), (1/2, −1/2), (0, 0), (−1/2, 1/2)}`: identical per-coordinate marginals (`11/16` each), yet `m_{4,1} + m_{4,2} = 0 ≤ 1` for **every** permutation (**jointly safe**).
- **Consequence:** Per-coordinate marginal thresholds are **unsound** (they admit `W_unsafe`), whereas naive sum-of-marginals bounds (`11/16 + 11/16 = 11/8 > 1`) are **over-conservative** (they falsely reject `W_safe`, crushing the certifiable-window fraction). Only a joint permutation certificate separates the two.

### Shared evaluation contract

- Fix the batch multiset `W`, optimizer law, hyperparameters, LR schedule, precedence constraints, and default order **before** searching a shield or issuing a certificate.
- Measure old-task retention on `A` (including a rare slice) and unaffected control `C` at **every prefix** of `W`, at the boundary `θ_K`, after `10` steps of `B2` (and again after `50` unassisted `B2` steps to test whether carryover survives `β_1^t` decay), at matched `B1`/`B2` utility and per-item margins.
- Charge all search, dual-LP solving, sketch computation, verification, and fallback pinning/accumulation costs. Report results on blind streaming windows separately from planted fixtures.

## Idea cards

**P** = candidate primitive if it beats the stacked controls on blind windows; **I** = improvement, diagnostic, or mandatory falsification audit. All first tests are proposed CPU-scale checks.

### A. Pre-shift momentum shields (Seed #15)

#### 01. Schedule-carried pre-shift momentum shield at matched endpoint weights (P; refines #197#15)
- **Mechanism:** When task `B2` is announced before the current window `W` runs under a predeclared nonconstant schedule (warmup, cosine, or step drop), choose a permutation `π` of `W` that matches the default order's endpoint weights `θ_K` (within `ε`) while orienting `m_K` along an `A`-protective direction (`−∇L_A`), so `B2`'s first updates inherit restoring momentum without shifting the serving checkpoint `θ_K`.
- **Novelty vs nearest prior art:** Replay scheduling and curricula move `θ_K`; partial Adam reset ([2306.17833][reset]), [STABLE][stable], and [delayed transport][transport] alter optimizer updates or weights directly; [#197](batch-order-interventions.md) card 15 proposed the seed without pinning the schedule requirement or serving-boundary contract. The candidate primitive is a data-order-only, endpoint-neutral pre-shift shield.
- **Cheapest first test:** Two-task linear-ReLU MLP under Adam and heavy-ball with a predeclared 8-step linear warmup; exhaust or beam-search permutations of `W`; evaluate `A` after 10 and 50 `B2` steps against replay-last scheduling (free endpoints), Adam reset at shift, direct `m_K` write ([#185](slot-splices.md) card 01), EWC/STABLE damping, gradient accumulation at equal latency, and clock-matched Adam ([2606.29554][shuffle]).
- **Old-task retention check:** `A` (incl. rare slice) and `C` at every prefix of `W`, at `θ_K`, and after 10 and 50 `B2` steps at matched `B1`/`B2` gain and initial margins.

#### 02. Destructive-interference momentum cancellation against an announced shift gradient (P)
- **Mechanism:** Rather than blindly pointing `m_K` along `−∇L_A` (which behaves like generic replay-last), use one announced `B2` preview batch (or task gradient direction `g_{B2}`) to orient `m_K` specifically along `−P_A g_{B2}`—cancelling only the `A`-damaging component of `B2`'s initial shock while leaving `B2`'s `A`-orthogonal progress unopposed, at matched `θ_K`.
- **Novelty vs nearest prior art:** [GPM][gpm] and [FOGO][fogo] project gradients *during* `B2`; replay-last pushes along `−∇L_A` regardless of `B2`. Aiming pre-shift momentum to destructively interfere with `P_A g_{B2}` is a targeted, order-only analogue of orthogonal projection that requires zero optimizer modification during `B2`.
- **Cheapest first test:** Same 8-batch warmup world as card 01, with two `B2` variants that have identical `B2` loss curvature but orthogonal vs aligned `P_A g_{B2}`. Compare against replay-last, GPM during `B2`, and direct `−P_A g_{B2}` momentum write at matched `B2` gain.
- **Old-task retention check:** `A` (rare slice) and `C` at prefixes, after 10 and 50 `B2` steps, plus a **mismatched-announcement negative** (wrong `B2` preview) to verify the shield degrades gracefully.

#### 03. Dual-clock `(m, v)` preconditioned shield in Adam (P)
- **Mechanism:** Exploit Adam's two decay constants (`β_1 ≈ 0.9`, ~10-step memory; `β_2 ≈ 0.999`, ~1,000-step memory): order `W` (with mixed gradient magnitudes) so `m_K` cancels `B2`'s immediate ~10-step transient while `v_K` concentrates high second-moment energy on `A`-sensitive coordinates, damping them across ~100–1,000 `B2` steps—all at `ε`-matched `θ_K`.
- **Novelty vs nearest prior art:** [Matched Specialization][matched] and [PR #136](https://github.com/manojbajaj95/cl/pull/136) study `v` swaps; [#197](batch-order-interventions.md) card 16 studies `v`-only damping. Coupling fast `m_K` cancellation with slow `v_K` damping in one permutation addresses card 05's short-horizon decay critique; must beat `m`-only shield + `v`-only shield + direct `(m, v)` write + Fisher/STABLE damping.
- **Cheapest first test:** 8-batch window with mixed-norm gradients under Adam + warmup; measure `A` retention at steps 1, 10, 50, and 200 of `B2` against `m`-only, `v`-only, Adam reset, and direct `(m, v)` write at matched `B2` gain.
- **Old-task retention check:** `A`/`C` at prefixes and across steps 1–200 of `B2`, checking that elevated `v_K` does not stall `B2` learning on shared features.

#### 04. Nonlinear ReLU gate-barrier steering during `B2`'s initial transient (P)
- **Mechanism:** In a linear host, carried-over momentum `m_K` is algebraically equivalent to a decaying additive drift—hard to separate from one extra replay step. In a ReLU host, order `W` so `m_K` steers the early `B2` trajectory *around* an `A`-critical ReLU activation boundary during the first few steps, after which `B2`'s own gradients settle into a separate, `A`-preserving linear region permanently.
- **Novelty vs nearest prior art:** [Finite-safe-regions (PR #152)](https://github.com/manojbajaj95/cl/pull/152) searches weight updates that keep ReLU signs; here, momentum order deflects an *unmodified* `B2` optimizer around a gate barrier. If a linear host shows the same effect or a single replay step at `B2` start ties it, the nonlinear mechanism is falsified.
- **Cheapest first test:** Small 2-layer ReLU MLP (plus a matched linear-host negative control) where `B2` has two equally good basins on opposite sides of an `A`-critical gate boundary. Compare the momentum shield against Adam reset, 1-step `A` replay at `B2` start, and gradient accumulation.
- **Old-task retention check:** `A` (including gate-flip counts on rare slices) and `C` at prefixes and after 100 `B2` steps (must persist long after `β_1^t → 0`).

#### 05. Carryover half-life audit: does the shield survive past `t ≈ 1/(1−β_1)` steps? (I)
- **Mechanism:** Under fixed-`β_1` momentum, `m_K` decays geometrically as `β_1^t`, so its linear displacement saturates around `1/(1−β_1)` steps (~10 steps at `β_1 = 0.9`). Sweep `B2` horizon `T ∈ {5, 10, 25, 100}` and `β_1 ∈ {0.5, 0.9, 0.95}` to measure whether protective gains at step 10 persist or wash out by step 100.
- **Novelty vs nearest prior art:** Diagnostic only; prevents claiming long-horizon CL protection from a 10-step transient.
- **Cheapest first test:** Run card 01 and card 04 across the `(T, β_1)` grid on CPU; plot `A`-retention gap vs `T` alongside `β_1^T`.
- **Old-task retention check:** `A`/`C` at every checkpoint `T`, paired with `B2` loss to confirm retention is not just slowed `B2` progress.

#### 06. Serving-contract separation audit: matched-endpoint shield vs free-endpoint replay-last (I)
- **Mechanism:** Directly test the operational justification for "identical endpoint weights": measure the `A`/`B1`/`C` serving-time loss and margin drift that free-endpoint replay-last incurs at the boundary `θ_K`, versus the matched-endpoint shield. If free-endpoint replay-last barely hurts `B1` at `θ_K` and matches `A` after `B2`, the endpoint-neutral constraint is unnecessary and Seed #15 reduces to replay scheduling.
- **Novelty vs nearest prior art:** Mandatory interface audit for Seed #15; inherits the ledger's "ties a simple baseline" gate.
- **Cheapest first test:** On card 01's windows, compare Pareto fronts of `(B1 serving loss at θ_K, A retention after 10 B2 steps)` for free-endpoint replay-last, matched-endpoint shield, and direct `m_K` write.
- **Old-task retention check:** `A`/`C` at prefixes, at `θ_K`, and after `B2`, reporting worst-slice degradation at `θ_K`.

#### 07. Residual-weight and accumulation falsifier for `ε`-tolerance shields (I)
- **Mechanism:** Because constant-LR Adam appears injective on orders ([#197](batch-order-interventions.md) hand check 2), practical shields often allow `||θ_K(π) − θ_K(default)|| ≤ ε`. Run a **weight-only counterfactual** (launch `B2` from `θ_K(π)` with *default* or *reset* `(m_K, v_K)`) and a **gradient-accumulation arm**; any retention gain reproduced by the weight-only arm is a weight-shift artifact, not a momentum shield.
- **Novelty vs nearest prior art:** Mandatory control; echoes [PR #114](https://github.com/manojbajaj95/cl/pull/114) and [PR #123](https://github.com/manojbajaj95/cl/pull/123) twin-matching discipline.
- **Cheapest first test:** Sweep `ε ∈ {0, 10⁻⁴, 10⁻³, 10⁻²}` on card 01's Adam world and decompose total `A` gain into `weight-only` + `slot-only` + `interaction`.
- **Old-task retention check:** `A`/`C` after 10 `B2` steps for all four arms (default, weight-only, slot-only, full shield).

### B. Order-safety certificates against ordering attacks (Seed #19)

#### 08. Joint Birkhoff-dual order-safety certificate over a declared suffix (P; refines #197#19)
- **Mechanism:** Linearize the window's post-suffix `A`-damage `ΔL_A(π)` as a linear functional of the permutation matrix `P` via the optimizer's impulse weights and the declared `T`-step suffix Jacobian, plus an explicit second-order Hessian-Lipschitz remainder bound `R_2(η, W)`. Maximize the linearized damage over the Birkhoff polytope (`O(n³)` assignment LP). If `OPT_LP + R_2 ≤ δ`, emit the dual potentials `(u, v)` as an `O(n²)`-checkable proof that **no** permutation in `S_n` harms `A` beyond `δ`, allowing the window to run on an untrusted data pipeline; otherwise fall back to hash-pinned order.
- **Novelty vs nearest prior art:** [BRRR][brrr] runs adversarial order search; [Proof-of-Learning][pol] audits *after* training by replay; [FullCert][fullcert] and [BagFlip][bagflip] certify against *data-value* poisoning, not permutation-only slot attacks. [#197](batch-order-interventions.md) card 02 certifies infeasibility of a *desired* target; here the same duality becomes a proactive **pipeline admission certificate** for retention safety.
- **Cheapest first test:** Windows of `n = 6..10` on a small MLP with exhaustive `n!` ground truth and a BRRR-style adversarial order search. Report false-safe rate (must be `0` with `R_2`), certifiable-window fraction, and verification cost vs hash-pinning and PoL replay.
- **Old-task retention check:** `A` (incl. rare slice) and `C` under the worst adversarial order found by BRRR/exhaustion for every certified window, compared against the hash-pinned fallback.

#### 09. Coupled `(m, v)` fractional-ratio certificate for Adam (P)
- **Mechanism:** In Adam, an adversary can pass separate `m`-only and `v`-only marginal checks yet pick a permutation that places large opposing gradients early and small aligned gradients late—shrinking `v_K` while keeping `|m_K|` high so the effective step `|m_K| / √(v_K + ε)` blows up past `δ`. Certify `max_{P ∈ B_n} (cᵀ m_K(P))² / (v_K(P) + ε) ≤ δ²` via Dinkelbach / fractional-linear relaxation over the Birkhoff polytope (each step is a standard assignment LP in `P`) plus a second-order remainder bound.
- **Novelty vs nearest prior art:** Existing Adam stability bounds treat `m` and `v` independently or assume i.i.d. shuffling. Certifying the coupled `m / √v` ratio over permutations closes an Adam-specific BRRR attack vector that linear-slot certificates miss.
- **Cheapest first test:** Single- and multi-coordinate Adam windows of `n = 6..8` containing a planted `m`-safe/`v`-safe/`(m/√v)`-unsafe window (exhaustible). Compare coupled-ratio certificate against independent `m`/`v` bounds and exhaustive truth.
- **Old-task retention check:** Worst-case `A`/`C` drop after 10 `B2` steps under the adversarial order on windows passed by independent bounds vs those passed by the coupled certificate.

#### 10. Prefix-and-suffix order-safety certificate (ruling out mid-window excursions) (P)
- **Mechanism:** Endpoint-slot certification allows an attacker to front-load `A`-conflicting batches, cross a destructive ReLU gate mid-window, and mask the damage by window end. Extend card 08 to certify `max_{1 ≤ k ≤ K} ΔL_A(π_{1:k}) ≤ δ_pre` jointly with post-suffix safety, using a prefix-layered Birkhoff relaxation (or exact subset DP for `n ≤ 16`).
- **Novelty vs nearest prior art:** [PR #197](batch-order-interventions.md) card 13 uses subset DP to *find* a prefix-safe key; [PR #195](https://github.com/manojbajaj95/cl/pull/195) checks prefixes on a *chosen* partial order. Here the certificate proves **every** pipeline permutation is prefix-safe on an incoming window, with a tighter relaxation than naive per-prefix union bounds.
- **Cheapest first test:** ReLU MLP windows of `n = 6..10` with a planted mid-window gate-flip attack whose endpoint `(θ_K, m_K)` looks safe. Measure how often endpoint-only card 08 falsely certifies an unsafe window and whether the layered certificate catches 100% of them.
- **Old-task retention check:** Worst-prefix `A`/`C` and post-suffix `A`/`C` across all permutations.

#### 11. Minimal-fence partial-order fallback synthesized from a BRRR counterexample (P)
- **Mechanism:** When card 08 refuses a window, the Birkhoff LP's maximizing vertex (or rounded permutation) is an explicit adversarial order `π*` that breaks `A`. Instead of falling back to total hash-pinning (zero pipeline parallelism), iteratively add the minimal precedence edges `i ≺ j` (or coarse block barriers) that cut off `π*` until the linear-ordering relaxation certifies the remaining family of extensions.
- **Novelty vs nearest prior art:** [Safe-order-families (PR #195)](https://github.com/manojbajaj95/cl/pull/195) exports a partial order for a frozen bridge; CEGAR / cutting-plane synthesis is standard. The CL-specific object is **minimal pipeline restriction**: trading the fewest ordering degrees of freedom for a certified `A`-retention bound.
- **Cheapest first test:** Uncertifiable windows from card 08 (`n = 8`); measure the number of added edges needed to certify vs total pinning (`n−1` edges), the fraction of `n!` orders kept free, and solver time.
- **Old-task retention check:** Worst-case `A`/`C` over all remaining linear extensions of the fenced poset, verified exhaustively at `n = 8`.

#### 12. Certifiable-window fraction and marginal-vs-joint separation audit (I)
- **Mechanism:** Directly tests the two make-or-break numbers from flood-triage row 304: (1) on natural non-planted streaming windows, what fraction are actually certifiable at realistic `η, β, δ`? (2) how often does a window pass per-coordinate marginal checks yet fail jointly (Fixture 2's `W_unsafe`), and how often does a conservative sum-of-marginals bound falsely reject a jointly safe window (`W_safe`)?
- **Novelty vs nearest prior art:** Mandatory diagnostic; if natural windows are either 99% trivially safe under marginals or <5% jointly certifiable, card 08 is dead on arrival.
- **Cheapest first test:** 200 blind windows drawn from a 2-task MLP stream (plus Fixture 2's planted pair) at 3 `η` values and 3 `δ` levels; tabulate `{marginal-only, sum-of-marginals, joint Birkhoff, exhaustive}` pass/fail confusion matrices.
- **Old-task retention check:** Realized worst-order `A`/`C` drop in each cell of the confusion matrix.

#### 13. Shift-agnostic (adversarial-suffix) order-safety certificate (P)
- **Mechanism:** Card 08 assumes the post-window suffix `B2` is declared. When the next shift is **unannounced**, certify that no permutation of `W` moves `(m_K, v_K)` outside a safe ellipsoid `{m : mᵀ H_A m ≤ r²}` (or `||P_A m_K||_2 ≤ r`) that guarantees `ΔL_A ≤ δ` for *every* future suffix with gradient norm `≤ G`, by maximizing a convex quadratic over the Birkhoff polytope via SDP / spectral relaxation plus remainder bound.
- **Novelty vs nearest prior art:** Robust control / ellipsoidal reachability ([1709.07523][reach]) bounds state sets; applying it over the Birkhoff polytope removes card 08's need to know `B2` in advance, at the price of a tighter certifiable fraction.
- **Cheapest first test:** Compare certifiable-window fraction of shift-agnostic card 13 vs declared-suffix card 08 on the same 200 windows, tested against 10 unseen `B2` tasks.
- **Old-task retention check:** Worst-case `A`/`C` across all 10 unseen `B2` tasks under adversarial window ordering.

#### 14. Compositional multi-window safety accounting with `β^K` decay credit (P)
- **Mechanism:** A multi-window attacker can chain individually `δ`-safe windows so carryover momentum accumulates past a global `A` budget `Δ_tot`. Track a running carryover-budget certificate across windows `t = 1..M`: window `t`'s certified worst-case slot entry `b_t` decays as `β^K b_{t-1} + c_t`, allowing an untrusted pipeline to stay unpinned over a long stream as long as the decayed sum stays below `Δ_tot` (re-pinning only the rare windows where it would exceed the cap).
- **Novelty vs nearest prior art:** [Leakage-leases (PR #176)](https://github.com/manojbajaj95/cl/pull/176) accounts for additive proof budgets across edits; here the optimizer's own `β^K` forgetting provides **exponential credit replenishment**, turning per-window certificates into a streaming defense.
- **Cheapest first test:** 20-window stream with a multi-window BRRR adversary trying to stack small safe drifts; compare decay-credited accounting against naive additive budgets and per-window-only certification.
- **Old-task retention check:** Cumulative `A`/`C` retention across all 20 windows under the multi-window adversary.

### C. Pipeline, attacker, and verification interfaces

#### 15. Low-rank `A`-sketch order-safety certificates (sub-replay cost) (P)
- **Mechanism:** Building card 08 on full `d`-dimensional gradients costs `O(n d)`. Instead, project each batch's gradient onto an `r`-dimensional `A`-sensitive subspace `U_A` (`r ≪ d`, e.g. top `r` Fisher/Hessian eigenvectors of `A`) and bound the orthogonal residual `||g_i^⊥||` by a scalar norm term. Solve the Birkhoff LP in `O(n³)` on the `r`-dimensional sketch, making certification far cheaper than one replay pass or PoL verification.
- **Novelty vs nearest prior art:** [SPACE-LoRA][space-lora] and [GPM][gpm] use low-rank `A` subspaces to constrain updates; here the subspace compresses an **order-safety proof** with an explicit sound residual term so soundness never relies on zero off-subspace leakage.
- **Cheapest first test:** Sweep sketch rank `r ∈ {2, 4, 8, 16}` on card 08's MLP windows; measure certifiable-window fraction lost to the residual bound and wall-clock speedup vs full-gradient LP and hash-pinning.
- **Old-task retention check:** Zero false certifications on `A`/`C` (including rare `A` slices intentionally placed partially outside `U_A` to stress the residual bound).

#### 16. Banded-Birkhoff certificates for bounded distributed pipeline jitter (P)
- **Mechanism:** Real data loaders and distributed shard workers do not apply arbitrary `S_n` permutations; they reorder batches within a bounded arrival/straggler jitter `|π(i) − i| ≤ J`. Restrict the Birkhoff polytope to banded doubly-stochastic matrices (`P_{ij} = 0` for `|i − j| > J`), certifying safety against realistic pipeline nondeterminism while dramatically expanding the certifiable-window fraction over full `S_n`.
- **Novelty vs nearest prior art:** Banded assignment polytopes are standard; using jitter-bounded certification to unlock unpinned distributed training without losing `A`-retention guarantees is the candidate mechanism.
- **Cheapest first test:** Sweep `J ∈ {1, 2, 4, n−1}` on card 12's 200 blind windows; plot certifiable-window fraction vs `J` and verify against exhaustive banded-permutation search.
- **Old-task retention check:** Worst-case `A`/`C` over all `J`-banded permutations vs unbanded adversarial orders (verifying that out-of-band jitter is rejected at runtime).

#### 17. Counterexample-guided batch quarantine (evict-one-batch certification) (P)
- **Mechanism:** When a window fails card 08, inspect the dual witness / adversarial permutation `π*` to identify the single highest-leverage batch `b*` responsible for the violation. Quarantine *only* `b*` (defer it to a pinned side-step or accumulate it with a balancing batch) so the remaining `n − 1` batches immediately pass the order-safety certificate and run freely on the untrusted pipeline.
- **Novelty vs nearest prior art:** Extends [#197](batch-order-interventions.md) card 22 (minimal augmentation to make a target reachable) in the defensive direction: minimal *quarantine* to make a window certifiably safe. Must beat random/gradient-norm outlier dropping at equal quarantined fraction.
- **Cheapest first test:** On card 08's uncertifiable windows, compare dual-guided 1-batch quarantine against top-gradient-norm quarantine and exhaustive 1-batch leave-one-out on recovery of certifiability.
- **Old-task retention check:** `A`/`C` after running the certified `n−1` window freely plus the quarantined batch in its pinned slot, at matched total `B` gain.

#### 18. Certified-pipeline vs gradient-accumulation cost crossover audit (I)
- **Mechanism:** The ledger's bounded-delay kill notes that accumulating the whole window into one macro-batch removes order effects by construction at zero certification cost. Map the exact trade-off surface—step-count loss (fewer optimizer updates per window), memory/latency overhead of large-batch accumulation, and mid-window serving—to determine where certified unpinned ordering strictly dominates both accumulation and hash-pinning.
- **Novelty vs nearest prior art:** Mandatory audit; prevents building a certification stack for a regime where gradient accumulation wins outright.
- **Cheapest first test:** On a 2-task MLP stream with window sizes `n ∈ {4, 8, 16, 32}`, compare `B2` convergence speed, wall-clock cost, and worst-order `A` retention across (a) full-window accumulation, (b) hash-pinned order, and (c) card 08 certified unpinned pipeline.
- **Old-task retention check:** `A`/`C` at matched wall-clock and matched `B2` accuracy across all three arms.

#### 19. Adaptive curvature-attacker audit against linearized certificates (I)
- **Mechanism:** Give a BRRR-style attacker white-box access to the linearized Birkhoff certificate and optimize a permutation specifically to stay inside the linear bound while maximizing second-order curvature drift (`O(η²)` gradient-bracket `[∇g_i, g_j]` and ReLU flips) on `A`. Measures whether the remainder bound `R_2` is both sound (zero escapes) and non-vacuous (doesn't crush certifiable fraction).
- **Novelty vs nearest prior art:** Mandatory red-team audit; echoes [Smith et al.][smith] `O(η²)` brackets and [FullCert][fullcert] soundness testing.
- **Cheapest first test:** On nonlinear ReLU windows of `n = 8`, run gradient-bracket-maximizing adversarial search against card 08 with and without `R_2`, sweeping `η`.
- **Old-task retention check:** Worst-case `A`/`C` drop under the adaptive attacker; any certified window with `ΔL_A > δ` is a soundness failure.

### D. Unifying protective orders and certificates

#### 20. Jitter-robust protective orders: coarse block shields certified over within-block shuffles (P)
- **Mechanism:** Fuse Seed #15 and Seed #19: instead of shipping one fragile permutation as a momentum shield, partition `W` into `2–3` coarse buckets (e.g., early vs late block) and certify via a block-restricted Birkhoff LP that **every** within-bucket permutation delivers at least protective carryover `γ > 0` on `A` at `ε`-matched `θ_K`. The pipeline keeps within-bucket parallelism while still deploying a certified momentum shield.
- **Novelty vs nearest prior art:** Combines [#195](https://github.com/manojbajaj95/cl/pull/195) order families with Seed #15 shields and Seed #19 adversarial certification; must beat a single pinned shield + hash-pinning and free-endpoint replay-last.
- **Cheapest first test:** 8-batch warmup windows split into two 4-batch blocks (`4! × 4! = 576` legal orders); verify exhaustively that every legal realization protects `A` after 10 `B2` steps and beats default/reset/accumulation.
- **Old-task retention check:** Worst-case `A`/`C` over all `576` within-block shuffles, at prefixes and after `B2`.

#### 21. Dual-use window triage: one Birkhoff LP routes to free, fenced, or shielded (P)
- **Mechanism:** Run one pre-window Birkhoff LP per incoming window to compute both worst-case `A`-harm (certificate) and best-case `A`-protective carryover at matched `θ_K` (shield). Route each window automatically into one of three modes: *free* (certified safe, no shift announced), *fenced/quarantined* (unsafe without shift), or *shielded* (shift announced and protective margin exceeds threshold).
- **Novelty vs nearest prior art:** Unifies cards 01, 08, and 11 into a single controller; per the ledger's merge rule, must beat the stacked static controls (always hash-pin + always replay-last before shift + Adam reset) at equal total compute and latency.
- **Cheapest first test:** 30-window stream with 3 announced task shifts and an untrusted reordering pipeline; compare total pinning overhead, `B` progress, and `A` retention against the stacked static controls.
- **Old-task retention check:** `A` (rare slice) and `C` across all 30 windows and after every shift.

#### 22. Order-neutralizing re-batching: partition examples so every batch order certifies safe (P)
- **Mechanism:** When a pipeline's batch arrival order cannot be pinned (e.g., asynchronous or sharded workers), keep the same training examples and fixed batch size, but **re-partition** examples into batches whose `A`-projected gradients are balanced across batches (herding/stratified batching), so the resulting batch multiset passes card 08's order-safety certificate under **all** `n!` permutations.
- **Novelty vs nearest prior art:** [GraB][grab] reorders fixed batches to herd running sums; here we change **batch membership** (not batch order) to make the window *permutation-invariant* along `A`-sensitive directions, turning an uncertifiable window into a certifiably order-safe one without pinning the pipeline or changing the multiset of examples.
- **Cheapest first test:** Take uncertifiable 8-batch windows (e.g. 64 examples grouped into 8 batches) from card 12; re-partition the 64 examples by greedy `A`-gradient balancing into 8 equal-size batches; measure the jump in card 08 certifiable-window fraction and compare against random re-batching and gradient accumulation.
- **Old-task retention check:** Worst-case `A`/`C` over all `8!` orders of the re-batched window, plus `B` convergence speed (checking that balancing does not hurt `B` progress via reduced gradient diversity).

## Ranked deeper questions

1. **Does an order-only momentum shield at matched endpoint weights buy any `A` retention after 10+ `B2` steps beyond free-endpoint replay-last, partial Adam reset, STABLE/EWC damping, and gradient accumulation—and does the serving-boundary constraint (`θ_K` fixed) justify it?** Start with cards 06, 07, 05, and 04. Heavy-ball is locked at constant LR, `m_K` decays as `β_1^t`, and `ε`-tolerance shields risk being weight-shift artifacts. If the only durable win is nonlinear gate-barrier steering (card 04) or dual-clock `(m, v)` preconditioning (card 03), narrow Seed #15 strictly to those; otherwise retire it as an improvement.
2. **What fraction of natural streaming windows are jointly certifiable as order-safe with a rigorous second-order remainder bound, and how large is the marginal-vs-joint gap (both multi-coordinate and Adam's `m/√v` coupling)?** Cards 12, 08, 09, and 19. This decides whether Seed #19 is a real defensive primitive or either vacuous (too few windows certify once `R_2` is included) or redundant (simple marginals already decide almost every window).
3. **In what concrete training regime does certifying an untrusted pipeline (or synthesizing minimal fences / order-neutral batches) strictly beat hash-pinning the order everywhere or using gradient accumulation?** Cards 18, 11, 16, and 22. Without a regime where pinning or accumulation pays a real latency/throughput/convergence penalty that certification avoids, Seed #19 is a neat proof with no deployment edge.
4. **Can coarse block-level shields or order-neutral re-batching survive bounded distributed jitter and multi-window adversaries without losing `B` plasticity?** Cards 20, 14, and 22. Tests whether the two seeds reinforce each other in a realistic streaming pipeline rather than working only on isolated single windows.

**Verdict:** Seed #19 (**order-safety certificates**, cards 08–11, 16, 22) remains the stronger primitive candidate: it avoids the heavy-ball lock and `β_1^t` horizon limit, has a clean joint-vs-marginal separation (Fixture 2 and Adam's `m/√v` ratio), and extends naturally to minimal fences (card 11), banded pipeline jitter (card 16), and order-neutralizing re-batching (card 22). Seed #15 (**pre-shift momentum shields**, cards 01–04) faces three steep gates—the serving-contract check (card 06), the residual-weight falsifier (card 07), and the `β_1^t` half-life audit (card 05)—and should be falsified with those three before scaling, keeping nonlinear gate-barrier steering (card 04) and dual-clock `(m, v)` shields (card 03) as its sharpest surviving hypotheses. No pilot is launched here.

[bagflip]: https://arxiv.org/abs/2205.13634
[brrr]: https://arxiv.org/abs/2104.09667
[dp-backdoor]: https://arxiv.org/abs/2605.21780
[fogo]: https://arxiv.org/abs/2606.10406
[fullcert]: https://arxiv.org/abs/2406.11522
[gpm]: https://arxiv.org/abs/2103.09762
[grab]: https://arxiv.org/abs/2205.10733
[matched]: https://arxiv.org/abs/2610.15830
[ocl-opt]: https://arxiv.org/abs/2610.27835
[poison-cert]: https://arxiv.org/abs/2512.20865
[pol]: https://arxiv.org/abs/2103.05633
[reach]: https://arxiv.org/abs/1709.07523
[reset]: https://arxiv.org/abs/2306.17833
[shuffle]: https://arxiv.org/abs/2606.29554
[smith]: https://arxiv.org/abs/2101.12176
[space-lora]: https://arxiv.org/abs/2609.34453
[stable]: https://arxiv.org/abs/2611.10655
[stored]: https://arxiv.org/abs/2608.20442
[transport]: https://arxiv.org/abs/2608.24593
