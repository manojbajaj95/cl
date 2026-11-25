# Open-ended learners 4: dormant skills, revival keys and paging

Depth 3 · child of [PR #386](https://github.com/manojbajaj95/cl/pull/386) (`tree/open-ended-learners-3.md`) OE3-12 and OE3-10 · 26 cards (OE4-01–OE4-26) · 4 ranked deeper questions · Ideas only; no experiments run

**What the reviewer kept, and what is missing.**
- **(a) Protect relearnability, not outputs (OE3-12).** Penalize updates that reduce scratch-copy revival of protected clusters through their hubs. Controls: EWC, LwF, replay, and top-10 #5 (relearning as the read head) as the readout.
- **(b) Tiny synthetic revival keys (OE3-10).** A few optimized synthetic examples whose short training run revives a whole forgotten cluster. Controls: dataset distillation, an equal-byte coreset, generative replay, reward programs.

As written, (a) needs a fork per check and does not say what is gained by letting outputs fade. (b) is dataset distillation aimed at revival, and it does not say why a key should beat a stored weight delta, how long it lasts, or where it comes from.

Taken together, they suggest one new object: a **dormant skill**. Its outputs are gone, its latent links are protected, and it can be woken by a key and put back to sleep by an anti-key. The cards below build that object out:
- a differentiable revival loss that removes the forks
- a revival-null subspace larger than the output-null space
- a dormancy exchange rate (how many dormant skills fit in the space of one expressed skill)
- keys planted at acquisition or minted against simulated forgetting
- keys that are weight-conditioned deltas rather than stored ones
- reversible on/off toggles
- paging: a bounded expressed working set over an unbounded dormant store

**Scope and controls.** The parent's rules carry over: the nonspecific-revival control, 10-seed replication, the merge rule, and equal bytes and compute. Two new controls apply throughout: a *stored task vector* (ΔW at equal bytes), the strongest rival to any key, and *few-shot real data* at the key's size. The learner-world branch's one-step hibernation (L5W03 / L6W19 in [PR #368](https://github.com/manojbajaj95/cl/pull/368)) caps *deployed* competence for world reasons. Dormancy here has a different job, freeing capacity and avoiding interference, and cards that come close to that branch say so.

## Literature check

alphaXiv searches (8 new queries): dataset distillation for continual learning, meta-learning for fast relearning, capability elicitation from few examples, loss-landscape basins and relearnability, model inversion for data-free CL, hypernetwork CL, robustness and transfer of distilled data, and mode connectivity.

| Line | Already available | What this node must add |
|---|---|---|
| Distilled replay | [Data-Distill-Net](https://arxiv.org/abs/2505.20135), [Prototypical Exemplar Condensation](https://arxiv.org/abs/2603.13804), [Hybrid Memory Replay](https://arxiv.org/abs/2410.15372), [Distilling RL into Single-Batch Datasets](https://arxiv.org/abs/2508.09283), [trajectory matching](https://arxiv.org/abs/2203.11932), [robust DD by adversarial trajectories](https://arxiv.org/abs/2503.12069), [DD by influence matching](https://arxiv.org/abs/2607.16859), [The Composition Gap in DD](https://arxiv.org/abs/2609.34343) | Distilled sets are trained to *teach a task from scratch* or to replay a task. None is optimized to *revive* a lapsed cluster from the current weights, planted at acquisition, or paired with a suppressing anti-key. |
| Relearnability as a target | [Re-Evaluating CL with Few-Shot Adaptation](https://arxiv.org/abs/2606.03843) (evaluates CL by relearnability), [Meta-Unlearning against relearning](https://arxiv.org/abs/2410.12777), [Maximizing Relearning Convergence Delay](https://arxiv.org/abs/2604.09391), [Margin calibration for relearn-robust unlearning](https://arxiv.org/abs/2607.27836), [Unlearning through Mode Connectivity](https://arxiv.org/abs/2607.23970), [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637), [OML](https://arxiv.org/abs/1905.12588) | Relearnability is *measured* in CL or *minimized* in unlearning. Nobody *maximizes* it as the protected quantity while letting outputs go, or prices the capacity this frees. |
| Waking hidden skills | [Awakening the Sleeping Agent](https://arxiv.org/abs/2604.08388) (unrelated agentic data reactivates general tool use), [Reference-Grafting](https://arxiv.org/abs/2608.29458) and [structural interventions](https://arxiv.org/abs/2611.31615) for sandbagged capabilities, [elicitation vs creation](https://arxiv.org/abs/2605.08368), [spurious forgetting](https://arxiv.org/abs/2610.08718), [transport keys](https://arxiv.org/abs/2606.02860) | Waking is found by accident or by search. No method *designs* the wake signal, pairs it with a sleep signal, or uses dormancy as a memory tier. |
| Weight generators | [Continual learning with hypernetworks](https://arxiv.org/abs/1906.00695), [Learning to Recover Task Experts from a Merged Model](https://arxiv.org/abs/2606.26902), [Merge++ checkpoint inversion](https://arxiv.org/abs/2609.22886), [model inversion for data-free CL](https://arxiv.org/abs/2605.11804), latent replay (Pellegrini et al. 2020) | They store or generate *weights or data for a task*. A key is different: a *weight-conditioned* update generator, since the same few examples produce whatever delta the current weights need to revive the cluster. |

---

## A · Making relearnability the protected quantity

### OE4-01 · The revival lookahead loss
- **Primitive:** a differentiable surrogate for "does relearning the hub still revive the cluster", requiring no fork: L_rev(θ) = Σ_{B∈cluster} L_B(θ − η ∇L_hub(θ)), a one-step lookahead through the hub's gradient. Adding λ·L_rev to the new-task loss makes (a) as cheap as a second-order term.
- **Mechanism:** At each step on the new task, compute the hub gradient on a small hub batch, take the virtual step, evaluate cluster loss there, and backpropagate (or use a first-order approximation). The cluster's own current loss is *not* penalized, so outputs may fade.
- **Nearest prior / gap:** MAML and MER use lookahead to make *learning* fast or non-interfering; [Meta-Unlearning](https://arxiv.org/abs/2410.12777) uses relearning lookahead to *block* revival. The gap: lookahead through a *hub* to *preserve* a cluster's revival while allowing its outputs to drop.
- **Cheapest first test:** MLP on 30 families with planted clusters, then an interfering phase, under a capacity bottleneck. Arms at equal compute: EWC, LwF, replay, fork-based OE3-12, revival lookahead. Kill if lookahead doesn't match fork-based OE3-12 on revived competence at less than a quarter of the compute.
- **Old-task retention:** Cluster competence before and after k hub-relearning steps (both reported), plus new-task accuracy.
- **Risk / likely tie:** One step may not predict k-step revival; test with k = 1, 5, 20.

### OE4-02 · The revival-null subspace
- **Primitive:** the subspace of weight directions that change a protected skill's *outputs* but not its *revival* (hub relearning still restores it). It contains the output-null space that OGD/GPM protect and is larger, so new learning gets more room.
- **Mechanism:** Estimate the Jacobian of the revival map (cluster loss after a hub step) with respect to θ on a few batches. Take its low-rank row space and project new-task gradients off that space only. Directions that touch cluster outputs but not revival stay open.
- **Nearest prior / gap:** OGD ([1910.07104](https://arxiv.org/abs/1910.07104)) and GPM ([2103.09762](https://arxiv.org/abs/2103.09762)) project off output-gradient spaces; [Interference and Retention in CL](https://arxiv.org/abs/2607.09202) analyzes interference geometry. The gap: projecting off the *revival* map instead of the output map.
- **Cheapest first test:** Same host. Measure the dimension of the protected space under GPM against revival-null. Kill if the revival-protected space isn't at least 30% smaller than GPM's, or if new-task accuracy at equal revived competence doesn't improve.
- **Old-task retention:** Revived cluster competence after k hub steps.
- **Risk / likely tie:** The two maps may share their top directions; then the gain is small.

### OE4-03 · The dormancy exchange rate
- **Primitive:** a law to measure: at fixed capacity, how many *dormant* (revivable) skills can be held in place of one *expressed* skill. If the rate is well above 1, protecting relearnability rather than outputs has a capacity price that can be counted, and memory should be tiered.
- **Mechanism:** Sweep capacity (width, LoRA rank). At each, find the largest number of skills held expressed (output-protected) and the largest number held dormant (revival-protected, OE4-01) at the same tolerance. The ratio is the exchange rate; fit how it scales with capacity.
- **Nearest prior / gap:** Capacity results for CL count expressed tasks; top-10 #5 (relearning as the read head) treats relearning as a channel. The gap: a measured ratio between the two storage tiers.
- **Cheapest first test:** MLP widths {32, 64, 128, 256} × LoRA ranks {1, 2, 4, 8}. Kill if the rate is below 1.5 at every capacity.
- **Old-task retention:** It is the measured quantity (expressed and revived competence).
- **Risk / likely tie:** A law card; it decides whether the tiered cards below are worth building.

### OE4-04 · Relearnability as a dial: signed revival targets
- **Primitive:** one operator that sets each cluster's revival to a *target*: high (keep dormant but revivable), zero (forget for real), or current (leave alone). Continual learning and unlearning become two settings of the same dial.
- **Mechanism:** Add Σ_c w_c · L_rev,c with w_c > 0 for keep-dormant clusters and w_c < 0 for forget clusters (relearning-delay unlearning). The forget side is certified by the closure check from OE3-16.
- **Nearest prior / gap:** [Synaptic role partitioning for simultaneous CL and unlearning](https://arxiv.org/abs/2611.24205) and [forget–recover networks](https://arxiv.org/abs/2608.03123) treat the two jobs with separate mechanisms. The gap: one signed revival target across clusters.
- **Cheapest first test:** MLP and 0.5B LoRA, 3 keep clusters and 1 forget cluster. Kill if the signed dial doesn't beat separate CL plus unlearning methods on both revived keep-competence and forget-cluster relearning delay.
- **Old-task retention:** Revived keep-cluster competence; non-target cluster outputs.
- **Risk / likely tie:** The two signs may fight in shared weights; report the frustration (OE3-03).

### OE4-05 · Expression adapters over a latent base
- **Primitive:** an architectural split in which the base weights hold only *relearnability* (latent links, protected by OE4-01) and every skill's *expression* lives in a small removable adapter. Removing an adapter makes a skill dormant; a key re-trains it in a few steps.
- **Mechanism:** Train the base with revival protection across all clusters; train per-cluster LoRA for expression. To drop expression, delete the adapter (no data kept). To wake, train a fresh adapter on the cluster's key. The base never needs output protection.
- **Nearest prior / gap:** Adapter-per-task CL keeps adapters forever; [Hypernetwork CL](https://arxiv.org/abs/1906.00695) generates weights per task. The gap: adapters that are *disposable*, because the base is trained to make them cheap to regrow.
- **Cheapest first test:** 0.5B model, 10 families. Arms at equal bytes: keep all adapters, keep keys and delete adapters (with revival-protected base), keep keys and delete adapters (plain base). Kill if the revival-protected base doesn't cut regrowth steps by half against the plain base.
- **Old-task retention:** Regrown competence per family, and the base's general benchmark.
- **Risk / likely tie:** Storing adapters may be cheap enough that dormancy isn't needed; the card stands on storage-limited settings.

---

## B · Keys as a memory object

### OE4-06 · Keys are weight-conditioned deltas
- **Primitive:** the reason a key should beat a stored task vector. A stored ΔW is fixed and goes stale as the weights drift. A key produces, through a short training run, *whatever* delta the current weights need. A key is a generator of updates conditioned on the weights it is applied to.
- **Mechanism:** At mastery, store both a task vector ΔW (or a LoRA) and a key of equal bytes. After increasing amounts of drift, compare revival from adding ΔW against revival from training on the key.
- **Nearest prior / gap:** Task arithmetic and TIES store fixed deltas; dataset distillation stores data for training from scratch; [Learning to Recover Task Experts](https://arxiv.org/abs/2606.26902) recovers experts from a merged model. The gap: the drift-conditioning of a key as its defining advantage.
- **Cheapest first test:** MLP and 0.5B LoRA, drift = training on 1–5 later families. Kill if keys don't beat stored task vectors at equal bytes once drift passes one family.
- **Old-task retention:** Revived competence against drift amount, for both formats.
- **Risk / likely tie:** At low drift the task vector wins; the claim is about the crossover.

### OE4-07 · Future-proof keys: optimized over the weights to come
- **Primitive:** a key optimized not for today's weights but for a *distribution of future weights*: simulated drifts, sampled by continuing training on plausible later tasks. Its revival holds for a stated horizon, its *key half-life*.
- **Mechanism:** Bilevel with an outer expectation over simulated futures θ' ~ p(θ' | θ) (forks trained on random or held-out tasks): minimize E_θ'[cluster loss after k key steps from θ']. Report half-life against actual later training.
- **Nearest prior / gap:** [Robust DD by adversarial trajectories](https://arxiv.org/abs/2503.12069) and [robust trajectory distillation](https://arxiv.org/abs/2606.29837) make distilled data robust to training noise. The gap: robustness to the *learner's future continual drift*, which is the property a retention format needs.
- **Cheapest first test:** MLP, 30 families. Arms at equal bytes: keys optimized at current weights, future-proof keys. Kill if future-proof keys' half-life isn't at least 2× longer.
- **Old-task retention:** Revival at 1, 3, 10 later families.
- **Risk / likely tie:** Simulated futures may differ from real ones; use held-out task types.

### OE4-08 · Planted keys: co-train the lock with the skill
- **Primitive:** instead of searching for a key after forgetting, *plant* one at acquisition. While learning a skill, train the network so that a fixed, random synthetic set (the key) will revive it later. The network is shaped to respond to its own key.
- **Mechanism:** During acquisition of cluster c, add a meta-term: after a simulated forgetting perturbation, k steps on a fixed random key K_c must restore c. K_c is never optimized; the weights are. Keys then cost almost nothing to store (a seed).
- **Nearest prior / gap:** Backdoors plant triggers for *behaviour at inference*; the parent's OE3-11 builds hubs out of real skills. The gap: a trigger for *relearning*, planted on purpose for retention.
- **Cheapest first test:** MLP, 20 families, planted keys of 4 random examples (stored as seeds). Arms: optimized keys after forgetting (OE3-10), planted keys, few-shot real data of the same size. Kill if planted keys don't match optimized keys' revival.
- **Old-task retention:** Revived competence per family; acquisition accuracy must not drop.
- **Risk / likely tie:** Second-order cost at acquisition; a first-order version may be enough.

### OE4-09 · Minted keys: optimized at mastery against simulated forgetting
- **Primitive:** mint a key *while the skill is still held*, using the current model as the target. The key is optimized so that a *simulated forgotten* copy, trained briefly on it, matches the current model on the cluster. No weights change, and no task data is needed after minting.
- **Mechanism:** At mastery: sample forgetting perturbations (interfering training on random tasks), then optimize K so that k steps on K bring each perturbed copy's outputs back to the current model's outputs on generated inputs (model-inversion style, data-free).
- **Nearest prior / gap:** [Model inversion for data-free CL](https://arxiv.org/abs/2605.11804) synthesizes replay data from the old model; [Merge++](https://arxiv.org/abs/2609.22886) inverts checkpoints for merging. The gap: inversion targeted at *revival from forgotten states*, done once at mastery.
- **Cheapest first test:** MLP and 0.5B LoRA. Arms at equal bytes: inversion replay, a coreset, minted keys. Kill if minted keys don't beat inversion replay on revival after real forgetting.
- **Old-task retention:** Revived competence after a real interfering phase.
- **Risk / likely tie:** Simulated forgetting may not match real forgetting.

### OE4-10 · Anti-keys and reversible toggles
- **Primitive:** pair each key with an *anti-key*, a few synthetic examples whose short training run *suppresses* a cluster's expression without breaking its revival. A skill can be switched off and on with a handful of training steps, and the switch is reversible.
- **Mechanism:** Optimize the anti-key so that k steps lower cluster performance while revival under the key stays above threshold (OE4-01 loss as the constraint). A toggle cycle is anti-key → (other learning) → key.
- **Nearest prior / gap:** Unlearning suppresses with an aim of permanence; relearning attacks undo it; the learner-world branch's hibernation caps expressed competence. The gap: designed, reversible on/off by training, used as a CL operation.
- **Cheapest first test:** MLP, 10 clusters, 5 toggle cycles each. Kill if revival after the 5th cycle falls below 80% of the first, or if anti-keys damage other clusters more than plain gradient ascent does.
- **Old-task retention:** Per-cluster competence after each on and off phase; untouched clusters stay put.
- **Risk / likely tie:** Toggling may wear down the latent links; the 5-cycle check measures that.

### OE4-11 · Key superposition and key capacity
- **Primitive:** one key that revives *several* clusters at once by superposition, and a capacity law for keys: how many clusters a key of b bytes can revive before they interfere.
- **Mechanism:** Optimize a joint key for clusters {c1…cm} with a summed revival loss. Sweep m and key size, and fit clusters revived as a function of bytes. Compare with concatenating single keys.
- **Nearest prior / gap:** [The Composition Gap in DD](https://arxiv.org/abs/2609.34343) shows distilled sets compose poorly for training from scratch. The gap: composition for *revival*, where the shared latent structure may make superposition cheap.
- **Cheapest first test:** MLP, 30 families in 6 clusters. Kill if a joint key doesn't revive more clusters per byte than concatenated single keys.
- **Old-task retention:** Per-cluster revived competence.
- **Risk / likely tie:** Like distilled data, keys may not compose.

### OE4-12 · Key hierarchies: coarse keys for modes, fine keys for skills
- **Primitive:** a two-level key code: a coarse key revives a revival mode (OE3-02), and small fine keys add the residual per skill. The byte cost falls as in hierarchical coding.
- **Mechanism:** Optimize the coarse key on the mode. Then, from the state after the coarse key, optimize tiny fine keys per skill. Store both levels. Wake a single skill with coarse plus fine.
- **Nearest prior / gap:** Hierarchical and residual vector quantization; key superposition (OE4-11). The gap: a residual code for *relearning signals*.
- **Cheapest first test:** MLP, 4 modes × 5 skills. Arms at equal bytes: flat per-skill keys, hierarchy. Kill if the hierarchy doesn't revive more skills at equal bytes.
- **Old-task retention:** Per-skill revived competence.
- **Risk / likely tie:** Little gain if modes are weak.

### OE4-13 · Procedural keys: a seed and a tiny generator
- **Primitive:** store a key not as examples but as a *program*: a seed plus a tiny generator network (or a short symbolic program) that emits the synthetic examples. The bytes drop further, and the generator can emit fresh key variants so the key is not memorized.
- **Mechanism:** Optimize the generator's parameters (a few hundred) so that its emitted batches revive the cluster. At rehearsal, sample a fresh batch from the generator.
- **Nearest prior / gap:** Generative replay keeps a full generator per domain; the root's OE01 task keys regenerate tasks from seeds; DD parameterizations (factorized, frequency-domain) shrink distilled sets. The gap: a parametric generator *of revival signals*, sized far below a generative replay model.
- **Cheapest first test:** MLP, 30 families. Arms at equal bytes: explicit keys, procedural keys, generative replay at the same parameter count. Kill if procedural keys don't beat explicit keys at equal bytes.
- **Old-task retention:** Revived competence per family.
- **Risk / likely tie:** A tiny generator may only emit near-duplicates.

### OE4-14 · Discrete revival keys for language models
- **Primitive:** keys for LMs as a few *synthetic token sequences* (found by discrete optimization), which when fine-tuned on for a few steps revive a forgotten capability. The discrete version of keys makes them readable, storable as text and portable across tokenizers.
- **Mechanism:** GCG-style coordinate search over token sequences and targets, scoring cluster accuracy after k LoRA steps on the candidate. Keep the shortest sequences that pass the nonspecific-revival control.
- **Nearest prior / gap:** [Awakening the Sleeping Agent](https://arxiv.org/abs/2604.08388) finds that unrelated agentic data reactivates tool use; [Reference-Grafting](https://arxiv.org/abs/2608.29458) elicits sandbagged skills; GCG optimizes prompts for *inference*. The gap: optimized text for *training-time revival*.
- **Cheapest first test:** Qwen2.5-0.5B, 10 code families forgotten after a math phase. Arms at equal tokens: real few-shot data, random synthetic text, discrete keys. Kill if discrete keys don't beat real few-shot data on revived accuracy.
- **Old-task retention:** Fresh-instance accuracy per family plus a base benchmark.
- **Risk / likely tie:** Discrete search is costly at scale.

### OE4-15 · Latent keys: synthetic activations instead of inputs
- **Primitive:** keys that live at an intermediate layer: synthetic activations plus targets that train only the layers above. They are cheaper to optimize and apply, and they skip input-space constraints.
- **Mechanism:** Choose the layer where the cluster's revival Jacobian is largest. Optimize synthetic activations so that k steps on the upper layers revive the cluster. Lower layers are protected by OE4-01.
- **Nearest prior / gap:** Latent replay (Pellegrini et al. 2020) stores real activations; latent-space DD for generative models. The gap: *optimized* activations for revival, with protection of the layers below.
- **Cheapest first test:** MLP and a small CNN. Arms at equal bytes: input keys, latent keys, latent replay. Kill if latent keys don't beat latent replay.
- **Old-task retention:** Revived competence per cluster.
- **Risk / likely tie:** If lower layers drift, latent keys break; protecting them is part of the card.

### OE4-16 · Keys that cross model versions
- **Primitive:** a key optimized on one model that revives the same cluster in a *sibling* model (another fine-tune of the same base, or a later checkpoint). Keys become portable skill seeds between versions.
- **Mechanism:** Optimize the key jointly on several siblings, then test it on a held-out sibling. Compare with transferring task vectors (which need aligned weights) and with distilled data.
- **Nearest prior / gap:** Cross-architecture DD; Trans-LoRA moves adapters through synthetic data. The gap: transfer of *revival* signals, which rely on shared latent structure from the common base.
- **Cheapest first test:** 0.5B base with 5 sibling fine-tunes that each forgot a cluster. Kill if the held-out sibling's revival from the joint key is under half of what its own optimized key achieves.
- **Old-task retention:** Revived competence in the held-out sibling.
- **Risk / likely tie:** Siblings that differ widely may share little latent structure.

### OE4-17 · Checkpoint keys: a key that restores an old model
- **Primitive:** a single key set that brings back a *whole previous checkpoint's behaviour* across all its skills after a large update, replacing the stored checkpoint for rollback.
- **Mechanism:** After a big update, optimize a key so that k steps from the new weights restore the old model's outputs across a broad generated input set (behavioural distance), while the new skill is kept (constrained). Rollback = train on the key.
- **Nearest prior / gap:** Counterfactual rollback (the repo's concept) and checkpoint storage; [Agentic-OPD](https://arxiv.org/abs/2611.12799) recovers capabilities by on-policy distillation from discarded checkpoints. The gap: a key-sized rollback signal for a whole model.
- **Cheapest first test:** 0.5B LoRA, 1 large interfering update. Arms at equal bytes: stored LoRA delta, distilled data, checkpoint key. Kill if the checkpoint key doesn't restore more old-benchmark accuracy per byte than the stored delta.
- **Old-task retention:** Old benchmark accuracy after rollback, with new-skill retention reported.
- **Risk / likely tie:** A LoRA delta is already small; the claim rests on drift after the update (OE4-06).

### OE4-18 · Keys in RL: synthetic transition batches that revive a policy cluster
- **Primitive:** the RL form of a key: a tiny synthetic batch of transitions (states, actions, targets) whose short training run revives a cluster of policies. This is the direct rival to the stored reward programs of OE2 and OE3.
- **Mechanism:** Optimize the synthetic transitions for revival of cluster returns after k policy-gradient or BC steps, starting from [single-batch RL distillation](https://arxiv.org/abs/2508.09283). Compare with reward-program regrowth at equal bytes and steps.
- **Nearest prior / gap:** Single-batch RL distillation trains a policy from scratch; OE2-22 stores rewards. The gap: synthetic transitions for *revival*, judged against stored objectives.
- **Cheapest first test:** MiniGrid, 12 skills in 3 clusters. Arms at equal bytes and equal environment steps: trajectory replay, reward programs, RL keys. Kill if RL keys don't beat reward programs on revived cluster return.
- **Old-task retention:** Return per skill after revival.
- **Risk / likely tie:** Reward programs need environment steps and keys don't; equalize total compute.

---

## C · Paging, multiplexing and dormancy as a memory tier

### OE4-19 · Paging for skills: a bounded expressed set over an unbounded dormant store
- **Primitive:** treat skills like virtual memory. A small *expressed working set* is output-protected. Every other skill is *dormant*, with only revival protected, and is paged in by a key and out by an anti-key or by letting it fade. The open-ended learner can invent indefinitely while expressing a bounded set.
- **Mechanism:** Page-fault = a task arrives for a dormant skill → train on its key (page in). Eviction policy = least recently used, with OE4-10 anti-keys or natural fading. The base is trained with OE4-01 on all clusters, expressed or not.
- **Nearest prior / gap:** Adapter swapping and MoE routing keep every skill's weights; spaced repetition keeps everything expressed. The gap: a two-tier skill memory where the lower tier costs only revival protection and a key.
- **Cheapest first test:** MLP and 0.5B LoRA, 40 families with capacity for 10 expressed. Arms at equal capacity and storage: replay of all, adapter swap with adapters stored, paging with keys. Kill if paging doesn't give the highest competence after page-in, averaged over all 40, at equal storage.
- **Old-task retention:** Competence after page-in for each family, and expressed-set competence throughout.
- **Risk / likely tie:** Page-in latency (key steps) has to be acceptable; report it.

### OE4-20 · Time-multiplexing conflicting skills
- **Primitive:** skills that *conflict* (frustrated pairs, OE3-03) share weights by taking turns being expressed. The inactive one is dormant but revivable, and keys switch between them. Conflict is resolved in time rather than with new capacity.
- **Mechanism:** For a frustrated pair, keep both under revival protection, express one at a time, and switch with keys and anti-keys. Measure switching cost against the cost of separate capacity.
- **Nearest prior / gap:** Context-dependent gating (XdG), task-ID heads and separate adapters resolve conflict in space. The gap: resolving it in time through dormancy.
- **Cheapest first test:** MLP with planted contradictory pairs (same inputs, opposite labels). Arms at equal parameters: task-ID head, separate adapters, multiplexing. Kill if multiplexing needs more than 2× the parameters of task-ID heads, or loses accuracy after 5 switches.
- **Old-task retention:** Accuracy on both members after each switch.
- **Risk / likely tie:** A task-ID head is cheap; the card stands where task IDs are unavailable at training time.

### OE4-21 · Dormant storage on purpose (relearning as the write channel)
- **Primitive:** write a new skill *directly into dormancy*: train it so that it is revivable by its key but never expressed, so it doesn't interfere with current behaviour. It realizes top-10 #5 (relearning as the read head) as a deliberate write path.
- **Mechanism:** Train with loss = revival loss after key steps (OE4-01 form) plus a penalty on the skill's *expressed* accuracy. The skill exists only as relearnability until its key is applied.
- **Nearest prior / gap:** Top-10 #5 treats relearning speed as a readable channel; backdoor and sandbagging work hides capabilities. The gap: a CL write mode that stores without expressing, for skills that conflict with the current working set or aren't needed yet.
- **Cheapest first test:** MLP, 10 expressed families plus 10 written dormant. Arms: expressed writing of all 20, dormant writing for the second 10. Kill if dormant writing doesn't keep the first 10 better while the second 10 still revive within 20 key steps.
- **Old-task retention:** Expressed accuracy on the first 10; revived accuracy on the dormant 10.
- **Risk / likely tie:** This sits close to sandbagging; the safety implication goes in the card's risks, with an audit by key search (OE3-16).

### OE4-22 · Merge into dormancy
- **Primitive:** merge several fine-tuned models so that every source skill is *revivable* in the merge, even if not all are expressed. Each source's key wakes its skill set, and merging conflicts are resolved by dormancy rather than averaging.
- **Mechanism:** Merge objective = summed revival losses over sources' clusters (each with its key), plus the expressed loss for one primary source. Conflicting sources stay dormant.
- **Nearest prior / gap:** TIES, model soups and [Learning to Recover Task Experts from a Merged Model](https://arxiv.org/abs/2606.26902) aim for expressed merged skills or recovery modules. The gap: merging for *joint revivability*.
- **Cheapest first test:** 4 LoRA fine-tunes of a 0.5B base with conflicting tasks. Arms at equal bytes: TIES, task arithmetic, recovery modules, merge into dormancy plus keys. Kill if per-source accuracy after waking doesn't beat TIES.
- **Old-task retention:** Per-source accuracy after its key, and base benchmark.
- **Risk / likely tie:** Must beat stored per-source LoRAs at equal bytes.

### OE4-23 · Versioned edits by dormancy
- **Primitive:** a knowledge edit that overwrites a fact but keeps the old value *dormant and revivable*. Rollback is a key, not a stored inverse edit, and a fact's version history lives in its revival structure.
- **Mechanism:** When editing, add a revival loss for the old value (keyed by a small synthetic set) and a suppression term for its expression. To roll back, apply the key. To finalize, close the revival path (OE3-16).
- **Nearest prior / gap:** GRACE codebooks and MEMIT edits store replacements; rollback by a stored inverse edit or checkpoint. The gap: dormancy as the versioning mechanism.
- **Cheapest first test:** GPT-2 or 0.5B, 100 sequential edits. Arms: MEMIT plus stored inverse edits, GRACE, dormancy versioning. Kill if key rollback doesn't restore old values as accurately as inverse edits at equal bytes after 100 edits.
- **Old-task retention:** Unedited fact accuracy and general benchmark after edits and rollbacks.
- **Risk / likely tie:** Inverse edits are exact when the weights haven't drifted; the claim is after drift (OE4-06).

### OE4-24 · Dormancy-preserving distillation
- **Primitive:** distil a teacher into a student so that the student inherits the teacher's *dormant* skills too: it must be revivable by the teacher's keys, not only match its expressed outputs.
- **Mechanism:** Distillation loss = KL on expressed outputs + Σ_c revival loss of the student under the teacher's key K_c (matching the teacher's revived outputs). Keys transfer the latent tier.
- **Nearest prior / gap:** Knowledge distillation transfers expressed behaviour; [Re-Evaluating CL with Few-Shot Adaptation](https://arxiv.org/abs/2606.03843) shows relearnability differs between models with equal accuracy. The gap: distilling the latent tier itself.
- **Cheapest first test:** MLP teacher with 10 dormant clusters → smaller student. Arms: plain KD, KD + replay of dormant clusters, dormancy-preserving KD. Kill if the student's revival under the teacher's keys doesn't beat plain KD by a CI-separated margin.
- **Old-task retention:** Student's expressed accuracy and revived competence.
- **Risk / likely tie:** The student may lack capacity for latent links; sweep its size.

### OE4-25 · The key proposer: an open-ended loop that invents keys
- **Primitive:** the root's self-curriculum, turned to retention. The proposer invents *keys* instead of tasks, rewarded by clusters revived per byte. The loop's archive is a key bank, so open-ended invention now produces memory as well as new skills.
- **Mechanism:** The proposer emits candidate keys (procedural, OE4-13) for lapsed clusters found by the competence-tracking archive (OE2). Reward = revival per byte minus damage to the expressed set. Kept keys go to the bank; the proposer learns what revives.
- **Nearest prior / gap:** Self-play proposers (Absolute Zero, R-Zero) invent tasks for capability; dataset distillation is offline optimization. The gap: an *online proposer of revival signals* inside an open-ended loop.
- **Cheapest first test:** MLP host from OE2 with 30 families. Arms at equal compute: per-cluster bilevel key optimization (OE3-10), the key proposer. Kill if the proposer doesn't reach equal revival with less compute after 10 clusters.
- **Old-task retention:** Revived competence across all clusters.
- **Risk / likely tie:** The proposer may need many trials before it beats direct optimization.

### OE4-26 · Keys as the protection signal: key-stability regularization
- **Primitive:** the merge of (a) and (b). Protect relearnability *by keeping the stored keys working*: the protected quantity is the cluster's revival after k steps on its key, which needs no hub fork, uses only a few synthetic examples, and is differentiable by lookahead.
- **Mechanism:** L_protect = Σ_c L_c(θ − η∇L_{K_c}(θ)), a lookahead through the *key's* gradient instead of the hub's (OE4-01). Keys are re-minted (OE4-09) when they drift past half-life.
- **Nearest prior / gap:** Parts: OE3-12 and OE3-10. Merge rule: it must beat OE3-12 with hub forks *plus* OE3-10 keys used for rehearsal only, stacked at equal compute and bytes. The interaction it claims: protecting key responsiveness during learning makes keys last longer *and* makes protection cheaper than hub forks.
- **Cheapest first test:** MLP, 30 families with clusters, under a capacity bottleneck. Arms at equal compute and bytes: EWC, replay, OE3-12 fork protection, OE3-10 key rehearsal, both stacked, key-stability regularization. Kill if it doesn't beat the stacked parts on revived competence and new-task accuracy together.
- **Old-task retention:** Revived competence per cluster after k key steps, and expressed competence for the working set.
- **Risk / likely tie:** Protection may overfit to the key (the key keeps working but no longer reflects the cluster); check revival with fresh real data too.

---

## Ranked deeper questions

1. **Does protecting relearnability instead of outputs buy measurable capacity, cheaply? (OE4-03, OE4-01, OE4-02, OE4-26)**
   Measure the dormancy exchange rate first. If it is below 1.5, the tiered cards drop. If it is above, test whether the lookahead loss through hubs or keys matches fork-based protection at a fraction of the compute, and whether the revival-null subspace leaves more room than GPM.
2. **Are keys a better memory format than data, task vectors or reward programs? (OE4-06, OE4-07, OE4-18, OE4-13)**
   The single most important comparison is a key against a stored task vector at equal bytes after increasing drift (OE4-06). If keys don't win past one family of drift, keys are just compressed data. Then test half-life under future-proofing, RL keys against reward programs, and procedural keys against explicit ones.
3. **Can a learner page skills between an expressed set and a dormant store? (OE4-19, OE4-10, OE4-20, OE4-21)**
   Paging needs reversible toggles that don't wear down latent links over cycles, and a dormant write mode. Test 40 families on capacity for 10: average competence after page-in against replay and adapter swapping at equal storage.
4. **Where do keys come from: searched, planted, minted or proposed? (OE4-08, OE4-09, OE4-25, OE4-14)**
   Compare planted keys (shape the weights), minted keys (inversion at mastery), proposer-invented keys and discrete LM keys against bilevel search after forgetting, at equal bytes and compute.
