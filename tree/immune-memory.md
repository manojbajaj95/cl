# Immune memory: remembering how to respond, not just what to replay

**Status:** research ideas only; no experiments run. **Parents:** the [immunology/development flood (PR #75)](https://github.com/manojbajaj95/cl/pull/75) and [neuro-bio flood (PR #46)](https://github.com/manojbajaj95/cl/pull/46). This branch of the tree concerns recurrent, partially observed environments and bounded adaptation, not weight-edit equivalence, editing capacity or edit localization.

## Root-cause hypothesis

When an old situation returns in altered form, the quickest past response may be the wrong one. The learner needs to discover whether the old response still works, where it stops working, and whether it should keep serving other situations while it learns a successor. Ordinary replay can preserve examples or outputs; a routed expert can restore a response. Neither, by itself, keeps an explicit, reusable policy for **what to observe, how much temporary compute to spend, and what to preserve when a response returns but no longer fits**. This is a hypothesis about the value of that separation, not a claim that replay or routing cannot implement it.

Use adaptive immunity as a source of operations, not as a simulator. Clonal selection makes copies of responders that have useful evidence; affinity maturation changes which encounters they respond to; tolerance limits responses to normal activity; memory B and T cell populations motivate different forms of long-lived readiness; vaccination motivates paying for selected experience before it is needed. Here a *clone* is a temporary learner or policy copy, *affinity* is measured or predicted task utility under a stated evaluation (not necessarily input similarity), and *self* means currently supported normal behavior, not everything the learner has ever done. Use only computational tasks and synthetic environment shifts.

## Prior-art and repo screen

- **Classical AIS already has these ingredients.** Forrest et al.'s [negative selection](https://doi.org/10.1109/risp.1994.296580) screens detectors against self examples. De Castro and Von Zuben's [CLONALG](https://doi.org/10.1109/tevc.2002.1011539) selects, clones and mutates by affinity and retains memory. Their [aiNet](https://doi.org/10.4018/978-1-930708-25-9.ch012) adds network interactions and suppression. The [deterministic dendritic cell algorithm](https://arxiv.org/abs/1006.1512) combines safe/danger signals over windows to assign context to encountered items. Detector screening, affinity-weighted reproduction, suppression, and multi-signal gating are therefore baselines, not contributions.
- **AIS and continual learning already intersect.** A [continuous pattern-recognition AIS](https://seer.ufrgs.br/index.php/rita/article/view/RITA_VOL27_NR4_34) already combines negative selection with clonal novelty learning. [CLCMTVD](https://doi.org/10.3233/jifs-200044) updates memory cells on testing data for time-varying classification. Recent neighbors from HF Papers and web searches include [SAIS](https://arxiv.org/abs/2402.07244) (symbiosis-inspired optimization), [Structured Affinity](https://arxiv.org/abs/2608.20104) (replay-free visual class-incremental memory using structured binding profiles; downstream probes evaluate the learned representations) and [Model Immunization](https://arxiv.org/abs/2505.17870) (countering falsehoods). None of these checks establishes priority for the cards. In particular, structured affinity, adding a memory population, and pre-exposure itself are not novelty claims.
- **Local exclusions.** Read the [idea ledger (PR #6)](https://github.com/manojbajaj95/cl/pull/6) before proposing cards. Its killed memory inoculation, self-quizzing, save/restore, and frozen prompt-pool patterns do not become new when renamed. The [economy flood (PR #45)](https://github.com/manojbajaj95/cl/pull/45) E28 already expands, adapts and contracts old units on recall. [PR #36](https://github.com/manojbajaj95/cl/pull/36) already has corrupted-lesson vaccination, reusable repair directions and the Z4 immune graph; [PR #42](https://github.com/manojbajaj95/cl/pull/42) A4 already rejects memories by failure fingerprint. PR #75 has responder forks, cross-reactivity, breadth mosaics, tolerance and recognition-space inocula; PR #46 has self-state screening and inhibition graphs. The [developmental-growth node (PR #127)](https://github.com/manojbajaj95/cl/pull/127) owns growth, role differentiation and structural repair. The comparisons below identify the proposed differences rather than assuming those lines are unrelated.

## Shared CPU test contract

- Start with a small stream of solvable tasks, first visits and at least one changed return. Compare with no task ID at inference or oracle change boundaries. Give arms identical observations and feedback opportunities; where a card selects observations, give all arms the same legal query menu and price, not the treatment's answers. Use paired seeds and split task families, not just examples, for transfer claims.
- Log prequential return loss or regret, samples/steps to a prespecified new-task target, and per-task and worst-old scores on fixed, untouched probes before and after each wave. Evaluate at the same elapsed budget and at matched acquisition; if a method misses the target, report it. Score old tasks before any labeled reminder and separately after a fixed reminder budget where recovery is part of the claim. Keep unrelated old tasks and old/new near misses separate; for legitimately revised behavior, score the old contract only where it still applies. Reject an apparent win if it comes from withholding service or failing to acquire the new task. A first screen should require improvement over the strongest named control without a material worst-old drop (e.g. predeclare a 2 pp tolerance on classification).
- Match peak and persistent bytes, counting candidates, optimizer state, learned generators, probe records and metadata; charge transient compute, active evaluations, environment calls and any extra context tokens. For neural arms include the better of equal-byte labeled replay and [DER++](https://arxiv.org/abs/2004.07211) at the same update budget, plus each card's stronger mechanism-specific control where applicable. For discrete agents use an equal-byte transition/retrieval store instead of an artificial SGD comparison. For adaptive allocators give a central scheduler the same observations and decisions, and for different training paths compare norm-matched updates and margin-stratified old tasks. Where the claim depends on history after common practice, confirm in a nonlinear host and measure relaxation under a shared suffix; a toy demonstration is not evidence for durable hidden history.

## Research ideas (22 cards)

### A. Clonal selection: spend temporary capacity to learn what to do

#### 1. Clone auditions that choose the next observation

- **Mechanism:** Clone competing old responders in scratch space. Each proposes an experiment and predicts the result under its current solution; a disagreement-aware allocator buys the experiment with highest expected ability to distinguish which response remains useful. Keep a small policy for selecting such experiments and discard unsuccessful clones.
- **Novelty bet — primitive candidate:** A clone's product can be a decision about *what to observe*, before any winner takes over. CLONALG scores on presented data; E28 spends more updates after recall, and ID19 generates a query from conflicting settlement conditions rather than from predictions of adapted candidates. The risk is that ordinary active learning ties.
- **Cheapest test:** Recurring symbolic navigation maps with two plausible transition rules; only one of four cheap scout moves discriminates them. Compare return regret against both an equal-byte recurrent expert bank with active model disagreement and a same-information central scheduler choosing over the same proposals.
- **Old-task retention:** After the changed map is learned, score untouched old maps and still-valid branches of the source map on the first visit, before scouting or updates, and score them again after the next allocation burst.

#### 2. Select on the work left after a clone contracts

- **Mechanism:** Let all clones explore, but select one by the validation utility of the *fixed-size teaching packet* it can leave behind, not by its own accuracy. The packet may contain an example, target and disagreement weight; evaluate it by briefly training a scratch copy of the eventual survivor.
- **Novelty bet — primitive candidate:** Fitness passes through a bounded recipient. CLONALG and E28 retain fit clones; PR #75 ID57 transfers a construction seed, not a packet whose value is ranked by a downstream learner on new evidence. This could reduce to dataset distillation with unnecessarily expensive teachers.
- **Cheapest test:** A width-16 MLP on three related two-dimensional functions. Match the candidate pool and norm of recipient updates. Compare against best-clone distillation, and against direct gradient-matched buffer selection with the same total forward/backward budget.
- **Old-task retention:** Following contraction, test both old functions on untouched draws, plus their low-margin boundary slices; compare at matched fit to the third function.

#### 3. Allocate offspring by reversible versus irreversible trial

- **Mechanism:** Offer two kinds of auditions in a simulator: shadow predictions on existing states, and real practice actions that change which states can be reached. Learn a price for the opportunity cost of each irreversible audition from later missed practice, and allocate clones with that price rather than a fixed trial count.
- **Novelty bet — improvement:** Affinity determines reproduction in CLONALG, and E28 budgets steps; here the binding constraint is the learner's future practice distribution, not evaluator compute. Test against a dual-control planner, not a passive clone allocator.
- **Cheapest test:** Toy workshop agent with scarce reset tickets; actions change which training stations are available next. Compare to an equal-information belief-state planner and an expert pool with uniform audition quotas at equal interactions and resets.
- **Old-task retention:** After the new station is learned, test the original stations on fresh read-only episodes, counting timeouts as failures and separating old states that were expensive to revisit.

#### 4. Recall tournaments with non-clonal challengers

- **Mechanism:** After every return, allocate a fixed fraction of practice to a learner initialized independently of the incumbent repertoire. Learn when to stop auditions by measuring whether that challenger improves with *independent* clues while the incumbent only improves with familiar clues.
- **Novelty bet — improvement:** Random immigrants are not new to AIS, and E28 already forks incumbents. The narrower claim is a stopping rule based on differential generalization to independent clues, not offspring diversity or confidence.
- **Cheapest test:** In a small contextual bandit, switch whether a recurring cue is still predictive while keeping initial incumbent and fresh-policy scores matched. Compare against a central sequential best-arm allocator on the same feedback, plus UCB with random restarts.
- **Old-task retention:** Reintroduce the original cue-value relationship in held-out old contexts after acquisition of the new one; score first-action reward and worst-old regret without updating.

### B. Affinity maturation: improve recognition without making recognition the goal

#### 5. Mature the feature that predicts *benefit of adapting*

- **Mechanism:** Train a recognition head on paired one-step trials: the increase in future utility from adapting a responder versus leaving it alone. Equal starting loss need not mean equal benefit from an update. Use the head to decide whose *optimizer* to wake, not whose answer to trust.
- **Novelty bet — improvement:** Structured affinity and ID10 learn better recognition; ID11 measures immediate gains from activating old responders. This card conditions on an actual training intervention with the same initial output. Ledger readiness predictors failed in the global candidate-selection setting, so learning-progress and projected readiness are required controls, not straw men.
- **Cheapest test:** A two-layer MLP with three specialists on rotating boundaries. Require measurable, replicated spread in realized adaptation benefit before testing prediction. Compare to held-out first-step gain, projected readiness and loss-based routing with the same trials and norm-matched steps.
- **Old-task retention:** Following a new boundary, test old rotations and the still-valid part of the source boundary at equal new fit; repeat under a shared practice suffix and report relaxation.

#### 6. Mature against the probability of confusing two repairs

- **Mechanism:** Train an affinity head to abstain specifically on input regions where two plausible responders disagree and applying the wrong response has a high measured cost. Region scores come from paired full rollout returns, not confidence alone. Keep the repair rules fixed during maturation.
- **Novelty bet — improvement:** ID10 also mutates recognition while holding payloads fixed; this version weights pairwise confusion by downstream cost, unlike prototype proximity or global hard-negative mining. A cost-sensitive router may well make the immune framing redundant.
- **Cheapest test:** A two-step inventory simulator where ambiguous orders vary independently in visual similarity and cost of a wrong response. Compare with a calibrated cost-sensitive selective classifier trained on the same counterfactual return table, at equal query and abstention budgets.
- **Old-task retention:** After learning a new order type, record old true-response rates and old costs per type, including safe ambiguous orders; charge abstentions and report old worst-case cost at matched coverage.

#### 7. Maturation over response delays, not detection delays

- **Mechanism:** For a recognized situation, maintain affinity scores indexed by when an old response takes effect; update them against delayed outcomes so that the same responder can be preferred for long windows and disfavored for short ones even at identical early success.
- **Novelty bet — improvement:** DCA windows assign context to events, and ID07 addresses a write by relative event timing. This learns the time-to-benefit distribution *of executing an already recognized response*. The real comparator is action-conditioned temporal credit, not fixed similarity.
- **Cheapest test:** Semi-Markov queue simulator with interventions having opposed immediate and delayed costs and censored feedback. Compare against an equal-state survival or distributional value head trained from identical rollouts, plus a windowed DCA-style scorer.
- **Old-task retention:** After introducing another response lag regime, check total old return at both horizons and rates of unnecessary interventions on legacy queues, including long-horizon cases that rarely produce quick rewards.

#### 8. Conserved coverage during maturation

- **Mechanism:** Represent each responder's covered transformations as a set of measured obligations. A maturation step proposes transferring an obligation to another candidate, which must demonstrate competence on that transformation before the first responder can drop coverage. Optimize the resulting assignment jointly with current gains.
- **Novelty bet — primitive candidate:** The operation is a verified reassignment of responsibility during learning, not aiNet similarity suppression or ID15's choice of a complementary committee at inference. It is not a market: a centralized assignment algorithm with the same evidence is the baseline.
- **Cheapest test:** Small transducers with overlapping rename/reorder skills. Compare against periodic global set cover with the same measurement budget and equal-size prioritized replay followed by pruning. Hold out combinations on which the cover table was never validated.
- **Old-task retention:** On each old transformation and unseen combination, evaluate the actual routed answer before and after reallocation and after a new skill, not just whether the coverage table still has an owner.

### C. Self-tolerance: learn when intervention is worse than leaving behavior alone

#### 9. Protect invariants of a set of legitimate answers

- **Mechanism:** Learn from independently confirmed successful old trajectories which observable relations are common to several legitimate solutions. A tolerance check admits variation inside those relations, including behavior unlike the incumbent, but audits sequential changes to the relations themselves.
- **Novelty bet — primitive candidate:** The protected object is an outcome-defined equivalence *among acceptable trajectories*. Negative selection and NB34 screen against known self examples; ID18 transfers similarity/dissimilarity constraints between learners rather than choosing which invariants to protect across several valid old paths. No credit if an equal-cost invariant learner ties.
- **Cheapest test:** Symbolic sorting workflow with multiple valid operation orders. Introduce a new throughput objective and a nuisance that makes formerly common paths rare. Compare against relational invariant mining with the same verifier and labeled stratified canaries with the same check budget.
- **Old-task retention:** After throughput training, use hidden validity labels for both familiar and unseen old paths. Score valid paths still accepted, invalid paths still rejected, and ordinary old-task completion rather than action agreement with the incumbent.

#### 10. Tolerance paid back in measured lost service

- **Mechanism:** Shadow-test a sample of rejected interventions asynchronously. Log the estimated utility denied by protection as a per-contract cost, and periodically renew or narrow the protection based on that cost and verified old service. A rejection is not taken as evidence that the current behavior was right.
- **Novelty bet — improvement:** Negative selection removes detectors and PR #75 ID19/ID22 store settlement evidence; this closes an explicit selective-feedback loop over the utility of interventions that were *never served*. The control must include rejection exploration rather than just treat rejections as unknown.
- **Cheapest test:** Bandit customer-routing simulator with a benign new category that initially resembles protected old traffic. Compare to budget-matched rejection sampling plus online constrained bandit optimization, giving both arms identical shadow-evaluation options.
- **Old-task retention:** After renewal, check legacy success, old false acceptance and worst-group old regret; match both new-category performance and the number of real service interruptions.

#### 11. Tolerance across a chain, not at each write

- **Mechanism:** Reserve a bounded harm allowance for a sequence of individually admissible interventions. Attribute measured drift in an old objective to the sequence and trigger its re-evaluation when state-dependent drift accumulates, even if no individual intervention predicts a large change.
- **Novelty bet — improvement:** Negative selection screens candidates and NB37 routes contradiction alarms; this protects a *trajectory* of otherwise permissible changes. Unlike ledger MX4's override-budget margin model, the outcome is cumulative service on held-out states, not a logit proxy.
- **Cheapest test:** Nonlinear planning toy where several low-impact policy changes can accumulate into a bad route. Compare with rolling stratified canaries and a budget-matched cumulative constraint monitor replaying exactly the same checkpoints. Include a same-net-change reordered stream and report relaxation after common practice.
- **Old-task retention:** Measure the minimum old completion rate during the chain and after acquisition, not only final accuracy. Include unrelated trajectories and old routes near the service threshold.

#### 12. Learn which tolerance checks can be inherited after a sensor swap

- **Mechanism:** Couple a learned monitor to a small calibration procedure; when a new sensor view arrives, adapt the *test* on paired calibration readings and verify that its accept/reject decisions still match real old service outcomes. Expire individual checks whose calibration uncertainty cannot be resolved.
- **Novelty bet — primitive candidate:** Transfer a callable calibration procedure for a check rather than its past labels or a universal invariance claim. ID18 transfers tolerated distinctions and ID62 transfers admissible moves; this asks whether a measured check remains interpretable after its observation channel changes.
- **Cheapest test:** A grid agent switches from one noisy position sensor to another, with limited paired views. Compare to a common observation translator shared by all checks plus refreshed labeled canaries at equal pairing and verification budgets.
- **Old-task retention:** On the replacement sensor, execute the legacy routes, including borderline permissible routes and hard negatives, and on the unchanged sensor rerun unrelated tasks after the learner acquires the new view.

### D. B/T-inspired memory: keep different forms of readiness

These are functional analogies: immediate task response, local experience, and coordination of later learning are different jobs. They do not imply a one-to-one mapping to cell types.

#### 13. Remember an experiment separately from the answer it once justified

- **Mechanism:** Keep a small bank of immediately callable policies and a separate bank of *diagnostic interventions with predicted branch outcomes*. On return, choose a diagnostic before adapting a policy; retain diagnostics that still discriminate after a policy is replaced. Unlike card 1, these interventions are stored and reused, not invented by new clones.
- **Novelty bet — primitive candidate:** Persistent separation of a reusable causal experiment from the answer it once supported. CLONALG stores responders, ID11 reads a panel of responders, and ID19 keeps per-conflict settlement conditions; this proposal asks whether a diagnostic can be reused across unrelated payloads and policy replacements.
- **Cheapest test:** A tool-use simulator swaps an action API while leaving the environment's causal relations unchanged. A generic two-action diagnostic should distinguish two failure causes after replacement. Compare against equal-byte episodic replay plus model-based active diagnosis, and a joint retrieval bank storing policy/diagnostic pairs with the same planning budget.
- **Old-task retention:** After learning the new API, test old goals that remain supported in both API versions, including goals whose old policy was not among the replaced ones. Measure first-attempt success separately from success after diagnostic calls.

#### 14. Resident memory for what the global learner never sees

- **Mechanism:** Give parts of an agent a tiny private cache of context preceding local errors; export only selected statistics to the global trainer. Keep private cache content tied to its *observation point* across a downstream policy replacement. Compare locality as an access constraint, not as free privileged information.
- **Novelty bet — improvement:** Structured AIS activation maps and ID58 role privileges are not about persistent access to transient local observations. This tests whether local memory preserves signal lost in aggregation; a central store with the same raw data is the required ceiling.
- **Cheapest test:** A symbolic workflow with noisy local action outcomes and one coarse end reward. Compare local caches, equal-byte central stratification over those same local observations, and reward-only storage; charge the same export traffic or let the central arm spend the allowance on summaries.
- **Old-task retention:** Check old workflows after a neighboring policy replacement, on local error trajectories as well as average reward; report any degradation outside the sites that had private caches.

#### 15. Transfer a branching recovery protocol, not replay content

- **Mechanism:** Learn a tiny finite-state protocol choosing between re-reading, asking for a label, and making a sandbox rollout. Its transitions depend on information obtained at the previous step. Transfer the protocol without examples or old labels to another learner that uses different policies.
- **Novelty bet — primitive candidate:** A portable policy for acquiring recovery evidence, rather than fast CLONALG recognition, PR #75 ID33's inherited tests, or the ledger's failure-triggered retrieval. The question is whether the *conditional sequence* transfers, not whether asking for help beats doing nothing.
- **Cheapest test:** Two families of toy assistants with different command sets but shared patterns of feedback availability. Compare against a budget-matched active-learning policy and the same action sequence without branching, with equal total interactions.
- **Old-task retention:** After recovery and a new command family, measure old command accuracy and clarification cost, including old unambiguous commands that ought not trigger the recovery protocol.

#### 16. Supplemental memory that proves when it can retire

- **Mechanism:** Run a small complementary policy only on experiments where the main learner's answer is uncertain. Before retiring it, compare a paired estimate of its actual causal lift to the cost of reacquiring missing competence after retirement. Sample enough reappearances to distinguish genuine redundancy from a quiet interval.
- **Novelty bet — improvement:** Unlike aiNet similarity suppression, ID13 shadow clones, or B4-R1 stability routing, retirement depends on measured *recoverability after removal*, not absence of current use. This is not a claim about programmed half-lives.
- **Cheapest test:** Recurrent nonlinear contextual bandit with two overlapping modules and irregular return gaps. Compare to leave-one-out eviction plus recency, and a central scheduler with the same trials and a hindsight return-frequency oracle reported only as a ceiling.
- **Old-task retention:** Evaluate old tasks without the retired module at multiple gaps and on their first return, then score recovery with an identical labeled reminder budget. Include the unrelated old skills that paid for keeping the supplemental policy.

#### 17. Keep the old feedback clock with the memory

- **Mechanism:** Store distributions for when feedback was historically observable, separately from policy values. On return use a missing observation to schedule an experiment only once it becomes atypical for that regime. Update the feedback model even when the task action does not change.
- **Novelty bet — improvement:** DCA aggregates temporal evidence and ID05 detects a missing sentinel; here the object is a learned delay/censoring model that preserves the difference between no reward and not yet seeing reward across returns. It must beat ordinary delayed-feedback inference.
- **Cheapest test:** Contextual bandit whose reward delays swap between action families while outcomes stay fixed. Compare to a centralized Bayesian delay model with the same state budget and a timeout-based replay learner given the same data.
- **Old-task retention:** After learning a new clock, recheck first-visit old reward and erroneous retraining on old long delays, including old actions with immediate feedback.

### E. Vaccination: choose practice for the future rather than guessing future labels

#### 18. Vaccinate with a distinction, not a prediction

- **Mechanism:** Before a shift, rehearse pairs of safe synthetic situations that currently deserve the same answer but differ in an *observable factor that could later matter*. Train a latent factor readout, not a guess at its future action label. Using the readout, learn the new action on first true feedback.
- **Novelty bet — primitive candidate:** The practice object is a label-neutral future decision axis. Model Immunization and PR #36 train responses to corrupted content; ID16 learns equivalence over update requests; ID63 splits representations using different existing consumers. Here neither the future rule nor a second old consumer is available. Compare against generic representation pretraining using the exact same factors.
- **Cheapest test:** A compositional MLP where shape governs old labels and position or color may govern a future subtask. Select discriminating practice pairs using a simulator that exposes legal knobs but hides the future assignment. Compare to balanced augmentation, supervised factor prediction on the same pairs, and active domain randomization under the same practice/label budget.
- **Old-task retention:** After first feedback teaches the new subtask, check old shape accuracy under held-out position/color combinations and false adoption of the newly relevant factor on old inputs, at matched new-label accuracy.

#### 19. Vaccinate against interference by rehearsing two skills in one episode

- **Mechanism:** Construct practice episodes that require an ordered handoff between currently mastered skills; feedback is on handoff success and side effects, not on whether each skill can execute alone. Choose compositions whose failures predict the later costs of adding a new intermediary.
- **Novelty bet — improvement:** Not corrupted-lesson training or ID57 construction-seed transfer. The technical bet over AIS and standard rehearsal is that *joint practice* preserves useful coordination better than independent practice even when per-skill exposure and update norm match. The ledger's composition-contract kill makes direct composed demonstrations a required control.
- **Cheapest test:** Two toy workflows share a serializer and later get a new intermediary using it. Compare the selected curriculum to uniformly composed episodes and oracle conflict-targeted composed rehearsal, at equal token-equivalent trace lengths, task marginals and calls.
- **Old-task retention:** After intermediary training, score old full workflows including order constraints and old standalone operations; match intermediary acquisition and report recovery under shared practice.

#### 20. Choose practice to reduce uncertainty about what to teach later

- **Mechanism:** Maintain a distribution over possible future shifts. Use a practice slot for an episode whose outcome helps choose *between future teaching curricula*, even if mastering that episode has little direct benefit. Keep the updated curriculum choice rule, not the practice episode itself.
- **Novelty bet — primitive candidate:** Treat pre-exposure as a value-of-information decision about future pedagogy. CLONALG optimizes current affinity, and the ledger's learning-progress self-curriculum ranks practice by current gains; neither asks whether today's observation changes which later lesson will be worth buying. Bayesian curriculum planning is the serious alternative.
- **Cheapest test:** Finite-state puzzles with two equally cheap lesson sequences and unknown stable learner bottlenecks. Compare against domain randomization, learning-progress allocation and an equal-budget central value-of-information planner; conceal which puzzles arrive next from all arms.
- **Old-task retention:** After the new puzzle is learned, score earlier puzzles without additional tutoring and at matched new success, especially the old family whose practice was sacrificed for the diagnostic episode.

#### 21. Learn when a booster should be withheld

- **Mechanism:** Infer from current observations whether a reminder of the oldest solution accelerates learning or anchors the wrong response. Withhold reminders when accuracy on a small set of shared features fails to predict success on new evidence, even if the old exemplar is a close match.
- **Novelty bet — improvement:** CLCMTVD already learns on shifted test data; E28 adapts the remembered responder, while PR #36 vaccination primes against bad lessons. This asks whether a *dose of correct old data* is counterproductive specifically because an old shortcut has changed sign. MIR, not no-replay, is the appropriate baseline.
- **Cheapest test:** Feature-learning MLP over recurrent distributions with independent cue familiarity and shortcut validity. Compare to [MIR](https://arxiv.org/abs/1908.04742) plus recency and held-out old losses under the same total labels, updates and update norm; use a common shuffled suffix to determine how long any priming cost lasts.
- **Old-task retention:** Measure old shortcut-valid accuracy separately from old unaffected tasks before and after the shifted return. A faster new fit fails if the common-task retention cost exceeds the predeclared floor.

#### 22. Exchange practice *gaps* between agents

- **Mechanism:** One agent transmits a compact specification of distinctions its curriculum did not test. The receiver chooses a practice episode to cover a gap only if it also remains untested in its own learner. Share a falsifiable statement of missing coverage rather than an answer or a repair.
- **Novelty bet — primitive candidate:** The transferable object is a curriculum gap measurable by an independent agent. This is not aiNet cross-stimulation, PR #75 ID14 evidence merging, ID15 inference coverage, or the ledger's lesson portability: it transmits where to collect evidence, not which lesson works on another model.
- **Cheapest test:** Two symbolic game players have disjoint histories and different encodings of board state. Compare gap specifications with equal-byte exchange of examples, a performance summary and centralized coverage planning with the same shared information and practice menu.
- **Old-task retention:** After additional practice, test standard old positions for both agents and old edge cases that only one had mastered. Require a gain on held-out future rule combinations, not merely agreement about which gaps exist.

## Ranked deeper sub-questions

1. **Can a reusable diagnostic outlive the policy it originally justified?** Start with card 13. Cross API replacement with a change in failure cause; hold out API/cause combinations and test independent policy and diagnostic reuse against a joint memory bank and same-information model-based diagnosis. The case for a separate memory primitive dies if a joint bank or fresh diagnosis matches first-return regret and old-task service at equal cost.
2. **Does contraction select different learners when judged by what they can teach?** Card 2 separates candidate fitness from the utility of the retained packet. First require that the best scratch clone and the best packet source differ on fresh seeds; then require lower cumulative loss than direct selection/distillation with no loss of old service. If both rank candidates alike, stop.
3. **Can a pre-exposure curriculum buy readiness without buying the future answer?** Card 18: hold the practice transcript fixed and randomize the later assignment. If ordinary factor prediction matches pair-based practice, it is representation learning, not a new vaccination primitive. If pair selection survives, test card 20's stronger claim that pre-exposure changes which teaching strategy to use.
4. **Can verified coverage be handed off without migrating forgetting into the gaps between checks?** Combine card 8's reassignment with card 9's outcome-based notion of legitimate service only after each clears its standalone baseline. Sweep hidden ambiguity between old skills and blind spots of the audits; compare against the stacked global cover + invariant verifier at equal bytes and checks. Fail on worst-old service, not just on mean coverage.
