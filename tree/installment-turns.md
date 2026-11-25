# Installment turns and next-bottleneck refills

**Status:** Ideas only; no learner training or GPU work. **Parent:** [Momentum-steering records and weakest-alias refills](momentum-steering.md) ([PR #250][parent]), cards 04 and 12. **Review seed:** [Flood triage, row 365][triage] scored both ideas 3: turn inherited momentum through truthful records under a decayed norm cap at every prefix, with only the last required to land the seal; and track the state that will limit tomorrow's allowance, not only today's worst. **Read first:** [Idea ledger][ledger].

## Can truthful records deliver a turn in stages and leave room for the next correction?

**Verdict: two feasibility separations, no established primitive.** A two-record word can land when no legal singleton lands and when passive coast misses the same deadline. A refill can win on today's worst alias, mean and minimum and still lose on the next declared correction, because a different alias binds. Neither separation beats exact finite-horizon robust control. Look for a reusable certificate that preserves its decisions more cheaply, or more safe admissions at the same all-in budget.

**Nearest prior art.** [Entry words][sealed] already search over real records, and [GradMatch][gradmatch] already selects real examples to match a gradient. Compare against both: the target here is the reachable *slot and weight path*, including intermediate old-task service, not gradient matching at the start or just sealing at the end. [GEM][gem] modifies the executed gradient; using the host's unmodified updates makes it a useful control, not the claimed operation. [Robust MPC][mpc] already optimizes over possible states and future constraints; [history-aware barriers][barriers] already budget excursions. A moving bottleneck is not itself novel. The question is whether the structure of truthful update sequences allows a smaller public certificate than a general robust solver on the same observations and record pool. These are scoped comparisons, not priority claims. The ledger's bounded-delay scheduling kill makes equal-deadline accumulation a required control where legal; the plasticity-reserve and forecast-weighted-write failures make **absolute** incoming C gain and old-task retention required matches, not optional diagnostics.

## Contract and falsifiers

- Fix the host, optimizer and schedule, old tasks A/B and installed C, incoming C witness and utility floor, legal labeled pool and batching rules, public observations, reads, horizons and deadlines. Records are verified ordinary training examples or lawful batches, billed once, not synthetic gradients or zero-gain recharge. Use separate held-out old-task tests; gate proxies are not sufficient. A failed prefix cannot be erased from the service report by eventual success.
- At stage `i`, propagate the whole fiber of possible joint states. For heavy-ball, `p_i = βm_{i−1}`, `m_i = p_i + g_i`, `w_i = w_{i−1} − m_i`. Require `||m_i|| ≤ ||p_i||` on every alias at every update. Preregister any stricter cap, norm and scheduler; a later reset is not decay and is only a control. If no sound fiber bound exists, refuse. A common word may be chosen up front; contingent variants must precommit branches keyed only to public observations and certify every branch they leave possible. Every served prefix must meet the old-task envelope. Only the final record must land the seal, including its coast bound; don't report the binding as sealed early. If normal service can interleave, declare its maps rather than silently pausing it.
- When already sealed, track slack for each alias and face through each refill and each declared next request, including the zero-gradient coast and ordinary intermediate service. An earned refill must be useful and improve the current certified minimum strictly; among qualifying refills, distinguish the current minimum from the minimum *after the next request*. Keep alias identity along each path; a next gradient can depend on the state produced by the refill. If a request is uncertain, name the allowed request family and its information pattern; a forecast alone cannot authorize an unsafe debit. No unobserved alias may be removed to improve the score.
- Match records and absolute C gain, gradients and probes, certificate bytes and compute, wall-time and latency, and old floors. Compare single-turn [#242][landing], [#234][sealed] entry without the cap, reset plus best truthful plan, passive decay, accumulation when legal, and a direct slot write as an illegal ceiling. Don't force a zero-slot reset arm to meet the installment cap: enforce the same service and seal instead. For refills compare today's-worst, mean, one-step exact minimum, and finite-horizon exact robust control with identical inputs. Include a pool with no feasible installment and a fiber where the bottleneck never switches; report refusal, downtime and old-task failures separately.

## Exact sanity checks

These are rational heavy-ball examples with `β = 1/2` and unit step, checked with Python `fractions`, not evidence about natural record supply. A fixed record `(x,y)` gives `g = (x·w−y)x`. All intermediate zero-gradient coast points lie on the segment from `w` to `w−m`, so both endpoints suffice for the affine reads below. Singletons are the only legal batches in these fixtures.

**F1. The first record turns; the second seals.** Start `w=(0,0), m=(0,4)`. Seal requires `w₁ ≤ −17/10`, including the coast. The legal pool is `P=((1,−1),−1)`, `Q=((1/5,−2/5),−4/5)`.

| Step | Weights after step | Inherited norm squared `||p||²` | Resulting slot norm squared `||m||²` | Seal? |
|---|---|---:|---:|---|
| `P` | `(−1,−1)` | 4 | 2 | no |
| `P,Q` | `(−17/10,−11/10)` | 1/2 | 1/2 | yes |

The slot turns from `(0,4)` through `(1,1)` to `(7/10,1/10)`. `Q` alone reaches only `w₁=−4/25`; waiting in the second slot after `P` reaches only `−3/2` before the deadline. `Q,P` and `P,P` violate the cap at step two; `Q,Q` misses the deadline (second `w₁=−66/125`). Thus removing `P` gives a no-word control at horizon two. On the independent incoming read `w₁` with target `−17/10`, each prefix of `P,Q` improves absolute error. Toy old reads A (`w₁ ∈ [−5/2,0]`), B (`w₂ ∈ [−4,0]`), and installed C (`w₁+w₂ ∈ [−4,0]`) pass at entry, both prefixes and their coasts. The negative control is about the fixed deadline, not indefinite waiting.

**F2. The best refill now is unsafe for the announced next request.** Start `w=(−1,−1)` with aliases `U: m=(1/2,−1)`, `V: m=(−1/2,0)`. Both faces are `wᵢ ≤ 0`; alias allowance is `min_i(−max(wᵢ,wᵢ−mᵢ))`. Refill records are `X=((1,2),−9/2)` and `Y=((1,2),−4)`. The identical next debit `D=((1,1),−17/4)` is evaluated from each resulting state, not as a fixed impulse.

| History | U allowance | V allowance | Certified minimum |
|---|---:|---:|---:|
| entry | 0 | 1/2 | 0 |
| `X` | 11/4 | 9/4 | 9/4 |
| `Y` | 9/4 | 7/4 | 7/4 |
| `X,D` | 1/2 | −1/2 | −1/2 (refuse) |
| `Y,D` | 19/8 | 3/2 | 3/2 (admit) |

Both refills strictly improve the certified minimum and improve an independent incoming read `w₁+w₂` toward target `−8`. Today's worst, the uniform mean, and the exact immediate minimum all rank `X` first. `V` becomes the bottleneck after either refill; its coast after the forced `X,D` reaches `w₁=1/2` while `U` stays sealed. A held-out debit read `w₁−w₂` with target `3` improves under `D` on both aliases after either refill. Toy old reads A (`w₁ ∈ [−5,0]`), B (`w₂ ∈ [−7,0]`), and installed C (`w₁+w₂ ∈ [−21/2,0]`) pass after each admissible step and its coast; forcing `X,D` fails A. With only `U` there is no switch and both histories admit `D`. The two-record robust controller selects `Y`; incoming gains are not matched between `X` and `Y`, so this is a decision counterexample, not an outcome comparison.

## Idea cards

### A. Make the whole turn feasible

### 01. Compile an installment word — primitive candidate
**Mechanism.** Reserve a common sequence whose prefixes are norm-safe and serve old tasks, and require only its terminal state to seal. **Novelty / control.** Restates [#250][parent] card 04; compare cap-free [entry words][sealed], the single-record turn, accumulation and reset plus best legal word. **Cheapest first test.** F1, then enumerate the same horizon with the indispensable record missing. **Old-task retention.** Read A/B/installed C at each prefix and the final coast, including the prefix before the seal.

### 02. Certify the remaining turn with a suffix table — primitive candidate
**Mechanism.** Cache for a fixed suffix the set of entry `(w,m)` states from which every cap passes and the suffix seals. Reuse the table for different prefixes without equating their histories. **Novelty / control.** Backward reachability is standard [MPC][mpc]; the claim is amortized decisions from certificates attached to real suffixes, not faster search by assumption. **Cheapest first test.** Reuse two suffixes across a rational grid of prefixes; compare exact re-search and certificate bytes. **Old-task retention.** Include a suffix that seals but fails an old read between its records so it must not be cached as admissible there.

### 03. Spend a record only if the rollback-free stop is safe — primitive candidate
**Mechanism.** Every first installment has a public timeout branch that continues ordinary old service without the missing record, and without claiming the new binding sealed. **Novelty / control.** A robust fallback policy is standard; compare hold-and-recheck and a full checkpoint restore on the same service deadline, charging state and downtime. **Cheapest first test.** Drop the second record after a first installment with useful C gain but a near-edge B read. **Old-task retention.** Serve held-out A/B/installed C at timeout and during the fallback, not just once the normal word resumes.

### 04. Cross a real gradient boundary between installments — primitive candidate
**Mechanism.** Pick a prefix that changes which existing features the next example exercises, permitting a cap-safe suffix not available under either initial gradient. **Novelty / control.** Unlike static [gradient matching][gradmatch], the second gradient is evaluated after the first update; compare equal-deadline accumulation and exhaustive state-dependent word search. **Cheapest first test.** Two ReLU features and three records, with a frozen-feature ablation to destroy the advantage. **Old-task retention.** Probe an old classifier using the switched feature before and after it crosses and at terminal coast.

### 05. Give the turn a worst-case service clock — primitive candidate
**Mechanism.** Before opening, certify the word against a declared window of possible interleaved ordinary A/B updates, with the cap checked again on each installment's actual incoming slot. **Novelty / control.** Robust scheduling already composes disturbance maps; compare exact robust scheduling, pause-and-resume, and per-step recertification. **Cheapest first test.** Insert one fixed-label old batch at either of two positions; require at least one nontrivial accepted word and one position-dependent rejection. **Old-task retention.** Execute held-out A/B/installed C at both service positions, counting delayed reads against their deadlines.

### 06. Branch on a real observation, not a hidden slot — primitive candidate
**Mechanism.** After the first record, use an ordinary public read to choose a pre-certified suffix for the remaining aliases; certify an indistinguishable branch as a union. **Novelty / control.** Belief-space [MPC][mpc] already branches on observations; test whether a read the host already serves can replace an expensive probe at equal reliability. **Cheapest first test.** Two slots with opposite useful suffixes; compare visible and rounded-to-identical reads. **Old-task retention.** Hold out A/B/installed C examples distinct from the branch read and run them on both branches and the timeout.

### 07. Attach a non-commutation witness to a word — improvement
**Mechanism.** Record the first prefix at which a permutation or accumulated batch loses feasibility, separating cap failure, service failure and missed terminal seal. **Novelty / control.** The ledger already rejects generic bounded-delay reordering; compare legal accumulation, reversed order and a state-independent-gradient ablation before attributing a split to the path. **Cheapest first test.** Enumerate all orders of three records under the same deadline; check whether the split survives equal absolute C gain. **Old-task retention.** Compare per-item margin-matched old errors at the first differing prefix and at the terminal check.

### 08. Reserve joinable suffixes across independent record queues — primitive candidate
**Mechanism.** Reserve a common final record for distinct cap-safe prefixes from two verified queues, so either queue can supply the first installment without double-counting the closer. **Novelty / control.** [Finish menus][menus] reserve continuations; the added requirement is a shared truthful closer with compatible hidden-slot regions. Compare separate menus and exact scheduling at equal reservations. **Cheapest first test.** Two possible first records, one shared closer and one close-but-incompatible prefix. **Old-task retention.** Read A/B/installed C through either prefix and on a queue timeout, while the binding remains unsealed.

### 09. Test the cap in effective Adam coordinates — improvement
**Mechanism.** Propagate first moment, second moment and bias-correction time through every installment, certifying both raw-slot and effective-displacement caps against the matched no-record step. **Novelty / control.** [AdamW dynamics][adamwio] already tracks delayed effects; compare heavy-ball surrogates, first-moment-only approval, reset and the full robust Adam trace. **Cheapest first test.** Two denominators that agree at the first prefix but diverge enough at the second that one raw-safe word fails the effective cap. **Old-task retention.** Measure the old read on the small-denominator axis after each record, not just after sealing.

### 10. Distinguish lack of truthful supply from lack of optimizer capacity — improvement
**Mechanism.** Evaluate the same prefix obligations with successively broader action sets: legal singletons, legal batches, then bounded unrestricted updates as an illegal ceiling. **Novelty / control.** This is an obstruction audit, not a new optimizer. Compare a longer legal deadline and a reset at the same old-service budget before asking for more labels. **Cheapest first test.** Exhaust a small finite pool, then add one ordinary verified example where only the wider action set formerly succeeded. **Old-task retention.** Require the ceiling and the rescued legal plan to preserve the same A/B/installed C reads at each prefix.

### B. Follow the binding state through the next request

### 11. Refill for the next bottleneck — primitive candidate
**Mechanism.** Propagate the current fiber through each valid inward refill and the announced debit; score the worst resulting alias and face rather than the alias that binds now. **Novelty / control.** Restates [#250][parent] card 12; compare greedy worst-state and mean scores, one-step exact minimum, reset, and finite-horizon robust control. **Cheapest first test.** F2 and a no-switch single-alias control; next match independent C gain. **Old-task retention.** Probe A/B/installed C at the refill and debit and at the worst admissible coast point.

### 12. Save only the aliases that can still become limiting — primitive candidate
**Mechanism.** Drop an alias-face from the *minimum calculation* only if another bounds it from below throughout the declared refill/debit family; keep the underlying state in the public fiber. **Novelty / control.** Dominance pruning in [robust control][mpc] is standard; test whether record structure yields auditable pruning and savings over generic pruning. **Cheapest first test.** A six-alias toy where two are dominated throughout and another is dominated only today. **Old-task retention.** Query the old read most sensitive to the superficially dominated alias after the worst declared debit.

### 13. Store the crossing, not today's winning alias — primitive candidate
**Mechanism.** For ordered truthful batch strengths or fixed policy settings, bound where the lower envelope switches alias or face; label unresolved intervals as requiring exact replay. **Novelty / control.** Compare parametric robust optimization and simple top-k tracking; the useful object would be a reusable crossing certificate for a fixed record family. **Cheapest first test.** Sweep a finite rational batch menu; include two crossings where checking only endpoints misses the binding alias. **Old-task retention.** Read A/B/installed C around both sides of each crossing and at the worst interior point.

### 14. Track a bottleneck that changes face but not alias — improvement
**Mechanism.** Retain face and coast-time witnesses separately so tracking the right alias cannot hide a new limiting read. **Novelty / control.** Multi-constraint [barriers][barriers] already handle this; compare their exact minimum against an alias-only cache and a current-face rule. **Cheapest first test.** A single alias and an axis-aligned box with one refill that switches the binding axis after a diagonal debit. **Old-task retention.** Use different held-out old tasks on the two axes and check both at the update and coast.

### 15. Certify request classes by their effect, not gradient norm — primitive candidate
**Mechanism.** Partition incoming request records into classes with certified post-refill transition bounds, keeping distinct cases for state-dependent residual changes. **Novelty / control.** Compare [impulse accounting][landing] and exact scenario [MPC][mpc]; seek fewer checks without conflating requests that have the same raw norm but different effects. **Cheapest first test.** A fixed labeled pool where two requests have equal norm at entry but reverse their ranking after a refill. **Old-task retention.** Probe A/B/installed C for the extremal record in each admitted class and audit a boundary record left out of the class.

### 16. Give a refill a safe-until deadline — primitive candidate
**Mechanism.** Certify a band of waiting times for an announced debit, returning the first time at which a hidden alias can exhaust the allowance. **Novelty / control.** Timed reachability is standard; compare a fixed age penalty, robust timing search and recertification on arrival. **Cheapest first test.** Scan one to four idle steps from two slots and include a case where waiting helps one alias and hurts the other after the same debit. **Old-task retention.** Execute A/B/installed C at the first and last admissible arrival and check a refused late arrival in the simulator.

### 17. Ask which uncertainty would change the refill choice — primitive candidate
**Mechanism.** Only request an allowed diagnostic when resolving a specific alias pair would change a safe decision for an announced debit. Otherwise take the robust refill or refuse. **Novelty / control.** Decision-focused active sensing is old; compare information gain, one ordinary diagnostic then exact robust choice, and no diagnostic at equal latency. **Cheapest first test.** Three aliases, two probes: one resolves a harmless alias and the other resolves the crossing pair. **Old-task retention.** Account for retention and read latency while waiting for a probe, not just after a successful refill.

### 18. Prove a floor even if the forecast is wrong — primitive candidate
**Mechanism.** Among refills that certify a hard allowance floor for every declared request, optimize slack for the likely next request; do not spend forecast-weighted slack before the request is known. **Novelty / control.** Standard hard-constrained risk-aware [MPC][mpc]; the potential gain is a cheap reusable floor for real record choices, not a revived reserve predictor. **Cheapest first test.** Reverse a two-request forecast and check that only the optional objective changes. **Old-task retention.** Probe A/B/installed C on the forecast miss and at both safety-floor boundaries.

### C. Test the interaction, not just the components

### 19. Require the landing word to leave a usable next refill — primitive candidate
**Mechanism.** Aim the terminal slot at both the seal and the preimage of a certified refill for the announced request. **Novelty / control.** [#250][parent] card 21 reserves a truthful record; here the record remains available in all arms but is only feasible from some terminal joint states. Compare stacked best independent turn and refill, and joint robust search. **Cheapest first test.** Two equal-gain sealing words and one common refill; require only one word to leave the refill safe. **Old-task retention.** Check A/B/installed C across both words, after the refill and at the debit.

### 20. Audit where the installed turn changes the worst-case request — improvement
**Mechanism.** Keep the same declared request family across two sealing words and attribute any change of binding request to reachable joint state, swapping only the terminal slot in an illegal diagnostic arm. **Novelty / control.** A causal ablation, not a new policy; compare reset and a state-dependent weight-only model to isolate carry from different learned weights. **Cheapest first test.** Enumerate two words with matched terminal weights but distinct certified slots and two competing debit directions. **Old-task retention.** Verify A/B/installed C remain matched before the debits and test both counterfactual debits at their worst coasts.

### 21. Reuse the same certificate across different record pools — primitive candidate
**Mechanism.** Publish an entry-state region and a required update-effect region for a turn suffix or refill; verify that a later pool supplies a real record mapping the whole fiber into that region. **Novelty / control.** Contracts for transitions are standard; compare a fresh [GradMatch][gradmatch] search plus robust replay and full robust planning, counting certificate construction and failed queries. **Cheapest first test.** Small pools with different examples yielding the same qualified effect and an impostor that matches only the point gradient. **Old-task retention.** Recheck A/B/installed C at every accepted substitution, particularly on the alias the impostor would harm.

### 22. Measure safe service, not the number of seals — improvement
**Mechanism.** Count delivered old-task reads, useful new corrections, refusal and waiting cost on the same horizon; separate one-step wins from gains that survive several announced requests. **Novelty / control.** An evaluation, not a new selector. Compare invariant bottleneck and switching hosts, cap-free entry plus one-step refill, and the exact joint controller. **Cheapest first test.** Exhaust short repeated turn/refill/debit traces with and without switched binding constraints. **Old-task retention.** Report worst-prefix and terminal A/B/installed C performance at matched absolute incoming C gain, with interrupted service counted.

## Ranked deeper questions

1. **Do naturally available records give cap-safe installment words a genuine advantage at equal deadline?** Start with 01, 04, 05 and 07. Move from F1 to a shared-feature CPU host with real labels; compare same-record accumulation, best truthful opener, reset plus the best word, and cap-free entry. Retire the claim if equal-budget controls tie at matched absolute C gain and old-task service, or if useful qualifying words are too rare.
2. **Can a moving-bottleneck certificate match robust decisions at lower total cost?** Start with 11–16. Count certificate construction, bytes, refresh, and failed queries; compare exact robust control with identical information. Reject a shortcut that admits an unsafe unseen alias, and retire it if savings disappear on a held-out sequence or an invariant-bottleneck control does just as well.
3. **Can plans safely tolerate delayed records and wrong forecasts without pausing old service?** Combine 03, 05, 06 and 16–18. Prices for missed deadlines and probes must be explicit; a forecast miss or indistinguishable branch must never turn a provisional result into an unsound seal.
4. **Does selecting the landing word and next refill together unlock anything their stacked baselines cannot?** Use 19–22 and cross a cooperative host with one where the two stages compete over carry. Compare independent best controllers at the same budgets as well as joint exact search; require a retained, usable correction, not more nominal headroom.

[parent]: https://github.com/manojbajaj95/cl/pull/250
[landing]: https://github.com/manojbajaj95/cl/pull/242
[sealed]: https://github.com/manojbajaj95/cl/pull/234
[menus]: https://github.com/manojbajaj95/cl/pull/222
[triage]: https://github.com/manojbajaj95/cl/blob/489e6acf8d4acada424aa10385eb0382cd276da7/reviews/flood-triage.md#L365
[ledger]: https://github.com/manojbajaj95/cl/blob/489e6acf8d4acada424aa10385eb0382cd276da7/reviews/idea-ledger.md
[gradmatch]: https://arxiv.org/abs/2103.00123
[gem]: https://arxiv.org/abs/1706.08840
[mpc]: https://doi.org/10.1016/j.automatica.2004.08.019
[barriers]: https://arxiv.org/abs/2610.31525
[adamwio]: https://arxiv.org/abs/2608.19762
