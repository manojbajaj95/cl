# CPU probe: choosing where versus how to edit

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python pilots/model-guided-edits/probe.py
```

This regenerates [results.json](results.json). Five seeds took 9.66 seconds total on one CPU thread with NumPy 2.2.6. Parentheses below are 95% percentile bootstrap intervals from 10,000 resamples of the **five model/stream seeds**, not of the 100 associations as independent models. These are pilot intervals, not population guarantees.

## Setup

For each seed, train a four-hidden-layer ReLU MLP (width 128) to regress a random teacher's standardized outputs. Held-out teacher MSE was 0.339 (0.317–0.363) in squared teacher standard deviations. Test 20 fresh inputs per seed, with new targets set to the student's original output plus a balanced, shuffled `±2` offset. Each association starts from the same unedited model. Measure retention on 512 independent teacher-distribution inputs and neighborhood transfer on 32 independent perturbations of each edited input (Gaussian noise with coordinate standard deviation 0.1).

At each of the five affine maps, fit a target preactivation via 20 damped gradient steps, then use the **same** fitted target with both rank-one operators: O1 minimizes weight change in Frobenius norm; O2 minimizes the regularized mean squared preactivation change under a separate 512-key calibration distribution. O2 uses the uncentered key second moment plus a ridge of 1% of its mean diagonal. The expected uniform-random choice averages all five layers; the weight-only choice takes the largest raw spectral norm; saliency takes the largest within-layer sum of `|gradient × weight|`; tracing takes the largest recovery of the original prediction under input corruption when restoring a random quarter of the clean input-key coordinates at that map (64 repeats). Full-state restoration would trivially reset the output at any depth in this sequential MLP.

Utility = edit efficacy (fractional reduction in squared error at the edited input) minus retention damage (mean squared prediction drift divided by the squared target offset, 4). Neighborhood transfer is the fractional reduction in neighborhood mean squared error to the new target. The oracle picks the best layer separately for each operator on the same held-out utility used for evaluation; no other chooser sees it.

## Results

Factorial sums of squares, computed within each association and then pooled: **location 39.75%** (39.31–40.24%), **operator 23.67%** (22.58–24.50%), **location × operator 36.58%** (36.10–37.16%). The utility-maximizing layer changed for **99%** (97–100%) of associations when switching operators. This is not a claim that location dominates in general: plain edits had much larger between-layer spread.

| Chooser | O1 regret (utility points × 100) | O2 regret (utility points × 100) |
| --- | ---: | ---: |
| Uniform random (expected) | 16.712 (15.819–17.426) | 0.383 (0.367–0.400) |
| Largest spectral norm | 0.000 (0.000–0.000) | 0.080 (0.075–0.087) |
| Gradient saliency | 8.601 (4.493–13.759) | 0.178 (0.089–0.277) |
| Partial causal trace | 16.151 (11.416–20.241) | 0.398 (0.266–0.503) |
| Oracle | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) |

Mean within-association Spearman between trace score and edit utility: **−0.123** (−0.224 to 0.024) for O1, **+0.027** (−0.112 to 0.209) for O2.

| Layer | O1 neighborhood error reduction (%) | O2 neighborhood error reduction (%) | O1 / O2 retention damage (× 100) |
| --- | ---: | ---: | ---: |
| Hidden 1 | 99.42 (99.39–99.46) | 99.42 (99.39–99.45) | 0.175 / 0.185 |
| Hidden 2 | 99.38 (99.32–99.44) | 99.34 (99.28–99.40) | 1.287 / 0.105 |
| Hidden 3 | 99.38 (99.33–99.43) | 99.28 (99.22–99.35) | 5.954 / 0.240 |
| Hidden 4 | 99.38 (99.32–99.45) | 99.23 (99.16–99.30) | 21.547 / 0.608 |
| Output | 99.34 (99.26–99.45) | 99.15 (99.08–99.21) | 55.475 / 1.300 |

## What this establishes

- Both operators write the same value at the new input and get essentially perfect efficacy. The utility gap comes from what the write does **off that input**. At the output map, where the calibration surrogate and evaluation drift measure the same type of quantity, O2 cut retention drift from 55.47 to 1.30 points (respective CIs 52.36–57.81 and 1.26–1.35). At hidden 1 it slightly *increased* drift, so covariance is not a universally better hidden-state surrogate.
- The spectral norm is a strong fixed-depth baseline here, not evidence of per-edit weight reading: it always chose hidden 1, the O1 oracle in this setup. Multiplying hidden 2's weights and bias by a positive factor and dividing hidden 3's weights by it left predictions unchanged to within `4e-15` yet moved the norm winner to hidden 2 on every seed. This rules out interpreting that raw statistic as an intrinsic address; it doesn't rule out invariant, task-conditioned features computed from weights.
- The trace ranking measures recovery of the **old** output after corruption, not the effects of writing a new value on other inputs. The near-zero correlations are a qualitative analogue of Hase et al.'s localization-versus-editing result, not a replication on factual recall or a test of whether a big model can learn a better chooser. Gaussian neighbors are near ceiling and not semantic paraphrases; isolated edits don't test accumulation or continual forgetting.
