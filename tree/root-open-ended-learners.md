# Root: Open-ended self-curriculum learners

Root node (depth 0) · 32 candidate primitives (OE01–OE32) · 4 ranked deeper questions · Ideas only; no experiments run

**Thesis.** Open-ended learners pick their own next problem. POET pairs environments with agents, OMNI and OMNI-EPIC write new environments in code and filter them for interestingness, AMIGo and asymmetric self-play train a goal setter against a solver, Voyager writes its own curriculum and skill library, PAIRED and ACCEL design levels by regret, learning-progress curiosity chooses goals by improvement, and self-instruct, self-rewarding LMs, Absolute Zero and R-Zero let a language model write, grade and solve its own tasks. All of these treat the task stream as something to make *harder* or *more novel*. None treats it as something the learner must *keep*. In an open-ended loop the learner both causes its old tasks to leave the stream (it moves on) and owns the only machinery that could bring them back (the generator, the judge, the goal space). Continual learning is therefore not an add-on to open-endedness: what an open-ended learner invents decides what it forgets. The cards below look for new objects or operations that let the inventor's own machinery carry retention: skills stored as things that regenerate them (task keys, reward programs, worlds), drives that treat "forgotten" as "novel again", goals and sensors that survive the learner's representation drift, and curricula that shape the geometry of the weights they write.

