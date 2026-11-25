# Return-to-ready parks: co-training a public maintenance park and its recovery basin

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Glued reply fragments](glued-fragments.md) ([PR #224][parent]), card 17 (pre-trained maintenance-mode park) and card 11 (universal park–edit–clear). **Review seed:** [Flood triage, row 357][triage] gives round-54 merge **MRS2** ([`ideas/flood/cross-pool-54.md`][cross54]) score 3: make the maintenance park a genuine return-to-ready state by using ordinary successor work to maintain a public park that retains every installed task (`A`, prior `Bᵢ`, prior `C`) and still admits real pairs when recovery is interrupted, co-training the park's safe edit region and recovery basin together — joining [#236#10][adaptive] (teach the recovery basin), [#237#15][seam] (train the same park across reachable old update orders), and [#224#17][parent] (pre-train a maintenance-mode park), together with MRS2's supporting parts (`#235#08` redundant finishes, `#236#02` relearnable interface, `#237#11/#12` trained park and safe edit region, `#224#11` park–edit–clear, `#226#09` closed continuation cell). **Ledger read first:** [Idea ledger][ledger].

## What would make this a continual-learning primitive?

In the [parent][parent], a universal park `s_park` is a fixed-width, history-independent live state that decouples a one-shot blind edit (`park → edit → clear`). In [seam leaks (#237)][seam], old-task training shapes a safe edit region `E(P)` around `s_park` and preserves it across reachable old update orders. In [adaptive renewal (#236)][adaptive], ordinary successor `C` updates contract reachable post-default beliefs back into a small recurring recovery interface. In [parked replacements (#244)][parked], a park compiles order-free batch partitions for incoming `B` work.

If the **maintenance park** (where blind pairs are edited) and the **recovery interface** (where ordinary `C` work returns the learner after an adaptive default) remain *separate*, two structural failures follow:
1. After recovering from a default, the host must still re-park before admitting the next blind pair, paying double entry latency, a second service-floor dip, and a second clear hazard.
2. When an arriving real pair interrupts `C` recovery *mid-basin* — before the learner reaches the park center — a separate recovery interface cannot admit the pair without stalling, re-parking past deadline, leaking which default occurred, or violating an installed task.

**MRS2's bet (return-to-ready park):** co-train **one public park** `P` whose **safe edit region** `E(P)` and **recovery basin** `B(P)` overlap and are sustained by ordinary useful successor `C` work, so that:
1. **Installed-task retention holds everywhere:** every state in `P`, every step along `B(P) → P`, every admitted interrupted-recovery exit, and every post-clear continuation satisfies hard `A`, prior `Bᵢ`, and disjoint/rare `C` floors for all compatible hidden histories `h ∈ H`.
2. **Interrupted recovery still admits real pairs:** even if recovery is interrupted before reaching `P`, any interior state inside the certified overlap `B(P) ∩ E(P)` already carries at least one common backed finish with a history-blind public clear `s_clear(target)`.
3. **No disguised shortcuts:** no save/restore stack (killed in the [Idea ledger][ledger] under return-point adapters), no inert spare or parked adapter masquerading as a load-bearing park feature, no disguised cleanup replacing matched `C` utility, and no covert history dispatch through norms, clipping inputs, or hidden optimizer slots. Keep **live service**, **executable reservations**, and **optimizer residuals** on three separate ledgers.

**Prior-art floor.** [Once-for-All][ofa] trains multi-setting subnetworks; [OML][oml] and [ANML][anml] meta-learn sequential plasticity; [OGD][ogd] and [GEM][gem] project updates away from old tasks; [safe RL via shielding][shield] and [barrier certificates][barrier] enforce invariant sets; [imperfect-information games][games] and [conformant planning][conformant] synthesize belief-state strategies; [Net2Net][net2net] and [make-before-break (#157)][make] decouple transitions via extra width; [optimizer resets][optreset] wipe slots globally; and [#224#17][parent], [#236#10][adaptive], [#237#12/#15][seam], and [#244][parked] cover individual pieces. Per the [Idea ledger][ledger] merge rule, MRS2 is a conditional primitive (`P`) only if co-training `E(P)` and `B(P)` under ordinary `C` work beats **each part alone**, **their best equal-budget stack**, a **separate park and recovery interface** (re-parking after each default), and a **parked adapter / inert spare** at matched width, `C` utility, and per-tick `A/Bᵢ/C` retention. Anything that only tunes, audits, or diagnoses an existing stack is labelled an improvement (`I`).

**Common test rules.** Freeze arrival and fault rules, legal reads, public transcript, lawful edit language `L`, width/capacity bounds, deadline `d`, `A/Bᵢ/C` floors (including rare slices), and `C`-utility targets before running. Check ordinary `A`, all installed `Bᵢ`, and disjoint rare `C` independently of the construction's witnesses at **every recovery tick, interruption tick, mid-edit tick, public clear, and post-clear continuation**. Charge offline co-training, park-state service loss, proof checking, rejected candidates, and fallback equally. Include both an **out-of-basin interruption negative** (must refuse or bail out safely, never silently admit) and a **matched-`C` non-contracting control** (to ensure `C` causally funds readiness rather than coinciding with it). All tests below are proposals.

## Two paper fixtures (feasibility and falsifiability checks, not proof of a matched-budget win)

### Fixture R1: overlapping safe edit region and recovery basin beats separate recovery + re-park, with an out-of-basin negative

Consider a fixed-width live host `(s, w, u) ∈ [0, 1]³` where `s` is an active shared coupling gate, `w` is the edited weight, and `u` is a compensatory offset. Lawful updates change one coordinate per tick. Installed tasks at **every tick**:
- Ordinary `A` requires `1/2 + (1/2)·s ≥ 1/2` (normal-mode value `1` at `s = 1`, `3/4` at `s = 1/2`, `1/2` at `s = 0` — so `s` is load-bearing in normal mode, not an inert spare).
- Two compatible post-default hidden histories `h₁, h₂` (left by an adaptive default with opposite-signed residual coupling) require `C₁ = 1 − 2·s·(w − u) ≥ 0` and `C₂ = 1 + 2·s·(w − u) ≥ 0`.

Suppose an arriving real pair `B₁` requires `(s, w, u) = (1, 1, 1)` within a **3-tick deadline** from the interruption tick.
- **Separate recovery + park interface:** ordinary `C` recovery targets normal mode `s = 1`. When interrupted at `(1, 0, 0)`, direct edits fail (`w ← 1` gives `C₁ = −1 < 0`; `u ← 1` gives `C₂ = −1 < 0`), while re-parking first (`s ← 0`, `w ← 1`, `u ← 1`, `s ← 1`) takes **4 ticks** and misses the 3-tick deadline.
- **Co-trained return-to-ready park (`B(P)` routed through `s ≤ 1/2`):** ordinary `C` recovery steps move `s` into `B(P) ∩ E(P) = {s ≤ 1/2}`. If recovery is interrupted at the interior basin state `(1/2, 0, 0)` (`A = 3/4 ≥ 1/2`, `C₁ = C₂ = 1`):
  1. `w ← 1` → `(1/2, 1, 0)`: `A = 3/4 ≥ 1/2`, `C₁ = 1 − 2(1/2)(1) = 0 ≥ 0`, `C₂ = 2 ≥ 0`.
  2. `u ← 1` → `(1/2, 1, 1)`: `A = 3/4 ≥ 1/2`, `C₁ = 1 ≥ 0`, `C₂ = 1 ≥ 0`.
  3. Public clear `s ← 1` → `(1, 1, 1)`: `A = 1 ≥ 1/2`, `C₁ = 1 ≥ 0`, `C₂ = 1 ≥ 0`, `B₁` met in **3 ticks**, with zero re-park hop, zero history read, and zero save/restore buffer.
- **Negative control (interruption leaving the basin):** suppose an out-of-contract perturbation pushes the host to `s = 3/4` (outside `B(P)`). At `(3/4, 0, 0)`, direct `w ← 1` yields `C₁ = 1 − 3/2 = −1/2 < 0` and `u ← 1` yields `C₂ = −1/2 < 0`, while re-parking `s ← 1/2` first takes 4 ticks and misses the deadline. The out-of-basin interruption is provably inadmissible and must be refused.

### Fixture R2: weight-only parking fails a post-clear optimizer-slot alias unless `C` contracts the slot

Extend Fixture R1 with a hidden momentum slot `m_w` on `w` (decay `β = 2/3`), where two post-default histories `h₁, h₂` land at the **same public weights** `(1/2, 0, 0)` inside `B(P) ∩ E(P)` but carry opposite hidden slots `m_w ∈ {+1, −1}`. After the 3-tick edit and public clear to `(1, 1, 1)`, commit-time weights satisfy `A = 1` and `C₁ = C₂ = 1`.
- **Without `C`-funded slot contraction:** on the first ordinary zero-gradient post-clear coast tick, `w' = w + β·m_w = 1 ± 2/3`, so `w' − u = ±2/3` at `s = 1`, giving `C₁ = 1 − 2(1)(2/3) = −1/3 < 0` (for `h₁`) or `C₂ = −1/3 < 0` (for `h₂`). Weight-only parking passes commit and fails post-clear.
- **With ordinary `C` slot contraction inside `B(P)`:** a truthful `C` prefix contracts `|m_w|` from `1` to `≤ 1/2` while advancing `C`. After the same 3-tick edit and public clear, the post-clear coast satisfies `|w' − u| ≤ (2/3)(1/2) = 1/3`, so `C₁, C₂ ≥ 1 − 2(1)(1/3) = 1/3 ≥ 0`.
- **Negative control:** substitute an equally `C`-accurate batch order that leaves `|m_w| = 1`; commit weights still tie `(1, 1, 1)`, exposing that weight-only readiness cannot replace `C`-funded slot contraction.

## Idea cards

### Co-training the safe edit region and recovery basin

#### 01. Co-train one public park whose safe edit region overlaps its recovery basin (P; MRS2 core)
- **Mechanism:** Optimize a fixed-width host on development streams so ordinary useful `C` updates contract reachable post-default beliefs into a basin `B(P)` whose interior already lies inside a certified safe edit region `E(P)` with a history-blind public clear, removing the separate recover-then-re-park hop.
- **Novelty vs nearest prior art:** [#224#17][parent] pre-trains a one-shot park, [#237#12/#15][seam] trains `E(P)` across old orders, and [#236#10][adaptive] trains a recovery basin; [OML][oml]/[ANML][anml] meta-learn plasticity without certified blind edit regions. The candidate primitive is **co-training `B(P) ∩ E(P)` as one live interface** so recovery progress immediately creates blind edit admissibility.
- **Cheapest first test:** Fixture R1 plus a 2-layer piecewise-linear CPU host with held-out default cuts and 3-tick pair deadlines; compare against `#224#17`, `#237#15`, `#236#10` alone, their best equal-budget stack, a separate park + recovery interface (re-parking after each default), and an out-of-basin interruption negative.
- **Old-task retention check:** Evaluate independent `A`, prior `Bᵢ`, and disjoint rare `C` at every recovery tick, interruption tick, mid-edit tick, clear, and post-clear continuation; reject any arm that wins by lowering normal-mode `A` or `C` utility.

#### 02. Certify a deadline-indexed interrupted-recovery admission frontier inside the basin (P)
- **Mechanism:** Instead of certifying blind pair admission only at the park center `s_park`, certify nested public frontiers `F_d ⊆ B(P) ∩ E(P)` indexed by remaining deadline `d`, so an arriving real pair is admitted at the exact tick recovery is interrupted whenever the current public state lies inside `F_d`.
- **Novelty vs nearest prior art:** [#236#03][adaptive] ranks recovery time to a fixed ready state and [barrier certificates][barrier] certify static invariant sets. Nested **deadline-indexed admission frontiers inside the recovery basin** turn partial recovery into immediate, verified service capacity.
- **Cheapest first test:** Sweep interruption tick `t_int ∈ {0, 1, 2}` and deadline `d ∈ {2, 3, 4}` on Fixture R1 and a tiny bilinear host; compare against center-only park admission, re-parking after interruption, and exact timed conformant planning.
- **Old-task retention check:** Check `A`, prior `Bᵢ`, and rare `C` along every admitted `F_d` exit and verify that an interruption just outside `F_d` triggers refusal rather than an unsafe rush.

#### 03. Keep a common backed finish live on every recovery step without history dispatch (P)
- **Mechanism:** Maintain at least one history-blind, resource-backed finish (extending [#235#08][menu] redundant finishes) whose entry precondition holds at every tick along `B(P) → P`, so any legal interruption can immediately launch a real pair without reading which default occurred or waiting for an unbacked slot.
- **Novelty vs nearest prior art:** [#235#08][menu] trains redundant finishes for live invalidations and [#224#09][parent] certifies anytime fragment exits. Keeping a **common backed finish continuously live along post-default recovery** couples executable reservation liveness directly to the basin trajectory.
- **Cheapest first test:** Two overlapping lease windows where lease 1 defaults and a real pair arrives at tick 1 or 2 of `C` recovery; compare against recovery-then-reserve, separate backup adapters (charged for width), and exact contingent scheduling.
- **Old-task retention check:** Score `A`, installed `Bᵢ`, and rare `C` at the default cut, every recovery tick, and across the launched pair's execution and clear, including a double-booking negative where one carrier is already committed.

#### 04. Train the shared park coordinate to be load-bearing in normal mode and decoupling in basin mode (P)
- **Mechanism:** Co-train `B(P) ∩ E(P)` subject to a hard normal-mode intervention floor on the shared coordinate `s` (extending the control in [#237#17][seam] into a training constraint), so one active feature carries both normal `A/Bᵢ` service and interrupted-recovery edit decoupling at fixed width.
- **Novelty vs nearest prior art:** [Once-for-All][ofa] trains nested subnetworks and [#224#12][parent] decouples a fixed gate algebraically. Enforcing **non-degenerate normal-mode load bearing** while co-training `B(P) ∩ E(P)` rules out the inert-spare shortcut and tests whether one active feature can serve both roles.
- **Cheapest first test:** A fixed-width 2-branch toy MLP where clamping `s = 0` drops normal `A` from `1.0` to `0.55` (above hard floor `0.50`, below normal target `0.95`); compare co-trained shared `s` against a parked adapter / inert spare at matched total parameters and against `#224#17` alone.
- **Old-task retention check:** Measure normal-mode `A/Bᵢ/C` (requiring `s` intervention drop ≥ threshold), basin-mode `A/Bᵢ/C`, and post-clear `B` accuracy; disqualify any solution that hides `A` in an unused bypass.

#### 05. Couple basin contraction with public clear reachability, not endpoint loss (P)
- **Mechanism:** During offline host design, penalize post-default `C` trajectories that reduce `C` loss yet leave the preimage of the history-blind public clear map `s_clear(target)`, optimizing for *clearable* readiness rather than raw weight proximity to `s_park`.
- **Novelty vs nearest prior art:** [#236#10][adaptive] penalizes missing recovery routes and [#237#16][seam] constrains clear maps to be history-free. Coupling **basin contraction directly to the public-clear preimage** prevents `C` recovery from landing in a "roach motel" park that is safe to enter but impossible to clear blindly.
- **Cheapest first test:** A 3-coordinate nonlinear host with two equal-`C`-loss basins, one clearable publicly for held-out `B` targets and one requiring history-specific restore; compare clear-coupled training against endpoint-loss basin training and `#237#16` alone.
- **Old-task retention check:** Evaluate `A`, prior `Bᵢ`, and rare `C` at park entry, mid-edit, clear, and two post-clear steps across held-out `B` targets, including an un-clearable target that must be refused.

#### 06. Co-train a relational ready-park across two active coordinates when single-coordinate parking starves A (P)
- **Mechanism:** Instead of parking one scalar coordinate `s`, co-train ordinary `C` updates to restore a public conserved relation `g(s₁, s₂) = c` across two active coordinates (extending [#244#05][parked] to post-default recovery), so `A` stays high while edits move along the relation's decoupling manifold.
- **Novelty vs nearest prior art:** [#244#05][parked] parks a relation for order-free batch partitions; [#224#18][parent] staggers scalar parks. Co-training a **relational recovery basin** lets `C` restore decoupled editability when no single-coordinate park clears `A`'s service floor.
- **Cheapest first test:** Extend Fixture R1 to `(s₁, s₂, w, u)` where `A` requires `s₁ + s₂ ≥ 3/2` (blocking `s₁ = 0` or `s₂ = 0`) while `C₁, C₂` depend on `(s₁ − s₂)·(w − u)`; compare relational ready-park against single-coordinate parking (infeasible), OGD projection, and width-charged `#157`.
- **Old-task retention check:** Check `A`, prior `Bᵢ`, and a rare `C` slice sensitive to `s₁ + s₂` at every recovery step, mid-edit, and clear, plus a negative where `C` breaks the conserved relation.

### Ordinary successor C work as the basin's engine

#### 07. Use ordinary C batches to contract hidden optimizer-slot aliases inside the park (P)
- **Mechanism:** Select lawful orders of required truthful `C` batches that simultaneously deliver target `C` utility and contract hidden momentum/second-moment aliases `m(h₁) − m(h₂)` inside `B(P)` (as in Fixture R2), certifying post-clear coast safety without wiping optimizer slots globally.
- **Novelty vs nearest prior art:** [Optimizer resets][optreset] destroy useful momentum globally; [#224#16][parent] parks one slot explicitly; [#238][echo] absorbs echoes before a consumer. Using **required ordinary `C` work inside the recovery basin** to contract post-default slot aliases eliminates both global resets and extra cleanup batches.
- **Cheapest first test:** Fixture R2 plus a small momentum MLP after two opposite-signed defaults; compare `C`-ordered slot contraction against weight-only parking, global momentum reset (charging `B` slowdown), separate cleanup batches, and a matched-`C` non-contracting batch order.
- **Old-task retention check:** Score `A`, prior `Bᵢ`, and rare `C` at commit and across a 5-step held-out post-clear momentum continuation to catch delayed slot-mediated relapse.

#### 08. Make the park self-renewing across alternating defaults and successful pairs (P)
- **Mechanism:** Certify a cross-exit induction invariant (combining [#236#09][adaptive] and [#237#15][seam]): both a *completed* blind pair ending at `s_clear` and an *interrupted default* land inside the same `C`-contractible basin `B(P)`, so ordinary `C` work re-arms the ready park across arbitrarily many rounds without per-round redesign.
- **Novelty vs nearest prior art:** [#236#09][adaptive] composes default and success exits for an abstract renewal game; [#237#15][seam] keeps one park across old-task orders. Proving **inductive basin closure across alternating successes and defaults** turns a one-shot park into a recurring maintenance primitive.
- **Cheapest first test:** A 3-round stream of `default → C → interrupted pair → clear → C → default → C → pair` on a tiny smooth host; compare inductive ready-park training against single-period park training, re-parking after each round, and fresh per-round synthesis.
- **Old-task retention check:** Protect every newly installed `Bᵢ` alongside `A` and prior `C` across all 3 rounds and a 4th held-out round; flag any arm whose park margin decays monotonically with round index.

#### 09. Share one ready park across two distinct successor C task families without a family tag (P)
- **Mechanism:** Train the fixed-width host so two unrelated incoming `C` task families each supply lawful updates that contract post-default beliefs into the *same* public park `P` and safe edit region `E(P)`, without dispatching on a task-family identifier.
- **Novelty vs nearest prior art:** [#236#12][adaptive] asks two `C` families to fund one renewal interface; [OML][oml] transfers representations for prediction. Requiring **multi-family `C` contraction into one certified `B(P) ∩ E(P)`** tests whether the park is a genuine structural feature rather than overfit to one `C` gradient direction.
- **Cheapest first test:** Train on two rotated-feature `C` families and hold out a third convex combination with randomized default cuts; compare single-park host against a task-ID oracle, per-family parked adapters, and `#236#12` plus separate re-parking.
- **Old-task retention check:** Evaluate `A`, installed `Bᵢ`, and *both* historical `C` families after switching families, mid-interruption, and after clearing a held-out `B` pair.

#### 10. Require C-funded basin replenishment to beat matched-C non-contracting controls (I)
- **Mechanism:** Run a paired-order causal intervention (adapting [#236#11][adaptive] to ready parks): replace the basin-contracting `C` prefix with a second truthful `C` batch order having identical `C` utility and `A/Bᵢ` retention at the interruption tick, and verify that only the contracting order unlocks blind pair admission.
- **Novelty vs nearest prior art:** [#236#11][adaptive] swaps equally useful `C` orders on renewal; this assay isolates whether ordinary `C` work *causally* maintains `B(P) ∩ E(P)` rather than merely coinciding with passive decay or a static host property.
- **Cheapest first test:** Construct a matched-utility `C` batch pair at two default cuts in Fixture R2 and a tiny nonlinear host; reject any primitive claim if both orders yield the same interrupted-recovery admission rate.
- **Old-task retention check:** Match `A`, prior `Bᵢ`, and rare `C` at every intermediate tick for both orders so apparent basin replenishment cannot be funded by silent forgetting.

#### 11. Repurchase park-basin approximation slack through ordinary C contractions (P)
- **Mechanism:** Maintain a bounded public approximation-error budget `ε` for `E(P)` under nonlinear host drift (extending [#236#16][adaptive] to parked edits); allow an interrupted pair to spend `Δε` only when a certified ordinary `C` prefix contracts all reachable aliases enough to replenish `ε` before the next default window.
- **Novelty vs nearest prior art:** [Approximate bisimulation][bisim] bounds transition error and [#224#21][parent] carries static drift margins. Making **`C` updates repurchase park-region slack** replaces one-way margin exhaustion with a certified, bounded-memory renewal loop.
- **Cheapest first test:** A scalar nonlinear host with controlled expansion during `B` edits and contraction during truthful `C` updates; compare slack-repurchasing ready parks against static drift margins, observed-error resets (illegal non-blind control), and exact reachability.
- **Old-task retention check:** Test worst-case `A`, prior `Bᵢ`, and rare `C` at maximal slack expansion (right before `C` replenishment) and plant an un-contractible drift step that must trigger refusal.

#### 12. Recycle a defaulted pair's backing only after a new blind pair executes from the ready park (P)
- **Mechanism:** Separate *eligibility* to retire a defaulted pair's reservation from *reusable capacity* (coupling [#236#18][adaptive] and `MRS5` to `B(P) ∩ E(P)`): declare backing reclaimed only after ordinary `C` work re-enters the ready park and a real arriving blind pair executes on that reclaimed backing and clears cleanly.
- **Novelty vs nearest prior art:** [#236#18][adaptive] requires cold reuse after renewal; garbage-collected adapters reclaim dormant units by accounting alone. Binding **reclamation to cold blind execution out of the ready park** catches phantom capacity that passes park checks yet cannot launch a real pair.
- **Cheapest first test:** A 2-carrier host after two consecutive defaults with one live rare reader attached to the first carrier; compare cold-reuse ready parks against accounting-only reclaim and separate park + GC at equal scratch capacity.
- **Old-task retention check:** Exercise the rare reader and all `A/Bᵢ/C` before release, during the interrupted-recovery launch on the reclaimed carrier, at clear, and on a post-clear normal step.

### Interrupted recovery, public clears, and blind-seam safety

#### 13. Synthesize a two-stage interrupted-recovery exit: finish-in-basin vs certified bailout (P)
- **Mechanism:** At any interruption state `x`, evaluate a purely public membership test: if `x ∈ F_d`, admit the arriving pair directly through `E(P)` and clear publicly; if `x ∉ F_d` (an out-of-basin interruption), execute a history-blind bailout or clean refusal that preserves all installed tasks without revealing which default occurred.
- **Novelty vs nearest prior art:** [#224#15][parent] emits offline park/clear infeasibility witnesses and [shielding][shield] blocks unsafe actions. A **two-stage online public gate (admit-in-basin vs blind bailout)** directly handles the row-357 out-of-basin interruption regime without stalls or history leaks.
- **Cheapest first test:** Fixture R1 mixing in-basin (`s = 1/2`) and out-of-basin (`s = 3/4`) interruptions under a 3-tick deadline; compare two-stage gating against optimistic admission (fails `C₁/C₂`), always-re-park (misses deadline), and query-to-split (charged for split bits).
- **Old-task retention check:** Check `A`, prior `Bᵢ`, and rare `C` on both accepted and bailed-out branches, plus a held-out continuation after bailout to ensure refusal leaves the host undamaged.

#### 14. Certify public clear maps under interrupted-recovery phase jitter (P)
- **Mechanism:** Train and verify the public clear map `s_clear(target)` so the same history-blind clear works regardless of *which tick* `t_int` of the `C` recovery word was interrupted, without indexing clear targets by private recovery progress or hidden step counters.
- **Novelty vs nearest prior art:** [#236#14][adaptive] tests phase-shift survival for renewal interfaces; [#237#16][seam] certifies one-shot history-free clears. Certifying **phase-invariant public clears across arbitrary interruption ticks** ensures interrupted recovery does not smuggle recovery phase as a covert selector.
- **Cheapest first test:** Interrupt a 3-step `C` recovery word at ticks `t_int ∈ {1, 2, 3}` with irregular predecessor lengths and apply the same public `s_clear(target)`; compare against phase-indexed clears, re-parking to a canonical center, and `#237#16` alone.
- **Old-task retention check:** Verify `A`, prior `Bᵢ`, and rare `C` at every interruption phase, at clear, and two steps post-clear; include an adversarial phase outside the certified window that must be refused.

#### 15. Separate service, executable reservations, and optimizer residuals on three public ledgers (I)
- **Mechanism:** Track ready-park admissibility across three explicit, unmerged public ledgers — (1) worst-history `A/Bᵢ/C` service margins, (2) backed finish reservations and deadlines, and (3) bounded optimizer-slot residual norms — refusing any transition that fails *any* single ledger even if a fused score looks safe.
- **Novelty vs nearest prior art:** Multi-objective shielding and [`cross-pool-54.md`][cross54] discipline rules motivate ledger separation; this is an architectural/verification improvement that prevents weight-level park checks from masking slot echoes (Fixture R2) or double-booked carriers.
- **Cheapest first test:** Seed three distinct single-ledger faults (a rare-`C` dip, a double-booked finish, and Fixture R2's slot alias) and compare three-ledger gating against a fused scalar park score and weight-only certification.
- **Old-task retention check:** Verify zero false admissions across all three seeded faults and measure whether ledger separation adds false refusals on valid Fixture R1 transitions.

#### 16. Block covert default-history dispatch across the recovery-to-edit seam (P)
- **Mechanism:** Enforce cross-seam non-interference (extending [#224#07][parent] and [#237#05][seam]) across the exact handoff from interrupted `C` recovery to a `B` edit: certify that live aggregate statistics (gradient norms, clipping inputs, adaptive denominators, and effective step sizes) executed during the interrupted edit are identical across all compatible post-default histories.
- **Novelty vs nearest prior art:** [Information-flow typing][flow] and [#237#05][seam] audit static fragment seams. Auditing **the dynamic recovery-to-edit seam** closes a specific MRS2 leak where post-default residuals subtly trigger different clipping branches during an interrupted `B` edit.
- **Cheapest first test:** Construct an interrupted-recovery fixture where two post-default histories agree on weights at `s = 1/2` yet cross a gradient-clip threshold differently during `B`; compare seam-non-interference certification against weight-only checks and a paid licensed split.
- **Old-task retention check:** Swap hidden post-default histories in shadow across the seam and check `A`, prior `Bᵢ`, and rare `C`; reject any edit whose retention relies on history-conditioned clipping.

#### 17. Detect a disguised save/restore or hidden-adapter park via shadow pre-default swaps (I)
- **Mechanism:** Audit every candidate ready park by (a) swapping hidden pre-default states in shadow and (b) zeroing any coordinate with zero normal-mode `A/Bᵢ` intervention effect at the interruption tick; a genuine public return-to-ready park still clears `A/Bᵢ/C` and admits `B`, whereas a smuggled save-stack or inert parked adapter fails immediately.
- **Novelty vs nearest prior art:** [#224#14][parent] checks no-escrow-leak on one-shot clears and [#237#17][seam] checks normal-mode contribution. Combining **shadow pre-default swaps with inert-coordinate zeroing** provides a single falsification audit against both degenerate MRS2 cheats.
- **Cheapest first test:** Pair a genuine Fixture R1 ready park with (i) a save-stack storing pre-default sign in a slack unit and (ii) a parked adapter holding `A` in an inert bypass; run the shadow audit on all three.
- **Old-task retention check:** Check `A`, prior `Bᵢ`, and rare `C` under shadow perturbations both at interruption and post-clear; confirm zero false failures on genuine ready parks.

#### 18. Handle double-interruption via rolling ready parks across coupled coordinates (P)
- **Mechanism:** Combine [#224#18][parent] (staggered rolling parks) with `B(P)`: if a *second* adaptive default strikes while an interrupted-recovery pair is mid-edit on coordinate `s₁`, shift live `A/Bᵢ` service onto `s₂`, preserve the already-installed first write without rollback, and let ordinary `C` work contract `s₁` back into `B(P)`.
- **Novelty vs nearest prior art:** [#224#18][parent] uses rolling parks for a single one-shot edit and [#236#05][adaptive] certifies two-order default overlaps. Coupling **rolling ready parks to mid-edit double defaults** extends interrupted-recovery safety to nested faults at fixed width.
- **Cheapest first test:** A 2-gate host (`s₁ + s₂ ≥ 1`) where default 1 triggers `C` recovery, an arriving pair interrupts at tick 1, and default 2 hits mid-edit; compare rolling ready parks against single-park abort/rollback (charged for backup bytes) and exact contingent planning.
- **Old-task retention check:** Verify `A`, installed `Bᵢ`, the partial first write, and rare `C` at default 1, interruption 1, default 2, second recovery, and final clear.

### Failure witnesses, composition limits, and falsification audits

#### 19. Emit a three-way impossibility witness: no basin, disjoint edit region, or un-clearable exit (P)
- **Mechanism:** When no return-to-ready park exists for a declared `(L, d, H)` contract, emit a minimal typed obstruction separating: (a) *no recovery basin* (`C` cannot contract post-default beliefs within budget), (b) *disjoint basin and edit region* (`B(P)` and `E(P)` both exist, but `B(P) ∩ E(P) = ∅` within deadline `d`), and (c) *un-clearable exit* (`B(P) ∩ E(P) ≠ ∅`, but no history-blind public clear meets `B` and `C`).
- **Novelty vs nearest prior art:** [#224#15][parent] splits no-safe-park vs unsafe-clear for one-shot parks; [#244#20][parked] splits entry, build, and clear obstructions. A **three-way ready-park witness** specifically diagnoses whether MRS2's coupling fails at `C` contraction, at `B(P) ∩ E(P)` overlap, or at public clearing — routing directly to the cheapest remedy.
- **Cheapest first test:** Construct three minimal variants of Fixture R1/R2 realizing each failure mode cleanly, plus the feasible case; compare typed routing against generic UNSAT refutation and always-re-park fallback.
- **Old-task retention check:** Confirm every remedy triggered by the witness (more `C` steps, re-park fallback, or licensed split) clears all per-tick `A`, prior `Bᵢ`, and rare `C` floors.

#### 20. Certify a minimal C-availability contract for the ready park with executable spoiling traces (I)
- **Mechanism:** Sweep public assumptions on incoming `C` batch spacing, interruption frequency, and default rate to output the weakest availability contract under which `B(P) ∩ E(P)` stays live, paired with an executable spoiling trace from lawful transitions just outside that contract (extending [#236#04/#08][adaptive]).
- **Novelty vs nearest prior art:** Assume–guarantee assumption mining and [#236#04/#08][adaptive] already compute minimal environment assumptions; applying this to MRS2 prevents hidden fairness premises ("enough `C` always arrives before the next pair") from inflating ready-park claims.
- **Cheapest first test:** Vary `C`-to-interruption spacing `{0, 1, 2, 3}` ticks on a 2-default stream and verify that the emitted spoiling trace reproduces an actual `B(P) ∩ E(P)` breach in the learner.
- **Old-task retention check:** Verify `A`, prior `Bᵢ`, and rare `C` on both sides of the availability boundary, confirming that contract violations fail gracefully to refusal rather than silent forgetting.

#### 21. Measure the normal-mode plasticity and C-utility tax of keeping a ready park live (I)
- **Mechanism:** Hold width, compute, and hard `A/Bᵢ/C` floors fixed while sweeping the `B(P) ∩ E(P)` co-training weight to plot the exact Pareto frontier between interrupted-recovery pair admission rate and normal-mode `A/B/C` utility — killing any ready park whose normal-mode tax exceeds a simple stall or re-park baseline.
- **Novelty vs nearest prior art:** Pareto-frontier auditing is standard; this specifically tests the ledger's anti-illusion rule that a maintenance park is not free if it quietly taxes normal `C` learning or `B` plasticity.
- **Cheapest first test:** A tiny smooth CPU host trained across 5 co-training weights with held-out `B` and `C` streams; compare the Pareto hypervolume against unshaped training + re-park, `#224#17` alone, and `#236#10` alone.
- **Old-task retention check:** Enforce identical per-tick `A`, prior `Bᵢ`, and rare `C` floors across all frontier points; reject any point that buys admission rate by relaxing rare-slice retention.

#### 22. Falsification audit: test whether MRS2 beats its stacked parts and separate interfaces (I)
- **Mechanism:** On an enumerated factorial grid of small multi-history default-and-interruption worlds, run a head-to-head comparison of (a) MRS2 co-trained ready park, (b) `#224#17` trained park alone, (c) `#237#15` order-preserving park alone, (d) `#236#10` recovery basin alone, (e) their best equal-budget stack, (f) a separate park + recovery interface re-parking after each default, (g) parked adapters / inert spares, and (h) exact contingent planning — charging offline co-training, park-state service loss, proof checks, and fallbacks equally.
- **Novelty vs nearest prior art:** [#224#22][parent] and [#237#22][seam] audit one-shot parks and seam leaks; this audit enforces the [Idea ledger][ledger] merge rule directly on MRS2, demanding a regime where co-training `B(P) ∩ E(P)` strictly beats the best stacked parts and separate interfaces.
- **Cheapest first test:** A factorial CPU grid crossing deadline tightness (3 vs 4 ticks), slot-alias presence (Fixture R2 on/off), interruption placement (in-basin vs out-of-basin), and `A` floor tightness (allowing scalar vs relational parks).
- **Old-task retention check:** Admit only arms clearing identical per-tick `A`, installed `Bᵢ`, and disjoint rare `C` floors at matched `C` utility; report interrupted-pair admission rate, out-of-basin refusals, shadow-swap leaks, and normal-mode tax separately.

## Ranked deeper questions

1. **Does co-training the safe edit region `E(P)` and recovery basin `B(P)` strictly beat the best equal-budget stack of `#224#17 + #237#15 + #236#10` and a separate park-plus-recovery interface once interrupted-recovery latency and normal-mode tax are charged?** Start with cards 01, 02, 21, and 22 on Fixture R1 and a tiny piecewise-linear host. A genuine primitive win requires admitting real pairs under interrupted recovery that every stacked and separate-interface control either misses by deadline, refuses, or pays for with extra width or lower `A/Bᵢ/C` utility.
2. **Can ordinary useful successor `C` work causally contract both weight-space post-default beliefs and hidden optimizer-slot aliases into `B(P) ∩ E(P)` without degrading `C` utility or smuggling disguised cleanup?** Start with cards 07, 10, and 11 on Fixture R2. If a matched-`C` non-contracting batch order gives the same admission rate, or if `C` contraction costs more `C` utility than a targeted cleanup step, do not credit ordinary `C` work for funding the park.
3. **Can one active, load-bearing shared feature carry both normal-mode `A/Bᵢ` service and return-to-ready park decoupling in a nonlinear host, or does co-training inevitably collapse into an inert spare or parked adapter?** Start with cards 04, 06, and 17. Require a verified normal-mode intervention floor on `s` (or on both coordinates of a relational park) and run the shadow pre-default swap + inert-coordinate zeroing audit before claiming fixed-width reuse.
4. **Does a ready park stay inductively self-renewing across alternating successes, adaptive defaults, and out-of-basin interruptions without leaking default history across the recovery-to-edit seam or growing its proof archive?** Start with cards 08, 12, 13, 14, and 16. Require cold blind execution on reclaimed backing, phase-invariant public clears, zero clipping/norm leaks across the seam, and clean bailout on out-of-basin interruptions over at least three consecutive renewal rounds.

**Verdict:** Keep return-to-ready parks (MRS2) as a conditional primitive only if co-training `B(P) ∩ E(P)` under ordinary useful `C` work lets one active, fixed-width public park retain all installed tasks (`A`, prior `Bᵢ`, rare `C`) and admit real pairs during interrupted recovery strictly better than `#224#17`, `#237#15`, `#236#10`, their best equal-budget stack, separate park-and-recovery interfaces, and parked adapters — while refusing out-of-basin interruptions and passing shadow-swap and seam-non-interference audits. Fixtures R1 and R2 make the interaction concrete and falsifiable, not established.

[parent]: https://github.com/manojbajaj95/cl/pull/224
[triage]: https://github.com/manojbajaj95/cl/blob/5fec005cdc2b6962a4989be02228c98e46ce50f1/reviews/flood-triage.md#L357
[cross54]: https://github.com/manojbajaj95/cl/blob/abb0e5f78b507fbeb628aa04ccc0a2af6abefb10/ideas/flood/cross-pool-54.md
[ledger]: https://github.com/manojbajaj95/cl/blob/5fec005cdc2b6962a4989be02228c98e46ce50f1/reviews/idea-ledger.md
[adaptive]: https://github.com/manojbajaj95/cl/pull/236
[seam]: https://github.com/manojbajaj95/cl/pull/237
[menu]: https://github.com/manojbajaj95/cl/pull/235
[echo]: https://github.com/manojbajaj95/cl/pull/238
[parked]: https://github.com/manojbajaj95/cl/pull/244
[make]: https://github.com/manojbajaj95/cl/pull/157
[ofa]: https://arxiv.org/abs/1908.09791
[oml]: https://huggingface.co/papers/1905.12588
[anml]: https://www.alphaxiv.org/abs/2002.09571
[ogd]: https://arxiv.org/abs/1910.07104
[gem]: https://arxiv.org/abs/1706.08840
[shield]: https://www.alphaxiv.org/abs/1708.08611
[barrier]: https://doi.org/10.1109/TAC.2007.902736
[games]: https://www.alphaxiv.org/abs/0706.2619
[conformant]: https://arxiv.org/abs/1401.3468
[net2net]: https://arxiv.org/abs/1511.05641
[optreset]: https://arxiv.org/abs/2306.17833
[bisim]: https://doi.org/10.1109/TAC.2007.895849
[flow]: https://doi.org/10.1109/JSAC.2002.806121
