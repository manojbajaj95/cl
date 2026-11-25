# Root: Continual verifiers, wider search

Wide root (depth 0) · 32 idea cards · **Ambitious but doable** · Ideas only; no experiments run

**Thesis.** A verifier can learn more than how to answer the next case. It can learn which conclusions the available observations cannot support, what looking at many candidates does to its error rate, how to correct a live evaluation without rewarding the wrong agent, and which kinds of external checking are worth buying. Those are different learning targets, with different evidence and retention tests. None requires treating a model's agreement as proof.

**Pramaana Labs.** The [everyday-provers report](https://pramaanalabs.ai/blog/towards-everyday-provers-for-real-world-verification) compares Hardy's proof-search efficiency across statutory, software and math benchmarks. In its [unsatisfiability report](https://pramaanalabs.ai/blog/the-other-half-of-reasoning-proving-unsatisfiability), Hardy uses a symbolic solver and reconstructs a Lean 4 proof for satisfiable and unsatisfiable Sudoku instances. Together with [Panini's formalization stage](https://pramaanalabs.ai/blog/pramaana-solves-imo-2026-in-lean-4-in-under-7-hours), this suggests a productive boundary: let the learned layers discover what to formalize or test, while requiring each checked result to state exactly which question, model and quantifier it covers. The proposals below are ours, not claims about Pramaana's roadmap.

**Scope and literature.** This is a sibling search off the [first root](root-continual-verifiers.md), not a continuation of the [paused branch](https://github.com/manojbajaj95/cl/pull/415). The [reviewer triage](https://github.com/manojbajaj95/cl/blob/179977548256ca89a45b243ea4e2beaf44068de5/reviews/flood-triage.md#L573-L576) and [idea ledger](https://github.com/manojbajaj95/cl/blob/179977548256ca89a45b243ea4e2beaf44068de5/reviews/idea-ledger.md) rule out presenting update-aware unlearning, stitching, distillation, tactic rebinding and change-impact invalidation as fresh directions. The cards do not carry forward old verdicts across rule edits, repair past policy updates, or attach expiry to progress labels. Targeted literature searches inform each nearest-prior comparison; they are not an exhaustive novelty review. **P** means a candidate reusable verification operation or object; **I** means an improvement, application or assay. A matched tie drops the primitive claim.

**First-test convention.** Use an enumerable toy world with an external oracle. Stream a change and then a recurrence; score each verdict before its label is revealed. Compare at equal independent labels, compute, state bytes and answer coverage where applicable. Report false accepts, false rejects, abstentions and true task success separately. Retention means live performance on untouched old tasks, not archived scores. All tests below are proposals.

## A · Learn what the formal model can and cannot certify

### CVW-01 · Learn to verify properties shared by every optimal answer — Ambitious but doable (I)
- **Mechanism:** Separate a solver's chosen optimum from properties forced by optimality. Train a formalizer on pairs of certified optima that disagree about a property, alongside cases where constraining the property to its negation provably worsens the optimum. One optimal solution is not a uniqueness proof.
- **Nearest prior / gap:** [Optimization backbones](https://arxiv.org/abs/1704.04775) already capture assignments shared by all optima. The proposal applies ordinary constrained optimization to a continual audit of what formalizers claim is forced, not a new backbone algorithm.
- **Cheapest first test:** Change a toy scheduler's tie-breaking strategy without changing its objective. Compare solver-output labels, randomized alternative optima and checked negation constraints on claims such as “this shift must be staffed by Ada.”
- **Old-task retention:** Keep proving the genuinely forced assignments in uniquely solved and multiply solved legacy schedules.

### CVW-02 · Negative proofs that name their quantifier — Ambitious but doable (I)
- **Mechanism:** Train the formalizer to distinguish “this proposed packing fails,” “none of the packings in this finite catalog work,” and “no packing exists.” Return the strongest checked statement obtained, with the catalog or domain explicit. Collect errors where search success encouraged a stronger statement than the proof warranted.
- **Nearest prior / gap:** [LeanTrail](https://arxiv.org/abs/2610.35926) audits what paper-to-Lean artifacts actually prove; [Hardy's unsatisfiability report](https://pramaanalabs.ai/blog/the-other-half-of-reasoning-proving-unsatisfiability) demonstrates checked global negation. This is supervision on the ladder of negative claims, not a new unsatisfiability algorithm.
- **Cheapest first test:** Stream finite schedules containing a failed candidate, a failed subcatalog or genuinely no solution. Compare quantifier-labeled training with matched binary correctness training and a hand-written statement classifier.
- **Old-task retention:** Preserve positive feasibility yield and correct global negatives on a held-out legacy schedule family.

### CVW-03 · Joint realizability before composing separate proofs — Ambitious but doable (P)
- **Mechanism:** When different formalizers close subclaims by choosing different completions of the same underspecified entity, require one shared completion before publishing the conjunction. Return a checked joint witness or an inconsistency proof over the shared choices; proof success for each subclaim alone cannot pass.
- **Nearest prior / gap:** [MechAlign](https://arxiv.org/abs/2610.35269) studies project-level semantic alignment. The proposed reusable interface exposes existential choices across otherwise opaque checked subclaims. If an ordinary shared constraint model gives the same composability and cost, this is constraint solving, not a primitive.
- **Cheapest first test:** Two verified allocations each admit a different common warehouse location but none admit the same one. Stream new subclaim producers and compare a shared-choice interface with monolithic solving and separate checks plus alignment review.
- **Old-task retention:** Keep accepting subclaims whose completions are independent or share an attainable location.

### CVW-04 · Separate a true theorem from a specification with teeth — Ambitious but doable (I)
- **Mechanism:** Teach formalization review using pairs: a valid theorem and a checked example of bad behavior that its specification still allows. Learn which recurring omissions need a strength check, with the examples generated from an independent bad-behavior model.
- **Nearest prior / gap:** [DafnyCert](https://arxiv.org/abs/2611.15548) already certifies specification strength. This is an improvement in allocating strength checks across families, not a new way to certify a spec or transplant a translation repair.
- **Cheapest first test:** Require a sorted list but omit preservation of its elements in one family. Hide a second weakness in a later task family. Compare learned allocation to exhaustive and uniform mutation checks at matched checking time.
- **Old-task retention:** Continue to spot the old omission without rejecting specifications whose task genuinely permits discarded elements.

### CVW-05 · Blind reconciliation across semantic encodings — Ambitious but doable (I)
- **Mechanism:** Run two formalizations with independently specified representations; before seeing the other's conclusions, each submits a concrete trace. Check whether both can interpret each trace and produce the same authorized observable result. Do not require full implementation equivalence.
- **Nearest prior / gap:** [SemantEq](https://arxiv.org/abs/2610.32919) looks at bidirectional equivalence of formal statements. This is a cheaper differential review assay for concrete traces, not an equivalence proof or a rule-version migration.
- **Cheapest first test:** Independently encode a toy deadline in elapsed minutes and as a calendar relation. Compare blind trace exchange with ordinary differential testing and same-encoding review on daylight changes and inclusive cutoffs.
- **Old-task retention:** Preserve agreement on standard dates and faithful handling of both legacy inclusive and exclusive endpoints.

### CVW-06 · Verify a secret case without turning it into training data — Ambitious but doable (I)
- **Mechanism:** Let a case holder prove a public pass/fail predicate about committed private inputs. Train only on public task metadata and the verified bit; record the disclosure policy separately so later reviewers know what was never observed.
- **Nearest prior / gap:** [Zero-Knowledge Model Checking](https://arxiv.org/abs/2605.00487) already provides the privacy mechanism. The improvement is testing whether verified low-disclosure feedback remains useful across verifier updates, not new cryptography.
- **Cheapest first test:** Simulate a private household budget with a public eligibility predicate. Compare signed labels, redacted examples and ideal proof-gated labels on label corruption, reviewer cost and future decision quality.
- **Old-task retention:** Preserve utility on public legacy cases and check that neither updated predictions nor stored artifacts expose held-out private attributes beyond an agreed baseline.

## B · Verify process judgments without rewarding presentation

### CVW-07 · Make a reward invariant to splitting a step — Ambitious but doable (P)
- **Mechanism:** Specify the credit operation on decompositions of the same execution: replacing one transition by certified substeps must leave total credit unchanged, including across different learned graders. Train a transition-level estimator with this refinement constraint; endpoint-only scoring is a competing explanation.
- **Nearest prior / gap:** [Rewarding Progress](https://arxiv.org/abs/2410.08146) already telescopes differences of a common potential, and [dynamic reward shaping](https://arxiv.org/abs/2608.08158) is a direct control. The only primitive claim is cross-grader refinement with intermediate information that a single common potential cannot recover at equal supervision.
- **Cheapest first test:** Re-express packing moves as either single actions or two micro-actions, with a hidden intermediate constraint violation. Compare a common potential with a violation flag, outcome-only scoring and refinement-constrained credit. A common-potential tie kills P.
- **Old-task retention:** Preserve legacy ranking and violation sensitivity when old step boundaries recur unchanged.

### CVW-08 · Lock the prefix judgment before revealing the answer — Ambitious but doable (I)
- **Mechanism:** Train and audit a judge on prefix/commit/reveal pairs. Record what was inferable from the prefix before showing its outcome, then elicit a separate error attribution on reveal; do not backfill the pre-reveal label from hindsight.
- **Nearest prior / gap:** [GroundedPRM](https://arxiv.org/abs/2510.14942) uses tree-guided process supervision. This is a prospective judging assay, contrasting identical prefixes with different continuations rather than proposing another progress estimator.
- **Cheapest first test:** Pair arithmetic traces with identical prefixes and correct, incorrect or lucky endings. Compare outcome-masked scoring plus matched supervised prefixes with the commit/reveal protocol on hindsight reversals.
- **Old-task retention:** Keep finding invalid legacy prefixes that happen to end with a correct answer.

### CVW-09 · Require the stated reason to be enough — Ambitious but doable (I)
- **Mechanism:** Ask a generative verifier for the smallest evidence slice sufficient to support its judgment. In a finite domain, independently test the judgment over all allowed completions of that slice. Train on insufficient explanations even when the full-input verdict was right.
- **Nearest prior / gap:** [Evaluation-process supervision](https://arxiv.org/abs/2611.32161) already trains generative reward models on how they evaluate. This adds a completion-based sufficiency test for rationales, not a witness compressor or proof of the model's internal reasoning.
- **Cheapest first test:** In three-line arithmetic proofs with irrelevant annotations, compare generated rationales graded by a model, evidence masking, and exhaustive completion checks at equal reviewed examples.
- **Old-task retention:** Preserve correct judgments on older valid proofs with multiple alternative sufficient explanations.

### CVW-10 · Check the act of choosing, not a random candidate — Ambitious but doable (I)
- **Mechanism:** Calibrate on the entire candidate-generation and selection procedure. Log the branch count, correlated proposal families and stopping rule; the quantity to bound is the error of the selected answer, not marginal per-candidate accuracy.
- **Nearest prior / gap:** [Reward model overoptimization](https://arxiv.org/abs/2210.10760) documents selection pressure, and [feedback-enhanced online multiple testing](https://arxiv.org/abs/2509.03297) supplies relevant statistical machinery. This is a selection-aware calibration improvement, not a guarantee that selection-neutral thresholds transport.
- **Cheapest first test:** Change best-of-4 to adaptive best-of-16 over near-duplicate traces. Compare direct winner calibration with per-item calibration, Bonferroni-style thresholds and group-wise calibration at matched winner coverage.
- **Old-task retention:** Preserve established error and coverage on old low-budget and high-diversity search regimes.

### CVW-11 · Learn to reject edit-irrelevance as a reason for correctness — Ambitious but doable (I)
- **Mechanism:** For an incorrect trace, find and check two minimal edits: one repairs it, the other changes as many tokens but leaves it incorrect. Train the judge on the contrast so explanation credit cannot come from merely noticing an edit.
- **Nearest prior / gap:** [GenPRM](https://arxiv.org/abs/2504.00891) learns generative checking; [Metamorphic Coverage](https://arxiv.org/abs/2508.16307) quantifies metamorphic tests. This is a matched supervised contrast, not a reusable semantic repair witness or a claim of new mutation machinery.
- **Cheapest first test:** Compare explanations for numeral fixes and equally sized whitespace or variable-renaming edits; hold out a family where a small operator replacement really matters.
- **Old-task retention:** Maintain false-reject rates on naturally concise and verbose valid traces, not just on synthesized pairs.

### CVW-12 · Distinguish a propagated error from a second mistake — Ambitious but doable (I)
- **Mechanism:** Train a process verifier to label local validity conditional on the stated input to a step, as well as global validity from the task's original premises. A legitimate operation on a wrong intermediate is not a second local mistake; an unrelated bad operation is.
- **Nearest prior / gap:** [Progression-aware Reasoning Origin](https://arxiv.org/abs/2609.33297) already checks incoming and outgoing evidence to locate where a propagated error started. Compare it directly: this two-target improvement must find independent secondary errors, not merely locate the first one.
- **Cheapest first test:** Inject an early numeral error into arithmetic traces, then apply the rest of the steps faithfully or inject an additional error. Compare earliest-error labels, per-step binary scoring and conditional supervision on independently locating both errors.
- **Old-task retention:** Preserve recognition of valid legacy derivations and reject old traces whose sole mistake contaminates every later result.

## C · Co-evolve without learning that agreement means correctness

### CVW-13 · Change the optimization view without changing the decision — Ambitious but doable (I)
- **Mechanism:** Keep a fixed binary verifier but rotate between dense training-side proxy signals engineered to agree on terminal reward and differ on intermediate incentives. Record when the learned policy succeeds only with the proxy it saw, to choose a safer future training signal.
- **Nearest prior / gap:** [Dynamic reward shaping](https://arxiv.org/abs/2608.08158) already changes shaping signals and [Verifier Errors in RLVR](https://arxiv.org/abs/2609.35677) studies imperfect feedback. This is a proxy-sensitivity assay, not a selective undo of learned policy changes.
- **Cheapest first test:** Use a grid with two valid paths and a long dead end that one dense proxy favors. Compare rotating proxies, endpoint-only reward and fixed shaping, with equal oracle calls and policy steps.
- **Old-task retention:** Keep success on legacy maps where one pathway still needs informative dense feedback.

### CVW-14 · Exchange failures across independently co-evolving lineages — Ambitious but doable (I)
- **Mechanism:** Run two solver–grader lineages on the same authorized task with disjoint development feedback. Periodically give each grader the other solver's accepted outputs and independently adjudicate wrong cross-lineage acceptances. Exchange concrete misses, not scores or parameters.
- **Nearest prior / gap:** [Co-Evolving Inspectable Graders](https://arxiv.org/abs/2610.11464) and [Verifier-Harness Co-Evolution](https://arxiv.org/abs/2610.17609) already revise checks while agents improve. This is a cross-play control for local conventions, not a new co-evolution algorithm.
- **Cheapest first test:** Give two arithmetic agents different harmless output conventions and seed one false shortcut per grader. Compare cross-play with pooled development and extra within-lineage sampling at equal adjudications.
- **Old-task retention:** Preserve acceptance of both harmless conventions on legacy tasks while rejecting the seeded shortcuts.

### CVW-15 · Pay for a useful challenger, not for finding something to reject — Ambitious but doable (I)
- **Mechanism:** Give a verifier revision proposer separately scored jobs: expose accepted failures and defend valid outputs against overbroad rejection. Score both jobs with a frozen external oracle, then select on a fixed tradeoff rather than number of caught errors.
- **Nearest prior / gap:** [Prover–verifier games](https://arxiv.org/abs/2108.12099) already train strategic participants for checkable answers, and [Veritas](https://arxiv.org/abs/2611.13336) generates agent verifiers. The proposal is a two-sided objective for revising a checker, not a new game equilibrium.
- **Cheapest first test:** Generate packings accepted by an imperfect checker and borderline valid packings; compare failure-only, mixed and two-role proposals at equal oracle calls.
- **Old-task retention:** Preserve true accepts on old border cases the challenger never sees during revision.

### CVW-16 · Predict which review edit would hurt the grader — Ambitious but doable (I)
- **Mechanism:** Ask a self-improving checker to pre-register, before scoring, which candidate checker edit will reduce or increase false accepts and false rejects. Use its forecasting errors as a supervised target, separately from its verdicts; do not authorize promotion based on the forecast.
- **Nearest prior / gap:** [Co-Evolving Inspectable Graders](https://arxiv.org/abs/2610.11464) already improves inspectable graders; [proper scoring for LLM forecasts](https://arxiv.org/abs/2608.28482) supplies the prediction baseline. This is an assay of self-knowledge, not a self-verification gate or a downstream policy teaching receipt.
- **Cheapest first test:** Predict the effect of adding exact equality, tolerance or a syntax check to toy graders. Compare forecasting from edit descriptions with direct canary results and a calibrated edit-type lookup.
- **Old-task retention:** Score forecasting calibration on withheld edits to older graders, and keep ordinary verdict quality unchanged.

### CVW-17 · Promote a grader only if users still ask it hard questions — Ambitious but doable (I)
- **Mechanism:** Measure when changing the public checker changes what verification requests get submitted at all. Keep a randomized nonbinding exposure arm and collect downstream independent labels for questions that disappeared from the binding arm where the toy setting allows it.
- **Nearest prior / gap:** [Performative Prediction with Selective Labels](https://arxiv.org/abs/2610.08272) models selective observation under deployment. This improvement studies request suppression, rather than CV28's changes in the solver's outputs on requests it actually sees.
- **Cheapest first test:** Applicants decide whether to submit a simulated eligibility request after seeing an advisory score. Compare promotion on submitted accuracy with exposure-arm estimates and a standard selective-label correction.
- **Old-task retention:** On a legacy cohort, measure both decision accuracy and submission access; neither may be traded away for average accuracy.

## D · Adapt at test time with a named risk target

### CVW-18 · Tune the reader on unlabeled streams, not the rule — Ambitious but doable (I)
- **Mechanism:** Split a learned checker into a parser and a decision module. Adapt the parser at test time using paired renderings of unchanged inputs, then measure whether the decision module sees the same fields. Treat a semantic change as outside the update objective.
- **Nearest prior / gap:** [Continual test-time domain adaptation](https://arxiv.org/abs/2203.13591) already updates models online; the improvement is constraining which checker state can adapt and supplying verifiable rendering pairs, not learning new acceptance rules from pseudo-labels.
- **Cheapest first test:** Alternate synthetic receipts with column swaps, new delimiters and one actual definition change. Compare parser-only adaptation with frozen parsing, fixed normalization and end-to-end CoTTA.
- **Old-task retention:** Preserve exact extraction and verdict safety on old layouts, including confusable fields never given as adaptation pairs.

### CVW-19 · Quote a risk bound in the target traffic, or disclose no overlap — Ambitious but doable (I)
- **Mechanism:** When verifier routing changes, use logged review probabilities to estimate false accepts on the new traffic only where labels have support. Report covered risk and the weight of unsupported regions separately instead of filling them with judge confidence.
- **Nearest prior / gap:** [Counterfactual online conformal prediction](https://arxiv.org/abs/2609.30811) handles adaptive logging; [Hidden Tails](https://arxiv.org/abs/2611.12713) certifies risks with selectively available labels. This is a direct application, not a new transport estimator.
- **Cheapest first test:** Change which receipt categories receive review, including one with zero historical review probability. Compare naive recalibration with weighted and partial-identification controls, and measure whether warnings match the unsupported mass.
- **Old-task retention:** Preserve decision coverage and bounded error in previously well-reviewed groups, without letting the new unsupported group disappear into their average.

### CVW-20 · Keep pending verdicts in the risk denominator — Ambitious but doable (I)
- **Mechanism:** At each release, count undecided audit outcomes as potential errors until they settle, or use a delay model with independently defended bounds. Adapt on the resolved labels but expose the worst-case gap between resolved and full-traffic risk.
- **Nearest prior / gap:** [Delayed-feedback conformal risk control](https://arxiv.org/abs/2611.17059) already addresses capacity limits. This is a verifier rollout assay for informative delay, not an independent holdout construction.
- **Cheapest first test:** Simulate a queue where wrong decisions take twice as long to settle, then change queue capacity. Compare completed-only estimates, delayed-risk control and worst-case pending correction at matched review throughput.
- **Old-task retention:** On fast-settling legacy tasks keep alert latency and approval coverage near the completed-only baseline at equal true risk.

### CVW-21 · Choose between one pooled guarantee and two deployable ones — Ambitious but doable (I)
- **Mechanism:** Maintain risk estimates for old and new populations separately and learn whether splitting them improves deployable coverage at a fixed false-accept ceiling for each. A pooled guarantee earns no credit if a small old group becomes unreliable.
- **Nearest prior / gap:** [Adaptive Conformal Inference](https://arxiv.org/abs/2106.00170) and [conformal sets under LLM-judge traffic shifts](https://arxiv.org/abs/2609.27955) already address coverage adaptation and shifting group mixtures. This is a group-retention benchmark, not a new conformal method or independence receipt.
- **Cheapest first test:** Move from 80/20 to 20/80 task traffic, with an asymmetric verifier error shift in the old minority group. Compare pooled, worst-group and split calibration at fixed labels.
- **Old-task retention:** Report both old family-specific error and old family-specific coverage after the mixture switches back.

### CVW-22 · Check whether a cheap shadow grader is still an experiment — Ambitious but doable (I)
- **Mechanism:** Randomly assign some frozen cases to two shadow checkers without exposing results to submitters. Monitor agreement and independently verified accuracy separately; use paired cases to test whether their errors became correlated during adaptation.
- **Nearest prior / gap:** [Monitoring-by-betting](https://arxiv.org/abs/2610.17399) supplies sequential shift tests; [Robust Conformal Consensus](https://arxiv.org/abs/2609.06367) combines judges. This is a drift assay of paired errors, not an ensemble provenance receipt or a claim that dissent supplies truth.
- **Cheapest first test:** Update two arithmetic checkers on a shared pseudo-label stream that makes them jointly miss one error. Compare raw disagreement, paired adjudication and independent per-model auditing at matched oracle budget.
- **Old-task retention:** Keep sensitivity to legacy failure modes on which only one model errs and preserve false-alarm rates during stable periods.

## E · Buy checkable information through markets and debate

### CVW-23 · Buy the right to challenge an entire class of verdicts — Ambitious but doable (P)
- **Mechanism:** A bounty pays once for a mechanically checkable family of misses, assessed against a frozen eligibility rule, not once for each paraphrase. After the family is accepted, independently sample from it and vary later bounties based on independently verified prevalence.
- **Nearest prior / gap:** [Evidence Markets](https://arxiv.org/abs/2606.07434) is the exchange baseline; [Recommendations with Costly Verification](https://arxiv.org/abs/2611.01195) studies inspection costs. Candidate object: a payment unit defined by a checked generator and its incremental coverage, not by individual evidence submissions.
- **Cheapest first test:** Simulate reporters that can cheaply enumerate paraphrases or discover an independent arithmetic error family. Compare per-item bounties, clustering plus deduplication and checked family bounties at equal payouts and oracle costs.
- **Old-task retention:** Keep previously discovered families detectable; avoid pricing rare legacy failures out of discovery through a frequency-only payout.

### CVW-24 · Buy a pre-verdict forecast that remains scorable after abstention — Ambitious but doable (I)
- **Mechanism:** Collect sealed forecasts before the verdict is released. Settle a random, declared subset against an independent oracle even when the operational judge abstains; separate forecast accuracy from whether the forecast was acted on.
- **Nearest prior / gap:** [Proper scoring rules for LLM forecasts](https://arxiv.org/abs/2608.28482) already shape beliefs; [PeerBTS](https://arxiv.org/abs/2605.24165) addresses effort incentives. This is a selectively settled forecasting design, not an incentive theorem for arbitrary markets.
- **Cheapest first test:** Compare random settlement, settlement only after approval and peer agreement when disagreement cases are systematically deferred. Equalize human checks and payout budgets.
- **Old-task retention:** Preserve forecast calibration and elicited effort on old routine cases, not just on new contested cases.

### CVW-25 · Separate a valid objection from a win against a weak defender — Ambitious but doable (I)
- **Mechanism:** Put an objection in a standalone record that fixes the disputed assertion and the rules of reply. Reuse the objection against multiple independently sampled defenders; learn from whether the objection survives independently checked replies, not how often its original speaker won.
- **Nearest prior / gap:** [Sensitive Debate](https://arxiv.org/abs/2610.02557) checks decompositions recursively; [When Honesty is Not Enough](https://arxiv.org/abs/2609.29189) analyzes failure under debate assumptions. This is an opponent-pool assay for reusable criticism, not a novel debate protocol or a query policy.
- **Cheapest first test:** Compare a true arithmetic counterexample and a plausible distractor against agents with different proof-verbalization skills. Compare single-match wins, round-robin wins and independently checked objections.
- **Old-task retention:** Keep old sound objections effective even as defenders get better at answering style-based objections.

### CVW-26 · Give a debate judge an independently settled “neither” outcome — Ambitious but doable (I)
- **Mechanism:** Score the adjudicator on whether either submitted answer is valid before comparing argument quality. Include debates where both proposed answers fail, and teach the judge to distinguish a checked double rejection from “not enough evidence to judge either.”
- **Nearest prior / gap:** [AI Safety via Debate](https://arxiv.org/abs/1805.00899) introduces adversarial judging, and [When Honesty is Not Enough](https://arxiv.org/abs/2609.29189) scrutinizes debate assumptions. This is a selective-outcome assay for systems that elicit two answers, not a new mechanism for adversarial truth elicitation.
- **Cheapest first test:** Vary the rate at which both candidates in a small arithmetic debate are wrong. Compare forced choice, confidence abstention and separately supervised double rejection, using exact labels outside the debate.
- **Old-task retention:** Continue picking the valid answer on old one-correct debates; “neither” should not become the default on unfamiliar arguments.

### CVW-27 · Run a market for the cost of checking, not for truth — Ambitious but doable (I)
- **Mechanism:** Ask check suppliers to quote time and cost for an authorized verification job. Use occasional randomized assignments to measure actual cost, correctness and deadlines, then adapt allocations. An arbitrarily cheap quote does not count as evidence.
- **Nearest prior / gap:** [Evidence Markets](https://arxiv.org/abs/2606.07434) trades on evidence; [Recommendations with Costly Verification](https://arxiv.org/abs/2611.01195) treats costly checks. This is a procurement baseline with audited service quality, not a claim of strategyproofness.
- **Cheapest first test:** Simulate checkers with different costs on routine and novel tasks and one overly optimistic seller. Compare fixed prices, lowest bid and quality-adjusted randomized procurement at equal total cost.
- **Old-task retention:** Maintain timely coverage of legacy low-volume case types when new high-volume cases attract most offers.

## F · Learn checkers for agents whose actions outlive the answer

### CVW-28 · Judge success at a stopping rule, not a log line — Ambitious but doable (I)
- **Mechanism:** Learn to predict when a workflow can be safely evaluated, separately from success. Use authoritative completion events to train the stopping policy and count stale premature verdicts as errors even if the eventual state is good.
- **Nearest prior / gap:** [Outcome Finality and Cross-Unit Separation](https://arxiv.org/abs/2608.14940) already defines the finality problem. This is an online estimate of decision time, not a new settlement semantics.
- **Cheapest first test:** A toy reservation system emits a success message before a delayed capacity check. Compare fixed timeouts, finality events and a learned stopping rule as delays change.
- **Old-task retention:** Keep latency and accuracy for synchronous legacy actions; rejecting early verdicts must not force waiting in cases known to be settled.

### CVW-29 · Detect the task another agent accidentally completed — Ambitious but doable (I)
- **Mechanism:** Evaluate outcome and agent contribution separately. In a simulator, replay the same exogenous updates with and without the target agent's action, and supervise a lightweight checker on the resulting attribution. Mark missing counterfactual support explicitly in deployment.
- **Nearest prior / gap:** [Auditing Action Settlement](https://arxiv.org/abs/2610.01138) addresses order, progress and replay; [Outcome Finality and Cross-Unit Separation](https://arxiv.org/abs/2608.14940) addresses interference. Improvement: learning a proxy for controlled no-action attribution, not a new causal estimator.
- **Cheapest first test:** Two scripted agents update a shared calendar, only one causing a reservation to persist. Compare postcondition-only scoring, event attribution and oracle replay at matched logging.
- **Old-task retention:** Preserve full credit for the target on isolated old jobs and correct behavior on legacy cooperative jobs where success really is shared.

### CVW-30 · Verify the recovery outcome without calling it the original success — Ambitious but doable (I)
- **Mechanism:** Label original fulfillment, restoration of invariants, and remediation costs separately. Learn a checker for the recovery predicates on real recovery traces, never automatically awarding fulfillment when compensation merely restores the starting state.
- **Nearest prior / gap:** [Janus](https://arxiv.org/abs/2609.38266) supports evidence-before-effect sagas, and [Evidence-Guided Recovery](https://arxiv.org/abs/2610.41453) addresses ambiguous actions and partial execution. This is an improvement in supervision for compensation, not a new transaction protocol.
- **Cheapest first test:** A simulated reservation partly executes; compensating actions recover capacity but do not satisfy the request. Compare scalar success with separate recovery labels under new failure schedules.
- **Old-task retention:** Preserve full credit for timely successful reservations and recognize legitimate cancellations required by legacy tasks.

### CVW-31 · Ask whether the verdict changes under any legal history — Ambitious but doable (P)
- **Mechanism:** Given a partial event order and the rule for scoring a workflow, return a checked pair of legal serializations with opposite scores, or certify that they all score alike within a bounded model. Train a fast checker to route cases into those two proof searches, not to certify a single guessed timeline.
- **Nearest prior / gap:** [Auditing Action Settlement](https://arxiv.org/abs/2610.01138) checks order and replay, and [Substep Linearizability](https://arxiv.org/abs/2610.16099) extends sequential specifications. The candidate operation is reasoning about invariance of the *score* over legal histories, not showing some history is legal. If ordinary bounded model checking is equally composable and cheap, P falls.
- **Cheapest first test:** Run two agents placing and releasing simulated reservations with one missing cross-service order edge. Compare timestamp sorting, linearizability checking plus replay and two-history certificates as concurrency increases.
- **Old-task retention:** Continue deciding legacy totally ordered histories cheaply; new ambiguity must not force extra search on fully observed cases.

### CVW-32 · Check for unintended public state changes, not just changed fields — Ambitious but doable (I)
- **Mechanism:** Learn a shortlist of externally observable consequences to query after an agent acts. Train from authoritative state differences projected through a fixed observation specification, so the checker does not treat harmless internal rewrites as failures or ignore user-visible derived changes.
- **Nearest prior / gap:** [Runtime Validation of Persistent Outcomes](https://arxiv.org/abs/2609.31301) already checks persistent effects after approved actions. This is a learned check-budget allocation improvement, not a new way to prove absence of side effects.
- **Cheapest first test:** A scheduling agent updates one booking but indirectly alters a shared availability total. Compare fixed postconditions, random probes and learned consequence selection at equal state reads.
- **Old-task retention:** Keep finding older persistent effects while accepting harmless cache or bookkeeping changes in unchanged workflows.

## Ranked deeper questions

1. **Can a verifier reuse an exact bound on what a partial history settles?** Start with CVW-31. Compare timestamp replay, ordinary bounded model checking and paired history certificates across new score predicates and recurring workflows. Kill the primitive claim if the controls match safe answer coverage, checking cost and old-task retention; keep the benchmark if useful.
2. **Can intermediate feedback respect step refinement without being just potential shaping?** Start with CVW-07. Compare a common potential with explicit violation state, endpoint scoring, and refinement-constrained cross-grader credit under held-out decompositions and equal labels. If the shared potential matches true success, intermediate violation detection and legacy ranking, this is shaping, not a new reward object.
3. **Does debate learn useful criticism or just learn whom it can beat?** Pair CVW-25 and CVW-26; switch to held-out defenders and independently vary whether either has a correct answer. Test whether independently checked objections predict true verdicts and retain value better than round-robin scores at equal budget. A tie leaves ordinary cross-play as the baseline.
4. **Which verifier errors are manufactured by deployment rather than inherited from the grader?** Pair CVW-10 and CVW-17: increase internal search while independently changing whether users see the grader before submitting. Evaluate winner calibration and request suppression separately. A standard selection-aware calibrator plus a randomized exposure arm is the default if it accounts for both effects.
5. **Does paying for checked families discover different failures at the same cost?** Test CVW-23 against per-item payments with strong deduplication at equal audit cost and payouts. Score independently confirmed new family coverage, resistance to overlapping generators, and recall on old rare faults. If deduplication ties, keep the simpler bounty.
