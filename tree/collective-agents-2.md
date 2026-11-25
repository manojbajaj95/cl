# Collective agents II: renew the evidence, not the echo

**Status:** Ideas only; no learner experiments, implementation, or GPU work. **Parent:** [Collective agents](root-collective-agents.md) ([PR #310](https://github.com/manojbajaj95/cl/pull/310)). **Review seeds:** [Flood triage, lines 426–429, with #310 on line 428](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L426-L429) on [PR #6](https://github.com/manojbajaj95/cl/pull/6) gives score 3 to **#10 re-derivation leases** (copies do not renew) and **#02 echo-cancelling updates** (subtract a model-labelled same-input gradient). The review awarded no 4s; it treats the subtraction as a potential control variate, not evidence of a new learning rule. Both seeds are baselines here.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Do not resubmit surprisingly-popular fleet memory, bagged writers, coded replicas, HW1 rediscovery voting, forecast-only obsolescence, or offline replay A/B based on importance weighting of archived agent runs. Cards using randomized verification log propensities in a new stream and must beat fresh-only and prospective randomized controls; they cannot recover outcomes with zero support. None of the cards assumes that a matching lineage, a verifier's approval, or a synthetic label is new information.

## Two distinctions the child depends on

1. **A successful use may say nothing about which part of a skill worked.** A root lease attaches to an item. A lease on a *claim about behaviour* could instead distinguish what the observation actually tested, which callers it covers, and which components still need evidence. An expiry means unknown, not false. A verifier can be causally independent of a prediction while the action or context being tested is still selected by it.
2. **Cancellation needs a declared target.** Let the receiver be at parameters θ and let g(y) = ∇θ ℓθ(x,y). For a normalized likelihood and y sampled from the receiver at fixed x, E[g(y) | x,θ] = 0 (standard score identity). Two independent self-label draws therefore give zero mean and *twice* the conditional gradient covariance of one; matching the exact same draw cancels it deterministically, which is equivalent to discarding that self-label. Subtracting an argmax gradient generally changes the mean. If the teacher is stale, E_teacher[g(y)] need not vanish at the receiver. In squared-error linear regression, g(y) = x(xᵀθ − y), so subtracting the exact same-input mean of a current self-label leaves the ordinary gradient unchanged. These are algebraic checks, not results. Test exact/soft, independent-sampled, shared-draw and argmax variants separately. Do not credit variance reduction for an estimand change, or credit an estimand change for a smaller update norm.

## First-test contract

- Use the parent's CPU FleetWorld-tab, starting with enumerable two-to-four-agent worlds and fixed paired arrival/delivery seeds. Every arm—including the legal central scheduler—gets K1 local raw data, K2 equal message bytes, K3 asynchronous delivery, K4 outputs feeding subsequent actions or learning, and the same total ground-truth budget R. Charge both short-lived buffers and persistent bytes, counterfactual executions, diagnostics, model reads and gradients. The scheduler only sees the same lawful messages at the same times; unconstrained full information is a ceiling, not a comparator.
- Every lease card runs time expiry, usage expiry, no expiry, evidence-mass weighting and root #10 with the candidate's acquisition schedule; every gradient card runs fresh-only, uniform fresh-data mixing, verification/filtering, root #02 including argmax, and the relevant control-variate estimator. Hybrid cards also run the two strongest components stacked independently. Match R, deployments, and step/compute budgets; report current-task performance and update norms rather than comparing only retention. Include a nominal world and the stated failure case. A proposal dies if the closest equal-budget control ties on its stated advantage at matched current-task progress.
- Report prequential current-world loss and the targeted parent failure mode (C1 homogenization, C2 drift, C3 rare loss, C4 shared-write interference, C5 cascades). For every card, score each agent on the parent's fixed first-ten-task holdout before and after the 50-round test, report worst-agent and rare-task accuracy, and add the targeted old slice below. Keep unchanged old tasks separate from deliberately revised facts: scoring an obsolete answer as correct can reward staleness. Evaluate the ordinary live read, including any archive miss, delay, fallback or abstention, and report paired uncertainty across at least five seeds for non-enumerable trials. Test labels never enter learning or lease renewal.

## Literature check

Searched the Hugging Face Papers index for agent skill sharing with verification/provenance, cache revalidation, networked model collapse, and federated control variates. Checked arXiv abstracts for the linked papers and relevant full-text passages for SkillClaw (§2.2–2.3), Zep (§5.3–5.6), Federation over Harness (§3), networked self-consumption (§3–5), PPI++ (§2–6), verifier-based retraining (§2–4), and Rogers-style lossy transmission (§4–6). In particular, SkillClaw tests incumbent and candidate on the same deployed toolchain before writing, Zep already ranks versions by verified trials and may retire unused provisional skills, and PPI++ already corrects imputed losses using labelled residuals and tunes the amount of imputation. These are direct controls, not missing literature. The screen is targeted, not a priority claim.

## A. Leases on what was actually tested (#10)

### 01. Renew only the claims separated by the event
- **Mechanism:** Each reusable skill lists a small set of competing explanations of its success. Verification grants a scoped renewal only to claims on which those explanations predicted different observed outcomes. A successful composite tool call cannot renew a step that a fallback could have supplied.
- **Novelty vs nearest prior art:** [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) records version-level verified trials and separates trust from search weight. The proposed unit is an expiring distinction between explanations, not the version's maturity or a win counter.
- **Cheapest first test:** Enumerate a two-step workflow with a hidden fallback; compare version-trial weighting and item leases given the same truth draws, then remove the fallback as a null. C2/C5.
- **Old-task retention check:** Score unchanged old workflows that need the masked step, not just composite workflows where the fallback saves it.

### 02. Renew a premise without renewing its dependents
- **Mechanism:** Factor a reusable tactic into explicit premises and one applicability claim per composition. A fresh premise witness refreshes only that premise; a dependent use needs an unexpired applicability witness too. A revoked premise stops new downstream inheritance without deleting sibling skills.
- **Novelty vs nearest prior art:** [Gray–Cheriton cache leases](https://doi.org/10.1145/74850.74870) expire authority to use cached objects under server-mediated consistency, while [SkillClaw, 2604.08377](https://arxiv.org/abs/2604.08377) validates an evolved skill end to end. The bet is cheaper selective *evidence* renewal when the server cannot announce ground truth and composition can fail with all premises intact.
- **Cheapest first test:** Enumerate a diamond of Boolean prerequisites with one premise flip and one purely compositional failure; compare item leases and dependency invalidation with equal checks. C2/C4.
- **Old-task retention check:** Test both unchanged sibling paths and old callers that depend on the diamond's unaffected premise.

### 03. Lease a caller-to-caller translation
- **Mechanism:** When two agents have related tool contexts, require a bridge observation that checks an explicit context translation. Attach a separate lease to that translation so the source skill remains live after transfer eligibility expires.
- **Novelty vs nearest prior art:** [Collaborative Memory, 2505.18279](https://arxiv.org/abs/2505.18279) handles dynamic access across users; [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) filters by applicability. The extra object is empirical authority to transfer support between distinct callers, not permission or an asserted context tag.
- **Cheapest first test:** Two private toy tool schemas differ by an action permutation that sometimes changes. Compare per-site leases and static applicability tags; use a schema pair with no stable translation as the negative case. C2/C3.
- **Old-task retention check:** Old source tasks must stay live after destination revocation; score a rare destination caller separately.

### 04. Use a rare old case as a separating experiment
- **Mechanism:** Given a small hypothesis set, allocate one warranted audit to an existing rare task whose result distinguishes several renewal claims; grant scope only where identifiability follows. Prefer a shared separator to the item with the lowest remaining TTL.
- **Novelty vs nearest prior art:** [Who Pays for the Knowledge Models Copy?, 2611.06022](https://arxiv.org/abs/2611.06022) separates fidelity loss from staleness, and root #11 allocates reality by transmission weakness. The claim here is that renewal queries can be amortized by *which hypotheses an actual task separates*, not just risk-based prioritization.
- **Cheapest first test:** Enumerate binary truth tables with a one-query separator and an otherwise identical world lacking it; compare exact risk-greedy and exact per-item allocation. C2/C3.
- **Old-task retention check:** Score held-out variations of the rare separating task and rare items never selected.

### 05. Split a lease on a counterexample instead of evicting the whole skill
- **Mechanism:** On a verified failure, subtract the smallest supported caller region from the old lease, preserving the existing expiry elsewhere. Neither sibling support nor the act of splitting extends a deadline; unsampled regions remain unknown.
- **Novelty vs nearest prior art:** [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) uses applicability and lowers rank on verified failures; the proposed change is a scoped subtraction from existing read authority under an explicit region model. Ordinary contextual change detection is a control.
- **Cheapest first test:** Use a four-cell rule table with one changed corner, then a global change. Compare reset, per-cell changepoint detectors and item-maturity weighting. C2/C4.
- **Old-task retention check:** Check unchanged neighbours at ordinary traffic, including agents that receive the split late.

### 06. Archive with a one-use quarantine exit
- **Mechanism:** Expired rules remain readable for a shadow prediction but not for inheritance. One budgeted protected comparison can restore a lease if it tests exactly the requested scope; the archive answer alone must never trigger its own renewal.
- **Novelty vs nearest prior art:** [No-Regret Caching, 2101.12588](https://arxiv.org/abs/2101.12588) optimizes cache hit costs; [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) excludes retired versions from search. Here the paid transition turns archived content into a candidate for returning to the training distribution, decoupling archival recall from contagion.
- **Cheapest first test:** Plant one rare stable skill and one stale high-confidence skill; compare archive access with no reinstatement, unconditional reinstatement, and fresh reconstruction. C3/C5.
- **Old-task retention check:** Count the first rare call after expiration and its latency or abstention, not only the score after successful reinstatement.

### 07. Renew a fallback independently of the preferred skill
- **Mechanism:** Pin two separate claims: “primary is better” and “fallback clears the old service floor.” Test the latter by bypassing the primary on a logged subset; its lease can survive a primary revision without certifying the revision.
- **Novelty vs nearest prior art:** [SkillClaw, 2604.08377](https://arxiv.org/abs/2604.08377) runs incumbent–candidate comparisons; the proposed audit concerns the fallback's independent ability to sustain live old service after a distributional shift, not candidate ranking.
- **Cheapest first test:** Replay a tiny incumbent/candidate/fallback table in which the fallback is masked in ordinary traffic; compare paired candidate evaluation plus standard fallback testing at the same execution count. C3/C4.
- **Old-task retention check:** Score old requests routed after primary expiry and old requests whose service depended on the fallback even before the change.

### 08. Store the order of evidence, not the order of arrival
- **Mechanism:** Give each scoped claim a conservative bound on the time of the newest valid test and the time of the newest contradiction. Delayed positive witnesses cannot overturn a newer contradiction unless acquisition order is known; incomparable events leave that scope unknown pending adjudication.
- **Novelty vs nearest prior art:** [Gray–Cheriton leases](https://doi.org/10.1145/74850.74870) address distributed cache consistency; [Bayesian Online Changepoint Detection, 0710.3742](https://arxiv.org/abs/0710.3742) tracks run length over an ordered stream. The control to beat is an event-time changepoint filter plus a timestamped lease; only a smaller sound witness under partial ordering would count.
- **Cheapest first test:** Exhaustively permute delayed updates in a two-clock, one-flip world. Compare arrival order, fixed grace windows, and a buffered event-time baseline. Include clock error wider than the drift interval. C2/C5.
- **Old-task retention check:** Measure time-to-service and false revocations on unchanged rare items with systematically delayed certificates.

### 09. Renew on an observation nobody could have scripted
- **Mechanism:** Commit to a prediction and a mechanically randomized harmless branch before opening the verifier response. Only the component that predicted the branch's world outcome gets renewal; agreement among agents after opening contributes nothing.
- **Novelty vs nearest prior art:** [Dependence-aware truth discovery, 2611.04805](https://arxiv.org/abs/2611.04805) corrects agent agreement through decorrelation weights, whereas the proposal changes what observations count by requiring prospective discriminating outcomes. Ordinary randomized audit is conceded.
- **Cheapest first test:** Enumerate a toy service where an agent's default action forces a success flag, but a diagnostic branch exposes whether its predicted relation is right; compare standard random audits and verified version scoring. Include a branch that is not diagnostic. C2/C5.
- **Old-task retention check:** Separate old calls with forced-success traces from genuine old skills, including their first unforced call.

### 10. Admit a plan only if its leases cover the actual path
- **Mechanism:** Compute, at plan time, which clauses a future execution will read and whether their scopes and expiration windows cover that execution. If not, queue one targeted verification or choose a shorter lawful plan; refresh only clauses actually tested.
- **Novelty vs nearest prior art:** [EpiCon, 2609.37923](https://arxiv.org/abs/2609.37923) organizes shared experience for retrieval; [Gray–Cheriton leases](https://doi.org/10.1145/74850.74870) govern cached access. The bet is an advantage over ordinary lease-aware planning when a scope-specific proof cheaply discharges several future reads, not just checking minimum TTL.
- **Cheapest first test:** Enumerate a three-step planner whose routes share one diagnostic and compare exact read-time checking, conservative minimum TTL, and on-demand checks at equal R. Include unpredictable paths with no shared proof. C2/C3.
- **Old-task retention check:** Score long old workflows whose mid-plan clause expires, including whether fallback completes within the original deadline.

## B. Replace label subtraction with a testable estimator (#02)

For cards below, “residual” refers to a declared gradient or outcome target, not a proxy for semantic novelty. An exact design-based reference with verification indicator V and known probability p(x) > 0 is b(x) + V/p(x) · (g(y) − b(x)). Here b must be fixed before the verification decision conditional on the logged covariates/history, and the target under this expression is the gradient on the *logged input distribution*. Averaging over V gives g(y) under randomized verification; neither self-selected inputs nor verification with zero probability are repaired by this identity.

### 11. Pair draws at the source of the echo
- **Mechanism:** Include a deterministic local coupling ID so the receiver can reproduce exactly the stale teacher's pseudo-label for the known self-authored branch and cancel its realized contribution. Preserve an authenticated world residual on the same input when available.
- **Novelty vs nearest prior art:** [Networked self-consumption, 2610.09409](https://arxiv.org/abs/2610.09409) studies coupled model dynamics. Exact self cancellation alone is source dropping; the only claim here is preservation of verified information in a mixed update when source masks cannot be transmitted at equal bytes.
- **Cheapest first test:** Compare replayable coupling to exact source dropping with paid masks and to an independent synthetic draw on two asynchronous scalar regressors; include loss of the coupling ID. C2/C5.
- **Old-task retention check:** Score old examples whose true label matches the synthetic label, especially when the verifying observation would otherwise be dropped with it.

### 12. Rectify before a delayed write crosses a model version
- **Mechanism:** Locally form a verified residual at generation time, then carry only the sufficient statistic needed to evaluate that residual at applied time. Keep b and the verification probabilities tied to generation; score the residual using the current receiver, not a stale baseline submitted as a new posterior.
- **Novelty vs nearest prior art:** [PPI++, 2311.01453](https://arxiv.org/abs/2311.01453) combines imputation and rectification; [asynchronous federated optimization, 2206.10189](https://arxiv.org/abs/2206.10189) weights delayed updates. The question is whether a compact, receiver-evaluable residual preserves the target better than both frozen messages and recomputing the whole estimator.
- **Cheapest first test:** In softmax with finite feature types, enumerate a receiver that changes between send and apply. Compare stale gradient, bandwidth-matched sketch, and exact current recomputation; include a label-nonlinear loss where the proposed statistic is insufficient. C2/C4.
- **Old-task retention check:** Score the old task immediately after the late write and after its next normal update.

### 13. Use shared drift to pick an opposing residual coefficient
- **Mechanism:** Estimate the covariance of agents' residual messages on a disjoint probe window. Choose coefficients for controls of the form (V/p − 1) times a predecision prediction, using conditional propensities. Reduce variance of the legal aggregate, not just of each message; freeze coefficients before application.
- **Novelty vs nearest prior art:** [PPI++, 2311.01453](https://arxiv.org/abs/2311.01453) power-tunes imputation, and [SCAFFOLD, 1910.06378](https://arxiv.org/abs/1910.06378) uses control variates for client drift. The tentative contribution is codec-sized cross-agent controls targeted at the noise modes sustained by feedback; full covariance tuning is the ceiling.
- **Cheapest first test:** Four scalar agents share a noisy teacher mode. Compare per-agent tuning, aggregate covariance tuning without feedback awareness, and a common mode that changes sign midstream. C1/C2.
- **Old-task retention check:** Score old minority tasks aligned and anti-aligned with the controlled mode, not just mean gradients.

### 14. Measure residuals on the actions the model stopped taking
- **Mechanism:** In a finite task family, reserve some real actions from the original supported action set under logged randomization. Use verified action–outcome residuals to estimate the named reference gradient, including actions hidden by the current skill's policy.
- **Novelty vs nearest prior art:** [Doubly Robust Policy Evaluation and Learning, 1103.4601](https://arxiv.org/abs/1103.4601) already corrects contextual bandit estimates with reward models and propensities. Novelty would require using the shared artifact to maintain a small positive-support intervention design that outperforms standard exploration plus DR at equal R, not rediscovering DR.
- **Cheapest first test:** Two actions, two contexts, one policy-mediated disappearance; compare fresh mixing, fixed exploration plus DR and optimally allocated exploration on the tiny known family. In a zero-support null, require abstention. C2/C3.
- **Old-task retention check:** Old tasks solved only by the disappearing action must be sampled in the live service metric, not only in the intervention stream.

### 15. Pay once for a cluster-level correction
- **Mechanism:** If multiple private agents propose correlated copies of one event class, draw a logged cluster verification and send a weighted residual for the cluster mean. Require exchangeability within the declared cluster or random member selection with known probabilities; do not treat one convenient member as representative.
- **Novelty vs nearest prior art:** [Dependence-aware truth discovery, 2611.04805](https://arxiv.org/abs/2611.04805) estimates source dependence; [PPI, 2301.09633](https://arxiv.org/abs/2301.09633) uses labelled corrections. The question is whether cheap causal copy IDs enable cluster sampling that beats context-stratified rectification under feedback.
- **Cheapest first test:** One repeated lineage and one rare independent lineage; compare equal-R per-item sampling, cluster Horvitz–Thompson and full cluster stratification, then permute hidden outcomes within a purported cluster. C2/C5.
- **Old-task retention check:** Score users whose rare old case shares a signature with the dominant but differently labelled lineage.

### 16. Subtract a different version to detect bias, not to hide it
- **Mechanism:** Report paired fresh residuals against the generating teacher and the receiver on the same local records. The difference localizes shift due solely to the baseline choice; if it exceeds a pinned tolerance, use the receiver-compatible rectifier or defer rather than average the discrepancies away.
- **Novelty vs nearest prior art:** [Fine-tuning transfer, 2503.20110](https://arxiv.org/abs/2503.20110) ports weight differences across versions, and [2206.10189](https://arxiv.org/abs/2206.10189) models stale aggregation. The new claim to test is whether a tiny residual contrast reliably identifies which stale writes need re-evaluation before they cause forgetting.
- **Cheapest first test:** One version change shifts calibration, another changes a rare decision boundary. Compare age threshold, delta norm, and gradient cosine using the same reports. If the contrast can be computed from cheap unlabelled baseline predictions, give that control the win. C2/C4.
- **Old-task retention check:** Score stable old cases whose probabilities move but decisions do not, separately from cases whose decisions actually flip.

### 17. Separate verification noise from pseudo-label noise
- **Mechanism:** Take paired fresh observations on a small randomly selected subset to estimate verifier repeatability by stratum; tune the rectifier from the resulting noise split. Correct bias only in strata with an identified verifier error model; otherwise report uncertainty or withhold.
- **Novelty vs nearest prior art:** [Verifier-based retraining, 2510.16657](https://arxiv.org/abs/2510.16657) shows that biased verifiers pull linear retraining toward their own centre. The experiment asks when swapping some coverage for repeats is worthwhile for an online correction, not whether agreement implies accuracy.
- **Cheapest first test:** A four-cell classifier with independent noisy votes in two cells and common-mode bias in one; compare repeat allocation, one-vote verification and fixed reliability weights. C2/C3.
- **Old-task retention check:** Score old low-frequency cases exposed to noisy verification, and show that common-mode biased repeats do not count as independent old-task evidence.

### 18. Track echo energy along the modes that actually propagate
- **Mechanism:** Use a bounded sketch of parent-to-child write response to identify persistent network modes. Choose among predeclared unbiased write estimators for low projected variance in those modes; optimize cumulative effect, not raw single-step variance.
- **Novelty vs nearest prior art:** [Networked self-consumption, 2610.09409](https://arxiv.org/abs/2610.09409) characterizes stability and diversity, while [Dreaming Learning, 2610.30009](https://arxiv.org/abs/2610.30009) studies spectral loss of diversity in Markov retraining. The candidate is a test-time estimator choice that anticipates where its noise will travel, not a new stability law.
- **Cheapest first test:** Exact two-mode linear recursion with swapped innovation noise and an ablation where the response is isotropic. Compare minimum per-step variance and optimal fixed linear feedback filtering at equal state bytes. C1/C2.
- **Old-task retention check:** Score an old task aligned with the slow mode before and after the feedback loop, at matched one-step successor gain.

### 19. Measure a write's disagreement separately from its contraction
- **Mechanism:** Split a proposed update into a world-innovation estimate and an explicit, metered agreement term. Test agreement only at fixed innovation and compare to a matched-norm fresh update; deactivate agreement when it consumes a pinned local old-task budget.
- **Novelty vs nearest prior art:** [Deep Mutual Learning, 1706.00384](https://arxiv.org/abs/1706.00384) already combines supervised terms with peer matching. The diagnostic asks if a fleet can choose a bounded agreement term that preserves recoverability of distinct old skills, rather than calling the removal of useful contraction “debiasing.”
- **Cheapest first test:** Two linear agents with a shared mean and opposite private components. Compare DML, subtractive root #02 and a projection onto registered old directions that has identical norm. C1/C4.
- **Old-task retention check:** Report both agents' opposing old tasks before and after sharing, using each agent's deployed reader rather than a trained probe.

### 20. Compress the correction, not the trusted label
- **Mechanism:** Locally send a bounded, randomly rounded gradient residual relative to a predeclared baseline, plus the small statistic needed to scale it. Check that rounding error has zero mean conditional on the pre-send state; measure clipping bias separately.
- **Novelty vs nearest prior art:** [PPI++, 2311.01453](https://arxiv.org/abs/2311.01453) already rectifies imputation, and [QSGD, 1610.02132](https://arxiv.org/abs/1610.02132) already quantizes gradients with unbiased rounding. The question is whether verifiable local residuals compress better per retained task than QSGD on fresh gradients or ordinary gradient difference coding.
- **Cheapest first test:** A two-coordinate sparse residual host plus a misspecified baseline that makes corrections dense. Compare equal-bit fresh-gradient quantization, generic gradient difference coding and exact uncompressed rectification. C2/C4.
- **Old-task retention check:** Include an old task depending on the routinely small residual coordinate and another whose correction would saturate the code.

## C. Combine the seeds without counting the same observation twice

### 21. Bind a residual to the exact clause it renews
- **Mechanism:** One verified event may produce a gradient residual and a renewal receipt, but each output is valid only for its declared estimand or claim. A compatible gradient can be applied while a renewal is withheld; one witness never multiplies into several observations at downstream readers.
- **Novelty vs nearest prior art:** [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) tracks verified outcome per skill; [PPI, 2301.09633](https://arxiv.org/abs/2301.09633) rectifies from labelled outcomes. The joint receipt is worth keeping only if shared acquisition measurably beats separate equal-budget renewal and gradient allocation.
- **Cheapest first test:** Two scopes share one label that identifies only one clause; enumerate designs choosing which observable to buy. Compare joint receipt, independent stack and shared audit without scope. C2/C4.
- **Old-task retention check:** A residual benefitting a common new scope must not renew or overwrite a rare, untested old scope; score them separately.

### 22. Move a verification slot toward what the live policy forgot to observe
- **Mechanism:** Detect when a lease becomes untestable because the current write removed its distinguishing action from the natural stream. Exchange a scheduled renewal slot for a randomized intervention which restores positive support, and compute its propensity-corrected residual on the declared reference distribution.
- **Novelty vs nearest prior art:** [Rogers-style copying, 2611.06022](https://arxiv.org/abs/2611.06022) models endogenous knowledge supply; [DR, 1103.4601](https://arxiv.org/abs/1103.4601) handles logged action selection. The proposed trigger is loss of *support for a deadline-bound renewal claim*, rather than uncertainty or reward regret alone.
- **Cheapest first test:** Enumerate two policies with identical reward/validation counts but different ability to observe a rare old branch. Compare exact equal-R active allocation, joint lease-plus-DR with fixed exploration, and a branch with no lawful intervention. C2/C3.
- **Old-task retention check:** Score the hidden old branch on natural held-out traffic as well as on the standardized old-task suite; an unserved request is a failure.

### 23. Correct the selection created by lease expiry
- **Mechanism:** Randomly reserve some verification opportunities for expired scopes, logging their positive sampling probabilities. Estimate the shared gradient for the pinned target mix even after expiry suppresses ordinary accesses; a successful audit may separately re-enable inheritance.
- **Novelty vs nearest prior art:** [Sample-selection collapse, 2606.13732](https://arxiv.org/abs/2606.13732) shows that a verifier with fragmented support can bias retraining. [PPI++, 2311.01453](https://arxiv.org/abs/2311.01453) assumes compatible labelled and unlabelled covariates in its simplest setting; the bet is a joint admission/audit policy that avoids making its own correction blind.
- **Cheapest first test:** Four-cell deterministic switch stream with rare-but-stable expired scope; compare fixed stratified probing, inverse-propensity rectification without renewal, and the stacked components. Force a zero-audit stratum as a failure case. C2/C3.
- **Old-task retention check:** Score the expired stable slice at its ordinary old-task frequency and at a balanced frequency; expiry must not hide loss behind aggregate performance.

### 24. Separate the lifetime of a fact from the lifetime of a baseline
- **Mechanism:** Maintain independent clocks for world support and usefulness of the nuisance prediction b. A baseline can go stale and be replaced without revoking a verified fact; a current but unverified prediction can remain a control variate without permission to propagate as truth.
- **Novelty vs nearest prior art:** [Zep, 2611.01386](https://arxiv.org/abs/2611.01386) separates trust from search weight; [PPI++, 2311.01453](https://arxiv.org/abs/2311.01453) tunes prediction weight. This combines genuinely different grounds for reuse only if two clocks outperform an independent stacked trust gate and power tuner.
- **Cheapest first test:** Swap model calibration without changing the world in one arm and change the world at fixed model version in another. Compare one TTL, two thresholds, and an online fitted PPI coefficient. C2/C4.
- **Old-task retention check:** Stable old facts should survive a bad baseline swap; superseded answers should not survive just because the baseline remains useful on average.

### 25. Give reused corrections finite coverage rights
- **Mechanism:** Let one verification justify residual transport to a declared equivalence class of receivers only if the class's loss and feature map admit exact transport or a precommitted error bound. Retransmission stays useful but does not count as a second draw, add inverse-variance weight, or reset validity.
- **Novelty vs nearest prior art:** [Fine-tuning transfer, 2503.20110](https://arxiv.org/abs/2503.20110) transfers a trained delta across bases; [dependence-aware truth discovery, 2611.04805](https://arxiv.org/abs/2611.04805) discounts correlated reporters. The joint object is a claim about where a single *measurement* remains usable with its dependence unchanged.
- **Cheapest first test:** Enumerate three logistic agents, two related by known feature permutation and one missing a coordinate. Compare fresh local correction, naive delta port, and exact residual transport plus ordinary item leases. C3/C4.
- **Old-task retention check:** Score old probes that use the missing coordinate and old probes shared by the valid receiver pair.

### 26. Ask for a discriminating audit when correction and renewal disagree
- **Mechanism:** When a verified residual points against a live lease, compare predictions from three hypotheses: legitimate world drift, teacher calibration shift, or mismatch between action and applicability. Spend the next audit on the first observation that separates these hypotheses; otherwise retain a scoped unknown state rather than revoking globally.
- **Novelty vs nearest prior art:** [Bayesian Online Changepoint Detection, 0710.3742](https://arxiv.org/abs/0710.3742) detects parameter shifts, and [verifier-based retraining, 2510.16657](https://arxiv.org/abs/2510.16657) isolates the effect of verifier bias. The proposal uses competing world and artifact explanations to choose which evidence to acquire, against full joint Bayesian experimental design on the toy host.
- **Cheapest first test:** Find two worlds with identical first residual but opposite correct lease decisions; enumerate all one-audit choices and compare with a changepoint score plus largest-residual scheduling. Include a pair no affordable comparison can separate. C2/C4.
- **Old-task retention check:** Count false revocations on unchanged old tasks and late revocations on old interfaces whose world semantics changed, separately.

### 27. Coupon-test the fallback before removing the echo
- **Mechanism:** In a paired verification opportunity, compare the deployed echo-assisted skill to its intent-preserving fallback. Use the observed *incremental* outcome to decide whether to keep the lease for use, but apply the world residual to the declared reference write target whether or not the echo helped.
- **Novelty vs nearest prior art:** [SkillClaw, 2604.08377](https://arxiv.org/abs/2604.08377) already compares skill versions under the same environment; [DR, 1103.4601](https://arxiv.org/abs/1103.4601) distinguishes policy value from logged reward. The narrow claim is that explicitly separating use authority from write authority keeps beneficial borrowed behaviour without making it self-certifying.
- **Cheapest first test:** In an enumerable environment, interleave a helpful echoed shortcut and a self-confirming wrong one. Compare ordinary incumbent–candidate validation plus fresh-only writes, leases plus residuals independently, and equal-cost shadow comparison where it is valid. C3/C5.
- **Old-task retention check:** Score rare old shortcuts that genuinely help, and tasks harmed by the shortcut that are invisible if the system evaluates only successful runs.

## Deeper questions, ranked

1. **Can a shared skill carry a smaller, expiring proof of what the world actually distinguished?** Start with 01, 02 and 04. Seek the smallest transferable claim set that prevents false renewal while preserving rare old service. Require a separation from item leases, version trust and an exact equal-R scheduler using the same messages. A matched counterexample with no separating observation sets the impossibility boundary.
2. **Does any echo-cancelling write beat a correctly specified, equally cheap rectifier?** Start with 12, 13 and 18. On a networked linear host, derive bias and long-run variance under delay and feedback; compare to fresh-only, exact source dropping, PPI-style correction and a fixed linear optimal estimator. Graduate only if finite-byte transport or mode-aware estimation wins on deployed old service at matched current gain.
3. **Can checking a lease create the missing support needed to estimate a write?** Start with 22 and 23. Construct two worlds observationally indistinguishable under closed-loop exploitation and determine the least lawful intervention budget that both keeps old access live and identifies the gradient. Standard exploration plus stratified DR is the bar; no positive support means no claim.
4. **Which parts of a measurement can travel without manufacturing independence?** Combine 03, 21 and 25. Ask whether scoped transport and one shared receipt preserve more old skills than fresh per-agent verification or an independent stacked protocol at matched bandwidth. Include a receiver where transfer is invalid despite matching launch predictions.
