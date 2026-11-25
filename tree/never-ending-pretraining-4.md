# Never-ending pretraining 4 · Give learning its own interface

Child of [Never-ending pretraining 3](never-ending-pretraining-3.md) ([PR #392](https://github.com/manojbajaj95/cl/pull/392)). The [review](https://github.com/manojbajaj95/cl/blob/2def70bc50f2b5c4f9692181359ebf420c17e8a0/reviews/flood-triage.md) kept NP3-02 (change conditional odds while fixing marginals) and NP3-22 (carry a revocable source residual through distillation) at 3. No card reached 4. The test here is different from “can the weights hold another kind of effect?” Each card specifies an input a learner can accept, combine, request, or pass forward that was not expressible as a static answer edit or a per-source subtraction. Non-neural antecedents count as prior art. These are candidates, not novelty verdicts; no experiments were run.

**Common controls.** Use tiny finite tables, synthetic byte strings in two tokenizers when relevant, or one checkpoint lineage with a small set of enumerated source worlds. Start dependence cards against ordinary fine-tuning, [MEMIT](https://arxiv.org/abs/2210.07229)/[AlphaEdit](https://arxiv.org/abs/2410.02355), [DPO](https://arxiv.org/abs/2305.18290), fine-tuning with marginal KL, and an exact [I-projection](https://doi.org/10.1214/aop/1176996454) implementation of NP3-02. For distillation, use standard distillation, distill-then-[NPO](https://arxiv.org/abs/2404.05868)/gradient ascent, retraining without the source, [source-aware training](https://arxiv.org/abs/2404.01019), [influence-based removal](https://arxiv.org/abs/2507.23257), and NP3-22. [Inverse Distillation](https://arxiv.org/abs/2609.36099) and [reasoning-distillation provenance](https://arxiv.org/abs/2512.20908) are additional controls for student correction and sentence-level lineage. Count teacher interventions, acquisition cost, stored state, and update compute; when the operation needs metadata, give controls the same information. Score old tasks separately. An ordinary control that realizes the operation with comparable cost and retention kills the candidate.

## A · Accept dependence evidence before accepting an update

### NP4-01 · Accept a swap packet instead of four examples
- **Mechanism.** Ingest two observed pairs and their crossed alternative as one training unit. The sender samples the two records independently within a stratum, randomizes presentation order, and supplies which pairing was observed. Score the observed pairing against the crossed pairing using the difference of their summed log joint scores. Additive single-item terms cancel exactly; the receipt records the sampling rule that justifies conditioning on the unordered items.
- **Nearest art.** [Exact contingency-table inference](https://doi.org/10.1214/ss/1177011454) conditions away margins; [Conditional Contrastive Learning](https://arxiv.org/abs/2202.05458) constructs conditional pair signals. The candidate is a packet whose pairing policy governs whether training may consume it, not a new contrastive loss.
- **First test / kill.** Compare independently sampled pairs against ones admitted by a known joint popularity filter, arranged to have the same single-item counts. Only admit the former unless the selection can be corrected. Kill if conditional contrastive training with the same metadata separates the channels equally well, or swap supervision alone changes isolated marginal reads.
- **Retention.** Keep old single-item predictions and dependence in contexts not named by the packet.

### NP4-02 · Join across time without learning from arrival order
- **Mechanism.** Accept each half-observation into a marginal lane immediately. Retain a stable join handle and a small embedding until the partner arrives; consume the pair as one dependence observation without training on either half again. Duplicate deliveries cannot finalize a second pair. Different orders should lead to the same sufficient statistics in the finite fixture.
- **Nearest art.** [DBSP](https://arxiv.org/abs/2203.16684) incrementally maintains joins and [training with incomplete datasets](https://arxiv.org/abs/2107.00429) learns despite absent views. The claimed learner operation is to commit marginal credit early, then settle joint credit later without keeping the original inputs.
- **First test / kill.** Shuffle two synthetic delivery lanes with duplicate IDs and lost partners. Kill if a byte-matched stream join followed by ordinary training attains the same cold predictions, or if joint credit changes merely with delivery order.
- **Retention.** Keep useful labels from records whose partners never arrive, plus established joint lessons outside the delayed cohort.

### NP4-03 · Put an inconsistent lesson on hold with a witness
- **Mechanism.** Pairwise observations enter as constraints on a shared joint law. A small solver either admits a feasible batch or returns a minimal infeasible subset. The scheduler holds only constraints participating in a conflict and requests one missing joint observation; compatible disjoint learning continues. No synthetic joint labels enter the held lane.
- **Nearest art.** The [marginal polytope](https://doi.org/10.1561/2200000001) formalizes joint compatibility, and [HardNet](https://arxiv.org/abs/2410.10807) enforces feasible constraints. Here an infeasibility witness also determines what the training stream must obtain before consuming a lesson.
- **First test / kill.** Supply three pairwise anti-correlations that cannot all hold for three binary variables, then provide an adjudicating triple. Kill if independent fine-tuning with consistency regularization or an external solver-plus-queue matches admission, query cost, and retained learning.
- **Retention.** Keep compatible old dependencies and complete ordinary learning while the contradictory batch is held.

### NP4-04 · Buy a pair when another label would teach nothing
- **Mechanism.** Offer the learner a menu of separately priced observations: an unpaired first view, unpaired second view, or a joined record. Choose the purchase that most reduces disagreement about a downstream lesson across feasible couplings, not the one with the highest pointwise label entropy. Exact enumeration suffices for two binary views.
- **Nearest art.** [Active Feature Acquisition](https://arxiv.org/abs/2107.04163) buys missing features to improve a prediction; [Balke–Pearl bounds](https://doi.org/10.1080/01621459.1997.10474074) identify which effects incomplete evidence permits. The target here is a population-level coupling, and the learner can pay to link existing views without buying another label.
- **First test / kill.** Offer many cheap marginal labels whose outcomes have the same distribution in two opposite dependence worlds, and one discriminating join. Kill if ordinary active feature acquisition with the same menu reaches the same lesson at equal cost, or the learner spends on nonidentifying labels.
- **Retention.** Keep previously learned marginal competence and dependencies outside the purchased stratum.

### NP4-05 · Carry a rank relation into a new marginal regime
- **Mechanism.** Learn a coupling in randomized percentile coordinates from a small paired stream; maintain local empirical quantile maps from cheap unpaired observations. After a marginal regime change, update only those maps. Transfer a dependence lesson to new raw values without following their original thresholds; latent ties use explicit randomized quantile bins.
- **Nearest art.** [Copulas](https://doi.org/10.1007/0-387-28678-0) separate dependence and marginals; [conditional support alignment](https://arxiv.org/abs/2305.18458) addresses label-shift adaptation. The bar is a continually reusable relation whose validity survives a learned, changing coordinate map, not the fact that ranks can normalize data.
- **First test / kill.** Shift scales monotonically in one byte-encoded stream without providing new pairs. Kill if ordinary empirical-copula refitting from separate marginal maps is equally reusable at matched state, or if the candidate cannot distinguish a rank-preserving change from a broken relation once one new pair is offered.
- **Retention.** Keep old percentile-pair predictions and literal-value answers in the unchanged domain.

### NP4-06 · Hand in an estimate of matched moments without handing in the records
- **Mechanism.** Two input streams accumulate shared-seed signed sketches by stable observation ID for bounded features. Inner products estimate paired moments without restoring pairs; a variance bound travels with each estimate and blocks training when collisions make the direction ambiguous. The learner consumes moments, not guessed positive pairs.
- **Nearest art.** [Coordinated matrix product sketching](https://arxiv.org/abs/2501.17836) already estimates cross-products from separately computed sketches; [cross-table MI sketching](https://arxiv.org/abs/2403.15553) estimates dependence without materializing joins. The candidate is admitting a moment as a learning unit only when its uncertainty allows a specific update, not a new sketch or secrecy guarantee.
- **First test / kill.** Hide every cross-stream match from the learner and supply a small synthetic sketch. Kill if an equal-state sample of actual pairs gives equally precise association, or the error receipt fails under skewed IDs.
- **Retention.** Keep marginal accuracy, as well as old associations indexed by a different sketch seed.

## B · Control what the next training stream can teach

### NP4-07 · Export a new training stream with invariant exposure counts
- **Mechanism.** Compile a learned coupling into a record generator by drawing two fixed marginal bags and solving the pairing assignment. The output is fresh supervised data with an exact exposure ledger, not a weight update. Publish paired examples and their two independently checkable marginal counts to the next stage.
- **Nearest art.** [Sinkhorn distances](https://arxiv.org/abs/1306.0895) make transport across fixed marginals practical; [synthetic self-distillation](https://arxiv.org/abs/2610.13113) uses generated data for continual transfer. The candidate matters only if the exposure guarantee continues to hold through another trainer that never sees the joint model.
- **First test / kill.** Generate new synthetic bilingual word pairs at fixed word frequencies; feed them to an unchanged next-stage trainer. Kill if ordinary optimal-transport resampling has the same conservation and downstream learning at equal cost, or the next stage loses the claimed prevalence protection.
- **Retention.** Keep monolingual next-byte accuracy and earlier word pairs not targeted by the generator.

### NP4-08 · Hand a future optimizer a contract it must obey
- **Mechanism.** Compile a low-rank admissible-step map for separate marginal readers. Each new dependence gradient is pulled into the locally common tangent space, then a small exact correction restores the protected reads. The learned artifact is reusable on unseen gradients; decline a step when the constraint and advertised descent cannot coexist.
- **Nearest art.** [AlphaEdit](https://arxiv.org/abs/2410.02355) uses a null space for weight edits; [HardNet](https://arxiv.org/abs/2410.10807) imposes architecture-level constraints. The test is whether a reusable map can replace repeated recomputation as the model and contexts change, not whether null-space steps work.
- **First test / kill.** Hand the same contract to two future streams with different gradients and a region where the tangent rotates. Kill if frozen heads, repeated I-projection, or recomputed null spaces match descent and retention at equal total cost, or the map silently violates a protected read.
- **Retention.** Check the protected marginal functions on fresh examples, plus old capabilities outside their declared scope.

### NP4-09 · Separate the sampler's associations from the world's
- **Mechanism.** Require a known randomized intake policy with nonzero probabilities on every target cell. Update an association channel with a corrected joint moment, combining a predicted moment with propensity-weighted residuals. A changed policy may change which lesson arrives but not what population that lesson describes; missing support forces refusal.
- **Nearest art.** [Doubly Robust Policy Evaluation](https://arxiv.org/abs/1103.4601) combines weighting and outcome modeling. This proposal lifts the selection policy into the training interface: a batch does not carry a well-defined dependence lesson until its observation policy and overlap are known.
- **First test / kill.** Alternate two known intake policies that reverse the apparent direction of association. Kill if standard inverse propensity weighted fine-tuning with the same policy and state learns equally well, or the interface invents a target effect in an unseen cell.
- **Retention.** Keep the old intake-independent marginal reads and previously identified relations in stable strata.

### NP4-10 · Intervene on prevalence during training to demote a shortcut
- **Mechanism.** Choose among permitted marginal interventions that maximize disagreement between a prevalence shortcut and a stable paired-label mechanism. Reweight intact environments or use a known simulator; never arbitrarily resample coordinates that would destroy the causal lesson. The intervention is a curriculum action selected for the current learner, not an edited fact.
- **Nearest art.** [Invariant Risk Minimization](https://arxiv.org/abs/1907.02893) seeks predictors stable across environments, and its [invariance-penalty analysis](https://arxiv.org/abs/2106.09777) warns that penalty choices can fail. The candidate chooses a realizable training intervention rather than consuming a fixed list of environments.
- **First test / kill.** Give two candidate environments at equal cost, only one of which breaks a planted shortcut. Kill if adversarial environment selection with ordinary IRM or balanced sampling matches learning and retention, or the selected intervention distorts the target mechanism.
- **Retention.** Keep old predictive uses of the shifted covariate that are valid outside the shortcut context.

### NP4-11 · Accumulate interaction evidence before choosing the reporting bins
- **Mechanism.** Store paired moments in a declared small multiresolution basis rather than committing examples to today's contingency table. Each later bin request compiles to a linear query on those moments, with an explicit approximation error or refusal. The reusable artifact is a training summary whose observation vocabulary can change without replay.
- **Nearest art.** [Graphical-model sufficient statistics](https://doi.org/10.1561/2200000001) and [dataset condensation by gradient matching](https://arxiv.org/abs/2006.05929) summarize data for later fitting. Here the allowed future moment queries are the interface, not the old gradient or objective.
- **First test / kill.** Keep a fixed byte budget for a synthetic paired stream; change the bins after all raw pairs expire. Kill if a reservoir or an ordinary multiresolution histogram meets the same resolution/retention curve, or the summary claims resolution finer than its metadata supports.
- **Retention.** Reproduce old bin queries and old marginal predictions at their original resolution.

### NP4-12 · Learn from products of prediction errors owned by different updates
- **Mechanism.** Train two marginal nuisance models on alternating folds, then use products of held-out residuals as labels for a conditional covariance channel. Transfer this residual score construction when one nuisance model is replaced; a first-order nuisance error should not create first-order dependence bias when the other nuisance is correct.
- **Nearest art.** [Double/debiased machine learning](https://arxiv.org/abs/1608.00060) uses orthogonality and cross-fitting to control nuisance error. The candidate is a continuing training contract that lets marginal learners advance independently without their current modeling errors becoming joint lessons.
- **First test / kill.** Drift one feature distribution while its marginal learner lags, under zero true conditional covariance. Kill if offline cross-fitted nuisance scores or separate fine-tuning plus marginal KL match at equal state and delay, or lag produces a spurious joint signal.
- **Retention.** Keep old nonzero correlations and old marginal heads after replacing the drifting nuisance estimate.

## C · Distill future learning behavior, not just today's teacher

### NP4-13 · Teach a response to future evidence
- **Mechanism.** Specify probe examples and readouts in a shared observable basis. Take and roll back one teacher step per probe, then distill the map from gradients in the shared basis to changes in held-out reads. The student realizes that map as a low-rank local update rule in its own weights; agreement before training is a separate objective.
- **Nearest art.** [Sobolev training](https://arxiv.org/abs/1706.04859) transfers input derivatives, [trajectory matching](https://arxiv.org/abs/2203.11932) matches parameter trajectories, and [online label-free gradient matching](https://arxiv.org/abs/2611.03496) addresses continual language modeling. The candidate must transfer responses to unseen training perturbations rather than replay known ones.
- **First test / kill.** Distill from two teachers with the same current outputs but opposite post-update responses to a withheld example. Kill if trajectory matching or matched meta-initialization predicts both responses on fresh probes equally well.
- **Retention.** Keep pre-update teacher fidelity and old tasks unaffected by the probe family after several student steps.

### NP4-14 · Export the skill that only a coalition can teach
- **Mechanism.** For two sources, transfer four teacher worlds and factor their predictions into a base, two single-source terms, and a mixed finite difference. The student must not credit a jointly learned rule to either source alone; admit it as a reusable coalition lesson. Start with exactly two sources; do not assume sparse high-order terms later.
- **Nearest art.** [Data Shapley](https://arxiv.org/abs/1904.02868) assigns value from contributor coalitions and [Task Arithmetic](https://arxiv.org/abs/2212.04089) combines differences in weights. This candidate retains the mixed term as a trainable object instead of dividing it among sources or fitting the complete teacher.
- **First test / kill.** Give each source one half of a synthetic translation rule. Kill if ordinary residual distillation plus task-vector arithmetic reproduces base, singleton and coalition behaviors on new compositions, or if the mixed term leaks to a singleton.
- **Retention.** Keep single-source facts and skills already present in the common teacher.

### NP4-15 · Distill an interpreter for evidence, not a list of past rulings
- **Mechanism.** Transfer a small typed program that converts observations and source relations into allowed teaching targets. Distill by demonstrating its behavior on program fragments, then execute new source IDs and evidence combinations the teacher never handled. In the first fixture, use finite proof operators with compositional parameters.
- **Nearest art.** [Provenance semirings](https://doi.org/10.1145/1265530.1265535) express compositional derivations; [reasoning distillation](https://arxiv.org/abs/2512.20908) traces which sentences enter distilled reasoning. The object that must transfer is the rule for accepting a new derivation, not its historical sentence trail.
- **First test / kill.** Withhold one proof shape and all its source IDs during distillation. Kill if a symbolic interpreter or chain-of-thought KD matches proof-dependent transfer and resource cost, or if the student memorizes eligible sources instead of executing the rule.
- **Retention.** Keep previously valid proofs and established facts unaffected by new evidence types.

### NP4-16 · Pass along the rule for assigning credit to a later label
- **Mechanism.** Let a teacher with privileged annotations expose the partition of a long example to which a delayed label should assign credit. Train a student routing rule but do not expose the outcomes at transfer. On a future stream, the student applies the rule to its own fresh labels; clear gradients from other spans by construction in the fixture.
- **Nearest art.** [Privileged Information Distillation](https://arxiv.org/abs/2602.04942) transfers a better-informed teacher and [RUDDER](https://arxiv.org/abs/1806.07857) redistributes delayed credit. Here the object is a reusable assignment rule that must work for labels the teacher has never seen.
- **First test / kill.** Transfer routing on synthetic multi-section records, then teach a disjoint set of labels with the same roles. Kill if ordinary privileged logit KD plus rationale masks routes credit as well at matched cost or privileged dependence survives on an irrelevant section.
- **Retention.** Keep competence on old labels and old routing in record types with a different witness section.

### NP4-17 · Promote a teacher hint to independent student evidence
- **Mechanism.** A teacher claim enters only as a proposed hypothesis. Accept it into the student's independent lane after a student-controlled, source-blind observation tests a discriminating implication. Maintain two states that can currently predict the same answer but differ in whether the hint is allowed to teach related queries.
- **Nearest art.** [A Good Self-Teacher Meets the Student Where They Are](https://arxiv.org/abs/2610.10447) adapts teacher and student jointly; [source-aware training](https://arxiv.org/abs/2404.01019) associates knowledge with its source. This candidate transfers hypothesis proposals, not permission to count the teacher as an independent witness.
- **First test / kill.** Use correct and spurious hypotheses that agree on the teacher transcript. Give one discriminating student observation for each. Kill if ordinary pseudo-labeling with validation learns the same novel consequences at the same observation cost, or if an untested hint graduates.
- **Retention.** Keep prior student-verified facts and teacher-dependent competencies that were never promoted.

### NP4-18 · Distill a decision about which evidence to ask for
- **Mechanism.** Train the student on a teacher's counterfactual choice of acquisition, not the answer acquired. In small source worlds, vary which independent records are visible and distill the action that reduces uncertainty about a targeted rule per unit cost. At the next phase, the same learner uses the policy to choose observations in its training stream.
- **Nearest art.** [Oracle-teacher feature acquisition](https://arxiv.org/abs/2611.26598) already distills which available measurement to buy for an instance; [Ask to Distill](https://arxiv.org/abs/2610.27450) learns which prompts elicit useful teaching. Here purchasing a witness changes which population rule future training can identify, not only today's instance prediction.
- **First test / kill.** Transfer a policy trained on one set of synthetic labs to a disjoint set with different prices and duplicate echoes. Kill if OracleImitator given the same source graph and a rule-level utility, or an ordinary uncertainty policy, learns as quickly at equal acquisition cost.
- **Retention.** Keep previously mastered rules while the policy spends on the new hypotheses.

### NP4-19 · Compress checkpoints by equivalence under future operations
- **Mechanism.** Define the state to keep by a declared family of future operations such as source consolidation and fresh lessons. In a linear fixture, start with the readout rows and close their span under right multiplication by every operation matrix. Distill coordinates in that span. A discarded direction is then invisible after any composition, not merely invisible now. Refuse compression if the closed space is full.
- **Nearest art.** [Representation learning with bisimulation](https://arxiv.org/abs/2006.10742) keeps equivalent control states together; [Sketched Metadifferentiation](https://arxiv.org/abs/2609.15044) compresses data effects. This uses learner updates as actions and compares the retained state against generic bisimulation and one-step attribution, not just output matching.
- **First test / kill.** Compress two checkpoints with identical outputs but a hidden difference that changes the second operation after the first. Kill if ordinary output KD plus a response sketch matches the operation family and state budget, or if compression merges the two inequivalent checkpoints.
- **Retention.** Keep old cold predictions and already validated two-operation behavior after compression.

### NP4-20 · Carry an order dependency, not a training schedule
- **Mechanism.** Package a teaching step with a compact prerequisite and an allowed substitute, such as “learn any one certified parse of this format before applying the rule.” The student negotiates the order using its current competence; it can omit already satisfied predecessors and must not imitate the teacher's entire ordering.
- **Nearest art.** [Language model curriculum learning](https://arxiv.org/abs/2506.11300) directly compares ordering and pacing strategies; [trajectory matching](https://arxiv.org/abs/2203.11932) compresses a teacher trajectory. A partial order with interchangeable prerequisites is a different transferable object from a good trajectory.
- **First test / kill.** Use two students with complementary synthetic prerequisites; each should skip a different lesson and reach the same skill. Kill if ordinary curriculum learning with the prerequisite metadata matches the handoff at equal cost, or the student follows the teacher's order regardless.
- **Retention.** Preserve alternative old prerequisites and tasks the student brought to the handoff.

## D · Keep different grounds for future training separate

### NP4-21 · Compose independently prepared lessons with a common ancestor only once
- **Mechanism.** A teaching capsule names a common checkpoint and exports an executable update on a narrow state, plus its precondition. Given sibling capsules in one lineage, apply the ancestor once and compose updates only when their preconditions remain valid; an overlapping pair requires an explicit interaction witness rather than either order by default.
- **Nearest art.** [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds weight differences from a common base and [DisTaC](https://arxiv.org/abs/2508.01148) conditions task vectors for merging. Here the bar is reusable *sequential* applicability to cases where both merge controls already succeed at present-day outputs.
- **First test / kill.** Merge two capsules locally, then inject a third lesson whose precondition tests an earlier distinction. Kill if task arithmetic or DisTaC preserves the same later applicability at equal cost or the interface accepts a known incompatible sequence.
- **Retention.** Keep common-ancestor skills and each capsule's independent lessons on held-out cases.

### NP4-22 · Separate the source that supplied the rule class from those that supplied its examples
- **Mechanism.** Transfer a hypothesis constructor separately from the evidence that selects a member of its class. The student can replace the constructor with an independently proposed class and refit from retained sufficient statistics, even when no source is removed. The interface says which observations still constrain the new class and which are not informative.
- **Nearest art.** [Unifying distillation and privileged information](https://arxiv.org/abs/1511.03643) studies extra teaching information, and [Corrective Machine Unlearning](https://arxiv.org/abs/2402.14015) targets effects of corrupted data. Neither a source label on the examples nor a residual in their logits captures who supplied the hypothesis space.
- **First test / kill.** Make two teacher architectures fit the same short strings but extrapolate different grammars. Replace the rule class without deleting records. Kill if architecture replacement plus matched sufficient-statistic fitting already does everything the capsule promises, or if unchanged evidence is needlessly forgotten.
- **Retention.** Keep fitted observations, stable extrapolations shared by both classes, and unrelated old grammar rules.

### NP4-23 · Distill who chose the prompts separately from who answered them
- **Mechanism.** Treat prompt selection and target generation as separate teacher actions. Expose the student to a small randomized auditing stream with logged proposal weights. The student learns the answer mechanism on common support and an acquisition policy for gaps; replacement of the prompt policy does not automatically invalidate answer content.
- **Nearest art.** [Beyond Prompt Count](https://arxiv.org/abs/2609.37377) analyzes how data shapes transfer in on-policy distillation, and [Doubly Robust Policy Evaluation](https://arxiv.org/abs/1103.4601) handles logged selection. The new contract allows the student to change what gets asked without claiming it learned answers in places never sampled.
- **First test / kill.** Give two teachers identical answers on all shared prompts but one never selects a rare category. Swap prompt policies. Kill if fixed-mixture KD plus importance weighting transfers equally well, or if the student reports verified knowledge outside both supports instead of requesting evidence.
- **Retention.** Keep answer competence on old shared prompts and under the other, unchanged prompt policy.

### NP4-24 · Transfer where a teacher may supervise before transferring what it says
- **Mechanism.** Distill a certificate of supported comparisons separately from answer confidence. The student must use its own labels or another teacher when the transferred certificate excludes a query, even if the old teacher is confidently extrapolating. Implement the certificate with a small set of features and valid support cells.
- **Nearest art.** [Conformal prediction](https://arxiv.org/abs/2107.07511) qualifies confidence under explicit assumptions, and [conditional support alignment](https://arxiv.org/abs/2305.18458) reasons about domain mismatch. Unlike calibrated KD, the target of transfer is an admission rule for future supervision, not a wider prediction set.
- **First test / kill.** Offer a confident teacher that is wrong exactly in one unsupported slice. Give the student a small independent stream there. Kill if standard confidence-gated KD with the same support information performs equally well, or the unsupported teacher still steers that slice.
- **Retention.** Preserve correct old teacher lessons in certified cells and student-led performance in other unsupported cells.

### NP4-25 · Move a teacher's evidence into a student with a different base rate
- **Mechanism.** Transfer an identifiable likelihood ratio of two evidence-generating processes, not the teacher posterior over labels. The student supplies its own class prior from later data; it combines the teacher experiment once with that prior and checks whether the conditions allowing factorization still hold.
- **Nearest art.** [Estimation beyond data reweighting](https://arxiv.org/abs/2305.10898) targets distribution-shift problems, and [privileged distillation](https://arxiv.org/abs/1511.03643) shares information available only to a teacher. Prior correction is standard; this candidate is only a new teaching unit if the evidence can be incrementally reused without rediscovering the teacher experiment.
- **First test / kill.** Train on the same two likelihoods with different teacher and student base rates; change the student rate twice. Kill if ordinary label-shift correction plus soft targets matches likelihood reuse, state, and retention, or the teacher's prior leaks into the result.
- **Retention.** Keep old evidence sensitivity and the unshifted prior in a separate domain.

### NP4-26 · Transfer how a source errs so the student can learn from future reports
- **Mechanism.** Teach a source-conditioned observation channel using teacher worlds with clean and noisy readings of the same latent labels. The student receives only later noisy reports and uses the channel as an input adapter to its learning objective. It can replace the latent prior independently; it need not imitate teacher answers.
- **Nearest art.** [Integrating Conflicting Data](https://doi.org/10.14778/1687627.1687690) estimates trustworthiness and copying; [privileged-information distillation](https://arxiv.org/abs/2602.04942) transfers a better-informed signal. This transfers a likelihood for interpreting future evidence, not a reliability tag or removal of an old record.
- **First test / kill.** Give a synthetic source opposite error patterns on two classes at equal headline accuracy. Teach its confusion channel and then stream noisy observations about new entities. Kill if ordinary confusion-matrix correction with matched supervision is equally reusable, or the student learns the source's bias as fact.
- **Retention.** Keep old clean labels and prior correction channels for independent sources.

## Ranked deeper questions

1. **Can a learner request the right evidence when its target is not identifiable from any number of marginal items?** Start with NP4-04, with NP4-01 defining what a paid join permits. Require acquisition savings against active feature acquisition that receives the same menu. If metadata plus a standard oracle suffices, stop.
2. **What must a checkpoint remember to preserve how it will learn rather than what it will say?** Compare NP4-13 and NP4-19 on equal-read checkpoints with opposite responses after a sequence. Require held-out composition, old-task retention, and less state than an explicit response table or matched replay.
3. **Can teacher effects be composed without either double-counting the ancestor or flattening a genuinely joint skill?** Start with NP4-14 and NP4-21 on an exact two-source toy. Require correct singleton, joint, and held-out successive lessons, not merely recovery of the original teacher.
4. **Can a student acquire independent grounds for a teacher's conclusion without inheriting the teacher's selection bias?** Pair NP4-17 with NP4-23. Start with two teachers that agree on their shared transcript but make different acquisition choices. Require the student to spend its own observation budget where it changes entitlement to a conclusion, while keeping unrelated old knowledge.
