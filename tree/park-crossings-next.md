# Returnable and repair-coupled park crossings

**Status:** Ideas and exact paper fixtures only; no implementation, learner runs, or GPU work. **Parent:** [Park crossings](park-crossings.md) ([PR #282][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, row 401][triage], #282 cards 04 and 10 (both score 3).

**Verdict:** Both extensions are algebraically feasible on engineered pools, and neither is a novelty win yet. A **return-option crossing** (#282#04) is a candidate primitive only if certifying a not-yet-arrived truthful return pair across all allowed post-crossing states beats an equal-byte compressed weight snapshot (plus replay of B work learned away) on retention, B progress, and latency. A **repair-coupled crossing** (#282#10) is a candidate primitive only if co-batching a truthful crossing B record with an overdue old-job repair record closes the destination park and transfers to unseen old-task examples where separate batches, [GEM][gem], and [GraB][grab] miss a deadline or land off target. Combining them counts only if repair-steered landing or return-by-repair unlocks on-time A/B/C coverage that stacking the two mechanisms separately cannot match at equal budget.

## Contract and deciding controls

- Freeze the native optimizer, step size, truthful record pool and indivisible record grammar, arrival schedule, publication boundaries, and deployed tolerances before choosing any batch. All old-task parks (`A_park`), overdue repair reads (`A_rep`), rare slices (`C`), and new-task targets (`B`) are fixed in advance on independent held-out inputs never used for selection.
- For **return-option crossings** (#282#04), freeze the allowed post-crossing update set `U_away` (including idle ticks and carried optimizer slots) and the declared future return menu `M_ret` (truthful records that have *not yet arrived* at the outbound commit) before issuing the outbound pair. A valid return certificate must cover **every** reachable post-crossing state in `S_post` up to the old job's due time `T_due`, without storing a copy of the starting weights `θ_0`. Crucially, measure whether returning to `P_+` *preserves* the B service learned in `P_-`: a return that merely resets `θ` back to `θ_0` loses to a stored checkpoint or to refusing the crossing.
- For **repair-coupled crossings** (#282#10), freeze an overdue old-job defect `A_rep` whose loss would violate its SLA if postponed, and a due `B` target requiring a cross-component jump at the same commit. Require both records to be unmodified truthful examples whose own losses decrease (or whose held-out generalizations improve) under the native step. Test `A_rep` on **unseen** held-out examples from the drifted old distribution so memorizing a sentinel does not pass as repair.
- **Strongest controls (must be matched on bytes, native steps, preview compute, and A/B/C retention):**
  - *For #282#04:* `#271#05` one-way crossing; a stored weight snapshot (full or equal-byte quantized/LoRA delta) plus replay of the B records learned in `P_-`; `#271` reserved second chords; [return corridors][return]; viability/returnability filters; a negative-control post-crossing state in `P_-` that no pair in `M_ret` can return from.
  - *For #282#10:* `#271#05` crossing alone; the overdue repair alone; both in separate batches at equal compute (both orders); [GEM][gem] (charged as an off-language gradient edit); [GraB][grab] ordering; [silent-DoF live replay][silent-replay]; an off-target repair twin (`r_A_bad`) that fixes `A_rep` equally well alone yet pushes the co-batched crossing off `P_-`.
  - *For A × B merges:* the best equal-budget stack of the two strongest single-seed controls, per the [idea ledger's][ledger] merge rule.
- Log rejections, waits, preview/certification cost, and every published prefix. Per the ledger: match per-item margins before attributing forgetting order, and gate any future pilot on target variance exceeding seed noise.

## Two exact paper fixtures

Each record is a fixed squared loss (sum of half-squares on its named coordinates), updated by native SGD on the mean of the records in the committed batch. These are exact `Fraction` feasibility witnesses separating the required controls, not evidence of prevalence in natural pools.

### R1. Return-option crossing that preserves B work without a weight snapshot

State `(x, y, z) ∈ Q^3`, native SGD with step size `η = 1/2`. Old routine `A` returns `q + x² − y² − 1` on held-out `q` (park `x² − y² = 1`, disconnected components `P_+ = {x ≥ 1}` and `P_- = {x ≤ −1}` for any tolerance `< 1`). Rare `C` requires `9/4 − y² ≥ 0` (`|y| ≤ 3/2`). Start at `s_0 = (1, 0, 0) ∈ P_+`. At tick 1, B requires landing in `P_-` with `(x + 1)² + y² ≤ 3/4`. At tick 2 (while in `P_-`), allowed post-crossing work is either idle, a `z`-only truthful B record targeting `z = 2` (which moves `z: 0 → 1`, learning B), or a `(y, z)` truthful B record targeting `(−9/4, 2)` (which moves `(-5/4, 3/4, 0) → (-5/4, -3/4, 1)`, staying on `P_-` while learning `z = 1`). At tick 3, a `P_+`-only old job is due (`x ≥ 1`, `A = 0`, `C ≥ 0`), and we also check whether learned B (`z = 1`) survived the return.

The outbound menu offers two truthful pairs on `(x, y)`:
- **Greedy one-way pair `O_near`:** targets `(−3, 2)` and `(−3, −2)` → lands at `(−1, 0, 0)` (tick-1 B error `0`).
- **Return-option pair `O_opt`:** targets `(−7/2, 5/2)` and `(−7/2, 1/2)` → lands at `(−5/4, 3/4, 0)` (tick-1 B error `5/8 ≤ 3/4`; both singletons fail `A` with defects `−1` and `+1/2`).

The future return menu `M_ret` (not yet arrived at tick 1, touching only `(x, y)` so `z` is preserved) has two truthful pairs: `R_a` with targets `(13/4, −7/4), (13/4, 1/4)` and `R_b` with targets `(13/4, 7/4), (13/4, −1/4)`. Neither pair's singletons are publishable (`A = −1/4`).

| Path through ticks 1 → 2 → 3 | State at tick 3 | `A` defect | `C` score | Learned B (`z`) kept? |
| --- | --- | ---: | ---: | --- |
| `O_opt` → idle → `R_a` | `(1, 0, 0)` | `0` | `9/4` | n/a (idle) |
| `O_opt` → `z`-update → `R_a` | `(1, 0, 1)` | `0` | `9/4` | **yes** (`z = 1`) |
| `O_opt` → `(y,z)`-update → `R_b` | `(1, 0, 1)` | `0` | `9/4` | **yes** (`z = 1`) |
| `O_near` → idle or `z`-update → `R_a` or `R_b` | `(9/8, ±3/8, 0 or 1)` | `+1/8` | `135/64` | fails `A` (stranded) |
| `O_near` → `z`-update → restore snapshot `s_0` | `(1, 0, 0)` | `0` | `9/4` | **no** (`z` erased to `0`) |

**Negative control (disallowed post-crossing state):** if an intervening update while away moves `(−5/4, 3/4, 0)` to `(−1, 0, 1)`, the learner is still exact on `P_-` (`A = 0`) yet leaves the returnable pre-image: both `R_a` and `R_b` give `A = +1/8`. The return certificate must refuse that intervening move.

### R2. Co-batched crossing with an overdue old-job repair

State `(x, y, u) ∈ Q^3`, native SGD with step size `η = 1` on the mean of the records in the batch. Old routine `A` has two checks: park `A_park: x² − y² − 1 = 0` (`P_+` vs `P_-`) and an overdue old-job generalization error `A_rep = u²` (deadline `≤ 9/4` at tick 1). Rare `C` requires `5 − y² − u²/4 ≥ 0`. New task `B` has held-out error `(x + 1)² + y²` (deadline `≤ 1/4` at tick 1). Start at `s_0 = (5/4, 3/4, 3) ∈ P_+` (`A_park = 0`, `A_rep = 9`, `B = 45/8`, `C = 35/16`).

Two truthful indivisible records are available at tick 1:
- **Overdue A repair `r_A`:** loss `½((x − 1)² + y² + u²)` (true target `(1, 0, 0) ∈ P_+` with `u = 0`).
- **Crossing B record `r_B`:** loss `½((x + 3)² + y²)` (supplies the cross-separator jump).
- **Off-target repair twin `r_A_bad`:** loss `½((x − 5/4)² + (y − 3/4)² + u²)` (equally valid repair of `u = 0` on `P_+` in isolation, but does not cancel `y = 3/4` when co-batched with `r_B`).

| Action at native `η = 1` | Committed state | `A_park` | `A_rep (u²)` | `B` error | `C` score | Verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Start (no work) | `(5/4, 3/4, 3)` | `0` | `9` | `45/8` | `35/16` | misses `A_rep`, `B` |
| **Co-batch `{r_A, r_B}`** | **`(−1, 0, 3/2)`** | **`0`** | **`9/4`** | **`0`** | **`71/16`** | **passes all** (`L_A`: `77/16→25/8`, `L_B`: `149/16→2`) |
| Repair alone (`r_A`) | `(1, 0, 0)` | `0` | `0` | `4` | `5` | misses `B` deadline |
| Crossing alone (`r_B`) | `(−3, 0, 3)` | `+8` | `9` | `4` | `11/4` | fails `A_park`, `A_rep`, `B` |
| Sequential `r_A → r_B` (2 ticks) | `(1,0,0) → (−3,0,0)` | `0 → +8` | `0` | `4 → 4` | `5` | misses tick-1 `B`; tick-2 fails `A_park`, `B` |
| Sequential `r_B → r_A` (2 ticks) | `(−3,0,3) → (1,0,0)` | `+8 → 0` | `9 → 0` | `4 → 4` | `11/4 → 5` | tick-1 publishes `A_park = +8`; tick-2 misses `B` |
| Off-target repair alone (`r_A_bad`) | `(5/4, 3/4, 0)` | `0` | `0` | `45/8` | `71/16` | valid solo repair; misses `B` |
| Co-batch `{r_A_bad, r_B}` | `(−7/8, 3/8, 3/2)` | `−3/8` | `9/4` | `5/32` | `275/64` | fails `A_park` (off-target repair twin) |

This checks joint algebraic closure, not natural prevalence: `r_A` alone is safe and fixes `u` completely, yet only co-batching `{r_A, r_B}` clears both tick-1 deadlines while landing exact on `P_-`. Both sequential orders (`GraB`-style reordering) fail.

## Idea cards

**P** = candidate primitive (a reusable operation or object); **I** = improvement or falsifier, not a pilot candidate by itself. Every card names the simplest same-budget control that could tie it.

### Sell a crossing only with a return option (#282#04)

#### 01. Certify multi-state returnability before issuing an outbound crossing (P)
- **Mechanism:** Admit an outbound crossing pair `O` from `P_+` to `P_-` only with a certificate that every state in the declared post-crossing reachable set `S_post` admits a not-yet-arrived truthful return pair in `M_ret` back to `P_+` by `T_due`, with zero stored copies of `θ_0`.
- **Novelty vs nearest prior art:** [Return corridors][return] shape trajectories toward a shared buffer; recursively feasible MPC and viability theory use continuous controllers or state constraints. Here the actuator is restricted to indivisible, not-yet-arrived truthful batches across a disconnected park separator. Simplest same-budget control: `#271#05` one-way crossing plus an equal-byte compressed snapshot of `θ_0`.
- **Cheapest first test:** Extend R1 to a 12-record finite pool with 3 allowed post-crossing updates and 1 stranded twin; compare on-time `P_+` return rate and total bytes against one-way crossing, `#271` reserved second chords, and equal-byte checkpointing. Kill if snapshot + replay ties on bytes and B retention.
- **Old-task retention check:** Evaluate held-out `A` and rare `C` at outbound commit, every intermediate `P_-` tick, and after return to `P_+`; include a trace where the old `P_+` job arrives early.

#### 02. Require work-preserving return on orthogonal B coordinates (P)
- **Mechanism:** Strengthen the return-option certificate so that the certified return pair in `M_ret` restores `P_+` while keeping the B task accuracy learned during the `P_-` stay above a declared floor, rather than unwinding B back to `θ_0`.
- **Novelty vs nearest prior art:** Weight-snapshot rollback and unlearning-style resets restore `P_+` by erasing intervening B progress; [recovery guarantees in CL][recovery-cl] analyze re-learning old tasks rather than preserving new work across a reverse component jump. Simplest same-budget control: store `θ_0` and replay the logged `P_-` B batches after rollback.
- **Cheapest first test:** In R1 with coupled `(y, z)` B updates, compare work-preserving return against snapshot rollback and against snapshot + post-rollback B replay at equal total steps and bytes. Kill if rollback + replay matches B accuracy at the same deadline.
- **Old-task retention check:** Check held-out `A` and rare `C` on `P_+` immediately after return and after one routine `A` update to verify that retained B did not leave `P_+` brittle.

#### 03. Gate intervening `P_-` updates with a live returnability envelope (P)
- **Mechanism:** While operating in `P_-`, maintain the pre-image `R ⊂ P_-` of `M_ret` back into `P_+` and admit an ordinary `P_-` B update only if its committed endpoint stays inside `R`, rejecting updates that are locally safe on `P_-` yet strand the learner before `T_due`.
- **Novelty vs nearest prior art:** [Update-admission auditing][admission-audit] balances error control against retained learning opportunity; control-barrier filters enforce continuous invariance. Here the barrier is the discrete pre-image of a finite future truthful-batch menu across a disconnected component gap. Simplest same-budget control: freeze the `P_-` coordinates that `A` reads (`OGD`/subspace lock) while away.
- **Cheapest first test:** Run a 4-tick `P_-` stream with benign and stranding B offers (as in R1's negative control); compare admitted B progress and return success against `OGD` coordinate freezing and unguarded `P_-` training. Kill if freezing the park coordinates admits equal B progress.
- **Old-task retention check:** Verify `A` and rare `C` at every admitted and rejected tick, and verify `P_+` service at `T_due` on unseen inputs.

#### 04. Certify return options against uncertain `k`-of-`m` future arrival menus (P)
- **Mechanism:** Instead of assuming a single named return pair will arrive by `T_due`, certify that the outbound landing and `S_post` remain returnable under *every* `k`-element subset of a declared arrival class `M_ret` (adversarial or missing-record arrival uncertainty).
- **Novelty vs nearest prior art:** [Pocket parks][pockets] and robust MPC handle bounded state disturbances; here the uncertainty is combinatorial over which truthful records actually appear in the stream before `T_due`. Simplest same-budget control: buffer one observed return pair locally (paying record-storage bytes) and replay it at `T_due`.
- **Cheapest first test:** Enumerate a 6-record `M_ret` where any 2 records may fail to arrive; compare `k`-of-`m` returnability against buffering 2 return records at equal memory bytes. Kill if local record buffering uses fewer bytes than the `k`-of-`m` certificate.
- **Old-task retention check:** Run all worst-case missing-record realizations and verify `A` and rare `C` at `T_due`, logging refusals when arrival diversity drops below `k`.

#### 05. Spend intervening `P_-` work to widen the returnable basin (P)
- **Mechanism:** Among functionally equivalent due B batches in `P_-` (matched immediate B gain and `A/C` safety), select the one whose side-effect moves the state to a point covered by *more* disjoint return pairs in `M_ret`, turning ordinary B service into return-option insurance.
- **Novelty vs nearest prior art:** [Return corridors][return] spend today's examples before branching; [control-minimization CL][control-cl] penalizes drift globally. This uses free redundancy among already-due `P_-` batches to expand discrete cross-component return coverage. Simplest same-budget control: pick the `P_-` batch with smallest parameter displacement from the outbound landing point.
- **Cheapest first test:** Build a 2-step `P_-` menu where two equal-B batches have equal distance from `s_opt` but cover 1 vs 3 return pairs in `M_ret`; test return rate under random record drops. Kill if minimum-displacement selection matches return coverage.
- **Old-task retention check:** Match initial margins on `A` and rare `C` across both batch choices and verify held-out `A/C` before and after the return crossing.

#### 06. Compress the return certificate to a component pre-image witness (P)
- **Mechanism:** Replace full weight snapshots and per-trajectory enumeration with a compact algebraic/interval witness `(B_ret, h_ret)` certifying that any state in box/ellipsoid `B_ret ⊂ P_-` maps into `P_+` under a named return rule `h_ret`, audited strictly on byte count against compressed checkpoints.
- **Novelty vs nearest prior art:** Certified continual learning and interval-bound training certify input balls around fixed weights; here the certified set is a weight-space pre-image of a discrete cross-component batch map. Simplest same-budget control: 4-bit quantized weight delta or rank-1 LoRA checkpoint of `θ_0`.
- **Cheapest first test:** Compute exact byte sizes of `(B_ret, h_ret)` vs 4-bit delta checkpoints on a 2-layer toy MLP with a 2-component quadratic park; verify zero false admissions on held-out post-crossing states. Kill if the compressed checkpoint is smaller at the same return accuracy.
- **Old-task retention check:** Check held-out `A` and rare `C` at the corners and interior of `B_ret` after applying `h_ret`, rejecting any witness with an unsafe corner.

#### 07. Certify return crossings under carried momentum and Adam slots (P)
- **Mechanism:** Include the carried first and second optimizer moments `(m, v)` accumulated during `P_-` B updates inside the return-option certificate, verifying that the return pair crosses back to `P_+` under the live stateful optimizer without resetting slots.
- **Novelty vs nearest prior art:** `#271` and `#260` handle correlated slots on outbound/entry steps; [return corridors][return] assume a fixed trajectory law. Here the carried `P_-` momentum actively opposes or deflects the reverse jump across `x = 0`. Simplest same-budget control: reset optimizer slots at `T_due` before running the return pair (if legal), or hold a low-momentum cap while in `P_-`.
- **Cheapest first test:** Port R1 to heavy-ball (`β = 1/2`) and diagonal Adam with 2 intervening `P_-` B steps; test whether a stateless return certificate fails on carried `m` while a slot-aware landing succeeds. Kill if a simple momentum-norm cap during `P_-` ties on B progress and return rate.
- **Old-task retention check:** Evaluate `A` and rare `C` at return *and* on the next ordinary `P_+` update after return, catching delayed momentum coasting off `P_+`.

#### 08. Price return-option crossings against compressed checkpoint-plus-replay (I)
- **Mechanism:** Build an adversarial falsifier that gives the baseline the exact byte budget of the return-option certificate to store a compressed `θ_0` delta plus a tiny replay buffer of the `P_-` B updates, then tests whether any regime still favors a no-snapshot return crossing.
- **Novelty vs nearest prior art:** Standard checkpointing/rollback is well known; this is a mandatory kill-gate audit ensuring `#282#04` does not win merely by forbidding cheap compressed snapshots. Simplest same-budget control: this card *is* the control.
- **Cheapest first test:** Sweep byte budgets (16 to 256 bytes) and post-crossing horizons (`H = 1..5`) on R1-scaled linear/ReLU toys; plot the frontier of (bytes, tick-3 latency, retained B accuracy, `A/C` pass rate). Kill `#282#04` if compressed checkpoint + replay dominates everywhere.
- **Old-task retention check:** Require both arms to pass identical held-out `A` and rare `C` floors at every published boundary, including during replay after rollback.

### Batch a crossing with a needed old-job repair (#282#10)

#### 09. Co-batch a crossing B record with an overdue A repair at a shared deadline (P)
- **Mechanism:** Pair an indivisible truthful `B` record (supplying most of the cross-component displacement) with an overdue truthful `A` repair record in one native batch so the single atomic commit lands on `P_-`, meets `B`'s deadline, and brings `A_rep` back under its SLA.
- **Novelty vs nearest prior art:** [GEM][gem] edits gradients to protect old tasks; [GraB][grab] reorders examples within an epoch; [silent-DoF replay][silent-replay] interleaves replay without crossing a disconnected park barrier. Here neither record is modified, and postponing either misses its own deadline. Simplest same-budget control: run `r_A` and `r_B` in separate batches (both orders) or use GEM/GraB at matched compute.
- **Cheapest first test:** Generalize R2 to a 10-record pool with 3 overdue `A` tasks and 3 `B` crossing offers; compare co-batched crossing against solo repair, solo crossing, both sequential orders, GEM, and GraB. Kill if sequential rehearsal or GraB meets the same joint deadline rate.
- **Old-task retention check:** Evaluate `A_park` and **unseen** `A_rep` generalization holdouts plus unrelated rare `C` immediately after the commit and after one subsequent ordinary update.

#### 10. Pick the crossing-compatible repair among equally good overdue A repairs (P)
- **Mechanism:** When an overdue old job has multiple truthful repair records that reduce `A_rep` equally well in isolation, select the repair whose secondary gradient components cancel `r_B`'s park-normal overshoot at the destination (separating `r_A` from `r_A_bad` in R2).
- **Novelty vs nearest prior art:** MIR and [reliability-informed replay][rifar] rank old examples by solo forgetting/loss; they do not select among equal-quality repairs by their finite-step steering of a co-batched cross-component jump. Simplest same-budget control: pick the highest-loss overdue `A` repair (MIR-style) and co-batch it with `r_B`.
- **Cheapest first test:** Construct a pool of 6 equally good truthful `A_rep` repairs (matched solo `A_rep` drop and `A_park` safety) where only 2 close `A_park` when co-batched with `r_B`; compare crossing-aware repair selection vs highest-loss and random repair selection. Kill if highest-loss repair matches landing rate.
- **Old-task retention check:** Verify that the selected repair transfers to unseen `A_rep` examples at least as well as the unselected repairs, and check unrelated rare `C`.

#### 11. Use B's crossing displacement to cancel an overdue repair's park violation (P)
- **Mechanism:** Exploit the symmetric case where an overdue `A` repair record cannot be run alone because its own gradient knocks the learner off `P_+` (e.g., due to shared features with `A_park`), yet co-batching it with a due `B` crossing record cancels the park-normal error at `P_-`.
- **Novelty vs nearest prior art:** Standard replay assumes individual old examples are safe to rehearse alone (though [2506.04377][replay-forgetting] notes replay can worsen forgetting under conflict). Turning an individually unsafe repair into a safe cross-component landing via a due `B` record is a distinct two-sided cancellation. Simplest same-budget control: dampen/clip the solo repair step size so it stays on `P_+`, then run `B`.
- **Cheapest first test:** Modify R2 so `r_A` alone leaves `P_+` (`A_park ≠ 0`), while `{r_A, r_B}` lands exact on `P_-`; compare against half-step clipped `r_A` followed by `r_B` at equal tick budget. Kill if step-damped solo repair + `B` meets both deadlines.
- **Old-task retention check:** Evaluate held-out `A_park`, unseen `A_rep`, and rare `C` on every published tick, verifying that no intermediate violation is hidden.

#### 12. Audit co-batched repairs for unseen old-task transfer vs sentinel memorization (I)
- **Mechanism:** Pair every co-batched repair test with a diagnostic split separating the co-batched repair record, the `A_park` sentinel, and an **unseen** drifted `A_rep` holdout, rejecting any co-batch whose apparent repair gain disappears on the unseen holdout.
- **Novelty vs nearest prior art:** Directly operationalizes the [idea ledger's][ledger] retention and margin-confound rules for `#282#10`; not a new learning primitive, but a required falsifier against cherry-picked sentinel anchors. Simplest same-budget control: a sentinel-only anchor paired with `r_B`.
- **Cheapest first test:** On a small multi-feature linear/MLP drift task, compare a genuine drifted-feature repair record against a sentinel-matching record that has zero alignment with the unseen `A_rep` holdout; verify the audit flags the sentinel arm. Kill the audit only if sentinel and unseen transfer are always colinear.
- **Old-task retention check:** Report unseen `A_rep` accuracy, `A_park` defect, and rare `C` margin separately, matching initial per-item margins.

#### 13. Co-batch a crossing with a scarce rare-C emergency repair (P)
- **Mechanism:** When the overdue repair belongs to a *rare* old task `C` (tiny pool, high forgetting risk), use a single scarce truthful `C` record simultaneously to restore `C`'s margin and to close `A_park` at `P_-` alongside the crossing `B` record, avoiding spending a separate tick or extra scarce `C` examples.
- **Novelty vs nearest prior art:** Rare-event replay and [replay-forgetting][replay-forgetting] show naive upsampling of scarce slices can hurt common tasks; here the scarce `C` record is spent once, doing double duty as a crossing stabilizer. Simplest same-budget control: run the scarce `C` record in a separate rehearsal batch before `B` at equal total `C` exposures.
- **Cheapest first test:** Give a 3-task (`A_park`, rare `C`, crossing `B`) toy a budget of 1 `C` record per window and a shared tick-1 deadline; compare co-batched `{r_C, r_B}` vs `C`-then-`B` and vs weighted replay. Kill if `C`-then-`B` or equal-exposure replay matches `C` retention and `B` deadline hit rate.
- **Old-task retention check:** Test unseen rare `C` examples (distinct from `r_C`), routine `A_park`, and a subsequent common update to ensure `C` is not immediately overwritten.

#### 14. Beat GEM across a non-convex barrier without editing gradients (P)
- **Mechanism:** Identify regimes where [GEM][gem] (projecting `g_B` onto `⟨g_B, g_A⟩ ≥ 0`) stalls on the wrong side of the park separator `x = 0` or lands off `P_-` after a finite step, while co-batching the unmodified truthful pair `{r_A, r_B}` crosses cleanly with zero gradient surgery.
- **Novelty vs nearest prior art:** [GEM][gem] and [OGD][ogd] enforce first-order linear non-interference, which is blind to disconnected nonlinear level sets. This tests whether unmodified truthful co-batching strictly expands the feasible crossing set over first-order projection. Simplest same-budget control: GEM (and exact finite-step multi-constraint retraction, charged as an off-language edit).
- **Cheapest first test:** Run R2 with `⟨g_B, g_A⟩ < 0` (conflicting `x` components) and compare co-batch `{r_A, r_B}` against GEM projection of `g_B` onto `g_A` and against OGD onto `∇A_park` at the same native step size. Kill if GEM + one repair step lands on `P_-` within the same deadline.
- **Old-task retention check:** Check `A_park`, unseen `A_rep`, and rare `C` after the commit; verify that GEM's failure is not merely a step-size mismatch by sweeping GEM's step size.

#### 15. Pre-filter repair-crossing pairs by a finite leverage-ratio band (P)
- **Mechanism:** Derive a cheap, checkable band on the ratio of repair-gradient norm to crossing-gradient norm (relative to the native step size and separator distance) that certifies when an overdue repair is strong enough to close `A_park` at `P_-` without pulling the batch back into the unsafe gap `x ≈ 0`.
- **Novelty vs nearest prior art:** `#271` previews full candidate pairs; [GradMatch][gradmatch] fits weighted sums. A leverage-ratio band is a fast necessary condition for indivisible equal-weight co-batches across a separator, cutting preview search cost. Simplest same-budget control: exhaustive preview over the small candidate pool (charging preview FLOPs).
- **Cheapest first test:** Sweep `r_A` and `r_B` norms on a 50-pair R2-like pool; measure precision/recall of the band and wall-clock preview savings vs exhaustive pair preview. Kill if exhaustive preview is cheaper or if the band misses >10% of valid co-batches.
- **Old-task retention check:** Verify that pairs passing the band and selected by preview still pass held-out `A_park`, unseen `A_rep`, and rare `C`, with zero false-safe admissions.

#### 16. Clear a multi-step repair backlog across a sequence of atomic crossings (P)
- **Mechanism:** When a single co-batched crossing only partially clears an overdue repair (as in R2, where `u²` drops from `9` to `9/4`, meeting the tick-1 SLA without reaching `0`), chain a second lawful co-batch (staying on `P_-` or crossing to another component) to drive the residual repair to zero without pausing `B` service.
- **Novelty vs nearest prior art:** Standard continual replay clears backlogs in offline phases; [silent-DoF replay][silent-replay] avoids offline phases within one component. Here partial repair installments are piggybacked across discrete park crossings. Simplest same-budget control: take one dedicated offline repair tick to zero `A_rep` immediately, then run `B`.
- **Cheapest first test:** Extend R2 to 2 ticks with a tick-1 SLA (`u² ≤ 9/4`) and tick-2 SLA (`u² ≤ 1/4`) plus two due `B` offers; compare chained co-batches against dedicated repair tick + delayed `B`. Kill if dedicated repair + `B` meets all SLAs at equal compute.
- **Old-task retention check:** Evaluate `A_park`, unseen `A_rep`, and rare `C` at both tick 1 and tick 2, plus a third tick with no repair records to ensure residual drift does not rebound.

### Couple return-option crossings with overdue repairs (#282#04 × #282#10)

#### 17. Steer an outbound crossing into the returnable basin via an overdue repair (P)
- **Mechanism:** Co-batch an overdue `A` repair `r_A` with the outbound `B` record `r_B` so the repair's secondary gradient lands the learner specifically inside the *returnable* subset `R ⊂ P_-` (where `r_B` paired with a non-repair stabilizer lands in a stranded region of `P_-`).
- **Novelty vs nearest prior art:** Genuine interaction of `#282#04` and `#282#10`: neither one-way repair-crossing (`#282#10`) nor non-repair return-option crossing (`#282#04`) alone clears both the tick-1 overdue repair and the tick-3 `P_+` return without a snapshot. Simplest same-budget control: stack `#282#10` (one-way repair-crossing) with an equal-byte compressed snapshot of `θ_0`, or run separate repair + return-option crossing.
- **Cheapest first test:** Combine R1 and R2 in `(x, y, u, z)`: make `{r_A, r_B}` land at `(-5/4, 3/4, 3/2, 0)` (returnable via `R_a`) while a non-repair crossing lands at `(-1, 0, 3, 0)` (stranded + misses `A_rep`). Run a 2×2 factorial ablation of (returnable vs one-way) × (repair-coupled vs separate). Kill if the stacked separate controls match on-time A/B/C coverage.
- **Old-task retention check:** Test `A_park`, unseen `A_rep`, and rare `C` at tick 1, during `P_-` B work, and after tick-3 return to `P_+`, confirming `z` (B work) survives return.

#### 18. Exercise the return option by co-batching it with a newly due old-job repair (P)
- **Mechanism:** Instead of spending an idle return batch at `T_due`, certify that the return crossing from `P_-` back to `P_+` is executed by co-batching a return-driving record with a newly due `A_rep` (or rare `C`) repair record, clearing both the lane return and the old-job repair in one atomic commit.
- **Novelty vs nearest prior art:** Rollback and [return corridors][return] treat return as pure overhead; co-batching return with a due repair turns the return step into productive old-task maintenance. Simplest same-budget control: execute a plain return pair at `T_due`, then run the repair at `T_due + 1` (or rollback + repair).
- **Cheapest first test:** Extend R1 so a second `A_rep` defect comes due at tick 3 alongside the `P_+` return deadline; compare return-by-repair against plain return + separate repair and against snapshot rollback + repair. Kill if plain return + repair meets the same tick-3 SLA.
- **Old-task retention check:** Evaluate `A_park`, unseen `A_rep`, rare `C`, and retained `P_-` B accuracy at tick 3 and after one further routine tick on `P_+`.

#### 19. Certify returnability across mandatory overdue repairs while away in `P_-` (P)
- **Mechanism:** Expand the allowed post-crossing set `S_post` in `#282#04` to include mandatory overdue `A` or rare `C` repairs that may trigger *while* the learner is in `P_-`, certifying that executing those repairs does not eject the learner from the returnable pre-image `R ⊂ P_-`.
- **Novelty vs nearest prior art:** `#282#04` only considers planned `P_-` B work; real continual streams inject unplanned maintenance repairs. Without repair-aware returnability, an urgent repair in `P_-` can silently strand the learner. Simplest same-budget control: defer all repairs until after returning to `P_+`, or keep a compressed snapshot of `θ_0`.
- **Cheapest first test:** Inject an unplanned overdue `C` repair at tick 2 in R1; compare a repair-aware outbound landing against a B-only returnable landing and against deferring the repair (which fails `C`'s tick-2 SLA). Kill if deferring the repair or re-routing via snapshot ties on all SLAs.
- **Old-task retention check:** Check `C` at tick 2 (no deferred SLA miss), `A_park` at every tick, and `P_+` service + retained B at tick 3.

#### 20. Trade immediate repair depth for a live return option under hard SLAs (P)
- **Mechanism:** Formalize the Pareto choice when a full repair (`A_rep → 0`) strands the learner in `P_-` (or forces staying in `P_+`), whereas a partial co-batched repair (`A_rep ≤ SLA_1`) lands inside the returnable basin `R` so both `B` and the later `P_+` job succeed.
- **Novelty vs nearest prior art:** Standard replay minimizes immediate old-task loss greedily; here minimizing `A_rep` past its SLA destroys future cross-component returnability. Simplest same-budget control: greedy minimum-`A_rep` repair selection subject to `A_park = 0`.
- **Cheapest first test:** In a 3-tick R1+R2 fixture with two lawful repair-crossing pairs—one giving `(A_rep = 0, stranded)` and one giving `(A_rep = 9/4 ≤ SLA, returnable)`—compare SLA-aware return-option selection vs greedy repair minimization. Kill if greedy repair leaves a valid return pair equally often on natural pools.
- **Old-task retention check:** Verify that the partial repair (`A_rep = 9/4`) genuinely holds on unseen `A_rep` inputs through tick 2 and is fully cleared by tick 3 without dragging down rare `C`.

#### 21. Pre-pay return-crossing momentum with an overdue repair during the `P_-` stay (P)
- **Mechanism:** Under heavy-ball or Adam, when an overdue `A` or `C` repair is due during the `P_-` stay, choose among equivalent truthful repair records the one whose carried optimizer momentum points toward `P_+`, lowering the displacement needed from the future return pair at `T_due`.
- **Novelty vs nearest prior art:** Combines momentum-assisted landing (`#242`/`#250`) with `#282#04` returnability and `#282#10` overdue repairs: the repair pays its own old-task debt while pre-charging the reverse crossing. Simplest same-budget control: run an arbitrary equivalent repair in `P_-` and reset momentum before the return batch (or use a stronger return pair).
- **Cheapest first test:** In a heavy-ball (`β = 1/2`) R1+R2 fixture with a weak future return menu `M_ret` that cannot cross back from zero momentum, test whether a momentum-aligned overdue repair in `P_-` unlocks exact `P_+` return where an unaligned equivalent repair fails. Kill if momentum reset + best available return pair matches return rate.
- **Old-task retention check:** Check `A_park`, unseen `A_rep`, and rare `C` at tick 2, at tick-3 return, and at tick 4 (to verify the charged momentum does not overshoot `P_+`).

#### 22. Stress-test returnable and repair-coupled crossings on natural labeled pools (I)
- **Mechanism:** Freeze an independently labeled multi-task regression/classification pool (no endpoint-constructed targets), induce a real 2-component park (e.g. sign-symmetric 2-layer ReLU or quadratic read) and genuine old-task drift, and measure how often return-option crossings, repair-coupled crossings, and their combination actually exist and beat stacked controls.
- **Novelty vs nearest prior art:** Mandatory falsification gate against engineered-pool artifacts (carrying forward `#282#22` and the [idea ledger's][ledger] variance/natural-pool rules); not a primitive. Simplest same-budget control: compressed snapshot + replay, GEM, GraB, and separate-batch scheduling on the exact same natural pool.
- **Cheapest first test:** Run a CPU-only 2-layer tiny network (exact or small-batch SGD/Adam, 10 seeds) on a natural multi-task split with frozen arrival windows; gate on whether target variance in on-time joint admissions exceeds seed variance and whether any proposed arm beats the best equal-byte/compute control. Kill the branch if natural-pool hit rate is near zero or ties controls.
- **Old-task retention check:** Log blind held-out `A_park`, unseen `A_rep`, and rare `C` at every published boundary, counting all refusals and deadline misses as outcomes.

## Ranked deeper questions

1. **Can a no-snapshot return-option crossing beat an equal-byte compressed weight snapshot plus B-replay?** (01, 02, 06, 08) Fix a strict byte budget and post-crossing horizon; compare a return-option certificate against a quantized/LoRA `θ_0` delta plus replaying the `P_-` B updates after rollback. Retire `#282#04` as a primitive if compressed checkpoint + replay dominates on retained B accuracy, return latency, and `A/C` safety across realistic horizons.
2. **In natural (non-engineered) pools, do overdue old-task repairs actually steer crossings onto `P_-`, or do they mostly push crossings off target?** (09, 10, 11, 14, 22) Measure the natural hit rate of truthful overdue repairs that simultaneously improve unseen `A_rep` generalization, close `A_park` at `P_-`, and meet `B`'s deadline, compared to separate batches, GEM, and GraB at equal compute. Retire `#282#10` if off-target interference dominates or if sequential rehearsal/GraB matches it.
3. **Does coupling overdue repair with return-option crossing yield an interaction that beats stacking them separately?** (17, 18, 19, 20, 21) Run the 2×2 factorial ablation of (return-option vs one-way) × (repair-coupled vs separate) at matched bytes and deadlines. Keep the merge only if repair-steered landing into `R ⊂ P_-` or return-by-repair achieves on-time A/B/C coverage unreachable by the stacked single-seed controls.
4. **Does a live returnability envelope survive carried optimizer state and arrival uncertainty without collapsing into freezing?** (03, 04, 05, 07) Measure how much useful `P_-` B learning remains admissible inside `S_post` under warmed Adam and `k`-of-`m` arrival uncertainty; retire the envelope if it admits no more B progress than locking the park coordinates (`OGD`) or staying in `P_+`.

[parent]: https://github.com/manojbajaj95/cl/pull/282
[ledger]: https://github.com/manojbajaj95/cl/blob/2d8f39d9cdfeeff351dfa37885c0ed0bea17cb71/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/2d8f39d9cdfeeff351dfa37885c0ed0bea17cb71/reviews/flood-triage.md#L401
[return]: https://github.com/manojbajaj95/cl/blob/devin/1795562037-return-corridors/tree/return-corridors.md
[pockets]: https://github.com/manojbajaj95/cl/pull/270
[gem]: https://arxiv.org/abs/1706.08840
[grab]: https://arxiv.org/abs/2205.10733
[ogd]: https://arxiv.org/abs/1910.07104
[gradmatch]: https://arxiv.org/abs/2103.00123
[admission-audit]: https://arxiv.org/abs/2609.10873
[control-cl]: https://arxiv.org/abs/2602.04542
[recovery-cl]: https://arxiv.org/abs/2604.17578
[silent-replay]: https://arxiv.org/abs/2609.31630
[rifar]: https://arxiv.org/abs/2610.03079
[replay-forgetting]: https://arxiv.org/abs/2506.04377
