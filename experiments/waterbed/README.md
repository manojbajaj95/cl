# A CPU test of the forgetting waterbed

Test whether the mean log-gain from task-mixture modulation to old-task
squared loss is invariant at matched final accuracy. Compare the raw area
with Jensen's prediction and repeat after dividing by the one-step gain.

## Run

From the repository root, with Python 3, NumPy (2.x), SciPy, and Matplotlib:

```sh
OPENBLAS_NUM_THREADS=1 python3 experiments/waterbed/run.py --self-test
OPENBLAS_NUM_THREADS=1 python3 experiments/waterbed/run.py
```

The full run writes `results.json` (seed-level arrays, summaries, parameters,
environment, runtime) and `frequency_response.pdf`. The optional `--output`
argument selects an existing output directory.

## Protocol

- Eight paired seeds define conflicting unit-variance linear teachers in a
  four-dimensional Gaussian input space. Both layers of a width-one linear
  student train from the same balanced task-A solution. Use expected gradients
  for the incoming mix to isolate the small-signal response, not minibatch noise.
- Compare two SGD learning rates, 10% replay from a finite fixed A cache
  (its exact empirical gradient), and diagonal EWC anchored at the task-A fit.
  The EWC diagonal is the second moment of the squared-loss gradient at the
  A fit under Gaussian observation noise (the Gaussian model's Fisher
  rescaled by the squared noise variance). All arms take one parameter update
  per step; replay additionally uses a cached sufficient statistic.
- Warm up at mixture 1/2, then drive at amplitudes 0.01 and 0.02. Quantize a
  log grid to Fourier bins; cosine phase includes Nyquist without degeneracy.
  Read old-task loss before each update and use the settled lock-in amplitude
  divided by drive amplitude. Use the lower amplitude for primary results.
- Compute area as the average of natural log-gain over frequency, integrating
  the shape-preserving interpolant of logs and using a flat extension to DC
  below the first sampled bin. Also preserve the area without this extension.
  Report range divided by mean absolute area (20% kill threshold), and the
  geometric-mean gain ratio, which does not depend on shared loss units.
- Accuracy is exact sign agreement with each clean teacher under held-out
  population inputs. Match the terminal average of the two task accuracies
  within 1 percentage point over paired seeds, amplitudes and frequencies.
  Report A accuracy separately, and report both unforced task losses so the
  comparison does not conflate matched accuracy with matched MSE. Mean
  forgetting is the old-task loss increase from the task-A fit, averaged over
  settled steps and then across equally weighted sweep frequencies.
- Report paired seed-level contrasts and Student-t 95% intervals around
  across-seed means. Plot ribbons are pointwise intervals on log-gain, not
  simultaneous bands. Compare measured areas against both dense LTI
  integration and the exact Jensen prediction.

## Result

At drive amplitude 0.01 (eight seeds, 55 frequencies):

| Method | Measured mean log-gain | Jensen prediction | Mean A loss | Final A accuracy |
| --- | ---: | ---: | ---: | ---: |
| SGD (0.025) | -4.7162 | -4.7161 | 0.10137 | 85.31% |
| SGD (0.150) | -2.9345 | -2.9311 | 0.10138 | 85.39% |
| Replay | -3.8237 | -3.8231 | 0.08262 | 86.91% |
| EWC | -3.9314 | -3.9315 | 0.04462 | 90.72% |

**The raw-area claim fails in this rig.** Across-method range is 46.26% of
the mean absolute log-area, above the 20% kill threshold; the geometric-mean
gain ratio is 5.94. The maximum matched terminal joint-accuracy gap is
0.00082 percentage points, with joint accuracy about 85.22% for all arms.
This aggregate is insensitive to redistributing accuracy between the two
teachers; individual A and B accuracies are not matched across methods.
The SGD pair alone exceeds the kill threshold (46.58%) and has the same
unforced predictions and per-task losses. Fast SGD has higher raw gain than
slow SGD at every sampled frequency and seed. Mean A forgetting varies by
2.27× across arms.

**The normalized area agrees with the local LTI explanation.** For
\(S(z)=c^\top(zI-M)^{-1}b\), the first Markov coefficient is \(c^\top b\).
For a stable scalar transfer with nonzero first coefficient, Jensen's formula
gives the mean log-gain as its log absolute value plus the sum of
\(\log |z_k|\) over finite zeros outside the unit circle, including
multiplicity. The measured areas differ by at most 0.00642 from this
prediction over seeds and arms; the dense LTI integral agrees within
\(9\times10^{-16}\). All fitted zeros lie inside the unit circle (max
modulus 0.9852); after division by one-step gain, the largest per-seed
cross-method area range is 0.00644. The response changes by at most 3.89%
when doubling amplitude. This is a local and conditional result, not a
law for stochastic training or a guarantee that normalized area is conserved
when zeros leave the unit circle.

For comparison, in scalar least squares with unit input variance, plain
gradient descent gives a pole at \(1-\eta\) and one-step coefficient
proportional to \(\eta\) at the same mixed-task optimum. For
\(0<\eta<1\), decreasing \(\eta\) lowers raw gain at every non-DC
frequency while preserving the optimum. Thus the general raw-area
invariance cannot follow from stability or matched final fit alone.

## Prior-art check

Searches on 2026-11-25 combined “Bode,” “continual learning,” “catastrophic
forgetting,” “switching,” and “sensitivity integral,” then broadened to
cyclic forgetting and frequency-domain tracking in time-varying optimization.
Closest inspected work:

- [Discrete-time Bode sensitivity integral constraints](https://arxiv.org/abs/1903.01225)
  and [complementary sensitivity integrals](https://arxiv.org/abs/1811.09884):
  the log-integral machinery is classical; the task-mixture to old-task
  loss transfer is not the canonical feedback sensitivity.
- [Temporal Variabilities Limit Convergence Rates in Gradient-Based Online
  Optimization](https://arxiv.org/abs/2510.12512) and [Convex Synthesis of
  First-Order Methods for Time-Varying Smooth Strongly Convex
  Optimization](https://arxiv.org/abs/2604.09926): frequency-domain and
  control analyses of tracking a moving optimizer, not an old-task loss
  readout.
- [Understanding Forgetting in Continual Learning with Linear
  Regression](https://arxiv.org/abs/2405.17583) analyzes step size and order;
  [Nearly Optimal Bounds for Cyclic Forgetting](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d72ae75abaa70a3b19c5d4f436c680d1-Abstract-Conference.html)
  bounds forgetting under repeated task projections. Neither studies a
  sinusoidal mixture-to-loss transfer integral.
- [Reawakening Knowledge](https://arxiv.org/abs/2403.09613) measures
  recovery under cyclic document training, [Continual Learning through
  Control Minimization](https://arxiv.org/abs/2602.04542) uses control to
  design a learner, and [MathBode](https://arxiv.org/abs/2509.23143)
  drives problem parameters to probe model reasoning, not learning or forgetting.

This is a provisional novelty check on the diagnostic and falsification,
not a claim of new control theory or exhaustive coverage.
