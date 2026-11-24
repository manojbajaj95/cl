# Self-depleting teaching supply: charge what new-task SGD closes, and what truthful replay opens

**Status:** Ideas only; no implementation, pilot, or GPU work. **Parent:** [Depletable teaching supply](depletable-teaching-supply.md) ([PR #209](https://github.com/manojbajaj95/cl/pull/209)). **Review seeds:** [Flood triage, row 320](https://github.com/manojbajaj95/cl/blob/1b941b702ffc6873034c8efbdb03e30bd85de32d/reviews/flood-triage.md#L320), score-3 cards **#02** (ordinary new-task SGD depletes joint teaching capacity) and **#18** (a truthful old-task replay example opens a gate, with separate readiness and retention certificates). **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/1b941b702ffc6873034c8efbdb03e30bd85de32d/reviews/idea-ledger.md).

## What would count as new?

The bet is a **certificate about what teaching remains possible after ordinary learning**, not a plasticity diagnostic, replay selector, or general claim about SGD. The same prospective proof should (1) turn a verified loss of reachable joint discharges into a teaching-step lower bound and (2) identify when a real old-task presentation buys both readiness and retention without billing it twice. Either part can fail independently. An ordinary SGD transition that reopens capacity refutes the no-refill claim for that envelope; it is not measurement noise.

**Nearest prior art and controls.** The parent concedes operator-counting and potential heuristics, resource-constrained planning, and Lyapunov certificates. [Dohare et al.](https://arxiv.org/abs/2306.13812), [ReDo](https://arxiv.org/abs/2302.12902), and [UPGD](https://arxiv.org/abs/2404.00781) address loss of plasticity or the plasticity–retention trade-off. [Learning Dynamics of Continual Learning](https://arxiv.org/abs/2609.33620) connects update–behavior interactions, forgetting and plasticity loss; that is a close diagnostic control, not evidence of a bound on future joint presentations. [GEM](https://arxiv.org/abs/1706.08840) protects old losses and [MIR](https://arxiv.org/abs/1908.04742) retrieves threatened old examples; [Dark Experience Replay](https://arxiv.org/abs/2004.07211) is a strong equal-budget replay control. None of these comparisons establishes priority. The [ledger](https://github.com/manojbajaj95/cl/blob/1b941b702ffc6873034c8efbdb03e30bd85de32d/reviews/idea-ledger.md) rules out pitching Gramian reserve or effective rank as a chooser, self-authorship as replay value, and order effects that gradient accumulation explains. Use margin-matched old tasks and an explicit smooth no-cliff control when a hard threshold drives the result.

## Contract and two paper fixtures

Freeze the parent's truthful pool, presentation atom, free transcript, admissible history/order envelope, optimizer state and schedule, repeat and reply rules, and the old-task A/C floors and new-task B utility target. Let `z_A,z_C` count distinct discharged teaching obligations, not accuracy or retention margin. Define retained old behavior on independent normal old-task reads, including rare slices. Check those floors at every live prefix; a path that already forgot A does not demonstrate loss of joint plasticity.

**Supply rule.** At a snapshot, let `S(h) ≥ 0` be a certified upper bound on future shared discharges in the no-refill envelope. A sufficient local proof for unit joint bonuses is `Δ(z_A+z_C+S) ≤ cost`: a single costs one, a joint costs one and consumes at least one unit of `S`, and an ordinary free B step has no new teaching discharge and satisfies `S(h′) ≤ S(h)`. An opener can raise readiness without minting supply if `S` already covers its future joint use. If replenishment is allowed, state its charge and check the full inequality on that edge; the no-refill cap itself no longer bounds gross future uses. Otherwise void the supply term and use a separately valid fallback. For demand `(d_A,d_C)`, telescoping gives `max(d_A,d_C,d_A+d_C−S(h))` from a zero-progress snapshot in the unit-per-skill game. The premises must cover **all** reachable lawful presentations, not just the observed B run. An upper envelope shrinking does not by itself prove the true optimum increased; a matched reachability oracle can test that.

**F1 — a drain induced by plain SGD, with a reopening negative.** Use a scalar `x∈[0,1]`. Each ordinary B item has label 1 and loss `(x−1)²/2`; SGD with rate 1/2 gives `T(x)=(x+1)/2`. In this hybrid toy, a fixed truthful joint presentation uses the same shared-coordinate update and discharges one outstanding A and one C obligation only if its actual movement `(1−x)/2` is at least `1/8`. Singles discharge one obligation and leave `x` unchanged. A/C normal reads are independent of `x` and held fixed here; the joint-discharge predicate and distinct obligation counters are explicit toy assumptions, not a model of measured forgetting. Then `S(x)` is the number of consecutive applications of `T` whose pre-step movement is at least `1/8`. Successive movements halve, so both B and any qualifying joint step remove one from positive supply; a single cannot restore it. For demand (2,2):

| B prefix from x=0 | x | S | Exact remaining paid presentations | Fixed initial-supply bound |
|---|---:|---:|---:|---:|
| 0 | 0 | 3 | 2 | 2 |
| 1 | 1/2 | 2 | 2 | 2 |
| 2 | 3/4 | 1 | 3 | 2 |
| 3 | 7/8 | 0 | 4 | 2 |

The bound is attained by spending up to two available joint presentations, then using singles. If the B stream instead admits a truthful label-0 item (a different input sharing `x`), the same SGD rule sends `7/8 → 7/16` and restores two qualifying joint updates. If that B item is free and lawful, the two joint presentations following it beat the four-step bound. The matched smooth control should replace the hard pass/fail with graded shared gain and fix a terminal target independent of the certificate; otherwise the toy manufactures the cliff it explains.

**F2 — a replay atom with two verifiable effects but one bill.** One stored, truthful A record has a vector-valued target `(1,1)`; the ordinary A model outputs `(r,g)` on it. Its loss is `((r−1)²+(g−1)²)/2`, so a unit-rate replay update from `(0,0)` gives `(1,1)`. Keep the labels and atom fixed. A held-out normal A input with true class + has signed margin `1+2r`; require margin ≥1 throughout and ≥3 at the terminal state. The old prediction is correct before replay; the replay restores headroom rather than rescuing a failed floor. A separate normal C read is fixed and passes its floor. The gate is `g=1`: it licenses a joint transition that discharges one obligation each and resets `g` to zero without changing `r`. Singles leave both coordinates fixed. These continuation rules are toy assumptions; the opener itself is an SGD update on a real old-task loss within the fixture.

At the same checkpoint, masking only the `g` update retains the A margin gain but does not license the joint step; masking only the `r` update licenses it but leaves the held-out A margin unchanged, including after the joint step. These are diagnostic interventions, not extra lawful presentations. Give readiness and retention weights of 1/2 each in `Φ=¾(z_A+z_C)+½g+½r`. Replay earns at most 1; joint earns `3/2−1/2=1`; singles earn 3/4. The terminal obligation `(1,1), r=1` requires at least two presentations; replay then joint attains two. Adding a gate-only two-step bound and a retention-only one-step bound would wrongly give three. If both effects disappear when the same update coordinate is masked, report coupled effects rather than independently controllable credit; even distinct effects still need a **single** verified cost inequality (or separately sound bounds combined by max). Do not add held-out retention improvement into `z_A` when it already appears in the retention term, or bill a replay presentation both as a free background step and as paid preparation.

**Blind gate for the cards.** Fit no thresholds or credit weights to held-out streams. Compare with exact augmented-state reachability on tiny pools, fixed supply, operator counting plus per-law refits, and recomputing the bound after every B prefix. For replay, stack ordinary replay selection with a same-cost non-replay opener and the parent's readiness potential under the same total presentation, old-replay and B-utility budgets; include uncredited replay and a coupled-credit negative. Match starting A/C margins, count proof/check/fallback cost, and show normal A/C performance after B, the opener, the joint step and the tail. A safe inequality too loose to improve on the stacked control is not a new primitive.

## Idea cards

**P** = candidate primitive (new certificate or operation, conditional on the controls); **I** = improvement or falsifier, not a pilot candidate.

### Certify the drain

#### 01. Count joint presentations that unmodified SGD makes unreachable (P)
- **Mechanism:** Attach a countdown to a monotone shared-feature slack and prove that ordinary B contracts it and every qualifying joint discharge spends it. Do not constrain B to make the theorem true.
- **Novelty vs nearest prior art:** Dohare et al. measure ability to learn; #209 counts consumable joint steps. The new object would certify what B has removed from the teacher's feasible continuations.
- **Cheapest first test:** Enumerate F1 and the truthful label-0 branch; beat fixed supply without false bounds and fail closed on the reopened branch. Then replace the scalar by a shared ReLU feature and hold out one B example.
- **Old-task retention check:** Match A/C margin profiles at each snapshot; check the shared unit has not already impaired a rare old read.

#### 02. Prove minibatch closure without proving every order (P)
- **Mechanism:** At a common checkpoint, bound all admitted minibatch gradients by an inward cone on the faces of nested supply regions; verify the finite-step landing, not just gradient signs.
- **Novelty vs nearest prior art:** IQCs and barrier certificates give closure; the proposed reusable witness projects only onto what determines future teaching, not convergence or whole-model stability.
- **Cheapest first test:** Two truthful B gradients with opposite tangential components; exhaust their batch mixtures and orders. Include one batch whose curvature crosses a face despite an inward initial derivative. Compare with exact search and accumulation.
- **Old-task retention check:** Evaluate A/C at every landing and compare with accumulation at equal B gain.

#### 03. Certify lost routes, not lost units (P)
- **Mechanism:** Track an upper graph of routes from truthful examples to overlapping old obligations. Prove B deletes edges at certified margins and cannot add edges; charge shared discharge against the remaining route budget.
- **Novelty vs nearest prior art:** ReDo counts dormant units and operator counting counts named actions. A route witness should distinguish two learners with identical dormant-unit counts but different shared read reachability.
- **Cheapest first test:** A two-feature graph where one dead unit has a substitute but the other is the only bridge. Compare effective rank, a per-feature counter and the exact route oracle.
- **Old-task retention check:** Evaluate A/C separately on substitute and bridge slices; reject a graph shrink explained by a missed ordinary read.

#### 04. Prove an exchange bound when SGD changes the usable examples (P)
- **Mechanism:** Allow B to reopen individual edges if every newly enabled joint use can be injected into a distinct retired use, preserving a non-increasing total cap.
- **Novelty vs nearest prior art:** Petri-net place invariants count tokens; the object here would be a substitution map over lawful data-dependent teaching continuations, not a frozen operator count.
- **Cheapest first test:** Make B swap one viable A/C joint item for another without changing capacity; plant a one-to-two replacement that defeats an injective witness. Compare with recomputation and route deletion.
- **Old-task retention check:** Check A/C on every substituted path, not merely at the swapped checkpoint.

#### 05. Make a natural reopening the oracle's first adversarial query (I)
- **Mechanism:** Search the frozen B pool and admissible batchings for a reopening witness before looking for smooth monotonicity fits; an uncovered witness invalidates the cap.
- **Novelty vs nearest prior art:** Standard counterexample-guided verification and #209's void rule; the audit tests whether natural B variation alone defeats the central premise.
- **Cheapest first test:** Enumerate a one- and two-example negative stream with contradictory shared-coordinate pulls; compare random prefix sampling at equal evaluations.
- **Old-task retention check:** Count reopenings only on paths satisfying A/C and B utility, and report floor violations separately.

#### 06. Obtain a drain bound from dose, not from the step counter (P)
- **Mechanism:** Bound depletion by accumulated movement along a certificate coordinate, with each legal B update contributing a verified nonnegative dose. A zero-gradient B step pays nothing.
- **Novelty vs nearest prior art:** LR-area and Lyapunov decay explain change with training time; the proposed output is a schedule-portable upper bound on remaining joint discharges.
- **Cheapest first test:** Vary B batch order and LR at matched B gain; test two schedules with equal LR area but different signed movement and one schedule that reverses sign. Compare per-law refits.
- **Old-task retention check:** Match A/C margins before each schedule and audit the terminal and maximum-dose prefixes.

#### 07. Prove joint-capacity contraction in a learner quotient (P)
- **Mechanism:** Quotient checkpoints by the joint teaching continuations they admit, then look for a simulation from each post-B class into its predecessor. Count capacity in the quotient rather than in parameter distance.
- **Novelty vs nearest prior art:** Simulation and abstract interpretation are established; the candidate is a teaching-specific quotient that can survive reparameterizations that invalidate a raw slack counter.
- **Cheapest first test:** Rescale two positively homogeneous units without changing the model, then compare B updates that do and do not preserve the quotient at the declared LR. Test against cached exact search.
- **Old-task retention check:** Require equivalent A/C floor checks on both representations and after their paired continuations.

#### 08. Distinguish closure of joint routes from the growth of debt (P)
- **Mechanism:** Maintain separate witnesses for unchanged teaching demand and loss of the ability to discharge it jointly. Discard comparisons whose debt or free transcript changed.
- **Novelty vs nearest prior art:** Learning-readiness and forgetting scores can mix these causes; the candidate witness identifies two matched checkpoints with identical required behavior and different future feasible sharing.
- **Cheapest first test:** Cross two factors in a two-head network: B damage to old logits and B contraction of shared teaching gradients. Demand that only the latter changes the certified joint term when old obligations are held fixed.
- **Old-task retention check:** Check fixed held-out A/C reads and separate high- and low-margin slices; a forgotten checkpoint is a negative control.

#### 09. Compile a smooth slack certificate into discrete teaching charges (P)
- **Mechanism:** Prove a real-valued progress budget upper-bounds the sum of joint bonuses, then round only at the final integer presentation bound rather than thresholding individual units.
- **Novelty vs nearest prior art:** Potential heuristics already relax integer planning. The new target is a CL capability bound that persists when no literal gate or dead unit exists.
- **Cheapest first test:** Replace F1's hard threshold by geometric gains toward fixed held-out targets; compare exact search, hard bins and a continuous certificate. Include a weak tail that crosses a target only after many updates.
- **Old-task retention check:** Audit continuous A/C error throughout the weak tail, not only correctness at the terminal threshold.

#### 10. Make a genuine B acquisition fund a paid exception (P)
- **Mechanism:** Keep a no-refill phase certificate and a distinct certified edge for the first B milestone that restores joint capacity. Charge its full bill or forbid reusing the previous cap.
- **Novelty vs nearest prior art:** Continual backprop, ReDo and #209's replenishment are controls. The candidate is an attributable renewal from useful B learning, not a scheduled reset or free license to restore supply.
- **Cheapest first test:** Compare equal B gain from two truthful B streams, only one of which rebuilds a joint route; use ReDo, exact recomputation and a free bundled refill as controls.
- **Old-task retention check:** Check A/C on the replenishing prefix itself and after spending the newly restored opportunity.

### Certify the replay opener

#### 11. Let a truthful old A item carry two separately certified effects (P)
- **Mechanism:** Certify the opener against a later gate-enabled continuation and certify its held-out A retention improvement against a matched skip or sham; charge the true replay atom once.
- **Novelty vs nearest prior art:** MIR and GEM address old-task loss; #209's readiness potential charges generic openers. The candidate is separate readiness and retention evidence with a common cost certificate.
- **Cheapest first test:** F2 plus both update masks, ordinary replay, a same-cost non-replay opener and a coupled-coordinate negative. Compare equal replay and total presentation budgets.
- **Old-task retention check:** Require held-out ordinary A improvement and no C-floor failure after the opener, joint step and tail; replay-item fit does not count.

#### 12. Separate a real retention mediator from an incidental readiness proxy (P)
- **Mechanism:** Swap only the post-replay candidate mediator at matched checkpoints; demand that changing readiness changes legal continuation while preserving the certified old read, and vice versa for the retention mediator.
- **Novelty vs nearest prior art:** Activation patching and causal mediation already probe pathways; the candidate is an importable witness for credit attribution, followed by a reachable transition check.
- **Cheapest first test:** Rotate F2 into mixed coordinates so gradient orthogonality is no longer an easy criterion; compare functional swaps to raw parameter masks. Disallow off-manifold swaps as evidence of lawful execution.
- **Old-task retention check:** Verify independent A/C readouts after the true replay and paired continuations; use the swaps only as attribution diagnostics.

#### 13. Optimize the split without inventing a second budget (I)
- **Mechanism:** Constrain the credit split by a single per-edge inequality over replay, joint spend, regression and terminal retention. If no split improves the bound, keep max of independently sound bounds.
- **Novelty vs nearest prior art:** Cost partitioning already enforces one budget; this is a sharp anti-double-counting audit for the shared replay atom.
- **Cheapest first test:** Solve a two-feature LP for F2 and a version where replay earns both effects but the joint step does not consume readiness. Compare exact optimum and naive sum; reject any invalid LP candidate.
- **Old-task retention check:** Check A/C on regressions too, so a later reversal cannot leave stale retention credit.

#### 14. Use expiring readiness, not expiring replay truth (P)
- **Mechanism:** Certify an interval over which replay's gate effect remains spendable under intervening B, while recording longer-lived A retention separately with signed regressions.
- **Novelty vs nearest prior art:** #209 has decaying readiness and replay methods have recency weights. The candidate is a certified replay-specific expiry independent of the retention lease.
- **Cheapest first test:** Give replay's two effects different decay rates; hold out one B interleaving and compare a single decay clock, exact search and a smooth no-cliff variant.
- **Old-task retention check:** Verify A/C just before and after expiry, including a tail where the opener's retention benefit also fades.

#### 15. Replay for A, open a gate for C (P)
- **Mechanism:** Use a truthful A item whose shared update opens a later C-serving route without counting any immediate C discharge. Retention and readiness refer to different tasks and different causal comparisons.
- **Novelty vs nearest prior art:** Gradient transfer and replay selection already favor compatible examples; the proposed certificate promises reachability of a future joint transition under protected old reads, not one-step transfer.
- **Cheapest first test:** Two A records have equal held-out A lift, but only one enables a fixed lawful joint example; compare MIR + the parent's potential and a non-replay opener of the same cost.
- **Old-task retention check:** Compare held-out A and C at every prefix, especially C before the promised joint transition.

#### 16. Certify a sequence of truthful replay atoms with no individually credited opener (P)
- **Mechanism:** A first old item leaves a latent preparation state, a second completes the gate, and each retains its own measured old-task effect. Budget the sequence by prefix inequalities, not by labeling both items as full openers.
- **Novelty vs nearest prior art:** Planning landmarks and multi-step replay composition cover sequences; the candidate is a minimal gate witness with independently checked retention along each prefix.
- **Cheapest first test:** Two complementary old items versus two repeats of either item at equal replay budget; compare augmented-state planning and loss-ranked replay. Include reversed order or lawful accumulation where applicable.
- **Old-task retention check:** Audit A/C after each atom; reject a pair that restores A only after temporarily violating its floor.

#### 17. Bind a replay credit to a public proof of old provenance (P)
- **Mechanism:** Reuse a gate certificate for an equivalence class of authentic old items only when each replacement passes a predeclared update/continuation witness and an independent retention check. Keep labels, atom and provenance fixed.
- **Novelty vs nearest prior art:** Coresets and distillation replace replay data; the candidate is a substitution contract for which truthful replacements qualify as gate openers, not a compression score.
- **Cheapest first test:** Hold out a truthful old item with similar replay gradient but wrong gate-side curvature; compare gradient matching and individual re-verification at equal proof and buffer bytes.
- **Old-task retention check:** Test normal A/C and the rare old slice the replacement omits, after replay and after the gate spend.

#### 18. Issue a refusal when both credits are the same effect (I)
- **Mechanism:** Look for an old item where the same gain raises the retention reading and defines readiness; report both measured outcomes but no independently controllable credit if the shared change cannot be separated.
- **Novelty vs nearest prior art:** #209's exclusion witness plus standard mediation controls; the audit prevents treating two names for one measured margin as two discoveries.
- **Cheapest first test:** Collapse F2's two coordinates to one, preserving visible endpoint gains. Compare independent-effect diagnostics and test the naive summed bound against exact search.
- **Old-task retention check:** Use a second ordinary held-out A slice so defining the gate with one retention read cannot substitute for testing retained behavior.

### Make the certificates interact

#### 19. Choose the useful replay before the last joint route closes (P)
- **Mechanism:** Combine a verified drain deadline with a replay opener's readiness interval; present the old item when there is still a lawful spend, not merely when old loss is largest.
- **Novelty vs nearest prior art:** Deadline scheduling and #209's combined potential are controls. The candidate is actionable timing derived from B's certified erosion and a truthful opener, not a fitted recency rule.
- **Cheapest first test:** Shift the B trajectory while holding replay loss fixed, with legal early and late slots; compare MIR + generic scheduling, exact search and a smooth no-cliff version.
- **Old-task retention check:** Check A/C in every slot and after the spend; reject an early strategy that simply protects an already stronger A checkpoint.

#### 20. Distinguish opening existing supply from creating new supply (P)
- **Mechanism:** Partition proof obligations into a gate predicate and a capacity cap that already includes the gated continuation. A replay transition that permits more total joint uses than the cap allowed must be explicitly classified and charged as replenishment.
- **Novelty vs nearest prior art:** Resource planning distinguishes enablement from production; the CL witness would diagnose which occurred for the same replay record across learner histories.
- **Cheapest first test:** Same replay item on two checkpoints: it unlocks one reserved joint use on one and resets a saturated feature on the other. Compare fixed mode labels and full recomputation; plant a bundled free reset that invalidates the cap.
- **Old-task retention check:** Compare A/C immediately after both versions of replay and through all added joint uses.

#### 21. Transfer one proof to a stream that changes the replay gate but not the drain (P)
- **Mechanism:** Factor the certificate so a new lawful update law can replace the gate-check module without changing the drain witness or credit weights; re-check their joint edges and refuse imports that would let the new opener refill supply for free.
- **Novelty vs nearest prior art:** Generalized potential heuristics and #209 port a whole potential. The candidate is selective proof reuse with replay-quality and retention semantics preserved across laws.
- **Cheapest first test:** Hold out a lagged gate law and a momentum-driven reopening law; compare monolithic re-verification, per-law refits and cached search, charging every failed import.
- **Old-task retention check:** Verify A/C at the replay, pending, joint and tail states under the new law, not just against the source-law floors.

#### 22. Force the two certificates to improve on their stacked controls (I)
- **Mechanism:** Compare supply-only, readiness-only, stacked separate certificates, and a joint certificate on the same exact game. Count proof construction, rechecks, failed envelopes and fallback as work.
- **Novelty vs nearest prior art:** This is the ledger's merge gate; it tests whether the interaction does more than add a plasticity score to a replay schedule.
- **Cheapest first test:** Blind factorial crossing SGD drain vs reopening, truthful dual-effect replay vs generic opener, and disjoint vs shared credit. Require no false lower bounds and at least one tighter correctly predicted optimum or cheaper verification than the best stack.
- **Old-task retention check:** Use the same A/C floors, rare slices and matched B target in every cell, including refuted certificates and fallback paths.

## Ranked deeper questions

1. **What family of unconstrained B updates genuinely cannot replenish joint teaching capacity?** Start with #01/#02/#09: prove the cap on held-out truthful minibatches and finite steps, then actively look for a reopening (including one with identical B loss). If no useful family survives, the monotonic term is only a local toy or must be replaced with a priced-refill bound.
2. **Can one truthful replay atom buy independently attributable readiness and retained behavior at equal budget?** Use #11/#12/#18: find a lawful example with separate counterfactual witnesses, and require a common edge inequality on the reachable game. If the best ordinary replay plus an opener matches it, or only old-item fit improves, there is no new credit primitive.
3. **Can a certificate distinguish permission from production without re-solving the teaching game?** With #04/#20/#21, hold out histories where replay merely reveals latent capacity and histories where it restores it. A proof that cannot reject the free refill is unsound; one that always rejects has no reuse value.
4. **Does the interaction help after removing hard thresholds and paying verification costs?** Compare #19/#22 with fixed supply, exact recomputation and the strongest equal-budget replay plus planning stack at matched A/C and B behavior. Demand a bound or verification gain that persists without the fixture's manufactured cliff.

**Verdict:** Both review seeds stay conditional. The paper fixtures delimit the claim: ordinary SGD can drain a specified joint budget, but a lawful reopening voids a no-refill certificate; truthful replay can have two demonstrable effects, but the presentation has one bill. The next decision is whether either witness survives a shared-feature learner with ordinary B updates and independent old-task reads.
