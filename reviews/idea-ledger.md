# Idea ledger

Every idea the reviewer has judged, with its verdict, the reason, and (for survivors) the control it must beat and the pilot outcome. Full reasoning is in [batches-1-3-and-pr4.md](batches-1-3-and-pr4.md). One row per idea; update the row when a pilot result lands.

Status values:
- **PILOTING**: passed review, pilot running.
- **KILLED**: stop.
- **KILLED (fix)**: dead as written; can be resubmitted with the named fix.
- **SURVIVED / FALSIFIED**: the pilot outcome.

## Survived review

| Idea | Source | Status | Strongest control | Smallest falsifying test | Pilot outcome |
|---|---|---|---|---|---|
| Self-contamination law R = k·(α_D·τ − d)/α_S | PR #4 | PILOTING | Gate-catch-rate-only predictor; extrapolating the early defect share | Find a setting with R in [0.5, 2] (~30 GPU-h), then sweep k ∈ {1,2,4,8} × 3 seeds. Dead if collapse onset doesn't switch near R = 1 | — |
| Self-quizzing replay (#11) | Batch 2 | PILOTING | Self-generated raw-text replay ([2605.26097](https://arxiv.org/abs/2605.26097)); teacher QA on the same questions, equal tokens | ~1B model, continued pretraining. Dead if self-QA ≤ teacher-QA on old-fact retention | — |
| Edit-capacity law, narrowed to pre-edit N* prediction (#14) | Batch 3 | PILOTING | Weight-norm threshold fitted on the first 10% of edits ([2602.02543](https://arxiv.org/abs/2602.02543)) | MEMIT on GPT-2-XL and GPT-J, 3 batch sizes. Dead if the key-covariance prediction of N* doesn't beat the norm control | — |
| Functional syndromes (coded key→value checks), narrowed to one linear memory layer | Cross-field 1 | PILOTING | Same-byte raw (k, v) replay + re-edit; dense random-projection sketch with least squares | Measure e_i = ΔW·k_i after fine-tuning. Dead if the top 10% of facts hold less than ~80% of the damage energy | — |
| Plasticity reserve (Gramian write selection) | Cross-field 2 | PILOTING | Optimization readiness ([2605.09044](https://arxiv.org/abs/2605.09044)) as the chooser; effective rank; random choice | CPU MLP, 50 tasks, 8 equal-loss candidates per write. Dead if its Spearman correlation with next-task gain is not above readiness | — |

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

## Patterns in the kills

- **Ties a simple baseline at equal budget:** replay, append + retrieve, save/restore. This is how PR #1 died.
- **True by construction:** exact restore, flat reacquisition, a threshold built into the simulator.
- **Already in 2026 papers:** found by alphaXiv but missed by the HF papers search.
