# Partner-targeted folds: minimizing certified merge interaction and super-additive joint refunds

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Fold-earned merge headroom](https://github.com/manojbajaj95/cl/blob/devin/1795563441-fold-earned-headroom/tree/fold-earned-headroom.md) ([PR #193](https://github.com/manojbajaj95/cl/pull/193)), cards #02, #05, and #01. **Review seed:** [Flood triage row 301](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L301) ([PR #6](https://github.com/manojbajaj95/cl/pull/6)) keeps two ideas at score 3: (#02) among function-preserving folds of branch `i`, pick the one minimizing the certified sum of mixed merge residuals `J` over committed partners rather than network width, with freed slots only a by-product; (#05) when two spent gates are foldable jointly (#183#14), test whether the joint fold's drop in `J` is super-additive over the sum of partial folds; both governed by per-partner credit (#01). **Grandparents:** [Cross-pool round 46](https://github.com/manojbajaj95/cl/blob/devin/1795537860-merged-ideas/ideas/flood/cross-pool-46.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36), MNS2), [neutral groups](https://github.com/manojbajaj95/cl/pull/183) (#183, cards #06 and #14), [merge-aware budgets](https://github.com/manojbajaj95/cl/pull/181) (#181, card #14), and [merge-weight ranges](https://github.com/manojbajaj95/cl/pull/189) (#189, card #16). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Four ledger rules constrain this node: (1) *coded merge interference* was killed because a fitted pairwise surrogate is BOCS and gradient-free search ties it, so no card may substitute a fitted interaction surrogate for a certified `J` bound; (2) the [retention-matched plasticity reserve rerun](https://github.com/manojbajaj95/cl/pull/21) collapsed next-task spread to 0.09 MSE points, so fold-selection policies must pass a real admission-spread gate before ranking; (3) the [replay-deadline kill](https://github.com/manojbajaj95/cl/pull/113) found smooth decay with no cliff, so every piecewise-linear ReLU fold gain faces a smooth-activation control; (4) every merged/composed idea must beat the union of its parts' best baselines stacked at equal compute, proof bytes, and old-task retention floors, and every card is marked **P** (candidate primitive) or **I** (improvement/audit).

## Is partner-targeted, super-additive folding a new object for continual learning?

**Not as compression, permutation alignment, or task-vector shaping.** [Neuron Merging](https://arxiv.org/abs/2010.13160), [Net-Trim](https://arxiv.org/abs/1611.05162), [ZipIt!](https://arxiv.org/abs/2305.03053), and [PackNet](https://arxiv.org/abs/1711.05769) fold or free units to minimize width or reconstruction error. [Git Re-Basin](https://arxiv.org/abs/2209.04836) and [C²M³](https://arxiv.org/abs/2405.17897) optimize neuron *permutations* across models to lower linear mode-connectivity barriers, and [Symmetry in Neural Network Parameter Spaces](https://arxiv.org/abs/2506.13018) surveys parameter symmetries; none treats non-permutation absorption or splitting under exact solo equivalence as a certified liability-reduction move against committed partners. [CoFiMA](https://arxiv.org/abs/2312.08977), [FedSEAM](https://arxiv.org/abs/2610.33496), [ChainLoRA](https://arxiv.org/abs/2610.00431), and [Orthogonal Yet Coupled](https://arxiv.org/abs/2609.37564) shape or decouple task vectors directly (changing solo parameters or outputs), whereas [LR-Merge](https://arxiv.org/abs/2611.25000) forecasts merge interference with a receiver-local affine surrogate that is not a sound bound across gate flips, and [TwistedMerge](https://arxiv.org/abs/2607.20887) / [HR-Merge](https://arxiv.org/abs/2611.27377) certify alignment consistency or validate fallback accuracy rather than old-task interaction bounds. [ReluDiff](https://arxiv.org/abs/2001.03662), [IBP](https://arxiv.org/abs/1810.12715), and [Certified CL](https://arxiv.org/abs/2407.06697) supply the verification machinery.

**Conditional primitive:** a *partner-indexed, super-additive fold operator* over the exact solo-equivalence fiber `ℰ(Δᵢ) = {Δᵢ′ : f(θ₀ + Δᵢ′) = f(θ₀ + Δᵢ) on Dᵢ}`. Moving within `ℰ(Δᵢ)` is invisible to branch `i`'s own tasks and retention probes, yet it changes the certified two-branch (or multi-branch) mixed residual `J(Δᵢ′, Π)` differently for each committed partner class `Π`. Two properties make this more than width compression: (1) **width and partner interaction oppose each other** — the width-minimal fold can strictly *worsen* committed `J` while a width-neutral or width-increasing split strictly lowers it (Witness 1); (2) **joint absorption is super-additive in certified `J`** — folding a subset `S` of spent gates jointly into a low-drift carrier can drop `J` by strictly more than the sum of feasible, individually profitable partial folds (Witness 2). The object is a primitive only if partner-targeted + joint fold selection with non-fungible per-partner credit yields strictly more useful merged admissions per unit of search and proof cost than width-minimal folding + `#181#14` interaction-only rotation + exact joint recertification + merge-and-prune stacked together.

### Contract

- **Equivalence fiber and mixed residual.** Inherit #193's two-branch sum bound `d_merge ≤ b₀ + qᵢ + qⱼ + Jᵢⱼ`, where `J(Δᵢ, Δⱼ) = sup_{x ∈ D} |f(θ₀ + Δᵢ + Δⱼ)(x) − f(θ₀ + Δᵢ)(x) − f(θ₀ + Δⱼ)(x) + f(θ₀)(x)|` over the declared merge domain `D` (old protected domains `P`, both new-task probes, and the declared suffix). A fold `F : Δᵢ ↦ Δᵢ′` is legal iff `f(θ₀ + Δᵢ′) = f(θ₀ + Δᵢ)` identically on the common refinement of activation cells covering `Dᵢ` (or on a declared `D_fold ⊇ Dᵢ` with an explicit boundary guard).
- **Per-partner credit vector.** For committed partner classes `Π₁, …, Π_K`, a fold `F` issues a signed credit vector `r(F) = (U_k − U′_k)_{k=1}^K`, where `U_k ≥ sup_{Δⱼ ∈ Π_k} J(Δᵢ, Δⱼ)` and `U′_k ≥ sup_{Δⱼ ∈ Π_k} J(Δᵢ′, Δⱼ)` are sound certified bounds. Credits are **non-fungible across partners**: positive credit on `Π₁` never offsets a negative debit (`U′_k > U_k`) on `Π₂` unless `Π₂` explicitly holds spare slack or receives a paired compensating move.
- **Super-additivity definition.** For a set of spent gates `S`, a joint fold `F_S` is *liability-super-additive* against `Π` iff `ΔJ(F_S, Π) > ∑_{g ∈ S} max_{F_g ∈ ℱ_g} ΔJ(F_g, Π)`, where `ℱ_g` is the set of legal single-gate folds of `g` (with `max ∅ = 0`). The strongest test requires `ℱ_g ≠ ∅` and `ΔJ(F_g, Π) > 0` for each `g ∈ S`, separating *liability* super-additivity from #183#14's *feasibility* jump.
- **No manufactured credit.** Never move `θ₀`, shrink `D`, drop a committed partner from `{Π_k}`, substitute a fitted surrogate for `U_k`, or double-count freed width as interaction credit. Charge all search calls, verification calls, receiver range consumed, staging width, and ledger bytes.

### Two exact paper witnesses

Both were checked numerically on a dense grid (`10⁻⁴` spacing, exact to `10⁻¹⁵` on these piecewise-linear networks).

**Witness 1 — Width-minimal folding worsens committed interaction; partner-targeted and split folds win.** One input `x`, merge domain `D = [−1, 4]`, old protected domain `P = [−1, 1]`. Base `θ₀` has three ReLU units: live receiver `r₁ = [x − 2]₊` (readout `1`), dormant receiver `r₂ = [x − 2]₊` (readout `0`), and dormant gate `g = [x − 2]₊` (readout `0`). Branch `i` installs its skill on `g` (`w_g: 0 → 1`; active width `2`). Three committed partners, each harmless alone on `P` (`0` output change on `[−1, 1]`):
- `j₁` drifts dormant `g`'s bias by `+2.5` (`[x + 0.5]₊`, free in `j₁`'s solo branch).
- `j₂` updates `r₁` to `[2x − 2]₊` (still silent on `P = [−1, 1]`).
- `j₃` drifts dormant `r₂`'s bias by `+0.5` (`[x − 1.5]₊`, free in `j₃`'s solo branch).

