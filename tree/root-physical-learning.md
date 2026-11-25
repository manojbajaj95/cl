# Root: physical learning — continual-learning primitives borrowed from physics and materials

New root node of the idea tree. Scope: mechanisms that make matter remember, forget, heal or switch (hysteresis, annealing and glasses, phase transitions, error-correcting codes, reaction–diffusion, conservation laws), turned into write rules, storage formats and fleet dynamics for models and agents.

Written after reading `reviews/idea-ledger.md` and `reviews/flood-triage.md`. Deliberately stays away from the reviewer's narrowing lines: no optimizer-state ideas, no meters/observability/forecast dashboards, no token retirement, no teaching markets, no relearnability read-outs, no synonymous coding or gauge/symmetry orbits. Cards are also screened against the existing pools so they are not renames: `ideas/flood/physics-math.md` (coercive weights, shape memory, spin echo, kinetic proofreading, parallel tempering, glassy aging clocks, MBL disorder, Kuramoto, solitons, RG), `ideas/flood/chemistry.md` (vitrimers, sorption hysteresis, yield surfaces, aging/rejuvenation, nucleation seeds, tiles), `ideas/flood/info-coding.md` (parity, LDPC, fountain, WOM, stuck-at, interleaving) and `tree/thermodynamics-of-remembering.md` (mismatch cost, Kovacs, Mpemba, counterdiabatic, spinodal). Where a card sits near one of these, the nearest internal card is named.

Ideas only. No GPU. Every first test is a CPU toy (linear/MLP on split or permuted MNIST-style data, or a small tabular agent) and every first test carries an **old-task retention check**: the old tasks are re-measured after the new learning, against an equal-budget control.

**Literature check method.** Each card was searched on alphaXiv (`discover_papers`) and the Hugging Face papers index (2026-11-25) with 1–3 queries on the mechanism plus "neural network / continual learning / agents". "No direct hit" means no paper in the top results used the mechanism for neural continual learning; it is not proof of novelty. Physics sources named are the canonical ones for the mechanism.

Labels follow the ledger: **PRIMITIVE** (a new kind of write rule, storage format or dynamics) or **IMPROVEMENT** (a better setting of a known one). Ambition: H/M/L.

---

## A. Hysteresis and return-point memory

### PL01 · Return-point memory over a data-mixture drive (Preisach hysteron bank) — PRIMITIVE, H
- **Mechanism.** Treat the data mixture (fraction of regime B vs regime A, or any scalar shift coordinate) as a drive field h. A block of parameters is replaced by a Preisach bank: many bistable hysterons with up/down thresholds (α≥β) whose states select one of two weight deltas. Sweeping h up and down sets hysterons; the Preisach *wiping-out* property means returning h to a past extremum restores the exact earlier state, erasing only the inner loops. Old regimes are recovered by re-traversing the drive, not by replay.
- **Novelty vs prior art.** Physics: Preisach model; return-point memory in disordered magnets and sheared amorphous solids (Keim, Paulsen, Zeravcic, Sastry, Nagel, "Memory formation in matter", RMP 2019); multi-field RPM (alphaXiv 2605.23781); fluidic hysterons (2607.15122). ML: hysteresis activation functions (2411.10573) and hysteresis-model surrogates (Bouc–Wen, 2411.02776) model hysteresis, they do not use it as a CL storage format. Nearest internal: physics #1 coercive weights (single threshold per weight, no nested-loop restoration) and chemistry #42 sorption hysteresis. Gap: the nested-loop/wiping-out guarantee as the memory contract. No direct hit.
- **Cheapest first test.** Two-regime linear regression whose optimum depends on h; train an MLP with a 256-hysteron bank vs a plain block of equal parameters under a drive h(t) with nested reversals. Falsifier: after returning h to a past extremum, the bank is not closer to its earlier weights/outputs than the plain block.
- **Retention check.** Accuracy on regime A at h=0 after a full excursion to h=1 and back, vs plain fine-tune and vs EWC at equal compute.

