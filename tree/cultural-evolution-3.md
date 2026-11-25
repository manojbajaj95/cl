# Cultural Evolution 3: Common Writes and Edits That Carry Their Own Exercise

Child of [cultural-evolution-2.md](cultural-evolution-2.md) ([PR #347](https://github.com/manojbajaj95/cl/pull/347), depth 2) · 26 cards · 4 ranked deeper questions · Ideas only; no GPU or experiments run

**Why this node exists.** The [review of #347, row 474][triage], gave no score 4 and kept two score-3 ideas: **CE2-05**, write only a change supported by every plausible reading of a pending edit, retaining the unresolved part; and **CE2-25**, attach an executable exercise that can settle the unresolved scope even after the learner's affordances change. This node asks what a partial commit leaves possible and what an inherited exercise must recover: evidence that changes a justified weight write, not necessarily the identity of the author’s intended rule.

**Literature check.** Hugging Face Papers and targeted web discovery were followed by checks of the linked abstracts or text. [Trans-LoRA][trans] distills a fitted source adapter to a new base using synthetic inputs derived from a small demonstration set. [AlphaEdit][alpha] projects a perturbation into the null space of preserved knowledge keys. [Deep Adaptive Design][dad] amortizes Bayesian sequential experiment choice with an information-gain objective. All three are serious baselines: distill the best fitted source adapter; apply null-space protection to the same keys; give adaptive design the full residual and same action model. More broadly, [decision region determination][drr] already asks which decision is justified without first identifying the true hypothesis. Neither robust editing, decision-aware querying nor their simple combination is new. As in the [idea ledger][ledger], **PRIMITIVE** labels a candidate reusable object or operation, not a priority claim; an equally resourced replay, optimization or active-learning solution may tie.

## Shared fixtures and checks

- **W · Common write.** Fit a small encoder and head on old tasks A and rare B. Collect a proposal C under an old coarse representation, put it in a queue, and learn a fine distinction from independent data S. Example: both plausible readings of C correct a shared return-routing mistake, but only one authorizes an extra decision for defective returns. A reading specifies effects it requires, permits and forbids. Enumerate readings in the finite fixture; in a second version fit them from observable proposal evidence and include misspecification, where the real intent may be missing. A raw oracle list is not the result. Start at a linear or tabular head, then use a tiny MLP with an actual rank-constrained adapter or weight update. Report exact feasible sets only where enumerated; verify actual logit changes after finite nonlinear updates.
- **A common write must do something.** Zero or holding C is the safety reference. Predeclare a nonzero beneficial effect or minimum progress before minimizing interference, rank or norm. “Every reading” means every surviving reading, not each posterior mode or their average. If no nonzero edit meeting the effect floor and old floors exists, hold; do not count holding as learning. Carry the residual as constraints on future observable effects and re-evaluate them on the live model, not as unspent coordinates from an obsolete adapter. A common edit, a unique optimal edit, and preservation of every possible continuation are three different claims.
- **Q · Scope exercise.** One or more handoffs change the actions available for learning C. Use finite worlds with common routine observations but different responses to a legitimate intervention; e.g. an explicit inspection disappears and a permitted re-ordering reveals the same distinction. The proposal cannot label the outcome or add an unavailable action. An exercise inherits an executable search or test and a mapping from *observed outcomes* to residual constraints. Include a decoy that predicts author identity, reward, or the simulator's answer without changing which edits are admissible. Final predictions use ordinary inputs with the exercise and teacher removed.
- **Matched controls.** W: refit from raw proposal evidence, Trans-LoRA-style transfer, AlphaEdit with the same preserved keys, most-likely reading, [IRM][irm] with the same environments, robust constrained fitting with the same hypothesis set, and holding. Q: random and optimal adaptive queries, DAD with the same residual, decision-region or value-of-information selection, an equally expressive exercise-only teacher, edit-only, and answer-carrying handoff as an informed reference. Stack the strongest W and Q controls for each combined card. Charge retained bytes, action opportunities, calibration observations, training and validation work, including abandoned attempts and any old model; fix oracle access and the work available *after* observation. Evaluate common progress, wrong commits, false holds and final C/D utility, not exercise success or posterior accuracy alone.
- **Retention in every card.** Use independent, ordinary A/B tests before and after S, at immediate commit or hold, through each handoff, after the exercise and after D/final commit. Exclude deliberately amended decisions only from the unchanged slice; keep the rare unamended analogues. Give no task IDs, old snapshot restores or special channels. Report both per-task and worst drop alongside comparable new behavior; disallow gain from trading off old tasks below a predeclared floor. Every card adds a specific old-task slice.

## A · CE2-05: What can two readings really agree to write?

### CE3-01 · Write a conclusion that neither reading expresses directly — PRIMITIVE
- **Mechanism:** Compile the logical consequences shared by the readings into a behavioral target on the new head. For example, two readings reverse different actions relative to a third but both entail that the third cannot win. Fit that decision inequality without asserting any winner; retain the unsupported pairwise comparison.
- **Nearest prior / gap:** [SoftEdit][soft] edits to a calibrated distribution over plausible outputs, while [decision rules under partial identification][partial] allow decisions without identifying the underlying state. The candidate is carrying an inferred *shared consequence* as an editable commitment, not treating multiple outputs as probabilities.
- **Cheapest first test / control:** Three-action head, opposite top choices with one forbidden action in common. Compare distribution distillation, minimax loss and direct inference followed by constrained logit fitting, all with the same reading descriptions. A tie with the last arm means standard consequence extraction suffices.
- **Old-task retention:** Check rare old cases where the shared forbidden action is legitimate and old near-ties whose winning action should not change.

### CE3-02 · Agree on a correction even when every full solution is different — PRIMITIVE
- **Mechanism:** A common move may improve both readings without equalling any component of their independently fitted optimal deltas. Find it in the image of the current model's edit operator and keep the permissible continuations for each reading, instead of intersecting coordinate masks.
- **Nearest prior / gap:** [MGDA][mgda] finds common descent directions, while [A³E][a3e] can zero opposite-sign entries when merging edits. Neither common descent nor excluding conflicting coordinates is new. The candidate object is a common move paired with its valid continuations after the representation changes.
- **Cheapest first test / control:** Fit two quadratic objectives with distinct optima and an overlapping improving region, then refit the head basis on S. Compare conflict-masked merge, MGDA followed by full replanning, and Trans-LoRA on both endpoints followed by recomputation, at equal residual storage and post-S work.
- **Old-task retention:** Retest A/B in the overlap of their feature supports before and after the common move is completed for one reading.

### CE3-03 · A shared edit can bind one conditional, not either of its facts — PRIMITIVE
- **Mechanism:** If all readings authorize changing a decision when two observable conditions coincide, but disagree outside that intersection, fit a joint-effect constraint on the new adapter. The resulting write must not independently change either condition’s default.
- **Nearest prior / gap:** [Compositional model editing][a3e] targets effects on compositional consequences, and [AlphaEdit][alpha] protects fixed knowledge associations. The candidate is a jointly authorized change with explicit forbidden marginals, which can persist while competing interpretations of the marginal effects remain open.
- **Cheapest first test / control:** Fit a two-feature nonlinear head with XOR-like distractors; run exact constrained refitting and AlphaEdit with joint and marginal anchors. Reject if the proposed artifact adds no transfer or efficiency over the same constraints directly.
- **Old-task retention:** Measure A/B on both isolated features and on old joint conditions not affected by C.

### CE3-04 · Commit a lower bound but keep the upper bound negotiable — PRIMITIVE
- **Mechanism:** For a shared outcome, readings authorize overlapping ranges of effect sizes rather than exact deltas. Commit the smallest observable improvement in their allowed intersection, then keep a bounded residual for later refinement. Keep the scale tied to an observable margin on the live head.
- **Nearest prior / gap:** [Robust baseline regret][regret] optimizes relative to a safe baseline, and [SoftEdit][soft] fits graded targets. The candidate is a transportable *interval commitment* with separate admissibility and progress floors, not a probability average or an accuracy gauge.
- **Cheapest first test / control:** Two strata give overlapping effect intervals on a calibrated logistic head, with a disjoint case as a hold reference. Compare direct robust constrained fitting plus storing intervals, and worst-case risk fitting without explicit range semantics.
- **Old-task retention:** Score old nearby margins and the old task that reacts to overly large changes despite unchanged hard predictions on C.

### CE3-05 · Protect a rare old effect that all readings use differently — PRIMITIVE
- **Mechanism:** Fit a change only if a specified old consequence remains valid *under each authorized continuation*, not merely at the common commit. Store the residual constraint that keeps its possible completions safe, and evaluate it on separate old examples.
- **Nearest prior / gap:** [AlphaEdit][alpha] protects stored associations for a single write, and [safe policy improvement][spibb] falls back to a baseline under uncertainty. Here the same current write must leave safe weight-space completions for multiple interpretations; this can invalidate an otherwise perfectly localized initial edit.
- **Cheapest first test / control:** Tiny head with an A/B-safe first edit whose only cheap completion for one reading flips rare B. Compare a robust two-stage exact solver and AlphaEdit plus lookahead with identical anchors and horizon. The solver provides the representational ceiling.
- **Old-task retention:** Check rare B at zero, first commit and for each possible completion independently, not their average.

### CE3-06 · Write only a change that survives an allowed change of class balance — PRIMITIVE
- **Mechanism:** The readings agree on a behavior only under some mixtures of resolved and unresolved cases. Carry the admissible mixture constraints through the split and require a common weight write to help throughout that range, reserving group-specific effects for later evidence.
- **Nearest prior / gap:** [Group DRO][dro] optimizes worst-group loss; [IRM][irm] targets invariance across environments. This candidate uses a mixture ambiguity set justified by the proposal to decide which *change* transfers, not a general claim that group robustness is new.
- **Cheapest first test / control:** Using a two-stratum head, construct one edit beneficial only at the observed mixture and a different effect valid throughout the stated range. Compare robust refitting with the same groups, same intervals and an equal-data invariant fit.
- **Old-task retention:** Score both original strata separately after S and after the edit, including rare B under its real old sampling distribution.

### CE3-07 · Carry one reason to hold that can be disproved later — PRIMITIVE
- **Mechanism:** If all useful writes are blocked, record a small witness (conflicting reading constraints or an old-task floor) and which observation would remove that blocker. It is a certificate about an attempted *write*, not evidence that C is worthless.
- **Nearest prior / gap:** [Scenario-based adjustable robust optimization][adjust] partitions scenarios to permit later decisions, and [decision region determination][drr] exploits conditions that suffice to decide. This candidate hands down a finite infeasibility witness that names a legitimate future event, so a later solver can distinguish a removable conflict from structural impossibility.
- **Cheapest first test / control:** Enumerate a linear case with two blockers, only one removable by evidence; compare recomputing the linear certificate from the full hypothesis set, storing all blockers, and storing a generic ambiguity flag. Count both storage and false releases.
- **Old-task retention:** Verify the B constraint is still enforced when an unrelated reading is ruled out and C becomes feasible in another region.

## B · CE2-05: The common edit changes what a later edit can reach

### CE3-08 · Commit the common effect in a place that leaves both futures reachable — PRIMITIVE
- **Mechanism:** Two actual low-rank updates have the same sanctioned effect on present tasks, but leave different reachable effects under the next rank-constrained write. Choose a first update with a valid completion for each reading; carry the completion constraints, not inactive rank or a reserved optimizer slot.
- **Nearest prior / gap:** [AdaLoRA][adalora] allocates a finite low-rank budget and [AlphaEdit][alpha] protects existing facts. The candidate is choosing where to place a first common effect by reachability of *specific unresolved reading edits*, rather than importance rank or an optimizer-state mechanism.
- **Cheapest first test / control:** Exact two-layer enumeration over binary rank-1 updates, with one first placement blocking one reading. Compare an adaptive rank allocator, a two-stage robust solver, and storing both completed adapters (charge both). Explicitly test that the difference remains under actual allowed writes.
- **Old-task retention:** Score both old head pathways after the first write and after each continuation; require rare B to pass even in the less likely continuation.

### CE3-09 · A new encoder can make a deferred edit cheaper without changing its meaning — PRIMITIVE
- **Mechanism:** Keep a residual described as differences in behavior across raw contrast classes. When an independent S update makes those differences separable at a single layer, compile the same residual to a smaller adapter instead of transferring the old full patch.
- **Nearest prior / gap:** [Trans-LoRA][trans] transfers fitted task capabilities, and [learnable drift compensation][drift] tracks representations for replay-free classification. The claim is reusing *unsatisfied constraints* in a new write geometry, not transferring task performance or tracking centroids.
- **Cheapest first test / control:** Two encoders with the same ordinary prediction quality but different separation of C's admissible region; wait for one labeled scope outcome. Compare exact raw replay/refitting and distilling a source patch at the same target rank and calibration budget.
- **Old-task retention:** Check old classifier decisions for both contrast classes even when they use the feature the later encoder sharpened.

### CE3-10 · Rebase a residual on the model's actual changed behavior, not the nominal delta — PRIMITIVE
- **Mechanism:** After the first write and an intervening model update, recompute the residual against the *originally licensed observable change* measured on retained comparisons. Accidental gains from S count only where the observable constraint actually holds; no arithmetical subtraction of old adapter factors.
- **Nearest prior / gap:** [Tangent task arithmetic][tangent] improves parameter-space compositionality, and [Trans-LoRA][trans] targets behavior in a new model. Here the residual is an outstanding obligation to meet a scoped effect after ordinary learning, not a task-vector difference.
- **Cheapest first test / control:** A nonlinear two-layer fixture where vector subtraction misestimates second-step effect; compare function-space refitting from the original raw request, target-effect subtraction, and exact finite recomputation, matching the reference examples and byte budget.
- **Old-task retention:** Retest A/B on cases with accidental gains from S and cases where first and later effects cancel despite similar parameter norms.

### CE3-11 · Let future evidence license a new composition, not a larger copy of the first write — PRIMITIVE
- **Mechanism:** Carry the normalized *relationship* the next edit must have to the committed change: e.g. in one region the new edit must preserve the correction while adding a distinct action, in another it must supersede its effect. The relationship becomes a constraint even if subsequent evidence selects a different implementation.
- **Nearest prior / gap:** [A³E][a3e] checks edited facts and their compositions; [O-Edit][oedit] protects sequential edits via subspace separation. This candidate transports an explicit contract for how one still-unknown correction may alter another's behavioral effect.
- **Cheapest first test / control:** In a toy two-layer head, two prospective completions match all individual targets but differ on a composition. Compare joint constrained editing on the same relation labels, independent O-Edit-style edits, and full replay at equal budget.
- **Old-task retention:** Measure unamended old compositions and ordinary inputs after both writes, including the rare pair sharing an intermediate feature.

### CE3-12 · Split one residual when independent evidence can finish its pieces — PRIMITIVE
- **Mechanism:** Separate a residual into independently resolvable obligations only when each possible completion of one leaves eligible completions for the other at the live rank budget. New evidence then authorizes one write without implicitly choosing another.
- **Nearest prior / gap:** [Adjustable robust optimization][adjust] represents decisions that adapt to scenario partitions; [MEMIT][memit] edits many associations together. The novelty candidate is a test for *independent authorization and realizability*, which may disagree with factorization of the evidence.
- **Cheapest first test / control:** Create one independent linear pair and one nonseparable pair sharing a rank-1 cap. Compare a full joint robust solver with equivalent factorization, and separately fitted scopes with identical stored examples and rank allowances.
- **Old-task retention:** On both evidence orders, check A/B after the first resolution and after both writes, especially the old behavior backed by the shared direction.

### CE3-13 · Merge two residuals only if either author can still decline their half — PRIMITIVE
- **Mechanism:** If two queued edits have a safe common effect, write it once and keep two separate withdrawal or narrowing conditions. The committed effect must remain justified by live evidence if either proposal recedes; otherwise its supporting constraints require recompilation.
- **Nearest prior / gap:** [Rational belief revision for model editing][belief] distinguishes knowledge revision from isolated replacements, while [verified three-way merge][merge] preserves behavioral changes from separate parents. The claimed object is a parametric common write with separable support from distinct pending requests, not a general merge algorithm.
- **Cheapest first test / control:** Two sources justify the same action now; one later reveals important exceptions. Compare provenance-tagged raw replay and constrained re-editing against the proposed residual structure at matched bytes and corrections. Include a case where a full retain-current edit would be wrong.
- **Old-task retention:** Check old outcomes that depend only on the unaffected source and old default cases that the now-narrowed combined edit should not displace.

## C · CE2-25: An exercise should resolve a write, not just an interpretation

### CE3-14 · Ask whether the admissible write changes, not which reading is true — PRIMITIVE
- **Mechanism:** Attach an exercise for which at least one possible legitimate result removes all barriers to a useful weight write. It can leave multiple latent readings unresolved if they agree on one safe action and required effect.
- **Nearest prior / gap:** [DAD][dad] optimizes sequential information gain; [decision region determination][drr] already targets the decision without identifying hypotheses. This is a CL instantiation only unless the mutable, overlapping *sets of feasible parameter writes* make an inherited description cheaper or more reusable than explicit decision-region planning.
- **Cheapest first test / control:** Give three readings, two with several viable edits in common and one that blocks all nonzero writes. Let a high-entropy query distinguish the first two while a lower-entropy query separates out the blocker. Compare exact decision-region design, information-gain DAD, and DAD trained for the same feasible-write objective.
- **Old-task retention:** Check old cases adjacent to every actually installed edit, including a rare case each reading would allow the model to preserve differently.

### CE3-15 · Let outcomes supply inequalities, not names of readings — PRIMITIVE
- **Mechanism:** The handoff carries an exercise whose observed ordinal outcome directly bounds permitted changes in a pair of logits. The successor can refine its feasible write region even when the old vocabulary no longer names the true interpretation; no outcome is decoded into a full intent label.
- **Nearest prior / gap:** [Knowledge Gradient for binary feedback][kg] learns from binary outcomes to choose a decision, and [SoftEdit][soft] supplies graded model-edit targets. The candidate is an exercise returning an observable constraint to a pending low-rank edit, rather than selecting a known hypothesis or receiving the end answer.
- **Cheapest first test / control:** Let two reward orderings support the same partial edit but permit different extension magnitudes. Compare ordinal supervision plus constrained refit, and decision-aware experimental design given the same observation likelihoods. Hold out a changed observation channel whose ordering is still usable.
- **Old-task retention:** Check unamended orderings near the ordinal boundary; retain A/B calibration as well as hard decisions.

### CE3-16 · Ask whether the apparent disagreement is implementable at all — PRIMITIVE
- **Mechanism:** An exercise has one arm for obtaining a scope outcome and another for finding a legitimately distinguishable feature with which to implement it. If the latter fails, a scope answer does not authorize a weight write that changes unrelated cases.
- **Nearest prior / gap:** [DAD][dad] plans experiment sequences and [AlphaEdit][alpha] restricts feasible parameter changes. The proposed artifact makes a write's *realizability* a decision variable for the sequence, rather than asking scope questions whose answer cannot change the live model.
- **Cheapest first test / control:** In a finite two-layer model, a single allowed anchor can distinguish two cases formerly mapped to the same feature. Compare joint goal-oriented design with the same anchor candidates and budget; test also a cell where no permitted feature can separate the cases.
- **Old-task retention:** Check A and B cases that were indistinguishable from the proposed C target until the feature was elicited.

### CE3-17 · Learn an exercise that knows when its question has stopped making sense — PRIMITIVE
- **Mechanism:** The artifact separates a test action from its enabling assumptions, such as the action changing order without changing material. A successor can test those assumptions with ordinary feedback; if false, it either remakes the experiment or leaves C pending without calling an uninterpretable outcome a label.
- **Nearest prior / gap:** [Goal-oriented sequential causal design][goal] targets relevant causal information; [SafeOpt][safeopt] restricts exploration to a safe set. The candidate is a transported validity condition on the *meaning* of an experiment outcome, distinct from action safety.
- **Cheapest first test / control:** Change an actuator so a previously separating intervention also affects a nuisance variable. Compare learner-fitted causal design with the same paired runs, hand-fixed invariants and a random exercise. Include a false-negative check where the intervention remains valid.
- **Old-task retention:** Check old tasks depending on the nuisance variable after the exercise, whether or not a write occurred.

### CE3-18 · Carry a case every reading agrees on as a negative control — PRIMITIVE
- **Mechanism:** A pending edit carries an intervention and a negative-control case on which every reading predicts the same scope result. A successor only converts an observed separation into an edit constraint if the negative control still passes after remapping the intervention.
- **Nearest prior / gap:** [Mutation-guided test generation][mutation] uses alternative behaviors to discriminate tests, and [goal-oriented experimental design][goal] targets relevant distinctions. The candidate binds a *non-discriminating* countercase to the decoding of evidence for a later weight edit.
- **Cheapest first test / control:** Two intervention remappings give the same predicted split but one introduces an unrelated shortcut on the negative control. Compare joint causal experiment design with an equivalent paired-quality constraint and the same outcomes; also test noisy negative controls so the method cannot win by holding everything.
- **Old-task retention:** Test both the old family used for the negative control and novel old examples that only share its nuisance feature.

### CE3-19 · Rebuild the exercise by matching what it can authorize — PRIMITIVE
- **Mechanism:** Two exercises can have different outcomes and trajectories yet induce the same partition of feasible next writes. Allow a successor to rewrite the exercise to a cheaper local one if its legitimate outcomes resolve the same actionable distinctions, including “keep pending.”
- **Nearest prior / gap:** [Decision region determination][drr] groups hypotheses that support the same decision; [symmetric edit lenses][lenses] transport changes between interfaces. The candidate is replacement of an experiment based on the write decisions its outcomes justify, not observation-level equivalence.
- **Cheapest first test / control:** Enumerate three actuator choices whose outcome names differ and whose induced regions either agree or only appear to agree on the first two readings. Compare full decision-equivalence enumeration, adaptation by a learned channel map, and DAD built from scratch with the same evidence.
- **Old-task retention:** Check old A/B after remaking and running the exercise, including inputs whose harmless decoy outcomes should never authorize edits.

### CE3-20 · Teach a second successor to rebuild the exercise without settling its result — PRIMITIVE
- **Mechanism:** A successor may test whether it can express the experiment under its affordances but may not expose the actual resolving outcome to the next learner. It instead passes a revised exercise and residual, so later legitimate evidence can settle scope in a changed setting.
- **Nearest prior / gap:** [Artificial Generational Intelligence][agi] learns across lifetimes and [DAD][dad] builds adaptive experiment policies. The hypothesis is inheritance of a *prospectively repaired experiment* that keeps its pending question intact, rather than transmitting a source posterior labeled on the old action model.
- **Cheapest first test / control:** Three generations with two actuator substitutions, the first allowed to map actions but unable to see final outcomes. Compare answer transfer, reusable goal-oriented design, and a meta-learned teacher at identical cumulative action and fitting cost; include a sham trial that leaks the correct branch from exercise coding.
- **Old-task retention:** Retest A/B in every generation, including old skills exercised by the replacement action even though they never supply scope evidence.

## D · CE2-05 × CE2-25: The edit and exercise must beat their separately optimized parts

### CE3-21 · Choose a common write that preserves the power of its own experiment — PRIMITIVE
- **Mechanism:** A common write can change what the deployed policy subsequently does and therefore which ordinary observations are available. Of two equally useful first edits, choose one that leaves a legitimate scope experiment reachable for every still-plausible reading.
- **Nearest prior / gap:** [Safe policy improvement][spibb] conservatively changes behavior, and [goal-oriented sequential design][goal] selects informative actions. The candidate makes preservation of a specific experiment's feasible outcomes a constraint on the first **weight write**, not just a preference over what experiment to run later.
- **Cheapest first test / control:** In a toy dispatched workflow, two eligible edits fix the same error but one stops visiting the only state where C can be disambiguated. Compare staged robust edit plus DAD and an exact joint two-stage controller given the same trajectories, observations and first-write constraints. Demand equal immediate C benefit.
- **Old-task retention:** Check rare old paths that share the useful state, and retest A/B after each resulting completion.

### CE3-22 · Commit the common part first only if the new observations still mean the same thing — PRIMITIVE
- **Mechanism:** An exercise may depend on ordinary inputs or actions whose distribution shifts after the common commit. Attach an applicability condition relative to the live policy and a plan to repair the contrast when it ceases to be valid, rather than treating feedback under both policies as exchangeable.
- **Nearest prior / gap:** [Performative Prediction][perform] studies model-induced data distributions, and [DAD][dad] adapts experiment choices to observations. The candidate is an exercise whose evidential validity is explicitly amendable when its own partial edit changes the data-generating policy.
- **Cheapest first test / control:** Make the first edit change which flow reaches an intervention, reversing a naive scope estimate without changing true intent. Compare a correct policy-dependent causal design with the same transition model and off-policy observations, and always-query-before-write. Include a regime unaffected by the commit.
- **Old-task retention:** Test ordinary old cases that still use the original flow as well as low-frequency cases newly exposed by the candidate commit.

### CE3-23 · Couple the query budget to which old-task floor actually binds — PRIMITIVE
- **Mechanism:** A residual can be infeasible because of ambiguity about C or because of uncertainty about retention near a rare old condition. The pending edit can carry two experiments and choose the first whose admissible result could enable a safe nonzero write, rather than gathering scope evidence for a physically blocked effect.
- **Nearest prior / gap:** [AlphaEdit][alpha] protects preserved keys and [information-theoretic safe optimization][safebo] selects informative experiments while accounting for safety constraints. The narrow candidate is a residual with two evidence channels and predictable transfer after its validity conditions change.
- **Cheapest first test / control:** Alternate a true scope blocker with an uncertain rare B blocker. Give the exact constrained value-of-information planner access to both experiments, and compare a context-conditioned design that sees the same constraints. Require one informative interaction to advance C without consuming the independent retention test.
- **Old-task retention:** Keep a separate rare-B holdout distinct from any protection observation, and test it after the immediate write and later resolution.

### CE3-24 · Pack the same resolving outcome for two edits only if they can both use it — PRIMITIVE
- **Mechanism:** Two queued edits can share an exercise when one result resolves their distinct required constraints and permits a realizable composition. If it helps each alone but forces incompatible writes, retain it as separate evidence rather than claim two edits for one observation.
- **Nearest prior / gap:** [Multi-target causal design][multi] selects interventions for multiple targets and [MEMIT][memit] fits many edits jointly. The candidate uses the joint write feasibility *after each possible outcome* to decide whether a common inherited exercise suffices.
- **Cheapest first test / control:** Build two tiny proposals that share a separating intervention, with either compatible or incompatible rank-1 completions. Compare stacked batch editing plus exact joint experiment design and separate exercises at matched full budgets. Score partial success explicitly.
- **Old-task retention:** Check A/B after each edit and after the composition, especially an old example influenced by both edits but absent from either teacher’s examples.

### CE3-25 · Ask for a result that can survive the next representation change — PRIMITIVE
- **Mechanism:** When two exercises authorize the same current write, prefer the one whose observed relationship is expressible in a later model without the soon-to-be-absent learning action. Carry an observable contrast underlying the authorization, not the actuator or the frozen proposed delta.
- **Nearest prior / gap:** [Trans-LoRA][trans] uses synthetic examples to transfer an already-fitted adapter, and [intervention design][sim2real] chooses interventions for learned invariance. The candidate is a future-usable evidence object that can authorize another compile of a pending change, not a test-time invariant prediction or tokenizer change.
- **Cheapest first test / control:** Two exercises yield equal immediate scope accuracy, but only one yields paired raw comparisons reusable after a new encoder learns D. Compare raw replay with optimally chosen retained anchors plus design optimized for both stages, given the same forecast of allowed shifts and total observations.
- **Old-task retention:** Check original A/B both at the first post-exercise commit and after D, including a rare case distinguishable only via the surviving comparison.

### CE3-26 · Let the next real task supply the experiment outcome, if it genuinely can — PRIMITIVE
- **Mechanism:** A residual carries a description of an observation that could settle scope. Before allocating a dedicated exercise, arrange a normal permitted next task so it supplies the same contrast as part of useful work. Use it as authorization only if its factual conditions match; otherwise run the exercise or hold.
- **Nearest prior / gap:** [Knowledge Gradient][kg] values observations by their downstream decisions, and [DAD][dad] learns adaptive test selection. Using routine observations is not novel by itself. The candidate is a portable substitution between an active experiment and an already-due interaction that yields the same write evidence with different opportunity costs.
- **Cheapest first test / control:** In a two-task fixture the learner can complete D in two equal-cost ways, one exposing the same result a separate C exercise would reveal. Compare joint value-of-information planning with the same task routes and deadline, immediate dedicated querying, and purely passive learning. Include a version where selecting the route biases the answer.
- **Old-task retention:** Check old D-like tasks that may not be rerouted and old A/B examples that appear to supply the contrast but must not cause the pending write to fire.

## Ranked deeper questions

1. **Can a useful common weight write preserve both future completions and the experiment needed to choose between them?** Start with CE3-05, CE3-08 and CE3-21. Construct two equally good localized writes, with only one preserving a legitimate experiment and both rank-limited completions. Compare stacked AlphaEdit, robust replanning and DAD given the same evidence, then a joint finite solver. A gain over a myopic fit is not enough; show an information, storage or compute trade-off against the joint baseline at the same A/B floor.
2. **What evidence is sufficient to authorize a write after the affordance changes, without identifying the original reading?** Start with CE3-14, CE3-17 and CE3-19. Give decision-region design and DAD the true decision objective where enumerable. Look for a reusable representation that protects against false release in a new actor’s observation channel, not a win from using entropy as the only control.
3. **What is the smallest residual that can be safely recompiled on a changing model?** Start with CE3-02, CE3-09 and CE3-10. Match retained bytes to raw evidence and Trans-LoRA-style transfer. Test whether the shorter residual preserves later consistency, especially where distinct source interpretations yield the same first write but different requirements after S and D.
4. **When can later useful work replace a dedicated exercise without weakening the evidence?** Start with CE3-23–CE3-26. Vary query opportunity cost, old-task constraints and correlations introduced by selecting routes; require the proposed mechanism to beat the edit-plus-design stack at both C and D while retaining A/B. Include a cell where no ordinary interaction can settle the scope.

[triage]: https://github.com/manojbajaj95/cl/blob/5ef6f6a29949430afe68a8f33901edae1a4584ee/reviews/flood-triage.md#L474
[ledger]: https://github.com/manojbajaj95/cl/blob/5ef6f6a29949430afe68a8f33901edae1a4584ee/reviews/idea-ledger.md
[trans]: https://arxiv.org/abs/2405.17258
[alpha]: https://arxiv.org/abs/2410.02355
[dad]: https://proceedings.mlr.press/v139/foster21a.html
[drr]: https://proceedings.mlr.press/v33/javdani14.html
[irm]: https://arxiv.org/abs/1907.02893
[soft]: https://arxiv.org/abs/2611.20562
[partial]: https://arxiv.org/abs/2111.04926
[mgda]: https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.1016/j.crma.2012.03.014/
[tangent]: https://arxiv.org/abs/2305.12827
[a3e]: https://proceedings.neurips.cc/paper_files/paper/2025/file/3d4c0a618d0acd7921493e4f30395c22-Paper-Conference.pdf
[regret]: https://arxiv.org/abs/1607.03842
[spibb]: https://proceedings.mlr.press/v97/laroche19a.html
[dro]: https://arxiv.org/abs/1911.08731
[adjust]: https://arxiv.org/abs/1805.10079
[adalora]: https://arxiv.org/abs/2303.10512
[drift]: https://arxiv.org/abs/2407.08536
[oedit]: https://arxiv.org/abs/2410.11469
[memit]: https://arxiv.org/abs/2210.07229
[belief]: https://arxiv.org/abs/2406.19354
[merge]: https://www.microsoft.com/en-us/research/publication/verified-three-way-program-merge/
[kg]: https://proceedings.mlr.press/v48/wangb16.html
[goal]: https://arxiv.org/abs/2507.07359
[safeopt]: https://proceedings.mlr.press/v37/sui15.html
[mutation]: https://arxiv.org/abs/2506.02954
[lenses]: https://repository.upenn.edu/cgi/viewcontent.cgi?article=3300&context=edissertations
[agi]: https://arxiv.org/abs/2406.00392
[perform]: https://proceedings.mlr.press/v119/perdomo20a.html
[safebo]: https://jmlr.org/papers/volume27/23-1687/23-1687.pdf
[multi]: https://arxiv.org/abs/2302.10607
[sim2real]: https://arxiv.org/abs/2012.02055
