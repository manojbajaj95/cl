# ED10b CPU Pilot: Curvature-Gated $\Gamma$ (Generic RFF) vs GAT-MLP, Capacity-Matched RMA, Always-$\Gamma$, and Always-EB12

**Verdict: `NO_PROMOTE` (4/8 gates passed, 4/8 failed — honest falsification against the ED10b promotion bar in `reviews/flood-triage.md`, line 572).**

## 1. Setup & Fair Controls

- **Simulator:** MuJoCo `3.17.0` (`RK4`, `dt = 0.01`, gravity `-9.81`) on CPU, 16 paired seeds per family, **1% relative Gaussian sensor noise** (`SENSOR_NOISE = 0.01`), 1,200 noisy ritual samples per body, 8 skill episodes × 80 steps per `(body, skill)` pair, 6 evaluation episodes per held-out body.
- **Body families (4):**
  1. `flat` (`A..D`): identical inertias/lengths, pure actuator gain changes (`k1, k2`).
  2. `curved` (`A..D`): varying masses, link lengths, end-effector payloads, and actuator gains.
  3. `contact` (`A..D`): unilateral MuJoCo wall (`condim=3`, normal + Coulomb friction `0.30..0.95`, `wall_x ∈ [0.48, 0.60]`, `solref_t ∈ [-6.5, -3.2]`) plus inertia/gain changes; expert `S5` engages active wall contact (`contact_frac > 0.05`) with `0.981` return.
  4. `mixed` (`B`, `F1..F3`, `C1..C3`): source body `B` with 3 pure-flat targets and 3 curved targets.
