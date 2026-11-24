# Future edit cost: can training data make tomorrow’s corrections cheap?

**Status:** ideas only; no experiments, probe code, or GPU. **Parent:** [Crossed evidence, cards 18 and 3](crossed-evidence.md) ([PR #143](https://github.com/manojbajaj95/cl/pull/143)). **Review seed:** [`reviews/flood-triage.md`, row 231](https://github.com/manojbajaj95/cl/blob/dacaef9b6807e0f716d8e3feebb074d03e373e8b/reviews/flood-triage.md#L231).

Can we choose today's training examples so a future change needs one safe write rather than a patch per downstream answer? Crossed evidence can force a model off one shortcut while leaving another intact: when a bridge toll changes, a route planner might stop caching by request but still cache by town and vehicle class. The latter may be the best use of finite capacity if changes are rare and demand is narrow. The test is not whether we can make a learner read every fact. It is whether we can buy the right mix of compiled answers and editable bindings, and come out ahead after paying for training, revisions, damage and serving.

## What to count, and what would settle it

- **Build one unpartitioned world first.** Use small CPU learners on arbitrary entity IDs, finite-valued facts and procedures such as thresholding a toll, comparing two routes and applying an exception. Generate truth from an executor; it is not part of the learned host. Before training declare a bank of witnesses `(q,v0,v1)` for which the answer changes. A selector can buy crossings from the same bank, using a forecast fit only to development histories or public metadata. Match exposures per key, answer counts, and training tokens/steps where compatible; use degree-preserving rewires and report residual mismatches. Edit values, paraphrases, request–world cells and event orders are disjoint from selector fit; hold out keys and entire procedure families in separate transfer tests. Any selector given realized test changes is an oracle, never a valid competitor.
- **Freeze the stream and the service requirements.** Reuse paired sequences with repeat writes, correlated bursts, reversals, never-changed keys, and a regime shift that breaks the training-time forecast. On the first CPU world start with independent changes and then turn on one complication at a time. At each event expose the same current update and public audit budget to every policy; no future values or evaluation labels enter the editor. Probe just before the update and after each allowed attempt, including the state served before a correction passes. Require separate floors for current direct recall, held-out derived answers that should change, and each old-task slice; never reward improving locality by failing to edit. Report one-write-safe rate: one binding update and a fixed audit, no consumer repair, all floors met. Count unmet floors through the next event or a declared deadline; abstaining and dropping a service are not free.
- **Keep a lifecycle ledger.** Report `(C,D)`, not just final accuracy. `C` itemizes upfront example acquisition/selection and training, total revision work (search, writes, validation, failed attempts, rollback, fallback and consumer repair), and serving cost over the same demand trace. Report persistent model, store and editor bytes and peak bytes separately, plus correction latency. `D` integrates request-weighted errors until the next event, splitting exact stale answers, other errors on changed outputs, and errors on unaffected outputs; show peak damage and worst old-task slice too. Report total revision work separately so cheaper inference cannot masquerade as cheaper editing. Compare Pareto fronts and, if ranking is needed, predeclare weights for cost and damage and show when the ranking changes. Account for simulated development edits as selection cost; distinguish them from deployment writes.
- **Keep the old tests old.** Freeze untouched old facts, unaffected requests, exceptions and skills evaluated both closed-book with current bindings and with correct premises supplied. Keep still-current earlier edits in a separate slice. For history tasks retain the old answer only under an explicit old version. Match pre-edit competence, direct-recall efficacy and margins on shared cases, report full-cohort results and matching attrition, and include a no-edit shadow to distinguish editor damage from ordinary drift. A verified binding swap with failed oracle-fed execution is writer damage, not failed reading.
- **Make shortcuts pay rent.** Match host parameters, precision, train compute and initial accuracy; charge alternative caches, routing metadata and editor state to the same persistent byte budget (or show separate Pareto curves when they cannot be matched). Fit request-only, world-only, world×family, a byte-capped low-rank joint table, and a reader and hybrid on the same data. Charge both keys and values, and include procedure cost in the reader budget. For each restricted class estimate minimum training disagreement under the cap (exact for tiny enumerable tables; bounds or achieved fits for larger classes), then report held-out service and revision costs. Do not infer the learned route from that score or from a decodable activation. Calibrate on known cache/reader/hybrid controls and classify an unpartitioned host by novel-binding swaps, orthogonal alias/request interventions, and wrong-key/same-value placebos. Allow mixed or unclassified results. Evaluate rankings across fixed-budget comparisons at several capacities, not a universal threshold.
- **Make the selector, not just the editor, win.** Cross each data policy with a frozen basic editor menu: gradient fine-tuning/replay, [ROME](https://arxiv.org/abs/2202.05262)/[MEMIT](https://arxiv.org/abs/2210.07229) or clearly labeled small-host proxies, and a protected editor such as [AlphaEdit](https://arxiv.org/abs/2410.02355). Compare uniform crossings, frequency and hazard allocation, matched random rewires, [KAFT](https://arxiv.org/abs/2211.05110) at equal examples, and spending the training budget on post-edit replay. Also price bounded exact KV + the same learned executor, learned retrieval, and an oracle executor ceiling. Use [Editable Neural Networks](https://arxiv.org/abs/2004.00345)-style edit-aware loss as an objective-change competitor, not as a data-only arm. Freeze choices on development streams; report paired uncertainty over entire test worlds/streams, not individual correlated requests.

**Ledger screen.** Read the [idea ledger](https://github.com/manojbajaj95/cl/blob/dacaef9b6807e0f716d8e3feebb074d03e373e8b/reviews/idea-ledger.md) first. No revival of KAFT as a novel fix, of cooldown/frequency effects without margin controls, of sparse damage as an assumption, or of a covariance-to-MEMIT-collapse law without beating a constant on a target that varies beyond seed noise. Exact store/retrieval, replay and restore are controls, not discoveries. Teaching dimension and query-by-committee already cover eliminating hypotheses by buying contradictions; cards below need a lifecycle interaction or an independently testable operation beyond those. [Edit-Ready Training](https://arxiv.org/abs/2611.26408) and Editable Neural Networks already train models to accept edits; the primary claim here would be a **data-only** effect under an unchanged learner and editor. Novelty statements are scoped hypotheses, not claims of priority. All cards inherit the ledger and checks above; a CPU test below is a proposal, not a result.

## Idea cards

### A. Decide which evidence to buy

#### 1. Buy the witness bundle that retires a future repair

- **Mechanism:** On development keys, measure how a small bundle of crossings changes the least work needed to meet all service floors. Allocate by that reduction times the forecast number of revisions; leave stable and unreformable keys alone. Buy bundles when no single crossing suffices to retire the repair.
- **Novelty vs nearest prior art:** [GLISTER](https://arxiv.org/abs/2012.10630) selects data for validation performance; [Editable Neural Networks](https://arxiv.org/abs/2004.00345) changes the objective. **Candidate primitive:** an evidence purchase priced by the future safe repair operation it replaces, with loss, architecture and writer fixed.
- **Cheapest first test:** Enumerate purchases of zero, one and two witness pairs per key in a toy; freeze a selector on development streams. Compare with uniform, frequency×hazard, greedy single pairs, equal-example KAFT and buying repair instead. Drop the bundle claim if benefits add or do not transfer.
- **Old-task retention check:** At each event verify untouched facts and independent procedures, including rare ones displaced by the upfront purchases.

#### 2. Buy robustness to a wrong forecast, not simply to frequent change

- **Mechanism:** Allocate crossings to minimize worst-case excess lifecycle cost over a small set of plausible change forecasts. A small reserve of witnesses may cover a family of keys if their consumers share an execution rule; no reserve gets credit without transfer.
- **Novelty vs nearest prior art:** [Group DRO](https://arxiv.org/abs/1911.08731) protects worst-group loss; [GLISTER](https://arxiv.org/abs/2012.10630) uses a validation objective. **Improvement:** use regret over *revision policies* instead of robust static task loss and require a large reduction in worst-stream damage at equal median cost.
- **Cheapest first test:** Train on the same candidate bank under two opposing public hazard forecasts plus uniform allocation. Test a held-out inversion of which keys drift; compare robust allocation with uniform, oracle, and static worst-group accuracy selection.
- **Old-task retention check:** Verify the protected minority's old exceptions and the majority's still-stable facts separately; robustness cannot come from sacrificing either group.

#### 3. Put a price on crossing an edit deadline

- **Mechanism:** Buy evidence for keys whose downstream demand spikes before a repair can finish, not keys with the most total downstream queries. Count actual exposure to stale service while the correction is in progress.
- **Novelty vs nearest prior art:** [WikiBigEdit](https://arxiv.org/abs/2503.05683) measures lifelong degradation. **Improvement:** make time-to-safe-service an upfront data-selection target and require a sizable deadline advantage over simply running the same editor earlier or faster once an update is known.
- **Cheapest first test:** Give two key groups equal update count and total traffic, but delay one group's demand after each event. Freeze the curriculum; reverse timing on held-out streams and compare with magnitude and total-demand allocations and prioritized post-edit repair.
- **Old-task retention check:** Sample unaffected old tasks during the burst, not just after recovery; urgent writes must not borrow safety from services that happen to be idle.

#### 4. Buy the cheapest route out of a cache

- **Mechanism:** For each affordable cache class, find a crossing bundle that raises its cost relative to a reader or hybrid, then spend only if measured revision savings repay that gap. Identical coverage can defeat a request cache while leaving a low-rank joint cache untouched.
- **Novelty vs nearest prior art:** [Shortcut Learning](https://arxiv.org/abs/2004.07780) and teaching dimension explain discrimination. **Candidate primitive:** a capacity-priced displacement test whose output is a predicted replacement route and the resulting revision bill, not an eliminated hypothesis count.
- **Cheapest first test:** Match graph degrees and coverage in two tiny worlds; select bundles against different rivals. Predict route and editor cost before training; compare to raw coverage, teaching counts, random rewires and a development-fitted constant.
- **Old-task retention check:** Include old exceptions uniquely served by the displaced cache as well as old requests on which the two routes agree.

#### 5. Select for portability across writers

- **Mechanism:** Buy crossings with savings across two materially different write mechanisms, rejecting examples that only make a single editor's key geometry favorable. Optimize the savings of the worse writer at matched direct recall, even if both share the same audit.
- **Novelty vs nearest prior art:** [MEND](https://arxiv.org/abs/2110.11309) learns an editor, and [Editable Neural Networks](https://arxiv.org/abs/2004.00345) trains for a prescribed editor. **Improvement:** data selection with an editor-held-out test; a large cross-writer effect would distinguish preparation of the fact representation from overfitting a writer.
- **Cheapest first test:** Select with bounded gradient writes and a rank-one proxy, then evaluate a frozen protected editor held out from selection. Compare to the best single-writer selector and an equal-cost writer-switch baseline.
- **Old-task retention check:** Under each writer track wrong-key neighbors, unaffected served outputs and execution with oracle premises; report failures rather than averaging across writers.

#### 6. Buy indirect evidence only where it substitutes for direct evidence

- **Mechanism:** Buy a crossing in one cheap-to-label consumer as a substitute for expensive crossings in others only if it lowers their *post-write* repair cost. Measure donor-to-recipient substitutions, not read accuracy transfer.
- **Novelty vs nearest prior art:** [RippleEdits](https://arxiv.org/abs/2307.12976) tests downstream effects; the parent already proposes cross-consumer allocation. **Improvement:** price a transfer by how much direct supervision it can replace without increasing repair work, including a negative transfer arm.
- **Cheapest first test:** Use a two-consumer donor/recipient matrix with asymmetric annotation prices; estimate on one pair and predict a disjoint pair. Compare to direct purchase, equal tokens dispersed across both consumers and a replay budget at the same price.
- **Old-task retention check:** Include donor, recipient and unrelated procedures, with rare recipient-only exceptions tested at current and supplied bindings.

### B. Find the shortcut that actually wins at fixed capacity

#### 7. Treat the cache and reader as a rate–revision frontier

- **Mechanism:** Fit constrained caches, readers and hybrids across byte budgets; for each measure how many separately correct answers become stale per newly changed binding and how much it costs to restore them. A cache may win on low fan-out despite worse revision scaling.
- **Novelty vs nearest prior art:** [Knowledge Capacity Scaling Laws](https://arxiv.org/abs/2404.05405) measures knowledge bits per parameter; [Cram Less to Fit More](https://arxiv.org/abs/2604.08519) addresses data pressure. **Candidate primitive:** a rate–revision frontier over representational budgets and update work at matched initial service, not a static capacity estimate or universal cutoff.
- **Cheapest first test:** Enumerate tiny exact tables and low-rank fits, and calibrate causal route probes on known hosts. At three byte caps predict held-out rankings of shortcuts and hybrid placement; compare to static held-out accuracy, compressed table size and a constant ranking.
- **Old-task retention check:** Charge cache eviction of still-current old answers and reader damage to independently learned old procedures as different slices, with equal floors.

#### 8. Find aliases whose collisions make editing more expensive than fitting

- **Mechanism:** Compare training corpora with alias collisions aligned with keys that co-change versus collision groups cut across keys that must change separately. Keep alias count and base accuracy identical where possible; vary joint hazard independently of alias structure.
- **Novelty vs nearest prior art:** [Knowledge Storage and Extraction](https://arxiv.org/abs/2309.14316) studies exposure diversity and extraction. **Improvement:** test whether equal-recall storage layouts have different isolated-write costs because of how *revision boundaries* cross alias groups.
- **Cheapest first test:** Use two equally ambiguous alias graphs and a held-out disambiguator; compare to canonicalization, explicit IDs and a degree-matched permutation. Seek a collision×independent-edit interaction, not merely accuracy loss on ambiguous inputs.
- **Old-task retention check:** Edits to one canonical fact must not change unrelated entities sharing an alias; score disambiguated old paraphrases too.

#### 9. Break the family shortcut without breaking the long tail

- **Mechanism:** Use counterexamples within a high-traffic request family to force a byte-capped world×family table either to split its entries or to share a binding reader. Separately vary rare exception mass so sharing has a measurable cost.
- **Novelty vs nearest prior art:** [Cram Less to Fit More](https://arxiv.org/abs/2604.08519) flattens skew to improve fact recall. **Improvement:** at matched marginal frequencies, predict when a compressed family cache remains the cheapest repair policy and when a reader is cheaper *after* retaining rare exceptions.
- **Cheapest first test:** Cross family-label heterogeneity with exception load. Compare equal-byte family tables, pruned joint tables, shared reader and a frequency-flattened selector. Use within-family new-value swaps to tell splitting from reading.
- **Old-task retention check:** Require separate floors on rare hard overrides and common old requests; show that eliminating a shortcut did not eliminate exceptions it used to serve.

#### 10. Measure whether the hybrid spends its cache on the right facts

- **Mechanism:** Infer which held-out probes are served by a cache or reader after training with forecast-aware witnesses; test whether stable frequent bindings preferentially stay compiled and high-cost volatile ones become read-through. Use both value swaps and interventions on the cached route; admit mixed service.
- **Novelty vs nearest prior art:** [SERAC](https://arxiv.org/abs/2206.06520) explicitly routes edits to a memory-backed counterfactual model. **Improvement:** test whether examples alone can move a service boundary in a fixed host without supplying a router, beating an equally priced explicit hybrid.
- **Cheapest first test:** Swap forecasts for matched fact groups while keeping their prediction tasks unchanged. Compare fitted route shifts with equal-budget explicit hazard routing and budgeted KV, and check held-out future edit bills.
- **Old-task retention check:** Test old stable-but-rare facts and the protected outputs on the boundary, where premature recompilation or stale cache fallback would be missed by an average.

#### 11. Separate query compression from value compression

- **Mechanism:** Match the best rank-capped static fit in two tiny worlds while swapping whether shared low-dimensional structure lives in request rules or in values. Then choose revisions that are either within the old value subspace or outside it, with replacement entropy and jump difficulty controlled.
- **Novelty vs nearest prior art:** [Knowledge Capacity Scaling Laws](https://arxiv.org/abs/2404.05405) considers storage capacity. **Improvement:** distinguish rival low-rank shortcuts by their failure on new value directions, not by the rank of trained weights or a predicted MEMIT collapse point.
- **Cheapest first test:** Synthesize equal-error Boolean grids; compute best budgeted table fits by enumeration and compare their predicted staleness to known readers and a small learned host. Require a held-out revision effect beyond update norm and constant prediction.
- **Old-task retention check:** Check untouched outputs along old directions, old exceptions and oracle-fed rule execution when a new direction is introduced.

#### 12. Test whether a cached answer has a cheaper invalidation key

- **Mechanism:** Train with crossed instances that agree on the answer but differ in which fact would invalidate it. Ask whether those examples help a learned cache generalize a dependency key and cheaply repair on notification, rather than force the model to execute on every query.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tests multi-hop consequences after edits. **Candidate primitive:** a learned invalidation handle assessed on edits to a previously unused branch, not a full dependency graph provided by the teacher.
- **Cheapest first test:** Use alternative paths with identical initial outputs and different mutable edges; compare those crossings with ordinary answer-changing witnesses, equal-cost dependency labels, a lazy cache with explicit version tags and a reader. Charge any audit/refresh required to discover the expired entry.
- **Old-task retention check:** Check cached answers whose answers or versions should *not* change, and verify that the old alternate route still executes when given its premises.

### C. Pay for sequences, not isolated corrections

#### 13. Make the second edit choose the first training example

- **Mechanism:** Allocate crossings using the interaction between edits: does buying evidence for A reduce how much editing B undoes A, or only improve A's first correction? Select on the extra repair work after the second edit relative to single-edit twins.
- **Novelty vs nearest prior art:** [Model Editing at Scale](https://arxiv.org/abs/2401.07453) measures gradual and catastrophic forgetting. **Improvement:** test a data-only cross-key interaction in the revision bill, beyond weighting keys by aggregate single-edit risk.
- **Cheapest first test:** Run no edit, A, B, A→B and B→A on paired worlds with matched direct efficacy; choose evidence on one set of pairs, test new pairs. Compare independently selected evidence, constrained writes and joint batches with equal supervision.
- **Old-task retention check:** Recheck A's still-current value after B, B's before A where appropriate, and unaffected old tasks at every prefix.

#### 14. Save a witness budget for facts whose change rate shifts

- **Mechanism:** Treat hazard as state-dependent. Buy evidence that makes a downstream skill survive when a key moves from stable to volatile *without* spending all budget permanently on the high-hazard class. Estimate the value of one early purchase versus a later allocation from a fixed reserve.
- **Novelty vs nearest prior art:** [History Matters](https://arxiv.org/abs/2312.05497) distinguishes time-dependent answers. **Improvement:** evaluate when optional training evidence should be acquired under changing hazard, not expiry labels or revision scheduling alone.
- **Cheapest first test:** Replay streams with same revision counts and different hazard onset, allowing a budget-matched evidence reserve to all policies. Compare upfront allocation, uniform reserve, reactive replay and a forecast-triggered reserve; include false warnings.
- **Old-task retention check:** Check old stable keys on both sides of the hazard switch and explicitly historical queries; do not erase an old version merely because the current answer changed.

#### 15. Learn an edit-commuting pair from paired-world supervision

- **Mechanism:** Buy joint worlds aimed at removing a *write order* effect, not merely teaching the missing case. With two independent semantic updates, detect whether training makes either edit order reach equivalent served behavior without extra restoration.
- **Novelty vs nearest prior art:** [MEMIT](https://arxiv.org/abs/2210.07229) can install many facts at once; [WikiBigEdit](https://arxiv.org/abs/2503.05683) measures sequential limits; the parent buys missing corners. **Improvement:** require a joint-evidence×write-order interaction beyond joint competence and reduced damage under batched writing.
- **Cheapest first test:** Use a 2×2 training grid, match final joint-query accuracy before editing on a common panel, then compare disjoint new values in both orders. Compare single-key selections, a stacked pair of marginal curricula, batched edits and exact store.
- **Old-task retention check:** Check both edits and unaffected old outputs after each prefix; equality of two damaged endpoints does not qualify.

#### 16. Train for repeated changes smaller than the answer boundary

- **Mechanism:** Buy evidence to keep direct bindings current even when most downstream requests do not yet change, focusing on histories where many small moves eventually change a rare consumer. Test whether a small correction can be stored once instead of being rediscovered at the boundary.
- **Novelty vs nearest prior art:** [Time Sensitive Knowledge Editing](https://arxiv.org/abs/2406.04496) targets time-conditioned recall; parent jump weighting favors large moves. **Improvement:** test whether increment-following evidence reduces cumulative repair under the same terminal jump, not whether a constructed threshold is detectable.
- **Cheapest first test:** Pair a sequence of small changes with a single jump to the same final value at matched served demand; compare selection by immediate answer flips, hazard×distance and evidence straddling eventual crossings. Include a simple late-repair policy and price its stale direct recall.
- **Old-task retention check:** Preserve unchanged outputs on intermediate steps and verify rare prior exceptions even when a formerly irrelevant threshold becomes active.

#### 17. Measure the marginal value of another edit before replacement

- **Mechanism:** Allocate crosses differently for a host expected to be retired after a few changes versus one kept for many. Measure the payback horizon from actual cumulative costs, without using a threshold forecast for editor collapse.
- **Novelty vs nearest prior art:** [WikiBigEdit](https://arxiv.org/abs/2503.05683) measures limits over many revisions. **Improvement:** establish when the break-even reverses against deployment replacement or exact retrieval under equal service, not simply that more training buys more accuracy.
- **Cheapest first test:** On long paired CPU streams score every preregistered horizon and test whether a payback point estimated on development streams holds on new ones. Compare a priced retrain/replacement policy, replay and always-on KV; vary serving volume independently of write count.
- **Old-task retention check:** Evaluate old tasks in early and late prefixes and immediately after replacement; recovery at replacement does not cancel intervening damage.

#### 18. Price stable-looking facts with asymmetric repair obligations

- **Mechanism:** For equally likely changes, select contrasts based on how hard it is to return all affected service to spec in each direction. E.g., a permission becoming invalid may require dropping several cached exceptions, whereas restoring it needs one new answer. Do not assume the asymmetry follows answer frequency.
- **Novelty vs nearest prior art:** [RippleEdits](https://arxiv.org/abs/2307.12976) enumerates dependency effects; [GLISTER](https://arxiv.org/abs/2012.10630) optimizes validation performance. **Improvement:** buy examples using a direction-specific measured repair curve that beats weighting by expected number of flipped answers.
- **Cheapest first test:** Hold degree, change count and answer margins fixed while flipping which direction has downstream redundancy. Compare directional selection with symmetric hazard, magnitude and consumer-count controls on held-out reversals.
- **Old-task retention check:** Test unaffected permissions and exceptions under both directions, including old denials/successes outside the affected scope.

### D. Check what part of a lower bill is real

#### 19. Use training-data counterfactuals to attribute the bill

- **Mechanism:** Train paired twins with and without a matched crossing bundle, then build a per-editor difference in full-stream cost and damage. Swap bundle assignment across keys to see whether savings follow evidence or merely the easy keys.
- **Novelty vs nearest prior art:** [Datamodels](https://arxiv.org/abs/2202.00622) maps example subsets to predictions. **Candidate primitive:** a data-to-revision response measured under interventions on both data and the later update, with signed effects on still-current old tasks.
- **Cheapest first test:** Enumerate a few small one-bundle substitutions; compare finite differences to a loss-based data selector and a constant response. Stop modeling it if repeat-train noise explains as much as the substitutions.
- **Old-task retention check:** Record negative as well as positive effects on retired-cache exceptions and untouched old skilled queries; a paired gain on edited keys cannot substitute for local retention.

#### 20. Measure an evidence dividend after equalized direct correction

- **Mechanism:** Give each model an effective binding write at a matched direct-recall operating point, read out changed-answer propagation, then meter the *additional* consumer repair required. Independently swap a validated activation to estimate propagation under direct value transport, not as a bound on editor performance.
- **Novelty vs nearest prior art:** [MQuAKE](https://arxiv.org/abs/2305.14795) tests composition, and the parent separates readability from editability. **Improvement:** convert their separation into a repair bill and test whether the training advantage survives removing direct-edit efficacy as an explanation.
- **Cheapest first test:** On a paired world use frozen editor budgets and a held-out calibration panel; compare allocation by downstream repair to allocation by direct recall, KAFT, ordinary replay and KV. Report reachability failures and full-cohort costs alongside matched effects.
- **Old-task retention check:** Compare oracle-fed execution before/after each effective write to isolate procedure damage, and untouched old facts to catch a destructive direct-correction control.

#### 21. Audit for delayed stale returns under a cheap correction

- **Mechanism:** After a write passes, serve the same old procedure on varied requests, then apply a permitted unrelated edit or continuation step. Ask whether certain examples buy durability, so one apparently safe write does not secretly lead to recurrent repair.
- **Novelty vs nearest prior art:** [On the Retention of Edited Knowledge](https://arxiv.org/abs/2507.14198) studies regression after fine-tuning. **Improvement:** test a data-only allocation that reduces *repeat repair work* at matched entry efficacy, against spending the same resources on paraphrases or protection after the first edit.
- **Cheapest first test:** Include one unrelated continuation and one no-continuation shadow per stream. Compare targeted crossings, matched paraphrases, freezing, and a bounded retrieval fallback; probe novel continuation families not used by the selector.
- **Old-task retention check:** Verify the continuation task learned, untouched old procedures still execute, and earlier edited facts still live. A blocked continuation is not durability.

#### 22. Stress-test the budget with a flooded repair queue

- **Mechanism:** Choose evidence against a fixed repair-work limit per time window. Evaluate whether it keeps a burst of correlated revisions serviceable, rather than simply making every isolated edit slightly cheaper. Count fallback calls, debt left at each deadline and collateral from aggressive catch-up.
- **Novelty vs nearest prior art:** [Model Editing at Scale](https://arxiv.org/abs/2401.07453) scales sequential edits and [MEMIT](https://arxiv.org/abs/2210.07229) batches writes. **Improvement:** train for a bounded repair queue and require a burst-specific benefit beyond same-bill isolated cost reductions plus optimal batch scheduling.
- **Cheapest first test:** Replay the same changes shuffled versus bursty under identical total editor work; compare a queue-aware curriculum with one ranked by isolated edit savings, batch editing, replay and KV. Allow every arm the same fallback and price it.
- **Old-task retention check:** Audit untouched old services at peak backlog, immediately after catch-up and after the next isolated edit; do not treat delayed probes as proof of safety.

## Ranked deeper questions

1. **Can data-only selection pay down the total safe revision bill at equal capacity?** Start with the tiny enumerated bundle purchase (1), attribute any gain with paired data swaps (19), and retest after equalized direct correction (20). A buy must beat uniform/frequency/hazard, KAFT, matched replay and priced KV on held-out streams at common service floors. If matched cost and damage tie, keep the cheaper/simple policy and the crossed evidence as a diagnostic.
2. **Which shortcut wins, and can its replacement predict the subsequent bill?** Test capacity-priced displacement (4) and the rate–revision frontier (7), using known-host calibration and blind route probes (8–12). Require out-of-sample ranking accuracy beyond static fit, raw coverage, teaching counts and a constant. If behavioral probes do not discriminate a hybrid from a larger cache, report the frontier without assigning a mechanism.
3. **What is the unit to train for: one fact, a pair of updates, or a service burst?** Begin with the paired single/double-edit contrast (13), then matched write orders (15) and queue stress (22). Compare with stacking the strongest marginal curricula and the strongest affordable batch editor; no distinct sequence mechanism is needed if those explain the result.
4. **Do the savings survive getting the future wrong?** Hold out key families, writers and change forecasts (2, 5, 14), then test deferred damage and the payback horizon (17, 21). If savings appear only under oracle forecasts, or disappear when validation/serving costs or delayed damage are counted, bound the useful regime rather than claiming future-proof training.
