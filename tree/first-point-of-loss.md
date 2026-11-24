# First point of loss: find the write that makes an old distinction unrecoverable

**Parent:** [Information-dumping map](information-dumping-map.md) ([PR #133](https://github.com/manojbajaj95/cl/pull/133)), especially card 3. **Status:** ideas only; no probe run. The parent asks where old-task information goes. This node asks whether an exact **step and operation** can be located, what kind of loss can be claimed there, and what a continual learner can do with that address that it could not do with a bad final accuracy score.

## What would count as a first point?

1. **Define a distinction that matters.** Train paired variants `A−` and `A+` from coupled initializations, varying only an old obligation, e.g. how to break a routing tie. Fix a held-out set of old queries and a target contrast (the direction and size of the difference required by the two obligations). Verify at launch that both models serve their own variant on fresh inputs. Randomize the variant assignment across independent worlds; balance launch performance and margins, sample order and optimization effort. Train both variants on the **same materialized B batches**, with the same RNG draws and schedule; B inputs, labels and public metadata must not reveal the A variant. A/B compatibility is within each run, not between the two mutually exclusive A obligations. Include an unrelated old task C and a joint-fit ceiling for each variant; do not pass a task ID at inference. Use deliberately conflicting A/B pairs only as diagnostic stress tests.
2. **Give each operation a real boundary.** In a deterministic CPU reference loop record `(global step, operation, before/after)`: e.g. gradient formation, clipping, slot damping and accumulation, preconditioning, cast, parameter commit, buffer reset. At each boundary enumerate weights, slots, active temporaries, RNG/counters and auxiliary data that remain available to the declared reader or future program. Include a gradient or accumulator while live; do not count a saved preimage unless the method pays to keep it. If both source and destination are still live, a lossy cast alone need not erase anything: the collision may be at the source's retirement. Separate loss in the current forward path, loss in a restricted observation (such as weights only), and loss in the complete state. Verify that instrumenting the loop does not change its endpoint. For fused operations with no meaningful intermediate state, report the fused boundary, not a fictitious internal instruction.
3. **Use fixed readers, not a new fit at every cut.** Preregister a reader bank, observations, precision/noise, query budget and tolerances. Train any readout on disjoint development trajectories pooled across cuts, then freeze its feature packing and weights; keep availability masks and cut metadata identical between pair members. Read the live A logits wherever a committed model is defined, plus bounded state and state-with-public-B readers. Use the same public query bank at every cut; do not give the reader pair IDs, A labels, the other model, or logs not included in its observation budget. Predict the obligation or reconstruct its old query targets, not the seed or the arbitrary identity of a run. Check raw same-input logits, complete first gradients, and single-step responses as shortcuts to any claimed extra optimizer or multi-step channel ([PR #114](https://github.com/manojbajaj95/cl/pull/114), [PR #123](https://github.com/manojbajaj95/cl/pull/123)). Report state-separation and observation precision separately; a larger frozen reader can invalidate a smaller reader's loss claim.
4. **Distinguish three outcomes.** *Service loss:* fresh A queries fail in normal use. *Budgeted loss:* the frozen bank goes from passing to failing its preregistered recovery tolerance on the named observation; quantify uncertainty and require equivalence to a no-signal control for a chance-level claim, not merely a nonsignificant difference. Name both sides of the bracket and report recrossings and the first failure that persists through a declared horizon separately. *Exact loss:* distinct legal A histories requiring different answers have identical complete continuation state after an operation, and shared public side information. Under the same target-blind continuation they cannot subsequently be distinguished ([PR #110](https://github.com/manojbajaj95/cl/pull/110)); this is pair-specific, not a universal impossibility theorem. Finding a terminal exact merger licenses binary search for the first equality at step boundaries under deterministic shared continuation, then a within-step scan; a frozen reader can recover after apparent failure, so its first crossing requires a scan. If there is no resolved crossing or no exact witness, say so. An injective update may cause service failure and finite-precision read failure without erasure.
5. **Make the address earn its keep.** In a tiny enumerated finite-state host, plant a cast/release merger, a weight-only loss with a live slot trace, and an injective contraction to calibrate the three outcomes. Then use real A-variant training in a tiny feature-learning MLP, with a linear/frozen-feature host as a control. Starting at the same legal prefix, replace just the candidate operation with a permitted alternative; recompute all dependent downstream operations, reuse the same B data and RNG, and compare with equally disruptive adjacent-step and wrong-operation shams. Test dose/precision matching and report both immediate rescue and later retention: an edit that merely moves the failure to the next write is not a remedy. Treat a known loss address or A evidence unavailable at deployment as oracle input; compare oracle headroom first, then freeze a prospective rule on unseen streams without borrowing future B or test labels. Compare against a whole-step intervention with the same information and cost. Localisation is valuable only if the operation-specific choice changes the retention–acquisition frontier.

## Ledger, prior art and common scoring

The [idea ledger](https://github.com/manojbajaj95/cl/blob/825a000f7f3fae56c0b1becee50865da75980cb1/reviews/idea-ledger.md) rules out scalar erasure budgets, Noether memory without finite-step survival, static Gramian forecasts without headroom, sparse repair by assumption, and wins by exact restore. Match per-item margins before claiming a loss order. [Replay deadlines](https://github.com/manojbajaj95/cl/pull/113) found weak timing value for target-blind replay in its continuous host; stored-target replay is not subject to that deadline, and pre-shock escrow is an existing control. [Practice-order interference](https://github.com/manojbajaj95/cl/pull/121) separates transient excursions from state that persists after re-mixing; measure both rather than declaring an irreversible event from a transient.

Prior-art anchors, not a priority claim: [reversible learning](https://arxiv.org/abs/1502.03492) already keeps a remainder tape; [NTK overlap](https://arxiv.org/abs/2010.04003) explains linearized interference; [EWC](https://arxiv.org/abs/1612.00796) and [OGD](https://arxiv.org/abs/1910.07104) already protect parameter directions; [MIR](https://arxiv.org/abs/1908.04742) retrieves examples predicted to be interfered with; [DER](https://arxiv.org/abs/2004.07211) already replays stored logits; [error feedback](https://arxiv.org/abs/1901.09847) tracks residuals of compressed updates; [GradVac](https://arxiv.org/abs/2010.05874) adjusts gradient similarity; [benign relearning](https://arxiv.org/abs/2406.13356) separates apparent forgetting from recovery. The novelty bets below are the specific objects or operations enabled by a causal address, not these ingredients in isolation.

Every proposed first test is CPU-scale. In addition to each card's named retention slice, score fresh **live** A−/A+ and C loss/accuracy from launch through B, at equal update counts and matched held-out B progress (count misses); include worst-task and lowest transient scores, then continue shared B or re-mix to check delayed failure. Score repaired models in normal forward service with no oracle at inference and report reconstruction separately. Charge retained bytes (including metadata), extra probes, inference and training work. Tune controls equally; compare paired uncertainty across independently generated worlds, and replicate an unexpected effect on at least ten seeds before explaining it. **P** marks a primitive candidate (a new reusable object or operation); **I** marks an improvement to an existing method.

## Ideas

### A. Give an operation an actionable loss address

#### 1. Release-aware carrier liveness map (P)

- **Mechanism:** Trace which currently live values suffice to recover a particular A contrast, and put a lease on the last readable alias until a replacement has been verified. Leases attach to value lifetimes, not layers.
- **Novelty rationale:** The parent's substitution matrix tests snapshots; this makes last-copy retirement an actionable event even when the lossy write itself was harmless. It is not keeping all old optimizer inputs for reversal.
- **Cheapest first test:** In a toy optimizer, retain a full-precision accumulator for staggered lifetimes around its cast; vary whether the rounded model or another slot still carries the contrast. Compare leases with cast-triggered copy and whole-step checkpoint at equal peak bytes and byte-steps.
- **Old-task retention check:** Carry the lease through the next write that can consume it; score live A near rounding ties and C away from ties after all leases have been freed.

#### 2. Loss-address instruction minimizer (P)

- **Mechanism:** Reduce an observed failing prefix to a legal reproducer by deleting or substituting B operations and recomputing dependencies. Export the smallest reproducer found *with* the preconditions under which the same operation causes loss.
- **Novelty rationale:** Stepwise ablation is the parent's diagnostic; a reusable counterexample plus precondition can test a new optimizer before full training. It need not identify a globally minimal subsequence.
- **Cheapest first test:** Enumerate short streams in a two-slot optimizer with occasional reset; evaluate whether reduced reproducers predict intervention gains on new prefixes better than the entire original prefix or a one-step loss ranking at equal audit cost.
- **Old-task retention check:** Patch only the reproduced precondition, then check ordinary A/C service on full streams, including examples never used in reduction.

#### 3. Competition between sufficient carrier sets (P)

- **Mechanism:** On tractable states find multiple minimal sets of jointly readable values, e.g. `{weight, centered slot}` or `{reference, residual}`; forbid a planned operation from removing the last complete set rather than protecting every individual value.
- **Novelty rationale:** Goes beyond pairwise carrier substitution and parity across exits: the unit of protection is a replaceable set with complementarity, not a marginal read score or a new code presuming independent failures.
- **Cheapest first test:** Enumerate tiny tables with both redundant and complementary carriers, then model correlated reset schedules. Compare exact subset sets against per-value salience and equal-byte replication; reject if the marginal policy ties on a nondegenerate schedule.
- **Old-task retention check:** After pruning, evaluate both the A contrast that requires joint carriers and other A/C capabilities that use just one of the values.

#### 4. Precision-by-budget loss surface (P)

- **Mechanism:** Map the first-loss address over a preregistered grid of arithmetic precision and fixed read budgets. Spend extra bits only where higher precision moves the loss surface and where a high-budget reader alone cannot do so.
- **Novelty rationale:** Separates actual precision allocation from changing decoders or optimizing the number of discarded bits. The actionable target is a shift in the loss address that carries through to service.
- **Cheapest first test:** Pair fixed-point and high-precision contraction with a true reset; compare address-guided mixed precision to magnitude/error-based mixed precision and stronger readouts under the same bytes and operations.
- **Old-task retention check:** Remove any diagnostic reader and score live low-margin and margin-matched high-margin A slices plus C during and after B.

#### 5. Recovery-path witness (P)

- **Mechanism:** After a fixed reader fails, search a bounded menu of **target-blind** legal operations for a common continuation that makes the original read pass again. Use the witness to choose an operation that brings a surviving contrast back into service, or return unresolved.
- **Novelty rationale:** Unlike replay deadlines or a signed differential register, a witness disproves exact loss at an earlier cut and identifies an executable common suffix, not a probe difference or a new decoder trained on A labels.
- **Cheapest first test:** Enumerate one- and two-operation suffixes in a small slot/weight host, including an exact-collision negative. Compare capacity-matched passive readers, raw one-step shortcuts and equal-budget stored-label replay for the repair claim.
- **Old-task retention check:** Deploy the same suffix to both runs and score ordinary A on unseen queries after returning to shared B; reject if restoring the contrast trades away C.

### B. Change the operation, not the whole learning rule

#### 6. Operation-contract compiler (P)

- **Mechanism:** Attach an A-observation tolerance to a typed optimizer edge; synthesize a local replacement that satisfies it while keeping the other consumers' interface unchanged. Different contracts can compile to retaining a slot, changing the rounding basis, or splitting a reduction.
- **Novelty rationale:** OGD constrains final updates; a compiled contract can change internal semantics even when the acceptable instantaneous weight step is unchanged. It is not perpetual activation pinning.
- **Cheapest first test:** Enumerate a finite menu of substitutions for a cast followed by slot reuse in a tiny MLP. Compare compilation to the best equally informed one-operation heuristic and whole-step projection, including search cost; test transfer to held-out B batches.
- **Old-task retention check:** After the compiled branch and after the next slot consumer, measure live A and C, including tasks with no contract attached.

#### 7. Consumer-before-release rescheduling (P)

- **Mechanism:** Move an existing consuming operation before its last high-precision input dies, carrying only the smaller result that consumer needs. The original low-precision path still serves B.
- **Novelty rationale:** This is a local dependency-schedule change, not reordering B practice or adding a residue tape; a gain requires useful information in the early consumer output and not just postponing a reset.
- **Cheapest first test:** Compare early and late application of the same slot read/update in a cast-heavy optimizer. Use a commuting case as a negative control and compare with late read plus equal-byte error feedback.
- **Old-task retention check:** Score A on inputs needing the affected slot and C after the next optimizer phase, when the full-precision input is no longer available in any arm.

#### 8. Branch-local normalization (P)

- **Mechanism:** When a global denominator first masks an old direction, split the optimizer consumer into a shared B-normalized branch and a small old-sensitive branch with a separately bounded scale, then reunite their weight proposals.
- **Novelty rationale:** Ordinary clipping and GradVac change how gradients combine; this tests whether changing **which consumer sees a denominator** beats a better global threshold or arbitrary group clipping. No invariant or unconditional retention guarantee is claimed.
- **Cheapest first test:** In a tiny MLP, alternate batches with matched norms but different scale couplings. Compare implicated-branch normalization, per-layer clipping, norm-matched gradient surgery, and a randomly chosen split.
- **Old-task retention check:** Test A on both high- and low-activation queries, and C in a branch that shares the denominator but was not protected.

#### 9. Null-consumer lift (P)

- **Mechanism:** If a write has several extended outputs with the same B-visible value, choose the representative that preserves the A contrast for a later legal consumer. The lift is useful only if subsequent training does not collapse all the representatives anyway.
- **Novelty rationale:** The parent moves where dissipation falls; this chooses among legal section maps of the same lossy interface. It must beat a state-matched side register or ordinary error feedback, not invoke gauge conservation.
- **Cheapest first test:** Enumerate legal slot encodings behind a small fixed-point optimizer interface; vary the later consumer so success is not guaranteed by an inert reserved bit. Compare alternative lifts at equal state size and identical immediate B output.
- **Old-task retention check:** Score A after the downstream consumer, after further B writes, and on C using the same optimizer interface.

#### 10. Local inverse islands (P)

- **Mechanism:** Replace a short cluster of irreversible operations with an augmented invertible block, then discharge its auxiliary state as soon as a legal downstream write has made the A obligation live again.
- **Novelty rationale:** Reversible training saves a global tape for reversal; here the invertible region is a temporary execution policy with a live-service exit criterion. No score is awarded for exact rewind by construction.
- **Cheapest first test:** Place islands at the measured boundary or at neighboring same-size clusters in a tiny optimizer with two lossy phases. Compare with an equal-byte checkpoint/recompute arm and a direct slot-precision increase.
- **Old-task retention check:** After discarding all augmentation, score fresh A and C during intervening B and at the deployed endpoint, not at a reconstructed A checkpoint.

#### 11. Conflict-at-commit arbitration (I)

- **Mechanism:** When two individually safe proposals jointly lose A at an aggregation commit, limit or alternate only the common component implicated by the commit intervention. Leave disjoint components and earlier gradient computation alone.
- **Novelty rationale:** An improvement to gradient surgery, not a new projection principle. Unlike a whole-step cosine gate, activation requires evidence of a causal joint failure at a particular consumer.
- **Cheapest first test:** Construct two proposal pairs with equal cosine and norm but different old-query effects through a nonlinear merge. Compare the best whole-step projection, microbatch clipping, and the operation-triggered variant at equal A-evidence and compute.
- **Old-task retention check:** Check A examples both inside and outside the implicated component and verify that C does not absorb the displaced interference.

### C. Handoff and recovery without restoring an old model

#### 12. Verified carrier handoff (P)

- **Mechanism:** Before a destructive write, copy only the still-needed distinction to a different pathway; release the source only after a fixed reader and a held-out development rollout pass on the destination alone. If the handoff fails, defer or take a costed fallback.
- **Novelty rationale:** Not the parent's weight/slot swap or a frozen adapter bank: the handoff changes who serves the old obligation and permits reclaiming the prior holder under a single-live-holder budget.
- **Cheapest first test:** Force two sequential slot reuses in a small network with changing shared features. Compare verify-and-release with copy-and-release, a central adapter bank, and duplication at matched peak memory and action budget.
- **Old-task retention check:** Record worst-window live A, including the handoff transition, and score C when destination capacity is contested.

#### 13. Boundary-dependent memory format (P)

- **Mechanism:** At a last-copy release, write the type of evidence the downstream consumer would otherwise lack: a discrete premise, a short old-target vector, or a conditional residual. Format and payload both count against a fixed buffer.
- **Novelty rationale:** DER and the parent's residue-to-repair compiler are single-format baselines. The bet is an interaction between the destroyed operation and the cheapest evidence format for that particular downstream consumer, not better example ranking.
- **Cheapest first test:** Alternate toy casts, hard resets and output masking, with the same held-out margin profile. Compare adaptive typing, the strongest single-format arm, and a type-shuffled arm at equal bytes, probes, and repair updates.
- **Old-task retention check:** Test both old obligations and C after decoding and on a later B segment that does not contain the same type of event.

#### 14. Common-state discriminator escrow (P)

- **Mechanism:** Before a family of exact mergers, save only a message that disambiguates incompatible old obligations conditional on what the actual downstream state still says. Share a message value across branches that never need opposite answers from the same observation.
- **Novelty rationale:** PR #110 already gives a global confusion graph and PR #113 escrows self-labels. This is a two-stage encoding policy keyed to the last operation that still lets the encoder choose: pay for a short early commitment only when no later legal observation can refine the ambiguity in time.
- **Cheapest first test:** Enumerate a small tree of publicly revealed B branch types, some revealed before and some after a carrier dies. Compare with optimal unconditional coloring, ordinary self-label escrow and adaptive stored-target replay; count waiting and metadata, and reject if adaptation only wins with oracle future B.
- **Old-task retention check:** Decode into a live model on each admissible branch and score normal A/C, including rare branches where the encoder could not wait.

#### 15. Consumer-local regeneration (P)

- **Mechanism:** After a restricted carrier fails, regenerate its operational output from a different still-live carrier for just the consumers that lost access. Do not attempt to reconstruct the erased tensor or replay its old values.
- **Novelty rationale:** The parent's borrow-back repairs an A readout and error feedback repairs a write residual; here a regenerated *intermediate* has several future consumers, so the claim is sharing a repair across them without fitting the old model.
- **Cheapest first test:** In a tiny MLP with two later slot consumers, fit one bounded regenerator on development streams. Compare with separate consumer patches, terminal readout, and direct equal-byte residual storage at the same compute.
- **Old-task retention check:** Score immediate and delayed A service on distinct read/write-dependent slices and C under the same future consumers.

#### 16. Side-information renewal (P)

- **Mechanism:** For a compressed old obligation decoded using the current model as side information, refresh only the part of its decoder input that the next identified operation would erase. Existing memory payload stays fixed until renewal no longer pays.
- **Novelty rationale:** This converts the drift-dependent code-length problem of [PR #105](https://github.com/manojbajaj95/cl/pull/105) into an operation-local refresh, not a new description lower bound or another complete memory checkpoint.
- **Cheapest first test:** In a tiny model with public prototype keys and periodic prototype merges, compare localized reference renewal to re-encoding whole records and storing independent descriptions at equal lifetime memory and work.
- **Old-task retention check:** Reinstall into the live model after two renewal cycles and one missed refresh; check old prototypes, unseen A queries, and C outside the dictionary.

#### 17. Next-consumer repair queue (I)

- **Mechanism:** When labels remain available, order repair by the first downstream operation that would propagate the current defect to another task, not by the time the original target went missing. Trigger only if that consumer dependency is causally verified.
- **Novelty rationale:** Stored-label replay has no merger deadline. This is a scheduling improvement aiming to reduce *collateral* failure, not PR #113's rejected earliest-deadline policy or MIR's prediction of the currently most interfered example.
- **Cheapest first test:** Give two toy defects the same immediate A loss but only one a pending shared-slot read; compare equal-update MIR, fixed scheduling, pre-shock escrow and late replay. Remove the shared read as a negative control.
- **Old-task retention check:** Check trajectory minima for both repaired and untouched old tasks as well as final A/C; no credit if the scheduler just moves bad service onto an unprioritized task.

### D. Turn addresses into constraints a learner can reuse

#### 18. Paired-loss regression tests for new optimizers (P)

- **Mechanism:** Build a small suite of legal A-variant state pairs whose distinguishing contrasts survive until different operations. Require an optimizer rewrite to pass the existing contrasts and explicitly record new first-loss addresses before deployment.
- **Novelty rationale:** Beyond terminal model parity or an A-curvature penalty: this is a behavioral equivalence check over state transitions with distinct future obligations, transferable across implementations of the same update.
- **Cheapest first test:** Mutate a tiny reference optimizer with clipping, cast placement and slot-reset changes that tie on B and often on first-step logits. Compare the witness suite with budget-matched random trajectories and endpoint checks for selection of a safer implementation.
- **Old-task retention check:** Run the selected implementation on previously unseen A variants and check ordinary A/C after long B, not just the checked witnesses.

#### 19. Cross-address routing policy (P)

- **Mechanism:** Route a bounded intervention budget by operation class: e.g. remap precision at a cast, retain an alias at retirement, or repair a read path when the distinction is still present. The policy may abstain when controls cannot distinguish addresses.
- **Novelty rationale:** Unlike the parent’s cross-optimizer map translation, this tests whether the diagnosed failure class selects a *different mechanism* rather than just the same damping in a different basis.
- **Cheapest first test:** Use pairs of small hosts with identical live forgetting curves but different verified loss operations. Factorialize policy × operation and compare the best fixed intervention and an equally informed validation-tuned mixture; require a held-out interaction.
- **Old-task retention check:** Report worst-case live A/C over host classes, charging abstentions and fallbacks, not just an aggregate gain driven by one easy class.

#### 20. Loss-resistant optimizer interface search (P)

- **Mechanism:** Search over the optimizer's declared producer/consumer interfaces and value lifetimes, not just learning rates, requiring the same B-facing contract and budget. Reward designs that preserve useful distinctions across multiple previously identified failure addresses.
- **Novelty rationale:** Optimizer tuning and mixed precision are controls; the proposed object is a reusable set of retention constraints over legal intermediate states. A slowing of B or freezing the A-sensitive layer does not qualify.
- **Cheapest first test:** Exhaust a small grammar of normalization order, temporary liveness and slot representations; compare with the same search ranked on terminal A/B only and with equally tuned OGD. Test whether operation-level constraints improve transfer to a different B order or batch size.
- **Old-task retention check:** Check common and rare old variants, C, and transient minima in B sequences longer than those seen by the search.

#### 21. Prospective safe-write menu (P)

- **Mechanism:** Compile each supported operation into a small menu of legal alternatives with certified old-obligation behavior for a delimited state family. At deployment, use only the alternatives justified by **current** eligibility evidence; expire the menu when its assumptions no longer hold.
- **Novelty rationale:** The parent forecasts map expiration and proposes unavoidable-loss checks; this turns finite certificates into a multi-operation execution interface that can take the fastest B option without treating a forecast as proof.
- **Cheapest first test:** In an enumerated fixed-point host, check all menu entries on all states in each certified family; test online composition under unseen schedules with distribution shift. Compare with a static safe rule and a cost-matched online trial-update filter, charging certification separately.
- **Old-task retention check:** Score actual A/C service inside the certified family and after drift or fallback; measure B service lost to conservative certification.

#### 22. Reclamation by redundant obligation (P)

- **Mechanism:** Intentionally retire the carrier at a verified loss address when independent live information implies the *same* old obligation for the deployment domain. Spend the freed optimizer memory on B rather than preserving a historical variant that no longer changes a required answer.
- **Novelty rationale:** This is neither low-importance pruning nor learning an obsolescence classifier. It uses a testable side-information substitution, with counterexamples blocking reclamation; the task contract, including archived queries, does not silently change.
- **Cheapest first test:** In a finite rules task, supply some redundant obligations and some lookalikes that diverge under rare legal contexts. Compare to sensitivity pruning and no reclamation under equal memory; vary rare-context coverage to find where the substitution breaks.
- **Old-task retention check:** Score rare counterexamples, historical queries still in scope, live A and C after multiple reclamations; reject on any verified equivalence violation in the finite domain.

## Ranked deeper sub-questions

1. **Does the address buy live retention beyond knowing the bad step?** In compatible nonlinear A/B pairs, does replacing the nominated operation beat equally costly whole-step, wrong-operation and adjacent-step interventions at matched B progress? If not, the map is a diagnostic, not an optimizer primitive.
2. **Are there actual mergers outside deliberate resets or coarse arithmetic?** Locate exact full-state witnesses where possible; otherwise ask whether the same budgeted boundary survives reasonable changes of reader capacity, precision and margin, or whether it dissolves into smooth contraction and temporary masking.
3. **What can be decided before the write without an oracle?** Compare the hindsight intervention frontier with a frozen prospective policy that sees only deployment-available evidence. If the gap is large, determine whether a small added audit, not a future batch transcript or retained A labels for free, closes it.
4. **Do loss addresses and remedies compose?** Protect two distinctions together in the same stream: can a carrier saved at one operation be consumed or erased at the next, and does a verified handoff prevent that better than equal-byte replay or independent safeguards?
5. **Which part of the address transfers?** Across equivalent parameterizations, implementations and B orderings, test whether the useful invariant is the physical write, the retirement of a sufficient carrier set, or only an abstract change in the observation budget. If transfer fails, bound the cost of recalibrating before proposing an online method.
