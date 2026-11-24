# Learned invalidation: can a model learn which facts its cached answers depend on?

**Status:** ideas only; no experiments, probe code, or GPU. **Parents:** [Future edit cost](future-edit-cost.md) ([PR #144](https://github.com/manojbajaj95/cl/pull/144), cards 12 and 16) and [Data-only edit cost](data-only-edit-cost.md) ([PR #147](https://github.com/manojbajaj95/cl/pull/147)). **Review seed:** [`reviews/flood-triage.md`, row 233](https://github.com/manojbajaj95/cl/blob/fc907cc4cfc9e4eb6dc5f50f3d9cff2e5efa575b/reviews/flood-triage.md#L233), which promoted #144#12 (train a cheaper invalidation key) and #144#16 (keep sub-threshold changes).

A model that answers "can a 12-tonne truck take the north bridge for under €20?" without re-deriving the toll every time has, in effect, cached an answer. When the toll moves from €14 to €16, the answer should not change; when it moves on to €21 it should. A build system knows this because it records which inputs each output read. A network does not: it has a dependency structure (its Jacobians), but nobody trained it to be the true one, and nothing in it keeps count of the €2 that did not yet matter. This node asks whether a model can **learn its own dependency graph from data**, sparse and correct, with a per-edge account of how much slack is left, so that a fact change flips exactly its dependents, including the ones that flip only after several small changes add up. If it can, editing becomes "write the fact; the graph does the rest", and forgetting becomes "invalidate along the graph" rather than "hope the gradient finds everything".

## Why this is hard (root cause)

- **Constant facts hide the graph.** If a fact never varied in training, every answer that reads it and every answer that memorized it are observationally identical. A dependency edge is identifiable only from data in which the fact moved while the answer did or did not move (the crossed witnesses of [PR #143](crossed-evidence.md)). With finite crossings, the learned graph is at best the true graph restricted to the crossed region; edges outside it are guesses.
- **An answer is not a record of its slack.** A cached Boolean answer stores which side of a boundary it is on, not how far. Sub-threshold drift (€14→€16) leaves every output unchanged, so output-level editing has no target and the information is simply lost; the €21 change then looks like a €7 jump to a learner that never saw the €16 step, or like a €5 jump to one that did. Sub-threshold correctness therefore needs a stored quantity beyond the answer: a margin measured in units of the fact, per dependency.
- **The model's own graph includes edges the world does not.** Superposition and shared directions give every answer nonzero sensitivity to many unrelated facts ([CLaRE 2603.19297](https://arxiv.org/abs/2603.19297) measures exactly these "entanglement" ripples). Learning a dependency graph means both adding the true edges and *removing* the spurious ones, at fixed capacity.
- **A recorded graph cannot certify that no edge is missing.** [Change-Provenant Supervision 2609.28574](https://arxiv.org/abs/2609.28574) shows lineage-scoped invalidation drops recall when one load-bearing edge is omitted and only independent revalidation catches it. Any learned graph needs a completeness audit, and its cost belongs in the bill.

## What to count, and what would settle it

- **Inherit the parents' contract.** Small CPU world with arbitrary entity IDs, numeric facts (tolls, weight limits, opening hours), and procedures (thresholds, comparisons, sums, exceptions) whose truth comes from an executor outside the learner. Declare the true dependency graph `G*` (which answers read which facts, with each edge's threshold) before training; the learner never sees `G*` except in arms that are explicitly given labels, which are priced. Inherit `(C, D)` from [PR #144](future-edit-cost.md): acquisition, training, revision work (writes, audits, failed attempts, rollback, consumer repair) and serving cost against request-weighted damage, split into exact stale answers, wrong changed answers and wrongly changed unaffected answers.
- **Score the graph, not just the answers.** After each edit report invalidation precision (of the answers that moved, the share in the true dependent set) and recall (of the true dependents whose answer should change, the share that did), separately for answer-changing and sub-threshold edits, and for edges never crossed in training. A host that is cheaper only because it moves everything (recall 1, precision low) or nothing (precision 1, recall low) fails.
- **Make sub-threshold drift a first-class event.** Streams contain runs of small moves that flip nothing, followed by a move that crosses some consumers' boundaries but not others'. Score the crossing step against the cumulative truth, and score every intermediate step on (a) unchanged answers and (b) current direct recall of the fact value. A host that "flips correctly" only because the final value was written directly, ignoring history, is not tracking drift; use arms where the final write is the small last step only.
- **Controls every card must beat.** An explicit build-system cache with the true graph (upper bound, priced in bytes); version-tagged lazy cache (invalidate everything touching an entity); a pure reader that recomputes from facts on every query (no cache, priced in serving); [MEMIT](https://arxiv.org/abs/2210.07229)/[AlphaEdit](https://arxiv.org/abs/2410.02355) proxies with RippleEdits-style propagation; [CODE 2605.28303](https://arxiv.org/abs/2605.28303)-style causal-narrative editing; [MQuAKE](https://arxiv.org/abs/2305.14795)-style retrieve-and-decompose (MeLLo); [GRACE](https://arxiv.org/abs/2211.11031)'s deferral radius for the sub-threshold question; and the parent's plain crossed evidence at equal tokens.
- **Old-task retention in every first test.** A frozen panel of untouched facts, unaffected cached answers, old procedures evaluated closed-book and with oracle premises, and old exceptions, checked after every write and every failed attempt. A graph that is correct for edited facts but erodes untouched skills is a failure.

**Ledger and triage screen.** Read the [idea ledger](https://github.com/manojbajaj95/cl/blob/fc907cc4cfc9e4eb6dc5f50f3d9cff2e5efa575b/reviews/idea-ledger.md) first. Not revived: functional syndromes / coded key→value checks (FALSIFIED: damage is not sparse, PR #24), so no card assumes sparse collateral; MEMIT capacity laws without beating a constant; KAFT as a novel fix; margin effects without margin matching; exact store/replay/restore as discoveries. Neighbours already graded: #144#12 and #144#16 (this node's seeds, kept as controls when a card only renames them), #147#12 reason handoff and #147#7 masked dependence (dependency *types* as data choices), #143#3 shortcut enumeration, top-10 #2 Nerode quotients, #126's label-free detection bridges, ECR10 shared failure drill. Agent-memory invalidation with explicit provenance (PACMI [2610.05732](https://arxiv.org/abs/2610.05732), dependency-tethered memory [2610.25123](https://arxiv.org/abs/2610.25123), invalidation contracts [2609.00243](https://arxiv.org/abs/2609.00243), FinCacheServe [2607.26076](https://arxiv.org/abs/2607.26076)) records dependencies outside the model; every card here asks for dependencies inside the weights and must beat those systems at equal bytes. Knot ([2605.28047](https://arxiv.org/abs/2605.28047)) and CLaRE ([2603.19297](https://arxiv.org/abs/2603.19297)) estimate a fixed model's dependencies; datamodels ([2202.00622](https://arxiv.org/abs/2202.00622), [2610.24721](https://arxiv.org/abs/2610.24721)) map training data to predictions. None of them trains the host so its own dependencies become correct and cheap to read. Prior-art deltas below are scoped hypotheses from abstracts and partial reads, not priority claims.

## Idea cards

### A. Make the dependency graph a learned, readable object

#### 1. Train the Jacobian to be the dependency graph

- **Mechanism:** Add an interchange-intervention loss ([IIT, 2112.00826](https://arxiv.org/abs/2112.00826)) on a designated fact slot: swapping one fact's representation between two inputs must change exactly the answers the executor says depend on it, and leave every other answer fixed. Crossed witnesses supply the positive edges; same-value and wrong-key swaps supply the negative (non-edges). The model's input–output sensitivity becomes `G*` restricted to crossed facts.
- **Novelty vs nearest prior art:** IIT and DAS ([2303.02536](https://arxiv.org/abs/2303.02536)) align a network with a known causal model for interpretability; [Mechanistic Unlearning 2410.12949](https://arxiv.org/abs/2410.12949) localizes before editing. **Candidate primitive:** a host trained so that *non-edges are enforced*, scored by post-edit invalidation precision/recall on a stream, not by alignment accuracy on a fixed model.
- **Cheapest first test:** Toll world with 64 bridges, 4 procedures, 2-layer MLP. Train with and without the swap loss at equal tokens and capacity; edit with one gradient step on the fact slot only. Compare precision/recall to plain crossed evidence, MEMIT-proxy and the true-graph cache.
- **Old-task retention check:** Untouched bridges' answers and the oracle-premise procedure panel after each edit; the swap loss must not lower pre-edit accuracy on rare exceptions.

#### 2. Teach dependency from unlabeled history, not from labels

- **Mechanism:** Train on logged streams in which facts change over time and answers are re-observed afterward (no dependency labels). The only signal is co-change: answers that changed when a fact changed, and answers that did not. A contrastive loss pulls the model's sensitivity toward observed co-change and away from non-co-change. Tests whether ordinary temporal data teaches the graph.
- **Novelty vs nearest prior art:** Time-aware LMs ([2106.15110](https://arxiv.org/abs/2106.15110)) condition on time; [Specialists Learn Faster 2610.13835](https://arxiv.org/abs/2610.13835) shows pretraining organization shapes update speed. **Candidate primitive:** dependency learned from the *diff* between snapshots as the training unit, with the graph scored, not the answers.
- **Cheapest first test:** Same world; give arm A stream diffs only, arm B the same final snapshots without diff structure (equal tokens), arm C explicit edge labels (priced upper bound). Measure graph recall on facts that changed in history versus facts that never changed.
- **Old-task retention check:** Facts that never changed in history must keep their answers through later edits elsewhere; check old procedures with oracle premises.

#### 3. Dependency heads: predict your own invalidation set

- **Mechanism:** A cheap auxiliary head, given a cached query, outputs a set (or sketch) of fact IDs its answer depends on; at edit time, the model scores which answers to refresh by querying the head with the changed fact. The head is trained jointly from crossed witnesses, so its prediction and the trunk's actual sensitivity are tied by a consistency loss (the head must agree with interventions on the trunk).
- **Novelty vs nearest prior art:** Knot ([2605.28047](https://arxiv.org/abs/2605.28047)) learns an external estimator of a fixed QA model's dependence on context units. **Candidate primitive:** the head is part of the host, trained to be faithful to the host's own interventions, and used as the edit router; faithfulness under edits is the test.
- **Cheapest first test:** Compare head-routed refresh (re-derive only predicted dependents) against Knot-style external estimator trained post hoc, CLaRE entanglement neighbours, and the true graph, on held-out facts. Count refresh calls in `C`.
- **Old-task retention check:** Answers the head wrongly omits must be detected by a fixed random audit; report audit-caught misses as damage, not as cost-free.

#### 4. Sparse graph by construction: a fact bus with read receipts

- **Mechanism:** Route every fact read through a narrow bus (a small set of key-addressed slots) with a hard top-k read gate per query. Each cached answer's read set is then literally its dependency set, logged at inference as "read receipts". Training uses ordinary targets; the bus forces the model to declare what it reads.
- **Novelty vs nearest prior art:** Memory layers and product-key memories ([1907.05242](https://arxiv.org/abs/1907.05242)) and sparse memory fine-tuning store facts in addressable slots; [SERAC](https://arxiv.org/abs/2206.06520) routes edits externally. **Candidate primitive:** the read gate as an invalidation index — editing slot *j* invalidates exactly answers whose receipts include *j* — tested for whether receipts are complete (no reads through the residual bypass).
- **Cheapest first test:** Measure receipt completeness: edit slot *j* and count answers that change without *j* in their receipt (bypass leaks). Vary top-k and bus width at fixed parameters; compare to an unconstrained host and the true-graph cache.
- **Old-task retention check:** The bottleneck must not cost old-procedure accuracy; compare old panels at matched parameters and training steps.

#### 5. Hash the dependencies, not the answer

- **Mechanism:** Train the model to emit, for each cached answer, a short code that is a learned function of the *values* of exactly the facts it depends on (a Merkle-like dependency hash). At serve time, recompute the code cheaply from current facts; a mismatch means "stale". Answers whose code is unchanged are served from cache.
- **Novelty vs nearest prior art:** Build systems ([Mokhov et al. 2018](https://dl.acm.org/doi/10.1145/3236774)) and Merkle trees hash declared inputs. **Candidate primitive:** a hash whose input set the network learned; the test is whether the hash is sensitive to dependents and insensitive to non-dependents on uncrossed facts.
- **Cheapest first test:** Train the code head on crossed witnesses; evaluate false-stale and missed-stale rates on held-out edits. Controls: entity-level version tags, a hash over all facts in the query (over-invalidates), the true graph.
- **Old-task retention check:** Cached old answers whose code must not change under unrelated edits; report false-stale on them as wasted cost and missed-stale as damage.

### B. Keep sub-threshold drift

#### 6. Store slack, not answers

- **Mechanism:** For each dependency edge (answer *a*, fact *f*), train the model to report, in units of *f*, how far *f* can move before *a* flips (signed slack). On a small move δ, the model decrements slack instead of changing *a*; it flips *a* when slack crosses zero. This is the minimal extra state the root-cause section says sub-threshold correctness needs.
- **Novelty vs nearest prior art:** [GRACE](https://arxiv.org/abs/2211.11031) keeps a deferral radius in key space around each edit; [Time Sensitive Knowledge Editing 2406.04496](https://arxiv.org/abs/2406.04496) edits time-conditioned recall; #144#16 buys evidence for small moves. **Candidate primitive:** a per-edge slack ledger in the units of the world fact, updated by writes that change no answer.
- **Cheapest first test:** Streams of 3–6 small toll moves then one crossing move; edit only by writing each δ to the fact slot. Compare a slack-trained host to: editing only on answer-changing moves, periodic full re-edit to the latest value, GRACE radius, and a true-graph cache with exact thresholds. Score the crossing step and every intermediate step.
- **Old-task retention check:** Intermediate steps must leave all answers unchanged (including unrelated bridges); rare exceptions with near-zero slack must still flip at the right step.

#### 7. Event-camera edits: write only threshold crossings, carry the residual

- **Mechanism:** Borrow sigma-delta modulation: the editor accumulates sub-threshold residuals per fact outside the weights and issues a weight write only when the accumulated change crosses the smallest slack among that fact's dependents (read from card 6 or the dependency head). Between writes the model is exactly unchanged.
- **Novelty vs nearest prior art:** Event cameras and sigma-delta converters transmit level crossings; lifelong editors (WISE [2405.14768](https://arxiv.org/abs/2405.14768), GRACE) write on every request. **Improvement** unless the model supplies the threshold: the new part is a *model-reported* per-fact crossing level that sets the write schedule.
- **Cheapest first test:** Count weight writes and damage over long drift streams versus write-every-change and write-on-answer-flip. Require equal current direct recall (read from the residual store + model) at each step.
- **Old-task retention check:** Fewer writes should mean less cumulative drift on the old panel; verify that it does, at matched final correctness.

#### 8. Hysteresis-aware caches for oscillating facts

- **Mechanism:** Some facts jitter around a boundary (opening hours ±5 minutes near closing time). Train the dependency edge to carry a band: flip only when drift exceeds the band, and record in the answer that it is "near-boundary" so a rare high-stakes consumer recomputes. Separates cheap stable service from correctness at the edge.
- **Novelty vs nearest prior art:** Selective prediction / abstention under uncertainty; FCR2 hysteresis loops (PR #36) concern curricula, not facts. **Improvement:** a learned per-edge band trades flip churn against stale exposure; must beat a global margin threshold.
- **Cheapest first test:** Jittering-fact streams with two consumers of different stakes; compare learned bands to a fixed global band and to recompute-on-every-change. Score churn, stale exposure and high-stakes errors.
- **Old-task retention check:** Far-from-boundary old answers must not be marked near-boundary (gratuitous recompute counts as cost).

#### 9. Cumulative-drift probes: can the model tell 14→16→21 from 14→21?

- **Mechanism:** A diagnostic that becomes a training signal: ask the model for the fact's change history and for answers under both paths. A host that tracks drift must give the same current answers on both paths and correct history only on the one that occurred. Train on paired paths with matched endpoints.
- **Novelty vs nearest prior art:** [TimeStress 2502.01220](https://arxiv.org/abs/2502.01220) tests temporal consistency of static facts. **Candidate primitive:** path-equivalence as an invariance on edit streams (current state depends only on endpoint; history depends on the path), a property no current editor guarantees.
- **Cheapest first test:** Paired streams with equal endpoints, different paths, same edit budget; measure current-answer divergence between paths (should be zero) and history accuracy. Controls: final-value write, ROME-proxy sequential edits.
- **Old-task retention check:** History queries for untouched facts and old revisions that remain current.

### C. Editing with a learned graph

#### 10. One-write edits that broadcast through the learned graph

- **Mechanism:** If card 1 or 4 holds, an edit is a single write to the fact slot; dependents update through the trunk's now-correct sensitivity, with no consumer repair. Measure the one-write-safe rate from [PR #144](future-edit-cost.md) directly against the dependency-trained host.
- **Novelty vs nearest prior art:** ChainEdit ([2507.08427](https://arxiv.org/abs/2507.08427)) and RippleCoT ([2410.03122](https://arxiv.org/abs/2410.03122)) propagate by generating rules or chains at edit time; MQuAKE's MeLLo decomposes at inference. **Candidate primitive:** propagation paid once at training, so edit time costs one write; the bill must account for the training surcharge.
- **Cheapest first test:** Full `(C, D)` over a 200-event stream: dependency-trained host + one write versus plain host + ChainEdit-style multi-write, versus MeLLo-style decomposition priced in serving.
- **Old-task retention check:** Standard frozen panel after each write; failed propagation is damage on dependents, collateral is damage on non-dependents.

#### 11. Edit the edge, not the fact

- **Mechanism:** Some changes are rule changes (the truck limit now applies to the south bridge too): a dependency edge appears or disappears while all fact values stay put. With a learned graph, an edit can target the edge (add *f* to *a*'s read set) as an operation distinct from a value write.
- **Novelty vs nearest prior art:** #147#4 (membership split) and #147#12 (reason handoff) are data choices for such changes; knowledge editing benchmarks edit values. **Candidate primitive:** an edge-write operator on the host's dependency structure, with its own precision/recall.
- **Cheapest first test:** Rule-change events in the toll world; compare edge writes (intervene on the read gate or IIT slot) with value-level fine-tuning on the changed answers. Score whether *future* value edits to *f* now reach *a*.
- **Old-task retention check:** Other consumers' read sets must be unchanged; check old answers that read *f* through other edges.

#### 12. Version vectors inside the weights

- **Mechanism:** Each fact slot carries a small learned version code bumped by every write; each cached answer carries the version codes it was computed under. An answer is stale when any of its stored codes differs from the slot's current code. A distributed-systems primitive (version vectors) realized as learned vectors so it costs no external store.
- **Novelty vs nearest prior art:** Version vectors and vector clocks are classical; [Positions Are Not Facts 2609.33759](https://arxiv.org/abs/2609.33759) discusses version handling in KV caches. **Candidate primitive** only if the codes live in weights and survive ordinary training; otherwise this is the explicit version-tag control.
- **Cheapest first test:** Compare learned codes to an external version table at equal bytes; measure stale detection after 1, 10, 100 edits and after unrelated fine-tuning.
- **Old-task retention check:** Unrelated fine-tuning must not corrupt codes on untouched facts (false stale = cost, missed stale = damage).

#### 13. Edits that report their own blast radius before committing

- **Mechanism:** Before writing, query the dependency head (card 3) for the predicted invalidation set; run the write on a shadow copy and compare the set of moved answers to the prediction; commit only on agreement, else escalate. Turns the learned graph into an edit-time safety check.
- **Novelty vs nearest prior art:** PreUnlearn ([2606.18473](https://arxiv.org/abs/2606.18473)) audits collateral before unlearning; CLaRE builds preservation sets. **Improvement** on those audits unless the prediction comes from the host itself and is trained to be faithful; then the shadow mismatch is a learned-graph completeness test, the missing piece named by 2609.28574.
- **Cheapest first test:** Inject edits that the host handles well and edits outside the crossed region; measure whether mismatch flags the bad ones better than a random audit of equal size and CLaRE neighbours.
- **Old-task retention check:** Committed edits must have no more old-panel damage than shadow-rejected ones would have had.

### D. Forgetting along the graph

#### 14. Deep unlearning as graph invalidation

- **Mechanism:** To forget fact *f*, invalidate *f* and every answer in its learned dependent closure; derived answers that are still entailed by other facts survive (overdetermination, #147#12). The learned graph supplies the closure that deep unlearning must otherwise search for.
- **Novelty vs nearest prior art:** Deep unlearning ([2410.15153](https://arxiv.org/abs/2410.15153), [2609.34442](https://arxiv.org/abs/2609.34442)) searches and severs knowledge paths in a fixed model. **Candidate primitive:** a host whose paths were trained to be readable, compared on recall of derived facts and on keeping overdetermined ones.
- **Cheapest first test:** Forget 10% of tolls; measure recoverability of each through multi-hop queries (deep-unlearning metric) and retention of overdetermined consequences. Controls: 2609.34442-style search on a plain host, gradient ascent, the true-graph oracle.
- **Old-task retention check:** Non-dependent facts and old procedures with oracle premises must be unaffected.

#### 15. Catastrophic forgetting as unregistered dependence

- **Mechanism:** Reframe interference: when training a new task B moves a fact or feature that old task A silently depends on, A breaks. If A's dependencies are registered (cards 1–4), B's training can be projected away from A's registered read set only, a much smaller protected set than GPM's full activation subspace.
- **Novelty vs nearest prior art:** GPM/OGD protect all of A's input subspace; rented constraints ([PR #145](https://github.com/manojbajaj95/cl/pull/145)) lease directions. **Candidate primitive:** protection scoped by a learned dependency graph, which should keep more B plasticity at equal A retention.
- **Cheapest first test:** Two-task toll world where B rewrites half the facts and A depends on a known quarter; compare graph-scoped protection to GPM, EWC and replay at equal B progress.
- **Old-task retention check:** This card's main metric is A retention; also check C (untouched third task).

#### 16. Forget a dependency, keep the fact

- **Mechanism:** Sometimes the fact is fine but a consumer must stop using it (a policy no longer considers vehicle weight). Remove the edge while keeping direct recall of *f* and every other consumer of *f*. Only possible if edges are separable objects.
- **Novelty vs nearest prior art:** Unlearning that keeps in-context use ([2510.17620](https://arxiv.org/abs/2510.17620)) separates recall from use; this is the converse at the level of one consumer.
- **Cheapest first test:** Edge-removal events; score direct recall of *f*, removed consumer's independence from *f* (intervention test), other consumers' dependence on *f*. Compare edge write (card 11) with fine-tuning the consumer's answers.
- **Old-task retention check:** Other consumers of *f* and the consumer's other dependencies.

### E. Learning the graph cheaply and checking it

#### 17. Active crossing purchase: buy the witness that most reduces graph uncertainty

- **Mechanism:** Maintain an ensemble of candidate graphs consistent with current training; buy the next crossed example where they disagree most about whether an edge exists, weighted by the edge's forecast edit hazard. Graph learning as active causal discovery ([2109.02429](https://arxiv.org/abs/2109.02429)).
- **Novelty vs nearest prior art:** Query-by-committee and active causal structure learning are known; #143#13 already lists QBC as an improvement. **Improvement**, kept as the control every graph-learning card must beat on witness efficiency.
- **Cheapest first test:** Equal witness budget: active versus uniform versus hazard-only purchase; score graph precision/recall and downstream one-write-safe rate.
- **Old-task retention check:** Purchases must not displace rare old exceptions; check them at equal tokens.

#### 18. A completeness certificate for a learned graph

- **Mechanism:** Use the 2609.28574 point head-on: a learned graph can miss edges. Bound missing-edge mass with a randomized audit: perturb random non-edge facts and count answers that move; a Clopper–Pearson bound on that rate is the certificate, and its audit cost enters `C`.
- **Novelty vs nearest prior art:** Statistical testing of software dependencies; ECR8/#145#19 sampled certificates for leases. **Audit, not a method**, but the required gate for any card claiming exact invalidation.
- **Cheapest first test:** Plant known bypass leaks (card 4) at controlled rates; check the bound covers them at the stated level and its cost scales as expected.
- **Old-task retention check:** The audit's perturbations must be on copies; confirm the served model is untouched.

#### 19. Does the graph transfer to facts never crossed?

- **Mechanism:** If the model learns a *schema-level* dependency rule (every route answer reads every bridge on the route), it should produce correct edges for new bridges with no crossings of their own. That is the difference between learning a graph and memorizing edges.
- **Novelty vs nearest prior art:** Compositional generalization (Coverage Principle [2505.20278](https://arxiv.org/abs/2505.20278)) for static answers; #147#21 recipe transfer across schemas. **Candidate primitive:** schema-level dependency generalization measured on edit propagation, not on static accuracy.
- **Cheapest first test:** Hold out 25% of bridges from crossings (they appear only at constant values); edit them later; compare graph recall on held-out versus crossed bridges for each host.
- **Old-task retention check:** Crossed bridges' answers after edits to held-out ones.

#### 20. Cost model: when is learning the graph worth it?

- **Mechanism:** The graph costs training tokens, an auxiliary loss and maybe bytes; it pays back in fewer writes and less collateral. Fit the break-even edit rate per architecture and compare to a pure reader (no cache, pays every query) and an explicit graph (pays bytes).
- **Novelty vs nearest prior art:** #144#17 payback horizon and the parent's rate–revision frontier. **Audit** inheriting #144#7's top-10 #4 test; included because every card here needs the number.
- **Cheapest first test:** On three edit rates and three capacities, compute `(C, D)` fronts for learned graph, explicit graph and reader.
- **Old-task retention check:** Retention floors fixed across all points of the front.

#### 21. Two-level caches: learned graph for frequent facts, reader for the tail

- **Mechanism:** Learn edges only for high-traffic, low-volatility answers; route tail queries through a reader that recomputes from facts. The graph becomes a cache over the reader, sized by the traffic it serves.
- **Novelty vs nearest prior art:** Parent #144#10 hybrid service boundary; FinCacheServe ([2607.26076](https://arxiv.org/abs/2607.26076)) with explicit dependencies. **Improvement** unless the boundary moves on its own as traffic shifts.
- **Cheapest first test:** Shift traffic mid-stream; measure whether the learned graph's coverage follows traffic without retraining, against a fixed boundary and FinCacheServe-style explicit dependencies.
- **Old-task retention check:** Tail answers formerly cached must stay correct after demotion.

#### 22. Self-built dependency graph from the model's own chain of thought

- **Mechanism:** For an LLM, ask the model to derive each cached answer once in a chain of thought, extract the facts it cited, and train it to make its closed-book answer's sensitivity match that cited set (card 1's loss with CoT-derived edges instead of executor labels). The model builds its own graph from its own reasoning.
- **Novelty vs nearest prior art:** [CODE 2605.28303](https://arxiv.org/abs/2605.28303) distills causal narratives into edits; CoT faithfulness work shows cited facts often are not the ones used. **Candidate primitive:** CoT-cited dependencies as self-supervision for closed-book sensitivity, scored on edit propagation and on cases where CoT cites the wrong fact.
- **Cheapest first test:** On Qwen2.5-0.5B (CPU, inference + LoRA small) with a synthetic fact set, compare CoT-derived edges to executor edges and to no graph loss; measure propagation recall after a ROME-proxy edit. This is the one card that needs a small LM; the toy world comes first.
- **Old-task retention check:** General instruction following and untouched-fact recall on a fixed held-out set after the graph loss.

#### 23. Adversarial facts that look independent but are not

- **Mechanism:** Build worlds where a dependency is hidden by masking (#147#7) or cancellation (#147#11): the answer does not move for most crossings but does under one joint condition. Test whether any learned graph recovers those edges, or whether they need an explicit rule.
- **Novelty vs nearest prior art:** #147 lists these as data choices; here they are stress tests for the graph. **Audit.**
- **Cheapest first test:** Measure recall on masked and cancelling edges for every host; report them separately from ordinary edges.
- **Old-task retention check:** The masking premise's other consumers.

## Can models learn their own dependency graph from data, and what would that change?

**What the root cause allows.** A model can learn the graph only where data varied the facts (identifiability), and must be told or trained to drop spurious edges (capacity). Sub-threshold drift needs slack, a quantity no answer-level objective supplies. So the honest claim is narrower than "models learn their dependency graph": with crossed evidence plus a non-edge constraint, a host might learn the graph on the crossed region and on schemas that generalize to new entities (card 19), with a certificate bounding missing edges (card 18).

**What it changes for editing.** Edits stop being per-answer repairs and become one fact write plus a graph read; the bill moves from edit time to training time (cards 10, 20). Sub-threshold drift is kept as slack instead of being lost (cards 6, 7). Rule changes become edge writes, a second edit type (card 11).

**What it changes for forgetting.** Unlearning becomes graph closure (card 14), forgetting one consumer's use of a fact becomes possible without forgetting the fact (card 16), and continual-learning interference can be reframed as unregistered dependence, with protection scoped to what old tasks actually read (card 15).

## Ranked deeper questions

1. **Does a non-edge constraint make a host's own sensitivity match the true dependency graph on held-out edits, at equal tokens and capacity, and does that cut the `(C, D)` bill?** Cards 1, 4 and 10 on the toll world, scored by invalidation precision/recall and one-write-safe rate against plain crossed evidence, MEMIT/ChainEdit propagation and the true-graph cache, with the frozen old panel after every write. If precision rises only by lowering recall, or the bill does not move, the learned graph is not worth its training surcharge.
2. **Can a model keep sub-threshold drift as per-edge slack in fact units, so cumulative small moves flip exactly the consumers whose boundary they cross?** Cards 6, 7 and 9: streams of small moves then one crossing move, written one δ at a time. Must beat edit-on-flip, latest-value re-edit and a GRACE radius; must keep every intermediate answer fixed. A negative result here is informative: it would mean drift must live outside the weights.
3. **Does the learned graph generalize at the schema level to facts never crossed, and can its missing-edge mass be bounded cheaply?** Cards 18, 19 and 23. Without this, the graph is an edge memorization that costs as many witnesses as an explicit table.
4. **Does graph-scoped protection keep more new-task plasticity than subspace protection at equal old-task retention?** Card 15 against GPM, EWC and replay. This connects the node back to forgetting in general: if registered dependence is cheaper to protect than all of A's activations, dependency learning is a continual-learning method, not only an editing one.
5. **Can an LLM build its graph from its own reasoning, and is that graph faithful?** Card 22, after the toy results; CoT-cited facts that are not the facts used would make self-built graphs a liability, which is itself worth knowing.
