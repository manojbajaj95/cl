# Compute requests: pilots that need a real LLM or a GPU

These are the active or gated pilots from [idea-ledger.md](idea-ledger.md) whose answer is not valid on CPU toy models. GPU-h are rough single-A100 estimates and include seeds. Run them in order within each tier. A failed gate stops that pilot.

**Shared rules:**
1. Match budgets: equal tokens, rollouts, and training steps across arms.
2. Report 95% CIs over seeds.
3. When truth comes from rollouts, report its split-half reliability first and stop if it is < 0.7 (the G1 lesson).
4. Any effect mined from an earlier pilot must replicate at ≥ 10 seeds before it is modelled (the Q1 and P1 lessons).

**Not listed here, because CPU is valid:**
- B3, lesson interference proxy (CPU Qwen2.5-1.5B, already running)
- M2, per-lesson attention bias, with N1 as an arm
- N2, prohibition rebound
- Functional syndromes
- P3's synthetic replication, if kept small

**Every pilot that makes a lesson-value claim also runs a temperature-matched no-lesson arm** (T fit by entropy matching on source tasks only; see A3 in [PR #27](https://github.com/manojbajaj95/cl/pull/27)).

## Which tier-1 pilots can run on OpenRouter free models (about 50 requests/day)

Call counts assume about 3–5 calls per agent episode. Free endpoints generally don't return token log-probs, so any arm that needs log-probs still needs a local model.

| Pilot | Calls at full spec | Free tier? | Smallest version that fits |
|---|---|---|---|
| H1 gate only | ~3,400 with live episodes | **Yes, if shrunk** | Give each of 20 agents a synthesized memory (10 lessons from rare- or common-regime trajectories, ~20 calls), then elicit meta-predictions (20 agents × 10 lessons, ~200 calls). About 220 calls, about 5 days. Same r ≥ 0.2 gate |
| Toolbox drift | ~36,000 | No | 1 seed × 2 arms (tools vs lessons + tests) × 100 episodes is still ~600 calls (~12 days) and underpowered; use a GPU |
| Ask when stuck | ~13,500 | No | Needs the store-size sweep; use a GPU |
| P3 writer distractibility | ~4,000 | No | Needs ≥ 200 episodes per arm, and the mask arm needs log-probs |
| Fleet Q2 | — | Killed | [PR #25](https://github.com/manojbajaj95/cl/pull/25) |

## Tier 1: agent-loop pilots (need a 7B+ instruct model served with vLLM)

### Toolbox drift: tools fail loudly, lessons fail silently
- **Model:** Qwen2.5-Coder-7B-Instruct as the agent, in a synthetic tool world with 20 recurring procedures.
- **Arms:**
  1. Procedures stored as code tools.
  2. Procedures stored as text lessons.
  3. Text lessons plus the same regression tests (the strongest control).
  4. Text lessons without tests (reference).
- **Protocol:** 600 episodes. Drift 30% of APIs at episode 300 (rename, argument change, semantics change).
- **Measures:** episodes until drift is detected; episodes until success recovers to 90% of the pre-drift rate.
- **Seeds and compute:** 3 seeds, about 10 GPU-h.
- **Kill line:** dead if arm 3 matches arm 1 on both measures within the seed CI.

### Ask when stuck: failure-triggered pull memory
- **Model:** Qwen2.5-7B-Instruct on the 2610.27406 "more memory, worse agent" setup.
- **Arms:**
  1. Push top-k at the start.
  2. FLARE-style confidence-triggered retrieval.
  3. Pull of question-indexed atoms only on a failure signature (tool error or failed check).
- **Protocol:** store sizes {0, 10, 30, 100, 300}, with tokens matched per retrieval.
- **Seeds and compute:** 3 seeds, about 15 GPU-h.
- **Kill line:** dead if arm 3 declines with store size like arm 1, or arm 2 ties arm 3 at every size.

### H1: surprisingly-popular fleet memory (7B gate only)
The CPU run is killed ([PR #23](https://github.com/manojbajaj95/cl/pull/23)) and H1b is dropped: it tied mean P_i, which doesn't depend on model scale. The CPU meta-predictions were flat (r = 0.000), plausibly a small-model ability gap, so only the gate is requested.
- **Model:** 20 Qwen2.5-7B-Instruct agents, each running 50 episodes; a fraction p = 0.2 sees the rare regime.
- **Measure:** meta-prediction dependence on the agent's own experience only.
- **Seeds and compute:** 3 seeds, about 1 GPU-h.
- **Kill line:** stop if r < 0.2. If r ≥ 0.2, run the full arms from the original spec in the ledger (about 20 GPU-h): SP must be ≥ 10 points ahead on rare-regime tasks and the union must not tie.

### P3: writing is more distractible than acting
- **Model:** Qwen2.5-7B-Instruct as agent and memory writer, in the contamination task world from PR #4.
- **Arms:** one injected distractor in every arm, then:
  1. Plain writer.
  2. Length-matched filler.
  3. Same-token "write only about the task" instruction.
  4. Writer sees only its own action trace.
  5. Action-log-prob relevance mask.
- **Protocol:** ≥ 200 episodes per arm.
- **Seeds and compute:** 3 seeds, about 8 GPU-h.
- **Kill line:** dead if the gap between bad-write rate and solve accuracy vanishes against filler, or arm 4 matches arm 5.

### Fleet Q2: killed at the truth-reliability gate
Killed ([PR #25](https://github.com/manojbajaj95/cl/pull/25)): exact-truth split-half reliability was about 0, and 9 of 40 lessons flipped sign. This is task heterogeneity, not sampling noise, so it isn't requested at larger scale. Q3 is dead with it.

### HW1: DROPPED
Killed at the variance gate ([PR #32](https://github.com/manojbajaj95/cl/pull/32)).

### A3 replication: DROPPED
A3 was killed by the margin-vs-scale test ([PR #33](https://github.com/manojbajaj95/cl/pull/33)): 1.5B follows lessons under a weak prior, and the margin account is published.

## Tier 2: weight-training pilots (need a GPU for LoRA or model editing)

### Double dosing, multi-cycle: DROPPED
Falsified on CPU ([PR #30](https://github.com/manojbajaj95/cl/pull/30)): 0 of 50 runs showed growing oscillation, and R1's fold-in failed its gate. At this effect size, a 1.5B model has no particular reason to start oscillating.

### E1 consolidation predictor (with M3 and F1 arms): HELD, B3 gate failed ([PR #28](https://github.com/manojbajaj95/cl/pull/28)), not in the total
- **Model:** Qwen2.5-1.5B-Instruct, distilling 200 lessons, each into LoRA ranks {4, 16, 64}.
- **Predictors:**
  1. E1: the lesson's ΔW share in the LoRA span.
  2. M3: the query-variance index G.
  3. F1: context ΔW alignment versus weight forgetting, on lesson pairs.
- **Controls:**
  1. One-step distillation gradient projected onto the LoRA span (the strongest control).
  2. First-step loss drop.
  3. In-context effect size.
  4. Length.
  5. Off-target in-context KL.
- **Seeds and compute:** 600 LoRA runs, 2 seeds, about 30 GPU-h.
- **Kill lines:**
  - E1 is dead if it is not ≥ 0.15 ρ above the best control at every rank.
  - M3 is dead if it adds < 0.1 ρ.
  - F1 is dead if it trails gradient cosine by > 0.1 ρ.

### D1 lesson capacity law: HELD, B3 gate failed ([PR #28](https://github.com/manojbajaj95/cl/pull/28)), not in the total
- **Model:** Qwen2.5-1.5B-Instruct, with 5 lesson pools and N swept over {1, 2, 4, …, 128}.
- **Comparison:** predict each pool's accuracy peak N* from where ΔW rank saturates.
- **Controls:**
  1. Length-matched dilution pool.
  2. Embedding effective rank.
  3. Token count.
- **Seeds and compute:** 3 seeds, about 6 GPU-h. This is inference only, but long contexts make it slow on CPU.
- **C2 arm:** also read the lessons in parallel passes (PCED-style).
- **Kill line:** dead if ρ < 0.5, if embedding rank comes within 0.2, or if the dilution pool peaks at the same N. Also dead if the knee moves ≥ 2× under parallel reading, since capacity is then set by attention crowding.

### Edit-capacity law: killed at CPU scale
Killed at CPU scale ([PR #22](https://github.com/manojbajaj95/cl/pull/22)), so not requested: a fixed guess of N* tied the law. A GPU run is worth it only if N* is first shown to vary widely across settings.

### Self-contamination law, R = k·(α_D·τ − d)/α_S (PR #4)
- **Ranked the best remaining GPU bet** (odds of a frontier result low to moderate).
- **Stage 1 (about 5 GPU-h, inference only):** Qwen2.5-7B lesson writer on a coding stream. Vary verifier strength by running 10–100% of the unit tests, and measure α_D, α_S, d and τ on about 300 candidates per coverage level. Stage 1 is dead if no level gives R in [0.5, 2] with CI, or if τ doesn't exceed the defect rate from same-length filler.
- **Protocol:**
  1. Find a setting with R in [0.5, 2] (stage 1 above).
  2. Sweep k ∈ {1, 2, 4, 8}.
- **Controls:**
  1. A predictor that uses only the gate catch rate.
  2. Extrapolating the early defect share.
- **Seeds and compute:** 3 seeds, about 5 GPU-h for stage 1 plus about 25 GPU-h for the k-sweep, roughly 30 GPU-h in total.
- **Stage 2 kill line:** dead if the gate-precision-only predictor ties R, or onset AUC < 0.75.
- **Kill line:** dead if collapse onset doesn't switch near R = 1.

**Total:** about 75 GPU-h (plus about 20 if H1's gate passes). If budget is short, run Tier 1 first; it holds the ideas closest to a paper.
