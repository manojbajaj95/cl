# Order-free parked replacements

**Status:** Ideas only; no learner runs, implementation, or GPU work. **Parent:** [Glued fragments](glued-fragments.md) ([PR #224](https://github.com/manojbajaj95/cl/pull/224)), especially fixed-width and trained parks (GF12/GF17). **Seed:** [Round 53, GPR2][gpr2], [triage row 347][triage] (score 3; no merge was rated above its strongest part). **Ledger read first:** [Idea ledger][ledger].

## What would count

A park should release an actual training constraint, not provide a second copy of the learner. Establish one public park value and a certified live reader path on existing capacity. Rebatch a fixed, lawfully visible set of truthful examples **once** into equal-size batches with the same sample multiplicities. Without further previews, repacking, deferral, or an order-aware optimizer, let the loader choose any permutation. Every prefix must preserve protected A (normal old tasks) and C (including rare, independently held-out old readers), as well as the declared service for B pieces already advertised. The complete build must satisfy one frozen replacement witness; clear to one public target and check A/B/C again on a held-out continuation.

**State and exposure contract.** Fix the old-reader domain, per-reader floors, B milestones, optimizer law (including slots, clock, normalization and precision), entry/clear language, lawful reads, and continuation horizon before adapting. The overwritten park coordinates agree across admissible histories; other live weights or slots need not agree, but certify them jointly over all aliases. Neither entry nor clear may save, restore or dispatch on a history-specific value. If entry needs teaching, use one public word of ordinary truthful batches at a fixed clock and bill its examples and ticks. The build pool can be repartitioned only when it is lawfully available; no peeking at future shards. A finite correction promise names its actual minibatches and execution class. If an expiring route is used, prove that its opener enables its consumer on the **same** route and before the earliest lawful closure; if that imposes an order on the build batches, the full-permutation claim fails. Handle arrivals, dropped batches or duplicates as separate contracts, not by quietly redefining “any order.”

**A proof handle.** For each set of completed batch IDs U, use a reachable envelope S(U) over the joint serving and optimizer state after the common entry. For every unused batch j, its actual transition must send S(U) into S(U ∪ {j}); certify due reads at S(U) and, if applicable, inside the update. Include all visible B promises, the live park and the next-step wake bound in the envelope. At the full set, every state must pass the same frozen B witness and the public clear/continuation check. Induction covers permutations without equating raw states or assuming commutation. Exact subset search is an oracle, not a scalable novelty claim; sound envelopes may refuse a valid partition. Name whether a refusal is an impossibility over the declared action language or merely unknown.

**Nearest prior art and deciding control.** [Glued fragments](glued-fragments.md) and [covering replies](covering-replies.md) already buy a blind park and a common reply; [preview rebatching][rebatch] already proposes fixed all-order batches; [sealed gates][seal] already covers joint activation/slot closure; [commuting writebacks][commute] already checks reachable diamonds with live reads. [GraB][grab] chooses an order, [OGD][ogd] protects old directions, [Net2Net][net2net] can add function-preserving capacity, and [RCU][rcu]/transactional publication already keep old service live using versions, waiting or isolation. Compare against **the best lawful stack** of independent park + certified rebatch + seal (including joint verification if the control supports it), each part alone, make-before-break with a tuned fixed order, GraB with a live reader guard, and transaction/gradient accumulation under identical exposure. Charge proof generation/checking, samples, updates, wall-clock deadlines, teacher or preview calls, optimizer/donor/shadow bytes, stalls, and reclaim; compare Pareto fronts if not all costs can be matched. A conditional primitive needs a real interaction: co-design cuts a precedence or capacity cost while giving the same old service and useful B, or admits a window that the matched stack cannot. A tie is an improvement at most. In particular, do not count a safety proof as B acquisition or clean commit scores as retention.

## Two paper fixtures (not evidence of a matched-budget win)

### W1. A jointly feasible park and partition, with a no-partition negative

An existing four-scalar learner has state (s,x,y,q) and starts at (1,0,0,0). Entry may set one public s ∈ [0,1], held fixed through the build; clear sets s ← 1. The served scores are A = (1+s)/2 with floor 1/2 and Cₕ = 1+2hs(x−y)−2|q| with floor 0, for both hidden old obligations h ∈ {−1,+1}. The editor never reads h. At s = 0, A = 1/2 and the C path is independently checkable as 1−2|q|; it does not depend on whether the B witness has passed.

Use four labeled records: the linear predictions x+q, x−q, y+q and y−q each have truthful label 1. Each of two size-two batches takes one ordinary mean squared-loss step (half-squared per record, learning rate 1, no momentum). B's frozen witness requires x = y = 1 and q = 0; a delivered same-axis piece can be served once its coordinate reaches 1, and must stay there. No separate copy or correction is allowed.

| Fixed partition | Both orders, before clear | What breaks |
| --- | --- | --- |
| Pair signs within each axis | First step sets just x or y to 1; second sets the other; q stays 0. | Without the park, one Cₕ is −1 after the first step. With the park, both Cₕ are 1 at every build read. |
| Pair axes by like sign | First step sets x = y = 1/2 and q = ±1. | Even parked, both Cₕ are −1 on that read. |
| Pair axes by opposite signs | First step sets x = y = 1/2; second gives x = y = 3/4; q stays 0. | Preserves old reads, misses the frozen B witness in both orders. |

These are all three size-two partitions up to batch relabeling. The first row permits the same clear for both orders (A = Cₕ = 1); it adds no width but does borrow A slack. For the negative, raise A's floor to 7/8, allowing a fixed park only at s ≥ 3/4 (A must also hold at clear). The first row now gives worst Cₕ ≤ −1/2 after one step, and the other rows are unchanged because x = y at their first read. No allowed partition meets the contract. W1 does **not** separate co-design from independent park + rebatch: that stack can find the same construction. A full accumulated step with retuned learning rate 2 can tie the endpoint if permitted, but cannot deliver the first B piece before the second batch is available to its update. Bill that distinction only in a workload that actually needs it.

### W2. Equal weights do not certify an off-training reader

Isolate one nuisance coordinate q and its carried velocity v. A rare protected reader's live score is 1−max(q,0), with floor 1; the build examples use an auxiliary linear read of q, not this ReLU. With ordinary heavy-ball SGD (momentum 1/2, step size 1) and loss (k/2)(q−t)², the update is v′ = v/2+k(t−q), q′ = q+v′. The two aliases start at q = −1/4 and v = +1/2 or −1/2. The two fixed correction batches P and Q have k = 1/2 and truthful targets t = +1/2 and −3/2 respectively. Each quadratic can be a mean over same-size regression records with the stated curvature and target; there is no sign-dependent slot assignment.

Without entry, the positive-velocity alias wakes on P first (q′ = 3/8), but not on Q then P (q = −5/8, −1/4). One fixed entry word, (k,t) = (1,−1), then (3/2,−1), reaches **the same** parked q = −11/8 with v = −5/8 or −1/8, without a reset. The intermediate q is −3/4 or −5/4, so entry itself is safe. Now both permutations are safe on both aliases:

| Build order | q after first (initial +v / −v) | q after second | v after second (both aliases) |
| --- | --- | --- | --- |
| P → Q | −3/4 / −1/2 | −13/16 / −9/16 | −1/16 |
| Q → P | −7/4 / −3/2 | −13/16 / −9/16 | 15/16 |

The end weights agree across orders on each alias, and every build read is safe. Extend the declared horizon by one ordinary correction (k,t) = (1/2,0): Q → P wakes on both aliases (q = 1/16 or 3/16), whereas P → Q stays shut. If the actual continuation were instead the truthful (1/2,−1/2) correction, all four would be safe for that tick, not forever. The admission test must either certify the actual next correction, pay for lawful conditioning before clear, or refuse the larger contract; substituting data to pass is not allowed. W2 isolates slot carry and reader wake, not B acquisition or a complete replacement.

## Idea cards

P = conditional primitive (a proposed reusable object or operation); I = improvement or falsification control. Every test is proposed, uses only a paper or tiny CPU fixture, and inherits the exposure and budget contract above.

### Park entry, live readers, and shared capacity

#### 01. Compile away an order edge by parking the coupling (P)
- **Mechanism:** Find a public reachable park that suppresses the coupling of two useful, mutually interfering B writes to a specific old path, while leaving that path live on the existing carrier. Return one joint park/partition/clear receipt, naming the removed precedence edge.
- **Novelty vs nearest prior art:** GF12 supplies a park and [preview rebatching][rebatch] supplies safe batches; the reusable object is a proof that this park removes an actual dependency for these ordinary updates without renting a carrier.
- **Cheapest first test:** Extend W1 to two admissible parks that decouple different interference modes and two batch pools; compare joint search against a method that selects its park by reader slack before optimizing the partition. Also compare the strongest joint verifier and charge search for both.
- **Old-task retention check:** Probe A and both hidden C signs at entry, before clear, and after an unrelated next update. Match the minimum served A margin, not just feasibility.

#### 02. Borrow a live carrier without reserving a full backup (P)
- **Mechanism:** Temporarily express a retiring reader through an already-serving narrow shared feature plus one public offset. Fit the replacement in the vacated coordinates; prove the borrowed feature can still do its original job and is returned after clear.
- **Novelty vs nearest prior art:** [RCU][rcu] serves old readers on an old version and [Net2Net][net2net] can add capacity. The candidate operation is a charged occupation of an existing live carrier that allows an all-order ordinary build when a full old version will not fit.
- **Cheapest first test:** Use a rank-two shared read head with both channels already in use. Enumerate legal fixed-width encodings versus width-matched projection and make-before-break; remove the shared feature as a necessity ablation.
- **Old-task retention check:** Exercise the transferred reader, the donor's original task and an independent C slice concurrently during the park and on the next edit.

#### 03. Discover a park by trying to learn behind it (P)
- **Mechanism:** Train a maintenance mode against the weakest B progress and old-reader margin across admissible build prefixes, not just a clean park snapshot. Freeze that mode before an unseen B window; require a proof at admission rather than trusting its training loss.
- **Novelty vs nearest prior art:** GF17 proposes pre-training a maintenance park. Here the future legal **partition family** is the causal training target; a policy that merely increases snapshot slack explains no win.
- **Cheapest first test:** Fit tiny two-layer models with equal entry ticks and objective budget: park-margin-only, future-order-only and joint training. On a held-out four- or six-record window compare exact certifiable B gains across all permutations.
- **Old-task retention check:** Match A/C before entry, report their worst prefix after entry, and check both after exit and recurrence; reject a gain bought by poorer normal-mode retention.

#### 04. Seal the update path with a truthful entry word (P)
- **Mechanism:** Search one public sequence of ordinary entry batches whose image lands in a common park with a bounded wake cone on the actual correction multiset. Keep carried slots; certify a nonzero useful correction, not a vacuous seal obtained by freezing the host.
- **Novelty vs nearest prior art:** [Sealed gates][seal] already prove correction closure; the proposed coupled object uses the order-free B build multiset to select an entry word that can be cheaper than a general correction seal.
- **Cheapest first test:** Vary W2's two held-out correction targets and entry-example budget. Compare a multiset-specific word to zeroing momentum, a trained general seal, and freezing the nuisance coordinate with the same useful B pressure.
- **Old-task retention check:** Check the off-training gate and normal A at entry, first arrival and coast; count safe refusal separately from retained A/C plus B acquisition.

#### 05. Park a relation, not an inactive unit (P)
- **Mechanism:** Fix a public relation between two actively used coordinates as the park. Build batches cancel deviations in a conserved old-read combination even though each coordinate moves and remains individually useful to B.
- **Novelty vs nearest prior art:** [OGD][ogd] projects updates and [commuting writebacks][commute] can cancel cross-effects. The candidate is a reachable live relation that ordinary, unprojected batches preserve only under a fixed partition while retaining real B degrees of freedom.
- **Cheapest first test:** Enumerate four records in a two-unit model sharing one normalization statistic. Test the joint relation against freezing either unit, exact output-gradient projection, and independent park plus partition search.
- **Old-task retention check:** Check old outputs that read the combined signal and separate rare probes that read each unit; if only the combined probe is protected, narrow the contract.

#### 06. Make clear consume a successor receipt, not a neutral output (P)
- **Mechanism:** A fixed clear is legal only if every final reachable state satisfies a frozen successor witness and admits the declared post-clear corrections. Synthesize one public, bounded finishing word if slots remain within sight of a wake, rather than choose a history-specific repair.
- **Novelty vs nearest prior art:** Parent park–edit–clear and transactional endpoint checks already gate publication. The extension is a common exit obligation over a permutation-indexed optimizer set that makes the reclaimed capacity immediately reusable.
- **Cheapest first test:** Use W2 with a separate B coordinate, compare endpoint-only clear, matched slot reset, and truthful fixed finish; include an incompatible actual next correction that no allowed finish can cover.
- **Old-task retention check:** Keep the park live during any finish, then score A, off-training C and the installed B on the very next shared update.

### Compile one partition for all orders, including intermediate B service

#### 07. Index the proof by what has been served, not which order got there (I)
- **Mechanism:** Merge prefixes with the same completed IDs into a reachable envelope, but retain branch distinctions when a union creates a spurious slot/weight corner. Record why each discarded distinction is irrelevant to the next batch and clear.
- **Novelty vs nearest prior art:** Subset dynamic programming, abstract reachability and [preview rebatching][rebatch] already motivate universal verification; this only improves a verifier that also carries old and provisional B readers.
- **Cheapest first test:** Exhaust four batches with correlated momentum and replace exact state sets by boxes, relational envelopes and boxes split only on a disagreeing reader. Count proof cost and false refusals against enumeration.
- **Old-task retention check:** Evaluate A/C on every exact prefix, including the rare C reader witnessing the spurious corner; require zero false admissions before claiming a speedup.

#### 08. Publish each B piece as a stable feature before its neighbors arrive (P)
- **Mechanism:** Build batches that each produce an independently usable B feature through shared weights. A certificate says the delivered feature survives every possible remaining batch, not that a completion flag is set.
- **Novelty vs nearest prior art:** Streaming publication and make-before-break can stage independent parts; the proposed receipt permits stable partial publication on the **same** capacity without private copies or requiring compositional independence.
- **Cheapest first test:** Give two consumers real deadlines one tick apart for distinct delivered subtasks. Compare shuffled compiled batches with tuned accumulation, isolated adapters and best fixed-order serving. Remove the early demand as a necessary negative.
- **Old-task retention check:** Run normal A and rare C together with real B reads after every batch; check that either choice of first published B piece leaves the same minimum old-service floors.

#### 09. Pair against the worst reachable curvature, not entry gradients (P)
- **Mechanism:** Exchange records between equal-size batches to cancel a reader-risk statistic jointly with its cross-batch curvature over the park's reachable region, leaving a useful B gradient. Issue the swap only if it repairs a specific worst permutation and does not create another.
- **Novelty vs nearest prior art:** [GraB][grab] reorders and [preview rebatching][rebatch] proposes balancing curvature. The candidate is a conditional swap that uses the changed live coupling at the park, not a generic improvement in gradient discrepancy.
- **Cheapest first test:** Add a quadratic interaction to W1 so one partition balances first derivatives at entry and fails on the second update. Compare gradient balancing, curvature balancing without the park and exact search with the park.
- **Old-task retention check:** Probe C away from the training examples on both first and second reads; separately track ordinary A and all delivered B pieces.

#### 10. Rebatch whole contrast units when examples are not additive (P)
- **Mechanism:** Declare which records must stay together for a truthful objective (contrast sets, normalization groups or coupled preference examples). Repartition intact units at fixed total batch size; certify the real batch loss rather than a sum of fictitious gradients.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] already preserves intact nonadditive units. Test the added claim that parking a real read dependency turns an otherwise infeasible, intact-unit partition into a certifiable replacement.
- **Cheapest first test:** Use six pairwise ranking records with two protected groups and one mixed old-read coupling. Enumerate legal partitions; include an illegal “solution” that splits a pair and changes the objective.
- **Old-task retention check:** Read old rankings using the serving normalization and include a held-out rare pair with the same coupling sign but unlike training data.

#### 11. Certify a deployable precision and batch context (I)
- **Mechanism:** Enclose the actual reduction tree, normalization state, precision and schedule at each prefix. Treat environment contexts outside the envelope as refused, not as extra certified orders.
- **Novelty vs nearest prior art:** Certified arithmetic and [commuting writebacks][commute] already bound rounding. This distinguishes architecture/loader scope from mathematical order freedom without proposing a new arithmetic primitive.
- **Cheapest first test:** Design a balanced batch safe over rationals but unsafe in one deployed float16 reduction. Compare exact accumulation, fixed reproducible reduction and a positive park margin at equal overhead.
- **Old-task retention check:** Assess A and the boundary C reader under every allowed context and order, including clear and a post-clear update; report coverage, not just worst-case error on a narrowed scope.

#### 12. Bind batch freedom to a common executable successor (P)
- **Mechanism:** Accept different final weights if a single public interface, a frozen B witness and the same small set of ordinary follow-up edits all work. If an optimizer slot only looks irrelevant at commit, the next edit must be able to falsify the receipt.
- **Novelty vs nearest prior art:** [Commuting writebacks][commute] already tolerates differences that stay unread. The proposed object is a replacement interface safe to hand to a new trainer without seeing how the loader ordered the build.
- **Cheapest first test:** Construct two endpoints with identical B predictions but different velocity; compare same-weight and same-output certificates against a two-edit continuation certificate. Use W2 as the adjacent failure.
- **Old-task retention check:** After handing off, alternate unseen A/C queries with the same lawful B continuation across endpoints. Any old-task loss voids handoff equivalence.

#### 13. Trade a small amount of A slack for a flat B arrival profile (P)
- **Mechanism:** Search for a park/partition pair maximizing worst-prefix useful B at each required deadline, subject to fixed old floors and a cumulative old-service loss cap. Ordinary batches must transfer the released coupling to progress, not just avoid harm.
- **Novelty vs nearest prior art:** GraB and margin-budget planning can improve worst prefixes; a coupled result needs one park choice to admit a high early B frontier that a park optimized only for retention plus best rebatch cannot reach.
- **Cheapest first test:** Add a third B piece to W1, then sweep A slack and B deadlines with tuned learning rates for every control. Demand a gap at a point where the fixed-order control also has to face lawful exogenous arrival.
- **Old-task retention check:** Match per-read A/C floors and area under the loss curve as well as arrival opportunities; rule out “winning” by making old service uniformly worse for longer.

### Deadlines, interference, and evidence against the merge

#### 14. Prove the opener uses the route that this replacement spends (P)
- **Mechanism:** Perform one public truthful opener before the free-order window. Prove an intervening prefix cannot close its specific route before the consumer's worst lawful position; verify readiness and spend on the same read/write footprint and charge the route once.
- **Novelty vs nearest prior art:** [Route budgets][routes] already binds opener and deadline. The proposed receipt transfers that readiness to arbitrary loader placement without granting extra replay, a second opening or a defended fixed order.
- **Cheapest first test:** Give one three-batch replacement a real opener and one a proxy that improves C without opening the named route. Place the consumer last and include an expiry one tick too early.
- **Old-task retention check:** Read A and the route-dependent rare C before the opener, immediately before the spend and after clear; report C retention even on refusals.

#### 15. Turn “opener before consumer” into a real impossibility witness (I)
- **Mechanism:** If both are distinct members of the free-order pool and a consumer requires prior opening, produce the consumer-first counterexample. Try a lawful unconditional opener before the window or same-batch teaching only if the *ordinary joint update* demonstrably achieves the required effect.
- **Novelty vs nearest prior art:** Operator precedence and [route budgets][routes] already imply the obstruction; the check prevents an all-order claim from inheriting a hidden ordered window.
- **Cheapest first test:** Build a binary-readiness learner with one close and one consume. Repack at unchanged batch size, exhaust all legal partitions, and compare fixed order, real jointly effective batching and a counterfeit concatenation whose simultaneous gradient cannot spend.
- **Old-task retention check:** Check A/C at the consumer-first read even if B is refused or never starts, and test that retries after a missed deadline do not silently spend old service.

#### 16. Preserve loader freedom without buying future access (P)
- **Mechanism:** Issue a partition only when every example it uses is lawfully visible. Precompute a parametric proof over types of records if useful, but instantiate and freeze all membership once before the build. Separate proof cost from actual data waiting time.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] already prices availability. The new candidate is a live park that can absorb the *lawful wait* and still clear with useful new service under a deadline that buffering without parking cannot meet.
- **Cheapest first test:** Replay a staggered four-record arrival trace with the same cutoff and buffers for every arm. Vary one late record across the deadline; compare fixed replay, best lawful stack and a future-peeking positive oracle billed as unavailable.
- **Old-task retention check:** Score A/C from the initial park through every waiting tick, including a late-window refusal and clearing with no B, not only when the batches run.

