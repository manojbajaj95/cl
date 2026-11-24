# Return corridors: shape tomorrow's branches so one small proof covers them

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Self-closing witnesses](self-closing-witnesses.md) ([PR #165](https://github.com/manojbajaj95/cl/pull/165)), cards 14 and 15. **Review seed:** [Flood triage row 263](https://github.com/manojbajaj95/cl/blob/563fd7a57adeb1bca9464bd071885ef27476e6d5/reviews/flood-triage.md#L263), two score-3 directions: choose today's examples so distinct B branches later re-enter a shared region one small certified buffer covers; spend an example to shrink the proof rather than to improve accuracy. **Ledger read first:** [idea ledger](https://github.com/manojbajaj95/cl/blob/563fd7a57adeb1bca9464bd071885ef27476e6d5/reviews/idea-ledger.md) (stacked ideas must beat stacked parts; no credit for "true by construction"; margin confounds; gate every pilot on target variance).

## Is shaping future training trajectories for cheap certification a new object for continual learning?

**Partly.** Each ingredient exists:

- **Shaping future training trajectories** is meta-learning ([MAML](https://arxiv.org/abs/1703.03400), [La-MAML](https://arxiv.org/abs/2002.09571)), [MER](https://arxiv.org/abs/1810.11910)-style gradient alignment, look-ahead selection ([HAL](https://arxiv.org/abs/2002.08165), [Premonition](https://arxiv.org/abs/2403.07356)), and, most directly, tamper resistance ([TAR](https://arxiv.org/abs/2408.00761)), which meta-trains weights so that *future* fine-tuning trajectories stay in a chosen region. Iterative machine teaching ([1705.10470](https://arxiv.org/abs/1705.10470)) chooses examples to steer a gradient learner.
- **Training for cheap verification** is [ReLU-stability training](https://arxiv.org/abs/1809.03008), [verification-friendly networks](https://arxiv.org/abs/2412.13229), set-based and [interval-bound](https://arxiv.org/abs/1810.12715) certified training.
- **Steering many trajectories into one region a certified controller covers** is the sequential composition of funnels (Burridge, Rizzi and Koditschek 1999; LQR-trees, Tedrake 2010; funnel libraries, Majumdar and Tedrake 2017), with contraction analysis (Lohmiller and Slotine 1998) for why trajectories merge.
- **Branches naturally merging** is [linear mode connectivity](https://arxiv.org/abs/1912.05671): after early training, SGD copies with different data orders end in one linearly connected basin; [Mirzadeh et al.](https://arxiv.org/abs/2010.04495) use this in CL.

What none of them does is the combination this node needs: the certified object is the **learner-state trajectory under the declared future training law** (not an input ball around one fixed network), the steering is done **only by today's truthful training data** (not an online controller, a meta-learned update rule or an adversarial outer loop), and the quantity optimized is **the size of a checkable substitution proof for a retired source** (not loss, robustness radius or retention alone).

The candidate object is a **return corridor**: a triple (today's subset `D`, an *entry funnel* certificate that every legal B branch from the post-`D` state enters a region `C` by step `τ` while old-task floors hold on the way, and *one* buffer `W` certified on `C` as in the parent's `R₀…R_H` chain). The candidate operation is **teach-to-certify**: spend example quota to lower `m(D)`, the minimum certified bytes, at matched today-accuracy, B progress and A/C floors. It is a primitive only if corridors compose or transfer (cards 14–16) in ways that the stack of look-ahead selection, joint MTT, certified training on the tube, meta-learning against the same verifier, and exact retirement cannot match at equal cost. Otherwise it is an improvement in how those tools are aimed. Three things could make the whole idea vacuous, and every card below is written against them:

1. **The natural corridor.** If branches already share a basin after a short spawn time (the Frankle et al. stability point), data shaping buys nothing beyond waiting. Measure the free corridor first.
2. **The rigid corridor.** A strongly contracting region is easy to certify because nothing moves there. Freezing, a tiny learning rate, saturated units or lazy width give tiny proofs and no learning. Every claim is a point on a frontier of certified bytes vs B progress and later plasticity, never bytes alone.
3. **The erased branch.** Merging branches that learned *different* B content would erase that content. Only the coordinates the witness obligation reads may merge (below).

### What must merge: the obligation quotient

The parent's discrepancy on a state `s` and legal batch `b` is `e(s,b) = d(F_src(s,b), F_wit(s,b))`. Usually it depends on `s` only through a projection `π(s)` (the weights, slots and clocks the source's correction reads, restricted to the probe inputs that drive it). Two branches need not meet in full state; they need only meet in `π`. A corridor is therefore a **merge in the obligation quotient**, while B-specific content lives in coordinates `e` does not read. This differs from [synchronizing consolidation (PR #108)](https://github.com/manojbajaj95/cl/pull/108), which showed that an injective update on the *edit-behaviour* quotient can never be collapsed by a finite word: here the quotient is defined by what the substitution proof must cover, and the merge comes from contraction of the training map along `π`, which today's data can add.

**Paper construction.** Let `s = (u, v)`, with the witness obligation reading only `u` and B content living in `v`. Two legal B orders leave `u₁, u₂` at distance `δ` after the separating batch. Along `u` the B update is `u ← u − η(a(u − u*))`, contraction factor `ρ = 1 − ηa`. A truthful labeled example consistent with A, whose gradient lies in `u`, adds curvature `a'`, giving `ρ' = 1 − η(a + a')`. After `k` steps the branch gap is at most `ρ'^k δ`. If `g` is the nearest ReLU gate to `u*` along `u`, once the reachable ball radius falls below `dist(u*, g)` the corridor sits in one activation cell, the training map is affine there, and one linear invariant plus one buffer certifies it. Entry takes about `τ = log(δ / dist(u*, g)) / −log ρ'`. The example buys a shorter transient and a single-cell proof; it pays by moving `u*` (it must stay correct for A) and by stiffening `u` (any B task that needs `u` learns more slowly). Before entry, each branch still needs its own coverage: the corridor shortens the separate-cover phase, it does not delete it.

### What to price

Fix the parent's frozen future law (start, legal batch orders, horizon, update code, numerics, sampler) before choosing `D`. Price `m(D) = |W| + |entry proof| + Σ_branches |transient cover before τ| + region/automaton bytes`, plus build-side source queries and verifier work counted separately. Compare at the same example quota, the same today-accuracy on independent A/C data (or report the accuracy given up per byte saved), and the same B progress on every branch. Report the natural-corridor baseline `m(∅ at τ_free)`. A corridor win must come from learned nonlinear trajectories, not a planted surcharge.

### Closest prior art and common controls

- **Natural merge:** run branches with no shaping and measure their LMC/spawn point ([1912.05671](https://arxiv.org/abs/1912.05671), [2010.04495](https://arxiv.org/abs/2010.04495)).
- **Proof-aware training without examples:** a ReLU-stability or interval-bound regularizer ([1809.03008](https://arxiv.org/abs/1809.03008), [2412.13229](https://arxiv.org/abs/2412.13229)) applied over the reachable weight tube, at matched today-accuracy. If a regularizer does what the examples do, the example is only a delivery vehicle.
- **Trajectory shaping for accuracy:** MER, HAL, Premonition and direct post-refresh bilevel selection, each stacked with joint MTT ([2203.11932](https://arxiv.org/abs/2203.11932)) and the parent's verifier.
- **Meta-learned future trajectories:** TAR-style outer loop ([2408.00761](https://arxiv.org/abs/2408.00761)) with the verifier cost as its objective, restricted to the same truthful example pool.
- **Certified retention:** [Certified CL](https://arxiv.org/abs/2407.06697), [InterContiNet](https://arxiv.org/abs/2206.07996), [CABA held-out anchors](https://arxiv.org/abs/2610.40740).
- **Ceiling:** exhaustive joint search over subsets, buffer grammar and proof grammar in finite toys; it is a ceiling, not a baseline to beat.
- **Retention rules from the ledger:** old tasks A/C on independent data never used for fitting, selection or calibration; scored at every visible prefix including the transient before re-entry, after source overwrite and after B reuse; rare slices and refusals reported; per-item margins matched before attributing any ordering. **P** = conditional primitive candidate; **I** = improvement or audit.

## Idea cards

### Build the corridor

#### 1. Compile an entry funnel from today's data (P)
- **Mechanism:** Treat each legal B branch as a trajectory of the training map. Choose `D` so that every branch's reachable set at some `τ` lies inside a region `C` certified for one buffer, and certify the funnel `R₀ → … → R_τ ⊆ C` with the parent's set-chain checker. The output is `(D, funnel proof, C, W)`.
- **Novelty vs nearest prior art:** Funnel composition and LQR-trees certify convergence under an online controller; here the only control is a fixed truthful dataset chosen before the future runs, and the cost is substitution bytes. TAR shapes future trajectories empirically, without a proof.
- **Cheapest first test:** Two-unit ReLU learner, two legal B orders separated by one labeled batch, a quantized pool of 12 truthful A-consistent examples. Exhaust all subsets of size 2; for each, compute natural-corridor `m`, shaped `m`, and the stacked baseline (HAL selection + joint MTT + same verifier).
- **Old-task retention check:** Score A/C at every prefix on both orders, including before `τ`; a dip in the transient fails the card even if `C` is safe.

#### 2. Hide branch differences where the witness cannot see them (P)
- **Mechanism:** Instead of merging branches, select examples that route the B-order differences into units or directions the obligation quotient `π` ignores (gates stably off on witness probe inputs, or directions the source's correction never reads). Branches stay different in `v` but coincide in `π`.
- **Novelty vs nearest prior art:** Masks and subspace methods (PackNet, GPM) separate *tasks*; this separates *order nuisance* from *proof-relevant state*, with the separation induced by data rather than a mask.
- **Cheapest first test:** Three-unit ReLU learner where one unit is read by the source correction and two are not. Compare a selector maximizing post-`D` gap in `π` vs in full state; measure whether separate per-branch buffers collapse to one.
- **Old-task retention check:** A/C on both orders after overwrite; also verify that the hidden units do not later feed A through a gate that opens under a legal batch (search for it explicitly).

#### 3. Add contraction only along the obligation (P)
- **Mechanism:** Pick examples whose loss curvature lies in `π` (paper construction above), so the training map contracts there under a certified contraction metric, while leaving the curvature in B's coordinates unchanged.
- **Novelty vs nearest prior art:** Contraction analysis certifies dynamical systems; curvature-shaping regularizers (EWC, SAM) add stiffness for retention or flatness. The use is to make *different futures* converge in proof-relevant coordinates only.
- **Cheapest first test:** Linear-in-`u`, ReLU-in-`v` toy. Compare examples aimed at `π` curvature vs equal-norm EWC-style stiffness on `u` vs random truthful examples; report entry time `τ`, proof bytes and B progress in `v`.
- **Old-task retention check:** A/C at the new fixed point `u*'` vs the old one: added curvature must not shift `u*` across an A decision; check rare slices near that decision.

#### 4. A truthful synchronizing prefix (I)
- **Mechanism:** Include in today's data a short truthful sequence whose effect is to map many quotient states to few, the analogue of a synchronizing word, but on the obligation quotient. Inherits PR #108's obstruction: if the B updates are injective on `π`, no data can synchronize it; the card must exhibit non-injectivity (saturation, dead gates, weight decay).
- **Novelty vs nearest prior art:** Černý reset words and PR #108; the change is the quotient, which is why the obstruction may not apply.
- **Cheapest first test:** Enumerate a quantized 2-unit learner's quotient transition table under legal batches; find the shortest truthful synchronizing prefix if any; compare with simply waiting for the natural merge.
- **Old-task retention check:** A/C before and after the prefix; a prefix that synchronizes by erasing A (destructive reset) is the PR #108 failure and counts as a loss.

#### 5. The shared-bottleneck corridor, exhaustively (I)
- **Mechanism:** Parent card 14's construction made exact: a separating labeled example, then two legal orders through a shared bottleneck. Compute shared vs separate buffer sizes and the transient cover.
- **Novelty vs nearest prior art:** This is the baseline construction for the node, not a new mechanism.
- **Cheapest first test:** Exhaust the finite tree; compare exact return-aware search, direct post-refresh bilevel selection stacked with joint MTT, and MER at equal example count.
- **Old-task retention check:** Score A/C on each branch before and after the merge; a temporary failure cannot be hidden by the return.

#### 6. Measure the free corridor before buying one (I)
- **Mechanism:** For each start and legal branch family, find the earliest step at which branches enter a common certifiable region with no shaping at all (an LMC-style spawn point under the frozen law). Shaping is credited only for `m` below that.
- **Novelty vs nearest prior art:** Frankle et al.'s instability analysis and Mirzadeh et al.; this is the audit that kills a "corridor" that SGD supplies for free.
- **Cheapest first test:** In the same toys, plot `m` vs start time with no `D`; compare with shaped `m` at the same total steps.
- **Old-task retention check:** A/C across the waiting period; waiting is only a valid baseline if the old floors hold while waiting.

#### 7. Trade transient cover against entry time (I)
- **Mechanism:** Optimize `D` for total bytes including the per-branch cover before `τ`, not just the shared buffer after. A fast but violent entry may need more transient cover than a slow gentle one.
- **Novelty vs nearest prior art:** Minimum-time vs minimum-energy funnels in control; the parent's overlap and timing accounting (cards 16 and 18). Improvement of the accounting.
- **Cheapest first test:** Sweep candidate examples in the paper construction by added curvature `a'`; plot transient bytes, buffer bytes and their sum against `τ`.
- **Old-task retention check:** Worst-prefix A/C for each `a'`; report the `a'` where transients first breach a floor.

### Spend examples on the proof

#### 8. Gate-stable tubes (P)
- **Mechanism:** Lift ReLU-stability training from input balls to the learner-state tube: choose examples so that, for every witness probe input, each hidden unit's sign is constant over all reachable states in `C`. The substitution proof becomes linear (one activation pattern) instead of a branch-and-bound over gate crossings.
- **Novelty vs nearest prior art:** [1809.03008](https://arxiv.org/abs/1809.03008) and [2412.13229](https://arxiv.org/abs/2412.13229) stabilize neurons over *input* perturbations of one fixed network; this stabilizes them over *parameter* trajectories induced by future training.
- **Cheapest first test:** Two-gate ReLU learner; equal-count subsets where only one keeps both gates stable over the tube. Count unstable gate-state pairs, verifier nodes and proof bytes; control with the same stability regularizer applied with no examples.
- **Old-task retention check:** A/C with and without the stabilizing examples at matched today-accuracy; a stabilized gate that silences an A feature fails.

#### 9. Select by verifier work, not by a surrogate (P)
- **Mechanism:** Score candidate subsets by the actual work of the frozen verifier on the future tube (nodes, LP calls, proof bytes), and keep only subsets within a today-accuracy tolerance. Compare with surrogates (unstable-gate count, margin to nearest gate).
- **Novelty vs nearest prior art:** Verification-cost-aware training uses differentiable surrogates; here the target is the true proof cost under future dynamics. The likely outcome is a good surrogate; that would demote the card to an improvement.
- **Cheapest first test:** Exhaust subsets in the two-gate toy; Spearman of each surrogate with true verifier work; gate first on whether true work varies more than across seeds (ledger rule).
- **Old-task retention check:** For the top subsets by each score, A/C after overwrite and B reuse, including rare slices.

#### 10. A corridor where training is affine (P)
- **Mechanism:** Aim for a corridor in which the full training map (weights and optimizer slots) is affine, so one ellipsoidal invariant certifies every branch. Achieve it through activation-pattern stability from data, not through width or a lazy parameterization.
- **Novelty vs nearest prior art:** NTK/lazy training gives affine dynamics by width, and the ledger already shows lazy width is what reduces forgetting under SP; this card must beat a laziness-matched control.
- **Cheapest first test:** Same toys at fixed width; compare data-induced affine corridors with a width- or scale-induced lazy arm matched on B progress.
- **Old-task retention check:** A/C plus a plasticity probe (a fresh task C' after the corridor); a corridor that is affine because the learner stopped learning fails.

#### 11. Fold branches by a symmetry (P)
- **Mechanism:** Choose examples so the two branches are images of each other under a symmetry of the training map (e.g. a unit permutation or sign flip that swaps the order effect). Certify one fundamental domain and transport the proof through the symmetry.
- **Novelty vs nearest prior art:** Equivariant verification and Git Re-Basin-style permutation alignment exist; the claim is that today's data can *create* the symmetry between future branches, halving proof bytes.
- **Cheapest first test:** Two-unit learner with a swap symmetry broken by one example; select examples that restore it on the reachable tube; compare to certifying both branches.
- **Old-task retention check:** A/C on both branches; check the symmetry does not also swap an A decision.

#### 12. Buy a coarser buffer grammar (I)
- **Mechanism:** Spend examples so the corridor tolerates a lower-precision buffer (fewer bits per witness value), reducing bytes without changing the number of witnesses.
- **Novelty vs nearest prior art:** Quantization-aware training; parent card 9. Improvement.
- **Cheapest first test:** Two precisions, exhaustive continuations; bytes saved per example spent vs quantization-aware fitting.
- **Old-task retention check:** A/C at deployed precision after reuse; float-only passes flagged.

#### 13. The exchange rate between accuracy and proof (I)
- **Mechanism:** For each candidate example measure two marginal values: today-accuracy gained and proof bytes saved. The seed claim is that some examples sit far off the accuracy axis: almost no accuracy, many bytes. Map the frontier.
- **Novelty vs nearest prior art:** Accuracy–verifiability trade-offs are reported for certified training; this measures them per example for future-trajectory proofs.
- **Cheapest first test:** Score every pool example in the toys on both axes; check whether the top bytes-saved examples differ from the top accuracy examples beyond seed noise.
- **Old-task retention check:** A/C for a subset chosen purely for bytes vs purely for accuracy, at equal count.

### Make corridors reusable

#### 14. A corridor as a public entry port (P)
- **Mechanism:** Publish `C`, `W` and the entry condition. A later independent learner with its own data inherits the buffer certificate if it proves only that its own trajectory enters `C` by `τ` and stays; it never re-checks `W` on `C`.
- **Novelty vs nearest prior art:** Assume-guarantee contracts (e.g. Pacti) and [unannounced consumers (PR #162)](https://github.com/manojbajaj95/cl/pull/162). The specific operation is reusing a training-time substitution proof by proving entry only.
- **Cheapest first test:** Freeze the corridor, then reveal a second B family designed blind. Compare entry-only checking with full recertification and with refitting a fresh buffer; count verifier work and admitted jobs.
- **Old-task retention check:** A/C under the second family after overwrite; a failed entry proof must refuse, and refusals are charged.

#### 15. Nested corridors across a task stream (P)
- **Mechanism:** Each new task's corridor is chosen inside the previous one, so certificates compose as a chain `C₁ ⊇ C₂ ⊇ …` and old buffers stay valid without rechecking.
- **Novelty vs nearest prior art:** InterContiNet keeps weights inside task-wise intervals for retention; this nests *substitution proofs*, not parameter boxes. Funnel libraries nest by construction.
- **Cheapest first test:** Three-task stream in the two-gate toy; compare nested corridors with recertifying each buffer every task and with InterContiNet intervals at equal bytes.
- **Old-task retention check:** A/C for all earlier tasks at every prefix; measure whether nesting starves later tasks (plasticity probe).

#### 16. Declared exits (P)
- **Mechanism:** The corridor declares which legal futures leave it (a larger learning rate, a batch family outside the funnel) and attaches a fallback: keep the source, or a pre-priced refusal. The certificate covers "inside or declared exit", not "everything".
- **Novelty vs nearest prior art:** Backup control barrier functions and contingency filters do this for control; the parent's refusal accounting does it for one buffer.
- **Cheapest first test:** Add one exit branch to card 1's toy; compare total cost with a corridor stretched to cover it.
- **Old-task retention check:** A/C on exit branches under the fallback; postponed refusals count as failures.

### Robust and stochastic corridors

#### 17. Worst-branch corridor (I)
- **Mechanism:** Choose `D` to minimize the worst `m` over a precommitted family of B objectives, not expected loss.
- **Novelty vs nearest prior art:** Robust bilevel selection and Premonition; parent card 17. Improvement.
- **Cheapest first test:** Blind choice among two predeclared B reversals after commitment; compare expected and worst-case selectors with the same verifier.
- **Old-task retention check:** A/C under both reversals, including the rare one.

#### 18. Probabilistic entry funnels (P)
- **Mechanism:** Under stochastic batches, certify that the probability of not entering `C` by `τ` is below `β`, with a deterministic proof for any declared rare branch; price `β` as residual risk.
- **Novelty vs nearest prior art:** Chance-constrained funnels and probabilistic model checking; parent card 6. The new part is entry probability as the thing today's data improves.
- **Cheapest first test:** Enumerate every sampler draw in a small replay sampler; compare data-shaped and unshaped entry probability at equal examples.
- **Old-task retention check:** Probability of any A/C floor breach before entry, by rare slice.

#### 19. Corridors in full optimizer state (I)
- **Mechanism:** Require Adam moments and clocks to enter the corridor too; momentum can carry branches through `C` and out. Select examples that damp the slot divergence as well.
- **Novelty vs nearest prior art:** Parent card 10 and [momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136). Audit.
- **Cheapest first test:** Same toy with SGD and Adam; report whether the SGD corridor survives momentum.
- **Old-task retention check:** A/C at the overshoot steps.

### Is it a new object? Try to break it

#### 20. Certificate debt as a lifelong objective (P)
- **Mechanism:** Treat cumulative certified bytes (plus verifier work) over a task stream as a first-class CL objective next to accuracy and forgetting, like regret, and ask which data policies minimize it at fixed retention and B progress.
- **Novelty vs nearest prior art:** CL metrics count accuracy, forgetting, forward transfer and memory; the [future-edit-cost node (PR #144)](https://github.com/manojbajaj95/cl/pull/144) prices revision work. Certificate debt is the proof-side analogue. New only if it ranks policies differently from those metrics.
- **Cheapest first test:** On a three-task toy stream, rank 6 data policies by certificate debt and by standard metrics; report rank correlation.
- **Old-task retention check:** Every policy is scored on A/C at every prefix; debt is compared only among policies meeting the floors.

#### 21. Rule out the rigid corridor (I)
- **Mechanism:** Plot certified bytes against B progress and a later plasticity probe for: freezing, learning rate decay, saturating units, lazy width, EWC stiffness, and data-shaped corridors. Only a corridor strictly above that frontier counts.
- **Novelty vs nearest prior art:** The ledger's "true by construction" pattern; this is the mandatory audit.
- **Cheapest first test:** All arms in the paper construction and the two-gate toy at matched B steps.
- **Old-task retention check:** A/C for every arm; the frozen arm sets the trivial retention ceiling and must be reported.

#### 22. Compile it away into meta-learning (I)
- **Mechanism:** Give a TAR-style outer loop the same truthful pool, frozen future law, verifier, and the proof cost as its objective. If it finds the same corridors at equal compute, the object is a choice of objective for existing machinery, not a new operation.
- **Novelty vs nearest prior art:** This is the strongest-stack control, the analogue of the parent's card 22 (compile away the novel interface).
- **Cheapest first test:** Same exhaustive toys; compare admitted jobs, bytes, verifier work and build compute.
- **Old-task retention check:** Same A/C floors at every prefix in both arms; a tie at matched scope means no primitive.

#### 23. Corridors that survive a changed future law (P)
- **Mechanism:** Ask whether a corridor built for one optimizer or learning rate still captures branches under a nearby law, and certify robustness of the entry funnel to a declared law family (e.g. lr in an interval).
- **Novelty vs nearest prior art:** Robust funnels in control; in CL the future law is usually assumed exact. New if the robust corridor is cheaper than per-law corridors.
- **Cheapest first test:** Two learning rates in the paper construction; compare one robust corridor with two separate ones and with no corridor.
- **Old-task retention check:** A/C under both laws, especially the faster one, which can overshoot.

## Ranked deeper questions

1. **Does today's truthful data create a corridor beyond the free one?** Measure the natural merge (card 6) and the rigid frontier (card 21) first, then ask whether shaped `D` (cards 1–3, 5) lowers total certified bytes at matched today-accuracy, B progress and A/C floors at every prefix, beating HAL/MER/bilevel selection plus joint MTT and the same verifier. If the free corridor or rigidity explains every win, stop.
2. **Can a merge be confined to the obligation quotient without erasing B content?** Cards 2–4 and the paper construction. Find a toy where full-state branches stay distinct, quotient branches merge, and separate buffers collapse to one; also find the PR #108-style obstruction (injective quotient dynamics) where no data can do it.
3. **Is an example worth more as proof than as accuracy, and is the example necessary?** Cards 8, 9 and 13: show examples whose bytes-saved rank differs from their accuracy rank beyond seed noise, and beat the same stability regularizer applied with no examples over the tube.
4. **Can a corridor certificate be reused by a later learner that only proves entry?** Cards 14–16: an independent B family, entry-only checking versus full recertification and refitting, matched retention. This is the test that would make the corridor a primitive rather than an objective for existing tools (card 22).
