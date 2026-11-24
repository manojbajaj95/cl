# Indistinguishable edit replies: corridors and common replies under partial observation

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Cross-pool round 41](../ideas/flood/cross-pool-41.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36)), crossing [Accommodation games](https://github.com/manojbajaj95/cl/pull/167) and [Return corridors](https://github.com/manojbajaj95/cl/pull/168). **Review seed:** [Flood triage row 269](https://github.com/manojbajaj95/cl/blob/f1aeb7d391ccb8ca315d6fa7ae3d19a7ad25d39d/reviews/flood-triage.md#L269) kept two directions at score 3: **AGR1** (select today's truthful examples so every future branch enters a shared witness region that also keeps a verified spare reply for the next edit) and **AGR4** (group future edits by what the learner's probes can observe and train so one verified reply works for each group, buying a distinguishing probe or refusing when none exists). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f1aeb7d391ccb8ca315d6fa7ae3d19a7ad25d39d/reviews/idea-ledger.md) (every merge must beat its parts' best baselines stacked at equal budget; no credit for true-by-construction results; label every card primitive candidate vs improvement/audit; include an old-task retention check in every cheapest first test).

## Is learning under partial observation of future editors a new object for continual learning?

**No as a mathematical formalism; conditionally yes as a continual-learning primitive.**

Each underlying mathematical ingredient already exists:

- **Partial-observation safety games** are observation-based two-player games solved by antichain fixed points over belief sets ([Chatterjee, Doyen, Henzinger & Raskin, 0706.2619](https://arxiv.org/abs/0706.2619)), where a winning strategy maps an observation history to one move safe for every state consistent with that history.
- **Finding one action that works across an uncertainty class** is conformant planning ([Palacios & Geffner, 1401.3468](https://arxiv.org/abs/1401.3468)) and contingent planning with sensing ([1909.13778](https://arxiv.org/abs/1909.13778)); choosing when to buy an extra observation versus act conservatively is classical value of information / dual control.
- **Steering trajectories into a shared certified set** is funnel composition / LQR-trees (Majumdar & Tedrake 2017), [Hamilton–Jacobi reachability](https://arxiv.org/abs/1709.07523), [control barrier functions](https://arxiv.org/abs/1903.11199), and tamper-resistant meta-training ([TAR, 2408.00761](https://arxiv.org/abs/2408.00761)).
- **Probe-indistinguishable retention twins** are already characterized linearly by [footprint counterfeits (PR #107)](https://github.com/manojbajaj95/cl/pull/107): a fixed linear assay `P` predicts protected margins `O` for all writes iff `row(O) ⊆ row(P)`, and whenever `row(O) ⊄ row(P)` there exist transcript-matched twins with opposite retention outcomes.

What none of those does alone is the continual-learning interaction where **today's truthful training examples substitute for tomorrow's probes and per-edit replies**:

1. **AGR1** requires future training branches to enter not merely a shared witness region `C` (where one small buffer covers today's labels), but `C ∩ Win_K` (where a verified spare reply still exists for the next foreign edit).
2. **AGR4** drops full white-box observation of the foreign edit `e_k`: the host sees only a bounded probe transcript `y_k = P(e_k(s))` and must answer every edit in the equivalence class `[y_k]_P` with **one** common verified reply `a(y_k) ∈ M`.
3. **The joint object** is an **observation-factored winning corridor** `(D, funnel, C, P, π_obs)`: a truthful dataset `D` chosen today so that every legal future training branch enters a shared witness region `C` inside the *observation-based* K-round winning kernel `Win_K^{obs}(P, M)`, where one compact buffer certifies `C` and one observation-indexed policy `π_obs` answers every indistinguishable edit class without needing to inspect hidden weights or buy extra probes.

**Primitive gate.** This object earns primitive status *only* if data-shaping `D` for `(C, Win_K^{obs}(P, M))` admits strictly more *useful frozen* multi-round edits—or matches admission at lower combined witness bytes, probe queries, and verification work—than the **stacked baseline** of its parts at identical move menu `M`, identical probe budget `|P|`, identical truthful example quota, and identical A/C retention floors:
- Return corridor alone ([PR #168](https://github.com/manojbajaj95/cl/pull/168) card 01) + full-info accommodation game ([PR #167](https://github.com/manojbajaj95/cl/pull/167) card 01) stacked;
- Antichain belief-state safety planning ([0706.2619](https://arxiv.org/abs/0706.2619)) / conformant planning ([1401.3468](https://arxiv.org/abs/1401.3468)) on the unshaped state with the exact same `P` and `M`;
- Spending the same evidence budget on active distinguishing probes instead of teaching examples;
- Obligation-quotient routing ([PR #168](https://github.com/manojbajaj95/cl/pull/168) card 02) and the free/natural corridor ([PR #168](https://github.com/manojbajaj95/cl/pull/168) card 06);
- Full-observation per-edit replies as the upper-bound ceiling.

## Formal setup and two exact rational witnesses

Let old tasks `A, C` have acquisition-anchored safe set `Win_0 = { s : inf_{x ∈ D_A} m_A(s, x) ≥ τ_A ∧ inf_{x ∈ D_C} m_C(s, x) ≥ τ_C }`. At round `k`, a blind foreign editor `E_k` applies a bounded write `e_k ∈ T(s_{k-1})`, and the host observes only the probe transcript `y_k = P(e_k(s_{k-1}))`. Define the transcript equivalence class (belief set) at state `s` as

```text
[y]_P(s) = { e ∈ T(s) : P(e(s)) = y }.
```

The observation-based K-round winning kernel over a fixed finite reply menu `M` is defined by backward induction with the reply quantifier **outside** the indistinguishable edit class:

```text
Win_0^{obs} = Win_0
Win_k^{obs}(P, M) = { s ∈ Win_0 : ∀ y ∈ P(T(s)), ∃ a ∈ M such that ∀ e ∈ [y]_P(s), a(e(s)) ∈ Win_{k-1}^{obs}(P, M) }.
```

Comparing `Win_k^{obs}` to full-info `Win_k` ([PR #167](https://github.com/manojbajaj95/cl/pull/167)) flips `∀ e ∈ [y]_P, ∃ a` into `∃ a, ∀ e ∈ [y]_P`. An observation-factored winning corridor `(D, τ, C, W, P, π_obs)` requires every legal B branch from the post-`D` state to keep `Win_0` (and transient replies when live-serving) on prefixes `t < τ` and enter `C ⊆ Win_K^{obs}(P, M)` by step `τ`, covered by one verified buffer `W`.

Two exact rational witnesses isolate why partial observation breaks full-info games, why today's examples can replace a probe, and why a shared 1-round corridor can still be a 2-round trap:

1. **Witness 1 (AGR4 — Full-info `Win_1` fails under `P`, yet one truthful example creates a common reply).** Let two rare A slices have margins `m_1(t_1, q_1) = 1 − ReLU(t_1 − q_1)` and `m_2(t_2, q_2) = 1 − ReLU(t_2 − q_2)` with floor `τ = 1/2`, starting at `(t_1, t_2) = (0, 0)`. The probe `P` observes only the scalar sum `y = t_1 + t_2` (`row(O) ⊄ row(P)`). Two blind edits arrive: `e_1: t_1 += 1` and `e_2: t_2 += 1`, both yielding `y = 1`. The fixed reply menu is `M = { a_1: q_1 += 1/2, a_2: q_2 += 1/2, a_both: (q_1, q_2) += (1/4, 1/4) }` (equal L1 budget `1/2`).
   - At unshaped state `s_0` with `(q_1, q_2) = (1/8, 1/8)` (pre-edit margins `1, 1`), `s_0 ∈ Win_1^{full}` (`a_1` answers `e_1` at margin `5/8`; `a_2` answers `e_2` at `5/8`). Yet `s_0 ∉ Win_1^{obs}(P, M)`: on `[y = 1] = {e_1, e_2}`, `a_1` fails `e_2` (`m_2 = 1/8`), `a_2` fails `e_1` (`m_1 = 1/8`), and `a_both` fails both (`3/8 < 1/2`).
   - Now apply one A-consistent truthful example `d ∈ D` that shifts starting thresholds to `s_0'` with `(q_1, q_2) = (1/4, 1/4)` (identical pre-edit A/C margins `1, 1`). Now `a_both` gives `(q_1, q_2) = (1/2, 1/2)`, holding `m_1 = 1/2, m_2 = 1` on `e_1` and `m_1 = 1, m_2 = 1/2` on `e_2`. Thus `s_0' ∈ Win_1^{obs}(P, M)`: **one teaching example replaced a distinguishing probe**.

2. **Witness 2 (AGR1 + AGR4 — Entering a shared 1-round corridor can lose the spare reply for round 2).** Extend Witness 1 to `K = 2` rounds: round 1 applies `e_1: t_1 += 1` or `e_2: t_2 += 1` (`y_1 = 1`); round 2 applies `e_1': t_1 += 1/2` or `e_2': t_2 += 1/2` (`y_2 = 3/2`), with the same `P` and `M`. Suppose two legal B branches land at `b_1: (q_1, q_2) = (1/2, 1/2)` and `b_2: (q_1, q_2) = (1/4, 1/2)`.
   - Both `b_1` and `b_2` lie inside the 1-round shared witness region `C_1 = Win_1^{obs}` (both have pre-edit margins `1, 1`, and `a_both` survives round 1 on both).
   - After round-1 `e_1` + `a_both`, `b_1` reaches `(q_1, q_2) = (3/4, 3/4)` and survives round 2 under `a_both` (`(1, 1)` gives `m_1 = 1 − ReLU(3/2 − 1) = 1/2` on `(e_1, e_1')`, and `1, 1` on `(e_1, e_2')`; symmetrically for `e_2`).
   - On `b_2`, round-1 `e_1` + `a_both` reaches `(1/2, 3/4)` (`m_1 = 1/2`, zero slack). In round 2, `P` sees only `(y_1, y_2) = (1, 3/2)`, which cannot distinguish `(e_1, e_1')` from `(e_2, e_2')`: `a_both` fails `(e_1, e_1')` (`m_1 = 1/4`), `a_1` fails `(e_2, e_2')` (`m_2 = 1/4`), and `a_2` fails `(e_1, e_1')` (`m_1 = 0`). So `b_2 ∈ C_1 \ Win_2^{obs}`. Only steering both branches into `C_2 = C_1 ∩ Win_2^{obs}` preserves a spare common reply.

## Four vacuity checks required on every card

1. **Omniscient probes:** If `P` already separates every edit needing a distinct reply, partial observation collapses to full-info [PR #167](https://github.com/manojbajaj95/cl/pull/167). Every test must verify a genuine `row(O) ⊄ row(P)` blindness gap.
2. **Rigid or over-hedged common replies:** A common reply that survives every edit by freezing weights, zeroing new-task utility, or burning excessive residual capacity can lose to buying one extra probe. Report the joint frontier of admitted useful edits, probe cost, B progress, and A/C floors.
3. **Free corridors and free common replies:** Natural SGD basin sharing ([PR #168](https://github.com/manojbajaj95/cl/pull/168) card 06) or an unshaped state may already admit a common reply. Credit shaping only for gains strictly above the unshaped baseline.
4. **Menu and probe inflation:** Freeze `M`, `P`, the editor bank `T`, and the truthful example pool identically across every baseline; charge every extra probe, stored frontier, or verifier call at equal cost.

## Idea cards

Labels follow the idea ledger: **P** = conditional primitive candidate; **I** = improvement or mandatory audit. All cheapest first tests are CPU-only (finite rational / small ReLU toys) and score old tasks A and C on independent held-out data never used for selection or calibration, including rare slices and every served prefix.

### Corridors that preserve a spare reply (AGR1)

#### 01. Shape today's examples to land every future branch inside `C ∩ Win_K` (P)
- **Mechanism:** Select truthful today-examples `D` so that every declared B training branch enters a shared witness region `C` by deadline `τ` *and* `C` lies inside the K-round winning kernel `Win_K` (or `Win_K^{obs}`), certifying both the shared buffer `W` and a verified spare reply for the next edit.
- **Novelty vs nearest prior art:** Directly develops AGR1. [Return corridors (PR #168)](https://github.com/manojbajaj95/cl/pull/168) card 01 certifies entry into a shared buffer region `C` without requiring a spare reply; [Accommodation games (PR #167)](https://github.com/manojbajaj95/cl/pull/167) card 01 trains into `Win_K` without merging diverging future branches into one buffer. New only if the joint target beats stacking `#168#01` and `#167#01` on Witness 2's dead-end corner trap.
- **Cheapest first test:** Implement Witness 2 in a 2-unit ReLU host with 2 legal B orders and a quantized pool of 12 truthful A-consistent examples. Compare natural convergence, `#168#01` corridor alone, `#167#01` kernel training alone, their best stack, and joint `C ∩ Win_2` selection at equal example count and fixed `M`.
- **Old-task retention check:** Verify A and C on independent rare slices at every prefix `t = 0, …, τ` on both B branches and after both rounds of frozen blind edits; any transient dip or round-2 breach fails the card.

#### 02. Merge branches in the reply-relevant quotient while keeping B content distinct (P)
- **Mechanism:** Define the *reply-obligation quotient* `π_reply(s)` as the projection onto coordinates read by either the witness buffer `W` or the spare reply menu `M`. Select `D` so diverging B branches merge in `π_reply` (sharing both the proof and the spare reply) while remaining distinct in B's private coordinates `v`.
- **Novelty vs nearest prior art:** Extends [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 02 (obligation quotient for passive proofs) and [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 10 (game-Nerode quotient, top-10 #2) to the *controlled* quotient under `M`; avoids PackNet/GPM hard masks by inducing separation through truthful data.
- **Cheapest first test:** 3-unit ReLU host where 2 units feed rare A slices and `M` (`π_reply`) while 1 unit carries B-order content (`v`). Compare full-state merging, obligation-only merging (`#168#02`), PackNet-style frozen masks, and `π_reply` merging on B utility, buffer bytes, and round-2 admission.
- **Old-task retention check:** Check A/C on every branch after overwrite and round-2 edits, and explicitly search for any legal edit that opens a gate coupling `v` back into A.

#### 03. Divert dead-end safe branches using round-2 losing suffixes (P)
- **Mechanism:** When a candidate `D` steers all B branches into `C_1` (safe for round 1) but one branch lands in `C_1 \ Win_2` (no spare reply left, as `b_2` in Witness 2), extract the minimal round-2 losing suffix `(e_1*, e_2*)` and add a truthful example to `D` that shifts that branch's trajectory into `C_1 ∩ Win_2` rather than enlarging `W`.
- **Novelty vs nearest prior art:** Joins [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 16 (counter-strategy trees) and [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 01 (rejected-edit witnesses) with trajectory shaping (`#168`). Unlike [SpecRepair](https://arxiv.org/abs/2106.01917) and 1-step CEGIS, the counterexample repairs a *future* branch's loss of a spare reply while today's accuracy and round-1 safety already pass.
- **Cheapest first test:** Plant 4 first-round ties where 2 branches enter dead-end corners in a 2-round ReLU game. Compare terminal-error replay, 1-step refusal repair (`#166`), exhaustive search (ceiling), and losing-suffix trajectory shaping at equal verifier calls.
- **Old-task retention check:** Re-verify A, C, and B across *all* branches and all legal edits (not only the extracted losing suffix) after updating `D`, confirming no displaced refusal breaks an earlier branch.

#### 04. Guarantee a spare reply during the transient before corridor entry (P)
- **Mechanism:** When a foreign edit can arrive *before* diverging B branches merge at step `τ` (live-serving regime), require every transient reachable set `R_t` (`t < τ`) to lie inside a transient winning set `Win_1^{trans}(M)` with a verified reply, pricing transient reply capacity alongside transient buffer bytes.
- **Novelty vs nearest prior art:** [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 07 accounts for passive transient buffer bytes and [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 04 splits live vs atomic commits; neither requires a verified spare reply *mid-funnel* before branches converge.
- **Cheapest first test:** Vary arrival time `t_edit ∈ {1, …, τ}` of a blind edit in the Witness 2 host. Compare atomic-only corridors, passive transient cover (`#168#07`), and live-reply transient funnels on admitted early edits and total bytes.
- **Old-task retention check:** Audit A/C at every prefix `t < τ` both before and after an early edit arrives, ensuring no branch sacrifices early safety to buy faster corridor entry.

#### 05. Export a corridor port bundled with its certified spare-reply menu (P)
- **Mechanism:** Publish `(C, W, R̂(C), M_C)` as one checkable artifact: a later independent learner with a blind B family proves only that its own trajectory enters `C` by `τ` and inherits *both* the substitution buffer `W` and the residual spare-reply guarantee `R̂(C)` without re-solving the K-round game.
- **Novelty vs nearest prior art:** Combines [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 14 (public entry ports) with [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 08/12 (residual menus / [Pacti](https://arxiv.org/abs/2303.17751) contract quotients). Primitive candidate only if entry-only checking admits blind later writers at strictly lower verification work than full recertification + fresh game synthesis.
- **Cheapest first test:** Freeze `(C, W, R̂(C), M_C)`, then reveal a held-out second B family designed blind. Compare full recertification + fresh game solve, Pacti relational composition fed the same offers, and entry-only port reuse on verifier work and admitted blind editors.
- **Old-task retention check:** Audit A, C, and the new B family after overwrite and after a held-out round-2 edit; any writer failing entry must be refused and charged.

#### 06. Measure the free winning corridor before spending examples (I)
- **Mechanism:** For any host and branch family, compute the earliest step at which unshaped SGD branches naturally share a region inside `Win_K` (an [LMC](https://arxiv.org/abs/1912.05671)-style spawn point for winning kernels) and compare against rigid baselines (freezing, low LR, EWC stiffness) at matched B progress.
- **Novelty vs nearest prior art:** Direct combination of [PR #168](https://github.com/manojbajaj95/cl/pull/168) cards 06 and 21 applied to `Win_K`; mandatory audit so AGR1 cannot claim wins that SGD or rigidity supplies for free.
- **Cheapest first test:** Sweep naturally convergent vs persistently branching 2-unit and 4-unit ReLU hosts; plot admitted K-round edits and proof bytes vs B progress for unshaped waiting, rigid stiffness, and `D`-shaped corridors.
- **Old-task retention check:** Score A/C across the entire waiting window; natural waiting is only a valid baseline when old floors hold throughout.

### Common replies for probe-indistinguishable edits (AGR4)

#### 07. Teach-to-merge belief classes so one common reply covers indistinguishable edits (P)
- **Mechanism:** Partition the declared edit family `T` by its probe transcript `y = P(e(s))` into classes `[y]_P`. Select truthful today-examples `D` that move the host state so every class `[y]_P` admits a *single* verified reply `a(y) ∈ M` covering every `e ∈ [y]_P`, even when a full-information policy would choose different moves for different edits in `[y]_P`.
- **Novelty vs nearest prior art:** Directly develops AGR4 and Witness 1. Belief-state safety games ([0706.2619](https://arxiv.org/abs/0706.2619)) and conformant planning ([1401.3468](https://arxiv.org/abs/1401.3468)) solve for `a(y)` on a *fixed* transition system; [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 07 poses partial observation without using today's truthful data to collapse belief splits. The candidate primitive is using training data to make a hidden edit distinction irrelevant to the accommodation.
- **Cheapest first test:** Implement Witness 1 and a 4-gate ReLU host with 4 pairs of probe-indistinguishable edits. Compare full-info per-edit planning (ceiling), belief-state solver (`0706.2619`) on the unshaped state, naive probe-conditioned repair, and `D`-shaped common-reply training at fixed `P` and `M`.
- **Old-task retention check:** Verify A and C on *every* edit inside each transcript class `[y]_P` (including planted worst-case twins); a class with no verified common reply must refuse rather than guess.

#### 08. Price teaching examples against distinguishing probes (data-for-sensing exchange rate) (P)
- **Mechanism:** For each ambiguous transcript class `[y]_P`, compute two costs to make it winnable: (a) the truthful example budget `Δ|D|` needed to reshape the host so one common reply `a(y)` works, versus (b) the probe budget `Δ|P|` needed to split `[y]_P` into smaller classes with separate replies. Choose the cheaper operation per class.
- **Novelty vs nearest prior art:** Active sensing / value of information in POMDPs trades measurement cost against action cost; here the novel lever is spending *training examples today* to eliminate a *future measurement* altogether.
- **Cheapest first test:** In a 4-gate ReLU host with 3 hidden coordinates and a bank of unit-cost probes and unit-cost truthful examples, map the Pareto frontier of `(examples spent, probes spent)` for 100% certified admission across all pairs; compare probe-only, data-only, and joint selection.
- **Old-task retention check:** Hold A/C floors and B utility strictly matched across all points on the frontier; verify that saving a probe never comes from silently lowering new-task progress.

#### 09. Co-design the probe set `P` and today's shaping examples `D` under one evidence budget (P)
- **Mechanism:** Jointly pick a small probe set `P` (to separate edits whose safe reply sets are geometrically disjoint) and a truthful example set `D` (to unify edits whose safe reply sets can be made to overlap), optimizing certified multi-round admission at a fixed total `(probe + example)` budget.
- **Novelty vs nearest prior art:** Active probing (e.g., L\*-style queries in [PR #104](https://github.com/manojbajaj95/cl/pull/104)) picks probes for a fixed model; data selection picks examples for a fixed probe. Co-designing them tests whether a strict interaction exists beyond running probe selection and data selection independently.
- **Cheapest first test:** 4-gate ReLU host with 2 separable edit pairs (one mergeable by `D`, one fundamentally disjoint). Compare probe-selection-only, `D`-selection-only, sequential (pick `P` then `D`), and joint `(P, D)` selection at fixed budget `|P| + |D| = 2`.
- **Old-task retention check:** Score A/C on independent held-out probes never included in `P`, ensuring `P` is not overfitted to the retention test set.

#### 10. Certify common replies over the full footprint-counterfeit fiber (P)
- **Mechanism:** For any observed transcript `y = P(e(s))`, define the counterfeit fiber `F_P(y) = { e' ∈ T : P(e'(s)) = y }` using [PR #107](https://github.com/manojbajaj95/cl/pull/107)'s nullspace construction (`Pv = 0, Ov ≠ 0`), and verify `a(y)` over the entire bounded fiber (via interval/LP bounds) rather than only over finite sample edits in `[y]_P`.
- **Novelty vs nearest prior art:** [PR #107](https://github.com/manojbajaj95/cl/pull/107) proved that linear probes admit retention counterfeits; [Interval Bound Propagation](https://arxiv.org/abs/1810.12715) and [Certified CL](https://arxiv.org/abs/2407.06697) certify over input/weight boxes. Certifying a single reply `a(y)` across the *probe-nullspace fiber* turns PR #107's impossibility result into a sound design constraint.
- **Cheapest first test:** Use PR #107's 4-feature counterfeit witness extended with a 2-move reply menu `M`. Compare sample-only common-reply fitting, norm-ball robust training, and exact fiber-certified common replies against adversarial unseen counterfeits `e + v` with `Pv = 0`.
- **Old-task retention check:** Audit A/C on both natural edits and adversarial nullspace counterfeits `e + v` at matched edit norm and new-task gain; zero counterfeits may slip past `a(y)`.

#### 11. Sound belief-class splitting: buy a probe only after proving no common reply exists (I)
- **Mechanism:** Run a two-stage fail-closed admission loop: (1) check whether `[y]_P` admits a verified common reply `a(y) ∈ M`; (2) only when a sound infeasibility certificate proves no common reply exists, select the single probe `p*` minimizing worst-case post-split failure and re-verify both child classes, refusing if budget is exhausted.
- **Novelty vs nearest prior art:** Contingent planning with lazy sensing ([1909.13778](https://arxiv.org/abs/1909.13778)) and CEGIS-style counterexample splitting; improvement/control algorithm that operationalizes AGR4's fallback rule cleanly.
- **Cheapest first test:** 4-gate ReLU host with 8 edit classes (4 mergeable, 4 requiring 1 extra probe). Compare always-probe (eager sensing), random probe fallback, and infeasibility-triggered lazy splitting on total probe queries and admission rate.
- **Old-task retention check:** Confirm that an incomplete/timed-out common-reply search never triggers an unverified reply and that every refused class leaves A/C untouched on the live host.

#### 12. Publish belief-intersected residual menus after a common reply (P)
- **Mechanism:** When the host answers an unresolved transcript class `[y_1]_P` with a common reply `a(y_1)`, it still does not know which `e_1 ∈ [y_1]_P` occurred. Publish the *belief-intersected* residual menu `R̂_{obs}(y_1) = ∩_{e_1 ∈ [y_1]_P} Res(a(y_1)(e_1(s)))` so round-2 blind editor `E_2` commits safely without ever resolving round 1's hidden identity.
- **Novelty vs nearest prior art:** Generalizes [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 08's state-indexed Brzozowski residual `Res(s_1)` to a *belief-set* residual `Res(B_1)` (intersection over consistent states). Primitive candidate only if `R̂_{obs}` stays non-empty and beats forcing a round-1 distinguishing probe + state-indexed residual at equal total cost.
- **Cheapest first test:** Extend Witness 2 to publish `R̂_{obs}(y_1)` after round-1 `a_both` and test 8 frozen round-2 candidates. Compare forced round-1 probing + state residual, scalar remaining-margin rules, and belief-intersected residuals.
- **Old-task retention check:** Verify every `e_2 ∈ R̂_{obs}(y_1)` against *every* hidden round-1 realization `e_1 ∈ [y_1]_P` on A, C, B, and `E_1` floors; zero false admissions allowed.

#### 13. Multi-round conformant corridors without belief collapse (P)
- **Mechanism:** Ask whether a shaped corridor `C` can support `K ≥ 2` consecutive rounds of probe-indistinguishable edits using only observation-history replies `a_k(y_1, …, y_k)` while keeping the *entire growing belief set* `B_k` inside a single certified witness region `C`, without ever collapsing `B_k` to a singleton.
- **Novelty vs nearest prior art:** Conformant planning ([1401.3468](https://arxiv.org/abs/1401.3468)) and belief-space funnels in robotics; in CL the question is whether belief diameter grows exponentially with `K` (killing conformant play after 1 round) or can be contracted by `D` and `M`.
- **Cheapest first test:** Run `K = 1, 2, 3, 4` rounds on a 4-gate ReLU host with 2 indistinguishable edit directions per round. Measure belief-set diameter, residual menu size, and admission rate with vs without `D`-shaping and contraction (`#168#03`).
- **Old-task retention check:** Score worst-case A/C across all `2^K` hidden edit histories consistent with `(y_1, …, y_K)` at every round `k ≤ K`.

### Where AGR1 and AGR4 reinforce or collide

#### 14. Dual-control common replies that reveal hidden edit state for round 2 (P)
- **Mechanism:** When two round-1 common replies `a(y_1), a'(y_1) ∈ M` both keep every `e_1 ∈ [y_1]_P` safe today, prefer the reply `a*(y_1)` whose post-reply states `a*(e_1(s))` become *distinguishable* under the existing fixed probe `P` on round 2 (active dual control via the accommodation move, paying zero extra probe queries).
- **Novelty vs nearest prior art:** Dual control (Feldbaum 1960) and active perception in POMDPs use control inputs to gather information; here the "control" is a verified CL accommodation move `a ∈ M` that simultaneously repairs old tasks and rotates hidden edit differences into `row(P)`.
- **Cheapest first test:** Build a 2-round ReLU host where `a_1` keeps hidden edits `e_1, e_2` indistinguishable at round 2 (`P` stays blind) while `a_2` (same cost, same round-1 safety) shifts a ReLU gate so `P` separates them at round 2. Compare myopic common-reply selection, buying an extra probe, and dual-control common-reply selection.
- **Old-task retention check:** Verify A, C, B, and `E_1` floors for both `e_1` and `e_2` immediately after `a*(y_1)` and after round 2; dual control must never trade round-1 safety for information.

#### 15. Collapse old-task damage onto one reply direction while preserving distinct new-task writes (P)
- **Mechanism:** Shape today's state with `D` so two probe-indistinguishable edits `e_1, e_2` can still install *different* useful new-task behaviors in B's output coordinates while their side effects on old tasks A/C align along a single shared damage vector that one common reply `a(y)` cancels.
- **Novelty vs nearest prior art:** Directly addresses Vacuity 2 (over-hedged / erased-edit common replies) by combining [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 02 (obligation quotient) with AGR4. Distinct from orthogonal projection (GPM/OGD), which forbids damage altogether rather than aligning unavoidable damage onto one shared repair axis.
- **Cheapest first test:** 4-unit ReLU host where `e_1` and `e_2` write distinct new-task features and share transcript `y`. Compare OGD/GPM (blocking damage), unshaped common replies, and damage-aligned `D`-shaping on *both* new-task accuracy of `e_1, e_2` and A/C retention after `a(y)`.
- **Old-task retention check:** Check A/C on rare slices *and* verify that `e_1` and `e_2` still achieve their distinct target accuracies after `a(y)` runs (a reply that erases `e_1`/`e_2` to save A fails).

#### 16. Unify branch uncertainty (AGR1) and editor uncertainty (AGR4) into one product belief corridor (P)
- **Mechanism:** When the host observes only `P`, it may be uncertain both about *which past B training branch* `b` produced `s` and *which foreign edit* `e` just arrived. Treat `(b, e)` pairs producing the same probe transcript `y = P(e(s_b))` as one joint belief class and train `D` so a single verified reply `a(y)` covers the product uncertainty.
- **Novelty vs nearest prior art:** Unifies AGR1 (branch uncertainty across training orders) and AGR4 (edit uncertainty across opaque foreign writes) into a single observation-based invariant. Neither `#167` nor `#168` treats mixed `(branch, edit)` ambiguity.
- **Cheapest first test:** Combine 2 B orders (`b_1, b_2`) with 2 foreign edits (`e_1, e_2`) under one scalar probe `P` so `(b_1, e_2)` and `(b_2, e_1)` share transcript `y`. Compare separate branch-merging + edit-probing, joint `(b, e)` common-reply shaping, and full-info planning.
- **Old-task retention check:** Audit all 4 `(b, e)` combinations on A, C, B, and `E_1`, including rare slices and prefixes before `τ`.

#### 17. Belief-safe replenishment: restore spare replies without knowing which gate eroded (P)
- **Mechanism:** Lift [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 06 (costed re-buffer move into `Win_∞`) to partial observation: include a belief-safe re-buffer move in `M` that restores dormant gate thresholds across *every* state in `[y]_P` without changing current A/C/B outputs and without needing to know which specific gate the opaque edit consumed.
- **Novelty vs nearest prior art:** Combines viability kernels under imperfect information with `#167#06`'s re-buffer move; tests whether blind replenishment can prevent finite-horizon exhaustion at fixed capacity, or whether blindness forces too much wasted capacity per refresh.
- **Cheapest first test:** 6-round stream on a 4-unit ReLU host with probe-indistinguishable edits and a costed re-buffer move in `M`. Compare fixed-horizon `Win_2^{obs}`, belief-safe `Win_∞^{obs}` replenishment, periodic full probing + state replenishment, and frozen expansion at equal capacity.
- **Old-task retention check:** Verify A, C, and a sliding window of installed edits at every round across all consistent hidden histories; verify the re-buffer move preserves all old outputs exactly.

#### 18. Common replies across probe-blind optimizer fossils (I)
- **Mechanism:** Two edits or B branches that match on forward probe transcripts `P` can leave different Adam/momentum buffers ([PR #136](https://github.com/manojbajaj95/cl/pull/136), [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 18, [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 19). Test whether a common reply `a(y)` verified on weights alone breaks after one subsequent momentum step, and whether momentum-damping examples in `D` or explicit slot-reset moves in `M` close the gap.
- **Novelty vs nearest prior art:** Audit extending `#167#18` and `#168#19` to partial observation, where forward probes are structurally blind to optimizer slots.
- **Cheapest first test:** Match weights and forward probe transcripts across two branches while varying momentum sign; run one Adam step after `a(y)` and compare weight-only `Win_2^{obs}`, momentum-aware `Win_2^{obs}`, and explicit optimizer reset in `M`.
- **Old-task retention check:** Score A/C at the post-reply overshoot step (not only immediately after `a(y)`), flagging any silent breach caused by hidden slot state.

### Audits, lower bounds, and compile-away controls

#### 19. Compile it away into belief-state contingent planning (I)
- **Mechanism:** Give an off-the-shelf antichain imperfect-information safety solver ([0706.2619](https://arxiv.org/abs/0706.2619)) or conformant/contingent planner ([1401.3468](https://arxiv.org/abs/1401.3468), [1909.13778](https://arxiv.org/abs/1909.13778)) the unshaped host state, the exact same `P`, the exact same `M`, and active-sensing probes at equal evidence cost. If it matches admission and total cost, `D`-shaping adds no new CL primitive.
- **Novelty vs nearest prior art:** Direct partial-observation counterpart of [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 19 and [PR #168](https://github.com/manojbajaj95/cl/pull/168) card 22; mandatory compile-away control from the idea ledger.
- **Cheapest first test:** Run both arms on Witnesses 1 & 2 and a 4-gate ReLU host with identical `P`, `M`, and total compute/evidence budget; measure admitted useful edits, bytes, and verifier work.
- **Old-task retention check:** Enforce identical A/C floors at every served prefix and every hidden edit realization; a tie at matched scope demotes the node from primitive to objective choice.

#### 20. Measure the price of blindness (over-hedging tax vs full-info replies) (I)
- **Mechanism:** Quantify how much new-task utility, residual menu volume, and multi-round horizon `K` are lost when replacing full-info per-edit replies `a(e)` with a single common reply `a(y)` across `[y]_P`, separating genuine ambiguity-immunity wins from over-hedged replies that silently burn twice the budget.
- **Novelty vs nearest prior art:** Price of anarchy / value of information audit; prevents AGR4 from claiming success on rounds where common replies only work by destroying future capacity.
- **Cheapest first test:** On a 4-gate ReLU host, sweep probe granularity `|P| ∈ {1, 2, 3, 4}` from fully blind to fully observable; plot admitted rounds `K`, residual volume, and new-task utility against `|P|` with and without `D`-shaping.
- **Old-task retention check:** Hold A/C floors identical across every `|P|`; report the exact `|P|` threshold where `D`-shaping stops beating one extra probe.

#### 21. Construct an impossibility witness where no truthful `D` creates a common reply (I)
- **Mechanism:** Build a minimal ReLU host where two probe-indistinguishable edits `e_1, e_2` have *disjoint* safe reply sets under every legal A-consistent state (`Win_1^{obs}(P, M) = ∅` while `Win_1^{full}(M) ≠ ∅`). Demand a sound infeasibility certificate forcing either a distinguishing probe or honest refusal.
- **Novelty vs nearest prior art:** Negative control parallel to [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 22 and [PR #107](https://github.com/manojbajaj95/cl/pull/107); proves that teaching examples cannot universally replace probes and tests whether methods fail closed.
- **Cheapest first test:** Tighten `M` in Witness 1 by removing `a_both` (leaving only `{a_1, a_2}` with fixed cap `1/2` and bounded threshold room); verify that every legal `D` fails `Win_1^{obs}` and compare fail-closed certification against heuristic shaping.
- **Old-task retention check:** Confirm A/C remain at acquisition floors on the unchanged live host and zero uncertified common replies are ever published.

#### 22. Freeze demand, probes, and menu to audit silent curation and refusal honesty (I)
- **Mechanism:** Lock the editor bank `T`, probe set `P`, reply menu `M`, and truthful example pool identically across every arm; verify that (a) no shaping method wins by steering editors away from hard edits (curating demand), and (b) every ambiguous transcript without a verified common reply or affordable split is honestly refused.
- **Novelty vs nearest prior art:** Experimental fairness audit combining [PR #166](https://github.com/manojbajaj95/cl/pull/166) card 21 (uncurated demand) and [PR #167](https://github.com/manojbajaj95/cl/pull/167) card 20 (menu inflation).
- **Cheapest first test:** Run all AGR1/AGR4 arms on a frozen blind editor bank with 25% planted infeasible ambiguous pairs; report false-accept rate (must be 0%), refusal rate, and admission on the feasible 75% separately.
- **Old-task retention check:** Independently audit A, C, B, and all installed edits after every admitted round; any false admission on a planted infeasible pair kills the arm immediately.

## Ranked deeper questions

1. **Can today's truthful examples strictly replace a future distinguishing probe without over-hedging?** Start from Witness 1 and cards 07, 08, 10, 15, and 20 against the compile-away control (card 19). Ask whether `D`-shaping creates a verified common reply `a(y)` across a genuine `row(O) ⊄ row(P)` blindness gap (including nullspace counterfeits) while keeping distinct new-task utility for `e_1, e_2` and beating active probing + belief-state planning (`0706.2619`) at equal total evidence cost. If buying one extra probe always dominates shaping `D`, AGR4 collapses to active sensing.
2. **Does steering future branches into `C ∩ Win_K` beat stacking return corridors and accommodation games?** Start from Witness 2 and cards 01–04 against the free-corridor and rigidity audits (card 06). Ask whether `C ∩ Win_K` selection avoids dead-end safe corners and lowers total bytes + verification work compared to running `#168#01` and `#167#01` sequentially on the exact same `M`, with live-serving A/C floors held at every prefix including transients `t < τ`.
3. **Do belief-intersected residual menus and multi-round common replies survive beyond round 1 without belief explosion?** Cards 12, 13, 14, and 17 test whether an unresolved round-1 transcript class `[y_1]_P` can sustain `K ≥ 2` rounds—via belief-intersected residuals, dual-control replies that rotate hidden differences into `P`, or belief-safe replenishment—or whether uncertainty compounds so fast that every practical learner must force a distinguishing probe after round 1.
4. **Can one public corridor port bundle both a shared witness proof and a partial-observation spare-reply guarantee for blind later writers?** Cards 05, 16, and 18 ask whether `(C, W, R̂_{obs}(C), M_C)` composes across independently authored blind B families (including hidden optimizer-state divergence) at lower total verifier work than full recertification + fresh game synthesis, which is the threshold separating a reusable CL primitive from a training-time objective.