### PL02 · Interacting-hysteron transition graphs that count and order regimes — PRIMITIVE, H
- **Mechanism.** Couple hysterons so a switch in one shifts the thresholds of others (van Hecke-style interacting hysterons). The resulting transition graph can count drive cycles and store the *order* of past regimes. Use it as a tiny discrete state register beside the network: the register state indexes which consolidated delta is active, so the model knows "B came after A, twice" without a task ID oracle.
- **Novelty vs prior art.** Physics: Kwakernaak & van Hecke, counting and sequential information processing in mechanical metamaterials (PRL 2023); hysteron pathways (2607.21974 three-body rotors). ML: finite-state controllers and task-ID inference exist, but none derived from designed hysteron graphs driven by the data stream itself. No direct hit. Nearest internal: chemistry #59 interlocking metamaterials (geometry, not counting).
- **Cheapest first test.** Stream A,B,A,C with noisy drive; compare a 6-hysteron designed graph vs an equal-size learned GRU task-inference head. Falsifier: graph state no better at selecting the correct delta than the GRU.
- **Retention check.** Per-regime accuracy on A after C, with selected delta, vs single shared model.

### PL03 · Noise-sustained multiple transient memories — PRIMITIVE, M
- **Mechanism.** Driven suspensions under cyclic shear of several amplitudes keep all of them transiently, then forget all but the largest at steady state — unless noise is added, which keeps several memories indefinitely (Keim & Nagel 2011; Paulsen et al. 2014). Transfer: in cyclic curricula (A,B,A,B with different shift magnitudes), inject a calibrated amount of label-free parameter noise per cycle to keep the memories of smaller-amplitude shifts from being absorbed by the largest one.
- **Novelty vs prior art.** Noise injection for plasticity (shrink-and-perturb, Ash & Adams 2020) and for flatness is known; the claim here is specific: a noise *window* exists in which multiple cyclic task memories coexist, absent at zero and at high noise. HF search on "multiple transient memories noise" returned nothing on learning. Nearest internal: thermodynamics node relaxation curricula (time, not noise window).
- **Cheapest first test.** Three tasks with distinct interference strength cycled 50 times; sweep noise σ. Falsifier: retention of the weakest task is monotone in σ (no window).
- **Retention check.** End-of-run accuracy on all three tasks vs replay at equal sample budget.

### PL04 · Bean critical-state penetration of updates through depth — PRIMITIVE, M
- **Mechanism.** In type-II superconductors a field penetrates only as deep as the critical current allows; the remnant profile records the field history (Bean 1962). Rule: each layer has a critical gradient J_c; a layer moves only by the excess of its incoming error signal over J_c, and the excess (not the full signal) is passed deeper. Small shifts touch only the outermost layers; big shifts penetrate deeper; the depth profile of past penetration is itself a history record.
- **Novelty vs prior art.** Layer freezing/surgical fine-tuning (Lee et al. 2022 "Surgical fine-tuning") chooses layers by hand; gradient clipping is per-step magnitude, not a depth-penetrating front. Nearest internal: physics #1 coercive weights (per-weight threshold, no front). No direct hit for Bean/critical-state learning.
- **Cheapest first test.** 6-layer MLP on input-shift vs label-shift tasks; compare critical-state rule vs surgical fine-tuning with oracle layer choice. Falsifier: no better than oracle surgical fine-tuning on new-task accuracy at equal old-task loss.
- **Retention check.** Old-task accuracy after each shift, plus check that deep layers' drift is bounded.

### PL05 · Rainflow-counted fatigue budget for old skills — PRIMITIVE, M
- **Mechanism.** Metals fail by cycles, not by mean load; rainflow counting decomposes an irregular load history into closed cycles, and Miner's rule sums their damage. Use rainflow counting on each old task's *loss trajectory* during later training to schedule consolidation actions (anchor, replay one batch) when accumulated cycle damage crosses a budget. This is a control rule, not a dashboard: it triggers writes.
- **Novelty vs prior art.** Fatigue + ML papers predict material life (2406.01523); none applies rainflow to a model's own loss history. Replay schedulers trigger on loss level or interval (e.g., MIR, Aljundi 2019), not on cycle amplitude. No direct hit. Risk: predictor pilots died on variance in prior rounds; this card must win as a *trigger*, judged by retention per replay batch.
- **Cheapest first test.** Fixed replay budget of N batches; rainflow trigger vs loss-threshold trigger vs periodic. Falsifier: rainflow ≤ loss-threshold on old-task retention per batch.
- **Retention check.** Old-task accuracy at end with equal replay count.

## B. Annealing, glasses and jamming

