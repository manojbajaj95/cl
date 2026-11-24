# Reviewer verdicts: proposer batches 1–3 (PR #5) and the artifact-epidemic law (PR #4)

Bar: a new result at NeurIPS/ICLR level, not a study. Each idea was checked for prior art on alphaXiv and the Hugging Face papers API (2026-11-24). **PURSUE** = pilot now, **REVISE** = pilot only after the named fix, **KILL** = stop.

## Shortlist worth piloting

| # | Idea | Strongest control it must beat | First step |
|---|---|---|---|
| 1 | PR #4: reproduction-number law for agent lesson pools | A per-candidate gate-precision predictor (α_D/α_S alone) and extrapolation of the defect fraction at round 200 | ~30 GPU-h: find a model × domain × gate with a non-degenerate R in [0.5, 2], then sweep retrieval breadth k across R = 1 on one real stream. Spend the 200–400 GPU-h only if onset tracks R there |
| 2 | #11 testing effect (self-generated, verified QA replay) | Self-generated *raw-text* replay ([2605.26097](https://arxiv.org/abs/2605.26097), [SSR 2403.01244](https://arxiv.org/abs/2403.01244)) and teacher-written QA with the same questions, at equal tokens | A claim stands only if self-QA beats teacher-QA. Otherwise it is QA formatting, which is already known |
| 3 | #14 edit capacity law (REVISE) | The norm-feedback collapse predictor of [Norm Anchors 2602.02543](https://arxiv.org/abs/2602.02543) and the spectral account in [2601.11042](https://arxiv.org/abs/2601.11042) | Predict N* from key covariance *before editing* better than an edited-weight norm threshold does, across ≥3 models |

## Noether memory (#1) and keyed restore (#13): KILL

