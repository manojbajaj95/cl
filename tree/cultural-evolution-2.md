# Cultural Evolution 2: Pending Edits and Inherited Exercises

Child of [root-cultural-evolution.md](root-cultural-evolution.md) ([PR #343](https://github.com/manojbajaj95/cl/pull/343), depth 1) · 26 cards · 4 ranked deeper questions · Ideas only; no GPU or experiments run

**Why this node exists.** The [review of #343, row 469][triage], kept two score-3 candidates: **CE07**, translate pending changes when a learner's vocabulary changes and leave ambiguous proposals unresolved; and **CE21**, hand down an exercise that can be remade under changed affordances, not its solution. This child puts both claims on the learner's weights. Can a proposal made against yesterday's representation still constrain a write to today's model? Can a chain transmit an interaction that teaches a student to make a useful weight update even when the originating demonstrations are no longer executable?

**Literature check.** Hugging Face Papers searches and targeted web searches were checked against arXiv and publisher abstracts or available text. [Heirloom][heirloom] transports personalization across base-model generations, [Trans-LoRA][translora] transfers already-fitted adapters, and [learnable drift compensation][drift] tracks old class prototypes as representations change. Transfer to a new base and drift tracking are not new. [PAIRED][paired] generates environments through agent regret, [Generative Teaching Networks][gtn] generate data for training new networks, and [Artificial Generational Intelligence][agi] already combines exploration and transmission across lifetimes. Neither synthetic curricula nor cultural chains are new. As in the [ledger][ledger], each **PRIMITIVE** is a candidate reusable object or operation, not an assertion of priority. A tie against the strongest matched baseline means there is no distinct mechanism shown by that test.

## Shared fixtures and decision rules

- **M · Pending write.** Fit a small CPU encoder and classifier on A and rare B. Collect an independently supervised proposed change C, hold it uncommitted, and update the encoder on an independent stream S. S can change which latent distinctions the encoder represents, not the tokenizer or the public input format. Use a finite table or linear network to prove the smallest separation, then a tiny MLP and SGD or a rank-1 update to test a learned (not oracle-assigned) split. For concreteness, C originally groups two kinds of returns; S learns to distinguish voluntary and defective returns. A C proposal might intend both, only one or no safe commit yet; hide this scope unless legitimately identified. Separate what to change, where it now applies, and whether current weights can express it. The old model may be used to write a proposal but is not free to retain. Look for C generalization to unseen examples, and a subsequent D write or read as specified. Score wrong commits and false holds separately so abstention alone cannot win.
- **M controls.** Compare raw C evidence replay and refitting on the new base, learned representation mapping followed by ordinary proposal resubmission/validation, a functional or adapter transfer baseline, and dropping pending C. Allow a hand-specified schema lens as an informed reference, not extra oracle labels for the proposed method. Every arm sees identical proposal-time observations and post-S anchor opportunities. Equalize retained bytes (including evidence, bridge samples, validators, and old models), calibration queries and training work. Where no byte advantage is plausible, test whether retaining a different kind of observation makes an edit identifiable, not whether a particular matrix multiply is novel.
- **E · Inherited exercise.** Use a finite task family and a tiny neural classifier or policy. A generation gets an exercise artifact and a limited opportunity to act, observe outcomes and update its weights. It or its successor may reinstantiate the exercise in a changed action space two handoffs later; neither knows the final affordance mapping at the first handoff. Example: choose which objects to inspect, with interventions that reveal whether order or material governs a transition. Later, the direct inspection action disappears but moving a witness object can expose the same distinction. The artifact receives only the same mapping evidence as its competitors. Withhold test contexts, independently vary distractors and include rival policies that pass familiar exercises. Check lasting behavior with the exercise, teacher and diagnostic interface removed. Do not count success on the exercise as success on the task.
- **E controls and retention in both fixtures.** Compare optimal teaching sets (exhaustively enumerated where possible), [recursive teaching sets][rtd], an equally parameterized adaptive curriculum/teacher, raw behavior demonstrations and direct answer transfer. The tutor has no free oracle: charge outcomes, expert calls, environment actions, rejected tries, passes through the model, teacher and student storage and compute across **all** generations. Include answer transfer even when it puts an upper bound only on an individual task. For M and E, test fixed held-out ordinary A/B inputs before, after S or each handoff, after C and after D if present; no task IDs or checkpoint switches. Report per-task and worst drop at matched new-task performance with the intended C change excluded from the *unchanged* A/B slices. All card retention lines supplement this contract. If a flat encoding of the same legitimate information ties at equal budget, the claim does not survive.

## A · CE07: Compile what is still justified

### CE2-01 · Keep the parent promise, do not invent the children's — PRIMITIVE
- **Mechanism:** A pending adapter carries a behavioral constraint rather than an old coordinate: for a known mix of two newly separated subtypes, it fixes the aggregate logit change and leaves the difference free. On the new base, fit only the identified component; keep the residual as an unresolved constraint for D instead of stamping identical changes onto both children.
- **Nearest prior / gap:** [SoftEdit][softedit] edits a model toward a calibrated distribution over plausible answers, and [Trans-LoRA][translora] trains a student adapter from teacher outputs. The new object is a *partially actionable proposal* whose unlabeled direction stays open through the split. The aggregate must represent legitimate knowledge, not an assumption that the population mix stays fixed.
- **Cheapest first test / control:** In M enumerate old aggregate-only evidence and two incompatible child corrections with that aggregate. Commit the common component, then reveal a subtype outcome on D. Compare pooled-target distillation plus a stored residual constraint, raw replay, and conservative no-write. Verify the aggregate across independent composition samples from the stated reference mix.
- **Old-task retention:** Score old individual decisions within each subtype, not just the aggregate, before and after D.

### CE2-02 · Carry a counterexample to cloning the update — PRIMITIVE
- **Mechanism:** Before S, record a minimal observable contrast where the proposed gradient must *not* have the same effect. After the split, use it as a linear constraint when fitting the target adapter, so the old proposal can exclude one child even if its positive traces do not name either child.
- **Nearest prior / gap:** [AlphaEdit][alphaedit] uses null-space constraints to preserve existing knowledge. Here the negative constraint is part of the intent of an uncommitted change and can discriminate its legal landing site after S; protecting a fixed old key is not the claim.
- **Cheapest first test / control:** Train two identical old deltas with different scope counterexamples. The learned new representation separates the two contrasted strata. Compare AlphaEdit with the same contrast as preservation examples, plus a flat stored positive/negative replay set; no extra labels for the candidate.
- **Old-task retention:** Check rare old negative cases near the newly learned boundary and old positives that the exclusion must not suppress.

### CE2-03 · Reference a difference between two proposed worlds — PRIMITIVE
- **Mechanism:** A pending write specifies a relation between two possible edited models, e.g. the increment from remedy X to remedy Y must affect defective returns only. Translate it by jointly fitting two new low-rank deltas against shared observable anchors; do not independently reconstruct two full outputs or install either old model.
- **Nearest prior / gap:** [Tangent task arithmetic][tangent] studies task-vector combinations and disentanglement in weight space. This object transports an identified *relative effect* even when each endpoint contains nuisance behavior that should not migrate.
- **Cheapest first test / control:** Make each endpoint depend on a different nuisance feature, with only the difference between target actions stable. Compare transfer of two endpoint adapters, arithmetic then transfer, and ordinary difference-target distillation with the same anchors, rank and bytes.
- **Old-task retention:** Check old cases involving each nuisance and the no-remedy path after one remedy is selected and written.

### CE2-04 · Keep an invariant test for descendants of the proposal — PRIMITIVE
- **Mechanism:** Store a falsifier for a proposal in terms of a transformation of legitimate inputs (e.g. changing shipping label alone should not change the edit's effect). On the new representation, require that relation for the *change in outputs*, not for outputs themselves, over generated pairs.
- **Nearest prior / gap:** [Intervention Design for Effective Sim2Real Transfer][sim2real] uses changes in simulated variables to learn robust behavior; [metamorphic specification mutation][metamorphic] generates testable relations for programs. The candidate applies a transported intervention specifically to the behavioral derivative of an uncommitted weight update.
- **Cheapest first test / control:** In M the new encoder entangles shipping labels with subtype. Use one learned label transform to fit a rank-1 write, then test held-out transforms. Compare update distillation on paired augmented examples with the same transform and number of forward passes.
- **Old-task retention:** Include old tasks where shipping label is genuinely predictive; these should keep their original label sensitivity.

### CE2-05 · A proposal whose immediate write must survive an unknown refinement — PRIMITIVE
- **Mechanism:** Represent a proposal as a set of feasible functional edits. Fit a small new write only if it helps every still-plausible interpretation and meets old behavioral constraints; move unresolved effects into a residual proposal, which later evidence can narrow. Unlike CE2-01, the common safe write need not be an aggregate.
- **Nearest prior / gap:** [SoftEdit][softedit] represents multiple valid answers; [Invariant Risk Minimization][irm] seeks a predictor useful across training environments. The candidate is a two-part commit rule across *uncertainty about the intended edit*, not across known environments.
- **Cheapest first test / control:** Enumerate three admissible edits to a linear head with overlapping but non-identical support. Compare worst-case robust fine-tuning plus a version-space store, equal-budget replay, and delaying all of C. Include a case where no safe write is possible.
- **Old-task retention:** Check A/B near the boundary for each feasible interpretation, then again after a residual choice is resolved on D.

### CE2-06 · Transport a relation between edits, not their shared latent name — PRIMITIVE
- **Mechanism:** An incoming pair of requests is identified only by a relation: one correction must be cumulative with the other in some inputs and cancel its effect in others. Store that signed condition while both are pending; after S fit their adapters jointly and test composition on fresh inputs.
- **Nearest prior / gap:** [Gradient-sign task vector transport][sign] already uses sign masks to transfer task vectors; [task arithmetic][tangent] already adds and negates task vectors. This card preserves the input-conditioned relation between *effects* under refinement, not the sign pattern of a parameter delta or an ordering law.
- **Cheapest first test / control:** In linear M, the same old key covers two strata with opposite required joint effects. Compare independent learned target transfer plus a relation penalty, and fit the two adapters directly on combined examples at matched rank. The direct equal-budget joint fit is a decisive null.
- **Old-task retention:** Measure old behavior after each adapter independently and after composition; average agreement can hide rare B failures.

### CE2-07 · Store uncertainty about the reason separately from uncertainty about the map — PRIMITIVE
- **Mechanism:** Carry a proposal with separate alternatives for what it should do and where its old predicate landed. Admit a new supervised example only to resolve the ambiguity it actually identifies; e.g. paired activations may settle alignment without granting authority to change a subtype. Compile only effects common to the surviving combinations.
- **Nearest prior / gap:** [Explicit many-to-many activation maps][manymaps] address cross-model alignment; [rational belief revision for model edits][belief] distinguishes edits from broader consistency requirements. The candidate splits uncertain content and uncertain transport as different kinds of evidence governing a future weight write.
- **Cheapest first test / control:** Construct a 2×2 finite ambiguity where one anchor breaks the map ambiguity and another outcome breaks the content ambiguity. Compare a joint Bayesian model with the same alternatives, evidence and storage and conventional calibrated adapter transfer; if the Bayesian model ties, this is a factorization rather than extra expressivity.
- **Old-task retention:** Include old sibling cases harmed by each premature commit and make both evidence-arrival orders face the same A/B evaluation.

## B · CE07: Survive realistic transport limits

### CE2-08 · Turn a pending delta into a short question to the new model — PRIMITIVE
- **Mechanism:** At proposal time, derive a small set of input interventions whose edited versus unedited responses would distinguish scope. After S, use those interventions to build a target-space write, using only previously licensed contrasts or fresh legitimately obtained outcomes. Do not distill the old model on arbitrary held-out data.
- **Nearest prior / gap:** [Trans-LoRA][translora] uses synthetic data to transfer learned adapters; [iterative teaching by data hallucination][hallucination] optimizes synthetic teaching signals. The candidate is a query program preserved for a *future representational split*, where examples chosen for old fit can omit the necessary intervention.
- **Cheapest first test / control:** Hide which of two interventions will remain accessible after S. Compare matched-byte proposal distillation on stored examples, their parameterized augmentation and a learned synthetic-query teacher with the same outcomes and compute.
- **Old-task retention:** Check input variations that resemble a proposed query but where the old task's decision must be unchanged.

### CE2-09 · Salvage a proposal by changing which layer receives it — PRIMITIVE
- **Mechanism:** Store a small description of the original edit's action on outputs and which computations it may affect. When the new head collapses a needed distinction, fit a lower-layer adapter that recreates only the needed conditional action instead of forcing an algebraic head-to-head transport.
- **Nearest prior / gap:** [MEND][mend] learns how to edit model parameters and [many-to-many activation maps][manymaps] align layers. The candidate is target-layer selection constrained by effects of a *pending* intervention under a representation bottleneck, not upgrading an installed adapter.
- **Cheapest first test / control:** In a two-layer MLP make an intermediate feature distinguish two children but the head representation collapse them. Compare exhaustive layer search using the same behavioral constraints, MEND-style amortized editing, and head-only transfer; the first is the strongest control at equal search work.
- **Old-task retention:** Score tasks that read the edited intermediate feature through different output branches.

### CE2-10 · Preserve a relational write when one of its witnesses disappears — PRIMITIVE
- **Mechanism:** A queued edit binds two input roles (e.g. refund follows order cancellation for the same transaction). After S, one embedding cannot distinguish an entity by its old feature. Train the adapter from still-accessible paired examples that constrain the relation; do not silently change the edit into two unary label writes.
- **Nearest prior / gap:** [Prototype-sample relation distillation][relation] preserves representation relationships in CL. Here the learned target is the relative effect of a queued rule on paired inputs, not preservation of distances or fitting isolated facts.
- **Cheapest first test / control:** On finite paired strings, replace one old feature with a new observable and hold out recombinations. Compare pairwise relational distillation with direct joint retraining given the same raw evidence. Report failure if enough information is absent on ordinary inputs.
- **Old-task retention:** Retest old pairs where each unary feature is present but their relation is false, in addition to rare legacy positives.

### CE2-11 · A cheap proposal should leave a receipt for what would make it expensive — PRIMITIVE
- **Mechanism:** Attach one small witness showing why a rejected alternative would require a different scope or another degree of freedom. When a new feature makes that witness decisive, choose whether to fit one adapter, fit two scoped writes, or leave C unresolved. The receipt is about *how many distinct edits the evidence now demands*, not a meter of model capacity.
- **Nearest prior / gap:** [Fast Model Editing at Scale][mend] produces efficient local edits and [AlphaEdit][alphaedit] projects edits to protect retained behavior. Neither comparison makes a missing evidence distinction an explicit part of the pending edit. No claim about predicting a general edit capacity threshold.
- **Cheapest first test / control:** Build two migrations with identical target rank budgets but different legitimately observed old contrasts. Compare a fixed rank and adaptive supervised rank search with the same contrasts and bytes. Count rank or refit work only when held-out C and old retention are matched.
- **Old-task retention:** Score rare B cases on both sides of the witness and after installing the additional write, not just after selecting rank.

### CE2-12 · Translate the boundary between two serial requests before translating either update — PRIMITIVE
- **Mechanism:** One pending proposal assumes that another applies only inside a scope boundary. Resolve the boundary on the new representation first; compile either delta only where that assumption still holds. The migrated object is an applicability dependency, not stored optimizer state or an edit ordering heuristic.
- **Nearest prior / gap:** [Memory-Based Model Editing][serac] uses a scope classifier to apply edits, and [verified three-way program merge][merge] checks reconciliation against changes. This card makes a scope dependency between uncommitted parametric writes a learned migration target.
- **Cheapest first test / control:** Two requests cover overlapping return types, with full overlap only in the old encoder. Compare scoped adapters with jointly learned gates (both fully charged), direct replay on both requests, and independently transferred edits. Verify active effects on unseen boundary cases after committing both.
- **Old-task retention:** Check each innocent overlap case and all A/B behavior after each individual install as well as the combined install.

### CE2-13 · Transfer the proof obligation to the recipient rather than its verdict — PRIMITIVE
- **Mechanism:** A queued adapter is eligible only if fitting it to the new weights passes a constraint stated in output space. When S exposes a previously unavailable witness, refit the write to meet that condition rather than using the old model's verdict as approval. This lets an old request demand a new kind of supervised evidence without changing its target.
- **Nearest prior / gap:** [Controlling Models by Transporting Activations][activation] transports activation-space controls, and [AlphaEdit][alphaedit] constrains the write to protect unrelated predictions. The extra operation is an old constraint that can be re-instantiated as an eligibility test in a new representation; if explicit revalidation ties, its value is procedural only.
- **Cheapest first test / control:** Before S, old observation pairs cannot test a requested no-effect condition; afterward a legitimate witness can. Compare standard learned mapping plus adapter refit and ordinary validation with identical observations, and unconstrained transfer. Include a correctly uncommittable proposal.
- **Old-task retention:** Run old ordinary tasks after S regardless of whether C commits; for accepted C, retest both witness-adjacent and independent old cases.

## C · CE21: Make an exercise that teaches a weight update

### CE2-14 · Substitute an intervention without changing the question — PRIMITIVE
- **Mechanism:** An exercise names a variable to vary, variables to hold fixed, and two hypothesized outcome patterns. A successor searches its available actions for a way to realize that contrast. The resulting observations, not the artifact itself, supervise SGD on the successor's predictor.
- **Nearest prior / gap:** [Deep Adaptive Design][dad] chooses informative actions conditional on an experiment history; [Environment Design for Inverse Reinforcement Learning][edirl] chooses environments to identify rewards. The candidate is a handed-down *experiment specification* the successor can realize with a different actuator, without retaining a source environment.
- **Cheapest first test / control:** In E, replace an order-toggle with a staged move sequence. Compare an adaptive design policy retrained with the same mapping evidence, optimal teaching examples and a parameterized rollout generator. Require the trained predictor to distinguish material from order on ordinary contexts after the intervention is unavailable.
- **Old-task retention:** Check old contexts in which changing order really does matter and old materials absent from generated trials.

### CE2-15 · Let the student choose the ambiguity its exercise will resolve — PRIMITIVE
- **Mechanism:** Store a procedure accepting two locally plausible rules and returning an experiment that would separate them if one exists. At handoff the successor constructs its own pair from errors of its current network, then fits on the outcomes. The artifact does not assume the successor has the previous learner's blind spot.
- **Nearest prior / gap:** [Machine Teaching of Active Sequential Learners][active] explicitly accounts for active learners; [teacher algorithms for curricula][portelas] choose tasks based on progress. The candidate is an inherited compiler from *student-specific disagreement* to an accessible intervention, not merely an adaptive choice among known levels.
- **Cheapest first test / control:** Train tiny networks to solve A/B with different spurious cues. Give both the same artifact and action interface but test a changed cue in the final generation. Compare active learner plus optimal experiment, adaptive curriculum on the same hypothesis inputs, and a static teacher blind to the student.
- **Old-task retention:** Retest each student's distinctive old skill; also check old examples in which the now-rejected cue legitimately predicts behavior.

### CE2-16 · Pass down a loss that becomes meaningful only after interaction — PRIMITIVE
- **Mechanism:** Inherit a procedure that generates a paired training loss only after a student performs an intervention and observes its consequence. In one student the loss might push two embeddings apart; in another it leaves the same representations merged. A successor can instantiate the loss through its own action interface.
- **Nearest prior / gap:** [Generative Teaching Networks][gtn] generate synthetic training data to train learners, and [trajectory-matching dataset distillation][mtt] synthesizes data by matching training trajectories. The proposed artifact defines conditions for an outcome-dependent loss rather than synthetic labels or a weight trajectory.
- **Cheapest first test / control:** In E assign two worlds identical passive observations but opposite outcomes for an intervention whose physical implementation has changed. Compare generated contrastive examples with an adaptive generator receiving the identical interaction outcomes and allowed to synthesize differentiable targets. No credit merely for access to fresh observations.
- **Old-task retention:** Verify old embeddings still support held-out A/B outputs, including a task that must not split on the newly tested attribute.

### CE2-17 · Inherit the shortcut the final task must rule out — PRIMITIVE
- **Mechanism:** A successor receives an executable exercise and a rival strategy that can pass it. Before reusing it, modify an available action or context so the intended rule and rival strategy produce different outcomes, then fine-tune on those observations. The exercise carries a way to be falsified, not just success.
- **Nearest prior / gap:** [Mutation-guided test generation][mutation] generates tests to expose changes to programs, and [PAIRED][paired] creates difficult environments using agent regret. The claim is that a *transferable rival policy* makes a diagnostic curriculum survive affordance change, not merely that adversarial examples train a stronger student.
- **Cheapest first test / control:** Let the rival exploit a color cue never varied in the first environment. Realize a color intervention after the old inspection action disappears. Compare a PAIRED-style adversary with the same rival and an optimal teaching set allowed to target it under the same teacher and query budgets.
- **Old-task retention:** Keep legitimate old uses of the color cue and behavior in the old context that originally admitted the shortcut.

### CE2-18 · The next student should have to act to tell two worlds apart — PRIMITIVE
- **Mechanism:** Inherit a pair of task generators constrained to give the same observations before the student's intervention, then diverge under an action it can actually take. Train a recurrent student on action–observation sequences so it learns to infer the rule and then apply it beyond the examples used to identify it.
- **Nearest prior / gap:** [Dynamic Teaching in Sequential Decision Making Environments][dynamic] already teaches through choice of trajectories, while [CLUTR][clutr] learns task representations to generate curricula. The candidate is a coupled generator with an observational-equivalence contract that a successor must re-establish after affordance change.
- **Cheapest first test / control:** Use a two-step hidden-rule classification problem with one separating action in each affordance regime. Compare a recurrent learner trained by an equally parameterized adaptive curriculum and plain supervised training on the same trajectories and actions.
- **Old-task retention:** Check ordinary old episodes requiring no query and those where a different query remains the correct way to choose the old rule.

### CE2-19 · Learn which contrast can be built from incomplete outcomes — PRIMITIVE
- **Mechanism:** The inherited exercise specifies a diagnostic relation between outcomes, not their identities. If an intervention now reveals only one component per try, realize the relation using two allowed trajectories with a shared initial condition, and make a weight update only when the common nuisance is actually controlled.
- **Nearest prior / gap:** [Causally invariant reward learning][invariantreward] uses diverse demonstrations to exploit causal invariance, and [intervention design][sim2real] shapes simulation contrasts. The novelty candidate is a transmissible equivalence between one simultaneous intervention and several partial observations under a new interaction interface.
- **Cheapest first test / control:** Change a toy simulator from joint readout to two single-channel readouts. Compare paired probing with a conventional causal experimental design baseline and direct partial-label training on the same bytes and calls. Include a confounded cell with no valid coupling; it must not produce confident updates.
- **Old-task retention:** Retest ordinary old cases that rely on the components' former joint signal and rare B where the two channels report different things.

### CE2-20 · Inherit an exercise for a missing intermediate concept — PRIMITIVE
- **Mechanism:** An artifact specifies a temporary auxiliary prediction head by how to elicit its target, not by naming a feature in the teacher's model. The student performs the exercise to obtain the intermediate labels, updates its encoder and main head, then discards the auxiliary head before deployment. A successor must be able to reconstruct the elicitation in a changed world, not copy the intermediate feature.
- **Nearest prior / gap:** [Concept Bottleneck Models][concept] train on human-specified intermediate concepts and permit interventions on predicted concepts. The candidate is a portable procedure for eliciting supervision for an otherwise latent concept, with a test of residual value after retiring the temporary head, not test-time concept correction.
- **Cheapest first test / control:** In E, material identity is revealed by moving a witness item in the first world but by comparing two resulting states in the second. Put each legitimately elicited label into a standard auxiliary-head learner and a bottleneck baseline at equal interaction budget. Compare with end-to-end fine-tuning on the same outcome observations; evaluate goal predictions when none of the diagnostic actions are offered.
- **Old-task retention:** After discarding the auxiliary head, check A/B including an old decision the elicited concept cannot explain on its own.

## D · CE21: Make the exercise survive the chain

### CE2-21 · Hand off two imperfect enactments that identify the same rule together — PRIMITIVE
- **Mechanism:** Instead of a fixed task, pass a description of two affordance-specific realizations whose evidence is complementary. A successor can replace one member as long as the new pair still jointly rules out the named alternatives, and fine-tunes on the paired evidence.
- **Nearest prior / gap:** [Identifiability across multiple experts][multiexpert] studies what multiple experts or environments identify for inverse RL; [recursive teaching sets][rtd] exploit structured distinctions among hypotheses. The candidate is a jointly identifying *replaceable pair of interactive tasks* carried through successive interface changes.
- **Cheapest first test / control:** Remove one of two diagnostic actions after handoff; neither surviving readout alone identifies the correct rule. Compare an optimal joint teaching set, an adaptive curriculum with the same joint constraints, and independently rebuilt exercises.
- **Old-task retention:** Score old tasks relying on each readout separately and old combined cases after each successor fits on both enactments.

### CE2-22 · Make the receiver rehearse how the exercise would fail after a different change — PRIMITIVE
- **Mechanism:** Before passing an exercise on, train a scratch student with one available action removed. Save a small dependency specifying what evidence the lost action supplied and an allowed fallback to recover it. The real successor uses the dependency to rebuild training interactions, not the scratch student's weights.
- **Nearest prior / gap:** [ACCEL][accel] evolves environment levels with regret, and [domain randomization][randomization] trains policies across varying dynamics. The target is transferring *why an exercise stops teaching* when an affordance changes, not making the same policy robust under more sampled worlds.
- **Cheapest first test / control:** In E, simulate loss of a direct observer during training, then withhold a different observer from the final successor. Compare affordance-dropout curricula and a generic causal planning baseline given the same lost-action episodes and scratch computation.
- **Old-task retention:** Check both old observer-specific tasks, including one never present in the scratch student's training.

### CE2-23 · Carry a teacher you can simplify only on a new student — PRIMITIVE
- **Mechanism:** A generation may replace an exercise with a smaller program only if a student that lacks its current solution can train from the replacement, and can still recreate the exercise under a sampled alternate affordance. This selects for teachability rather than for the carrier's ability to solve the task.
- **Nearest prior / gap:** [Generative Teaching Networks][gtn] train fresh network learners with generated data, and [Artificial Generational Intelligence][agi] tests cross-lifetime transmission. The candidate is an edit operator on exercises whose admissibility depends on a second handoff, not just one generation's learning speed.
- **Cheapest first test / control:** Compress a two-part exercise where a fully trained student needs neither part but a fresh student needs both unless one is rewritten. Compare teacher-program compression with a two-generation training objective, and compression scored only on the current model; charge all fresh student updates.
- **Old-task retention:** Check a rare old task of each fresh student before and after inherited training, including where the removed exercise evidence also supports an old distinction.

### CE2-24 · Pass a family of witnesses, not more rehearsal — PRIMITIVE
- **Mechanism:** The exercise produces observation pairs that expose the same distinction at independently sampled nuisance values and induces consistency of the *learned rule* across them. Later successors can bind newly available nuisance controls and still generate valid training pairs without the original dataset.
- **Nearest prior / gap:** [Intervention design][sim2real] and [Invariant Risk Minimization][irm] address invariance across interventions and environments. The claim is a compact inherited rule for generating interventions through new affordances, not a new invariance loss or a memory replay schedule.
- **Cheapest first test / control:** Teach order sensitivity in E while independently varying shape, then hand off into a world where only texture is controllable and shape no longer correlates with the answer. Compare exhaustive equal-cost augmentation, an equally parameterized generative curriculum and IRM on the same observations.
- **Old-task retention:** Check shape and texture on separate A/B tasks where each genuinely matters; global invariance is a failure.

### CE2-25 · Use an inherited exercise to finish an unresolved write — PRIMITIVE
- **Mechanism:** Hand off a pending behavioral edit and the exercise that can identify its unresolved scope. The successor translates the exercise into a new affordance, gathers ordinary evidence, then writes only the justified component into its own weights. The source neither labels the new subtype nor exports an installed patch.
- **Nearest prior / gap:** [Heirloom][heirloom] transfers personalization and [Deep Adaptive Design][dad] identifies variables via experiments. The combined primitive is an update carrying an executable way to procure the evidence missing for that update. A performance gain must come from the coupling, not merely better transfer or experiment design.
- **Cheapest first test / control:** Cross M and E: old grouped evidence cannot locate an exceptions edit; after both a representation split and an actuator change, a translated intervention identifies its scope. Stack learned mapping and ordinary refit *plus* an equally informed adaptive teacher, and compare keeping the edit or exercise alone at the same total budget.
- **Old-task retention:** Track stepwise A/B after S, every handoff, the interaction and final commit; include old examples where the exercise's discriminating relation would imply a wrong edit if treated as global.

### CE2-26 · Require the exercise's learner to teach a different compatible rule — PRIMITIVE
- **Mechanism:** A successor inherits how to construct a separating exercise, is given a fresh target from the same rule family, and uses ordinary world outcomes to teach it to a third learner. This distinguishes a transferable construction method from an exercise that implicitly encodes the original answer.
- **Nearest prior / gap:** [Artificial Generational Intelligence][agi] combines intergenerational transfer with individual exploration; [recursive teaching sets][rtd] specify teaching sets across a concept class. The candidate artifact is a constructor tested on an unseen target and changed interaction vocabulary, never evaluated only on what the first teacher knew.
- **Cheapest first test / control:** First teach object ordering, then ask the exercise recipient to teach a rule about material using two affordances not available in generation one. Compare direct transmission of the hypothesis class plus optimal teaching, and an equally parameterized meta-trained environment generator. Include a carrier with the original answer but no constructor.
- **Old-task retention:** Test the original rule and both students' normal A/B tasks after the fresh lesson; constructing a new exercise is not allowed to erase the old decision.

## Ranked deeper questions

1. **What part of a pending write is actually identifiable across a learned split?** Start with CE2-01, CE2-02 and CE2-07. Make identical source deltas with different supported scopes, then separate the cases where a learned new encoder permits a common write, child-specific writes or no safe write. If raw replay, a typed schema lens, and learned mapping plus resubmission cover every cell at the same budgets, the node has found a benchmark, not a new mechanism.
2. **What minimum description lets an exercise survive loss of its original actuator?** Start with CE2-14, CE2-17 and CE2-21. Hold out the final affordance change and include an answer-carrying baseline and an exact adaptive teacher. Require a lasting weight-level gain on unrelated held-out inputs from the new family, not success in the final classroom, with no ordinary A/B loss.
3. **Can an unresolved update and an exercise together beat their independently optimized counterparts?** Start with CE2-25. Vary which representation distinction becomes available and which action survives independently. Find a case where allocating the exercise around the missing decision changes safe commits, and a case where either component is redundant. Compare at matched C success and A/B retention against both controls stacked.
4. **What makes an artifact teachable by a successor rather than just usable by one?** Start with CE2-23 and CE2-26. Compare identical two-handoff budgets, including time spent on scratch students; score a held-out objective whose answer is different and a final learner with only ordinary deployment inputs. Count a benchmark as passed only if the procedure generalizes and each generation keeps its old tasks.

[triage]: https://github.com/manojbajaj95/cl/blob/1c62d86/reviews/flood-triage.md#L469
[ledger]: https://github.com/manojbajaj95/cl/blob/1c62d86/reviews/idea-ledger.md
[heirloom]: https://arxiv.org/abs/2611.00650
[translora]: https://arxiv.org/abs/2405.17258
[drift]: https://arxiv.org/abs/2407.08536
[paired]: https://arxiv.org/abs/2012.02096
[gtn]: https://proceedings.mlr.press/v119/such20a.html
[agi]: https://arxiv.org/abs/2406.00392
[rtd]: https://jmlr.org/papers/volume15/doliwa14a/doliwa14a.pdf
[softedit]: https://arxiv.org/abs/2611.20562
[alphaedit]: https://arxiv.org/abs/2410.02355
[tangent]: https://arxiv.org/abs/2305.12827
[sim2real]: https://arxiv.org/abs/2012.02055
[metamorphic]: https://arxiv.org/abs/2511.18249
[irm]: https://arxiv.org/abs/1907.02893
[sign]: https://arxiv.org/abs/2510.09658
[manymaps]: https://arxiv.org/abs/2610.09058
[belief]: https://arxiv.org/abs/2406.19354
[hallucination]: https://proceedings.mlr.press/v206/qiu23a.html
[mend]: https://arxiv.org/abs/2110.11309
[relation]: https://arxiv.org/abs/2303.14771
[serac]: https://proceedings.mlr.press/v162/mitchell22a.html
[merge]: https://www.microsoft.com/en-us/research/publication/verified-three-way-program-merge/
[activation]: https://arxiv.org/abs/2410.23054
[dad]: https://proceedings.mlr.press/v139/foster21a.html
[edirl]: https://arxiv.org/abs/2210.14972
[active]: https://arxiv.org/abs/1809.02869
[portelas]: https://arxiv.org/abs/1910.07224
[mtt]: https://georgecazenavette.github.io/mtt-distillation/
[mutation]: https://arxiv.org/abs/2506.02954
[dynamic]: https://arxiv.org/abs/1210.4918
[clutr]: https://proceedings.mlr.press/v202/azad23a.html
[invariantreward]: https://arxiv.org/abs/2409.08012
[concept]: https://arxiv.org/abs/2007.04612
[multiexpert]: https://arxiv.org/abs/2209.10974
[accel]: https://proceedings.mlr.press/v162/parker-holder22a.html
[randomization]: https://arxiv.org/abs/1710.06537
