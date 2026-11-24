# Two-clock examples: can training keep a proof launchable?

**Status:** Ideas only; no experiments, implementation, or GPU work.

**Parent:** [Split-timed proof deadlines](split-timed-deadlines.md) ([PR #180](https://github.com/manojbajaj95/cl/pull/180)).

**Review seeds:** [Flood triage, row 285](https://github.com/manojbajaj95/cl/blob/23cfd2e9633460d9b6825fd7a01d539ccc383de3/reviews/flood-triage.md#L285) scores two ideas at 3: **#11**, spend one truthful example to delay optimizer-slot carry and keep a multi-step entry bridge launchable; **#12**, reorder legally swappable B updates to keep proof options open without changing the samples or their B target.

**Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/23cfd2e9633460d9b6825fd7a01d539ccc383de3/reviews/idea-ledger.md). Beat the stacked parts, not just each part alone. The ledger's bounded-delay scheduling kill makes gradient accumulation a required control. The [replay-deadline null (PR #113)](https://github.com/manojbajaj95/cl/pull/113) makes a smooth, no-cliff world mandatory; neither a planted threshold nor an order effect alone is evidence.

## Can an example or an update order preserve the right to import a proof?

Training-data choice and batch order are not new. The candidate new object is a **reusable receipt for an intervention that preserves a proof option**: an independently checkable statement that a truthful example or legal ordering keeps a particular bridge launchable while its hidden-slot lease remains valid for every step that needs it. Bind the receipt to the frozen suffix proof, edit, update-law version, observable precondition, legal continuation family, budget and old-task floors. The teacher is gone before import; the receipt cannot use the private slot values to choose an action. If the receipt neither buys a safe useful admission beyond the strongest fixed-budget stack nor saves marginal verification across independent imports, call it an improvement or drop it. The theorem itself never expires.

- **Two clocks, not two independent maxima.** The entry clock is the last safe *launch* boundary for a bridge to the frozen entry set. The lease ends before the first update that could carry an omitted slot residual into a proof-visible effect beyond tolerance. At launch, one transcript-based action must work for all compatible states and all permitted futures; prove entry, old-task safety and lease coverage through the bridge's last slot-sensitive step. Do not splice the entry window from one continuation to the lease from another. Record feasible launch boundaries before reducing them to a deadline: windows can close and reopen. Report dynamical closure, lack of information and checker refusal separately.
- **Two permitted intervention families.** For examples, truth means an independently fixed label or observation from the declared source; eligibility does not depend on its gradient being convenient. Use the declared loss and optimizer, not a relabel, custom slot write or teacher query at import time. For ordering, fix the queued batch multiset, target, optimizer law, learning-rate schedule and externally bound precedence constraints. Independence means the law permits a swap, not that the full-state maps commute. No foreknowledge of later arrivals, skipped updates or changes to the edit. Charge buffer residence and any delay to B.
- **Judge admissions, not just extra clock ticks.** Count safe useful imports, false admissions, missed admissions, B gain and cost (examples, updates, wall-clock/buffer delay, bytes, oracle calls and checker work). Match B accuracy **and** loss bands; compare every method on the same held-out streams, including refusals. In every card A/C means held-out old-task data, including a rare slice, checked at prefixes as well as after the common unchanged suffix. Tiny planted worlds check bookkeeping only; look for the effect on blind, independently generated families, including smooth, reopening and no-carry cases.

### Paper witness: one truthful example, two effects

This is a hand-worked construction, not evidence. Fix the target throughout a toy teaching pool to `y = -x₁/2 + max(x₂, 0)`. The learner predicts with two coordinates: a masked weight initially zero and a visible bridge reserve initially zero. At boundary 0 these give prediction zero. The masked momentum slot is private, either 4 or 6. On the one allowed teaching step, with half-squared loss and unit rates, the optimizer updates that slot to half its value minus the first gradient, but keeps the weight masked; it applies plain SGD to the reserve. For features `(2, -1)` the truthful label is `-1`, and the gradient at zero is `(2, -1)`. One real update therefore maps both possible slots to `{0, 1}` and raises the reserve to 1 in either history.

At boundary 1 a fixed tick would propagate the slot if it were at least 2, terminating the lease *before* the tick and closing the two-step bridge's route. The bridge can launch at 1 only with reserve 1 and the route open, and runs across the next two updates. Between the tick at 1 and entry at 3, no other operation touches the slot. The next tick, at 3, first adds a known +3 and then checks the same threshold, so the private lease must end by 3; the frozen entry contract permits slot disclosure at 3 and the suffix covers the tick there. A matched step on the truthful zero-feature/zero-label item yields slots `{2, 3}` and reserve 0. The truthful slot-only item `(2, 0; -1)` yields `{0, 1}` and reserve 0; the truthful entry-only item `(0, 1; 1)` yields `{2, 3}` and reserve 1. Thus the dual-effect item delays the first carrying tick past the slot-sensitive bridge and is the only one of these four choices that leaves the bridge launchable. The bridge and suffix are unchanged. The planted gate and chosen pool make this a sanity check, not proof that useful dual-effect items occur at competitive frequency.

### Paper witness: equal B work, unequal proof options

Queue four legally swappable B batches, each updating a distinct independent B head to its own fixed target and contributing, respectively, `+2, -2, +1, -1` to a private masked accumulator initially zero. In this toy future law, an update reaching accumulator 2 closes the bridge route and ends the lease just before that update; later cancellation cannot reopen it. In the listed order the accumulator is `2, 0, 1, 0`; in the order `-2, +2, -1, +1` it is `-2, 0, -1, 0`. Final B heads and final accumulator agree, but only the second order can launch a two-step bridge after the first two batches and finish alongside the last two. This shows why endpoint matching is not enough, not that a deployed learner has such a latch. If one accumulated update is legal and gives the same B gains, retention and admission without delaying the bridge decision, the schedule has no demonstrated advantage.

## Idea cards

`P` denotes a candidate primitive; `I` denotes an improvement or a test that could explain the effect away. All first tests are proposals for tiny CPU studies or hand enumeration, not work performed here.

### Find a single honest example that buys both clocks

#### 01. The one-example replacement (P)
- **Mechanism:** Choose one eligible example by the set of bridges that can actually finish without slot carry; do not optimize two marginal deadlines and add them up.
- **Novelty vs nearest prior art:** [Matching Training Trajectories (MTT)](https://arxiv.org/abs/2203.11932) selects data by trajectory agreement; [PR #172](https://github.com/manojbajaj95/cl/pull/172) can buy earlier split evidence. The proposed receipt certifies that one truthful update replaces two interventions without replacing the edit or the proof.
- **Cheapest first test:** Exhaust one tiny pool, logging single- and dual-effect items. Compare with same-pool MTT, buying earlier evidence and separately optimized bridge and lease actions stacked at equal example and oracle budgets; also show the two-example upper bound. Require an extra useful safe admission on blind pools at matched B gain.
- **Old-task retention check:** Measure A/C before teaching, after the original carry boundary and after the common suffix; match old-item margins when comparing candidate pools.

#### 02. Accept a push only if both hidden histories agree on it (P)
- **Mechanism:** Certify one label whose update makes the same bridge safe for distinguishability-equivalent histories, even when the slot updates themselves do not coalesce.
- **Novelty vs nearest prior art:** [Iterative machine teaching](https://arxiv.org/abs/1705.10470) picks examples for learner updates; [PR #179](https://github.com/manojbajaj95/cl/pull/179) uses examples instead of a probe. Here indistinguishability can persist *through entry*; the pushed states need a shared safe bridge, not a shared slot estimate.
- **Cheapest first test:** Enumerate two pairs of hidden slots: one requiring opposite single-state teachings and one with a shared truthful item. Compare belief-level search against point-estimate teaching, a charged slot probe and separate robust actions.
- **Old-task retention check:** Evaluate A/C in every hidden sibling after entry; refuse any item with only mean-case retention.

#### 03. Teach against the same future, not against separate worst cases (P)
- **Mechanism:** Attach branch-indexed lease and entry guarantees to one example, proving that each possible future has a policy that remains safe using only information revealed so far.
- **Novelty vs nearest prior art:** [Time-varying reach-avoid](https://arxiv.org/abs/1410.6445) can express this quantifier order. The candidate is a reusable example certificate that preserves useful branch correlations when separately exported entry and lease summaries discard them.
- **Cheapest first test:** Build a four-leaf tree with early and late carry on different public arrivals; compare marginal summaries, a branchwise stack and an exact contingent planner. Add indistinguishable arrivals where the same certificate must refuse.
- **Old-task retention check:** Report the minimum A/C across all four trajectories, including the waiting decision before arrivals are distinguishable.

#### 04. Price the truthful pool, not a freely synthesized gradient (I)
- **Mechanism:** Map how often measured dual-effect gains survive when generated points must belong to a fixed, realistically available source with independently checked labels.
- **Novelty vs nearest prior art:** [MTT](https://arxiv.org/abs/2203.11932) allows synthetic optimization. This audit asks whether a useful bridge-and-lease effect survives the feasible truthful support at equal acquisition cost.
- **Cheapest first test:** Compare exact search on raw samples to a relaxed feature-space oracle, using both abundant and scarce pools, then thin the pool at random. No claimed object if only off-support points win.
- **Old-task retention check:** Include old subgroups that overlap or conflict with the truthful pool; report the worst subgroup after the chosen item and suffix.

#### 05. Reuse a truthful item as a certificate across optimizer time (P)
- **Mechanism:** Export the interval of slot ages and learning rates for which the same item keeps the bridge and lease compatible; refuse outside the interval rather than interpolate across a split.
- **Novelty vs nearest prior art:** [Adam](https://arxiv.org/abs/1412.6980) exposes time-sensitive moments and bias corrections; [Pacti](https://arxiv.org/abs/2303.17751) can state the assumptions. The test is whether two-clock conditions let the example travel more cheaply across independent checkpoints than composing the contracts anew.
- **Cheapest first test:** Solve a scalar momentum variant over a few checkpoint ages, then blind-check the bound on a tiny Adam variant with explicit counters, resuming only within a proven scope. Compare a table of per-checkpoint solutions and a compiled generic contract.
- **Old-task retention check:** Check A/C at the original and imported ages, especially on the largest allowed effective learning rate.

### Change the order, not the work

#### 06. Four batches, one safe proof launch (P)
- **Mechanism:** Permute four queued B batches under the frozen law. Choose an order for which the lease lasts until the frozen entry bridge can finish, not the one that merely defers the first visible loss.
- **Novelty vs nearest prior art:** [Critical learning periods](https://arxiv.org/abs/1711.08856), [iterative machine teaching](https://arxiv.org/abs/1705.10470) and [curriculum learning](https://arxiv.org/abs/2010.13166) already exploit timing; the target here is preserving a different, previously exported proof under equal B work.
- **Cheapest first test:** Enumerate all 24 permutations in a tiny masked learner; filter to matched final B gain, then compare B-loss curriculum, critical-period and machine-teaching schedules, split avoidance alone, a full stack and gradient accumulation where legal. Charge equal search work when comparing selectors, and label exhaustive search as an oracle if a selector uses less.
- **Old-task retention check:** Measure worst-prefix A/C for every order and check again after a common, adversarially selected legal batch.

#### 07. Swap with a lease-aware commutation witness (P)
- **Mechanism:** Allow an adjacent swap only with a witness covering its intermediate state and the reachable bridge starts, including future carry from apparently commuting B changes.
- **Novelty vs nearest prior art:** [Learning order and Lie brackets](https://arxiv.org/abs/2611.20087) use noncommutation as a forgetting signal. Even endpoint-commuting B changes may violate proof availability at an intermediate boundary; the witness certifies the swap through that boundary.
- **Cheapest first test:** Put two swappable pairs into a six-step partial order. Compare endpoint/Lie-bracket ranking, exact prefix certificates and generic reach-avoid. Include a no-bridge version where the accumulation control should tie.
- **Old-task retention check:** Inspect A/C between the swapped updates and after a common carry-revealing suffix, not just after the pair.

#### 08. Keep choices for more than one as-yet-unrequested port (P)
- **Mechanism:** Choose the next B batch to preserve several frozen proof entry options until an independent request reveals which edit is actually needed; never allocate separate unrealizable schedules to simultaneous requests.
- **Novelty vs nearest prior art:** [Reach-avoid](https://arxiv.org/abs/1410.6445) represents multiple targets, and [PR #180 #15](split-timed-deadlines.md#15-protect-a-scarce-shared-repair-action-with-contingent-reservations-p) protects a scarce repair. Here the reserved resource is the legal ordering of already-owed B work before demand is revealed.
- **Cheapest first test:** Queue four batches and two mutually exclusive request types with a fixed reveal boundary. Compare largest deadline, largest per-port slack, exact contingent planning and a shared portfolio certificate; repeat with both requests allowed to expose double-counting.
- **Old-task retention check:** Require A/C floors before reveal and under each possible request; include the no-request B run.

#### 09. Schedule only batches that have actually arrived (P)
- **Mechanism:** Commit only the next B update from already visible batches; issue a proof-option policy with a fallback when the remaining offer set cannot support the bridge, rather than using a hindsight permutation.
- **Novelty vs nearest prior art:** [Critical learning periods](https://arxiv.org/abs/1711.08856) motivate timing, and [time-varying reach-avoid](https://arxiv.org/abs/1410.6445) supports receding-horizon policies. A portable guarantee must additionally bind the receipt to the arrival and buffer contract that keeps a specific old proof usable.
- **Cheapest first test:** Take the four-batch problem with two late arrivals and a two-batch buffer, enumerate arrival orders and compare no-lookahead curriculum, split avoidance, matching-buffer accumulation and a hindsight ceiling.
- **Old-task retention check:** Evaluate A/C during buffer-induced waits and on fallback/refusal trajectories as well as on successful entries.

#### 10. Look for an order win even when endpoint slots match (I)
- **Mechanism:** Compare orders that reach an observationally and slot-equivalent B endpoint but offer different legal launch windows earlier. Equalization is a diagnostic on matched states, never an extra allowed intervention.
- **Novelty vs nearest prior art:** [Lie-bracket order effects](https://arxiv.org/abs/2611.20087) already explain some retention differences; [PR #178](https://github.com/manojbajaj95/cl/pull/178) isolates hidden slot divergence. This tests whether the option matters before endpoints converge, not whether final weights encode order.
- **Cheapest first test:** Pair convergent prefixes and fix one independent port-request time between them and another after convergence. Compare the actual admission advantage to the smooth/no-carry control; expect no advantage after genuinely identical full states and histories relevant to the law.
- **Old-task retention check:** Check A/C at the request boundaries and after convergence; distinguish a real preserved option from different old-task losses.

### Ask what an example and an order can buy together

#### 11. Teach one prefix, unlock a legal swap (P)
- **Mechanism:** Pick an item and a swap jointly: the item makes an otherwise unsafe intermediate state safe, and the swap frees a later bridge launch that the item alone cannot reach.
- **Novelty vs nearest prior art:** [Iterative machine teaching](https://arxiv.org/abs/1705.10470) selects a sequence of teaching examples; [PR #172 #15](https://github.com/manojbajaj95/cl/pull/172) studies noncommuting splits. Here the item is optional teaching, the swapped work is mandatory B, and the claimed interaction is on one frozen proof's admission.
- **Cheapest first test:** Exhaust a four-item by 24-permutation grid. Compare neither, example only, order only, the separately optimized pair and the joint choice. Require a held-out admission from the joint chooser at equal search and B gain that the full stacked pair misses.
- **Old-task retention check:** Compare A/C in all arms after the optional item, at the swapped intermediate boundary and after the suffix.

#### 12. Make a truthful label useful only before the wrong batch (P)
- **Mechanism:** Bind the receipt to a precondition on the placement of an item, not to the raw sample: the same example can steer the lease clear at one boundary and lose the bridge at another because its current gradient changes.
- **Novelty vs nearest prior art:** [Critical learning periods](https://arxiv.org/abs/1711.08856) and [machine teaching](https://arxiv.org/abs/1705.10470) already make examples time-dependent. The claim is a reusable proof that particular insertion boundaries, including disconnected ones, preserve both obligations under a fixed B schedule contract.
- **Cheapest first test:** Try the same two labels at every admissible insertion boundary of a quadratic learner, enumerate the true safe set and compare a fixed early placement, an endpoint teacher, a verified interval and a reusable set certificate.
- **Old-task retention check:** Measure A/C at each candidate placement and after entry, including placements with a longer lease but worse old-task loss.

#### 13. Certify a swap class instead of one lucky permutation (P)
- **Mechanism:** Export a partial order of hard-before constraints. Any linear extension must preserve both clocks for the same frozen bridge; prove coverage over the class, not by recording only the successful witness.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) can encode ordering constraints. The hypothesis is that proof-specific swap invariants compress safe schedule classes and admit reordered jobs at lower marginal cost than generic contract composition or per-order certification.
- **Cheapest first test:** Enumerate six batches and find a safe class with at least two genuinely different B orders. Try to break its rule on all linear extensions; compare checker bytes, time and coverage to a whitelist and compiled contract.
- **Old-task retention check:** Score worst-prefix A/C over the entire class, including the extension that delays replay of the nearest old class longest.

#### 14. Give each option a paid escape hatch (P)
- **Mechanism:** Tie an example's two-clock guarantee to one reserved legal adjacent swap, executable only if a public warning arrives soon enough. Bind the reservation to real queued work and forbid double-booking that swap.
- **Novelty vs nearest prior art:** [Reach-avoid](https://arxiv.org/abs/1410.6445) supports contingent responses, and [PR #180 #15](split-timed-deadlines.md#15-protect-a-scarce-shared-repair-action-with-contingent-reservations-p) reserves repair actions. Here the reservation is removable scheduling slack on committed B batches, not an additional renewal or repair update.
- **Cheapest first test:** Run a two-branch stream with a warning before or after the last useful swap. Compare max-delay buffer, always-swap and optimal contingent control at equal delay and reservation costs.
- **Old-task retention check:** Check A/C on timely warning, late warning, no warning and fallback; never credit the warning detected only after A/C loss.

#### 15. Change only the lease-sensitive span of bridge execution (P)
- **Mechanism:** If a frozen bridge already offers multiple valid schedules for its substeps, move all slot-sensitive substeps to a proven safe prefix while B still meets its target. The remainder must use no hidden slot and reach the same entry condition.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) can compose dependencies, and [PR #180 #05](split-timed-deadlines.md#05-prove-the-bridge-can-finish-before-it-starts-p) checks completion. This asks whether a short certified span can cover many legal B/bridge interleavings without needing a new suffix proof for each.
- **Cheapest first test:** Hand-enumerate a three-substep bridge with one hidden dependency, matched B schedules and a generic scheduling baseline. Introduce a later β-dependent optimizer read as a negative case; the span must expand or the receipt refuse.
- **Old-task retention check:** Track A/C after each interleaved substep, especially when a valid entry schedule would temporarily lose an old ability.

### Put the alleged primitive in danger

#### 16. Try to replace the lease-aware teacher with old-gradient protection (I)
- **Mechanism:** Use ordinary protection of old-task gradients, plus the best entry-only scheduler, to see if it recovers the same proof options without forecasting hidden carry.
- **Novelty vs nearest prior art:** [GEM](https://arxiv.org/abs/1706.08840) and [Orthogonal Gradient Descent](https://arxiv.org/abs/1910.07104) protect old gradients or outputs. This is a direct alternative explanation for apparent two-clock examples, not a new gradient projector.
- **Cheapest first test:** Use a tiny conflicting-task stream with and without masked slots. If update projections are legal in the frozen law, stack a same-memory projector with the entry scheduler; otherwise use its score to choose among the same legal actions. Match A/C margin, B progress and oracle calls before comparing admissions.
- **Old-task retention check:** Apply the same disjoint old test battery to baseline and joint policy, including after reopening the masked coordinates.

#### 17. Remove the hard gate and see whether timing still pays (I)
- **Mechanism:** Replace a planted absorbing split with a smooth transfer and a reopening. Keep the action grammar, tolerances and resource envelope fixed; measure the safe launch set rather than infer a cliff from one threshold.
- **Novelty vs nearest prior art:** [Time-varying reach-avoid](https://arxiv.org/abs/1410.6445) already handles changing safe sets, and the [PR #113 replay-deadline null](https://github.com/manojbajaj95/cl/pull/113) found a smooth timing curve. The test asks whether evidence for the receipt survives both, not whether thresholds can be built.
- **Cheapest first test:** Sweep three fixed tolerances on hard, smooth, reopening and no-carry micro-worlds. Compare constant schedules, margin-matched heuristics, the exact oracle and the proposed receipt, reporting both restricted coverage and oracle misses.
- **Old-task retention check:** Record worst-prefix and final A/C for each tolerance; reject improvements bought by silently moving the retention floor.

#### 18. Test the next read, not the next logit (I)
- **Mechanism:** Hold the next weight update fixed while varying a previously omitted slot; check whether the receipt holds when the first permissible later training reader consumes the differing value.
- **Novelty vs nearest prior art:** [Adam](https://arxiv.org/abs/1412.6980) supplies deferred optimizer dependence, and [PR #178](https://github.com/manojbajaj95/cl/pull/178) already constructs hidden slot splits. The new test target is whether an *intervention's* two-clock claim survives the sanctioned later read, not whether such slots exist.
- **Cheapest first test:** Enumerate pairs of histories with matching next logits and differing second moments. Replay each same example and order under one fixed legal read; compare to full-state verification and a value-insensitive read control to count false lease extensions.
- **Old-task retention check:** Recheck A/C immediately after the read and after a held-out old-task probe batch; report pre-read equivalence separately.

#### 19. Try to collapse the schedule into one accumulated update (I)
- **Mechanism:** Replace reorderable B work by accumulation where the law supports it, including the true optimizer state evolution and any need to permit mid-window launches.
- **Novelty vs nearest prior art:** [Lie-bracket learning order](https://arxiv.org/abs/2611.20087) motivates removing reorder effects; the ledger already killed bounded-delay scheduling when accumulation tied. The case that remains is access to a frozen proof before the window closes, at the same B progress.
- **Cheapest first test:** Match a four-batch permutation against a gradient-accumulation arm with the same samples and maximum latency. Compare with a second arm that may process the same bridge request at the same boundary; if that arm is illegal, report why and show the unrestricted accumulation ceiling separately.
- **Old-task retention check:** Include A/C at request time and after the same common suffix; accumulation cannot hide intra-window loss by evaluating less often.

#### 20. Compile away the receipt across blind imports (I)
- **Mechanism:** Express the same example and ordering policies, hidden-state uncertainty and entry/lease guards as a generic partially observed reach-avoid contract. Share the suffix proof equally on both sides.
- **Novelty vs nearest prior art:** [Reach-avoid](https://arxiv.org/abs/1410.6445) and [Pacti](https://arxiv.org/abs/2303.17751) are the strongest compilation account. The candidate is only novel if a CL-specific receipt is cheaper to reuse or safer at the same budget; representation alone is not a contribution.
- **Cheapest first test:** Freeze one suffix proof and hold out independent import streams with different pools and order contracts. Plot achieved coverage against total first-plus-marginal checking work and receipt bytes, including verifier failures; a cost-preserving compilation wins the null.
- **Old-task retention check:** Verify A/C for both representations on every accepted import and on default execution for refused imports; count disagreement by cause.

## Ranked deeper questions

1. **Can one truthful example buy a safe useful admission that the strongest stacked parts cannot buy?** Start with 01, 02 and 04: use exactly the same examples and calls, compare equal B gain and reserve the two-item result as a ceiling. A win confined to planted dual-effect pools or explained by margin-matched retention protection (16) is not enough.
2. **Is reordering preserving a proof option or just avoiding damage?** Cross a late port request with the order permutations at matched B gain (06, 10), then try split avoidance and accumulation (19). Look for an advantage before convergence that disappears when no bridge can be requested. If the schedule only changes B loss or ordinary A/C loss, reject the proof-specific claim.
3. **Does the useful part travel without a hidden-state or hindsight oracle?** Try the partial-arrival and swap-class certificates (09, 13, 14) on blind imports and challenge them with the later optimizer read (18). Distinguish conservative refusal from a genuine loss of repairability.
4. **Does a specialized receipt earn its keep once the gate is less convenient?** Use the smooth/reopening suite (17) and the generic compilation (20). Require reusable evidence or more safe useful admissions at matched total cost on held-out cases, not more nominal clock ticks.

**Verdict:** Keep both seeds as testable candidates, not established primitives. First try to buy both clocks with one truthful update and then try to make the order effect disappear with accumulation. Promote only if the gain is proof-specific, survives the stacked baseline and preserves ordinary old tasks.
