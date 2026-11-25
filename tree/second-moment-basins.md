# Second-moment absorption and basin-preserving C

**Parent:** [Trained recovery basins](recovery-basins.md) ([PR #246][parent]). **Status:** Ideas only; no pilot or GPU work. [Flood triage, row 359][triage] keeps parent cards **07** (absorb second-moment differences only in directions old readers cannot see) and **14** (basin-preserving C: online C updates may never shrink the certified recovery basin) at score 3. The [idea ledger][ledger] requires an old-task retention check in every first test, the stacked best controls of the parts for any merge, and a kill line that linear algebra does not already settle.

**Verdict:** The two bets have different difficulties. *Card 07 is a structural claim, not a first-order one.* A momentum difference is additive, so absorbing it needs only a reader-null subspace that the step map keeps invariant. A second-moment (`v`) difference is a *multiplicative gain on whatever first moment later passes through that coordinate*. It stays hidden while that coordinate is at rest, it grows in proportion to the live gradient, and it decays on the `1/(1−β₂)` clock (about 693 steps to half for β₂ = 0.999, against about 7 for β₁ = 0.9). The check below shows that `v` absorption needs the reader-null subspace to be spanned by preconditioner axes, so a rotated null subspace that absorbs momentum exactly still leaks `v`, and a common non-scalar `v` already breaks rotated momentum absorption. The candidate primitive is therefore **preconditioner-aligned readout**: C training places what old readers ignore on whole optimizer coordinates (or whole blocks of a block preconditioner), so slot histories can differ there without consequence. *Card 14 is constrained optimization once the basin functional is known.* The check shows the right constraint is the basin functional itself, not a parameter box (too strict) or nothing (the plain path shrinks the basin at *every* finite step even when its endpoint is safe). What is open is computing and certifying that functional cheaply for real hosts and using it as a barrier. Neither bet is shown to beat its strongest controls here.

## Contract

- **Inherited.** The parent's public-interface contract and renewal equivalence (two states are equivalent iff every declared reader gives the same outputs under every lawful continuation up to the horizon), its basin objective and certificate scoring, and its full A/Bᵢ/prior-C panel at named cuts and after a common ordinary suffix ([parent][parent]).
- **Second-moment absorption (card 07).** Two states share weights and first moments but differ in `v` (or in Adafactor/Shampoo factors). The `v` difference is *absorbed* when, for every lawful continuation up to the horizon (including a large-gradient B batch and a later task that touches a resting coordinate), every declared reader's output is identical. It is *contracted* when the gap decays below the margin in time, and *reset* when `v` is overwritten. Only absorption produced by ordinary C training (features C and a later B witness use) counts, and the readers include an undeclared held-out reader from the B-witness family.
- **Basin-preserving C (card 14).** After deployment, every online C step must keep the certified basin (the set of reachable post-default aliases with a certified public route to ready by the deadline) a superset of the deployment basin, checked exactly at every step, not only at the endpoint. The barrier is the parent's learned rank function or an exact basin functional. Steps that cannot keep the basin are refused, deferred or rerouted, and the C progress lost is charged.
- **What it must beat.** For 07: #236#13 momentum-only absorption, a `v` reset, #216#10/#232 shrinking, waiting for `β₂` decay, plain momentum as the negative, DDC-style gauge-equivariant preconditioning ([2606.29176][ddc]), SOAP/Shampoo eigenbasis rotation, and a `v` difference on a reader-visible coordinate. For 14: #236#10 offline-only basin training, unconstrained online C at matched C progress, CBF filters on fixed safe sets, constrained adaptive update laws ([2504.19412][cpul]), backup-CBF online set expansion ([2610.05381][bcbf]), EWC on basin parameters, and a useful C update that must shrink the basin.

## Paper checks (exact, CPU)

Script: [`probes/second_moment_basins_check.py`](probes/second_moment_basins_check.py) (fractions only, under a second). Dynamics: heavy-ball with a frozen diagonal preconditioner `P = diag(1/√v)` (the β₂ → 1 regime over a short horizon), `m' = ½m + Hθ`, `θ' = θ − ½·P m'`. Leak = reader · (θ difference between the two histories).

**S1. `v` absorption needs preconditioner-aligned null directions.** Rotated host `H = [[1, ½], [½, 1]]` (eigenvectors (1,1), (1,−1)), reader (1,−1); aligned host `H = I`, service reader (1,0).

| Case | Leak k = 1..4 |
|---|---|
| rotated host, momentum difference on null (1,1), `P = I` | 0, 0, 0, 0 (exactly, forever) |
| same momentum difference, common `P = diag(1, ½)` | −1/8, −3/32, 1/256, 39/512 |
| rotated host, `v` difference on coordinate 2 only (`P₂` = 1 vs ½), `θ₀ = (½, ½)` | 3/16, 21/64, 165/512, 213/1024 |
| aligned host, `v` difference on coordinate 2, service reader (1,0) | 0, 0, 0, 0 (exactly, forever) |
| aligned host, same, later-B reader (0,1) | −1/8, −7/32, −27/128, −63/512 |
| aligned host, `v` difference on coordinate 1 (negative control) | −1/8, −7/32, −27/128, −63/512 |

Two further facts from the same script: multiplying the live gradient by 4 multiplies the `v`-difference leak by exactly 4 at every step, while a momentum-difference leak is unchanged (additive). And a `v` difference on a resting coordinate (θ₂ = m₂ = 0) is invisible to *every* reader until a later task moves θ₂ = 1/4, after which reader (0,1) sees −1/16, −7/64, −27/256: a sleeper gap that wakes at first touch, on a clock about 100× slower than momentum. So the absorbing structure for `v` is a set of whole axes, the leak is gradient-proportional (a big B batch is the right stress test), and "nobody reads it yet" is not absorption. These are rational toy facts. They do not show that C training can produce axis-aligned readout in a real network, or that it is worth its cost.

**S2. The basin functional is the right barrier; a box is too strict and the plain path shrinks the basin all the way.** Parent host with a second learnable parameter `a` (hidden-slot decay): `x ← [[½, h], [0, a]] x`. After two steps `s₂ = h·r·(½ + a)`, so the certified alias radius is `R = 1/(16·h(½ + a))`, and deployment needs `R ≥ ½`. Online C loss `½‖(h, a) − target‖²`, from `(h, a) = (1/8, ½)`, learning rate ½, 12 steps.

| Target | Rule | Final C loss | Smallest radius on the path |
|---|---|---|---|
| (1/4, 0) | none | ≈ 0 | **4/9 (shrinks)** |
| (1/4, 0) | box `h ≤ 1/8` | 1/128 | 1/2 |
| (1/4, 0) | basin `h(½ + a) ≤ 1/8` | ≈ 0 | 1/2 |
| (1/4, ½) | none | ≈ 0 | **≈ 1/4 (shrinks)** |
| (1/4, ½) | box or basin | 1/128 | 1/2 (refuses the update) |

On the first target the unconstrained path has radius 4/9, 16/35, 64/135, … : `h(½ + a) = 1/8 + c(1 − c)/16` with `c = 2⁻ᵗ`, so a default arriving at *any* finite step fails, even though the limit is safe. The basin barrier gets the full C gain because it lets `h` rise only as fast as `a` falls. On the second target the useful update must shrink the basin, and the barrier pays 1/128, the honest price. This is ordinary constrained optimization. Here the functional is closed-form, and the open part is a learned or verified barrier for nonlinear hosts with alias sets that are not boxes.

## Idea cards

### 01. Absorb second-moment differences only where readers cannot see (inherited, #246 card 07)
**Mechanism.** Certify that every reachable `v` gap rescales only directions in the reader-null subspace over the horizon, for all declared readers and an undeclared one. **Novelty vs nearest prior art.** [Delayed optimizer-state transport][dost] and [AdamW I/O dynamics][aio] measure `v`'s delayed effect; [DDC][ddc] makes Adam equivariant to *architectural* gauges. None asks which history differences in `v` old readers can ignore. **Cheapest first test.** S1 scaled to a 4-unit two-layer linear host trained on C, two histories with different B-batch norms (so `v` differs), exact leak for 20 steps including one ×10 B batch. **Old-task retention check.** A/Bᵢ/prior-C panel after the ×10 batch on both histories.

### 02. Basin-preserving C (inherited, #246 card 14)
**Mechanism.** Constrain each online C step so the certified basin contains the deployment basin, using the rank function as a barrier, with refusals charged. **Novelty vs nearest prior art.** CBF filters keep a *fixed* state safe set invariant; [constrained adaptive update laws][cpul] keep parameters in a box; [backup CBFs with memory][bcbf] grow the certified set by storing balls for a fixed plant. Here the learner's own update is filtered by its future recoverability. **Cheapest first test.** S2 with a 3-parameter host and four aliases from the parent's D₀/D₁/D₂ fixture, exact basin recomputed each step; compare none/box/EWC/basin. **Old-task retention check.** Panel at every step of the online C stream, and the worst alias's route endpoint.

### 03. Preconditioner-aligned readout — primitive candidate
**Mechanism.** Add a training term that makes every old reader's null space a union of optimizer axes (per-parameter for Adam, per-block for Shampoo/SOAP eigenbases), so any `v` difference on those axes is absorbed by construction. **Novelty vs nearest prior art.** [Adam sees the basis][basis] and [the optimizer writes the residual basis][resbasis] show Adam picks privileged bases as a side effect; this *targets* the basis to make history differences harmless. **Cheapest first test.** S1 rotated host with a learnable rotation `Q` and a penalty on reader mass off-axis; check that the `v` leak goes to zero with C loss unchanged. **Old-task retention check.** Panel after rotation; the rotation must not move A/C outputs.

### 04. Sleeper second moments — primitive candidate
**Mechanism.** Treat a `v` gap on a resting coordinate as a dormant history channel, and certify absorption against the *first later task that touches it*, not against current readers. **Novelty vs nearest prior art.** Dormant-neuron and plasticity work (ReDo) tracks dead units, not stale optimizer statistics that wake with them. **Cheapest first test.** S1 sleeper: enumerate later tasks that move θ₂, count those whose readers see the wake-up leak. **Old-task retention check.** Panel at the wake-up step for each later task.

### 05. Gradient-proportional stress tests — improvement
**Mechanism.** Since a `v` leak scales with the live gradient (S1: exactly ×4), certify absorption at the largest admissible gradient norm, not at typical ones. **Novelty vs nearest prior art.** Worst-case input bounds; the multiplicative structure tells which bound matters. **Cheapest first test.** Sweep B-batch norm 1–100× on the 4-unit host. **Old-task retention check.** Panel at the largest norm.

### 06. Absorb `v` while it decays, not after — primitive candidate
**Mechanism.** Combine absorption with the `β₂` clock: route C so a `v` gap is reader-null only until it has decayed below the margin, freeing the axis afterwards for readable use. **Novelty vs nearest prior art.** Time-varying observability; distinct from permanent axis allocation (card 03). **Cheapest first test.** Exact schedule with β₂ = 3/4 rationals, then β₂ = 0.999 in floats with error bounds; count axis-steps reclaimed. **Old-task retention check.** Panel when the axis becomes readable again.

### 07. Absorb momentum and `v` jointly — primitive candidate
**Mechanism.** Require one subspace that is both `H`-invariant (momentum) and `P`-invariant for every reachable `P` (second moment); S1 shows these conflict in rotated hosts. **Novelty vs nearest prior art.** Joins #236#13 and #246#07; must beat their stack plus a `v` reset. **Cheapest first test.** Search over 2×2 hosts for one where both leak zero, against the stack. **Old-task retention check.** Panel on both slot differences at once.

### 08. Common-`v` breakage as a retention hazard — improvement
**Mechanism.** S1 shows a *common* non-scalar `P` breaks rotated momentum absorption; audit every momentum-absorption claim (#236#13, #229) under the actual Adam preconditioner. **Novelty vs nearest prior art.** Audit; known non-equivariance ([2606.29176][ddc]) applied to slot certificates. **Cheapest first test.** Rerun #246 F2 with `P = diag(1, ½)`. **Old-task retention check.** Panel under Adam vs heavy-ball.

### 09. Factored second moments as the absorbing structure — primitive candidate
**Mechanism.** Adafactor's row/column factors give `v` gaps a rank-one form; train readers so the gap lies in the null of their row factors, which is cheaper than per-coordinate alignment. **Novelty vs nearest prior art.** Adafactor/BOM compress state for memory; this uses the factorization as an absorption basis. **Cheapest first test.** 3×3 weight matrix, Adafactor update, two histories, exact leak. **Old-task retention check.** Panel per row reader.

### 10. Cross-learner merge with differing `v` — primitive candidate
**Mechanism.** When merging learners whose `v` differ, keep either `v` only on axes certified reader-null and average elsewhere, making merge-then-continue match either continuation. **Novelty vs nearest prior art.** Merging ignores or averages optimizer state ([2608.20442][ost] transfers it); this certifies continuation equivalence. **Cheapest first test.** S1 with two parents and an averaged `v`; leak under each rule. **Old-task retention check.** Both parents' tasks after merge and a suffix.

### 11. `v`-equivalence-preserving state compression — primitive candidate
**Mechanism.** Once a `v` axis is certified absorbed, store one shared scalar for it (or drop it), cutting optimizer memory with no future service change. **Novelty vs nearest prior art.** Factored optimizers compress by design; this compresses only learned-irrelevant state. **Cheapest first test.** S1 aligned host: replace `v₂` by any value, check service trajectory unchanged. **Old-task retention check.** Panel with and without compression after a suffix.

### 12. Barrier from the rank function — primitive candidate
**Mechanism.** Use the parent's learned recovery-rank `V` as a discrete barrier: accept a C step only if `V` still decreases by ≥ 1 along a public word from every deployment alias. **Novelty vs nearest prior art.** Learner–verifier CLF synthesis ([2611.21009][clf]) certifies a fixed controller; here the certificate gates the learner. **Cheapest first test.** S2 with `V` fitted once at deployment, then checked per step; count false refusals vs the exact functional. **Old-task retention check.** Panel at each refusal.

### 13. Curved-path C (lift before you load) — primitive candidate
**Mechanism.** When a C target is basin-safe but the gradient path is not (S2), schedule coordinates so basin-enlarging moves (`a ↓`) lead basin-shrinking ones (`h ↑`). **Novelty vs nearest prior art.** Make-before-break / safe path planning (#157, #152) on the basin functional instead of an old-decision set. **Cheapest first test.** S2: compare projected GD, an ordered step and a learned preconditioner at equal steps. **Old-task retention check.** Panel along each path.

### 14. Basin credit: pay for a shrink with an earlier enlargement — primitive candidate
**Mechanism.** Allow a C update to shrink the basin only by spending margin a previous C update earned, with a ledger that the certificate checks. **Novelty vs nearest prior art.** Energy tanks and slack budgets (#242, #151); new only if the ledger is not linear in the basin radius. **Cheapest first test.** S2 second target, preceded by an `a ↓` update that earns slack. **Old-task retention check.** Panel at the spend.

### 15. Basin-preserving C under Adam — primitive candidate
**Mechanism.** Joins 01 and 02: `v` gaps are themselves aliases, so `v` absorption enlarges the basin, and the barrier must hold on the joint (weights, `m`, `v`) state. **Novelty vs nearest prior art.** Must beat the stack of the two parts. **Cheapest first test.** S2 host trained with frozen-`v` Adam; aliases differing in `v` only. **Old-task retention check.** Panel on the worst `v` alias.

### 16. Deferred C instead of refused C — improvement
**Mechanism.** Queue basin-shrinking C updates until a later C update makes room, and charge only the delay. **Novelty vs nearest prior art.** Buffering; controls are replay and waiting. **Cheapest first test.** Stream of four C targets on S2, count deferred vs refused. **Old-task retention check.** Panel at each release.

### 17. Online basin growth from served defaults — primitive candidate
**Mechanism.** After each recovered default, add its realized route to the certified basin (as [backup CBFs with memory][bcbf] add balls), so online C can only add verified aliases. **Novelty vs nearest prior art.** That work stores balls for a fixed plant; here the stored route is for the changing learner, and must be rechecked after each C step. **Cheapest first test.** S2 with three defaults over the stream; count stored routes that stay valid. **Old-task retention check.** Panel on stored routes after C.

### 18. Undeclared-reader attack on `v` absorption — improvement
**Mechanism.** Sample readers from the later-B witness family and report the fraction that see the `v` leak. **Novelty vs nearest prior art.** Held-out probing. **Cheapest first test.** S1 aligned host, random readers. **Old-task retention check.** A/C probes as declared readers.

### 19. C price of axis alignment — improvement
**Mechanism.** Report C loss of the aligned host vs the best rotated host at equal steps (parent F2 found a 3× C slowdown for momentum absorption). **Novelty vs nearest prior art.** Scorecard. **Cheapest first test.** Sweep the rotation in card 03's test. **Old-task retention check.** Panel at each point.

### 20. Basin collapse under width and online length — improvement
**Mechanism.** Measure the first online C step and the first width at which the barrier must refuse a useful update. **Novelty vs nearest prior art.** Laziness/width confound from the ledger. **Cheapest first test.** Widths 2, 4, 8; 100-step C stream. **Old-task retention check.** Panel at each failure point.

### 21. Falsifier: a C stream that needs a rotated readout — improvement
**Mechanism.** Build a C task whose best readout is rotated against the optimizer axes; the claim must report the `v` leak or the C cost, not retrain. **Novelty vs nearest prior art.** Negative control. **Cheapest first test.** S1 rotated host as the C task. **Old-task retention check.** Panel on the failing stream.

### 22. Falsifier: an update that must shrink the basin — improvement
**Mechanism.** S2's second target as a standing test: the barrier must refuse it and report the C price, and no rule may claim a free gain there. **Novelty vs nearest prior art.** Negative control. **Cheapest first test.** Already in the script. **Old-task retention check.** Panel after the refusal.

## Ranked deeper questions

1. **Can ordinary C training produce preconditioner-aligned readout that absorbs `v` differences for every declared and held-out reader, at a C cost below a `v` reset plus waiting?** Cards 01/03/05/18/19/21. Kill if a `v` reset at the history split ties service and retention at equal steps, if DDC-style or SOAP-basis preconditioning gives the same zero leak with no C-side change, or if any B-witness reader sees the leak under a large-gradient batch.
2. **Is a `v` gap on a resting coordinate a real retention hazard in practice?** Cards 04/06. Measure how often a later task wakes stale `v` in a small transformer stream and whether it moves A/C outputs beyond margin; kill if the effect stays under noise at 10 seeds.
3. **Does a basin barrier on online C keep held-out defaults recoverable at matched C progress, where fixed safe-set CBFs, parameter boxes and EWC either refuse more or shrink the basin?** Cards 02/12/13/17/22. Kill if EWC on basin parameters or a box plus ordered steps matches admissions and retention.
4. **Is the joint Adam-state barrier more than the stack?** Cards 07/15. Require a `v` alias that is certified only by the joint rule.

[parent]: https://github.com/manojbajaj95/cl/pull/246
[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L359
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[ddc]: https://www.alphaxiv.org/abs/2606.29176
[basis]: https://www.alphaxiv.org/abs/2608.05136
[resbasis]: https://www.alphaxiv.org/abs/2611.optimizer-residual-neuron-basis
[dost]: https://www.alphaxiv.org/abs/2608.24593
[aio]: https://www.alphaxiv.org/abs/2608.19762
[ost]: https://www.alphaxiv.org/abs/2608.20442
[cpul]: https://www.alphaxiv.org/abs/2504.19412
[bcbf]: https://www.alphaxiv.org/abs/2610.05381
[clf]: https://www.alphaxiv.org/abs/2611.21009