#### 17. Finish with a reader that straddles the clear (P)
- **Mechanism:** Require a two-stage old call that starts during park to have a public continuation after clear, with a bounded summary carrying only its lawful request state. Reclaim the carrier without stopping it or preserving a full old-version reader.
- **Novelty vs nearest prior art:** [RCU][rcu] waits for prior readers and transactional snapshots pin a version. The candidate is a learned, checkable cross-mode continuation strictly smaller than waiting or storing the needed prior state.
- **Cheapest first test:** Use a two-hop inference call with one dependent query arriving just after clear. Compare waiting, version pinning at charged bytes, and a public continuation. Include a pair of queries that alias under a too-short summary.
- **Old-task retention check:** Compare full A/C responses for calls started before, during and after the park. Test the same calls after every legal B permutation.

#### 18. Reclaim capacity for the next blind build, not for a ceremonial clear (P)
- **Mechanism:** Compose two replacement windows with different parked readers and prove the first release makes the necessary width, slots and deadline available to the second. No renewed backup, undeclared slot reset or margin re-credit is allowed.
- **Novelty vs nearest prior art:** Rolling parks in the parent and [RCU][rcu] already reclaim. The proposed composition rule makes capacity available for a second *independently order-free* learner while the first replacement stays live.
- **Cheapest first test:** Use two small replacement windows and one shared donor feature; compare inverse arrival orders, staying parked, staged copies, and independently re-proved parks with equivalent bytes.
- **Old-task retention check:** Score original A and rare C plus the first installed B during all reads of the second build and after both clears; reject a trade that quietly retires the first B.

