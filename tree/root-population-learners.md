# Root: Population continual learners

Root node (depth 0) · 32 candidate primitives · **Ambitious but doable** · Ideas only; no experiments run

**Thesis.** When feedback points to different hills, branch rather than compromise. A fork is a persistent learner, not an alternative decoding or a temporary experiment: it can specialize on one user group, learn from another fork without inheriting its local preferences, and outlive or be outlived by its teachers. The unit of design is the operation *between* evolving learners. Success means learning useful new behavior without breaking the service that each group already relies on.

**Scope and overlap.** Informed by the [idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md) and [flood triage](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md). This is a fresh root, not level six of [the test-time learners](https://github.com/manojbajaj95/cl/pull/378): a routed preference split alone is that branch’s baseline; the question here is what separately learning copies can subsequently exchange. [Collective agents](https://github.com/manojbajaj95/cl/pull/310) already covers generic conflict forks, rebase, gossip and re-derivation leases; this root makes exchanges and revocations conditional on their effects on successive learners. [Redundant skill populations](https://github.com/manojbajaj95/cl/pull/116) rules out calling replication an erasure code and points out the common-trunk failure floor. [Internal skill markets](https://github.com/manojbajaj95/cl/pull/124), [learning economics](https://github.com/manojbajaj95/cl/pull/324), and [cross-generation inheritance](https://github.com/manojbajaj95/cl/pull/130) already cover generic allocation markets, teacher buyouts, and one-way skill porting. The corresponding cards below specify a different object to trade, a binding local-information constraint, or a multi-parent or multi-generation operation.

## Literature check

Checked titles and abstracts on arXiv and the FedWeIT proceedings page. The gaps below distinguish the proposed operation from the named comparator; they are not claims of exhaustive novelty. **P** means a candidate primitive: each mechanism names a reusable object or operation, not a better coefficient or threshold for an existing algorithm. If the strongest equal-budget control ties, the card does not earn primitive status.

| Existing work | Starting point for this root |
|---|---|
| [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) decomposes local models into global and sparse task-specific weights and selectively transfers other clients’ task weights. [FedPC](https://arxiv.org/abs/2304.07421) studies personalized peer-to-peer federated continual learning; [Federated Orthogonal Training](https://arxiv.org/abs/2309.01289) targets global retention. | Personalized transfer, serverless coordination and old-task protection already exist. What gets exchanged here also carries a scope, a test or a downstream obligation. |
| [Model Soups](https://arxiv.org/abs/2203.05482) averages fine-tunes; [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds and negates task vectors; [TIES](https://arxiv.org/abs/2306.01708) trims and resolves sign disagreements; [DARE](https://arxiv.org/abs/2311.03099) drops and rescales deltas. | A good one-shot merge is not evidence that later descendants can safely learn, trade, or forget. |
| [Git-Theta](https://arxiv.org/abs/2306.04529) already tracks parameter-level changes and supports efficient updates and automatic merges. [BTM](https://arxiv.org/abs/2208.03306) grows a pool of domain experts; [BTX](https://arxiv.org/abs/2403.07816) combines experts into MoE layers. [LoraHub](https://arxiv.org/abs/2307.13269) composes LoRAs from a few examples and [MoE-LoRA](https://arxiv.org/abs/2502.15828) learns mixtures of low-rank experts. | Version control, specializing experts and routing are substrates. The novel objects, if any, must change what a recipient can learn or retain. |
| [Population Based Training](https://arxiv.org/abs/1711.09846) jointly optimizes a population and its hyperparameter schedules. [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) balances exploration and imitation to produce cultural accumulation across generations in context and weights. | Keep multiple objectives alive instead of selecting one champion. Measure what survives successive handoffs without assuming that copies supply independent evidence. |

**First-test convention.** Everything below is a proposal. A/B are untouched old tasks absent from the adaptation stream; include at least one local old skill per cohort. Freeze holdouts before learning, and score live routed service as well as direct access to the relevant branch so routing failures are not mistaken for lost weights. Compare at matched total stored state (including archives, probes and metadata), data, update FLOPs, message bytes and serving calls where applicable. Use ordinary/no-exchange forks, a routed adapter bank and a central allocator with the *same* evidence, timing and access constraints as nulls wherever they can express the same operation. If only the unconstrained centralized oracle wins, report the binding constraint; if a constrained central control ties, do not claim a population advantage.

## A · Branch, specialize, exchange

### PL01 · Bridge packets — Ambitious but doable (P)
- **Mechanism:** Export a pair of counterfactuals that hold the task fixed and flip the cohort-specific preference, with a small delta that must improve both task outcomes without removing the preference flip. A receiver can import the bridge and retain its own policy.
- **Nearest prior / gap:** [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) selectively imports task weights; the packet makes cross-cohort invariance and preserved disagreement jointly testable. Unlike #378’s split, both forks keep learning and trade the invariant part.
- **Cheapest first test:** Two tiny classifiers with opposed formatting preferences and an unseen shared parity rule. Swap bridge packets versus selective transfer and routed adapters; tie if the same two probe labels in ordinary replay recover the same recipient gain.
- **Old-task retention:** After two reciprocal imports, score A/B and each cohort’s original formatting on matched inputs.

### PL02 · Disagreement-preserving transplant — Ambitious but doable (P)
- **Mechanism:** For a donor delta, store a recipient-side response Jacobian over *decision contrasts* between forks. Project the delta away from directions that close or reverse those contrasts before applying it; do not require either fork to match the other’s logits.
- **Nearest prior / gap:** [Federated Orthogonal Training](https://arxiv.org/abs/2309.01289) protects retention with orthogonal updates. Here the protected quantity is the difference between two legitimate policies, not either policy alone.
- **Cheapest first test:** Two small nonlinear heads learn opposing thresholds and a shared nuisance transform. Compare per-fork orthogonal protection and identical contrast probes used in distillation; test whether recipient gain survives when contrasts are held fixed.
- **Old-task retention:** Score standalone A/B, worst-cohort accuracy and pairwise decision reversal after three bidirectional transplants.

### PL03 · Fork successor stress test — Ambitious but doable (P)
- **Mechanism:** A proposed reunion stores the smallest successor update on which reunited and separate descendants differ in learnability. If the witness is still a credible future request, preserve separate forks even when both serve today’s inputs equally well.
- **Nearest prior / gap:** [Model Soups](https://arxiv.org/abs/2203.05482) selects on current validation; [BTM](https://arxiv.org/abs/2208.03306) keeps or combines experts. The reusable object is a falsifier for *future interchangeability*, not today’s score.
- **Cheapest first test:** Make two tiny nets agree on current inputs but use different latent features. Spend ten matched future labels after merge or split; compare ordinary merge validation plus equal rehearsal with the witness. Tie if the witness predicts no additional plasticity loss.
- **Old-task retention:** Score both cohorts’ A/B at reunion and after the future-label block.

### PL04 · Traveling exception — Ambitious but doable (P)
- **Mechanism:** Transfer a shared delta with an executable exception that references a contrast, not a user ID. A recipient places the exception in its own router and can forward the same bundle to a newly founded fork.
- **Nearest prior / gap:** [BTX](https://arxiv.org/abs/2403.07816) and [MoE-LoRA](https://arxiv.org/abs/2502.15828) route expert computation; here the routing exception travels with a specific write and must remain meaningful after a cohort relabel.
- **Cheapest first test:** Three symbolic agents with different cohort names, two sharing a real exception. Compare global delta plus relearned router and local-only adapters. Tie if spending the same labels retraining the router closes the third fork’s transfer gap.
- **Old-task retention:** On each receiving fork, score A/B and prior exception cases before and after forwarding the packet.

### PL05 · Co-teacher edge — Ambitious but doable (P)
- **Mechanism:** Offer two complementary deltas as one typed edge: validate neither in isolation, only their joint effect. Keep the identity of each co-teacher so that downstream copies can withdraw the bundle if either prerequisite changes.
- **Nearest prior / gap:** [LoraHub](https://arxiv.org/abs/2307.13269) assembles modules for a target; #79 tests epistasis. This edge is a reusable, jointly revocable transfer unit rather than a score for a static combination.
- **Cheapest first test:** Tiny networks where one learned feature is useful only with another fork’s decoder; later revise one teacher. Compare equally tuned LoRA composition and an always-atomic bundle with no withdrawal trigger. Tie if simple bundling handles the revision.
- **Old-task retention:** Check A/B and a separate pre-existing donor feature after adoption and after revocation.

### PL06 · Exchangeable refusal — Ambitious but doable (P)
- **Mechanism:** A receiver that rejects a donor update sends a minimal failing probe and the *range of effects* it could accept on that probe. A third fork can synthesize an acceptable patch without seeing the first fork’s examples or adopting its preference.
- **Nearest prior / gap:** [FedMD](https://arxiv.org/abs/1910.03581) exchanges predictions for heterogeneous distillation; #76 sends edits as evidence. Here the object is a recipient’s rejection turned into a reusable admissible interval for another donor.
- **Cheapest first test:** Three linear learners with local-only labels and a shared query dictionary. Compare rejected-bit feedback, raw logits and matched-byte interval feedback. Tie if a single scalar regret per query suffices.
- **Old-task retention:** Recheck rejecting and third-party forks on A/B and protected local contrasts after two repair rounds.

### PL07 · Disentangled fork fusion — Ambitious but doable (P)
- **Mechanism:** Forks trained in different orders exchange a four-corner functional change table (before/after each update alone and jointly). Keep the shared main effect in both copies and the interaction at its source unless it reproduces in a third lineage.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds deltas; [TIES](https://arxiv.org/abs/2306.01708) resolves sign conflicts. The object traded is an estimated interaction residual with a recipient-side replication condition; ordinary write-skew detection alone is the ledger null.
- **Cheapest first test:** Two nonlinear toy forks learn a shared feature and incompatible local labels in opposite orders. Compare TIES, additive transfer and probes used only to veto the merge. Tie if the residual buys no transfer beyond vetoing.
- **Old-task retention:** After a third fork imports the main effect, score A/B per branch under the original and reversed update order.

## B · Merge, gossip and vote

### PL08 · Functional cherry-pick — Ambitious but doable (P)
- **Mechanism:** Commit a tested behavior difference against parent and child, with no requirement that the original tensor diff survive transport. A receiver can replay the operation in its coordinate system and emit a new commit linked to the same change.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) tracks and merges structured parameter changes; [FedMD](https://arxiv.org/abs/1910.03581) shares predictions. The cherry-pick names a contrast against a specific parent, with a persistent identity across nonidentical implementations.
- **Cheapest first test:** Three ReLU nets, one with permuted channels and one with a genuine local edit. Compare parameter rebase and equal-probe parent-free distillation; tie if distillation matches both selectivity and next-hop reproducibility.
- **Old-task retention:** Score A/B, including the receiver’s private edit, after two hops and a subsequent local update.

### PL09 · Merge with a live alternative — Ambitious but doable (P)
- **Mechanism:** A merge keeps one compact rejected counter-merge and the future observation that would reopen it. When such evidence arrives, replay only the affected post-merge descendants against the alternative, not the entire ancestry.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) retains model history; [Model Soups](https://arxiv.org/abs/2203.05482) selects a result. Here discarded alternatives can become live inputs to a partial rebase triggered by later learning, rather than a passive log.
- **Cheapest first test:** Two merges of tiny adapters tie initially and separate when one rare case returns. Compare one equally sized checkpoint, manual rollback and full re-train as an oracle. Tie if the checkpoint alone recovers as quickly.
- **Old-task retention:** Score A/B and independent post-merge skills before and after reopening, not just on the recovered alternative.

### PL10 · Gossip the discriminating question — Ambitious but doable (P)
- **Mechanism:** A peer sends a question on which two candidate patches disagree, before sending either payload. A remote learner answers with local evidence; only then does the selected delta travel. Query selection accounts for how the answer would alter *future* compatibility with an already queued write.
- **Nearest prior / gap:** [FedPC](https://arxiv.org/abs/2304.07421) is already peer-to-peer continual transfer; flood M49 already sends questions. The sharpened object is a question keyed to a pending write pair, not an unsolicited request for labels.
- **Cheapest first test:** Three peers with one short message per round; make two deltas tie immediately but compose differently with tomorrow’s delta. Compare randomly sampled and immediate-gain questions; tie if delayed compatibility does not increase gain per byte.
- **Old-task retention:** Score A/B under actual gossip schedules after the queued write, including at a peer that received no payload.

### PL11 · Witness-lineage ballot — Ambitious but doable (P)
- **Mechanism:** Votes report the lineage of an observation, not just the voter checkpoint. Identical inherited claims collapse to one witness; related forks that independently rerun the test can still contribute distinct evidence.
- **Nearest prior / gap:** [TIES](https://arxiv.org/abs/2306.01708) elects signs in tensor space; the ledger already considers fleet popularity. The ballot counts independent *encounters* supporting a behavioral write, not votes by identity or static ancestry.
- **Cheapest first test:** Six peers, four descendants of a bad early teacher and two independent variants. Compare one-fork-one-vote, static lineage weighting and behavior-correlation weighting. Tie if fresh witness ancestry adds nothing with equal probes.
- **Old-task retention:** Score old A/B service across both family trees after voting and a later independent rediscovery.

### PL12 · Abstention with missing evidence — Ambitious but doable (P)
- **Mechanism:** A ballot can return `unknown on domain D` and appoint a peer whose evidence could close that hole. Permit a scoped commit before resolution, without treating abstention as assent on D.
- **Nearest prior / gap:** [FedWeIT](https://proceedings.mlr.press/v139/yoon21b.html) selects incoming knowledge by task relevance. The ballot carries an unresolved domain and a targeted evidence request that descendants inherit as a constraint.
- **Cheapest first test:** Simulate overlapping clients where only one intermittently observes a rare cohort. Compare abstain-only, unanimous gating and a fixed quarantine. Tie if targeted unknowns do not reduce either miswrites or delay.
- **Old-task retention:** Score A/B in the known domain and in D separately before, during and after resolving the abstention.

### PL13 · Probe-only gossip before consensus — Ambitious but doable (P)
- **Mechanism:** Maintain two overlays: local evidence can spread everywhere, but deployable deltas propagate only along edges where a receiver reproduced the stated effect. Record an empirical reproduction graph distinct from the message graph.
- **Nearest prior / gap:** [Decentralized PSGD](https://arxiv.org/abs/1705.09056) communicates for optimization and [FedPC](https://arxiv.org/abs/2304.07421) disseminates knowledge between peers. Separating observation edges from live-install edges makes selective evidence diffusion possible without synchronizing the weights.
- **Cheapest first test:** Ring of four learners, one delta that depends on a missing feature at two peers. Compare ordinary gossip, local admission, and two-channel propagation with equal bytes. Tie if local admission plus ordinary probe broadcast suffices.
- **Old-task retention:** Score A/B separately on certifying, observing-only and downstream peers after multiple valid and invalid broadcasts.

### PL14 · Adaptive merge ancestry — Ambitious but doable (P)
- **Mechanism:** When two forks have several common ancestors, choose a different comparison ancestor for each behavior slice. Store the mapping with the merge so later descendants know which reference established each import.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) provides versioned checkpoint changes and merge tooling. The proposal references *behavior slices* to multiple parents, including slices expressed in overlapping parameters.
- **Cheapest first test:** Tiny diamond DAG with two overlapping features acquired in crossed order. Compare a single Git-style merge base, same-weight DARE/TIES, and tensor-block merge bases. Tie if per-tensor ancestry accounts for the gain.
- **Old-task retention:** Score A/B and both pre-diamond skills after a later child imports just one slice.

### PL15 · Transfer with a recipient-signed receipt — Ambitious but doable (P)
- **Mechanism:** A recipient records gain, scope and parent version for a patch, signs that behavioral receipt, and can forward it separately from the weights. A later learner uses *receipt coverage* to decide which probes it must buy rather than reusing the original acceptance claim.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) records parameter changes; [FedFomo](https://arxiv.org/abs/2012.08565) weights collaborators by their utility to a client. The receipt lets a third party condition its own validation budget on independently tested scope.
- **Cheapest first test:** Three-stage transfer with two subdomains and sparse local probes. Compare full revalidation at equal cost, unscoped donor scores and receipt coverage; tie if ordinary held-out score sharing is as selective.
- **Old-task retention:** Evaluate A/B on all recipients, including the final learner that skips probes, after a local regime shift.

## C · Trade weight updates and skills under local information

### PL16 · Continuation swap — Ambitious but doable (P)
- **Mechanism:** Two forks each supply a provisional delta and reserve a local trial slot for the other. Complete the swap only if each recipient can learn its *next* private lesson faster with the incoming delta; immediate validation gain is not the consideration.
- **Nearest prior / gap:** [FedFomo](https://arxiv.org/abs/2012.08565) weights other models by first-order benefit to the local objective. Unlike #124’s rank leases, the swap exchanges experimentally measured reductions in future learning cost between holders of nonshareable data.
- **Cheapest first test:** Two linear feature learners each see one half of a sequence with complementary latent features. Compare equal-compute unilateral acceptance, unconditional exchange and a constrained central scheduler. Tie if immediate validation gain predicts both continuation gains.
- **Old-task retention:** Score each cohort’s A/B after the next lesson and after rejecting one side of a later swap.

### PL17 · Refutation bounty payable in a repair — Ambitious but doable (P)
- **Mechanism:** A seller posts a scoped delta and pledges one rank-limited repair on the first verified counterexample. The finder chooses whether to spend that repair on narrowing the scope or fitting a corrected patch; the buyer gets an artifact it can test and forward.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) provides patch exchange, and #124 already has audit bonds. The deliverable is an updated learner plus the repaired scope, not merely financial settlement or a validation alarm.
- **Cheapest first test:** Four rule-table agents, one rare failure visible to exactly one buyer, one auditing message each. Compare equally subsidized random audit and ordinary counterexample repair. Tie if promising repair in advance does not elicit evidence earlier.
- **Old-task retention:** After correction propagates, score A/B and the previously valid part of the patch at both the original and downstream buyers.

### PL18 · Price the missing complement — Ambitious but doable (P)
- **Mechanism:** A buyer issues a request for a delta that turns an already-owned but useless delta into a working pair. The buyer evaluates the incoming patch on and off its private complement; only the incremental joint effect can settle the trade.
- **Nearest prior / gap:** [LoraHub](https://arxiv.org/abs/2307.13269) searches over available adapters; flood M2 sells a cross term. Here the buyer’s missing-complement request induces *new* training by another fork, not just a new price for an existing combination.
- **Cheapest first test:** A buyer has a private decoder and three potential sellers can learn different features, but only one gets a training slot. Compare auctions for ready-made updates, shortlist sharing and equal-budget joint tuning with the same information. Tie if selecting from existing adapters matches.
- **Old-task retention:** Check A/B and the decoder’s original behavior after adding the complement and later removing it.

### PL19 · Swap audit rights, not capabilities — Ambitious but doable (P)
- **Mechanism:** A buyer cannot inspect a seller’s held-out examples, but can commission one local evaluation of a specified counterfactual merge. The receipt is single-scope and the buyer can exchange an evaluation on its own cohort in return, even when neither wants the other’s weights.
- **Nearest prior / gap:** [FedMD](https://arxiv.org/abs/1910.03581) pools predictions to train; #124 pays for diagnosis. This transaction trades paired *incremental merge evaluations* and can change both forks’ subsequent write decisions without moving either patch into service.
- **Cheapest first test:** Two cohorts with nonshareable tests, two merge candidates, one counterparty query each. Compare exchanging generic held-out scores and equal-cost public replay. Tie if specifying the counterfactual does not improve write selection.
- **Old-task retention:** Score the buyer’s A/B and seller’s A/B on their actual next versions, including the cohort that never imports a delta.

### PL20 · Bid in bytes of dependency — Ambitious but doable (P)
- **Mechanism:** A seller gives two forms of a skill, a tiny patch that depends on a donor feature and a larger self-contained version. A buyer bids how much future storage and serving access it will commit to that dependency, and can later switch forms using a behavior-equivalence test.
- **Nearest prior / gap:** [DARE](https://arxiv.org/abs/2311.03099) reduces the number of delta parameters; #324’s path pricing varies how data are purchased. This trade prices the *continuing dependency* incurred by installing one implementation of a skill instead of another.
- **Cheapest first test:** Three linear adapters with one shared basis whose host intermittently becomes unavailable. Compare smallest-patch-first and static full-patch purchase at equal lifetime storage and query budgets. Tie if a fixed prefetch rule matches across outage regimes.
- **Old-task retention:** Check A/B in connected and disconnected periods and immediately after switching implementations, including old skills sharing the borrowed feature.

### PL21 · Trial slots as a tradable learning resource — Ambitious but doable (P)
- **Mechanism:** Peers lend one of their protected shadow updates, not a serving slot, to fit a candidate on a local stream that the origin cannot observe. The origin receives a bound on improvement per step and can redirect the next trial; shadow weights remain local unless independently admitted.
- **Nearest prior / gap:** [PBT](https://arxiv.org/abs/1711.09846) allocates fixed compute across training members; #124 already leases capacity. The traded unit is the ability to measure a specific learning curve on a peer’s nonexportable observations before spending scarce update compute.
- **Cheapest first test:** Three online learners each see a different curvature regime; allow just two disposable trials. Compare matched local exploration and static experimental assignment. Tie if held-out performance alone chooses the same trials.
- **Old-task retention:** Score A/B on both the unchanged shadow lenders and the eventual adopters after the next real update.

## D · Lineage and inheritance

### PL22 · Inherit the disagreement, not either answer — Ambitious but doable (P)
- **Mechanism:** Bequeath two parent responses and the conditions under which each is admissible. A child learns a test to distinguish the conditions, rather than distilling an average or assuming one parent is a universal teacher.
- **Nearest prior / gap:** [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) accumulates skills by imitation and exploration; #130 filters fossils from one parent. The inheritance unit here is a paired, tagged disagreement the child can disambiguate with new evidence.
- **Cheapest first test:** Two teacher policies choose different actions depending on a hidden regime the child can query once. Compare mixture KD, best parent, and KD of parents plus an ordinary router. Tie if an off-the-shelf router trained with the same query resolves the regimes.
- **Old-task retention:** Revisit A/B from both parents and confirm the child still switches correctly after an unrelated new rule.

### PL23 · Inherit a negative genealogy — Ambitious but doable (P)
- **Mechanism:** A lineage can bequeath a failed ancestor write and the witness that falsified it, with a scope for the failure. A child probes that witness before spending training budget on a rediscovered edit; an independent pass clears the inherited veto locally.
- **Nearest prior / gap:** [PBT](https://arxiv.org/abs/1711.09846) copies successful training states. #310’s re-derivation lease renews successful shared items; here reproducible failures are transmissible and can be lifted as conditions change.
- **Cheapest first test:** Three generations repeatedly encounter a tempting shortcut whose old failure disappears in only one cohort. Compare permanent denial, no failure history and equal-byte failed-edit hashes. Tie if hashes work without the probe.
- **Old-task retention:** Score A/B after a stale veto is lifted in one child but still enforced in its sibling.

### PL24 · Optimizer-state meiotic crossover — Ambitious but doable (P)
- **Mechanism:** Choose a block’s phenotype from one parent and borrow update momentum from the other only in directions where both parents predict the same response on a shared mini-probe. Record the two provenances separately and expire borrowed momentum after a short window.
- **Nearest prior / gap:** [PBT](https://arxiv.org/abs/1711.09846) selects whole training members and hyperparameter schedules; the ledger already flags Lamarckian optimizer settings. This is multi-parent, per-direction inheritance of optimizer *state* conditional on measured agreement.
- **Cheapest first test:** Two small regressors learn different biases but the same feature; offspring get two new gradient steps. Compare whole-parent copy, reset and ungated momentum crossover. Tie if zeroing momentum is as fast and more stable.
- **Old-task retention:** Score old A/B at child initialization, two steps later and after momentum expiry, including tasks associated with the non-weight parent.

### PL25 · Leave-one-ancestor-out inheritance — Ambitious but doable (P)
- **Mechanism:** For an acquired capability, maintain a compact counterfactual child trained with one ancestry edge withheld. If withholding edge X removes useful gains, mark X as functional dependence; descendants can choose robust alternatives before X disappears.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) captures checkpoint ancestry; [BTM](https://arxiv.org/abs/2208.03306) branches from mixtures. Functional edge ablation measures dependence in an evolving *child*, which a historical commit reference or a one-shot teacher ablation cannot establish.
- **Cheapest first test:** Two parents contribute overlapping features to a third learner; later retire one parent. Compare weight attribution and one-shot teacher ablation with the withheld-edge child, using full replay as the oracle. Tie if additive source attribution predicts the same repair.
- **Old-task retention:** Score A/B and the acquired capability after simulated retirement and after the child trains another unrelated task.

### PL26 · Generation-stable skill name — Ambitious but doable (P)
- **Mechanism:** Define a skill’s persistent ID by a small behavioral fingerprint and an operation for refreshing it. Each successor must pass one earlier generation’s probes *and* a fresh probe from a separately trained peer before replacing the fingerprint.
- **Nearest prior / gap:** [Voyager](https://arxiv.org/abs/2305.16291) stores executable lifelong skills; [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) transfers competence by social learning. The refresh operation tests two kinds of continuity while allowing implementation and local use to change.
- **Cheapest first test:** Pass a sorting skill across four symbolic agents with drifting input alphabets. Compare a static signature and latest-only signatures at the same challenge budget. Tie if either static/fresh-only method prevents both drift and needless rejection.
- **Old-task retention:** Score A/B, including original and previously unseen permutations, after every refresh and a late unrelated update.

### PL27 · Protected divergent seed — Ambitious but doable (P)
- **Mechanism:** During selection, retain one seed outside the dominant lineage *only if* a cheap forward training step demonstrates a useful update response absent from the champions. It is selected as a future teacher, not just an unusual policy or a redundant serving member.
- **Nearest prior / gap:** [Effective Diversity in Population Based RL](https://arxiv.org/abs/2002.00632) uses behavior diversity to improve exploration. The seed criterion is retention-compatible *conditional plasticity* available to a future child.
- **Cheapest first test:** Four small policies with matched current performance encounter a reversal of a previously unobserved condition. Compare random reserve, behavior diversity and learning-progress ranking under one reserve slot. Tie if ordinary diversity selects equally useful teachers.
- **Old-task retention:** Evaluate A/B on the reserve and mainstream branch after selection and on the child that borrows the reserve’s update after the reversal.

## E · Collective forgetting and revival

### PL28 · Retirement with a negative transfer test — Ambitious but doable (P)
- **Mechanism:** Before retiring a shared delta, have each live descendant test both detaching it and distilling from a stale copy; keep the former if harmless, and store a small rejection probe if the latter revives the retired behavior. Do not assume parameter subtraction undoes training.
- **Nearest prior / gap:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) uses negation to suppress a task; #310 expires unrefreshed shared items. This object prevents re-import after a distributed revocation, including through a descendant with a different implementation.
- **Cheapest first test:** Three tiny adapters; one peer misses a retirement round and later advertises its older distilled model. Compare timestamp tombstones, delta negation and replay with matched probe/storage budget. Tie if version tags reject the behavior even through that new commit.
- **Old-task retention:** Measure non-retired A/B and legitimate related variants before detachment, after reconnection and after another import.

### PL29 · Distillation cut for forgetting — Ambitious but doable (P)
- **Mechanism:** Track known routes by which a feature can be re-taught, including old predictions and distilled children. Choose the smallest set of teaching edges to disable while keeping normal serving edges, then probe for the retired behavior after a simulated reconnection.
- **Nearest prior / gap:** [FedMD](https://arxiv.org/abs/1910.03581) uses distillation to move knowledge without moving weights. Instead of counting how many copies carry the item (#116), this cut tests whether an acquired behavior can return via allowed *teaching* channels.
- **Cheapest first test:** Four toy agents with logits, weights and serving links forming different graphs. Compare deactivating nodes, deleting weight packets only and the teaching-edge cut. Tie if node-based deletion matches extinction with equal service capacity.
- **Old-task retention:** Score A/B through the actual serving routes after partition healing and one full distillation cycle.

### PL30 · Last executable, not last copy — Ambitious but doable (P)
- **Mechanism:** Retain a multi-agent *execution path* for a rare skill, not a checkpoint quota. Each proposed retirement is legal only if live peers can deliver both normal and fallback routes under the named failure, including their local interfaces and latencies.
- **Nearest prior / gap:** [BTX](https://arxiv.org/abs/2403.07816) routes to experts. #116 already identifies path quorums and the common-mode bound; the sharper claim is that retirement can transfer a *dependency obligation* to an independently updated substitute via a live two-hop handover, not add more copies.
- **Cheapest first test:** Three symbolic workers, each holding only part of a workflow, plus one substitute. Remove one version at a time. Compare ordinary path quorum and greedy route repair; tie if an equal-cost quorum plus live probes recovers the same executable paths.
- **Old-task retention:** Score A/B end-to-end under one unavailable worker and a common-trunk version mismatch, with an oracle router as a diagnostic.

### PL31 · Forget locally, relearn independently — Ambitious but doable (P)
- **Mechanism:** In an agreed retirement window, refuse all ancestral demonstrations of an expiring convention but reserve one learner to try to derive it independently from permitted new evidence. It can propose the rule again under a new lineage only if fresh evidence survives counterfactual tests of the old shortcut.
- **Nearest prior / gap:** [Artificial Generational Intelligence](https://arxiv.org/abs/2406.00392) mixes imitation and exploration; #310 already renews items from fresh reality. The distinction is an explicit no-imitation window, with old and re-derived implementations challenged against the same rival explanation before readmission.
- **Cheapest first test:** In a rule stream, one convention goes stale and another becomes valid again for a different reason. Compare no-imitation probe, re-derivation lease, fixed embargo and permanent refusal. Tie if independent-refresh leases separate the two returns at equal probes.
- **Old-task retention:** Check A/B throughout the embargo and after the readmitted behavior is passed to a third learner, including related behaviors that did not retire.

### PL32 · Forget one teacher, preserve the convergent skill — Ambitious but doable (P)
- **Mechanism:** A recipient that learned the same behavior independently and from an expiring teacher keeps the independent implementation but rejects replay originating from the teacher. When origins cannot be distinguished with the evidence on hand, record an unknown and ask for a new independent witness rather than declaring success.
- **Nearest prior / gap:** [Git-Theta](https://arxiv.org/abs/2306.04529) tracks provenance of parameter edits; [Task Arithmetic](https://arxiv.org/abs/2212.04089) negates an entire task vector. The proposed operation removes one teaching dependency while preserving behavior supported by another; this is selective retirement, not a guarantee of data unlearning.
- **Cheapest first test:** Two teachers transmit the same toy skill by different features, one with an unwanted side effect. Compare removing all implementations, forgetting only the named delta, and teacher-free retraining at equal examples. Tie if deleting the named delta alone keeps the skill and stops the side effect through later transfers.
- **Old-task retention:** Evaluate A/B, the convergent skill, and an unrelated skill inherited from the other teacher after revocation and a late peer reconnection.

## Ranked deeper questions

1. **Can independent branches export the generalizable improvement without importing the policy dispute?** (PL01, PL02, PL05, PL07) Start with two real preference hills plus a hidden shared rule, then bring in a third cohort that has never seen either hill. Demand a transfer gain over both ordinary FedWeIT-style selective exchange and a matched routed adapter bank, with no extra preference reversals on A/B. If sharing ordinary labeled replay works equally well, keep the fork but drop the proposed exchange primitive.
2. **What constitutes independent evidence when weights, probes and skills all travel?** (PL10–PL13, PL15, PL26) Cross an echoing family with an independently rediscovering relative and force one rare cohort to sit outside the dominant gossip cluster. Compare raw voting, static model ancestry and witness ancestry at equal probe budgets. The result must improve both time-to-correction and worst-cohort A/B; raw update acceptance is not the endpoint.
3. **Can a population retire a teaching dependency without forgetting the useful behavior it once taught?** (PL25, PL28–PL32) Use a small diamond ancestry with an offline learner that returns with a distilled version of the retired feature. Demand that a dependency cut stops revival while old A/B and the independently supported implementation still work. If simple checkpoint deletion and revalidation match at equal state and queries, keep them instead.
4. **What should change hands when neither participant can inspect the other’s future curriculum?** (PL16–PL21, PL27) Give peers local-only evidence and one peer evaluation per round. Compare continuation swaps, missing-complement procurement and evaluation receipts against an ordinary constrained scheduler and an unconstrained oracle. Rank by samples to the next retained skill per exchanged byte, not trade volume. If the constrained scheduler ties, the operation may be useful but the market framing adds nothing.
