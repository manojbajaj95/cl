# Defect transmission before the GPU sweep

Single-generation challenge on Qwen2.5-Coder-1.5B-Instruct Q4_K_M (CPU). See the [protocol](protocol.md) for the gate and [results](results.json) for all contrasts.

**Keep, narrowly. Run only the capped 5 GPU-h Stage 1, not the k-sweep.** Defective notes increased new helper defects by **+2.32 pp [0.24, 4.83]** over same-length filler and **+4.43 pp [2.33, 6.90]** over the entropy-matched no-note control. The increase is specific to the planted signature: **+3.70 pp [1.14, 6.73]** vs filler; other defects decreased by 1.39 pp [−2.74, −0.28]. The correct note is a positive control for content use.

| Retrieved context | Any defect in new helper | Planted defect in new helper | Any defect in initial patch |
| --- | ---: | ---: | ---: |
| Defective note (gross τ) | 57.94% [49.93, 66.17] | 33.26% [25.60, 40.81] | 57.50% [46.16, 68.38] |
| Same-length filler | 55.62% [48.09, 63.58] | 29.56% [22.96, 36.24] | 53.67% [42.88, 64.31] |
| Correct note | 47.50% [38.26, 57.39] | 25.31% [18.42, 32.65] | 41.71% [31.17, 53.51] |
| No note, nominal temperature | 55.33% [48.22, 62.77] | 29.52% [23.49, 35.53] | 50.45% [41.60, 59.21] |
| No note, matched temperature | 53.51% [45.46, 62.05] | 28.74% [21.92, 35.69] | 46.22% [36.28, 57.28] |

Intervals are paired-family percentile 95% bootstrap CIs across 48 held-out tasks in 16 families. Defective minus correct was +10.43 pp [5.67, 15.68]. The PR #4-style background adjustment was **5.22% [0.53, 10.97]**; this is not an identified per-episode transmission probability without the protocol's background assumption. The source fit gave temperatures 0.533 (solve) and 0.659 (write); held-out entropies were 0.705 vs 0.699 and 0.786 vs 0.775 nats, respectively (defective note vs matched). As a descriptive check, 10 of 16 families had a positive gross contrast vs filler, and leave-one-family-out point estimates were +1.36 to +2.70 pp.

**What Stage 1 needs to show.** This is weak-feedback, planted-note evidence on a constrained decoder; neither free-form lesson writing nor gate selectivity, removal, or collapse was tested. Do not plug the gross defect rate into the reproduction law. If the adjusted point estimate carried over and had the law's interpretation, even an optimistic zero-removal gate with defective admission no higher than sound admission would give \(R\le 0.42\) at \(k=8\). Measure transmission with free-form runnable artifacts and matched controls on 7B, vary hidden verifier coverage, and stop unless there is clear transmission above filler and a plausible setting with \(R\) in the requested interval. Do not fund the larger sweep from this CPU result alone.

## Reproduce

From this directory, in a Python 3.10 virtual environment:

```sh
python -m pip install numpy==1.26.4
python -m unittest -v
python analyze.py policies.jsonl --out reproduced.json
cmp results.json reproduced.json
```

For fresh inference, use the [pinned model revision](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/blob/f86cb2c1fa58255f8052cc32aeede1b7482d4361/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf) with SHA-256 `cc324af070c2ecbfd324a30884d2f951a7ff756aba85cb811a6ec436933bb046`. Build the CPU binding and score the prompts:

```sh
python -m pip install packaging==25.0 scikit-build-core==0.11.6 wheel==0.45.1 cmake==3.31.10 ninja==1.11.1.4
CMAKE_BUILD_PARALLEL_LEVEL=6 python -m pip install --no-build-isolation --no-binary=llama-cpp-python llama-cpp-python==0.3.18
python collect.py --model /path/to/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf --out fresh-policies.jsonl
python analyze.py fresh-policies.jsonl --out fresh-results.json
```

[The frozen policies](policies.jsonl) contain all notes, menu permutations, full prompt token counts, outcome signatures, and raw logits. The first row records the checkpoint and inference configuration. Fresh logits may differ slightly with CPU kernels; the frozen policy file reproduces the analysis without inference.
