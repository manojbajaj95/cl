# Open-ended learners 3: revival structure and reward-program entries

Depth 2 · child of [PR #385](https://github.com/manojbajaj95/cl/pull/385) (`tree/open-ended-learners-2.md`) OE2-03 and OE2-22 · 26 cards (OE3-01–OE3-26) · 4 ranked deeper questions · Ideas only; no experiments run

**What the reviewer kept, and why it is not yet a primitive.**
- **(a) Revival graph (OE2-03).** Rehearse the skills whose relearning restores other forgotten skills for free, ordered by revival count. As written, it is a *scheduling heuristic over a measured graph*. It does not say what structure the graph has, whether revival can be designed rather than found, or what the graph tells us that output probes don't.
- **(b) Archive entries as stored reward programs (OE2-22).** One object serves as probe, descriptor and rehearsal carrier. Its kill condition is explicit: it is dead if probe and rehearsal rarely disagree in the stacked baseline. It still lacks a reason why an *objective* should carry more than data does, and a descriptor that is not hand-chosen.

This node pushes both toward objects:
- **Graph structure:** a minimal revival basis, revival eigenmodes, a frustration index for signed revival, revival equivalence classes as label-free task identity, and edge lifetimes, i.e. latent links that lapse.
- **Designed revival:** synthetic revival keys, hubs built on purpose, and an update rule that protects relearnability instead of outputs.
- **Joining (a) and (b):** an entry's descriptor is its revival row, and the test is whether optimizing a stored objective revives more neighbours than training on stored data.

**Scope and controls.** The parent's constraints carry over:
- Every rehearsal-order card must beat uniform rehearsal at equal steps (#119).
- Merges must beat the union of their parts' baselines (ledger merge rule).
- Margin confounds apply: before claiming that A revives B, show that B's recovery exceeds what unrelated relearning of equal size gives. This is *nonspecific revival*, which [Rethinking Benign Relearning](https://arxiv.org/abs/2602.03379) traces partly to shared syntax.
- Revival edges must replicate at ≥ 10 seeds before any card builds on them (ledger anomaly-mining rule).

## Literature check

alphaXiv searches (8 new queries): relearning transfer and recovery, spurious and superficial forgetting, anticipatory recovery under cyclic training, reward machines, evaluation–training mismatch in CL, prerequisite graphs and spaced repetition, coresets for recovery, and successor-feature task identity.

| Line | Already available | What this node must add |
|---|---|---|
| Forgetting as lost access | [Spurious forgetting](https://arxiv.org/abs/2610.08718), [Forgetting is Not Erasure: transport keys](https://arxiv.org/abs/2606.02860), [Accessibility Collapse](https://arxiv.org/abs/2606.06032), [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637), [Hidden not Deleted](https://arxiv.org/abs/2609.27593), [Binding-Specific Relearning Savings](https://arxiv.org/abs/2610.22381), [Agentic-OPD](https://arxiv.org/abs/2611.12799) (recovering forgotten agent skills from discarded checkpoints) | These recover *one* skill's latent knowledge, by keys, a readout, or distillation. None measures *which other* skills come back when one is relearned, or uses that structure. |
| Relearning that spreads | [Anticipatory recovery](https://arxiv.org/abs/2403.09613) (cyclic training recovers a document *before* it reappears), [Localizing Transfer Between Memorization Tasks](https://arxiv.org/abs/2610.00771), relearning attacks on unlearning ([2605.11685](https://arxiv.org/abs/2605.11685), [2608.25429](https://arxiv.org/abs/2608.25429), [2604.09391](https://arxiv.org/abs/2604.09391)) | Anticipatory recovery shows revival under a *fixed* cycle; the unlearning work shows relearning paths as an attack. No work treats the revival relation among a learner's own skills as an object with structure (basis, modes, frustration, lifetime). |
| Prerequisites and review | Knowledge-tracing prerequisite graphs ([2611.09345](https://arxiv.org/abs/2611.09345), [2611.16323](https://arxiv.org/abs/2611.16323)), [spaced repetition for continual pretraining](https://arxiv.org/abs/2608.17530), [Replay on Demand](https://arxiv.org/abs/2609.40089), [interpretable memory models for spaced repetition](https://arxiv.org/abs/2610.10548) | Prerequisite graphs model *acquisition* order for students; spaced repetition schedules each item alone. Revival is the forgetting-side relation, measured on the learner itself. |
| Structured objectives | Reward machines ([ARM-FM](https://arxiv.org/abs/2510.14176), [active RM inference](https://arxiv.org/abs/2604.07480)), [successor features](https://arxiv.org/abs/1606.05312), [Task diversity produces systematic transfer but inhibits continual RL](https://arxiv.org/abs/2606.00880), [Fast and Slow Successor Features](https://arxiv.org/abs/2605.26357) | Reward machines specify tasks for learning; SF reward vectors identify tasks for transfer. Neither is used as a *retention* entry whose structure localizes a lapse. |

---

## A · What structure does the revival graph have?

### OE3-01 · Minimal revival basis and the repertoire's latent dimension
- **Primitive:** the *revival basis*, the smallest set of skills whose relearning restores the whole lapsed repertoire within tolerance. Its size is a new measurement: the latent dimension of what the learner still holds but cannot express.
- **Mechanism:** From the measured revival graph (thresholded edges above the nonspecific-revival control), compute a minimum dominating set over multi-hop revival, approximated greedily. Verify by relearning only the basis and probing everything. Track basis size over training: a growing basis means latent structure is fragmenting.
- **Nearest prior / gap:** Coresets and exemplar condensation ([2603.13804](https://arxiv.org/abs/2603.13804)) choose *data* that represents a task; anticipatory recovery shows revival in cycles. The gap: a set of *skills* defined by relearning effects, with its size as an observable.
- **Cheapest first test:** MLP on 30 generated families with planted shared factors (k = 5 latent factors), forced to forget by an interfering phase. Kill if the greedy basis doesn't come within 2 of k, or if relearning the basis restores less than relearning a random set of the same size.
- **Old-task retention:** Competence on all 30 families after basis-only relearning.
- **Risk / likely tie:** If revival is mostly nonspecific, every set of the same size works and the basis is meaningless; the random-set control decides.

### OE3-02 · Revival eigenmodes: rehearse modes, not skills
- **Primitive:** *revival modes*, the leading eigenvectors of the (symmetrized) revival matrix. A mode is a weighted bundle of skills that revive together. Rehearsal is a short training on a mode-weighted mixture, so it targets the shared latent direction rather than any one skill.
- **Mechanism:** Measure the revival matrix R (R_ij = recovery of j after relearning i, minus the nonspecific control). Take the top eigenvectors. Rehearse by sampling skills in proportion to |v_k| for the most-lapsed modes.
- **Nearest prior / gap:** Spectral clustering of task-affinity matrices (TAG-style gradient affinity) groups tasks for *joint training*; [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637) studies the geometry of recoverability for single tasks. The gap: a spectral decomposition of the *forgetting-side* relation, used as the rehearsal unit.
- **Cheapest first test:** Same host as OE3-01. Arms at equal steps: uniform rehearsal, revival out-degree (OE2-03), mode rehearsal. Kill if modes don't beat out-degree on worst-family retention.
- **Old-task retention:** Per-family competence.
- **Risk / likely tie:** With one dominant mode, this equals uniform rehearsal.

### OE3-03 · Signed revival and the frustration index
- **Primitive:** keep the *negative* edges too: relearning A further damages B. When the signed graph has cycles with an odd number of negative edges, no rehearsal order revives everything. The *frustration index* (the minimum number of edges whose removal makes the graph balanced, as in spin glasses) measures how far a repertoire is from being jointly recoverable.
- **Mechanism:** Measure signed revival. Compute frustration by balance theory. Use it two ways: as a capacity alarm (high frustration means skills compete for the same latent substrate) and to choose which skill to give separate capacity (the node whose isolation removes the most frustration).
- **Nearest prior / gap:** Gradient conflict (PCGrad, GEM) is pairwise and about *learning*; write-skew (top-10 #3) is about set-level breakage of new writes. The gap: frustration of the *revival* relation, a set-level quantity about recoverability.
- **Cheapest first test:** MLP with planted competing pairs (opposite labels on shared features). Kill if frustration doesn't rise with planted competition, or if isolating the highest-frustration node doesn't beat isolating a random node on retention.
- **Old-task retention:** Competence on all families after the isolation step plus one rehearsal pass.
- **Risk / likely tie:** Negative edges may just be interference measured in a different way.

### OE3-04 · Revival algebra: symmetry, transitivity and hierarchy
- **Primitive:** test whether revival is symmetric (A ↔ B), transitive (A → B → C implies A → C) and graded. The pattern of failures reveals a latent hierarchy: asymmetric edges point from general skills to specific ones, and transitivity failures mark skills that share different substrates with a common neighbour.
- **Mechanism:** Measure R on triples. Fit a partial order from asymmetric edges, and flag intransitive triples. Use the order to place new skills: a new skill revived by an existing general skill needs no protection of its own.
- **Nearest prior / gap:** Prerequisite-relation learning in knowledge tracing ([2608.03006](https://arxiv.org/abs/2608.03006)) infers acquisition order from student data. The gap: the algebra of a model's *own* relearning relation.
- **Cheapest first test:** Hierarchical generated families (general rule plus specific exceptions). Kill if asymmetric edges don't point from general to specific in at least 80% of planted pairs.
- **Old-task retention:** Retention of specific skills when only general ones are rehearsed.
- **Risk / likely tie:** Order may follow difficulty rather than generality; match difficulty.

### OE3-05 · Revival equivalence classes as label-free task identity
- **Primitive:** define two skills as *the same task* for CL purposes when each revives the other almost fully. The resulting equivalence classes give task boundaries without labels, defined by the learner's own latent structure rather than by the data source.
- **Mechanism:** Threshold mutual revival; take connected components of the mutual-revival graph. Use classes as the unit for protection, rehearsal and capacity. Compare with task-free CL boundary detection.
- **Nearest prior / gap:** Task-free CL detects shifts from loss spikes; successor-feature task inference ([2610.05350](https://arxiv.org/abs/2610.05350)) identifies tasks by rewards; the top-10 Nerode quotient groups *edits* by future behaviour. The gap: grouping *skills* by mutual relearning, a forgetting-side quotient.
- **Cheapest first test:** Streams where data sources and true latent tasks are crossed (one source holds two tasks; two sources hold one). Kill if revival classes don't recover the latent tasks better than source labels or loss-spike boundaries.
- **Old-task retention:** Retention when protection is applied per revival class against per source.
- **Risk / likely tie:** Close to clustering by gradient similarity; include it as a control.

### OE3-06 · Edge lifetimes: when latent links lapse
- **Primitive:** *second-order forgetting*: a revival edge A → B can itself disappear, so that after long enough, relearning A no longer restores B. Edges get lifetimes, and the learner rehearses an edge (relearn A, check B) just before it is predicted to break, not when B lapses.
- **Mechanism:** Re-measure edges periodically. Fit survival curves per edge. Schedule edge maintenance by hazard. A broken edge means B's latent trace is now erased, not just hidden.
- **Nearest prior / gap:** Spaced repetition schedules *items* by their recall hazard ([2610.10548](https://arxiv.org/abs/2610.10548)); accessibility-collapse work studies whether a single skill's trace persists. The gap: a lifetime for the *link* between latent traces.
- **Cheapest first test:** Long interfering stream on an MLP. Measure edge survival. Arms at equal steps: item-hazard rehearsal, edge-hazard maintenance. Kill if edges don't decay measurably slower or faster than items (then edges add nothing), or if edge maintenance doesn't beat item rehearsal on final retention.
- **Old-task retention:** Competence on all families, and the number of surviving edges at the end.
- **Risk / likely tie:** Measuring edges costs forks; count fork compute in the budget.

### OE3-07 · The revival step-size window
- **Primitive:** revival depends on how hard the learner relearns. Small relearning steps restore latent neighbours (access), while large ones overwrite them. The *revival window* is the range of step sizes and lengths where a root revives the most neighbours, and it is a property of the learner's state.
- **Mechanism:** For each root, sweep relearning learning rate × steps and measure neighbour revival. The window's width and position over training is a readout of how fragile the latent store is. Rehearsal uses window-centred steps.
- **Nearest prior / gap:** [Learning rates regulate catastrophic overtraining](https://arxiv.org/abs/2604.13627); relearning attacks vary step budget. The gap: an explicit window for *collateral revival*, used to set rehearsal step size.
- **Cheapest first test:** MLP and LoRA hosts. Kill if neighbour revival is monotone in step size (no window).
- **Old-task retention:** Neighbour competence and root competence at the chosen step size.
- **Risk / likely tie:** The window may simply be "under-train the root".

### OE3-08 · Cause fingerprints: the revival pattern tells why forgetting happened
- **Primitive:** forgetting caused by interference, by disuse with weight decay, or by a partial reset leaves *different revival patterns*: dense mutual revival suggests lost access, sparse revival suggests erasure. The pattern is a fingerprint that names the cause and so the right repair (readout fix, rehearsal or regrowth).
- **Mechanism:** Induce each cause in controlled runs and record revival graphs. Train a classifier from graph statistics (density, modes, frustration) to cause. Apply it in open-ended runs to choose the repair.
- **Nearest prior / gap:** [Spurious forgetting](https://arxiv.org/abs/2610.08718) and [Hidden not Deleted](https://arxiv.org/abs/2609.27593) separate suppression from erasure for single features. The gap: diagnosing cause from the *relational* pattern across skills.
- **Cheapest first test:** MLP with three induced causes × 10 seeds. Kill if graph statistics classify cause no better than single-skill relearning savings do.
- **Old-task retention:** Retention after the cause-matched repair against a fixed repair.
- **Risk / likely tie:** Savings alone may separate the causes.

### OE3-09 · Does the revival graph survive a model change?
- **Primitive:** test whether revival structure is a property of the *skills* or of the *weights*. Retrain the same repertoire on a different seed or architecture and compare graphs. If they match, the graph is portable structure, and a new model can rehearse along the old model's hubs from day one.
- **Mechanism:** Measure R on two models trained on the same family sequence. Compare by rank correlation of edges and overlap of revival bases.
- **Nearest prior / gap:** Representation similarity across seeds (CKA) and model stitching compare activations. The gap: comparing *relearning relations*.
- **Cheapest first test:** 5 seeds × 2 widths of MLP. Kill if edge rank correlation across seeds is below 0.5.
- **Old-task retention:** Retention in the new model when it rehearses using the old model's basis against its own measured basis.
- **Risk / likely tie:** If the graph is seed-specific, every card here must measure per model.

---

## B · Designing revival instead of finding it

### OE3-10 · Revival keys: synthetic inputs that revive a cluster
- **Primitive:** a *revival key*, a tiny synthetic training set (a few inputs and targets, not drawn from any task) optimized so that one short training run on it revives a whole cluster of lapsed skills. The key is a new storage object, smaller than a replay buffer and not tied to any single task.
- **Mechanism:** Treat the key as parameters. Bilevel optimization: inner loop = k steps on the key from the current weights; outer loss = probe loss on the cluster's skills after the inner loop (dataset-distillation style, but aimed at revival). Store keys per co-lapse cluster and rehearse by training on the key.
- **Nearest prior / gap:** Dataset distillation and gradient matching condense data for *training from scratch*; [transport keys](https://arxiv.org/abs/2606.02860) recover latent knowledge with a learned map at read time. The gap: a synthetic *training* input optimized to restore many lapsed skills through the weights' own latent links.
- **Cheapest first test:** MLP on 30 families. Arms at equal bytes: reservoir replay, distilled replay per family, revival keys per cluster. Kill if keys don't beat distilled replay on cluster retention at equal bytes.
- **Old-task retention:** Per-family competence after key rehearsal.
- **Risk / likely tie:** Keys may overfit to the current weights and stop working after more training; re-optimize on lapse.

### OE3-11 · Designed revival hubs
- **Primitive:** train a skill so that it *becomes* a revival hub on purpose. While learning X, add a term that makes "a few steps of relearning X" restore its neighbours. Hubs are built, not found.
- **Mechanism:** Meta-objective during acquisition: after a simulated forgetting perturbation, the loss of neighbours after k relearning steps on X (MAML-style second order). The learner gets a small set of master-key skills that rehearsal can rely on.
- **Nearest prior / gap:** OML and MAML-style meta-learning shape *fast learning*; OE2-03 finds hubs after the fact. The gap: optimizing the revival topology during acquisition.
- **Cheapest first test:** MLP, 20 families, one designated hub per cluster of 4. Arms at equal compute: plain training plus out-degree rehearsal, designed hubs plus hub rehearsal. Kill if designed hubs don't raise revival out-degree, or don't beat plain training plus out-degree rehearsal on retention.
- **Old-task retention:** Retention of non-hub families when only hubs are rehearsed.
- **Risk / likely tie:** Second-order cost; a first-order approximation may lose the effect.

### OE3-12 · Protect relearnability, not outputs
- **Primitive:** an update rule that allows old outputs to fade but preserves their *revival paths*. The constraint is on the latent links (recovery after short relearning of the hub), not on old predictions (EWC, LwF).
- **Mechanism:** During new learning, periodically estimate revival of protected clusters through their hubs on a fork, and penalize updates that reduce it. Old skills can be overwritten in expression while staying revivable. This frees capacity that output-protection wastes on skills not currently needed.
- **Nearest prior / gap:** EWC, LwF and replay protect outputs; [Efficient Unlearning through Maximizing Relearning Convergence Delay](https://arxiv.org/abs/2604.09391) does the opposite (makes relearning slow); the [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637) studies when recovery is possible. The gap: relearnability as the protected quantity during continual learning.
- **Cheapest first test:** MLP and LoRA hosts with a capacity bottleneck. Arms at equal compute: EWC, replay, relearnability protection. Kill if relearnability protection doesn't give better new-task learning at equal *revived* old-task competence.
- **Old-task retention:** Old-task competence both before and after a short hub-relearning pass, with both numbers reported.
- **Risk / likely tie:** Forks make this expensive; a cheap proxy (gradient alignment of hubs and neighbours) may be needed.

### OE3-13 · Revivable forgetting: shed leaves first
- **Primitive:** when capacity forces forgetting, choose to forget *leaves*, skills with a strong in-edge from a protected hub, because they come back cheaply. The forgetting policy is set by revivability, not by recency or importance.
- **Mechanism:** Rank skills by maximum in-revival from hubs. Under capacity pressure, release protection on the top leaves (allow overwrite) and keep hubs protected. Restore leaves on demand by hub relearning.
- **Nearest prior / gap:** Reachability GC (programs-weights P33), planned forgetting and importance-weighted protection (EWC Fisher). The gap: revivability as the criterion for what to let go.
- **Cheapest first test:** MLP with capacity for 15 of 30 families. Arms: protect the most recent, protect by Fisher, protect hubs and shed leaves. Kill if shedding leaves doesn't give the highest *on-demand* competence (after a short hub relearning) across all 30.
- **Old-task retention:** On-demand competence over all families.
- **Risk / likely tie:** Hubs may also be the high-Fisher skills, so it ties Fisher.

### OE3-14 · Cycle the curriculum along revival edges
- **Primitive:** order the open-ended loop's rehearsal *cyclically along revival edges* so that anticipatory recovery does part of the rehearsal: each step relearns a skill whose out-edges point to the skills due next.
- **Mechanism:** Find a Hamiltonian-like cycle that maximizes summed edge weight through the revival graph (TSP heuristic). Rehearse in that order. Compare to a fixed random cycle (where anticipatory recovery was first reported) and to out-degree order.
- **Nearest prior / gap:** [Anticipatory recovery](https://arxiv.org/abs/2403.09613) observes recovery under a *fixed* repeated sequence; spaced repetition orders items independently. The gap: choosing the cycle by measured revival.
- **Cheapest first test:** Transformer LM (small) on 20 cycled document groups, then MLP on families. Arms at equal steps: random fixed cycle, out-degree order, revival cycle. Kill if the revival cycle doesn't beat a random fixed cycle on the minimum over the cycle of each group's loss.
- **Old-task retention:** Per-group loss across one full cycle.
- **Risk / likely tie:** Anticipatory recovery may be strong under any fixed order.

### OE3-15 · Revival channel: context versus weights
- **Primitive:** split each revival edge into a *context channel* (putting A's examples in the prompt restores B, with no update) and a *weight channel* (training on A restores B). Context-revivable edges mean B is held but not cued; weight-only edges mean B's trace must be re-linked.
- **Mechanism:** For an LM, measure both channels per edge. Skills revivable through context need only a retrieval cue at test time; weight-only skills get rehearsal. This gives two tiers of rehearsal cost.
- **Nearest prior / gap:** Access versus ability ([2610.08718](https://arxiv.org/abs/2610.08718)) and [Accessibility Collapse](https://arxiv.org/abs/2606.06032) separate suppression from erasure for one skill. The gap: separating the *channel through which another skill restores it*.
- **Cheapest first test:** 0.5B LM on 10 code families learned in sequence. Kill if the context channel never revives (then only weights matter) or if channel-tiered rehearsal doesn't beat weight-only rehearsal at equal compute.
- **Old-task retention:** Accuracy on all families with and without the context cue.
- **Risk / likely tie:** Context revival may come down to few-shot prompting; compare with unrelated few-shot examples.

### OE3-16 · Unlearning certificate by revival-path closure
- **Primitive:** call a skill *forgotten* only when all its revival in-paths are closed: no skill in the repertoire revives it within a budget. Unlearning becomes cutting revival edges, and the certificate is the closure check.
- **Mechanism:** After unlearning X, measure in-revival to X from every archived skill. If any edge is above threshold, apply a targeted cut (unlearn along the path or protect against that relearning direction) and re-check.
- **Nearest prior / gap:** Relearning-attack robustness ([2605.11685](https://arxiv.org/abs/2605.11685), [2608.25429](https://arxiv.org/abs/2608.25429)) tests relearning on *forget-set-related* data; [Behavioral Forgetting Is Not Privacy](https://arxiv.org/abs/2610.21799). The gap: closing revival from the learner's *own other skills*, not only from attack data.
- **Cheapest first test:** MLP and 0.5B LM. Unlearn one family with gradient ascent, then measure in-revival from each other family. Kill if no other family revives X beyond the nonspecific control (then closure is trivially satisfied).
- **Old-task retention:** Competence on all other families after the cuts.
- **Risk / likely tie:** Cuts may damage the reviving skills; report it.

### OE3-17 · Revival insurance across resets
- **Primitive:** before a plasticity reset, store only the *revival basis's* skills (as reward programs or keys). After the reset, regrow the basis and let revival restore the rest. Insurance costs only the basis.
- **Mechanism:** Combine OE3-01 (basis), OE2-22 entries (rewards) and the root's OE03 (reset and regrow). After regrowth of the basis, measure how much of the full repertoire returns without direct training.
- **Nearest prior / gap:** Resets with full replay; distillation from the pre-reset model; root OE03 regrows from all worlds. The gap: whether revival *survives a reset at all*. It survives only if revival is a property of the skills rather than the weights (OE3-09 tests that).
- **Cheapest first test:** MLP with a partial reset (ReDo-style) and a full reset. Arms at equal storage: full replay, distillation, basis-only regrowth. Kill if basis-only regrowth restores less than half the non-basis skills after a partial reset.
- **Old-task retention:** All-skill competence after regrowth.
- **Risk / likely tie:** A full reset likely destroys revival; the card stands on partial resets.

---

## C · Reward-program entries joined with revival

### OE3-18 · Probe–rehearsal disagreement census
- **Primitive:** the measurement that decides (b). In the stacked baseline (a competence probe plus separately stored rehearsal data), count how often the probe says "lapsed" but rehearsal on the stored data doesn't fix what the probe measures, or fixes it without restoring the behaviour. The *disagreement rate* is a property of a format pair.
- **Mechanism:** For each lapse event, run rehearsal from the stored data and re-probe. Also run a behavioural check unrelated to both. Record the four outcomes. Do the same with merged reward entries.
- **Nearest prior / gap:** [Three-interface diagnosis of CL in LMs](https://arxiv.org/abs/2611.30151) and [Near-Zero Forgetting Is Not Enough](https://arxiv.org/abs/2611.31511) show that metrics disagree. The gap: disagreement between *the detector and the repair* of one archive.
- **Cheapest first test:** MiniGrid, 20 behaviours, 5 lapse cycles. Kill rule from the review: if disagreement is under 10% in the stacked baseline, retire OE2-22 and every card in this section that depends on it.
- **Old-task retention:** Behavioural success after each repair.
- **Risk / likely tie:** This is the kill test, not a mechanism; it goes first.

### OE3-19 · The revival row as an entry's descriptor
- **Primitive:** describe each archive entry by its *revival row*, how much optimizing its stored reward restores every other lapsed entry. The descriptor is made of relearning effects, so entries that rehearse each other sit close together and novelty means "revives nothing we have".
- **Mechanism:** For each reward entry, optimize briefly from a perturbed fork and record recovery across entries. Novelty of a new behaviour = distance of its (estimated) revival row to retained rows. The descriptor updates as the graph changes.
- **Nearest prior / gap:** OE2-01 used competence signatures (passes right after producing a behaviour); successor-feature task vectors describe tasks by rewards. The gap: a descriptor defined by *what an entry's rehearsal restores*.
- **Cheapest first test:** MiniGrid, 30 behaviours. Arms at equal steps: hand descriptors, competence signatures (OE2-01), revival rows. Kill if revival rows don't give better worst-behaviour retention than competence signatures.
- **Old-task retention:** Worst-behaviour success at the end.
- **Risk / likely tie:** Revival rows cost one fork per entry; estimate with a learned predictor and report its error.

### OE3-20 · Objective revival versus data revival
- **Primitive:** the direct test of why an objective should beat data as a carrier. Relearning a root by *optimizing its stored reward* (on-policy) may revive more neighbours than relearning by *SFT on its stored trajectories* (off-policy), because on-policy rollouts visit the neighbours' states.
- **Mechanism:** For each root, measure the revival row under both formats at equal steps. Compare out-degree and the size of the revival basis. If objectives revive more, (b) gains a reason beyond storage size.
- **Nearest prior / gap:** [Self-Distillation Enables Continual Learning](https://arxiv.org/abs/2601.19897) and [RL Forgets! Towards Continual Policy Optimization](https://arxiv.org/abs/2607.04364) compare on-policy and SFT for *forgetting*; [Agentic-OPD](https://arxiv.org/abs/2611.12799) recovers skills on-policy. The gap: comparing them for *collateral revival*.
- **Cheapest first test:** MiniGrid and Craftax-Classic, 12 skills. Kill if objective relearning's out-degree is not above SFT's by a CI-separated margin at 10 seeds.
- **Old-task retention:** Neighbour revival under each format.
- **Risk / likely tie:** On-policy steps cost environment interactions; equalize total samples.

### OE3-21 · Cluster rewards: one objective that revives a mode
- **Primitive:** write a single reward program per revival mode (OE3-02), a short composition of entry rewards, whose optimization revives the whole mode. It is the objective-space version of a revival key.
- **Mechanism:** Search compositions (weighted sum, min, sequence) of the mode's entry rewards by length, scored by revival of the mode after brief optimization. Store cluster rewards for rehearsal.
- **Nearest prior / gap:** [Option Keyboard](https://arxiv.org/abs/2106.13105) and GPI compose rewards to *produce* new behaviour; OE3-10 keys live in data space. The gap: a composed objective chosen to *revive* a measured cluster.
- **Cheapest first test:** Crafting world with 4 modes of 5 skills. Arms at equal steps: per-entry rehearsal, revival keys (OE3-10), cluster rewards. Kill if cluster rewards don't beat per-entry rehearsal on mode retention.
- **Old-task retention:** Per-skill success within each mode.
- **Risk / likely tie:** Must beat the union of OE3-10 and per-entry rehearsal (merge rule).

### OE3-22 · Reward-machine entries localize the lapse
- **Primitive:** store each entry as a small *reward machine* (an automaton over subgoal events), not a flat reward. The probe reports *which stage* lapsed, and rehearsal optimizes only that stage's reward. A lapse becomes a location inside a skill.
- **Mechanism:** Write the entry as a reward machine (LM-written, as in ARM-FM, or inferred from trajectories as in active RM inference). Probe per stage. Revival is measured between stages, so shared subgoal stages across skills become hubs.
- **Nearest prior / gap:** [ARM-FM](https://arxiv.org/abs/2510.14176) and [active reward-machine inference](https://arxiv.org/abs/2604.07480) build RMs for learning tasks. The gap: RMs as *retention entries*, with stage-level lapse and stage-level revival.
- **Cheapest first test:** Multi-stage Craftax-Classic skills that share early stages. Arms at equal steps: flat reward entries, reward-machine entries. Kill if stage-level rehearsal doesn't restore skills in fewer steps.
- **Old-task retention:** Per-stage and whole-skill success.
- **Risk / likely tie:** Hand-designed event detectors make it easy; the detectors must be learned or LM-written.

### OE3-23 · Consistency-trained entries: make probe and reward agree
- **Primitive:** store a probe *and* a reward per entry as two separate programs, and treat their agreement as a training target. When they disagree on a rollout, refine whichever is wrong against ground truth. The entry is the consistent pair.
- **Mechanism:** Probe = verifier with negative tests; reward = shaped objective for regrowth. A disagreement (high reward, probe fail, or the reverse) triggers counterexample refinement of the reward (OE2-12) or the probe. The census rate (OE3-18) is driven down by construction.
- **Nearest prior / gap:** OE2-22 uses one program for both jobs; reward-model ensembles flag hacking by disagreement ([RMB](https://arxiv.org/abs/2609.33221)). The gap: probe–reward consistency as the *definition* of a valid retention entry.
- **Cheapest first test:** MiniGrid with reward-hackable tasks. Arms: single-program entries, two-program consistent entries. Kill if consistent entries don't show fewer hacked regrowths at equal steps.
- **Old-task retention:** Behavioural success after regrowth, checked by an independent evaluator.
- **Risk / likely tie:** Two programs cost more bytes; count them.

### OE3-24 · Entry lifetime law: does a shorter objective lapse slower?
- **Primitive:** a testable law relating an entry's *reward length* to its lapse hazard and its revival in-degree. Short-objective skills may be stored in more general weights, so they lapse slower and are revived by more neighbours.
- **Mechanism:** Across many entries, regress lapse hazard and in-revival on reward length, controlling for difficulty and training steps.
- **Nearest prior / gap:** OE2-17 claimed short rewards regrow more general skills; MDL theories of generalization. The gap: length of the stored objective as a predictor of retention dynamics.
- **Cheapest first test:** 40 MiniGrid behaviours with LM-written rewards. Kill if length explains less than 10% of the variance in hazard after difficulty is controlled.
- **Old-task retention:** It is the measured hazard.
- **Risk / likely tie:** Length may proxy for difficulty; matching is essential.

### OE3-25 · Checker-entry revival graph in a language model
- **Primitive:** the LM testbed for this whole node. Entries are checker programs plus prompt generators (OE2-20). The revival graph is measured over code families through RLVR on one family's checker, and the basis, modes and frustration are computed on a real 0.5B–1.5B model.
- **Mechanism:** Learn 12 code families in sequence and induce forgetting with a 13th domain. For each family, run k RLVR steps on its checker and measure recovery of the others. Compute OE3-01–OE3-03 statistics.
- **Nearest prior / gap:** [Localizing Transfer Between Memorization Tasks](https://arxiv.org/abs/2610.00771) studies forward transfer in LMs; relearning-attack work measures revival only for unlearned data. The gap: the full revival relation over an LM's own skills under RLVR.
- **Cheapest first test:** Qwen2.5-0.5B-Instruct with LoRA, 12 families × 10 seeds. Kill if no edge passes the nonspecific control at 10 seeds (then revival structure is not real at LM scale).
- **Old-task retention:** Fresh-instance accuracy per family and a base benchmark.
- **Risk / likely tie:** Syntax-driven nonspecific revival ([2602.03379](https://arxiv.org/abs/2602.03379)) may dominate; the control is required.

### OE3-26 · Revival-weighted objective archive as a self-model
- **Primitive:** together, the set of reward entries and their signed revival graph form a compact *model of the learner's skills*: what it values (rewards), how those skills connect (revival), and where they compete (frustration). It can forecast the retention cost of a planned update before any training.
- **Mechanism:** For a candidate new task, write its reward and estimate its signed revival row against the archive from one short fork. Forecast which entries will lapse (negative edges) and which hubs will cover them. Accept, defer or give the task separate capacity based on the forecast.
- **Nearest prior / gap:** Interference forecasting from gradient overlap; the root's OE11 learner-dynamics model predicts competence change from task features. The gap: forecasting from the learner's *own objective archive and revival structure*, read off one fork.
- **Cheapest first test:** MLP host, 20 archive entries, 10 candidate new tasks. Kill if the archive forecast doesn't beat gradient-overlap forecasting on which entries lapse.
- **Old-task retention:** Retention after the forecast-guided accept/defer policy against accepting everything.
- **Risk / likely tie:** This sits close to machinery; it stands only if the forecast beats gradient overlap.

---

## Ranked deeper questions

1. **Is revival structure real, specific and low-dimensional? (OE3-01, OE3-02, OE3-03, OE3-25)**
   First, at 10 seeds and against the nonspecific-revival control, show that revival edges exist beyond equal-size unrelated relearning, in an MLP and in a 0.5B LM. Then test whether the revival basis recovers planted latent factors and whether signed revival shows frustration. If edges don't replicate, this whole line and OE2-03 stop.
2. **Does an objective carry more than data, and do probe and rehearsal disagree? (OE3-18, OE3-20, OE3-23)**
   Run the disagreement census on the stacked baseline. If it is under 10%, retire the reward-entry merge. If it is higher, test whether optimizing stored rewards revives more neighbours than SFT on stored trajectories at equal samples. That is the only reason for (b) beyond storage size.
3. **Can revival be designed rather than found? (OE3-10, OE3-11, OE3-12, OE3-21)**
   Revival keys, designed hubs, relearnability protection and cluster rewards each try to *build* latent links. Test each against its found-revival counterpart and replay at equal compute and bytes.
4. **What does revival tell us that output probes can't? (OE3-05, OE3-06, OE3-08, OE3-16)**
   Label-free task identity, edge lifetimes, cause fingerprints and unlearning by path closure all read the relearning relation as information. Each must beat the single-skill measurement it extends (loss-spike boundaries, item hazards, savings, forget-set relearning).
