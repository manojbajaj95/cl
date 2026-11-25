# Developmental growth of networks: morphogenesis, genome encodings, and regeneration for continual learning

Branch: standalone root node far from the edit-equivalence / Nerode-congruence / footprint cluster ([PR #102](https://github.com/manojbajaj95/cl/pull/102)–[PR #114](https://github.com/manojbajaj95/cl/pull/114)). Instead of asking when two weight edits are algebraically equivalent, this node asks **which mechanisms from developmental biology and morphogenesis—local self-organizing growth, differentiation, trophic pruning, genome-to-network encodings, and active regeneration after damage—yield genuine continual-learning primitives beyond Progressive Nets, DEN, and NAS**.

**Node question:** When we move past append-only column growth and centralized architecture search, what *local developmental rules* and *genotype–phenotype operations* allow a continual learner to grow, partition, prune, and self-repair its own circuits without task IDs, global controllers, or linear parameter blowup—and beat equal-byte replay, EWC, and Progressive/frozen-backbone baselines?

**Short answer.** Three structural failures separate biological development from current growing-network CL, and the CPU probe below illustrates all three:
1. **The Genotype–Phenotype Dilemma (pleiotropy vs. regenerability).** Replacing direct weights with a compact shared developmental program (CPPN genome) suffers **pleiotropic catastrophe** (`37.1%` old-task accuracy vs. `39.0%` for direct SGD, Probe 1): mutating a shared generative rule alters the unfolded network everywhere. Conversely, adapting only the somatic phenotype while keeping an old regenerative attractor creates a **regeneration-vs-plasticity conflict**: triggering local regeneration after a 29.2% lesion restores Task A (`87.2% → 88.3%`) while actively *erasing* unassimilated somatic Task B (`84.8% → 67.1%`, `−17.7 pp`). Solving both requires *cis-regulatory compartmentalization* (`A@B = 83.2%`, `B@B = 90.8%`) plus explicit *compartment boundary identity*—without boundary identity, a translation-invariant local CA regenerator blurs across a straddling seam (`83.0% → 70.8%`).
2. **Freezing old units fails without task IDs due to shared-readout spillover.** Extending [PR #115](https://github.com/manojbajaj95/cl/pull/115) (`tree/breadth-outside-edit-theory.md`), Probe 2 shows that even an *oracle* progressive baseline that hard-freezes all old units at the task boundary (`oracle_freeze_grow`) still drops **51.3 pp** on Task A (`90.8% → 39.5%`) when no task ID is given at inference, because newly grown global-`tanh` units fire on Task A's domain and hijack the shared readout. Pairing a strictly local *trophic plasticity lock* with a localized *morphogen-receptor gate* on newly budded units cuts forgetting to **1.0 ± 0.4 pp** (`90.1%` A retention, `90.3%` after 25% trophic pruning) with zero task IDs, zero Fisher matrices, and zero replay—while revealing a real developmental tradeoff: premature commitment slows Task B (`80.6%` vs. `91.8%` without the lock).
3. **Static checkpoints vs. homeostatic attractors.** Existing CL fights damage (conflicting updates, pruning, quantization) by storing external backups or replaying data. Morphogenetic systems encode functional structure as an *active local attractor* maintained by neighbor signaling and retrograde trophic support, turning both pruning (consumer-verified apoptosis) and repair (blastema/boundary regeneration) into local dynamical operations.

## Root cause: why Progressive Nets, DEN, and NAS stall

1. **Append-only growth scales storage, not generative structure.** Progressive Neural Networks ([1606.04671](https://arxiv.org/abs/1606.04671); streaming variant cPNN [2603.03040](https://arxiv.org/abs/2603.03040)) and Dynamically Expandable Networks (DEN, [1708.01547](https://arxiv.org/abs/1708.01547)) treat growth as static parameter appending gated by task boundaries or global loss spikes. Without a task-ID oracle, lateral/shared readouts leak new-task activity onto old domains (Probe 2); with task IDs, they reduce to a frozen-backbone router (cf. Ledger kill B2).
2. **Centralized controllers ignore local tissue state.** NAS, DEN, and neurogenesis-CL methods (Self-Regulated Neurogenesis [2403.14684](https://arxiv.org/abs/2403.14684), NORACL [2604.27031](https://arxiv.org/abs/2604.27031), MPCS [2605.02509](https://arxiv.org/abs/2605.02509)) trigger expansion or pruning from global loss, activation-norm, or weight-magnitude heuristics. They lack *lateral inhibition* (to stop newly budded units from collapsing onto the same residual), *retrograde consumer verification* (to prune only units whose downstream consumers no longer depend on them), and *growth-induced drift compensation* ([2408.10566](https://arxiv.org/abs/2408.10566), [2603.08647](https://arxiv.org/abs/2603.08647), [PR #115](https://github.com/manojbajaj95/cl/pull/115)).
3. **Developmental encodings without modularity amplify forgetting.** Neural Developmental Programs ([2307.08197](https://arxiv.org/abs/2307.08197)), Growing NCA ([2607.15726](https://arxiv.org/abs/2607.15726), [2610.08479](https://arxiv.org/abs/2610.08479), [2512.08360](https://arxiv.org/abs/2512.08360)), and indirect encodings ([2407.10359](https://arxiv.org/abs/2407.10359), [2610.00149](https://arxiv.org/abs/2610.00149), [2403.14019](https://arxiv.org/abs/2403.14019)) achieve compression and single-task self-assembly, but have not solved *sequential* continual updates: a shared genome couples all unfolded weights (pleiotropy), while a frozen genome erases somatic learning whenever regeneration runs (Probe 1).

### Small CPU probe ([`tree/probes/developmental_growth_probe.py`](probes/developmental_growth_probe.py), NumPy, ~13 s)

Setup: two jointly solvable nonlinear binary tasks A and B in `R^12` occupying shifted input regimes (`±1.6` along a regime axis) with flipped decision rules on a shared subspace (`conflict = 0.6`), evaluated with **no task IDs** through a single shared readout head. 16 paired worlds (`zlib.crc32` deterministic seeds), mean ± 95% CI.

**Probe 1 — Genotype–Phenotype Dilemma (`H = 24`, 29.2% contiguous lesion straddling the A/B boundary):**

| Arm | `A@A` (%) | `A@B` (%) | `B@B` (%) | `A_abl → A_reg` (%) | `B_abl → B_reg` (%) |
|---|---:|---:|---:|---:|---:|
| `direct_sgd` | `90.4 ± 1.0` | `39.0 ± 1.8` | `92.4 ± 0.8` | `39.9 → 39.9` | `89.4 → 89.4` |
| `shared_genome` (single CPPN) | `88.1 ± 1.3` | `37.1 ± 2.2` | `90.4 ± 0.9` | `41.3 → 37.1` | `85.9 → 90.4` |
| `compartment_genome` (cis-reg + receptor) | `89.6 ± 1.2` | `83.2 ± 1.2` | `90.8 ± 1.6` | `83.0 → 83.2` | `88.5 → 90.8` |
| `somatic_B_plus_A_regen` (local CA on A) | `89.6 ± 1.2` | `88.3 ± 1.3` | `85.9 ± 0.8` | `87.2 → 88.3` | `84.8 → 67.1` *(−17.7 pp)* |
| `assimilated_AB_regen` (naive CA, no seam tag) | `89.6 ± 1.2` | `83.2 ± 1.2` | `90.8 ± 1.6` | `83.0 → 70.8` *(−12.2 pp)* | `88.5 → 87.9` |

**Probe 2 — Growth-Induced Drift & Shared-Readout Spillover (`H = 16 → 32`, task-ID-free):**

| Arm | `A@A` (%) | `A@B` (%) | `A_drop` (pp) | `B@B` (%) | `A_prune25%` (%) |
|---|---:|---:|---:|---:|---:|
| `naive_grow` (zero-out widen + SGD) | `90.8 ± 0.9` | `39.7 ± 1.5` | `51.1 ± 1.9` | `92.0 ± 0.8` | `39.9 ± 1.5` |
| `ewc_grow` (widen + diag Fisher EWC) | `90.8 ± 0.9` | `39.3 ± 1.2` | `51.5 ± 1.8` | `87.7 ± 4.3` | `39.1 ± 1.2` |
| `oracle_freeze_grow` (hard-freeze old 16) | `90.8 ± 0.9` | `39.5 ± 1.6` | `51.3 ± 2.1` | `91.8 ± 0.8` | `39.1 ± 1.5` |
| `trophic_only_grow` (local lock, global `tanh`) | `90.8 ± 0.9` | `45.8 ± 1.6` | `45.0 ± 2.0` | `87.3 ± 1.1` | `49.4 ± 1.7` |
| `receptor_only_grow` (local receptor, no lock) | `91.1 ± 0.8` | `73.2 ± 1.8` | `18.0 ± 1.9` | `91.8 ± 1.0` | `73.4 ± 1.7` |
| `trophic_receptor_grow` (local lock + receptor) | `91.1 ± 0.8` | `90.1 ± 0.8` | `1.0 ± 0.4` | `80.6 ± 1.4` | `90.3 ± 0.9` |

*Takeaways from the probe:* (1) A shared developmental genome is *no better* than direct SGD against forgetting (`37.1%` vs `39.0%`). (2) Unassimilated regeneration actively erases somatic learning (`−17.7 pp`), and naive local CA regeneration fails when a lesion erases a compartment seam (`−12.2 pp`). (3) Hard-freezing old units (`oracle_freeze_grow`) fails completely without task IDs (`39.5%`) because of readout spillover; local trophic locking + domain receptors cuts forgetting by 50 pp (`90.1%`), exposing premature commitment (`B@B = 80.6%`) as the next mechanism to fix.

### Relation to prior art, the idea ledger, and earlier bio floods

- **Idea ledger ([`reviews/idea-ledger.md`](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md), PR #6):**
  - *Avoids killed patterns:* no frozen-backbone + per-skill embeddings (B2), no save/restore stacks disguised as regeneration (Return-point adapters / A3 time-travel), no raw parameter-norm conservation (#1, #8), and no redundant copies behind one shared trunk ([PR #116](https://github.com/manojbajaj95/cl/pull/116)).
  - *Required controls for every card:* matched total persistent bytes (including genome, enhancer tables, receptor centers, and CA kernels), matched forward/backward FLOPs, no task IDs at inference unless explicitly labeled an oracle, and comparison against equal-budget replay, EWC, Progressive/DEN, and magnitude pruning.
- **Separation from earlier bio floods:** [`ideas/flood/immuno-dev.md`](https://github.com/manojbajaj95/cl/blob/devin/1795539211-immuno-dev-flood/ideas/flood/immuno-dev.md) focused on immune tolerance, Spemann organizers, lineage fate maps, epithelial extrusion, and autotomy; [`ideas/flood/neuro-bio.md`](https://github.com/manojbajaj95/cl/blob/devin/1795538372-neuro-bio-idea-flood/ideas/flood/neuro-bio.md) focused on synaptic tagging, dendritic plateaus, morphogen axes (NB24), reaction-diffusion plasticity domains (NB22), cohort clocks, and ghost conduits. The 22 cards below target *distinct* morphogenetic primitives: cis-regulatory modularity, shadow enhancers, gene duplication/transposons, chromatin masks, germline assimilation, Notch–Delta stem partitioning, bistable toggle-switch commitment/dedifferentiation, receptor co-development, Turing neurogenesis, Slit/Robo chemotactic self-wiring, retrograde trophic apoptosis, subplate scaffolding, boundary-anchored & blastema regeneration, bioelectric blueprints, canalization, heterochrony, and critical-period E-I reopening.

---

## Research ideas (22 cards)

### A. Genome-to-network encodings & cis-regulatory modularity

1. **Cis-regulatory enhancer switches for non-pleiotropic genome edits.**
   - *Mechanism:* Factor a developmental genome into a shared, slowly evolving core rule `g_core(z)` and a compact table of modular *cis-regulatory enhancers* `e_k(m)` gated by local morphogen coordinates `m`. Learning a new skill never mutates `g_core` directly; it adds or edits a low-byte enhancer motif that turns on a different developmental subroutine only inside uncommitted morphogen regions.
   - *Novelty rationale:* Candidate **primitive**—replaces parameter-space adapters (LoRA) with *developmental-program* enhancers that unfold into arbitrary layer widths and survive cell ablation. Directly fixes Probe 1's shared-genome pleiotropy (`37.1% → 83.2%`). *Risk / likely tie:* at fixed width, may tie a bank of small LoRA adapters + coordinate router at equal bytes unless unfolding compresses multi-unit structure better than low-rank factors.
   - *Cheapest first test:* 8-task stream on a `d=12, H=32` tissue MLP; compare core + enhancer genome against equal-byte LoRA bank + router, shared CPPN genome, and DEN.
   - *Old-task retention check:* Task-ID-free held-out accuracy and worst-task drop across tasks 1–7 after task 8, plus 30% unit-ablation recovery without replay.

2. **Shadow enhancers (redundant developmental decoders for mutational buffering).**
   - *Mechanism:* Inspired by *Drosophila* shadow enhancers, encode each committed skill's developmental unfolding via *two structurally distinct* enhancer motifs (`e_k^{(1)}, e_k^{(2)}`) reading different morphogen/positional coordinates that converge onto the same functional subcircuit. If a subsequent continual update or quantization shock corrupts one enhancer's upstream coordinate field, the shadow enhancer maintains phenotypic output (developmental canalization against CL mutations).
   - *Novelty rationale:* Candidate **primitive**—unlike [PR #116](https://github.com/manojbajaj95/cl/pull/116)'s replicated parameter copies behind one shared trunk, shadow enhancers decouple *developmental read coordinates* so a single upstream drift cannot kill both developmental paths. *Risk / likely tie:* a 2-model ensemble with independent feature projections at equal bytes.
   - *Cheapest first test:* 6-task stream with deliberate perturbations to one coordinate channel between tasks; compare shadow-enhancer genome against single-enhancer genome and equal-byte 2-expert ensemble.
   - *Old-task retention check:* Worst-case old-task accuracy under coordinate-channel drift and after sequential task-6 training, at matched total bytes and new-task accuracy.

3. **Gene duplication and neofunctionalization via developmental transposons.**
   - *Mechanism:* When a new task triggers high residual error inside an already-committed compartment, execute a *gene-duplication* operation: copy that compartment's compact cis-regulatory motif into an uncommitted morphogen zone with a shifted receptor center, keep the original motif under purifying selection (high trophic lock), and release the duplicate to diverge freely under gradient descent (*neofunctionalization*).
   - *Novelty rationale:* Candidate **primitive**—turns transfer learning into a structural *copy-and-diverge* operator on compact generative motifs rather than copying full weight matrices (Progressive Nets) or fine-tuning shared weights. *Risk / likely tie:* initializing a new LoRA/adapter from the closest prior adapter's weights (adapter warm-start).
   - *Cheapest first test:* 10-task stream where tasks 6–10 are structured mutations of tasks 1–5 (rotated/negated sub-rules); compare motif duplication against random-init compartment growth and equal-byte adapter warm-start.
   - *Old-task retention check:* Held-out accuracy on ancestral tasks 1–5 (verifying zero drift in the original motif) alongside sample efficiency on variant tasks 6–10.

4. **Epigenetic chromatin-accessibility masks over a fixed developmental genome.**
   - *Mechanism:* Pre-train a rich, over-parameterized developmental genome `g` once; during continual deployment, freeze `g` and learn only sparse, heritable *chromatin open/close marks* `c ∈ [0,1]^G` (conditioned on local input-context morphogens) that gate which developmental genes transcribe into active weights. Forgetting is prevented because old chromatin profiles are never overwritten—only silenced in incompatible contexts—and can be re-opened in one local signaling step.
   - *Novelty rationale:* Candidate **primitive** if chromatin marks act on *developmental rules* (multi-step unfolding) rather than directly masking static weights (PackNet/SupSup/HAT, which are prior art). *Risk / likely tie:* SupSup / binary supermasks over a fixed random network at equal mask bits.
   - *Cheapest first test:* 10-task domain-incremental MLP (`H=64`) with equal mask-bit budget; compare chromatin marks over a 3-step developmental rule against SupSup/HAT weight masks and prompt-pool gating.
   - *Old-task retention check:* Task-ID-free accuracy on tasks 1–9 after task 10, plus zero-shot re-opening latency when task 1 recurs after 8 intervening tasks.

5. **Germline assimilation (Baldwin-style somatic-to-genome consolidation).**
   - *Mechanism:* Maintain two distinct substrates: fast *somatic weights* `θ` that adapt rapidly to incoming tasks (no pleiotropy), and a compact *developmental genome* `g` that unfolds the base body plan. Only after a somatic adaptation passes a persistence/stability criterion (surviving `K` episodes without reversal) does an offline *germline assimilation* step distill `Δθ` into a new cis-regulatory motif of `g`, freeing somatic plasticity and granting the skill full regenerability.
   - *Novelty rationale:* Candidate **primitive**—directly resolves Probe 1's pleiotropy-vs-regenerability dilemma by separating fast non-pleiotropic somatic exploration from slow regenerable germline storage, filtering transient noise out of the genome. *Risk / likely tie:* fast-weight/slow-weight consolidation (CLS / complementary learning systems) with periodic replay distillation.
   - *Cheapest first test:* 8-task stream containing 4 persistent tasks and 4 transient 1-epoch distractor shocks; compare germline assimilation against direct genome SGD, somatic-only SGD, and CLS replay distillation at equal bytes.
   - *Old-task retention check:* Accuracy on persistent old tasks after distractor shocks AND after 30% unit ablation, checking that transient distractors are *not* assimilated into the genome.

---

### B. Local morphogenetic growth, differentiation & symmetry breaking

6. **Notch–Delta lateral inhibition for self-partitioning stem pools.**
   - *Mechanism:* Maintain a pool of uncommitted stem units wired in a local neighborhood graph. When residual error arrives, stem units compute local error reduction; the first unit crossing threshold upregulates a *Delta* signal to its immediate neighbors, triggering their *Notch* receptor to suppress identical feature alignment and push their updates into the orthogonal residual subspace—preventing newly grown units from collapsing onto the same feature.
   - *Novelty rationale:* Candidate **primitive**—replaces global diversity regularizers and task-indexed expert allocators with a strictly local, decentralized symmetry-breaking rule that partitions capacity on the fly. *Risk / likely tie:* orthogonal initialization + standard SGD or global cosine-decorrelation penalty on new units.
   - *Cheapest first test:* Multi-cluster continual stream where each new task has 3 distinct sub-modes; bud 12 stem units per wave and compare Notch–Delta lateral inhibition against global decorrelation penalty and naive widening.
   - *Old-task retention check:* Old-task accuracy (no task IDs) and effective feature rank of newly budded units at matched total hidden width.

7. **Bistable toggle-switch fate commitment with reversible dedifferentiation.**
   - *Mechanism:* Give each unit a 2-state local gene-regulatory toggle `(u_i, v_i)` (mutually inhibiting *stemness* `u_i` vs. *commitment* `v_i`) governed by a bistable ODE. Sustained trophic support flips a unit sharply from plastic stem (`u_i ≈ 1`) to committed specialist (`v_i ≈ 1`), avoiding Probe 2's gradual premature-commitment slowdown (`B@B = 80.6%`); conversely, prolonged trophic starvation flips a dead/obsolete unit back to plastic stem (*dedifferentiation*) so capacity recycles without growing width.
   - *Novelty rationale:* Candidate **primitive**—replaces continuous heuristic plasticity decay (MAS/SI/trophic-EMA) with a *hysteretic bistable switch* that stays fully plastic during active learning, locks sharply once mature, and recycles obsolete units automatically. *Risk / likely tie:* thresholded plasticity freeze + periodic reset of low-activity units (ReDo / Continual Backprop).
   - *Cheapest first test:* Extend Probe 2 to a 6-task bounded-width stream (`H = 32`) where task 1 becomes obsolete after task 4; compare bistable toggle against Probe 2's continuous trophic lock, Continual Backprop (CBP), and EWC.
   - *Old-task retention check:* Retention on still-active old tasks (tasks 2–5) at matched task-6 accuracy, verifying that toggle hysteresis closes Probe 2's 11 pp B-accuracy gap without losing its 1.0 pp A-retention.

8. **Morphogen-receptor co-development with inter-compartment repulsion.**
   - *Mechanism:* Directly addressing Probe 2's shared-readout spillover (`oracle_freeze_grow = 39.5%`), newly budded units co-develop both computational weights and a localized input-domain receptor `r_i(x)`. During budding, high-trophic incumbent units emit a *repulsive morphogen* whenever a new unit's receptor fires on incumbent-supported inputs, pushing the new unit's receptor center/bandwidth out of occupied domains *before* its outgoing readout weights are allowed to grow.
   - *Novelty rationale:* Candidate **primitive**—makes *readout non-interference* a local developmental precondition enforced during unit maturation, eliminating spillover in task-ID-free streams without storing old-task replay buffers. *Risk / likely tie:* k-means / GMM gating over input embeddings (RBF-MoE) trained online.
   - *Cheapest first test:* Probe 2's shifted-regime stream swept across regime separation `δ ∈ {0.8, 1.2, 1.6, 2.4}`; compare repulsive receptor co-development against Probe 2's static receptor, online RBF-MoE, and EWC.
   - *Old-task retention check:* Task-ID-free accuracy on all prior tasks across overlap levels `δ`, reporting both A-retention and B-convergence at matched parameter count.

9. **Turing reaction–diffusion capacity waves (local activator–inhibitor neurogenesis).**
   - *Mechanism:* Treat the layer as a 1D/2D spatial sheet. Local prediction error acts as a short-range *activator* `a(x)` that triggers cell division (unit budding) where `a(x) > θ`, while newly committed units secrete a faster-diffusing *inhibitor* `h(x)` that suppresses division nearby. Unlike NB22 (which only modulates *plasticity* in fixed units), here the Turing instability physically *grows and spaces* new functional columns at a wavelength matched to task complexity, with zero global expansion trigger.
   - *Novelty rationale:* Candidate **primitive**—replaces centralized DEN/NORACL expansion thresholds with self-organizing spatial capacity allocation that naturally budgets more units to high-curvature regimes. *Risk / likely tie:* local error-threshold unit splitting (DEN) with a minimum-distance cooldown.
   - *Cheapest first test:* 8-task stream with heterogeneous task complexities (2 simple linear, 6 complex nonlinear) under a fixed total unit cap `H_max = 64`; compare Turing neurogenesis against uniform periodic growth and DEN-style loss-threshold splitting.
   - *Old-task retention check:* Worst-task and average accuracy across all 8 tasks at equal final `H`, verifying that simple tasks do not starve complex tasks or overwrite earlier columns.

10. **Chemotactic axon guidance for continual self-wiring (Slit/Robo-style sparse growth).**
    - *Mechanism:* Instead of dense `O(T^2)` lateral connections (Progressive Nets), newly budded units grow sparse candidate connections guided by two local fields: a *chemoattractant* secreted by downstream units with high residual error on the current stream, and a *chemorepellent* (Slit/Robo) secreted by downstream units with high trophic lock on old skills. Synapses stabilize only where attractant exceeds repellent.
    - *Novelty rationale:* Candidate **primitive**—replaces dense lateral wiring and global NAS topology search with local, polarity-guided sparse connectivity that preserves old downstream circuits by construction. *Risk / likely tie:* RigL / SET dynamic sparse rewiring masked by Fisher importance.
    - *Cheapest first test:* 3-layer sparse modular MLP (`density = 15%`) on a 6-task compositional stream; compare chemotactic wiring against Fisher-masked RigL and Progressive dense lateral connections at matched active FLOPs.
    - *Old-task retention check:* Held-out accuracy on tasks 1–5 (specifically checking downstream shared layers for readout drift) plus forward transfer on compositional task 6.

---

### C. Trophic pruning, apoptosis & tissue turnover

11. **Retrograde neurotrophic survival factor (consumer-verified apoptosis).**
    - *Mechanism:* Downstream layers continuously emit retrograde *trophic packets* back along incoming edges proportional to each upstream unit's counterfactual drop in correct-prediction margin when locally jittered. Units whose integrated trophic intake falls below a metabolic floor undergo *apoptosis* (orderly removal) and return their parameter slot to the stem pool—unlike NB08 (which requires an explicit neighbor handoff), apoptosis fires directly on consumer-verified disuse.
    - *Novelty rationale:* Candidate **primitive**—replaces weight-magnitude or activation-norm pruning (which routinely kill small-weight but high-leverage rare-skill units) with a local, consumer-verified survival economy. *Risk / likely tie:* Taylor/Hessian sensitivity pruning (OBD/SNIP) run periodically on a replay buffer.
    - *Cheapest first test:* 10-task stream with a fixed unit cap `H = 32` and 2 rare low-magnitude skills; compare retrograde trophic apoptosis against magnitude pruning, activation pruning, and buffer-based Taylor pruning at equal probe cost.
    - *Old-task retention check:* Accuracy on the 2 rare low-magnitude old skills after 3 pruning-and-regrowth cycles, alongside average accuracy across all 10 tasks.

12. **Competitive neurotrophin uptake (fixed-budget synaptic pruning at consumers).**
    - *Mechanism:* Each downstream neuron has a *fixed* total neurotrophin budget `B_j` that it distributes across its incoming synapses proportional to recent predictive contribution. When a new task grows incoming synapses onto consumer `j`, total synaptic mass cannot grow unboundedly: new synapses gain trophic share only by displacing uninformative synapses, while high-margin old synapses retain a protected baseline share.
    - *Novelty rationale:* Candidate **primitive**—enforces local capacity conservation *per consumer* rather than globally, preventing new tasks from drowning out old inputs in shared downstream layers. *Risk / likely tie:* per-neuron L1/L2 weight-norm projection (MaxNorm) during SGD.
    - *Cheapest first test:* Shared-trunk 2-layer MLP (`H = 32`) on a 6-task stream with skewed task frequencies (10:1); compare competitive neurotrophin uptake against per-neuron L2 normalization and EWC.
    - *Old-task retention check:* Accuracy on rare old tasks (10× lower frequency) after dominant new tasks, verifying no dilution of rare-skill incoming weights.

13. **Synaptic scaling homeostasis (multiplicative gain stabilization across growth).**
    - *Mechanism:* Growth-induced forgetting ([PR #115](https://github.com/manojbajaj95/cl/pull/115)) occurs partly because adding new units shifts the activation variance and softmax temperature of downstream layers. Install a strictly local homeostatic controller on each compartment that multiplicatively scales its outgoing gain `α_c` to hold its long-run pre-activation variance constant across growth and pruning events, without touching relative feature directions.
    - *Novelty rationale:* *Improvement* or minor **primitive** (local architectural homeostasis for continual growth); distinct from LayerNorm/BatchNorm because it operates per-compartment against a *developmental setpoint* rather than re-centering across the mixed batch (which shifts under domain drift). *Risk / likely tie:* LayerNorm or RMSNorm with frozen affine parameters.
    - *Cheapest first test:* Extend Probe 2 and PR #115's widening probe with 4 sequential growth events (`H = 16 → 24 → 32 → 40 → 48`); compare compartmental synaptic scaling against LayerNorm, RMSNorm, and unnormalized widening.
    - *Old-task retention check:* Immediate post-growth and post-training old-task accuracy and logit-margin drift across all 4 growth events.

14. **Programmed developmental scaffolding (transient subplate circuits).**
    - *Mechanism:* Inspired by mammalian cortical subplate neurons—which wire early sensory pathways and then die via programmed apoptosis—when a difficult new task arrives, the learner buds high-plasticity *transient scaffold units* carrying an explicit developmental countdown clock. During their lifespan, scaffold units absorb the initial high-variance gradient shock and guide permanent low-plasticity units via local feature alignment; as their clock expires, their gain decays smoothly to zero and they self-destruct, leaving zero permanent parameter growth.
    - *Novelty rationale:* Candidate **primitive**—turns temporary architectural expansion into a *self-cleaning optimization aid* that protects permanent weights from early-task shock (cf. Probe 2 of `thermodynamics-of-remembering.md`) without permanent memory bloat. *Risk / likely tie:* warmup learning-rate schedule + temporary LoRA merged into base weights.
    - *Cheapest first test:* 6-task high-conflict stream at fixed final capacity `H = 24`; compare transient subplate scaffolds (temporary `+12` units decaying to 0) against LR warmup, temporary merged LoRA, and plain SGD at equal total FLOPs.
    - *Old-task retention check:* Held-out accuracy on tasks 1–5 after task 6's scaffold has fully apoptosed, checking that final parameter count equals the baseline.

---

### D. Regeneration after damage, forgetting & catastrophic shocks

15. **Boundary-anchored local CA regeneration (fixing Probe 1's seam-blurring failure).**
    - *Mechanism:* Probe 1 showed that a naive translation-invariant 3-cell CA regenerator degrades Task A by `−12.2 pp` when a lesion straddles the A/B compartment seam. Equip every cell with a persistent 2-bit *compartment identity / polarity marker* (analogous to *Drosophila engrailed/hedgehog* selector genes) and gate the local CA update so cells only integrate neighbor messages from the *same* compartment side (and re-establish the sharp seam at the polarity flip).
    - *Novelty rationale:* Candidate **primitive**—makes local weightless regeneration compatible with *multi-task compartmentalized* tissues, restoring both compartments from surviving neighbors with zero weight backups and zero replay data. *Risk / likely tie:* low-rank SVD / error-correcting code over the weight matrix at equal bytes.
    - *Cheapest first test:* Direct rerun of Probe 1 (`assimilated_AB_regen`) adding a 2-bit compartment tag to the 3-cell CA rule; compare against untagged CA (Probe 1's `70.8%`) and equal-byte low-rank weight backup.
    - *Old-task retention check:* Recovery of *both* Task A and Task B after a 30% straddling lesion, plus retention after a subsequent Task C is added as a third compartment.

16. **Blastema dedifferentiation and positional-value regeneration after shock.**
    - *Mechanism:* Inspired by salamander limb regeneration: arrange units along a continuous functional axis (positional value `p_i ∈ [0, 1]`). When a destructive shock or pruning event knocks out a contiguous band of units, surviving edge cells detect a *positional-value discontinuity* (`|p_{i+1} - p_{i-1}| > 2Δp`), dedifferentiate into a local proliferative *blastema*, and iteratively intercalate intermediate units whose weights are interpolated by a learned local developmental rule until positional continuity is restored.
    - *Novelty rationale:* Candidate **primitive**—regeneration is triggered *autonomously* by a local topological gap detector rather than an external fault flag, and reconstructs missing intermediate functional capabilities without storing checkpoints. *Risk / likely tie:* periodic weight-checkpoint restore or linear interpolation of surviving neighbor weights.
    - *Cheapest first test:* 1D continuous-skill manifold (e.g. rotated/frequency-indexed regression tasks mapped smoothly along `H=32` units); ablate 25% contiguous interior units and compare blastema intercalation against linear neighbor interpolation and no-regeneration baselines.
    - *Old-task retention check:* Accuracy on the ablated interior skills AND unaffected exterior skills after regeneration, with zero replay examples.

17. **Regeneration-gated plasticity (resolving the regeneration-vs-plasticity conflict).**
    - *Mechanism:* Probe 1 proved that running a pre-B regenerative attractor after somatic B learning erases B (`84.8% → 67.1%`). Separate *structural damage* (sharp drop in local alive/coherence invariants without corresponding trophic rise) from *intentional plasticity* (smooth somatic shift accompanied by rising local trophic support). Gate the local CA regenerator to fire *only* on structural-damage faults, and allow any somatic shift whose trophic support stays high for `τ` steps to locally rewrite the CA attractor's fixed point in that compartment.
    - *Novelty rationale:* Candidate **primitive**—explicitly arbitrates between *homeostatic self-repair* and *continual learning*, a conflict absent from both standard CL (no regeneration) and standard NCA (no continual learning). *Risk / likely tie:* explicit task-boundary switch turning regeneration off during training and re-fitting it afterward.
    - *Cheapest first test:* Probe 1's `somatic_B_plus_A_regen` stream interleaved with random 20% unit-dropout faults *during* Task B learning; compare trophic-gated regeneration against always-on regeneration and always-off regeneration.
    - *Old-task retention check:* Task A accuracy after both Task B and mid-training faults, alongside Task B accuracy (requiring no `−17.7 pp` erasure).

18. **Bioelectric voltage-pattern memory (decoupled slow-field blueprint over fast weights).**
    - *Mechanism:* Inspired by Michael Levin's bioelectric morphogenetic fields: maintain a tiny, slow-timescale *resting-potential graph* `V_i ∈ R^2` across units (2 scalars per unit, `<1%` of weight bytes) coupled to immediate neighbors via gap-junction conductances. `V` encodes only coarse functional commitments (target activation polarity, compartment role, and gain regime), not full weights. After severe weight noise, quantization, or conflicting-task drift, a short local *bioelectric relaxation* phase adjusts fast weights to re-satisfy the slow `V`-pattern constraints before resuming inference.
    - *Novelty rationale:* Candidate **primitive**—a ultra-compact, topological *blueprint layer* that guides fast weight self-repair without storing weight snapshots or replay data. *Risk / likely tie:* storing per-unit activation statistics (mean/var) and running test-time batch-norm/feature alignment.
    - *Cheapest first test:* 4-task MLP (`H = 32`) subjected to 4-bit weight quantization or Gaussian weight corruption (`σ = 0.25`) between tasks; compare bioelectric relaxation against stored activation-mean alignment and equal-byte sparse replay.
    - *Old-task retention check:* Held-out accuracy on tasks 1–3 after corruption + bioelectric relaxation and after learning task 4, charging the exact bytes of `V`.

19. **Planarian split-and-regrow continual ensembles (holographic rollback without checkpoints).**
    - *Mechanism:* Train a small developmental tissue so that *any* 50% sub-tissue can regenerate the full multi-task competence via local CA rules (like a bisected planarian). When an untrusted or high-conflict continual update arrives, *bisect* the tissue in place: apply the risky update to Half 1 while Half 2 stays intact, evaluate Half 1 on held-out old-task probes, and either *propagate* Half 1's update (if retention passes) or *discard* Half 1 and regenerate it from Half 2 (if retention fails)—achieving rollback with zero extra persistent checkpoint storage.
    - *Novelty rationale:* Candidate **primitive**—turns holographic regenerability into a *zero-extra-memory transactional rollback* mechanism for risky continual updates (avoiding Ledger's Return-point adapter kill because no separate checkpoint is stored). *Risk / likely tie:* keeping a 50%-width network + a full checkpoint copy in the same total parameter budget.
    - *Cheapest first test:* Stream of 8 tasks where 3 tasks are adversarial/poisoned label flips; compare planarian split-and-regrow (`H = 32`, two `H = 16` halves) against an equal-byte `H = 16` network with an explicit backup copy.
    - *Old-task retention check:* Accuracy on clean tasks 1–5 after surviving the 3 poisoned waves, matched on total persistent bytes (tissue + CA kernel vs. half-network + backup).

---

### E. Canalization, heterochrony & multi-scale developmental timing

20. **Waddington canalization buffer (absorbing transient shocks before fate commitment).**
    - *Mechanism:* Shape the developmental unfolding `Φ_T(g)` with a contractive *canalizing manifold* (trained via contractive Jacobian regularization on the local cell-update steps) so small, transient somatic weight perturbations relax back onto the existing functional attractor within `K` homeostatic steps. Only a sustained, multi-episode coherent error signal supplies enough impulse to push the tissue over the Waddington ridge into a new stable valley.
    - *Novelty rationale:* Candidate **primitive**—builds *noise-vs-regime-shift filtering* directly into the geometry of the developmental dynamics rather than relying on external change-point detectors or loss thresholds. *Risk / likely tie:* momentum/EMA weight smoothing or a simple sliding-window change-point detector gating SGD.
    - *Cheapest first test:* 6-task stream corrupted by frequent 1-batch label-noise bursts and brief 1-episode distractor regimes; compare canalized unfolding against EMA weight smoothing and sliding-window SGD gating at equal compute.
    - *Old-task retention check:* Worst-checkpoint old-task accuracy during noise bursts AND adaptation speed when a *true* persistent regime shift occurs.

21. **Heterochronic developmental schedules (task-adaptive unfolding depth `T`).**
    - *Mechanism:* A single compact developmental genome `g` unfolds a network iteratively over developmental steps `t = 1, ..., T`. Familiar or low-conflict tasks run at early embryonic depth `T = 2` (fast, compact phenotype); encountering a novel high-conflict skill triggers *neoteny* (prolonged unfolding to `T = 6`), sprouting deeper specialized compartments from the same genome without increasing stored genome size. Old skills continue executing at their native developmental stage `T_k`.
    - *Novelty rationale:* Candidate **primitive**—couples continual capacity growth to *unfolding time* rather than stored parameter count, generalizing early-exit networks into a single generative genome whose depth is a continual-learning degree of freedom. *Risk / likely tie:* early-exit / anytime multi-depth network with fixed per-depth heads.
    - *Cheapest first test:* 6-task stream of increasing difficulty on a recurrent/unrolled weight-generating genome (`T ∈ {2, 4, 6}`); compare heterochronic unfolding against an equal-byte fixed-depth early-exit MLP.
    - *Old-task retention check:* Accuracy of early-stage tasks (1–2) evaluated at `T = 2` after late-stage tasks (5–6) are learned at `T = 6`, verifying zero backward interference from deeper unfolding.

22. **Local critical-period opening and re-opening via inhibitory maturation.**
    - *Mechanism:* Model each functional compartment with paired excitatory (computational) and local inhibitory (plasticity-braking, PV-interneuron-like) units. New compartments start in an open *critical period* (low inhibition, receptive fields and wiring fully plastic); as local accuracy stabilizes, inhibitory tone matures and closes the critical period (leaving only fine-grained weight tuning). If a later distribution shift causes sustained unresolvable error in *one* compartment, a local neuromodulatory pulse transiently suppresses inhibition *only* in that compartment to re-open its critical period while distant mature compartments stay locked.
    - *Novelty rationale:* Candidate **primitive**—provides *spatially localized, reversible plasticity windows* that avoid both permanent ossification (loss of plasticity) and global unfreezing (catastrophic forgetting). *Risk / likely tie:* per-module learning-rate warmup triggered by per-module validation-loss spike.
    - *Cheapest first test:* 8-task stream where task 2 undergoes a mid-stream rule revision at step 6 while tasks 1, 3, 4, 5 stay fixed; compare local critical-period re-opening against global LR reset, per-module LR spike, and Continual Backprop.
    - *Old-task retention check:* Held-out accuracy on unchanged tasks 1, 3, 4, 5 after revising task 2, plus revision speed on task 2.

---

## Deeper sub-questions, ranked by chance of a new primitive

1. **Can a boundary-anchored, trophic-gated local developmental attractor regenerate *multi-task* subcircuits after ablation or shock without erasing newer somatic skills—and beat equal-byte weight backups?** *(Ideas 5, 15, 16, 17, 18.)*
   - *Why #1:* Active self-repair from surviving neighbors is the sharpest capability in developmental biology that has *no* counterpart in Progressive Nets, EWC, or replay. Probe 1 already isolated the exact two failure modes blocking it—unassimilated somatic erasure (`−17.7 pp`) and seam blurring (`−12.2 pp`). Solving both with a compact local rule would establish a genuinely new CL primitive (homeostatic regeneration).
   - *Sharpest next CPU test:* Extend `tree/probes/developmental_growth_probe.py` Probe 1 with (a) 2-bit compartment identity tags on the 3-cell CA rule and (b) trophic-gated regeneration under interleaved 25% mid-training lesions, benchmarked against an equal-byte low-rank weight backup and equal-byte replay.
   - *Kill criterion:* Kill if the local CA rule cannot recover ≥80% of the lesion drop on *both* A and B across straddling lesions without erasing somatic B, or if an equal-byte low-rank checkpoint / replay buffer beats it across every lesion size.

2. **Does co-developing repulsive morphogen receptors with a reversible bistable toggle switch eliminate BOTH Probe 2's readout spillover AND its premature-commitment tradeoff in task-ID-free streams?** *(Ideas 6, 7, 8, 13.)*
   - *Why #2:* Probe 2 uncovered a striking empirical fact: even *oracle* freezing of old units loses `51.3 pp` without task IDs due to shared-readout spillover, while local trophic locking + receptors cut forgetting to `1.0 pp` at the cost of `−11.2 pp` on Task B. If a bistable toggle + repulsive receptor closes that B-accuracy gap across a 6–10 task stream (including overlapping domains and obsolete-task recycling), we get a strictly local, task-ID-free growth primitive.
   - *Sharpest next CPU test:* Extend Probe 2 to a 6-task stream sweeping domain overlap `δ ∈ {0.8, 1.2, 1.6, 2.4}` and total width cap `H = 48`, comparing bistable toggle + repulsive receptors against online RBF-MoE, Continual Backprop, and EWC at matched bytes and FLOPs.
   - *Kill criterion:* Kill if bistable switching fails to recover B accuracy within 2 pp of `receptor_only_grow` while keeping A drop ≤ 3 pp, or if a plain online RBF-MoE with frozen old experts ties it at equal bytes across all overlap levels `δ`.

3. **Can cis-regulatory modularity (enhancer switches, shadow enhancers, gene duplication) break the pleiotropy barrier of genome-to-network encodings while beating LoRA/adapter banks at equal total bytes?** *(Ideas 1, 2, 3, 4.)*
   - *Why #3:* Probe 1 showed a naive shared genome ties direct SGD (`37.1%` vs `39.0%`). Breaking pleiotropy while preserving *sub-linear byte scaling* across 10+ related tasks (via shared core rules + tiny enhancer motifs + motif duplication) would yield a new compact generative representation for CL—something append-only adapters cannot do.
   - *Sharpest next CPU test:* 12-task stream of structured task families (4 base tasks × 3 compositional variants) on a `H = 64` tissue MLP; compare core + cis-regulatory enhancer genome + motif duplication against an equal-byte LoRA/adapter bank with warm-start and SupSup supermasks.
   - *Kill criterion:* Kill if enhancer genomes require ≥ as many total bytes as a LoRA/adapter bank to match its retention and transfer across the 12-task family, or if core-rule updates still induce >5 pp pleiotropic forgetting on earlier families.

4. **Does consumer-verified retrograde trophic apoptosis plus transient subplate scaffolding beat magnitude/Taylor pruning and DEN on long bounded-capacity streams?** *(Ideas 10, 11, 12, 14.)*
   - *Why #4:* Real continual learners cannot grow forever. Replacing heuristic magnitude pruning and global loss-triggered expansion with local consumer-verified survival signals (apoptosis) and self-destructing learning scaffolds addresses bounded-capacity CL directly, especially when rare skills carry small weight norms.
   - *Sharpest next CPU test:* 10-task bounded-width (`H = 32`) stream with 2 rare low-magnitude tasks and 3 prune-regrow cycles; compare retrograde trophic apoptosis + transient subplate scaffolds against magnitude pruning, buffer-based Taylor pruning, and DEN at matched FLOPs and final parameter count.
   - *Kill criterion:* Kill if retrograde trophic apoptosis ties magnitude or Taylor pruning on rare-skill retention (within 2 pp across 16 seeds), or if transient subplate scaffolds fail to beat a simple LR warmup + temporary merged LoRA at equal FLOPs.
