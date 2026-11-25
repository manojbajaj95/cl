# Route-merged folds: one paid fold for several routes, optimizer state leased for a declared horizon

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Work–memory folds](work-memory-folds.md) ([PR #269](https://github.com/manojbajaj95/cl/pull/269)). **Review seed:** [Flood triage, row 386](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L386), score-3 cards #269#08 (one paid fold serving several declared successor routes, merging only states no route can tell apart, with no route tag) and #269#10 (price carried optimizer state for a declared horizon, with an explicit expiry).

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). State an actual discrete transition, not a gradient-flow invariant (Noether-memory kill). A tied save/restore or an equality built into a toy is not a result. Merge cards must beat the union of their parts' baselines stacked at equal resources. Every first test must show that old tasks still work. **P** means a candidate reusable operation; **I** means an improvement or falsifier. Neither label means novelty has been established.

## What would be new?

Both seeds ask the same question along two axes: **which readers is a fold accountable to?** Seed #08 widens the set of readers across routes (any of several declared successors may arrive). Seed #10 limits it in time (only readers within H future updates count). In a linear or finite model both axes add rows to one observability relation: a route set R with horizon H gives the stacked map `O_{R,H}(s) = (reader_r(step_t(s)))` for r ∈ R and t < H. The cheapest exact fold merges states with equal `O_{R,H}`. That much is classical: Myhill–Nerode/bisimulation minimisation, Kalman observability, k-step (finite-horizon) lumpability, multiple-input lumpability.

The candidate learning operations are the parts the classical picture does not give:

- **Route merge as a priced purchase, not a prediction.** The learner keeps one tagless fold whose classes are the *meet* of the routes' partitions, and pays for it only when that meet fits the slot. Unlike best-route pruning or an oracle route tag, it never has to guess which successor comes. It is useful only when required C work makes the routes' partitions *line up* (nested or equal), so the meet is no finer than the coarsest route needs.
- **A lease on optimizer state with a lawful end.** The fold is certified only for H updates. At expiry the learner must already hold a renewal state that does not rely on the merged-away distinctions, or refuse the late reader. The point is that renewal has to be **bought before the merge**: once two states are merged, no later payment can separate them again. Expiry is a commitment, not a timeout.
- Nearest recent prior: [Delayed Optimizer-State Transport Shapes Short-Horizon Training Decisions](https://www.alphaxiv.org/abs/2608.24593) shows that moment history changes short-horizon decisions (it measures the effect; it does not price or certify a horizon). [Quantised-state staleness and resets](https://www.alphaxiv.org/abs/2603.16731) studies stale optimizer state and resets. [Guarded Compression of Adam State](https://www.alphaxiv.org/abs/2611.00589) bounds error at a fixed restore. [Backpropagated Output Momentum](https://www.alphaxiv.org/abs/2609.36738) moves history into task space. [Optimizer Memory Schedules](https://www.alphaxiv.org/abs/2609.04577) varies optimizer memory with the training horizon. Leases and TTL caches (Gray & Cheriton 1989) give expiry semantics. None of these merges exact optimizer state across routes, and none ties a purchased horizon to a pre-paid renewal. alphaXiv was searched for optimizer-state merging and finite-horizon optimizer state; no direct match was found, which is not proof of absence.

## Contract

- Inherit the [parent contract](work-memory-folds.md#contract): pinned host, split, decoder and fold family, arithmetic and RNG, eligible causal C policies, standardized batches, worst-case serialized payload M, A/B/C floors at matched service milestones, a preset price λ, and the stacked control.
- **Routes.** Before results, declare the finite route set R (each route is a successor update class U_r together with its readers) and the eligibility of each route at each cut. A route that might arrive counts, including unlikely ones. A tagless fold must give exact continuation for every r ∈ R. Any route-revealing bit the learner can read (a schedule field, a batch ID, a clock) is charged in M unless it is truthfully common to all routes.
- **Horizons.** Declare H in counted optimizer updates (not wall time), the reader classes counted inside H, and the expiry action: (a) refuse late readers, (b) switch to a renewal state that was certified and paid for before the fold, or (c) fall back to a declared reset whose A/B/C cost is reported. A horizon cannot be extended after the fold unless the extension's certificate uses only the stored state.
- **Prices.** Under λ, a candidate is `(R, H, k, M_{R,H,k}, renewal bytes, refusal set)`. Score `M + λk + μ·renewal + ν·refusals`, with μ and ν fixed before the traces. Report the frontier over (|R|, H), not just the winner.
- **Controls.** One fold per route with an oracle tag (cost floor for prediction); one fold per route with a paid tag and separate decoders; best-route pruning; indefinite-horizon minimal fold (#269#01); horizon-indexed refunds (#251#04); a slot reset at expiry; quantised or low-rank optimizer state at equal bytes with its exact error; a route set whose meet exceeds the slot; a consumer that arrives one update after H. The stacked control is the best causal C prefix, plus per-route exact transport with a paid tag, plus an indefinite fold with a reset at H, at equal C data, width-steps, information and evidence.

## One exact paper check (not a learner result)

Two momentum slots `m = (m₁, m₂) ∈ {0,1,2,3}²` with decay 1/2 and 1/4 (two parameter groups with different β), and no further gradient on them. Route A reads the summed contribution `u_t = m₁/2ᵗ + m₂/4ᵗ`; route B reads a signed head `w_t = m₁/2ᵗ − m₂/4ᵗ`; route C reads `2u_t` (a rescaled copy of A's head). A reader at step t < H can see its route's value. Classes are counted exactly with `Fraction` over all 16 states.

| Route set | H = 1: classes / bits | H ≥ 2: classes / bits | Oracle tag (bits) | Separate folds (bits) |
|---|---:|---:|---:|---:|
| {A} | 7 / 3 | 16 / 4 | — | — |
| {A, C} | 7 / 3 | 16 / 4 | 3 + 1 | 6 |
| {A, B} | 16 / 4 | 16 / 4 | 3 + 1 | 6 |

- **Route merge works only when the partitions line up.** A and C read the same partition, so one tagless 3-bit fold (the sum `s = m₁ + m₂`, decoded as `(s, 0)`) serves both. That beats the paid tag (4 bits) and separate folds (6 bits). A and B are complementary: their meet is the full grid, so the tagless fold costs 4 bits. That is no better than the paid tag and saves nothing over keeping the raw state. This is the reviewer's "route set whose joint quotient exceeds the slot".
- **Routes and horizons trade one for one here.** Two complementary routes at H = 1 cost exactly what one route costs at H = 2, because both add independent rows to the same observability relation.
- **Expiry is real and cannot be renewed after merging.** The merged pair (1,0) and (0,1) agrees at t = 0 (u = 1) but separates at t = 1 (1/2 vs 1/4). With the `(s, 0)` decoder, the worst update error at t = 1 is 3/4 (state (0,3)). A 3-bit H = 1 lease is exact until expiry. After it, no payment recovers the lost distinction: renewal must be the 4-bit state bought up front, or a declared reset or refusal.
- Nothing here is a learner result. The decays, readers and public schema are chosen, and there is no width release, no A task and no C work. The check only shows that both seeds are well defined, that the tagless merge can strictly beat a paid tag, and that it gives no saving at all on complementary routes.

## Idea cards

### 01. Pay once for a fold every declared route can continue from (P; seed #08)
- **Mechanism:** Compute the meet of the per-route continuation partitions over all declared routes; fold with no route tag only if the meet fits the priced slot, otherwise keep the wider state or refuse.
- **Novelty vs nearest prior art:** Restates #269#08. Multiple-input lumpability gives the partition; the new part is buying it at a posted price instead of predicting the route (best-route pruning) or paying a tag.
- **Cheapest first test:** The paper check's {A,C} vs {A,B}, then a 3-parameter momentum host with two real successor losses; compare the oracle tag, a paid tag, separate folds and a reset.
- **Old-task retention check:** Run A after each route, including the least likely one, and report the worst A drift over routes.

### 02. Lease optimizer state for H updates with a stated end (P; seed #10)
- **Mechanism:** Certify exact continuation only for H counted updates; at H switch to a renewal state certified before the fold, or refuse late readers.
- **Novelty vs nearest prior art:** Restates #269#10. Finite-horizon lumpability and leases are known; the candidate is a width buyback whose expiry action is part of the purchase, unlike 2608.24593 (measures horizon effects) or 2603.16731 (resets after staleness).
- **Cheapest first test:** The paper check at H = 1: 3-bit lease plus 4-bit renewal bought up front vs 4 bits held throughout vs reset at t = 1 (error 3/4).
- **Old-task retention check:** Evaluate A just before expiry, at the first late reader, and after renewal or reset.

### 03. Spend C work to align the routes before folding (P)
- **Mechanism:** Choose required C batches whose updates map the reachable states so the per-route partitions become nested; then the meet equals the finest single route.
- **Novelty vs nearest prior art:** #269#01 shrinks one route's quotient. Here the target is the *gap* between the meet and the finest route, which is zero work for aligned routes and impossible for some complementary ones.
- **Cheapest first test:** Enumerate C orders on a 2-slot host where A and B start complementary; find a truthful C batch that collapses `m₂` on both heads, and compare against the same batch under per-route folds.
- **Old-task retention check:** Gate every prefix of the aligning C sequence on A, not just its end.

### 04. Prove when a route set can never share a fold (P)
- **Mechanism:** Certify that every eligible C policy within the budget leaves the meet larger than the slot, via an independent pair of histories separated by some route at every reachable cut.
- **Novelty vs nearest prior art:** #269#03 gives one-route impossibility witnesses; this is a cross-route obstruction that justifies a tag or refusal without search.
- **Cheapest first test:** A and B in the paper check under all one-batch C actions with integer gradients; certify the 4-bit floor or find a counterexample.
- **Old-task retention check:** Exclude only histories already ruled out by the precommitted A floors.

### 05. Price the route tag only where the routes disagree (P)
- **Mechanism:** Keep a shared fold for the meet of agreeing routes and a partial tag that is read only by the disagreeing ones, charging the tag in M.
- **Novelty vs nearest prior art:** A hybrid between a tagless merge and a full tag; standard in prefix codes, new only if C work can move routes from the tagged block to the shared one.
- **Cheapest first test:** {A, B, C}: share A/C, tag B; compare with a full tag and a tagless 4-bit fold.
- **Old-task retention check:** Check A under the tagged route specifically, since the tag can leak route identity into the learner.

### 06. Let a route expire out of the merge (P)
- **Mechanism:** Give each route its own horizon; when a route's last eligible arrival passes, re-certify a coarser meet and release bytes without new evidence.
- **Novelty vs nearest prior art:** Combines both seeds. The coarsening is lawful because it only drops rows from the observability relation; the claim to test is that this releases bytes earlier than a fixed-horizon lease.
- **Cheapest first test:** Routes A and B with B eligible only before step 1; show the fold drops from 4 to 3 bits after B's window closes.
- **Old-task retention check:** Evaluate A right after the release and under a late B that tries to arrive anyway (it must be refused).

### 07. Buy renewal before the merge, never after (P)
- **Mechanism:** Treat renewal bytes as a call option paid at fold time; a renewal state computed afterwards from the merged state is invalid unless it is certified using only that state.
- **Novelty vs nearest prior art:** Lease renewal is classical; here the information-theoretic point is that a merge is irreversible, so post-hoc renewal is impossible, not just expensive.
- **Cheapest first test:** In the paper check, compare a pre-paid 4-bit renewal, a post-hoc "renewal" from s (error 3/4 at t = 1), and a reset.
- **Old-task retention check:** A at the renewal step under both the true and the decoded state.

### 08. Charge the clock that announces expiry (P)
- **Mechanism:** Count the update counter used to trigger expiry as part of M unless it is truthfully common, and check that a lawful clock change cannot expose merged states early.
- **Novelty vs nearest prior art:** #269#18 charges clocks for bias correction; here the clock also carries the lease boundary.
- **Cheapest first test:** Adam bias correction with two counters merged under H = 2; a counter reset at step 1 must either be priced or refused.
- **Old-task retention check:** A after the counter event on each route.

### 09. Pick H by price, not by guess (I)
- **Mechanism:** Publish the frontier `M(H)` and a fixed μ for renewal; choose H minimising `M(H) + μ·renewal(H)` before seeing the traces.
- **Novelty vs nearest prior art:** An improvement on fixed-horizon leases; needs to beat the best fixed H chosen in hindsight by a margin.
- **Cheapest first test:** Three-decay host (1/2, 1/4, 1/8) where M rises 3→4→5 bits with H; compare policy vs hindsight on withheld arrival times.
- **Old-task retention check:** Include A drift during the horizon chosen, not only at its end.

### 10. Let rounding end the horizon for free (P)
- **Mechanism:** Under fixed precision, fast-decaying moments underflow; certify the step after which two merged states become exactly equal again and set H there so no renewal is needed.
- **Novelty vs nearest prior art:** Staleness work (2603.16731) treats quantisation error as noise; here underflow is used as a lawful collision that ends the lease at no cost.
- **Cheapest first test:** The paper check at 2 fractional bits; find the step after which `m₂/4ᵗ` rounds to 0 for all states and the merged pair's readers coincide.
- **Old-task retention check:** Compare A under exact and rounded arithmetic at the certified step.

### 11. One fold for routes that read through different heads (P)
- **Mechanism:** Merge across routes that read the same slots through different linear heads by folding onto the joint row space of their heads; charge the extra rank.
- **Novelty vs nearest prior art:** Observability for multi-output systems is textbook; the candidate is using C work to rotate heads into a shared row space before the fold.
- **Cheapest first test:** Heads A and C (shared row) vs A and B (complementary); add a C batch that changes B's effective head.
- **Old-task retention check:** A read through each head after the fold.

### 12. Merge routes that diverge only after a shared prefix (P)
- **Mechanism:** If all routes share their first j updates, fold for the shared prefix with H = j and attach a per-route continuation bought for the remainder.
- **Novelty vs nearest prior art:** Combines the seeds as a two-stage lease; like trie compression of continuations. It must beat a single fold for the longest route.
- **Cheapest first test:** Two routes with a shared first step and different second-step readers; compare total bytes and peak bytes.
- **Old-task retention check:** A at the divergence step under both routes.

### 13. Let the route reveal itself lawfully, then shrink (P)
- **Mechanism:** Keep the meet until the first truthful batch that identifies the route (as a public fact), then fold to that route's quotient; charge the waiting bytes.
- **Novelty vs nearest prior art:** A deferred decision, like late binding; competes with an oracle tag that knows the route at once.
- **Cheapest first test:** {A, B} where the first batch's label shows the route; compare bytes × steps against an oracle tag and a tagless 4-bit fold.
- **Old-task retention check:** A during the waiting period and after the shrink.

### 14. Lease state across a route switch mid-horizon (P)
- **Mechanism:** Certify a fold for "route r until step j, then route r′ until H", so mixed successors are covered without the full meet.
- **Novelty vs nearest prior art:** Switched-system observability; new only if the mixed schedule's quotient is strictly coarser than the meet and is reachable by real schedules.
- **Cheapest first test:** A then B switching at step 1 vs the full {A, B} meet at H = 2.
- **Old-task retention check:** A at the switch step.

### 15. Refuse a route rather than break the merge (P)
- **Mechanism:** When adding a route would make the meet exceed the slot, refuse it at the cut, report the refusal cost ν, and keep the cheaper fold for the rest.
- **Novelty vs nearest prior art:** Admission control is classical; the candidate is a refusal priced against bytes in the same objective, with refusals audited.
- **Cheapest first test:** {A, B, C}: refuse B and keep a 3-bit fold; compare against the 4-bit fold and against a paid tag.
- **Old-task retention check:** A under the refused route's fallback (reset or wait).

### 16. Reuse one receipt across all routes (P)
- **Mechanism:** One replay receipt for the C prefix (#269#02) plus one closure certificate per route; share the replay and charge per-route closure separately.
- **Novelty vs nearest prior art:** Proof-of-Learning replay is shared work; the question is whether the per-route closure checks cost less than a separate audit per route.
- **Cheapest first test:** Three routes, one shared two-batch prefix; compare against three separate audits with caching.
- **Old-task retention check:** Independent A evaluation at replayed states.

### 17. A receipt that expires with the lease (P)
- **Mechanism:** Bind the receipt to H so a verifier rejects any claim of exact continuation past expiry; delete evidence at expiry under a fixed evidence budget.
- **Novelty vs nearest prior art:** Expiring credentials are standard; the candidate links evidence lifetime to the certified horizon, freeing evidence bytes as well as optimizer bytes.
- **Cheapest first test:** Paper check: a receipt for H = 1 must reject a claimed t = 1 continuation of the merged pair.
- **Old-task retention check:** A at expiry with evidence deleted.

### 18. Merge across two learners that will receive the same successor (P)
- **Mechanism:** Two replicas or shards that will see identical future routes fold onto one shared optimizer state when their states are equivalent under all routes in R.
- **Novelty vs nearest prior art:** Optimizer-state sharing across replicas exists for memory (ZeRO, AdamPM); the candidate merges *different* states that no declared route can tell apart, which pooling does not certify.
- **Cheapest first test:** Two 2-slot learners with states (1,0) and (0,1) under route A at H = 1: one shared 3-bit state; under route B they must stay separate.
- **Old-task retention check:** Each learner's A after the merge, under each route.

### 19. Discount the tag by route probability, but stay exact (I)
- **Mechanism:** Use an entropy-coded route tag (short codes for likely routes) instead of a fixed tag when the tagless meet is too large.
- **Novelty vs nearest prior art:** Classical entropy coding; worth reporting only if it changes which cut is chosen under λ.
- **Cheapest first test:** {A, B} with route probabilities 0.9/0.1; expected vs worst-case bytes under the contract's worst-case payload rule.
- **Old-task retention check:** A under the rare route.

### 20. Stress the merge with the full stacked control (I)
- **Mechanism:** Require a tagless route merge with a lease to buy a point that a best causal C prefix, per-route exact transport with a paid tag, and an indefinite fold reset at H cannot buy together.
- **Novelty vs nearest prior art:** An audit. If the stack ties at equal C data, width-steps and evidence, both seeds are accounting around known parts.
- **Cheapest first test:** Paper check plus a C batch: find any (R, H, k) where the merge-and-lease beats the stack; report all ties.
- **Old-task retention check:** Worst A drift over all routes and all steps up to H plus one.

### 21. Hold the late reader to the declared horizon (I)
- **Mechanism:** For each certified lease, run a consumer that arrives exactly one update after H, and require it to be refused or served from the renewal state, never from the merged state.
- **Novelty vs nearest prior art:** A falsifier for any lease that quietly relies on decay to hide errors.
- **Cheapest first test:** Paper check t = 1 consumer against the 3-bit lease: an unrefused service shows error 3/4.
- **Old-task retention check:** A after the late consumer under each expiry action.

### 22. Use released width for a real later writer (I)
- **Mechanism:** Credit the merge only if the freed bytes or width are used by a later B writer that would otherwise be refused, at equal A retention.
- **Novelty vs nearest prior art:** Parent card #269#05 applied across routes and horizons.
- **Cheapest first test:** Allocator with 16-byte blocks; show the merge frees a whole block that a later writer takes.
- **Old-task retention check:** A after allocator reuse, under every route.

## Ranked deeper questions

1. **Can truthful C work line up complementary routes so one tagless fold beats a paid tag?** Use 01, 03, 04 and 20. The paper check shows the merge saves bytes only on aligned routes; the open question is whether real C batches can turn complementary routes into aligned ones at lower total cost than the stacked control.
2. **Is a pre-paid renewal ever cheaper than holding the full state through the horizon?** Use 02, 07, 09 and 21. Renewal must be bought before the merge; if renewal plus lease bytes over time never beats just keeping the full state, the lease is measurement, not a new operation.
3. **Can routes and horizons expire independently and release bytes early?** Use 06, 12, 13 and 14. Dropping rows from the observability relation is free in theory; test whether real route windows close early enough to free usable width before the first sensitive reader.
4. **Does lawful rounding give free expiry?** Use 08 and 10. If finite precision makes merged states collide again after a certified step, the lease ends with no renewal; test whether that step comes soon enough to matter and survives a clock change.

**Verdict:** Keep both score-3 seeds conditional. The paper check shows that a tagless route merge can beat a paid tag (3 vs 4 bits) only when the routes' partitions line up; on complementary routes it saves nothing. A horizon lease is exact until expiry but cannot be renewed after merging, so renewal must be bought up front. Together they earn their name only if real C work aligns routes and a pre-paid lease releases usable width ahead of the stacked control, with A, B and C retained.
