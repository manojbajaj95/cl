# Forgetting cycles between versions: did the skill disappear, or did its route close?

**Status:** Ideas only; no experiments run. **Branch:** continual learning → evaluation under change → [past selves as adversaries (PR #135)](https://github.com/manojbajaj95/cl/pull/135) → forgetting cycles.

## What a cycle would and would not tell us

The [flood triage (rows 219–220)](https://github.com/manojbajaj95/cl/blob/2310552dd3f4b7e094e61dc70445b9974c530de2/reviews/flood-triage.md#L219-L220) singled out two cards from the parent: #13 asks whether several versions can each expose a different verified regression; #7 gives the failing model an ancestor-proposed observation and checks whether it recovers. The cross-pool LA2 already crosses access paths to diagnose one failure. This child asks whether **the structure across versions** distinguishes rotating strengths, recurring loss of access, and cumulative loss—and whether it tells us where to intervene.

Freeze chronologically ordered versions A, B, C, but allow discovery in either direction. Keep an arrow A → B only when A proposes a family of still-valid tasks for which A passes and B fails on independently checked, held-out instances under the same serving interface and budget. Record the family, discovery cost, signed pass-rate gap and uncertainty, and run the reverse audit too. C → A can close the loop by showing that C has an old competence A lacked. It is **not** evidence that A forgot that competence: call it a temporal loss at A only if a checkpoint before A demonstrably had it. Record exposures, losses, gains and first observed mastery separately; a missing edge may mean untested or underpowered.

Cycles in the raw exposure graph can be trivial: two specialists may expose each other, and three versions with different strengths can do the same. For a stronger test, predeclare a practical margin and compare both directions on a common, independently sampled panel for each family. Freeze one admissible family set for the whole triple. For each ordered pair, compare the largest family advantage with the largest reverse family advantage, using simultaneous bounds across families and pairs. Count a dominant leg only if its winning family has a verified exposure witness and its lower bound beats the largest reverse upper bound by the predeclared margin. A strict triangle requires this asymmetry on every leg; keep the raw family-labelled graph too so opposite strengths are not erased. Do not use the difference of pooled negative-flip rates on a common panel as the cyclic score: the discordant rates differ by exactly the accuracy gap, and scalar accuracy differences sum to zero around a triangle. Pair-specific discovery alone can manufacture cycles by changing what gets measured.

For example, suppose A, B, C pass respectively on families x/y/z with probabilities (.90/.10/.50), (.50/.90/.10), and (.10/.50/.90). Each version beats the next by .40 on two families, but loses by .80 on one; using the largest family gap gives A → C → B → A. All three have the same average. This is a rotation of **performance profiles**, not proof of temporary forgetting or persistent knowledge in weights. Track the same tasks over time: recovered old families indicate recurrence, distinct downward steps indicate attrition, and gains with no earlier witness are acquisition. A triple can contain all three. Clockwise and counterclockwise cycles have no causal interpretation without an intervention.

## The hint-recovery assay

On a verified miss, ask an ancestor that mastered the family to propose an admissible cue: a task interpretation, retrieval key, legal observation, or intermediate state the evaluator can independently validate. Freeze the recipient and replay from the same start, same remaining budget and matched seed. Give both versions the hint. Compare against no hint, matched neutral and shuffled hints, common task rephrasing, hints from the recipient and a capability-matched non-ancestor, and an audited interface/state override where available. Count all proposal and selection attempts; use a discovery split to select hint rules and a blind split with new tasks, realizations and destinations to test them.

Prefer cues fixed across instances with different answers. For state-dependent cues, use answer-balanced cases sharing the same cue, check for leakage through wording/order/length, and include a cue-only solver and a matched novice or pre-acquisition recipient. If a hint supplies a critical computation, reveals a new fact, narrows the answer to one choice, or enables a novice to learn a new procedure as readily, call it **assisted solving**, not evidence of retained ability. Check that a rescued recipient completes independently verified downstream steps and generalizes when irrelevant surface features and destinations change. Use an intentionally answer-bearing arm to calibrate how easily teaching can masquerade as rescue; never count it as recovery.

Report **serving loss** before intervention, **access loss under the tested interface** when a non-teaching cue reproducibly restores execution, and **persistent failure within the declared intervention class and budget** otherwise. A failed hint alone cannot prove erasure. Bound claims of true loss to a finite, inspectable host: exhaust the admitted read/intervention space or show that two histories requiring different responses lead to the same complete accessible state, with matched inference and no external carrier. In an open model mark unresolved cases as such. Rebuild the graph at each intervention level with the same tasks, and report separately which triangles disappear because the losing endpoint improves versus because a previously winning endpoint is harmed. Diagnostic rescues and unaided retention after a repair are two separate outcomes.

## Prior art and shared first-test contract

- **Cycles and audits already exist.** [PSRO](https://arxiv.org/abs/1711.00832) and [Real World Games Look Like Spinning Tops](https://arxiv.org/abs/2004.09468) give population and non-transitivity baselines. [HodgeRank](https://arxiv.org/abs/1011.1716) separates scalar ranking from cyclic residuals. [Asymmetric self-play](https://arxiv.org/abs/1703.05407), [DeepXplore](https://arxiv.org/abs/1705.06640), [CheckList](https://arxiv.org/abs/2005.04118), and [Regression Bugs](https://arxiv.org/abs/2105.03048) already give task proposals, disagreement search, behavioral families, and negative flips. The claim to test is what signed, verified, family-specific cycles buy over those baselines, not that a cycle can be drawn.
- **Hints and retention already exist.** [Chain-of-thought prompting](https://arxiv.org/abs/2201.11903), [zero-shot CoT](https://arxiv.org/abs/2205.11916), [Ask Me Anything](https://arxiv.org/abs/2210.02441), and [Tree of Thoughts](https://arxiv.org/abs/2305.10601) make generic cues, alternate prompts and search mandatory controls; [implicit in-context gradient descent](https://arxiv.org/abs/2212.10559) makes learning from a hint an alternative explanation. [LwF](https://arxiv.org/abs/1606.09282), [DER](https://arxiv.org/abs/2004.07211), and [MIR](https://arxiv.org/abs/1908.04742) are repair controls. The [idea ledger](https://github.com/manojbajaj95/cl/pull/6) rules out credit for generator identity alone, margin effects dressed up as mechanisms, and archival gains that tie replay or save/restore at equal budget.
- **Scope.** [Cross-generation inheritance (#130)](https://github.com/manojbajaj95/cl/pull/130) and [fossil beliefs (#132)](https://github.com/manojbajaj95/cl/pull/132) ask what to transfer or refuse; [generator-side forgetting (#120)](https://github.com/manojbajaj95/cl/pull/120) asks whether the ability to pose tasks was lost; [label-free detection (#126)](https://github.com/manojbajaj95/cl/pull/126) already separates router and executor effects with a swap; [first point of loss (#134)](https://github.com/manojbajaj95/cl/pull/134) already distinguishes service failure, bounded unreadability, and exact information loss. Here the starting point is an independently verified solved/failed contrast and the target is its **joint** behavior across versions, families and interventions.
- **Common CPU contract.** Use tiny learned planners, transducers or classifiers with independently enumerable tasks and competing updates; use planted access-only, execution-only and verifier-drift cases only for calibration, never as evidence that cycles arise naturally. Hold out entire families or templates where appropriate, not just seeds. On discovery, log proposer recall against the attainable family panel. Match calls, hint and rollout budgets, proof checks, archive bytes and update steps. Bootstrap over training streams and task families; select edges and thresholds before confirmation; compare against nulls with matched difficulty, old margins, temporal lag and search coverage. Each first test includes a matched next-update or release comparison with ordinary unaided old tasks, measuring each old cohort (including non-cycle ones) and matching newest-task acquisition. No runs or novelty claims are reported here.

## Research ideas (22 cards)

### A. Measure a cycle that is not a sampling artifact

#### 1. A triangle certificate with an expiry condition
- **Mechanism:** Store three signed family witnesses and a bound on each pair's reverse-family advantage; revoke a certificate if a new reverse witness overturns a bound or the rules change. Unknown pairs never count as wins.
- **Novelty bet (primitive candidate):** Unlike HodgeRank's residual or Regression Bugs' negative-flip rate, the certificate can be falsified by a named held-out reverse family; compare to HodgeRank on the same family score table plus marginal flip intervals.
- **Cheapest first test:** Sample small learned three-skill streams twice; confirm certificates blind, and compare against nested-competence and crossed-strength simulations with the same margins and audit power. Use both diagnostics to choose between identical candidate next updates.
- **Old-task retention:** Score untouched ordinary instances from every prior skill after the chosen update; test whether certificate-guided choices beat pooled-flip choices at equal new-task gain.

#### 2. A rotation null conditioned on the skills each model has
- **Mechanism:** Resample task-by-version outcomes while holding per-version success, per-family difficulty, and adjacent-checkpoint overlap fixed within strata. Ask whether cycles require higher-order structure beyond specialization and serial correlation.
- **Novelty bet (improvement):** The spinning-top baseline models strategic payoffs; this null tests whether verified regression triples remain surprising even after controlling for the actual competence panel and time ordering.
- **Cheapest first test:** Enumerate admissible small binary panels with those constraints, and check whether excess cycles predict which losses recur after one update better than a lag-matched flip count.
- **Old-task retention:** For each predictor, replay an equal number of old cases before the next shift; check clean per-cohort accuracy and newest-task gain.

#### 3. Close the loop on identical item IDs
- **Mechanism:** Attach item-level version histories to the family graph. Test whether the apparent loop tracks recurring misses on the *same* items or whether each edge loses different items within similarly named families.
- **Novelty bet (primitive candidate):** CheckList families and negative-flip tables supply the inputs; the new object is a cycle certificate that carries recurrence or disjoint-attrition evidence, compared to ordinary per-family transition counts.
- **Cheapest first test:** Alternate rule training in a small transducer, hold a fixed blind panel, and compare item-closure classifications and matched replay selections against families with shuffled IDs within difficulty bins.
- **Old-task retention:** Measure original old distribution and generalization to new instances of the same rules after replay; a win on the traced IDs alone does not count.

#### 4. Reverse the curriculum, not the time arrows
- **Mechanism:** Train from a common checkpoint with the same batches in opposite orders. Keep confirmation tasks fixed. Predict which cycle edges exchange families when the order switches and which stay tied to capacity.
- **Novelty bet (improvement):** Spinning-top analysis characterizes strength tiers; this probes intervention on training order rather than attributing a descriptive residual to history. Compare to the per-family recency rule and MIR's local interference score.
- **Cheapest first test:** Run both permutations of three mini-curriculum blocks in a small MLP, then a common fourth block with equal-size repairs chosen by each predictor.
- **Old-task retention:** Report ordinary old accuracy after the fourth block, separating the reordered and untouched cohorts at matched fourth-block progress.

#### 5. Forecast rotators before the last vertex exists
- **Mechanism:** Use the first two confirmed legs and earlier same-family histories to predict a specific reverse edge after a separately specified update, including which family supplies it. Score failed predictions as well as closures.
- **Novelty bet (improvement):** Unlike PSRO scheduling after observing payoffs, this bets on prospective family-specific regression structure; compare to recency, marginal flip rates and MIR stacked together.
- **Cheapest first test:** Blind the last checkpoint in tiny sequence-learning streams; choose a replay set from each forecast before training and measure edge and family precision.
- **Old-task retention:** Run the common last update and measure independent ordinary old cases across all skill families, not just those predicted to close the loop.

### B. Ask what a hint actually restores

#### 6. Hints that cannot choose the answer
- **Mechanism:** Have the ancestor nominate a single reusable cue for an answer-balanced class. Randomly instantiate the hidden task details after the cue is frozen, so the recipient must generate the condition-specific output.
- **Novelty bet (primitive candidate):** Adds a prospective no-answer-information constraint to the parent's paired hint replay, stronger than ordinary CoT or paraphrase sweeps; compare equal-information generic, current and unrelated cues and a cue-only solver.
- **Cheapest first test:** On a finite rewrite grammar, freeze a hint such as which stored rule to query, then sample new symbol bindings and counterbalanced outputs. Use rescue results to select matched route versus execution repair.
- **Old-task retention:** After repair, test blind old grammar instances with no supplied cue, including other rules and bindings, at matched new-rule progress.

#### 7. Cross the donor and recipient on every leg
- **Mechanism:** Use a frozen hint bank with every donor (including a pre-mastery version) addressing every recipient on the same cases. Compare the donor × recipient interaction after removing generic cue quality and recipient responsiveness.
- **Novelty bet (primitive candidate):** Unlike Ask Me Anything prompt aggregation or a one-edge router/executor swap, a cross-version response matrix tests whether compatible access routes themselves rotate; compare a donor-quality plus recipient-quality model and same-budget recipient search.
- **Cheapest first test:** Use a small learned route selector with multiple equivalent cue vocabularies; reserve unseen cue realizations and test whether the interaction selects a better gateway to repair than the additive model.
- **Old-task retention:** Evaluate all old destinations unaided after equal-cost repairs, including pairs for which the donor matrix predicted no rescue.

#### 8. Matched twins disagree only after the cue
- **Mechanism:** Match a previously competent checkpoint and a never-trained sibling on unaided failure and generic cue responsiveness. Ask whether a frozen ancestor cue preferentially restores fast, correct downstream execution in the formerly competent one.
- **Novelty bet (improvement):** Implicit in-context learning predicts that cues can teach; a history-by-hint interaction is a stricter recovery signal than prompt lift alone, although matching does not establish weight-level localization.
- **Cheapest first test:** Train two tiny retrieval agents to the same unhinted failure rate by different histories and test both on novel answer-balanced tasks, with deliberately teaching hints as a positive control; compare route-only and solver-only repair.
- **Old-task retention:** Check both histories on ordinary unhinted old retrieval and planning after the same new update, scoring untouched cohorts separately.

#### 9. Remove the last cue atom
- **Mechanism:** Let an ancestor propose several independently checkable cue atoms. Find minimal sufficient subsets, then swap or remove one atom on unseen tests. If a different sufficient subset rescues the same skill, the original route was not uniquely necessary.
- **Novelty bet (primitive candidate):** Unlike a single forced-access swap or Tree of Thoughts reranking complete branches, this yields alternate minimal access sets with falsifiable sufficiency and redundancy. Compare the best singleton plus equal-budget random subsets.
- **Cheapest first test:** Exhaust subsets of four legal observations in a small grid planner; preselect minimal sets on discovery cases and use their redundancy to allocate equal-cost route repair.
- **Old-task retention:** Check unhinted old routes with both single and redundant paths, including ordinary untouched routes, after the update.

#### 10. Predict rescue transfer before translating a cue
- **Mechanism:** Derive a version-to-version cue mapping from cases where all versions succeed; freeze it and predict rescue on cases where one fails. Across A, B and C, compare direct map with composition around the loop.
- **Novelty bet (primitive candidate):** This is composition of access vocabularies, not adapter transfer or Ask Me Anything's prompt ensemble. Direct translations, matched paraphrase search and a shared canonical interface are baselines.
- **Cheapest first test:** In small learned planners with redundant key aliases, fit mappings on common successes, then check where composed hints work on unseen failed routes and compare composition-guided repair against direct mapping.
- **Old-task retention:** Score old aliases and destinations using each version's ordinary interface after equal-budget repair, alongside the new destinations.

#### 11. Cue now, solve after a fork
- **Mechanism:** Supply a legal hint before randomly branching the task into several outcomes, then remove the cue from subsequent observations. Test whether the recipient carries forward an internal plan or simply follows a hinted endpoint.
- **Novelty bet (primitive candidate):** [ReAct](https://arxiv.org/abs/2210.03629) interleaves external observations and decisions; a post-cue fork falsifies recovery shortcuts across all downstream branches without demanding identical private reasoning.
- **Cheapest first test:** In a tiny partially observed puzzle, independently randomize the goal after the cue; compare success in fresh forks to reading the same budget of generic reminders, and select route versus state maintenance repair.
- **Old-task retention:** Test unhinted normal old puzzles and previously unseen forks after the next update; verify that ordinary newest-task performance survives.

### C. Compare what changes when the graph is intervened on

#### 12. A cycle's lifetime across the hint budget
- **Mechanism:** Construct the same labelled graph under increasingly permissive nested menus: serving, format cues, legal retrieval cues and forced admissible state. Record the smallest verified rescue level per edge, labeling reversals and newly introduced edges.
- **Novelty bet (primitive candidate):** Extends the parent's single-edge paired intervention and #134's reader-budget distinction to **joint persistence**: does a whole motif predict repairability beyond independent edge thresholds? Compare to those thresholds plus HodgeRank and pooled prompt gains.
- **Cheapest first test:** Exhaust the finite menus for three freely trained small controllers and compare motif-guided versus independent-edge repair allocation with equal resource caps.
- **Old-task retention:** Measure unaided per-cohort success after one matched update; flag any graph improvement caused by a lower winning endpoint rather than recovery.

#### 13. Cut one gateway, predict which edges disappear
- **Mechanism:** Identify a candidate shared access gate from two edges; force it open on only one recipient and predict collapse on a held-out incident edge before looking. Leave executor and other routes frozen.
- **Novelty bet (primitive candidate):** LA2 and #126 localize a single break; the proposed cross-edge effect tests a reusable cause and must beat independent LA2 diagnosis plus grouping cases by shared task family.
- **Cheapest first test:** Use a small modular planner with shared gates of unannounced reach and compare held-out edges using one bridge cue, a placebo gate and independent single-edge fixes.
- **Old-task retention:** Patch the implicated gate with matched supervision and score unrelated old routes that share it, old routes that do not, and the latest routes unaided.

#### 14. Test whether the missing piece follows the reader or the memory
- **Mechanism:** In a finite modular host, cross frozen readers and stores across all vertices under a fixed typed interface. Predict the full cycle from the best reader-only and store-only model; ask which residual requires a specific reader–store pairing.
- **Novelty bet (primitive candidate):** A multi-version extension of #126's four-corner swap is only interesting if it predicts a new incompatible pairing beyond fit-per-pair swaps or imitation via LwF. Use sham swaps on equivalent representations to detect interface artifacts.
- **Cheapest first test:** Enumerate the swap grid of a tiny learned key-value agent and withhold one pairing, then compare compatibility-guided repair with equal-cost reader-only or store-only adaptation.
- **Old-task retention:** Give no borrowed memory at assessment; score ordinary old query and write behavior after the matched repairs, as well as the newest keys.

#### 15. Learn whether repairing the loop commutes
- **Mechanism:** Repair two confirmed edges in opposite orders with identical batches. Predict whether repairing one through access versus execution displaces the other loss onto a third previously intact family.
- **Novelty bet (primitive candidate):** MIR predicts immediate interference; the cycle-level bet is that diagnosis predicts a noncommuting collateral repair beyond MIR plus pairwise repair lifts and the parent's collateral audit.
- **Cheapest first test:** From the same small transducer snapshot, test both repair orders, joint replay and matched single-edge repeats. Keep total steps fixed and check the predicted third-edge sign blind.
- **Old-task retention:** Compare the unaided post-repair Pareto front on ordinary old cohorts, including the third family, at matched new-task acquisition.

#### 16. Distinguish bottleneck sharing from merely hard tasks
- **Mechanism:** Two deficient families can each be rescued in isolation. Alternate them with the same context and budget, and test whether activating one suppresses the other more in cycle vertices than in matched acyclic controls.
- **Novelty bet (improvement):** The target is a causal interaction between rescues, not a margin or confidence proxy. Compare simple context dilution, random order, and generic Tree of Thoughts search at equal budget.
- **Cheapest first test:** Switch between two small planning rules with neutral matched context and counterbalanced order; test whether an interaction-selected routing fix beats a difficulty-selected replay batch.
- **Old-task retention:** Check ordinary singleton old tasks and natural mixed old sequences without assessor hints, as well as the latest rule.

#### 17. Construct opposite histories ending in the same state
- **Mechanism:** In a finite learner, find distinct training histories that produce different old answers but merge into identical complete readable states. Exhaust permitted hint actions that cannot identify the history. Use those pairs as erasure anchors, alongside retained-but-misrouted controls.
- **Novelty bet (improvement):** #134 already defines exact loss; the new use is calibration of cycle diagnoses against indistinguishable erased histories rather than treating non-rescue as proof. Compare to thresholding Regression Bugs plus hint success alone.
- **Cheapest first test:** Enumerate a quantized automaton with full snapshot access and comparable old pass rates. Check diagnostic false-loss and false-recovery rates, then compare where diagnostics allocate a fixed next-update repair budget.
- **Old-task retention:** Test ordinary unaided inputs from both histories and unaffected old families after repair, distinguishing relearning from restoring access.

### D. Spend the archive and repair budgets on the right evidence

#### 18. Retain the vertex whose probes cannot be replaced
- **Mechanism:** Choose archive members by marginal ability to discriminate rotation from attrition and access from downstream loss on new families, not by volume of regressions. Penalize a vertex if its unique cues can be replaced by a compact static artifact.
- **Novelty bet (improvement):** Extends the parent's cycle-coverage archive with identifiable diagnoses, not just PSRO diversity. Compare recency, accuracy, PSRO, family coverage and a same-byte store of cases plus cues.
- **Cheapest first test:** Keep two small planners or equal-byte artifacts from a five-version stream. Predict the next release's correct repair type on blinded losses; charge the full audit.
- **Old-task retention:** Apply equal-budget repairs and measure unaided ordinary performance over all old cohorts, including those from discarded versions.

#### 19. Rehearse the gateway without rehearsing the task
- **Mechanism:** Use hint recovery to pick older gates for training. Teach access choices on separate tasks with disjoint answers, then remove the helper; use downstream replay only on persistent misses.
- **Novelty bet (improvement):** LA2 already advocates routing versus consumer repair. The falsifiable extension is whether one transferable gateway update repairs several cycle edges without training on their outputs; compare LA2 plus MIR with equal labels, updates and budgets, and generic gateway training.
- **Cheapest first test:** Hold out all hint-witness tasks while training a small router on distinct goals using the same verified gateway assignments. Compare to end-to-end replay and a wrong-gateway control.
- **Old-task retention:** Assess unaided normal old tasks on both sides of the loop and old tasks beyond it, retaining newest-task gains.

#### 20. Fixed-budget release portfolios that preserve access
- **Mechanism:** Build a small set of candidate updates and use the graph to reject choices that only shift exposed failure families, distinguishing recoverable displacements from newly persistent ones. The deployed candidate runs alone.
- **Novelty bet (improvement):** Unlike a scalar negative-flip gate or a PSRO mixture at inference, select a single release by its forecast of which failure types will persist. Compare to the strongest per-family Pareto gate plus hint-aided flip counts.
- **Cheapest first test:** In a three-shift stream, choose among common candidates using blind diagnostics per arm. Charge withheld releases against new-task acquisition rather than rewarding permanent abstention.
- **Old-task retention:** Score ordinary unaided old performance throughout the stream and worst-cohort loss at comparable new-task adoption.

#### 21. Pay for disambiguation instead of the next failure
- **Mechanism:** Pick the next edge-and-hint query by expected ability to distinguish two competing diagnoses (e.g., recurring router closure versus unrelated execution losses), then choose the cheapest repair that would differ between them.
- **Novelty bet (improvement):** PSRO and asymmetrical curricula seek informative opponents or tasks; this query's value is a changed repair decision, not extra cycle count. Compare family coverage, expected failure yield and uncertainty sampling with the same hypothesis menu.
- **Cheapest first test:** Allocate a dozen checks in a tiny held-out controller stream with mixed causes and unequal audit costs; compare how often matched planners choose the repair that maximizes blind retention.
- **Old-task retention:** After the chosen repairs, score ordinary unhinted sequences at matched latest-task gain; include small cohorts with little chance of attracting queries.

#### 22. Retire a cycle only after testing the next shift
- **Mechanism:** Declare a loop resolved only when an unaided repair generalizes and the same access routes survive a new overlapping curriculum block. Where routes recur but old failures relocate, keep the underlying families under separate surveillance.
- **Novelty bet (improvement):** The parent's escrow and MIR already retest cases; the added prediction is that a shared cue-dependent motif forecasts synchronized relapse beyond each edge's own recurrence and task similarity.
- **Cheapest first test:** In a tiny planner, choose equal-size follow-up buffers with motif-based or independent-edge forecasts and run the same held-out shift. Compare calibrated relapse predictions and clean retention.
- **Old-task retention:** Track normal unaided old tasks after repair and after the next shift, including non-motif families and latest tasks; do not count assisted successes as preserved.

## Ranked deeper sub-questions

1. **Do verified cycles distinguish recurring loss of access from cumulative loss?** First confirm strict triangles against matched nulls and trace identical items (1–4). Then apply the no-answer-information hint assay (6–8, 12). If old items recur and triangles disappear through recipient rescue, the evidence favors rotating access; if misses accumulate and resist the menu, report bounded persistent attrition, not erasure. If neither diagnosis beats independent per-family histories, drop the graph as a diagnostic.
2. **When does an ancestor cue identify retained execution rather than deliver a substitute skill?** Start with pre-mastery twins, answer-balanced forks and the exact-loss anchors (6, 8, 11, 17). Ask whether rescue predicts the effect of an unaided route-only repair on fresh tasks better than generic prompt lift or replay. If novices benefit equally, retain the hint only as assistance.
3. **Can one repair break multiple edges without moving the loss?** Predict the side effects of a shared-gate intervention and opposite repair orders before exposing the blind cases (13–16, 19). Keep the motif only if it improves held-out ordinary retention at matched new-task progress over the strongest stacked single-edge controls.
4. **What should a bounded archive retain once cases, cues and live policies compete?** Compare equal-byte archives for their ability to choose a repair that survives the next shift (18, 21–22). If static cases plus cues predict recovery and preserve old tasks as well as live vertices, keep the artifacts and retire the policies.