**Scope.** Read before writing: the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). Orthogonal to the three branches that recently stalled at score 3: learner–world co-evolution ([PR #363](https://github.com/manojbajaj95/cl/pull/363), where a *deployed* learner's outputs reshape users and tools), test-time weights ([PR #311](https://github.com/manojbajaj95/cl/pull/311)) and population learners ([PR #381](https://github.com/manojbajaj95/cl/pull/381)). Here the learner is alone and its world is *invented by itself*, on purpose, for learning. Ledger results this root builds on and must not restate:
- **LP self-curricula are closed** (ledger row "Learning-progress self-curricula", [PR #119](https://github.com/manojbajaj95/cl/pull/119)): every LP selector retains less than uniform sampling in a linear host (ALP −0.058), because at stationarity all practice gain is recovery of self-inflicted drift. The one positive number is a one-step total-competence lookahead oracle at +0.067 over uniform. Cards OE06, OE20 and OE24 must beat uniform, not ALP.
- **Generator-side forgetting** ([PR #120](https://github.com/manojbajaj95/cl/pull/120), FCU9): a self-play proposer may lose the ability to emit old task types. Inverse-witness synthesis (#120 #1) and conservative task-language extension (#120 #11) are already rowed; no card here restates them.
- **Generator identity doesn't matter for replay** ([PR #8](https://github.com/manojbajaj95/cl/pull/8)): self-written QA replay ties teacher-written QA. No card claims an effect from *who* writes a task.
- **Past selves as adversaries and pop-quiz adversaries** ([PR #135](https://github.com/manojbajaj95/cl/pull/135), #119 #10) are rowed as combinations of FSP/PSRO and PAIRED aimed at the past; cards that use past checkpoints (OE09) say what differs.
- **Exercise hand-down** (CE21 in [PR #343](https://github.com/manojbajaj95/cl/pull/343)) passes a task generator between learners; OE01 and OE02 keep generators *inside* one learner as its memory format and must beat it.

## Literature check

alphaXiv searches (16 queries) across open-ended environment generation, LLM self-play from zero data, learning-progress and autotelic goal selection, self-rewarding and self-evolution collapse, forgetting under UED, objective invention, interestingness and quality diversity, library learning, discovered RL objectives, skill discovery and generated environments. Each card names its nearest prior art; a "gap" is a hypothesis to verify against the full text before any pilot, not a priority claim.

| Line | Already available | What a new primitive here must add |
|---|---|---|
| Environment generation | [POET](https://arxiv.org/abs/1901.01753), [Enhanced POET](https://arxiv.org/abs/2003.08536), [OMNI](https://arxiv.org/abs/2306.01711), [OMNI-EPIC](https://arxiv.org/abs/2405.15568), [Dreaming in Code](https://arxiv.org/abs/2602.08194), [GenEnv](https://arxiv.org/abs/2512.19682), [COvolve](https://arxiv.org/abs/2603.28386), [XLand](https://arxiv.org/abs/2107.12808), [GREMLIN](https://arxiv.org/abs/2611.33101) (random neural environments for rule discovery) | Archives exist but are used to pick the *next* task. Nothing uses the archive as the learner's memory format, or makes an environment's laws the unit that decides what must be re-tested. |
| Regret-based design | [PAIRED](https://arxiv.org/abs/2012.02096), [PLR](https://arxiv.org/abs/2010.03934), [ACCEL](https://arxiv.org/abs/2203.01302), [PACE](https://arxiv.org/abs/2605.01358) (parameter change as a UED score), [Training Stability under Adaptive Curricula](https://arxiv.org/abs/2611.08787), [Learning Curricula in Open-Ended Worlds](https://arxiv.org/abs/2312.03126) | Regret and parameter change score difficulty or stability of the *current* task. A primitive must score a task by what it does to the learner's *old* competence or weight geometry. |
| Goal setters | [Asymmetric self-play](https://arxiv.org/abs/1703.05407), [AMIGo](https://arxiv.org/abs/2006.12122), [Voyager](https://arxiv.org/abs/2305.16291), [DIAYN](https://arxiv.org/abs/1802.06070), [feature control](https://arxiv.org/abs/1705.06769), [Go-Explore](https://arxiv.org/abs/1901.10995) | Goals are coordinates in a fixed space. Nothing handles goals invented in a representation that the learner's own training then moves. |
| Learning progress | [CURIOUS](https://arxiv.org/abs/1810.06284), [Teacher–Student CL](https://arxiv.org/abs/1707.00183), [MAGELLAN](https://arxiv.org/abs/2502.07709), [Gradient-Momentum Coupling](https://arxiv.org/abs/2605.05856), [Signed Compression Progress on a Sealed Audit](https://arxiv.org/abs/2606.11417) | Ledger #119: LP rewards recovery of self-inflicted drift and retains less than uniform. A primitive must change what is counted as progress, not how it is estimated. |
| LLM self-play and self-reward | [Self-Instruct](https://arxiv.org/abs/2212.10560), [Self-Rewarding LMs](https://arxiv.org/abs/2401.10020), [Absolute Zero](https://arxiv.org/abs/2505.03335), [R-Zero](https://arxiv.org/abs/2508.05004), [J-Zero](https://arxiv.org/abs/2608.26582), [G-Zero](https://arxiv.org/abs/2605.09959), [CompassPlay](https://arxiv.org/abs/2609.32228) (proposer paid for where it moves the solver), [Skill Self-Play](https://arxiv.org/abs/2607.22529), [Self-Play Pretraining](https://arxiv.org/abs/2609.30063) | Collapse is the studied failure: [Questioning the Questions](https://arxiv.org/abs/2610.04299), [Survive or Collapse](https://arxiv.org/abs/2605.22217), [Vocabulary Dropout](https://arxiv.org/abs/2604.03472), [Fragility of Self-Rewarding](https://arxiv.org/abs/2611.28582), [placebo trial](https://www.alphaxiv.org/abs/2610.reward-placebo-zero-data-self-play). Forgetting of skills the loop no longer proposes is measured ([Are Self-Evolving Agents Continual Learners?](https://arxiv.org/abs/2610.25858)) but no operator targets it. |
| Objective invention | [Eureka](https://arxiv.org/abs/2310.12931), [Habitats](https://arxiv.org/abs/2611.31160) (open-ended evolution of agent objectives), [Subjective functions](https://arxiv.org/abs/2512.15948), [Discovering RL algorithms](https://arxiv.org/abs/2007.08794), [learned intrinsic rewards](https://arxiv.org/abs/1912.05500) | Objectives are invented to make new behaviour. None is used to *store* a mastered behaviour or to discover a retention rule. |
| Abstraction growth | [DreamCoder](https://arxiv.org/abs/2006.08381), [LILO](https://arxiv.org/abs/2310.19791), [EliteReplay](https://arxiv.org/abs/2610.22290) | Libraries grow by compression of solutions; no rule ties admission of a *new task* to compression of the *old task archive*. |
| Definitions | [An Information-Theoretic Definition for Open-Ended Learning](https://arxiv.org/abs/2606.08369) | Defines open-endedness for an observer; it does not say what the learner may forget while staying open-ended. |

---

## A · Skills stored as things that regenerate them

### OE01 · Task keys: replay by regeneration, not storage
- **Primitive:** a *task key*, a short seed plus generator version that deterministically rebuilds a self-invented task with its checker. The archive of an open-ended learner becomes a list of keys, and rehearsal re-instantiates fresh instances instead of replaying stored episodes.
- **Mechanism:** The proposer is restricted to emitting tasks as (generator program, seed); the generator is frozen per version and versioned on change. A skill is "kept" if it passes fresh instances regenerated from its key. Replay budget is spent on new instances, so the solver can't memorize replayed items. When the generator version changes, keys are migrated by re-running old seeds under the old frozen version (kept in cold storage, a few KB each).
- **Nearest prior / gap:** OMNI-EPIC archives environment code, POET archives env parameters, GREMLIN draws random neural environments from seeds; all use the archive to choose the next task. Deep generative replay ([1705.08690](https://arxiv.org/abs/1705.08690)) regenerates *data* from a learned, drifting generator. The gap: a frozen, versioned, exact regenerator as the CL memory format, with fresh-instance rehearsal. Ledger SM1 (seed log) stores training seeds, not task regenerators.
- **Cheapest first test:** Procedural gridworld or arithmetic-program tasks, MLP or 0.5B LM solver, 20 self-invented families. Arms at equal bytes and equal replay steps: stored-episode reservoir replay, generative replay with the live proposer, task-key regeneration. Kill if key regeneration ties stored replay on held-out fresh instances of old families.
- **Old-task retention:** Accuracy on fresh instances of all 20 families after the 20th, plus the base model's held-out benchmark.
- **Risk / likely tie:** Many procedural benchmarks already sample fresh instances; the claim rests on the learner inventing the generators itself and on the instance-freshness effect beating stored replay.

### OE02 · Self-inverse RL: compress each mastered skill into a reward program
- **Primitive:** a *skill reward*, a short program the learner writes for itself whose maximization from the current weights re-grows a mastered skill. The stored object is an objective, not data or weights.
- **Mechanism:** When a self-invented skill passes mastery, the learner writes candidate reward programs (Eureka-style) and keeps the shortest one whose brief optimization from a *perturbed* copy of the current policy regains the skill. Rehearsal = a few RL steps on the stored reward when a probe shows decay. The archive is objectives; data is discarded.
- **Nearest prior / gap:** Eureka writes rewards for human-named tasks; Habitats evolves objectives to produce new behaviour; inverse RL recovers rewards from experts. The gap: inverse RL of *oneself*, used as a retention format, with the "regrows from a perturbed policy" test as the admission rule.
- **Cheapest first test:** MiniGrid or Craftax-Classic skills, PPO agent, 8 skills in sequence. Arms at equal storage bytes and equal rehearsal compute: behaviour-cloning replay of stored trajectories, policy distillation from a frozen snapshot, stored skill rewards. Kill if stored rewards regain less of the skill than trajectory replay at equal compute.
- **Old-task retention:** Success on all 8 skills after the last, measured both before and after one rehearsal pass.
- **Risk / likely tie:** Reward programs may be longer than trajectories for skills without a clean success predicate; the card needs skills where a 10-line reward suffices.

### OE03 · Worlds as the genome: keep the environments, regrow the agent
- **Primitive:** treat the archive of self-invented environments as the learner's persistent state and the network as disposable: periodically reinitialize (or partially reset) and regrow from the archive, and measure whether the worlds alone are a sufficient statistic of the learner.
- **Mechanism:** An open-ended loop runs for G generations. At each generation boundary the agent is reset (full or ReDo-style partial reset) and retrained on a curriculum *replayed from the archive in invention order*, then continues inventing. The archive is pruned to the smallest subset that still regrows all skills ("world core"). Plasticity is restored by the reset; retention is carried by the worlds.
- **Nearest prior / gap:** POET keeps env–agent pairs; plasticity resets ([ReDo](https://arxiv.org/abs/2302.12902), primacy-bias resets) rely on a replay buffer; iterated learning and generational training regrow from a teacher. The gap: the learner's *own invented worlds*, replayed in invention order, as the only carrier across resets, plus the world-core pruning operator.
- **Cheapest first test:** OMNI-EPIC-lite in a 2D physics or MiniGrid code space, 3 generations. Arms: no reset; reset + replay buffer; reset + teacher distillation from the old agent; reset + world archive. Kill if world-archive regrowth needs more than 2× the compute of distillation to reach the same skill coverage.
- **Old-task retention:** Coverage of all archived worlds after each regrowth, and plasticity on a fresh held-out world.
- **Risk / likely tie:** Distillation from the old agent is the strong control and is cheap; the claim needs a regime where the old agent's plasticity is already lost.

### OE04 · Experience-to-environment compiler
- **Primitive:** compile the learner's *old* experience into a small executable environment (code) that reproduces the success conditions of its old skills, then rehearse by playing in the compiled world.
- **Mechanism:** For each finished skill, an LM writes environment code fit to logged transitions (Dreaming-in-Code style), verified by checking that the old policy's success rate in the compiled env matches its logged rate and that a broken policy fails. Only compiled worlds that pass both checks are kept; raw logs are deleted.
- **Nearest prior / gap:** Dreaming in Code and GenEnv generate environments *forward* for curriculum; world-model replay and SD05-style counterfactual replay ([PR #333](https://github.com/manojbajaj95/cl/pull/333)) use learned neural simulators. The gap: compiling past experience *backward* into a verified code world, with the two-sided success check as the admission rule.
- **Cheapest first test:** Text-game or MiniGrid tasks with an LM coder (7B). Arms at equal storage: raw-log replay, neural world-model replay, compiled-world replay. Kill if compiled worlds fail the two-sided check on more than half the skills, or tie raw-log replay.
- **Old-task retention:** Success on the real old environments after rehearsal only in compiled worlds.
- **Risk / likely tie:** Compiled worlds may capture success conditions but not the dynamics that make the skill hard, so rehearsal there may be too easy.

### OE05 · Archive MDL ratchet: add a task only if it shortens the archive
- **Primitive:** an admission rule for open-ended task invention: a new task enters the archive only if, together with an updated abstraction library, the total description length of *all* archived tasks goes down or rises by less than the new task's own length. Novelty is paid for with unification.
- **Mechanism:** Tasks are programs in a growing DSL (DreamCoder/LILO). On each proposal, re-run library compression over archive ∪ {new}. Admit if ΔMDL < len(new) − margin. The solver learns abstractions, and every abstraction it learns is exercised by old tasks re-expressed through it, so old tasks stay in use.
- **Nearest prior / gap:** DreamCoder compresses *solutions* to grow a library; OMNI filters by interestingness; POET by minimal criterion. The gap: MDL of the *task archive* as the minimal criterion, which couples invention to re-expression of old tasks.
- **Cheapest first test:** List-processing or ARC-like program tasks, small synthesizer with library learning, 200 proposals. Arms: OMNI-style interestingness filter, POET minimal criterion, random admission, MDL ratchet. Kill if the ratchet admits fewer than 20% of tasks or does not raise old-task solve rate after the last proposal.
- **Old-task retention:** Solve rate on the first 50 archived tasks after all proposals, re-expressed or not.
- **Risk / likely tie:** Compression may favour trivial variants; the margin needs tuning and an anti-trivia check.

---

## B · Drives that count "forgotten" as "new again"

### OE06 · Forgetting-horizon novelty archive
- **Primitive:** a novelty archive whose entries decay at the learner's *measured* forgetting rate, so a behaviour becomes novel again exactly when the learner can no longer produce it. Novelty search and rehearsal become one drive.
- **Mechanism:** Each archive entry stores a behaviour descriptor and a cheap probe. An entry is "present" only while its probe passes; failed probes remove it from the novelty reference set. The novelty reward for re-producing a lapsed behaviour is the same as for a new one. No separate replay.
- **Nearest prior / gap:** Novelty search (Lehman & Stanley) keeps a permanent archive; Go-Explore returns to archived cells for exploration; CURIOUS pays absolute LP to revisit forgotten goals. The gap: membership defined by *current* competence, so the novelty reference set is the learner's retained repertoire. Ledger #119 showed LP revisiting loses to uniform; novelty based on lapse is a different signal (binary, competence-anchored) and must beat uniform too.
- **Cheapest first test:** #119's linear host plus a nonlinear MLP host, 20 goal families. Arms: uniform, ALP, permanent-archive novelty, lapse-archive novelty, #119's lookahead oracle. Kill if lapse novelty doesn't beat uniform on worst-family retention.
- **Old-task retention:** Mean and worst-family competence over all 20 families at the end.
- **Risk / likely tie:** If lapse detection is noisy, the drive reduces to periodic random revisits, which is uniform.

### OE07 · Boredom memory: retain the interestingness function
- **Primitive:** treat the learner's *interestingness model* as a continual learner with its own retention, and detect cycles caused by its forgetting: if the model forgets that a family was boring, the loop re-invents it, and the archive cycles.
- **Mechanism:** OMNI-style interestingness is learned online from the archive. Keep a frozen "boredom ledger" of family-level verdicts and an equivalence probe; when the live model calls an archived-boring family interesting again, either (a) the learner forgot the family (then it is rehearsal, allowed) or (b) the model forgot its verdict (then it is a cycle, blocked). The two are told apart by a solver probe.
- **Nearest prior / gap:** OMNI uses a frozen LLM for interestingness; QDAIF and [What makes a theorem interesting](https://arxiv.org/abs/2611.02905) learn it; none studies forgetting of the interestingness function. The gap: interestingness drift as a CL object and the solver-probe split between rehearsal and cycling.
- **Cheapest first test:** Open-ended loop with a learned interestingness head over 500 proposals in a code-task space. Arms: frozen OMNI judge, learned judge, learned judge + boredom memory. Kill if the learned judge without memory shows no measurable cycling (family re-invention rate within 10% of frozen).
- **Old-task retention:** Solver success on all families, and the share of proposals that are re-inventions.
- **Risk / likely tie:** Cycling may not appear at small scale; the first test is also the existence test.

### OE08 · Stepping-stone value by counterfactual frontier expansion
- **Primitive:** score a candidate task by how many *other* archived-unsolved tasks become solvable after brief training on it, measured on a forked solver, and charge it for archived-solved tasks it breaks. A task's value is its signed effect on the frontier.
- **Mechanism:** For each proposal, fork the solver, train k steps, re-probe the archive (solved and unsolved sample). Value = newly solved − newly broken. The proposer is trained on this value.
- **Nearest prior / gap:** POET transfers agents between environments; CompassPlay pays the proposer for the direction it moves the solver; #119's one-step lookahead oracle uses total competence. The gap: a signed frontier count over an *invented* archive, which pays for opening and charges for breaking. It is the learnable form of #119's oracle in open-ended spaces.
- **Cheapest first test:** Absolute-Zero-style code puzzles, 0.5B solver. Arms at equal solver steps: learnability reward (p(1−p)), CompassPlay reward, signed frontier value. Kill if frontier value ties learnability on final archive coverage.
- **Old-task retention:** Archive coverage plus the base model's held-out reasoning set.
- **Risk / likely tie:** Fork-and-probe is expensive; an amortized predictor may reduce it to CompassPlay.

### OE09 · Temporal-disagreement goals
- **Primitive:** invent goals where the current learner and a checkpoint from k updates ago *disagree* about the outcome of an action, and go resolve the disagreement in the world. Each resolution is either a new skill or a detected loss.
- **Mechanism:** Keep a ring of past checkpoints. Sample states; compute disagreement between current and past predicted success or value. Goals = high-disagreement states. After the attempt, label the disagreement: past right → forgetting (trigger rehearsal of that goal), current right → learning (no action).
- **Nearest prior / gap:** Ensemble disagreement exploration ([1906.04161](https://arxiv.org/abs/1906.04161)) uses parallel models; PR #135 uses past checkpoints as auditors that search for negative flips. The gap: temporal disagreement as the *goal generator* inside the open-ended loop, with the world as the arbiter rather than a labelled test set.
- **Cheapest first test:** Goal-conditioned MiniGrid with a shifting goal distribution. Arms: random goals, ensemble disagreement, AMIGo, temporal disagreement. Kill if temporal-disagreement goals don't find more true negative flips per episode than random goals.
- **Old-task retention:** Success on goals mastered early, at the end of training.
- **Risk / likely tie:** Must show more than PR #135; the difference is that it is an exploration drive, not an audit.

### OE10 · Gradient-subspace novelty search
- **Primitive:** call a task novel if its gradient on the current solver is orthogonal to the span of past tasks' gradients. One quantity serves as a novelty drive (new directions are new skills) and a forgetting guard (orthogonal updates interfere less, as in OGD).
- **Mechanism:** Maintain a low-rank basis of past task gradients (GPM-style). The proposer is rewarded by ‖(I − P)g_task‖ / ‖g_task‖, gated by learnability. Training then proceeds without projection; the curriculum, not the optimizer, avoids interference.
- **Nearest prior / gap:** OGD ([1910.07104](https://arxiv.org/abs/1910.07104)) and GPM ([2103.09762](https://arxiv.org/abs/2103.09762)) project updates; PACE scores environments by parameter change; novelty search uses behaviour space. The gap: moving orthogonality from the optimizer to the task proposer, so the learner *invents* non-interfering tasks.
- **Cheapest first test:** Procedural task generator over a 2-layer MLP or LoRA on 0.5B. Arms: behavioural novelty, learnability, GPM-projected training on learnability tasks, gradient-novelty proposer. Kill if gradient-novelty doesn't beat GPM-projected training on retention at equal coverage.
- **Old-task retention:** Accuracy on all generated tasks after the run.
- **Risk / likely tie:** Orthogonal gradients at the current point may not stay orthogonal; the test must report retention, not only the score.

### OE11 · Learner-dynamics model as a planning substrate
- **Primitive:** a learned forward model of the learner's own training, mapping (current state summary, candidate task) → predicted change in the competence vector over all archived tasks, used to plan multi-step self-curricula.
- **Mechanism:** Fit the model on cheap forks (k steps on a candidate, re-probe archive). Plan with beam search over task sequences to maximize the minimum archived competence plus frontier growth. Refit as the learner changes.
- **Nearest prior / gap:** Learning to teach ([1805.03643](https://arxiv.org/abs/1805.03643)) and machine teaching optimize a teacher policy; #119 showed a *one-step* total-competence oracle beats uniform by +0.067 where all LP selectors lose. The gap: a learned, multi-step approximation of that oracle over invented tasks.
- **Cheapest first test:** #119's host (linear and MLP), 20 families. Arms: uniform, ALP, the one-step oracle, learned model with 1-step and 4-step planning. Kill if the learned model recovers less than half of the oracle's gain over uniform.
- **Old-task retention:** Mean and worst-family competence.
- **Risk / likely tie:** The model needs many forks; the test reports fork compute against a uniform-sampling budget.

### OE12 · Plasticity-keeping proposer
- **Primitive:** a proposer whose reward is the *solver's plasticity*, not its competence: tasks are chosen to keep dormant units active, effective rank high, and the solver's speed on a fresh probe task fast.
- **Mechanism:** Every N steps, measure plasticity indicators (dormant-unit fraction, effective rank, steps-to-fit a fresh random task). The proposer is rewarded by their improvement, gated so the task is still learnable. Plasticity becomes something the self-curriculum invents tasks for.
- **Nearest prior / gap:** Plasticity loss is fixed by resets, ReDo, shrink-and-perturb and regularizers; Training Stability under Adaptive Curricula studies UED instability. The gap: plasticity as the proposer's objective, using task choice instead of weight surgery.
- **Cheapest first test:** Permuted or shifting-label stream with a self-proposer that can choose task parameters. Arms: learnability proposer, learnability + ReDo, plasticity proposer. Kill if the plasticity proposer doesn't keep steps-to-fit below learnability + ReDo after 50 shifts.
- **Old-task retention:** Accuracy on the first 10 tasks after the last shift.
- **Risk / likely tie:** Plasticity-friendly tasks may be noise tasks that teach nothing; learnability gating must be strict.

---

## C · Goals, sensors and intentions that survive the learner's own drift

### OE13 · Goal re-grounding across representation drift
- **Primitive:** a *goal translator* that carries self-invented goals, defined as targets in the learner's own latent space, forward when training moves that space. Without it, an invented goal silently changes meaning.
- **Mechanism:** Goals are stored as (latent target, a few anchor observations that achieved it). After each update, re-embed anchors, fit a small map old-latent → new-latent on them, and re-target the goal. A goal whose anchors no longer embed consistently is flagged as "lost meaning" and re-grounded by re-achieving it.
- **Nearest prior / gap:** Skew-Fit, DIAYN and feature-control goals live in a learned latent space that drifts; CE07 ([PR #343](https://github.com/manojbajaj95/cl/pull/343)) migrates pending *amendments* when a symbolic vocabulary changes. The gap: drift of *self-invented goals* in a neural latent space, and anchor-based re-grounding.
- **Cheapest first test:** Visual goal-conditioned agent (latent goals from a VAE trained online), 3 phases. Arms: no re-grounding, frozen encoder for goals, anchor re-grounding. Kill if latent goals from phase 1 reach the same success in phase 3 with no re-grounding.
- **Old-task retention:** Success on phase-1 goals in phase 3.
- **Risk / likely tie:** The frozen-encoder control is cheap; the card must show the online encoder is needed for new goals.

### OE14 · Sensor invention: open-endedness by growing the observation space
- **Primitive:** let the learner invent new *observation channels* (computed features, measurement tools) that make new goals expressible, and keep old goals achievable in the old channels.
- **Mechanism:** The agent can write a small feature function (code or a probe head) over raw state and append it to its observation. Goals can then name the new feature. A new sensor is kept only if goals over it are learnable and old goals' success does not drop.
- **Nearest prior / gap:** Active feature acquisition picks among given features; CE23 in the cultural-evolution root does affordance acquisition in a symbolic setting; OMNI-EPIC writes whole environments. The gap: growing the agent's own sensorium as the open-ended axis.
- **Cheapest first test:** Crafter-like world where some state is only visible via a computed feature. Arms: fixed sensors with goal invention, given full sensors, sensor invention. Kill if sensor invention doesn't reach goals that fixed sensors can't express.
- **Old-task retention:** Success on goals invented before each new sensor.
- **Risk / likely tie:** Hand-designing the feature language makes the test easy; the feature language must be generic.

### OE15 · Intention persistence across updates
- **Primitive:** retention of *commitments*: a long-horizon goal the learner invented at time t must still be pursued correctly at t+k after the weights changed. The retained object is an intention, not a skill.
- **Mechanism:** Invented goals carry a commitment record (goal, plan sketch, progress state). After each update, the learner resumes active commitments; a commitment fails if the updated policy abandons or misreads it. Train with a persistence loss on resumed episodes.
- **Nearest prior / gap:** BDI agents keep intentions symbolically; goal-conditioned RL resets goals per episode; Voyager keeps a skill library, not commitments. The gap: intentions that span weight updates as a CL retention target.
- **Cheapest first test:** Multi-episode tasks in a text game where a goal spans 3 training rounds. Arms: no record, record without persistence loss, record + persistence loss. Kill if no-record agents already resume correctly.
- **Old-task retention:** Completion rate of commitments made before updates, plus standard old-task success.
- **Risk / likely tie:** May reduce to memory in the prompt; the test must run with weights-only state.

### OE16 · Autobiographical tasks: invent tasks about your own past
- **Primitive:** a self-curriculum whose tasks are questions about the learner's *own history* (what it solved, how, when), so remembering becomes a skill that the open-ended loop trains, not a side effect.
- **Mechanism:** The proposer samples past episodes from a log and writes questions whose answer requires recalling them ("what tool sequence solved task family F the first time?"). The solver is trained on these without the log in context. The loop schedules them like any invented task.
- **Nearest prior / gap:** Self-quizzing replay (ledger #11) was falsified: generator identity doesn't matter. The gap here is not who writes the quiz but *what it asks about*: procedural, temporally indexed facts about the learner's own trajectory, which no teacher has.
- **Cheapest first test:** 0.5B LM agent on a stream of 10 tool-use families. Arms at equal tokens: plain replay, teacher QA on task content, autobiographical QA. Kill if autobiographical QA doesn't beat plain replay on re-solving old families.
- **Old-task retention:** Re-solve rate on all 10 families.
- **Risk / likely tie:** Could tie teacher QA as #11 did; the test must include the teacher-QA arm.

---

## D · Curricula that shape the weights they write

### OE17 · Minimal-pair task invention to localize updates
- **Primitive:** for every new task, the proposer also invents its *minimal pair*: a near-identical task with the opposite answer. Training on both confines the update to the feature that tells them apart, so the new skill touches fewer weights.
- **Mechanism:** The proposer must emit (t, t̄) with t̄ differing from t in one controlled factor and with the opposite label or outcome. The solver trains on both. A pair is kept if the solver's update on the pair has smaller overlap with old-task Fisher than the update on t alone.
- **Nearest prior / gap:** Contrast sets ([2004.02709](https://arxiv.org/abs/2004.02709)) and counterfactual augmentation evaluate or regularize robustness. The gap: minimal pairs as a *self-curriculum operator for update localization* in CL.
- **Cheapest first test:** Self-generated rule-learning tasks on 0.5B with LoRA. Arms at equal tokens: tasks only, tasks + random negatives, tasks + minimal pairs. Kill if minimal pairs don't reduce forgetting on 5 earlier rule families.
- **Old-task retention:** Accuracy on earlier rule families.
- **Risk / likely tie:** May act like generic data augmentation; the random-negatives arm controls for that.

### OE18 · Task homotopy bridges
- **Primitive:** when the learner invents a task far from its current skills, the proposer also invents a *path* of intermediate tasks from an old task to the new one, and trains along it so the old task stays in the basin.
- **Mechanism:** Tasks have a parameter (code or env params). The proposer builds a path t_old → t_new with steps sized so the solver stays above a success threshold on both endpoints. A bridge is useful if old-task retention after the path beats direct training at equal steps.
- **Nearest prior / gap:** Gradual domain adaptation ([2002.11361](https://arxiv.org/abs/2002.11361)) uses intermediate domains for *adaptation*; POET transfers agents between paired environments; reverse curriculum ([1707.05300](https://arxiv.org/abs/1707.05300)) moves start states. The gap: self-invented paths chosen for *retention of the starting task*.
- **Cheapest first test:** Parametric control tasks (e.g., varying physics) with a PPO agent. Arms: direct training on t_new, random intermediates, homotopy bridge. Kill if bridge retention of t_old equals direct training.
- **Old-task retention:** Return on t_old after reaching t_new.
- **Risk / likely tie:** Bridges may help only by being more training on near-old tasks; equal-step control handles it.

### OE19 · Compositional rehearsal: new tasks that call old skills
- **Primitive:** each invented task declares which old skills it *calls*, and the scheduler guarantees every old skill is called within its measured half-life. Rehearsal is carried inside new tasks; nothing is replayed.
- **Mechanism:** Tasks are compositions over a skill library (Voyager-style). The proposer is constrained to "one new primitive plus old calls". A half-life estimate per skill sets how soon it must be called again; the proposer is penalized when a skill goes uncalled past it.
- **Nearest prior / gap:** Voyager composes skills from a code library (retention by storage); compositional curricula exist. The gap: composition as the *rehearsal carrier* in weights, with a half-life-driven call schedule.
- **Cheapest first test:** Program-synthesis or crafting tasks with a 0.5B LM solving in weights (no library in context). Arms at equal steps: replay of old tasks, unconstrained invention, compositional rehearsal. Kill if compositional rehearsal ties replay on solo old-skill tests.
- **Old-task retention:** Solo tests of each old skill.
- **Risk / likely tie:** Called skills may be solved through shortcuts that don't exercise the solo skill.

### OE20 · Edge-of-basin mutational rehearsal
- **Primitive:** rehearse old tasks through *mutants at the edge of their basin* (where the current solver is borderline) instead of exact replay: the proposer mutates old tasks, not only new ones.
- **Mechanism:** For each old family, mutate (ACCEL-style edits) until the solver's success is near 50%; train on those. Exact replay is never used. Mutants are re-centred on the original family by a check that the original still passes.
- **Nearest prior / gap:** ACCEL mutates levels to raise regret on the *current* frontier; MIR replays maximally interfered samples. The gap: mutation aimed at the boundary of *old* skills as a replay format.
- **Cheapest first test:** MiniGrid families with a PPO agent. Arms at equal steps: exact replay, MIR, random mutation replay, edge-of-basin mutation. Kill if edge mutants don't beat exact replay on held-out variants of old families.
- **Old-task retention:** Success on original and held-out variant instances of old families.
- **Risk / likely tie:** Uniform per #119; the test includes uniform replay.

### OE21 · Self-lesion curriculum
- **Primitive:** the learner invents *damage to itself* (masking, noise, rank cuts on chosen layers) as tasks and practises recovering its old skills from the damage, making old skills fast to relearn after later forgetting.
- **Mechanism:** Periodically, the proposer picks a lesion; the solver recovers on a small old-task budget; the proposer is rewarded for lesions that are recoverable but costly. Over time skills are stored in forms that recover fast.
- **Nearest prior / gap:** Dropout and SAM regularize; OML ([1905.12588](https://arxiv.org/abs/1905.12588)) and MER ([1810.11910](https://arxiv.org/abs/1810.11910)) meta-learn non-interference; relearning attacks show fast recovery. The gap: self-chosen lesions as an open-ended task class for *fast relearning*. Top-10 #5 (relearning as read head) is a channel; this is a curriculum.
- **Cheapest first test:** MLP on 5 tasks then 5 interfering tasks. Arms: plain, dropout, MER, self-lesion. Kill if self-lesion doesn't cut relearning steps for the first 5 tasks after the interfering phase.
- **Old-task retention:** Accuracy and relearning steps on the first 5 tasks.
- **Risk / likely tie:** May equal noise injection; the random-lesion arm controls for choice.

### OE22 · Interference vaccines
- **Primitive:** for each mastered skill, the proposer invents the task predicted to interfere with it *most*, and the learner trains on small doses of that task together with the skill. Old skills are hardened against future learning the loop has not yet done.
- **Mechanism:** Interference predicted by gradient overlap with the skill's Fisher. Vaccine doses are short; the dose is set so the skill drops by at most ε during the dose and is recovered.
- **Nearest prior / gap:** MER and OML meta-learn for low interference on given streams; PR #119 #10 aims PAIRED at past tasks as a test; adversarial training hardens to input changes. The gap: adversarial *future tasks* invented for vaccination.
- **Cheapest first test:** 5-family stream on MLP or LoRA. Arms: MER, EWC, random-task doses, vaccine doses. Kill if vaccines don't beat random-task doses on retention after unseen interfering tasks.
- **Old-task retention:** Retention after a held-out interfering stream.
- **Risk / likely tie:** MER at equal compute is the strong control.

### OE23 · Concept-level learning progress over library abstractions
- **Primitive:** compute progress and forgetting per *abstraction* in the learner's growing library rather than per task, and choose what to practise by abstraction.
- **Mechanism:** Every task solution is parsed into the library abstractions it uses. LP and decay are tracked per abstraction; the curriculum picks the abstraction with the best signed progress and invents a task that uses it.
- **Nearest prior / gap:** MAGELLAN predicts LP over language goals; DreamCoder grows libraries; #119 closed task-level LP. The gap: a CL unit (abstraction) shared across tasks, so practice on one task counts for every task that uses the abstraction.
- **Cheapest first test:** DreamCoder-lite domain, 100 tasks. Arms: uniform task sampling, task-level ALP, abstraction-level signed LP. Kill if abstraction LP doesn't beat uniform on old-task solve rate.
- **Old-task retention:** Solve rate on the first 30 tasks.
- **Risk / likely tie:** Might restate task-level LP with clustering.

---

## E · Inventing objectives, rules, verifiers and forgetting itself

### OE24 · Discovered retention rules on self-generated random task streams
- **Primitive:** meta-discover a continual-learning update rule (DiscoRL-style) on streams of *random neural tasks the learner generates itself*, then transfer the rule to real streams.
- **Mechanism:** Generate random neural environments or labelling functions (GREMLIN-style) in sequences with controlled interference. Meta-learn an update rule (a small network that maps gradients and state to updates) to maximize final retention plus plasticity. Evaluate on held-out real CL benchmarks.
- **Nearest prior / gap:** GREMLIN discovers RL rules on random neural environments; Discovering RL Algorithms meta-learns update rules; OML and ANML meta-learn representations for CL on given tasks. The gap: rule discovery for *retention* on self-generated streams, so no human task set is needed.
- **Cheapest first test:** Random MLP-labelled tasks, 50 sequences; evaluate on Split-MNIST and permuted MNIST. Arms: SGD, EWC, OML, discovered rule. Kill if the discovered rule doesn't beat EWC on held-out benchmarks.
- **Old-task retention:** Accuracy on all tasks of each held-out sequence.
- **Risk / likely tie:** Rules trained on random tasks may not transfer.

### OE25 · Verifier invention with verifier retention
- **Primitive:** treat *verifiers* as what the open-ended loop invents (new checkers that make new domains trainable) and track their retention separately: a judge that forgets how to grade old tasks breaks the loop even when the solver still passes.
- **Mechanism:** The learner writes checkers (code, rubrics, tests) for domains it cannot yet verify; a checker is kept if it agrees with held-out ground truth on a small calibration set. Each checker carries its calibration set and is re-validated after updates. Three retention axes are reported: proposer, solver, verifier.
- **Nearest prior / gap:** J-Zero trains challenger, solver and judge together; Fragility of Self-Rewarding studies judge drift; #120 covers proposer forgetting. The gap: verifier invention as the open-ended axis and verifier retention as a separate measured axis.
- **Cheapest first test:** 0.5B–1.5B LM writes unit tests for new code families. Arms: fixed verifier, invented verifiers without re-validation, with re-validation. Kill if invented verifiers don't open new families beyond the fixed verifier's coverage.
- **Old-task retention:** Solver success on old families and verifier agreement on old calibration sets.
- **Risk / likely tie:** Small models write weak tests; the test needs a domain where test writing is easy.

### OE26 · Self-chosen forgetting goals
- **Primitive:** add *unlearning* to the learner's own goal space: it may set goals of the form "become unable to do X" for self-invented skills it predicts it won't need, to free capacity for new invention.
- **Mechanism:** Candidate forget goals are archived skills with no live dependents (no current task calls them). The learner unlearns one (gradient ascent or masking) and is rewarded by the following rise in LP on new tasks. Unlearned skills keep their task key (OE01) so they can be regrown.
- **Nearest prior / gap:** Reachability GC (programs-weights P33) and planned forgetting retire unused knowledge; machine unlearning removes data on request. The gap: forgetting as an *intrinsic goal* in an autotelic loop, paid by later plasticity, with regrowability as the safety rule.
- **Cheapest first test:** Small-capacity MLP or LoRA rank 4 on a long invented stream. Arms: no forgetting, random forgetting, dependency-aware forgetting goals. Kill if forgetting goals don't raise new-task learning speed at equal capacity.
- **Old-task retention:** Retention of skills with live dependents, and regrowth cost of forgotten ones.
- **Risk / likely tie:** Unlearning can damage dependents; the dependency check must be behavioural.

### OE27 · Promissory tasks: self-forecast learnability
- **Primitive:** the learner invents tasks it can't solve yet *with a forecast of when it will* (in training steps), and is rewarded for calibrated forecasts. Its curriculum becomes a set of promises about its own learning curve.
- **Mechanism:** Each promissory task has a deadline from the learner's forecast. When it comes due, the outcome scores the forecast (proper scoring rule). Forecast errors flag either unexpected forgetting (forecast for an old-related task fails) or unexpected transfer.
- **Nearest prior / gap:** MAGELLAN predicts LP; CURIO forecasts value of exploration. The gap: long-horizon forecasts of solve time as the task currency, with forecast failures as a forgetting signal.
- **Cheapest first test:** Arithmetic-program tasks of graded difficulty, 0.5B LM. Arms: no forecasts, MAGELLAN-style LP prediction, promissory tasks. Kill if forecasts are no better than a difficulty-only baseline.
- **Old-task retention:** Accuracy on early tasks; correlation of forecast misses with measured forgetting.
- **Risk / likely tie:** Forecasting may be easy for smooth curricula; test needs varied interference.

### OE28 · World-law charter: re-test only what depends on a changed law
- **Primitive:** the environment generator keeps an explicit set of *laws* (invariants) that every invented world obeys; each mastered skill records which laws it depends on; changing a law is an amendment that triggers retention tests only for dependent skills.
- **Mechanism:** Worlds are code with declared invariants (gravity direction, object permanence, tool semantics). Skill–law dependence is measured by evaluating the skill in worlds where one law is flipped. An amendment re-tests and rehearses only dependent skills.
- **Nearest prior / gap:** OMNI-EPIC writes worlds in code without declared laws; CE08 (cultural evolution) handles self-amendment of rules symbolically. The gap: law-dependency of *learned skills* as the unit of retention testing in an invented world.
- **Cheapest first test:** 2D physics worlds with 5 toggleable laws, 10 skills. Arms: re-test everything, random subset, law-dependent subset at equal test budget. Kill if law-dependent testing doesn't catch more forgotten skills per test.
- **Old-task retention:** Success of all skills after 3 amendments.
- **Risk / likely tie:** Dependency maps may be dense.

### OE29 · Invariance-violating task invention
- **Primitive:** invent tasks by finding an invariance the solver has implicitly learned (measured by equivariance probes) and generating a world where that invariance fails. New tasks come from the learner's own assumptions.
- **Mechanism:** Probe the solver for invariances (e.g., output unchanged under colour swap, position shift). Choose the strongest; generate worlds where it breaks. Keep the old worlds where it holds as retention tests, so the learner must condition rather than drop the invariance.
- **Nearest prior / gap:** Adversarial example search breaks invariances to attack; PAIRED maximizes regret without naming the assumption. The gap: probing learned invariances as the task generator.
- **Cheapest first test:** Visual gridworld agent, 5 candidate invariances. Arms: random task generation, PAIRED, invariance-violating generation. Kill if it doesn't produce higher-LP tasks than random.
- **Old-task retention:** Success in worlds where each invariance holds.
- **Risk / likely tie:** Probes may find trivial invariances.

### OE30 · Diff-conditioned task generation
- **Primitive:** after each update, a proposer *reads the weight change* ΔW and generates tasks targeting behaviours ΔW affects. Tasks come from the learner's own weight diff.
- **Mechanism:** A weight-space encoder (trained on pairs of LoRA deltas and behaviour changes) maps ΔW to a description of affected behaviours; the proposer turns it into probes. Probes that show regressions trigger rehearsal.
- **Nearest prior / gap:** Weight-space learning and model diffing predict properties from weights; regression test selection uses code diffs. The gap: weight-diff-conditioned *task generation* inside the loop.
- **Cheapest first test:** LoRA updates on a 0.5B model over 10 families. Arms: random probes, probes from data diff, probes from weight diff. Kill if weight-diff probes don't find regressions faster than random.
- **Old-task retention:** Regression detection rate and final old-family accuracy.
- **Risk / likely tie:** Encoder needs much training data.

### OE31 · Niche-capacity ecology inside one network
- **Primitive:** give each invented task niche (family) a parameter budget inside one network and let niches compete for capacity by their measured use; an ecology decides what stays, instead of a fixed protection rule.
- **Mechanism:** Niches own sub-masks (PackNet-style). Capacity is reallocated by an ecological rule (niches with high call rate and high LP grow; idle ones shrink but keep a seed mask). A new niche needs free capacity, which forces shrinking.
- **Nearest prior / gap:** PackNet ([1711.05769](https://arxiv.org/abs/1711.05769)) and HAT allocate fixed masks per task; MoE routes; POET pairs niches with agents. The gap: competitive, use-driven capacity dynamics inside a single learner in an open-ended loop.
- **Cheapest first test:** MLP on 30 invented families with capacity for 10. Arms: PackNet with first-come allocation, random reallocation, ecology. Kill if ecology doesn't beat PackNet on worst-family success at the end.
- **Old-task retention:** Per-family success.
- **Risk / likely tie:** Close to population routing; stays inside one network to avoid the population branch.

### OE32 · Archive frontier vs retention: the open-ended CL trade-off curve
- **Primitive:** a measured *trade-off curve* between archive growth rate (new solvable tasks per step) and retention (fraction of archive still solved), obtained by sweeping the proposer's drive, to test whether open-endedness and retention trade off along a fixed curve or whether some drives move the curve.
- **Mechanism:** Run the same open-ended loop under many drives (learnability, novelty, OE06, OE10, OE11). For each, plot growth against retention. A drive is a primitive only if it moves the curve, not just along it.
- **Nearest prior / gap:** An Information-Theoretic Definition for Open-Ended Learning defines open-endedness; Are Self-Evolving Agents Continual Learners? measures forgetting in self-evolution. The gap: the joint curve as the yardstick for every card in this root.
- **Cheapest first test:** Shared harness for OE06/OE10/OE11 in the same host. Kill if all drives fall on one curve within noise (then only the curve matters).
- **Old-task retention:** It is the retention axis.
- **Risk / likely tie:** A measurement, not a mechanism; included as the shared yardstick.

---

## Ranked deeper questions

1. **Can an open-ended learner store skills as things that regenerate them, and regrow cheaper than replay? (OE01, OE02, OE03, OE04, OE05)**
   Task keys, skill rewards, world archives and compiled worlds all replace stored data with a regenerator the learner invented. Build one host (MiniGrid or procedural code tasks) with equal storage bytes and equal rehearsal compute, and compare stored-episode replay, distillation from a snapshot and each regenerator. Drop the line if no regenerator beats stored replay on fresh instances of old families.
2. **Can a drive make exploration and rehearsal the same act without losing to uniform? (OE06, OE08, OE10, OE11, OE32)**
   Ledger #119 says every LP selector loses to uniform and only a total-competence oracle wins. Lapse-based novelty, signed frontier value, gradient-subspace novelty and a learned learner-dynamics model are four ways to count "forgotten" as "worth doing". Test all in #119's host plus a nonlinear host and report them on OE32's growth–retention curve. Drop the line if none beats uniform on worst-family retention.
3. **Do self-invented goals, sensors and intentions survive the learner's own representation drift? (OE13, OE14, OE15)**
   Every open-ended learner invents goals in a space its training moves. Test whether phase-1 latent goals still mean the same thing in phase 3, and whether anchor re-grounding fixes it better than a frozen goal encoder that blocks new goals.
4. **Can the curriculum shape the weight geometry so that learning is additive? (OE10, OE17, OE18, OE21, OE22)**
   Gradient-subspace novelty, minimal pairs, homotopy bridges, self-lesions and interference vaccines all move the job of avoiding interference from the optimizer to the task inventor. Test each against the optimizer-side control it replaces (GPM, augmentation, direct training, dropout, MER) at equal compute.
