# Cultural Evolution 4: Common Edits That Keep Futures Open

Child of [cultural-evolution-3.md](cultural-evolution-3.md) ([PR #349](https://github.com/manojbajaj95/cl/pull/349), depth 3) · 26 cards · 4 ranked deeper questions · Ideas only; no GPU or experiments run

**Why this node exists.** The [review of #349, row 477][triage], found no score 4 and kept two score-3 candidates. **CE3-08:** among first low-rank writes with the same sanctioned effect, pick one that leaves a lawful completion for each still-plausible reading. **CE3-21:** choose a common write that does not stop the learner from obtaining the ordinary observations that would settle its scope. A continuation must be both **writable** under the next update's real constraints and **choosable** using evidence the deployed learner can still obtain. A spare direction is a serious explanation for the first effect; generic conservatism or separately optimized active learning might explain the second.

**Literature check.** Hugging Face Papers and targeted web searches were checked against publisher/arXiv abstracts and available text. [AdaLoRA][adalora] uses SVD-like adapter triplets and importance-based rank allocation; compare it with the same total rank and a version scored on future reachability. [AlphaEdit][alpha] projects a write into the null space of preserved knowledge keys; use identical keys in single-step and lookahead baselines rather than crediting null-space protection as new. [SPIBB][spibb] uses baseline behavior in poorly supported regions in offline RL; it is a control for conservative behavior, not itself a guarantee that a particular future experiment will remain informative. [Dual stochastic MPC][dual] and [Deep Adaptive Design][dad] already optimize the information consequences of action sequences. [Adjustable robust optimization][adjust] already plans outcome-dependent recourse. The claim to test is not that planning or reserves are new. It is that a particular **training placement** can preserve measured, evidence-dependent recourse in a model more cheaply than a signed spare or an ordinary joint planner. A **PRIMITIVE** below is a candidate new object/operation under the [ledger][ledger], not a priority claim.

## Shared fixtures and required controls

- **R · Real weight reachability.** A tiny CPU encoder/head has learned A and rare B. C authorizes a common behavioral change plus one of two scoped continuations; acquire C in the old representation and add an independent split S before committing. First writes must match the common benefit, not anticipate an unresolved reading, and meet A/B floors on ordinary inputs. Define the accessible layers, number of writes, cumulative deployed rank, per-write rank or norm as separate limits, and releasable versus fixed factors *before* enumerating the legal next writes. Include all equally licensed first placements in the search; predeclare a minimum nonzero effect. Charge existing and temporary state, including factorization, branch tables, anchors, and proposal data. Use exhaustive finite matrices first and confirm any apparent separation on an actually trained small MLP with held-out inputs and lawful candidate generation. Intermediate “reachable” outputs must survive an actual write, not just a Jacobian approximation.
- **E · Surviving experiment.** Give each reading a finite table of routine observations and a lawful experiment that can change the authorized next action. Keep simulator truth out of training and planning; enumerate with oracle dynamics only as a bound, then learn dynamics from a common stream. Some equally useful first writes preserve the experiment, others change which visits occur, which actions remain available, or which outcomes mean what. Each arm has the same legitimate evidence, environment actions, costs and deadline after the write, with no extra reset/refill. Include both-edits-preserve, neither-can-preserve and same-visit-but-no-longer-discriminative cases. Measure worst-reading probability of a lawful informative result by deadline, then actual scope decisions and resulting C/D behavior. A visit or a confident guess is not a successful experiment.
- **Required on every card: commit-and-reserve with a signed spare coefficient (SCR).** Following [#348’s review, row 476][spare], jointly fit a licensed common write and one dormant rank-1 direction `uvᵀ` from the same proposal evidence and candidate layer set as the method. Score candidate common placements and spare directions with the same pre-commit information/work; freeze the spare direction and set its deployed coefficient to zero until an authorized observation arrives, then choose and fit a bounded real coefficient of either sign, or stay at zero. It need not be ±1, and the signs need not have equal magnitudes. Keep the common effect and old floors, and charge factors, coefficient precision, temporary validation work and rank to the same limits. If the proposed method can adapt the experiment or collect anchors, SCR gets the same legal opportunity, planner and evidence. If both arms can afford multiple spare coefficients or a post-result refit, include those as **stronger additional** controls at matched total bytes/rank/work, not in place of SCR. A signed scalar should tie when all feasible continuations lie on one line.
- **Algebra sanity cell, not a CL result.** For cumulative rank ≤1 and initial common write `W=E11`, matrices `E11+aE12` and `E11+bE21` with nonzero `a,b` are each reachable by one rank-1 correction. A fixed spare through `W` cannot hit both. Even if SCR selects its anchor anywhere on the line through the two targets, interior points have rank 2 and the endpoints prematurely pick a reading. This is a necessary-control check in a deliberately limited fixture, not evidence that a realistic stream needs nonlinear recourse, or that any storage advantage follows. Include a collinear null, allow a matched two-coefficient arm when feasible, and require a learned split or a learned observation model for any follow-up claim.
- **Matched baselines and retention.** Compare same-effect random placement, empty spare rank, branch copies and full refits where affordable; compare AdaLoRA, AlphaEdit, SPIBB-style conservative improvement, post-write DAD, a dedicated experiment, and exact joint weight/action search in the cells where each applies. Stack strongest controls for crossing R and E. Charge every attempt and include wrong commits, false holds and delay. Score held-out ordinary A/B before and after S, after the first write, during the experiment window, after each possible completion and after independent D where present. Use no old snapshot for serving, task ID, private reading label or privileged routing. Keep a separate rare-old holdout; each card adds a particular old-task slice. Reject a claimed win if a simpler same-budget control matches C/D utility at the same old floors.

## A · CE3-08: Place the common effect where the next legal weight write can reach

### CE4-01 · Choose a shared factor rather than a spare direction — PRIMITIVE
- **Mechanism:** Use a common rank-1 write with separate legal continuation families: a later rank-1 step may change its input factor or its output factor. Choose a first placement from which both families contain a correct completion, without storing either candidate as a second fitted adapter.
- **Nearest prior / gap:** [Fixed-rank matrix optimization][fixedrank] already exploits row and column tangent structure; [AdaLoRA][adalora] reallocates adapter rank. The candidate is choosing a deployed common factor for two specific later legal edits, not inventing tangent structure or using two spare dimensions.
- **Cheapest first test / control:** Start with the algebra cell, then allow equal-effect common placements in a 3×3 MLP head and learn which first factor preserves both alternatives. Compare commit-and-reserve with a signed spare coefficient, matched two-spare and two-factor refit arms, and best exact placement.
- **Old-task retention:** Check old reads into both first-factor families and rare B after each possible factor change.

### CE4-02 · Take a first step that keeps a rank-one detour legal — PRIMITIVE
- **Mechanism:** A desired completion may be representable at rank one but blocked by a floor along every direct allowed update from one common placement. Choose a placement that admits a two-step detour with each intermediate deployed state still lawful.
- **Nearest prior / gap:** [Contingency-aware reachability][reach] guarantees backups along physical trajectories, and [fixed-rank optimization][fixedrank] finds paths on a rank-constrained surface. The candidate is an intermediate behavioral floor as part of a *lawful edit path*, rather than checking only final representability.
- **Cheapest first test / control:** Enumerate a discrete low-rank factor grid with one forbidden intermediate observation and two permitted future writes. Compare commit-and-reserve with a signed spare coefficient, a two-coefficient detour if within budget, exact path search and end-state-only screening. Reject if the graph is constructed from target labels alone.
- **Old-task retention:** Score ordinary A/B at the detour waypoint, including rare cases hidden by a passing final evaluation.

### CE4-03 · Place the edit so the next ordinary gradient reaches the right branch — PRIMITIVE
- **Mechanism:** Select a common placement based on whether one ordinary labeled example, under the same fixed restricted gradient update, produces the authorized effect for either reading. The next lesson supplies the differentiating gradient; it does not select a stored branch or rewrite the optimizer.
- **Nearest prior / gap:** [MAML][maml] trains initializations for rapid adaptation, and [InfLoRA][inf] restricts CL writes to subspaces. The narrow task is fitting an already useful common edit whose *specified actual update rule* remains able to learn both distinct future effects.
- **Cheapest first test / control:** Tiny linear-plus-ReLU learner with two equal-effect first writes and identical next-step SGD, no hidden momentum. Compare commit-and-reserve with a signed spare coefficient, ordinary MAML on the same task family, and random placement; test fresh examples from each branch.
- **Old-task retention:** Check A/B cases whose gradient features overlap the second lesson, not just the original anchor examples.

### CE4-04 · Preserve an alternative operation under a new head restriction — PRIMITIVE
- **Mechanism:** Store a compact choice of live effect constraints such that if one layer later becomes frozen, the alternative writable layer still has lawful recourse for all readings. Pick the first placement using the set of declared restriction changes, not a preselected fallback rank slot.
- **Nearest prior / gap:** [Adjustable robust optimization][adjust] adapts to revealed scenarios and [AdaLoRA][adalora] distributes limited rank across layers. The candidate preserves reading-specific *behavioral reachability under a revealed write interface*, not a free extra layer.
- **Cheapest first test / control:** In a two-layer network independently freeze one layer after the first commit, before revealing the reading. Compare commit-and-reserve with a signed spare coefficient allowed to choose its initial layer, a two-layer matched reserve, adaptive rank allocation and exact robust planning.
- **Old-task retention:** Retest all A/B cases depending on each frozen layer before and after committing either reading.

### CE4-05 · Save a restriction that makes the next fit solvable without saving a solution — PRIMITIVE
- **Mechanism:** Fit a common write and export a conditioned feasible subproblem for the next edit (e.g. a reusable linear equality on observable effects). It bounds the next authorized search but encodes neither full completion; the next learner fits to a fresh target from its branch.
- **Nearest prior / gap:** [Multiparametric quadratic programming][mpc] precomputes feasible and optimal regions and [AlphaEdit][alpha] restricts editable directions using preserved keys. The candidate is retaining a reusable low-cost *subproblem* rather than the complete solution map or a coefficient.
- **Cheapest first test / control:** Vary a future target within each of two ranges not disclosed at commit. Compare commit-and-reserve with a signed spare coefficient, an exact stored parametric solution and raw refitting at the same retained bytes and post-result computation.
- **Old-task retention:** Check A/B at branch interval endpoints and interior targets, including the lowest-margin old decision.

### CE4-06 · Make one future write safe by where the first one reads its inputs — PRIMITIVE
- **Mechanism:** Two equal present effects can arise from different incoming features. Choose the first feature dependence so a later allowed change of the shared head can alter the intended new cases without affecting old cases that use another input route.
- **Nearest prior / gap:** [O-LoRA][olora] separates task update subspaces and [AlphaEdit][alpha] preserves fixed key-value associations. The candidate chooses the present feature dependence using downstream constraints on the next *permitted* edit, not simply orthogonalizing today's update.
- **Cheapest first test / control:** Train a two-input network with two correlated features now and decorrelate them on S/D. Compare commit-and-reserve with a signed spare coefficient, AlphaEdit plus lookahead given the same held-out anchors, and direct replay/refitting. No claim if initial placements are actually inequivalent on old inputs.
- **Old-task retention:** Test the rare old group that still relies on the correlated feature the new outcome will change.

### CE4-07 · Keep an unseen magnitude family reachable, not just two endpoints — PRIMITIVE
- **Mechanism:** A first placement preserves a range of later sanctioned effects for each reading, including ones neither first learner knew. Fit the second write to a new magnitude after observing it; choosing endpoint branches alone does not count.
- **Nearest prior / gap:** [Parametric MPC][mpc] solves families of constrained recourse problems; [Trans-LoRA][trans] distills a fitted task adapter. The test is whether a compact common placement supports unseen behavior families with less stored recourse than explicit parametric fitting or adapter transfer.
- **Cheapest first test / control:** In R draw held-out magnitudes from two non-collinear intervals after the common write. Compare commit-and-reserve with a signed spare coefficient, matched piecewise-linear packet of coefficients, and exact parametric refit. A collinear cell should show no advantage.
- **Old-task retention:** Test A/B both near the center and at extreme legal magnitudes; an average can miss a rare-old boundary failure.

## B · CE3-21: Preserve something the learner can genuinely find out

### CE4-08 · Preserve an ordinary choice that serves as the experiment — PRIMITIVE
- **Mechanism:** When two updated policies finish routine work equally well, deploy the weight placement that still selects a lawful action whose result can decide scope before a deadline. The same routine should also finish its intended job; only gaining from preselected special visits is not enough.
- **Nearest prior / gap:** [Dual control][dual] already chooses actions partly for information value, while [SPIBB][spibb] preserves baseline decisions under weak evidence. The candidate is an effect-constrained weight placement that realizes a particular learning-relevant choice in ordinary deployment.
- **Cheapest first test / control:** Two finite routing paths serve a job; only one exposes the order/material contrast. Compare commit-and-reserve with a signed spare coefficient using the same route planner, SPIBB-style conservative routing, post-write DAD, and a dedicated experiment at the same action cost.
- **Old-task retention:** Check old jobs requiring either path, including rare B whose legal service deadline differs from C.

### CE4-09 · Keep an outcome informative after the model changes its own policy — PRIMITIVE
- **Mechanism:** Preserve a contrast pair whose outcomes still separate readings under the updated policy, not merely access to its test state. Choose a common write that changes neither the measured nuisance balance nor the legitimate transformation needed to justify the contrast.
- **Nearest prior / gap:** [Performative Prediction][perform] models changes in data caused by predictive decisions and [goal-oriented causal design][goal] selects interventions for a target quantity. The candidate is the enforceable **contrast-preservation constraint on the initial weight write**, with an ordinary causal comparator.
- **Cheapest first test / control:** Both first edits reach the query with equal frequency; only one leaves a paired outcome interpretable. Compare commit-and-reserve with a signed spare coefficient, policy-conditioned design with the same causal model, and increased passive sampling. Verify the decoded observation changes a valid write.
- **Old-task retention:** Test old contexts where the nuisance actually matters, ensuring the first write did not gain by erasing the feature globally.

### CE4-10 · Preserve access for every reading, not just for the average world — PRIMITIVE
- **Mechanism:** Use an observation-conditioned policy to execute the experiment, but require some legal informative trajectory within budget for each reading; a path that becomes available only when a particular reading is true must supply a credible alternative in the other world.
- **Nearest prior / gap:** [SafeMDP][safemdp] explores safely reachable and returnable states, and [DAD][dad] amortizes adaptive experiment selection. The candidate is a worst-reading requirement fed back into selection of the common parametric edit, not a new safe-exploration theorem.
- **Cheapest first test / control:** In E, two policies have equal mean access to an inspection but one has zero access under a rare reading. Compare commit-and-reserve with a signed spare coefficient and the same adaptive planner, plus minimax dual design with the same world models.
- **Old-task retention:** Report A/B by reading and check rare B when the experiment must take the alternative lawful path.

### CE4-11 · Preserve a prefix, not a fixed probe itinerary — PRIMITIVE
- **Mechanism:** Choose a first write that keeps an initial ordinary action available from which later observations can determine different legitimate tests. The useful object is a shared first prefix with mutually exclusive continuations, not commitment to both complete trajectories.
- **Nearest prior / gap:** [Predictive state representations][psr] model action–observation tests, and [DAD][dad] explicitly plans conditional choices. The candidate constrains a weight write to keep a minimal prefix that supports an adaptive decision tree after the edit.
- **Cheapest first test / control:** Two readings share the first step but call for different second checks. Compare commit-and-reserve with a signed spare coefficient given the same conditional planner, best open-loop sequence, and exact contingent planning over each first write.
- **Old-task retention:** Check old tasks requiring one of the diverging second actions outside the experiment; don't reserve the prefix by breaking normal behavior.

### CE4-12 · Keep a reversible observation opportunity under a hard deadline — PRIMITIVE
- **Mechanism:** An experiment can be technically reachable but useless if its path misses an existing service obligation. Choose a common write whose deployment can interrupt and resume an ordinary route in time, exposing a result without leaving unfinished old work behind.
- **Nearest prior / gap:** [SafeMDP][safemdp] plans returnable exploration and [contingency-aware reachability][reach] checks viable backups. The candidate couples timely return to **installation of the common edit**, not introducing returnability as a new idea.
- **Cheapest first test / control:** In a finite queue with two equal-service first writes, one leaves a slack window for an authorized excursion and one does not. Compare commit-and-reserve with a signed spare coefficient, a deadline-constrained planning baseline with identical slack, and a separate same-time experiment.
- **Old-task retention:** Measure normal A/B completion and old deadline misses during the excursion as well as after returning.

### CE4-13 · Preserve a foreign actor's opportunity to finish the exercise — PRIMITIVE
- **Mechanism:** The first learner can no longer take the separating action, but its write chooses whether a later authorized actor receives the physical state or observable record needed to complete the exercise. Carry the state condition and exercise, not the actor identity or guessed result.
- **Nearest prior / gap:** [Artificial Generational Intelligence][agi] transfers knowledge between learners, and [decision region determination][drr] values informative tests by decisions. The candidate is preserving a specific transferable experimental affordance by selecting the earlier actor's weight placement.
- **Cheapest first test / control:** Swap helper capabilities after a shared commit. Compare commit-and-reserve with a signed spare coefficient with identical helper access, an equally parameterized handoff planner, DAD on the successor and answer-carrying transfer as a bound.
- **Old-task retention:** Check old tasks normally served by both actors and rare B requests not eligible for the experimental handoff.

### CE4-14 · Keep the control arm of the experiment available — PRIMITIVE
- **Mechanism:** A common write can make the revised behavior universal and thereby remove the comparison needed to distinguish readings. Pick a common placement that preserves one legitimately unchanged matched case rather than silently substituting an obsolete checkpoint as its control.
- **Nearest prior / gap:** [Goal-oriented causal design][goal] already selects informative controls and [SPIBB][spibb] already backs off to baseline behavior in uncertain regions. The candidate preserves the actual availability of a specific control case while still making a positively useful shared edit.
- **Cheapest first test / control:** One common write leaves an untreated lawful case in ordinary traffic, another erases it without reducing immediate C score. Compare commit-and-reserve with a signed spare coefficient, SPIBB-style fallback over the same cases, and a joint design allowed the same intervention menu; never withhold an effect C requires.
- **Old-task retention:** Check ordinary B outside the deliberately retained control and confirm the control's own old decisions remain valid, not merely unchanged by accident.

## C · CE3-08 × CE3-21: Fit the write and its experiment to one another

### CE4-15 · Pick the experiment that distinguishes writable actions — PRIMITIVE
- **Mechanism:** For each first placement, fit an exercise that groups its possible outcomes by which *legal weight continuations* they authorize. A question exposing the true reading is not useful if the branch it identifies is unreachable, and an alternative placement can make a coarser question sufficient.
- **Nearest prior / gap:** [Decision region determination][drr] selects queries based on decision regions, and [adjustable robust optimization][adjust] already couples revealed scenarios with recourse. Here decisions are overlapping sets of resulting behavior under a constrained neural re-edit; the plausible gain is an efficient jointly indexed structure, not a different Bayes rule.
- **Cheapest first test / control:** Cross reachable/unreachable branches with high/low-information outcomes in a linear head and learned finite environment. Compare commit-and-reserve with a signed spare coefficient plus the same design objective, stacked AlphaEdit and decision-aware DAD, and exact joint enumeration.
- **Old-task retention:** Check every actually reachable live continuation for rare B, including interpretations that share a decision after grouping.

### CE4-16 · Make the ordinary outcome a usable training example — PRIMITIVE
- **Mechanism:** Of equally helpful first writes, choose one for which a separating observation both licenses the right reading and activates a usable feature for the next rank-constrained gradient. Receiving a label that the current writable layer cannot act on is not recourse.
- **Nearest prior / gap:** [MAML][maml] makes examples useful for future gradient steps, and [dual MPC][dual] chooses informative actions. The candidate preserves *the joint authorizing and training function of one future observation* rather than optimizing adaptation from an externally supplied training set.
- **Cheapest first test / control:** Use a toy network where two first weights give identical decisions and identical query access, but one masks the observed feature. Compare commit-and-reserve with a signed spare coefficient, same-budget meta-learning plus separate DAD, and exact joint placement/query search. Match total post-result training steps.
- **Old-task retention:** Retest old cases sharing that feature and cases mapped to the same intermediate unit after the first write.

### CE4-17 · Leave a legal path to a different experiment if the writable layer changes — PRIMITIVE
- **Mechanism:** Provide two brief experiment specifications tied to different future edit interfaces. The common placement preserves access to the one that can authorize a completion in whichever layer remains writable, rather than reserving one experiment regardless of what will accept its evidence.
- **Nearest prior / gap:** [Adjustable robust optimization][adjust] allocates scenario-dependent decisions and [Trans-LoRA][trans] retargets an adapter to another base. The candidate is an observation-to-edit compatibility relation crossing an independently changed action interface and trainable layer.
- **Cheapest first test / control:** Independently randomize which layer freezes and which action disappears, with at least one irreconcilable cell. Compare commit-and-reserve with a signed spare coefficient, matched flexible two-spare planning, and an exact two-stage solver given the same options; no winner gets preview of the draw.
- **Old-task retention:** After each reveal and each allowed experiment, test old A/B that rely on the newly frozen layer or discontinued action.

### CE4-18 · Let one outcome remove the need for a second update — PRIMITIVE
- **Mechanism:** Choose a first write whose behavior already satisfies a reading that needs only the common result, while preserving a distinct writable branch for the reading requiring more. The experiment must distinguish “done” from “apply another edit,” not force every possible result to spend a reserve.
- **Nearest prior / gap:** [SPIBB][spibb] uses a baseline when evidence is insufficient and [decision-region determination][drr] stops when a decision is supported. The candidate treats **no second weight write** as an authorized, positive completion tied to the chosen first placement, not an abstention or a zero training score.
- **Cheapest first test / control:** Two readings share a required output, one also imposes a novel minority correction. Compare commit-and-reserve with a signed spare coefficient permitted to stay zero, a two-stage value-of-information policy with optimal stopping, and always-update. A tie with optimally used zero is expected in the collinear cell.
- **Old-task retention:** Retest old cases in both the zero-update and nonzero branches and quantify unnecessary adaptation that changes B despite no benefit.

### CE4-19 · Optimize the first write for the expense of the reachable continuation — PRIMITIVE
- **Mechanism:** When multiple first writes preserve both futures and the experiment, choose one that places both completions within the allowed *post-observation* adaptation budget. Equal expressivity without equal time to fit is not equivalent if an independent routine task is due.
- **Nearest prior / gap:** [AdaLoRA][adalora] budgets parameter updates, [MAML][maml] optimizes fast fitting, and [dual control][dual] prices future information. The proposed object is a first edit jointly constrained by worst-branch evidence delay and measured continuation fitting cost.
- **Cheapest first test / control:** Sweep a fixed one- versus two-update deadline on a tiny head with matched initial performance on held-out C cases and shared candidate next lessons. Compare commit-and-reserve with a signed spare coefficient, exact schedule search and meta-learned placement with the same gradients and total compute.
- **Old-task retention:** Evaluate ordinary A/B during and after the update deadline, including B tasks that cannot wait for adaptation to finish.

### CE4-20 · Keep a reusable experiment-to-update map, not two cached answers — PRIMITIVE
- **Mechanism:** Fit a compact mapping from legitimate experiment outcomes to constraints on a fresh executable weight edit. The map can remain valid when an independent new target changes the needed delta, and tests each new completion against the current common effect.
- **Nearest prior / gap:** [DAD][dad] amortizes design selection and [multiparametric programming][mpc] amortizes solutions over varying parameters. The candidate keeps a decision-carrying interface between experiments and downstream fitting, rather than transferring precomputed branch parameters.
- **Cheapest first test / control:** In E/R learn on endpoint outcomes and hold out novel effect targets within each scope branch. Compare commit-and-reserve with a signed spare coefficient, an explicit piecewise solution map, and a fresh solver with the same time, storage and effect constraints. Require old branch copies to miss the new target.
- **Old-task retention:** Check ordinary old tasks from both response regimes after each newly fitted target; the branch not chosen for C still has its old behavior.

## D · CE3-08 × CE3-21: Test what survives a further ordinary change

### CE4-21 · Keep the experiment possible after one unrelated legal write — PRIMITIVE
- **Mechanism:** Select a common placement with a lawful alternative experiment path for each allowed intervening D change. The later learner may substitute a path but cannot roll back D or recover the old availability by replaying the original model.
- **Nearest prior / gap:** [Contingency-aware reachability][reach] retains fallback paths under disturbances and [distributionally robust recourse][robrec] seeks actions resilient to model changes. The candidate's contingency is caused by mandatory *weight learning* before scope has resolved, rather than by an externally actuated state change alone.
- **Cheapest first test / control:** Rotating a small encoder feature on D removes the most direct probe; another legal route survives only for one common placement. Compare commit-and-reserve with a signed spare coefficient with the same replacement route search, reparameterized DAD and exact recourse planning against the same D set.
- **Old-task retention:** Test A/B through the intervening D update, then again after the substitute experiment and the remaining C edit.

### CE4-22 · Complete one reading without making the next ambiguity unlearnable — PRIMITIVE
- **Mechanism:** After the first experiment resolves C, choose among C completions that keep a lawful experiment and an eligible write available for a different pending D. The first pair can agree on changing C while differing on which independent question remains askable.
- **Nearest prior / gap:** [Robust MPC][terminal] uses conditions for future feasibility and [adjustable robust optimization][adjust] plans recourse across scenarios. The candidate is a composable next-write/next-experiment condition consumed by an ordinary completion, not indefinite reservation of an edit slot.
- **Cheapest first test / control:** Enumerate two successive scoped requests and a known finite menu of experiments, then withhold D's outcome. Compare commit-and-reserve with a signed spare coefficient reoptimized at each legitimate horizon, and receding-horizon joint planning with the same D knowledge and compute.
- **Old-task retention:** Retest A/B at C commit, during the D experiment and after D; preserve C’s completed behavior independently of old A/B.

### CE4-23 · Exploit evidence from the ordinary path without conditioning on the wrong group — PRIMITIVE
- **Mechanism:** A useful first write changes who reaches an observed event. When rebuilding the scope exercise, retain a lawful comparison using denominators from the ordinary exposure process, or choose a placement with an identifiable comparison. Do not count extra reach to the event as better experiment success.
- **Nearest prior / gap:** [Performative Prediction][perform] studies model-dependent data and [goal-oriented causal design][goal] targets a causal quantity. The hypothesis is an outcome-decoding rule transported jointly with the placement, preserving which ordinary comparisons can license a later **parameter** change.
- **Cheapest first test / control:** Make two equal-effect edits induce different selection on a hidden subgroup; include a design with observable exposure counts and one with nonidentification. Compare commit-and-reserve with a signed spare coefficient plus the same valid correction, and an exact propensity-aware joint planner. Hold out the group used in fit.
- **Old-task retention:** Check A/B conditional on eligible exposure *and* as naturally served, keeping a separate rare population outside the query sample.

### CE4-24 · Require useful evidence under corrupted observations, not just an open route — PRIMITIVE
- **Mechanism:** Select a common write whose experiment keeps a lawful next edit justifiable under a declared corruption model. If one observation can lie within a bound, preserve an independently generated corroboration or a robust contrast; a more confident classifier alone cannot authorize the edit.
- **Nearest prior / gap:** [Noisy Bayesian active learning][noisy] designs tests under noisy observations; [conformal risk control][conformal] calibrates expected risk under its assumptions. The candidate makes the *weight placement* preserve independent evidence needed to finish a pending write, not a guarantee against arbitrary noise.
- **Cheapest first test / control:** Let two placements offer one clean-looking but correlated path and two sometimes-disagreeing independent paths at the same query cap. Specify the noise process before fitting. Compare commit-and-reserve with a signed spare coefficient, DAD with the same likelihoods, robust decision-region querying, and exact joint planning. Count erroneous authorizations.
- **Old-task retention:** Check rare B past wrong-looking observations and after valid corroboration, not only in trials where the evidence was clean.

### CE4-25 · Make the experiment itself supply a new legal direction — PRIMITIVE
- **Mechanism:** The exercise's observation can furnish a new input/output contrast that determines the orientation of the next rank-1 update, not just a scalar on a frozen vector. Choose a common placement where each possible observed orientation admits the proper edit under old floors.
- **Nearest prior / gap:** [InfLoRA][inf] allocates update subspaces from learned data and [AlphaEdit][alpha] constrains write orientation. The candidate binds a legitimate experiment outcome to constructing the next writable direction, with the first edit chosen so that construction works for either reading.
- **Cheapest first test / control:** In a learned small head, vary the completion orientation continuously within both branches, conditioned on a fresh observation. Compare commit-and-reserve with a signed spare coefficient, the same information given to ordinary post-result InfLoRA/refitting, and multiple spare directions at same cost. Include the collinear null.
- **Old-task retention:** Test old groups exposed to the newly fitted direction after each branch; compare to exact same-floor constrained refits on the old anchors.

### CE4-26 · Leave a lawful alternate lesson when the planned outcome becomes unusable — PRIMITIVE
- **Mechanism:** A common placement preserves a route to one experiment and a second procedure to obtain equivalent authorizing evidence if the first result is late, missing, or invalidated by D. It cannot learn from a timeout as if it identified the latent reading; it can only switch to a legally comparable lesson.
- **Nearest prior / gap:** [DAD][dad] already plans adaptive experiments and [predictive state representations][psr] encode alternative tests. The candidate is a fallback that specifically preserves the authorization and reachability of a future weight edit across a changing learner, not general experimental redundancy.
- **Cheapest first test / control:** Introduce observation failure independent of interpretation, then a failure predictive of interpretation to test the invalid shortcut. Compare commit-and-reserve with a signed spare coefficient and the same fallback access, optimal adaptive design with failures, and one dedicated query. Compare at the same completion deadline.
- **Old-task retention:** Score ordinary A/B before the failed test, during any fallback task, and after each lawful completion or hold.

## Ranked deeper questions

1. **Can an equal-effect first weight write keep both non-collinear completions reachable without merely storing their directions?** Start with CE4-01, CE4-05 and CE4-25. Run the signed-spare collinear null first, then allow the best common anchor and matched multi-spare/branch selectors in the non-collinear case. Seek a learned, held-out separation when target orientations arrive late, not just an algebraic impossibility constructed by ruling out the control.
2. **Can a useful weight write preserve its own experiment without simply acting like a conservative policy or a separate planner?** Start with CE4-08, CE4-09 and CE4-14. Require equal nominal C benefit and an ordinary A/B floor, and compare SPIBB, the signed-spare control with the same planner, post-write DAD and a same-cost dedicated exercise. Count lawful scope resolution, not visits. A learned environment must support the comparison beyond expert-specified dynamics.
3. **When is reachable and learnable recourse strictly harder than each on its own?** Start with CE4-15–CE4-17. Independently vary the writable layer and the availability and semantics of the observation; include a cell where the separately chosen best first write and experiment fail only together. Compare the strongest stacked controls to an exact joint solver at matched retained bytes and update/action work, not to whichever half is weaker.
4. **Does the mechanism survive one further ordinary update without a dormant checkpoint or a route exclusive to a single future?** Start with CE4-21, CE4-22 and CE4-26. Blind the first learner to the next D change and measure ordinary retention throughout. An explicit refit, refreshed signed spare or receding-horizon dual planner is a legitimate winner; only extra lawful continuations or reduced cost at the same floor count.

[triage]: https://github.com/manojbajaj95/cl/blob/f0df5d148bd15641297f146d814d0c4e320c9b5d/reviews/flood-triage.md#L477
[spare]: https://github.com/manojbajaj95/cl/blob/f0df5d148bd15641297f146d814d0c4e320c9b5d/reviews/flood-triage.md#L476
[ledger]: https://github.com/manojbajaj95/cl/blob/f0df5d148bd15641297f146d814d0c4e320c9b5d/reviews/idea-ledger.md
[adalora]: https://arxiv.org/abs/2303.10512
[alpha]: https://arxiv.org/abs/2410.02355
[spibb]: https://proceedings.mlr.press/v97/laroche19a.html
[dual]: https://proceedings.mlr.press/v120/arcari20a.html
[dad]: https://proceedings.mlr.press/v139/foster21a.html
[adjust]: https://arxiv.org/abs/1805.10079
[fixedrank]: https://doi.org/10.1137/110845768
[reach]: https://arxiv.org/abs/2603.17022
[maml]: https://proceedings.mlr.press/v70/finn17a.html
[inf]: https://arxiv.org/abs/2404.00228
[mpc]: https://cse.lab.imtlucca.it/~bemporad/publications/papers/acc00-mpqp.pdf
[olora]: https://aclanthology.org/2023.findings-emnlp.715/
[trans]: https://arxiv.org/abs/2405.17258
[perform]: https://proceedings.mlr.press/v119/perdomo20a.html
[goal]: https://arxiv.org/abs/2507.07359
[safemdp]: https://proceedings.neurips.cc/paper_files/paper/2016/hash/9a49a25d845a483fae4be7e341368e36-Abstract.html
[psr]: https://proceedings.neurips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html
[agi]: https://arxiv.org/abs/2406.00392
[drr]: https://proceedings.mlr.press/v33/javdani14.html
[robrec]: https://arxiv.org/abs/2302.11211
[terminal]: https://doi.org/10.1002/rnc.5409
[noisy]: https://arxiv.org/abs/1010.3091
[conformal]: https://arxiv.org/abs/2208.02814
