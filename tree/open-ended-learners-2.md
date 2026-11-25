# Open-ended learners 2: competence-tracking archives and skills stored as objectives

Depth 1 · child of [PR #384](https://github.com/manojbajaj95/cl/pull/384) (`tree/root-open-ended-learners.md`) OE06 and OE02 · 26 cards (OE2-01–OE2-26) · 4 ranked deeper questions · Ideas only; no experiments run

**Why the parent's two ideas fall short as written.** The reviewer kept two cards at score 3.
- **(a) Competence-tracking novelty archive (OE06).** Entries carry a cheap probe and become novel again once the learner can no longer produce them, so exploration and rehearsal are one drive.
- **(b) Skill stored as the shortest reward program (OE02).** The stored program regrows the skill when briefly optimized from a perturbed policy, so retention stores an objective.

Both are still *policies about* an archive or a reward. Neither yet says what new object they create.

(a) still uses a hand-designed behaviour descriptor and a hand-set exchange rate between novelty and rehearsal. It also cannot tell *lost* from *latent*, and it has no law predicting how large a repertoire it can hold.

(b) has no rule for *which* skills an objective stores more cheaply than a policy. It doesn't stop a reward program from cheating, for example a reward that just says "imitate the stored trajectory". And it doesn't say what a stored objective buys that a stored policy can't, such as surviving a model or world change.

This node asks those questions and returns objects:
- a descriptor made from competence itself
- graphs of co-lapse and revival
- a queueing law for repertoires
- objective compressibility as a property of a skill
- counterexample-refined rewards
- the archive whose entries *are* reward programs, so one object does both jobs

**Scope.** Inherits the parent's scope and ledger constraints. LP selectors lose to uniform (#119), so every drive card here must beat uniform at equal environment steps. Generator identity doesn't matter ([PR #8](https://github.com/manojbajaj95/cl/pull/8)), and re-derivability memory (LP39, [PR #59](https://github.com/manojbajaj95/cl/pull/59), next tier after the top 10) is the prior for any "store only what is hard to regrow" card. Merge cards follow the ledger rule: they must beat the union of their parts' baselines at equal budget. The node stays a single learner, so no population and no deployed world.

## Literature check

alphaXiv searches (8 new queries, on top of the parent's 16): novelty archives and revisiting, Go-Explore variants, quality diversity in dynamic domains, inverse RL of one's own policy, reward storage in continual RL, LLM-written rewards, reward simplicity and MDL, relearning savings, and successor-feature reward bases.

| Line | Already available | What this node must add |
|---|---|---|
| Archives that revisit | [Go-Explore](https://arxiv.org/abs/1901.10995) and [First return, then explore](https://arxiv.org/abs/2004.12919) return to archived *states*. [Intelligent Go-Explore](https://arxiv.org/abs/2405.15143) uses an FM to judge interestingness. [BR-NS](https://arxiv.org/abs/2104.03936) drops the archive. [Dynamic Quality-Diversity Search](https://arxiv.org/abs/2404.05769) re-evaluates elites when the *environment* changes. [Joint Agent Memory and Exploration via Novelty Signals](https://arxiv.org/abs/2606.01528) couples memory and novelty. [MAP-Elites](https://arxiv.org/abs/1504.04909) and AURORA (Cully 2019) learn descriptors. [CURIOUS](https://arxiv.org/abs/1810.06284) pays absolute LP for forgotten goals. | Dynamic QD re-evaluates because the *world* moved; here the *learner* moved. No archive defines membership or descriptors by the learner's current competence, or reads the archive's lapse pattern as a measurement of the learner. |
| Rewards as skill carriers | [GAIL](https://arxiv.org/abs/1606.03476) and [AIRL](https://arxiv.org/abs/1710.11248) recover rewards from experts; AIRL claims rewards transfer across dynamics. [Successor features](https://arxiv.org/abs/1606.05312), [GPI](https://arxiv.org/abs/1901.10964), the [Option Keyboard](https://arxiv.org/abs/2106.13105) and [spectral successor features for continual RL](https://arxiv.org/abs/2611.26504) build reward bases. [Eureka](https://arxiv.org/abs/2310.12931), [MLREF](https://arxiv.org/abs/2608.18827) (reward-module reuse) and [Causal Reward World Models](https://arxiv.org/abs/2606.23280) write reward code. [EPIC](https://arxiv.org/abs/2006.13900) compares rewards up to shaping. [Habitats](https://arxiv.org/abs/2611.31160) evolves objectives. | All of these use rewards to *produce* behaviour from experts or descriptions. None writes rewards *for its own mastered skills* as the retention format, prices when that beats storing a policy, or refines a reward until regrowth is unique. |
| Continual-RL retention | [Policy Improvement-Guided Replay](https://arxiv.org/abs/2611.25989), [Continual Policy Consolidation](https://arxiv.org/abs/2601.22475), [The World Model Remembers, the Actor Forgets](https://arxiv.org/abs/2607.19749) (dream rehearsal), [Hierarchical Orchestra of Policies](https://arxiv.org/abs/2411.03008) | They store data, policies or world models. None stores objectives. |
| Savings and simplicity | [Binding-Specific Relearning Savings](https://arxiv.org/abs/2610.22381), [Same accuracy, twice as fast](https://arxiv.org/abs/2502.21147), [RL with Simple Sequence Priors](https://arxiv.org/abs/2305.17109) | Savings measure how much is latent; simplicity priors regularize policies. Neither defines the *description-length ratio between a skill's reward and its policy*. |

---

## A · The competence-tracking archive as a measuring instrument

### OE2-01 · Competence signature as the behaviour descriptor
- **Primitive:** replace the hand-designed behaviour descriptor with the *competence signature*: for a new behaviour, the bit vector of which archived probes the learner passes right after producing it. Novelty is Hamming distance in signature space, so the descriptor is made of the learner's own repertoire and changes when the repertoire does.
- **Mechanism:** Each archive entry has a probe. When the agent produces a candidate behaviour, it runs a sampled subset of probes and records the pass/fail vector. Novelty = distance to the k nearest signatures among *currently retained* entries. A lapsed entry flips bits in every signature that included it, so lapse shows up as novelty without a separate rule.
- **Nearest prior / gap:** AURORA and learned MAP-Elites descriptors embed observations; [BR-NS](https://arxiv.org/abs/2104.03936) scores novelty by prediction error; Go-Explore uses cells. The gap: a descriptor whose coordinates are *the learner's own probes*, so novelty is defined relative to what it can do now.
- **Cheapest first test:** #119 linear host and an MLP host with 20 goal families, plus MiniGrid with 30 goal types. Arms at equal environment steps: uniform, CURIOUS ALP, permanent-archive novelty with hand descriptors, OE06 lapse archive with hand descriptors, competence-signature novelty. Kill if signatures don't beat hand-descriptor OE06 on worst-family retention.
- **Old-task retention:** Mean and worst-family competence over all families at the end, plus the first 10 MiniGrid goal types.
- **Risk / likely tie:** With few probes, signatures saturate and novelty becomes random, which is uniform.

### OE2-02 · Co-lapse graph: what forgets together shares substrate
- **Primitive:** the *co-lapse graph*, whose edges join archive entries that tend to lapse in the same probe pass. The archive's lapse pattern becomes a measurement of which skills share weights, read without opening the network.
- **Mechanism:** Log lapse events per entry over time. Fit a co-occurrence graph (pointwise mutual information of lapses within a window). Rehearsal then picks one representative per co-lapse cluster instead of every lapsed entry, and capacity growth is triggered per cluster.
- **Nearest prior / gap:** Forgetting events (Toneva et al.) count per-example lapses; task-interference matrices need gradients or forks. The gap: a graph read from the open-ended archive's own lapses, used to compress rehearsal.
- **Cheapest first test:** MLP on 30 generated families with known shared and private sub-structure. Check whether co-lapse clusters recover the planted structure, then compare rehearsal by cluster representative against lapse-all and uniform at equal steps. Kill if cluster rehearsal doesn't match lapse-all retention at less than half the rehearsal steps.
- **Old-task retention:** Per-family competence at the end.
- **Risk / likely tie:** Clusters may only reflect recency of training.

### OE2-03 · Revival graph: rehearse what brings others back
- **Primitive:** the *revival graph*, a directed edge A → B when re-acquiring lapsed A restores lapsed B with no training on B. Rehearsal picks entries by revival out-degree.
- **Mechanism:** When a lapsed entry re-enters through exploration, re-probe the other lapsed entries. Record those that come back for free. Over time, rehearse the high out-degree entries first. A root with many revivals is a stepping stone in the forgetting direction.
- **Nearest prior / gap:** Relearning savings ([2610.22381](https://arxiv.org/abs/2610.22381)) measure latent knowledge per item; POET transfer measures forward stepping stones. The gap: stepping stones for *relearning*, measured inside the archive.
- **Cheapest first test:** Same host as OE2-02. Arms at equal steps: uniform rehearsal, lapse-all, revival-ordered. Kill if revival ordering doesn't beat uniform on worst-family retention.
- **Old-task retention:** Per-family competence, and revived-without-training counts.
- **Risk / likely tie:** Revivals may be rare in small networks; the test reports the base rate first.

### OE2-04 · Latent versus lost: a two-tier archive
- **Primitive:** split archive state into *expressed* (the learner produces the behaviour spontaneously), *latent* (it can be elicited with a hint or a short prefix) and *lost*. Only lost entries count as novel, latent ones get a cheap re-expression nudge, and the latent share is a readout of hidden retention.
- **Mechanism:** Each probe has a spontaneous form and an elicited form (goal-conditioned start, prefix or hint). Lapse in spontaneous but pass in elicited → latent. Re-expression training on latent entries uses only elicited rollouts, which costs a fraction of exploration.
- **Nearest prior / gap:** Access-vs-ability work (2610.08718, cited in triage row 161) and unlearning diagnostics ([2611.29285](https://arxiv.org/abs/2611.29285)) separate suppression from loss after the fact. The gap: the split built into an exploration archive, so it changes the drive.
- **Cheapest first test:** 0.5B LM self-play on 10 code-puzzle families, with prefixes as elicitation. Arms at equal tokens: OE06 (one tier), two-tier. Kill if the latent share is under 10% of lapses, or if the two-tier archive doesn't reach OE06's retention with fewer exploration tokens.
- **Old-task retention:** Spontaneous and elicited success per family.
- **Risk / likely tie:** Elicitation can teach the skill; the hint must be too short to solve the task alone.

### OE2-05 · Chronic lapses as the capacity-growth trigger
- **Primitive:** count how often each entry has lapsed and re-entered. Entries that keep lapsing are evidence that the network lacks room for them, and they trigger capacity growth (a new adapter or unit block) bound to their co-lapse cluster.
- **Mechanism:** Keep a lapse counter per entry. When a cluster's mean count passes a threshold, add capacity used only by gradients from that cluster's tasks, initialized from the current weights. Growth is driven by the open-ended archive, not by task boundaries.
- **Nearest prior / gap:** Progressive nets and dynamically expandable networks grow per task; plasticity work grows on loss plateaus; the self-modifying-architecture root ([PR #335](https://github.com/manojbajaj95/cl/pull/335)) grows by its own criteria. The gap: lapse recurrence as the growth signal.
- **Cheapest first test:** Small MLP or rank-2 LoRA under a long generated stream. Arms at equal final parameters: grow on a fixed schedule, grow on loss plateau, grow on chronic lapse. Kill if chronic-lapse growth doesn't beat the schedule on worst-family retention.
- **Old-task retention:** Worst-family competence and parameter count at the end.
- **Risk / likely tie:** Chronic lapses may come from noisy probes; probes need a repeat check.

### OE2-06 · Lapse-anchored proposer for LM self-play
- **Primitive:** in proposer–solver self-play, the proposer's novelty reference set is the *solver's currently retained archive*, so the proposer is paid for tasks the solver can't do now, whether new or forgotten. Two collapse modes become one signal: the proposer drifting away from old types (#120) and the solver forgetting them.
- **Mechanism:** Absolute-Zero-style loop with an archive of solved task types, each with a probe. The proposer's reward = learnability × novelty against retained types. Forgotten types re-enter the novelty pool, so the proposer is paid to re-emit them.
- **Nearest prior / gap:** [Absolute Zero](https://arxiv.org/abs/2505.03335) and [R-Zero](https://arxiv.org/abs/2508.05004) reward learnability; [Vocabulary Dropout](https://arxiv.org/abs/2604.03472) and [Questioning the Questions](https://arxiv.org/abs/2610.04299) fight proposer diversity collapse; FCU9 checks old type emission with a witness. The gap: one novelty reference set shared by proposer drift and solver forgetting.
- **Cheapest first test:** 0.5B solver and proposer on code-reasoning puzzles, 200 steps. Arms: learnability only, learnability + diversity bonus, learnability + witness-checked replay (FCU9), lapse-anchored proposer. Kill if lapse-anchored doesn't beat witness replay on old-type accuracy.
- **Old-task retention:** Accuracy on the first 20 task types, plus a base benchmark (e.g., GSM8K).
- **Risk / likely tie:** The proposer may emit easy variants of old types; learnability gating must hold.

### OE2-07 · Little's law for repertoires
- **Primitive:** a law for open-ended continual learners: the steady-state size of the retained repertoire L equals the invention rate λ (new archive entries per step) times the mean retention time W (steps until lapse), L = λW. Any drive that raises λ without changing W grows the repertoire in proportion; capacity limits appear as W falling when λ rises.
- **Mechanism:** Measure λ, W and L on the competence-tracking archive under several drives and capacities. Fit W(λ) per capacity; its slope is the learner's *repertoire interference coefficient*. A drive is a primitive if it shifts W(λ), not if it moves along it.
- **Nearest prior / gap:** Little's law is queueing theory; the parent's OE32 asks for a growth–retention curve without a law; [An Information-Theoretic Definition for Open-Ended Learning](https://arxiv.org/abs/2606.08369) defines open-endedness for an observer. The gap: a falsifiable conservation law for repertoire size, and W(λ) as the yardstick.
- **Cheapest first test:** MLP host at 3 capacities × 5 drive strengths, ~1e5 steps each. Kill if L deviates from λW by more than 20% at steady state, which would mean entries are lapsing in correlated bursts and the law needs a burst term.
- **Old-task retention:** It is the measured W.
- **Risk / likely tie:** Little's law holds for any stable queue; the content is W(λ) and its shift, not the identity itself.

### OE2-08 · The rehearsal–novelty parity principle
- **Primitive:** a testable claim behind (a): a lapsed behaviour should be priced *exactly* like a new one. Price parity holds when rediscovering a lapsed entry teaches as much transferable structure as discovering a new one; the card measures the exchange rate at which the two are equal.
- **Mechanism:** Sweep the relative price ρ of re-entry to new discovery (ρ = 1 is OE06). Measure total retained competence and frontier growth. Predict the optimal ρ from measured revival out-degree (OE2-03) and transfer of new entries.
- **Nearest prior / gap:** CURIOUS uses |LP| (implicit parity in magnitude); Go-Explore weights cells by visit counts. The gap: an explicit exchange rate with a predicted optimum.
- **Cheapest first test:** #119 host and MiniGrid, ρ ∈ {0, 0.25, 0.5, 1, 2, 4}. Kill if the optimum is not predicted within a factor of 2 by the revival and transfer measurements.
- **Old-task retention:** Worst-family competence at each ρ.
- **Risk / likely tie:** The optimum may be flat; then parity is harmless but not a principle.

### OE2-09 · Lapse-rate homeostasis
- **Primitive:** use the archive's lapse rate as the learner's plasticity–stability readout and regulate the step size (or the size of the trust region) to hold it at a target. Stability is set by what the learner can still do, not by distance in weights.
- **Mechanism:** Every probe pass gives a lapse rate r_t. A controller adjusts the learning rate multiplicatively toward r*. New learning speed is measured alongside, and r* is chosen on the Pareto front.
- **Nearest prior / gap:** Homeostatic plasticity in neuroscience; adaptive LR schedules by loss; EWC strength tuning. The gap: a behavioural lapse rate from a self-built archive as the controlled variable.
- **Cheapest first test:** Shifting stream with MLP and LoRA hosts. Arms: fixed LR tuned on a validation stream, cosine restarts, lapse homeostasis. Kill if homeostasis doesn't beat the tuned fixed LR on a held-out stream with a different shift rate.
- **Old-task retention:** Per-task accuracy after the stream.
- **Risk / likely tie:** A tuned fixed LR is strong when the shift rate is constant; the test needs a changing rate.

### OE2-10 · The self-built retention benchmark
- **Primitive:** treat the archive as a retention benchmark the learner built by exploring, and test whether it is *valid*: does lapse on the self-archive predict forgetting on an external human benchmark the learner never saw?
- **Mechanism:** For each checkpoint, compute archive lapse rate and external forgetting (held-out suites in the same domain). Fit the predictive relation; if it holds, the archive can stand in for external probes during open-ended runs.
- **Nearest prior / gap:** [Are Self-Evolving Agents Continual Learners?](https://arxiv.org/abs/2610.25858) measures forgetting with human benchmarks. The gap: validity of the learner's own exploration archive as a retention benchmark.
- **Cheapest first test:** 0.5B LM self-play on code puzzles, with HumanEval-like held-out tasks. Kill if the rank correlation between archive lapse and external forgetting across 20 checkpoints is below 0.5.
- **Old-task retention:** It is the measured quantity.
- **Risk / likely tie:** A measurement card; it decides whether the other cards can be run without external labels.

---

## B · Skills stored as objectives

### OE2-11 · Objective compressibility: when a reward is shorter than a policy
- **Primitive:** a property of a skill, its *objective compressibility*: the description length of the shortest reward program that regrows it from a perturbed policy, divided by the description length of a policy or trajectory store that keeps it at the same success. Skills with ratio < 1 should be stored as objectives, the rest as data.
- **Mechanism:** For each mastered skill, search reward programs by length (LM-written, verified by regrowth). Compare to compressed trajectory replay and a distilled small policy. Store each skill in the format with the lower length at equal regrowth success.
- **Nearest prior / gap:** [RL with Simple Sequence Priors](https://arxiv.org/abs/2305.17109) and MDL policies regularize the policy; LP39 re-derivability stores what is hard to regrow. The gap: the ratio between objective and policy lengths, as a per-skill choice of retention format.
- **Cheapest first test:** 12 MiniGrid and Craftax-Classic skills. Measure the ratio, then run mixed-format retention against all-trajectory and all-reward at equal total bytes. Kill if the mixed format doesn't beat the better pure format.
- **Old-task retention:** Success on all 12 skills after an interfering phase and one rehearsal pass.
- **Risk / likely tie:** LM-written reward length depends on the DSL; fix it before measuring.

### OE2-12 · Counterexample-guided reward refinement
- **Primitive:** when regrowing from a stored reward produces a *different* policy than the original (the reward has several optima), the learner finds the state where the two disagree and adds the shortest term that rules out the impostor. Repeat until regrowth is unique up to a tolerance. The stored object is a reward whose optimum is certified to be the skill.
- **Mechanism:** Regrow several times from different perturbations. Cluster the resulting policies by behaviour; if more than one cluster, pick a disagreement state and ask the reward writer for a term that scores the original higher there. This is CEGIS on objectives.
- **Nearest prior / gap:** Reward identifiability results (rewards are identifiable only up to shaping, Ng et al. 1999; EPIC); iterative reward design ([A Bird's-Eye View of Iterative Reward Design](https://arxiv.org/abs/2610.04364)) refines from human or LM feedback. The gap: refinement against *one's own regrowth impostors*, aimed at retention.
- **Cheapest first test:** Gridworld skills with deliberately ambiguous first-draft rewards. Arms: first-draft reward, Eureka-style refinement on return, counterexample refinement. Kill if counterexample refinement doesn't raise the share of regrowths that match the original behaviour.
- **Old-task retention:** Behaviour match to the original skill after regrowth.
- **Risk / likely tie:** Terms may pile up until the reward is as long as a trajectory; OE2-11's ratio caps it.

### OE2-13 · Discriminative skill rewards: regrow this, not the neighbour
- **Primitive:** store each skill's reward together with the neighbouring skills it must *not* regrow. The shortest reward is found under that contrast, so regrowth restores one skill without pulling the policy toward a similar one and causing interference.
- **Mechanism:** The reward writer gets the skill's rollouts plus rollouts of its two nearest archived skills and must write a reward that ranks the skill's rollouts above both. Regrowth then checks that the neighbours' success doesn't drop.
- **Nearest prior / gap:** Contrastive reward learning and DIAYN-style discriminability make skills distinct during discovery. The gap: contrast as a constraint on the *stored* objective, so rehearsal doesn't interfere.
- **Cheapest first test:** 8 similar navigation skills. Arms: plain stored rewards, discriminative stored rewards. Kill if discriminative rewards don't cut neighbour degradation during regrowth.
- **Old-task retention:** Success of the regrown skill and of its neighbours.
- **Risk / likely tie:** May equal adding the neighbours' rewards with negative weight.

### OE2-14 · Objective-space consolidation
- **Primitive:** while learning something new, add small doses of the stored skill rewards as auxiliary objectives. Consolidation acts in objective space rather than weight space (EWC) or data space (replay).
- **Mechanism:** Multi-objective RL in which the new task's reward is the main objective and the stored rewards enter with weights that rise when a skill's probe nears lapse. No old data is used.
- **Nearest prior / gap:** EWC regularizes weights; replay and distillation use data; multi-task RL trains on all rewards at full weight. The gap: lapse-weighted doses of *self-written* rewards as the only consolidation signal.
- **Cheapest first test:** 8-skill Craftax-Classic sequence. Arms at equal environment steps: EWC, trajectory replay, policy distillation, objective-space consolidation. Kill if it doesn't beat trajectory replay at equal bytes.
- **Old-task retention:** Success on all 8 skills after the sequence.
- **Risk / likely tie:** Rollouts under old rewards cost environment steps that replay doesn't; count them in the budget.

### OE2-15 · Rewards that carry a skill across a model or world change
- **Primitive:** the stored objective as a *portable* skill format. After a backbone swap, an observation change or a change in the environment's dynamics, a stored policy is useless, but the stored reward still says what the skill was and can regrow it in the new setting.
- **Mechanism:** Store reward programs over a stable state interface. After the change, regrow each skill from the new model's prior and compare with transferring the policy (fine-tune, distill through a shared interface) and with relearning from task text.
- **Nearest prior / gap:** [AIRL](https://arxiv.org/abs/1710.11248) shows rewards can transfer across dynamics; Trans-LoRA moves adapters between models; the cultural-evolution root's CE07 migrates symbolic updates across vocabulary changes. The gap: self-written rewards as the retention format that survives a substrate change.
- **Cheapest first test:** MiniGrid skills learned with a CNN, then moved to a different encoder or to altered dynamics (slippery floor). Arms at equal steps: policy fine-tune, distillation through state, relearning from task description, regrowth from stored rewards. Kill if regrowth doesn't beat policy fine-tuning on success after the change.
- **Old-task retention:** Success on all skills after the change.
- **Risk / likely tie:** AIRL-style transfer is the prior; the gap is self-written rewards for one's own skills.

### OE2-16 · The externalization spectrum of a skill
- **Primitive:** split each skill into the part held in *weights* and the part held in its *objective*. The measure is the perturbation radius from which the stored reward still regrows the skill. Radius ∞ (regrows from scratch) means fully externalized; radius 0 means the reward adds nothing over the weights.
- **Mechanism:** For each skill, regrow from perturbations of growing size (weight noise, interfering training, partial reset, scratch). The radius at which regrowth fails is the skill's externalization. Use it to decide which skills can survive resets (the parent's OE03) and which need weight protection.
- **Nearest prior / gap:** Relearning savings measure what remains in weights after forgetting; OE03 regrows from worlds. The gap: one number placing a skill between weight-held and objective-held.
- **Cheapest first test:** 12 skills, 5 perturbation levels. Kill if the radius doesn't predict which skills survive a full reset plus regrowth within 2× the original training steps.
- **Old-task retention:** Success after each perturbation and regrowth.
- **Risk / likely tie:** May correlate only with skill difficulty; report it with difficulty matched.

### OE2-17 · Occam for objectives: short rewards regrow more general skills
- **Primitive:** a testable claim that a skill regrown from a *short* reward generalizes to held-out variants better than the original policy did, because the short reward drops the incidental details the original policy learned.
- **Mechanism:** For each skill, compare the original policy and policies regrown from rewards of increasing length on held-out variants (new layouts, new object colours).
- **Nearest prior / gap:** Simplicity priors on policies; shortcut learning; reward design for robustness. The gap: storage through a short objective as a generalization step, a side benefit of retention.
- **Cheapest first test:** MiniGrid and Procgen-lite skills with layout variants. Kill if regrown policies from the shortest passing rewards don't beat the original on held-out variants.
- **Old-task retention:** Success on original instances must not drop below the original policy's.
- **Risk / likely tie:** Regrowth adds training, which alone may help; compare against the original trained for the same extra steps.

### OE2-18 · Internal rewards: store the skill as a target on one's own activations
- **Primitive:** a skill reward written over the learner's *internal features*, not over environment state. The stored object is a short target pattern on a few units, regrown by optimizing the policy to reach it. It is often shorter than an environment reward.
- **Mechanism:** After mastery, find a sparse set of features whose values separate the skill's rollouts from others (probe). Store the target. Regrowth = RL with reward = negative distance to the target. Re-anchor the features when the encoder drifts (parent's OE13).
- **Nearest prior / gap:** [Feature control as intrinsic motivation](https://arxiv.org/abs/1705.06769) uses feature targets for exploration; activation steering adds directions at inference. The gap: internal-feature targets as the *retention format*, regrown by optimization.
- **Cheapest first test:** 8 Craftax-Classic skills. Arms at equal bytes: environment reward programs, internal targets, trajectory replay. Kill if internal targets regrow less than environment rewards do.
- **Old-task retention:** Success on all skills after an interfering phase.
- **Risk / likely tie:** Drift of the features may break targets faster than rewards; OE13 is a dependency.

### OE2-19 · A library of objectives: the agent's values as compressed rewards
- **Primitive:** run library learning on the *stored reward programs* to extract shared reward abstractions, the learner's reusable "values". New skills are stored as short compositions of library terms, and forgetting is tracked per abstraction.
- **Mechanism:** DreamCoder/LILO compression over the reward-program archive. New skill rewards are written using library terms; each term carries a lapse counter summed over the skills that use it.
- **Nearest prior / gap:** [DreamCoder](https://arxiv.org/abs/2006.08381) and [LILO](https://arxiv.org/abs/2310.19791) compress solutions; MLREF reuses reward modules across tasks for design. The gap: compressing *one's own retention objectives* into a library.
- **Cheapest first test:** 30 skills in a crafting world with shared subgoals. Arms: flat reward archive, reward library. Kill if the library doesn't shorten stored rewards by 30% or more at equal regrowth success.
- **Old-task retention:** Success on all skills after regrowth from library-expressed rewards.
- **Risk / likely tie:** Few shared subgoals means no compression.

### OE2-20 · Store the checker, not the data: verifier programs as LM skill memory
- **Primitive:** the language-model form of (b): store each mastered skill as a short *checker program* (unit tests, a verifier or a rubric) plus a prompt generator. When probes show the skill decaying, regrow it by RLVR against the stored checker. No old solutions are kept.
- **Mechanism:** After mastery of a task family, the model writes a checker and a generator; both are kept only if the checker agrees with ground truth on a calibration set. Rehearsal = a few RLVR steps on fresh generated prompts graded by the stored checker.
- **Nearest prior / gap:** [Absolute Zero](https://arxiv.org/abs/2505.03335) and RLVR train on checkers for *new* skills; replay stores solutions; the parent's OE25 tracks verifier retention. The gap: checker plus generator as the retention format for an LM's own skills.
- **Cheapest first test:** 0.5B–1.5B LM, 10 code families learned in sequence. Arms at equal bytes and equal gradient steps: solution replay, self-QA replay, stored checker RLVR. Kill if checker RLVR doesn't beat solution replay on fresh instances of old families.
- **Old-task retention:** Fresh-instance accuracy on all 10 families, plus a base benchmark.
- **Risk / likely tie:** Small models write weak checkers; the calibration gate is mandatory.

### OE2-21 · Regrowth-cost pricing for format choice
- **Primitive:** for each skill, measure the *regrowth cost* (steps to regain the skill from its stored objective after a standard perturbation) and use it, together with storage bytes, to choose among storing nothing, storing an objective and storing data. A skill is kept only in the cheapest format that regrows it within its deadline.
- **Mechanism:** Periodically perturb a fork and time regrowth from each format. Pick the format by cost per byte under a deadline. Skills that regrow cheaply from nothing (rediscoverable by exploration) store nothing.
- **Nearest prior / gap:** LP39 re-derivability memory (stores what is hard to re-derive); the parent's OE01 and OE03. The gap: a three-way format choice priced by measured regrowth.
- **Cheapest first test:** 12 skills, total storage capped at 25% of what storing all trajectories needs. Arms: all-trajectory under the cap, all-reward, priced choice. Kill if priced choice doesn't beat the better pure format at the cap.
- **Old-task retention:** Success on all 12 skills after an interfering phase and regrowth.
- **Risk / likely tie:** Close to LP39; the difference is that objectives are a middle option.

---

## C · One object for both: crosses of (a) and (b)

### OE2-22 · Archive entries are reward programs
- **Primitive:** the natural merge. Every archive entry *is* a stored reward program. The lapse probe is a brief rollout scored by that reward, re-entry is novelty under the archive drive, and rehearsal is a few optimization steps on the same reward. One object serves as descriptor, probe and rehearsal carrier.
- **Mechanism:** When a new behaviour is archived, write its reward (with OE2-12 refinement). The probe = success under the stored reward from the current policy. Lapse → the entry becomes novel → the drive picks it → regrowth is optimizing the stored reward.
- **Nearest prior / gap:** Parts: OE06 and OE02. Merge rule: it must beat OE06 with trajectory replay *plus* OE02 with a fixed rehearsal schedule, stacked at equal steps and bytes. The interaction it claims is that the reward probe detects lapse in the same terms that regrowth repairs it, so no probe–rehearsal mismatch arises.
- **Cheapest first test:** MiniGrid and Craftax-Classic, 20 discovered behaviours. Arms at equal steps and bytes: OE06 + trajectory replay, OE02 on a fixed schedule, both stacked, merged entries. Kill if merged entries don't beat the stacked parts on worst-behaviour retention.
- **Old-task retention:** Success on all archived behaviours at the end.
- **Risk / likely tie:** Likely ties the stacked parts unless probe–rehearsal mismatch is common; measure mismatch first.

### OE2-23 · Novelty in objective space under shaping equivalence
- **Primitive:** measure archive novelty over *stored reward programs*, compared up to potential shaping (EPIC distance), instead of over behaviours. The learner explores the space of objectives it can satisfy, and two rewards that induce the same optimum are one entry.
- **Mechanism:** New behaviours are rewritten as rewards, canonicalized, and compared by EPIC distance to retained entries. Novelty = distance to the nearest retained objective. Lapse is still defined by competence (OE06).
- **Nearest prior / gap:** [EPIC](https://arxiv.org/abs/2006.13900) compares rewards; [Habitats](https://arxiv.org/abs/2611.31160) evolves objectives for new behaviour; OMNI filters tasks for interestingness. The gap: shaping-invariant objective distance as the novelty metric of a competence-tracking archive.
- **Cheapest first test:** Gridworld with 40 possible goals that share many shaping-equivalent rewards. Arms at equal steps: behaviour-space novelty, objective-space novelty. Kill if objective novelty doesn't cover more distinct optima.
- **Old-task retention:** Success on all covered optima at the end.
- **Risk / likely tie:** EPIC requires a coverage distribution; the choice matters.

### OE2-24 · Mini-task entries: reward plus start distribution
- **Primitive:** store each skill as a *mini-task*: its reward program plus the start-state distribution from which it was practised. Rehearsal needs both, since a reward without its starts may regrow the skill only from easy states.
- **Mechanism:** The archive entry = (reward, start sampler as a short program or seed set, from the parent's OE01). Regrowth samples starts from the stored sampler. Probes use the same starts.
- **Nearest prior / gap:** Reverse curriculum ([1707.05300](https://arxiv.org/abs/1707.05300)) uses starts for learning; Go-Explore returns to start cells; OE01 and OE02 store keys and rewards separately. The gap: the pair as one retention object, tested against each half.
- **Cheapest first test:** Skills whose difficulty depends on the start (MiniGrid with far and near starts). Arms at equal steps: reward only, starts only with trajectory replay, mini-task. Kill if the mini-task doesn't beat the reward alone on far-start success.
- **Old-task retention:** Far- and near-start success on all skills.
- **Risk / likely tie:** Must beat the union of its two parts (merge rule).

### OE2-25 · Lapse-forced reward rewriting
- **Primitive:** when an entry lapses and is regrown from its stored reward, rewrite the reward against the *current* model before re-storing it, so the objective tracks what the learner now needs to be told. Rewards that stop shrinking or start growing at each rewrite mark skills the learner is losing its grip on.
- **Mechanism:** After each regrowth, ask the reward writer for the shortest reward that regrows the skill from the current policy's perturbation. Track reward length over successive lapses: a falling length means the skill is becoming easy to restore, a rising one means it is fading.
- **Nearest prior / gap:** CE21 hands down exercises across learners; OE2-11 measures compressibility once. The gap: reward length over time as a per-skill readout of how much the weights still hold.
- **Cheapest first test:** 12 skills over 5 lapse–regrow cycles. Kill if reward-length trends don't predict which skills fail to regrow at cycle 5 better than the regrowth step count does.
- **Old-task retention:** Regrowth success at each cycle.
- **Risk / likely tie:** Regrowth steps may carry the same information more cheaply.

### OE2-26 · Self-written rewards for unplanned behaviours
- **Primitive:** archive admission by writing an objective. A behaviour the agent stumbled into is archived *only if* it can write a reward program that regrows it; otherwise it is treated as noise. Writing an objective becomes the test of whether a behaviour is a skill.
- **Mechanism:** On a novel behaviour, attempt a reward program within a length budget; admit the behaviour if regrowth from a perturbed policy matches it. Novelty search then fills the archive only with behaviours that have compact objectives.
- **Nearest prior / gap:** Novelty search admits by distance; POET admits by minimal criterion; OMNI by interestingness. The gap: compressible objective as the admission criterion, filtering out lucky or noise behaviours.
- **Cheapest first test:** Open-ended MiniGrid exploration, 200 candidate behaviours. Arms: distance admission, minimal criterion, objective admission. Kill if objective admission doesn't raise the share of archived behaviours that are still reproducible after training on 50 more.
- **Old-task retention:** Reproducibility of archived behaviours at the end.
- **Risk / likely tie:** Behaviours without short rewards may be the interesting ones; the test reports what is excluded.

---

## Ranked deeper questions

1. **Does one object, a stored reward used as probe, descriptor and rehearsal carrier, beat the union of the archive and reward-storage parts? (OE2-22, OE2-12, OE2-24, OE2-26)**
   Measure first how often probe and rehearsal disagree in the stacked baseline (OE06 + trajectory replay plus OE02 on a schedule). If disagreement is rare, the merge is bookkeeping. If it is common, test whether merged entries, refined until regrowth is unique, beat the stacked parts on worst-behaviour retention at equal steps and bytes.
2. **Is objective compressibility a real property that chooses the retention format? (OE2-11, OE2-16, OE2-17, OE2-21)**
   Measure the reward-to-policy length ratio and the externalization radius on 12 skills, then test whether a mixed-format archive chosen by those two numbers beats either pure format, and whether short-reward regrowth generalizes better.
3. **Does a competence-defined archive make exploration double as rehearsal, beating uniform and CURIOUS? (OE2-01, OE2-04, OE2-06, OE2-08)**
   Competence signatures, the latent/lost split, the lapse-anchored proposer and the parity price all test the claim behind (a). Run them in #119's host plus MiniGrid and a 0.5B self-play loop at equal steps. Drop the line if none beats uniform on worst-family retention.
4. **Is there a repertoire law? (OE2-07, OE2-02, OE2-05)**
   Test L = λW on the archive at three capacities, fit W(λ) as the repertoire interference coefficient, and check whether co-lapse-driven growth shifts it.
