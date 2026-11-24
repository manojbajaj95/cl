# Irreversible split points: is the point of no return in a training trajectory a new object for continual learning?

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Cross-pool round 40](../ideas/flood/cross-pool-40.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36)). **Review seed:** [Flood triage row 268](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/flood-triage.md#L268) gives SRW1 and SRW3 score 3: replay a refused edit in shadow to locate the earliest training prefix after which source and substitute diverge in a way that later damages an old task, and place the witness there (SRW1); when a complete shadow check passes but the cheap verifier refuses, spend a truthful example moving reachable states out of the verifier's uncertain region instead of adding a correction (SRW3). **Ledger read first:** [idea ledger](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/idea-ledger.md) (merges must beat stacked parts at equal budget; primitive-or-improvement gate; no credit for "true by construction"; match per-item margins; gate every predictor on target variance; check independent old-task retention including rare slices in every first test; no self-generated data credited over matched teacher data).

## Is the point of no return in a training trajectory a new object for continual learning?

**Not automatically.** Trajectories diverging is [linear mode connectivity (LMC)](https://arxiv.org/abs/1912.05671) and [critical learning periods](https://arxiv.org/abs/1711.08856); finding the first failing step in a trace is delta debugging, [first-point-of-loss (PR #134)](https://github.com/manojbajaj95/cl/pull/134), and causal-prefix minimization ([PR #166](https://github.com/manojbajaj95/cl/pull/166) card 05); pushing states away from uncertain gates is [ReLU-stability training](https://arxiv.org/abs/1809.03008), [interval-bound training](https://arxiv.org/abs/1810.12715), and [return corridors (PR #168)](https://github.com/manojbajaj95/cl/pull/168). Moreover, [replay-deadlines (PR #113)](https://github.com/manojbajaj95/cl/pull/113) already showed that in a continuous linear host, repair value decays smoothly with no cliff, making timing policies tie within 0.011 of the hindsight oracle.

The candidate new object is a **typed irreversible split point** `(t*, Σ, κ, W_pre)` of a coupled training dynamics under a frozen future law:

- Fix a source learner `S` and its retired-teacher substitute `W`, a frozen legal continuation law `F` (full state: weights, optimizer slots `m, v`, clocks, sampler, deployed numerics), a legal but refused edit `e`, an accommodation budget `A_bud`, a witness grammar `G`, and fixed old-task floors `F_old` on independent `A` and `C`.
- Replay `S` and `W` in shadow along the prefix `t = 0, …, T` leading to `e`'s refusal at `T`.
- Define `t*` as the **earliest prefix step** after which no witness `W_post ∈ G` (within `A_bud`) placed at `t > t*` can make `e` safely admissible while holding `F_old`, whereas a witness `W_pre ∈ G` placed at or before `t*` can.
- Assign a **split type** `κ ∈ {dynamical, verifier}`:
  - **Dynamical split (SRW1):** the true trajectories of `S` and `W` genuinely cross a separatrix `Σ` (e.g. a ReLU gate dies, an Adam second-moment `v` locks in a different preconditioner scale, or a saddle separates basins) so that even an exact checker rejects every post-`t*` witness.
  - **Verifier split (SRW3):** the true trajectories remain safely reconcilable at `T` (exact shadow check passes), but the cheap verifier's sound over-approximation straddles `Σ` at `t_v < T` and explodes into its uncertain region, refusing `e`. Here the remedy is not a corrective example at `T` but a truthful example before `t_v` that moves the reachable tube off `Σ` without changing the intended correction.

This differs from [PR #134](https://github.com/manojbajaj95/cl/pull/134) (which locates where an old bit disappears inside one trajectory between paired A-variants) and [PR #113](https://github.com/manojbajaj95/cl/pull/113) (which schedules target-blind self-replay by a scalar merge deadline): here `t*` is a **two-trajectory bifurcation conditioned on an external refused edit**, and it splits cleanly into a *dynamical* irreversibility boundary vs an *epistemic* verifier boundary.

It earns **primitive (P)** status only if split points are **sharp, distinguishable from smooth decay, and reusable across unseen edits**—for instance, if a split hyperplane `Σ` discovered from one refused edit predicts and prevents irreversible divergence for disjoint edits from an independent editor, or if dynamical and verifier splits can be factored and traded off beyond stacked counterexample-guided repair + causal-prefix minimization + MTT + interval-bound training + PR #168 return corridors at equal checks, bytes, and old-task retention. If `t*` only picks a slightly better timestep for one edit's counterexample, it is an **improvement (I)**.

### Three traps that would make the object vacuous

1. **The smooth-decay trap (PR #113 repeat).** If repair cost rises smoothly with `t` rather than jumping at a separatrix, there is no "point of no return"—only a monotone trade-off where endpoint or uniform placement ties within seed noise. Every claim must first pass a sharpness check (card 04, card 20).
2. **The trivial-endpoint trap.** If `t* = 0` (the earliest numerical mismatch) or `t* = T` (the final gate refusal) almost everywhere, locating `t*` adds nothing beyond [PR #166](https://github.com/manojbajaj95/cl/pull/166) and [PR #165](https://github.com/manojbajaj95/cl/pull/165). A genuine split must sit strictly in `0 < t* < T`, where `t = 0` is non-specific and `t = T` is already too late.
3. **The verifier-mirage trap.** Mistaking a loose interval verifier's straddle for a real dynamical point of no return—or claiming SRW3 "fixes learning" when spending the same compute on one extra branch-and-bound split in the verifier would admit the edit for free (card 21).

### Paper construction (both SRW1 and SRW3 in one 1-gate + momentum-slot system)

Let a scalar rescue pathway have activation `h(w) = ReLU(w)` (gate hyperplane `Σ = {w = 0}`) with momentum slot `m` (`m_{t+1} = m_t + g_t`, `w_{t+1} = w_t - m_{t+1}`, `η = β = 1`). Suppose old task `A` requires a corrective gradient through `h(w)` whenever a refused edit `e` arrives at step `T = 4`; on steps `t = 0…3`, `A` accuracy is untouched (`m_A ≥ 0.7`, floor `0.5`).

1. **Dynamical split (SRW1):** At `t = 0`, source `S` and substitute `W` share identical weights `w_0 = 0.20` and identical outputs, differing only in a tiny slot residual `m_S(0) = 0`, `m_W(0) = +0.05` (earliest numerical mismatch is `t = 0`, harmless on its own). At `t = 1`, a benign `B` batch applies `g_1 = +0.18`:
   - `S` lands at `m_S(1) = 0.18`, `w_S(1) = +0.02 > 0` (gate alive).
   - `W` lands at `m_W(1) = 0.23`, `w_W(1) = -0.03 < 0` (gate dead: `h'(w_W) = 0`).
   - At `t = 2, 3`, both serve `A` and `C` cleanly. At `t = 4`, edit `e` arrives. On `S`, `h'(w_S) = 1`, so one truthful example restores `m_A ≥ 0.5`. On `W`, `h'(w_W) = 0`, so **no gradient-based truthful witness placed at `t ≥ 2` can move `w_W` back across `0`**. Thus `t* = 1` is a strict interior point of no return (`0 < 1 < 4`): placing one truthful witness at `t = 1` (before `w_W` crosses `0`) keeps `w_W(1) > 0` and admits `e`, whereas placing it at `t = 4` fails completely and acting on every `t = 0` slot mismatch wastes budget on benign drift.
2. **Verifier split (SRW3):** Now set `m_W(0) = -0.02`, so `w_W(1) = +0.04 > 0`. The true trajectory never dies and an exact shadow check passes `e` at `t = 4`. However, a cheap interval verifier carries an over-approximation radius `ε = 0.06` around `w_W(1)`, giving `[-0.02, +0.10]`, which straddles `w = 0`. Soundness forces the interval verifier to include the dead-gate branch `h' = 0` and refuse `e` at `t = 4`. Adding a corrective example at `t = 4` cannot remove the straddle at `t = 1`. Spending one truthful example at `t = 1` that shifts `w` by `+0.05` moves the tube to `[+0.03, +0.15] > 0`, eliminating the dead-gate branch from the interval proof **without changing the correction at `t = 4`**.
3. **Caveat:** Replace `ReLU` with `LeakyReLU(0.2)` and the cliff disappears into a smooth cost ramp. Whether real nonlinear CL trajectories sit closer to the hard-gate cliff or the leaky ramp is an empirical question (card 20).

### Prior art and common controls

- **Trajectory divergence & critical periods:** [LMC / spawn point (1912.05671)](https://arxiv.org/abs/1912.05671), [LMC in CL (2010.04495)](https://arxiv.org/abs/2010.04495), [Critical Learning Periods (1711.08856)](https://arxiv.org/abs/1711.08856), and [critical periods in deep linear nets (2308.12221)](https://arxiv.org/abs/2308.12221) show early prefixes can lock in basin or plasticity deficits. Here the split is defined between *source and substitute* with respect to a *specific refused edit and verifier*, not generic SGD noise.
- **Counterexample repair & CEGAR:** [Counterexample-guided neural repair (2301.11342)](https://arxiv.org/abs/2301.11342), [abstraction-refinement verification (1910.14574)](https://arxiv.org/abs/1910.14574), [2207.00759](https://arxiv.org/abs/2207.00759), and [counterexample-guided branching (2603.14823)](https://arxiv.org/abs/2603.14823) alternate verification and refinement. SRW3's baseline is **spending the same compute on one CEGAR verifier refinement** instead of moving the trajectory with an example.
- **Verification-friendly training & condensation:** [ReLU-stability training (1809.03008)](https://arxiv.org/abs/1809.03008), [IBP (1810.12715)](https://arxiv.org/abs/1810.12715), [verification-friendly networks (2412.13229)](https://arxiv.org/abs/2412.13229), [MTT (2203.11932)](https://arxiv.org/abs/2203.11932), [GCR (2111.11210)](https://arxiv.org/abs/2111.11210), and [DAgger (1011.0686)](https://arxiv.org/abs/1011.0686).
- **Sibling tree nodes:** [replay-deadlines (PR #113)](https://github.com/manojbajaj95/cl/pull/113) (smooth decay kill), [first-point-of-loss (PR #134)](https://github.com/manojbajaj95/cl/pull/134) (single-trajectory old-bit erasure), [momentum-fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) (hidden Adam slot memory), [witness-examples (PR #163)](https://github.com/manojbajaj95/cl/pull/163), [finite-edit-guards (PR #164)](https://github.com/manojbajaj95/cl/pull/164), [self-closing-witnesses (PR #165)](https://github.com/manojbajaj95/cl/pull/165), [rejected-edit-witnesses (PR #166)](https://github.com/manojbajaj95/cl/pull/166), and [return-corridors (PR #168)](https://github.com/manojbajaj95/cl/pull/168).
- **Mandatory controls & accounting:** Every idea must beat the stacked baseline of its parts (endpoint counterexample repair + causal-prefix minimization + branch-matched MTT + IBP/ReLU-stability regularizer + PR #168 return corridors) at equal verifier calls, teacher queries, witness bytes (including split metadata), and `B` progress. Evaluate on an independent frozen editor suite; report worst-prefix `A` and `C` retention including rare slices, never counting refusals as retention.

## Idea cards

**P** = conditional primitive candidate (new reusable object or operation). **I** = improvement or audit. All first tests are CPU-scale thought-outlines, not executed results.

### A. Locate and type the split point (SRW1)

#### 01. Counterfactual bisection for the repairability cliff (P)
- **Mechanism:** Given a refused edit `e` at step `T`, binary-search the shadow prefix `t ∈ [0, T]` by testing whether a bounded witness placed at `t` restores safe admission of `e` at `T` (with full-state rollout from `t` to `T`). Output the earliest non-repairable step `t*` and its pre-split state pair `(s_S(t*-1), s_W(t*-1))`.
- **Novelty vs nearest prior art:** Delta debugging and [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 05 shrink a failing input/prefix to preserve *failure*; bisection here locates the phase boundary of *repairability* under a fixed witness grammar, which can sit strictly between earliest numerical mismatch and final failure.
- **Cheapest first test:** Scalar-to-4-unit ReLU learner with Adam slots (paper construction + 10 random seeds, horizon `T = 16`). Compare bisection-placed witnesses (`t*-1`) against endpoint placement (`T`), earliest-mismatch placement (`0`), and causal-prefix minimization at equal shadow-rollout and witness budget.
- **Old-task retention check:** Score independent `A` and `C` (including rare gate-adjacent slices) at every prefix `0…T` and one extra post-`e` refresh; reject if fixing `t*` degrades an untouched `C` slice.

#### 02. Two-sided split typing: dynamical separatrix vs verifier straddle (P)
- **Mechanism:** At the candidate split `t*` found by the cheap verifier, run an exact (or tightened) shadow replay of `S` and `W`. If exact shadow also becomes unrepairable after `t*`, label `κ = dynamical` (route to SRW1 witness placement); if exact shadow stays repairable through `T`, label `κ = verifier` (route to SRW3 tube-clearance).
- **Novelty vs nearest prior art:** [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 04 classifies refusals at `T` (missing witness vs impossible vs uncertain); typing *the split point* localizes where the verifier's over-approximation first bifurcates from truth so the remedy acts at `t_v` rather than `T`.
- **Cheapest first test:** Mix 50% planted dead-gate dynamical splits and 50% planted interval-straddle verifier splits in a 2-unit ReLU toy. Compare typed routing (SRW1 vs SRW3) against untyped corrective-only repair and untyped verifier-refinement at equal total checks and bytes.
- **Old-task retention check:** Score `A` and `C` on independent data after every admitted edit; verify that verifier-typed moves never erode true `A` margin to buy cheap proof clearance.

#### 03. Slot-only split points hidden before weights diverge (P)
- **Mechanism:** Search for split points `t*` where `w_S(t*) = w_W(t*)` and all forward logits match, yet Adam `m` or `v` slots have already crossed a separatrix that will flip a gate under a future batch + refused edit. Place a witness at `t*-1` targeting the slot discrepancy rather than weight distance.
- **Novelty vs nearest prior art:** [Momentum-fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) shows optimizer slots carry hidden state; this turns slot divergence into a localized split address conditioned on a refused edit, beating weight-only state matching ([PR #114](https://github.com/manojbajaj95/cl/pull/114) / [PR #123](https://github.com/manojbajaj95/cl/pull/123) controls: must beat first-gradient and one-step response shortcuts).
- **Cheapest first test:** Paper construction with `w_S(0) = w_W(0)` and matched launch logits/gradients, differing only in Adam `v` (second-moment scale). Compare full-state bisection against weight-only bisection, first-gradient matching, and one-step response matching.
- **Old-task retention check:** Roll out two extra `B` steps after `e` under Adam; score `A` and `C` at every step, flagging delayed momentum overshoot.

#### 04. Split-point sharpness spectrum: cliff vs ramp (I)
- **Mechanism:** Along a refused edit's prefix `t = 0…T`, compute the minimum witness cost `c(t)` (bytes or gradient norm) to restore admission if placed at `t`. Classify each refusal by its maximum step jump `Δ_max = max_t (c(t+1) - c(t))` vs total rise `c(T) - c(0)`.
- **Novelty vs nearest prior art:** Direct diagnostic response to [PR #113](https://github.com/manojbajaj95/cl/pull/113)'s kill of replay deadlines; prevents proposing split-point machinery on smooth hosts where no cliff exists.
- **Cheapest first test:** Compare `c(t)` curves across ReLU, LeakyReLU, GELU, and linear hosts on 20 seeded streams; gate the rest of the node on whether ReLU/Adam exhibits `Δ_max / (c(T) - c(0)) > 0.5` beyond seed noise.
- **Old-task retention check:** Measure `c(t)` strictly among witnesses that hold independent `A` and `C` floors at every prefix; do not count illegal cheap witnesses.

#### 05. Causal split minimization across non-contiguous steps (I)
- **Mechanism:** When a split is caused by a synergy of distant steps (e.g., an early warmup batch that lowers `v` plus a late batch that pushes `w` across `0`), find a minimal cut-set of prefix steps `{t_1, …, t_k}` whose witness intervention prevents the split, rather than assuming a single contiguous prefix.
- **Novelty vs nearest prior art:** Generalizes [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 05 (single causal prefix) to minimal multi-step cut-sets; improvement in diagnosis, not a new CL object on its own.
- **Cheapest first test:** 4-step Adam toy where step 1 shrinks `v` and step 3 pushes `w` over a gate; compare single-step bisection, 2-step cut-set search, and full-trajectory MTT at equal shadow evaluations.
- **Old-task retention check:** Evaluate `A` and `C` across the full unedited `B` stream after applying the cut-set witness; verify that fixing step 1 does not break step 2's `B` progress or `C` retention.

#### 06. Split-placed witness with full-state closure recheck (I)
- **Mechanism:** After placing a witness at `t*-1` and refitting, freeze the updated substitute and re-run the parent's self-closing reachability check ([PR #165](https://github.com/manojbajaj95/cl/pull/165)) over both source and substitute rollouts from `t*-1` through `T`, verifying the *original* refused payload `e` rather than only the split condition.
- **Novelty vs nearest prior art:** Combines SRW1 placement with [PR #165](https://github.com/manojbajaj95/cl/pull/165)'s closure certificate; prevents "split-fixing" that passes at `t*` while opening a new divergence at `t*+2`.
- **Cheapest first test:** Two-gate ReLU toy where fixing gate 1 at `t* = 1` pushes the trajectory across gate 2 at `t = 3`. Compare split-only verification vs full-horizon closure recheck on false-admission rate.
- **Old-task retention check:** Independent `A` and `C` at every prefix `0…T`, plus a held-out second edit `e'` applied after `e`.

### B. Steer away from the verifier's uncertain region (SRW3)

#### 07. Uncertain-region repulsion examples (P)
- **Mechanism:** When `κ = verifier` at `t_v` (exact shadow passes, cheap verifier straddles `Σ`), select a truthful example from today's pool at `t_v - 1` whose update maximizes signed clearance of the verifier's reachable tube from `Σ`, leaving the intended correction at `T` untouched.
- **Novelty vs nearest prior art:** [ReLU-stability training (1809.03008)](https://arxiv.org/abs/1809.03008) and [IBP (1810.12715)](https://arxiv.org/abs/1810.12715) add a loss regularizer over input balls; [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 08 stabilizes gates over all future `B` branches at once. Here a *single refused edit's* verifier split targets one specific `t_v` and hyperplane `Σ` using only truthful data.
- **Cheapest first test:** Paper construction (verifier-split arm) with a 12-example truthful pool. Compare repulsion-example selection at `t_v - 1` against corrective-example addition at `T`, ReLU-stability regularizer (no extra example), and PR #168 global gate-stable selection at equal bytes and accuracy.
- **Old-task retention check:** Independent `A` and `C` before and after `e`, plus margin audit on `A` inputs near `Σ` to ensure repulsion did not silence an active `A` feature.

#### 08. Orthogonal decomposition of an example into correction vs proof clearance (P)
- **Mechanism:** Score every candidate truthful example `x` at step `t` by a 2D vector `(Δ_corr(x), Δ_proof(x))`: change in exact shadow admissibility of `e` vs change in the cheap verifier's over-approximation volume at `t_v`. Track the Pareto frontier to separate examples that teach behavior from examples that buy cheap proofs.
- **Novelty vs nearest prior art:** Extends [PR #165](https://github.com/manojbajaj95/cl/pull/165) card 15 and [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 13 by factoring a single example's value against an exact oracle vs cheap verifier on the *same* refused edit.
- **Cheapest first test:** Exhaustive 2-gate ReLU pool (20 truthful examples); test whether `Δ_corr` and `Δ_proof` have low rank correlation (`|ρ| < 0.3`) and whether picking high-`Δ_proof` / zero-`Δ_corr` examples beats correction-only selection on admitted jobs per byte. Gate on target variance across seeds.
- **Old-task retention check:** Score `A`, `C`, and rare slices for the top examples on each axis; verify that pure proof-clearance examples do not sacrifice `A` margin relative to equal-count random truthful examples.

#### 09. Split-avoidance vs verifier-refinement arbitrage (P)
- **Mechanism:** At each verifier split `t_v`, price two operations in a common currency (verifier FLOPs + persisted bytes): (a) spend one truthful example to push the tube off `Σ` (SRW3), or (b) spend one CEGAR refinement step ([2603.14823](https://arxiv.org/abs/2603.14823)) to tighten the verifier around `Σ`. Choose (a) only when moving the trajectory amortizes across multiple future edits sharing `Σ`.
- **Novelty vs nearest prior art:** CEGAR always refines the verifier; certified training always moves the model. Treating trajectory movement and verifier refinement as interchangeable moves over a shared split `Σ` is a new control surface if amortization beats either pure strategy.
- **Cheapest first test:** Stream of 10 frozen edits where 6 hit the same verifier straddle `Σ_1` and 4 hit distinct one-off straddles. Compare pure SRW3, pure CEGAR refinement, and amortized arbitrage at equal total compute and bytes.
- **Old-task retention check:** Independent `A` and `C` after all 10 edits; ensure amortized trajectory moves never accumulate drift that breaks a late `C` floor.

#### 10. Multi-verifier split consensus (I)
- **Mechanism:** Run two cheap verifiers with different abstractions (e.g., interval box and zonotope) over the shadow prefix. Splits that appear in only the weaker verifier are tagged as *abstraction artifacts* (candidates for verifier upgrade, not permanent memory); splits present in both are prioritized for SRW3 repulsion.
- **Novelty vs nearest prior art:** [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 20 audits verifier-manufactured memory post hoc; consensus uses two abstractions online to prevent spending witness bytes on weak-verifier artifacts.
- **Cheapest first test:** 2-unit ReLU toy with correlated weights where an interval box splits but a zonotope does not; compare consensus-gated SRW3 against interval-only SRW3 on wasted witness bytes and admitted edits.
- **Old-task retention check:** Same independent `A` and `C` floors across all arms; verify that skipping interval-only splits never admits an unsafe edit.

#### 11. Tube-pinching before a gate bottleneck (I)
- **Mechanism:** Rather than shifting the trajectory mean away from `Σ` (which can shift `A` outputs), choose a truthful example at `t_v - 1` whose local Hessian contracts the verifier's *interval radius* along `Σ`'s normal, pinching the tube so it clears `Σ` at the same mean state.
- **Novelty vs nearest prior art:** Combines SRW3 with [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 03 (obligation contraction); an improvement when mean-shifting examples violate an `A` margin floor.
- **Cheapest first test:** Symmetric two-sided gate (`w ∈ [-0.1, +0.1]` safe, dead outside) where any mean shift hits the opposite gate; compare tube-pinching examples vs mean-shifting SRW3 vs IBP regularizer.
- **Old-task retention check:** Check `A` margins on both sides of the corridor and `B` plasticity along orthogonal directions (rule out rigid freezing).

### C. Split points as reusable, composable continual-learning objects

#### 12. Reusable split-boundary atlas across unseen editors (P)
- **Mechanism:** Record each discovered split as a compact object `(Σ_i, κ_i, W_pre,i, scope_i)` keyed to the gate/invariant hyperplane `Σ_i`, not the refusing edit `e`. When a later independent editor proposes a disjoint edit `e'`, check whether `e'`'s shadow trajectory approaches any stored `Σ_i`; if so, apply `W_pre,i` proactively without re-running full bisection.
- **Novelty vs nearest prior art:** [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 01 reuses an endpoint repair target; an atlas reuses the *dynamical separatrix* itself across distinct edits and editors, turning split points into a persistent geometric index.
- **Cheapest first test:** 4-unit ReLU host with 2 hidden gate bottlenecks and 2 independent committed editors with disjoint payloads hitting the same bottlenecks. Compare atlas reuse against fresh bisection, [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 01, and matched CEGIS + MTT at equal checks and bytes.
- **Old-task retention check:** Independent `A` and `C` after every editor's edit; explicitly test a false-hit edit that approaches `Σ_i` from the safe side to confirm zero negative transfer.

#### 13. Split-point equivalence classes of refused edits (P)
- **Mechanism:** Partition refused edits by whether they trigger the *same earliest split* `(t*, Σ)` under the frozen continuation law, even if their payloads and final errors at `T` look completely different. Maintain one pre-split witness per split class and split the class only when a continuation separates their pre-split remedies.
- **Novelty vs nearest prior art:** [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 07 groups refusals by shared endpoint correction; grouping by *earliest split* can collapse edits whose final errors diverge wildly after the same bifurcation, reducing witness count strictly below endpoint classes.
- **Cheapest first test:** Plant 6 refused edits with 6 distinct final error patterns at `T = 6` that all stem from 2 early gate splits at `t* = 2`. Compare split-class witnesses against endpoint-correction classes ([PR #166](https://github.com/manojbajaj95/cl/pull/166) card 07) and [GCR](https://arxiv.org/abs/2111.11210) gradient clustering on witness bytes and held-out admission.
- **Old-task retention check:** Score `A` and `C` on all 6 edits and 4 unseen edits; penalize any over-merged class that causes a floor breach on an unseen edit.

#### 14. Cascading split chains and fixed-point termination (P)
- **Mechanism:** When placing `W_pre,1` before `t*_1` shifts the trajectory onto a new separatrix `Σ_2` at `t*_2` for another old task, record the directed edge `Σ_1 → Σ_2` and solve jointly for a pre-split witness set that clears the entire strongly connected component (or certifies incompatibility if a cycle exists).
- **Novelty vs nearest prior art:** Standard CEGIS loops can oscillate when fixing one counterexample creates another; tracking the *split-dependency graph* gives a finite structural criterion for when a repair loop converges vs cycles.
- **Cheapest first test:** 2-gate coupled ReLU toy where clearing gate 1 pushes the trajectory across gate 2, with a third truthful example that clears both simultaneously. Compare naive sequential SRW1, joint split-chain repair, and exhaustive finite search.
- **Old-task retention check:** Verify both old tasks `A_1`, `A_2`, and unrelated `C` at every prefix; confirm cycles return an explicit `incompatible` verdict rather than looping or silently dropping `A_2`.

#### 15. Non-commuting split ordering (P)
- **Mechanism:** Given two refused edits `e_1, e_2` with split points `t*_1 < t*_2` on shared gates/slots, test whether repairing `t*_1` first shifts or eliminates `t*_2` (causal dominance) whereas repairing `t*_2` first leaves `t*_1` broken. Schedule witness refits in topological split-time order rather than arrival order.
- **Novelty vs nearest prior art:** [PR #156](https://github.com/manojbajaj95/cl/pull/156) and [PR #158](https://github.com/manojbajaj95/cl/pull/158) order *writes* by preconditions; this orders *split repairs* by causal prefix time `t*`, even when `e_2` arrived before `e_1`.
- **Cheapest first test:** Two refused edits on a 2-unit Adam toy where `e_2` arrives first (`t*_2 = 4`) and `e_1` arrives second (`t*_1 = 1`) and `t*_1`'s repair automatically resolves `t*_2`. Compare arrival-order repair, reverse-time repair, and split-time topological repair on total witness bytes and verifier calls.
- **Old-task retention check:** Score `A` and `C` under both orders after all refits; verify that eliminated splits are still independently rechecked on `e_2`'s original payload.

#### 16. Split-aware teacher retirement summaries (P)
- **Mechanism:** Before retiring the source teacher `S`, discard bulk trajectory logs and retain only `S`'s exact state/gradient collar `[t* - Δ, t*]` around discovered separatrices `Σ_i`. After retirement, diagnose new refusals against these collars and abstain whenever a new split falls outside all retained collars.
- **Novelty vs nearest prior art:** [PR #163](https://github.com/manojbajaj95/cl/pull/163) and [PR #165](https://github.com/manojbajaj95/cl/pull/165) card 12 summarize the source over the full horizon; focusing teacher retention on narrow pre-split collars tests whether a tiny fraction of trajectory bytes preserves most post-retirement repairability.
- **Cheapest first test:** Retire `S` on a 16-step ReLU stream under a fixed byte cap; compare pre-split collar summaries against uniform-stride checkpoints, endpoint summaries, and [MTT](https://arxiv.org/abs/2203.11932) at equal retained bytes on post-retirement unseen edits.
- **Old-task retention check:** Overwrite `S` before evaluation; score independent `A`, `C`, and abstention rate on unseen edits, ensuring the substitute never fabricates teacher answers outside retained collars.

#### 17. Cross-host split transport via bifurcation topology (P)
- **Mechanism:** Export a split not as weight coordinates but as an invariant behavioral signature (the pair of inputs/batches whose activation-sign flip order changes across `t*`, plus the truthful pre-split witness). On a re-initialized or permuted host, test whether locating the homologous sign-flip step transfers split prevention without transferring weights.
- **Novelty vs nearest prior art:** [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 08 and [MEND](https://arxiv.org/abs/2110.11309) transport edit effects; this tests whether the *locus of irreversibility* is an invariant of the task+data stream rather than one random seed's coordinates.
- **Cheapest first test:** Train two 4-unit ReLU hosts with permuted units and different seeds on the same `A → B` stream; test whether the behavioral split signature from host 1 finds `t*` on host 2 faster than fresh bisection and beats random-step placement.
- **Old-task retention check:** Evaluate host 2's own independent `A` and `C` references after applying the transported witness and checking the original refused payload.

### D. Active probing, pricing, and falsification audits

#### 18. Pre-emptive split probing before any edit is refused (P)
- **Mechanism:** During normal training, run cheap synthetic shadow perturbations (sampled from the declared legal-edit ball, without waiting for a real refusal) to detect steps `t` where two nearby trajectories cross a gate or where the verifier's interval straddles `Σ`. Pre-emptively place a truthful clearance example when clearance drops below a threshold.
- **Novelty vs nearest prior art:** Reactive SRW1/SRW3 waits for a refused edit; pre-emptive probing turns split detection into an online regularization/data-selection primitive. Must beat passive [ReLU-stability](https://arxiv.org/abs/1809.03008) and random-step probing at equal compute.
- **Cheapest first test:** 4-unit ReLU stream followed by a blind suite of 10 frozen edits. Compare pre-emptive shadow-probe clearance, reactive SRW1/SRW3 on the first 3 edits, ReLU-stability regularizer, and unshaped training at equal total verifier calls and data budget.
- **Old-task retention check:** Score `A` and `C` across all 10 blind edits plus `B` acquisition speed; penalize pre-emptive moves that slow `B` beyond a matched stiffness baseline.

#### 19. Split-horizon pricing: the irreversibility tax curve (I)
- **Mechanism:** For each discovered split `t*`, measure the extra witness bytes and lost `A` margin incurred by delaying intervention by `Δ = 0, 1, 2, …` steps past `t*`. Use the resulting slope to prioritize which pending splits must be repaired immediately vs deferred.
- **Novelty vs nearest prior art:** Schedules consolidation by measured irreversibility slope rather than loss or staleness; improvement over uniform or FIFO repair scheduling (and must beat [PR #113](https://github.com/manojbajaj95/cl/pull/113)'s flat-timing null).
- **Cheapest first test:** Queue 4 concurrent splits with different post-`t*` cost slopes under a 1-witness-per-step budget; compare slope-prioritized repair against FIFO, earliest-`T`, and largest-current-error scheduling.
- **Old-task retention check:** Worst-prefix `A` and `C` across the entire queue; verify that deferring a low-slope split never lets it silently cross an unrecoverable cliff.

#### 20. The smooth-decay null (PR #113 stress test) (I)
- **Mechanism:** Directly attempt to kill SRW1 by testing whether realistic nonlinear training (ReLU vs GELU/SiLU, weight decay, Adam, mini-batch noise) actually produces sharp interior splits `0 < t* < T` with `c(t)` cliffs, or whether repairability decays smoothly so that any prefix placement ties within seed variance.
- **Novelty vs nearest prior art:** Mandatory falsification audit drawn directly from [PR #113](https://github.com/manojbajaj95/cl/pull/113) and the [idea ledger](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/idea-ledger.md)'s target-variance gate.
- **Cheapest first test:** 10-seed sweep on a small 2-layer MLP (`width ∈ {8, 32}`) with ReLU and GELU under Adam and SGD; report the fraction of refused edits with a strict interior cliff (`0 < t* < T`, jump > 2× seed SD). If < 10%, demote split points to a ReLU-specific corner case.
- **Old-task retention check:** Match `A`, `C`, and `B` progress across activation families so differences in cliff rate are not artifacts of underfitting or margin mismatch.

#### 21. Verifier-tightening compile-away audit (I)
- **Mechanism:** Take every compute unit (shadow rollouts, gradient evaluations, verifier calls) spent by SRW3 searching for a truthful repulsion example and give it instead to the baseline to tighten the verifier (e.g., one extra branch-and-bound split, tighter LP/zonotope pass, or [CEGAR branching 2603.14823](https://arxiv.org/abs/2603.14823)). SRW3 survives only if moving the trajectory beats tightening the checker on *future unseen edits*.
- **Novelty vs nearest prior art:** The exact compile-away test for SRW3 (analogous to [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 22).
- **Cheapest first test:** 2-gate ReLU toy with interval verifier vs 1-split branch-and-bound vs SRW3 repulsion example, evaluated on 10 unseen frozen edits from an independent editor. Compare total compute, proof bytes, and admitted utility.
- **Old-task retention check:** Both arms face identical independent `A` and `C` floors; tightening the verifier cannot change `A`/`C` at all, so any `A`/`C` drop from SRW3's trajectory move is charged directly against SRW3.

#### 22. Split-placement vs stacked endpoint-repair + MTT ablation (I)
- **Mechanism:** Head-to-head comparison at strictly equal shadow checks, teacher queries, and persisted bytes: (1) SRW1 pre-split witness at `t*-1`, (2) endpoint counterexample-guided repair at `T` ([2301.11342](https://arxiv.org/abs/2301.11342)), (3) earliest-mismatch witness at `t = 0`, (4) causal-prefix minimization ([PR #166](https://github.com/manojbajaj95/cl/pull/166) card 05) + branch-matched [MTT](https://arxiv.org/abs/2203.11932), and (5) [PR #168](https://github.com/manojbajaj95/cl/pull/168) return-corridor selection.
- **Novelty vs nearest prior art:** Enforces the ledger's merge rule: SRW1 + SRW3 must beat the union of their parts' strongest baselines on an independent frozen editor suite.
- **Cheapest first test:** Coupled Adam ReLU learner (`T = 12`) with planted dynamical and verifier splits plus ordinary smooth refusals; score admitted frozen-edit utility, proof bytes, and worst-prefix retention across 10 seeds.
- **Old-task retention check:** Independent `A`, `C`, and rare slices at every visible prefix `0…T`, plus a post-retirement check with source reads blocked and overwritten.

## Ranked deeper questions

1. **Do realistic nonlinear training trajectories actually have sharp interior points of no return (`0 < t* < T`), or only smooth repair-cost ramps?** Start with cards 01, 04, and 20. Measure `c(t)` across ReLU, GELU, SGD, and Adam at matched margins and `B` progress. If repair cost decays smoothly with no cliff above seed noise (as in [PR #113](https://github.com/manojbajaj95/cl/pull/113)), stop—the "irreversible split point" is not a real dynamical object outside contrived hard-gate toys.
2. **Does a split hyperplane discovered by one refused edit transfer to unseen edits from an independent editor?** Cards 12, 13, and 22. Compare a split-boundary atlas against [PR #166](https://github.com/manojbajaj95/cl/pull/166) endpoint witnesses and stacked CEGIS + causal-prefix minimization + MTT at equal checks, bytes, and `A`/`C` floors. Transfer across disjoint edits is the decisive test for whether a split point is a reusable **primitive** rather than a per-edit timing improvement.
3. **When a cheap verifier refuses an edit that exact shadow admits, does spending a truthful example to clear the verifier's uncertain region (SRW3) beat spending the same compute to tighten the verifier?** Cards 02, 07, 08, 09, and 21. Score on future unseen edits and independent `A`/`C` retention. If one CEGAR refinement step beats trajectory repulsion at equal compute, SRW3 is only a workaround for a weak checker.
4. **Can split-point structure survive teacher retirement and host re-parameterization?** Cards 16 and 17. Test whether retaining narrow pre-split collars `[t* - Δ, t*]` preserves post-retirement repairability better than equal-byte checkpoints/MTT, and whether the bifurcation topology transfers across seeds/permutations without raw weight alignment.
