# Curved parks: teach finite chords through live Adam

**Status:** Ideas and paper fixtures only; no learner runs, implementation, or GPU work. **Parent:** [Relation parks](relation-parks.md) ([PR #255][parent]). **Seeds:** Parent cards 02 and 14, the new score-3 ideas in [flood-triage][triage]. **Read first:** [Idea ledger][ledger].

## What would count

The two seeds change **which existing records train together**, not the learner's update rule. A chord is one committed update on a batch of two truthful records, not two sequential single-record updates. For a fixed serving read `R(x,y) = y − f(x)`, a parameter step `d` is on-park exactly when `d_y = f(x+d_x) − f(x)`. At a regular point its tangent defect is then the finite Taylor remainder `f(x+d_x) − f(x) − f′(x)d_x`, generally nonzero. Neither a tangent projection nor a small gradient is evidence of chord closure. Require independently exercised roles for both coordinates on real readers and useful B training. A level set that can be straightened locally is not a result by itself; ask whether the same **lawful records and ordinary optimizer** can realize the useful moves with equal cost after a change of coordinates, or with a frozen coordinate.

For a fixed-size swap, keep record IDs and multiplicities, exchange intact training units, and compute the actual signed defect `e_i(s) = R(w + d_i(s)) − r` at the reachable state `s = (w,m,v,t,…)`. Adam's step uses the bias-corrected first **and** second moments from the candidate's actual batch gradient; the second moment receives the elementwise square of that **batch** gradient, not the mean of squared record gradients. For old and new membership with respective displacements `d,d′`, the exact score change is

> `e′ − e = (d′_y − d_y) − [f(x+d′_x) − f(x+d_x)]`.

This is a signed finite effect, not a Hessian norm. To isolate reachable curvature in a swap, compare its signed score change at two actually reachable states; to isolate the two-slot interaction, also compare the two one-slot-frozen diagnostic arms at the **same** pre-state. The diagnostic arms do not issue batches, and independently mixed slot values need not be reachable. Rebuild the reachable prefixes after each proposed exchange: the old offending batch-ID order should improve, and every legal order and public boundary must still pass. Include the deployed optimizer's epsilon, clipping, weight decay, and precision whenever present.

**Shared first-test contract.** Freeze the old park read, independent held-out routine A and rare C jobs, their margins and service times, and a meaningful B deadline/holdout before opening the pool. Admit one public partition before membership freezes; evaluate every legal prefix across all entry aliases in scope, then one public clear and common next update with carried slots. Timeouts and fallback service count as service outcomes. Use an exact enumerator on tiny pools as the feasibility oracle, not a baseline the same action space can out-admit. Compare at matched useful B progress, records, arrival rights, and verification budget against the strongest stack of independent relation parking plus optimizer-aware reachable rebatching ([#225][rebatch]), then add affine parks, tangent/finite retraction, freezing, raw curvature, [GraB][grab] with and without its order advantage, random swaps, and both single-slot ablations. A candidate primitive must expose a useful new operation or a reusable proof with lower cost on held-out pools; a better heuristic alone is an improvement. **P** = primitive candidate, **I** = improvement or necessary control; neither is a verdict.

## Two paper fixtures

### F1. Ordinary two-record batches take exact non-tangent steps

Start at `(1,1)` with `R=y−x²=0`. Take ordinary SGD at learning rate 2 on the mean of two squared-error record losses. A fixed labeled source supplies zero-target x-only and y-only records with known positive loss coefficients (equivalently squared feature magnitudes): for each `k ∈ {1/2, 3/4}`, one record has loss `(1−k)x²/2` and one has loss `(1−k²)y²/2`. This stylized source is specified up front; the compiler may only pair the supplied records. Pairing by k gives `(x,y) → (kx,k²y)` and preserves R at every committed update. The direction changes both coordinates, with tangent defect `(1−k)²x² > 0`. Either single record alone at the same optimizer setting leaves the park, as does mismatching the x/y records. For the no-landing twin, replace the fixed old read by `y−x⁴` from the same start; no two-record batch from these four lands on-park at the first update.

| Frozen execution | First committed weights | Second committed weights |
| --- | --- | --- |
| Half-scale first | (1/2, 1/4) | (3/8, 9/64) |
| Three-quarter-scale first | (3/4, 9/16) | (3/8, 9/64) |

An old A family predicting `z+R` retains its target z even for held-out z; independent rare C requires `x+y ≥ 7/16`. Held-out B squared error `x²+y²` is at most `9/10` at tick 1 and `1/5` at tick 2 in both orders. Public clear just ends the membership window; a common next truthful pair with `k=19/20` still gives `R=0` and `x+y=12369/25600 > 7/16`. This is a positive feasibility witness, **not** a win over exact retraction or over a known representation of the scaling symmetry. The records are engineered to make the mechanism visible.

### F2. Both Adam slots reverse a swap ranking, but the next chord fails

Fix the same old read `R=y−x²` at `w=(0,0)`. Use standard bias-corrected [Adam][adam] with `β₁=β₂=1/2`, no clipping or decay, `ε=√6−2 > 0`, and public step-2 rate `η=√6−1`. Consider two step-1 histories with gradients `(−a,−a)`, `a∈{1,4}`, initially zero slots. These aliases are reachable at the same weights from suitable initial weights (each starts at minus its first-step displacement, with its corresponding truthful squared-loss target); this is not a same-initialization construction. At step 2 a coordinate whose next gradient is `−k` moves by

> `D(a,k) = η[(a+2k)/3] / (√[(a²+2k²)/3]+ε)`.

Use two-record mean squared-error batches with fixed truthful two-output targets. The initial batches have y-targets `(1, 2η−1)` and `(3−2η, 1)`; all x-targets are 1. Swapping `2η−1` and the second batch's `1` gives both batches mean target `(1,1)`, without changing the record multiset. Every raw batch-loss Hessian is the identity. A finite raw-SGD score at the same rate prefers the *original first batch* (`k=η` in y: raw `R=η²−η²=0` versus `η−η²` after swap). Executed Adam instead has `D(1,1)=D(4,1)=1`: `|m̂|` and `√v̂+ε` both double across aliases, so either swapped batch lands on `(1,1)`. The two original batches have nonzero signed defects (`D(a,η)>1>D(a,2−η)` for both aliases). Using one alias's updated numerator and the other's denominator for the swapped batch would give `d_x=d_y=2` or `1/2`, neither on-park. These cross-slot probes diagnose alias cancellation, not feasible combined states.

Within either single pre-state, changing only the first slot from the original first batch to the swapped batch undershoots `d_y=1` (the old denominator is larger); changing only the second slot overshoots (the old numerator magnitude is larger). The x step remains 1. Thus a fixed-state single-slot diagnostic also misses the chord; the raw reversal here is local to the first batch, not a claim about the raw score of the worst prefix.

On the first committed update A predicting `z+R` retains its target z only after the swap; a separate old C “balanced” classification with margin `1/2−|x−y|` passes in all first-step arms, and held-out B x-error is zero in all. **Do not certify the partition.** After either first batch in the swapped partition, the other has zero gradient at `(1,1)`, but still moves both coordinates by the same positive d under live Adam (keep the public rate `η`). Then `R=−d−d²`: A breaks even though C and the batch loss at that prefix do not warn. This deliberately tuned fixture separates a transferable first-edge cancellation from a transferable window. It does not establish a practical epsilon regime, a useful second B deadline, or superiority to joint exact verification.

## Idea cards

### Make truthful chords a usable operation

#### 01. Index record pairs by the finite remainder (P)
- **Mechanism:** Index truthful record pairs by which range of x and live states makes their two-axis displacement satisfy the chord equation. Look up pairs by the *signed* departure from the tangent, issuing a small witness with the IDs and its valid domain.
- **Novelty vs nearest prior art:** [ONG][ong], retraction, and OGD modify the update; [iterative machine teaching][teaching] already chooses examples. The candidate is a reusable edge index for unmodified ordinary updates on a fixed live old read, not the existence of an example curriculum.
- **Cheapest first test:** Generalize F1 to a nonhomogeneous cubic read and hide a second pool; compare exact enumeration, tangent matching, and finite retraction with identical B milestones. A single global change of coordinates exposing a matching shortcut is a control, not a win.
- **Old-task retention check:** Read A at both ends of every issued chord, exercise unseen C states near the claimed domain boundary, and verify both again on a common post-clear update.

#### 02. Pair using a provable monotone order, not all pairwise previews (P)
- **Mechanism:** Find a public chart in which the rank order of x-record demand for normal displacement and y-record supply is the same at all reachable x. Batch by rank; reduce the check to interval endpoints only if the paired defects are provably monotone, and fall back to exact search when ranks can cross.
- **Novelty vs nearest prior art:** Sorted transport and batched gradient matching are known. The gap is a state-uniform ordering derived from the finite chord condition that saves *executed optimizer previews* without losing exact admissions in a defined family.
- **Cheapest first test:** Sweep two to eight labels per side in a one-dimensional chart, with one held-out family whose two interior ranks cross while the endpoints appear sorted. Compare with exhaustive partitions and sorted matching on raw gradients.
- **Old-task retention check:** Score A and rare C at the rank crossing and on the actual fallback path; also compare every B deadline so easy tail deletions cannot buy a cheaper certificate.

#### 03. Repair an entire matching with a reachable no-good cut (P)
- **Mechanism:** When a candidate ordering fails, extract the smallest prefix membership pattern sufficient for the signed defect and use it to forbid that pattern across all matching completions. An alternating path can then move the normal correction to a different pair without losing any records.
- **Novelty vs nearest prior art:** Conflict-directed search and #225's witness-guided swap already exist. The proposed object is a relation-specific cut that rules out *many curve-induced prefix failures* without checking each new matching independently.
- **Cheapest first test:** Use three disjoint pairs where every single exchange is infeasible but a three-cycle repairs the partition. Add a twin where a tempting cut ceases to be sound after the first pair changes the reachable x range.
- **Old-task retention check:** Require real A/C service at the earliest refuted prefix and after each accepted prefix, not merely on the final park; include refused windows in the denominator.

#### 04. Certify a generation rule for a family of chords (P)
- **Mechanism:** Derive a small identity in observable data and state that proves closure of every chord in a whole family, not only at enumerated weights. A newly observed pair can inherit the witness after checking its record parameters.
- **Novelty vs nearest prior art:** F1's scaling is a symmetry and does not count; exact invariant synthesis is also established. The conditional advance is a cheap, reusable *record-side* witness for a family with useful noncommuting updates and no single scale parameter.
- **Cheapest first test:** Look for two polynomial squared-loss feature maps on one smooth read that share a certificate form but move in different directions. Compare with symbolic invariant checking on each pair and with exact graph traversal.
- **Old-task retention check:** Withhold an A input class and C queries at chart extremes; require they survive new pairs and a later old-task update without widening tolerances.

#### 05. Cross a dead zone with one committed truthful batch (P)
- **Mechanism:** A legal finite update may cross an off-park region with no observer inside the atomic update, landing on a second component of a fixed old read's level set. Its two records must both contribute to a useful B deadline and must not be separately committable.
- **Novelty vs nearest prior art:** Disjunctive parks and ordinary mode switching already cover two pockets, including [sealed entry][sealed]. The distinction is a useful **within-window** chord crossing not reachable by service-safe continuously constrained moves, at the already-deployed read granularity.
- **Cheapest first test:** Use the two components of `x²−y²=1`, two natural examples and a B item only serviceable on the other component. In the twin expose an intermediate off-park state through a real split commit; give the retraction baseline the same permitted discontinuous actions.
- **Old-task retention check:** Run independent A and C before and after the hop and at every real observation point; reject if the result depends on removing an existing read.

#### 06. Return to the same old value with a changed next-write capability (P)
- **Mechanism:** Choose two noncommuting chord batches that leave every due old read equal in either order but leave distinct next-B capacities. Admit the order-free start only if a common later truthful batch uses both terminal states, or both supply the same next deadline.
- **Novelty vs nearest prior art:** [Commuting writebacks][commute] already reason about observable order equivalence. The proposed gap is using the curved, noncommuting walk as productive state, rather than merely showing unequal hidden endpoints.
- **Cheapest first test:** In a two-axis curve graph have both paths pass the same A/C reads and only one meet a common continuation. Seek a second pair that admits both paths and beats a matched commuting park in B service, not simply in state divergence.
- **Old-task retention check:** Run the same A/C continuation, including a normal old update before the next B request, without resetting either endpoint.

#### 07. Find the minimum truthful arity of a useful chord (P)
- **Mechanism:** On restricted record families, characterize the smallest legal batch that realizes a non-tangent chord. Use convexity or the discrete gradient lattice to produce an impossibility witness for all smaller batches at a fixed, declared optimizer.
- **Novelty vs nearest prior art:** Teaching dimension and sparse coreset selection already measure example count. This bound is on the arity of a *single service-safe finite transition*, not the sample count to fit a hypothesis; it matters only if it predicts pooling costs beyond exact small enumeration.
- **Cheapest first test:** Construct a fixed pool with one useful three-record chord and no one- or two-record chords, then promote F1 to the two-record positive control. Exhaust every subset and give accumulated gradients the same permitted read timings.
- **Old-task retention check:** Report worst A/C margins after each committed update and measure actual service while waiting to fill a larger batch.

#### 08. Train for future chord supply without changing the old reader (P)
- **Mechanism:** During earlier ordinary training, select useful updates that shape the model's response to a later family of paired truthful records; freeze the serving read and verify the predicted increase in chord availability on unseen arrivals.
- **Novelty vs nearest prior art:** Meta-learning and machine teaching already make future adaptation easier. The extra target is *more legal finite on-park edges at equal old margins and B gain*, not a favorable effective learning rate or an arbitrary writable subspace.
- **Cheapest first test:** Compare two tiny initializations after identical old-task training, chosen by ordinary validation vs a chord-availability objective on disjoint source pools. Match feature norms, old margins, and unrestricted B speed; test a no-chord task family.
- **Old-task retention check:** Keep A/C fixed before training, recheck their held-out inputs throughout the unseen B window, and reject if the new initialization only sacrifices a rare slice.

#### 09. Certify the defect in deployed arithmetic (I)
- **Mechanism:** Replay the exact rounded commit for arithmetic-sensitive pairs, or prove a directed bound on the *difference* between normal motion and curve remainder. Split near a rounding tie; return unknown if the remainder is below resolution.
- **Novelty vs nearest prior art:** Floating-point interval verification already exists. This is a precision falsifier for a good paper chord, not a new learning operation.
- **Cheapest first test:** Scale F1 until a coarse preview rounds two pair signatures into the same bin, while actual rounded commits straddle an old-read boundary. Compare direct simulated commits and a generic independent interval bound.
- **Old-task retention check:** Use deployment arithmetic for A/C, including rare cases one representable step from the boundary and the next optimizer commit.

#### 10. Close two independent old curves with a single pair (P)
- **Mechanism:** In three live coordinates, require the same two-record step to land on the intersection of two fixed nonlinear old reads. Look for evidence that one record provides shared curvature correction rather than two independent compensators packaged together.
- **Novelty vs nearest prior art:** Multi-constraint retraction and modular parks are existing routes. A primitive candidate needs joint truthful realizability that buys useful progress or fewer records against a stack of per-reader protectors.
- **Cheapest first test:** Cross `y=x²` with `z=x³` and a two-record action language. Include a separable 4-record solution, an exact joint selector, and a twin where the two constraints demand incompatible displacements.
- **Old-task retention check:** Score old A and rare C separately at every deadline and retain a third holdout read that detects replacing one curve by a redundant copy.

### Make swaps see the actual adaptive step

#### 11. Issue a full two-slot chord receipt (P)
- **Mechanism:** For an exchanged batch, certify the signed finite defect from its correlated post-update moments, not from its raw gradient or denominator alone. Store the conditions under which both axes of the result satisfy the chord.
- **Novelty vs nearest prior art:** #225 already does joint Adam rebatching; F2's ranking reversal alone is an improvement. The candidate is a small cancellation receipt that can be reused across unrelated warmed histories instead of rerunning joint verification.
- **Cheapest first test:** Extend F2 to a held-out warm-slot family with fixed conventional epsilon and match first-step B gain; compare exact Adam previews, raw exchange scores, numerator-only and denominator-only scores, adaptive scores on a linear park, and randomized exchanges.
- **Old-task retention check:** Require A/C on the formerly offending first prefix, its reverse order, and the next real read; F2 as written must be refused.

#### 12. Score the change of a swap across reached states (P)
- **Mechanism:** Form a four-corner signed difference: after-minus-before membership defect at one incoming prefix, minus that difference at another. Use a reusable bound on this interaction to prioritize a shared repair, but rebuild the after-swap reach set independently.
- **Novelty vs nearest prior art:** Reachable-curvature swaps in #244 and #255 already use loss curvature and failing prefixes. The candidate is a finite state-by-membership certificate *of the executed Adam step* that prunes rescoring without freezing either moment.
- **Cheapest first test:** Construct two prefix states with the same parameters and opposite swap effects due to inherited moments. Add a flat reachable twin where raw and adaptive rankings agree. Compare with fresh reachable previews and best cached joint rebatching at equal preview calls.
- **Old-task retention check:** Recheck the worst A and rare C margins under both recomputed reachable sets, including newly reachable offenders not named by the first witness.

#### 13. Check the attainable image, not a product of slot intervals (P)
- **Mechanism:** Represent which joint first/second-moment ratios can arise on both axes from each legal record choice, then intersect their image with the finite chord band. Preserve correlations across coordinates and histories rather than certifying every fictitious box corner.
- **Novelty vs nearest prior art:** Relational abstract domains and interval branch-and-bound already preserve correlation. The candidate is a small Adam/read-specific sufficient representation that matches exact admissions at lower preview or storage cost than generic joint domains.
- **Cheapest first test:** Lift F2 from two points to a lawful one-parameter correlated family plus a twin mixing incompatible histories; compare box bounds, a generic relational domain, and exact/arithmetic ground truth.
- **Old-task retention check:** Query A and C at attainable extremal states and run an adversarial continuation breaking a too-coarse ratio representation.

#### 14. Prove when alias-blind swappers lack enough information (P)
- **Mechanism:** Put two publicly indistinguishable warm histories on the same old curve and construct opposite unique safe swaps. Find the smallest *lawfully readable* joint statistic separating their decisions, or prove that a public partition must refuse.
- **Novelty vs nearest prior art:** Indistinguishability lower bounds and preview access are known. A useful new object would be a minimal decision statistic for finite Adam chord feasibility, versus disclosing full hidden warm state or using an oracle.
- **Cheapest first test:** Exhaust four-record pools over two signed Adam histories with matched public weight and step norm; tabulate the intersection of safe swap sets. Include a nonempty intersection twin and give an exact hidden-state selector only to the diagnostic oracle.
- **Old-task retention check:** Demonstrate the distinct A/C failure for each blind wrong choice, and report retention and delay of the real refusal policy as well as the oracle.

#### 15. Select a swap with a truthful second chord reserved (P)
- **Mechanism:** For each first-safe exchange, check whether the next due, already eligible B unit lands from the *carried* moment pair. Reserve the next usable record IDs before freezing; issue only intersections valid across branches, never a reset between chords.
- **Novelty vs nearest prior art:** Contingent scheduling and [slot echo][echo] already track next-read effects. This asks for a compact two-edge Adam chord composition rule that admits more windows than independent per-edge checks at equal cost or matches exhaustive plans more cheaply.
- **Cheapest first test:** Use F2 as the failure arm and add a tiny pool with a second useful batch compatible with both aliases and both arrival orders. Compare exact two-step search and a first-edge score followed by its strongest legal repair.
- **Old-task retention check:** Require A/C at both commits, at public clear, and after a third common lawful batch; verify second-tick B service independently of zero training gradient.

#### 16. Route opposite momentum signs through the same chord certificate (P)
- **Mechanism:** Use a fixed pair's gradient to move inherited numerators of opposite signs onto the same side of a finite chord condition, while the denominator response supplies the right magnitude. Check sign crossing explicitly rather than taking absolute slot norms.
- **Novelty vs nearest prior art:** Momentum steering already turns carry without reset; this must use the second slot to enable a single truthful swap over sign aliases, not merely damp a large first moment.
- **Cheapest first test:** Enumerate a two-axis Adam toy with aliases sharing `v` and opposite signs of `m`. Compare a first-moment optimizer with matched step sizes, momentum reset, and exact full-state scoring. Require a sign mirror where the same certificate correctly refuses.
- **Old-task retention check:** Test signed C categories, not just squared A drift, as well as old accuracy after the next sensitive update exposes a wrong sign.

#### 17. Transfer chord scores across public clocks (P)
- **Mechanism:** Build a score on normalized moment ratios with explicit clock-dependent validity and a bound for epsilon's change in scale. Reuse it across prespecified checkpoints only when the actually executed bias corrections preserve the chord inequality.
- **Novelty vs nearest prior art:** Standard bias-correction and scale analysis explain optimizer changes. The gap is chart-specific, certified cross-clock *swap decisions* without clock resets, fitted rate changes, or more preview access.
- **Cheapest first test:** Find the same truthful pool at three reachable public clocks with equal raw curvature; include an epsilon-scale twin where ignoring time reverses the winner. Compare exact previews, a time-binned cache, and ratio transfer.
- **Old-task retention check:** Execute A/C at the early and late clocks using their real schedules and carried slots; require the same B deadline rather than allowing a late catch-up.

#### 18. Use a real clipping-branch change to create a chord (P)
- **Mechanism:** A predeclared joint gradient clip may produce the right finite chord only after one truthful exchange moves the batch across the clipping threshold, changing both moment inputs. Certify the live clipping scale, not just the branch bit.
- **Novelty vs nearest prior art:** Clipping-aware rebalancing and [seam-leak checks][seam] already track hidden scale. The candidate is an exchange that uses the unchanged clip as an actuator to create an otherwise unavailable on-park move, versus a generic scale monitor.
- **Cheapest first test:** Enumerate four real squared-loss records near the threshold with a reachable warm start. Compare clipping disabled, a same-branch/different-scale twin, and the strongest exact legal selection at matched B progress.
- **Old-task retention check:** Probe old A and rare C on both sides of the clipping threshold and through the first next-step read that consumes the changed moments.

#### 19. Kill the raw-curvature explanation with crossed controls (I)
- **Mechanism:** Build one control matching raw finite curvature but deleting the second-slot response, and a distinct control with a curved raw loss where the adaptive and raw swap rankings agree everywhere reachable.
- **Novelty vs nearest prior art:** A necessary causal ablation, not a new optimizer. F2 matches raw Hessians, but its positive epsilon and rates are tuned, so a mere ranking reversal cannot establish a general swap primitive.
- **Cheapest first test:** Cross raw-curvature family, Adam denominator family and fixed-park curvature on a four-to-six-record pool. Match B gains and compare full-score, raw-score, random, and both frozen-slot arms.
- **Old-task retention check:** Report A/C safety at each legal prefix in every crossed cell and after common clear; require the flat/aligned nulls to retain their margin at the same B threshold.

### Test whether the two seeds help each other

#### 20. Let a pending old read determine which chord slack is spendable (P)
- **Mechanism:** Prefer a swap that preserves a second independently due old read's *future* viable chord set, not merely its positive margin now. Publish that small set as a consumable constraint and prove the actual next due update can spend it.
- **Novelty vs nearest prior art:** Robust scheduling and the parent already reserve directional slack. What is new if it works is a chord-indexed obligation for an old service update that is itself useful, rather than a scalar safety budget or a hidden repair.
- **Cheapest first test:** Build two first-step Adam ties with equal A/C output margins; only one leaves a common truthful C update on-park before the deadline. Shift that deadline one tick as a control and compare exact joint scheduling.
- **Old-task retention check:** Run actual normal A and rare C service including C's required update; reject a plan that preserves C's read but skips C learning.

#### 21. Compile a joint chord-and-swap witness smaller than the two proofs (P)
- **Mechanism:** Share a relation-specific finite remainder bound between the pair matcher and the two-slot swap verifier. Reuse it for a held-out subwindow only if it certifies the matched pairs *and* excludes every reachable invalid repair.
- **Novelty vs nearest prior art:** A separate park plus #225 rebatching already solves the union. The claim is a genuine interaction: a correlated witness buys lower end-to-end proof cost or more admitted windows under a fixed resource cap, not a larger allowed action space.
- **Cheapest first test:** Factorial-cross affine/curved read and independent/coupled moment response at fixed matched B deadlines. Compare exact joint truth and the best separately optimized stack at equal bytes, raw records, and preview calls.
- **Old-task retention check:** Require the same held-out A/C floors and real deadlines in every cell, including refused-window fallback, clear, and the next shared training update.

#### 22. Make useful chords shrink continuation disagreement without a reset (P)
- **Mechanism:** Instead of driving slot distance to zero, select useful paired updates that contract the *next-read difference* between warm aliases under a fixed family of truthful follow-ons while already closing the curved read.
- **Novelty vs nearest prior art:** [Slot echo][echo] tracks future readers and ordinary decay already contracts some histories. The candidate is a contraction available through actual curved B work and the joint slots that outperforms ordinary decay or generic warm-up at identical B service.
- **Cheapest first test:** Use F2's aliases but design a three-tick positive arm with two chords that jointly contract the gap and a witness where slot distance shrinks while the continuation defect grows. Compare a pause/decay arm, equal-service rebatching, and the exact horizon oracle.
- **Old-task retention check:** Measure held-out A/C at every tick, under multiple predeclared common follow-ons, and during the decay fallback; accept no B progress credit for a no-op.

## Ranked deeper questions

1. **Can one useful two-slot chord rule survive a whole Adam window?** Start with 11, 13 and 15: find a feasible crossed case beyond F2 with conventional epsilon, nontrivial B reads in both orders, unseen warm histories, and a common continuation. Kill the primitive claim if the best jointly scored #225 baseline matches the receipt at equal cost.
2. **When can natural record supply realize finite moves no allowed tangent or frozen-axis policy can?** Use 01, 05, 07 and 08: characterize supply and arity in a fixed non-engineered source, then compare with exact finite retraction at matched A/C and B progress. A smooth coordinate change is not enough to explain a win unless it preserves the allowed actions and service.
3. **What information is necessary to reuse a swap proof?** Use 12, 14 and 17: prove a lower bound from alias collisions, then derive a sound public statistic or costed certificate that generalizes across pools and clocks without hidden-state routing. A refusal must distinguish no lawful solution from insufficient information or a loose bound.
4. **Do curved pairing and adaptive swap scoring interact beyond their strongest separate implementations?** Use 20–22 and the crossed 19 control. Require exact feasibility agreement and a measurable held-out reduction in verification cost or increase in certified useful windows at a fixed cap, with independent held-out old service and matched B gain. Otherwise keep them separate improvements.

**Research call:** First try to turn F2's first-edge reversal into a fully lawful two-batch window, without tuning epsilon to the aliases or manufacturing labels. F1 proves chord feasibility in a structured pool and F2 proves the score distinction can matter; neither yet beats the strongest combined control.

[parent]: https://github.com/manojbajaj95/cl/pull/255
[triage]: https://github.com/manojbajaj95/cl/blob/b8f309216cdf2d4955679d359dde270342aad4c5/reviews/flood-triage.md#L370
[ledger]: https://github.com/manojbajaj95/cl/blob/b8f309216cdf2d4955679d359dde270342aad4c5/reviews/idea-ledger.md
[rebatch]: https://github.com/manojbajaj95/cl/pull/225
[commute]: https://github.com/manojbajaj95/cl/pull/217
[sealed]: https://github.com/manojbajaj95/cl/pull/260
[echo]: https://github.com/manojbajaj95/cl/pull/229
[seam]: https://github.com/manojbajaj95/cl/pull/237
[grab]: https://arxiv.org/abs/2205.10733
[ong]: https://arxiv.org/abs/2508.17169
[teaching]: https://arxiv.org/abs/1705.10470
[adam]: https://arxiv.org/abs/1412.6980
