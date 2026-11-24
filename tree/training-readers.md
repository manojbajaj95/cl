# Training readers: what still needs state after inference moves?

**Status:** Ideas only; no experiments, probe code, or GPU. **Parent:** [Declared write footprints](declared-footprints.md) ([PR #159](https://github.com/manojbajaj95/cl/pull/159)), cards 14 and 16. **Review seed:** [Flood triage row 255](https://github.com/manojbajaj95/cl/blob/a478b5ec2e2d98f7f6998f0df1ed38e0ab7e49f3/reviews/flood-triage.md#L255), two score-3 ideas: count permitted future training reads after inference drains, and choose the replacement whose receipt removes the last reader of useful shared state.

## Is future-training dependence a new object for continual learning?

An optimizer bank, frozen teacher, Fisher/anchor pair or replay buffer may have no inference readers and still be needed by an admitted training continuation. Track two things separately: **a pending access** to a version is a lifetime obligation even if its eventual read would have negligible effect; **a functional dependence** is evidence that substituting or withholding the state changes what an admissible continuation can learn or retain within its budget. Read tracking settles which accesses must be migrated or drained. It does not tell us how to train a replacement that needs a different set of accesses. Conversely, a successful ablation does not by itself rebind a program or prevent a late read.

Give each training obligation a versioned continuation family, an admission window, performance and retention floors, and a resource envelope. A family might be “five scheduled steps of B with Adam and a teacher, on draws from this stream,” not “whatever we might want to learn someday.” Release a physical group only after inference and training obligations are discharged and all old-version work has drained. Discharge by completion with no further admission, or by checking a replacement continuation that meets the contract without reading the group and atomically switching admissions to it. An untested branch inside the contract remains a blocker. A future family outside the contract is not covered; enforce that boundary and report the cost of rejecting or rebuilding for it. A migration receipt is scoped to that group, version, family and evidence; a sample of successful continuations is not a proof for the whole family.

**Paper case.** A and C already serve from replacements. Old optimizer bank `g` is large enough to train B; old teacher bank `h` is not. C's next calibration has migrated off `g` but still reads `h`. A's pending refresh has one program that drops `h` but reads `g`, and another that drops `g` but reads `h`. Both meet the same old-service and refresh targets. Pick the second if it can be built and verified within the overlap cap: it removes the last read of `g`, including pending training, without pretending that `h` is also free. Close admissions and drain old versions, overwrite `g` with B's allocation, and run the real A/C refreshes while training B. Independently match the inference weights at the cut in two learners and vary the pending slot or teacher read: identical current outputs need not imply identical post-refresh A/C. Inference-only retirement fails the access contract; exact joint selection given both programs and the complete graph gets the right answer. The toy demonstrates the decision, not novelty.

## Prior-art screen and common CPU controls

- **Training-only state is established.** [Adam](https://arxiv.org/abs/1412.6980), [optimizer resets](https://arxiv.org/abs/2306.17833), [TAG](https://arxiv.org/abs/2105.05155) and [optimizer-state trait transfer](https://arxiv.org/abs/2608.20442) cover histories, resets, task-dependent moments and delayed behavior. [Momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) and [delayed-release edits (PR #141)](https://github.com/manojbajaj95/cl/pull/141) already separate serving from optimizer-carried futures. The question here is when one can irreversibly reuse the backing storage without forfeiting an already admitted training capability, not whether slots store history.
- **Teachers, anchors and replay are established.** [Learning without Forgetting](https://arxiv.org/abs/1606.09282), [momentum distillation in online CL](https://arxiv.org/abs/2309.02870), [EWC](https://arxiv.org/abs/1612.00796), [GPM](https://arxiv.org/abs/2103.09762) and [Dark Experience Replay (DER)](https://arxiv.org/abs/2004.07211) already use such state. [Matching Training Trajectories (MTT)](https://arxiv.org/abs/2203.11932) compresses training evidence by matching weight trajectories. Compare cached logits, reset slots, a low-rank sketch and same-byte replay before claiming any new operation. This is a quick HF and repository prior-art screen, not clearance.
- **Retirement and scheduling are established.** [RCU](https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html) handles removal and draining; program reference tracking, effect declarations and [transactional memory](https://arxiv.org/abs/1502.04908) can protect pending uses when reservations are registered. [MPLS make-before-break](https://www.rfc-editor.org/rfc/rfc3209.html#section-4.6.4), [make-before-break writes (PR #157)](https://github.com/manojbajaj95/cl/pull/157) and [disjunctive protection](disjunctive-protection.md) are controls for handover and alternative supports. Compare actual-reads-only tracking with reservation-aware tracking, and also give the combined baseline the same checked effects, dependency graph, candidates and freedom to replan. Do not call the same optimizer on the same candidate set a new CL primitive.
- **Follow the [idea ledger](https://github.com/manojbajaj95/cl/blob/a478b5ec2e2d98f7f6998f0df1ed38e0ab7e49f3/reviews/idea-ledger.md).** No credit for exact restore, trained-on audit cases, planted thresholds or a sparse-damage assumption. The ledger already rejected teacher-refresh novelty against [CGTR](https://arxiv.org/abs/2606.03532), and found no clean separation of teacher depletion from ordinary task interference. Use paired same-start continuations with identical data, starting margins and schedules when isolating a read; match B progress when comparing whole policies. A combined proposal must beat the stacked controls, not just each constituent.
- **Common first-test protocol.** Start with rational linear updates or a tiny CPU MLP on three tasks. Hold out ordinary A/C examples from all training, audit and selection; measure each against its acquisition reference before handover, at visible prefixes, and through real continuations **after destructive reuse**, with no extra recovery pass. Track rare slices separately. Price weights, states, copies, staged scratch, failed builds, checks and recomputation; report peak bytes, byte-time, time to release and whether B actually uses the region. Compare at matched B progress and old-task floors; report infeasible matches rather than dropping tasks. Enumerate tiny worlds exactly; on sampled streams report false releases and false pins against paired shadow branches, not just retention on successful migrations. Labels: **P** = candidate primitive if the stated control fails; **I** = improvement or audit.

## Idea cards

### Find out which future training really needs the state

#### 1. A reservation before the first training read (I)
- **Mechanism:** Register a scheduled training continuation against versioned slots or teachers before it can be queued; deny reuse until it completes, is canceled within contract, or migrates.
- **Novelty vs nearest prior art:** RCU with explicit reservations and [transactional memory](https://arxiv.org/abs/1502.04908) already handle lifetimes; this tests the CL cost of ignoring queued-but-not-started work.
- **Cheapest first test:** Start matched scalar learners with identical weights and different pending slot/teacher reads. Put reuse between service cutover and the first refresh, with inference counts, actual-access tracking and full reservations as arms.
- **Old-task retention check:** Score ordinary A/C at cutover and after both refreshes at matched B; record any dropped refresh as unmet service.

#### 2. Find the shortest continuation that separates two learner states (I)
- **Mechanism:** Search permitted batch and mode sequences for the shortest suffix where replacing a group changes attainment of a retention or learning floor; use the suffix to reject a false receipt.
- **Novelty vs nearest prior art:** [AdamW input–state–output dynamics](https://arxiv.org/abs/2608.19762) and optimizer transplants already predict divergence. Test contract-changing witnesses beyond one-step response, not divergence itself.
- **Cheapest first test:** Enumerate two to five updates of a two-feature learner with a clip or augmentation gate; compare one-step, linearized and random suffix audits at equal query cost.
- **Old-task retention check:** On untouched A/C test sets, follow each audited suffix and held-out suffixes after the migration decision; score the worst prefix.

#### 3. Reserve a conditional reader, not its whole job (I)
- **Mechanism:** Localize a reservation to a reachable branch such as “query the teacher if the replay margin drops below the trigger.” Discharge only if the branch is unreachable under the versioned continuation, or can run without the teacher.
- **Novelty vs nearest prior art:** [Sequential effects](https://arxiv.org/abs/1808.02010) can express conditionals; novelty is not branch-sensitive analysis but finding useful CL lifetime savings without overfitting observed branches.
- **Cheapest first test:** Enumerate six-step batch strings in a clipped linear classifier; compare unconditional pins, trace frequency and exact branch feasibility, then inject a reachable rare trigger.
- **Old-task retention check:** Score A/C on common paths and the rare trigger after reuse, including fallback execution under the same deadline.

#### 4. Discover joint dependencies that single-state ablation misses (I)
- **Mechanism:** Record “keep at least one of these” clauses for interchangeable training supports, and minimize failing joint removals into new clauses before committing simultaneous retirements.
- **Novelty vs nearest prior art:** [Disjunctive protection](disjunctive-protection.md) already supplies the logic. The transfer is testing alternative training support, e.g. [EWC](https://arxiv.org/abs/1612.00796) plus replay, under later updates.
- **Cheapest first test:** Sweep pairs of anchor and rehearsal budgets in a tiny softmax learner; compare independent leave-one-out, bitset clauses and exact subset checks at equal audit cost.
- **Old-task retention check:** Evaluate A/C after each joint release and subsequent updates, with enough novel B progress that freezing cannot pass.

#### 5. Measure negative training readers (I)
- **Mechanism:** Mark an accessed group as replaceable when absence plus a specified reset substitute improves B without violating A/C or other continuation floors. This removes an actual read rather than calling it harmless.
- **Novelty vs nearest prior art:** [Optimizer-history leakage](https://arxiv.org/abs/2610.03940) and [optimizer resets](https://arxiv.org/abs/2306.17833) already motivate forgetting slots. This is a retirement decision, not a new reset method.
- **Cheapest first test:** Change gradient alignment across two rotated tasks and compare keep, selective reset, and norm-matched global reset at equal held-out progress.
- **Old-task retention check:** Check A and C separately immediately and after both aligned and conflicting continuations; a gain on A cannot pay for a loss on C.

#### 6. Map whose future improves when a shared teacher changes (I)
- **Mechanism:** Certify a replacement teacher against each consuming learner's matched refresh, including a context-use control to distinguish training support from general interference.
- **Novelty vs nearest prior art:** [Momentum distillation](https://arxiv.org/abs/2309.02870) and [CGTR](https://arxiv.org/abs/2606.03532) already refresh teachers. The result sought is a per-consumer release matrix, not a new EMA schedule or depletion claim.
- **Cheapest first test:** Give two CPU students different augmentation policies and a teacher whose soft targets can vary at fixed top-1 labels. Compare frozen, EMA, logit-cache and proposed replacements.
- **Old-task retention check:** After irrevocably removing the teacher, score both students on their ordinary A/C tasks and report a separate shift/context probe.

### Train replacements to stop reading a particular group

#### 7. Distill a teacher's effect on the update, not its predictions (P)
- **Mechanism:** Generate a byte-capped substitute optimized for post-refresh trajectories across permitted augmentations and student starting states, then bind several consumers to it instead of the old teacher.
- **Novelty vs nearest prior art:** [MTT](https://arxiv.org/abs/2203.11932) matches trajectories and [LwF](https://arxiv.org/abs/1606.09282) distills logits. The candidate operation is removing a shared producer by satisfying several versioned update contracts with one substitute; if ordinary joint MTT does it, this is an improvement.
- **Cheapest first test:** Two linear students use the same soft teacher but different training losses; compare cached logits, independent and stacked MTT, and a shared certificate-conditioned substitute on held-out starts and augmentations.
- **Old-task retention check:** Run both refreshes after the teacher bytes are overwritten; score A/C over each trajectory at matched B and report any family that still pins the teacher.

#### 8. Give a pending optimizer a new state representation (P)
- **Mechanism:** Fit an adapter from a large shared Adam bank into local sufficient state for a named continuation family; train the continuation's own update rule to consume the new state, with no access to the bank after migration.
- **Novelty vs nearest prior art:** [8-bit optimizers](https://arxiv.org/abs/2110.02861) and [TAG](https://arxiv.org/abs/2105.05155) compress or specialize optimizer histories. The proposed operation is cross-rule migration of a pending read, at equal caps against quantization plus exact graph scheduling.
- **Cheapest first test:** On small rotated quadratics with nonzero moments and differing bias clocks, compare reset, block quantization, a fitted local preconditioner and joint rule/state fitting. Hold out later gradients and disallow clock access through the old bank.
- **Old-task retention check:** Score held-out A/C before and through the new rule's post-reuse descent, not just one-step delta agreement.

#### 9. Replace an anchor with witnesses that keep generating the right constraint (P)
- **Mechanism:** Substitute a few synthetic examples for a shared Fisher/anchor pair by fitting the corrective update they generate over the reachable learner states, not by fitting the old weights.
- **Novelty vs nearest prior art:** [EWC](https://arxiv.org/abs/1612.00796) supplies the quadratic and [gradient-matched condensation](https://arxiv.org/abs/2006.05929) supplies the fitting method. The claim is a checkable migration between training-state types that holds for unseen admissible states; exact quadratic reproduction is a control.
- **Cheapest first test:** Fit witnesses to a rotated quadratic, then extend to a tiny nonlinear classifier where gradients diverge off the fitted region. Compare equally sized low-rank Fisher, raw rehearsal and trajectory condensation.
- **Old-task retention check:** Drop the original Fisher and anchor, visit intermediate states not used in fitting, and score A/C after the new update sequence.

#### 10. Bind a replay sampler to capabilities instead of example IDs (I)
- **Mechanism:** Declare what a future replay job needs (e.g., support on a rare boundary under two augmentation modes). Fit a small replacement buffer and rebind that job, instead of preserving every entry it could sample.
- **Novelty vs nearest prior art:** [DER](https://arxiv.org/abs/2004.07211) and [MTT](https://arxiv.org/abs/2203.11932) already store alternative supports. Improvement only unless a checked contract predicts migrations beyond same-byte replay.
- **Cheapest first test:** Enumerate augmentations in a three-class toy; compare reservoir, class-balanced, gradient-matched and contract-constrained buffers, with replay RNG and old indices inaccessible.
- **Old-task retention check:** Measure A/C overall and on untouched rare examples after destructive reuse and the full scheduled replay window.

#### 11. Train for two separate handovers, not one universal backup (P)
- **Mechanism:** Deliberately construct alternative continuations for the same pending job, each avoiding a different shared group. Publish their separate verified envelopes so the system can switch to the one that clears a later bottleneck.
- **Novelty vs nearest prior art:** Alternatives are already present in [disjunctive protection](disjunctive-protection.md), and [Progressive Nets](https://arxiv.org/abs/1606.04671) add routes. The claim is that learning alternatives targeted at distinct future training reads pays for itself after charging the unused one.
- **Cheapest first test:** Train a CPU refresh with a teacher-only and replay-only alternative; randomly reveal which group later B needs, with policies fit before the reveal. Compare a robust single replacement, both ordinary independently trained alternatives and exact menu selection.
- **Old-task retention check:** After the selected group is overwritten, run A/C refreshes under both held-out bottleneck types and report rejected cases.

#### 12. Make the next continuation independent by choosing today's training data (P)
- **Mechanism:** Buy current examples whose disagreements force the replacement learner to acquire the skill it would otherwise read from an old teacher during its next refresh. Keep the later optimizer and schedule fixed.
- **Novelty vs nearest prior art:** [MTT](https://arxiv.org/abs/2203.11932) and [future edit cost](future-edit-cost.md) already optimize data for later behavior. The candidate is a data choice that removes a typed future read rather than just making a correction cheaper.
- **Cheapest first test:** Fit a tiny spurious-feature classifier with matched example counts and current margins; compare random, gradient-matched and disagreement examples on unseen later task orders and teacher-free refreshes.
- **Old-task retention check:** Remove the teacher and score ordinary A/C before and after the permitted refresh, with holdouts that break the spurious correlation.

#### 13. Teach borrowers a shared substitute across incompatible optimizers (P)
- **Mechanism:** Learn one support object with separate read interfaces for, say, an Adam student and a projected-SGD student, and retire the old group only when both pass their own contract.
- **Novelty vs nearest prior art:** [GPM](https://arxiv.org/abs/2103.09762) and [MTT](https://arxiv.org/abs/2203.11932) already preserve directions and trajectories. The claimed benefit is joint trainability through heterogeneous interfaces relative to a shared replay set plus ordinary per-job projection.
- **Cheapest first test:** Use two small learners with overlapping protected subspaces; compare one shared object, independently compressed state, and stacked shared replay plus GPM at equal total bytes and steps.
- **Old-task retention check:** Run both consumers after overwrite and score A/C for each; one failing borrower invalidates the shared-group receipt.

### Choose by the last reader and the state a later learner can use

#### 14. Rank equal-service programs by what B can actually build (I)
- **Mechanism:** For each replacement calculate which group's last read disappears, then value the group's region against B's declared training effects and deadline, not just its size.
- **Novelty vs nearest prior art:** [PackNet](https://arxiv.org/abs/1711.05769) values freed parameters; generic graph planning over equal candidates already covers the selection rule. The CL result would be evidence that reuse value often differs from local size or accuracy.
- **Cheapest first test:** Exhaustively enumerate the paper case with a larger fragmented group B cannot use; compare smallest support, best accuracy, whole-graph greedy, and exact joint selection with the same disjunctive certificates.
- **Old-task retention check:** Overwrite the selected group with B and run the admitted refreshes; compare ordinary A/C at matched held-out B, not the score of theoretical free bytes.

#### 15. Train the candidate menu around the marginal last reader (P)
- **Mechanism:** Feed the set of almost-released groups to a builder; train a program that avoids the currently pivotal read, then recompute which reader is pivotal after its receipt. The graph guides *generation*, not just sorting.
- **Novelty vs nearest prior art:** [PackNet](https://arxiv.org/abs/1711.05769) and generic joint planning choose sparse supports and schedules. The candidate operation buys different learnable programs with a fixed search budget; a planner given these same programs is an oracle for scheduling, not an unfairly weaker control.
- **Cheapest first test:** With two held-out consumer graphs and a fixed CPU build budget, compare fixed-menu exact planning, graph-greedy generation, tuning for smallest support, and a joint search over the same builder grammar. Include an exhaustive tiny ceiling.
- **Old-task retention check:** Score A/C during staged training and after B overwrites each chosen group, with later refreshes run on unseen data.

#### 16. Build the complement, not the best solo replacement (P)
- **Mechanism:** Train the first borrower to leave only the reads that a second borrower can cheaply drop, even when neither singleton releases anything. Backpropagate a product of soft survival scores as a training heuristic; admit only hard, checked receipts.
- **Novelty vs nearest prior art:** [PackNet](https://arxiv.org/abs/1711.05769) gives support sparsity and joint scheduling already values complements. Beat jointly trained support penalties plus exact retirement under the same compute, not just a myopic ranking.
- **Cheapest first test:** Train two refresh heads sharing two banks with one scratch cell; perturb learner compatibility across held-out worlds rather than forcing a complement in every test.
- **Old-task retention check:** Report A/C after each receipt, before release, and after combined refreshes and B reuse; an impressive singleton does not excuse prefix damage.

#### 17. Buy a new continuation rather than rent a group indefinitely (I)
- **Mechanism:** Compare training-time byte rent from an unavoidable late read against one-time migration, including validation and overlap; choose a bounded move rather than keeping a large bank for a sparse job.
- **Novelty vs nearest prior art:** Checkpoint/recompute tradeoffs such as [sublinear-memory training](https://arxiv.org/abs/1604.06174) are known. This is accounting for cross-job state with retention and hard deadlines.
- **Cheapest first test:** Simulate interleaved CPU refreshes of a linear model with delayed job arrivals; replay the first cap violation using actual training. Compare pinning, precomputing, paging with charged bytes, and migration at fixed B demand.
- **Old-task retention check:** Score A/C after every scheduled refresh, penalizing deadline misses even if eventual recovery is good.

#### 18. Choose migration evidence by its chance of unlocking a build (I)
- **Mechanism:** Allocate audit rollouts to unresolved readers of groups that can enable a viable B build; use the audit to admit or reject a migration, never to count uncertain coverage as a release.
- **Novelty vs nearest prior art:** [Certified CL](https://arxiv.org/abs/2407.06697) covers retention certification and active testing already prioritizes informative cases. Improvement if value-of-information buys earlier useful releases than most-uncertain-first.
- **Cheapest first test:** Use a tiny enumerable backlog with hidden validity for candidate refreshes. Compare random, uncertainty, exhaustive and build-value audit ordering at equal checks and a held-out workload.
- **Old-task retention check:** After each resulting release, run ordinary and rare A/C continuations on independent examples and log false releases and wasted pins.

#### 19. Cut a training-only lifetime cycle with one independent bridge (P)
- **Mechanism:** If retiring a teacher depends on rebuilding a buffer whose builder uses a slot bank, and retiring that bank needs the teacher, train one temporary bridge that breaks a build-time read edge. Remove the bridge after both migrations.
- **Novelty vs nearest prior art:** [MPLS make-before-break](https://www.rfc-editor.org/rfc/rfc3209.html#section-4.6.4) and graph cycle-breaking already describe the schedule; [MTT](https://arxiv.org/abs/2203.11932) gives a way to build a substitute. Claim only a learned bridge that works within a cap where the best conventional bridge cannot.
- **Cheapest first test:** Enumerate a two-job dependency cycle using tiny linear teacher and replay jobs. Compare exact planning over copies, recomputation, compressed substitutes and a learned bridge, all counting temporary memory.
- **Old-task retention check:** Score A/C at both handed-over boundaries, after removing the bridge and while B uses the released region.

### Make the resulting release durable

#### 20. Separate a stale receipt from a failed learner (I)
- **Mechanism:** A receipt declares which continuation inputs and state versions it assumes. Rebase against changed assumptions before admissions reopen; block only the affected continuation.
- **Novelty vs nearest prior art:** [Transactional memory](https://arxiv.org/abs/1502.04908) validates read sets; [certified CL](https://arxiv.org/abs/2407.06697) addresses preservation. Improvement if a behavioral envelope reuses evidence cheaply without silently carrying over an invalid permission.
- **Cheapest first test:** Race a teacher-domain update against a receipt in a CPU classifier; compare exact version invalidation, envelope recheck and full recertification with identical effect maps.
- **Old-task retention check:** Include both race orders and a safely rejected refresh; after permitted reuse, score A/C within deadline rather than allowing a rescue run.

#### 21. Release a representation, keep a bounded way to learn unforeseen jobs (P)
- **Mechanism:** Under an explicit policy for out-of-contract arrivals, choose a replacement that gives up a current training read while leaving a cheap generative or replay seed to build support for new families. That seed is charged and cannot read the retired allocation.
- **Novelty vs nearest prior art:** [Deep Generative Replay](https://arxiv.org/abs/1705.08690) already supplies rebuild data. The candidate is a controllable tradeoff between retiring now and admitting unseen future jobs cheaply, not safety for unspecified training.
- **Cheapest first test:** Rotate small classifiers across a hidden family of future tasks. Compare keep-all where feasible, same-byte raw replay, generative replay plus exact reservations, and a release-aware seed at equal persistent and peak bytes.
- **Old-task retention check:** Separate retention on scheduled A/C refreshes from success and refusal on new jobs; during any admitted new learning, check ordinary A/C without restore.

#### 22. Infer a portable training-read interface across learner updates (P)
- **Mechanism:** Learn a representation of a group's contribution to admissible updates, and bind new consumers through that interface rather than the producer's physical layout. Recheck each new consumer, not just the original two.
- **Novelty vs nearest prior art:** [MTT](https://arxiv.org/abs/2203.11932) and [AdamW input–state–output dynamics](https://arxiv.org/abs/2608.19762) characterize training paths. The new object would be a checked, reusable interface across types of read and learner, not an embedding of an observed trajectory.
- **Cheapest first test:** Fit on two CPU learner variants and hold out a third with a different optimizer or augmentation rule. Compare raw replay, linear response and jointly distilled trajectories plus exact planning, pricing enrollment and certification.
- **Old-task retention check:** Deny the original storage to the new consumer, accept only if it passes its own gate, and check A/C on independent data over the real new continuation.

## Ranked deeper questions

1. **Can training for the last reader unlock learning that retirement plus planning cannot buy?** Compare read-aware candidate generation (cards 15–16) with the strongest stacked control: checked read/write effects, versioned reservations, exact joint planning, and conventional reset, distillation and replay builders at equal search and scratch. Give both the same grammar and test held-out orders. Count a win only when B really spends the released state at matched A/C floors. If both find the same feasible programs at the same cost, the novelty claim fails.
2. **What is the smallest training-read contract that generalizes?** Can a short, versioned update envelope support predictions for permitted but unseen continuations across slots, teachers and Fisher/replay state (cards 2, 7–9, 22)? Use exhaustive floors in tiny worlds and paired probes on withheld streams; track false pins, false releases and coverage separately. If certifying a substitute costs as much as keeping the original or replaying every branch, name the useful regime rather than claiming generality.
3. **When do partial training receipts complement each other rather than merely move the bill?** Price shared substitutes, joint teacher/replay dependencies and transient cycles (cards 4, 13, 16, 19) against independent relocation plus exact planning. Demand irreversibly reusable bytes net of new buffers and overlap, no postponed A/C refresh, and measured B progress.
4. **How much future flexibility should a learner explicitly give up to free capacity now?** Sweep admission horizons, surprise arrival rates and fallback budgets (cards 3, 17, 21). Compare to retaining or recomputing state with the same service obligations and report refused later work separately from old-task forgetting. A policy that wins only by closing admissions has not learned a better migration.

**Verdict:** Future reads and their lifetimes are not new, nor is picking the last-reader cut from a known graph. The candidate CL object is a checked training dependency that a learner can deliberately change while preserving what its admitted successors can learn. Keep that claim only if learning to remove the pivotal dependency beats ordinary retention methods and exact retirement planning on the same budget, after the freed state is actually spent.
