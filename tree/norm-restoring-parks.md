# Norm-restoring parks: pay for renewal with ordinary learning

**Status:** Ideas only; one paper fixture, no pilots or GPU work. **Parent:** [Producer rewrites](producer-rewrites.md) ([PR #247](https://github.com/manojbajaj95/cl/pull/247)). **Seed:** score-3 [flood triage, row 363][triage], [round 55, PKR12][pkr12]: join #247#12's useful old update with #237#04's producer-side closure and #236#13/#246's live continuation. **Ledger read first:** [Idea ledger][ledger]. **P** marks a candidate reusable primitive, not established novelty; **I** marks a method, comparison, or falsifier.

## The bet and what would count

A park is a fixed public maintenance interface for a useful new edit **B**. It should become ready again after each admitted ordinary update, without selecting a new park, resetting live moments, or computing a history-specific repair. **A** is frequent old service; **C** is independently required old work, including rare old obligations. C data, labels, objective, due reads, and allowed optimizer law must be legitimate independently of B. Measure C's actual learning progress against vanilla C; neither an inert C step with a rename nor a corrective step charged to nobody counts as ordinary work.

- **Fix the contract before seeing B or future order.** Publish the park, entry/clear and admissible B scripts, public context `p`, admitted arrivals, allowed cuts (including preemption, if promised), finite horizon or inductive invariant, and reader family. Freeze which inputs survive deletion and which old outputs must still work. For a fixed public context and coupled randomness, the same public norm law `ν(p)` must hold across reachable histories, not necessarily across different public inputs. It cannot be a cached old norm, a code for hidden history, or a per-history choice of recipe. The rewritten producer must get the scale from lawful surviving inputs.
- **C closes the reader relation; the rewrite closes the scale path.** Two hidden states can retain different moments if the declared readers see equivalent park behavior. Check entry, first and second moment effects, next emitted norm, clip predicate, effective native update (direction and size), and downstream reads through clear and continuation. Compare traces for the paired histories under common public arrivals and scripts. Show each ordinary update returns to the same licence for every reachable ready entry and admitted order; if B is available during a write, prove those cuts too. Otherwise charge unavailability and still check old service at every served cut. Do not force history-dependent authorized old outputs to be equal: judge each against its own task.
- **Beat the stack, not just a reset.** Compare vanilla old training; each part alone; norm reset and live-slot reset separately; fixed clip; the strongest legal public scale schedule (at the producer or readers); and re-parking after each update. Stack the best public schedule, strongest legal constrained C updater (e.g. projected/reparameterized training), and exact incremental checks, with the same ABI and atomicity options. If a scalar is the only outward effect, a reader computing the same lawful schedule should tie exactly; don't create a win by forbidding it. Charge data, all extra writes and checks, optimizer state, bytes, waits, refusals and failed edits. Compare at matched realized A/C utility and B progress or report the frontier. Include a late reader, a split write, same-flag/different-action clipping, and an ordinary arrival with no admissible restoring rewrite.

**Prior-art floor (quick Hugging Face Papers lookup, not a priority claim).** [NFNet adaptive gradient clipping][agc] already scales gradients by parameter norms; [RMSNorm][rms] already buys rescaling invariance. [Adam][adam] is the live adaptive denominator control, not an erasable scalar. [GEM][gem] projects updates for old tasks; [learned optimizers][l2l] shape update dynamics; [trajectory matching][mtt] fits what training does to states. [Control barrier functions][cbf] cover return/forward-safety reasoning and [Net2Net][n2n] covers function-preserving rewrites. The ledger's Noether result warns against inferring finite-step survival from ideal invariance; read-pinning warns against certifying producer outputs while the downstream response moves. None of these comparisons makes assembling the pieces novel. The bet is a contract in which **the same work that genuinely learns C renews a usable, post-deletion B interface**, with a measurable advantage over assembling those pieces separately.

## A paper fixture: both parts matter, but the best stack ties

Fix a public calibration target `c ∈ {1/2, 3/4}` before each two-arrival episode. Two reachable starts can have `x=c/2` or `3c/2` (e.g. a previous half-step toward target `0` or `2c` from `c`). Treat a live old-feature block with `h∈{−1,+1}`, `y=h/2`, and momentum `m∈{0,h/4}` as the rest of the admitted entry set. C really needs to fit `(x−c)²/2+(y−h)²/2` on each arrival. Use ordinary unit-step SGD on the first block and fixed momentum on the second:

```text
x' = x − (x−c)
m' = (m + h−y)/2
y' = y + m'
```

The original norm producer emits `sqrt(x²+m²)`. Rewrite it to emit the norm of the surviving calibration coordinate `x`; retain the live `y,m` path. The same public park is available after each C commit, with scale `|x|=c` and native B action `min(1,c)=c` on a public unit proposal in a separate edit register. B and clear leave the C registers alone. Before C, the rewritten scale varies with the two `x` starts; after C, the original producer still leaks the first-boundary momentum magnitude (`1/4` vs `3/8`). In both cases after C, the clip predicate alone would not establish equality. For example at `c=1/2`, the old producer clips both unit proposals but yields `sqrt(5)/4` and `5/8`.

Check A's sign prediction on `y` and C's calibration and sign-conditioned regression at each served commit and after B/clear. Across the two C steps, `y/h` is either `1/2 → 3/4 → 1` or `1/2 → 7/8 → 9/8`; the sign stays correct, regression error drops on the first step and does not increase on the second, and calibration loss becomes zero. Momentum remains live, and a delayed reader using `m` as B's direction would invalidate the proposed contract. A reset of `m` before C changes the authorized `y` trajectory; a public reader emitting `c` after C ties this B trace exactly. A fixed threshold cannot give both required B actions. This is a two-arrival sanity check, not an unbounded closure proof: the SGD block is algebraically an assignment, B is isolated, and neither establishes an advantage. A useful next fixture must remove those conveniences.

## Idea cards

### Make the useful C step earn the return

#### 01. One C gradient pays two debts (P)
- **Mechanism:** Choose a trainable feature basis so a required C minibatch changes the old prediction while correcting both the next native moment action and the producer's norm input. Freeze that basis before the held-out batch schedule.
- **Novelty vs nearest prior art:** [GEM][gem] projects for old losses; the candidate is a reusable correction performed by the unaugmented C loss at matched learning gain, not projecting a second time.
- **Cheapest first test:** Enumerate rational two-feature squared-loss batches and fixed momentum with alternate honest orders. Remove the assignment in the fixture, and compare basis-only, rewrite-only, and joint training against projected C plus the best public schedule.
- **Old-task retention check:** Track A margins and held-out C error at every served cut and after B/clear; include a shared feature where the cheapest correction damages rare C.

#### 02. Restore an action without restoring the moments (P)
- **Mechanism:** Train C into a paired relation where differences in first moment and preconditioning cancel **on the declared B proposal directions**, but remain live for C. Rewrite the scale separately from that ratio.
- **Novelty vs nearest prior art:** [Adam][adam] normalizes using its moments; [parent #13](producer-rewrites.md#13-quotient-the-old-transitions-by-what-the-next-editor-can-do-p) proposes a quotient. The sharper bet is learning an invariant cancellation on a useful proposal set when neither moment is individually invariant.
- **Cheapest first test:** Use an Adam-like two-coordinate rational toy with predeclared perfect-square denominators, two B directions and one out-of-span direction. Compare exact moment projection plus a public scale, and a step that preserves clipping but breaks cancellation.
- **Old-task retention check:** Apply a withheld C gradient outside the B span after B/clear and score A and C on the next live update as well as its starting checkpoint.

#### 03. Correct only the sign of a future collision (P)
- **Mechanism:** Use C to move two hidden states to opposite sides of a gauge symmetry where the norm and native B action agree, while their moment signs continue to serve distinct old contexts.
- **Novelty vs nearest prior art:** [RMSNorm][rms] is norm invariance, and the ledger's Noether memory failed once actual updates/rebalancing were used. The claim needs finite-step action closure after C and legal rebalancing, not retention of a conserved scalar.
- **Cheapest first test:** Enumerate a sign-symmetric two-unit model, ordinary finite-step momentum, and a permitted gauge rebalance. Compare symmetry augmentation plus public scaling and an optimizer that erases the moment sign.
- **Old-task retention check:** Test both contexts' A outputs and C gradient progress before and after rebalancing, clear, and an asymmetric rare arrival.

#### 04. Spend C progress on the hardest reachable pair (I)
- **Mechanism:** Select among equally due truthful C minibatches by the worst pairwise reduction in native action discrepancy, within an explicit service deadline. Certify closure for all remaining legal orders; do not silently prune a hard order.
- **Novelty vs nearest prior art:** The [parent's][parent] order and counterexample cards already support selection and repair; a minimax batch discriminator is a stronger prioritization rule, not a new interface.
- **Cheapest first test:** Exhaust two due batches whose mean discrepancy falls equally but whose worst pair differs; compare random, gradient-matched, and worst-pair selection plus the same public producer.
- **Old-task retention check:** Score rare C by its actual deadline and A at each prefix. Missing a due C label counts as a failure even if all served B actions match.

#### 05. Let lawful C contraction buy exactness only where needed (P)
- **Mechanism:** Train C to shrink a hidden discrepancy into a single certified quantized return cell. A rewritten producer consumes permitted surviving inputs within that cell; exact action is checked on the deployed quantized reader, not inferred from small real-valued distance.
- **Novelty vs nearest prior art:** [Barrier invariance][cbf] and the [parent's][parent] precision card cover the ingredients; the test is exact reusable return with looser private-state constraints than exact projection.
- **Cheapest first test:** Simulate fixed-point SGD on a rational grid with a threshold one unit away; compare stochastic rounding, exact projection, and public reader scaling plus exact cell checks.
- **Old-task retention check:** Verify A, rare C, and C's convergence floor on both sides of each rounding boundary and with the same B/clear script.

#### 06. Separate the debts in time without moving the park (P)
- **Mechanism:** Factor one ordinary C update into useful feature learning and moment propagation. Arrange the producer input and reader coupling so every advertised cut already satisfies the same licence even when the two writes land at different times.
- **Novelty vs nearest prior art:** The parent's #16 already asks for non-atomic renewal; this card requires both a scale debt and a native-action debt to stay discharged across the exposed split, not merely an old-service margin.
- **Cheapest first test:** Exhaust all legal interleavings of two C writes and one B edit. Compare atomic projection, reparameterized independent writes, and a split where the norm is already correct but the direction still diverges.
- **Old-task retention check:** Resume C after B at each advertised cut, then clear and score A and rare C. Charge any stall or refused edit to availability.

#### 07. Use a task's lawful slack as temporary private storage (P)
- **Mechanism:** Keep moment information in an existing C-sensitive direction unused by B, provided the next allowed C update cannot route it back into B's declared reads. The norm producer uses a different, surviving statistic; no copied norm is permitted.
- **Novelty vs nearest prior art:** [GEM][gem] and the parent's parked-null directions already separate update effects; the stronger hypothesis is reusable law-preserving transport of information that is useful to C but irrelevant to all declared B continuations.
- **Cheapest first test:** Test a three-coordinate rotation where one ordinary update moves slack into a new C coordinate and a later update can leak it into B. Compare a fixed block split and save/restore at matched bytes.
- **Old-task retention check:** Withhold the C probe whose response needs the transported moment and verify it after the second arrival and B/clear.

#### 08. Teach an arrival that fixes the next denominator, not today's scalar (I)
- **Mechanism:** Aim C training at the moment read on a later native update while the rewritten norm law handles the immediate scale. A batch that only reduces today's discrepancy is a negative control.
- **Novelty vs nearest prior art:** [Trajectory matching][mtt] already targets later training states. The refinement is matching a small set of licensed future reads while keeping other C state live, not inventing a new training objective family.
- **Cheapest first test:** Pair short adaptive-moment trajectories that agree at one boundary and diverge on the next nonzero gradient. Compare current-only matching, two-step matching, and exact per-arrival parking at equal real C data.
- **Old-task retention check:** Score frequent A and withheld rare C after the second native update, then repeat after clearing the same B edit.

### Make the surviving inputs earn the norm

#### 09. Use a public norm law with more than one useful value (I)
- **Mechanism:** Fix one park and one rewritten producer whose scale depends on a legal current calibration input, not on the retained clip history. Predeclare B targets with disjoint acceptable scale intervals across public contexts.
- **Novelty vs nearest prior art:** [Adaptive gradient clipping][agc] already varies scale by context, and the parent already proposes public curves. This is an identifiability control: fixed clip should lose, the equally expressive public schedule should tie.
- **Cheapest first test:** Start with the two calibration targets above, then add an unseen public value. Let both producer and reader controls compute the same allowed law.
- **Old-task retention check:** Check A/C when calibration values alternate and test the rare C probe after the out-of-fit public value and clear.

#### 10. Rewrite an internally reused norm rather than a last-mile clip (P)
- **Mechanism:** Replace the norm at a seam that feeds both a native update and a local C path, preserving C's lawful old behavior. Require the one surviving-input rewrite to remain valid under subsequent ordinary C gradients.
- **Novelty vs nearest prior art:** [Net2Net][n2n] preserves current functions under a rewrite; the candidate benefit is reducing duplicated checks or extra writes for future native consumers, not beating a scalar-only reader substitute.
- **Cheapest first test:** Give the producer two uses (a clip and a shared trust-ratio calculation). Allow the baseline to patch both legally and compare matched utility, writes and verification cost rather than imposing a read-only restriction.
- **Old-task retention check:** Test a C trajectory whose next gradient uses the internal branch; check it alongside A after two arrivals and B/clear.

#### 11. Recover scale from a retained job, not a retained copy (P)
- **Mechanism:** Learn a factorization where a C-essential calibration feature suffices to compute the norm after each honest update. Demonstrate independent use of that feature by an old reader; forbid a backup accumulator or per-history decoding.
- **Novelty vs nearest prior art:** [RMSNorm][rms] factors scale from representation. The proposed capability is removal of one historical accumulator while continued C work maintains the surviving inputs, under a fixed storage allowance.
- **Cheapest first test:** Delete the old accumulator after creating reachable histories with identical current calibration and different old accumulators. Compare current-feature reader substitution and a same-byte shadow statistic charged as retained state.
- **Old-task retention check:** Ablate the calibration feature to demonstrate its independent C use; keep A and rare C intact without that ablation, including delayed C after clear.

#### 12. Find a late read by changing the continuation, not spoofing the slot (I)
- **Mechanism:** Search honest C suffixes and actual B/clear continuations that convert a currently invisible moment into a norm input or action change. Minimize the witness to a reachable pair and its discriminating reader.
- **Novelty vs nearest prior art:** [Seam leaks](seam-leaks.md) already requires reachable witnesses; this targets a false PKR12 win where the apparent renewal is real at the first boundary and false on continuation.
- **Cheapest first test:** Plant a rare reader after a second C update, plus a harmless old-only moment read. Compare read-set tracing and exhaustive paired search against an endpoint audit.
- **Old-task retention check:** Include a pair that passes A/C despite a B leak and a pair that fails delayed C despite equal B; require the audit to distinguish the failures.

#### 13. Refuse when normal service and common scale have no joint solution (P)
- **Mechanism:** For each reachable history, compute the set of scales consistent with immutable old readers and useful B actions. Return a small witness for an empty intersection rather than reset moments, re-park, or make B inert.
- **Novelty vs nearest prior art:** The parent's obstruction card already rules out incompatible edits. This version identifies the **ordinary arrival** after which even a lawful producer rewrite cannot restore the common norm while retaining old service.
- **Cheapest first test:** Use equal public contexts where a due C continuation leaves old downstream readers requiring disjoint intervals, e.g. `[1/4,1/2]` and `[3/4,1]`, of the same mandatory export. Compare exact intersection and a bound checker; then give C its own allowed input as a positive control.
- **Old-task retention check:** Verify A and mandatory C survive safe refusal; run each unlawful scale in the fixture to locate the lost C obligation, and debit the unavailable B edit.

#### 14. Preserve a vector witness behind a public scalar (P)
- **Mechanism:** Train C and the rewrite to preserve the joint response of several readers (clip, gate, native update) while only the norm is public. Treat the vector of permitted actions as the proof obligation, not something to log or store for each history.
- **Novelty vs nearest prior art:** The parent's #07 already compiles one statistic for several readers. The candidate extension is a shared continuation proof for useful C-driven renewal when individual scalar checks would miss a joint action effect.
- **Cheapest first test:** Give two readers a common public coin. Let gate and direction bits be correlated in one history and anticorrelated in another, so their marginals tie but their executed actions do not. Compare independent public schedules, a joint schedule, and exact trace checking under coupled seeds.
- **Old-task retention check:** Drive both branches of the old workload plus the rare joint C read after clear; do not replace genuine historic A/C differences by common targets.

### Make renewal reusable, or make it lose

#### 15. Reuse a return proof across independently written B editors (P)
- **Mechanism:** Export a checked response basis for a declared family of readers. A separate B builder fits within it and checks only its new directions instead of revalidating the whole C arrival graph.
- **Novelty vs nearest prior art:** [Seam leaks](seam-leaks.md) already indexes proofs by consumers, and the ledger's read-pinning failed when the consumer moved. The new candidate covers the native response of later readers following ordinary C renewal.
- **Cheapest first test:** Hold out two B writers inside the basis and one whose downstream layer changes the response. Compare warm exact incremental checking with identical time/bytes and allow it to cache the same common subproofs.
- **Old-task retention check:** Evaluate A and rare C for each B builder after two renewals and clear, including the builder that must be refused.

#### 16. Use the same C batch across several legal parks without selecting one privately (P)
- **Mechanism:** For distinct public interfaces announced up front, train C to close their common reader relation. Each park keeps its own fixed law and is selected by a declared public request, never by hidden optimizer state.
- **Novelty vs nearest prior art:** [Seam leaks](seam-leaks.md) already proposes public park portfolios. The new test is whether one required old batch pays the return cost of several different norm laws more cheaply than separate closure proofs/updates.
- **Cheapest first test:** Use two parks with overlapping and then disjoint correction constraints; compare dual constrained training and independent parks with shared cached checks.
- **Old-task retention check:** Alternate public park requests during A and C, score rare C after both clear orders, and report the cost of parks that cannot be offered.

#### 17. Renew under a truthful delay without pretending the norm was restored (I)
- **Mechanism:** If a promised C batch is not yet due or available, allow only the already certified B subfamily until the same full licence returns. Publish this as an availability profile, not full-time closure.
- **Novelty vs nearest prior art:** [Barrier methods][cbf] and re-parking already bound safe waiting. This is an honest service control that can kill a claim of uninterrupted renewal.
- **Cheapest first test:** Enumerate a stream with one delayed corrective batch and one urgent B offer. Compare immediate re-parking, waiting for relaxed B, and a public schedule plus an exact checker.
- **Old-task retention check:** Keep A served during the delay and meet the original C deadline; score A/C after each refused or accepted B and clear.

#### 18. Factor renewal by delayed-reader horizon (P)
- **Mechanism:** Maintain different proof depths for newly requested B continuations, using one park and one producer. A longer horizon can expand the audited moment effects, but cannot change the norm law already promised at shorter horizons.
- **Novelty vs nearest prior art:** Bounded continuation proofs are in the [parent][parent]; the candidate is amortized extension when C keeps regenerating the short proof while obligations for long readers grow.
- **Cheapest first test:** Build a four-step recurrence with one late read and compare proving from scratch, exact incremental certificates, and a factored proof with a reusable prefix. Count editor refusals.
- **Old-task retention check:** Score A/C at every horizon boundary and after a subsequent ordinary update, not just at the short B clear.

#### 19. Retain the same public scale under a legal optimizer migration (P)
- **Mechanism:** Transfer live C state into a new optimizer representation using a public map and let the next required C batch finish the return. Request the same B action before and after migration on declared supported cuts.
- **Novelty vs nearest prior art:** [Net2Net][n2n] and [learned optimizers][l2l] are controls for preserving function and adapting dynamics. The bet is a composable return certificate across changes in the native action, beyond keeping endpoint predictions.
- **Cheapest first test:** Switch between two small momentum parameterizations, first exactly conjugate (must tie an exact map), then approximate. Compare optimizer-state conversion plus a public reader with fresh re-parking.
- **Old-task retention check:** Test a rare old batch whose first migrated update depends on the inherited moment and score A before switch, through B/clear, and on continuation.

#### 20. Force a negative result with the strongest scalar substitute (I)
- **Mechanism:** Construct a scalar-only ABI where the public reader can implement every legal producer schedule, and a coupled ABI where a schedule-only replacement may leave the native update wrong. Use both as controls before testing any learned renewal.
- **Novelty vs nearest prior art:** The [parent's][parent] strongest-control search is the precedent. This is a reduction test, not a new primitive: prove equivalence in the first regime and price a legal multi-reader replacement in the second.
- **Cheapest first test:** Enumerate exact B traces with and without an internal feedback edge from scale, giving the control the same legal inputs and change budget. If it ties both, retire the rewrite advantage claim.
- **Old-task retention check:** Include A and rare C after the feedback edge's second use; count old damage caused by any attempted substitution or repair.

#### 21. Derive a minimum cost for an honest return (P)
- **Mechanism:** Given actual due C gradients and allowable ordinary steps, bound the achievable reduction in reader discrepancy before the B deadline. Use the bound to distinguish “learn a better basis” from “no admitted C update can renew this park.”
- **Novelty vs nearest prior art:** [GEM][gem] supplies feasible update cones and [barriers][cbf] bound invariant transitions. The candidate certificate separates lack of truthful restorative work from an unfixable producer, and can reject proposed parks before running them.
- **Cheapest first test:** Enumerate all legal fixed-momentum steps in a small rational C task with rank-one gradients, then add a single legitimate off-axis batch. Compare a reachability bound and exact enumeration against fresh re-parking.
- **Old-task retention check:** Require each eligible C move to maintain A margins and meet held-out C progress, and each refusal to leave ordinary old service intact.

#### 22. Test whether one C update eliminates two separate checks (P)
- **Mechanism:** Couple the producer's surviving-input precondition and the reader-action invariant in one proof of an ordinary C transition. Compare using that joint certificate with proving or refreshing each obligation independently.
- **Novelty vs nearest prior art:** [Barrier reasoning][cbf] already composes invariants and the parent already couples norm laws and renewal. The possible primitive is a checkable shared witness that future C arrivals and B readers can reuse at lower total cost, not an intersection declared by fiat.
- **Cheapest first test:** Enumerate a finite two-moment state machine, then add an independent old updater and a held-out B reader inside the declared family. Compare one shared certificate against the strongest separate stack with memoized proof sharing. Include a regime where independent obligations tie.
- **Old-task retention check:** Exhaust A/C served prefixes, commit, clear and a rare continuation for both updaters. Match real C progress and B actions before comparing proof bytes, waits, and rejected offers.

## Ranked deeper questions

1. **Does joint renewal buy useful edits or cheaper guarantees once the strongest separate stack is allowed?** Start with #01/#10/#22: shared old/new features, live moments, a legal multi-reader schedule, and B writers held out inside the declared family. Require identical useful B action and matched A/C floors; compare edit availability and full cost. If the stack ties, PKR12 is a workflow, not a primitive.
2. **When can truthful C work restore native action without overwriting old optimizer information?** Use #02/#08/#21 to separate moment-wise equality from action equality under a delayed adaptive read. Find a finite-step condition applicable to real C gradients, and an arrival whose feasible restoring set is empty.
3. **What is the smallest sufficient reader contract that survives future ordinary work?** Use #12/#15/#18 to look for the first lawful continuation that separates apparently equivalent histories. Ask whether a shared response proof costs less than exact incremental checks without hiding refused readers or widening a supposedly fixed licence.
4. **How much of the advantage survives exposed writes and overdue C?** Use #06/#17 with independently scheduled arrivals and B offered at every promised cut. Distinguish real availability from an atomicity assumption or a service delay, at matched deadline and retention.

**Verdict: ambitious but testable on paper or CPU; no pilot result.** Preserve a single falsifiable claim: a genuine C update and a surviving-input rewrite can jointly buy a cheaper or more available fixed licence for nontrivial B at the same old-task utility. Equal norms, finite endpoint matches, and a tie with the lawful separate stack do not pass. If the first coupled fixture cannot produce an advantage over that stack, keep the negative control and stop before scaling.

[parent]: producer-rewrites.md
[ledger]: https://github.com/manojbajaj95/cl/blob/a7116c90af9084f7fe94df0fd9ec4c2c59156116/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/a7116c90af9084f7fe94df0fd9ec4c2c59156116/reviews/flood-triage.md#L363
[pkr12]: https://github.com/manojbajaj95/cl/blob/4ad1c6637ea57f2409bd1ae47b46abe0b7ac3a12/ideas/flood/cross-pool-55.md#L27
[agc]: https://huggingface.co/papers/2102.06171
[rms]: https://huggingface.co/papers/1910.07467
[adam]: https://huggingface.co/papers/1412.6980
[gem]: https://huggingface.co/papers/1706.08840
[l2l]: https://huggingface.co/papers/1606.04474
[mtt]: https://huggingface.co/papers/2203.11932
[cbf]: https://huggingface.co/papers/1903.11199
[n2n]: https://huggingface.co/papers/1511.05641
