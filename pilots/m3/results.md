# M3 and R1 CPU pilot results

**M3: kill.** No growing oscillation in 50 seed × lesson traces for keep or
NCA. Mean absolute error grew, but the mean signed error stayed on the
under-dose side. Deleting lessons after the first write did not recover
calibration.

**R1: kill at the reviewer's 15 pp threshold.** Absorption-matched last-cycle
flips fell **42.86 pp** `[−82.86, −2.86]` with keep. This suggests some
erosion, but the interval does not establish a drop of at least 15 pp.

## M3: repeated consolidation

Five seeded runs, ten graded queue policies, three feedback-driven cycles.
Values are in percentage points (pp); brackets are paired 95% seed-bootstrap
intervals. A negative signed error means less movement than the target
calls for, not overshoot.

| Arm | Cycle | Both signed error | Both absolute error | Weights-only absolute error |
| --- | ---: | ---: | ---: | ---: |
| Keep | 1 | −16.59 [−17.39, −15.86] | 29.90 [18.50, 42.14] | 34.40 [24.84, 43.95] |
| Keep | 2 | −18.02 [−18.18, −17.89] | 32.64 [20.19, 45.08] | 32.75 [20.77, 44.73] |
| Keep | 3 | −18.37 [−18.64, −18.10] | 33.75 [22.29, 45.21] | 33.64 [21.88, 45.40] |
| NCA | 1 | −17.51 [−17.85, −17.17] | 22.01 [18.79, 25.41] | 23.83 [20.08, 27.66] |
| NCA | 2 | −18.76 [−19.08, −18.40] | 26.49 [21.51, 31.47] | 27.29 [21.19, 33.39] |
| NCA | 3 | −18.38 [−18.93, −17.96] | 27.01 [21.19, 32.86] | 27.18 [21.18, 33.17] |

- **Manipulation check:** fixed nominal context on the frozen model cut
  calibration error from 33.11 to 21.14 pp (11.96 pp improvement, deterministic
  for this panel). It did shift behavior, but was not itself near-perfect.
- **Growing oscillation:** 0/50 for both arms. The seed and crossed
  seed × lesson bootstrap intervals were both `[0%, 0%]`; a bootstrap
  on zero events is degenerate and cannot bound unseen settings.
  Cycle-3 minus cycle-1 absolute error grew by 3.85 pp `[0.91, 6.79]`
  for keep and 5.00 pp `[0.15, 10.03]` for NCA. This was worsening
  calibration, not growing oscillation. With no oscillation in keep,
  this pilot cannot show that NCA suppresses it.
- **Evict after distilling:** error stayed at the cycle-1 weights-only
  value, 34.40 pp `[24.84, 43.95]`, with no further writes. It was
  13.25 pp worse than nominal context alone `[3.70, 22.81]`, and did not
  improve on the frozen context-free base (gain −1.29 pp `[−10.85, 8.26]`).

The keep arm's weights-only policy was also poorly calibrated at the final
cycle, so this is a stop decision for the pilot, not evidence against
oscillation after strong internalization. The initial A/B-format preflight
was abandoned for a weak nominal-context manipulation (about 1 pp
calibration gain); Yes/No phrasing was selected on development scores before
starting the five-seed result run.

## R1: can a contradicting lesson still flip the decision?

Raw flip rates are conditional on weights-only choosing the old action.
Absorption is the mean change from the frozen base in probability of that
action across all disagreement probes. Both are in pp.

| Arm | Cycle | Raw flip rate | Weights-only absorption |
| --- | ---: | ---: | ---: |
| Keep | 1 | 31.33 [10.00, 52.67] | +0.05 [−0.23, +0.33] |
| Keep | 2 | 17.76 [2.86, 32.66] | +0.40 [+0.27, +0.53] |
| Keep | 3 | 0.00 [0.00, 0.00] | +0.44 [+0.21, +0.66] |
| NCA | 1 | 17.31 [4.29, 30.34] | −0.19 [−0.47, +0.09] |
| NCA | 2 | 4.00 [0.00, 12.00] | +0.38 [+0.24, +0.54] |
| NCA | 3 | 4.00 [0.00, 12.00] | +0.09 [−0.24, +0.41] |
| Lower LR | 1 | 28.33 [23.19, 34.33] | −0.29 [−0.31, −0.27] |
| Lower LR | 2 | 28.57 [21.33, 36.38] | −0.47 [−0.65, −0.34] |
| Lower LR | 3 | 29.61 [20.80, 35.24] | −0.45 [−0.62, −0.25] |

| Arm | Cycle 1 → 3 matched flip rate | Paired change | Matched probes by seed |
| --- | ---: | ---: | --- |
| Keep | 42.86 → 0.00 | −42.86 [−82.86, −2.86] | 1, 13, 1, 7, 15 |
| NCA | 9.00 → 4.00 | −5.00 [−19.00, +8.00] | 9, 8, 5, 5, 5 |
| Lower LR | 55.00 → 65.00 | +10.00 [0.00, +30.00] | 1, 1, 0, 5, 1 |

The keep arm's matched absorption changed by only +0.34 pp
`[−3.45, +4.14]`. Its cycle-2 matched flip change was −31.25 pp
`[−75.00, 0.00]`. The decline from cycle 1 to 3 clears zero but not
the prespecified −15 pp bound, and matching left only one probe in two
seeds. We ran the controls because a decline was detectable:

- **Lower LR** retained raw flips and did not lose them on its small
  matched panel. Against keep at cycle 3 on common support its flip rate
  was higher by 20.00 pp `[0.00, 60.00]` (12 probes in three seeds).
  This is suggestive, not a robust preservation result at equal absorption.
- **NCA** had a weaker decline on its own matched panel but already
  started with a low flip rate and ended at 4%. Only one seed had
  cycle-3 common support with keep, so preservation relative to keep
  is not established.

The main and lower-LR runs produced 300 and 150 complete lesson-cycle
records in 1,196.6 and 658.7 seconds, respectively, on eight CPU threads.
See [the protocol and commands](README.md) to regenerate the traces and CIs.
