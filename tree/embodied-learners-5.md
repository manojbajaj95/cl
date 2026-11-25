# Embodied learners, depth 4: skills across past bodies and a body driver that outlives policies

Depth-4 node under [tree/embodied-learners-4.md](embodied-learners-4.md) ([PR #398](https://github.com/manojbajaj95/cl/pull/398)) → [#397](https://github.com/manojbajaj95/cl/pull/397) → [#396](https://github.com/manojbajaj95/cl/pull/396) → [#395](https://github.com/manojbajaj95/cl/pull/395) · 26 candidate primitives (EE01–EE26) · 5 ranked deeper questions · Ideas only; no experiments run (the ED08 pilot awaits owner approval and is not run or redesigned here)

**What the review kept (score 3).** From the [PR #398 triage row](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). Γ itself stays at 3 and moves to 4 if ED08 and ED10 pass. Two uses of Γ were also kept:
- **(a) Produce backward transfer** (ED14). Transport a skill learned on today's body back to every stored past body with no data there; this is exact on flat paths and flagged for practice on curved ones. Controls: no transport, RMA latent set to the old body, EB12 conjugator, fine-tuning on the old body at equal steps, EL23 homotopy walk, zero-shot success on past bodies against practice needed, retention.
- **(b) A per-robot-model action-space connection** (ED20 + ED21). Fit it once in action and proprioception space so any policy version, including a new VLA, reuses it; the holonomy it cannot absorb is strategy curvature that requires a skill change. Controls: PEA per policy per shift, TeAR, a weight-space Γ, RMA, one Γ across policy versions and fleet units, fraction of holonomy left after the fit, retention.

**This node's push.** Both are still *uses* of Γ. To become primitives they need objects of their own:
- (a) becomes a statement about **where a skill lives**. A skill is not one policy but a *section* over the archive of bodies the robot has had: defined on all of them, glued by transport, and updated by operations that act on the whole archive at once.
- (b) becomes a statement about **where memory lives**. A robot unit carries a learned **body driver** (action-space Γ plus an observation-side counterpart) that outlives policy versions. The policy talks to a canonical virtual robot, and the driver's residual is a narrow, typed channel carrying only the body information a strategy needs.

Together they split a lifelong robot's memory into two artifacts with different lifetimes: **unit-resident body memory** (driver, archive) and **version-resident skill memory** (policy).

**Shared controls.** The reviewer's controls above, plus [GEM](https://arxiv.org/abs/1706.08840)-style backward-transfer measurement, backward-transfer methods ([Beyond not-forgetting](https://arxiv.org/abs/2211.00789), [Selective backward refinement](https://arxiv.org/abs/2606.01379)), [backward-compatible training](https://arxiv.org/abs/2003.11942) for version compatibility, universal action spaces ([UMR](https://arxiv.org/abs/2609.34256), [unified hand action space](https://arxiv.org/abs/2607.03570), [PHASOR](https://arxiv.org/abs/2606.01851)) and ER at equal budget. Ledger rules from the root hold. Testbeds: the root's MuJoCo bodies and body archives, policy "versions" as differently trained or differently sized networks, then LIBERO with PEA-style actuation shifts and two VLA checkpoints.

## Literature check

New searches: backward-compatible representations and model upgrades, universal/canonical action spaces across embodiments, producing positive backward transfer, sheaf neural networks and gluing local models, information bottlenecks on dynamics context, learned low-level controller interfaces, hardware co-design for policy reuse, and offline evaluation over hardware variants.

| Line | Nearest prior | Gap for this node |
|---|---|---|
| Backward transfer | [GEM](https://arxiv.org/abs/1706.08840) (measures BWT), [Beyond not-forgetting](https://arxiv.org/abs/2211.00789), [Selective backward refinement](https://arxiv.org/abs/2606.01379), [forgetting-free positive transfer](https://arxiv.org/abs/2601.05623) | Backward transfer to old *tasks* through shared parameters. Transfer to old *bodies*, with the archive as the object of learning, is new. |
| Gluing local models | [Sheaf networks with connection Laplacians](https://arxiv.org/abs/2206.08702), [Sheaf networks and holonomy](https://arxiv.org/abs/2607.19514), [Equivariant/sheaf foundations](https://arxiv.org/abs/2607.03798) | Sheaves over graph nodes with learned restriction maps. A sheaf of *skills* over a robot's body archive, with Γ as the restriction maps, is new. |
| Version compatibility | [BCT](https://arxiv.org/abs/2003.11942), [stationary representations](https://arxiv.org/abs/2606.12488), [hyperbolic backward compatibility](https://arxiv.org/abs/2506.05826) | Embedding compatibility for retrieval. Compatibility of control policies with a robot-resident driver is new. |
| Canonical action interfaces | [UMR](https://arxiv.org/abs/2609.34256), [unified hand action space](https://arxiv.org/abs/2607.03570), [PHASOR](https://arxiv.org/abs/2606.01851), [HPT](https://arxiv.org/abs/2409.20537), [latent-action world models](https://arxiv.org/abs/2610.36791), [Tune to learn](https://arxiv.org/abs/2604.02523) (controller gains shape learning) | Shared action spaces across *models* of robots, fixed after training. A per-unit, continually updated driver with a typed residual is new. |
| Body context with limited bandwidth | [BoBDeLaN](https://arxiv.org/abs/2611.21209) (bounded-bandwidth context for Lagrangian control), [Online adaptation to latent physical properties](https://arxiv.org/abs/2611.06118), [RMA](https://arxiv.org/abs/2107.04034) | Context channels carry everything the encoder finds useful. A channel restricted to what a gauge-absorbing driver cannot absorb is new. |
| Hardware choice and evaluation | [Differentiable co-design](https://arxiv.org/abs/2611.19329), [Shape your body](https://arxiv.org/abs/2606.00702), [RoboFQE](https://arxiv.org/abs/2610.18699), [LIBERO-RIG](https://arxiv.org/abs/2610.18843) | Co-design optimizes a body for a task at design time; repair-time part choice for skill retention and evaluation over past bodies without hardware are new. |

---

## A · A skill is a section over the body archive (pushing (a))

### EE01 · The body archive as a learning substrate
- **Primitive** (new object: the set of bodies the robot has had, each stored as a ritual trace plus its Γ-chart, treated as a domain every skill is defined on).
- **Mechanism:** Instead of a policy for the current body, each skill is a section \(s: \mathcal{A}\to\Pi\) over the archive \(\mathcal{A}\), with Γ-transport as restriction maps between bodies. Learning on today's body updates the whole section at once; old bodies are first-class, not evaluation-only.
- **Nearest prior / gap:** [Sheaf networks with connection Laplacians](https://arxiv.org/abs/2206.08702) glue local predictors over graphs; RMA conditions on the current body. A skill as a section over the robot's own body history is new.
- **Cheapest first test:** Ant with a 6-body archive from wear and repair, 4 skills learned in sequence on the latest body. Arms: no transport, ED14 one-shot transport, RMA set to old bodies, fine-tuning per old body at equal steps, section updates. **Kill** if section updates do not beat one-shot transport on mean archive success after 4 skills, over 10 seeds.
- **Old-skill retention:** Every skill on every archived body.
- **Risk / likely tie:** If Γ is flat, the section is just transport (ED14).

### EE02 · Ghost bodies as a regularizer for today's learning
- **Primitive** (new operation: every update on today's body must also hold when transported to archived "ghost" bodies).
- **Mechanism:** While learning on the current body, add a loss on the transported policy's predicted performance on each ghost (via its stored ritual model and Γ). This prevents skills from overfitting to the current wear state, at no hardware cost.
- **Nearest prior / gap:** Domain randomization trains over a *designed* body family; [GEM](https://arxiv.org/abs/1706.08840) constrains old-task loss. Constraining against the robot's own past bodies is new.
- **Cheapest first test:** EE01 archive. **Kill** if ghost regularization does not raise archive success by ≥ 10% at ≤ 3% current-body cost versus domain randomization over the archive's parameter range.
- **Old-skill retention:** Archive success of earlier skills.
- **Risk / likely tie:** Ghost models drift from reality; stale ghosts can mislead.

### EE03 · Two-way era distillation
- **Primitive** (new operation: old-body resident skills and new transported skills teach each other).
- **Mechanism:** On each archived body there may be both a resident skill (learned there long ago) and a transported newer one. Distill in both directions: the resident one supplies body-specific contact details, the transported one supplies newer task competence. Gluing disagreement localizes curvature.
- **Nearest prior / gap:** [Policy distillation](https://arxiv.org/abs/1511.06295) is one-way; [Beyond not-forgetting](https://arxiv.org/abs/2211.00789) transfers backward within one model.
- **Cheapest first test:** 3 archived bodies with resident skills plus a new improved skill on the current body. **Kill** if two-way distillation does not beat the better of resident or transported on each archived body.
- **Old-skill retention:** Resident skills' success must not drop.
- **Risk / likely tie:** Simple max-of-two selection may tie.

### EE04 · Harmonic extension of a new skill over the archive
- **Primitive** (new operation: extend a skill learned on one body to the archive by minimizing transport disagreement (a connection-Laplacian energy) with old bodies' anchors fixed).
- **Mechanism:** Learning a skill on body B defines the section at B. Extend to all bodies by solving for the section that minimizes \(\sum_{ij}\|s_i - \Gamma_{ij}s_j\|^2\), with resident skills as boundary conditions. Curvature shows up as irreducible energy, which ranks where practice is needed.
- **Nearest prior / gap:** Connection-Laplacian diffusion in [sheaf networks](https://arxiv.org/abs/2206.08702); [REvolveR](https://arxiv.org/abs/2202.05244) walks one path.
- **Cheapest first test:** EE01 archive. **Kill** if harmonic extension does not beat ED14 one-shot transport on curved-region bodies at zero practice.
- **Old-skill retention:** Boundary skills unchanged; others measured.
- **Risk / likely tie:** On a flat archive, identical to transport.

### EE05 · Archive quotient: merge bodies that transport flatly
- **Primitive** (new operation: collapse archive entries connected by flat paths into one equivalence class).
- **Mechanism:** Bodies related by pure gauge (for example actuator gain changes in the envelope) are one body up to the driver. Storing one representative per class shrinks the archive to the number of strategy-distinct bodies. Its size is a measure of how many bodies a skill really has to know.
- **Nearest prior / gap:** No archive compression by geometric equivalence found.
- **Cheapest first test:** 12-body archive with 4 strategy-distinct classes. **Kill** if the quotient loses > 5% archive success versus the full archive.
- **Old-skill retention:** Archive success after quotienting.
- **Risk / likely tie:** Needs the flat/curved distinction to hold (ED08).

### EE06 · Practice where transport carries furthest
- **Primitive** (new rule: choose the body to practice on, current or a simulated ghost, by how far its gains transport across the archive).
- **Mechanism:** Practice on body \(b\) improves the section everywhere \(b\) connects flatly. Choose \(b\) to maximize transported gain over the archive weighted by expected use.
- **Nearest prior / gap:** [Practice is not free](https://arxiv.org/abs/2611.19979) prices practice per task; uniform rehearsal beats LP ([PR #119](https://github.com/manojbajaj95/cl/pull/119)).
- **Cheapest first test:** EE01 archive, ghost practice in sim. **Kill** if transport-weighted body choice does not beat practicing on the current body and uniform practice over the archive.
- **Old-skill retention:** Archive success of all skills.
- **Risk / likely tie:** Current-body practice may dominate when use is concentrated there.

### EE07 · Transportability as a skill-learning objective
- **Primitive** (new objective: learn skills to be transportable, penalizing path dependence of the skill itself).
- **Mechanism:** Among solutions of similar current-body return, prefer the one whose holonomy around archive loops is smallest. This selects strategies that do not depend on body details the archive says will change.
- **Nearest prior / gap:** Robustness objectives over parameter ranges (DR); [Fishr](https://arxiv.org/abs/2109.02934). A loop-holonomy penalty is new.
- **Cheapest first test:** Pusher with two equally good strategies on the current body, one of which fails on old bodies. **Kill** if the penalty does not pick the transportable strategy in ≥ 80% of seeds.
- **Old-skill retention:** Archive success.
- **Risk / likely tie:** DR over archive parameters may do the same.

### EE08 · Prospective transport to predicted future bodies
- **Primitive** (new operation: transport skills forward along a predicted wear trajectory before the body gets there).
- **Mechanism:** Extrapolate the ritual trace along the wear trend (root EL01 data), extend Γ along it, and pre-compute skill sections for the next wear states, so adaptation is ready at the moment of drift.
- **Nearest prior / gap:** [RUL-aware planning](https://arxiv.org/abs/2610.02469) predicts degradation for planning; RMA adapts after the fact.
- **Cheapest first test:** HalfCheetah with steady gear wear. **Kill** if prospective sections do not reduce the post-drift performance dip by ≥ 50% versus RMA.
- **Old-skill retention:** All skills at each wear level.
- **Risk / likely tie:** Wear is rarely smooth; faults are abrupt.

### EE09 · Pareto merge of resident and transported skills
- **Primitive** (new operator: per body, combine resident and transported skills by ritual-predicted performance, not by recency).
- **Mechanism:** For each archive entry, keep whichever (or a blend) the ritual model predicts performs best; blends are taken in the gauge-fixed frame so they are well defined.
- **Nearest prior / gap:** Model merging ([ResMerge](https://arxiv.org/abs/2610.41663)) merges in weight space without a body frame.
- **Cheapest first test:** EE03 setting. **Kill** if the ritual-predicted choice is wrong > 20% of the time against ground truth.
- **Old-skill retention:** Resident skills where kept.
- **Risk / likely tie:** Graded as an improvement if EE03 already wins.

### EE10 · Body-space mixup through transport
- **Primitive** (new augmentation: interpolated bodies between archive entries, with skills transported to them, as training data).
- **Mechanism:** Interpolate ritual traces between neighboring bodies, transport skills to the midpoint and train the body-side model there. This densifies the archive without new hardware states.
- **Nearest prior / gap:** [REvolveR](https://arxiv.org/abs/2202.05244) interpolates robots for one-way transfer; mixup in input space.
- **Cheapest first test:** Sparse 4-body archive. **Kill** if mixup does not improve success on held-out intermediate bodies over the sparse archive.
- **Old-skill retention:** Archive success.
- **Risk / likely tie:** Curved regions make midpoints wrong.

## B · A body driver that outlives policies (pushing (b))

### EE11 · The learned body driver
- **Primitive** (new artifact: a per-unit, continually updated action and proprioception driver that presents a canonical virtual robot to any policy).
- **Mechanism:** The driver is Γ in action space plus its proprioceptive inverse, fitted from ritual and free motion. Every policy is written against the canonical robot; the driver runs at control rate between policy and hardware. Wear updates only the driver.
- **Nearest prior / gap:** Universal action spaces ([UMR](https://arxiv.org/abs/2609.34256), [unified hand action space](https://arxiv.org/abs/2607.03570), [PHASOR](https://arxiv.org/abs/2606.01851)) are fixed after training; [PEA](https://arxiv.org/abs/2611.28308) calibrates per policy per shift; [TeAR](https://arxiv.org/abs/2609.36182) is policy-specific.
- **Cheapest first test:** 2 policy versions on one worn arm. **Kill** if a driver fit with version 1 loses > 20% of its benefit for version 2, or PEA per version matches it at equal probe time.
- **Old-skill retention:** Both versions' skills after drift.
- **Risk / likely tie:** Strategy curvature remains for the policy (EE13).

### EE12 · Driver-compatible policy training
- **Primitive** (new constraint: policy versions are trained so that existing drivers remain valid; backward compatibility for control).
- **Mechanism:** Like [BCT](https://arxiv.org/abs/2003.11942) for embeddings: the new policy's actions must mean the same canonical-robot commands as the old one's, enforced by a compatibility loss on the ritual and canonical probes. Fleet drivers then survive upgrades without refitting.
- **Nearest prior / gap:** BCT and [stationary representations](https://arxiv.org/abs/2606.12488) target retrieval embeddings.
- **Cheapest first test:** Upgrade policy width ×2 on 4 worn units. **Kill** if compatible training does not keep driver-mediated success within 5% without refitting, versus ≥ 15% drop without the loss.
- **Old-skill retention:** Old skills under the new version on each unit.
- **Risk / likely tie:** Upgrades may not perturb action semantics enough to matter.

### EE13 · Typed residual channel: only what strategy needs
- **Primitive** (new interface: the driver passes the policy only the body information it cannot absorb itself).
- **Mechanism:** After the driver absorbs gauge, fit the residual holonomy (strategy curvature) as a low-dimensional code and feed it to the policy as its only body input. The policy cannot see body details the driver handles.
- **Nearest prior / gap:** [RMA](https://arxiv.org/abs/2107.04034) latents and [BoBDeLaN](https://arxiv.org/abs/2611.21209) bounded-bandwidth contexts carry whatever helps; nothing restricts the channel to what a driver cannot absorb.
- **Cheapest first test:** Ant with gain and mass changes. Arms: RMA latent, bounded-bandwidth context, driver + typed residual. **Kill** if the typed residual does not match RMA return with ≤ 25% of its channel dimension and better transfer to new skills.
- **Old-skill retention:** All skills across bodies.
- **Risk / likely tie:** A small RMA latent may already be nearly minimal.

### EE14 · Body-information bottleneck defined by the driver
- **Primitive** (new quantity: the information about the body a policy must receive, i.e. the entropy of the typed residual).
- **Mechanism:** Measure \(I(\text{residual};\text{body})\) across body families. Gauge families need zero bits; strategy-distinct families need about \(\log\) (number of strategy classes, EE05). This number becomes a design constraint for policy inputs.
- **Nearest prior / gap:** Information bottlenecks on context exist for generalization; none ties the bits to geometric strategy classes.
- **Cheapest first test:** 3 families with 1, 2 and 4 known strategy classes. **Kill** if measured bits do not order the families correctly.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** An assay unless used to size the channel (EE13).

### EE15 · Hierarchical drivers: model, unit and moment
- **Primitive** (new structure: driver = robot-model driver + unit delta (manufacturing variation) + fast delta (heat, payload)).
- **Mechanism:** The model driver is fit from the fleet; unit deltas from each robot's ritual; fast deltas decay like root EL05. Each layer has its own update rate and lifetime.
- **Nearest prior / gap:** [Fleet policy merging](https://arxiv.org/abs/2310.01362) merges policies; [collective experience](https://arxiv.org/abs/2610.25736) shares data.
- **Cheapest first test:** 6 units with distinct manufacturing offsets. **Kill** if hierarchical drivers do not beat one driver per unit in success on a new unit after 1 ritual.
- **Old-skill retention:** All units' skills after fleet updates.
- **Risk / likely tie:** Per-unit drivers may be cheap enough.

### EE16 · Canonical-coordinate datasets
- **Primitive** (new data format: demonstrations stored in canonical-robot coordinates through each unit's inverse driver at recording time).
- **Mechanism:** Every demo is stored after applying the recording unit's inverse driver, so datasets are free of per-unit and per-wear artifacts. Datasets from heterogeneous labs then share coordinates up to strategy curvature.
- **Nearest prior / gap:** [Open X-Embodiment](https://arxiv.org/abs/2310.08864) pools raw heterogeneous data; [LIBERO-RIG](https://arxiv.org/abs/2610.18843) shows setup sensitivity.
- **Cheapest first test:** Demos from 3 worn units of one arm. **Kill** if canonical demos do not beat raw demos for a new unit with its driver.
- **Old-skill retention:** Earlier-demo skills after adding new units' data.
- **Risk / likely tie:** Raw data plus RMA may suffice.

### EE17 · Simulation is the canonical robot
- **Primitive** (new framing: sim-to-real is driver fitting only; policies are never fine-tuned on hardware for body reasons).
- **Mechanism:** The simulator defines the canonical robot. Each real unit gets a driver fitted from ritual data; policy fine-tuning on hardware is restricted to strategy-curvature regions flagged by the residual.
- **Nearest prior / gap:** [Deep inverse dynamics transfer](https://arxiv.org/abs/1610.03518), [actuator reality shaping](https://arxiv.org/abs/2607.02205), [actuator identification](https://arxiv.org/abs/2604.10351).
- **Cheapest first test:** Sim → "real" (actuator-model edits) for 4 skills. **Kill** if driver-only transfer does not reach 90% of policy fine-tuning return with no task episodes.
- **Old-skill retention:** Sim skills remain intact (policy untouched).
- **Risk / likely tie:** Close to inverse-dynamics transfer; the novelty is lifetime and sharing.

### EE18 · Unit-resident memory: split lifelong memory by artifact lifetime
- **Primitive** (new principle: body knowledge is stored on the robot unit and skill knowledge in the policy; each is continual on its own clock).
- **Mechanism:** The driver, the archive and the ritual history live with the unit and survive policy swaps; the policy lives with versions and survives unit swaps. Continual-learning metrics are reported per artifact: body retention across policy versions and skill retention across units.
- **Nearest prior / gap:** No CL framework splits memory between hardware-resident and software-resident artifacts.
- **Cheapest first test:** 2 units × 3 policy versions with wear between versions. **Kill** if the split does not beat a monolithic policy carrying body adaptation on the sum of both retention metrics.
- **Old-skill retention:** Both metrics.
- **Risk / likely tie:** The split is a design pattern unless EE11 and EE12 hold.

### EE19 · Policies robust to driver error
- **Primitive** (new training target: policies tolerant of the driver's residual error distribution, not of raw body variation).
- **Mechanism:** Train policies with perturbations drawn from the driver's measured error (much narrower than the body family), so robustness is spent only where the driver is imperfect.
- **Nearest prior / gap:** [Domain randomization](https://arxiv.org/abs/1703.06907) over the full family; [Tune to learn](https://arxiv.org/abs/2604.02523) shows controller gains shape learning.
- **Cheapest first test:** Ant. **Kill** if driver-error randomization does not beat full-family DR on in-family return with equal training.
- **Old-skill retention:** Skills across bodies.
- **Risk / likely tie:** Driver error may be state-dependent and hard to sample.

### EE20 · Observation-side driver
- **Primitive** (new artifact: a perception driver from each unit's sensors to canonical observations, reused across policy versions).
- **Mechanism:** Self-observation segments of the ritual (root EB08) fit a map from the unit's current camera and proprio to canonical ones. Policies never see mounting or calibration drift.
- **Nearest prior / gap:** [UniLatent](https://arxiv.org/abs/2611.10061), [continual hand–eye calibration](https://arxiv.org/abs/2604.15814).
- **Cheapest first test:** LIBERO with camera shifts and two policy checkpoints. **Kill** if one observation driver does not serve both checkpoints within 10% of per-checkpoint calibration.
- **Old-skill retention:** Original-setup success for both checkpoints.
- **Risk / likely tie:** Large pretrained encoders may absorb small shifts.

### EE21 · Driver warm-start for a new robot model from its kinematic graph
- **Primitive** (new operation: initialize a new model's driver from existing models' drivers by kinematic-graph similarity).
- **Mechanism:** Drivers of related arms share structure (joint types, chains). Map graph nodes and transfer driver components; refine on the new model's ritual.
- **Nearest prior / gap:** [MetaMorph](https://arxiv.org/abs/2203.11931), [KITE](https://arxiv.org/abs/2606.22113).
- **Cheapest first test:** 3 arms → a 4th. **Kill** if warm-start does not halve the ritual time needed to reach a cold driver's quality.
- **Old-skill retention:** Existing models' drivers unchanged.
- **Risk / likely tie:** Kinematic similarity may not predict dynamics.

## C · The two together

### EE22 · Hardware-generation backport
- **Primitive** (new operation: run a skill learned on a new hardware generation on old generations through their drivers and archive sections).
- **Mechanism:** Generation N's skill is written in canonical coordinates; old generations receive it via their drivers. Strategy residuals flag which skills need practice on old hardware.
- **Nearest prior / gap:** Cross-embodiment pretraining is forward-looking ([RT-X](https://arxiv.org/abs/2310.08864), [HPT](https://arxiv.org/abs/2409.20537)); backward support of legacy hardware is unaddressed.
- **Cheapest first test:** 3 "generations" of an arm (link and actuator changes). **Kill** if backported skills do not beat fine-tuning on old generations at ≤ 10% of the data.
- **Old-skill retention:** Old generations' resident skills.
- **Risk / likely tie:** Large generation gaps are curved.

### EE23 · Hardware regression suite without hardware
- **Primitive** (new operation: evaluate a policy version on every archived body of every unit through drivers and ritual models before deployment).
- **Mechanism:** The archive plus drivers gives a counterfactual evaluation over past and present bodies; a new version ships only if transported performance does not regress anywhere.
- **Nearest prior / gap:** [RoboFQE](https://arxiv.org/abs/2610.18699) estimates policy value from offline trajectories; LIBERO-RIG is a fixed benchmark.
- **Cheapest first test:** 3 versions × 8 archived bodies. **Kill** if predicted regressions do not match measured ones at AUROC ≥ 0.8.
- **Old-skill retention:** Is what it guards.
- **Risk / likely tie:** Graded as a tool if it wins.

### EE24 · Repair-time part choice to keep skills flat
- **Primitive** (new operation: choose replacement parts or controller gains so the repaired body lies in a flat region relative to existing skills).
- **Mechanism:** Among available spare parts or gain settings, choose the one whose driver change has the least strategy residual on skills in use. Hardware choice becomes a retention tool.
- **Nearest prior / gap:** Co-design optimizes a body for tasks at design time ([differentiable co-design](https://arxiv.org/abs/2611.19329), [Shape your body](https://arxiv.org/abs/2606.00702)); repair-time choice for retention is new.
- **Cheapest first test:** 5 candidate replacement actuators (sim). **Kill** if the chosen part does not beat the nominal part on post-repair success by ≥ 10%.
- **Old-skill retention:** All skills after repair.
- **Risk / likely tie:** Parts may differ too little.

### EE25 · Two-dimensional transport: bodies × policy versions
- **Primitive** (new base space: transport skills along both body changes and policy-version changes, with a mixed curvature between them).
- **Mechanism:** Version upgrades and body changes both move the policy. If they commute (zero mixed curvature), drivers and versions are independent (EE18 holds); non-zero mixed curvature says which upgrades disturb body memory.
- **Nearest prior / gap:** Depth-2's commutators were over body directions only.
- **Cheapest first test:** 2 versions × 3 bodies, both orders. **Kill** if mixed curvature does not predict which upgrades break drivers (ρ ≥ 0.6).
- **Old-skill retention:** Skills after both orders.
- **Risk / likely tie:** Possibly an assay.

### EE26 · Driver distilled into the low-level controller
- **Primitive** (new storage: compile the driver into feedforward and gain schedules in the robot's controller, so body memory lives in firmware).
- **Mechanism:** Fit controller-level parameters that reproduce the driver; policies and even the network runtime can change without touching body memory.
- **Nearest prior / gap:** Root EL31 (gains as a storage medium); [Tune to learn](https://arxiv.org/abs/2604.02523).
- **Cheapest first test:** Arm with gear wear. **Kill** if the distilled controller loses > 10% of the network driver's benefit.
- **Old-skill retention:** Skills under a swapped policy.
- **Risk / likely tie:** Curved compensation may not compile into gains.

## Ranked deeper questions

1. **Does treating a skill as a section over the body archive beat one-shot transport?** (EE01, EE02, EE04) This is where backward transfer becomes an object (the archive) with its own operations (ghost regularization, harmonic extension). First test: EE01 against ED14 transport, RMA set to old bodies and per-body fine-tuning.
2. **Does one driver serve several policy versions, and can versions be trained to keep it valid?** (EE11, EE12) This is ED20's reuse claim plus a backward-compatibility constraint for control. First test: EE11 across two versions, then EE12 under a width upgrade.
3. **Is the typed residual a smaller and better body channel than an RMA latent?** (EE13, EE14) If yes, the driver tells a policy exactly what it must know about its body. First test: EE13 at matched return.
4. **Does splitting memory by artifact lifetime improve lifelong retention?** (EE18, EE25) Body memory on the unit, skill memory in the policy, and their mixed curvature as the test of independence. First test: EE18 with 2 units × 3 versions.
5. **Can the archive and drivers support legacy hardware and pre-deployment checks?** (EE22, EE23) Backport and regression without hardware make the two kept ideas operational for fleets. First test: EE23's predicted-vs-measured regressions.
