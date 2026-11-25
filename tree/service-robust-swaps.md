# Service-robust swaps: keep paired openers live through ordinary A/C work and partner no-shows

**Status:** Ideas only. The worked examples below are exact-arithmetic sanity checks, not pilot results; every proposed first test is a pencil-and-paper or CPU check. No GPU.

**Parent:** [Paired tail clips](paired-tail-clips.md) ([PR #249](https://github.com/manojbajaj95/cl/pull/249)). **Review seeds:** [Flood triage, line 364](https://github.com/manojbajaj95/cl/blob/489e6acf8d4acada424aa10385eb0382cd276da7/reviews/flood-triage.md#L364), score-3 cards #249#07 (a paired swap proven to hold through a bounded run of ordinary A and C service steps) and #249#09 (an explicit timeout path for an opener whose partner queue never arrives). Following the [idea ledger](https://github.com/manojbajaj95/cl/blob/489e6acf8d4acada424aa10385eb0382cd276da7/reviews/idea-ledger.md), every test must check ordinary A/C retention, compare against the strongest components stacked at equal budget, and treat **I**-labelled cards as controls or audits rather than pilot nominations.

## The two obligations

- **Service-closed reciprocal swap certificate.** Freeze the learner, optimizer, independently queued truthful B pools, protected core `K`, reachable envelope `H`, allowed ordinary A/C service step family `S` with bound `m`, and allowed post-seam suffixes before selecting `(R, L)`. Write `R`, `L`, and each `s ∈ S` for the complete state transitions (weights, optimizer slots, running stats, randomness, and clocks), not gradient-only maps. Both `R` and `L` must fix every state in `K` as read by the existing A/C proof. For every legal intervening run `w ∈ S^{≤m}`, certify that: (1) every intermediate prefix of `w` preserves A/C floors on `R(H)` and `L(H)`; (2) `w` maps `R`'s repaired landing tube into `Fix(L)` and keeps the untouched left tail inside `L`'s active repair domain (and symmetrically for `L` then `w` then `R`); and (3) the second opener stays eligible at actual execution precision and admits both residual orders without undoing `w`'s A/C service progress. A/C safety of `w` alone does not imply swap closure.
- **Unmatched-opener timeout continuation.** Pair the two-order swap contract with an explicit timeout continuation `T_R` (and symmetrically `T_L`) for each unmatched prefix `(R, w)` when deadline `τ` passes without the partner queue arriving. `T_R` is priced as a right to keep serving A and C—and recurring B traffic on the arrived queue—without rolling back `R` or `w`, and without fabricating a synthetic partner example. Because the opposite tail stays live in the reachable envelope, `T_R` must declare the exact narrower post-timeout suffix menu that remains A/C-safe across the entire post-wait envelope, bind activation of `T_R` to explicit revocation of the partner's original swap ticket so a late arrival at `τ + 1` cannot silently unlock spent margin, and route late arrivals to safe refusal or fresh recertification.
- **Joint coupling.** Intervening service `w` and timeout continuation `T_R` are coupled: a service step can keep one swap order safe while breaking `T_R`, or keep `T_R` safe while pushing the untouched tail out of the partner's active repair domain. Claims that combine both obligations must beat stacking the best service-closed swap with the best standalone timeout or rollback path at equal budget.

**Shared falsifier.** Compare against: (a) `#240#03`/`#249#01` swap with no intervening service plus pausing A/C service until both queues arrive; (b) fresh recertification after every service step; (c) a fixed two-sided global clamp; (d) freezing shared parameters during the wait; (e) checkpoint rollback to the pre-opener state (charging lost `R` B-gain, lost intervening A/C service, and any un-reverted serving state); (f) saga-style compensating undo; and (g) negative controls—a service step that pushes one landing tube out of the opposite item's reach, and an unmatched prefix whose timeout path breaks an old floor. Also run the [#113 smooth/accumulation null](https://github.com/manojbajaj95/cl/pull/113) and a tail-free pack. Match B gain **per queue**, ordinary A/C service completed during the wait, raw arrivals, steps, peak bytes (including verifier and checkpoint state), checks, and deadlines, or report the exact Pareto tradeoff. Measure hazardous admits, honest refusals, worst old A/C slice, and late-arrival safety at every exposed prefix, intermediate service step, timeout boundary, and post-seam suffix.

**Nearest precedents (checked via alphaXiv).** Rely-guarantee concurrency ([algebraic rely-guarantee composition, 2607.17536][rg]) already proves invariance under bounded environment interference; it is the formal control, not a claim that interference-freedom is new. Transactional memory and rollback for stateful agents ([MemTX, 2607.23929][memtx]; [ChronoMem, 2607.27773][chronomem]; [Audit-First Rollback, 2609.00406][auditrb]) and classical sagas/leases ([Sagas][sagas]) already handle staged commit, compensation, and expiry; [KV-Cache Retention Breaks Rollback Consistency (2608.15939)][kvrb] shows that rollback in stateful learners can leak un-reverted serving state, making it a sharp control for forward timeout vs rollback. Related sibling tree nodes—[escrowed paired leases (#214)][pr214], [margin loans (#233)][pr233], [sealed gates (#234)][pr234], [menu replacements (#235)][pr235], [echo-absorbing work (#238)][pr238], and [verified renewal (#243)][pr243]—cover partner defaults, pending loans, and slot contraction in other mechanisms. The narrower candidate primitive here is whether **truthful one-sided tail openers under an unchanged optimizer** can carry an existing A/C proof across bounded stateful A/C service *and* gracefully downgrade to a certified forward one-sided continuation on partner no-show, cheaper than pausing, per-step rechecking, or rollback.

## Paper fixtures

All fixtures use a two-coordinate shared-state learner `(h, u)` with envelope `H = {(−3/2, 0), (−1/2, 0), (0, 0), (1/2, 0), (3/2, 0)}` and protected core `K = {(−1/2, 0), (0, 0), (1/2, 0)}`. Two independently queued truthful B views predict `max(h + u − 1, 0)` (right queue) and `max(u − h − 1, 0)` (left queue), both with target zero. One ordinary SGD step with learning rate `1/2` on half squared error yields:

- `R(h, u) = (h − g_R/2, u − g_R/2)` where `g_R = max(h + u − 1, 0)`, fixing `h + u ≤ 1` and repairing `(3/2, 0) ↦ (5/4, −1/4)` (B loss `1/8 → 0`);
- `L(h, u) = (h + g_L/2, u − g_L/2)` where `g_L = max(u − h − 1, 0)`, fixing `u − h ≤ 1` and repairing `(−3/2, 0) ↦ (−5/4, −1/4)` (B loss `1/8 → 0`).

Both `R` and `L` update *both* shared coordinates `h` and `u`, fix every point in `K`, and fix each other's repaired landings (`L(5/4, −1/4) = (5/4, −1/4)` and `R(−5/4, −1/4) = (−5/4, −1/4)`). Old-task gaps are `A(h, u, d) = 2 − (h + u) − d ≥ 0` and `C(h, u, d) = 2 − (u − h) + d ≥ 0` for cumulative residual shift `d ∈ {−1, 0, +1}`. Before either opener arrives, neither `d = +1` (fails `A = −1/2` at `(3/2, 0)`) nor `d = −1` (fails `C = −1/2` at `(−3/2, 0)`) is safe across `H`.

**S1 — Service-closed swap vs asymmetric tube-escaping service step.**
- *S1a (service-closed):* Take the ordinary A/C service step `S_ok(h, u) = (7/8 · h, u)`, i.e. one SGD step (`η = 1/8`) on truthful old-task loss `1/2 h²`. For every `m ∈ {0, 1, 2}` (and up to `m = 3`, since `(3/2)(7/8)³ = 1029/1024 > 1`), running `S_ok^m` between `R` and `L` in *either* order preserves A/C floors at every intermediate step, keeps the first landing fixed by the second opener (at `m = 2`, `R`'s landing moves `(5/4, −1/4) → (245/256, −1/4) ∈ Fix(L)`), keeps the untouched opposite tail strictly active (`(−3/2, 0) → (−147/128, 0)`), and admits both `d = ±1` after the second opener. At `m = 4`, `(3/2)(7/8)⁴ = 7203/8192 < 1`: the untouched tail crosses the hinge and the second opener becomes a zero-gain no-op, showing the horizon `m` is genuinely finite.
- *S1b (tube-escaping negative):* Replace `S_ok` with one ordinary step `w_asym(h, u) = (h + 1/4, u + 1/4)`. During the interleave (`d = 0`), `w_asym` is A/C-safe in *both* orders. In order `L → w_asym → R`, the untouched right tail `(3/2, 0)` moves to `(7/4, 1/4)` (`A = 0`), which `R` repairs back to `(5/4, −1/4)` so both `d = ±1` succeed. In order `R → w_asym → L`, however, `R`'s landing `(5/4, −1/4)` moves to `(3/2, 0)` (`A(d=0) = 1/2`), which `L` fixes unchanged, leaving `h + u = 3/2` at the seam so `d = +1` fails `A = −1/2 < 0`. A/C safety of `w_asym` during the wait does not certify a two-order swap.

**S2 — Unmatched opener timeout continuation and late-arrival revocation.**
Suppose `R` arrives, `m ∈ {0, 1, 2}` steps of `S_ok` run, and `L` never arrives by deadline `τ`. Because `L` never arrived, the untreated left tail remains live (`(−3/2, 0)` at `m = 0`; `(−147/128, 0)` at `m = 2`).
- Rolling back to pre-`R` discards `R`'s B-loss drop (`1/8 → 0`) and all `m` steps of A/C service `S_ok`, and returns to a state where *neither* `d = +1` nor `d = −1` is safe.
- Naively admitting the full two-order menu `{+1, −1}` breaks `C` on the untouched left tail (`C(d = −1) = −1/2` at `m = 0`, `−19/128` at `m = 2`).
- The certified timeout continuation `T_R` keeps `R` and `S_ok^m`, explicitly narrows the post-timeout menu to `{+1}` (where `min A = 0, 5/32, 75/256 ≥ 0` for `m = 0, 1, 2` and `C ≥ 1` everywhere, unlocking a residual move that was illegal pre-`R`), and revokes `L`'s swap ticket.
- *Late-arrival hazard:* If `T_R` executes a `+1` residual shift `(h, u) ↦ (h + 1/2, u + 1/2)` at `m = 0`, `R`'s landing moves `(5/4, −1/4) → (7/4, 1/4)` (`A(d = 0) = 0`) and the left tail moves `(−3/2, 0) → (−1, 1/2)`. If `L` arrives late and is naively allowed to restore the original `{+1, −1}` menu, a second `+1` move gives `A = −1 < 0` on `(7/4, 1/4)`. Timeout must therefore revoke the original swap contract.

**S3 — Service–timeout separation.**
On the same post-`R` envelope `R(H)`:
- `w_asym(h, u) = (h + 1/4, u + 1/4)` keeps the `L → w_asym → R` swap safe (and keeps `d = 0` A/C-safe after `R`), yet breaks `T_R`'s `d = +1` timeout continuation on `(5/4, −1/4) → (3/2, 0)` (`A = −1/2`).
- Conversely, `w_t(h, u) = (h + 1/2, u − 1/2)` leaves `h + u` invariant and lowers `u − h` by `1`, so it keeps `d = 0` and `T_R`'s `d = +1` timeout completely safe (even raising `C` margin by `+1`), yet pulls the untouched left tail `(−3/2, 0) → (−1, −1/2)` inside `Fix(L)` (`u − h = 1/2 ≤ 1`), rendering `L`'s reserved repair vacuous (zero left-queue B gain).
Therefore, certifying intervening service for swap completion and certifying it for partner no-show are genuinely distinct obligations.

## Idea cards

**P** denotes a candidate primitive (a reusable object or operation); **I** denotes an improvement, control, or audit. Every test inherits the shared A/C retention and equal-budget rules above.

### Service-robust swaps (#249#07 seed and extensions)

#### 01. Service-closed swap certificate — P, #249#07 seed
- **Mechanism.** Attach to a reciprocal pair `(R, L)` a certified family `S` of ordinary A/C service steps and horizon `m` such that every `w ∈ S^{≤m}` keeps both landing tubes inside the opposite opener's fixed set, keeps the opposite tail active and repairable, and keeps the second queue's reservation valid with no service pause.
- **Novelty / control.** Rely-guarantee concurrency ([2607.17536][rg]) already certifies interference freedom; the candidate CL primitive is a reusable teaching-swap license that stays valid while live A/C training runs on shared weights. Compare against `#240#03`/`#249#01` with paused service, fresh per-step recertification, a fixed global clamp, and S1b's tube-escaping step.
- **Cheapest first test.** Enumerate S1a (`m ∈ {0..4}`) and S1b across both arrival orders on CPU; require rejection of S1b and horizon expiry before `m = 4`.
- **Old-task retention.** Check A/C at every intermediate `S_ok` step, after the second opener, and on both post-seam residual orders `d = ±1`.

#### 02. Drift-metered swap horizon instead of a fixed step count — P
- **Mechanism.** Compile the swap's allowed intervening service into a checkable monotone budget (e.g. directional drift along the opposite hinge normal) charged per executed A/C step, expiring the swap right before the first step whose cumulative drift could exit `Fix(L)` or cross the untouched tail's hinge.
- **Novelty / control.** Step-count bounds and timed leases (#249#03) are known; a state-free directional meter lets many small orthogonal A/C steps run during a wait while stopping immediately on one large parallel step. Compare against a fixed worst-case step cap `m`, per-step exact rechecking, and pausing service.
- **Cheapest first test.** Mix small and large A/C steps along orthogonal and parallel directions in S1; compare total admitted A/C service before expiry against the tightest sound fixed step count `m`.
- **Old-task retention.** Verify A/C floors on every admitted mixed-step sequence and on the rejected step that exhausts the meter.

#### 03. Cone-filtered A/C admission during an open swap window — P
- **Mechanism.** While `R` is pending, classify incoming ordinary A/C batches against a precompiled safe service cone `C_R`: execute cone-interior batches immediately on live weights and queue only cone-violating batches until `L` arrives or timeout fires.
- **Novelty / control.** Constrained updates (OGD/GEM) project gradients, changing the A/C update itself; here ordinary A/C batches run *unmodified* whenever they fall in `C_R`, trading selective deferral for exact proof reuse. Compare against pausing all A/C traffic, OGD projection at matched A/C progress, and per-batch recertification.
- **Cheapest first test.** Feed an interleaved stream containing both `S_ok` and `w_asym` batches between `R` and `L`; verify `S_ok` runs immediately, `w_asym` is deferred until after `L`, and both orders pass.
- **Old-task retention.** Score both A/C service latency (deferred share) and worst-slice A/C retention during the wait and after the deferred batch executes.

#### 04. Service steps that contract the landing tube back into the opposite fixed set — P
- **Mechanism.** Certify an intervening run of ordinary A/C batches that actively pulls a drifted first-opener landing *inward* toward `K` and deeper into `Fix(L)`, turning a swap that is brittle under raw wait drift into a service-stabilized swap without synthetic replay.
- **Novelty / control.** [Echo-absorbing work (#238)][pr238] contracts optimizer-slot gaps using required C batches; here ordinary A/C steps stabilize a *cross-opener landing tube* so the opposite tail clip stays a no-op on repaired histories. Compare against passive waiting, a synthetic replay step at equal compute, and `#238` stacked with fresh recertification.
- **Cheapest first test.** Add a small outward wait drift to S1 that breaks the swap after 1 idle tick, and test whether one ordinary `S_ok` step restores membership in `Fix(L)` while keeping the untouched tail active.
- **Old-task retention.** Measure A/C loss reduction from `S_ok` itself plus worst-slice A/C across both arrival orders and after an adversarial order where `S_ok` is withheld.

#### 05. Asymmetric per-order service horizons `(m_R, m_L)` — P
- **Mechanism.** When `R → w → L` remains certified for `m_R` ordinary A/C steps while `L → w → R` remains certified for `m_L < m_R`, issue a typed pair of horizons `(m_R, m_L)` rather than truncating both orders to `min(m_R, m_L)` or rejecting the pair.
- **Novelty / control.** Symmetric commutation contracts discard asymmetric headroom; the typed horizon keeps two-order legality up to `m_L` and explicitly documents the extra service window available when the faster-arriving queue is `R`. Compare against symmetric `min(m_R, m_L)` leases and separate single-opener contracts.
- **Cheapest first test.** Modify S1 with asymmetric A/C service step `w_asym` (safe in `L → w → R` for `m_L = 1`, unsafe in `R → w → L` for `m_R = 0`) and measure admitted A/C service vs symmetric `m = 0` pause.
- **Old-task retention.** Check A/C across both orders at their respective horizons and verify strict refusal at `m_R + 1` and `m_L + 1`.

#### 06. Stateful slot-and-clock closure audit under live A/C service — I
- **Mechanism.** Test whether ordinary A/C service steps executed under momentum, Adam `(m, v)`, running BatchNorm/LayerNorm stats, or step-dependent LR schedules break the swap's exact fixed-set identity even when parameter weights stay inside the certified tube.
- **Novelty / control.** Slot drift is already flagged in `#249#04` and `#234`; this is a mandatory falsification control to separate weight-only toy wins from full-state service closure. Compare exact full-state identity, weight-only screening, slot reset (disallowed as a teaching claim), and fresh recertification.
- **Cheapest first test.** Re-run S1a with heavy-ball momentum (`β = 1/2`) and diagonal Adam slots updated by `S_ok`, checking whether `L` still fixes `R`'s repaired landing after `m = 1, 2` service steps.
- **Old-task retention.** Probe a slot-sensitive old-task read after one post-seam A/C batch in addition to immediate A/C outputs.

#### 07. Reusable service-induced negative witness — P
- **Mechanism.** When an ordinary A/C service step `s` pushes a candidate pair's landing tube out of the opposite fixed set, store the minimal `(s-class, landing face)` obstruction so future pair searches prune every candidate pair exposing that face without re-simulating full `m`-step interleaves.
- **Novelty / control.** Conflict-driven pruning and `#249#06` prefix counterexamples are known; the candidate object is an *interleave-specific* negative edge indexed by the ordinary service class `S`, reusable across different B pools sharing the same A/C workload. Compare against exact transition caching and `#249#06` per-pair checks.
- **Cheapest first test.** Construct 6 candidate pairs in S1 where 4 expose the `h + u = 1` face vulnerable to `w_asym` and 2 sit safely interior; verify the witness prunes the 4 without falsely pruning the 2.
- **Old-task retention.** Verify A/C on the 2 surviving pairs across all `w ∈ S^{≤m}` and confirm the pruned pairs truly fail an old slice under `w_asym`.

#### 08. Mid-wait partner rebinding without pausing service — P
- **Mechanism.** If ordinary A/C service drifts the landing tube or untouched tail close to `L_1`'s boundary before `L_1` arrives, atomically rebind the open reservation to a pre-certified substitute `L_2` from the same B queue whose fixed set contains the drifted tube and whose active domain still repairs the tail—without rolling back `R` or pausing A/C.
- **Novelty / control.** [Menu replacements (#235)][pr235] swap reserved finishes under invalidating updates, and `#249#05` substitutes the *first* item; here the *waiting second opener* is rebound mid-service to extend the live swap window. Compare against pausing service at `L_1`'s boundary, triggering early timeout, and full replanning.
- **Cheapest first test.** Give the left queue two truthful hinge items `L_1` (threshold `−1`) and `L_2` (threshold `−3/4`); run `S_ok^4` where `L_1` goes vacuous (`−7203/8192 > −1`) while `L_2` still repairs the tail and fixes `R`'s drifted landing.
- **Old-task retention.** Check A/C at the rebind tick, after `L_2` arrives, and on fallback if `L_2` is absent from the queue.

#### 09. Two-tier service scheduler: tube-invariant vs slack-consuming A/C batches — P
- **Mechanism.** Partition the ordinary A/C service queue into batches certified invariant on the swap tube (run without debiting the swap horizon) and batches that consume tube slack (debited against the horizon and capped before exit).
- **Novelty / control.** Priority scheduling is standard; the candidate CL interface is a *tube-invariance tag* compiled from the active swap certificate that lets non-interfering A/C work run unboundedly during a long partner wait. Compare against a uniform step cap `m` and full per-batch verification.
- **Cheapest first test.** Mix `u`-orthogonal A/C batches (leaving both `h + u` and `u − h` unchanged) with `S_ok` batches in S1; verify unbounded orthogonal service plus `m ≤ 2` `S_ok` steps keep both swap orders certified.
- **Old-task retention.** Confirm zero A/C regression on both tiers and verify that a mislabelled slack-consuming batch is caught by the tube check.

#### 10. Precision-bound audit for multi-step interleaved service — I
- **Mechanism.** Track worst-case floating-point or quantized rounding across `m` interleaved A/C steps jointly with the two opener hinges, rejecting any swap whose rounded tube can straddle an opener's active/inactive boundary.
- **Novelty / control.** Interval arithmetic and `#249#17` quantization checks are prior art; this audit prevents false service-robustness claims where exact rational arithmetic stays inside `Fix(L)` while `bf16`/`fp16` rounding triggers a spurious clip. Compare against exact-arithmetic screening and higher-precision execution.
- **Cheapest first test.** Run S1a at `m = 3` (`(3/2)(7/8)³ = 1029/1024 ≈ 1.0049`) under 8-bit/16-bit rounding where `1029/1024` rounds to `1.0`, turning `L` into an unexpected no-op.
- **Old-task retention.** Check A/C on both rounded and unrounded trajectories and verify conservative refusal when rounding crosses the boundary.

### Unmatched-opener timeout continuations (#249#09 seed and extensions)

#### 11. Certified forward timeout continuation for an unmatched opener — P, #249#09 seed
- **Mechanism.** Pair every dual-order swap contract with an explicit timeout continuation `T_R` (and `T_L`) that, on partner no-show at deadline `τ`, retains `R` and all intervening A/C service, unlocks the certified one-sided suffix menu safe across the full envelope (including the still-live opposite tail), and refuses unsafe suffixes without fabricating the missing partner.
- **Novelty / control.** Classical sagas ([Sagas][sagas]) compensate backward, and transactional agent memory ([MemTX, 2607.23929][memtx]) aborts uncommitted writes; the candidate primitive is a *forward, no-undo, no-synthetic-data* continuation that monetizes partial tail repair into a strictly larger safe suffix menu than pre-`R`. Compare against pre-opener rollback, saga compensation, a global clamp, and an unchecked timeout that breaks C.
- **Cheapest first test.** Enumerate S2 for `m ∈ {0, 1, 2}`: verify `T_R` unlocks `d = +1` (illegal pre-`R`), refuses `d = −1`, keeps `R`'s B-loss drop (`1/8 → 0`) and `S_ok^m` progress, and beats rollback on total A/C + B utility.
- **Old-task retention.** Measure A/C on all post-timeout `d = +1` states (including the untouched left tail), and verify the negative control (`d = −1`) is rejected before violating `C`.

#### 12. Revocation-bound late-arrival gate after timeout — P
- **Mechanism.** Bind activation of `T_R` at deadline `τ` to an explicit state/epoch token that invalidates `L`'s original swap certificate; any `L` arriving at `τ + 1` must pass a fresh post-timeout admission check or be refused, never silently unlocking the original two-order menu.
- **Novelty / control.** Lease expiry and revocation lists ([2609.00406][auditrb], [verified renewal #243][pr243]) are known; the specific learning hazard is that `T_R` consumes margin on `R`'s repaired landing, so a late `L` that looks locally valid on the untreated tail can still trigger a post-seam A violation. Compare against unrevoked late join, full recertification on every arrival, and permanent queue banning.
- **Cheapest first test.** Run S2's late-arrival fixture where `T_R` executes `d = +1` (moving `(5/4, −1/4) → (7/4, 1/4)`) and `L` arrives at `τ + 1`; verify the unrevoked arm violates `A = −1 < 0` on a second `+1`, while the revoked gate blocks it cleanly.
- **Old-task retention.** Check A/C on the refused late arrival, on a certified fresh-check late arrival, and on recurring traffic from `R`'s queue.

#### 13. Escalating timeout ladder (staged menu downgrade) — P
- **Mechanism.** Replace a single binary deadline `τ` with a certified monotone ladder `τ_1 < τ_2 < τ_3`: at `τ_1`, narrow the pending swap's allowed service class; at `τ_2`, unlock a low-risk one-sided timeout suffix while keeping a narrower late-join window open; at `τ_3`, revoke the swap completely and commit to `T_R`.
- **Novelty / control.** Staged timeouts and backoff are standard in distributed systems; the candidate CL object is a certified *monotone sequence of suffix-and-service sub-contracts* where each downgrade preserves the remaining proof without re-verifying from scratch. Compare against a single hard timeout `τ` and per-tick contingent replanning.
- **Cheapest first test.** Extend S2 with a late-but-bounded arrival at `τ_2 + 1` and a never-arriving partner past `τ_3`; compare admitted B + A/C utility against a single hard cutoff at `τ_2` or `τ_3`.
- **Old-task retention.** Verify A/C floors at every ladder transition and confirm no transition widens a previously narrowed guarantee.

#### 14. Self-discharging opener using recurring arrived-queue B or A/C traffic — P
- **Mechanism.** When `L` never arrives by `τ`, certify a lawful forward discharge sequence drawn from subsequent truthful items on `R`'s own queue or ordinary A/C batches that retires the pending swap reservation and restores steady-state A/C margins, without inventing synthetic `L` data.
- **Novelty / control.** [Margin loans (#233)][pr233] repay a pending excursion via a cycle map, and [escrowed paired leases (#214)][pr214] use successor-held batches; here an unmatched one-sided tail clip is retired using *only* ordinary arrived-queue or A/C traffic while keeping `R`'s repaired landing intact. Compare against holding `T_R`'s narrowed menu indefinitely, rollback, and synthetic partner replay.
- **Cheapest first test.** After `R` times out in S2, run `k = 4` ordinary `S_ok` A/C steps (`(−3/2)(7/8)⁴ = −7203/8192 ∈ [−1, 1]`) and verify that ordinary A/C service itself pulls the untreated left tail inside `[-1, 1]`, restoring the full `{+1, −1}` menu without `L` ever arriving.
- **Old-task retention.** Check A/C at every discharge step and verify that `R`'s right-tail B loss stays zero throughout discharge.

#### 15. No-show-priced pair selection — P
- **Mechanism.** When independently queued B pools have different arrival hazards or different one-sided timeout suffix values, score candidate reciprocal pairs `(R, L)` by their worst-case or expected A/C + B utility across *all three outcomes* (`R` then `L`, `L` then `R`, and either unmatched timeout `T_R` / `T_L`), not only two-arrival completion.
- **Novelty / control.** Stochastic scheduling and recourse planning already weight failure branches; the testable CL claim is that two reciprocal pairs tied on two-arrival B gain can have starkly different unmatched timeout menus, flipping which truthful pair should be opened. Compare against two-arrival-only `#249#01` selection stacked with post-hoc `T_R`.
- **Cheapest first test.** Build two reciprocal pairs in a 2×2 queue pool with identical two-arrival endpoints and B gains, where Pair A's `T_R` unlocks `d = +1` while Pair B's `T_R` unlocks nothing (`d = 0` only); sweep partner drop rate `p ∈ {0, 0.2, 0.5}`.
- **Old-task retention.** Report A/C floors separately on completed swaps and no-show streams, verifying no gain comes from starving the lower-arrival queue.

#### 16. Rollback leakage audit vs forward timeout — I
- **Mechanism.** Measure the true cost of checkpoint rollback against forward timeout `T_R` when non-weight serving state (optimizer slots, KV caches, running norm stats, or RNG cursors) is imperfectly reverted or expensive to snapshot, charging both discarded `R`/`w` progress and post-rollback A/C discrepancy.
- **Novelty / control.** [KV-Cache Retention Breaks Rollback Consistency (2608.15939)][kvrb] shows rollback breaks when serving state persists; this control prevents toy comparisons that treat rollback as a zero-byte, zero-side-effect undo. Compare full-state snapshot rollback, weight-only rollback (negative control), saga undo, and forward `T_R`.
- **Cheapest first test.** Run S2 with a live momentum slot updated during `R` and `S_ok`: compare weight-only rollback (leaking post-`R` momentum into the next A/C step), full-state rollback (charging snapshot bytes + lost `R`/`S_ok` progress), and forward `T_R`.
- **Old-task retention.** Measure immediate and multi-step A/C after weight-only rollback, full rollback, and `T_R`.

#### 17. Untreated-tail sentinel for post-timeout traffic — P
- **Mechanism.** Attach to `T_R` a lightweight certified guard tracking the reachable bound on the still-live untreated opposite tail under post-timeout B and A/C updates, refusing any future update that could push that hidden tail across an A/C floor before full steady state is restored.
- **Novelty / control.** Runtime safety shields / CBFs are known; the specific role here is keeping a *post-timeout* learner serving recurring traffic safely while remembering only the compact tail-bound certificate rather than the pre-opener history. Compare against freezing the model after timeout, full history replay, and unguarded post-timeout serving.
- **Cheapest first test.** After `T_R` fires in S2, feed a recurring stream of right-queue B updates and A/C batches including one batch that nudges `u − h` upward on the untouched left tail; verify the sentinel catches it while admitting benign updates.
- **Old-task retention.** Measure worst-slice A/C on the hidden untreated tail across the full post-timeout stream and charge false refusals on benign updates.

### Coupling service robustness and timeout continuations

#### 18. Joint service-and-timeout feasibility certificate — P
- **Mechanism.** Certify an allowed intervening service family `S` only if every `w ∈ S^{≤m}` simultaneously preserves (a) both swap landing tubes and opposite-tail activity if the partner arrives, *and* (b) the unmatched timeout continuations `T_R` and `T_L` if the partner never arrives.
- **Novelty / control.** Stacking `#249#07` and `#249#09` independently can admit a service step that satisfies one certificate while voiding the other (S3); the joint certificate defines the exact intersection of safe intervening service. Compare against independent `#249#07` + `#249#09` stacked, pausing service, and fresh per-step recertification.
- **Cheapest first test.** Run S3 with `S_ok`, `w_asym`, and `w_t`: verify the joint certificate admits `S_ok` (`m ≤ 2`), rejects `w_asym` (breaks `T_R` and `R → w → L`), and rejects `w_t` (vacates `L`'s repair despite keeping `T_R` safe).
- **Old-task retention.** Evaluate A/C across both completed orders and both no-show timeouts for every admitted `w`.

#### 19. Early service-driven timeout (trading a speculative swap for urgent A/C work) — P
- **Mechanism.** When an urgent ordinary A/C batch `s` lies outside the swap-closed set `S` (it would exit `Fix(L)` or vacate `L`) yet lies strictly inside `T_R`'s certified safe set, allow the learner to fire `T_R` early, revoke `L`'s swap ticket, and execute `s` immediately instead of pausing A/C until deadline `τ`.
- **Novelty / control.** Preemption and early abort are known in transaction managers; here the learner executes a *certified forward downgrade* that preserves `R` and admits `s` without rollback, using S3's separation (`w_t` is timeout-safe even though it breaks the swap). Compare against pausing `s` until `τ`, rolling back `R` to run `s`, and fixed-deadline `T_R`.
- **Cheapest first test.** Arrive `R` in S3, then deliver urgent A/C batch `w_t` before `τ`: verify early `T_R` executes `w_t` with zero A/C wait latency, revokes `L`, and keeps `d = +1` safe, whereas pausing delays `w_t` until `τ` and rollback discards `R`.
- **Old-task retention.** Measure A/C latency, worst-slice A/C after `w_t` and `d = +1`, and safe refusal if `L` arrives after early revocation.

#### 20. Service-paid timeout upgrade (intervening A/C work widens the unmatched menu) — P
- **Mechanism.** Certify when a bounded run of ordinary A/C service steps executed during the wait shrinks the still-live untreated opposite tail enough to *enlarge* `T_R`'s post-timeout safe suffix menu (or shorten the remaining discharge horizon), so normal A/C traffic during the wait pays down no-show risk even if `L` never arrives.
- **Novelty / control.** [Loan commits (#241#16)][pr241] uses required old work to carry a handoff; here required A/C service during an open swap *upgrades* the timeout continuation while still keeping the swap live for `m ≤ 3`. Compare against fixed pre-wait `T_R` menus, pausing service, and synthetic tail replay at equal compute.
- **Cheapest first test.** In S2, track `min A(d = +1)` (`0 → 5/32 → 75/256`) and `min C(d = −1)` (`−1/2 → −5/16 → −19/128 → +...`) across `m = 0..4` steps of `S_ok`, testing whether a smaller residual `d = −3/4` (illegal at `m = 0` with `C = −1/4`) becomes certified at `m = 2` (`C = 13/128`) while `L` still swaps cleanly.
- **Old-task retention.** Check A/C on every newly unlocked timeout suffix and confirm no suffix is unlocked before its exact envelope bound crosses zero.

#### 21. Unified slack ledger across intervening service and timeout margin — P
- **Mechanism.** Maintain one non-double-counted slack budget shared between the `m` intervening A/C steps and `T_R`'s post-timeout residual margin: each slack-consuming A/C step automatically tightens either the remaining swap deadline `τ` or the post-timeout residual cap so service and timeout never overspend the same A/C margin.
- **Novelty / control.** Resource accounting and [self-depleting supply (#220)][pr220] avoid double-billing; here the ledger couples live service execution directly to the unmatched-opener fallback contract. Compare against static split budgets (half for service, half for timeout) and uncoupled certificates that can double-spend margin.
- **Cheapest first test.** Construct a stream where `R` has total A-margin `1` to split between service drift and post-timeout residual `d`: verify the unified ledger lets a quiet wait spend full `d = +1` on timeout while a busy wait (`+1/4` drift) caps timeout at `d = +3/4` and blocks `d = +1`.
- **Old-task retention.** Confirm zero A/C violations across all valid splits and explicitly test the double-spent static-timeout failure as a negative control.

#### 22. Multi-seam renewal across alternating swaps and timeouts — P
- **Mechanism.** Certify that both a completed service-closed swap `(R, w, L)` and a discharged timeout continuation `(R, w, T_R)` land inside a declared renewable core `K_next` from which the next independent B-queue pair `(R', L')` can be opened without full recertification or checkpoint accumulation.
- **Novelty / control.** [Verified renewal (#243)][pr243] and [adaptive renewal (#236)][pr236] study multi-round return to a ready interface; the testable delta here is whether one-sided tail clips plus ordinary A/C service can close a *multi-seam loop* across mixed swap and no-show rounds under an unchanged optimizer. Compare against per-round full recertification, periodic checkpoint resets, and fixed global clamps.
- **Cheapest first test.** Run a 4-round CPU sequence alternating `(R, S_ok^2, L)`, `(L, S_ok^1, T_L + discharge)`, `(R', S_ok^2, L')`, and a late-arrival refusal on S1/S2; track envelope drift, per-queue B progress, and verifier checks against fresh per-round recertification.
- **Old-task retention.** Measure worst-slice A/C after every round and verify that cumulative drift across rounds does not silently erode `K_next`.

## Ranked deeper questions

1. **Can ordinary stateful A/C service preserve a paired swap without pausing or per-step rechecking?** Start with cards 01, 04, and 06. Freeze full proof state (including momentum/Adam slots, running stats, and clocks) and compare against pausing A/C service, fresh per-step rechecking, and a fixed clamp on S1a/S1b plus a tiny shared-weight ReLU host. If optimizer slots or clocks break exact identity on every real A/C batch, publish the counterexample rather than claiming weight-only closure.
2. **Does a certified forward timeout continuation beat pre-opener rollback and saga compensation at equal A/C retention?** Start with cards 11, 12, and 16. Require a setting (like S2) where the first opener unlocks real one-sided utility and intervening A/C service has real value, and measure rollback's full cost including non-weight serving state (`2608.15939`). If rollback plus a small replay buffer ties `T_R` at equal bytes and A/C floors, prefer rollback.
3. **Does joint service-and-timeout certification beat stacking the two mechanisms independently?** Start with cards 18, 19, and 21. Isolate S3-like regimes where ordinary A/C batches satisfy one obligation while breaking the other, and test whether early service-driven timeout (card 19) or unified slack accounting (card 21) yields a strict Pareto gain in A/C latency and safe admissions over the best independent stack.
4. **Can mixed swap and timeout rounds renew cleanly across multiple seams under an unchanged optimizer?** Start with cards 08, 14, and 22. Run multi-round streams with partner no-shows, late arrivals, and mid-wait service drift; test whether self-discharge and partner rebinding maintain a bounded renewable core at lower total verification cost than fresh per-round recertification.

**Verdict:** Conditional primitive candidate, not a pilot nomination. A service-robust swap with an explicit timeout continuation counts as a new CL primitive only if an unchanged optimizer supports truthful shared-state openers whose existing A/C proof survives bounded stateful A/C service *and* degrades forward on partner no-show at lower total cost (A/C latency, verifier work, and retained B gain) than pausing service, per-step rechecking, or full-state rollback. Otherwise keep the S1b/S2/S3 counterexamples and prefer a single opener or clamp with explicit pause/rollback and ordinary recertification.

[rg]: https://arxiv.org/abs/2607.17536
[memtx]: https://arxiv.org/abs/2607.23929
[chronomem]: https://arxiv.org/abs/2607.27773
[auditrb]: https://arxiv.org/abs/2609.00406
[kvrb]: https://arxiv.org/abs/2608.15939
[sagas]: https://doi.org/10.1145/38713.38742
[pr214]: https://github.com/manojbajaj95/cl/pull/214
[pr233]: https://github.com/manojbajaj95/cl/pull/233
[pr234]: https://github.com/manojbajaj95/cl/pull/234
[pr235]: https://github.com/manojbajaj95/cl/pull/235
[pr238]: https://github.com/manojbajaj95/cl/pull/238
[pr241]: https://github.com/manojbajaj95/cl/pull/241
[pr243]: https://github.com/manojbajaj95/cl/pull/243
[pr220]: https://github.com/manojbajaj95/cl/pull/220
[pr236]: https://github.com/manojbajaj95/cl/pull/236
