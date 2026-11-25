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
verifier feedback) and α_D/α_S. Results below are for Qwen2.5-1.5B-Instruct Q4 on CPU. τ is measured
for the one relevant lesson in context, with 3 distractor lessons.

| Domain | Trials | ε | τ, no feedback | τ, verifier feedback | Self-gate α_D / α_S | Wrong answers with bad lesson |
| --- | --- | --- | --- | --- | --- | --- |
| Real units (model has a prior) | 240 | 0.00 | 0.48 | 0.05 | 0/32 vs 0.40 | 0.99 |
| Made-up units (no prior) | 120 | 0.00 | 1.00 | 1.00 | 0.02 vs 0.00 (rejects all) | 1.00 |

- **Planted lessons override the model at solve time.** With a bad lesson in context, the agent answers wrong 99–100% of the time, even when it knows the true factor.
- **Feedback stops transmission only when the model can check the lesson.** For real units, a verifier's "incorrect" makes the agent drop the bad factor (τ 0.48 → 0.05), and the self-judge rejects every defective lesson. For made-up units, τ stays 1.0 even with feedback: the agent keeps the planted factor. The self-gate there rejects everything, so it blocks learning instead of telling defects apart.
- **R depends on model × domain × gate.** It is not a property of the agent alone. The dangerous regime is knowledge the model cannot check, which is exactly what deployed agents learn (private APIs, a user's conventions, hidden policies). That is where the paper's experiments should focus.

## Stage 0c: does measured R predict real stream collapse? (CPU, Qwen2.5-1.5B)

[`agents/llm_pilot/stream.py`](../agents/llm_pilot/stream.py) runs closed-loop lesson-memory streams on made-up unit conversions. Each episode the agent retrieves k lessons from its own pool, answers, and writes one new lesson that a gate admits. With probability f, a verifier sees the outcome and admits the lesson only if the answer was right; otherwise the lesson is admitted unchecked. Seeded defects are either plain wrong factors or "Correction:"-style wrong factors. A challenge trial with fixed lesson mixes (1,200 calls) measures ε, τ, α_D, α_S and R for each (style, k, f) **before** any stream runs. Then 216 streams run, one for each style × k ∈ {1,2,4} × f ∈ {0,0.4,0.8} × 6 unit pairs × 2 seeds, each with 50 episodes from 8 seed lessons at a 25% defect share. [`analyze_stream.py`](../agents/llm_pilot/analyze_stream.py) scores each predictor on whether the stream's defect share grew.

| Predictor of "defect share grew" (216 streams) | AUC [95% CI] | Spearman with final defect share |
| --- | --- | --- |
| **R measured offline** | **0.87 [0.82, 0.91]** | 0.64 |
| Gate catch rates only (α_D/α_S) | 0.75 [0.68, 0.81] | 0.43 |
| Full mean-field forecast from the curve | 0.86 [0.81, 0.91] | 0.62 |
| Stream's own defect share after 5 episodes | 0.84 [0.78, 0.90] | 0.62 |
| ... after 10 episodes | 0.94 [0.91, 0.97] | 0.79 |
| ... after 25 episodes | 0.97 [0.95, 0.99] | 0.93 |

| Measured R | Streams | Share grew | Final defect share | Success, last 12 episodes |
| --- | --- | --- | --- | --- |
| < 0.95 | 144 | 0.08 | 0.12 | 0.67 |
| 0.95-1.1 (neutral copying) | 48 | 0.35 | 0.23 | 0.60 |
| > 1.1 | 24 | 0.62 | 0.41 | 0.35 |

- **R predicts collapse where the gate does not.** At k=4 with no gate, both defect styles have gate ratio 1.0, but R is 0.67 for plain defects and 2.07 for correction-style ones. Plain pools cleaned themselves in 0/12 streams that grew (final share 0.06), because the model follows the majority of retrieved lessons. Correction-style pools grew in 10/12 streams (final share 0.49), and task success fell to 0.28. R gets this from the defect-transmission curve; catch rates cannot see it.
- **Retrieval breadth changes the sign.** For plain defects, larger k lowers R (majority voting suppresses a lone defect). For persuasive defects, larger k raises it. This is the k·τ term, measured rather than assumed.
- **Online extrapolation wins after about 10 episodes.** R matches a 5-episode extrapolation and is available before deployment, but loses to extrapolating 10+ episodes of the stream itself. Pools here are small (8 seed lessons, 50 episodes), so 10 episodes is 20% of the run. The reviewer's bar (beat extrapolation from round 200) is not met on equal footing at this scale.
- **Misfit.** Correction-style, k=4, f=0.8 has R = 0.76 but grew in 6/12 streams. The mean-field forecast (0.21) undershoots the observed 0.27. A likely cause is that descendants inherit the persuasive phrasing, which the root-only challenge trial does not measure. This needs a heritable-virulence term.
- **Limits.** One 1.5B model, one task family, 50-episode streams, and outcome-only gates. "Grew" at R ≈ 1 is drift. Next: longer streams and larger pools (so early extrapolation has less of a head start), 7B/32B models, real skill stores.

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