Compare four exact function-preserving forms of `Δᵢ` (identical output `2[x − 2]₊` on all of `ℝ`):
- **Pre-fold `Δᵢ`** (active width `2`): `J = (2.5, 0, 0)`, sum `2.5`, max `2.5`. On `P`, `J(Δᵢ, j₁) = 1.5`, so merging with `j₁` breaks old task A even though both solos preserve A.
- **Width-minimal fold `F_width`** (`g → r₁`, active width `2 → 1`): `J = (0, 4.0, 0)`, sum `4.0`, max `4.0`. Net refund on sum is **`−1.5`** (width dropped, committed interaction got strictly worse).
- **Partner-targeted fold `F_partner`** (`g → r₂`, active width stays `2`): `J = (0, 0, 0.5)`, sum `0.5`, max `0.5`. Net refund on sum is **`+2.0`** (`+2.5` on `j₁`, `0` on `j₂`, `−0.5` debit on `j₃`), with zero width reduction.
- **Minimax split fold `F_split`** (`g → (1/9)r₁ + (8/9)r₂`, active width `2`): `J = (0, 4/9, 4/9)`, sum `8/9 ≈ 0.889`, **max `4/9 ≈ 0.444`**, beating both `F_width` and `F_partner` on worst-partner interaction.

Thus minimizing width, minimizing sum of `J`, and minimizing max `J` pick three different points on the same solo-equivalence fiber.