- **Fair arms addressing every ED10 critique:**
  - **`Gamma_RFF` (always-$\Gamma$):** Replaces ED10's hand-engineered rigid-body trig/quadratic dynamics basis with a pure generic Random Fourier Feature basis (`GenericRFFBasis`: 48 RFF in `q`, 96 RFF in `(q, qd)`, `ridge_B = 8.0`, `ridge_f = 4.0`).
  - **`Gamma_gated` (curvature-gated $\Gamma$):** Uses ED08's split-half cross-fitted curvature $F^2_{\text{cal}}$ from the same noisy rituals to route flat pairs ($F^2_{\text{cal}} \le 0.015$ or $z \le 2.5$) to `EB12` and curved/contact pairs to `Gamma_RFF`.
  - **`GAT_MLP`:** Grounded Action Transformation (Hanna & Stone 2017 / Christiano et al. 1610.03518) with generic 2-layer `tanh` forward (`(q, qd, u) -> qdd`) and inverse (`(q, qd, qdd) -> u`) MLPs fitted via L-BFGS-B from the exact same noisy rituals.
  - **`RMA_matched_frozen` / `RMA_matched_replay`:** Capacity-matched RMA using the **exact same per-skill 160-dim RFF `SkillPolicy` class and basis features as $\Gamma$** (eliminating ED10's `S5@B` capacity confound: `S5@B` is `0.980–0.986` across all 4 families, matching `Gamma` and `Expert`), modulated by a ritual-SVD body latent via an output affine head + 32-unit residual MLP.
  - **`EB12` (always-EB12):** State-independent 6-parameter affine action conjugator $u_{\text{dst}} = A u_{\text{src}} + b$.

## 2. Main Results (16 Paired Seeds, 1% Sensor Noise)

### Held-out `S5` Return (`B -> held-out bodies`) & `S5@B` Training Sanity Check

| Family | `S5@B` (Gated / Best RMA / Expert) | `Gamma_gated` | `Gamma_RFF` | `EB12` | `GAT_MLP` | Best `RMA_matched` | `NoTransport` | `Expert` |
|---|---|---|---|---|---|---|---|---|
| **FLAT** | `0.985 / 0.985 / 0.981` | `0.9793 ± 0.0019` | `0.9343 ± 0.0176` | `0.9793 ± 0.0019` | `0.9660 ± 0.0023` | **`0.9851 ± 0.0008`** (`replay`) | `0.9485 ± 0.0046` | `0.9820` |
| **CURVED** | `0.982 / 0.985 / 0.981` | `0.9085 ± 0.0116` | `0.9095 ± 0.0110` | **`0.9336 ± 0.0036`** | `0.9164 ± 0.0157` | `0.8013 ± 0.0543` (`frozen`) | `0.7007 ± 0.0115` | `0.9820` |
| **CONTACT** | `0.977 / 0.980 / 0.981` | `0.8174 ± 0.0220` | `0.8133 ± 0.0216` | **`0.8593 ± 0.0139`** | `0.5798 ± 0.0316` | `0.6376 ± 0.0531` (`frozen`) | `0.3226 ± 0.0437` | `0.9810` |
| **MIXED** | `0.986 / 0.986 / 0.982` | `0.9358 ± 0.0099` | `0.9276 ± 0.0091` | `0.9574 ± 0.0020` | `0.9387 ± 0.0102` | **`0.9717 ± 0.0025`** (`frozen`) | `0.8533 ± 0.0091` | `0.9814` |

### Paired Gaps (`Gamma_gated − Control`, 16 Paired Seeds, 4,000-draw Bootstrap 95% CI)

| Family | vs `GAT_MLP` | vs Best `RMA_matched` | vs `always-Gamma` (`Gamma_RFF`) | vs `always-EB12` |
|---|---|---|---|---|
| **FLAT** | `+0.0133 ± 0.0032` (`+4.15 SE`) | `-0.0057 ± 0.0018` (`-3.22 SE`) | **`+0.0450 ± 0.0173` (`+2.60 SE`)** | `+0.0000` (`0.00 SE`) |
| **CURVED** | `-0.0078 ± 0.0212` (**`-0.37 SE`**, CI `[-0.046, +0.034]`) | `+0.1072 ± 0.0546` (**`+1.96 SE`**, CI `[+0.012, +0.218]`) | `-0.0010 ± 0.0021` (`-0.49 SE`) | `-0.0250 ± 0.0118` (**`-2.12 SE`**) |
| **CONTACT** | **`+0.2376 ± 0.0448` (`+5.30 SE`**, CI `[+0.156, +0.324]`) | **`+0.1797 ± 0.0606` (`+2.97 SE`**, CI `[+0.067, +0.296]`) | **`+0.0040 ± 0.0019` (`+2.12 SE`)** | `-0.0419 ± 0.0215` (`-1.95 SE`) |
| **MIXED** | `-0.0029 ± 0.0166` (`-0.18 SE`) | `-0.0359 ± 0.0105` (`-3.43 SE`) | **`+0.0082 ± 0.0031` (`+2.68 SE`**, CI `[+0.004, +0.015]`) | `-0.0216 ± 0.0100` (**`-2.16 SE`**, CI `[-0.041, -0.004]`) |

### Old-Skill Retention (`S1..S4` Across All Bodies) & ED08 Curvature Gate Accuracy

| Family | `Gamma_gated` Ret | `Gamma_RFF` Ret | `EB12` Ret | `GAT_MLP` Ret | Best `RMA_matched` Ret | Gate `use_gamma` Rate by Target |
|---|---|---|---|---|---|---|
| **FLAT** | `0.9643 ± 0.0081` | `0.9323 ± 0.0133` | `0.9643 ± 0.0081` | `0.8237 ± 0.0189` | `0.9844 ± 0.0005` | `A: 0%, C: 0%, D: 0%` ($F^2_{\text{cal}} \le 0$) |
| **CURVED** | `0.8292 ± 0.0260` | `0.8243 ± 0.0252` | `0.7944 ± 0.0210` | `0.8418 ± 0.0129` | `0.7471 ± 0.0390` | `A: 100%, C: 100%, D: 50%` |
| **CONTACT** | `0.5473 ± 0.0238` | `0.5467 ± 0.0216` | `0.4654 ± 0.0276` | `0.5640 ± 0.0247` | `0.7023 ± 0.0246` | `A: 100%, C: 100%, D: 50%` |
| **MIXED** | `0.9056 ± 0.0119` | `0.8944 ± 0.0135` | `0.9166 ± 0.0101` | `0.8519 ± 0.0113` | `0.9395 ± 0.0109` | `F1–F3: 0%`; `C1: 100%, C2: 81%, C3: 100%` |

## 3. Gate-by-Gate Evaluation

| Gate | Requirement | Observed | Status |
|---|---|---|---|
| `curved_gated_beats_gat_mlp_gt_2se` | `> +2.0 SE` | `-0.37 SE` (`0.9085` vs `0.9164`) | **FAIL** |
| `curved_gated_beats_matched_rma_gt_2se` | `> +2.0 SE` | `+1.96 SE` (`0.9085` vs `0.8013`) | **FAIL** |
| `contact_gated_beats_gat_mlp_gt_2se` | `> +2.0 SE` | `+5.30 SE` (`0.8174` vs `0.5798`) | **PASS** |
| `contact_gated_beats_matched_rma_gt_2se` | `> +2.0 SE` | `+2.97 SE` (`0.8174` vs `0.6376`) | **PASS** |
| `mixed_gated_beats_always_gamma_gt_2se` | `> +2.0 SE` | `+2.68 SE` (`0.9358` vs `0.9276`) | **PASS** |
| `mixed_gated_beats_always_eb12_gt_2se` | `> +2.0 SE` | `-2.16 SE` (`0.9358` vs `0.9574`) | **FAIL** |
| `retention_ge_0.85_all_families` | `>= 0.85` on all 4 | `0.964` / `0.829` / `0.547` / `0.906` | **FAIL** |
| `rma_capacity_matched_s5_trainB_ge_0.90` | `>= 0.90` on all 4 | `0.985` / `0.985` / `0.980` / `0.986` | **PASS** |

## 4. What We Learned

1. **All three ED10 reviewer critiques were substantive:**
   - Replacing ED10's hand-engineered rigid-body trig/quadratic basis with a **generic RFF basis** caused `Gamma_gated` to **tie `GAT_MLP`** on smooth curved bodies (`-0.37 SE`) and **lose to `always-EB12`** on held-out `S5` (`-2.12 SE` curved, `-2.16 SE` mixed, `-1.95 SE` contact): at 1% sensor noise, inverting a generic RFF $B_{\text{dst}}(q)^{-1}$ adds more finite-sample variance on a localized skill than a 6-parameter global affine conjugator (`EB12`) loses in bias.
   - Giving RMA the **exact same per-skill 160-dim RFF policy class** as $\Gamma$ eliminated ~75% of ED10's curved gap (from `+8.22 SE` down to `+1.96 SE`), and on the 7-body `MIXED` family `RMA_matched` actually **beat** `Gamma_gated` (`0.9717` vs `0.9358`, `-3.43 SE`) via denser body-latent interpolation.
   - On `CONTACT`, `Gamma_gated` **did** beat both `GAT_MLP` (`+5.30 SE`) and `RMA_matched` (`+2.97 SE`) on `S5`, but still trailed `EB12` (`-1.95 SE`) and failed `S1..S4` retention (`0.5473 < 0.85`) because projecting contact-dependent skills through a single canonical body `B` loses wall-offset-specific behavior.
2. **What survived:** The **ED08 split-ritual curvature gate** itself worked cleanly (0/96 false positives on flat targets `A,C,D,F1..F3`; 100% detection on strong curved/contact targets), giving a statistically significant gain over `always-Gamma` on `FLAT` (`+2.60 SE`), `CONTACT` (`+2.12 SE`), and `MIXED` (`+2.68 SE`). However, without a stronger low-variance transport estimator that beats `EB12` and `GAT_MLP` under a generic basis, curvature-gated $\Gamma$ does **not** clear the promotion bar.

## 5. Reproduction

```bash
python3 -u pilots/ed10b_curvature_gated_gamma/pilot.py
python3 -m unittest pilots/ed10b_curvature_gated_gamma/test_ed10b.py -v
```
