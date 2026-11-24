# Fleet Q3 protocol: forecast lesson obsolescence at the next model generation

The reviewer's verdict is PASS, low priority. Everything below is frozen before any generation-4 call.

* **Gate.** Run only after the Fleet Q2 pilot has shown that its lift truth is reliable (split-half ≥ 0.7). Otherwise Q3 is parked.
* **World and lessons.** As in `pilots/fleet-q2-upgrade-triage/protocol.md`: the G1 router, the same 40 frozen lessons, and constrained A/B/C actions normalized over the legal set. All four models run CPU `llama-cpp-python` Q4_K_M with one explicit chat template.
* **Lineage (4 generations, ~1.5B).** G1 Qwen1.5-1.8B-Chat → G2 Qwen2-1.5B-Instruct → G3 Qwen2.5-1.5B-Instruct → G4 Qwen3-1.7B (non-thinking).
* **Tokenizer check.** Before running, check that the legal-token paths match across all four (as in Q2's 1116/1116 check). Drop a generation whose A/B/C tokens differ rather than remapping them.
* **Quantities.** Probe states come from 60 no-memory episodes per generation (disjoint from the truth starts); a\* is the verifier-correct action. For each generation g:
  * ℓ_g(L, x) = log P_g(a\*|x,L) − log P_g(a\*|x)
  * u_g(x) = log P_{g+1}(a\*|x) − log P_g(a\*|x), computed for g = 1, 2
  * T_g(L) as in Q2, with G_g playing the role of M2
* **Precondition.** Spearman(u_1, u_2) over the probe states. **Dead if < 0.3.**
* **Predictor (fits on G1–G3 only, frozen).**
  * ū = (u_1 + u_2)/2
  * A(L) = cos(ℓ_G3(L), ū)
  * F(L) = T_G3(L)·(1 − max(0, A(L)))
  * F(L) is the forecast of Δ_G4(L): current benefit, discounted by how much the lesson patches what the lineage keeps learning.
* **Controls (same G1–G3 data).**
  1. **Own lift-trend extrapolation.** Least-squares line through T_G1, T_G2 and T_G3, evaluated at G4 (observational-scaling-law style).
  2. **Zero-shot success trend.** No-memory success on the lesson's source states, extrapolated linearly over G1–G3 to G4. Predicted Δ = −extrapolated success.
  3. Persistence: T_G3 alone.
* **Truth.** Δ_G4(L) = success(G4+L) − success(G4), from 200 paired G4 rollouts per lesson on common random starts. Reliability is the Spearman between the two 100-rollout halves, Spearman–Brown corrected; below 0.7, rerun with 400 rollouts. A lesson is **obsolete** if Δ_G3 > 0 and Δ_G4 ≤ 0; report how many there are.
* **Kill rules (on point estimates).**
  * Spearman(u_1, u_2) < 0.3.
  * Spearman(F, Δ_G4) less than 0.15 above control 1.
  * Also report the margins over controls 2 and 3, Spearman(u_2, u_3) as an after-the-fact check, and the AUROC for obsolescence.
* **Uncertainty.** As in Q2: a joint bootstrap over probe episodes (rescoring every predictor), paired rollout slots and lessons.
* **Cost.** About 6 minutes of lesson scoring per generation on 4 threads, so roughly 25 minutes in total. Rollouts from the filled table are negligible.
