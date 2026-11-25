# Embodied learners, depth 1: undoing body adaptations and routing updates by the body probe

Depth-1 node under [tree/root-embodied-learners.md](root-embodied-learners.md) ([PR #395](https://github.com/manojbajaj95/cl/pull/395)) · 28 candidate primitives (EB01–EB28) · 5 ranked deeper questions · Ideas only; no experiments run

**What the review kept (score 3, no 4).** From the [PR #395 triage row](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md):
- **(a) Undo a body adaptation when the body returns** (EL02 + EL03). Each adaptation is a named delta keyed by a body fingerprint from a fixed, object-free calibration motion (the "ritual") and is removed when the fingerprint returns to an earlier body, so repair causes no repair shock. Controls: no rollback, continued fine-tuning, RMA/online system identification, policies conditioned on measured body parameters, adapters keyed by the true body version, performance after repeated wear/repair cycles, retention of other skills.
- **(b) Route each update into body and skill channels by the ritual** (EL27). Project each update onto the directions that change the ritual's predicted sensor trace; that part goes to a shared body channel and the rest to the skill. Controls: no routing, EL04 blame routing, an RMA body latent, PCGrad, GPM, transfer of body corrections to untrained skills, per-skill retention under wear.

**Why both stall at 3.** (a) as stated is bookkeeping: an adapter keyed by the true body version already does the same lookup, and the fingerprint only replaces the oracle key. (b) is a gradient projection with a new basis; GPM and OGD already project, and an RMA latent already gives a shared body module. To reach a 4, a card must add an **object or operation the two ideas do not have**: something that is true of bodies (they return, they form cycles, they can be probed without touching anything, they can be deliberately perturbed in software) and that no task-keyed or parameter-keyed method can use.

**Push directions.** (1) *Loops, not keys:* a body that goes A→B→A defines a closed loop, and what survives the loop is skill, not compensation (EB01, EB06, EB19). (2) *Undo by construction, not by storage:* make deltas detachable or invertible when they are written (EB02, EB03, EB05). (3) *Invariance makes old data valid:* if the skill channel cannot see body drift, old replay never goes stale (EB22, EB23). (4) *The probe is designed, not fixed:* choose the ritual for the policy's own sensitivities (EB14, EB15, EB24).

**Shared controls for every card.** The reviewer's controls above, plus [task-vector negation](https://arxiv.org/abs/2212.04089) as the generic "remove a delta" baseline, which an audit on VLA policies finds suppresses the target skill reliably but with fragile locality ([Suppression sticks, locality is fragile](https://arxiv.org/abs/2608.04692)). Also [PEA](https://arxiv.org/abs/2611.28308), which probes actuation shifts invisible to a visuomotor policy and calibrates at test time with the base frozen (it restores most LIBERO-Spatial success under gain, stiffness and payload shifts), and plain ER at equal budget. Ledger rules from the root still hold: uniform-rehearsal controls ([PR #119](https://github.com/manojbajaj95/cl/pull/119)), split-half reliability of rollout truth (G1), ≥ 10 seeds, named bridge assumptions ([PR #126](https://github.com/manojbajaj95/cl/pull/126)). Testbeds are the root's CPU MuJoCo bodies with XML edits, then LIBERO with PEA's actuation shifts.

## Literature check

alphaXiv searches on excitation-trajectory design, task-vector negation and unlearning, per-actuator fault adaptation, fleet sharing of adaptation, inverse-dynamics action transfer, path dependence of fine-tuning, null-space-preserving fine-tuning, disentangling dynamics from task in meta-RL, reversible adapters, hypernetworks from context to policy weights, and plasticity under repeated dynamics change. Each card names its nearest prior; "gap" is a hypothesis to check against full text before a pilot.

| Line | Nearest prior | What is missing for (a) or (b) |
|---|---|---|
| Removing a learned delta | [Task arithmetic](https://arxiv.org/abs/2212.04089), [VLA task-vector negation audit](https://arxiv.org/abs/2608.04692), [Unmerge](https://arxiv.org/abs/2609.38895), [weight disentanglement](https://arxiv.org/abs/2604.17078), [Reversible LoRA editing](https://arxiv.org/abs/2603.11239), [Reversible behavioral learning](https://arxiv.org/abs/2603.02934) | Deltas are removed by a label (task or edit id). None uses a physical cycle to decide which part of a delta to remove, or trains a delta to be removable. |
| Body probes and excitation | [IDTD](https://arxiv.org/abs/2610.10905) (Fisher/Schur-complement trajectory design that exposes each physical parameter on its own interval), [Contact-aware Fisher behavior synthesis](https://arxiv.org/abs/2505.12214), [Active embodiment identification](https://arxiv.org/abs/2605.08020), [PEA](https://arxiv.org/abs/2611.28308), [Self-simulation](https://arxiv.org/abs/2311.12151) | Probes identify physical parameters. None is designed for, or grown with, the policy's own skill sensitivities, or used as a gradient basis. |
| Body vs task factorization | [RMA](https://arxiv.org/abs/2107.04034), [Meta-RL adaptation](https://arxiv.org/abs/1803.11347), [Disentangled multi-context meta-learning](https://arxiv.org/abs/2509.01297), [Latent dynamics geometries](https://arxiv.org/abs/2606.02280), [Deep inverse dynamics transfer](https://arxiv.org/abs/1610.03518), [Learning to undo](https://arxiv.org/abs/2611.23081) (learned undo map on the state space), [Residual policy learning](https://arxiv.org/abs/1812.06298) | Factorization is trained jointly from a body distribution. None is driven online by a probe whose span is the body channel, or keeps the skill channel provably blind to the body. |
| Projection methods | [GPM](https://arxiv.org/abs/2103.09762), [OGD](https://arxiv.org/abs/1910.07104), [PCGrad](https://arxiv.org/abs/2001.06782), [Null-basis LoRA](https://arxiv.org/abs/2609.25618), [PhysGuard](https://arxiv.org/abs/2606.16602) | Bases come from old-task activations or gradients. A basis from a physical probe that is re-measured on every body is new. |
| Actuator faults and plasticity | [TeAR](https://arxiv.org/abs/2609.36182), [Residual fault adaptation](https://arxiv.org/abs/2609.17404), [CAPABLE](https://arxiv.org/abs/2610.11971), [Joint-health-aware RL](https://arxiv.org/abs/2610.41348), [DRAP](https://arxiv.org/abs/2611.05029) (plasticity set by dynamics risk), [Replay under dynamics shift](https://arxiv.org/abs/2609.18167), [CAWM](https://arxiv.org/abs/2609.18950) | All adapt forward. None measures behavior after repair or over repeated wear/repair cycles. |
| Fleet sharing | [Robot fleet learning via policy merging](https://arxiv.org/abs/2310.01362), [Collective experience across 96 robots](https://arxiv.org/abs/2610.25736) | Whole policies or experience are merged; body-specific corrections are not separated out and shared by body diff. |

---

## A · Return as an algebraic event (pushing (a))

### EB01 · Body holonomy: skill is what survives a closed body loop
- **Primitive** (new object: the net weight change around a closed loop in body space).
- **Mechanism:** When the body goes A→B→A (wear then repair, tool on then off), compensation should cancel and skill learning should not. Record weights at each ritual-detected body change; the loop residual \(\Delta_{\circ} = \theta_{A'} - \theta_{A}\) after return is the holonomy. Decompose every in-loop delta into the part that the loop cancels (body) and the part that persists in \(\Delta_\circ\) (skill), by regressing in-loop deltas on the ritual-trace change. Rollback removes only the cancelling part. With several loops, the body and skill subspaces are fitted from loop statistics, without labels.
- **Nearest prior / gap:** Path dependence of fine-tuning is studied ([learning dynamics of CL](https://arxiv.org/abs/2609.33620)); task-vector negation removes whole deltas. A cycle in the *world* as the label for what to keep is new.
- **Cheapest first test:** Hopper, ankle gear 50% for 300 episodes during which a new hop-forward skill is learned, then repair. Arms: no rollback, continued FT, adapter keyed by true body version, EL02 full rollback, holonomy rollback. **Kill** if holonomy rollback does not beat full rollback on retaining the in-fault skill *and* match keyed adapters on pre-fault skills, over 10 seeds.
- **Old-skill retention:** Pre-fault skills and in-fault skill after repair, and after 5 wear/repair cycles.
- **Risk / likely tie:** With one loop the decomposition is underdetermined; it may need ≥ 3 loops, which is the repeated-cycle control.

### EB02 · Pre-registered inverse
- **Primitive** (new object: an inverse delta trained at write time, before the body returns).
- **Mechanism:** At each body change, the stored ritual trace of the *old* body is a free target. While adapting to the new body, also train an inverse delta \(\delta^{-1}\) such that \(\theta+\delta+\delta^{-1}\) reproduces the old body's ritual predictions and stored pre-change skill outputs. Undo is then available even after the forward delta has been merged or further trained.
- **Nearest prior / gap:** [Learning to undo](https://arxiv.org/abs/2611.23081) learns a state-space undo map between MDPs; reversible editing keeps the edit separate. An inverse trained in advance, so that undo survives merging, is not in either.
- **Cheapest first test:** As EB01, but merge the delta into the base every 50 episodes (ResMerge-style). **Kill** if \(\delta^{-1}\) does not recover ≥ 80% of pre-fault return in the first 10 post-repair episodes, or task-vector negation of the merged delta does as well.
- **Old-skill retention:** All pre-fault skills after repair; in-fault skill after applying \(\delta^{-1}\).
- **Risk / likely tie:** The inverse goes stale as training continues; refresh cost must be counted.

### EB03 · Restore by re-identification
- **Primitive** (new operation: undo an adaptation by optimizing the policy until it reproduces the stored ritual predictions of the returned body).
- **Mechanism:** Keep no deltas at all. Each body version stores only its ritual trace and the policy's predicted trace on it. On return, a short optimization over a small set of parameters (e.g. the body channel of (b)) matches the stored predicted trace; skills follow because the ritual covers their actuators (bridge assumption). Storage is one trace per body instead of one delta per body.
- **Nearest prior / gap:** [PEA](https://arxiv.org/abs/2611.28308) calibrates at test time from probes to the *current* body; IDTD identifies physical parameters. Restoring a *past* policy state from a stored probe target is new.
- **Cheapest first test:** Ant, 4 body versions visited in a cycle twice. Arms: keyed adapters (oracle), EL02 deltas, PEA-style probe calibration toward the current body, re-identification to the stored trace. **Kill** if re-identification needs > 2× the real episodes of keyed adapters to recover pre-change return, or ties PEA-style calibration (then the stored target adds nothing).
- **Old-skill retention:** All skills on every revisited body.
- **Risk / likely tie:** Ritual coverage of skill-relevant directions is the whole bet; EB14 addresses it.

### EB04 · Actuator-factored deltas and partial rollback
- **Primitive** (new object: a delta factored by the ritual interval that exposes each actuator).
- **Mechanism:** Use an IDTD-style ritual whose intervals each expose one actuator group. Fit each delta as a sum of factors, each tied to the ritual interval whose trace it changes. A repair that replaces one motor but leaves a worn gearbox pops only that motor's factor.
- **Nearest prior / gap:** [IDTD](https://arxiv.org/abs/2610.10905) decouples parameters for identification; [Joint-health-aware RL](https://arxiv.org/abs/2610.41348) conditions on per-joint health. Per-actuator undo of a learned delta is new.
- **Cheapest first test:** Ant with two independent faults (one gear, one damping), repair only one. **Kill** if factored rollback does not beat both full rollback and no rollback on post-partial-repair return.
- **Old-skill retention:** Return on all skills after each partial repair.
- **Risk / likely tie:** Faults interact through contacts; factors may not separate.

### EB05 · Detachability as a training constraint
- **Primitive** (new operation: train each adaptation so that removing it restores the old body's behavior exactly).
- **Mechanism:** Add a loss during adaptation: with the delta removed, the policy must still match its pre-change outputs on the old ritual and old skill states. The delta is thereby kept out of directions that change old-body behavior, so undo is exact by construction, not hoped for.
- **Nearest prior / gap:** The VLA negation audit finds suppression works but locality is fragile ([2608.04692](https://arxiv.org/abs/2608.04692)); weight-disentanglement work ([2604.17078](https://arxiv.org/abs/2604.17078), [KFAC disentanglement](https://arxiv.org/abs/2602.17385)) enforces it between tasks. Detachability defined against a physical old body is new.
- **Cheapest first test:** EB01 setting. **Kill** if the constraint does not cut post-repair return loss by ≥ 50% versus an unconstrained delta at ≤ 10% cost on in-fault return.
- **Old-skill retention:** Pre-fault skills after removal; locality on unrelated skills (the audit's failure).
- **Risk / likely tie:** Equivalent to EWC around the old body if the constraint is quadratic; the EWC arm checks this.

### EB06 · Commutator of body deltas
- **Primitive** (new object: the commutator of two body adaptations, as a test of entanglement and a stored correction).
- **Mechanism:** For two body changes X and Y, adapt in orders XY and YX in a sim branch; the difference \([\delta_X,\delta_Y]\) says whether the adaptations are independent. Commuting pairs can be stacked and popped in any order; non-commuting pairs get a stored correction term. This decides when per-change deltas (a) are valid at all.
- **Nearest prior / gap:** NP07 update conjugacy ([PR #389](https://github.com/manojbajaj95/cl/pull/389)) asks the same about tokenizer migrations; task-vector composability studies ([2609.39405](https://arxiv.org/abs/2609.39405)) measure task interference. Body-change commutators are new.
- **Cheapest first test:** 4 body changes on Reacher, all 6 pairs both orders. **Kill** if commutator norm does not predict pop-order error (Spearman ρ ≥ 0.6) over held-out pairs.
- **Old-skill retention:** Skills after popping in both orders.
- **Risk / likely tie:** May be an assay; it graduates only if the stored correction fixes non-commuting pops.

### EB07 · Body-delta manifold from wear history
- **Primitive** (new object: a curve in weight space, indexed by the ritual coordinate, fitted from the history of deltas).
- **Mechanism:** Over repeated wear cycles, deltas lie near a low-dimensional manifold. Fit it from stored deltas and ritual traces only; a new wear level is served by a point on the manifold (interpolation or extrapolation), and return is a move back along it.
- **Nearest prior / gap:** Context-conditioned and hypernetwork policies ([HypEMBER](https://arxiv.org/abs/2607.19628), [SHINE](https://arxiv.org/abs/2602.06358)) are trained from a designed body distribution. A manifold learned from the robot's own delta history, without a parameter label, is the difference.
- **Cheapest first test:** HalfCheetah with gear wear at 10 levels, 3 cycles. **Kill** if manifold extrapolation to an unseen level is not better than a measured-parameter-conditioned policy trained on the same levels.
- **Old-skill retention:** All skills at every past wear level.
- **Risk / likely tie:** The conditioned-policy control is strong when parameters are measurable.

### EB08 · Remount rollback for sensors
- **Primitive** (new operation: undo a perception adaptation when a sensor returns to an earlier mount).
- **Mechanism:** Add a self-observation segment to the ritual (look at the gripper at fixed poses). Camera moves change that segment's trace; perception deltas are keyed to it and popped on remount, separately from actuator deltas.
- **Nearest prior / gap:** [Continual hand–eye calibration](https://arxiv.org/abs/2604.15814) and [Blackout vs freeze](https://arxiv.org/abs/2609.39145) handle the current camera. Undoing on remount is new.
- **Cheapest first test:** LIBERO-RIG camera shifts in a cycle. **Kill** if remount rollback does not beat PEA-style calibration plus continued FT on the original camera.
- **Old-skill retention:** Success on the original mount after the cycle.
- **Risk / likely tie:** Pretrained encoders may absorb small shifts.

### EB09 · Diff-keyed delta transplant between sibling robots
- **Primitive** (new object: a body delta keyed by the ritual *difference* from factory, shareable across robots of one model).
- **Mechanism:** A worn-gripper delta learned on robot 1 is applied to robot 2 when robot 2's ritual diff from factory matches. The fleet keeps a library of diffs and deltas; skills stay per-robot.
- **Nearest prior / gap:** [Fleet policy merging](https://arxiv.org/abs/2310.01362) and [collective experience learning](https://arxiv.org/abs/2610.25736) share whole policies or data. Sharing only body corrections by diff is new, and is not the population root's forks of one learner.
- **Cheapest first test:** 4 Ant copies with different skill sets; one gets a fault, its delta is applied to another with the same fault. **Kill** if the transplanted delta does not beat RMA on the receiver's first 20 episodes, or damages the receiver's own skills.
- **Old-skill retention:** Receiver's unique skills after the transplant.
- **Risk / likely tie:** Deltas may not be robot-independent even for one model.

### EB10 · Ritual-coverage certificate for rollback
- **Primitive** (new object: a bound from ritual-trace match to skill-return match).
- **Mechanism:** Estimate, per skill, how ritual error bounds skill error (local Lipschitz from ritual to skill trajectories, via the policy's Jacobians). A rollback is certified when the ritual matches within the bound, so no task rollouts are needed after repair.
- **Nearest prior / gap:** Label-free forgetting detection ([PR #126](https://github.com/manojbajaj95/cl/pull/126)) needs a bridge assumption; this makes the bridge quantitative. No robot paper certifies restoration.
- **Cheapest first test:** EB03 setting. **Kill** if certified rollbacks fail (return < 90% of pre-change) more than 5% of the time.
- **Old-skill retention:** Is what it certifies.
- **Risk / likely tie:** The bound may be too loose to certify anything.

## B · The ritual as a gradient basis (pushing (b))

### EB11 · Two-sided ritual projection: skills that cannot see the body
- **Primitive** (new operation: skill updates are constrained to the ritual's null space, body updates to its span).
- **Mechanism:** Compute the ritual Jacobian \(J_r = \partial \hat r / \partial\theta\) (JVPs over the ritual's predicted trace). Body-channel updates are projected onto \(\mathrm{span}(J_r)\); skill updates onto its null space, so no skill can privately learn a body compensation. Re-measure \(J_r\) on every body change, so the basis follows the body instead of old tasks.
- **Nearest prior / gap:** [GPM](https://arxiv.org/abs/2103.09762) and [OGD](https://arxiv.org/abs/1910.07104) protect old-task subspaces; [Null-basis LoRA](https://arxiv.org/abs/2609.25618) preserves a capability's subspace. A basis from a physical probe, re-measured per body and applied two-sided, is new.
- **Cheapest first test:** Pusher, 4 skills, gear wear on 2 joints. Arms: no routing, EL04 blame routing, RMA latent, PCGrad, GPM, one-sided EL27, two-sided. **Kill** if two-sided does not give better zero-shot transfer of the wear correction to the 3 skills that never trained under wear than EL27 and RMA, over 10 seeds.
- **Old-skill retention:** Per-skill return under wear and on the factory body.
- **Risk / likely tie:** The null-space constraint may block legitimate skill learning that touches the same actuators.

### EB12 · The body channel as a shared action conjugator
- **Primitive** (new object: a learned operator \(g\) with \(a' = g(a, s)\) wrapped around every skill and trained only on ritual and free-motion data).
- **Mechanism:** Instead of a body sub-network inside the policy, the body channel is an action (and proprioception) conjugator applied outside all skills. It is trained so that conjugated ritual commands reproduce the factory body's ritual trace. Skills are written once in factory coordinates and never see drift. Rollback (a) is resetting \(g\) to a stored version.
- **Nearest prior / gap:** [Deep inverse dynamics transfer](https://arxiv.org/abs/1610.03518) maps sim actions to real with a model trained on task data; [Learning to undo](https://arxiv.org/abs/2611.23081) learns a state-space undo map; [TeAR](https://arxiv.org/abs/2609.36182) rectifies actions from telemetry. A conjugator trained only on the ritual, shared by all skills and versioned per body, is the difference.
- **Cheapest first test:** EB11 setting. **Kill** if the conjugator trained only on the ritual does not match a TeAR-style rectifier trained on task data, on skills never practiced under wear.
- **Old-skill retention:** All skills after wear, with \(g\) frozen during skill learning.
- **Risk / likely tie:** State-dependent drift (contacts) may not be expressible outside the policy.

### EB13 · Leak migration
- **Primitive** (new operation: move body compensation that leaked into skill weights back into the body channel).
- **Mechanism:** Per skill, measure the leak: the component of its accumulated delta inside \(\mathrm{span}(J_r)\). Periodically distill that component into the body channel (match outputs on the ritual and on the skill's states), then remove it from the skill. This is a consolidation operation that keeps the factorization clean after unconstrained online learning.
- **Nearest prior / gap:** Sleep-style consolidation ([Sleeping robots](https://arxiv.org/abs/2606.17493)) merges skills; no method moves a *body* component between modules.
- **Cheapest first test:** EB11 setting but with unconstrained updates plus migration every 50 episodes. **Kill** if migration does not reach two-sided projection's transfer to untrained skills.
- **Old-skill retention:** Skill return before and after each migration (it must not drop > 2%).
- **Risk / likely tie:** If EB11 works, migration is only a fallback.

### EB14 · Skill-aware ritual design
- **Primitive** (new operation: design the ritual so its Jacobian spans the directions in which the policy's skills are sensitive to body change).
- **Mechanism:** Estimate, from the skill set, the Fisher information of skill success with respect to body parameters (in sim branches). Optimize the ritual (bounded, object-free, safe) so that \(\mathrm{span}(J_r)\) covers the top eigen-directions. The probe is chosen for what the policy needs to know, not for physical identifiability.
- **Nearest prior / gap:** [IDTD](https://arxiv.org/abs/2610.10905) and [Contact-aware Fisher behavior synthesis](https://arxiv.org/abs/2505.12214) design excitation to identify physical parameters; [Active embodiment identification](https://arxiv.org/abs/2605.08020) learns an ID policy. Designing the probe against policy sensitivity is new.
- **Cheapest first test:** EB11 with three rituals: hand-designed, IDTD-style, skill-aware. **Kill** if skill-aware does not beat IDTD-style on transfer to untrained skills at equal ritual length.
- **Old-skill retention:** Same as EB11.
- **Risk / likely tie:** When skills use all actuators, the two designs may coincide.

### EB15 · Ritual growth with the skill set
- **Primitive** (new operation: append a ritual segment when a new skill's body-sensitive directions are not spanned).
- **Mechanism:** After each new skill, check the residual of its body-sensitivity directions outside \(\mathrm{span}(J_r)\). If it exceeds a threshold, synthesize a short segment (EB14) that covers it. Coverage of all skills by the probe becomes an invariant the learner maintains, and the cost is ritual seconds.
- **Nearest prior / gap:** No probe in the literature grows with the learner.
- **Cheapest first test:** 8 Meta-World skills streamed, ritual capped at 10 s. **Kill** if grown rituals do not reduce late-skill failure under wear versus a fixed ritual of the final length designed up front.
- **Old-skill retention:** All 8 skills under wear.
- **Risk / likely tie:** A long fixed ritual may be enough.

### EB16 · World ritual: a third channel from a calibration object
- **Primitive** (new object: a fixed object interaction whose trace spans the world channel).
- **Mechanism:** Add a second probe: push a fixed calibration object. Its Jacobian minus the body span defines a world channel (friction, surface). Updates split three ways: body (ritual span), world (object-probe span), skill (rest).
- **Nearest prior / gap:** EL04 blame routing uses separate models; [Latent dynamics geometries](https://arxiv.org/abs/2606.02280) learns a dynamics latent. Probe-defined world routing is new.
- **Cheapest first test:** EL04's joint body-plus-world event. **Kill** if three-way routing does not beat EL04 and EB11 on both untrained-skill transfer and isolation of the world write.
- **Old-skill retention:** Untouched skills after both events.
- **Risk / likely tie:** Calibration objects may not represent task objects.

### EB17 · Sensor ritual and a perception channel
- **Primitive** (new object: the self-observation segment's Jacobian as the perception channel).
- **Mechanism:** Looking at the robot's own gripper at fixed poses defines a perception span; camera moves are routed there and popped on remount (EB08). Actuation shifts, which do not change images ([PEA](https://arxiv.org/abs/2611.28308)), go to the body channel.
- **Nearest prior / gap:** PEA separates visual from actuation shifts for calibration; [UniLatent](https://arxiv.org/abs/2611.10061) aligns observations. Routing continual updates by the two probes is new.
- **Cheapest first test:** LIBERO with PEA's "camera + gains" combination. **Kill** if two-probe routing does not beat PEA plus continued FT on retention of the original setup.
- **Old-skill retention:** Original-setup success after the combined shift.
- **Risk / likely tie:** PEA alone may restore most of it.

### EB18 · Roll back only the body channel
- **Primitive** (new operation: the join of (a) and (b) — on repair, pop the body channel's delta and keep everything the skill channel learned meanwhile).
- **Mechanism:** With routing in place, a fault period produces a body-channel delta and skill-channel learning. On fingerprint return, pop only the body-channel delta. This removes the bookkeeping objection to (a): the key is not just a lookup, because the routing decides *what* the key controls.
- **Nearest prior / gap:** Keyed adapters (the reviewer's oracle control) pop everything learned under that key, including skill learning.
- **Cheapest first test:** EB01 setting. **Kill** if body-channel rollback does not keep ≥ 90% of in-fault skill learning after repair while matching keyed adapters on pre-fault skills.
- **Old-skill retention:** Pre-fault, in-fault and post-repair skills; 5 wear/repair cycles.
- **Risk / likely tie:** Equals EB01 if holonomy and the ritual define the same subspace (EB19 tests that).

### EB19 · Holonomy-defined body subspace as a check on the ritual
- **Primitive** (new operation: estimate the body subspace from loops alone and compare it to the ritual's span).
- **Mechanism:** From several A→B→A loops, the directions that cancel define a body subspace with no probe at all (EB01). The angle between it and \(\mathrm{span}(J_r)\) measures what the ritual misses; the union is the body channel.
- **Nearest prior / gap:** None found that defines a parameter subspace from physical cycles.
- **Cheapest first test:** 6 loops on Ant. **Kill** if the loop subspace is no better aligned with true body-parameter gradients (from sim) than a random subspace of equal dimension.
- **Old-skill retention:** EB18 using the union versus either subspace.
- **Risk / likely tie:** Needs loops, which real robots rarely see on demand (EB24).

### EB20 · Ritual-gated skill plasticity
- **Primitive** (new operation: when the ritual trace mismatches its prediction, freeze skill learning and let only the body channel learn).
- **Mechanism:** A ritual mismatch means the body moved. During mismatch, any task error is attributed to the body and skill learning rates go to zero until the body channel closes the gap. This prevents skills from rewriting themselves during the transient after a body change.
- **Nearest prior / gap:** [DRAP](https://arxiv.org/abs/2611.05029) sets plasticity by dynamics risk; [CAWM](https://arxiv.org/abs/2609.18950) flushes replay at changepoints. Gating by a body probe's prediction error, per channel, is new.
- **Cheapest first test:** EB11 with abrupt faults. **Kill** if gating does not reduce skill-channel drift during the transient by ≥ 50% versus DRAP-style plasticity at equal final return.
- **Old-skill retention:** Untouched skills through the transient.
- **Risk / likely tie:** Gradual wear gives no clear mismatch; then gating does nothing.

### EB21 · One skill channel, a body channel per robot
- **Primitive** (new operation: a new body receives only a body channel, initialized by aligning its ritual trace to existing bodies').
- **Mechanism:** Skills live in a shared channel in factory coordinates of a reference body. A new robot runs the ritual, its body channel is initialized by regressing from ritual-trace differences to existing body channels, then refined on the ritual only. No skill data is needed to bring old skills to the new body.
- **Nearest prior / gap:** [HPT](https://arxiv.org/abs/2409.20537) learns per-body stems from task data; [UniLatent](https://arxiv.org/abs/2611.10061) aligns observations; RMA infers extrinsics. A body channel obtained from the ritual alone is new.
- **Cheapest first test:** 4 unimals sequentially. **Kill** if ritual-only body channels do not reach 70% of HPT-style stem fine-tuning return with zero task episodes.
- **Old-skill retention:** Earlier bodies' return after new bodies are added.
- **Risk / likely tie:** Large morphology changes break the shared-coordinate assumption.

## C · Objects the two ideas imply

### EB22 · Replay that never goes stale
- **Primitive** (new property: if the skill channel is ritual-null, old skill data stays valid after any body change).
- **Mechanism:** Store replay in skill-channel coordinates (inputs and targets before the body conjugator, EB12). After a body change, only the body channel needs fresh data; the whole replay buffer stays usable, so no flushing or reweighting is needed.
- **Nearest prior / gap:** [Replay under dynamics shift](https://arxiv.org/abs/2609.18167) characterizes stale replay; [CAWM](https://arxiv.org/abs/2609.18950) flushes it; RIFAR reweights by reliability. Making staleness impossible by construction is new.
- **Cheapest first test:** Model-based RL on Ant with 4 body changes. Arms: keep all replay, CAWM flush, RIFAR-style weighting, skill-coordinate replay. **Kill** if skill-coordinate replay does not beat the best of the three on post-change return within 50 episodes.
- **Old-skill retention:** Old skills after each change.
- **Risk / likely tie:** Only as good as the factorization.

### EB23 · Counterfactual body replay
- **Primitive** (new operation: transport old trajectories to the current body through the body channel's inverse).
- **Mechanism:** For data that cannot be stored in skill coordinates (raw logs), apply \(g_{\text{new}}^{-1}\circ g_{\text{old}}\) to old actions to get what the current body should have done; replay those.
- **Nearest prior / gap:** EL01 age transport from the root; inverse-dynamics relabeling. Transport by the versioned conjugator is the new part.
- **Cheapest first test:** EB22 setting with raw logs. **Kill** if transported replay does not beat untransported replay on post-change return.
- **Old-skill retention:** Same.
- **Risk / likely tie:** Merge with EB22 if they tie.

### EB24 · Self-perturbation: generate body loops in software
- **Primitive** (new operation: the robot deliberately changes its own controller gains, limits or latency to create safe A→B→A loops).
- **Mechanism:** Real repairs are rare, but gain and latency changes are free and reversible. Run the ritual under software perturbations to measure \(J_r\) along known directions and to create loops for EB01 and EB19 on demand, without wear.
- **Nearest prior / gap:** Domain randomization perturbs in sim during training; PEA uses gain shifts as evaluation. Online software perturbation as a source of body loops is new.
- **Cheapest first test:** EB19 with loops from gain perturbations only, evaluated on a real (XML) fault. **Kill** if the perturbation-derived subspace does not beat a random one on EB18 retention under the real fault.
- **Old-skill retention:** Skills after perturbation sessions (they must not drift).
- **Risk / likely tie:** Software-reachable changes may not span mechanical wear.

### EB25 · Carry the body channel through policy upgrades
- **Primitive** (new operation: when the policy is distilled into a new architecture, transfer the body channel by ritual matching, separately from skills).
- **Mechanism:** [Policy distillation](https://arxiv.org/abs/1511.06295) on task data averages body knowledge into the student. Instead, distill skills in factory coordinates and fit the student's body channel to reproduce the teacher's ritual predictions, so years of wear history survive a model swap.
- **Nearest prior / gap:** Policy distillation and VLA upgrades re-learn body specifics from task data.
- **Cheapest first test:** Teacher MLP adapted through 3 body versions → student of a different width. **Kill** if the separated transfer does not beat plain distillation on worn-body return of skills with little data.
- **Old-skill retention:** Student's return on all skills and body versions.
- **Risk / likely tie:** Plain distillation may already carry it if task data covers the body.

### EB26 · Safety constraints written in body-channel coordinates
- **Primitive** (new operation: store safe sets and intervention constraints in factory coordinates so that body change does not move them).
- **Mechanism:** Constraints learned from interventions (root EL19) are expressed before the conjugator; the conjugator carries them to the current body, and rollback restores them with the body.
- **Nearest prior / gap:** [SafeAdapt](https://arxiv.org/abs/2604.09452) and [Safe CRL](https://arxiv.org/abs/2605.18842) are single-body; root EL20 transports sets heuristically.
- **Cheapest first test:** 2-link arm with link-mass changes and 10 constraints. **Kill** if violation rate after body change is not lower than re-learning constraints in raw coordinates.
- **Old-skill retention:** Violation rate and task return on returned bodies.
- **Risk / likely tie:** Constraints in task space may already be body-invariant.

### EB27 · Ritual from task fragments
- **Primitive** (new object: a ritual assembled from repeated fixed segments of ordinary tasks, for robots with no idle time).
- **Mechanism:** Homing motions, approach phases and grasp-preshapes recur across tasks. Select segments whose commands repeat closely and whose Jacobians span the skill sensitivities (EB14) and use them as an implicit ritual.
- **Nearest prior / gap:** The root's EL03 kill arm already compares a dedicated ritual to task-rollout fingerprints; this makes the task-derived version a designed object.
- **Cheapest first test:** EB11 with the dedicated ritual replaced by mined fragments. **Kill** if fragments lose > 20% of the dedicated ritual's untrained-skill transfer.
- **Old-skill retention:** Same as EB11.
- **Risk / likely tie:** Fragments may vary too much in context.

### EB28 · How many ritual dimensions does a skill set need?
- **Assay** (not a primitive).
- **Mechanism:** Measure the rank of the skill set's body-sensitivity Fisher across body families and skill counts; predicts ritual length for EB14/EB15.
- **Nearest prior / gap:** None found for policies; IDTD reports per-parameter identifiability.
- **Cheapest first test:** Rank over 4–16 Meta-World skills on 3 arms. **Kill** if rank grows linearly with skill count (then the shared body channel buys nothing).
- **Old-skill retention:** Not applicable; it gates EB11–EB15.
- **Risk / likely tie:** Assay.

## Ranked deeper questions

1. **Does a closed body loop separate skill from compensation?** (EB01, EB19, EB24) If the loop residual identifies what to keep, rollback no longer needs an oracle key, which answers the bookkeeping objection. First test: EB01 on Hopper with ≥ 3 loops from EB24's software perturbations.
2. **Does popping only the body channel keep in-fault skill learning?** (EB18) This is the joint form of the two kept directions and the most direct beat of keyed adapters. First test: EB18 against keyed adapters and full rollback.
3. **Can skills be made blind to the body without losing skill?** (EB11, EB12, EB22) If yes, replay never goes stale and the rest of this node follows. First test: EB11 two-sided projection versus RMA, GPM and PCGrad on untrained-skill transfer.
4. **Is a probe designed for policy sensitivity better than one designed for physics?** (EB14, EB15) First test: EB14 against IDTD-style excitation.
5. **Does any of it survive VLAs under actuation shifts?** (EB17, EB03) PEA restores most success with a frozen base; the question is whether stored-probe restoration and channel routing add retention across repeated shifts. First test: EB17 on LIBERO with PEA's shifts.
