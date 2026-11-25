# Fold-earned merge headroom: refunds that a refactor has to prove

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Cross-pool merges, round 46](https://github.com/manojbajaj95/cl/blob/devin/1795537860-merged-ideas/ideas/flood/cross-pool-46.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36)), MNS2 and MNS3. **Review seed:** [Flood triage row 290](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L290) ([PR #6](https://github.com/manojbajaj95/cl/pull/6)) keeps both at score 3: MNS2 folds installed gates into live carriers and reissues only the measured fall in the certified joint merge bound, then asks whether the fold also yields a common reply that lets partner diagnostics be deleted; MNS3 publishes one region in merge-coefficient and price space where a neutral release path and a no-query fallback are both certified. **Grandparents:** [merge-aware budgets](https://github.com/manojbajaj95/cl/pull/181) (#181, cards 9 and 14), [stopping proofs](https://github.com/manojbajaj95/cl/pull/182) (#182, cards 03, 08, 09, 11), [neutral groups](https://github.com/manojbajaj95/cl/pull/183) (#183, cards 13–15) and [cancelling pairs](https://github.com/manojbajaj95/cl/pull/175) (#175, card 13). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Three of its rows bound this node. Coded merge interference was killed because a fitted pairwise surrogate is BOCS and gradient-free merge search ties it, so no card may sell a fitted interaction model as the certificate. The [retention-matched reserve rerun](https://github.com/manojbajaj95/cl/pull/21) left only 0.09 absolute MSE points of next-task spread, so a headroom claim must show a real spread in useful later admissions before ranking anything. The [replay-deadline kill](https://github.com/manojbajaj95/cl/pull/113) found smooth decay with no cliff, so every refund schedule needs a smooth-cost control. The merge-card rule applies throughout: beat the stacked baselines of every part at equal compute, information and proof bytes.

## Is a fold-backed refund of joint merge liability a new object for continual learning?

**Not as compaction, recycling, or coefficient tuning.** [Neuron Merging](https://arxiv.org/abs/2010.13160), [Net-Trim](https://arxiv.org/abs/1611.05162), [ZipIt!](https://arxiv.org/abs/2305.03053) and [PackNet](https://arxiv.org/abs/1711.05769) already fold or free units while keeping outputs. [Continual backprop](https://arxiv.org/abs/2108.06325) and [elastic networks](https://arxiv.org/abs/2608.01475) already recycle capacity. [TIES](https://arxiv.org/abs/2306.01708), [AdaMerging](https://arxiv.org/abs/2310.02575), [αTransfer](https://arxiv.org/abs/2610.07819) and [proximity-regularized merging](https://arxiv.org/abs/2609.32332) already choose or flatten merge coefficients. The closest 2026 work is [LR-Merge](https://arxiv.org/abs/2611.25000): it reads a receiver-local Jacobian–vector product to build a surrogate that is *affine in the merge coefficients*, so one build answers later coefficient queries in seconds. That surrogate is a forecast, not a bound; a coefficient that opens a closed ReLU gate is exactly where it reads zero slope. [TwistedMerge](https://arxiv.org/abs/2607.20887) certifies higher-order alignment obstructions and abstains to a fallback; it certifies alignment consistency, not old-task floors over a coefficient region. [HR-Merge](https://arxiv.org/abs/2611.27377) uses "headroom" for the validation accuracy a merge loses and adds a fail-closed strength that includes zero; that is a different headroom (accuracy to recover, not liability allowance to reissue) and its fallback is validated, not certified. [Certified CL](https://arxiv.org/abs/2407.06697), [IBP](https://arxiv.org/abs/1810.12715) and differential verification ([ReluDiff](https://arxiv.org/abs/2001.03662)) supply the proof tools; [parametric LP sensitivity](https://doi.org/10.1007/978-1-4757-4106-3) supplies the region idea.

**Conditional primitive:** a *refund that is indexed by partner and proved by a refactor*. A fold is function-preserving for the branch that performs it, yet merging acts on weights, so the same fold can lower, keep, or raise the joint interaction term with different partners (Witness 1). The candidate object is a receipt `(fold F, partner class Π, reference, scope, U → U′)` that credits exactly `U − U′` of joint allowance against `Π`, plus, for MNS3, a published region `R ⊂ (coefficients × prices)` inside which a merger may choose late, release back along a certified path, or stop asking. If certified merging (exact joint recertification after every fold) plus merge-and-prune plus parametric sensitivity and a byte-matched cache gives the same useful merged admissions at the same evidence cost, the object is an implementation convenience, not a primitive.

### Contract

- **Reference and bound.** Use #181's schematic two-branch sum bound `d_merge ≤ b₀ + qᵢ + qⱼ + Jᵢⱼ`, valid by adding and subtracting the solo readout changes for a weight-space sum; any other merge operator needs its own argument. `J` is the sup over the declared merge domain `D` (old protected domains, both new-task probes, the declared suffix) of the mixed term `f(θ₀+Δᵢ+Δⱼ) − f(θ₀+Δᵢ) − f(θ₀+Δⱼ) + f(θ₀)`.
- **What a fold may earn.** A fold rewrites `Δᵢ` to `Δᵢ′` with `f(θ₀+Δᵢ′) = f(θ₀+Δᵢ)` on the full protected domain of branch `i` (checked on the common refinement of activation cells, as in #183's contract). It earns `J(Δᵢ,Π) − J(Δᵢ′,Π)` against partner class `Π`, recomputed by a sound bound; nothing more. Solo output preservation earns nothing by itself. A slot freed by the fold is a separate gain, and partner-diagnostic deletion is a third gain needing #182's regret proof. Never sum them from one certificate.
- **No manufactured credit.** Do not move the reference, reset an accountant, drop partners from `Π`, narrow `D`, restore a checkpoint, or undo a violated prefix. Credit is issued only after the fold is installed and checked at every visible intermediate.
- **Region semantics (MNS3).** A region is a finite union of cells in coefficient space (and price space for queries). Inside a cell, every point is certified for old tasks and the suffix under every partner hypothesis the cell names. Gate flips and arithmetic rounding are cell boundaries; interpolation across them is forbidden. A *neutral release path* is a certified path from any point in the region to the fallback (for example dropping a partner's coefficient to zero). A *no-query fallback* is a point certified under all live partner hypotheses. Explicit holes mark where asking is necessary.
- **Costs.** Charge width, staging, receiver ranges, optimizer and replay bytes, proof bytes, verification calls, queries and failed attempts. A refund that is never spent on a later useful merged admission counts as zero.

### Two exact paper witnesses

Both were checked numerically on a dense grid; the numbers are exact for these piecewise-linear toys.

**Witness 1 — one fold, opposite refunds.** One input `x`, merge domain `D = [−1, 4]`, old task A on `P = [−1, 1]`. Base: live receiver `r = [x−2]₊` with readout 1; dormant slot `g` with the same input weights `(1, −2)` and readout 0. Branch `i` installs its new skill by setting `g`'s readout to 1 (pre-fold form). The fold moves that duty into the receiver: `r` readout 1 → 2, `g` readout back to 0, freeing `g`. Branch `i`'s function is identical in both forms everywhere, and neither form touches A. Two possible partners, each harmless alone on A:
- `j₁` drifts the dormant slot `g`'s bias by +2.5 (free in its own branch, because `g`'s readout is 0 there). Pre-fold: `J = 2.5` on `D` and `1.5` on A's domain `P` (the merged model breaks A at `x = 1` though both solos preserve A exactly). Post-fold: `J = 0`. **Refund 2.5.**
- `j₂` raises the receiver's bias by +1 (`r = [x−1]₊`, still silent on `P`). Pre-fold: `J = 0`. Post-fold: `J = 1` on `x ≥ 2` (overshoot on both new-task probes). **Negative refund: the fold costs 1.**

So the refund is partner-indexed, and crediting it from solo output preservation is unsound in both directions. A third partner touching neither unit gives refund 0. This is the minimal case for MNS2's first test (fold lowers, preserves, worsens).

**Witness 2 — a coefficient region with a priced hole.** One old example with preactivation `−0.8`, readout 1, cap 0.25 on its output. Merge `θ₀ + αΔᵢ + βΔⱼ`; `Δᵢ` adds 0.6 to that preactivation; `Δⱼ` adds either 0.6 (hypothesis H₁, prior `p`) or 0.9 (H₂), and the two are indistinguishable without a probe. New-task utility is `min(α,1) + min(β,1)`. Under H₁ the gate stays closed (exact zero interaction, the signed premise holds) for `α+β ≤ 4/3`, opens between `4/3` and `1.75` while staying within cap, and fails above `1.75`. With biases stored in fixed point (step 0.05, round half to even) the flip moves to `α+β ≈ 1.375`, so float and deployed cells differ. The no-query fallback must satisfy both `α+β ≤ 1.75` and `0.6α + 0.9β ≤ 1.05`; its best point is `(1, 0.5)` with utility 1.5. A probe revealing H₁ allows `(1, 0.75)` with utility 1.75; revealing H₂ keeps 1.5. The probe is worth `0.25p`, so the published region says: at query price `c ≥ 0.25p`, never ask; take `(1, 0.5)`. The release path from `(1, 0.75)` to `(1, 0)` lowers the preactivation monotonically, so it is certified under both hypotheses. Adding a second unit that reads `−Δⱼ` makes release non-monotone in `β`: the path crosses an open gate, which becomes an explicit hole. An LR-Merge-style affine surrogate read at the receiver sees zero slope (gate closed) and certifies nothing across `4/3`.

### Common first-test rules

Freeze partner classes, operator, domains, reference, margins and rounding before each comparison. Give every arm the same legal moves, information, compute and proof bytes. Stacked control for MNS2: #181#14 interaction repair alone + #183#13/#175#13 fold alone + merge-and-prune + post-merge correction + exact joint recertification after each fold, with speculative refill as a negative control. Stacked control for MNS3: fixed coefficients + the proximity-regularized plateau + exact per-setting recheck + parametric sensitivity with a byte-matched cache + LR-Merge's affine surrogate + #182#03 price regions alone. Exhaustive planning with the same state and move set is an upper bound, not a baseline. Count only useful merged admissions at fixed old-task floors; refusing everything, narrowing `D`, or deferring the same learning does not count. **Retention:** score old A/C on held-out examples at every fold intermediate, at merge, at the late-chosen coefficient, along the release path and after one legal suffix update; keep both new-task skills; report worst slices at matched starting margins. **P** = candidate primitive if it beats the stacked control; **I** = improvement or audit.

## Idea cards

### Earn the refund (MNS2 core)

#### 01. Partner-indexed fold receipts (P)
- **Mechanism:** After a fold, issue one receipt per declared partner class: certified `Jᵢ,Π` before and after, credit `max(0, U − U′)`, and a debit when the fold raises `J` (Witness 1, `j₂`). A fold with any negative receipt against a committed partner is refused or must be paired with a compensating move.
- **Novelty vs nearest prior art:** Neuron Merging and ZipIt fold for compression and score the endpoint; #181#14 repairs interaction by moving a representation. No prior method charges a function-preserving refactor for the joint liability it changes per partner.
- **Cheapest first test:** Enumerate Witness 1 with three partners (lower/keep/raise) and a fourth sampled from small random edits; compare receipt accounting with exact joint recertification and with crediting from solo preservation. Count unsafe admissions and refused safe ones.
- **Old-task retention check:** A on `P` at the fold, at each merge, and after a suffix update in each partner world; both new-task probes at merge.

#### 02. Fold toward the partner, not toward the smallest network (P)
- **Mechanism:** Among all function-preserving folds available to branch `i`, pick the one that minimizes the certified sum of `J` over committed partners, not unit count. Free slots become a by-product.
- **Novelty vs nearest prior art:** Compaction objectives minimize width or error; partner-aware merging (CoFiMA, FedSEAM) shapes task vectors, not refactors under exact solo equivalence.
- **Cheapest first test:** Give branch `i` two receivers, one shared with partner `j`'s writes and one not; compare width-minimal folding, partner-minimal folding and #181#14 rotation at equal search.
- **Old-task retention check:** Exact equality of branch `i` on its full domain during folding; A/C at merge and after the suffix.

#### 03. Three gains, three proofs from one refactor (P)
- **Mechanism:** One fold may (a) free a slot, (b) lower `J`, (c) create a common reply under which a partner-specific diagnostic table can be deleted. Issue three separately checkable receipts; spending any one never presumes another.
- **Novelty vs nearest prior art:** MNS2 states the claim; prior work bundles compaction and verification. The test is whether separating receipts avoids double-counting that a single endpoint check would miss.
- **Cheapest first test:** Plant cases where each subset of the three gains holds (8 cells) in a four-unit host; compare one bundled certificate, three receipts and exact replanning; count false refunds.
- **Old-task retention check:** A/C at each spend of each receipt; the deleted diagnostic must not be the only thing protecting a slice (check by erasure).

#### 04. Dormant-drift audit before folding (I)
- **Mechanism:** Witness 1's `j₁` shows partners drift coordinates that are free in their own branch. Before crediting a fold, bound the drift each partner class may apply to dormant coordinates the fold reactivates or deactivates.
- **Novelty vs nearest prior art:** Unregistered dependence (earlier tree nodes) and GPM's protected subspaces cover the idea; this is an audit of fold receipts.
- **Cheapest first test:** Sweep partner drift magnitude on the freed slot; report the smallest drift at which a fold receipt flips sign.
- **Old-task retention check:** A on `P` at merge across the drift sweep.

#### 05. Joint absorption creates refunds no single fold can (P)
- **Mechanism:** Two spent gates that cannot be folded alone may be absorbable jointly (#183#14). Credit the joint fold's drop in `J`, and check whether that drop exceeds the sum of what each partial fold would earn.
- **Novelty vs nearest prior art:** #183#14 frees slots by joint feasibility; this asks whether joint absorption is also super-additive in liability refund.
- **Cheapest first test:** #183#14's `[x+2]₊ + [1−x]₊` pair with constant receivers, plus a partner writing one of the gate slots; compare joint, greedy and exact.
- **Old-task retention check:** Full pre-fold function on `[−1,1]`; A/C after merge and after a third useful write.

#### 06. Refunds that expire with the partner class (I)
- **Mechanism:** A receipt holds only for the partner class it was computed against; when a new partner enters, re-derive it from the fold's stored before/after state, not from the old number.
- **Novelty vs nearest prior art:** Contract refinement (Pacti) covers scoped validity; an improvement on #181#2.
- **Cheapest first test:** Admit a held-out partner after a credited fold; compare stale credit, re-derived credit and full recheck.
- **Old-task retention check:** A/C at the late merge with the new partner.

#### 07. Fold during training, not after it (P)
- **Mechanism:** Interleave folds into branch `i`'s ongoing learning so the optimizer's next steps happen in the folded parameterization, then price whether later updates keep the lowered `J` or erode it.
- **Novelty vs nearest prior art:** Net2Net and continual backprop change parameterization mid-training for capacity; nobody tracks joint merge liability across later updates.
- **Cheapest first test:** Fold at step `t` versus at the end in a two-branch toy MLP; compare `J` at merge, total B progress and suffix stability.
- **Old-task retention check:** A/C before, during and after each fold and at merge; check that momentum carried through the fold does not reopen a closed gate.

#### 08. Price the receiver range a fold consumes (I)
- **Mechanism:** A fold uses part of a receiver's writable range (#183#15). Charge that range against later folds and against any partner that writes the same receiver.
- **Novelty vs nearest prior art:** Resource reservation; an improvement on #183#15.
- **Cheapest first test:** Two folds competing for one receiver with a partner writing it; compare static reserve, priced reserve and exact planning.
- **Old-task retention check:** A/C during both folds and at merge.

#### 09. Fold receipts that survive an optimizer change (P)
- **Mechanism:** A receipt states which optimizer slots of the folded units it assumes. On an optimizer handoff, either re-establish the receipt or fall back to the pre-fold debit.
- **Novelty vs nearest prior art:** #178 optimizer-slot splits and #181#5 cover handoffs; the candidate binds a liability refund to slot state.
- **Cheapest first test:** Two successors with equal weights but different momentum on the receiver; one extra step after the fold; compare stale receipt and recheck.
- **Old-task retention check:** A/C on the first momentum-sensitive step and at merge.

#### 10. Speculative refill as the null every refund must beat (I)
- **Mechanism:** Issue credit equal to the fold's freed width (or its solo-loss drop) without a joint proof, and count how often it is unsafe.
- **Novelty vs nearest prior art:** A negative control, as in #181.
- **Cheapest first test:** Run alongside cards 01–05 on the same enumerated worlds.
- **Old-task retention check:** Report every unsafe merged prefix on A/C.

### Publish a region (MNS3 core)

#### 11. Cells, not intervals, of merge coefficients (P)
- **Mechanism:** Partition coefficient space by activation-pattern changes and rounding boundaries; certify old tasks cell by cell with exact or IBP bounds; publish the certified union with its holes.
- **Novelty vs nearest prior art:** #181#9 proposes an interval; LR-Merge answers coefficient queries with an affine surrogate (estimate); parametric LP sensitivity gives regions for LPs. A sound cell complex for merged ReLU networks that later learners can query is the candidate.
- **Cheapest first test:** Witness 2 plus a two-unit variant; compare fixed coefficients, the proximity plateau, LR-Merge's surrogate, exact per-setting recheck and the cell region on unsafe picks and utility.
- **Old-task retention check:** A/C at every vertex and at a late-chosen interior point in each cell, in float and in fixed point.

#### 12. Price the question in the same region (P)
- **Mechanism:** Extend the region with a query-price axis: inside the no-ask part the fallback is certified under every hypothesis and the probe's value of information is below its price (Witness 2: `c ≥ 0.25p`).
- **Novelty vs nearest prior art:** #182#03 regions over prices and EVSI are known separately; the candidate is one certificate that a merger checks once for both "which coefficients" and "whether to ask".
- **Cheapest first test:** Enumerate Witness 2 over `p` and `c`; compare separate interval + EVSI, exact joint planning and the joint region at equal bytes.
- **Old-task retention check:** A/C at the fallback, at the post-probe optimum, and after a suffix update under each hypothesis.

#### 13. Certified release paths (P)
- **Mechanism:** For each region point, store a path back to a fallback (lowering a partner's coefficient, or a fold that removes its dependence) whose every intermediate is certified; refuse points whose only release crosses a hole.
- **Novelty vs nearest prior art:** Mode connectivity finds low-loss paths empirically; reach-avoid planning certifies paths in control. A merge-cancellation path with old-task certificates is not in the merging literature we found.
- **Cheapest first test:** Witness 2 with and without the `−Δⱼ` reader; compare endpoint-only certification, straight-line release and certified-path selection; count released states that break A.
- **Old-task retention check:** A/C at every point along the release path, and the surviving branch's new skill afterwards.

#### 14. Signed interactions only under checked sign premises (I)
- **Mechanism:** Inside a cell, take cancellation credit from a signed cross term only if every partner in the class satisfies the sign; otherwise use the absolute bound.
- **Novelty vs nearest prior art:** #181#6; an improvement.
- **Cheapest first test:** Rank-one edits with aligned, opposed and unconstrained signs across a gate flip.
- **Old-task retention check:** A/C on a held-out slice where the sign reverses.

#### 15. Rounding is a regime boundary (I)
- **Mechanism:** Compute cells in the deployed arithmetic (fixed point, bf16, int8); a float-certified point that crosses a rounded boundary is not certified.
- **Novelty vs nearest prior art:** Quantization-aware verification exists; an audit of card 11.
- **Cheapest first test:** Witness 2's flip at `4/3` versus `≈1.375`; extend to int8 per-channel scales on a two-unit merge.
- **Old-task retention check:** A/C in deployed arithmetic at each certified vertex.

#### 16. Regions that survive further local learning (P)
- **Mechanism:** After publishing a region, a branch keeps training; each local update is admitted only if the region shrinks by at most a declared amount, so the merger's late choice stays valid.
- **Novelty vs nearest prior art:** #181#9 states survival as a goal; proximity regularization widens a plateau empirically. The candidate is a training-time admission rule on a published coefficient region.
- **Cheapest first test:** Two quantized ReLU branches; ten local updates with and without the admission rule; measure region area, B progress and unsafe late picks.
- **Old-task retention check:** A/C at each update and at the late merge.

### Couple the two (MNS2 × MNS3)

#### 17. A fold that widens the region is the refund (P)
- **Mechanism:** Measure a fold's refund not as a scalar drop in `J` but as the gain in certified region volume (or in utility of the best no-query point). Credit only that measured widening.
- **Novelty vs nearest prior art:** The interaction neither part has alone: a refactor priced by the coefficient choices it opens. Stacked control: fold, then recompute region from scratch.
- **Cheapest first test:** Witness 1 lifted to coefficients `(α, β)`: with `j₁`, the fold should widen the safe region; with `j₂`, shrink it. Compare scalar-`J` credit, region-volume credit and exact recheck.
- **Old-task retention check:** A/C across the widened region in both partner worlds.

#### 18. Fold to remove the reason to ask (P)
- **Mechanism:** Choose the fold so that the two partner hypotheses agree on every region cell that matters (the fold makes the distinguishing unit irrelevant), turning a probe into a no-query fallback and allowing the diagnostic table to be deleted under #182.
- **Novelty vs nearest prior art:** #182#09 teaches a common reply with examples; here a function-preserving refactor creates it. Separate from stopping because it changes the state, not the belief.
- **Cheapest first test:** Witness 2 with a fold that moves `Δᵢ` off the shared unit; compare probe value before and after, against teaching examples and against buying the probe.
- **Old-task retention check:** A/C at the post-fold fallback and after deleting the diagnostic; erasure check that deletion removed nothing still read.

#### 19. Refund only what a later merge spends (P)
- **Mechanism:** Hold fold receipts as options; they become allowance only when a merge request with a named coefficient cell arrives and the receipt covers it.
- **Novelty vs nearest prior art:** #181 earns headroom after repair; the candidate ties earned headroom to a coefficient cell, so the same fold can pay for one late choice and not another.
- **Cheapest first test:** Two later merge requests at different coefficients; compare eager scalar credit and cell-scoped options.
- **Old-task retention check:** A/C at each served request.

### Audits and limits

#### 20. Smooth-cost control (I)
- **Mechanism:** Replace ReLU gates with softplus of tunable sharpness; if refunds and regions degrade to what smooth Fisher-weighted merging predicts, the gate story is the whole effect.
- **Novelty vs nearest prior art:** Required by the replay-deadline kill (no cliff, smooth decay).
- **Cheapest first test:** Sweep sharpness in Witnesses 1 and 2; compare region and receipts with Fisher/LR-Merge forecasts.
- **Old-task retention check:** A/C at each sharpness.

#### 21. Spread gate before any ranking (I)
- **Mechanism:** Before comparing fold policies, check that useful later merged admissions vary across folds by more than seed noise.
- **Novelty vs nearest prior art:** The ledger's predictor-pilot rule (plasticity reserve, gradient-share, edit-capacity law died at this gate).
- **Cheapest first test:** 50 random hosts with three candidate folds each; report admission spread over seed spread.
- **Old-task retention check:** A/C floors held fixed while measuring the spread.

#### 22. Exhaustion: how many paid folds before no refund is left (I)
- **Mechanism:** Under a declared demand stream, repeat fold → refund → admit until no fold earns positive credit; report the shortest exhausting sequence or a nonempty invariant.
- **Novelty vs nearest prior art:** #183#18; an audit of whether refunds are renewable.
- **Cheapest first test:** Enumerate a six-unit host with two partners and five requests.
- **Old-task retention check:** A/C after every admitted request.

#### 23. Independent partner checks the receipt without the source (P)
- **Mechanism:** A partner verifies a fold receipt from the published before/after units and its own class description, never seeing branch `i`'s training data or trajectory.
- **Novelty vs nearest prior art:** #171 entry ports and #181#1; the candidate is a source-free check of a refund, not of a property.
- **Cheapest first test:** Held-out partner with permuted units; compare receipt check, full recheck and trust.
- **Old-task retention check:** A/C at the partner's merge.

## Ranked deeper questions

1. **Is a fold's joint refund ever both positive and cheaper to prove than recertifying the merge?** Witness 1 shows the sign is partner-indexed. Use cards 01–05, 10 and 17: on enumerable hosts with independently authored partners, count useful merged admissions at fixed A/C floors per unit of proof cost, against exact joint recertification after every fold plus merge-and-prune. If recertification ties at equal cost, the receipt is bookkeeping.
2. **Can one published region replace both per-setting rechecks and the question of whether to probe?** Use cards 11–13 and Witness 2: compare the joint coefficient-and-price region with separate intervals plus EVSI and with LR-Merge's affine surrogate, in float and deployed arithmetic. The region counts only if a merger makes fewer unsafe picks and fewer queries at equal utility and proof bytes.
3. **Can a function-preserving refactor create a common reply that makes a partner question moot?** Use card 18 and #182#09: the fold must reduce the probe's value to below its price where teaching examples at equal cost cannot. Check by erasure that the deleted diagnostic protected nothing.
4. **Do refunds survive continued local learning and optimizer handoffs?** Use cards 07, 09 and 16. A refund that local training erodes within a few steps, or that a momentum swap reopens, is not a resource.
5. **Is the effect gate-specific?** Use cards 20 and 21 first. If smooth activations or a flat admission spread erase the advantage, report the negative result and stop.

**Verdict:** MNS2 survives as a narrower claim than written: a fold earns joint headroom only per partner class, and Witness 1 shows the same fold can pay 2.5 or cost 1. MNS3 survives as a cell complex with holes, not an interval; Witness 2 shows rounding moves its boundary and a probe price decides whether to ask. The best primitive candidate is card 17, which prices a refactor by the certified coefficient choices it opens. It must beat fold-then-recertify, the proximity plateau and LR-Merge's surrogate at equal cost, with A/C retention held throughout.
