# Artifact epidemics: a reproduction-number law for agents that learn from deployment

**Claim.** A deployed agent that writes lessons, skills or memories from its own episodes and retrieves them
later is a branching process over artifacts. The pool contaminates itself iff

\[ R = k\,\frac{\alpha_D\,\tau - d}{\alpha_S} > 1 \]

with k = artifacts retrieved per episode, τ = probability that a defective artifact in context makes the new
artifact defective, α_D / α_S = the admission gate's pass rates for defective / sound candidates, and
d = per-retrieval probability that a defect is exposed and removed. Below 1 the defective fraction stays at
≈ ε α_D / (α_S (1 − R)); above 1 it grows as N^{R−1} with pool size N, until retrieved defects cost more than sound
artifacts help. Each quantity is measurable with a planted-defect challenge trial. The law gives three falsifiable
predictions:

1. **Gate odds, not gate strictness.** Only α_D/α_S enters R. A stricter gate that scales both rates
   leaves R unchanged and only slows learning down.
2. **Retrieval breadth is a contagion dial.** Raising k (a common lever for improving accuracy) multiplies R.
3. **Deleting the source is not enough above threshold.** Once R > 1, descendants carry the defect forward.
   Only removal along the provenance graph (tracing contacts) reduces R; rolling back the root artifact does not.

## Why this is new

| Closest work | What it shows | What it lacks |
| --- | --- | --- |
| [Pre-commit gating vs skill contamination (2608.05810)](https://arxiv.org/abs/2608.05810), [anytime-valid self-evolution (2607.00871)](https://arxiv.org/abs/2607.00871) | Gates admit fewer bad updates | No pool dynamics: a gate that scores well per candidate can still have R > 1 |
| [More Memory, Worse Agents (2610.27406)](https://arxiv.org/abs/2610.27406), [Memory reward inflation (2608.00017)](https://arxiv.org/abs/2608.00017), [continual internalization collapse (2606.04703)](https://arxiv.org/abs/2606.04703) | Accumulated experience can hurt; errors get reproduced | Empirical collapse without a threshold, a predictor of it, or a measurable control parameter |
| [Recursive criticality of AI self-improvement (2609.00137)](https://arxiv.org/abs/2609.00137) | A reproduction number for capability gains | Concerns R&D-level capability gains, not defect propagation in an agent's artifact store |
| [SkillJack (2608.03509)](https://arxiv.org/abs/2608.03509) | Persistent adversarial skills | Adversarial persistence of one injection; no endogenous transmission dynamics |
| [Forgetting Without Restarting (2609.04875)](https://arxiv.org/abs/2609.04875), [dependency-guided repair (2608.10502)](https://arxiv.org/abs/2608.10502), [frontier-scan idea #2](frontier-scan.md#2-counterfactual-rollback-of-learned-sparse-writes) | Rollback of dependent state/writes | Repair after the fact. Here provenance is a *control input* that changes R online, and the theory says when repair is necessary |

To our knowledge, none of these papers predicts *when* self-improvement turns into self-contamination from
quantities measured before deployment. A paper would need to show that R measured with the challenge trial
predicts the onset of collapse across real agents, models and gates.

## Stage 0 results (CPU simulator)

Code: [`agents/epidemic`](../agents/epidemic). `python -m agents.epidemic.experiments` regenerates everything
below (≈3 minutes on 6 cores); tests are in `tests/test_epidemic.py`.

- **Sharp transition at R = 1.** In 260 runs (τ ∈ [0, 0.6], α_D/α_S ∈ [0.25, 2], 4 seeds each, T = 4000), the median defective fraction is 0.013 for R < 0.9 and 0.38 for R > 1.1
  ([figure](../agents/epidemic/results/phase_diagram.png)).
- **Path dependence (founder effects).** Below the fixed point, outcomes vary widely across seeds because early defects get locked in. The unconditional mean-field ODE overestimates contamination at finite T. Conditioned on the state at round 200, however, the ODE predicts the round-4000 fraction with r = 0.97 and MAE = 0.047.
- **Rise then fall.** At R = 1.6, success peaks at 0.80 within the first rounds (median, 12 seeds; no-memory baseline 0.40) and decays to 0.45 by round 6000. The defective fraction grows along the predicted N^{R−1} slope ([figure](../agents/epidemic/results/rise_then_fall.png)).
- **Interventions at round 2500** (R = 1.6, 12 seeds; success over the last 500 rounds, defective fraction at the end):

| Intervention | Success after | Final defect fraction |
| --- | --- | --- |
| None | 0.41 | 0.44 |
| Roll back root defects | 0.42 | 0.43 |
| Remove provenance closure of roots | 0.66 | 0.19 |
| Oracle purge of all defects | 0.82 | 0.03 |

- **Online tracing moves R across 1.** With exposure d = 0.1 (R = 1.1), success at the end of the run is 0.63 without tracing and 0.81 when each traced descendant is also removed with probability φ = 0.9. The defective fraction drops from 0.20 to 0.03. With d = 0, tracing does nothing because no defect is ever exposed.

## Stage 0b: measuring R on a real model

[`agents/llm_pilot/challenge_trial.py`](../agents/llm_pilot/challenge_trial.py) plants a wrong unit-conversion lesson in the agent's context. It then
asks the agent to solve a task, distill a new lesson, and self-gate it. That yields ε, τ (with and without
verifier feedback) and α_D/α_S. LLM_RESULTS

## Plan to a paper

1. **Measure R on real agents.** Run the challenge trial on 3+ models (Qwen2.5 1.5B/7B/32B, one API model) × 3 gates (self-judge, held-out
   verifier, unit tests) × 2 retrieval breadths (k). ≈ 30 GPU-hours on one 24 GB GPU for the open models.
2. **Run real streams.** Use continual task streams with real artifact stores (skill libraries in the style of AgentCL and ServeLearnBench, and a code-agent lesson memory),
   1–5k episodes, ≥ 5 paired streams per setting. Preregister R_measured and test whether collapse onsets where predicted;
   include sweeps that cross R = 1 by changing k and the gate. ≈ 200–400 GPU-hours. This is where a cluster would help.
3. **Test the controls.** Compare provenance-closure removal, R-aware retrieval (cap k so that k·τ·α_D/α_S < 1), and the existing
   pre-commit gates at a matched compute budget.
4. **Close a theory gap.** Add finite-population and founder-effect corrections. The current mean-field ODE is accurate only conditional on the early state.

**Kill criteria.** Stop if R measured on real agents does not separate stable from collapsing streams (AUC < 0.75),
or if a per-candidate gate baseline explains collapse as well as R does.
