# Never-ending pretraining 5 · Put operations on the learner, not just its weights

Child of [Never-ending pretraining 4](never-ending-pretraining-4.md) ([PR #393](https://github.com/manojbajaj95/cl/pull/393)). The [review](https://github.com/manojbajaj95/cl/blob/fcf56597c126ca4da1c27b5b21e5f6fcc5f48b06/reviews/flood-triage.md) retained NP4-13 (distill a teacher's response to future evidence) and NP4-19 (compress by what future operations can distinguish) at 3, with no 4. [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) already gives a Nerode-type quotient for declared future learning, and [Learning Dynamics of Continual Learning](https://arxiv.org/abs/2609.33620) already ties updates to their effects on future prediction and trainability. Neither equal current reads with different futures, nor a learning-response signature, counts as a new primitive here. The proposals change what training can execute, permit, cancel, or guarantee. No experiments were run.

**Fixtures and common controls.** One regularly updated learner. A checkpoint includes weights, optimizer state, randomness when relevant, and any claimed contracts or summaries. Use affine or finite-state learners for exact counterexamples, then a small shared encoder with byte-defined old reads. Declare the action alphabet, scope of protection, state and compute budgets, and whether an invariant holds at every step or only at publication. Compare preserved responses against output distillation, [Sobolev training](https://arxiv.org/abs/1706.04859), [trajectory matching](https://arxiv.org/abs/2203.11932)/[gradient matching](https://arxiv.org/abs/2006.05929), and [MAML](https://arxiv.org/abs/1703.03400) where appropriate. Compare state schemes against full checkpoints, output-only distillation, equal-byte low-rank or quantized state, [Fisher-weighted retention](https://arxiv.org/abs/1612.00796), and [sketched influence](https://arxiv.org/abs/2609.15044). Give a simple symbolic runtime or exact replay the same operation metadata. Count negative steps, scratch buffers, logs, slow paths and retained state. Kill an operation if a simpler control matches its declared behavior, cost, and retention.

## A · Make an instruction act on learning itself

### NP5-01 · Execute the interaction between two lessons
- **Mechanism.** Make the commutator of two certified reversible learning actions an instruction: run A, B, then their inverses in the same order. First-order effects cancel; in small-step flows the leading effect is their vector-field bracket. Give it an explicit effect budget rather than pretending it is an ordinary descending batch.
- **Nearest art.** [Nonlinear control](https://doi.org/10.1007/978-1-84628-615-5) already uses bracket motions; [SGD dynamical stability](https://arxiv.org/abs/2305.17490) analyzes training dynamics. The claim is an executable new learning move for a protected open-ended trainer, not that SGD order matters.
- **First test / kill.** Use two affine shears whose commutator moves a held-out response direction that neither instantaneous individual action spans at the initial point. Compare all equal-length signed schedules and a direct projected step. Kill if the bracket is not controllable across step sizes or the direct step buys the same effect.
- **Retention.** Keep first-order old reads and old effects outside the intended bracket coordinate after repeated executions.

### NP5-02 · Cancel a past instruction through a later block
- **Mechanism.** For actual history “A then B,” execute the conjugated inverse of A through B: apply the action B composed with inverse A composed with inverse B, with compositions read right to left. Compile that operation from a compact representation of B; decline if B erased distinctions needed for the inverse. Preserve what B would have learned without A.
- **Nearest art.** [Reversible Learning](https://arxiv.org/abs/1502.03492) reverses optimization to obtain hypergradients, and [Sagas](https://doi.org/10.1145/38713.38742) introduced compensating transactions. A generic compensation may erase later optimizer effects; this one must reproduce the later block as if A had never run. [Deletion-order analysis](https://arxiv.org/abs/2610.01149) is a close dynamics comparator.
- **First test / kill.** In a finite two-mode affine learner, cancel A after two differently ordered B blocks. Compare inverse-vector subtraction, exact replay without A and influence removal. Kill if the compact version needs the full block trace or loses B's behavior on a fresh next update.
- **Retention.** Preserve lessons in B that are independent of A, including old facts sharing the edited head.

### NP5-03 · Rewrite an instruction only when every later context may substitute it
- **Mechanism.** Compile repeated training subwords into canonical instructions using equalities proved on the reachable state space for a declared action vocabulary. Distinguish an equality of present effects from a congruence: substitute only when every permitted suffix has the same protected reads. An operator proof expires if its state domain changes.
- **Nearest art.** [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) studies equivalence of states by future training; [Causal Edit Serialization](https://arxiv.org/abs/2610.22820) models interacting edits. Here it is the instruction language, not the checkpoint, that gets rewritten and shortened.
- **First test / kill.** Supply two word pairs with equal terminal reads, only one of which remains equal after a third action. Kill if ordinary peephole rewriting with the same operator model achieves the same speed and safety, or the compiler accepts the bad pair.
- **Retention.** Keep old read traces at public boundaries and preserve the previously valid suffixes of the rewritten instruction.

### NP5-04 · Compile an intended effect into legal positive lessons
- **Mechanism.** Treat a requested change as a target in a cone of measured lesson responses. Compile it into nonnegative doses of actual available lessons with protected directions constrained. If the target lies outside the cone, return a separating direction and do not apply a negative-dose parameter edit. Initially restrict the claim to exact local linear dynamics.
- **Nearest art.** [Gradient Surgery](https://arxiv.org/abs/2001.06782) alters conflicting gradients; [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) characterizes reachable safe responses in an affine model. Here the differentiator is translation into allowed *ordinary lessons* under restricted controls, including a witness that a repair is unteachable.
- **First test / kill.** Give one attainable target and one that a projected parameter edit attains only by negative evidence weight. Kill if constrained example reweighting matches execution and rejection at the same cost, or the cone witness rejects a realizable target.
- **Retention.** Keep a protected old read linked to the easiest positive-dose lesson and old tasks outside the synthesis basis.

### NP5-05 · Prime a response without changing a current answer
- **Mechanism.** Allow a finite operation on hidden update state that keeps current reads and the response to a reference lesson fixed, but changes the response to a second named lesson. In a tiny bilinear system, solve for an optimizer or feature-state displacement satisfying both equalities and the requested directional derivative. This prepares learning without providing the actual new answer.
- **Nearest art.** [Dynamics of Hidden Learning Structure](https://arxiv.org/abs/2610.29054) jointly regulates protected repairs and trainable structure, and [Matched Specialization, Different Adaptation](https://arxiv.org/abs/2610.15830) changes later adaptation through Adam second moments. A conditional two-lesson instruction must beat both broad priming and simple moment transplantation.
- **First test / kill.** Prepare for one format while protecting response to another with the same present accuracy. Kill if MAML, protected repair, or direct moment transfer realizes both response constraints at equal state, or any protected reference response drifts.
- **Retention.** Keep old predictions immediately and keep old learning speed on a third, unprimed lesson.

### NP5-06 · Give a training step a covariance but not a mean change
- **Mechanism.** Specify a zero-mean random displacement in the kernel of protected current reads and set its covariance as part of the training instruction. Choose a covariance that changes the chance of entering one accessible response region after the next ordinary lesson. Use a declared symmetric distribution over two exactly solved displacements in the first fixture.
- **Nearest art.** [SGD noise experiments](https://arxiv.org/abs/2301.13703) separate effects of noise across learning regimes, and [Matched Specialization](https://arxiv.org/abs/2610.15830) studies persisted second moments. The object is a controllable *distribution of executed effects*, not optimizer-memory statistics or generic added noise.
- **First test / kill.** Give a tiny learner two future response regions accessible along different null directions. Kill if isotropic noise or covariance-matched ordinary mini-batching attains the same controlled transition at equal old-task loss, or the first moment shifts.
- **Retention.** Keep protected old reads on every random branch, not just on average.

### NP5-07 · Transfer a conserved training quantity with a named compensating recipient
- **Mechanism.** For two branches of a shared linear learner with explicitly defined conserved charges under ordinary flow, add a narrow exchange instruction with opposite charge changes in the two branches. The sum remains invariant, and the payload names the authorized recipient. Derive the exchange algebra on the fixture rather than assuming real networks have the same conservation law.
- **Nearest art.** [Noether’s learning dynamics](https://arxiv.org/abs/2105.02716) relates parameter symmetries to conserved quantities; [FIRE](https://arxiv.org/abs/2602.08040) reinitializes for stability and plasticity. This proposal makes a conserved quantity transferable under an explicit balance sheet instead of resetting an entire branch.
- **First test / kill.** Choose a two-branch factorized model in which one branch is poorly conditioned. Compare natural balanced rescaling, independent reinitialization, and constrained projected optimization. Kill if a charge transfer cannot change later conditioning with current reads matched, or the ordinary balance step matches fully.
- **Retention.** Keep both old functions and adaptation to a third task that uses the recipient and donor jointly.

## B · Change what a checkpoint promises

### NP5-08 · Execute safely from a checkpoint that denotes a set
- **Mechanism.** A checkpoint may retain a set of possible hidden states rather than inventing a single missing moment estimate. Execute a training action only if its effect is acceptable for every state in the set; propagate the set under the actual action. Use a box and affine transitions first, with a fallback to a full state when one is still available.
- **Nearest art.** [Robust state abstractions](https://arxiv.org/abs/2007.07206) handle latent environment variation, and [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) retains future-relevant distinctions. This operation lets a knowingly ambiguous checkpoint *keep training* without claiming those distinctions are equal.
- **First test / kill.** Quantize two optimizer states to the same set; give one safe batch and one which reverses a protected margin in only one state. Kill if interval filtering plus standard compression gives equal throughput and retention, or the ambiguous batch is accepted.
- **Retention.** Hold protected margins in each represented state, and keep nonambiguous old tasks trainable.

### NP5-09 · Preserve paired counterfactuals, not just two marginal laws
- **Mechanism.** Checkpoint a shared noise map and a compact action-dependent coupling for “run either A or B on the same future draws.” Two representations are interchangeable only if the paired effect needed by the comparison survives. In a finite example, keep a common Bernoulli bit and the permutation with which each instruction consumes it.
- **Nearest art.** [Bisimulation metrics](https://arxiv.org/abs/1207.1386) compare controlled transition laws, while [structural counterfactuals](https://arxiv.org/abs/1302.4929) and [WorldKernel](https://arxiv.org/abs/2606.10934) explicitly distinguish a cross-world coupling from marginal predictions. The proposed action tests checkpoint interchangeability for a *specified optimizer counterfactual*, not identification of a coupling from the marginal update laws.
- **First test / kill.** Make A and B individually fair while changing their joint difference by flipping one draw. Kill if a common seed plus the ordinary draw program gives the same paired behavior at equal bytes, or single-action calibration hides a bad paired checkpoint.
- **Retention.** Keep marginal old performance for both actions and the paired comparison for an older, untouched branch.

### NP5-10 · Erase a hidden history by executing a neutral synchronizer
- **Mechanism.** Search for a legal finite word that sends all admitted hidden states with the same protected reads to a common successor without changing those reads. Commit that word before dropping history. The object is an active reset map realized by training, not a claim the histories already were equivalent.
- **Nearest art.** The repo's [synchronizing-batches branch](https://github.com/manojbajaj95/cl/pull/213) already pursues synchronization by training, and [Dynamics of Hidden Learning Structure](https://arxiv.org/abs/2610.29054) regulates future response. This candidate must synchronize a specifically named hidden coordinate while keeping another hidden capability distinguishable, not reset all differences.
- **First test / kill.** Give three equal-read optimizer states with two hidden coordinates. Kill if an ordinary reset or existing synchronized batch erases the intended history and retains the other coordinate just as well, or the proposed synchronizer erases both.
- **Retention.** Keep current old reads and a future lesson dependent on the hidden coordinate that was not authorized to reset.

### NP5-11 · Substitute a checkpoint only when future training costs remain affordable
- **Mechanism.** Use a directed simulation relation: replacement state S can stand in for T if S can match each required transition and protected read of T within a declared cost vector, recursively. In a finite learner attach a Pareto antichain of continuation costs and use it to grant or refuse replacement. Symmetric equivalence is not required.
- **Nearest art.** [MDP abstraction](https://arxiv.org/abs/2302.03921) preserves predictive structure and [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) protects a capability-cost frontier. The differentiator is a compositional *substitution rule* for an already deployed checkpoint with fixed future budgets.
- **First test / kill.** Give two exact-output checkpoints with equal eventual responses, but one needs an extra intervention to achieve a named continuation. Kill if storing a scalar frontier or explicit state-machine simulation meets all replacement decisions at equal cost.
- **Retention.** Preserve old performance and feasible old lessons under their original budgets, not merely in unlimited time.

### NP5-12 · Add a training instruction without retroactively making discarded state available
- **Mechanism.** Bind every compressed checkpoint to an action vocabulary. When enabling a new instruction, test whether it maps equivalent old states to equivalent successors. If not, load a predeclared sufficient sidecar or refuse the instruction. In the linear fixture the certificate is whether the discarded subspace remains in the kernel after applying the new matrix.
- **Nearest art.** [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) gives quotients relative to declared probes. [Predictable MDP Abstraction](https://arxiv.org/abs/2302.03921) studies abstraction that preserves dynamics. This is an online operation for extending the alphabet without making unsupported guarantees about already compressed checkpoints.
- **First test / kill.** Drop a momentum direction invisible to existing actions; add one action that rotates it into an old read. Kill if a versioned full checkpoint or standard validity check manages both compatible and incompatible extensions at the same storage and cost, or if the rotation is silently allowed.
- **Retention.** Keep all old action sequences and the protected read on successful extension; on refusal keep the old running learner unchanged.

### NP5-13 · Spend an error allowance only when a later action can amplify it
- **Mechanism.** Attach a directional error set to approximate checkpoint state. Each action advances that set and debits protected read tolerances only in visible directions. An operation is refused before it exceeds a protected tolerance, even if its immediate error is small and only a known follow-up makes it visible.
- **Nearest art.** [Bisimulation metrics](https://arxiv.org/abs/1207.1386) bound differences between states, and [finite-radius training sensitivity](https://arxiv.org/abs/2608.30960) examines deviations beyond infinitesimal response. This is a live budget for composing approximate operations rather than a fixed compression score.
- **First test / kill.** Compose a contraction, a rotation, and an amplifier on a noisy two-coordinate checkpoint. Kill if scalar error certificates match accepted actions at equal guarantees, or actual downstream read error exceeds the amount the contract promised.
- **Retention.** Keep separate tolerances for rare old queries and common ones through repeated accepted actions.

## C · Give training instructions execution semantics

### NP5-14 · Commit the optimizer and the example together
- **Mechanism.** A committed training instruction advances weights, moments, and the consumed-example cursor together. Stage the small changed blocks, bind them to an operation nonce, and publish one version pointer; abandoned attempts cannot leave changed moments behind. Use a segmented optimizer with idempotent materialization so a retry does not allocate another full checkpoint.
- **Nearest art.** [Hybrid-parallel in-memory checkpointing](https://arxiv.org/abs/2310.12670) makes pretraining recovery efficient, and [DataStates-LLM](https://arxiv.org/abs/2601.16956) decomposes heterogeneous training state into composable providers. Exactly-once transactions are old; the candidate must beat both segmented checkpointing and generic logging while preserving the effect of a single partially executed step.
- **First test / kill.** Interrupt an Adam step separately after the weight, moment and cursor writes. Kill if ordinary transaction logging or full checkpoint replay attains equivalent states under the same storage and restart budget, or any retry changes the next step.
- **Retention.** Keep old predictions and old-example responses after each recovery.

### NP5-15 · Freeze state proven unreachable by a permitted training program
- **Mechanism.** Keep a read-only base plus a compact writable overlay chosen by the transitive write footprint of the allowed program, including optimizer buffers. If a new instruction could write a frozen block, materialize it with the original numeric state before use. The inactive state still serves reads; it is not zeroed or replaced by an approximate model.
- **Nearest art.** [LoRA](https://arxiv.org/abs/2106.09685) freezes a base with trainable low-rank updates, and [continual pruning](https://arxiv.org/abs/1903.04476) manages capacity across tasks. This contract certifies a program-specific writable footprint instead of a fixed architecture partition.
- **First test / kill.** Use different action programs with the same active weights but different future optimizer dependencies. Kill if fixed adapters or standard dynamic freezing saves equal active state and preserves thawed behavior, or a program writes an unmaterialized block.
- **Retention.** Keep old reads from the frozen state and old training response after one block is thawed.

### NP5-16 · Make a learning authorization noncopyable inside a checkpoint
- **Mechanism.** Represent permission for a bounded operation as a linear capability. Splitting an optimizer job partitions the budget instead of cloning it. Commit consumes a capability once and ties the consumption to the promised output footprint; later copies of the same state must reconcile against one authoritative counter before publication.
- **Nearest art.** [Linear logic](https://doi.org/10.1016/0304-3975(87)90045-4) formalizes consumable resources. [Fiber Regulation and Acquisition](https://arxiv.org/abs/2610.29054) constrains learning actions. This proposal is a semantics for authorizing *composed* learning effects, not a claim an unenforced checkpoint can prevent copying.
- **First test / kill.** Split one shared-encoder update into two packages which each ask for the same scarce protected movement. Kill if a standard external quota matches the accepted programs and budget decisions at equal cost, or splitting doubles what can be spent.
- **Retention.** Keep old capabilities with separate allocations and reject attempts without consuming their budget.

### NP5-17 · Relax a protected read during a private step and restore it at commit
- **Mechanism.** Allow a short private sequence outside a protected set only if a verified completion returns to it before any publication or unrelated update. Use a coupled forward and compensating action with a finite scratch budget; abort if the completion cannot be proven. Contrast with always-safe paths, not with publishing transient degradation.
- **Nearest art.** [Control barrier functions](https://arxiv.org/abs/1903.11199) target forward invariance; the repo's [return corridors](https://github.com/manojbajaj95/cl/pull/168) include trajectories back to safety. Here the unit is a single atomic training instruction with an externally unchanged old read at every visible boundary.
- **First test / kill.** Use a two-step affine construction whose best endpoint cannot be reached through individually safe steps. Kill if projected optimization or an existing return corridor achieves it at equal training cost, or any failure exposes the temporary violation.
- **Retention.** Keep old-task reads at all public boundaries and keep unrelated optimizer state when a private step aborts.

### NP5-18 · Share a reversible training prefix without keeping every alternative
- **Mechanism.** Define an instruction with several legal continuations that all start from one short reversible training prefix. Execute that prefix once and use bounded reversible suffix scratch space to pick and commit a continuation. Selection may use a protected proof but may not average alternative models; always publish one continuation in one lineage.
- **Nearest art.** [Reversible Learning](https://arxiv.org/abs/1502.03492) reverses optimizer paths for differentiation, and [automatic recovery](https://arxiv.org/abs/2601.17483) saves training after instability. The candidate is reusable scratch execution for a composition that cannot be selected until after its common prefix.
- **First test / kill.** In a tiny learner, make prefix effects determine which of two continuations is legal. Kill if a generic shared checkpoint plus retries matches prefix compute and scratch bytes, or rejecting a suffix changes a later legal suffix.
- **Retention.** Keep old reads through the published path and keep response to an unrelated later batch after a losing suffix runs privately.

### NP5-19 · Upgrade an optimizer operation without stranding in-flight instructions
- **Mechanism.** Version the semantics of an instruction whose execution has already started. Specify an adapter on intermediate state and a continuation relation showing which v1 suffixes v2 can still satisfy. If none exists, finish under v1 instead of interpreting old intermediate buffers as v2. This is not a requirement that all new instructions emulate v1.
- **Nearest art.** [Universal Checkpointing](https://arxiv.org/abs/2406.18820) changes distributed parallelism at resume, and [staged training](https://arxiv.org/abs/2203.06211) transports optimizer state across model sizes. The proposed adapter preserves a *partly executed instruction* across an optimizer semantic change, not just the placement or dimensions of its state.
- **First test / kill.** Switch two momentum implementations mid-instruction in a toy trainer, including one unreachable v1 accumulator. Kill if finish-old-then-switch or ordinary optimizer-state transfer matches continuation cost and retention, or unsupported execution is accepted.
- **Retention.** Keep the old instruction's published guarantees and old tasks not involved in the upgrade.

### NP5-20 · Expose two writable views without silently choosing a completion
- **Mechanism.** Give an operator a view of the checkpoint in which it requests a change; realize it in shared state only when the companion view can remain within its training contract. Use a bidirectional lens with an explicit complement and a partial put operation, so ambiguity about future behavior causes refusal rather than an arbitrary reconstruction.
- **Nearest art.** [Bidirectional lenses](https://doi.org/10.1145/1047659.1040325) synchronize views using complements, and [Intrinsic–Extrinsic Coupling](https://arxiv.org/abs/2609.30185) demonstrates continuation-sensitive state interventions. The requested put must satisfy future-operation obligations of both views, not just their current projections.
- **First test / kill.** Give two moment/weight views of one finite learner with a put that is harmless in current reads but blocks a promised subsequent step. Kill if an ordinary lens plus the same constraints realizes all legal puts at equal state, or the proposed lens accepts this one.
- **Retention.** Keep old reads and future steps on the companion view after every successful put.

## D · Protect a sequence, not merely the next batch

### NP5-21 · Compile a training contract into a monitor of legal words
- **Mechanism.** Keep a small automaton that accepts action sequences, not per-operation permission bits. Its state distinguishes whether a required repair is pending or already paid. Each actual training action advances the monitor; the same next gradient may be legal in one history and illegal in another with identical weights.
- **Nearest art.** [Linear logic](https://doi.org/10.1016/0304-3975(87)90045-4) gives consumption semantics, and [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) addresses future closure viability. The candidate makes sequencing obligations part of the learner's execution rules instead of another loss term.
- **First test / kill.** Construct two equal-read histories differing only in one pending obligation. Kill if a conventional finite-state optimizer wrapper with the same proof achieves equivalent behavior and cost, or the monitor rejects an equivalent legal sequence.
- **Retention.** Keep old obligations that were already discharged and old tasks with no relation to the pending repair.

### NP5-22 · Replace a retention test by a stronger proof obligation
- **Mechanism.** Exchange one old read certificate for a smaller family of inductive constraints when that family implies all old obligations under every declared action. Store the implication, not weights for a second copy of the old task; revalidate it when an action is added. In a finite linear fixture, prove implication by row-span containment and closure.
- **Nearest art.** [Forward invariance of neural ODEs](https://arxiv.org/abs/2210.04763) verifies state constraints, and [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) distinguishes semantic reconstruction from protecting a historical realization. This operation substitutes an inductive *warranty* for a list of old tests rather than compressing the checkpoint itself.
- **First test / kill.** Replace multiple old read queries by a few invariants, including one query invisible until a later allowed rotation. Kill if direct span compression plus a fixed guard works equally well, or the new proof omits the delayed read.
- **Retention.** Keep all implied old queries and old tasks outside the new certificate at their original tolerances.

### NP5-23 · Make temporary learning state expire by a training action, not wall time
- **Mechanism.** Put a volatile response change in a transient mode. A named class of subsequent honest updates discharges it with a verified contraction or annihilation, while permanent reads and permanent learning actions remain independent of the transient mode. A model can acquire a temporary ability to learn something without an arbitrary timer or replay.
- **Nearest art.** [Noether's learning dynamics](https://arxiv.org/abs/2105.02716) exposes training invariants and [SGD dynamical stability](https://arxiv.org/abs/2305.17490) analyzes contraction and stability. The new operation intentionally creates an effect whose expiration condition is semantic training progress.
- **First test / kill.** Let one real follow-up task erase the priming action and another task leave it live at the same step count. Kill if elapsed-step decay or a standard transient adapter achieves equal behavior and cost, or the named discharge also erases a permanent lesson.
- **Retention.** Keep old reads during the transient and keep old permanent response after discharge.

### NP5-24 · Apply a correction only when two safe instructions run together
- **Mechanism.** Compile a joint execution branch with its own inducement term for two overlapping updates. On the finite fixture subtract their predicted mixed effect on a protected read only when both execute, leaving each action on its own unchanged. Charge the corrective term as a legal third action, and refuse if it cannot be realized.
- **Nearest art.** [Intrinsic–Extrinsic Coupling](https://arxiv.org/abs/2609.30185) isolates nonadditive state-intervention and continuation effects, and [Gradient Surgery](https://arxiv.org/abs/2001.06782) mitigates gradient conflict. The candidate adds a jointly triggered instruction rather than modifying the two standalone lessons to be universally harmless.
- **First test / kill.** Find in a quadratic fixture two individually safe updates whose composition breaks an old read. Kill if gradient surgery, serial projection, or an explicit two-case conditional program matches action fidelity and budget, or the correction leaks into the singleton case.
- **Retention.** Keep protected reads on the joint path and retain prior independent learning behavior of each instruction.

### NP5-25 · Run a protected inverse without reconstructing the whole past
- **Mechanism.** Permit a many-to-one training action to be reversed only on the declared protected quotient. In an affine fixture check that it maps discarded directions to discarded directions and induces an invertible map on the retained quotient; invert that smaller map and never claim recovery of erased optimizer traces.
- **Nearest art.** [Reversible Learning](https://arxiv.org/abs/1502.03492) reverses full states with auxiliary information; [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) identifies distinctions required for future responses. The desired operation is undo with an honest, first-class scope rather than selective data unlearning or reconstruction from a lossy snapshot.
- **First test / kill.** Use an action that erases one hidden coordinate while changing a protected one invertibly, then add a variant which makes the erased coordinate future-visible. Kill if ordinary reversible storage or checkpoint recovery matches both cost and scope, or the unsafe inverse is admitted.
- **Retention.** Keep the old read trajectory on the recoverable quotient and keep unrelated current improvements.

### NP5-26 · Construct a safe direction by asking what can reveal it later
- **Mechanism.** For linear declared dynamics, close the protected read rows under every allowed future action. Permit a proposed additive displacement only in the annihilator of this closed space, then find the best legal displacement within it. A currently hidden change is blocked if any allowed suffix could reveal it; this constructs a protected update, not a smaller snapshot.
- **Nearest art.** [AlphaEdit](https://arxiv.org/abs/2410.02355) protects current reads through a null space; [Fiber Fingerprints](https://arxiv.org/abs/2608.15976) characterizes future distinguishability. Closing the read rows removes unsafe directions rather than creating capacity. It earns its cost only if it leaves useful moves with a stronger protection guarantee than rechecking a finite probe bank; [Generalized Residual Closure](https://arxiv.org/abs/2609.38911) is a strong safe-response comparator.
- **First test / kill.** Compare two displacements invisible today; an allowed rotation reveals just one. Kill if static or repeatedly recomputed null-space edits find the same surviving useful moves at equal cost, or if the closed annihilator is routinely empty on the fixture.
- **Retention.** Keep old immediate and delayed reads on every declared suffix exact in the linear case.

## Ranked deeper questions

1. **Can a learner keep training safely from incomplete state without pretending the state is exact?** Start with NP5-08, NP5-12 and NP5-13. Use an equal-read pair separated by a new action. Beat full checkpointing and standard interval filtering on accepted useful updates at the same protected-read tolerance, including deliberate refusals.
2. **Can two legal lessons synthesize a useful action that neither can express alone?** Start with NP5-01 and NP5-04. Include a negative where the direct projected step legally achieves the goal more cheaply. Demand a reachable target and retained old response, not a detected order effect.
3. **What is the smallest genuinely future-safe set of useful writes?** Start with NP5-26, using NP5-22 as the maintained protection proof. Compare the closed annihilator with static and probe-based alternatives, and report an empty safe set as a substantive negative rather than relaxing protection.
4. **Can undo be both useful and honest about which past is gone?** Contrast NP5-02 and NP5-25 on paths with a noninvertible suffix. Require later independent lessons to remain in selective cancellation and refuse when the relevant lost state cannot be recovered. Count all retained bytes against full replay.
