# Route-merged fold successors: earning shared state and deleting route exceptions

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Route-merged folds](route-merged-folds.md) ([PR #280](https://github.com/manojbajaj95/cl/pull/280)). **Review seeds:** [Flood triage, row 398](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L398) ([PR #6](https://github.com/manojbajaj95/cl/pull/6)) keeps #280#03 at score 3 (required C work makes route partitions nest) and #280#05 at score 3 (required C work moves routes out of a paid exception block). The inherited route merge and horizon lease are controls, not new seeds.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). No gradient-flow invariant, fitted interference surrogate, save/restore win, or threshold built into a toy. Use actual discrete learner transitions and retention-matched comparisons. **P** marks a candidate reusable operation, not established novelty; **I** marks an improvement or audit. Closest comparisons below are working hypotheses, not claims of exhaustive prior-art search.

## What might be new?

Exact lumpability, finite-state minimization and observability already tell us which histories a fixed set of readers can distinguish. A partial tag is not new as a prefix code. [Witsenhausen's zero-error side-information formulation](https://doi.org/10.1109/TIT.1976.1055607) gives a stronger comparison: a fixed-length single-shot encoder must separate histories that a reader can confuse but must answer differently. The proposed learning operation changes **which distinctions must be stored**, by choosing which already-required, truthfully labeled C batches run before the cut. It must not redefine old-task targets or routes, guess the successor, or shift discarded bits to a route signal. [Guarded Compression of Adam State](https://www.alphaxiv.org/abs/2611.00589) is the nearby optimizer comparison: compress a given state's continuation with an error guard, rather than use required work to alter exact cross-route distinctions before encoding.

## Contract and first gates

- Inherit the [parent contract](route-merged-folds.md#contract). Pin the host, reader programs, lawful C actions and arrival envelopes, arithmetic, horizon, fallback and A/B/C floors. For clarity, A denotes old tasks, B successor service, C the required task that provides candidate pre-fold batches, and r indexes successor routes. Compare equal total required C service with the same information, width-steps, evidence budget and deadlines. Record peak allocation, worst-case serialized bytes (including padding, headers, schema selectors and state readable elsewhere), the price of wide C work, and any refusals or renewal. No free clocks, tags or logs.
- For reachable histories after a C policy, define Pᵣ by exact equality of all declared route-r continuation answers within the horizon, with no additional decoder side information. The tagless partition is the common refinement. A chain is sufficient, not necessary: a single finest route that refines every other one suffices, even if those other routes are incomparable. Report class counts, the gap between the joint and finest single-route log class counts, and the rounded, physically allocated payload separately. A gap can close because the finest route got *more* expensive; that alone buys nothing.
- For a partial tag, specify what is encoded before the route arrives, where any residual lives, and what each reader learns from the actual request. No bit may be fetched from the discarded source. At fixed lawful decoder information, if all histories can reach all routes, the whole immutable payload still has to distinguish every joint class; marking residuals as “only read by exceptions” does not lower that bound. If readers have differing lawful histories or observations, use the confusion graph: an edge joins two histories if a common legal reader observation demands different answers. A proper coloring gives an exact unrestricted fixed-length code; report actual serialization and evidence costs as well. Any proposed win over static coding must come from C changing the edges or the reachable set, not from assuming a free oracle.
- Use an exact no-fold replay for each C policy to check continuation, distinct from task retention against the precommitted floors and matched control stream. Unless a card adds a checkpoint, evaluate held-out A at entry, after each wide C batch, after folding and at the first sensitive read on **every** route, including exceptions. Keep B/C floors and service fixed; use the same late-reader fallback and charge it.
- The **stacked control** receives the same eligible batches and causal information: strongest C prefix selected for one-route quotient shrinking (#269#01), best lawful static tagless/partial/full-tag codecs after that prefix, and the parent indefinite-fold-plus-reset control at expiry. Also give that stack the candidate C order to isolate codec gains from scheduling gains; include route-oracle tagging only as a named information floor when it cannot be implemented causally. Compare independently to unaligned #269#08, partial tagging without C, random eligible order, and equal-byte quantization with measured continuation error. Include a complementary pair no allowed C work can align and an exception C cannot delete.

## Idea cards

### 01. Target the unnecessary route distinction (P; #280#03)
- **Mechanism:** Select a causal prefix that removes pairs separated by a secondary route but still equivalent to a candidate finest route, then fold to the finest route's key only when all such pairs are gone.
- **Novelty vs nearest prior art:** #269#01 buys a smaller single-route quotient; the candidate operation buys a refinement relation even when neither route gets smaller on its own.
- **Cheapest first test:** Enumerate two orders of two ordinary squared-loss C records on a two-slot quantized momentum learner and compute the pair sets exactly. Compare original meet, best single-route prefix, random order and tagged controls; reject a win made only by increasing the finest quotient.
- **Old-task retention check:** Include A examples sensitive to both momentum coordinates; test them at the cut and after each successor head reads.

### 02. Align readers by restricting reachability, not resetting momentum (P)
- **Mechanism:** Look for C transitions that retain multiple distinct momentum vectors but restrict the reachable pairs to a relation on which one reader's answer determines the other.
- **Novelty vs nearest prior art:** Minimal realization finds a quotient of a given system; this would earn a smaller reachable quotient by learning C, without pinning or zeroing an entire read channel.
- **Cheapest first test:** Enumerate states of a two-feature integer regression host after each legal prefix of a fixed C dataset. Compare with a slot reset, a no-fold replay and a C dataset of the same size whose updates leave the state grid complementary.
- **Old-task retention check:** Score A on both original feature directions, including histories that retain nonzero momentum in both slots.

### 03. Buy a finest reader without forcing a chain (P)
- **Mechanism:** Select C to establish a reader that refines every other route simultaneously while allowing the secondary routes to remain mutually incomparable.
- **Novelty vs nearest prior art:** Equality of the meet and an existing finest partition is elementary; the candidate is a C purchase targeted at this weaker certificate instead of pairwise alignment.
- **Cheapest first test:** Use three readers on three small discrete coordinates; retain two incomparable single-coordinate readers and see whether C lets the third reader determine both at lower priced width than a chain-seeking prefix.
- **Old-task retention check:** Run A after both incomparable routes as well as after the carrier route; do not pool away a single failing branch.

### 04. Make one C order fix what the other breaks (P)
- **Mechanism:** Choose between orders of the same required examples by their exact changes to the route partitions; require that reversing the order reverses which refinement holds.
- **Novelty vs nearest prior art:** Curriculum learning and order-dependent SGD already know that order changes weights. The candidate is to use that order dependence to delete a certified cross-route distinction at matched task service, not to forecast forgetting.
- **Cheapest first test:** Enumerate both orders of two overlapping-feature minibatches in fixed-point momentum SGD. Compare random order, loss-first C scheduling and accumulating the two gradients before updating.
- **Old-task retention check:** Check A between the two batches as well as after either order, so an intermediate collapse cannot purchase a cheap cut.

### 05. Learn an alignment that survives the next C suffix (P)
- **Mechanism:** Require a candidate finest reader to determine the other routes' answers under every still-eligible truthful C suffix inside H, not just at the cut.
- **Novelty vs nearest prior art:** Finite-horizon lumpability supplies the verification; the new target is a prefix that earns a smaller quotient closed under unresolved C arrivals, rather than shortening the parent lease.
- **Cheapest first test:** Enumerate a cut and two one-batch suffixes on a two-slot host. Compare the best closure-aware prefix to the cheapest cut-only prefix with a fully charged reset when it fails.
- **Old-task retention check:** Evaluate A after both suffixes, including the one that reopens the cut-only partition.

### 06. Let complementary C batches earn alignment only together (P)
- **Mechanism:** Seek two required batches whose pair of transitions removes the remaining conflicting history pairs even though neither buys an allocatable block by itself.
- **Novelty vs nearest prior art:** #269's work–memory price and [fold-earned headroom](fold-earned-headroom.md) already allow nonlinear refunds. Here the reusable object would be a joint transition eliminating cross-route distinctions, verified against exact singletons rather than a fitted pairwise surrogate.
- **Cheapest first test:** Enumerate baseline, each singleton and both orders on a three-slot host; compare the joint change in unrounded class counts before claiming any gain from allocator thresholds.
- **Old-task retention check:** Run A after each singleton, both intermediate prefixes and both final continuations; no credit for a pair that hides one failing stage.

### 07. Trade a finer finest route for a smaller joint fold (P)
- **Mechanism:** Allow a C prefix to split some classes of the leading route if it removes enough cross-route distinctions to reduce the exact joint payload overall.
- **Novelty vs nearest prior art:** Single-route quotient shrinking would reject the local increase. This would be a retention-safe exchange between intra-route and cross-route distinctions, not mere closing of the refinement gap.
- **Cheapest first test:** Enumerate candidate prefixes on a three-coordinate host with one signed and one sum reader; demand a strict decrease in joint allocation despite a rise in the largest single-route class count. Compare exhaustive codec choice after each control prefix.
- **Old-task retention check:** Check A on histories in the newly split route classes and after the competing reader, not only average drift over the old partition.

### 08. Certify an alignment corridor across unknown arrivals (P)
- **Mechanism:** At each arrival, maintain the set of still-possible refinement certificates; make a wide C choice only if the continuation policy can preserve a priced cut on every allowed arrival path.
- **Novelty vs nearest prior art:** Robust dynamic programming is known; the candidate is a reusable schedule certificate for purchasing the same exact fold without hindsight route or batch ordering.
- **Cheapest first test:** Enumerate a depth-three arrival tree with deadlines; compare to fixed-cut, greedy pair removal and a hindsight oracle. Put an unalignable complementary pair on one branch to test refusal accounting.
- **Old-task retention check:** Run A at the worst arrival leaf, at any delayed cut, and under the declared fallback when that branch cannot align.

### 09. Use C to delete the last route exception (P; #280#05)
- **Mechanism:** Encode a shared key plus paid residual for a disagreeing route. Re-encode without that residual only after C makes every answer for that route a function of the shared key.
- **Novelty vs nearest prior art:** Static prefix or refinement coding already supplies the shared-plus-residual format. The candidate operation is moving a declared route into the shared code by doing real C work.
- **Cheapest first test:** Begin with two agreeing routes and a complementary third; enumerate required C prefixes on a two-slot host. Compare static partial tag, tagless merge, full paid tag, equal-byte quantization and an exception none of the legal prefixes can remove.
- **Old-task retention check:** Re-run A after the former exception first uses the shared key; also test A under both routes already in the shared block.

### 10. Delete only the exceptional fibers that C actually fixes (P)
- **Mechanism:** Within each shared-key fiber, encode only distinctions its exception readers still need. A C prefix may zero the residual on some fibers without moving an entire route into the shared block.
- **Novelty vs nearest prior art:** Conditional coding already gives fiber-wise residuals. The candidate is C work targeted at lowering the **largest** surviving fiber cost after accounting for framing, not reducing the average number of exceptions.
- **Cheapest first test:** Enumerate two candidates with the same number of affected histories: one fixes only small fibers and one fixes the largest. Compare with an exact all-route codec and a static fiber code at the same cut.
- **Old-task retention check:** Check A separately in the largest surviving fiber and in the fibers whose residual was deleted.

### 11. Earn a shared exception residual (P)
- **Mechanism:** If two exception routes still disagree with the base code, use C to make one paid residual answer both routes while leaving their answer functions distinct.
- **Novelty vs nearest prior art:** Multilevel source coding can share refinements from fixed distributions. The proposed move changes the residual confusion problem without needing to move either route into the base block.
- **Cheapest first test:** With one base and two exception routes, enumerate C cuts and compute the exact residual code sizes per fiber for independent and shared exceptions. Compare with an unrestricted joint code and the best static shared residual.
- **Old-task retention check:** Run A after each exception uses the same verified residual, including the history where confusing the two residual decoders would fail A.

### 12. Remove route selection from the carrier (P)
- **Mechanism:** Seek truthful C work after which a fixed decoder can answer two successor operations from the same payload without a separately stored route selector; operation-specific parameters must come from the real request and be charged if not common.
- **Novelty vs nearest prior art:** Prefix codes and normal dispatch already share code paths. The learning claim is elimination of stored selection information, not moving it to an opcode, hidden caller or scheduler.
- **Cheapest first test:** Enumerate two fixed reader programs and both initial route modes; explicitly list every decoder input before and after C. Repeat with the request field masked to detect a shifted tag.
- **Old-task retention check:** Test A on both actual request types, including the route whose branch selector was removed, at matched service.

### 13. Change the confusion graph without changing the route frequencies (P)
- **Mechanism:** Target a C prefix that removes edges between histories with the same lawful reader observation, while keeping the arrival rule and distribution fixed. Encode the resulting graph rather than paying for an oracle route.
- **Novelty vs nearest prior art:** Witsenhausen gives the exact static graph-coloring problem. The candidate is training on mandatory examples to reduce its chromatic number without altering legal observations or relabeling outcomes.
- **Cheapest first test:** Enumerate at most eight histories with two routes and one priced request field; compute exact coloring before and after each prefix. Repeat with the field removed and with a static codec given the identical field.
- **Old-task retention check:** Evaluate A on both ends of every deleted edge before and after C and on the least common route after decoding.

### 14. Make an exception disappear for every legal request variant (P)
- **Mechanism:** Admit a route to the shared block only if its residual vanishes under all legal encodings of its real request, not just the observed batch IDs or the order used to discover alignment.
- **Novelty vs nearest prior art:** Robustness to nuisance inputs is standard; the proposed object is an exception-deletion certificate tied to lawful request equivalence, not a statistical route classifier.
- **Cheapest first test:** Use a reader with two equivalent batch encodings and one genuinely different opcode. Enumerate C policies against all three, and compare to a codec trained only on the usual encoding.
- **Old-task retention check:** Run A after the held-out spelling of the former exception and after the genuine opcode that must still trigger the correct branch.

### 15. Reassign a route without rewriting the entire fold (P)
- **Mechanism:** Choose C and a base key such that moving an exception route into the base leaves existing base codewords valid; reclaim a residual block without moving the shared records.
- **Novelty vs nearest prior art:** Incremental recoding and allocator compaction are known. The proposed learning operation earns backward compatibility through C, rather than paying for a table that translates old keys.
- **Cheapest first test:** In a four- or eight-history model, enumerate base codebooks and lawful C updates; compare stable-key reclamation to a fresh exact joint code, counting peak double-buffer and migration bytes.
- **Old-task retention check:** Test A through both a pre-existing base reference and a newly issued reference, then after the reclaimed block is reused.

### 16. Replace an exception with continuation from a bounded common state (P)
- **Mechanism:** Authorize a predeclared narrow continuation of C using only the shared key and actual new C records; use it to answer an exception that no longer needs its own residual. Prove this factorization before erasure, and count the extra update latency.
- **Novelty vs nearest prior art:** Recompute-versus-store is classical. This would substitute already-required narrow learning for an exception only when the entire future answer factors through the stored key, not resurrect merged-away bits as in post-hoc renewal.
- **Cheapest first test:** Enumerate four merged history pairs, one required narrow C step and two exception readers. Try to find a pair with equal keys and identical legal C input but different exception answers; one such pair kills deletion.
- **Old-task retention check:** Check A while waiting, after the narrow C update and after both exception attempts, including the declared fallback if factorization fails.

### 17. Buy partial sharing before full alignment is affordable (P)
- **Mechanism:** Offer a frontier from paid exceptions to no exceptions at successive cuts; value each C batch by the exact class distinctions and allocatable residual it removes across both parts of the code.
- **Novelty vs nearest prior art:** Work–memory pricing and static layered coding are known. The interaction is a lawful intermediate codec that becomes affordable before either a full tagless fold or a single-route shrink changes usable capacity.
- **Cheapest first test:** Enumerate three C cuts on a three-route fixed-point learner under a posted price and deadline. Compare both seeds separately and stacked, including the candidate order with the best ordinary static codec.
- **Old-task retention check:** Check A after the intermediate cut and after each remaining tagged route; count any retention loss from waiting for full alignment.

### 18. Make alignment and residual deletion prove each other (P)
- **Mechanism:** Use the same exact relation produced by C both to bound the common refinement and to establish which pairs no longer need a residual; reject any deletion not justified by that relation.
- **Novelty vs nearest prior art:** #269 already reuses training work for receipts; the candidate is one cross-route certificate with less evidence than exact separate alignment and tag-elision checks, not amortized replay alone.
- **Cheapest first test:** State all reachable pairs on a six-state host and withhold a C record. Compare shared proof to cached replay plus independent exact checks, pricing replay, proof size and accepted incorrect claims.
- **Old-task retention check:** Independently evaluate A on replayed states at both accepted cuts and on the fallback for the rejected missing-record case.

### 19. Test whether alignment survives finite arithmetic choices (I)
- **Mechanism:** Freeze one deployment arithmetic; compare its exact earned partition to rational arithmetic and nearby fixed precisions without selecting whichever format yields the smallest fold.
- **Novelty vs nearest prior art:** Fixed-point lumpability and the parent's underflow card already exploit collisions. This audit separates C-induced route alignment from accidental rounding or a clock-dependent reset.
- **Cheapest first test:** Enumerate the same admissible two-batch prefixes with rational and two fixed-point formats, including a near-threshold gradient; use equal-byte guarded quantization as the control.
- **Old-task retention check:** Recheck held-out A at the sensitive read in each arithmetic, including the fractional boundary where equality changes.

### 20. Redeem an earned block on a later writer (I)
- **Mechanism:** Run the alignment/tag-elision stack and the strongest control with the same allocator. Credit only a strict reduction in priced width or a later B write that now fits without changing the route or task floors.
- **Novelty vs nearest prior art:** Parent #280#22 and #269#05 already require actual allocator reuse. This is the interaction test: does combining both seeds buy a block neither seed plus its strongest controls buys?
- **Cheapest first test:** Choose the allocation granularity and B request before enumeration. Compare the full 2×2 design (alignment choice on/off, partial codec on/off), plus exact joint codec, with identical C records and budgets; publish ties.
- **Old-task retention check:** Check A after B uses the block and then after the least-common or last remaining exception route; include peak migration and fallback costs rather than hiding them at the cut.

## Ranked deeper questions

1. **Can required C work make the common refinement cheaper before it makes any single route cheaper?** Start with 01, 03, 04 and 07. Need a strict priced and allocator-visible win over the same-budget single-route selector plus best codec, on a host not engineered to zero a slot. If the gap closes only by making one route finer or missing B/C floors, drop the alignment claim.
2. **When can a learner actually delete an exception rather than hide it in the arriving request?** Use 09–13 and 16. Establish the no-side-information floor first, then ask whether lawful C changes a real residual or confusion graph while paying for every decoder input. A tie to static coding on the same post-C states credits C, not the codec.
3. **Do both seeds together buy a point either seed alone cannot buy?** Use 06, 17, 18 and 20. Demand a preregistered width or B-admission gain over the stacked control with the same total C service, certificate budget, horizon and worst A drift. Separate the effect of the C order from conditional coding, and stop if the interaction disappears.
4. **Does the gain withstand unseen lawful arrivals and arithmetic rather than one contrived cut?** Use 05, 08, 14 and 19. Require a positive case and an immovable complementary control at matched retention, with no profitable uncharged exceptions, and honor the same late-reader rule in both.
