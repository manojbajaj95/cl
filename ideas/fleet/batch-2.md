# Fleet-memory proposer batch 2

I read the ledger (PR #6, including the Fleet Q1 kill for bagging and the Fleet Q2 pass) and PR #7 batches 1–11 before each idea. Prior art was checked on alphaXiv on 2026-11-24.

## Q3. Forecast which lessons the *next* model will make obsolete, before it exists
**Claim.** Q2 measures obsolescence once M2 exists. A fleet operator has to decide earlier, for example which lessons to keep, rewrite, or bake into fine-tuning data for the next release. Hypothesis: within a model lineage, upgrades improve the same states repeatedly. Define the per-state upgrade direction as u_k(x) = log P_{k+1}(a\*|x) − log P_k(a\*|x) on logged states. Then u_k and u_{k+1} are positively correlated, because each new model fixes more of the same residual errors. If so, a lesson's alignment with the *last* upgrade, A(L) = cos(ℓ_{k+1}(L), u_k), forecasts obsolescence at step k+2 using only M_k and M_{k+1}. Lessons with high A(L) patch exactly what the lineage keeps learning. Lessons with low A(L) encode things the lineage does not learn on its own, which makes them durable and worth keeping or distilling into weights.
**Strongest control, and why it should fail.**
1. **Lift trend.** Extrapolate the lesson's own lift: predicted Δ at step k+2 = 2·ℓ̄_{k+1} − ℓ̄_k. This is the simplest same-input baseline and the most likely to tie. It sees only that the lesson's lift shrank, not *where* the lineage is improving. A lesson whose lift shrank for unrelated reasons (noise, or a shift in where the policy goes) gets the same forecast.
2. Current lift magnitude ℓ̄_{k+1}.
3. Q2's T(L) on M_{k+1}.
4. Base-model difficulty of the lesson's source states under M_{k+1}.

All controls use the same logs and the same scoring calls.
**Smallest falsifying test.**
- Setup: the G1 router world and lessons as in the Fleet Q2 protocol. Chain: Qwen2.5-0.5B → 1.5B → 3B-Instruct (same tokenizer, CPU, log-prob scoring only for the 3B).
- Step 0, the precondition: Spearman(u_0, u_1) over the 36 states. **Kill** if it is < 0.3, because then the lineage has no persistent direction.
- Step 1: forecast obsolescence at 3B from the 0.5B and 1.5B models only. Truth comes from 200 paired 3B rollouts per lesson; a lesson is obsolete if Δ_1.5B > 0 and Δ_3B ≤ 0.
- **Kill** if A(L)'s AUROC for obsolescence is < 0.65, or not ≥ 0.10 above the lift trend (control 1).
- **Kill** if fewer than 5 of the 40 lessons become obsolete at 3B, which leaves too few positives.
- Replicate on Qwen2-1.5B → Qwen2.5-1.5B → Qwen3-1.7B, reported only. That chain mixes family versions, so it tests whether the result holds beyond scale steps.
**Closest prior art.**
- Agent Behavior Maps (2610.30014) and Oyama et al. place models and agents as centred log-likelihood vectors on shared trajectories and show that prompt displacements roughly compose. They give the coordinates, but do not forecast per-memory obsolescence.
- Model ladders and task scaling laws (2412.04403), proxy-task emergence prediction (2412.07111) and anticipatory evaluation (2509.20645) forecast benchmark-level capability, not which stored lesson stops being needed.
- Memory portability (2609.05339), UpgradeBench (2608.20918) and no-universal-regression-signal (2608.13607) are all measured after the new model exists.
- Skills going stale (2611.22525) is about environment change, not model change.

I found no forward forecast of memory obsolescence from upgrade-direction persistence.
**Ledger check.** It depends on Q2 (it reuses Q2's lift quantities) but is a separate claim: Q2 can pass while Q3 fails its step-0 precondition. It is not policy-drift obsolescence (killed at proposal in PR #7), which is about the environment changing.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Write lessons to maximize worst-case lift across several models, so memory transfers to unseen models | Rosetta Memory 2606.07711 trains write/read operators with a minimum-gain curriculum across LLMs; PromptBridge 2512.01420; GroupDRO system-prompt selection 2608.04339 |
| LEEP-style poolability test: score agent A's log under B's model before pooling A's lessons into B | LEEP/transferability estimation (2002.12462) applied to memory; Agent Behavior Maps 2610.30014 already cross-scores agents on shared trajectories |
| Collaborative filtering on a lesson × agent lift matrix to route lessons to agents | The full matrix is cheap to compute exactly from logs (no rollouts), so imputation solves a problem that does not exist; routed CL 2610.38796 |
| Contrastive pooling: admit a lesson only if it raises the likelihood of other agents' successes and lowers that of their failures | Exactly G1's unweighted likelihood control (success minus failure) |
| Detect lucky lessons by replication across copies | Agreement-based, which is H1's territory; Lessons from Luck 2610.33029 already measures luck carried into lessons |
| Write-time filter during a staged rollout: old copies skip lessons where the new version already succeeds | Q2's score applied at write time; no separate claim |
| Q1 repaired with writer temperature or seed diversity as the control | Q1 was killed for exactly that tie, and I have no mechanism that beats it |
