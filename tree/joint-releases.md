# Joint releases shaped by co-occurring edits

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Demand-shaped neutral structure](demand-shaped-neutrality.md) ([PR #191](https://github.com/manojbajaj95/cl/pull/191)), cards 06 and 21. **Review seed:** [Flood triage row 298](https://github.com/manojbajaj95/cl/blob/433078891ef76ae1040c9c539cd48c3b5eaf5aba/reviews/flood-triage.md#L298), score 3: use historical co-occurrence to shape a neutral release for the conjunction, and check it on combinations never used for shaping.

**Can a live model make room for two edits together better than it can make room for them separately, without learning either answer in advance?** [Task arithmetic](https://arxiv.org/abs/2212.04089) and [TIES](https://arxiv.org/abs/2306.01708) combine already fitted changes; [MEMIT](https://arxiv.org/abs/2210.07229) fits many known edits jointly; [MQuAKE](https://arxiv.org/abs/2305.14795) tests whether edited facts support composed answers. All are useful controls or evaluation precedents, but none is the test here: learn a *neutral preparation* from past pairings, then spend it on a new pairing without access to its payloads during shaping. [Neural teleportation](https://arxiv.org/abs/2012.01118), [APRNN](https://arxiv.org/abs/2304.03496), and [Smart Predict-then-Optimize (SPO)](https://arxiv.org/abs/1710.08005) already supply function-preserving moves, checked repair, and preparation driven by downstream cost. Beating each in isolation is not enough.

## What would count as a joint release?

- **Prepare, release, spend.** At fixed width and deployed precision, preparation and the release preserve the full old function pointwise on a declared domain `P`: ordinary old inputs (A), rare slices, every affected downstream reader, and all live-write scopes (C). A release is a finite, executable rewrite that makes room for both later writes (B₁ and B₂). Only the spend changes the requested behavior; each new target must clear its own utility floor, and its scope joins C once admitted. Check every visible intermediate or publish atomically and charge for it. A small exact linear or ReLU verifier supplies the proof on `P`; an independent old-task suite checks ordinary behavior and probes for omissions in the declared scope, not the other way around.
- **Hold out combinations, not just instances.** Draw two historical streams with identical singleton counts, difficulties, request counts, and timing, but opposite co-occurrence. For example, use two edge-disjoint regular bipartite graphs of equal degree on the same families; withhold a perfect matching from each while leaving at least one training edge per vertex. Give the blind editor only the current request and public contract. Use fresh payloads throughout the test and keep the held-out edges out of both shaping and tuning. Report seen edges with fresh payloads separately; an edge lookup has no claim to transfer. Also include time/count-matched shuffled history and unilateral streams.
- **Require a non-additive, realized benefit.** At matched total cost and retention, score the fraction of held-out requests on which **both** writes land and still work after publication, not guessed compatibility, freed-but-unused slots, or mean utility across the two targets. Compare joint-shaped and marginal-shaped hosts on the same bundles, then subtract their differences in singleton success for the two members, measured from clean copies of each host. Also report absolute bundle uplift, each singleton result, and the cost frontier; if all writes land, compare end-to-end costs instead. A history-by-pairing crossover with matched singleton performance is the key signature. Test the best legal serial order and joint publication; count a cheap batch transaction or verifier reuse equally in every arm.
- **Beat the stack, not a straw baseline.** Stack independently tuned releases, best-order installation and rounded/runtime-matched exact joint repair with shared certification; also give the stack the correctly shaped host, plus compare against demand-blind recompilation and history-aware SPO-style preparation or teleportation. Give a paid co-occurrence/repair cache the same history and legal actions, and a batched fitter or task arithmetic/TIES both current payloads at spend time where applicable. Charge historical access, preparation amortized over service volume, addressing metadata, precision, scratch, search, failed checks, proof work, commits and fallbacks. Exhaustive repair is a feasibility oracle on the same host and action set, not a competitor to beat at equal search coverage.

The [idea ledger](https://github.com/manojbajaj95/cl/blob/433078891ef76ae1040c9c539cd48c3b5eaf5aba/reviews/idea-ledger.md) rules out another Gramian/readiness forecast, insertion-point pinning as a retention certificate, and sparse black-box interference scores as a merging primitive. Here co-occurrence is a training signal, never a safety argument. The certificates concern executed rewrites and all affected readers; the unit of success is paired service.

### A paper witness: equal solo menus, unequal bundle menus

Take four live ReLU slots, use `u=[x]₊` and `v=[y]₊`, and start with old-head readout coefficients all 1. On `P=[0,1]²` the functions are linearly independent. Hosts `H₁=(u,v,v,u)` and `H₂=(u,u,v,v)` both compute `2u+2v` everywhere. A release may change old-head coefficients in `[0,2]` but not old activations; the spend can replace released slots, but cannot use any slot that still contributes to the old head. The B₁ request addresses slot 1 or 3; the B₂ request addresses slot 2 or 4. The singleton menu and minimal coefficient changes are identical: every slot can be released by moving its coefficient to its twin (two changes). For a bundle, setting both addressed coefficients to zero is possible exactly when each activation class has a survivor. Thus `H₁` admits `(1,2),(3,4)` and refuses `(1,4),(3,2)`; `H₂` does the reverse. Every viable bundle takes the same four coefficient changes. An admitted bundle can spend its two slots on independently specified ReLUs in task-specific heads, dormant on `P` (e.g. `[x-t]₊` and `[y-s]₊` for fresh `t,s>1`), with positive targets outside `P`. Check each new head after its installation and again after the other write.

This is a feasibility contrast under a specified address and action restriction, not evidence of learning a new edge or beating a good editor. Its table is small enough to memorize, and unrestricted reassignment or address remapping may erase the gap. The useful follow-up is to increase the address set, block whole edges, and ask if learning the arrangement from partial pairings beats an explicit matching, exact repair and a paid cache when the restrictions come from real reader contracts. If just changing names explains the effect, it is address allocation, not a new weight-space primitive.

## Idea cards

### Shape the host for conjunctions

#### 01. Compile a bundle-only release
- **Mechanism:** While preserving all old behavior, move live contributions so co-demanded addresses have distinct legal survivors; offer one release that zeros both addresses without adding width.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** The parent's card 06 supplies the joint release; unlike SPO with an unchanged host, the proposed object is an executable neutral rewrite, not a pair predictor.
- **Cheapest first test:** Extend the witness to multiple addresses per family; flip the co-occurrence matchings, block edges, and compare to marginal shaping plus exact joint repair, an explicit matching, and a paid cache.
- **Old-task retention check:** Prove old-head equality through release and spend; test A/C and both B targets after the other write.

#### 02. Learn a counterweight neither release can afford alone
- **Mechanism:** Place two future-releasable carriers so their old-output components are `p+r` and `q−r`. The neutral bundle moves only `p+q` to a shared survivor; neither singleton has a legal destination for its signed `r) component under the same action budget.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Neutral unit groups](neutral-groups.md) already exploits exact cancellation. Here the object to learn is a protected-output component canceled on release across *unseen* partner addresses, with both freed addresses required by the spend.
- **Cheapest first test:** Enumerate three-output linear blocks with bounded coefficient alphabets and both a cancelable and noncancelable history. Compare against fixed cancelling-pair templates, exact repair, and the best singleton plan at the same bundle budget.
- **Old-task retention check:** Prove cancellation at every affected head and include old inputs that isolate `r`; refuse if even one reader sees a residual.

#### 03. Join under quotas, not just linear span
- **Mechanism:** Prearrange interchangeable carriers across bounded-norm or fan-in regions so a bundle can redistribute old work around a jointly saturated region without increasing the number of active carriers.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Neuron Merging](https://arxiv.org/abs/2010.13160) redistributes a pruned unit's contribution. The proposed object is a checked exchange of scarce survivor capacity across two release sites, not two independently valid merges.
- **Cheapest first test:** Enumerate a tiny capacitated flow on live affine units; compare learned exchanges to exact min-cost flow after either host preparation. Remove the cap as a negative control.
- **Old-task retention check:** Check old readouts, capacity limits and C across the actual redistribution, not just existence of a flow.

#### 04. Give a pair one spare boundary, not two spare neurons
- **Mechanism:** Align two release rewrites so they can reuse one movable ReLU breakpoint. Move it outside protected cells to create two useful edit regions with separately addressed outputs.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Net2Net](https://arxiv.org/abs/1511.05641) preserves function under architectural expansion; the claim here is that co-demand can prepare a shared, subsequently spendable boundary without width expansion.
- **Cheapest first test:** Enumerate segmented one-dimensional ReLU blocks and hold out intervals and address edges. Compare with independent breakpoint fitting plus APRNN and unrestricted exact breakpoint search.
- **Old-task retention check:** Verify on the common old/new cell refinement, including both sides of every protected breakpoint and all downstream readers.

#### 05. Leave the partner choice until the payload arrives
- **Mechanism:** Prepare a neutral rewrite with two mutually exclusive completion branches. Use one generic opening move when B₁'s payload is known; resolve the branch when B₂ is revealed, without undoing B₁.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Finite safe regions](finite-safe-regions.md) already offers feasible menus. This is a reusable opening move that preserves *alternative paired completions* after it is used, not a ranked list of complete releases.
- **Cheapest first test:** Enumerate a two-step game with delayed B₂ and a single scratch slot. Compare to exact online planning, deferring all work, and cached full plans; count waiting time.
- **Old-task retention check:** Prove the shared prefix, both completions and the stop-after-B₁ path; after B₂, verify B₁'s newly acquired floor as well as A/C legacy tasks.

#### 06. Compose unseen partners by a checked interface equation
- **Mechanism:** Factor candidate release witnesses into local redistributions plus signed boundary obligations. Join two parts only when their obligations cancel and a composed verifier proves the whole release; store parts, not edge answers.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Mergeable writes](mergeable-writes.md) separates compatibility from safe publication; the candidate here is a reusable interface for assembling a *pre-spend neutral release* from previously unpaired pieces.
- **Cheapest first test:** Train on a connected bipartite graph with withheld edges. Compare factorized witnesses to exact repair with memoization and a same-byte table; include a false match with equal interface signatures but a hidden reader.
- **Old-task retention check:** Extend the checked cut to that reader; refuse any pair for which signature cancellation cannot be lifted to the full protected cone.

### Spend, interrupt, and renew

#### 07. Preserve both spend orders by construction
- **Mechanism:** Compile the neutral release into two independent write locations plus, where needed, a verified correction to their shared readout, so either installation order gives both targets.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Task arithmetic and [mergeable writes](mergeable-writes.md) make composition the comparison point. This candidate shapes the live host before learning either delta and certifies the two orderings rather than only their merged endpoint.
- **Cheapest first test:** Enumerate two writes on a small residual net where a stale readout spoils one order. Compare re-fitting the second write and exact joint repair at the same latency.
- **Old-task retention check:** Run A/C at both prefixes and the endpoint; check that whichever new task lands first survives the second.

#### 08. Make a half-used joint release safe to abandon
- **Mechanism:** Design a release whose unused half can be donated back by a finite inverse on the released support, retaining the first useful write even when its expected partner never arrives.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Cancelling-pair renewal](cancelling-pairs.md) and rollback are controls; the object is a selective inverse of an *unspent* half of a joint release after the other half has changed the live model.
- **Cheapest first test:** Use a three-arrival CPU stream (B₁, B₂ or timeout, then D); compare rollback plus B₁ replay, leaving the slot idle, and exact repair.
- **Old-task retention check:** Prove the inverse on legacy scopes and on the acquired B₁ behavior; B₁ must survive the donation and subsequent D.

#### 09. Spend a bundle without burning the next co-demand edge
- **Mechanism:** Choose release witnesses that carry an exchange route for a later bundle even when both initial spends pin their new addresses; use overlapping witnesses with different surviving carriers.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's pin witness and [self-replenishing capacity](self-replenishing-capacity.md) already address renewal; this isolates the incremental cost of renewing a viable *pair* rather than one slot.
- **Cheapest first test:** Replay one fixed pin trace over a short stream with overlapping and disjoint later bundles. Compare exact re-enumeration with memoization and compare hosts matched on first-bundle costs.
- **Old-task retention check:** Keep both initial acquisitions live during the second release; verify their readers and target floors before accepting a later spend.

#### 10. Let an arriving write absorb the other's old work
- **Mechanism:** During the joint release, transfer shared old computation to a legal survivor; fit the first new skill to reuse that survivor without moving its old outputs, making the second slot available without a separate scaffold.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** MEMIT already fits co-arriving targets jointly. The candidate is a service protocol in which a neutral redistribution creates a reusable shared feature whose old-function obligation survives later learning.
- **Cheapest first test:** Fit two small analytic tasks with and without a shared feature. Use exact multi-target fitting plus matched architectural constraints as the control; if it finds the same reusable carrier at equal cost, drop the primitive claim.
- **Old-task retention check:** Prove the transfer before fitting and re-prove the survivor on old scopes after each fit, including any old task that uses the feature differently.

#### 11. Ask for one partner bit, not a forecast of both payloads
- **Mechanism:** When two safe release paths differ only on the unseen partner address, request the least information needed to choose between them, then shape both continuations without learning either task value.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Data-only edit cost](data-only-edit-cost.md) already prices information for edits. Here value comes from shrinking uncertainty about which *joint neutral action* is executable, not guessing co-occurrence from a confidence score.
- **Cheapest first test:** In a finite ambiguity game, compare the cheapest useful query to asking for the full address, top-pair lookup, waiting, and exact budgeted diagnosis.
- **Old-task retention check:** Refuse service if the reply is absent or ambiguous; prove retention on both answered paths and check A/C through fallback.

#### 12. Route around a live pin without isolating either write
- **Mechanism:** Use co-demand to build two equally neutral ways to vacate the pair. After a recorded pin arrives, select a finite witness that avoids the pinned unit or reader binding entirely, even if it shares other support.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's reroute already handles a pin. The differentiator is whether paired admissibility survives the same pin trace better than combining two robust singleton menus.
- **Cheapest first test:** Enumerate overlapping groups on a small readout and include a cap that invalidates every signed-equivalence reroute. Compare exact joint re-enumeration with memoization.
- **Old-task retention check:** Check the pin at the downstream reader, not the insertion point; verify the exact move and both edits on every live scope.

### Separate mechanisms from cheaper bookkeeping

#### 13. Swap the support, not the predictor
- **Mechanism:** Transplant a function-equivalent support between hosts shaped by opposite co-demand, discard private labels and reset charged metadata. Keep all surrounding weights and the public editor fixed.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) supplies alignment; this specializes the parent's card 21 to ask if the *pair interaction* follows the support rather than just the singleton direction.
- **Cheapest first test:** Run cross-history swaps, within-history shams, a same-byte cache swap and an overlap-breaking sham matched on norms, width and solo menus.
- **Old-task retention check:** Audit the entire reader cone and old-task floors before and after transplant, then again after the first successful held-out bundle.

#### 14. Move only the paired frontier
- **Mechanism:** Seek a neutral rewrite that changes which pairs can release together while keeping each address's singleton minimum-cost curve unchanged.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** Neural teleportation changes optimization geometry. This isolates joint editability after controlling *all* measured marginal editability, not just pre-edit loss or the mean number of free slots.
- **Cheapest first test:** Exhaustively tabulate singleton and pair frontiers in the witness class; then match hosts on singleton costs and test the held-out crossover against equivalent label permutations.
- **Old-task retention check:** Use the same full retention verifier in every cell, including shams, and check C after the later of the two installs.

#### 15. Prove the verifier work wasn't just shared setup
- **Mechanism:** Charge proof setup once in every arm; give independently prepared releases a joint proof of their actual composed endpoint. Measure whether shared support also creates strictly new feasible joint spends.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** [Certified Continual Learning](https://arxiv.org/abs/2407.06697) motivates incremental verification. Reusing proof work alone is an optimization, not a learned neutral release.
- **Cheapest first test:** Cross separable and genuinely shared old constraints with shared and separate verifier setup; compare solution sets under exact enumeration before comparing proof costs.
- **Old-task retention check:** Require identical protected scopes and proof strength, and include a hidden cross-reader for which two local proofs do not compose.

#### 16. Try hard to explain the effect with changed addresses
- **Mechanism:** Factor a candidate gain into a physical release and a logical rename. Give the control the cheapest admissible indirection table, including reader rebinds; retain a weight-space claim only for what renaming cannot reproduce.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** Git Re-Basin quotients label permutations; this audit asks whether the same quotient explains the entire joint-service crossover.
- **Cheapest first test:** Use the witness with freely rebindable addresses and then with one genuinely immutable reader binding. Compare to exact remapping plus repair, charging metadata and downstream checks.
- **Old-task retention check:** The immutable reader must see its original output through both installation orders; check resolved reader identities as well as task scores.

#### 17. Learn repeated structure, not an edge list
- **Mechanism:** Shape releases from local demand motifs that recur across address groups, then compose them at an interface shared with a held-out group whose atoms were seen only in other pairings.
- **Novelty vs nearest prior art — IMPROVEMENT:** [SCAN](https://arxiv.org/abs/1711.00350) and [CFQ](https://arxiv.org/abs/1912.09713) motivate blocking compounds while exposing atoms. The proposed test transfers verified actions under recombination rather than predicted labels.
- **Cheapest first test:** Use both edge-blocked and motif-relabelled splits, and compare to a matrix-completion predictor plus exact joint repair and a history-indexed cache. Balance singleton frequencies within each arm.
- **Old-task retention check:** Test the held-out motif against the full old task bank; matching the intended graph edge is not a retention certificate.

#### 18. Ask whether the joint move survives actual arithmetic
- **Mechanism:** Shape two old-output contributions to cancel in the deployed number format, including the update and accumulation order. Exclude a release if cancellation exists only at wider precision.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent already charges quantization and rounding. Here precision is crossed with pair demand to distinguish a portable joint witness from a precision-dependent tie.
- **Cheapest first test:** Enumerate small integer/quantized blocks with exact bounded arithmetic, compare to rational repair rounded at deployment and exact integer repair, and charge extra bits as state.
- **Old-task retention check:** Prove deployed equality on A/C and test the first rounding-boundary input that would distinguish the shared move from the exact-real one.

### Stress the conjecture

#### 19. Let co-demand reverse while old obligations persist
- **Mechanism:** Use a neutral exchange to retarget joint releases to a new pairing graph without clearing old pins or loading a new model. Measure the service lost during the handover.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Continual backprop](https://arxiv.org/abs/2306.13812) recycles representational capacity, and the parent considers obsolete singleton demand. This isolates turnover when singleton demand does not change at all.
- **Cheapest first test:** Alternate two matched-marginal graphs and vary dwell time; compare fresh exact recompilation, cache refresh and no retargeting including transition costs.
- **Old-task retention check:** Keep all old and previously accepted bundle scopes active through the switch, including rare slices not sampled in the second regime.

#### 20. Track what the pair cannot give back
- **Mechanism:** Have each finite witness declare which other bundle it makes unavailable under the same pins and caps. Charge that lost executable option when choosing between equal immediate releases.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Accommodation games](accommodation-games.md) already values future options. Here prices derive from a checked loss of *specific pair service*, not a reserve score or a Gramian.
- **Cheapest first test:** Solve a three-bundle exact game and compare to immediate service, an oracle using all continuations, and cached joint repair. Include a negative where all witnesses leave the same next menu.
- **Old-task retention check:** Evaluate retention on the selected release and its certified continuations with already accepted tasks still live.

#### 21. Find the bottleneck that no co-demand can move
- **Mechanism:** For a frozen move set, derive a lower bound on the survivor resources required to preserve independent old outputs. Separate impossibility under this contract from a large search bill.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** APRNN or an exact solver can report infeasibility; an interpretable obstruction could generalize across pairings. Unlike the killed sparse-rank idea, derive it from actual protected functions, not a structural sparsity pattern.
- **Cheapest first test:** Give the verifier exact independent functions, then replace one with a dependent one without changing the graph. Compare a symbolic bound to exhaustive feasibility in both cases.
- **Old-task retention check:** Deliberately force the infeasible edit and exhibit the old-task input or reader it breaks; the admissible case must still pass the ordinary A/C verifier.

#### 22. Use triples to break a pairwise explanation
- **Mechanism:** Learn reusable joint releases for pairs, then try to assemble a triple whose three pairs are each feasible. Require a new simultaneous witness when pair witnesses compete for the same survivor.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Mergeable writes](mergeable-writes.md) already questions coalition closure. The object here would be a checked composition rule for neutral release fragments that consumes survivor claims once, rather than a learned higher-order interference score.
- **Cheapest first test:** Enumerate blocks with three required addresses and one shared constrained survivor; include both a positive triple and a pairwise-compatible but infeasible triple. Compare exact three-way repair and cached pair closures.
- **Old-task retention check:** Use a single whole-coalition proof on A/C; test all three newly acquired behaviors after the final spend, not only the pair endpoints.

## Ranked deeper questions

1. **Does reversing historical co-occurrence flip held-out bundle service without moving the singleton frontier?** Start with 01, 13–17: block edges as well as payloads, swap the support, and give the stack exact joint repair, equal verifier sharing and a paid co-occurrence cache. Stop if the crossover follows metadata or label permutations, disappears under a second blind editor, or only improves already seen edges.
2. **What executable object crosses an unseen edge?** Compare signed counterweights (02), capacity exchanges (03), and checked interface composition (06, 22). Look for a fragment that measurably expands the budgeted service frontier when composed, refuses a planted hidden-reader or shared-survivor negative, and beats exact repair with memoization at full cost.
3. **Can a paired release survive the first spend, a missing partner, and a live pin?** Use 05, 07–09 and 12. Replay the same arrivals and pins in every arm; count partial spends, abandonment, and subsequent pair service under the same acquisition floors. If best-order repair or ordinary rollback-plus-replay ties, do not call the release reusable.
4. **Where does the advantage stop being worth buying?** Cross precision, co-demand drift, and verifier burden (15, 18–21). Report amortized break-even in served bundles and identify the move restriction or protected bottleneck responsible. If wider legal actions remove the effect, report a result for the restricted editor, not general weight-space memory.

**Verdict:** Keep the score-3 idea as a falsifiable candidate, not a novelty verdict or a compute request. The clean win is a held-out bundle advantage that tracks historical co-occurrence and follows a neutral support transplant, with unchanged singleton service and no sacrifice of A/C. If exact joint repair plus marginal preparation and a paid cache match it at full cost, report batching or address allocation, not a new primitive.
