# Physical learning 2 — return-point memory over the data mix, and temperature-chaos stacking

Child of [PR #341](https://github.com/manojbajaj95/cl/pull/341) (`tree/root-physical-learning.md`). This node follows the two ideas the reviewer scored 3 there (`reviews/flood-triage.md`, row 465):

- **PL01, return-point memory over a data-mixture drive (Preisach bank).** Its controls: an equal-byte gated two-delta block driven by the same scalar, a nearest-mixture lookup table, EWC, replay at equal budget, a shuffled-threshold bank, and per-task A/B retention after C and on nested returns.
- **PL07, temperature-chaos stacking.** Its controls: the same task order at a fixed temperature, the reversed temperature order, a matched learning-rate schedule with no task–temperature link, a task-ID-gated temperature, and retention of A and B after C and after reheating.

`reviews/idea-ledger.md` was read first. Its rules apply here: each card is labelled PRIMITIVE or IMPROVEMENT, names its strongest control, and every first test includes an old-task retention check. The reviewer listed PL02 (interacting hysterons) and PL28 (pinned fronts) as variants to test only after PL01, so cards that depend on PL01 say so. This node keeps to the reviewer's narrowing lines (optimizer state, meters, token retirement, teaching markets, relearnability, synonymous coding, gauge orbits). Temperature here is a hyperparameter of the write, not optimizer state. Ideas only, no GPU: every first test is a CPU toy.

**Literature check, 2026-11-25.** I queried alphaXiv `discover_papers` and the Hugging Face papers index on each mechanism and read the abstracts of the closest hits. Shared nearest prior art for branch P:
- *Preisach Attention* ([2605.23603](https://arxiv.org/abs/2605.23603)) uses learned (α, β) relays and an extremum stack as a sequence-model layer. That is in-context state over tokens, not weights that persist across a training stream.
- Differentiable Preisach for accelerator magnets ([2202.07747](https://arxiv.org/abs/2202.07747)) and Preisach/Prandtl neural networks ([2611.23240](https://arxiv.org/abs/2611.23240), [2001.01559](https://arxiv.org/abs/2001.01559)) model hysteresis in an external system.
- Recurring concept drift: MICE ([2610.36585](https://arxiv.org/abs/2610.36585)) recalls stored contexts at detected changes, and HMM states recovered from weights ([2607.27482](https://arxiv.org/abs/2607.27482)) are found after the fact. Both are memoryless in the drive, so they are the lookup-table control.

Shared nearest prior art for branch T:
- Training regimes in CL ([2006.06958](https://arxiv.org/abs/2006.06958), Mirzadeh et al.: learning rate, batch size and dropout change forgetting).
- Learning rates and catastrophic overtraining ([2604.13627](https://arxiv.org/abs/2604.13627)).
- Mini-batch noise lowers sharpness via dominant-subspace fluctuations ([2607.23012](https://arxiv.org/abs/2607.23012)).
- Scale-invariant thermodynamics of training ([2511.07308](https://arxiv.org/abs/2511.07308)).
- Infinite LR schedules and rewarming for continual pretraining ([2503.02844](https://arxiv.org/abs/2503.02844)).
- Spin-glass temperature chaos off equilibrium ([2011.09419](https://arxiv.org/abs/2011.09419), [2010.01214](https://arxiv.org/abs/2010.01214)).

None of these assigns each task a distinct noise temperature as its storage address, or recalls a task by reheating. "No direct hit" below means no paper in the top results did the card's specific thing. It is not proof of novelty.

Shared toys:
- **Mix toy.** Two regimes A and B: a 2-D input, 4-class labels whose rule rotates between A and B, and a drive h ∈ [0, 1] = fraction of B in each batch. A 2-layer MLP of width 64.
- **Ladder toy.** Three tasks from permuted 8×8 digits, a width-128 MLP, temperature T = η/B (learning rate over batch size), and fixed step counts.

---

## P. Return-point memory over the data mix (from PL01)

### P01 · Path-dependent target: the test that separates hysteresis from lookup — PRIMITIVE, H
- **Mechanism.** At the same mix h = 0.5, the correct weights depend on which regime the stream came from, as with a persisting user population or a sticky market regime. A Preisach bank encodes the path in its extremum stack. A memoryless gate on h, or a nearest-mixture lookup, cannot. This is the case the memory contract is for, and it must be won before any other P card matters.
- **Novelty vs prior art.** Recurring-drift methods ([2610.36585](https://arxiv.org/abs/2610.36585), [2506.14790](https://arxiv.org/abs/2506.14790), [2408.09324](https://arxiv.org/abs/2408.09324)) key on the current segment's statistics, not on the drive's history. Preisach Attention ([2605.23603](https://arxiv.org/abs/2605.23603)) is path-dependent over tokens, not over training. No direct hit for a path-dependent optimum as a CL benchmark.
- **Cheapest first test.** Mix toy where the label rule at h = 0.5 is A's after a descent from 1 and B's after an ascent from 0. Compare a 128-hysteron bank against the reviewer's equal-byte gated two-delta block on h, against the nearest-mixture lookup table, and against a GRU on the h history with equal parameters. Falsifier: the bank does not beat the lookup by ≥ 10 pp at h = 0.5, or the GRU matches it.
- **Retention check.** A accuracy at h = 0 and B accuracy at h = 1 after 20 nested reversals, against EWC and equal-budget replay.

### P02 · Prandtl–Ishlinskii play-operator weights — PRIMITIVE, H
- **Mechanism.** Replace bistable relays with continuous play (backlash) operators of widths r₁ … r_K. Each weight is w = w₀ + Σ_k c_k · play_{r_k}(h). A play operator ignores drive reversals smaller than its width and tracks larger ones. The sum has exact return-point memory and an analytic inverse, so the drive value that produced any stored weight can be computed. This is a smooth version of PL01 that gradients can train directly.
- **Novelty vs prior art.** PI operators are used to model and control actuators ([2504.12114](https://arxiv.org/abs/2504.12114), [2608.17791](https://arxiv.org/abs/2608.17791)) and inside networks that model hysteretic plants ([2611.23240](https://arxiv.org/abs/2611.23240)). No hit for PI-parameterised weights in a learner's own continual training.
- **Cheapest first test.** P01's toy, PI weights with K = 8 against the Preisach bank and the gated two-delta block at equal bytes. Falsifier: PI does not match the bank on P01 with fewer than half the training steps.
- **Retention check.** As P01, plus A accuracy after a C regime that moves h outside [0, 1].

### P03 · Learn the Preisach density, not the switches — PRIMITIVE, M
- **Mechanism.** Fix a grid of (α, β) thresholds and learn only the density μ(α, β), the weight each hysteron's delta carries, with a differentiable relaxation of the relays. The bank's memory then rests on fixed, interpretable switching points, while the learning concerns only what each switch contributes.
- **Novelty vs prior art.** Differentiable Preisach density fitting exists for magnets ([2202.07747](https://arxiv.org/abs/2202.07747)). Using it as the parameterisation of a continual learner is not found.
- **Cheapest first test.** Learned-density grid against a fully learned bank (thresholds and deltas) and against a shuffled-threshold bank. Falsifier: shuffled thresholds tie, which would mean the grid placement does nothing.
- **Retention check.** Nested-return accuracy on A and B.

### P04 · Design the bank from first-order reversal curves (FORC) — PRIMITIVE, M
- **Mechanism.** Magnetics identifies μ(α, β) from FORCs, and the Mayergoyz identification theorem says FORCs determine a Preisach system. Run the plain learner along FORC drive protocols on a small calibration stream (ramp h to α, reverse to β), record its loss surface, and place hysterons where the FORC diagram has mass. Capacity goes only to switching points the data stream actually has.
- **Novelty vs prior art.** No machine-learning hit for FORC (the query returned unrelated "reversal" papers). FORC analysis is standard in rock magnetism and magnetic materials.
- **Cheapest first test.** A FORC-placed bank of 32 hysterons against a uniform 32-hysteron grid and a uniform 128-hysteron grid. Falsifier: FORC-32 does not match uniform-128.
- **Retention check.** Nested-return retention on A and B.

### P05 · Vector drives on the regime simplex — PRIMITIVE, M
- **Mechanism.** With K regimes the drive is a point on a simplex, not a scalar. Multi-field return-point memory holds only under conditions on the drive paths ([2605.23781](https://arxiv.org/abs/2605.23781)). Build the bank from one scalar sub-bank per simplex edge, with drives restricted to paths along which RPM provably holds, and route off-edge paths through the nearest vertex.
- **Novelty vs prior art.** Multi-field RPM is a 2026 physics result. No CL use.
- **Cheapest first test.** Three regimes and random simplex walks. Compare the edge-decomposed bank against one bank on a single learned scalar projection and against the lookup table. Falsifier: the projection ties.
- **Retention check.** Accuracy at each vertex after 50 walks.

### P06 · No-passing couplings: avalanches that keep return-point memory — PRIMITIVE, H
- **Mechanism.** Interacting hysterons usually break RPM, which is why the reviewer gated PL02. Ferromagnetic, cooperative couplings satisfy the no-passing property, under which RPM provably holds (Sethna et al. 1993; Middleton 1992). Add only positive couplings between hysterons whose deltas agree on a probe set. One drive shift then flips a coherent avalanche (a whole regime at once), and the bank still restores exactly.
- **Novelty vs prior art.** The physics of interacting hysterons is active ([2512.15449](https://arxiv.org/abs/2512.15449), [2107.06556](https://arxiv.org/abs/2107.06556), [2508.08174](https://arxiv.org/abs/2508.08174)). No learning-system hit. This is the safe version of PL02.
- **Cheapest first test.** Cooperative-coupled against uncoupled against random-sign-coupled banks on P01. Falsifier: random-sign coupling restores as well as cooperative coupling, or coupling does not cut the drive excursion needed to switch a regime.
- **Retention check.** Nested-return accuracy, and the RPM error ‖w(return) − w(earlier)‖.

### P07 · AC demagnetisation as bounded unlearning — PRIMITIVE, H
- **Mechanism.** A decaying oscillating drive h(t) = h₀ + a(t)·sin(ωt), with a → 0, wipes every hysteron whose thresholds lie inside the swept band and leaves all others untouched. To unlearn a bad regime that lives in a range of h, demagnetise that band. RPM's wiping-out property says what is erased: only memories inside the band.
- **Novelty vs prior art.** Unlearning methods (selective synaptic dampening [2308.07707](https://arxiv.org/abs/2308.07707), gradient ascent) have no structural erasure bound. Searching "AC demagnetization erase memory" found only attention-erase papers. No direct hit.
- **Cheapest first test.** Poison regime B′ at h ∈ [0.6, 0.8]. Demagnetise that band, and compare with gradient ascent on B′ and with dampening at equal steps. Falsifier: demagnetisation harms A or B more than those controls.
- **Retention check.** A and B accuracy after unlearning, and B′ accuracy (should fall).

### P08 · Cycle-trained limit cycles (transition-graph memory) — PRIMITIVE, M
- **Mechanism.** Amorphous solids under repeated cyclic shear settle onto a limit cycle of their state transition graph, which then stores the cycle (Mungan, Sastry, Dahmen, Regev, PRL 2019). For streams that repeat a regime cycle (weekday/weekend, seasons), train the bank over a few cycles until its state sequence is periodic, then freeze the transition graph. Later perturbations that do not leave the cycle's basin are undone each period.
- **Novelty vs prior art.** No learning hit (the query returned materials-database papers). Periodic-drift CL uses explicit seasonality models.
- **Cheapest first test.** A cycle A→B→C→A with noise. Compare against a seasonality-indexed lookup with equal storage. Falsifier: the lookup recovers each regime as fast.
- **Retention check.** Per-regime accuracy after a one-off D perturbation.

### P09 · Hysteron widths matched to drive noise — IMPROVEMENT, M
- **Mechanism.** Narrow loops chatter under a noisy drive estimate; wide loops miss real reversals. Set the width distribution α − β from the measured drive noise, so the bank switches on real reversals and holds through noise. This is a Schmitt-trigger design rule applied to the bank.
- **Novelty vs prior art.** Schmitt-trigger hysteresis for regime switching is standard in control. IMPROVEMENT, because it tunes PL01.
- **Cheapest first test.** Sweep drive noise and compare matched widths against a fixed width and the shuffled-threshold bank. Falsifier: no width effect.
- **Retention check.** Retention on nested returns at each noise level.

### P10 · Inferred drive: the bank without a given h — PRIMITIVE, H
- **Mechanism.** In practice no one hands the learner h. Estimate it online as a scalar from a density-ratio classifier between a frozen reference buffer of A and the incoming batch, and drive the bank with the estimate. The bank's hysteresis then absorbs the estimator's noise (see P09).
- **Novelty vs prior art.** Task-free CL with shift detection ([2207.05080](https://arxiv.org/abs/2207.05080); Aljundi et al. 2019) switches models on detected changes. MICE ([2610.36585](https://arxiv.org/abs/2610.36585)) segments at detected changes. None feeds a continuous estimated drive into a hysteretic store.
- **Cheapest first test.** P01's toy with h hidden. Compare the inferred-h bank against MICE-style segment recall, and against the bank given the oracle h. Falsifier: inferred-h is more than 5 pp below the oracle and does not beat segment recall.
- **Retention check.** A/B retention on nested returns.

### P11 · Hysteron bank over an agent's lesson set — PRIMITIVE, M
- **Mechanism.** For an agent with a store of text lessons, give each lesson a hysteron: it enters the context when a scalar drive (for example the share of recent tasks from a user population, or a tool's recent failure rate) crosses α, and leaves when it falls below β. When the drive returns to an earlier extremum, the lesson set is exactly what it was then, with no re-curation.
- **Novelty vs prior art.** Lesson stores in this repo's prior pilots use retrieval, recency or leave-one-out credit (ledger M2, which was falsified against recency). A drive-hysteretic inclusion rule is not found. Nearest: Schmitt-style gating in agent controllers.
- **Cheapest first test.** A tabular agent with 30 lessons and two user populations alternating with nested reversals. Compare against recency and against a drive-threshold rule without hysteresis (α = β). Falsifier: α = β ties.
- **Retention check.** Success on population-A tasks after a B excursion.

### P12 · Rank-one hysteron deltas and the stack-depth capacity law — PRIMITIVE, M
- **Mechanism.** Each hysteron toggles one rank-one weight component, uvᵀ. The number of nested turning points a bank can restore is set by the number of distinct thresholds. Predict the capacity (restorable stack depth against hysteron count N and rank budget), and cap the bank at the knee.
- **Novelty vs prior art.** LoRA-style component banks exist, but none are indexed by a drive history. No hit.
- **Cheapest first test.** Sweep N ∈ {8, 32, 128} and the nesting depth. Falsifier: restorable depth does not grow with N.
- **Retention check.** Accuracy at each restored turning point.

### P13 · Congruent-loop transfer to a new regime pair — PRIMITIVE, L
- **Mechanism.** In a Preisach system, minor loops between the same drive extremes are congruent. Learn the bank on A↔B, then for a new pair A↔C reuse the loop shape and fit only the deltas. The bank's switching structure transfers; only its content is new.
- **Novelty vs prior art.** No hit for loop-shape transfer.
- **Cheapest first test.** A bank transferred from A↔B against a fresh bank on A↔C at equal steps. Falsifier: no sample-efficiency gain.
- **Retention check.** A↔B nested returns after learning A↔C.

## T. Temperature-chaos stacking (from PL07)

### T01 · Descending ladder with data-free reheating — PRIMITIVE, H
- **Mechanism.** This is PL07 made exact. Tasks 1, 2, 3 are trained at T, T/4 and T/16 (T = η/B). Recall task k by a data-free reheating phase at T_k: SGD on the model's own predictions over random inputs at temperature T_k for a fixed number of steps.
- **Novelty vs prior art.** Training-regime work ([2006.06958](https://arxiv.org/abs/2006.06958)) changes the regime globally. Rewarming ([2503.02844](https://arxiv.org/abs/2503.02844)) restarts learning on new data. Neither uses temperature as a per-task address or data-free reheating as recall. Spin-glass temperature chaos ([2011.09419](https://arxiv.org/abs/2011.09419)) is the physics.
- **Cheapest first test.** Ladder toy with all of the reviewer's controls: fixed temperature, reversed order, a matched LR schedule with no task–temperature link, a task-ID-gated temperature, and reheating at a random temperature. Falsifier: reheating at T₁ recovers task 1 no better than reheating at a random temperature.
- **Retention check.** Tasks 1 and 2 after task 3 and after each reheat.

### T02 · Temperature-gap rule from the chaos exponent — IMPROVEMENT, M
- **Mechanism.** Temperature chaos makes the overlap between states at T and T′ decay beyond a length that shrinks with |T − T′|. Measure the overlap of solutions trained at a pair of temperatures as a function of the ratio T/T′, and set the ladder spacing at the ratio where the overlap stops changing. This turns PL07 into a design rule rather than a guessed factor of 4.
- **Novelty vs prior art.** The reviewer marked the root's scaling laws (PL12–14) as diagnostics. This one is used only to set T01's ladder, so it is labelled IMPROVEMENT.
- **Cheapest first test.** Ratio sweep {2, 4, 8, 16}. Falsifier: retention after the ladder is flat in the ratio.
- **Retention check.** Ladder-end accuracy per task.

### T03 · Curvature-band storage — PRIMITIVE, H
- **Mechanism.** Spin-glass memory survives cooling because lower temperatures rearrange only short length scales. In SGD the analogue is that noise at T explores only directions with curvature below about 1/T, while sharper directions stay settled ([2607.23012](https://arxiv.org/abs/2607.23012) shows noise acts on dominant-subspace sharpness). Predict that each task's weight change lies in a distinct Hessian band, the lower-temperature tasks in sharper bands, and write explicitly into those bands (project task k's update onto its band).
- **Novelty vs prior art.** Spectral CL methods (GPM, Adam-NSCL) project away from old gradient subspaces, not into curvature bands set by temperature. No direct hit.
- **Cheapest first test.** Measure the overlap of each task's Δw with Hessian eigenbands after T01. Then run explicit band projection at a fixed temperature against GPM. Falsifier: band overlaps do not separate by temperature.
- **Retention check.** All three tasks after the ladder.

### T04 · Rejuvenation instead of reset — PRIMITIVE, M
- **Mechanism.** In aging glasses, cooling restarts aging at the new scale, which restores mobility without erasing older structure. When a model's plasticity decays (aging), cool it, lowering T by a step, instead of resetting units. Predict that new-task learning speed comes back while old tasks stay.
- **Novelty vs prior art.** Plasticity loss is fixed by resets (continual backprop, ReDo, FIRE [2602.08040](https://arxiv.org/abs/2602.08040)) or by shrink-and-perturb. No hit for cooling as the fix. Nearest internal: chemistry #61, aging and rejuvenation by time.
- **Cheapest first test.** A 20-task stream where plasticity decays. Compare cooling steps against continual backprop at an equal compute budget. Falsifier: lower new-task speed or lower retention than continual backprop.
- **Retention check.** First-5-task accuracy at the end.

### T05 · Temperature cycling as data-free rehearsal — PRIMITIVE, M
- **Mechanism.** Short periodic visits to each stored temperature (T₁ → T₃ → T₁ …), with no data, keep each task's memory refreshed, like temperature-cycling protocols in spin glasses. Rehearsal then costs compute but needs no stored examples.
- **Novelty vs prior art.** Data-free rehearsal by generators or model inversion exists. Rehearsal by temperature alone is not found.
- **Cheapest first test.** Against generative replay and against reheating at a random temperature, at equal compute. Falsifier: random-temperature visits tie.
- **Retention check.** All tasks after 10 later tasks.

### T06 · Maximum-entropy temperature ladder for RL skills — PRIMITIVE, M
- **Mechanism.** In maximum-entropy RL the entropy coefficient α is a temperature. Learn each new skill at a lower α, and recall an old skill by raising α back to its level, with no skill ID.
- **Novelty vs prior art.** Continual RL surveys ([2506.21872](https://arxiv.org/abs/2506.21872)) cover regularisation and replay. α schedules are tuned for exploration, not as storage addresses. No hit.
- **Cheapest first test.** Gridworld with three goals, SAC-style tabular soft Q. Compare against fixed α and against a goal-ID-conditioned policy. Falsifier: recall at α_k is no better than a random α.
- **Retention check.** Success on goals 1 and 2 after goal 3.

### T07 · Effective temperature η·λ in normalised networks — IMPROVEMENT, M
- **Mechanism.** In scale-invariant (normalised) networks, the equilibrium effective temperature is set by learning rate × weight decay ([2511.07308](https://arxiv.org/abs/2511.07308)). Build the ladder on η·λ rather than η/B, so it stays exact under normalisation.
- **Novelty vs prior art.** IMPROVEMENT on T01's parameterisation.
- **Cheapest first test.** T01 with BatchNorm, comparing an η/B ladder against an η·λ ladder. Falsifier: no difference.
- **Retention check.** As T01.

### T08 · Scale-separated merging — PRIMITIVE, M
- **Mechanism.** Task vectors trained at well-separated temperatures from a shared base should live at different curvature scales (T03) and interfere less when summed. Train task deltas in parallel at different temperatures, then merge.
- **Novelty vs prior art.** Merging interference work (TIES [2306.01708](https://arxiv.org/abs/2306.01708), RI [2603.13467](https://arxiv.org/abs/2603.13467)) resolves sign and magnitude conflicts after training. No hit for choosing training temperatures to make deltas mergeable.
- **Cheapest first test.** Three tasks: deltas trained at one temperature against deltas trained at three. Compare simple addition and TIES. Falsifier: no gain over same-temperature TIES.
- **Retention check.** Per-task accuracy of the merged model, and base-task accuracy.

### T09 · Thermal hysterons: temperature as the Preisach drive — PRIMITIVE, H
- **Mechanism.** This joins the node's two lines. Use the training temperature itself as h for a Preisach bank: each hysteron switches on when T crosses α and off below β. Then T01's reheating has a hard guarantee, because returning T to T_k restores the bank state of task k exactly, while the dense weights carry the scale-separated part.
- **Novelty vs prior art.** None for either half in CL. The combination is the strongest test of whether temperature addresses can be made exact.
- **Cheapest first test.** Compare T01 alone, the bank alone with h = task index, and the thermal bank. Falsifier: the thermal bank does not beat the better of the other two.
- **Retention check.** Tasks 1 and 2 after task 3 and after reheating.

### T10 · Step versus ramp between temperatures — IMPROVEMENT, L
- **Mechanism.** In spin glasses, rejuvenation depends on the size of the temperature step. Compare stepping T between tasks against ramping it, to find whether separation needs abrupt quenches.
- **Novelty vs prior art.** LR-schedule shape is well studied for single tasks. IMPROVEMENT.
- **Cheapest first test.** Step against linear ramp at equal step counts. Falsifier: no difference.
- **Retention check.** Ladder-end accuracy.

### T11 · Snapshot library from reheats — IMPROVEMENT, M
- **Mechanism.** After the ladder, reheat to each T_k briefly and snapshot. Serve the snapshots through P10's inferred drive or a small router. This trades storage for exact recall and bounds what T01 can claim.
- **Novelty vs prior art.** Snapshot ensembles exist. IMPROVEMENT, used as the ceiling arm for T01.
- **Cheapest first test.** Snapshots against per-task checkpoints taken during training (the oracle). Falsifier: reheated snapshots more than 5 pp under the oracle.
- **Retention check.** Per-task accuracy.

### T12 · Noise-shape addresses instead of noise level — PRIMITIVE, M
- **Mechanism.** Rather than a scalar T, give each task a distinct anisotropic noise covariance during its training: Gaussian noise injected in a random task-specific subspace. Recall by reheating with that covariance. There are many more addresses than with a scalar ladder, which runs out at the noise floor.
- **Novelty vs prior art.** Noise-injection regularisers are isotropic or fixed. No hit for task-addressed noise shapes.
- **Cheapest first test.** Six tasks with shape addresses against a six-rung scalar ladder. Falsifier: no gain at 6 tasks.
- **Retention check.** All six tasks at the end.

### T13 · Temperature ladder for agent lesson curation — PRIMITIVE, L
- **Mechanism.** An agent's curator accepts or rejects lesson edits by a Metropolis rule at temperature T on the measured score change. Early lessons are accepted at high T (broad, general); later lessons at low T, which keeps only precise edits that do not disturb the broad ones. Raising T reopens the general layer for revision.
- **Novelty vs prior art.** Curators in prior pilots (ACE-style) accept greedily. Simulated-annealing curation for agents is not found.
- **Cheapest first test.** A tabular agent with 3 task phases. Compare annealed curation against greedy and against a fixed-T Metropolis curator. Falsifier: fixed T ties.
- **Retention check.** Phase-1 success after phase 3.

---

## Ranked deeper questions

1. **Does a path-dependent optimum exist in real streams, and does hysteresis beat lookup there?** If P01 fails, the whole P branch collapses to a gated lookup, which the reviewer already holds as a control. Run P01 with the reviewer's full control set first.
2. **Does SGD temperature separate tasks by curvature scale?** T03's band-overlap measurement decides whether T01 has a mechanism or is a schedule effect. If bands do not separate, T01, T05, T08 and T09 fall with it.
3. **Can a drive be inferred well enough to run the bank without labels?** P10 sets whether return-point memory works task-free. Its gap to the oracle drive is the number that matters.
4. **Can exact erasure (P07) and exact restoration (P01) come from one structure?** If demagnetisation unlearns one band without touching others, the bank becomes a controlled store for both writes and deletions, which no current CL mechanism guarantees.
5. **Is temperature a usable address beyond 3–4 tasks?** The scalar ladder hits a noise floor. T12 (noise shapes) and T09 (thermal hysterons) are the two ways past it. Compare both at 6+ tasks.
