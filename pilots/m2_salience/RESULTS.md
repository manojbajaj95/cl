# M2: outcome-trained salience for in-context lessons

**Verdict: KILL.** M2 reached **46.67%** on returning regimes against **83.33%** for the evidence-guided EASE-KV control, a **−36.67 pp** gap (paired 95% CI **[−45.00, −25.56]**). First-visit loss was **−30.09 pp** **[−36.20, −23.61]**. Even without the oracle evidence control, M2 trailed binary LOO and hand-set recency by 0.42 pp each on returns, below the required +5 pp. M2 did clear the entropy-matched no-lesson comparison. The conditional **R1 stability-to-LoRA routing: not run (M2 killed)**.

## Results

Cells are accuracy (%) or paired differences (pp), with 95% bootstrap intervals.

| Arm | First visits | Returning visits | M2 − arm, first | M2 − arm, returning |
|---|---:|---:|---:|---:|
| Uniform | 33.33 [33.33, 33.33] | 34.17 [30.00, 40.00] | +16.57 [11.48, 21.30] | +12.50 [1.11, 23.33] |
| **M2** | **49.91 [44.81, 54.63]** | **46.67 [39.44, 55.56]** | — | — |
| Binary LOO | 47.31 [43.61, 50.93] | 47.08 [40.69, 51.94] | +2.59 [−1.94, 6.94] | −0.42 [−6.11, 6.11] |
| ACE-style | 44.17 [39.26, 48.43] | 44.58 [33.19, 55.28] | +5.74 [1.30, 10.09] | +2.08 [−3.75, 8.61] |
| REPLUG-style | 36.57 [33.33, 39.54] | 34.44 [28.75, 39.58] | +13.33 [8.52, 17.69] | +12.22 [1.25, 25.42] |
| EASE-KV (oracle evidence) | 80.00 [75.00, 83.33] | 83.33 [80.00, 87.50] | −30.09 [−36.20, −23.61] | −36.67 [−45.00, −25.56] |
| Hand-set recency | 46.11 [43.24, 49.17] | 47.08 [38.19, 53.33] | +3.80 [−0.09, 7.50] | −0.42 [−11.67, 9.03] |
| No lesson, temperature matched | 33.33 [33.33, 33.33] | 33.33 [25.00, 40.00] | +16.57 [11.48, 21.30] | +13.33 [8.06, 19.03] |

| Arm − no-lesson temperature | First visits | Returning visits |
|---|---:|---:|
| Uniform | 0.00 [0.00, 0.00] | +0.83 [−7.50, 15.00] |
| M2 | +16.57 [11.48, 21.30] | +13.33 [8.06, 19.03] |
| Binary LOO | +13.98 [10.28, 17.59] | +13.75 [9.72, 18.61] |
| ACE-style | +10.83 [5.93, 15.09] | +11.25 [6.81, 16.25] |
| REPLUG-style | +3.24 [0.00, 6.20] | +1.11 [−11.11, 12.22] |
| EASE-KV | +46.67 [41.67, 50.00] | +50.00 [40.00, 57.50] |
| Hand-set recency | +12.78 [9.91, 15.83] | +13.75 [3.19, 27.36] |

Per-seed accuracy, first / returning:

| Seed | Uniform | M2 | LOO | ACE | REPLUG | EASE-KV | Recency | Temperature |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 101 | 33.33 / 32.50 | 50.28 / 54.58 | 45.83 / 50.83 | 46.94 / 55.83 | 33.89 / 28.33 | 75.00 / 80.00 | 45.56 / 50.42 | 33.33 / 40.00 |
| 202 | 33.33 / 30.00 | 46.94 / 45.00 | 46.67 / 48.75 | 39.17 / 45.42 | 36.67 / 37.08 | 81.67 / 87.50 | 43.61 / 37.92 | 33.33 / 35.00 |
| 303 | 33.33 / 40.00 | 52.50 / 40.42 | 49.44 / 41.67 | 46.39 / 32.50 | 39.17 / 37.92 | 83.33 / 82.50 | 49.17 / 52.92 | 33.33 / 25.00 |

**Gradient signal:** 1,800/1,800 episodes had a nonzero dense gradient. Dense log probability varied in 180/180 sampled query groups (100%); binary correctness varied in 148/180 (82.22%). More usable feedback did not produce the predicted return advantage.

**Temperature check:** source-only T = 1.180 matched full-policy entropy at 0.6298 nats (untempered no lesson: 0.5149). In the exact replay of seed 101, M2 changed the greedy action relative to uniform on 361/600 episodes (60.17%), ruling out pure positive output-temperature scaling of that policy. Its entropy rose by 0.2267 nats on average, but the correlation between episode mean bias and entropy change was only r = 0.009 (mean within-episode bias SD: 2.04 logit units).

CPU wall time: 32m 27s for calibration, recency tuning and all three test seeds, excluding the temperature replay. Full precision, per-episode hits and CIs are in [results.json](results.json).

## Prior work