#### 19. Certify a different contract for missing or duplicated deliveries (I)
- **Mechanism:** Keep the base contract exact-once; specify a separate finite loss/duplicate policy for pauses, refusal and reclaim. A repeated delivery can be rejected by a charged public ID set; never claim the ordinary optimizer is idempotent unless proved.
- **Novelty vs nearest prior art:** Exactly-once logs and interruptible contracts already cover delivery; this is a guard against promoting a permutation proof into an unproved streaming promise.
- **Cheapest first test:** In W1 drop one axis batch, then duplicate it before the other. Compare deduplication, timeout to safe park, and replay or transaction fallback at equal memory and waiting cost.
- **Old-task retention check:** Keep answering A/C through stalls and duplicates, and reject a fallback whose old-task score survives only by skipping scheduled reads.

#### 20. Return separate entry, build and clear obstructions (I)
- **Mechanism:** Classify exact small-instance failures: no lawful live park, at least one bad prefix in every equal-size partition, or no common frozen witness/clear. A failed relaxed verifier reports unknown, not infeasible.
- **Novelty vs nearest prior art:** Parent GF15 and [preview rebatching][rebatch] already type refusals; this diagnostic checks the full sequence and reveals whether more evidence, a different batch pool or different carrier capacity would help.
- **Cheapest first test:** Use W1's high-floor negative, a mixed-curvature prefix failure and W2 under an incompatible continuation. Add a correlated-slot feasible example a box abstraction wrongly refuses.
- **Old-task retention check:** Verify refusing arms keep A/C live where refusal happens, including a case in which no feasible clear exists and staying parked itself has a deadline.

