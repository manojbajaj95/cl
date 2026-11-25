# Test-time weights IV: when a weight change must beat something that writes no weights

**Status:** Ideas only; no implementation, learner runs or GPU. **Parent:** [Test-time weights III](test-time-weights-3.md) ([PR #317](https://github.com/manojbajaj95/cl/pull/317)). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/idea-ledger.md). **Review seeds:** [Flood triage, rows 434–437](https://github.com/manojbajaj95/cl/blob/046ce92971d3e1a19026e21bcbfa778785999d76/reviews/flood-triage.md#L434-L437) ([PR #6](https://github.com/manojbajaj95/cl/pull/6)). The #317 row is 435 and keeps two ideas at score 3: [#13](test-time-weights-3.md#13-do-not-pick-the-rival-that-is-easiest-to-beat-p) pre-registers a cheaper no-write rival (for example a frozen model plus a receipt decoder) and withholds authority for the weight change if it never separates from that rival; [#18](test-time-weights-3.md#18-make-an-observation-only-switch-that-cannot-change-the-forecast-p) restores the predecessor's reporting path for ordinary requests while keeping the candidate's forecast and service decision. The other rows review other nodes.

## What might be new?

Both seeds replace a single question ("is the new weight better than the old weight?") with a question about **what the weight change is for**. #13 asks whether the gain needs weights at all: a decoder, a retrieval entry or a head refit may buy the same verdicts with zero old-task damage and trivial revocation. #18 asks whether the loss needs weights at all: if the candidate only made failures unreportable, restoring the meter is the cheap fix and rollback is the expensive one. The shared object proposed here is a **weightless shadow**: for each live write, the cheapest no-weight mechanism (decoder, retrieval, head, reporting switch) that a pre-registered contract says could explain the write's gain or its loss. A weight write keeps authority only on the cells where it is not encompassed by its shadow, and loses only the authority its shadow cannot replace. The new claims are (1) that the shadow can be built from the write itself and committed before exposure, so it is not the easiest rival chosen after the fact, and (2) that gain-side shadows (#13) and loss-side shadows (#18) must be compared on the same disputed cells, because a weight write can look necessary only because its cheaper rival was never observable.

## Literature check and test contract

alphaXiv searches (2026 test-time updating, parametric vs contextual memory, gated model adoption, performative/selective-label observability) and the Hugging Face papers API (fine-tuning vs retrieval, in-context vs weight editing, cascades) were run on 2026-11-25; abstracts and method sections of the closest hits were read. Deltas below are hypotheses, not exhaustive priority claims.

- **The question "weights or something cheaper?" is not new.** [Externalise the Memory](https://arxiv.org/abs/2610.30478) pre-registers a parametric-vs-contextual contrast on identical weights and finds retrieval adds +34 pp while the adapter adds nothing detectable once the buffer is attached; [Can Test-Time Memory Evolution Outperform Test-Time Training?](https://arxiv.org/abs/2610.32046) compares memory evolution against TTT; [Cortex](https://arxiv.org/abs/2610.20399) and [From Lookups to Lessons](https://arxiv.org/abs/2611.00450) distil context or retrieval into weights. [A Resource-Priced Ladder for Frozen EEG Trunks](https://arxiv.org/abs/2611.25315) is the closest operational prior: a gated ladder factory → Bayesian head → affine map → full fine-tune, priced by accuracy, fit time and label cost, with the head matching fine-tuning at ~23× lower fit time. These are offline comparisons or utility-priced gates; none ties a *particular live write's* authority to forecast evidence that separates it from a pre-committed cheaper rival.
- **Adoption gating against an incumbent is prior art.** [Evidence-Gated Research](https://arxiv.org/abs/2610.01751) freezes a challenger before evidence and adopts on an anytime-valid e-value against a moving incumbent; [Slice-Wise Non-Regression with Incumbent Fallback](https://arxiv.org/abs/2609.13714) certifies non-inferiority per slice and returns the exact incumbent when certification fails; [TTT Settlement](https://arxiv.org/abs/2610.05076) scores updates on independent text before commit; [Beyond Update Counts: A Control Map](https://arxiv.org/abs/2610.36109) evaluates acquisition, retention and locality separately. [Third Eye](https://arxiv.org/abs/2611.12988) asks whether a self-update stays useful after the next update. All compare candidate vs incumbent; the rival set never includes a *weightless shadow of the candidate*.
- **Forecast encompassing is the statistical floor.** Chong & Hendry (1986), [Harvey, Leybourne & Newbold (1998)](https://doi.org/10.1080/07350015.1998.10524753) and the [conditional predictive ability test](https://doi.org/10.1111/j.1468-0262.2006.00718.x) (Giacomini & White 2006) already ask whether one forecast adds information beyond another, unconditionally or per context. Any card that reduces to "run an encompassing test against a decoder" is an application, labelled I.
- **Observation vs treatment is prior art.** [Separable effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC8536652/) decomposes treatment components; [Algorithmic Censoring](https://dl.acm.org/doi/10.1145/3617694.3623247) restores feedback for groups that stop producing labels; [Performative Prediction with Selective Labels](https://arxiv.org/abs/2610.08272) bounds risk under selective observation; [Stabilizing Performative Feedback Loops with Minimal Model Deployments](https://arxiv.org/abs/2609.14065) limits deployments to stabilize the loop; Netflix's [Counterfactual Observability Framework](https://arxiv.org/abs/2609.22747) separates raw engagement from counterfactual measurement. Shadow/dark-launch deployment (run a model without acting on it) is standard engineering practice. A report-only fallback is new only if it changes which deployment right is revoked, not if it is just better logging.
- **Shared host and counts.** Reuse #317's host: finite tables first, then at most a tiny CPU classifier on scripted document-routing or parcel-service streams, with receipts in a format that can drift independently of consequences. Pin predecessor, candidate, **weightless shadow(s)**, claims, eligible contrast cells, reporting paths, cost per rung (bytes, latency, revocation cost, old-task damage) and expiry before exposure. Count arrivals, registered disagreements (candidate vs predecessor, candidate vs shadow, shadow vs predecessor), observation opportunities and labelled verdicts separately. No new live probes in candidate arms; a randomized exploration control pays for its actions and labels.
- **Strongest stacked control (merge-card rule).** Every card must beat the stack of: #317 #13 as written (one pre-registered cheap rival, three-way prequential selection) + #317 #18 as written (report-only fallback) + Settlement + slice-wise non-regression with incumbent fallback + an EGR-style anytime-valid adoption gate + the 2611.25315 utility-priced ladder, at matched bytes, scoring passes and exposure, or report the latency–harm frontier instead.
- **Retention is a constraint, not a training source.** Freeze old-task fixtures before edits (old formats, old consequence cells, old tasks that need receipts); score before, during and after provisional exposure, after demotion to a shadow and after removal, with the worst old slice shown separately. A weightless rung is not exempt: a decoder can break old-format tasks. All-abstain and all-shadow are not wins when they lose new-task service. **P** = candidate reusable primitive; **I** = improvement or audit.

## A. Make the weight change beat the cheapest thing that could replace it (#317 #13)

### 01. Grant authority by rung, not by write (P)
- **Mechanism:** Pre-register a ladder of rivals ordered by revocation cost and old-task risk: frozen model, receipt decoder, retrieval entry, output-head refit, adapter, full weights. A live write earns rung *k* only on the contrast cells where no rung below *k* encompasses its forecasts; elsewhere it is served at the lowest rung that ties it. One delta can therefore hold full-weight authority on one cell and decoder-level authority on another.
- **Novelty vs nearest prior art:** [2611.25315](https://arxiv.org/abs/2611.25315) gates escalation along a similar ladder by a utility that prices accuracy, fit time and labels, globally per session. The proposal makes the ladder per cell and per write, and the climbing evidence is forecast separation from the rung below, not a utility estimate.
- **Cheapest first test:** Enumerate a four-cell table: format drift only, consequence drift only, both, neither. Fit each rung exactly. Compare global utility-priced escalation and three-way prequential selection (#317 #13). Kill if per-cell rung authority never assigns different rungs to cells at equal bytes and harm.
- **Old-task retention check:** Score old-format and old-consequence fixtures under each rung assignment, including cells served at a lower rung than the write.

### 02. Let a write keep weights only where its shadow is encompassed (I)
- **Mechanism:** On each pre-registered cell, run a forecast-encompassing test of candidate against shadow: if the optimal combination puts zero weight on the candidate, the weight delta has no authority there. Report the combination weight as the write's per-cell necessity.
- **Novelty vs nearest prior art:** This is the [Harvey–Leybourne–Newbold](https://doi.org/10.1080/07350015.1998.10524753) encompassing test or the [Giacomini–White](https://doi.org/10.1111/j.1468-0262.2006.00718.x) conditional test applied to a live write; it is the statistical floor every other card here must beat, not a primitive.
- **Cheapest first test:** Hand-compute encompassing weights on the four-cell table with ten events per cell. Compare plain paired prequential loss and [EGR](https://arxiv.org/abs/2610.01751) adoption. Keep only as the required control if it changes no decision.
- **Old-task retention check:** Apply the same test on frozen old cells; a write that is encompassed there by the predecessor must not be granted authority on them.

### 03. Compile each write into its own weightless shadow before exposure (P)
- **Mechanism:** At commit time, build the shadow from the write itself: evaluate the delta's output change on a pinned intake sample and fit the cheapest weightless object that reproduces it (a logit-bias table keyed on receipt tokens, a retrieval entry holding the write's training examples, a head refit). Commit the shadow before any outcome is observed. The write's authority is its residual over its own shadow, not over an arbitrary rival someone picked.
- **Novelty vs nearest prior art:** [Cortex](https://arxiv.org/abs/2610.20399) and [From Lookups to Lessons](https://arxiv.org/abs/2611.00450) go the other way (context → weights). #317 #13 leaves the rival's choice to the designer, which permits choosing a weak rival. Deriving the strongest admissible rival from the delta and freezing it pre-exposure is the proposed primitive.
- **Cheapest first test:** Two writes with identical gains on a tiny classifier: one whose gain is a pure output-bias shift, one that changes a feature. The compiled shadow should absorb the first and not the second. Compare a designer-picked decoder rival and a head-refit rival. Kill if a generic head refit reaches the same verdict at equal bytes.
- **Old-task retention check:** Serve old fixtures through the shadow alone and through the write alone; the shadow must not be credited if it breaks old formats.

### 04. Write only the residual the shadow cannot carry (P)
- **Mechanism:** Fit the shadow first on the same receipts, then compute the weight update on the residual loss with the shadow attached, so the committed weight delta is orthogonal (in output space on the intake sample) to what a decoder could do. Weights change only for consequences the shadow cannot express.
- **Novelty vs nearest prior art:** Residual fitting is boosting; head-first then body is common in [online label-shift adaptation](https://arxiv.org/abs/2402.03545) and in 2611.25315's ladder. The new part is that the residual split is pinned before exposure and defines which part of the delta the settlement contract can revoke.
- **Cheapest first test:** Linear host with a two-dimensional output-bias subspace. Compare full update, head-then-body fine-tuning and residual-only update on old-task damage at equal new-cell gain. Kill if head-then-body ties.
- **Old-task retention check:** Measure old-task damage separately for the shadow component and the weight residual after a later, unrelated write.

### 05. Pick the rival blind, from pre-exposure traffic only (I)
- **Mechanism:** Choose among candidate shadows using only intake data available before exposure and a pre-registered rule (for example, the shadow with the smallest description length that reproduces the delta on intake). Forbid swapping rivals after outcomes arrive.
- **Novelty vs nearest prior art:** Pre-registration and frozen challengers are already in [EGR](https://arxiv.org/abs/2610.01751) and [2609.13714](https://arxiv.org/abs/2609.13714). This is the rival-side counterpart; it is an audit discipline, not a mechanism.
- **Cheapest first test:** Simulate post-hoc rival choice across five shadows and count false weight authorizations versus blind choice on null tables. Keep as a required protocol if the gap is large.
- **Old-task retention check:** Include old cells in the intake sample used for choosing the rival.

### 06. Make the write name the cells where its shadow must fail (P)
- **Mechanism:** Require each write to forecast, before exposure, a set of intake contexts where the decoder shadow and the candidate disagree on a consequence (not a format). The write's weight authority is settled only on these cells; if they never arrive, it holds shadow-level authority only.
- **Novelty vs nearest prior art:** [#313 #01](test-time-weights-2.md#01-make-a-write-predict-how-it-would-lose-p) settles on predecessor disagreements; #317 #17 registers intake disagreement cells. The change is that the disagreement partner is the weightless shadow, so the claim is specifically "this needs weights".
- **Cheapest first test:** Cross receipt-format drift with consequence drift; make the consequence cells rare (1:20). Compare predecessor-only disagreement settlement plus a separate decoder gate. Kill if that stack grants the same authority at equal exposure.
- **Old-task retention check:** Old consequence cells that the predecessor handled and the shadow cannot represent must be scored after any weight grant.

### 07. Charge the write the old-task damage its shadow never pays (I)
- **Mechanism:** Pin the shadow's old-task damage (zero for a decoder that only reads new receipts) and require the weight write to beat it on new cells at the same old-task tolerance, using the write's measured damage on frozen fixtures as a cost in the settlement score.
- **Novelty vs nearest prior art:** Slice-wise non-regression ([2609.13714](https://arxiv.org/abs/2609.13714)) and Control Map locality ([2610.36109](https://arxiv.org/abs/2610.36109)) already score unrelated behaviour. This only reprices the comparison against the shadow.
- **Cheapest first test:** Tabulate gain and damage for full write, shadow and the residual write (card 04). Keep only if it changes a deployment decision versus non-regression gating alone.
- **Old-task retention check:** Worst old slice under each arm, reported beside new-cell gain.

### 08. Claim durability, not just accuracy, for weight authority (P)
- **Mechanism:** The advantage weights could have over a retrieval or decoder shadow is generalization to future keys the shadow will not match (paraphrases, new receipt variants). Make the weight write pre-register a durability forecast: a class of future contexts where the shadow misses and the write still predicts. Grant weight authority only when natural traffic from that class settles it.
- **Novelty vs nearest prior art:** [Third Eye](https://arxiv.org/abs/2611.12988) tests whether a self-update survives the next update; [Externalise the Memory](https://arxiv.org/abs/2610.30478) finds retrieval beats distilled weights on situation-specific corrections. The proposal turns "weights generalize beyond retrieval keys" into a falsifiable per-write claim with its own settlement cells.
- **Cheapest first test:** Retrieval shadow keyed on exact receipt strings versus a tiny classifier write; introduce paraphrased receipts after the write. Compare a fixed consolidation threshold. Kill if the write never wins a durability cell or if retrieval with a fuzzy key ties.
- **Old-task retention check:** Old tasks with paraphrased inputs, scored before and after the durability verdict.

### 09. Consolidate when the shadow's running cost crosses the write's damage (I)
- **Mechanism:** A weightless shadow costs memory and latency that grow with traffic; a weight write costs old-task damage and revocation risk once. Promote a shadow into weights only when its pinned running cost exceeds the write's measured damage plus revocation cost.
- **Novelty vs nearest prior art:** Consolidation from context to weights is [Cortex](https://arxiv.org/abs/2610.20399); cost-aware escalation is [2611.25315](https://arxiv.org/abs/2611.25315) and [cascade deferral](https://arxiv.org/abs/2307.02764). This is a scheduling rule.
- **Cheapest first test:** Closed-form costs on a stream with growing retrieval store. Keep only if it beats a fixed store-size trigger on old-task damage.
- **Old-task retention check:** Old tasks before and after each promotion.

### 10. Beat the stacked shadow, not each shadow alone (I; audit)
- **Mechanism:** The rival for a weight write is the best combination of all cheaper rungs (decoder + retrieval + head), fitted on the same receipts at the same bytes. A write that beats each separately but not their combination gets no weight authority.
- **Novelty vs nearest prior art:** This is the ledger's merge-card rule applied to rivals; forecast combination is classical.
- **Cheapest first test:** Construct a table where decoder covers format drift and retrieval covers one rare cell; the write beats each, not the stack. Every primitive in this node must report this control.
- **Old-task retention check:** The stacked shadow's own old-task damage, which can exceed any single rung's.

### 11. Let the shadow learn at the write's rate (P)
- **Mechanism:** A frozen shadow becomes an easy rival as traffic drifts. Allow the shadow to be refit on the same receipts the write sees, under the same commit rules, so separation measures what only weights can do now, not what a stale decoder failed to track.
- **Novelty vs nearest prior art:** EGR's moving incumbent ([2610.01751](https://arxiv.org/abs/2610.01751)) updates the incumbent after adoption; here the cheap rival co-adapts continuously, and the write's authority can be withdrawn when an updated shadow catches up.
- **Cheapest first test:** Slowly drifting receipt format; compare frozen shadow vs co-adapting shadow on false weight authorizations. Kill if periodic re-fitting of a frozen shadow at the same bytes ties.
- **Old-task retention check:** Old-format tasks after the shadow has been refit many times.

### 12. Demote a write to its shadow instead of reverting it (P)
- **Mechanism:** When a write loses separation from its shadow, revert the weights but keep serving its shadow, so the encompassed part of the benefit survives at near-zero old-task risk. Only a loss against the predecessor removes the shadow too.
- **Novelty vs nearest prior art:** [Owned Edits](https://arxiv.org/abs/2611.15917) supports scoped withdrawal and [SPIBB](https://arxiv.org/abs/1712.06924) backs off to a baseline. Neither has an intermediate state that keeps the cheap part of a revoked weight change.
- **Cheapest first test:** Two-rung table where the write's gain is 80% format and 20% consequence; the consequence part then turns harmful. Compare full rollback and slice-wise incumbent fallback. Kill if fallback per slice keeps the same service.
- **Old-task retention check:** Old tasks under the demoted state, including those that depended on the reverted weights.

### 13. Treat an encompassed write as a diagnosis of the drift (P)
- **Mechanism:** Use the pattern of which rung encompasses a write on which cells as a label for the drift itself (format, prior, feature, consequence). Route later writes on the same cells straight to that rung unless their own disagreement cells say otherwise.
- **Novelty vs nearest prior art:** Shift-type diagnosis exists (label vs covariate shift tests); 2611.25315 notes severity does not follow one ordinal ladder across datasets. The proposal is to reuse the per-write rung verdict as the diagnosis, with no separate shift detector.
- **Cheapest first test:** Three drift types in sequence; compare a label-shift test plus covariate detector routing. Kill if the generic detectors pick the same rungs.
- **Old-task retention check:** Old tasks on cells routed to a lower rung by an earlier diagnosis.

## B. Repair the meter before the model (#317 #18)

### 14. Compare rollback with a report-only fallback on the same silence (P)
- **Mechanism:** When a write's disputed cells go silent, run two pre-registered fallbacks on disjoint pinned cohorts: full rollback (treatment and reporting) and report-only fallback (#317 #18). If report-only restores outcomes that confirm the candidate, the silence was observability loss, and the write keeps authority; if confirmed outcomes are bad, it was harm.
- **Novelty vs nearest prior art:** [Separable effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC8536652/) decompose treatment components analytically. The proposal uses two mechanically restricted fallbacks as a live diagnosis of why a write's falsifiers vanished, which #317 #18 alone (one fallback) cannot tell apart from a reporting effect on outcomes.
- **Cheapest first test:** Enumerate three worlds with equal silence: reporting lost, real harm, both. Compare #317 #18 alone, [Algorithmic Censoring](https://dl.acm.org/doi/10.1145/3617694.3623247)-style exploration at equal exposure. Kill if exploration identifies the world equally fast.
- **Old-task retention check:** Old tasks in both fallback cohorts, including those whose service depends on receipt timing.

### 15. Switch reporting only on cells where candidate and shadow disagree (P)
- **Mechanism:** Restrict the report-only fallback to the pre-registered disagreement cells between the write and its weightless shadow (card 06), so the reporting overhead is spent only where a receipt could decide whether weights are needed.
- **Novelty vs nearest prior art:** Disagreement-targeted label acquisition is [online active learning](https://arxiv.org/abs/1904.09056); here the "query" is restoring an existing report path without changing treatment, and the targeting is by rung disagreement.
- **Cheapest first test:** Fixed reporting budget; compare uniform report-only fallback, predecessor-disagreement targeting and shadow-disagreement targeting. Kill if predecessor-disagreement targeting ties at equal overhead.
- **Old-task retention check:** Old cells outside the targeted set, which receive no extra reporting.

### 16. Seal the forecast before the meter changes (P)
- **Mechanism:** Commit the candidate's and the shadow's forecasts for every request in the switched cohort before the reporting switch flips, and log the hash. A switch decision that could depend on forecast content (choosing which requests to observe) voids the cohort.
- **Novelty vs nearest prior art:** Pre-registration of forecasts is standard in forecasting competitions; the narrower point is that a report-only switch is itself a selection lever and must be blind to the forecasts it settles.
- **Cheapest first test:** Simulate a switch operator who sees forecasts and selects favourable cases; count spurious confirmations vs a blind operator. Keep as protocol if non-trivial.
- **Old-task retention check:** Old cases in switched and unswitched cohorts.

### 17. Detect a reporting path that secretly treats (I; audit)
- **Mechanism:** Before using the switch, run a placebo flip on cells where candidate and predecessor agree. Any outcome change there means reporting changes treatment and the switch grants no permission (#317 #18's non-diagnostic case).
- **Novelty vs nearest prior art:** A negative-control outcome test ([Negative Controls](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/)); an audit, not a primitive.
- **Cheapest first test:** Ticket table where delivery of a receipt causes a follow-up service. The placebo flip must catch it. Required control for cards 14–20.
- **Old-task retention check:** Old tasks that depend on receiving a receipt, under placebo flips.

### 18. Price reporting debt and revoke only the right it funded (P)
- **Mechanism:** Every report-only fallback adds overhead to the write's account. The write's authority stays while its reporting debt per settled verdict is below a pinned rate; above it, only the observability-dependent right (keeping the weights on silent cells) lapses, not the predictive right on cells that still report.
- **Novelty vs nearest prior art:** #317 #15 separates predictive and acting rights; [SPIBB](https://arxiv.org/abs/1712.06924) restricts deviation where data are scarce. The new object is a reporting cost tied to a specific right of a specific write.
- **Cheapest first test:** Two writes with equal accuracy, one needing 5× more restored reporting to settle. Compare a global reporting budget. Kill if the global budget gives the same scopes.
- **Old-task retention check:** Old-task latency and correctness as reporting overhead grows.

### 19. Let the shadow serve while the meter is restored (P)
- **Mechanism:** During a report-only fallback on a silent cell, serve that cell from the write's weightless shadow, not from the weights, so the switch window carries no fresh weight-attributable harm. Settle the weight claim afterwards from the restored receipts of the shadow-vs-weight disagreement it logged in shadow mode.
- **Novelty vs nearest prior art:** Shadow deployment (run without acting) is standard practice. The combination — serving the cheap rival while the expensive one runs in shadow and the meter is repaired — is a specific three-way arrangement neither #317 #13 nor #18 contains.
- **Cheapest first test:** Silent harmful cell vs silent harmless cell. Compare rollback during the window and keeping the write during the window. Kill if rollback-plus-shadow-logging of the write ties on harm and time-to-verdict.
- **Old-task retention check:** Old tasks served by the shadow during the window.

### 20. Charge the observation switch to the rival comparison it serves (I)
- **Mechanism:** When reporting is restored to settle candidate-vs-shadow (not candidate-vs-predecessor), charge the overhead to the weight-necessity claim; a weight write whose necessity costs more reporting than its benefit stays at shadow rung.
- **Novelty vs nearest prior art:** Value-of-information measurement; an accounting rule built on cards 01 and 18.
- **Cheapest first test:** Closed-form value of information on the four-cell table. Keep only if it changes a rung decision.
- **Old-task retention check:** As card 18.

## C. Gain-side and loss-side shadows on the same cells

### 21. Ask whether a weight write is needed only because its rival was unobservable (P)
- **Mechanism:** A weight write can seem to beat a decoder shadow only because the decoder's failures were reported and the write's were not. Before granting weight authority, restore reporting symmetrically (report-only switch on both arms' disagreement cells) and re-run the encompassing comparison.
- **Novelty vs nearest prior art:** [Performative Prediction with Selective Labels](https://arxiv.org/abs/2610.08272) bounds selectively observed risk for one model. The proposal targets the asymmetric case where observability differs between two rivals and the asymmetry is what grants the expensive one authority.
- **Cheapest first test:** Construct a table where the weight write hides its own failures and the decoder does not; encompassing alone grants weights, symmetric reporting does not. Compare worst-case bounds (#317 #19) per arm. Kill if per-arm bounds give the same decision.
- **Old-task retention check:** Old cells under both arms with complete evaluator labels.

### 22. Split one observation budget between rival separation and self-falsification (P)
- **Mechanism:** A write needs receipts for two questions: is it better than the predecessor, and is it better than its shadow. Allocate a fixed reporting budget across the two, prioritizing whichever verdict is closer to changing the write's rung.
- **Novelty vs nearest prior art:** Evidence routing toward unresolved components is in [EGR](https://arxiv.org/abs/2610.01751). This routes between two rivals of one write, where the answers grant different rights.
- **Cheapest first test:** Enumerate budgets of 4, 8, 16 restored reports; compare EGR-style routing across cells but one rival. Kill if single-rival routing reaches the same rungs.
- **Old-task retention check:** Old cells excluded from the budget.

### 23. Test the weight write after the shadow has been adopted (P)
- **Mechanism:** Once a decoder shadow is adopted for format drift, the residual separation of a weight write must be re-measured on top of it, not inherited from the verdict against the bare predecessor. Order of adoption becomes explicit: shadow first, weights only on the residual.
- **Novelty vs nearest prior art:** [Control Map](https://arxiv.org/abs/2610.36109) shows update order changes results; [#317 #25](test-time-weights-3.md#25-require-a-finding-that-could-undo-a-second-write-without-touching-the-first-p) handles a second write. Here the first adopted object is weightless and the second is the weight write.
- **Cheapest first test:** Base, shadow, write, shadow+write on a four-cell table; the write's gain vanishes on top of the shadow. Kill if full-composite scoring catches it with no ordering rule.
- **Old-task retention check:** Old tasks under shadow alone and shadow+write.

### 24. Keep the shadow honest on the old task (I)
- **Mechanism:** A decoder shadow is not damage-free if old tasks share the receipt channel; score the shadow on frozen old fixtures before letting it encompass anything.
- **Novelty vs nearest prior art:** Locality checks are standard (Control Map). An audit that prevents the shadow from winning by construction.
- **Cheapest first test:** Old-format receipts collide with the new format; the decoder breaks them. Required in every card.
- **Old-task retention check:** This card is the check.

### 25. Write into the meter, not the model (P)
- **Mechanism:** For writes whose only measured effect is on how outcomes are reported (a parser fix, a receipt remapping), store the change as a reporting-path edit under #317 #18's switch rather than as weights or a decoder on predictions. Weight authority is then reserved for changes in predicted consequences.
- **Novelty vs nearest prior art:** Label-noise correction and annotator models learn the reporting channel; the proposal is to route a live write's content to the reporting layer by its settlement pattern, so reporting fixes cannot masquerade as learning.
- **Cheapest first test:** Write whose gain is entirely a receipt remap; compare a decoder shadow on predictions and a label-noise transition matrix. Kill if the transition matrix gives the same decisions.
- **Old-task retention check:** Old tasks that use the original receipt mapping.

### 26. Build twin worlds where format drift and consequence drift look the same (I; audit)
- **Mechanism:** Two worlds with identical arrivals, actions, visible receipts and silences; in one the gain is format-only (shadow suffices), in the other consequence (weights needed), differing only on unreported cells. Any method must give both the same rung until one ordinary separating receipt arrives.
- **Novelty vs nearest prior art:** Distinguishability fixtures as in #317 #26 and [partial identification](https://arxiv.org/abs/2204.11318).
- **Cheapest first test:** Two six-row tables; reject any method that assigns different rungs from identical inputs.
- **Old-task retention check:** One old task in the unreported cohort.

### 27. Break the switch and require every method to notice (I; audit)
- **Mechanism:** Make the report-only switch change service on a hidden slice; every card from B and C must then withhold any permission derived from the switched cohort.
- **Novelty vs nearest prior art:** #317 #18's own falsifier, made a shared fixture.
- **Cheapest first test:** Ticket table from card 17 with the side effect active only on disputed cells.
- **Old-task retention check:** Old tasks on the hidden slice.

## Ranked deeper questions

1. **Can a write be compiled into a weightless shadow strong enough that beating it means the change truly needs weights?** Start with 03, 06 and 10, with 02 as the floor and 26 as the audit. Require a win over the stacked shadow and over 2611.25315's utility-priced ladder at matched bytes and old-task tolerance. If a head refit always ties the compiled shadow, the shadow adds nothing beyond the ladder.
2. **When a write's falsifiers go silent, can a report-only fallback tell lost observability from harm faster than rollback or exploration?** Test 14 with 17 and 27 as controls, then 19. Stop if exploration at equal exposure identifies the world as fast, or if no host has a reporting path independent of treatment.
3. **Does weight authority ever survive symmetric observability?** Test 21 with 15: grant weights only after both the write and its shadow are observed on their disagreement cells. A null here would say test-time weight writes in this host win only by hiding their failures.
4. **What, if anything, do weights buy over a co-adapting shadow?** Test 08 and 11 together: durability to future keys is the only advantage left once the shadow learns at the same rate. Stop if fuzzy retrieval ties on paraphrase cells.
