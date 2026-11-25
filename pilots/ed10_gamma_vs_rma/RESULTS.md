# ED10 Body-Connection (Γ) vs Fairest RMA CPU Pilot — Results

- **Source spec:** `tree/embodied-learners-4.md` (PR #398, ED10) & reviewer score-4 bar (`reviews/flood-triage.md`, row 561)
- **Prerequisite:** ED08 body-curvature CPU pilot ([PR #409](https://github.com/manojbajaj95/cl/pull/409), PASS 10/10 gates)
- **Verdict:** **PASS** (6/6 gates; curved 1% noise gap **+8.22 SE**, curved 2% noise stress gap **+12.95 SE**)
- **Runtime:** 246.1s on CPU (8 workers, MuJoCo 3.17.0, NumPy/SciPy, 16 paired seeds at 1% noise + 8 paired seeds at 2% noise)

## Protocol

1. **Bodies (MuJoCo 3.17.0 2-link vertical-plane arm, RK4 `dt=0.01s`, gravity `-9.81 m/s²`):**
   - **Flat family (`A, B, C, D`):** identical mass/length/payload, varying only unsaturated actuator gains `(k1, k2)` (`u_max = 200`).
   - **Curved family (`A, B, C, D`):** varying link masses `(m1, m2)`, link lengths `(l1, l2)`, distal payload `mp`, and actuator gains `(k1, k2)` (`u_max = 250`).
   - **Sensor noise:** **1% relative Gaussian noise** on `(q, qd)` during all rollouts and on `(q, qd, qdd)` during ritual collection (primary); **2% relative Gaussian noise** stress test.
2. **Continual-learning schedule:**
   - **Rituals:** 1,200 task-agnostic noisy transitions `(q, qd, u -> qdd)` per body (identical dataset shared across all arms; no XML parameters exposed).
   - **Phase 1 (old skills `S1..S4`):** 8 noisy expert episodes × 80 steps per `(body, skill)` across all four bodies `A, B, C, D`.
   - **Phase 2 (new skill `S5`):** 8 noisy expert episodes × 80 steps **ONLY on body `B`**.
   - **Evaluation:** zero-shot `S5` tracking return `exp(-4 * MSE)` and joint-space RMSE on held-out bodies `{A, C, D}` (6 noisy episodes/body) + old-skill retention `S1..S4` across all four bodies `{A, B, C, D}`.
3. **Arms (identical ritual & demonstration budgets):**
   - **Gamma (`Γ`):** state-dependent function-space connection fitted purely from noisy rituals via ridge regression on a task-agnostic periodic-in-$q$ × quadratic-in-$\dot q$ dynamics basis (`qdd = B(q) u + f(q, qd)`), transporting `u_B -> u_dst` by matching predicted acceleration with Tikhonov damping `1e-3`.
   - **EB12:** state-independent global affine action conjugator `u_dst = A u_B + b` fitted from the same ritual dynamics.
   - **RMA_replay (fairest RMA, full fine-tune):** 64-unit shared skill trunk + hidden FiLM body modulator + explicit `2x2` output-level body affine head conditioned on 6D ritual SVD body latents `z_b`, trained on `S1..S4@{A..D}` then fine-tuned with L-BFGS-B (`maxiter=350`) on `S5@B` (4× weighted) + full `S1..S4@{A..D}` replay.
   - **RMA_frozen_body (fairest RMA, frozen body head):** identical architecture and Phase 1 weights, freezing all body modulators (`Wg, bg, Wb, bb, WA, bA, Wd, bd`) during Phase 2 while fine-tuning the skill trunk on `S5@B` + `S1..S4` replay.
   - **NoTransport:** `S5@B` skill policy deployed directly on `{A, C, D}`.
   - **Expert:** exact MuJoCo computed-torque ceiling under the same sensor noise.

## Primary Results (1% Sensor Noise, 16 Paired Seeds)

### Curved Family — `S5` Zero-Shot Transfer to `{A, C, D}` & `S1..S4` Retention

| Arm | `S5 @ {A,C,D}` Return (↑) | `S5 @ {A,C,D}` RMSE (↓) | `S5 @ B` (train) | `S1..S4` Retention (↑) |
|---|---:|---:|---:|---:|
| **Gamma (Γ)** | **0.8791 ± 0.0149** | **0.1705 ± 0.0111** | 0.9536 ± 0.0050 | **0.9016 ± 0.0099** |
| EB12 (flat conjugator) | 0.8003 ± 0.0130 | 0.2309 ± 0.0087 | 0.7653 ± 0.0083 | 0.4416 ± 0.0203 |
| RMA_frozen_body (best RMA) | 0.5421 ± 0.0304 | 0.4175 ± 0.0247 | 0.7005 ± 0.0179 | 0.8986 ± 0.0082 |
| RMA_replay | 0.3995 ± 0.0536 | 0.5927 ± 0.0704 | 0.7004 ± 0.0178 | 0.9112 ± 0.0074 |
| NoTransport | 0.2128 ± 0.0198 | 0.6570 ± 0.0223 | 0.9550 ± 0.0050 | — |
| Expert ceiling | 0.9465 ± 0.0021 | 0.1171 ± 0.0024 | 0.9435 ± 0.0045 | — |

- **Paired gap (`Gamma - best RMA`, return):** **`+0.3370 ± 0.0410` (`+8.22 SE`)**, 95% bootstrap CI `[+0.2605, +0.4118]` — exceeds the `> 2 SE` bar by >4×.
- **Paired gap (`Gamma - best RMA`, `-RMSE`):** **`+0.2470 ± 0.0314` (`+7.86 SE`)**, 95% CI `[+0.1899, +0.3072]`.
- **Paired gap (`Gamma - EB12`, return):** **`+0.0787 ± 0.0163` (`+4.84 SE`)**, 95% CI `[+0.0464, +0.1071]`; on `S1..S4` canonical retention, Gamma beats EB12 `0.9016` vs `0.4416`.

### Flat Family — `S5` Zero-Shot Transfer to `{A, C, D}` & `S1..S4` Retention

| Arm | `S5 @ {A,C,D}` Return (↑) | `S5 @ {A,C,D}` RMSE (↓) | `S5 @ B` (train) | `S1..S4` Retention (↑) |
|---|---:|---:|---:|---:|
| **Gamma (Γ)** | **0.9227 ± 0.0096** | **0.1384 ± 0.0084** | 0.9549 ± 0.0051 | **0.9433 ± 0.0027** |
| EB12 (flat conjugator) | 0.9504 ± 0.0024 | 0.1123 ± 0.0030 | 0.9500 ± 0.0052 | 0.9409 ± 0.0018 |
| RMA_frozen_body (best RMA) | 0.7512 ± 0.0226 | 0.2705 ± 0.0145 | 0.8233 ± 0.0143 | 0.9497 ± 0.0015 |
| RMA_replay | 0.6545 ± 0.0311 | 0.3327 ± 0.0202 | 0.8231 ± 0.0142 | 0.9506 ± 0.0015 |
| NoTransport | 0.2040 ± 0.0115 | 0.7109 ± 0.0193 | 0.9549 ± 0.0051 | — |
| Expert ceiling | 0.9465 ± 0.0021 | 0.1170 ± 0.0024 | 0.9435 ± 0.0045 | — |

- **Paired gap (`Gamma - best RMA`, return):** **`+0.1715 ± 0.0247` (`+6.95 SE`)**, 95% CI `[+0.1293, +0.2240]` — Gamma does not lose to RMA on the flat family.
- **Flat-vs-curved dissociation:** On the flat family, `EB12` (`0.9504`) edges out `Gamma` (`0.9227`, `-2.82 SE`) because a 6-parameter global affine map has lower estimation variance when true curvature is zero; on the curved family, that sign reverses (`+4.84 SE` in favor of `Gamma`).

## 2% Sensor-Noise Stress Test (8 Paired Seeds)

- **Curved 2%:** `Gamma = 0.8808 ± 0.0105` vs `best RMA (RMA_frozen_body) = 0.4478 ± 0.0381` -> **`+0.4330 ± 0.0334` (`+12.95 SE`)**; `EB12 = 0.7774 ± 0.0200` (`Gamma - EB12 = +5.53 SE`); Gamma `S1..S4` retention `0.9068`.
- **Flat 2%:** `Gamma = 0.9271 ± 0.0073` vs `best RMA = 0.5592 ± 0.0390` -> **`+0.3679 ± 0.0440` (`+8.37 SE`)**; Gamma `S1..S4` retention `0.9417`.

## Gate Summary (6/6 PASS)

| Gate | Value | Threshold | Result |
|---|---:|---:|:---:|
| Curved 1% `Gamma - best RMA` (return) | `+8.22 SE` | `> +2.0 SE` | PASS |
| Curved 1% `Gamma - best RMA` (`-RMSE`) | `+7.86 SE` | `> +2.0 SE` | PASS |
| Curved 1% `Gamma - EB12` (return) | `+4.84 SE` | `> +2.0 SE` | PASS |
| Flat 1% `Gamma` does not lose to `best RMA` | `+6.95 SE` | `>= -2.0 SE` | PASS |
| Old-skill `S1..S4` retention (flat / curved) | `0.9433 / 0.9016` | `>= 0.85` | PASS |
| Curved 2% stress `Gamma - best RMA` | `+12.95 SE` | `> +2.0 SE` | PASS |

## Caveats & Scope Boundaries

1. **Multi-skill trunk capacity vs per-skill policy:** Both RMA arms fit all 5 skills in a single 64-unit FiLM+affine MLP (`S5@B` train return `0.7005` curved / `0.8233` flat vs `0.954` for Gamma's per-skill RBF policy). Even relative to each arm's own `S5@B` training performance, RMA's held-out drop on curved `{A,C,D}` is `-0.158` (`RMA_frozen_body`) / `-0.301` (`RMA_replay`) vs Gamma's `-0.075` (and `-0.274` vs `-0.081` at 2% noise).
2. **Flat variance trade-off:** On the zero-curvature flat family, `EB12` (`0.9504`) slightly beats `Gamma` (`0.9227`) due to fewer fitted parameters, matching the theoretical prediction that state-dependent transport pays a small variance cost when curvature is identically zero.
3. **Simulation scope:** CPU MuJoCo 2-link arm with supervised trajectory demonstrations and a rigid-body periodic-in-$q$ × quadratic-in-$\dot q$ dynamics basis (learned solely from noisy rituals, no XML parameters). Higher-DoF legged/contact MuJoCo bodies and online RL (ED11/ED14) remain subsequent tests.

## Reproducibility

```bash
python3 -u pilots/ed10_gamma_vs_rma/pilot.py
python3 -m unittest discover -s pilots/ed10_gamma_vs_rma -p "test_*.py" -v
```