**Witness 2 — Super-additive joint absorption in certified `J`, even when both partial folds are feasible.** One input `x`, `D = P = [−1, 1]`. Base `θ₀` has five ReLU units: constant receiver `c = [0·x + 1]₊` (readout `0`), live receivers `r₁ = [x + 2]₊` and `r₂ = [1 − x]₊` (readout `1` each), and dormant spent gates `g₁ = [x + 2]₊`, `g₂ = [1 − x]₊` (readout `0` each). Branch `i` installs `w_{g₁} = 1, w_{g₂} = 1` (adding `g₁ + g₂ = 3` on `D`).
- **Partner `j_gr`** drifts biases by `+1.0` on `g₁, g₂`, `+0.8` on `r₁, r₂`, and `0` on `c`.
  - Pre-fold: `J = 2.0`.
  - **Regime 2a (without `r₁, r₂`, as in #183#14):** Neither `g₁` nor `g₂` can fold alone into `c` (`0 + 0 = 0`), while joint fold `F_joint` (`g₁ + g₂ → 3c`) gives `J = 0`, refund **`+2.0`**.
  - **Regime 2b (with `r₁, r₂` present — both partial folds feasible and profitable):** Partial fold 1 (`g₁ → r₁`) earns `+0.2` (`J: 2.0 → 1.8`); partial fold 2 (`g₂ → r₂`) earns `+0.2` (`J: 2.0 → 1.8`); greedy sequential folding earns `0.2 + 0.2 = +0.4` (`J: 2.0 → 1.6`). Joint fold `F_joint` (`g₁ + g₂ → 3c`, touching neither `r₁` nor `r₂`) gives `J = 0`, earning **`+2.0` — 5× (`+1.6`) more than the sum of feasible partial folds**.
- **Partner `j_c`** drifts `c`'s bias by `+0.5` and leaves `g₁, g₂, r₁, r₂` untouched. Now `F_joint` *costs* `1.5` (`J: 0 → 1.5`) while greedy folding costs `0`. Super-additivity is itself partner-indexed.

### Common first-test rules

Freeze `θ₀`, partner classes `{Π_k}`, merge operator (weight-space sum), domains `D` and `P`, rounding, and budget before each run. **Stacked control for #193#02:** width-minimal folding (Neuron Merging / ZipIt!) + `#181#14` interaction-only rotation + permutation alignment (Git Re-Basin / C²M³) + exact joint recertification after each fold. **Stacked control for #193#05:** greedy sequential single-gate folds + `#183#14` slot-only joint folding without `J` credit + exact joint search at matched compute + speculative refill (#193#10) as negative control. Measure useful merged admissions per unit of total search + proof cost at fixed old-task retention floors. **Retention:** verify exact branch-`i` equivalence on `Dᵢ` at every fold intermediate, score old tasks A/C on held-out slices at merge and after one legal suffix update, and keep both branches' new-task skills. **P** = candidate primitive; **I** = improvement or audit.

## Idea cards

### Partner-targeted fold selection (deepening #193#02)

#### 01. Width-increasing partner-targeted splits (P)
- **Mechanism:** Allow exact function-preserving *splits* (strictly increasing active unit count, as in Witness 1's `F_split` generalized to splitting one gate across two or more receivers) whenever distributing readout duty across receivers lowers worst-partner or total certified `J` below every width-reducing fold.
- **Novelty vs nearest prior art:** Net2Net widens networks for capacity; Neuron Merging and ZipIt! strictly reduce width; #193#02 still frames folds as compression into live receivers. Using a width-*increasing* exact refactor to earn merge headroom against committed partners is the candidate operation.
- **Cheapest first test:** Witness 1 with two active receivers and a minimax-`J` cap of `0.45` (infeasible for every width-1 and single-receiver fold, feasible for `F_split` at `4/9`); compare width-minimal folding, single-receiver partner folding, `#181#14` rotation, and split folding on admission rate at matched search cost.
- **Old-task retention check:** Exact output match of branch `i` on `D` after the split; A/C retention on `P` at merge with each committed partner and after one legal suffix update.

#### 02. Partner-vector Pareto frontier of folds (P)
- **Mechanism:** Instead of scalarizing committed partners into one sum `∑_k J_k`, compute and cache the small Pareto-undominated set of function-preserving folds over the vector `(J(·, Π₁), …, J(·, Π_K))`, deferring the final fold choice until the merger names which partner actually arrives next.
- **Novelty vs nearest prior art:** Multi-objective pruning trades accuracy vs. FLOPs; CoFiMA and FedSEAM merge against a fixed partner set. Caching an equivalence-fiber Pareto frontier indexed by partner interaction vectors so late partner arrivals pick without re-searching is the candidate object.
- **Cheapest first test:** Witness 1 with random arrival order of `{j₁, j₂, j₃}` (one partner merges next); compare eager sum-minimal folding, eager width-minimal folding, late re-search from scratch, and the cached 3-point frontier at matched total bytes and verification calls.
- **Old-task retention check:** A/C on `P` at the late-selected fold and merge for every arrival order, plus branch `i` equivalence across all frontier points.

#### 03. Non-permutation symmetry folds beyond Re-Basin (P)
- **Mechanism:** Optimize over the full piecewise-linear equivalence group — positive rescalings `((α_u w_u, α_u b_u), v_u / α_u)` and affine-cell linear combinations — to minimize certified `J` against committed partners' write footprints, strictly enlarging the search space beyond unit permutations.
- **Novelty vs nearest prior art:** Git Re-Basin and C²M³ (`2405.17897`) optimize permutations only; neural teleportation (`2012.01118`) uses continuous symmetries for optimization speed; `2506.13018` catalogs symmetries without certified merge bounds. Targeting continuous rescaling + absorption symmetries to certified `J` is the candidate.
- **Cheapest first test:** Two-layer ReLU toy where permutation-only alignment leaves `J > 0` because a partner scales input weights of a shared gate, while positive rescaling `α_u` reduces `J` to near zero; compare Git Re-Basin, C²M³, `#181#14` rotation, and continuous-symmetry folding.
- **Old-task retention check:** Exact output invariance on `D` in float and deployed fixed-point (checking rescaling does not trigger overflow/rounding flips); A/C at merge and after suffix.

#### 04. Partner-disjoint receiver routing (I)
- **Mechanism:** When multiple live or dormant receivers span the same activation cell as a spent gate, score each candidate receiver by its certified overlap with committed partners' declared write supports and route the fold into the least-written receiver first.
- **Novelty vs nearest prior art:** Structural conflict avoidance (FedSEAM `2610.33496`, sparse subspace routing) applied to receiver selection inside #193#02; an improvement unless it beats full `J` minimization on search cost.
- **Cheapest first test:** Ten-unit host with 3 equivalent receivers and 2 committed partners writing disjoint subsets; compare width-minimal, support-disjoint routing, and full `J`-certified search on verification calls and unsafe admissions.
- **Old-task retention check:** Exact branch-`i` equivalence on `D`; A/C on `P` at merge with both partners.

#### 05. Sign-aligned folding for certified interaction cancellation (P)
- **Mechanism:** Choose a function-preserving fold whose moved readout weight has the opposite sign to a committed partner's certified preactivation shift on a shared receiver, creating a *negative* mixed residual that offsets an unavoidable positive interaction elsewhere — valid only inside cells where the sign premise is certified (#193#14).
- **Novelty vs nearest prior art:** TIES resolves sign conflicts by majority vote on task vectors; #181#6/#193#14 note signed bounds passively. Actively selecting a fold on `ℰ(Δᵢ)` to *create* certified signed cancellation against a committed partner is the candidate.
- **Cheapest first test:** Two-unit ReLU host where an unavoidable `J = +1.0` on unit 1 can be offset to `0.2` by folding a redundant gate into unit 2 with opposite readout sign against a sign-certified partner; compare unsigned `J`-minimization, TIES, and sign-aligned folding, plus an adversarial sign-flip partner as negative control.
- **Old-task retention check:** A/C on `P` under both the nominal partner and a sign-reversed out-of-class partner (must fail closed on the latter).

#### 06. Adversarial dormant-drift minimax folding (I)
- **Mechanism:** When partner write coordinates are only bounded in norm (not named per unit), pick the fold in `ℰ(Δᵢ)` minimizing worst-case `J` over an `ℓ_∞` or `ℓ_2` drift ball on all dormant units of `θ₀`, preventing Witness 1's `j₁`-style hidden-drift ambush.
- **Novelty vs nearest prior art:** Robust optimization / IBP worst-case perturbation bounds applied to #193#04's dormant-drift audit; an improvement on #193#02 when partner classes are coarse.
- **Cheapest first test:** Witness 1 with partner class `Π = {‖Δ_dormant‖_∞ ≤ ε}` (unnamed target unit); sweep `ε` and compare nominal partner folding, width-minimal folding, and minimax dormant-drift folding on worst-case `J`.
- **Old-task retention check:** A/C on `P` at the worst-case vertex of the drift ball.

#### 07. Two-step lookahead folding under sequential partner arrivals (P)
- **Mechanism:** Because folding consumes receiver writable range (#183#15/#193#08), a myopic fold for partner 1 can exhaust the only receiver that would have saved partner 2. Certify a fold only together with a residual equivalence witness proving a low-`J` fold remains available for the next committed partner in queue.
- **Novelty vs nearest prior art:** Dynamic programming / resource reservation over a known queue; the candidate is coupling a fold's certified refund with a residual-fiber reachability proof for later partners without re-training.
- **Cheapest first test:** Three-unit host with two sequential partner commitments and bounded receiver range; compare myopic `#193#02`, static receiver reservation (#193#08), and two-step lookahead folding on total admitted merges.
- **Old-task retention check:** A/C on `P` after fold 1, merge 1, fold 2, and merge 2, with both partners' new skills preserved.

### Super-additive joint absorption (deepening #193#05)

#### 08. Feasible-partial super-additive joint folds (P)
- **Mechanism:** Search joint folds of `k ≥ 2` spent gates into a low-drift shared carrier (such as Witness 2b's constant receiver `c`) even when every individual gate already has a feasible, profitable partial fold into another receiver, crediting the verified excess drop `ΔJ(S) − ∑_{g ∈ S} ΔJ({g})`.
- **Novelty vs nearest prior art:** #183#14 and #193#05 motivate joint folds from single-gate *infeasibility*; Witness 2b proves super-additivity in certified `J` persists even when every partial fold is feasible and profitable, separating liability super-additivity from feasibility.
- **Cheapest first test:** Witness 2b (`r₁, r₂` drifted `+0.8`, `g₁, g₂` drifted `+1.0`, `c` drifted `0`); compare greedy sequential folds (refund `0.4`), `#183#14` slot-only joint folding, exact joint search, and speculative refill on useful admissions and proof calls.
- **Old-task retention check:** Exact output match on `D = [−1, 1]` before and after folding; A/C at merge with `j_gr` and after a third useful write.

#### 09. Minimal-arity super-additive witness certificates (P)
- **Mechanism:** Given a pool of spent gates, extract a minimal subset `S` (`|S| = 2, 3, …`) whose joint fold earns strictly positive excess `J`-refund over all proper partitions of `S`, and attach a small minimality proof so downstream verifiers check only `S` and its receiver rather than the whole layer.
- **Novelty vs nearest prior art:** #183#06 finds minimal neutral groups for slot release; minimal unsatisfiable subsets find minimal obstructions. Certifying minimal *super-additive liability* subsets `S` for partner-indexed refunds is the candidate.
- **Cheapest first test:** Six-gate host containing one planted 3-gate super-additive group (`|S| = 3`, all pairs have zero excess) plus 3 decoy gates; compare pairwise joint search, full-layer exact search, and minimal-arity extraction on search time and refund recovered.
- **Old-task retention check:** Exact equivalence on `D` over the 3-gate cell refinement; A/C at merge and after suffix.

#### 10. Cross-branch atomic joint absorption (P)
- **Mechanism:** When branch `i` holds spent gate `g₁` and committed partner `j` holds `g₂`, neither branch can fold its own gate into a shared constant/low-drift receiver alone without changing its solo function. Execute an atomic paired fold that jointly absorbs `g₁ + g₂` at merge time while proving both branches' solo skills survive in the merged output.
- **Novelty vs nearest prior art:** #189#16 moves both branches atomically to widen a merge-weight range; here both branches perform a *jointly* function-preserving absorption of complementary spent gates across branches that neither could legally fold solo.
- **Cheapest first test:** Split Witness 2 across two branches (`i` holds `g₁ = [x+2]₊`, `j` holds `g₂ = [1−x]₊`, third partner `k` drifts both `g₁, g₂`); compare solo-only folds (both infeasible), `#189#16` paired representation moves, and atomic cross-branch absorption on `J` against `k`.
- **Old-task retention check:** Merged model preserves A/C on `P` and both `i` and `j`'s new-task skills; verify no solo branch silently breaks if the merge is later aborted.

#### 11. Domain-guarded joint folds with boundary-crossing refusal (P)
- **Mechanism:** Joint ReLU identities like `[x + 2]₊ + [1 − x]₊ = 3` hold exactly only on a bounded polytope `D_fold = [−1, 1]` and diverge outside it. Package every joint fold with its exact validity polytope `D_fold` and a cheap check that refuses any partner whose preactivation shift pushes an input of `D` across `∂D_fold`.
- **Novelty vs nearest prior art:** Piecewise-linear region verification (IBP, ReluDiff) checks fixed domains; binding a joint fold's refund receipt to its exact algebraic identity polytope `D_fold` prevents silent out-of-domain divergence when partners shift inputs.
- **Cheapest first test:** Witness 2 with a partner that shifts `x` (or upstream features) by `±0.3`, pushing `x = 1` past the kink of `[1 − x]₊`; compare unguarded joint folding, full-domain global folding (infeasible), and polytope-guarded joint folding on unsafe admissions.
- **Old-task retention check:** A/C on `P` and on boundary-adjacent held-out probes just inside and just outside `D_fold`.

#### 12. Atomic vs. staged joint-fold intermediate safety (I)
- **Mechanism:** When hardware or adapter rank limits prevent installing a `k`-gate joint fold in one atomic step, check whether there exists an ordering of single-weight edits whose intermediates stay inside the certified `J` cap, or else certify that an atomic commit (staging buffer) is mandatory.
- **Novelty vs nearest prior art:** Make-before-break (#157) and #183 staged neutral paths; an audit/improvement checking whether super-additive joint folds have safe serializations or require atomic staging.
- **Cheapest first test:** Witness 2b under 1-unit-at-a-time weight writes; verify every serial ordering temporarily breaks `D` equivalence or raises `J`, and price the staging-buffer bytes needed for atomic commit against greedy sequential folds.
- **Old-task retention check:** A/C at every visible intermediate weight state if staged, or exact pre/post equivalence if atomic.

#### 13. Cross-partner fold-unlocking cascades (P)
- **Mechanism:** Branch `i`'s joint fold zeros two shared gate slots `g₁, g₂`, which removes a live-reader constraint that previously blocked partner `j` from folding its own spent gate `g₃` into `g₁`. Credit branch `i` only for its own `J` drop, and issue a conditional *unlock token* that `j` converts into a second refund only after `j`'s fold is certified.
- **Novelty vs nearest prior art:** Dependency graphs in compiler register allocation; in continual merging, certifying a two-hop cross-branch fold cascade without double-counting the unlocked refund is the candidate.
- **Cheapest first test:** Four-unit host where `j`'s fold is blocked until `i`'s joint fold frees `g₁`; compare independent solo folds, exact two-branch joint planning, and unlock-token cascading on total admissions and false-credit count.
- **Old-task retention check:** A/C after `i`'s fold, after `j`'s unlocked fold, and at the final merge.

#### 14. Negative-synergy joint-fold veto (I)
- **Mechanism:** Before executing a joint fold of `S`, test whether combining partial folds *increases* certified `J` against any committed partner (as in Witness 2's `j_c`, where `F_joint` costs `1.5` while both partial folds cost `0`), and emit a veto receipt that forces fallback to partial folds or escrow.
- **Novelty vs nearest prior art:** Safety audit for #193#05; ensures super-additive search cannot silently trade a `j_gr` win for a `j_c` catastrophe.
- **Cheapest first test:** Witness 2 with both `j_gr` and `j_c` committed simultaneously; compare unvetoed joint folding, greedy partial folding, and veto-gated folding on worst-partner `J` and unsafe merges.
- **Old-task retention check:** A/C on `P` against both `j_gr` and `j_c` at merge.

### Per-partner credit accounting and governance

#### 15. Non-fungible partner-indexed credit ledgers (P)
- **Mechanism:** Store fold-earned headroom as a vector ledger `C[Π_k]` keyed by partner class rather than a scalar pool. A refund `+2.5` against `Π₁` may only pay for later writes/merges that increase liability toward `Π₁`; spending it on `Π₂` is rejected by type.
- **Novelty vs nearest prior art:** Scalar leakage leases (#176) and privacy odometers (`1605.08294`) track one scalar budget; #193#01 introduces per-partner receipts. Enforcing *non-fungibility* across partner classes as an accounting invariant prevents cross-subsidy violations like Witness 1.
- **Cheapest first test:** Witness 1 followed by a second branch `i` update that adds `+1.0` liability against `j₂` while claiming `+2.5` credit earned against `j₁`; compare scalar-pool accounting, non-fungible vector accounting, and full joint recertification on unsafe admissions.
- **Old-task retention check:** A/C on `P` after the post-fold update and merge with `j₂` (scalar pool admits an unsafe merge; vector ledger refuses).

#### 16. Debited-partner escrow and compensating-fold pairing (P)
- **Mechanism:** When a fold produces mixed signs across partners (Witness 1's `F_partner`: `+2.5` on `j₁`, `−0.5` on `j₃`), do not immediately refuse or immediately credit; place the `+2.5` in escrow until either `j₃`'s existing slack absorbs `0.5` or a second fold/repair on another unit earns `≥ +0.5` against `j₃`, settling the pair atomically.
- **Novelty vs nearest prior art:** Escrow/netting in clearinghouses (#124#11) applied to signed partner-indexed fold receipts; differs from #193#01's immediate refusal by allowing multi-fold net-positive packages without relaxing any partner's floor.
- **Cheapest first test:** Two-block extension of Witness 1 where block 1's `F_partner` is `(+2.5, 0, −0.5)` and block 2 has a fold `(0, 0, +0.6)`; compare immediate refusal of any debit, unconstrained sum credit, and escrow-paired settlement on safe admissions.
- **Old-task retention check:** A/C on `P` against all three partners after atomic settlement; verify no merge occurs while escrow is open.

#### 17. Coalitional credit for multi-way merges (P)
- **Mechanism:** For `m ≥ 3` branches merging simultaneously (`θ₀ + Δᵢ + Δⱼ + Δ_k`), a fold that drops both pairwise `J_{ij}` and `J_{ik}` to `0` can still leave a nonzero 3-way mixed term `J_{ijk}` (a ReLU gate opened only when all three sum). Index fold credits by partner *subsets* (coalitions) up to merge arity `m`, and refuse to infer coalitional credit from pairwise receipts alone.
- **Novelty vs nearest prior art:** #181#8 and MNS6 note pair-invisible coalitions as an audit; extending per-partner fold receipts to subset-indexed coalitional ledgers is the candidate accounting object for multi-branch continual merging.
- **Cheapest first test:** Three-branch ReLU gate with preactivation `−1.5`, each branch adding `+0.6` (every pair stays closed at `−0.3`, all three open at `+0.3`); fold branch `i` onto or off that gate and compare pairwise-only credit vs. 3-way coalitional credit on unsafe 3-way admissions.
- **Old-task retention check:** A/C on `P` at every pairwise merge and at the 3-way merge.

#### 18. Sound credit splitting under partner-class refinement (I)
- **Mechanism:** When a coarse partner class `Π` is later split into narrower subclasses `Π₁ ∪ Π₂` (e.g., after a probe or new commitment), derive subclass credits from the stored before/after fold state without re-running fold search, guaranteeing `U′(Π_r) ≤ U′(Π)` and debiting any subclass whose pre-fold bound was looser.
- **Novelty vs nearest prior art:** Contract refinement (Pacti) and #193#06; an improvement that preserves receipt reuse across belief updates without re-searching `ℰ(Δᵢ)`.
- **Cheapest first test:** Coarse partner class covering `j₁` and `j₃` in Witness 1, refined after folding; compare stale-credit reuse, sound refinement splitting, and full re-search on verification calls and soundness.
- **Old-task retention check:** A/C on `P` in both refined subclasses at merge.

### Controls, audits, and falsifiers

#### 19. Admission-spread gate before ranking fold policies (I)
- **Mechanism:** Before comparing partner-targeted, split, and joint fold selectors, measure across 50 random piecewise-linear hosts and partner sets whether useful merged admissions at fixed A/C floors vary across candidate folds by more than seed and tie-breaking noise.
- **Novelty vs nearest prior art:** Enforces the ledger's plasticity-reserve kill ([PR #21](https://github.com/manojbajaj95/cl/pull/21): 0.09 MSE spread after retention matching). If fold choice has flat admission spread, stop.
- **Cheapest first test:** 50 random 6-unit ReLU hosts × 3 committed partners × 4 candidate folds each; report across-fold admission spread over within-fold seed spread.
- **Old-task retention check:** Hold A/C floors fixed on `P` across every host and fold.

#### 20. Fitted-surrogate vs. certified-`J` fold selection control (I)
- **Mechanism:** Select folds using (a) a fitted pairwise surrogate (LR-Merge `2611.25000` / BOCS-style regression), (b) random legal folds on `ℰ(Δᵢ)`, and (c) certified `J` bounds; partner-targeted certified selection must beat both on safe admissions at equal total compute.
- **Novelty vs nearest prior art:** Directly enforces the ledger's *coded merge interference* kill (fitted surrogate = BOCS, tied by gradient-free search) and tests whether certification adds value beyond fast interference forecasting.
- **Cheapest first test:** Witness 1 + Witness 2b + 20 random hosts with gate-crossing partners (where receiver-local Jacobian surrogates read zero slope); log unsafe admissions and total compute per safe admission.
- **Old-task retention check:** Report every A/C violation on `P` admitted by the surrogate arm.

#### 21. Smooth-activation collapse audit (I)
- **Mechanism:** Replace every ReLU in Witnesses 1 and 2 with `softplus_β(z) = β⁻¹ log(1 + e^{βz})` and sweep `β` from sharp (`100`) to smooth (`1`). Check whether width-vs-partner opposition and super-additive joint refunds persist or flatten into what smooth Fisher/CoFiMA weighting already predicts.
- **Novelty vs nearest prior art:** Enforces the ledger's [replay-deadline kill](https://github.com/manojbajaj95/cl/pull/113) (no cliff, smooth decay) and #193#20. Note that exact joint ReLU cancellation (`[x+2]₊ + [1−x]₊ = 3`) becomes only approximate under softplus, so the fold fiber `ℰ(Δᵢ)` itself shrinks.
- **Cheapest first test:** Sweep `β ∈ {1, 2, 5, 20, 100}` on Witnesses 1 and 2b; plot exact-fiber diameter, width-vs-partner `J` gap, and super-additive excess refund against `β` and against CoFiMA.
- **Old-task retention check:** A/C on `P` at each `β`, verifying that approximate softplus folds do not silently leak solo error.

#### 22. Proof-cost break-even audit vs. width-minimal + recertify (I)
- **Mechanism:** Account for every search call, cell-refinement check, IBP/ReluDiff verification, and ledger byte spent on partner-targeted and joint folds, and find the exact threshold in partner count `K` and host width `W` where it beats the stacked baseline (width-minimal fold + `#181#14` rotation + exact joint recertification).
- **Novelty vs nearest prior art:** Required by the ledger's merge-card rule and #193's cost contract; separates a genuine primitive from expensive bookkeeping.
- **Cheapest first test:** Sweep `K ∈ {1, 2, 4, 8}` partners and `W ∈ {4, 8, 16}` units on synthetic hosts with exact accounting of verification calls, bytes, and useful merged admissions.
- **Old-task retention check:** Identical A/C retention floor enforced across all arms.

## Ranked deeper questions

1. **Does partner-targeted fold selection (including width-neutral and width-increasing splits) beat width-minimal folding + `#181#14` rotation + exact recertification on useful merged admissions per unit of total proof cost?** Witness 1 proves width and partner `J` can strictly oppose each other on a single fiber. Test cards 01–03, 19, 20, and 22 on enumerable hosts with independently authored partners; if the stacked control ties at matched search and proof bytes, partner-targeted folding is an optimization convenience, not a primitive.
2. **How often is joint absorption super-additive in certified `J` beyond feasibility — and does it survive realistic partner-drift distributions?** Witness 2b shows a 5× super-additive jump even when both partial folds are feasible and profitable, while `j_c` shows a partner can flip the sign. Test cards 08, 09, 11, and 14 across random multi-gate hosts: measure the fraction of hosts with positive excess refund over greedy partial folds and whether `D_fold` boundary guards keep it sound.
3. **Is non-fungible per-partner (and coalitional) credit strictly necessary, or does scalar headroom plus cheap per-merge recheck tie it?** Test cards 15–17 on multi-partner and 3-way merge streams where cross-subsidy (Witness 1) and pair-invisible coalitions (card 17) are planted. The vector/coalitional ledger earns its bytes only if it prevents unsafe admissions that scalar credit misses while costing less than full recheck.
4. **Can cross-branch atomic joint folds and unlock cascades compose across independent learners without centralizing training data?** Test cards 10 and 13 under source-free handoff (#193#23): each branch publishes only its spent-gate signature, `D_fold`, and partner class, and the merger checks whether an atomic paired fold beats solo-only folding plus `#189#16` paired moves.
5. **Do partner-targeted and super-additive fold gains survive smooth activations and realistic scale?** Run cards 19 and 21 first as kill gates. If softplus smoothing collapses the equivalence fiber `ℰ(Δᵢ)` or if admission spread across folds falls within seed noise, report the negative result and stop before scaling.

**Verdict:** Both score-3 seeds from PR #193 sharpen into testable, non-trivial claims. Witness 1 establishes that width minimization and committed-partner `J` minimization can point in opposite directions on the exact same function-preserving fiber — and that minimax partner interaction can even favor a *split* over compression. Witness 2b establishes that joint absorption can be strictly super-additive in certified `J` even when every partial fold is individually feasible and profitable, while remaining partner-indexed. The strongest primitive candidates are **card 01/02** (partner-vector Pareto / split folds on `ℰ(Δᵢ)`), **card 08** (feasible-partial super-additive joint folds), and **card 15/16** (non-fungible per-partner credit with debited-partner escrow). All three must clear the spread gate (card 19), the smooth-activation audit (card 21), and the stacked control of width-minimal folding + `#181#14` rotation + exact recertification at matched compute, proof bytes, and A/C retention.