#### 21. Detect a covert checkpoint by swapping hidden histories (I)
- **Mechanism:** Exchange unobservable pre-park histories at a fixed lawful view. Audit that park value, partition, clear and any compiler trace are the same, and audit resource usage for serialized optimizer slots or per-history donor state.
- **Novelty vs nearest prior art:** Parent GF14 already rejects escrow leaks; this falsifier extends it to batch IDs, proofs, allocator state and recovery paths through a second build.
- **Cheapest first test:** Insert an oracle that selects equal-size partitions by hidden velocity while emitting the same final B metric. Compare a blind compiler with identical activation/slot ranges, and test whether clear actually reconstructs a retired value.
- **Old-task retention check:** Serve A/C before and after swapping histories and through an independent follow-up; do not credit perfect old retention from a hidden rollback.

#### 22. Hunt the crossover where the strongest stack stops tying (I)
- **Mechanism:** Cross live park, partition and truthful entry/seal, then include the best combined control, not just the single-factor arms. Score feasible protected replacements at a fixed wall-clock/service cap and compare Pareto costs.
- **Novelty vs nearest prior art:** This is the ledger's stacked-baseline gate, not an operation. Null cases (already-safe orders, no early service, no shared coupling) should erase any benefit.
- **Cheapest first test:** Exhaust small streams varying shared coupling, slot carry, old slack and delivery deadlines. Include W1 as feasibility only, a no-partition negative, and a retuned accumulation arm.
- **Old-task retention check:** Compare worst-prefix and prequential A/C over the same requested reads, B at clear and continuation, and report refusals, unsupported scopes and stalls independently.

