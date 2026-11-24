# Rented constraints: leasing protected directions against a proven wake-up

**Parent:** [Bounded burial and universal wake-up words](bounded-burial.md) ([PR #142](https://github.com/manojbajaj95/cl/pull/142)), extending its cards #1 (rent the constraint, not the parameter) and #11 (idempotent wake boundary). **Triage:** [flood-triage.md, row 230](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L230). **Status:** Ideas only; no experiments run; no GPU.

**Node question:** Can a new task B temporarily write along weight directions that a continual learner protects for an old skill A, but only where a proven, label-free wake-up sequence `W` restores A afterwards? And does choosing `W` with idempotent dynamics (applying it twice does about what applying it once does) make such leases safe to grant, renew and revoke without watching A?

## Root cause: what a lease changes, and why idempotence is not enough

Projection methods ([OGD](https://arxiv.org/abs/1910.07104), [GPM](https://arxiv.org/abs/2103.09762), [Adam-NSCL](https://arxiv.org/abs/2103.07113), [TRGP](https://arxiv.org/abs/2202.02931), [SGP](https://arxiv.org/abs/2302.01386), [FS-DGPM](https://arxiv.org/abs/2110.04593), DUET [2611.29269](https://arxiv.org/abs/2611.29269)) protect A by keeping B's update `Δθ` out of a subspace `P_A` that A's current outputs depend on. That is a constraint on the **present state**. A lease swaps it for a constraint on a **future state**: B may move along `P_A`, provided the trajectory stays inside the set `S_W = {θ : W(θ) serves A, B and C}`. The protected object changes from "A's outputs now" to "A's outputs after `W`". This needs three properties, and idempotence gives only the first:

1. **Retraction.** `W(W(θ)) ≈ W(θ)` on task-relevant outputs, so a wake can be issued blindly and repeated (PR #142 #11).
2. **Correct fixed set.** The fixed points of `W` are states where A is right. An idempotent `W` can map every host to a constant or polarity-flipped A, so idempotence alone says nothing about correctness (card 10).
3. **Basin coverage.** Every state the lease lets B reach lies in the basin of the good fixed set, and `W` keeps B's increment. This is a forward-invariance condition of the kind a control barrier function certifies ([Ames et al. 2019](https://arxiv.org/abs/1903.11199)), not a null-space condition.

So a lease is safe when B's writes are confined to **basin(W) ∩ {B kept by W}**. Idempotence makes the boundary of that set observable without labels (`W` stops moving the outputs once it has finished), but it does not certify the set. Two negative controls follow:

- **Linear host.** In a linear least-squares host, public unlabeled gradient steps cannot depend on A's labels. Once B overwrites A's coordinates along `P_A`, no public `W` restores A's polarity on both A⁺/A⁻ twin hosts. Leases must fail there. A lease that "works" in the linear host is storing A somewhere, which makes it an equal-byte saved delta.
- **Stored coordinates.** A `W` that resets `P_A` coordinates to stored values is PackNet/saved deltas with extra steps (true by construction, ledger pattern). The wake must be public-data dynamics whose effect depends on the host's surviving state, as in spurious forgetting ([2501.13453](https://arxiv.org/abs/2501.13453), [2610.08718](https://arxiv.org/abs/2610.08718)) and interface drift recoverable by transport keys ([2606.02860](https://arxiv.org/abs/2606.02860)). The lease is plausible only where `P_A` mixes **access** directions (readout or interface alignment that B can disturb and a public `W` can realign) with **payload** directions (the A distinction itself, which must not be leased).

## What would count

The PR #142 contract binds every card: dormancy is a randomized intervention at fixed model size; A must pass when learned, may fail during the lease, and must pass after `W`; B's gain must survive paying for `W` (PR #142 #21's release × wake interaction on joint service); `W` is frozen on disjoint development histories, carries no answer (it must wake opposite-label A⁺/A⁻ twins), and is charged for its public batches, steps, bytes and latency. On top of that, a lease adds:

- **Lease terms are declared before B trains.** Leased directions (rank, layer, which basis), maximum write radius or step count, the term (steps until mandatory wake), the renewal rule and the revocation rule are all fixed in advance. A lease that grows when A happens to recover is a selection on A.
- **"Proven" means a proof that cannot become replay.** A grant decision that looks at A labels on a shadow fork is labelled relearning by selection (PR #139). Allowed evidence is (a) label-free quantities on the live host (W-displacement, contraction estimates, public-output geometry), or (b) a fixed audit set whose bytes and labels are charged to the lease and given to every baseline as replay data at the same budget. Either way the proof has to beat its own cost.
- **Baselines at equal budget.** GPM, TRGP (trust-region relaxed projection), SGP (scaled projection), FS-DGPM (dynamically released bases), Adam-NSCL, EWC with the same `W`, PackNet with release, equal-byte saved deltas, DER++ with the audit set as buffer, NSR-style retrieval of compressed subspaces ([2606.30067](https://arxiv.org/abs/2606.30067)), and unconstrained B plus the same `W`. The decisive comparison is **post-wake B at matched post-wake A/C floors** versus GPM/TRGP/SGP, plus the same lease with a sham `W`.
- **Retention reporting.** Fresh paired-polarity A queries before the lease, during the lease, right after `W`, and after a further B window; C throughout; B before and after `W`. Report worst-skill and lower-tail margins, wake failures and the number of renewals, not just endpoint accuracy.
- **Ledger screen.** [Idea ledger (PR #6)](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md): no scalar forecast without a target-variance gate (plasticity-reserve kills), no Gramian write selection (PR #9/#21), match margins before any forgetting-order claim, merges must beat the stack of their parts' baselines. PR #142's #2–#4/#6/#7 are already triaged as variants of #1, so cards here change the **condition** under which writes are allowed, the **wake's dynamics**, or the **proof**, not the resource that is borrowed.

## Idea cards

### A. What is leased, and against what

#### 1. Protect the wake image, not the state (primitive)

- **Mechanism:** Replace GPM's constraint `Δθ ⟂ P_A(θ)` with `J_{A∘W}(θ) Δθ ≈ 0`: B may move freely as long as the **post-wake** A outputs do not move. Estimate the post-wake Jacobian by differentiating A's public-input features through a short unrolled `W` (no A labels: match post-wake A logits on public inputs before and after the step). Directions that change A now but are undone by `W` become writable; directions that `W` cannot undo stay protected.
- **Nearest art / delta:** GPM/Adam-NSCL/SGP project out the current-output subspace; TRGP relaxes it inside a trust region by task correlation. None protects a post-repair function. Unrolled differentiation through an update rule is MAML-style; the new object is a null space of the composed map `A∘W`.
- **Cheapest first test:** Width-64 MLP, A then C then B with overlapping features, `W` = 4 frozen public steps. Compare post-wake-Jacobian projection to GPM, TRGP, SGP and FS-DGPM at the same per-step B gradient norm, plus a sham `W` in the Jacobian. Reject if B's post-wake gain at matched A/C floors does not exceed the best projection baseline, or if it also "works" in the linear host (leak).
- **Old-task retention check:** Paired A⁺/A⁻ accuracy after `W`, C during B, and A again after 50 further unprojected B steps, to catch protection that only holds at the wake point.

#### 2. Lease access, never payload (primitive)

- **Mechanism:** Split A's protected basis into access directions (where stitching an old late stage onto the new early stage with an alignment map recovers A) and payload directions (where it does not). Lease only access directions to B; keep payload under hard projection. The wake is a public realignment of the access interface, not a stored key.
- **Nearest art / delta:** Transport keys ([2606.02860](https://arxiv.org/abs/2606.02860)) recover A through a stored task-specific alignment from paired anchors; spurious forgetting (2610.08718) removes one shared shift direction. Here the access/payload split decides **write rights during B**, and recovery uses no stored key.
- **Cheapest first test:** Label each GPM basis vector as access or payload with the stitching test on development histories, freeze the rule, then lease (a) access only, (b) payload only, (c) a rank-matched random split. Reject unless (a) beats (c) and (b) fails, at equal B progress and equal wake cost.
- **Old-task retention check:** A per polarity after `W` on held-out histories; check that payload-only leases are the ones that destroy the A⁺/A⁻ distinction (decoded from hidden features), not just its readout.

#### 3. Basin-radius write budget (primitive)

- **Mechanism:** Estimate, label-free, a radius `r(θ)` within which `W` still contracts outputs back to the awake set (largest perturbation along leased directions after which `W∘W ≈ W` and post-wake public A logits return to their pre-lease values). Clip B's cumulative leased displacement to `r`. Capacity is granted in units of basin radius, not rank.
- **Nearest art / delta:** TRGP's trust region is defined by task-gradient correlation; Lipschitz certification ([Weng et al. 2018](https://arxiv.org/abs/1801.10578)) bounds input perturbations. This bounds parameter displacement by a repair operator's basin.
- **Cheapest first test:** Sweep radius multipliers {0.5, 1, 2, 4}·`r̂`; the claim is a sharp wake-failure knee near 1. Compare to a fixed-norm budget tuned on development and to TRGP. Gate first: the knee must be wider than seed variance (ledger predictor gate).
- **Old-task retention check:** Failure rate and worst-case A margin per multiplier, plus C, with the multiplier chosen on development only.

#### 4. Lease term from W-displacement drift (improvement)

- **Mechanism:** During the lease, periodically apply `W` on a throwaway fork and measure `d(θ) = ‖f(W(θ)) − f(θ)‖` on public inputs. A rising slope of `d` means B is approaching the basin edge; end the lease (wake, reinstate protection) before the extrapolated crossing. No A labels.
- **Nearest art / delta:** Label-free forgetting detection (PR #126) and real-time spurious-forgetting detection ([2512.20634](https://arxiv.org/abs/2512.20634)) monitor current behaviour; this monitors how far the repair has to travel, which can grow while A's current score is already zero.
- **Cheapest first test:** Compare `d`-slope termination to fixed terms, a gradient-norm trigger and an oracle A-labelled trigger, all with the same total fork cost. Gate on target variance first.
- **Old-task retention check:** Count wakes that fail after termination as A request failures; report C and B at each termination.

#### 5. Collateral: the cheapest bits that keep the basin (primitive)

- **Mechanism:** A lease can require B to deposit collateral: a few frozen coordinates, a sign mask, or one low-rank factor along `P_A` that `W` cannot rebuild from public data. Choose collateral by greedy basin gain per byte on development histories. Collateral is returned (unfrozen) at lease end.
- **Nearest art / delta:** PackNet and WSN ([2202.11782](https://arxiv.org/abs/2202.11782)) freeze whole masks; saved deltas store everything. The new quantity is the minimum stored state that turns a failing public wake into a working one, which PR #139's carrier sets frame as hitting-set protection.
- **Cheapest first test:** At equal bytes, compare chosen collateral, random collateral, top-Fisher collateral, and an equal-byte saved delta with no wake. Reject if the saved delta ties.
- **Old-task retention check:** A after `W` with and without collateral, and C/B after collateral is released, to show collateral did not simply block B.

#### 6. Revocable leases with a B ratchet (primitive)

- **Mechanism:** An A request can arrive mid-lease. Revocation = apply `W`, reinstate protection, and continue B under projection. Train B under the lease with an auxiliary term that keeps B's gain inside the post-wake image (`B∘W` loss on B's own data), so revocation keeps what B learned.
- **Nearest art / delta:** PR #142 #6 prices service interruptions; it does not ask whether B's gains survive an early wake. This adds a ratchet on the B side, analogous to keeping committed work through a transaction abort.
- **Cheapest first test:** Revoke at random times; compare B retention after revocation with and without the `B∘W` term, against GPM-from-start at the same total steps.
- **Old-task retention check:** A immediately after each revocation and after resuming B; C throughout; report B loss across revocation.

#### 7. Sub-leases and lease chains (primitive; audit)

- **Mechanism:** B leases A's directions; later D leases B's (including the part B wrote along `P_A`). Waking now needs `W_A` and `W_B`. Test whether the two wakes commute on the joint awake set and whether chained leases compound basin loss.
- **Nearest art / delta:** Leases come from distributed caching ([Gray & Cheriton 1989](https://dl.acm.org/doi/10.1145/74850.74870)), where nested leases are a known hazard; PR #142 #9 studies order within one word, not nested leases across tasks.
- **Cheapest first test:** Four-task MLP stream; cross `W_A W_B`, `W_B W_A` and a joint word, at equal steps, against GPM on all four tasks.
- **Old-task retention check:** All four tasks on the same post-wake copy; flag any order that revives A by losing B.

#### 8. Fractional leases on singular values (improvement)

- **Mechanism:** Instead of all-or-nothing release of a basis vector, lease each protected direction at a rate `λ_i ∈ [0,1]` chosen from its measured post-wake recoverability (card 1's Jacobian), so B gets partial write access where `W` partially repairs.
- **Nearest art / delta:** SGP scales projection by singular-value importance for the **current** task; this scales by recoverability under `W`.
- **Cheapest first test:** SGP vs recoverability-scaled projection at equal B progress, with a shuffled-`λ` control.
- **Old-task retention check:** A after `W`, especially the A inputs aligned with the most-leased directions.

### B. Idempotent wake dynamics

#### 9. Train the wake to be a retraction in weight space (primitive)

- **Mechanism:** Meta-learn the public batches and step sizes of `W` on development histories with a loss on `‖f(W(W(θ))) − f(W(θ))‖` plus post-wake joint service, so `W` becomes a retraction in parameter-update space.
- **Nearest art / delta:** [IGN](https://arxiv.org/abs/2311.01462) trains a network to be idempotent on its inputs; [IT³](https://arxiv.org/abs/2410.04201) uses idempotence of the model on its own predictions for test-time training; [IDER](https://arxiv.org/abs/2603.00624) makes outputs idempotent through an old checkpoint with a replay buffer. Here the idempotent object is the **training continuation**, with no old checkpoint or buffer.
- **Cheapest first test:** Compare a retraction-trained `W` to the best fixed-step word from PR #142 and to adaptive early stopping, at the same maximum steps, on mixed awake, half-dormant and dormant hosts.
- **Old-task retention check:** No A/C regression on already-awake hosts after 1, 2 and 5 applications; joint A/B/C service on dormant ones.

#### 10. Wrong fixed points: break idempotence-as-safety (primitive; audit)

- **Mechanism:** Search adversarially over lease-reachable states for hosts where `W` is idempotent (displacement below threshold) but A is wrong: constant, polarity-flipped, or B-collapsed. The fraction of such states measures how much idempotence can be trusted as a blind safety signal.
- **Nearest art / delta:** Idempotent generative models are known to have collapsed fixed points; [2606.22304](https://arxiv.org/abs/2606.22304) and [2511.02614](https://arxiv.org/abs/2511.02614) add manifold alignment to avoid them. No CL work audits a repair operator's spurious fixed points.
- **Cheapest first test:** Within the lease radius, run gradient search for low displacement and low A margin; report the attainable A error at displacement below the deployment threshold. Compare with random states and with an A-naive host.
- **Old-task retention check:** This card is itself the retention audit; include C and B at the found states.

#### 11. Contraction certificate on outputs (primitive)

- **Mechanism:** Estimate the Lipschitz constant of `θ ↦ f(W(θ))` on public inputs over the leased neighbourhood with power iteration on the unrolled Jacobian. If it is below 1 toward a fixed set that passes the development audit, Banach's theorem gives a basin radius; lease only inside it.
- **Nearest art / delta:** Lipschitz certification bounds input sensitivity; control barrier functions certify forward invariance of a state set. This certifies a parameter-space repair operator.
- **Cheapest first test:** Compare certificate-bounded leases to card 3's empirical radius and to TRGP at equal B progress. Report how loose the certificate is.
- **Old-task retention check:** Wake failure rate inside the certified radius must be near zero on held-out histories; A per polarity and C at every lease end.

#### 12. Wakes that commute with B steps (primitive)

- **Mechanism:** If `W∘S_B ≈ S_B∘W` on B and A outputs for B's SGD step `S_B`, then B can keep training during the lease and the wake can happen at any time. Shape `W` (and the B optimizer) to minimise the commutator, measured on public inputs.
- **Nearest art / delta:** Commutation of updates appears in PR #142 #9 (`UV` vs `VU` within the wake) and in model-merging interference; the commutator between repair and ongoing learning is new.
- **Cheapest first test:** Measure commutator norm against wake-time sensitivity (A after `W` at times t, t+50, t+200). Claim dies if low-commutator wakes are not less time-sensitive than high-commutator ones at matched displacement.
- **Old-task retention check:** A after wakes issued at random times during B, and B after each wake.

#### 13. Paired re-burial and wake: a projection pair (primitive)

- **Mechanism:** Define re-burial `R` (resume leased B writes) and wake `W` so that `R∘W∘R ≈ R` and `W∘R∘W ≈ W`. Then repeated lease cycles neither drift A nor accumulate B loss. Measure drift per cycle as the lifecycle's ratchet error.
- **Nearest art / delta:** PR #142 #20 stresses request order; FCR2 (PR #36) measures hysteresis loops. This targets zero per-cycle drift as a design property.
- **Cheapest first test:** 20 lease cycles; compare per-cycle drift in A margin and B loss for the paired design, plain `W`, and GPM with no leases.
- **Old-task retention check:** A, C and B after every cycle, plus decodability of the A distinction from hidden features, to catch slow payload erosion.

#### 14. Robust idempotence under public-data drift (improvement)

- **Mechanism:** `W` uses public batches whose distribution drifts. Train `W` to stay a retraction across a family of public distributions (domain randomisation on the wake data).
- **Nearest art / delta:** Benign relearning from structured public data ([2602.03379](https://arxiv.org/abs/2602.03379)) shows wakes depend on public data; this asks for a wake that is safe across public-data shifts.
- **Cheapest first test:** Hold out public distributions; compare robust `W` to the PR #142 word and to fresh per-distribution search at equal steps.
- **Old-task retention check:** A per polarity under each held-out public distribution, C and B.

#### 15. Idempotence as a stopping rule (improvement)

- **Mechanism:** Apply `W` in rounds until displacement falls below a threshold frozen on development. If displacement is a valid label-free completeness signal, the expected wake cost falls without failures.
- **Nearest art / delta:** Gain-guided TTA ([2609.36655](https://arxiv.org/abs/2609.36655)) stops corrections by estimated gain; this stops by fixed-point arrival.
- **Cheapest first test:** Compare to a fixed round count and an oracle A-labelled stop at equal max cost; also run on A-naive hosts, where displacement should fall without A appearing (this separates "wake finished" from "nothing to wake").
- **Old-task retention check:** A after stop; C; B after stop.

### C. Proving the wake before granting the lease

#### 16. Proof-carrying lease on a shadow fork (primitive)

- **Mechanism:** Before granting, fork the host, let an adversarial B-writer move it as far as the lease allows, apply `W`, and check a fixed audit set. Grant only if the worst case passes. The audit set's bytes and labels are charged; every baseline gets the same set as replay data.
- **Nearest art / delta:** Relearning attacks on unlearning probe worst-case revival; adversarial weight perturbation ([AWP](https://arxiv.org/abs/2004.05884)) trains for robustness to weight attacks. Here the attack checks a lease, and the key control is DER++ with the audit set as its buffer.
- **Cheapest first test:** Compare proof-carrying leases to replay with the same audit set, GPM, and leases granted without proof. Reject if replay ties at equal bytes.
- **Old-task retention check:** Fresh A queries disjoint from the audit set; C; B after wake.

#### 17. Twin-polarity proof without labels (primitive)

- **Mechanism:** Certify `W` on development histories by showing it revives opposite labels on A⁺/A⁻ twin hosts (so it carries no answer) and keeps A-naive hosts naive. On the live host, grant the lease based only on `W`'s certified class and label-free host statistics (card 3/11), never on live A labels.
- **Nearest art / delta:** PR #139 card 10 (matched A-naive control) and PR #142's paired-polarity rule are tests of a word. Using them as a transferable licence for write rights is new.
- **Cheapest first test:** Freeze certification on development rule generators; test on held-out generators and B drift schedules. Compare to leases certified on A labels of the live host (non-deployable upper bound).
- **Old-task retention check:** Live-host A per polarity after `W`, C and B, with certificate failures reported.

#### 18. Worst-case B-writer as a lease adversary (primitive; audit)

- **Mechanism:** Train a B-writer within the lease's rules (same radius and directions) whose objective is B loss plus a penalty for `W` succeeding. The lease is safe for the rules if even this writer cannot break `W` without giving up B.
- **Nearest art / delta:** PR #135 uses past selves as adversaries to find regressions; this adversary targets the wake, not A directly.
- **Cheapest first test:** Compare the adversary's achievable wake failure with ordinary B training and random writes of equal norm. Rules that the adversary breaks at little B cost are rejected before any deployment test.
- **Old-task retention check:** A after `W` on adversarial states; C; the adversary's B loss to confirm it stayed within rules.

#### 19. Statistical lease certificate (improvement)

- **Mechanism:** Sample N lease-reachable states (random B minibatch orders, seeds, step counts), apply `W`, and certify a failure rate `≤ ε` with a Clopper–Pearson bound before granting. Cost scales with N; compare with the deterministic certificate of card 11.
- **Nearest art / delta:** Scenario approach in robust control ([Campi & Garatti](https://doi.org/10.1137/07069821X)); applied here to wake success over a lease's randomness.
- **Cheapest first test:** Check bound calibration on held-out histories; compare cost and tightness to card 11 and to no certificate.
- **Old-task retention check:** Observed A failure rate on held-out leases versus the certified `ε`; C and B.

### D. When is a lease worth it?

#### 20. Lease versus release plus saved delta: the break-even (primitive; audit)

- **Mechanism:** A lease costs wake steps, fork checks and collateral; release plus an equal-byte saved delta costs bytes and a restore. Derive and measure the break-even: a lease wins only if the bytes the basin saves exceed the wake and proof costs. This is the node's go/no-go audit.
- **Nearest art / delta:** NSR ([2606.30067](https://arxiv.org/abs/2606.30067)) stores compressed LoRA subspaces and retrieves them, about 0.29 MB per task. This asks when not storing beats storing.
- **Cheapest first test:** Sweep saved-delta bytes and lease radii on the MLP; plot post-wake B at matched A/C floors against total cost; find the region, if any, where leases dominate.
- **Old-task retention check:** A after restore versus after `W`, C and B under both regimes.

#### 21. Critical lease rank (primitive; audit)

- **Mechanism:** As the rank of leased directions grows, wake success may drop sharply at a critical rank `k*`. Predict `k*` from label-free quantities (card 3's radius, the access/payload split of card 2) before B trains.
- **Nearest art / delta:** Rank-sweep release appears in PR #142 #1; ledger kills of capacity laws (N* in PR #22, plasticity reserve in PR #9) mean the prediction must beat a constant guess and a first-10% fit.
- **Cheapest first test:** Gate first: the transition must exist and be sharper than seed variance. Only then compare the predictor to the constant and early-fit controls.
- **Old-task retention check:** A after `W` per rank, C, B.

#### 22. Multi-tenant leases with one wake (primitive)

- **Mechanism:** Several old skills each lease directions to B. One frozen `W` (PR #142's universal word) must wake all of them at once. Allocate leases so their basins overlap (shared access directions) and avoid leasing directions where two skills' wakes conflict.
- **Nearest art / delta:** PR #142 #8/#17 test one word across hosts and co-resident skills; here the allocation of write rights is chosen to make one word suffice.
- **Cheapest first test:** Four co-resident A skills; compare overlap-aware allocation with independent per-skill leases and GPM, at equal B progress and one wake call.
- **Old-task retention check:** All four A skills, C and B on the same post-wake copy; worst-skill margin.

## Ranked deeper questions

1. **Does a lease beat projection after paying for the wake?** Cards 1, 2 and 20. At matched post-wake A/C floors and equal bytes, steps and latency, a lease must give more post-wake B than GPM, TRGP, SGP and FS-DGPM, must fail in the linear host, and must lose with a sham `W`. If tuned TRGP or release plus saved deltas ties, the node has no capacity primitive.
2. **Is idempotence label-free evidence of a safe wake, or are wrong fixed points common?** Cards 10, 15 and 11. Measure how often low displacement coexists with wrong or collapsed A in lease-reachable states. If the attainable error at the deployment threshold is high, idempotence is only a cost saver for wakes, not a licence for leases.
3. **Can a lease be proved without the proof turning into replay?** Cards 16, 17 and 18. Proof-carrying leases must beat DER++ given the same audit set; twin-polarity certification must transfer to held-out rule generators; adversarial B-writers must fail to break `W` cheaply.
4. **Do repeated lease cycles drift?** Cards 13, 6 and 7. Over 20 or more cycles, per-cycle drift in A's hidden distinction and in B's gain must stay below the seed floor; otherwise leases are a slow form of forgetting.