### PL06 · Kinetically constrained (East/Fredrickson–Andersen) write permission — PRIMITIVE, H
- **Mechanism.** In kinetically constrained models a site may flip only if a neighbour is excited; this alone yields glassy, heterogeneous, history-dependent dynamics. Arrange parameter blocks on a fixed chain/graph; a block may update only if a neighbour block is "excited" (its local loss contribution exceeds a threshold). Learning spreads as facilitation fronts from where the new data bites; regions with no excited neighbours are dynamically frozen without any importance estimate or task ID.
- **Novelty vs prior art.** Physics: KCM theory (2212.05132; book 2412.13634). ML: masks from importance (PackNet, SPG) or sparse fine-tuning; none uses a neighbour-facilitation constraint. alphaXiv query returned only physics. No direct hit.
- **Cheapest first test.** MLP with 32 blocks on a ring; split-task stream. Compare to random sparse masks with the same fraction updated. Falsifier: no retention gain at equal new-task accuracy.
- **Retention check.** Old-task accuracy after each new task; plus fraction of blocks ever updated.

### PL07 · Temperature-chaos stacking (rejuvenation and memory) — PRIMITIVE, H
- **Mechanism.** In spin glasses, aging at T1, cooling to T2 starts fresh aging (rejuvenation), and reheating to T1 recovers the T1 memory (Jonason et al., PRL 1998), because different temperatures probe different length scales. Train each new task at a strictly lower SGD noise temperature (batch noise/LR ratio) than the last; recall an old task by briefly returning to its temperature with no data.
- **Novelty vs prior art.** SGD temperature (LR/batch) is known to set solution scale; cooldown/rewarm is crowded (memory note). The claim that a *descending temperature ladder* stores tasks at separate scales and that re-heating without data recalls one is untested; HF hit 2503.18371 ("Do your best and get enough rest") is about rest schedules, not temperature separation. Nearest internal: chemistry #61 aging/rejuvenation (time-coded) — this card is temperature-coded.
- **Cheapest first test.** Three tasks at T, T/3, T/9; then a data-free warm phase at T. Falsifier: no recovery of task 1 above a matched data-free warm phase at a random temperature.
- **Retention check.** All tasks after the ladder vs constant-temperature sequential training.

### PL08 · Vapour-deposition growth of new capacity — IMPROVEMENT, M
- **Mechanism.** Ultrastable glasses form when deposited slowly onto a substrate near 0.85 Tg: only the free surface is mobile, so each thin layer equilibrates before burial (Swallen et al., Science 2007). Each new task gets a thin new layer of capacity that is fully mobile; the layer just below is mobile at reduced rate; deeper layers are frozen. The control knob is deposition rate (examples per new unit) relative to surface relaxation.
- **Novelty vs prior art.** Progressive nets (Rusu 2016) and dynamically expandable networks grow capacity; none prescribes a deposition-rate law tied to surface mobility. HF/alphaXiv: no learning hits. Honest label: improvement on progressive growth.
- **Cheapest first test.** Sweep units added per task and mobility of the sub-surface layer. Falsifier: retention independent of deposition rate at fixed final size.
- **Retention check.** Old-task accuracy vs progressive nets of equal final size.

### PL09 · Swap moves between non-equivalent units — PRIMITIVE, M
- **Mechanism.** Swap Monte Carlo equilibrates glass formers by exchanging *different-sized* particles, reaching states local moves cannot (Ninarello, Berthier, Coslovich, PRX 2017). Propose swaps of two non-equivalent hidden units' incoming weights (a function-changing, non-local move), accept by Metropolis on joint (new loss + anchor on old outputs). Swaps relocate old-task features into units the new task does not need.
- **Novelty vs prior art.** Closest: Monte Carlo parameter swapping to bypass memorization in grokking (alphaXiv 2608.01833) — single-task, not CL; Git Re-Basin (2209.04836) uses function-preserving permutations (gauge line, avoided here). CL use of non-equivalent swaps: no hit.
- **Cheapest first test.** Two-task MLP; SGD + swaps vs SGD + equal number of extra SGD steps. Falsifier: no retention gain.
- **Retention check.** Task-1 accuracy after task 2.

### PL10 · Isostatic contact counting for old-task constraints — PRIMITIVE, M
- **Mechanism.** Near the jamming transition, the network's behaviour is set by counting active constraints vs degrees of freedom (Maxwell counting); deep nets show a jamming transition at the overparameterization threshold (Geiger, Spigler et al. 2019). Keep a running count of "contacts" — old-task examples still at nonzero hinge loss — per parameter subspace, and allocate the new task only to subspaces below isostatic count.
- **Novelty vs prior art.** Jamming in DNN loss landscapes is known (Spigler et al., J. Phys. A 2019); null-space projection CL (2611.29269, Adam-NSCL) uses gradient subspaces, not contact counts. No direct hit for contact-count allocation.
- **Cheapest first test.** Hinge-loss MLP near the jamming width; compare contact-count allocation vs null-space projection at equal rank. Falsifier: no difference.
- **Retention check.** Old-task margin and accuracy.

