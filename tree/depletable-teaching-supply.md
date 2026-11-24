# Depletable teaching supply: count the joint steps that are left, and charge the step that opens the gate

**Status:** Ideas only; no implementation, experiments, or GPU work. **Parent:** [Shared-coverage bounds](shared-coverage-bounds.md) ([PR #201](https://github.com/manojbajaj95/cl/pull/201)). **Review seeds:** [Flood triage, row 310](https://github.com/manojbajaj95/cl/blob/001a806da6727594d1958f976804e1d55d24cdff/reviews/flood-triage.md#L310) kept parent **#03** (count remaining high-overlap joint teaching transitions as a consumable entitlement instead of charging worst-case overlap per step) and **#04** (verify Bellman inequalities on a signed progress potential with gate readiness as a coordinate, so the gate-opening step is charged for the discharge it enables, and test whether the readiness predicate ports across update laws without refitting) at score 3. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/001a806da6727594d1958f976804e1d55d24cdff/reviews/idea-ledger.md).

## What would count as a new object?

**Not a consumable-resource heuristic or a planning potential.** [Operator-counting heuristics](https://ojs.aaai.org/index.php/ICAPS/article/view/13581) (Pommerening et al. 2014) already bound how often each operator can fire; [potential heuristics](https://ojs.aaai.org/index.php/AAAI/article/view/9654) (Pommerening, Helmert, Röger, Seipp 2015) already verify per-operator inequalities on a state potential; [generalized potential heuristics](https://www.ijcai.org/proceedings/2019/0771.pdf) (Francès et al. 2019) already transfer one potential across all instances of a planning domain; Petri-net place invariants already certify conserved and depletable token counts; amortized analysis (Tarjan 1985) already charges an expensive operation to the potential that earlier operations built; [Lyapunov functions for first-order methods](https://arxiv.org/abs/1705.04398) (Taylor, Van Scoy, Lessard 2018) and IQCs (Lessard, Recht, Packard 2016) already certify one potential across a class of optimizers; a common Lyapunov function already certifies a switched system under every switching law. [Learned cost partitioning](https://arxiv.org/abs/2606.04597) is the 2026 neighbour found on alphaXiv. The parent concedes iterative and multi-learner machine teaching, GCR, cost partitioning and robust reachability.

The bet is narrower: a **teaching-step lower-bound certificate for continual learning** whose two extra coordinates, a *joint-teaching supply* `S` and a *gate readiness* `g`, are defined on law-invariant observables of the learner (what joint discharge is still reachable, and within how many steps), so that the same certificate checks against a new update law (optimizer, LR schedule, lag, batching) by re-verifying local inequalities, without refitting weights or re-solving the teaching game, and still keeps old tasks A/C above their floors at every live prefix. Counting consumables or charging openers alone is not new; porting the counted object across update laws in a learner whose old tasks are protected might be.

### The two invariants

Freeze everything the parent freezes (truthful pool, presentation atom, order/repeat rules, hidden-history envelope, free transcript, reply menu, A/C and new-utility floors). Let `z=(z_A,z_C)` be the discharged pre-reply obligations with demand `d=(d_A,d_C)`.

- **Supply.** `S(h)` = an upper bound on the number of high-overlap joint transitions still lawful from history `h`. Certify `λ·Δz − μ·ΔS ≤ c` on every reachable lawful step (`ΔS ≤ 0` for ordinary joint steps, `ΔS > 0` only for a step that *pays* for replenishment). Telescoping gives `k ≥ ceil((λ·d − μ·S_0 + μ·S_end)/c)`, and the bound must be combined (by max) with the per-skill bounds `k ≥ d_i/c_i`. A replenishing step that also discharges breaks the inequality, and the cap must then be voided, not silently kept.
- **Readiness.** `Φ = λ·z + ρ·g`, where `g` encodes "a joint step is reachable within the law's delay". Charge the opener: `ΔΦ ≤ c` on the opening step means it earns readiness, and the joint step that consumes readiness pays it back (`ρ·Δg < 0`). Simultaneous credit for readiness and for the discharge it enables is forbidden unless the inequality allows it. Porting across laws = re-checking `ΔΦ ≤ c` on the new law's transitions with `ρ`, `λ`, `g`'s definition frozen; a failure is a reported refutation, not a refit.

### Two paper fixtures, checked by exhaustive search (not pilot results)

A throwaway BFS (not committed; tiny state spaces) checked both.

**F1. Supply makes the joint bound exact, and a free reset must void it.** Actions: `a` (+1 A), `c` (+1 C), `j` (+1 A, +1 C, needs `S>0`, `S−=1`), optional `r` (`S+=1`, no discharge). Worst-case per-step charging gives `k ≥ ceil((d_A+d_C)/2)`. With `Φ = z_A+z_C+S` every step has `ΔΦ ≤ 1`, so `k ≥ d_A+d_C−S_0`, combined by max with `max(d)`.

| demand | `S_0` | exact optimum | worst-case bound | supply bound (max with per-skill) | optimum with paid reset `r` | optimum with free reset bundled into `a` |
|---|---|---|---|---|---|---|
| (2,2) | 0 | 4 | 2 | 4 | 4 | 3 |
| (2,2) | 1 | 3 | 2 | 3 | 3 | 3 |
| (3,3) | 1 | 5 | 3 | 5 | 5 | 4 |
| (4,1) | 2 | 4 | 3 | max(3,4)=4 | 4 | 4 |

The paid reset leaves the bound tight because `r` itself has `ΔΦ=1`. The bundled reset (`a` plus `S+=1`) has `ΔΦ=2`, the optimum really drops (4→3 at `(2,2), S_0=0`), and the certificate must fall back to the sound but weak `ceil(4/2)=2`.

**F2. The readiness coordinate must be defined on the law-invariant event, not the law's flag.** Opener `o` sets readiness; `j` needs an open gate, gives (+1,+1) and closes it. Law L0: `o` opens the gate immediately. Law L1 (one-step lag): `o` sets pending `p`, which becomes open `g` after the next step. Exact optima for demand (2,2) are 4 under both laws, (3,3) gives 6 under both, while the uncharged "joint counts double" bound is 2.

| potential | max `ΔΦ` under L0 | max `ΔΦ` under L1 | bound under L1 |
|---|---|---|---|
| `z_A+z_C+g` | 1 (exact bound 4) | **2** (inequality fails) | refuted, no bound |
| `z_A+z_C+g+p` | 1 (same as above on reachable L0 states, where `p=0`) | 1 | 4 (exact) |

So the reviewer's "one-step-lag law where the old inequality must fail" is real for the flag-based predicate and not for "open or pending". Whether a law-invariant definition exists for realistic update laws (momentum, Adam, LR warmup) is the open question, not a result.

**Blind comparison (all cards).** Freeze certificates before seeing held-out update laws. Compare with augmented-state exact search (offline truth), operator-counting LP, potential heuristics refit per law, generalized potential heuristics fitted on source laws, worst-case per-step charging, fixed cost partitioning, and the parent's best stack (cost partitioner + generic proof reuse). Naive summation is the unsound negative control. Charge certificate bytes, verification, failed ports and fallback. Check ordinary old A/C tasks and worst slices at every live prefix, at transient open-gate states, and after resets. Ledger constraints: no Gramian or plasticity-reserve chooser, no functional-syndrome retention sketch, no bounded-delay reordering claim (gradient accumulation removes order effects at equal latency), and the [PR #113](https://github.com/manojbajaj95/cl/pull/113) smooth no-cliff control for any timing claim. A tie with exact search plus re-verification is not a primitive.

## Idea cards

**P** = candidate primitive, conditional on beating the stacked control; **I** = improvement, audit or falsifier.

### Count the supply

#### 01. A portable joint-supply certificate (P)
- **Mechanism:** Ship `(λ, μ, c, S-definition)` with the bound; the importer only checks `λ·Δz − μ·ΔS ≤ c` on its own lawful transitions and reads `S_0` from its own state.
- **Novelty vs nearest prior art:** Operator counting bounds operator uses per instance; here the counted object is joint teaching discharge in a learner with protected old skills, and the certificate is meant to move between learners.
- **Cheapest first test:** F1 plus a renamed learner where `j` is realized by a different truthful example; compare with operator-counting LP and exact search at equal bound quality.
- **Old-task retention check:** Verify A/C floors after every joint step, since a joint example that discharges both obligations may still damage a third old slice.

#### 02. Supply that the learner's own training depletes (P)
- **Mechanism:** Let ordinary new-task SGD close joint opportunities (e.g. a shared feature saturates); define `S` as the remaining joint-discharge capacity of that feature, certified as non-increasing under the new-task updates.
- **Novelty vs nearest prior art:** Plasticity-loss work measures lost capacity after the fact; the candidate turns it into a sound budget term of a teaching lower bound.
- **Cheapest first test:** Two-unit ReLU toy where a shared unit's slack shrinks with each B step; check whether the bound tracks the true rising optimum better than a fixed-overlap bound.
- **Old-task retention check:** Hold A/C margins matched across arms; the supply drop must not be explained by A already being forgotten.

#### 03. Price replenishment, or void the cap (P)
- **Mechanism:** Every supply-raising transition must appear in the certificate with its own charge; any unlisted replenishing step found by the importer voids the supply term and falls back to the worst-case bound.
- **Novelty vs nearest prior art:** Resource planning has producers and consumers; the specific bet is a refusal rule that keeps the bound sound under unseen reset mechanisms (warm restarts, re-initialization, LR re-warmup).
- **Cheapest first test:** F1 with paid and bundled resets (table above); add a warm-restart LR schedule as a natural replenisher and check the rule fires.
- **Old-task retention check:** Audit A/C at the reset state itself; a reset that regains joint supply by re-plasticizing may forget A.

#### 04. Supply per overlap class, not one scalar (I)
- **Mechanism:** Keep a vector `S_k` for joint-discharge classes `(A,C)`, `(A,E)`, `(C,E)`; certify each class separately, combine by LP.
- **Novelty vs nearest prior art:** This is operator counting with landmarks; it measures what a scalar supply loses.
- **Cheapest first test:** Three skills with pairwise joint examples of supply 1 each; compare scalar, vector and exact optima.
- **Old-task retention check:** Check all three old skills; a vector that looks tight on A/C can hide E's slice.

#### 05. Supply that survives a changed presentation atom (I)
- **Mechanism:** Re-express `S` in units of truthful presentations, not records, so batching two records into one does not double the apparent supply.
- **Novelty vs nearest prior art:** Parent card 06 audit applied to supply; guards against inventing supply by repackaging.
- **Cheapest first test:** Present `j`'s two halves as one batched record versus two; require `S` to count both arms identically when the interface is frozen.
- **Old-task retention check:** Compare prefix retention in both arms, including a loss-normalization change that hits C only.

#### 06. Hidden supply under an information set (P)
- **Mechanism:** When the remaining supply depends on hidden history, certify `S ≤ max over compatible histories` and update it only on public evidence.
- **Novelty vs nearest prior art:** Conformant planning handles hidden state; the bet is a supply term that tightens only when truthful teaching reveals it, without an oracle.
- **Cheapest first test:** Two hidden lanes with supply 0 and 2; compare the max-supply bound with a priced oracle and with conformant exact search.
- **Old-task retention check:** Check A/C on every still-compatible lane, including one where a joint step is unsafe.

#### 07. Spend-order freedom: which joint steps to keep for later (P)
- **Mechanism:** Certify not just how many joint steps remain but that any lawful order of spending them gives the same bound, so a scheduler can postpone them to protect old tasks.
- **Novelty vs nearest prior art:** Partial-order reduction proves order irrelevance for verification; here order freedom is the deliverable to a retention-aware scheduler.
- **Cheapest first test:** Joint steps with order-dependent A damage; verify the bound is order-invariant while A damage is not, and that a scheduler exploits it.
- **Old-task retention check:** Compare A/C under the earliest and latest spend orders at matched B gain; the ledger's bounded-delay kill applies unless the order changes something gradient accumulation cannot.

#### 08. A supply that two learners share (P)
- **Mechanism:** When two learners will be merged, the joint-teaching supply of shared truthful examples is one pool; certify the split so no example is credited to both.
- **Novelty vs nearest prior art:** Merge-aware budgets ([PR #181](https://github.com/manojbajaj95/cl/pull/181)) reserve interaction allowances; this reserves teaching supply.
- **Cheapest first test:** Two learners sharing one joint example; compare naive double crediting, an exact joint plan and the certified split.
- **Old-task retention check:** Verify A/C on the merged model and on each learner before merging.

### Charge the gate opener

#### 09. Readiness on the law-invariant event (P)
- **Mechanism:** Define `g` as "a joint step is reachable within the law's declared delay" (F2's `g+p`), not as an internal flag; ship it with `λ, ρ, c`.
- **Novelty vs nearest prior art:** Generalized potential heuristics transfer across instances of one domain; this transfers across update laws of one learner, which changes the transitions themselves.
- **Cheapest first test:** F2 with L0/L1, then L2 (two-step lag) and L3 (gate decays if unused for one step); check the frozen certificate passes, fails or weakens exactly where exact search says it should.
- **Old-task retention check:** Check A/C at the transient open state under each law; a lag can leave the model in a gate-open state longer.

#### 10. Readiness that decays (P)
- **Mechanism:** If an unused open gate closes, `ΔΦ` on the closing step is `−ρ`; certify that the decay can only weaken, never strengthen, the bound, and price re-opening.
- **Novelty vs nearest prior art:** Amortized analysis assumes stored potential persists; decay is the CL-specific case (momentum and second moments decay).
- **Cheapest first test:** L3 above; compare against exact search and a refit potential heuristic.
- **Old-task retention check:** Verify A/C after a decayed, re-opened gate; repeated opening may accumulate damage.

#### 11. Optimizer state as the gate (P)
- **Mechanism:** Let readiness be a momentum or Adam second-moment condition that makes the next joint example effective; the opener is a truthful batch that prepares that state.
- **Novelty vs nearest prior art:** Optimizer-slot splits and splices ([PR #178](https://github.com/manojbajaj95/cl/pull/178), [PR #185](https://github.com/manojbajaj95/cl/pull/185)) move slot state; this charges a teaching step for preparing it.
- **Cheapest first test:** Heavy-ball toy where momentum along a shared direction lets one example discharge two obligations; compare with refitting the potential per β and with a clock-matched optimizer control (2606.29554).
- **Old-task retention check:** A/C after the preparing batch and after the joint step; momentum aimed at the shared direction may overshoot A.

#### 12. Port across LR schedules without refitting (P)
- **Mechanism:** Write `c` as a function of the step's learning rate declared in the schedule; the importer checks inequalities per step with the schedule substituted.
- **Novelty vs nearest prior art:** PEP/IQC certificates already parameterize by step size for convex objectives; the bet is a teaching bound, on a non-convex toy, with old-task floors.
- **Cheapest first test:** Constant, cosine and warmup schedules on a two-skill linear toy; compare to refit-per-schedule potentials and exact search.
- **Old-task retention check:** Match A/C headroom at the start of each schedule; warmup's small steps should not count as retention.

#### 13. Charge the opener in both legal orders (I)
- **Mechanism:** Verify the potential on both orders of gate-opening and a regression step (as the reviewer asked); report which order makes the opener pay more.
- **Novelty vs nearest prior art:** Audit; partial-order bounds already do this.
- **Cheapest first test:** Gate `o` and an A-regression step `x` in both orders; check exact optima and the potential in each.
- **Old-task retention check:** Check A at the regression step in both orders; the potential must not credit discharge that `x` undid.

#### 14. Refuse double credit with an explicit exclusion witness (P)
- **Mechanism:** Whenever a certificate claims both readiness credit and later discharge for one step, require a reachable two-path witness showing the credit is disjoint; otherwise collapse to one.
- **Novelty vs nearest prior art:** Parent card 21 carries proofs of non-sharing; this is the readiness-side analogue that keeps the opener charge sound.
- **Cheapest first test:** A step that opens the gate and also discharges A; plant a law where both credits are lawful and one where they are not.
- **Old-task retention check:** Verify A/C along both witness paths.

### Couple the two

#### 15. Supply and readiness in one potential (P)
- **Mechanism:** `Φ = λ·z + μ·S + ρ·g`; one inequality per transition covers gates that open joint supply and joint steps that consume both.
- **Novelty vs nearest prior art:** Potential heuristics combine features linearly; the bet is that these two CL-specific features are enough for exact bounds on a family of gated teaching problems.
- **Cheapest first test:** Combine F1 and F2 (joint steps need an open gate and positive supply); compare exact optima, the combined potential and each part alone.
- **Old-task retention check:** A/C at the open-gate, last-supply state, the most stressed prefix.

#### 16. Find the law-invariant features automatically (P)
- **Mechanism:** Search a small feature grammar (gate open, pending within d, supply remaining) for the potential that passes inequalities on several source laws simultaneously, then freeze it.
- **Novelty vs nearest prior art:** Generalized potential heuristics learn description-logic features over instances; this learns over update laws and is judged on a held-out law.
- **Cheapest first test:** Fit on L0+L2, test on L1 and L3; compare with refitting per law and with a common-Lyapunov SDP.
- **Old-task retention check:** Run the frozen bound's suggested shortest sequence on the held-out law and check A/C at every prefix.

#### 17. The bound as a stopping signal for teaching (I)
- **Mechanism:** Use `Φ_remaining / c` as a sound countdown: stop searching for shorter curricula once the incumbent meets it.
- **Novelty vs nearest prior art:** Branch-and-bound already does this; it prices how often the specialized bound prunes more than LP bounds.
- **Cheapest first test:** Count nodes expanded by A* with the combined potential vs operator-counting LP on F1/F2 variants.
- **Old-task retention check:** The incumbent's A/C floors are checked independently; a pruned search must not skip a retention-safe shorter sequence.

#### 18. Gate openers that are also old-task replay (P)
- **Mechanism:** Choose an opener that is a truthful A replay example; its readiness credit and its retention benefit are certified separately, so the bound charges teaching cost honestly while retention improves.
- **Novelty vs nearest prior art:** Replay is old; the bet is that the potential lets replay double as gate preparation without double counting.
- **Cheapest first test:** Compare a pure opener, a pure replay step and a replay-opener at equal steps on A retention and bound tightness.
- **Old-task retention check:** This is the retention check; also measure C, which replay of A may hurt.

### Audits and falsifiers

#### 19. Lag ladder audit (I)
- **Mechanism:** Sweep delay d = 0..4 with the frozen `g+p` style readiness; record the first d where the certificate fails.
- **Novelty vs nearest prior art:** Falsifier for card 09's portability claim.
- **Cheapest first test:** F2 extended to d=4 by exhaustive search.
- **Old-task retention check:** A/C at each d's open state.

#### 20. Supply-inflation attack (I)
- **Mechanism:** An adversarial importer adds a lawful step that raises `S` at no listed charge; check the void rule fires on every such step.
- **Novelty vs nearest prior art:** Soundness audit for card 03.
- **Cheapest first test:** Random lawful transition additions to F1; count missed voids (must be zero).
- **Old-task retention check:** Check A/C after the attack step; inflation through re-initialization should show up as forgetting.

#### 21. Margin-matched comparison (I)
- **Mechanism:** Any claim that the certified curriculum retains A/C better must match per-item margins before attributing it to the bound.
- **Novelty vs nearest prior art:** Ledger margin-confound pattern applied here.
- **Cheapest first test:** Pair curricula with equal initial A/C margins on the F1/F2 toys realized as linear learners.
- **Old-task retention check:** Margin-matched A/C after the reply.

#### 22. Compile-away tournament (I)
- **Mechanism:** Freeze interface; compare the supply/readiness certificate against operator-counting LP + per-law potential refit + exact search cache on held-out laws, counting checks, bytes, failed ports and fallbacks.
- **Novelty vs nearest prior art:** Falsifier: if the stack ties at equal bound and cost, the node has no primitive.
- **Cheapest first test:** Three held-out laws (lag, decay, batched joint atom) on F1+F2 combined.
- **Old-task retention check:** Same independently verified serving bundles and A/C floors in all arms.

## Ranked deeper questions

1. **Does a law-invariant readiness definition exist beyond toy lags?** Under momentum, Adam and LR warmup, can one frozen `(λ, μ, ρ, g-definition)` pass the local inequalities on held-out laws and stay within one step of exact optima, where refit potentials and operator-counting LP need per-law work? This decides whether card 09 is a primitive.
2. **Can the learner's own training be certified as a supply drain?** Find a shared feature whose joint-discharge capacity provably falls under new-task updates, so the teaching bound rises in step with real plasticity loss and beats a fixed-overlap bound, at matched A/C margins (card 02).
3. **Which replenishers occur naturally in CL, and does the void rule catch all of them?** Warm restarts, re-initialization, LR re-warmup and optimizer resets; each either has a certified charge or voids the cap, with A/C checked at the reset (cards 03 and 20).
4. **Is the combined potential ever strictly better than the parent's best stack at equal total work?** Run card 22 on blind laws; failed ports count.

**Verdict:** Both seeds stay conditional. F1 shows a supply term makes the joint bound exact where worst-case charging is loose by half, and that a free reset must void it. F2 shows the flag-based readiness coordinate fails under a one-step lag while the "open or pending" coordinate ports unchanged. Neither is new as planning or amortized analysis; the candidate primitive is the update-law-portable teaching certificate with A/C floors, and it counts only if it beats operator counting + refit potentials + exact search caching on held-out laws.
