# Past selves as adversaries: make forgetting contestable

**Status:** Ideas only; no experiments run. **Branch:** continual learning → evaluation under change → adversarial regression discovery.

## Why the usual defenses miss the loss

A fixed regression suite can only ask questions someone already knew to put in it. Replay can preserve average accuracy while a rare workflow or a recovery behavior disappears. Distillation from the last checkpoint asks the learner to imitate outputs on a chosen distribution; it does not ask the checkpoint to look for missing parts of that distribution. Self-evaluation can miss the same behavior as the actor if both have learned to search in the same way.

Freeze a few earlier versions and give them a different job: **find a valid old task the present version fails, and help establish that the failure is a regression.** A checkpoint can propose a case, act as an opponent that drives the current policy into a rare state, or dispute a diagnosis. It doesn't get to decide what's correct. An independent checker decides that, and a frozen same-lineage witness must still succeed under the same task specification, interface and budget. The hypothesis is that lineage gives auditors useful search biases that a current self-critic or equally capable independent auditor lacks. If not, keep the simpler auditor.

This is not edit equivalence, adapter transport, or transplanting an old skill to a new base. [Cross-generation inheritance (#130)](https://github.com/manojbajaj95/cl/pull/130) asks what to pass down; [fossil beliefs (#132)](https://github.com/manojbajaj95/cl/pull/132) asks what not to copy when the world changes. Here a witness need not teach, donate weights, or be right on any new task. The live question is what an earlier policy can make **observable** in a continuing learner and whether acting on that evidence improves retention.

## Prior art and what it makes a baseline

- **Historical opponents are not new.** [Fictitious Self-Play](https://proceedings.mlr.press/v37/heinrich15.html), [PSRO](https://arxiv.org/abs/1711.00832), and [AlphaStar's league](https://doi.org/10.1038/s41586-019-1724-z) already train with historical policies and exploiters. [Asymmetric self-play](https://arxiv.org/abs/1703.05407) already generates tasks one player can do and another cannot. Compare an ordinary league or proposer/solver game given the same archive and budgets; only independently validated **loss of old competence** counts here, not beating the latest opponent.
- **Imitation and hard replay are not new.** [Learning without Forgetting (LwF)](https://arxiv.org/abs/1606.09282), [Dark Experience Replay (DER)](https://arxiv.org/abs/2004.07211), [Deep Generative Replay (DGR)](https://arxiv.org/abs/1705.08690), and [Maximally Interfered Retrieval (MIR)](https://arxiv.org/abs/1908.04742) cover frozen targets, stored logits, synthetic replay and retrieving items threatened by an update. [Adversarial Continual Learning](https://arxiv.org/abs/2003.09553) uses adversarial training to separate task-invariant and task-specific representations; that discriminator isn't an auditor. Use both an ancestor that supplies targets without searching and a hard-example selector with no lineage.
- **Model-diff testing already exists.** [DeepXplore](https://arxiv.org/abs/1705.06640) uses disagreement to guide test generation; [CheckList](https://arxiv.org/abs/2005.04118) supplies behavioral families and invariance tests; [Regression Bugs](https://arxiv.org/abs/2105.03048) and [model-update regression in structured prediction](https://arxiv.org/abs/2202.02976) measure and reduce negative flips. [LLM red-teaming with LLMs](https://arxiv.org/abs/2202.03286) already generates failures with a separate language model. Compare those search and scoring ideas directly; neither merely finding disagreement nor counting verified negative flips is the novelty.
- **Critics and temporal judges already exist.** [Self-play debate](https://arxiv.org/abs/2409.16636) trains debaters to improve judging; [Self-Play Critic (SPC)](https://arxiv.org/abs/2504.19162) pits a generator of erroneous reasoning against a critic. [Self-Rewarding](https://arxiv.org/abs/2401.10020) uses the model as judge; [Temporal Self-Rewarding](https://arxiv.org/abs/2508.06026) anchors rejected responses to an earlier model and uses later models for chosen responses. Temporal separation alone does not distinguish this node. The proposed signal is a checkable regression on a still-valid task, not relative preferences from earlier models.

This is a targeted prior-art screen, not a priority claim. The [idea ledger (#6)](https://github.com/manojbajaj95/cl/pull/6) is a guardrail: self-quizzing tied style- and coverage-matched replay; small margins confounded apparent forgetting order; L1 prompt-addressable checkpoints lost to equal-byte stored deltas and hurt current ability. Use actual frozen policies or their stored deltas, not version prompts that pretend to reconstruct them. Teacher-refresh schedules and on-policy self-distillation are out of scope.

## Shared first-test contract and kill controls

- **A witness is not a label.** Predeclare the still-valid old task distribution and a separate changed-rule distribution. Count verified negative flips where a frozen earlier reference succeeds and the current learner fails. Track positive flips and ordinary old-task accuracy too: the audit challenge mix isn't a population estimate. Check stale-ancestor proposals against current rules, including cases where the current model is correctly better.
- **Separate discovery, intervention and assessment.** Give the auditor a search sandbox. Never train on assessment cases, paths, seeds or templates. Compare unique verified regression families per unit budget and what fraction of an independently enumerated lost set they cover. Then spend the same update budget per arm and report performance on untouched ordinary old tasks, the predeclared vulnerable slice, and the new task; include collateral loss and confidence intervals across streams. A detection-only first test is followed in the same toy by a matched repair or release comparison; improvements confined to the discovered cases aren't retention.
- **Pay for the whole audit.** Match candidate calls, rollout steps, checked labels, training updates and archive bytes where relevant. Compare static replay, passive ancestor replay/KD, current self-critique, an equally capable unrelated or sibling auditor, directed differential search without lineage, and a historical league without the old-task objective. Match item difficulty, format, task coverage and old margins when attributing gains to lineage. Use the strongest relevant combination, not a weak single ablation. Run the ordinary serving policy without ancestor help at test time.
- **Stop if the causal link breaks.** First confirm there is measurable loss, that the checker is reliable (paired seeds and split-half agreement if stochastic), and that a matching log or buffer doesn't already supply the useful cases. Do not engineer a toy where ancestry has exclusive access to the right answer. If search finds more regressions but produces no retention gain at matched new-task performance, keep it as an evaluation idea, not a learning result.

## Research ideas (22 cards)

### A. Discover failures that fixed replay would not see

#### 1. Counterexample walks across the old task manifold
- **Mechanism:** Start from an ordinary old success. Let a frozen ancestor propose legal one-step task mutations, retaining branches where it still succeeds and the current policy begins to fail. Deduplicate by checked failure family.
- **Novelty bet (improvement):** An informed lineage-specific mutation order reaches lost regions faster than DeepXplore-style directed disagreement with the same starts, validity checks and verifier budget.
- **Cheapest first test:** Search parameterized grid routes after a navigation curriculum shift; compare against current and sibling proposers and differential search with the same filters.
- **Old-task retention:** Repair with equal numbers of checked cases; score untouched original routes and independently generated detours, plus latest routes.

#### 2. The ancestor as a live opponent, not a replay log
- **Mechanism:** In a cooperative game with legal perturbations, let an ancestor choose moves that expose recovery behavior it can still carry out. Fork each reached state so old and current policies get identical continuations and inference budgets.
- **Novelty bet (primitive candidate):** The paired continuation is a witness of *lost recovery*, not the win/loss payoff of AlphaStar-style leagues or a diff on traces the old policy visited alone.
- **Cheapest first test:** In a tiny delivery simulator, alternate traffic patterns and compare live cross-play with ordinary league sampling and difficulty-matched ancestor trajectories.
- **Old-task retention:** After repair, run normal old delivery episodes and new fork states without an ancestor at execution; check delivery under the newest traffic too.

#### 3. Regressions in what the agent asks
- **Mechanism:** Freeze the ancestor's information-seeking policy and have it challenge the current agent at the first omitted clarification. The environment checks whether its answer could change the optimum at equal query cost.
- **Novelty bet (primitive candidate):** The witness is a decision-relevant *missing query*, not a wrong final answer scored by Regression Bugs or generic asymmetric self-play.
- **Cheapest first test:** In a hidden-goal routing game, vary which observations are normally free; compare to identical final-outcome differential search plus a query-entropy heuristic.
- **Old-task retention:** Check untampered old episodes for net payoff after query costs and correct clarifications on unseen goals, as well as payoff on the latest regime.

#### 4. Margin-matched exchanges of task roles
- **Mechanism:** The ancestor proposes pairs of role permutations that should preserve a rule but change superficial cues. Seek pairs the old version handles in both directions and whose current failure is sharply asymmetric.
- **Novelty bet (improvement):** Ancestor-chosen permutations reveal a specific symmetry lost in training beyond CheckList invariance pairs selected at random or by current-model confidence.
- **Cheapest first test:** Train small classifiers on successive relational table tasks; use the same grammar and margin bins in all search arms.
- **Old-task retention:** Evaluate clean old tables and held-out role permutations after a matched update, alongside tables from the latest curriculum.

#### 5. Discontinuous failures inside a task family
- **Mechanism:** Freeze an old policy to bracket a range where it stays competent, then use the pair to search for pockets where current competence vanishes and returns. Issue a bracketed witness with two nearby current passes, not just the failure.
- **Novelty bet (improvement):** Boundary shape makes sparse holes cheaper to locate than DeepXplore-style point disagreement or MIR selection from the same pool.
- **Cheapest first test:** Enumerate a small scheduling domain with a nuisance parameter, then compare budgeted search against the exhaustive map; allow holes in all arms, don't assume one transition.
- **Old-task retention:** Compare matched repair on independent normal old schedules and novel parameter grids, not on the mined brackets alone.

### B. Turn disagreement into a usable verdict

#### 6. Debate the regression, not the answer
- **Mechanism:** An ancestor claims a loss and submits a witness. The current version can object that the case is invalid, the check is incomplete, or both answers pass. The only accepted ruling is a checked trace or a validated counterexample.
- **Novelty bet (primitive candidate):** The debated proposition is a regression across versions; unlike self-play debate, no judge preference is counted as truth, and unlike a single diff the defense can invalidate the claim.
- **Cheapest first test:** In a toy logic-task stream with multiple valid outputs, compare two-round debate with one-shot DeepXplore-style diff plus the same verifier calls, including an automated validity filter.
- **Old-task retention:** Train on accepted claims at equal update cost and measure unchanged old rules on untouched problems; separately test intended new behavior that the old policy disputes.

#### 7. Paired interventions to distinguish inaccessible from lost
- **Mechanism:** At an observed negative flip, have the ancestor propose a legal missing intermediate observation. Give it to *both* policies in a separate replay; separate failures fixed by that observation from failures persistent under it.
- **Novelty bet (primitive candidate):** A paired intervention witnesses which part of a chain to repair rather than using SPC-style free-form critiques or automatically cloning the old trajectory.
- **Cheapest first test:** Compare intervention-chosen repairs with scripted one-factor ablations and trace replay in a small route planner with separable sensing and planning.
- **Old-task retention:** Score ordinary old routes without supplied observations and report sensing and planning slices, then score new routes.

#### 8. Two ancestors cross-examine the same claim
- **Mechanism:** One old policy brings a witness; another chooses a same-spec transformation that should preserve the alleged loss. The checker can accept the original claim but reject its proposed scope.
- **Novelty bet (primitive candidate):** The second checkpoint acts as a falsifier of the first's generalization, not an ensemble judge as in self-rewarding or a historical opponent sampled for difficulty.
- **Cheapest first test:** In a table reasoning stream with alternating formats, compare independent cross-examination to same-ancestor resampling and CheckList transforms at fixed cost.
- **Old-task retention:** Repair at the accepted scope and measure ordinary old tables, unseen formats in scope, neighboring old formats out of scope, and the newest format.

#### 9. A witness for the first consequential divergence
- **Mechanism:** An ancestor and current policy replay the same deterministic start; branch at candidate decisions with a common continuation or an exact little solver. Mark the earliest choice at which the attainable outcome drops, not the first lexical or action disagreement.
- **Novelty bet (primitive candidate):** A version-paired causal turning point is a stronger repair target than SPC step critiques or comparing entire prefixes; harmless alternate actions must survive.
- **Cheapest first test:** Use a tiny warehouse planning graph and compare matched supervision on decisive branches, first disagreements and terminal-only DER.
- **Old-task retention:** Evaluate independent normal old plans and long old plans with different turning points; also test latest warehouse maps.

#### 10. Silent losses behind successful outcomes
- **Mechanism:** Ask an ancestor to find two equally valid plans where the current strategy has stopped keeping a required reserve (time, fuel or capacity), then demand a legal continuation that consumes that reserve.
- **Novelty bet (primitive candidate):** The continuation certifies a latent regression in robustness despite an identical nominal pass; must beat CheckList stress tests combined with ordinary differential fuzzing.
- **Cheapest first test:** Use budgeted delivery with optional delays; match stress level and continuation-generation calls across auditors.
- **Old-task retention:** Check old nominal deliveries and unseen old delay patterns before and after matched repair, plus latest delivery efficiency.

### C. Organize the archive without making its votes authoritative

#### 11. Select the archive for disagreements it can find
- **Mechanism:** Keep checkpoints by their marginal yield of distinct verified failure families on rotating development releases, not by recency, performance, or output diversity alone.
- **Novelty bet (improvement):** Archive slots buy complementary *discovery* rather than the opponent diversity of PSRO; test whether frozen curated cases cover the same failures more cheaply.
- **Cheapest first test:** Pick two of six small grid policies, then measure transfer of the selection onto held-out shifts against equal-byte chronological checkpoints, diversity selection and a verified case buffer.
- **Old-task retention:** Rehearse the found cases and assess unseen normal episodes from all earlier curricula, including those whose checkpoints were dropped.

#### 12. Audit the spaces where no ancestor can testify
- **Mechanism:** Keep a map of old task families that have evidence of past competence but no surviving checkpoint able to witness a fresh failure. Route those families to checker-labeled probes instead of treating the archive's silence as evidence of retention.
- **Novelty bet (primitive candidate):** An explicit distinction between "checked and clean" and "no eligible witness" makes archive survivorship actionable. Unlike CheckList coverage alone, it distinguishes a sampled family that cannot produce an eligible witness from one that can.
- **Cheapest first test:** Drop checkpoints under a small byte cap in a three-curriculum scheduling stream; use the same family metadata and probe budget for the map, a CheckList coverage baseline, and lowest-current-confidence search.
- **Old-task retention:** Spend matched repair budgets and measure ordinary old schedules from both witnessed and witness-missing families, plus the newest schedules.

#### 13. Non-transitive chains of forgetting
- **Mechanism:** Build a directional edge only when one version exposes verified losses in another that it can solve itself. Allocate audits to close three-version cycles where every version can still expose something another has lost.
- **Novelty bet (primitive candidate):** The useful graph is over evidenced task regressions, not a league payoff matrix. It must beat the same PSRO scheduler plus positive-congruent replay when edges carry generic scores.
- **Cheapest first test:** In a small multi-skill stream with repeated tasks and naturally competing gradients, compare cycle coverage scheduling to mean yield, graph-free family coverage and latest-only scheduling.
- **Old-task retention:** Report normal old accuracy per cohort after identical repair effort; a gain on cycle edges must not cost uncited cohorts or new tasks.

#### 14. Stale ancestors as negative controls
- **Mechanism:** Run one challenger known to have trained under a retired rule beside a same-lineage witness of a still-valid skill. Require the audit pipeline to reject obsolete objections while admitting verified losses with similar confidence.
- **Novelty bet (improvement):** This tests the false-alarm mechanism of ancestry-guided search rather than transferring world knowledge (Fossil Beliefs) or averaging temporal self-rewarding preferences.
- **Cheapest first test:** Change one tie-breaking rule but keep all underlying scheduling constraints; compare calibration to a rule filter plus skepticism prompt without the stale challenger.
- **Old-task retention:** After using accepted witnesses, check old rules that remain valid and old tasks explicitly specified as historical; verify the new default does not revert.

#### 15. Reserve a secret lineage jury
- **Mechanism:** Split each version family into public audit opponents and hidden frozen auditors, and reveal neither hidden prompts nor cases during updates. Rotate hidden auditors as the curriculum changes.
- **Novelty bet (improvement):** Tests whether public repair changes the policy or merely teaches it to recognize particular critics; held-out examples from public critics and ordinary self-play league evaluation are the controls.
- **Cheapest first test:** Give tiny planners shared public and secret challenger distributions with matched difficulty and disjoint seeds; induce several rounds of public repair and measure the gap.
- **Old-task retention:** Run independent ordinary old tasks without any auditor tokens; compare those results with secret-auditor failures and newest-task success.

### D. Learn from the contest without copying the contestant

#### 16. Counterexample escrow over several releases
- **Mechanism:** Use part of each new release's audit budget to retest prior *families* of repaired regressions with mutations proposed by their original witnesses. Retire a family only when fresh variants stop failing.
- **Novelty bet (improvement):** This tests repair durability against change, beyond MIR on previously failed examples and CheckList reruns of fixed cases.
- **Cheapest first test:** Run three curriculum shifts for a small sequence transducer; compare live remutation with a fixed regression suite plus equally many random family variants.
- **Old-task retention:** Score independent ordinary old sequences at every round and time until losses recur, while holding newest-task acquisition comparable.

#### 17. Bid for training budget with verifiable failures
- **Mechanism:** Give each frozen auditor a small calibration quota of verification attempts. Allocate the next round's search-and-repair budget by the number of fresh, validated families those bids add beyond the replay pool, with an exploration floor; test whether that small sample actually predicts useful additional cases.
- **Novelty bet (improvement):** Targets marginal diagnostic novelty under a real repair budget. Compare to uniform sampling plus deduplication, MIR, and prioritized generative replay on the same generated candidates.
- **Cheapest first test:** Train a small model on alternating sequence tasks and measure retention gained per checked case by the bidding versus pooled selection arms.
- **Old-task retention:** Use untouched normal cases from all old tasks, including frequent tasks whose individual failures rarely earn a bid; track new-task gain.

#### 18. The defense can submit a better solution
- **Mechanism:** When the ancestor claims a successful trace is invalid because it departed from an old method, let the current policy rebut with a checker-accepted alternative at the original task budget. Store the pair as a boundary case: preserve the alternative where it works, repair only independently verified failures of it.
- **Novelty bet (primitive candidate):** Bids admit verified alternatives and produce paired evidence about when the new strategy works; Temporal Self-Rewarding's cross-version preferences and LwF both serve as controls, as does direct verified self-training.
- **Cheapest first test:** Use small arithmetic expression problems with multiple valid derivations; compare matched updates on verified rebuttals, current-only self-training, and ancestor targets.
- **Old-task retention:** Check normal old problems and unseen families with alternate solutions, and measure efficiency on new problems.

#### 19. Refute a repair with its nearest collateral loss
- **Mechanism:** Once a candidate fix passes the original witness, the ancestor gets a small search budget to find a nearby old task that the *unrepaired current policy* passed but the repaired one fails. Compare repairs on both findings.
- **Novelty bet (primitive candidate):** This is a contest over candidate repairs, not a one-way historical regression test; must beat repair selection using Regression Bugs scoring, hard replay and an equally budgeted static neighborhood audit.
- **Cheapest first test:** In a table classifier, compare a few repair batches or update strengths after one shift, with common candidate repairs and matched post-update audits.
- **Old-task retention:** Choose on audit evidence only; assess normal old tables and hidden nearby families, plus new-task performance.

#### 20. Preserve recovery from one's own mistakes
- **Mechanism:** Let a frozen earlier version propose legal wrong first moves it used to recover from. Route identical perturbed states to both policies and train only when the old policy demonstrably recovers and the current one cannot.
- **Novelty bet (improvement):** Adversarial replay of self-induced recoverable mistakes differs from Card 2's *external* opponent and from ordinary DGR of good trajectories; compare to current-policy error replay plus random, severity-matched perturbations.
- **Cheapest first test:** In an undo-capable puzzle, identify reachable error states without requiring the old action to be the unique path there; match remaining horizon.
- **Old-task retention:** Test standard old puzzles from unperturbed starts and off-policy recovery from fresh mistakes, plus new puzzles.

#### 21. Teach the current version to pose the challenge it missed
- **Mechanism:** After repairing the task, also train the current auditor role on the ancestor's *choice of discriminating experiment*, not the old answer. Retire the ancestor and see whether the trained auditor exposes a different regression in the next version.
- **Novelty bet (primitive candidate):** The object under retention is the ability to discover future loss, distinct from self-quizzing replay and SPC's co-trained reasoning critic. Equal-budget direct distillation of a generic test generator is the critical control.
- **Cheapest first test:** Use a finite mutation grammar over rule puzzles and a tiny trainable proposer; train on only one release's audited families, evaluate across two unseen shifts.
- **Old-task retention:** Check ordinary old puzzle solving after auditor training and measure old-family discovery on unseen puzzles, plus latest puzzle solving.

#### 22. Constrain releases by a blind challenge budget
- **Mechanism:** Compare candidate releases on a fixed blind batch of old-task challenges selected by ancestry witnesses. If a candidate crosses a predeclared failure threshold on the batch, use a separate budget for diagnosis and repair or defer the update; a repaired candidate must face fresh blind challenges.
- **Novelty bet (improvement):** The bet is that active historical discovery improves a real release decision beyond negative-flip gating on fixed tests plus matched directed fuzzing; abstaining forever is not success.
- **Cheapest first test:** Simulate a short stream of small routing-policy releases; compare at equal verification cost and equal opportunity to adopt new skills, charging for deferral.
- **Old-task retention:** Track normal old route success across the entire stream, conditional negative flips for accepted releases, and delayed access to the latest routing tasks.

## Ranked deeper sub-questions

1. **Does shared lineage buy anything once search resources are matched?** Start with 1–3. Compare an actual ancestor with unrelated and sibling policies matched on old competence, and with the same ancestor performing passive replay. If directed search using those controls finds the same families at the same cost and yields the same retention, drop the special role for ancestry.
2. **What kind of witness supports a repair that generalizes?** Compare case, omitted query, and first consequential divergence (3, 7, 9, 10) against equal-cost whole-case replay. Measure whether the witness raises held-out ordinary retention or just makes failure diagnoses more legible.
3. **What should survive in a fixed-size audit archive?** Compare executable challengers, cached cases and distilled search policies (11–13, 21) in fresh rounds. A live archive deserves space only if it finds something the best same-byte artifacts cannot.
4. **Can successive repair rounds preserve both current gains and the ability to discover loss?** Use independent auditors and changed-rule controls (14–16, 19, 22). Separate feigned improvement on seen audits, repairs that just relocate errors, and intentional replacement of old behavior.
