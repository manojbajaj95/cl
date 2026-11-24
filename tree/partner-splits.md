# Partner-helping unit splits: earning merge headroom by growing width, and sign-aligned folds that cancel certified interaction

**Status:** Ideas only; no experiments, code, or GPU work. Both witnesses below were checked numerically on a dense grid (`10⁻⁵` spacing; exact on these piecewise-linear nets). **Parent:** [Partner-targeted folds](https://github.com/manojbajaj95/cl/blob/devin/1795563875-partner-folds/tree/partner-folds.md) ([PR #204](https://github.com/manojbajaj95/cl/pull/204)), cards #01 and #05. **Review seed:** [Flood triage row 315](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L315) keeps two ideas at score 3: (#01) *width-increasing partner-targeted splits*: exact function-preserving splits of one gate across several receivers whenever spreading read-out duty lowers the worst certified partner interaction, so the refactor earns merge headroom by growing width; (#05) *sign-aligned folding for certified cancellation*: a fold whose moved read-out weight has the opposite sign to a committed partner's sign-certified shift on a shared receiver, creating a negative mixed residual that offsets an unavoidable positive one. The reviewer named the controls: width-minimal folding, single-receiver partner folding, #181 interaction-only repair, Net2Net widening without the partner objective, a cap feasible only for the split, solo scores matched, A/B/C retention (for #01); unsigned `J`-minimization, TIES sign election, #181 signed bounds used passively, post-merge correction, and a partner whose sign is not certified so the fold must be refused (for #05). **Grandparents:** [Fold-earned headroom](https://github.com/manojbajaj95/cl/pull/193) (#193), [cross-pool round 46](https://github.com/manojbajaj95/cl/pull/36) (MNS2/MNS3), [merge-aware budgets](https://github.com/manojbajaj95/cl/pull/181) (#181), [neutral groups](https://github.com/manojbajaj95/cl/pull/183) (#183), [cancelling pairs](https://github.com/manojbajaj95/cl/pull/175) (#175).

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Rules that bind this node: (1) *coded merge interference* was killed because a fitted pairwise surrogate is BOCS and gradient-free search ties it, so every card selects splits by a sound certified `J`, never a fitted surrogate; (2) the [plasticity-reserve reruns](https://github.com/manojbajaj95/cl/pull/21) died at a spread gate (0.09 MSE points after retention matching), so split policies must first show real spread in admitted merges; (3) the [replay-deadline kill](https://github.com/manojbajaj95/cl/pull/113) found smooth decay with no cliff, so every ReLU-exact gain faces a softplus control; (4) the merge-card rule: beat the union of the parts' best baselines stacked at equal compute, proof bytes and retention floor; (5) the width/laziness kill ([2506.16884](https://arxiv.org/abs/2506.16884)): wider SP nets forget less because they are lazier, so any "growing width helps" claim must hold at matched parameterization (muP) and matched solo function, not just matched parameter count; (6) every card is labelled **P** (candidate primitive) or **I** (improvement or audit), and every first test includes an old-task retention check.

## Is a partner-helping split a new object?

**Not as widening, neuron splitting, or sign resolution.** [Net2Net](https://arxiv.org/abs/1511.05641) duplicates units and divides their outgoing weights equally to grow capacity; [splitting steepest descent / Firefly](https://arxiv.org/abs/1910.02366) splits neurons to escape saddles; [Expand Neurons, Not Parameters](https://arxiv.org/abs/2510.04500) splits neurons at fixed parameter count to cut polysemantic interference inside one model; [Exact Network Surgery](https://arxiv.org/abs/2607.16568) and [Isotropic activations](https://arxiv.org/abs/2602.23405) make growth exactly function-preserving; [Partial Fusion](https://arxiv.org/abs/2605.22350) trades ensemble width against weight aggregation. None picks the split *weights* to minimize a certified mixed residual against named committed partners. On the merging side, [TIES](https://arxiv.org/abs/2306.01708), [CABS+](https://arxiv.org/abs/2608.12842), [CASS](https://arxiv.org/abs/2609.34184) and [Joint Null-Space Projection](https://arxiv.org/abs/2611.17103) remove or project away conflicting coordinates *after* fine-tuning, changing solo functions; [CAMFT](https://arxiv.org/abs/2609.22253) trains for mergeability; [LR-Merge](https://arxiv.org/abs/2611.25000) forecasts interference with a receiver-local affine surrogate that reads zero slope at a closed gate. All treat sign conflict as damage to drop or elect; none *uses* a certified opposite sign to cancel interaction while leaving each solo function exactly unchanged. Outside ML the nearest ideas are portfolio diversification under budgeted uncertainty ([Bertsimas–Sim 2004](https://doi.org/10.1287/opre.1030.0065)), secret sharing (no single party sees more than one share), and active noise cancellation (an anti-phase signal placed where the disturbance is certified).

**Conditional primitive:** a *certified-interaction program over the twin fiber*. Inside the exact solo-equivalence fiber `ℰ(Δᵢ)` of #204, the units of `θ₀` that compute the same function on all of `ℝ` (twins, up to positive rescaling) form classes; branch `i` may redistribute its read-out mass `v` over a class with any signed weights `α` with `Σ α_u = v`, and the solo function is unchanged identically. For piecewise-linear nets each partner's mixed residual is linear in `α` and its sup over `D` is attained at finitely many breakpoints, so "find the split or signed fold minimizing worst certified partner interaction" is an exact linear program (a Chebyshev approximation), and its dual is a certificate that no redistribution does better. Seed #01 is the nonnegative case of this LP (headroom from spreading), seed #05 is the signed case (headroom from cancelling). The object is a primitive only if the LP plus its dual certificate yields strictly more safe merged admissions per unit of search, proof and width cost than isolation into fresh private units + width-minimal folding + #204 single-receiver partner folding + exact joint recertification, stacked.

### Contract

- **Inherit #204.** Mixed residual `J(Δᵢ, Δⱼ) = sup_{x ∈ D} |f(θ₀+Δᵢ+Δⱼ) − f(θ₀+Δᵢ) − f(θ₀+Δⱼ) + f(θ₀)|`, per-partner non-fungible credit `r(F) = (U_k − U′_k)`, no manufactured credit (never move `θ₀`, shrink `D`, drop a partner, or substitute a fitted surrogate for `U_k`).
- **Split.** A legal split of branch `i`'s read-out mass `v` on gate `g` is `α ∈ ℝ^{T(g)}` over the twin class `T(g)` (units with identical input weights and bias in `θ₀`, or positive rescalings of them), with `Σ α_u = v`. *Width* is the number of units with `α_u ≠ 0`. Nonnegative `α` is a spreading split; any negative `α_u` is a signed split.
- **Sign certificate.** A partner class `Π` is *sign-certified on receiver u over cell C* iff every `Δⱼ ∈ Π` moves `u`'s preactivation by a shift of one known sign on every `x ∈ C ∩ D`. A signed split that relies on cancellation is legal only against sign-certified classes; against any other class the certificate must use the unsigned bound, which refuses it.
- **Width is charged, not free.** A split pays for every newly active unit (read-out bytes, later write range, proof cells) and is compared against the *isolation control*: putting the skill on a fresh private unit no partner writes, which gives `J = 0` against unit-local partners. A split earns credit only where isolation is unavailable (fixed width cap, partner classes that cover unnamed or new units, shared upstream features).

## Two exact paper witnesses

**Witness S1 — splitting one gate across receivers cuts worst-partner interaction below every single-receiver fold.** One input `x`, merge domain `D = [−1, 3]`, old protected domain `P = [−1, 1]`. Base `θ₀` has four twin units `g, r₁, r₂, r₃`, each `[x − 1]₊` with read-out `0`. Branch `i` installs its skill `[x − 1]₊` (zero on `P`, so `i` alone keeps old task A exactly). Four committed partners, each changing nothing alone (they drift dormant biases): `j₀` drifts `g` by `+2`, `j₁, j₂, j₃` drift `r₁, r₂, r₃` by `+1`. The residual against `jₖ` is `α_u · ([x − 1 + b]₊ − [x − 1]₊)`, which is nonzero on `(0, 1] ⊂ P` — merging breaks old task A even though both solos keep it.

| Form of `Δᵢ` (all give `[x − 1]₊` exactly) | `α` over `(g, r₁, r₂, r₃)` | `J` vector | max `J` | sum `J` | width |
|---|---|---|---|---|---|
| Keep on `g` | `(1, 0, 0, 0)` | `(2, 0, 0, 0)` | 2 | 2 | 1 |
| Single-receiver partner fold (#204) | `(0, 1, 0, 0)` | `(0, 1, 0, 0)` | 1 | 1 | 1 |
| Net2Net equal split, no partner objective | `(¼, ¼, ¼, ¼)` | `(½, ¼, ¼, ¼)` | 0.5 | 1.25 | 4 |
| Equal split over receivers | `(0, ⅓, ⅓, ⅓)` | `(0, ⅓, ⅓, ⅓)` | 0.333 | 1 | 3 |
| **Minimax split** `α ∝ 1/b` | `(1/7, 2/7, 2/7, 2/7)` | `(2/7, 2/7, 2/7, 2/7)` | **0.286** | 1.143 | 4 |

A cap of `0.4` on worst-partner `J` is infeasible for every width-1 form and for Net2Net's equal split, and feasible for the partner-weighted splits (the reviewer's "cap feasible only for the split"). The minimax value follows a *parallel-resistance law*: with each twin `u` exposed to its own partner with sup shift `c_u`, the best worst-case `J` is `v / Σ_u (1/c_u)`, so every added twin receiver strictly lowers it. The minimax split also raises sum `J` (1.143 > 1), so worst-partner and total interaction pick different splits; and the isolation control (a fresh private unit) gives `J = 0` here, which is why the contract charges width and requires a regime where isolation is unavailable.

**Witness S2 — a sign-aligned fold cancels an unavoidable interaction that every unsigned bound would leave.** `D = [−1, 3]`. Branch `i`'s skill is `[x − 2]₊ − 0.75·[2x − 3]₊`, written on two units it owns in `θ₀`: `g = [x − 2]₊` (no twin) and `h = [2x − 3]₊`, which has two dormant twins `r = r′ = [2x − 3]₊`. Partner `j` drifts the biases of `g` and `r` by `+1` (both dormant in `j`'s solo, so `j` alone changes nothing); `j` does not touch `h` or `r′`. The `g` term is unavoidable: `s_g(x) = [x − 1]₊ − [x − 2]₊`, sup `1`.

| Form of `Δᵢ` | exact `J` against `j` | unsigned per-unit bound `Σ_u |α_u|·sup|s_u|` |
|---|---|---|
| Pre-fold (`−0.75` on `h`) | 1.00 | 1.00 |
| Fold `h → r′` (partner-free twin; unsigned optimum) | 1.00 | 1.00 |
| **Sign-aligned fold `h → r`** (`−0.75` read-out against `j`'s `+1` shift) | **0.25** | 1.75 |
| `h → r` against a sign-uncertified class (`r` drifted by `−1`) | 1.75 | 1.75 |

The sign-aligned fold moves negative read-out onto the receiver that `j` shifts upward, so `j`'s residual on `r` (`clip(2x − 2, 0, 1)`, scaled by `−0.75`) cancels most of the unavoidable `g` residual: exact `J` drops `1 → 0.25`, a 4× cut. The weight `0.75` is the Chebyshev optimum (`0.6 → 0.40`, `0.7 → 0.30`, `0.75 → 0.25`, `0.8 → 0.30`, `1.0 → 0.50`). Any certificate that bounds each unit's contribution separately (triangle inequality, IBP per unit, #181 bounds used passively) scores this fold *worst* (`1.75`), so it can only be found with a signed bound on the summed residual. If `j`'s class allows either sign on `r`, the same fold gives `J = 1.75` and must be refused.

### Common first-test rules

Freeze `θ₀`, partner classes, merge operator (weight-space sum), `D`, `P`, rounding and budget before each run. **Stacked control for #01:** isolation into fresh private units at the same width budget + width-minimal folding + #204 single-receiver partner folding + Net2Net equal splitting + #181 interaction-only repair + exact joint recertification. **Stacked control for #05:** unsigned `J`-minimization + TIES sign election + #181 signed bounds used passively + post-merge correction (one repair step on the merged model at matched data) + a sign-uncertified partner that must be refused. Measure safe merged admissions per unit of search + proof + width cost at fixed A/B/C retention floors. **Retention:** exact branch-`i` equivalence on `Dᵢ` after every split, old tasks A/C on held-out slices of `P` at merge and after one legal suffix update, and both branches' new skills kept.

## Idea cards

### Partner-helping splits (deepening #204#01)

#### 01. Minimax twin-split LP with dual refusal certificate (P)
- **Mechanism:** For each twin class, solve `min_α max_k max_{x ∈ breakpoints} |Σ_u α_u s_{k,u}(x)|` subject to `Σ α_u = v` as an exact LP; publish the split and the LP dual (a weighting of partners and breakpoints) proving no redistribution in the class beats it, so a verifier checks one dual feasibility instead of re-searching.
- **Novelty vs nearest prior art:** Net2Net fixes `α` equal; #204#01 searches folds case by case; LR-Merge (`2611.25000`) forecasts, never bounds. An exact LP over the twin fiber with a checkable optimality certificate is the candidate object.
- **Cheapest first test:** Witness S1 plus 50 random hosts (twin classes of size 2–6, 2–5 unit-local partners); compare LP split, Net2Net, #204 single-receiver search and exhaustive grid on max `J`, verification time and dual check time.
- **Old-task retention check:** A/C on `P` at merge with each partner; exact branch-`i` equivalence on `D`.

#### 02. Parallel-resistance headroom law (P)
- **Mechanism:** Prove and test that against unit-local partners the best worst-case `J` over a twin class is `v / Σ_u (1/c_u)`, so headroom earned per added twin is the partner-weighted harmonic increment; use it as a price for width before any search.
- **Novelty vs nearest prior art:** Diversification under budgeted uncertainty (Bertsimas–Sim) gives the same algebra for portfolios; as a closed-form merge-headroom price for function-preserving width it is new to merging and CL.
- **Cheapest first test:** Witness S1 with `K = 1…8` twin receivers and exposures drawn from a log-uniform law; check the closed form against the LP to `10⁻¹²` and against Net2Net's `v·max c_u / K`.
- **Old-task retention check:** A/C on `P` at the predicted minimax split for each `K`.

#### 03. Sparse-adversary hedging splits (P)
- **Mechanism:** When partner classes are norm-budgeted but unnamed (`ℓ₁` or `Γ`-sparse drift over any unit, including units a split creates), splitting `v` into `K` shards caps worst `J` at `ε·max_u |α_u|`, so equal shards cut it to `ε/K`, and fresh private units no longer give `J = 0` because the class covers them.
- **Novelty vs nearest prior art:** #204#06 minimaxes over dense `ℓ∞` dormant drift, where splitting buys nothing (`ε·Σ|α_u|` is fixed); the sparse class is the one where width buys certified headroom and isolation loses its free zero.
- **Cheapest first test:** S1 with `Π = {one-unit bias drift ≤ ε}` over all units; compare isolation, single-receiver fold, equal split and LP split on worst `J`, and an `ℓ∞` class as the negative control where all splits tie.
- **Old-task retention check:** A/C on `P` at the adversary's best vertex for each split.

#### 04. Width-cap regime map: when splitting beats isolation (I)
- **Mechanism:** Map the frontier in (width budget, partner coverage, upstream sharing) where a split of an existing gate beats putting the skill on a fresh private unit; outside it the card refuses to split.
- **Novelty vs nearest prior art:** Progressive nets, PackNet and parameter isolation give `J = 0` whenever width is free; this audit locates the regime the seed needs and stops the node if it is empty in practice.
- **Cheapest first test:** Two-layer ReLU hosts where fresh units must read shared first-layer features that partners drift; sweep spare width `0…4` and shared-feature drift; report where LP splits beat isolation on max `J` at equal width.
- **Old-task retention check:** A/C on `P` for both arms at every grid point.

#### 05. Rescaled-twin splits through positive homogeneity (P)
- **Mechanism:** Enlarge twin classes to units equal up to positive rescaling (`[a·z]₊ = a[z]₊`); a partner bias shift on a rescaled twin has exposure `c/a`, so splits can route mass onto twins whose scale makes partner shifts smaller in output units.
- **Novelty vs nearest prior art:** #204#03 uses rescaling symmetries for folds; neural teleportation (`2012.01118`) uses them for optimization. Pricing exposure by twin scale inside the split LP is the new element.
- **Cheapest first test:** S1 with `r₂ = [2x − 2]₊` and read-out halved; check the LP picks it at exposure `c/2` and that fixed-point rounding at deployment does not break equivalence.
- **Old-task retention check:** Exact equivalence on `D` in float32 and int8; A/C on `P` at merge.

#### 06. Upstream-twin splits in deep nets (P)
- **Mechanism:** In depth, twins exist one layer down: two hidden paths computing the same function into the same receiver. Split the receiver's dependence across upstream twins so a partner drifting one first-layer path sees only its share.
- **Novelty vs nearest prior art:** Splitting work is single-layer (Net2Net, Firefly); `2510.04500` splits for polysemanticity inside one model. Splitting along *paths* against partners that drift upstream features is the candidate.
- **Cheapest first test:** 2-layer ReLU host with two upstream twin paths and one partner drifting each; compare receiver-level split, path-level split and isolation on max `J` at matched width.
- **Old-task retention check:** A/C on `P`, plus a check that path splitting does not change the downstream layer's solo function on any cell of `D`.

#### 07. Split-then-refold lifecycle (P)
- **Mechanism:** Split only for the merge window, then fold the shards back once the partner commits and its drift becomes known, returning the width; credit is earned only for the window and the refold must be function-preserving on the merged model.
- **Novelty vs nearest prior art:** Split-and-merge for compression (Net2Net then pruning) never ties the width loan to a partner's commitment window; #193/#204 fold only.
- **Cheapest first test:** S1 stream: split, merge `j₁`, refold, merge `j₂`; compare permanent split, no split and split-then-refold on total width-steps and safe admissions.
- **Old-task retention check:** A/C on `P` after split, merge, refold and second merge.

#### 08. Split receipts as partner-indexed width loans (P)
- **Mechanism:** Record each split as a loan: width borrowed, partner-indexed `J` credit earned, and the refold condition; a later learner may claim the shard units only by repaying (refolding or proving its own write leaves the credited `J` intact).
- **Novelty vs nearest prior art:** #204#15 keeps non-fungible credit; #176 leakage leases are scalar. Tying certified credit to the specific width that earned it is the new accounting object.
- **Cheapest first test:** S1 plus a third learner that wants `r₂`; compare free reuse, loan repayment and full recheck on unsafe admissions and verification calls.
- **Old-task retention check:** A/C on `P` after the third learner's write and the next merge.

#### 09. Partner-aware widening during training (I)
- **Mechanism:** When a learner grows (Net2Net, model growth), choose duplicate split weights by the LP against committed partners instead of equal division, so growth also prepays merge headroom.
- **Novelty vs nearest prior art:** Growth papers (`2607.14571`, Net2Net) optimize capacity or plasticity; this only changes the split weights, so it is an improvement unless the headroom is large.
- **Cheapest first test:** Grow a 4-unit learner to 8 under equal vs LP split, train both the same steps, merge with 3 partners; compare max `J` and new-task loss.
- **Old-task retention check:** A/C on `P` after growth, training and merge; matched muP to avoid the laziness confound.

#### 10. Split-induced write-range cost audit (I)
- **Mechanism:** Every active shard consumes receiver write range that later edits need (#183#15). Charge each shard the future edit freedom it blocks, and count split credit only net of it.
- **Novelty vs nearest prior art:** Enforces #193's cost contract on splits; separates headroom from moved liability.
- **Cheapest first test:** S1 followed by a later branch-`i` edit that needs `r₁` unconstrained; compare admitted edits after no split, LP split and split-then-refold.
- **Old-task retention check:** A/C on `P` after the later edit.

### Sign-aligned folds (deepening #204#05)

#### 11. Signed Chebyshev fold with sign certificate (P)
- **Mechanism:** Allow negative split weights and solve the signed LP; attach for every receiver used with nonzero cancelling weight a sign certificate (interval bound on the partner's preactivation shift over each cell) and refuse the fold if any certificate fails.
- **Novelty vs nearest prior art:** TIES drops minority-sign coordinates; #181 signed bounds are passive. Creating cancellation by choice, inside an exact solo fiber, with a refusal rule, is the candidate.
- **Cheapest first test:** Witness S2 (`J: 1 → 0.25`) plus 50 random hosts with planted unavoidable terms; compare unsigned optimum, TIES-style election, signed LP, and the sign-uncertified partner (must refuse; `J` would be 1.75).
- **Old-task retention check:** A/C on `P` against the nominal partner and the sign-flipped one.

#### 12. Signed-bound gap as a novelty meter (I)
- **Mechanism:** Measure on real merges how often the exact summed residual is far below the unsigned per-unit bound; that gap is the only room sign-aligned folds can use. If it is small in practice, the seed is a toy effect.
- **Novelty vs nearest prior art:** Audit enforcing the ledger's spread-gate rule on #05.
- **Cheapest first test:** 100 pairs of small ReLU MLPs fine-tuned on related toy tasks; compute exact `J` and the unsigned bound per pair; report the ratio distribution.
- **Old-task retention check:** Report A/C on `P` for pairs where the gap is largest.

#### 13. Anti-phase dummy pairs vs sign-aligned folds (I)
- **Mechanism:** The same cancellation can be built without folding: add `−a` on a partner-shifted twin and `+a` on a partner-free twin (a zero-function pair, #175). Compare this with folding an existing gate in the signed direction, which uses no extra active width.
- **Novelty vs nearest prior art:** #175 cancelling pairs are output-neutral at fixed width; this card decides whether #05 adds anything beyond a cancelling pair placed for a partner.
- **Cheapest first test:** S2 with an extra twin pair; compare dummy pair, sign-aligned fold and both on `J`, active width and later write range.
- **Old-task retention check:** A/C on `P` for each arm at merge.

#### 14. Partner-pair mutual cancellation contracts (P)
- **Mechanism:** Two learners agree before training that `i` places negative read-out on the receiver `j` will shift upward and vice versa, each publishing only a sign certificate for its drift; the merge then has certified cancelling cross terms on both sides.
- **Novelty vs nearest prior art:** CAMFT (`2609.22253`) trains for mergeability with shared objectives; here the exchange is only signs and receiver ids, and solo functions stay exact.
- **Cheapest first test:** Two learners on toy tasks sharing 4 twin receivers; compare independent training, CAMFT-style joint regularization and sign-contract folding on `J` and bytes exchanged.
- **Old-task retention check:** A/C on `P` at merge, plus each learner's own new task.

#### 15. Sign-certificate lifetime under partner suffix updates (I)
- **Mechanism:** A sign certificate is only as good as the partner's next update. Attach an expiry (the set of suffix updates the certificate survives) and void cancelling credit once a partner's update leaves it.
- **Novelty vs nearest prior art:** #180 split-timed deadlines and #176 leases expire admission rights; applying expiry to sign premises closes the main soundness hole of #05.
- **Cheapest first test:** S2 with `j` taking 10 SGD steps after commitment; track how often the sign premise breaks and compare voided vs unvoided credit on unsafe merges.
- **Old-task retention check:** A/C on `P` at each step's merge.

#### 16. Cancellation against multiple partners at once (P)
- **Mechanism:** A negative read-out on a receiver cancels a partner shifting it upward but adds to one shifting it downward. Solve the signed LP over the joint partner vector and report the Pareto set; refuse folds that help one partner by hurting another beyond its slack (#204#15 non-fungibility).
- **Novelty vs nearest prior art:** #204#02 caches Pareto sets of unsigned folds; signed cancellation makes partner interests conflict on the same receiver, which unsigned folds never do.
- **Cheapest first test:** S2 with a second partner drifting `r` by `−0.5`; compare single-partner signed fold, joint signed LP and unsigned fold on max `J`.
- **Old-task retention check:** A/C on `P` at merge with each partner and with both.

#### 17. Split plus sign: mixed-sign shard portfolios (P)
- **Mechanism:** Combine seeds: one gate's mass spread over many twins with weights of both signs, so partners with known signs are cancelled and partners with unknown signs are diluted. The LP chooses both at once.
- **Novelty vs nearest prior art:** Neither seed alone; the combination is a joint diversification-and-hedging object with no ML precedent found.
- **Cheapest first test:** Host with 5 twins, two sign-certified partners and two sparse unnamed partners; compare spreading only, signing only and the joint LP on worst `J`.
- **Old-task retention check:** A/C on `P` at merge against all four partners.

### Controls, audits and falsifiers

#### 18. Isolation and Net2Net control suite (I)
- **Mechanism:** Every split result is reported against (a) a fresh private unit at the same width, (b) Net2Net equal split, (c) #204 single-receiver partner fold; the seed survives only where it beats all three.
- **Novelty vs nearest prior art:** Enforces the merge-card rule; Witness S1 already shows (a) wins when width is free.
- **Cheapest first test:** Same 50 hosts as card 01 with width budgets 0, 1, 2 spare units.
- **Old-task retention check:** A/C on `P` for all arms.

#### 19. Post-merge correction control (I)
- **Mechanism:** Compare a pre-merge split or signed fold against simply merging and running one correction step on the merged model with the same data the certificate used.
- **Novelty vs nearest prior art:** Reviewer-named control for #05; Merge++ (`2609.22886`) and HR-Merge (`2611.27377`) refine after merging.
- **Cheapest first test:** S1 and S2 plus random hosts; one-step and five-step correction at matched samples.
- **Old-task retention check:** A/C on `P` after correction, since correction can move old tasks the split never touched.

#### 20. Smooth-activation collapse audit for twins (I)
- **Mechanism:** Under softplus, twins stay exact twins (same weights), so splits survive, but sign certificates become soft and the residual sum no longer has finite breakpoints. Sweep `β` and test whether S2's cancellation and S1's harmonic law persist.
- **Novelty vs nearest prior art:** Enforces the PR #113 smooth-decay rule.
- **Cheapest first test:** `β ∈ {1, 2, 5, 20, 100}` on S1 and S2; report LP value and certificate tightness.
- **Old-task retention check:** A/C on `P` at each `β`.

#### 21. Spread gate on split choice (I)
- **Mechanism:** Before ranking split policies, check that safe admissions vary across candidate splits by more than seed noise on random hosts.
- **Novelty vs nearest prior art:** Enforces the PR #21 kill.
- **Cheapest first test:** 50 hosts × 3 partners × 5 splits; report across-split over within-split variance.
- **Old-task retention check:** A/C floors fixed across hosts.

#### 22. muP-matched width control (I)
- **Mechanism:** Any merge-headroom gain from growing width must survive at matched muP scaling and matched solo function, ruling out the laziness effect the ledger already killed.
- **Novelty vs nearest prior art:** Enforces the width/laziness kill (`2506.16884`).
- **Cheapest first test:** Train split and unsplit learners after the split under SP and muP for 100 steps; compare `J` after training.
- **Old-task retention check:** A/C on `P` after training under both parameterizations.

## Ranked deeper questions

1. **Is there a realistic regime where splitting an existing gate beats isolation into fresh units?** Witness S1 shows the split wins only when a fresh private unit is not allowed or not safe. Cards 03, 04, 06 and 18 decide it: sparse partner classes that cover new units, fixed width caps, and shared upstream features. If isolation ties everywhere, seed #01 is an accounting curiosity.
2. **How large is the signed-bound gap in real merges?** Witness S2 cuts `J` 4× only because the exact summed residual is far below the unsigned per-unit bound. Card 12 measures that gap on independently fine-tuned pairs; if it is small, seed #05 has no room to act.
3. **Can sign certificates survive partner training?** Cancelling credit is only sound while the partner's shift keeps its sign. Cards 14 and 15 test whether sign premises last over realistic suffix updates and whether exchanging signs alone beats CAMFT-style joint regularization.
4. **Does the twin-fiber LP with its dual certificate cut verification cost enough to be a primitive?** Card 01's dual is a small certificate a merger can check without search. It counts only if it beats the stacked control (isolation + width-minimal + #204 single-receiver fold + recertification) on safe admissions per unit of proof and width cost, and survives the softplus audit (card 20).

**Verdict:** Both score-3 seeds sharpen into one exact object: an LP over the twin fiber whose nonnegative solutions are seed #01 (spreading, with a parallel-resistance law `v / Σ 1/c_u`) and whose signed solutions are seed #05 (certified cancellation). Witness S1 shows a partner-weighted split beats every single-receiver fold and Net2Net's equal split (worst `J` 2 → 1 → 0.5 → 0.286) but also that a fresh private unit beats it when width is free. Witness S2 shows a sign-aligned fold cuts `J` 1 → 0.25 where every unsigned bound scores it worst (1.75), and that the same fold must be refused against a sign-uncertified partner. Strongest candidates: **card 01** (LP + dual certificate), **card 03** (sparse-adversary hedging, the regime where isolation loses), **card 11** (signed Chebyshev fold with sign certificate). All three must first pass the isolation control (card 18), the signed-gap measurement (card 12), the spread gate (card 21) and the muP-matched width control (card 22).
