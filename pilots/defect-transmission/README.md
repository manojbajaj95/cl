# Defect transmission before the GPU sweep

Single-generation challenge on Qwen2.5-Coder-1.5B-Instruct Q4_K_M (CPU). See the [protocol](protocol.md) for the gate and [results](results.json) for all contrasts.

**Keep under the CPU criterion; GPU work remains parked.** At one retrieved note, defective notes increased new helper defects by **+2.32 pp [0.24, 4.83]** over same-length filler and **+4.43 pp [2.33, 6.90]** over the entropy-matched no-note control. The increase is specific to the planted signature: **+3.70 pp [1.14, 6.73]** vs filler; other defects decreased by 1.39 pp [−2.74, −0.28]. The correct note is a positive control for content use.

| Retrieved context | Any defect in new helper | Planted defect in new helper | Any defect in initial patch |
| --- | ---: | ---: | ---: |
| Defective note (gross τ) | 57.94% [49.93, 66.17] | 33.26% [25.60, 40.81] | 57.50% [46.16, 68.38] |
| Same-length filler | 55.62% [48.09, 63.58] | 29.56% [22.96, 36.24] | 53.67% [42.88, 64.31] |
| Correct note | 47.50% [38.26, 57.39] | 25.31% [18.42, 32.65] | 41.71% [31.17, 53.51] |
| No note, nominal temperature | 55.33% [48.22, 62.77] | 29.52% [23.49, 35.53] | 50.45% [41.60, 59.21] |
| No note, matched temperature | 53.51% [45.46, 62.05] | 28.74% [21.92, 35.69] | 46.22% [36.28, 57.28] |

Intervals are paired-family percentile 95% bootstrap CIs across 48 held-out tasks in 16 families. Defective minus correct was +10.43 pp [5.67, 15.68]. The PR #4-style background adjustment was **5.22% [0.53, 10.97]**; this is not an identified per-episode transmission probability without the protocol's background assumption. The source fit gave temperatures 0.533 (solve) and 0.659 (write); held-out entropies were 0.705 vs 0.699 and 0.786 vs 0.775 nats, respectively (defective note vs matched). As a descriptive check, 10 of 16 families had a positive gross contrast vs filler, and leave-one-family-out point estimates were +1.36 to +2.70 pp.

## Retrieval-depth follow-up

The reviewer asked whether the upper 95% CI of \(k\tau_{\mathrm{eff}}(k)\) reaches 0.5 at any retrieval depth. We replaced a single filler with a defective note in an otherwise sound stack to estimate the low-prevalence effect; this avoids counting the loss of a correct note as transmission. The separate dose fit uses zero, one, and all defective notes in filler stacks. See the [depth protocol](depth-protocol.md) and [full results](depth-results.json).

| Notes retrieved | Local per-defect τ_eff (95% CI) | k·τ_eff (95% CI) | Fitted per-defect τ in filler (95% CI) | k·fitted τ (95% CI) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 5.22% [0.53, 10.97] | 0.052 [0.005, 0.110] | 5.22% [0.53, 10.97] | 0.052 [0.005, 0.110] |
| 2 | 7.24% [3.75, 11.15] | 0.145 [0.075, 0.223] | 2.86% [0.64, 5.74] | 0.057 [0.013, 0.115] |
| 4 | 7.88% [3.44, 13.10] | 0.315 [0.138, 0.524] | 1.45% [0.23, 3.05] | 0.058 [0.009, 0.122] |
| 8 | 6.71% [2.78, 11.86] | 0.537 [0.222, 0.949] | 0.92% [0.08, 2.08] | 0.074 [0.006, 0.166] |

The local contrast clears the headroom gate at k=4 and k=8; neither lower bound clears 0.5. The fitted filler-stack dose does not: repeated defective notes saturate. At k=8, the all-defective risk was 14.2 pp [8.6, 19.1] below the independent-hit extrapolation from one defective note. The mostly-sound arm still raised the planted-signature risk by 3.2 pp [1.1, 6.0] over its one-filler match at k=8, but did not beat the no-note temperature control on all defects (−1.9 pp [−4.4, 0.3]). The two controls answer different questions; the depth result does not establish a monotone, independent per-note transmission mechanism.

**Funding decision.** The old capped Stage 1 is technically justified by the requested *local* headroom gate if that plan is reopened; neither the larger GPU sweep nor the parked replacement stream stage is greenlit by this result. Replicate the low-prevalence, planted-defect effect with free-form runnable lessons and both controls on 7B before interpreting \(R\). Actual gate selectivity, removal, and collapse are still unmeasured here; do not plug the gross defect rate into \(R\).

## Reproduce

From this directory, in a Python 3.10 virtual environment:

```sh
python -m pip install numpy==1.26.4
python -m unittest -v
python analyze.py policies.jsonl --out reproduced.json
cmp results.json reproduced.json
python depth_analyze.py --dir depth-data --out reproduced-depth.json
cmp depth-results.json reproduced-depth.json
```

For fresh inference, use the [pinned model revision](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/blob/f86cb2c1fa58255f8052cc32aeede1b7482d4361/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf) with SHA-256 `cc324af070c2ecbfd324a30884d2f951a7ff756aba85cb811a6ec436933bb046`. Build the CPU binding and score the prompts:

```sh
python -m pip install packaging==25.0 scikit-build-core==0.11.6 wheel==0.45.1 cmake==3.31.10 ninja==1.11.1.4
CMAKE_BUILD_PARALLEL_LEVEL=6 python -m pip install --no-build-isolation --no-binary=llama-cpp-python llama-cpp-python==0.3.18
python collect.py --model /path/to/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf --out fresh-policies.jsonl
python analyze.py fresh-policies.jsonl --out fresh-results.json
mkdir -p fresh-depth-data
python depth_collect.py --model /path/to/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf --dir fresh-depth-data --threads 7
python depth_analyze.py --dir fresh-depth-data --out fresh-depth-results.json
```

[The frozen single-note policies](policies.jsonl) contain all notes, menu permutations, full prompt token counts, outcome signatures, and raw logits. The first row records the checkpoint and inference configuration. [The frozen depth policies](depth-data/) use the same checkpoint and contain each stack's notes, order, token counts, and raw logits; the depth analysis reuses the single-note policies for k=1 and the no-note controls. Fresh logits may differ slightly with CPU kernels; the frozen policies reproduce the reports without inference.
