# Producer rewrites: close the norm seam and renew the same park

**Status:** Ideas only; two paper fixtures, no pilots, training runs, or GPU work. **Parent:** [Seam leaks](seam-leaks.md) ([PR #237](https://github.com/manojbajaj95/cl/pull/237)), cards 04 and 15, the two score-3 ideas in [flood triage, row 350][triage]. **Ledger read first:** [Idea ledger][ledger]. `P` is a conditional primitive; `I` is an improvement, restatement, or falsifier. An invariant by construction is a sanity check, not evidence of an advantage.

## Two contracts, not just two endpoint tests

- **Rewrite the producer before deletion.** Freeze the retained interface, the reachable histories `H(p)` compatible with each public transcript `p`, the permitted reader family, and its horizon. Replace the norm-writing recipe with one shared `F*`. After deleting the specified record and its derivatives, run `F*` using only permitted surviving inputs: no old log, per-history table, selection on hidden history, or backup copy of the deleted norm. Live old-task slots may still differ if licensed to remain. For each public input and coupled public seed, require `scale_R(F*(s), p) = scale_R(F*(t), p)` for every `s,t ∈ H(p)` and permitted reader `R`. Also compare effective edit traces: a common scale does not excuse a direction, gate, clock, or later read that still leaks. Scales may differ between genuinely public inputs. Preserve the specified other old-task effects of the producer, including delayed ones; equal scale with a no-op editor does not count.
- **Renew one fixed park.** Choose a public park value, public park–edit–clear script family, and a small, published invariant `K` before the future B targets and old update orders arrive. A public description of `K` is not a licence to query its private coordinates live. Prove that each allowed truthful old update maps every compatible state at its entry into `K` at its next editor-ready boundary, including `U_e(K) ⊆ K` for the allowed arrivals once ready. With a declared scheduler, discharge these obligations for each reachable scheduler context; apply induction to all allowed orders, not just shuffled samples or equal endpoints. Latent endpoints can differ. If B can start between microsteps, certify those cuts too; otherwise advertise and charge the wait. Preserve old service throughout the updates, the park, clear, and continuation. No re-parking choice, per-order restore, or recertification at each arrival in the proposed arm.
- **Test both utility and cost.** A is ordinary old service, C an independent rare-old obligation, and B useful new edit progress. Match normal A/C performance, truthful data and update budget, and realized B gain or report a frontier. Check A/C separately in every history at served prefixes, commit/clear, and a nontrivial continuation; count refusals and waiting. Charge preparation, validation and proof work, resident and transient bytes, width, and latency. Compare seam rejection, a slot reset, a fixed clip threshold, the strongest lawful **public** scale schedule (including consumer-side replacement if it can tie), and GEM-style constraints. Compare a one-time park, drift-certificate transport (parent's #224#21), GEM, exact planning with fresh recertification/re-parking, and dual-mode old training. For joint cards stack the best legal separate controls; a per-history oracle is a diagnostic only.

**Prior-art floor.** [Weight normalization][wn] separates magnitude from direction; [adaptive group gradient clipping][aggc] isolates norm spill-over but its EMA is history-sensitive. Neither is evidence that replacing a seam producer beats an equally expressive public reader rewrite. [GEM][gem] protects old tasks with episodic gradients, and [ROGO][rogo] already studies a relaxed gradient projection without a memory buffer. [Robust output barrier functions][barrier] already certify invariance with partial observations, and [GraB][grab] chooses advantageous orders. The open bets are retaining useful producer dynamics while deleting the controlling norm record, and returning to **one reusable editing interface** without needing to choose or observe the old update order. These are nearby comparisons from a quick alphaXiv/Hugging Face Papers scan, not a priority claim.

## Two exact paper fixtures

### 1. Rewrite the emitted norm, keep the live slot

Let hidden `h ∈ {−1,+1}` select a reachable live old slot `m=h`. A fragment receives `z=n·d_h`, where `n=(3+h)/4` and `d_h=(3h/5,4/5)` has unit Euclidean norm. Treat the stored norm record as deletable; `z` is the fragment's live input, not a saved record. The original fragment produces `||z||₂=n` as a clip threshold and uses the direction `z/||z||₂` for its local old-task path. A later editor clips a public unit proposal to that threshold. The one rewritten executable normalizes `z`, feeds the same direction to the local path, and emits the norm of `(3/4)·(z/||z||₂)`, namely `3/4` in both histories. It never selects a recipe or restores a deleted record. This is an action-level invariant for the downstream editor, not erasure of information from `z` or `m`.

| `h` | Original unit-proposal action | Rewritten action (B target `3/4`) | Retained direction | Live slot |
|---|---:|---:|---|---:|
| −1 | 1/2 | 3/4 | (−3/5, 4/5) | −1 |
| +1 | 1 | 3/4 | (3/5, 4/5) | +1 |

For an explicit old-service check, A scores `1−|d₁−3h/5|` and delayed C scores `1−|m−h|/2`, each with floor `3/4`. Both score 1 on either rewrite path; resetting `m` leaves C at `1/2`. A fixed `3/4` clamp with the original local direction and slot ties exactly for this one reader. A second reader emitting `m` as an edit signal would invalidate the trace proof, regardless of equal scale. Zero `z` is outside the two-history fixture and must be specified and checked if admitted.

### 2. Renew a park without synchronizing the host

State `(u,v)` starts with `|u|≤1`, `|u+v|≤1/4`; `u` is a live old-task feature. A truthful old label `t∈{−1,+1}` gives `u'=(u+t)/2`, the half-step toward its squared-error target. The park-aware update writes `v'=-u'` in the same published atomic transaction. Thus every arrival returns to `K={|u|≤1, u+v=0}`. For example, from `(0,0)` orders `(+1,−1)` and `(−1,+1)` yield `u=−1/4` and `u=+1/4`, respectively. Both renew the exact same licence; the host neither sees an order-dependent editor choice nor converges to one latent state.

Let normal A score `1−|u|/8` and parked C score `1−|u+v|`, both with floor `3/4`. B requires writing a bit while a gate is at the fixed public value 0 (and then clearing the gate to 1); assume neither bit nor gate changes these scores and use C also as the clear check. After every atomic update A is at least `7/8` and C is 1. If the same two writes are exposed separately, the first `+1` from `(0,0)` momentarily gives `u+v=1/2` and fails C. If vanilla training leaves `v=0`, either first label fails the subsequent park at C=`1/2`. An exact projection onto `v=-u` with the same atomicity ties by construction. This example only checks the contract; it does not show meaningful B gains or that learning the invariant beats projection.

## Idea cards

### Change what the norm producer actually makes

#### 01. One producer, two outputs (I; #237#04)
- **Mechanism:** Separate the export norm from the old-task update, preserving the live direction and slot transition; compile one replacement before deletion.
- **Novelty vs nearest prior art:** The review seed with [weight normalization][wn] as a building block, not a new normalization rule.
- **Cheapest first test:** Exhaust fixture 1 plus a public proposal of `1/4`; compare the strongest public clamp and slot reset. Expect the clamp tie.
- **Old-task retention check:** Score A after the producer and C after the slot-consuming continuation; exclude a rewrite that launders its loss through a failed reset control.

#### 02. Learn a right inverse for the norm and the old update together (P)
- **Mechanism:** Parameterize only variants in the inverse image of the required old output and prescribed public norm. Search before deletion for a shared map through that intersection, not a different inverse for each history.
- **Novelty vs nearest prior art:** [ROGO][rogo] relaxes a projection for plasticity; here the target is a reusable inverse-image map for a norm producer subject to a separate live old-output constraint.
- **Cheapest first test:** Enumerate rational 2D producer stencils with one old linear read and one public norm; include an empty intersection and benchmark project-then-rescale plus reader substitution.
- **Old-task retention check:** Add a withheld C read in the correction direction and require no loss on the next actual update, not just preservation of the fitted linear read.

#### 03. Share a public scale curve, not a constant (I)
- **Mechanism:** Emit a deterministic public curve of proposal class and phase from a rewritten estimator; certify each class across all aliases without routing on their latent slots.
- **Novelty vs nearest prior art:** [AGGC][aggc] uses groups and time; replacing EMA with a public schedule is a control, not in itself a new operation.
- **Cheapest first test:** Use two public proposal classes with disjoint B-useful scale intervals; compare one fixed clamp, a parameter-matched public reader schedule, and the rewrite. The latter two should tie if only the exported scalar matters.
- **Old-task retention check:** Check rare C at both ends of each scale interval and on alternating classes; no credit for the class a method had to refuse.

#### 04. Cancel private magnitude before taking the norm (P)
- **Mechanism:** Arrange existing producer channels so a public linear map removes their shared private nuisance component before norm computation. Preserve downstream old readers of the uncombined channels; do not concatenate a backup.
- **Novelty vs nearest prior art:** Projection and paired cancellation are known. The candidate operation factors a live multi-channel producer so a buyer can delete the old norm history and retain useful original readers.
- **Cheapest first test:** Enumerate `(a+r,b+r)` over a small rational grid and verify `|a−b|` after a second old update; compare group clipping and a public reader schedule with untouched local outputs. Break one channel's nuisance coefficient as a negative case.
- **Old-task retention check:** Give A and C separate channel reads and a delayed contrastive read; reject cancellation that removes needed information from the channels themselves.

#### 05. Make the rewriting rule equivariant, but only expose its invariant (P)
- **Mechanism:** Learn one shared basis change under which reachable histories differ by a norm-preserving group action. Emit that invariant norm, retain covariant internal directions for authorized old work, and prove later moments don't convert direction into scale.
- **Novelty vs nearest prior art:** [Weight normalization][wn] separates directions and magnitudes; the new candidate is a transferable orbit-based norm contract for independently reused producers and their live slots.
- **Cheapest first test:** Enumerate signed permutations of 2D slots, then add an anisotropic preconditioner that breaks the orbit. Compare explicit public magnitude substitution plus exact continuation checking.
- **Old-task retention check:** Check C after the first asymmetric old update and A on all orbit members; a clean first scale is insufficient.

#### 06. Rewrite the recurrence, not each emitted sample (P)
- **Mechanism:** Split an EMA-like producer into a public driving recurrence for the export and a separate retained private correction used only for old service; use a fixed state map before deleting the old scalar accumulator. Justify the bytes by reusing existing slots.
- **Novelty vs nearest prior art:** [AGGC][aggc] has adaptive norm recurrences. The proposed object is a continuation-preserving decomposition that can remain closed across new requests without another purge.
- **Cheapest first test:** Model a two-slot rational recurrence with public input and private signed residual; test all length-three suffixes and a feedback edge from the residual. Compare clamping plus unmodified private EMA, slot reset, and exact state aggregation.
- **Old-task retention check:** Make C depend on the residual after two updates; prove retaining it does not recreate an edit-side scale read.

#### 07. Compile one vector statistic for several mismatched consumers (P)
- **Mechanism:** Solve for a shared statistic in the joint equal-scale preimage of the clip, trust-ratio, and gating readers. Preserve the producer's old outputs and compile under fixed ABI/width rather than patch each reader separately.
- **Novelty vs nearest prior art:** The parent certifies a reader family; this synthesizes a common producer for that family. Contract composition and per-reader clamps remain controls.
- **Cheapest first test:** Use three tiny rational reader functions, with pairwise feasible but jointly infeasible constraints as a negative. Compare independent clamps (where allowed), exact whole-script repair, and rewritten export.
- **Old-task retention check:** Interleave all three readers and a rare C refresh; check A/C even when a jointly infeasible request must refuse.

#### 08. Choose the rewrite that survives lowering to finite precision (I)
- **Mechanism:** Treat rounding, accumulation order, overflow and zero norm as part of the producer contract; seek a shared stencil whose rounded scales, trace and timing agree.
- **Novelty vs nearest prior art:** Relational finite-precision verification applied to the parent's norm seam, not a learning primitive.
- **Cheapest first test:** Enumerate an 8-bit accumulator around a rounding tie and a saturation edge; compare exact fixed-point lowering, a public reader replacement, and real-valued equality alone.
- **Old-task retention check:** Score A/C on every reachable quantized edge and continuation, including zero input if admitted; refuse unsupported ranges rather than quietly weakening the floor.

#### 09. Certify a deletion counterfactual, not just a zeroed buffer (I)
- **Mechanism:** Retire the log and all unauthorized derivatives, then replay the same public suffix while independently varying reachable surviving slots. Check allocations and actual edit sinks as well as nominal scale.
- **Novelty vs nearest prior art:** The parent's whole-program relational check plus liveness/deletion auditing; this is an adversarial validation protocol.
- **Cheapest first test:** Use twins where poisoning a supposedly retired normalizer cache changes a delayed scale, and a harmless private old-service slot negative control. Compare zeroing the named buffer and exact read tracing.
- **Old-task retention check:** Measure C on the slot-sensitive suffix; neither reading a forbidden cache nor indiscriminately zeroing authorized state passes.

#### 10. Produce an obstruction, not a bespoke history branch (P)
- **Mechanism:** For each allowed producer grammar, bound the intersection of old-effect-preserving realizations and common useful norm scales. Export a witness that can be reused to prune downstream edit plans, or show exactly which declared restriction must change.
- **Novelty vs nearest prior art:** Parent #09 proves disjoint useful actions; this obstruction concerns realizability under a common producer and separates producer limitations from the possibility of a consumer-side repair.
- **Cheapest first test:** Enumerate linear stencils over a two-point domain where the only permissible producer norm differs; add one legitimate public reader override and check that the obstruction does not rule it out.
- **Old-task retention check:** Give C a strict lower bound on the producer's local amplitude. Run the lawful refusal fallback and compare against any proposed rewrite on the same floor.

### Train the old updates to return to the same park

#### 11. Learn closure, not just parked accuracy (I; #237#15)
- **Mechanism:** Fit the old transition rule to re-enter one small `K` on all reachable members of each belief class at the next editor boundary. Freeze the park and verify each arrival type.
- **Novelty vs nearest prior art:** The score-3 parent seed; [robust output barriers][barrier] already supply an invariance template. Require a reusable B licence beyond ordinary robust old service.
- **Cheapest first test:** Exhaust length-three binary arrivals on fixture 2 and one held-out initial state in the declared range; compare exact projection, a one-time park, and fresh recertification.
- **Old-task retention check:** Measure A/C after every arrival and at the next park–edit–clear path; show that the admitted old updates actually improve their truthful objective somewhere.

#### 12. Replenish parked safety using the useful old update itself (P)
- **Mechanism:** Learn a coupling that translates the correction toward an old-task target into repair of the exhausted park margin, with no extra replay step and with a proof for arrivals pointing either way.
- **Novelty vs nearest prior art:** [GEM][gem] constrains updates and parent #15 enforces return; the new candidate is a *joint useful correction and recovery* rule that earns a park renewal at no extra arrival, if it beats their stack.
- **Cheapest first test:** In a 2D rational host, choose two opposing truthful labels and one low-margin entry. Compare projected SGD plus exact re-parking, and include a label whose only progress directions make return impossible.
- **Old-task retention check:** Check frequent A and rare C across the weak-margin entry, repair, and B suffix; report the old update's realized learning gain instead of calling rejected updates renewals.

#### 13. Quotient the old transitions by what the next editor can do (P)
- **Mechanism:** Learn a low-dimensional quotient of the host on which each old arrival has a certified return map; keep different optimizer states live while the quotient determines the same park licence. Do not dynamically select the park by reading the quotient.
- **Novelty vs nearest prior art:** Exact state aggregation already supplies a quotient test. The candidate is a learned quotient for continuing park usability rather than equality of trajectories or predictions.
- **Cheapest first test:** Compare a two-moment summary to exact partition refinement on a finite quantized optimizer; include an alias with the same score but an out-of-class next moment.
- **Old-task retention check:** Apply a delayed rare C probe after moments evolve and after B clears; reject a quotient that hides a C failure even if park eligibility agrees.

#### 14. Prove a whole belief class with a small set of extreme states (I)
- **Mechanism:** Publish a compact polytope and certify return for affine arrival maps by checking its vertices; partition a piecewise affine optimizer only where a change of regime matters.
- **Novelty vs nearest prior art:** Robust invariant-set analysis; this would make the park proof cheaper, not introduce a new invariant principle.
- **Cheapest first test:** Compare vertex enumeration with exhaustive finite-state checks for a 2D host. Add an interior clipping kink where checking only the original vertices is unsound.
- **Old-task retention check:** Check worst A/C over the whole certified region and validate breakpoints independently; a cheap outer approximation must count its refusals.

#### 15. Let order effects survive only in parked-null directions (P)
- **Mechanism:** Permit noncommuting old updates; train them so their order-dependent component stays in a subspace respected by every later old update and invisible to the fixed B script, while retaining useful old-task differences there.
- **Novelty vs nearest prior art:** [GraB][grab] chooses a good order, and requiring commutation removes order differences. The candidate trains the editor's null relation to absorb *propagated* order effects without forcing the host to commute.
- **Cheapest first test:** Use two noncommuting rational affine maps with a one-dimensional visible quotient; add a third map that turns the hidden commutator into a visible gate shift. Compare GraB, full commutation, and dual-mode training with fresh certificates.
- **Old-task retention check:** Demonstrate order-sensitive but lawful old learning, and measure A/C after both orders, the propagating suffix, and the same B script.

#### 16. Renew the interface during a non-atomic old update (P)
- **Mechanism:** Reparameterize the old write in a tangent basis or learn a certified sequence of individually safe writes so service and park availability survive preemption, not merely the atomic commit.
- **Novelty vs nearest prior art:** Hybrid barrier reasoning and transactions already supply safe switching and isolation. The candidate is uninterrupted blind editing without making every correction atomic or freezing old learning.
- **Cheapest first test:** Expose the split write in fixture 2; compare atomic writes, a one-coordinate `(u,q=u+v)` reparameterization, and a bounded microstep plan. Charge latency and count actual interruption opportunities.
- **Old-task retention check:** Interrupt at every served prefix, perform B where advertised, and score A/C after resumption and clear. A hidden stall is not continuous availability.

#### 17. Learn against counterexample orders, certify against all in scope (I)
- **Mechanism:** Alternate fitting the old updater with a verifier that returns a reachable entry and spoiling order; freeze both rule and invariant before final proof.
- **Novelty vs nearest prior art:** Counterexample-guided synthesis and robust barrier fitting; a practical search strategy, not a novel proof claim.
- **Cheapest first test:** Plant a three-arrival failure whose pairs pass; compare counterexample-guided training, random permutations, and exhaustive training at equal search budget. Keep the final verification domain explicit.
- **Old-task retention check:** Check A/C on the repaired order and withheld episodes, including old utility lost because the correction was weakened to fit `K`.

#### 18. Make closure compositional across independently trained arrival rules (P)
- **Mechanism:** Publish a fixed park contract covering safe intermediate reads and post-boundary return, then allow independently built old-task updaters to prove that contract before deployment. Do not change the park when a newcomer fails.
- **Novelty vs nearest prior art:** Contract composition is standard. The bet is that independently trained useful old updates preserve one live editing interface more cheaply than recompiling a joint policy after each arrival type is added.
- **Cheapest first test:** Train or enumerate two tiny affine old updaters separately, check all interleavings with a third proposer, and compare joint training and exact recertification. Include individually safe maps that violate the common return contract.
- **Old-task retention check:** Test every updater's original A/C plus cross-service C after swapping the producer order and clearing B; score rejection of the incompatible updater.

### Look for a joint effect, not two successes counted twice

#### 19. Have park renewal restore the producer's norm law (P)
- **Mechanism:** Design `K` so each old update returns the producer's norm-bearing inputs to a public-scale equivalence class while leaving authorized private behavior live. Require the post-deletion producer to reuse the same rewrite after every arrival.
- **Novelty vs nearest prior art:** Parent #19 parks a dependency away; this requires useful old training to restore the producer law and retire repeated seam and park checks together.
- **Cheapest first test:** Couple a two-channel norm stencil to fixture 2 and hold out arrival order. Compare a public clip schedule plus projected old updates plus cached exact checks; include a deployment where that stack ties.
- **Old-task retention check:** Score A/C before and after each renewal, at B commit, and on an old suffix that reads the preserved channels; audit scale again after clear.

#### 20. Admit a mid-edit old arrival only under a common return proof (P)
- **Mechanism:** Prove a staged B script remains on the same public phase and uses the same next scale after an old update, even when private slot differences survive the arrival. The update must re-enter `K` for the current phase, not jump back to an initial state.
- **Novelty vs nearest prior art:** Parent #20 certifies interrupted seams; this candidate equips the updater to return the interrupted phase to the learned interface rather than wait or synthesize a replacement suffix.
- **Cheapest first test:** Use two B phases, two arrival types, and all legal placements. Compare serialization with cached certificates plus a public clamp and dual-mode training; force one arrival to violate a later reader's scale domain.
- **Old-task retention check:** Check A/C before, during and after the arrival and clear; count B deadlines rather than declaring a stalled run safe and successful.

#### 21. Find the smallest public interface worth maintaining (P)
- **Mechanism:** Co-synthesize a shared producer stencil and small `K` across independently proposed reader/update families. Prove a lower bound on certificate size or retained bytes needed for the same lawful B coverage.
- **Novelty vs nearest prior art:** Parent #02 indexes a certificate by consumers; exact quotients compress state. The candidate is a joint complexity frontier for two reusable interfaces at once, not simply a smaller manifest.
- **Cheapest first test:** Enumerate a finite host with two readers, two truthful arrival maps, and two public interface sizes. Compare separately minimized interfaces and their best stack; demand a strict achievable-frontier difference.
- **Old-task retention check:** Require normal A/C and both parked floors across every claimed point on the frontier. Include a rare C alias that makes the one-bit interface insufficient.

#### 22. Search for the strongest legal tie first (I)
- **Mechanism:** Put the best public reader replacement, unchanged legitimate slot dynamics, ordinary projection or dual-mode training, and cached certifier in one baseline. Impose the same deletion and park contracts on all arms.
- **Novelty vs nearest prior art:** The ledger's stacked-control rule; the goal is to kill artificial gains from weak clamps or rechecking everything from scratch.
- **Cheapest first test:** Cross both fixtures and one coupled negative example before any broader CPU search. Count accepted useful B edits, preparation and proof work, pause time, and bytes; don't nominate a merged primitive if independent solutions tie.
- **Old-task retention check:** Require the same per-history A/C floors at every served prefix and after a real suffix, including honest refusals and fallback operation.

## Ranked deeper questions

1. **Can a producer-side rewrite free a useful B edit that the strongest legal public reader replacement cannot, while keeping the producer's other old effects?** Start with #02/#06/#07 and #22. Find a genuine coupling to live transition state or an independently fixed reader ABI; if both sides can implement the same lawful public schedule while preserving the private path, keep the simpler one. Demonstrate an actual deletion and nontrivial continuation, not just algebraic equality.
2. **Can a small learned `K` remain inductive under useful truthful old learning, without a per-arrival projection or certifier that ties it?** Compare #12/#13/#15 to the projected and cached baselines. Seek the smallest order that disproves closure and a paired check that separates loss of closure from rare C forgetting. Require gain on old arrivals, not preservation by freezing.
3. **Can renewed availability buy a B deadline that isolation cannot, even after accounting for the return boundary?** Use #16/#20 to examine every interruptible prefix. If the proof needs a transaction that stalls B just as long as serialization or restoration, report the tie.
4. **Is there a strict joint benefit at matched bytes, training and proof cost?** Compare #19/#21 to #22; look for a shared return-and-rewrite certificate that admits more of the same B requests or retires more actual state without losing either old floor. If proof maintenance costs as much as the stack, retain separate contracts.

**Verdict:** The exact fixtures check blindness and renewal but tie lawful public clamping and atomic projection, respectively. Advance only a case with demonstrably useful post-deletion reuse or order-robust B availability beyond the strongest legal stack.

[ledger]: https://github.com/manojbajaj95/cl/blob/c9d08e7d73f0e83077e9915fc1915925146784e8/reviews/idea-ledger.md
[triage]: https://github.com/manojbajaj95/cl/blob/c9d08e7d73f0e83077e9915fc1915925146784e8/reviews/flood-triage.md#L350
[wn]: https://www.alphaxiv.org/abs/1602.07868
[aggc]: https://www.alphaxiv.org/abs/2601.11864
[gem]: https://huggingface.co/papers/1706.08840
[rogo]: https://huggingface.co/papers/2301.12131
[barrier]: https://www.alphaxiv.org/abs/2111.09971
[grab]: https://www.alphaxiv.org/abs/2205.10733
