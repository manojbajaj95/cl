# Root: Embodied continual learners (robots whose bodies, sensors and worlds drift)

Root node (depth 0) · 32 candidate primitives (EL01–EL32) · 5 ranked deeper questions · Ideas only; no experiments run

**Thesis.** Every other root in this tree treats the learner's *interface* to the world as fixed: tokens in, tokens out. A robot's interface is a physical body that wears, heats up, gets repaired, has sensors swapped and is replaced by a successor body, while the world it touches drifts too. This makes three things true for robots that are not true for language learners. (1) Some drops in old-skill performance are *correct revisions* (the body changed) and some are damage, and the learner has a cheap physical way to tell them apart: it can move without touching anything. (2) Old bodies come back (a worn motor is replaced, a tool is detached, a camera is remounted), so "retention" includes returning to a past body, not only to past tasks. (3) Practice costs wear, time and safety, and some events cannot be re-experienced at all, so what is worth remembering depends on what it costs to relearn. Current lifelong-robot-learning work ([LIBERO](https://arxiv.org/abs/2306.03310), [LOTUS](https://arxiv.org/abs/2311.02058), [TAIL](https://arxiv.org/abs/2310.05905), [Memory Anchors](https://arxiv.org/abs/2608.26545), [Sleeping Robots](https://arxiv.org/abs/2606.17493), [CPC](https://arxiv.org/abs/2601.22475)) holds the body fixed and streams *tasks*; embodiment-transfer work ([RT-X](https://arxiv.org/abs/2310.08864), [Octo](https://arxiv.org/abs/2405.12213), [CrossFormer](https://arxiv.org/abs/2408.11812), [HPT](https://arxiv.org/abs/2409.20537), [OmniAct](https://arxiv.org/abs/2611.33158)) trains on many bodies at once and never asks what happens to body A when body N arrives; adaptation work ([RMA](https://arxiv.org/abs/2107.04034), [TeAR](https://arxiv.org/abs/2609.36182), [CAPABLE](https://arxiv.org/abs/2610.11971), [Rapid Embodiment Adaptation](https://arxiv.org/abs/2608.01506)) adapts to the current body and forgets the question of the next one. The cards below look for new objects and operations that treat *the body itself* as a versioned, diffable, partly reversible part of the learner's state.

**Scope.** Read before writing: the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). Orthogonal to the explored roots: learner–world co-evolution ([PR #363](https://github.com/manojbajaj95/cl/pull/363), where the learner's *outputs* reshape users and tools; here the world and the body drift on their own), test-time learners ([PR #373](https://github.com/manojbajaj95/cl/pull/373), weight updates during inference; here adaptation is cheap and the question is what it does to stored skills), population learners ([PR #379](https://github.com/manojbajaj95/cl/pull/379), many forks of one learner; here one learner has many *bodies* over time), open-ended learners ([PR #384](https://github.com/manojbajaj95/cl/pull/384), a learner that invents its tasks; here tasks may be fixed and the body is what changes) and never-ending pretraining ([PR #389](https://github.com/manojbajaj95/cl/pull/389), data and tokenizer drift; here sensor and actuator drift). Ledger results this root must respect:
- **LP self-curricula lose to uniform** ([PR #119](https://github.com/manojbajaj95/cl/pull/119)): every card that schedules rehearsal (EL16, EL18, EL28) must beat uniform rehearsal at equal robot time, not only an LP selector.
- **Noisy rollout truth** (G1, [PR #7](https://github.com/manojbajaj95/cl/pull/7)): any card whose ground truth is a rollout success rate reports split-half reliability of that truth first; robot success rates at n < 50 are often too noisy to rank anything.
- **Anomaly replication** (Q1 and P1, mined from [PR #12](https://github.com/manojbajaj95/cl/pull/12) and [PR #11](https://github.com/manojbajaj95/cl/pull/11)): no card is mined from one-seed robot surprises; effects must hold at ≥ 10 seeds before a mechanism is built on them.
- **Label-free forgetting detection needs a bridge assumption** ([PR #126](https://github.com/manojbajaj95/cl/pull/126)): EL03 and EL22 name theirs (the body's own kinematics; shared object effects).
- **Update conjugacy across a migration** (NP07, [PR #389](https://github.com/manojbajaj95/cl/pull/389)) and **push/pop frames** (TT02, [PR #373](https://github.com/manojbajaj95/cl/pull/373)) are rowed for tokenizers and test-time updates; EL26 and EL27 say what a physical attach/detach event or a calibration ritual adds.

**Shared conventions.** "Cheap" means CPU MuJoCo (Gymnasium Ant/HalfCheetah/Hopper/Reacher/Pusher with XML edits to gear, damping, mass, joint range and sensor noise), dm_control, [Continual World](https://arxiv.org/abs/2105.10919)/Meta-World, MetaMorph unimals and [GaugeBench](https://arxiv.org/abs/2610.07597) re-descriptions; GPU stages use LIBERO and [LIBERO-RIG](https://arxiv.org/abs/2610.18843) with a small VLA. Every first test reports old-skill success on the **original, undamaged body** as well as the current one, because the factory body can return after repair.

## Literature check

alphaXiv searches across lifelong robot learning and LIBERO, continual imitation and VLA forgetting, continual RL and world models under dynamics shift, cross-embodiment and morphology-aware policies, actuator degradation and damage recovery, sim-to-real and real-to-sim loops, sensor faults and cross-sensor tactile transfer, safe continual RL and shielding, reset-free practice cost, body schema and tool use, and motion retargeting; titles and abstracts read for the closest matches. Each card names its nearest prior art; a "gap" is a hypothesis to verify against full text before any pilot, not a priority claim.

| Line | Already available | What a new primitive here must add |
|---|---|---|
| Lifelong robot learning (task streams on one body) | [LIBERO](https://arxiv.org/abs/2306.03310), [LOTUS](https://arxiv.org/abs/2311.02058), [TAIL](https://arxiv.org/abs/2310.05905), [Memory Anchors](https://arxiv.org/abs/2608.26545) (rehearse where new and old observations collapse with conflicting actions), [Sleeping Robots](https://arxiv.org/abs/2606.17493) (wake–sleep consolidation, skill-coupling collapse), [CPC](https://arxiv.org/abs/2601.22475), [SARAM](https://arxiv.org/abs/2610.24804), [ResMerge](https://arxiv.org/abs/2610.41663), [REGEN](https://arxiv.org/abs/2606.27374) and [RIFAR](https://arxiv.org/abs/2610.03079) (world-action-model replay), [VLAs resist forgetting](https://arxiv.org/abs/2603.03818) (ER nearly zero forgetting), [Near-zero forgetting is not enough](https://arxiv.org/abs/2611.31511) | The body is constant in all of these. A primitive must make *body change* a first-class event the memory responds to, and must beat plain ER, which is already near zero forgetting on pretrained VLAs. |
| Continual RL and world models | [Continual World](https://arxiv.org/abs/2105.10919), [Policy Distillation](https://arxiv.org/abs/1511.06295), [Stability gap in CRL](https://arxiv.org/abs/2611.26252), [The world model remembers, the actor forgets](https://arxiv.org/abs/2607.19749), [CAWM](https://arxiv.org/abs/2609.18950) (CUSUM changepoint, flush stale replay), [What should world models forget?](https://arxiv.org/abs/2610.03713) (retention stratified by invariance timescale), [Replay retention under dynamics shift](https://arxiv.org/abs/2609.18167) | Changepoint detection and stale-replay flushing exist; stratification is argued. Missing: deciding *which* stored item a dynamics shift invalidates, and keeping the pre-shift version for when the body returns. |
| Embodiment transfer | [RT-X](https://arxiv.org/abs/2310.08864), [Octo](https://arxiv.org/abs/2405.12213), [CrossFormer](https://arxiv.org/abs/2408.11812), [HPT](https://arxiv.org/abs/2409.20537), [MetaMorph](https://arxiv.org/abs/2203.11931), [OmniAct](https://arxiv.org/abs/2611.33158), [REvolveR](https://arxiv.org/abs/2202.05244) (interpolated robots for transfer), [KITE](https://arxiv.org/abs/2606.22113), [Cross-controller transfer](https://arxiv.org/abs/2610.39280), [The embodiment gap](https://arxiv.org/abs/2608.18433), [GaugeBench](https://arxiv.org/abs/2610.07597) (MetaMorph drops from 4030.6 to 51.6 when the same robots are re-described) | Joint multi-body training and one-shot transfer. Nobody measures what happens to old bodies when bodies arrive *sequentially*, or stores skills so that re-description and body change act as transformations rather than overwrites. |
| Wear, damage and fault adaptation | [Robots that adapt like animals](https://arxiv.org/abs/1407.3501) (IT&E repertoires), [Hierarchical QD damage recovery](https://arxiv.org/abs/2204.05726), [RMA](https://arxiv.org/abs/2107.04034), [TeAR](https://arxiv.org/abs/2609.36182) (telemetry-conditioned action rectification), [CAPABLE](https://arxiv.org/abs/2610.11971), [Rapid Embodiment Adaptation](https://arxiv.org/abs/2608.01506), [Joint-health-aware RL](https://arxiv.org/abs/2610.41348), [Reset-free recovery after leg damage](https://arxiv.org/abs/2610.20838), [Active embodiment identification](https://arxiv.org/abs/2605.08020), [Teaching robots to build simulations of themselves](https://arxiv.org/abs/2311.12151) | All adapt to the *current* body. None treats repair (return to an old body) as a retention event, wear as an irreversible clock that indexes memory, or the self-model probe as an index of which skills broke. |
| Sim-to-real loops | [Domain randomization](https://arxiv.org/abs/1703.06907), [RealSimLoop](https://arxiv.org/abs/2609.09828), [Online sim-to-real via closed-loop modeling](https://arxiv.org/abs/2609.28878), [Neural fidelity calibration](https://arxiv.org/abs/2611.28274), [Frozen in Time](https://arxiv.org/abs/2610.40857) (sim fine-tuning then real adaptation erodes both), [PhysGuard](https://arxiv.org/abs/2606.16602) (Fisher projection for sim-to-real surrogates) | Sim and real are treated as a source and a target. A primitive must treat them as two coupled memories with a per-region fidelity map that decides where real data may write. |
| Sensors | [Targeted modality dropout](https://arxiv.org/abs/2610.09566), [Online sensor diagnosis and repair](https://arxiv.org/abs/2610.36852), [Blackout vs freeze](https://arxiv.org/abs/2609.39145), [Evidence-gated regularization](https://arxiv.org/abs/2609.03142), [TaF-Foundation](https://arxiv.org/abs/2611.20718) and [BIDETA](https://arxiv.org/abs/2609.08673) (cross-sensor tactile), [UniLatent](https://arxiv.org/abs/2611.10061), [Continual hand–eye calibration](https://arxiv.org/abs/2604.15814), [Drift compensation for a soft sensorized finger](https://arxiv.org/abs/2503.16540) | Robustness to a missing or new sensor at one moment. Missing: sequences of swaps (sensor generations), the overlap window when old and new sensors are both mounted, and per-skill sensor dependency as a retention index. |
| Safe online learning and practice cost | [Shielding](https://arxiv.org/abs/1708.08611), [SafeAdapt](https://arxiv.org/abs/2604.09452) (Rashomon-set projection for safe continual updates), [Safe CRL with adaptive constraints](https://arxiv.org/abs/2605.18842), [SEVI](https://arxiv.org/abs/2610.31829), [HG-DAgger](https://arxiv.org/abs/1810.02890), [Intervention-aware world models](https://arxiv.org/abs/2609.06009), [REVERSAL-BENCH](https://arxiv.org/abs/2609.17745) (the reset-free reversibility cliff), [Practice is not free](https://arxiv.org/abs/2611.19979) (cost-aware practice scheduling), [Removing one user's corrections](https://arxiv.org/abs/2611.10280) | Safe sets are certified for one body and one data distribution; practice cost is used to pick the next task. Missing: retention priority set by the cost of *relearning*, safe-set transport across body change, and interventions stored as persistent constraints. |

---

## A · The body as a versioned object (wear, repair, hardware change)

### EL01 · Wear clock: a monotone body-age coordinate that indexes every write
- **Primitive** (new object: an irreversible time axis for the body, separate from task time).
- **Mechanism:** Fit a one-dimensional latent \(a_t\) from proprioceptive telemetry (tracking error, current per torque, backlash) under a monotonicity constraint: wear only increases between repairs. Every replay item, adapter and residual is stamped with the \(a\) at which it was written. Retrieval and rehearsal are conditioned on the *current* \(a\): items written at a younger age are replayed through a learned age-transport map \(T_{a\to a'}\) instead of verbatim, so old data teaches the right action for today's body instead of yesterday's.
- **Nearest prior / gap:** [RMA](https://arxiv.org/abs/2107.04034) and [Rapid Embodiment Adaptation](https://arxiv.org/abs/2608.01506) infer a free extrinsics vector with no ordering; [Joint-health-aware RL](https://arxiv.org/abs/2610.41348) conditions on joint health but has no memory; [CAWM](https://arxiv.org/abs/2609.18950) flushes replay at changepoints, which throws away data that is still useful after transport. Monotone, transported replay is not in any of them.
- **Cheapest first test:** MuJoCo Ant with gear ratio decaying 0.5% per episode on two legs and friction rising on one joint, 4 locomotion skills (directions) learned in sequence. Arms: ER, ER + RMA-style free latent, CAWM-style flush, wear-clock replay with linear \(T\). **Kill** if wear-clock replay does not beat the free-latent arm on current-body return of the first skill by ≥ 1 SE over 10 seeds at equal replay budget, or if a free latent sorted post hoc recovers the same ordering and the same gain.
- **Old-skill retention:** First-skill return on the current (aged) body, and on the factory body after a simulated "repair" reset of the gear ratio; the latter must not fall below ER.
- **Risk / likely tie:** Wear is often multi-dimensional; a 1-D clock may be a worse RMA. The test above has a 3-D wear stream for that reason.

### EL02 · Repair as rollback: store the adaptation residue, then pop it
- **Primitive** (new operation: reverse a body adaptation when the body returns).
- **Mechanism:** Every adaptation the policy makes to a body change is kept as a separate, named delta (adapter or weight diff) tied to the body-version fingerprint that triggered it (EL03). When a repair is detected (fingerprint jumps back toward an older version), the deltas written since that version are popped and the old skill is restored without retraining. Deltas that also improved task skill (not only body compensation) are split off by a two-body consistency test: keep the part of the delta that helps on both the old and the worn body.
- **Nearest prior / gap:** [TeAR](https://arxiv.org/abs/2609.36182) and [CAPABLE](https://arxiv.org/abs/2610.11971) adapt to actuator degradation and keep going; [ResMerge](https://arxiv.org/abs/2610.41663) merges residuals into the base; [Reset-free recovery after leg damage](https://arxiv.org/abs/2610.20838) treats damage as irreversible. None measures post-repair performance, which is where a compensated policy overcorrects.
- **Cheapest first test:** Hopper with an ankle at 50% gear for 300 episodes, then restored. Arms: keep fine-tuning (default), ResMerge-style merged residual, EWC, rollback. Measure return in the first 10 episodes after repair. **Kill** if keep-fine-tuning recovers within 10 episodes anyway (no repair shock exists), or rollback is not better than EWC on post-repair return.
- **Old-skill retention:** Post-repair return on all skills learned *before* the fault and *during* it; rollback must not delete during-fault task learning (the split test is checked here).
- **Risk / likely tie:** The repair shock may be small for robust policies; the first measurement is whether it exists.

### EL03 · Calibration ritual as a body hash
- **Primitive** (new object: a fixed, object-free motion whose sensor trace is the body's identity).
- **Mechanism:** The robot runs a fixed 5-second ritual (joint sweeps, a self-touch, a gravity hold) at the start of every session. A small encoder maps the trace to a fingerprint \(h\). The fingerprint is used three ways: as a changepoint detector for body change, as the key under which skill deltas are stored (EL02), and as a label-free forgetting alarm: if \(h\) has not moved, any drop in a skill is due to the world or to forgetting; if it moved, the drop may be a correct revision. The bridge assumption (PR #126) is that the ritual excites the same actuators the skills use.
- **Nearest prior / gap:** [Teaching robots to build simulations of themselves](https://arxiv.org/abs/2311.12151) and [Active embodiment identification](https://arxiv.org/abs/2605.08020) learn self-models, [OmniCalib](https://arxiv.org/abs/2609.19582) self-calibrates, [Continual hand–eye calibration](https://arxiv.org/abs/2604.15814) updates one calibration. None uses the self-probe as an index into a skill memory or as a forgetting/drift discriminator.
- **Cheapest first test:** Reacher + Pusher with 6 perturbation types (link length, gear, damping, camera pose, object mass, goal distribution); half are body changes and half are world changes. **Kill** if the ritual fingerprint does not separate body from world changes at AUROC ≥ 0.85, or a fingerprint computed from the first second of ordinary task rollouts does as well (then the ritual adds nothing).
- **Old-skill retention:** On body-change events, rehearse only skills whose ritual-gradient overlap is high; retention of all skills must not fall below uniform rehearsal at equal budget.
- **Risk / likely tie:** Self-ID from task rollouts may suffice; the kill arm checks this.

### EL04 · Blame-routed writes: self versus world
- **Primitive** (new operation: split every prediction error into a body part and a world part and write each to a different store).
- **Mechanism:** Maintain a body model (predicts proprioception from commands, trained on ritual and free motion) and a world model (predicts object state). A new error is attributed by which model's residual explains it. Body-attributed errors update a shared body-adaptation module used by *all* skills; world-attributed errors update only the skill that saw them. This prevents one skill from privately learning compensation for a weak motor (and other skills never learning it) and prevents a world quirk in one task from rewriting the body module used by all.
- **Nearest prior / gap:** [Proprioceptive–visual correspondence for self–other distinction](https://arxiv.org/abs/2606.13222) separates self from other for perception; [Online sensor diagnosis and repair](https://arxiv.org/abs/2610.36852) localizes faulty sensors. Neither routes learning writes.
- **Cheapest first test:** Pusher with 4 skills; inject a gear fault while one skill also gets a new object friction. Arms: per-skill fine-tuning, shared fine-tuning, blame-routed. **Kill** if blame-routed does not transfer the motor compensation to the 3 skills that never saw the fault (zero-shot return) better than shared fine-tuning, or loses more first-skill return.
- **Old-skill retention:** Return of untouched skills after both events; the world-attributed write must not leak into them (measured by their return on the old object).
- **Risk / likely tie:** Attribution can be confounded when body and world change together; the test does exactly that.

### EL05 · Fast body state: a short-lived write store for heat, battery and payload
- **Primitive** (new object: a decaying memory for reversible body states, kept apart from slow wear).
- **Mechanism:** Motor heat, battery sag and carried payload change dynamics for minutes and then revert. Adaptations to these states go to a store whose contents decay back to zero on a timescale fitted from telemetry (e.g. cooling constant), so they are never consolidated into the slow policy. A write is allowed into the slow store only if the same compensation persists across two cool-down cycles.
- **Nearest prior / gap:** [What should world models forget?](https://arxiv.org/abs/2610.03713) argues for retention stratified by invariance timescale in world models; fast/slow weights are standard. The new part is grounding the decay constant in a measured physical state and gating consolidation by survival across its cycles.
- **Cheapest first test:** HalfCheetah with a simulated thermal model (torque limit drops with integrated effort, recovers at rest), 3 gaits. Arms: online fine-tuning, fast/slow weights with a fixed decay, physically timed decay. **Kill** if the physically timed decay does not beat the best fixed decay on cold-start return of the first gait, or does not reduce consolidation of heat compensation (gait run cold should not be under-powered).
- **Old-skill retention:** Cold-body return on all gaits after a long hot session.
- **Risk / likely tie:** A tuned fixed decay may tie; that is the kill arm.

### EL06 · Damage reserve: keep part of the body unused so skills survive losing it
- **Primitive** (new object: an allocated actuator nullspace reserve, budgeted like replay).
- **Mechanism:** For each skill, train a family of solutions that differ in which joints carry the load, and pay a small task cost to keep at least one solution per skill that does not rely on each actuator. The reserve is updated as new skills arrive, so the continual-learning question becomes which reserves to keep when capacity is short. On a fault, the matching reserve is selected, not relearned.
- **Nearest prior / gap:** [Robots that adapt like animals](https://arxiv.org/abs/1407.3501) and [Hierarchical QD](https://arxiv.org/abs/2204.05726) build repertoires offline for one skill; [MoE fault-tolerant locomotion](https://arxiv.org/abs/2606.25965) trains on fault distributions. Keeping per-skill reserves *across a growing skill stream* under a budget is the new part.
- **Cheapest first test:** Ant, 4 sequential skills, budget of 2 reserve solutions per skill. Faults: one leg locked after training. Arms: fault-randomized training, IT&E-style repertoire for the last skill only, budgeted reserves. **Kill** if reserves give < 20% better post-fault return on the *first* skill than fault randomization at equal sample budget.
- **Old-skill retention:** Post-fault return of all four skills; intact-body return must stay within 5% of a no-reserve policy (the reserve's price).
- **Risk / likely tie:** Domain randomization over faults may already give this for free on small bodies.

## B · Sensors as replaceable organs

### EL07 · Gauge-fixed skill storage
- **Primitive** (new object: skills stored in a canonical gauge, with the robot's description as a transformation).
- **Mechanism:** [GaugeBench](https://arxiv.org/abs/2610.07597) shows morphology-aware policies collapse when the same robot is re-described (joint order, frames, units). Store every skill in a canonical gauge computed from the body (e.g. sort joints by ritual response, express frames relative to gravity and end effector). A sensor swap, re-mount, driver update or unit change is then a gauge transformation applied at the interface, and no stored skill needs rehearsal.
- **Nearest prior / gap:** GaugeBench defines the failure, not a CL fix; [UniLatent](https://arxiv.org/abs/2611.10061) aligns observations across embodiments in one step. Treating a sequence of re-descriptions as a continual stream with zero-write retention is new.
- **Cheapest first test:** 4 unimals, 3 re-descriptions each arriving sequentially. Arms: fine-tune, ER, canonical gauge. **Kill** if canonical gauge does not keep the first description's return within 10% after all re-descriptions, or if ER at 5% replay does the same.
- **Old-skill retention:** Return under every past description, not just the current one.
- **Risk / likely tie:** Canonicalization can be ambiguous for symmetric bodies; EL30 uses that symmetry.

### EL08 · Overlap-window translator
- **Primitive** (new operation: learn a sensor-to-sensor map during the window when both are mounted, then retire the old sensor).
- **Mechanism:** Real sensor upgrades often have a window when old and new are both available. Record paired streams, fit a translator new→old, and run every old skill through it. Skills are then fine-tuned on the new sensor *only where* the translator's error is high, so the old-sensor knowledge is kept where the map is exact and relearned only where the new sensor sees something the old one could not.
- **Nearest prior / gap:** [TaF-Foundation](https://arxiv.org/abs/2611.20718) and [BIDETA](https://arxiv.org/abs/2609.08673) build cross-sensor tactile representations from large paired corpora; [Drift compensation for a soft finger](https://arxiv.org/abs/2503.16540) updates one sensor. The overlap window as a learning event with error-gated relearning is new.
- **Cheapest first test:** Pusher with an RGB camera replaced by a depth camera at a different pose; 200 paired frames. Arms: retrain on new sensor, translator only, translator + error-gated fine-tune, joint fine-tune on both. **Kill** if the gated arm needs > 80% of the retrain arm's real episodes to match its return.
- **Old-skill retention:** Return on all skills learned before the swap, measured on the new sensor only.
- **Risk / likely tie:** Pretrained visual encoders may already absorb the swap; include a frozen pretrained-encoder arm.

### EL09 · Sensor lineage chain
- **Primitive** (new object: a version chain over sensor generations, with re-anchoring to stop translator error from compounding).
- **Mechanism:** After many swaps (EL08), skills reach the current sensor through a chain of translators whose errors compound. Keep the chain but re-anchor it: on each swap, the ritual (EL03) gives a body-grounded common reference that all generations observe, and translators are refit against the ritual, not against the previous link. The chain is a memory of past sensors that can be read backward if an old sensor returns.
- **Nearest prior / gap:** No CL paper found that models more than one sensor swap; GaugeBench and LIBERO-RIG are single-change benchmarks.
- **Cheapest first test:** 5 sequential camera generations (pose, FOV, noise) on Reacher. Arms: chained translators, re-anchored chain, retrain each time. **Kill** if re-anchoring does not reduce first-skill error growth over the chain by ≥ 2× versus naive chaining.
- **Old-skill retention:** First-skill return after 5 generations, and on generation 1 when it is remounted.
- **Risk / likely tie:** Chains of 5 may be too short to show compounding; extend to 10 in the same test.

### EL10 · Physical receipts for the success detector
- **Primitive** (new object: a physically grounded check that keeps the reward or success model honest across sensor drift).
- **Mechanism:** Online robot learning depends on a learned success detector that drifts with the sensors it reads. Every success label is paired with a "receipt": a cheap physical check (contact force, object weight on a scale, gripper aperture) that does not depend on the drifting sensor. Receipts are sparse but are the ground truth the detector is periodically re-fit to, and their disagreement rate is the trigger for relabeling the replay buffer.
- **Nearest prior / gap:** Reward-model drift is studied for LLM judges; [SEVI](https://arxiv.org/abs/2610.31829) uses evidential uncertainty for safety, not for success labels; [Online sensor diagnosis](https://arxiv.org/abs/2610.36852) repairs perception, not labels.
- **Cheapest first test:** Pusher with a learned vision success detector; camera drifts slowly; receipts are object position from simulator state at 5% of episodes. **Kill** if receipt-triggered relabeling does not reduce the fraction of replay items with wrong labels by ≥ 50% versus a fixed-schedule detector re-fit at equal receipts.
- **Old-skill retention:** True success (simulator) on old skills after the drift; must exceed fine-tuning with the unrefit detector.
- **Risk / likely tie:** A simple periodic re-fit may tie; it is the control.

### EL11 · Per-skill sensor dependency set as the retention index
- **Primitive** (new object: a minimal sensor set per skill, used to decide what a swap can break).
- **Mechanism:** For each skill, find by ablation the minimal set of sensors (and channels) that keeps it above threshold; store it with the skill. On a sensor swap, only skills whose set includes the swapped sensor are rehearsed or adapted; the rest are frozen. Training adds a pressure to shrink each set (so skills become cheaper to keep).
- **Nearest prior / gap:** [Targeted modality dropout](https://arxiv.org/abs/2610.09566), [Evidence-gated regularization](https://arxiv.org/abs/2609.03142) and [Blackout vs freeze](https://arxiv.org/abs/2609.39145) make one policy robust to missing modalities; none uses dependency sets to schedule retention.
- **Cheapest first test:** 6 Meta-World skills with camera + proprio + force; swap force sensor. Arms: rehearse all, rehearse random half, rehearse by dependency set. **Kill** if the dependency-set arm does not match rehearse-all retention at ≤ 60% of the rehearsal budget.
- **Old-skill retention:** Is the measure.
- **Risk / likely tie:** Ablation-based dependency may not predict fine-tuning interference.

## C · Sim and real as two coupled memories

### EL12 · Gap-localized plasticity
- **Primitive** (new operation: real data writes only into the state–action regions where sim and real disagree).
- **Mechanism:** Maintain a per-region fidelity map (sim vs real one-step prediction error, binned over state–action space or a learned embedding). Real-world updates are masked: gradients from transitions in high-fidelity regions are dropped or down-weighted, so the sim-trained policy is not rewritten where sim was already right, and real data is spent where it matters. The map is updated as new regions are visited.
- **Nearest prior / gap:** [Neural fidelity calibration](https://arxiv.org/abs/2611.28274) and [RealSimLoop](https://arxiv.org/abs/2609.09828) improve the simulator; [Frozen in Time](https://arxiv.org/abs/2610.40857) shows sim-to-real adaptation erodes sim skills; [PhysGuard](https://arxiv.org/abs/2606.16602) projects with Fisher information. None masks policy updates by measured fidelity.
- **Cheapest first test:** Sim = HalfCheetah, "real" = HalfCheetah with modified contact friction only on the back foot. Arms: full fine-tune, EWC, PhysGuard-style Fisher projection, fidelity-masked. **Kill** if the masked arm does not keep ≥ 90% of sim-skill return while matching full fine-tune's real return, or Fisher projection does the same.
- **Old-skill retention:** Return of 3 other sim-trained gaits on "real" after adaptation (they share the front foot dynamics).
- **Risk / likely tie:** Fidelity bins may be too coarse in high dimensions; first test is low-dimensional on purpose.

### EL13 · Exploit-signature unlearning
- **Primitive** (new operation: find and remove behaviour that only works because of a simulator artifact).
- **Mechanism:** A sim-trained skill may rely on a sim exploit (penetration, overly sticky contact). Find exploit signatures as state–action segments whose sim value is high and whose real value (or high-fidelity sim value) is low, and unlearn them by targeted gradient ascent on those segments with a retention anchor elsewhere. The exploit set becomes a stored list that future sim training is regularized against.
- **Nearest prior / gap:** [Demonstration unlearning](https://arxiv.org/abs/2608.20784) and [Removing one user's corrections](https://arxiv.org/abs/2611.10280) unlearn data sources; domain randomization hides exploits by noise. Unlearning by physical-fidelity signature is new.
- **Cheapest first test:** Train Hopper in sim with penetration allowed, evaluate in sim with penetration forbidden. Arms: fine-tune in strict sim, randomization over penetration stiffness, signature unlearning. **Kill** if unlearning does not match fine-tuning's strict-sim return with ≤ 50% strict-sim samples.
- **Old-skill retention:** Return on non-exploiting skills learned in lax sim.
- **Risk / likely tie:** Exploits may be distributed, not segment-local.

### EL14 · Simulator branches keyed by body version
- **Primitive** (new object: a versioned simulator that is part of the learner's memory, one branch per body version).
- **Mechanism:** Each body version (EL03 fingerprint) has its own calibrated simulator branch. Rehearsal of an old skill runs in the branch for the body it was learned on *and* in the current branch; disagreement between the two says whether the skill's change is a correct revision or forgetting. When a body returns (repair), its sim branch is reactivated for rehearsal.
- **Nearest prior / gap:** [Teaching robots to build simulations of themselves](https://arxiv.org/abs/2311.12151), [RealSimLoop](https://arxiv.org/abs/2609.09828) and [Online closed-loop sim-to-real](https://arxiv.org/abs/2609.28878) keep one current simulator. Versioned, branch-keyed sims as a CL memory are new.
- **Cheapest first test:** Ant with 4 body versions in a cycle (A→B→C→A). Arms: one current sim, sim branches. **Kill** if branches do not recover A-body return on return to A within 20% fewer episodes than one current sim refit.
- **Old-skill retention:** Return on all skills under each past body version.
- **Risk / likely tie:** Branch calibration may cost more real data than it saves.

### EL15 · Minimum rehearsal fidelity
- **Primitive** (new quantity: the lowest simulator fidelity at which rehearsal still retains a skill).
- **Mechanism:** Rehearsing in a cheap, crude sim saves robot time but may teach wrong actions. For each skill, measure the fidelity threshold below which sim rehearsal *hurts* real retention, and rehearse each skill at its threshold. Retention becomes a fidelity-cost curve, not a replay ratio.
- **Nearest prior / gap:** [World-model rehearsal](https://arxiv.org/abs/2607.19749), [REGEN](https://arxiv.org/abs/2606.27374) and [RIFAR](https://arxiv.org/abs/2610.03079) rehearse in a learned model and weight by reliability; none measures fidelity thresholds per skill.
- **Cheapest first test:** 4 Meta-World skills, 4 sim fidelity levels (contact model, timestep). **Kill** if per-skill thresholds do not vary by ≥ 2 levels across skills (then one global fidelity suffices), or fidelity-matched rehearsal does not beat uniform-fidelity rehearsal at equal compute.
- **Old-skill retention:** Is the measure.
- **Risk / likely tie:** RIFAR's reliability weighting may already approximate it.

## D · Safety, practice cost and irreversibility

### EL16 · Re-acquisition cost as retention priority
- **Primitive** (new quantity: what it would cost the robot to relearn a skill, used as its retention weight).
- **Mechanism:** For each skill, estimate its re-acquisition cost: robot hours, human demonstrations, wear and safety risk to relearn it from the current policy. Rehearsal and capacity go to skills with the highest cost-to-relearn times expected use, not to the most-forgotten ones. A skill that is cheap to relearn (one demo) may be allowed to decay.
- **Nearest prior / gap:** [Practice is not free](https://arxiv.org/abs/2611.19979) prices practice to choose the next task; [Memory Anchors](https://arxiv.org/abs/2608.26545) rehearses by representational conflict; LP selectors lose to uniform ([PR #119](https://github.com/manojbajaj95/cl/pull/119)). Pricing *relearning* to set retention is new.
- **Cheapest first test:** 8 Meta-World skills with assigned relearning costs (number of demos needed, measured by relearning from a forgotten state once). Arms: uniform rehearsal, Memory-Anchors-style, cost-weighted. Metric: total relearning cost paid over a 20-task stream with random revisits. **Kill** if cost-weighted does not reduce total cost by ≥ 15% versus uniform, at equal rehearsal budget.
- **Old-skill retention:** Retention of high-cost skills; low-cost ones may drop by design but are reported.
- **Risk / likely tie:** Costs measured once may not predict later relearning.

### EL17 · Irreversible-event memory class
- **Primitive** (new object: a write class for events that cannot be re-experienced, stored and rehearsed differently).
- **Mechanism:** Some events cannot be practiced again: a fall that broke a part, a spill, a collision with a person. They are rare and costly, so ordinary replay forgets them. Tag them by a reversibility estimate (the robot could not return to the pre-event state) and store them in a never-evicted, never-merged buffer whose lessons are compiled into constraints (EL19) rather than averaged into the policy.
- **Nearest prior / gap:** [REVERSAL-BENCH](https://arxiv.org/abs/2609.17745) measures the reversibility cliff for reset-free RL; [Failing gracefully](https://arxiv.org/abs/2608.05313) limits harm. A dedicated retention class for irreversible events is new.
- **Cheapest first test:** Point-mass navigation with absorbing "break" states that end learning on that body; 5 tasks streamed. Arms: ER, prioritized replay, irreversible buffer + constraint compile. **Kill** if the irreversible arm does not cut repeat entries into absorbing states by ≥ 50% after 5 tasks versus prioritized replay.
- **Old-skill retention:** Task return on old tasks must not fall (constraints may over-restrict).
- **Risk / likely tie:** Prioritized replay with a large priority may tie; it is the control.

### EL18 · Wear-priced forgetting
- **Primitive** (new operation: deliberately let a skill decay when rehearsing it costs more wear than its expected use is worth).
- **Mechanism:** Real rehearsal wears the body (EL01 gives the wear rate). Each skill gets a keep-or-release decision: rehearse while expected future value > wear cost of rehearsal; otherwise release it to a cold store (demos only) and free capacity. Forgetting becomes an economic choice, not an accident.
- **Nearest prior / gap:** [Practice is not free](https://arxiv.org/abs/2611.19979) measures practice cost; no CL method chooses to forget for wear.
- **Cheapest first test:** Same stream as EL16 with wear accumulated per rehearsal episode and degrading the body. **Kill** if wear-priced forgetting does not give higher total stream return (net of wear degradation) than uniform rehearsal and no rehearsal.
- **Old-skill retention:** Released skills' relearn time from the cold store must be reported.
- **Risk / likely tie:** Close to EL16; merge if the two decisions coincide.

### EL19 · Interventions as persistent constraint objects
- **Primitive** (new object: each human safety intervention becomes a stored constraint, not just a training sample).
- **Mechanism:** When a human stops or corrects the robot for safety, store a constraint (a state region and action set to avoid) with its provenance and body version. Constraints are enforced by a shield at execution and are transported across body changes (EL20); they are checked as a separate retention suite: an old intervention must never be re-violated, whatever the policy forgets.
- **Nearest prior / gap:** [HG-DAgger](https://arxiv.org/abs/1810.02890) and [Intervention-aware world models](https://arxiv.org/abs/2609.06009) learn from interventions as data; [Shielding](https://arxiv.org/abs/1708.08611) enforces hand-written specs; [SafeAdapt](https://arxiv.org/abs/2604.09452) keeps a policy in a safe Rashomon set. Interventions as a growing, transportable spec set is new.
- **Cheapest first test:** Simulated human (oracle) intervening on a 2D manipulation stream of 6 tasks. Metric: re-violation rate of old interventions after each new task. Arms: HG-DAgger, intervention-aware penalty, constraint objects. **Kill** if constraint objects do not reduce re-violations by ≥ 50% at ≤ 10% task-return cost.
- **Old-skill retention:** Old-task return under the growing shield.
- **Risk / likely tie:** Constraint sets may grow until the robot freezes; track the feasible-action fraction.

### EL20 · Safe-set transport across body change
- **Primitive** (new operation: move a certified safe set from one body to the next instead of re-certifying it from scratch).
- **Mechanism:** A safe set (control-barrier region) certified on body A is mapped to body B through the body diff (EL03 fingerprint change, or a kinematic map), with a conservative shrink proportional to model uncertainty. Online learning on B starts inside the transported set and grows it with data. The set history is kept so returning to A restores A's set.
- **Nearest prior / gap:** [Safe CRL with adaptive constraints](https://arxiv.org/abs/2605.18842), [SEVI](https://arxiv.org/abs/2610.31829) and [SafeAdapt](https://arxiv.org/abs/2604.09452) are single-body; [Stoppability value](https://arxiv.org/abs/2609.02358) is learned per robot. Transport of safe sets across bodies is new.
- **Cheapest first test:** Double-integrator and 2-link arm with link-length and mass changes; 4 body versions. Arms: re-learn safe set, keep old set, transported set. **Kill** if the transported set has a violation rate above re-learning, or does not reach 80% of the re-learned set's volume within half the data.
- **Old-skill retention:** Safe-set volume and violation rate on returned body A.
- **Risk / likely tie:** Uncertainty shrink may be so conservative that it is no better than starting small.

### EL21 · Near-miss harvesting as constraint witnesses
- **Primitive** (new object: near-misses as cheap, safe stand-ins for failures the robot cannot afford to have).
- **Mechanism:** Collisions and falls are rare and costly; near-misses (small margin to a constraint) are frequent and safe. Store near-misses with their margin, fit a constraint boundary from them by extrapolation, and keep those witnesses in a retention buffer so later skills do not drift toward old failure modes. The buffer is checked after every update: a new policy that reduces margin on old witnesses is flagged.
- **Nearest prior / gap:** Safety-margin shaping and near-miss analysis exist in safety engineering; [Learned stoppability](https://arxiv.org/abs/2609.02358) and [VAPS](https://arxiv.org/abs/2610.01397) score viability. Near-miss witnesses as a retention set across a skill stream is new.
- **Cheapest first test:** Same stream as EL19 without the human; witnesses only. **Kill** if margin-drop flags do not predict actual future violations at AUROC ≥ 0.8.
- **Old-skill retention:** Old-task return when updates are gated by the flag.
- **Risk / likely tie:** Margins may be noisy; split-half reliability first.

## E · Skills that persist across bodies

### EL22 · Cross-body consistency as a label-free forgetting detector
- **Primitive** (new object: the same skill on two bodies as a mutual check).
- **Mechanism:** When a policy controls several bodies, the *effect* of a skill on objects (object pose change) should agree across bodies even though the actions differ. A drop in agreement on one body, with the other unchanged, is a label-free sign that the skill was forgotten for that body. The bridge assumption is that object effects are shared across bodies (PR #126 requires one to be named).
- **Nearest prior / gap:** [RT-X](https://arxiv.org/abs/2310.08864), [CrossFormer](https://arxiv.org/abs/2408.11812) and [KITE](https://arxiv.org/abs/2606.22113) share data across bodies; none uses cross-body agreement as a monitor.
- **Cheapest first test:** Reacher-2 and Reacher-3 links on the same targets, sequential new tasks on one body. **Kill** if agreement drop does not predict measured forgetting on the other body at Spearman ρ ≥ 0.6 over 10 seeds.
- **Old-skill retention:** Is what it detects; also check that triggering rehearsal by it beats uniform.
- **Risk / likely tie:** Bodies differ in reach; agreement must be measured on the shared workspace.

### EL23 · Body homotopy memory
- **Primitive** (new operation: move a skill between bodies along a path of interpolated bodies, and keep the path as memory).
- **Mechanism:** [REvolveR](https://arxiv.org/abs/2202.05244) transfers along interpolated robots once. Keep the whole path: a stored sequence of intermediate bodies and policy checkpoints. A skill learned later on body B is carried back to body A by walking the path in reverse with short fine-tuning at each step, so old bodies keep receiving new skills.
- **Nearest prior / gap:** REvolveR and [The embodiment gap](https://arxiv.org/abs/2608.18433) are one-way; cross-embodiment pretraining has no stored path. Reverse transport of new skills to old bodies is new.
- **Cheapest first test:** Ant-4-leg → Ant-6-leg via 5 interpolated bodies; new skill learned on 6-leg. Arms: direct fine-tune on 4-leg, reverse homotopy, multi-body joint training. **Kill** if reverse homotopy does not reach 80% of direct fine-tune return with ≤ 50% of 4-leg samples.
- **Old-skill retention:** Old 4-leg skills after the new one is carried back.
- **Risk / likely tie:** Joint multi-body training may dominate.

### EL24 · Effect contracts with per-body realizers
- **Primitive** (new object: a skill as a body-free contract on object effects, plus a small realizer per body).
- **Mechanism:** Store each skill as a contract (pre- and post-conditions on object state) and a realizer per body that satisfies it. A new body only needs new realizers, learned against the contract; old contracts are never rewritten by new bodies. Realizer forgetting is local to one body.
- **Nearest prior / gap:** [KITE](https://arxiv.org/abs/2606.22113) decouples kinematics from interaction; [HPT](https://arxiv.org/abs/2409.20537) uses body-specific stems and a shared trunk; [Cross-controller transfer](https://arxiv.org/abs/2610.39280) adapts in-context. The contract as the unit of retention, verified per body, is new.
- **Cheapest first test:** 4 manipulation skills, 3 arms arriving in sequence. Arms: HPT-style shared trunk fine-tuning, per-body policies, contracts + realizers. **Kill** if contracts do not keep arm-1 success within 5% while matching HPT's arm-3 success with ≤ HPT's parameters.
- **Old-skill retention:** Arm-1 and arm-2 success after arm 3.
- **Risk / likely tie:** Contracts may underspecify dynamic skills (throwing).

### EL25 · Embodiment interference kernel
- **Primitive** (new quantity: a predicted interference between two bodies from their kinematic graphs, used to order body arrival and allocate capacity).
- **Mechanism:** Fit a kernel \(k(G_A, G_B)\) over kinematic graphs that predicts how much training on B hurts A. Use it to decide when a new body gets its own capacity versus sharing, and which old bodies need rehearsal.
- **Nearest prior / gap:** [MetaMorph](https://arxiv.org/abs/2203.11931) and [OmniAct](https://arxiv.org/abs/2611.33158) learn across morphologies; none predicts sequential interference.
- **Cheapest first test:** 12 unimals, all pairwise sequential fine-tunes (66 pairs). **Kill** if a graph-kernel predictor does not beat a size-difference baseline at predicting interference (held-out pairs, ρ improvement ≥ 0.2).
- **Old-skill retention:** Is the target.
- **Risk / likely tie:** This may be an assay, not a primitive; graded as such if it wins.

### EL26 · Body-schema push and pop for tools and attachments
- **Primitive** (new operation: attaching a tool pushes a body-schema frame; detaching pops it).
- **Mechanism:** A tool or end effector changes the body. On attach, a body-schema frame (extended kinematics and a small adapter) is pushed; all learning while the tool is on writes only to that frame. Detaching pops it and the bare-hand policy is exactly restored; reattaching the same tool restores its frame. This is TT02's push/pop with a physical, detectable event as the trigger instead of an inference boundary.
- **Nearest prior / gap:** [Body Schema Policy](https://arxiv.org/abs/2611.22713), [GeMuCo](https://arxiv.org/abs/2409.06427) and [Any-ttach](https://arxiv.org/abs/2605.30569) model or swap end effectors; [A²-VLA](https://arxiv.org/abs/2611.25656) adapts to new tools. None isolates tool-time writes for exact bare-hand retention.
- **Cheapest first test:** Pusher with a stick tool; alternate 5 bare-hand and 5 tool tasks. Arms: one policy, tool-conditioned policy, push/pop frames. **Kill** if push/pop does not keep bare-hand success within 2% while matching tool-conditioned tool success.
- **Old-skill retention:** Bare-hand success after tool use is the main check.
- **Risk / likely tie:** Tool-conditioned policies may already separate.

### EL27 · Ritual-gradient routing of updates into body and skill channels
- **Primitive** (new operation: decompose each update by its projection onto the direction that changes the body ritual's prediction).
- **Mechanism:** Every update has a component that changes how the policy acts on the body as a whole (visible in the ritual's predicted trace, EL03) and a component that is skill-specific. Project each gradient onto the ritual-gradient subspace; that part goes to a shared body channel, the remainder to the skill. This is a body analogue of NP07's update conjugacy: a body change followed by training should equal training followed by the body change, and the ritual subspace is where they are allowed to differ.
- **Nearest prior / gap:** Gradient projection (OGD, GPM) protects old tasks' subspaces; [PhysGuard](https://arxiv.org/abs/2606.16602) projects by Fisher. Using a body probe to define the subspace is new.
- **Cheapest first test:** Same as EL04. **Kill** if routing does not match blame-routed writes (EL04) with no world model, or loses to GPM on first-skill return.
- **Old-skill retention:** Untouched-skill return after body change.
- **Risk / likely tie:** Merge with EL04 if they coincide.

## F · What a body can rehearse

### EL28 · Shadow practice: object-free motor rehearsal
- **Primitive** (new operation: rehearse the motor part of a skill with no objects, no resets and no task reward).
- **Mechanism:** Most forgetting in a body-change stream is in the motor mapping, not in task logic. Shadow practice replays each skill's action trajectory in free space and fits only the body adaptation to track the stored effector path. It costs no setup and little wear, so it can run between tasks.
- **Nearest prior / gap:** [Sleeping robots](https://arxiv.org/abs/2606.17493) consolidates offline; [Practice makes policies](https://arxiv.org/abs/2607.26809) and [Reconstruct, practice, go real](https://arxiv.org/abs/2610.02204) practice with objects; mental practice is studied in human motor learning. Free-space practice as a retention channel is new.
- **Cheapest first test:** Pusher with gear drift; 4 skills. Arms: no rehearsal, object rehearsal at cost 5×, shadow practice at cost 1×, uniform rehearsal (PR #119 control). **Kill** if shadow practice does not retain ≥ 70% of object-rehearsal gain at 1/5 the cost.
- **Old-skill retention:** Object-task success after shadow practice only.
- **Risk / likely tie:** Contact-rich skills may not benefit.

### EL29 · Contact-event anchors
- **Primitive** (new object: discrete contact events as the anchors retention is measured and protected on).
- **Mechanism:** Skills differ most at contact events (make, break, slip). Store only contact-event snapshots (state, force, action) per skill and protect the policy on them; free-space parts are left to adapt. This is a smaller, physically chosen anchor set than whole trajectories.
- **Nearest prior / gap:** [Memory Anchors](https://arxiv.org/abs/2608.26545) chooses anchors by representational collapse; [Hybrid contact dynamics](https://arxiv.org/abs/2605.16398) models mode switches. Contact events as anchors is new.
- **Cheapest first test:** 6 Meta-World skills. Arms: ER whole trajectories, Memory Anchors, contact anchors at equal storage. **Kill** if contact anchors do not match Memory Anchors at ≤ 30% of its storage.
- **Old-skill retention:** Is the measure.
- **Risk / likely tie:** Contact detection may be noisy in vision-only setups.

### EL30 · Mirror rehearsal from body symmetry
- **Primitive** (new operation: use the body's symmetry group as a free rehearsal source).
- **Mechanism:** For a symmetric body, a mirrored skill is a different skill that shares weights. Practicing the mirror of a skill retains the original without storing it. When the body becomes asymmetric (damage, payload on one side), the symmetry is broken in a measured way, and mirror rehearsal is reweighted by the asymmetry.
- **Nearest prior / gap:** Symmetry augmentation for locomotion ([Symmetry considerations for learning task symmetric robot policies](https://arxiv.org/abs/2403.04359)) uses symmetry for sample efficiency; none uses it for retention or under broken symmetry.
- **Cheapest first test:** Ant with left-turn and right-turn skills; learn left, then 3 new tasks, then mirror-practice only. **Kill** if mirror rehearsal does not beat ER of left-turn at equal budget.
- **Old-skill retention:** Left-turn return after the stream.
- **Risk / likely tie:** Symmetric augmentation may already hold the skill.

### EL31 · Controller gains as a storage medium
- **Primitive** (new object: part of each skill stored in the low-level controller's impedance parameters, not in the network).
- **Mechanism:** Low-level impedance gains shape passive behaviour. Store a skill partly as a gain profile, which is not touched when the policy network is fine-tuned; the network only adds corrections. New skills that conflict in network space may not conflict in gain space.
- **Nearest prior / gap:** Variable impedance control and DMPs store behaviour in controller parameters; morphological computation argues the body computes. Using gains as a separate CL store with read/write rules is new.
- **Cheapest first test:** 4 Meta-World skills with a policy that outputs impedance. Arms: network-only, network + per-skill gain profile frozen after learning. **Kill** if gain profiles do not reduce first-skill forgetting by ≥ 30% versus network-only at equal parameters.
- **Old-skill retention:** Is the measure.
- **Risk / likely tie:** Equivalent to a per-skill adapter; graded as improvement if so.

### EL32 · Body × task retention matrix (benchmark)
- **Improvement / assay** (enabling tool for all other cards).
- **Mechanism:** A stream where both the body (wear, repair, sensor swap, new body) and tasks change, with a factorized matrix of retention: each skill on each past body. Built on MuJoCo with XML edits and LIBERO-RIG hardware changes.
- **Nearest prior / gap:** [LIBERO](https://arxiv.org/abs/2306.03310), [LIBERO-RIG](https://arxiv.org/abs/2610.18843), [Continual World](https://arxiv.org/abs/2105.10919) and [CALVIN-MAX](https://arxiv.org/abs/2611.31868) are task or one-change benchmarks.
- **Cheapest first test:** Build the 4-body × 6-skill matrix on Ant/Pusher. **Kill** if ER and fine-tuning are not separated by > 2 SE on the matrix (the benchmark would not discriminate).
- **Old-skill retention:** Is the benchmark.
- **Risk / likely tie:** Assay, not a primitive.

## Ranked deeper questions

1. **Is repair shock real?** (EL02, EL14, EL26) If a policy that has adapted to a worn body loses performance when the body is repaired, "return to an old body" is a new retention problem no benchmark measures. First answer: the Hopper fault/repair test in EL02. Kill the whole group if the shock is < 10% and recovers in under 10 episodes.
2. **Can a body probe tell correct revision from forgetting?** (EL03, EL04, EL27) If the ritual separates body from world change, it gives the label-free forgetting signal PR #126 said needs a bridge assumption. First answer: EL03's 6-perturbation test.
3. **Where should real data be allowed to write?** (EL12, EL13, EL15) Fidelity-masked updates may solve the erosion seen in Frozen in Time. First answer: EL12's HalfCheetah test against Fisher projection.
4. **Should retention be priced?** (EL16, EL18) Retention weighted by relearning cost changes what "forgetting" means for robots. First answer: EL16 against uniform rehearsal.
5. **Do skills survive bodies arriving in sequence?** (EL22, EL23, EL24) Cross-embodiment work trains jointly; the sequential case is unmeasured. First answer: EL24's 3-arm stream.
