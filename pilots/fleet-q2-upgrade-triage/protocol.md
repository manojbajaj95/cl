# Fleet Q2 protocol: predict which lessons a model upgrade makes obsolete

The reviewer's gates come from ledger row "Fleet Q2" (PR #6). Everything below is frozen before any model-2 scoring. This mirrors the G1 protocol (`pilots/g1-offline-ab/protocol.md`, PR #14) and reuses its world.

* **World.** The G1 router (PR #14, `pilots/g1-offline-ab/agent.py`): three checkpoints and 12 codes. The tool interface constrains the next token to A, B or C, and the action sets the next code. Utility is binary: success means at least 2 correct routes. Logits are normalized over the legal set at temperature 1 for both sampling and scoring, as in G1. All models run CPU `llama-cpp-python` Q4_K_M with one explicit chat template.
* **Upgrade (gating).** M1 = Qwen2.5-0.5B-Instruct → M2 = Qwen2.5-1.5B-Instruct. Their tokenizer files are identical, and the legal-token paths are identical on G1 prompts (1116/1116).
* **Replication (non-gating).** Qwen2-1.5B-Instruct → Qwen2.5-1.5B-Instruct, reported only.
* **Lessons (40, frozen before any M2 call).**
  * 20 are written by M1. M1 runs 300 no-memory episodes. For 20 failed episodes drawn at random, M1 makes one distill call in the PR #4 format: one sentence, shown the trace plus the verifier-correct action at each step. These are the compensation lessons the claim is about.
  * The other 20 are G1's frozen lessons: 7 helpful, 7 weak or neutral and 6 misleading, chosen at random by class.
  * One lesson goes into the system prompt at a time.
* **Probe logs (no lesson rollouts).** Use 60 M1 no-memory episodes and 60 M2 no-memory episodes, disjoint from the truth starts. They are capped at 60 so state coverage stays partial; report it. a\*(x) is the verifier-correct action at each logged state x, so M1's mistakes count too. At each logged state, compute:
  * ℓ₁(x) = log P_M1(a\*|x,L) − log P_M1(a\*|x)
  * ℓ₂(x) = log P_M2(a\*|x,L) − log P_M2(a\*|x)
  * u(x) = log P_M2(a\*|x) − log P_M1(a\*|x)
* **Primary predictor (frozen).** T(L) = Σ_x ŵ(x)·[P_M2(a\*|x,L) − P_M2(a\*|x)], where ŵ is M2's empirical no-memory state visitation in its 60 probe episodes. This is a first-order estimate of the change in success, weighted by where M2 actually goes. Sign: higher T means the lesson helps M2 more.
* **Mechanism diagnostics (reported, not gated).**
  * cos(ℓ₁, u) over states in the M1 log, and whether it separates obsolete lessons from still-useful ones.
  * The mean of ℓ₂ on states where u > 0, which measures whether a lesson overrides M2's improvements.
* **Controls (same logs and same scoring budget).**
  1. M2 zero-shot success on each lesson's source tasks. For M1-written lessons this is the source episodes' starts; for G1 lessons it is the starts whose checkpoint the lesson names. Predicted Δ = −success.
  2. Old-model likelihood gain: the mean ℓ₁ (the "reload everything" belief).
  3. Mechanism ablation: the unweighted mean ℓ₂ over the M1 log.
  4. A frozen M2 ordinal judge given the lesson and a summary of M2's behaviour log.
  5. Selective-maintenance replay (2611.22525): replay the lesson's source success on M2 and flag a conflict.
* **Truth.**
  * Per lesson, Δ_M2(L) = success(M2+L) − success(M2), from 200 paired M2 rollouts on common random starts. The no-lesson arm gets 200 rollouts on the same starts.
  * Δ_M1(L) is measured the same way.
  * A lesson is **obsolete** if Δ_M1 > 0 and Δ_M2 ≤ 0.
  * Exact expected success over all 27 action paths per start is reported as an oracle ceiling and a check, never as a predictor input.
  * Reliability: Spearman between the two 100-rollout halves of Δ_M2, Spearman–Brown corrected. Below 0.7 the run is uninformative, not killed; rerun with 400 rollouts.
* **Kill rules (on point estimates).**
  * Spearman(T, Δ_M2) < 0.5.
  * Spearman(T, Δ_M2) less than 0.15 above control 1.
  * Fewer than 15% of the 40 lessons (6 of 40) are obsolete or harmful on M2, i.e. Δ_M2 < 0 or obsolete: the phenomenon is too small to matter.
  * Also report T's margins over controls 2–5, and the 3 pp pruning check: keep the lessons with T > 0 versus reload-all, in a 5-lesson context on M2, at equal context.
* **Uncertainty.** Percentile 95% CIs from a joint bootstrap over probe episodes (rescoring all predictors), paired rollout slots and lessons. The judge is conditional on its one fixed summary.
* **Cost.** Scoring 40 lessons on both models over the 36-state table takes about 5–6 min on 4 threads. Rollouts from the filled table are negligible. Writer and judge calls add about 60 short generations.
