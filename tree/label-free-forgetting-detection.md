# Label-free forgetting detection: can a monitor beat a small labelled canary?

Parent: [PR #125, Thermodynamics of remembering](https://github.com/manojbajaj95/cl/pull/125), especially card 13, the Harada–Sasa fluctuation–dissipation gap. The parent shows that equal weight displacement can cause very different old-task loss; it does not show that any label-free signal beats a labelled canary. This node proposes tests, not results.

**Node question.** Can a deployed model or agent tell that it has lost a previously demonstrated capability, without grading its outputs, sooner or more reliably than a small, well-designed labelled canary at the same monitoring budget? The bet is on structured probes: how responses compare with spontaneous noise, how a skill behaves under equivalent routes, and whether an intervention restores access to it. Entropy or output drift alone is not the claim.

## What is identifiable?

Forgetting is a drop relative to the pre-update system on **fresh inputs from a fixed old task distribution**, with the same task semantics and execution conditions. A changed workload, changed API contract, or stochastic decoder is not evidence of forgetting. Report deployed-stack loss and controlled-stack loss separately: a missing route can cause real deployed failure while the skill remains available through another route.

There is no distribution-free detector. On an old region where the old and current models disagree, two worlds can give the monitor identical inputs, outputs, and intervention traces while the hidden rubric prefers the old answer in one and the current answer in the other. Even exact self-consistency cannot break that symmetry, and live traffic can omit the affected region entirely. Each card therefore bets on an observable bridge: historical behavior, a task relation that excludes some wrong behaviors, an independently perturbed component, or a coverage assumption. No per-item expected answer, scored reward, execution-success predicate, or grader may enter the label-free arm; a relation or tool trace that effectively reveals correctness counts as supervision. Report blind spots or abstain rather than treating silence as retention.

## Common CPU first-test protocol

- **Two small worlds.** Train a linear or two-layer model on old symbolic classification families, then on new families with tunable overlap; use a tabular agent in a small symbolic tool environment for routing, retrieval, or tool cases. Use paired checkpoints and independently seeded streams. Separate ordinary interfering updates from planted faults used to check identifiability. Cross actual forgetting with harmless changes in traffic mix, confidence/temperature, update scale, or environment version. Include stable yet wrong outputs and, where relevant, useful changes that disagree with the old checkpoint. Match pre-update difficulty, per-item margin and frequency before claiming any ordering advantage.
- **One retention target.** An evaluator-only, fresh, fixed old-task panel measures drop in accuracy or task success from the healthy checkpoint, by family and overall. Start with a 5 percentage-point drop in a prespecified old family as the event; estimate when it first occurs with enough independent examples to resolve that drop. Compare event recall at a fixed false-alarm rate (e.g. 5% of healthy windows), delay from first crossing (negative means lead), and misses by family. Use only past observations to alarm; fix evaluation horizons and thresholds without test labels. Record post-update new-task success too. If the healthy and impaired truth panels cannot reliably be separated, the first test is inconclusive, not a monitor win.
- **The bar on every card.** Beat the strongest affordable small labelled canary, not an intentionally random or stale panel. Compare stratified, margin/diversity-selected, and, where affordable, refreshed or sequential canaries under the same false-alarm allowance; let the canary use paired pre/post scores, group information available to both sides, and spend spare budget on repeats or more judicious label selection. Also compare the strongest applicable simple unlabelled control: confidence/entropy, output KL or disagreement against the old checkpoint, input two-sample drift, or direct single-factor ablations. Match query schedules and available action types for baselines where possible; demonstrate signal beyond raw dose, margin, or component changes.
- **Pay for everything.** Sweep a shared end-to-end budget: charge annotation or executable grading, retained bytes, inference calls/tokens, sandbox/tool calls, fork copies, baseline collection and per-window compute. Both sides face the same per-resource caps and all-in cost ceiling; the label-free arm can spend avoided annotation costs on other observations within those caps. Report the raw resource vector and break-even cost frontier when prices differ or one resource cannot be matched. Include a cheap-label regime, even free labels in the toy environment; do not assume that label savings buy unlimited queries. Gold audit labels never train, tune, or select the label-free detectors and are excluded from both arms' costs. Fit nuisance parameters on ungraded healthy history and hold out whole worlds, families or shift types as specified. Bootstrap paired streams, not individual items or windows. If evaluating an alarm-triggered response, use the same repair and repair budget for both arms and recheck fresh old and new tasks.

## Prior art and ledger screen

These are scoped novelty hypotheses, not a claim of exhaustive clearance.

- [Failing Loudly (1810.11953)](https://arxiv.org/abs/1810.11953) compares tests for dataset shift; [black-box label shift (1802.03916)](https://arxiv.org/abs/1802.03916) makes assumptions about the shift. Neither an input shift alarm nor a changed prediction histogram settles fixed-old-task loss. [Average Thresholded Confidence (2201.04234)](https://arxiv.org/abs/2201.04234) calibrates an unlabeled-target accuracy proxy using source labels; [performance under covariate shift (2401.08348)](https://arxiv.org/abs/2401.08348) uses source information and covariate-shift structure. Compare where those assumptions hold; old-task conditional performance can change with the input distribution held fixed. [Efficient stratified model evaluation (2406.07320)](https://arxiv.org/abs/2406.07320) motivates a serious labelled sampling control.
- [Self-consistency (2203.11171)](https://arxiv.org/abs/2203.11171) aggregates reasoning paths, [semantic entropy probes (2406.15927)](https://arxiv.org/abs/2406.15927) estimate uncertainty, and [CheckList (2005.04118)](https://arxiv.org/abs/2005.04118) already tests behavioral invariance and directional expectations. Agreement and metamorphic testing are baselines, not new primitives. [Empirical CL forgetting in LLMs (2308.08747)](https://arxiv.org/abs/2308.08747) measures forgetting with downstream task evaluations; use those as audit targets, not label-free inputs. [Unsupervised accuracy estimation by perturbation (2307.10062)](https://arxiv.org/abs/2307.10062) already uses perturbation-induced prediction changes; perturbing something is not the novelty.
- [Harada–Sasa (cond-mat/0502505)](https://arxiv.org/abs/cond-mat/0502505) is an equality for specified stochastic dynamics and conjugate response/observable pairs, not arbitrary logits across deploys. [Training irreversibility (2605.21933)](https://arxiv.org/abs/2605.21933) is not an old-task detector. Below, a fluctuation–response residual is an empirical alarm unless the assumed dynamics and forcing actually justify a physical FDT interpretation. A frozen API has sampling fluctuations, not SGD fluctuations; it cannot identify an SGD response kernel.
- The [idea ledger](https://github.com/manojbajaj95/cl/blob/52c8e82/reviews/idea-ledger.md) rules out weight-bit loss (Landauer), pure noise-temperature forgetting, sparse damage decoding (functional syndromes), and an early memory-loop Lyapunov alarm that lost to direct two-order divergence. The cycle-consistency lesson score was dropped, and attaching the same tests erased the proposed tools-versus-lessons detection advantage. Reverse grokking and cooldown facts warn against margin and frequency confounds; the A3 controls warn that entropy matching can explain apparent mechanisms. No weight-bit counts, sparse-fault assumption, lesson-quality judge, or free regression oracle below.

## Research ideas

Every first test is the cheapest proposed opportunity to **beat the small labelled canary under the common budget and false-alarm rule** as well as the local control named in the card. Every retention check uses the sealed old-task panel, never detector feedback. These cards propose possible advantages; a tie is a falsifier for the claimed advantage in that setting.

### A. Separate directed response from ordinary noise

1. **Response residual on an old-task observable.**
   - **Mechanism:** In a sandbox that exposes writes, collect lagged covariance of unlabeled predictive contrasts under repeated healthy updates and paired signed impulse responses to a small write perturbation. Learn the healthy relation between the two, then score its frequency-band residual during continual updates. Use paired random seeds and an amplitude sweep to test the linear-response regime.
   - **Why new:** This is the parent's candidate made operational: an old-panel-specific, healthy-calibrated residual, not an assumed equilibrium temperature or a scalar measure of train irreversibility.
   - **Cheapest first test:** Two-layer MLP; match update magnitude and seed variance between conflicting and benign streams. Try to beat the canary, logit drift, and both inputs to the residual individually or stacked.
   - **Old-task retention check:** Measure lead to a fresh old-family accuracy crossing after slow and abrupt shifts; also test the arm in which stirring the optimizer forgets nothing.

2. **Signed response fingerprint at matched noise.**
   - **Mechanism:** Apply opposite perturbations along a few historical update directions and matched random directions; compare the direction of the resulting old-probe changes after whitening by repeat-query noise. Score sign reversals and orientation, not just susceptibility magnitude.
   - **Why new:** Perturbation-based accuracy estimation already uses response size; the hypothesis is that directional rotation contains signal after response size, entropy, and noise are matched, rather than reviving the killed noise law.
   - **Cheapest first test:** Linear softmax learner with two rotated update subspaces, fixed margin and equal mean response norm; compare a norm-only detector and simple old-output KL beside the canary.
   - **Old-task retention check:** Score untouched items from each old subspace after ordinary updates as well as planted rotations; check which family actually declines.

3. **Response cancellation and hysteresis.**
   - **Mechanism:** In copied agent state, apply equal and opposite weak updates in both orders. Subtract the sum of individual responses and the healthy order residual. Test whether extra noncancellation reveals inaccessible old behavior at unchanged marginal scores.
   - **Why new:** Unlike a Lyapunov fit or global edit-equivalence claim, this asks whether a measured local order interaction buys retention warning beyond direct two-order divergence.
   - **Cheapest first test:** Tabular retrieval policy with two bounded recency nudges and paired seeds; compare direct order-swapping, independent nudges, and the canary at the same cost.
   - **Old-task retention check:** Check fresh returning tasks under the unperturbed live policy, including old tasks using neither nudged route.

4. **Construct two states with identical immediate answers but different relaxation.**
   - **Mechanism:** Use a short, fixed sandbox perturbation and measure the relaxation of the unlabeled old-panel output distribution back toward its initial distribution; flag a slow tail or overshoot after matching instantaneous drift.
   - **Why new:** The parent Kovacs probe uses old-task loss to see the hump; the hypothesis is that a short, ungraded relaxation trace forecasts the next real loss when immediate output and margin checks agree.
   - **Cheapest first test:** Use a repaired and an unshocked MLP with matched old-probe disagreement and entropy. Compare the trace with its endpoint, total drift, and the canary; do not infer long-run effects if even evaluator truth has no spread.
   - **Old-task retention check:** Release both learners into a blind mix of old and new examples and score the worst subsequent old checkpoint plus recovery.

5. **Paired frequency tags on an agent route.**
   - **Mechanism:** In a cloned agent, weakly toggle retrieval bias or a neutral context cue on a balanced schedule and measure the output component coherent with the toggle. Compare the tagged component to an orthogonal placebo waveform to reject nonstationary background variance.
   - **Why new:** Moves beyond a single noisy WITH/WITHOUT estimate only if repeated, phase-locked response separates route access from distractor churn more cheaply at equal total calls.
   - **Cheapest first test:** Two-route tabular agent with random tool delays and a weak, signed retrieval bias. Compare randomized A/B means, a seed-noise control, and the canary.
   - **Old-task retention check:** Without tags, replay unseen old goals under nominal delays and under a changed delay distribution; delay alone should not trigger forgetting.

### B. Test structure, not just consistency

6. **Relations that separate known wrong solvers.**
   - **Mechanism:** Select label-free input transformations for which common, consistent shortcuts violate an output relation. Choose transforms against synthetic shortcut policies, not audited task labels; record which shortcuts survive the entire panel.
   - **Why new:** CheckList already gives invariant and directional tests; the new object is a relation panel designed to rule out particular classes of stable wrong behavior, with its residual ambiguity exposed. It is not a lesson judge.
   - **Cheapest first test:** Toy symbolic routing with a position heuristic and a constant fallback; compare random metamorphic tests, semantic entropy, and the canary.
   - **Old-task retention check:** Score fresh routing tasks with held-out permutations and an unseen shortcut; a consistently wrong survivor is a miss, not evidence of retention.

7. **Hold the goal fixed; cross the independent realizations.**
   - **Mechanism:** Elicit one old goal through two different observable routes and check whether the two action traces agree after removing route-specific syntax. Monitor the route-by-goal interaction rather than overall agreement.
   - **Why new:** Voting cannot identify a systematically bad route; this tests independent realizations for selective collapse, including whether a shared decoder causes both to agree while wrong.
   - **Cheapest first test:** Compare text-to-tool and direct symbolic routes in a two-path agent with shared and independent bottlenecks; compare plain self-consistency, disagreement, and the canary.
   - **Old-task retention check:** Score fresh old goals per route and end-to-end under normal routing; report common-mode misses explicitly.

8. **Balanced squares of semantic changes.**
   - **Mechanism:** Cross a known nuisance transformation with a task-relevant transformation having a known output relation, such as renaming tools versus swapping two operand roles. Compare relation residuals across all four corners rather than grading an output.
   - **Why new:** Single-transform metamorphic tests can pass when an agent handles each change in isolation; the squared contrast targets a failure that appears only when meaning and surface change together.
   - **Cheapest first test:** Four-item tool-world squares with held-out lexical substitutions; compare an equal-size independent transformation panel and the canary.
   - **Old-task retention check:** Score fresh compositions requiring both transformations and ordinary old tasks requiring neither; flag if the monitor only detects exotic failures.

9. **Consistency along withheld composition paths.**
   - **Mechanism:** Ask the same old transformation in one step and through independently phrased substeps. Check the relation between their outputs without scoring either, and compare path-specific disagreement with pre-update history.
   - **Why new:** This is not generic cycle scoring: direct and factored paths can agree on trivial short problems, so the hypothesis is that disagreement growth with composition depth detects loss of transferable old procedure first.
   - **Cheapest first test:** Tabular string transducer, one- to three-step compositions, with shortcut policies and random path lengths. Compare plain round-trip consistency and the canary.
   - **Old-task retention check:** Score previously unseen composition orders and routine one-step old tasks independently of the decomposition generator.

10. **Relational shrinkage of the answer space.**
   - **Mechanism:** On a family of unlabeled inputs, use only justified output equivalences and inequalities to estimate what fraction of input pairs the model incorrectly collapses into the same answer class; do not identify the class labels themselves.
   - **Why new:** A confident constant policy has low entropy and high repeat agreement; detecting the loss of required distinctions needs relations between inputs rather than uncertainty per input. A global label permutation can still fool it.
   - **Cheapest first test:** Binary or multiclass symbolic classifier with a known input symmetry and equal-confidence under-collapse and over-collapse faults. Compare prediction histograms, CheckList-style isolated relations, and the canary.
   - **Old-task retention check:** Audit unseen old input components, including a planted global permutation with intact relations, to measure the blind spot.

11. **A monitor that tests its own invariances.**
   - **Mechanism:** Maintain a sentinel panel of task-preserving perturbations and matched changes known only to alter execution conditions (e.g. decoder seed or wrapper syntax). Down-weight an alarm when it responds equally to both before generalizing it to live traffic.
   - **Why new:** Training an uncertainty score on benign examples is familiar; the candidate is a live counterfactual test of whether the alarm itself is invariant to a newly deployed nuisance, with an explicit abstention.
   - **Cheapest first test:** Hold out a wrapper version and cross wrapper/temperature change with model overwrite. Compare a healthy-calibrated confidence score, an input-drift gate stacked with output drift, and the canary.
   - **Old-task retention check:** Certify loss on fresh old tasks under both wrappers; report true forgetting events the nuisance gate suppresses.

### C. Distinguish lost access from lost ability

12. **Four-corner component transplant.**
   - **Mechanism:** In a sandbox, cross old/current routing and old/current executor snapshots on identical unlabeled goals. Observe which swap restores the healthy pattern; quantify interaction rather than attributing every changed trace to the edited component.
   - **Why new:** Direct ablation is standard; the claim is that one crossed experiment detects and attributes even a forgetting event caused by two individually harmless edits, unlike single-factor comparisons.
   - **Cheapest first test:** Tabular router and solver with hidden route-only, solver-only, and interaction faults. Charge both snapshots; compare single swaps, full rollback/KL, and the canary.
   - **Old-task retention check:** Audit withheld old goals in all four corners; an output-pattern restoration that does not restore task success is a false attribution.

13. **Restoration curve, not just restoration.**
   - **Mechanism:** Ramp an ungraded routing cue from weak to strong, measure the return of historical behavior, and compare with a matched decoy cue. The shape distinguishes a usable skill lying behind a shifted access threshold from similarity that never recovers.
   - **Why new:** Ledger MX1 measures route-dependent correctability, not whether the curve identifies old-skill loss better than matched margin or a single crossover point. The cue must not contain the answer.
   - **Cheapest first test:** Tabular agent with retrieval dilution versus executor overwrite, matched initial disagreement. Compare a single maximum-dose test, a margin control, and the canary.
   - **Old-task retention check:** Score fresh old tasks at normal and each intervention strength; classify latent retention only where live success actually returns with the cue.

14. **Freeze the world, not the agent.**
   - **Mechanism:** Run current and old stacks against the same recorded environmental responses up to shared actions; use a fixed symbolic sandbox for counterfactual branches. Contrast with fresh sessions to isolate an agent-side change from an external contract change.
   - **Why new:** Does not resurrect “tools fail loudly”: no validator is free. The proposed signal is the interaction between policy version and world version, not exceptions or tool tests.
   - **Cheapest first test:** Cross a symbolic API schema migration with an interfering agent update. Compare exception counts, raw policy disagreement, and a canary with access to the same sandbox.
   - **Old-task retention check:** Audit old goals under the pinned old contract and under the current contract separately; do not call a policy sound for the current contract just because it passes old ones.

15. **Gateway versus reachability on a fixed prefix.**
   - **Mechanism:** Start the agent just before or just after a known old workflow branch point, without showing later outcomes. Track whether downstream trace support is preserved despite vanishing use of that branch from an ordinary start.
   - **Why new:** The [generator-side node](https://github.com/manojbajaj95/cl/pull/120) separates exposure from ability; here controlled prefix interventions aim to diagnose a deployed agent's lost gateway without goal validation or relying on unsupported offline off-policy estimates (ledger G1).
   - **Cheapest first test:** Three-stage symbolic workflow with randomized occurrence of an old branch; compare unconditional action frequencies, direct state-conditioned frequencies, and the canary.
   - **Old-task retention check:** Score fresh full workflows and suffix recoveries independently to distinguish disuse from a start-state failure or downstream loss.

16. **Route enrichment without grading.**
   - **Mechanism:** Reassign neutral probe identifiers to make under-observed old routes appear more often in sandbox traffic. Estimate which route-conditional failure signatures rise instead of scoring whatever the production router serves.
   - **Why new:** Ordinary drift alarms weight by live exposure; the hypothesis is that experimentally equalizing route exposure reveals a degrading subgroup even with no sparse damage assumption or correctness oracle.
   - **Cheapest first test:** Tabular mesh with rare routes; halve one route's exposure while separately driving executor loss. Compare uniform old replay, live reweighting, and an equally stratified canary.
   - **Old-task retention check:** Audit fresh old inputs by route and report the worst route as well as the production-weighted average. Exposure change alone is a negative control.

### D. Use the monitoring budget to buy information a fixed panel misses

17. **Adaptive challenge tree over competing failure stories.**
   - **Mechanism:** Choose the next unlabeled intervention that best separates overwrite, decoder jitter, routing loss, and benign drift under competing trace models; stop once additional queries cannot change a decision cheaply.
   - **Why new:** The object being reused is a diagnostic experiment policy, not a learned loss surrogate or a fixed stack of alarms. It must beat the same component tests simply stacked or sampled in a fixed order.
   - **Cheapest first test:** Four causes in a tabular agent with one held-out cause mixture; compare fixed schedules, a score-only sequential test, and an adaptive labelled canary.
   - **Old-task retention check:** Audit old-family success and separately whether the declared cause matches which intervention actually recovers success on new old-task instances.

18. **Sentinel rotation with a coverage floor.**
   - **Mechanism:** Keep a fixed cheap reference slice for calibration, rotate the remaining unlabelled queries toward behavioral regions whose recent traces leave the largest ambiguity, and reserve a nonzero exploration share for unpopular regions.
   - **Why new:** Active testing and stratified sampling are prior art; the hypothesis is that trace-based rotation can sustain usable old-family coverage under a query/label tradeoff while a fixed canary goes stale. It must also beat adaptive, refreshed labelling.
   - **Cheapest first test:** Six symbolic families with a moving rare failure region; compare uniform rotation, uncertainty alone, and static and refreshed canaries of the same all-in cost.
   - **Old-task retention check:** Score a balanced fresh old panel, per-family delay and miss rate, including families not visited in live traffic.

19. **Query the disagreement boundary, audit the interior.**
   - **Mechanism:** Search locally for where old/current answers first diverge under an allowed semantics-preserving perturbation, and estimate how much of the old input neighborhood the discrepancy invades. Keep independent interior samples to avoid a detector that only finds artificially brittle boundary points.
   - **Why new:** Adversarial perturbation accuracy proxies already look for sensitivity; the proposed gain is estimating change in the *extent* of historical disagreement, beyond the first flip or endpoint margin.
   - **Cheapest first test:** Two-dimensional MLP with an old decision region and benign logit rescaling. Compare margin attacks, random drift probes, and a boundary-stratified canary with matched search costs.
   - **Old-task retention check:** Score unperturbed, fresh old examples across the contour and far inside it; ignore disagreement on infeasible inputs.

20. **Historical reference ensemble with disagreement veto.**
   - **Mechanism:** Store compact summaries from independently trained healthy runs over common ungraded probes. Alarm on drift shared across their stable regions; abstain when healthy runs already disagree about the relevant region.
   - **Why new:** Model disagreement is not new. The candidate advantage is separating drift from acceptable historical solutions using a storage-matched reference set, not pooling fleet votes as in the ledger's failed surprisingly-popular fleet memory.
   - **Cheapest first test:** Small softmax models with equivalent alternative procedures and shared-bias faults. Compare a single old checkpoint, raw ensemble disagreement, and the canary; charge the ensemble and its creation.
   - **Old-task retention check:** Audit previously agreed and disputed strata and report the coverage/false-alarm tradeoff, including false alarms on legitimate improvements.

21. **A difference-in-differences monitor across independent update cohorts.**
   - **Mechanism:** Stagger the same new update across cloned learners or agents; subtract changes over a not-yet-updated cohort on the same ungraded old inputs, and independently repeat the stagger for suspect families.
   - **Why new:** Shadow rollouts and staggered experiments are familiar; the hypothesis is that repeated, synchronized within-family contrasts beat raw shadow divergence when ambient nuisance drifts as much as the updated system.
   - **Cheapest first test:** Two tabular cohorts subject to shared wrapper drift and occasional unequal noise; compare raw A/B differences, simple fitted time trends, and the canary. Swap cohort order to test the parallel-trends assumption.
   - **Old-task retention check:** Audit fresh old tasks for each cohort at common checkpoints; failure in both cohorts may be undetectable by this contrast and counts as a miss if old skill actually fell.

22. **An explicit coverage certificate with an abstention region.**
   - **Mechanism:** Partition the old support using independently observable task attributes, and maintain an empirical map from each detection channel to the perturbations or relations it can observe. Combine the maps to decide where “no alarm” is interpretable and spend spare queries on uncovered regions. Never certify correctness from coverage alone.
   - **Why new:** The primary object is a map of what label-free probe channels could distinguish, not a confidence number or a sparse damage decoder. It is valuable only if the map improves decisions compared with a simple per-family sample-count/variance rule.
   - **Cheapest first test:** Enumerable symbolic tasks with some indistinguishable regions and a varying pattern of accessible routes; compare channel stacking, count-based abstention, and a canary allowed the same abstention rate.
   - **Old-task retention check:** Report recall and delay on the entire fresh old panel as well as on covered regions, with loss on uncovered families counted separately and not silently dropped.

## Deeper sub-questions, ranked

1. **What is the cheapest observable that separates harmful forgetting from benign drift when confidence, margin, and raw disagreement are matched?** *(1–5, 17)* Start with matched-noise conflicting and benign streams in the MLP; pre-register a signed response residual and test it against its stacked ingredients and the best canary. A tie across the cost frontier demotes the fluctuation–response program, not just one choice of perturbation.
2. **Which old-task failures are indistinguishable to a given probe family, and what breaks the ambiguity?** *(6–10, 22)* Enumerate shortcut policies in the symbolic world; group them by identical observational and interventional signatures, then measure the cost of splitting a wrong/correct pair with a new relation versus one label. A large unsplittable class tells us where to abstain or buy labels.
3. **Can an ungraded intervention diagnose reversibility well enough to choose an effective repair?** *(4, 12–15)* Separate gate failure, tool drift, executor overwrite and their interactions. Compare the monitor's recommended repair to the canary-driven and immediate rollback arms with equal repair budget; demand better fresh old-task retention without erasing new learning.
4. **Where is the break-even frontier under rare recurrence, correlated probes, and cheap labels?** *(16–22)* Sweep label cost, cohort dependence, probe quality and prevalence on unseen streams. Report the budget regions where the labelled canary wins or no method is reliable. A gain that disappears under refreshed, stratified canaries is not a deployment case.
