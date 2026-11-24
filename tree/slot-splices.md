# Slot splices: can a learner borrow a future response without borrowing the optimizer?

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Optimizer-slot splits](optimizer-slot-splits.md) ([PR #178](https://github.com/manojbajaj95/cl/pull/178)). **Review seed:** [Flood triage, row 283](https://github.com/manojbajaj95/cl/blob/46a521230d3e49a72784ebec7445c97a69551633/reviews/flood-triage.md#L283) gives #178 cards 02 and 03 score 3: a minimum two-sided slot splice and a slot-only witness from phased gradient cancellation. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md). Match initial per-item margins and useful new learning; beat the best component controls run together; don't count a planted effect or save/restore as evidence of a new primitive.

## What would make a splice more than a partial optimizer reset?

Optimizer state already transports hidden history. [Momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) swaps slots at common weights; [delayed-release edits (PR #141)](https://github.com/manojbajaj95/cl/pull/141) writes slots for a later effect. [Stored in Optimizer State][stored] demonstrates causal slot mediation; [Matched Specialization][matched] exchanges second moments; [Delayed Optimizer-State Transport][transport] already uses the value of slot changes under committed short future paths. [Optimizer resetting][reset] and weight-space [TIES-Merging][ties] are simpler intervention and merging controls, not claims that the optimizer slots themselves can be merged safely. Weight equality, a gate flip after a swap, and a smaller tensor copy are not novelty by themselves.

The candidate object is a **reusable two-sided splice contract**: a declared optimizer schema, touched support and copy/rewrite rule, a receiver-side applicability check, an edit/suffix scope and deadline, and evidence that the same rule rescues the substitute and damages the source when the donor/recipient roles are reversed in shadow. An optional realization is a bounded sequence of *truthful* minibatches whose endpoint weights match the no-witness branch but whose altered slots unlock the same useful work. The test is whether a checked contract reduces total checking and intervention work, or admits more blind useful edits at the same retention and budget, without retaining the donor checkpoint. A direct transplant that cannot be realized through the allowed interface is a diagnostic, not a sample-only repair.

### What is held fixed?

- Match `θ`, Adam clock `k`, optimizer schema/hyperparameters, and the remaining continuation state at the two-sided test boundary (including schedule, stochastic state and normalization). A transplanted block is read from the original fork in each direction; score the reverse only in shadow. Freeze the edit, allowable suffixes, old-task floors, and B utility target before choosing the block. Check realized immediate **update vectors** on a common probe separately, not just matching logits or update norms.
- Predeclare the block partition, legal writes and costs (including queries, bytes read/written or stored, calibration examples, and feared side effects checked on both forks). On tiny worlds exhaust legal subsets, including the empty and full supports. Report ties and incomparable supports; “minimum” means globally cheapest under the declared tariff and scope, not greedy-small or unique. Separate donor-sourced values from reset or edited values, and exact toy guarantees from validation in naturally trained networks.
- For a sample witness, freeze the legal examples and LR schedule before search. Define silence against the same committed weight reference and end time; if clocks differ from a no-witness fork, also run a clock- and work-matched reference and isolate the slots with endpoint swap/reset. Discard near cancellations whose residual weight drift could explain the success; restore reference slots on witness weights and restore reference weights with witness slots in shadow, then use a weight-only rollout or bound over the declared suffixes to test mediation.
- Every first test is a proposed paper or CPU test, not a result. Use disjoint old suites A (with a rare stress slice) and C (unaffected control), current task B, and a frozen useful edit. Match B progress and initial margins; record A/C before the intervention, at every committed step and after the edit plus unassisted B. Gate signs and equality checks diagnose mechanism, not retention. Reserve editors, suffixes and old evaluation examples independently. Charge search, failed attempts, certification and fallback; compare against matched-budget direct rollout/repair, reset/projection or replay, and cached checks where relevant.

### A paper positive control for the second seed

Take scalar [Adam][adam], `β₁ = 1/2`, zero initial moments and clock, and any `0 < β₂ < 1`. Two truthful hinge-loss examples with distinct contexts and opposite labels, tied to this coordinate, supply gradients `+1` and `−1` while both stay in their active region. With schedule `η, 3η` and sufficiently small `η`, the orders `(+1, −1)` and `(−1, +1)` have bias-corrected first moments `(+1, −1/3)` and `(−1, +1/3)` respectively. Both have corrected second moment 1 at each step. Both return exactly to the starting weight in real arithmetic, with the same clock, but raw first moments `−1/4` and `+1/4`. At the next common `+1` pulse the corrected first moments are `3/7` and `5/7`; a fixed downstream gate between the two resulting weights separates their futures. In this single-slot contrast swapping `m` interchanges the two responses. The opposite order is a clock- and sample-matched control, not a no-treatment checkpoint. This construction says nothing about natural incidence, old-task service during the intermediate excursion, or portability to a second pulse. Those are the tests below.

## Idea cards

**P** = candidate primitive if the named operation works on blind edits beyond the stacked controls; **I** = diagnostic or improvement of a known operation. Labels are proposal judgments, not review scores.

### A. Make the two review seeds fail first

#### 01. Minimum two-sided slot splice (P)
- **Mechanism:** Find the cheapest legal donor block transfer that rescues the substitute, while the reverse transfer makes the source unsafe in shadow; hold all other slots fixed. Package the block and its applicability check for another editor.
- **Novelty / control:** [Slot mediation][stored] and [second-moment swaps][matched] establish the carrier. The extra claim is a minimal, portable causal block rather than a full-state intervention. Compare full swaps, uniform Adam reset, norm-matched dampening, and exhaustive block subsets as the oracle.
- **First test:** Enumerate four blocks in a tiny Adam MLP with a larger-moment decoy. Freeze the selected support and check, then give them to a blind second editor without the donor checkpoint. Report the planted oracle and naturally trained pairs separately.
- **Old-task retention:** The committed forward splice must recover rare A and preserve normal A/C through the edit and subsequent B steps at matched B gain. Record the reverse failure only in shadow.

#### 02. Two truthful phases, one silent endpoint (P)
- **Mechanism:** Commit two truthful minibatches that cancel realized weight motion, not just raw gradients, but leave a beneficial moment change; disallow any intermediate A/C breach.
- **Novelty / control:** [Gradient matching][gm], [MTT][mtt] and [#141](https://github.com/manojbajaj95/cl/pull/141) already shape later trajectories. The distinct actuation is useful slot motion under an endpoint equality and path safety constraint; give MTT the same examples, two steps and constraints. Compare reversed order, direct slot write and projected replay.
- **First test:** Start from the paper pair, then enumerate a small pool of real labeled examples and predeclared schedules on one trained CPU checkpoint. Use one held-out pulse; include sham-clock and crossed endpoint-weight/slot arms. Discard approximate pairs if residual weight drift can explain the effect.
- **Old-task retention:** Test independent A/C after each batch, after the useful edit and after B continuation, with identical minimum B gain.

### B. A causal block that can travel

#### 03. A menu of incomparable supports (P)
- **Mechanism:** Export only non-dominated sound splice alternatives under bytes, write permissions and deadline, so receivers unable to touch different blocks can still apply the same contract.
- **Novelty / control:** [Reachability][reach] can enumerate feasible actions; the claim is a compact reusable menu, not a Pareto plot. Compare cached exhaustive menus and on-demand minimum repair with the same validation budget.
- **First test:** Design a four-block truth table with two genuinely different sufficient repairs; learn the menu on one editor, then blind-test editors whose write permissions differ.
- **Old-task retention:** Check A/C for every committed menu choice, including rare A for the cheapest branch, and count only edits that also reach the B target.

#### 04. A direction-specific applicability check (P)
- **Mechanism:** Carry a compact predicate on the recipient's untouched slots, not just the transferred values. The predicate may allow rescue in one recipient but forbid it in a second with the same weights and immediate response.
- **Novelty / control:** [Delayed transport][transport] sees short committed paths; [reachability][reach] sees all state variables. Can one small, reusable precondition outperform an equally priced rollout budget on blind paths?
- **First test:** Hide a near-threshold neighbor slot across three naturally trained prefixes; fit the check on two and compare it to a truncated full-state check on the third. Wrong positive admissions fail even if cheap.
- **Old-task retention:** Use independent A/C at the edit and late B checkpoint, including a C slice that depends on the untouched neighbor.

#### 05. A matched-delta splice that survives a new suffix (P)
- **Mechanism:** Search for two opposite-direction exchanges within the level set of one matched next-update vector, then require the same support to change the outcome only on later pulses.
- **Novelty / control:** [#178](optimizer-slot-splits.md) constructs matched responses, and [transport][transport] values later state effects. The added claim is portable sparse intervention after enforcing functional equivalence on the immediate probe. Compare searched full-state perturbations and norm-matched partial writes.
- **First test:** Enumerate quantized `(m,v)` pairs in one Adam coordinate under a fixed update-vector equality, then test the declared block under two unseen, unequal-magnitude gradients.
- **Old-task retention:** Require rare A rescue and no C loss after the longer suffix and edit, not merely at the common first update.

#### 06. A causal support that survives reindexing (P)
- **Mechanism:** Address a splice by the role of its activation channel, not by a flat slot index; transport the corresponding moment entries on both sides of a function-preserving permutation.
- **Novelty / control:** [Git Re-Basin][rebasin] aligns weight symmetries and [#109](https://github.com/manojbajaj95/cl/pull/109) warns that gauge writes may protect nothing. Exact permutation equivariance is a sanity check, not a win; compare re-basin plus full slot transplant plus cached rollout.
- **First test:** Blind-permute a two-layer MLP, then introduce one same-function redundant channel as a negative ambiguity case. Charge alignment and abstain unless the budgeted predicate identifies a usable role; test against the stacked control.
- **Old-task retention:** Check A/C under relabeling and after useful B in both clean and ambiguous cases; do not count an abstention as a rescue.

#### 07. A splice with a clock-independent payload (P)
- **Mechanism:** Encode a target delayed-response relation rather than raw moments; compile it to legal local values for a receiver's clock and denominators, with a bound on which pulse horizons survive.
- **Novelty / control:** [Adam bias correction][adam] and [optimizer transport][transport] motivate clock-aware conversion; simple closed-form rescaling is the control. The claim is a checked response relation reusable across clocks, not solving one update equation.
- **First test:** Run separate matched-within-pair forks at two clocks, derive the payload at the first, check it at the second under two pulse magnitudes; compare analytic correction plus local rollout. Never swap clocks during a two-sided test.
- **Old-task retention:** Verify rare A and C after both magnitudes and a B tail, rejecting payloads that match the calibration response but fail later.

#### 08. Cross-episode splice composition (P)
- **Mechanism:** Combine two independently validated blocks only when the first application preserves the precondition of the second, and vice versa if order independence is claimed. Export explicit interactions when disjoint storage is not sufficient.
- **Novelty / control:** [TIES][ties] resolves interference in weight deltas; [regression CEGAR][cegar] can recheck the composed trainer. The bar is safe composition at less cost than disjoint mask union plus cached exact verification.
- **First test:** Use a tied-loss MLP with two geometrically disjoint slot blocks but a shared downstream gate. Validate individually, then blind-test the order/commutation check on independent pairs.
- **Old-task retention:** Retain A and C separately after each application and both useful edits. If composition buys A by losing C, it fails.

#### 09. A slot packet with a precision safety margin (P)
- **Mechanism:** Ship an interval of admissible encodings for each copied entry; allocate bits only where rounding would erase rescue or reverse harm under the declared suffix.
- **Novelty / control:** [8-bit optimizers][eightbit] and [4-bit states][fourbit] already compress moments. Compare equal-bit blockwise quantization plus validation; the candidate is a guarantee for a particular transplant, not smaller slots.
- **First test:** Exhaust an eight-value quantizer in two blocks, with the smaller-norm block nearer a gate. Check encodings on a withheld pulse and charge interval metadata.
- **Old-task retention:** Require A/C floors under the entire claimed quantization envelope on the tiny oracle and at a larger-margin B continuation.

#### 10. Counterexample-guided splice splitting (P)
- **Mechanism:** When a blind edit breaks a shared splice check, keep the original payload but split its eligibility predicate by the smallest witnessed confound; allow a second payload only if no cheap sound split exists.
- **Novelty / control:** [Regression CEGAR][cegar] and [correction classes (PR #169)](https://github.com/manojbajaj95/cl/pull/169) already refine scopes. Compare separate CEGAR plus cached minimum repair; the candidate must reuse the same physical payload productively after counterexamples.
- **First test:** Stream edits with two different suffix couplings and one delayed invalidation. Compare after pricing rejected guesses and exact checks; freeze the next family before refinement.
- **Old-task retention:** Measure A/C after accepted blind edits and after the invalidating suffix in clean shadow; isolate the rare C case the coarse scope missed.

#### 11. Teach a learner to rebuild a donor packet (P)
- **Mechanism:** Discard the donor allocation after publishing a target response signature. Synthesize local slots that satisfy it; require a shadow replacement with the receiver's original slots to restore the failure on an available reference fork.
- **Novelty / control:** [learned optimizers][learnopt] learn update rules and [optimizer-state transport][transport] uses prospective value. Compare statically compressed donor plus dequantization and full local repair. A cheap signature must save memory or enable new recipients; approximation alone is not novelty.
- **First test:** Retain two calibration pulses, erase donor slots on the test fork, fit candidate slots from a discrete legal grid, and test a different pulse/edit; keep the original donor only in an isolated oracle for true reverse validation.
- **Old-task retention:** Confirm rare A recovery and ordinary A/C after B; do not count agreement with the donor signature as retained service.

#### 12. Donor-quorum specificity (I)
- **Mechanism:** Given several safe donors, score supports by how often forward rescue and reverse harm co-occur, rather than attributing the effect of one unusually large donor to a universal slot.
- **Novelty / control:** [Causal abstraction][causal] already tests interchange across examples. Treat this as a specificity audit; compare stratified random donors and magnitude rank with the same shadow trials.
- **First test:** Separate donors by equal immediate update but different moment histories. Withhold a donor family; ask whether the quorum selects a smaller, more reusable support than a single donor.
- **Old-task retention:** Score A/C for the winning support on held-out receivers, including rare A; never average away an unsafe committed edit with safe donor pairs.

### C. Realize the same intervention with truthful batches

#### 13. Separate directional memory from step scale (P)
- **Mechanism:** Build two silent batch words, one that moves `m` at matched `v`, another that moves `v` at matched `m`, to actuate the block a splice identified without privileged writes.
- **Novelty / control:** [Matched Specialization][matched] separates second-moment structure and effective step scale via direct interventions. The claim is constrained, repeatable **sample-only** control of each channel. Compare trajectory matching with the same endpoint and moment constraints and independent direct swaps as ceilings.
- **First test:** Enumerate length-two to length-four words from four distinct labeled contexts, permitting the same predeclared schedules for every arm; report when one of the target directions has no legal realization.
- **Old-task retention:** In both actuator arms check A/C throughout the word and under a new B pulse, including the C slice harmed by a generic denominator shift.

#### 14. Compile a splice into a batch word (P)
- **Mechanism:** Convert the target splice's response contract, not necessarily its exact slots, into a truthful batch word that preserves weights and is safe at every prefix. Return infeasible rather than silently switching to a raw slot write.
- **Novelty / control:** [MTT][mtt] fits trajectories; [#141](https://github.com/manojbajaj95/cl/pull/141) already supplies delayed release. Compare those together with the same examples and constraints, not synthetic examples versus privileged access.
- **First test:** Compile a frozen one-block transplant with a tiny exhaustive word search; reserve a second editor and pulse. If independent unconditioned MTT ties total work and admissions, the compiler adds no primitive.
- **Old-task retention:** Score A/C at all intermediate states and after the editor uses the word; match B utility against the direct splice and projected replay.

#### 15. An order key recovered from a batch multiset (P)
- **Mechanism:** Send a checked permutation of truthful batches that the receiver already has. Different permutations of the same multiset act as distinct slot writes while agreeing on endpoint weights; allow no extra examples.
- **Novelty / control:** [Gradient matching][gm] and [MTT][mtt] can choose sequences; the claim is a portable intervention encoded only as order. Compare uniform and greedy orders plus MTT constrained to the same multiset and compute.
- **First test:** Enumerate four batches with repeated gradient signs but unequal magnitudes; ship an order chosen on train histories, no slot values, and challenge it on unseen histories.
- **Old-task retention:** Auditing A/C at each position rules out orders that temporarily erase an old task even if the final weights return.

#### 16. Deferred cancellation ending before the repair deadline (P)
- **Mechanism:** Separate the two truthful portions of a silent word by one real B update, neutralizing only the witness's weight effect relative to a concurrent B reference. Reject a cancellation that completes after the edit needs the repaired carrier.
- **Novelty / control:** [Delayed transport][transport] already optimizes across committed intervening batches; [#178](optimizer-slot-splits.md) supplies action deadlines. Compare a contiguous witness plus direct replay/checks and an equally budgeted path-specific transport planner.
- **First test:** Insert one frozen B step between two searchable phases. Run a no-witness B fork with matched clock/work and challenge the chosen word with an unseen B schedule; exact alignment is only needed on the claimed scope.
- **Old-task retention:** Track A/C before and after the intervening B step, at cancellation, and after the edit; require the same B utility as the reference.

#### 17. Self-canceling words under local drift (P)
- **Mechanism:** Choose a second truthful batch using a tiny prefix observation to close the weight loop even when the first batch moves differently on a new recipient. Charge acquisition, observation and search as part of the actuator.
- **Novelty / control:** [MTT][mtt] and [delayed transport][transport] could replan on the recipient. The claim is a reusable corrective menu with cheaper validation than rerunning either. Compare open-loop words and equal-query local replanning.
- **First test:** Precompute a two-option closing menu in a scalar learner and hold out initial slot histories. Reject cases when a residual-only shadow arm reproduces the supposed slot benefit.
- **Old-task retention:** Require A/C at the largest intermediate excursion, after either selected closing batch and after unassisted B.

#### 18. An energy budget that still leaves a useful slot trace (I)
- **Mechanism:** Diagnose whether there is a useful witness with bounded maximum path displacement and total path length, not merely zero net displacement.
- **Novelty / control:** [GEM][gem] and [orthogonal gradient descent][ogd] protect old functions during learning. This is a feasibility audit over prefix safety, not a new constraint method. Compare projected replay and equal-radius trajectory matching.
- **First test:** Exhaust a small labeled pool at two radii, with a witness made to fail by taking a large intermediate excursion. See whether any nonplanted word reaches the B target after discarding deceptive endpoints.
- **Old-task retention:** Evaluate independently held-out A/C at every step; displacement radius cannot substitute for behavioral tests.

#### 19. A prefix-safe abort for an incomplete word (P)
- **Mechanism:** At legal stopping points, carry a truthful exit batch or checked no-op, so interruption cannot leave a pending slot effect that makes the next editor unsafe.
- **Novelty / control:** [Reachability][reach] already enumerates recovery actions. Compare precomputed abort plans and exact checkpoint rollback with the same storage/delay; the claim is a reusable recovery branch without undoing separate useful B work.
- **First test:** Abort each prefix of a three-phase word in a tiny learner; allow one next-editor arrival between phases. Withhold the arrival schedule; log when no exit fits the budget.
- **Old-task retention:** In each abort case require A/C before exit, after exit and after a new useful edit; an unsafe incomplete prefix falsifies the contract.

#### 20. An impossibility witness for a sample-only actuator (P)
- **Mechanism:** When all legal weight-returning words miss a candidate's response region, return a separating certificate (or a finite exhaustion certificate) instead of recommending more search.
- **Novelty / control:** [Reachability][reach] already certifies inaccessible regions. The possible primitive is a cheap reusable separation of transaction interfaces: a permitted slot write can work while no legal truthful word can implement it under the same retention and deadline.
- **First test:** Enumerate words up to four steps on a finite gradient pool with a legal direct splice. Check a simple exclusion bound on blind batch libraries, including one where an extra legal context makes the witness feasible; compare cached enumeration.
- **Old-task retention:** Verify A/C after the direct splice and across any legal counterexample word. Exclusions apply only to the declared pool, path floors, and horizon.

### D. Make the two branches compete

#### 21. A splice that predicts which lawful witness matters (P)
- **Mechanism:** Use two-sided swaps to prune a witness compiler's search to small causal supports, but keep a nonminimal, larger-support arm when minimum supports have no lawful realization.
- **Novelty / control:** [Slot mediation][stored] plus [MTT][mtt] is the stacked baseline. Novelty requires a causal support to reduce lawful search enough to offset its discovery and checking overhead without shrinking the reachable safe edit menu.
- **First test:** Use one four-block world where the smallest synthetic splice is unreachable by any legal word but a larger one is reachable; blind-test support-guided search against parallel direct search plus trajectory matching.
- **Old-task retention:** Require both the accepted word and the paid stacked baseline to satisfy the same A/C floors across prefixes and useful B edits.

#### 22. A common obligation across slot and data interfaces (P)
- **Mechanism:** Validate one receiver-side response obligation against either a slot packet or a lawful minibatch word, keeping a separate path-safety obligation for the word. Route the same blind edit to the cheaper available interface, without trusting equality of weights alone.
- **Novelty / control:** [Neural proof sharing][proof] already reuses proofs; regression checks can be cached for each interface. Beat separate optimized verification for both plus a price-based router, not a control forced to ignore one interface.
- **First test:** Use a mixed stream where some recipients lack slot-write permissions and others lack a truthful sample pool. Introduce one shared response premise invalidated by a new suffix; check that both routes stop relying on it, while the word's extra prefix check is still charged.
- **Old-task retention:** Exercise independent A/C on actual forward continuations through both routes, with a rare-slice failure reserved for the changed premise and equal useful B progress.

## Ranked deeper questions

1. **Does a minimal two-sided block found with one editor remain useful to a blind second editor without the source?** Start with card 01. Separate the exhaustive planted oracle from natural incidence; challenge the block and its check against full swap, reset, norm-matched damping and short full-state repair. A sparse rescue without a reverse effect or a blinded transfer is not the proposed primitive.
2. **Can truthful batches realize a useful silent repair without residual weight drift, clock mismatch or intermediate forgetting?** Start with card 02 and test the held-out pulse. Exact paper cancellation is only a positive control. If residual drift alone predicts success, or path-constrained MTT and projected replay tie at equal utility and work, drop the sample-actuator claim.
3. **Does causal localization reduce the cost of finding a lawful implementation?** Try card 21 only after both seeds survive separately. Count swaps, search and failed candidates; deliberately include cases where the smallest transplant has no lawful word. If the stacked control ties, keep splice diagnosis and witness design separate.
4. **Which premises actually survive an optimizer or editor change?** Treat schedule, precision and suffix shifts as negative controls for reuse. A contract that abstains correctly but never admits more edits or saves work is a useful diagnostic, not a portable training operation.

**Verdict:** Keep the two score-3 seeds as independent candidate primitives, not a merged win. If selected later, try cards 01 and 02 as CPU falsifiers, then card 21 only if both survive. If full-state transport/repair plus cached verification ties, report a diagnostic; if only direct slot writes work, report causal mediation, not a usable sample-only repair. No pilot is launched here.

[adam]: https://arxiv.org/abs/1412.6980
[causal]: https://arxiv.org/abs/2106.02997
[cegar]: https://arxiv.org/abs/1806.04829
[eightbit]: https://arxiv.org/abs/2110.02861
[fourbit]: https://arxiv.org/abs/2309.01507
[gem]: https://arxiv.org/abs/1706.08840
[gm]: https://arxiv.org/abs/2006.05929
[learnopt]: https://arxiv.org/abs/1606.04474
[matched]: https://arxiv.org/abs/2610.15830
[mtt]: https://arxiv.org/abs/2203.11932
[ogd]: https://arxiv.org/abs/1910.07104
[proof]: https://arxiv.org/abs/2608.19351
[reach]: https://arxiv.org/abs/1709.07523
[rebasin]: https://arxiv.org/abs/2209.04836
[reset]: https://arxiv.org/abs/2306.17833
[stored]: https://arxiv.org/abs/2608.20442
[ties]: https://arxiv.org/abs/2306.01708
[transport]: https://arxiv.org/abs/2608.24593
