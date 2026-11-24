# Cancelling release counterweights

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Joint releases](joint-releases.md) ([PR #198](https://github.com/manojbajaj95/cl/pull/198)), cards 02 and 05. **Review seed:** [Flood triage row 307](https://github.com/manojbajaj95/cl/blob/5878c212655d5cf023e9b3e1d46b2618cc462b92/reviews/flood-triage.md#L307), two score-3 ideas: learn signed counterweights that cancel on release across unseen partner addresses; make one neutral opening move before choosing between mutually exclusive finishes when the second payload arrives.

**Can a learner use past demand to change what a later editor can safely do, even when the editor has never seen these addresses paired and does not yet know the second payload?** Cancellation itself is not new: [Cancelling-pair renewal](cancelling-pairs.md) and [Neutral unit groups](neutral-groups.md) already exploit collectively silent structure; [Neuron Merging](https://arxiv.org/abs/2010.13160) redistributes removed contributions. [Finite safe regions](finite-safe-regions.md), [Mergeable writes](mergeable-writes.md), and contingent planning (see [Accommodation games](accommodation-games.md)) already supply safe sets, checked combinations, and policies with delayed observations. The candidate is a demand-shaped arrangement of *live* contributions that lets a blind editor execute a cheaper or otherwise unavailable paired release on an unseen edge, or preserve two genuinely different completions after a useful first write, not merely predict a partner or store two plans.

## What would count?

- **Signed, joint, and useful.** On a declared protected domain, two occupied addresses carry old-output functions `p+r` and `q−r`; `r` is nonzero and not absorbable alone under the legal actions and budget. A joint release transfers `p+q` to a legal survivor and vacates both addresses before any new contribution at those addresses is counted. Prove neither singleton can do this under the same total budget, not just under half the budget. Verify all exposed states or charge for atomic publication. Use both vacated addresses for a genuine write and score actual target utility, not number of free slots.
- **Open before knowing which finish.** On B₁, execute one neutral opening that does not depend on B₂, spend for B₁, and publish its useful behavior before observing B₂ or a proxy for it. From that *same* post-spend state, either B₂ continuation is legal in its own world; both cannot be exercised under the contract. Compare the two branches on cloned post-B₁ states. In a live execution choose only one. B₁ stays available throughout: no rollback, reconstruction from replay, or replacing a saved B₁ checkpoint. A missing or out-of-menu B₂ must leave a functioning B₁, even when it causes a refusal. Do not assume that waiting for B₂ has zero cost.
- **Test transfer rather than recollection.** For edge transfer, design balanced bipartite address families with several edges per vertex; withhold entire compatible edges while exposing their vertices on different edges, and match address frequencies and timing against shuffled or incompatible histories. For address transfer, withhold whole physical partner addresses from shaping *and* tuning; introduce them through the same public descriptor or compiled interface in every arm. An arbitrary unseen ID with no observable structure is not a prediction problem with a solution. Include equal-sign and hidden-reader negatives with the same superficial address cues. Pair historical streams with opposite useful matchings, fresh B₁/B₂ payloads, and identical singleton demand. Match the singleton service frontier and transplant the shaped support separately from private metadata.
- **Beat the strongest stack.** Give controls fixed templates, neutral-group search, checked exact joint repair with proof sharing and memoization, best legal serial releases, and the same logical rebinding if allowed. For delayed B₂ also give a non-clairvoyant exact online planner with the same actions and observations, priced plan cache, eager commitment, and deferring all work. Give the best stack access to the shaped host too, to separate host value from editor value; exhaustive planning on a given host is a feasibility oracle, not an algorithm to beat on coverage. Match width, precision, incumbent utility and acquisition floors; charge history, shaping, interface bytes, scratch and retained state, proof/search, failed attempts, publication, waiting and fallbacks. Score both paired success and worst-branch B₁/B₂ service at fixed costs, then break-even costs at equal service.
- **Retention is a live contract.** A denotes legacy tasks, C all already accepted writes and affected downstream readers. Prove neutrality where claimed on the full declared A/C domain at deployed precision and run independent ordinary-task and rare-slice checks. Once B₁ lands it joins C, even on a timeout. The [idea ledger](https://github.com/manojbajaj95/cl/blob/5878c212655d5cf023e9b3e1d46b2618cc462b92/reviews/idea-ledger.md) disqualifies another readiness/Gramian score, gauge-only memory erased by rebalance, insertion-point pinning as evidence of downstream safety, and gains explained by equal-budget replay or save/restore. Neither small residuals nor algebra true by construction are evidence of useful learning.

### Paper witness: one prefix, two incompatible finishes

Take a protected additive head on `P=[0,1]^6` with independent coordinate functions `h,d,p,q₀,q₁,r`. Five live, immutably addressed slots `s,o,a,b₀,b₁` contribute `h,d,p+r,q₀−r,q₁−r`, respectively. Declare a restricted editor: it may transfer old work only into `s`, which can hold any allowed combination of the first five coordinates but cannot carry `r`. It may clear another slot's contribution only on a proved neutral publish. No rebinding or rewriting surviving carriers is legal. B₁ requires `o`: open by moving `d` to `s`, then install a fresh B₁ payload at `o` in its own output head and pin it. New payloads have zero contribution to the protected head.

After that same opening and spend, B₂ for branch `i` requires `a` and `bᵢ`. Atomically clear their old contributions and add `p+qᵢ` to `s`, then spend the two slots on that fresh payload. The untouched partner still supplies the initial net `−r`. Neither singleton, nor clearing all three, can be neutral because `s` cannot supply the missing `r` coefficient. The two finishes also cannot be taken in sequence because the first pins their shared slot `a`. Refuse a request for both partners alone, which would remove `−2r`; an absent partner leaves the useful B₁ intact. The old-head identities follow by coefficient comparison. B₁ and B₂ utility is a separate check (for instance, make each spent address necessary for a different independently specified output coordinate).

This is a restricted feasibility witness, not a learning result: a hand-authored planner solves it, a wider survivor action set can erase the separation, and the witness says nothing about transfer or a speedup. Use it to test the definitions and reintroduce address variation, independently authored reader contracts, and real search costs before making a stronger claim.

## Idea cards

### Learn what cancels

#### 01. Put the counterweight in the live host
- **Mechanism:** From historical pairings, fit a neutral rearrangement that distributes a signed component across live carriers so releasing a compatible pair requires moving only its unsigned sum. Expose a checked release, not the pairing labels.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** Parent 02 supplies the operation. Neutral unit groups already recognizes sums; the target is an arrangement learned from history that helps at a fresh edge.
- **Cheapest first test:** Replicate the witness across several addresses per sign, train with two alternative pairing histories, and query blocked edges against fixed templates, exact joint repair and best serial release. Swap the shaped support between matched hosts.
- **Old-task retention check:** Compare all old-head coefficients, including inputs isolating `r`, and check accepted writes in C after both freed addresses are used.

#### 02. Compile a partner address that shaping never saw
- **Mechanism:** Learn a map from a public reader/slot description to a signed contribution; create the new partner with a neutral reallocation from its own local survivors. Join with a previously shaped address without consulting a historical edge list.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Parent 06 already checks interface equations. The added object is a truthful registration operation that produces the counterpart at a new physical address under fixed capacity.
- **Cheapest first test:** Withhold one bank of addresses and test neutral onboarding on first contact. Compare a fixed interface generator, exact repair with the descriptor, and a paid predictor plus repair. Shuffle opaque IDs while keeping descriptions unchanged.
- **Old-task retention check:** Prove old behavior during registration and exercise the new bank's original readers before and after the paired release.

#### 03. Identify the transferable part by changing coordinates
- **Mechanism:** Represent the counterweight as a function at the protected cut, transport it through legal permutations and rescalings, and rebind it to the transformed physical addresses rather than matching stored parameter vectors.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Git Re-Basin](https://arxiv.org/abs/2209.04836) aligns parameter permutations; this is a transport audit against the ledger's Noether-memory kill, not a new alignment method.
- **Cheapest first test:** Rebalance a host without changing its function; compare raw signatures, canonical rebinding, and exact remap plus repair. Separately swap only metadata to see which one actually carries success.
- **Old-task retention check:** Prove the rebalance preserves every registered reader, then rerun A/C after the transported release and spend.

#### 04. Cancel on the whole protected cell arrangement
- **Mechanism:** Decompose the signed obligation into piecewise-affine residuals; join candidate partners by function equality on a common ReLU refinement, allowing two different local decompositions of the same residual.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [APRNN](https://arxiv.org/abs/2304.03496) checks finite repair. The proposed reusable object is a transferable cancellation proof between distinct factorings, not matching slopes on a training panel.
- **Cheapest first test:** Use two segmented one-dimensional nets with identical residual functions and a decoy with a narrow extra hinge between probes. Compare to full piecewise-linear repair and sampled-signature matching plus verification.
- **Old-task retention check:** Verify breakpoints and each protected cell, then check old tasks adjacent to the planted hinge after both writes.

#### 05. Export an imbalance witness instead of a compatibility score
- **Mechanism:** When a pair fails, produce a protected input/reader and a separating functional that kills all legal survivor contributions but not the proposed residual. Cache that obstruction only across states for which its premises still hold.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Rejected edit witnesses](https://github.com/manojbajaj95/cl/blob/de750947352309bba99756dc3f8c914233ea3aa2/tree/rejected-edit-witnesses.md) and linear dual certificates already explain infeasibility. Reuse is on a family of signed obligations, not a new certificate calculus.
- **Cheapest first test:** Enumerate a capped linear survivor bank with one capacity change that invalidates an old witness; compare witness reuse to exact solving and a negative-result cache.
- **Old-task retention check:** Show the forbidden release fails at the named old reader; verify every alternative admitted by the same selector on A/C.

#### 06. Match a counterweight modulo legal survivor work
- **Mechanism:** Cancel the parts of the two obligations that lie outside the survivor subspace; send the remaining sum through an exact bounded feasibility check. Reuse the first-stage quotient only while the survivor contract is unchanged.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [GPM](https://arxiv.org/abs/2103.09762) projects updates in activation space. This would make a survivor-relative partner class that can issue finite releases, with a separate capacity proof.
- **Cheapest first test:** Give each address a different raw residual with the same quotient and include a matching quotient whose sum exceeds the cap. Compare to canonical hash matching, exact bounded repair, and cached solve results.
- **Old-task retention check:** Verify the bounded lift pointwise, including old tasks that detect a component removed by the quotient.

#### 07. Change one reader and invalidate only the affected joins
- **Mechanism:** Attach signed obligations to reader-specific dependencies. When a later true acquisition adds a cross-reader, extend the cut; previously matched pairs lacking a proof on the new reader cannot publish.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Training readers](https://github.com/manojbajaj95/cl/blob/5a2172e0ecd35f6f6dd7f0feebf913d7a785cc40/tree/training-readers.md) and mergeable-write certificates already motivate rechecking consumers. The test is whether residual-local invalidation saves enough work without repeating the read-pinning failure.
- **Cheapest first test:** Add a reader that distinguishes one previously equivalent pair, leaving another pair unchanged. Compare selective repair to whole-bank recertification and version-keyed memoization.
- **Old-task retention check:** Run legacy tasks and the newly accepted reader after the attempted release; the bad pair must be refused despite equality at the old cut.

#### 08. Route the unsigned sum across a scarce survivor pool
- **Mechanism:** Use signed matching to nominate a pair, then allocate its unsigned remainder through a shared, capped survivor pool without assigning a permanent reserve to either address.
- **Novelty vs nearest prior art — INHERITED / IMPROVEMENT:** Parent 03 already treats scarce exchanges and min-cost flow. The additional question is whether cross-address cancellation relieves a real capacity cut rather than hiding reserved slots.
- **Cheapest first test:** Enumerate one small capped network with a control that lifts the routing restrictions without adding capacity, and price capacity consumed by the pair. Compare to exact flow plus exact repair and disjoint fixed reserves.
- **Old-task retention check:** Check that all old work arrives at the correct readers and that no previously pinned acquisition is displaced by routing.

#### 09. Make a quantized pair really cancel
- **Mechanism:** Compile both parts and their survivor addition under the deployed accumulator and publish order; reject real-number cancellations that leave rounding or saturation residuals.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** Parent 18 already demands deployed arithmetic; this audit isolates which partner classes survive rounding and whether extra bits explain apparent transfer.
- **Cheapest first test:** Enumerate small signed integer blocks including a saturation-boundary decoy. Compare operand-aware certificates to integer exact repair and wide-real repair rounded back to the same precision.
- **Old-task retention check:** Verify deployed outputs for boundary values with a bit-exact check and exercise the attributable old task after spend.

#### 10. Renew with a contribution from a genuine acquisition
- **Mechanism:** Let a real later task supply part of a new signed pair while it learns its own behavior; neutrally reassign the old workload and recycle a spent release interface rather than accumulating a bank of hidden adapters.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** [Successor recovery](https://github.com/manojbajaj95/cl/blob/743a51a5fe58d60488ec53e720063abf5ad77501/tree/successor-recovery.md) and [triage row 305](https://github.com/manojbajaj95/cl/blob/5878c212655d5cf023e9b3e1d46b2618cc462b92/reviews/flood-triage.md#L305)'s RSL4 already propose recovery bought by the next skill. Here renewal must restore unseen-edge service, not merely recover a known callable route.
- **Cheapest first test:** Sweep three acquisitions under fixed width, one with no reusable feature. Compare the best stack of successor recovery, fresh neutral-group search and same-size cache at matched acquisition utility.
- **Old-task retention check:** Retain A and every previously accepted B/C task at each renewal; verify that refusing a bad renewal does not remove the last learned task.

### Open now, decide later

#### 11. One opening, two finishes that cannot coexist
- **Mechanism:** Compile a neutral first move and publish B₁, leaving one shared writable address and two partner-specific completions; let the actual B₂ payload select which completion consumes the shared address.
- **Novelty vs nearest prior art — INHERITED PRIMITIVE CANDIDATE:** Parent 05 supplies the operation. The residual menus in Accommodation games (card 09) and contingent planning already model alternatives; the target is a cheaper live implementation at fixed width, not branching policy syntax.
- **Cheapest first test:** Exhaust the witness game from one post-B₁ state, including missing and out-of-menu B₂. Compare exact online planning, eager commitment, deferral, and priced full-plan caching; count waiting and scratch.
- **Old-task retention check:** Verify the opening, B₁-only stop, rejected request, and both successful continuations; B₁ must never become unavailable during a finish.

#### 12. Make the opening independent of the payload's last bit
- **Mechanism:** Give two B₂ payloads the *same address*, but make their target functions require incompatible readout changes. Publish a single B₁ opening that works for either case without knowing the sign of a last, withheld target bit.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Parent 05 already delays a choice. This test asks for a payload-conditioned continuation at the same address, which a partner-ID lookup cannot implement.
- **Cheapest first test:** Enumerate a finite affine editor with two target intervals requiring opposite capacity allocations. Hide the interval until B₁ has passed its utility check; compare exact non-clairvoyant planning and a paid two-plan cache.
- **Old-task retention check:** Check A/C and B₁ on the common prefix and both branch executions against identical contracts; verify misrouting fails the B₂ target floor rather than quietly relaxing B₁.

#### 13. Carry the opening to a different editor
- **Mechanism:** Transfer a public description of the published state, pinned B₁ and spent budget, plus residual branch conditions. A fresh editor with only live read access and the B₂ payload checks and finishes without source history.
- **Novelty vs nearest prior art — INHERITED / IMPROVEMENT:** [Safe order families](https://github.com/manojbajaj95/cl/blob/8a1f7adec2c0d5b7e62c4b3baac313489a4f58ac/tree/safe-order-families.md) already hands off partially executed schedules. Here receipts are for mutually exclusive payload-conditioned finishes, not arbitrary residual linear extensions.
- **Cheapest first test:** Hand off after B₁ to an independently implemented solver. Compare from-scratch verification, a paid checkpoint and cached conditional plans at equal transfer bytes; include a stale receipt.
- **Old-task retention check:** Verify the imported B₁ commitment and the actual reachable readers; stale-state refusal must keep A/C and B₁ in service.

#### 14. Buy the smallest observation that selects a finish
- **Mechanism:** After B₁ is published, ask for one truthful payload predicate only if the two viable finishes disagree on it; defer expensive target inspection until the admissible branch is certified.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Decision-relevant queries](https://github.com/manojbajaj95/cl/blob/50f1ef5988107438ac3ae05ea313ba0ebb44fb79/tree/decision-relevant-queries.md) already prices distinctions. The incremental claim is query savings on an executable, already-in-use opening.
- **Cheapest first test:** Enumerate small payload truth tables with identical partner addresses. Compare full reveal, exact decision-tree construction and direct online repair; plant a case where every cheap predicate is uninformative.
- **Old-task retention check:** Keep A/C and B₁ unchanged while observing, and verify the chosen finish against the full actual payload and protected scope before publication.

#### 15. Retire an unused option without taking B₁ down
- **Mechanism:** On timeout or a declined B₂, release branch-only reservations while keeping B₁ live; recover capacity using a verified forward move or simply drop the reservation if there is no weight-state debt.
- **Novelty vs nearest prior art — IMPROVEMENT:** Parent 08 and [Deletion licenses](https://github.com/manojbajaj95/cl/blob/77a12d71d4f921d15156ebea2f050dfa00316be8/tree/deletion-licenses.md) already cover abandonment and safe removal. Here expiry is priced against service during the interval, not credited for reversing an untouched option.
- **Cheapest first test:** Run B₁, timeout or out-of-menu B₂, then D under a single scratch limit. Compare idle reservations, exact forward repair, and rollback plus replay as a priced control that cannot satisfy uninterrupted B₁ if it takes it offline.
- **Old-task retention check:** Certify cleanup and D with B₁ in C, including the stop path where the timeout fires during an old read.

#### 16. Publish a finish without exposing either singleton
- **Mechanism:** Stage the paired weight changes and branch claim privately, then verify and publish one version; make interruptions before publish expose only the post-B₁ version and charge for the staging state.
- **Novelty vs nearest prior art — AUDIT / IMPROVEMENT:** Atomic publication is standard and mergeable writes already requires it. The question is whether paired release remains worthwhile once staged state and pinning are charged exactly.
- **Cheapest first test:** Enumerate visibility points on a two-reader toy. Compare equal-cost atomic publication for all arms to a naive in-place schedule; include a too-small staging budget.
- **Old-task retention check:** Run A/C and B₁ on each exposed version and on interrupted publication; distinguish safe refusal from any transient old-output violation.

#### 17. Keep an opening valid across an intervening accepted write
- **Mechanism:** Compile a residual branch proof with declared dependencies so a third write D may land during the wait. Revalidate the branches from the actual post-D state, never from a restored B₁ snapshot.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Mergeable writes handles compatible subsets and safe-order families handles residual orderings. Here the obligation is to preserve alternative finishes for an unrevealed payload while a third, useful task acquires new protections.
- **Cheapest first test:** Enumerate a B₁–D–B₂ game with one D that leaves both options and one that kills exactly one. Compare joint exact planning, giving D a private reserve, and local version-based invalidation.
- **Old-task retention check:** Check A/C after D and both reachable B₂ outcomes, including D and B₁; never count a pruned branch as available.

#### 18. Bound exactly what a prefix must keep
- **Mechanism:** Derive a lower bound on shared live state and scratch by constructing late payloads with equal observations but disjoint necessary pre-reveal states. Separate a truly impossible common opening from an expensive one.
- **Novelty vs nearest prior art — IMPROVEMENT:** Partial-information games already give common-action obstructions. The useful specialization is an actionable fixed-width bound with a named protected reader or live pin that forces the distinction.
- **Cheapest first test:** Solve two small indistinguishable worlds with and without one extra writable slot. Compare the bound to exhaustive non-clairvoyant and clairvoyant game values; vary the slot restriction independently of task labels.
- **Old-task retention check:** Show which old or B₁ scope each invalid opening would break, and verify both successful branches at the larger budget.

#### 19. Price the latest safe time to commit
- **Mechanism:** Preserve both branches only until the service gain from waiting falls below that of committing to one now, using measured branch availability and actual downtime, not a forecast of memory collapse.
- **Novelty vs nearest prior art — IMPROVEMENT:** Deferral and multistage planning already price delayed decisions; the ledger's replay-deadline kill rules out assuming a cliff. This card tests the actual early-service/capacity trade-off.
- **Cheapest first test:** Sweep observed B₂ delays and relative frequencies, including a smooth no-cliff world. Compare exact online policies, fixed waits, eager commitment and pure deferral under a common latency budget.
- **Old-task retention check:** Measure A/C and B₁ through the wait and after commitment or refusal; an interval with B₁ unavailable is not a cheap opening.

#### 20. Make a misleading early hint harmless
- **Mechanism:** Permit hints to rank which finish to *stage*, but never to bind the shared address. A verified payload predicate and a live state check are required before claiming the mutually exclusive finish.
- **Novelty vs nearest prior art — IMPROVEMENT:** Speculation with guarded commit is established. This audit asks whether a counterweight opening actually permits useful speculation with the same reservation and latency costs as the baseline.
- **Cheapest first test:** Replay equal-latency streams with truthful, reversed, and uninformative hints; compare no speculation, priced branch precomputation, and exact online repair. Include a wrong hint with a valid but different payload.
- **Old-task retention check:** Check A/C and B₁ while the wrong branch is privately staged, after discard, and after publication of the correct finish.

### Make the two mechanisms compete with their stack

#### 21. Spend an opening that makes two counterweight joins possible
- **Mechanism:** During the opening, transfer old work out of both B₁’s slot and a saturated survivor into a second legal survivor. This frees room for either unsigned pair sum in the first survivor. Shape the signed residual at the shared release address so either of two held-out partners can use that room from the *same* post-B₁ state; the chosen finish pins the shared address.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** The witness merely juxtaposes parent 02 and 05. Claim an interaction only if the common prefix creates executable cross-address joins that the best separately prepared counterweights plus contingent repair cannot match.
- **Cheapest first test:** Cross shaped vs fixed counterweights with common vs separate openings on histories with held-out edges and fresh delayed payloads. Stack the best pair editor with exact online planning and a paid plan cache on each host. Include a null where opening and residual supports are disjoint.
- **Old-task retention check:** Verify the signed release at every affected head and uninterrupted post-spend B₁ on both branches, the timeout, and the refused third branch.

#### 22. Patch the residual contract, not the installed first task
- **Mechanism:** When a new partner arrives outside both advertised finishes, search for a bounded neutral change of survivor and residual *after* B₁. Expose a fresh branch only if the patch plus finish fits the original live budget and preserves all pinned scopes.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Accommodation games](accommodation-games.md) already seeks neutral routes around later demand; the proposed operation substitutes a counterweight continuation in an already-spent opening rather than rebuilding the prefix.
- **Cheapest first test:** Add an unforeseen address with a different signed residual and one legal survivor exchange. Compare patching to exact online replanning, a paid wider initial menu and the stack from 21. Add a case where a new pin blocks every exchange.
- **Old-task retention check:** Prove the patch and finish under A/C including B₁ and the new pin; the infeasible case must preserve the published B₁ and refuse the new branch.

## Ranked deeper questions

1. **Does signed support, rather than address bookkeeping, explain cheaper service on unseen partners?** Start with 01–03 and 06: reverse historical compatibility at fixed marginals, transplant support separately from metadata, and test both held-out edges and entirely new addresses. Require a realized paired-service win under matched singleton costs and A/C. Drop the novelty claim if a lawful rename, fixed template, or paid cache plus exact repair ties.
2. **Can one pre-reveal opening deliver useful B₁ and preserve two incompatible finishes under realistic reader and pin contracts?** Use 11–13 and 17–18. Compare from the same B₁ state, including same-address payload variants, no B₂ and a genuine out-of-menu B₂. If both branches fit simultaneously, or waiting/replay ties on the service frontier without taking B₁ offline, the witness does not establish a new opening resource.
3. **Is their combination more than the best stack of its parts?** Use 21–22: vary whether opening and cancellation share real scarce support, change the late payload without advancing its reveal, and compare to the powered stack on the same shaped host. Count time from B₁ arrival and reject any gain explained by transaction amortization or extra scratch.
4. **Where do the proofs and economics stop transferring?** Use 04, 07, 09–10 and 16. Vary protected readers, precision, incoming shared structure, and publication costs. Track the first verified obstruction or break-even point rather than averaging away rare failures. If each join needs a full proof and exact repair ties, keep only the feasibility observation.

**Verdict:** Keep both score-3 ideas as falsifiable candidates. The smallest worthwhile proposal is a held-out partner crossover that follows the signed support, paired with a delayed-payload witness that keeps B₁ live and has two provably exclusive finishes. Neither algebraic cancellation nor a hand-authored branch table demonstrates learning; if the equal-budget stack ties, report the useful planning or batching restriction, not a new continual-learning primitive.
