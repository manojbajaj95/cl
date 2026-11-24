# Plasticity reserve follow-up: kill at the absolute-gain gate

The eight writes differed by **1.098 absolute MSE points** in the original setup and **0.091 points** after matching retention and projecting next-task updates. Both 95% CIs are entirely below the requested **1.5-point** minimum. Stop before scoring: no projected Gramian, optimization-readiness, or forecast-weighted choices were run. This screens out the candidate pool and assay, not the scores themselves.

## Gain spread across eight candidates

For each write, average each candidate's test-loss reduction over five common adaptation orders, then take the range across candidates. Average over the 49 nonterminal writes per stream. Intervals are 95% Student t intervals across 512 stream seeds (101–612), not across individual writes. Absolute MSE points are `100 × (MSE before − MSE after)`, without dividing by starting MSE; the floor is 0.015 raw MSE. Relative gain instead divides by each candidate's own starting MSE before computing the range.

| Candidate match and next-task learner | Relative gain spread (pp) | Absolute gain spread (MSE points) |
|---|---:|---:|
| Original: current loss only, plain SGD | 4.757 [4.708, 4.807] | 1.098 [1.077, 1.119] |
| Current loss only, projected SGD, at the jointly matched checkpoints | 2.176 [2.135, 2.217] | — |
| Current loss and prior retention, projected SGD | **0.458 [0.448, 0.468]** | **0.091 [0.088, 0.093]** |
| Paired change from adding retention matching under the same projection | −1.718 [−1.753, −1.683] | — |

On the exact [PR #9](https://github.com/manojbajaj95/cl/pull/9) seeds (101–103), the replay reproduces the **4.899 pp [3.751, 6.046]** relative range; its absolute range was **1.171 MSE points [0.695, 1.647]**. The expanded sweep puts even the original absolute range below the gate. This is a scale-sensitive finding: it does not establish that differences in the relative-gain denominator alone produced the original spread. The matched/projected candidates still show a small real difference: the order-corrected absolute candidate variance was `6.27e−7 [5.22e−7, 7.33e−7]` in squared raw MSE units, versus `1.51e−7 [1.00e−7, 2.01e−7]` candidate-by-order residual variance. The spread failed on practical size, not on an inability to distinguish it from order noise.

Across the 25,088 matched decision points, the maximum current-loss range was 1.930% and the maximum range on any individual prior task was 1.998%, both under the 2% cap. The extra matching step backtracked 82.0% of endpoints. The current-only comparison uses the same checkpoints, projection and adaptation draws as the jointly matched candidates, isolating the additional matching step there; the original plain-SGD replay uses its own current-only trajectory. The projection removes stored first-order loss directions; it is not a guarantee of unchanged retention after adaptation.

## Reproduce

See the [protocol](plasticity_retention_protocol.md). The CPU-only sweep took 434 seconds with eight workers and one BLAS thread per worker (Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3). The JSON output contains all per-seed summaries as well as the aggregate CIs and gate decision.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s pilots
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python pilots/plasticity_retention.py \
  --workers 8 --output "$HOME/plasticity-retention-gate.json"
```
