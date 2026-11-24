# Flood batch 1 (merged-ideas proposer): 34 raw ideas, unfiltered

Format: mechanism, why it's new, and the cheapest first test. No self-filtering; the reviewer ranks the pool. Lesson/memory tests include the usual filler and entropy-matched temperature arms. Paths refer to existing harnesses (see `ideas/merged/batch-1.md` and `batch-2.md`).

1. **Lesson vaccination.** Fine-tune the reader on deliberately corrupted lessons paired with their true outcomes, so it learns a state-dependent override threshold. This lowers defect transmission without an external verifier. *New:* the verifier term of the contamination law moves inside the reader. *Test:* 0.5B LoRA on 2k vaccinated pairs in the challenge world; measure τ and the true-lesson follow index.

2. **Dreaming at the decision boundary.** During sleep, search for self-generated states whose margin is below the directive shift, and consolidate lessons only there, with N1 masks. *New:* compute goes only where a lesson can change behavior. *Test:* M3 world; boundary dreams vs random dreams vs real replay at equal tokens.

3. **Trainable trust dial.** Each stored fact gets a scalar override budget, meta-trained to be low for facts that later change and high for stable ones. *New:* how anchored a memory is becomes a learned variable. *Test:* synthetic churn world on 0.5B; check that the dial learns each fact's change rate.

4. **Lesson market.** Fleet agents trade lessons priced by flippable mass × verified lift on the buyer's own states. *New:* contagion is controlled by prices, not by verification. *Test:* `pilots/fleet_sp/` + challenge world, 8 agents; market vs uniform vs bandit sharing.

5. **Global antidote for diffuse damage.** Learn a low-rank function-space direction from 50 probe facts and subtract it after each update. *New:* the bet is that damage diffuse in parameter space is low-rank in function space. *Test:* #24 harness at ranks 1–8 vs targeted rollback.

6. **Margin thermostat.** Keep every protected fact's margin inside a band [m_lo, m_hi] during training: raise it if it falls, release it if it rises too high so the fact stays editable. *New:* a two-sided margin constraint that trades retention against editability. *Test:* #24 GPT-2-XL; band vs L2-to-init vs EWC at equal shift gain.

7. **Overridability-weighted EWC.** Weight the Fisher penalty by each fact's in-context follow index: anchored facts need no protection, unanchored ones do. *New:* importance comes from context behavior, not gradients. *Test:* #24 harness, EWC vs follow-weighted EWC.

8. **Lessons as logit-space vectors.** Distill each lesson into a fixed vector added to the logits only when the base margin is below the shift. *New:* gates by margin, so the lesson costs no context tokens and does no harm in confident states. *Test:* A3 world, vector vs in-context lesson vs temperature.

9. **Entropy-debt accounting.** Since most lesson effect is entropy, track the cumulative entropy change each lesson causes, and retire lessons whose argmax effect is zero while their entropy effect is non-zero. *New:* separates the "useful flip" part of a lesson from its "temperature" part. *Test:* reanalyze #27/#29 tables for each lesson's flip vs entropy share.

10. **Position-prior scrubbing.** Before consolidating, train the model so it has no position/order prior in the action slot. #33 suggests this makes it follow lessons. *New:* removing an anchor to buy lesson-followability. *Test:* 1.5B with permutation-augmented SFT; follow index before and after.

11. **Anchor transplant.** Copy the residual direction that makes an anchored fact resistant onto a new fact so it resists override. *New:* makes stability a transferable vector. *Test:* GPT-2-XL; patch the anchor direction and measure follow index and retention.

12. **Contradiction-first curriculum.** Order continual tasks so each new one first contradicts the previous one on its smallest-margin items. *New:* stress-tests correctability early, so later anchoring is deliberate. *Test:* M3 world; contradiction-first vs random order, final retention and follow.

13. **Self-play forgetting adversary.** A second model writes fine-tuning batches that maximize functional damage on probe facts; the learner trains on its own rehearsal of the adversary's worst cases. *New:* a learned adversary for forgetting, not for attacks. *Test:* #24; adversary-hardened vs replay at equal tokens.

14. **Lesson half-life from correctability.** Each lesson's TTL is set by how fast its follow index decays across consolidation cycles (R1). *New:* data-driven retirement, not recency. *Test:* M3 repeated-consolidation; TTL vs keep-all vs recency.

15. **Two-route memory.** Every lesson is written twice: to a sticky mid-layer route and to an editable readout route, and the readout copy is retired once the sticky copy agrees for k cycles. *New:* a dual store like the hippocampus and neocortex, with correctability as the transfer signal. *Test:* MX1 arms plus a dual arm.