### PL11 · Recrystallization by stored churn — PRIMITIVE, M
- **Mechanism.** Deformed metals recrystallize where stored dislocation energy is highest. Define a unit's stored energy as its path length divided by its net displacement (churn: much movement, little progress). After each task, re-initialize and regrow only the highest-churn units; low-churn units, which hold settled knowledge, stay.
- **Novelty vs prior art.** Continual backprop (Dohare 2024), ReDo, FIRE (2602.08040) reset by utility or dormancy, not by path/displacement ratio. Churn criterion: no hit. Nearest internal: chemistry #18 dislocation glide (admission, not reset).
- **Cheapest first test.** Permuted-task stream with 2% resets per task; churn vs utility vs random selection. Falsifier: churn ≤ utility on both plasticity and retention.
- **Retention check.** Old-task accuracy after resets.

### PL12 · Bond-chaos overlap length as the safe edit radius — PRIMITIVE, L
- **Mechanism.** In spin glasses, a small change δJ to couplings leaves the ground state intact below an overlap length ℓ ~ δJ^(−1/ζ) and scrambles it beyond (Bray & Moore 1987). Hypothesis: for a model, a data perturbation of strength δ leaves outputs intact within an input-space radius that shrinks as a power of δ; edits should be localized below that radius, giving a principled scope for edits.
- **Novelty vs prior art.** Editing scope radii exist (GRACE codebook radius, Hartvigsen 2023) as tuned hyperparameters; a chaos exponent linking edit strength to scope is not reported. No hit.
- **Cheapest first test.** Fine-tune with perturbation strength δ; measure output change vs distance from the edit set; fit ℓ(δ). Falsifier: no power law / no sharp crossover.
- **Retention check.** Old-task accuracy outside ℓ.

### PL13 · Nucleation threshold for sparse edits — PRIMITIVE, M
- **Mechanism.** A metastable phase survives until a nucleus exceeds critical size r* ∝ σ/Δμ. Hypothesis: an old skill survives sparse fine-tuning until the edited parameter region exceeds a critical size that falls with task conflict; below it the edit is absorbed, above it the new task "crystallizes" and spreads. Rule: choose sparse-mask size just above r* for the new task and no more.
- **Novelty vs prior art.** Sparse fine-tuning retention is studied (sparse memory fine-tuning; memory note says densely covered); a sharp, conflict-dependent nucleation threshold is a new falsifiable law. Nearest internal: chemistry #19 seeded nucleation (seed choice, not size law). No hit for nucleation theory of forgetting.
- **Cheapest first test.** Sweep mask size at three conflict levels. Falsifier: smooth forgetting curves with no conflict-dependent knee.
- **Retention check.** Old-task accuracy vs mask size.

## C. Phase transitions and collective switching

### PL14 · Kibble–Zurek switch speed — PRIMITIVE, H
- **Mechanism.** Quenching through a symmetry-breaking transition leaves defects with density ∝ τ_Q^(−ν/(1+zν)). When a new task forces a representational transition (a new feature split), switching fast leaves "defects": domains of units with inconsistent assignment (mixed concepts, dead units). Prescribe task-switch speed (mixture ramp time) from the measured KZ exponent to minimize defects within a time budget.
- **Novelty vs prior art.** Phase transitions in training are catalogued (model zoo 2504.18072; grokking as phase transition 2604.04655, 2210.15435); adiabatic switching is physics #4 (gap-scheduled). KZ defect counting as a CL quantity: no hit in either index.
- **Cheapest first test.** Teacher–student task requiring a symmetry break; vary ramp time; count units whose sign assignment disagrees with the majority domain. Falsifier: no power law in defect count vs ramp time.
- **Retention check.** Old-task accuracy as a function of ramp time at equal total steps.

### PL15 · Transition-order triage: fork on first-order shifts, share on continuous ones — PRIMITIVE, M
- **Mechanism.** Fit a learned order parameter (e.g., top principal component of features) as the mixture shifts; a jump (first-order, with coexistence) means the old and new solutions are distinct phases and must get separate capacity; a continuous change means they can share. The Maxwell lever rule sets the capacity split.
- **Novelty vs prior art.** ML for phase detection (Carrasquilla & Melko 2017; Wetzel 2017) and expansion triggers on loss spikes exist; using transition *order* to choose fork vs share is not found. Nearest internal: thermodynamics spinodal card (phase separation in weights, not triage).
- **Cheapest first test.** Two families of shifts (continuous rotation vs label swap); triage vs always-share vs always-fork at equal parameters. Falsifier: triage not better than the best fixed policy on both families.
- **Retention check.** Old-task accuracy per family.

