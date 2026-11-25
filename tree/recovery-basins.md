# Trained recovery basins

**Parent:** [Adaptive-default escrow renewal](adaptive-renewal.md) ([PR #236][parent]). **Status:** Ideas only; no pilot or GPU work. [Flood triage, row 349][triage] keeps parent cards **10** (teach the recovery basin, not the endpoint) and **13** (move private slot differences into a useful shared feature) at score 3. The [idea ledger][ledger] requires an old-task retention check in every first test, and the stacked best controls of the parts as the joint control.

**Verdict:** Both bets are about *what offline host training optimizes*, not about a new runtime controller. Card 10 counts only if a host trained against a basin objective (every reachable post-default belief has a certified public route into the ready interface by the deadline) admits held-out defaults that endpoint-trained, meta-learned and robust-trained hosts miss at matched C accuracy and retention. Card 13 counts only if C learning itself places hidden optimizer-slot differences in the unobservable subspace of every declared service and witness reader, so the renewal equivalence holds *without* waiting for contraction or resetting slots, and the absorbing feature is one that C and a later B genuinely use. Computing a basin, a region of attraction or an unobservable subspace is known; shaping it with truthful C training under a fixed public interface is the candidate. The paper checks below show both effects exist in two-parameter linear hosts and show their first costs: the basin host gives up design-trace endpoint loss, and the absorbing host gives up C speed and stays visible to an undeclared reader.

## Contract

- **Inherited from the parent.** One public policy fixed before evaluation; ready is a service guarantee (timely paired service and closure under service and default), not an empty ledger; proofs track reachable belief sets and a bounded recovery rank; the same small interface every round; full A/Bᵢ/prior-C panel at named cuts and after a common ordinary suffix ([parent contract][parent]).
- **Basin objective (card 10).** On offline design streams, sample reachable post-default belief sets `𝔅` (aliases with one public history). Loss = C task loss + λ·Σ_𝔅 [no certified public word reaches ready from all of 𝔅 by the deadline], with a differentiable surrogate (worst-alias distance to ready after the best public word; hinge on a recovery-rank decrease). The certificate, not the surrogate, is what is scored at test. Endpoint-only training uses the same streams and C loss with λ = 0. Held-out evaluation uses default patterns and cut times outside the design set.
- **Absorption objective (card 13).** The renewal equivalence is fixed in advance: two states are equivalent iff every declared reader (service witness, live B witness, protected A/C probes) gives the same outputs under every lawful continuation up to the horizon. A hidden-slot difference is *absorbed* when it lies in that unobservable subspace, *contracted* when it decays below the margin in time, *reset* when deleted. Only absorption by a feature that also carries incoming C and a later B witness counts; a dedicated inert spare is the control.
- **What it must beat.** Endpoint-only training (#226 card 21), ANML/OML/MAML meta-learned hosts, robust/adversarial training on the same perturbation set, runtime recoverability filters on a fixed host, Leave-No-Trace reset policies, Lyapunov/ROA-enlarging training, slot reset, waiting for contraction (#216 card 10, #232), output-space momentum, and a dedicated spare feature at matched width; all at matched truthful examples, offline compute, bytes, verification and retention floors.

## Paper checks (exact, CPU)

Script: [`probes/recovery_basins_check.py`](probes/recovery_basins_check.py) (fractions only, under a second).

**F1. The basin objective prefers a host the endpoint objective rejects.** Deviation `x = (s, r)`: `s` is the live service coordinate, `r` a hidden slot. One C step is `x ← [[1/2, h], [0, 1/2]] x`, with coupling `h` set by the host. The design default lands at `(1/2, −1/2)`; held-out aliases with the same public `s = 0` land at `(0, ±1/2)`. Ready after two C steps means `|s| ≤ 1/16`.

| Host `h` | Design endpoint `s₂` | Design endpoint loss | Worst held-out alias `|s₂|` | Held-out ready? |
|---|---|---|---|---|
| 0 | 1/8 | 1/128 | 0 | yes |
| 1/8 | 1/16 | 1/512 | 1/16 | yes |
| 1/4 | 0 | 0 | 1/8 | **no** |

Endpoint-only training picks `h = 1/4`, which zeroes the design loss and loses the held-out aliases. The basin penalty picks `h ∈ [0, 1/8]` and pays at most `1/512` endpoint loss. The fixture only shows that the two objectives can disagree. It does not show that a nonlinear host has such a choice, that C learns through it, or that the public word is uniform over larger alias sets.

**F2. Absorbing a slot difference is not shrinking it, and it is reader-relative.** Heavy-ball on C loss `½θᵀHθ` (`β = η = 1/2`). Two states share `θ` but differ by `d = (0, 1)` in the momentum slot. Leak = reader·(θ difference) at step k.

| Host | Service reader `(1,0)` leaks k=1..4 | Later-B reader `(1,1)` leaks k=1..4 | C loss from `(1/2,1/2)` after 4 steps |
|---|---|---|---|
| coupled `H = [[1,1/2],[1/2,1]]` (contract only) | 0, 1/16, 1/8, 33/256; not below 1/64 within 8 steps | −1/4, −3/16, −1/64, 21/256 | 2523/524288 |
| aligned `H = I` (absorb) | 0, 0, 0, 0 (exactly, forever) | −1/4, −1/4, −1/8, 0; below 1/64 from k=8 | 1/64 |

In the aligned host the slot difference is still live after four steps (`m` differs by −1/4) yet never reaches the service reader. That is the equivalence without contraction. But (i) the reader `(1,1)`, which a later B witness may use, sees it, so absorption must be certified against every declared reader; and (ii) the aligned host learns C about 3× slower here, so absorption has a C price that the scorecard must charge.

## Idea cards

### 01. Train the basin, not the endpoint — inherited candidate (#236 card 10)
**Mechanism.** Add λ·(uncertified post-default belief sets) to offline host training, using a worst-alias route surrogate and scoring only exact certificates. **Novelty vs nearest prior art.** [Recoverability][recov] grows a certified tube toward the viability kernel of a *fixed* plant and switches at runtime; [ANML][anml]/[OML][oml] optimize average adaptation. Here the plant is the learner and the trained object is the host's basin under a fixed public C word language. **Cheapest first test.** F1 scaled to a 3-parameter host with two public words and four aliases; compare λ = 0, ANML-style meta-gradient on endpoint loss, and random hosts at matched C accuracy. **Old-task retention check.** A/Bᵢ/prior C floors at installation and at every state along the worst certified route.

### 02. Absorb slot differences into the renewal equivalence — inherited candidate (#236 card 13)
**Mechanism.** Let C update a shared feature so that hidden optimizer-slot differences land in the unobservable subspace of all declared readers instead of contracting. **Novelty vs nearest prior art.** Observability theory computes unobservable subspaces; [fiber fingerprints][fiber] and [training-state equivalence][tse] show readout-identical states diverge under future training; [BOM][bom] moves momentum into output space by design. None trains the host so truthful C learning places live slot differences in a fixed equivalence. **Cheapest first test.** F2 with `H = JᵀJ` from a two-unit shared layer trained on C; compare slot reset, waiting for contraction, and an inert dedicated spare at matched width. **Old-task retention check.** A/Bᵢ/prior C at every prep prefix and after a normal slot-coupled suffix.

### 03. Certify a basin against a held-out default *grammar* — primitive candidate
**Mechanism.** Train basins on default patterns generated by a small grammar (cut position, overlap, burst length) and certify on unseen productions of the same grammar, not on resampled traces. **Novelty vs nearest prior art.** Domain randomization and robust training sample perturbations; the candidate is a certificate quantified over a compositional default language. **Cheapest first test.** Grammar with two cut types and nesting depth ≤ 2; hold out depth-2 productions; compare trace-resampled robust training at equal compute. **Old-task retention check.** Panel at the deepest held-out production's worst route.

### 04. Shape the basin boundary where defaults actually land — primitive candidate
**Mechanism.** Weight the basin penalty by the reachable post-default distribution induced by ordinary B/C training itself, so capacity is spent where defaults land, not uniformly. **Novelty vs nearest prior art.** ROA enlargement ([neural Lyapunov][lyap]) maximizes volume; this targets reachable mass under learner dynamics. **Cheapest first test.** Two hosts with equal basin volume, different overlap with the reachable default cloud; check held-out ready rate. **Old-task retention check.** Panel on both hosts at matched volume.

### 05. Learn a recovery rank function with the host — primitive candidate
**Mechanism.** Co-train a small rank network `V` that must decrease by ≥ 1 along the chosen public word from every alias, as a certificate carrier the verifier checks exactly. **Novelty vs nearest prior art.** Learner–verifier Lyapunov synthesis ([2611.21009][clf]) learns controller+CLF for a plant; here the "plant" is SGD on the host and the rank is in deadline ticks. **Cheapest first test.** Quadratic host, ICNN-free piecewise-linear `V`, exact check on vertices; compare a fixed rank from the parent. **Old-task retention check.** Panel at each level set of `V` visited.

### 06. Make absorption survive the optimizer schedule — primitive candidate
**Mechanism.** Require the absorbing subspace to be invariant for every step of the declared learning-rate/β schedule (warmup, decay), not one fixed `(η, β)`. **Novelty vs nearest prior art.** [2610.18085][equiv] shows optimizers are not reparameterization-equivariant; this asks for a learned invariance that holds across the schedule. **Cheapest first test.** F2 with η switching 1/2 → 1/4 at k=3 and Adam-style per-coordinate scaling; check exact zero leak throughout. **Old-task retention check.** Panel at each schedule switch.

### 07. Absorb second-moment differences, not just momentum — primitive candidate
**Mechanism.** Adam `v` differences rescale future steps multiplicatively; certify that the rescaling acts only inside the reader-null subspace. **Novelty vs nearest prior art.** [Delayed optimizer-state transport][dost] and [AdamW I/O dynamics][aio] measure `v`'s delayed effect; none shapes where it acts. **Cheapest first test.** Two states differing in `v₂` only; diagonal vs rotated host; exact leak for 6 steps. **Old-task retention check.** Panel after a large-gradient B batch that amplifies the `v` gap.

### 08. Price absorption in C speed — improvement
**Mechanism.** Report the C-progress loss of the absorbing host against the best contracting host at equal steps (F2: 1/64 vs 2523/524288). **Novelty vs nearest prior art.** An honest scorecard term; no new object. **Cheapest first test.** Sweep coupling between 0 and 1/2 in F2; plot leak bound vs C loss Pareto front. **Old-task retention check.** Panel at each Pareto point.

### 09. Declare readers before absorbing, and stress with an undeclared one — improvement
**Mechanism.** Certify absorption for the declared reader set, then attack with a held-out reader built from B's future witness family (F2's `(1,1)`). **Novelty vs nearest prior art.** Standard held-out probing; needed to stop absorption being a reader-choice artifact. **Cheapest first test.** Random readers from the B-witness family; fraction that see the leak. **Old-task retention check.** A/C probes included as declared readers.

### 10. Basin-and-absorb joint host — primitive candidate
**Mechanism.** One offline objective: basin penalty over post-default aliases whose aliasing is *exactly* the hidden-slot difference, so absorption makes aliases equivalent and enlarges the certified basin at once. **Novelty vs nearest prior art.** Joins 01 and 02; must beat the stack of separately trained basin host plus slot reset. **Cheapest first test.** F1 with `r` defined as a momentum slot and F2 dynamics; compare joint vs stacked at equal compute. **Old-task retention check.** Panel on the worst alias of the joint basin.

### 11. Turn alias sets into one alias by C learning — primitive candidate
**Mechanism.** Train C updates that map distinct aliases to the same reader-equivalence class before the next service window, so a uniform public word exists by construction. **Novelty vs nearest prior art.** Synchronizing words in automata collapse states by input; here truthful C batches are the synchronizing input and the host is trained to admit one. **Cheapest first test.** Three aliases from the parent's D₀/D₁/D₂ fixture realized in a 2-unit ReLU host; search for a C batch order that synchronizes. **Old-task retention check.** Panel on all three aliases after synchronization.

### 12. Penalize basins that rely on a protected recovery window — improvement
**Mechanism.** Add a second penalty for routes that need a default-free interval longer than the declared promise. **Novelty vs nearest prior art.** Parent card 04 finds the weakest promise; this trains against needing it. **Cheapest first test.** Two hosts with equal basins under a 2-tick window; shrink to 1 tick. **Old-task retention check.** Panel inside the shortened window.

### 13. Distill the basin certificate into the host's own features — primitive candidate
**Mechanism.** After training, require that membership in the basin be readable by a linear probe on the host's features, so the public policy can check readiness without an external solver. **Novelty vs nearest prior art.** Learned safety critics ([monotone viability][mvl]) are separate networks; here the host carries its own readiness signal. **Cheapest first test.** Probe accuracy on held-out aliases vs a separate critic at equal bytes. **Old-task retention check.** Probe and panel after a C suffix.

### 14. Basin-preserving C — primitive candidate
**Mechanism.** Constrain online C updates (after deployment) so the certified basin does not shrink, using the rank network as a barrier. **Novelty vs nearest prior art.** CBF-filtered learning protects safe sets of a plant; here online learning protects its own future recoverability. **Cheapest first test.** Online C stream that, unconstrained, shrinks F1's basin (drives h → 1/4); compare projected C and OGD. **Old-task retention check.** Panel and incoming C utility at matched steps.

### 15. Grow the basin with C, not spare capacity — primitive candidate
**Mechanism.** Require basin enlargement to be caused by a feature that improves C loss; ablate it and the basin must shrink. **Novelty vs nearest prior art.** Separates "C finances recovery" (parent bet) from a spare buffer. **Cheapest first test.** Host with one C-useful and one inert unit of equal norm; ablate each. **Old-task retention check.** Panel after each ablation.

### 16. Recovery basins for multiple ready interfaces — primitive candidate
**Mechanism.** Train basins into a small set of ready interfaces (one per service class), with routes chosen by public history. **Novelty vs nearest prior art.** Multi-target reach-avoid is known; the candidate is learner-generated interfaces sharing one host. **Cheapest first test.** Two interfaces, four aliases, exact route search. **Old-task retention check.** Panel at both interfaces.

### 17. Adversarial basin training with reachable-only adversary — improvement
**Mechanism.** Inner loop finds the reachable post-default alias set with no certified route; outer loop updates the host. Unreachable aliases are excluded by a reachability check. **Novelty vs nearest prior art.** Adversarial training (cf. [2604.01188][advcert]); the reachability filter avoids over-hedging. **Cheapest first test.** Compare with unconstrained-adversary training on F1-style hosts; count over-hedged service refusals. **Old-task retention check.** Panel on adversarial aliases.

### 18. Absorb slot differences across learners being merged — primitive candidate
**Mechanism.** Two learners with different optimizer histories merge weights; train the shared feature so their slot differences are reader-null, making merge-then-continue equal to either continuation. **Novelty vs nearest prior art.** Merging ignores or averages optimizer state; this certifies continuation equivalence. **Cheapest first test.** F2 with two slot states and averaged weights; leak after merge. **Old-task retention check.** Panel for both parents' tasks after merge and a suffix.

### 19. Certificate cost accounting — improvement
**Mechanism.** Report verifier time, certificate bytes and offline design compute alongside basin size and absorption margin. **Novelty vs nearest prior art.** Bookkeeping. **Cheapest first test.** Log for F1/F2 scaled to 4 parameters. **Old-task retention check.** Not applicable beyond the panel already run.

### 20. Basin collapse under scale — improvement
**Mechanism.** Measure how certified basin fraction scales with host width at matched C accuracy; a primitive that vanishes with width is not one. **Novelty vs nearest prior art.** Laziness/width effects (ledger: SP-lazy forgetting) are a known confound. **Cheapest first test.** Widths 2, 4, 8 under SP and muP. **Old-task retention check.** Panel at each width.

### 21. Equivalence-preserving slot compression — primitive candidate
**Mechanism.** Once a slot difference is certified reader-null, drop the slot coordinates in that subspace, saving optimizer memory with no future service change. **Novelty vs nearest prior art.** [BOM][bom] and factored optimizers compress state by design; this compresses exactly the learned null part. **Cheapest first test.** F2: delete `m₂`; verify identical service trajectory. **Old-task retention check.** Panel with and without the dropped coordinate after a suffix.

### 22. Falsify the bet with a C stream that absorbs nothing — improvement
**Mechanism.** Construct a held-out C stream that learns well but whose Hessian couples the slot into the service reader (F2 coupled host); the claim must report failure, not retrain. **Novelty vs nearest prior art.** Negative control. **Cheapest first test.** Rotated-feature C task; measure leak and C accuracy. **Old-task retention check.** Panel on the failing stream.

## Ranked deeper questions

1. **Does basin training admit held-out defaults that endpoint, meta-learned and robust training miss, at matched C accuracy and retention?** Cards 01/03/04/17. Kill if robust training on the same perturbation set or a runtime recoverability filter on an endpoint-trained host matches the certified held-out ready rate.
2. **Can truthful C learning absorb a slot difference for every declared reader, including a later B witness, without a C-speed loss larger than slot reset's cost?** Cards 02/06/07/08/09. Kill if reset plus waiting matches service at equal steps, or if any reader from the B-witness family sees the leak.
3. **Is the joint host more than the stack?** Cards 10/11/15. Require a reachable alias set certified only by the joint host; otherwise call it a composition.
4. **Do basins persist under online C and growing width?** Cards 14/20/22. Find the first width or online-C step where the certificate fails, and check whether basin-preserving C pays for itself in incoming C utility.

[parent]: https://github.com/manojbajaj95/cl/pull/236
[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L349
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[recov]: https://www.alphaxiv.org/abs/2611.23589
[anml]: https://www.alphaxiv.org/abs/2002.09571
[oml]: https://huggingface.co/papers/1905.12588
[fiber]: https://www.alphaxiv.org/abs/2608.15976
[tse]: https://www.alphaxiv.org/abs/2611.23245
[bom]: https://www.alphaxiv.org/abs/2609.36738
[lyap]: https://www.alphaxiv.org/abs/1808.00924
[clf]: https://www.alphaxiv.org/abs/2611.21009
[equiv]: https://www.alphaxiv.org/abs/2610.18085
[dost]: https://www.alphaxiv.org/abs/2608.24593
[aio]: https://www.alphaxiv.org/abs/2608.19762
[mvl]: https://www.alphaxiv.org/abs/2611.07616
[advcert]: https://www.alphaxiv.org/abs/2604.01188
