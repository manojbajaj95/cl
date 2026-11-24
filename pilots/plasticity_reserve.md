# Plasticity reserve: kill this write rule

Eight current-loss-matched writes produced measurably different next-task gains, but a regularized unlabeled Gramian log determinant did not predict which writes learned faster. It lost to task-aligned optimization readiness, did not reliably beat current-task readiness, and did not improve final-task learning speed over random selection. Do not scale this rule.

## Did the candidates differ?

In a CPU-only 5×5 ReLU MLP on 50 Slowly-Changing Regression tasks, all 750 writes (5 policies × 3 seeds × 50 tasks) contained eight candidates within **2%** current-task population MSE range. The median range was 0.95%, the maximum 1.97%. Matching backtracked 70.45% of endpoints partway toward the best raw endpoint (median retained fraction 0.5). Thus this tests local, admissible writes rather than unrestricted endpoints.

Across 147 nonterminal writes on the random trajectories, the average within-write range of next-task gain was **4.90 percentage points** (95% CI 3.75 to 6.05), after averaging five adaptation batch orders per candidate. Candidate gain variance, after removing order effects and correcting for the five replicates, was **0.000408** (95% CI 0.000196 to 0.000620), versus **0.000054** candidate-by-order residual variance (95% CI −0.000128 to +0.000235; the t interval is unbounded). There was signal to rank.

The random policy's mean 50-step gain fell from 39.08% on tasks 1–10 to 30.68% on tasks 41–50: **−8.40 pp** (95% CI −18.39 to +1.58). Gain on four fixed independent regression targets also fell, **−6.27 pp** (−15.99 to +3.44). Both decay checks point down but are imprecise; the experiment does not establish a population-level decline.

## Did the score predict later adaptation?

Within-write Spearman correlation with next-task 50-step relative MSE reduction, averaged first within each of the three streams:

| Score or paired difference | Spearman | 95% stream-level t CI | 95% block bootstrap CI |
|---|---:|---:|---:|
| Gramian log determinant | −0.015 | [−0.177, +0.148] | [−0.102, +0.072] |
| Current-task optimization readiness | −0.077 | [−0.437, +0.282] | [−0.253, +0.071] |
| Next-task optimization readiness (labeled oracle) | +0.704 | [+0.590, +0.818] | [+0.621, +0.789] |
| Penultimate feature effective rank | −0.037 | [−0.157, +0.082] | [−0.126, +0.055] |
| Trace-normalized Gramian effective rank | −0.039 | [−0.194, +0.116] | [−0.150, +0.053] |
| **Gramian minus current-task readiness** | **+0.063** | **[−0.272, +0.397]** | **[−0.091, +0.236]** |
| **Gramian minus next-task readiness** | **−0.719** | **[−0.947, −0.491]** | **[−0.839, −0.592]** |

The two readiness arms use the supervised formula from [Wang et al. (2605.09044)](https://arxiv.org/abs/2605.09044): squared mean gradient norm divided by loss, multiplied by that norm divided by the mean squared minibatch gradient norm. The current-task arm sees no future data; the task-aligned oracle gets a separate labeled next-task support draw. Neither Gramian nor feature rank takes labels as input to its score. The Gramian is `JJᵀ` for the scalar model output on 64 fixed random probes: a one-step, local parameter-to-output response under unrestricted Euclidean parameter perturbations, not the target-conditioned, finite-horizon controllability Gramian in [Okanohara (2602.07950)](https://arxiv.org/abs/2602.07950).

## Did the chooser improve learning speed?

Three paired 50-task streams per policy. Gains are relative test MSE reduction after 50 SGD steps; differences are in percentage points. Brackets are 95% stream-level t CIs.

| Chooser | Task 50 gain (%) | Task 50 vs random (pp) | Tasks 41–50 gain (%) | Tasks 41–50 vs random (pp) |
|---|---:|---:|---:|---:|
| Random | 17.35 [−27.44, +62.13] | — | 30.68 [+19.66, +41.70] | — |
| **Gramian** | **14.24 [−38.22, +66.70]** | **−3.11 [−72.41, +66.20]** | **25.81 [+10.90, +40.72]** | **−4.87 [−30.20, +20.46]** |
| Current readiness | 16.25 [−15.09, +47.59] | −1.10 [−29.10, +26.90] | 28.81 [+23.98, +33.64] | −1.87 [−8.07, +4.32] |
| Feature effective rank | 26.28 [−15.51, +68.07] | +8.94 [−28.55, +46.42] | 30.22 [+15.89, +44.56] | −0.45 [−11.52, +10.61] |
| Next readiness (oracle) | 12.98 [−17.34, +43.29] | −4.37 [−32.93, +24.19] | 29.93 [+20.44, +39.42] | −0.75 [−2.36, +0.87] |

The Gramian-minus-random task-50 gain differences were +25.51, −4.61 and −30.22 pp by seed. The Gramian also started task 50 with lower mean MSE (0.1000 vs. 0.1245) and finished the 50 diagnostic steps with lower mean MSE (0.0782 vs. 0.1017), but the paired post-adaptation MSE difference was −0.0235 (95% CI −0.1244 to +0.0774). Relative gain measures speed from each learner's own starting point, not absolute error. The intervals do not rule out either benefit or harm; the kill call is failure to meet the screening bar, not proof the underlying reachability idea cannot work.

## Reproduce

See the [frozen protocol](plasticity_reserve_protocol.md) and [raw traces and summaries](plasticity_reserve_results.json). The held-out sweep took 9.78 s wall time (45.00 summed worker-seconds) on an Intel Xeon CPU with Python 3.10.12, NumPy 2.2.6 and SciPy 1.15.3, using one BLAS thread per worker. The regression stream is generated locally; no download or accelerator is used.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s pilots
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python pilots/plasticity_reserve.py \
  --workers 5 --output pilots/plasticity_reserve_results.json
```