### PL16 · Absorbing-state threshold for rare-skill persistence (agents) — PRIMITIVE, M
- **Mechanism.** In a contact process, activity dies out below a critical infection rate (directed percolation). Model an agent's rare skill as active in contexts where it was recently used; it "infects" neighbouring contexts through use. Set the minimum rehearsal rate per skill just above the measured critical rate, so the skill never falls into the absorbing (forgotten) state, at minimal cost.
- **Novelty vs prior art.** Agent skill-library staleness work (Repo2Skill-Evo 2608.21964, pre-commit skill gating 2608.05810) detects or gates; spaced repetition schedules per item. Using an absorbing-state critical rate as the rehearsal floor: no hit.
- **Cheapest first test.** Tabular agent with 50 skills, Zipf usage; fixed rehearsal budget allocated by critical-rate rule vs uniform vs Leitner. Falsifier: no gain in surviving skills.
- **Retention check.** Success on all 50 skills at the end vs no-rehearsal agent.

### PL17 · Committed-minority reserve for fleets — PRIMITIVE, M
- **Mechanism.** In naming games, a committed minority above ~10% flips a population's convention (Xie et al. 2011). Keep a small, computed fraction of agents that never adopt a new skill version; if the new version fails, the reserve can tip the fleet back, and while the new version is good the reserve is below the tipping threshold so it does not block adoption.
- **Novelty vs prior art.** LLM populations show convention formation and committed-minority tipping (Ashery, Aiello, Baronchelli 2025; topology effects 2610.31165) — as social phenomena, not as a designed rollback reserve for continual learning. Canary deployments are the engineering analogue without the threshold law.
- **Cheapest first test.** 100 tabular agents with gossip learning; inject a bad update; measure recovery time vs reserve fraction. Falsifier: no reserve fraction gives both fast adoption of good updates and recovery from bad ones.
- **Retention check.** Fleet success on old tasks after a bad update.

## D. Error-correcting codes (non-overlapping with info-coding pool)

### PL18 · Topological storage of a skill bit in weight-sign loops — PRIMITIVE, H
- **Mechanism.** In the toric code, a logical bit is a product over a non-contractible loop; no local error changes it, only a string spanning the lattice. Lay a small weight block on a 2-D torus; read a protected skill switch as the parity of signs along a loop, with stabilizer penalties keeping local plaquette parities even. Later sparse/local fine-tuning cannot flip the logical bit without a system-spanning change.
- **Novelty vs prior art.** ML is used to *decode* topological codes (2608.15760) and topological reservoirs exist (2611.24013); bit-wise weight training (2202.09571) is unencoded. Storing a learned skill as a logical operator inside weights: no hit. Nearest internal: physics #26 winding-number bits (invariant over inputs, not a code in weights).
- **Cheapest first test.** Gate between two heads by the loop parity; fine-tune on new task with random local updates of growing support. Falsifier: protected bit flips at the same support as an unencoded sign bit.
- **Retention check.** Old-head selection and accuracy after new training.

### PL19 · Erasure conversion with dual-rail heads — PRIMITIVE, H
- **Mechanism.** Neutral-atom and dual-rail qubits convert errors into detectable erasures, which need about half the redundancy of unknown errors. Give each old-task output a dual-rail pair (valid = exactly one rail high); training damage tends to push pairs into invalid states (00/11) rather than silently flipping. The system then repairs only erased outputs, with half the redundancy.
- **Novelty vs prior art.** Selective prediction / abstention exists; erasure conversion as a CL storage format with a repair budget: no hit (search on "erasure conversion dual rail" returned only QEC). Nearest internal: info-coding erasure/fountain cards assume erasures are given; this card manufactures them.
- **Cheapest first test.** Old task with dual-rail heads vs plain heads + parity; measure fraction of errors flagged after new-task fine-tuning. Falsifier: silent flips not reduced.
- **Retention check.** Old-task accuracy after repair at equal redundancy.

### PL20 · Concatenated consolidation with a threshold — PRIMITIVE, M
- **Mechanism.** The threshold theorem: if each level's error rate is below p_th, concatenation suppresses logical error doubly-exponentially. Build consolidation levels that each correct the level below on a fixed period (level 1 every 10 steps, level 2 every 100, …); predict flat retention when per-period damage is below threshold and collapse above.
- **Novelty vs prior art.** Benna–Fusi cascades and complementary-learning systems use multi-timescale transfer, not error correction with a threshold. Learned code concatenation (2604.14931) is for quantum codes. No direct hit.
- **Cheapest first test.** Three levels on a linear model; sweep per-period interference. Falsifier: no threshold behaviour.
- **Retention check.** Old-task accuracy over long streams vs Benna–Fusi cascade.

