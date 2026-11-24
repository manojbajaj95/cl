# Thermodynamics of remembering: non-equilibrium laws and operations for continual learning

Branch: standalone root node far from the edit-equivalence / Nerode-congruence / footprint cluster ([PR #102](https://github.com/manojbajaj95/cl/pull/102)–[PR #114](https://github.com/manojbajaj95/cl/pull/114)). Instead of asking when two edit histories are algebraically equivalent, this node asks **what non-equilibrium thermodynamic laws, work/dissipation budgets, and physical operations govern the cost of retaining skills under continual drive**.

**Node question:** When we strip away equilibrium metaphors and parameter-bit counting, which laws from stochastic and non-equilibrium thermodynamics yield *new measurable quantities* or *new continual-learning operations* (bounds, diagnostics, protocols, or feedback engines) that beat standard replay, regularization, and linear schedules at matched budgets?

**Short answer.** Three physical distinctions separate genuine thermodynamic structure from metaphor, and the CPU probe below illustrates all three:
1. **Parameter erasure is not functional erasure.** Counting erased weight bits fails because gauge/null-space moves erase parameter coordinates with zero functional forgetting, whereas conflicting moves of the *same* parameter L2 norm (`3.21`) destroy 58.9 pp of old-task accuracy and cost 61.6 relearning steps (Probe 1). The operational Landauer object is **functional mismatch dissipation** in the predictive channel (`D_KL(p_old || p_cur)`), not weight-space bit count.
2. **Retaining a skill under a live stream is a non-equilibrium steady state (NESS), not an equilibrium minimum.** Equilibrium `F = U - TS` misses the continuous *housekeeping* dissipation needed to hold an old skill against stream drive, and misses *feedback work* extracted by replay/gating (Sagawa–Ueda). Moreover, finite-time transition cost depends on the *relaxation-time* friction tensor, not instantaneous gradient variance: in Probe 2, smoothing a quench cuts protocol work 5× (`3.83 → 0.76`), but pacing by instantaneous gradient variance `||g_B - g_A||²` alone has the *wrong sign* and loses to both linear and anti-geodesic pacing (`0.962` vs `0.922` and `0.889` mean joint loss) because instantaneous variance peaks at the pure endpoints while relaxation is slowest in the mixed interior.
3. **Shocked-and-repaired learners carry hidden non-equilibrium stress.** Forward/reverse protocol dissipation `W_diss = (W_fwd + W_rev)/2` is strictly positive and scales monotonically with task conflict (`+0.195 → +0.870 → +1.192`, Probe 3a). Even after repairing a shocked MLP back to the exact old-task loss of an unshocked twin (`ΔL_A = +0.0096`), releasing both into an identical 50/50 stream triggers a **Kovacs-like non-monotonic forgetting hump** (`+0.0096 → +0.0194 → +0.0100`, Probe 3b) that instantaneous loss cannot see.

## Root cause: why physics analogies in CL usually stall—and where real laws live

1. **Equilibrium assumptions fail on SGD.** Standard SGD with finite step size `η` breaks microscopic reversibility (detailed balance) and generates discrete-time entropic forces that break non-isometric continuous symmetries ([2605.21933](https://arxiv.org/abs/2605.21933), [2505.12387](https://arxiv.org/abs/2505.12387)). That is why naive Noether conservation ([PR #6 ledger](https://github.com/manojbajaj95/cl/pull/6), #1) and equilibrium Jarzynski/Crooks or FDT formulas fail out of the box. The usable tools from physics are the ones that *do not assume detailed balance*: **Hatano–Sasa** excess/housekeeping splits, **Harada–Sasa** FDT-violation equalities, **Kolchinsky–Wolpert** mismatch costs, **Thermodynamic Uncertainty Relations (TUR)**, and **Sagawa–Ueda** feedback bounds.
2. **Bit counts in weight space ignore the reader.** Ledger #8 killed naive Landauer erasure budgets because erasing weight bits bounds parameter information, not *accessible* old-task behavior. A function-preserving ReLU rescaling moves weights by the exact same L2 norm as a destructive task switch while keeping old-task predictive KL at `0.0000` (Probe 1). Any Landauer-style law for CL must be written on the **accessible input→output channel** (or on the mismatch between the update operator's reference distribution and the live stream).
3. **Instantaneous loss hides non-equilibrium state.** Just as glasses and driven polymers exhibit the Kovacs memory effect—two states with identical energy/volume diverge when released because their internal mode populations differ—a continual learner that was shocked by task B and repaired on task A can match an unshocked twin's `L_A` while carrying latent stress that rebounds under later updates (Probe 3b).
4. **Finite-time protocol geometry requires relaxation time, not just variance.** In Sivak–Crooks finite-time thermodynamics, the optimal friction metric is the *time-integrated* force autocorrelation `ζ(λ) = ∫₀^∞ ⟨δF(0) δF(t)⟩ dt = Var(F) · τ_relax(λ)`. Dropping `τ_relax(λ)` gives a proxy that can point *backwards* (Probe 2). Any thermodynamic curriculum or speed-limit operation must measure or bound the relaxation clock, not just static gradient norm/variance.

### Small CPU probe ([`tree/probes/thermo_remembering_probe.py`](probes/thermo_remembering_probe.py), NumPy, ~10 s)

Setup: 2-layer ReLU MLP (`d=12, H=32`, plus linear host in 3b), logistic loss on binary tasks A and B with controlled subspace overlap and rule conflict `c ∈ [0, 1]`, plain SGD, 16 paired worlds (`zlib.crc32` deterministic seeds), mean ± 95% CI.

**Probe 1 — Parameter displacement vs predictive-channel mismatch (matched `||Δθ||`):**

| Update arm | `||Δθ||` | `D_KL(p_A \|\| p_cur)` | Task-A acc drop | Relearn steps (to −2 pp) |
|---|---|---|---|---|
| `gauge_null` (ReLU rescale) | `3.208 ± 0.043` | `0.0000 ± 0.0000` | `0.00 ± 0.00 pp` | `0.0 ± 0.0` |
| `ortho_task` (disjoint subspace) | `2.895 ± 0.100` | `0.0366 ± 0.0098` | `1.54 ± 1.27 pp` | `4.9 ± 4.1` |
| `conflict_task` (overlapping flip) | `3.208 ± 0.043` | `0.9650 ± 0.0528` | `58.89 ± 3.19 pp` | `61.6 ± 10.6` |

**Probe 2 — Finite-time protocol schedules `λ: 0 → 1` at exact matched total B-exposure (`mean(λ) = 0.5`, `N = 400`, `c = 0.85`):**

Measured instantaneous variance profile `ζ_inst(λ) = E[||g_B − g_A||²]` on a calibration world: `[3.31, 1.94, 1.47, 1.19, 1.07, 0.97, 1.21, 1.29, 1.83, 1.96, 3.58]` (highest at endpoints, lowest at `λ = 0.5`).

| Schedule | Protocol work `W_proto` | Mean joint loss | Worst-checkpoint A | End A / End B |
|---|---|---|---|---|
| `quench` (step 0→1) | `+3.832 ± 0.115` | `1.402 ± 0.028` | `29.05%` | `29.27% / 92.02%` |
| `linear` (`t/N`) | `+0.764 ± 0.034` | `0.922 ± 0.013` | `31.76%` | `31.76% / 90.75%` |
| `geodesic` (naive `√ζ_inst`) | `+0.792 ± 0.035` | `0.962 ± 0.014` | `31.03%` | `31.03% / 91.21%` |
| `anti_geo` (`1/√ζ_inst`) | `+0.753 ± 0.033` | `0.889 ± 0.012` | `32.54%` | `32.54% / 90.50%` |

*Takeaway:* Smooth ramping cuts protocol work 5× vs quench, but naive `√ζ_inst` pacing loses to linear and anti-geodesic because instantaneous variance omits `τ_relax(λ)`.

**Probe 3a — Forward/reverse protocol work dissipation `W_diss = (W_fwd + W_rev)/2` (`K = 100`, Langevin-SGD):**
- `conflict = 0.0`: `W_diss = +0.195 ± 0.026`, `accA_drop = 0.49 ± 0.73 pp`
- `conflict = 0.5`: `W_diss = +0.870 ± 0.040`, `accA_drop = 10.99 ± 1.48 pp`
- `conflict = 1.0`: `W_diss = +1.192 ± 0.027`, `accA_drop = 34.52 ± 3.67 pp`

**Probe 3b — Kovacs-like hidden-stress rebound (shocked with B then repaired on A to match unshocked twin's `L_A`, then released into shared 50/50 stream):**
- `linear`: start `ΔL_A = +0.0097 ± 0.0001` → peak `+0.0153 ± 0.0010` → end `+0.0124 ± 0.0010`
- `mlp`: start `ΔL_A = +0.0096 ± 0.0002` → peak **`+0.0194 ± 0.0024`** → end `+0.0100 ± 0.0021`

*Limits:* Tiny synthetic MLP/linear hosts, plain SGD without Adam/momentum, one noise level, no LLM or GPU runs. Probe 3b's rebound is small in absolute loss (`~0.01`) and needs testing under stronger representational reorganization and matched-margin controls.

## Screen against ledger, flood pool, and prior art

- **Ledger kills ([PR #6 `reviews/idea-ledger.md`](https://github.com/manojbajaj95/cl/pull/6/files)) not repeated here:**
  - *#8 Landauer erasure budget* (KILLED: weight-bit counts say nothing about accessibility; `β → 1` confounds optimizer). Ideas 1–5 explicitly work in the *accessible predictive channel* or *mismatch cost*, not raw weight bits.
  - *#1 Noether memory & #2 Gauge preconditioning* (KILLED: finite-step SGD/momentum breaks continuous invariants; rescaling is effective-LR). Not repeated.
  - *Noise vs overwrite at equal LR area* (KILLED: no pure noise-temperature forgetting law without conflict). Every temperature/bath idea below varies *conflict* and matches drift/LR area.
  - *#12 Residual skill bits* (KILLED: mask-search dependent; relearning savings already measure it) and *#5 Forgetting as edge-of-stability crossing* (KILLED). Not repeated.
  - *Ledger patterns enforced across all 22 cards:* control for **per-item margin** before claiming forgetting order; do not dress up a **first-order Taylor expansion** as a physical law; beat **equal-budget replay, EWC, linear ramps, and direct loss monitoring**; include an explicit **old-task retention check** on held-out old tasks in every cheapest first test.
- **Flood pool items ([PR #44 `ideas/flood/physics-math.md`](https://github.com/manojbajaj95/cl/pull/44), #14–#25) not repeated here:** Crooks irreversibility meter (#14), equilibrium FDT forecast (#15), Onsager asymmetry (#16), replica-overlap fracture (#17), Carnot LR cycle (#18), Hopfield dreaming (#19), stochastic resonance recall (#20), kinetic proofreading (#21, downgraded to sequential testing), parallel tempering (#22), glassy aging clocks (#23), frustration loops (#24), percolation threshold (#25).
- **2025–2026 arXiv prior art screened (alphaXiv + arXiv API):**
  - *Thermodynamic Theory of Learning I & II* ([2601.17607](https://arxiv.org/abs/2601.17607), [2602.07950](https://arxiv.org/abs/2602.07950)): Epistemic Speed Limit (Wasserstein lower bound on single-task entropy production) and minimum-energy controllability Gramian for CL reachability.
  - *Thermodynamic Irreversibility of Training Algorithms* ([2605.21933](https://arxiv.org/abs/2605.21933)) & *Neural Thermodynamics* ([2505.12387](https://arxiv.org/abs/2505.12387)): discrete-step SGD irreversibility = backward error = entropy production to `O(η)`, breaking non-isometric symmetries.
  - *Speed limits for information acquisition in SGD* ([2609.08219](https://arxiv.org/abs/2609.08219)): Fisher-information flow speed limit decomposing drift and noise.
  - *Kramers Escape Approach to CL* ([2604.04154](https://arxiv.org/abs/2604.04154)): EWC as linear-in-tasks barrier height with exponential escape collapse; insight vs repetition as temperature protocols.
  - *Stochastic Thermodynamics of Associative Memory* ([2601.01253](https://arxiv.org/abs/2601.01253)), *Dissipative Learning / BEDS* ([2601.17933](https://arxiv.org/abs/2601.17933)), *Information Thermodynamics of Agents* ([2504.06209](https://arxiv.org/abs/2504.06209)), *Thermodynamics of Classifiers* ([2605.24365](https://arxiv.org/abs/2605.24365)), *Thermodynamic Costs of Simple Linear Regression* ([2605.19195](https://arxiv.org/abs/2605.19195)), *SGD as Free Energy Minimization* ([2505.23489](https://arxiv.org/abs/2505.23489)), *Laws of Thermodynamics for Exponential Families* ([2501.02071](https://arxiv.org/abs/2501.02071)), *Statistical Mechanics of CL* ([2212.02846](https://arxiv.org/abs/2212.02846)), *ML in and out of equilibrium* ([2306.03521](https://arxiv.org/abs/2306.03521)).
- **Required controls for every card:** matched total update steps, stored bytes (including probes/monitors/buffers), and new-task loss/accuracy; compare against equal-budget uniform replay, EWC/LwF, linear schedules, and direct held-out loss monitoring.

## Research ideas (22 cards)

### A. Functional Landauer & mismatch-cost laws (replacing weight-bit counting)

1. **Kolchinsky–Wolpert mismatch-cost routing.**
   - *Mechanism:* Model a continual update operator `T` (a fine-tune step or adapter update) as a physical channel whose zero-dissipation reference input distribution is `q_0` (the old-task feature/logit distribution). By Kolchinsky–Wolpert, running `T` on shifted distribution `p_0` incurs an irreducible *mismatch dissipation* `D_KL(p_0 || q_0) − D_KL(Tp_0 || Tq_0)`. Estimate this drop on unlabeled probes across candidate modules/layers and route the new-task write to the module with minimal mismatch dissipation rather than minimal parameter norm.
   - *Why it might be new:* Ledger #8 killed parameter-bit Landauer counting, and 2605.19195 applies mismatch cost only to single-task linear regression; using the *contraction of input-to-output KL mismatch* as a write-routing criterion for CL is untested. Likely tie: routing by activation-space cosine distance or Fisher trace.
   - *Cheapest first test:* Modular 4-expert MLP on a 6-task stream with shared and conflicting subspaces; compare mismatch-cost routing against Fisher-trace routing, activation-distance routing, and random routing at matched capacity.
   - *Old-task retention check:* Held-out accuracy and predictive KL on all prior tasks after task 6, matched on task-6 accuracy.

2. **Decoder-constrained Landauer erasure floor.**
   - *Mechanism:* Define the *accessible* information of skill `A` as the mutual information `I(X_A; Y_hat | D)` reachable under a fixed deployed decoder `D` (fixed prompt budget, temperature, and top-k). Compute the minimum channel entropy production required to shift `p(Y_hat | X_B, D)` by `Δ_B` without lowering `I(X_A; Y_hat | D)` below floor `I_min`, using Blahut–Arimoto on a small surrogate channel; flag updates whose realized functional erasure exceeds the floor by a large waste factor.
   - *Why it might be new:* Directly fixes Ledger #8's fatal objection ("erased weight bits say nothing about accessibility") by binding erasure to the actual read channel `D`. Risk: in small worlds this may reduce to KL-regularized distillation (LwF) on unlabeled probes.
   - *Cheapest first test:* Constrained-output toy classifier / tiny LM head under 3 decoder settings (greedy, T=1, top-2); test whether decoder-constrained erasure predicts actual deployed-decoder forgetting better than parameter KL and full-distribution KL.
   - *Old-task retention check:* Deployed-decoder accuracy on held-out old tasks at matched new-task accuracy, with per-item margin stratified.

3. **Reversible vs irreversible forgetting efficiency (`η_forget = ΔF_task / W_proto`).**
   - *Mechanism:* Decompose the protocol work `W_proto` spent moving from task A to task B into the unavoidable equilibrium free-energy gap `ΔF_task` (estimated from a slow quasi-static reference) and the avoidable finite-time excess work `W_ex = W_proto − ΔF_task`. Track `η_forget` online across optimizers and batch sizes to separate *intrinsic task conflict* (high `ΔF_task`, needs capacity) from *protocol waste* (high `W_ex`, fixable by pacing/preconditioning).
   - *Why it might be new:* CL benchmarks lump intrinsic conflict and optimizer-induced shock into one forgetting number. Probe 2 shows a 5× `W_proto` gap between quench and smooth ramp on the *exact same* task pair. Likely tie: comparing final forgetting of SGD vs small-LR SGD directly.
   - *Cheapest first test:* Sweep task conflict `c ∈ {0.0, 0.3, 0.6, 0.9}` and step-size schedules on a 2-layer MLP; test whether `W_ex / W_proto` predicts how much forgetting is recoverable by slower pacing alone, against a gradient-norm baseline.
   - *Old-task retention check:* Held-out task-A accuracy after matched task-B convergence, plus relearning steps to 95% of initial A accuracy.

4. **Selective-unlearning Landauer scaling law (collateral erasure per bit removed).**
   - *Mechanism:* Measure the minimum work (excess dissipation in retained-task predictive channels) needed to *selectively* erase one skill `k` while holding `M` correlated old skills within tolerance `ε`, as a function of the mutual information `I(h_k; h_{−k})` of their internal representations. Test whether collateral erasure follows a sharp Landauer-like lower bound `W_collat ≥ c · I(h_k; h_{−k}) / ε` that predicts when selective unlearning becomes more expensive than retraining from a clean checkpoint.
   - *Why it might be new:* Machine unlearning measures empirical utility drop (e.g. 2602.06331), not an information-thermodynamic lower bound on collateral erasure as a function of representational entanglement. Risk: may track simple gradient-cosine overlap in linear regimes.
   - *Cheapest first test:* Synthetic multi-task MLP with tunable hidden-unit sharing (`I` swept from 0 to 1); compare exact selective unlearning work against gradient-cosine and Fisher-overlap predictors.
   - *Old-task retention check:* Worst-task accuracy and predictive KL across the `M` retained skills, plus resistance of the erased skill to 20-step relearning probes.

5. **Consolidation erasure exchange rate (nats lost per nat internalized).**
   - *Mechanism:* When distilling an in-context rule or episodic memory into weights, define the *erasure exchange rate* `R_erase = Σ_{j ≠ new} ΔD_KL(p_j^old || p_j^cur) / ΔI_internalized(new)` measured on unlabeled old-task probes. Trigger consolidation only for items whose predicted `R_erase` is below a threshold; keep high-`R_erase` items in external/in-context memory permanently.
   - *Why it might be new:* Replaces heuristic consolidation rules (age, frequency, or L1's uniform packing) with a dimensionless thermodynamic exchange rate in nats/nat. Likely tie: gating consolidation by validation-set old-task loss drop on a replay buffer.
   - *Cheapest first test:* 20-rule synthetic context-to-weight distillation stream on a tiny transformer/MLP (matching bytes between weights and external buffer); compare `R_erase` gating against frequency gating, validation-loss gating, and uniform consolidation.
   - *Old-task retention check:* Held-out accuracy on previously consolidated rules and unconsolidated base tasks at equal total storage bytes.

### B. Non-equilibrium free energy & housekeeping costs of retained skills

6. **Hatano–Sasa excess vs housekeeping forgetting decomposition (`Σ_tot = Σ_ex + Σ_hk`).**
   - *Mechanism:* For a learner continuously driven by a non-stationary stream of tasks, decompose total entropy production into *excess* dissipation `Σ_ex` (paid during distribution shifts) and *housekeeping* dissipation `Σ_hk` (paid continuously to maintain old skills against ongoing stream drift). Estimate `Σ_hk` from the steady-state probability current (nonzero circulation of weights/logits around the task cycle) and use it to set the *minimum* replay power required to prevent secular drift.
   - *Why it might be new:* Existing free-energy CL theories (2212.02846, 2505.23489) treat retained skills as equilibrium minima where `Σ_hk = 0`. In cyclic or drifting streams, `Σ_hk > 0` predicts a nonzero maintenance floor even at zero shift. Risk: in simple linear cycles, `Σ_hk` may reduce to mean squared gradient disagreement.
   - *Cheapest first test:* 4-task cyclic stream on a 2-layer MLP under Langevin-SGD; measure circulation current and `Σ_hk` vs actual minimum replay fraction needed to hold old-task accuracy ≥ 85%, against a gradient-variance baseline.
   - *Old-task retention check:* Worst-task accuracy over 20 full cycles at matched total gradient steps and replay budget.

7. **Sagawa–Ueda feedback information engine for replay and gating.**
   - *Mechanism:* Treat any adaptive replay selector, probe-before-write gate, or dynamic router as a Maxwell demon that measures the learner's state (`I_meas` bits per step) and uses feedback to save forgetting work `W_saved`. By Sagawa–Ueda, `W_saved ≤ kT_eff · I_meas`, and resetting the demon's memory costs at least `kT_eff · H_reset`. Audit real CL selectors by measuring their *feedback efficiency* `γ = W_saved / (kT_eff · I_meas)` and net work `W_saved − C_measure − C_reset`.
   - *Why it might be new:* Gives a unified thermodynamic accounting law for why clever selectors often lose to uniform replay once probe/index overhead is charged (cf. ledger's PR #113 and G1 kills). Risk: measuring `T_eff` cleanly in non-isotropic SGD is nontrivial.
   - *Cheapest first test:* Compare uniform replay, loss-prioritized replay, and probe-gated replay on a 5-task MLP stream; measure `I_meas`, `W_saved`, and total compute/probe cost, testing whether `γ` predicts the crossover where prioritization beats uniform.
   - *Old-task retention check:* Held-out old-task accuracy at matched total forward+backward FLOPs (charging every selector probe).

8. **Entropic vs energetic skill stabilization (`ΔF_eff = ΔU − T_eff ΔS`).**
   - *Mechanism:* Two weight basins with identical old-task loss and margin (`ΔU`) can differ drastically in local basin entropy `ΔS` (log-volume of weight perturbations preserving old-task accuracy, estimated via low-rank Hutchinson/slice sampling). Actively regularize toward *high-entropy* old-task basins (maximizing `ΔS` rather than sharpening `ΔU` as EWC does) when future stream temperature `T_eff = η/B` is high, testing whether entropic stabilization survives high-LR adaptation where Kramers barriers (2604.04154) collapse.
   - *Why it might be new:* SAM/flatness seeks low curvature on the *current* task; this explicitly predicts a *temperature-dependent crossover* (`T_eff > ΔU / ΔS`) where entropic basin volume beats energetic EWC stiffness at matched old-task margin. Likely tie: SAM + EWC tuned on a validation grid.
   - *Cheapest first test:* 2-task MLP at low vs high `T_eff = η/B` (3 temperatures × 10 seeds), comparing EWC, SAM, and an explicit basin-volume regularizer at matched pre-switch old-task margin.
   - *Old-task retention check:* Held-out old-task accuracy after high-`T_eff` task-B training, checking that high-`ΔS` basins do not sacrifice new-task convergence speed.

9. **Grand-canonical chemical potential for skill capacity (`μ_k = ∂F / ∂n_k`).**
   - *Mechanism:* Treat shared hidden capacity as a finite particle reservoir and define each retained skill's *chemical potential* `μ_k`: the marginal increase in joint free energy (old + new loss minus entropy) when tightening skill `k`'s error budget by `δ`. When the sum of active chemical potentials exceeds a critical threshold `μ_crit`, the learner is thermodynamically saturated and must *grow* (spawn a new module/adapter) or *evict* the highest-`μ_k` skill to external memory.
   - *Why it might be new:* Expansion triggers in CL use heuristic loss spikes or novelty thresholds; `μ_k` prices *shared-capacity congestion* across all retained skills simultaneously. Likely tie: spawning a module whenever worst old-task validation loss crosses a fixed threshold.
   - *Cheapest first test:* 10-task stream on a small growable MLP (`H` starts at 16, can add 8-unit blocks up to budget `H=48`); compare `μ_k`-triggered growth against loss-threshold growth and periodic growth at equal final parameter count.
   - *Old-task retention check:* Average and worst-task accuracy across all 10 tasks at the final budget, plus new-task learning speed.

10. **Self-budgeting Maxwell-demon replay controller.**
    - *Mechanism:* Build a replay controller that estimates its own online Sagawa–Ueda net work (`ΔL_old_saved − α · probe_cost`) over a sliding window and dynamically varies its measurement bit-rate `I_meas` (from 0 bits = uniform replay up to full per-item scoring) so it *never* spends more compute measuring what to replay than it recovers in retention.
    - *Why it might be new:* Turns Sagawa–Ueda from an analysis bound into a concrete self-throttling CL operation that automatically degrades to uniform replay when tasks are easy or non-conflicting. Likely tie: a simple UCB bandit switching between uniform and loss-prioritized replay.
    - *Cheapest first test:* Mixed-regime stream alternating low-conflict (where uniform wins at equal FLOPs) and high-conflict shocks (where targeted replay wins); compare against uniform, always-prioritized, and a bandit controller at equal total FLOPs.
    - *Old-task retention check:* Time-averaged and worst-checkpoint old-task accuracy across both regimes, charging all selector forward passes.

11. **Spinodal phase separation of conflicting skills.**
    - *Mechanism:* In binary mixtures, when the second derivative of free energy with respect to composition turns negative (`∂²F/∂φ² < 0`, the spinodal), homogeneous mixing is locally unstable and the system spontaneously separates into two coexisting phases. Monitor the curvature of the joint `(A, B)` free energy along the task-mixing coordinate `λ`; when it goes negative (indicating irreducible conflict in shared features), split the affected layer into two weakly coupled branches rather than paying permanent housekeeping dissipation.
    - *Why it might be new:* Flood #17 used replica-overlap bimodality (expensive K-replica training); spinodal instability is detectable from a *single* trajectory's local curvature along the mixture axis `λ`. Risk: may tie splitting whenever gradient cosine between A and B stays negative.
    - *Cheapest first test:* 6-task stream containing both compatible and conflicting task pairs on a small MLP; compare spinodal-triggered layer splitting against negative-gradient-cosine splitting and random splitting at equal total parameters.
    - *Old-task retention check:* Held-out accuracy on both compatible and conflicting old tasks, verifying that compatible tasks still share representations for positive forward transfer.

### C. Fluctuation theorems, speed limits & dissipation–precision tradeoffs

12. **Thermodynamic Uncertainty Relation (TUR) for retention variance.**
    - *Mechanism:* Apply the discrete-time TUR (`Var(J_ret) / ⟨J_ret⟩² ≥ 2 / Σ_tot`, or the dynamical-activity bound `≥ 1 / A_tot` for non-reversible dynamics) to the cumulative retention current `J_ret` across random minibatch/task orders. Use the ratio `Q_TUR = Σ_tot · Var(J_ret) / (2 ⟨J_ret⟩²)` (the thermodynamic precision efficiency) to diagnose whether high seed-to-seed forgetting variance is *fundamental* (near the TUR bound, requiring more replay/activity) or *avoidable* (far above 1, fixable by variance reduction).
    - *Why it might be new:* CL literature reports seed variance as noise, never as a quantity lower-bounded by update dissipation/activity. Directly addresses the seed-variance bottleneck observed repeatedly in `cl-research.md` (Q1, HW1, plasticity reserve). Risk: the discrete-time activity bound may be loose by orders of magnitude in deep nets.
    - *Cheapest first test:* Exact finite-state Markov learner + 2-layer MLP under Langevin-SGD across 64 seeds; measure `Var(J_ret)/⟨J_ret⟩²`, total path entropy production `Σ_tot`, and dynamical activity `A_tot` across LR and replay rates.
    - *Old-task retention check:* Both mean and 5th-percentile (worst-seed) old-task accuracy across 64 seeds at matched compute.

13. **Harada–Sasa FDT-violation meter for unlabeled forgetting detection.**
    - *Mechanism:* Near equilibrium, spontaneous fluctuations equal forced response; *out of equilibrium*, the Harada–Sasa equality states that the integrated violation of fluctuation–dissipation equals the exact rate of energy dissipation (`J_diss = ∫ [C(ω) − 2T R''(ω)/ω] dω`). On unlabeled old-task probes, compare the autocorrelation of output fluctuations under normal SGD noise against the linear response to a tiny synthetic probe perturbation; use the FDT violation to detect *hidden non-equilibrium forgetting current* before accuracy drops.
    - *Why it might be new:* Fixes Flood #15's equilibrium FDT assumption (which breaks under SGD) by turning the *violation* itself into the signal. Likely tie: simply tracking the variance or drift rate of unlabeled probe logits directly.
    - *Cheapest first test:* 2-layer MLP undergoing slow vs abrupt task drift; correlate Harada–Sasa FDT violation on unlabeled task-A probes with future task-A accuracy drop, against logit-variance and logit-drift baselines.
    - *Old-task retention check:* Early-warning AUC for predicting a ≥ 5 pp held-out old-task drop, plus retention gain when using the alarm to trigger bounded replay.

14. **Hatano–Sasa broken-ergodicity detector for irreversible forgetting.**
    - *Mechanism:* Between two non-equilibrium steady states (task-A NESS and task-B NESS), the Hatano–Sasa integral fluctuation theorem gives `⟨exp(−Y)⟩ = 1`, where `Y` is the excess work along the transition. In finite ensembles, a persistent downward bias `⟨exp(−Y)⟩ < 1` is a classic physical signature of *broken ergodicity* (trajectories trapped in a new basin that cannot return to the old NESS). Use finite-sample deviations of `⟨exp(−Y)⟩` across short forked rollouts to detect when forgetting has crossed from *reversible lag* into *irreversible basin loss*.
    - *Why it might be new:* Flood #14 proposed equilibrium Crooks (which assumes detailed balance and fails for SGD); Hatano–Sasa holds for *non-reversible* Markov dynamics between NESSs and explicitly turns the *breakdown* of the identity into an irreversibility detector. Risk: exponential averages have notoriously high variance in finite samples.
    - *Cheapest first test:* 2-layer MLP on reversible (orthogonal/mild) vs irreversible (high-conflict, capacity-limited) transitions; compare `log ⟨exp(−Y)⟩` against raw mean `⟨Y⟩` and old-loss gap for predicting relearning failure (failing to recover old accuracy in `K` steps).
    - *Old-task retention check:* Actual relearning recovery on held-out old tasks after the detected crossing, matched against triggering repair from a simple old-loss threshold.

15. **Constrained Epistemic Speed Limit (CESL) for two-task transport.**
    - *Mechanism:* Extend 2601.17607's single-task Wasserstein Epistemic Speed Limit and 2609.08219's Fisher speed limit to *retention-constrained* transport: derive the lower bound on total entropy production `Σ_min(T)` required to move an ensemble's task-B distribution by Wasserstein distance `W_2(p_0^B, p_T^B)` in `T` steps while keeping `D_KL(p_0^A || p_t^A) ≤ δ` for all `t ≤ T`. Use `Σ_min(T) / Σ_actual` as an algorithm-independent *thermodynamic efficiency* score for CL optimizers (SGD, Adam, OGD, EWC, replay).
    - *Why it might be new:* 2601.17607 and 2609.08219 bound single-task learning only; adding the retention tube `D_KL ≤ δ` creates a curved obstacle in Wasserstein space whose geodesic length strictly exceeds the unconstrained distance, quantifying the *irreducible speed penalty of remembering*.
    - *Cheapest first test:* Gaussian/linear ensemble (exact analytic geodesic around a KL ball) + 32-particle ReLU MLP ensemble; measure `Σ_min / Σ_actual` across SGD, OGD, EWC, and replay at matched `δ` and `T`.
    - *Old-task retention check:* Verify `D_KL ≤ δ` and held-out task-A accuracy throughout the trajectory, not only at endpoint `T`.

16. **Large-deviation rate function for rare catastrophic-forgetting spikes.**
    - *Mechanism:* Estimate the scaled cumulant generating function `ψ(k) = (1/t) log ⟨exp(k · ΔL_A)⟩` from short-horizon minibatch/stream fluctuations and take its Legendre transform `I(a) = sup_k [ka − ψ(k)]` (the large-deviation rate function). Use `I(a)` to forecast the probability of a rare catastrophic-forgetting excursion (`ΔL_A > a_crit`) over a 10× longer deployment horizon, and choose batch size / clipping / replay to steepen the tail of `I(a)` rather than only lowering mean `ΔL_A`.
    - *Why it might be new:* CL evaluates expected forgetting; in deployed agents, rare worst-case batch or shift excursions cause irreversible collapse. Large-deviation theory predicts tail collapse from normal-regime statistics. Likely tie: fitting a Gaussian or empirical quantile to short-horizon `ΔL_A` spikes.
    - *Cheapest first test:* Heavy-tailed stream of rare conflicting batches on a 2-layer MLP (100 seeds); test whether Legendre-transformed `I(a)` forecasts 1,000-step collapse probability from the first 100 steps better than Gaussian variance and empirical 95th-percentile baselines.
    - *Old-task retention check:* Tail (worst 5% of seeds) old-task accuracy at step 1,000 when using `I(a)`-guided clipping/replay vs mean-loss-guided replay at equal budget.

17. **Jarzynski-reweighted off-policy replay (debiasing stale or synthetic buffers).**
    - *Mechanism:* When a replay buffer holds stale self-generated logits or synthetic old-task examples drawn from a drifted distribution `p_buf ≠ p_old`, standard replay biases the equilibrium toward `p_buf`. Treat the drift from `p_old` to `p_buf` as a finite-time protocol with measurable path work `W_i` per buffered item (accumulated log-ratio of model likelihoods along the drift), and weight each replayed item by its Jarzynski factor `w_i ∝ exp(−β W_i)` to recover unbiased old-task free-energy gradients.
    - *Why it might be new:* Unlike ordinary importance sampling (which needs the true `p_old(x)` density), Jarzynski reweighting uses *trajectory work* accumulated along the model's own past updates. Risk: weight degeneracy (low ESS) under large drift, similar to G1's IS failure.
    - *Cheapest first test:* 3-task stream with a self-generated replay buffer (no raw old labels); compare Jarzynski-weighted self-replay against unweighted self-replay, DER-style logit replay, and recency-weighted replay, reporting ESS explicitly.
    - *Old-task retention check:* Held-out true old-task accuracy and calibration (ECE/NLL) after 3 tasks at equal buffer bytes.

### D. Finite-time protocols, thermal memory effects & thermodynamic operations

18. **True relaxation-time Sivak–Crooks geodesic curricula (`ζ(λ) = Var(F) · τ_relax(λ)`).**
    - *Mechanism:* Directly fixes Probe 2's negative result: estimate the *integrated autocorrelation* friction `ζ(λ) = ∑_{τ=0}^{τ_max} Cov(F_t, F_{t+τ})` of the generalized force `F = L_B − L_A` along the mixture coordinate `λ ∈ [0, 1]` (capturing both variance and slow relaxation near the mixed saddle), and pace `dλ/dt ∝ 1 / √ζ(λ)` at matched total B-exposure.
    - *Why it might be new:* Probe 2 proved that instantaneous variance `Var(F)` points the *wrong way* (`0.962` vs `0.922` linear vs `0.889` anti-geodesic); incorporating `τ_relax(λ)` tests whether true Sivak–Crooks thermodynamic length actually beats linear and anti-geodesic schedules in nonlinear continual learners.
    - *Cheapest first test:* Extend Probe 2 on the same 16 worlds by measuring the autocorrelation time `τ_relax(λ)` on the calibration world and comparing `√(Var · τ_relax)` pacing against `linear`, `anti_geo`, and `quench` at exact matched `mean(λ) = 0.5`.
    - *Old-task retention check:* Cumulative old-task loss excursion, worst-checkpoint task-A accuracy, and final `(A, B)` accuracy.

19. **Kovacs-effect stress sensor and annealing pulse.**
    - *Mechanism:* Directly builds on Probe 3b's Kovacs rebound (`+0.0096 → +0.0194 → +0.0100` in MLP): after any shock-and-repair episode, run a tiny non-destructive fork of `k = 10` neutral/Langevin steps to detect a Kovacs forgetting hump (`max_t L_A(t) − L_A(0) > δ_K`). When a hump is detected, apply a short low-temperature equilibration ("annealing") pulse on a balanced mix before admitting the next new task, preventing hidden stress from compounding across consecutive shifts.
    - *Why it might be new:* Standard CL stops repairing as soon as `L_A` returns to target; Probe 3b shows that loss-matched repaired states still carry hidden non-equilibrium stress that rebounds later. Likely tie: simply running `k` extra repair steps unconditionally (equal-step control!).
    - *Cheapest first test:* 4-shock sequential stream on a 2-layer MLP; compare Kovacs-triggered annealing against unconditional extra repair steps and no-anneal repair at *exact matched total gradient steps*.
    - *Old-task retention check:* Worst-checkpoint and final held-out accuracy on all shocked-and-repaired old tasks across 16 worlds.

20. **Mpemba-effect pre-heating for low-forgetting task switching.**
    - *Mechanism:* In statistical physics, the strong Mpemba effect accelerates relaxation to a target equilibrium by briefly *heating* or perturbing the system so that its overlap with the slowest-decaying Fokker–Planck eigenmode vanishes. Before switching from task A to a joint `(A, B)` target, test whether a brief, directionally chosen high-LR or isotropic-noise pulse (followed by standard cooling) projects out the slow interfering allocation mode and reaches the joint `(A, B)` basin *faster and with less integrated old-task forgetting* than monotonic cooling from cold A.
    - *Why it might be new:* Warmup/rewarm schedules in CL are heuristic and usually *hurt* retention (ledger: cooldown facts forgotten on rewarm, controlled by margin); a true Mpemba speedup requires a *non-monotonic* win in relaxation time and integrated retention against both constant-LR and monotonic-anneal controls at equal total steps.
    - *Cheapest first test:* 2-layer MLP trained on A, switching to 50/50 `(A, B)` over `N = 300` steps; sweep short pre-pulse temperature/duration at matched total step count against monotonic LR decay and constant LR.
    - *Old-task retention check:* Time-averaged and worst-checkpoint held-out task-A accuracy, plus time to reach 90% on both A and B.

21. **Counterdiabatic ("shortcut to adiabaticity") continual-learning updates.**
    - *Mechanism:* In finite-time thermodynamics, adding a counterdiabatic driving term `H_CD(t)` forces the system to track the instantaneous equilibrium `p*_λ(t)` along a fast protocol `λ(t)` with *zero* excess dissipation. In CL, approximate the first-order counterdiabatic auxiliary update `Δθ_CD = −λ̇ · H_λ^{-1} (g_B − g_A)` (via conjugate gradients / K-FAC on a tiny sketch) during fast task transitions so the learner tracks the moving joint minimum without paying Probe 2's 5× quench penalty.
    - *Why it might be new:* Natural gradient / K-FAC preconditions the *current* gradient `g_λ`; counterdiabatic driving adds an explicit *protocol-velocity term* proportional to `λ̇ · (g_B − g_A)` that vanishes at static `λ` and cancels finite-speed lag. Likely tie: plain K-FAC / Gauss–Newton on `(1 − λ)L_A + λL_B` at the same Hessian-vector-product budget.
    - *Cheapest first test:* Linear + 2-layer MLP fast transition (`N = 40` steps, where quench penalty is largest); compare counterdiabatic updates against plain K-FAC/CG natural gradient and smooth-ramp SGD at matched HVP + gradient FLOPs.
    - *Old-task retention check:* Worst-checkpoint and endpoint held-out task-A accuracy at matched task-B accuracy.

22. **Multi-temperature heat-sink partitioning (controlled thermal conductance across layers).**
    - *Mechanism:* Partition parameters into a "hot" plastic subsystem (high `T_h = η_h / B`) and a "cold" memory subsystem (low `T_c = η_c / B`), coupled by an explicit *thermal conductance* parameter `κ` (strength of gradient/feature coupling or elastic tether between fast and slow weights). Derive the steady-state heat flux `Q̇(κ, T_h − T_c)`—the rate at which hot-bath fluctuations leak into and erode cold-bath old-task accuracy—and tune `κ` to maximize new-task learning power per unit of leaked old-task heat.
    - *Why it might be new:* Multi-timescale learners (Benna–Fusi, fast/slow weights, LoRA + frozen base) fix the coupling architecture heuristically; framing the interface as a *thermal conductance* yields a measurable heat-leakage law `Q̇(κ)` predicting when fast-weight adaptation still erodes slow weights through the coupling. Likely tie: standard fast/slow LR ratio sweep or LoRA with frozen base (`κ = 0` limit).
    - *Cheapest first test:* Two-block MLP (fast adapter + slow backbone) with tunable coupling `κ` on a 6-task stream; verify whether measured heat flux predicts slow-backbone forgetting across `κ`, and test whether optimal `κ*` beats frozen-base (`κ = 0`) and uniform-LR (`T_h = T_c`) baselines.
    - *Old-task retention check:* Held-out accuracy on tasks 1–5 after task 6, verifying that `κ*` beats `κ = 0` on tasks requiring backbone adaptation while keeping old-task loss below uniform-LR.

## Deeper sub-questions, ranked by chance of a new primitive

1. **Can a Sagawa–Ueda feedback efficiency law (`W_saved ≤ kT_eff · I_meas − C_reset`) predict—before deployment—when adaptive replay/gating beats uniform replay at equal FLOPs?** *(Ideas 7, 10.)*
   - *Why #1:* If real CL selectors obey a tight measurable feedback bound, we get a **universal accounting primitive** for agent and model memory (explaining why many smart selectors tie uniform replay once probe costs are charged, and yielding a self-throttling controller).
   - *Sharpest next CPU test:* Measure `I_meas`, `W_saved`, and total FLOPs across 5 replay/gating policies on a 5-task MLP stream with swept conflict and probe cost.
   - *Kill criterion:* Kill if `T_eff` cannot be defined consistently across architectures, if the bound is loose by >10× in all regimes, or if a simple bandit over `{uniform, prioritized}` matches the thermodynamic controller across every regime.

2. **Does the true relaxation-time Sivak–Crooks friction metric (`ζ(λ) = ∫ ⟨δF(0)δF(t)⟩ dt`) or a counterdiabatic `λ̇`-term actually beat linear ramps and K-FAC on fast continual transitions?** *(Ideas 3, 18, 21.)*
   - *Why #2:* Probe 2 already showed a 5× protocol-work gap between quench and ramp and caught why naive instantaneous-variance geodesics fail. Resolving whether *relaxation-time* geodesics or *counterdiabatic* `λ̇`-driving unlock a real finite-time speedup would yield a genuinely new continual optimization primitive.
   - *Sharpest next CPU test:* Extend `tree/probes/thermo_remembering_probe.py` to measure `τ_relax(λ)` and test both true geodesic pacing and first-order counterdiabatic driving (`N = 40` and `N = 400`) against linear ramp, anti-geodesic, and K-FAC at matched HVPs and total B-exposure.
   - *Kill criterion:* Kill if `τ_relax(λ)` pacing still ties linear/anti-geodesic within 1 SE, or if counterdiabatic driving loses to plain K-FAC at equal HVP budget.

3. **Is the Kovacs hidden-stress rebound (Probe 3b) large enough in realistic nonlinear streams to make post-repair stress sensing + annealing beat unconditional extra repair steps?** *(Ideas 13, 19, 20.)*
   - *Why #3:* Probe 3b gave a clean toy witness (`+0.0096 → +0.0194 → +0.0100`) that loss-matched repaired models still hide non-equilibrium stress. Turning that into a *stress-relief operation* (or Mpemba pre-pulse) would address a failure mode invisible to every current retention metric.
   - *Sharpest next CPU test:* Multi-shock stream on a deeper ReLU MLP and a small transformer with AdamW; test whether Kovacs rebound scales with depth/conflict and whether stress-triggered annealing beats equal-step unconditional repair on worst-checkpoint old-task accuracy.
   - *Kill criterion:* Kill if the rebound stays < 1 pp on held-out accuracy at realistic widths/depths, disappears once margin is matched, or never beats unconditional extra repair steps at matched compute.

4. **Can functional mismatch dissipation (Kolchinsky–Wolpert) or Hatano–Sasa broken ergodicity separate reversible lag from irreversible skill loss without old labels?** *(Ideas 1, 2, 6, 14.)*
   - *Why #4:* Unlabeled early-warning signals for irreversible forgetting are high-value if they beat raw logit drift and gradient cosine. Probe 1 already showed functional predictive KL cleanly fixes Ledger #8's parameter-erasure failure.
   - *Sharpest next CPU test:* Sweep reversible vs irreversible transitions (including capacity-limited MLPs where old basins become unreachable) and compare `log ⟨exp(−Y)⟩`, Harada–Sasa FDT violation, and mismatch contraction against unlabeled logit drift and gradient cosine for predicting relearning failure.
   - *Kill criterion:* Kill if unlabeled logit drift or gradient cosine ties or beats every thermodynamic estimator across all conflict/capacity regimes, or if exponential-average variance makes `⟨exp(−Y)⟩` unusable at realistic ensemble sizes.
