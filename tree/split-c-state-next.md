# Split C state (next): selective continuation momentum and region-opening payments

**Status:** Ideas only; two exact paper fixtures and proposed CPU first tests, no training or GPU. **Parent:** [Split C state](split-c-state.md) ([PR #278][parent]). **Review seeds:** [Flood triage row 396][triage] scores #278 cards 05 and 13 at 3. Give the receiving lane its own residual momentum only in directions that affect post-cut C service, rederiving the rest from the allowed surviving clock and inputs rather than the old optimizer. Train a C response whose ordinary update opens a reader-neutral region from which partner P's later *real* ordinary update can pay the complement. Cards 01 and 09 restate those seeds as baseline controls.

**Ledger read first:** The [idea ledger][ledger] rejects exact restore and true-by-construction claims, requires every first test to check old-task retention, and requires beating the strongest equal-budget stack of simple controls. **P** marks a candidate primitive (a reusable object or operation); **I** marks an improvement or audit, not a pilot candidate. These are proposer labels, not reviewer verdicts.

## What would count

- **Continuation state split by lawful rederivability, not just parameter sparsity.** A and C are ordinary old tasks; B is the incoming task. The receiving third lane keeps its own old workload. Partition the recipient's pre-cut optimizer state into copied residual directions `M_copy` (needed for post-cut C continuation and not reconstructible after primary loss) and rederived directions `M_rederive` (reconstructed solely from the permitted surviving clock, public surviving inputs, and surviving shared state `S`, never from the retired lane's optimizer). Charge all metadata, basis indices, clock state, verification residuals, and rederivation compute alongside copied floats. Include the mandatory failure mode: a pre-cut private perturbation on a direction assumed to be rederivable.
- **Region opening verified on the real adaptive successor, never on a simulated P.** Q's first update must be a genuine, deadline-bound C response with its original target and update rule. It opens a reader-neutral region only if executing P's *actual* later ordinary update (with P's real optimizer state, step rule, and lawful target) delivers the required complement inside every intermediate reader band, whereas executing P without Q's opening (or with a closing C target) fails. Never credit a simulated, linearized, or hypothetical P update; never add a rescue batch or alter C's target.
- **Equal-budget stacked controls on the same frontier.** Freeze representation, placement, rederivation map, and opening contracts before blind faults and requests. Stack [#267][standby]#07 representation split without optimizer state, full optimizer-state copy, slot reset at handover, [#239][folds] smallest post-hoc state, `#267#19` fixed two-payer split, [#256][working]#13 split with no opening, equal-compute rescue batches, and exact scheduling on tiny domains. Match resident/peak bytes, update work, and occupied slots (or report the full Pareto frontier with refusals and missed C/B kept in the denominator).

**Nearest work (targeted alphaXiv check; not exhaustive):** [Backpropagated Output Momentum (BOM)][bom] relocates optimizer momentum from parameters to task space, and [QAM][qam] studies checkpoint state under shifted schedules; neither partitions optimizer state by what survives a physical handover cut versus what is lawfully rederivable from a surviving clock and public inputs. [Delayed Optimizer-State Transport][transport] and [Subliminal Trait Transfer][subliminal] show that carried optimizer moments causally shape short-horizon updates, and [ORACLE][oracle] enforces constraints *after* optimizer preconditioning rather than on raw gradients; those establish why adaptive execution matters, not how to split and rederive handover momentum or open a successor's safe region. [RASP][rasp], [Recyclable Unit Gating][gating], and [Update Admission Auditing][admission] study sparse plasticity, unit gating, and admission in continual learning, but do not use a deadline-bound transferred C response to open a reader-neutral corridor for a second partner's real complement payment.

## Exact paper fixtures, not novelty claims

**M · One copied momentum coordinate, one lawfully rederived coordinate.** Let C's residual parameter be `r = (r_1, r_2)` updated by momentum SGD (`beta = 1/2`, `lr = 1`), reaching `r = (0, 0)` at the cut with surviving shared state `s = 1/2`. Two pre-cut histories differ in private momentum `m_1 in {+1/2, -1/2}` (from a retired private C source), while `m_2 = +1/4` came solely from a surviving public input `x_pub` at the surviving clock tick `t` and is rederivable from `(s, x_pub, t)`. After the cut, a pinned C update has gradient `g = (1/2, 1/2)`. Copying `m_1` and rederiving `m_2` gives `m'_1 in {3/4, 1/4}`, `r'_1 in {-3/4, -1/4}`, and `m'_2 = 5/8`, `r'_2 = -5/8` — matching full 2-scalar copy with 1 copied scalar. A slot reset (`m = (0, 0)`) gives `r' = (-1/2, -1/2)`, failing both histories and both coordinates. Rederivation-error negative: if a hidden private pre-cut event instead left true `m_2 = -1/4`, lawful rederivation still produces `m_2 = +1/4` and lands at `r'_2 = -5/8` instead of `-3/8` (error `1/4`), which must be caught or refused. This fixture checks semantics only; a hand-placed split ties it.

**G · One ordinary C response opens a reader-neutral gate for P's real complement.** Start with old-reader drifts `(1/4, 1/4, 0)` inside the safe box `[-1/4, 1/4]^3`, gate parameter `g = -1`, and partner parameter `p = 0`. Readers observe `y_1 = p`, `y_2 = p`, and `y_3 = 2 * ReLU(-g) * p`. B's required final step adds `(1/4, 1/4, 0)`. P's ordinary lawful update moves `p` by `Delta p = -1/4`. If P runs while `g = -1` (`ReLU(1) = 1`), Reader 3 suffers `Delta y_3 = -1/2`, violating `[-1/4, 1/4]` immediately; no static two-payer split of `p` works. Instead, Q runs first and serves its truthful C correction `t = +1` via one unit-rate SGD step on `(g - t)^2 / 2`, moving `g` to `+1` (`ReLU(-1) = 0`). Because `p = 0`, Q's step is reader-neutral (`Delta y = (0, 0, 0)`, drift stays `(1/4, 1/4, 0)`) while closing Reader 3's sensitivity to `p`. P's real ordinary update `Delta p = -1/4` then yields `Delta y = (-1/4, -1/4, 0)`, bringing drift to `(0, 0, 0)`, and B's step lands at `(1/4, 1/4, 0)`. Closing negative: if Q's truthful target is `t = -2`, Q moves `g` to `-2` (`ReLU(2) = 2`), so P would hit Reader 3 by `-1` and B must be refused. Simulated-P negative: crediting P without running P's real update leaves drift at `(1/4, 1/4, 0)`, so B pushes Readers 1 and 2 to `1/2`.

## Idea cards

### Selective continuation momentum and lawful rederivation

#### 01. Copy only post-cut-relevant residual momentum; rederive the rest (P, #278#05 seed)
- **Mechanism:** Give the receiving lane its own residual momentum only in directions that change post-cut C service; reconstruct the remaining directions solely from the permitted surviving clock, public inputs, and `S`, never from the retired optimizer.
- **Novelty vs nearest prior art:** [PR #278][parent] card 05 introduces the split; [PR #239][folds] finds minimal continuation slots post hoc. The candidate primitive is a pre-cut continuation split partitioned by physical survivability and lawful rederivability.
- **Cheapest first test:** Execute fixture M and a 4D linear momentum-SGD stream; compare `#267#07` representation split without optimizer state, full optimizer-state copy, slot reset, `#239` post-hoc minimal slot, and an injected private perturbation on a rederived direction.
- **Old-task retention check:** Score A, pinned C, unseen post-cut C after two real updates, B utility, and the receiver's untransferred old workload.

#### 02. Train C so pre-cut momentum aligns with rederivable public directions (P)
- **Mechanism:** During preparation, regularize C's residual parameterization so gradient history from routine pre-cut C traffic lies in the span reconstructible from surviving public inputs and clock, shrinking the non-rederivable subspace `M_copy` before any fault occurs.
- **Novelty vs nearest prior art:** `#239` compresses whatever optimizer state training happened to leave behind; [BOM][bom] stores full task-space history. The candidate operation actively *shapes* training dynamics to minimize non-rederivable momentum rank at fixed C accuracy.
- **Cheapest first test:** Compare an unregularized 8D MLP with `#239` post-hoc slot extraction against a rederivability-regularized twin under a 2-scalar copy cap, plus full-state copy and slot reset. Include a shift where pre-cut private traffic cannot align with public features.
- **Old-task retention check:** Measure A, pinned v1/v2 C, unseen C after two post-cut updates, B finish, and receiver old tasks; verify regularization does not slow pre-cut C learning.

#### 03. Carry a task-space reconstruction seed instead of parameter-space momentum (P)
- **Mechanism:** Store a tiny signed residual in surviving public input/output coordinates (rather than parameter coordinates) and backpropagate it through the receiver's local weights and surviving clock at handover to synthesize `M_copy`, allowing different receiver parameterizations to inherit the same continuation state.
- **Novelty vs nearest prior art:** [BOM][bom] relocates full momentum to task space for general optimization. The candidate object is a *minimal differential witness* carrying only the non-rederivable private delta across a cross-lane handover cut.
- **Cheapest first test:** Hand over between two differently rotated 4D linear receivers on fixture M variants; compare parameter-space partial copy, full BOM history, slot reset, and a 1-scalar task-space seed. Test a non-invertible Jacobian where task-space backprop loses a needed nullspace direction.
- **Old-task retention check:** Evaluate A, pinned C, two post-cut C updates on the rotated receiver, and the receiver's own old tasks; charge seed bytes and backprop FLOPs.

#### 04. Split continuation moments by sensitivity to handover clock skew (P)
- **Mechanism:** When the handover clock can slip by up to `delta_t` ticks, separate residual momentum into clock-sensitive directions (rederived from the actual observed surviving clock) and delay-invariant directions (copied directly with a bounded-jitter decay contract).
- **Novelty vs nearest prior art:** [QAM][qam] handles schedule-shifted checkpoints globally; standard momentum assumes exact step counts. The candidate primitive is a skew-typed optimizer split that stays valid under bounded handover arrival jitter without storing per-tick checkpoints.
- **Cheapest first test:** Inject `delta_t in {0, 1, 2}` tick delays on a 2-timescale momentum stream (`beta_1 = 0.5, beta_2 = 0.9`); compare fixed-clock rederivation, full copy, slot reset, and skew-typed copy. Include a jitter larger than the declared `delta_t`.
- **Old-task retention check:** Score A, deadline-pinned C under every legal `delta_t`, unseen C after two updates, B finish, and refusal accuracy when jitter exceeds `delta_t`.

#### 05. Attach a self-verifying tripwire for broken momentum rederivation (P)
- **Mechanism:** Pair the rederived momentum `M_rederive` with a 1-scalar public consistency invariant predicted for the first post-cut C gradient; if a hidden pre-cut private perturbation invalidated rederivation, the first-step mismatch trips before write commit and forces scoped refusal or fallback.
- **Novelty vs nearest prior art:** [Update Admission Auditing][admission] audits policy updates after evaluation; checkpoint checksums verify stored bytes, not *omitted* private history. The candidate operation detects silent rederivation invalidity using only the first ordinary post-cut gradient.
- **Cheapest first test:** Run fixture M's hidden-perturbation negative and a 6D nonlinear stream; compare unchecked rederivation, full copy, slot reset, and tripwire-guarded rederivation. Include a crafted perturbation orthogonal to the first post-cut gradient (missed-alarm negative).
- **Old-task retention check:** Track false refusals on clean handovers, silent A/C violations on corrupted handovers, pinned C deadlines, and receiver old workload.

#### 06. Rederive adaptive second moments from public norms; copy only sign-critical first moments (P)
- **Mechanism:** Under Adam/RMSProp, reconstruct the coordinate/block curvature denominator `v` from surviving public gradient norms and clock, copying only the residual first-moment coordinates `m` where pre-cut private events can flip the post-cut update sign.
- **Novelty vs nearest prior art:** Adafactor and `#264` share or factor `v` across shards; `#251#03` ties `v` at birth. The candidate split reconstructs `v` *without copying it* while reserving replica bytes strictly for sign-flipping private `m` directions.
- **Cheapest first test:** Run a 4D Adam handover where two histories share weights and public gradient magnitudes but have opposite private `m_1`; compare full `(m, v)` copy, `v`-reset, Adafactor-style factored `(m, v)` at equal bytes, and public-`v` + sign-`m` copy. Include a private gradient spike that invalidates public `v`.
- **Old-task retention check:** Verify A, pinned C, unseen C over three Adam steps, B utility, and receiver old work; log any step-size overshoot from `v` misestimation.

#### 07. Horizon-truncate copied momentum to the declared handover window (P)
- **Mechanism:** Compute the exact decay horizon `H` of the B/C handover overlap and copy only private momentum components whose `beta^k`-weighted influence exceeds the post-cut service tolerance within `k <= H`, dropping fast-decaying modes that wash out before any sensitive C read.
- **Novelty vs nearest prior art:** Low-rank and magnitude-based optimizer pruning ignore when each mode is actually read. The candidate rule prices copied momentum bits by *deadline-weighted post-cut impact* over a finite cut window `H`.
- **Cheapest first test:** Construct a 6D stream with mixed decay rates and C reads at ticks `k in {1, 2, 4}`; compare magnitude pruning, `#239` post-hoc slot, full copy, and horizon-weighted copy at equal bytes. Include a fast-decaying mode read immediately at `k = 1`.
- **Old-task retention check:** Score A, every C read across `k = 1..H`, held-out C after `H`, B utility, and receiver old workload.

#### 08. Audit the rederivation-error versus copy-byte frontier (I)
- **Mechanism:** Sweep the fraction of copied vs rederived momentum coordinates across varying levels of private pre-cut traffic and clock noise, plotting exact post-cut C continuation error against equal-byte quantized/low-rank full copies and slot resets.
- **Novelty vs nearest prior art:** Diagnostic audit rather than a new primitive; determines whether lawful rederivation actually beats equal-byte lossy compression of the full optimizer state when private traffic is non-negligible.
- **Cheapest first test:** Sweep private-to-public gradient ratio from `0` to `1` on a 16D quadratic and small ReLU host; compare rederivation + selective copy, 2–4 bit quantized full copy, rank-`r` SVD copy, and slot reset at matched bytes.
- **Old-task retention check:** Report A/C retention, pinned deadline hit rate, B completion, and silent-error rate at every point on the byte curve.

### Region-opening first payments and real-successor complements

#### 09. Open a reader-neutral region with Q's ordinary response for P's real update (P, #278#13 seed)
- **Mechanism:** Train Q so serving its pending truthful C correction via its ordinary update moves the host into a reader-neutral region from which P's later *real* ordinary update can safely pay the remaining complement; credit P only when P actually executes.
- **Novelty vs nearest prior art:** `#267#19` and `#256#13` use static two-payer splits with fixed reader sensitivities. The candidate operation uses a real C update to alter the *admissible effect set* of a subsequent real partner update.
- **Cheapest first test:** Execute fixture G and a learned 2-unit ReLU host; compare `#267#19` fixed split, `#256#13` split without opening, equal-compute rescue batch, crediting a simulated P update, and fixture G's closing target `t = -2`.
- **Old-task retention check:** Check Readers 1–3 at every prefix (`Q`, `P`, `B`), held-out A/C, Q and P's own old tasks, and safe refusal on `t = -2`.

#### 10. Simultaneous dual-gate clearance: mute a fragile reader while activating a payment channel (P)
- **Mechanism:** Train Q's single ordinary C response to cross a piecewise-linear boundary that simultaneously decouples a fragile old reader from P's writable block and couples an endangered reader to it, turning P's ordinary update from harmful to net-reparative in one step.
- **Novelty vs nearest prior art:** [RASP][rasp] and [Recyclable Unit Gating][gating] gate plasticity via auxiliary masks or dedicated gates. Here the gate flip is paid for entirely by a *truthful, deadline-bound C correction* with no extra mask write or slot.
- **Cheapest first test:** Extend fixture G so Reader 2 also starts decoupled (`ReLU(g) * p`) while Reader 3 starts coupled (`2 * ReLU(-g) * p`); compare static splits, separate mask-update + P at equal compute, and trained single-response dual clearance. Include a host where no single truthful target flips both gates.
- **Old-task retention check:** Score all three readers at every prefix, unseen C inputs straddling the gate boundary, B utility, and both partners' old workloads.

#### 11. Open a region that is neutral under P's real adaptive step rule (P)
- **Mechanism:** Following [ORACLE][oracle], define the reader-neutral region in *post-optimizer update space* (incorporating P's live momentum and adaptive denominator), and train Q's ordinary response to open a corridor that stays safe after P's actual preconditioned step rather than P's raw gradient.
- **Novelty vs nearest prior art:** [ORACLE][oracle] projects or aligns constrained updates post-optimizer at runtime. The candidate operation has an *earlier* ordinary partner update reshape the nonlinear host so a later unconstrained adaptive update lands inside the post-optimizer safe set.
- **Cheapest first test:** Run fixture G with Adam/momentum on P where P's carried momentum rotates P's step away from its raw gradient; compare raw-gradient opening, ORACLE runtime projection on P, equal-compute rescue, and adaptive-aware opening. Include an out-of-family P moment that breaks the corridor.
- **Old-task retention check:** Execute the real adaptive `Q -> P -> B` suffix, verify all intermediate reader prefixes, held-out A/C, and P/Q routine tasks.

#### 12. Fan-out opening: one C response unlocks a safe corridor for multiple candidate payers (P)
- **Mechanism:** When it is unknown which partner (`P_1` or `P_2`) will have a lawful request ready before B's deadline, train Q's single ordinary C response to open a shared reader-neutral intersection usable by whichever partner's real ordinary update arrives first, crediting only the executed one.
- **Novelty vs nearest prior art:** Contingent scheduling chooses among already-feasible partners; `#275#13` opens across hidden aliases of one edit. The candidate operation opens a single nonlinear corridor for *heterogeneous* real partner updates without extra slots or double-crediting.
- **Cheapest first test:** Pair Q with two partners `P_1, P_2` whose updates threaten different fragile readers (`R_3, R_4`); compare single-partner opening, dedicated reserve per partner, contingent scheduling without opening, and fan-out opening. Include two partners whose required corridors are disjoint.
- **Old-task retention check:** Test `P_1`-only, `P_2`-only, and neither-arrives branches across all four readers, A/C retention, and B refusal when neither arrives.

#### 13. Self-closing neutral regions: P's real payment automatically re-shields the corridor (P)
- **Mechanism:** Design the opened region so that P's real complement payment not only cancels the endangered reader's drift but also moves the shared gate back across the boundary (re-isolating the fragile reader) before subsequent unrelated writes arrive.
- **Novelty vs nearest prior art:** `#275#15` / `#284#13` rely on time-based gate decay to close a temporary learning window. Here the *act of paying* closes the corridor deterministically on completion, tying re-shielding to real execution rather than a clock.
- **Cheapest first test:** Add a post-B unrelated write `W` on `p` to fixture G; compare permanently open regions, time-decay windows, explicit re-lock step at equal compute, and self-closing `Q -> P` pairs. Include a late P where `W` arrives before P closes the gate.
- **Old-task retention check:** Score Readers 1–3 through `Q -> P -> B -> W`, unseen C inputs near the re-closed boundary, and both partners' old tasks.

#### 14. Opening-preserving safe abort when P never arrives or fails (P)
- **Mechanism:** Require Q's region-opening C response to lie inside an unconditional old-task invariant set even if P's slot is revoked, P's real target has the wrong sign, or B is refused—so committing Q's real C response never leaves behind an exposed fragile reader.
- **Novelty vs nearest prior art:** Transactional rollback undoes Q's write (violating Q's C deadline). The candidate contract guarantees forward-only safety: Q's committed opening is strictly benign as a standalone state, never a half-finished debt.
- **Cheapest first test:** Revoke P's slot after Q commits on a 2-unit ReLU host followed by three routine A/C updates; compare rollback-plus-requeue, unguarded opening, static split, and abort-safe opening. Include a host where every opening exposes a fragile reader to routine post-abort traffic.
- **Old-task retention check:** Deliver Q's pinned C response on deadline, refuse B cleanly, and verify zero degradation on A, C, and receiver old tasks over the post-abort suffix.

#### 15. Two-hop chained openings for high-codimension reader conflicts (P)
- **Mechanism:** When a single due C response cannot simultaneously clear two conflicting fragile readers, train an ordered pair of lawful due C responses `Q_1 -> Q_2` where `Q_1` opens a neutral region for `Q_2`'s ordinary update and `Q_2` opens the complement region for P's real update.
- **Novelty vs nearest prior art:** Multi-step curriculum/bridging uses synthetic helper batches. The candidate primitive chains *exclusively owed, deadline-bound C corrections* into a multi-hop safe-set expansion with every intermediate prefix certified.
- **Cheapest first test:** Construct a 3-gate ReLU host with two fragile readers where no single C target clears both; compare single-hop opening, static 3-payer split, equal-compute synthetic bridge, and chained `Q_1 -> Q_2 -> P`. Test reversed arrival order `Q_2 -> Q_1` as a mandatory negative.
- **Old-task retention check:** Check every reader at all four prefixes (`Q_1`, `Q_2`, `P`, `B`), pinned C deadlines for both `Q_1` and `Q_2`, and B refusal on reversed order.

#### 16. Audit the simulated-P versus real-P credit gap (I)
- **Mechanism:** Measure how often a scheduler that credits a linearized or one-step simulated P update inside Q's opened region violates an old reader when P's actual nonlinear, momentum-carrying update executes, separating curvature error from optimizer-carry error.
- **Novelty vs nearest prior art:** Diagnostic audit (required by [flood triage row 396][triage]'s "crediting a simulated P update" control); establishes when real-P verification is strictly necessary rather than replaceable by cheap linearized lookahead.
- **Cheapest first test:** Run 50 random 2-layer ReLU handovers comparing linearized-P credit, frozen-momentum simulated-P credit, and full real-P execution; record false-safe admission rates and worst-prefix reader violations.
- **Old-task retention check:** Report true A/C prefix violations, missed B finishes from over-conservative simulation, and receiver old-task accuracy across all three estimators.

### Coupling rederived continuation state with region-opening payments

#### 17. Momentum-propelled region opening: copy only the gate-crossing momentum direction (P)
- **Mechanism:** When Q's truthful single-step C gradient is too small to push `g` across the opening boundary on its own, copy only the single gate-aligned residual momentum coordinate (`M_copy`) while rederiving all non-gate directions (`M_rederive`), so Q's ordinary response crosses into the reader-neutral region for P at minimal replica cost.
- **Novelty vs nearest prior art:** Neither `#278#05` (continuation momentum) nor `#278#13` (region opening) alone handles a truthful C target whose raw gradient falls short of the gate threshold. The candidate primitive couples selective momentum retention directly to boundary-crossing feasibility.
- **Cheapest first test:** Combine fixtures M and G with `lr = 1/2` so Q's truthful target `t = +1` moves `g` only halfway without carried momentum `m_g > 0`, crossing only when `m_g` is copied; compare slot reset, `#267#07` no-momentum split, full optimizer copy, and 1-coordinate gate-momentum copy. Include a negative where carried momentum has the wrong sign.
- **Old-task retention check:** Verify Q's C accuracy, all three reader prefixes across `Q -> P -> B`, unseen post-cut C updates, and receiver old workload.

#### 18. Size Q's opened region to absorb P's bounded momentum-rederivation error (P)
- **Mechanism:** When P's optimizer state is partially rederived rather than fully copied, P's actual complement step carries a bounded angular/norm uncertainty ball `E_rederive`; train Q's ordinary response to open a reader-neutral corridor wide enough to contain P's entire `E_rederive`-perturbed update, trading opening margin for copied momentum bytes.
- **Novelty vs nearest prior art:** Robust control uses fixed uncertainty sets; `#278#05` treats rederivation error purely as a C-continuation cost. The candidate interface turns *opening width* into a direct substitute for *copied optimizer bytes* on the partner lane.
- **Cheapest first test:** Inject bounded rederivation error `eps` on P's momentum in a 2D extension of fixture G; compare narrow opening + full P momentum copy, wide opening + rederived P momentum at matched total bytes, and narrow opening + rederived P (expected violation). Include an `eps` exceeding the maximum reachable opening width.
- **Old-task retention check:** Score A/C at every prefix across worst-case `eps`, P and Q's old tasks, B completion, and peak replica bytes.

#### 19. Use Q's region-opening boundary crossing to prune copied continuation momentum (P)
- **Mechanism:** Crossing a ReLU/gating boundary during Q's ordinary response can zero out downstream sensitivity to specific pre-cut private momentum coordinates; exploit that known post-opening nulling to drop those coordinates from `M_copy` at the cut, shrinking the copied optimizer state below `#239`'s static post-hoc minimum.
- **Novelty vs nearest prior art:** `#239` computes the smallest sufficient optimizer slot assuming a fixed post-cut Jacobian/continuation regime. Here Q's *region-opening update itself* collapses an equivalence class of pre-cut moments, strictly reducing required replica bytes.
- **Cheapest first test:** Construct a 3D ReLU host where private momentum `m_3` affects post-cut C *unless* Q's first update closes gate 3; compare `#239` static minimal slot (copies `m_1, m_3`), full copy, slot reset, and opening-pruned copy (copies `m_1` only). Test a closing negative where Q fails to cross gate 3.
- **Old-task retention check:** Execute two post-cut C updates, P's complement, B's finish, A retention, and receiver old tasks; verify exact continuation equivalence on the pruned coordinate.

#### 20. Joint continuation-and-opening minimal replica (P)
- **Mechanism:** Learn a single minimal replica code over pre-cut optimizer states that merges two histories iff they yield both identical post-cut C service *and* identical opening/complement feasibility for P's real update, preventing marginal compression from erasing a tiny momentum component that flips P's opening gate.
- **Novelty vs nearest prior art:** `#278#19` learns a joint state replica for C answers and static signed effects; `#239#02` minimizes continuation state for C alone. The candidate quotient tracks *optimizer-state equivalence* jointly across C continuation and nonlinear region-opening transitions.
- **Cheapest first test:** Enumerate 2-bit momentum histories where C-only continuation merges two states that land on opposite sides of fixture G's gate `g = 0`; compare C-only `#239` slot, opening-only copy, two separate codes at equal bytes, and the joint minimal replica.
- **Old-task retention check:** Run both separated histories through `Q -> P -> B`, verifying A/C at every prefix, unseen post-cut C, and total replica bytes.

#### 21. Momentum-damped gate protection against closing C targets (P)
- **Mechanism:** Train the copied residual momentum direction `M_copy` so that when a lawful but wrong-sign C correction arrives (the closing negative `t = -2`), carried momentum cushions the gate motion enough to keep the host inside a recoverable or abort-safe band without falsifying Q's C answer, cleanly refusing B rather than corrupting old readers.
- **Novelty vs nearest prior art:** Gradient clipping caps all updates uniformly and degrades truthful C corrections. The candidate mechanism uses *directional* continuation momentum to create asymmetric resistance against gate closure while keeping opening moves fast.
- **Cheapest first test:** Run fixture G with both `t = +1` (opening) and `t = -2` (closing) targets under a shared copied `m_g > 0`; compare uniform gradient clipping, slot reset, full copy without asymmetric shaping, and momentum-damped gate protection. Include a repeated closing burst that overcomes carried momentum.
- **Old-task retention check:** Deliver Q's truthful C answer in both arms, refuse B cleanly on `t = -2`, and verify zero A/C violations on the post-refusal suffix.

#### 22. Interaction falsifier: decoupled split-momentum + opening stack versus coupled design (I)
- **Mechanism:** Run a 2×2 factorial crossing selective momentum copy/rederivation (Seed A) with region-opening first payments (Seed B) against their best decoupled stack given identical replica bytes, compute, and exact scheduling; drop every coupling claim (17–21) if the decoupled stack matches the coupled feasible handover set.
- **Novelty vs nearest prior art:** Required interaction audit from the [idea ledger][ledger] ("merge cards must beat the union of their parts' baselines"); tests whether coupling continuation momentum with region opening creates genuinely new feasible handovers rather than accounting reshuffling.
- **Cheapest first test:** Combine fixtures M and G in a 4-unit ReLU MLP under tight byte and slot caps; compare Seed A alone, Seed B alone, their equal-budget decoupled stack with exact search, and the coupled design across clean, hidden-perturbation, and closing-target stress suites.
- **Old-task retention check:** Report per-version C service, all intermediate A/C reader prefixes, unseen post-cut C, receiver old workload, B completion, and refusal/silent-error rates in one denominator.

## Ranked deeper questions

1. **Can one ordinary transferred C response open a reader-neutral region that makes P's *real* adaptive update a necessary complement payment, beating static two-payer splits (`#267#19`, `#256#13`) and equal-compute rescues?** Start with 09, 10, 11, and 16. Test on fixture G and a 2-layer ReLU host with momentum/Adam on P; compare against simulated-P credit and ORACLE runtime projection. Drop the primitive claim if static splits, runtime projection, or equal-compute rescues match the feasible set at equal A/C retention.
2. **Does pre-cut rederivability training plus selective momentum copying beat equal-byte optimizer compression and `#239` post-hoc minimal slots when private pre-cut traffic is non-zero?** Start with 01, 02, 05, and 08. Sweep the private-to-public gradient ratio and inject hidden pre-cut perturbations on rederived directions; require both lower post-cut continuation error than equal-byte quantized/low-rank copies and reliable tripwire detection before commit.
3. **Does coupling selective continuation momentum with region-opening payments strictly expand the feasible handover frontier over stacking both mechanisms independently?** Start with 17, 18, 19, and 22. Isolate whether momentum-propelled opening (17), rederivation-error absorption (18), or opening-pruned momentum (19) solves byte- and slot-constrained handovers that the equal-budget decoupled stack with exact scheduling cannot.
4. **Can opened regions and rederived continuation states fail forward-safely under blind faults—revoked P, wrong-sign closing targets, clock skew, and hidden private perturbations?** Start with 04, 05, 13, 14, and 21. Measure silent A/C violations and missed C deadlines in the full refusal denominator; if forward-only safety requires rollback or extra reserve slots, downgrade to the single-fault regime.

[parent]: https://github.com/manojbajaj95/cl/pull/278
[triage]: https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/flood-triage.md#L396
[ledger]: https://github.com/manojbajaj95/cl/blob/f2fe7c5bad6528041fbcfb2340929cc9ef64bba0/reviews/idea-ledger.md
[standby]: https://github.com/manojbajaj95/cl/pull/267
[working]: https://github.com/manojbajaj95/cl/pull/256
[folds]: https://github.com/manojbajaj95/cl/pull/239
[bom]: https://www.alphaxiv.org/abs/2609.36738
[transport]: https://www.alphaxiv.org/abs/2608.24593
[subliminal]: https://www.alphaxiv.org/abs/2608.20442
[oracle]: https://www.alphaxiv.org/abs/2610.09040
[qam]: https://www.alphaxiv.org/abs/2609.35168
[rasp]: https://www.alphaxiv.org/abs/2611.03513
[gating]: https://www.alphaxiv.org/abs/2609.38356
[admission]: https://www.alphaxiv.org/abs/2609.10873
