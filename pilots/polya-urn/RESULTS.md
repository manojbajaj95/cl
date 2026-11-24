# P1: KILL at the comparator gate

The matched 100-step two-order comparator ranked all eight [PR #11](https://github.com/manojbajaj95/cl/pull/11) policies in the correct order at both 200 and 1,000 updates. Its long-horizon Spearman ρ was **1.000 [0.976, 1.000]**; degradation was **0.000 [−0.024, +0.024]**. There is no room for a +0.20 ρ improvement on this panel. Per the [fixed protocol](PROTOCOL.md), stop here: κ estimation, the γ sweep, the success-blind ablation and the common-suffix control were **not run**.

## Has rank prediction degraded?

The target is the mean of six pairwise RMS distances in action probability on fixed probes. Spearman ρ ranks the eight policy means over 48 paired streams. Brackets are 95% paired seed-bootstrap CIs, conditional on the policy panel.

| Two-order predictor | ρ at target step 200 | ρ at target step 1,000 | Degradation (200 minus 1,000) |
|---|---:|---:|---:|
| 20 steps per order | 0.952 [0.881, 0.952] | 0.952 [0.881, 0.952] | 0.000 [−0.071, +0.071] |
| **100 steps per order** | **1.000 [0.976, 1.000]** | **1.000 [0.976, 1.000]** | **0.000 [−0.024, +0.024]** |

Resampling policies as well as seed blocks did not change the decision: matched degradation CI [0.000, 0.000], with the long-horizon ρ CI [0.976, 1.000]. The discrete ranks and small policy panel limit what either interval says about unseen policies. All 10,000 bootstrap draws were valid.

## What happened to the motivating crossover?

First order pair only, using the same pair at each horizon; the difference CIs are paired over streams. Levels and changes are in RMS action-probability units.

| Policy | Step 20 | Step 200 | Step 1,000 | Change 20→200 [95% CI] | Change 200→1,000 [95% CI] |
|---|---:|---:|---:|---:|---:|
| Utility eviction | 0.187 | 0.351 | 0.343 | +0.165 [+0.136, +0.193] | −0.009 [−0.040, +0.023] |
| Gated consolidation | 0.090 | 0.199 | 0.202 | +0.109 [+0.089, +0.129] | +0.002 [−0.016, +0.021] |
| FIFO | 0.219 | 0.220 | 0.203 | +0.001 [−0.014, +0.016] | −0.017 [−0.032, −0.002] |

Utility eviction passed FIFO by step 200, but both success-coupled policies showed no detectable further growth through step 1,000. Other policies also had some early growth (full results below), making growth alone nonspecific. This is not a no-decay or causal ablation: the stock utility rule discounts the matched entry on use, and the final probes can reflect recency. Neither an urn mechanism nor γ's effect is identified by this stop screen.

## Reproduce

[Raw policy–seed rows](runs.csv) · [Full estimates and CIs](results.json) · [Protocol](PROTOCOL.md)

From a clone that has the PR #11 commit (if missing, run `git fetch origin refs/pull/11/head`), with Python 3.10.12, NumPy 2.2.6 and SciPy 1.15.3:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python pilots/polya-urn/gate.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s pilots/polya-urn -v
```

The full run took 53 seconds on one CPU thread. Each policy–seed unit used 4,000 transitions for target generation; both direct comparators reuse prefixes of those runs. Only the two relevant short prefixes are charged to the 100-step predictor, not the validation targets.