16. **Interference-aware lesson packing.** Since B3 shows real second lessons hurt more than filler, choose which lessons appear together in the context by a learned pairwise interference matrix. *New:* combinatorial context packing. *Test:* B3 harness; packed vs random vs retrieval sets.

17. **Counterfactual lesson credit.** Credit each lesson by the log-prob change on the chosen action in the states where it flipped the argmax; ignore its entropy effect. *New:* removes the temperature confound from lesson credit assignment. *Test:* A3/G1 cached tables.

18. **Margin-matched replay buffer.** Choose which old items to replay so that the buffer's margin histogram matches the new task's margin histogram. *New:* targets interference by matching margin distributions rather than by loss. *Test:* replay pilot; matched vs MIR vs random.

19. **Salience as a learned optimizer.** Use M2's per-memory attention bias as a learned learning-rate multiplier for the corresponding fine-tuning data. *New:* the context-salience signal drives weight updates. *Test:* M2 + M3; salience-scaled LR vs uniform.

20. **Mask-inherited consolidation.** Train LoRA only on the layers where N1 masks showed visibility helped. *New:* the attention-visibility map defines where weights get written. *Test:* N1 layer map → LoRA layer subset vs all layers.

21. **Weights that forget on purpose.** After each task, apply a small learned noise that targets only the parameters that move high-margin facts, keeping the model plastic. *New:* targeted plasticity injection steered by function, not magnitude. *Test:* plasticity scripts; targeted vs uniform shrink-perturb.

22. **Correctability probes as a training loss.** Add a loss that keeps the follow index of held-out contradicting directives above a floor during consolidation. *New:* editability is regularized directly. *Test:* M3 world; with and without the floor, measuring retention.

23. **Lesson compression into a 1-token handle.** Distill each lesson into one learned token embedding; the reader decides whether to attend to it, as in N1. *New:* lessons cost almost no context and can be masked per layer. *Test:* A3 world; handle vs full text vs filler token.

24. **Fleet disagreement as a teacher.** When fleet members disagree at small margin, that state becomes a training example labeled by an external check. *New:* disagreement-driven active learning across agents with shared memory. *Test:* `pilots/fleet_sp/`.

25. **Temporal causality ledger.** Store for each weight update which lessons caused it (provenance), and roll back a lesson's effect by replaying with that lesson's gradient negated. *New:* provenance-level unlearning for continual agents. *Test:* challenge world, provenance closure vs negated-gradient rollback.

26. **Order-invariance as a learned property.** Train with a two-order consistency loss (the comparator from PR #11/#17) so the final model does not depend on task order. *New:* uses the comparator as a regularizer. *Test:* utility-eviction world; consistency loss vs append-only.

27. **Syndrome fingerprints for model diffing.** Characterize each update by its functional-drop profile across 1k probe facts, and cluster updates. *New:* a taxonomy of updates by the damage they do. *Test:* #24 with 20 updates, clustering stability.

28. **Lesson ecology.** Lessons have fitness (use × lift) and reproduce by mutation (rewording), and a lesson dies when its niche (the states it flips) is taken by a better lesson. *New:* evolutionary memory management with niche exclusion. *Test:* G1 router; ecology vs LOO pruning.

29. **Directive-shift calibration.** Teach the model to output, alongside each answer, the directive shift needed to change it (its own override budget). *New:* self-reported correctability for humans and verifiers. *Test:* 0.5B; regress the reported vs measured shift.

30. **Consolidation by distillation into a frozen copy's margins.** Consolidate a lesson by matching the margins the lesson induces, not its token distribution. *New:* margin-space distillation avoids copying the temperature. *Test:* M3; margin-KD vs token-KD vs effect-class distillation.

31. **Sleep-phase rank budget.** Each sleep cycle gets a fixed LoRA rank; lessons compete for rank by flippable mass, and losers stay in context. *New:* a hard capacity market between weights and context. *Test:* M3; rank-budgeted vs all-in.

32. **Rare-event insurance.** Keep a small set of "sentinel" probes for rare events, and block any update that drops a sentinel's margin below a threshold. *New:* constrained updates guarded by sentinel margins. *Test:* rare-event world (label-conflict caveat noted).

33. **Lesson-conditioned temperature removal.** At inference, subtract the entropy-matched temperature effect of the lesson, leaving only its directional effect. *New:* isolates and deploys only the useful part of a lesson. *Test:* A3/G1 tables; debiased vs raw lesson.

34. **Model writes its own unit tests for memory.** Each consolidated lesson comes with self-written probe questions; a lesson is retired when its probes drift. *New:* self-maintained regression suite for parametric memory. *Test:* M3 world; probe-drift retirement vs keep-all vs recency.
