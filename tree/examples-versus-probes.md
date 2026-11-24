# Examples versus probes: teaching a learner not to need a measurement

**Status:** Ideas only; no experiments, implementation, or GPU work. **Parent:** [Indistinguishable edit replies](indistinguishable-edits.md) ([PR #173](https://github.com/manojbajaj95/cl/pull/173)). **Review seeds:** [Flood triage, row 275](https://github.com/manojbajaj95/cl/blob/a5e4d368c09f7a3e6108c7a0214c7bb3cecf58c1/reviews/flood-triage.md#L275) kept the parent's **#08** (price truthful teaching against a probe that splits an ambiguous edit group) and **#14** (prefer a safe common first reply that makes the same fixed probe distinguish edits in round two) at score 3. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/a5e4d368c09f7a3e6108c7a0214c7bb3cecf58c1/reviews/idea-ledger.md).

## Is data spent today that replaces a future measurement a new continual-learning object?

**No, not by itself. Conditionally yes if the substitution can be carried, reused, and revoked across edits.** [Iterative machine teaching](https://proceedings.mlr.press/v70/liu17b.html) already selects examples for their effect on a learner; [value of information](https://doi.org/10.1109/TSSC.1966.300074) already prices sensing against acting without it; dual control already takes actions partly for what they let the controller observe later. An exact belief-state planner given the same training actions, transition model, horizon, and costs can represent both score-3 ideas. Renaming its plan is not a discovery.

The candidate CL object is a **revocable record of when a probe can be skipped**: the truthful data or reference to its installed effect; the covered edit families, versions, and transcript classes; the shared reply and its independently checked A/C and new-utility guarantees; any promised later use of the fixed probe; and the failure condition that restores the split probe. It differs from a cache of probe answers: the teaching need not reveal what happened, and a new hidden edit may have an answer that has never been observed. It differs from a one-shot winning policy only if the same record can travel to held-out edit families or survive later learning with cheaper checks than replanning and recertifying. If routine replay, a probe-result cache, and belief-state planning tie it at equal cost, call it an improvement, not a primitive.

### What to price

Freeze the truthful candidate pool and learner update rule, editor payloads and deadlines, reply menus and costs, free transcript, optional probe bank, and independently checked utility and retention floors. Neither the examples nor the first reply may label the realized hidden edit in advance, change the offered demand, or silently expand the probe/reply menu. At an ambiguous transcript, a covered shared reply must work for **every** consistent edit; a splitting probe is worth buying only if each resulting class can be served more cheaply or a previously impossible offer can be served. A refusal pays its lost utility and is not a certified admission.

Keep service outcomes fixed when pricing substitution. For each training choice compare the minimum feasible future paid probes with and without it, across the *same* frozen offers, reply menus, floors, and deadlines. Report the nondominated tuples of examples and training work, optional probes (expected and worst-case), delay, bytes, and verification work. Count fixed scheduled reads too, but do not call moving an optional read to a later round a saving. Quote a break-even price only under declared weights, horizon, and frequency; training is paid even if an edit never arrives. Repeat with held-out editor families and changed training order. For simultaneous changes, use the whole belief history: round-two outcomes must separate **reply-relevant** alternatives over legal continuations, not just the two original edits in isolation or a nuisance variable. Require equal first-round reply cost, immediate service, and safety in the #14 comparison.

**Controls for every card.** Use the relevant combination of probe-only (including adaptive value-of-information sensing), data-only (ordinary replay, [GCR](https://arxiv.org/abs/2111.11210) or [trajectory matching](https://arxiv.org/abs/2203.11932) where applicable), unshaped/myopic common replies, [belief-state safety planning](https://arxiv.org/abs/0706.2619), and the best stack of those parts with a probe-result cache. For #14, include dual control with the same reply and sensing menu; when scope is finite, enumerate the exact joint planner as an oracle, not as a baseline to claim superiority over. Give full observation only to a ceiling arm. Charge certification, retained answers and artifacts, acquisition, fitting, and rechecks; log all offered edits, including refusals. Match initial A/C margins and new-task progress in mechanism comparisons. Keep old A/C checks independent of teaching and probing, report worst rare slices as well as ordinary accuracy, and check every live prefix, including later writes and reversal. Do not count verifier access to hidden state as free sensing: use offline universal proofs, or price information used by an online checker.

### A four-gate paper example that separates the two bets

Let one hidden edit set `b=0` and the other `b=1`. Initially `q=1/8` and `u0=u1=g=0`. Old A has two slices with margins `1−ReLU(d0−q−u0)` and `1−ReLU(d1−q−u1)`, each floored at `1/2`; initially `d0=d1=0`, and the edit sets `(d0,d1)=(1−b,b)`. Old C has margin `1−ReLU(u0+u1−3/4)`, also floored at `1/2`. The two edits install distinct correct new outputs in a private lane not read by the router and untouched by any reply. Edit and first reply are staged; only their verified result serves. All first replies add total `1/2` to the `u` coordinates: a specialist assigns it all to one slice and leaves `g=0`; both common replies add `1/4` to each and differ only in the setting `g∈{0,1}`, at equal cost. The scheduled read `P=ReLU(b+g−1)` is zero for both edits before the first reply; an optional unit-cost split probe reads `b` directly. One unit-cost truthful regression example with target `1/4` brings the shared prediction `q` to `1/4` in one unit step on half-squared error; it contains no edit identity.

- **One round (#08).** Untaught, a common reply leaves the damaged slice at `3/8`; an optional probe plus its specialist reaches `5/8`. Taught, either common reply reaches `1/2` on both edits without the optional probe. No teaching or probe gives no certified policy on both edits. The feasible `(examples, optional reads)` minima are `(1,0)` and `(0,1)`; this shows substitution, not a strict total-cost win at unit prices.
- **Two rounds (#14).** Before the second reply, a frozen continuation adds `1/4` damage to the same slice. Its menu allows another `1/4` on one slice, or a split `1/8` on each. After taught round one the damaged slice needs all `1/4` again. With `g=1`, the **same** scheduled `P` now returns `b`; a specialist brings the margin back to `1/2` in both histories. With `g=0`, a no-split policy cannot serve both histories: the equal split leaves `3/8`, and either specialist fails on one history. In the untaught probe-only arm, cache `b` from round one; its specialist gives `5/8` again after round two. C stays at `1` and neither reply touches the new outputs. Round two is staged as well. If `P` is not already scheduled in round two, charge its read; if legal round-two edits can change `b` or overwrite `g`, redo the calculation on the resulting histories. These planted examples are sanity checks, not evidence of novelty or transfer.

## Idea cards

**P** = conditional primitive candidate: a reusable object or operation with a specific way to fail the gate. **I** = improvement or audit, not a primitive. First tests are paper or small CPU designs, not results.

### Pay for a shared reply instead of a split

#### 01. Transfer a skipped-probe record to a blind editor (P)
- **Mechanism:** Carry the scope, installed teaching effect, shared reply, and recheck predicates to an editor with a different payload but the same verified reply obligation.
- **Novelty vs nearest prior art:** PR #173 #08 prices a single trade; [decision-relevant queries (PR #174)](https://github.com/manojbajaj95/cl/pull/174) carries a justification for buying or reusing information. Here the new editor is served without ever learning its hidden identity. Drop the object if the existing query/repair cache plus routine verification ties.
- **Cheapest first test:** Add a held-out editor pair with different private outputs to the paper case. Price transferring the record versus data replay plus cached split results and fresh belief planning; include a third pair outside scope.
- **Old-task retention check:** Recheck ordinary and rare A/C on the new pair and verify the out-of-scope case never serves without its fallback.

#### 02. Measure marginal prices when the same example serves many classes (I)
- **Mechanism:** Build a joint frontier over classes; amortize teaching once, but charge any probe paid for and reused across several classes once too.
- **Novelty vs nearest prior art:** Set cover and joint value of information already capture shared setup; the measurement is whether CL teaching supplies stronger cross-class economies than joint sensing.
- **Cheapest first test:** Enumerate three ambiguous classes with two overlapping examples and a reusable probe result. Compare per-class exchange rates to the exact frontier; include a case where coordination buys nothing.
- **Old-task retention check:** Verify both A slices and a C slice visited only on the last arrival in each class order.

#### 03. Teach a combination that no singleton can replace (P)
- **Mechanism:** Record minimal teaching bundles whose joint updates make the shared reply admissible, including the required order if updates do not commute.
- **Novelty vs nearest prior art:** [Trajectory matching](https://arxiv.org/abs/2203.11932) optimizes multi-step data effects; a bundle earns the label only if a verified no-split effect transfers without repeating full trajectory search.
- **Cheapest first test:** Enumerate two truthful samples and a decoy in a gated host where neither sample alone saves a probe. Compare greedy scores, trajectory matching with the same pool, and exact bundle search; transfer to a hidden editor pair.
- **Old-task retention check:** Check A/C after each teaching step in both orders, not just after the gate opens.

#### 04. Refinance an expiring substitution (P)
- **Mechanism:** Bind the no-probe promise to quantitative slack. When an unrelated write consumes enough slack, restore just the unpaid probe obligation, or spend a new truthful example to extend the scope.
- **Novelty vs nearest prior art:** [Barrier certificates](https://arxiv.org/abs/1903.11199) track safety and PR #168 tracks return corridors; the candidate is an independently checked change in which observations become necessary while service itself remains safe.
- **Cheapest first test:** Add a drift step that changes `q` but not pre-edit predictions. Compare slack-triggered reinstatement with version-wide invalidation and routine live sensing at equal recheck cost.
- **Old-task retention check:** Test A/C before drift, at the reinstatement boundary, and after the first split-probe fallback.

#### 05. Prove that an expensive probe was never needed (I)
- **Mechanism:** Establish the cheapest unshaped common policy before fitting any data; test whether ordinary B training already makes that same policy feasible by the deadline.
- **Novelty vs nearest prior art:** This is PR #168's free-corridor control applied to the exchange-rate claim, not a new teaching rule.
- **Cheapest first test:** Cross initial `q∈{1/8,1/4}` with ordinary B training that either moves or preserves `q`; estimate substitution both with and without the free-control arm.
- **Old-task retention check:** Match A/C and B in all arms and check both hidden edits at the first time the baseline claims free admission.

#### 06. Bound an irreducible sensing bill (I)
- **Mechanism:** Pair two transcript twins with disjoint verified reply sets for every reachable state under the truthful example pool; witnesses for this disjointness lower-bound required future observations.
- **Novelty vs nearest prior art:** [Footprint counterfeits (PR #107)](https://github.com/manojbajaj95/cl/pull/107) gives indistinguishable states; [conformant planning](https://arxiv.org/abs/1401.3468) already decides common actions. The CL diagnostic quantifies impossibility over reachable teaching states rather than just the current one.
- **Cheapest first test:** Cap truthful updates below `q=1/4` in the paper case. Enumerate all reachable `q`, check the bound, then add the missing example as a negative control.
- **Old-task retention check:** Independently score A/C on both twins, including the case where a reply passes common A examples but fails the rare slice.

#### 07. Buy insurance against a probe outage (I)
- **Mechanism:** Price teaching as an option to serve under a sanctioned missing-probe pattern, not just as a way to lower the expected number of reads.
- **Novelty vs nearest prior art:** Robust experimental design already prices missing measurements; the question is whether data can insure deadline-critical CL edits more cheaply than redundant sensing.
- **Cheapest first test:** Give the optional split probe one predeclared outage slot and compare teaching, a backup probe, and wait/refuse under the same outage and arrival traces.
- **Old-task retention check:** Verify A/C on uninterrupted and outage paths, including the live service immediately before a waiting policy resumes.

### Make a safe reply that leaves a useful measurement

#### 08. Separate what matters, not every hidden edit (I)
- **Mechanism:** Rank equal-cost common replies by the round-two admissible policy their fixed-probe partitions enable, not by edit-identity accuracy or entropy.
- **Novelty vs nearest prior art:** This is decision-focused active sensing ([1809.05504](https://arxiv.org/abs/1809.05504) for downstream objectives); it sharpens PR #173 #14's separation criterion.
- **Cheapest first test:** Split each plant edit into four nuisance variants. Compare a reply revealing the nuisance with one revealing the one bit that chooses the safe specialist; use exact belief planning as the reference.
- **Old-task retention check:** Keep A/C and round-one utility matched; check both specialists on every nuisance variant at round two.

#### 09. Carry a reply's observability guarantee through other writers (P)
- **Mechanism:** Attach a checked promise that all legal intervening writes preserve the fixed probe's decision regions, scoped by their effect on its input and on the next reply obligation.
- **Novelty vs nearest prior art:** Dual control plans through a dynamics model; [HJ reachability](https://arxiv.org/abs/1709.07523) verifies reachable sets. The candidate is a recheckable interface that a later author can use without reconstructing the originating edit policy.
- **Cheapest first test:** Add two intervening writer families: one changes a nuisance coordinate, one toggles `g`. Compare local rechecks with whole-history belief replanning and a fixed countdown lease.
- **Old-task retention check:** Test A/C and round-one edit retention after each writer and after the round-two specialist or restored split probe.

#### 10. Don't mistake separation in isolation for separation after continuation (I)
- **Mechanism:** Choose a revealing reply only if each round-two transcript class over legal continuations still has a common reply. A pair that separates before round two may collide once unknown edits arrive.
- **Novelty vs nearest prior art:** [Imperfect-information games](https://arxiv.org/abs/0706.2619) track exactly these enlarged beliefs; this is a guard against a misleading proxy for dual control.
- **Cheapest first test:** Allow a legal offset to the fixed probe's preactivation and plant two histories with the same final read but different obligations. Compare isolated-pair ranking and joint belief enumeration.
- **Old-task retention check:** Check A/C after the offset and after the actual common or fallback reply on both colliding histories.

#### 11. Demand a separation margin, not a one-bit coincidence (I)
- **Mechanism:** Prefer the common reply with a positive gap between decision regions under declared measurement noise; abstain or buy a separate read in overlap.
- **Novelty vs nearest prior art:** Robust filtering and [barrier certificates](https://arxiv.org/abs/1903.11199) already use uncertainty margins; here the margin is on a future choice, not on the sensor's raw signal alone.
- **Cheapest first test:** Give equal-cost common replies different probe gaps, add bounded read noise and quantization, and compare raw gap, exact robust partition, and repeated reading.
- **Old-task retention check:** Match first-round A/C margins, then test the extreme noise values and all routed second replies on withheld A/C.

#### 12. Reveal an optimizer branch without reading optimizer state (P)
- **Mechanism:** Select a common reply whose lawful update makes hidden momentum differences visible on the fixed behavioral probe only when the next required reply depends on them.
- **Novelty vs nearest prior art:** [Momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) motivates latent state; dual control already excites latent dynamics. A candidate operation is a transferable, checked conversion from a hidden training-state distinction to a later behavioral observation at no extra query.
- **Cheapest first test:** Use two quadratic learners with identical weights and different momentum. Enumerate equal-cost repairs and frozen next edits; compare direct optimizer read, standard active excitation and behavior-only repair.
- **Old-task retention check:** Match A/C accuracy before the repair and check margins after it and after the momentum-driven step; reject if either reply makes a previously safe old slice fail.

#### 13. Keep the fixed-probe transition safe through rollback (P)
- **Mechanism:** Roll back the reveal claim along with the reply that enabled it. Preserve cheap proof fragments for unaffected histories and reinstate sensing obligations for the rest.
- **Novelty vs nearest prior art:** Transactional checkpoints restore state and [counterexample-guided safety repair](https://arxiv.org/abs/2106.01917) invalidates unsafe claims. The candidate is rollback of an observation guarantee with local, independently checked reuse rather than global recertification.
- **Cheapest first test:** Undo a reveal gate across two paths, one with an independently purchased split result. Compare replaying previous observation history, global recertification, and dependency-aware restoration of the obligation.
- **Old-task retention check:** Check C immediately on rollback, A on both resumed states, and previous new-task retention on any reversed edit that was still promised.

#### 14. Prevent a revealing reply from becoming a new task side channel (I)
- **Mechanism:** Restrict fixed-probe outcomes to the information needed to route round two; count and reject any protocol in which the reply receives hidden identity through a verifier, label, or private task lane.
- **Novelty vs nearest prior art:** Information-constrained control and standard leakage audits anticipate this; it is a fairness check on apparent teaching or control wins.
- **Cheapest first test:** Permute hidden edit names and new-output encodings while preserving allowed probe and reply semantics. Run a deliberately leaky router as a positive control.
- **Old-task retention check:** Check A/C after both rounds under every permutation; successful classification of a leaked name is not retention or admission.

### Combine, compose, and stress the substitution

#### 15. Teach the safe gateway to a later reveal (P)
- **Mechanism:** Select today's examples to enable a common reply that is both safe now and revealing later, rather than any common reply. Neither intervention alone need remove the optional probe over two rounds.
- **Novelty vs nearest prior art:** PR #173 #08 and #14 are the parts; exact joint dual control can represent their interaction. The candidate is a gateway guarantee that stays valid and cheaper to check on new editors, not the fact that a joint solver wins a planted toy.
- **Cheapest first test:** Give a myopic equal-cost tie-break the closed gate in the four-gate case. Factor teaching versus no teaching and myopic versus revealing reply; compare the best composed stack and joint oracle, then change both private outputs and one legal continuation for held-out tests.
- **Old-task retention check:** Match A/C and served utility in round one between taught replies; report both rounds, including where held-out C invalidates the reveal.

#### 16. Take on measurement debt only with a repayment deadline (I)
- **Mechanism:** Bound the number of edits that can remain unresolved and the deadline by which a fixed scheduled read must make a needed distinction. Prepay a split probe if that promise is infeasible.
- **Novelty vs nearest prior art:** Contingent planning with deadlines already handles delayed sensing; this distinguishes eliminating a read from postponing a necessary one.
- **Cheapest first test:** Shift the second demand before or after the scheduled read and compare exact finite-horizon planning, earliest-split, and deadline-aware fallback at equal delay prices.
- **Old-task retention check:** Measure A/C throughout the unresolved window and after repayment, including an old task that cannot wait for verification.

#### 17. Compose two records without a falsely shared reply (P)
- **Mechanism:** Join no-probe certificates only when the same reply covers their union and passed prefixes commute under both scopes; otherwise keep them separate or buy a query.
- **Novelty vs nearest prior art:** Assume–guarantee checks and [imperfect-information games](https://arxiv.org/abs/0706.2619) already compose contracts and intersect safe menus. New only if verified local records can reduce certificate work versus joint synthesis without concealing cross-writer interactions.
- **Cheapest first test:** Use a four-cell product of two editor families, with a shared optimizer slot making the fourth cell fail. Compare local composition, fresh exact planning, and an unsafe marginal-stacking control.
- **Old-task retention check:** Check ordinary A/C and the cross-family C slice in all legal joint cells and both writer orders before granting coverage.

#### 18. Trade storage for future sensing without assuming a free cache (P)
- **Mechanism:** Evict raw examples or split results only when the installed teaching effect, its proof, and a priced fallback preserve future service within memory and latency caps.
- **Novelty vs nearest prior art:** [GCR](https://arxiv.org/abs/2111.11210) chooses replay contents; standard caching trades space and reacquisition. The candidate is an auditable conversion from an evicted learning artifact to a bounded future sensing obligation, including an explicit way to revalidate it.
- **Cheapest first test:** Stream alternating known and blind editor families through a two-slot store. Compare replay plus LRU probe cache, always re-probe, and retained scope records with reacquisition priced.
- **Old-task retention check:** Test A/C after eviction and after the first cold return, including a rare A slice that needs the evicted replay data for ordinary retention.

#### 19. Sell the cost saving only if it repeats (I)
- **Mechanism:** Separately report upfront teaching cost, recurring proof cost, and the distribution of probe savings over repeats and nonarrivals. Do not amortize across offers that were never served.
- **Novelty vs nearest prior art:** This is lifecycle value-of-information accounting, not a new learning operation.
- **Cheapest first test:** Cycle horizons `1,2,4` with repeated, independent, and canceled offers; compare teacher break-even with a cache that can reuse exactly the same split results.
- **Old-task retention check:** Score A/C even on canceled-offer streams, where paying for teaching could degrade old tasks without any service gain.

#### 20. Find the smallest truthful training change that buys a decision (I)
- **Mechanism:** Search only the example changes that can cross a common-reply or later-separation boundary; use candidate gradients to prioritize, never to certify.
- **Novelty vs nearest prior art:** [Iterative machine teaching](https://proceedings.mlr.press/v70/liu17b.html) selects examples to steer a learner, and GCR selects gradient coresets. The improvement is predicting a probe-replacement boundary rather than immediate loss or raw update size.
- **Cheapest first test:** Compare one-step surrogates, matched-margin replay, gradient coreset selection, and exact enumeration of eight truthful examples on four gates; add an activation flip where the linear prediction fails.
- **Old-task retention check:** Verify ordinary and rare A/C independently for the selected teaching step and after both branches; reject a prediction that trades C for a saved read.

#### 21. Compile the record through a model change, or withdraw it (P)
- **Mechanism:** Relate old and new host states by their reply guarantees and fixed-probe decision regions, without requiring identical hidden coordinates or carrying every parent example.
- **Novelty vs nearest prior art:** Simulation relations already preserve policies under abstraction, and PR #168 covers return corridors. The proposed reusable artifact transports a conditional right to skip sensing through a learner revision, not just a safe endpoint.
- **Cheapest first test:** Reparameterize one gate in a small host, then add a non-equivalent gate. Compare scope translation with copying the old policy, replaying all data, and fully solving the new belief game.
- **Old-task retention check:** Evaluate A/C just after migration, after both rounds, and across the first fallback; verify a function-matched migration can still fail later retention or observability.

#### 22. Separate a missing proof from a real need to measure (I)
- **Mechanism:** Maintain two frontiers: what is feasible in the fully enumerated simulator and what a bounded verifier can establish. Count their gap as a proof cost, not evidence that the hidden state intrinsically needed sensing.
- **Novelty vs nearest prior art:** Verification-guided refinement ([SpecRepair](https://arxiv.org/abs/2106.01917)) already handles inconclusive checks. The audit prevents claiming a CL substitution when teaching merely makes a chosen checker less conservative.
- **Cheapest first test:** Give a coarse verifier a spurious interval corner; compare its frontier with enumeration and with refinement plus no extra data at equal work.
- **Old-task retention check:** After restoring a rejected shared reply, verify each old A/C slice with independent exact checks on all transcript twins at each served prefix.

## Ranked deeper questions

1. **When do today's truthful examples actually beat buying a future split?** Find a strict held-out Pareto gain at matched certified admission, old-task floors, and new utility over the best replay + active sensing + cache stack, after charging every check and delay. Start with cards 01, 02, 05, 06, and 19. A unit-cost tie or a gain limited to planted pairs is not enough.
2. **Can the first safe reply change what the *same* later probe lets the learner do?** Use cards 08–12 and 15 to test decision-relevant separation across all legal continuations, holding first-round cost, utility, and A/C fixed. If the gain is only more mutual information or disappears under a second legal writer, keep it as a dual-control audit.
3. **What can be checked locally when a no-probe promise is carried to a new editor or host?** Use cards 04, 09, 13, 17, and 21 to compare partial rechecks to fresh planning and recertification. If invalidation always widens to the full history, the record is a log, not a transferable CL primitive.
4. **Where are the hard limits of replacing sensing with learning?** Use cards 03, 06, 11, 16, and 22 to separate irreducible ambiguity from weak teaching pools, lawful continuations that erase the reveal, deadlines, and weak verification. A useful answer identifies which extra example, lawful probe, or proof would change the conclusion without relaxing retention.
