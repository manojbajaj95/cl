# Node: what must an editor see, beyond the weights, to beat random search?

Parent: [PR #49, model-guided edits](https://github.com/manojbajaj95/cl/pull/49) (`tree/model-guided-edits.md`), sub-question 1.

Question: what information beyond the weights (data statistics, a learned simulator of edit effects) must an editor see for its choices to beat random search at equal verification budget?

Ideation only. No experiments were run for this node.

## Root cause

**An editor beats random search only if it carries information about the verifier's answer that is cheaper to get than asking the verifier. Today no source of such information is valid where forgetting actually happens.**

Three parts:

1. **The effect of an edit is a property of (W, data, path), not of W.** What an edit does is fixed by the weights, the activation distribution of the inputs to keep (key covariance C), the downstream Jacobian J, and how C and J themselves move as the edit is applied. Weight-only editors see one of these four, in an arbitrary gauge (PR #49's probe: a function-preserving rescale flips a weight-only chooser).
2. **The simulators we have are local, and forgetting is not.** First-order response models predict per-fact margin changes at r = 0.974–0.998, yet fail to predict forgetting, because forgetting happens far outside the region where the linear model was checked ([2609.32818](https://arxiv.org/abs/2609.32818)). Their bound only certifies facts whose response coefficients drift less (R) than the fact's distance to the boundary (a). So the missing quantity is **response drift**: how the sensitivity of each protected behavior changes along the edit path. No editor, and no editing benchmark, exposes it.
3. **The learned predictors we have are per-run and aggregate.** TuneAhead ([2606.17660](https://arxiv.org/abs/2606.17660)) predicts a fine-tune's final score within ±3 pp from dataset descriptors plus a short probe run, but needs 1,300 runs and outputs one scalar. Meta Models ([2610.37001](https://arxiv.org/abs/2610.37001)) shows TabPFN on numeric training records matches fine-tuned LLM meta-models, which says the information is numeric, not textual. PreUnlearn ([2606.18473](https://arxiv.org/abs/2606.18473)) finds collateral damage is best predicted by *interaction* features between the forget set and the evaluation set, i.e. data geometry, before any update. Steering side effects are forecastable from unsteered representations, with magnitude set mostly by the target behavior ([2608.11227](https://arxiv.org/abs/2608.11227)). None of these is amortized over edits, per-probe, and valid at large edit sizes at once.

So the information an editor needs is: **(new-data × keep-data interaction geometry) + (response drift along the path) + (a calibrated uncertainty, so it knows when to ask the verifier).** Weights are nearly redundant once these are known (PR #49: with a data-aware operator a random layer is within 0.4 points of the oracle).

A sharper way to say why LLM editors tie random search (Self-WSP [2611.28833](https://arxiv.org/abs/2611.28833), [2611.25613](https://arxiv.org/abs/2611.25613)): the accept/reject verifier is the only component that sees data, so all the learning happens in the verifier loop, and the editor contributes a prior with near-zero bits. Any information the editor is given that the verifier also computes for free (loss on a probe set) adds nothing; only information that **predicts the verifier on inputs it has not been run on** counts.

### Evidence from papers

| Paper | Finding relevant to the root cause |
|---|---|
| When can first-order models bound forgetting? [2609.32818](https://arxiv.org/abs/2609.32818) | Linear response predicts margins (r ≈ 0.97–0.998) but not forgetting; a bound holds only where response drift R < margin distance a. |
| TuneAhead [2606.17660](https://arxiv.org/abs/2606.17660) | Static data descriptors + short probe predict fine-tune score (RMSE 1.47 pp on 370 held-out runs); aggregate, per-run, needs 1,300 runs. |
| Meta Models [2610.37001](https://arxiv.org/abs/2610.37001) | TabPFN on numeric training records ≥ fine-tuned LLM meta-model in seconds; learning response is a numeric modality. |
| PreUnlearn [2606.18473](https://arxiv.org/abs/2606.18473) | Pre-update collateral damage predicted best by forget-set × eval-set interaction features; damage decays with semantic distance but crosses domain boundaries. |
| Forecasting steering side effects [2608.11227](https://arxiv.org/abs/2608.11227) | 67-behavior cross-effect matrix; side effects structured, asymmetric, and forecastable from unsteered representations better than similarity heuristics. |
| REVIVE [2601.11042](https://arxiv.org/abs/2601.11042) | Sequential-edit collapse tracks disruption of dominant singular directions of pretrained weights; a weight-only statistic that matters only for accumulated edits. |
| AlphaEdit [2410.02355](https://arxiv.org/abs/2410.02355), BetaEdit [2605.09285](https://arxiv.org/abs/2605.09285), LOKI [2606.19679](https://arxiv.org/abs/2606.19679), FisherEdit [2610.25914](https://arxiv.org/abs/2610.25914) | The best editors already consume data statistics (null space of keep keys, Fisher); they are closed-form, not predictive, and do not model drift across sequential edits. |
| HiEdit [2604.11214](https://arxiv.org/abs/2604.11214) | RL layer selection gives +8.48% over RLEdit; consistent with "where" being a small lever. |
| Graph metanetworks for LMs [2610.18471](https://arxiv.org/abs/2610.18471), UWE [2610.21995](https://arxiv.org/abs/2610.21995) | Symmetry-aware weight encoders exist for transformers; they predict static properties (training corpus, fine-tune detection), not edit effects. |
| Sketched metadifferentiation [2609.15044](https://arxiv.org/abs/2609.15044), Datamodels [2202.00622](https://arxiv.org/abs/2202.00622) | Data→prediction influence matrices can be recovered from few measurements; the edit→prediction analogue has not been built. |

## Raw ideas (no self-filtering)

Each entry: mechanism, why new, cheapest first test (all include a retention check). Overlaps and likely ties are flagged for the reviewer. Ideas already in PR #49 (weight debugger, weight-edit world model / MPC, null-space cartography, neural-functional eyes) are not repeated; ideas below are the ones that answer *which* information and *how* it is supplied.

1. **Edit-response tensor (an influence matrix for edits).** Measure a small set of random edits and recover a low-rank tensor E[edit basis × probe × edit size] by compressed sensing (as SPELL/MAGE do for data). Any new edit's effect on any probe is then read off by projecting onto the basis. *New:* datamodels map data → predictions; this maps edits → predictions and includes edit size, so it carries the nonlinearity that first-order models miss. *First test:* GPT-2 small, MEMIT edits on CounterFact; fit E from 500 edits, predict per-probe retention for 200 held-out edits; compare rank correlation vs first-order finite-difference response. Retention check: neighborhood + unrelated-fact margins.

2. **Response-drift meter as the editor's input.** For each candidate edit, report R: the change in the protected probes' gradient (or margin sensitivity) between the start and an ε-step along the edit. The editor sees (predicted Δ, R, a) per probe and only proposes edits with R < a. *New:* turns the R term of the 2609.32818 bound from an a-posteriori certificate into a planning signal. *First test:* toy MLP from PR #49; editor = argmax predicted gain subject to R < a vs random; count verifier calls to reach a utility threshold. Retention: invariant probe set.

3. **Interaction-geometry token.** Give the editor one number per (new item, keep cluster): the cosine of their keys in the edited layer weighted by C⁻¹ (the ROME "leak" coefficient), plus the same in function space (NTK kernel entry). *New:* PreUnlearn shows interaction features predict damage for unlearning; nobody feeds them to an editor's proposal step. *First test:* rank 1,000 random MEMIT edits by the token; check Spearman with measured neighborhood damage vs a weight-norm control (the control that killed the capacity law).

4. **Counterfactual edit replay buffer (an editor's episodic memory).** Store every (edit, measured effect) the system has ever verified, across tasks. New proposals are scored by kernel regression over this buffer in a symmetry-invariant edit embedding. *New:* continual learning *of the editor's physics*, rather than of the model. *First test:* sequential editing with 1,000 edits; after each 100, test whether buffer-scored proposals need fewer verifier calls than random. Retention: earlier edits' efficacy.

5. **Edit TabPFN.** Treat (edit features, layer stats, probe features) → Δmargin as a tabular in-context task and use TabPFN with no training. *New:* Meta Models did this for training runs; edits are the cheaper, denser case. *First test:* 2,000 GPT-2 MEMIT edits; held-out R² for per-probe Δ vs a fitted MLP and vs first-order response. Retention: unrelated-fact margins.

6. **Simulator disagreement as the only signal shown.** The editor never sees predictions, only where an ensemble of simulators disagrees. It must propose edits that resolve the disagreement (active learning) or exploit agreement. *New:* makes the editor an experiment designer whose information is epistemic, which is what beats random search when the verifier is expensive. *First test:* toy MLP; ensemble of 5 small simulators; disagreement-guided vs random proposals; verifier calls to threshold. Risk: this is Bayesian optimization with an ensemble surrogate; new only if the edit embedding transfers across tasks.

7. **Shadow model (a small twin that is edited first).** Keep a distilled 10× smaller twin aligned to the big model by stitching maps. Edits are tried on the twin, the results transported back. The twin is the simulator. *New:* a simulator that is itself a model of the same function, not a regressor on edit features; it extrapolates to large edits because it is nonlinear in the same way. *First test:* Pythia-410M with Pythia-70M twin; does twin-ranked edit order agree with true order (Spearman) above random? Retention on both.

8. **Retention-shadow price.** Compute a Lagrange multiplier per keep cluster from a single constrained edit solve (how much retention loss one more unit of efficacy costs). The editor sees prices, not weights. *New:* economic dual of AlphaEdit's hard null space; tells the editor which clusters are cheap to sacrifice. *First test:* toy MLP; edits planned with prices vs uniform; utility at equal budget.

9. **Edit-effect sketches in the residual stream.** Pass a random projection of each keep probe's activations through the model once; store their sketch. Any edit's effect on all probes is estimated by applying the edit to the sketch only (Johnson–Lindenstrauss). *New:* a constant-cost simulator whose input is data statistics compressed once, not weights. *First test:* GPT-2; sketch dimension 64 vs 1,024; correlation of estimated vs true Δ on 1,000 probes. Retention: these probes are the retention set.

10. **Learned simulator trained only on the model's own past SGD steps.** Every SGD step the model has ever taken is a (ΔW, Δloss on batch) pair. Train a simulator on this log; it is free data. *New:* uses the training trajectory as the edit-effect dataset; no extra measurements. *First test:* log 10k steps of a small model's fine-tune; does the simulator predict effects of held-out *rank-1* edits better than chance? Retention: held-out tasks.

11. **Edit-effect contrastive pretraining for editors.** Pretrain the editor on pairs (edit, effect fingerprint) with a CLIP-style loss so that it embeds edits by what they do. Proposals are then made in effect space and decoded to ΔW. *New:* the editor's representation of an edit is functional by construction. *First test:* toy MLP; retrieval accuracy from effect to edit; editing gain over random at equal budget.

12. **Gradient-of-verifier as observation.** Give the editor the gradient of the verifier score with respect to each candidate's coefficients in a low-dimensional edit basis, computed by forward-mode on 16 probes. *New:* WSP editors receive scalar accept/reject; this gives them a vector of the same cost. *First test:* Self-WSP loop with scalar vs vector feedback on Qwen 0.5B; equal-budget gain over random. Risk: ties plain zeroth-order descent in that basis.

13. **Data-weighted gauge fixing.** Canonicalize weights by whitening each layer with its input covariance C^{1/2} and output Jacobian norms. In this gauge weight entries are proportional to effect. *New:* gauge fixing (PR #49 idea 3) used activation stats only for permutation; using C and J for scale makes raw-weight readers effect-aware. *First test:* rerun PR #49's weight-only chooser in this gauge; does the function-preserving rescale still flip it, and does regret fall?

14. **Edit-cost oracle via path integral.** Estimate retention damage by integrating the first-order response along the straight path in 4 steps (Riemann sum), not at the start. *New:* the cheapest way to include drift R; the editor sees a 4-step "simulated rollout". *First test:* 2609.32818's setting at small scale; does the 4-step estimate predict forgetting where the one-step one fails?

15. **Twin probes (keep-set mirror of each new item).** For each new fact, automatically generate the 20 keep-set inputs most likely to be damaged (nearest in C⁻¹-metric key space) and give them to the editor as must-pass tests. *New:* a data statistic produced on demand per edit, targeted at the edit, unlike fixed neighborhood sets. *First test:* CounterFact; damage on twin probes vs random neighbors predicts total damage on 10k unrelated facts.

16. **Simulator-in-the-loop RL for editors with advantage over random (merge with PR #49 idea 5).** Reward the editor for gain minus random-search gain, but evaluated inside the simulator with occasional real checks; the simulator is updated on the real checks. *New:* Dyna-style editor training; the editor's skill is to exploit the simulator, the simulator's job is to stay honest. *First test:* toy MLP; editors trained with and without simulator rollouts; real-verifier calls to threshold.

17. **Edit transfer coefficients between tasks.** Measure how an edit for task A changes the loss on tasks B..Z on a small panel, build the cross-effect matrix (like the 67-behavior steering matrix), factorize it, and use the factors to predict effects of edits for unseen tasks. *New:* steering cross-effects were measured; for weight edits they are not, and not used to plan. *First test:* 20 MEMIT edit families × 20 probe families on GPT-2; held-out family prediction.

18. **Self-simulation: the edited model predicts its own post-edit outputs.** Ask the model, with the edit described in context (spec in function space), to predict its outputs on probes after the edit. Use its predictions as the simulator. *New:* tests whether models have an internal model of their own learning; if they do, it is the cheapest simulator. *First test:* Qwen 1.5B; edits from known facts; compare its predicted vs actual post-edit answers on neighbors; retention probes included. Risk: Weight-Space Reading shows readers over-predict change.

19. **Edits with an explicit domain of validity.** Every edit carries a simulator-predicted region (in key space) where its effect is certain; outside it the edit is gated off. *New:* the simulator's uncertainty becomes part of the edit itself, so continual edits do not interact in unmodeled regions. *First test:* 500 sequential edits; gated vs ungated; retention on unrelated facts and efficacy.

20. **Information budget experiment (bits per verifier call).** Give editors different information sources (W only; W + C; W + C + J; + R; + simulator) and measure verifier calls to reach a target, giving an information-to-savings curve. *New:* turns the node's question into a measured exchange rate; nobody has priced each information source. *First test:* toy MLP, 5 seeds; the curve itself is the result. Retention in utility.

21. **Edit-effect hash table.** Hash edits by a locality-sensitive hash of their effect on a fixed random probe batch; edits with equal hashes are treated as equivalent, so the editor searches over effect classes, not ΔW. *New:* quotients the edit space by behavior, removing the redundancy that makes random search competitive. *First test:* count distinct effect classes among 10k random rank-1 edits; search over classes vs over raw edits.

22. **Adversarial simulator (worst-case effect predictor).** Train a simulator to predict the maximum damage over a family of inputs (a learned fuzzer that outputs the worst input). The editor sees worst-case, not average, effects. *New:* certifiable editing using a learned adversary; differs from PR #49 idea 13 because the fuzzer output is a prediction given before the edit. *First test:* toy MLP; worst-case predicted vs found by PGD on 200 edits.

23. **Data-free simulator from the model's generative prior.** Sample keep data from the model itself (self-generated probes) to estimate C and interaction features when the real keep data is gone. *New:* answers whether the needed data statistics can be recovered from weights + sampling, which would make "beyond the weights" free. *First test:* GPT-2; C from self-samples vs C from WikiText; edit retention with each.

24. **Temporal simulator for accumulated edits.** Model the drift of C and J as a function of the number and type of past edits, so the editor predicts the effect of edit k given edits 1..k−1. *New:* sequential collapse (REVIVE, capacity law) is described, not forecast per edit; this is a state-space model of the model. *First test:* MEMIT 2,000 sequential edits; predict per-edit retention from history vs a constant baseline (the control that killed N* in the ledger).

## Deeper sub-questions, ranked by chance of a new primitive

1. **Is there an amortized edit-response operator, an "influence matrix for edits" with edit size as an axis, that is valid where forgetting happens?** This is the object that the first-order models (2609.32818) lack. If it exists and is low rank, edits become queries against it, and planning replaces verification. Ideas 1, 5, 9, 14, 24.
2. **What is the exchange rate between each information source (C, J, interaction geometry, response drift R, simulator) and verifier calls?** A measured bits-per-call curve would settle whether editors can ever beat random search and which information to supply. Ideas 2, 3, 8, 20.
3. **Can the model simulate its own learning, either through a small shadow twin or by self-prediction, so the simulator comes for free with the model?** Ideas 7, 10, 18, 23.
4. **Can edit effects be quotiented into a finite set of behavior classes, so editors search in effect space instead of weight space?** Ideas 11, 17, 21.
5. **Can edits carry their own domain of validity, making the simulator's uncertainty a part of the stored edit for continual accumulation?** Ideas 19, 22, plus 6.
