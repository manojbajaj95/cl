# Embodied learners, depth 3: making the body connection Γ stand on its own

Depth-3 node under [tree/embodied-learners-3.md](embodied-learners-3.md) ([PR #397](https://github.com/manojbajaj95/cl/pull/397)) → [#396](https://github.com/manojbajaj95/cl/pull/396) → [#395](https://github.com/manojbajaj95/cl/pull/395) · 26 candidate primitives and tests (ED01–ED26) · 5 ranked deeper questions · Ideas only; no experiments run

**Where the review left Γ.** From the [PR #397 triage row](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md): EC01+EC02+EC04 (learn a body connection Γ from ritual and free-motion data, estimate its curvature from software-perturbation micro-loops, subtract enclosed curvature from the loop residual) is the candidate closest to 4 since the top 10 was set. It reaches 4 only if real drift is curved (EC26); if every drift is flat, Γ collapses to depth-1's single conjugator (EB12). EC13+EC14 (compose single-change conjugators, read the composition gap as cross-curvature, fork a skill only where it is large) stays at 3. Controls named: EB12 conjugator, EB01 raw residual, keyed rollback, RMA, PEA, domain randomization, residual-minus-curvature against held-out skill gain, curvature estimate stability, retention over repeated and ordered loops.

**Γ as a standalone primitive.** Body states \(h\) (measured by the ritual) form a base space. Over each \(h\) sits the space of policies that are correct for that body. Γ is a learned connection on this bundle: it says how to move a policy when the body moves by \(dh\), using no task data. It brings four operations no prior continual-learning method has together:
1. **Transport** a skill along a body path.
2. **Holonomy:** the residual after a closed path.
3. **Curvature** \(F\): holonomy per unit area, measured from micro-loops.
4. **Flatness test:** \(F\approx0\) on a region means one global conjugator exists there.

What makes it more than a reparametrized RMA latent is that \(F\) is an *invariant*: it does not depend on how bodies or weights are coordinatized, it can be predicted from physics before any learning (section A), and it says something a body-conditioned policy cannot: where body-conditioning is *necessary*.

**This node's job.** (A) Give independent, physics-level reasons why some drift directions must be curved and others flat, so the curvature claim is a falsifiable prediction rather than a hope. (B) Build the sharpest kill tests, including ones that kill Γ in favour of RMA or PEA. (C) Say what Γ enables beyond rollback and routing. (D) Meet the strongest prior art head-on: gauge-equivariant networks, Fishr and gradient matching, RMA, PEA, domain randomization.

**Shared controls.** All of #397's controls, plus a body-conditioned policy trained on the *same* ritual data (the fairest RMA), Fishr with bodies as environments, and an action-space PEA-style calibrator re-run at each body. Ledger rules hold (uniform-rehearsal control, split-half reliability, ≥ 10 seeds, named bridge assumptions). Testbeds: MuJoCo arms and Ant with torque limits, XML edits, learned actuator models ([2604.10351](https://arxiv.org/abs/2604.10351), [2607.02205](https://arxiv.org/abs/2607.02205)) for realistic drift, then LIBERO with PEA's actuation shifts.

## Literature check

New searches for this node: gauge-equivariant networks and learned connections, invariant gradient variances and gradient matching, gait-transition bifurcations under body change, torque saturation under actuator degradation, friction and contact-mode changes, sensitivity of optimal policies to dynamics parameters, curvature of learned dynamics manifolds, and integrability tests for learned maps.

| Prior art | What it does | Why Γ is not it |
|---|---|---|
| [Gauge equivariant CNNs](https://arxiv.org/abs/1902.04615), [lattice gauge-equivariant nets](https://arxiv.org/abs/2012.12901), [torsor CNNs](https://arxiv.org/abs/2510.23288) | Hard-code a *known* connection on a given manifold so features transform correctly | Γ is *learned* from a robot's own body data; its curvature is the measured quantity, not a fixed input. ED22 uses gauge-equivariance *given* a learned Γ. |
| [Fishr](https://arxiv.org/abs/2109.02934), [gradient matching for DG](https://arxiv.org/abs/2104.09937), [Hessian alignment](https://arxiv.org/abs/2308.11778) | Match gradient statistics across environments for invariance | They seek one invariant predictor across environments (implicitly flat). Γ says *where* invariance is impossible. ED23 tests transported Fishr against Fishr. |
| [RMA](https://arxiv.org/abs/2107.04034), [meta-RL adaptation](https://arxiv.org/abs/1803.11347) | Body latent \(z\) and a policy conditioned on it, trained over a body distribution | A conditioned policy is a global section of the bundle, fixed at training. It cannot transport skills learned later, and it gives no invariant saying where conditioning is needed. ED10, ED24. |
| [PEA](https://arxiv.org/abs/2611.28308) | Probes actuation shifts and calibrates a frozen visuomotor policy at test time | A memoryless, action-space flat connection at one body. It has no path, so no holonomy and no order effects. ED25. |
| [Domain randomization](https://arxiv.org/abs/1703.06907) | One policy for the whole family | Averages conflicting strategies in curved regions. ED26 predicts DR regret from \(F\). |
| [Representation holonomy](https://arxiv.org/abs/2601.21653), [Lie-bracket forgetting warning](https://arxiv.org/abs/2611.20087), [curvature-encoded dynamics](https://arxiv.org/abs/2403.11948) | Holonomy of features over inputs; brackets between task gradients; curvature as a latent-dynamics prior | None defines a connection over physical body states or links its curvature to the limits of body-blind skills. |
| Gait transitions: [learned gait transitions](https://arxiv.org/abs/2104.04644), [DeepTransition](https://arxiv.org/abs/2306.07419); [allometric scaling of bipeds](https://arxiv.org/abs/2603.22560); hybrid contact ([2605.16398](https://arxiv.org/abs/2605.16398)); degradation priors ([2610.10934](https://arxiv.org/abs/2610.10934)) | Strategy changes with speed/mass; scaling laws; mode switches | Used in section A as *independent* evidence for where curvature must and must not appear. |

---

## A · Independent reasons drift should be curved (and where it must be flat)

### ED01 · A priori curvature table from the manipulator equation
- **Primitive** (new object: a predicted curvature sign table, derived before learning).
- **Mechanism:** With \(M(q)\ddot q + C(q,\dot q)\dot q + g(q) = K\tau\), a pure actuator-gain change \(K\to K'\) is compensated exactly by \(\tau\to K'^{-1}K\tau\), which is the same for every state and skill. Such directions are **pure gauge (flat)** as long as torques stay unsaturated. Changes to link mass, length or payload enter \(M(q)\) and \(g(q)\) in a configuration-dependent way; two such directions generically do not commute through the policy, so they are **curved**. Write the table for each drift pair *before* measuring.
- **Nearest prior / gap:** Classical adaptive control uses linearity in parameters; no CL work turns it into a flat/curved prediction for a learned connection.
- **Cheapest first test:** 2-link and 3-link arms, 6 drift directions (2 gains, 2 masses, 1 length, 1 payload), all 15 pairs. **Kill** if measured \(\|F\|\) does not match the predicted zero/non-zero pattern on ≥ 12 of 15 pairs, or if gain pairs show curvature above noise (the estimator is then measuring artifacts).
- **Old-skill retention:** Micro-loops must leave skills unchanged (≥ 98% return).
- **Risk / likely tie:** If all physics pairs come out flat at policy level, Γ collapses to EB12. That is the review's gate, now with a prediction.

### ED02 · Saturation creates curvature
- **Primitive** (new prediction: torque limits turn flat gain directions curved).
- **Mechanism:** Gain compensation \(K'^{-1}K\tau\) fails when it exceeds limits; then compensation must reallocate effort across joints, and the reallocation depends on what else has changed. Curvature should be near zero inside the torque envelope and rise sharply at its boundary.
- **Nearest prior / gap:** Degradation papers ([TeAR](https://arxiv.org/abs/2609.36182), [joint-health-aware RL](https://arxiv.org/abs/2610.41348), [voltage-constrained actuation](https://arxiv.org/abs/2605.10696)) handle limits, not their geometric effect.
- **Cheapest first test:** Reacher with gain loss on two joints, torque limit swept from loose to tight. **Kill** if \(\|F\|\) does not increase monotonically as the limit tightens.
- **Old-skill retention:** Skills near the envelope boundary after loops.
- **Risk / likely tie:** Saturation may make compensation infeasible rather than curved; the test separates the two by checking reachability.

### ED03 · Strategy bifurcations are curvature defects
- **Primitive** (new prediction: curvature concentrates at body states where the optimal strategy switches).
- **Mechanism:** Optimal gait switches with mass and speed ([learned gait transitions](https://arxiv.org/abs/2104.04644), [DeepTransition](https://arxiv.org/abs/2306.07419)). A loop around such a boundary should carry large holonomy; a loop that stays on one side should not. Curvature then maps the strategy-switch boundaries in body space without labels.
- **Nearest prior / gap:** Gait-transition work treats boundaries as control facts; none reads them as curvature.
- **Cheapest first test:** Ant with mass × leg-length grid where gait switches are known from exhaustive training. **Kill** if the \(F\) map does not localize the switch boundary (IoU ≥ 0.5 with the boundary band).
- **Old-skill retention:** Both gaits after loops crossing the boundary.
- **Risk / likely tie:** Discontinuities may break the micro-loop estimator; finite-area loops are used.

### ED04 · Contact-mode switches as curvature
- **Primitive** (new prediction: friction or compliance changes that cross a stick/slip or make/break threshold are curved; changes within one mode are flat).
- **Mechanism:** Within one contact mode, a friction change rescales forces (near-gauge); across modes, the skill must change its contact plan ([hybrid contact dynamics](https://arxiv.org/abs/2605.16398)).
- **Nearest prior / gap:** Contact-rich adaptation ([friction margins](https://arxiv.org/abs/2610.36961)) handles modes, not curvature.
- **Cheapest first test:** Pusher, friction × object-mass grid. **Kill** if \(F\) is not ≥ 3× larger on mode-crossing loops than within-mode loops.
- **Old-skill retention:** Push skills in both modes.
- **Risk / likely tie:** Mode boundaries may be thin; grid resolution matters.

### ED05 · Dynamic similarity as a known-flat control
- **Primitive** (new control: body scalings along dynamic-similarity directions must be flat).
- **Mechanism:** Scaling length, mass and time together at constant Froude number leaves dynamics similar ([allometric scaling](https://arxiv.org/abs/2603.22560)); with time rescaling in the policy interface, these directions should be pure gauge. Any curvature measured there is estimator error.
- **Nearest prior / gap:** Scaling laws are not used as calibration for learned-adaptation geometry.
- **Cheapest first test:** Hopper scaled at constant Froude number versus scaled length only. **Kill** if the estimator reports curvature on the Froude family above 20% of the length-only family.
- **Old-skill retention:** As ED01.
- **Risk / likely tie:** Contact and actuator limits break similarity; keep them in-envelope.

### ED06 · Visual and actuation shifts should commute
- **Primitive** (new prediction: in a closed-loop visuomotor policy, camera shifts and actuation shifts are independent directions; their cross-curvature is near zero).
- **Mechanism:** A camera move changes what the policy sees; an actuation shift changes what commands do ([PEA](https://arxiv.org/abs/2611.28308)). If the policy is closed-loop, compensations should act on different interfaces and commute. A non-zero cross-curvature would mean the policy entangles perception with dynamics, which is a measurable defect.
- **Nearest prior / gap:** PEA evaluates "camera + gains" jointly but not order or commutation.
- **Cheapest first test:** LIBERO with camera × gain loops. **Kill** of the *prediction* if cross-curvature is large; then report it as an entanglement finding.
- **Old-skill retention:** Original setup after the loops.
- **Risk / likely tie:** Either outcome is informative; this is the cheapest real-pipeline check of the estimator.

### ED07 · Function-space curvature, not weight-space curvature
- **Primitive** (new requirement: \(F\) is defined on the policy's outputs, not on weights).
- **Mechanism:** Weight-space loops can carry spurious holonomy from parametrization and optimizer non-equivariance ([Same function, different trajectory](https://arxiv.org/abs/2610.18085)). Define transport by function matching on ritual and probe states and measure holonomy as an output difference. Then \(F\) is invariant to reparametrization and comparable across architectures.
- **Nearest prior / gap:** EC02 measured weight residuals.
- **Cheapest first test:** Measure \(F\) for the same physics in two architectures (MLP, transformer) and two optimizers. **Kill** if function-space \(F\) disagrees across them by more than across seeds (then it is not a body property).
- **Old-skill retention:** As ED01.
- **Risk / likely tie:** Function matching on finite probes may miss directions.

## B · Sharpest kill tests

### ED08 · Calibrated estimator on known-flat and known-curved bodies
- **Test** (gates everything else).
- **Mechanism:** Combine ED01 gain pairs and ED05 Froude scaling (known flat) with ED02 saturation and ED03 gait boundaries (known curved). Estimator must report zero on the first and non-zero on the second with split-half reliability ≥ 0.8 across seeds, loop sizes and rituals.
- **Nearest prior / gap:** EC26 measured curvature without calibration.
- **Cheapest first test:** As stated. **Kill** if AUROC (flat vs curved) < 0.9 or reliability < 0.8.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** None; this is the first experiment.

### ED09 · Real-drift curvature from learned actuator models
- **Test** (EC26 made realistic).
- **Mechanism:** Use learned actuator models ([2604.10351](https://arxiv.org/abs/2604.10351), [actuator reality shaping](https://arxiv.org/abs/2607.02205)) fitted to real motors at several wear and temperature states as the drift directions, not synthetic XML edits.
- **Cheapest first test:** Arm with 4 actuator-model states × 2 payloads. **Kill (of the curvature half)** if all measured \(F\) are within the ED08 flat band.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** Sim with real actuator models is still sim; logged real data is the next step.

### ED10 · Γ versus the fairest RMA
- **Test** (the decisive comparison).
- **Mechanism:** A conditioned policy can represent any body dependence, so on a fixed body family it should tie Γ. Γ's claim is *continual*: skills learned after a body change are transported to other bodies with no further body-family training. Give RMA the same ritual data and online fine-tuning.
- **Cheapest first test:** Learn skill S5 only on body B; evaluate on A, C, D. Arms: RMA (ritual-trained latent, policy fine-tuned on S5 at B), EB12 conjugator, Γ transport. **Kill** if Γ does not beat RMA by > 2 SE on S5 at the other bodies in the curved family, or if it loses in the flat family.
- **Old-skill retention:** S1–S4 on all bodies after S5.
- **Risk / likely tie:** RMA's latent may generalize well enough; that is the kill.

### ED11 · Curvature predicts where single-latent methods fail
- **Test.**
- **Mechanism:** If curvature is real, RMA and PEA errors after body change should concentrate in high-\(F\) regions.
- **Cheapest first test:** Ant grid; correlate per-cell RMA/PEA regret with \(F\). **Kill** if Spearman ρ < 0.5.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** RMA failures may be driven by data coverage, not geometry; control by coverage.

### ED12 · Residual-minus-curvature against held-out skill gain
- **Test** (the review's own control, sharpened).
- **Mechanism:** Across 20 loops with known in-loop learning, compare raw residual (EB01), residual minus enclosed \(F\) (EC04) and a keyed-rollback estimate against held-out-task skill gain.
- **Cheapest first test:** Hopper and Ant. **Kill** if residual-minus-curvature does not beat the raw residual by ρ ≥ 0.2 in the curved family.
- **Old-skill retention:** Pre-loop and in-loop skills after 20 loops.
- **Risk / likely tie:** In flat families they tie by design; report both.

### ED13 · Ordered-loop retention
- **Test.**
- **Mechanism:** Visit bodies in orders ABCA and ACBA. Γ predicts the difference in final policy from enclosed curvature; single-latent methods predict none.
- **Cheapest first test:** 3 body changes on Reacher, 6 orders. **Kill** if order effects on retention are below noise, or if Γ's predicted order effects correlate < 0.5 with measured ones.
- **Old-skill retention:** All skills after each order.
- **Risk / likely tie:** Small effects; 10 seeds per order.

## C · What Γ enables beyond rollback and routing

### ED14 · Backward transfer for free
- **Primitive** (new operation: transport skills learned on today's body back to every past body with no data there).
- **Mechanism:** When a skill is learned on worn body B, transport it to A (factory) and to any stored body. Where the path is flat, this is exact; where curved, transport plus enclosed curvature is the best zero-shot guess, and the skill is flagged for practice.
- **Nearest prior / gap:** Backward transfer in CL is measured, rarely produced; root EL23 homotopy walks paths with fine-tuning.
- **Cheapest first test:** ED10 setting. **Kill** if transported skill on A is < 80% of a skill trained on A in flat regions.
- **Old-skill retention:** Existing A skills after transport.
- **Risk / likely tie:** Same as ED10.

### ED15 · Composition with a curvature-licensed fork
- **Primitive** (the review's 3-scored EC13+EC14, made strict).
- **Mechanism:** Compose single-change conjugators; predict the composition gap from ED01's table and measured cross-curvature; fork a skill only where the gap exceeds the ED08 noise band, merge back when it falls.
- **Nearest prior / gap:** [Cross-space symmetry compositions](https://arxiv.org/abs/2605.22639) compose known symmetries; [SARAM](https://arxiv.org/abs/2610.24804) expands by interference.
- **Cheapest first test:** Pusher with tool, wear and payload changes. Arms: one RMA latent, PEA, a conjugator per combination, always-fork, never-fork, curvature-licensed fork. **Kill** if the curvature-licensed arm is not on the Pareto front of held-out-combination success versus skill count.
- **Old-skill retention:** All skills under every combination.
- **Risk / likely tie:** Per-combination conjugators win when combinations are few.

### ED16 · Maintenance order as path planning
- **Primitive** (new operation: choose the order of repairs or tool changes to minimize enclosed curvature on active skills).
- **Mechanism:** With \(F\) known, a maintenance or tool-change sequence is a path; choose the one with least holonomy on skills in use.
- **Nearest prior / gap:** [RUL-aware planning](https://arxiv.org/abs/2610.02469) balances degradation, not policy geometry.
- **Cheapest first test:** ED13 setting. **Kill** if the planned order is not in the top quartile of measured retention.
- **Old-skill retention:** Under the chosen order.
- **Risk / likely tie:** Order effects may be small (ED13 kills first).

### ED17 · Curvature-directed practice
- **Primitive** (new rule: practice budget follows enclosed curvature, because only there transport is insufficient).
- **Mechanism:** After a body change, practice each skill in proportion to the curvature along its operating region; flat-region skills get none.
- **Nearest prior / gap:** Uniform rehearsal beats LP selectors ([PR #119](https://github.com/manojbajaj95/cl/pull/119)); Memory Anchors chooses by representation collapse.
- **Cheapest first test:** 6 skills on Ant through 4 body changes. **Kill** if curvature-directed practice does not beat uniform at equal practice.
- **Old-skill retention:** All 6 skills.
- **Risk / likely tie:** Uniform is a strong baseline.

### ED18 · Transported critics keep off-policy data valid
- **Primitive** (new operation: transport Q-functions with Γ so replay from old bodies remains usable for off-policy RL).
- **Mechanism:** Transport both actor and critic; replay from body A is evaluated by the transported critic.
- **Nearest prior / gap:** [Replay under dynamics shift](https://arxiv.org/abs/2609.18167), [CAWM](https://arxiv.org/abs/2609.18950); depth-1 EB22.
- **Cheapest first test:** SAC on Ant with 4 body changes. **Kill** if transported critics do not beat CAWM flush on post-change return.
- **Old-skill retention:** Old skills via replay.
- **Risk / likely tie:** Merges with EB22 if equal.

### ED19 · Early warning from curvature and skill sensitivity
- **Primitive** (new operation: predict which skills will break under an incoming drift before any task rollout).
- **Mechanism:** Score each skill by the overlap of its sensitivity with \(F\) along the drift direction measured by the ritual.
- **Nearest prior / gap:** [Lie-bracket early warning](https://arxiv.org/abs/2611.20087) uses task gradients and old data; this uses body geometry and none.
- **Cheapest first test:** 8 skills, 5 drifts. **Kill** if AUROC for "skill drops > 20%" is < 0.8 or a sensitivity-only score does as well.
- **Old-skill retention:** Is the target.
- **Risk / likely tie:** Sensitivity alone may suffice in flat families.

### ED20 · Policy-agnostic connection in action space
- **Primitive** (new object: Γ defined on actions and proprioception, reusable across policy versions and robots of one model).
- **Mechanism:** An action-space connection is a property of the body, not of a policy. Fit it once per robot model; any policy, including a new VLA version, uses it. Its curvature is then a hardware property that can be shared across a fleet.
- **Nearest prior / gap:** [PEA](https://arxiv.org/abs/2611.28308) calibrates per policy per shift; [TeAR](https://arxiv.org/abs/2609.36182) is policy-specific.
- **Cheapest first test:** Two different policies on the same arm. **Kill** if an action-space Γ fit with policy 1 loses > 20% of its benefit on policy 2.
- **Old-skill retention:** Both policies' skills after drift.
- **Risk / likely tie:** Action-space Γ cannot represent strategy changes (ED21).

### ED21 · Where must Γ live? Action space versus weight space
- **Primitive** (new criterion: curvature that an action-space connection cannot absorb is exactly the strategy-level curvature).
- **Mechanism:** Fit Γ in action space first; the remaining function-space holonomy is strategy curvature that requires weight-space (or skill-fork) changes.
- **Nearest prior / gap:** None separates the two.
- **Cheapest first test:** ED03 gait boundary. **Kill** if action-space Γ removes the boundary holonomy (then strategy curvature is not real).
- **Old-skill retention:** Both gaits.
- **Risk / likely tie:** Hard to separate in practice.

## D · Strongest prior art, head-on

### ED22 · Gauge-equivariant skill heads given a learned Γ
- **Primitive** (new operation: build skill networks equivariant under the holonomy group of the learned connection).
- **Mechanism:** [Gauge-equivariant CNNs](https://arxiv.org/abs/1902.04615) assume a known connection. Here, estimate the holonomy group of Γ from loops (ED08) and constrain skill heads to be equivariant under it, so body change acts on skills by a known transformation.
- **Cheapest first test:** Ant flat family. **Kill** if equivariant heads do not beat EB11 null-space skills on transfer to unseen bodies.
- **Old-skill retention:** All skills on unseen bodies.
- **Risk / likely tie:** The holonomy group may be too large to constrain anything.

### ED23 · Transported Fishr
- **Primitive** (new operation: match gradient variances across bodies *after* transport).
- **Mechanism:** [Fishr](https://arxiv.org/abs/2109.02934) and [gradient matching](https://arxiv.org/abs/2104.09937) seek invariance across environments directly. Applying them after Γ-transport asks for invariance only of gauge-invariant content; in curved regions, mismatch is permitted in proportion to \(F\).
- **Cheapest first test:** Curved Pusher family. Arms: Fishr, gradient matching, EC12 gradient invariance, transported Fishr. **Kill** if transported Fishr does not beat Fishr on held-out bodies in the curved family.
- **Old-skill retention:** Per-skill under wear.
- **Risk / likely tie:** Fishr may already be strong in the flat family.

### ED24 · RMA's latent as a chart for Γ
- **Primitive** (new use: define Γ in RMA latent coordinates so RMA becomes a component and curvature a diagnostic of its latent).
- **Mechanism:** Use RMA's encoder to coordinatize bodies; learn Γ over \(z\); measure curvature in \(z\). High curvature where RMA's latent is folded flags extrapolation failures.
- **Nearest prior / gap:** [RMA](https://arxiv.org/abs/2107.04034) uses \(z\) as input only.
- **Cheapest first test:** Ant with RMA trained on half the body grid. **Kill** if curvature in \(z\) does not predict RMA's out-of-range errors at ρ ≥ 0.5.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** Becomes a diagnostic if it wins.

### ED25 · Order-swap test against PEA
- **Test.**
- **Mechanism:** PEA re-calibrates at each body and has no path memory. Visit gain, stiffness and payload shifts in two orders with a skill learned mid-sequence; Γ transports it, PEA cannot.
- **Cheapest first test:** LIBERO-Spatial, 3 shifts, 2 orders, one new task learned at the second shift. **Kill** if Γ does not beat PEA on the new task at the other shifts, or if order has no effect.
- **Old-skill retention:** Original tasks after both orders.
- **Risk / likely tie:** PEA's shifts may be flat (ED06 checks).

### ED26 · Curvature predicts domain-randomization regret
- **Test.**
- **Mechanism:** [Domain randomization](https://arxiv.org/abs/1703.06907) averages strategies; regret against per-body policies should be largest in high-\(F\) regions.
- **Cheapest first test:** Ant grid with DR policy and per-cell oracles. **Kill** if per-cell DR regret does not correlate with \(F\) at ρ ≥ 0.5.
- **Old-skill retention:** Not a write.
- **Risk / likely tie:** Regret may track coverage instead; control by coverage.

## Ranked deeper questions

1. **Does the manipulator-equation table predict measured curvature?** (ED01, ED05, ED08) Gains flat, Froude scaling flat, mass/length/payload curved, saturation and gait boundaries curved. This is the review's EC26 gate turned into a pre-registered prediction; it runs first. If it fails, Γ collapses to EB12.
2. **Is the curvature real in function space and on realistic actuators?** (ED07, ED09) Rules out optimizer and parametrization artifacts and synthetic-drift artifacts.
3. **Does Γ beat the fairest RMA on skills learned after a body change?** (ED10, ED14) This is where a connection does what a conditioned policy cannot. If RMA ties, Γ survives only as a diagnostic (ED11, ED24, ED26).
4. **Does the curvature-licensed fork reach the Pareto front on held-out combinations?** (ED15) This is the review's other 3, given a noise band and a physics prior.
5. **Is the action-space connection a hardware property?** (ED20, ED21) If Γ fit once per robot model serves any policy, it is a reusable artifact, and its residual curvature is exactly where skills must change strategy.