## Ranked deeper questions

1. **Does a coupled park and partition remove a real capacity or precedence cost that the best stack cannot?** Use 01, 02, 08 and 22. Find a case with live old reads and real early B demand where the matched park + rebatch + seal stack, tuned fixed order, and tuned accumulation fail or cost more. Stop if W1-like feasibility is the only gain.
2. **Can one truthful entry word seal the actual optimizer while leaving enough ordinary B updates to matter?** Use 04, 06, 09 and 12. Require a nonvacuous certified correction class and a useful fixed-width replacement under carried momentum or Adam, including an unseen off-training reader and a real post-clear update. A reset or frozen path tying at equal B utility defeats the entry claim.
3. **Can a route-dependent replacement really tolerate last arrival?** Use 14–16. Put the consumer at the latest legal tick; distinguish a proved opener on the same surviving route from a service proxy, an uncharged barrier or a hidden precedence constraint. If no lawful opener survives, withdraw full-order freedom for that pool.
4. **Can released capacity be reused without paying for an old version later?** Use 05, 17, 18 and 21. Demand a straddling reader and a second blind replacement; compare against exact projection, version pinning and fresh verification. Count a gain only if original A/C and the first B stay live at equal backing, scheduling and proof cost.

**Research call:** The first bet is shared-capacity live replacement with real intermediate B demand; audit it against the strongest stack before any pilot. The exact fixtures show a feasible contract and a false-certification mode, not novelty or a budget win.

[gpr2]: https://github.com/manojbajaj95/cl/blob/6495bf986ca24f828f281ca2e429645b452c3ea3/ideas/flood/cross-pool-53.md#L7
[triage]: https://github.com/manojbajaj95/cl/blob/2ae3dc935108edbb954849f7e09d6063e7a9f1ce/reviews/flood-triage.md#L347
[ledger]: https://github.com/manojbajaj95/cl/blob/2ae3dc935108edbb954849f7e09d6063e7a9f1ce/reviews/idea-ledger.md
[rebatch]: https://github.com/manojbajaj95/cl/pull/225
[seal]: https://github.com/manojbajaj95/cl/pull/234
[commute]: https://github.com/manojbajaj95/cl/pull/217
[routes]: https://github.com/manojbajaj95/cl/pull/230
[grab]: https://arxiv.org/abs/2205.10733
[ogd]: https://arxiv.org/abs/1910.07104
[net2net]: https://arxiv.org/abs/1511.05641
[rcu]: https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html