[PASTA](https://arxiv.org/abs/2311.02262) steers attention to user-named spans, and [learned memory curation](https://arxiv.org/abs/2609.37930) controls which memories to keep. [EASE-KV](https://arxiv.org/abs/2611.11299) already uses signed attention-logit biases per memory and tests an outcome-trained allocator. The incremental claim here is that dense log-probability updates make salience reversible enough to improve returns to prior regimes.

## Protocol

- Frozen Qwen2.5-0.5B-Instruct on CPU. Ten stations, three conflicting valve lessons per station, fixed pool of 30 in a seed-shuffled order. Each regime uses a different correct valve at each station. Regime IDs are never in the prompt. Each 120-episode visit uses six shuffled 20-query blocks (two phrasings per station); visits follow A, B, A, C, B. Test seeds: 101, 202, 303.
- Report three-way greedy valve accuracy, before updating. A1/B1/C1 are first visits; A2/B2 are returns. After prediction, the simulator reveals the correct valve to every adaptive arm. Log probabilities are normalized over A/B/C. A separate seed 999 checked lesson leverage before the run: uniform 33.33%, current-regime oracle subset 78.33%, a 45.00 pp gap. The uniform calibration rate is 1/3 by construction across all three equally weighted mappings.
- **Uniform:** all lessons, zero bias. **M2:** one scalar per lesson; add it to each lesson token's key logit for every query-suffix position, layer and head. Freeze the causal prompt-prefix KV, backpropagate the correct valve's log probability into these 30 scalars, and update by Adam (LR 0.15, clip biases to [−4, +4]).
- **LOO:** credit each lesson by the change in correct-valve log probability when physically removing it from the full bank. Update exponentially discounted credit (0.9) every episode, rerank every ten episodes, keep nonnegative credit, and score all candidates even when excluded so they can re-enter. **ACE-style:** keep lessons whose discounted helpful counts meet or exceed harmful counts; compare each single-lesson context's binary correctness with no notes, using the same discount and keep-update schedule as LOO. Both start with all lessons.
- **REPLUG-style:** mix the 30 single-lesson answer distributions in probability space, optimizing mixture logits against the same revealed answer with M2's Adam LR and clipping. **EASE-KV:** [2611.11299, §3.3 and Appendix B](https://arxiv.org/html/2611.11299), Uniform ±2: +2 for the current query's oracle supporting lesson, −2 for all others (zero on non-lesson tokens). This diagnostic reads evidence labels *before* scoring; it is deliberately stronger in information than the online arms. EASE and M2 share the exact same frozen, causally encoded text KV rather than splicing separate latent-memory banks.
- **Recency:** no learned coefficients; bias each lesson by 2 × 2^(−age / half-life) from its last confirmation by a past outcome; never-confirmed lessons get zero. Choose half-life on seed 0 only: 20 episodes (58.50% overall, vs. 50.17%, 51.00%, 46.17% for 5, 80, 320), then freeze it for all test seeds.
- **No-lesson temperature:** following the [PR #27 confound check](https://github.com/manojbajaj95/cl/pull/27), fit one T on 20 source queries from disjoint station identities by matching mean predictive entropy to the full-lesson policy. Freeze T before evaluating. Scaling the three logits by 1/T changes confidence but cannot change greedy accuracy; this control tests whether memory changes the preferred action, unlike the prior pilots' stochastic policy returns. Replay seed 101 exactly to measure M2's argmax changes, bias dispersion and mean bias versus entropy change.
- **Uncertainty:** 10,000 paired hierarchical bootstrap replicates, resampling seeds and then contiguous 20-episode blocks within each visit with identical indices for every arm. The best-control CIs reselect the best control in each bootstrap draw. With just three seeds and repeated query phrasings, these intervals are pilot-scale, not a generalization claim. Fixed predictions are memoized by exact prompt; feedback and online updates are not. The experiment matches episode/outcome information for adaptive arms, not control FLOPs.
- **Signal diagnostic:** count nonzero M2 gradient norms (>10⁻⁸) on every episode. Every tenth episode also compares eight allocations (current bias and seven independent {−2, 0, +2} per-lesson perturbations, clipped) for the same query. Contrast means correct-valve log-prob variation >10⁻⁶ or, for the binary-reward variant, a mix of right and wrong greedy answers. This compares supervision resolution at matched allocations, not performance of a separately trained binary policy.

## Reproduce

From the repository root on CPU (Python 3.10):

```sh
python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r pilots/m2_salience/requirements.txt
python -m unittest discover -s pilots -p 'test_*.py'
SECONDS=0  # Bash elapsed time
python -m pilots.m2_salience.pilot --calibrate --output gate.json
python -m pilots.m2_salience.pilot --tune-recency --output tuning.json
python -m pilots.m2_salience.pilot --tuning tuning.json --output raw-m2.json
M2_SECONDS=$SECONDS
python -m pilots.m2_salience.temperature_check --output diagnostic.json
python -m pilots.m2_salience.temperature_check --raw raw-m2.json --diagnostic diagnostic.json --output m2-with-temperature.json
python -m pilots.m2_salience.report m2-with-temperature.json --calibration gate.json --wall-seconds "$M2_SECONDS" --output m2-results.json
```

See [the separate N1 pilot](../n1_layer_local_kv/RESULTS.md) for layer-local lesson visibility.