Rerun with a harder (nonlinear-teacher) task stream, in `pilots/noether_check.py`:
- **Ordinary SGD erases it.** Per step, discrete SGD drifts balancedness by η²(‖g_in‖² − ‖g_out‖²). In `pilots/div_check.py` at lr 0.05, one task moved d by 0.036–0.048 on average, about as much as its natural spread. After 3 tasks at lr 0.05, bits written at 3× the spread decode at chance (0.52), and SGD with momentum is at chance at every amplitude. The proposer's 99.6% comes from an easy linear-teacher task with small gradients. Finite-step symmetry breaking is also analysed in [2611.06718](https://arxiv.org/abs/2611.06718).
- **When it survives, a non-conserved channel mostly survives too.** At lr ≤ 0.002 (SGD) or ≤ 1e-4 (Adam/AdamW), the ‖w_in‖² channel keeps 0.97–1.00 at ≥1× spread, the same as d. d's only edge is at 0.3×: 0.81–1.00 against 0.70–0.81 for the control. At lr 0.01 and 0.3×, d (0.65) is *worse* than the control (0.77).
- **Adam lr 1e-3:** 0.82 at 3×, chance below.
- **Anyone can erase it.** A function-preserving rebalancing is one closed-form step (accuracy at or below chance in every run, function change ≤ 4e-6), and weight canonicalization in merging tools ([2511.12601](https://arxiv.org/abs/2511.12601)) does it as a side effect.
- **#13 adds nothing for CL.** The adapter bank has to travel with the model anyway, so the key can travel in it. What is left is fragile watermarking.

## Other ideas

| # | Verdict | Reason |
|---|---|---|
| 2 gauge preconditioning | KILL | For a homogeneous in/out pair, a unit's NTK contribution scales as c²A + B/c² (SGD) or cA' + B'/c (Adam), which is minimal near balance. Rescaling can make units *more* plastic, never stiffer. The only real knob is scale-invariant (LN/QK-norm) weights, which is the known effective-LR effect, and weight decay undoes it |
| 3 rational forgetting | REVISE (low) | Matching the exponent is close to Bayes-optimal by construction, so the monotone kill test will pass trivially. It must beat scale-free multi-timescale learners (Benna–Fusi cascades, mixtures of learning rates) that need no estimate of α |
| 4 decode training order | KILL | A study. That forgetting is not erasure is already shown ([spurious forgetting 2501.13453](https://arxiv.org/abs/2501.13453), [2610.08718](https://arxiv.org/abs/2610.08718)); recovering lineage from weights also exists (Model Tree Heritage Recovery, Horwitz et al. 2024) |
| 5 forgetting as EoS crossing | KILL | Incoherent: 2/η stability applies to the loss being descended. The old task's curvature has no dynamical role during new-task training. As a predictor it reduces to ½Δθᵀ H_old Δθ |
| 6 text Fisher for memories | KILL | [ACE 2510.04618](https://arxiv.org/abs/2510.04618) already addresses context collapse with delta updates. Append + retrieve is likely to match at equal tokens |
| 7 programmable half-life | REVISE (low) | Lifecycle-aware parametric memory with learned fade exists ([2611.25235](https://arxiv.org/abs/2611.25235)). "Expired" must also survive a cheap relearning attack, or it is suppression, not expiry |
| 8 Landauer budget | KILL | Erased-bit counts bound information loss but say nothing about accessibility. Making β → 1 changes the optimizer, a confound |
| 9 metamemory | KILL | For replay targeting, buffer items already have labels, so per-item loss is free. The science part is crowded ([2405.05904](https://arxiv.org/abs/2405.05904), [2610.08718](https://arxiv.org/abs/2610.08718), [2610.22381](https://arxiv.org/abs/2610.22381)) |
| 10 counter-gradient data | REVISE (low) | On images it reduces to dataset condensation. Under shuffling and Adam, cancellation only holds in expectation. Control: gradient-matched *selection* of real examples (GradMatch/CRAIG) at equal size |
| 12 residual skill bits | KILL | The bit count depends on the mask-search algorithm, and random nets already contain good subnetworks. Relearning savings already measure this |
| 15 memory shorthand | KILL (low) | A 1.5B model is unlikely to invent a shorthand that beats NL at equal tokens. Prompt compression and gisting cover the compression part |
| 16 forecast forgetting | KILL | First-order per-fact prediction was tested and found to fail beyond the validated region ([2609.32818](https://arxiv.org/abs/2609.32818)). Pre-training behaviour bounds exist ([FireGate 2611.11979](https://arxiv.org/abs/2611.11979)). Evaluating 5% of probes is a cheap control that is hard to beat |
| 17 iterated learning | REVISE (low) | Overlaps PR #4. Control: same-compute iterative refinement by one agent without generational resets |

## PR #4 artifact-epidemic law: novel enough to stage, not ready for 200–400 GPU-h

- **Novelty.** The closest work ([2610.27406](https://arxiv.org/abs/2610.27406), [skill misevolution 2608.12851](https://arxiv.org/abs/2608.12851), [SEABench 2609.35596](https://arxiv.org/abs/2609.35596), [Zombie Agents 2602.15654](https://arxiv.org/abs/2602.15654)) shows error reproduction and persistence. None gives a threshold measured before deployment. The branching-process math is standard, so the paper rests entirely on real-agent validation.
- **The simulator is not evidence.** It implements the branching process, so the R = 1 threshold is built in. The mean-field only fits conditioned on the round-200 state, which weakens the "measured before deployment" claim.
- **Both measured LLM regimes are degenerate.** With real units the self-gate rejects every defect (α_D = 0, so R = 0). With made-up units it rejects everything (α_S ≈ 0, so learning stops). No real setting with an intermediate R has been found, so the GPU test currently has nothing to predict.
- **Assumptions to test.** τ independent of how many defects are retrieved; uniform retrieval (similarity retrieval clusters defects); no deduplication or merging in the store.
- **Next step.** First the ~30 GPU-h measurement step (plan item 1), chosen to find intermediate R, for example with a weaker verifier or partially checkable domains. Then one cheap k-sweep stream that tests prediction 2. Scale only if the collapse onset tracks R with AUC ≥ 0.75 there and the gate-precision control does worse.

## Rolling review (three parallel proposers)

| Idea | Verdict | Strongest control | Smallest falsifying test |
|---|---|---|---|
| Functional syndromes (coded key→value checks, sparse damage decode) | PASS, narrowed to one linear memory layer (MEMIT-edited MLP). Weight ECC exists only for hardware faults ([2602.00076](https://arxiv.org/abs/2602.00076), [2611.02042](https://arxiv.org/abs/2611.02042)) | Raw (key, value) replay of m pairs plus re-editing, and a dense random-projection sketch with least-squares decoding, both at equal bytes | Fine-tune a MEMIT-edited GPT-2-XL and measure e_i = ΔW·k_i. Dead if the top 10% of facts hold less than ~80% of the damage energy |
| Functional sigma-delta low-bit updates | KILL | — | Combines error feedback ([2610.18139](https://arxiv.org/abs/2610.18139)) with subspace projection. It cannot beat full error feedback on protected drift, and its only gain is an O(r) debt buffer |
| Agent A1 memory inoculation (PR #7) | KILL | — | Amounts to few-shot skepticism exemplars, and inoculation prompting exists ([2606.30252](https://arxiv.org/abs/2606.30252)). A skeptic instruction plus correct-revision exemplars at equal tokens likely ties |
| Agent A2 Baldwin vs Lamarck | KILL | — | The Baldwinian arm is cross-episode meta-RL for LLM agents ([2602.04089](https://arxiv.org/abs/2602.04089), [2512.16848](https://arxiv.org/abs/2512.16848)). The crossover is the expected meta-learning vs memorization tradeoff |
| Agent A3 time-travel memory | KILL | — | Flat reacquisition holds by construction for a frozen pool with a selector. Forget-Me-Not and recurring-drift model pools exist, and a regime-keyed append-only log ties |
| Return-point adapters | KILL | — | Saving the states makes it a save/restore stack, so exactness is by construction. A stateful router ties |
| Plasticity reserve (Gramian write selection) | PASS | Optimization readiness ([2605.09044](https://arxiv.org/abs/2605.09044)) as the same chooser, plus effective rank and random choice among candidates | CPU MLP on Slowly-Changing Regression or Permuted-MNIST, 50 tasks, 8 equal-loss candidate writes per step. Dead if the Gramian score's Spearman correlation with next-task gain is not above readiness, or choosing by it does not beat random choice |
| Rare-event distillation (prefix splitting) | PASS, narrowed to rare mid-trajectory behaviors | Same-budget MOPD previous-student replay, uniform prefix replay, frequency-weighted prompt upsampling | ~0.5B model, behavior at ~1/1000 mid-rollout. Dead if no win beyond the seed CI |
| Sparse-write certificates | KILL | — | Structural rank is only an upper bound, dense patterns carry no information, and SVD/OGD is cheap |
| Agent B3 lesson-only interference (ΔW alignment) | PASS | Function-vector cosine; NLI; dilution control | 200 lesson pairs on CPU Qwen2.5-1.5B. Dead if not ≥ 0.15 Spearman above NLI and above FV cosine |
| Agent B2 vocabulary-grown skills | KILL | — | Prompt-pool CL plus ToolkenGPT; zero forgetting is the frozen-backbone property |
| Agent C2 memory-loop Lyapunov exponent | PASS | 20-step two-order divergence; seed-only noise floor | 8 designs, λ from 20 updates. Dead if not ≥ 0.3 Spearman above the cheap two-order control |
| Agent C1 inverse tool models | KILL | — | Same data as hindsight-relabelled forward SFT (AgentHER) |
| Agent D1 lesson capacity law | PASS, gated on B3's proxy surviving | Length-matched dilution; embedding rank | 5 pools. Dead if ρ < 0.5 or embedding rank within 0.2 |
| Agent D2 write-time poison detection | KILL | — | Trigger-specific poisons evade random-probe energy; TaskTracker/LatentTriad cover broad ones |
| Agent E1 consolidation predictor | PASS, gated on B3 | One-step distillation gradient projection onto the LoRA span | 200 lessons × 3 ranks |
| Agent E2 edge-of-chaos tuning | PASS, gated on C2 | Self-consistency tuning | 3 designs × 7 knob values. Dead if the peak misses λ = 0 by > 1 step |
| Agent F1 context→weight interference | KILL (fold into E1) | — | Gradient cosine is a cheap known predictor that dominates it |
| Cross-field 4 effect-class distillation | PASS, narrowed to syntax shifts | Canonicalized token KL; reward-only replay | API-migration stream, Pareto test |
| Cross-field 4 bounded-delay scheduling | KILL | — | O(η²) order effect; gradient accumulation ties |
| Agent G1 offline A/B of memory edits | PASS | Likelihood-gain (no IS) control; LLM judge; uplift model | 30 lessons vs fresh-rollout truth; check ESS first |
