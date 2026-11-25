# Open-ended learners 5: codes, flows and engrams for dormant skills

Depth 4 · child of [PR #387](https://github.com/manojbajaj95/cl/pull/387) (`tree/open-ended-learners-4.md`) OE4-02 and OE4-08 · 26 cards (OE5-01–OE5-26) · 4 ranked deeper questions · Ideas only; no experiments run

**What the reviewer kept.**
- **(a) Revival-null protection (OE4-02).** Project new-task gradients off only the directions that would break a skill's revivability, a smaller protected set than OGD/GPM.
- **(b) Planted revival keys (OE4-08).** Shape the weights at learning time so that a fixed random synthetic set revives the skill after simulated forgetting.

The review warned that the last node drifted into *format variants* (keys as text, as activations, as generators). This node therefore avoids new formats and asks what kind of object (a) and (b) are. Three answers lead to genuinely new primitives:
- **(b) is a code.** Planting is *encoding*, interference is *noise*, and a short training run on the key is a *decoder*. That gives gradient-decodable codes, code-division multiplexing of dormant skills, and a lower bound on key length.
- **(a) is a statement about a dynamical system.** The relearning flow has a basin of attraction, so protection means staying in the basin. That gives a relearning-flow basin and cone, a pullback Fisher, updates that commute with revival, and an exact theory in deep linear networks.
- **Dormancy is what neuroscience calls a silent engram.** Tagging, reactivation before interference and reconsolidation are *operations* on dormant memories that ML has no counterpart for.

A final group asks what dormancy does *for an open-ended learner*: composing keys to make skills never trained, and novelty defined by revivability.

**Scope and controls.** The parent's controls carry over (stored task vector at equal bytes, few-shot real data at key size, nonspecific revival, 10 seeds, merge rule), plus the review's list for (b): post-hoc keys, minted keys, dataset distillation, coresets, task vectors and MAML. Unlike the learner-world branch's hibernation (#368), dormancy here serves capacity, interference and invention, never a deployment cap.

## Literature check

alphaXiv searches (8 new queries): backdoors and triggers as recovery mechanisms, null-space and Hessian projection in CL, watermarks that survive fine-tuning, silent engrams and reactivation in neuroscience, error-correcting codes in network weights, analytic theory of relearning in linear networks, random-projection and superposed memory, and self-repair after ablation.

| Line | Already available | What this node must add |
|---|---|---|
| Projection methods | [OGD](https://arxiv.org/abs/1910.07104), [GPM](https://arxiv.org/abs/2103.09762), [Learning in the Null Space: Small Singular Values](https://arxiv.org/abs/2602.21919), [Dually Constrained Parameter Projection](https://arxiv.org/abs/2611.29269), [Fisher-orthogonal projected natural gradient](https://arxiv.org/abs/2601.12816), [Hessian Null Space Continuation](https://arxiv.org/abs/2609.38081), [One-Step Curvature Probes Miss the Fitting Operator](https://arxiv.org/abs/2610.03952) | All of them protect *outputs or loss* at the current point. None protects a *flow* (where relearning would take the weights) or requires updates to *commute* with revival. |
| Things that survive fine-tuning | Watermarks robust to fine-tuning ([2505.01007](https://arxiv.org/abs/2505.01007), [backdoor watermark persistence](https://arxiv.org/abs/2501.02704)), [password-locked models](https://arxiv.org/abs/2405.19550), [Suppressing Misaligned Behaviors, Durably](https://arxiv.org/abs/2611.05358), [Does Fine-Tuning Undo Activation Steering?](https://arxiv.org/abs/2608.24988), [Homeopathic Learning](https://arxiv.org/abs/2611.10110) | They plant a *signal* or *lock a capability behind a prompt*. None plants a *training-time decoder* for a skill, or multiplexes many skills by code. |
| Codes in weights | [Real-numbered ECC for neural networks](https://arxiv.org/abs/2602.00076), [fault-tolerant NNs from biological codes](https://arxiv.org/abs/2202.12887), [keyed parity in weights](https://arxiv.org/abs/2611.02042), [superposed analog memory](https://arxiv.org/abs/2610.26118), [Kilobyte Models](https://arxiv.org/abs/2608.00860) | These codes are decoded by *arithmetic at inference* to fix hardware faults. Here the decoder is *gradient descent on a key*, and the noise is *later learning*. |
| Theory of forgetting and relearning | [Saxe et al. exact dynamics](https://arxiv.org/abs/1312.6120), [Lampinen & Ganguli](https://arxiv.org/abs/1809.10374), [A Dynamical Theory of LoRA in CL](https://arxiv.org/abs/2609.39367), [Exact Operator Framework for Forgetting](https://arxiv.org/abs/2604.13460), [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637) | Recoverability is described, not *designed*. There is no closed form for the revival-null space or for minimum key length. |
| Engrams and self-repair | Silent engrams reactivated by tagging (Ryan et al. 2015, *Science*), [retroactive interference and engram expression](https://doi.org/10.1101/2023.03.17.533126), [reactivation protects motor memories from interference](https://doi.org/10.1101/2025.06.26.661747), [Hydra effect](https://arxiv.org/abs/2307.15771), [Conditional Co-Ablation](https://arxiv.org/abs/2607.01940) | The neuroscience operations (tag, reactivate before interference, reconsolidate) have no ML counterpart for *dormant* skills. |

---

## A · Dormant skills as codes

### OE5-01 · Gradient-decodable codes
- **Primitive:** a code over weights whose *decoder is gradient descent*. A skill is encoded at learning time so that, after any later perturbation within a radius r (later learning treated as noise), k steps on its planted key bring it back exactly. The radius r is the code's *decoding radius*, the first number that says how much future learning a skill can absorb.
- **Mechanism:** At acquisition, sample perturbations of growing norm (from interfering training and random directions). Train the weights so that k key steps from every perturbation up to radius r restore the skill. Grow r until restoration fails, and report r against the parameters spent. Later, monitor how far new learning has moved the weights in the skill's sensitive directions, and decode (apply the key) before the radius is exceeded.
- **Nearest prior / gap:** [Real-numbered ECC for NNs](https://arxiv.org/abs/2602.00076) and [biological codes](https://arxiv.org/abs/2202.12887) correct hardware faults with arithmetic decoders; MAML shapes weights for fast adaptation to *new* tasks. The gap: a code for *skills*, decoded by training, with interference as the channel.
- **Cheapest first test:** MLP on 10 families. Arms at equal parameters: OE4-08 planted keys (one radius), MAML-shaped weights, EWC, and codes trained to a target r. Kill if the measured decoding radius doesn't predict which skills survive a held-out interfering stream (AUC < 0.7).
- **Old-task retention:** Per-family competence after decoding at each perturbation norm.
- **Risk / likely tie:** The radius may depend on direction, not norm; then a subspace radius replaces a scalar.

### OE5-02 · Code-division multiplexing of dormant skills
- **Primitive:** plant *mutually orthogonal* keys, like spreading codes in CDMA, so that many dormant skills share the same weights and are separated only at revival time by which code is trained on. Capacity comes from code orthogonality, not from parameter partitions.
- **Mechanism:** Assign each skill a key drawn from a set chosen to have near-zero gradient correlation at the shared weights. Plant each skill with its own code (OE4-08 objective) and add a cross-talk penalty: training on code i must not revive skill j. Report how many skills fit before cross-talk passes a threshold.
- **Nearest prior / gap:** PackNet and HAT partition weights; [superposed analog memory](https://arxiv.org/abs/2610.26118) and superposition in networks store vectors in shared space; [Kilobyte Models](https://arxiv.org/abs/2608.00860) store a network as a seed. The gap: multiple access to dormant skills by orthogonal training codes.
- **Cheapest first test:** MLP width 128, 5–40 skills. Arms at equal parameters: PackNet masks, random keys planted independently, orthogonal codes. Kill if orthogonal codes don't hold more skills at a cross-talk below 10%.
- **Old-task retention:** Per-skill revived competence and cross-talk revival of non-target skills.
- **Risk / likely tie:** Gradient correlations of keys change as the weights drift; codes may need re-orthogonalizing.

### OE5-03 · A lower bound on key length
- **Primitive:** a theorem-shaped claim: the shortest key that can revive a skill must carry at least as many bits as later learning erased about that skill from the weights. Planted keys can approach the bound; post-hoc keys can't, because they have no control over what was erased.
- **Mechanism:** Estimate the erased information as the drop in mutual information between the skill's labels and the outputs, or the description length of the minimal correcting update, after interference. Measure the shortest key (in examples × bits) that revives it, for post-hoc, minted and planted keys. Compare both to the bound.
- **Nearest prior / gap:** Rate–distortion views of forgetting (top-10 #4 rate–drift law); dataset-distillation scaling laws ([Utility Boundary of DD](https://arxiv.org/abs/2512.05817)). The gap: a bound on *revival* signals, which separates keys that read latent structure from keys that re-teach.
- **Cheapest first test:** Linear and MLP teacher–student with controlled erasure. Kill if post-hoc key length falls *below* the estimated bound (then the estimate is wrong), or if planted keys don't come within 2× of it.
- **Old-task retention:** Revived competence as key length shrinks toward the bound.
- **Risk / likely tie:** Estimating erased information in nonlinear nets is noisy; the linear case comes first.

### OE5-04 · Timescale-addressed dormant storage
- **Primitive:** store skills at different *relearning timescales*: one skill wakes after 1 key step, another only after 100, using the *same* key. The number of steps becomes an address, and a short pass and a long pass on one key read different skills.
- **Mechanism:** Plant skill A to revive at k = 1 and to be *unrevived* at k = 1 for skill B, which revives at k = 100 (staged planting with a step-indexed loss). Waking A doesn't wake B, so a coarse and a fine memory share one key.
- **Nearest prior / gap:** Multi-timescale learning (fast and slow weights); top-10 #1 waterbed law (forgetting spread across timescales). The gap: *relearning time* as an address for dormant content.
- **Cheapest first test:** MLP, 2–4 skills on one key at k ∈ {1, 10, 100}. Kill if revival at k = 1 wakes more than 20% of the k = 100 skill.
- **Old-task retention:** Per-skill competence at each k.
- **Risk / likely tie:** Long-k skills may just be worse-stored; compare with a single-skill control at k = 100.

### OE5-05 · Data-free keys: optimizer operations and seeded perturbations
- **Primitive:** a key that contains *no data at all*. It is either an optimizer operation (a few steps of reversed weight decay, a SAM ascent step, a reset of one moment buffer) or a seeded weight perturbation. Planting shapes the weights so that this operation, applied after forgetting, revives the skill.
- **Mechanism:** Choose a fixed operation O (for example, five steps of noise from seed s followed by five steps of weight-decay reversal). At acquisition, add the meta-term that O applied after a simulated forgetting perturbation restores the skill. Storage is a seed and an operation name.
- **Nearest prior / gap:** Weight-noise robustness; [Homeopathic Learning](https://arxiv.org/abs/2611.10110) studies dilute data having strong effects; stochastic resonance. The gap: *operations on weights* as planted revival triggers.
- **Cheapest first test:** MLP, 10 skills. Arms at equal storage: planted data keys, seeded-noise keys, weight-decay-reversal keys, no planting. Kill if data-free keys revive less than half of what planted data keys do.
- **Old-task retention:** Revived competence per skill and collateral change on others.
- **Risk / likely tie:** An operation that revives one skill may revive all of them (nonspecific); seeds must make it specific.

### OE5-06 · A key port: a reserved input pathway for revival
- **Primitive:** give the network a *separate input channel used only for keys*. Revival signals enter through the port, gradients from port data update the shared weights, and keys never have to look like task inputs or compete with the task distribution.
- **Mechanism:** Add a small input projection that maps port inputs into the first hidden layer; task data never uses it. Plant keys through the port (OE4-08 objective). After forgetting, train on port inputs only. The port is unused at inference.
- **Nearest prior / gap:** Soft prompts and prefix tuning add trainable inputs for *task conditioning*; password-locked models gate capability behind input text. The gap: an input pathway reserved for *training-time revival*.
- **Cheapest first test:** MLP and a small CNN, 10 skills. Arms at equal key bytes: keys in input space, keys through the port. Kill if the port doesn't revive better *and* disturb non-target skills less.
- **Old-task retention:** Revived competence; non-target competence after port training.
- **Risk / likely tie:** Port gradients may hit only the first layer; the port may need to reach several depths.

---

## B · Protection as a property of the relearning flow

### OE5-07 · Relearning-flow basin and the revival cone
- **Primitive:** treat k-step revival as a *dynamical system* (gradient flow on the key) and protect *membership in its basin of attraction* to the skill, not a subspace. The safe update directions form a *cone* (convex for small steps), which is larger than the revival-null *subspace* of OE4-02 because it also allows directions that move deeper into the basin.
- **Mechanism:** Fit a local Lyapunov function V(θ) for the relearning flow (the cluster loss after k key steps works as a first proxy). Allowed updates are those with ∇V · Δθ ≤ ε. Project new-task gradients onto this half-space (cone) instead of a null space.
- **Nearest prior / gap:** OE4-02 projects off a subspace; [Stable Recovery Manifold](https://arxiv.org/abs/2606.13637) describes recoverable regions; A-GEM projects onto a half-space defined by *current* loss. The gap: a half-space defined by the *relearning flow's* Lyapunov function.
- **Cheapest first test:** MLP, 20 families. Arms at equal compute: GPM, A-GEM, OE4-02 revival-null, revival cone. Kill if the cone doesn't give more new-task accuracy at equal revived competence than OE4-02.
- **Old-task retention:** Revived competence after k key steps, and expressed competence.
- **Risk / likely tie:** The Lyapunov proxy may be poor far from the skill.

### OE5-08 · Pullback Fisher: EWC measured where the skill will be revived
- **Primitive:** an importance metric computed at the *revived point*, not the current one: take the Fisher of the skill at θ_rev = Flow_key(θ) and pull it back through the Jacobian of the key flow. The result, F_pb = Jᵀ F(θ_rev) J, weights parameters by how much they matter *after revival*.
- **Mechanism:** At each protection refresh, run the key flow on a fork, compute the Fisher there, and backpropagate through the flow (or estimate J with JVPs). Use F_pb as the EWC metric. Outputs at θ may drift; only post-revival importance is protected.
- **Nearest prior / gap:** EWC uses the current Fisher; [Fisher-orthogonal projected natural gradient](https://arxiv.org/abs/2601.12816) projects with it. The gap: a metric transported through the relearning map.
- **Cheapest first test:** MLP, 20 families. Arms: EWC, online EWC, pullback EWC. Kill if pullback EWC doesn't beat EWC on new-task accuracy at equal revived competence.
- **Old-task retention:** Revived competence and expressed competence.
- **Risk / likely tie:** The flow Jacobian is costly; a k = 1 approximation may lose the effect.

### OE5-09 · Updates that commute with revival
- **Primitive:** a constraint stronger than revival-null: learning the new task and reviving an old skill should give the same result in either order. Formally, the commutator [U_new, R_old] = U_new∘R_old − R_old∘U_new ≈ 0 on old and new outputs. A learner whose updates commute with revival has no order effects between learning and remembering.
- **Mechanism:** Estimate the commutator with two short forks (update then revive, revive then update) and penalize the output gap on both tasks. When it is near zero, an old skill can be revived at any later time without undoing new learning.
- **Nearest prior / gap:** Commuting updates as content (PR #96's commutation law), order effects in CL, and [anticipatory recovery](https://arxiv.org/abs/2403.09613). The gap: commutation *with the revival operator* as the training constraint.
- **Cheapest first test:** MLP, 10 old and 10 new families. Arms: plain training, OE4-02 projection, commutator penalty. Kill if the penalty doesn't cut the new-task loss caused by later revival by half against OE4-02.
- **Old-task retention:** Old competence after revival, and new competence after old revival.
- **Risk / likely tie:** Two forks per check is costly; estimate on a sample of pairs.

### OE5-10 · Exact revival-null geometry in deep linear networks
- **Primitive:** a closed-form result: in a two-layer linear network trained on a teacher with singular modes, derive the revival-null subspace for a planted key and its dimension, and prove it strictly contains the output-null subspace by a computable gap. This would turn (a) into a theorem with a number to test.
- **Mechanism:** Use Saxe-style mode dynamics; write k-step key training as a map on mode strengths; linearize; compute the null space of the revived-output Jacobian. Predict the gap from the mode spectrum and test it numerically.
- **Nearest prior / gap:** [Saxe et al.](https://arxiv.org/abs/1312.6120), [Lampinen & Ganguli](https://arxiv.org/abs/1809.10374), [dynamical theory of LoRA in CL](https://arxiv.org/abs/2609.39367). The gap: a revival-specific null space, not a forgetting curve.
- **Cheapest first test:** Numerical check in linear nets of widths 16–256. Kill if the measured gap differs from the prediction by more than 20%.
- **Old-task retention:** Revived teacher-mode strengths under projected new learning.
- **Risk / likely tie:** Linear results may not carry to nonlinear nets; OE5-07 is the nonlinear follow-up.

### OE5-11 · Plant in the null space of future gradients
- **Primitive:** choose *where* to encode a new skill so that the gradients of tasks the learner will meet later are naturally orthogonal to its revival directions. Protection is built in at encoding time and needs no projection later.
- **Mechanism:** Estimate the covariance of future gradients from the base model on a broad generic corpus (or from the open-ended proposer's task distribution). At acquisition, penalize overlap between the skill's revival Jacobian and the top subspace of that covariance.
- **Nearest prior / gap:** [Estimating and Orthogonalizing Unknown Pre-training Gradients](https://arxiv.org/abs/2609.30935) protects *pretraining* knowledge from fine-tuning; OGD protects after the fact. The gap: encoding new skills *away from expected future learning*.
- **Cheapest first test:** MLP host with a known future-task distribution. Arms: plain planting, planting plus OE4-02 projection later, planting in the future null space. Kill if future-null planting doesn't match planting plus projection without the projection cost.
- **Old-task retention:** Revived competence after the future stream.
- **Risk / likely tie:** The future-gradient estimate may be wrong for open-ended tasks.

### OE5-12 · The expression–revival trade-off frontier
- **Primitive:** a law to test: for fixed capacity, the *sharpness* of a skill's expression trades off against the *width* of its revival basin. Strongly expressed skills are narrow and hard to revive from far away, while weakly expressed ones are revivable from far. The frontier says how to set each skill's operating point.
- **Mechanism:** Sweep a coefficient that trades expressed accuracy against decoding radius (OE5-01) during acquisition. Plot the frontier and fit its shape across widths.
- **Nearest prior / gap:** Flatness and generalization (SAM); [Flatness Preserves Instruction Following](https://arxiv.org/abs/2606.23641). The gap: a frontier between *expression* and *revivability* rather than between sharpness and generalization.
- **Cheapest first test:** MLP widths 64–512. Kill if no trade-off appears (the radius doesn't fall as expressed accuracy rises at fixed width).
- **Old-task retention:** It is the measured axis.
- **Risk / likely tie:** A law card; it decides how to set the planting strength.

### OE5-13 · Weight triage: expressed, dormant support, free
- **Primitive:** partition the weights into three sets: those carrying *expressed* skills, those carrying only *dormant support* (revival directions), and *free* weights that neither uses. Free weights can be reclaimed for new learning, and dormant support can be shared more loosely than expressed weights.
- **Mechanism:** Score each parameter by expressed-output sensitivity and by revival sensitivity (pullback, OE5-08). Assign learning rates by set: free gets full, dormant support gets revival-cone updates, expressed gets output protection.
- **Nearest prior / gap:** PackNet, HAT and importance-based learning rates use two states (important / free). The gap: a third state, *dormant support*, with its own update rule.
- **Cheapest first test:** MLP under a capacity bottleneck. Arms: two-state importance, three-state triage. Kill if triage doesn't hold more skills at equal revived and expressed competence.
- **Old-task retention:** Expressed and revived competence.
- **Risk / likely tie:** Dormant-support scores may overlap strongly with expressed ones.

### OE5-14 · Revival-preserving compression walk
- **Primitive:** an *active* operation: wander through weights inside the revival-null space (or cone) to make them sparser or lower-norm, freeing capacity while every dormant skill stays revivable. This is sleep-like compression with a guarantee on what can come back.
- **Mechanism:** Between learning phases, run projected descent on an L1 or rank penalty with gradients projected onto the revival-null space of all dormant skills and the output-null space of expressed ones. Measure how much capacity is freed.
- **Nearest prior / gap:** Pruning and magnitude decay with output constraints; sleep-replay consolidation ([2606.08447](https://arxiv.org/abs/2606.08447)). The gap: compression that is allowed to erase dormant *outputs* while keeping their revival.
- **Cheapest first test:** MLP, 20 dormant and 5 expressed skills. Arms: pruning with output constraints, the compression walk. Kill if the walk doesn't free at least 30% more parameters at equal revived competence.
- **Old-task retention:** Revived competence of dormant skills; expressed accuracy.
- **Risk / likely tie:** The null space may be too small to move far.

---

## C · Operations on dormant memories, from engram research

### OE5-15 · Engram tags: units marked at learning, trained only at revival
- **Primitive:** at acquisition, *tag* the units most active for a skill (an engram tag mask). Expression may later move elsewhere, but revival training updates *only tagged units*, so the key restores the skill through its original substrate and touches nothing else.
- **Mechanism:** Record the top-activated units per layer for the skill. Store the mask (bits) with the planted key. At revival, mask gradients to tagged units. Tags may overlap across skills, since only revival is masked.
- **Nearest prior / gap:** Silent engrams reactivated through tagged cells (Ryan et al. 2015); PackNet masks expression; [Conditional Co-Ablation](https://arxiv.org/abs/2607.01940) finds backup units. The gap: a mask used *only* for revival, with expression left shared.
- **Cheapest first test:** MLP and a small transformer, 20 skills. Arms: unmasked key revival, tagged revival, PackNet. Kill if tagged revival doesn't cut collateral change on non-target skills by half at equal revived competence.
- **Old-task retention:** Target revived competence; non-target competence during revival.
- **Risk / likely tie:** Tagged units may be overwritten by later learning; combine with OE5-07.

### OE5-16 · Reactivate before interference
- **Primitive:** apply the key *briefly, just before* learning a competing task. The old skill is temporarily expressed, so new-task gradients meet it in its active form and the protection set is computed at the reactivated point, which neuroscience reports protects memories from interference.
- **Mechanism:** Before each new task, take k₀ key steps on clusters predicted to interfere, then compute OE4-02 or OE5-07 protection at that point, then train the new task. The old skill is allowed to fade again afterwards.
- **Nearest prior / gap:** [Reactivation protects motor memories from interference](https://doi.org/10.1101/2025.06.26.661747); replay interleaves old data during learning. The gap: a short revival *before* learning as an operation that reshapes the protection set.
- **Cheapest first test:** MLP, 10 old and 10 new families. Arms at equal compute: no reactivation, interleaved replay, reactivation before learning. Kill if reactivation doesn't beat interleaved replay on revived competence after the new phase.
- **Old-task retention:** Revived competence after each new task.
- **Risk / likely tie:** It may reduce to replay with a different schedule; equal compute decides.

### OE5-17 · Reconsolidation editing of dormant skills
- **Primitive:** edit a dormant skill *during its revival window*: wake it with the key, apply a small correction while it is active, then let it go dormant again. The skill is updated without ever staying expressed. This is the reconsolidation operation, which ML lacks.
- **Mechanism:** Key → k steps (skill expressed) → edit on a few corrective examples → anti-key or fade. Check that the corrected version is what the key now revives.
- **Nearest prior / gap:** Memory reconsolidation (Nader et al. 2000); model editing (MEMIT, GRACE) edits *expressed* behaviour. The gap: editing *dormant* skills through their revival window.
- **Cheapest first test:** MLP with 10 dormant skills, 3 needing a label correction. Arms: edit while dormant (direct fine-tune), wake-edit-sleep. Kill if wake-edit-sleep doesn't give more corrected revival with less collateral damage.
- **Old-task retention:** Revived competence of edited and unedited dormant skills.
- **Risk / likely tie:** Editing while dormant may already work if the gradients reach the latent substrate.

### OE5-18 · Allocate new skills by excitability
- **Primitive:** route a new skill to the units that are currently *most excitable* (high recent activity and plasticity) and away from units tagged by dormant skills. This allocation rule from engram biology (CREB-driven allocation) decides *where* planting happens.
- **Mechanism:** Keep an excitability trace per unit (recent activation and gradient magnitude). At acquisition, bias learning-rate multipliers toward high-excitability, untagged units. Dormant tags (OE5-15) carry a refractory penalty.
- **Nearest prior / gap:** Engram allocation by excitability (Josselyn & Tonegawa reviews; [competition for limited neural resources](https://arxiv.org/abs/2609.32620)); dynamic sparse training picks units by gradient. The gap: allocation against *dormant* tags.
- **Cheapest first test:** MLP, a stream of 30 skills. Arms: uniform learning rates, dynamic sparse allocation, excitability allocation. Kill if it doesn't reduce tag overlap and raise revived competence.
- **Old-task retention:** Revived competence for early skills.
- **Risk / likely tie:** May equal sparsity regularization.

### OE5-19 · Locked skills: revivable only by their own key
- **Primitive:** plant a skill so that it is revivable *only* by its exact key. Any other relearning (related data, nonspecific revival) fails. Storage becomes access-controlled: a dormant skill can't be woken by accident, by interference, or by an attacker without the key.
- **Mechanism:** During planting, add an anti-revival term: k steps on held-out related data and on random keys must *not* restore the skill, while k steps on the key must. Check with relearning attacks.
- **Nearest prior / gap:** [Password-locked models](https://arxiv.org/abs/2405.19550) hide capability behind a prompt and show fine-tuning unlocks it; [relearn-robust unlearning](https://arxiv.org/abs/2607.27836). The gap: a *training-time* lock with a key as the only revival path.
- **Cheapest first test:** MLP and 0.5B LoRA, 5 locked skills. Kill if relearning on 32 related examples revives more than 20% of a locked skill, or if the key revives less than 80%.
- **Old-task retention:** Key revival; unlocked skills untouched.
- **Risk / likely tie:** This is dual-use; the card restricts it to conflict isolation and stays inside the unlearning audit of OE3-16.

---

## D · Dormancy as a resource for open-ended invention

### OE5-20 · Key composition creates skills never trained
- **Primitive:** training on the *union* of two planted keys revives a *composite* skill that was never learned as such (A then B, or A conditioned on B), if the two skills share the substrate. Dormancy becomes a generative operation: new skills come from combining memories.
- **Mechanism:** Plant A and B separately. Measure whether training on K_A ∪ K_B (or a sequence K_A then K_B) yields competence on a held-out composite task AB beyond training on A and B data at equal steps.
- **Nearest prior / gap:** Task arithmetic adds task vectors to compose skills; [The Composition Gap in DD](https://arxiv.org/abs/2609.34343) shows distilled sets compose poorly. The gap: composition *through revival dynamics*.
- **Cheapest first test:** Compositional MLP or small-transformer tasks (rule A, rule B, rule A∘B held out). Arms at equal steps: task-vector addition, few-shot A and B data, key union. Kill if key union doesn't beat task-vector addition on AB.
- **Old-task retention:** A and B competence after composition.
- **Risk / likely tie:** Composition may need the composite structure in the base.

### OE5-21 · Exploration in key space
- **Primitive:** the root's open-ended loop runs its search *over keys* instead of over tasks or environments. It perturbs, mixes and composes planted keys, trains briefly, and keeps any result that reaches a behaviour new to the archive. The dormant store becomes the search space for invention.
- **Mechanism:** Population of key combinations (unions, interpolations, small mutations). Each candidate is trained for k steps on a fork; novelty is scored with the competence-tracking archive (OE2). Novel behaviours are planted with their own keys.
- **Nearest prior / gap:** Novelty search over parameters or behaviours; OMNI over environments; latent-space exploration in generative models. The gap: open-ended search in the space of *revival signals*.
- **Cheapest first test:** MiniGrid agent with 10 planted skills. Arms at equal environment steps: novelty search over environments, over policy parameters, over keys. Kill if key-space search doesn't find more archive-new behaviours.
- **Old-task retention:** Planted skills stay revivable after exploration.
- **Risk / likely tie:** Composite behaviours may be trivial mixes; the archive's competence signatures (OE2-01) decide novelty.

### OE5-22 · Novelty by revivability
- **Primitive:** call a behaviour *novel* only if no planted key revives it. A rediscovery (revivable from the store) is rehearsal, and true invention is whatever the dormant store can't reach. The open-ended drive is anchored to the learner's latent memory, not only its expressed one.
- **Mechanism:** For a candidate behaviour, try key revival from the bank on a fork; if any key reaches it within k steps, mark it a rediscovery. Pay full novelty only for unreachable behaviours. Rediscoveries refresh their key instead.
- **Nearest prior / gap:** OE2-01 competence signatures (expressed repertoire); OE06 lapse archive. The gap: a novelty definition that includes *dormant* competence.
- **Cheapest first test:** MiniGrid with 20 planted dormant skills. Arms at equal steps: lapse novelty (OE06), revivability novelty. Kill if revivability novelty doesn't find more behaviours that no key can reach.
- **Old-task retention:** Dormant revivability and expressed competence at the end.
- **Risk / likely tie:** Fork checks are expensive; estimate with key-response similarity.

### OE5-23 · Dormant alternatives: many solutions per skill
- **Primitive:** plant *several* alternative solutions to one skill (different strategies), each dormant behind its own key. When the world changes, the learner wakes whichever alternative still works instead of relearning, so adaptation becomes selection among dormant variants.
- **Mechanism:** During acquisition, collect diverse solutions (quality-diversity or different seeds) and plant each with its own key. On a performance drop, try keys in order of predicted fit and keep the first that recovers.
- **Nearest prior / gap:** [EliteReplay](https://arxiv.org/abs/2610.22290) keeps diverse solutions in RL post-training; quality-diversity archives keep elites as separate policies. The gap: alternatives stored *dormant in one network*, woken by keys.
- **Cheapest first test:** MiniGrid tasks with 3 viable strategies, then a world change that breaks two. Arms at equal bytes: one expressed strategy plus relearning, stored QD policies, dormant alternatives. Kill if dormant alternatives don't recover faster than relearning.
- **Old-task retention:** Success before and after the change, and revivability of unused alternatives.
- **Risk / likely tie:** Stored QD policies are the strong control when storage is cheap.

### OE5-24 · Key-warmed learning: dormant skills as a prior for new ones
- **Primitive:** before learning a new task, wake (partially) the dormant skills predicted to share structure, learn the new task from that state, then let them sleep again. Forward transfer comes from memories that aren't currently expressed.
- **Mechanism:** Predict relevance from key-response similarity between the new task's first gradient and each key's gradient. Take k₀ steps on the top keys, learn the new task, then fade. Compare learning speed.
- **Nearest prior / gap:** Forward transfer from expressed skills; adapter retrieval (LoraHub-style) composes *stored* adapters. The gap: transfer from *dormant* skills through their keys.
- **Cheapest first test:** MLP, 20 dormant families and 10 new families with planted shared structure. Arms: cold learning, retrieval of stored adapters at equal bytes, key-warmed learning. Kill if key-warming doesn't cut steps-to-threshold by 25% against cold learning.
- **Old-task retention:** Dormant revivability after the warm-start cycle.
- **Risk / likely tie:** Waking may cause interference that outweighs the transfer.

### OE5-25 · Revivability as a pretraining objective
- **Primitive:** pretrain a base model so that *whatever it is later fine-tuned on* will be plantable and revivable: the meta-objective is revivability of downstream skills after downstream interference. The base is shaped for dormancy, not only for transfer.
- **Mechanism:** During (small-scale) pretraining, sample downstream tasks, plant with keys on a fork, apply interfering tasks, and score revival. Backpropagate a first-order meta-gradient into the base.
- **Nearest prior / gap:** Meta-learned representations for CL (OML, ANML); [Re-Evaluating CL with Few-Shot Adaptation](https://arxiv.org/abs/2606.03843). The gap: pretraining for *planted revival* specifically.
- **Cheapest first test:** Small transformer pretrained on synthetic tasks, then 10 downstream families. Arms at equal pretraining compute: plain, OML-style, revivability pretraining. Kill if revivability pretraining doesn't raise downstream key revival after interference.
- **Old-task retention:** Downstream revival and pretraining-task performance.
- **Risk / likely tie:** Expensive; a toy version comes first.

### OE5-26 · Plant before continued pretraining, revive after
- **Primitive:** the language-model test of this whole node. Plant keys for instruction-tuned skills, run continued pretraining on new-domain text (which normally erases them), then revive each skill from its planted key. If it works at 0.5B–1.5B, dormancy is a practical CL tool for LMs.
- **Mechanism:** Instruction-tune Qwen2.5-0.5B on 8 skill families with planting (OE4-08), with revival-null protection (OE4-02) or the revival cone (OE5-07) during CPT. After CPT, train k steps per key.
- **Nearest prior / gap:** [Spaced repetition for continual pretraining](https://arxiv.org/abs/2608.17530), [Replay on Demand](https://arxiv.org/abs/2609.40089), [TFGN](https://arxiv.org/abs/2605.15053) replay-free CPT. The gap: planted revival as the retention mechanism across CPT.
- **Cheapest first test:** 0.5B, 50M CPT tokens. Arms at equal bytes and compute: replay at 1%, task vectors re-added after CPT, post-hoc keys, planted keys with and without the cone. Kill if planted keys plus the cone don't beat 1% replay on revived skill accuracy.
- **Old-task retention:** Per-skill accuracy after revival, the new-domain perplexity gain, and a base benchmark.
- **Risk / likely tie:** 1% replay is a strong control at this scale.

---

## Ranked deeper questions

1. **Are dormant skills a code, with a decoding radius, multiple access and a length bound? (OE5-01, OE5-02, OE5-03, OE5-04)**
   Measure the decoding radius of planted skills and test whether it predicts survival under a held-out stream. Test whether orthogonal planted codes multiplex more skills than masks at equal parameters. Check the key-length bound in linear nets first. If the radius doesn't predict survival, drop the coding view.
2. **Is protection best defined by the relearning flow rather than by outputs or subspaces? (OE5-07, OE5-08, OE5-09, OE5-10)**
   Derive the revival-null gap in deep linear nets, then compare the revival cone, pullback Fisher and commuting updates against OE4-02 and GPM on new-task accuracy at equal revived competence.
3. **Do engram operations (tag, reactivate before interference, reconsolidate) work on artificial dormant skills? (OE5-15, OE5-16, OE5-17, OE5-18)**
   Each has a clear control: unmasked revival, interleaved replay, editing while dormant, and dynamic sparse allocation. Run all four in one MLP host with 20 planted skills.
4. **Can dormancy drive invention, not just retention? (OE5-20, OE5-21, OE5-22, OE5-23)**
   Test whether key unions yield held-out composite skills beyond task-vector addition, and whether search in key space finds more archive-new behaviours than search over environments or parameters at equal steps.
