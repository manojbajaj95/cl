# A CPU test of dirty-paper writes

Top-10 idea #6: precode a new task's update against the known old weights
(Costa's dirty-paper coding) instead of projecting it away from them, and
compare with GPM/OWM projection at equal update norm. Kill bar: no gain over
GPM, with old-task accuracy as the primary metric.

## Run

From the repository root, with Python 3, NumPy (2.x) and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python3 experiments/dirty_paper/run.py --self-test
OPENBLAS_NUM_THREADS=1 python3 experiments/dirty_paper/run.py              # ~7 CPU-min
OPENBLAS_NUM_THREADS=1 python3 experiments/dirty_paper/run.py --summarize-only
```

The full run writes `results.json` (parameters, per-seed norms, accuracy and
decay curves, summaries, environment, runtime). `--summarize-only` recomputes
the summary from the saved seeds.

## Protocol

- Two-layer ReLU MLP (16 → 64 frozen features → scalar readout). Labels are
  residues mod 8 and the readout is decoded mod 8: the one decoder for which
  dirty-paper coding applies. Old task A: 24 items, old weights interpolate
  `t_A + 8L` with `L` uniform on `{-S..S}` (S = 0 or 4). New task B: 16 items,
  each at angle 15/30/60/90 degrees from a distinct A item. 16 seeds each.
- Writes: FT, GPM (hard projection), OWM (soft projection), GPM + gradient
  descent on the periodic loss (strongest matched baseline), and three
  dirty-paper precoders: THP (coordinatewise wrap), A-null vector
  perturbation (closest-vector coset point, LLL + Schnorr–Euchner) and a joint
  precoder that may move A's outputs by whole periods.
- Equal update norm: 15 budgets from 0.05 to 1.5 times GPM's exact-write norm.
  Pre-registered decision (fixed before the first sweep): budget-averaged B
  accuracy of the best dirty-paper arm, credited only where its A accuracy is
  within 1 pp of GPM's, minus the best projection arm; killed unless the 95%
  t-interval is above 0 and the mean is at least 1 pp.
- Post hoc (not in the decision): interference-free reference writes, weight
  shrink half-lives for A and B, and a switched write (joint precoder when the
  budget covers its exact norm, modular GD otherwise).

## Result

Killed in 7 of 8 configurations, including the main one (θ = 30°, S = 0:
−0.91 pp, 95% CI −1.89 to 0.06). Known interference is free for the precoder
(norm 0.96–1.07× an interference-free write), but GPM with modular descent
recovers most of the saving, no A-null write can beat GPM's 100% old-task
accuracy, and the joint precoder (0.54–0.80× modular descent's norm) drops
old-task accuracy to 14% when the budget is short. See `papers/dirty-paper/`.
