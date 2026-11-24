# Memory-loop Lyapunov pilot: KILL

Do not scale up this estimator. Across eight update designs × three seeds, early λ ranked 200-update order dependence worse than the 20-update two-order control: **Δρ = −1.286 (95% CI [−1.975, +0.099])**, missing the required **+0.30** margin. λ also lost to the growth, edit and convergence baselines. The initial-memory signal was distinguishable **below** the seed-only floor, not above it: mean early divergence was 0.000140 vs. 0.143732 (about 1,029× smaller); paired gap **−0.144 [−0.182, −0.102]**.

## Predicting endpoint order dependence

The target is mean pairwise RMS behavioral distance across four matched task orders at 200 updates. Values are Spearman ρ [95% paired bootstrap CI], across design means (primary) and individual design–seed units (secondary).

| Predictor | 8 design means | 24 design–seed units |
|---|---:|---:|
| 20-update λ | −0.381 [−1.000, +0.595] | −0.228 [−0.834, +0.570] |
| 20-update two-order divergence | +0.905 [+0.235, +1.000] | +0.705 [+0.102, +1.000] |
| **λ minus two-order control** | **−1.286 [−1.975, +0.099]** | **−0.933 [−1.682, +0.203]** |
| Entry growth rate / final entry count | −0.150 [−0.874, +0.871] | −0.218 [−0.854, +0.747] |
| Existing-entry edit rate | +0.434 [−0.519, +0.981] | +0.409 [−0.422, +0.899] |
| Shadow convergence non-declaration | +0.000 [−0.871, +0.871] | −0.065 [−0.651, +0.441] |
| Shadow convergence declaration level | +0.180 [−0.714, +0.975] | +0.146 [−0.603, +0.845] |
| Shadow draft rejection rate | −0.551 [−0.981, +0.392] | −0.464 [−0.930, +0.280] |

For the secondary endpoint (clean accuracy spread across the four final orders), design-level ρ was −0.333 [−0.975, +0.595] for λ and +0.857 [+0.089, +1.000] for the direct control (paired Δρ −1.190 [−1.923, +0.125]). Pooled Δρ was −1.004 [−1.659, +0.040]. [Raw results](results.json) include all coefficients and intervals, valid bootstrap counts, trajectories, and per-order accuracies.

## Perturbation vs. loop-seed noise

Means over updates 1–20, averaged across seeds per design. Gap is perturbed minus seed-only RMS distance with a paired 95% CI.

| Design | Mean λ / update | Final order distance | Perturbed RMS | Seed-only RMS | Gap [95% CI] |
|---|---:|---:|---:|---:|---:|
| Append | −0.029 | 0.028 | 0.000152 | 0.149 | −0.149 [−0.176, −0.129] |
| FIFO | −0.692 | 0.196 | 0.000071 | 0.169 | −0.169 [−0.196, −0.153] |
| Utility eviction | −0.014 | 0.417 | 0.000165 | 0.196 | −0.196 [−0.214, −0.182] |
| Similarity merge | −0.019 | 0.110 | 0.000172 | 0.116 | −0.116 [−0.160, −0.039] |
| Summary rewrite | −0.103 | 0.126 | 0.000087 | 0.054 | −0.054 [−0.083, −0.026] |
| Reflection | −0.006 | 0.061 | 0.000200 | 0.092 | −0.092 [−0.103, −0.087] |
| Gated consolidation | −0.245 | 0.195 | 0.000158 | 0.169 | −0.169 [−0.196, −0.154] |
| High-gain rewrite | −0.326 | 0.321 | 0.000112 | 0.205 | −0.205 [−0.256, −0.142] |

All design means had negative λ despite appreciable order effects (e.g., FIFO and high-gain rewrite); only one individual λ was positive (+0.00047). Eight trajectories hit the log floor. Mean expected clean accuracy improved from the common 0.522 start for six designs, not for summary rewrite or reflection. Local contraction under matched forcing is not the same claim as invariance to changing the forcing order. The endpoint still includes recency from the last task block, the convergence signals are proxies, and the direct control already sits near its rank-correlation ceiling. These results kill this pilot at the requested gate; they do not establish what happens in an LLM memory loop or after a common final replay.

## Reproduce

See the [fixed protocol](PROTOCOL.md). From the repository root, with Python 3.10.12, NumPy 2.2.6, and SciPy 1.15.3:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python pilots/lyapunov/experiment.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s pilots/lyapunov -v
```
