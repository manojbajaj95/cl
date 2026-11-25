# ED08 Body-Curvature CPU Pilot — Results

**Verdict: PASS** (10/10 pre-registered gates cleared on CPU with analytic simulated bodies; see caveats below).

- **Source spec:** `tree/embodied-learners-4.md` (PR #398), ED01–ED05, ED07, ED08; reviewer bar in `reviews/flood-triage.md` (row 561).
- **Scope:** CPU-only simulated-body pilot (`N_SEEDS = 24`, `N_RITUAL = 400`, `N_EVAL = 200`, `REL_NOISE_STD = 0.0005`, loop sizes `{0.10, 0.15, 0.20}`, runtime `68.2 s` on 8 CPU cores). No GPU; ED10 (`Gamma` vs RMA) is out of scope for this pilot.
- **Reproduce:**
  ```bash
  python3 -u pilots/ed08_body_curvature/pilot.py
  python3 -m unittest discover -s pilots/ed08_body_curvature -p "test_*.py" -v
  ```

---

## 1. Estimator & Simulated Bodies

### Calibrated Function-Space Curvature Estimator (`estimator.py`)
Naive round-trip loop holonomy $\|u_{\text{fwd}} - u_0\|$ fails calibration for two independent reasons:
1. **Round-trip projection bias:** Even on a flat pair like `(k1, m1)`, projecting the nonlinear step `m1 -> m1 + dm1` onto an action-space affine transport produces nonzero symmetric round-trip error (`F_raw > 0`).
2. **Squared-norm noise bias:** Under observation noise $\epsilon$, $\mathbb{E}[\|d + \epsilon\|^2] = \|d\|^2 + \sigma^2 > 0$, making flat loops read strictly positive.

Our calibrated estimator eliminates both biases in function space:
- **Orientation-reversed antisymmetrization:** For every rectangular loop $(p_{00}, p_{10}, p_{11}, p_{01})$, transport evaluation actions around both the forward loop and the reversed loop and take $d = \tfrac{1}{2}(u_{\text{fwd}} - u_{\text{rev}}) / (\Delta u\,\Delta v)$, cancelling all symmetric round-trip artifacts to machine precision (`< 1e-13` on clean flat loops).
- **Cross-fitted split-ritual inner product:** Split the ritual dataset into two disjoint halves (`200 / 200` states), fit independent transport loops $d^{(1)}, d^{(2)}$, and compute the unbiased squared curvature
  $$F^2_{\text{cal}} = \frac{\frac{1}{N_{\text{eval}}} \sum_{i} \langle d^{(1)}_i, d^{(2)}_i \rangle}{\frac{1}{N_{\text{eval}}} \sum_{i} \|u_{\text{eval}, i}\|^2}, \qquad \hat{F}_{\text{cal}} = \sqrt{\max(0, \overline{F^2_{\text{cal}}})}.$$

### Simulated Bodies (`bodies.py`)
Pure NumPy/SciPy analytic rigid-body models (VM has no PyTorch/MuJoCo/Gymnasium):
1. **2-link planar manipulator (ED01, ED02, ED05, ED07):** Exact Lagrangian $M(q)\ddot{q} + C(q,\dot{q})\dot{q} + G(q) = \tau$, independent joint gains $(k_1, k_2)$, masses $(m_1, m_2)$, link lengths $(l_1, l_2)$, end-effector payload $m_p$, smooth `tanh` or hard `clip` torque saturation, and optional Froude time scaling ($\dot{q} \propto L^{-1/2}, \ddot{q} \propto L^{-1}$).
2. **Planar pusher with Coulomb friction (ED04):** Smooth stick/slip transition over a $6 \times 6$ grid of friction $\mu \in [0.15, 0.85]$ and object mass $m_{\text{obj}} \in [0.8, 3.2]$.
3. **SLIP hopper apex map (ED03):** Smooth stance-dominated vs flight-dominated gait switch over a $6 \times 6$ grid of body mass $m \in [1.0, 4.2]$ and leg length $l_0 \in [0.75, 1.40]$.

---

## 2. Unified ED08 Gate Summary

| Gate | Requirement | Measured | Pass |
|---|---|---|---|
| Flat vs curved AUROC | $\ge 0.90$ | Pooled **1.0000**; per-seed mean **0.9210** `[0.8934, 0.9464]` (11 flat vs 14 curved) | PASS |
| Flat reads zero | 95% CI contains 0 | Pooled exact-flat $F^2_{\text{cal}} = -1.59\times 10^{-6}$ `[-8.46e-6, +5.74e-6]`; max flat $\hat{F} = 0.0035$ vs min curved $\hat{F} = 0.0101$ | PASS |
| Split-half reliability (seeds) | $\ge 0.80$ | Spearman $\rho = \mathbf{0.9091}$, Pearson $r = \mathbf{1.0000}$ | PASS |
| Split-half reliability (rituals) | $\ge 0.80$ | Spearman $\rho = \mathbf{0.9939}$, Pearson $r = \mathbf{0.9978}$ | PASS |
| Loop-size reliability (`0.10, 0.15, 0.20`) | $\ge 0.80$ | Min Pearson $r = \mathbf{0.9973}$ (min Spearman $\rho = 0.7597$ due to tie-breaking among 9 zero-mean flat pairs) | PASS |
| ED01 15-pair arm pattern | $\ge 12/15$ | **15/15** exact matches (9/9 flat gain pairs = 0; 6/6 curved inertial pairs > 0) | PASS |
| ED02 torque saturation (`tanh`) | Monotonic $\rho \ge 0.85$ | Spearman $\rho = \mathbf{0.964}$ (`0.0011` at $u_{\max}=\infty$ $\to$ `0.8146` at $u_{\max}=12$) | PASS |
| ED03 hopper gait boundary | IoU $\ge 0.50$, AUROC $\ge 0.90$ | Unsupervised IoU = **0.700**, grid AUROC = **0.966**, boundary/within ratio = **6.3x** | PASS |
| ED04 pusher contact switch | Ratio $\ge 3\times$ | Mode-crossing / within-mode ratio = **24.4x** (`0.0491` vs `0.0020`) | PASS |
| ED05 constant-Froude scaling | Ratio $\le 20\%$ | Matched `(froude_L, l2)` Froude/length-only ratio = **0.0000** (`F_clean = 4.1e-14` vs `0.0196`) | PASS |

---

## 3. Per-Experiment Breakdown

### ED01 (15-Pair Arm Table) & ED05 (Constant-Froude Scaling)
- **All 9 gain-involving pairs** (`k1_k2, k1_m1, k1_m2, k1_l2, k1_mp, k2_m1, k2_m2, k2_l2, k2_mp`) have $F_{\text{clean}} < 10^{-13}$ and 95% CIs on $F^2_{\text{cal}}$ containing 0 (`max F_cal_unbiased = 0.0035`).
- **All 6 inertial pairs** read strictly positive above their 95% CIs: `m1_l2` (`0.139`), `l2_mp` (`0.083`), `m2_l2` (`0.047`), and the three pure-mass pairs `m1_m2`, `m1_mp`, `m2_mp` (`0.010–0.012`).
- **ED05 matched Froude test:** On the identical parameter loop `(froude_L, l2)`, enabling Froude time-scaling collapses curvature from `F_cal = 0.0176` (`F_clean = 0.0196`) to `F_cal = 0.0000` (`F_clean = 4.12e-14`, 95% CI on $F^2_{\text{cal}}$ `[-4.15e-5, +3.62e-6]`).

### ED02 (Torque/Command Saturation on Flat `k1 x k2`)
- **`tanh` saturation:** Curvature rises monotonically from `0.0011` (`u_max = inf`, CI straddles 0) to `0.0174` (`80`), `0.0726` (`50`), `0.0779` (`35`), `0.2229` (`25`), `0.4501` (`18`), and `0.8146` (`12`); Spearman $\rho = 0.964$.
- **Caveat — hard `clip` saturation:** Hard rail clamping is non-monotonic ($\rho = 0.464$) because piecewise-constant dead zones make global affine transport fits degenerate once a large fraction of ritual states saturate to the rail.

### ED07 (Function-Space vs Weight-Space Invariance: 2 Archs × 2 Optimizers)
Tested `MLP` and `RBF` policies distilled with `L-BFGS-B` and `Adam` (8 seeds each) on `flat_k1_k2`, `curved_m1_l2`, and `sat_k1_k2`:

| Distillation mode | `curved_m1_l2` across-cfg std (fn) | `curved_m1_l2` within-seed std (fn) | `curved_m1_l2` across-cfg std (wt) | `flat_k1_k2` max (fn) | `flat_k1_k2` max (wt) |
|---|---|---|---|---|---|
| `action_transport_distill` | **0.0219** | 0.0224 | 0.4266 (19.5× worse) | 0.0879 | 0.8185 |
| `full_inverse_distill` | 0.3807 | 0.0962 | 3.9597 | 0.0879 | 0.8185 |

- Under `action_transport_distill`, function-space across-architecture/optimizer variation (`0.0219`) is smaller than within-seed variation (`0.0224`), whereas weight-space curvature varies `19.5×` more (`0.4266`) and reads large false curvature (`0.8185`) on the flat `k1 x k2` loop.

### 1% Relative Sensor-Noise Stress Test (SNR Floor)
At `REL_NOISE_STD = 0.01` (20× higher noise than primary) with the same `N_RITUAL = 400`, dividing holonomy by $\text{Area} = \Delta u\,\Delta v = 0.0225$ raises the $F^2$ variance floor to $\sim 10^{-3}$, burying the three small pure-mass pairs (`m1_m2, m1_mp, m2_mp`, $F \approx 0.011$): ED01 drops to `11/15` and loop-size Pearson $r$ drops to `0.14–0.72`, while ED05 Froude ratio stays `0.0000`. Resolving $F \sim 0.01$ under 1% noise requires proportionally larger ritual budgets ($N_{\text{ritual}} \propto \sigma^2 / (\text{Area}^2 F^4)$).

---

## 4. Limitations & Next Step
1. **Analytic CPU simulators:** The VM lacked MuJoCo/PyTorch/Gymnasium, so ED01–ED05 and ED07 were run on exact analytic NumPy/SciPy rigid-body models and NumPy MLP/RBF policies rather than full physics-engine RL rollouts.
2. **Hard-clip saturation & 1% noise floor:** Hard-clip dead zones degrade global affine transport, and 1% sensor noise buries small pure-mass curvature at `N_RITUAL = 400`.
3. **Next gate (not run here):** ED10 (`Gamma` vs fairest RMA on curved body transitions) is now unlocked by this ED08 PASS.
