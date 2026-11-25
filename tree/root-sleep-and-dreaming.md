# Root: Sleep, Dreaming, and Offline Continual Learning

Root node (depth 0) · 32 candidate primitives · Ideas only; no experiments run

**Thesis.** A learner with no new evidence overnight cannot discover which of two observationally equivalent worlds it inhabits. It can still learn something useful: a policy that works in both, a question that separates them, or a skill that survives when two previously separate settings meet. The distinction is between replaying an episode and constructing an executable rehearsal world where several continuations can be tried without acting on the real world. Sleep can also put several incompatible intermediate learning states behind one deployment boundary. The primitives here are operations on worlds, trajectories, phase boundaries, and what survives them.

## What this root is not

The [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) requires a new object or operation and retention in the first test. The [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md) already covers optimizer-state manipulations, meters and observability, token retirement, and teaching markets; none is a proposed mechanism here. The [cognitive-science flood](https://github.com/manojbajaj95/cl/blob/devin/1795539368-cogsci-flood/ideas/flood/cogsci.md) already has two-stage replay/recombination, old-world imagination, narrative replay, and nap-frequency sweeps (C39/C43/C64/C62). The [brain root](https://github.com/manojbajaj95/cl/pull/308) already has bridge stitching, homeostatic downscaling, phase-gated writes, and reverse credit replay. The [synchronizing consolidation node](https://github.com/manojbajaj95/cl/blob/c3469a061e75964fcece8366ef673d90a2fd8a83/tree/synchronizing-consolidation.md) asks for a common update word that coalesces edit states; here competing worlds or paths can remain distinct indefinitely. No card needs self-authored questions to beat teacher-authored questions ([#8](https://github.com/manojbajaj95/cl/pull/8)), repeated consolidation to oscillate, or repeated fold-in to erode correctability ([#30](https://github.com/manojbajaj95/cl/pull/30)).

**Literature check.** AlphaXiv discovery and Hugging Face paper search surfaced recent work; comparisons use arXiv/publisher abstracts and paper summaries for the closest matches. Novelty is a hypothesis about the operation, not a claim of exhaustive precedence. Ordinary [wake–sleep](https://www.science.org/doi/10.1126/science.7761831) and [Reweighted Wake–Sleep](https://arxiv.org/abs/1406.2751) train recognition/generation in complementary directions. [Deep Generative Replay](https://arxiv.org/abs/1705.08690) synthesizes old examples; [sleep-like unsupervised replay](https://www.nature.com/articles/s41467-022-34938-7) uses noise and Hebbian plasticity to recover old tasks. [Language Models Need Sleep](https://arxiv.org/abs/2606.03979) distills contexts with replay and iterates on self-training examples. [Do Agents Need to Sleep?](https://arxiv.org/abs/2611.02216) proposes ringing, resonance, and renormalization for digital memory. Neither naming two stages NREM/REM nor changing the amount or source of replay is a new primitive.

**Shared CPU-first protocol.** Use a tabular agent, a finite grammar, or a tiny classifier; start with two ordinary old tasks (one rare) and later expose a new task. Lock the old held-out cases, wake stream, and scoring before sleep. Dreams may use only wake-derived rules, logs, and declared structural assumptions, never held-out behavior or hidden simulator truth. A hand-written toy can demonstrate separation under known rules first; repeat with fitted rules and controlled misspecification before making a learning claim. Charge branching, rejected dreams, verifier calls, retained state, and serving downtime. Include no sleep, real replay, fixed-generator or equal-format replay, and the named matched control; where a structured object is proposed, also give a flat learner the same generated transitions or constraints. Compare old retention at matched new performance and new performance at matched retention. Test the normal awake interface without privileged task labels, before and after sleep and after subsequent interference. Each card names an extra old-task slice; it does not replace this common check.

## A · Build worlds you can operate on

### SD01 · Replay a square, not four worlds
- **Mechanism:** Fit two local rule edits from wake data. Generate a square with one edit per edge and execute both orders with coupled seeds. Export the equality of the resulting behaviors where justified, and paired divergent traces where the edits interact.
- **Nearest prior / gap:** [DiCode (2602.08194)](https://arxiv.org/abs/2602.08194) generates executable world variants for curriculum progression. The proposed object is the commuting or noncommuting square of interventions, not any of its worlds.
- **Cheapest first test:** Learn door-latch and key-consumption edits in a tiny maze. Compare square supervision against the same four executions shuffled; hold out a new maze layout with one interaction.
- **Old-task retention:** Score both single-edit worlds and the original maze, including old routes that still consume keys.

### SD02 · Glue worlds by what crosses the seam
- **Mechanism:** Join two learned simulators on a boundary by negotiating a state map and its preconditions. Carry resources, hidden commitments, and their updates across the seam; reject a join if no map preserves both sides' interface rules.
- **Nearest prior / gap:** [Generative Trajectory Stitching (2503.05153)](https://arxiv.org/abs/2503.05153) composes trajectory pieces with diffusion. A reusable interface mapping changes which continuations exist for *any* policy crossing the seam.
- **Cheapest first test:** Join two tabular warehouses with different units and a capacity constraint. Compare endpoint stitching and the same joined trajectories; hold out a third load and a new route.
- **Old-task retention:** Run each original warehouse independently, including near-capacity delivery jobs.

### SD03 · Rehearse on a quotient, then explicitly lift
- **Mechanism:** Build a smaller rehearsal world by identifying states with matching locally tested transition laws. Train on that quotient and lift episodes back through multiple concrete realizations; if one fails, split that equivalence class instead of changing its label globally.
- **Nearest prior / gap:** [Projection Abstractions in Planning (2412.02615)](https://arxiv.org/abs/2412.02615) connects planning abstractions and MDP homomorphisms. Abstraction refinement itself is not new; the question is whether learning in a fitted quotient and lifting across *old and new* realizations can preserve rare exceptions across continual shifts at lower cost than working in the full worlds.
- **Cheapest first test:** Compress grid rooms by exit topology, with one door depending on room history. Compare a fixed learned abstraction and an equal-step concrete simulator.
- **Old-task retention:** Test old rooms omitted from quotient training, especially the locking-door room and its visually identical neighbor.

### SD04 · Insert clock time without inserting decisions
- **Mechanism:** Generate worlds by inserting action-free waits while letting selected background processes advance. Rehearse policies on matched decision sequences before and after this dilation; a wait is an intervention on elapsed time, not another sampled action.
- **Nearest prior / gap:** [Domain Randomization (1703.06907)](https://arxiv.org/abs/1703.06907) varies simulator parameters for transfer. This generates paired trajectories by changing the map from decision count to physical time, with the action sequence fixed across the pair.
- **Cheapest first test:** In a queue toy, food spoils by clock time but batteries drain by action. Compare independent delay randomization and matched dilation pairs on unseen wait patterns.
- **Old-task retention:** Re-run original short jobs and the old deadline-sensitive job on unmodified clocks.

### SD05 · Rewrite a law while fixing the exogenous draw
- **Mechanism:** Infer plausible hidden draws for an observed episode, substitute one local transition law, and execute both versions under shared draws. Consolidate the response *to the substitution*, not the substituted outcome as a fact about wake.
- **Nearest prior / gap:** [Counterfactual Data Augmentation Under Confounding (2305.18183)](https://arxiv.org/abs/2305.18183) generates counterfactual examples to remove confounding. The proposed target is a reusable multi-step policy response to swapping a specific dynamical mechanism.
- **Cheapest first test:** Change a precedence rule in a tiny dispatcher while preserving job arrivals. Compare independently sampled worlds and paired rollouts without the law identifier.
- **Old-task retention:** Score legacy dispatch orders on the original precedence rule, including rare tied arrivals.

### SD06 · Dream a set of worlds, never the average world
- **Mechanism:** Keep multiple transition tables that fit the same wake trace. Compile a policy only for prefixes executable in all of them; where safe actions diverge, export a conditional policy with a genuinely informative first action.
- **Nearest prior / gap:** [Probabilistic Dreaming (2603.04715)](https://arxiv.org/abs/2603.04715) retains distinct latent futures, and [Lexpop (2602.08734)](https://arxiv.org/abs/2602.08734) extracts finite-state controllers for hidden-model POMDPs. The bet is to consolidate a reusable agreement prefix and distinguishing branch from wake-consistent laws without a probability over those laws; the value must come from reusing the parts as laws recur or change, not from rediscovering contingent planning.
- **Cheapest first test:** Fit observational twins for two hidden valve rules, then add a third. Compare ensemble-average, robust hidden-model planning from scratch, and partial policy reuse with equal model knowledge; charge fitting and planning across both sleeps.
- **Old-task retention:** Test both familiar valve settings and old routes that do not require any identifying action.

### SD07 · Rehearse a law and its smallest exception
- **Mechanism:** Generate a pair of worlds differing in one executable rule. Use a solver to find the shortest continuation where the optimum differs; store the witness as a guard on the learned procedure, not as a universal negative.
- **Nearest prior / gap:** [DiCode (2602.08194)](https://arxiv.org/abs/2602.08194) edits environment code to scaffold skill; [MemDream (2609.34545)](https://arxiv.org/abs/2609.34545) probes and repairs memories. Here one rule edit and its distinguishing continuation jointly define a reusable skill guard.
- **Cheapest first test:** Synthesize a default and a permit exception in a 12-state planning grammar; compare random hard negatives and a flat guard classifier on the same witnesses.
- **Old-task retention:** Test the old default on unrelated cases and the original exception on longer trajectories.

### SD08 · Move an exception without moving its scenery
- **Mechanism:** Extract a guarded interaction from one fitted world and instantiate it under correspondences in another; any nonportable precondition remains explicit. Rehearse two transferred versions, one where the guard applies and one where it does not.
- **Nearest prior / gap:** [Discovery by Dreaming (2607.16256)](https://arxiv.org/abs/2607.16256) recombines knowledge across domains. The bet is on a transplant of *executable transitions with preconditions* that can remain only partially defined after the move.
- **Cheapest first test:** Transplant a “return reusable container before reorder” rule from inventory to a finite lending world, versus unrestricted cross-world recombination.
- **Old-task retention:** Run original returns and ordinary lending cases where the transplanted rule is inapplicable.

## B · Learn from relationships between trajectories

### SD09 · Play two histories from the same observation
- **Mechanism:** Generate pairs with identical visible state but distinct reachable histories, and hold actions fixed up to the first consequence that separates them. Train a finite-state policy to carry the minimum history distinction that changes subsequent action.
- **Nearest prior / gap:** [Decision Transformer (2106.01345)](https://arxiv.org/abs/2106.01345) conditions action on sequences. This intervention creates matched history swaps specifically to teach a history-dependent decision rather than infer it from incidental sequence coverage.
- **Cheapest first test:** A card reader looks identical after differently colored prior signals; compare ordinary rollout replay and the same unpaired examples on held-out intervening distractors.
- **Old-task retention:** Score old signal sequences and old fully observed access tasks without new history hints.

### SD10 · Rehearse handovers, not only complete skills
- **Mechanism:** Roll out old and new policies to a checkpoint, then cross-run each policy's continuation from both reachable states. Learn a handover operator that changes only what's needed to make the recipient's continuation valid.
- **Nearest prior / gap:** [When Robots Sleep (2606.17493)](https://arxiv.org/abs/2606.17493) consolidates frozen skill memories into a shared policy and measures skill coupling. Here a handover is explicit training data from cross-policy start states, with a learned repair action.
- **Cheapest first test:** Two grid delivery policies park carts on different sides. Compare joint replay and unordered boundary starts with equal rollout budgets; require a successful unseen handover.
- **Old-task retention:** Test both original end-to-end deliveries plus old handovers whose states were already compatible.

### SD11 · Rehearse what the continuation assumes
- **Mechanism:** For each historical action prefix, replace the original suffix with two plausible follow-on tasks that need different resources. Train prefixes to preserve common options before the next task is known, without pretending those continuations occurred.
- **Nearest prior / gap:** [Elastic Decision Transformer (2307.02484)](https://arxiv.org/abs/2307.02484) adapts how much history conditions action to stitch behavior. This changes which future tasks a shared prefix leaves feasible, not which history window conditions a fixed task.
- **Cheapest first test:** In a depot, a route can consume the last battery before a future delivery type is announced. Compare pooled trajectory replay and task-conditioned policies with discovery delayed equally.
- **Old-task retention:** Recheck old battery-intensive deliveries, including cases where spending the last battery is correct.

### SD12 · Rehearse the same intent across an action remapping
- **Mechanism:** Build a family of reversible action encodings from inferred tool equivalences. Keep the goal and world fixed while replaying a plan under each encoding; learn an intermediate action representation that can be rendered to each interface.
- **Nearest prior / gap:** [REGEN (2606.27374)](https://arxiv.org/abs/2606.27374) creates old-task trajectories from prior instructions and observations. The proposed paired operator acts on the action language itself, with round-trip equality of actual effects.
- **Cheapest first test:** Use mutually invertible command grammars for a grid API and hold out one composition of commands. Compare ordinary relabeling and unpaired mixed-interface replay at the same transition count.
- **Old-task retention:** Run legacy command sequences, including ambiguous surface verbs that have different effects under the old API.

### SD13 · Learn to intervene from a set of possible pasts
- **Mechanism:** Work backward from a logged terminal observation to all compatible predecessor histories in a fitted world; then roll forward with a new action from each. Train interventions that succeed across the predecessor set rather than choosing the most plausible reconstructed history.
- **Nearest prior / gap:** [Probabilistic Dreaming (2603.04715)](https://arxiv.org/abs/2603.04715) carries multiple future particles. This rehearsal starts from ambiguity about what *already happened* and makes action labels invariant to incompatible prehistories.
- **Cheapest first test:** End at the same display reading with two hidden machine configurations. Compare MAP reconstruction and forward uncertainty rollouts with matched particle counts.
- **Old-task retention:** Test ordinary forward sequences, including an old case where observing the earlier action makes a specialized repair safe.

### SD14 · Convert a broken abstraction into a distinguishing action
- **Mechanism:** When two states share a compressed signature but require different actions, dream a shortest real-world action prefix whose observable result separates them. Train the agent to execute that prefix rather than use a hidden simulator label.
- **Nearest prior / gap:** [Dream Rehearsal (2607.19749)](https://arxiv.org/abs/2607.19749) uses world-model-graded dreams for self-imitation; [MemDream (2609.34545)](https://arxiv.org/abs/2609.34545) generates memory probes. The output here is an executable, branching sensing procedure for a single fitted world and aliased states.
- **Cheapest first test:** In a two-key maze, let a safe test action reveal which key is being held. Compare uncertainty-penalized policy replay and random probing on longer layouts.
- **Old-task retention:** Re-run unambiguous old locks and old cases with the clue already visible; unnecessary probes count as failures if they violate the old deadline.

### SD15 · Pair dreams with the same ending and different causes
- **Mechanism:** Generate matched terminal successes, one caused by the agent's action and one by a background rescue that would occur anyway. Consolidate the action only where the coupled intervention changes the ending; preserve the pair as supervision for when to act.
- **Nearest prior / gap:** [Dream Rehearsal (2607.19749)](https://arxiv.org/abs/2607.19749) grades imagined trajectories for self-imitation. This compares action replacements under a shared exogenous draw even when both factual rollouts are successful.
- **Cheapest first test:** Tiny sorting world with occasional automatic resets. Compare return-graded self-imitation and advantage distillation using the same model and samples; kill if ordinary advantages capture the full effect.
- **Old-task retention:** Test the original no-rescue world and legacy cases where waiting for a reset is actually optimal.

### SD16 · Rehearse a repair loop, not the corrected ending
- **Mechanism:** Corrupt an internal state along a dream trajectory with a plausible execution error, and train a loop that returns to a viable state without resetting completed work. Require the subsequent continuation to remain valid.
- **Nearest prior / gap:** [Electric Sheep (2403.07979)](https://arxiv.org/abs/2403.07979) augments predicted episodes for generalization. The new object is a reusable recovery loop semantically anchored to a valid suffix, not a noisier episode.
- **Cheapest first test:** In a three-step assembly grammar, alter the second component and dream rework paths. Compare augmented replay and the same corrections trained without a shared continuation.
- **Old-task retention:** Test clean assembly and the original recovery paths where restarting is the only valid response.

## C · Give the offline schedule semantics

### SD17 · Seal a whole revision behind one dawn
- **Mechanism:** Consolidate an enabling rule and its exception as one publication unit. A running episode keeps its original policy until a natural boundary; the next episode sees both changes or neither.
- **Nearest prior / gap:** [SIESTA (2303.10725)](https://arxiv.org/abs/2303.10725) separates fast wake updates from offline rehearsal. This adds a composable visibility contract for overlapping episodes, not a prescription for how often to sleep.
- **Cheapest first test:** Update a tool's units and two dependent procedures during a two-turn delivery. Compare micro-sleep and ordinary atomic model replacement at the same downtime; only claim a primitive if pinning across calls matters.
- **Old-task retention:** Include old jobs crossing the update and old jobs that start after it, with no explicit version selector from the user.

### SD18 · Schedule by which intermediate artifacts exist
- **Mechanism:** Offline passes produce typed artifacts, such as an executable world patch or a suffix policy. Passes can consume compatible artifacts but cannot consume a draft as if it were a resolved transition rule. Schedule the dependency graph, not a fixed list of phase names.
- **Nearest prior / gap:** [GAPT (2505.08727)](https://arxiv.org/abs/2505.08727) switches between memorization and compression objectives. This schedule follows producer–consumer dependencies between heterogeneous artifacts and can interleave independently ready work.
- **Cheapest first test:** Feed two changing tool rules and a dependent composite under interrupted sleep; compare the best fixed ordering and ordinary prioritized rehearsal with equal available work.
- **Old-task retention:** Exercise old composites under both tools after each interruption and after the full graph completes.

### SD19 · Resume a dream with a new suffix, not a silently changed premise
- **Mechanism:** Save an interrupted branch with its explicit world assumptions. If wake experience changes them, retain the valid prefix and regenerate from the first invalid transition; pin an entire old branch only when there is no valid seam.
- **Nearest prior / gap:** [Dream-RSI (2609.14858)](https://arxiv.org/abs/2609.14858) dreams over historical discovery trees to improve exploration. The proposed operation repairs open imagined branches against changed world rules before reuse, rather than just expanding an experience tree.
- **Cheapest first test:** Interrupt planning in a maze, then observe a change to one door. Match saved bytes and replay work against complete restart and reuse of all branches. Include one update that forces a full restart.
- **Old-task retention:** Test unchanged old routes through other doors and old task goals with alternate routes through the affected room.

### SD20 · Sleep with the next shift hidden
- **Mechanism:** Partition a sleep epoch into an irreversible representation commitment and a later specialization phase. Between them reveal which of several previously learned settings is returning; only the specialization may use that setting cue.
- **Nearest prior / gap:** [Offline Recurrence (2605.26099)](https://arxiv.org/abs/2605.26099) consolidates accumulated context into fast weights before clearing the cache. The new contract is a reveal boundary that forces a single compact carrier to support several possible awakenings.
- **Cheapest first test:** Learn three tiny dialects, choose a memory representation under a bit budget, then reveal a wake example. Compare shared replay with the same reveal and best equal-byte mixture of dialect summaries.
- **Old-task retention:** Score all three dialects in counterbalanced awakenings, including the one rarely selected during training.

### SD21 · Close a dream when its evidence arrives, not when the night ends
- **Mechanism:** A sleep pass can produce conditional lessons indexed by mutually exclusive outcomes of a real pending event. When the outcome reaches the next sleep epoch, bind it to the matching lesson; dreams alone cannot choose the branch.
- **Nearest prior / gap:** [ENGRAM (2611.09472)](https://arxiv.org/abs/2611.09472) separates training admission from verified release. Here the expensive object generated ahead of time is a *contingent curriculum*, with a later externally observed outcome choosing its meaning.
- **Cheapest first test:** A grid tool's update is announced but its behavior is revealed after a busy shift; compare deferred generation and robust-only training at the same final compute, tracking learning by the first wake deadline.
- **Old-task retention:** Test unchanged old tool actions, and ensure the unobserved branch never takes effect on unaffected legacy jobs.

### SD22 · Open a second rehearsal clock for actions already in flight
- **Mechanism:** Protect outstanding multi-turn obligations by explicitly replaying the remaining suffixes from their current states in one rehearsal stream, while a separate stream rehearses complete future instances. Commit a shared policy only if it can choose correctly from both kinds of state without an episode-version tag.
- **Nearest prior / gap:** [Hippocam (2610.12124)](https://arxiv.org/abs/2610.12124) preserves state needed for later work through nested intents; [SRT (2608.17530)](https://arxiv.org/abs/2608.17530) sets per-sample review times. This schedules *suffixes of outstanding obligations* with real deadlines rather than examples by age, and learns one successor policy rather than pinning old versions.
- **Cheapest first test:** Start two finite booking jobs before a schema update. Compare whole-job replay, same suffixes sampled without deadlines, and pinned old versions at equal bytes. Allow the proposed policy to fail if the normal state cannot identify obligations.
- **Old-task retention:** Score the completion of in-flight old jobs and the success of fresh jobs using still-live old rules.

### SD23 · Rehearse through a scheduled loss of a dependency
- **Mechanism:** Insert an interval into an otherwise faithful dream during which one usual source of information is absent. Rehearse a three-part handoff: what to acquire before the blackout, what to do while the source is absent, and what to reconcile when it returns.
- **Nearest prior / gap:** [Dropout's Dream Land (2109.08342)](https://arxiv.org/abs/2109.08342) varies learned simulators with dropout to improve transfer to reality. Here the phase schedule removes a specific interface with known start and end events; the learned object carries information across both boundaries rather than making every action robust to random dropout.
- **Cheapest first test:** A finite dispatch agent loses live inventory during a known migration window while manifests remain readable before and after. Compare random interface dropout and a hand-coded cache, charging reads and retained state.
- **Old-task retention:** Run old dispatch jobs with no blackout and old jobs spanning the blackout whose items must be rechecked on return.

### SD24 · Alternate world fitting and policy teaching across disjoint nights
- **Mechanism:** One sleep phase fits a world patch from a wake partition; another uses separately logged outcomes to define when that patch can label a rollout. No synthetic event can travel back into the evidence pool that licensed its world rule.
- **Nearest prior / gap:** [Reweighted Wake–Sleep (1406.2751)](https://arxiv.org/abs/1406.2751) uses different distributions for recognition/generation updates; [MemDream (2609.34545)](https://arxiv.org/abs/2609.34545) separates probing, diagnosis, and editing roles. Here admissible information flow between phases is part of the rehearsal operation, not a different teacher or a scalar gate.
- **Cheapest first test:** Fit an incorrect shortcut from correlated cues in one of two small streams. Compare pooled fitting, simple cross-validation followed by joint replay, and the one-way evidence schedule with identical examples and compute.
- **Old-task retention:** Score both old streams, especially valid old shortcuts sharing the spurious cue.

## D · Change what a dream leaves behind

### SD25 · Distill a dream into a skill with a rescue continuation
- **Mechanism:** The offline teacher emits two linked procedures: a fast nominal policy and a recovery continuation it can call when the current execution no longer satisfies its preconditions. Train the call and return on generated failures.
- **Nearest prior / gap:** [Option-Critic (1609.05140)](https://arxiv.org/abs/1609.05140) learns skill policies and termination conditions; [SayCan (2204.01691)](https://arxiv.org/abs/2204.01691) selects feasible skills. The bet here is training an explicit repair-and-resume continuation jointly with a particular nominal option, rather than just terminating into the general policy over options.
- **Cheapest first test:** A tiny assembly graph with a reversible fast-path error; compare replanning with primitive actions and independent backup-policy distillation at equal rollout and action budgets.
- **Old-task retention:** Check original procedures with and without their legacy recovery triggers; unnecessary rescue steps count against task success.

### SD26 · Distill safely interchangeable actions as a set
- **Mechanism:** If separate fitted worlds and successful rollouts agree only on an allowable action set, train on the set rather than electing one representative. Later phases may substitute any member without re-labelling the original lesson.
- **Nearest prior / gap:** [Dream Rehearsal (2607.19749)](https://arxiv.org/abs/2607.19749) samples and grades imagined action traces for imitation. This output is a set-valued supervision object carried across shifts, not an averaged policy or a preferred trajectory.
- **Cheapest first test:** A small scheduling grammar with equivalent old actions, one of which becomes unavailable. Compare entropy-regularized imitation and training on all successful actions with equal evidence.
- **Old-task retention:** Check old feasible equivalents and old single-option cases, where broadening the set would be incorrect.

### SD27 · Write the unexecuted goal as an executable test of transfer
- **Mechanism:** Turn a dream continuation into a goal predicate that could be satisfied by multiple distinct plans. Carry the predicate into later sleeps and synthesize a fresh plan for the changed world instead of preserving only the original action trace.
- **Nearest prior / gap:** [Hindsight Experience Replay (1707.01495)](https://arxiv.org/abs/1707.01495) relabels what a rollout actually achieved. This retains a predicate for a continuation that did *not* occur, to be re-solved under future rules.
- **Cheapest first test:** A box-pushing world changes layout after the dream. Compare goal relabeling, keeping the best imagined action trace, and carrying the predicate with the same planning budget.
- **Old-task retention:** Test original goal predicates on old layouts, including old partial successes that must not count as completion.

### SD28 · Make a dream produce an executable invitation to ask
- **Mechanism:** Compile an imagined branch that cannot be decided from the available observations into a bounded question and two lawful next actions. The wake agent asks only at the corresponding reachable state; an answer is real evidence, not dream verification.
- **Nearest prior / gap:** [MemDream (2609.34545)](https://arxiv.org/abs/2609.34545) asks simulated memory queries to repair a graph; [Reflexion (2303.11366)](https://arxiv.org/abs/2303.11366) stores verbal feedback. The proposed output is an executable external query coupled to the competing actions it would resolve.
- **Cheapest first test:** A finite scheduling assistant encounters two indistinguishable user policies; compare generic clarification and disagreement-triggered random questioning at equal query budgets.
- **Old-task retention:** Score routine old requests with enough information to act and old clarification cases phrased differently from the dream.

### SD29 · Consolidate an impossibility into a different goal
- **Mechanism:** When a fitted dream world proves a goal unreachable from a state, construct a nearest achievable goal ordered by which requirements the user declared substitutable. Train a fallback that explains the changed goal and performs it only when permitted.
- **Nearest prior / gap:** [DiCode (2602.08194)](https://arxiv.org/abs/2602.08194) generates feasible progressions by editing the world. Here the world stays fixed and sleep emits a reusable, explicit goal substitution justified by an unreachable continuation.
- **Cheapest first test:** In a finite planning world with a partial order of acceptable destinations, compare a no-op and training on reward-shaped fallback trajectories. Check worlds where a feasible but longer path makes a tempting fallback invalid.
- **Old-task retention:** Re-run ordinary original goals and legacy strict goals for which no substitution is permitted.

### SD30 · Distill a reversible macro, not just a shortcut
- **Mechanism:** Generate a macro and a paired undo procedure in the rehearsal world. Train only interpretations whose forward–undo composite restores task-relevant state across a declared set of starting conditions; other conditions remain outside the macro's domain.
- **Nearest prior / gap:** [Deep Reinforcement Learning With Macro-Actions (1606.04615)](https://arxiv.org/abs/1606.04615) learns with extended actions. Here the macro has an executable partial inverse with its own boundary conditions, tested offline as a pair rather than as two independently useful skills.
- **Cheapest first test:** In a small inventory tool, moving a reserved item is reversible only before shipment. Compare independent forward/undo rehearsal and primitive-action search on unseen inventory combinations.
- **Old-task retention:** Test established undo operations, committed orders that cannot be undone, and ordinary forward-only workflows.

### SD31 · Train on the proof boundary, not the verifier's verdict
- **Mechanism:** Distill a pair of executable histories: a witness that satisfies a temporal obligation and the shortest valid perturbation that breaks it. Export the shared prefix and diverging action as a structured decision rule.
- **Nearest prior / gap:** [Safe RL via Shielding (1708.08611)](https://arxiv.org/abs/1708.08611) synthesizes a reactive shield from a supplied temporal specification. The proposal uses its minimal counterexamples and matched successes as a reusable teaching object for a learner that will not have the shield at wake; the learner will not inherit the shield's guarantee.
- **Cheapest first test:** Teach “reconfirm after an address change” in a 10-state workflow; compare successful demonstrations plus ordinary failed traces and flat training on the same witness pairs.
- **Old-task retention:** Score unchanged-address tasks and old reauthorization rules with similar surface words but different triggering events.

### SD32 · Carry a world rule as a bounded generator of exceptions
- **Mechanism:** Instead of consolidating all exceptions into a classifier, distill a program that enumerates nearby counterexamples to a rule on demand within the next sleep budget. Use those generated exceptions to train the successor, including their precise scope.
- **Nearest prior / gap:** [Dream2Learn (2603.01935)](https://arxiv.org/abs/2603.01935) creates synthetic classes coherent with learned representations; [Auto-Dreamer (2605.20616)](https://arxiv.org/abs/2605.20616) synthesizes a compact replacement for a working memory region. The proposed persistent output is an executable *exception generator*, scored on new exceptions it yields after a subsequent shift, not on compactness or fidelity today.
- **Cheapest first test:** Build a tiny command grammar with scoped precedence exceptions. Match bytes and generation cost against an exemplar bank, a fitted general generator, and an exception list plus the same symbolic search tool.
- **Old-task retention:** Score old exceptions no longer surfaced by current generation and default cases the generator must leave alone.

## Deeper questions, ranked

1. **What can a dream teach that was not already in the wake evidence?** (SD01/05/06/13) Separate identification of the true law from computation of its consequences. Enumerate all laws consistent with one finite wake stream. Compare pooled dreaming, conservative planning, and executable policies that agree until an informative action. Ask whether the latter yields a useful new behavior at a fixed old-task floor without assigning probability mass the evidence cannot support.
2. **Can rehearsal worlds be composed without preserving everything about their origins?** (SD02/03/08/10) Seek the smallest seam state that preserves valid continuations for both sides. Hold out a new seam user and a hidden obligation; compare raw splicing, full simulator composition and learned interface maps, charging state bytes and fitting. A useful interface must transfer beyond the trajectories that defined it.
3. **When does the boundary of sleep matter more than how often the learner sleeps?** (SD17–24) Give all arms identical runnable artifact builders and equal compute, then vary only which intermediate results can be read, which obligations cross dawn, and when new evidence is revealed. Look for a stream where no equally informed, unstructured phase order matches both new acquisition and old in-flight success. If atomic publication with pinned episodes ties, do not claim a new learning mechanism.
4. **What should survive a dream: an action, a constraint, or a generator?** (SD25–32) Train each carrier from the same imagined rollouts, then perturb action vocabulary, affordances, and goal combinations independently. Estimate the bytes and rehearsal episodes needed to recover old behavior and generalize. A carrier earns its keep only if it beats flat training on the same supervision under a change it was not designed around.
