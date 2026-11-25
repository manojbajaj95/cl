# Learning Economics 3: How much of the learner can a teacher lock in?

**Depth 2 · 26 idea cards · Ideas only; no experiments or GPU.** Child of [Learning Economics 2](learning-economics-2.md) ([PR #326]), following the two score-3 ideas in [the reviewer's row 444][triage] on [PR #6][review]:

- **LE2-24 — reachability covenant.** An incumbent can build a monopoly into the learner with no exclusivity agreement: keep sending lessons that leave only the incumbent a short path to the next target. Bound entrant teaching distance at every exposed incumbent state, not just at handoff.
- **LE2-01 — pay on a substitute's sample cost.** The buyout pays only if a randomly drawn, independent entrant using ordinary examples can finish the job within a budget. Delivery alone is not success.

Read the [idea ledger][ledger] first. This node does not reprice the Nerode quotient, revive gauge preconditioning, forecast forgetting from first-order gradients, or claim a win for checkpoint restoration, sparse-damage recovery, replay, or teacher identity alone. The parent distance and payout are baselines, not new cards. The intended separation is **state-induced dependence versus genuine teacher advantage**: a seller that has intrinsically better examples may win even on a completely open learner. Buying from it is not evidence of lock-in.

## What would count as a limit?

- **Define the counterfactual at the switch.** Fix the new target, old-task floors, ordinary-example rights, entrant observations, compute, availability process and horizon. For a checkpoint *s*, ask for the least total number of ordinary examples permitting an implementable entrant policy to hit the new target and stay within the old floors at every exposed step, with a predeclared success probability. Count failed draws; record “not reached by horizon” rather than imputing a finite distance. Report absolute cost and excess over a matched open-curriculum checkpoint with comparable starting new error, old error and work. Pair the same future opportunities and seller types. An omniscient shortest path (and any target-aware control not given to real entrants) is only a lower bound.
- **Separate a capable replacement from a lucky audit.** Lock the entrant pool, target generator, outcome rule and eligible data *before* the incumbent chooses. Draw the evaluator teacher and future task after commitment; share neither test labels nor teacher-specific setup. Keep rejected, unavailable and timed-out draws in the denominator. Log elapsed time and a complete cost vector (examples, labels, updates, probes, setup, rights, persistent bytes and spend); never call a larger capability set a reduction in ordinary sample cost. When a card deliberately buys a new right, give the same right to its controls and report its price.
- **Test the learner and the procurement mechanism separately.** On CPU, enumerate the smallest game with genuine seller choices and best responses, then try the separating case using an actual learner (tabular update, factorized squared loss or tiny shared-feature classifier). Freeze the update rule within an arm; where a card changes it, give the same rule to the strongest allocation control. Compare per-label and delivery-based #324 LE01 buyouts, LE2-03 gap as a meter, LE2-01 cost-triggered buyout, LE2-24 covenant vs no covenant, translation, equal-example open replay, a teaching-dimension cap, and a genuinely better incumbent. Include a rule only finishable with special data. Use the relevant strongest controls **stacked** at equal cost. Run the same-powers central buyer and a full-information bound; if the former induces the same learning at the same cost, do not claim a distinct market mechanism. If a simple update or allocation ties at the same information and work, drop the proposed operation.
- **Retention in every first test.** Pretrain two unchanged ordinary tasks, one rare, including old exceptions to the emerging new rule. Score a fixed unseen mix on the live learner through ordinary prediction: before instruction, at exposed prefixes, after the switch and after later updates. No task IDs, teacher hints, incumbent routing, test-label access or restore for evaluation. Compare per-task loss and worst-slice drop with a predeclared no-new-learning floor, at matched new progress. Card-specific slices below are extra, not substitutes.

**Literature check.** Used Hugging Face Papers searches for machine teaching (including multiple teachers and limited observation), teacher switching and transfer, compatible representations, continual distillation, robust sequential control, gradient-based selection, adaptive holdouts and outcome contracts. Checked the linked primary arXiv records and abstracts for the specific comparisons. This is a targeted prior-art screen, not an exhaustive priority claim. In particular, [IMT] and [Sequential MT] already optimize teaching sequences; [UNIC] already learns an encoder from complementary teachers; [Stationary] already targets compatibility; [Contracts] already pays on a downstream outcome for hidden effort. None of those ingredients is new here. **P** denotes a candidate reusable operation; **I** an improvement or discriminating audit, not a reviewer verdict.

## A · LE2-24: preserve a way out at each exposed state

### LE3-01 · Let a real entrant take the next scheduled step — P
- **Mechanism / learner effect:** At a precommitted boundary, an entrant, not the incumbent, performs already-budgeted teaching. To keep the next installment, the incumbent must leave a state where that ordinary update both learns its assigned subskill and leaves the *following* entrant continuation short. This can change the basin the learner enters even if current scores are unchanged.
- **Nearest prior / gap:** [Sequential MT] uses optimal control to reach one target; [Sherpa] adapts teaching to individual student outcomes. The proposed operation is an exposed, productive substitution with a second independent continuation, not selecting a better first teacher or running shadow probes.
- **Cheapest first test:** Fit a two-feature classifier through three subgoals, where spending the next lesson on a source shortcut can improve subgoal two while making subgoal three slow. Compare the parent covenant plus equal-budget shadow audit and a fixed alternating curriculum; remove the third subgoal as a null.
- **Old-task retention:** Score rare old exceptions immediately after the live entrant update and after the third subgoal, including cases on which the shortcut was previously valid.

### LE3-02 · Permit a long planned detour only if every interruption has a short exit — P
- **Mechanism / learner effect:** Bind the covenant to an entrant policy that can respond to the interruption time, with the same public information a real replacement would see. A multi-step incumbent curriculum can take a detour only if each delivered prefix still has a bounded safe exit; a faster endpoint does not excuse an unusable intermediate representation.
- **Nearest prior / gap:** [Sequential MT] optimizes paths and [TC-RMDP] models correlated, time-dependent changes. The proposed contract makes the exit policy constrain which examples a private incumbent actually supplies; a robust planner over identical offered examples is the direct reduction to beat.
- **Cheapest first test:** Enumerate a two-stage rule/exception curriculum with interruption at either stage, then use small SGD updates for the transitions. Compare an endpoint cap, a raw per-prefix cap that ignores lesson arrival, and coupled robust planning; reject if the same-powers buyer can obtain the same exits without changing supply.
- **Old-task retention:** Include an old exception whose incumbent-only correction would have arrived after interruption. Score it at the prefix and after the public exit.

### LE3-03 · Test exit under correlated shortages, not fictitious independent failures — I
- **Mechanism / learner effect:** Couple entrant availability to shared sources. Reward a teaching path that leaves two distinct learnable ways to finish using different sources, not many interchangeable sellers relying on one source. This can favor a representation that admits different gradient directions.
- **Nearest prior / gap:** [TC-RMDP] already treats correlated shifts. This is an application and supply audit: the question is whether supplying the shared availability information changes the learned checkpoint beyond robust procurement on the same menu.
- **Cheapest first test:** Use four sellers, two shared data sources and two ordinary feature views; keep each seller's marginal attendance fixed while moving from independent to paired outages. Compare random entrant, marginal caps and a correlation-aware robust buyer.
- **Old-task retention:** Withdraw the shared source and score old cases dominated by it, especially the rare cases that remaining sellers cannot label.

### LE3-04 · Preserve public gradients, not just a public prediction interface — P
- **Mechanism / learner effect:** Require a live representation to admit a safe useful change from actual public examples, not just from a private basis or from an arbitrary vector the buyer cannot realize. During incumbent selection, prefer equal-accuracy lessons that keep an ordinary entrant gradient effective after restricting damage to old tasks.
- **Nearest prior / gap:** [Stationary] preserves compatibility for feature comparisons; [Adam-NSCL] projects updates into old-feature null spaces. The proposed object is a **realizable public update** surviving the retention restriction, not matching embeddings or counting free dimensions. Test against their stack and the parent exact distance gate.
- **Cheapest first test:** Build a two-layer learner with matched predictions in two gauges, one of which suppresses an ordinary example's safe finite step. Compare compatible training, projected SGD, and translation; evaluate actual two-step trajectories, not predicted first-order drift. This uses [PR #104] as a control, not a new gauge principle.
- **Old-task retention:** Check rare old examples that the projection did not see, including one sharing the public input direction with the new task.

### LE3-05 · Withdraw the teacher's optimizer privileges one at a time — I
- **Mechanism / learner effect:** Audit a declared sequence of removals (private preconditioner, private feature labels, then privileged examples) and disallow an installment that only looks open while one privilege remains. Counterfactually remove each privilege at the same checkpoint to tell whether the learner has open training dynamics or only a compatible input format.
- **Nearest prior / gap:** [BT²] transforms representations for backward compatibility; [Task arithmetic] changes behavior through weight directions. This is a handoff audit, not a new transform or parameter edit. It must distinguish state dependence from a privilege any checkpoint would need.
- **Cheapest first test:** Cross two curriculum checkpoints with public versus private optimizer and example menus in a factorized linear learner. Match step counts and charge optimizer state; if removing a privilege hurts equally on both checkpoints, classify it as teacher advantage.
- **Old-task retention:** Score old tasks after every removal and subsequent ordinary update; include a narrow slice where a private preconditioner had been protecting an old margin.

### LE3-06 · Buy an example that works with two frozen, incompatible entrant policies — P
- **Mechanism / learner effect:** Require one incumbent example to make progress possible under both independently committed entrant update policies. The proposed purchase is a shared prerequisite in the learner, not a common data format. It should yield a checkpoint each can extend without access to the other's state or custom lesson.
- **Nearest prior / gap:** [Multiple learners] teaches several students from one teacher; [UNIC] distills several teachers into one encoder. Neither comparator by itself asks one incumbent write to enable multiple *future trainers on the same learner*. Compare equal-example augmentation and independent minimum-distance gates.
- **Cheapest first test:** In a low-rank learner, register two sample-selection policies that disagree on ordering of an ordinary view. Search for a short common prerequisite at the same immediate score as two specialist prefixes; reject if balanced replay or the stack ties on both held-out continuations.
- **Old-task retention:** Recheck old view-specific tasks after each entrant's complete independent continuation; a model passing by ignoring one view fails.

### LE3-07 · Replace the supplier twice without a shared handoff channel — P
- **Mechanism / learner effect:** Test A→B→C using independently drawn entrants and the same learner. B must learn an actual new part *and* leave a C-continuable state. A single easy swap is insufficient if B has to install its own convention to succeed.
- **Nearest prior / gap:** [UNIC] combines complementary teachers, and [LwF] preserves old capabilities during an update. Neither alone makes a substitute's live update preserve the next supplier's teaching ability; compare mixed-teacher training plus LwF and reapplying LE2-24 at each handoff.
- **Cheapest first test:** Use three sequential grammar extensions and two incompatible encodings. Compare protocols after matching B accuracy, C's ordinary menu and all setup. Require a mechanism beyond rolling LE2-24, such as an independently precommitted pair of ordinary extensions that reveals an interaction invisible to the same-budget rolling gate.
- **Old-task retention:** Score original productions and the newly learned B productions after C, with no teacher-specific dictionary at inference.

### LE3-08 · Separate entrant blindness from an unreachable checkpoint — P
- **Mechanism / learner effect:** Give entrants a budget for choosing an ordinary diagnostic example, and propose paying for an incumbent lesson that makes the diagnostic's *observed response* identify a safe next write. This need not shorten the omniscient path; it can shorten the path attainable by a blind replacement. A private header from the incumbent does not count.
- **Nearest prior / gap:** [Sequential MT] finds fast training inputs; [Side observations] learns from information revealed by one's own actions. The object is a purchased change in what a real entrant can infer about **which safe teaching action to take** from its normal interaction. Compare belief-state planning on the same transcript.
- **Cheapest first test:** Pair function-identical factorized checkpoints with opposing safe next steps and a candidate ordinary one-example diagnostic. Compare full-state oracle, adaptive public diagnostic and static translator; if equal-budget adaptive planning already solves both without changing the incumbent lesson, drop the purchase.
- **Old-task retention:** Score the old tasks after the diagnostic itself and the chosen update; neither a destructive read nor a probe-only safe suffix qualifies.

### LE3-09 · Count open routes by what the learner can lose simultaneously — P
- **Mechanism / learner effect:** At a checkpoint, identify minimal bundles of ordinary lesson types whose joint absence destroys *all* safe continuations. Admit incumbent teaching that breaks a single common bottleneck, even where the number and length of visible paths do not change. The representation should become repairable using either of two genuinely distinct learned features.
- **Nearest prior / gap:** [TC-RMDP] covers correlated threats; exact robust reachability already subsumes any cut it computes from the same information. The proposed reusable object is a cut restriction at teaching time eliciting a different curriculum, not a new reachability theorem.
- **Cheapest first test:** In a small finite grammar with two routes to learn a new production, ablate ordinary label types jointly and individually after two matched curricula. Compare two-best distances, source-aware robust planning and equal-budget protected sourcing; drop if the explicit cuts never change offer or training beyond that stack.
- **Old-task retention:** Under each critical removal, score rare old productions after taking the surviving route; exclude routes that finish by dropping them.

## B · LE2-01: pay for a real reduction in sample cost

### LE3-10 · Pay for surplus over an incumbent-quality control, not for beating the incumbent — P
- **Mechanism / learner effect:** Estimate the same entrant's paired sample saving against a public-curriculum branch at equal starting progress, with an incumbent precommitment to either portable or specialized teaching. Pay only for savings that follow the checkpoint rather than the entrant identity. An intrinsically superior incumbent can still sell specialization without owning the learner.
- **Nearest prior / gap:** [IMT] minimizes a teacher's own sample count; [Contracts] rewards hidden actions using outcomes. Here the candidate outcome is cross-checkpoint entrant sample savings net of supplier quality, not standalone success against a deadline.
- **Cheapest first test:** Cross public/specialized checkpoints with novice/expert entrants in a rule-and-exception learner. Compare unpaired LE2-01, a fixed quality adjustment, and central adaptive procurement. Require a changed seller choice and lower held-out entrant cost after matching immediate accuracy.
- **Old-task retention:** Demand the same old-exception floor on both branches and score after switching both; exclude savings attributable to less old behavior being retained.

### LE3-11 · Pay a general lesson for reducing the tail of retries — I
- **Mechanism / learner effect:** Replace mean-cost payout with a predeclared bound on the probability of exhausting a limited public label budget. It can favor learning a rule that avoids entrant-specific failure modes even when median sample cost is unchanged.
- **Nearest prior / gap:** [TC-RMDP] handles adverse shift; [Optimal contracts] learns outcome-dependent payment with hidden actions. Tail risk alone is not a primitive. Look for a change in representation and tail failures that survives a risk-aware buyer with the same powers.
- **Cheapest first test:** Two seller types can supply either one general example or a cheaper batch of narrow cases. Enumerate entrant arrivals with identical medians but different miss probabilities, then fit a quasiregular tiny learner. Compare a hard worst-case covenant, mean payment and an equivalent tail constraint without the payment.
- **Old-task retention:** Count runs that miss an old-task floor as unsuccessful even if the new deadline is met; report the worst old slice among retries.

### LE3-12 · Pay on the second use of the same ordinary data budget — P
- **Mechanism / learner effect:** One entrant trains on an ordinary first extension, then a different entrant gets the same capped budget on a held-out extension. Pay only for a sample-cost gain on the second job without undoing the first. A teacher that hard-codes the public audit target cannot win by making only that target easy.
- **Nearest prior / gap:** [Meta Pseudo Labels] updates a teacher using downstream student performance; [Sherpa] rewards student learning. This proposal pays on ability to continue **after** realistic intermediate training, not on that training's validation score. Compare meta-teaching on two-turn outcomes at identical information.
- **Cheapest first test:** Draw two disjoint rule extensions from a preregistered generator, each with one rare exception. Compare one-turn payout, held-out one-turn audits, and a central two-turn meta-curriculum. Apply the second update to the actual checkpoint left by the first.
- **Old-task retention:** Test original tasks plus the first extension's learned exceptions after the second teacher leaves.

### LE3-13 · Make audits cross lesson procedure and test generator — I
- **Mechanism / learner effect:** Freeze seller delivery before drawing both the ordinary teaching procedure and the task generator used to audit it. Pay only if both held-out axes show a gain. This should select for a reusable representation rather than memorized evaluator inputs or a representation tuned to the auditor's update order.
- **Nearest prior / gap:** [Adaptive holdouts] analyzes reuse under adaptive analysis; [AntiLeakBench] constructs fresh benchmarks. Freshness is not novel; this audit holds out an independent **training procedure** as well as test cases. A full factorial holdout without a payment is the strongest simple control.
- **Cheapest first test:** In a small rule learner, hide one of two ordinary lesson-orders and one of two grammar generators. Train with repeat then one-time audits; compare a matched fresh test-only split and the full factorial control. Reject if outcomes separate only on a reused validation set.
- **Old-task retention:** Keep hidden examples for old tasks using each grammar and include an old shortcut that happens to solve the repeated audit alone.

### LE3-14 · Pay for removing dependence on a hint that was once needed — P
- **Mechanism / learner effect:** Pair a hinted route with a later entrant-only route on the same task family. A sellable lesson must leave extra sample savings when the hint is permanently unavailable, not just good performance with it. Separate teaching a durable rule from renting out a missing observation.
- **Nearest prior / gap:** [SDFT] uses in-context demonstrations as privileged teacher input; [Denser ≠ Better] tests continual self-distillation limits. This is not changing teacher refresh or testing depletion. The proposed trigger is paired savings for a separate ordinary entrant *after withdrawing the context*, against an equally informed unhinted alternative.
- **Cheapest first test:** Use synthetic finite grammars where a hint may reveal an answer or a reusable rule; hold hint length and initial success fixed, include answer-matched public instruction and ordinary-example replay. Compare delivery payout and LE2-01 applied to just one undisclosed family.
- **Old-task retention:** With all added context withdrawn, score old parses including contexts where the hinted rule would be wrong.

### LE3-15 · Make a release payment conditional on leaving old exceptions learnable — P
- **Mechanism / learner effect:** Beyond retention today, require the ordinary entrant to learn one genuinely new exception without displacing known old exceptions. This selects a rule with editable scope over a globally rigid rule that looks portable at first.
- **Nearest prior / gap:** [Quasiregular] shows rule/exception overregularization and recovery; [GEM] protects old tasks while transferring. The paid product would be retained **exception accommodation** by another trainer, not simply delayed score checking or the parent's exception escrow.
- **Cheapest first test:** In a quasiregular classifier, hold the shared rule fixed and draw a previously hidden exception from either a familiar or a new feature cluster. Compare delivery buyout with exception replay, GEM plus LE2-01, and exact old-floor validation. Reject if the same stack suffices.
- **Old-task retention:** Check old exceptions both inside and outside the new exception cluster during subsequent public updates.

### LE3-16 · Let the entrant spend its audit examples doing paid production — P
- **Mechanism / learner effect:** Choose between two already-due public lesson jobs whose immediate value is comparable but whose observed learning increments reveal whether future examples will work. Make measured successor cost determine payout and keep the productive update. This changes the live learner while avoiding a separate pure audit only if the same live step both teaches and discriminates.
- **Nearest prior / gap:** [Side observations] gets information while acting; [Data values] plans sequential selection; [Universal openers] already reuses a productive step as a diagnostic. Compare productive diagnosis stacked with LE2-01 on the same observations. The candidate is procuring that ordinary step from an entrant so the incumbent has reason to leave an auditable, teachable checkpoint, not a new productive-probe technique.
- **Cheapest first test:** In a factorized classifier, find an existing subgoal with two ordinary examples that both achieve it, but only one reveals whether the next low-cost suffix is safe. Match labels and wall-clock with a shadow contrast; reject if information-only selection or a diagnostic that costs nothing ties.
- **Old-task retention:** Measure the exposed production step and the resulting follow-up; the diagnostic cannot buy evidence by damaging an old exception.

### LE3-17 · Buy a cheaper switch without paying to create the dependency — P
- **Mechanism / learner effect:** Debit an incumbent's eventual release payment for excess ordinary continuation cost it creates at exposed prefixes, relative to a reference fixed independently of its choices. Even a later rescue with real endpoint value cannot wipe the debit. This targets an early private-feature curriculum followed by an expensive “rescue.”
- **Nearest prior / gap:** [Optimal contracts] treats costly hidden actions, and [Endogenous information] permits additional buyer experiments. Neither comparator alone fixes a benchmark for a learner specific cost the seller can first inflate. A fixed-price delivery buyout plus no-covenant/LE2-24 arms is essential.
- **Cheapest first test:** Let a seller choose open/closed first lessons and later supply a common rescue lesson or do nothing. Compare endpoint-only open-reference savings (LE3-10), a hard prefix veto stacked with those savings, and a cumulative debit at the same available spend and entrant audit work. Require fewer closed exposed states than endpoint-only pay without the lost open continuations of the hard veto.
- **Old-task retention:** Score old tasks before any rescue; a harmful committed prefix is not excused by restoring its accuracy later.

### LE3-18 · Elicit which ordinary lesson family the incumbent cannot make portable — P
- **Mechanism / learner effect:** Let a seller commit to one excluded family and offer a lower payout for covering fewer families. Randomize the test over the covered families and verify the excluded family separately without letting it disappear from reporting. A truthful narrower offer can preserve a cheaper useful open representation instead of either withdrawing supply or claiming universality.
- **Nearest prior / gap:** [Contracts] elicits costly information through outcome-dependent transfers; [Optimal contracts] acts over hidden choices. The novel candidate is disclosure of **where continued teaching is unavailable from the offered learner**, validated via outcomes, not a seller's quality tier.
- **Cheapest first test:** Two private seller types, two extension families and a small shared-feature learner; solve best responses, then compare one universal outcome threshold and an equally informed buyer eliciting a fixed curriculum. Require a nonempty range of costs where coverage disclosures change the actual learned state and predict held-out sample cost. Do not label a partially open state fully open.
- **Old-task retention:** Demand the same old floors regardless of declared exclusion, including old examples from the family the seller excludes for new training.

## C · Use the covenant and the payout together, including when neither can work

### LE3-19 · Require the on-path safety check and off-path payout test to disagree where they should — I
- **Mechanism / learner effect:** Separately report safe exit at each exposed prefix and genuine sample savings after the proposed buyout. A fast endpoint can mask one closed prefix; an open path can buy nothing that accelerates actual continuation. Use both axes to deny those misleading wins.
- **Nearest prior / gap:** [Sequential MT] and [Contracts] already support path optimization and outcome pay; the parent controls already supply both gates. This is a required interaction audit, not a new primitive by combining scores.
- **Cheapest first test:** Cross safe/unsafe prefix with high/low end saving using matched full-game opportunities. Compare covenant only, payout only, and their straightforward conjunction. If joint cards cannot outperform the conjunction at the same resources, keep only the audit.
- **Old-task retention:** Make one closed prefix specifically closed by the old floor and verify that endpoint recovery cannot erase that failure.

### LE3-20 · Turn the missed takeover into an ordinary repair that earns a second payout test — P
- **Mechanism / learner effect:** If a contracted independent takeover fails, give a different entrant the precommitted right to attempt one ordinary corrective lesson, without letting the incumbent see the failed test instances. Pay only if the corrective write leaves the next entrant more sample-efficient within the originally counted budget. This can induce an incumbent to leave a repairable near miss rather than an irreversible one.
- **Nearest prior / gap:** [Residual integration] adds a target-side residual to prevent negative transfer; [Sequential MT] optimizes a sequence. Compare ordinary residual repair followed by the parent gates. The joint claim is an interaction: a *credible post-failure action* changes pre-failure teaching choices, not just what an extra label learns.
- **Cheapest first test:** Low-rank learner with two equally accurate first curricula, one losing a public feature direction irrevocably within budget. Enumerate seller choices with and without the reserve, and compare the full baseline stack including unconditional reserve and identical example rights.
- **Old-task retention:** Score old cases at the failed takeover, after corrective training and during the final replacement; failure cannot reset the old reference.

### LE3-21 · Budget the replacement path for doing two jobs without duplicating an example — P
- **Mechanism / learner effect:** A safe exit must cover both a scheduled ordinary update and a newly revealed task. The covenant accepts a prefix only if the same limited entrant stream can perform both; the buyout pays for reducing that joint sample cost. Two independently short paths do not count as a jointly feasible one.
- **Nearest prior / gap:** [Sequential MT] optimizes shortest curricula, and [GEM] constrains interference. The candidate is **jointly productive replacement distance** against simultaneous obligations, not the sum or max of single-job distances. An augmented-state planner with joint target and identical offerings is a strong reduction.
- **Cheapest first test:** Enumerate two private incumbent prefixes and ordinary lesson orders in a shared-feature regressor. Hold single-job distances fixed, vary whether the same first ordinary example advances both; test if the joint gate plus payout elicits a different incumbent lesson beyond the parent stack.
- **Old-task retention:** The scheduled job does not replace the frozen old tasks. Score those throughout and recheck the first job once the second is learned.

### LE3-22 · Require an actual detour to change what the next real buyer needs — P
- **Mechanism / learner effect:** Where the incumbent predicts that a single delivered example lets the entrant choose between two later extensions, commit to one ordinary intermediate use whose occurrence is decided outside the seller. Pay only if the triggered continuation stays short and the other branch does not become permanently inaccessible. This tests learning to preserve options through use, not buying a catalog of options.
- **Nearest prior / gap:** [Data values] models sequential selection, and [TC-RMDP] supports history-dependent planning under correlated conditions. Compare their planner equivalent and both parent gates. The hypothesis is a realized **branch intervention** distinguishes learning an extension-ready feature from knowing which future branch an evaluator will take.
- **Cheapest first test:** Use a finite-state learner with two future grammar extensions and one already-due grammar update. Cross which update is externally due with two incumbent lesson variants, using separate counterfactual runs and matched cost. Look for a buyout that changes lesson selection when branch use, not only its score, is audited.
- **Old-task retention:** Test ordinary old grammar and its rare dialect on both branch histories, including after learning the initially unused extension.

### LE3-23 · Identify the smallest public separator, then test if the seller can make it unnecessary — P
- **Mechanism / learner effect:** If two indistinguishable checkpoints require incompatible first updates to stay safe, no ordinary entrant can promise both without further evidence. Instead of buying that evidence at each switch, pay the incumbent a share of the cost avoided against a registered public diagnosis-and-teach policy, if an upstream lesson makes the same safe continuation work across the indistinguishable states. This can reduce the buyer's observation requirement rather than its oracle path length.
- **Nearest prior / gap:** [Interventional CRL] uses interventions to identify latent structure; [Sequential MT] chooses training actions; [Universal openers] already uses a learner update to make the same later write safe across hidden histories. The new claim must be about procurement: private incumbents offer a common continuation because the price is tied to savings over independently buying repeated diagnosis, not because the common write itself is new. Compare a buyer that directly procures a universal opener, as well as optimal belief-state teaching and LE3-08 under the same budget.
- **Cheapest first test:** Build two latent starting states with identical public observations up to the first required action and disjoint safe action sets; add a discoverable diagnostic as the control. Try a real upstream teaching example in a small shared-feature learner, and check whether it makes the safe sets overlap without leaking the hidden state or changing the task. Include a negative where no allowed upstream example makes them overlap.
- **Old-task retention:** Exhaustively check old floors in *both* latent states after the new common action; an averaged pass in a mixture does not count.

### LE3-24 · Locate the point where a covenant prevents learning rather than preventing lock-in — I
- **Mechanism / learner effect:** Trace the frontier between legitimate useful specialization and excess entrant cost, with and without an independent supplier able to provide a missing feature. If ordinary examples contain no information distinguishing two target rules, report nonidentifiability rather than punishing the incumbent as a monopolist.
- **Nearest prior / gap:** [NIMT] teaches a target function under a specified teaching process; [IRM] targets invariant predictors across environments. This is a falsifying control: availability and identifiability limits are not new learning primitives.
- **Cheapest first test:** Two equiprobable target functions agree on every eligible public training example but disagree on the evaluation slice; even an adaptive blind policy has at most 50% expected accuracy on the disagreeing binary slice. Add one independent separating example to both arms and see if the measured *excess* over the open checkpoint now separates supported from unsupported lock-in.
- **Old-task retention:** Old labels stay fixed across hidden worlds. Report which old floors make the attainable portion of the frontier narrower; never lower them to make the contract feasible.

### LE3-25 · Replace a persistent incumbent convention with an ordinary feature that earns its storage — P
- **Mechanism / learner effect:** Allow a small feature left by the incumbent only if public updates independently use it to retire a private convention while continuing a scheduled task. Require the result to work after removing private side channels, and count feature bytes and compute. The hypothesized purchase is a self-displacing dependence, not a permanent adaptor or a saved checkpoint.
- **Nearest prior / gap:** [BT²] and [Backward-compatible alignment] learn transforms across feature spaces; [Residual integration] adds a trainable target path. Compare their stack plus explicit translation and equal-budget open replay. The test is whether downstream productive updates make the original convention unnecessary rather than calling the translator forever.
- **Cheapest first test:** Small two-view MLP with a privately rotated view. Match prediction and bytes at handoff, then learn two public subskills and remove the private view. If translation retained at equal cost gives the same uncued continuation and ordinary future learning, reject the mechanism.
- **Old-task retention:** Check old convention-heavy cases after removal via the normal public interface, with no cached old answers or route back to the retired feature.

### LE3-26 · Ask whether the covenant and buyout can both be credible at the same price — I
- **Mechanism / learner effect:** Enumerate seller participation, delivery choices and the learner's actual state trajectory together. A hard prefix cap can eliminate the only type willing to sell a genuinely portable general lesson at the proposed buyout. Conversely, paying for cheap completion can induce an unsafe prefix when recovery is subsidized. Report which learner obtains the rule or falls back to exceptions, not just contract feasibility.
- **Nearest prior / gap:** [Endogenous information] models buyers who can later acquire more information; [Optimal contracts] learns outcome-dependent offers. This is a planner-equivalence and participation audit for the joint proposal, not a new contracting theorem.
- **Cheapest first test:** Two private costs, two continuation rent levels and a two-stage rule-plus-exception learner. Enumerate feasible transfers for parent gates separately, their conjunction, and the best equally informed coordinating buyer; verify outcomes with the same tiny classifier. Flag ranges where neither gate can be relaxed without losing actual entrant performance or violating old floors.
- **Old-task retention:** Include the buyer left with no supplier and the buyer left with only the exception installments. Measure ordinary old tasks during delay and after any independent lessons.

## Ranked deeper questions

1. **Can a buyer pay a private incumbent to remove the need to diagnose which learner state an entrant inherited?** (LE3-04, 08, 23.) Find the smallest nontrivial learner where two checkpoints look identical to an entrant but have disjoint safe next updates. Can an outcome payment elicit a prerequisite that creates a common safe continuation, using no privileged information at handoff, at lower total cost than diagnosis plus tailored teaching or a delivery-based opener? Report the impossible case too.
2. **Can a productive handoff expose dependence at the same cost as continuing to teach?** (LE3-01, 07, 16.) Look for a live ordinary example that genuinely learns a due subskill and reveals whether the next independent seller can extend it. It must beat the same-work shadow-audit plus scheduling stack, not just an unaudited handoff.
3. **Which part of measured lock-in comes from the learner rather than what the sellers know or can deliver?** (LE3-03, 05, 10, 24.) Cross checkpoint, rights, observable information and simultaneous availability. Require no accusation when the public problem is nonidentifiable or the incumbent has a genuine example advantage on both matched states.
4. **When do the covenant and payout together change what gets taught, rather than duplicating a robust buyer?** (LE3-17, 19–21, 26.) Seek a parameter range where the credible ordinary repair changes a strategic seller's delivered lesson and lowers held-out joint continuation cost while retaining old tasks. Otherwise report the reduction to the same-powers buyer and keep only the discriminating tests.

[PR #326]: https://github.com/manojbajaj95/cl/pull/326
[PR #104]: https://github.com/manojbajaj95/cl/pull/104
[Universal openers]: https://github.com/manojbajaj95/cl/pull/284
[review]: https://github.com/manojbajaj95/cl/pull/6
[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L444
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[IMT]: https://arxiv.org/abs/1705.10470
[Sequential MT]: https://arxiv.org/abs/1810.06175
[NIMT]: https://arxiv.org/abs/2306.03007
[Multiple learners]: https://arxiv.org/abs/2311.10318
[TC-RMDP]: https://arxiv.org/abs/2406.08395
[BT²]: https://arxiv.org/abs/2211.03989
[Stationary]: https://arxiv.org/abs/2606.12488
[Backward-compatible alignment]: https://arxiv.org/abs/2408.08793
[Adam-NSCL]: https://arxiv.org/abs/2103.07113
[GEM]: https://arxiv.org/abs/1706.08840
[LwF]: https://arxiv.org/abs/1606.09282
[Task arithmetic]: https://arxiv.org/abs/2212.04089
[Adaptive holdouts]: https://arxiv.org/abs/1506.02629
[AntiLeakBench]: https://arxiv.org/abs/2412.13670
[Optimal contracts]: https://arxiv.org/abs/2309.09801
[Contracts]: https://arxiv.org/abs/2103.03911
[Endogenous information]: https://arxiv.org/abs/2103.05788
[Quasiregular]: https://arxiv.org/abs/2609.26018
[Data values]: https://arxiv.org/abs/2502.04554
[Sherpa]: https://arxiv.org/abs/2610.08778
[UNIC]: https://arxiv.org/abs/2408.05088
[Side observations]: https://arxiv.org/abs/2604.24555
[Meta Pseudo Labels]: https://arxiv.org/abs/2003.10580
[SDFT]: https://arxiv.org/abs/2601.19897
[Denser ≠ Better]: https://arxiv.org/abs/2607.01763
[Residual integration]: https://arxiv.org/abs/2505.11771
[Interventional CRL]: https://arxiv.org/abs/2209.11924
[IRM]: https://arxiv.org/abs/1907.02893
