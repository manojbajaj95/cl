# Embodied learners, depth 2: the body connection — holonomy as skill, curvature as the limit of body-blindness

Depth-2 node under [tree/embodied-learners-2.md](embodied-learners-2.md) ([PR #396](https://github.com/manojbajaj95/cl/pull/396)), itself under [tree/root-embodied-learners.md](root-embodied-learners.md) ([PR #395](https://github.com/manojbajaj95/cl/pull/395)) · 26 candidate primitives (EC01–EC26) · 5 ranked deeper questions · Ideas only; no experiments run

**What the review kept (score 3, no 4).** From the [PR #396 triage row](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md):
- **(a) Skill is what survives a closed body loop** (EB01). After A→B→A, the net weight change is skill and the rest is compensation. Controls: fingerprint-keyed rollback, no rollback, adapters keyed by true body version, RMA, EWC, residual magnitude against skill gained on held-out tasks, repeated loops, loops created with software perturbations.
- **(b) Body-blind skills** (EB11 + EB12). Skill updates are confined to the null space of the calibration-motion ("ritual") Jacobian, or all skills are wrapped in one action conjugator trained only on ritual and free-motion data. Controls: EL27 soft routing, RMA latent, domain randomization, GPM, PCGrad, replay validity after body change, skill loss from the constraint, per-skill retention under wear.

**Thesis: (a) and (b) are one object.** Define a **body connection** \(\Gamma\): a learned map from an infinitesimal body change \(dh\) (measured by the ritual) to the weight change \(d\theta = \Gamma(h)\,dh\) that compensates it. Transporting the policy along a body path with \(\Gamma\) is pure compensation. Then:
- (b) asks for a **flat** connection: if \(\Gamma\) has zero curvature, compensation is path-independent, a single global conjugator exists, and skills can be body-blind.
- (a) measures **holonomy**: around a closed loop, transport by a flat \(\Gamma\) returns to the start, so any residual is either skill learning or curvature.
- **Curvature** \(F = d\Gamma + \Gamma\wedge\Gamma\) is therefore the exact obstruction to body-blindness. It marks the regions of body space where a skill *must* depend on the body (a different strategy with a heavy payload, a different grasp with a lost finger). It also separates the holonomy residual into "skill learned" (present even with \(F=0\)) and "body-dependent skill" (proportional to the curvature enclosed).

This moves both kept ideas from bookkeeping (what to pop, what to project) to a new learnable object with a measurable invariant. The cards below build \(\Gamma\), measure \(F\), and use \(F\) to decide where body-blindness is possible and where it must yield. Nearest uses of the same mathematics are representation holonomy as a similarity measure ([Gauge-invariant representation holonomy](https://arxiv.org/abs/2601.21653)), Lie-bracket order effects between *tasks* ([Lie-bracket prediction of transfer order](https://arxiv.org/abs/2606.24993), [Lie bracket as an early warning for forgetting](https://arxiv.org/abs/2611.20087)) and measurement-induced bundles for dynamics under environmental constraints ([2505.19521](https://arxiv.org/abs/2505.19521)). None defines a connection over *body* space, or uses its curvature to bound body-blindness or decompose loop residuals.

**Shared controls.** The reviewer's controls above, plus a measured-parameter-conditioned policy, task-vector negation ([2608.04692](https://arxiv.org/abs/2608.04692)), [PEA](https://arxiv.org/abs/2611.28308) and ER at equal budget. Ledger rules from the root still apply: uniform-rehearsal controls ([PR #119](https://github.com/manojbajaj95/cl/pull/119)), split-half reliability (G1), ≥ 10 seeds, named bridge assumptions ([PR #126](https://github.com/manojbajaj95/cl/pull/126)). Testbeds: CPU MuJoCo bodies with XML edits (gear, damping, mass, link length) and software perturbations (gains, latency), then LIBERO with PEA-style actuation shifts.

## Literature check

alphaXiv searches on holonomy and parallel transport of network parameters, gauge and fiber-bundle formulations of control, equivariant and morphology-symmetric policies, hysteresis compensation, Lie brackets and order dependence of SGD, real-to-sim-to-real cycles and cross-embodiment world models, on top of the root and depth-1 checks.

| Line | Nearest prior | What the body connection adds |
|---|---|---|
| Holonomy and connections in deep learning | [Representation holonomy](https://arxiv.org/abs/2601.21653), [Sheaf networks and holonomy](https://arxiv.org/abs/2607.19514), [Mode connectivity](https://arxiv.org/abs/2308.12666), [Walking the weight manifold](https://arxiv.org/abs/2505.22994) | Holonomy of features over inputs, or paths between minima. Not a connection over physical body states that the learner traverses. |
| Order effects of updates | [Lie-bracket transfer order](https://arxiv.org/abs/2606.24993), [Lie bracket and forgetting](https://arxiv.org/abs/2611.20087), [Commutator memory](https://arxiv.org/abs/2609.34348), NP5-01 bracket (reviewer row 556) | Brackets between *task* gradient fields. Body curvature is a bracket between *compensations* along two body directions, measurable without task data. |
| Bundles and symmetry in control | [Measurement-induced bundles](https://arxiv.org/abs/2505.19521), [Cross-space symmetry compositions](https://arxiv.org/abs/2605.22639), [MIRROR](https://arxiv.org/abs/2610.17422), [GaugeBench](https://arxiv.org/abs/2610.07597) | Fixed, known symmetries or constraint manifolds. A learned, possibly curved, compensation map over drifting bodies is new. |
| Body factorization | [RMA](https://arxiv.org/abs/2107.04034), [Deep inverse dynamics transfer](https://arxiv.org/abs/1610.03518), [Learning to undo](https://arxiv.org/abs/2611.23081), [TeAR](https://arxiv.org/abs/2609.36182), [PEA](https://arxiv.org/abs/2611.28308) | All assume one conjugator/latent suffices (flatness), without testing it. |
| Sim–real cycles | [Getting out and getting back](https://arxiv.org/abs/2610.00821), [Real-is-Sim](https://arxiv.org/abs/2504.03597), [RealSimLoop](https://arxiv.org/abs/2609.09828) | Cycles are used for data. The residual of a sim→real→sim policy loop as "what real taught" is new. |
| Cross-embodiment world models | [Latent-action cross-embodiment world models](https://arxiv.org/abs/2610.10846), [AnyWorld](https://arxiv.org/abs/2608.29242), [OmniAct](https://arxiv.org/abs/2611.33158) | Shared latent actions across bodies, trained jointly; no continual transport or curvature. |
| Hysteresis | [Neural hysteretic kinematics](https://arxiv.org/abs/2404.07168), [Tendon-sheath hysteresis compensation](https://arxiv.org/abs/2011.01817) | Path-dependent bodies are compensated per device; their effect on holonomy (a loop that does not close physically) is unaddressed. |

---

## A · Building the connection

### EC01 · Learn the body connection \(\Gamma\) from the ritual
- **Primitive** (new object: a learned map from ritual-measured body change to compensating weight change).
- **Mechanism:** Small network \(\Gamma_\phi(h)\) outputs a low-rank weight-space direction per ritual-trace direction. Train it on ritual and free-motion data only: transporting the policy by \(\Gamma\) along a body path must keep the ritual's predicted trace equal to the factory trace. Skills are never trained through \(\Gamma\); they move along it.
- **Nearest prior / gap:** EB12's conjugator is \(\Gamma\) integrated under the flatness assumption; hypernetworks from context ([HypEMBER](https://arxiv.org/abs/2607.19628)) map context to weights trained on task data. A connection trained on the ritual and used for transport is new.
- **Cheapest first test:** Pusher, 4 skills, gear and damping drift on 2 joints. Arms: EB12 conjugator, RMA latent, EL27 soft routing, domain randomization, \(\Gamma\)-transport. **Kill** if \(\Gamma\)-transport does not beat EB12 on zero-shot return of skills never trained under drift, over 10 seeds.
- **Old-skill retention:** Every skill on the current and factory body.
- **Risk / likely tie:** Under a flat drift family, \(\Gamma\) and the conjugator coincide; the test uses a curved family (EC02) too.

### EC02 · Curvature as a measurable, label-free quantity
- **Primitive** (new object: \(F\), the curvature of \(\Gamma\), estimated from infinitesimal body loops).
- **Mechanism:** Use software perturbations along two body directions \(u,v\) (gain on joint 1, latency) to run a small square loop; transport the policy around it with \(\Gamma\); the residual over the loop area estimates \(F(u,v)\). No task data is needed.
- **Nearest prior / gap:** Task-gradient Lie brackets ([2606.24993](https://arxiv.org/abs/2606.24993), [2611.20087](https://arxiv.org/abs/2611.20087)) and the reviewer's NP5-01 bracket measure order effects between data sources. A bracket between body compensations estimated from physical micro-loops is new.
- **Cheapest first test:** Construct two drift families in MuJoCo: one flat by design (gear scaling, compensable by action rescaling) and one curved (link length plus payload, which changes the optimal strategy). **Kill** if estimated \(\|F\|\) does not separate the two families at AUROC ≥ 0.9.
- **Old-skill retention:** Not a write; ensure micro-loops do not drift skills (return before/after ≥ 98%).
- **Risk / likely tie:** Noise in small loops; loop size versus noise is part of the test.

### EC03 · Flatness test: when body-blindness is possible
- **Primitive** (new criterion: body-blind skills are allowed exactly where \(F\approx 0\)).
- **Mechanism:** Over the visited body region, if curvature is near zero, enforce EB11's hard null-space constraint; where \(F\) is large, relax it for the skills whose sensitivity overlaps \(F\)'s directions. Body-blindness becomes a region-dependent property derived from geometry, not a global design choice.
- **Nearest prior / gap:** EL27 soft routing tunes one global strength; GPM/PCGrad have no body notion.
- **Cheapest first test:** EC02 families. Arms: global hard constraint, global soft routing, curvature-gated. **Kill** if curvature-gated does not beat both on the *curved* family while matching the hard constraint on the flat one.
- **Old-skill retention:** Per-skill retention in both families.
- **Risk / likely tie:** A tuned soft routing may land in between.

### EC04 · Holonomy decomposition: skill learned versus body-dependent skill
- **Primitive** (new operation: split a loop residual into a curvature term and a learning term).
- **Mechanism:** For a loop \(\gamma\) traversed while learning, residual \(\Delta_\gamma = \text{(enclosed curvature)} + \text{(skill learned)}\). Estimate the first from EC02 and subtract; what remains is body-independent skill gain that should be kept on every body. The curvature part is body-specific skill to store keyed by region (not compensation to discard).
- **Nearest prior / gap:** EB01 treats the whole residual as skill. Separating out enclosed curvature is new.
- **Cheapest first test:** Hopper loops in a curved family with a new skill learned in the loop. **Kill** if the corrected residual does not predict held-out-task skill gain better than the raw residual (Spearman improvement ≥ 0.2), the reviewer's "residual against skill gained on held-out tasks" control.
- **Old-skill retention:** Pre-loop skills and the in-loop skill after 5 loops.
- **Risk / likely tie:** If curvature is small in practice, EB01 already suffices.

### EC05 · Gauge-invariant skill descriptors (Wilson loops)
- **Primitive** (new object: skill features that are invariant under any compensation, built from loop transports).
- **Mechanism:** A skill's description in weight space changes with compensation (gauge). Loop transports of the skill's outputs around fixed small body loops are gauge-invariant (Wilson loops). Use them as body-invariant keys for retrieval and as a forgetting metric: if a skill's Wilson-loop signature changes, the skill changed, not the body.
- **Nearest prior / gap:** [Representation holonomy](https://arxiv.org/abs/2601.21653) uses holonomy for similarity; [GaugeBench](https://arxiv.org/abs/2610.07597) shows description dependence. Gauge-invariant forgetting metrics over body changes are new.
- **Cheapest first test:** Ant with drift and new skills. **Kill** if the Wilson-loop forgetting signal does not predict measured forgetting under body drift at ρ ≥ 0.6, where raw output distance fails (ρ < 0.3).
- **Old-skill retention:** Is the target.
- **Risk / likely tie:** May be a detector (assay) unless used to gate writes; EC06 does that.

### EC06 · Write only gauge-invariant change
- **Primitive** (new operation: skill updates are projected onto directions that change Wilson-loop signatures, discarding pure gauge).
- **Mechanism:** A body-blind skill update should change only gauge-invariant content. Project each skill gradient onto the directions that move EC05's signatures; the rest is compensation and goes to \(\Gamma\). This replaces EB11's ritual null space (which assumes flatness) with an invariant that is still correct in curved regions.
- **Nearest prior / gap:** EB11 null space; GPM/OGD.
- **Cheapest first test:** EC02 curved family. **Kill** if gauge-projected updates do not beat EB11's null space on both untrained-skill transfer and per-skill retention in the curved family.
- **Old-skill retention:** Per-skill return under wear.
- **Risk / likely tie:** Signature gradients are costly; use 2–4 loops.

## B · Loops the robot can traverse

### EC07 · Active loop design
- **Primitive** (new operation: choose which body loops to traverse to best separate skill from compensation).
- **Mechanism:** Loops differ in what they reveal. Choose software-perturbation loops that maximize the Fisher information of the holonomy decomposition (EC04) for the skills currently changing, at bounded wear and time.
- **Nearest prior / gap:** [IDTD](https://arxiv.org/abs/2610.10905) designs excitation for physical parameters; EB14 designs the ritual. Designing *loops* for skill/compensation separation is new.
- **Cheapest first test:** EC04 setting, 3 loops per round: random, IDTD-style, active. **Kill** if active loops do not reduce decomposition error by ≥ 30% versus random at equal loop time.
- **Old-skill retention:** As EC04.
- **Risk / likely tie:** Random loops may be enough in low dimension.

### EC08 · Sim→real→sim holonomy: what real data taught
- **Primitive** (new object: the residual of a sim→real→sim policy loop as the real-world knowledge to keep).
- **Mechanism:** Fine-tune in real, transport back to sim with \(\Gamma\) (sim and real as two "bodies"), and compare to the original sim policy. The loop residual is what real taught that sim lacked (keep, and push into the simulator); the rest is sim-specific compensation (discard on return to real).
- **Nearest prior / gap:** [Getting out and getting back](https://arxiv.org/abs/2610.00821) and [Real-is-Sim](https://arxiv.org/abs/2504.03597) co-train or twin; [Frozen in time](https://arxiv.org/abs/2610.40857) shows erosion. A holonomy over the sim–real pair is new.
- **Cheapest first test:** HalfCheetah sim versus friction-changed "real". **Kill** if the residual does not identify the changed dynamics region better than the fidelity map of root EL12.
- **Old-skill retention:** Sim skills and real skills after two loops.
- **Risk / likely tie:** Sim and real differ in more than a body; \(\Gamma\) may not cover the gap.

### EC09 · Cross-body holonomy: skill learned through another body
- **Primitive** (new operation: robot1→robot2→robot1 transfer loop, residual = body-invariant improvement gained on robot 2).
- **Mechanism:** Transport robot 1's policy to robot 2 with a cross-body connection, learn there, transport back. The residual is skill improvement that robot 1 gains from robot 2's practice, with robot 2's compensation cancelled.
- **Nearest prior / gap:** [REvolveR](https://arxiv.org/abs/2202.05244) transfers one way; joint cross-embodiment training ([CrossFormer](https://arxiv.org/abs/2408.11812), [HPT](https://arxiv.org/abs/2409.20537)) has no loop. The round trip as a learning operation is new.
- **Cheapest first test:** Reacher-2 and Reacher-3. **Kill** if the round-trip residual improves robot 1 less than joint multi-body training at equal robot-2 samples.
- **Old-skill retention:** Robot 1's other skills after the round trip.
- **Risk / likely tie:** Joint training is strong.

### EC10 · Hysteretic bodies: loops that do not close physically
- **Primitive** (new object: a connection with memory state, for bodies whose physical loop itself has a residual).
- **Mechanism:** Backlash, cable stretch and thermal effects make A→B→A not return to A. Model the body state as \((h, m)\) with a hysteresis memory \(m\) estimated from the ritual's direction-dependent trace; \(\Gamma\) acts on both. Otherwise physical hysteresis is misread as skill in the holonomy.
- **Nearest prior / gap:** Hysteresis compensation exists for continuum robots ([2404.07168](https://arxiv.org/abs/2404.07168), [2011.01817](https://arxiv.org/abs/2011.01817)), per device; none considers its effect on learning-loop residuals.
- **Cheapest first test:** MuJoCo joint with simulated backlash in a loop. **Kill** if the memory-augmented connection does not reduce false "skill" in the residual by ≥ 50% versus EC04.
- **Old-skill retention:** As EC04.
- **Risk / likely tie:** Real hysteresis may be too small to matter.

### EC11 · Irreversibility from failed transport
- **Primitive** (new operation: detect permanent damage as a loop whose \(\Gamma\)-transport cannot be closed by any ritual-consistent path).
- **Mechanism:** If after "repair" the ritual trace cannot be brought back to A's by transport, the body did not return; label the change irreversible and stop keeping the A-version compensation reachable.
- **Nearest prior / gap:** [Reset-free recovery after damage](https://arxiv.org/abs/2610.20838) and [REVERSAL-BENCH](https://arxiv.org/abs/2609.17745) treat irreversibility in task state, not in body.
- **Cheapest first test:** 10 repairs, 3 incomplete. **Kill** if detection AUROC < 0.85 or a simple ritual-distance threshold does as well.
- **Old-skill retention:** Skills after incomplete repairs (no shock from popping a wrong compensation).
- **Risk / likely tie:** Likely ties a threshold; then graded as assay.

## C · Body-blind skills, deepened

### EC12 · Gradient-level body invariance
- **Primitive** (new property: a skill's *learning signal* is body-invariant after transport, not only its outputs).
- **Mechanism:** Require that skill gradients computed on body B, transported by \(\Gamma\) to factory coordinates, equal gradients computed on the factory body (self-perturbation supplies paired data). Then practice on any body is equally valid practice for every body, so a worn robot's practice improves the skill for the repaired robot.
- **Nearest prior / gap:** Output invariance (domain randomization, EB11). Optimizer equivariance studies ([Same function, different trajectory](https://arxiv.org/abs/2610.18085)) show gradients are not invariant to reparameterization. Gradient invariance across bodies as a training target is new.
- **Cheapest first test:** Practice skill on worn Ant, evaluate on factory. Arms: domain randomization, EB11, gradient-invariant. **Kill** if gradient invariance does not give ≥ 20% more factory-body gain per worn-body episode than EB11.
- **Old-skill retention:** Other skills on both bodies.
- **Risk / likely tie:** Paired gradients may be too costly.

### EC13 · Conjugator algebra: composing body changes
- **Primitive** (new object: conjugators that compose, \(g_{\text{tool}}\circ g_{\text{wear}}\), and whose failure to compose is curvature).
- **Mechanism:** Learn conjugators for single changes (tool, wear, payload) and predict combinations by composition. Where composition fails, the measured gap is the cross-curvature \(F(\text{tool},\text{wear})\) and tells which combination needs its own skill variant.
- **Nearest prior / gap:** [Cross-space symmetry compositions](https://arxiv.org/abs/2605.22639) compose known symmetries; root EB06 measures delta commutators. Composition of learned body conjugators with curvature as the residual is new.
- **Cheapest first test:** 3 changes on Pusher, 4 combinations held out. **Kill** if composed conjugators do not beat a conjugator conditioned on the combination's measured parameters on held-out combos.
- **Old-skill retention:** All skills under single and combined changes.
- **Risk / likely tie:** The conditioned control is strong.

### EC14 · Non-conjugable residual promotes body-specific skills
- **Primitive** (new operation: where curvature is high, automatically create a body-conditioned skill variant; everywhere else keep one body-blind skill).
- **Mechanism:** Monitor \(F\) along each skill's operating region. When it crosses a threshold, fork that skill into a body-region-keyed variant initialized by transport; merge back when \(F\) falls. Skill count grows only where geometry demands.
- **Nearest prior / gap:** Adapter expansion ([SARAM](https://arxiv.org/abs/2610.24804)) grows by task interference; MoE fault experts ([2606.25965](https://arxiv.org/abs/2606.25965)) are fixed. Growth by body curvature is new.
- **Cheapest first test:** EC02 curved family. **Kill** if curvature-triggered forks do not beat interference-triggered expansion at equal parameter count.
- **Old-skill retention:** Unforked skills unchanged; forked skill on both regions.
- **Risk / likely tie:** Threshold tuning.

### EC15 · Body-blind world model
- **Primitive** (new object: a world model in factory-body coordinates whose dreams stay valid after any flat body change).
- **Mechanism:** Train the world model on transported data so it never models compensation. Rehearsal in it ([dream rehearsal](https://arxiv.org/abs/2607.19749)) stays valid after body drift; only \(\Gamma\) needs refitting.
- **Nearest prior / gap:** Cross-embodiment world models ([2610.10846](https://arxiv.org/abs/2610.10846), [AnyWorld](https://arxiv.org/abs/2608.29242)) are trained jointly; [CAWM](https://arxiv.org/abs/2609.18950) flushes stale replay.
- **Cheapest first test:** Model-based Ant with 4 body changes. **Kill** if the body-blind world model does not beat CAWM on post-change return within 50 episodes.
- **Old-skill retention:** Old skills via dream rehearsal after each change.
- **Risk / likely tie:** Merges with EB22 if equal.

### EC16 · Heterogeneous demonstrations through the connection
- **Primitive** (new operation: continual imitation from demonstrators on different bodies, transported into factory coordinates before learning).
- **Mechanism:** Teleoperation demos from other arms, or from the same arm in a worn state, are transported by a cross-body or wear connection; skills learn only gauge-invariant content (EC06).
- **Nearest prior / gap:** [Grounded continual imitation](https://arxiv.org/abs/2610.00542) and retargeting ([2509.15443](https://arxiv.org/abs/2509.15443)) map demos geometrically; no curvature-aware transport.
- **Cheapest first test:** Demos from 3 arm variants into 1 policy. **Kill** if transported demos do not beat retargeted demos on target success with equal demos.
- **Old-skill retention:** Earlier-demo skills after later variants.
- **Risk / likely tie:** Retargeting may suffice for kinematic differences.

### EC17 · Soft-to-hard annealing by curvature confidence
- **Primitive** (new schedule: body-blindness hardens as curvature estimates become confident).
- **Mechanism:** Start with EL27 soft routing; harden to EB11's null space in regions where EC02 confidently shows \(F\approx 0\).
- **Nearest prior / gap:** Soft routing (EL27); DRAP-style plasticity.
- **Cheapest first test:** EC03 setting with noisy curvature. **Kill** if annealing does not beat the better of fixed soft and fixed hard.
- **Old-skill retention:** Per-skill.
- **Risk / likely tie:** Close to EC03; merge if equal.

### EC18 · Conjugators for action chunks in VLAs
- **Primitive** (new object: \(\Gamma\) acting on action-chunk tokens of a frozen VLA).
- **Mechanism:** Apply the connection to the decoded action chunk; the VLA stays frozen and body-blind; \(\Gamma\) is fit from a ritual and PEA-style probes.
- **Nearest prior / gap:** [PEA](https://arxiv.org/abs/2611.28308) calibrates under actuation shifts with a frozen base; it does not test path dependence or composition.
- **Cheapest first test:** LIBERO-Spatial with gain, stiffness and payload shifts visited in two orders. **Kill** if \(\Gamma\) does not beat PEA on the second-order visit (where path dependence matters).
- **Old-skill retention:** Original-setup success after the cycle.
- **Risk / likely tie:** PEA's shifts may be flat.

## D · Consequences and assays

### EC19 · Loop-gated consolidation
- **Primitive** (new operation: consolidate into long-term memory only what survives a body loop).
- **Mechanism:** Fast weights learn freely; at each closed loop, the curvature-corrected residual (EC04) is consolidated into slow weights and the rest decays.
- **Nearest prior / gap:** [Sleep consolidation](https://arxiv.org/abs/2606.17493) consolidates by time; root EL05 by cool-down cycles. Consolidation gated by physical loop closure is new.
- **Cheapest first test:** EC04 setting with 5 loops. **Kill** if loop-gated consolidation does not beat time-gated consolidation on held-out-body return.
- **Old-skill retention:** Slow-weight skills after many loops.
- **Risk / likely tie:** Few loops in practice; EC07 makes them.

### EC20 · Body visit order as a control variable
- **Primitive** (new operation: choose the order of body changes during training, using curvature, to minimize harmful path effects).
- **Mechanism:** With \(F\) known, order body exposures (sim randomization or real tool use) so that enclosed curvature on skill-relevant directions is minimal.
- **Nearest prior / gap:** [Lie-bracket transfer order](https://arxiv.org/abs/2606.24993) orders data sources for LMs.
- **Cheapest first test:** 4 body changes, all 24 orders on Reacher. **Kill** if curvature-predicted best order is not in the top quartile of measured orders.
- **Old-skill retention:** Under the chosen order.
- **Risk / likely tie:** Order effects may be small.

### EC21 · Forgetting decomposition under body drift
- **Assay** (decomposes forgetting into compensation, curvature and task interference).
- **Mechanism:** Total skill change = transport (compensation, no forgetting) + curvature term + task-interference term.
- **Nearest prior / gap:** [Stability gap in CRL](https://arxiv.org/abs/2611.26252) and dynamics-shift replay studies do not decompose by body geometry.
- **Cheapest first test:** Root EL32 matrix. **Kill** if the three terms do not sum to the measured change within 10%.
- **Old-skill retention:** Is the measure.
- **Risk / likely tie:** Assay.

### EC22 · Curvature map as safety information
- **Primitive** (new use: high-curvature body regions are where safe sets transported by \(\Gamma\) are unreliable).
- **Mechanism:** Shrink transported safe sets (root EL20, depth-1 EB26) in proportion to enclosed curvature along the path from the certified body.
- **Nearest prior / gap:** [SafeAdapt](https://arxiv.org/abs/2604.09452), [SEVI](https://arxiv.org/abs/2610.31829) are single-body.
- **Cheapest first test:** 2-link arm with curved mass/length family. **Kill** if curvature-scaled shrink does not lower violations versus uniform shrink at equal set volume.
- **Old-skill retention:** Task return inside the shrunk sets.
- **Risk / likely tie:** Uniform shrink tuned per body may tie.

### EC23 · Morphology-changing connections
- **Primitive** (new object: a connection between bodies with different DOF, as a learned fiber map).
- **Mechanism:** For bodies with different joint counts, \(\Gamma\) maps between different fibers (action spaces); a learned retargeting is its flat special case.
- **Nearest prior / gap:** [Implicit kinodynamic retargeting](https://arxiv.org/abs/2509.15443), [KITE](https://arxiv.org/abs/2606.22113), [MetaMorph](https://arxiv.org/abs/2203.11931).
- **Cheapest first test:** 4-leg → 6-leg Ant. **Kill** if fiber-map transport does not beat retargeting plus fine-tuning on 6-leg return with equal samples.
- **Old-skill retention:** 4-leg skills after 6-leg learning.
- **Risk / likely tie:** Large DOF changes may defeat a connection.

### EC24 · Ritual-free connection from proprioceptive futures
- **Primitive** (new operation: fit \(\Gamma\) from free play by matching predicted proprioceptive futures to a factory forward model).
- **Mechanism:** For robots with no ritual time, use any motion: transport must make the factory forward model's predictions match observed proprioception.
- **Nearest prior / gap:** [Deep inverse dynamics transfer](https://arxiv.org/abs/1610.03518), depth-1 EB27 task-fragment rituals.
- **Cheapest first test:** EC01 setting without ritual. **Kill** if free-play \(\Gamma\) loses > 20% of ritual-\(\Gamma\) transfer.
- **Old-skill retention:** As EC01.
- **Risk / likely tie:** Task-correlated motion biases the fit.

### EC25 · Holonomy-based credit for fleets
- **Primitive** (new operation: aggregate skill updates across a fleet only through their loop-corrected residuals).
- **Mechanism:** Each robot sends only curvature-corrected loop residuals (body-invariant skill gain) to a shared skill model; compensation stays local.
- **Nearest prior / gap:** [Fleet policy merging](https://arxiv.org/abs/2310.01362), [collective experience across 96 robots](https://arxiv.org/abs/2610.25736), depth-1 EB09.
- **Cheapest first test:** 4 Ant copies with different wear. **Kill** if residual-only aggregation does not beat policy merging on every robot's held-out skill.
- **Old-skill retention:** Each robot's local skills after aggregation.
- **Risk / likely tie:** Policy merging with RMA-style conditioning may tie.

### EC26 · Curvature spectrum of real robots
- **Assay** (gates the whole node).
- **Mechanism:** Measure \(\|F\|\) over common drift directions (gear, damping, latency, payload, camera) on simulated and logged real robots.
- **Nearest prior / gap:** None found.
- **Cheapest first test:** EC02 on 5 drift directions × 3 bodies. **Kill (of the node's curvature half)** if all measured curvatures are within noise of zero; then one conjugator suffices and only EC01/EC12 survive.
- **Old-skill retention:** Not applicable.
- **Risk / likely tie:** Assay.

## Ranked deeper questions

1. **Is real body drift curved?** (EC26, EC02) If every common drift is flat, a single conjugator (EB12) is enough and the holonomy half collapses into rollback. If some drift is curved, curvature is the first principled bound on how body-blind skills can be. First test: EC02's flat-versus-curved families, then EC26.
2. **Does subtracting enclosed curvature make the loop residual a true skill measure?** (EC04, EC19) This is the reviewer's "residual against held-out skill gain" control, now with a reason the raw residual fails. First test: EC04 on Hopper.
3. **Can body-blind learning signals make practice on any body count for every body?** (EC12) Gradient-level invariance is stronger than EB11's output invariance and would let a worn robot's practice transfer to the repaired one. First test: EC12 against EB11 and domain randomization.
4. **Does a learned connection beat a conjugator when changes compose?** (EC13, EC14) Composition failure is where single-latent methods (RMA, PEA) should break. First test: EC13's held-out combinations.
5. **Does the connection scale to frozen VLAs?** (EC18) PEA restores most success under actuation shifts; the open question is path dependence across repeated, ordered shifts. First test: EC18 on LIBERO-Spatial.