### PL21 · Common-mode-immune (decoherence-free) encoding — PRIMITIVE, M
- **Mechanism.** Decoherence-free subspaces store information in combinations immune to collective noise. Much of forgetting is common-mode (shared drift of a representation, bias shifts). Encode old-task read-outs differentially: each logit is a difference of two paired units that drift together under common updates.
- **Novelty vs prior art.** Spurious-forgetting and bias-shift work (e.g., CBA 2308.06925, 2610.08718) corrects common drift after the fact. A storage format immune by design: no hit.
- **Cheapest first test.** Paired vs unpaired heads under a task that induces global shift. Falsifier: equal drift.
- **Retention check.** Old-task accuracy.

### PL22 · Minimum-bandwidth regeneration of a damaged module — PRIMITIVE, M
- **Mechanism.** Regenerating codes (Dimakis et al. 2010) repair a lost storage node by downloading small pieces from many others, at much less bandwidth than full decoding. Store old-task knowledge spread over modules so a damaged module can be rebuilt by small functional downloads (a few probe outputs) from the intact ones.
- **Novelty vs prior art.** Info-coding pool covers erasure coding; the repair-bandwidth trade-off is new to CL. No hit on "regenerating codes neural network".
- **Cheapest first test.** 8 modules; damage one by new-task training; repair from k probe outputs per module. Falsifier: repair cost equals full distillation.
- **Retention check.** Old-task accuracy after repair.

### PL23 · Grid (GKP-style) snap-back for continuous weights — IMPROVEMENT, M
- **Mechanism.** GKP codes correct small continuous displacements by rounding modulo a grid. Keep critical old-task weights on a lattice; periodic snap-back during later training corrects drift smaller than half the spacing; spacing chosen from measured drift.
- **Novelty vs prior art.** Lattice quantization and per-axis deltas (2512.19720) compress; using modular snap-back as correction during continual training: no hit. Honest label: improvement on quantization.
- **Cheapest first test.** Snap vs anchor penalty at equal compute. Falsifier: anchor ≥ snap.
- **Retention check.** Old-task accuracy.

### PL24 · Bias the forgetting noise, then code against one type — PRIMITIVE, M
- **Mechanism.** Cat qubits suppress bit-flips exponentially so only phase errors need a cheap repetition code. Shape the output parameterization (e.g., margin-preserving heads) so forgetting shows up mostly as confidence loss, not label flips, then protect only against the remaining type.
- **Novelty vs prior art.** Biased-noise codes are QEC-only in search results; no CL hit.
- **Cheapest first test.** Measure error-type ratio for two parameterizations. Falsifier: no bias achievable.
- **Retention check.** Old-task accuracy with cheap code vs full code.

## E. Reaction–diffusion and excitable media

### PL25 · Turing-spaced skill domains — PRIMITIVE, H
- **Mechanism.** Activator–inhibitor dynamics on a lattice of modules: a new task excites a local activator; long-range inhibition spaces skill domains so they do not overlap. Capacity allocation emerges without a router.
- **Novelty vs prior art.** Graph reaction–diffusion networks (GREAD 2211.14208) and Turing fusion (2606.01615) use RD as layers; noise-field spatial functionalization (2606.24588) is closest but is not activator–inhibitor CL allocation. Nearest internal: immuno-dev morphogen gradients (gradients, not Turing). No direct hit.
- **Cheapest first test.** 64 modules on a ring; compare with k-WTA routing. Falsifier: equal overlap and retention.
- **Retention check.** Old-task accuracy.

### PL26 · Excitable refractory writes — PRIMITIVE, M
- **Mechanism.** In excitable media (FitzHugh–Nagumo, Belousov–Zhabotinsky) a region that fires becomes refractory and cannot fire again until a slow recovery variable relaxes, which is why waves annihilate instead of overwriting each other. Give each parameter block a recovery variable: a large write (update norm above threshold) drives the block refractory, its learning rate is suppressed while recovery is low, and recovery returns on a fixed time constant. Consecutive conflicting writes cannot land on the same block back to back; they are pushed to neighbouring, recovered blocks.
- **Novelty vs prior art.** Reconsolidation lability windows (Nader et al. 2000) are the neuroscience analogue in the opposite direction (labile after recall). Critical learning periods (2308.12221) are global, not per-region. ML search on "excitable media refractory learning rule" returned spiking-neuron papers only. Nearest internal: chemistry #47 product inhibition (write idempotence, no recovery dynamics). No direct hit.
- **Cheapest first test.** MLP with 32 blocks, five fast-alternating tasks. Compare refractory rule vs a fixed per-block cooldown timer with the same mean downtime, and vs plain SGD. Falsifier: refractory ≤ fixed cooldown on retention at equal new-task accuracy.
- **Retention check.** Accuracy on tasks 1–4 after task 5, against both controls.

