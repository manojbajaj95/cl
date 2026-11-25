# Learning Economics 4: Diverse teaching exits that survive sequential reuse

**Depth 3 · 26 idea cards · Ideas only; no experiments or GPU.** Child of [Learning Economics 3](learning-economics-3.md) ([PR #327]), following the two score-3 ideas in [the reviewer's row 445][triage] on [PR #6][review]:

- **LE3-03 — test exit under correlated shortages.** Reward a teaching path that leaves two learnable ways to finish drawing on different upstream sources, not many nominal sellers sharing one source. A single shared bottleneck makes seller count meaningless.
- **LE3-12 — pay on the second use of the same data budget.** One entrant trains on a first extension with capped budget *k*, a different entrant gets the same capped budget on a held-out extension, and payment requires a gain on the second job without undoing the first—paying for a reusable representation rather than one easy continuation.

Read the [idea ledger][ledger] first. This node does not reprice the Nerode quotient, revive gauge preconditioning, forecast plasticity from NTK Gramians (killed in PR #9/#21), claim wins for save/restore, sparse-damage codes, or teacher identity alone, or relabel standard modality dropout and offline meta-learning as procurement primitives. The parent single-source covenant, single-entrant payout, and LE3-03/LE3-12 individually are baselines, not new cards; every joint card in Section C must beat the **stacked** controls of both parents plus non-strategic source-diverse multitask pretraining at equal examples, updates, and bytes.

## What separates genuine exit diversity and second-use reuse from relabeling?

- **Source-disjoint learnability, not static modality robustness.** Two correlated features that vanish together under one upstream outage are one exit. A genuine second exit requires an operational **source-disjointness witness**: two entrant policies restricted to disjoint upstream data/feature sources that *each* reach target error within budget *k* from the same checkpoint without breaching old floors. Compare against [Targeted Modality Dropout], [Feature Sieve], [DivDis], and a non-strategic source-diverse curriculum with no covenant.
- **Live two-hop sequential reuse, not reset-checkpoint meta-learning.** Standard continual meta-learning ([OML]) and few-shot continual evaluation ([Few-Shot CL]) optimize or score adaptation from a reset checkpoint or offline-meta-trained foresight. Here, an independent Entrant 1 mutates the live weights on Extension 1 within budget *k*, and an uncoordinated Entrant 2 must adapt *that mutated checkpoint* on a held-out Extension 2 within budget *k* without undoing Extension 1 or old tasks. Compare against single-entrant LE2-01, multitask pretraining, [CRMA]/[MoRe] modular continual fine-tuning, and [SE2D] continual distillation.
- **Learner-side state effect and planner-equivalence gate.** Following [LE2-27][PR #326] and [LE3-26][PR #327], every card must show a change in what the learner represents, retains, or can adapt to—not merely feasible trades over a fixed menu. Always include the same-powers central buyer and equal-budget open replay. If a central buyer or blank-capacity partitioning achieves the same two-hop diverse exits at the same spend, drop the proposed contract primitive.
- **Retention in every first test.** Pretrain two unchanged ordinary tasks, one rare, including old exceptions to both emerging extensions. Score a fixed unseen mix on the live learner via ordinary prediction: before instruction, after Entrant 1, after Entrant 2, and under each source outage. No task IDs, teacher hints, source routing, or checkpoint restore for evaluation. Report per-task loss and worst-slice drop against a predeclared no-new-learning floor at matched new progress.

**Literature check.** Checked alphaXiv (`discover_papers` and PDF queries) across multimodal continual learning and modality dropout, simplicity bias and feature multiplicity, continual meta-learning and few-shot continual evaluation, continual multi-teacher distillation, heterogeneous data-source games, and multi-stage/continual procurement contracts. Every linked arXiv record below was verified from the retrieved paper records. In particular, [CMCDR] already regularizes modality contribution drift for *old* tasks; [Few-Shot CL] already evaluates continual learning via few-shot adaptation with foresight meta-learning; [SE2D] already distills sequential domain teachers; [Heterogeneous Data Game] already models competition across heterogeneous sources; and [Continual Coverage] already studies online contract selection. None of those ingredients is claimed as new here. **P** denotes a candidate reusable operation; **I** an improvement or discriminating audit, not a reviewer verdict.

## A · LE3-03: Diverse teaching exits under correlated shortages

### LE4-01 · Pay to keep two source-disjoint gradient cones open — P
- **Mechanism / learner effect:** An incumbent can pass a multi-seller check while steering the representation so every useful future update aligns with one shared upstream feature. Require two entrants drawing from disjoint upstream sources to reach the new target via finite-step weight updates whose projections into the old-task null space remain linearly independent, paying only when ablating either source's feature subspace still leaves an affordable finish route.
- **Nearest prior / gap:** [Feature Sieve] and [DivDis] diversify static predictors at train time; [CMCDR] preserves existing modality contribution profiles on old tasks. Neither targets **post-handoff adaptability along disjoint source subspaces** elicited from a strategic incumbent.
- **Cheapest first test:** Two-view shared-feature classifier with two redundant cues (source A, source B) and an incumbent who can teach a collapsed single-cue shortcut or a dual-cue representation. Compare seller-count covenant (#326), [Feature Sieve] plus open replay, and source-diverse curriculum without a covenant; reject if the collapsed shortcut passes or if non-strategic replay ties at equal examples.
- **Old-task retention:** Score rare old exceptions after finishing via source A alone and via source B alone; include an old slice that relies on source B when source A is perturbed.

### LE4-02 · Anti-shortcut inoculation: pay only if the weaker source can finish when the dominant source is blacked out — P
- **Mechanism / learner effect:** Under simplicity bias ([Language Shortcut]), a dominant source (e.g., clean text or logs) suppresses gradient flow into a weaker source (e.g., noisy telemetry), leaving the weaker source unable to *teach* new rules even when both sources exist. Pay the incumbent only if an entrant restricted strictly to the weaker source can finish a new rule within budget *k* during a total blackout of the dominant source.
- **Nearest prior / gap:** [Targeted Modality Dropout] and [Sequential Modality Dropout] drop modalities during training for static *inference* robustness; [Language Shortcut] diagnoses LLM text dominance. The proposed object is **weaker-source teachability** (learning a new rule from the weaker source alone), not zero-shot inference with a missing modality.
- **Cheapest first test:** Two-modality toy learner (high-SNR cue A, lower-SNR cue B) where standard SGD ignores cue B. Compare [Targeted Modality Dropout] at matched dropout compute, a single-source covenant, and equal-example cue-B replay; reject if static modality dropout already yields equal cue-B finite-step sample cost on a new rule.
- **Old-task retention:** Verify that keeping cue B teachable does not degrade old dominant-source tasks or rare cross-modal exceptions when both cues are present.

### LE4-03 · Latent-correlation discovery via surprise cluster-outage swaps — P
- **Mechanism / learner effect:** Buyers rarely know which nominally independent sellers secretly share an upstream labeler, base model, or data feed. After the incumbent commits its checkpoint, cluster available entrants by the empirical correlation of their single-step updates on an unlabeled public probe, black out the largest empirical cluster at once, and pay only if an entrant from a residual cluster finishes within budget *k*.
- **Nearest prior / gap:** [Heterogeneous Data Game] analyzes known heterogeneous sources; [TC-RMDP] assumes a known shift-correlation structure. Here the buyer **infers hidden source sharing from live checkpoint update covariance** and ties incumbent payout to surviving whole-cluster removal.
- **Cheapest first test:** Six sellers where four secretly draw from latent feed 1 and two from latent feed 2, with seller labels hidden from the buyer. Compare random-entrant LE2-01, seller-count covenants, and known-source LE3-03 as an oracle ceiling; include a null where all six sellers share one latent feed (payout must fail).
- **Old-task retention:** Score old tasks under the residual-cluster entrant's finish trajectory, including rare old cases originally learned mostly from the blacked-out cluster.

### LE4-04 · Non-interfering exit channels: taking exit A must not atrophy sensitivity to source B — P
- **Mechanism / learner effect:** Even if a checkpoint starts with two valid source-disjoint exits, executing exit A's live updates can saturate or rotate shared weights so source B's features lose gradient sensitivity. Pay the incumbent for a **cross-source-preserving representation** where finishing an immediate subgoal via source A keeps source B's finite-step sample cost on a parallel target bounded (and symmetrically for B then A).
- **Nearest prior / gap:** [CMCDR] regularizes modality contribution drift for *old* tasks during training; [Evading Simplicity Bias] trains separate ensemble members. Here a single learner must preserve **unused source B's future plasticity** across unregularized live updates driven purely by source A.
- **Cheapest first test:** Shared-trunk MLP with two input views; Entrant 1 updates on subgoal 1 using view A only, then measure view B's sample cost on subgoal 2. Compare [CMCDR] on old tasks, open dual-view replay, and an unconstrained incumbent; reject if view-A updates leave view-B sample cost unchanged even without the contract.
- **Old-task retention:** Score old view-A, view-B, and joint-view slices after both the view-A update and the subsequent view-B continuation.

### LE4-05 · Buy an exit-forking lesson that converts a single-source checkpoint into a dual-source checkpoint — P
- **Mechanism / learner effect:** An operational learner may already be locked into source A from legacy training. Procure a short **exit-forking write** whose sole paid deliverable is to drop source B's independent finish cost below *k* while keeping source A's finish cost and all old-task accuracies intact—opening a second teaching exit without retraining from scratch.
- **Nearest prior / gap:** [GRAFT] and [SE2D] distill multiple teachers for inference coverage; [BT²] aligns features for retrieval compatibility. The candidate primitive is a **targeted plasticity-opening lesson** judged strictly by whether a previously ineffective source B can now *teach* new rules.
- **Cheapest first test:** Pretrain a two-view classifier on source A alone until source B's finish cost exceeds 5× budget *k*. Compare an exit-forking lesson against equal-example source-B fine-tuning, [SE2D]-style logit preservation, and full dual-source replay; reject if plain source-B replay achieves the same finish cost at equal examples and retention.
- **Old-task retention:** Check old source-A tasks and rare exceptions immediately after the exit-forking lesson and after finishing a new rule via source B.

### LE4-06 · Price worst-slice source substitutability, not average exit cost — P
- **Mechanism / learner effect:** An incumbent can satisfy an average source-diversity check by making source B work on frequent regular cases while leaving rare or boundary exceptions reachable only via source A. Tie the buyout to the **worst-slice source-disjoint finish cost**, requiring both source A and source B to independently learn rare/boundary cases within budget *k*.
- **Nearest prior / gap:** [Robust procurement design] handles worst-case buyer uncertainty over scalar value; [Quasiregular] studies rule-vs-exception recovery. The proposed object is **slice-level source substitutability** inside a continual learner's representation.
- **Cheapest first test:** Quasiregular rule-plus-exception task with two sources where a shortcut representation makes regular cases dual-source learnable but exception clusters source-A-only. Compare mean-cost LE3-03, uniform exception replay, and worst-slice pricing; include a negative where source B contains no information on one exception slice (must report nonidentifiability rather than penalize).
- **Old-task retention:** Require old rare exceptions to hold their floor under *both* source-A and source-B worst-slice continuations.

### LE4-07 · Shared-circuit bottleneck audit: separate disjoint raw sources from colliding internal circuits — I
- **Mechanism / learner effect:** Discriminating audit. Two entrants with disjoint raw data feeds can still route their updates through the *same* internal bottleneck subspace, so a single weight-level shift or interference event disables both exits simultaneously. Measure the **effective subspace overlap** between entrant A's and entrant B's finish trajectories and flag "pseudo-diverse" checkpoints where raw sources are disjoint but internal circuits collide.
- **Nearest prior / gap:** [Mechanistic Mode Connectivity] tests whether static minimizers share mechanisms; [SPACE-LoRA] allocates subspaces across tasks. This is a diagnostic audit separating **raw-source diversity** from **internal circuit-exit diversity**, not a standalone training primitive.
- **Cheapest first test:** Construct two checkpoints with identical raw-source finish costs *k* for A and B: one routing both views through a single shared bottleneck unit, one through two parallel sub-circuits. Perturb the shared bottleneck with an unrelated task update and test whether the overlap metric predicts joint exit collapse better than raw-source counts.
- **Old-task retention:** Score old tasks before and after the perturbing update; flag cases where apparent exit diversity survives only by sacrificing old-task margins.

### LE4-08 · Asymmetric dual-exit contracts: compress the scarce source's finish budget — P
- **Mechanism / learner effect:** When source A is cheap and abundant but outage-prone, while source B is scarce and expensive, requiring symmetric budgets $k_A = k_B$ either fails or wastes capacity. Offer an **asymmetric dual-exit contract** $(k_A, k_B)$ with $k_B \ll k_A$ that rewards the incumbent for compressing the *scarce* source's finish cost—shifting representation capacity toward the bottleneck supply.
- **Nearest prior / gap:** [Continual Coverage] optimizes contract duration under price uncertainty; [Dual-Mode Procurement] designs dual-mode platforms. Neither couples asymmetric supply scarcity to **how a neural representation allocates sample-efficiency capacity across sources**.
- **Cheapest first test:** Two-view learner where source B labels cost 5× source A labels. Compare symmetric LE3-03 ($k_A = k_B$), weighted dual-source replay at equal dollar spend, and an asymmetric $(k_A, k_B)$ payout; reject if weighted replay in a central buyer achieves the same dollar-weighted finish cost.
- **Old-task retention:** Confirm that compressing $k_B$ does not erode old tasks that depend on source A's finer distinctions.

### LE4-09 · Single-source drought audit: test for an irreversible feature-collapse ratchet — I
- **Mechanism / learner effect:** Discriminating audit. During a prolonged shortage of source B, the learner absorbs *T* consecutive updates from source A alone. Measure whether source B's finish cost recovers when source B returns, or whether *T* source-A updates permanently atrophy source B's read/write pathways (a continual-learning "use-it-or-lose-it" ratchet).
- **Nearest prior / gap:** [Closing the loop] frames missing data as loss of actuation in dynamical systems; [Few-Shot CL] measures relearning after forgetting. This audit tests **asymmetric plasticity atrophy** under prolonged single-source operation, gating whether continuous diversity maintenance is needed beyond initial handoff.
- **Cheapest first test:** Train a two-view learner through $T \in \{5, 20, 50\}$ source-A-only tasks, then re-introduce source B on a fresh task and measure finish cost *k* vs a fresh dual-view baseline. Compare with [CMCDR] old-task regularization; if source-B finish cost stays flat across *T*, ongoing drought covenants are unnecessary.
- **Old-task retention:** Track old source-B-dependent tasks throughout the *T*-step source-A drought and after source B returns.

## B · LE3-12: Pay on the second use of the same data budget

### LE4-10 · Order-swap second-use payout (commutative two-hop adaptability) — P
- **Mechanism / learner effect:** An incumbent can game a fixed-order two-hop test (Extension 1 → Extension 2) by planting a one-way scaffold that only works in that sequence. Draw two held-out extensions and evaluate **both** sequential orders (1→2 and 2→1) on independent copies of the committed checkpoint, paying on the *minimum* second-use gain across both orders.
- **Nearest prior / gap:** [OML] meta-trains across task orderings offline; [Few-Shot CL] evaluates few-shot plasticity along a single sequence. Here the paid object is **order-symmetric two-hop live weight reuse** by uncoordinated entrants with no central meta-learner.
- **Cheapest first test:** Synthetic two-extension rule learner where an incumbent can supply an asymmetric scaffold (cheap 1→2, slow 2→1) or a symmetric shared feature. Compare fixed-order LE3-12, single-entrant LE2-01, and multitask pretraining at equal examples; reject if fixed-order LE3-12 already selects the symmetric feature.
- **Old-task retention:** Score original tasks and whichever extension went first after *both* orderings complete.

### LE4-11 · Self-protecting features: pay for natural-SGD non-interference between uncoordinated entrants — P
- **Mechanism / learner effect:** In LE3-12, Entrant 2 has no access to Entrant 1's training data or old-task replay—it runs plain SGD on Extension 2 within budget *k*. Pay the incumbent specifically for a representation whose **unprojected natural gradients** on Extension 1 and Extension 2 land in non-destructive subspaces by default, so Entrant 2 does not overwrite Entrant 1 even without OGD, replay, or adapters.
- **Nearest prior / gap:** [CRMA] and [SPACE-LoRA] protect prior tasks via explicit spectral bounds or subspace projection during task 2; [MoRe] uses explicit modular routing. Here Entrant 2's update rule is **frozen vanilla SGD**, and the paid object is a self-isolating incumbent geometry.
- **Cheapest first test:** Factorized linear or small MLP learner with two disjoint extension families; freeze Entrant 1 and Entrant 2 to plain SGD with no replay. Compare [CRMA]-style spectral regularization, multitask pretraining, and LE2-01 single-entrant payout; reject if plain multitask pretraining yields equal Entrant-1 retention after Entrant 2.
- **Old-task retention:** Score both original tasks (ordinary + rare) and Entrant 1's held-out slices after Entrant 2's unconstrained SGD update.

### LE4-12 · Charge the incumbent for plasticity debt exported from Entrant 1 to Entrant 2 — P
- **Mechanism / learner effect:** An incumbent can make Extension 1 artificially cheap by leaving a high-curvature shortcut that Entrant 1 exploits, saturating the representation so Entrant 2 stalls. Measure the **cross-entrant plasticity externality** $\Delta k_{2|1} = k(\text{Ext 2 after Ext 1}) - k(\text{Ext 2 directly from handoff})$ via live rollouts and debit the incumbent whenever Entrant 1's update slows Entrant 2.
- **Nearest prior / gap:** [Control Minimization] frames sequential stability-plasticity as optimal control; [Few-Shot CL] scores per-shot plasticity. Unlike Gramian plasticity-reserve predictors (killed in PR #9/#21), $\Delta k_{2|1}$ is measured directly via paired live rollouts as a contractable externality.
- **Cheapest first test:** Small ReLU/MLP classifier where a shortcut initialization gives low $k(\text{Ext 1})$ but spikes $\Delta k_{2|1} > 0$, versus a slower-start shared feature with $\Delta k_{2|1} \le 0$. Compare raw LE3-12 (total second-hop cost), LE2-01, and a central two-step planner; reject if raw LE3-12 already eliminates every positive-debt checkpoint.
- **Old-task retention:** Require old-task floors on *both* branches of the paired rollout (direct Ext 2 and post-Ext-1 Ext 2); a checkpoint cannot lower $\Delta k_{2|1}$ by failing direct Ext 2 or dropping old tasks.

### LE4-13 · Myopic-entrant buffer: pay on second use after a noisy, slightly misspecified first entrant — P
- **Mechanism / learner effect:** Real entrants do not run ideal hyperparameter-tuned updates; Entrant 1 may overfit slightly or use a misspecified step size on Extension 1. Run Entrant 1 from a pre-registered distribution of **myopic/noisy update policies** (e.g., 2× step size or small-batch noise) and pay only if Entrant 2 still succeeds on Extension 2 without undoing Extension 1—eliciting a wide, basin-buffered representation rather than a brittle knife-edge initialization.
- **Nearest prior / gap:** [Non-contractible Outsider] analyzes contracting with an uncontrolled third party; [SE2D] distills from teachers of varying expertise. The proposed primitive is **second-hop teachability robust to an uncoordinated, sloppy first entrant**.
- **Cheapest first test:** Low-rank learner comparing a sharp minimum (fast under tuned Entrant 1, collapses under 2× LR Entrant 1) against a flat/buffered representation. Compare clean-entrant LE3-12, noise-injected pretraining (SAM/weight noise) at equal compute, and multitask pretraining; reject if standard flat-minima pretraining ties without the contract.
- **Old-task retention:** Score old tasks and rare exceptions after the noisy Entrant 1 update and after Entrant 2's continuation.

### LE4-14 · Compositional second use: Extension 2 must recombine Extension 1's new skill with the incumbent's base — P
- **Mechanism / learner effect:** When Extension 1 and Extension 2 are independent parallel tasks, orthogonal heads or blank capacity can trivially pass LE3-12. Require Extension 2 to **compose** Entrant 1's newly learned rule with an incumbent-taught base relation within budget *k*, forcing the incumbent to leave a representation where Entrant 1's live weight update is *composable* by Entrant 2 rather than isolated.
- **Nearest prior / gap:** [Program Memory] and [MoRe] compose explicit modules; [OML] tests disjoint classification heads. Requiring **weight-space composability across two independent sequential entrants** separates genuine compositional representations from task partitioning.
- **Cheapest first test:** Synthetic relational grammar: incumbent teaches base relations $R_1, R_2$, Entrant 1 teaches new unary transform $T$, and Entrant 2 must learn composite $T \circ R_1$ within budget *k* without seeing $T$'s training data. Compare LE3-12 on disjoint extensions, blank-capacity partitioning, and multitask pretraining; reject if isolated-head partitioning solves the composite within *k*.
- **Old-task retention:** Score base relations $R_1, R_2$, bare transform $T$, and rare exceptions to $R_1$ after Entrant 2 finishes $T \circ R_1$.

### LE4-15 · Positive sequential acceleration: pay only if the second use is strictly cheaper than the first — P
- **Mechanism / learner effect:** Tighten LE3-12 from "same budget *k*" to **strict positive sequential transfer**: Entrant 2 must reach target error in $\le \alpha k$ ($\alpha < 1$) *after* Entrant 1 trains on Extension 1, beating Entrant 2's direct cost from the incumbent checkpoint. This pays the incumbent for a scaffolding representation that turns Entrant 1's live update into a stepping stone for Entrant 2.
- **Nearest prior / gap:** [Few-Shot CL] observes learning-to-learn from offline foresight meta-learning; [TripleWin] prices coupled data-model equilibria. Here positive sequential acceleration is **externally contracted** on an incumbent who never observes either entrant's private extension.
- **Cheapest first test:** Hierarchical feature-learning task where Extension 1 and Extension 2 share a latent intermediate concept; test whether an incumbent can teach the prerequisite basis so Entrant 1's update completes the shared concept and halves Entrant 2's sample cost. Compare constant-budget LE3-12, direct multitask pretraining, and [OML]; include a negative where Extensions 1 and 2 share no latent structure.
- **Old-task retention:** Verify that the accelerated Entrant 2 update does not overfit the shared intermediate concept at the expense of old tasks that use different combinations of the base features.

### LE4-16 · Optimizer-mismatched second use: Entrant 2 uses a different update class than Entrant 1 — P
- **Mechanism / learner effect:** An incumbent representation tuned to one optimizer's implicit bias (e.g., full-weight SGD) can stall when Entrant 2 arrives with a different update rule (e.g., rank-*r* LoRA or Adam/Muon). Pre-register a mismatched update class for Entrant 2 and pay only when the post-Entrant-1 checkpoint stays cheap to adapt under the mismatched updater.
- **Nearest prior / gap:** [Muon Simplicity Bias] shows optimizer choice alters feature-learning trajectories; [Representation Finetuning] studies fixed PEFT adapters. Contracting for **optimizer-agnostic two-hop reuse** tests whether reusability lives in the learned weights rather than a matched optimizer trajectory.
- **Cheapest first test:** Small MLP where Entrant 1 runs SGD and Entrant 2 runs rank-4 LoRA (and the reverse). Compare same-optimizer LE3-12, [Representation Finetuning] baselines, and multitask pretraining; reject if same-optimizer LE3-12 checkpoints already transfer with zero gap to the mismatched updater.
- **Old-task retention:** Score old tasks and Entrant 1's extension after the mismatched Entrant 2 update, with no adapter switching at inference.

### LE4-17 · Blank-capacity audit: separate genuine reusable features from unused parameter hoarding — I
- **Mechanism / learner effect:** Discriminating audit. An incumbent can pass LE3-12 without teaching any reusable feature simply by solving the initial task in half the network and leaving the other half near-random ("blank capacity") for Entrants 1 and 2 to carve up independently. Benchmark every LE3-12 winner against a **matched-parameter partitioned baseline** (freeze half for base, leave half freshly initialized) to verify that the buyout actually purchased shared representation rather than empty parameters.
- **Nearest prior / gap:** [SPACE-LoRA] and [Brain-Inspired Modularity] explicitly allocate unused capacity; [Paid with Models] analyzes rent-seeking in collaborative ML. This is the mandatory falsifier for Section B: if blank-capacity hoarding ties at equal parameters, LE3-12 is buying unused capacity, not reusable features.
- **Cheapest first test:** Run LE3-12 on a 2-layer MLP of width *W* versus a partitioned control (width *W*/2 trained on base + width *W*/2 random init). Require the incumbent-taught checkpoint to beat the partitioned control on Extension 2 sample cost by a clear margin over seeds; if it ties, retire non-compositional LE3-12 tasks.
- **Old-task retention:** Match old-task accuracy at handoff between the incumbent checkpoint and the width-*W*/2 partitioned control before running Entrants 1 and 2.

### LE4-18 · Hop-3 cliff audit: test whether a two-use payout merely shifts exhaustion to hop 3 — I
- **Mechanism / learner effect:** Discriminating audit. Paying on hop 2 could induce a strategic incumbent to supply a "two-use battery" that passes Entrants 1 and 2 but collapses on Entrant 3. Evaluate checkpoints selected by 1-hop (LE2-01), 2-hop (LE3-12), and multitask baselines out to hops 3 and 4 under held-out extensions.
- **Nearest prior / gap:** [Sequential Contract Design] analyzes multi-stage effort under fixed budgets; [Few-Shot CL] evaluates multi-task sequences. This audit tests whether **2-hop contractability extrapolates to continual $N$-hop sustainability**.
- **Cheapest first test:** Four sequential extensions drawn from the same generator on a small shared-feature classifier; compare sample cost and retention curves across hops 1–4 for 1-hop payout, 2-hop payout, and central multitask pretraining. Flag any regime where hop-2 wins reverse by hop 3.
- **Old-task retention:** Track original old tasks plus every preceding extension (1 through $t-1$) at each hop $t \in \{2, 3, 4\}$.

## C · Composing LE3-03 + LE3-12: Diverse exits that stay diverse across sequential reuse

*Every card in this section is a joint mechanism and must beat the **stacked** control of LE3-03 alone + LE3-12 alone + source-diverse multitask pretraining at equal examples, audit work, and bytes.*

### LE4-19 · Cross-source two-hop payout: Entrant 1 uses Source A, Entrant 2 must finish Extension 2 using Source B — P
- **Mechanism / learner effect:** The direct composition of both seeds. Entrant 1 trains on Extension 1 using Source A; then Source A suffers a correlated shortage, and an independent Entrant 2 must learn held-out Extension 2 using **disjoint Source B** within budget *k*, without undoing Extension 1 or old tasks. A checkpoint passing LE3-03 (two exits at hop 1) and LE3-12 (same-source reuse at hop 2) separately can still fail if Source A's hop-1 update destroys Source B's hop-2 usability.
- **Nearest prior / gap:** [CMCDR] preserves old modality profiles; [OML] and [Few-Shot CL] assume a stationary source distribution across sequential hops. The novel claim is an **interaction**: cross-source sequential reuse requires preserving Source B's *future adaptability* through Source A's live mutation.
- **Cheapest first test:** Two-view shared-feature learner with two sequential extensions; compare (i) stacked LE3-03 + same-source LE3-12, (ii) source-diverse multitask pretraining, and (iii) the cross-source two-hop payout at equal total audit examples. Reject if the stacked parent controls already yield equal Source-B hop-2 sample cost.
- **Old-task retention:** Score old Source-A tasks, old Source-B tasks, and Entrant 1's Extension 1 after Entrant 2 finishes Extension 2 using Source B alone.

### LE4-20 · Mid-extension outage handoff: Entrant 2 finishes an interrupted Source-A update using Source B — P
- **Mechanism / learner effect:** Source A suffers a correlated outage *midway* through Entrant 1's Extension 1, leaving a half-adapted checkpoint. Entrant 2 (restricted to Source B) must both complete Extension 1 *and* learn held-out Extension 2 within the remaining budget, without rolling back to the pre-Entrant-1 checkpoint. Pay the incumbent for a representation where **partial weight progress from Source A transfers directly into Source B's update basin**.
- **Nearest prior / gap:** [Missing Arbitrary Modalities] handles missing modalities in static classification; [SE2D] distills sequential teachers on a fixed unlabeled set. The proposed object is **cross-source mid-trajectory continuability** of an interrupted live weight update.
- **Cheapest first test:** Interrupt Entrant 1 at 50% of budget *k* on a two-view rule learner, then hand the live checkpoint to Source-B Entrant 2. Compare against rolling back to handoff and restarting from Source B alone (the key control!), plus stacked LE3-03 + LE3-12; reject if rollback-and-restart ties or beats continuation.
- **Old-task retention:** Score old tasks at the interruption point, after Source-B completion of Extension 1, and after Extension 2.

### LE4-21 · Diversity-preserving first hop: pay the incumbent so Entrant 1's update does not collapse hop-2 exit count — P
- **Mechanism / learner effect:** A checkpoint can start with two valid exits (A and B), yet a greedy Entrant 1 using Source A pulls the weights into a Source-A-only basin, leaving Entrant 2 with only one exit and renewed vulnerability to a Source-A outage. Pay the incumbent only if **both** Source A and Source B remain independently valid finish routes for Extension 2 *after* Entrant 1's live update.
- **Nearest prior / gap:** [CMCDR] constrains the *updater* via a regularizer; here Entrant 1 is an unregularized independent entrant, and the incumbent is paid to shape the **initial representation** so Entrant 1's natural update preserves *second-hop* exit diversity.
- **Cheapest first test:** Fork two counterfactual copies of the post-Entrant-1 checkpoint: run Extension 2 via Source A on copy 1 and via Source B on copy 2, requiring both to finish within *k*. Compare against stacked LE3-03 + LE3-12 and source-diverse multitask replay; reject if hop-1 diversity automatically persists after Entrant 1 without the hop-2 diversity check.
- **Old-task retention:** Enforce old-task and Extension-1 floors on *both* counterfactual hop-2 branches.

### LE4-22 · Source-rotation benchmark: pay only when cross-source hop-2 stays close to the incumbent's own hop-2 cost — P
- **Mechanism / learner effect:** On a hard Extension 2, even the incumbent might need many examples, so an absolute sample cap *k* confuses task difficulty with source lock-in. Run paired hop-2 rollouts from the same post-Entrant-1 checkpoint—one with Source-B Entrant 2, one with the *incumbent itself* using Source A—and pay the diversity bonus only when Source B's sample cost stays within a declared ratio of the incumbent's own hop-2 cost.
- **Nearest prior / gap:** [Heterogeneous Data Game] studies static provider specialization; [Federated Model Marketplace] prices single-round data valuation. Paired **post-Entrant-1 cross-source vs incumbent-continuation benchmarking** controls for Extension 2 difficulty without requiring a separate public-curriculum branch.
- **Cheapest first test:** Vary Extension 2 difficulty across easy and hard rule families in a two-view classifier. Compare fixed-cap LE4-19, unpaired LE3-03 + LE3-12, and the paired ratio trigger; require the paired trigger to eliminate false rejections on hard-for-everyone extensions while still catching source-A lock-in.
- **Old-task retention:** Match old-task and Extension-1 retention floors on both arms of the paired hop-2 benchmark.

### LE4-23 · Non-rivalrous diverse exits: pay if parallel Source-A and Source-B hop-2 entrants merge without retraining — P
- **Mechanism / learner effect:** From the post-Entrant-1 checkpoint, let Entrant 2a learn Extension 2a via Source A and Entrant 2b learn Extension 2b via Source B in parallel. Pay the incumbent if their two weight deltas can be **linearly merged** (task arithmetic) onto the post-Entrant-1 checkpoint while preserving Extension 1, both Extensions 2a/2b, and old tasks—proving that diverse exits occupy non-conflicting weight subspaces even after live reuse.
- **Nearest prior / gap:** [Off-Policy Merging] and [Task arithmetic] merge adapters trained from a fixed base; [CRMA] bounds spectral norms during sequential updates. Here **post-reuse mergeability of source-disjoint entrants** is elicited upstream from a strategic incumbent.
- **Cheapest first test:** Two-view MLP after Entrant 1's live update; train parallel rank-4 or full-weight deltas for 2a (Source A) and 2b (Source B), then evaluate their linear sum without retraining. Compare against stacked LE3-03 + LE3-12, [Off-Policy Merging] from a multitask base, and sequential training; reject if multitask pretraining gives equal zero-retrain merge accuracy.
- **Old-task retention:** Score original tasks, rare exceptions, and Entrant 1's Extension 1 on the *merged* checkpoint with no post-merge fine-tuning.

### LE4-24 · Cross-source spurious-coupling stress test across sequential entrants — P
- **Mechanism / learner effect:** Entrant 1 (Source A) and Entrant 2 (Source B) can both succeed sequentially while secretly relying on a single shared background proxy present in both feeds. At payout, apply a **third-stage targeted proxy perturbation** and pay only if both Extension 1 and Extension 2 retain accuracy (or recover in $r \ll k$ steps from their respective sources), blocking "fake diversity" where both sources exploit one fragile correlate.
- **Nearest prior / gap:** [Diverse Ensembles] and [Complexity Matters] study spurious correlates in single-task training; [SAE-FD] distills sparse features for CL. Here the stress test targets **cross-source spurious coupling across two sequential entrants**.
- **Cheapest first test:** Two-view classifier with a shared spurious background cue present in both views A and B during training but flipped at stress-test time. Compare unperturbed LE4-19, stacked LE3-03 + LE3-12, and [Diverse Ensembles] at equal compute; reject if unperturbed LE4-19 already avoids the shared spurious cue.
- **Old-task retention:** Include an old task where the background cue is genuinely predictive and verify that resisting spurious coupling on Extensions 1–2 does not break that old task.

### LE4-25 · Planner-equivalence gate for joint diversity and two-hop reuse — I
- **Mechanism / learner effect:** Discriminating audit (extending [LE2-27][PR #326] and [LE3-26][PR #327] to depth 3). Enumerate a minimal strategic game with one private-cost incumbent, two correlated sources, and two sequential extensions. Compare (a) the joint LE4-19/LE4-21 contract, (b) the stacked independent LE3-03 + LE3-12 gates, and (c) an equally informed **central buyer** directly procuring a source-diverse multitask curriculum over the same menu. Identify the exact parameter region where the joint contract induces a strictly better learner checkpoint; if empty, collapse the joint cards.
- **Nearest prior / gap:** [Optimal contracts] and [Robust procurement design] characterize when decentralized contracts outperform direct control. This audit enforces that Section C's joint cards earn their complexity over a same-powers central buyer.
- **Cheapest first test:** Solve exact seller best responses in a 2-type incumbent, 2-source, 2-extension game coupled to a tiny factorized learner. Log checkpoint quality, total spend, and failure rates across all three mechanisms; require a nonempty region where the joint contract strictly dominates both the central buyer and the stacked parent gates.
- **Old-task retention:** Include the no-trade fallback and single-source fallback in the enumeration; never relax old-task floors to make a contract feasible.

### LE4-26 · Representation-vs-supply 2×2 decomposition audit — I
- **Mechanism / learner effect:** Discriminating audit answering the root critique from [PR #324] (row 442): whether diverse teaching exits live in the **learner's weights** or merely in **who supplies data**. Cross two checkpoints (incumbent-contracted vs public source-diverse multitask) with two supply regimes (correlated-outage market vs independent-source market) across two sequential hops. Only mechanisms producing a nonzero checkpoint-by-supply interaction (changing *what the learner can do* under outage) warrant GPU-scale pilots.
- **Nearest prior / gap:** [Heterogeneous Data Game] isolates market equilibria; [Few-Shot CL] isolates representation plasticity. Crossing them in a 2×2 factorial test directly separates learner-side representation effects from pure procurement effects.
- **Cheapest first test:** Run the 2×2 design on the two-view sequential-extension classifier with 5 seeds; compute the interaction contrast on hop-2 finish cost and old-task worst-slice retention. Kill the representation claim if the checkpoint main effect and interaction both fall within the seed CI of the public multitask control.
- **Old-task retention:** Report the full 2×2 interaction on rare old exceptions as a co-primary endpoint alongside hop-2 sample cost.

## Ranked deeper questions

1. **Does taking one diverse exit (Source A) collapse the learner's remaining exits (Source B) for the next independent entrant, and can an upstream lesson prevent that collapse without constraining Entrant 1?** (LE4-04, 19, 21.) Test whether an unregularized Source-A update on Extension 1 atrophies Source B's finite-step learnability on Extension 2 in a real small neural learner, and whether a cross-source two-hop payout elicits a representation that beats stacked LE3-03 + LE3-12 and [CMCDR].
2. **When does a two-hop sequential payout actually buy a reusable shared representation rather than blank partitioned capacity?** (LE4-11, 14, 17, 18.) Run the LE4-17 blank-capacity audit and LE4-14 compositional second-use test side by side. If partitioned random capacity ties on disjoint extensions, compositional second use—not disjoint reuse—is the real separator for continual learning.
3. **Can a buyer elicit source-disjoint teaching exits when the correlation structure across sellers' upstream data sources is unknown in advance?** (LE4-01, 03, 07, 24.) Test whether clustering entrants by live checkpoint update covariance (LE4-03) and checking internal circuit overlap (LE4-07) catches hidden shared feeds and shared spurious correlates that seller-count covenants miss.
4. **Is there a nonempty regime where jointly contracting for correlated-shortage diversity and two-hop reuse beats both the stacked parent gates and a same-powers central buyer?** (LE4-19, 22, 25, 26.) Run the LE4-25 planner-equivalence enumeration and the LE4-26 2×2 representation-vs-supply decomposition before spending any GPU compute; if the interaction vanishes, keep only the audits and retire the market framing.

[PR #324]: https://github.com/manojbajaj95/cl/pull/324
[PR #326]: https://github.com/manojbajaj95/cl/pull/326
[PR #327]: https://github.com/manojbajaj95/cl/pull/327
[review]: https://github.com/manojbajaj95/cl/pull/6
[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L445
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[CMCDR]: https://arxiv.org/abs/2607.27260
[Targeted Modality Dropout]: https://arxiv.org/abs/2610.09566
[Sequential Modality Dropout]: https://arxiv.org/abs/2608.10240
[Language Shortcut]: https://arxiv.org/abs/2611.20349
[Missing Arbitrary Modalities]: https://arxiv.org/abs/2607.24683
[Closing the loop]: https://arxiv.org/abs/2608.09030
[Brain-Inspired Modularity]: https://arxiv.org/abs/2609.25146
[SAE-FD]: https://arxiv.org/abs/2605.25525
[OML]: https://arxiv.org/abs/1905.12588
[Representation Finetuning]: https://arxiv.org/abs/2603.11201
[MoRe]: https://arxiv.org/abs/2605.14364
[SPACE-LoRA]: https://arxiv.org/abs/2609.34453
[Control Minimization]: https://arxiv.org/abs/2602.04542
[Few-Shot CL]: https://arxiv.org/abs/2606.03843
[Program Memory]: https://arxiv.org/abs/2605.13162
[CRMA]: https://arxiv.org/abs/2606.00382
[Heterogeneous Data Game]: https://arxiv.org/abs/2505.07688
[TripleWin]: https://arxiv.org/abs/2511.03368
[Federated Model Marketplace]: https://arxiv.org/abs/2509.18104
[Off-Policy Merging]: https://arxiv.org/abs/2610.05872
[SE2D]: https://arxiv.org/abs/2605.04059
[GRAFT]: https://arxiv.org/abs/2610.02597
[DivDis]: https://arxiv.org/abs/2202.03418
[Mechanistic Mode Connectivity]: https://arxiv.org/abs/2211.08422
[Feature Sieve]: https://arxiv.org/abs/2301.13293
[Evading Simplicity Bias]: https://arxiv.org/abs/2105.05612
[Diverse Ensembles]: https://arxiv.org/abs/2311.16176
[Complexity Matters]: https://arxiv.org/abs/2403.03375
[Muon Simplicity Bias]: https://arxiv.org/abs/2610.16868
[Non-contractible Outsider]: https://arxiv.org/abs/2509.06267
[Robust procurement design]: https://arxiv.org/abs/2512.08177
[Dual-Mode Procurement]: https://arxiv.org/abs/2609.03285
[Continual Coverage]: https://arxiv.org/abs/2605.16601
[Paid with Models]: https://arxiv.org/abs/2412.11122
[Sequential Contract Design]: https://arxiv.org/abs/2611.25988
[TC-RMDP]: https://arxiv.org/abs/2406.08395
[BT²]: https://arxiv.org/abs/2211.03989
[Task arithmetic]: https://arxiv.org/abs/2212.04089
[Optimal contracts]: https://arxiv.org/abs/2309.09801
[Quasiregular]: https://arxiv.org/abs/2609.26018
