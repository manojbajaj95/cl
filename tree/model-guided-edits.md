# Node: can a big model decide where and how to change a model's weights?

Question: can a big model look at a smaller model (or itself) and decide where and how to change its weights so it learns something new?

## Root cause

**Weights are not self-describing.** Whether an edit works, and what it breaks, depends on three things together: the weights W, the activation distribution that flows into them (key covariance C), and the downstream map that turns their output into behavior (Jacobian J). Current editors see W alone, or W plus loose summaries. So their choice of "where" is a prior over likely sites, not a prediction. The accept/reject verifier in the outer loop does the learning. That is why LLM editors tie random or black-box search at equal budget.

A second, deeper part: **"where" is mostly the wrong variable.** Once the edit operator uses the data (C), almost any site works. The decision that matters is which subspace of the input distribution the edit may touch, and that subspace comes from data, not from reading weights.

### Evidence from papers

| Paper | Finding |
|---|---|
| Self-WSP [2611.28833](https://arxiv.org/abs/2611.28833) | Qwen3.5-0.8B self-edits raise GSM8K from 11.8% to 62.2%, but "the model shows little understanding of the edits it makes", and random search with the same budget matches self-editing on GSM8K. |
| LLM repair without gradients [2611.25613](https://arxiv.org/abs/2611.25613) | Live LLM selection matches black-box search on SmolLM2 and Qwen2.5. On Pythia it gets 65.62% against 66.15% for a fixed projection. "Operator coverage accounted for recovery." |
| Weight-Space Reading (Poindexter, Nov 2026) | A 27B reader predicts the direction of subtle self-edits at 0.730 balanced accuracy. Yet on 40 edits that changed nothing (incl. 6 no-ops), readers predicted a change 53–88% of the time. There is no self-reading advantage, and a different-family model reads destructive edits as well as the target itself (0.594 vs 0.593). |
| Memorization on steroids? [2611.08070](https://arxiv.org/abs/2611.08070) | Zero-shot weight reading is local arithmetic at the input and output layers plus dataset priors, with no tracing through middle layers. Permuting labels breaks every semantic claim. |
| Hase et al. 2023 ([2301.04213](https://arxiv.org/abs/2301.04213)) | Causal-tracing localization does not predict which layer edits best. |
| Theoretical limits of parameter editing [2606.00570](https://arxiv.org/abs/2606.00570) (ICML 2026) | Localized edits spread along fragile low-variance directions, which causes global interference. A retrieval baseline beats every parameter editor. |

### CPU probe ([pilots/model-guided-edits/](../pilots/model-guided-edits/README.md))

Setup: a 4-hidden-layer MLP (width 128), 5 seeds × 20 new associations. Each association gets a rank-1 edit at every layer with two operators: O1 is min-norm, O2 is ROME-style and uses the retention key covariance. Five choosers pick the layer: random, weight-only (spectral norm), gradient saliency, causal trace, and oracle. Regret is in utility points ×100, where utility = efficacy − retention damage.

| Chooser | Regret, O1 (weights only) | Regret, O2 (data-aware) |
|---|---|---|
| Random layer | 16.71 | 0.38 |
| Weight-only (spectral norm) | 0 * | 0.08 |
| Gradient saliency | 8.60 | 0.18 |
| Causal trace | 16.15 | 0.40 |

- With the data-aware operator, a random layer is within 0.4 points of the oracle. Switching the operator changed the best layer on 99% [97, 100] of associations.
- \* The weight-only chooser always picked hidden layer 1. A function-preserving rescaling (output drift < 4e-15) moved its choice to hidden layer 2 on all 5 seeds. So any chooser that reads raw weights depends on the gauge (the arbitrary scaling of equivalent weights), not on what the network computes.
- Causal-trace score vs edit utility across layers: Spearman −0.12 [−0.22, 0.02] (O1) and +0.03 [−0.11, 0.21] (O2). This is a toy analogue of Hase et al.
- Limits: toy MLP, single non-accumulated edits, Gaussian neighbors too easy to separate arms on generalization. No LLM editor was run.

**Takeaway for the tree:** making the editor smarter about *where* has almost no headroom. The headroom is in giving the editor the forward information it lacks (C, J, data null space), or in models whose weights carry their own meaning.

## Raw ideas (no self-filtering)

Each entry gives the mechanism, why it is new, and the cheapest first test. Risks and likely prior art are noted for the reviewer.

1. **Weight debugger (W, C, J as text).** The editor gets a "debug symbol table" for each layer: top key-covariance eigen-directions, decoded through downstream Jacobians into the tokens or classes they move. *New:* WSP editors so far see W or summary statistics, never the forward context that decides an edit's effect. *First test:* rerun the Self-WSP loop on Qwen 0.5B with and without the symbol table; measure the gain over equal-budget random search. *Risk:* an ordinary interpretability dump could tie.
2. **Weight-edit world model (MPC in weight space).** Train a small simulator that predicts Δbehavior from (ΔW, layer stats) on thousands of random edits. The LLM plans edits inside the simulator and only verifies the top few for real. *New:* it splits editing into a learned physics model plus a planner, instead of one-shot reading. *First test:* toy MLP with 10k random rank-1 edits; does the simulator catch no-op edits (readers miss 53–88%) and halve real evaluations? *Risk:* it may be just a surrogate model for black-box optimization.
3. **Gauge-fixed canonical weights.** Before the editor reads them, map weights to a canonical form: neurons permuted and rescaled by activation statistics, attention heads sorted. Equal functions then always look the same. *New:* reading has never been made invariant to the symmetries that broke the probe's weight-only chooser. *First test:* weight-only chooser regret with and without canonicalization under random rescalings, in this probe. *Risk:* weight-space-learning work (NFN, GMN) treats symmetry for learned encoders, but not for LLM readers.
4. **Edits with falsifiable predictions.** Every proposed ΔW must come with predicted outputs on 20 held-out probes. The edit is accepted only if predicted ≈ actual. Calibration errors are fed back to the editor (in context, or as RL). *New:* it turns editing from search into hypothesis testing, which forces a real forward model. *First test:* Self-WSP logs; do edits whose predictions came true generalize better to the test set than edits that only passed the verifier?
5. **Advantage-over-random reward for editors.** RL-train the editor on reward = gain − gain of random search at the same budget. Only information beyond search is rewarded. *New:* it directly targets the failure that random search ties. *First test:* GRPO on a 0.5B editor of a toy MLP; measure bits saved versus random.
6. **Bits-of-prior meter.** A metric: how many bits about the right edit the editor's proposal distribution carries, measured as the log-ratio of evaluations that random search needs versus the editor at equal success. *New:* a common unit to compare every WSP paper. *First test:* compute it from published Self-WSP and 2611.25613 budgets. *Risk:* a measurement, not a method; its value is as a benchmark primitive.
7. **Reading SGD's diffs to learn edit idioms.** Show the big model 50 (task, SGD ΔW) pairs from one task family and ask it to write the 51st ΔW without data. *New:* it learns the edit operator from optimizer traces, so "how" comes from gradient descent's own grammar. *First test:* task family = linear-teacher remaps on an MLP; compare against the mean-ΔW and nearest-neighbor ΔW baselines.
8. **Self-describing weights (manifests at birth).** Train the model with an auxiliary head that maps each block's in/out weights to a text description of its feature. Later editors read the manifest, not raw numbers. *New:* the model is built to be edited, so reading becomes a lookup. *First test:* a toy MLP trained with a manifest head; editor regret with and without it.
9. **Edit address space (virtual memory for skills).** Reserve a writable key-addressed page in each block, with keys taken from the data null space. "Where" becomes a key lookup that the model computes itself; the editor writes only the value. *New:* address and content are separated in the architecture. *Risk:* close to GRACE / memory layers; the new part is that keys come from the null space C.
10. **Null-space cartography.** The big model gets a data-derived map of "free" directions (near-zero retention covariance) per layer and must place new skills there. It chooses among free subspaces by semantics. *New:* it combines AlphaEdit-style projection with semantic choice. *First test:* in the probe, do semantically chosen free subspaces beat random free subspaces? *Risk:* AlphaEdit might already cover the gain.
11. **Cross-model edit transport.** The big model finds where it stores a fact in its own weights. A representational alignment (stitching map) then transports that edit into the small model's coordinates. *New:* an edit is computed once in the teacher and moved, not re-derived. *First test:* two MLPs trained from different seeds with a learned linear stitch; transported edit efficacy vs a directly computed edit.
12. **Portability score as proof of understanding.** If an editor understands an edit, its *description* of the edit should recompile into a working edit on another seed of the same small model. *New:* it separates understanding from luck. *First test:* in the probe, describe an O2 edit in features, recompile on seed 2, and measure efficacy.
13. **Fuzzing co-evolution.** A second model searches for inputs where the edit breaks retention, and the editor must survive the fuzzer. *Risk:* overlaps P30 differential fuzzing (PR #39); new only if the fuzzer is fed C to target fragile low-variance directions (2606.00570).
14. **Editing in function space, compiled to weights.** The editor states the change as "for inputs like X, output Y; preserve Z". A compiler (O2 plus layer search) picks location and form. *New:* the probe shows location is an implementation detail; this makes it the compiler's job. *First test:* LLM-written specs vs LLM-written ΔW on the Self-WSP math task at equal budget.
15. **Frozen-editor vs drifting-editor self-improvement.** In Self-WSP the editor is the edited model. Compare a frozen editor snapshot, a co-evolving editor, and an editor that only improves its editing skill. *New:* it separates "the edit made the solver better" from "the edit made the editor better", the real recursive-self-improvement question. *First test:* replicate Self-WSP's continued runs with a frozen editor.
16. **Posterior edits.** The editor outputs a distribution over ΔW, applied as a weight-space ensemble or a sampled edit with uncertainty. Continual learning becomes a sequence of Bayesian updates written by the LLM. *First test:* toy MLP; is the editor's stated uncertainty calibrated against actual damage?
17. **Neural-functional eyes for an LLM editor.** A permutation-equivariant weight encoder (NFN/GMN style) turns each layer into tokens that the LLM reads instead of raw floats. *New:* it pairs learned weight encoders with language-model planning. *First test:* reading accuracy on the 2611.08070 protocol, raw text vs encoder tokens.
18. **Student points, teacher writes.** The small model reports where it is uncertain (per-layer Fisher, or the failing probes), and the big model writes edits only there. Reverses who decides "where". *First test:* in the probe, a Fisher-ranked chooser vs saliency under O1.
19. **Edit grammar from successful edits.** Mine many accepted WSP edits into a basis of reusable operators (direction removal, block scaling, row swap). New edits are short programs in that basis. *Risk:* overlaps P21 learned weight ISA; new only if the basis is mined from LLM edits, not designed.
20. **Activation-conditioned edits.** The editor writes rules of the form "if feature f > τ at layer l, add Δ", compiled into a gated rank-1 block. *Risk:* close to P22 hot-fix bytecode and GRACE.
21. **Edits as forward-only experiments at scale.** The editor proposes subspaces; millions of cheap forward A/B perturbations (zeroth-order, antithetic) inside each subspace estimate the update. The LLM only chooses the search space. *New:* it ties Manoj's forward-propagation idea to model-guided location. *First test:* in the probe, ES restricted to the LLM's chosen subspace vs full-space ES at equal forward passes.
22. **Edit triage by edit size.** The editor first predicts whether a lesson needs weights at all (retrieval beats editing in 2606.00570) or can be a single rank-1 write. *Risk:* an improvement; routing between context and weights is crowded.

## Deeper sub-questions, ranked by chance of a new primitive

1. **What forward information must an editor see for its choices to beat random search, and can a learned weight-edit simulator supply it?** This is the direct cure for the root cause, and the bits-of-prior meter (idea 6) gives a clean measurement. Ideas 1, 2, 4, 6.
2. **Can models be trained to be readable and writable, with gauge-fixed or self-describing weights, so editing becomes a lookup?** This designs the substrate instead of the editor, and the probe's gauge result shows the current substrate defeats readers. Ideas 3, 8, 9, 17.
3. **If location is an implementation detail, what is the right specification language for an edit, and can a compiler from spec to weights replace both SGD and WSP for single lessons?** Ideas 10, 14, 21.
4. **Can an editor become a continual learner of *how to edit*, accumulating idioms from SGD diffs and its own outcomes?** Ideas 5, 7, 15, 19.
5. **Can an edit computed in one model be transported to another, so the big model learns once and writes many times?** Ideas 11, 12.
