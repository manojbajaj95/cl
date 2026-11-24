# Slack erosion: can an answer start forgetting before it gets anything wrong?

**Status:** ideas only; no experiments, probe code, or GPU. **Parent:** [Stored slack](stored-slack.md) ([PR #151](https://github.com/manojbajaj95/cl/pull/151)), cards 12 and 14. **Review seed:** [flood-triage row 243](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/flood-triage.md#L243), the two score-3 directions: hidden forgetting at perfect accuracy, and reclaiming precision according to what dependent answers actually need. **Screen:** [idea ledger](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/idea-ledger.md).

Yesterday a €14 toll could rise by €6 before an old route answer stopped saying “yes.” After training on an unrelated task, the answer still says “yes” at €14, but now it takes only a €2 increase to flip it. Nothing has been forgotten on the ordinary test set. Has the learner nevertheless lost a measurable part of what it knew? Conversely, if every dependent answer can tolerate a known amount of error in the stored toll, can we spend the unneeded precision on a new task?

## Why this is hard (root cause)

- **Accuracy observes a point; slack probes the boundary around it.** Keep the true fact fixed during unrelated training. On an initially correct old query, measure how far a *declared, valid intervention on the fact* must move before the served answer changes. Record the positive and negative directions separately; in a multi-fact case record a safe region, not a sum of edge radii. Erosion is the difference from install time, not the fact's movement. Fix semantics, units and intervention protocol before training. Compare across procedures on the same fact scale or under a fixed, shared distribution of feasible moves, not by averaging euros and minutes. No observed crossing within a capped sweep is censored, not infinite slack.
- **More slack can be worse.** When the true toll crosses €20, the answer *should* change. A fossil that always says “yes” has large apparent slack but fails the procedure. Record the oracle boundary alongside the learned one: score both premature flips and missed legitimate flips. Validate interventions through known readers or slot substitution, not merely a prompt that restates the answer. In nonlinear cases a local zero derivative is neither an infinite radius nor proof that the fact is unused.
- **There are two forecast targets.** `T_update` is the first incorrect answer at the unchanged fact under a held-out continuation of B training. `T_move` is the first failure against the correct answer under a declared fact-move process in a fork. A flip that tracks a changed oracle is not forgetting. Slack from fact interventions might predict `T_move` but not `T_update`; compare each separately, using only observations available before the forecast. A candidate law is that recent erosion adds calibrated first-passage information over current margin **and** current slack, with the future update or move distribution declared. It is not the identity “distance divided by speed,” and it need not be monotone.
- **A precision budget is an intersection of obligations.** A candidate stored value is safe only if *every* registered consumer still meets its tolerance, including direct recall, and the true fact and procedure still agree at the reference point. For frozen scalar consumers and symmetric rounding with step `q`, `q/2 < minᵢ sᵢ` is a sufficient worst-case rule when `sᵢ` is consumer i's smaller directional slack; ties need an explicit boundary convention. With joint errors, use the joint feasible region. With drifting readers, intersect the safe sets over the declared horizon or reserve part of the budget for that drift. Exact recall of a discrete fact requires preserving its exact value, not just its answer class. Reducing numerical precision frees nothing unless bytes, rank or slots are actually recovered and used by B.

## Two gates before calling either a law

**Precursor gate.** Use A (old facts and procedures), B (unrelated labels, potentially shared parameters), and C (untouched skills). Start from matched A-correct checkpoints; verify A is still 100% correct at the forecast landmarks and report coverage without conditioning on future survival. Include exact linear readers as a tying control, then a nonlinear reader with exceptions and an ordinary tiny shared MLP, where the geometry is not planted. Freeze forecast windows, intervention limits and evaluation panels. Compare with a constant hazard or time guess, forgetting-event counts ([1812.05159](https://arxiv.org/abs/1812.05159)), current margin and its slope (after margin matching), gradient norm, directional first-order response ([2609.32818](https://arxiv.org/abs/2609.32818)), current computed slack `m/|∂m/∂f|` on a scalar edge, a matched-query recompute, and a rate–drift predictor based on projected decoder drift or measured message rate. Report held-out, censor-aware calibration and lead time at the same false-alarm rate; hold out streams, seeds and procedures. First establish that target variation between conditions exceeds repeated-seed variation and that there are enough events; otherwise stop at the constant baseline. The ledger's killed “forecast before update” matters here: good local response fit is not evidence that the approximation holds out to the first error. The stability gap ([2205.13452](https://arxiv.org/abs/2205.13452)) is an actual transient accuracy drop, not the correct-at-every-landmark regime here; count both rather than mistaking one for the other.

**Budget gate.** [Top-10 #4 / PR #105](https://github.com/manojbajaj95/cl/pull/105) prices a fixed description decoded with a drifting learner as side information: for exact zero-error intent, the trajectory-union confusion graph requires at least `ceil(log₂ χ(∪ₜ Gₜ))` fixed-length bits. Slack asks a different operational question: what distortions to an already installed slot can we spend while its consumers keep working? These quantities need not track each other. With a frozen reader and a single known install intent, the description needs no distinguishing bits, yet changing the consumer threshold can make the safe rounding interval arbitrarily narrow or wide. Conversely, adding a future state that distinguishes two previously conflated edit intents adds a graph edge without changing today's installed slot or its slack. Neither example proves a new coding law: if a representation must satisfy the same consumer tolerances across the same receiver states, the budget can be the feasible distortion set of a generalized rate–distortion problem with decoder side information ([0901.1705](https://arxiv.org/abs/0901.1705)), and exact consumer outputs can themselves define the intent. Test for an independently useful *allocation rule*, not universal novelty: cross consumer tolerance with decoder drift; compare an actual rate–drift allocation and a combined allocation at equal bytes, permissible observations and A/C retention. Match direct recall and traffic in all arms. If the generalized allocator ties, call slack a useful input to it, not a new primitive.

**Common bill for the cards.** Tests below are proposals for enumeration or CPU-scale learners, not findings. Compare at the same persistent and peak bytes, audit queries, permitted lookahead and B training budget where applicable. Charge dependency maps, residuals, backups, metadata, recomputes and side information. Whenever a card stores a slack estimate, pit it against on-demand computed slack and an equal-byte external slack table; a table that ties can validate the measurement but not in-model storage. In allocation tests, include uniform bits, Fisher/Hessian mixed precision ([1911.03852](https://arxiv.org/abs/1911.03852)), traffic-weighted rate–distortion, and adaptive weight decay (FADE, [2604.27063](https://arxiv.org/abs/2604.27063)) with storage actually recovered. Report B gain at matched A/C retention, and A/C loss at matched B gain; include an ordinary no-compression reference. Ledger screen: don't revive margin-gated visibility (MX2), sparse coded detection of diffuse damage (PR #24), or the parent's slack-over-rate expiry as a new law.

## Idea cards

### A. What erodes while the answer stays correct?

#### 1. Margin-matched boundary histories

- **Mechanism:** Use the recent history of fact-space boundary displacement to forecast failures from checkpoints with the same current margin and fact radius. A changing reader may carry a different hazard than one that always had this radius.
- **Novelty vs nearest prior art:** Forgetting events ([1812.05159](https://arxiv.org/abs/1812.05159)) count observed mistakes; first-order response ([2609.32818](https://arxiv.org/abs/2609.32818)) predicts logit displacement. **Candidate primitive:** a boundary-history state only if it adds information beyond both levels and slopes.
- **Cheapest first test:** A tiny shared MLP fits toll thresholds and exceptions; train B on disjoint labels. At margin- and radius-matched landmarks, compare the last three boundary probes with margin history and a constant at equal queries, forecasting both targets on held-out suffixes.
- **Old-task retention check:** Verify the full A panel is right at landmarks; report later ordinary A failures, premature/missed counterfactual flips and untouched C.

#### 2. Cross-procedure slack as a common forecast unit

- **Mechanism:** Match the distribution of physical moves seen by a threshold rule, a two-leg route and an exception rule. Predict failures from probability mass between learned and oracle boundaries rather than compare incomparable logits.
- **Novelty vs nearest prior art:** Certified radii ([1902.02918](https://arxiv.org/abs/1902.02918)) guarantee local invariance, not transfer of a forgetting forecast between different readers. **Candidate primitive** only if a calibration learned on some procedures transfers to a new one.
- **Cheapest first test:** Fit on two toy reader families and hold out a third. Rescale their logits as a negative control, and compare to normalized margin, computed slack and direct stress-test failure rates at the same probe count.
- **Old-task retention check:** Check each reader on the old fact and on both sides of its true decision boundary; report C separately.

#### 3. Boundary curvature as an early warning

- **Mechanism:** Measure first-crossing distances at two scales; a near branch switch can move the exact boundary while local `m/|∂m/∂f|` hardly changes.
- **Novelty vs nearest prior art:** [2609.32818](https://arxiv.org/abs/2609.32818) shows why extrapolating strong local response fits fails. **Improvement:** test whether measured departure from linearity, rather than a better logit extrapolation, forecasts the next old error.
- **Cheapest first test:** Fit a small piecewise nonlinear reader, with a linear sibling as a tying control. Equalize fact queries across two-scale bracketing, a local quadratic response fit and repeated first-order recomputes.
- **Old-task retention check:** Report old answers and old exception accuracy, including counterfactuals beyond the fitted local region.

#### 4. A rotating weak direction

- **Mechanism:** Track which combinations of fact moves first cause an error. The minimum radius may stay flat while its shortest direction rotates into a common future move.
- **Novelty vs nearest prior art:** Certified robustness ([1902.02918](https://arxiv.org/abs/1902.02918)) prices a norm ball; NTK overlap ([2010.04003](https://arxiv.org/abs/2010.04003)) measures task alignment in update space. **Candidate primitive:** an orientation forecast in consumer fact space rather than a scalar radius.
- **Cheapest first test:** Two-dimensional toll-plus-delay readers under shared-feature B training. Compare directional probes to a minimum radius, Jacobian projected on the same move covariance and a uniform stress grid at equal probes.
- **Old-task retention check:** Keep old single-fact readers and the joint reader correct at the reference facts; evaluate rare move directions separately.

#### 5. Slack recovery without answer relearning

- **Mechanism:** Apply two orders of matched B minibatches that erode and then restore a boundary while all old-answer labels stay withheld. Recovery distinguishes a reversible loss of robustness from durable impairment.
- **Novelty vs nearest prior art:** The stability gap ([2205.13452](https://arxiv.org/abs/2205.13452)) detects overt recovery; [2207.04543](https://arxiv.org/abs/2207.04543) studies accumulation visible when tasks recur. **Improvement:** test for recovery visible before any overt mistake or recurrence.
- **Cheapest first test:** Enumerate short opposite-order runs in a shared MLP, with the same batches and update count. Compare recovery to shuffled order, margin recovery and drift projected onto old responses.
- **Old-task retention check:** Inspect A after each update, not just at endpoints; verify apparent recovery with new counterfactuals and untouched C.

#### 6. Fact–procedure crossover diagnosis

- **Mechanism:** Swap old and new fact slots and readers in a 2×2 diagnostic. A shrunken boundary might follow the slot, the reader or their interaction even with perfect served A answers.
- **Novelty vs nearest prior art:** Edit-durability studies ([2511.05852](https://arxiv.org/abs/2511.05852)) measure surviving edits. **Improvement:** isolate which component moved the boundary *before* the edit visibly fails, without assuming a redundant code.
- **Cheapest first test:** Use a separable table and small reader; compare crossover to fact-only and reader-only audits under the same number of evaluations. First use exact slot and reader perturbations as attribution checks.
- **Old-task retention check:** Score unmodified A and C separately from swapped forks, plus direct recall and oracle-boundary fidelity for each fork.

#### 7. A two-clock first-passage forecast

- **Mechanism:** Model future fact shocks and future reader updates separately; allow one clock to accelerate the other by moving the boundary before the next shock. Forecast ordinary forgetting and shock-exposed fragility separately.
- **Novelty vs nearest prior art:** First-passage margin bounds ([2609.32818](https://arxiv.org/abs/2609.32818)) model fine-tuning response. **Candidate primitive** only if the coupling adds out-of-stream forecast skill, not just two independent risks or parent card 11's slack/rate timer.
- **Cheapest first test:** Cross intermittent fact-move schedules with short B streams; predeclare both horizons. Compare to additive independent hazards, slack divided by speed and the strongest same-probe response forecast.
- **Old-task retention check:** Log failures at the unchanged fact and under moved facts separately, with expected oracle changes excluded and C scored on the ordinary stream.

#### 8. Matched damage, different slack

- **Mechanism:** Fork from the same checkpoint and select equal-B-loss updates with matched logit margins but different effects on A's boundary. Use a shared suffix to ask whether boundary damage is causally relevant, not just correlated with harder streams.
- **Novelty vs nearest prior art:** GEM ([1706.08840](https://arxiv.org/abs/1706.08840)) constrains losses on old examples. **Improvement:** a discriminating intervention holding nominal losses fixed, not a claim that a new one-sided penalty is novel.
- **Cheapest first test:** Enumerate balanced minibatch choices for a two-layer reader. Compare against same-size matched forks selected by directional gradient norm and a margin slope.
- **Old-task retention check:** Both forks must keep nominal A and C right at selection; report actual A failure and B progress after the identical suffix.

#### 9. The rare exception leads the mean

- **Mechanism:** Track erosion on sentinel consumers that share a slot but differ in exception paths. Test whether the cross-consumer tail matters more than the mean, without assuming all damage concentrates on a sparse set.
- **Novelty vs nearest prior art:** Interference-ranked replay ([1908.04742](https://arxiv.org/abs/1908.04742)) ranks by expected loss increase. **Improvement:** choose diagnostic sentinels by which boundary facets they cover, not by expected utility for replay.
- **Cheapest first test:** Many toll consumers with a few exceptions. Hold out queries from each path and compare facet coverage to random, margin-ranked and interference-ranked probes at equal audit count.
- **Old-task retention check:** Report ordinary A accuracy, worst-path A accuracy and C; a tail signal that tracks rare paths only on the audit set fails.

#### 10. When shrinking slack is good

- **Mechanism:** Treat boundary movement toward the oracle as repair, even if it reduces a raw radius. Test whether the excess or deficit of learned slack relative to oracle slack is a better early warning than radius shrinkage itself.
- **Novelty vs nearest prior art:** Randomized smoothing ([1902.02918](https://arxiv.org/abs/1902.02918)) measures invariance, not whether that invariance encodes a stale decision. **Improvement:** make oracle movement tests a falsifier for a seemingly strong retention score.
- **Cheapest first test:** Mix fossilizing, correctly reading and overly reactive toy readers. Compare signed oracle discrepancy, raw slack and direct counterfactual error sampling at the same query and label budget.
- **Old-task retention check:** Check old nominal decisions and the required switch after a legitimate move; report untouched C to rule out improvement bought with collateral damage.

### B. What can a learner safely give up?

#### 11. Asymmetric storage cells

- **Mechanism:** Round into a shifted, nonuniform codebook whose cells fit both directional tolerance limits. A consumer near only one boundary may leave unused room on the other side.
- **Novelty vs nearest prior art:** HAWQ-V2 ([1911.03852](https://arxiv.org/abs/1911.03852)) uses curvature for precision allocation. **Improvement** unless consumer-aligned cells beat a distortion-matched allocator with the same codebook freedom; asymmetric quantization itself is not new.
- **Cheapest first test:** Enumerate scalar fact bins with one tight side and heterogeneous consumers. Compare symmetric slack, uniform rounding and traffic-weighted nonuniform quantization, charging the boundaries.
- **Old-task retention check:** A decisions, boundary fidelity and direct recall must stay within their separate tolerances; assign the saved packed bits to B and score C.

#### 12. Spend a joint budget, not independent radii

- **Mechanism:** Encode facts together along directions of permissible joint error; the same total slot error can be harmless if it cancels across consumers and harmful if it aligns.
- **Novelty vs nearest prior art:** Task-vector quantization ([2503.06921](https://arxiv.org/abs/2503.06921)) and the parent's escrow formulation already motivate correlated errors. **Candidate primitive:** a reusable safe error set passed from readers to an allocator, only if joint rate–distortion does not tie.
- **Cheapest first test:** Enumerate pairs of bridge tolls under sum and difference consumers. Compare vector quantization aligned to feasible sets with per-edge minima and full joint task-distortion vector quantization at equal bytes.
- **Old-task retention check:** Test both joint and single-fact A queries, including direct recall and rare co-moves; verify old C and actual B uptake.

#### 13. Rank on demand from the binding consumers

- **Mechanism:** Give a shared slot the smallest rank that satisfies old readers; return unused rank to B rather than preserve every old feature direction.
- **Novelty vs nearest prior art:** NTK overlap/PCA projected gradients ([2010.04003](https://arxiv.org/abs/2010.04003)) exploit low-dimensional task geometry. **Improvement:** choose rank by tolerable consumer error rather than energy retained, not by inventing a new projector.
- **Cheapest first test:** Enumerate low-rank memory matrices for two toy skills. Compare slack-constrained rank, SVD energy and Hessian-weighted reconstruction at equal parameter and optimizer-state bytes.
- **Old-task retention check:** A must retain minority readers poorly represented by high-energy components; check exact-recall consumers and C when B fills the reclaimed rank.

#### 14. Merge slots only while their obligations intersect

- **Mechanism:** Two facts with different values can share one prototype if their safe reconstruction sets overlap; split them when a new consumer makes the intersection empty.
- **Novelty vs nearest prior art:** Multi-decoder rate–distortion ([0901.1705](https://arxiv.org/abs/0901.1705)) already permits many tolerated reconstructions. **Candidate primitive:** an online, consumer-auditable merge/split contract, only if it earns its metadata relative to reclustering or a rate–drift codec.
- **Cheapest first test:** Stream a dozen discrete slots and newly registered readers; compare online intersection merges, weighted k-means and an exhaustive finite-codebook optimizer, including split costs.
- **Old-task retention check:** Run all existing A readers before and after each merge and split, preserve distinct exact-recall values where required, and check C after B uses the freed slots.

#### 15. Separate accuracy spend from drift reserve

- **Mechanism:** Reserve a portion of each safe interval for future reader drift; spend only the remainder on present compression. The rule rejects a cheap codec that leaves a correct but fragile A panel.
- **Novelty vs nearest prior art:** Rate–drift ([PR #105](https://github.com/manojbajaj95/cl/pull/105)) and multi-decoder rate–distortion ([0901.1705](https://arxiv.org/abs/0901.1705)) already price future state changes. **Candidate primitive** only if an explicit consumer reserve transfers better or can be maintained more cheaply than the full trajectory allocation under the same access.
- **Cheapest first test:** Enumerate frozen and drifting threshold schedules crossed with loose and tight recall tolerances. Compare slack-only, drift-only, split reserve and full horizon distortion allocation with equal information, bytes and recodes.
- **Old-task retention check:** Score A and direct recall immediately and after held-out drift, with C untouched; reject “reclaimed” capacity if B cannot use it without increasing failure rates.

#### 16. Precision debt when a consumer arrives late

- **Mechanism:** A new reader may demand more precision than an old slot retains. Track an explicit obligation to acquire or retain a residual, rather than silently assuming deleted bits can be recovered.
- **Novelty vs nearest prior art:** Rate–distortion with decoder side information ([0901.1705](https://arxiv.org/abs/0901.1705)) permits supplementary bits. **Improvement:** bill reinstating precision as maintenance in an online CL stream; split logic alone cannot recover a deleted discriminator.
- **Cheapest first test:** Start with loose consumers, then add a tight one. Compare base-plus-priced residuals, keeping high precision from day one and reacquiring from a charged fact source; include a no-source case where exact recovery is impossible.
- **Old-task retention check:** Score old A and C before and after the upgrade, old direct recall throughout, and B gain net of capacity paid back.

#### 17. Trade slack only through verified equivalent procedures

- **Mechanism:** Route an answer through a different procedure that uses a lower-precision fact but is equivalent on a declared domain. Release the old fact bits only if that equivalence includes exceptions.
- **Novelty vs nearest prior art:** Backward-compatible representation training ([2003.11942](https://arxiv.org/abs/2003.11942)) preserves compatibility across versions. **Candidate primitive:** exchanging storage precision for an alternate reader with a checked consumer contract, not merely retraining for compatibility.
- **Cheapest first test:** Enumerate route rules with algebraically redundant facts and explicit exceptions. Compare retaining exact slots, approximate distillation and equivalent substitution at equal storage and execution cost.
- **Old-task retention check:** Exhaustively check old route branches in the finite domain, retain any direct-recall slot bits, and check held-out C when B spends the released bytes.

#### 18. Guarantees for rare readers, averages for the rest

- **Mechanism:** Use hard lower bounds on precision for designated consumers and traffic-weighted distortion for others. Test whether slack reveals low-traffic consumers that need many bits despite contributing little average loss.
- **Novelty vs nearest prior art:** Multi-decoder rate–distortion ([0901.1705](https://arxiv.org/abs/0901.1705)) can already express different distortion constraints. **Improvement:** a practical allocation comparison against a constrained rate–distortion control, not a new optimum in disguise.
- **Cheapest first test:** Enumerate a small popularity-skewed route panel. Compare hard-plus-soft slack with traffic-only and constrained per-reader distortion at equal bits and the same consumer declarations.
- **Old-task retention check:** Report per-reader violations as well as traffic-weighted A, direct recall and C; never average away loss of a protected reader.

#### 19. Pay to refresh the weakest tolerance

- **Mechanism:** Refresh slack measurements only where uncertainty changes a real bit-allocation decision; when the estimate is stale, fall back to a conservative bound rather than assume the initial tolerance persists.
- **Novelty vs nearest prior art:** FADE ([2604.27063](https://arxiv.org/abs/2604.27063)) adapts forgetting rates online. **Improvement:** choose where to audit by the value of the resulting precision decision, not simply by sensitivity or age.
- **Cheapest first test:** Stream heterogeneous reader drift and cap fact interventions. Compare decision-driven refresh to periodic, smallest-radius-first and exact oracle refresh priced in queries.
- **Old-task retention check:** Count false-safe compression on A and needless bit retention separately, and report direct recall, C and net B gain after paying for audits.

### C. Where the two objects should come apart

#### 20. Same coding rate, different failure times

- **Mechanism:** Hold the future exact-intent confusion graph fixed while moving an installed consumer boundary inside each exact-output class. Test whether the next error time moves even though the rate does not.
- **Novelty vs nearest prior art:** The trajectory-union rate in [PR #105](https://github.com/manojbajaj95/cl/pull/105) is a coding converse; multi-decoder coding ([0901.1705](https://arxiv.org/abs/0901.1705)) does not imply a hazard at a fixed code size. **Candidate primitive** only if the separation is predictive in a learned reader, not just true by construction in a table.
- **Cheapest first test:** Enumerate fixed-graph toy pairs as a sanity check; then train small readers and look for matched-rate and matched-margin pairs under held-out continuations. Compare slack with projected drift, response and constant hazards at equal observations.
- **Old-task retention check:** Confirm that the installed A answer and intent decoding are correct at landmarks, then score A after the common suffix, plus untouched C.

#### 21. Same slack, different coding rates

- **Mechanism:** Hold today's installed safe sets fixed while varying which future receiver states distinguish currently merged intents. Short-run safety can then be identical even when the side information needed for future decoding differs.
- **Novelty vs nearest prior art:** Uncertain side-information delay ([1109.1293](https://arxiv.org/abs/1109.1293)) and the rate–drift law already handle changing decoder views. **Improvement:** use the reverse separation to audit when slack-only allocation fails, not as another proof of the coding bound.
- **Cheapest first test:** Enumerate tiny future receiver tables with matched present safe sets. Compare stored exact intents, slack-only slots and a joint codec at equal bits; distinguish action accuracy from successful future reapplication.
- **Old-task retention check:** Report installed A survival, exact-intent decode and reapplication separately; verify recall and unaffected C before reporting any B gain.

#### 22. The extra coordinate test

- **Mechanism:** Give a fixed-capacity allocator two coordinates per fact: the allowed consumer distortion and the estimated future side-information bill. Ablate each coordinate and ask whether the joint allocator chooses a different, better use for the last byte.
- **Novelty vs nearest prior art:** A generalized multi-decoder distortion objective ([0901.1705](https://arxiv.org/abs/0901.1705)) can absorb both. **Candidate primitive** only as a reusable online allocation interface if it beats the strongest matched-info, matched-compute generalized baseline in held-out streams, not just either coordinate alone.
- **Cheapest first test:** Enumerate a small fixed-byte knapsack of facts, then check whether policies learned on one tolerance × drift grid transfer to another. Include computed-slack-plus-rate, traffic-plus-rate and a full finite oracle as controls; charge all policy metadata.
- **Old-task retention check:** Spend the final byte on B and trace the A/C retention frontier, including exact recall and later reapplication. If no frontier shifts, there is no usable capacity gain.

## Deeper questions, ranked

1. **Does erosion add calibrated lead time before the first actual old-task mistake?** Start with cards 1 and 7. On held-out, margin-matched streams with perfect A at forecast time, beat current computed slack, response and rate–drift with a fixed false-alarm budget. If only fact-move fragility becomes predictable, call it a stress diagnostic, not a general forgetting law.
2. **Does spending consumer slack move the retention–plasticity frontier beyond a drift-rate allocator?** Cross tolerance with decoder drift (cards 15 and 22), include direct recall as a consumer, and require actual B uptake at fixed A/C retention. If generalized rate–distortion ties, keep the engineering rule and drop the new-object claim.
3. **When does the consumer geometry force a joint budget rather than per-fact prices?** Find the cheapest joint contract that catches correlated errors, rotating weak directions and binding exceptions without giving back the savings in audits and metadata (cards 4, 12 and 19).
4. **What remains of reclaimed capacity once demand can change?** Distinguish safely deleting redundant precision from borrowing precision that a future consumer will demand back. Price backups, acquisition and splits, especially where recovery is impossible without a new source (cards 14, 16 and 21).