### PL27 · Liesegang consolidation spacing — PRIMITIVE, M
- **Mechanism.** In Liesegang patterns, a reactant diffuses into a gel and precipitates in bands only when the local product exceeds supersaturation; band positions obey a geometric spacing law (Jablczynski). Accumulate "unconsolidated" mass (sum of update norms since the last consolidation) and fire a consolidation event (distill fast weights into slow weights, or commit an agent's scratch notes to its lesson store) only when the mass crosses a supersaturation threshold that the last event depleted. Spacing then adapts to how much is being learned, and becomes geometric in a stationary stream.
- **Novelty vs prior art.** Fast/slow weight consolidation (Benna & Fusi 2016; complementary learning systems) and spaced repetition use fixed or item-level schedules. Event-triggered consolidation on loss spikes exists in task-free CL (Aljundi et al. 2019, task-free CL). Triggering on accumulated update mass with depletion: no hit (the Liesegang query returned nothing in either index).
- **Cheapest first test.** Fast/slow weight MLP on a task-free stream with variable shift rates. Same number of consolidation events: Liesegang trigger vs periodic vs loss-spike trigger. Falsifier: Liesegang trigger does not beat both.
- **Retention check.** Slow-weight accuracy on early segments at the end of the stream.

### PL28 · Pinned Allen–Cahn fronts for module ownership — PRIMITIVE, M
- **Mechanism.** In a bistable medium (Allen–Cahn), two phases coexist separated by fronts; a weak drive moves a front only if it beats pinning by heterogeneities, so the boundary moves in discrete jumps and stays put otherwise. Let each module carry a phase field φ ∈ [−1, 1] saying which regime owns it; regime B's loss acts as the drive on φ, with diffusion along a module graph and pinning sites at modules marked important. Ownership changes only at the front and only when B's pressure exceeds pinning, so most modules never switch.
- **Novelty vs prior art.** Mixture-of-experts routing is soft and per-input; expert ownership in CL (e.g., expert expansion) is assigned by gating loss. Allen–Cahn hits are PINN solvers (2511.14497), not allocation. No direct hit. Nearest internal: PL25 (Turing spacing; this card is two-phase with pinning).
- **Cheapest first test.** 16 modules, A→B shift of growing size. Compare φ-front ownership vs soft gating vs hard top-1 routing at equal parameters. Falsifier: same number of switched modules and same retention as hard routing.
- **Retention check.** Regime A accuracy after B, and count of modules that switched owner.

### PL29 · Pushed-front adoption to preserve rare variants (fleets) — PRIMITIVE, H
- **Mechanism.** When a population expands as a *pulled* front, a few founders at the tip take over and diversity behind the front is lost; with an Allee effect (growth needs a local quorum) the front becomes *pushed* and diversity is preserved (Hallatschek & Nelson 2008; Birzu, Hallatschek, Korolev, PNAS 2018). In a fleet of agents sharing skills by gossip, require that an agent adopt a new skill version only when a quorum of its neighbours already holds it. Adoption becomes a pushed front, and locally adapted variants of old skills survive behind it instead of being swept.
- **Novelty vs prior art.** Gossip and federated learning spread updates by averaging or copying; LLM population studies (2610.31165) show topology effects on consensus. Quorum-gated adoption tied to the pulled/pushed transition is not used for continual learning: no hit for "pushed pulled fronts" with learning.
- **Cheapest first test.** 200 tabular agents on a ring, each with a locally tuned variant of an old skill; release a new globally better version. Compare quorum-gated vs plain copying. Falsifier: same loss of local variants at the same adoption speed.
- **Retention check.** Each agent's performance on its local old task after adoption is complete.

## F. Conservation laws by design

Not the killed Noether/balancedness line: these cards impose a conserved quantity as a hard rule of the write, instead of hoping SGD conserves one.

### PL30 · Flux-form learning: forgetting only by local transport — PRIMITIVE, H
- **Mechanism.** Write output-distribution change as a continuity equation ∂ρ/∂t = −∇·J on a declared graph over behaviours (classes, tools, response modes). The update may move probability mass only along graph edges, with a flux limit per edge. Learning a new behaviour B must take mass from B's declared neighbours, never from distant old behaviours, so where forgetting can happen is chosen in advance.
- **Novelty vs prior art.** Wasserstein gradient flows and optimal-transport regularisers move mass optimally but do not forbid non-local moves. Null-space projection (2611.29269) and control-minimisation CL (2602.04542) restrict parameter directions, not mass flow over behaviours. Lagrangian flow networks (2305.16846) enforce conservation for physics, not CL. Nearest internal: CD2 waterbed (mass must go somewhere, no locality). No direct hit.
- **Cheapest first test.** 10-class classifier; add class 11 with a declared neighbour set. Flux-form update vs KL-to-old-model anchor at equal new-class accuracy. Falsifier: non-neighbour classes lose as much accuracy under flux form as under KL anchor.
- **Retention check.** Accuracy on the non-neighbour old classes.

### PL31 · Adiabatic-invariant memory in cyclic training — PRIMITIVE, L
- **Mechanism.** For a fast oscillation whose parameters drift slowly, the action J = ∮p dq is conserved (adiabatic invariance). When a learner is trained on a fast A/B alternation, its weights orbit; under slow drift of the task mix the orbit's action should be preserved even as its centre moves. Store an old task in the orbit amplitude and read it by stopping the alternation and integrating over one period.
- **Novelty vs prior art.** Adiabatic fine-tuning of neural quantum states (2503.17140) uses the physics adiabatic theorem for a different purpose; training-dynamics thermodynamics (2511.07308) treats steady states, not invariants. No hit for adiabatic invariants as memory. Low ambition rating because the readout may be impractical outside linear models.
- **Cheapest first test.** Two-task linear regression with alternating minibatches and a slow mix drift; measure J along training. Falsifier: J drifts at the same rate as the orbit centre.
- **Retention check.** Task A error recovered from the orbit after drift vs plain sequential training.

### PL32 · Debye-screened (charge-neutral) edits — IMPROVEMENT, M
- **Mechanism.** In an electrolyte a charge gathers a screening cloud so its field decays as exp(−r/λ_D). Install each edit together with automatically computed counter-edits on a shell of nearby probe inputs, so the edit's net effect (and its first moments) vanishes beyond a chosen screening length λ_D in representation space. λ_D is the single scope knob.
- **Novelty vs prior art.** Locality in model editing is a known goal: MEMIT preserves key statistics, GRACE (Hartvigsen et al. 2023) uses a codebook radius, editing benchmarks measure locality (UniEdit 2505.12345). Explicit counter-charges with multipole cancellation are not used, hence IMPROVEMENT. No direct hit for screening.
- **Cheapest first test.** 100 synthetic fact edits on a small MLP language model. Compare screened edits vs GRACE radius vs MEMIT-style covariance constraint at equal edit success. Falsifier: no better locality–success curve.
- **Retention check.** Accuracy on unedited facts at distance > λ_D and on a held-out general task.

---

## Ranked deeper questions

1. **Can return-point memory be the memory contract of a learner?** If PL01/PL02 hold, old regimes come back exactly by re-traversing a drive, with no replay and no task ID. Decisive test: nested-reversal drives on a toy where plain fine-tuning and EWC both fail.
2. **Does task conflict set a sharp critical size or speed for forgetting?** PL13 (nucleation size), PL14 (Kibble–Zurek ramp) and PL12 (chaos length) all predict a knee with a conflict-dependent exponent. One sweep over mask size, ramp time and edit strength on the same toy can confirm or kill all three.
3. **Can forgetting be turned into detectable, one-type errors?** PL19 (erasure conversion), PL24 (biased noise) and PL18 (topological bit) change *what kind* of error forgetting is, which halves or better the redundancy needed. Test whether a parameterization exists where most damage is flagged.
4. **Can local dynamical constraints replace importance estimates?** PL06 (facilitation), PL25/PL28 (pattern-forming allocation) and PL30 (flux form) protect old knowledge by the shape of the dynamics rather than by Fisher or masks. Compare each against an equal-budget importance mask.
5. **Do collective-physics thresholds set fleet rehearsal and rollback?** PL16 (absorbing state), PL17 (committed minority) and PL29 (pushed fronts) give numeric thresholds for multi-agent CL. A 200-agent tabular simulation can check all three.
