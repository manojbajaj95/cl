# Gap-relocating installments: spend the first record on where the gap lands

**Status:** Ideas only; no learner training or GPU work. **Parent:** [Installment turns and next-bottleneck refills](installment-turns.md) ([PR #262][parent]), cards 04, 09 and 19. **Review seed:** [Flood triage, round 57][triage] kept ITS4 from [cross-pool round 57][its4] at score 3. ITS4 freezes the useful successor, then picks a truthful first record that moves the reachable leftover gap into the successor's certified damping region, even if the raw gap first grows. It respects the momentum cap and intermediate readers and checks the executed update after both stages. It joins #262 card 04, [gap handoffs][gaphand] cards 01/04 and [#261][norm] card 08 (next-denominator repair). **Read first:** [Idea ledger][ledger].

## Can a truthful opener make a frozen successor's damping apply to a gap it could not touch?

**Verdict: one exact feasibility separation in heavy-ball, no primitive yet.** In G1 below, the frozen successor `Q` is cap-illegal at entry, after a coast, and after itself. A truthful, useful opener `R` raises the squared slot gap between two paired histories (5/4 → 29/16). `R` then `Q` ends at 17/256 with a smaller weight gap. A wrong-direction opener `P` with the same raw gap leaves `Q` illegal. Two things stay unresolved. First, part of `R`'s job in G1 is to make `Q` admissible, not only to aim the gap. Second, G1 is quadratic, so the gap map is linear and independent of labels. That is matrix arithmetic, a [Kaczmarz][kaczmarz]-style projection sequence, not a learned property. The claim lives or dies where the opener crosses a real feature boundary (#262 card 04) and where the successor is adaptive (card 09).

**Nearest prior art.** [Shuffle-order noise from optimizer memory][shuffle] shows that equal-multiset orders differ at first order in the learning rate. [AdamW input-output dynamics][adamwio] and [delayed state transport][transport] measure how one minibatch acts through later updates. [OptiSelect][optiselect] scores data by its optimizer-shaped effect. [GraB][grab] balances gradient order. [Trajectory matching][mtt] fits later states. Backward reachability and funnel libraries ([Majumdar & Tedrake][funnels]) compose controllers whose outputs land in a successor's region of attraction. That last item is the closest structural match: ITS4 is "land in the next funnel" with truthful records as the only actuator. The open question is whether that actuator restriction, plus a frozen useful successor, gives a smaller certificate or more admissions than generic reachability, robust MPC, or batch reordering at equal work. These are scoped comparisons, not priority claims. Ledger rules that apply: bounded-delay reordering already died, so equal-deadline reordering and accumulation are required controls. The plasticity-reserve and forecast-write kills make absolute incoming C gain and old-task retention required matches. Merge cards must beat their parts' best stack.

## Contract and falsifiers

- **Paired histories, not injected slots.** Two writeback orders of the same A/B work give paired joint states `(w,m[,v,t])`, the aliases `U` and `V`. The gap is the difference between them. Report the slot gap, the weight gap and the next executed-update gap separately. A reset, slot rotation or direct write is a diagnostic ceiling, not a lawful arm.
- **Freeze `Q` first.** `Q` is a required, useful C batch with fixed records, delivery time and progress floor. Its *certified damping region* `D_Q` is the set of paired states from which `Q` is legal on both aliases (cap, readers) and leaves the declared gap below tolerance without growing the weight gap. Preregister `D_Q` from `Q` alone, before searching for openers.
- **The opener is truthful and pays for itself.** `R` is an ordinary verified record or lawful batch that improves its own loss on every alias. It is billed once and must satisfy `||m_i|| ≤ ||βm_{i−1}||` on every alias. The raw gap may grow after `R`. Every served prefix and its zero-gradient coast must pass the old-task envelope.
- **Recompute, don't transport.** Evaluate `Q`'s gradient at the weights `R` reaches on each alias. For adaptive hosts, score the executed update `Δu = Δ(m̂/(√v̂+ε))` after both stages, with clipping and bias correction live, not `Δm` alone ([#258][gaphand] H2).
- **Controls at matched absolute C gain, records, compute and deadline:** `Q` alone, `R` alone, `R` plus coast, waiting (decay), `Q,Q` accumulation, reversed order, best reordering of the same multiset, the [#248][compl] slot-gap handoff, the best stack of #262 card 04, #258 cards 01/04 and #261 card 08, exact joint optimization over the pool, a wrong-direction opener with equal raw gap, a gap the pool cannot move into `D_Q`, and a slot reset. Report refusals, downtime and old-task failures separately.

## Exact sanity check (not evidence of learning)

**G1 · An opener that grows the gap makes the frozen successor admissible and damping.** Heavy-ball with `β = 1/2`, unit step, `g = (x·w − y)x`, cap `||m'|| ≤ ||βm||`, Python `fractions`. Aliases: `U: w=(−1,0), m=(−1/2,−9/2)`; `V: w=(0,0), m=(0,−7/2)`. Entry gap `Δw=(−1,0)`, `Δm=(−1/2,−1)`: squared slot gap 5/4, squared weight gap 1. Pool: opener `R=((1,−1),1)`, frozen successor `Q=((3/2,0),1)`, wrong opener `P=((1/2,3/2),−2)`; coast is `g=0`.

| Arm | Legal (cap on both aliases)? | Squared slot gap | Squared weight gap | Own-loss change (U; V) |
|---|---|---:|---:|---|
| entry | — | 5/4 | 1 | — |
| `R` | yes | 29/16 (grows) | 5/16 | 4→0; 1→9/16 |
| `R,Q` | yes, yes | **17/256** | **169/256** | `Q`: 49/64→361/1024; 1/4→1/64 |
| `Q` | no (refused) | — | — | — |
| coast, `Q` | `Q` refused | — | — | — |
| `Q,Q` / `Q,R` | refused at step 1 | — | — | — |
| `R,R` | refused at step 2 | — | — | — |
| `R`, coast | yes | 29/64 | 85/64 (grows) | no C work at step 2 |
| `P` | yes | 29/16 (equal to `R`) | 29/16 | 9/4→25/16; 4→9/64 |
| `P,Q` | `Q` refused | (73/32 if forced) | (137/32 if forced) | — |
| slot reset (illegal) | — | 0 by fiat | 1 | — |

End states after `R,Q`: `U: w=(17/16,3/8), m=(3/16,−1/8)`, `V: w=(3/4,9/8), m=(1/4,−3/8)`. Toy old reads A (`w₁ ∈ [−1,3/2]`), B (`w₂ ∈ [−1/2,3/2]`) and installed C (`w₁+w₂ ∈ [−1,2]`) pass on both aliases at entry, after each step, and at the final coast endpoint. The `R,Q` path stays in `w₁ ∈ [−1,5/4]`, `w₂ ∈ [0,21/16]`, `w₁+w₂ ∈ [−1,31/16]`. The tolerance `≤ S₀/16 = 20/256` is met only by `R,Q`.

What it shows: the slot gap alone does not rank openers. `P` and `R` tie on raw gap, but only `R` lands where `Q` is legal and damping. Waiting after `R` shrinks the slot gap less and grows the weight gap. What it does not show: it does not show that natural record pools supply such openers, and it says nothing about adaptive updates. Because the gap map is label-independent and linear here, the real question is whether this survives ReLU boundaries and Adam denominators. Incoming C gain is not matched across arms, so G1 is a decision counterexample, not an outcome comparison.

## Idea cards

### A. Find the landing

### 01. Aim the opener at the frozen successor's damping preimage — primitive candidate (ITS4)
**Mechanism.** Preregister `D_Q` from the frozen `Q`, then choose the truthful record whose paired image enters `D_Q` while staying cap-safe and old-safe, even if the raw gap grows. **Novelty vs nearest prior art.** Funnel composition ([Majumdar & Tedrake][funnels]) lands controllers in a successor's region; here the only actuator is a truthful record, and the successor must stay frozen and useful. **Cheapest first test.** G1, then a 2-feature ReLU regression with real labels. Enumerate all singletons and pairs and compare against best reordering, `Q,Q`, `R`+coast and exact joint search at matched C gain. **Old-task retention.** Read A/B/installed C on both aliases after `R`, after `Q` and at both coasts. Reject any landing that passes only at the endpoint.

### 02. Separate admission from aim — improvement
**Mechanism.** Split the opener's effect into "makes `Q` legal" (cap and reader slack) and "moves the gap into `Q`'s contracting directions". Swap in an illegal-cap diagnostic arm to see which matters. **Novelty vs nearest prior art.** An attribution audit of G1-style wins against [#262][parent] card 10 (supply vs capacity). **Cheapest first test.** Rerun G1 with the cap lifted: does `Q` from entry or after `P` then contract? (Forced `P,Q` gives 73/32, so in G1 aim matters too.) **Old-task retention.** Check that lifting the cap does not change which arms pass the A/B/C reads; if it does, the reads, not the gap, decide.

### 03. Relocate across a real ReLU boundary — primitive candidate (#262 card 04 × ITS4)
**Mechanism.** The opener changes which existing units `Q`'s records activate, so `Q`'s paired Jacobian, not just its input, changes; land the gap in the new cell's damping region. **Novelty vs nearest prior art.** A quadratic host makes the landing linear algebra; a cell change makes the successor's damping depend on the opener, which reordering, GradMatch and Kaczmarz cannot express. **Cheapest first test.** Two hidden ReLUs, three records; a frozen-mask ablation must destroy the win. **Old-task retention.** Probe an old classifier that uses the switched unit before and after the crossing, and at the coast.

### 04. Certify the landing in executed Adam updates — primitive candidate (#262 card 09)
**Mechanism.** Define `D_Q` on the executed adaptive update after `Q`: first moment, second moment, bias correction, ε and clipping. Choose the opener so both `Δm̂` and the denominator gap land where `Q`'s update difference is small. **Novelty vs nearest prior art.** [AdamW IO dynamics][adamwio] measures delayed minibatch effects; [#258][gaphand] H2 shows equal numerators can still give unequal updates. Here the opener is chosen against the successor's executed update. **Cheapest first test.** Scalar Adam with `β₁=β₂=1/2`: find openers that zero `Δm` after `Q` but not `Δu`, and the reverse. Use exact surds or a 50-digit decimal. **Old-task retention.** Read the small-denominator old coordinate after `Q` and at the next ordinary update.

### 05. Spend the opener on the next denominator, not today's gap — primitive candidate (#261 card 08 × ITS4)
**Mechanism.** Let `R`'s squared gradients shape `Δv` so that `Q`'s gain difference stops amplifying the residual first moment. Raw `Δm` may stay. **Novelty vs nearest prior art.** [#258][gaphand] card 11 splits moment repair across P/Q; here one opener prepares the denominator for a frozen useful `Q`. **Cheapest first test.** Cross "opener aims `Δm`" with "opener aims `Δv`" at an equal record budget, and test the 2×2 against a joint executed-update objective. **Old-task retention.** Probe A on the coordinate whose `v` the opener inflates; a quieter old update can still be a wrong one.

### 06. Steer the weight gap that the successor turns into slot damping — primitive candidate (#258 card 04)
**Mechanism.** The opener's job is the *weight* gap: `Q`'s curvature converts `Δw` into forcing that cancels `Δm`. In G1, `R` flips `Δw` from `(−1,0)` to `(1/4,−1/2)` so that `Q`'s `x xᵀΔw` term opposes `βΔm`. **Novelty vs nearest prior art.** [#258][gaphand] card 04 uses a weight gap as carrier; here the opener writes it and `Q` is fixed. **Cheapest first test.** Enumerate openers at equal `Δm` image but opposite `Δw` image; recompute `Q` on both. **Old-task retention.** Keep a weight-sensitive A read live after `R`; a carrier the old read hears is refused.

### 07. Use the equal-gap wrong opener as the standard negative — improvement
**Mechanism.** For every candidate, construct the legal, useful opener with the same raw gap (slot and, where possible, weight) but the wrong landing, like `P` in G1. **Novelty vs nearest prior art.** Makes ITS4's control concrete; generic reshuffles do not match raw gap. **Cheapest first test.** In a finite pool, report how often an equal-gap wrong opener exists. If it rarely exists, the claim cannot be tested in that pool. **Old-task retention.** Match old-read margins between `R` and `P` before comparing gaps.

### 08. Find the reachable leftover gap before choosing the opener — improvement
**Mechanism.** Compute the set of gaps the pool can reach in one legal record, intersect with `D_Q`, and refuse when the intersection is empty. **Novelty vs nearest prior art.** Backward reachability; this is the obstruction audit #258 card 10 asks for, here with a frozen successor. **Cheapest first test.** Two pools: G1's, and one with `R` removed, where the intersection must be empty. **Old-task retention.** Report intersections that exist only by violating an old read.

### B. Make the region robust

### 09. Land a pair, not a point, in one region — primitive candidate
**Mechanism.** Both aliases must end in the same `Q` activation cell and clip branch, or `Q`'s damping is a midpoint illusion. **Novelty vs nearest prior art.** [#258][gaphand] card 02 lands pairs in disjoint regions; this version requires the same opener to do it without per-history dispatch. **Cheapest first test.** A two-cell `Q`, with a pair whose midpoint is in `D_Q` and whose ends straddle the boundary. **Old-task retention.** Old reads straddling the same cell boundary.

### 10. Land with margin against unseen writeback orders — improvement
**Mechanism.** Choose the opener by its distance from leaving `D_Q` under the declared family of paired histories, not by the best central contraction. **Novelty vs nearest prior art.** Robust reachability margin; [#258][gaphand] card 08 does this for P, here for an opener against a frozen `Q`. **Cheapest first test.** Three writeback orders, two openers; one is central-best, the other margin-best. **Old-task retention.** Report the first A/B miss under the worst order, not just the nominal pass.

### 11. Relocate for a successor sequence, not one batch — primitive candidate
**Mechanism.** `D_Q` is the preimage of the whole required `Q₁…Q_k` sequence; the opener lands where every stage stays legal and the gap stays damped. **Novelty vs nearest prior art.** [#258][gaphand] card 05 trains P for a corridor; here the target is a certified multi-step region and P is a single truthful record. **Cheapest first test.** Two `Q` batches with crossed curvature axes; one landing contracts at `Q₁` and rebounds at `Q₂`. **Old-task retention.** Read B after each `Q` stage.

### 12. One opener for several possible successors — primitive candidate
**Mechanism.** If the next useful batch is one of `{Q_a, Q_b}`, land in `D_{Q_a} ∩ D_{Q_b}` so no route tag is needed. **Novelty vs nearest prior art.** [#258][gaphand] card 06 freezes heterogeneous routes; here the opener is the only choice and the intersection is preregistered. **Cheapest first test.** Three routes; drop one route to make the intersection empty. **Old-task retention.** The old read most sensitive to the route withheld at test time.

### 13. Bound when the landing expires — primitive candidate
**Mechanism.** Certify how many coast or interleaved-service steps the landed pair can wait before leaving `D_Q`. A late `Q` is refused, not trusted. **Novelty vs nearest prior art.** [#262][parent] card 16 does safe-until deadlines for refills; this one covers a relocation. **Cheapest first test.** G1 with zero to three coast steps between `R` and `Q`. **Old-task retention.** Execute A/B/installed C at the last admissible delay.

### 14. Keep ordinary old service running between opener and successor — primitive candidate
**Mechanism.** Certify the landing under a declared window of interleaved A/B batches (#262 card 05 service clock), with `D_Q` checked on the state the service actually produces. **Novelty vs nearest prior art.** Robust scheduling composes disturbances; the new requirement is that service must not knock the pair out of `Q`'s region. **Cheapest first test.** Insert one old batch at either position; require one accepted and one position-dependent rejected plan. **Old-task retention.** The interleaved old batch is itself the probe; also count delayed reads.

### C. Make it cheaper or reusable

### 15. Publish `D_Q` once and reuse it for any opener pool — primitive candidate
**Mechanism.** A frozen useful `Q` publishes its damping region as a certificate; later pools only need to prove their opener maps the fiber into it. **Novelty vs nearest prior art.** Assume-guarantee contracts and [#262][parent] card 21; the claim is amortization over many openers. **Cheapest first test.** Three pools against one `D_Q`, with an impostor opener that matches the point gradient only. **Old-task retention.** Recheck A/B/C at each accepted substitution.

### 16. Pay for the relocation from the opener's own C gain — improvement
**Mechanism.** Admit an opener only if its own loss gain covers the extra charged work; in G1, `R` takes U's own loss 4→0. **Novelty vs nearest prior art.** Like [#262][parent] card 22, it measures service, not slot gaps. **Cheapest first test.** In G1-style enumeration, compare total C loss after `R,Q` with the best legal two-record plan that ignores the gap. **Old-task retention.** Worst-prefix A/B/C at matched absolute C gain.

### 17. Turn relocation into a batch-partition rule — primitive candidate
**Mechanism.** Repartition the examples already owed, so the first batch lands the gap for the frozen second batch; no example is omitted or moved across the deadline. **Novelty vs nearest prior art.** [GraB][grab] balances order and [OptiSelect][optiselect] ranks one-step utility; the criterion here is the paired preimage of a frozen successor. **Cheapest first test.** Exhaust equal-size partitions of a six-example set; compare with GraB and one-step OptiSelect-style ranking at equal trials. **Old-task retention.** An A probe that depends on one rare example in the first batch.

### 18. Let an old-task batch be the opener — primitive candidate
**Mechanism.** The required A/B service batch, not a C record, relocates the gap for a frozen C successor, so the relocation is free work. **Novelty vs nearest prior art.** [#252 effect commits][effect] hand off through a required old update; here the handoff target is a damping region. **Cheapest first test.** G1 with `R` relabeled as an A record; check that A's own read improves. **Old-task retention.** The opener's own task must not get worse; check B.

### 19. Make the opener choice a single public bit — primitive candidate
**Mechanism.** Among a small certified menu of openers, a public read after the previous step picks one; aliases the read cannot separate are certified as a union. **Novelty vs nearest prior art.** Belief-space MPC branching ([#262][parent] card 06); the payoff is replacing a private slot read with one the host already serves. **Cheapest first test.** Two aliases needing opposite openers, with a visible read and a rounded-identical read. **Old-task retention.** Hold out the A/B items the read is computed from.

### D. Interaction and audits

### 20. Merge test: relocation × next-bottleneck refill — primitive candidate (#262 card 19 × ITS4)
**Mechanism.** One opener both lands the pair gap in `D_Q` and leaves a refill legal for the next announced request. **Novelty vs nearest prior art.** It must beat the stacked best relocation plus best refill, as the ledger's merge rule requires. **Cheapest first test.** Two equal-gain openers, one shared refill; only one opener leaves both feasible. **Old-task retention.** A/B/C at opener, `Q`, refill and debit.

### 21. Audit whether the order dependence was worth removing — improvement
**Mechanism.** Before relocating, measure whether the paired gap actually changes a future decision or old read. Relocating a harmless gap is wasted work. **Novelty vs nearest prior art.** [Shuffle-order noise][shuffle] quantifies the gap; this asks if closing it pays. **Cheapest first test.** Two paired histories whose gaps differ in size but not in downstream old-task error. **Old-task retention.** Old-task error differences between `U` and `V` before and after `Q`.

### 22. Scale check: does a relocating opener exist in a real fine-tuning pool? — improvement
**Mechanism.** Search a small LM's fine-tuning pool for openers whose paired image enters a frozen successor's empirical damping region, using two shuffle orders as the paired histories. **Novelty vs nearest prior art.** The supply question #262 question 1 leaves open, now for gap landing; compare with [delayed transport][transport] measurements. **Cheapest first test.** A CPU MLP on a 3-task stream with 2 orders, 50 candidate openers and a frozen next batch; report the fraction landing in `D_Q` against equal-gap wrong openers. **Old-task retention.** Held-out old-task accuracy on both histories after `Q`.

## Ranked deeper questions

1. **Does the landing survive a real feature boundary?** Cards 01, 03, 06 and 07. Move G1 to a 2-unit ReLU host with real labels. The claim survives only if a cell-changing opener lands the pair in `D_Q` where reordering, `Q,Q`, waiting, the best stack of #262/#258/#261 and exact joint search at matched C gain do not. Retire it if the frozen-mask ablation keeps the win, because then it is quadratic linear algebra.
2. **Is the executed adaptive update damped, not just the first moment?** Cards 04, 05 and 09. In scalar or 2-D Adam, look for an opener that equalizes executed updates after `Q` where `Δm`-aimed openers and the #258 card 11 split repair fail. Retire it if a joint executed-update objective over the same pool ties.
3. **Is the win admission or aim?** Cards 02 and 08. In G1 the opener both legalizes `Q` and aims the gap. If, across pools, wins vanish once the cap is lifted, the primitive is cap slack, already covered by #242/#250. It is not relocation.
4. **Can a published damping region amortize across opener pools and service interleavings?** Cards 13–15. Count certificate construction, bytes and failed queries against fresh robust search per pool. Retire if savings vanish on a held-out pool or an interleaved old batch routinely ejects the pair.

[parent]: https://github.com/manojbajaj95/cl/pull/262
[triage]: https://github.com/manojbajaj95/cl/blob/d74d580d4cadcf7514a10ed23597142cba8ad7d1/reviews/flood-triage.md#L385
[its4]: https://github.com/manojbajaj95/cl/blob/d80ad1f8262721aa3701c88343e570d203ca4ac9/ideas/flood/cross-pool-57.md
[ledger]: https://github.com/manojbajaj95/cl/blob/d74d580d4cadcf7514a10ed23597142cba8ad7d1/reviews/idea-ledger.md
[gaphand]: https://github.com/manojbajaj95/cl/pull/258
[norm]: https://github.com/manojbajaj95/cl/pull/261
[compl]: https://github.com/manojbajaj95/cl/pull/248
[effect]: https://github.com/manojbajaj95/cl/pull/252
[kaczmarz]: https://doi.org/10.1007/s00041-008-9030-4
[shuffle]: https://arxiv.org/abs/2606.29554
[adamwio]: https://arxiv.org/abs/2608.19762
[transport]: https://arxiv.org/abs/2608.24593
[optiselect]: https://arxiv.org/abs/2610.03432
[grab]: https://arxiv.org/abs/2205.10733
[mtt]: https://arxiv.org/abs/2203.11932
[funnels]: https://arxiv.org/abs/1601.04037
