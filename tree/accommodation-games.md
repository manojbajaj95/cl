# Accommodation games

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Finite edit guards](finite-edit-guards.md) ([PR #164](https://github.com/manojbajaj95/cl/pull/164)), cards 13 and 14. **Review seed:** [Flood triage row 262](https://github.com/manojbajaj95/cl/blob/abfa922e0ba87ea8cae758f17a1c8a8a0fd319d3/reviews/flood-triage.md#L262) kept two directions at 3: train a learner to reach states from which it always has a verified answer to any bounded foreign write (a winning strategy rather than a safe sequence), and publish the residual menu of writes still allowed after one write consumes room. Grading follows the [idea ledger](https://github.com/manojbajaj95/cl/blob/abfa922e0ba87ea8cae758f17a1c8a8a0fd319d3/reviews/idea-ledger.md).

**Is continual learning as a game against future editors a new object?** Not as a mathematical object. A finite-horizon two-player safety game where an adversary picks a bounded edit and the host answers from a finite move menu to keep an old-task floor is a discriminating kernel in viability theory, a backward reachable tube in [Hamilton–Jacobi reachability](https://arxiv.org/abs/1709.07523), a control-invariant set for [control barrier functions](https://arxiv.org/abs/1903.11199), or strong contingent planning on an AND–OR graph. Publishing the remaining safe edits after one write consumes room is a Brzozowski derivative (residual language) `e⁻¹L(s)` or a quotient contract `C / C₁` in assume–guarantee algebra ([Pacti](https://arxiv.org/abs/2303.17751)), whose equivalence relation over edit histories is already the Myhill–Nerode quotient tracked as top-10 #2 in the idea ledger. The continual-learning candidate is a *learned, reusable game-ready state and residual-menu interface*: while learning an ordinary useful task B, a learner lands inside a nontrivial K-round winning region `Win_K` and exports a compact, checkable residual menu so later, independently authored blind editors can commit and update the menu without re-running full game synthesis or seeing each other's private data. It earns primitive status only if it admits strictly more *useful frozen* multi-round edits—or matches admission at lower total verification, planning, and storage cost—than myopic finite guards plus online repair, generic contingent planning on the *exact same* move menu, and constrained continual learning with the same verifier. Renaming a safety game, shrinking the edit family to a trivial box, or granting extra response moves unavailable to controls does not establish a new primitive.

## What the game and residual menu promise

Let old tasks A and C have acquisition-anchored safe sets `Win_0 = { s : inf_{x ∈ D_A} m_A(s, x) ≥ τ_A and inf_{x ∈ D_C} m_C(s, x) ≥ τ_C }`, where `m` is a declared post-edit score (starting with signed classification margin and an explicit tie rule). At each round `k = 1, …, K`:

1. A blind foreign editor `E_k` picks a bounded write `e_k ∈ T_k(s_{k-1})` frozen before seeing the host's descendant state.
2. The host answers with a verified accommodation `a_k ∈ M(s_{k-1}, e_k)` from a fixed finite menu `M` (identical across all baselines, subject to a declared cost cap and preserving previously installed tasks `B, E_1, …, E_{k-1}`), yielding `s_k = a_k(e_k(s_{k-1}))`.

The K-round winning region is defined by backward induction with alternating quantifiers:

```text
Win_0 = S_A ∩ S_C
Win_k = { s ∈ Win_0 : ∀ e ∈ T(s), ∃ a ∈ M(s, e) such that a(e(s)) ∈ Win_{k-1} }
```

Atomic commit publishes `s_k` only after `a_k` completes; live-intermediate serving additionally requires `e(s) ∈ Win_0` before `a` runs. After a concrete round-1 transition `s_0 → s_1 = a_1(e_1(s_0))`, the exact residual admissible menu for round 2 is

```text
Res(s_1; M, Win_0) = { e_2 ∈ T(s_1) : ∃ a_2 ∈ M(s_1, e_2) with a_2(e_2(s_1)) ∈ Win_0 }.
```

A published residual artifact certifies a subset `R̂(s_1) ⊆ Res(s_1)` together with the host version, edit/state semantics (including optimizer slots if read or written), and checkable response proof. Unknown or timed-out checks never admit a write.

Two exact rational witnesses isolate why myopic guards, open-loop safe sequences, and scalar remaining budgets fail before any learning is claimed:

1. **Myopic max-margin picks a losing state; open-loop safe sequences have no solution.** Let two rare A slices have margins `m_1(t_1, q_1) = 1 − ReLU(t_1 − q_1)` and `m_2(t_2, q_2) = 1 − ReLU(t_2 − q_2)` with floor `τ = 1/2`, starting at `(t_1, t_2) = (0, 0)` and `(q_1, q_2) = (1/4, 1/4)`. In round 1, `E_1` adds `t_1 += 1`, and the host chooses between two equal-utility verified accommodations: `a_shift` sets `(q_1, q_2) = (3/4, −1/4)` (post-round-1 margins `3/4, 3/4`, worst margin `3/4`), while `a_hold` sets `(q_1, q_2) = (1/2, 1/4)` (margins `1/2, 1`, worst margin `1/2`). In round 2, `E_2` picks either `e_A: t_1 += 1/2` or `e_B: t_2 += 1`, and the host answers from `M_2 = { q_1 += 1/2, q_2 += 1/2 }`. From `a_shift`, `e_B` leaves best-response margin `1 − ReLU(1 − 1/4) = 1/4 < 1/2` (lost, despite beating `a_hold` on immediate worst margin). From `a_hold`, the reactive strategy `e_A ↦ (q_1 += 1/2)` and `e_B ↦ (q_2 += 1/2)` keeps both slices `≥ 1/2`. Yet no *open-loop* round-2 move from `a_hold` survives both `e_A` and `e_B` (`q_1 += 1/2` alone fails `e_B` at `1/4`; `q_2 += 1/2` alone fails `e_A` at `0`).
2. **Equal post-write margin, different residual menus.** Let a rare A slice have margin `m_A(u, v) = 1 − ReLU(u − 1/2) − ReLU(v − 1/2)` with floor `τ = 1/2`, starting at `(0, 0)`. Compare two round-1 writes: `w_1 = (3/4, 0)` (crosses gate `u`, leaves gate `v` with dormant buffer `1/2`) and `w_2 = (5/8, 5/8)` (crosses both gates). Both leave the exact same post-write margin `3/4` (remaining margin slack `1/4`). Test three round-2 candidates `T_3 = { d_u = (+1/2, 0), d_v = (0, +1/2), d_small = (+1/4, 0) }`: after `w_1`, the exact residual menu is `{ d_v, d_small }` (`d_v` keeps `m_A = 3/4` with zero extra loss); after `w_2`, the exact residual menu is `{ d_small }` (`d_v` drops `m_A` to `1/4 < 1/2`). Any scalar budget based on remaining margin makes the same call on `d_v` in both states—unsound after `w_2` or needlessly refusing `d_v` after `w_1`—and any isotropic norm budget cannot separate `d_u` and `d_v` (both norm `1/2`) after `w_1`.

## Closest controls and the common first test

- **Safety games, viability, and control:** [Hamilton–Jacobi reachability](https://arxiv.org/abs/1709.07523), [Control Barrier Functions](https://arxiv.org/abs/1903.11199), reactive GR(1) synthesis, and strong contingent planning already formalize `Win_K` and `Win_∞`. In CL, [Continual Learning through Control Minimization](https://arxiv.org/abs/2602.04542) casts preservation vs learning as control competition, [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) models recursive closure of stability–plasticity residuals, [Theory of Continual Learning Against Data Poisoning](https://arxiv.org/abs/2606.29841) studies adversarial streams, and [Stackelberg LHF](https://arxiv.org/abs/2512.16626) uses sequential-move games in preference alignment. Compare directly against myopic finite guards ([Finite edit guards](finite-edit-guards.md)), [InterContiNet](https://arxiv.org/abs/2206.07996), [APRNN](https://arxiv.org/abs/2304.03496) online repair, [Certified CL](https://arxiv.org/abs/2407.06697), [CABA](https://arxiv.org/abs/2610.40740), [La-MAML](https://arxiv.org/abs/2002.09571), and [OGD](https://arxiv.org/abs/1910.07104)/[GPM](https://arxiv.org/abs/2103.09762).
- **Residual menus and contract quotients:** [Pacti](https://arxiv.org/abs/2303.17751) already computes assume–guarantee quotients, [Mergeable writes](mergeable-writes.md) and [Precondition writes](precondition-writes.md) already package substitute menus and ordering prerequisites, and top-10 #2 in the ledger already tracks the Nerode quotient over future writes. Every residual-menu card must beat fresh exact verification from `s_1`, a scalar remaining-budget rule, and Pacti-style relational planning fed the same effect language.
- **First gate (proposed, CPU only):** Start from the two rational witnesses, then tiny piecewise-linear ReLU hosts with enumerable edit banks `T_1, T_2` and a **single frozen accommodation menu `M` shared identically by every arm**. Freeze blind editors `E_1, E_2, E_3` from a pre-provider reference before B commits; publish only the family specification, never the held-out payloads. Include no-crossing, trap-accommodation, residual-exhaustion, and impossible (`Win_2 = ∅`) cases. Match B utility, total parameter/adapter capacity, and A/C acquisition floors across arms. Score *useful frozen multi-round writes admitted* at identical worst-case A/C (and prior `B, E_1`) floors; charge backward-induction/training compute, verifier calls, stored certificate bytes, and inter-editor disclosure. Count solver `unknown` separately from `unsafe`, and audit normal A/C plus all previously installed tasks at every served prefix.

## Idea cards

### Reach states with a winning strategy

#### 01. Train B into the K-round winning kernel, not the 1-step safe set
- **Mechanism:** While learning B, optimize a sound differentiable lower bound on the K-round alternating minimax margin (`min_{e_1} max_{a_1} … min_{e_K} max_{a_K} m_A`) over development edit families and a declared finite menu `M`. Lock B, then certify membership in `Win_K` on a predeclared held-out family before blind editors arrive.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [InterContiNet](https://arxiv.org/abs/2206.07996) learns static nested boxes and [Finite edit guards](finite-edit-guards.md) card 02 learns 1-step guards; HJ reachability computes winning sets offline. The candidate is a learned K-round winning state that admits more blind multi-round frozen edits than 1-step guards or generic contingent planning from ordinary B at equal `M` and cost.
- **Cheapest first test:** Build a 2-round ReLU host containing Witness 1's trap. Compare ordinary B + APRNN repair, 1-step finite guard (PR #164 card 02), InterContiNet box training, generic 2-step contingent planning from ordinary B, and `Win_2`-trained B on held-out `E_1, E_2` banks.
- **Old-task retention check:** Certify A and C at acquisition floors after B, after `E_1` + `a_1`, and after `E_2` + `a_2` on every reachable branch, plus normal B and `E_1` accuracy.

#### 02. Separate reactive accommodation from static safe sequences
- **Mechanism:** On tiny ReLU hosts, solve both the closed-loop game `Win_K` (`∀ e ∃ a`) and the open-loop safe-sequence problem (`∃ a ∀ e`) over the exact same `T` and `M`, measuring how much extra useful frozen-edit admission comes strictly from observing `e_k` before choosing `a_k`.
- **Novelty vs nearest prior art — IMPROVEMENT:** Closed-loop vs open-loop control is classical. This is the required separation audit showing whether reactive accommodation buys real plasticity over static safe sequences (and confirming the gap collapses in an affine negative control).
- **Cheapest first test:** Enumerate Witness 1 plus an affine control where minimax duality holds; sweep gate density and menu size `|M|` on quarter-grid ReLU hosts at equal B utility.
- **Old-task retention check:** Exhaustively check A/C margins on every round-1 and round-2 leaf and verify that open-loop failures are real floor violations, not tie-breaking artifacts.

#### 03. Compile a compact accommodation policy alongside the weights
- **Mechanism:** Alongside the trained weights `s_0 ∈ Win_K`, export a small, independently checkable response map `π: (s, e) ↦ a ∈ M` (such as a gate-cell decision list) paired with a proof certificate. When blind `E_k` arrives, the host evaluates `π(s_{k-1}, e_k)` and checks only that one candidate instead of re-solving a K-step game tree.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Reactive synthesis already compiles strategies to finite controllers. The CL candidate is whether a learned weight-plus-policy artifact beats fresh online contingent planning and online APRNN repair on total verification work and admission on held-out editors.
- **Cheapest first test:** On a 2-round ReLU host with 8–16 candidate edits per round, compare compiled `π` + single-move check, fresh 2-step contingent planning, online APRNN, and a fixed default accommodation rule at equal bytes and verifier calls.
- **Old-task retention check:** Independently verify every move `π` outputs on A, C, B, and prior `E_1` before publication; reject if `π`'s precondition cell does not match the live state.

#### 04. Keep live-intermediate safety separate from atomic-commit winning
- **Mechanism:** Split the game into atomic mode (only `a_k(e_k(s_{k-1}))` is served) and live-intermediate mode (`e_k(s_{k-1})` is served before `a_k` runs, requiring `e_k(s_{k-1}) ∈ Win_0` as well as `a_k(e_k(s_{k-1})) ∈ Win_{k-1}`). Train B with a split-margin objective when live traffic cannot wait for accommodation.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Finite safe regions](finite-safe-regions.md) and [Finite edit guards](finite-edit-guards.md) card 16 already separate endpoints from served paths. Here it scopes the game's winning condition so an atomic-only strategy cannot claim safety under live intermediate serving.
- **Cheapest first test:** Construct a 2-round ReLU host where `e_1(s_0)` transiently crosses a gate and drops `m_A` below `τ` until `a_1` compensates. Compare atomic-only `Win_2`, live-intermediate `Win_2`, and shadow-copy buffering at equal memory.
- **Old-task retention check:** Audit A, C, and B at both `e_k(s_{k-1})` and `a_k(e_k(s_{k-1}))` for every round; record any transient floor violation as a failure in live mode.

#### 05. Play the game against an adaptive, not merely blind, future editor
- **Mechanism:** Replace the fixed frozen-delta adversary `e ∈ T` with a state-dependent editor operator `E_k(s)` (for example, one clipped gradient step on a hidden task `D_k` evaluated at `s`), turning the interaction into a Stackelberg feedback game where `a_k` can reshape gradients so `E_{k+1}(s_k)` takes a less destructive step.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [La-MAML](https://arxiv.org/abs/2002.09571) anticipates gradient updates without safety guarantees, [Stackelberg LHF](https://arxiv.org/abs/2512.16626) plays a leader–follower game on preferences, and [Finite edit guards](finite-edit-guards.md) card 06 types a single update rule. Combining state-dependent editor operators with verified multi-round accommodation tests whether steering *what the next editor wants to write* beats defending against an arbitrary delta ball.
- **Cheapest first test:** Use a 2-round toy host where `E_1, E_2` are deterministic 1-step clipped SGD updates on held-out linear/ReLU tasks. Compare frozen-delta-ball `Win_2`, operator-aware Stackelberg `Win_2`, La-MAML + verifier, and online APRNN at equal `M`.
- **Old-task retention check:** Replay the exact unmodified `E_1, E_2` update rules on the committed host and verify A, C, B, and `E_1` floors after every step; never substitute hand-picked deltas.

#### 06. Build a self-replenishing accommodation move (infinite-horizon viability)
- **Mechanism:** Include a costed "re-buffer" move in `M` that shifts unused hidden capacity to restore dormant gate thresholds without changing current A/C/B outputs, and train B into a control-invariant (viability) kernel `Win_∞` from which every bounded edit can be returned to `Win_∞` rather than exhausting slack after K rounds.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Viability kernels and [Control Barrier Functions](https://arxiv.org/abs/1903.11199) are known in control; [Control Minimization](https://arxiv.org/abs/2602.04542) handles continuous regularization. The CL candidate is whether a learned weight-space viability kernel with a fixed re-buffer move sustains unbounded streams of useful bounded edits at fixed capacity without collapsing into periodic full retraining.
- **Cheapest first test:** Run a 6-round stream on a 4-unit ReLU host with bounded per-round edits and a costed re-buffer move in `M`. Compare fixed-horizon `Win_2`, viability-trained `Win_∞`, periodic replay, and frozen expansion at equal capacity and compute.
- **Old-task retention check:** Verify A, C, and a sliding window of installed edits at every round and confirm that the re-buffer move itself preserves all old outputs and rare slices exactly.

#### 07. Play the accommodation game with partial observation of the foreign edit
- **Mechanism:** When `E_k` applies an opaque write (such as a quantized or black-box adapter) whose effect is observed only through a bounded probe transcript `y = P(e_k(s))`, solve the belief-state safety game: train B so every pair of foreign writes indistinguishable under `P` admits a *single* shared verified accommodation `a(y) ∈ M`.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Partially observable safety games are studied in formal methods, and [PR #107](https://github.com/manojbajaj95/cl/pull/107) showed linear assays admit retention counterfeits. The CL candidate is training a host whose accommodation menu is insensitive to probe-indistinguishable write differences without needing full white-box weight inspection.
- **Cheapest first test:** Pair two writes that match on a small probe set `P` (using PR #107's counterfeit construction) while differing on a rare A slice. Compare white-box contingent planning (ceiling), belief-state `Win_2` with shared `a(y)`, and naive probe-conditioned repair.
- **Old-task retention check:** Verify A and C on both true and counterfeit writes in every equivalence class of `P`; refuse admission whenever two writes in the same transcript class have no common safe accommodation.

### Publish and update residual menus after room is spent

#### 08. Compile a gate-indexed residual menu after each concrete edit
- **Mechanism:** After concrete round-1 moves `(e_1, a_1)` land, propagate the guard only across gate cells whose slack or activation sign changed—computing the exact Brzozowski residual `R̂(s_1) ⊆ Res(s_1)`—and publish `R̂(s_1)` with a checkable membership certificate so blind `E_3` commits by inclusion check rather than fresh verification.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** This directly develops PR #164 card 13 and row 262's second score-3 idea. Brzozowski derivatives and [Pacti](https://arxiv.org/abs/2303.17751) quotients are known algebra; the CL candidate is a compact gate-indexed residual that beats fresh verification from `s_1` and scalar budgets on useful blind `E_3` admission per unit total cost.
- **Cheapest first test:** Implement Witness 2 and a 4-gate ReLU host with 16 frozen `E_3` payloads. Compare gate-indexed residual update, fresh exact verification from `s_1`, scalar remaining-margin/norm rules, and PR #164 card 17 dependency slices.
- **Old-task retention check:** Independently audit every `E_3` admitted by `R̂(s_1)` on A, C, B, and `E_1`; check that zero unsafe writes slip past the residual and report false-rejection rate vs exact `Res(s_1)`.

#### 09. Expose a trade-off frontier of residual menus instead of one post-edit state
- **Mechanism:** When two round-1 accommodations `a_1, a_1' ∈ M` achieve identical immediate A/C/B/`E_1` utility but yield incomparable residual menus `R̂(s_1)` vs `R̂(s_1')` (one keeps direction `u` open, the other keeps `v` open), retain a small Pareto frontier of certified candidate states—or defer committing `a_1` until `E_3`'s family is declared—rather than locking into one residual prematurely.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Mergeable writes](mergeable-writes.md) offers substitute menus at write time; this extends substitute menus *across rounds* to post-accommodation states so future editors pick which residual capacity to consume.
- **Cheapest first test:** Build a 2-round ReLU host with two orthogonal rare slices where `a_1` protects `u` and `a_1'` protects `v`, then draw a blind `E_3` needing either `u` or `v`. Compare single myopic `a_1`, single minimax-volume `a_1`, a 2-state residual frontier, and exact 2-step joint planning (ceiling) at equal storage.
- **Old-task retention check:** Verify every frontier state on A, C, B, and `E_1` before deferral and audit the chosen branch after `E_3` commits; charge the full byte cost of storing the frontier.

#### 10. Quotient residual menus by future-game equivalence (game-theoretic Nerode classes)
- **Mechanism:** Compress published residual menus by merging post-edit states that induce the same K-round winning strategies over `T` (safety-game bisimulation / game-Nerode quotient) instead of exporting raw parameter envelopes, testing whether equivalence classes beat parameter boxes at equal bytes.
- **Novelty vs nearest prior art — IMPROVEMENT:** Top-10 #2 in the idea ledger already defines the Nerode quotient over future writes, and bisimulation quotients are standard in verification. This tests whether quotienting by *controlled* game futures saves bytes over parameter-box residuals ([InterContiNet](https://arxiv.org/abs/2206.07996)).
- **Cheapest first test:** On an enumerable finite-state ReLU host, compare raw parameter-box residuals, static Nerode classes (no accommodation `M`), game-Nerode classes (with `M`), and exact verification at matched certificate byte budgets.
- **Old-task retention check:** Verify that any two states merged into one game-Nerode class have identical verified safety outcomes under every `e_2 ∈ R̂` and its paired `a_2 ∈ M` on A, C, and B.

#### 11. Charge each edit for the residual-menu volume it destroys, not its weight norm
- **Mechanism:** When `E_1` proposes a small menu of equal-utility candidate writes (as in [Mergeable writes](mergeable-writes.md)), admit the candidate that leaves the largest certified residual menu `R̂(s_1)` for held-out `E_2` families, rather than the smallest `‖Δθ‖` or highest immediate margin.
- **Novelty vs nearest prior art — IMPROVEMENT:** Option-value selection was raised in [Finite safe regions](finite-safe-regions.md) card 15. Here it is specialized to exact certified residual menus so Witness 1 and Witness 2's margin/norm traps are tested directly.
- **Cheapest first test:** Give `E_1` two equal-utility writes matching Witness 2 (`w_1 = (3/4, 0)` vs `w_2 = (5/8, 5/8)`), then evaluate a frozen held-out `E_2` bank. Compare minimum-norm, maximum-immediate-margin, residual-volume selection, and exhaustive 2-step planning.
- **Old-task retention check:** Check A, C, B, and `E_1` after round 1 and after every admitted `E_2`; ensure `E_1`'s utility is strictly matched across its menu options.

#### 12. Factor residual menus across independent editors via contract quotients
- **Mechanism:** When two concurrent blind editors `E_2, E_3` arrive with independent private tasks, split `Win_2(s_0)` into a [Pacti](https://arxiv.org/abs/2303.17751)-style quotient `R_2 × R_3 ⊆ Win_2` (handling signed bilinear cross-terms as in [Finite edit guards](finite-edit-guards.md) witness 2) so `E_2` picks from `R_2` and publishes the tightened residual `R_3' = Win_2 / e_2` without seeing `E_3`'s payload.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Contract quotients are standard in Pacti and additive escrow is standard in databases. The CL candidate is whether a learned host state admits a nontrivial factored residual across blind neural editors that beats serial verify-then-reverify and scalar escrow at equal disclosure.
- **Cheapest first test:** Extend PR #164 witness 2 to two sequential blind editors `E_2, E_3` with a signed cross-term. Compare serial verify-then-reverify, scalar escrow split, Pacti relational planning fed the same offers, and factored residual menus; include a planted sign-flip pair.
- **Old-task retention check:** Audit A, C, B, `E_2`, and `E_3` in both commit orders and verify that sign-flipped pairs are refused even when magnitudes match.

#### 13. Attach a residual-expiry witness when an unadvertised write breaks the menu
- **Mechanism:** Bind every published residual menu `R̂(s_1)` to a checked invariant over the dormant gate thresholds and optimizer slots it depends on. If an intervening uncertified write shifts a dormant gate while leaving all passive old outputs unchanged, emit a minimal counterexample invalidating `R̂(s_1)` before `E_3` commits.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Finite edit guards](finite-edit-guards.md) card 17 tracks dependency slices for 1-step proofs; here the target is stale residual menus across multi-round games where passive output checksums look clean.
- **Cheapest first test:** Interleave an output-preserving dormant-gate shift (PR #164 witness 1) between `s_1` and `E_3`. Compare passive output checksums, full re-verification from scratch, and gate-threshold expiry witnesses at equal check cost.
- **Old-task retention check:** Confirm that every invalidated residual blocks `E_3` until re-proved, and that zero unsafe `E_3` writes pass when dormant thresholds move while passive A/C logits stay identical.

#### 14. Learn a conservative residual predictor with a certified fallback
- **Mechanism:** Train a fast neural or piecewise-linear surrogate to propose a candidate residual subset `R̃(s_1)` after `(e_1, a_1)`, then run an exact soundness verifier only on `R̃(s_1)` (shrinking it on counterexamples) so every published residual is sound while avoiding full backward reachability over all of `T`.
- **Novelty vs nearest prior art — IMPROVEMENT:** Surrogate-guided verification and [Certified CL](https://arxiv.org/abs/2407.06697) incremental certification are known. The test is whether a learned residual proposer beats a fixed scalar shrink rule and direct verification of `T` on wall-clock cost per admitted useful `E_3` write.
- **Cheapest first test:** On a 10-gate ReLU host with 32 frozen `E_3` candidates, compare direct verification of all 32, a scalar shrink heuristic + check, and a surrogate proposer + exact soundness check at equal wall-clock budget.
- **Old-task retention check:** Require 100% soundness on A, C, B, and `E_1` for every published residual (surrogate guesses never authorize a write without the exact check) and track false-rejection rate.

### Game-theoretic structure of multi-round continual learning

#### 15. Trade pre-emptive reshaping against reactive accommodation at fixed budget
- **Mechanism:** Split a fixed total weight-change/compute budget between *pre-emptive* reshaping during B training (before `E_1` is revealed) and *reactive* accommodation `a_1 ∈ M` (after `E_1` is revealed), measuring the exact value of waiting in nonlinear ReLU hosts.
- **Novelty vs nearest prior art — IMPROVEMENT:** Value of information in two-stage stochastic/robust optimization is classical. In CL it isolates when proactive robust training ([InterContiNet](https://arxiv.org/abs/2206.07996)) wastes capacity defending against edits that never happen, versus when reactive-only repair ([APRNN](https://arxiv.org/abs/2304.03496)) arrives too late after a gate collapses.
- **Cheapest first test:** Sweep the proactive/reactive budget split `α ∈ {0, 0.25, 0.5, 0.75, 1}` on a 2-round ReLU host with 4 possible `E_1` directions at fixed total update norm and FLOPs.
- **Old-task retention check:** Evaluate worst-case A/C retention and normal B/`E_1` accuracy at every `α`, including live-intermediate checks when `α < 1`.

#### 16. Turn a failed accommodation into a minimal counter-strategy tree for the next B
- **Mechanism:** When backward induction proves `s ∉ Win_K`, extract the adversary's minimal winning counter-strategy `(e_1*, …, e_K*)`—a short game tree witnessing why every legal accommodation sequence fails—and feed it back into B's training objective, generalizing CEGIS from single-step counterexamples to multi-round game trees.
- **Novelty vs nearest prior art — IMPROVEMENT:** [SpecRepair](https://arxiv.org/abs/2106.01917) and [Finite edit guards](finite-edit-guards.md) card 18 already use 1-step counterexamples; counter-strategy synthesis is known in reactive synthesis. The test is whether multi-round counter-strategy trees transfer to held-out editor families better than 1-step counterexample replay at equal verifier calls.
- **Cheapest first test:** On a 2-round ReLU host where 1-step guards pass but 2-step traps fail, compare 1-step counterexample replay, random 2-step edit sampling, and minimal counter-strategy tree training on held-out `E_1, E_2` banks.
- **Old-task retention check:** Certify A, C, and B on held-out editor families after training; never allow counter-strategy caches to substitute for exact verification at commit time.

#### 17. Protect previously installed foreign writes as new players in the game
- **Mechanism:** Once `(e_1, a_1)` installs task `E_1`, fold `E_1`'s own floor `S_{E_1}` into the winning condition `Win_0' = S_A ∩ S_C ∩ S_{E_1}` for round 2, testing whether a learner can synthesize a *growing-objective* winning strategy where each admitted editor becomes a protected old task without driving the residual menu to empty.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Standard safety games assume a fixed target set `Win_0`, whereas real continual learning adds a new retention obligation every round. This isolates the exact tension between growing obligations and nontrivial residual menus at fixed capacity.
- **Cheapest first test:** Run a 3-round ReLU game where each admitted `E_k` adds one rare slice to `Win_0`. Compare fixed-objective `Win_K` (which lets `E_2` erase `E_1`), growing-objective `Win_K`, frozen-adapter expansion at equal parameter cap, and full multi-task retraining ceiling.
- **Old-task retention check:** Check A, C, B, and every previously admitted `E_1, …, E_{k-1}` at every round; report both worst-task floor and fraction of rounds where `R̂(s_k)` remains nonempty.

#### 18. Separate accommodation games in weights from accommodation in optimizer state
- **Mechanism:** When `E_k` is a stateful gradient editor (SGD+momentum or Adam), allow `a_k ∈ M` to adjust optimizer preconditioners (`v`, damping) alongside weights, testing whether stateful accommodations win multi-round games where weight-only accommodations fail—while preventing stale momentum from leaking into old tasks.
- **Novelty vs nearest prior art — IMPROVEMENT:** Optimizer resets ([2306.17833](https://arxiv.org/abs/2306.17833)), [PR #136](https://github.com/manojbajaj95/cl/pull/136) (momentum fossils), and [PR #141](https://github.com/manojbajaj95/cl/pull/141) (delayed-release edits) already study optimizer-state effects. Here the question is strictly whether adding optimizer-slot moves to `M` enlarges `Win_K` for stateful editors over weight-only `M` plus optimizer reset.
- **Cheapest first test:** Use a 2-round stateful Adam editor on a tiny ReLU host; compare weight-only `M`, weight-only `M` + full optimizer reset, and weight+preconditioner `M` on the same frozen task stream.
- **Old-task retention check:** Verify A, C, B, and `E_1` both immediately after `a_k` and after a neutral follow-up step that flushes any remaining momentum/preconditioner state.

### Try to erase the novelty

#### 19. Compile the accommodation game into standard contingent planning + verifier
- **Mechanism:** Express the exact state space, edit family `T`, accommodation menu `M`, and safety floors as a standard K-step AND–OR contingent planning problem with an exact verifier and no learned game-specific representation. If ordinary planning matches multi-round admission and total paid work, "accommodation games" is a restatement, not a new CL primitive.
- **Novelty vs nearest prior art — IMPROVEMENT:** Direct compile-away null hypothesis (parallel to PR #164 card 20). Any surviving primitive claim must beat this baseline on total cost or held-out blind-editor admission.
- **Cheapest first test:** Run cards 01, 03, and 08 head-to-head against generic K-step AND–OR planning on identical quarter-grid ReLU hosts, identical `M`, and identical frozen editor banks.
- **Old-task retention check:** Require exact acquisition-floor parity on A, C, B, and `E_1` at every served prefix across both implementations; no average-case relaxation.

#### 20. Audit menu inflation: freeze M identically across every baseline
- **Mechanism:** Enforce a strict control where every accommodation move `a ∈ M` (bias shift, rank-1 compensation, re-buffer) available to the game learner is also granted to myopic guards and online APRNN repair; test whether the game's advantage disappears once baselines get the same moves.
- **Novelty vs nearest prior art — IMPROVEMENT:** Experimental fairness audit preventing a classic confound where a new framework wins only because it secretly enlarged the action space.
- **Cheapest first test:** On Witness 1 and a 4-unit ReLU host, run myopic guard + online APRNN with `M = ∅` vs with full `M`, alongside `Win_2`-trained B with the same `M`.
- **Old-task retention check:** Audit A, C, B, and `E_1` at every round under identical `M` and identical per-round cost caps; flag any arm that exceeds `M`'s declared budget.

#### 21. Measure the bit lower bound of an exact residual menu
- **Mechanism:** Construct a host with `n` independent dormant gates where each round-1 write crosses an arbitrary subset `S ⊆ {1, …, n}` of gates, making the exact round-2 residual menu encode `S` (`n` bits). Any standalone residual summary answering all round-2 queries without host access therefore requires `≥ n` bits in the worst case, pinning down when compact residuals must rely on structured edit families or abstention.
- **Novelty vs nearest prior art — IMPROVEMENT:** Indexing lower bound (parallel to PR #164 card 19), not a new proof method; sets a hard floor on standalone residual compression.
- **Cheapest first test:** Enumerate all `2^n` gate-crossing patterns for small `n`; compare a packed `n`-bit exact residual, structured low-rank residual menus, scalar budgets, and bounded interactive host queries (charging host queries separately).
- **Old-task retention check:** Every admitted round-2 write must satisfy exact A/C floors on all `n` rare slices and normal inputs; report false-rejection and `unknown` rates as a function of bit budget.

#### 22. Force a finite-horizon exhaustion trap and demand honest refusal
- **Mechanism:** Construct a 2-round game where every legal B state belongs to `Win_1` (survives any single write) yet `Win_2 = ∅` (no strategy survives two rounds at fixed capacity and floors). Demand a checked infeasibility proof of `Win_2 = ∅`—distinguished from solver `unknown`—rather than silently relaxing A/C floors or narrowing `T` to trivial no-ops.
- **Novelty vs nearest prior art — IMPROVEMENT:** Infeasible-core / counter-strategy extraction is known; this is the mandatory negative control against claims that accommodation games make arbitrary continual streams safe at fixed capacity.
- **Cheapest first test:** Tighten the capacity/slack cap in Witness 1 so every `s ∈ Win_1` has an adversary winning move in round 2. Compare myopic 1-round guards (which falsely accept round 1), fail-closed backward induction, and equal-capacity frozen expansion.
- **Old-task retention check:** Confirm A and C stay at acquisition floors on the unchanged live host and that no uncertified round-2 promise or weakened floor is ever published.

## Ranked deeper questions

1. **Can learning into `Win_K` beat myopic guards, online repair, and generic contingent planning on blind multi-round editors?** Start from Witness 1, then cards 01–03 against the compile-away and menu-inflation controls (cards 19–20). Demand strictly more *useful frozen* multi-round writes—or equal admission at lower total verification, planning, and storage cost—with the exact same `M`, capacity, and A/C floors. A tie with generic contingent planning on the same learned state demotes the game framing to engineering.
2. **Does a published residual menu `R̂(s_1)` buy real reuse beyond scalar budgets and fresh re-verification?** Start from Witness 2, then cards 08–09, 11–12, and the bit lower bound (card 21). Test whether gate-indexed residuals or small residual frontiers admit strictly more blind `E_3` writes per unit total cost than fresh verification from `s_1`, scalar remaining-budget rules, and Pacti relational planning fed the same offers.
3. **Can growing-objective and self-replenishing games avoid multi-round exhaustion at fixed capacity?** Cards 06, 15, 17, and 22 ask whether `Win_K` stays nontrivial once each admitted foreign write becomes a protected old task—or whether capacity exhaustion forces either frozen expansion or trivial menus.
4. **What changes when future editors are adaptive or only partially observed?** Cards 05, 07, and 18 test whether state-dependent gradient editors, opaque black-box writes, and stateful optimizer slots separate continual-learning accommodation games from classical frozen-delta safety games, or whether worst-case delta balls plus optimizer resets already capture the usable headroom.
