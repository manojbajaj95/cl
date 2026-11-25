# B3 pilot: lesson-only interference prediction

## Verdict: KILL

On the 200 pairs, negative implicit-update alignment was **0.329 Spearman points below NLI**, not 0.15 above it, and **0.437 below function-vector cosine**. A length-matched irrelevant lesson caused a larger average accuracy drop than the real second lesson (7.08 vs. 3.70 percentage points). None of the three keep criteria passed.

| Accuracy-drop statistic | Estimate | 95% pair CI | 95% lesson-cluster CI |
| --- | ---: | ---: | ---: |
| Spearman: negative ΔW inner product | −0.273 | [−0.398, −0.141] | [−0.514, 0.006] |
| Spearman: negative ΔW cosine | −0.226 | [−0.358, −0.085] | [−0.462, 0.012] |
| Spearman: NLI contradiction | 0.057 | [−0.083, 0.187] | [−0.202, 0.286] |
| Spearman: function-vector cosine | 0.165 | [0.015, 0.303] | [−0.071, 0.414] |
| ΔW inner product minus NLI | −0.329 | [−0.508, −0.149] | [−0.648, −0.002] |
| ΔW inner product minus function-vector cosine | −0.437 | [−0.678, −0.185] | [−0.880, 0.007] |
| Partial Spearman: ΔW, controlling for length and control drop | −0.245 | [−0.381, −0.107] | [−0.472, 0.034] |
| Mean accuracy drop with B (pp) | 3.70 | [1.00, 6.30] | [−2.64, 11.63] |
| Mean accuracy drop with irrelevant lesson (pp) | 7.08 | [4.10, 10.08] | [−2.00, 17.69] |
| Actual minus irrelevant drop (pp) | −3.38 | [−6.43, −0.25] | [−11.74, 3.88] |

The accuracy drop was 7.15 pp for the 100 same-workflow conflicts and 0.25 pp for the 100 cross-workflow pairs. But A-alone accuracy was only **23.40%** (lesson-cluster CI [14.77%, 32.55%]; uniform five-label chance is 20%), so there was little baseline headroom. The irrelevant/actual drop ratio was 1.91 at the point estimates; the denominator can cross zero in the clustered bootstrap, so the absolute drops and their difference are more informative about uncertainty. This is a no-go for this predictor and setup, not evidence that implicit updates never predict interference or that attention dilution is the sole cause.

The continuous correct-label log-probability drop gave Spearman −0.258 (lesson-cluster CI [−0.643, 0.154]) for ΔW, 0.127 for NLI and 0.082 for function-vector cosine; the mean real and irrelevant drops were 1.114 and 0.670 nats. Full secondary and control intervals are in [results.json](results.json). The run took **18 min 42 s** on eight CPU threads, excluding downloads and installation.

## Design

- **Model:** Qwen2.5-1.5B-Instruct, CPU float32. There are 25 rule lessons (five workflows × five positions in a list of labels), 20 held-out input lists balanced across correct labels, and 200 distinct ordered pairs. For each A, B is each of the four contradictory rules for A's workflow and one seeded random rule from each other workflow.
- **Interference:** With the same 20 items, compare A alone, A followed by B, and A followed by an irrelevant museum-handling instruction. The control occupies the same slot and is exactly Qwen-token-length matched for each full prompt. The primary outcome is the A-alone minus A+B difference in greedy next-token label accuracy (including whitespace variants); the secondary outcome is the difference in average log probability of the correct label.
- **Implicit update:** Single-token rank-one specialization of [Mazzawi et al., §2 and Appendix A](https://arxiv.org/abs/2510.08734). Compare the same fixed neutral readout (`End of notes.`) with and without the lesson, with no task inputs or answers. At each of layers 6, 12, 18 and 24 (zero-based), let `a` be the no-lesson post-attention RMSNorm output and `a_I` its contextual counterpart. For each SwiGLU up/gate projection `W`, use the minimum-norm update `ΔW = W(a_I − a)aᵀ/‖a‖²`: this exactly reproduces the contextual projection on that reference activation. The normalized input difference includes earlier layers' effects; this is a local readout proxy, not the paper's iterative full-model patching algorithm. Score the negative summed Frobenius inner products across projections/layers; report negative cosine as a secondary predictor.
- **Baselines:** Ordered DeBERTa-v3-small NLI contradiction probability, and ordinary cosine of [Wang et al.](https://arxiv.org/abs/2605.16591)-style function vectors. For FV, causally localize the 10 highest mean-effect attention heads out of all 336 by replacing each head's final-token activation in a wrong-rule prompt with its clean mean, then ranking the gains in correct-label probability. Average each lesson's sum of those heads' projected final-token outputs over two calibration inputs separate from the 20 held-out items. The FV baseline gets task-specific calibration; ΔW does not.
- **Inference:** Spearman on the 200 directed pairs, with paired percentile 95% intervals from 2,000 draws each: resample pair rows, or resample all 25 lesson identities and weight each row by the product of the multiplicities of its A and B (same draw on both axes). For the dilution check, compare signed mean drops and compute their ratio; the partial Spearman diagnostic residualizes predictor and outcome ranks on length and control-drop ranks. Apply the reader's thresholds to the primary point estimates, not to the secondary metrics or CI endpoints.

This is a narrow rule-task pilot: the five workflows share the positional selection primitive, and results are conditional on this prompt format, model and irrelevant control topic. The control estimates loss under a placebo lesson; equal token count alone does not isolate an attention mechanism. The two-way lesson bootstrap accounts for repeated identities, not uncertainty over workflow families or input lists.

## Reproduce

From this directory in a Python 3.10 environment:

```sh
python -m pip install -r requirements.txt
python -B -m unittest discover -v
python -B pilot.py
python -B pilot.py --reanalyze results.json --output reanalysis.json
```

`pilot.py` runs on CPU and defaults to pinned Hugging Face checkpoints, eight PyTorch threads and 2,000 draws. `results.json` includes each pair's predictor scores, condition accuracies/mean log probabilities, exact-matched control text, selected heads, configuration and CIs for both outcomes.
