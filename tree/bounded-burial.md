# Bounded burial and universal wake-up words

**Parent:** [Recovery witnesses and sufficient carrier sets](recovery-witnesses.md) ([PR #139](https://github.com/manojbajaj95/cl/pull/139)), extending #19 (bounded burial) and #4 (universal wake-up words). **Triage:** [flood-triage.md, lines 225–226](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L225-L226). **Status:** Ideas only; no experiments run; no GPU.

**Node question:** Can a learner deliberately make old skills unavailable to ordinary inference so that new training can reuse a measurable resource, provided a short, label-free continuation restores the old skills on demand? Can one fixed continuation restore whole families of previously unseen dormant skills without knowing which was requested?

## What would count

- **Dormancy is an intervention, not a low score.** Randomize the choice to release a write constraint or equivalent reservation after learning A and unrelated old task C. Train B on the same stream with fixed model size. An A skill must have passed when learned, fail normal service after release, then pass again after a legal wake. Compare against the same learner with no release and the same release with no wake. Charge parameters, optimizer slots, masks, public batches, recipe bits, search, copies, and write FLOPs. Track reclaimed writable dimensions or freed resident bytes explicitly; a larger B gradient or a falling A score alone is not freed capacity.
- **The bound is a service contract.** Fix a continuation menu, step cap `K`, and separate latency/compute caps before testing. Let `L*` denote the minimum number of legal operations that restore an old skill above its preregistered floor **while keeping B and C above theirs** at a declared cut. Measure both wake latency and the service window once ordinary updates resume. For multiple requests, charge the full request trace (including re-burial, waiting, and any retries); report failures and lower-tail retention, not just the best endpoint. Evaluate at planned cuts and random request times. Failure to find a word means unresolved under the tested menu and budget, not erasure.
- **A word cannot carry the answer.** Fit or select burial policies and words on disjoint development histories. Freeze them, the public batches, and all selection rules before opening held-out obligations. At wake time use no old labels, rewards, graded feedback, task ID, or old examples for universal claims. A state-dependent public update may produce different weight changes, but it is the same instruction sequence and public inputs on every recipient. An adaptive selector is a separate baseline, not a universal word. Audit labels score results offline; they never pick a word, a stopping time, or a release decision on that run.
- **Universality has two axes.** Test the same frozen word on different histories with opposite old labels on identical queries, and on hosts that each hold several jointly serviceable old skills. In the latter case they must all pass after **one** invocation, not one fork per skill. Reserve whole rule generators and B drift schedules for test, not just new examples. Report family coverage and worst-skill margins, including the misses; a shared output shift that helps only one side is not recall. Include an A-naive host with matched initialization and B exposure, plus a never-buried host and a matched naturally forgotten host. Match pre-wake margins among failure arms where feasible; report mismatches.

### CPU assay and equal-budget controls

Start with a linear negative control and a width-64 MLP. Generate balanced private rules `A_i^− / A_i^+` with independent random label polarities on identical public queries; use disjoint query regions when multiple skills must answer simultaneously. Learn A and C before B. Use both ordinary overlapping-feature streams and designer shifts that calibrate individual mechanisms; success only on a built-in switch is a positive control, not evidence for natural allocation. Freeze policies on separate seeds, generators and schedules. Compare paired differences across fresh seeds, including re-burial and peak wake overhead. To claim a genuinely sequential wake, also defeat matched one-operation and frozen linearized/first-update controls; do not count a fused cheap reset as two-step depth by definition.

- **Allocation controls:** tune EWC, replay/DER++, and PackNet or routed adapters at the same total budget. Include equal-byte saved deltas, unconstrained B, and a relaxed-retention baseline that can also use the wake budget. Compare B at matched post-wake A/C floors **and** A/C at matched B. Measure the full frontier, not a single penalty coefficient.
- **Wake controls:** no-op, plain continued B, fixed irrelevant public steps, common-shift removal, optimizer reset, entropy/prior calibration, and an oracle per-skill word as a non-deployable upper benchmark. Include equal-update random and reversed recipes as appropriate. Charge public samples and updates to all arms. Report accuracy and paired signed margins on fresh A queries before wake, after wake, and after resuming B. C is scored throughout, B again **after** the wake. These checks apply to every card below; each card names the extra retention check its mechanism could fail.
- **Ledger screen:** [idea ledger (PR #6)](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). No exact restore disguised as learning, no fitted per-task delta disguised as a word ([L1 verdict, PR #42](https://github.com/manojbajaj95/cl/pull/42)), no scalar plasticity-reserve forecast, and no repeat of re-annealing after plain overwrite. Triage L225 treats carrier-compaction and witness search as parent work; L226's hysteresis and per-branch return ticket are comparators, not proposals here. Cards are primitive candidates (a reusable operation or test object) or improvements (must deliver a substantial equal-budget gain); novelty comparisons are scoped, not claims of exhaustive priority.

## Idea cards

### A. What can a dormant learner actually give back?

#### 1. Rent the constraint, not the parameter (primitive)

- **Mechanism:** The same parameter block can host both skills, but B temporarily rents the *right to write along directions* previously reserved for live A. Admit a larger write radius only where a frozen word still restores A and preserves the B increment.
- **Nearest art / delta:** [EWC](https://arxiv.org/abs/1612.00796) penalizes important directions to preserve service. Here the unit of rental is write access conditioned on recoverable, rather than immediate, service.
- **Cheapest first test:** In the MLP, sweep the rank of released constraints at fixed gradient norm and budget; compare against randomly released directions, tuned soft EWC, and relaxed EWC plus the same word. Reject if B's post-wake gain does not depend on which constraints were released.
- **Old-task retention check:** Compare the hardest paired A cases at matched final B and after 50 more B steps; require C to pass while the rental is active.

#### 2. Lease just the update interaction (primitive)

- **Mechanism:** Protect two individually benign B write directions but permit their interaction to obscure A. Wake with a public continuation that removes the obscuring interaction while keeping both B contributions.
- **Nearest art / delta:** [Riemannian Walk](https://arxiv.org/abs/1801.10112) scores parameter paths for preservation; this allocates a write *pair* based on a non-additive service/wake effect. Not an additive importance ranking.
- **Cheapest first test:** At matched losses, test no release, each directional release alone, and both, with crossed signs and sum-of-singleton predictions. Reject if the factorial interaction vanishes against an equal-norm single write.
- **Old-task retention check:** After the same wake on all four arms, score A and C and both B subskills separately; keeping average B by sacrificing one does not count.

#### 3. Borrow intermediate compute width (improvement)

- **Mechanism:** Let B temporarily train through a shared intermediate block previously needed to serve A; lower A's active compute allocation but let a label-free word restore usable A propagation through the changed block, without changing the serving width.
- **Nearest art / delta:** [Switch Transformers](https://arxiv.org/abs/2101.03961) route among resident experts; [PackNet](https://arxiv.org/abs/1711.05769) freezes old masks. The bet is that B can train the same freed channels and the wake works without selecting an old mask or loading an expert.
- **Cheapest first test:** Give two MLPs the same active and resident widths; compare shared-channel release to routed masks and ungated B with the same wake. Require a lower active-width budget at equal quality, including wake operations.
- **Old-task retention check:** Score rare A inputs dependent on the borrowed channels and C immediately after each of two wake/reuse cycles.

#### 4. Give B the short-term state, not the old answer (improvement)

- **Mechanism:** Reallocate momentum capacity to B while retaining whatever old distinctions survive in the shared weights. Wake with public gradients that rebuild a usable joint weight–slot configuration, rather than copying the old momentum.
- **Nearest art / delta:** PR #139 studies weight–slot carriers. [LoRA](https://arxiv.org/abs/2106.09685) saves training state by reducing trainable parameters; this asks whether reassigning fixed slot bytes buys B progress even when model width is unchanged.
- **Cheapest first test:** Limit active slot bytes in an Adam MLP; cross slot reallocation vs. uniform low-precision slots with public rebuild vs. ordinary reset. Reject if reset at the same memory and steps ties.
- **Old-task retention check:** Check A and C at wake and after a matched B restart; score B both before the restart and after the A wake.

#### 5. Re-teach the writer, not the old task (primitive)

- **Mechanism:** During acquisition, constrain *how* an A update writes into shared state so later B gradients can mute service without destroying the A distinction. Use a development-trained write rule, not per-skill residuals.
- **Nearest art / delta:** [Spurious forgetting](https://arxiv.org/abs/2501.13453) recovers from alignment disruption after the fact. This trains the acquisition writer for recoverable reuse on tasks not seen during writer design.
- **Cheapest first test:** On synthetic rule generators, compare two-step meta-training of a shared writer against matched ordinary acquisition plus recovery training and generic augmentation. Hold out both A rule generators and B shifts. Require gains outside architecturally planted gates.
- **Old-task retention check:** Match initial A/C performance and check A per polarity after wake, C during B, and A again after a second unseen B release.

#### 6. Buy burst capacity with a predeclared request budget (improvement)

- **Mechanism:** Permit release for B training bursts only when an external latency budget can absorb the wake, with a limit on how long requests remain unserved. Use one frozen word and a public request clock, not estimated A accuracy.
- **Nearest art / delta:** [DER++](https://arxiv.org/abs/2004.07211) trades replay against online plasticity. This trades *service interruptions* for otherwise unavailable B burst throughput, not replay spending.
- **Cheapest first test:** Replay fixed clustered and adversarially interleaved request traces against tuned periodic replay, per-skill adapters and always-live training. Require more post-wake B progress per wall-clock proxy at equal tail latency; count instantaneous switching if the baseline supports it.
- **Old-task retention check:** Count missed A/C requests as failures, even if both tasks are accurate at the final cut.

#### 7. Retain the counterfactual write option (primitive)

- **Mechanism:** Where B can take several same-loss writes, keep only a public scalar controlling how much of a *future* B update can reverse an occluding access direction while retaining the B function. Store no reverse delta or old checkpoint.
- **Nearest art / delta:** [EWC](https://arxiv.org/abs/1612.00796) restricts current writes to preserve old performance; the proposed allocation reserves a control degree of freedom for future public gradients, not a protected old parameter subspace.
- **Cheapest first test:** Construct two same-B-loss update directions in a two-layer host and reverse which has the public option after a new input rotation. Compare this policy with random choices, direct B-loss tie-breaking, and equal-byte low-rank deltas. Reject if the reserve only predicts success and does not causally affect it.
- **Old-task retention check:** Audit the A/C floors under the same future B batches on both branches, including a second wake when the option should still be available.

### B. Can one word wake many different things?

#### 8. Synchronize access, preserve payload (primitive)

- **Mechanism:** Search for a word that contracts dispersion of access states across histories while *preserving* private payload contrasts. Select on public proxy dynamics only after development; the word must align access without synchronizing the answers.
- **Nearest art / delta:** [Common-shift repair](https://arxiv.org/abs/2610.08718) removes a shared direction. Here the bet is that different local shifts admit the same operation sequence without sharing a single corrective direction.
- **Cheapest first test:** Use three independent B rotations and held-out A rules; compare fixed two-step words with rank-matched shift removal, momentum reset and their stack. Require an advantage without a planted common intercept.
- **Old-task retention check:** Wake four independently polarized skills together; score minimum fresh A accuracy, C and final B on every host.

#### 9. Ordered universal words with the same ingredients (primitive)

- **Mechanism:** Exploit public updates `U,V` whose ordered effects on access do not commute. Train burial policies whose wake is `UV` even when the hidden skills and drift paths differ.
- **Nearest art / delta:** PR #139 has two-step witness search; [NTK](https://arxiv.org/abs/1806.07572) motivates a frozen linearized control. The added claim is to *shape multiple burial processes* so one order generalizes, not just discover a noncommuting witness for a single pair.
- **Cheapest first test:** On held-out task families, compare `UV`, `VU`, shuffled repeats, a matched single combined update and unconstrained B with the same ingredients. Reject if order gains disappear outside the analytic positive control.
- **Old-task retention check:** Require the same winning order to hold A/C above floor without temporary B downtime beyond the wake budget.

#### 10. One word after a change of basis (primitive)

- **Mechanism:** Express public wake operations in a local coordinate frame constructed from B covariance; use one coordinate-invariant program across recipients rather than a fitted correction vector in shared parameter coordinates.
- **Nearest art / delta:** [RoSE](https://arxiv.org/abs/2503.16793) adapts semantic representations at test time. This applies an identical program to public B data without old test examples and tests transfer where raw-space corrections disagree.
- **Cheapest first test:** Hold out rotations of hidden-layer features and then test natural drift; compare public whitening alone, common-shift removal in the same frame, and a fixed raw-space word. Count covariance estimation and reject on ties.
- **Old-task retention check:** Score each A polarity under the novel frames, and C and B under both the original and changed input distributions.

#### 11. An idempotent wake boundary (primitive)

- **Mechanism:** Choose public update dynamics whose target is an awake manifold: one word enters it, applying that same word again moves little along task-relevant outputs. This is an attractor for access, not for payload.
- **Nearest art / delta:** [ARC](https://arxiv.org/abs/2405.14318) adapts a classifier using self-labeled examples when needed. Here repeat-safe repair must generalize without old inputs or feedback indicating which skills are already awake.
- **Cheapest first test:** Mix live, partly dormant and dormant hosts. Reapply one fixed word up to five times, comparing against fixed-step repair, public normalization and an adaptive early-stop baseline at the same max cost.
- **Old-task retention check:** Require no A/C regression on already-awake hosts and sustained joint A/B/C scores on formerly dormant ones, not merely imperceptible parameter changes.

#### 12. Missing-step tolerance without a fresh search (improvement)

- **Mechanism:** Compile two overlapping public update subsequences into a short fixed word so a dropped batch or unavailable operation does not strand a subset of dormant skills.
- **Nearest art / delta:** [Benign relearning](https://arxiv.org/abs/2602.03379) shows recovery can depend on public data structure. Here the engineering target is worst-case one-step dropout at fixed length, rather than average recovery on helpful inputs.
- **Cheapest first test:** Delete each instruction of a four-step word in turn on held-out hosts; compare to repeated best fixed step and random repetition at equal latency. Require a substantial increase in worst-deletion coverage.
- **Old-task retention check:** Check polarity-matched A coverage, C and B after every deletion, including deletion of the first and last steps.

#### 13. Standardize the burial side of the interface (primitive)

- **Mechanism:** During B learning, constrain access-altering writes to share a protocol while leaving private A contents unconstrained. Optimize B under this narrow write interface so independent learners can use the same fixed wake word later.
- **Nearest art / delta:** [L2P](https://arxiv.org/abs/2112.08654) selects stored prompts per input; this standardizes how a host becomes dormant, with no per-skill read-time routing or prompt pool.
- **Cheapest first test:** Use independent B trainers with different optimizers; cross common interface vs. no interface with fixed word vs. per-trainer words. Use a single shared shift-removal direction as a strong protocol baseline. Require out-of-trainer generalization at matched B progress.
- **Old-task retention check:** Hold out joint A families as well as trainers; reject if the protocol helps the common old skills by making unusual ones unrecoverable.

#### 14. Wake on a shared gradient carrier, not a shared gradient (primitive)

- **Mechanism:** Use a fixed unlabeled batch schedule whose gradient passes through a shared *pathway*, yet lets its update vectors diverge across hosts in ways determined by their own state.
- **Nearest art / delta:** [Benign relearning from syntax](https://arxiv.org/abs/2602.03379) finds helpful public data structure; the added causal claim is that the family shares a gradient pathway, not a task-like batch or an update direction.
- **Cheapest first test:** Cross public batch swaps with masked public backpropagation through candidate and size-matched random pathways; compare fixed shift repair and the same batches through full backprop. Freeze masks on development and reject if pathway ablation has no selective effect.
- **Old-task retention check:** Verify the intact pathway revives opposite A rules on different hosts while keeping C and B, and gives no matching polarity effect on A-naive hosts.

#### 15. A fail-closed universal envelope (improvement)

- **Mechanism:** Define a public validity envelope for one word (for example, a range of measured B gradient geometry); outside it, do not deliberately bury a new obligation instead of guessing another wake. The gate consumes no A feedback at deployment.
- **Nearest art / delta:** [Real-time spurious-forgetting detection](https://arxiv.org/abs/2512.20634) diagnoses alignment depth. This prices refusal to release capacity using measured joint post-wake coverage on previously unseen drift.
- **Cheapest first test:** Freeze a gate on development curricula; test on drift mixtures where norm-matched hosts differ in coverage. Compare against constant conservative burial, a norm threshold and always-wake at matched release coverage.
- **Old-task retention check:** Count false admits as request failures on A/C; report foregone B gains on safe rejects and separate refusal from successful service.

### C. What breaks, and can that limit guide the mechanism?

#### 16. Certify a lower bound on shared-word length (primitive; audit)

- **Mechanism:** Represent each audit recipient's acceptable terminal states in a finite quantized surrogate, search their product transition graph, and find the shortest word acceptable to *all*. Contrasting shortest per-recipient lengths with the product minimum exposes an actual price of sharing.
- **Nearest art / delta:** [Universal perturbations](https://arxiv.org/abs/1610.08401) look for a single input-space perturbation that fools many inputs. This is a product constraint over training-state transitions with selective restoration, not all recipients driven to the same output.
- **Cheapest first test:** Enumerate a tiny three-operation graph on two-slot quantized learners, then test whether the surrogate predicts conflict in a tiny MLP. Reject surrogate claims if its edge predictions fail; exact lower bounds apply only to the enumerated model.
- **Old-task retention check:** Encode A/C/B floors in the acceptable sets; count no word as feasible if it revives A in exchange for B or C.

#### 17. Balance per-host needs against one-shot co-revival (primitive; audit)

- **Mechanism:** Construct an audit matrix with rows as histories and columns as skills on each history. Compare per-host and per-skill success margins with the joint minimum, then transplant only a candidate shared access component to test whether the two axes share a cause.
- **Nearest art / delta:** [Common-shift repair](https://arxiv.org/abs/2610.08718) addresses common disruption; PR #139's multiplexing uses different words per skill. This separates broad cross-host transfer from simultaneous within-host service and directly tests which one fails at a shared access component.
- **Cheapest first test:** Evaluate four histories with four co-resident skills, holding the total exposure budget fixed. Cross donor access component vs. random matched component and fixed word vs. no wake. Reject a shared mechanism if transplantation predicts only one axis.
- **Old-task retention check:** A recipient passes only if all four A skills, C and B pass on the same post-wake copy.

#### 18. Preserve private bits under repeated public wakes (primitive; audit)

- **Mechanism:** Train histories that differ on independent private bits. Quantize the entire allowed continuation state and look for collisions across histories, before burial, after burial, and after repeated wakes. A collision of complete states with identical public side information proves that no shared word can recover those different bits on both histories.
- **Nearest art / delta:** [Syntax-driven benign relearning](https://arxiv.org/abs/2602.03379) shows why a recovery claim must rule out structure in public data; PR #139 distinguishes service loss and exact loss. Here collisions constrain a *cycling capacity budget* and can localize whether the release, the wake, or repeated reuse destroys distinctions.
- **Cheapest first test:** Enumerate four to eight bits in a quantized toy and compare collision losses against matched-bit resident deltas and a no-wake sequence at equal update cost. In the MLP treat only observed collisions in complete state as proofs; failed probes are not proofs.
- **Old-task retention check:** Decode each private A bit after every cycle on fresh queries and check C/B floors; averages can hide a systematically lost bit.

#### 19. Trade off words by their service footprints (primitive; audit)

- **Mechanism:** Treat each word as a vector of changes to awake A, dormant A, C, and B on the *same* host. Compare attainable footprints under one word versus servicing independently on destructive forks; use incompatibility to decide whether to abandon single-word deployment for that family.
- **Nearest art / delta:** [Riemannian Walk](https://arxiv.org/abs/1801.10112) measures retention along learning paths; PR #139's multiplexing assumes separate words. This exposes incompatibility of good individual endpoints, not just bad mean accuracy or search failure.
- **Cheapest first test:** Exhaustively enumerate length-0–3 words on a small menu and compare the best single frontier with a budget-matched fork baseline including copy cost. Change B's feature overlap to test whether the incompatibility moves predictably.
- **Old-task retention check:** Score the entire old portfolio after each command; mark fork-only recovery as **not** same-host revival.

#### 20. Request-order stress as a capacity check (improvement)

- **Mechanism:** Allocate write access using the worst short request schedule in development, not the average number of wakes. Optimize over matched bursts and alternations so recurrent wake/re-bury costs enter admission decisions.
- **Nearest art / delta:** [DER++](https://arxiv.org/abs/2004.07211) protects online retention through replay. This improvement targets net writable capacity under service scheduling, not offline endpoint retention or learning a repair order (triage L226).
- **Cheapest first test:** Use traces with identical A/B/C request counts but different ordering and burstiness. Compare at equal bytes, updates and time to mean-rate admission and an always-live controller. Require real B gain at the same worst-trace service floor.
- **Old-task retention check:** Report the worst prefix and the cumulative failures for rare A skills and C; test a held-out ordering after tuning.

#### 21. Recover the gain, not just the old skill (primitive; audit)

- **Mechanism:** At a common cut, compare the causal B benefit of release with and without a wake. A positive release-by-wake interaction on joint service distinguishes genuine reusable capacity from B merely borrowing progress that the wake returns.
- **Nearest art / delta:** [Spurious forgetting](https://arxiv.org/abs/2501.13453) measures recovery; [PackNet](https://arxiv.org/abs/1711.05769) measures allocation. This factorial comparison requires both effects in the *same* post-wake model at fixed resident size.
- **Cheapest first test:** Cross release/no release with wake/no wake and include equal-budget B-only and relaxed-retention controls. Use a same-cost sham wake; require post-wake B gain over non-release/wake at matched retention, not a cruder pre-wake gain or an interaction driven solely by damaging a control.
- **Old-task retention check:** Take fresh A and C measurements in all four arms at the identical service times, plus a full further B window in the winning arm.

## Ranked deeper questions

1. **Does deliberate dormancy buy usable B capacity after paying to wake A?** Start with #21 and #1: at fixed size, bytes and time, randomized release must buy a B gain that remains *after* wake, while A and C meet the service contract. If tuned relaxed retention plus a cheap fixed wake or saved deltas ties, there is no demonstrated capacity primitive.
2. **Is there one frozen word for whole unseen families, including several skills on one host?** Start with #8 and #17, holding out both private rules and drift schedules. If the paired and naive controls pass but common-shift repair ties, call it shared alignment repair, not a new universal mechanism.
3. **Can we design the burial interface without building the answer into the assay?** Compare #5 and #13 against their stacked acquisition and repair baselines on ordinary training paths. Require causal generalization beyond a simulator gate whose inverse is known.
4. **Which bound fails first as scale or request pressure increases?** Use #16, #18 and #20 to separate word-length incompatibility, actual loss of private distinctions, and unaffordable request latency. A finite-menu miss is not evidence for state erasure; a two-step recovery on its own is not evidence for a workable lifecycle.
