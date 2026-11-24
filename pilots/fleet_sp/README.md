# Surprisingly-popular fleet memory (H1 and H1b)

This CPU pilot tests the [reviewed H1](https://github.com/manojbajaj95/cl/blob/devin/1795532059-agent-cl-ideas/ideas/agents/batch-8.md#h1-minority-lessons-from-rare-regimes-surprisingly-popular-aggregation-for-fleet-memory) and the [H1b prior-subtraction follow-up](https://github.com/manojbajaj95/cl/blob/devin/1795532059-agent-cl-ideas/ideas/agents/batch-10.md#h1b-surprisingly-popular-without-asking-use-the-memory-free-model-as-the-meta-prediction) from [PR #7](https://github.com/manojbajaj95/cl/pull/7).

## Verdict: kill both in this pilot

**H1 fails the exposure gate.** All 320 forecasts on correct rare-regime lessons were exactly 1/9. Pearson correlation is undefined for a constant forecast; under the prespecified zero-signal convention, the gate was **r = 0.000 [0.000, 0.000]** versus the required 0.20. The degenerate interval reflects identical assigned values in the four fleets, not a bound on correlations attainable with other elicitation prompts. On all rare-regime lessons the diagnostic estimate was **0.191 [−0.057, 0.472]**; this variation came from incorrect lessons, whose estimate was also 0.191. As required by the gate, we did not evaluate the H1 controls (keep-all + regime retrieval, BP-TD, majority, confidence weighting or high-confidence minority). Elicited SP was evaluated only as the H1b reference.

**H1b matched elicited SP but did not establish a gain over mean endorsement without prior subtraction.** Log-prob SP's rare-task gain over mean endorsement was one answer out of 64: **+1.56 percentage points [0.00, +4.69]**. Its paired difference from elicited SP was **0.00 points [0.00, 0.00]**. None of the three evaluated methods selected a correct rare lesson in any fleet.

| Method | Common accuracy, % [95% CI] | Rare accuracy, % [95% CI] |
| --- | ---: | ---: |
| Elicited SP (H1b reference) | 96.88 [90.63, 100.00] | 4.69 [0.00, 9.38] |
| Log-prob SP (H1b) | 96.88 [90.63, 100.00] | 4.69 [0.00, 9.38] |
| Mean endorsement probability, no prior subtraction | 96.88 [90.63, 100.00] | 3.13 [0.00, 6.25] |

**What failed upstream:** All four correct rare lessons were in every union. Rare-exposed agents assigned them about 23.1% endorsement probability on average versus 3.4% without exposure (difference **+19.75 points [18.04, 21.55]**), but the fleet produced only 5 greedy endorsements out of 320 votes on these lessons. Exposed agents had explicit rare examples but proposed just 1.06 of the four correct rare rules on average; unexposed agents guessed 0.84. This is a failure of this CPU model, prompt and world to produce or preserve useful rare lessons, not evidence against SP when informed agents reliably endorse correct minority lessons. The four fleets share one synthetic API rule family; CIs reflect between-fleet variation within that family.

Machine-readable gate, per-fleet accuracies and paired deltas: [results.json](results.json).

## Protocol

- **World:** A private API has four operations with conventional HTTP methods in the common regime and a different allowed method for each operation in the rare regime. Regime names are randomly assigned. In each of four independently seeded fleets, all 20 agents see four accepted common calls, and four uniformly chosen agents also see four accepted rare calls. Example IDs and presentation order vary. All agents share Qwen2.5-1.5B-Instruct (Q4_K_M, CPU); no weights are updated.
- **Authoring:** Each agent proposes one of two possible methods for every regime/operation and reports its confidence (1–4). An agent without rare experience has to extrapolate. Recommendations are sampled from the model at temperature 0.7; confidence is the greedy response. Both correct and mistaken recommendations enter the same deduplicated pool. The pool keeps each recommendation's maximum author confidence for the minority control.
- **Rating:** Every agent sees its own call history and rates each pooled recommendation. For each lesson, $P_i$ is the next-token probability of “Yes” conditioned on “Yes” or “No”; the greedy response is the binary endorsement. Each agent also directly predicts fleet endorsement on a 10-point grid (0/9 to 9/9) and rates its own vote confidence (1–4). $P_0$ is measured with the same endorsement prompt and answer tokens, but no call history.
- **Gate:** Compute Pearson $r$ within each fleet between exposure (0/1) and each agent's mean elicited forecast on correct rare-regime lessons. The cross-fleet mean gates H1 at $r \ge 0.20$. For diagnostics, report the corresponding correlations for all and for incorrect rare lessons. Averaging forecasts over correct and incorrect lessons can cancel opposite effects; the gate targets the correct tail lessons H1 is meant to preserve. Constant forecasts (or no correct rare proposals) count as zero signal. Correctness is available to the offline gate and grading code only, never selectors or evaluation prompts. If the gate fails, skip H1's controls and still score elicited SP as the reference for H1b.
- **Evaluation:** A fresh, history-free copy of the same model responds greedily with four memory entries and the task's regime, operation and two candidate methods. Each fleet has 16 held-out calls per regime (four fresh IDs per operation, counterbalanced option order). Static selectors pick four entries globally; union retrieval can choose four per question. The experiment asserts equal prompt token counts across arms for each question, and uses shared random ordering and score tie breaks independent of the labels. No validation or test labels tune any selector.

| Arm | Selection score / retrieval |
| --- | --- |
| Elicited SP | Greedy endorsement fraction minus mean elicited forecast |
| Log-prob SP (H1b) | $\mathrm{mean}_i\,P_i - P_0$ |
| Mean $P_i$ (H1b ablation) | $\mathrm{mean}_i\,P_i$, without subtracting $P_0$ |
| Majority | Greedy endorsement fraction |
| Confidence | Greedy endorsement fraction weighted by the agent's elicited confidence in its vote |
| High-confidence minority | Below 50% endorsement first, highest author confidence first within that set; fill any remaining slots by author confidence |
| BP-TD (co-occurrence and family) | Posterior probability of “Yes” in the binary-label specialization of [2611.04805](https://arxiv.org/abs/2611.04805), cross-checked against the [reference algorithm](https://github.com/LaureBerti/BPTD/blob/058f95b2b59562785d2cfaeb3edee973c756127f/bptd/bp.py). Same-label and different-label votes contribute signed agreement; co-occurrence uses the paper's fixed signed threshold 0.5, and family weights count the 20 same-base agents as one effective vote. Both use the Beta(2,1) prior, 0.3 damping, 0.4 signed smoothing, and 100-iteration cap; no labels. |
| Keep-all + retrieval | Keep all pooled lessons; prefer matches on explicit regime, then exact operation, then greedy endorsement share. No access to correct answers. |

Bootstrap CIs use 20,000 fleet-level resamples; paired differences resample the same fleets across arms. The four fleets, not the 128 held-out calls, are the independent units. H1 requires a gate pass, at least +10 percentage points on rare tasks vs majority, and a positive rare-task advantage over the other controls (in particular a paired CI above zero against keep-all retrieval); the original H1 proposal's stricter +10 points vs best control and at most −2 on common are also checked when applicable. H1b must match or beat elicited SP on rare-task point accuracy and show an advantage over mean $P_i$ alone; a paired CI including zero is insufficient to establish that advantage.

## Reproduce

```sh
python -m pip install numpy==2.2.6 scipy==1.15.3
python -m pip install --prefer-binary --only-binary=:all: \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu \
  llama-cpp-python==0.3.38
curl -fL -O https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
OPENBLAS_NUM_THREADS=1 python -B pilots/fleet_sp/experiment.py \
  --model qwen2.5-1.5b-instruct-q4_k_m.gguf --out fleet-sp-run
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s pilots/fleet_sp -v
```

The downloaded GGUF's SHA-256 is `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`. Use a fresh output directory for a new configuration. The script caches per-fleet proposals, ratings and held-out answers and writes a `summary.json`.
