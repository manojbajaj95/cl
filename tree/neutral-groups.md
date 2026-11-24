# Neutral unit groups

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Cancelling-pair renewal](cancelling-pairs.md) ([PR #175](https://github.com/manojbajaj95/cl/pull/175)). **Review seed:** [Flood triage row 279](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/flood-triage.md#L279) scored two ideas 3: find a small neutral group when no pair cancels (#06), turn it into two useful gates and reclaim the remaining slots; then recover a pair by folding spent gates into compatible live carriers without undoing their writes (#13).

**Is the space of output-neutral groups a new memory resource for continual learning?** Not as a null space, an equivalence class, or a way to count free neurons. [Hidden symmetries of ReLU networks](https://arxiv.org/abs/2306.06179) establishes function-preserving redundancies beyond rescaling and permutation in some networks. [Net-Trim](https://arxiv.org/abs/1611.05162) sparsifies a network subject to layer-output constraints; [Neuron Merging](https://arxiv.org/abs/2010.13160) compensates for removed neurons in the next layer. [GPM](https://arxiv.org/abs/2103.09762) uses activation subspaces to protect past tasks. [PackNet](https://arxiv.org/abs/1711.05769) frees weights for future tasks; [elastic online networks](https://arxiv.org/abs/2608.01475) already grow and shrink to sustain plasticity. [Net2Net](https://arxiv.org/abs/1511.05641) and [GradMax](https://arxiv.org/abs/2201.05125) already provision capacity without an initial function change.

The narrower candidate is an **editable reserve carried in the arrangement of live units**: learn useful joint release opportunities from past demand, make them spendable by a later editor without the old training data, and replenish them after useful writes become protected. That is memory only if information from past demand helps the editor handle future requests, not merely if a solver can find a neutral move. The [idea ledger](https://github.com/manojbajaj95/cl/blob/48aee0a8c0071a5d4cb82731b2624f4a385ebc9e/reviews/idea-ledger.md) warns against both shortcuts: the [retention-matched reserve rerun](https://github.com/manojbajaj95/cl/pull/21) left only 0.09 absolute MSE points of next-task spread, and Noether memory was erased by a function-preserving rebalance. Here the outcomes are admitted useful edits, net released slots actually used, and total cost at matched retention. Nullity, probe accuracy, and bits readable only in a chosen parameter gauge are not outcomes.

## Contract and two paper witnesses

Start with one additive residual ReLU block. Let `P` be the union of all live protected domains, including ordinary inputs and rare slices. On a verified activation cell the contribution of each hidden unit to the block output is affine. Stack its vector-valued affine coefficients (restricted to each cell's affine hull) across cells as a column of `D`. A proposed set `S` is **already removable at the block output** exactly when `D 1_S = 0`, where `1_S` is its binary indicator. Such supports are discrete; the union of overlapping neutral groups need not be neutral. A minimal-support nonzero vector in `ker D` gives a circuit of possible *readout reweightings*, not necessarily a removable set. It may take a legal reweight-and-compensate move to reach one, or there may be no such move. There is no general license to rotate ReLU units. To certify a replacement, check the old/new common refinement on all of `P`; boundaries are covered by continuity here, but must be checked separately if routing is discontinuous. Equality at an additive cut is sufficient only if it captures every affected reader. Finite replay checks are not cell proofs.

Publish only exact renewals on `P`, including consolidation and release; stage atomically or check every visible intermediate. Useful requested edits need not be exact renewals, but must clear a frozen utility test against no write and keep every acquisition-anchored old floor. Once a write is installed, include its live scope during every later renewal. Freeze request generators, addressing, deadlines and domains before the renewal algorithm sees the test sequence. Charge host width, optimizer and replay bytes, gate descriptors, spare slots, staging, source access, and all search, training and checks. Require later utility on reclaimed slots; clearing a mask or writing a no-op earns nothing.

The common controls are pair-only (the arity test), exact circuit enumeration or sparse compaction, GPM plus ordinary recycling, and **generic exact joint repair/merge-and-prune + gate reset + the same continuation planner and verifier**. Give that last stack the same physical moves, information and matched search budget; also allow it to run on each trained host. An exhaustive solver with the same starting state and move set is an upper bound, not a baseline the new interface can logically exceed. To separate information stored in the host from better search, cross host preparation and release method, and give a same-byte external edit cache the same opportunity to store past-demand hints.

**Witness 1 — two gates and a real slot, with no pair.** On `P = [-1,1]`, put three ReLUs with signed contributions `[1]₊`, `[x+2]₊`, `−[x+3]₊` over any unchanged base predictor. On `P` they sum to zero; every nonempty proper subset changes the protected output somewhere. Publish `[x−2]₊` and `−[−x−2]₊` in two slots, releasing the third, initially with zero readout. Two predetermined requests each increase only their named gate's preactivation bias by one: the positive gate adds one at `x = 2`, and the negative gate subtracts one at `x = −2`. Either order preserves `P` and the other new target. A third request can then install `[x−3]₊` in the released slot for a further unit of output at `x = 4`, preserving `P` and both targets. This is an existence result against pair-only release, not a separation from exact joint repair. The first swap changes off-domain outputs (e.g. at `x = 3`), so it does not certify an undeclared old task.

**Witness 2 — fold the spent gates or prove why not.** In a separate four-slot state, suppose two installed gates contribute `u = [x−1]₊` and `−v = −[−x−1]₊`, with their effects now owed on `[-2,2]`. Two existing receivers contribute `2u` and `−2v`. Change those coefficients to `3` and `−3` and release the spent gates in one step; the complete function is unchanged. Rebuild the two slots as `[x−4]₊` and `−[−x−4]₊`. A third useful bias write at `x = 4` is available without changing the prior domain. For a hard negative, give the two existing receivers fixed shapes that are affine on `[-2,2]` and permit only readout changes: no combination of them can absorb the two interior kinks of `u−v`. Keeping one kink in a spare slot is not recovering both slots. This obstruction is relative to that move menu; it does not rule out changing the receiver shapes. The compatible case is exactly merge-and-prune plus reset, so it is a positive control, not novelty or indefinite renewal.

## Idea cards

### Find what can be released

#### 01. Cash out a minimal live triple
- **Mechanism:** Enumerate small actual zero-sum supports, stage two gates, and return the other slots as unreserved capacity.
- **Novelty vs nearest prior art — IMPROVEMENT:** More expressive than pair-only release, but circuit enumeration plus exact compaction already gives this one-shot operation.
- **Cheapest first test:** Use Witness 1 and an otherwise matched control with the third bias perturbed. Compare pair-only, exact circuits, GPM plus reset, and exact joint repair.
- **Old-task retention check:** Prove equality on the full interval and check it again after both edit orders and the independent third write.

#### 02. Turn a latent circuit into a legal release
- **Mechanism:** Within fixed cells, solve for a finite readout move on the kernel that drives coefficients to zero, with sign, range, and address restrictions enforced along the allowed publication path.
- **Novelty vs nearest prior art — IMPROVEMENT:** GPM supplies protective subspaces and Net-Trim supplies sparse endpoints; the target is reaching a representation with two specific gate destinations, not finding another null direction.
- **Cheapest first test:** Give two activation matrices the same nullity, but lock the only adjustable coefficient in one. Compare an exact constrained sparse solver with a local projection followed by reset.
- **Old-task retention check:** Refuse the locked proposal, retain all cells in both hosts, and test the first later edit on any released slot.

#### 03. Reroute a circuit around a newly acquired obligation
- **Mechanism:** Keep two overlapping release witnesses. When one unit becomes pinned by a later write, use circuit elimination to propose a new support that avoids it; compile and verify the actual finite move.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Matroid circuit elimination already gives a relation; the candidate is a retained, executable alternative that survives pinning and saves justified replanning.
- **Cheapest first test:** Use two rational circuits sharing one unit, then pin it. Compare reuse of their witnesses against re-enumeration with memoization and generic exact repair, including a sign-constrained case where neither can release.
- **Old-task retention check:** Protect the original cells and the new pin's acquired output through the alternate release and one new use.

#### 04. Spend only cancellation that survives a disputed boundary
- **Mechanism:** A proposed release triggers an exact search for an omitted activation boundary that makes its sum nonzero; add the counterexample cell rather than merely adding a nearby point.
- **Novelty vs nearest prior art — IMPROVEMENT:** Counterexample-guided verification and [APRNN](https://arxiv.org/abs/2304.03496) are the controls; value would come from smaller exact proofs, not a stronger guarantee than full verification.
- **Cheapest first test:** Plant a narrow triangular ReLU residual between all discovery probes. Compare adaptive cell refinement, uniform probes, and full exact checking under the same checker budget.
- **Old-task retention check:** Reject the false group on the overlooked rare slice; accepted groups must keep it through release and a useful write.

#### 05. Count every reader of a silent group
- **Mechanism:** Certify each outgoing read at a common additive cut before releasing a slot; alternatively repair every nonneutral reader in the same transaction.
- **Novelty vs nearest prior art — IMPROVEMENT:** Neuron Merging already adjusts downstream weights. The stress case is one silent output head hiding a live auxiliary or routing reader that also governs future learning.
- **Cheapest first test:** Give a triple a cancelling readout on the main head and a noncancelling readout on an auxiliary head. Compare main-only discovery plus full verification with all-reader discovery plus the same verifier.
- **Old-task retention check:** Keep the auxiliary task and its downstream decisions, not just the main logits, after the reclaimed slot is used.

#### 06. Price the signal that cannot be thrown away
- **Mechanism:** For a group with nonzero protected residual, preserve that residual in the cheapest legal carrier(s), then ask whether two gate slots and a net release still fit.
- **Novelty vs nearest prior art — IMPROVEMENT:** This is exact structured compression plus renewal; the useful result is a boundary between real release and moving the same cost elsewhere.
- **Cheapest first test:** Compare a constant residual that fits an existing bias with a residual having an uncovered interior kink. Match width and receivers in exact merge-and-prune and joint repair.
- **Old-task retention check:** Test the residual everywhere it is owed and verify it again after the two new gates are used; count any extra carrier against the release.

### Convert release into useful, independent access

#### 07. Spend one group on two independently useful gates
- **Mechanism:** Design each gate to respond to a different family of finite requests; require either order and a later use of an actually released slot.
- **Novelty vs nearest prior art — IMPROVEMENT:** GradMax already chooses useful neutral directions; the difference tested is multi-request service at fixed width without consuming the other gate.
- **Cheapest first test:** Make two held-out request families in a rational two-input host. Compare a one-direction GradMax or readiness rule, complementary gate placement from dormant slots, and exact repair plus the same planner.
- **Old-task retention check:** Check the full old domain after renewal, each order of the two writes, and a third request outside both families.

#### 08. Make two gates jointly usable without an inference-time task ID
- **Mechanism:** Place their activation supports or bound their combined effect so that two separately authorized writes compose when tasks share contexts.
- **Novelty vs nearest prior art — IMPROVEMENT:** Task masks and the parent tree's mergeable-write contracts already provide isolation and join checks. The wager is a cheaper collision-free realization inside the converted group.
- **Cheapest first test:** Plant a shared strip where each gate alone passes the margin floor but both together fail it. Compare masked routing, independently certified gates plus a joint checker, and joint placement.
- **Old-task retention check:** Keep the common strip and both acquired targets when both edits are present; never use oracle task labels at inference.

#### 09. Address gates by what a write does, not unit index
- **Mechanism:** Attach a small semantic edit interface to the two gates, with a checked translation after permutation or positive rescaling; freeze editor requests against that interface.
- **Novelty vs nearest prior art — IMPROVEMENT:** Neural symmetry and [Git Re-Basin](https://arxiv.org/abs/2209.04836) already align parameterizations; test whether translation costs less than resolving the same effect with exact repair.
- **Cheapest first test:** Permute and rescale equal-function hosts after publishing paired effect requests. Compare fixed indices, canonical alignment, and the effect interface with matched metadata.
- **Old-task retention check:** Recheck old domains and both realized effects, including a replaced slot with the same index but a different meaning.

#### 10. Reclaim groups when readers cannot pause
- **Mechanism:** Stage the two-gate conversion across a minimal set of jointly updated reads, or refuse if no admissible sequence of individually safe writes exists.
- **Novelty vs nearest prior art — IMPROVEMENT:** Atomic publication and the parent's make-before-break lineage are standard. The question is whether group witnesses reduce the scratch or publication scope needed at equal guarantees.
- **Cheapest first test:** Enumerate in-place schedules for the triple with zero and one scratch slot, then compare to generic transactional repair with the same isolation and scratch.
- **Old-task retention check:** Evaluate all reader-visible states and then take one useful reclaimed-slot write; a safe endpoint must not excuse a transient violation.

#### 11. Keep the optimizer from resurrecting a retired circuit
- **Mechanism:** Assign freed slots new optimizer state and transfer old state to surviving carriers only when its allowed next steps are certified.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Continual backprop](https://arxiv.org/abs/2306.13812) already couples unit recycling with reset. Joint release adds the hazard that residual momentum can break a safety relation that was exact at publication.
- **Cheapest first test:** Plant unequal momentum on the live triple; compare reset, a projected next step, and checked state transfer at matched learning steps, bytes and gate utility.
- **Old-task retention check:** Keep old domains during renewal and after the first optimizer step and later useful write; do not inspect only the checkpoint.

#### 12. Sell only cancellation the deployed arithmetic honors
- **Mechanism:** Use sign, scaling and accumulation constraints to seek a bit-exact conversion under the deployed numerical semantics; expose infeasibility instead of rounding away a residual.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Integer-only quantization](https://arxiv.org/abs/1712.05877) and equivalence checking already handle the arithmetic. The target is the cheapest way to keep a group spendable under it.
- **Cheapest first test:** Use a tiny enumerated fixed-point input grid with overflow and rounding cases. Compare float-exact compaction plus deployment recheck with integer-native search and an equally priced no-release control.
- **Old-task retention check:** Compare actual outputs on the complete declared quantized domain after conversion and keep the floors after the gates are exercised.

### Replenish after the gates carry obligations

#### 13. Fold spent gates into compatible live carriers
- **Mechanism:** Transfer both installed gate contributions to already occupied receivers on the union of live domains, then rebuild the released gate slots without restoring the prewrite checkpoint.
- **Novelty vs nearest prior art — IMPROVEMENT:** Witness 2 is a direct instance of Neuron Merging plus reset; the operation by itself is not a new primitive.
- **Cheapest first test:** Use the compatible and incompatible halves of Witness 2 and demand a third useful write. Compare merge-and-prune, PackNet-style reserve, and generic exact repair plus reset.
- **Old-task retention check:** Require exact equality on the original and newly installed domains during folding, then retain both gate writes after the third one.

#### 14. Fold two spent gates that cannot be absorbed separately
- **Mechanism:** Search for a joint transfer into shared receivers subject to bounds on existing weights; the feasibility constraint is on the sum of the spent duties.
- **Novelty vs nearest prior art — IMPROVEMENT:** Joint linear feasibility already covers it, unlike greedy pairwise merging. The wager is that joint folding returns materially more usable slots at equal total cost.
- **Cheapest first test:** On `[-1,1]`, give two spent units contributions `[x+2]₊` and `[1−x]₊`, with fixed existing receivers spanning only constants. Their joint residual is constant, while neither contribution can be folded alone. Compare greedy folding plus repair with an exact joint solver; include a changed slope that breaks the cancellation.
- **Old-task retention check:** Preserve the full pre-fold function and every live reader; declare the negative case infeasible under those receivers, and check retention after the third write.

#### 15. Keep a receiver available until the last promised fold
- **Mechanism:** A paid reservation commits part of a compatible receiver's writable range to a future fold; revoke only from a state with an independently verified substitute or with the contract explicitly expired.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Resource reservations and safe-region planning are old; the candidate is a reusable contract between separately learned writes to support their later joint retirement.
- **Cheapest first test:** Reveal a competing useful write before the fold demand. Compare a static reserve, price-based reservation, and exact retirement planning with the same options and clocks.
- **Old-task retention check:** Preserve the old and both spent-gate behaviors during the conflict, the eventual fold, and use of recovered slots; count any refused competing utility.

#### 16. Budget overlapping release groups without double-counting
- **Mechanism:** Maintain a release hypergraph whose edges include affected slots, receivers, and obligations. Two valid releases may conflict or only become possible in one order.
- **Novelty vs nearest prior art — IMPROVEMENT:** Set packing and the parent's budgeted simulation already cover static conflicts and ordered planning, respectively; exploit group structure only if it beats them on actual reclaimed work.
- **Cheapest first test:** Build three small triples where the cheapest immediate release destroys two later releases. Compare greedy, static exact packing, and exact on-demand scheduling with the same checks.
- **Old-task retention check:** Verify every accepted transition and every prior installed task after the winning schedule consumes its slots.

#### 17. Learn today's write with tomorrow's fold destination
- **Mechanism:** Among equally useful current writes, train for an exact, bounded fold into existing receivers once another compatible duty arrives; do not expose the test companion to training.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Compressibility training and elastic growth/pruning already prepare for compaction. The stronger claim is blind, continuation-specific renewability above matched compression-aware training plus exact repair.
- **Cheapest first test:** Use held-out companion families in a four-slot rational host, with planted incompatible companions. Match initial utility, sparsity and old retention before using the same joint solver on both hosts.
- **Old-task retention check:** Preserve all preexisting tasks and current utility before the companion, after the joint fold, and after the reclaimed pair serves a new target.

#### 18. Measure the first genuine exhaustion point
- **Mechanism:** Treat repeated conversion, installation, and folding as a fixed-width game with obligations that do not expire; look for an inductive renewal set or a short exhausting request sequence.
- **Novelty vs nearest prior art — IMPROVEMENT:** This specializes the parent's simulation and invariant planning. A nontrivial result needs new persistent duties, not repeated reinstalls of the same gate or a planted expiration rule.
- **Cheapest first test:** Enumerate bounded rational states for a small receiver dictionary; contrast recurring compatible duties with demand for distinct indispensable kinks, using the same exact planner with and without learned placement.
- **Old-task retention check:** Re-evaluate every acquired domain after every release and subsequent write; exhaustion is failure to admit useful new work, not permission to evict an old task.

### Test whether the reserve remembers anything

#### 19. Train the arrangement to remember a family of demands
- **Mechanism:** Use past requests to shape which live supports are cheap to convert while keeping the protected function and current width fixed. Later editors come from held-out instances of those families.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Teleportation already chooses a same-function representation for trainability; the test is persistent, family-specific access supplied to an independent finite editor, beyond matched meta-training for plasticity.
- **Cheapest first test:** Train on two opposed mixtures of past requests and cross both hosts with identical blind editors and exact solvers. Include a family-swap negative and a uniform dormant-gate control; match pre-edit scores on test targets so the reserve cannot simply pre-answer them.
- **Old-task retention check:** Require the same protected function at handoff, retain all old floors through independently requested writes, and measure any worsening on the nonfavored family.

#### 20. Erase only the proposed memory and ask what stops working
- **Mechanism:** Recompile the learned arrangement at matched function, width and free-slot count, without using demand history. Separate harmless gauge changes from recompilations that destroy release structure.
- **Novelty vs nearest prior art — IMPROVEMENT:** Hidden symmetry and the ledger's failed Noether channel already motivate gauge controls. This is a causal discriminator between selective stored access and a generally better checkpoint, not a new storage mechanism.
- **Cheapest first test:** Compare the original, a permuted/rescaled copy with translated edits, and a neutral recompilation. Match off-domain test predictions where possible; exclude any example whose pre-edit target prediction differs from the causal comparison otherwise.
- **Old-task retention check:** Verify the same old function after every transformation and the same acquisition floors after edits; do not credit a selective loss that is already present before writing.

#### 21. Put the same hint budget outside the weights
- **Mechanism:** Trade learned group placement for an explicit same-budget table of edit-family hints or cached compaction plans, leaving the generic editor unchanged.
- **Novelty vs nearest prior art — IMPROVEMENT:** An adapter bank or compiled repair cache is the obvious memory control. A learned reserve is interesting only if it generalizes better or costs less end to end.
- **Cheapest first test:** Freeze host width; compare neutral placement with a past-request-only cache under a common total-byte cap, allowing each arm to spend its remaining bytes on proofs or hints. Test repeats and new family members separately.
- **Old-task retention check:** Match the old function and all old floors in both arms, and try to falsify any apparent gain with the cache allowed the same generic repair and verification.

#### 22. Hand off a release witness when its training source disappears
- **Mechanism:** Store a small checkable certificate for a family of supported conversions tied to cell and state preconditions, not to replay of the optimizer trajectory that produced the group.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** Proof-carrying repair and the tree's [entry-port certificates](https://github.com/manojbajaj95/cl/pull/171) already separate proof from history; the possible increment is cheap reuse across independent edits that change the available support.
- **Cheapest first test:** Delete preparation traces and give a second editor three support-changing edits: commuting, overlapping, and one beyond the advertised scope. Compare versioned certificates against exact recheck and a byte-matched proof cache.
- **Old-task retention check:** Verify old and acquired domains on accepted imports; fail closed on stale evidence and confirm a use of the newly released slots.

#### 23. Map where higher arity buys real usable capacity
- **Mechanism:** Vary protected cell and readout structure, then measure the minimum group size that actually frees a usable slot after retaining two gates and all carriers.
- **Novelty vs nearest prior art — IMPROVEMENT:** Matrix spark and minimal support already describe algebraic dependencies. The study asks where this bound stops predicting finite release because real readers, activation changes, or continuation debt dominate.
- **Cheapest first test:** Enumerate rational hosts with identical nullity but different smallest feasible release arities, including no-release cases. Compare kernel-based prediction, exact minimal support, and the exact finite-move oracle.
- **Old-task retention check:** Require cellwise equality and a useful reclaimed-slot write for every counted frontier point, at the same old floors and new utility threshold.

#### 24. Keep only the differences a blind editor can spend
- **Mechanism:** Quotient alternative neutral arrangements by budgeted continuation behavior, not group identity: retire an arrangement only if a retained one simulates its useful responses and successors.
- **Novelty vs nearest prior art — IMPROVEMENT:** The parent's alternating simulation already supplies the criterion. Group witnesses might make the proof cheaper; a shared nullity or a shared next-step menu is not equivalence.
- **Cheapest first test:** Construct two hosts with the same available first releases but different second folds, plus a harmlessly permuted duplicate. Compare raw caching, next-step pruning and exact budgeted simulation with and without group summaries.
- **Old-task retention check:** Replay distinguishing suffixes and check all acquired obligations at each transition; refuse to discard the branch that alone supports a later useful retained edit.

## Ranked deeper questions

1. **Can learning store family-specific release opportunities, rather than just favorable initial outputs or a faster solver?** Start with 19–21: cross prepared hosts and common release methods, then erase and swap demand families. Require more useful frozen requests served or lower total cost at matched retention and pre-edit target outputs. If a same-budget explicit cache or matched compaction-aware training ties, call it an alternative implementation.
2. **When does a group of arity greater than two create net new usable capacity?** Use 01–06, 07 and 23. Demand two complementary gate writes and a third on an actually unreserved slot. A separation from pair-only is necessary but insufficient; if the matched sparse-compaction and exact-repair stack ties, group discovery is an improvement.
3. **Can useful gates be spent, folded and rebuilt repeatedly without taking back their utility?** Use 13–18. Require more than one paid return with non-expiring duties; count all receiver and staging costs. For an indefinite claim, require a nonempty invariant under declared demand, or report the shortest exhausting sequence. A planted compatible fold is only a positive control.
4. **Can a second editor verify and spend the reserve cheaply after the source is gone?** Use 03, 09, 22 and 24. Let an independent editor alter supports and bring stale or adversarial requests. Require savings over generic exact checks plus caching without weakening scope or retention; otherwise the certificate is ordinary verification metadata.

**Verdict:** The triple shows why looking past pairs is worthwhile, not why the host has a new memory. The best case for a primitive is a learned, finite, renewable release opportunity that later editors can independently cash out. If guarded compaction, recycling and a paid hint cache account for the gain, keep the engineering improvement and drop the memory claim.
