# Idea ledger

Every idea the reviewer has judged, with its verdict, the reason, and (for survivors) the control it must beat and the pilot outcome. Full reasoning is in [batches-1-3-and-pr4.md](batches-1-3-and-pr4.md). One row per idea; update the row when a pilot result lands.

Status values:
- **PILOTING**: passed review, pilot running.
- **GATED on X**: passed review; launch only if pilot X survives.
- **KILLED**: stop.
- **KILLED (fix)**: dead as written; can be resubmitted with the named fix.
- **SURVIVED / FALSIFIED**: the pilot outcome. A FALSIFIED row ends with **What we learned**, a negative result proposers can build on.

## Survived review

| Idea | Source | Status | Strongest control | Smallest falsifying test | Pilot outcome |
|---|---|---|---|---|---|
| Self-contamination law R = k·(α_D·τ − d)/α_S | PR #4 | PILOTING | Gate-catch-rate-only predictor; extrapolating the early defect share | Find a setting with R in [0.5, 2] (~30 GPU-h), then sweep k ∈ {1,2,4,8} × 3 seeds. Dead if collapse onset doesn't switch near R = 1 | — |
| Self-quizzing replay (#11) | Batch 2 | FALSIFIED | Self-generated raw-text replay ([2605.26097](https://arxiv.org/abs/2605.26097)); teacher QA on the same questions, equal tokens | ~1B model, continued pretraining. Dead if self-QA ≤ teacher-QA on old-fact retention | Pilot killed it. Over 3 held-out seeds, self-QA retention was −1.39 pp vs teacher QA on the same questions (paired 95% CI −6.19 to +3.41) and −0.93 pp vs verified prose (−3.56 to +1.71). A style-matched teacher control also showed no advantage (−0.35 pp, CI −5.59 to +4.90). [PR #8](https://github.com/manojbajaj95/cl/pull/8). **What we learned:** who writes the replay doesn't matter (self vs teacher vs style-matched teacher all tie). QA-replay gains come from format and fact coverage, not self-generation. Don't propose generator-identity effects without a new mechanism |
| Edit-capacity law, narrowed to pre-edit N* prediction (#14) | Batch 3 | PILOTING | Weight-norm threshold fitted on the first 10% of edits ([2602.02543](https://arxiv.org/abs/2602.02543)) | MEMIT on GPT-2-XL and GPT-J, 3 batch sizes. Dead if the key-covariance prediction of N* doesn't beat the norm control | — |
| Functional syndromes (coded key→value checks), narrowed to one linear memory layer | Cross-field 1 | PILOTING | Same-byte raw (k, v) replay + re-edit; dense random-projection sketch with least squares | Measure e_i = ΔW·k_i after fine-tuning. Dead if the top 10% of facts hold less than ~80% of the damage energy | — |
| Plasticity reserve (Gramian write selection) | Cross-field 2 | PILOTING | Optimization readiness ([2605.09044](https://arxiv.org/abs/2605.09044)) as the chooser; effective rank; random choice | CPU MLP, 50 tasks, 8 equal-loss candidates per write. Dead if its Spearman correlation with next-task gain is not above readiness | — |
| Rare-event distillation (weighted prefix splitting), narrowed to rare mid-trajectory behaviors | Cross-field 3 | PILOTING | Same-budget MOPD replay toward the previous student ([2611.02746](https://arxiv.org/abs/2611.02746)); uniform prefix replay ([2607.04763](https://arxiv.org/abs/2607.04763)); prompt upsampling weighted by behavior frequency | ~0.5B model, an old behavior firing ~1/1000 mid-rollout, then a new domain. Dead if splitting doesn't beat the best control beyond the seed CI, or hurts common behaviors | — |
| Lesson-only interference prediction (−⟨ΔW_A, ΔW_B⟩), B3 | Agent 2 (PR #7) | PILOTING | Function-vector cosine ([2605.16591](https://arxiv.org/abs/2605.16591)); NLI; embedding cosine; length-matched irrelevant-lesson dilution control | CPU Qwen2.5-1.5B, 200 lesson pairs. Dead if Spearman is not ≥ 0.15 above NLI, doesn't beat FV cosine, or dilution explains most of the drop | — |
| Memory-loop Lyapunov exponent predicts order dependence (C2) | Agent 3 (PR #7) | PILOTING | 20-step two-order divergence; growth rate, edit rate, [2611.01304](https://arxiv.org/abs/2611.01304) convergence signals; seed-only noise floor | 8 designs × 3 seeds, λ from 20 updates vs. order dependence after 200 updates × 4 orders. Dead if not ≥ 0.3 Spearman above the 20-step two-order control, or perturbed ≈ seed-only divergence | — |
| Lesson capacity law: accuracy peak N* where stacked lesson ΔW rank saturates (D1) | Agent 4 (PR #7) | GATED on B3 | Length-matched dilution pool; embedding effective rank; token count | Reuse B3's proxy, 5 lesson pools, sweep N for N*. Dead if ρ < 0.5, embedding rank within 0.2, or the dilution pool peaks the same | — |
| Consolidation predictor: lesson's ΔW share in LoRA reachable span (E1) | Agent 5 (PR #7) | GATED on B3 | One-step distillation gradient projected onto the LoRA span; first-step loss drop; in-context effect size; length | 200 lessons, LoRA ranks {4, 16, 64}. Dead if not ≥ 0.15 ρ above the best control at every rank, or the gradient projection ties | — |
| Edge-of-chaos tuning: hold memory-loop λ at 0 (E2) | Agent 5 (PR #7) | GATED on C2 | Label-free tuning by self-consistency, memory growth rate, edit-acceptance rate; labelled grid search is the ceiling | 3 designs × 7 knob values × 3 seeds. Dead if the peak misses λ = 0 by more than one step in ≥ 2 designs, or self-consistency tuning is within the seed CI | — |

## Killed

| Idea | Source | Status | Why |
|---|---|---|---|
| Noether memory (#1) | Batch 1 | KILLED | Reviewer rerun: SGD at lr 0.05 and SGD with momentum erase the payload. A non-conserved channel survives about as well at low LR, and a one-step rebalance erases it |
| Gauge preconditioning (#2) | Batch 1 | KILLED | Rescaling only makes units more plastic. What remains is the known effective-LR effect |
| Rational (power-law) forgetting (#3) | Batch 1 | KILLED (fix) | Must beat multi-timescale learners (Benna–Fusi, mixtures of LRs) that need no estimate of α |
| Decode training order from weights (#4) | Batch 1 | KILLED | A study. Spurious forgetting and model lineage recovery already exist |
| Forgetting as an edge-of-stability crossing (#5) | Batch 1 | KILLED | Old-task curvature plays no part in new-task dynamics |
| Text Fisher for agent memories (#6) | Batch 1 | KILLED | ACE delta updates and append + retrieve cover it |
| Programmable half-life (#7) | Batch 2 | KILLED (fix) | [2611.25235](https://arxiv.org/abs/2611.25235) exists. Expiry must also survive a relearning attack |
| Landauer erasure budget (#8) | Batch 2 | KILLED | Counting erased bits says nothing about accessibility |
| Metamemory (#9) | Batch 2 | KILLED | Buffer loss is free, and the area is crowded ([2610.08718](https://arxiv.org/abs/2610.08718)) |
| Counter-gradient data (#10) | Batch 2 | KILLED (fix) | Must beat gradient-matched selection of real examples (GradMatch/CRAIG) |
| Residual skill bits (#12) | Batch 2 | KILLED | The count depends on the mask search, and relearning savings already measure this |
| Noether-keyed skill restore (#13) | Batch 3 | KILLED | Depends on Noether memory, and the key can travel with the adapter bank anyway |
| Private memory shorthand (#15) | Batch 3 | KILLED | Unlikely to beat natural language at equal tokens; prompt compression covers it |
| Forecast forgetting before an update (#16) | Batch 3 | KILLED | First-order forecasts fail ([2609.32818](https://arxiv.org/abs/2609.32818)); FireGate bounds behaviour change |
| Iterated learning for lessons (#17) | Batch 3 | KILLED (fix) | Must beat one agent refining at the same compute |
| Functional sigma-delta updates | Cross-field 1 | KILLED | Can't beat full error feedback; the only gain is an O(r) buffer |
| Return-point adapters | Cross-field 2 | KILLED | Saving the states makes it a save/restore stack, so exactness is by construction |
| Memory inoculation (A1) | Agent 1 (PR #7) | KILLED | Few-shot skepticism prompting; inoculation prompting exists ([2606.30252](https://arxiv.org/abs/2606.30252)) |
| Baldwin vs Lamarck (A2) | Agent 1 (PR #7) | KILLED | Cross-episode meta-RL for LLM agents exists ([2602.04089](https://arxiv.org/abs/2602.04089)) |
| Time-travel memory (A3) | Agent 1 (PR #7) | KILLED | Flat reacquisition holds by construction; Forget-Me-Not and recurring-drift model pools exist |
| Sparse-write certificates (graph matchings) | Cross-field 3 | KILLED | Structural rank only bounds true rank from above, so it can't certify that every edit harms. Dense Jacobian patterns carry no information. Masked-Jacobian SVD (OGD) is cheap; certified retention exists ([2610.40740](https://arxiv.org/abs/2610.40740)) |
| Vocabulary-grown skills (B2) | Agent 2 (PR #7) | KILLED | Frozen backbone + per-skill embeddings is prompt-pool CL (L2P/DualPrompt/CODA) plus ToolkenGPT/Toolken+. Zero forgetting is the frozen-backbone property; online macro mining only changes the token source |
| Inverse tool models for tool drift (C1) | Agent 3 (PR #7) | KILLED | Hindsight relabelling for LLM agents exists ([AgentHER 2603.21357](https://arxiv.org/abs/2603.21357)). The inverse model sees the same data as forward SFT on relabelled goals; drift is a new application, not a new mechanism |
| Write-time poison detection by off-domain ΔW energy (D2) | Agent 4 (PR #7) | KILLED | Targeted/sleeper poisons ([2605.15338](https://arxiv.org/abs/2605.15338)) fire only on triggers, so random off-domain probes miss them by construction. Broad injections are already caught by TaskTracker activation deltas and [LatentTriad 2611.05088](https://arxiv.org/abs/2611.05088) |
| Context interference predicts LoRA forgetting (F1) | Agent 6 (PR #7) | KILLED (fold into E1) | Its ceiling, distillation-gradient cosine, is cheap and is the established GEM/OGD forgetting predictor, so even a pass loses to a known method. Test the shared-geometry claim inside E1's pilot on the same lesson pairs |

## Patterns in the kills

- **Ties a simple baseline at equal budget:** replay, append + retrieve, save/restore. This is how PR #1 died.
- **True by construction:** exact restore, flat reacquisition, a threshold built into the simulator.
- **Already in 2026 papers:** found by alphaXiv but missed by the HF papers search.
