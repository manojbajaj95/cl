# Learning Economics 5: Preserved Second Teaching Routes

Child of [learning-economics-4.md](learning-economics-4.md) ([PR #329]) · 26 idea cards · Ideas only; no experiments run

**Why this node exists.** The reviewer gave two cards score 3 in [flood-triage row 447][triage]: **LE4-01**, keep two source-disjoint gradient cones open, and **LE4-04**, taking the first exit must not close the other. The question is not whether two sellers can teach from the handoff checkpoint. It is whether they can still teach **in sequence on one live learner**, when the first entrant optimizes only its own objective, and whether the first teacher can change that outcome with the lessons it chooses.

## What would count as a preserved route?

- **Define the counterfactual before pricing it.** Let `C_B(s)` be the number of ordinary B examples a fixed entrant needs to reach the Extension 2 loss target while meeting the applicable retention floors from state `s`, within a fixed step cap. Use paired B streams to compare the handoff checkpoint `s_0` to the live state `s_A` after a successful A update. Report completion rates and paired cost differences when both routes finish; report one-sided cost bounds when only one finishes. For this diagnostic comparison use the same old-task floors in both arms and report A's retention separately; for an operational finish from `s_A`, also require the floor on A's extension. Compare successful first-hop states matched on Extension 1 loss and old retention: the reset arm is a diagnostic, not a deployable policy. Swap sources when the world admits it. A and B must draw from independent upstream feeds (not different names for one labeler); enforce this by construction in the first fixture and include a shared-feed negative control.
- **A gradient cone is a candidate witness, not a certificate by itself.** Build it from updates an ordinary entrant can actually obtain using its own examples and optimizer. In a diagnostic copy compare their images on fixed prediction probes (including unseen extension probes), filtering by old-task damage and by nontrivial progress. Guard against scale, rank, and parameter gauge: include [PR #104]'s function-equal rescaling as a null under matched effective steps and report actual finite-step completion with the deployed optimizer. Separation without teachability is not a win; shared directions are allowed when they demonstrably do not bottleneck the two routes.
- **Run LE4-26 first.** Cross incumbent lesson/representation (ordinary vs proposed) with source supply (independent vs shared-bottleneck), holding source IDs, stream lengths and label rights fixed. Score old tasks and finite-step costs in all cells. A supply-only gain is not a learner-state result; a representation gain that also occurs under shared supply may be useful but does not establish a *source-disjoint* mechanism. Then compare with LE3-03 static two-exit + LE3-12 second-use gates, ordinary same-capacity shared-trunk training, open replay, and a same-powers central buyer. Add LE4-01 + LE4-04 stacked as the closest parent control when combining them. If the planner ties with the same information, action set and commitment, keep the learning mechanism, not a market claim.
- **Match budget and keep the transition honest.** Count incumbent examples, audit examples, update steps, width/rank, and persistent bytes; charge extra probes and offline training. No future labels for the incumbent: use public precursor families and draw unseen targets after commitment. Unless a card explicitly tests a change to an entrant's interface, entrants do not coordinate or inherit each other's private data, optimizer state, masks or hints. No restore on the measured live path.
- **Old-task check in every first test.** Pretrain two normal tasks, one rare, including examples with independently useful A and B cues. Report per-task loss and worst-slice drop before teaching, after A, and after B, using ordinary prediction with no task IDs, teacher hints or restores. Apply preregistered per-task floors, including the first extension after B, at matched new-task progress. Check the outage slices separately on old examples for which the remaining inputs still identify the answer.

**Literature check.** Read the [idea ledger][ledger] first and consulted the research memory. Searched alphaXiv `discover_papers` for cross-modal interference and dormant learnability, finite-step machine teaching, and gradient transport/projection; cross-checked with Hugging Face Papers searches for gradient projection, continual backprop, gradient surgery, task arithmetic and iterative teaching, and read the cited arXiv abstracts. In particular, [PGGB] already directly boosts weak-modality gradients, [GPM] and [Octopus] already use orthogonalization for continual learning, and [OML] and [La-MAML] already optimize future online adaptation. [Co-observation] and [Cross-modal Adaptation] already separate useful aspects of sequential learning from forgetting. The ledger rules out a Gramian-only reserve score, a gauge change that only changes effective LR, or a merged card that ties its stacked parts. The gaps below are hypotheses relative to the closest papers found, not claims of exhaustive novelty. **P** denotes a candidate reusable operation; **I** denotes an improvement or discriminating audit.

## A · LE4-01: Turn source-disjoint cones into usable update routes

### LE5-01 · Teach on a shared trunk, spend on disjoint residuals — P
- **Mechanism / learner effect:** Teach a shared representation for old prediction but choose incumbent examples that make source-private residual updates independently useful on new targets. Subsidize residual progress, not feature dissimilarity: each source must move a different extension probe while the shared predictor stays useful.
- **Nearest prior / gap:** [Feature Sieve] suppresses simple features to elicit complementary ones; [GPM] protects old subspaces. The proposed teaching target is two *source-obtainable residual updates* on one live representation, beyond the protected shared subspace.
- **Cheapest first test:** Fit a rank-two linear trunk to common rules plus two source-specific residuals; choose among equal-size incumbent lesson subsets. Compare feature sieving plus equal-rank GPM and a random two-slot split. Reject if either gets the same B finish rate after A at equal A progress.
- **Old-task retention:** In addition to the shared old rule, check rare old cases whose prediction needs the common trunk and one residual together.

### LE5-02 · Sell a balanced set of teaching examples, not a wide gradient cone — P
- **Mechanism / learner effect:** Find a small basket of A examples whose updates jointly accomplish A's extension but cancel their displacement on B's learning probes; teach the representation so such baskets exist among ordinary data. B does not supply co-training gradients during A's hop.
- **Nearest prior / gap:** [PCGrad] projects observed conflicting task gradients; [Iterative Teaching] selects examples for fast convergence. Here cancellation must be achievable by legal source-local example selection with nonnegative counts, and B's finite-step progress is the protected quantity.
- **Cheapest first test:** Enumerate two-example batches for a bilinear regressor. Compare A-only greedy teaching, PCGrad with equally charged probe access, and random balanced batches. Reject if cancellation needs negative weights or if it does not lower held-out B cost.
- **Old-task retention:** Check the rare old boundary examples most likely to move when two opposite updates cancel on B but not on old prediction probes.

### LE5-03 · Buy separation that survives the removal of one lesson — P
- **Mechanism / learner effect:** Select a precursor set so each source has a working residual update after any one precursor example is withheld. Target distinct *support* for the directions, not just orthogonal directions supported by the same rare anchor.
- **Nearest prior / gap:** [Nonparametric Teaching] selects examples for rapid function-space convergence; [DivDis] diversifies predictive hypotheses. Here the backup is a different training witness for a subsequent update, not a different fitted predictor.
- **Cheapest first test:** Enumerate three-of-five example lessons in a two-factor model, withholding each lesson example in turn before training. Compare random redundancy and static two-exit diversity with the same lesson length. Reject if the worst withheld-case B cost ties.
- **Old-task retention:** Include old cases that the missing precursor was useful for, to catch a design that pays for redundant exits by dropping an old exception.

### LE5-04 · Teach separated effects, even when the weights move together — P
- **Mechanism / learner effect:** Select precursor examples using the ratio of progress on a source's own probe to adverse movement on the other source's probe per legal update. Two parameter updates can overlap strongly yet have different functional effects; favor those over harmless-looking orthogonal weight changes with colliding effects.
- **Nearest prior / gap:** [OGD] projects to avoid changing old outputs; [Nonparametric Teaching] teaches in function space. This scores *directed future cross-effects* between two entrant update sets before the targets are known.
- **Cheapest first test:** Construct two function-equivalent factorized linear checkpoints and two lessons with similar weight cosines. Compare equal-rank GPM, normalized parameter-angle selection, and selecting on first-hop progress alone. Reject if effects do not predict or improve finite-step B finish beyond the effective-step control.
- **Old-task retention:** Score the full old mix, including cases off the small probe set, to expose protection that only works on the measured output coordinates.

### LE5-05 · Teach an escape from a cone that is only wide on paper — P
- **Mechanism / learner effect:** Require two *successive* useful directions from each source's ordinary examples after its first legal step. Choose lessons that keep the second direction accessible rather than spending the only transition that exposes it. This buys curvature of a feasible teaching route, not a large initial Jacobian.
- **Nearest prior / gap:** [GPM] builds activation bases from completed tasks; [Order Bracket] uses gradient-field order to predict forgetting. Neither first-step geometric signal guarantees a second usable example from a constrained source.
- **Cheapest first test:** Two-layer gated regressor where one admissible update can turn off the only source-private gate. Select among equal-size two-example lessons using one- versus two-step branches. Reject if the two-step selector cannot beat direct B-cost lookahead or the parent cone gate on held-out lessons.
- **Old-task retention:** Record rare old losses after the first and second A steps, not just after training returns to a safe endpoint.

### LE5-06 · Design a lesson with a substitute gradient, not a substitute label — P
- **Mechanism / learner effect:** Teach a latent coordinate so one source can supply an ordinary pairwise comparison and the other an ordinary point label, each yielding a usable but distinct continuation of the shared skill. No interface translating B labels into inaccessible A labels is carried into the second hop.
- **Nearest prior / gap:** [Multimodal Teaching] already selects complementary feedback across environments for reward identification. Here two feedback types must independently drive *live updates* after one type has already changed the fit.
- **Cheapest first test:** Small ordinal regressor; give A only comparisons and B only point labels, both sufficient for the corresponding extension. Compare joint mixed-feedback teaching and independent heads with equal scalar observations and matched steps. Reject if either preserves B cost just as well.
- **Old-task retention:** Score both old ranking consistency and rare absolute-threshold decisions; a monotone rescaling can preserve one while destroying the other.

### LE5-07 · Try to counterfeit an open cone — I
- **Mechanism / learner effect:** Insert a nuisance branch that can absorb arbitrarily large gradients without changing a target prediction. Use it to estimate how often an angle or effective-rank payment buys a decorative degree of freedom rather than a viable update.
- **Nearest prior / gap:** [DivDis] explicitly diversifies predictions; [GPM] uses subspace directions for stability. This is a falsification of source-route accounting, not a new projection method.
- **Cheapest first test:** Attach redundant features to the same two-source regressor at equal parameter count across arms. Compare raw angles, margin-matched output effects and actual finish cost. Drop any geometric gate that a useless branch can satisfy.
- **Old-task retention:** Include a rare slice near the common decision threshold so the audit also detects a false positive caused by trading old margin for a larger gradient signal.

### LE5-08 · Find where sharing beats separation — I
- **Mechanism / learner effect:** Trace where forcing orthogonality is harmful: independent feeds can teach a common latent rule, and A's successful step can make B cheaper despite near-identical gradients. Admit shared directions when the measured second route survives.
- **Nearest prior / gap:** [PGGB] balances jointly observed modalities and [Cross-modal Contributions] analyzes modality roles across environments. This test asks when a *prospective* separation contract should refuse to penalize genuine positive transfer.
- **Cheapest first test:** Sweep true rule overlap in a linear two-source model, including identical target directions but independent upstream samples. Compare the parent cone requirement, gradient diversity and a B-finish-only gate. Reject separation as a universal requirement if it makes B slower at matched A progress.
- **Old-task retention:** Check a frequent old rule shared by both sources and a rare old exception served by only one.

## B · LE4-04: Keep the unused route teachable through a live first exit

### LE5-09 · Train a lesson to hold B's update response fixed while A moves — P
- **Mechanism / learner effect:** Match how a source-B support step changes predictions on separate B query probes *before and after* an ordinary A update. Teach with this difference as a target, not a penalty on B's current logits. Labels for actual Extension 2 remain hidden until the handoff.
- **Nearest prior / gap:** [CMCDR] regularizes modality contribution to previous predictions; [La-MAML] looks ahead to mitigate interference. Here the target of preservation is an unused source's support-to-query response, with no modification to A's deployed update.
- **Cheapest first test:** Enumerate precursor labels for a two-view width-four MLP; choose on held-out precursor probe response. Compare CMCDR + [Continual Backprop], La-MAML, and direct B lookahead on the same precursor draws. Reject if unseen B finish cost does not improve at matched A loss.
- **Old-task retention:** Require the old-view A and B slices to pass after A alone and again after B; retention from a good B response is not assumed.

### LE5-10 · Buy recovery along the first entrant's normal forward path — P
- **Mechanism / learner effect:** Distinguish permanent closure from a temporary loss of B sensitivity that A's next useful examples can reopen. Teach a representation with a cheap A-only continuation that advances A and reopens B, without rollback, B labels, or discarding A progress.
- **Nearest prior / gap:** [Trust-Region CL] combines replay and a Fisher constraint to re-converge to prior optima. Here the recovered object has never been learned, and the repair consists only of forward ordinary learning on A.
- **Cheapest first test:** In a saturating shared-unit MLP, commit A to an ordinary common-prefix stream with two possible next batches. Compare equal-step no-op/wait, generic refresh, replay and A-only loss selection. Reject if the reopening is reproducible just by reducing effective step size.
- **Old-task retention:** Watch the rare old slice at maximum B suppression and after reopening; a good final checkpoint cannot erase an interim floor violation.

### LE5-11 · Make B's latent code survive A by using inactive examples, not inactive units — P
- **Mechanism / learner effect:** Teach B-relevant coordinate contrasts inside examples that A's local loss can already score correctly, so A's later updates have little drive to erase those contrasts. Unlike spare units, those coordinates must already contribute to shared old prediction and to a compositional B extension.
- **Nearest prior / gap:** [Continual Backprop] replaces underused units; [Cross-modal Adaptation] shows the benefits of modality-specific isolation. This attempts preservation in *used shared capacity* through the placement of examples rather than replacement or isolation.
- **Cheapest first test:** Two-view parity-plus-threshold MLP; contrast matched incumbent lessons that teach the same A margin but arrange B-relevant contrasts differently. Compare random reserve capacity, unit refresh, and ordinary multitask pretraining. Reject if removing the claimed contrast leaves B cost unchanged.
- **Old-task retention:** Include an old compositional task that fails if the shared contrast is disabled; check it after both hops without routing.

### LE5-12 · Teach first-hop examples whose gradients turn away before the bottleneck — P
- **Mechanism / learner effect:** Move the shared feature's saturation boundary upstream so A's hard examples remain learnable but the gradient of its already-solved examples shrinks *before* they can kill the dormant B feature. Select lessons by where this turnover occurs along an ordinary A curve.
- **Nearest prior / gap:** [PGGB] adjusts gradient magnitude online with weak-modality probes; [Continual Backprop] refreshes capacity. Here the incumbent sets a data-dependent turnover in an unchanged optimizer when B is absent.
- **Cheapest first test:** Two-feature tanh regressor with staggered A difficulty. Compare margin- and effective-LR-matched lesson variants, gradient clipping, and generic plasticity-preserving training. Reject if a global downscale matches the A trajectory and the B-cost gain.
- **Old-task retention:** Separate rare old low-margin cases from easy old cases and match their initial margins before attributing any difference to the turnover.

### LE5-13 · Make A's new feature the amplifier for B's first lesson — P
- **Mechanism / learner effect:** Teach a shared factorization in which installing A's missing factor raises the sensitivity to B's independent signal. B must then learn a genuinely new factor, not merely get higher zero-shot accuracy from A.
- **Nearest prior / gap:** [OML] learns representations for fast online learning; [Co-observation] shows joint data access can help representation. Here sequential, disjoint sources must create a *positive cross-update interaction* without joint access during either hop.
- **Cheapest first test:** Three-factor bilinear regression with hidden B residual. Compare B finish after A versus a retention- and A-progress-matched factorization, open replay, and the same-rank joint precursor baseline. Reject if the gap disappears after matching B's starting loss or if random unused capacity ties.
- **Old-task retention:** Test an old factor composition and a rare exception that breaks naive multiplicative generalization, at both handoffs.

### LE5-14 · Pass every ordinary prefix, not only the endpoint — P
- **Mechanism / learner effect:** Select incumbent lessons for a bound on B finish cost along successful A prefixes that could be real interruption points. A can temporarily cross a dead gate and reopen it by the end; an endpoint payment misses the period in which a source outage would strand the learner.
- **Nearest prior / gap:** [Time-Constrained Robust MDPs] models structured changes in environmental uncertainty; [Order Bracket] analyzes endpoint order effects. This buys *new-target teachability at a live training prefix*, with no choice of A policy at deployment.
- **Cheapest first test:** Enumerate three legal stopping points in a gated linear curriculum with equal endpoint loss. Compare LE4-04 endpoint payment, the parent interruption covenant, and equal-budget prefix replay. Reject if the new objective adds no held-out worst-prefix benefit over the stacked controls.
- **Old-task retention:** Measure old losses at every interruption candidate and after B takes over from the worst prefix.

### LE5-15 · Preserve B by letting its activity move to another shared coordinate — P
- **Mechanism / learner effect:** Teach redundant factorizations of the *same* old shared feature so A can change the dominant carrier while B's examples automatically act through a different live one. B's optimizer and data stay fixed; success is relocation of effective update, not a handoff token.
- **Nearest prior / gap:** [Octopus] orthogonalizes gradients during fine-tuning; [Task Arithmetic] manipulates stored parameter deltas. This asks for endogenous reassignment of B's learning response with no saved delta or mask.
- **Cheapest first test:** Width-three linear factorization with a shared feature and overlapping residuals. Compare GPM, equal-width isolated branches, and random gauge-preserving rebalances. Reject if the result is only an effective-LR change or survives disabling the proposed alternate carrier.
- **Old-task retention:** Score an old example requiring the shared feature and a rare example requiring the outgoing carrier's residual after both entrants update.

### LE5-16 · Trace the closure to a specific live write — I
- **Mechanism / learner effect:** In diagnostic copies, replay the same A examples while independently matching batch order, optimizer state, and A endpoint progress; transplant only the suspected feature block in the smallest controlled model. Ask which state change is necessary for the B-cost jump.
- **Nearest prior / gap:** [Cross-modal Adaptation] compares cross-modal interference across adaptation architectures; [Order Bracket] links order to forgetting. The outcome here is causal responsibility for the loss of an *untrained* continuation, not evidence from existing task scores or angle correlations.
- **Cheapest first test:** Two-view MLP with one shared and one private block. Compare same examples/no update, a progress-matched A write, and block swaps plus sham swaps. Drop the feature claim if resetting moment estimates alone explains the effect. Diagnostic swaps are not permitted in the live winning arm.
- **Old-task retention:** Require donor and recipient checkpoints to match old losses, then recheck old and rare slices after every swap to identify hybrids that are simply broken.

### LE5-17 · Separate lost B learnability from the loss of A-compatible B examples — I
- **Mechanism / learner effect:** Cross the post-A checkpoint with a B stream resampled to have the same relationship to A's target as before the handoff. This separates a state that no longer responds to B from a sampling process that stopped exposing informative B residuals.
- **Nearest prior / gap:** [Co-observation] controls data access to separate representational effects from retention and plasticity; [Heterogeneous Data Game] varies source mixtures. Here the distinguishing signal is the state-by-stream interaction on an identical second-hop target.
- **Cheapest first test:** Use two independent label feeds with optionally outcome-dependent sampling. Cross natural and progress-matched A states against fixed and outcome-filtered B streams. If the difference vanishes on the fixed stream, do not call it weight-level closure.
- **Old-task retention:** Use a fixed old mix, not the resampled B stream; separately score the rare old group most likely to disappear under the sampling rule.

## C · Make cone separation and live preservation earn their combination

### LE5-18 · Teach one source to reveal a second independent residual route — P
- **Mechanism / learner effect:** Buy a precursor representation in which A's update resolves a shared ambiguity and thereby makes an ordinary B example informative about a distinct residual. Unlike static cone preservation, permit B to start weak, but require a second independent update that works after the first live use.
- **Nearest prior / gap:** [DivDis] uses additional supervision to select among already-diverse hypotheses; [Iterative Teaching] chooses efficient next examples. Here the first source creates new learnability for a second source rather than directly selecting the final hypothesis.
- **Cheapest first test:** Two-factor regression with a sign ambiguity: A data identify one factor; unseen B examples must fit the other. Compare direct joint teaching, held-out B lookahead and stacked parent gates at equal budgets. Reject if A simply supplies B's answer or if starting B loss explains the gain.
- **Old-task retention:** Old sign-insensitive and rare sign-sensitive examples must both pass; resolving the new ambiguity must not silently flip the old convention.

### LE5-19 · Sell an examples-only repair that restores B without undoing A — P
- **Mechanism / learner effect:** If A did close the B route, buy a small third-party set of ordinary, target-blind precursor examples that rewires the local response while keeping both A's acquired skill and old predictions. The repair teacher does not supply B's held-out label or private A data.
- **Nearest prior / gap:** [DUET] projects to preserve previous and current loss; [CPLUS] uses self-probe gradients to protect prior behavior. Here a data-only live repair targets a future gradient path, with explicit floors on both installed capabilities.
- **Cheapest first test:** Enumerate eligible repair batches for a two-layer MLP after a verified closure. Compare equal-cost generic refresh, old replay plus DUET, direct B training with the same total examples, and a full state-restore diagnostic. Reject if replay or extra B examples tie without more rights.
- **Old-task retention:** Score old tasks and A immediately before and after repair and again after B, including old rare cases that share the repaired feature.

### LE5-20 · Buy a smaller public teaching interface by composing portable routes — P
- **Mechanism / learner effect:** Teach two source interfaces whose updates both use a compact common bottleneck but leave independent residuals. Pay only if the exposed bottleneck rank needed to teach sequentially drops versus two separately bought routes; keep architecture and total trainable rank fixed.
- **Nearest prior / gap:** [GPM] compresses retained-task bases and [Octopus] enforces update separation without historic data. This prices *minimum shared interface rank for finite-step sequential teachability*, not rank for reconstructing old features.
- **Cheapest first test:** Enumerate one- to three-dimensional public representations for a two-source regression world. Compare equal-rank GPM, a per-source split and concatenated parent routes, charging storage and all pretraining. Reject if rank savings are lost on a held-out composition or obtained by hiding private state.
- **Old-task retention:** Compact interfaces must retain an old joint-input example that cannot be solved from either private residual alone.

### LE5-21 · Teach an update that tolerates the other source's unknown units — P
- **Mechanism / learner effect:** Fix the public training interface but keep the other entrant's input scaling private. Choose precursor data that induce stable route effects across plausible input units; protect not only the directions but the useful step lengths of the unused source after A.
- **Nearest prior / gap:** [PGGB] adapts online to differing gradient strengths; [La-MAML] learns per-parameter rates. The proposed object is a lesson that protects finite-step learnability under source-local measurement units without deploying either intervention.
- **Cheapest first test:** Rescale B sensor values over a small hidden grid after A commits. Compare plain standardization, a coordinate-matched adaptive optimizer, and stacked parent gates. Reject if normalization alone ties or if apparent benefit comes from a lower effective rate for A.
- **Old-task retention:** Score each old task in its original units and a held-out calibration slice to distinguish ordinary retained behavior from an accidental interface remapping.

### LE5-22 · Purchase two independent ways of reopening the same continuation — P
- **Mechanism / learner effect:** Where a closure cannot be prevented cheaply, train the representation so either of two disjoint repair sources can restore B's learnability without copying the other's example or erasing A. Diversity is now a property of *repairs to teachability*, not of final solutions.
- **Nearest prior / gap:** [Continual Coverage] ensures active contract coverage under uncertain prices; [DUET] preserves current and previous task losses through projection. Neither makes future learning recoverable through two disjoint, ordinary source streams.
- **Cheapest first test:** In a four-feed toy regressor (A, B and two repair feeds), enumerate two repair batches following the same A closure. Compare a single generic repair repeated twice, LE5-19 plus static seller diversity, and same-rank elastic capacity. Reject if the apparent pair relies on one shared calibrator or if one generic repair ties under independent outages.
- **Old-task retention:** Check old and A floors on each alternative repair branch and on its actual B continuation, not an average across them.

### LE5-23 · Buy a contract that charges for consuming someone else's teaching option — P
- **Mechanism / learner effect:** Set an incumbent payment held back in proportion to excess B examples after a randomized real A hop versus a progress-matched reference hop; allow a neutral auditor to reveal only the score. Test if the contingent amount changes the incumbent's *lesson choice* and the learner's response, not merely price or seller entry.
- **Nearest prior / gap:** [Optimal Contracts] learns outcome-dependent payments for hidden actions; [Heterogeneous Data Game] analyzes competition over data sources. Here the hidden action changes a subsequent teacher's admissible updates, and the outcome is paired learner-state cost with supply held fixed.
- **Cheapest first test:** Enumerate two lessons, two private seller costs and two A streams using the LE4-26 grid. Compare the fixed fee, static LE4-01, sequential LE4-04, their stack and the same-powers planner. If the planner ties, there is no independent market primitive; if the payout never changes lesson choice, drop the contract.
- **Old-task retention:** All branches counted as completed must retain rare old performance and A's new skill; a low-cost B finish after dropping one does not earn payment.

### LE5-24 · Discount directions that are consumed in the first successful gradient step — P
- **Mechanism / learner effect:** Price a useful direction by the B progress still attainable after an entire *set* of equally good A steps, not by the pre-update angle or a single convenient trajectory. Choose an incumbent lesson that changes the shared representation so none of the admitted A steps is a cheap way to foreclose B.
- **Nearest prior / gap:** [Time-Constrained Robust MDPs] constrains how uncertainty changes and [La-MAML] learns from lookahead. Here the uncertainty set contains progress-matched source-local training actions and the protected payoff is an entrant's future sample cost.
- **Cheapest first test:** Enumerate two A batches with matching progress in a gated network, only one of which consumes a shared feature. Compare mean-case and worst-case lookahead at the same audit budget, plus the stacked parent gates. Reject if the robust variant merely removes a valid A route or ties on held-out A draws.
- **Old-task retention:** Apply old and rare-slice floors on each admitted A trajectory, including the one with the highest B cost.

### LE5-25 · Try to separate route closure from generic plasticity loss — I
- **Mechanism / learner effect:** Add a fresh C extension with the same starting loss, target difficulty and sample budget as B, but no reliance on B's putative path. The contrast of B's and C's cost changes distinguishes selective closure from a model that has simply stopped learning.
- **Nearest prior / gap:** [Continual Backprop] directly tests general loss of learnability, and [Cross-modal Adaptation] measures asymmetries in cross-modal interference. The audit is a source-selective causal contrast at matched initial difficulty, not another generic plasticity score.
- **Cheapest first test:** Use one tiny factorized regressor and swap which latent factor C requires. Compare a true shared B bottleneck to uniform saturation with matched start losses and steps; calibrate against shrink-and-perturb or [Continual Backprop]. If costs move together, stop calling the effect route-specific.
- **Old-task retention:** Match and report common and rare old losses across B and C branches; the cost contrast is uninterpretable if C buys progress by forgetting more.

### LE5-26 · Test whether two routes still matter when checked together — I
- **Mechanism / learner effect:** Cross the parent cone gate on/off with the parent live-preservation gate on/off, on the same incumbent lesson menu. Read out the set of source-disjoint transitions that remain affordable after successful updates, not the number of independently passing tests.
- **Nearest prior / gap:** [CMCDR] targets modality-contribution drift, [GPM] protects established subspaces, and [Continual Coverage] prices uninterrupted coverage. This is an interaction audit on live learnability, not a claim that combining these controls is new.
- **Cheapest first test:** After LE4-26, enumerate the four gate cells and add a same-powers planner that can choose any lesson and a stacked parent baseline. Include a shared-direction world where imposing both gates ought to lose. Keep a joint primitive only if it enlarges the held-out feasible region at matched progress and spend.
- **Old-task retention:** Plot that feasible region at fixed old-task floors, with the rare floor separate; an expansion obtained only by weakening a floor is not preservation.

## Ranked deeper questions

1. **Can the incumbent teach B's future update response to survive an unmodified A hop, without partitioning the model?** (LE5-09, LE5-13, LE5-25.) Run LE4-26 first, then require an unseen B-target gain at matched A progress and old retention over CMCDR, refresh and the parent stack; a matched C target tests whether this is selective or just generic plasticity.
2. **Which functional separation witness predicts a real second finish, and when is separation the wrong goal?** (LE5-02, LE5-04, LE5-07, LE5-08.) Demand that it beat a first-step or static angle baseline on held-out finite-step trajectories, reject decorative directions and admit useful shared-gradient cases.
3. **If the path closes, can legal examples reopen it without reverting the first entrant's learning?** (LE5-10, LE5-19, LE5-22.) Require an improvement over equal-budget replay, generic refresh and direct B examples; source-disjoint repair counts only with both previously installed sets of skills intact.
4. **When does paying for a preserved option do more than change which teacher gets paid?** (LE5-17, LE5-23, LE5-26.) Separate supply from representation, then require a lesson-choice and retention-safe learning effect over the same-powers planner and stacked parent gates before retaining a market claim.

[PR #329]: https://github.com/manojbajaj95/cl/pull/329
[PR #104]: https://github.com/manojbajaj95/cl/pull/104
[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L447
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[CMCDR]: https://arxiv.org/abs/2607.27260
[PGGB]: https://arxiv.org/abs/2611.02651
[GPM]: https://arxiv.org/abs/2103.09762
[OGD]: https://arxiv.org/abs/1910.07104
[PCGrad]: https://arxiv.org/abs/2001.06782
[Octopus]: https://arxiv.org/abs/2605.14938
[Continual Backprop]: https://arxiv.org/abs/2306.13812
[OML]: https://arxiv.org/abs/1905.12588
[La-MAML]: https://arxiv.org/abs/2007.13904
[DUET]: https://arxiv.org/abs/2611.29269
[CPLUS]: https://arxiv.org/abs/2609.32771
[Trust-Region CL]: https://arxiv.org/abs/2602.02417
[Co-observation]: https://arxiv.org/abs/2608.18803
[Cross-modal Adaptation]: https://arxiv.org/abs/2610.38436
[Cross-modal Contributions]: https://arxiv.org/abs/2606.14883
[Iterative Teaching]: https://arxiv.org/abs/1705.10470
[Nonparametric Teaching]: https://arxiv.org/abs/2306.03007
[Multimodal Teaching]: https://arxiv.org/abs/2607.08647
[DivDis]: https://arxiv.org/abs/2202.03418
[Feature Sieve]: https://arxiv.org/abs/2301.13293
[Order Bracket]: https://arxiv.org/abs/2611.20087
[Task Arithmetic]: https://arxiv.org/abs/2212.04089
[Time-Constrained Robust MDPs]: https://arxiv.org/abs/2406.08395
[Heterogeneous Data Game]: https://arxiv.org/abs/2505.07688
[Continual Coverage]: https://arxiv.org/abs/2605.16601
[Optimal Contracts]: https://arxiv.org/abs/2309.09801
